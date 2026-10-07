from dataclasses import replace
from pathlib import Path

import pytest

from reasoning_diff.events import align_events, assign_event_regions, parse_events
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t1_official import load_igsm_snapshot
from reasoning_diff.next_round import sentence_graph_task


def events(text, task):
    return assign_event_regions(parse_events(text, task), text, initial_thinking=True)


@pytest.mark.parametrize('text', [
    'q = 8 * 6 = 48 mod23=2.',
    'q = 48 mod23=48-2*23=48-46=2.',
    'q = 48 mod 23 = 2.',
])
def test_spaced_and_adjacent_modulus_keep_explicit_residue(t1_tiny_path, text):
    parsed = events(text, load_t1_fixture(t1_tiny_path))
    assert len(parsed) == 1
    assert parsed[0].value == '2' and parsed[0].event_phase == 'reduction'
    assert text[parsed[0].value_start:parsed[0].end] == '2'


@pytest.mark.parametrize('left,right', [
    ('q = p1 + p2 = 2 + 3 = 5', 'q = 2 + 4 = 6'),
    ('q = p1 + p2 = 2 + 3 = 5', 'q = p2 + p1 = 4 + 2 = 6'),
    ('q = (p1 + p2) + 3 = 8', 'q = p1 + (p2 + 4) = 9'),
])
def test_printed_equation_views_resolve_same_operation(t1_tiny_path, left, right):
    task = load_t1_fixture(t1_tiny_path)
    aa, bb = events(left, task), events(right, task)
    pairs = align_events(aa, bb)['pairs']
    assert len(pairs) == 1
    changed = [replace(e, value='99999', correct=False, task_parents=['wrong']) for e in bb]
    assert [(a.identity, b.identity) for a,b in pairs] == [(a.identity,b.identity) for a,b in align_events(aa, changed)['pairs']]


@pytest.mark.parametrize('left,right', [
    ('q = p1 + p2 = 2 + 3 = 5', 'q = p1 + other = 2 + 4 = 6'),
    ('q = p1 - p2 = 2 - 3 = -1', 'q = p2 - p1 = 3 - 2 = 1'),
    ('q = p1 * p2 = 2 * 3 = 6', 'q = p1 + p2 = 2 + 3 = 5'),
])
def test_different_named_operands_or_operations_never_match_through_numbers(t1_tiny_path, left, right):
    task = load_t1_fixture(t1_tiny_path)
    assert align_events(events(left, task), events(right, task))['pairs'] == []


@pytest.fixture
def forest_task():
    path = Path(__file__).resolve().parents[1] / 'artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200/igsm-official-0003-op21.json'
    return sentence_graph_task(load_igsm_snapshot(path))


def test_topic_does_not_turn_partial_sum_into_named_entity(forest_task):
    text = "Starfish's Nasal Cavity equals a sum of several quantities. So:\n\nSum1 = 1 + 8 = 9.\nStarfish_Nasal = 8."
    parsed = events(text, forest_task)
    assert not any('Sum1' in e.text for e in parsed)
    assert len(parsed) == 1 and parsed[0].value == '8'
    assert parsed[0].node_id == next(n.id for n in forest_task.nodes if "Starfish's Nasal Cavity" in n.aliases)


def test_unique_lexical_abbreviation_needs_no_later_declaration(forest_task):
    parsed = events('SF_O = 9 * 2 = 18.\nRF_Coral = 3 * (8 - 2) = 18.', forest_task)
    assert [e.node_id for e in parsed] == [next(n.id for n in forest_task.nodes if name in n.aliases)
                                         for name in ("Secondary Forest's Organs", "Riparian Forest's Coral")]
    assert events('S = 18.\nX = 18.\nSum1 = 18.', forest_task) == []


def test_add_operand_label_is_not_an_assignment(forest_task):
    assert events('Then add Starfish_PC: 22 + 2 = 24.', forest_task) == []


def test_lexical_binding_is_independent_of_later_declarations(forest_task):
    first = events('SF_O = 18.', forest_task)
    later = events('SF_O = 18.\nLet SF_O be Secondary Forest\'s Organs.\nSF_O = 19.', forest_task)
    assert [(e.node_id,e.value) for e in first] == [(e.node_id,e.value) for e in later[:1]]


def test_matching_uses_value_masked_discourse_context(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = events('Checking multiplication again.\nq = 6.', task)
    right = events('Initial result.\nq = 999.\n\nChecking multiplication again.\nq = 8.', task)
    pairs = align_events(left, right)['pairs']
    assert [(a.value,b.value) for a,b in pairs] == [('6','8')]
    # Masked numbers cannot change the selected occurrence.
    altered = events('Initial result.\nq = 6.\n\nChecking multiplication again.\nq = 10000.', task)
    assert [(a.identity,b.identity) for a,b in pairs] == [(a.identity,b.identity) for a,b in align_events(left, altered)['pairs']]


def test_indistinguishable_discourse_does_not_create_a_tie_break(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = events('Checking multiplication again.\nq = 6.', task)
    right = events('Checking multiplication again.\nq = 8.\n\nChecking multiplication again.\nq = 8.', task)
    assert align_events(left,right)['pairs'] == []


def test_camel_case_name_initials_and_unique_word_prefixes():
    from reasoning_diff.events import _abbreviates
    assert _abbreviates('FD_GC', "FreshDirect's Gummy Candy")
    assert _abbreviates('OC_Ingredient', "Ocado's Ingredient")
    assert not _abbreviates('Sum1', "Starfish's Nasal Cavity")


def test_context_keeps_other_quantity_identity_without_its_value(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = events('Checking p1 arithmetic again.\nq = 6.', task)
    right = events('Checking p2 arithmetic again.\nq = 6.\n\nChecking p1 arithmetic again.\nq = 8.', task)
    assert [(a.value,b.value) for a,b in align_events(left,right)['pairs']] == [('6','8')]


def test_sentence_graph_natural_prompt_keeps_single_pass_instruction(t1_tiny_path):
    from reasoning_diff.models.generate import task_prompt
    from reasoning_diff.quantity_steps import controlled_task
    from reasoning_diff.schema import Task
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    prompt = task_prompt(task)
    assert task.metadata['natural_prompt_policy'] == 'single_pass_named_results_v1'
    assert 'Do not restart' in prompt and 'quantity names' in prompt
    assert '<step' not in prompt and 'NODE_ID' not in prompt
    original = task.to_dict()
    original['metadata'].pop('natural_prompt_policy')
    assert task_prompt(Task.from_dict(original)) == task.question
    assert 'Do not restart' not in task_prompt(controlled_task(task))


def test_ambiguous_abbreviation_cannot_inherit_an_unrelated_topic():
    path = Path(__file__).resolve().parents[1] / 'artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200/igsm-official-0045-op10.json'
    task = sentence_graph_task(load_igsm_snapshot(path))
    text = "Swimming Pool's Mountaineering Backpack equals a difference. Then AS_B = 7."
    assert not any(e.node_id == next(n.id for n in task.nodes if "Swimming Pool's Mountaineering Backpack" in n.aliases)
                   for e in events(text, task))


def test_measurement_rejects_mixed_natural_prompt_conditions(t1_tiny_path):
    from reasoning_diff.next_round import measurement_report
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    rows = [{"id": f"base{seed}", "task_id": task.task_id, "seed": seed, "events": [],
             "status": "natural_complete", "metadata": {"natural_prompt_policy": policy}}
            for seed, policy in enumerate(('legacy', 'single_pass_named_results_v1'))]
    report = measurement_report(rows, [task.to_dict()], [], [])
    assert not report['checks']['generation_condition_homogeneous']
    assert not report['checks']['prompt_policy_matches_task']
    assert report['natural_prompt_policies'] == ['legacy', 'single_pass_named_results_v1']


def test_scalar_residue_annotation_is_not_a_raw_value_stage(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    raw = events('q is 32.', task)
    residue = events('q = 9 mod 23.', task)
    assert align_events(raw, residue)['pairs'] == []
    # Stage selection depends on printed notation, not whether the value
    # happens to be in the residue range.
    assert align_events(events('q is 9.', task), residue)['pairs'] == []
    assert len(align_events(events('q = 8 (mod 23).', task), residue)['pairs']) == 1


@pytest.mark.parametrize('declaration', [
    "(let's denote this as X)", "(let's call this X)",
    "(which is the quantity we need to find, let's denote this as X)",
])
def test_inline_parenthetical_alias_before_prose_predicate(forest_task, declaration):
    text = f"The number of Starfish's Nasal Cavity {declaration} equals a sum.\nX = 8 mod 23."
    parsed = events(text, forest_task)
    expected = next(n.id for n in forest_task.nodes if "Starfish's Nasal Cavity" in n.aliases)
    assert [(e.node_id, e.value) for e in parsed] == [(expected, '8')]
    assert all(text[e.value_start:e.end] == e.value for e in parsed)
