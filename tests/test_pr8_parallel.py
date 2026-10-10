import importlib
from pathlib import Path
from threading import Barrier, Event, Lock
from types import SimpleNamespace

import pytest

from reasoning_diff.io import read_jsonl
from reasoning_diff.models import generate
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("run_pr8")


def test_layer_sweep_overlaps_collection_and_fit_with_resource_limits(runner, tmp_path):
    first_collectors = Barrier(3)
    first_fits = Barrier(2)
    fit_started = Event()
    lock = Lock()
    collected = set()
    occupied = set()
    state = {"label_done": False, "cpu": 0, "peak_cpu": 0, "fit_count": 0}

    def stage(name, command, *options, gpu=None):
        if command == "label":
            state["label_done"] = True
            return
        layer = int(name.rsplit("-", 1)[1])
        if command == "collect":
            with lock:
                assert gpu not in occupied
                occupied.add(gpu)
            if layer != 35:
                first_collectors.wait(timeout=10)
            else:
                assert fit_started.wait(timeout=10)
            with lock:
                collected.add(layer)
                occupied.remove(gpu)
        elif command == "fit":
            with lock:
                assert state["label_done"] and layer in collected
                state["cpu"] += 1
                state["peak_cpu"] = max(state["peak_cpu"], state["cpu"])
                state["fit_count"] += 1
                first_pair = state["fit_count"] <= 2
            fit_started.set()
            if first_pair:
                first_fits.wait(timeout=10)
            with lock:
                state["cpu"] -= 1

    runner.layer_sweep(stage, tmp_path / "smoke", tmp_path, tmp_path / "prep", tmp_path / "label",
                       "qwen3-8b", [2, 3, 6], [0, 12, 24, 35])
    assert collected == {0, 12, 24, 35}
    assert not occupied
    assert state["peak_cpu"] == 2 and state["fit_count"] == 4


def test_layer_sweep_propagates_failed_fit(runner, tmp_path):
    def stage(_name, command, *_options, **_kwargs):
        if command == "fit":
            raise RuntimeError("fit failed")

    with pytest.raises(RuntimeError, match="fit failed"):
        runner.layer_sweep(stage, tmp_path / "smoke", tmp_path, tmp_path / "prep", tmp_path / "label",
                           "qwen3-8b", [2], [0])


def test_batched_pilot_preserves_requests_and_resumes(runner, tmp_path, t1_tiny_path, monkeypatch):
    task = load_t1_fixture(t1_tiny_path)
    monkeypatch.setattr(runner.cli, "_load_tasks", lambda _args: [task, task])
    loads = []
    monkeypatch.setattr(runner.cli, "_load_frozen_runtime", lambda _args: loads.append(True) or {})
    batching = importlib.import_module("trace_batching")

    class Decoder:
        def __init__(self, batch_size):
            assert batch_size == 2

        def __call__(self):
            return {"batch_execution": {"backend": "test_batched"}}

        def close(self):
            pass

    monkeypatch.setattr(batching, "BatchDecoder", Decoder)
    calls = []

    def generate_trace(_task, **kwargs):
        assert kwargs["max_new"] == 32768 and kwargs["enable_thinking"]
        generate.decode_loop()
        calls.append((kwargs["run_id"], kwargs["seed"]))
        trace = SimpleNamespace(metadata={}, id=kwargs["run_id"], seed=kwargs["seed"])
        trace.to_dict = lambda: {"id": trace.id, "seed": trace.seed, "metadata": trace.metadata}
        return trace

    monkeypatch.setattr(generate, "generate_task_trace", generate_trace)
    original_decode = generate.decode_loop
    args = SimpleNamespace(dataset=t1_tiny_path, out_root=tmp_path, model="qwen3-8b", max_new=32768, batch_size=2)
    runner.pilot_worker(args)
    traces = read_jsonl(tmp_path / "traces.jsonl")
    assert [(row["id"], row["seed"]) for row in traces] == [
        (f"trace-base:{index}:seed{seed}", seed) for index in range(2) for seed in range(3)]
    assert all(row["metadata"]["execution"]["backend"] == "test_batched" for row in traces)
    assert generate.decode_loop is original_decode
    runner.pilot_worker(args)
    assert len(calls) == 6 and len(loads) == 1
    assert read_jsonl(tmp_path / "traces.jsonl") == traces
