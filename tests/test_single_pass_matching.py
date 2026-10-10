from dataclasses import replace

import pytest

from reasoning_diff.events import align_events, assign_event_regions, parse_events
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.schema import Node


def parsed(text, task):
    return assign_event_regions(parse_events(text, task), text, initial_thinking=True)


@pytest.mark.parametrize('intro', ['Let me write that:', 'Let us write this:', "Let's note this:"])
def test_explicit_topic_notation_without_as_is_bound_at_its_first_use(t1_tiny_path, intro):
    task = load_t1_fixture(t1_tiny_path)
    task.nodes[-1].aliases = ['q', "Studio's Total"]
    text = f"X = 999.\nThe number of Studio's Total equals a sum. {intro}\n\nX = 7.\nX = 8."
    events = parsed(text, task)
    assert [(e.node_id, e.value) for e in events] == [('q', '7'), ('q', '8')]
    assert all(text[e.start:e.end] == e.text and text[e.value_start:e.end] == e.value for e in events)


def test_explicit_notation_cannot_inherit_a_topic_across_a_paragraph(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    task.nodes[-1].aliases = ['q', "Studio's Total"]
    text = "The number of Studio's Total equals a sum.\n\nLet me write that:\nX = 7."
    assert parsed(text, task) == []


def test_rhs_only_unambiguous_abbreviation_has_the_same_printed_source(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    task.premises[0].text = "The number of Alpha Studio's Rucksack equals 2."
    task.premises[0].kind = 'sentence'
    task.premises[0].start, task.premises[0].end = 0, len(task.premises[0].text)
    left = parsed("q = AS_R = 2.", task)
    right = parsed("q = Alpha Studio's Rucksack = 3.", task)
    assert len(left) == len(right) == 1
    assert left[0].expression_signature == right[0].expression_signature
    assert len(align_events(left, right)['pairs']) == 1
    assert len(align_events(left, [replace(right[0], value='999', correct=False)])['pairs']) == 1


def test_rhs_abbreviation_does_not_choose_between_two_entities(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    task.premises[0].text = "The number of Alpha Studio's Rucksack equals 2."
    task.premises[1].text = "The number of Alpha Studio's Ribbons equals 3."
    for premise in task.premises:
        premise.kind = 'sentence'
        premise.start, premise.end = 0, len(premise.text)
    left = parsed('q = AS_R = 2.', task)
    right = parsed("q = Alpha Studio's Rucksack = 2.", task)
    assert left and 'unresolved:' in left[0].expression_signature
    assert not align_events(left, right)['pairs']


def test_explicit_operations_on_different_entities_can_change_written_order(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    task.nodes.append(Node('r', ['p1', 'p2'], '0', ['r'], 'p1 * p2'))
    left = parsed('q = p1 + p2 = 4.\nr = p1 * p2 = 0.', task)
    right = parsed('r = p1 * p2 = 8.\nq = p1 + p2 = 6.', task)
    result = align_events(left, right)
    assert {(a.node_id, b.node_id) for a, b in result['pairs']} == {('q', 'q'), ('r', 'r')}
    assert all(c['recovery'] == 'entity_local_explicit_operation' for c in result['pair_certificates'])
    altered = [replace(e, value='999', correct=False, task_parents=['fake']) for e in right]
    assert [(a.identity, b.identity) for a, b in result['pairs']] == [
        (a.identity, b.identity) for a, b in align_events(left, altered)['pairs']]


def test_local_recovery_keeps_same_entity_reversed_stages_unknown(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = parsed('q = p1 + p2 = 4.\nq = p1 * p2 = 0.', task)
    right = parsed('q = p1 * p2 = 8.\nq = p1 + p2 = 6.', task)
    assert not align_events(left, right)['pairs']


def test_local_recovery_cannot_resolve_duplicate_operations_by_count_or_value(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = parsed('q = p1 + p2 = 4.\nq = p1 + p2 = 5.', task)
    right = parsed('q = p1 + p2 = 4.', task)
    assert not align_events(left, right)['pairs']


def test_local_recovery_respects_existing_same_entity_anchors(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    task.nodes.append(Node('r', ['p1', 'p2'], '0', ['r'], 'p1 * p2'))
    left = parsed('q = p1 + p2 = 4.\nr = p1 * p2 = 0.\nq = 4.', task)
    right = parsed('q = 4.\nr = p1 * p2 = 0.\nq = p1 + p2 = 4.', task)
    result = align_events(left, right)
    q_pairs = [(a.start, b.start) for a, b in result['pairs'] if a.node_id == 'q']
    assert len(q_pairs) <= 1
