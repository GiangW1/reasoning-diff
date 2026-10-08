from dataclasses import replace
from itertools import product

from reasoning_diff.events import align_events
from reasoning_diff.schema import Event, EventIdentity
from reasoning_diff import cli


def events(names):
    counts, result = {}, []
    for index, name in enumerate(names):
        counts[name] = counts.get(name, 0) + 1
        result.append(Event(EventIdentity(name, counts[name]), str(index), index * 10, index * 10 + 3,
                            index * 10 + 2, name + "=0", node_id=name, event_region="thinking",
                            event_kind="commit", event_phase="commit", expression_signature="scalar"))
    return result


def test_interleaved_context_resolves_repeats_without_values():
    left, right = events("qrq"), events("qrq")
    pairs = align_events(left, right)["pairs"]
    assert [(a.identity.occurrence_version, b.identity.occurrence_version) for a, b in pairs if a.node_id == "q"] == [(1, 1), (2, 2)]
    changed = [replace(event, value="999", correct=False) for event in right]
    assert [(a.identity.key(), b.identity.key()) for a, b in pairs] == [
        (a.identity.key(), b.identity.key()) for a, b in align_events(left, changed)["pairs"]]


def test_one_of_two_duplicate_confirmations_is_never_chosen():
    left, right = events("qrqq"), events("qrq")
    pairs = align_events(left, right)["pairs"]
    assert [(a.node_id, a.identity.occurrence_version, b.identity.occurrence_version) for a, b in pairs] == [("q", 1, 1), ("r", 1, 1)]


def test_strategy_or_region_changes_do_not_supply_context():
    left, right = events("qrq"), events("qrq")
    right[1].event_region = "answer"
    assert align_events(left, right)["pairs"] == []
    right[1].event_region = "thinking"
    right[1].event_phase = "reduction"
    assert align_events(left, right)["pairs"] == []


def all_matchings(left, right, i=0, j=0):
    """Independent exhaustive oracle for the small sequence cases below."""
    choices = {()}
    for a in range(i, len(left)):
        for b in range(j, len(right)):
            if left[a] == right[b]:
                choices.update(((a, b), *tail) for tail in all_matchings(left, right, a + 1, b + 1))
    return choices


def test_every_reported_pair_is_in_all_optimal_monotone_matchings():
    sequences = ["".join(items) for length in range(1, 5) for items in product("qr", repeat=length)]
    for left in sequences:
        for right in sequences:
            choices = all_matchings(left, right)
            length = max(map(len, choices))
            best = [set(choice) for choice in choices if len(choice) == length]
            forced = set.intersection(*best)
            a, b = events(left), events(right)
            reported = {(e.start // 10, f.start // 10) for e, f in align_events(a, b)["pairs"]}
            assert reported <= forced
            if len({left[i] for i, j in forced}) > 1:
                assert reported == forced


def test_unknown_correspondence_keeps_known_task_label(t1_tiny_path):
    from reasoning_diff.edits import apply_value_edit
    from reasoning_diff.next_round import trace_labels
    from reasoning_diff.tasks.t1_fixture import load_t1_fixture
    task = load_t1_fixture(t1_tiny_path)
    edit = apply_value_edit(task, "p1", "5")
    base = cli._synthetic_trace(task, "q = 7\nq = 7", "base", 0)
    changed = cli._synthetic_trace(edit.task, "q = 7", "edit", 0)
    base.events, changed.events = events("qq"), events("q")
    observations = cli._observations(task, base, changed, edit, "stream:0", "check")
    labels = trace_labels(observations, [task])
    assert len(labels) == 2
    assert all(label.task_known and label.task_label == 1 for label in labels)
    assert all(not label.behavior_known and label.behavior_label is None for label in labels)
