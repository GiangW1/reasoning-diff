"""CPU fixtures exercise protocol wiring; these are not model evidence."""
from itertools import permutations
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from reasoning_diff import cli
from reasoning_diff.events import align_events, assign_event_regions, parse_events
from reasoning_diff.graphs import ancestors
from reasoning_diff.models.generate import task_prompt
from reasoning_diff.next_round import measurement_report, scan_edits, sentence_graph_task
from reasoning_diff.quantity_steps import ESTIMAND, MATCHING_POLICY, PROTOCOL, controlled_task, format_report
from reasoning_diff.schema import EventIdentity, Task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def controlled(t1_tiny_path, multiple=False):
    task = load_t1_fixture(t1_tiny_path)
    if multiple:
        task = Task.from_dict({**task.to_dict(), "nodes": [
            {"id": "r", "aliases": ["r"], "parents": ["p1"], "value": "4", "expression": "p1"},
            {"id": "q", "aliases": ["q"], "parents": ["r", "p2"], "value": "0", "expression": "r * p2"}]})
    return controlled_task(sentence_graph_task(task))


def transcript(task, values=None):
    return "\n".join(f'<step node="{n.id}">I calculate and check. <commit>{(values or {}).get(n.id, n.value)}</commit></step>'
                     for n in task.nodes) + f'\n</think>\\boxed{{{task.answer_spec.value}}}'


def trace(task, text, tid, seed):
    result = cli._synthetic_trace(task, text, tid, seed)
    result.events = assign_event_regions(parse_events(text, task), text, initial_thinking=True)
    result.metadata.update(boundary_status="ok", generated_tokens=len(text), quantity_step_format=format_report(text, task))
    result.status = "natural_complete"
    return result


def test_explicit_condition_loading_and_no_gold_in_prompt(t1_tiny_path, tmp_path):
    args = cli.build_parser().parse_args(["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(tmp_path),
                                         "--premise-protocol", "sentence_graph", "--trajectory-protocol", "quantity_steps"])
    task = cli._load_tasks(args)[0]
    assert task.metadata["trajectory_protocol"] == PROTOCOL
    assert task.metadata["measurement_estimand"] == ESTIMAND
    assert task.source_kind == "project_derived"
    prompt = task_prompt(task)
    # Only the question's givens and registered node names can reach the model.
    for n in task.nodes:
        n.value = "999999"
    task.answer_spec.value = "888888"
    assert task_prompt(task) == prompt
    assert "999999" not in prompt and "888888" not in prompt
    args.premise_protocol = "leaf"
    with pytest.raises(ValueError, match="sentence-graph"):
        cli._load_tasks(args)


def test_value_blind_registered_step_pairing_and_true_boundaries(t1_tiny_path):
    task = controlled(t1_tiny_path, multiple=True)
    left_text, right_text = transcript(task), transcript(task, {"r": "15", "q": "-9"})
    left, right = [assign_event_regions(parse_events(text, task), text, initial_thinking=True) for text in (left_text, right_text)]
    assert format_report(left_text, task)["passed"]
    result = align_events(left, right)
    assert result["structural"]["detector"] == MATCHING_POLICY
    assert [(a.node_id, b.node_id) for a, b in result["pairs"]] == [("r", "r"), ("q", "q")]
    for event in left:
        assert left_text[event.start:event.end] == event.text
        assert left_text[event.start:].startswith('<step node="')
        assert left_text[event.value_start:].startswith(event.value)
        assert "I calculate" in left_text[event.start:event.value_start]
    for n in task.nodes:
        n.value = "999"
    assert [(e.node_id, e.value) for e in parse_events(left_text, task)] == [("r", "4"), ("q", "0")]


@pytest.mark.parametrize("change,issue", [
    (lambda s: s.replace('node="q"', 'node="unlisted"'), "unknown_nodes"),
    (lambda s: s.replace("</commit>", "</commit>more reasoning"), "malformed_steps"),
    (lambda s: s.replace("<commit>0", "<commit>1</commit><commit>0"), "malformed_steps"),
    (lambda s: s.split("\n</think>")[0] + "\n" + s, "duplicate_nodes"),
    (lambda s: s + '<step node="q"><commit>0</commit></step>', "answer_steps"),
    (lambda s: s.replace("<commit>0", "<commit>4 * 0"), "malformed_steps"),
    (lambda s: s.replace("</think>", "</step></think>"), "malformed_steps"),
    (lambda s: s.replace("</think>", "</commit></think>"), "uncontained_commits"),
])
def test_invalid_transcripts_fail_closed(t1_tiny_path, change, issue):
    task = controlled(t1_tiny_path)
    text = change(transcript(task))
    report = format_report(text, task)
    assert not report["passed"] and report[issue]
    base = parse_events(transcript(task), task)
    if issue == "duplicate_nodes":
        assert not align_events(base, parse_events(text, task))["pairs"]


def test_out_of_order_and_missing_steps_are_reported(t1_tiny_path):
    task = controlled(t1_tiny_path, multiple=True)
    text = transcript(task)
    steps = text.splitlines()
    assert not format_report("\n".join([steps[1], steps[0], steps[2]]), task)["passed"]
    assert format_report("\n".join(steps[1:]), task)["missing_nodes"] == ["r"]


def test_natural_and_controlled_events_cannot_be_pooled(t1_tiny_path):
    task = controlled(t1_tiny_path)
    natural = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    assert not align_events(parse_events(transcript(task), task), parse_events("q = 0", natural))["pairs"]
    natural_events = parse_events("q = 0", natural)
    natural_events[0].identity = EventIdentity("q", 2, "global")
    assert not align_events(parse_events(transcript(task), task) + natural_events,
                            parse_events(transcript(task), task))["pairs"]
    with pytest.raises(ValueError, match="trajectory conditions"):
        measurement_report([], [task.to_dict(), {**natural.to_dict(), "task_id": "other"}], [], [])


def test_full_scan_and_base_noise_produce_supported_trajectory_rows(t1_tiny_path):
    task = controlled(t1_tiny_path, multiple=True)
    bases = [trace(task, transcript(task, {"r": str(4 + seed)}), f"base{seed}", seed) for seed in range(3)]
    observations = []
    for left, right in permutations(bases, 2):
        observations.extend(cli._sham_observations(task, left, right, right.seed, "noise"))
    for edit in scan_edits(task, 3):
        changed = trace(edit.task, transcript(edit.task), edit.id, edit.metadata["rng_seed"])
        observations.extend(cli._observations(task, bases[changed.seed], changed, edit, f"stream:{changed.seed}", edit.id))
    report = measurement_report([t.to_dict() for t in bases], [task.to_dict()], [o.to_dict() for o in observations], [])
    assert report["passed"]
    assert report["matching_policy"] == MATCHING_POLICY
    assert report["measurement_estimand"] == ESTIMAND
    assert report["overall"]["matched_cell_coverage"] == 1
    assert report["overall"]["common_noise_coverage"] == 1
    assert report["overall"]["rho_coverage"] == 1
    assert report["trajectories"][0]["rho_raw"] == 0
    # r varies across seeds but distractor edits do not change it: excess is signed.
    assert report["trajectories"][0]["rho"] < 0
    assert report["p1_estimability"]["status"] == "single_class"


def test_missing_registered_steps_do_not_shrink_denominator(t1_tiny_path):
    task = controlled(t1_tiny_path, multiple=True)
    full = transcript(task)
    missing = "\n".join(full.splitlines()[1:])
    rows = [trace(task, text, f"base{i}", i).to_dict() for i, text in enumerate((full, missing))]
    report = measurement_report(rows, [task.to_dict()], [], [])
    eligible = sum(len(set(p.premise_id for p in task.premises) - deps) for deps in ancestors(task).values())
    assert [r["eligible_cells"] for r in report["trajectories"]] == [eligible, eligible]
    assert not report["checks"]["registered_step_format"]


def test_intervention_parses_context_but_excludes_already_emitted_steps(t1_tiny_path):
    task = controlled(t1_tiny_path, multiple=True)
    rendered = '<prompt><step node="q">example <commit>999</commit></step><think>'
    full = rendered + transcript(task)
    cut = full.index('<step node="q">', len(rendered))
    body, events = cli._parse_intervention_events(task, full, cut, rendered)
    assert body == transcript(task)
    assert [(e.node_id, e.value) for e in events] == [("q", "0")]
    # A token prefix may split the step tag; reconstructing the entire text resolves it.
    assert cli._parse_intervention_events(task, full, cut + 3, rendered)[1][0].node_id == "q"
    with pytest.raises(ValueError, match="rendered prompt"):
        cli._parse_intervention_events(task, full, cut, "different prompt")


def test_intervention_continuation_inherits_natural_alias_declarations(t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    text = "Let X be q\nX = 4 * 0 = 0\n</think>\\boxed{0}"
    cut = text.index("X = 4")
    body, events = cli._parse_intervention_events(task, text, cut)
    assert body == text and [(e.node_id, e.value) for e in events] == [("q", "0")]


@pytest.mark.parametrize("op", [5, 10, 15, 21])
def test_official_edits_and_source_pairs_preserve_registered_schedule(op):
    from reasoning_diff.edits import make_source_value_pair
    from reasoning_diff.tasks.t1_official import load_igsm_snapshot
    root = Path(__file__).resolve().parents[1] / "artifacts/rd-pr7-qwen200-20261004-light/inputs/igsm-pilot200"
    task = controlled_task(sentence_graph_task(load_igsm_snapshot(sorted(root.glob(f"*-op{op}.json"))[0])))
    plan = task.metadata["quantity_step_plan"]
    pid, value = cli._default_edit(task)
    source = make_source_value_pair(task, pid, value)
    edits = [*scan_edits(task, 3), source["same_value_diff_source"], source["same_source_diff_value"]]
    for edit in edits:
        assert controlled_task(edit.task).metadata["quantity_step_plan"] == plan
        text = transcript(edit.task)
        assert format_report(text, edit.task)["passed"]
        assert len(align_events(parse_events(transcript(task), task), parse_events(text, edit.task))["pairs"]) == len(plan)


class CharTokenizer:
    eos_token_id = None
    is_fast = True

    def apply_chat_template(self, messages, **kwargs):
        import torch
        return torch.tensor([[ord(c) for c in "<user>" + messages[0]["content"] + "</user><think>"]])

    def decode(self, ids, **kwargs):
        return "".join(chr(int(i)) for i in ids)

    def __call__(self, text, **kwargs):
        return {"input_ids": [ord(c) for c in text], "offset_mapping": [[i, i + 1] for i in range(len(text))]}


def test_frozen_generation_keeps_exact_step_prefix_and_protocol_metadata(t1_tiny_path, monkeypatch):
    import torch
    import numpy as np
    from reasoning_diff.models import generate, collect
    task = controlled(t1_tiny_path, multiple=True)
    tokenizer = CharTokenizer()
    model = torch.nn.Linear(1, 1)
    text = transcript(task)
    def decode(_model, prompt_ids, _rng, **kwargs):
        assert kwargs["max_new"] == 4096
        ids = prompt_ids[0].tolist()
        generated = [ord(c) for c in text]
        return {"generated_ids": generated, "token_ids": ids + generated, "stop_reason": "eos"}
    monkeypatch.setattr(generate, "decode_loop", decode)
    packed = {"model": model, "tokenizer": tokenizer, "card": {"id": "fixture", "arch": "qwen3", "context_limit": 10000}, "device": "cpu"}
    result = generate.generate_frozen_trace(task, "qwen3-8b", packed=packed, max_new=4096)
    assert result.metadata["protocol_version"] == PROTOCOL
    assert result.metadata["quantity_step_format"]["passed"]
    assert result.metadata["boundary_status"] == "ok"
    assert not result.metadata["finalizer_used"] and not result.metadata["thinking_forced_close"]
    assert result.status == "natural_complete"
    monkeypatch.setattr(collect, "_n_layers", lambda _: 2)
    monkeypatch.setattr(collect, "_hidden_at_layer", lambda _, ids, layer: np.zeros((len(ids), 2)))
    features = collect.collect_hidden_trace("qwen2", result.token_ids, result.offsets, result.events, task.premises,
                                           model=model, hidden_layer=0, rendered_prompt_text=result.metadata["rendered_prompt_text"],
                                           strict_prompt_spans=True, include_nonthinking_events=False)
    for row, event in zip(features["event_records"], result.events):
        prefix = tokenizer.decode(row["prefix_token_ids"])
        assert prefix == result.text[:event.start]
        assert event.expression_signature == PROTOCOL


def test_prepare_label_and_checkpoint_plan_share_controlled_protocol(t1_tiny_path, tmp_path, monkeypatch):
    from reasoning_diff.models import generate
    from reasoning_diff.io import read_json, read_jsonl
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    batched = importlib.import_module("prepare_batched")
    argv = ["prepare", "--fixture", str(t1_tiny_path), "--out-dir", str(tmp_path / "prepare"), "--eval-mode", "scientific",
            "--premise-protocol", "sentence_graph", "--trajectory-protocol", "quantity_steps", "--noise-reference", "base_pairs",
            "--behavior-repeats", "3", "--checkpoint-traces", "--split-fractions", "0.4", "0.15", "0.1", "0.1", "0.1", "0.15"]
    planned = [(t.task_id, seed, run) for t, seed, run in batched.prepare_requests(cli.build_parser().parse_args(argv))]
    actual = []
    def generated(task, **kwargs):
        assert task.metadata["trajectory_protocol"] == PROTOCOL
        assert not kwargs["allow_forced_target"]
        actual.append((task.task_id, kwargs["seed"], kwargs["run_id"]))
        return trace(task, transcript(task), kwargs["run_id"], kwargs["seed"])
    monkeypatch.setattr(generate, "generate_task_trace", generated)
    assert cli.main(argv) == 0
    assert actual == planned
    prep = tmp_path / "prepare"
    report = measurement_report(read_jsonl(prep / "traces.jsonl"), read_jsonl(prep / "tasks.jsonl"),
                                read_jsonl(prep / "observations.jsonl"), read_jsonl(prep / "splits.jsonl"))
    assert report["passed"]
    assert read_json(prep / "run_spec.json")["config"]["trajectory_protocol"] == "quantity_steps"
    assert cli.main([*argv, "--resume"]) == 0
    assert len(actual) == len(planned)
    assert cli.main(["label", "--in-dir", str(prep), "--out-dir", str(tmp_path / "labels")]) == 0
    labels = read_jsonl(tmp_path / "labels/labels.jsonl")
    assert labels and any(row["behavior_label"] == 1 for row in labels)


@pytest.mark.parametrize("invalid_edit", [False, True])
def test_server_pair_pilot_checks_actual_generated_format_and_resumes(t1_tiny_path, tmp_path, monkeypatch, invalid_edit):
    from reasoning_diff.io import read_json
    from reasoning_diff.models import generate
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    runner = importlib.import_module("run_pr8")
    task = controlled(t1_tiny_path)
    def load(args):
        assert args.trajectory_protocol == "quantity_steps"
        return [task]
    monkeypatch.setattr(cli, "_load_tasks", load)
    monkeypatch.setattr(cli, "_load_frozen_runtime", lambda _: {})
    batching = importlib.import_module("trace_batching")
    class Decoder:
        def __init__(self, _batch_size):
            pass
        def __call__(self):
            return {"batch_execution": {"backend": "fixture"}}
        def close(self):
            pass
    monkeypatch.setattr(batching, "BatchDecoder", Decoder)
    calls = []
    def generated(owner, **kwargs):
        generate.decode_loop()
        calls.append(owner.task_id)
        text = transcript(owner)
        if invalid_edit and "unused_a" in owner.task_id:
            text = text.replace('node="q"', 'node="unknown"')
        return trace(owner, text, kwargs["run_id"], kwargs["seed"])
    monkeypatch.setattr(generate, "generate_task_trace", generated)
    args = SimpleNamespace(dataset=t1_tiny_path, out_root=tmp_path, model="qwen3-8b", max_new=32768,
                           batch_size=2, mode="pilot-worker", trajectory_protocol="quantity_steps")
    runner.pilot_worker(args)
    args.mode = "pair-pilot-worker"
    runner.pilot_worker(args)
    report = read_json(tmp_path / "paired_measurement.json")
    assert report["passed"] is not invalid_edit
    assert report["checks"]["registered_step_format"] is not invalid_edit
    assert report["matching_policy"] == MATCHING_POLICY
    assert len(report["registered_step_formats"]) == 6
    assert len(calls) == 6
    runner.pilot_worker(args)
    assert len(calls) == 6
    args.trajectory_protocol = "natural"
    monkeypatch.setattr(cli, "_load_tasks", lambda _: [task])
    with pytest.raises(ValueError, match="protocol mismatch"):
        runner.pilot_worker(args)


def test_server_rejects_malformed_base_before_paired_scan(t1_tiny_path, tmp_path, monkeypatch):
    from reasoning_diff.io import read_json, write_jsonl
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    runner = importlib.import_module("run_pr8")
    monkeypatch.setitem(__import__("sys").modules, "fcntl", SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *a: None))
    monkeypatch.setattr(runner, "SERVER", tmp_path)
    monkeypatch.setattr(runner.shutil, "disk_usage", lambda _: SimpleNamespace(free=10 * 1024**3))
    monkeypatch.setattr(runner, "cohorts", lambda _: ([t1_tiny_path], [t1_tiny_path]))
    monkeypatch.setattr(runner.subprocess, "check_output", lambda *a, **k: "/dev/mock\n")
    task = controlled(t1_tiny_path)
    calls = []
    def run(command, **kwargs):
        if command[0] == "quota":
            return SimpleNamespace(returncode=0, stdout="")
        calls.append(command)
        assert command[command.index("--trajectory-protocol") + 1] == "quantity_steps"
        dest = Path(command[command.index("--out-root") + 1])
        text = transcript(task) + '<step node="q"><commit>0</commit></step>'
        row = trace(task, text, "base0", 0).to_dict()
        row["events"][0]["event_region"] = "thinking"
        # The check recomputes from text, rather than trusting this stale flag.
        row["metadata"]["quantity_step_format"] = {"passed": True}
        write_jsonl(dest / "traces.jsonl", [row])
        write_jsonl(dest / "tasks.jsonl", [task.to_dict()])
        return SimpleNamespace(returncode=0)
    monkeypatch.setattr(runner.subprocess, "run", run)
    out = tmp_path / "run"
    with pytest.raises(RuntimeError, match="length/parser pilot failed"):
        runner.main(["--mode", "full", "--trajectory-protocol", "quantity_steps", "--dataset", str(tmp_path),
                     "--out-root", str(out), "--gpus", "2"])
    assert not read_json(out / "length_pilot.json")["checks"]["registered_step_format"]
    assert read_json(out / "registered_step_formats.json")["base0"]["answer_steps"] == 1
    assert len(calls) == 1


@pytest.mark.parametrize("invalid_format", [False, True])
def test_scientific_intervention_reconstructs_controlled_steps(t1_tiny_path, tmp_path, monkeypatch, invalid_format):
    import numpy as np
    import torch
    from reasoning_diff.edits import apply_value_edit, make_source_value_pair
    from reasoning_diff.io import read_jsonl, write_json, write_jsonl, write_npz
    from reasoning_diff.models import collect
    task = apply_value_edit(controlled(t1_tiny_path, multiple=True), "p2", "1").task
    pair = make_source_value_pair(task, "p1", "5")
    donor_task = pair["same_source_diff_value"].task
    owners = [task, donor_task]
    traces, rows = [], []
    tokenizer = CharTokenizer()
    for tid, owner in zip(("base", "donor"), owners):
        body = transcript(owner)
        result = trace(owner, body, tid, 0)
        prompt = "<user>" + task_prompt(owner) + "</user><think>"
        result.text = prompt + body
        result.token_ids = [ord(c) for c in result.text]
        result.offsets = [[i, i + 1] for i in range(len(result.text))]
        result.metadata.update(rendered_prompt_text=prompt, rendered_prompt_char_len=len(prompt))
        for event in result.events:
            event.start += len(prompt)
            event.end += len(prompt)
            event.value_start += len(prompt)
        event = result.events[-1]
        rows.append({"trace_id": tid, "node_id": event.node_id, "identity_key": event.identity.key(),
                     "event_region": "thinking", "event_kind": "commit", "event_phase": event.event_phase,
                     "expression_signature": event.expression_signature, "event_scope": "global",
                     "prefix_token_ids": result.token_ids[:event.start]})
        traces.append(result.to_dict())
    features = tmp_path / "features"
    write_jsonl(features / "traces.jsonl", traces)
    write_jsonl(features / "event_rows.jsonl", rows)
    write_jsonl(features / "tasks.jsonl", [t.to_dict() for t in owners])
    write_jsonl(features / "probes.jsonl", [{"head": "behavior", "U": [[1.], [0.]]}])
    write_json(features / "run_spec.json", {"config": {"hidden_layer": 0, "model_kind": "qwen2"}})
    write_npz(features / "features.npz", {"H": np.array([[0., 0.], [1., 1.]])})
    model = torch.nn.Linear(1, 1)
    packed = {"model": model, "tokenizer": tokenizer, "card": {"layers": 2, "context_limit": 10000}, "device": "cpu"}
    monkeypatch.setattr(cli, "_load_frozen_runtime", lambda _: packed)
    monkeypatch.setattr(collect, "_hidden_at_layer", lambda _, ids, layer: np.tile([sum(ids) / 10000., 1.], (len(ids), 1)))
    decoded = []
    def intervene(_kind, ids, layer, **kwargs):
        prefix = traces[0]["metadata"]["rendered_prompt_text"] + transcript(task).splitlines()[0] + "\n"
        assert tokenizer.decode(ids) == prefix
        decoded.append(ids)
        body = "\n".join(transcript(task, {"q": "5"}).splitlines()[1:]).replace("\\boxed{4}", "\\boxed{5}")
        if invalid_format:
            body = body.replace('node="q"', 'node="unknown"')
        baseline = "\n".join(transcript(task).splitlines()[1:])
        return {"generated_ids": [ord(c) for c in body], "baseline_generated_ids": [ord(c) for c in baseline],
                "stop_reason": "eos", "baseline_stop_reason": "eos", "hook": "once", "hook_fired": True,
                "transform": "add_delta", "followed_donor": True, "timing": "pre_step"}
    monkeypatch.setattr(collect, "intervene_hidden_decode", intervene)
    args = cli.build_parser().parse_args(["intervene", "--in-dir", str(features), "--out-dir", str(tmp_path / "intervene"),
                                         "--backend", "frozen", "--model-name", "qwen3-8b", "--eval-mode", "scientific",
                                         "--dev-layer-scores", "0.8", "0.5", "--dev-layer-ids", "0", "1"])
    args._c2_only = True
    args._source_pair = {"trace_ids": {"base": "base", "same_source_diff_value": "donor"},
                         "targets": pair["targets"], "nontargets": pair["nontargets"]}
    assert cli.cmd_intervene(args) == 0
    outputs = read_jsonl(tmp_path / "intervene/interventions.jsonl")
    main = next(row for row in outputs if row["condition"] == "main")
    baseline = next(row for row in outputs if row["condition"] == "baseline")
    assert decoded and main["target"] == int(not invalid_format) and baseline["target"] == 0
    assert main["invalid"] == int(invalid_format)
    assert main["quantity_step_format"]["passed"] is not invalid_format
    assert main["trajectory_protocol"] == PROTOCOL
    assert main["nontarget"] is None and main["nontarget_observable_nodes"] == []
