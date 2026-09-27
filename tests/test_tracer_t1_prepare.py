from pathlib import Path

from reasoning_diff.cli import main
from reasoning_diff.edits import apply_value_edit
from reasoning_diff.events import align_events, parse_fixture_events
from reasoning_diff.graphs import ancestors
from reasoning_diff.io import read_json, read_jsonl
from reasoning_diff.measure import dependency_densities, lcs_overlap, preservation_to_csp
from reasoning_diff.schema import EventIdentity, SOURCE_KINDS, SPLIT_ROLES, Task
from reasoning_diff.splits import assign_split, assert_same_role
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def test_enums_and_identity_exclude_values():
    assert "probe_train" in SPLIT_ROLES
    assert "transfer_pairs" in SPLIT_ROLES
    assert "train" not in SPLIT_ROLES
    assert "fixture" in SOURCE_KINDS and "official" in SOURCE_KINDS
    key = EventIdentity("p1 * p2", 1, "global").key()
    assert "4" not in key and "0" not in key


def test_fixture_is_never_official(t1_tiny_path):
    raw = read_json(t1_tiny_path)
    assert raw["source_kind"] == "fixture"
    task = load_t1_fixture(t1_tiny_path)
    assert task.source_kind == "fixture"
    assert task.graph_status == "complete"
    assert ancestors(task)["q"] == {"p1", "p2"}


def test_value_edit_recomputes_expression(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    edited = apply_value_edit(task, "p1", "7")
    assert edited.task.source_kind == "fixture"
    assert edited.task.premises[0].value == "7"
    assert edited.task.answer_spec.value == "0"
    assert edited.task.nodes[0].value == "0"


def test_split_roles_cohere():
    role = assign_split("fix-t1-001")
    assert role in SPLIT_ROLES
    assert assign_split("fix-t1-001") == role
    assert_same_role({"base": role, "edit": role, "seed1": role})


def test_identity_alignment_ignores_values(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    a = parse_fixture_events("q = 0\n", task)
    b = parse_fixture_events("q = 1\n", task)
    pairs = align_events(a, b)["pairs"]
    assert len(pairs) == 1
    assert a[0].identity == b[0].identity
    assert a[0].value != b[0].value


def test_pitfalls_densities_and_null_excess():
    result = dependency_densities(
        premises=["p1", "p2", "p3", "p4"],
        task_set=["p1", "p2"],
        behavior_set=["p2", "p3"],
    )
    assert result["S"] == ["p3"]
    assert result["M"] == ["p1"]
    assert result["rho_S_raw"] == 0.5
    assert result["rho_M_raw"] == 0.5
    assert result["rho_S_excess"] is None
    assert result["null_reason"] == "sham_protocol_missing"
    signed = dependency_densities(
        premises=["p1", "p2", "p3", "p4"],
        task_set=["p1", "p2"],
        behavior_set=["p2", "p3"],
        noise_set=["p2", "p3", "p4"],
        sham_protocol={"name": "matched_opportunities", "opportunities": 1},
    )
    assert signed["rho_S_excess"] == -0.5


def test_to_empty_is_null():
    assert lcs_overlap([], []) is None
    assert lcs_overlap([1, 2], [1, 3]) == 0.5


def test_prepare_cli(tmp_path, t1_tiny_path):
    out = tmp_path / "run"
    assert main(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(out)]) == 0
    tasks = read_jsonl(out / "tasks.jsonl")
    assert tasks[0]["source_kind"] == "fixture"
    assert all(row["source_kind"] != "official" for row in tasks)
    splits = read_jsonl(out / "splits.jsonl")
    assert splits[0]["role"] in SPLIT_ROLES
    labels = read_jsonl(out / "labels.jsonl")
    dens = next(row["densities"] for row in labels if "densities" in row)
    assert dens["rho_S_excess"] is None
    spec = read_json(out / "run_spec.json")
    assert spec["source_kinds"][Path(t1_tiny_path).name] == "fixture"
    manifest = read_json(out / "manifest.json")
    assert "digest" in manifest
    assert "run_spec.json" in manifest["file_hashes"]
