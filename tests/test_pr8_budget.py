import importlib
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest

from reasoning_diff import cli
from reasoning_diff.io import read_json, read_jsonl, write_jsonl
from reasoning_diff.splits import DEFAULT_FRACTIONS, split_for_task
from reasoning_diff.tasks.t1_official import load_igsm_snapshot


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("run_pr8")


def test_budget_cohort_is_balanced_disjoint_and_keeps_existing_splits(runner):
    inputs = Path(__file__).resolve().parents[1] / "artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200"
    smoke, full = runner.cohorts(inputs.glob("igsm-official-*.json"))
    selected = runner.limit_formal(full, 32)
    assert len(selected) == len(set(selected)) == 32
    assert not set(smoke) & set(selected)
    assert selected == runner.limit_formal(list(reversed(full)), 32)
    counts = Counter()
    for path in selected:
        task = load_igsm_snapshot(path)
        counts[task.metadata["op"], split_for_task(task, seed=0, fractions=DEFAULT_FRACTIONS)] += 1
    for op in (5, 10, 15, 21):
        assert {role: counts[op, role] for role in ("probe_train", "dev", "calibration", "test")} == {
            "probe_train": 4, "dev": 1, "calibration": 1, "test": 2}
    assert runner.limit_formal(full, None) is full
    with pytest.raises(ValueError, match="formal limit"):
        runner.limit_formal(full, 31)


def test_intervention_shards_keep_all_pairs_and_all_controls(tmp_path, monkeypatch):
    src = tmp_path / "input"
    write_jsonl(src / "edits.jsonl", [{"kind": "source_value_pair", "base_task_id": f"t{i}",
                "trace_ids": {"base": f"b{i}", "same_value_diff_source": f"s{i}", "same_source_diff_value": f"v{i}"}}
                for i in range(5)])
    write_jsonl(src / "splits.jsonl", [{"task_id": f"t{i}", "role": "test"} for i in range(5)])

    def impl(args):
        write_jsonl(Path(args.out_dir) / "interventions.jsonl", [{"condition": c, "status": "prospective_decode"}
                    for c in ("baseline", "main", "crand", "clayer")])
        return 0

    monkeypatch.setattr(cli, "_cmd_intervene_impl", impl)
    common = ["intervene", "--in-dir", str(src), "--all-source-pairs", "--pair-split", "test"]
    sequential = tmp_path / "sequential"
    assert cli.main([*common, "--out-dir", str(sequential)]) == 0
    merged = []
    for index in range(3):
        out = tmp_path / f"shard{index}"
        assert cli.main([*common, "--out-dir", str(out), "--pair-shard", str(index), "3"]) == 0
        rows = read_jsonl(out / "interventions.jsonl")
        assert all(r["pair_index"] % 3 == index for r in rows)
        merged.extend(rows)
    key = lambda r: (r["pair_index"], r["pair_kind"], r["condition"])
    assert sorted(merged, key=key) == sorted(read_jsonl(sequential / "interventions.jsonl"), key=key)
    assert len({key(r) for r in merged}) == len(merged) == 40
    with pytest.raises(ValueError, match="pair shard"):
        cli.cmd_intervene(cli.build_parser().parse_args([*common, "--out-dir", str(tmp_path / "invalid"), "--pair-shard", "3", "3"]))


def test_deadline_is_preserved_on_resume_and_prevents_new_work(runner, tmp_path, t1_tiny_path, monkeypatch):
    monkeypatch.setitem(__import__("sys").modules, "fcntl", SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *_args: None))
    monkeypatch.setattr(runner, "SERVER", tmp_path)
    monkeypatch.setattr(runner.shutil, "disk_usage", lambda _: SimpleNamespace(free=10 * 1024**3))
    monkeypatch.setattr(runner, "cohorts", lambda _paths: ([t1_tiny_path], [t1_tiny_path]))
    monkeypatch.setattr(runner.subprocess, "check_output", lambda *_a, **_kw: "/dev/mock\n")
    clock = {"now": 100.0}
    monkeypatch.setattr(runner.time, "time", lambda: clock["now"])
    pilot_calls = []

    def run(command, **kwargs):
        if "pilot-worker" in command:
            assert 0 < kwargs["timeout"] <= 0.36
            pilot_calls.append(command)
            clock["now"] = 101.0
            raise runner.subprocess.TimeoutExpired(command, timeout=kwargs["timeout"])
        return SimpleNamespace(stdout="")

    monkeypatch.setattr(runner.subprocess, "run", run)
    out = tmp_path / "out"
    args = ["--mode", "full", "--out-root", str(out), "--dataset", str(tmp_path), "--gpus", "2", "--time-budget-hours", "0.0001"]
    for _ in range(2):
        with pytest.raises(runner.subprocess.TimeoutExpired):
            runner.main(args)
        assert read_json(out / "pipeline.json")["status"] == "budget_exhausted"
        assert read_json(out / "execution_budget.json")["started_at_epoch"] == 100.0
    assert len(pilot_calls) == 1
