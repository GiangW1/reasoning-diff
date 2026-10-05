import importlib
from pathlib import Path

import pytest

from reasoning_diff import cli
from reasoning_diff.io import file_digest, read_json, read_jsonl


@pytest.fixture
def modules(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("fit_cached_inputs"), importlib.import_module("postprocess_pr7")


@pytest.mark.parametrize("position", ["pre_step", "all"])
def test_cached_fit_matches_original_outputs(modules, tmp_path, t1_tiny_path, position, monkeypatch):
    cached, _ = modules
    prep, collect, label = [tmp_path / name for name in ("prep", "collect", "label")]
    assert cli.main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert cli.main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(collect), "--backend", "tiny"]) == 0
    assert cli.main(["label", "--in-dir", str(prep), "--out-dir", str(label)]) == 0
    common = ["fit", "--in-dir", str(collect), "--labels-dir", str(label), "--split", "probe_train", "--position", position]
    event_hash = file_digest(collect / "event_rows.jsonl")
    original_read = cli.read_jsonl
    file_reads = 0

    def counted_read(path):
        nonlocal file_reads
        if Path(path).resolve() == (collect / "event_rows.jsonl").resolve():
            file_reads += 1
        return original_read(path)

    monkeypatch.setattr(cli, "read_jsonl", counted_read)
    assert cli.main([*common, "--out-dir", str(tmp_path / "normal")]) == 0
    baseline_reads = file_reads
    assert cached.main([*common, "--out-dir", str(tmp_path / "cached")]) == 0
    for filename in ("probes.jsonl", "p1_table.jsonl"):
        assert read_jsonl(tmp_path / "normal" / filename) == read_jsonl(tmp_path / "cached" / filename)
    assert file_digest(collect / "event_rows.jsonl") == event_hash
    stats = read_json(tmp_path / "cached/input_cache.json")
    assert stats["file_reads"] == 1
    assert stats["cache_hits"] > 0
    assert baseline_reads > stats["file_reads"]
    assert file_reads - baseline_reads == 1
    if position == "all":
        def unexpected_fit(*_args, **_kwargs):
            raise AssertionError("completed position fits must be reused during assembly")

        monkeypatch.setattr(cli.BilinearProbe, "fit", unexpected_fit)
        assert cached.main([*common, "--out-dir", str(tmp_path / "cached"), "--resume"]) == 0
        assert read_json(tmp_path / "cached/input_cache.json")["file_reads"] == 0


def test_parallel_jobs_respect_dependencies_and_resource_limits(modules):
    _, parallel = modules
    current = {}
    starts = []
    snapshots = []

    class Process:
        def __init__(self, steps):
            self.steps = steps

        def poll(self):
            self.steps -= 1
            return 0 if self.steps <= 0 else None

    jobs = [parallel.Job("label", []), parallel.Job("collect0", [], gpu=True), parallel.Job("collect1", [], gpu=True),
            parallel.Job("fit0", [], ("label", "collect0")), parallel.Job("fit1", [], ("label", "collect1")),
            parallel.Job("report", [], ("fit0", "fit1"))]

    def launch(job, gpu):
        assert all(current.get(dep) == "complete" for dep in job.dependencies)
        if gpu is not None:
            assert all(device != gpu or current[name] != "running" for name, device in starts)
        starts.append((job.name, gpu))
        return Process(4 if job.name == "collect1" else 2)

    def update(states):
        current.clear()
        current.update(states)
        snapshots.append(states)
        assert sum(states[name] == "running" and gpu is None for name, gpu in starts) <= 2

    parallel.run_jobs(jobs, launch, [2, 3], update=update, pause=lambda _seconds: None)
    assert all(state == "complete" for state in current.values())
    assert any(state["fit0"] == "running" and state["collect1"] == "running" for state in snapshots)
    assert starts[-1][0] == "report"


def test_failed_stage_never_launches_its_dependents(modules):
    _, parallel = modules
    starts = []

    class Failed:
        def poll(self):
            return 1

    def launch(job, _gpu):
        starts.append(job.name)
        return Failed()

    with pytest.raises(RuntimeError, match="postprocessing jobs failed"):
        parallel.run_jobs([parallel.Job("fit", []), parallel.Job("report", [], ("fit",))], launch, [2], pause=lambda _seconds: None)
    assert starts == ["fit"]
