"""Prospective features never include the target first token or a straddling token."""
from __future__ import annotations

from ..events import boundary_index
from ..schema import POSITION_KINDS


def select_prefix_index(
    offsets: list[list[int]],
    target_char: int,
    kind: str,
    value_start: int | None = None,
    target_end: int | None = None,
) -> dict:
    if kind not in POSITION_KINDS and kind not in {"pre_step", "pre_value", "post_step"}:
        raise ValueError(kind)
    if kind == "pre_value":
        limit = value_start if value_start is not None else target_char
    elif kind == "post_step":
        limit = target_end if target_end is not None else target_char
    else:
        limit = target_char
    idx = boundary_index(offsets, limit, "end" if kind == "post_step" else "before")
    straddling = [i for i, (a, b) in enumerate(offsets) if a < limit < b]
    leaks = bool(straddling)
    return {
        "token_index": idx,
        "kind": kind,
        "leaks_target": leaks,
        "straddling_excluded": straddling,
        "expressible": idx is not None,
        "boundary_source": "offline_annotation",
        "limit": limit,
    }


def assert_no_future_leak(prefix_end: int, target_char: int) -> None:
    if prefix_end > target_char:
        raise ValueError("prefix includes target content")
