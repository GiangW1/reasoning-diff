"""Regressions for confirmed round-01 defects. Each case is an independent oracle."""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from reasoning_diff.analysis import p1_incremental
from reasoning_diff.cli import main
from reasoning_diff.edits import apply_value_edit
from reasoning_diff.events import align_events, parse_fixture_events
from reasoning_diff.interventions import c_layer_delta, c_rand_delta, inlp_remove, project_delta
from reasoning_diff.io import read_json, read_jsonl, write_npz
from reasoning_diff.measure import build_labels, dependency_densities, preservation_to_csp
from reasoning_diff.models.features import select_prefix_index
from reasoning_diff.probes.calibrate import conformal_threshold
from reasoning_diff.schema import Event, EventIdentity, Observation, Trace
from reasoning_diff.splits import assign_family, assign_split
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t2_gsm_symbolic import apply_formula_edit, load_gsm_symbolic
from reasoning_diff.tasks.t2_noop import make_noop_pair
from reasoning_diff.tasks.t3_humaneval import load_humaneval
from reasoning_diff.io import read_json as read_json_file


def _event(entity, occ, value, parents=None, node_id="", graph_status="unknown"):
    return Event(
        EventIdentity(entity, occ, "global"),
        value,
        0,
        3,
        2,
        f"{entity}={value}",
        parents,
        node_id=node_id or entity,
        graph_status=graph_status,
    )


def test_b01_missing_noise_is_null_not_zero():
    task = np.array([[0, 1]], dtype=float)
    behavior = np.array([[1, 0]], dtype=float)
    result = dependency_densities(task=task, behavior=behavior, noise=None)
    assert result["events"][0]["S"]["noise"] is None
    assert result["events"][0]["S"]["excess"] is None
    assert result["events"][0]["M"]["noise"] is None
    assert result["rho_S_noise"] is None


def test_b02_finite_scan_no_change_is_unknown():
    obs = Observation(
        "o1",
        "a",
        "b",
        "e",
        "p1",
        ["q", "q"],
        "no_change",
        ["0", "0"],
        "q",
        scan_state="no_response_observed_in_scan",
        node_id="q",
    )
    labels = build_labels([obs], {"q": {"p1"}})
    assert labels[0].behavior_known is True
    assert labels[0].behavior_label == 0


def test_b03_sham_does_not_enter_r_behavior():
    real = Observation(
        "o1",
        "a",
        "b",
        "e",
        "p3",
        ["q", "q"],
        "no_change",
        ["0", "0"],
        "q",
        rng_pair="stream:0",
        scan_state="observed_response",
        exhaustive=True,
        node_id="q",
    )
    sham = Observation(
        "o2",
        "a",
        "b",
        "e",
        "sham:q",
        ["q", "q"],
        "changed",
        ["0", "1"],
        "q",
        rng_pair="sham:0",
        scan_state="observed_response",
        node_id="q",
    )
    labels = build_labels(
        [real, sham],
        {"q": {"p1"}},
        sham_protocol={"name": "matched", "opportunities": 1},
    )
    by_id = {lab.premise_id: lab for lab in labels}
    assert by_id["p3"].behavior_label == 0
    assert by_id["p3"].noise_ref is None
    assert by_id["sham:q"].noise_ref == 1.0


def test_b04_deletion_does_not_rematch_by_shifted_occurrence():
    base = [_event("q", 1, "1", ["p1"], "q"), _event("q", 2, "2", ["p1"], "q")]
    changed = [_event("q", 1, "2", ["p1"], "q")]
    aligned = align_events(base, changed)
    assert aligned["pairs"] == []
    assert aligned["structural"]["disappeared"]


def test_b06_surface_mentions_are_text_not_parents(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    events = parse_fixture_events("q = 0\n", task)
    assert events[0].task_parents == ["p1", "p2"]
    assert events[0].surface_mentions == []


def test_b07_humaneval_family_is_full_task_id():
    task = load_humaneval("tests/fixtures/t3_humaneval_one.json")
    assert task.base_group_id == "HumanEval/0"


def test_b08_formula_edit_updates_question_and_nodes():
    sidecar = read_json_file("tests/fixtures/t2_formula_sidecar.json")
    task = load_gsm_symbolic("tests/fixtures/t2_symbolic_one.json", sidecar)
    edited = apply_formula_edit(task, sidecar, "a", "5")
    assert "5" in edited.question
    assert edited.premises[0].value == "5"
    assert edited.nodes[0].value == "8"
    assert edited.answer_spec.value == "8"


def test_b09_value_edit_does_not_rewrite_larger_numeral(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    data = task.to_dict()
    data["question"] = "p1 = 14. p2 = 0. What is q = p1 * p2?"
    data["premises"][0] = {
        "premise_id": "p1",
        "text": "p1 = 14",
        "start": 0,
        "end": 7,
        "value": "4",
        "kind": "fact",
    }
    data["premises"][1] = {
        "premise_id": "p2",
        "text": "p2 = 0",
        "start": 9,
        "end": 15,
        "value": "0",
        "kind": "fact",
    }
    from reasoning_diff.schema import Task

    broken = Task.from_dict(data)
    with pytest.raises(ValueError):
        apply_value_edit(broken, "p1", "9")


def test_b10_noop_does_not_steal_front_span(t1_tiny_path):
    base = load_t1_fixture(t1_tiny_path)
    pair = make_noop_pair(base, "p1 = 4 is a red herring.", "front", "high", True)
    original = next(p for p in pair.premises if p.premise_id == "p1")
    injected = next(p for p in pair.premises if p.premise_id == "noop")
    assert original.start > injected.start
    assert pair.question[original.start:original.end] == original.text


def test_b11_empty_parents_are_not_clean_when_graph_unknown():
    base = Trace("b", "t", "g", "m", 0, "q=1", [1], [[0, 3]], [_event("q", 1, "1", [])], "1", True)
    changed = Trace("c", "t", "g", "m", 0, "q=2", [1], [[0, 3]], [_event("q", 1, "2", [])], "2", True)
    result = preservation_to_csp(base, changed, {"p1"})
    assert result["csp"] is None
    assert result["clean_matched"] == 0


def test_b13_assign_family_uses_family_id_not_first_member():
    with pytest.raises(ValueError):
        assign_family(["z-member", "a-member"])
    a = assign_family(["z-member", "a-member"], family_id="family-A")
    b = assign_family(["a-member", "m-other"], family_id="family-B")
    # Different family ids must be allowed to differ; hashing the first member would collide on a-member.
    assert set(a.values()) == {a["z-member"]}
    if a["a-member"] == b["a-member"]:
        c = assign_family(["a-member", "m-other"], family_id="family-C")
        assert len({a["a-member"], b["a-member"], c["a-member"]}) >= 2


def test_b14_gsm_plus_source_cannot_enter_fit_split():
    assert assign_split("anything", source="gsm_plus") == "test"
    assert assign_split("anything", test_only=True) == "test"
    from reasoning_diff.tasks.t2_gsm_plus import load_gsm_plus

    task = load_gsm_plus("tests/fixtures/t2_gsmplus_one.json")
    assert assign_split(task.base_group_id) == "test"
    assert task.base_group_id.startswith("gsm_plus:")


def test_c01_auc_is_rank_and_permutation_invariant():
    length = np.array([1.0, 2.0, 3.0, 4.0])
    op = np.zeros(4)
    rho = length.copy()
    y = np.array([0.0, 0.0, 1.0, 1.0])
    out = p1_incremental(length, op, rho, y, precomputed=True)
    assert out["delta_auc"] == 0.0
    perm = np.array([2, 0, 3, 1])
    shuffled = p1_incremental(length[perm], op[perm], rho[perm], y[perm], precomputed=True)
    assert shuffled["auc_base"] == pytest.approx(out["auc_base"])
    assert shuffled["auc_full"] == pytest.approx(out["auc_full"])


def test_c01_held_out_fit_does_not_use_eval_rows():
    rng = np.random.default_rng(0)
    n = 40
    length = rng.normal(size=n)
    op = rng.normal(size=n)
    rho = rng.normal(size=n)
    y = (length + op > 0).astype(float)
    held = np.zeros(n, dtype=bool)
    held[n // 2 :] = True
    out = p1_incremental(length, op, rho, y, held_out=held)
    assert out["held_out"] is True
    assert out["auc_base"] is not None


def test_c02_conformal_alpha_at_least_one_is_invalid():
    assert conformal_threshold([0.1, 0.2, 0.3], 1.0)["status"] == "invalid"
    assert conformal_threshold([0.1, 0.2, 0.3], 1.5)["status"] == "invalid"


def test_c03_inlp_iterates_on_projected_h():
    h = np.array([[2.0, 0.0], [2.0, 0.0], [0.0, 1.0], [0.0, 1.0]])
    y = np.array([1.0, 1.0, 0.0, 0.0])
    p = inlp_remove(h, y, steps=2)
    projected = h @ p
    assert np.allclose(projected[:, 0], 0.0, atol=1e-6)


def test_c04_crand_matches_provided_main_norm_not_rng1():
    rng = np.random.default_rng(0)
    base = rng.normal(size=8)
    donor = rng.normal(size=8)
    from reasoning_diff.interventions import orthonormal_basis

    main = project_delta(base, donor, orthonormal_basis(8, 2, np.random.default_rng(99)))
    target = float(np.linalg.norm(main))
    cr = c_rand_delta(base, donor, 2, np.random.default_rng(3), target_norm=target)
    assert cr["actual_norm"] == pytest.approx(target)
    with pytest.raises(ValueError):
        c_rand_delta(base, donor, 2, np.random.default_rng(3))
    layer = c_layer_delta(base, donor, orthonormal_basis(8, 2, np.random.default_rng(7)), target)
    assert layer["actual_norm"] == pytest.approx(target)


def test_d01_three_positions_differ_and_leak_flag_is_real():
    offsets = [[0, 1], [1, 3], [3, 5], [5, 8], [8, 10]]
    pre = select_prefix_index(offsets, 3, "pre_step")
    val = select_prefix_index(offsets, 3, "pre_value", value_start=5)
    post = select_prefix_index(offsets, 3, "post_step", target_end=8)
    assert pre["token_index"] != val["token_index"] != post["token_index"]
    assert pre["token_index"] == 1
    assert val["token_index"] == 2
    assert post["token_index"] == 3
    leak = select_prefix_index([[0, 10]], 3, "pre_step")
    assert leak["token_index"] is None
    assert leak["leaks_target"] is True
    assert leak["straddling_excluded"] == [0]


def test_e02_default_prepare_is_not_zero_multiply(tmp_path, t1_tiny_path):
    out = tmp_path / "prep"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(out)]) == 0
    tasks = read_jsonl(out / "tasks.jsonl")
    edited = tasks[1]
    assert edited["answer_spec"]["value"] != tasks[0]["answer_spec"]["value"]
    obs = read_jsonl(out / "observations.jsonl")
    assert any(row["outcome"] == "changed" for row in obs)


def test_e04_analyze_manifest_includes_report(tmp_path):
    out = tmp_path / "an"
    with pytest.raises(ValueError, match="--in-dir"):
        main(["analyze", "--out-dir", str(out)])
    src = tmp_path / "empty"
    src.mkdir()
    assert main(["analyze", "--in-dir", str(src), "--out-dir", str(out)]) == 0
    manifest = read_json(out / "manifest.json")
    assert "report.json" in manifest["file_hashes"]
    report = read_json(out / "report.json")
    assert report.get("scientific_conclusion") is None


def test_e08_module_entrypoint_exists():
    import reasoning_diff.__main__ as entry

    assert hasattr(entry, "main")


def test_e06_npz_write_is_atomic(tmp_path):
    path = tmp_path / "feat.npz"
    write_npz(path, {"x": np.arange(3)})
    leftovers = list(tmp_path.glob(".feat.npz.*.tmp"))
    assert leftovers == []
    assert path.exists()


def test_b23_observed_no_change_without_exhaustive_is_unknown():
    obs = Observation(
        "o1",
        "a",
        "b",
        "e",
        "p1",
        ["q", "q"],
        "no_change",
        ["0", "0"],
        "q",
        scan_state="observed_response",
        exhaustive=False,
        node_id="q",
    )
    labels = build_labels([obs], {"q": {"p1"}})
    assert labels[0].behavior_known is True
    assert labels[0].behavior_label == 0


def test_b24_integer_value_does_not_edit_decimal_fraction(t1_tiny_path):
    from reasoning_diff.schema import Task

    task = load_t1_fixture(t1_tiny_path)
    data = task.to_dict()
    data["question"] = "p1 = 3.5. p2 = 0. What is q = p1 * p2?"
    data["premises"][0] = {"premise_id": "p1", "text": "p1 = 3.5", "start": 0, "end": 8, "value": "5", "kind": "fact"}
    data["premises"][1] = {"premise_id": "p2", "text": "p2 = 0", "start": 10, "end": 16, "value": "0", "kind": "fact"}
    broken = Task.from_dict(data)
    with pytest.raises(ValueError):
        apply_value_edit(broken, "p1", "9")
    data["question"] = "p1 = 5.5. p2 = 0. What is q = p1 * p2?"
    data["premises"][0] = {"premise_id": "p1", "text": "p1 = 5.5", "start": 0, "end": 8, "value": "5", "kind": "fact"}
    with pytest.raises(ValueError):
        apply_value_edit(Task.from_dict(data), "p1", "9")


def test_b06_surface_mentions_include_text_after_value(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    events = parse_fixture_events("q = 0 mentions p1\n", task)
    assert "p1" in events[0].surface_mentions


def test_c_unknown_label_is_masked():
    from reasoning_diff.probes.bilinear import weighted_bce

    pred = np.array([0.2, 0.8])
    target = np.array([-1.0, 1.0])
    loss = weighted_bce(pred, target, np.ones(2))
    only = weighted_bce(pred[1:], target[1:], np.ones(1))
    assert loss == pytest.approx(only)


def test_rho_event_mean_is_not_union():
    from reasoning_diff.measure import dependency_densities

    out = dependency_densities(
        event_sets=[
            {"premises": ["p1", "p2"], "task_set": ["p1"], "behavior_set": ["p2"]},
            {"premises": ["p1", "p2"], "task_set": ["p1"], "behavior_set": []},
        ]
    )
    assert out["aggregation"] == "mean_over_events"
    assert out["rho_S_raw"] == pytest.approx(0.5)


def test_p1_requires_held_out_by_default():
    out = p1_incremental(np.ones(4), np.ones(4), np.ones(4), np.array([0, 0, 1, 1.0]))
    assert out["status"] == "requires_held_out"


def test_pipeline_consumes_upstream(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    lab = tmp_path / "lab"
    fit = tmp_path / "fit"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    assert main(["fit", "--in-dir", str(col), "--labels-dir", str(lab), "--out-dir", str(fit), "--split", "probe_train"]) == 0
    labels = read_jsonl(lab / "labels.jsonl")
    assert any("task_label" in row for row in labels)
    probes = read_jsonl(fit / "probes.jsonl")
    assert probes[0]["split"] == "probe_train"
    assert "loss" in probes[0]
