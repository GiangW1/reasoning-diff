import importlib
from pathlib import Path

import pytest
import torch

from reasoning_diff import cli
from reasoning_diff.models import generate
from reasoning_diff.models.tiny import build_tiny
from reasoning_diff.schema import Task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.fixture
def batching_modules(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("trace_batching"), importlib.import_module("prepare_batched")


def test_batch_keeps_per_row_rng_padding_and_stops(batching_modules):
    batching, _ = batching_modules
    model = build_tiny("qwen2").eval()
    prompts = [torch.tensor([[1, 2, 3]]), torch.tensor([[1, 2, 3, 4, 5]])]
    expected = [generate.decode_loop(model, prompt, torch.Generator().manual_seed(seed), 8,
                temperature=0.6, top_k=20, top_p=0.95)["generated_ids"]
                for seed, prompt in enumerate(prompts)]
    requests = [batching.DecodeRequest(model, prompt, torch.Generator().manual_seed(seed), 8,
                temperature=0.6, top_k=20, top_p=0.95)
                for seed, prompt in enumerate(prompts)]
    results = batching.decode_batch(requests)
    assert [row["generated_ids"] for row in results] == expected
    assert [row["prompt_ids"] for row in results] == [prompt.reshape(-1).tolist() for prompt in prompts]
    for seed, request in enumerate(requests):
        request.generator.manual_seed(seed)
    requests[0].stop_condition = lambda produced: len(produced) == 2
    stopped = batching.decode_batch(requests)
    assert stopped[0]["generated_ids"] == expected[0][:2]
    assert stopped[0]["stop_reason"] == "stop_condition"
    assert stopped[1]["generated_ids"] == expected[1]
    assert stopped[1]["stop_reason"] == "max_new"


def test_batch_request_plan_matches_existing_prepare(batching_modules, tmp_path, t1_tiny_path, monkeypatch):
    _, runner = batching_modules
    original = load_t1_fixture(t1_tiny_path)
    second = Task.from_dict({**original.to_dict(), "task_id": "second", "base_group_id": "second"})
    monkeypatch.setattr(cli, "_load_tasks", lambda _args: [original, second])
    stage_args = ["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(tmp_path / "out"),
                  "--eval-mode", "scientific", "--split-fractions", "0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]
    args = cli.build_parser().parse_args(stage_args)
    planned = [runner.request_key(task, seed, run) for task, seed, run in runner.prepare_requests(args)]
    actual = []

    def record(task, **kwargs):
        actual.append(runner.request_key(task, kwargs["seed"], kwargs["run_id"]))
        return cli._synthetic_trace(task, cli._trace_text(task), kwargs["run_id"], kwargs["seed"])

    monkeypatch.setattr(generate, "generate_task_trace", record)
    assert cli.main(stage_args) == 0
    assert actual == planned
