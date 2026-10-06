"""Tiny-model collection and prospective swap decode. Real weights stay pending_server."""
from __future__ import annotations

import hashlib
import inspect
import numpy as np
import torch

from ..interventions import apply_swap, orthonormal_basis
from ..protocol import stable_row_key
from .adapters import as_input_ids, model_device
from .features import select_prefix_index
from .generate import decode_loop
from .tiny import build_tiny, resid_post_hook
from .tokenize import readout_layer_index, span_token_indices


def _n_layers(model) -> int:
    inner = getattr(model, "model", model)
    layers = getattr(inner, "layers", None)
    if layers is not None:
        return len(layers)
    cfg = getattr(model, "config", None)
    n_layers = int(getattr(cfg, "num_hidden_layers", 0) or 0)
    if n_layers < 1:
        raise ValueError("cannot determine layer count")
    return n_layers


def _capture_forward_output(model, token_ids, layer: int | None = None, **kwargs):
    """Capture a hidden boundary without Transformers output flags."""
    inner = getattr(model, "model", model)
    if layer is None:
        module = getattr(inner, "norm", None)
        label = "final norm"
    else:
        layers = getattr(inner, "layers", None)
        if layers is None or layer < 0 or layer >= len(layers):
            raise ValueError(f"invalid hidden layer: {layer}")
        module = layers[layer]
        label = f"layer {layer}"
    if module is None:
        raise ValueError(f"model has no module for {label}")
    captured = []

    def hook(_module, _inputs, output):
        captured.append(output[0] if isinstance(output, tuple) else output)

    handle = module.register_forward_hook(hook)
    try:
        clean_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        output = model(input_ids=as_input_ids(token_ids, model), **clean_kwargs)
    finally:
        handle.remove()
    if not captured:
        raise RuntimeError(f"hidden capture did not fire for {label}")
    return output, captured[-1]


def _hidden_at_layer(model, token_ids: list[int], layer: int) -> np.ndarray:
    cap = int(getattr(getattr(model, "config", None), "max_position_embeddings", 0) or 0)
    if cap and len(token_ids) > cap:
        raise ValueError(f"trace length {len(token_ids)} exceeds model context {cap}")
    model.eval()
    with torch.inference_mode():
        options = {"logits_to_keep": 1} if "logits_to_keep" in inspect.signature(model.forward).parameters else {}
        _fwd, hidden = _capture_forward_output(model, token_ids, layer=layer, use_cache=False, **options)
    return hidden[0].float().detach().cpu().numpy()


def collect_hidden_trace(
    kind: str,
    token_ids: list[int],
    offsets: list[list[int]],
    events: list,
    premises: list,
    weight_seed: int = 0,
    model=None,
    weight_source: str = "random_init",
    hidden_layer: int | None = None,
    prompt_text: str | None = None,
    rendered_prompt_text: str | None = None,
    strict_prompt_spans: bool = False,
    trace_id: str = "",
    task_id: str = "",
    base_group_id: str = "",
    include_nonthinking_events: bool = True,
) -> dict:
    if model is None:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(weight_seed)
            model = build_tiny(kind)
    n_layers = _n_layers(model)
    layer = readout_layer_index(n_layers) if hidden_layer is None else hidden_layer
    hidden = _hidden_at_layer(model, token_ids, layer)
    dim = hidden.shape[-1]
    positions = {"pre_step": [], "pre_value": [], "post_step": []}
    event_ids = []
    identity_keys = []
    event_records = []
    for event in events:
        event_region = getattr(event, "event_region", "unknown")
        # C1 concerns information available before a reasoning commit.  The
        # raw trace retains answer-region events for audit; they do not enter
        # the hidden-state matrix used by the scientific probe.
        c1_eligible = include_nonthinking_events or event_region in {"thinking", "unknown"}
        if not include_nonthinking_events and (getattr(event, "status", "ok") != "ok" or getattr(event, "event_kind", "commit") == "restatement"):
            c1_eligible = False
        if not c1_eligible:
            continue
        start = event.start
        value_start = getattr(event, "value_start", start)
        end = event.end
        feat = {
            "pre_step": select_prefix_index(offsets, start, "pre_step"),
            "pre_value": select_prefix_index(offsets, start, "pre_value", value_start=value_start),
            "post_step": select_prefix_index(offsets, start, "post_step", target_end=end),
        }
        pre_idx = feat["pre_step"].get("token_index")
        if pre_idx is None or pre_idx >= hidden.shape[0]:
            continue
        ident = getattr(event, "identity", None)
        event_id = getattr(event, "node_id", None) or getattr(ident, "entity_or_expression", None)
        identity_key = ident.key() if ident is not None else event_id
        event_ids.append(event_id)
        identity_keys.append(identity_key)
        event_records.append(
            {
                "row_key": stable_row_key(
                    task_id=task_id,
                    base_group_id=base_group_id,
                    trace_id=trace_id,
                    event_id=event_id,
                    identity_key=identity_key,
                    position="pre_step",
                ),
                "trace_id": trace_id,
                "task_id": task_id,
                "base_group_id": base_group_id,
                "event_id": event_id,
                "identity_key": identity_key,
                "node_id": getattr(event, "node_id", None),
                "timing": "pre_step",
                "event_region": event_region,
                "event_kind": getattr(event, "event_kind", "commit"),
                "event_phase": getattr(event, "event_phase", "unknown"),
                "expression_signature": getattr(event, "expression_signature", ""),
                "event_scope": getattr(ident, "scope", "global"),
                "event_status": getattr(event, "status", "ok"),
                "analysis_eligibility": {
                    "C1": True,
                    "C2": bool(getattr(event, "status", "ok") == "ok"),
                    "C3": bool(getattr(event, "status", "ok") == "ok"),
                    "C4": False,
                },
                "token_index": pre_idx,
                "token_position": pre_idx,
                "boundary_start": start,
                "boundary_end": value_start,
                "prefix_token_ids": list(token_ids[: pre_idx + 1]),
                "prefix_token_count": int(pre_idx + 1),
                "kv_update_range": [int(pre_idx + 1), int(len(token_ids))],
            }
        )
        for name, item in feat.items():
            idx = item.get("token_index")
            if idx is None or idx >= hidden.shape[0]:
                positions[name].append(np.full(dim, np.nan))
            else:
                positions[name].append(hidden[idx])
    if positions["pre_step"]:
        h_matrix = np.stack(positions["pre_step"])
        h_position = "pre_step"
        pre_step = h_matrix
        pre_value = np.stack(positions["pre_value"])
        post_step = np.stack(positions["post_step"])
    else:
        h_matrix = np.zeros((0, dim), dtype=float)
        h_position = "no_event"
        pre_step = h_matrix
        pre_value = h_matrix
        post_step = h_matrix
    span_source = rendered_prompt_text or prompt_text

    matched_spans: set[tuple[int, int]] = set()

    def resolved_span(premise, cursor: int) -> tuple[int, int, int, str]:
        """Resolve premise text in the exact rendered prompt coordinates."""
        if span_source:
            # The loader's ``start``/``end`` fields are coordinates in the
            # logical question.  They are not valid after a chat template has
            # added system/user markers, so every scientific span is located
            # by an exact text round trip instead.
            prefix = f"{premise.document_id}: " if getattr(premise, "document_id", None) else ""
            for needle, prefix_len in ((prefix + premise.text, len(prefix)), (premise.text, 0)):
                # Premises are not guaranteed to be stored in prompt order.
                # Prefer the old forward search, then scan from the beginning
                # while avoiding a span already assigned to another premise.
                locations = []
                loc = span_source.find(needle, cursor)
                if loc >= 0:
                    locations.append(loc)
                loc = span_source.find(needle)
                while loc >= 0:
                    if loc not in locations:
                        locations.append(loc)
                    loc = span_source.find(needle, loc + 1)
                for loc in locations:
                    start = loc + prefix_len
                    span = (start, start + len(premise.text))
                    if span in matched_spans:
                        continue
                    matched_spans.add(span)
                    return start, span[1], span[1], "matched"
            if strict_prompt_spans:
                raise ValueError(f"premise span not found in rendered prompt for {premise.premise_id}")
            return premise.start, premise.end, cursor, "fallback_logical_coordinates"
        return premise.start, premise.end, cursor, "logical_coordinates"

    e_rows = []
    premise_spans = []
    premise_records = []
    search_cursor = 0
    for premise in premises:
        span_start, span_end, next_cursor, span_status = resolved_span(premise, search_cursor)
        premise_spans.append([span_start, span_end])
        search_cursor = max(search_cursor, next_cursor)
        span_text = span_source[span_start:span_end] if span_source and span_status == "matched" else premise.text
        if span_source and span_status == "matched" and span_text != premise.text:
            span_status = "mismatch"
        if strict_prompt_spans and span_status != "matched":
            raise ValueError(f"premise span round-trip failed for {premise.premise_id}")
        premise_records.append(
            {
                "row_key": stable_row_key(
                    task_id=task_id,
                    base_group_id=base_group_id,
                    trace_id=trace_id,
                    premise_id=premise.premise_id,
                    position="embedding",
                ),
                "trace_id": trace_id,
                "task_id": task_id,
                "base_group_id": base_group_id,
                "premise_id": premise.premise_id,
                "prompt_start": span_start,
                "prompt_end": span_end,
                "text": premise.text,
                "matched_text": span_text,
                "status": span_status,
                "kind": premise.kind,
                "source": "rendered_prompt" if rendered_prompt_text else ("logical_prompt" if prompt_text else "premise_fields"),
            }
        )
        idxs = [i for i in span_token_indices(offsets, span_start, span_end) if i < hidden.shape[0]]
        if idxs:
            e_rows.append(hidden[idxs].mean(axis=0))
        else:
            e_rows.append(np.full(dim, np.nan))
    if not e_rows:
        e_rows.append(np.full(dim, np.nan))
    return {
        "H": np.asarray(h_matrix, dtype=float),
        "E": np.stack(e_rows),
        "H_pre_step": pre_step,
        "H_pre_value": pre_value,
        "H_post_step": post_step,
        "hidden_layer": layer,
        "n_layers": n_layers,
        "weight_source": weight_source,
        "pooling": "premise_span_mean",
        "h_position": h_position,
        "event_ids": event_ids,
        "identity_keys": identity_keys,
        "premise_spans": premise_spans,
        "event_records": event_records,
        "premise_records": premise_records,
    }


def collect_tiny(kind: str, prompt_ids: list[int], max_new: int = 4, seed: int = 0, weight_seed: int = 0) -> dict:
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(weight_seed)
        model = build_tiny(kind)
    g = torch.Generator(device=model_device(model)).manual_seed(seed)
    prompt = torch.tensor([prompt_ids], dtype=torch.long)
    decoded = decode_loop(model, prompt, g, max_new=max_new)
    offsets = [[i, i + 1] for i in range(len(decoded["token_ids"]))]
    target = len(prompt_ids)
    value_start = min(target + 1, len(decoded["token_ids"]))
    target_end = len(decoded["token_ids"])
    feat = {
        "pre_step": select_prefix_index(offsets, target, "pre_step"),
        "pre_value": select_prefix_index(offsets, target, "pre_value", value_start=value_start),
        "post_step": select_prefix_index(offsets, target, "post_step", target_end=target_end),
    }
    n_layers = len(model.model.layers)
    layer = readout_layer_index(n_layers)
    hidden = _hidden_at_layer(model, decoded["token_ids"], layer)
    prefix_index = max(min(target - 1, hidden.shape[0] - 1), 0)
    return {
        **decoded,
        "features": feat,
        "model_kind": kind,
        "weight_source": "random_init",
        "hidden_prefix": hidden[prefix_index],
        "hidden_all": hidden,
        "hidden_layer": layer,
        "n_layers": n_layers,
    }


def intervene_tiny(kind: str, prompt_ids: list[int], layer: int = 1, donor: np.ndarray | None = None, weight_seed: int = 0) -> dict:
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(weight_seed)
        model = build_tiny(kind)
    ids = torch.tensor([prompt_ids], dtype=torch.long)
    base = model(input_ids=ids, use_cache=True)
    cache_a = base.past_key_values
    hidden = _hidden_at_layer(model, prompt_ids, layer)
    base_vec = hidden[min(hidden.shape[0] - 1, max(len(prompt_ids) - 1, 0))]
    rng = np.random.default_rng(0)
    donor_vec = np.asarray(donor, dtype=float) if donor is not None else base_vec + rng.normal(scale=1.0, size=base_vec.shape)
    basis = orthonormal_basis(base_vec.shape[-1], 1, rng)

    def transform(t):
        vec = t.detach().float().cpu().numpy().reshape(-1)
        swapped = apply_swap(vec, donor_vec, basis)
        return torch.as_tensor(swapped, dtype=t.dtype, device=t.device).view_as(t)

    ids2 = ids.clone()
    with resid_post_hook(model, layer, transform, once=True):
        patched = model(input_ids=ids2, past_key_values=None, use_cache=True)
    return {
        "base_logits": base.logits.detach(),
        "patched_logits": patched.logits.detach(),
        "cache_isolated": cache_a is not patched.past_key_values,
        "layer": layer,
        "hook": "resid_post",
        "transform": "pi_z_swap",
    }


def intervene_hidden_decode(
    kind: str,
    prompt_ids: list[int],
    layer: int,
    donor: np.ndarray | None = None,
    seed: int = 0,
    weight_seed: int = 0,
    max_new: int = 4,
    temperature: float = 0.6,
    top_k: int = 20,
    top_p: float = 0.95,
    eos_id: int | None = None,
    event_aligned: bool = False,
    basis_seed: int | None = None,
    basis: np.ndarray | None = None,
    mode: str = "pi_z_swap",
    projector: np.ndarray | None = None,
    delta: np.ndarray | None = None,
    target_prefix_len: int | None = None,
    model=None,
) -> dict:
    if model is None:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(weight_seed)
            model = build_tiny(kind)
    donor_vec = np.asarray(donor, dtype=float) if donor is not None else None
    rng = np.random.default_rng(1 if basis_seed is None else int(basis_seed))
    fitted_basis = None if basis is None else np.asarray(basis, dtype=float)
    if mode == "pi_z_swap":
        if donor_vec is None:
            raise ValueError("pi_z_swap requires donor")
        if fitted_basis is None:
            fitted_basis = orthonormal_basis(donor_vec.shape[-1], min(2, donor_vec.shape[-1]), rng)
        if fitted_basis.ndim != 2 or fitted_basis.shape[0] != donor_vec.shape[-1]:
            raise ValueError("basis must have shape (hidden_dim, rank)")
        if fitted_basis.shape[1] < 1 or fitted_basis.shape[1] > fitted_basis.shape[0]:
            raise ValueError("basis rank must be between 1 and hidden_dim")
        basis = fitted_basis

        def transform(t):
            vec = t.detach().float().cpu().numpy().reshape(-1)
            swapped = apply_swap(vec, donor_vec, basis)
            return torch.as_tensor(swapped, dtype=t.dtype, device=t.device).view_as(t)

    elif mode == "inlp":
        proj = np.asarray(projector, dtype=float)

        def transform(t):
            vec = t.detach().float().cpu().numpy().reshape(-1)
            out = vec @ proj if proj.ndim == 2 and vec.shape[-1] == proj.shape[0] else vec
            return torch.as_tensor(out, dtype=t.dtype, device=t.device).view_as(t)

    elif mode == "add_delta":
        step = np.asarray(delta, dtype=float)

        def transform(t):
            vec = t.detach().float().cpu().numpy().reshape(-1)
            return torch.as_tensor(vec + step, dtype=t.dtype, device=t.device).view_as(t)

    elif mode == "replace":
        target = np.asarray(delta, dtype=float)

        def transform(t):
            return torch.as_tensor(target, dtype=t.dtype, device=t.device).view_as(t)

    else:
        raise ValueError(mode)

    g = torch.Generator(device=model_device(model)).manual_seed(seed)
    prompt = as_input_ids(prompt_ids, model)
    context = int(getattr(model.config, "max_position_embeddings", 0) or 0)
    if context:
        max_new = min(max_new, context - int(prompt.shape[1]))
        if max_new < 1:
            raise ValueError("no intervention generation space remains in the model context")
    if event_aligned:
        if target_prefix_len is None:
            raise ValueError("event-aligned intervention requires target_prefix_len")
        if int(target_prefix_len) != int(prompt.shape[1]):
            raise ValueError("target_prefix_len must match the supplied prefix")
    with resid_post_hook(model, layer, transform, once=True) as record:
        decoded = decode_loop(model, prompt, g, max_new=max_new, eos_id=eos_id, temperature=temperature, top_k=top_k, top_p=top_p)
    if event_aligned and record.sequence_length != int(target_prefix_len):
        raise RuntimeError("event-aligned hook did not fire on the requested prefix length")
    g2 = torch.Generator(device=model_device(model)).manual_seed(seed)
    baseline = decode_loop(model, prompt, g2, max_new=max_new, eos_id=eos_id, temperature=temperature, top_k=top_k, top_p=top_p)
    return {
        **decoded,
        "baseline_generated_ids": baseline["generated_ids"],
        "baseline_stop_reason": baseline["stop_reason"],
        "followed_donor": decoded["generated_ids"] != baseline["generated_ids"],
        "hook": "resid_post",
        "transform": mode,
        "timing": "pre_step" if event_aligned else "hook_on_prompt",
        "hook_fired": record.touched,
        "hook_token_position": record.token_position,
        "hook_sequence_length": record.sequence_length,
        "hook_input_norm": record.input_norm,
        "hook_delta_norm": record.delta_norm,
        "basis_hash": None if basis is None else hashlib.sha256(np.ascontiguousarray(basis).tobytes()).hexdigest(),
        "basis_rank": None if basis is None else int(basis.shape[1]),
        "basis_norm": None if basis is None else float(np.linalg.norm(basis)),
        "layer": layer,
        "prefix_token_ids": prompt[0].detach().cpu().tolist(),
        "target_prefix_len": int(target_prefix_len) if target_prefix_len is not None else int(prompt.shape[1]),
        "kv_update_range": [int(prompt.shape[1]), int(prompt.shape[1] + len(decoded.get("generated_ids") or []))],
        "prefix_boundary_verified": bool(not event_aligned or record.token_position == int(target_prefix_len) - 1),
    }


def intervene_swap_decode(
    kind: str,
    prompt_ids: list[int],
    donor: np.ndarray,
    layer: int,
    seed: int = 0,
    weight_seed: int = 0,
    max_new: int = 4,
    temperature: float = 0.6,
    top_k: int = 20,
    top_p: float = 0.95,
    event_aligned: bool = False,
    basis_seed: int | None = None,
) -> dict:
    return intervene_hidden_decode(
        kind,
        prompt_ids,
        layer,
        donor=donor,
        seed=seed,
        weight_seed=weight_seed,
        max_new=max_new,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        event_aligned=event_aligned,
        basis_seed=basis_seed,
        mode="pi_z_swap",
    )
