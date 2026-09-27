"""CE-level regressions for late r07/r08 defects that still reproduced."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from reasoning_diff.cli import main
from reasoning_diff.edits import apply_rename_edit, make_source_value_pair
from reasoning_diff.events import merge_review, review_export
from reasoning_diff.io import read_json, read_jsonl, write_jsonl
from reasoning_diff.graphs import ancestors
from reasoning_diff.measure import build_labels, dependency_densities, event_density_sets
from reasoning_diff.repair import run_repair
from reasoning_diff.schema import Event, EventIdentity, Observation
from reasoning_diff.splits import _TEST_ONLY_FAMILY_KEYS, clear_test_only_families, split_for_task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t2_gsm_plus import load_gsm_plus
from reasoning_diff.tasks.t2_gsm_symbolic import load_gsm_symbolic
from reasoning_diff.transfer import common_dim_then_procrustes


FRAC = ["0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]


def test_fit_without_tasks_jsonl_refuses_first_seen_order(tmp_path, t1_tiny_path):
    work = tmp_path / "run"
    prep = work / "prep"
    col = work / "col"
    lab = work / "lab"
    odd = tmp_path / "orphan" / "hidden_features"
    isolated = tmp_path / "orphan" / "isolated_labels"
    fit = tmp_path / "orphan" / "fit"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    odd.mkdir(parents=True)
    isolated.mkdir(parents=True)
    (odd / "features.npz").write_bytes((col / "features.npz").read_bytes())
    if (col / "traces.jsonl").exists():
        (odd / "traces.jsonl").write_bytes((col / "traces.jsonl").read_bytes())
    (isolated / "labels.jsonl").write_bytes((lab / "labels.jsonl").read_bytes())
    with pytest.raises(ValueError, match="tasks.jsonl"):
        main(["fit", "--in-dir", str(odd), "--labels-dir", str(isolated), "--out-dir", str(fit), "--split", "probe_train"])


def test_fit_does_not_bind_ancestor_col_tasks(tmp_path, t1_tiny_path):
    from reasoning_diff.cli import _e_premise_ids, _find_tasks_jsonl
    from reasoning_diff.schema import Task

    work = tmp_path / "bind"
    prep = work / "prep"
    col = work / "col"
    lab = work / "lab"
    feat = work / "deep" / "x" / "feat"
    isolated = work / "deep" / "x" / "labs"
    fit = work / "deep" / "x" / "fit"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    feat.mkdir(parents=True)
    isolated.mkdir(parents=True)
    (feat / "features.npz").write_bytes((col / "features.npz").read_bytes())
    if (col / "traces.jsonl").exists():
        (feat / "traces.jsonl").write_bytes((col / "traces.jsonl").read_bytes())
    (isolated / "labels.jsonl").write_bytes((lab / "labels.jsonl").read_bytes())
    real = Task.from_dict(read_jsonl(prep / "tasks.jsonl")[0])
    swapped = real.to_dict()
    swapped["task_id"] = "WRONG-TASK"
    swapped["premises"] = list(reversed(swapped["premises"]))
    write_jsonl(col / "tasks.jsonl", [swapped])
    assert _find_tasks_jsonl(feat, isolated) is None
    with pytest.raises(ValueError, match="tasks.jsonl"):
        main(["fit", "--in-dir", str(feat), "--labels-dir", str(isolated), "--out-dir", str(fit), "--split", "probe_train"])
    labels = [row for row in read_jsonl(isolated / "labels.jsonl") if "premise_id" in row]
    assert _e_premise_ids(real, labels) != _e_premise_ids(Task.from_dict(swapped), labels)


def test_collect_copies_tasks_so_fit_follows_e_order(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    col = tmp_path / "col"
    lab = tmp_path / "lab"
    fit = tmp_path / "fit"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep)]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--backend", "offline"]) == 0
    assert (col / "tasks.jsonl").exists()
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    assert main(["fit", "--in-dir", str(col), "--labels-dir", str(lab), "--out-dir", str(fit), "--split", "probe_train"]) == 0
    assert (fit / "probes.jsonl").exists()


def test_scalar_prefill_hidden_is_not_prefill():
    for hidden in (0, True, 1.0, [0], []):
        rec = run_repair(
            "task_oracle",
            ["q"],
            [3],
            "new prefix",
            execute=lambda *a, h=hidden: {"generated_ids": [1], "prefill_hidden": h},
        )
        assert rec.refilled_prefix is False
        assert rec.status == "prefill_unavailable"


def test_t3_prepare_survives_source_value_pair(tmp_path):
    hot = tmp_path / "hot"
    msq = tmp_path / "msq"
    assert main(["prepare", "--kind", "hotpot", "--fixture", "tests/fixtures/t3_hotpot_one.json", "--out-dir", str(hot)]) == 0
    assert main(["prepare", "--kind", "t3_musique", "--fixture", "tests/fixtures/t3_musique_pair.json", "--out-dir", str(msq)]) == 0
    assert (hot / "tasks.jsonl").exists()
    assert (msq / "tasks.jsonl").exists()
    assert not any(row.get("kind") == "source_value_pair" for row in read_jsonl(hot / "edits.jsonl"))
    assert not any(row.get("kind") == "source_value_pair" for row in read_jsonl(msq / "edits.jsonl"))


def test_source_value_pair_rewrites_graph_ids(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    pair = make_source_value_pair(task, "p2", "2")
    sourced = pair["same_value_diff_source"].task
    assert "p2 = 0" in sourced.question
    assert "src_b = 0" in sourced.question
    assert sourced.nodes[0].expression == "p1 * src_b"
    assert {p.premise_id for p in sourced.premises} == {"p1", "p2", "src_b"}
    assert sourced.nodes[0].parents == ["p1", "src_b"]
    assert "p2" not in sourced.nodes[0].parents
    assert next(p.value for p in sourced.premises if p.premise_id == "p2") == next(
        p.value for p in sourced.premises if p.premise_id == "src_b"
    )
    assert sourced.answer_spec.value == task.answer_spec.value
    from reasoning_diff.models.generate import generate_task_trace

    src_trace = generate_task_trace(sourced, seed=0, weight_seed=0, run_id="trace-source")
    assert sourced.question == src_trace.metadata["prompt_text"]
    assert "* src_b" in src_trace.metadata["prompt_text"]
    assert src_trace.metadata["prompt_len"] == len(sourced.question)


def test_plus_locks_symbolic_family_to_test():
    clear_test_only_families()
    plus_record = {
        "id": "plus-1",
        "original_id": "gsm8k-1",
        "question": "Ada has 4 apples and buys 3 more. How many apples?",
        "answer": "7",
        "perturbation_type": "numerical substitution",
        "seed_question": "Ada has 4 apples and buys 3 more. How many apples?",
    }
    official_plus = {
        "question": "Ada has 4 apples and buys 3 more. How many apples?",
        "solution": "4+3=7",
        "answer": "7",
        "perturbation_type": "numerical substitution",
        "seed_question": "Ada has 4 apples and buys 3 more. How many apples?",
    }
    symbolic_record = {
        "id": "sym-1",
        "instance": 0,
        "question": "Ada has 4 apples and buys 3 more. How many apples?",
        "answer": "7",
        "original_id": "gsm8k-1",
        "original_question": "Ada has 4 apples and buys 3 more. How many apples?",
        "original_answer": "7",
    }
    from pathlib import Path
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as raw:
        root = Path(raw)
        (root / "plus.json").write_text(json.dumps(plus_record), encoding="utf-8")
        (root / "official.json").write_text(json.dumps(official_plus), encoding="utf-8")
        (root / "sym.json").write_text(json.dumps(symbolic_record), encoding="utf-8")
        plus = load_gsm_plus(root / "plus.json")
        symbolic = load_gsm_symbolic(root / "sym.json")
        assert split_for_task(plus) == "test"
        assert split_for_task(symbolic) == "test"
        assert split_for_task(symbolic, siblings=[plus]) == "test"
        clear_test_only_families()
        official = load_gsm_plus(root / "official.json")
        symbolic2 = load_gsm_symbolic(root / "sym.json")
        assert official.metadata["shared_gsm_text"] == symbolic2.metadata["shared_gsm_text"]
        assert split_for_task(symbolic2) == "test"
        _TEST_ONLY_FAMILY_KEYS.clear()
        assert split_for_task(symbolic2) == "test"
    clear_test_only_families()


def test_analyze_refuses_fake_p1_from_labels(tmp_path):
    src = tmp_path / "lab"
    src.mkdir()
    from reasoning_diff.io import write_jsonl

    write_jsonl(
        src / "labels.jsonl",
        [
            {"event_id": "q", "premise_id": "p1", "task_label": 1, "behavior_label": 0},
            {"event_id": "q", "premise_id": "p2", "task_label": 0, "behavior_label": 1},
            {"event_id": "q", "premise_id": "p3", "task_label": 1, "behavior_label": 0},
            {"event_id": "q", "premise_id": "p4", "task_label": 0, "behavior_label": 1},
        ],
    )
    out = tmp_path / "an"
    assert main(["analyze", "--in-dir", str(src), "--out-dir", str(out)]) == 0
    report = read_json(out / "report.json")
    assert report["p1"] is None
    assert report["scientific_conclusion"] is None


def test_common_dim_marks_truncated_when_n_lt_dim():
    a = np.ones((2, 5))
    b = np.ones((2, 3))
    out = common_dim_then_procrustes(a, b)
    assert out["truncated"] is True
    assert out["status"] == "not_applicable_too_few_rows"


def test_sham_hits_do_not_broadcast_real_premises_into_n(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    anc = ancestors(task)
    proto = {"name": "no_edit_matched", "hits": ["q"]}
    labels = build_labels(
        [
            Observation("o1", "tb", "te", "e1", "p1", ["q", "q"], "no_change", ["4", "4"], "q", "stream:0", "observed_response", False, "q"),
            Observation("o2", "tb", "te", "e1", "p2", ["q", "q"], "changed", ["0", "2"], "q", "stream:0", "observed_response", False, "q"),
            Observation("os", "tb", "ts", "sham:no_edit", "sham:q", ["q", "q"], "changed", ["82", "53"], "q", "sham:0", "observed_response", False, "q"),
        ],
        anc,
        sham_protocol=proto,
    )
    assert all(lab.noise_ref is None for lab in labels if lab.premise_id in {"p1", "p2"})
    assert any(lab.premise_id == "sham:q" and lab.noise_ref == 1.0 for lab in labels)
    dens = event_density_sets(task, labels, sham_protocol=proto)
    rows = dens.get("events") or []
    assert rows
    for row in rows:
        assert row.get("rho_M_excess") is None
        assert row.get("rho_S_excess") is None
        assert row.get("rho_M_noise") is None
        assert row.get("rho_S_noise") is None
        assert row.get("null_reason") == "noise_set_missing"


def _scientific_sham_lock(dens: dict) -> bool:
    if any(dens.get(key) is not None for key in ("rho_M_excess", "rho_S_excess", "rho_M_noise", "rho_S_noise")):
        return False
    events = dens.get("events") or []
    if not events:
        return False
    return all(
        row.get("rho_M_excess") is None
        and row.get("rho_S_excess") is None
        and row.get("rho_M_noise") is None
        and row.get("rho_S_noise") is None
        and row.get("null_reason") == "noise_set_missing"
        for row in events
    )


def test_scientific_sham_does_not_book_rho_m_excess_one(tmp_path, t1_tiny_path):
    prep = tmp_path / "prep"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *FRAC, "--sham-opportunities", "1"]) == 0
    dens = next(row["densities"] for row in read_jsonl(prep / "labels.jsonl") if "densities" in row)
    assert _scientific_sham_lock(dens)
    forged_zero = {**dens, "rho_M_excess": 0.0}
    forged_empty = {**dens, "events": []}
    forged_booked = {**dens, "events": [{**(dens["events"][0]), "rho_M_excess": 1.0, "null_reason": "noise_set_missing"}]}
    forged_no_reason = {**dens, "events": [{**(dens["events"][0]), "null_reason": None}]}
    assert not _scientific_sham_lock(forged_zero)
    assert not _scientific_sham_lock(forged_empty)
    assert not _scientific_sham_lock(forged_booked)
    assert not _scientific_sham_lock(forged_no_reason)
    weak = lambda d: d.get("rho_M_excess") != 1.0 or d.get("null_reason")
    assert weak(forged_zero)
    assert weak(forged_empty)
    labels = [row for row in read_jsonl(prep / "labels.jsonl") if row.get("premise_id") in {"p1", "p2"}]
    assert all(row.get("noise_ref") is None for row in labels)


def test_unknown_behavior_is_not_counted_as_m(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    labels = build_labels(
        [
            Observation("o1", "tb", "te", "e1", "p1", ["q", "q"], "no_change", ["4", "4"], "q", "stream:0", "unscanned", False, "q"),
            Observation("o2", "tb", "te", "e1", "p2", ["q", "q"], "no_change", ["0", "0"], "q", "stream:0", "unscanned", False, "q"),
        ],
        ancestors(task),
    )
    assert all(lab.behavior_known is False for lab in labels)
    dens = event_density_sets(task, labels)
    rows = dens.get("events") or [dens]
    assert all(row.get("rho_M_raw") is None for row in rows)
    assert all(row.get("M") == [] for row in rows)
    assert all(row.get("behavior_unknown") for row in rows)


def test_sham_no_change_does_not_book_empty_n(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    proto = {"name": "no_edit_matched", "hits": []}
    labels = build_labels(
        [
            Observation("o1", "tb", "te", "e1", "p2", ["q", "q"], "changed", ["0", "2"], "q", "stream:0", "observed_response", True, "q"),
            Observation("os", "tb", "ts", "sham:no_edit", "sham:q", ["q", "q"], "no_change", ["0", "0"], "q", "sham:0", "observed_response", False, "q"),
        ],
        ancestors(task),
        sham_protocol=proto,
    )
    assert any(lab.premise_id == "sham:q" and lab.noise_ref == 0.0 for lab in labels)
    dens = event_density_sets(task, labels, sham_protocol=proto)
    rows = dens.get("events") or []
    assert rows
    for row in rows:
        assert row.get("rho_M_excess") is None
        assert row.get("rho_S_excess") is None
        assert row.get("rho_M_noise") is None
        assert row.get("rho_S_noise") is None
        assert row.get("null_reason") == "noise_set_missing"


def test_observed_real_noise_ref_without_sham_does_not_book_empty_n(t1_tiny_path):
    from reasoning_diff.schema import Label

    task = load_t1_fixture(t1_tiny_path)
    proto = {"name": "no_edit_matched", "hits": []}
    labels = [
        Label("q", "p1", 1, True, 0, True, 0.0, "no_edit_matched"),
        Label("q", "p2", 1, True, 0, True, 0.0, "no_edit_matched"),
    ]
    dens = event_density_sets(task, labels, sham_protocol=proto)
    rows = dens.get("events") or []
    assert rows
    for row in rows:
        assert row.get("rho_M_excess") is None
        assert row.get("rho_S_excess") is None
        assert row.get("rho_M_noise") is None
        assert row.get("rho_S_noise") is None
        assert row.get("null_reason") == "noise_set_missing"


def test_c7_m01_mapped_noise_premise_is_deducted():
    out = dependency_densities(
        premises=["p1", "p2", "p3"],
        task_set={"p1", "p2"},
        behavior_set={"p1", "p2", "p3"},
        noise_set=["p3"],
        sham_protocol={"name": "no_edit_matched"},
        noise_evaluated=True,
    )
    assert out["rho_S_noise"] == 1.0
    assert out["rho_S_excess"] == 0.0


def test_review_export_can_merge_human_rows(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    event = Event(EventIdentity("q", 1), "9", 0, 1, 0, "q=9", node_id="q", record_id="r1")
    rows = review_export([event], task)
    assert rows[0]["review"] is None
    assert rows[0]["review_status"] == "awaiting_human"
    filled = merge_review(rows, [{"record_id": "r1", "review": "ok"}])
    assert filled[0]["review"] == "ok"
    assert filled[0]["review_status"] == "filled"


def test_load_source_value_pair_does_not_walk_sibling_prep(tmp_path):
    from reasoning_diff.cli import _load_source_value_pair

    col = tmp_path / "features"
    prep = tmp_path / "prep"
    prep.mkdir()
    col.mkdir()
    write_jsonl(prep / "edits.jsonl", [{"kind": "source_value_pair", "trace_ids": {"base": "trace-base", "same_value_diff_source": "trace-source"}}])
    assert _load_source_value_pair(col) is None


def test_rename_swap_is_simultaneous(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    swapped = apply_rename_edit(task, {"p1": "p2", "p2": "p1"}).task
    assert swapped.question == "p2 = 4. p1 = 0. What is q = p2 * p1?"
    assert swapped.nodes[0].expression == "p2 * p1"
    assert {p.premise_id for p in swapped.premises} == {"p1", "p2"}
    assert swapped.nodes[0].parents == ["p2", "p1"]
    assert next(p.value for p in swapped.premises if p.premise_id == "p2") == "4"
    assert next(p.value for p in swapped.premises if p.premise_id == "p1") == "0"


def test_tiny_prefix_ids_refuse_silent_truncate():
    from reasoning_diff.cli import _tiny_prefix_ids

    assert len(_tiny_prefix_ids("x" * 70)) == 70
    with pytest.raises(ValueError, match="refuse truncated"):
        _tiny_prefix_ids("x" * 97)


def test_intervene_cli_hook_ids_exceed_64(tmp_path, t1_tiny_path, monkeypatch):
    from reasoning_diff.models import collect as collect_mod

    seen: list[int] = []
    orig = collect_mod.intervene_hidden_decode

    def wrap(kind, prompt_ids, *args, **kwargs):
        seen.append(len(list(prompt_ids)))
        return orig(kind, prompt_ids, *args, **kwargs)

    monkeypatch.setattr(collect_mod, "intervene_hidden_decode", wrap)
    body = json.loads(Path(t1_tiny_path).read_text(encoding="utf-8"))
    question = body["question"]
    if len(question) < 70:
        body["question"] = question + ("x" * (70 - len(question)))
    fixture = tmp_path / "t1_70.json"
    fixture.write_text(json.dumps(body), encoding="utf-8")
    stage_a = tmp_path / "stage_a"
    stage_b = tmp_path / "stage_b"
    inter = tmp_path / "stage_c"
    assert main(["prepare", "--fixture", str(fixture), "--out-dir", str(stage_a), "--eval-mode", "scientific", "--split-fractions", *FRAC]) == 0
    traces = read_jsonl(stage_a / "traces.jsonl")
    assert min(len(row["metadata"]["prompt_text"]) for row in traces) >= 70
    assert main(["collect", "--fixture", str(fixture), "--in-dir", str(stage_a), "--out-dir", str(stage_b), "--eval-mode", "scientific", "--backend", "tiny", "--weight-seed", "0"]) == 0
    assert main(["intervene", "--in-dir", str(stage_b), "--out-dir", str(inter), "--backend", "tiny", "--dev-layer-scores", "0.05", "0.9", "0.8"]) == 0
    row = read_jsonl(inter / "interventions.jsonl")[0]
    assert seen
    assert all(n > 64 for n in seen)
    assert row.get("relative", {}).get("prefix_n") == seen[0]
    assert row.get("relative", {}).get("prefix_truncated") is False


def test_calibrate_cli_ignores_sibling_lab(tmp_path, t1_tiny_path, monkeypatch):
    from reasoning_diff import cli

    asked: list[list[str | None]] = []
    orig = cli._find_labels_jsonl

    def wrap(*dirs):
        asked.append([None if d is None else str(Path(d).resolve()) for d in dirs])
        return orig(*dirs)

    monkeypatch.setattr(cli, "_find_labels_jsonl", wrap)
    work = tmp_path / "run"
    prep = work / "stage_a"
    col = work / "stage_b"
    lab = work / "real_lab"
    fit = work / "fit"
    sibling = work / "lab"
    cal_sib = tmp_path / "cal_sib"
    cal_clear = tmp_path / "cal_clear"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(prep), "--eval-mode", "scientific", "--split-fractions", *FRAC]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(prep), "--out-dir", str(col), "--eval-mode", "scientific", "--backend", "tiny", "--weight-seed", "0"]) == 0
    assert main(["label", "--in-dir", str(prep), "--out-dir", str(lab)]) == 0
    assert main(["fit", "--in-dir", str(col), "--labels-dir", str(lab), "--out-dir", str(fit), "--split", "probe_train", "--eval-mode", "scientific"]) == 0
    sibling.mkdir()
    write_jsonl(sibling / "labels.jsonl", [{"premise_id": "WRONG", "task_label": 1, "behavior_label": 1, "event_id": "q"}])
    asked.clear()
    assert main(["calibrate", "--in-dir", str(fit), "--features-dir", str(col), "--out-dir", str(cal_sib), "--split", "calibration"]) == 0
    assert asked
    for call in asked:
        assert str(sibling.resolve()) not in call
        assert all(d in {None, str(fit.resolve()), str(col.resolve())} for d in call)
    (sibling / "labels.jsonl").unlink()
    asked.clear()
    assert main(["calibrate", "--in-dir", str(fit), "--features-dir", str(col), "--out-dir", str(cal_clear), "--split", "calibration"]) == 0
    assert read_jsonl(cal_sib / "calibration.jsonl") == read_jsonl(cal_clear / "calibration.jsonl")


def test_calibrate_does_not_bind_sibling_lab_labels(tmp_path):
    from reasoning_diff.cli import _find_labels_jsonl
    from reasoning_diff.io import write_jsonl

    feat = tmp_path / "features"
    sibling = tmp_path / "lab"
    feat.mkdir()
    sibling.mkdir()
    write_jsonl(sibling / "labels.jsonl", [{"premise_id": "WRONG", "task_label": 1}])
    assert _find_labels_jsonl(feat) is None
    assert _find_labels_jsonl(feat, sibling) == sibling / "labels.jsonl"


def test_intervene_pairs_source_without_prep_sibling_name(tmp_path, t1_tiny_path):
    stage_a = tmp_path / "stage_a"
    stage_b = tmp_path / "stage_b"
    inter = tmp_path / "stage_c"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(stage_a), "--eval-mode", "scientific", "--split-fractions", *FRAC, "--sham-opportunities", "1"]) == 0
    assert main(["collect", "--fixture", str(t1_tiny_path), "--in-dir", str(stage_a), "--out-dir", str(stage_b), "--eval-mode", "scientific", "--backend", "tiny", "--weight-seed", "0"]) == 0
    assert (stage_b / "edits.jsonl").exists()
    assert (stage_b / "edits.jsonl").read_bytes() == (stage_a / "edits.jsonl").read_bytes()
    assert main(["intervene", "--in-dir", str(stage_b), "--out-dir", str(inter), "--backend", "tiny", "--dev-layer-scores", "0.05", "0.9", "0.8"]) == 0
    row = read_jsonl(inter / "interventions.jsonl")[0]
    assert row["relative"].get("donor_kind") == "same_value_diff_source"


def test_model_card_pins_hidden_size_and_rejects_unknown():
    from reasoning_diff.models.adapters import card

    qwen = card("qwen3-8b")
    distill = card("r1-distill-qwen-7b")
    assert qwen["hidden_size"] == 4096
    assert distill["hidden_size"] == 3584
    assert qwen["revision"] != "latest"
    assert distill["revision"] != "latest"
    assert qwen["revision"] != distill["revision"]
    with pytest.raises(KeyError):
        card("not-a-registered-model")


def test_forbid_host_exec_never_calls_wrapped_fn():
    from reasoning_diff.executor import forbid_host_exec

    called = []

    def boom(*_args, **_kwargs):
        called.append(1)
        return 1

    wrapped = forbid_host_exec(boom)
    with pytest.raises(RuntimeError, match="host execution"):
        wrapped()
    assert called == []


def test_procrustes_recovers_known_rotation():
    from reasoning_diff.analysis import procrustes
    from reasoning_diff.transfer import apply_map

    rotation = np.array([[0.0, -1.0], [1.0, 0.0]])
    source = np.array([[1.0, 0.0], [0.0, 2.0], [1.0, 1.0]])
    target = source @ rotation
    fitted = procrustes(source, target)
    assert fitted["status"] == "adapted_geometry"
    assert np.allclose(fitted["R"], rotation)
    assert np.allclose(source @ fitted["R"], target)
    mapped = apply_map(source, {"W": fitted["R"]})
    assert np.allclose(mapped, target)
    assert procrustes(source, source[:, :1])["status"] == "not_applicable_shape_mismatch"


def test_attention_mean_uses_premise_indices_not_empty_zero():
    from reasoning_diff.baselines import attention_mean

    weights = np.array([[0.1, 0.8, 0.1]])
    assert attention_mean(weights, [1]) == pytest.approx(0.8)
    assert attention_mean(weights, [0, 2]) == pytest.approx(0.1)
    assert attention_mean(np.array([]), [1]) == 0.0
    assert attention_mean(weights, []) == 0.0


def test_apply_model_template_passes_thinking_only_for_qwen3():
    from reasoning_diff.models.generate import apply_model_template

    class _Tok:
        def __init__(self):
            self.kwargs = None

        def apply_chat_template(self, messages, **kwargs):
            self.kwargs = kwargs
            return np.zeros((1, 3))

    tok = _Tok()
    qwen3 = apply_model_template(tok, [{"role": "user", "content": "hi"}], "qwen3", enable_thinking=False)
    assert tok.kwargs["enable_thinking"] is False
    assert qwen3["enable_thinking"] is False
    assert qwen3["prompt_len"] == 3
    tok2 = _Tok()
    apply_model_template(tok2, [{"role": "user", "content": "hi"}], "qwen2", enable_thinking=True)
    assert "enable_thinking" not in tok2.kwargs
