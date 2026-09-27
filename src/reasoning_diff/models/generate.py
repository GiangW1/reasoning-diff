"""Explicit decode loop with isolated torch.Generator. HF generate(generator=) is unused."""
from __future__ import annotations

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
) -> dict:
    model.eval()
    tokens = as_input_ids(prompt_ids, model)
    prompt_len = int(tokens.shape[1])
    past = None
    produced = []
    sampling = {"temperature": temperature, "top_k": top_k, "top_p": top_p}
    with torch.inference_mode():
        for _ in range(max_new):
            step = tokens if past is None else tokens[:, -1:]
            out = model(input_ids=step, past_key_values=past, use_cache=True)
            past = out.past_key_values
            logits = out.logits[:, -1, :]
            gen_device = getattr(generator, "device", None) or torch.device("cpu")
            if logits.device != gen_device:
                logits = logits.to(gen_device)
            nxt = sample_next(logits, generator, temperature=temperature, top_k=top_k, top_p=top_p)
            nxt = nxt.to(tokens.device)
            produced.append(int(nxt.item()))
            tokens = torch.cat([tokens, nxt], dim=-1)
            if eos_id is not None and int(nxt.item()) == eos_id:
                break
    return {
        "prompt_ids": tokens[0, :prompt_len].detach().cpu().tolist(),
        "generated_ids": produced,
        "token_ids": tokens[0].detach().cpu().tolist(),
        "stop_reason": "eos" if eos_id is not None and produced and produced[-1] == eos_id else "max_new",
        "sampling": sampling,
        "device": str(model_device(model)),
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
    tokens = torch.tensor([ids], dtype=torch.long)
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
    if docs:
        return "\n".join(docs) + "\n\n" + task.question
    return task.question


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
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    device: str | None = None,
):
    from ..events import answers_equal, extract_answer, parse_events
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
        runtime = {key: packed.get(key) for key in ("device", "dtype", "think_ids", "cuda_name")}
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
    g = torch.Generator().manual_seed(seed)
    started = time.perf_counter()
    decoded = decode_loop(
        model,
        prompt_tensor,
        g,
        max_new=max_new,
        eos_id=getattr(tokenizer, "eos_token_id", None),
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
    )
    elapsed = time.perf_counter() - started
    full_ids = decoded["token_ids"]
    generated_ids = decoded["generated_ids"]
    text = tokenizer.decode(full_ids, skip_special_tokens=False)
    gen_text = tokenizer.decode(generated_ids, skip_special_tokens=False)
    offset_failures = []
    try:
        offsets, offset_failures = offsets_from_tokenizer(tokenizer, full_ids, text, return_failures=True)
    except Exception as exc:
        offset_failures = [{"error": type(exc).__name__, "message": str(exc)}]
        offsets = [[i, i + 1] for i in range(len(full_ids))]
    rid = run_id or f"trace:{task.task_id}:{seed}"
    events = parse_events(gen_text, task)
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
    pred = extract_answer(gen_text, task.answer_spec.kind)
    gold = task.answer_spec.value
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
        correct=answers_equal(pred, gold, task.answer_spec.kind),
        cost=Cost(prefill_tokens=len(prompt_ids), decode_tokens=len(generated_ids), elapsed_seconds=elapsed),
        run_id=rid,
        record_id=rid,
        metadata={
            "weight_source": "frozen_checkpoint",
            "generation": "decode_loop",
            "model_name": model_name or info.get("name"),
            "revision": info.get("revision"),
            "prompt_len": len(prompt_ids),
            "sampling": decoded.get("sampling"),
            "prompt_text": prompt,
            "parse_status": "ok" if events else "parse_failed",
            "parse_region": "generated",
            "offset_reconstruction_failures": offset_failures,
            "boundary_status": "ok" if not offset_failures else "fallback_cursor",
            "forced_target": False,
            "evidence_status": "model_generated",
            "device": runtime.get("device") or decoded.get("device"),
            "dtype": runtime.get("dtype"),
            "think_ids": runtime.get("think_ids") or list(info.get("think_ids") or []),
            "cuda_name": runtime.get("cuda_name"),
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
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    backend: str = "tiny",
    model_name: str | None = None,
    packed: dict | None = None,
    device: str | None = None,
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
        )
    from ..events import answers_equal, extract_answer, parse_events
    from ..schema import Cost, Trace
    from .tiny import build_tiny
    from .tokenize import decode_ids, encode_text

    prompt = task_prompt(task)
    prompt_ids, _ = encode_text(prompt)
    if len(prompt_ids) > 96:
        raise ValueError("tiny prompt exceeds context; refuse truncated source/value prompts")
    if model is None:
        torch.manual_seed(weight_seed)
        model = build_tiny(kind)
    g = torch.Generator().manual_seed(seed)
    ids = torch.tensor([prompt_ids], dtype=torch.long)
    started = time.perf_counter()
    decoded = decode_loop(model, ids, g, max_new=max_new, temperature=temperature, top_k=top_k, top_p=top_p)
    gen_text = decode_ids(decoded["generated_ids"])
    token_ids = decoded["token_ids"]
    target = getattr(task, "target", None) or (task.nodes[-1].id if task.nodes else None)
    assigned = ""
    if target:
        token_ids, assigned = append_target_assignment(model, token_ids, target, g)
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
    events = []
    for event in raw:
        event.start += len(prompt)
        event.end += len(prompt)
        event.value_start += len(prompt)
        events.append(event)
    parse_status = "ok" if events else "parse_failed"
    if assigned and any(e.start >= len(prompt) + len(gen_text) for e in events):
        parse_status = "constrained_target"
    if target and not any(e.node_id == target for e in events):
        parse_status = "parse_failed"
    for event in events:
        event.run_id = rid
        event.base_group_id = task.base_group_id
        event.record_id = f"{rid}:{event.identity.key()}"
    pred = extract_answer(full_text, task.answer_spec.kind)
    gold = task.answer_spec.value
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
        correct=answers_equal(pred, gold, task.answer_spec.kind),
        cost=Cost(prefill_tokens=len(prompt_ids), decode_tokens=len(generated), elapsed_seconds=elapsed),
        run_id=rid,
        record_id=rid,
        metadata={
            "weight_source": "random_init",
            "generation": "decode_loop",
            "prompt_len": len(prompt_ids),
            "weight_seed": weight_seed,
            "sampling": decoded.get("sampling"),
            "prompt_text": prompt,
            "parse_status": parse_status,
            "target_assignment": assigned,
            "forced_target": bool(assigned),
            "evidence_status": "synthetic_target_assignment" if assigned else "model_generated",
            "parse_region": "generated",
        },
    )


def apply_model_template(tokenizer, messages: list[dict], model_kind: str, enable_thinking: bool = True) -> dict:
    kwargs = {"add_generation_prompt": True, "tokenize": True, "return_tensors": "pt"}
    if model_kind == "qwen3":
        kwargs["enable_thinking"] = enable_thinking
    ids = tokenizer.apply_chat_template(messages, **kwargs)
    prompt_len = int(ids.shape[-1]) if hasattr(ids, "shape") else len(ids)
    return {"input_ids": ids, "model_kind": model_kind, "enable_thinking": enable_thinking, "prompt_len": prompt_len}
