"""Independent oracles for round-03 confirmed defects."""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from reasoning_diff.analysis import cone_fit, p1_incremental, p2_paired, p3_recovery, week8_decision
from reasoning_diff.baselines import fit_text_predictor, text_predictor
from reasoning_diff.cli import main
from reasoning_diff.edits import apply_operator_reverse, apply_rename_edit, apply_value_edit
from reasoning_diff.events import align_events, extract_answer
from reasoning_diff.executor import SubprocessExecutor, get_executor
from reasoning_diff.interventions import ie_z, rescue_controls, select_weak_layer
from reasoning_diff.io import read_json, read_jsonl, write_npz
from reasoning_diff.measure import dependency_densities
from reasoning_diff.probes.bilinear import BilinearProbe, weighted_bce
from reasoning_diff.probes.boundary import BoundaryMLP
from reasoning_diff.probes.calibrate import predict_set, sequence_score
from reasoning_diff.repair import repairability, run_repair
from reasoning_diff.schema import Event, EventIdentity, Task
from reasoning_diff.splits import assign_split, split_for_task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t1_official import load_igsm_snapshot
from reasoning_diff.tasks.t2_gsm_plus import load_gsm_plus
from reasoning_diff.tasks.t3_humaneval import apply_spec_edit, load_humaneval
from reasoning_diff.tasks.t3_musique import paragraph_edit
from reasoning_diff.transfer import apply_bilinear_inputs, fit_linear_map


def test_b14_plus_family_key_stays_test_even_when_hash_would_train():
    assert assign_split("gsm8k-1", source="gsm_plus") == "test"
    task = load_gsm_plus("tests/fixtures/t2_gsmplus_one.json")
    assert split_for_task(task) == "test"
    assert task.premises[0].kind == "placeholder"


def test_b24_integer_does_not_edit_trailing_decimal(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    data = task.to_dict()
    data["question"] = "p1 = 5.0. p2 = 0. What is q = p1 * p2?"
    data["premises"][0] = {"premise_id": "p1", "text": "p1 = 5.0", "start": 0, "end": 8, "value": "5", "kind": "fact"}
    data["premises"][1] = {"premise_id": "p2", "text": "p2 = 0", "start": 10, "end": 16, "value": "0", "kind": "fact"}
    with pytest.raises(ValueError):
        apply_value_edit(Task.from_dict(data), "p1", "9")


def test_c3_m01_event_mean_not_union():
    out = dependency_densities(
        event_sets=[
            {"premises": ["1", "2", "3"], "task_set": ["3"], "behavior_set": ["1", "3"]},
            {"premises": ["1", "2", "3"], "task_set": ["1", "2"], "behavior_set": ["1", "2"]},
        ]
    )
    assert out["rho_S_raw"] == pytest.approx(0.25)


def test_c3_m07_empty_noise_ignores_hits():
    out = dependency_densities(
        premises=["p1", "p2", "p3"],
        task_set=["p1"],
        behavior_set=["p2"],
        noise_set=[],
        sham_protocol={"name": "x", "hits": ["p3"]},
    )
    assert out["rho_S_noise"] is None
    assert out["null_reason"] == "noise_set_empty"


def test_p1_precomputed_is_scores_not_magic():
    length = np.array([1.0, 2.0, 3.0, 4.0])
    y = np.array([0.0, 0.0, 1.0, 1.0])
    out = p1_incremental(length, np.zeros(4), length, y, precomputed=True)
    assert out["estimator"] == "precomputed_scores"
    assert out["delta_auc"] == 0.0


def test_p1_held_out_logistic_detects_rho(monkeypatch):
    n = 40
    length = np.full(n, 10.0)
    op = np.random.default_rng(0).normal(scale=1000, size=n)
    y = np.array([0.0, 1.0] * 20)
    rho = y.copy()
    held = np.zeros(n, dtype=bool)
    held[20:] = True
    out = p1_incremental(length, op, rho, y, held_out=held)
    assert out["estimator"] == "held_out_logistic"
    assert out["auc_full"] == pytest.approx(1.0)
    assert out["delta_auc"] > 0


def test_p2_inconsistent_denom_is_null():
    out = p2_paired(0.2, 0.5, 0.8, 0.6, 99, shared_premises=["p1"])
    assert out["status"] == "denominator_inconsistent"
    assert out["delta_rho"] is None


def test_p3_reports_nontarget():
    out = p3_recovery(0.5, 0.4, 0.3, 0.1, nontarget=0.2, baseline_acc=0.45)
    assert out["nontarget"] == 0.2
    assert out["vs_baseline"] == pytest.approx(0.05)


def test_sequence_score_units_and_predict_set():
    assert sequence_score([0.7, 0.4], True, False) == pytest.approx(0.7)
    assert sequence_score([0.7, 0.4], True, False, nonconformity="one_minus_p") == pytest.approx(0.6)
    chosen = predict_set(np.array([0.7, 0.4]), 0.3)
    assert bool(chosen[0]) is True
    assert bool(chosen[1]) is False


def test_bilinear_score_and_fn_weight():
    probe = BilinearProbe(2, 2, rank=1)
    probe.U[:] = [[1.0], [0.0]]
    probe.V[:] = [[1.0], [0.0]]
    probe.b = 0.0
    h = np.array([1.0, 0.0])
    e = np.array([1.0, 0.0])
    assert probe.score(h, e) == pytest.approx(1 / (1 + math.exp(-1)))
    pred = np.array([0.8])
    pos = weighted_bce(pred, np.array([1.0]), np.array([1.0]), 10)
    assert pos == pytest.approx(10 * (-math.log(0.8)))


def test_boundary_mlp_trains():
    mlp = BoundaryMLP(4)
    x = np.array([[1.0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0]])
    y = np.array([1.0, 0.0, 1.0, 0.0])
    out = mlp.fit(x, y, steps=40)
    assert out["status"] == "ok"
    assert mlp.predict(x).shape == (4,)


def test_cone_fit_returns_r2():
    x = np.linspace(0, 1, 12)
    y = 1 - np.exp(-0.8 * (1 - x) ** 1.5)
    out = cone_fit(x, y)
    assert out["r2"] is not None
    assert out["r2"] > 0.9


def test_repairability_and_budget():
    assert repairability(4, 10) == pytest.approx(0.6)
    rec = run_repair("task_oracle", ["q"], [1, 2, 3], "new prefix tokens", generated_tokens=[9, 8], prefix_token_ids=[1, 2, 3])
    assert rec.generated_tokens == 2
    assert rec.extra_prefill_tokens == 3
    assert rec.original_token_budget == 3
    assert rec.record_id
    refused = run_repair("task_oracle", ["q"], [1, 2, 3], "new prefix tokens")
    assert refused.refilled_prefix is False
    assert refused.extra_prefill_tokens is None


def test_week8_blocks_already_decided():
    out = week8_decision({"status": "not_evaluated", "note": "already decided"})
    assert "already decided" in out["forbidden_claims_blocked"]
    assert out["skip_p2_p3"] is True


def test_align_equal_count_requires_same_node():
    a = Event(EventIdentity("q", 1), "1", 0, 1, 0, "q=1", node_id="q")
    b = Event(EventIdentity("q", 1), "9", 0, 1, 0, "r=9", node_id="r")
    aligned = align_events([a], [b])
    assert aligned["pairs"] == []
    assert aligned["structural"]["scanned"] is False


def test_extract_answer_ignores_open_think():
    assert extract_answer("<think>the number is 99", "numeric") is None
    assert extract_answer("<think>99</think> \\boxed{7}", "numeric") == "7"


def test_subprocess_executor_timeout_and_ok():
    exe = SubprocessExecutor()
    ok = exe.submit("x=1", "assert x==1", limits={"timeout": 2})
    assert ok.status == "ok"
    assert ok.tests_passed is True
    bad = exe.submit("import time\ntime.sleep(5)", "assert True", limits={"timeout": 0.2})
    assert bad.status == "timeout"
    assert get_executor(None).submit("1", "1").status == "executor_unavailable"


def test_ie_z_and_rescue_controls():
    assert ie_z(np.array([1.0, 1.0]), np.array([0.0, 0.0])) == pytest.approx(1.0)
    rng = np.random.default_rng(0)
    out = rescue_controls(np.zeros(2), np.array([1.0, 0.0]), np.array([0.0, 1.0]), rng)
    assert out["matched_norm"] == pytest.approx(1.0)
    assert select_weak_layer({0: 0.9, 3: 0.1}) == 3


def test_rename_keeps_expression(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    edit = apply_rename_edit(task, {"p1": "alpha"})
    assert "alpha = 4" in edit.task.question
    assert edit.task.nodes[0].expression == "alpha * p2"
    assert edit.task.premises[0].premise_id == "alpha"
    assert edit.task.record_id != task.record_id


def test_operator_reverse(t1_tiny_path):
    task = apply_value_edit(load_t1_fixture(t1_tiny_path), "p2", "2").task
    edit = apply_operator_reverse(task, "q")
    assert "/" in edit.task.nodes[0].expression
    assert edit.kind == "operator_reverse"


def test_spec_and_paragraph_need_truth():
    he = load_humaneval("tests/fixtures/t3_humaneval_one.json")
    spec = apply_spec_edit(he, "def f():\n    pass\n", "assert f() is None")
    assert spec.validity == "needs_truth"
    from reasoning_diff.tasks.t3_musique import load_musique_records

    musique = load_musique_records("tests/fixtures/t3_musique_pair.json")[0]
    para = paragraph_edit(musique, musique.premises[0].premise_id, "replacement only")
    assert para.validity == "needs_truth"


def test_igsm_mismatch_raises():
    import json
    from pathlib import Path

    src = Path("tests/fixtures/t1_official_shape.json")
    data = json.loads(src.read_text(encoding="utf-8"))
    data["answer"] = "99"
    bad = Path("tests/fixtures/t1_official_shape.json")
    # in-memory path via tmp
    import tempfile

    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "bad.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(ValueError, match="does not match template recompute"):
            load_igsm_snapshot(path)


def test_fit_hashes_labels_dir(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    lab = tmp_path / "lab"
    fit = tmp_path / "fit"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    assert main(["fit", "--in-dir", str(col), "--labels-dir", str(lab), "--out-dir", str(fit), "--split", "probe_train"]) == 0
    spec = read_json(fit / "run_spec.json")
    assert any("labels.jsonl" in key for key in spec["input_hashes"])
    probes = read_jsonl(fit / "probes.jsonl")
    assert probes[0]["head"] == "task"
    assert probes[1]["head"] == "behavior"
    assert "U" in probes[0]
    Trace = __import__("reasoning_diff.schema", fromlist=["Trace"]).Trace
    Trace.from_dict(read_jsonl(col / "traces.jsonl")[0])


def test_analyze_uses_p1_table(tmp_path):
    src = tmp_path / "lab"
    src.mkdir()
    from reasoning_diff.io import write_jsonl

    write_jsonl(
        src / "p1_table.jsonl",
        [
            {"length": 1, "op": 0, "rho": 0, "y": 0, "held_out": False},
            {"length": 2, "op": 0, "rho": 1, "y": 1, "held_out": False},
            {"length": 3, "op": 0, "rho": 0, "y": 0, "held_out": True},
            {"length": 4, "op": 0, "rho": 1, "y": 1, "held_out": True},
        ],
    )
    out = tmp_path / "an"
    assert main(["analyze", "--in-dir", str(src), "--out-dir", str(out)]) == 0
    report = read_json(out / "report.json")
    assert report["p1"] is not None
    assert report["scientific_conclusion"] is None


def test_text_predictor_requires_fit():
    with pytest.raises(ValueError):
        text_predictor("prefix", "p1")
    weights = fit_text_predictor(["a uses p1", "b hides"], np.array([1.0, 0.0]))
    assert 0.0 <= text_predictor("a uses p1", "p1", weights) <= 1.0


def test_labeled_transfer_needs_labels():
    src = np.eye(2)
    tgt = np.array([[2.0, 0.0], [0.0, 3.0]])
    with pytest.raises(ValueError):
        fit_linear_map(src, tgt, "transfer_pairs", labeled=True)
    fitted = fit_linear_map(src, tgt, "transfer_pairs", labeled=True, labels=np.array([0.0, 1.0]))
    mapped_h, mapped_e = apply_bilinear_inputs(tgt, tgt, fitted, fitted)
    assert mapped_h.shape == src.shape
