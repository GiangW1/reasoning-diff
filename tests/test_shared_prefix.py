"""Shared-prefix CPU contracts; scripted continuations are not model evidence."""
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from reasoning_diff import cli
from reasoning_diff.io import digest, file_digest, read_json, write_json, write_jsonl
from reasoning_diff.models.generate import task_prompt
from reasoning_diff.next_round import sentence_graph_task
from reasoning_diff.schema import Task
from reasoning_diff.shared_prefix import (PROTOCOL, make_plan, prefix_text, read_response, requests_for,
                                         run_request, summarize)
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.fixture
def source(t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    prompt = "<user>" + task_prompt(task) + "</user><think>"
    body = "p1 = 4.\nq = p1 * p2 = 0.\nq = 0.\n</think>\\boxed{0}"
    row = cli._synthetic_trace(task, prompt + body, "trace-base", 0).to_dict()
    row.update(model="fixture")
    row["metadata"].update(rendered_prompt_text=prompt, rendered_prompt_char_len=len(prompt),
                           boundary_status="ok", enable_thinking=True, revision="test")
    return row, task


def plan_for(source):
    row, task = source
    return make_plan([row], [task.to_dict()])


def outputs(plan, requests, *, value="8"):
    anchors = {a["id"]: a for a in plan["anchors"]}
    return [{"request": r, "protocol": PROTOCOL, "history_hash": anchors[r["anchor_id"]]["history_hash"],
             "status": "observed", "value": value} for r in requests]


def test_source_duplicate_task_records_must_agree(source):
    row, task = source
    assert make_plan([row], [task.to_dict(), task.to_dict()]) == plan_for(source)
    other = task.to_dict()
    other["question"] += " changed"
    with pytest.raises(ValueError, match="conflicting source task"):
        make_plan([row], [task.to_dict(), other])
    with pytest.raises(ValueError, match="duplicate source trace"):
        make_plan([row, row], [task.to_dict()])


def test_controlled_trace_metadata_cannot_masquerade_as_natural(source):
    row, task = source
    row["metadata"]["trajectory_protocol"] = "quantity_steps_v1"
    with pytest.raises(ValueError, match="natural numeric"):
        make_plan([row], [task.to_dict()])


def test_anchor_is_before_original_value_and_keeps_repeats(source):
    plan = plan_for(source)
    assert len(plan["anchors"]) == 2
    first, second = plan["anchors"]
    assert first["history"].endswith("q = p1 * p2 = ")
    assert second["history"].endswith("q = p1 * p2 = 0.\nq = ")
    assert first["id"] != second["id"] and first["pilot"] and not second["pilot"]
    assert "value" not in first


def test_prompt_edit_changes_only_question_not_history(source):
    plan = plan_for(source)
    anchor = plan["anchors"][0]
    task = source[1]
    edited = next(v for v in plan["variants"] if v.get("premise_id") == "p1")
    variant = Task.from_dict(edited["task"])
    text = prefix_text(anchor, task, variant)
    assert text.endswith(anchor["history"])
    assert text == anchor["rendered_prompt"].replace(task_prompt(task), task_prompt(variant)) + anchor["history"]
    # Gold annotations cannot reach this prefix.
    variant.answer_spec.value = "99999"
    for node in variant.nodes:
        node.value = "99999"
    assert prefix_text(anchor, task, variant) == text


def test_pilot_is_preselected_and_scan_reuses_request_ids(source):
    plan = plan_for(source)
    pilot, scan = requests_for(plan, "pilot"), requests_for(plan, "scan")
    assert len(pilot) == 6  # Three fresh baselines and three seed-0 edits.
    assert {r["id"] for r in pilot} <= {r["id"] for r in scan}
    assert len({r["id"] for r in scan}) == len(scan)
    assert {r["seed"] for r in pilot if r["kind"] == "base"} == {0, 1, 2}
    assert {r["premise_id"] for r in pilot if r["kind"] == "edit"} == {"p1", "unused_a", "unused_b"}
    assert len(scan) == 2 * (3 + 3 * len(source[1].premises))


@pytest.mark.parametrize("text,stop,status,value", [
    ("8.\nq = 99.", "stop_condition", "observed", "8"),
    ("-7\n", "stop_condition", "observed", "-7"),
    ("2 * 3 = 6\n", "stop_condition", "observed", "6"),
    ("8</think>", "stop_condition", "observed", "8"),
    ("8", "eos", "observed", "8"),
    ("8", "max_new", "budget_exhausted", None),
    ("3 + 4\nq = 7", "stop_condition", "unparseable_assignment", None),
    ("\nq = 8\n", "stop_condition", "unparseable_assignment", None),
    ("I reconsider.\nq = 8\n", "stop_condition", "unparseable_assignment", None),
    ("1/0\n", "stop_condition", "unparseable_assignment", None),
])
def test_only_the_anchored_assignment_can_supply_a_response(source, text, stop, status, value):
    plan = plan_for(source)
    result = read_response(plan["anchors"][0], source[1], text, stop)
    assert (result["status"], result["value"]) == (status, value)


class Tokenizer:
    eos_token_id = 0
    def encode(self, text, add_special_tokens=False):
        assert not add_special_tokens
        return list(map(ord, text))
    def decode(self, ids, skip_special_tokens=False):
        return "".join(map(chr, ids))


def runtime():
    import torch
    return {"model": torch.nn.Linear(1, 1), "tokenizer": Tokenizer(),
            "card": {"id": "fixture", "revision": "test", "context_limit": 10000}}


def test_runtime_uses_fresh_shared_seeds_and_exact_reencoded_prefix(source):
    plan = plan_for(source)
    anchor, packed = plan["anchors"][0], runtime()
    tasks = {v["id"]: Task.from_dict(v["task"]) for v in plan["variants"]}
    calls = []
    def decode(model, ids, generator, **kw):
        calls.append((ids, generator.initial_seed()))
        assert not kw["stop_condition"]([ord("8")])  # A digit can still grow.
        produced = list(map(ord, "8\n"))
        assert kw["stop_condition"](produced)
        return {"generated_ids": produced, "stop_reason": "stop_condition"}
    requests = requests_for(plan, "pilot")
    for request in requests:
        result = run_request(request, anchor, source[1], tasks[request["variant_id"]], packed, 16, decode)
        assert result["status"] == "observed" and result["value"] == "8"
        assert packed["tokenizer"].decode(result["prefix_ids"]) == prefix_text(anchor, source[1], tasks[request["variant_id"]])
    assert [seed for _, seed in calls] == [r["seed"] for r in requests]


@pytest.mark.parametrize("failure", ["roundtrip", "context", "source", "revision"])
def test_invalid_prefix_never_calls_decoder(source, failure):
    plan, packed = plan_for(source), runtime()
    anchor, request = plan["anchors"][0], requests_for(plan, "pilot")[0]
    if failure == "roundtrip":
        packed["tokenizer"].decode = lambda *a, **kw: "wrong"
    elif failure == "context":
        packed["card"]["context_limit"] = 1
    elif failure == "source":
        anchor["source_usable"] = False
    else:
        packed["card"]["revision"] = "different"
    def forbidden(*a, **kw):
        pytest.fail("invalid input reached decoder")
    if failure == "revision":
        with pytest.raises(ValueError, match="model/revision"):
            run_request(request, anchor, source[1], source[1], packed, 16, forbidden)
    else:
        result = run_request(request, anchor, source[1], source[1], packed, 16, forbidden)
        assert result["status"] in {"prefix_roundtrip_failed", "context_exhausted", "source_unusable"}


def test_noise_is_same_history_resampled_baseline_and_excess_can_be_negative(source):
    plan = plan_for(source)
    requests = requests_for(plan, "pilot")
    rows = outputs(plan, requests)
    for row in rows:
        if row["request"]["kind"] == "base" and row["request"]["seed"] != 0:
            row["value"] = "9"
    report = summarize(plan, requests, rows, "pilot")
    assert report["passed"]
    assert all(r["response"] == 0 and r["noise"] == 1 and r["excess"] == -1 for r in report["contrasts"])
    assert report["overall"]["mean_excess_on_common_support"] == -1


def test_failed_and_missing_draws_do_not_shrink_denominator(source):
    plan = plan_for(source)
    requests = requests_for(plan, "pilot")
    rows = outputs(plan, requests)
    del rows[1]  # one independent baseline is missing
    report = summarize(plan, requests, rows, "pilot")
    assert not report["passed"] and report["missing_requests"] == 1
    assert report["overall"]["planned_comparisons"] == 3
    assert report["overall"]["paired_coverage"] == 1
    assert report["overall"]["common_noise_coverage"] == 0
    assert all(r["excess"] is None for r in report["contrasts"])


@pytest.mark.parametrize("change", ["duplicate", "history", "protocol"])
def test_mixed_or_duplicate_responses_cannot_enter_report(source, change):
    plan = plan_for(source)
    requests = requests_for(plan, "pilot")
    rows = outputs(plan, requests)
    if change == "duplicate":
        rows.append(rows[0])
    else:
        rows[0]["history_hash" if change == "history" else "protocol"] = "wrong"
    with pytest.raises(ValueError):
        summarize(plan, requests, rows, "pilot")


@pytest.fixture
def runner(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("run_shared_prefix")


def save_source(path, source):
    row, task = source
    write_jsonl(path / "tasks.jsonl", [task.to_dict()])
    write_jsonl(path / "traces.jsonl", [row])
    write_json(path / "manifest.json", {"file_hashes": {n: file_digest(path / n) for n in ("tasks.jsonl", "traces.jsonl")}})


def test_plan_is_cpu_only_and_changed_protocol_cannot_resume(source, tmp_path, runner, monkeypatch):
    src, out = tmp_path / "source", tmp_path / "out"
    save_source(src, source)
    monkeypatch.setattr(runner, "run_workers", lambda *a: pytest.fail("plan started a worker"))
    args = ["--in-dir", str(src), "--out-root", str(out)]
    assert runner.main(args) == 0
    assert runner.main(args) == 0
    assert read_json(out / "plan_summary.json")["requests"]["pilot"] == 6
    with pytest.raises(ValueError, match="protocol changed"):
        runner.main(args + ["--max-new", "17"])
    write_jsonl(src / "traces.jsonl", [])
    with pytest.raises(ValueError, match="manifest mismatch"):
        runner.main(args)


@pytest.mark.parametrize("invalid", [True, False])
def test_scan_requires_pilot_and_resumes_authenticated_results(source, tmp_path, runner, monkeypatch, invalid):
    src, out = tmp_path / "source", tmp_path / "out"
    save_source(src, source)
    monkeypatch.setattr(runner, "SERVER", tmp_path)
    monkeypatch.setitem(__import__("sys").modules, "fcntl", SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *a: None))
    calls = []
    def workers(root, phase, gpus, env, deadline):
        calls.append(phase)
        plan = read_json(root / "plan.json")
        fp = read_json(root / "protocol.json")["fingerprint"]
        for row in outputs(plan, requests_for(plan, phase)):
            if invalid and row["request"]["kind"] == "edit":
                row.update(status="unparseable_assignment", value=None)
            write_json(root / "responses" / f"{row['request']['id']}.json", {"fingerprint": fp, "result_hash": digest(row), "result": row})
    monkeypatch.setattr(runner, "run_workers", workers)
    args = ["--mode", "scan", "--in-dir", str(src), "--out-root", str(out), "--time-budget-hours", "1"]
    if invalid:
        with pytest.raises(RuntimeError, match="pilot failed"):
            runner.main(args)
        assert calls == ["pilot"] and read_json(out / "pipeline.json")["status"] == "failed"
    else:
        assert runner.main(args) == 0
        assert calls == ["pilot", "scan"]
        assert read_json(out / "scan_report.json")["passed"]
        calls.clear()
        started_at = read_json(out / "execution_budget.json")["started_at"]
        monkeypatch.setattr(runner.time, "time", lambda: started_at + 7200)
        assert runner.main(args) == 0
        assert calls == []  # Fully checkpointed phases must not launch workers.
        request = requests_for(read_json(out / "plan.json"), "pilot")[0]
        fp = read_json(out / "protocol.json")["fingerprint"]
        assert runner.saved_result(out, request, fp)
        path = out / "responses" / f"{request['id']}.json"
        row = read_json(path)
        row["result"]["value"] = "tampered"
        write_json(path, row)
        with pytest.raises(ValueError, match="checkpoint mismatch"):
            runner.saved_result(out, request, fp)
        with pytest.raises(ValueError, match="checkpoint mismatch"):
            runner.main(args)
        assert read_json(out / "pipeline.json")["status"] == "failed"


@pytest.mark.parametrize("expired", [False, True])
def test_worker_failure_or_deadline_stops_sibling_processes(tmp_path, runner, monkeypatch, expired):
    (tmp_path / "logs").mkdir()
    children = []
    class Process:
        def __init__(self, command, **kwargs):
            self.args, self.terminated, self.code = command, False, None
            self.log = kwargs["stdout"]
            children.append(self)
            if not expired and len(children) == 1:
                self.code = 7
        def poll(self):
            return self.code
        def terminate(self):
            self.terminated, self.code = True, -15
        def wait(self, timeout=None):
            return self.code
    monkeypatch.setattr(runner.subprocess, "Popen", Process)
    times = iter([0, 0, 2])  # Deadline after both launches.
    monkeypatch.setattr(runner.time, "time", lambda: next(times))
    error = runner.subprocess.TimeoutExpired if expired else runner.subprocess.CalledProcessError
    with pytest.raises(error):
        runner.run_workers(tmp_path, "pilot", [2, 3], {}, 1 if expired else None)
    assert len(children) == 2
    assert children[1].terminated
    assert all(child.log.closed for child in children)


def test_deadline_is_persisted_and_partial_failure_reports_missing_requests(source, tmp_path, runner, monkeypatch):
    src, out = tmp_path / "source", tmp_path / "out"
    save_source(src, source)
    monkeypatch.setattr(runner, "SERVER", tmp_path)
    monkeypatch.setitem(__import__("sys").modules, "fcntl", SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *a: None))
    calls = []
    def workers(root, phase, gpus, env, deadline):
        calls.append(deadline)
        raise runner.subprocess.TimeoutExpired("fixture", 0)
    monkeypatch.setattr(runner, "run_workers", workers)
    args = ["--mode", "pilot", "--in-dir", str(src), "--out-root", str(out), "--time-budget-hours", "1"]
    for _ in range(2):
        with pytest.raises(runner.subprocess.TimeoutExpired):
            runner.main(args)
    assert calls[0] == calls[1]
    report = read_json(out / "pilot_report.json")
    assert report["missing_requests"] == 6 and report["overall"]["planned_comparisons"] == 3
    assert read_json(out / "pipeline.json")["status"] == "budget_exhausted"


def test_worker_shards_requests_and_reuses_pilot_in_scan(source, tmp_path, runner, monkeypatch):
    from reasoning_diff.models import adapters
    import trace_batching
    src, out = tmp_path / "source", tmp_path / "out"
    save_source(src, source)
    assert runner.main(["--in-dir", str(src), "--out-root", str(out), "--gpus", "2", "3"]) == 0
    loads, decoded, closed = [], [], []
    def load(*args, **kwargs):
        loads.append(args)
        return runtime()
    class Decoder:
        def __init__(self, size):
            assert size == 2
        def __call__(self, model, ids, generator, **kw):
            decoded.append(generator.initial_seed())
            return {"generated_ids": list(map(ord, "8\n")), "stop_reason": "stop_condition"}
        def close(self):
            closed.append(True)
    monkeypatch.setattr(adapters, "load_frozen", load)
    monkeypatch.setattr(trace_batching, "BatchDecoder", Decoder)
    for phase in ("pilot", "scan", "scan"):
        for shard in range(2):
            assert runner.worker(SimpleNamespace(out_root=out, phase=phase, shard_index=shard)) == 0
    plan = read_json(out / "plan.json")
    requests = requests_for(plan, "scan")
    fp = read_json(out / "protocol.json")["fingerprint"]
    assert len(decoded) == len(requests)
    assert len(loads) == len(closed) == 4  # Final resume does not even load a model.
    assert all(runner.saved_result(out, r, fp)["status"] == "observed" for r in requests)
    assert runner.collect_report(out, plan, "scan", fp)["passed"]


@pytest.mark.parametrize("corrupt", [False, True])
def test_eos_is_removed_only_from_parsing_and_full_boundary_is_verified(source, corrupt):
    plan, packed = plan_for(source), runtime()
    anchor, request = plan["anchors"][0], requests_for(plan, "pilot")[0]
    tokenizer = packed["tokenizer"]
    if corrupt:
        decode_text = tokenizer.decode
        tokenizer.decode = lambda ids, **kw: ("corrupt" if ids[-1] == ord("8") else "") + decode_text(ids, **kw)
    def decode(*a, **kw):
        return {"generated_ids": [ord("8"), tokenizer.eos_token_id], "stop_reason": "eos"}
    result = run_request(request, anchor, source[1], source[1], packed, 16, decode)
    assert result["generated_ids"][-1] == tokenizer.eos_token_id
    assert result["status"] == ("continuation_boundary_failed" if corrupt else "observed")
    if not corrupt:
        assert result["value"] == "8" and result["continuation"] == "8"


def test_straddling_original_token_is_reencoded_without_its_value(source):
    row, task = source
    class MergedTokenizer(Tokenizer):
        # The original token contains both the assignment head and its value.
        def encode(self, text, add_special_tokens=False):
            return super().encode(text.replace("= 0", chr(9999)), add_special_tokens)
        def decode(self, ids, skip_special_tokens=False):
            return super().decode(ids, skip_special_tokens).replace(chr(9999), "= 0")
    tokenizer = MergedTokenizer()
    row["token_ids"] = tokenizer.encode(row["text"])
    plan, packed = plan_for(source), runtime()
    packed["tokenizer"] = tokenizer
    anchor, request = plan["anchors"][0], requests_for(plan, "pilot")[0]
    def decode(model, ids, generator, **kw):
        assert 9999 not in ids
        assert tokenizer.decode(ids).endswith("q = p1 * p2 = ")
        return {"generated_ids": list(map(ord, "8\n")), "stop_reason": "stop_condition"}
    assert run_request(request, anchor, task, task, packed, 16, decode)["value"] == "8"


def test_zero_anchor_source_is_retained_and_blocks_measurement(source):
    row, task = source
    row["text"] = row["metadata"]["rendered_prompt_text"] + "Thinking without any assignment."
    plan = plan_for(source)
    assert plan["anchors"] == [] and len(plan["sources"]) == 1
    report = summarize(plan, [], [], "pilot")
    assert not report["passed"] and not report["checks"]["every_source_has_anchor"]


def test_failed_source_is_not_removed_from_planned_support(source):
    row, _ = source
    row["metadata"]["boundary_status"] = "failed"
    plan = plan_for(source)
    assert all(not a["source_usable"] for a in plan["anchors"])
    assert all("source_boundary_failed" in a["source_failures"] for a in plan["anchors"])
    requests = requests_for(plan, "pilot")
    report = summarize(plan, requests, [], "pilot")
    assert report["overall"]["planned_comparisons"] == 3 and not report["passed"]
