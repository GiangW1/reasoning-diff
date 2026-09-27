"""Tiny-model collection and prospective swap decode. Real weights stay pending_server."""
from __future__ import annotations

import numpy as np
import torch

from ..interventions import apply_swap, orthonormal_basis
from .adapters import as_input_ids
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


def _hidden_at_layer(model, token_ids: list[int], layer: int) -> np.ndarray:
    cap = int(getattr(getattr(model, "config", None), "max_position_embeddings", 0) or 0)
    if cap and len(token_ids) > cap:
        raise ValueError(f"trace length {len(token_ids)} exceeds model context {cap}")
    ids = as_input_ids(token_ids, model)
    model.eval()
    with torch.inference_mode():
        fwd = model(input_ids=ids, output_hidden_states=True, use_cache=False, past_key_values=None)
    states = fwd.hidden_states
    idx = min(layer + 1, len(states) - 1)
    return states[idx][0].detach().cpu().numpy()


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
) -> dict:
    if model is None:
        torch.manual_seed(weight_seed)
        model = build_tiny(kind)
    n_layers = _n_layers(model)
    layer = readout_layer_index(n_layers) if hidden_layer is None else hidden_layer
    hidden = _hidden_at_layer(model, token_ids, layer)
    dim = hidden.shape[-1]
    positions = {"pre_step": [], "pre_value": [], "post_step": []}
    event_ids = []
    identity_keys = []
    for event in events:
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
        event_ids.append(getattr(event, "node_id", None) or getattr(ident, "entity_or_expression", None))
        identity_keys.append(ident.key() if ident is not None else event_ids[-1])
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
    def resolved_span(premise, cursor: int) -> tuple[int, int, int]:
        """Resolve local sentence/paragraph spans in the rendered prompt."""
        if prompt_text and getattr(premise, "kind", None) in {"sentence", "paragraph"}:
            prefix = f"{premise.document_id}: " if getattr(premise, "document_id", None) else ""
            needle = prefix + premise.text
            loc = prompt_text.find(needle, cursor)
            if loc >= 0:
                start = loc + len(prefix)
                return start, start + len(premise.text), start + len(premise.text)
            loc = prompt_text.find(premise.text, cursor)
            if loc >= 0:
                return loc, loc + len(premise.text), loc + len(premise.text)
        return premise.start, premise.end, cursor

    e_rows = []
    premise_spans = []
    search_cursor = 0
    for premise in premises:
        span_start, span_end, next_cursor = resolved_span(premise, search_cursor)
        premise_spans.append([span_start, span_end])
        search_cursor = max(search_cursor, next_cursor)
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
    }


def collect_tiny(kind: str, prompt_ids: list[int], max_new: int = 4, seed: int = 0, weight_seed: int = 0) -> dict:
    torch.manual_seed(weight_seed)
    model = build_tiny(kind)
    g = torch.Generator().manual_seed(seed)
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
        vec = t.detach().cpu().numpy().reshape(-1)
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
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    event_aligned: bool = False,
    basis_seed: int | None = None,
    basis: np.ndarray | None = None,
    mode: str = "pi_z_swap",
    projector: np.ndarray | None = None,
    delta: np.ndarray | None = None,
    model=None,
) -> dict:
    if model is None:
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
            vec = t.detach().cpu().numpy().reshape(-1)
            swapped = apply_swap(vec, donor_vec, basis)
            return torch.as_tensor(swapped, dtype=t.dtype, device=t.device).view_as(t)

    elif mode == "inlp":
        proj = np.asarray(projector, dtype=float)

        def transform(t):
            vec = t.detach().cpu().numpy().reshape(-1)
            out = vec @ proj if proj.ndim == 2 and vec.shape[-1] == proj.shape[0] else vec
            return torch.as_tensor(out, dtype=t.dtype, device=t.device).view_as(t)

    elif mode == "add_delta":
        step = np.asarray(delta, dtype=float)

        def transform(t):
            vec = t.detach().cpu().numpy().reshape(-1)
            return torch.as_tensor(vec + step, dtype=t.dtype, device=t.device).view_as(t)

    elif mode == "replace":
        target = np.asarray(delta, dtype=float)

        def transform(t):
            return torch.as_tensor(target, dtype=t.dtype, device=t.device).view_as(t)

    else:
        raise ValueError(mode)

    g = torch.Generator().manual_seed(seed)
    prompt = as_input_ids(prompt_ids, model)
    with resid_post_hook(model, layer, transform, once=True) as record:
        decoded = decode_loop(model, prompt, g, max_new=max_new, temperature=temperature, top_k=top_k, top_p=top_p)
    g2 = torch.Generator().manual_seed(seed)
    baseline = decode_loop(model, prompt, g2, max_new=max_new, temperature=temperature, top_k=top_k, top_p=top_p)
    return {
        **decoded,
        "baseline_generated_ids": baseline["generated_ids"],
        "followed_donor": decoded["generated_ids"] != baseline["generated_ids"],
        "hook": "resid_post",
        "transform": mode,
        "timing": "pre_step" if event_aligned else "hook_on_prompt",
        "hook_fired": record.touched,
        "layer": layer,
    }


def intervene_swap_decode(
    kind: str,
    prompt_ids: list[int],
    donor: np.ndarray,
    layer: int,
    seed: int = 0,
    weight_seed: int = 0,
    max_new: int = 4,
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
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
