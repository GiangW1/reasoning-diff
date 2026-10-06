import pytest

from reasoning_diff.events import assign_event_regions, parse_events
from reasoning_diff.next_round import measurement_report, sentence_graph_task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def example(path, include_noise=True):
    task = sentence_graph_task(load_t1_fixture(path))
    text = "q = 7\nq = 8\nq = 9"
    events = assign_event_regions(parse_events(text, task), text, initial_thinking=True)
    trace = {"id": "base", "task_id": task.task_id, "seed": 0,
             "events": [event.to_dict() for event in events], "status": "natural_complete",
             "correct": True, "metadata": {"boundary_status": "ok"}}
    observations = []
    # Unequal premise support checks that events, rather than cells, receive
    # equal weights on exactly the same raw and noise support.
    for index, outcomes in enumerate((("changed", "no_change"), ("no_change",), ("changed",))):
        for pid, outcome in zip(("unused_a", "unused_b"), outcomes):
            observations.append({"reference_trace": "base", "alignment_ref": events[index].identity.key(),
                                 "premise_id": pid, "outcome": outcome, "rng_pair": "stream:0"})
    if include_noise:
        for index, outcome in enumerate(("changed", "no_change")):
            observations.append({"reference_trace": "base", "alignment_ref": events[index].identity.key(),
                                 "premise_id": "sham:q", "outcome": outcome, "rng_pair": "sham:1"})
    return measurement_report([trace], [task.to_dict()], observations, [])


def test_common_support_diagnostic_does_not_erase_partial_measurement_or_pass_gate(t1_tiny_path):
    report = example(t1_tiny_path)
    row = report["trajectories"][0]
    assert row["rho"] is None and row["rho_raw"] == pytest.approx(0.5)
    common = row["common_support_diagnostic"]
    assert common["raw"] == pytest.approx(0.25)
    assert common["noise"] == pytest.approx(0.5)
    assert common["excess"] == pytest.approx(-0.25)
    assert common["events"] == 2 and common["observed_events"] == 3
    assert common["event_coverage"] == pytest.approx(2 / 3)
    assert common["cells"] == 3
    assert common["status"] == "descriptive_only"
    assert report["overall"]["rho_coverage"] == 0
    assert not report["checks"]["rho_coverage"] and not report["passed"]


def test_empty_common_support_stays_null(t1_tiny_path):
    row = example(t1_tiny_path, include_noise=False)["trajectories"][0]
    common = row["common_support_diagnostic"]
    assert common["raw"] is common["noise"] is common["excess"] is None
    assert common["events"] == common["cells"] == 0
    assert common["status"] == "no_common_support"
    assert row["rho"] is None
