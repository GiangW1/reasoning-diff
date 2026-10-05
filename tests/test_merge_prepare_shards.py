import importlib.util
from pathlib import Path

from reasoning_diff.io import read_json, read_jsonl, write_jsonl


def test_merge_prefixes_source_pair_trace_ids_and_keeps_provenance(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts/merge_pr6_shards.py"
    spec = importlib.util.spec_from_file_location("merge_prepare_shards", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    shards = [tmp_path / "a", tmp_path / "b"]
    for index, shard in enumerate(shards):
        write_jsonl(shard / "tasks.jsonl", [{"task_id": f"task-{index}"}])
        write_jsonl(shard / "traces.jsonl", [{"id": "trace-base", "events": [{"run_id": "trace-base"}]}])
        write_jsonl(shard / "edits.jsonl", [{"trace_ids": {"base": "trace-base"}}])
        write_jsonl(shard / "observations.jsonl", [{"reference_trace": "trace-base"}])
    out = tmp_path / "merged"
    module.merge_prepare(shards, out)
    for index, (trace, edit, observation) in enumerate(zip(
        read_jsonl(out / "traces.jsonl"), read_jsonl(out / "edits.jsonl"), read_jsonl(out / "observations.jsonl"), strict=True,
    )):
        expected = f"shard{index}:trace-base"
        assert trace["id"] == trace["events"][0]["run_id"] == edit["trace_ids"]["base"] == observation["reference_trace"] == expected
    assert "run_spec.json" in read_json(out / "manifest.json")["file_hashes"]
    assert len(read_json(out / "run_spec.json")["input_hashes"]) == 8
