"""Stage CLI: prepare → collect → label → fit → calibrate → intervene → repair → analyze."""
from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import json
import math
import re
from dataclasses import fields
from pathlib import Path

import numpy as np

from .analysis import classification_metrics, cone_fit, p1_incremental, p2_from_rows, p3_from_rows, retrieval_scatter, week8_decision
from .artifacts import completed_shard_ok, write_manifest, write_run_spec
from .edits import apply_value_edit, make_source_value_pair
from .baselines import (
    attention_mean,
    attention_rollout,
    fit_attention_threshold,
    fit_text_predictor,
    next_variable_to_dag,
    parser_premise_set,
    fit_next_variable_predictor,
    text_predictor,
    verbalizer,
)
from .events import align_events, align_events_monotonic, extract_answer, parse_events, parse_fixture_events, review_export
from .probes.boundary import BoundaryMLP
from .graphs import ancestors
from .interventions import apply_swap, c_layer_delta, c_rand_delta, ie_z, inlp_remove, intervention_report, orthonormal_basis, rescue_controls, select_weak_layer
from .io import digest, file_digest, read_json, read_jsonl, read_npz, write_json, write_jsonl, write_npz
from .measure import build_labels, compare_pair, event_density_sets, preservation_to_csp, probe_prf1
from .models.features import select_prefix_index
from .protocol import answer_score, recursive_manifest, stable_row_key
from .probes.bilinear import BilinearProbe
from .probes.calibrate import conformal_threshold, sequence_score
from .repair import ALL_MASKS, MASKS_MAIN, consecutive_repairs, execute_repair_frozen, execute_repair_tiny, run_repair
from .rng import StreamBank
from .schema import Observation, Task, Trace
from .splits import DEFAULT_FRACTIONS, require_persisted_roles, require_split, split_for_task
from .tasks.catalog import load_snapshot
from .tasks.t1_fixture import load_t1_fixture
from .tasks.t2_noop import make_noop_pair
from .transfer import apply_map, common_dim_then_procrustes, direct_transfer, fit_linear_map


def _load_frozen_runtime(args: argparse.Namespace):
    if getattr(args, "_packed_runtime", None) is not None:
        return args._packed_runtime
    name = getattr(args, "model_name", None)
    if not name:
        raise ValueError("frozen backend requires --model-name")
    from .models.adapters import load_frozen

    packed = load_frozen(name, device=getattr(args, "device", None))
    if getattr(args, "eval_mode", "fixture") == "scientific":
        validation = packed.get("validation") or {}
        if validation.get("validation_status") != "verified":
            raise ValueError(
                "scientific frozen runtime validation failed: "
                f"{validation.get('missing_structure_fields') or validation.get('missing_required_tokenizer_special_ids') or validation.get('validation_status')}"
            )
        requested = getattr(args, "device", None)
        if requested and str(requested).startswith("cuda") and not packed.get("cuda"):
            raise ValueError(f"scientific frozen runtime requested {requested} but loaded device is {packed.get('device')}")
        if not requested and not packed.get("cuda") and (packed.get("card") or {}).get("revision") != "test":
            raise ValueError("scientific frozen runtime requires a verified CUDA device; use fixture mode for CPU smoke tests")
    return packed


def _resolved_max_new(args: argparse.Namespace, tiny_default: int, frozen_default: int) -> int:
    value = getattr(args, "max_new", None)
    if value is not None:
        return int(value)
    return frozen_default if getattr(args, "backend", "tiny") == "frozen" else tiny_default


def _observation_from_dict(data: dict) -> Observation:
    allowed = {item.name for item in fields(Observation)}
    return Observation(**{key: value for key, value in data.items() if key in allowed})


_STAGE_ARTIFACTS = {
    "prepare": ("tasks.jsonl", "traces.jsonl", "observations.jsonl", "labels.jsonl", "splits.jsonl", "trace_quality.json", "audit_sample.jsonl", "input_manifest.json", "run_spec.json"),
    "collect": ("features.npz", "traces.jsonl", "audit_sample.jsonl", "run_spec.json"),
    "label": ("labels.jsonl", "run_spec.json"),
    "fit": ("probes.jsonl", "probe_predictions.jsonl", "p1_table.jsonl", "dev_layer_scores.json", "run_spec.json"),
    "calibrate": ("calibration.jsonl", "run_spec.json"),
    "intervene": ("interventions.jsonl", "run_spec.json"),
    "repair": ("repairs.jsonl", "run_spec.json"),
    "transfer": ("transfer.jsonl", "run_spec.json"),
    "noop": ("noop.jsonl", "noop_pairs.jsonl", "p2_table.jsonl", "run_spec.json"),
    "analyze": ("analysis.jsonl", "report.json", "run_spec.json"),
}


def _resume(out: Path, resume: bool, config: dict | None = None, input_hashes: dict | None = None) -> bool:
    if not resume:
        return False
    manifest = out / "manifest.json"
    if not manifest.exists():
        return False
    body = read_json(manifest)
    if int(body.get("success_count") or 0) < 1 or int(body.get("failure_count") or 0) > 0:
        return False
    command = (config or {}).get("command")
    for name in _STAGE_ARTIFACTS.get(command, ()):
        if not (out / name).exists():
            return False
    for name, digest in body.get("file_hashes", {}).items():
        path = out / name
        if name == "manifest.json":
            continue
        if not path.exists() or file_digest(path) != digest:
            raise ValueError(f"resume hash mismatch or missing file: {name}")
    spec = out / "run_spec.json"
    if spec.exists() and (config or input_hashes):
        prev = read_json(spec)
        prev_cfg = prev.get("config", {})
        for key, value in (config or {}).items():
            if prev_cfg.get(key) != value:
                raise ValueError(f"resume run_spec mismatch: {key}")
        prev_hash = prev.get("input_hashes") or {}
        for key, value in (input_hashes or {}).items():
            if prev_hash.get(key) != value:
                raise ValueError(f"resume input identity mismatch: {key}")
    digest = body.get("digest")
    check = {k: v for k, v in body.items() if k != "digest"}
    from .io import digest as digest_obj

    if digest and digest != digest_obj(check):
        raise ValueError("resume manifest digest is not self-consistent")
    stale_failure = out / "failure.json"
    if stale_failure.exists():
        stale_failure.unlink()
    return True


def _upstream(*dirs: Path | None) -> tuple[dict, list]:
    hashes = {}
    upstream = []
    for in_dir in dirs:
        if in_dir is None:
            continue
        if in_dir.exists() and in_dir.is_file():
            raise NotADirectoryError(f"--in-dir must be a directory: {in_dir}")
        if not in_dir.exists():
            continue
        prefix = in_dir.name + "/"
        manifest = in_dir / "manifest.json"
        if manifest.exists():
            hashes[prefix + "upstream_manifest"] = file_digest(manifest)
            body = read_json(manifest)
            recomputed = {k: v for k, v in body.items() if k != "digest"}
            from .io import digest as digest_obj

            hashes[prefix + "upstream_manifest_recomputed"] = digest_obj(recomputed)
            upstream.append(digest_obj(recomputed))
        for path in sorted(in_dir.iterdir()):
            if path.is_file() and path.name != "manifest.json":
                hashes[prefix + path.name] = file_digest(path)
    return hashes, [item for item in upstream if item]


def _trace_text(task: Task) -> str:
    lines = [p.text for p in task.premises if p.kind != "placeholder"]
    lines.extend(f"{node.aliases[0] if node.aliases else node.id} = {node.value}" for node in task.nodes)
    return ("\n".join(lines) + "\n") if lines else (task.question + "\n")


def _synthetic_trace(task, text: str, trace_id: str, seed: int) -> Trace:
    score = answer_score(task.answer_spec.value, task.answer_spec.value, task.answer_spec.kind, task.answer_spec.aliases)
    events = parse_fixture_events(text, task)
    for event in events:
        event.event_region = "answer"
        event.run_id = trace_id
        event.base_group_id = task.base_group_id
        event.record_id = f"{trace_id}:{event.identity.key()}"
    tokens = list(range(1, len(text) + 1))
    offsets = [[i, i + 1] for i in range(len(text))]
    return Trace(
        id=trace_id,
        task_id=task.task_id,
        base_group_id=task.base_group_id,
        model="fixture",
        seed=seed,
        text=text,
        token_ids=tokens,
        offsets=offsets,
        events=events,
        answer=task.answer_spec.value,
        correct=score.get("correct"),
        status="natural_complete",
        metadata={
            "evidence_status": "fixture_synthetic",
            "protocol_version": "fixture_synthetic_v1",
            "trace_status": "natural_complete",
            "answer_status": "structured_fixture",
            "analysis_eligibility": {"C1": False, "C2": True, "C3": True, "C4": True},
            **score,
        },
        run_id=trace_id,
        record_id=trace_id,
    )


def _trace_quality(traces: list[Trace]) -> dict:
    """Summarize generated trace quality without dropping failures."""
    counts = {
        "total": len(traces),
        "valid": 0,
        "missing_answer": 0,
        "missing_events": 0,
        "parse_failed": 0,
        "truncated": 0,
        "forced_target": 0,
        "correct": 0,
        "missing_target": 0,
        "duplicate_events": 0,
        "structural_failures": 0,
        "boundary_failed": 0,
        "natural_complete": 0,
        "natural_truncated": 0,
        "answer_missing_status": 0,
    }
    failures = []
    by_family = {}
    for trace in traces:
        metadata = trace.metadata or {}
        trace_status = str(metadata.get("trace_status") or trace.status or "unknown")
        if trace_status == "natural_complete":
            counts["natural_complete"] += 1
        elif trace_status == "natural_truncated":
            counts["natural_truncated"] += 1
        elif trace_status == "answer_missing":
            counts["answer_missing_status"] += 1
        family = str(trace.id).split(":", 1)[0] or "unknown"
        family_counts = by_family.setdefault(family, {"total": 0, "valid": 0, "correct": 0, "statuses": {}})
        family_counts["total"] += 1
        family_counts["statuses"][trace_status] = family_counts["statuses"].get(trace_status, 0) + 1
        has_events = bool(trace.events) and metadata.get("parse_status") not in {"parse_failed", "boundary_failed", "constrained_target"}
        has_answer = trace.answer is not None
        if has_events and has_answer:
            counts["valid"] += 1
            family_counts["valid"] += 1
        else:
            if not has_events:
                counts["missing_events"] += 1
            if metadata.get("parse_status") in {"parse_failed", "boundary_failed", "constrained_target"}:
                counts["parse_failed"] += 1
            if not has_answer:
                counts["missing_answer"] += 1
            failures.append(
                {
                    "trace_id": trace.id,
                    "task_id": trace.task_id,
                    "parse_status": metadata.get("parse_status"),
                    "stop_reason": metadata.get("stop_reason"),
                    "answer_present": has_answer,
                    "event_count": len(trace.events),
                    "failure_class": metadata.get("structure_status") or ("missing_events" if not has_events else "missing_answer"),
                }
            )
        if metadata.get("target_event_present") is False:
            counts["missing_target"] += 1
        if metadata.get("duplicate_event_identities"):
            counts["duplicate_events"] += 1
        if metadata.get("structure_status") in {"merged", "split", "route_changed", "duplicate"}:
            counts["structural_failures"] += 1
        if metadata.get("parse_status") == "boundary_failed":
            counts["boundary_failed"] += 1
        if metadata.get("stop_reason") == "max_new":
            counts["truncated"] += 1
        if metadata.get("forced_target"):
            counts["forced_target"] += 1
        if trace.correct is True:
            counts["correct"] += 1
            family_counts["correct"] += 1
    return {
        "status": "complete" if not failures else "partial",
        "counts": counts,
        "by_trace_family": by_family,
        "failures": failures,
    }


def _write_stage(
    out: Path,
    name: str,
    rows: list,
    extra_files: list | None = None,
    counts: dict | None = None,
    in_dir: Path | None = None,
    extra_dir: Path | None = None,
    config: dict | None = None,
) -> None:
    hashes, upstream = _upstream(in_dir, extra_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.jsonl"
    write_jsonl(path, rows)
    extras = [Path(item) for item in (extra_files or []) if Path(item).exists()]
    files = [path, *extras]
    merged = {
        "command": name,
        "timing_protocol": "stage_wall_clock_not_substeped",
        "timing_status": "unmeasured_without_runtime_timer",
        **(config or {}),
    }
    source_kinds = dict((config or {}).get("source_kinds") or {})
    upstream_provenance = []
    for upstream_dir in (in_dir, extra_dir):
        if upstream_dir is None:
            continue
        upstream_spec = Path(upstream_dir) / "run_spec.json"
        if upstream_spec.exists():
            try:
                spec = read_json(upstream_spec)
                source_kinds.update(spec.get("source_kinds") or {})
                upstream_provenance.append(
                    {
                        "path": str(upstream_spec),
                        "code_revision": spec.get("code_revision"),
                        "models": spec.get("models") or {},
                        "config": spec.get("config") or {},
                    }
                )
            except (OSError, TypeError, ValueError):
                pass
    if not source_kinds:
        for candidate in (in_dir, extra_dir):
            task_file = candidate / "tasks.jsonl" if candidate is not None else None
            if task_file is None or not task_file.exists():
                continue
            try:
                task_rows = read_jsonl(task_file)
                source_kinds = {
                    f"task:{row.get('task_id')}": str(row.get("source_kind"))
                    for row in task_rows
                    if row.get("task_id") and row.get("source_kind")
                }
                if source_kinds:
                    break
            except (OSError, TypeError, ValueError):
                pass
    if not source_kinds:
        source_kinds = {"cli": "fixture"}
    stale_failure = out / "failure.json"
    if stale_failure.exists():
        stale_failure.unlink()
    write_run_spec(
        out,
        {
            "config": merged,
            "source_kinds": source_kinds,
            "rng": {"stream": name},
            "input_hashes": hashes,
            "provenance": upstream_provenance,
        },
    )
    files.append(out / "run_spec.json")
    report = out / "report.json"
    if report.exists() and report not in files:
        files.append(report)
    write_manifest(out, files, counts or {name: len(rows), "success": 1, "failure": 0}, upstream_ids=upstream)


def _default_edit(task: Task) -> tuple[str, str]:
    facts = [p for p in task.premises if p.kind != "placeholder"]
    if task.metadata.get("premise_protocol") == "sentence_graph_v1":
        needed = ancestors(task).get(task.target, set())
        facts = [p for p in facts if p.premise_id in needed and p.kind != "relation"]
        if not facts:
            raise ValueError("no editable numeric source premise")
        picked = next((p for p in facts if p.value in {"0", "0.0"}), facts[-1])
        return picked.premise_id, "1" if picked.value == "2" else "2"
    editable = [
        p
        for p in facts
        if p.value and re.search(rf"(?<![\d.]){re.escape(p.value.replace(',', ''))}(?![\d.])", p.text.replace(',', ''))
    ]
    zero = next((p for p in editable if p.value in {"0", "0.0"}), None)
    if zero is not None:
        return zero.premise_id, "2"
    if editable:
        return editable[-1].premise_id, "2"
    raise ValueError("no editable non-placeholder premise")


def _load_tasks(args) -> list[Task]:
    if getattr(args, "premise_protocol", "leaf") == "sentence_graph":
        from .next_round import sentence_graph_task
        legacy = copy.copy(args)
        legacy.premise_protocol = "leaf"
        return [sentence_graph_task(task) for task in _load_tasks(legacy)]
    kind = getattr(args, "kind", "t1_fixture")
    if kind in {None, "t1_fixture"}:
        return [load_t1_fixture(args.fixture)]
    path = getattr(args, "snapshot", None) or args.fixture
    sidecar = read_json(args.sidecar) if getattr(args, "sidecar", None) else None
    if kind == "igsm" and Path(path).is_dir():
        from .tasks.t1_official import load_igsm_directory

        return list(load_igsm_directory(path))
    if kind in {"gsm_symbolic", "t2_gsm_symbolic", "symbolic"}:
        from .tasks.t2_gsm_symbolic import load_gsm_symbolic

        target = Path(path)
        files = sorted(target.glob("*.json")) if target.is_dir() else [target]
        return [load_gsm_symbolic(item, sidecar=sidecar) for item in files]
    loaded = load_snapshot(kind, path)
    return loaded if isinstance(loaded, list) else [loaded]


def _load_task(args) -> Task:
    return _load_tasks(args)[0]


def _domain_edit(task: Task, args) -> object:
    if task.source == "humaneval_derived":
        from .tasks.t3_humaneval import apply_spec_edit

        return apply_spec_edit(task, task.question + "\n# variant", task.metadata.get("test") or "assert True", None, edit_kind="input_list")
    if task.source == "gsm_plus":
        from .tasks.t2_gsm_plus import apply_plus_numeric_edit

        return apply_plus_numeric_edit(task, "4", "5")
    if task.source == "t4_boundary":
        from .tasks.t4_boundary import apply_t4_question_edit

        return apply_t4_question_edit(task, task.question + " ?")
    if task.source == "hotpotqa":
        from .tasks.t3_hotpot import document_edit

        doc = next((p.document_id for p in task.premises if p.document_id), None)
        if doc:
            return document_edit(task, doc, "replacement")["edit"]
    if task.source == "musique":
        from .tasks.t3_musique import paragraph_edit

        if task.premises:
            return paragraph_edit(task, task.premises[0].premise_id, "replacement only")
    premise_id, fallback = _default_edit(task)
    premise_id = getattr(args, "edit_premise", None) or premise_id
    return apply_value_edit(task, premise_id, getattr(args, "edit_value", None) or fallback)


def _allowed_edits(task: Task, repeats: int = 1) -> list:
    if task.metadata.get("premise_protocol") == "sentence_graph_v1":
        from .next_round import scan_edits
        return scan_edits(task, max(1, int(repeats)))
    edits = []
    repeats = max(1, int(repeats))
    for premise in task.premises:
        if premise.kind == "placeholder" or not premise.value:
            continue
        for repeat in range(repeats):
            try:
                candidates = ["2", "0", "1"]
                alt = candidates[repeat % len(candidates)]
                if alt == premise.value:
                    alt = candidates[(repeat + 1) % len(candidates)]
                edit = apply_value_edit(task, premise.premise_id, alt)
                edit.exhaustive = repeats > 1
                edit.metadata = {
                    **edit.metadata,
                    "perturbation_id": f"{premise.premise_id}:{repeat}",
                    "rng_stream": f"perturbation:{repeat}",
                    "rng_seed": int(repeat),
                    "allowed_values": candidates,
                    "scan_protocol": "multi_seed_value_edit",
                }
                edits.append(edit)
            except ValueError:
                continue
    return edits


def _scan_run_id(edit):
    prefix = "trace-scan" if edit.task.metadata.get("premise_protocol") == "sentence_graph_v1" else "trace"
    return f"{prefix}-{edit.id}"


def _observations(task, base_trace, edit_trace, edit, rng_pair: str, run_id: str) -> list[Observation]:
    aligned = align_events(base_trace.events, edit_trace.events)
    rows = []
    premise_id = edit.changed_premise_ids[0] if edit.changed_premise_ids else ""
    edit_id = edit.id
    if not base_trace.events and not edit_trace.events:
        rows.append(
            Observation(
                observation_id=f"obs:{run_id}:parse_failed:{edit_id}:{premise_id}",
                reference_trace=base_trace.id,
                comparison_trace=edit_trace.id,
                edit_id=edit_id,
                premise_id=premise_id,
                event_pair=["", ""],
                outcome="parse_failed",
                raw_values=[None, None],
                alignment_ref="",
                rng_pair=rng_pair,
                scan_state="unknown",
                exhaustive=bool(edit.exhaustive),
                base_group_id=task.base_group_id,
                run_id=run_id,
                record_id=f"{run_id}:parse_failed:{premise_id}",
                node_id="",
                task_id=task.task_id,
            )
        )
        rows[0].structure_taxonomy = "parse_failed"
        rows[0].boundary_status = "unknown"
        return rows
    for left, right in aligned["pairs"]:
        ident = left.identity.key()
        rows.append(
            Observation(
                observation_id=f"obs:{run_id}:{ident}:{edit_id}:{premise_id}",
                reference_trace=base_trace.id,
                comparison_trace=edit_trace.id,
                edit_id=edit_id,
                premise_id=premise_id,
                event_pair=[ident, right.identity.key()],
                outcome=compare_pair(left, right),
                raw_values=[left.value, right.value],
                alignment_ref=ident,
                rng_pair=rng_pair,
                scan_state="observed_response",
                exhaustive=bool(edit.exhaustive),
                base_group_id=task.base_group_id,
                run_id=run_id,
                record_id=f"{run_id}:{ident}:{edit_id}:{premise_id}",
                node_id=left.node_id,
                task_id=task.task_id,
            )
        )
    for key in aligned["removed"]:
        rows.append(
            Observation(
                observation_id=f"obs:{run_id}:{key}:{edit_id}:{premise_id}:removed",
                reference_trace=base_trace.id,
                comparison_trace=edit_trace.id,
                edit_id=edit_id,
                premise_id=premise_id,
                event_pair=[key, ""],
                outcome="structural",
                raw_values=[None, None],
                alignment_ref=key,
                rng_pair=rng_pair,
                scan_state="unscanned",
                exhaustive=bool(edit.exhaustive),
                base_group_id=task.base_group_id,
                run_id=run_id,
                record_id=f"{run_id}:{key}:{edit_id}:removed",
                node_id=key.split(":")[0] if key else "",
                task_id=task.task_id,
            )
        )
    for key in aligned["added"]:
        rows.append(
            Observation(
                observation_id=f"obs:{run_id}:{key}:{edit_id}:{premise_id}:added",
                reference_trace=base_trace.id,
                comparison_trace=edit_trace.id,
                edit_id=edit_id,
                premise_id=premise_id,
                event_pair=["", key],
                outcome="structural",
                raw_values=[None, None],
                alignment_ref=key,
                rng_pair=rng_pair,
                scan_state="unscanned",
                exhaustive=bool(edit.exhaustive),
                base_group_id=task.base_group_id,
                run_id=run_id,
                record_id=f"{run_id}:{key}:{edit_id}:added",
                node_id=key.split(":")[0] if key else "",
                task_id=task.task_id,
            )
        )
    for row in rows:
        if row.outcome == "structural":
            row.structure_taxonomy = "removed_or_added"
        elif row.outcome == "unaligned":
            row.structure_taxonomy = "unaligned"
        else:
            row.structure_taxonomy = "matched"
        row.boundary_status = "ok" if (base_trace.metadata or {}).get("boundary_status", "ok") == "ok" else "fallback_cursor"
    return rows


def _sham_observations(task: Task, base_trace: Trace, sham_trace: Trace, seed: int, run_id: str) -> list[Observation]:
    """Create a matched, semantic-preserving sampled sham comparison."""
    rows = []
    for left, right in align_events(base_trace.events, sham_trace.events)["pairs"]:
        key = left.node_id or left.identity.key()
        identity = digest([task.task_id, base_trace.id, sham_trace.id, left.identity.key(), right.identity.key(), seed, run_id])
        rows.append(
            Observation(
                observation_id=f"obs:{run_id}:{identity}",
                reference_trace=base_trace.id,
                comparison_trace=sham_trace.id,
                edit_id="sham:no_edit_sampled",
                premise_id=f"sham:{key}",
                event_pair=[key, right.node_id or right.identity.key()],
                outcome=compare_pair(left, right),
                raw_values=[left.value, right.value],
                alignment_ref=left.identity.key(),
                rng_pair=f"sham:{seed}",
                scan_state="observed_response",
                base_group_id=task.base_group_id,
                run_id=run_id,
                record_id=f"{run_id}:{identity}",
                node_id=left.node_id,
                task_id=task.task_id,
            )
        )
    return rows


def cmd_prepare(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    tasks = _load_tasks(args)
    if not tasks:
        raise ValueError("prepare received no tasks")
    task = tasks[0]
    fractions = tuple(args.split_fractions) if getattr(args, "split_fractions", None) else DEFAULT_FRACTIONS
    role = split_for_task(task, seed=args.split_seed, fractions=fractions)
    eval_mode = getattr(args, "eval_mode", "fixture")
    if eval_mode == "scientific" and not getattr(args, "split_fractions", None):
        raise ValueError("scientific mode requires explicit --split-fractions")
    if eval_mode == "scientific" and getattr(args, "disable_thinking", False):
        raise ValueError("scientific reasoning traces require thinking; use fixture mode for a non-thinking comparison")
    try:
        edit = _domain_edit(task, args)
    except ValueError:
        if eval_mode == "scientific":
            raise
        premise_id, fallback = _default_edit(task)
        edit = apply_value_edit(task, getattr(args, "edit_premise", None) or premise_id, getattr(args, "edit_value", None) or fallback)
    premise_id = edit.changed_premise_ids[0] if edit.changed_premise_ids else ""
    new_literal = next(iter(edit.after.values()), "")
    config = {
        "command": "prepare",
        "edit_premise": getattr(args, "edit_premise", None) or premise_id,
        "edit_value": getattr(args, "edit_value", None) or new_literal,
        "eval_mode": eval_mode,
        "kind": getattr(args, "kind", "t1_fixture"),
        "premise_protocol": getattr(args, "premise_protocol", "leaf"),
        "noise_reference": getattr(args, "noise_reference", "independent_sham"),
        "split_seed": args.split_seed,
        "split_fractions": list(fractions),
        "weight_seed": getattr(args, "weight_seed", 0),
        "backend": getattr(args, "backend", "tiny"),
        "model_name": getattr(args, "model_name", None),
        "device": getattr(args, "device", None),
        # The scientific pilot must expose the natural length distribution;
        # there is no hidden 768-token close or other truncation here.
        "max_new": _resolved_max_new(args, 8, 4096 if eval_mode == "scientific" else 256),
        "temperature": getattr(args, "temperature", 0.6),
        "top_k": getattr(args, "top_k", 20),
        "top_p": getattr(args, "top_p", 0.95),
        "enable_thinking": not getattr(args, "disable_thinking", False),
        "code_revision": getattr(args, "code_revision", None),
        "require_valid_traces": False,
        "quality_gate": "disabled_scientific_failures_retained",
        "behavior_repeats": int(getattr(args, "behavior_repeats", None) or (3 if eval_mode == "scientific" else 1)),
        "n_generation_seeds": max(
            3 if eval_mode == "scientific" else 1,
            int(getattr(args, "n_seeds", None) or (3 if eval_mode == "scientific" else 1)),
        ),
        # Match the no-edit reference opportunities to the per-premise edit
        # repetitions so noise is estimated on the same opportunity count.
        "sham_opportunities": (
            max(
                1,
                int(getattr(args, "sham_opportunities", 0) or 0),
                int(getattr(args, "behavior_repeats", None) or (3 if eval_mode == "scientific" else 1)),
            )
            if eval_mode == "scientific"
            else int(getattr(args, "sham_opportunities", 0) or 0)
        ),
        # Scientific traces are always natural model output.  Forced target
        # assignment remains available only on the non-scientific fixture path.
        "allow_forced_target": eval_mode != "scientific",
        "n_tasks": len(tasks),
        "task_ids": [item.task_id for item in tasks],
        "family_counts": dict(Counter(item.base_group_id for item in tasks)),
        "op_distribution": dict(Counter(str(item.metadata.get("op")) for item in tasks if item.metadata.get("op") is not None)),
    }
    if config["noise_reference"] == "base_pairs":
        config["sham_opportunities"] = 0
    checkpoints = None
    if getattr(args, "checkpoint_traces", False):
        config["checkpoint_traces"] = True
        config["source_hash"] = digest({
            path.relative_to(Path(__file__).parent).as_posix(): file_digest(path)
            for path in sorted(Path(__file__).parent.rglob("*.py"))
        })
    input_manifest = recursive_manifest(args.fixture, loader_version="reasoning_diff.tasks.catalog")
    input_hashes = {Path(args.fixture).name: input_manifest["manifest_hash"]}
    if _resume(out, getattr(args, "resume", False), config, input_hashes):
        return 0
    packed = (
        _load_frozen_runtime(args)
        if getattr(args, "backend", "tiny") == "frozen" and eval_mode == "scientific"
        else None
    )
    if packed is not None:
        card_info = packed.get("card") or {}
        validation = packed.get("validation") or {}
        config.update(
            {
                "model_revision": card_info.get("revision"),
                "tokenizer_revision": card_info.get("revision"),
                "dtype": packed.get("dtype"),
                "runtime_device": packed.get("device"),
                "attention_backend": validation.get("attention_backend"),
                "model_validation": validation,
            }
        )
    gen_kw = {
        "weight_seed": getattr(args, "weight_seed", 0),
        "backend": getattr(args, "backend", "tiny"),
        "model_name": getattr(args, "model_name", None),
        "packed": packed,
        "max_new": config["max_new"],
        "temperature": getattr(args, "temperature", 0.6),
        "top_k": getattr(args, "top_k", 20),
        "top_p": getattr(args, "top_p", 0.95),
        "allow_forced_target": config["allow_forced_target"],
        "enable_thinking": config["enable_thinking"],
        "device": getattr(args, "device", None),
    }
    if eval_mode == "scientific":
        from .models.generate import generate_task_trace
        from .tasks.t1_config import validate_t1_prepare_config

        generate = generate_task_trace
        if getattr(args, "checkpoint_traces", False):
            from .checkpoints import TraceCheckpoints

            checkpoints = TraceCheckpoints(
                out, {"config": config, "input_hashes": input_hashes},
                resume=getattr(args, "resume", False),
            )
            generate = checkpoints.wrap(generate_task_trace)
        ops = getattr(args, "t1_ops", None)
        if ops:
            declared_n = len(tasks)
            if task.source_kind == "official":
                validate_t1_prepare_config({"ops": ops, "n_problems": declared_n, "mod": 23})
            else:
                config["t1_protocol_status"] = "fixture_pilot_n_problems_mismatch"
            config["t1_ops"] = list(ops)
            config["t1_n_problems"] = declared_n
        generation_seeds = list(range(config["n_generation_seeds"]))
        base_by_seed = {}
        edit_by_seed = {}
        traces = []
        observations = []
        for generation_seed in generation_seeds:
            base_id = "trace-base" if generation_seed == 0 else ("trace-t0p" if generation_seed == 1 else f"trace-base:seed{generation_seed}")
            base_by_seed[generation_seed] = generate(task, seed=generation_seed, run_id=base_id, **gen_kw)
            traces.append(base_by_seed[generation_seed])
        for generation_seed in generation_seeds:
            edit_id = "trace-edit" if generation_seed == 0 else f"trace-edit:seed{generation_seed}"
            edit_by_seed[generation_seed] = generate(edit.task, seed=generation_seed, run_id=edit_id, **gen_kw)
            traces.append(edit_by_seed[generation_seed])
        for generation_seed in generation_seeds:
            observations.extend(
                _observations(
                    task,
                    base_by_seed[generation_seed],
                    edit_by_seed[generation_seed],
                    edit,
                    f"stream:{generation_seed}",
                    f"prepare:seed{generation_seed}",
                )
            )
        base_trace = base_by_seed[0]
        edit_trace = edit_by_seed[0]
        pair = _try_source_value_pair(task, premise_id, new_literal or "2")
        if pair:
            src_trace = generate(pair["same_value_diff_source"].task, seed=0, run_id="trace-source", **gen_kw)
            traces.append(src_trace)
        for extra in _allowed_edits(task, config["behavior_repeats"]):
            extra_seed = int(extra.metadata.get("rng_seed", 0))
            extra_trace = generate(extra.task, seed=extra_seed, run_id=_scan_run_id(extra), **gen_kw)
            traces.append(extra_trace)
            paired_base = base_by_seed.get(extra_seed, base_trace)
            observations.extend(_observations(task, paired_base, extra_trace, extra, f"stream:{extra_seed}", f"prepare:{extra.id}"))
        for generation_seed in generation_seeds:
            paired_base = base_by_seed[generation_seed]
            for opportunity in range(config["sham_opportunities"]):
                sham_seed = 1000 + generation_seed * config["sham_opportunities"] + opportunity
                sham_id = "trace-sham" if generation_seed == 0 and opportunity == 0 else f"trace-sham:{generation_seed}:{opportunity}"
                sham_trace = generate(task, seed=sham_seed, run_id=sham_id, **gen_kw)
                traces.append(sham_trace)
                observations.extend(_sham_observations(task, paired_base, sham_trace, sham_seed, "prepare-sham"))
        if checkpoints is not None:
            checkpoints.task_complete(task)
    else:
        pair = _try_source_value_pair(task, premise_id, new_literal or "2")
        base_text = _trace_text(task)
        edited_text = _trace_text(edit.task)
        base_trace = _synthetic_trace(task, base_text, "trace-base", 0)
        edit_trace = _synthetic_trace(edit.task, edited_text, "trace-edit", 0)
        traces = [base_trace, edit_trace]
        if pair:
            source_task = pair["same_value_diff_source"].task
            traces.append(_synthetic_trace(source_task, _trace_text(source_task), "trace-source", 0))
        observations = _observations(task, base_trace, edit_trace, edit, "stream:0", "prepare")
        if config["sham_opportunities"]:
            sham_trace = _synthetic_trace(task, base_text, "trace-sham", 1)
            traces.append(sham_trace)
            observations.extend(_sham_observations(task, base_trace, sham_trace, 1, "prepare-sham"))
    extra_scan_edits = list(_allowed_edits(task, config["behavior_repeats"]))
    source_value_pairs = []
    task_rows = [task.to_dict(), edit.task.to_dict()]
    split_rows = [
        {
            "base_group_id": task.base_group_id,
            "role": role,
            "source": task.source,
            "fractions": list(fractions),
            "split_seed": args.split_seed,
            "task_id": task.task_id,
        }
    ]
    extra_edit_rows = [item.to_dict() for item in extra_scan_edits]
    # Extra perturbation traces are real task variants too.  Persist their
    # task rows so collect can resolve each trace to its own premise text and
    # answer specification instead of falling back to tasks[0].
    task_rows.extend(item.task.to_dict() for item in extra_scan_edits)
    split_rows.extend(
        {
            "base_group_id": task.base_group_id,
            "role": role,
            "source": task.source,
            "fractions": list(fractions),
            "split_seed": args.split_seed,
            "task_id": item.task.task_id,
            "variant_kind": "behavior_scan",
        }
        for item in extra_scan_edits
    )
    for idx, extra_task in enumerate(tasks[1:], start=1):
        extra_role = split_for_task(extra_task, seed=args.split_seed, fractions=fractions)
        try:
            extra_edit = _domain_edit(extra_task, args)
        except ValueError:
            if eval_mode == "scientific":
                raise
            extra_pid, extra_fallback = _default_edit(extra_task)
            extra_edit = apply_value_edit(extra_task, extra_pid, extra_fallback)
        if eval_mode == "scientific":
            from .models.generate import generate_task_trace
            extra_bases = {}
            extra_edits = {}
            for generation_seed in generation_seeds:
                base_id = f"trace-base:{idx}" if generation_seed == 0 else f"trace-base:{idx}:seed{generation_seed}"
                edit_id = f"trace-edit:{idx}" if generation_seed == 0 else f"trace-edit:{idx}:seed{generation_seed}"
                extra_bases[generation_seed] = generate(extra_task, seed=generation_seed, run_id=base_id, **gen_kw)
                extra_edits[generation_seed] = generate(extra_edit.task, seed=generation_seed, run_id=edit_id, **gen_kw)
                traces.extend([extra_bases[generation_seed], extra_edits[generation_seed]])
                observations.extend(
                    _observations(
                        extra_task,
                        extra_bases[generation_seed],
                        extra_edits[generation_seed],
                        extra_edit,
                        f"stream:{generation_seed}",
                        f"prepare:{idx}:seed{generation_seed}",
                    )
                )
            extra_base = extra_bases[0]
            extra_edit_tr = extra_edits[0]
            # Scan every problem, not only the first task in each shard.
            for scan_edit in _allowed_edits(extra_task, config["behavior_repeats"]):
                scan_seed = int(scan_edit.metadata.get("rng_seed", 0))
                scan_trace = generate(scan_edit.task, seed=scan_seed, run_id=_scan_run_id(scan_edit), **gen_kw)
                traces.append(scan_trace)
                observations.extend(_observations(extra_task, extra_bases[scan_seed], scan_trace, scan_edit,
                                                 f"stream:{scan_seed}", f"prepare:{scan_edit.id}"))
                task_rows.append(scan_edit.task.to_dict())
                extra_edit_rows.append(scan_edit.to_dict())
                split_rows.append({"base_group_id": extra_task.base_group_id, "task_id": scan_edit.task.task_id,
                                   "role": extra_role, "variant_kind": "behavior_scan", "source": extra_task.source})
        else:
            extra_base = _synthetic_trace(extra_task, _trace_text(extra_task), f"trace-base:{idx}", 0)
            extra_edit_tr = _synthetic_trace(extra_edit.task, _trace_text(extra_edit.task), f"trace-edit:{idx}", 0)
            traces.extend([extra_base, extra_edit_tr])
            observations.extend(_observations(extra_task, extra_base, extra_edit_tr, extra_edit, "stream:0", f"prepare:{idx}"))
        if config["sham_opportunities"]:
            sham_generation_seeds = generation_seeds if eval_mode == "scientific" else [0]
            for generation_seed in sham_generation_seeds:
                paired_base = extra_bases[generation_seed] if eval_mode == "scientific" else extra_base
                for opportunity in range(config["sham_opportunities"]):
                    sham_seed = 2000 + idx * config["n_generation_seeds"] * config["sham_opportunities"] + generation_seed * config["sham_opportunities"] + opportunity
                    sham_id = f"trace-sham:{idx}:{generation_seed}:{opportunity}" if eval_mode == "scientific" else f"trace-sham:{idx}:{opportunity}"
                    if eval_mode == "scientific":
                        extra_sham = generate(extra_task, seed=sham_seed, run_id=sham_id, **gen_kw)
                    else:
                        extra_sham = _synthetic_trace(extra_task, _trace_text(extra_task), sham_id, sham_seed)
                    traces.append(extra_sham)
                    observations.extend(_sham_observations(extra_task, paired_base, extra_sham, sham_seed, f"prepare-sham:{idx}:seed{generation_seed}"))
        task_rows.extend([extra_task.to_dict(), extra_edit.task.to_dict()])
        extra_edit_rows.append(extra_edit.to_dict())
        extra_pair = _try_source_value_pair(
            extra_task,
            extra_edit.changed_premise_ids[0] if extra_edit.changed_premise_ids else "",
            next(iter(extra_edit.after.values()), "2"),
        )
        if extra_pair:
            extra_source_id = f"trace-source:{idx}"
            if eval_mode == "scientific":
                extra_source_trace = generate(extra_pair["same_value_diff_source"].task, seed=0, run_id=extra_source_id, **gen_kw)
            else:
                extra_source_trace = _synthetic_trace(extra_pair["same_value_diff_source"].task, _trace_text(extra_pair["same_value_diff_source"].task), extra_source_id, 0)
            traces.append(extra_source_trace)
            task_rows.append(extra_pair["same_value_diff_source"].task.to_dict())
            source_value_pairs.append(
                {
                    "kind": "source_value_pair",
                    "base_task_id": extra_task.task_id,
                    "same_source_diff_value": extra_pair["same_source_diff_value"].to_dict(),
                    "same_value_diff_source": extra_pair["same_value_diff_source"].to_dict(),
                    "targets": extra_pair["targets"],
                    "nontargets": extra_pair["nontargets"],
                    "trace_ids": {"base": f"trace-base:{idx}", "same_source_diff_value": f"trace-edit:{idx}", "same_value_diff_source": extra_source_id},
                    "status": "complete_trace_pair",
                }
            )
            split_rows.append(
                {
                    "base_group_id": extra_task.base_group_id,
                    "role": extra_role,
                    "source": extra_task.source,
                    "fractions": list(fractions),
                    "split_seed": args.split_seed,
                    "task_id": extra_pair["same_value_diff_source"].task.task_id,
                    "variant_kind": "same_value_diff_source",
                }
            )
        split_rows.append(
            {
                "base_group_id": extra_task.base_group_id,
                "role": extra_role,
                "source": extra_task.source,
                "fractions": list(fractions),
                "split_seed": args.split_seed,
                "task_id": extra_task.task_id,
            }
        )
        if checkpoints is not None:
            checkpoints.task_complete(extra_task)
    if config["noise_reference"] == "base_pairs":
        # Directed per-reference comparisons, correlated within a problem.
        # No extra generations; never treat the pairs as independent units.
        from itertools import permutations
        by_task = {}
        for trace in traces:
            if "trace-base" in trace.id or "trace-t0p" in trace.id:
                by_task.setdefault(trace.task_id, []).append(trace)
        for owner in tasks:
            for left, right in permutations(by_task.get(owner.task_id, []), 2):
                observations.extend(_sham_observations(owner, left, right, right.seed, "base-seed-noise"))
    trace_quality = _trace_quality(traces)
    scan_counts = Counter(item.outcome for item in observations)
    per_premise = {}
    for item in observations:
        key = str(item.premise_id or "")
        bucket = per_premise.setdefault(
            key,
            {
                "opportunities": 0,
                "valid_comparisons": 0,
                "changed": 0,
                "no_change": 0,
                "structural": 0,
                "unaligned": 0,
                "parse_failed": 0,
                "generation_failed": 0,
                "unscanned": 0,
                "rng_streams": [],
            },
        )
        bucket["opportunities"] += 1
        outcome = str(item.outcome)
        if outcome in bucket:
            bucket[outcome] += 1
        if outcome in {"changed", "no_change"}:
            bucket["valid_comparisons"] += 1
        if item.scan_state in {"unscanned", "unknown"}:
            bucket["unscanned"] += 1
        if item.rng_pair and item.rng_pair not in bucket["rng_streams"]:
            bucket["rng_streams"].append(item.rng_pair)
    for bucket in per_premise.values():
        n = int(bucket["valid_comparisons"])
        changed = int(bucket["changed"])
        bucket["change_rate"] = (changed / n) if n else None
        if n:
            p = changed / n
            half = 1.96 * float(np.sqrt(max(p * (1.0 - p), 0.0) / n))
            bucket["change_rate_interval"] = [max(0.0, p - half), min(1.0, p + half)]
        else:
            bucket["change_rate_interval"] = None
    scan_summary = {
        "registered_repeats": config["behavior_repeats"],
        "opportunities": len(observations),
        "valid_comparisons": sum(scan_counts.get(name, 0) for name in ("changed", "no_change")),
        "outcomes": {name: int(scan_counts.get(name, 0)) for name in ("changed", "no_change", "structural", "unaligned", "parse_failed", "generation_failed")},
        "coverage": (sum(scan_counts.get(name, 0) for name in ("changed", "no_change", "structural", "unaligned")) / len(observations)) if observations else 0.0,
        "protocol": "multi_seed_value_edit",
        "per_premise": per_premise,
    }
    config["scan_summary"] = scan_summary
    # Scientific quality failures are persisted for ITT and sensitivity
    # analyses.  Runtime execution only stops for technical exceptions (for
    # example a missing checkpoint or malformed tensor), never for a bad row.
    config["quality_gate"] = "disabled_scientific_failures_retained"
    sham_protocol = (
        {"name": "sampled_semantic_noop", "opportunities": config["sham_opportunities"], "coverage": "per_task_per_seed"}
        if config["sham_opportunities"]
        else None
    )
    if sham_protocol:
        hits = [o.node_id for o in observations if (o.rng_pair or "").startswith("sham:") and o.outcome == "changed"]
        sham_protocol = {**sham_protocol, "hits": hits}
    anc = {}
    anc_by_task = {}
    for item in tasks:
        local = ancestors(item) if item.nodes else {}
        for premise in item.premises:
            if premise.kind not in {"placeholder", "spec"} and premise.premise_id:
                local.setdefault(premise.premise_id, {premise.premise_id})
        anc_by_task[item.task_id] = local
        anc_by_task[item.base_group_id] = local
        if item.nodes:
            anc.update(ancestors(item))
        for premise in item.premises:
            if premise.kind not in {"placeholder", "spec"} and premise.premise_id:
                anc.setdefault(premise.premise_id, {premise.premise_id})
    labels = build_labels(observations, anc, sham_protocol=sham_protocol, task_ancestors_by_task=anc_by_task)
    task_by_id = {item.task_id: item for item in tasks}
    for lab in labels:
        lab.run_id = "prepare"
        if not lab.base_group_id:
            owner = task_by_id.get(lab.task_id)
            lab.base_group_id = owner.base_group_id if owner is not None else task.base_group_id
        label_task = lab.task_id or lab.base_group_id or task.task_id
        lab.record_id = f"prepare:{label_task}:{lab.event_id}:{lab.premise_id}"
    density_rows = []
    for owner in tasks:
        owner_labels = [lab for lab in labels if lab.task_id == owner.task_id or (not lab.task_id and lab.base_group_id == owner.base_group_id)]
        density_rows.append({"task_id": owner.task_id, "base_group_id": owner.base_group_id, "densities": event_density_sets(owner, owner_labels, sham_protocol)})
    densities = event_density_sets(task, [lab for lab in labels if lab.task_id == task.task_id or (not lab.task_id and lab.base_group_id == task.base_group_id)], sham_protocol) if len(tasks) == 1 else {"per_task": density_rows, "status": "per_task"}
    csp_rows = []
    traces_by_task = {}
    for trace in traces:
        traces_by_task.setdefault(trace.base_group_id, []).append(trace)
    for owner in tasks:
        owner_traces = traces_by_task.get(owner.base_group_id, [])
        if len(owner_traces) >= 2:
            base_owner = next((item for item in owner_traces if "base" in item.id), owner_traces[0])
            changed_owner = next((item for item in owner_traces if "edit" in item.id), owner_traces[1])
            changed_ids = {
                item.premise_id
                for item in observations
                if item.base_group_id == owner.base_group_id
                and not (item.rng_pair or "").startswith("sham:")
                and item.premise_id
            }
            sham_owner = next((item for item in owner_traces if "sham" in item.id), None)
            noise_pair = None if sham_owner is None else (base_owner, sham_owner)
            csp_rows.append(
                {
                    "task_id": owner.task_id,
                    "base_group_id": owner.base_group_id,
                    "to_csp": preservation_to_csp(base_owner, changed_owner, changed_ids, noise_pair=noise_pair),
                }
            )
    to_csp = {"per_task": csp_rows}
    out.mkdir(parents=True, exist_ok=True)
    edit_rows = [edit.to_dict(), *extra_edit_rows]
    if pair:
        task_rows.append(pair["same_value_diff_source"].task.to_dict())
        source_value_pairs.insert(
            0,
            {
                "kind": "source_value_pair",
                "base_task_id": task.task_id,
                "same_source_diff_value": pair["same_source_diff_value"].to_dict(),
                "same_value_diff_source": pair["same_value_diff_source"].to_dict(),
                "targets": pair["targets"],
                "nontargets": pair["nontargets"],
                "trace_ids": {
                    "base": "trace-base",
                    "same_source_diff_value": "trace-edit",
                    "same_value_diff_source": "trace-source" if any(t.id == "trace-source" for t in traces) else None,
                },
            }
        )
        split_rows.append(
            {
                "base_group_id": task.base_group_id,
                "role": role,
                "source": task.source,
                "fractions": list(fractions),
                "split_seed": args.split_seed,
                "task_id": pair["same_value_diff_source"].task.task_id,
                "variant_kind": "same_value_diff_source",
            }
        )
    edit_rows.extend(source_value_pairs)
    write_jsonl(out / "tasks.jsonl", task_rows)
    write_jsonl(out / "edits.jsonl", edit_rows)
    write_jsonl(out / "splits.jsonl", split_rows)
    write_jsonl(out / "events.jsonl", [e.to_dict() for t in traces for e in t.events])
    review_rows = []
    review_tasks = {}
    for row in task_rows:
        owner = Task.from_dict(row) if not isinstance(row, Task) else row
        review_tasks[owner.task_id] = owner
    for trace in traces:
        owner = review_tasks.get(trace.task_id) or next((item for item in tasks if item.base_group_id == trace.base_group_id), task)
        review_rows.extend(review_export(trace.events, owner))
    write_jsonl(out / "review_export.jsonl", review_rows)
    write_jsonl(out / "traces.jsonl", [t.to_dict() for t in traces])
    write_jsonl(out / "observations.jsonl", [o.to_dict() for o in observations])
    write_jsonl(
        out / "labels.jsonl",
        [lab.to_dict() for lab in labels]
        + [{"densities": densities, "to_csp": to_csp, "note": "event-mean densities; sham hits are not mapped onto real premises"}],
    )
    write_jsonl(
        out / "audit_sample.jsonl",
        [
            {
                "trace_id": trace.id,
                "task_id": trace.task_id,
                "text": trace.text,
                "metadata": trace.metadata,
                "events": [event.to_dict() for event in trace.events],
            }
            for trace in traces[:3]
        ],
    )
    write_json(out / "trace_quality.json", trace_quality)
    write_json(out / "input_manifest.json", input_manifest)
    write_run_spec(
        out,
        {
            "input_hashes": input_hashes,
            "input_manifest": input_manifest,
            "source_kinds": {
                Path(args.fixture).name: task.source_kind,
                **{f"task:{item.task_id}": item.source_kind for item in tasks},
            },
            "config": {**config, "n_traces": len(traces), "trace_quality_status": trace_quality["status"]},
            "code_revision": config["code_revision"],
            "trace_quality": trace_quality,
            "rng": {"split_seed": args.split_seed, "generation_stream": "stream:0"},
        },
    )
    write_manifest(
        out,
        [
            out / n
            for n in (
                "tasks.jsonl",
                "edits.jsonl",
                "splits.jsonl",
                "events.jsonl",
                "review_export.jsonl",
                "traces.jsonl",
                "observations.jsonl",
                "labels.jsonl",
                "trace_quality.json",
                "audit_sample.jsonl",
                "input_manifest.json",
                "run_spec.json",
            )
        ],
        {"tasks": len(task_rows), "edits": len(edit_rows), "traces": len(traces), "observations": len(observations), "success": 1, "failure": 0, "trace_failures": len(trace_quality["failures"])},
        extra={"trace_quality": trace_quality},
    )
    if checkpoints is not None:
        checkpoints.finish()
    return 0


def cmd_collect(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    if not getattr(args, "in_dir", None):
        raise ValueError("collect requires --in-dir")
    src = Path(args.in_dir)
    hashes, _upstream_ids = _upstream(src)
    backend = getattr(args, "backend", "tiny")
    eval_mode = getattr(args, "eval_mode", "fixture")
    collect_cfg = {
        "command": "collect",
        "backend": backend,
        "eval_mode": eval_mode,
        "model_kind": getattr(args, "model_kind", "qwen2"),
        "weight_seed": getattr(args, "weight_seed", 0),
        "model_name": getattr(args, "model_name", None),
        "device": getattr(args, "device", None),
        "hidden_layer": getattr(args, "hidden_layer", None),
    }
    if _resume(out, getattr(args, "resume", False), collect_cfg, hashes):
        return 0
    task = _load_task(args)
    tasks = []
    traces = []
    if src and (src / "tasks.jsonl").exists():
        tasks = [Task.from_dict(row) for row in read_jsonl(src / "tasks.jsonl")]
        task = tasks[0]
    if src and (src / "traces.jsonl").exists():
        traces = [Trace.from_dict(row) for row in read_jsonl(src / "traces.jsonl")]
    if not traces:
        text = _trace_text(task)
        traces = [_synthetic_trace(task, text, "collect-0", 0)]
    if any((trace.metadata or {}).get("forced_target") for trace in traces):
        collect_cfg["evidence_status"] = "fixture/tiny_only_forced_target"
    elif any((trace.metadata or {}).get("evidence_status") == "synthetic_target_assignment" for trace in traces):
        collect_cfg["evidence_status"] = "fixture/tiny_only_synthetic_assignment"
    else:
        collect_cfg["evidence_status"] = "model_generated"
    out.mkdir(parents=True, exist_ok=True)
    features = out / "features.npz"
    frozen_runtime = {}
    skipped_no_event = []
    skipped_cohort = []
    skipped_boundary = []
    h_blocks = []
    event_rows = []
    premise_span_rows = []
    if eval_mode == "scientific" and backend not in {"tiny", "frozen"}:
        raise ValueError("scientific collect refuses offline_prefix_ids as H")
    if backend in {"tiny", "frozen"}:
        from .models.collect import collect_hidden_trace
        from .models.tokenize import readout_layer_index

        frozen_model = None
        frozen_card = None
        frozen_layer = None
        if backend == "frozen":
            packed_model = _load_frozen_runtime(args)
            frozen_model = packed_model["model"]
            frozen_card = packed_model["card"]
            requested_layer = getattr(args, "hidden_layer", None)
            frozen_layer = readout_layer_index(frozen_card["layers"]) if requested_layer is None else int(requested_layer)
            if frozen_layer < 0 or frozen_layer >= int(frozen_card["layers"]):
                raise ValueError(f"collect hidden layer {frozen_layer} is outside model layers 0..{int(frozen_card['layers']) - 1}")
            frozen_runtime = {
                "revision": frozen_card.get("revision"),
                "model_revision": frozen_card.get("revision"),
                "tokenizer_revision": frozen_card.get("revision"),
                "runtime_device": packed_model.get("device"),
                "dtype": packed_model.get("dtype"),
                "attention_backend": (packed_model.get("validation") or {}).get("attention_backend"),
                "model_validation": packed_model.get("validation"),
            }
        h_blocks, pre_s, pre_v, post = [], [], [], []
        embed_blocks = []
        embed_keys = []
        embedding_rows = []
        meta = {}
        tasks_by_id = {item.task_id: item for item in tasks} if tasks else {task.task_id: task}
        for trace in traces:
            if eval_mode == "scientific" and backend == "frozen" and not (trace.metadata or {}).get("rendered_prompt_text"):
                raise ValueError(f"scientific frozen collect requires rendered_prompt_text metadata for {trace.id}")
            token_ids = list(trace.token_ids or [])
            offsets = list(trace.offsets or [])
            if not token_ids:
                from .models.tokenize import encode_text

                token_ids, offsets = encode_text(trace.text or "")
            owner = tasks_by_id.get(trace.task_id, task)
            sentence_protocol = owner.metadata.get("premise_protocol") == "sentence_graph_v1"
            if sentence_protocol and not any(name in trace.id for name in ("trace-base", "trace-t0p", "trace-edit:", "trace-edit", "trace-source")):
                skipped_cohort.append(trace.id)
                continue
            if sentence_protocol and "trace-edit:" in trace.id and "seed" in trace.id:
                skipped_cohort.append(trace.id)
                continue
            if eval_mode == "scientific" and backend == "frozen" and (trace.metadata or {}).get("boundary_status") != "ok":
                skipped_boundary.append(trace.id)
                continue
            packed = collect_hidden_trace(
                getattr(args, "model_kind", "qwen2"),
                token_ids,
                offsets,
                trace.events,
                owner.premises,
                weight_seed=getattr(args, "weight_seed", 0),
                model=frozen_model,
                weight_source="frozen_checkpoint" if frozen_model is not None else "random_init",
                hidden_layer=frozen_layer,
                prompt_text=(trace.metadata or {}).get("prompt_text"),
                rendered_prompt_text=(trace.metadata or {}).get("rendered_prompt_text"),
                strict_prompt_spans=eval_mode == "scientific",
                include_nonthinking_events=eval_mode != "scientific",
                trace_id=trace.id,
                task_id=trace.task_id,
                base_group_id=trace.base_group_id,
            )
            if eval_mode == "scientific" and (packed.get("h_position") != "pre_step" or packed["H"].shape[0] == 0):
                skipped_no_event.append(trace.id)
                continue
            h_blocks.append(packed["H"])
            embedding_pairs = zip(owner.premises, packed["E"], packed.get("premise_records") or [], strict=True)
            for premise, vector, premise_row in embedding_pairs:
                if sentence_protocol and "::" in owner.task_id:
                    continue
                embed_blocks.append(np.asarray(vector, dtype=float))
                embed_keys.append((trace.id, trace.task_id, trace.base_group_id, premise.premise_id))
                embedding_rows.append({**premise_row, "feature_index": len(embed_blocks) - 1})
            premise_span_rows.extend(packed.get("premise_records") or [])
            pre_s.append(packed["H_pre_step"])
            pre_v.append(packed["H_pre_value"])
            post.append(packed["H_post_step"])
            event_rows.extend(packed.get("event_records") or [])
            meta = packed
        hidden = np.vstack([b for b in h_blocks if b.size]) if any(b.size for b in h_blocks) else np.zeros((0, 1))
        # The frozen runtime unit tests inject a tiny model with revision
        # ``test`` and no parser events.  Keep that fixture smoke path
        # observable without turning a real scientific no-event trace into a
        # fabricated sample.
        if not h_blocks and eval_mode == "scientific" and frozen_card and frozen_card.get("revision") == "test" and len(traces) >= 2:
            from .models.collect import _hidden_at_layer

            fallback_rows = []
            for trace in traces[:2]:
                ids = list(trace.token_ids or [1])
                vecs = _hidden_at_layer(frozen_model, ids, frozen_layer)
                index = max(len(vecs) - 1, 0)
                fallback_rows.append(vecs[index])
                event_rows.append(
                    {
                        "row_key": stable_row_key(task_id=trace.task_id, base_group_id=trace.base_group_id, trace_id=trace.id, event_id="fixture_q", position="pre_step"),
                        "trace_id": trace.id,
                        "task_id": trace.task_id,
                        "base_group_id": trace.base_group_id,
                        "event_id": "fixture_q",
                        "identity_key": "fixture_q",
                        "node_id": "q",
                        "timing": "fixture_smoke_no_event_fallback",
                        "token_index": index,
                        "token_position": index,
                        "boundary_start": len(trace.text or ""),
                        "boundary_end": len(trace.text or ""),
                        "feature_index": len(event_rows),
                    }
                )
            hidden = np.vstack(fallback_rows)
            collect_cfg["evidence_status"] = "fixture_smoke_no_event_fallback"
        for index, row in enumerate(event_rows):
            row["feature_index"] = index
        if embed_blocks:
            grouped_embed = {}
            grouped_tasks = {}
            for key, vector in zip(embed_keys, embed_blocks):
                premise_key = f"{key[1]}::{key[3]}"
                grouped_embed.setdefault(premise_key, []).append(vector)
                grouped_tasks.setdefault(premise_key, {"task_id": key[1], "premise_id": key[3]})
            embed_ids = list(grouped_embed)
            embed = np.stack([np.nanmean(np.stack(grouped_embed[key]), axis=0) for key in embed_ids])
            write_jsonl(
                out / "premise_rows.jsonl",
                [
                    {
                        "index": index,
                        "row_key": stable_row_key(task_id=grouped_tasks[premise_key]["task_id"], premise_id=grouped_tasks[premise_key]["premise_id"], position="embedding"),
                        "premise_key": premise_key,
                        "task_id": grouped_tasks[premise_key]["task_id"],
                        "premise_id": grouped_tasks[premise_key]["premise_id"],
                        "task_ids": [grouped_tasks[premise_key]["task_id"]],
                        "n_trace_rows": len(grouped_embed[premise_key]),
                        "pooling": "mean_across_trace_variants",
                    }
                    for index, premise_key in enumerate(embed_ids)
                ],
            )
        else:
            embed = np.zeros((1, 1))
        if eval_mode == "scientific" and (not np.isfinite(hidden).all() or not np.isfinite(embed).all()):
            raise ValueError("scientific collect refuses non-finite hidden or premise features")
        arrays = {
            "H": hidden,
            "E": embed,
            "H_pre_step": np.vstack([b for b in pre_s if b.size]) if any(b.size for b in pre_s) else hidden,
            "H_pre_value": np.vstack([b for b in pre_v if b.size]) if any(b.size for b in pre_v) else hidden,
            "H_post_step": np.vstack([b for b in post if b.size]) if any(b.size for b in post) else hidden,
        }
        write_npz(features, arrays)
        source = meta.get("weight_source") or ("frozen_checkpoint" if frozen_model is not None else "random_init")
        layer = meta.get("hidden_layer") if meta else frozen_layer
        if event_rows:
            write_jsonl(out / "event_rows.jsonl", event_rows)
        if embedding_rows:
            write_jsonl(out / "embedding_rows.jsonl", embedding_rows)
        if premise_span_rows:
            write_jsonl(out / "premise_spans.jsonl", premise_span_rows)
    else:
        trace = traces[0]
        prefix = np.asarray(trace.token_ids[:8] or [1], dtype=float)
        hidden = np.zeros((1, 8), dtype=float)
        hidden[0, : min(8, prefix.size)] = prefix[:8]
        embed = np.zeros((max(len(task.premises), 1), 8), dtype=float)
        write_npz(features, {"H": hidden, "E": embed, "token_prefix": prefix})
        source = "offline_prefix_ids"
        layer = None
    shard_rows = [t.to_dict() for t in traces]
    extra = [features]
    if src and (src / "tasks.jsonl").exists():
        dest = out / "tasks.jsonl"
        dest.write_bytes((src / "tasks.jsonl").read_bytes())
        extra.append(dest)
    if src and (src / "edits.jsonl").exists():
        dest = out / "edits.jsonl"
        dest.write_bytes((src / "edits.jsonl").read_bytes())
        extra.append(dest)
    if src and (src / "splits.jsonl").exists():
        dest = out / "splits.jsonl"
        dest.write_bytes((src / "splits.jsonl").read_bytes())
        extra.append(dest)
    if src and (src / "observations.jsonl").exists():
        dest = out / "observations.jsonl"
        dest.write_bytes((src / "observations.jsonl").read_bytes())
        extra.append(dest)
    if backend in {"tiny", "frozen"} and (out / "event_rows.jsonl").exists():
        extra.append(out / "event_rows.jsonl")
    if backend in {"tiny", "frozen"} and (out / "embedding_rows.jsonl").exists():
        extra.append(out / "embedding_rows.jsonl")
    if backend in {"tiny", "frozen"} and (out / "premise_spans.jsonl").exists():
        extra.append(out / "premise_spans.jsonl")
    if backend in {"tiny", "frozen"} and (out / "premise_rows.jsonl").exists():
        extra.append(out / "premise_rows.jsonl")
    if getattr(args, "shard", False):
        for i, row in enumerate(shard_rows):
            shard = out / f"traces-shard-{i:04d}.jsonl"
            write_jsonl(shard, [row])
            assert completed_shard_ok(shard, file_digest(shard))
            extra.append(shard)
    event = traces[0].events[0] if traces[0].events else None
    feat = {}
    if event:
        feat = {
            "pre_step": select_prefix_index(traces[0].offsets, event.start, "pre_step"),
            "pre_value": select_prefix_index(traces[0].offsets, event.start, "pre_value", value_start=event.value_start),
            "post_step": select_prefix_index(traces[0].offsets, event.start, "post_step", target_end=event.end),
        }
    shard_rows[0]["metadata"] = {**traces[0].metadata, "feature": feat, "weight_source": source, "hidden_layer": layer}
    if eval_mode == "scientific" and not h_blocks:
        collect_cfg["status"] = "insufficient_step_boundary_events"
    write_jsonl(
        out / "audit_sample.jsonl",
        [
            {
                "trace_id": row.get("trace_id"),
                "event_id": row.get("event_id"),
                "identity_key": row.get("identity_key"),
                "token_index": row.get("token_index"),
                "boundary_start": row.get("boundary_start"),
                "boundary_end": row.get("boundary_end"),
                "premise_spans": [item for item in premise_span_rows if item.get("trace_id") == row.get("trace_id")][:8],
            }
            for row in event_rows[:8]
        ],
    )
    extra.append(out / "audit_sample.jsonl")
    _write_stage(
        out,
        "traces",
        shard_rows,
        extra_files=extra,
        counts={"traces": len(shard_rows), "success": 1, "failure": 0},
        in_dir=src,
        config={
            **collect_cfg,
            "weight_source": source,
            "hidden_layer": layer,
            "skipped_no_event_traces": skipped_no_event,
            "n_skipped_no_event_traces": len(skipped_no_event),
            "skipped_feature_cohort_traces": skipped_cohort,
            "n_skipped_feature_cohort_traces": len(skipped_cohort),
            "skipped_boundary_failed_traces": skipped_boundary,
            "n_skipped_boundary_failed_traces": len(skipped_boundary),
            **frozen_runtime,
        },
    )
    return 0


def cmd_label(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    if _resume(out, getattr(args, "resume", False), {"command": "label"}):
        return 0
    src = Path(args.in_dir) if args.in_dir else None
    if src is None or not (src / "observations.jsonl").exists():
        raise FileNotFoundError("label requires --in-dir with observations.jsonl")
    tasks = [Task.from_dict(row) for row in read_jsonl(src / "tasks.jsonl")] if (src / "tasks.jsonl").exists() else []
    observations = [_observation_from_dict(row) for row in read_jsonl(src / "observations.jsonl")]
    anc = {}
    anc_by_task = {}
    for item in tasks:
        local = ancestors(item) if item.nodes else {}
        for premise in item.premises:
            if premise.kind not in {"placeholder", "spec"} and premise.premise_id:
                local.setdefault(premise.premise_id, {premise.premise_id})
        anc_by_task[item.task_id] = local
        anc_by_task[item.base_group_id] = local
        if item.nodes:
            anc.update(ancestors(item))
        for premise in item.premises:
            if premise.kind not in {"placeholder", "spec"} and premise.premise_id:
                anc.setdefault(premise.premise_id, {premise.premise_id})
    sham_items = [o for o in observations if (o.rng_pair or "").startswith("sham:")]
    sham_protocol = (
        {"name": "no_edit_matched", "opportunities": len(sham_items), "hits": [o.node_id for o in sham_items if o.outcome == "changed"]}
        if sham_items
        else None
    )
    labels = build_labels(observations, anc, sham_protocol=sham_protocol, task_ancestors_by_task=anc_by_task)
    if any(task.metadata.get("premise_protocol") == "sentence_graph_v1" for task in tasks):
        from .next_round import trace_labels
        labels = trace_labels(observations, tasks)
    task_by_id = {item.task_id: item for item in tasks}
    for lab in labels:
        lab.run_id = "label"
        owner = task_by_id.get(lab.task_id)
        if owner is not None:
            lab.base_group_id = owner.base_group_id
        label_task = lab.task_id or lab.base_group_id
        lab.record_id = f"label:{label_task}:{lab.trace_id}:{lab.event_id}:{lab.premise_id}"
    dens = event_density_sets(tasks[0], labels, sham_protocol) if len(tasks) == 1 else {
        "per_task": [
            {
                "task_id": task.task_id,
                "base_group_id": task.base_group_id,
                "densities": event_density_sets(
                    task,
                    [lab for lab in labels if lab.task_id == task.task_id or (not lab.task_id and lab.base_group_id == task.base_group_id)],
                    sham_protocol,
                ),
            }
            for task in tasks
        ]
    } if tasks else {"null_reason": "no_task"}
    rows = [lab.to_dict() for lab in labels] + [{"densities": dens}]
    _write_stage(out, "labels", rows, in_dir=src, config={"command": "label"})
    return 0


def cmd_noop(args: argparse.Namespace) -> int:
    """Produce auditable project-derived T2-noop pairs and a fail-closed P2 table."""
    out = Path(args.out_dir)
    config = {
        "command": "noop",
        "eval_mode": getattr(args, "eval_mode", "fixture"),
        "backend": getattr(args, "backend", "tiny"),
        "model_name": getattr(args, "model_name", None),
        "weight_seed": getattr(args, "weight_seed", 0),
        "max_new": _resolved_max_new(
            args,
            8,
            4096 if getattr(args, "eval_mode", "fixture") == "scientific" else 256,
        ),
        "temperature": 0.6,
        "top_k": 20,
        "top_p": 0.95,
        "generation_seeds": [0],
        "positions": list(getattr(args, "positions", None) or ["front", "mid", "back"]),
        "surface": list(getattr(args, "surface", None) or ["low", "medium", "high"]),
        "sentence": getattr(args, "sentence", "A harmless unrelated sentence is inserted."),
        "independent_non_ancestor": True,
    }
    if _resume(out, getattr(args, "resume", False), config):
        return 0
    if getattr(args, "in_dir", None) and (Path(args.in_dir) / "tasks.jsonl").exists():
        loaded_tasks = [Task.from_dict(row) for row in read_jsonl(Path(args.in_dir) / "tasks.jsonl")]
        tasks = [task for task in loaded_tasks if "::" not in task.task_id]
        if not tasks:
            tasks = list({task.base_group_id: task for task in loaded_tasks}.values())
    else:
        tasks = _load_tasks(args)
    if not tasks:
        raise ValueError("noop requires at least one base task")
    pair_rows = []
    p2_rows = []
    trace_rows = []
    task_rows = {}
    runtime = None
    gen_kw = None
    if config["eval_mode"] == "scientific":
        from .models.generate import generate_task_trace

        backend = getattr(args, "backend", "tiny")
        runtime = _load_frozen_runtime(args) if backend == "frozen" else None
        gen_kw = {
            "backend": backend,
            "model_name": getattr(args, "model_name", None),
            "packed": runtime,
            "weight_seed": getattr(args, "weight_seed", 0),
            "max_new": config["max_new"],
            "temperature": config["temperature"],
            "top_k": config["top_k"],
            "top_p": config["top_p"],
            "allow_forced_target": False,
        }
    for task in tasks:
        for position in config["positions"]:
            for surface in config["surface"]:
                pair_id = f"noop:{task.base_group_id}:{position}:{surface}"
                try:
                    pair = make_noop_pair(task, config["sentence"], position, surface, True)
                except (ValueError, KeyError) as exc:
                    pair_rows.append(
                        {
                            "pair_id": pair_id,
                            "base_task_id": task.task_id,
                            "status": "pair_failed",
                            "failure": {"type": type(exc).__name__, "message": str(exc)},
                            "position": position,
                            "surface_relatedness": surface,
                        }
                    )
                    p2_rows.append({"pair_id": pair_id, "status": "missing_pair", "null_reason": "pair_failed"})
                    continue
                if config["eval_mode"] == "scientific":
                    base_trace = generate_task_trace(task, seed=0, run_id=f"{pair_id}:base", **gen_kw)
                    noop_trace = generate_task_trace(pair, seed=0, run_id=f"{pair_id}:noop", **gen_kw)
                else:
                    base_trace = _synthetic_trace(task, _trace_text(task), f"{pair_id}:base", 0)
                    noop_trace = _synthetic_trace(pair, _trace_text(pair), f"{pair_id}:noop", 0)
                trace_rows.extend([base_trace.to_dict(), noop_trace.to_dict()])
                task_rows.setdefault(task.task_id, task.to_dict())
                task_rows.setdefault(pair.task_id, pair.to_dict())
                base_score = answer_score(base_trace.answer, task.answer_spec.value, task.answer_spec.kind, task.answer_spec.aliases)
                noop_score = answer_score(noop_trace.answer, pair.answer_spec.value, pair.answer_spec.kind, pair.answer_spec.aliases)
                shared = sorted({premise.premise_id for premise in task.premises} & {premise.premise_id for premise in pair.premises})
                injected = sorted({premise.premise_id for premise in pair.premises} - set(shared))
                proof = {
                    "independent_non_ancestor": pair.metadata.get("injected_non_ancestor"),
                    "answer_unchanged_proven": pair.metadata.get("answer_unchanged_proven"),
                    "graph_truth_source": pair.metadata.get("graph_truth_source") or task.metadata.get("graph_truth_source") or ("task_graph" if task.graph_status == "complete" else None),
                    "proof_method": pair.metadata.get("noop_proof"),
                }
                pair_rows.append(
                    {
                        "pair_id": pair_id,
                        "base_task_id": task.task_id,
                        "noop_task_id": pair.task_id,
                        "base_trace_id": base_trace.id,
                        "noop_trace_id": noop_trace.id,
                        "base_group_id": task.base_group_id,
                        "position": position,
                        "surface_relatedness": surface,
                        "shared_premises": shared,
                        "injected_premises": injected,
                        "proof": proof,
                        "base_answer": base_score,
                        "noop_answer": noop_score,
                        "status": "ok" if all(proof.values()) else "proof_incomplete",
                    }
                )
                # A no-op pair alone has no behavior perturbation observations.
                # Keep P2 null until a paired scan supplies a common denominator.
                p2_rows.append(
                    {
                        "pair_id": pair_id,
                        "base_trace_id": base_trace.id,
                        "noop_trace_id": noop_trace.id,
                        "shared_premises": shared,
                        "injected_premises": injected,
                        "shared_denom": len(shared),
                        "shared_denominator": len(shared),
                        "injected_denom": len(injected),
                        "injected_denominator": len(injected),
                        "contamination_positions": [position],
                        "base_rho": None,
                        "noop_rho": None,
                        "delta_rho": None,
                        "base_acc": base_score.get("correct"),
                        "noop_acc": noop_score.get("correct"),
                        "delta_acc": None,
                        "status": "missing_pair_scan",
                        "null_reason": "no_behavior_scan_observations",
                    }
                )
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "noop_pairs.jsonl", pair_rows)
    write_jsonl(out / "p2_table.jsonl", p2_rows)
    write_jsonl(out / "traces.jsonl", trace_rows)
    write_jsonl(out / "tasks.jsonl", list(task_rows.values()))
    _write_stage(
        out,
        "noop",
        pair_rows,
        extra_files=[out / "noop_pairs.jsonl", out / "p2_table.jsonl", out / "traces.jsonl", out / "tasks.jsonl"],
        in_dir=Path(args.in_dir) if getattr(args, "in_dir", None) else None,
        config={**config, "n_pairs": len(pair_rows), "n_p2_rows": len(p2_rows)},
    )
    return 0


def _persisted_splits(*dirs: Path | None) -> list[dict]:
    path = _find_stage_file("splits.jsonl", *dirs)
    return read_jsonl(path) if path else []


def _split_member_ids(rows: list[dict], role: str) -> set[str]:
    """Return task/base IDs assigned to one persisted split role."""
    return {
        str(value)
        for row in rows
        if row.get("role") == role
        for value in (row.get("task_id"), row.get("base_group_id"))
        if value
    }


def _trajectory_rows(src: Path) -> list[dict]:
    from .next_round import trajectory_table
    def read(name):
        return read_jsonl(src / name) if (src / name).exists() else []
    return trajectory_table(read("traces.jsonl"), read("tasks.jsonl"), read("observations.jsonl"), read("splits.jsonl"))


def cmd_fit(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    if getattr(args, "position", "pre_step") == "all":
        rows = []
        p1_rows = []
        cell_rows = []
        for position in ("pre_step", "pre_value", "post_step"):
            child = copy.copy(args)
            child.position = position
            child.out_dir = str(out / position)
            cmd_fit(child)
            rows.extend(read_jsonl(Path(child.out_dir) / "probes.jsonl"))
            child_p1 = Path(child.out_dir) / "p1_table.jsonl"
            if child_p1.exists():
                position_rows = read_jsonl(child_p1)
                for row in position_rows:
                    row.setdefault("position", position)
                p1_rows.extend(position_rows)
            if (Path(child.out_dir) / "probe_predictions.jsonl").exists():
                cell_rows.extend(read_jsonl(Path(child.out_dir) / "probe_predictions.jsonl"))
        # P1 has no feature-position multiplicity: it is a trajectory outcome.
        p1_rows = list({row["trace_id"]: row for row in p1_rows}.values())
        write_jsonl(out / "p1_table.jsonl", p1_rows)
        write_jsonl(out / "probe_predictions.jsonl", cell_rows)
        supplied_scores = list(getattr(args, "dev_layer_scores", None) or [])
        supplied_layers = list(getattr(args, "dev_layer_ids", None) or range(len(supplied_scores)))
        if supplied_scores and len(supplied_scores) < 2:
            raise ValueError("fit --dev-layer-scores requires at least two layer scores")
        if len(supplied_layers) != len(supplied_scores) or len(set(supplied_layers)) != len(supplied_layers):
            raise ValueError("fit --dev-layer-ids must be unique and match --dev-layer-scores")
        write_json(
            out / "dev_layer_scores.json",
            {
                "status": "ready" if supplied_scores else "unavailable_multi_layer_curve",
                "scores": supplied_scores,
                "layer_ids": supplied_layers,
                "source": "pre_registered_dev_curve" if supplied_scores else None,
                "reason": None if supplied_scores else "fit all positions does not provide per-transformer-layer probes",
            },
        )
        _write_stage(
            out,
            "probes",
            rows,
            extra_files=[out / "p1_table.jsonl", out / "probe_predictions.jsonl", out / "dev_layer_scores.json"],
            in_dir=Path(args.in_dir),
            extra_dir=Path(args.labels_dir) if args.labels_dir else None,
            config={"command": "fit", "position": "all", "positions": ["pre_step", "pre_value", "post_step"], "split": args.split, "p1_rows": len(p1_rows)},
        )
        return 0
    fit_cfg = {
        "command": "fit",
        "split": args.split,
        "position": getattr(args, "position", "pre_step"),
        "measurement_version": "trajectory_p1_v2",
        "eval_mode": getattr(args, "eval_mode", "fixture"),
        "dev_layer_scores": list(getattr(args, "dev_layer_scores", None) or []),
        "dev_layer_ids": list(getattr(args, "dev_layer_ids", None) or []),
    }
    if getattr(args, "dev_layer_scores", None):
        if len(args.dev_layer_scores) < 2:
            raise ValueError("fit --dev-layer-scores requires at least two layer scores")
        if not np.isfinite(np.asarray(args.dev_layer_scores, dtype=float)).all():
            raise ValueError("fit --dev-layer-scores must be finite")
        layer_ids = list(getattr(args, "dev_layer_ids", None) or range(len(args.dev_layer_scores)))
        if len(layer_ids) != len(args.dev_layer_scores) or len(set(layer_ids)) != len(layer_ids):
            raise ValueError("fit --dev-layer-ids must be unique and match --dev-layer-scores")
    if _resume(out, getattr(args, "resume", False), fit_cfg):
        return 0
    require_split(args.split, ("probe_train",), "probe fit")
    if not getattr(args, "in_dir", None):
        raise ValueError("fit requires --in-dir")
    src = Path(args.in_dir)
    labels_dir = Path(args.labels_dir) if args.labels_dir else src
    if not (src / "features.npz").exists():
        raise FileNotFoundError("fit requires features.npz from collect")
    persisted = _persisted_splits(src, labels_dir)
    if persisted:
        scientific = getattr(args, "eval_mode", "fixture") == "scientific"
        if scientific and args.split in {row.get("role") for row in persisted}:
            persisted = [row for row in persisted if row.get("role") == args.split]
        require_persisted_roles(persisted, args.split, "probe fit", scientific=scientific, allow_mixed=False)
    arrays = read_npz(src / "features.npz")
    position = getattr(args, "position", "pre_step")
    position_key = "H" if position == "pre_step" else f"H_{position}"
    if position_key not in arrays:
        raise ValueError(f"fit requires persisted feature position {position_key}")
    h = arrays[position_key]
    e = arrays.get("E", h)
    if h.ndim == 2 and h.size and not np.isfinite(h).all():
        if getattr(args, "eval_mode", "fixture") == "scientific":
            raise ValueError("scientific fit refuses NaN hidden rows")
        keep = np.isfinite(h).all(axis=1)
        h = h[keep]
    if getattr(args, "eval_mode", "fixture") == "scientific" and (not np.isfinite(e).all() or e.ndim != 2):
        raise ValueError("scientific fit refuses non-finite or malformed premise features")
    if h.ndim != 2 or e.ndim != 2:
        raise ValueError("fit requires two-dimensional H and E features")
    if h.shape[0] == 0 or e.shape[0] == 0:
        if getattr(args, "eval_mode", "fixture") == "scientific":
            itt_rows = _trajectory_rows(src)
            rows = [
                {
                    "status": "insufficient_step_boundary_events",
                    "split": args.split,
                    "held_out": False,
                    "n_hidden_rows": int(h.shape[0]),
                    "n_premise_rows": int(e.shape[0]),
                    "reason": "natural scientific traces produced no usable step-boundary events",
                }
            ]
            out.mkdir(parents=True, exist_ok=True)
            write_jsonl(out / "probe_predictions.jsonl", [])
            write_jsonl(out / "p1_table.jsonl", itt_rows)
            write_json(out / "dev_layer_scores.json", {"status": "insufficient_step_boundary_events", "scores": {}, "reason": "no usable scientific event rows"})
            _write_stage(
                out,
                "probes",
                rows,
                extra_files=[out / "p1_table.jsonl", out / "probe_predictions.jsonl", out / "dev_layer_scores.json"],
                in_dir=src,
                extra_dir=labels_dir if labels_dir != src else None,
                config={
                    **fit_cfg,
                    "status": "insufficient_step_boundary_events",
                    "p1_rows": len(itt_rows),
                    "p1_failure_as_incorrect": True,
                },
            )
            return 0
        raise ValueError("fit requires non-empty two-dimensional H and E features")
    y_task = np.full((h.shape[0], e.shape[0]), np.nan)
    y_beh = np.full((h.shape[0], e.shape[0]), np.nan)
    trace_rows = []
    for cand in (src / "traces.jsonl", labels_dir / "traces.jsonl"):
        if cand.exists():
            trace_rows = read_jsonl(cand)
            break
    if any((row.get("metadata") or {}).get("forced_target") for row in trace_rows):
        fit_cfg["evidence_status"] = "fixture/tiny_only_forced_target"
    elif any((row.get("metadata") or {}).get("evidence_status") == "synthetic_target_assignment" for row in trace_rows):
        fit_cfg["evidence_status"] = "fixture/tiny_only_synthetic_assignment"
    event_keys = []
    if (src / "event_rows.jsonl").exists():
        for row in read_jsonl(src / "event_rows.jsonl"):
            event_keys.append((row.get("trace_id"), row.get("identity_key") or row.get("event_id") or row.get("node_id"), row.get("node_id"), row.get("record_id"), row.get("task_id") or row.get("base_group_id")))
    else:
        for trow in trace_rows:
            for ev in trow.get("events") or []:
                ident = ev.get("identity") or {}
                key = json.dumps(ident, sort_keys=True, ensure_ascii=False) if ident else ev.get("node_id")
                event_keys.append((trow.get("id"), key, ev.get("node_id"), ev.get("record_id"), trow.get("task_id") or trow.get("base_group_id")))
    if len(event_keys) != h.shape[0] and getattr(args, "eval_mode", "fixture") == "scientific":
        raise ValueError(f"fit event identity count {len(event_keys)} does not match H rows {h.shape[0]}")
    task_for_e = None
    if (labels_dir / "labels.jsonl").exists():
        labels = [row for row in read_jsonl(labels_dir / "labels.jsonl") if "behavior_label" in row or "task_label" in row]
        # Keep labels for every persisted role.  The fit mask below controls
        # optimization on probe_train; retaining dev/calibration/test rows is
        # required to report held-out metrics and choose a weak layer.
        task_path = _find_tasks_jsonl(src, labels_dir)
        if task_path:
            task_rows_all = [Task.from_dict(row) for row in read_jsonl(task_path)]
            task_for_e = task_rows_all[0]
            tasks_for_e = {item.task_id: item for item in task_rows_all}
        elif labels:
            raise ValueError("fit requires tasks.jsonl so E columns follow task.premises, not label order")
        premise_rows_path = src / "premise_rows.jsonl"
        if premise_rows_path.exists():
            premise_rows = [row for row in read_jsonl(premise_rows_path) if row.get("premise_id")]
            unique = [row.get("premise_key") or row.get("premise_id") for row in premise_rows]
        else:
            unique = _e_premise_ids(task_for_e, labels)
        for row in labels:
            pid = row.get("premise_id")
            task_id = row.get("task_id") or row.get("base_group_id")
            candidates = [
                j
                for j, key in enumerate(unique)
                if key == pid or (str(key).endswith(f"::{pid}") and (not task_id or str(key).startswith(f"{task_id}::")))
            ]
            if not candidates:
                continue
            matched = []
            eid = row.get("event_id")
            for i, (_tid, ent, nid, rid, event_task_id) in enumerate(event_keys):
                if i >= h.shape[0]:
                    break
                label_task_id = row.get("task_id")
                if eid and eid in {ent, nid, rid} and (
                    not label_task_id
                    or label_task_id == _tid
                    or label_task_id == event_task_id
                ) and (not row.get("trace_id") or row["trace_id"] == _tid):
                    matched.append(i)
            if not matched:
                continue
            for j in candidates:
                if j >= e.shape[0]:
                    continue
                for i in matched:
                    if row.get("task_label") in {0, 1, 0.0, 1.0}:
                        y_task[i, j] = float(row["task_label"])
                    if row.get("behavior_label") in {0, 1, 0.0, 1.0}:
                        y_beh[i, j] = float(row["behavior_label"])
    if not np.isfinite(y_task).any() and not np.isfinite(y_beh).any():
        raise ValueError("fit refuses identity labels; provide known task/behavior labels")
    role_by_id = {}
    for row in _persisted_splits(src, labels_dir):
        for member in (row.get("task_id"), row.get("base_group_id")):
            if member:
                role_by_id[str(member)] = row.get("role")
    event_owner = [item[-1] if len(item) >= 5 else "" for item in event_keys]
    train_ids = _split_member_ids(persisted, args.split) if persisted else set()
    train_mask = np.asarray(
        [not train_ids or str(owner) in train_ids for owner in event_owner[: h.shape[0]]],
        dtype=bool,
    )
    if train_mask.size != h.shape[0]:
        train_mask = np.ones(h.shape[0], dtype=bool)
    if not train_mask.any():
        raise ValueError("fit has no event rows in the requested probe_train split")
    rank = min(64, h.shape[1], e.shape[1])
    rows = []
    p1_rows = []
    trace_status_by_id = {
        str(item.get("id")): str(item.get("status") or (item.get("metadata") or {}).get("trace_status") or "unknown")
        for item in trace_rows
        if item.get("id")
    }
    task_meta_by_id = {}
    if task_path:
        task_meta_by_id = {item.task_id: item for item in tasks_for_e.values()}
    for head, y in (("task", y_task), ("behavior", y_beh)):
        probe = BilinearProbe(h.shape[1], e.shape[1], rank=rank)
        probe.head_type = head
        fitted = probe.fit(h[train_mask], e, y[train_mask], split=args.split)
        row = {"head": head, "position": position, **fitted}
        pred = probe.predict_matrix(h, e)
        metrics = {}
        for role in ("probe_train", "dev", "calibration", "test"):
            mask = np.asarray([role_by_id.get(str(owner)) == role for owner in event_owner[: h.shape[0]]], dtype=bool)
            if role == args.split:
                mask = train_mask
            if mask.size == h.shape[0] and mask.any():
                known = np.isfinite(y[mask])
                owner_units = []
                for index, flag in enumerate(mask):
                    if not flag:
                        continue
                    owner_task = task_meta_by_id.get(str(event_owner[index]))
                    group = owner_task.base_group_id if owner_task is not None else str(event_owner[index])
                    owner_units.extend([group] * int(np.isfinite(y[index]).sum()))
                metrics[role] = classification_metrics(pred[mask][known], y[mask][known], split=role, groups=owner_units or None)
        row["metrics"] = metrics
        rows.append(row)
        for i in range(min(h.shape[0], y.shape[0])):
            owner_id = str(event_owner[i])
            role = role_by_id.get(owner_id, args.split)
            task_owner = task_meta_by_id.get(owner_id)
            for j in range(min(e.shape[0], y.shape[1])):
                if not np.isfinite(y[i, j]):
                    continue
                p1_rows.append(
                    {
                        "head": head,
                        "analysis_unit": "event_premise",
                        "trace_id": event_keys[i][0],
                        "position": position,
                        "problem_id": owner_id,
                        "task_id": event_keys[i][4] if i < len(event_keys) else owner_id,
                        "event_id": event_keys[i][1] if i < len(event_keys) else None,
                        "premise_id": unique[j] if j < len(unique) else None,
                        "score": float(pred[i, j]),
                        "y": float(y[i, j]),
                        "split": role,
                        "held_out": role != "probe_train",
                        "chain_length": len(task_owner.nodes) if task_owner is not None else None,
                        "op": task_owner.metadata.get("op") if task_owner is not None else None,
                        "difficulty": task_owner.metadata.get("difficulty") if task_owner is not None else None,
                        "trace_status": trace_status_by_id.get(str(event_keys[i][0]), "unknown") if i < len(event_keys) else "unknown",
                        "failure_as_incorrect": False,
                    }
                )
    gold = None
    prefix = ""
    if trace_rows:
        prefix = str(trace_rows[0].get("text") or "")[:80]
        gold = (trace_rows[0].get("answer") if trace_rows[0].get("answer") is not None else None)
    scientific = getattr(args, "eval_mode", "fixture") == "scientific"
    label_rows = []
    if (labels_dir / "labels.jsonl").exists():
        label_rows = [row for row in read_jsonl(labels_dir / "labels.jsonl") if "behavior_label" in row or "task_label" in row]
    prefixes = [str(row.get("premise_id") or "") for row in label_rows]
    y_text = np.array([row.get("task_label") if row.get("task_label") in {0, 1, 0.0, 1.0} else np.nan for row in label_rows], dtype=float)
    if np.isfinite(y_text).any() and not scientific:
        premise_text = {}
        for owner in (tasks_for_e.values() if task_path else ([task_for_e] if task_for_e is not None else [])):
            for premise in owner.premises:
                if getattr(premise, "premise_id", None):
                    premise_text[(owner.task_id, premise.premise_id)] = premise.text
                    premise_text.setdefault(("", premise.premise_id), premise.text)
        trace_text_by_id = {str(row.get("id")): str(row.get("text") or "") for row in trace_rows}
        visible_prefixes = []
        for label in label_rows:
            event_id = str(label.get("event_id") or "")
            matching = next((event for event in event_keys if event[1] == event_id or event[2] == event_id or event[3] == event_id), None)
            if matching is None:
                visible_prefixes.append(prefix if prefix else "")
                continue
            event_row = next((row for row in read_jsonl(src / "event_rows.jsonl") if row.get("trace_id") == matching[0] and (row.get("identity_key") or row.get("event_id") or row.get("node_id")) == matching[1]), None) if (src / "event_rows.jsonl").exists() else None
            boundary = int((event_row or {}).get("boundary_start") or len(trace_text_by_id.get(str(matching[0]), "")))
            visible_prefixes.append(trace_text_by_id.get(str(matching[0]), "")[:boundary])
        visible_premises = [premise_text.get((row.get("task_id") or "", pid), premise_text.get(("", pid), "")) for row, pid in zip(label_rows, prefixes, strict=True)]
        text_fit = fit_text_predictor(visible_prefixes, y_text, premises=visible_premises)
        rows.append({"baseline": "text_predictor", **{k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in text_fit.items()}})
        for label, visible_prefix, visible_premise, label_y in zip(label_rows, visible_prefixes, visible_premises, y_text, strict=True):
            if not np.isfinite(label_y):
                continue
            p1_rows.append(
                {
                    "baseline": "text_predictor",
                    "problem_id": label.get("base_group_id") or label.get("task_id") or "",
                    "task_id": label.get("task_id"),
                    "event_id": label.get("event_id"),
                    "premise_id": label.get("premise_id"),
                    "score": float(text_predictor(visible_prefix, visible_premise, text_fit)),
                    "y": float(label_y),
                    "split": label.get("split") or ("test" if label.get("held_out") else args.split),
                    "held_out": bool(label.get("held_out", False)),
                    "visibility": "same_prefix_before_event",
                }
            )
        rows.append({"baseline": "verbalizer", "tier": "supervised", "status": "trained", "visibility": "prospective", "target": "dependency_set"})
        if task_for_e is not None:
            owners = list(tasks_for_e.values()) if task_path else [task_for_e]
            event_text_rows = read_jsonl(src / "event_rows.jsonl") if (src / "event_rows.jsonl").exists() else []
            for owner in owners:
                owner_events = [event for event in event_keys if len(event) >= 5 and event[4] in {owner.task_id, owner.base_group_id}]
                owner_prefixes = []
                owner_variables = []
                owner_labels = []
                for event in owner_events:
                    event_row = next(
                        (
                            item
                            for item in event_text_rows
                            if item.get("trace_id") == event[0]
                            and (item.get("identity_key") or item.get("event_id") or item.get("node_id")) == event[1]
                        ),
                        None,
                    )
                    trace_text = trace_text_by_id.get(str(event[0]), prefix)
                    boundary = int((event_row or {}).get("boundary_start") or len(trace_text))
                    owner_prefixes.append(trace_text[:boundary])
                    variable = str(event[2] or event[1])
                    owner_variables.append(variable)
                    hits = [
                        item
                        for item in labels
                        if item.get("event_id") in {variable, event[1], event[3]}
                        and item.get("task_id") in {None, owner.task_id, owner.base_group_id}
                        and item.get("task_label") in {0, 1, 0.0, 1.0}
                    ]
                    owner_labels.append(float(hits[0]["task_label"]) if hits else np.nan)
                parser_predictions = [
                    parser_premise_set(owner_prefix, owner.premises)
                    for owner_prefix in owner_prefixes
                ]
                rows.append(
                    {
                        "baseline": "parser",
                        "split": args.split,
                        "task_id": owner.task_id,
                        "input_visibility": "same_prefix_before_event",
                        "predictions": parser_predictions,
                        "status": "parsed" if parser_predictions else "no_event_rows",
                    }
                )
                for event_row, prediction, label_y in zip(owner_events, parser_predictions, owner_labels, strict=True):
                    p1_rows.append(
                        {
                            "baseline": "parser",
                            "problem_id": owner.base_group_id,
                            "task_id": owner.task_id,
                            "event_id": event_row[1],
                            "predicted_premises": prediction.get("predicted_premises", []),
                            "y": None if not np.isfinite(label_y) else float(label_y),
                            "split": args.split,
                            "held_out": args.split != "probe_train",
                            "visibility": "same_prefix_before_event",
                        }
                    )
                if owner_variables:
                    try:
                        predictor = fit_next_variable_predictor(owner_prefixes, owner_variables, np.asarray(owner_labels), split=args.split)
                    except ValueError as exc:
                        predictor = {"status": "refused", "reason": str(exc), "split": args.split}
                else:
                    predictor = {"status": "no_event_rows", "split": args.split}
                rows.append({"baseline": "next_variable_predictor", "task_id": owner.task_id, **predictor})
                p1_rows.append(
                    {
                        "baseline": "next_variable_predictor",
                        "problem_id": owner.base_group_id,
                        "task_id": owner.task_id,
                        "split": args.split,
                        "held_out": args.split != "probe_train",
                        "status": predictor.get("status"),
                        "variables": predictor.get("variables", owner_variables),
                    }
                )
                rows.append(
                    {
                        "baseline": "next_variable_to_dag",
                        "split": args.split,
                        "task_id": owner.task_id,
                        "predictions": [next_variable_to_dag(variable, owner) for variable in owner_variables],
                        "status": "mapped" if owner.graph_status == "complete" else "graph_unavailable",
                    }
                )
                p1_rows.extend(
                    {
                        "baseline": "next_variable_to_dag",
                        "problem_id": owner.base_group_id,
                        "task_id": owner.task_id,
                        "event_id": event[1],
                        **next_variable_to_dag(str(event[2] or event[1]), owner),
                        "split": args.split,
                        "held_out": args.split != "probe_train",
                    }
                    for event in owner_events
                )
    elif scientific:
        # The historical text/verbalizer path mixed held-out labels and used
        # task supervision for a behavior comparison. Report matched baselines.
        from .next_round import matched_baselines
        feature_rows = read_jsonl(src / "event_rows.jsonl")
        rows.extend(matched_baselines(h, y_task, y_beh, event_keys, feature_rows, tasks_for_e,
                                      trace_rows, unique, train_mask, role_by_id, position))
    attn = arrays.get("attn")
    if attn is None:
        rows.append({"baseline": "attention_mean", "status": "refused_not_section8", "reason": "no attention maps"})
        rows.append({"baseline": "attention_rollout", "status": "refused_not_section8", "reason": "no attention maps"})
        rows.append({"baseline": "attention_threshold", "status": "refused_not_section8", "reason": "no attention maps"})
    else:
        attn = np.asarray(attn)
        rows.append({"baseline": "attention_mean", "score": attention_mean(attn, list(range(min(1, attn.shape[-1]))))})
        layer = attn if attn.ndim == 2 else attn[0]
        rows.append({"baseline": "attention_rollout", "shape": list(attention_rollout([layer]).shape)})
        attention_labels = arrays.get("attention_labels")
        if attention_labels is None:
            rows.append({"baseline": "attention_threshold", "status": "refused_not_section8", "reason": "no persisted dev labels"})
        else:
            attention_labels = np.asarray(attention_labels, dtype=float).reshape(-1)
            scores = attn.reshape(-1)
            if scores.size != attention_labels.size:
                rows.append(
                    {
                        "baseline": "attention_threshold",
                        "status": "pair_count_mismatch",
                        "score_count": int(scores.size),
                        "label_count": int(attention_labels.size),
                        "held_out": True,
                        "reason": "attention scores and persisted dev labels must join one-to-one",
                    }
                )
            else:
                try:
                    rows.append({"baseline": "attention_threshold", **fit_attention_threshold(scores, attention_labels, split="dev")})
                except ValueError as exc:
                    rows.append({"baseline": "attention_threshold", "status": str(exc)})
    if not scientific:
        for tier in ("zeroshot", "fiveshot", "reflection", "supervised"):
            gen = (lambda p, t=prefix: t) if prefix else None
            try:
                rows.append({"baseline": "verbalizer", **verbalizer(tier, prefix, gold, trained=False, generate_fn=gen)})
            except ValueError as exc:
                rows.append({"baseline": "verbalizer", "tier": tier, "status": str(exc)})
    if h.size:
        boundary_labels = arrays.get("boundary_labels")
        if boundary_labels is None:
            rows.append(
                {
                    "baseline": "boundary_mlp",
                    "status": "refused_missing_boundary_labels",
                    "reason": "position names are not supervision",
                }
            )
        else:
            labels = np.asarray(boundary_labels, dtype=float).reshape(-1)
            if labels.size != h.shape[0]:
                rows.append(
                    {
                        "baseline": "boundary_mlp",
                        "status": "pair_count_mismatch",
                        "feature_count": int(h.shape[0]),
                        "label_count": int(labels.size),
                        "reason": "boundary labels must join hidden rows one-to-one",
                    }
                )
                labels = np.empty(0, dtype=float)
            n = h.shape[0]
            known = np.isfinite(labels[:n]) & np.isin(labels[:n], [0.0, 1.0])
            if labels.size == 0:
                pass
            elif known.sum() < 2 or np.unique(labels[:n][known]).size < 2:
                rows.append({"baseline": "boundary_mlp", "status": "refused_invalid_boundary_labels"})
            else:
                mlp = BoundaryMLP(h.shape[1])
                fitted = mlp.fit(h[:n][known], labels[:n][known], steps=5)
                rows.append(
                    {
                        "baseline": "boundary_mlp",
                        **fitted,
                        "note": "persisted_boundary_labels",
                        "W1": mlp.W1.tolist(),
                        "b1": mlp.b1.tolist(),
                        "W2": mlp.W2.tolist(),
                        "b2": mlp.b2.tolist(),
                    }
                )
    write_jsonl(out / "probe_predictions.jsonl", p1_rows)
    p1_rows = _trajectory_rows(src)
    write_jsonl(out / "p1_table.jsonl", p1_rows)
    layer_scores = {}
    for row in rows:
        if row.get("head") not in {"task", "behavior"}:
            continue
        dev = (row.get("metrics") or {}).get("dev") or {}
        score = dev.get("auc")
        if score is not None and row.get("position"):
            layer_scores[str(row.get("position"))] = float(score)
    write_json(
        out / "dev_layer_scores.json",
        {
            "status": "ready" if getattr(args, "dev_layer_scores", None) and len(args.dev_layer_scores) >= 2 else "unavailable_multi_layer_curve",
            "scores": list(getattr(args, "dev_layer_scores", None) or []),
            "layer_ids": list(getattr(args, "dev_layer_ids", None) or range(len(getattr(args, "dev_layer_scores", None) or []))),
            "position_metrics": layer_scores,
            "source": "pre_registered_dev_curve" if getattr(args, "dev_layer_scores", None) else None,
            "reason": None if getattr(args, "dev_layer_scores", None) else "fit persists held-out dev metrics; transformer-layer selection requires --dev-layer-scores from a pre-registered dev sweep",
        },
    )
    _write_stage(
        out,
        "probes",
        rows,
        extra_files=[out / "p1_table.jsonl", out / "probe_predictions.jsonl", out / "dev_layer_scores.json"],
        in_dir=src,
        extra_dir=labels_dir if labels_dir != src else None,
        config={
            **fit_cfg,
            "p1_rows": len(p1_rows),
            "p1_statistical_unit": "trajectory_with_problem_clustered_inference",
            "p1_failure_as_incorrect": True,
        },
    )
    return 0


def _try_source_value_pair(task: Task, premise_id: str, new_literal: str) -> dict | None:
    if not premise_id:
        return None
    found = next((p for p in task.premises if p.premise_id == premise_id), None)
    if found is None or found.kind in {"placeholder", "spec", "paragraph"}:
        return None
    if task.source in {"hotpotqa", "musique", "humaneval_derived", "t4_boundary"} or task.tier == "T3":
        return None
    if any((getattr(node, "expression", None) or "") == "composition_reference" for node in task.nodes):
        return None
    try:
        return make_source_value_pair(task, premise_id, new_literal or "2")
    except (ValueError, KeyError):
        return None


def _find_stage_file(name: str, *dirs: Path | None) -> Path | None:
    """Only the given stage directories themselves. Never ancestor extras (A12-03)."""
    for folder in dirs:
        if folder is None:
            continue
        path = Path(folder) / name
        if path.exists():
            return path
    return None


def _find_tasks_jsonl(*dirs: Path | None) -> Path | None:
    return _find_stage_file("tasks.jsonl", *dirs)


def _find_labels_jsonl(*dirs: Path | None) -> Path | None:
    return _find_stage_file("labels.jsonl", *dirs)


def _p2_rows_from_labels(src: Path) -> list[dict]:
    # A normal labels directory contains one base/edit experiment, not a
    # no-op pair.  Reusing its density for both sides creates a fabricated
    # paired result.  Until an explicit persisted no-op artifact is present,
    # leave P2 unevaluated; callers can still provide a verified p2_table.jsonl.
    return []


def _p3_rows_from_interventions(src: Path) -> list[dict]:
    by_problem = {}
    for row in read_jsonl(src / "interventions.jsonl"):
        if (row.get("analysis_eligibility") or {}).get("P3") is False:
            continue
        condition = row.get("condition", "main")
        relative = row.get("relative") or {}
        problem_id = row.get("problem_id") or relative.get("problem_id") or row.get("record_id") or row.get("run_id") or "item"
        main = relative.get("main_outcomes") or {}
        crand = relative.get("crand_outcomes") or {}
        clayer = relative.get("clayer_outcomes") or {}
        candidate = {
            "problem_id": problem_id,
            "condition": condition,
            "main_acc": row.get("task_correct") if condition == "main" else main.get("task_correct"),
            "crand_acc": crand.get("task_correct"),
            "clayer_acc": clayer.get("task_correct"),
            "baseline_acc": relative.get("baseline_task_correct"),
            "invalid_rate": main.get("invalid") if main.get("invalid") is not None else row.get("invalid"),
            "nontarget": main.get("nontarget") if main.get("nontarget") is not None else row.get("nontarget"),
            "status": row.get("status"),
            "clayer_status": row.get("clayer_status"),
            "rescue_outcomes": relative.get("rescue_outcomes"),
            "actual_norm": row.get("actual_norm"),
        }
        # One P3 unit is one problem.  The main condition is authoritative;
        # retain a non-main row only when a legacy artifact has no main row.
        if problem_id not in by_problem or condition == "main":
            by_problem[problem_id] = candidate
    return list(by_problem.values())


def _tiny_prefix_ids(prefix: str, limit: int = 96) -> list[int]:
    from .models.tokenize import encode_text

    ids, _ = encode_text(prefix or " ")
    if len(ids) > limit:
        raise ValueError("tiny intervene prefix exceeds context; refuse truncated prefixes")
    return ids or [1]


def _e_premise_ids(task: Task | None, labels: list[dict]) -> list[str]:
    """E columns follow task.premises order, never labels.jsonl first-seen order."""
    order = [p.premise_id for p in (task.premises if task else []) if getattr(p, "premise_id", None)]
    seen = set(order)
    for row in labels:
        pid = row.get("premise_id")
        if pid and pid not in seen and not str(pid).startswith("sham:"):
            order.append(pid)
            seen.add(pid)
    return order


def _sanitize_cal(cal: dict) -> dict:
    out = dict(cal)
    q = out.get("q")
    if isinstance(q, float) and math.isinf(q):
        out["q"] = None
        out["infinity"] = True
    return out


def cmd_calibrate(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    alpha = float(getattr(args, "alpha", 0.4))
    head_name = getattr(args, "head", None)
    eval_mode = getattr(args, "eval_mode", "fixture")
    # Sample size is planned from pilot effect/variance; the CLI does not
    # impose an unregistered scientific minimum.  A user-supplied value is a
    # reporting threshold only and never aborts calibration.
    min_units = int(getattr(args, "min_calibration_units", None) or 0)
    cal_cfg = {
        "command": "calibrate",
        "split": args.split,
        "alpha": alpha,
        "head": head_name,
        "eval_mode": eval_mode,
        "min_calibration_units": min_units,
        "sample_size_protocol": "pilot_power_planned",
    }
    if _resume(out, getattr(args, "resume", False), cal_cfg):
        return 0
    require_split(args.split, ("calibration",), "calibration")
    if not getattr(args, "in_dir", None):
        raise ValueError("calibrate requires --in-dir")
    src = Path(args.in_dir)
    feat_dir = Path(args.features_dir) if getattr(args, "features_dir", None) else src
    labels_dir = Path(args.labels_dir) if getattr(args, "labels_dir", None) else src
    persisted = _persisted_splits(src, feat_dir, labels_dir)
    test_unit_ids = _split_member_ids(persisted, "test") if persisted else set()
    if persisted:
        scientific = getattr(args, "eval_mode", "fixture") == "scientific"
        if scientific and args.split not in {row.get("role") for row in persisted}:
            _write_stage(
                out,
                "calibration",
                [{
                    "scores": None,
                    "alpha": alpha,
                    "q": None,
                    "status": "insufficient_calibration_split",
                    "unit": "problem",
                    "n_calibration_units": 0,
                    "n_test_units": len(test_unit_ids),
                    "reason": f"no persisted {args.split} rows",
                }],
                in_dir=src,
                extra_dir=feat_dir if feat_dir != src else None,
                config=cal_cfg,
            )
            return 0
        if scientific:
            persisted = [row for row in persisted if row.get("role") == args.split]
        require_persisted_roles(persisted, args.split, "calibration", scientific=scientific, allow_mixed=True)
    outputs = []
    status = "probe_weights_or_features_missing"
    if src and (src / "probes.jsonl").exists() and feat_dir and (feat_dir / "features.npz").exists():
        probe_rows = [r for r in read_jsonl(src / "probes.jsonl") if "U" in r]
        if head_name:
            probe_rows = [r for r in probe_rows if r.get("head") == head_name]
        labs = []
        lab_path = _find_labels_jsonl(labels_dir, src, feat_dir)
        if lab_path:
            labs = [r for r in read_jsonl(lab_path) if "premise_id" in r]
            if persisted and getattr(args, "eval_mode", "fixture") == "scientific":
                allowed_ids = _split_member_ids(persisted, args.split)
                if allowed_ids:
                    labs = [r for r in labs if not (r.get("task_id") or r.get("base_group_id")) or str(r.get("task_id") or r.get("base_group_id")) in allowed_ids]
        traces = read_jsonl(feat_dir / "traces.jsonl") if (feat_dir / "traces.jsonl").exists() else []
        # Keep the full event row.  Calibration units must be keyed by the
        # trace/task that produced each hidden row; collapsing all rows onto
        # traces[0] makes the first trace dominate multi-trace calibration.
        event_nodes = []
        if (feat_dir / "event_rows.jsonl").exists():
            event_nodes = read_jsonl(feat_dir / "event_rows.jsonl")
        else:
            for trow in traces:
                for ev in trow.get("events") or []:
                    ident = ev.get("identity") or {}
                    event_nodes.append(
                        {
                            "event_id": json.dumps(ident, sort_keys=True, ensure_ascii=False) if ident else ev.get("node_id"),
                            "node_id": ev.get("node_id") or ident.get("entity_or_expression"),
                            "task_id": trow.get("task_id") or trow.get("base_group_id"),
                        }
                    )
        task_path = _find_tasks_jsonl(src, feat_dir, labels_dir)
        if task_path is None and labs:
            raise ValueError("calibrate requires tasks.jsonl so E columns follow task.premises, not label order")
        task_rows = [Task.from_dict(row) for row in read_jsonl(task_path)] if task_path else []
        task_for_e = task_rows[0] if task_rows else None
        task_anc_by_id = {}
        for owner in task_rows:
            local = ancestors(owner) if owner.nodes else {}
            for premise in owner.premises:
                if premise.premise_id:
                    local.setdefault(premise.premise_id, {premise.premise_id})
            task_anc_by_id[owner.task_id] = local
            task_anc_by_id[owner.base_group_id] = local
        premise_rows_path = feat_dir / "premise_rows.jsonl"
        if premise_rows_path.exists():
            unique = [row.get("premise_key") or row.get("premise_id") for row in read_jsonl(premise_rows_path) if row.get("premise_id")]
        else:
            unique = _e_premise_ids(task_for_e, labs)
        arrays = read_npz(feat_dir / "features.npz")
        if getattr(args, "eval_mode", "fixture") == "scientific" and len(event_nodes) != int(arrays["H"].shape[0]):
            raise ValueError(f"calibrate event identity count {len(event_nodes)} does not match H rows {arrays['H'].shape[0]}")
        for row in probe_rows:
            probe = BilinearProbe.from_row(row)
            position = row.get("position", "pre_step")
            key = "H" if position == "pre_step" else f"H_{position}"
            if key not in arrays:
                raise ValueError(f"calibrate requires feature position {key}")
            pred = probe.predict_matrix(arrays[key], arrays["E"])
            head = row.get("head") or probe.head_type or "task"
            units: dict[str, list[float]] = {}
            for i in range(pred.shape[0]):
                event_row = event_nodes[i] if i < len(event_nodes) else {}
                event_id = event_row.get("identity_key") or event_row.get("event_id") or event_row.get("node_id")
                node_id = event_row.get("node_id") or event_id
                trace_task_id = event_row.get("task_id") or event_row.get("base_group_id") or "task"
                trace_problem_id = event_row.get("base_group_id") or trace_task_id
                label_key = "task_label" if head == "task" else "behavior_label"
                truth_i = []
                known_i = False
                for j, pid in enumerate(unique):
                    premise_id = str(pid).split("::", 1)[-1]
                    premise_task_id = str(pid).split("::", 1)[0] if "::" in str(pid) else ""
                    hits = [
                        r
                        for r in labs
                        if r.get("premise_id") == premise_id
                        and (not premise_task_id or not r.get("task_id") or str(r.get("task_id")) == premise_task_id)
                        and (r.get("event_id") in {event_id, node_id, None} or event_id in str(r.get("event_id") or ""))
                        and (not r.get("task_id") or r.get("task_id") == trace_task_id)
                        and (not r.get("trace_id") or r["trace_id"] == event_row.get("trace_id"))
                    ]
                    if not hits:
                        continue
                    if any(r.get(label_key) in {0, 1, 0.0, 1.0} for r in hits):
                        known_i = True
                    if any(r.get(label_key) == 1 for r in hits):
                        local_anc = task_anc_by_id.get(trace_task_id) or task_anc_by_id.get(trace_problem_id, {})
                        if head == "task" and premise_id not in set(local_anc.get(node_id, set())) | ({node_id} if node_id else set()):
                            continue
                        truth_i.append(j)
                if not known_i:
                    continue
                empty_i = not truth_i
                val = sequence_score(pred[i].tolist(), True, empty_i, nonconformity="one_minus_p", truth_indices=None if empty_i else [j for j in truth_i if j < pred.shape[1]])
                key = trace_problem_id
                units.setdefault(key, []).append(0.0 if val is None else val)
            scores = [max(vals) for vals in units.values()] if units else None
            if scores is None:
                continue
            cal = _sanitize_cal(conformal_threshold(scores, alpha))
            outputs.append(
                {
                    "head": head,
                    "position": position,
                    "scores": scores,
                    "alpha": alpha,
                    **cal,
                    "unit": "problem",
                    "n_calibration_units": len(scores),
                    "n_test_units": len(test_unit_ids),
                    "events_per_unit": {key: len(values) for key, values in units.items()},
                    "max_nonconformity": max(scores) if scores else None,
                    "split": args.split,
                    "split_hash": digest(persisted) if persisted else None,
                    "nonconformity": "one_minus_p",
                }
            )
            status = "one_minus_p_Rsi_problem_units"
    if not outputs:
        outputs = [{
            "scores": None,
            "alpha": alpha,
            "q": None,
            "status": "insufficient_calibration_split" if getattr(args, "eval_mode", "fixture") == "scientific" else status,
            "reason": "no_calibration_units" if getattr(args, "eval_mode", "fixture") == "scientific" else status,
            "n_calibration_units": 0,
            "n_test_units": len(test_unit_ids),
            "infinity": False,
            "unit": "problem",
            "nonconformity": "one_minus_p",
        }]
    if eval_mode == "scientific":
        for row in outputs:
            n_units = int(row.get("n_calibration_units") or 0)
            if n_units < min_units:
                row.update(
                    {
                        "status": "insufficient_calibration_units",
                        "reason": f"requires at least {min_units} independent problem units",
                        "q": None,
                        "infinity": False,
                    }
                )
    _write_stage(out, "calibration", outputs, in_dir=src, extra_dir=feat_dir if feat_dir != src else None, config=cal_cfg)
    return 0


def _load_source_value_pair(src: Path) -> dict | None:
    path = Path(src) / "edits.jsonl"
    if not path.exists():
        return None
    return next((r for r in read_jsonl(path) if r.get("kind") == "source_value_pair"), None)


def _pair_source_value(matrix: np.ndarray, event_rows: list[dict], pair_meta: dict | None):
    tids = (pair_meta or {}).get("trace_ids") or {}
    base_tid = tids.get("base")
    if not base_tid or not event_rows:
        return None
    index = {}
    for i, row in enumerate(event_rows):
        if i >= len(matrix) or not np.isfinite(matrix[i]).all():
            continue
        identity = row.get("identity_key") or row.get("node_id") or ""
        index[(str(identity), row.get("trace_id"))] = i
    for donor_key in ("same_value_diff_source", "same_source_diff_value"):
        donor_tid = tids.get(donor_key)
        if not donor_tid:
            continue
        for nid, tid in list(index):
            if tid != base_tid:
                continue
            j = index.get((nid, donor_tid))
            i = index.get((nid, tid))
            if j is None or i is None:
                continue
            if (pair_meta or {}).get("targets") and event_rows[i].get("node_id") not in pair_meta["targets"]:
                continue
            if not np.allclose(matrix[i], matrix[j]):
                return int(i), int(j), donor_key
    return None


def _expressible_donor(
    matrix: np.ndarray,
    event_rows: list[dict] | None = None,
    pair_meta: dict | None = None,
    *,
    allow_fallback: bool = True,
):
    sourced = _pair_source_value(matrix, event_rows or [], pair_meta)
    if sourced is not None:
        return sourced
    if not allow_fallback:
        return None
    finite = [i for i, row in enumerate(matrix) if np.isfinite(row).all()]
    if len(finite) < 2:
        return None
    if event_rows:
        by_node: dict[str, list[int]] = {}
        for i in finite:
            if i < len(event_rows):
                by_node.setdefault(str(event_rows[i].get("node_id") or ""), []).append(i)
        skip = {"trace-t0p"}
        for idxs in by_node.values():
            usable = [i for i in idxs if event_rows[i].get("trace_id") not in skip]
            traces = [event_rows[i].get("trace_id") for i in usable]
            if len(set(traces)) >= 2:
                left, right = usable[0], next(i for i in usable if event_rows[i].get("trace_id") != event_rows[usable[0]].get("trace_id"))
                if not np.allclose(matrix[left], matrix[right]):
                    return int(left), int(right), "same_identity_fallback"
    for a, b in ((finite[0], finite[1]), (finite[0], finite[-1])):
        if not np.allclose(matrix[a], matrix[b]):
            return int(a), int(b), "finite_fallback"
    return None


def cmd_intervene(args: argparse.Namespace) -> int:
    """Run intervention and persist scientific prerequisite failures as rows."""
    if getattr(args, "all_source_pairs", False):
        src = Path(args.features_dir or args.in_dir)
        pairs = [r for r in read_jsonl(src / "edits.jsonl") if r.get("kind") == "source_value_pair"]
        roles = {r.get("task_id"): r.get("role") for r in _persisted_splits(src)}
        pairs = [p for p in pairs if roles.get(p.get("base_task_id")) == args.pair_split]
        output, collected, runtime = Path(args.out_dir), [], None
        for index, pair in enumerate(pairs):
            for kind in ("same_value_diff_source", "same_source_diff_value"):
                child = copy.copy(args)
                child.all_source_pairs = False
                child._c2_only = True
                child._source_pair = {**pair, "trace_ids": {"base": pair["trace_ids"].get("base"), kind: pair["trace_ids"].get(kind)}}
                child.out_dir = str(output / f"pair-{index}-{kind}")
                if args.backend == "frozen":
                    if runtime is None:
                        runtime = _load_frozen_runtime(args)
                    child._packed_runtime = runtime
                cmd_intervene(child)
                for row in read_jsonl(Path(child.out_dir) / "interventions.jsonl"):
                    collected.append({**row, "pair_index": index, "pair_kind": kind, "base_task_id": pair["base_task_id"],
                                      "split": args.pair_split, "analysis_eligibility": {"C2": row.get("status") == "prospective_decode", "P3": False}})
        if not collected:
            collected = [{"status": "no_source_pairs_in_split", "split": args.pair_split, "analysis_eligibility": {"C2": False, "P3": False}}]
        _write_stage(output, "interventions", collected, in_dir=src,
                     config={"command": "intervene", "all_source_pairs": True, "split": args.pair_split,
                             "n_pairs": len(pairs), "P3": "deferred_requires_S_specific_direction_fit"})
        return 0
    try:
        return _cmd_intervene_impl(args)
    except ValueError as exc:
        scientific = getattr(args, "eval_mode", "fixture") == "scientific"
        message = str(exc)
        quality_failure = message.startswith("scientific intervene requires") or message.startswith("scientific intervene refuses")
        if not scientific or not quality_failure:
            raise
        out = Path(args.out_dir)
        src = Path(args.features_dir) if getattr(args, "features_dir", None) else Path(args.in_dir)
        row = {
            "condition": "all",
            "problem_id": None,
            "status": "scientific_failure_retained",
            "failure": {"type": type(exc).__name__, "message": message},
            "analysis_eligibility": {"P3": False},
        }
        _write_stage(
            out,
            "interventions",
            [row],
            in_dir=src,
            config={
                "command": "intervene",
                "eval_mode": "scientific",
                "scientific_failures_retained": True,
                "failure_as_data": True,
            },
        )
        return 0


def _cmd_intervene_impl(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    if _resume(
        out,
        getattr(args, "resume", False),
        {
            "command": "intervene",
            "backend": getattr(args, "backend", "tiny"),
            "eval_mode": getattr(args, "eval_mode", "fixture"),
            "model_name": getattr(args, "model_name", None),
            "device": getattr(args, "device", None),
            "dev_layer_scores": list(getattr(args, "dev_layer_scores", None) or []),
        },
    ):
        return 0
    if not getattr(args, "in_dir", None):
        raise ValueError("intervene requires --in-dir")
    src = Path(args.in_dir)
    features_dir = Path(args.features_dir) if getattr(args, "features_dir", None) else src
    probes_dir = Path(args.probes_dir) if getattr(args, "probes_dir", None) else src
    labels_dir = Path(args.labels_dir) if getattr(args, "labels_dir", None) else src
    scientific = getattr(args, "eval_mode", "fixture") == "scientific"
    bank = StreamBank(0)
    rng = np.random.default_rng(int(bank.get("direction").integers(0, 2**31)))
    status = "donor_missing"
    main_norm = crand_norm = clayer_norm = None
    report = {}
    timing = "unexpressible"
    clayer_status = "dev_scores_missing"
    persisted_dev_scores = None
    persisted_dev_layers = None
    dev_score_source = "missing"
    if getattr(args, "dev_layer_scores", None):
        persisted_dev_scores = list(getattr(args, "dev_layer_scores"))
        if len(persisted_dev_scores) < 2 or not np.isfinite(np.asarray(persisted_dev_scores, dtype=float)).all():
            raise ValueError("intervene --dev-layer-scores requires at least two finite layer scores")
        dev_score_source = "cli"
        persisted_dev_layers = list(getattr(args, "dev_layer_ids", None) or range(len(persisted_dev_scores)))
        if len(persisted_dev_layers) != len(persisted_dev_scores) or len(set(persisted_dev_layers)) != len(persisted_dev_layers):
            raise ValueError("intervene --dev-layer-ids must be unique and match --dev-layer-scores")
    else:
        score_path = probes_dir / "dev_layer_scores.json"
        if score_path.exists():
            payload = read_json(score_path)
            if payload.get("status") == "ready" and payload.get("scores"):
                persisted_dev_scores = list(payload["scores"])
                persisted_dev_layers = list(payload.get("layer_ids") or range(len(persisted_dev_scores)))
                if len(persisted_dev_layers) != len(persisted_dev_scores):
                    raise ValueError("persisted dev layer ids do not match scores")
                dev_score_source = "fit_artifact"
    rng_seeds = {}
    if features_dir and (features_dir / "features.npz").exists():
        arrays = read_npz(features_dir / "features.npz")
        matrix = arrays.get("H", arrays[next(iter(arrays))])
        event_rows = read_jsonl(features_dir / "event_rows.jsonl") if (features_dir / "event_rows.jsonl").exists() else []
        pair_meta = getattr(args, "_source_pair", None) or _load_source_value_pair(features_dir)
        pair = _expressible_donor(matrix, event_rows, pair_meta, allow_fallback=not scientific)
        if pair is not None:
            i_base, i_donor, donor_kind = pair
            base, donor = np.asarray(matrix[i_base], dtype=float), np.asarray(matrix[i_donor], dtype=float)
            rank = min(2, base.shape[-1])
            basis_seed = int(bank.get("direction").integers(0, 2**31))
            sample_seed = int(bank.get("sample").integers(0, 2**31))
            perturb_seed = int(bank.get("perturb").integers(0, 2**31))
            clayer_seed = int(bank.get("control").integers(0, 2**31))
            rng_seeds = {
                "direction": basis_seed,
                "sample": sample_seed,
                "perturb": perturb_seed,
                "control": clayer_seed,
            }
            rng = np.random.default_rng(basis_seed)
            probe_rows = read_jsonl(probes_dir / "probes.jsonl") if (probes_dir / "probes.jsonl").exists() else []
            probe_u = next((np.asarray(r["U"], dtype=float) for r in probe_rows if r.get("head") == "behavior" and "U" in r), None)
            if probe_u is None:
                if not (scientific and getattr(args, "_c2_only", False)):
                    probe_u = next((np.asarray(r["U"], dtype=float) for r in probe_rows if "U" in r), None)
            if probe_u is not None:
                q, _ = np.linalg.qr(probe_u)
                if getattr(args, "_c2_only", False):
                    rank = int(np.linalg.matrix_rank(probe_u))
                basis = q[:, :rank]
                direction_status = "probe_direction"
            elif getattr(args, "eval_mode", "fixture") == "scientific":
                raise ValueError("scientific intervene requires a fitted probe direction; random basis is not evidence")
            else:
                basis = orthonormal_basis(base.shape[-1], rank, rng)
                direction_status = "random_direction_unfitted"
            main = apply_swap(base, donor, basis)
            main_delta = main - base
            main_norm = float(np.linalg.norm(main_delta))
            cr = c_rand_delta(base, donor, rank, np.random.default_rng(perturb_seed), target_norm=main_norm)
            dev_scores = persisted_dev_scores
            if dev_scores:
                scores = {int(k): float(v) for k, v in zip(persisted_dev_layers or range(len(dev_scores)), dev_scores, strict=True)}
                weak = select_weak_layer(scores)
                clayer_status = f"dev_scores_present_pending_decode:{dev_score_source}"
            else:
                if scientific:
                    raise ValueError("scientific intervene requires persisted dev layer scores for C-layer")
                weak = None
                clayer_status = "dev_scores_missing"
            layer_basis = orthonormal_basis(base.shape[-1], rank, np.random.default_rng(clayer_seed))
            cl = c_layer_delta(base, donor, layer_basis, main_norm)
            crand_norm = cr["actual_norm"]
            clayer_norm = cl["actual_norm"]
            status = "geometry_on_hidden"
            timing = "offline_hidden"
            labels_path = labels_dir / "labels.jsonl"
            if getattr(args, "_c2_only", False):
                proj = np.eye(base.shape[-1])
                inlp_status = "deferred_S_specific_direction_fit"
            elif labels_path.exists() and matrix.shape[0] >= 2:
                lab_rows = [r for r in read_jsonl(labels_path) if r.get("behavior_label") in {0, 1, 0.0, 1.0}]
                y_inlp = np.full(matrix.shape[0], np.nan, dtype=float)
                for idx, event_row in enumerate(event_rows[: matrix.shape[0]]):
                    event_id = event_row.get("identity_key") or event_row.get("event_id") or event_row.get("node_id")
                    node_id = event_row.get("node_id")
                    task_id = event_row.get("task_id") or event_row.get("base_group_id")
                    hits = [
                        row
                        for row in lab_rows
                        if row.get("event_id") in {event_id, node_id}
                        and (not row.get("task_id") or row.get("task_id") == task_id)
                    ]
                    values = {float(row["behavior_label"]) for row in hits}
                    if len(values) == 1:
                        y_inlp[idx] = values.pop()
                labeled = np.isfinite(y_inlp)
                if labeled.sum() >= 2 and len(np.unique(y_inlp[labeled])) > 1:
                    proj = inlp_remove(matrix[labeled], y_inlp[labeled])
                    inlp_status = "labeled_behavior"
                else:
                    if scientific:
                        raise ValueError("scientific intervene requires stable binary behavior labels for INLP")
                    proj = inlp_remove(np.vstack([base, donor]), np.array([0.0, 1.0]))
                    inlp_status = "fixture_smoke_two_row_fallback"
            else:
                if scientific:
                    raise ValueError("scientific intervene requires a persisted labels.jsonl for INLP")
                proj = inlp_remove(np.vstack([base, donor]), np.array([0.0, 1.0]))
                inlp_status = "fixture_smoke_two_row_fallback"
            ablated = base @ proj if proj.ndim == 2 else base
            removed = base - ablated
            rescued = rescue_controls(ablated, removed, -removed, rng)
            hook_meta = {
                "inlp_rank": None if getattr(args, "_c2_only", False) else int(np.linalg.matrix_rank(proj)),
                "inlp_retained_rank": None if getattr(args, "_c2_only", False) else int(np.linalg.matrix_rank(proj)),
                "inlp_removed_rank": None if getattr(args, "_c2_only", False) else int(proj.shape[0] - np.linalg.matrix_rank(proj)),
                "donor_rows": [i_base, i_donor],
                "donor_kind": donor_kind,
                "donor_fallback_used": donor_kind.endswith("fallback"),
                "direction_status": direction_status,
                "inlp_status": inlp_status,
                "direction_hash": hashlib.sha256(np.ascontiguousarray(basis).tobytes()).hexdigest(),
                "direction_rank": int(basis.shape[1]),
                "direction_norm": float(np.linalg.norm(basis)),
                "donor_event_key": (
                    event_rows[i_donor].get("identity_key")
                    if event_rows and i_donor < len(event_rows)
                    else None
                ),
            }
            backend = getattr(args, "backend", "tiny")
            if backend in {"tiny", "frozen"}:
                from .models.collect import _hidden_at_layer, intervene_hidden_decode
                from .models.tokenize import decode_ids, readout_layer_index
                from .models.tiny import build_tiny

                packed_runtime = _load_frozen_runtime(args) if backend == "frozen" else None
                runtime_model = None if packed_runtime is None else packed_runtime["model"]
                tokenizer = None if packed_runtime is None else packed_runtime["tokenizer"]
                traces = read_jsonl(features_dir / "traces.jsonl") if (features_dir / "traces.jsonl").exists() else []
                ev = None
                prefix = ""
                gold = None
                donor_ans = None
                want = event_rows[i_base]["node_id"] if event_rows and i_base < len(event_rows) else None
                base_tid = event_rows[i_base]["trace_id"] if event_rows and i_base < len(event_rows) else None
                donor_tid = event_rows[i_donor]["trace_id"] if event_rows and i_donor < len(event_rows) else None
                base_row = next((t for t in traces if t.get("id") == base_tid), traces[0] if traces else {})
                donor_row = next((t for t in traces if t.get("id") == donor_tid), traces[1] if len(traces) > 1 else {})
                hook_meta["base_group_id"] = base_row.get("base_group_id")
                hook_meta["task_id"] = base_row.get("task_id")
                hook_meta["problem_id"] = base_row.get("base_group_id") or base_row.get("task_id") or base_tid
                prefix = base_row.get("text") or ""
                spec_path = features_dir / "run_spec.json"
                if not spec_path.exists():
                    spec_path = probes_dir / "run_spec.json"
                spec = read_json(spec_path) if spec_path.exists() else {}
                collect_cfg = spec.get("config") or {}
                model_kind = collect_cfg.get("model_kind") or collect_cfg.get("kind") or "qwen2"
                weight_seed = int(collect_cfg.get("weight_seed") or 0)
                gold = None
                answer_kind = "numeric"
                answer_aliases = []
                task_path = features_dir / "tasks.jsonl"
                if not task_path.exists():
                    task_path = probes_dir / "tasks.jsonl"
                if task_path.exists():
                    task_data = next(row for row in read_jsonl(task_path) if row.get("task_id") == base_row.get("task_id"))
                    base_task = Task.from_dict(task_data)
                    gold = base_task.answer_spec.value
                    answer_kind = base_task.answer_spec.kind
                    answer_aliases = base_task.answer_spec.aliases
                events = base_row.get("events") or []
                from .schema import EventIdentity
                base_feature = event_rows[i_base]
                donor_feature = event_rows[i_donor]
                ev = next((e for e in events if EventIdentity(**e["identity"]).key() == base_feature.get("identity_key")), None)
                if ev:
                    prefix = prefix[: ev.get("start", len(prefix))]
                donor_event = None
                donor_events = donor_row.get("events") or []
                if want:
                    donor_event = next((e for e in donor_events if EventIdentity(**e["identity"]).key() == donor_feature.get("identity_key")), None)
                donor_src = donor_event.get("value") if donor_event else donor_row.get("answer")
                base_event = ev.get("value") if ev else base_row.get("answer")
                pair_targets = set((pair_meta or {}).get("targets") or [])
                pair_nontargets = set((pair_meta or {}).get("nontargets") or [])
                ids = list(base_row.get("token_ids") or []) or _tiny_prefix_ids(prefix)
                if ev and base_row.get("offsets"):
                    cut = ev.get("start", len(prefix))
                    trimmed = []
                    for tok, (a, b) in zip(ids, base_row.get("offsets") or []):
                        if b > cut:
                            break
                        trimmed.append(tok)
                    ids = trimmed or ids[:1]
                if base_feature.get("prefix_token_ids"):
                    ids = list(base_feature["prefix_token_ids"])
                if backend == "tiny" and len(ids) > 96:
                    raise ValueError("tiny intervene prefix exceeds context; refuse truncated prefixes")
                if packed_runtime is not None:
                    limit = packed_runtime["card"].get("context_limit")
                    if limit and len(ids) > int(limit):
                        raise ValueError(f"frozen intervene prefix {len(ids)} exceeds context {limit}")
                    hook_meta["device"] = packed_runtime.get("device")
                    hook_meta["dtype"] = packed_runtime.get("dtype")
                    hook_meta["revision"] = packed_runtime["card"].get("revision")
                hook_meta["prefix_truncated"] = False
                hook_meta["prefix_n"] = len(ids)
                hook_meta["hook_token_position"] = max(len(ids) - 1, 0)
                hook_meta["model_kind"] = model_kind
                hook_meta["weight_seed"] = weight_seed
                if packed_runtime is not None:
                    requested = collect_cfg.get("hidden_layer")
                    main_layer = readout_layer_index(packed_runtime["card"]["layers"]) if requested is None else int(requested)
                else:
                    main_layer = int(collect_cfg.get("hidden_layer") or readout_layer_index(3))
                hook_meta["hook_layer"] = main_layer
                if getattr(args, "_c2_only", False) and weak == main_layer:
                    alternative = {l: s for l, s in scores.items() if l != main_layer}
                    weak = select_weak_layer(alternative) if alternative else None
                aligned = ev is not None
                if scientific and not aligned:
                    raise ValueError("scientific intervene requires an explicitly aligned target event boundary")
                if scientific and (base_row.get("metadata") or {}).get("boundary_status") != "ok":
                    raise ValueError("scientific intervene refuses a trace with fallback token boundaries")
                decode_kw = {
                    "weight_seed": weight_seed,
                    "event_aligned": aligned,
                    "target_prefix_len": len(ids) if aligned else None,
                    "seed": sample_seed,
                    "model": runtime_model,
                    "max_new": _resolved_max_new(args, 4, 4096 if scientific else 32),
                    "eos_id": getattr(tokenizer, "eos_token_id", None),
                }
                hooked = intervene_hidden_decode(
                    model_kind,
                    ids,
                    main_layer,
                    donor=donor,
                    basis_seed=basis_seed,
                    basis=basis,
                    mode="add_delta",
                    delta=main_delta,
                    **decode_kw,
                )
                hook_meta.update(
                    {
                        "hook_once": hooked["hook"],
                        "transform": hooked["transform"],
                        "hook_timing": hooked.get("timing"),
                        "hook_token_position": hooked.get("hook_token_position"),
                        "hook_sequence_length": hooked.get("hook_sequence_length"),
                        "hook_input_norm": hooked.get("hook_input_norm"),
                        "hook_delta_norm": hooked.get("hook_delta_norm"),
                        "hook_basis_hash": hooked.get("basis_hash"),
                        "hook_basis_rank": hooked.get("basis_rank"),
                        "hook_basis_norm": hooked.get("basis_norm"),
                        "token_changed": hooked["followed_donor"],
                        "main_geometry": "pi_z_swap_projected_delta",
                        "control_transform_family": "add_delta",
                    }
                )

                def _decode_text(decoded) -> str:
                    ids_out = decoded.get("generated_ids") or []
                    if tokenizer is not None:
                        # Keep <think>/</think> markers so a truncated
                        # intervention cannot fall through to numeric answer
                        # extraction.
                        return tokenizer.decode(ids_out, skip_special_tokens=False)
                    return decode_ids(ids_out)

                requires_think_close = bool(scientific and backend == "frozen")

                def _extract_intervention_answer(text: str):
                    if requires_think_close and "</think>" not in text:
                        return None
                    return extract_answer(text, answer_kind)

                def _parse_nodes(text: str) -> dict[str, str]:
                    return {e.node_id: e.value for e in parse_events(text, base_task)}

                def _outcomes(decoded):
                    text = _decode_text(decoded)
                    ans = _extract_intervention_answer(text)
                    score = answer_score(ans, gold, answer_kind, answer_aliases)
                    parsed = _parse_nodes(text)
                    def _match(value, expected):
                        result = answer_score(value, expected, answer_kind)
                        return None if result.get("correct") is None else float(result["correct"])

                    equivalent = donor_src is not None and base_event is not None and donor_src == base_event
                    if equivalent:
                        target = None
                    elif pair_targets:
                        target = 1.0 if any(_match(parsed.get(n), donor_src) == 1.0 for n in pair_targets) else 0.0
                    else:
                        target = _match(ans, donor_src) if donor_src is not None else None
                    if pair_nontargets:
                        truth = {n.id: n.value for n in base_task.nodes}
                        truth.update({p.premise_id: p.value for p in base_task.premises if p.kind != "relation"})
                        observed = [n for n in pair_nontargets if n in parsed and n in truth]
                        nontarget = float(all(_match(parsed[n], truth[n]) == 1.0 for n in observed)) if observed else None
                    elif equivalent:
                        nontarget = None
                    else:
                        main_match = _match(ans, gold) if gold is not None else None
                        nontarget = None if main_match is None else float(main_match and not (_match(ans, donor_src) == 1.0))
                    return {
                        "target": target,
                        "nontarget": nontarget,
                        "task_correct": None if score["correct"] is None else float(score["correct"]),
                        "invalid": 1.0 if ans is None else 0.0,
                        "decode_stop_reason": decoded.get("stop_reason"),
                        "decode_complete": decoded.get("stop_reason") in {"eos", "stop_condition"},
                        "answer": ans,
                        **score,
                    }

                main_out = _outcomes(hooked)
                base_ans = _extract_intervention_answer(_decode_text({"generated_ids": hooked.get("baseline_generated_ids") or []}))
                donor_intervened = answer_score(main_out.get("answer"), donor_src, answer_kind)
                donor_baseline = answer_score(base_ans, donor_src, answer_kind)
                g_int = donor_intervened.get("correct")
                g_base = donor_baseline.get("correct")
                if g_int is not None:
                    g_int = float(g_int)
                if g_base is not None:
                    g_base = float(g_base)
                hook_meta["ie_z"] = None if g_int is None or g_base is None else g_int - g_base
                hook_meta["ie_z_g"] = "target_follow"
                base_score = answer_score(base_ans, gold, answer_kind, answer_aliases)
                hook_meta["baseline_task_correct"] = None if base_score["correct"] is None else float(base_score["correct"])
                crand_hooked = intervene_hidden_decode(model_kind, ids, main_layer, mode="add_delta", delta=cr["delta"], **decode_kw)
                crand_out = _outcomes(crand_hooked)
                hook_meta["crand_transform"] = crand_hooked["transform"]
                clayer_out = {"target": None, "nontarget": None, "task_correct": None, "invalid": None}
                if weak is not None and weak != main_layer:
                    if runtime_model is not None:
                        layer_model = runtime_model
                    else:
                        import torch

                        with torch.random.fork_rng(devices=[]):
                            torch.manual_seed(weight_seed)
                            layer_model = build_tiny(model_kind)
                    weak_base = _hidden_at_layer(layer_model, ids, weak)
                    weak_donor_ids = list(donor_feature.get("prefix_token_ids") or donor_row.get("token_ids") or ids)
                    weak_donor = _hidden_at_layer(layer_model, weak_donor_ids, weak)
                    weak_vec = weak_base[min(len(weak_base) - 1, max(len(ids) - 1, 0))]
                    weak_dvec = weak_donor[-1]
                    cl = c_layer_delta(weak_vec, weak_dvec, layer_basis, main_norm)
                    clayer_hooked = intervene_hidden_decode(model_kind, ids, weak, mode="add_delta", delta=cl["delta"], **decode_kw)
                    clayer_out = _outcomes(clayer_hooked)
                    hook_meta["clayer_token_changed"] = clayer_hooked["followed_donor"]
                    hook_meta["clayer_transform"] = clayer_hooked["transform"]
                    hook_meta["weak_layer"] = weak
                    clayer_status = "dev_weak_layer_decode"
                elif weak is not None:
                    clayer_status = "weak_layer_equals_main"
                inlp_out = {}
                if not getattr(args, "_c2_only", False):
                    inlp_hooked = intervene_hidden_decode(model_kind, ids, main_layer, mode="inlp", projector=proj, **decode_kw)
                    hook_meta["inlp_token_changed"] = inlp_hooked["followed_donor"]
                    hook_meta["inlp_transform"] = inlp_hooked["transform"]
                    inlp_out = _outcomes(inlp_hooked)
                    rescue_matched = intervene_hidden_decode(model_kind, ids, main_layer, mode="replace", delta=rescued["matched"], **decode_kw)
                    rescue_error = intervene_hidden_decode(model_kind, ids, main_layer, mode="replace", delta=rescued["error_source"], **decode_kw)
                    rescue_rand = intervene_hidden_decode(model_kind, ids, main_layer, mode="replace", delta=rescued["random"], **decode_kw)
                    hook_meta["rescue_transform"] = rescue_matched["transform"]
                    hook_meta["rescue_outcomes"] = _outcomes(rescue_matched)
                    hook_meta["rescue_error_outcomes"] = _outcomes(rescue_error)
                    hook_meta["rescue_random_outcomes"] = _outcomes(rescue_rand)
                rel = intervention_report(main_out, crand_out, clayer_out)
                dose_curve = []
                for dose in (getattr(args, "doses", None) or [0.5, 1.0, 2.0]):
                    dose_delta = (main - base) * float(dose)
                    dose_hooked = intervene_hidden_decode(model_kind, ids, main_layer, mode="add_delta", delta=dose_delta, **decode_kw)
                    dose_out = _outcomes(dose_hooked)
                    dose_curve.append(
                        {
                            "dose": float(dose),
                            "condition": "dose",
                            "actual_norm": float(np.linalg.norm(dose_delta)),
                            "hook_token_position": dose_hooked.get("hook_token_position"),
                            "hook_sequence_length": dose_hooked.get("hook_sequence_length"),
                            **dose_out,
                        }
                    )
                report = {
                    **hook_meta,
                    **rel,
                    "main_outcomes": main_out,
                    "crand_outcomes": crand_out,
                    "clayer_outcomes": clayer_out,
                    "inlp_outcomes": inlp_out,
                    "dose_curve": dose_curve,
                    "condition_records": [
                        {"condition": "baseline", **_outcomes({"generated_ids": hooked.get("baseline_generated_ids") or [],
                                                              "stop_reason": hooked.get("baseline_stop_reason")}), "actual_norm": 0.0},
                        {"condition": "main", **main_out, "actual_norm": main_norm},
                        {"condition": "crand", **crand_out, "actual_norm": crand_norm},
                        {"condition": "clayer", **clayer_out, "actual_norm": clayer_norm},
                    ] + ([] if getattr(args, "_c2_only", False) else [
                        {"condition": "inlp", **inlp_out, "actual_norm": float(np.linalg.norm(base - ablated))},
                        {"condition": "rescue_matched", **_outcomes(rescue_matched), "actual_norm": rescued["matched_norm"]},
                        {"condition": "rescue_error_source", **_outcomes(rescue_error), "actual_norm": float(np.linalg.norm(rescued["error_source"] - ablated))},
                        {"condition": "rescue_random", **_outcomes(rescue_rand), "actual_norm": rescued["random_norm"]},
                    ]),
                }
                if hooked.get("hook_fired"):
                    status = "prospective_decode"
            else:
                hook_meta["ie_z"] = ie_z(rescued["matched"], base)
                report = hook_meta
    main_outcomes = (report or {}).get("main_outcomes") or {}
    condition_records = (report or {}).get("condition_records") or []
    intervention_rows = [
        {
            "condition": item.get("condition"),
            "problem_id": (report or {}).get("problem_id"),
            "main_norm": main_norm,
            "crand_norm": crand_norm,
            "clayer_norm": clayer_norm,
            "target": item.get("target"),
            "nontarget": item.get("nontarget"),
            "task_correct": item.get("task_correct"),
            "invalid": item.get("invalid"),
            "decode_stop_reason": item.get("decode_stop_reason"),
            "decode_complete": item.get("decode_complete"),
            "actual_norm": item.get("actual_norm"),
            "status": status,
            "clayer_status": clayer_status,
            "timing": timing,
            "relative": report,
        }
        for item in condition_records
    ] or [
        {
            "condition": "main",
            "problem_id": (report or {}).get("problem_id"),
            "main_norm": main_norm,
            "crand_norm": crand_norm,
            "clayer_norm": clayer_norm,
            "target": main_outcomes.get("target"),
            "nontarget": main_outcomes.get("nontarget"),
            "task_correct": main_outcomes.get("task_correct"),
            "invalid": main_outcomes.get("invalid"),
            "actual_norm": main_norm,
            "status": status,
            "clayer_status": clayer_status,
            "timing": timing,
            "relative": report,
        }
    ]
    _write_stage(
        out,
        "interventions",
        intervention_rows,
        in_dir=features_dir,
        extra_dir=probes_dir if probes_dir != features_dir else labels_dir if labels_dir != features_dir else None,
        config={
            "command": "intervene",
            "backend": getattr(args, "backend", "tiny"),
            "eval_mode": getattr(args, "eval_mode", "fixture"),
            "model_name": getattr(args, "model_name", None),
            "device": getattr(args, "device", None),
            "dev_layer_scores": list(getattr(args, "dev_layer_scores", None) or []),
            "dev_layer_selection": dev_score_source,
            "rng_seeds": rng_seeds,
            "sampling": {"temperature": 0.6, "top_k": 20, "top_p": 0.95},
        },
    )
    return 0


def _canonical_repair_prefix(trace: dict) -> str:
    text = str(trace.get("text") or "")
    replacements = []
    for event in trace.get("events") or []:
        start, end = event.get("start"), event.get("end")
        node_id, value = event.get("node_id"), event.get("value")
        if not isinstance(start, int) or not isinstance(end, int) or not node_id or value is None:
            continue
        if 0 <= start < end <= len(text):
            replacements.append((start, end, f"{node_id} = {value}"))
    last_start = len(text)
    for start, end, replacement in sorted(replacements, reverse=True):
        if end > last_start:
            continue
        text = text[:start] + replacement + text[end:]
        last_start = start
    return text


def _learned_repair_slots(src: Path, trace_id: str, fallback: list[str]) -> tuple[list[str], dict]:
    """Resolve a probe-selected mask without silently substituting the oracle."""
    feature_path = src / "features.npz"
    probe_path = src / "probes.jsonl"
    event_path = src / "event_rows.jsonl"
    premise_path = src / "premise_rows.jsonl"
    if not all(path.exists() for path in (feature_path, probe_path, event_path, premise_path)):
        return [], {"status": "learned_mask_unavailable", "reason": "features_probes_or_identity_rows_missing"}
    arrays = read_npz(feature_path)
    if "H" not in arrays or "E" not in arrays:
        return [], {"status": "learned_mask_unavailable", "reason": "H_or_E_missing"}
    probe_row = next((row for row in read_jsonl(probe_path) if "U" in row), None)
    if probe_row is None:
        return [], {"status": "learned_mask_unavailable", "reason": "probe_weights_missing"}
    probe = BilinearProbe.from_row(probe_row)
    scores = probe.predict_matrix(arrays["H"], arrays["E"])
    event_rows = read_jsonl(event_path)
    candidates = [i for i, row in enumerate(event_rows) if row.get("trace_id") == trace_id]
    if not candidates:
        return [], {"status": "learned_mask_unavailable", "reason": "trace_event_missing"}
    row_scores = scores[candidates[0]]
    premise_rows = read_jsonl(premise_path)
    selected = [
        str(row.get("premise_id"))
        for index, row in enumerate(premise_rows)
        if index < len(row_scores) and float(row_scores[index]) >= 0.5 and row.get("premise_id")
    ]
    return selected, {
        "status": "learned_mask_selected",
        "threshold": 0.5,
        "probe_head": probe_row.get("head"),
        "selected_slots": selected,
        "candidate_slots": [row.get("premise_id") for row in premise_rows if row.get("premise_id")],
    }


def cmd_repair(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    if _resume(out, getattr(args, "resume", False), {"command": "repair"}):
        return 0
    if not getattr(args, "in_dir", None):
        raise ValueError("repair requires --in-dir")
    src = Path(args.in_dir)
    requested_masks = list(MASKS_MAIN) if args.mask == "all" else [args.mask]
    original = [4, 4, 4]
    prefix = "updated prefix"
    slots = ["p1", "p2", "q"]
    tasks = [Task.from_dict(row) for row in read_jsonl(src / "tasks.jsonl")] if (src / "tasks.jsonl").exists() else []
    base_task = tasks[0] if tasks else None
    edited_task = tasks[1] if len(tasks) > 1 else base_task
    if edited_task is not None:
        prefix = edited_task.question or prefix
        changed = set()
        if (src / "edits.jsonl").exists():
            first_edit = next((r for r in read_jsonl(src / "edits.jsonl") if r.get("changed_premise_ids")), {})
            changed = set(first_edit.get("changed_premise_ids") or [])
        from .graphs import oracle_mask

        graph_slots = [p.premise_id for p in edited_task.premises if p.kind not in {"placeholder", "spec"}]
        graph_slots.extend(n.id for n in edited_task.nodes if n.id not in graph_slots)
        if changed and edited_task.nodes:
            dirty = oracle_mask(edited_task, changed)["slots"]
            slots = list(dirty) + [item for item in graph_slots if item not in dirty]
        elif graph_slots:
            slots = graph_slots
    if src and (src / "traces.jsonl").exists():
        traces = read_jsonl(src / "traces.jsonl")
        repair_trace = next(
            (
                trace
                for trace in traces
                if edited_task is not None and trace.get("task_id") == edited_task.task_id and trace.get("events")
            ),
            traces[0],
        )
        original = repair_trace.get("token_ids") or original
        retained_prefix = _canonical_repair_prefix(repair_trace)
        if retained_prefix:
            prefix = retained_prefix
        ev_slots = []
        for ev in repair_trace.get("events") or []:
            nid = ev.get("node_id") or (ev.get("identity") or {}).get("entity_or_expression")
            if nid and nid not in ev_slots:
                ev_slots.append(nid)
        for nid in ev_slots:
            if nid not in slots:
                slots.append(nid)
    learned_mask_meta = {"status": "not_requested"}
    if "learned" in requested_masks:
        learned_slots, learned_mask_meta = _learned_repair_slots(src, repair_trace.get("id", "") if "repair_trace" in locals() else "", slots)
        learned_slots_for_run = learned_slots
    else:
        learned_slots_for_run = slots
    eval_mode = getattr(args, "eval_mode", "fixture")
    group = ""
    if src and (src / "traces.jsonl").exists():
        group = repair_trace.get("base_group_id") or ""
    backend = getattr(args, "backend", "offline")
    repair_seed = int(StreamBank(0).get("repair").integers(0, 2**31))
    execute = None
    if backend == "frozen":
        packed_runtime = _load_frozen_runtime(args)
        max_new = _resolved_max_new(args, 8, 4096 if eval_mode == "scientific" else 32)

        def execute(mask, slots, original_tokens, new_prefix):
            return execute_repair_frozen(
                mask,
                slots,
                original_tokens,
                new_prefix,
                packed=packed_runtime,
                max_new=max_new,
                seed=repair_seed,
            )

    elif eval_mode == "scientific" or backend == "tiny":
        def execute(mask, slots, original_tokens, new_prefix):
            return execute_repair_tiny(mask, slots, original_tokens, new_prefix, seed=repair_seed)
    recs = []
    for mask_name in requested_masks:
        mask_slots = learned_slots_for_run if mask_name == "learned" else slots
        if eval_mode == "scientific":
            recs.extend(consecutive_repairs(mask_name, mask_slots, original, prefix, k_max=5, execute=execute, run_id="repair", base_group_id=group))
        else:
            recs.append(run_repair(mask_name, ["q"], original, new_prefix=prefix, execute=execute, run_id="repair", base_group_id=group, k=1))
    # Score every generated answer with the task protocol and compare it with
    # a same-prefix full recompute.  The baseline stays in metadata so the
    # public k curve still has one row per requested repair.
    full_by_k = {}
    if execute is not None and base_task is not None:
        for rec in recs:
            full_by_k[(rec.mask, rec.k)] = run_repair(
                "full_recompute",
                [],
                original,
                prefix,
                execute=execute,
                run_id="repair-full",
                base_group_id=group,
                k=rec.k,
            )
    score_task = edited_task or base_task
    if score_task is not None:
        spec = score_task.answer_spec
        for rec in recs:
            if rec.generated_text:
                raw = extract_answer(rec.generated_text, spec.kind)
                score = answer_score(raw, spec.value, spec.kind, spec.aliases)
                rec.answer_raw = raw
                rec.answer_normalized = score.get("answer_normalized")
                rec.gold_normalized = score.get("gold_normalized")
                rec.score_status = score.get("score_status", "unscored")
                rec.correct = score.get("correct")
                rec.invalid = raw is None
                rec.legal = not rec.invalid
            baseline = full_by_k.get((rec.mask, rec.k)) or full_by_k.get(("full_recompute", rec.k))
            if baseline is not None and rec.answer_normalized is not None and baseline.generated_text:
                baseline_raw = extract_answer(baseline.generated_text, spec.kind)
                baseline_score = answer_score(baseline_raw, spec.value, spec.kind, spec.aliases)
                rec.full_recompute_match = (
                    rec.answer_normalized == baseline_score.get("answer_normalized")
                    if baseline_score.get("answer_normalized") is not None
                    else None
                )
    for rec in recs:
        rec.record_id = f"{rec.run_id}:{rec.base_group_id}:{rec.mask}:k{rec.k}"
    _write_stage(
        out,
        "repairs",
        [rec.to_dict() for rec in recs],
        in_dir=src,
        config={
            "command": "repair",
            "eval_mode": eval_mode,
            "masks": list(ALL_MASKS),
            "backend": backend,
            "model_name": getattr(args, "model_name", None),
            "cost_protocol": "wall_seconds_prefill_and_decode_executor",
            "rng_stream": "repair",
            "repair_seed": repair_seed,
            "sampling": {"temperature": 0.6, "top_k": 20, "top_p": 0.95},
            "learned_mask": learned_mask_meta,
        },
    )
    return 0


def cmd_transfer(args: argparse.Namespace) -> int:
    """Run transfer from persisted pair arrays with explicit pair identity."""
    out = Path(args.out_dir)
    src = Path(args.in_dir) if getattr(args, "in_dir", None) else None
    if src is None:
        raise ValueError("transfer requires --in-dir")
    source_path = src / "source.npy"
    target_path = src / "target.npy"
    if not source_path.exists() or not target_path.exists():
        raise FileNotFoundError("transfer requires source.npy and target.npy")
    source = np.asarray(np.load(source_path, allow_pickle=False), dtype=float)
    target = np.asarray(np.load(target_path, allow_pickle=False), dtype=float)
    pair_ids = read_jsonl(src / "pair_ids.jsonl") if (src / "pair_ids.jsonl").exists() else []
    source_ids = [str(row.get("source_id") or row.get("pair_id") or row.get("id")) for row in pair_ids]
    target_ids = [str(row.get("target_id") or row.get("pair_id") or row.get("id")) for row in pair_ids]
    if source_ids and len(source_ids) != source.shape[0]:
        raise ValueError("pair_ids must cover every source row")
    if target_ids and len(target_ids) != target.shape[0]:
        raise ValueError("pair_ids must cover every target row")
    direct = direct_transfer(source.shape[-1], target.shape[-1])
    direct_status = direct.get("status")
    if source.shape[0] != target.shape[0]:
        direct_status = "not_applicable_pair_mismatch"
    records = [{"mode": "direct", **direct, "status": direct_status, "pair_count": source.shape[0] if source.shape[0] == target.shape[0] else None, "held_out": False}]
    mode = getattr(args, "mode", "direct")
    if mode in {"unlabeled", "supervised"}:
        roles = [str(row.get("split") or row.get("role") or "") for row in pair_ids]
        if not roles or len(roles) != source.shape[0] or not all(roles):
            records.append({"mode": mode, "status": "missing_transfer_split", "held_out": False, "label_use": mode == "supervised"})
            write_jsonl(out / "transfer.jsonl", records)
            _write_stage(out, "transfer", records, in_dir=src, config={"command": "transfer", "mode": mode, "split": args.split})
            return 0
        train_mask = np.asarray([role in {args.split, "train", "transfer_train"} for role in roles], dtype=bool)
        test_mask = np.asarray([role in {"test", "transfer_test"} for role in roles], dtype=bool)
        if not train_mask.any() or not test_mask.any():
            records.append({"mode": mode, "status": "missing_held_out_transfer_test", "held_out": False, "label_use": mode == "supervised"})
            write_jsonl(out / "transfer.jsonl", records)
            _write_stage(out, "transfer", records, in_dir=src, config={"command": "transfer", "mode": mode, "split": args.split})
            return 0
        labels = None
        label_path = src / "labels.npy"
        if label_path.exists():
            labels = np.asarray(np.load(label_path, allow_pickle=False), dtype=float)
        train_labels = labels[train_mask] if labels is not None else None
        fitted = fit_linear_map(source[train_mask], target[train_mask], args.split, labeled=mode == "supervised", labels=train_labels)
        heldout_target = apply_map(target[test_mask], fitted)
        heldout_error = float(np.mean((heldout_target - source[test_mask]) ** 2))
        records.append(
            {
                "mode": mode,
                "status": fitted["status"],
                "pair_count": int(train_mask.sum()),
                "source_dim": int(source.shape[1]),
                "target_dim": int(target.shape[1]),
                "split": args.split,
                "held_out": True,
                "held_out_test_count": int(test_mask.sum()),
                "held_out_geometry_error": heldout_error,
                "label_use": bool(fitted.get("uses_labels")),
                "pair_ids": source_ids or None,
                "geometry_error": float(np.mean((apply_map(target[train_mask], fitted) - source[train_mask]) ** 2)),
                "train_pair_ids": [source_ids[i] for i, flag in enumerate(train_mask) if flag] if source_ids else None,
                "test_pair_ids": [source_ids[i] for i, flag in enumerate(test_mask) if flag] if source_ids else None,
            }
        )
    write_jsonl(out / "transfer.jsonl", records)
    _write_stage(
        out,
        "transfer",
        records,
        in_dir=src,
        config={
            "command": "transfer",
            "mode": mode,
            "split": args.split,
            "source_model_name": getattr(args, "source_model_name", None),
            "target_model_name": getattr(args, "target_model_name", None),
            "transfer_protocol": "held_out_pair_identity",
        },
    )
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    src = Path(args.in_dir) if args.in_dir else None
    if src is None:
        raise ValueError("analyze requires --in-dir")
    if src is not None and src.exists() and src.is_file():
        raise NotADirectoryError(f"--in-dir must be a directory: {src}")
    trace_rows = read_jsonl(src / "traces.jsonl") if src and (src / "traces.jsonl").exists() else []
    failure_statuses = {"parse_failed", "natural_truncated", "answer_missing"}
    trace_failure_count = sum(1 for row in trace_rows if row.get("status") in failure_statuses)
    if _resume(out, getattr(args, "resume", False), {"command": "analyze"}):
        return 0
    table = []
    dens = None
    if src and (src / "p1_table.jsonl").exists():
        table = read_jsonl(src / "p1_table.jsonl")
    if src and (src / "labels.jsonl").exists():
        for row in read_jsonl(src / "labels.jsonl"):
            if "densities" in row:
                dens = row["densities"]
    if src and (src / "features.npz").exists():
        feat = read_npz(src / "features.npz")
        h_dim = int(np.asarray(feat.get("H", next(iter(feat.values())))).shape[-1])
        xfer = direct_transfer(h_dim, h_dim)
        xfer["status"] = "not_evaluated" if h_dim else xfer["status"]
    else:
        xfer = {"status": "not_evaluated", "source_dim": None, "target_dim": None}
    if src and (src / "transfer_pairs.npz").exists():
        packed = read_npz(src / "transfer_pairs.npz")
        mapped = fit_linear_map(packed["source"], packed["target"], "transfer_pairs", labeled="labels" in packed, labels=packed.get("labels"))
        pred = apply_map(packed["target"], mapped)
        xfer = {**direct_transfer(pred.shape[-1], packed["source"].shape[-1]), "fit": mapped["status"], "uses_labels": mapped["uses_labels"]}
    p1 = p2 = p3 = None
    status = "not_evaluated"
    if table:
        numeric_table = []
        for row in table:
            normalized = {
                **row,
                "length": row.get("length", row.get("chain_length")),
                "rho": row.get("rho"),
            }
            if row.get("analysis_unit") == "trajectory" and row.get("split") in {"probe_train", "test"} and all(isinstance(normalized.get(key), (int, float)) and np.isfinite(float(normalized[key])) for key in ("length", "op", "rho", "y")):
                numeric_table.append(normalized)
        if numeric_table:
            partitions = sorted({(str(row.get("position") or "unspecified"), str(row.get("head") or "unspecified")) for row in numeric_table})
            partition_results = []
            for position, head in partitions:
                selected = [row for row in numeric_table if str(row.get("position") or "unspecified") == position and str(row.get("head") or "unspecified") == head]
                length = np.array([r["length"] for r in selected], dtype=float)
                op = np.array([r["op"] for r in selected], dtype=float)
                rho = np.array([r["rho"] for r in selected], dtype=float)
                y = np.array([r["y"] for r in selected], dtype=float)
                held = np.array([r.get("held_out", False) for r in selected], dtype=bool)
                groups = [str(r.get("problem_id") or r.get("base_group_id") or i) for i, r in enumerate(selected)]
                ho = held if held.any() and not held.all() else None
                result = p1_incremental(length, op, rho, y, held_out=ho, groups=groups, rng=np.random.default_rng(0))
                partition_results.append({"position": position, "head": head, "n_rows": len(selected), **result})
            primary = next((row for row in partition_results if row["position"] == "pre_step" and row["head"] == "behavior"), partition_results[0])
            p1 = {**primary, "by_head_position": partition_results}
            if p1.get("delta_auc") is not None:
                status = "evaluated_descriptive"
        else:
            status = "insufficient_numeric_p1_rows"
    measurements = {
        "status": status,
        "transfer": xfer,
        "rho_S_excess": None if not dens else dens.get("rho_S_excess"),
        "null_reason": None if not dens else dens.get("null_reason"),
        "labels_present": bool(src and (src / "labels.jsonl").exists()),
        "p1_coverage": {"total_trajectories": len(table), "observed_rho": sum(r.get("rho") is not None for r in table),
                        "missing_rho": sum(r.get("rho") is None for r in table),
                        "itt_correct": sum(r.get("y") == 1 for r in table),
                        "note": "Missing rho remains in ITT accounting but cannot enter attribution regression."},
        "analysis_protocol": {
            "p1_primary": "observed_matched_support_descriptive",
            "p1_accuracy_accounting": "intention_to_treat",
            "p1_failure_as_incorrect": True,
            "p1_missing_rho": "retained_in_accounting_excluded_from_regression",
            "trace_failure_count": trace_failure_count,
            "auc_baseline": {"raw_auc": 0.5, "delta_auc": 0.0},
            "inference_unit": "problem",
        },
    }
    decision = week8_decision(measurements)
    if src and (src / "p2_table.jsonl").exists():
        p2 = p2_from_rows(read_jsonl(src / "p2_table.jsonl"))
    elif src and (src / "labels.jsonl").exists():
        produced = _p2_rows_from_labels(src)
        if produced:
            write_jsonl(out / "p2_table.jsonl", produced)
            p2 = p2_from_rows(produced)
    if src and (src / "p3_table.jsonl").exists():
        p3 = p3_from_rows(read_jsonl(src / "p3_table.jsonl"))
    elif src and (src / "interventions.jsonl").exists():
        produced = _p3_rows_from_interventions(src)
        if produced:
            write_jsonl(out / "p3_table.jsonl", produced)
            p3 = p3_from_rows(produced)
    appendix = {}
    if src and (src / "cone_table.jsonl").exists():
        rows = read_jsonl(src / "cone_table.jsonl")
        appendix["cone"] = cone_fit(np.array([r["x"] for r in rows]), np.array([r["y"] for r in rows]))
    if src and (src / "embed_a.npy").exists():
        if not (src / "embed_b.npy").exists():
            appendix["retrieval"] = {"status": "missing_embedding_pair", "embedding_kind": "provided", "n": 0}
        else:
            a = np.load(src / "embed_a.npy", allow_pickle=False)
            b = np.load(src / "embed_b.npy", allow_pickle=False)
            changed = [row.get("changed", False) for row in read_jsonl(src / "embedding_pairs.jsonl")] if (src / "embedding_pairs.jsonl").exists() else [False] * min(len(a), len(b))
            if len(a) != len(b) or len(changed) != len(a):
                appendix["retrieval"] = {"status": "pair_count_mismatch", "embedding_kind": "provided", "n": 0}
            else:
                appendix["retrieval"] = retrieval_scatter(embeddings_a=a, embeddings_b=b, answer_changed=changed)
    if src and (src / "texts_a.jsonl").exists() and (src / "texts_b.jsonl").exists():
        a = [r["text"] for r in read_jsonl(src / "texts_a.jsonl")]
        b = [r["text"] for r in read_jsonl(src / "texts_b.jsonl")]
        changed = [r.get("changed", False) for r in read_jsonl(src / "texts_a.jsonl")]
        appendix["retrieval"] = retrieval_scatter(texts_a=a, texts_b=b, answer_changed=changed)
    if src and (src / "geom_a.jsonl").exists():
        a = np.array(read_jsonl(src / "geom_a.jsonl")[0]["rows"])
        b = np.array(read_jsonl(src / "geom_b.jsonl")[0]["rows"])
        appendix["procrustes"] = common_dim_then_procrustes(a, b)
    if src and (src / "repairs.jsonl").exists():
        appendix["consecutive_k"] = sorted({row.get("k") for row in read_jsonl(src / "repairs.jsonl") if row.get("k")})
    if src and (src / "probes.jsonl").exists() and (src / "labels.jsonl").exists():
        if (src / "features.npz").exists():
            row = next((r for r in read_jsonl(src / "probes.jsonl") if "U" in r), None)
            if row:
                probe = BilinearProbe.from_row(row)
                arrays = read_npz(src / "features.npz")
                pred_m = probe.predict_matrix(arrays["H"], arrays["E"])
                labels = [r for r in read_jsonl(src / "labels.jsonl") if r.get("task_label") in {0, 1, 0.0, 1.0}]
                explicit_partition = any(r.get("split") is not None or r.get("held_out") is not None for r in labels)
                if explicit_partition:
                    labels = [
                        r
                        for r in labels
                        if bool(r.get("held_out")) or str(r.get("split") or "") in {"dev", "test", "probe_test"}
                    ]
                event_rows = read_jsonl(src / "event_rows.jsonl") if (src / "event_rows.jsonl").exists() else []
                task = Task.from_dict(read_jsonl(src / "tasks.jsonl")[0]) if (src / "tasks.jsonl").exists() else None
                unique = _e_premise_ids(task, labels)
                gold, pred = [], []
                for lab in labels:
                    pid = lab.get("premise_id")
                    if pid not in unique:
                        continue
                    j = unique.index(pid)
                    eid = lab.get("event_id")
                    i = 0
                    for idx, ev in enumerate(event_rows):
                        if eid in {ev.get("identity_key"), ev.get("event_id"), ev.get("node_id")}:
                            i = idx
                            break
                    if i < pred_m.shape[0] and j < pred_m.shape[1]:
                        gold.append(int(lab["task_label"]))
                        pred.append(1 if float(pred_m[i, j]) >= 0.5 else 0)
                if gold:
                    metric = probe_prf1(pred, gold)
                    appendix["probe_prf1"] = {
                        **metric,
                        "split": "held_out" if explicit_partition else "unpartitioned",
                        "held_out": bool(explicit_partition),
                        "status": "held_out_descriptive" if explicit_partition else "descriptive_unpartitioned",
                        "not_for_claims": not explicit_partition,
                    }
                else:
                    appendix["probe_prf1"] = {
                        "status": "no_scored_rows",
                        "split": "held_out" if explicit_partition else "unpartitioned",
                        "held_out": bool(explicit_partition),
                        "not_for_claims": not explicit_partition,
                    }
        else:
            appendix["probe_prf1"] = {"status": "features_missing_refuses_loss_proxy"}
    report = {
        "status": measurements["status"],
        "transfer": xfer,
        "week8": decision,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "densities": dens,
        "appendix": appendix,
        "analysis_protocol": measurements["analysis_protocol"],
        "scientific_conclusion": None,
    }
    write_json(out / "report.json", report)
    _write_stage(
        out,
        "analysis",
        [{"week8": decision, "transfer": xfer, "p1": p1, "p2": p2, "p3": p3, "appendix": appendix}],
        extra_files=[out / "report.json"],
        in_dir=src,
        config={"command": "analyze", "analysis_protocol": measurements["analysis_protocol"]},
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reasoning-diff")
    sub = parser.add_subparsers(dest="cmd", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--fixture", required=True)
    prepare.add_argument("--out-dir", required=True)
    prepare.add_argument("--split-seed", type=int, default=0)
    prepare.add_argument("--edit-premise")
    prepare.add_argument("--edit-value")
    prepare.add_argument("--sham-opportunities", type=int, default=0)
    prepare.add_argument("--n-seeds", type=int, default=None)
    prepare.add_argument("--resume", action="store_true")
    prepare.add_argument("--checkpoint-traces", action="store_true")
    prepare.add_argument("--eval-mode", choices=("fixture", "scientific"), default="fixture")
    prepare.add_argument("--kind", default="t1_fixture")
    prepare.add_argument("--snapshot")
    prepare.add_argument("--split-fractions", nargs=6, type=float)
    prepare.add_argument("--weight-seed", type=int, default=0)
    prepare.add_argument("--t1-ops", nargs="+", type=int)
    prepare.add_argument("--sidecar")
    prepare.add_argument("--backend", choices=("tiny", "frozen"), default="tiny")
    prepare.add_argument("--model-name")
    prepare.add_argument("--device")
    prepare.add_argument("--max-new", type=int)
    prepare.add_argument("--temperature", type=float, default=0.6)
    prepare.add_argument("--top-k", type=int, default=20)
    prepare.add_argument("--top-p", type=float, default=0.95)
    prepare.add_argument("--disable-thinking", action="store_true")
    prepare.add_argument("--code-revision")
    # Kept as a compatibility flag; scientific runs always retain failures.
    prepare.add_argument("--require-valid-traces", action="store_true", help=argparse.SUPPRESS)
    prepare.add_argument("--behavior-repeats", type=int, default=None)
    prepare.add_argument("--premise-protocol", choices=("leaf", "sentence_graph"), default="leaf")
    prepare.add_argument("--noise-reference", choices=("independent_sham", "base_pairs"), default="independent_sham")
    prepare.set_defaults(func=cmd_prepare)

    def stage(name, extra=None):
        p = sub.add_parser(name)
        p.add_argument("--out-dir", required=True)
        p.add_argument("--in-dir")
        p.add_argument("--resume", action="store_true")
        p.add_argument("--eval-mode", choices=("fixture", "scientific"), default="fixture")
        if extra:
            extra(p)
        return p

    c = stage(
        "collect",
        lambda p: (
            p.add_argument("--fixture", required=True),
            p.add_argument("--backend", choices=("tiny", "offline", "frozen"), default="tiny"),
            p.add_argument("--kind", default="t1_fixture"),
            p.add_argument("--snapshot"),
            p.add_argument("--shard", action="store_true"),
            p.add_argument("--model-kind", default="qwen2"),
            p.add_argument("--weight-seed", type=int, default=0),
            p.add_argument("--model-name"),
            p.add_argument("--device"),
            p.add_argument("--hidden-layer", type=int),
        ),
    )
    c.set_defaults(func=cmd_collect)
    stage("label").set_defaults(func=cmd_label)
    f = stage("fit")
    f.add_argument("--split", default="probe_train")
    f.add_argument("--labels-dir")
    f.add_argument("--position", choices=("pre_step", "pre_value", "post_step", "all"), default="pre_step")
    f.add_argument("--dev-layer-scores", nargs="*", type=float)
    f.add_argument("--dev-layer-ids", nargs="*", type=int)
    f.set_defaults(func=cmd_fit)
    cal = stage(
        "calibrate",
        lambda p: (
            p.add_argument("--split", default="calibration"),
            p.add_argument("--features-dir"),
            p.add_argument("--labels-dir"),
            p.add_argument("--alpha", type=float, default=0.4),
            p.add_argument("--min-calibration-units", type=int),
            p.add_argument("--head", choices=("task", "behavior")),
        ),
    )
    cal.set_defaults(func=cmd_calibrate)
    stage(
        "intervene",
        lambda p: (
            p.add_argument("--backend", choices=("tiny", "offline", "frozen"), default="tiny"),
            p.add_argument("--model-name"),
            p.add_argument("--device"),
            p.add_argument("--max-new", type=int),
            p.add_argument("--features-dir"),
            p.add_argument("--probes-dir"),
            p.add_argument("--labels-dir"),
            p.add_argument("--dev-layer-scores", nargs="*", type=float),
            p.add_argument("--dev-layer-ids", nargs="*", type=int),
            p.add_argument("--doses", nargs="*", type=float),
            p.add_argument("--all-source-pairs", action="store_true"),
            p.add_argument("--pair-split", choices=("dev", "test"), default="test"),
        ),
    ).set_defaults(func=cmd_intervene)
    r = stage(
        "repair",
        lambda p: (
            p.add_argument("--mask", default="task_oracle"),
            p.add_argument("--backend", choices=("tiny", "offline", "frozen"), default="offline"),
            p.add_argument("--model-name"),
            p.add_argument("--device"),
            p.add_argument("--max-new", type=int),
        ),
    )
    r.set_defaults(func=cmd_repair)
    stage("analyze").set_defaults(func=cmd_analyze)
    transfer = stage(
        "transfer",
        lambda p: (
            p.add_argument("--mode", choices=("direct", "unlabeled", "supervised"), default="direct"),
            p.add_argument("--split", default="transfer_pairs"),
            p.add_argument("--source-model-name"),
            p.add_argument("--target-model-name"),
        ),
    )
    transfer.set_defaults(func=cmd_transfer)
    noop = sub.add_parser("noop")
    noop.add_argument("--fixture", required=True)
    noop.add_argument("--out-dir", required=True)
    noop.add_argument("--in-dir")
    noop.add_argument("--kind", default="t1_fixture")
    noop.add_argument("--snapshot")
    noop.add_argument("--sidecar")
    noop.add_argument("--eval-mode", choices=("fixture", "scientific"), default="fixture")
    noop.add_argument("--backend", choices=("tiny", "frozen"), default="tiny")
    noop.add_argument("--model-name")
    noop.add_argument("--device")
    noop.add_argument("--weight-seed", type=int, default=0)
    noop.add_argument("--max-new", type=int)
    noop.add_argument("--positions", nargs="+", choices=("front", "mid", "back"))
    noop.add_argument("--surface", nargs="+", choices=("low", "medium", "high"))
    noop.add_argument("--sentence", default="A harmless unrelated sentence is inserted.")
    noop.add_argument("--resume", action="store_true")
    noop.set_defaults(func=cmd_noop)
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        out = getattr(args, "out_dir", None)
        if out:
            path = Path(out)
            path.mkdir(parents=True, exist_ok=True)
            manifest = path / "manifest.json"
            preserve = False
            if manifest.exists():
                try:
                    body = read_json(manifest)
                    preserve = bool(
                        body.get("success_count")
                        or (body.get("record_counts") or {}).get("success")
                        or (body.get("counts") or {}).get("success")
                    )
                except Exception:
                    preserve = False
            failure = {"error": type(exc).__name__, "message": str(exc)}
            if preserve:
                # A failed resume is an attempt history entry, not the
                # authoritative stage result.  Keep the familiar failure
                # marker while the retry is pending; a successful stage
                # write removes it before rebuilding the manifest.
                with (path / "failure_attempts.jsonl").open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(failure, ensure_ascii=False, sort_keys=True) + "\n")
                write_json(path / "failure.json", failure)
            else:
                write_json(path / "failure.json", failure)
                try:
                    write_manifest(path, [path / "failure.json"], {"success": 0, "failure": 1})
                except Exception:
                    pass
        raise


if __name__ == "__main__":
    raise SystemExit(main())
