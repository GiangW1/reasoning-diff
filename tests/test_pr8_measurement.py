"""Measurement regressions: these are contracts, not evidence for the claim."""
import pytest

from reasoning_diff.events import assign_event_regions, parse_events
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def test_truncated_thinking_keeps_reasoning_events(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    events = parse_events("q = 3 + 4 = 7", task)
    assign_event_regions(events, "q = 3 + 4 = 7", initial_thinking=True)
    assert events and all(e.event_region == "thinking" for e in events)


def test_equation_chain_commits_final_value(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    event = parse_events("q = 0 + 22 = 22", task)[0]
    assert event.value == "22"
    assert event.text == "q = 0 + 22 = 22"
    assert event.event_kind == "calculation"
    assert parse_events("q = 0 + 22", task) == []
    assert parse_events("q = (0 + 22) = 22", task)[0].value == "22"
    assert parse_events("q = 0 + 22 = 22. p1 = 4.", task)[0].value == "22"


def test_dev_selection_is_not_last_layer():
    from reasoning_diff.next_round import select_dev_layer
    assert select_dev_layer([0, 12, 24, 35], [0.6, 0.82, 0.7, 0.49]) == 12
    assert select_dev_layer([0, 12], [None, 0.7]) == 12
    with pytest.raises(ValueError, match="dev"):
        select_dev_layer([0, 12], [None, None])


def test_trajectory_p1_retains_missing_rho_without_zero_sentinel(t1_tiny_path):
    from reasoning_diff.next_round import trajectory_table
    task = load_t1_fixture(t1_tiny_path)
    trace = {"id": "b", "task_id": task.task_id, "base_group_id": task.base_group_id,
             "status": "natural_truncated", "correct": True, "events": [],
             "metadata": {"generated_tokens": 4096}, "seed": 0}
    rows = trajectory_table([trace], [task.to_dict()], [], [])
    assert len(rows) == 1
    assert rows[0]["rho"] is None
    assert rows[0]["y"] == 0
    assert rows[0]["length"] == 4096
    assert rows[0]["analysis_unit"] == "trajectory"


def test_sentence_graph_edits_every_fact_with_recomputed_truth(t1_tiny_path):
    from reasoning_diff.next_round import sentence_graph_task, scan_edits
    from reasoning_diff.graphs import ancestors
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    assert task.source_kind == "project_derived"
    assert len(task.premises) > 3
    assert "relation_q" in ancestors(task)["q"]
    edits = scan_edits(task, 3)
    assert {e.changed_premise_ids[0] for e in edits} == {p.premise_id for p in task.premises}
    for edit in edits:
        edit.task.validate()
        assert edit.task.question != task.question
        assert edit.task.metadata["premise_protocol"] == "sentence_graph_v1"


def test_smoke_rejects_missing_events_and_budget_truncation(t1_tiny_path):
    from reasoning_diff.next_round import smoke_report
    task = load_t1_fixture(t1_tiny_path)
    traces = [{"id": "b", "task_id": task.task_id, "base_group_id": task.base_group_id,
               "status": "natural_truncated", "events": [], "metadata": {}}]
    report = smoke_report(traces, [task.to_dict()], [], [], [])
    assert not report["passed"]
    assert "completion_rate" in report["failures"]
    assert "thinking_calculation_events" in report["failures"]


def test_p1_keeps_failed_trace_when_other_traces_have_observations(t1_tiny_path):
    from reasoning_diff.next_round import trajectory_table
    task = load_t1_fixture(t1_tiny_path)
    traces = [{"id": name, "task_id": task.task_id, "status": "natural_truncated",
               "events": [], "metadata": {"generated_tokens": 4096}}
              for name in ("base0", "base1")]
    observations = [{"reference_trace": "base0", "alignment_ref": "q", "outcome": "unaligned"}]
    rows = trajectory_table(traces, [task.to_dict()], observations, [])
    assert {r["trace_id"] for r in rows} == {"base0", "base1"}
    assert all(r["rho"] is None and r["y"] == 0 for r in rows)


def test_smoke_uses_probe_metrics_without_baseline_overwrite():
    from reasoning_diff.next_round import smoke_report
    good = {role: {"status": "ok"} for role in ("probe_train", "dev")}
    probe = {"head": "behavior", "position": "pre_step", "U": [[1]], "metrics": good}
    baseline = {"head": "behavior", "position": "pre_step", "baseline": "text_predictor", "metrics": {}}
    report = smoke_report([], [], [], [], [probe, baseline])
    assert report["checks"]["behavior_train_and_dev"]
    report = smoke_report([], [], [], [], [{**probe, "metrics": {}}, {**baseline, "metrics": good}])
    assert not report["checks"]["behavior_train_and_dev"]


def test_offsets_keep_special_tokens_and_split_unicode():
    from reasoning_diff.models.tokenize import offsets_from_tokenizer
    # U+00E9 has two bytes; these GPT byte tokens must overlap its char span.
    class Tok:
        all_special_ids = [1]
        def convert_ids_to_tokens(self, tid):
            return {1: "<think>", 2: "Ã", 3: "©", 4: "x"}[tid]
    offsets, failures = offsets_from_tokenizer(Tok(), [1, 2, 3, 4], "<think>éx", True)
    assert not failures
    assert offsets == [[0, 7], [7, 8], [7, 8], [8, 9]]


def test_offset_failure_never_fabricates_a_cursor():
    from reasoning_diff.models.tokenize import offsets_from_tokenizer
    class Tok:
        def decode(self, ids, **kwargs):
            return "a"
    offsets, failures = offsets_from_tokenizer(Tok(), [1, 2], "ab", True)
    assert failures and offsets == [[0, 0], [0, 0]]


def test_rule_premises_do_not_hide_node_aliases(t1_tiny_path):
    from reasoning_diff.next_round import sentence_graph_task
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    assert parse_events("The number of q equals 7.", task)[0].node_id == "q"


def test_behavior_labels_do_not_pool_different_seeds(t1_tiny_path):
    from reasoning_diff.next_round import trace_labels
    from reasoning_diff.schema import Observation
    task = load_t1_fixture(t1_tiny_path)
    observations = []
    for seed, outcome in enumerate(("changed", "no_change")):
        observations.append(Observation(str(seed), f"base{seed}", f"edit{seed}", "edit", "p1", ["q", "q"],
                                        outcome, ["0", "1"], "q", task_id=task.task_id, node_id="q"))
    labels = trace_labels(observations, [task])
    assert [(l.trace_id, l.behavior_label) for l in labels] == [("base0", 1), ("base1", 0)]
    assert len({l.record_id for l in labels}) == 2


def test_p1_excess_uses_matched_support_and_keeps_negative_excess(t1_tiny_path):
    from reasoning_diff.next_round import sentence_graph_task, trajectory_table
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    event = parse_events("q = 7", task)[0]
    event.event_region = "thinking"
    trace = {"id": "base", "task_id": task.task_id, "status": "natural_complete", "correct": True,
             "seed": 0, "events": [event.to_dict()], "metadata": {"generated_tokens": 100}}
    obs = [{"reference_trace": "base", "alignment_ref": event.identity.key(), "premise_id": "unused_a",
            "outcome": "no_change", "rng_pair": "stream:0"},
           {"reference_trace": "base", "alignment_ref": event.identity.key(), "premise_id": "unused_b",
            "outcome": "unaligned", "rng_pair": "stream:0"},
           {"reference_trace": "base", "alignment_ref": event.identity.key(), "premise_id": "sham:q",
            "outcome": "changed", "rng_pair": "sham:1"}]
    row = trajectory_table([trace], [task.to_dict()], obs, [{"base_group_id": task.base_group_id, "role": "test"}])[0]
    assert row["support_cells"] == 1
    assert row["eligible_cells"] == 2
    assert row["coverage"] == 0.5
    assert row["rho_raw"] == 0 and row["rho"] == -1
    assert row["y"] == 1 and row["held_out"]


def test_natural_source_pair_changes_downstream_sentence(t1_tiny_path):
    from reasoning_diff.edits import make_source_value_pair, recompute
    from reasoning_diff.next_round import sentence_graph_task
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    pair = make_source_value_pair(task, "p1", "2")
    source = pair["same_value_diff_source"].task
    rule = next(p for p in source.premises if p.premise_id == "relation_q")
    assert "alternate reserve quantity" in rule.text
    assert "src_b" in rule.value
    assert recompute(source).answer_spec.value == task.answer_spec.value
    source.validate()


def test_donor_matches_full_occurrence_identity():
    import numpy as np
    from reasoning_diff.cli import _pair_source_value
    rows = [{"node_id": "q", "identity_key": "q:1", "trace_id": "base"},
            {"node_id": "q", "identity_key": "q:2", "trace_id": "donor"}]
    pair = {"trace_ids": {"base": "base", "same_value_diff_source": "donor"}}
    assert _pair_source_value(np.array([[0., 0.], [1., 1.]]), rows, pair) is None


def test_all_task_scan_batch_plan_and_base_pair_noise(tmp_path, t1_tiny_path, monkeypatch):
    import importlib
    from pathlib import Path
    from reasoning_diff import cli
    from reasoning_diff.models import generate
    from reasoning_diff.next_round import sentence_graph_task
    from reasoning_diff.schema import Task
    from reasoning_diff.io import read_jsonl
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    runner = importlib.import_module("prepare_batched")
    original = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    second = Task.from_dict({**original.to_dict(), "task_id": "second", "base_group_id": "second"})
    monkeypatch.setattr(cli, "_load_tasks", lambda _args: [original, second])
    argv = ["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(tmp_path / "prepare"), "--eval-mode", "scientific",
            "--premise-protocol", "sentence_graph", "--noise-reference", "base_pairs", "--behavior-repeats", "3",
            "--split-fractions", "0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]
    planned = [runner.request_key(t, seed, run) for t, seed, run in runner.prepare_requests(cli.build_parser().parse_args(argv))]
    actual = []
    def record(task, **kwargs):
        actual.append(runner.request_key(task, kwargs["seed"], kwargs["run_id"]))
        return cli._synthetic_trace(task, cli._trace_text(task), kwargs["run_id"], kwargs["seed"])
    monkeypatch.setattr(generate, "generate_task_trace", record)
    assert cli.main(argv) == 0
    assert actual == planned
    traces = read_jsonl(tmp_path / "prepare/traces.jsonl")
    assert not any("sham" in t["id"] for t in traces)
    observations = read_jsonl(tmp_path / "prepare/observations.jsonl")
    for task in (original, second):
        scanned = {o["premise_id"] for o in observations if o["task_id"] == task.task_id and not o["rng_pair"].startswith("sham:")}
        assert scanned == {p.premise_id for p in task.premises}
    noise = [o for o in observations if o["rng_pair"].startswith("sham:")]
    assert noise and all(o["reference_trace"] != o["comparison_trace"] for o in noise)


def test_all_pairs_continues_after_missing_first_donor(tmp_path, monkeypatch):
    from reasoning_diff import cli
    from reasoning_diff.io import write_jsonl, read_jsonl
    features = tmp_path / "features"
    features.mkdir()
    write_jsonl(features / "edits.jsonl", [{"kind": "source_value_pair", "base_task_id": f"t{i}",
               "trace_ids": {"base": f"b{i}", "same_value_diff_source": f"s{i}", "same_source_diff_value": f"v{i}"}} for i in range(2)])
    write_jsonl(features / "splits.jsonl", [{"task_id": f"t{i}", "base_group_id": f"t{i}", "role": "test"} for i in range(2)])
    seen = []
    def intervene(args):
        pair = args._source_pair
        seen.append(pair)
        status = "donor_missing" if pair["base_task_id"] == "t0" else "prospective_decode"
        write_jsonl(__import__("pathlib").Path(args.out_dir) / "interventions.jsonl", [{"condition": "main", "status": status}])
        return 0
    monkeypatch.setattr(cli, "_cmd_intervene_impl", intervene)
    assert cli.main(["intervene", "--in-dir", str(features), "--out-dir", str(tmp_path / "out"), "--backend", "offline", "--all-source-pairs"]) == 0
    assert len(seen) == 4
    rows = read_jsonl(tmp_path / "out/interventions.jsonl")
    assert sum(r["analysis_eligibility"]["C2"] for r in rows) == 2
    assert all(not r["analysis_eligibility"]["P3"] for r in rows)


def test_calibration_uses_each_positions_features(tmp_path, t1_tiny_path):
    import numpy as np
    from reasoning_diff import cli
    from reasoning_diff.io import write_jsonl, write_npz, read_jsonl
    from reasoning_diff.probes.bilinear import BilinearProbe
    task = load_t1_fixture(t1_tiny_path)
    src = tmp_path / "in"
    src.mkdir()
    write_jsonl(src / "tasks.jsonl", [task.to_dict()])
    write_jsonl(src / "splits.jsonl", [{"task_id": task.task_id, "base_group_id": task.base_group_id, "role": "calibration"}])
    write_jsonl(src / "event_rows.jsonl", [{"task_id": task.task_id, "base_group_id": task.base_group_id, "trace_id": "base0", "node_id": "q", "identity_key": "q"}])
    write_jsonl(src / "premise_rows.jsonl", [{"premise_id": "p1", "premise_key": f"{task.task_id}::p1"}])
    write_jsonl(src / "labels.jsonl", [{"task_id": task.task_id, "trace_id": "base0", "event_id": "q", "premise_id": "p1", "task_label": 1}])
    probe = BilinearProbe(1, 1, rank=1)
    probe.U[:] = probe.V[:] = 1
    row = {"dim_h": 1, "dim_e": 1, "rank": 1, "U": [[1]], "V": [[1]], "b": 0, "head": "task"}
    write_jsonl(src / "probes.jsonl", [{**row, "position": p} for p in ("pre_step", "pre_value", "post_step")])
    write_npz(src / "features.npz", {"H": np.array([[0.]]), "H_pre_value": np.array([[2.]]), "H_post_step": np.array([[-2.]]), "E": np.array([[1.]])})
    assert cli.main(["calibrate", "--in-dir", str(src), "--out-dir", str(tmp_path / "out"), "--eval-mode", "scientific"]) == 0
    rows = read_jsonl(tmp_path / "out/calibration.jsonl")
    scores = {r["position"]: r["scores"][0] for r in rows}
    assert scores["pre_value"] < scores["pre_step"] < scores["post_step"]


def test_failed_length_pilot_never_launches_formal_generation(tmp_path, t1_tiny_path, monkeypatch):
    import importlib
    from pathlib import Path
    from types import SimpleNamespace
    from reasoning_diff.io import write_jsonl, read_json
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    runner = importlib.import_module("run_pr8")
    monkeypatch.setitem(__import__("sys").modules, "fcntl", SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *args: None))
    monkeypatch.setattr(runner, "SERVER", tmp_path)
    monkeypatch.setattr(runner, "cohorts", lambda _paths: ([t1_tiny_path], [t1_tiny_path]))
    monkeypatch.setattr(runner.subprocess, "check_output", lambda *a, **k: "/dev/mock\n")
    calls = []
    def run(command, **kwargs):
        calls.append(command)
        if "pilot-worker" in command:
            output = Path(command[command.index("--out-root") + 1])
            write_jsonl(output / "traces.jsonl", [{"status": "natural_truncated", "events": [], "metadata": {"generated_tokens": 4096, "boundary_status": "ok"}}])
        return SimpleNamespace(stdout="")
    monkeypatch.setattr(runner.subprocess, "run", run)
    out = tmp_path / "output"
    with pytest.raises(RuntimeError, match="pilot failed"):
        runner.main(["--mode", "full", "--out-root", str(out), "--dataset", str(tmp_path), "--gpus", "2"])
    assert not read_json(out / "length_pilot.json")["passed"]
    assert not any(any("prepare_batched.py" in str(v) for v in c) for c in calls)


@pytest.mark.parametrize("op", [5, 10, 15, 21])
def test_exported_official_strata_convert_to_consistent_sentence_facts(op):
    from pathlib import Path
    from reasoning_diff.tasks.t1_official import load_igsm_snapshot
    from reasoning_diff.next_round import sentence_graph_task, scan_edits
    from reasoning_diff.edits import recompute, make_source_value_pair
    from reasoning_diff.cli import _default_edit
    root = Path(__file__).resolve().parents[1] / "artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200"
    original = load_igsm_snapshot(sorted(root.glob(f"*-op{op}.json"))[0])
    task = sentence_graph_task(original)
    assert task.answer_spec.value == original.answer_spec.value
    assert len(task.premises) == len(original.premises) + len(original.nodes) + 2
    for edit in scan_edits(task, 3):
        edit.task.validate()
        assert recompute(edit.task).answer_spec.value == edit.task.answer_spec.value
    pid, value = _default_edit(task)
    source = make_source_value_pair(task, pid, value)["same_value_diff_source"].task
    source.validate()
    assert source.answer_spec.value == task.answer_spec.value
    assert "alternate reserve quantity" in source.question


def test_auc_with_ties_matches_pairwise_definition_and_scales():
    import numpy as np
    from reasoning_diff.analysis import _auc
    scores = np.array([0.1, 0.1, 0.5, 0.9, 0.9, 1.])
    y = np.array([0, 1, 1, 1, 0, 0])
    pos, neg = scores[y == 1], scores[y == 0]
    expected = np.mean(pos[:, None] > neg) + 0.5 * np.mean(pos[:, None] == neg)
    assert _auc(scores, y) == pytest.approx(expected)
    assert _auc(np.tile(scores, 10000), np.tile(y, 10000)) == pytest.approx(expected)
