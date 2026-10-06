import importlib
from pathlib import Path

import pytest

@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("reparse_pr8")


def test_reparse_uses_generated_text_and_keeps_raw_generation(runner, t1_tiny_path):
    from reasoning_diff.tasks.t1_fixture import load_t1_fixture
    task = load_t1_fixture(t1_tiny_path)
    prefix = "q = 999\nassistant: "
    text = prefix + "q = 7\n</think>\n7"
    row = {"id": "base", "task_id": task.task_id, "base_group_id": task.base_group_id,
           "model": "saved", "seed": 0, "text": text, "token_ids": [11, 12],
           "offsets": [[0, len(prefix)], [len(prefix), len(text)]], "events": [],
           "answer": "7", "correct": True, "status": "natural_complete",
           "metadata": {"rendered_prompt_text": prefix, "rendered_prompt_char_len": len(prefix),
                        "enable_thinking": True, "boundary_status": "ok"}}
    trace = runner.reparse_trace(row, task, "parser")
    assert [event.value for event in trace.events] == ["7"]
    assert all(event.start >= len(prefix) and event.event_region == "thinking" for event in trace.events)
    assert trace.token_ids == row["token_ids"] and trace.offsets == row["offsets"]
    assert (trace.text, trace.answer, trace.correct, trace.status) == (text, "7", True, "natural_complete")
    assert row["events"] == [] and "measurement_reparse" not in row["metadata"]


def test_reparse_refuses_unknown_prompt_boundary(runner, t1_tiny_path):
    from reasoning_diff.tasks.t1_fixture import load_t1_fixture
    task = load_t1_fixture(t1_tiny_path)
    row = {"id": "base", "task_id": task.task_id, "base_group_id": task.base_group_id,
           "model": "saved", "seed": 0, "text": "q = 7", "token_ids": [], "offsets": [],
           "events": [], "answer": None, "correct": None,
           "metadata": {"rendered_prompt_text": "different", "rendered_prompt_char_len": 9}}
    with pytest.raises(ValueError, match="generation boundary"):
        runner.reparse_trace(row, task, "parser")


def test_final_commitments_select_by_position_and_exclude_answer_and_restatements(runner, t1_tiny_path):
    from reasoning_diff.events import assign_event_regions, parse_events
    from reasoning_diff.schema import Trace
    from reasoning_diff.tasks.t1_fixture import load_t1_fixture
    task = load_t1_fixture(t1_tiny_path)
    text = "q = 7\nq = 2\n</think>\nq = 3"
    events = parse_events(text, task)
    assign_event_regions(events, text, initial_thinking=True)
    trace = Trace("base", task.task_id, task.base_group_id, "saved", 0, text, [], [], events, "3", False)
    final = runner.final_commitments(trace)
    assert [event.value for event in final.events] == ["2"]
    assert final.events[0].identity.occurrence_version == 2
    assert len(trace.events) == 3 and final.correct is False
    final.events[0].event_kind = "restatement"
    assert [event.value for event in runner.final_commitments(trace).events] == ["7"]
