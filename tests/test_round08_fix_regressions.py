from __future__ import annotations

import numpy as np

from reasoning_diff.io import file_digest
from reasoning_diff.events import answers_equal
from reasoning_diff.analysis import p3_from_rows, week8_decision
from reasoning_diff.cli import _p2_rows_from_labels
from reasoning_diff.measure import build_labels
from reasoning_diff.models.collect import intervene_hidden_decode
from reasoning_diff.repair import consecutive_repairs, mask_prefix, run_repair
from reasoning_diff.schema import Observation
from reasoning_diff.transfer import fit_linear_map


def _obs(task_id: str, outcome: str, *, sham: bool = False) -> Observation:
    return Observation(
        observation_id=f"{task_id}:{'sham' if sham else 'real'}",
        reference_trace=task_id,
        comparison_trace=f"{task_id}:edit",
        edit_id="sham:no_edit" if sham else "edit",
        premise_id="sham:p1" if sham else "p1",
        event_pair=["q", "q"],
        outcome=outcome,
        raw_values=["0", "1"],
        alignment_ref='{"entity_or_expression":"q","occurrence_version":1,"scope":"global"}',
        rng_pair="sham:0" if sham else "",
        scan_state="observed_response",
        task_id=task_id,
        base_group_id=task_id,
    )


def test_build_labels_is_generator_safe_and_task_scoped():
    rows = [_obs("t1", "changed"), _obs("t1", "changed", sham=True), _obs("t2", "no_change")]
    kwargs = {"task_ancestors": {"q": {"p1"}}, "sham_protocol": {"name": "matched"}}
    as_list = build_labels(rows, **kwargs)
    as_generator = build_labels((row for row in rows), **kwargs)
    assert [(r.task_id, r.premise_id, r.noise_ref) for r in as_list] == [
        (r.task_id, r.premise_id, r.noise_ref) for r in as_generator
    ]
    assert {r.task_id for r in as_list} == {"t1", "t2"}
    assert next(r for r in as_list if r.task_id == "t1" and r.premise_id == "sham:p1").noise_ref == 1.0


def test_directory_digest_is_deterministic_and_content_sensitive(tmp_path):
    root = tmp_path / "snapshot"
    (root / "b").mkdir(parents=True)
    (root / "b" / "two.txt").write_text("two", encoding="utf-8")
    (root / "one.txt").write_text("one", encoding="utf-8")
    first = file_digest(root)
    assert first == file_digest(root)
    (root / "one.txt").write_text("changed", encoding="utf-8")
    assert file_digest(root) != first


def test_consecutive_repairs_restart_from_clean_prefix():
    seen = []

    def execute(mask, slots, original_tokens, prefix):
        masked = mask_prefix(mask, prefix, slots)
        seen.append((slots, masked))
        return {"generated_ids": [1], "prefill_hidden": [1.0, 2.0], "text": masked}

    rows = consecutive_repairs("task_oracle", ["q", "p1"], [1, 2], "q = 1", execute=execute, k_max=2)
    assert len(rows) == 2
    assert seen[0][1] == "q = ?"
    assert seen[1][1] == "q = ?"


def test_repair_marks_missing_task_oracle_slot():
    rec = run_repair(
        "task_oracle",
        ["q"],
        [1, 2],
        "hello",
        execute=lambda *args: {"generated_ids": [1], "prefill_hidden": [1.0, 2.0]},
    )
    assert rec.status == "mask_unmatched"
    assert rec.failures == ["slot_not_found:q"]


def test_intervention_uses_supplied_basis(monkeypatch):
    import reasoning_diff.models.collect as collect

    def fail_random_basis(*args, **kwargs):
        raise AssertionError("random basis should not be sampled when fitted basis is supplied")

    monkeypatch.setattr(collect, "orthonormal_basis", fail_random_basis)
    donor = np.ones(32, dtype=float)
    basis = np.zeros((32, 1), dtype=float)
    basis[0, 0] = 1.0
    result = intervene_hidden_decode("qwen2", [1, 2, 3], 1, donor=donor, basis=basis, max_new=1)
    assert result["transform"] == "pi_z_swap"


def test_answer_scoring_normalizes_span_variants():
    assert answers_equal("The Hague.", "the hague", "span") is True


def test_p2_does_not_fabricate_noop_from_ordinary_labels(tmp_path):
    (tmp_path / "labels.jsonl").write_text('{"densities": {"rho_S_raw": 0.5}}\n', encoding="utf-8")
    assert _p2_rows_from_labels(tmp_path) == []


def test_p3_gate_uses_same_metric_key_as_summary():
    summary = p3_from_rows([{"main_acc": 1.0, "crand_acc": 0.0, "clayer_acc": 0.5, "invalid_rate": 0.0}])
    assert summary["vs_crand"] == summary["p3_vs_crand"] == 1.0
    assert week8_decision({"vs_crand": 1.0}, {"gate2": 0.5})["gates"]["gate2"]["decision"] == "compared"


def test_transfer_rejects_malformed_supervised_labels():
    source = np.eye(3)
    target = np.eye(3)
    try:
        fit_linear_map(source, target, "transfer_pairs", labeled=True, labels=np.array([0.0, 0.0, 0.0]))
    except ValueError as exc:
        assert "two label classes" in str(exc)
    else:
        raise AssertionError("single-class supervised transfer must be refused")
