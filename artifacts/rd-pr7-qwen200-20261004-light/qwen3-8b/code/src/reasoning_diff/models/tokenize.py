"""Tiny-vocab tokenizer and readout-layer / span helpers. No HF downloads."""
from __future__ import annotations

import math

TINY_VOCAB = 64


def encode_text(text: str, vocab_size: int = TINY_VOCAB) -> tuple[list[int], list[list[int]]]:
    ids = [(ord(ch) % (vocab_size - 1)) + 1 for ch in text]
    offsets = [[i, i + 1] for i in range(len(text))]
    return ids, offsets


def decode_ids(ids: list[int]) -> str:
    return "".join(chr(32 + (int(i) % 95)) for i in ids)


def readout_layer_index(n_layers: int) -> int:
    """0-based layer in the paper 60%–75% depth band. No silent last-layer fallback."""
    if n_layers < 1:
        raise ValueError("n_layers must be positive")
    in_band = [i for i in range(n_layers) if 0.60 <= (i + 1) / n_layers <= 0.75]
    if not in_band:
        raise ValueError(f"no layer in 60-75% band for n_layers={n_layers}")
    return in_band[len(in_band) // 2]


def offsets_from_tokenizer(tokenizer, token_ids: list[int], text: str, return_failures: bool = False):
    offsets = []
    failures = []
    cursor = 0
    for index, tid in enumerate(token_ids):
        piece = tokenizer.decode([tid], skip_special_tokens=True)
        loc = text.find(piece, cursor) if piece else cursor
        if loc < 0:
            failures.append({"token_index": index, "token_id": int(tid), "piece": piece, "cursor": cursor})
            loc = cursor
        end = loc + max(len(piece), 0)
        offsets.append([loc, end if end > loc else loc])
        cursor = max(end, cursor)
    return (offsets, failures) if return_failures else offsets


def span_token_indices(offsets: list[list[int]], start: int, end: int) -> list[int]:
    """Tokens fully contained in [start, end). Overlap / straddle is excluded."""
    return [i for i, (a, b) in enumerate(offsets) if a >= start and b <= end and a < b]
