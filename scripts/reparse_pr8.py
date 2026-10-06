#!/usr/bin/env python3
"""Recompute PR8 measurements from saved text without generating new tokens."""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import replace
from itertools import permutations
from pathlib import Path

from reasoning_diff import cli
from reasoning_diff.artifacts import write_manifest, write_run_spec
from reasoning_diff.events import ALIGNMENT_POLICY, assign_event_regions, parse_events
from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, write_json, write_jsonl
from reasoning_diff.next_round import cached_paired_screen, measurement_report, trace_labels, trajectory_table
from reasoning_diff.schema import Edit, Task, Trace


def reparse_trace(row, task, parser_hash):
    trace = Trace.from_dict(row)
    meta = trace.metadata
    prefix = meta.get("rendered_prompt_text")
    prefix_length = meta.get("rendered_prompt_char_len")
    if not isinstance(prefix, str) or len(prefix) != prefix_length or not trace.text.startswith(prefix):
        raise ValueError(f"cannot establish exact generation boundary for {trace.id}")
    generated = trace.text[prefix_length:]
    events = parse_events(generated, task)
    assign_event_regions(events, generated, initial_thinking=bool(meta.get("enable_thinking")))
    for event in events:
        event.start += prefix_length
        event.end += prefix_length
        event.value_start += prefix_length
        event.run_id = trace.run_id
        event.base_group_id = trace.base_group_id
        event.record_id = f"{trace.id}:{event.identity.key()}"
        if trace.text[event.start:event.end] != event.text:
            raise ValueError(f"reparsed event offset mismatch in {trace.id}")
    trace.events = events
    trace.metadata = {**meta, "measurement_reparse": {
        "original_trace_hash": digest(row), "parser_hash": parser_hash,
        "generated_text_unchanged": True, "token_ids_and_offsets_unchanged": True,
        "answer_score_and_generation_status_unchanged": True,
    }, "parse_status": "boundary_failed" if meta.get("boundary_status") != "ok" else "ok" if events else "parse_failed",
        "target_event_present": any(event.node_id == task.target for event in events)}
    return trace


def summary(traces, table):
    supported = sum(row["support_cells"] for row in table)
    eligible = sum(row["eligible_cells"] for row in table)
    return {"base_traces": len(table), "matched_cells": supported, "eligible_cells": eligible,
            "matched_cell_coverage": supported / eligible if eligible else 0,
            "trajectories_with_rho": sum(row["rho"] is not None for row in table),
            "thinking_calculation_events": sum(
                event.get("event_region") == "thinking" and event.get("event_kind") != "restatement"
                for trace in traces if "trace-base" in trace["id"] or "trace-t0p" in trace["id"]
                for event in trace["events"])}


def final_commitments(trace):
    """A separate entity-level estimand; select by text position, never values."""
    selected = {}
    for event in sorted(trace.events, key=lambda event: (event.start, event.end)):
        if event.event_region == "thinking" and event.event_kind != "restatement" and event.status == "ok":
            selected[(event.identity.entity_or_expression, event.identity.scope)] = event
    events = [replace(event, event_kind="commit", event_phase="final_assignment", expression_signature="entity_final_state")
              for event in sorted(selected.values(), key=lambda event: event.start)]
    return replace(trace, events=events)


def rebuild_observations(traces, tasks, edits, comparisons):
    observations = []
    for row in comparisons.values():
        edit = edits[row["edit_id"]]
        if edit.changed_premise_ids != [row["premise_id"]]:
            raise ValueError("saved observation and edit premise differ")
        observations.extend(cli._observations(tasks[row["task_id"]], traces[row["reference_trace"]],
                                             traces[row["comparison_trace"]], edit, row["rng_pair"], row["run_id"]))
    base = defaultdict(list)
    for trace in traces.values():
        if "trace-base" in trace.id or "trace-t0p" in trace.id:
            base[trace.task_id].append(trace)
    # Reconstruct every registered directed pair, including pairs that had no
    # matched events under the old parser and therefore no saved observation.
    for task_id, group in base.items():
        for left, right in permutations(group, 2):
            observations.extend(cli._sham_observations(tasks[task_id], left, right, right.seed, f"reparse-noise:{task_id}"))
    return observations


def remeasure(source, output, *, report_only=False):
    source, output = source.resolve(), output.resolve()
    if output == source or output.is_relative_to(source) or (output.exists() and any(output.iterdir())):
        raise ValueError("use a new output directory outside the original prepare artifacts")
    filenames = ("tasks.jsonl", "edits.jsonl", "splits.jsonl", "traces.jsonl", "observations.jsonl")
    hashes = {name: file_digest(source / name) for name in filenames}
    manifest = read_json(source / "manifest.json")
    if any(manifest["file_hashes"].get(name) != value for name, value in hashes.items()):
        raise ValueError("original prepare manifest does not match its saved artifacts")
    spec = read_json(source / "run_spec.json")
    sources = list((spec.get("upstream_run_specs") or {}).values()) or [spec]
    if not sources or any(s.get("config", {}).get("noise_reference") != "base_pairs" for s in sources):
        raise ValueError("reparse requires the saved PR8 base-pair noise protocol")
    original = {name: read_jsonl(source / name) for name in filenames}
    tasks = {row["task_id"]: Task.from_dict(row) for row in original["tasks.jsonl"]}
    edits = {row["id"]: Edit.from_dict(row) for row in original["edits.jsonl"] if "task" in row}
    parser_hash = file_digest(Path(cli.__file__).with_name("events.py"))
    measurement_hashes = {path.name: file_digest(path) for path in (
        Path(__file__), Path(cli.__file__), Path(cli.__file__).with_name("events.py"),
        Path(cli.__file__).with_name("next_round.py"))}
    traces = {row["id"]: reparse_trace(row, tasks[row["task_id"]], parser_hash) for row in original["traces.jsonl"]}
    comparisons = {}
    for row in original["observations.jsonl"]:
        if not (row.get("rng_pair") or "").startswith("sham:"):
            key = tuple(row[name] for name in ("reference_trace", "comparison_trace", "edit_id", "rng_pair", "run_id"))
            comparisons.setdefault(key, row)
    observations = rebuild_observations(traces, tasks, edits, comparisons)
    rows = [trace.to_dict() for trace in traces.values()]
    obs_rows = [obs.to_dict() for obs in observations]
    table = trajectory_table(rows, original["tasks.jsonl"], obs_rows, original["splits.jsonl"])
    before = trajectory_table(original["traces.jsonl"], original["tasks.jsonl"], original["observations.jsonl"], original["splits.jsonl"])
    report = {"status": "measurement_reparsed", "scientific_conclusion": None,
              "source_prepare": str(source), "input_hashes": hashes, "parser_hash": parser_hash,
              "measurement_source_hashes": measurement_hashes,
              "n_traces": len(rows), "n_real_comparisons": len(comparisons),
              "matching_policy": ALIGNMENT_POLICY, "coverage_threshold": 0.5,
              "before": summary(original["traces.jsonl"], before), "after": summary(rows, table),
              "formal_launch_ready": False, "remaining_checks": "new features, fits and causal smoke required"}
    quality = measurement_report(rows, original["tasks.jsonl"], obs_rows, original["splits.jsonl"])
    report["measurement_quality"] = quality
    report["cached_paired_screen"] = cached_paired_screen(rows, original["tasks.jsonl"], obs_rows, original["splits.jsonl"])
    if not quality["passed"] or not report["cached_paired_screen"]["passed"]:
        report["remaining_checks"] = "saved measurement checks failed; resolve and audit step correspondence before new generation"
    report["matched_cell_gate_passed"] = quality["checks"]["matched_cell_coverage"]
    final = {key: final_commitments(trace) for key, trace in traces.items()}
    final_rows = [trace.to_dict() for trace in final.values()]
    final_obs = [obs.to_dict() for obs in rebuild_observations(final, tasks, edits, comparisons)]
    final_table = trajectory_table(final_rows, original["tasks.jsonl"], final_obs, original["splits.jsonl"])
    report["final_commitment_diagnostic"] = {
        **summary(final_rows, final_table), "status": "diagnostic_only",
        "estimand": "last_explicit_thinking_assignment_per_entity_and_scope",
        "selection": "text_position_independent_of_answer_values",
        "limitation": "entity-level results do not replace all-step reasoning dependency measurements",
    }
    if hashes != {name: file_digest(source / name) for name in filenames}:
        raise ValueError("original prepare artifacts changed during remeasurement")
    output.mkdir(parents=True, exist_ok=True)
    outputs = {**{name: original[name] for name in ("tasks.jsonl", "edits.jsonl", "splits.jsonl")},
               "traces.jsonl": rows, "observations.jsonl": obs_rows, "p1_table.jsonl": table,
               "final_commitment_p1_table.jsonl": final_table,
               "events.jsonl": [event.to_dict() for trace in traces.values() for event in trace.events],
               "labels.jsonl": [label.to_dict() for label in trace_labels(observations, list(tasks.values()))]}
    if report_only:
        outputs = {}
    report["artifact_scope"] = "measurement_report_only" if report_only else "reparsed_prepare"
    for name, contents in outputs.items():
        write_jsonl(output / name, contents)
    write_json(output / "measurement_report.json", report)
    write_run_spec(output, {"config": {"command": "reparse_pr8", "parser_hash": parser_hash,
                                       "measurement_source_hashes": measurement_hashes,
                                       "matching_policy": report["matching_policy"], "generation_reused": True,
                                       "report_only": report_only},
                            "source_kinds": spec.get("source_kinds"), "input_hashes": hashes,
                            "source_prepare": str(source), "upstream_run_specs": spec})
    write_manifest(output, [output / name for name in (*outputs, "measurement_report.json", "run_spec.json")],
                   {**{name: len(contents) for name, contents in outputs.items()}, "success": 1, "failure": 0},
                   upstream_ids=[read_json(source / "manifest.json")["digest"]])
    print(report["before"], flush=True)
    print(report["after"], flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--report-only", action="store_true", help="Verify measurements and cached pilot without exporting derived trace files")
    args = parser.parse_args()
    remeasure(args.in_dir, args.out_dir, report_only=args.report_only)


if __name__ == "__main__":
    main()
