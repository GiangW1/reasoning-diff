"""Real PR8 expression forms and measurement failure regressions; no model runs."""
from pathlib import Path
import json

import pytest

from reasoning_diff import cli
from reasoning_diff.events import align_events, assign_event_regions, parse_events
from reasoning_diff.next_round import sentence_graph_task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t1_official import load_igsm_snapshot


def thinking(text, task):
    events = parse_events(text, task)
    return assign_event_regions(events, text, initial_thinking=True)


def test_answer_repetition_does_not_remove_identical_thinking(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = thinking("q = 7\n</think>\nq = 7", task)
    right = thinking("q = 7\n</think>\n7", task)
    pairs = align_events(left, right)["pairs"]
    assert len(pairs) == 1
    assert pairs[0][0].event_region == pairs[0][1].event_region == "thinking"


def test_equal_counts_never_pair_thinking_with_answer(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = thinking("q = 2\nq = 7\n</think>\n7", task)
    right = thinking("q = 2\n</think>\nq = 8", task)
    assert all(a.event_region == b.event_region for a, b in align_events(left, right)["pairs"])


def test_unique_calculation_survives_extra_scalar_confirmation(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = thinking("q = 2 * 3 = 6\nq = 6", task)
    right = thinking("q = 2 * 4 = 8\nq = 8\nq = 8", task)
    pairs = align_events(left, right)["pairs"]
    assert [(a.value, b.value) for a, b in pairs] == [("6", "8")]
    assert align_events(left, right)["structural"]["ambiguous"]


def test_repeated_indistinguishable_steps_stay_unknown(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = thinking("q = 7\nq = 7", task)
    right = thinking("q = 7\nq = 7", task)
    assert align_events(left, right)["pairs"] == []


@pytest.mark.parametrize("text,value", [
    ("q = 7 + p1 = 7 + 2 = 9.", "9"),
    ("q = p1 * p2 = 9 * 2 = 18.", "18"),
    ("q = 3 * (p1 - p2) = 3*(18 - 2) = 3*16 = 48.", "48"),
    ("q = (15 + 10) mod 23 = 25 mod 23 = 2", "2"),
    ("q = (2 + 3) = 5", "5"),
    ("q = p1 \\times p2 = 3 \\times 2 = 6 $", "6"),
])
def test_multistage_equations_read_only_explicit_terminal_scalar(t1_tiny_path, text, value):
    event = parse_events(text, load_t1_fixture(t1_tiny_path))[0]
    assert event.value == value
    assert text[event.value_start:event.end] == value
    assert text[event.start:event.end] == event.text
    assert event.expression_signature


@pytest.mark.parametrize("text", ["q = p1 = 3 + 4", "q = 2 + 3", "q = lookup(p1) = 3", "q = p1 and p2 = 3", "q = 25 mod 23", "q = 1/0 mod 23"])
def test_uncommitted_or_unsupported_expression_is_not_guessed(t1_tiny_path, text):
    assert parse_events(text, load_t1_fixture(t1_tiny_path)) == []


@pytest.mark.parametrize("text", ["q = 3 mod 23", "q = 3 (mod 23)"])
def test_printed_residue_annotation_remains_scalar_commit(t1_tiny_path, text):
    event = parse_events(text, load_t1_fixture(t1_tiny_path))[0]
    assert (event.value, event.event_kind, event.event_phase) == ("3", "commit", "commit")


@pytest.mark.parametrize("relation", ["≡", r"\equiv"])
def test_explicit_congruence_chain_reads_printed_residue(t1_tiny_path, relation):
    text = f"q = 20 * 5 = 100 {relation} 8 (mod 23)."
    event = parse_events(text, load_t1_fixture(t1_tiny_path))[0]
    assert (event.value, event.event_kind, event.event_phase) == ("8", "calculation", "reduction")
    assert text[event.value_start:event.end] == "8"
    assert text[event.start:event.end] == event.text


@pytest.mark.parametrize("rhs", ["100 ≡ 3 + 5", r"100 \equiv 3 + 5", "100 ≡ 31 mod 23"])
def test_congruence_never_computes_an_unprinted_residue(t1_tiny_path, rhs):
    assert parse_events("q = " + rhs, load_t1_fixture(t1_tiny_path)) == []


@pytest.fixture
def official_task():
    root = Path(__file__).resolve().parents[1]
    path = root / "artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200/igsm-official-0003-op21.json"
    return sentence_graph_task(load_igsm_snapshot(path))


@pytest.mark.parametrize("declaration", [
    "Let me denote Secondary Forest's Organs as SF_O.",
    "Let SF_O be Secondary Forest's Organs.",
    "Let me denote SF_O as Secondary Forest's Organs.",
    "The number of Secondary Forest's Organs equals the product of two quantities. So SF_O = 18.",
])
def test_real_pr8_prose_declarations_map_without_gold_values(official_task, declaration):
    text = declaration + "\nSF_O = X * Y = 9 * 2 = 18."
    events = parse_events(text, official_task)
    assert events and events[-1].value == "18"
    expected = next(n.id for n in official_task.nodes if "Secondary Forest's Organs" in n.aliases)
    assert events[-1].node_id == expected


def test_later_answer_alias_does_not_resolve_earlier_thinking(official_task):
    text = "SF_O = 18.\n</think>\nLet SF_O be Secondary Forest's Organs.\nSF_O = 18."
    events = thinking(text, official_task)
    assert events and all(e.event_region == "answer" for e in events)


@pytest.mark.parametrize("declaration", [
    "- SF_O = Secondary Forest's Organs",
    "Number of Secondary Forest's Organs = a product. So, SF_O = 18.",
    "Number of Secondary Forest's Organs equals a product. Therefore, SF_O = 18.",
])
def test_additional_saved_pr8_declarations(official_task, declaration):
    events = parse_events(declaration + "\nSF_O = 18.", official_task)
    assert events and events[-1].value == "18"
    assert "Secondary Forest's Organs" in next(n.aliases for n in official_task.nodes if n.id == events[-1].node_id)


@pytest.mark.parametrize("text", ["sum of p1 and q = 2 + 18 = 20", "Then add q: 22 + 2 = 24", "p1 * q = 2 * 3 = 6"])
def test_operand_mentions_are_not_assignment_heads(t1_tiny_path, text):
    assert not any(e.node_id == "q" for e in parse_events(text, load_t1_fixture(t1_tiny_path)))


@pytest.mark.parametrize("marker", ["- ", "* ", "+ ", "• ", "  - ", "\t* "])
def test_markdown_bullet_is_not_an_operand_operator(t1_tiny_path, marker):
    text = marker + "q = 2 * 3 = 6"
    events = parse_events(text, load_t1_fixture(t1_tiny_path))
    assert len(events) == 1
    event = events[0]
    assert (event.node_id, event.value, event.event_phase) == ("q", "6", "calculation")
    assert event.start == len(marker) and text[event.value_start:event.end] == "6"


@pytest.mark.parametrize("text", [
    "- Let **SF_O** = Secondary Forest's Organs\n**SF_O** = 9 * 2 = 18.",
    "- SF_O = number of Secondary Forest's Organs = X * Y\nSF_O = 9 * 2 = 18.",
    "The number of Secondary Forest's Organs equals a product. Let me write that as:\n\nSF_O = X * Y\nSF_O = 9 * 2 = 18.",
    "Secondary Forest's Organs = a product. So:\n\nSF_O = X * Y\nSF_O = 9 * 2 = 18.",
])
def test_saved_edit_notation_and_markdown_forms(official_task, text):
    events = thinking(text, official_task)
    assert events and events[-1].value == "18"
    expected = next(n.id for n in official_task.nodes if "Secondary Forest's Organs" in n.aliases)
    assert events[-1].node_id == expected
    assert text[events[-1].start:events[-1].end] == events[-1].text


def test_formatting_mask_preserves_arithmetic_power_operators(t1_tiny_path):
    text = "q = 2**3**2 = 512"
    events = thinking(text, load_t1_fixture(t1_tiny_path))
    assert len(events) == 1 and events[0].value == "512"
    assert "Pow" in events[0].expression_signature


@pytest.mark.parametrize("text", [
    "Secondary Forest's Organs = a product.\n\nSo SF_O = 18.",
    "X = Secondary Forest's Organs = 18. So SF_O = 18.",
])
def test_new_notation_does_not_inherit_distant_or_rhs_topic(official_task, text):
    assert not any("SF_O" in event.text for event in thinking(text, official_task))


def test_saved_bulleted_declaration_pair_resolves_same_operand(official_task):
    fixture = json.loads((Path(__file__).parent / "fixtures/pr8_bulleted_declaration_pair.json").read_text(encoding="utf-8"))
    expected = next(n.id for n in official_task.nodes if "Riparian Forest's Seahorse" in n.aliases)
    traces = [thinking(case["text"], official_task) for case in fixture["cases"]]
    events = [[event for event in parsed if event.node_id == expected] for parsed in traces]
    assert all(len(parsed) == 1 for parsed in events)
    assert events[0][0].expression_signature == events[1][0].expression_signature
    assert "unresolved:" not in events[0][0].expression_signature
    assert any(left.node_id == expected for left, right in align_events(*traces)["pairs"])


def test_scientific_observations_reject_failed_comparison_boundary(t1_tiny_path):
    from reasoning_diff.edits import apply_value_edit
    task = load_t1_fixture(t1_tiny_path)
    edit = apply_value_edit(task, "p1", "2")
    left = cli._synthetic_trace(task, "q = 7", "base", 0)
    right = cli._synthetic_trace(edit.task, "q = 8", "edit", 0)
    left.metadata["boundary_status"] = "ok"
    right.metadata["boundary_status"] = "failed"
    rows = cli._observations(task, left, right, edit, "stream:0", "check")
    assert rows and not any(r.outcome in {"changed", "no_change"} for r in rows)


def test_noise_compares_same_regions_and_step_phases(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = cli._synthetic_trace(task, "q = 7", "base", 0)
    right = cli._synthetic_trace(task, "q = 8", "noise", 1)
    left.events[0].event_region = "thinking"
    right.events[0].event_region = "answer"
    assert cli._sham_observations(task, left, right, 1, "noise") == []


SAVED_AUDIT = json.loads((Path(__file__).parent / "fixtures/pr8_saved_excerpt_audit.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", SAVED_AUDIT["cases"], ids=lambda case: case["id"])
def test_manually_annotated_saved_pr8_excerpts(case):
    root = Path(__file__).resolve().parents[1]
    task = sentence_graph_task(load_igsm_snapshot(root / "artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200"
                                                / f"{case['task_id']}.json"))
    text = case["context"] + case["text"]
    events = [event for event in thinking(text, task) if event.start >= len(case["context"])]
    expected = [(next(n.id for n in task.nodes if annotation["node_alias"] in n.aliases),
                 annotation["value"], annotation["event_phase"], annotation["event_kind"], annotation["text"])
                for annotation in case["expected"]]
    assert [(e.node_id, e.value, e.event_phase, e.event_kind, e.text) for e in events] == expected
    assert all(text[e.start:e.end] == e.text and text[e.value_start:e.end] == e.value for e in events)
    # Change the gold values while preserving names: matching and extraction
    # must not obtain an entity or a computed value from the answer key.
    for node in task.nodes:
        node.value = "999"
    assert [(e.node_id, e.value, e.expression_signature) for e in thinking(text, task) if e.start >= len(case["context"])] == [
        (e.node_id, e.value, e.expression_signature) for e in events]
