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
    assert trace.events[1].event_kind == "commit"
    trace.events[1].event_kind = "restatement"
    assert [event.value for event in runner.final_commitments(trace).events] == ["7"]


def test_remeasure_preserves_raw_manifest_and_rebuilds_missing_noise(runner, tmp_path, t1_tiny_path):
    from reasoning_diff import cli
    from reasoning_diff.artifacts import write_manifest, write_run_spec
    from reasoning_diff.edits import apply_value_edit
    from reasoning_diff.io import file_digest, read_json, read_jsonl, write_jsonl
    from reasoning_diff.next_round import sentence_graph_task
    from reasoning_diff.tasks.t1_fixture import load_t1_fixture
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    edit = apply_value_edit(task, "unused_a", "3")
    traces = []
    for seed in range(3):
        trace = cli._synthetic_trace(task, "prompt\nq = 7\n</think>\n7", f"trace-base:seed{seed}", seed)
        trace.events = []
        trace.metadata.update(rendered_prompt_text="prompt\n", rendered_prompt_char_len=7,
                              enable_thinking=True, boundary_status="ok")
        traces.append(trace.to_dict())
    donor = cli._synthetic_trace(edit.task, "prompt\nq = 8\n</think>\n8", "trace-edit", 0)
    donor.events = []
    donor.metadata.update(traces[0]["metadata"])
    traces.append(donor.to_dict())
    source, output = tmp_path / "original", tmp_path / "remeasured"
    files = {"tasks.jsonl": [task.to_dict(), edit.task.to_dict()], "edits.jsonl": [edit.to_dict()],
             "splits.jsonl": [], "traces.jsonl": traces,
             "observations.jsonl": [{"reference_trace": traces[0]["id"], "comparison_trace": donor.id,
                 "edit_id": edit.id, "rng_pair": "stream:0", "run_id": "saved", "task_id": task.task_id,
                 "premise_id": "unused_a", "outcome": "structural", "alignment_ref": "", "node_id": "q"}]}
    for name, rows in files.items():
        write_jsonl(source / name, rows)
    write_run_spec(source, {"config": {"noise_reference": "base_pairs"}})
    write_manifest(source, [source / name for name in (*files, "run_spec.json")], {"success": 1})
    hashes = {path.name: file_digest(path) for path in source.iterdir()}
    runner.remeasure(source, output)
    assert hashes == {path.name: file_digest(path) for path in source.iterdir()}
    updated = read_jsonl(output / "traces.jsonl")
    for old, new in zip(traces, updated, strict=True):
        assert new["events"]
        for field in ("text", "token_ids", "offsets", "answer", "correct", "status"):
            assert new[field] == old[field]
    noise = [row for row in read_jsonl(output / "observations.jsonl") if row["rng_pair"].startswith("sham:")]
    assert len(noise) == 6 and len({row["observation_id"] for row in noise}) == 6
    report = read_json(output / "measurement_report.json")
    assert report["before"]["trajectories_with_rho"] == 0
    assert report["after"]["trajectories_with_rho"] == 1
    assert report["matching_policy"] == "region_structure_forced_sequence_v3"
    assert not report["formal_launch_ready"]
    lightweight = tmp_path / "report-only"
    runner.remeasure(source, lightweight, report_only=True)
    assert {path.name for path in lightweight.iterdir()} == {"manifest.json", "run_spec.json", "measurement_report.json"}
    assert read_json(lightweight / "measurement_report.json")["measurement_quality"] == report["measurement_quality"]
    assert read_json(lightweight / "run_spec.json")["config"]["report_only"]
    assert hashes == {path.name: file_digest(path) for path in source.iterdir()}
    with pytest.raises(ValueError, match="new output directory"):
        runner.remeasure(source, output)
    write_jsonl(source / "traces.jsonl", [])
    with pytest.raises(ValueError, match="manifest"):
        runner.remeasure(source, tmp_path / "tampered")
