"""Frozen model cards. Revisions are required; 'latest' is rejected."""
from __future__ import annotations

import os

import torch

MODELS = {
    "qwen3-8b": {
        "id": "Qwen/Qwen3-8B",
        "revision": "b968826d9c46dd6066d109eabc6255188de91218",
        "arch": "qwen3",
        "hidden_size": 4096,
        "layers": 36,
        "think_ids": (151667, 151668),
        "context_limit": 32768,
    },
    "r1-distill-qwen-7b": {
        "id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "revision": "916b56a44061fd5cd7d6a8fb632557ed4f724f60",
        "arch": "qwen2",
        "hidden_size": 3584,
        "layers": 28,
        "think_ids": (151648, 151649),
        "context_limit": 16384,
    },
}


def card(name: str) -> dict:
    if name not in MODELS:
        raise KeyError(name)
    info = dict(MODELS[name])
    info["name"] = name
    if info["revision"] == "latest":
        raise ValueError("mutable latest revision is forbidden")
    return info


def infer_device(explicit: str | None = None) -> torch.device:
    if explicit:
        return torch.device(explicit)
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def infer_dtype(device: torch.device, explicit=None) -> torch.dtype:
    if explicit is not None:
        return getattr(torch, explicit) if isinstance(explicit, str) else explicit
    return torch.bfloat16 if device.type == "cuda" else torch.float32


def model_device(model) -> torch.device:
    return next(model.parameters()).device


def as_input_ids(token_ids, model) -> torch.Tensor:
    device = model_device(model)
    if hasattr(token_ids, "to"):
        tensor = token_ids.to(device=device, dtype=torch.long)
        return tensor if tensor.ndim == 2 else tensor.unsqueeze(0)
    return torch.tensor([list(token_ids)], dtype=torch.long, device=device)


def _local_files_only(explicit: bool | None) -> bool:
    if explicit is not None:
        return bool(explicit)
    return os.environ.get("RD_LOCAL_FILES_ONLY", "1") not in {"0", "false", "False"}


def think_ids_from_tokenizer(tokenizer, expected=None) -> tuple[int, int]:
    open_id = tokenizer.convert_tokens_to_ids("<think>")
    close_id = tokenizer.convert_tokens_to_ids("</think>")
    if open_id is None or close_id is None:
        raise ValueError("tokenizer missing <think> ids")
    actual = (int(open_id), int(close_id))
    if any(item < 0 for item in actual):
        raise ValueError("tokenizer missing <think> ids")
    if expected is not None and tuple(int(item) for item in expected) != actual:
        raise ValueError(f"think ids {actual} do not match card {tuple(expected)}")
    return actual


def load_frozen(name: str, local_files_only: bool | None = None, device: str | None = None, dtype=None):
    info = card(name)
    from transformers import AutoModelForCausalLM, AutoTokenizer

    local_only = _local_files_only(local_files_only)
    device_obj = infer_device(device)
    dtype_obj = infer_dtype(device_obj, dtype)
    tokenizer = AutoTokenizer.from_pretrained(
        info["id"], revision=info["revision"], local_files_only=local_only
    )
    think_ids = think_ids_from_tokenizer(tokenizer, info.get("think_ids"))
    model = AutoModelForCausalLM.from_pretrained(
        info["id"],
        revision=info["revision"],
        local_files_only=local_only,
        torch_dtype=dtype_obj,
    )
    model.to(device_obj)
    model.eval()
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    return {
        "model": model,
        "tokenizer": tokenizer,
        "card": info,
        "device": str(device_obj),
        "dtype": str(dtype_obj).removeprefix("torch."),
        "think_ids": list(think_ids),
        "cuda": device_obj.type == "cuda",
        "cuda_name": torch.cuda.get_device_name(device_obj) if device_obj.type == "cuda" else None,
    }
