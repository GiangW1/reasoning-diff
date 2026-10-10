"""Frozen model cards. Revisions are required; 'latest' is rejected."""
from __future__ import annotations

import os
from pathlib import Path

import torch

MODELS = {
    "qwen3-8b": {
        "id": "Qwen/Qwen3-8B",
        "revision": "b968826d9c46dd6066d109eabc6255188de91218",
        "arch": "qwen3",
        "hidden_size": 4096,
        "layers": 36,
        "think_ids": (151667, 151668),
        "tokenizer_special_ids": {"bos": 151643, "eos": 151645, "pad": 151643},
        "required_tokenizer_special_ids": ("eos", "pad"),
        "context_limit": 32768,
    },
    "qwen3-14b": {
        "id": "Qwen/Qwen3-14B",
        "revision": "40c069824f4251a91eefaf281ebe4c544efd3e18",
        "arch": "qwen3",
        "hidden_size": 5120,
        "layers": 40,
        "think_ids": (151667, 151668),
        "tokenizer_special_ids": {"bos": 151643, "eos": 151645, "pad": 151643},
        "required_tokenizer_special_ids": ("eos", "pad"),
        "context_limit": 40960,
    },
    "r1-distill-qwen-7b": {
        "id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "revision": "916b56a44061fd5cd7d6a8fb632557ed4f724f60",
        "arch": "qwen2",
        "hidden_size": 3584,
        "layers": 28,
        "think_ids": (151648, 151649),
        "tokenizer_special_ids": {"bos": 151643, "eos": 151645, "pad": 151643},
        "required_tokenizer_special_ids": ("eos", "pad"),
        "context_limit": 16384,
    },
    "r1-distill-qwen-14b": {
        "id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
        "revision": "1df8507178afcc1bef68cd8c393f61a886323761",
        "arch": "qwen2",
        "hidden_size": 5120,
        "layers": 48,
        "think_ids": (151648, 151649),
        "tokenizer_special_ids": {"bos": 151643, "eos": 151645, "pad": 151643},
        "required_tokenizer_special_ids": ("eos", "pad"),
        "context_limit": 131072,
    },
    "r1-distill-qwen-32b": {
        "id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "revision": "711ad2ea6aa40cfca18895e8aca02ab92df1a746",
        "arch": "qwen2",
        "hidden_size": 5120,
        "layers": 64,
        "think_ids": (151648, 151649),
        "tokenizer_special_ids": {"bos": 151643, "eos": 151645, "pad": 151643},
        "required_tokenizer_special_ids": ("eos", "pad"),
        "context_limit": 131072,
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


def _model_source(name: str, info: dict) -> str:
    """Use a verified local snapshot when RD_MODEL_ROOT is configured."""
    root = os.environ.get("RD_MODEL_ROOT")
    if root:
        local_name = {
            "qwen3-8b": "Qwen3-8B",
            "qwen3-14b": "Qwen3-14B",
            "r1-distill-qwen-7b": "DeepSeek-R1-Distill-Qwen-7B",
            "r1-distill-qwen-14b": "DeepSeek-R1-Distill-Qwen-14B",
            "r1-distill-qwen-32b": "DeepSeek-R1-Distill-Qwen-32B",
        }.get(name)
        if local_name:
            path = Path(root) / local_name
            if (path / "config.json").is_file():
                return str(path)
    return info["id"]


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


def validate_loaded_model(model, tokenizer, info: dict) -> dict:
    """Check runtime structure against the pinned model card."""
    config = getattr(model, "config", None)
    checks = {
        "hidden_size": getattr(config, "hidden_size", None),
        "layers": getattr(config, "num_hidden_layers", None),
        "context_limit": getattr(config, "max_position_embeddings", None),
    }
    missing_structure = [
        key for key, value in checks.items()
        if info.get(key) is not None and value is None
    ]
    mismatches = {
        key: {"expected": info.get(key), "actual": value}
        for key, value in checks.items()
        if value is not None and info.get(key) is not None
        and (int(value) < int(info[key]) if key == "context_limit" else int(value) != int(info[key]))
    }
    if mismatches:
        raise ValueError(f"checkpoint structure does not match model card: {mismatches}")
    if tokenizer is None:
        raise ValueError("frozen checkpoint requires tokenizer")
    special_ids = {
        "bos": getattr(tokenizer, "bos_token_id", None),
        "eos": getattr(tokenizer, "eos_token_id", None),
        "pad": getattr(tokenizer, "pad_token_id", None),
    }
    expected_special_ids = info.get("tokenizer_special_ids") or {}
    special_mismatches = {
        key: {"expected": expected_special_ids[key], "actual": value}
        for key, value in special_ids.items()
        if expected_special_ids.get(key) is not None and value is not None
        and value not in (expected_special_ids[key] if isinstance(expected_special_ids[key], list) else [expected_special_ids[key]])
    }
    if special_mismatches:
        raise ValueError(f"tokenizer special ids do not match model card: {special_mismatches}")
    required_ids = tuple(info.get("required_tokenizer_special_ids") or special_ids)
    missing_required = [key for key in required_ids if special_ids.get(key) is None]
    return {
        "validation_status": "verified" if config is not None and not missing_structure and not missing_required else "injected_runtime_unverified",
        "config": checks,
        "missing_structure_fields": missing_structure,
        "tokenizer_special_ids": special_ids,
        "expected_tokenizer_special_ids": expected_special_ids,
        "missing_tokenizer_special_ids": [key for key, value in special_ids.items() if value is None],
        "missing_required_tokenizer_special_ids": missing_required,
        "attention_backend": getattr(config, "_attn_implementation", None) if config is not None else None,
    }


def load_frozen(name: str, local_files_only: bool | None = None, device: str | None = None, dtype=None):
    info = card(name)
    from transformers import AutoModelForCausalLM, AutoTokenizer

    local_only = _local_files_only(local_files_only)
    source = _model_source(name, info)
    device_obj = infer_device(device)
    dtype_obj = infer_dtype(device_obj, dtype)
    tokenizer = AutoTokenizer.from_pretrained(
        source, revision=info["revision"], local_files_only=local_only
    )
    think_ids = think_ids_from_tokenizer(tokenizer, info.get("think_ids"))
    model = AutoModelForCausalLM.from_pretrained(
        source,
        revision=info["revision"],
        local_files_only=local_only,
        torch_dtype=dtype_obj,
    )
    model.to(device_obj)
    model.eval()
    validation = validate_loaded_model(model, tokenizer, info)
    # Manual decoding and hooks do not need Transformers' output capture.
    # Disable the legacy Qwen3 decorator path that can reject valid forwards
    # with a misleading kwargs error.
    for flag in ("output_hidden_states", "output_attentions"):
        if hasattr(getattr(model, "config", None), flag):
            setattr(model.config, flag, False)
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
        "validation": validation,
    }
