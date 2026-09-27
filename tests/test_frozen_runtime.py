"""Offline coverage for the paper frozen path. No downloads, no real 7B/8B weights."""
from __future__ import annotations

import pytest
import torch

from reasoning_diff.cli import build_parser, main
from reasoning_diff.io import read_json, read_jsonl
from reasoning_diff.models.adapters import card, infer_device, infer_dtype, load_frozen, think_ids_from_tokenizer
from reasoning_diff.models.collect import intervene_hidden_decode
from reasoning_diff.models.generate import decode_loop, generate_frozen_trace, generate_task_trace
from reasoning_diff.models.tiny import build_tiny
from reasoning_diff.models.tokenize import readout_layer_index
from reasoning_diff.repair import execute_repair_frozen
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


class _Tok:
    eos_token_id = None

    def __init__(self, think=(151667, 151668)):
        self.think = think

    def convert_tokens_to_ids(self, token: str):
        return self.think[0] if token == "<think>" else self.think[1]

    def apply_chat_template(self, messages, **_kwargs):
        text = messages[0]["content"]
        ids = [(ord(ch) % 63) + 1 for ch in text[:6]] or [1]
        return torch.tensor([ids], dtype=torch.long)

    def decode(self, ids, skip_special_tokens=True):
        if hasattr(ids, "tolist"):
            ids = ids.tolist()
        if ids and isinstance(ids[0], list):
            ids = ids[0]
        if len(ids) == 1:
            return chr(97 + (int(ids[0]) % 26))
        return "q = 0"


def _packed(task_model=None, context_limit=128):
    model = task_model or build_tiny("qwen2")
    return {
        "model": model,
        "tokenizer": _Tok(),
        "card": {
            "name": "qwen3-8b",
            "id": "local-tiny",
            "arch": "qwen2",
            "revision": "test",
            "layers": 3,
            "context_limit": context_limit,
            "think_ids": (151667, 151668),
        },
        "device": "cpu",
        "dtype": "float32",
        "think_ids": [151667, 151668],
        "cuda_name": None,
    }


def test_infer_device_and_cuda_bf16():
    assert infer_device("cpu").type == "cpu"
    assert infer_dtype(torch.device("cpu")) == torch.float32
    assert infer_dtype(torch.device("cuda")) == torch.bfloat16
    if not torch.cuda.is_available():
        assert infer_device().type == "cpu"


def test_cards_record_paper_context_and_think_ids():
    qwen = card("qwen3-8b")
    r1 = card("r1-distill-qwen-7b")
    assert qwen["context_limit"] == 32768
    assert r1["context_limit"] == 16384
    assert qwen["think_ids"] == (151667, 151668)
    assert r1["think_ids"] == (151648, 151649)
    assert qwen["name"] == "qwen3-8b"
    assert readout_layer_index(36) in range(21, 27)
    assert readout_layer_index(28) in range(16, 22)


def test_think_ids_must_match_card():
    tok = _Tok((1, 2))
    with pytest.raises(ValueError, match="think ids"):
        think_ids_from_tokenizer(tok, (151667, 151668))
    assert think_ids_from_tokenizer(_Tok(), (151667, 151668)) == (151667, 151668)


def test_load_frozen_places_eval_and_dtype(monkeypatch):
    import transformers

    captured = {}

    class Mod(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.p = torch.nn.Parameter(torch.ones(1))

        def eval(self):
            return super().eval()

    model = Mod()

    monkeypatch.setattr(transformers.AutoTokenizer, "from_pretrained", staticmethod(lambda *a, **k: _Tok()))

    def fake_model(*_args, **kwargs):
        captured.update(kwargs)
        return model

    monkeypatch.setattr(transformers.AutoModelForCausalLM, "from_pretrained", staticmethod(fake_model))
    packed = load_frozen("qwen3-8b", device="cpu")
    assert captured["revision"] == "b968826d9c46dd6066d109eabc6255188de91218"
    assert captured["local_files_only"] is True
    assert captured["torch_dtype"] == torch.float32
    assert packed["device"] == "cpu"
    assert packed["think_ids"] == [151667, 151668]
    assert all(not item.requires_grad for item in packed["model"].parameters())
    assert not packed["model"].training


def test_decode_loop_keeps_prompt_then_appends():
    model = build_tiny("qwen2")
    prompt = torch.tensor([[1, 2, 3]], dtype=torch.long)
    out = decode_loop(model, prompt, torch.Generator().manual_seed(0), max_new=2)
    assert out["prompt_ids"] == [1, 2, 3]
    assert len(out["generated_ids"]) == 2
    assert out["token_ids"][:3] == [1, 2, 3]
    assert out["device"] == "cpu"


def test_generate_frozen_reuses_packed_and_does_not_force_target(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    packed = _packed()
    trace = generate_frozen_trace(task, "qwen3-8b", packed=packed, max_new=3, seed=0)
    assert trace.metadata["weight_source"] == "frozen_checkpoint"
    assert trace.metadata["forced_target"] is False
    assert trace.metadata["parse_region"] == "generated"
    assert trace.cost.decode_tokens == 3
    assert trace.cost.prefill_tokens > 0
    assert trace.metadata["device"] == "cpu"
    via_dispatch = generate_task_trace(task, backend="frozen", model_name="qwen3-8b", packed=packed, max_new=2)
    assert via_dispatch.metadata["forced_target"] is False
    assert via_dispatch.cost.decode_tokens == 2


def test_generate_frozen_refuses_overlong_prompt(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    packed = _packed(context_limit=2)
    with pytest.raises(ValueError, match="context"):
        generate_frozen_trace(task, "qwen3-8b", packed=packed, max_new=1)


def test_generate_frozen_requires_name():
    with pytest.raises(ValueError, match="model-name"):
        generate_task_trace(object(), backend="frozen")


def test_intervene_hidden_decode_accepts_injected_model():
    import numpy as np

    model = build_tiny("qwen2")
    donor = np.ones(32)
    out = intervene_hidden_decode("qwen2", [1, 2, 3], 1, donor=donor, model=model, max_new=2)
    assert out["hook_fired"]
    assert len(out["generated_ids"]) == 2
    assert "baseline_generated_ids" in out


def test_execute_repair_frozen_prefills_current_prefix():
    packed = _packed()
    out = execute_repair_frozen("task_oracle", ["q"], [1, 2, 3, 4], "q = 1", packed=packed, max_new=2)
    assert out["refilled_prefix"] is True
    assert out["extra_prefill_tokens"] == len(out["prefix_token_ids"])
    assert len(out["generated_ids"]) == 2
    assert len(out["prefill_hidden"]) == 32


def test_cli_accepts_frozen_backends():
    parser = build_parser()
    intervene = parser.parse_args(["intervene", "--out-dir", "x", "--backend", "frozen", "--model-name", "qwen3-8b"])
    assert intervene.backend == "frozen"
    assert intervene.model_name == "qwen3-8b"
    repair = parser.parse_args(["repair", "--out-dir", "x", "--backend", "frozen", "--model-name", "r1-distill-qwen-7b"])
    assert repair.backend == "frozen"
    prepare = parser.parse_args(["prepare", "--fixture", "f", "--out-dir", "x", "--backend", "frozen", "--model-name", "qwen3-8b", "--max-new", "128"])
    assert prepare.max_new == 128


def test_frozen_cli_pipeline_uses_injected_runtime(tmp_path, t1_tiny_path, monkeypatch):
    from reasoning_diff import cli

    packed = _packed()
    monkeypatch.setattr(cli, "_load_frozen_runtime", lambda _args: packed)
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    inter = tmp_path / "inter"
    repair = tmp_path / "repair"
    fractions = ["0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *fractions]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--eval-mode", "scientific", "--backend", "frozen", "--model-name", "qwen3-8b"]) == 0
    spec = read_json(col / "run_spec.json")
    assert spec["config"]["weight_source"] == "frozen_checkpoint"
    assert spec["config"]["hidden_layer"] == readout_layer_index(3)
    assert spec["config"]["revision"] == "test"
    assert main(["intervene", "--in-dir", str(col), "--out-dir", str(inter), "--backend", "frozen", "--model-name", "qwen3-8b"]) == 0
    row = read_jsonl(inter / "interventions.jsonl")[0]
    assert row["status"] in {"prospective_decode", "geometry_on_hidden"}
    assert row["relative"]["revision"] == "test"
    assert main(["repair", "--in-dir", str(col), "--out-dir", str(repair), "--backend", "frozen", "--model-name", "qwen3-8b", "--eval-mode", "scientific"]) == 0
    recs = read_jsonl(repair / "repairs.jsonl")
    assert recs
    assert recs[0]["refilled_prefix"] is True
    assert recs[0]["extra_prefill_tokens"]


def test_frozen_cli_requires_model_name(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    with pytest.raises(ValueError, match="model-name"):
        main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(tmp_path / "col"), "--backend", "frozen"])
