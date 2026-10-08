import pytest

from reasoning_diff.events import align_events, parse_events
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.mark.parametrize('middle', [
    ' Now, modulo 23: 48 divided by 23 is 2*23=46, so 48-46=2. So ',
    '\n\nNow, compute 48 modulo 23. Let\'s divide 48 by 23: 23*2=46, so 48-46=2. Therefore, ',
    '\n\nNow, applying modulo 23. Let me divide 48 by 23. 23*2=46, so 48-46=2. Therefore, 48 mod 23 is 2. So:\n\n',
    ' But since we\'re working modulo 23, let\'s compute 48 mod 23. 23*2=46, so 48-46=2. Therefore, ',
    ' 48 mod 23 = 2. So ',
])
def test_local_modular_work_marks_concluding_commit_without_dropping_raw_result(t1_tiny_path, middle):
    task = load_t1_fixture(t1_tiny_path)
    text = 'q = 3 * 16 = 48.' + middle + 'q = 2.'
    parsed = parse_events(text, task)
    assert parsed[0].value == '48' and parsed[0].event_phase == 'calculation'
    assert parsed[-1].event_phase == 'residue_commit'
    assert all(text[e.start:e.end] == e.text and text[e.value_start:e.end] == e.value for e in parsed)
    explicit = parse_events('q = 3 * 16 = 48. q = 7 mod 23.', task)
    assert (parsed[-1], explicit[-1]) in align_events(parsed, explicit)['pairs']


@pytest.mark.parametrize('text', [
    'q = 3 * 16 = 48. So q = 2.',
    'q = 3 * 16 = 48. p1 = 2 mod 23. So q = 2.',
    'q = 3 * 16 = 48. Now reduce p1 modulo 23. Therefore, q = 2.',
    'q = 3 * 16 = 48. If 48 mod 23 = 2, then q = 2.',
    'q = 3 * 16 = 48. We will reduce modulo 23 later. So q = 48.',
    'q = 3 * 16 = 48. 48 mod 23 = 2. Rechecking without modulo: so q = 48.',
    'q = 3 * 16 = 48. 48 mod 23 = 2. </think> Therefore, q = 2.',
    'q = 3 * 16 = 48. 48 mod 23 = 2. Here is an independent calculation. So q = 2.',
])
def test_modular_context_does_not_cross_entities_boundaries_or_scope(t1_tiny_path, text):
    parsed = parse_events(text, load_t1_fixture(t1_tiny_path))
    assert not any(e.node_id == 'q' and e.event_phase == 'residue_commit' for e in parsed)


def test_modular_context_uses_words_not_arithmetic_correctness(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    # An explicitly claimed (wrong) residue keeps its printed stage and value.
    parsed = parse_events('q = 3 * 16 = 99. Now, modulo 23: 48-46=2. So q = 800.', task)
    assert (parsed[-1].value, parsed[-1].event_phase) == ('800', 'residue_commit')
