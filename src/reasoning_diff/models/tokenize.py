"""Tiny-vocab tokenizer and readout-layer / span helpers. No HF downloads."""
from __future__ import annotations

import math
from bisect import bisect_left, bisect_right

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
    """Exact round trip only; never search ahead or invent cursor offsets."""
    offsets = None
    if getattr(tokenizer, "is_fast", False):
        encoded = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
        if list(encoded["input_ids"]) == list(token_ids):
            offsets = [list(pair) for pair in encoded["offset_mapping"]]
    if offsets is None and hasattr(tokenizer, "convert_ids_to_tokens"):
        # Byte-level BPE can split a UTF-8 character across tokens. Mapping
        # the original bytes keeps those tokens straddling the same character.
        bs = list(range(33, 127)) + list(range(161, 173)) + list(range(174, 256))
        cs = list(bs)
        extra = 0
        for byte in range(256):
            if byte not in bs:
                bs.append(byte)
                cs.append(256 + extra)
                extra += 1
        decoder = dict(zip(map(chr, cs), bs))
        special = set(getattr(tokenizer, "all_special_ids", []))
        try:
            pieces = [tokenizer.convert_ids_to_tokens(int(tid)).encode("utf-8") if tid in special else
                      bytes(decoder[ch] for ch in tokenizer.convert_ids_to_tokens(int(tid))) for tid in token_ids]
            if b"".join(pieces) == text.encode("utf-8"):
                boundaries = [0]
                for char in text:
                    boundaries.append(boundaries[-1] + len(char.encode("utf-8")))
                cursor, offsets = 0, []
                for piece in pieces:
                    end = cursor + len(piece)
                    offsets.append([bisect_right(boundaries, cursor) - 1, bisect_left(boundaries, end)])
                    cursor = end
        except (KeyError, TypeError, AttributeError):
            pass
    if offsets is None:
        pieces = [tokenizer.decode([int(tid)], skip_special_tokens=False) for tid in token_ids]
        if "".join(pieces) == text:
            offsets, cursor = [], 0
            for piece in pieces:
                offsets.append([cursor, cursor + len(piece)])
                cursor += len(piece)
    failures = [] if offsets is not None else [{"error": "offset_roundtrip_failed", "n_tokens": len(token_ids)}]
    if offsets is None:
        offsets = [[0, 0] for _ in token_ids]
    return (offsets, failures) if return_failures else offsets


def span_token_indices(offsets: list[list[int]], start: int, end: int) -> list[int]:
    """Tokens fully contained in [start, end). Overlap / straddle is excluded."""
    return [i for i, (a, b) in enumerate(offsets) if a >= start and b <= end and a < b]
