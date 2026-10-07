import pytest

from reasoning_diff.events import align_events, parse_events
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def test_repeated_destination_name_is_a_label_in_an_equation_chain(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    next(n for n in task.nodes if n.id == 'q').aliases.append("Example's Quantity")
    text = "q = Example's Quantity = p1 * p2 = 4 * 0 = 0"
    left = parse_events(text, task)
    right = parse_events('q = p1 * p2 = 9 * 2 = 18', task)
    assert len(left) == 1 and left[0].event_phase == 'calculation'
    assert left[0].expression_signature == right[0].expression_signature
    assert len(align_events(left, right)['pairs']) == 1
    assert left[0].text == text


def test_other_entity_and_self_reference_are_not_labels(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    copy = parse_events('q = p1 = 2 * 2 = 4', task)[0]
    assert copy.event_phase == 'copy' and "id='p1'" in copy.expression_signature
    calc = parse_events('q = q + 1 = 5', task)[0]
    assert calc.event_phase == 'calculation' and "id='q'" in calc.expression_signature


def test_explicit_multiword_and_primed_aliases(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    text = "p1 (AMS MB) = 7\np2 (R') = 2\nq (AS Rucksack) = AMS MB - R'\nAS Rucksack = AMS MB - R' = 7 - 2 = 5"
    parsed = parse_events(text, task)
    assert [(e.node_id, e.value) for e in parsed] == [('p1', '7'), ('p2', '2'), ('q', '5')]
    assert 'unresolved:' not in parsed[-1].expression_signature
    assert "id='p1'" in parsed[-1].expression_signature and "id='p2'" in parsed[-1].expression_signature


def test_multiword_alias_conflict_abstains(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    assert parse_events('q (AS Item) = p1 * p2\np1 (AS Item) = 4\nAS Item = 4', task) == []


@pytest.mark.parametrize('expression', ['15 plus 10 is 25', '15 + 10 equals 25', '15 multiplied by 10 is 150'])
def test_explicit_arithmetic_with_prose_operators(t1_tiny_path, expression):
    task = load_t1_fixture(t1_tiny_path)
    parsed = parse_events('q is ' + expression + '.', task)
    assert len(parsed) == 1 and parsed[0].event_phase == 'calculation'


@pytest.mark.parametrize('text', [
    'q = 21 + p1. p1 is 2. So 21 + 2 = 23.',
    'q = 21 + p1. p1 is 2, so 21 + 2 = 23.',
    'q = 22 * p1. Since p1 is 0, 22 * 0 is 0.',
    'q is 15 plus p1. Since p1 is 10, that would be 15 + 10. Let me compute that: 15 + 10 = 25.',
    'q = 15 + p1. Since p1 is 10, that would be 15 + 10. Let me compute that. 15 + 10 is 25.',
])
def test_explicit_operand_substitution_keeps_named_destination(t1_tiny_path, text):
    task = load_t1_fixture(t1_tiny_path)
    parsed = [e for e in parse_events(text, task) if e.node_id == 'q']
    assert len(parsed) == 1 and parsed[0].event_phase == 'calculation'
    assert "id='p1'" in parsed[0].expression_signature
    assert all(text[e.start:e.end] == e.text for e in parsed)
    # Correspondence depends on the printed whole operation, not its answer.
    other = parse_events('q = 19 * 4 = 76.' if '*' in text else 'q = 19 + 4 = 23.', task)
    assert len(align_events(parsed, other)['pairs']) == 1
    other[0].value, other[0].correct = '999', False
    assert len(align_events(parsed, other)['pairs']) == 1


@pytest.mark.parametrize('text', [
    'q = 21 + p1. p2 is 2, so 21 + 2 = 23.',
    'q = 21 + p1. p1 is 2. Another calculation: 21 + 2 = 23.',
    'q = 21 + p1. p1 is 2, so 21 * 2 = 42.',
    'q = (p1 * 2) + p2. p1 is 2, so 2 * 2 = 4.',
    'q = 21 + p1. Since p1 is 2, that would be 21 * 2. Let me compute that: 21 + 2 = 23.',
    'q = 21 + p1. Since p1 is 2, that would be 21 + 2.\n\nLet me compute that: 21 + 2 = 23.',
    'q = 21 + p1. Since p1 is 2, that would be 21 + 2.</think>\n21 + 2 = 23.',
])
def test_substitution_cannot_claim_other_topic_or_partial_term(t1_tiny_path, text):
    assert not any(e.node_id == 'q' for e in parse_events(text, load_t1_fixture(t1_tiny_path)))


@pytest.mark.parametrize('text', [
    'q = p1 + p2 = 15 + 10 = 25 mod23=2.',
    'q = p1 + p2 = 15 + 10 = 25, 25 mod 23 = 2.',
    'q = p1 + p2 = 15 + 10 = 25. 25 mod 23 is 2.',
    'q = p1 + p2 = 15 + 10 = 25 ≡ 2 mod 23.',
])
def test_raw_and_reduced_printed_results_survive_equation_layout(t1_tiny_path, text):
    task = load_t1_fixture(t1_tiny_path)
    parsed = parse_events(text, task)
    assert [(e.value, e.event_phase) for e in parsed] == [('25', 'calculation'), ('2', 'reduction')]
    assert all(e.status == 'ok' and text[e.start:e.end] == e.text for e in parsed)
    assert len({e.value_start for e in parsed}) == 2
    separate = parse_events('q = p1 + p2 = 16 + 10 = 26. 26 mod 23 = 3.', task)
    assert len(align_events(parsed, separate)['pairs']) == 2


@pytest.mark.parametrize('text', [
    'q = (15 + 10) mod 23 = 2.',
    'q = 25 mod 23 = 2.',
    'q = 2 (mod 23).',
    'q = 15 + 10 mod 23.',
    'q = 48 mod23=48-2*23=48-46=2.',
])
def test_raw_stage_requires_a_printed_complete_arithmetic_result(t1_tiny_path, text):
    parsed = parse_events(text, load_t1_fixture(t1_tiny_path))
    assert not any(e.event_phase == 'calculation' for e in parsed)


@pytest.mark.parametrize('work', ['So 15 + 10 = 25.', '15 + 10 = 25.'])
def test_later_prose_does_not_hide_immediate_printed_substitution(t1_tiny_path, work):
    text = 'q = p1 + p2. ' + work + ' 25 mod 23 is 2. So q is 2.'
    parsed = parse_events(text, load_t1_fixture(t1_tiny_path))
    assert [(e.value, e.event_phase) for e in parsed] == [
        ('25', 'calculation'), ('2', 'reduction'), ('2', 'residue_commit')]
