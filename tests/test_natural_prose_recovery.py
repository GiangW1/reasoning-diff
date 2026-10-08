import pytest

from reasoning_diff.events import align_events, parse_events
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.mark.parametrize('formula, symbolic', [
    ('sum of p1 and p2', 'p1 + p2'),
    ('the product of p1 and p2', 'p1 * p2'),
    ('difference between p1 and p2', 'p1 - p2'),
    ('product of 18 and (sum of 0 and p1)', '18 * (0 + p1)'),
    ('(product of p1 and 0) + (product of p2 and 2)', '(p1 * 0) + (p2 * 2)'),
    ('sum of (product of p1 and 0) and (product of p2 and 2)', '(p1 * 0) + (p2 * 2)'),
    ('product of p1 (which is 22) and p2 (which is 1)', 'p1 * p2'),
])
def test_printed_prose_formula_has_same_structure_as_symbolic_formula(t1_tiny_path, formula, symbolic):
    task = load_t1_fixture(t1_tiny_path)
    prose = parse_events('q = ' + formula + ' = 17.', task)
    arithmetic = parse_events('q = ' + symbolic + ' = 999.', task)
    assert len(prose) == 1
    assert prose[0].expression_signature == arithmetic[0].expression_signature
    assert len(align_events(prose, arithmetic)['pairs']) == 1


def test_numeric_annotation_after_full_quantity_name_is_not_multiplication(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    task.premises[0].text = "The number of Example's Value equals 2."
    task.premises[0].kind = 'sentence'
    task.premises[0].end = len(task.premises[0].text)
    text = "q = sum of Example's Value (22) and 0. So 22 + 0 = 22."
    parsed = parse_events(text, task)
    assert len(parsed) == 1 and parsed[0].value == '22'
    assert "id='p1'" in parsed[0].expression_signature
    assert not parse_events('q = p1(22) + 0 = 22.', task)


@pytest.mark.parametrize('text', [
    'q = 4 * p1. That\'s 4*14 = 56.',
    'q = product of p1 and p2. So 22 * 1 = 22.',
    'q = 18 * (0 + p1) = 18 * 14. Let me compute that. 18*14 is 252.',
    'q = sum of p1 and p2. That is 14 + 10 = 24.',
])
def test_adjacent_numeric_work_can_use_an_explicit_simplified_formula(t1_tiny_path, text):
    task = load_t1_fixture(t1_tiny_path)
    parsed = parse_events(text, task)
    assert len(parsed) == 1 and parsed[0].event_phase == 'calculation'
    assert "id='p1'" in parsed[0].expression_signature
    assert text[parsed[0].start:parsed[0].end] == parsed[0].text


@pytest.mark.parametrize('text', [
    'q = product of p1 and p2. So 22 + 1 = 23.',
    'q = sum of (product of p1 and 2) and p2. So 22 * 2 = 44.',
    'q = 18 * (0 + p1). Let me compute that. 18 * 14 = 252.',
    'q = sum of p1 and p2 and p3 = 20.',
    'q = product of p1 and unknown(p2) = 2.',
    'q = product of p1 and p2.\n\nThat is 22 * 1 = 22.',
])
def test_prose_formula_does_not_infer_missing_structure(t1_tiny_path, text):
    assert not parse_events(text, load_t1_fixture(t1_tiny_path))


@pytest.mark.parametrize('continuation', [
    'Since 25 mod 23 is 2.',
    "So that's 25 mod 23 = 2.",
    '25 divided by 23 is 1 with remainder 2.',
    '25 divided by 23 is 1 with a remainder of 2.',
    'Modulo 23, 25 - 23 = 2.',
])
def test_explicit_remainder_continues_named_raw_calculation(t1_tiny_path, continuation):
    text = 'q = 15 + 10 = 25. ' + continuation
    task = load_t1_fixture(t1_tiny_path)
    parsed = parse_events(text, task)
    assert [(e.value, e.event_phase) for e in parsed] == [('25', 'calculation'), ('2', 'reduction')]
    assert all(text[e.start:e.end] == e.text for e in parsed)
    assert all(text[e.value_start:e.end] == e.value for e in parsed)
    other = parse_events('q = 16 + 10 = 26. 26 mod 23 = 3.', task)
    assert len(align_events(parsed, other)['pairs']) == 2


@pytest.mark.parametrize('continuation', [
    '25 divided by 23 is 1.',
    'p1 = 25. 25 divided by 23 is 1 with remainder 2.',
    '\n\n25 divided by 23 is 1 with remainder 2.',
    '25 divided by 23 is 1 with remainder 2 + 3.',
    'Modulo 23, 23 * 1 = 23.',
    'Another calculation: 25 divided by 23 is 1 with remainder 2.',
])
def test_remainder_requires_explicit_local_complete_result(t1_tiny_path, continuation):
    parsed = parse_events('q = 15 + 10 = 25. ' + continuation, load_t1_fixture(t1_tiny_path))
    assert not any(e.event_phase == 'reduction' for e in parsed)
