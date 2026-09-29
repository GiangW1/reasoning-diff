"""Explicit decode loop with isolated torch.Generator. HF generate(generator=) is unused."""
from __future__ import annotations

import re
import time

import torch
from torch.nn import functional as F

from .adapters import as_input_ids, model_device


def sample_next(logits: torch.Tensor, generator: torch.Generator, temperature: float = 1.0, top_k: int = 0, top_p: float = 1.0) -> torch.Tensor:
    if temperature <= 0:
        return torch.argmax(logits, dim=-1, keepdim=True)
    scores = logits / temperature
    if top_k > 0:
        values, _ = torch.topk(scores, min(top_k, scores.size(-1)))
        cutoff = values[..., -1, None]
        scores = scores.masked_fill(scores < cutoff, -float("inf"))
    if top_p < 1.0:
        sorted_scores, sorted_idx = torch.sort(scores, descending=True)
        cdf = torch.cumsum(F.softmax(sorted_scores, dim=-1), dim=-1)
        mask = cdf > top_p
        mask[..., 1:] = mask[..., :-1].clone()
        mask[..., 0] = False
        sorted_scores = sorted_scores.masked_fill(mask, -float("inf"))
        scores = torch.zeros_like(scores).scatter(-1, sorted_idx, sorted_scores)
    probs = F.softmax(scores, dim=-1)
    return torch.multinomial(probs, 1, generator=generator)


def decode_loop(
    model,
    prompt_ids: torch.Tensor,
    generator: torch.Generator,
    max_new: int,
    eos_id: int | None = None,
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    stop_condition=None,
) -> dict:
    model.eval()
    tokens = as_input_ids(prompt_ids, model)
    prompt_len = int(tokens.shape[1])
    past = None
    produced = []
    transfer_seconds = 0.0
    stop_reason = "max_new"
    sampling = {"temperature": temperature, "top_k": top_k, "top_p": top_p}
    with torch.inference_mode():
        for _ in range(max_new):
            step = tokens if past is None else tokens[:, -1:]
            call = {"input_ids": step, "use_cache": True}
            if past is not None:
                call["past_key_values"] = past
            out = model(**call)
            past = out.past_key_values
            logits = out.logits[:, -1, :]
            gen_device = getattr(generator, "device", None) or torch.device("cpu")
            if logits.device != gen_device:
                transfer_started = time.perf_counter()
                logits = logits.to(gen_device)
                transfer_seconds += time.perf_counter() - transfer_started
            nxt = sample_next(logits, generator, temperature=temperature, top_k=top_k, top_p=top_p)
            nxt = nxt.to(tokens.device)
            produced.append(int(nxt.item()))
            tokens = torch.cat([tokens, nxt], dim=-1)
            if eos_id is not None and int(nxt.item()) == eos_id:
                stop_reason = "eos"
                break
            if stop_condition is not None and stop_condition(produced):
                stop_reason = "stop_condition"
                break
    return {
        "prompt_ids": tokens[0, :prompt_len].detach().cpu().tolist(),
        "generated_ids": produced,
        "token_ids": tokens[0].detach().cpu().tolist(),
        "stop_reason": stop_reason,
        "sampling": sampling,
        "device": str(model_device(model)),
        "device_transfer_seconds": transfer_seconds,
    }


def _digit_token_ids(vocab_size: int = 64) -> dict[int, str]:
    from .tokenize import encode_text

    out = {}
    for ch in "0123456789":
        tid = encode_text(ch, vocab_size)[0][0]
        out[tid] = ch
    return out


def append_target_assignment(model, token_ids: list[int], target: str, generator, vocab_size: int = 64) -> tuple[list[int], str]:
    """Teacher-force '\\n{target} = ' then sample digits from model logits. Not gold values."""
    from .tokenize import encode_text

    line = f"\n{target} = "
    extra, _ = encode_text(line, vocab_size)
    ids = list(token_ids) + extra
    digit_map = _digit_token_ids(vocab_size)
    tokens = torch.tensor([ids], dtype=torch.long, device=model_device(model))
    produced_digits = []
    with torch.inference_mode():
        out = model(input_ids=tokens, use_cache=True)
        past = out.past_key_values
        logits = out.logits[:, -1, :]
        for _ in range(2):
            masked = torch.full_like(logits, float("-inf"))
            for tid in digit_map:
                if tid < logits.shape[-1]:
                    masked[..., tid] = logits[..., tid]
            nxt = sample_next(masked, generator, temperature=1.0)
            produced_digits.append(int(nxt.item()))
            tokens = torch.cat([tokens, nxt.view(1, 1)], dim=-1)
            step = model(input_ids=nxt.view(1, 1), past_key_values=past, use_cache=True)
            past = step.past_key_values
            logits = step.logits[:, -1, :]
    digit_text = "".join(digit_map.get(i, "0") for i in produced_digits)
    return tokens[0].tolist(), line + digit_text


def task_prompt(task) -> str:
    docs = []
    for premise in getattr(task, "premises", []) or []:
        if getattr(premise, "kind", None) in {"sentence", "paragraph"} and premise.text:
            title = getattr(premise, "document_id", None) or ""
            docs.append(f"{title}: {premise.text}" if title else premise.text)
    prompt = "\n".join(docs) + "\n\n" + task.question if docs else task.question
    mod = getattr(getattr(task, "answer_spec", None), "mod", None)
    if getattr(task, "source_kind", None) == "official" and mod:
        prompt += (
            f"\n\nUse these iGSM rules: compute every arithmetic operation modulo {mod}; "
            "a requested aggregate category is the sum of the exact quantities named for the "
            "queried entity in the question; this benchmark meaning is fixed, so do not debate "
            "or reinterpret it. "
            "use only the givens needed for the query and ignore irrelevant equations. "
            "Reason naturally until reaching a conclusion, without restarting or repeating an "
            "earlier step. After </think>, give a concise answer and end with exactly one final "
            "answer in the form \\boxed{number}."
        )
    return prompt


def generate_frozen_trace(
    task,
    model_name: str,
    seed: int = 0,
    max_new: int = 256,
    run_id: str = "",
    local_files_only: bool | None = None,
    enable_thinking: bool = True,
    packed: dict | None = None,
    model=None,
    tokenizer=None,
    temperature: float = 0.6,
    top_k: int = 20,
    top_p: float = 0.95,
    device: str | None = None,
):
    from ..events import assign_event_regions, extract_answer_with_status, parse_events
    from ..protocol import answer_score
    from ..schema import Cost, Trace
    from .adapters import card, load_frozen
    from .tokenize import offsets_from_tokenizer

    if packed is None and model is None:
        if not model_name:
            raise ValueError("frozen generate requires --model-name")
        packed = load_frozen(model_name, local_files_only=local_files_only, device=device)
    if packed is not None:
        model = model or packed["model"]
        tokenizer = tokenizer or packed["tokenizer"]
        info = packed["card"]
        runtime = {key: packed.get(key) for key in ("device", "dtype", "think_ids", "cuda_name", "validation")}
    else:
        if tokenizer is None:
            raise ValueError("frozen generate requires tokenizer")
        info = card(model_name) if model_name else {"id": "injected", "arch": "qwen2", "revision": "", "context_limit": None}
        runtime = {"device": str(model_device(model))}
    prompt = task_prompt(task)
    messages = [{"role": "user", "content": prompt}]
    templated = apply_model_template(tokenizer, messages, info.get("arch", "qwen2"), enable_thinking=enable_thinking)
    ids = templated["input_ids"]
    if hasattr(ids, "tolist"):
        prompt_ids = ids[0].tolist() if getattr(ids, "ndim", 1) > 1 else ids.tolist()
        prompt_tensor = ids if getattr(ids, "ndim", 1) > 1 else ids.unsqueeze(0)
    else:
        prompt_ids = list(ids)
        prompt_tensor = torch.tensor([prompt_ids], dtype=torch.long)
    limit = info.get("context_limit")
    if limit and len(prompt_ids) > int(limit):
        raise ValueError(f"frozen prompt {len(prompt_ids)} exceeds context {limit}")
    g = torch.Generator(device=model_device(model)).manual_seed(seed)
    started = time.perf_counter()

    def boxed_answer_complete(generated: list[int]) -> bool:
        if getattr(task, "source_kind", None) != "official":
            return False
        tail = tokenizer.decode(generated[-96:], skip_special_tokens=False)
        return re.search(r"\\boxed\{[^{}\n]+\}", tail) is not None

    thinking_budget = max_new
    decoded = decode_loop(
        model,
        prompt_tensor,
        g,
        max_new=thinking_budget,
        eos_id=getattr(tokenizer, "eos_token_id", None),
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        stop_condition=boxed_answer_complete,
    )
    forced_think_close = False
    finalizer_used = False
    finalizer_control_tokens = 0
    extra_prefill_tokens = 0
    model_generated_tokens = len(decoded["generated_ids"])
    elapsed = time.perf_counter() - started
    full_ids = decoded["token_ids"]
    generated_ids = decoded["generated_ids"]
    text = tokenizer.decode(full_ids, skip_special_tokens=False)
    rendered_prompt_text = tokenizer.decode(prompt_ids, skip_special_tokens=False)
    if not text.startswith(rendered_prompt_text):
        raise ValueError("decoded full trace does not preserve the rendered prompt prefix")
    gen_text = tokenizer.decode(generated_ids, skip_special_tokens=False)
    offset_failures = []
    try:
        offsets, offset_failures = offsets_from_tokenizer(tokenizer, full_ids, text, return_failures=True)
    except Exception as exc:
        offset_failures = [{"error": type(exc).__name__, "message": str(exc)}]
        offsets = [[i, i + 1] for i in range(len(full_ids))]
    rid = run_id or f"trace:{task.task_id}:{seed}"
    events = parse_events(gen_text, task)
    assign_event_regions(events, gen_text)
    identity_keys = [event.identity.key() for event in events]
    target = getattr(task, "target", None) or (task.nodes[-1].id if task.nodes else None)
    target_present = target is None or any(event.node_id == target for event in events)
    duplicate_events = len(identity_keys) != len(set(identity_keys))
    special_ids = {
        int(value)
        for value in (
            getattr(tokenizer, "bos_token_id", None),
            getattr(tokenizer, "eos_token_id", None),
            getattr(tokenizer, "pad_token_id", None),
        )
        if value is not None
    }
    crossing_tokens = sum(
        1
        for event in events
        for boundary in (event.start, event.value_start, event.end)
        if any(a < boundary < b for a, b in offsets if a < b)
    )
    prompt_n = len(prompt_ids)
    if prompt_n < len(offsets):
        gen_char_start = offsets[prompt_n][0]
    elif offsets:
        gen_char_start = offsets[-1][1]
    else:
        gen_char_start = 0
    for event in events:
        event.start += gen_char_start
        event.end += gen_char_start
        event.value_start += gen_char_start
        event.run_id = rid
        event.base_group_id = task.base_group_id
        event.record_id = f"{rid}:{event.identity.key()}"
    pred, answer_status = extract_answer_with_status(gen_text, task.answer_spec.kind)
    gold = task.answer_spec.value
    score = answer_score(pred, gold, task.answer_spec.kind, task.answer_spec.aliases)
    trace_status = (
        "parse_failed"
        if not events
        else "natural_truncated"
        if decoded.get("stop_reason") == "max_new"
        else "answer_missing"
        if pred is None
        else "natural_complete"
    )
    return Trace(
        id=rid,
        task_id=task.task_id,
        base_group_id=task.base_group_id,
        model=info.get("id") or model_name,
        seed=seed,
        text=text,
        token_ids=full_ids,
        offsets=offsets,
        events=events,
        answer=pred,
        correct=score["correct"],
        status=trace_status,
        cost=Cost(
            prefill_tokens=len(prompt_ids),
            decode_tokens=model_generated_tokens,
            extra_prefill_tokens=extra_prefill_tokens,
            elapsed_seconds=elapsed,
            device_transfer_seconds=float(decoded.get("device_transfer_seconds") or 0.0),
            timing_status="measured",
            hardware={"device": runtime.get("device") or decoded.get("device"), "dtype": runtime.get("dtype")},
        ),
        run_id=rid,
        record_id=rid,
        metadata={
            "weight_source": "frozen_checkpoint",
            "generation": "decode_loop",
            "model_name": model_name or info.get("name"),
            "revision": info.get("revision"),
            "prompt_len": len(prompt_ids),
            "generated_tokens": len(generated_ids),
            "model_generated_tokens": model_generated_tokens,
            "thinking_budget_tokens": thinking_budget,
            "thinking_forced_close": forced_think_close,
            "constrained_thinking_tokens": int(forced_think_close),
            "finalizer_used": finalizer_used,
            "finalizer_control_tokens": finalizer_control_tokens,
            "finalizer_max_new": 1024 if finalizer_used else 0,
            "stop_reason": decoded.get("stop_reason"),
            "sampling": decoded.get("sampling"),
            "enable_thinking": enable_thinking,
            "prompt_text": prompt,
            "rendered_prompt_text": rendered_prompt_text,
            "rendered_prompt_char_len": len(rendered_prompt_text),
            "rendered_prompt_prefix_status": "exact",
            "parse_status": "boundary_failed" if offset_failures else ("ok" if events else "parse_failed"),
            "target_event_present": target_present,
            "duplicate_event_identities": duplicate_events,
            "structure_status": "duplicate" if duplicate_events else ("target_missing" if not target_present else "ok"),
            "parse_region": "generated",
            "offset_reconstruction_failures": offset_failures,
            "offset_reconstruction_failure_count": len(offset_failures),
            "boundary_crossing_token_count": crossing_tokens,
            "special_token_count": sum(int(token) in special_ids for token in full_ids),
            "boundary_status": "ok" if not offset_failures else "fallback_cursor",
            "forced_target": False,
            "evidence_status": "model_generated_natural",
            "protocol_version": "natural_no_finalizer_v1",
            "trace_status": trace_status,
            "answer_status": answer_status,
            "analysis_eligibility": {
                "C1": bool(any(event.event_region == "thinking" for event in events)),
                "C2": bool(events),
                "C3": bool(events),
                "C4": bool(pred is not None),
            },
            **score,
            "device": runtime.get("device") or decoded.get("device"),
            "dtype": runtime.get("dtype"),
            "think_ids": runtime.get("think_ids") or list(info.get("think_ids") or []),
            "cuda_name": runtime.get("cuda_name"),
            "validation": runtime.get("validation"),
        },
    )


def generate_task_trace(
    task,
    kind: str = "qwen2",
    seed: int = 0,
    max_new: int = 8,
    weight_seed: int = 0,
    run_id: str = "",
    model=None,
    temperature: float = 0.6,
    top_k: int = 20,
    top_p: float = 0.95,
    backend: str = "tiny",
    model_name: str | None = None,
    packed: dict | None = None,
    device: str | None = None,
    allow_forced_target: bool = True,
    enable_thinking: bool = True,
):
    if backend == "frozen":
        if not model_name and packed is None and model is None:
            raise ValueError("frozen generate requires --model-name")
        return generate_frozen_trace(
            task,
            model_name or "",
            seed=seed,
            max_new=max_new,
            run_id=run_id,
            packed=packed,
            model=model,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            device=device,
            enable_thinking=enable_thinking,
        )
    from ..events import assign_event_regions, extract_answer_with_status, parse_events
    from ..protocol import answer_score
    from ..schema import Cost, Trace
    from .tiny import build_tiny
    from .tokenize import decode_ids, encode_text

    prompt = task_prompt(task)
    prompt_ids, _ = encode_text(prompt)
    if len(prompt_ids) > 96:
        raise ValueError("tiny prompt exceeds context; refuse truncated source/value prompts")
    if model is None:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(weight_seed)
            model = build_tiny(kind)
    g = torch.Generator(device=model_device(model)).manual_seed(seed)
    ids = torch.tensor([prompt_ids], dtype=torch.long, device=model_device(model))
    started = time.perf_counter()
    decoded = decode_loop(model, ids, g, max_new=max_new, temperature=temperature, top_k=top_k, top_p=top_p)
    gen_text = decode_ids(decoded["generated_ids"])
    token_ids = decoded["token_ids"]
    target = getattr(task, "target", None) or (task.nodes[-1].id if task.nodes else None)
    assigned = ""
    decoded_token_count = len(decoded.get("generated_ids") or [])
    if target and allow_forced_target:
        token_ids, assigned = append_target_assignment(model, token_ids, target, g)
    assignment_token_count = max(0, len(token_ids) - len(decoded.get("token_ids") or []))
    elapsed = time.perf_counter() - started
    full_text = prompt + gen_text + assigned
    offsets = [[i, i + 1] for i in range(len(full_text))]
    if len(offsets) < len(token_ids):
        extra = len(token_ids) - len(offsets)
        start = len(full_text)
        offsets.extend([start + i, start + i + 1] for i in range(extra))
    elif len(offsets) > len(token_ids):
        offsets = offsets[: len(token_ids)]
    rid = run_id or f"trace:{task.task_id}:{seed}"
    generated = gen_text + assigned
    raw = parse_events(generated, task)
    assign_event_regions(raw, generated)
    events = []
    for event in raw:
        event.start += len(prompt)
        event.end += len(prompt)
        event.value_start += len(prompt)
        events.append(event)
    parse_status = "ok" if events else "parse_failed"
    if assigned and any(e.start >= len(prompt) + len(gen_text) for e in events):
        parse_status = "constrained_target"
    target_present = target is None or any(e.node_id == target for e in events)
    duplicate_events = len({e.identity.key() for e in events}) != len(events)
    crossing_tokens = sum(
        1
        for event in events
        for boundary in (event.start, event.value_start, event.end)
        if any(a < boundary < b for a, b in offsets if a < b)
    )
    if target and not target_present:
        parse_status = "parse_failed"
    for event in events:
        event.run_id = rid
        event.base_group_id = task.base_group_id
        event.record_id = f"{rid}:{event.identity.key()}"
    pred, answer_status = extract_answer_with_status(full_text, task.answer_spec.kind)
    gold = task.answer_spec.value
    score = answer_score(pred, gold, task.answer_spec.kind, task.answer_spec.aliases)
    trace_status = (
        "fixture_forced_target"
        if assigned
        else "parse_failed"
        if not events
        else "natural_truncated"
        if decoded.get("stop_reason") == "max_new"
        else "answer_missing"
        if pred is None
        else "natural_complete"
    )
    return Trace(
        id=rid,
        task_id=task.task_id,
        base_group_id=task.base_group_id,
        model=f"tiny-{kind}",
        seed=seed,
        text=full_text,
        token_ids=token_ids,
        offsets=offsets,
        events=events,
        answer=pred,
        correct=score["correct"],
        status=trace_status,
        cost=Cost(
            prefill_tokens=len(prompt_ids),
            decode_tokens=decoded_token_count + assignment_token_count,
            elapsed_seconds=elapsed,
            device_transfer_seconds=float(decoded.get("device_transfer_seconds") or 0.0),
            timing_status="measured",
            hardware={"device": str(model_device(model)), "dtype": str(next(model.parameters()).dtype) if list(model.parameters()) else None},
        ),
        run_id=rid,
        record_id=rid,
        metadata={
            "weight_source": "random_init",
            "generation": "decode_loop",
            "prompt_len": len(prompt_ids),
            "weight_seed": weight_seed,
            "sampling": decoded.get("sampling"),
            "generated_tokens": decoded_token_count + assignment_token_count,
            "model_generated_tokens": decoded_token_count,
            "constrained_target_tokens": assignment_token_count,
            "stop_reason": "constrained_target" if assigned else decoded.get("stop_reason"),
            "allow_forced_target": allow_forced_target,
            "prompt_text": prompt,
            "rendered_prompt_text": prompt,
            "rendered_prompt_char_len": len(prompt),
            "parse_status": parse_status,
            "target_event_present": target_present,
            "duplicate_event_identities": duplicate_events,
            "structure_status": "duplicate" if duplicate_events else ("target_missing" if not target_present else "ok"),
            "offset_reconstruction_failure_count": 0,
            "boundary_crossing_token_count": crossing_tokens,
            "boundary_status": "unverified_character_offsets",
            "special_token_count": 0,
            "target_assignment": assigned,
            "forced_target": bool(assigned),
            "evidence_status": "synthetic_target_assignment" if assigned else "model_generated_natural",
            "protocol_version": "natural_no_finalizer_v1" if not assigned else "fixture_forced_target_v1",
            "trace_status": trace_status,
            "answer_status": answer_status,
            "analysis_eligibility": {
                "C1": bool(any(event.event_region == "thinking" for event in events)),
                "C2": bool(events),
                "C3": bool(events),
                "C4": bool(pred is not None),
            },
            **score,
            "parse_region": "generated",
        },
    )


def apply_model_template(tokenizer, messages: list[dict], model_kind: str, enable_thinking: bool = True) -> dict:
    kwargs = {"add_generation_prompt": True, "tokenize": True, "return_tensors": "pt"}
    if model_kind == "qwen3":
        kwargs["enable_thinking"] = enable_thinking
    ids = tokenizer.apply_chat_template(messages, **kwargs)
    if hasattr(ids, "get") and "input_ids" in ids:
        ids = ids["input_ids"]
    prompt_len = int(ids.shape[-1]) if hasattr(ids, "shape") else len(ids)
    return {"input_ids": ids, "model_kind": model_kind, "enable_thinking": enable_thinking, "prompt_len": prompt_len}
