"""CE-level regressions for round-05 A/F confirmed defects."""
from __future__ import annotations

import numpy as np
import pytest

from reasoning_diff.analysis import p1_incremental, retrieval_scatter, week8_decision
from reasoning_diff.baselines import verbalizer
from reasoning_diff.cli import main
from reasoning_diff.events import parse_events
from reasoning_diff.io import read_json, read_jsonl, read_npz
from reasoning_diff.models.tokenize import readout_layer_index, span_token_indices
from reasoning_diff.repair import mask_prefix, run_repair
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t2_gsm_plus import apply_plus_numeric_edit, load_gsm_plus
from reasoning_diff.tasks.t3_hotpot import document_edit, load_hotpot
from reasoning_diff.transfer import common_dim_then_procrustes


FRAC = ["0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]


def test_scientific_prepare_emits_parseable_events(tmp_path, t1_tiny_path):
    out = tmp_path / "prep"
    assert (
        main(
            [
                "prepare",
                "--fixture",
                str(t1_tiny_path),
                "--out-dir",
                str(out),
                "--eval-mode",
                "scientific",
                "--split-fractions",
                *FRAC,
                "--sham-opportunities",
                "1",
            ]
        )
        == 0
    )
    traces = read_jsonl(out / "traces.jsonl")
    assert traces
    assert all(len(row["events"]) >= 1 for row in traces)
    assert any(ev.get("node_id") == "q" for row in traces for ev in row["events"])
    assert "p1 = 4 | p2 = 0 | q = 0" not in traces[0]["text"]
    obs = read_jsonl(out / "observations.jsonl")
    sham = [row for row in obs if (row.get("rng_pair") or "").startswith("sham:")]
    assert sham
    assert all(str(row.get("premise_id") or "").startswith("sham:") for row in sham)
    edits = read_jsonl(out / "edits.jsonl")
    assert any(row.get("kind") == "source_value_pair" for row in edits)


def test_scientific_collect_h_is_step_boundary_not_last_token(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *FRAC]) == 0
    traces = read_jsonl(prep / "traces.jsonl")
    n_events = sum(len(row["events"]) for row in traces)
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--eval-mode", "scientific", "--backend", "tiny"]) == 0
    arrays = read_npz(col / "features.npz")
    assert arrays["H"].shape[0] <= n_events
    assert arrays["H"].shape[0] == arrays["H_pre_step"].shape[0]
    assert arrays["H"].shape[0] > 1
    assert np.isfinite(arrays["H"]).all()


def test_span_no_straddle_fallback():
    assert span_token_indices([[0, 2], [2, 6], [6, 8]], 2, 6) == [1]
    assert span_token_indices([[0, 2], [2, 6]], 1, 3) == []


def test_readout_rejects_empty_band():
    with pytest.raises(ValueError, match="60-75"):
        readout_layer_index(2)
    assert readout_layer_index(3) == 1


def test_verbalizer_uses_extracted_answer_not_substring():
    assert verbalizer("zeroshot", "p", "7", False, generate_fn=lambda p: "answer 7")["score"] == 1.0
    assert verbalizer("zeroshot", "p", "7", False, generate_fn=lambda p: "17")["score"] == 0.0
    assert verbalizer("zeroshot", "p", "7", False, generate_fn=lambda p: "answer 70")["score"] == 0.0
    assert verbalizer("zeroshot", "p", "7", False, generate_fn=lambda p: r"\boxed{8} also 7")["score"] == 0.0


def test_dummy_execute_is_not_prefill():
    rec = run_repair("task_oracle", ["q"], [1, 2, 3], "hello world tokens", execute=lambda *a: {"generated_ids": [1], "extra_prefill_tokens": 0})
    assert rec.refilled_prefix is False
    assert rec.status == "prefill_unavailable"
    assert "q = ?" in mask_prefix("task_oracle", "p1 = 4 q = 0", ["q"]) or "[mask:q]" in mask_prefix("task_oracle", "hello world tokens", ["q"])


def test_p1_bootstrap_resamples_delta_auc():
    rng = np.random.default_rng(0)
    n = 40
    y = np.array([0.0, 1.0] * 20)
    length = rng.normal(size=n)
    op = rng.normal(size=n)
    rho = y + rng.normal(scale=0.3, size=n)
    held = np.zeros(n, dtype=bool)
    held[20:] = True
    groups = [str(i // 4) for i in range(n)]
    out = p1_incremental(length, op, rho, y, held_out=held, groups=groups, rng=np.random.default_rng(1))
    lo, hi = out["bootstrap"]["interval"]
    assert out["bootstrap"]["status"] == "resampled_delta_auc"
    assert lo <= hi
    assert out["bootstrap"]["n"] >= 1


def test_week8_threshold_without_metric_is_not_evaluated():
    out = week8_decision({"status": "not_evaluated"}, gate_thresholds={"gate0": 0.9})
    assert out["gates"]["gate0"]["decision"] == "threshold_present_measurement_missing"
    assert out["gates"]["gate0"]["decision"] not in {"pass", "fail", "evaluated"}


def test_intervene_tiny_geometry_timing_stays_offline(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    inter = tmp_path / "int"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *FRAC]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--eval-mode", "scientific", "--backend", "tiny"]) == 0
    assert main(["intervene", "--in-dir", str(col), "--out-dir", str(inter), "--backend", "tiny"]) == 0
    row = read_jsonl(inter / "interventions.jsonl")[0]
    assert row["timing"] != "pre_step"
    assert row.get("clayer_status") != "dev_weak_layer"
    assert row["status"] != "donor_missing"
    assert row["status"] in {"prospective_decode", "geometry_on_hidden"}
    assert (row.get("relative") or {}).get("hook_once") == "resid_post"
    assert (row.get("relative") or {}).get("transform") == "pi_z_swap"


def test_repair_k_changes_masked_prefix(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    rep = tmp_path / "rep"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *FRAC]) == 0
    assert main(["repair", "--in-dir", str(prep), "--out-dir", str(rep), "--mask", "task_oracle", "--eval-mode", "scientific"]) == 0
    rows = read_jsonl(rep / "repairs.jsonl")
    assert {row["k"] for row in rows} == {1, 2, 3, 4, 5}
    assert all(row["refilled_prefix"] for row in rows)
    slots = [tuple(row["slots"]) for row in rows]
    assert len(set(slots)) > 1


def test_parse_events_reads_premises_and_target(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    events = parse_events("p1 = 4. p2 = 0.\nq = 9", task)
    ids = {e.node_id for e in events}
    assert {"p1", "p2", "q"} <= ids
    assert next(e.value for e in events if e.node_id == "q") == "9"


def test_common_dim_is_not_silent_truncate():
    a = np.eye(4)
    b = np.eye(3)
    out = common_dim_then_procrustes(a, b)
    assert out["truncated"] is False
    assert out["a_map"] == "pca"
    assert out["common_dim"] == 3


def test_retrieval_scatter_marks_bow_fallback():
    out = retrieval_scatter(texts_a=["a b"], texts_b=["a c"], answer_changed=[True])
    assert out["status"] == "embeddings_missing_bow_fallback"
    assert out["embedding_kind"] == "bow_descriptive_not_paper_embed"


def test_plus_numeric_edit_is_isolated_token():
    task = load_gsm_plus("tests/fixtures/t2_gsmplus_one.json")
    question = "Ada has 13 apples and buys 3 more. How many apples?"
    task.question = question
    task.premises[0].text = question
    task.premises[0].end = len(question)
    edited = apply_plus_numeric_edit(task, "3", "9")
    assert "13" in edited.task.question
    assert "19" not in edited.task.question
    assert "9 more" in edited.task.question


def test_hotpot_spoken_answer_stays_unverified():
    task = load_hotpot("tests/fixtures/t3_hotpot_one.json")
    rec = document_edit(task, next(p.document_id for p in task.premises if p.document_id), "replacement", new_answer="Spain")
    assert rec["edit"].validity == "needs_truth"
    assert rec["task"].answer_spec.status == "requires_independent_truth"


def test_analyze_uses_labels_or_stays_null(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    lab = tmp_path / "lab"
    an = tmp_path / "an"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    assert main(["analyze", "--in-dir", str(lab), "--out-dir", str(an)]) == 0
    report = read_json(an / "report.json")
    assert report["scientific_conclusion"] is None
    assert report["week8"]["gates"]["gate0"]["decision"] == "unregistered"
