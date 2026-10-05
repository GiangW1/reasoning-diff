from pathlib import Path

import pytest

from reasoning_diff import cli
from reasoning_diff.checkpoints import TraceCheckpoints
from reasoning_diff.io import read_json, read_jsonl, write_json
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def test_prepare_recovers_saved_traces_after_interruption(tmp_path, t1_tiny_path, monkeypatch):
    from reasoning_diff.models import generate

    out = tmp_path / "prepare"
    calls = []

    def interrupted(task, **kwargs):
        calls.append(kwargs["run_id"])
        if len(calls) == 3:
            raise RuntimeError("simulated interruption")
        return cli._synthetic_trace(task, cli._trace_text(task), kwargs["run_id"], kwargs["seed"])

    monkeypatch.setattr(generate, "generate_task_trace", interrupted)
    args = [
        "prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(out),
        "--eval-mode", "scientific", "--checkpoint-traces", "--max-new", "2",
        "--split-fractions", "0.4", "0.15", "0.1", "0.1", "0.1", "0.15",
    ]
    with pytest.raises(RuntimeError, match="simulated interruption"):
        cli.main(args)
    saved = {path.name: path.read_bytes() for path in (out / "checkpoints" / "traces").glob("*.json")}
    assert len(saved) == 2
    assert read_json(out / "progress.json")["saved_traces"] == 2

    resumed_calls = []

    def resumed(task, **kwargs):
        resumed_calls.append(kwargs["run_id"])
        return cli._synthetic_trace(task, cli._trace_text(task), kwargs["run_id"], kwargs["seed"])

    monkeypatch.setattr(generate, "generate_task_trace", resumed)
    assert cli.main([*args, "--resume"]) == 0
    assert not set(calls[:2]) & set(resumed_calls)
    for name, payload in saved.items():
        assert (out / "checkpoints" / "traces" / name).read_bytes() == payload
    progress = read_json(out / "progress.json")
    assert progress["status"] == "complete"
    assert progress["completed_tasks"] == 1
    assert read_json(out / "manifest.json")["success_count"] == 1
    assert len(read_jsonl(out / "traces.jsonl")) == len(calls[:2]) + len(resumed_calls)


def test_checkpoint_rejects_changed_protocol(tmp_path):
    TraceCheckpoints(tmp_path, {"config": {"n_tasks": 1, "max_new": 4096}})
    with pytest.raises(ValueError, match="specification mismatch"):
        TraceCheckpoints(tmp_path, {"config": {"n_tasks": 1, "max_new": 2048}}, resume=True)


def test_checkpoint_rejects_corruption_without_regenerating(tmp_path, t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    store = TraceCheckpoints(tmp_path, {"config": {"n_tasks": 1}})
    trace = cli._synthetic_trace(task, cli._trace_text(task), "base", 0)
    store.wrap(lambda *_args, **_kwargs: trace)(task, run_id="base", seed=0)
    path = next((tmp_path / "checkpoints" / "traces").glob("*.json"))
    row = read_json(path)
    row["trace"]["text"] = "corrupted"
    write_json(path, row)
    recovered = TraceCheckpoints(tmp_path, {"config": {"n_tasks": 1}}, resume=True)

    def forbidden(*_args, **_kwargs):
        pytest.fail("a corrupted saved sample must not silently regenerate")

    with pytest.raises(ValueError, match="hash mismatch"):
        recovered.wrap(forbidden)(task, run_id="base", seed=0)
