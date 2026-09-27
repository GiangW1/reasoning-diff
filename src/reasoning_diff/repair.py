"""Ungated local repair. Offline scoring never changes the execution path."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Callable

import numpy as np

from .events import NUMBER
from .schema import SCHEMA_VERSION


def _hidden_is_prefill(hidden) -> bool:
    if hidden is None or isinstance(hidden, (bool, str)):
        return False
    try:
        arr = np.asarray(hidden, dtype=float)
    except (TypeError, ValueError):
        return False
    if arr.ndim == 0 or arr.size < 2:
        return False
    return bool(np.isfinite(arr).all() and float(np.linalg.norm(arr)) > 0)


MASKS_MAIN = ("full_recompute", "task_oracle", "linear_truncation", "prompt_instruction", "supervised_text")
MASKS_APPENDIX = ("behavior_reference", "retrieval_of_thought", "matched_budget_random")
ALL_MASKS = MASKS_MAIN + MASKS_APPENDIX


@dataclass
class RepairRecord:
    mask: str
    slots: list[str]
    original_token_budget: int
    generated_tokens: int
    extra_prefill_tokens: int | None
    refilled_prefix: bool
    failures: list[str] = field(default_factory=list)
    gated: bool = False
    verifier_fallback: bool = False
    schema_version: int = SCHEMA_VERSION
    record_id: str = ""
    run_id: str = ""
    base_group_id: str = ""
    status: str = "ok"
    k: int | None = None
    text: str = ""

    def __post_init__(self) -> None:
        if self.mask not in ALL_MASKS:
            raise ValueError(self.mask)
        if self.gated or self.verifier_fallback:
            raise ValueError("gated repair and verifier fallback are excluded")
        if not self.record_id:
            self.record_id = f"repair:{self.run_id}:{self.mask}:{','.join(self.slots)}:k{self.k}"

    def to_dict(self) -> dict:
        return asdict(self)


def mask_prefix(mask: str, new_prefix: str, slots: list[str]) -> str:
    if mask == "full_recompute":
        return new_prefix
    if mask == "task_oracle":
        text = new_prefix
        for slot in slots:
            text = re.sub(rf"(?<!\w){re.escape(slot)}\s*=\s*{NUMBER}", f"{slot} = ?", text, flags=re.I)
        if text == new_prefix:
            text = new_prefix + " [mask:" + ",".join(slots) + "]"
        return text
    if mask == "linear_truncation":
        words = new_prefix.split()
        return " ".join(words[: max(1, len(words) // 2)]) if words else ""
    if mask == "prompt_instruction":
        return "recompute damaged slots. " + new_prefix
    if mask == "supervised_text":
        return "complete the solution. " + new_prefix
    if mask == "retrieval_of_thought":
        return "retrieved: " + new_prefix
    if mask == "matched_budget_random":
        return new_prefix[::-1][: max(1, len(new_prefix) // 2)]
    if mask == "behavior_reference":
        return "behavior slots " + " ".join(slots) + " " + new_prefix
    return new_prefix


def _unmatched_slots(mask: str, new_prefix: str, slots: list[str]) -> list[str]:
    if mask != "task_oracle":
        return []
    return [
        slot
        for slot in slots
        if re.search(rf"(?<!\w){re.escape(slot)}\s*=\s*{NUMBER}", new_prefix, flags=re.I) is None
    ]


def execute_repair_tiny(
    mask: str,
    slots: list[str],
    original_tokens: list[int],
    new_prefix: str,
    kind: str = "qwen2",
    weight_seed: int = 0,
    max_new: int | None = None,
) -> dict:
    import torch

    from .models.generate import sample_next
    from .models.tiny import build_tiny
    from .models.tokenize import encode_text

    prompt = mask_prefix(mask, new_prefix, slots)
    ids, _ = encode_text(prompt)
    ids = ids[:32] or [1]
    budget = max(len(original_tokens), 1)
    torch.manual_seed(weight_seed)
    model = build_tiny(kind)
    produce = max_new if max_new is not None else max(1, min(8, budget))
    g = torch.Generator().manual_seed(0)
    prefix = torch.tensor([ids], dtype=torch.long)
    model.eval()
    with torch.inference_mode():
        prefill = model(input_ids=prefix, use_cache=True, output_hidden_states=True)
    past = prefill.past_key_values
    hidden = prefill.hidden_states[-1][0, -1].detach().cpu()
    produced = []
    tokens = prefix
    with torch.inference_mode():
        if produce > 0:
            nxt = sample_next(prefill.logits[:, -1, :], g, temperature=1.0)
            produced.append(int(nxt.item()))
            tokens = torch.cat([tokens, nxt.view(1, 1)], dim=-1)
            for _ in range(produce - 1):
                out = model(input_ids=tokens[:, -1:], past_key_values=past, use_cache=True)
                past = out.past_key_values
                nxt = sample_next(out.logits[:, -1, :], g, temperature=1.0)
                produced.append(int(nxt.item()))
                tokens = torch.cat([tokens, nxt.view(1, 1)], dim=-1)
    return {
        "generated_ids": produced,
        "prefix_token_ids": ids,
        "generated_tokens": len(produced),
        "extra_prefill_tokens": len(ids),
        "prefill_hidden": hidden.tolist(),
        "refilled_prefix": True,
        "text": prompt,
        "masked_prefix": prompt,
    }


def execute_repair_frozen(
    mask: str,
    slots: list[str],
    original_tokens: list[int],
    new_prefix: str,
    packed: dict | None = None,
    model=None,
    tokenizer=None,
    model_name: str | None = None,
    max_new: int | None = None,
    seed: int = 0,
    device: str | None = None,
) -> dict:
    import torch

    from .models.adapters import as_input_ids, load_frozen
    from .models.generate import apply_model_template, decode_loop, sample_next

    if packed is None and model is None:
        if not model_name:
            raise ValueError("frozen repair requires --model-name")
        packed = load_frozen(model_name, device=device)
    if packed is not None:
        model = model or packed["model"]
        tokenizer = tokenizer or packed["tokenizer"]
        info = packed.get("card") or {}
    else:
        if tokenizer is None:
            raise ValueError("frozen repair requires tokenizer")
        info = {}
    prompt = mask_prefix(mask, new_prefix, slots)
    templated = apply_model_template(tokenizer, [{"role": "user", "content": prompt}], info.get("arch", "qwen2"))
    ids = templated["input_ids"]
    prefix = as_input_ids(ids, model)
    prefix_ids = prefix[0].detach().cpu().tolist()
    limit = info.get("context_limit")
    if limit and len(prefix_ids) > int(limit):
        raise ValueError(f"frozen repair prefix {len(prefix_ids)} exceeds context {limit}")
    budget = max(len(original_tokens), 1)
    produce = max_new if max_new is not None else max(1, min(64, budget))
    model.eval()
    with torch.inference_mode():
        prefill = model(input_ids=prefix, use_cache=True, output_hidden_states=True, past_key_values=None)
    hidden = prefill.hidden_states[-1][0, -1].detach().cpu()
    g = torch.Generator().manual_seed(seed)
    produced = []
    tokens = prefix
    past = prefill.past_key_values
    with torch.inference_mode():
        if produce > 0:
            logits = prefill.logits[:, -1, :]
            if logits.device != g.device:
                logits = logits.to(g.device)
            nxt = sample_next(logits, g, temperature=1.0).to(tokens.device)
            produced.append(int(nxt.item()))
            tokens = torch.cat([tokens, nxt.view(1, 1) if nxt.ndim == 1 else nxt], dim=-1)
            if produce > 1:
                decoded = decode_loop(model, tokens, g, max_new=produce - 1, eos_id=getattr(tokenizer, "eos_token_id", None))
                produced.extend(decoded["generated_ids"])
    return {
        "generated_ids": produced,
        "prefix_token_ids": prefix_ids,
        "generated_tokens": len(produced),
        "extra_prefill_tokens": len(prefix_ids),
        "prefill_hidden": hidden.tolist(),
        "refilled_prefix": True,
        "text": prompt,
        "masked_prefix": prompt,
    }


def run_repair(
    mask: str,
    slots: list[str],
    original_tokens: list[int],
    new_prefix: str,
    generated_tokens: list[int] | None = None,
    prefix_token_ids: list[int] | None = None,
    execute: Callable | None = None,
    run_id: str = "",
    base_group_id: str = "",
    k: int | None = None,
) -> RepairRecord:
    if not new_prefix and mask != "full_recompute":
        raise ValueError("retained text must be re-prefilled on the current prefix")
    if execute is not None:
        result = execute(mask, slots, original_tokens, new_prefix)
        raw_ids = result.get("generated_ids")
        raw_n = result.get("generated_tokens")
        if raw_ids is not None:
            n_gen = len(list(raw_ids))
        elif isinstance(raw_n, int):
            n_gen = raw_n
        else:
            n_gen = 0
        extra = result.get("extra_prefill_tokens", len(result.get("prefix_token_ids") or []))
        hidden = result.get("prefill_hidden")
        prefilled = _hidden_is_prefill(hidden)
        unmatched = _unmatched_slots(mask, new_prefix, slots) if prefilled else []
        return RepairRecord(
            mask=mask,
            slots=list(slots),
            original_token_budget=len(original_tokens),
            generated_tokens=n_gen,
            extra_prefill_tokens=extra if prefilled else None,
            refilled_prefix=prefilled,
            failures=([] if prefilled else ["execute_without_prefill"])
            + ([f"slot_not_found:{slot}" for slot in unmatched] if unmatched else []),
            record_id="",
            run_id=run_id,
            base_group_id=base_group_id,
            status="mask_unmatched" if unmatched else ("ok" if prefilled else "prefill_unavailable"),
            k=k,
            text=str(result.get("text") or result.get("masked_prefix") or ""),
        )
    if prefix_token_ids is not None:
        produced = list(generated_tokens or [])
        return RepairRecord(
            mask=mask,
            slots=list(slots),
            original_token_budget=len(original_tokens),
            generated_tokens=len(produced),
            extra_prefill_tokens=len(prefix_token_ids),
            refilled_prefix=False,
            failures=["prefix_ids_without_hidden"],
            record_id="",
            run_id=run_id,
            base_group_id=base_group_id,
            status="prefill_unavailable",
            k=k,
        )
    return RepairRecord(
        mask=mask,
        slots=list(slots),
        original_token_budget=len(original_tokens),
        generated_tokens=len(generated_tokens or []),
        extra_prefill_tokens=None,
        refilled_prefix=False,
        failures=["tokenizer_or_model_missing"],
        record_id="",
        run_id=run_id,
        base_group_id=base_group_id,
        status="prefill_unavailable",
        k=k,
    )


def consecutive_repairs(
    mask: str,
    slots: list[str],
    original_tokens: list[int],
    new_prefix: str,
    k_max: int = 5,
    execute: Callable | None = None,
    **kwargs,
) -> list[RepairRecord]:
    rows = []
    # Each k is an independent intervention on the same retained prefix.
    # Feeding the previous masked text into the next round compounds markers
    # and changes the estimand from "mask k slots" to "mask k slots plus all
    # prior edits".
    for k in range(1, k_max + 1):
        use_slots = slots[:k] if slots else [str(k)]
        rec = run_repair(mask, use_slots, original_tokens, new_prefix, execute=execute, k=k, **kwargs)
        rows.append(rec)
    return rows


def repairability(generated: int, full_recompute: int) -> float | None:
    if full_recompute == 0:
        return None
    return 1.0 - generated / full_recompute


def recompute_ratio(slots: int, n: int) -> float | None:
    if n == 0:
        return None
    return slots / n
