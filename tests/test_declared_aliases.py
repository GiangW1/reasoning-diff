from pathlib import Path

import pytest

from reasoning_diff.events import assign_event_regions, parse_events
from reasoning_diff.next_round import sentence_graph_task
from reasoning_diff.tasks.t1_official import load_igsm_snapshot


@pytest.fixture
def task():
    path = Path(__file__).resolve().parents[1] / "artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200/igsm-official-0045-op10.json"
    return sentence_graph_task(load_igsm_snapshot(path))


@pytest.mark.parametrize("declaration,symbol", [
    ("- Rucksack (AS_R)", "AS_R"),
    ("- Rucksack: A_R", "A_R"),
    ("- Rucksack (let's denote this as AS_R)", "AS_R"),
    ("- Rucksack: Let's denote this as A_R", "A_R"),
    ("- Rucksack: A_{R}", "A_{R}"),
    ("- Let R = number of Rucksack", "R"),
    ("- R = the number of Rucksack.", "R"),
])
def test_explicit_scoped_alias_resolves_calculation_with_exact_offsets(task, declaration, symbol):
    text = f"For Aerobics Studio:\n{declaration}\n{symbol} = 7 * 7 = 49.\nTherefore, {symbol} = 3 mod 23."
    events = parse_events(text, task)
    assign_event_regions(events, text, initial_thinking=True)
    assert [(e.node_id, e.value, e.event_kind) for e in events] == [
        ("p_0_0_0_2", "49", "calculation"), ("p_0_0_0_2", "3", "commit")]
    assert all(e.event_region == "thinking" for e in events)
    assert all(text[e.start:e.end] == e.text and text[e.value_start:e.end] == e.value for e in events)


def test_scopes_disambiguate_same_item_and_preserve_entity_identity(task):
    text = "For Aerobics Studio:\n- Backpacking Pack: A_B\nFor Badminton Court:\n- Backpacking Pack: B_B\nA_B = 3.\nB_B = 20."
    assert [(e.node_id, e.value) for e in parse_events(text, task)] == [("p_0_0_0_0", "3"), ("p_0_0_1_0", "20")]


def test_alias_definition_in_future_does_not_label_earlier_assignment(task):
    text = "X = 3.\nFor Aerobics Studio:\n- Rucksack: X\nX = 4."
    events = parse_events(text, task)
    assert [e.value for e in events] == ["4"]
    assert events[0].start == text.rfind("X")


def test_conflicting_or_undeclared_aliases_remain_unresolved(task):
    text = "For Aerobics Studio:\n- Backpacking Pack: X\nFor Badminton Court:\n- Backpacking Pack: X\nX = 20.\nUndeclared = 3."
    assert parse_events(text, task) == []


def test_short_item_without_scope_cannot_be_guessed_from_value(task):
    assert parse_events("- Backpacking Pack: X\nX = 3.", task) == []


def test_full_entity_can_be_declared_without_heading(task):
    text = "- Aerobics Studio's Rucksack: X\nX = 3."
    assert [(e.node_id, e.value) for e in parse_events(text, task)] == [("p_0_0_0_2", "3")]


@pytest.mark.parametrize("declaration", [
    "- Aerobics Studio's Rucksack (AS_R) = 7 * 7 = 49.",
    "- Aerobics Studio Rucksack (AS_R) = AS_M * 7 = 49.",
    "So, Aerobics Studio Rucksack (AS_R) = AS_M = 49.",
])
def test_inline_alias_declaration_preserves_committed_result_and_offsets(task, declaration):
    text = declaration + "\nTherefore, AS_R = 3 mod 23."
    events = parse_events(text, task)
    assert [(e.node_id, e.value) for e in events] == [("p_0_0_0_2", "49"), ("p_0_0_0_2", "3")]
    assert all(text[e.start:e.end] == e.text and text[e.value_start:e.end] == e.value for e in events)


def test_inline_alias_does_not_apply_to_earlier_assignments(task):
    text = "X = 3.\n- Aerobics Studio Rucksack (X) = M = 4."
    events = parse_events(text, task)
    assert [(e.node_id, e.value) for e in events] == [("p_0_0_0_2", "4")]
    assert events[0].start > text.index("\n")


@pytest.mark.parametrize("rhs", ["M and X = 3", "M = 3 + 4", "M + 3", "lookup(M) = 3"])
def test_symbolic_rhs_requires_one_explicit_unambiguous_numeric_result(task, rhs):
    text = f"For Aerobics Studio:\n- Rucksack: AS_R\nAS_R = {rhs}."
    assert parse_events(text, task) == []


def test_possessive_normalization_cannot_choose_between_two_entities(task):
    from reasoning_diff.schema import Task
    altered = task.to_dict()
    next(node for node in altered["nodes"] if node["id"] != "p_0_0_0_2")["aliases"] = ["Aerobics Studio Rucksack"]
    ambiguous = Task.from_dict(altered)
    assert parse_events("- Aerobics Studio Rucksack (X) = 3.", ambiguous) == []


@pytest.mark.parametrize("later", [
    "The number of Aerobics Studio's Rucksack equals a product. Let me denote this as X = 4.",
    "Let X be Aerobics Studio's Rucksack. X = 4.",
    "Aerobics Studio's Rucksack (X) = 4.",
])
def test_repeated_later_declaration_preserves_earliest_explicit_binding(task, later):
    text = "X = 999.\nThe number of Aerobics Studio's Rucksack equals a product. Let me write that as:\n\nX = 3.\n" + later
    events = parse_events(text, task)
    assert [e.value for e in events] == ["3", "4"]
    assert events[0].start == text.index("X = 3")


@pytest.mark.parametrize("intro", ["", "Let's call this ", "Let's denote this as "])
def test_entity_colon_declarations_without_bullets(task, intro):
    text = f"Aerobics Studio's Rucksack: {intro}X = 3.\nX = 4."
    events = parse_events(text, task)
    assert [(e.node_id, e.value) for e in events] == [("p_0_0_0_2", "3"), ("p_0_0_0_2", "4")]
    assert all(text[e.start:e.end] == e.text and text[e.value_start:e.end] == e.value for e in events)


def test_two_aliases_for_one_printed_result_are_one_event(task):
    text = "- Aerobics Studio's Rucksack: X = 3."
    events = parse_events(text, task)
    assert len(events) == 1 and events[0].value == "3"
    assert events[0].start == text.index("Aerobics")
