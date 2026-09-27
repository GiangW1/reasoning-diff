"""Independent counterexamples from the 2026-09-21 acceptance review."""
from __future__ import annotations

import json

import numpy as np
import pytest

from reasoning_diff.analysis import p1_incremental, p2_from_rows, p3_from_rows
from reasoning_diff.cli import _observations, main
from reasoning_diff.edits import apply_operator_reverse, apply_rename_edit, apply_value_edit
from reasoning_diff.events import extract_answer, parse_events
from reasoning_diff.executor import IsolatedBwrapExecutor, get_executor
from reasoning_diff.io import read_json, read_jsonl
from reasoning_diff.measure import build_labels, dependency_densities, event_density_sets
from reasoning_diff.repair import execute_repair_tiny, run_repair
from reasoning_diff.schema import Observation, Task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t2_gsm_symbolic import load_gsm_symbolic
from reasoning_diff.tasks.t2_noop import make_noop_pair
from reasoning_diff.tasks.t3_hotpot import document_edit, load_hotpot
from reasoning_diff.transfer import apply_map, fit_linear_map
from reasoning_diff.baselines import fit_text_predictor, text_predictor


def test_e02_failed_manifest_is_not_resume_success(tmp_path, t1_tiny_path):
    missing = tmp_path / "missing"
    missing.mkdir()
    fit = tmp_path / "fit"
    with pytest.raises(FileNotFoundError):
        main(["fit", "--in-dir", str(missing), "--out-dir", str(fit), "--split", "probe_train"])
    assert (fit / "manifest.json").exists()
    body = read_json(fit / "manifest.json")
    assert body["success_count"] == 0
    with pytest.raises(FileNotFoundError):
        main(["fit", "--in-dir", str(missing), "--out-dir", str(fit), "--split", "probe_train", "--resume"])


def test_e03_resume_rejects_split_seed_change(tmp_path, t1_tiny_path):
    out = tmp_path / "prep"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(out), "--split-seed", "8"]) == 0
    with pytest.raises(ValueError, match="split_seed"):
        main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(out), "--split-seed", "0", "--resume"])


def test_e01_scientific_fit_refuses_test_family(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--split-seed", "8"]) == 0
    roles = {row["role"] for row in read_jsonl(prep / "splits.jsonl")}
    if roles != {"test"}:
        pytest.skip("seed 8 did not land on test for this fixture")
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    with pytest.raises(ValueError, match="test-family"):
        main(["fit", "--in-dir", str(col), "--labels-dir", str(prep), "--out-dir", str(tmp_path / "fit"), "--split", "probe_train", "--eval-mode", "scientific"])


def test_r14_collect_keeps_actual_token_ids(tmp_path, t1_tiny_path):
    from reasoning_diff.models.tokenize import encode_text

    prep = tmp_path / "prep"
    col = tmp_path / "col"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", "0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]) == 0
    trace = read_jsonl(prep / "traces.jsonl")[0]
    recoded, _ = encode_text(trace["text"])
    assert recoded != trace["token_ids"]
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "tiny", "--eval-mode", "scientific"]) == 0
    used = read_jsonl(col / "traces.jsonl")[0]["token_ids"]
    assert used == trace["token_ids"]


def test_cr_s02_f1_is_identity_not_row_order(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    from reasoning_diff.io import write_jsonl, write_npz

    write_npz(src / "features.npz", {"H": np.ones((1, 1)), "E": np.array([[1.0], [0.0]])})
    write_jsonl(
        src / "probes.jsonl",
        [{"head": "task", "U": [[1.0]], "V": [[1.0]], "b": 0.0, "dim_h": 1, "dim_e": 1, "rank": 1}],
    )
    write_jsonl(
        src / "labels.jsonl",
        [
            {"event_id": "q", "premise_id": "p1", "task_label": 1, "behavior_label": 1},
            {"event_id": "q", "premise_id": "p2", "task_label": 0, "behavior_label": 0},
        ],
    )
    write_jsonl(src / "event_rows.jsonl", [{"trace_id": "t", "node_id": "q", "identity_key": "q", "event_id": "q"}])
    write_jsonl(
        src / "tasks.jsonl",
        [load_t1_fixture("tests/fixtures/t1_tiny.json").to_dict()],
    )
    out_a = tmp_path / "a"
    assert main(["analyze", "--in-dir", str(src), "--out-dir", str(out_a)]) == 0
    f1_a = read_json(out_a / "report.json")["appendix"]["probe_prf1"]["f1"]
    write_jsonl(
        src / "labels.jsonl",
        [
            {"event_id": "q", "premise_id": "p2", "task_label": 0, "behavior_label": 0},
            {"event_id": "q", "premise_id": "p1", "task_label": 1, "behavior_label": 1},
        ],
    )
    out_b = tmp_path / "b"
    assert main(["analyze", "--in-dir", str(src), "--out-dir", str(out_b)]) == 0
    f1_b = read_json(out_b / "report.json")["appendix"]["probe_prf1"]["f1"]
    assert f1_a == f1_b


def test_cr_s03_p2_p3_use_all_rows():
    p2 = p2_from_rows(
        [
            {"base_rho": 0, "noop_rho": 1, "base_acc": 1, "noop_acc": 0, "shared_premises": ["p1"], "shared_denom": 1},
            {"base_rho": 1, "noop_rho": 0, "base_acc": 0, "noop_acc": 1, "shared_premises": ["p1"], "shared_denom": 1},
        ]
    )
    assert p2["delta_rho"] == pytest.approx(0.0)
    p3 = p3_from_rows(
        [
            {"main_acc": 1, "crand_acc": 0, "clayer_acc": 0, "invalid_rate": 0},
            {"main_acc": 0, "crand_acc": 1, "clayer_acc": 1, "invalid_rate": 0},
        ]
    )
    assert p3["vs_crand"] == pytest.approx(0.0)


def test_cr_s04_p1_rejects_overlapping_groups():
    n = 12
    y = np.array([0, 1] * 6, dtype=float)
    rho = y.copy()
    held = np.array([False] * 6 + [True] * 6)
    groups = [str(i % 6) for i in range(n)]
    with pytest.raises(ValueError, match="overlap"):
        p1_incremental(np.ones(n), np.ones(n), rho, y, held_out=held, groups=groups, rng=np.random.default_rng(0))


def test_cr_s05_transfer_applies_means():
    target = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    source = target + np.array([10.0, -5.0])
    fitted = fit_linear_map(source, target, "transfer_pairs", labeled=False)
    mapped = apply_map(target, fitted)
    assert np.allclose(mapped, source)


def test_cr_s06_supervised_map_uses_labels():
    target = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    source = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    a = fit_linear_map(source, target, "transfer_pairs", labeled=True, labels=np.array([0, 0, 1, 1]))
    b = fit_linear_map(source, target, "transfer_pairs", labeled=True, labels=np.array([0, 1, 0, 1]))
    assert not np.allclose(a["W"], b["W"])


def test_cr_s10_text_predictor_fits_train_points():
    fitted = fit_text_predictor(["alpha", "beta"], np.array([0.0, 1.0]), premises=["", ""])
    assert text_predictor("alpha", "", fitted) < 0.5
    assert text_predictor("beta", "", fitted) > 0.5


def test_cr_s12_analyze_writes_procrustes_json(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    from reasoning_diff.io import write_jsonl

    write_jsonl(src / "geom_a.jsonl", [{"rows": [[1, 0], [0, 1]]}])
    write_jsonl(src / "geom_b.jsonl", [{"rows": [[1, 0], [0, 1]]}])
    out = tmp_path / "an"
    assert main(["analyze", "--in-dir", str(src), "--out-dir", str(out)]) == 0
    report = read_json(out / "report.json")
    assert report["appendix"]["procrustes"]["status"] == "adapted_geometry"


def test_dm05_nan_noise_is_null():
    result = dependency_densities(task=np.array([[0, 1]]), behavior=np.array([[1, 0]]), noise=np.array([[np.nan, np.nan]]))
    assert result["rho_S_noise"] is None
    assert result["rho_S_excess"] is None


def test_dm04_unknown_graph_is_null(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    data = task.to_dict()
    data["graph_status"] = "unknown"
    data["graph_kind"] = "none"
    data["nodes"] = []
    data["target"] = None
    unknown = Task.from_dict(data)
    labels = build_labels(
        [Observation("o", "a", "b", "e", "p1", ["q", "q"], "changed", ["1", "2"], "q", node_id="q")],
        {},
    )
    dens = event_density_sets(unknown, labels)
    assert dens["rho_S_raw"] is None
    assert dens["null_reason"] == "task_graph_unknown"


def test_dm06_gsm_gold_extracts_terminal(tmp_path):
    path = tmp_path / "rec.json"
    path.write_text(
        json.dumps({"id": 0, "instance": 1, "question": "q", "answer": "Calculate 4+3=7.\\n#### 7"}),
        encoding="utf-8",
    )
    task = load_gsm_symbolic(path)
    assert task.answer_spec.value == "7"
    assert task.task_id == "0:1"
    assert extract_answer("The answer is Paris.", "span") == "paris"


def test_dm09_operator_reverse_rewrites_question(t1_tiny_path):
    task = apply_value_edit(load_t1_fixture(t1_tiny_path), "p2", "2").task
    edited = apply_operator_reverse(task, "q")
    assert edited.task.question != task.question
    assert edited.changed_premise_ids


def test_dm14_rename_maps_target(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    edited = apply_rename_edit(task, {"q": "z"})
    assert edited.task.target == "z"


def test_dm13_noop_mid_keeps_original_words(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    pair = make_noop_pair(task, "A shop has 9 chairs.", "mid", "low", True)
    assert "What is q" in pair.question
    assert "Wh A shop" not in pair.question


def test_dm15_hotpot_document_replace_is_one_document():
    task = load_hotpot("tests/fixtures/t3_hotpot_one.json")
    out = document_edit(task, "DocA", "New document")
    docs = [p for p in out["task"].premises if p.document_id == "DocA"]
    assert len(docs) == 1
    assert docs[0].text == "New document"


def test_dm11_premise_event_is_not_independent(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    events = parse_events("p1 = 4\nq = 8", task)
    premise = next(e for e in events if e.node_id == "p1")
    assert premise.task_parents == ["p1"]


def test_mc09_full_recompute_keeps_question():
    out = execute_repair_tiny("full_recompute", ["q"], [1], "p1 = 2; q = 3", max_new=0)
    assert out["prefix_token_ids"] != [1]
    assert out["prefix_token_ids"]


def test_mc10_run_repair_accepts_token_count():
    rec = run_repair("task_oracle", ["q"], [1], "abc", execute=lambda *a: {"generated_tokens": 3, "prefill_hidden": [1.0, 2.0]})
    assert rec.generated_tokens == 3


def test_e04_isolated_backend_is_callable():
    exe = get_executor("isolated")
    assert isinstance(exe, IsolatedBwrapExecutor)
    result = exe.submit("x=1", "assert x==1")
    assert result.status in {"ok", "failed", "executor_unavailable", "timeout"}


def test_e05_models_package_is_not_gitignored():
    from subprocess import run

    proc = run(["git", "check-ignore", "-v", "--", "src/reasoning_diff/models/adapters.py"], capture_output=True, text=True)
    assert proc.returncode == 1


def test_dm01_repeated_events_keep_separate_keys():
    from reasoning_diff.schema import Event, EventIdentity, Trace

    task = load_t1_fixture("tests/fixtures/t1_tiny.json")
    left = [
        Event(EventIdentity("q", 1), "8", 0, 1, 0, "q=8", ["p1", "p2"], node_id="q", graph_status="complete"),
        Event(EventIdentity("q", 2), "8", 2, 3, 2, "q=8", ["p1", "p2"], node_id="q", graph_status="complete"),
    ]
    right = [
        Event(EventIdentity("q", 1), "9", 0, 1, 0, "q=9", ["p1", "p2"], node_id="q", graph_status="complete"),
        Event(EventIdentity("q", 2), "8", 2, 3, 2, "q=8", ["p1", "p2"], node_id="q", graph_status="complete"),
    ]
    base = Trace("b", task.task_id, task.base_group_id, "tiny", 0, "q=8\nq=8", [1], [[0, 1]], left, "8", True)
    edit_tr = Trace("e", task.task_id, task.base_group_id, "tiny", 0, "q=9\nq=8", [1], [[0, 1]], right, "9", True)
    edit = apply_value_edit(task, "p2", "2")
    rows = _observations(task, base, edit_tr, edit, "stream:0", "r")
    labels = build_labels(rows, {"q": {"p1", "p2"}})
    keys = [(lab.event_id, lab.behavior_label) for lab in labels if lab.premise_id == "p2"]
    assert len(keys) == 2
    assert {lab.behavior_label for lab in labels if lab.premise_id == "p2"} == {0, 1}
