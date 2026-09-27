"""CE-level regressions for round-06 A–F confirmed defects."""
from __future__ import annotations

import numpy as np
import pytest

from reasoning_diff.analysis import p1_incremental
from types import SimpleNamespace

from reasoning_diff.cli import _e_premise_ids, main
from reasoning_diff.probes.calibrate import sequence_score
from reasoning_diff.events import parse_events
from reasoning_diff.io import read_json, read_jsonl, read_npz
from reasoning_diff.measure import event_density_sets
from reasoning_diff.models.generate import generate_task_trace
from reasoning_diff.repair import run_repair
from reasoning_diff.schema import Label
from reasoning_diff.tasks.catalog import load_snapshot
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


FRAC = ["0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]


def test_generated_events_exclude_prompt_assignments(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    trace = generate_task_trace(task, seed=0, weight_seed=0, run_id="g")
    prompt = trace.metadata["prompt_text"]
    assert all(ev.start >= len(prompt) for ev in trace.events)
    assert any(ev.node_id == "q" for ev in trace.events)
    assert trace.metadata["parse_region"] == "generated"
    assert "p1 = 4 | p2 = 0 | q = 0" not in trace.text
    prompt_events = parse_events(prompt, task)
    assert any(ev.node_id in {"p1", "p2"} for ev in prompt_events)


def test_scientific_h_is_finite_and_pairs_donor(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    inter = tmp_path / "int"
    lab = tmp_path / "lab"
    fit = tmp_path / "fit"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *FRAC, "--sham-opportunities", "1"]) == 0
    traces = read_jsonl(prep / "traces.jsonl")
    assert all(row["metadata"].get("parse_region") == "generated" for row in traces)
    assert all(ev["start"] >= len(row["metadata"]["prompt_text"]) for row in traces for ev in row["events"])
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--eval-mode", "scientific", "--backend", "tiny", "--weight-seed", "0"]) == 0
    arrays = read_npz(col / "features.npz")
    assert arrays["H"].shape[0] >= 2
    assert np.isfinite(arrays["H"]).all()
    rows = read_jsonl(col / "event_rows.jsonl")
    assert len(rows) == arrays["H"].shape[0]
    spec = read_json(col / "run_spec.json")
    assert spec["config"]["weight_seed"] == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    assert main(["fit", "--in-dir", str(col), "--labels-dir", str(lab), "--out-dir", str(fit), "--split", "probe_train", "--eval-mode", "scientific"]) == 0
    probes = read_jsonl(fit / "probes.jsonl")
    bilinear = next(row for row in probes if "U" in row)
    assert np.isfinite(np.asarray(bilinear["U"])).all()
    needed = {"verbalizer", "attention_mean", "attention_rollout", "attention_threshold"}
    section8 = [row for row in probes if row.get("baseline") in needed]
    assert {row.get("baseline") for row in section8} >= needed
    attn = [row for row in section8 if row.get("baseline").startswith("attention")]
    assert attn and all(row.get("status") == "refused_not_section8" for row in attn)
    verb = [row for row in section8 if row.get("baseline") == "verbalizer"]
    assert verb and verb[0].get("status") in {"trained", "refused_not_section8"}
    assert main(["intervene", "--in-dir", str(col), "--out-dir", str(inter), "--backend", "tiny", "--dev-layer-scores", "0.05", "0.9", "0.8"]) == 0
    row = read_jsonl(inter / "interventions.jsonl")[0]
    assert row["status"] == "prospective_decode"
    assert row["timing"] == "offline_hidden"
    assert row["clayer_status"] == "dev_weak_layer_decode"
    rel = row["relative"]
    assert rel["hook_once"] == "resid_post"
    assert rel["transform"] == "pi_z_swap"
    assert rel.get("weak_layer") == 0
    assert rel.get("donor_kind") == "same_value_diff_source"
    assert rel.get("inlp_transform") == "inlp"
    assert rel.get("crand_transform") == "add_delta"
    assert rel.get("rescue_transform") == "replace"
    assert rel.get("ie_z_g") == "target_follow"
    assert rel.get("clayer_transform") == "add_delta"
    assert rel["donor_rows"][0] != rel["donor_rows"][1]
    edits = read_jsonl(prep / "edits.jsonl")
    pair = next(row for row in edits if row.get("kind") == "source_value_pair")
    assert pair["trace_ids"]["same_source_diff_value"] == "trace-edit"
    assert pair["trace_ids"]["same_value_diff_source"] == "trace-source"


def test_prefix_ids_alone_are_not_prefill():
    rec = run_repair("task_oracle", ["q"], [3], "new prefix", prefix_token_ids=[1, 2, 3], generated_tokens=[9])
    assert rec.refilled_prefix is False
    assert rec.status == "prefill_unavailable"
    dummy = run_repair("task_oracle", ["q"], [3], "new prefix", execute=lambda *a: {"generated_ids": [1], "refilled_prefix": True, "prefill_hidden": []})
    assert dummy.refilled_prefix is False


def test_p1_bootstrap_interval_is_not_degenerate():
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
    assert lo < hi


def test_sham_hits_do_not_book_evaluated_zero_noise():
    labels = [
        Label("q", "sham:q", 0, True, None, False, 1.0, "no_edit_matched"),
        Label("q", "p1", 1, True, 0, True, 0.0, "no_edit_matched"),
    ]
    task = load_t1_fixture("tests/fixtures/t1_tiny.json")
    dens = event_density_sets(task, labels, sham_protocol={"name": "no_edit_matched", "hits": ["q"]})
    rows = dens.get("events") or []
    assert rows
    for row in rows:
        assert row.get("rho_S_noise") is None
        assert row.get("rho_M_noise") is None
        assert row.get("rho_S_excess") is None
        assert row.get("rho_M_excess") is None
        assert row.get("null_reason") == "noise_set_missing"


def test_catalog_aliases_musique_and_t4():
    musique = load_snapshot("t3_musique", "tests/fixtures/t3_musique_pair.json")
    t4 = load_snapshot("t4_boundary", "tests/fixtures/t4_boundary.json")
    assert musique
    assert (t4[0] if isinstance(t4, list) else t4).tier == "T4"


def test_truth_indices_follow_e_columns_not_label_order():
    labels = [{"premise_id": "p3"}, {"premise_id": "p2"}, {"premise_id": "p1"}]
    task = SimpleNamespace(premises=[SimpleNamespace(premise_id=n) for n in ("p1", "p2", "p3")])
    cols = _e_premise_ids(task, labels)
    assert cols == ["p1", "p2", "p3"]
    pred = [0.9, 0.1, 0.8]
    truth = [j for j, p in enumerate(cols) if p == "p1"]
    assert sequence_score(pred, True, False, "one_minus_p", truth) == pytest.approx(0.1)
    wrong = [p for p in dict.fromkeys(r["premise_id"] for r in labels)]
    assert wrong == ["p3", "p2", "p1"]
    assert sequence_score(pred, True, False, "one_minus_p", [wrong.index("p1")]) == pytest.approx(0.2)
    only_last = _e_premise_ids(task, [{"premise_id": "p2"}])
    assert only_last.index("p2") == 1
    assert sequence_score([0.1, 0.9, 0.8], True, False, "one_minus_p", [only_last.index("p2")]) == pytest.approx(0.1)


def test_missing_in_dir_fails_for_downstream(tmp_path):
    with pytest.raises(ValueError, match="in-dir"):
        main(["calibrate", "--out-dir", str(tmp_path / "c"), "--split", "calibration"])
    with pytest.raises(ValueError, match="in-dir"):
        main(["intervene", "--out-dir", str(tmp_path / "i")])
    with pytest.raises(ValueError, match="in-dir"):
        main(["repair", "--out-dir", str(tmp_path / "r"), "--mask", "task_oracle"])
