"""Stage CLI: prepare → collect → label → fit → calibrate → intervene → repair → analyze."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import fields
from pathlib import Path

import numpy as np

from .analysis import cone_fit, p1_incremental, p2_from_rows, p3_from_rows, retrieval_scatter, week8_decision
from .artifacts import completed_shard_ok, write_manifest, write_run_spec
from .edits import apply_value_edit, make_source_value_pair
from .baselines import attention_mean, attention_rollout, fit_attention_threshold, fit_text_predictor, verbalizer
from .events import align_events, align_events_monotonic, extract_answer, parse_events, parse_fixture_events, review_export
from .probes.boundary import BoundaryMLP
from .graphs import ancestors
from .interventions import apply_swap, c_layer_delta, c_rand_delta, ie_z, inlp_remove, intervention_report, orthonormal_basis, rescue_controls, select_weak_layer
from .io import file_digest, read_json, read_jsonl, read_npz, write_json, write_jsonl, write_npz
from .measure import build_labels, compare_pair, event_density_sets, preservation_to_csp, probe_prf1
from .models.features import select_prefix_index
from .probes.bilinear import BilinearProbe
from .probes.calibrate import conformal_threshold, sequence_score
from .repair import ALL_MASKS, consecutive_repairs, execute_repair_frozen, execute_repair_tiny, run_repair
from .rng import StreamBank
from .schema import Observation, Task, Trace
from .splits import DEFAULT_FRACTIONS, require_persisted_roles, require_split, split_for_task
from .tasks.catalog import load_snapshot
from .tasks.t1_fixture import load_t1_fixture
from .transfer import apply_map, common_dim_then_procrustes, direct_transfer, fit_linear_map


def _load_frozen_runtime(args: argparse.Namespace):
    name = getattr(args, "model_name", None)
    if not name:
        raise ValueError("frozen backend requires --model-name")
    from .models.adapters import load_frozen

    return load_frozen(name, device=getattr(args, "device", None))


def _resolved_max_new(args: argparse.Namespace, tiny_default: int, frozen_default: int) -> int:
    value = getattr(args, "max_new", None)
    if value is not None:
        return int(value)
    return frozen_default if getattr(args, "backend", "tiny") == "frozen" else tiny_default


def _observation_from_dict(data: dict) -> Observation:
    allowed = {item.name for item in fields(Observation)}
    return Observation(**{key: value for key, value in data.items() if key in allowed})


_STAGE_ARTIFACTS = {
    "prepare": ("tasks.jsonl", "traces.jsonl", "observations.jsonl", "labels.jsonl", "splits.jsonl", "run_spec.json"),
    "collect": ("features.npz", "traces.jsonl", "run_spec.json"),
    "label": ("labels.jsonl", "run_spec.json"),
    "fit": ("probes.jsonl", "run_spec.json"),
    "calibrate": ("calibration.jsonl", "run_spec.json"),
    "intervene": ("interventions.jsonl", "run_spec.json"),
    "repair": ("repairs.jsonl", "run_spec.json"),
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
    events = parse_fixture_events(text, task)
    for event in events:
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
        correct=True,
        run_id=trace_id,
        record_id=trace_id,
    )


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
    merged = {"command": name, **(config or {})}
    source_kinds = {}
    for upstream_dir in (in_dir, extra_dir):
        if upstream_dir is None:
            continue
        upstream_spec = Path(upstream_dir) / "run_spec.json"
        if upstream_spec.exists():
            try:
                source_kinds.update(read_json(upstream_spec).get("source_kinds") or {})
            except (OSError, TypeError, ValueError):
                pass
    if not source_kinds:
        source_kinds = {"cli": "fixture"}
    write_run_spec(
        out,
        {
            "config": merged,
            "source_kinds": source_kinds,
            "rng": {"stream": name},
            "input_hashes": hashes,
        },
    )
    files.append(out / "run_spec.json")
    report = out / "report.json"
    if report.exists() and report not in files:
        files.append(report)
    write_manifest(out, files, counts or {name: len(rows), "success": 1, "failure": 0}, upstream_ids=upstream)


def _default_edit(task: Task) -> tuple[str, str]:
    facts = [p for p in task.premises if p.kind != "placeholder"]
    zero = next((p for p in facts if p.value in {"0", "0.0"}), None)
    if zero is not None:
        return zero.premise_id, "2"
    if facts:
        return facts[-1].premise_id, "2"
    raise ValueError("no editable non-placeholder premise")


def _load_tasks(args) -> list[Task]:
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


def _allowed_edits(task: Task) -> list:
    edits = []
    for premise in task.premises:
        if premise.kind == "placeholder" or not premise.value:
            continue
        try:
            alt = "2" if premise.value in {"0", "0.0"} else "0"
            edits.append(apply_value_edit(task, premise.premise_id, alt))
        except ValueError:
            continue
    return edits


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
        "split_seed": args.split_seed,
        "split_fractions": list(fractions),
        "weight_seed": getattr(args, "weight_seed", 0),
        "backend": getattr(args, "backend", "tiny"),
        "model_name": getattr(args, "model_name", None),
        "device": getattr(args, "device", None),
        "max_new": _resolved_max_new(args, 8, 256),
        "temperature": getattr(args, "temperature", 1.0),
        "top_k": getattr(args, "top_k", 0),
        "top_p": getattr(args, "top_p", 1.0),
        "n_tasks": len(tasks),
    }
    input_hashes = {Path(args.fixture).name: file_digest(args.fixture)}
    if _resume(out, getattr(args, "resume", False), config, input_hashes):
        return 0
    packed = (
        _load_frozen_runtime(args)
        if getattr(args, "backend", "tiny") == "frozen" and eval_mode == "scientific"
        else None
    )
    gen_kw = {
        "weight_seed": getattr(args, "weight_seed", 0),
        "backend": getattr(args, "backend", "tiny"),
        "model_name": getattr(args, "model_name", None),
        "packed": packed,
        "max_new": config["max_new"],
        "temperature": getattr(args, "temperature", 1.0),
        "top_k": getattr(args, "top_k", 0),
        "top_p": getattr(args, "top_p", 1.0),
        "device": getattr(args, "device", None),
    }
    if eval_mode == "scientific":
        from .models.generate import generate_task_trace
        from .tasks.t1_config import validate_t1_prepare_config

        ops = getattr(args, "t1_ops", None)
        if ops:
            declared_n = len(tasks)
            if task.source_kind == "official":
                validate_t1_prepare_config({"ops": ops, "n_problems": declared_n, "mod": 23})
            else:
                config["t1_protocol_status"] = "fixture_pilot_n_problems_mismatch"
            config["t1_ops"] = list(ops)
            config["t1_n_problems"] = declared_n
        base_trace = generate_task_trace(task, seed=0, run_id="trace-base", **gen_kw)
        seed1_trace = generate_task_trace(task, seed=1, run_id="trace-t0p", **gen_kw)
        edit_trace = generate_task_trace(edit.task, seed=0, run_id="trace-edit", **gen_kw)
        traces = [base_trace, seed1_trace, edit_trace]
        if any(not t.events or t.metadata.get("parse_status") == "parse_failed" for t in traces):
            raise ValueError("scientific prepare: parse_failed (no events)")
        pair = _try_source_value_pair(task, premise_id, new_literal or "2")
        if pair:
            src_trace = generate_task_trace(pair["same_value_diff_source"].task, seed=0, run_id="trace-source", **gen_kw)
            if src_trace.events and src_trace.metadata.get("parse_status") != "parse_failed":
                traces.append(src_trace)
        observations = _observations(task, base_trace, edit_trace, edit, "stream:0", "prepare")
        for extra in _allowed_edits(task):
            extra_trace = generate_task_trace(extra.task, seed=0, run_id=f"trace-{extra.id}", **gen_kw)
            traces.append(extra_trace)
            observations.extend(_observations(task, base_trace, extra_trace, extra, "stream:0", f"prepare:{extra.id}"))
        if getattr(args, "sham_opportunities", 0):
            sham_trace = generate_task_trace(task, seed=2, run_id="trace-sham", **gen_kw)
            traces.append(sham_trace)
            for left, right in align_events(base_trace.events, sham_trace.events)["pairs"]:
                observations.append(
                    Observation(
                        observation_id=f"obs:sham:{left.node_id or left.identity.key()}",
                        reference_trace=base_trace.id,
                        comparison_trace=sham_trace.id,
                        edit_id="sham:no_edit",
                        premise_id=f"sham:{left.node_id or left.identity.entity_or_expression}",
                        event_pair=[left.node_id or left.identity.key(), right.node_id or right.identity.key()],
                        outcome=compare_pair(left, right),
                        raw_values=[left.value, right.value],
                        alignment_ref=left.identity.key(),
                        rng_pair="sham:0",
                        scan_state="observed_response",
                        base_group_id=task.base_group_id,
                        run_id="prepare-sham",
                        record_id=f"prepare-sham:{left.identity.key()}",
                        node_id=left.node_id,
                        task_id=task.task_id,
                    )
                )
    else:
        pair = _try_source_value_pair(task, premise_id, new_literal or "2")
        base_text = _trace_text(task)
        edited_text = _trace_text(edit.task)
        base_trace = _synthetic_trace(task, base_text, "trace-base", 0)
        edit_trace = _synthetic_trace(edit.task, edited_text, "trace-edit", 0)
        traces = [base_trace, edit_trace]
        observations = _observations(task, base_trace, edit_trace, edit, "stream:0", "prepare")
        if getattr(args, "sham_opportunities", 0):
            sham_trace = _synthetic_trace(task, base_text, "trace-sham", 1)
            traces.append(sham_trace)
            for left, right in align_events(base_trace.events, sham_trace.events)["pairs"]:
                observations.append(
                    Observation(
                        observation_id=f"obs:sham:{left.node_id or left.identity.key()}",
                        reference_trace=base_trace.id,
                        comparison_trace=sham_trace.id,
                        edit_id="sham:no_edit",
                        premise_id=f"sham:{left.node_id or left.identity.entity_or_expression}",
                        event_pair=[left.node_id or left.identity.key(), right.node_id or right.identity.key()],
                        outcome=compare_pair(left, right),
                        raw_values=[left.value, right.value],
                        alignment_ref=left.identity.key(),
                        rng_pair="sham:0",
                        scan_state="observed_response",
                        base_group_id=task.base_group_id,
                        run_id="prepare-sham",
                        record_id=f"prepare-sham:{left.identity.key()}",
                        node_id=left.node_id,
                        task_id=task.task_id,
                    )
                )
    extra_scan_edits = list(_allowed_edits(task))
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

            extra_base = generate_task_trace(extra_task, seed=0, run_id=f"trace-base:{idx}", **gen_kw)
            extra_edit_tr = generate_task_trace(extra_edit.task, seed=0, run_id=f"trace-edit:{idx}", **gen_kw)
        else:
            extra_base = _synthetic_trace(extra_task, _trace_text(extra_task), f"trace-base:{idx}", 0)
            extra_edit_tr = _synthetic_trace(extra_edit.task, _trace_text(extra_edit.task), f"trace-edit:{idx}", 0)
        traces.extend([extra_base, extra_edit_tr])
        observations.extend(_observations(extra_task, extra_base, extra_edit_tr, extra_edit, "stream:0", f"prepare:{idx}"))
        task_rows.extend([extra_task.to_dict(), extra_edit.task.to_dict()])
        extra_edit_rows.append(extra_edit.to_dict())
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
    sham_protocol = (
        {"name": "no_edit_matched", "opportunities": args.sham_opportunities}
        if getattr(args, "sham_opportunities", 0)
        else None
    )
    if sham_protocol:
        hits = [o.node_id for o in observations if (o.rng_pair or "").startswith("sham:") and o.outcome == "changed"]
        sham_protocol = {**sham_protocol, "hits": hits}
    anc = {}
    for item in tasks:
        if item.nodes:
            anc.update(ancestors(item))
        for premise in item.premises:
            if premise.kind not in {"placeholder", "spec"} and premise.premise_id:
                anc.setdefault(premise.premise_id, {premise.premise_id})
    labels = build_labels(observations, anc, sham_protocol=sham_protocol)
    for lab in labels:
        lab.run_id = "prepare"
        if not lab.base_group_id:
            lab.base_group_id = task.base_group_id
        label_task = lab.task_id or lab.base_group_id or task.task_id
        lab.record_id = f"prepare:{label_task}:{lab.event_id}:{lab.premise_id}"
    densities = event_density_sets(task, labels, sham_protocol)
    noise_pair = None
    if any(t.id == "trace-sham" for t in traces):
        noise_pair = (traces[0], next(t for t in traces if t.id == "trace-sham"))
    to_csp = preservation_to_csp(traces[0], edit_trace if eval_mode != "scientific" else next(t for t in traces if t.id == "trace-edit"), {premise_id}, noise_pair=noise_pair)
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "tasks.jsonl", task_rows)
    edit_rows = [edit.to_dict(), *extra_edit_rows]
    if pair:
        edit_rows.append(
            {
                "kind": "source_value_pair",
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
    write_jsonl(out / "edits.jsonl", edit_rows)
    write_jsonl(out / "splits.jsonl", split_rows)
    write_jsonl(out / "events.jsonl", [e.to_dict() for t in traces for e in t.events])
    write_jsonl(out / "review_export.jsonl", review_export([e for t in traces for e in t.events], task))
    write_jsonl(out / "traces.jsonl", [t.to_dict() for t in traces])
    write_jsonl(out / "observations.jsonl", [o.to_dict() for o in observations])
    write_jsonl(
        out / "labels.jsonl",
        [lab.to_dict() for lab in labels]
        + [{"densities": densities, "to_csp": to_csp, "note": "event-mean densities; sham hits are not mapped onto real premises"}],
    )
    write_run_spec(
        out,
        {
            "input_hashes": {Path(args.fixture).name: file_digest(args.fixture)},
            "source_kinds": {Path(args.fixture).name: task.source_kind},
            "config": {**config, "n_traces": len(traces)},
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
                "run_spec.json",
            )
        ],
        {"tasks": len(task_rows), "edits": len(edit_rows), "traces": len(traces), "observations": len(observations), "success": 1, "failure": 0},
    )
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
            frozen_layer = readout_layer_index(frozen_card["layers"])
            frozen_runtime = {
                "revision": frozen_card.get("revision"),
                "runtime_device": packed_model.get("device"),
                "dtype": packed_model.get("dtype"),
            }
        h_blocks, pre_s, pre_v, post, event_rows = [], [], [], [], []
        embed_blocks = []
        embed_keys = []
        meta = {}
        tasks_by_id = {item.task_id: item for item in tasks} if tasks else {task.task_id: task}
        for trace in traces:
            token_ids = list(trace.token_ids or [])
            offsets = list(trace.offsets or [])
            if not token_ids:
                from .models.tokenize import encode_text

                token_ids, offsets = encode_text(trace.text or "")
            owner = tasks_by_id.get(trace.task_id, task)
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
            )
            if eval_mode == "scientific" and (packed.get("h_position") != "pre_step" or packed["H"].shape[0] == 0):
                raise ValueError("scientific collect requires step-boundary events")
            h_blocks.append(packed["H"])
            for premise, vector in zip(owner.premises, packed["E"]):
                embed_blocks.append(np.asarray(vector, dtype=float))
                embed_keys.append((trace.task_id, premise.premise_id))
            pre_s.append(packed["H_pre_step"])
            pre_v.append(packed["H_pre_value"])
            post.append(packed["H_post_step"])
            for node_id, ident in zip(packed.get("event_ids") or [], packed.get("identity_keys") or packed.get("event_ids") or []):
                event_rows.append({"trace_id": trace.id, "node_id": node_id, "identity_key": ident, "event_id": ident, "task_id": trace.task_id})
            meta = packed
        hidden = np.vstack([b for b in h_blocks if b.size]) if any(b.size for b in h_blocks) else np.zeros((0, 1))
        if embed_blocks:
            grouped_embed = {}
            grouped_tasks = {}
            for key, vector in zip(embed_keys, embed_blocks):
                premise_id = key[1]
                grouped_embed.setdefault(premise_id, []).append(vector)
                grouped_tasks.setdefault(premise_id, set()).add(key[0])
            embed_ids = list(grouped_embed)
            embed = np.stack([np.nanmean(np.stack(grouped_embed[pid]), axis=0) for pid in embed_ids])
            write_jsonl(
                out / "premise_rows.jsonl",
                [
                    {
                        "index": index,
                        "premise_id": premise_id,
                        "task_ids": sorted(grouped_tasks[premise_id]),
                        "n_trace_rows": len(grouped_embed[premise_id]),
                        "pooling": "mean_across_trace_variants",
                    }
                    for index, premise_id in enumerate(embed_ids)
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
        source = meta["weight_source"]
        layer = meta["hidden_layer"]
        if event_rows:
            write_jsonl(out / "event_rows.jsonl", event_rows)
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
    if backend in {"tiny", "frozen"} and (out / "event_rows.jsonl").exists():
        extra.append(out / "event_rows.jsonl")
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
    _write_stage(
        out,
        "traces",
        shard_rows,
        extra_files=extra,
        counts={"traces": len(shard_rows), "success": 1, "failure": 0},
        in_dir=src,
        config={**collect_cfg, "weight_source": source, "hidden_layer": layer, **frozen_runtime},
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
    for item in tasks:
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
    labels = build_labels(observations, anc, sham_protocol=sham_protocol)
    for lab in labels:
        lab.run_id = "label"
        if not lab.base_group_id:
            lab.base_group_id = tasks[0].base_group_id if tasks else ""
        label_task = lab.task_id or lab.base_group_id or (tasks[0].task_id if tasks else "")
        lab.record_id = f"label:{label_task}:{lab.event_id}:{lab.premise_id}"
    dens = event_density_sets(tasks[0], labels, sham_protocol) if tasks else {"null_reason": "no_task"}
    rows = [lab.to_dict() for lab in labels] + [{"densities": dens}]
    _write_stage(out, "labels", rows, in_dir=src, config={"command": "label"})
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


def cmd_fit(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    fit_cfg = {"command": "fit", "split": args.split, "eval_mode": getattr(args, "eval_mode", "fixture")}
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
        require_persisted_roles(persisted, args.split, "probe fit", scientific=scientific, allow_mixed=scientific)
    arrays = read_npz(src / "features.npz")
    h = arrays.get("H", arrays[next(iter(arrays))])
    e = arrays.get("E", h)
    if h.ndim == 2 and h.size and not np.isfinite(h).all():
        if getattr(args, "eval_mode", "fixture") == "scientific":
            raise ValueError("scientific fit refuses NaN hidden rows")
        keep = np.isfinite(h).all(axis=1)
        h = h[keep]
    if getattr(args, "eval_mode", "fixture") == "scientific" and (not np.isfinite(e).all() or e.ndim != 2):
        raise ValueError("scientific fit refuses non-finite or malformed premise features")
    if h.ndim != 2 or e.ndim != 2 or h.shape[0] == 0 or e.shape[0] == 0:
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
    task_for_e = None
    if (labels_dir / "labels.jsonl").exists():
        labels = [row for row in read_jsonl(labels_dir / "labels.jsonl") if "behavior_label" in row or "task_label" in row]
        if persisted and getattr(args, "eval_mode", "fixture") == "scientific":
            allowed_ids = _split_member_ids(persisted, args.split)
            if allowed_ids:
                labels = [row for row in labels if not (row.get("task_id") or row.get("base_group_id")) or str(row.get("task_id") or row.get("base_group_id")) in allowed_ids]
        task_path = _find_tasks_jsonl(src, labels_dir)
        if task_path:
            task_for_e = Task.from_dict(read_jsonl(task_path)[0])
        elif labels:
            raise ValueError("fit requires tasks.jsonl so E columns follow task.premises, not label order")
        premise_rows_path = src / "premise_rows.jsonl"
        if premise_rows_path.exists():
            unique = [row.get("premise_id") for row in read_jsonl(premise_rows_path) if row.get("premise_id")]
        else:
            unique = _e_premise_ids(task_for_e, labels)
        for row in labels:
            if row.get("premise_id") not in unique:
                continue
            j = unique.index(row["premise_id"])
            if j >= e.shape[0]:
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
                ):
                    matched.append(i)
            if not matched:
                continue
            for i in matched:
                if row.get("task_label") in {0, 1, 0.0, 1.0}:
                    y_task[i, j] = float(row["task_label"])
                if row.get("behavior_label") in {0, 1, 0.0, 1.0}:
                    y_beh[i, j] = float(row["behavior_label"])
    if not np.isfinite(y_task).any() and not np.isfinite(y_beh).any():
        raise ValueError("fit refuses identity labels; provide known task/behavior labels")
    rank = min(64, h.shape[1], e.shape[1])
    rows = []
    for head, y in (("task", y_task), ("behavior", y_beh)):
        probe = BilinearProbe(h.shape[1], e.shape[1], rank=rank)
        probe.head_type = head
        fitted = probe.fit(h, e, y, split=args.split)
        rows.append({"head": head, **fitted})
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
    if np.isfinite(y_text).any():
        premise_text = {
            p.premise_id: p.text
            for p in (task_for_e.premises if task_for_e is not None else [])
            if getattr(p, "premise_id", None)
        }
        visible_prefixes = [prefix] * len(prefixes) if prefix else [""] * len(prefixes)
        visible_premises = [premise_text.get(pid, "") for pid in prefixes]
        text_fit = fit_text_predictor(visible_prefixes, y_text, premises=visible_premises)
        rows.append({"baseline": "text_predictor", **{k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in text_fit.items()}})
        rows.append({"baseline": "verbalizer", "tier": "supervised", "status": "trained", "visibility": "prospective", "target": "dependency_set"})
    elif scientific:
        rows.append({"baseline": "verbalizer", "status": "refused_not_section8", "reason": "no labeled dependency set"})
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
            n = min(scores.size, attention_labels.size)
            try:
                rows.append({"baseline": "attention_threshold", **fit_attention_threshold(scores[:n], attention_labels[:n], split="dev")})
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
            n = min(h.shape[0], labels.size)
            known = np.isfinite(labels[:n]) & np.isin(labels[:n], [0.0, 1.0])
            if known.sum() < 2 or np.unique(labels[:n][known]).size < 2:
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
    _write_stage(out, "probes", rows, in_dir=src, extra_dir=labels_dir if labels_dir != src else None, config=fit_cfg)
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
    rows = []
    for row in read_jsonl(src / "interventions.jsonl"):
        main = (row.get("relative") or {}).get("main_outcomes") or {}
        crand = (row.get("relative") or {}).get("crand_outcomes") or {}
        clayer = (row.get("relative") or {}).get("clayer_outcomes") or {}
        rows.append(
            {
                "problem_id": row.get("record_id") or row.get("run_id") or "item",
                "main_acc": main.get("task_correct") if main.get("task_correct") is not None else row.get("task_correct"),
                "crand_acc": crand.get("task_correct"),
                "clayer_acc": clayer.get("task_correct"),
                "baseline_acc": (row.get("relative") or {}).get("baseline_task_correct"),
                "invalid_rate": main.get("invalid") if main.get("invalid") is not None else row.get("invalid"),
                "nontarget": main.get("nontarget") if main.get("nontarget") is not None else row.get("nontarget"),
                "status": row.get("status"),
                "clayer_status": row.get("clayer_status"),
                "rescue_outcomes": (row.get("relative") or {}).get("rescue_outcomes"),
            }
        )
    return rows


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
    cal_cfg = {"command": "calibrate", "split": args.split, "alpha": alpha, "head": head_name, "eval_mode": getattr(args, "eval_mode", "fixture")}
    if _resume(out, getattr(args, "resume", False), cal_cfg):
        return 0
    require_split(args.split, ("calibration",), "calibration")
    if not getattr(args, "in_dir", None):
        raise ValueError("calibrate requires --in-dir")
    src = Path(args.in_dir)
    feat_dir = Path(args.features_dir) if getattr(args, "features_dir", None) else src
    labels_dir = Path(args.labels_dir) if getattr(args, "labels_dir", None) else src
    persisted = _persisted_splits(src, feat_dir, labels_dir)
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
                    "reason": f"no persisted {args.split} rows",
                }],
                in_dir=src,
                extra_dir=feat_dir if feat_dir != src else None,
                config=cal_cfg,
            )
            return 0
        require_persisted_roles(persisted, args.split, "calibration", scientific=scientific, allow_mixed=scientific)
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
        task_for_e = Task.from_dict(read_jsonl(task_path)[0]) if task_path else None
        task_anc = ancestors(task_for_e) if task_for_e and task_for_e.nodes else {}
        premise_rows_path = feat_dir / "premise_rows.jsonl"
        if premise_rows_path.exists():
            unique = [row.get("premise_id") for row in read_jsonl(premise_rows_path) if row.get("premise_id")]
        else:
            unique = _e_premise_ids(task_for_e, labs)
        arrays = read_npz(feat_dir / "features.npz")
        for row in probe_rows:
            probe = BilinearProbe.from_row(row)
            pred = probe.predict_matrix(arrays["H"], arrays["E"])
            head = row.get("head") or probe.head_type or "task"
            units: dict[str, list[float]] = {}
            for i in range(pred.shape[0]):
                event_row = event_nodes[i] if i < len(event_nodes) else {}
                event_id = event_row.get("identity_key") or event_row.get("event_id") or event_row.get("node_id")
                node_id = event_row.get("node_id") or event_id
                trace_task_id = event_row.get("task_id") or event_row.get("base_group_id") or "task"
                label_key = "task_label" if head == "task" else "behavior_label"
                truth_i = []
                known_i = False
                for j, pid in enumerate(unique):
                    hits = [
                        r
                        for r in labs
                        if r.get("premise_id") == pid
                        and (r.get("event_id") in {event_id, node_id, None} or event_id in str(r.get("event_id") or ""))
                        and (not r.get("task_id") or r.get("task_id") == trace_task_id)
                    ]
                    if not hits:
                        continue
                    if any(r.get(label_key) in {0, 1, 0.0, 1.0} for r in hits):
                        known_i = True
                    if any(r.get(label_key) == 1 for r in hits):
                        if head == "task" and pid not in set(task_anc.get(node_id, set())) | ({node_id} if node_id else set()):
                            continue
                        truth_i.append(j)
                if not known_i:
                    continue
                empty_i = not truth_i
                val = sequence_score(pred[i].tolist(), True, empty_i, nonconformity="one_minus_p", truth_indices=None if empty_i else [j for j in truth_i if j < pred.shape[1]])
                key = trace_task_id
                units.setdefault(key, []).append(0.0 if val is None else val)
            scores = [max(vals) for vals in units.values()] if units else None
            if scores is None:
                continue
            cal = _sanitize_cal(conformal_threshold(scores, alpha))
            outputs.append({"head": head, "scores": scores, "alpha": alpha, **cal, "unit": "problem", "n_problems": len(scores), "nonconformity": "one_minus_p"})
            status = "one_minus_p_Rsi_problem_units"
    if not outputs:
        if getattr(args, "eval_mode", "fixture") == "scientific":
            raise ValueError("scientific calibrate refuses loss or literal scores")
        outputs = [{"scores": None, "alpha": alpha, "q": None, "status": status, "infinity": False, "unit": "problem", "nonconformity": "one_minus_p"}]
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
        index[(str(row.get("node_id") or ""), row.get("trace_id"))] = i
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
            if not np.allclose(matrix[i], matrix[j]):
                return int(i), int(j), donor_key
    return None


def _expressible_donor(matrix: np.ndarray, event_rows: list[dict] | None = None, pair_meta: dict | None = None):
    sourced = _pair_source_value(matrix, event_rows or [], pair_meta)
    if sourced is not None:
        return sourced
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
        },
    ):
        return 0
    if not getattr(args, "in_dir", None):
        raise ValueError("intervene requires --in-dir")
    src = Path(args.in_dir)
    bank = StreamBank(0)
    rng = np.random.default_rng(int(bank.get("direction").integers(0, 2**31)))
    status = "donor_missing"
    main_norm = crand_norm = clayer_norm = None
    report = {}
    timing = "unexpressible"
    clayer_status = "dev_scores_missing"
    if src and (src / "features.npz").exists():
        arrays = read_npz(src / "features.npz")
        matrix = arrays.get("H", arrays[next(iter(arrays))])
        event_rows = read_jsonl(src / "event_rows.jsonl") if (src / "event_rows.jsonl").exists() else []
        pair_meta = _load_source_value_pair(src)
        pair = _expressible_donor(matrix, event_rows, pair_meta)
        if pair is not None:
            i_base, i_donor, donor_kind = pair
            base, donor = np.asarray(matrix[i_base], dtype=float), np.asarray(matrix[i_donor], dtype=float)
            rank = min(2, base.shape[-1])
            basis_seed = int(bank.get("direction").integers(0, 2**31))
            sample_seed = int(bank.get("sample").integers(0, 2**31))
            rng = np.random.default_rng(basis_seed)
            probe_rows = read_jsonl(src / "probes.jsonl") if (src / "probes.jsonl").exists() else []
            probe_u = next((np.asarray(r["U"], dtype=float) for r in probe_rows if r.get("head") == "behavior" and "U" in r), None)
            if probe_u is None:
                probe_u = next((np.asarray(r["U"], dtype=float) for r in probe_rows if "U" in r), None)
            if probe_u is not None:
                q, _ = np.linalg.qr(probe_u)
                basis = q[:, :rank]
                direction_status = "probe_direction"
            elif getattr(args, "eval_mode", "fixture") == "scientific":
                raise ValueError("scientific intervene requires a fitted probe direction; random basis is not evidence")
            else:
                basis = orthonormal_basis(base.shape[-1], rank, rng)
                direction_status = "random_direction_unfitted"
            main = apply_swap(base, donor, basis)
            main_norm = float(np.linalg.norm(main - base))
            cr = c_rand_delta(base, donor, rank, np.random.default_rng(int(bank.get("perturb").integers(0, 2**31))), target_norm=main_norm)
            dev_scores = getattr(args, "dev_layer_scores", None)
            if dev_scores:
                scores = {int(k): float(v) for k, v in dict(zip(range(len(dev_scores)), dev_scores)).items()}
                weak = select_weak_layer(scores)
                clayer_status = "dev_scores_present_pending_decode"
            else:
                weak = None
                clayer_status = "dev_scores_missing"
            layer_basis = orthonormal_basis(base.shape[-1], rank, np.random.default_rng(5 + (weak if weak is not None else 0)))
            cl = c_layer_delta(base, donor, layer_basis, main_norm)
            crand_norm = cr["actual_norm"]
            clayer_norm = cl["actual_norm"]
            status = "geometry_on_hidden"
            timing = "offline_hidden"
            labels_path = src / "labels.jsonl"
            if labels_path.exists() and matrix.shape[0] >= 2:
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
                    proj = inlp_remove(np.vstack([base, donor]), np.array([0.0, 1.0]))
                    inlp_status = "two_row_fallback"
            else:
                proj = inlp_remove(np.vstack([base, donor]), np.array([0.0, 1.0]))
                inlp_status = "two_row_fallback"
            ablated = base @ proj if proj.ndim == 2 else base
            removed = base - ablated
            rescued = rescue_controls(ablated, removed, -removed, rng)
            hook_meta = {
                "inlp_rank": int(np.linalg.matrix_rank(proj)),
                "donor_rows": [i_base, i_donor],
                "donor_kind": donor_kind,
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
                traces = read_jsonl(src / "traces.jsonl") if (src / "traces.jsonl").exists() else []
                ev = None
                prefix = ""
                gold = None
                donor_ans = None
                want = event_rows[i_base]["node_id"] if event_rows and i_base < len(event_rows) else None
                base_tid = event_rows[i_base]["trace_id"] if event_rows and i_base < len(event_rows) else None
                donor_tid = event_rows[i_donor]["trace_id"] if event_rows and i_donor < len(event_rows) else None
                base_row = next((t for t in traces if t.get("id") == base_tid), traces[0] if traces else {})
                donor_row = next((t for t in traces if t.get("id") == donor_tid), traces[1] if len(traces) > 1 else {})
                prefix = base_row.get("text") or ""
                spec = read_json(src / "run_spec.json") if (src / "run_spec.json").exists() else {}
                collect_cfg = spec.get("config") or {}
                model_kind = collect_cfg.get("model_kind") or collect_cfg.get("kind") or "qwen2"
                weight_seed = int(collect_cfg.get("weight_seed") or 0)
                gold = None
                if (src / "tasks.jsonl").exists():
                    gold = Task.from_dict(read_jsonl(src / "tasks.jsonl")[0]).answer_spec.value
                events = base_row.get("events") or []
                ev = next((e for e in events if e.get("node_id") == want), None) or next((e for e in events if e.get("start", 0) > 0), None)
                if ev:
                    prefix = prefix[: ev.get("start", len(prefix))]
                donor_event = None
                donor_events = donor_row.get("events") or []
                if want:
                    donor_event = next((e for e in donor_events if e.get("node_id") == want), None)
                donor_src = donor_event.get("value") if donor_event else donor_row.get("answer")
                base_event = ev.get("value") if ev else base_row.get("answer")
                pair_targets = set((pair_meta or {}).get("targets") or [])
                pair_nontargets = set((pair_meta or {}).get("nontargets") or [])
                ids = list(base_row.get("token_ids") or []) or _tiny_prefix_ids(prefix)
                if ev and base_row.get("offsets"):
                    cut = ev.get("start", len(prefix))
                    trimmed = []
                    for tok, (a, _b) in zip(ids, base_row.get("offsets") or []):
                        if a >= cut:
                            break
                        trimmed.append(tok)
                    ids = trimmed or ids[:1]
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
                    main_layer = int(collect_cfg.get("hidden_layer") or readout_layer_index(packed_runtime["card"]["layers"]))
                else:
                    main_layer = int(collect_cfg.get("hidden_layer") or readout_layer_index(3))
                hook_meta["hook_layer"] = main_layer
                aligned = ev is not None
                decode_kw = {
                    "weight_seed": weight_seed,
                    "event_aligned": aligned,
                    "seed": sample_seed,
                    "model": runtime_model,
                    "max_new": _resolved_max_new(args, 4, 32),
                }
                hooked = intervene_hidden_decode(
                    model_kind,
                    ids,
                    main_layer,
                    donor=donor,
                    basis_seed=basis_seed,
                    basis=basis,
                    mode="pi_z_swap",
                    **decode_kw,
                )
                hook_meta.update({"hook_once": hooked["hook"], "transform": hooked["transform"], "hook_timing": hooked.get("timing"), "token_changed": hooked["followed_donor"]})

                def _decode_text(decoded) -> str:
                    ids_out = decoded.get("generated_ids") or []
                    if tokenizer is not None:
                        return tokenizer.decode(ids_out, skip_special_tokens=True)
                    return decode_ids(ids_out)

                def _parse_nodes(text: str) -> dict[str, str]:
                    found = {}
                    for ev_row in events:
                        nid = ev_row.get("node_id")
                        if nid and nid in text:
                            val = extract_answer(text, "numeric")
                            if val is not None:
                                found[nid] = val
                    return found

                def _outcomes(decoded):
                    text = _decode_text(decoded)
                    ans = extract_answer(text, "numeric")
                    parsed = _parse_nodes(text)
                    equivalent = donor_src is not None and base_event is not None and donor_src == base_event
                    if pair_targets:
                        target = 1.0 if any(parsed.get(n) == donor_src for n in pair_targets) else 0.0
                    elif equivalent:
                        target = None
                    else:
                        target = 1.0 if donor_src is not None and ans == donor_src else 0.0
                    if pair_nontargets:
                        nontarget = 1.0 if all(parsed.get(n) == base_event for n in pair_nontargets if n in parsed) and parsed else 0.0
                    elif equivalent:
                        nontarget = None
                    else:
                        nontarget = 1.0 if gold is not None and ans == gold and ans != donor_src else 0.0
                    return {
                        "target": target,
                        "nontarget": nontarget,
                        "task_correct": 1.0 if gold is not None and ans == gold else (None if gold is None else 0.0),
                        "invalid": 1.0 if ans is None else 0.0,
                        "answer": ans,
                    }

                main_out = _outcomes(hooked)
                base_ans = extract_answer(_decode_text({"generated_ids": hooked.get("baseline_generated_ids") or []}), "numeric")
                g_int = 1.0 if donor_src is not None and main_out["answer"] == donor_src else 0.0
                g_base = 1.0 if donor_src is not None and base_ans == donor_src else 0.0
                hook_meta["ie_z"] = g_int - g_base
                hook_meta["ie_z_g"] = "target_follow"
                hook_meta["baseline_task_correct"] = None if gold is None or base_ans is None else float(base_ans == gold)
                crand_hooked = intervene_hidden_decode(model_kind, ids, main_layer, mode="add_delta", delta=cr["delta"], **decode_kw)
                crand_out = _outcomes(crand_hooked)
                hook_meta["crand_transform"] = crand_hooked["transform"]
                clayer_out = {"target": None, "nontarget": None, "task_correct": None, "invalid": None}
                if weak is not None and weak != main_layer:
                    layer_model = runtime_model if runtime_model is not None else build_tiny(model_kind)
                    weak_base = _hidden_at_layer(layer_model, ids, weak)
                    weak_donor_ids = list(donor_row.get("token_ids") or ids)
                    weak_donor = _hidden_at_layer(layer_model, weak_donor_ids[: len(ids)] or weak_donor_ids, weak)
                    weak_vec = weak_base[min(len(weak_base) - 1, max(len(ids) - 1, 0))]
                    weak_dvec = weak_donor[min(len(weak_donor) - 1, max(len(ids) - 1, 0))]
                    cl = c_layer_delta(weak_vec, weak_dvec, layer_basis, main_norm)
                    clayer_hooked = intervene_hidden_decode(model_kind, ids, weak, mode="add_delta", delta=cl["delta"], **decode_kw)
                    clayer_out = _outcomes(clayer_hooked)
                    hook_meta["clayer_token_changed"] = clayer_hooked["followed_donor"]
                    hook_meta["clayer_transform"] = clayer_hooked["transform"]
                    hook_meta["weak_layer"] = weak
                    clayer_status = "dev_weak_layer_decode"
                elif weak is not None:
                    clayer_status = "weak_layer_equals_main"
                inlp_hooked = intervene_hidden_decode(model_kind, ids, main_layer, mode="inlp", projector=proj, **decode_kw)
                hook_meta["inlp_token_changed"] = inlp_hooked["followed_donor"]
                hook_meta["inlp_transform"] = inlp_hooked["transform"]
                rescue_matched = intervene_hidden_decode(model_kind, ids, main_layer, mode="replace", delta=rescued["matched"], **decode_kw)
                rescue_error = intervene_hidden_decode(model_kind, ids, main_layer, mode="replace", delta=rescued["error_source"], **decode_kw)
                rescue_rand = intervene_hidden_decode(model_kind, ids, main_layer, mode="replace", delta=rescued["random"], **decode_kw)
                hook_meta["rescue_transform"] = rescue_matched["transform"]
                hook_meta["rescue_outcomes"] = _outcomes(rescue_matched)
                hook_meta["rescue_error_outcomes"] = _outcomes(rescue_error)
                hook_meta["rescue_random_outcomes"] = _outcomes(rescue_rand)
                rel = intervention_report(main_out, crand_out, clayer_out)
                report = {**hook_meta, **rel, "main_outcomes": main_out, "crand_outcomes": crand_out, "clayer_outcomes": clayer_out}
                if hooked.get("hook_fired"):
                    status = "prospective_decode"
            else:
                hook_meta["ie_z"] = ie_z(rescued["matched"], base)
                report = hook_meta
    _write_stage(
        out,
        "interventions",
        [
            {
                "main_norm": main_norm,
                "crand_norm": crand_norm,
                "clayer_norm": clayer_norm,
                "target": ((report or {}).get("main_outcomes") or {}).get("target"),
                "nontarget": ((report or {}).get("main_outcomes") or {}).get("nontarget"),
                "task_correct": ((report or {}).get("main_outcomes") or {}).get("task_correct"),
                "invalid": ((report or {}).get("main_outcomes") or {}).get("invalid"),
                "status": status,
                "clayer_status": clayer_status,
                "timing": timing,
                "relative": report,
            }
        ],
        in_dir=src,
        config={
            "command": "intervene",
            "backend": getattr(args, "backend", "tiny"),
            "eval_mode": getattr(args, "eval_mode", "fixture"),
            "model_name": getattr(args, "model_name", None),
            "device": getattr(args, "device", None),
        },
    )
    return 0


def cmd_repair(args: argparse.Namespace) -> int:
    out = Path(args.out_dir)
    if _resume(out, getattr(args, "resume", False), {"command": "repair"}):
        return 0
    if not getattr(args, "in_dir", None):
        raise ValueError("repair requires --in-dir")
    src = Path(args.in_dir)
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
        original = traces[0].get("token_ids") or original
        ev_slots = []
        for ev in traces[0].get("events") or []:
            nid = ev.get("node_id") or (ev.get("identity") or {}).get("entity_or_expression")
            if nid and nid not in ev_slots:
                ev_slots.append(nid)
        for nid in ev_slots:
            if nid not in slots:
                slots.append(nid)
    eval_mode = getattr(args, "eval_mode", "fixture")
    group = ""
    if src and (src / "traces.jsonl").exists():
        group = traces[0].get("base_group_id") or ""
    backend = getattr(args, "backend", "offline")
    execute = None
    if backend == "frozen":
        packed_runtime = _load_frozen_runtime(args)
        max_new = _resolved_max_new(args, 8, 32)

        def execute(mask, slots, original_tokens, new_prefix):
            return execute_repair_frozen(
                mask,
                slots,
                original_tokens,
                new_prefix,
                packed=packed_runtime,
                max_new=max_new,
            )

    elif eval_mode == "scientific" or backend == "tiny":
        execute = execute_repair_tiny
    if eval_mode == "scientific":
        recs = consecutive_repairs(args.mask, slots, original, prefix, k_max=5, execute=execute, run_id="repair", base_group_id=group)
    else:
        recs = [run_repair(args.mask, ["q"], original, new_prefix=prefix, execute=execute, run_id="repair", base_group_id=group, k=1)]
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
        length = np.array([r["length"] for r in table], dtype=float)
        op = np.array([r["op"] for r in table], dtype=float)
        rho = np.array([r["rho"] for r in table], dtype=float)
        y = np.array([r["y"] for r in table], dtype=float)
        held = np.array([r.get("held_out", False) for r in table], dtype=bool)
        groups = [str(r.get("problem_id") or r.get("base_group_id") or i) for i, r in enumerate(table)]
        ho = held if held.any() and not held.all() else None
        p1 = p1_incremental(length, op, rho, y, held_out=ho, groups=groups, rng=np.random.default_rng(0))
        if p1.get("delta_auc") is not None:
            status = "evaluated_descriptive"
    measurements = {
        "status": status,
        "transfer": xfer,
        "rho_S_excess": None if not dens else dens.get("rho_S_excess"),
        "null_reason": None if not dens else dens.get("null_reason"),
        "labels_present": bool(src and (src / "labels.jsonl").exists()),
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
        pass
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
                    appendix["probe_prf1"] = probe_prf1(pred, gold)
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
        "scientific_conclusion": None,
    }
    write_json(out / "report.json", report)
    _write_stage(out, "analysis", [{"week8": decision, "transfer": xfer, "p1": p1, "p2": p2, "p3": p3, "appendix": appendix}], extra_files=[out / "report.json"], in_dir=src, config={"command": "analyze"})
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
    prepare.add_argument("--resume", action="store_true")
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
    prepare.add_argument("--temperature", type=float, default=1.0)
    prepare.add_argument("--top-k", type=int, default=0)
    prepare.add_argument("--top-p", type=float, default=1.0)
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
        ),
    )
    c.set_defaults(func=cmd_collect)
    stage("label").set_defaults(func=cmd_label)
    f = stage("fit")
    f.add_argument("--split", default="probe_train")
    f.add_argument("--labels-dir")
    f.set_defaults(func=cmd_fit)
    cal = stage(
        "calibrate",
        lambda p: (
            p.add_argument("--split", default="calibration"),
            p.add_argument("--features-dir"),
            p.add_argument("--labels-dir"),
            p.add_argument("--alpha", type=float, default=0.4),
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
            p.add_argument("--dev-layer-scores", nargs="*", type=float),
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
            write_json(path / "failure.json", {"error": type(exc).__name__, "message": str(exc)})
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
            if not preserve:
                try:
                    write_manifest(path, [path / "failure.json"], {"success": 0, "failure": 1})
                except Exception:
                    pass
        raise


if __name__ == "__main__":
    raise SystemExit(main())
