import pytest

from reasoning_diff.io import read_json
from reasoning_diff.splits import assign_split
from reasoning_diff.tasks.t2_gsm_plus import load_gsm_plus, refuse_fit_split
from reasoning_diff.tasks.t2_gsm_symbolic import apply_formula_edit, load_gsm_symbolic, score_numeric


def test_symbolic_sidecar_edit():
    sidecar = read_json("tests/fixtures/t2_formula_sidecar.json")
    task = load_gsm_symbolic("tests/fixtures/t2_symbolic_one.json", sidecar)
    assert task.graph_status == "partial"
    assert task.base_group_id == "gsm8k-12"
    edited = apply_formula_edit(task, sidecar, "a", "5")
    assert edited.answer_spec.value == "8"
    assert score_numeric("8", "8")["value"] == 1.0


def test_symbolic_without_sidecar_is_unknown():
    task = load_gsm_symbolic("tests/fixtures/t2_symbolic_one.json")
    assert task.graph_status == "unknown"
    with pytest.raises(ValueError):
        apply_formula_edit(task, {}, "a", "5")


def test_gsm_plus_is_test_only():
    task = load_gsm_plus("tests/fixtures/t2_gsmplus_one.json")
    assert task.graph_status == "unknown"
    assert task.metadata["fit_eligible"] is False
    assert task.metadata["role"] == "test"
    assert assign_split(task.base_group_id, test_only=True) == "test"
    with pytest.raises(ValueError):
        refuse_fit_split(task, "probe_train")
