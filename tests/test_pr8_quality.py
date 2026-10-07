import importlib
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from reasoning_diff import cli
from reasoning_diff.events import assign_event_regions, parse_events
from reasoning_diff.io import read_json, write_json, write_jsonl
from reasoning_diff.next_round import c2_summary, intervention_coverage, measurement_report, sentence_graph_task
from reasoning_diff.schema import Task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def data(task, n=3, noise_references=None):
    traces, observations = [], []
    event = parse_events("q = 7", task)[0]
    assign_event_regions([event], "q = 7", initial_thinking=True)
    for seed in range(n):
        tid = f"base{seed}"
        traces.append({"id": tid, "task_id": task.task_id, "seed": seed, "events": [event.to_dict()],
                       "status": "natural_complete", "correct": True, "metadata": {"boundary_status": "ok", "generated_tokens": 100}})
        for pid in ("unused_a", "unused_b"):
            observations.append({"reference_trace": tid, "alignment_ref": event.identity.key(), "premise_id": pid,
                                 "outcome": "no_change", "rng_pair": f"stream:{seed}", "task_id": task.task_id})
        if noise_references is None or seed in noise_references:
            observations.append({"reference_trace": tid, "alignment_ref": event.identity.key(), "premise_id": "sham:q",
                                 "outcome": "no_change", "rng_pair": "sham:1", "task_id": task.task_id})
    return traces, observations


def test_rho_on_one_seed_cannot_pass_measurement(t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    traces, obs = data(task, noise_references={0})
    report = measurement_report(traces, [task.to_dict()], obs, [])
    assert report["overall"]["matched_cell_coverage"] == 1
    assert report["overall"]["rho_coverage"] == pytest.approx(1 / 3)
    assert not report["checks"]["rho_coverage"]
    assert not report["checks"]["common_noise_coverage"]


def test_fully_matched_target_cannot_hide_missing_intermediate_variables(t1_tiny_path):
    original = load_t1_fixture(t1_tiny_path).to_dict()
    original["nodes"] = [
        {"id": "r", "aliases": ["r"], "parents": ["p1"], "value": "4", "expression": "p1"},
        {"id": "s", "aliases": ["s"], "parents": ["p2"], "value": "0", "expression": "p2"},
        {"id": "q", "aliases": ["q"], "parents": ["r", "s"], "value": "0", "expression": "r * s"}]
    task = sentence_graph_task(Task.from_dict(original))
    traces, obs = data(task)
    report = measurement_report(traces, [task.to_dict()], obs, [])
    assert report["overall"]["matched_cell_coverage"] == 1
    assert report["overall"]["variable_coverage"] == pytest.approx(1 / 3)
    assert not report["checks"]["variable_coverage"]
    assert report["trajectories"][0]["missing_nodes"] == ["r", "s"]
    assert report["parser_recall"] == "not_estimated_without_annotated_steps"


def test_problem_with_no_support_cannot_hide_in_global_mean(t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    other = Task.from_dict({**task.to_dict(), "task_id": "other", "base_group_id": "other"})
    first, obs = data(task)
    second, _ = data(other)
    for row in second:
        row["id"] = "other:" + row["id"]
    report = measurement_report([*first, *second], [task.to_dict(), other.to_dict()], obs, [])
    assert report["overall"]["matched_cell_coverage"] == 0.5
    assert not report["checks"]["matched_cell_coverage"]
    assert report["by_problem"]["other"]["rho_coverage"] == 0


def test_single_accuracy_class_is_reported_without_blocking_engineering_smoke(t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    traces, obs = data(task)
    report = measurement_report(traces, [task.to_dict()], obs, [])
    assert report["passed"]
    assert report["p1_estimability"] == {"status": "single_class", "class_counts": {"0": 0, "1": 3},
                                          "blocks_engineering_smoke": False}


def test_pilot_support_denominator_is_registered_not_all_unscanned_facts(t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    traces, obs = data(task)
    report = measurement_report(traces, [task.to_dict()], obs, [], {task.task_id: ["unused_a"]})
    assert report["trajectories"][0]["eligible_cells"] == 1
    assert report["trajectories"][0]["support_scope"] == "registered_pilot_facts"


def test_cached_paired_screen_uses_exact_registered_edits(t1_tiny_path):
    from itertools import permutations
    from reasoning_diff.next_round import cached_paired_screen, registered_pilot_edits
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    bases, observations = [], []
    for seed in range(3):
        trace = cli._synthetic_trace(task, "q = 7", f"base{seed}", seed)
        trace.events = assign_event_regions(parse_events(trace.text, task), trace.text, initial_thinking=True)
        trace.metadata.update(boundary_status="ok", generated_tokens=100)
        bases.append(trace)
    for left, right in permutations(bases, 2):
        observations.extend(cli._sham_observations(task, left, right, right.seed, "noise"))
    for edit in registered_pilot_edits(task):
        changed = cli._synthetic_trace(edit.task, "q = 8", edit.id, 0)
        changed.events = assign_event_regions(parse_events(changed.text, edit.task), changed.text, initial_thinking=True)
        observations.extend(cli._observations(task, bases[0], changed, edit, "stream:0", edit.id))
    rows = [trace.to_dict() for trace in bases]
    saved = [obs.to_dict() for obs in observations]
    report = cached_paired_screen(rows, [task.to_dict()], saved, [])
    assert report["passed"] and report["overall"]["n_traces"] == 1
    assert report["cache_coverage"]["planned_edits"] == report["cache_coverage"]["cached_edits"] == 3
    assert report["trajectories"][0]["support_scope"] == "registered_pilot_facts"
    assert all(obs["alignment_certificate"] for obs in saved if obs["outcome"] in {"changed", "no_change"})
    missing = [row for row in saved if row["premise_id"] != "unused_a"]
    assert not cached_paired_screen(rows, [task.to_dict()], missing, [])["checks"]["registered_edit_comparisons"]
    duplicate = [*saved, {**saved[-1], "comparison_trace": "other-cached-trace"}]
    assert not cached_paired_screen(rows, [task.to_dict()], duplicate, [])["checks"]["registered_edit_comparisons"]


def conditions(kind="same_source_diff_value"):
    return [{"base_task_id": "t", "pair_index": 0, "pair_kind": kind, "condition": condition,
             "status": "prospective_decode", "decode_complete": True, "invalid": 0,
             "actual_norm": 0 if condition == "baseline" else 1, "clayer_status": "dev_weak_layer_decode",
             "task_correct": int(condition == "baseline"), "target": None if kind == "same_value_diff_source" else int(condition == "main"),
             "analysis_eligibility": {"C2": True, "P3": False}}
            for condition in ("baseline", "main", "crand", "clayer")]


def test_duplicate_condition_does_not_complete_causal_contrast():
    rows = conditions()
    assert intervention_coverage(rows)["usable_main_contrasts"] == 1
    assert intervention_coverage([*rows, rows[0]])["usable_main_contrasts"] == 0


def test_c2_preserves_same_value_target_nonidentifiability():
    summary = c2_summary(conditions("same_value_diff_source"))
    assert summary["effects"][0]["target_follow_vs_baseline"] is None
    assert summary["effects"][0]["task_correct_vs_baseline"] == -1
    assert summary["P3"] == "not_evaluated"


def test_donor_uses_unique_phase_anchor_instead_of_occurrence_number():
    rows = [{"node_id": "q", "identity_key": f"q:{occurrence}", "trace_id": trace, "event_region": "thinking",
             "event_kind": "calculation", "event_phase": "calculation", "expression_signature": "multiply"}
            for trace, occurrence in (("base", 1), ("donor", 2))]
    pair = {"trace_ids": {"base": "base", "same_value_diff_source": "donor"}}
    h = np.array([[0., 0.], [1., 1.]])
    assert cli._pair_source_value(h, rows, pair) == (0, 1, "same_value_diff_source")
    assert cli._pair_source_value(np.vstack([h, h[1]]), [*rows, {**rows[1], "identity_key": "q:3"}], pair) is None
    rows[1]["event_phase"] = "reduction"
    assert cli._pair_source_value(h, rows, pair) is None


@pytest.mark.parametrize("base_text,donor_text", [
    ("q = 2 * 3 = 6\nq = 6 mod 5 = 1", "q = 8 mod 5 = 3\nq = 2 * 4 = 8"),
    ("q = 2 * 3 = 6\nq = 2 * 3 = 6", "q = 2 * 4 = 8"),
])
def test_donor_checks_full_trace_order_and_uncollected_repetitions(t1_tiny_path, base_text, donor_text):
    task = load_t1_fixture(t1_tiny_path)
    traces = {tid: cli._synthetic_trace(task, text, tid, 0) for tid, text in (("base", base_text), ("donor", donor_text))}
    for trace in traces.values():
        trace.events = assign_event_regions(parse_events(trace.text, task), trace.text, initial_thinking=True)
    rows = [{"node_id": "q", "identity_key": trace.events[0].identity.key(), "trace_id": tid,
             "event_region": "thinking", "event_kind": "calculation", "event_phase": "calculation",
             "expression_signature": trace.events[0].expression_signature} for tid, trace in traces.items()]
    pair = {"trace_ids": {"base": "base", "same_source_diff_value": "donor"}}
    assert cli._pair_source_value(np.array([[0., 0.], [1., 1.]]), rows, pair, traces=traces) is None


def test_source_donor_uses_only_registered_source_substitution(t1_tiny_path):
    from reasoning_diff.edits import make_source_value_pair
    task = load_t1_fixture(t1_tiny_path)
    edits = make_source_value_pair(task, "p1", "5")
    base = cli._synthetic_trace(task, "q = p1 * p2 = 0", "base", 0)
    donor = cli._synthetic_trace(edits["same_value_diff_source"].task, "q = src_b * p2 = 0", "donor", 0)
    rows = []
    for trace, owner in ((base, task), (donor, edits["same_value_diff_source"].task)):
        trace.events = assign_event_regions(parse_events(trace.text, owner), trace.text, initial_thinking=True)
        event = trace.events[0]
        rows.append({"node_id": "q", "identity_key": event.identity.key(), "trace_id": trace.id})
    pair = {"trace_ids": {"base": "base", "same_value_diff_source": "donor"}, "targets": ["q"],
            "same_value_diff_source": edits["same_value_diff_source"].to_dict()}
    h = np.array([[0., 0.], [1., 1.]])
    traces = {"base": base, "donor": donor}
    assert cli._pair_source_value(h, rows, pair, traces=traces) == (0, 1, "same_value_diff_source")
    del pair["same_value_diff_source"]
    assert cli._pair_source_value(h, rows, pair, traces=traces) is None


def test_p1_refuses_single_class_training_even_when_test_has_two_classes():
    from reasoning_diff.analysis import p1_incremental
    output = p1_incremental(np.arange(4.), np.ones(4), np.arange(4.), np.array([1, 1, 0, 1]),
                            held_out=np.array([False, False, True, True]))
    assert output["status"] == "single_class_train"
    assert output["delta_auc"] is None


def test_final_analysis_keeps_measurement_missingness_and_c2(tmp_path):
    source = tmp_path / "input"
    write_jsonl(source / "p1_table.jsonl", [{"analysis_unit": "trajectory", "trace_id": "base", "y": 1,
                                           "rho": None, "split": "test"}])
    write_jsonl(source / "interventions.jsonl", conditions("same_value_diff_source"))
    write_json(source / "measurement_report.json", {"passed": False, "failures": ["rho_coverage"]})
    assert cli.main(["analyze", "--in-dir", str(source), "--out-dir", str(tmp_path / "out")]) == 0
    report = read_json(tmp_path / "out/report.json")
    assert report["p1_coverage"]["missing_rho"] == 1
    assert report["measurement_quality"]["failures"] == ["rho_coverage"]
    assert report["c2"]["usable_main_contrasts"] == 1
    assert report["p3"] is None


@pytest.mark.parametrize("paired_failure", [False, True])
def test_measurement_failure_stops_before_any_collect_or_fit(tmp_path, t1_tiny_path, monkeypatch, paired_failure):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    runner = importlib.import_module("run_pr8")
    monkeypatch.setitem(__import__("sys").modules, "fcntl", SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *a: None))
    monkeypatch.setattr(runner, "SERVER", tmp_path)
    monkeypatch.setattr(runner.shutil, "disk_usage", lambda _: SimpleNamespace(free=10 * 1024**3))
    monkeypatch.setattr(runner, "cohorts", lambda _paths: ([t1_tiny_path], [t1_tiny_path]))
    monkeypatch.setattr(runner.subprocess, "check_output", lambda *a, **k: "/dev/mock\n")
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    traces, obs = data(task, noise_references={0})
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        if "--out-root" in command:
            output = Path(command[command.index("--out-root") + 1])
            write_jsonl(output / "tasks.jsonl", [task.to_dict()])
            write_jsonl(output / "traces.jsonl", traces)
            if "pair-pilot-worker" in command:
                write_json(output / "paired_measurement.json", {"passed": not paired_failure})
        elif "--out-dir" in command:
            output = Path(command[command.index("--out-dir") + 1])
            for name, rows in (("traces.jsonl", traces), ("tasks.jsonl", [task.to_dict()]),
                               ("observations.jsonl", obs), ("splits.jsonl", [])):
                write_jsonl(output / name, rows)
        return SimpleNamespace(stdout="", returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", run)
    out = tmp_path / "run"
    with pytest.raises(RuntimeError, match="paired measurement pilot failed" if paired_failure else "before feature collection"):
        runner.main(["--mode", "full", "--out-root", str(out), "--dataset", str(tmp_path), "--gpus", "2"])
    assert not any("collect" in command or "fit" in command or "intervene" in command for command in calls)
    assert read_json(out / "pipeline.json")["status"] == "failed"
    if paired_failure:
        assert read_json(out / "pipeline.json")["stage"] == "paired_pilot"
        assert not any(any("prepare_batched.py" in str(v) for v in command) for command in calls)
    else:
        assert read_json(out / "smoke/measurement_report.json")["overall"]["rho_coverage"] == pytest.approx(1 / 3)
    assert not any(str(out / "full/prepare-gpu2") in command for command in calls)


@pytest.mark.parametrize("mode,bad_full_controls", [("pilot", False), ("smoke", False), ("full", True)])
def test_runner_carries_c2_and_quality_and_rejects_failed_formal_controls(tmp_path, t1_tiny_path, monkeypatch, mode, bad_full_controls):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    runner = importlib.import_module("run_pr8")
    monkeypatch.setitem(__import__("sys").modules, "fcntl", SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *a: None))
    monkeypatch.setattr(runner, "SERVER", tmp_path)
    monkeypatch.setattr(runner.shutil, "disk_usage", lambda _: SimpleNamespace(free=10 * 1024**3))
    monkeypatch.setattr(runner, "cohorts", lambda _paths: ([t1_tiny_path], [t1_tiny_path]))
    monkeypatch.setattr(runner.subprocess, "check_output", lambda *a, **k: "/dev/mock\n")
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    traces, obs = data(task)
    obs.extend({"task_id": task.task_id, "premise_id": p.premise_id, "rng_pair": "stream:0",
                "reference_trace": "base0", "outcome": "structural"} for p in task.premises if p.premise_id not in {"unused_a", "unused_b"})
    from reasoning_diff.next_round import trajectory_table
    table = trajectory_table(traces, [task.to_dict()], obs, [])
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        if "--out-root" in command:
            output = Path(command[command.index("--out-root") + 1])
            write_jsonl(output / "tasks.jsonl", [task.to_dict()])
            write_jsonl(output / "traces.jsonl", traces)
            if "pair-pilot-worker" in command:
                write_json(output / "paired_measurement.json", {"passed": True})
        elif "--out-dir" in command:
            output = Path(command[command.index("--out-dir") + 1])
            output.mkdir(parents=True, exist_ok=True)
            if "fit" in command:
                write_jsonl(output / "probes.jsonl", [{"head": "behavior", "position": "pre_step", "U": [[1]],
                            "metrics": {role: {"status": "ok", "auc": .7} for role in ("probe_train", "dev")}}])
                write_jsonl(output / "p1_table.jsonl", table)
            elif "collect" in command:
                write_jsonl(output / "event_rows.jsonl", [{}])
            elif "intervene" in command:
                controls = [*conditions(), *conditions("same_value_diff_source")]
                if bad_full_controls and output.parent.name == "full":
                    controls[3]["invalid"] = 1
                write_jsonl(output / "interventions.jsonl", controls)
            elif "label" in command:
                write_jsonl(output / "labels.jsonl", [])
            elif "analyze" in command:
                source = Path(command[command.index("--in-dir") + 1])
                assert (source / "interventions.jsonl").exists()
                assert read_json(source / "measurement_report.json")["passed"]
            else:
                for name, rows in (("traces.jsonl", traces), ("tasks.jsonl", [task.to_dict()]),
                                   ("observations.jsonl", obs), ("splits.jsonl", [])):
                    write_jsonl(output / name, rows)
        return SimpleNamespace(stdout="", returncode=0)

    monkeypatch.setattr(runner.subprocess, "run", run)
    out = tmp_path / "run"
    args = ["--mode", mode, "--out-root", str(out), "--dataset", str(tmp_path), "--gpus", "2"]
    if mode == "pilot":
        assert runner.main(args) == 0
        assert read_json(out / "pipeline.json")["full_scan_started"] is False
        assert read_json(out / "paired_pilot.json")["passed"]
        assert sum("pilot-worker" in command for command in calls) == 1
        assert sum("pair-pilot-worker" in command for command in calls) == 1
        assert not any(any("prepare_batched.py" in str(v) for v in command) for command in calls)
        assert not any("collect" in command or "fit" in command or "intervene" in command for command in calls)
        return
    if bad_full_controls:
        with pytest.raises(RuntimeError, match="both source-pair kinds in full"):
            runner.main(args)
        assert read_json(out / "pipeline.json")["status"] == "failed"
        assert not read_json(out / "full/smoke_report.json")["passed"]
    else:
        assert runner.main(args) == 0
        assert read_json(out / "pipeline.json")["status"] == "complete"
    assert read_json(out / "smoke/smoke_report.json")["checks"]["causal_decode"]
    assert any("analyze" in command for command in calls)


def test_paired_pilot_reuses_base_generations_and_resumes(tmp_path, t1_tiny_path, monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    runner = importlib.import_module("run_pr8")
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    monkeypatch.setattr(runner.cli, "_load_tasks", lambda _args: [task])
    monkeypatch.setattr(runner.cli, "_load_frozen_runtime", lambda _args: {})
    from reasoning_diff.models import generate
    batching = importlib.import_module("trace_batching")
    class Decoder:
        def __init__(self, _batch_size):
            pass
        def __call__(self):
            return {"batch_execution": {"backend": "mock"}}
        def close(self):
            pass
    monkeypatch.setattr(batching, "BatchDecoder", Decoder)
    calls = []
    def generate_trace(owner, **kwargs):
        generate.decode_loop()
        calls.append((owner.task_id, kwargs["seed"]))
        trace = cli._synthetic_trace(owner, "q = 7", kwargs["run_id"], kwargs["seed"])
        trace.events = assign_event_regions(parse_events(trace.text, owner), trace.text, initial_thinking=True)
        trace.status, trace.correct = "natural_complete", True
        trace.metadata.update(boundary_status="ok", generated_tokens=100,
                              rendered_prompt_text="", rendered_prompt_char_len=0, enable_thinking=True)
        return trace
    monkeypatch.setattr(generate, "generate_task_trace", generate_trace)
    args = SimpleNamespace(dataset=t1_tiny_path, out_root=tmp_path, model="qwen3-8b", max_new=32768, batch_size=2, mode="pilot-worker")
    runner.pilot_worker(args)
    from reasoning_diff.io import file_digest
    original = file_digest(tmp_path / "traces.jsonl")
    args.mode = "pair-pilot-worker"
    runner.pilot_worker(args)
    report = read_json(tmp_path / "paired_measurement.json")
    assert len(calls) == 6
    assert report["passed"] and report["overall"]["n_traces"] == 1
    assert report["pilot_protocol"]["edit_seed"] == 0
    assert report["overall"]["eligible_cells"] == 2
    assert file_digest(tmp_path / "traces.jsonl") == original
    runner.pilot_worker(args)
    assert len(calls) == 6
    # The standalone CPU recovery entry point must reuse every request and
    # preserve the generation files, including failed measurements.
    raw = tmp_path / "raw"
    shard = raw / "pilot-gpu2"
    shard.mkdir(parents=True)
    for path in list(tmp_path.glob("*.json*")):
        path.rename(shard / path.name)
    write_json(raw / "protocol.json", {"gpus": [2], "trajectory_protocol": "natural",
                                      "smoke_inputs": {task.task_id + ".json": "fixture"}})
    before = {p.name: file_digest(p) for p in shard.iterdir()}
    reparse = importlib.import_module("reparse_pr8")
    output = tmp_path / "reparsed"
    report = reparse.remeasure_pilot(raw, output)
    assert report["passed"] and report["posthoc_reparse"]
    assert report["n_generated_traces"] == 6 and len(calls) == 6
    assert before == {p.name: file_digest(p) for p in shard.iterdir()}
    with pytest.raises(ValueError, match="new output directory"):
        reparse.remeasure_pilot(raw, output)
    paired_path = next(shard.glob("paired-*.json"))
    original_pair = read_json(paired_path)
    write_json(paired_path, {**original_pair, "seed": 2})
    with pytest.raises(ValueError, match="seed mismatch"):
        reparse.remeasure_pilot(raw, tmp_path / "wrong-seed")
    write_json(paired_path, {**original_pair, "text": original_pair["text"] + "tampered"})
    with pytest.raises(ValueError, match="saved generation table"):
        reparse.remeasure_pilot(raw, tmp_path / "wrong-text")
    write_json(paired_path, original_pair)
    protocol = read_json(raw / "protocol.json")
    protocol["smoke_inputs"]["missing-problem.json"] = "fixture"
    write_json(raw / "protocol.json", protocol)
    with pytest.raises(ValueError, match="registered pilot problems"):
        reparse.remeasure_pilot(raw, tmp_path / "missing-problem")
