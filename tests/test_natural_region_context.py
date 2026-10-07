from reasoning_diff.events import align_events, assign_event_regions, parse_events
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def events(text, task):
    return assign_event_regions(parse_events(text, task), text, initial_thinking=True)


def test_answer_only_words_cannot_select_a_thinking_occurrence(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    right = events('Checking multiplication again.\nq = 6.\n\n'
                   'Reviewing subtraction carefully.\nq = 9.', task)
    for answer in ('Checking multiplication again.', 'Reviewing subtraction carefully.', ''):
        left = events('q = 6.\n</think>\n' + answer + ' Answer: 6.', task)
        assert not align_events(left, right)['pairs']


def test_thinking_context_survives_clipping_at_region_boundary(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    left = events('Checking multiplication again.\nq = 6.\n</think>\nReviewing subtraction carefully.', task)
    right = events('Checking multiplication again.\nq = 8.\n\nReviewing subtraction carefully.\nq = 9.', task)
    assert [(a.value, b.value) for a, b in align_events(left, right)['pairs']] == [('6', '8')]
    assert 'reviewing' not in left[0].alignment_context


def test_answer_context_cannot_inherit_thinking_words(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    parsed = events('Checking multiplication again.\n</think>\nq = 6.', task)
    assert parsed[0].event_region == 'answer'
    assert 'checking' not in parsed[0].alignment_context
    assert 'multiplication' not in parsed[0].alignment_context
