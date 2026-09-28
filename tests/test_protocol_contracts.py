from __future__ import annotations

import numpy as np

from reasoning_diff.analysis import classification_metrics, p3_from_rows
from reasoning_diff.protocol import answer_score, recursive_manifest, stable_row_key


def test_stable_row_key_is_order_independent_and_identity_sensitive():
    first = stable_row_key(task_id="t1", base_group_id="g1", trace_id="r0", event_id="q", premise_id="p1")
    second = stable_row_key(premise_id="p1", event_id="q", trace_id="r0", base_group_id="g1", task_id="t1")
    changed = stable_row_key(task_id="t2", base_group_id="g1", trace_id="r0", event_id="q", premise_id="p1")
    assert first == second
    assert first != changed


def test_answer_score_preserves_span_aliases_and_missing_status():
    scored = answer_score("The Hague.", "the hague", "span", aliases=["Den Haag"])
    missing = answer_score(None, "the hague", "span")
    assert scored["correct"] is True
    assert scored["score_status"] == "scored"
    assert missing["correct"] is None
    assert missing["score_status"] == "missing_answer"


def test_recursive_manifest_is_stable_for_directory(tmp_path):
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    first = recursive_manifest(tmp_path, data_version="v1", loader_version="loader")
    second = recursive_manifest(tmp_path, data_version="v1", loader_version="loader")
    assert first["manifest_hash"] == second["manifest_hash"]
    assert [item["path"] for item in first["files"]] == ["a.txt", "b.txt"]


def test_classification_metrics_reports_held_out_pr_auc():
    metrics = classification_metrics(np.array([0.1, 0.9, 0.8, 0.2]), np.array([0, 1, 1, 0]), split="test", groups=["a", "b", "b", "c"])
    assert metrics["held_out"] is True
    assert metrics["auc"] == 1.0
    assert metrics["pr_auc"] == 1.0
    assert metrics["n_units"] == 4


def test_p3_keeps_problem_interval_and_unregistered_status():
    report = p3_from_rows(
        [
            {"problem_id": "p1", "main_acc": 1.0, "crand_acc": 0.0, "clayer_acc": 0.5, "invalid_rate": 0.0},
            {"problem_id": "p2", "main_acc": 0.0, "crand_acc": 0.0, "clayer_acc": 0.0, "invalid_rate": 1.0},
        ]
    )
    assert report["statistical_unit"] == "problem"
    assert report["multiplicity_status"] == "unregistered"
    assert report["vs_crand_interval"]["n_groups"] == 2
