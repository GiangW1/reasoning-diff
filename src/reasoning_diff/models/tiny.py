"""Random-weight Qwen2/Qwen3 miniatures. No from_pretrained, no downloads."""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass

import torch


def tiny_config(kind: str):
    if kind == "qwen3":
        from transformers import Qwen3Config

        return Qwen3Config(
            hidden_size=32,
            intermediate_size=64,
            num_hidden_layers=3,
            num_attention_heads=4,
            num_key_value_heads=2,
            head_dim=8,
            vocab_size=64,
            max_position_embeddings=128,
        )
    from transformers import Qwen2Config

    return Qwen2Config(
        hidden_size=32,
        intermediate_size=64,
        num_hidden_layers=3,
        num_attention_heads=4,
        num_key_value_heads=2,
        vocab_size=64,
        max_position_embeddings=128,
    )


def build_tiny(kind: str):
    cfg = tiny_config(kind)
    if kind == "qwen3":
        from transformers import Qwen3ForCausalLM

        return Qwen3ForCausalLM(cfg)
    from transformers import Qwen2ForCausalLM

    return Qwen2ForCausalLM(cfg)


@dataclass
class HookRecord:
    layer: int
    touched: bool = False


@contextmanager
def resid_post_hook(model, layer: int, transform, once: bool = False):
    handle = None
    record = HookRecord(layer)
    fired = {"n": 0}

    def _hook(_module, _inp, output):
        if once and fired["n"] >= 1:
            return output
        fired["n"] += 1
        record.touched = True
        tensor = output[0] if isinstance(output, tuple) else output
        if getattr(tensor, "ndim", 0) >= 2:
            patched = tensor.clone()
            patched[:, -1:] = transform(tensor[:, -1:])
        else:
            patched = transform(tensor)
        if isinstance(output, tuple):
            return (patched,) + output[1:]
        return patched

    try:
        handle = model.model.layers[layer].register_forward_hook(_hook)
        yield record
    finally:
        if handle is not None:
            handle.remove()


def clone_cache(cache):
    if cache is None:
        return None
    if hasattr(cache, "layers"):
        cloned = cache.__class__()
        cloned.layers = []
        for layer in cache.layers:
            item = layer.__class__()
            if getattr(layer, "keys", None) is not None:
                item.keys = layer.keys.clone()
            if getattr(layer, "values", None) is not None:
                item.values = layer.values.clone()
            for attr in ("is_initialized", "dtype", "device", "cache_order"):
                if hasattr(layer, attr):
                    try:
                        setattr(item, attr, getattr(layer, attr))
                    except Exception:
                        pass
            cloned.layers.append(item)
        for attr in ("_seen_tokens", "seen_tokens", "_seen_tokens_offset", "is_initialized"):
            if hasattr(cache, attr):
                try:
                    setattr(cloned, attr, getattr(cache, attr))
                except Exception:
                    pass
        return cloned
    if hasattr(cache, "copy"):
        copied = cache.copy()
        if copied is not cache:
            return copied
    raise TypeError("cache cannot be cloned without sharing storage")


def decode_step(model, input_ids, past=None, use_cache=True):
    model.eval()
    with torch.inference_mode():
        out = model(input_ids=input_ids, past_key_values=past, use_cache=use_cache)
    return out
