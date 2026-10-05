"""T1 prepare-grid checks. Does not invent scientific thresholds."""
from __future__ import annotations

ALLOWED_OPS = (5, 10, 15, 21)
DEFAULT_N_PROBLEMS = 500
DEFAULT_MOD = 23


def validate_t1_prepare_config(config: dict) -> dict:
    ops = tuple(config.get("ops") or config.get("op") or ())
    if isinstance(ops, int):
        ops = (ops,)
    if not ops or any(op not in ALLOWED_OPS for op in ops):
        raise ValueError(f"ops must be a nonempty subset of {ALLOWED_OPS}")
    n_problems = int(config.get("n_problems", DEFAULT_N_PROBLEMS))
    if n_problems != DEFAULT_N_PROBLEMS:
        raise ValueError(f"declared n_problems must be {DEFAULT_N_PROBLEMS} unless protocol is re-registered")
    mod = int(config.get("mod", DEFAULT_MOD))
    if mod != DEFAULT_MOD:
        raise ValueError("official iGSM arithmetic uses mod=23; other moduli are derived tasks")
    return {"ops": list(ops), "n_problems": n_problems, "mod": mod, "status": "checked"}
