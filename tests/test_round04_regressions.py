"""Regressions for round-04 A–F confirmed science-path defects."""
from __future__ import annotations

import numpy as np
import pytest

from reasoning_diff.analysis import p1_incremental, p2_paired, week8_decision
from reasoning_diff.baselines import fit_attention_threshold, verbalizer
from reasoning_diff.cli import main
from reasoning_diff.edits import apply_source_value_edit, make_source_value_pair
from reasoning_diff.events import Event, EventIdentity, align_events_monotonic
from reasoning_diff.executor import ChildProcessExecutor, IsolatedExecutor, SubprocessExecutor
from reasoning_diff.io import read_json, read_jsonl, read_npz
from reasoning_diff.measure import dependency_densities, event_density_sets
from reasoning_diff.models.tokenize import readout_layer_index, span_token_indices
from reasoning_diff.probes.boundary import BoundaryMLP
from reasoning_diff.probes.calibrate import sequence_score
from reasoning_diff.repair import execute_repair_tiny, mask_prefix, run_repair
from reasoning_diff.schema import Label
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t2_gsm_plus import load_gsm_plus
from reasoning_diff.tasks.t2_gsm_symbolic import load_gsm_symbolic


def test_readout_layer_is_60_75_band():
    assert readout_layer_index(3) == 1
    assert 0 <= readout_layer_index(32) < 32


def test_scientific_prepare_is_generated_not_node_values(tmp_path, t1_tiny_path):
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
                "0.4",
                "0.15",
                "0.1",
                "0.1",
                "0.1",
                "0.15",
                "--sham-opportunities",
                "1",
            ]
        )
        == 0
    )
    traces = read_jsonl(out / "traces.jsonl")
    assert traces[0]["model"] != "fixture"
    assert traces[0]["metadata"].get("generation") == "decode_loop"
    assert "p1 = 4 | p2 = 0 | q = 0" not in traces[0]["text"]
    assert all(len(row["events"]) >= 1 for row in traces)
    seeds = {row["seed"] for row in traces}
    assert 0 in seeds and 1 in seeds
    sham = next(row for row in traces if row["id"] == "trace-sham")
    assert sham["seed"] == 2
    assert sham["text"] != traces[0]["text"] or sham["token_ids"] != traces[0]["token_ids"]


def test_scientific_collect_span_pool_and_refuses_offline(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    fracs = ["0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *fracs]) == 0
    with pytest.raises(ValueError, match="offline_prefix_ids"):
        main(
            [
                "collect",
                "--fixture",
                str(t1_tiny_path),
                "--in-dir",
                str(prep),
                "--out-dir",
                str(col),
                "--eval-mode",
                "scientific",
                "--backend",
                "offline",
            ]
        )
    assert (
        main(
            [
                "collect",
                "--fixture",
                str(t1_tiny_path),
                "--in-dir",
                str(prep),
                "--out-dir",
                str(col),
                "--eval-mode",
                "scientific",
                "--backend",
                "tiny",
            ]
        )
        == 0
    )
    arrays = read_npz(col / "features.npz")
    assert arrays["E"].shape[0] >= 2
    assert not np.allclose(arrays["E"][0], arrays["E"][1], equal_nan=False)
    spec = read_json(col / "run_spec.json")
    assert spec["config"]["hidden_layer"] == 1
    assert spec["config"]["weight_source"] == "random_init"
    assert "H_pre_step" in arrays


def test_intervene_geometry_is_not_pre_step(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    inter = tmp_path / "int"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    assert main(["intervene", "--in-dir", str(col), "--out-dir", str(inter), "--backend", "offline"]) == 0
    row = read_jsonl(inter / "interventions.jsonl")[0]
    assert row["status"] == "donor_missing"
    assert row["timing"] == "unexpressible"
    assert row["clayer_status"] == "dev_scores_missing"


def test_repair_tiny_prefills_and_masks_differ():
    a = mask_prefix("task_oracle", "hello world tokens", ["q"])
    b = mask_prefix("full_recompute", "hello world tokens", ["q"])
    c = mask_prefix("prompt_instruction", "hello world tokens", ["q"])
    assert a != b != c
    executed = execute_repair_tiny("task_oracle", ["q"], [1, 2, 3, 4], "hello world tokens")
    rec = run_repair("task_oracle", ["q"], [1, 2, 3, 4], "hello world tokens", execute=execute_repair_tiny, run_id="r")
    assert rec.refilled_prefix is True
    assert rec.generated_tokens > 0
    assert rec.extra_prefill_tokens == executed["extra_prefill_tokens"]


def test_sequence_score_uses_true_edges_only():
    assert sequence_score([0.9, 0.1, 0.2], True, False, nonconformity="one_minus_p", truth_indices=[0]) == pytest.approx(0.1)
    assert sequence_score([0.9, 0.1, 0.2], True, False, nonconformity="one_minus_p") == pytest.approx(0.9)


def test_boundary_bce_not_negative():
    mlp = BoundaryMLP(2)
    x = np.array([[10.0, 0.0], [10.0, 0.0]])
    y = np.array([0.0, 0.0])
    mlp.W1[:] = 0
    mlp.W2[:] = 10
    mlp.b2[:] = 10
    out = mlp.fit(x, y, steps=0)
    assert out["loss"] is not None
    assert out["loss"] > 0


def test_evaluated_zero_hit_sham_is_zero_noise_not_null():
    labels = [
        Label("q", "p3", 0, True, 1, True, 0.0, "no_edit_matched"),
        Label("q", "p1", 1, True, 0, True, 0.0, "no_edit_matched"),
        Label("q", "p2", 1, True, 0, True, 0.0, "no_edit_matched"),
    ]
    task = load_t1_fixture("tests/fixtures/t1_tiny.json")
    # force ancestors q -> p1,p2 by using fixture; behavior p3 is not a premise on tiny.
    out = dependency_densities(
        premises=["p1", "p2", "p3"],
        task_set=["p1", "p2"],
        behavior_set=["p3"],
        noise_set=[],
        sham_protocol={"name": "no_edit_matched"},
        noise_evaluated=True,
    )
    assert out["rho_S_raw"] == pytest.approx(1.0)
    assert out["rho_S_noise"] == pytest.approx(0.0)
    assert out["rho_S_excess"] == pytest.approx(1.0)
    empty = event_density_sets(task, labels, {"name": "no_edit_matched"})
    empty_rows = empty.get("events") or []
    assert empty_rows
    for row in empty_rows:
        assert row.get("null_reason") == "noise_set_missing"
        assert row.get("rho_S_noise") is None
        assert row.get("rho_M_noise") is None
        assert row.get("rho_S_excess") is None
        assert row.get("rho_M_excess") is None


def test_week8_zero_excess_is_descriptive_negative():
    out = week8_decision({"status": "not_evaluated", "rho_S_excess": 0.0})
    assert out["status"] == "c3_negative_descriptive"
    assert out["skip_p2_p3"] is True
    assert out["gates"]["gate0"]["decision"] == "unregistered"


def test_p2_integer_denom_without_set_is_unverified():
    out = p2_paired(0.2, 0.5, 0.8, 0.6, 99)
    assert out["status"] == "denominator_unverified"
    assert out["delta_rho"] is None


def test_p1_returns_bootstrap_interval():
    n = 20
    y = np.array([0.0, 1.0] * 10)
    rho = y.copy()
    held = np.zeros(n, dtype=bool)
    held[10:] = True
    out = p1_incremental(np.full(n, 3.0), np.zeros(n), rho, y, held_out=held, groups=[str(i // 2) for i in range(n)], rng=np.random.default_rng(0))
    assert out["bootstrap"] is not None
    assert out["bootstrap"]["interval"] is not None


def test_verbalizer_without_generate_is_unavailable():
    out = verbalizer("zeroshot", "prefix", "gold", False)
    assert out["status"] == "generate_unavailable"
    assert out["score"] is None
    gen = verbalizer("zeroshot", "prefix", "7", False, generate_fn=lambda p: "answer 7")
    assert gen["status"] == "generated"
    assert gen["score"] == 1.0


def test_attention_threshold_uses_dev_split():
    fitted = fit_attention_threshold(np.array([0.1, 0.8, 0.2, 0.9]), np.array([0.0, 1.0, 0.0, 1.0]), split="dev")
    assert fitted["split"] == "dev"
    assert 0.0 <= fitted["threshold"] <= 1.0


def test_child_process_is_not_isolated_executor():
    assert not isinstance(ChildProcessExecutor(), IsolatedExecutor)
    assert SubprocessExecutor is ChildProcessExecutor
    assert ChildProcessExecutor.isolated_sandbox is False


def test_source_value_pair_has_both_conditions(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    pair = make_source_value_pair(task, "p2", "2")
    assert pair["same_value_diff_source"].metadata["same_value_diff_source"] is True
    edit = apply_source_value_edit(task, "p2", "2")
    assert edit.metadata["decoupled_pair"]["same_value_diff_source"] is True


def test_plus_and_symbolic_share_gsm8k_family():
    plus = load_gsm_plus("tests/fixtures/t2_gsmplus_one.json")
    symbolic = load_gsm_symbolic("tests/fixtures/t2_symbolic_one.json")
    assert plus.metadata["shared_gsm_family"] == symbolic.base_group_id == "gsm8k-12"
    assert plus.base_group_id.startswith("gsm_plus:")


def test_nl_monotonic_keeps_matching_versions():
    left = Event(EventIdentity("q", 1), "1", 0, 1, 0, "q=1", node_id="q")
    mid = Event(EventIdentity("q", 2), "2", 2, 3, 2, "q=2", node_id="q")
    right = Event(EventIdentity("q", 2), "9", 2, 3, 2, "q=9", node_id="q")
    out = align_events_monotonic([left, mid], [right])
    assert out["pairs"] == []
    assert out["structural"]["ambiguous"]


def test_span_pool_uses_contained_tokens():
    assert span_token_indices([[0, 2], [2, 6], [6, 8]], 2, 6) == [1]


def test_resume_collect_matches_written_command(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    before = read_json(col / "manifest.json")
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline", "--resume"]) == 0
    after = read_json(col / "manifest.json")
    assert after["file_hashes"] == before["file_hashes"]


def test_failed_resume_does_not_clobber_success_manifest(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    (col / "traces.jsonl").write_text("not-json", encoding="utf-8")
    with pytest.raises(ValueError):
        main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline", "--resume"])
    manifest = read_json(col / "manifest.json")
    assert "traces.jsonl" in manifest["file_hashes"]
    assert (col / "failure.json").exists()


def test_calibrate_infinity_is_json_safe(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    lab = tmp_path / "lab"
    fit = tmp_path / "fit"
    cal = tmp_path / "cal"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "tiny"]) == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    assert main(["fit", "--in-dir", str(col), "--labels-dir", str(lab), "--out-dir", str(fit), "--split", "probe_train"]) == 0
    assert main(["calibrate", "--in-dir", str(fit), "--features-dir", str(col), "--out-dir", str(cal), "--split", "calibration"]) == 0
    row = read_jsonl(cal / "calibration.jsonl")[0]
    assert row["q"] is None or isinstance(row["q"], (int, float))
    if row.get("infinity"):
        assert row["q"] is None


def test_analyze_requires_directory(tmp_path):
    with pytest.raises(ValueError):
        main(["analyze", "--out-dir", str(tmp_path / "an"), "--eval-mode", "scientific"])
    src = tmp_path / "file.json"
    src.write_text("{}", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        main(["analyze", "--in-dir", str(src), "--out-dir", str(tmp_path / "an2")])
    assert not (tmp_path / "an2" / "report.json").exists()


def test_scientific_repair_runs_k_1_to_5(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    rep = tmp_path / "rep"
    fracs = ["0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *fracs]) == 0
    assert main(["repair", "--in-dir", str(prep), "--out-dir", str(rep), "--mask", "task_oracle", "--eval-mode", "scientific"]) == 0
    rows = read_jsonl(rep / "repairs.jsonl")
    assert {row["k"] for row in rows} == {1, 2, 3, 4, 5}
    assert all(row["refilled_prefix"] for row in rows)
    assert all(row["generated_tokens"] > 0 for row in rows)
