#!/usr/bin/env python3
"""Server PR8: length pilot -> measurement smoke -> optionally full cohort.

Run from the source checkout; outputs and model assets stay in /mnt/mydata/wja.
The pilot/smoke groups are excluded from the formal cohort.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import os
import shutil
import subprocess
import sys
import time
from threading import Lock, local

from reasoning_diff import cli
from reasoning_diff.alignment_audit import alignment_audit
from reasoning_diff.events import ALIGNMENT_POLICY
from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, write_json, write_jsonl
from reasoning_diff.next_round import (intervention_coverage, measurement_report, parser_coverage,
                                       registered_pilot_edits, select_dev_layer, smoke_report)
from reasoning_diff.schema import Task, Trace
from reasoning_diff.quantity_steps import ESTIMAND, MATCHING_POLICY, PROTOCOL, is_controlled, trace_format
from reasoning_diff.splits import DEFAULT_FRACTIONS, split_for_task
from reasoning_diff.tasks.t1_official import load_igsm_snapshot

REPO = Path(__file__).resolve().parents[1]
SERVER = Path("/mnt/mydata/wja/reasoning-diff")


def cohorts(paths):
    """One train and one dev problem per op, selected before any generation."""
    tasks = [(p, load_igsm_snapshot(p)) for p in sorted(paths)]
    chosen = []
    ops = sorted({t.metadata["op"] for _, t in tasks})
    for op in ops:
        for role in ("probe_train", "dev"):
            candidates = [(p, t) for p, t in tasks if t.metadata["op"] == op and split_for_task(t, seed=0, fractions=DEFAULT_FRACTIONS) == role]
            if not candidates:
                raise ValueError(f"no {role} problem for op{op}; cannot build a disjoint smoke")
            chosen.append(candidates[0])
    groups = {t.base_group_id for _, t in chosen}
    return [p for p, _ in chosen], [p for p, t in tasks if t.base_group_id not in groups]


def limit_formal(paths, limit):
    """Preselect by difficulty and existing split, independently of model outputs."""
    if limit is None:
        return paths
    tasks = [(p, load_igsm_snapshot(p)) for p in paths]
    ops = sorted({t.metadata["op"] for _, t in tasks})
    if not ops or limit % len(ops) or limit // len(ops) < 4:
        raise ValueError("formal limit must allow at least four problems per op and be divisible by the number of ops")
    per_op = limit // len(ops)
    quotas = {"dev": max(1, round(per_op * 0.15)), "calibration": max(1, round(per_op * 0.10)),
              "test": max(1, round(per_op * 0.25))}
    quotas["probe_train"] = per_op - sum(quotas.values())
    selected = []
    for op in ops:
        for role, count in quotas.items():
            candidates = [(p, t) for p, t in tasks if t.metadata["op"] == op
                          and split_for_task(t, seed=0, fractions=DEFAULT_FRACTIONS) == role]
            candidates.sort(key=lambda item: digest({"selection": "pr8-budget-v1", "family": item[1].base_group_id}))
            if len(candidates) < count:
                raise ValueError(f"not enough op{op} {role} problems for the registered cohort")
            selected.extend(p for p, _ in candidates[:count])
    return sorted(selected)


def pilot_worker(args):
    """Resume base lengths or a registered small paired measurement pilot."""
    from reasoning_diff.models import generate
    from trace_batching import BatchDecoder
    opts = cli.build_parser().parse_args(["prepare", "--fixture", str(args.dataset), "--kind", "igsm",
                                         "--out-dir", str(args.out_root), "--premise-protocol", "sentence_graph",
                                         "--trajectory-protocol", getattr(args, "trajectory_protocol", "natural"),
                                         "--eval-mode", "scientific", "--backend", "frozen", "--model-name", args.model, "--device", "cuda"])
    tasks = cli._load_tasks(opts)
    paired = getattr(args, "mode", "pilot-worker") == "pair-pilot-worker"
    out = args.out_root
    out.mkdir(parents=True, exist_ok=True)
    spec = {"source": {p.relative_to(REPO).as_posix(): file_digest(p) for directory in ("src", "scripts") for p in sorted((REPO / directory).rglob("*.py"))},
            "tasks": [digest(t.to_dict()) for t in tasks], "model": args.model, "max_new": args.max_new, "seeds": [0, 1, 2],
            "batch_size": args.batch_size, "trajectory_protocol": getattr(args, "trajectory_protocol", "natural")}
    spec_name = "paired_pilot_spec.json" if paired else "pilot_spec.json"
    if paired and (not (out / "pilot_spec.json").exists() or read_json(out / "pilot_spec.json") != spec):
        raise ValueError("paired pilot base protocol mismatch; use a new output root")
    if (out / spec_name).exists() and read_json(out / spec_name) != spec:
        raise ValueError("pilot inputs/code changed; use a new output root")
    write_json(out / spec_name, spec)
    requests = [(index, task, seed, out / f"trace-{index}-seed{seed}.json") for index, task in enumerate(tasks) for seed in range(3)]
    base_requests = list(requests)
    edits = []
    if paired:
        if any(not path.exists() for _, _, _, path in base_requests):
            raise ValueError("paired pilot requires the completed base-only pilot")
        for index, task in enumerate(tasks):
            for edit in registered_pilot_edits(task):
                pid = edit.changed_premise_ids[0]
                edits.append((index, edit))
                requests.append((f"{index}:{pid}", edit.task, 0, out / f"paired-{index}-{pid}.json"))
    missing = [request for request in requests if not request[3].exists()]
    if missing:
        packed = cli._load_frozen_runtime(opts)
        decoder = BatchDecoder(args.batch_size)
        original_decode = generate.decode_loop
        thread_state = local()

        def decode(*values, **kwargs):
            result = decoder(*values, **kwargs)
            thread_state.execution = result["batch_execution"]
            return result

        def save(request):
            index, task, seed, path = request
            run_id = f"trace-pilot-edit:{index}" if "::" in task.task_id else f"trace-base:{index}:seed{seed}"
            trace = generate.generate_task_trace(task, seed=seed, run_id=run_id, backend="frozen",
                                                 model_name=args.model, packed=packed, device="cuda", max_new=args.max_new,
                                                 temperature=0.6, top_k=20, top_p=0.95, enable_thinking=True, allow_forced_target=False)
            trace.metadata["op"] = task.metadata.get("op")
            trace.metadata["execution"] = thread_state.execution
            write_json(path, trace.to_dict())

        generate.decode_loop = decode
        try:
            with ThreadPoolExecutor(max_workers=args.batch_size) as pool:
                for start in range(0, len(missing), args.batch_size):
                    list(pool.map(save, missing[start:start + args.batch_size]))
        finally:
            generate.decode_loop = original_decode
            decoder.close()
    rows = [read_json(path) for _, _, _, path in requests]
    write_jsonl(out / ("paired_traces.jsonl" if paired else "traces.jsonl"), rows)
    write_jsonl(out / "tasks.jsonl", [task.to_dict() for task in tasks])
    if paired:
        from itertools import permutations
        bases = {(index, seed): Trace.from_dict(read_json(path)) for index, _, seed, path in base_requests}
        observations = []
        scanned = {}
        for index, edit in edits:
            pid = edit.changed_premise_ids[0]
            edited = Trace.from_dict(read_json(out / f"paired-{index}-{pid}.json"))
            observations.extend(cli._observations(tasks[index], bases[index, 0], edited, edit, "stream:0", f"pilot:{index}:{pid}"))
            scanned.setdefault(tasks[index].task_id, []).append(pid)
        for index, task in enumerate(tasks):
            for left, right in permutations([bases[index, seed] for seed in range(3)], 2):
                observations.extend(cli._sham_observations(task, left, right, right.seed, f"pilot-noise:{index}"))
        # Only seed 0 is edited in this cheap screen; seeds 1/2 provide noise.
        references = [bases[index, 0].to_dict() for index in range(len(tasks))]
        report = measurement_report(references, [task.to_dict() for task in tasks], [o.to_dict() for o in observations], [], scanned)
        if any(is_controlled(task) for task in tasks):
            formats = {row["id"]: trace_format(row, task) for row, (_, task, _, _) in zip(rows, requests)}
            report["registered_step_formats"] = formats
            report["checks"]["registered_step_format"] = all(row["passed"] for row in formats.values())
            report["failures"] = [key for key, passed in report["checks"].items() if not passed]
            report["passed"] = not report["failures"]
        report["pilot_protocol"] = {"edit_seed": 0, "noise_seeds": [1, 2], "scanned_premises": scanned,
                                    "scope": "relevant_fact_and_two_distractors", "formal_evidence": False}
        if not any(is_controlled(task) for task in tasks):
            report["alignment_audit"] = alignment_audit(rows, [task.to_dict() for task in tasks],
                                                        [o.to_dict() for o in observations], report)
        write_jsonl(out / "paired_observations.jsonl", [o.to_dict() for o in observations])
        write_jsonl(out / "paired_tasks.jsonl", [task.to_dict() for task in tasks] + [edit.task.to_dict() for _, edit in edits])
        write_json(out / "paired_measurement.json", report)


def layer_sweep(stage, work, dataset, prep, labels, model, gpus, layers):
    """Keep one collection per GPU and overlap it with two CPU fit jobs."""
    with ThreadPoolExecutor(max_workers=2) as cpu_pool:
        label_job = cpu_pool.submit(stage, f"{work.name}-label", "label", "--in-dir", prep, "--out-dir", labels)

        def fit(layer):
            label_job.result()
            stage(f"{work.name}-fit-{layer}", "fit", "--in-dir", work / f"collect-layer{layer}",
                  "--labels-dir", labels, "--out-dir", work / f"fit-layer{layer}")

        def collect_lane(index, gpu):
            fits = []
            for layer in layers[index::len(gpus)]:
                stage(f"{work.name}-collect-{layer}", "collect", "--fixture", dataset, "--kind", "igsm", "--in-dir", prep,
                      "--out-dir", work / f"collect-layer{layer}", "--backend", "frozen", "--model-name", model,
                      "--device", "cuda", "--hidden-layer", layer, gpu=gpu)
                fits.append(cpu_pool.submit(fit, layer))
            return fits

        with ThreadPoolExecutor(max_workers=len(gpus)) as gpu_pool:
            lanes = [gpu_pool.submit(collect_lane, index, gpu) for index, gpu in enumerate(gpus)]
            fits = [job for lane in lanes for job in lane.result()]
        label_job.result()
        for job in fits:
            job.result()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("pilot", "smoke", "full", "pilot-worker", "pair-pilot-worker"), default="smoke")
    parser.add_argument("--dataset", type=Path, default=SERVER / "runs/pr7-200-20261004/inputs/igsm-pilot200")
    parser.add_argument("--model-root", type=Path, default=SERVER / "assets/models")
    parser.add_argument("--out-root", type=Path, default=SERVER / "runs/pr8-sentence-facts")
    parser.add_argument("--model", choices=("qwen3-8b", "r1-distill-qwen-7b"), default="qwen3-8b")
    parser.add_argument("--gpus", type=int, nargs="+", default=[2, 3, 6])
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--trajectory-protocol", choices=("natural", "quantity_steps"), default="natural")
    parser.add_argument("--max-new", type=int, default=32768)
    parser.add_argument("--formal-limit", type=int, help="Balanced exploratory subset; default uses all remaining problems")
    parser.add_argument("--time-budget-hours", type=float, help="Stop subprocesses at the persisted wall-clock deadline")
    args = parser.parse_args(argv)
    if args.mode in {"pilot-worker", "pair-pilot-worker"}:
        pilot_worker(args)
        return 0
    import fcntl
    root = args.out_root.resolve()
    if (not root.is_relative_to(SERVER) or not args.gpus or len(set(args.gpus)) != len(args.gpus) or args.max_new < 1 or args.batch_size < 1
            or (args.time_budget_hours is not None and args.time_budget_hours <= 0)):
        raise ValueError("invalid server output path, GPU list, batch size or token budget")
    root.mkdir(parents=True, exist_ok=True)
    lock = (root / "run.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    available = shutil.disk_usage(root).free
    quota = subprocess.run(["quota", "-w", "-u", os.environ.get("USER", "wja")], capture_output=True, text=True, check=True)
    filesystem = subprocess.check_output(["findmnt", "-n", "-o", "SOURCE", "-T", str(root)], text=True).strip()
    for line in quota.stdout.splitlines():
        fields = line.split()
        if fields and fields[0] == filesystem:
            used, _, hard = [int(v.rstrip("*")) for v in fields[1:4]]
            if hard:
                available = min(available, max(0, hard - used) * 1024)
    if available < 2 * 1024**3:
        raise ValueError("less than 2 GiB output space remains on the actual output filesystem/quota")
    for name in ("cache", "tmp", "logs"):
        (root / name).mkdir(exist_ok=True)
    env = {**os.environ, "PYTHONPATH": str(REPO / "src"), "PYTHONUNBUFFERED": "1", "RD_MODEL_ROOT": str(args.model_root),
           "RD_LOCAL_FILES_ONLY": "1", "HF_HUB_OFFLINE": "1", "HF_HOME": str(root / "cache"), "TMPDIR": str(root / "tmp"),
           "PYTHONDONTWRITEBYTECODE": "1", "CUDA_DEVICE_ORDER": "PCI_BUS_ID",
           "OMP_NUM_THREADS": "8", "OPENBLAS_NUM_THREADS": "8", "MKL_NUM_THREADS": "8", "NUMEXPR_NUM_THREADS": "8"}
    smoke, full = cohorts(args.dataset.glob("igsm-official-*.json"))
    full = limit_formal(full, args.formal_limit)
    protocol = {"premise_protocol": "sentence_graph_v1", "noise": "directed_base_seed_pairs_common_cells",
                "trajectory_protocol": PROTOCOL if args.trajectory_protocol == "quantity_steps" else "natural",
                "measurement_estimand": ESTIMAND if args.trajectory_protocol == "quantity_steps" else "natural_parsed_steps",
                "natural_prompt_policy": None if args.trajectory_protocol == "quantity_steps" else "single_pass_named_results_v1",
                "max_new": args.max_new, "context_policy": "budget_clipped_to_remaining_card_context",
                "seeds": [0, 1, 2], "temperature": 0.6, "top_k": 20, "top_p": 0.95,
                "matching_policy": MATCHING_POLICY if args.trajectory_protocol == "quantity_steps" else ALIGNMENT_POLICY, "coverage_threshold": 0.5,
                "measurement_checks": "overall_and_each_problem_and_op_before_collection",
                "paired_pilot": {"edit_seed": 0, "noise_seeds": [1, 2], "facts": "first_relevant_definition_and_two_distractors"},
                "batch_size": args.batch_size, "gpus": args.gpus, "model": args.model,
                "formal_limit": args.formal_limit, "cohort_status": "exploratory" if args.formal_limit is not None else "full_available_cohort",
                "formal_selection": "op_and_persisted_split_stratified_hash_v1" if args.formal_limit is not None else "all_non_smoke_families",
                "time_budget_hours": args.time_budget_hours,
                "execution": {"pilot_batched": True, "parallel_layer_collection": True, "cpu_jobs": 2,
                              "blas_threads_per_job": 8, "parallel_position_fits": True, "cached_fit_inputs": True,
                              "parallel_intervention_pairs": True},
                "model_root": str(args.model_root.resolve()),
                "smoke_inputs": {p.name: file_digest(p) for p in smoke}, "formal_inputs": {p.name: file_digest(p) for p in full},
                "source_hashes": {p.relative_to(REPO).as_posix(): file_digest(p) for directory in ("src", "scripts") for p in sorted((REPO / directory).rglob("*.py"))},
                "scientific_conclusion": None, "P3": "deferred_S_specific_ablation", "C4": "deferred_genuine_incremental_repair"}
    if (root / "protocol.json").exists() and read_json(root / "protocol.json") != protocol:
        raise ValueError("PR8 protocol changed; use a new output root to avoid stale checkpoints")
    write_json(root / "protocol.json", protocol)
    deadline = None
    if args.time_budget_hours is not None:
        budget_path = root / "execution_budget.json"
        budget = read_json(budget_path) if budget_path.exists() else {
            "started_at_epoch": time.time(), "seconds": args.time_budget_hours * 3600}
        write_json(budget_path, budget)
        deadline = budget["started_at_epoch"] + budget["seconds"]
    write_json(root / "pipeline.json", {"status": "running", "mode": args.mode, "scientific_conclusion": None})
    job_states = {}
    status_lock = Lock()

    def status(name, state, gpu, **fields):
        with status_lock:
            job_states[name] = {"status": state, "gpu": gpu, "updated_at": datetime.now(timezone.utc).isoformat(), **fields}
            write_json(root / "execution_progress.json", {"jobs": job_states})
            if state in {"failed", "budget_exhausted"}:
                write_json(root / "pipeline.json", {"status": state, "stage": name, **fields, "scientific_conclusion": None})

    def run(name, command, gpu=None):
        status(name, "running", gpu)
        with (root / "logs" / f"{name}.log").open("a") as handle:
            print(name, flush=True)
            try:
                timeout = max(0, deadline - time.time()) if deadline is not None else None
                if timeout == 0:
                    raise subprocess.TimeoutExpired(command, timeout=0)
                subprocess.run([str(x) for x in command], cwd=REPO,
                               env={**env, "CUDA_VISIBLE_DEVICES": str(gpu) if gpu is not None else ""},
                               stdout=handle, stderr=subprocess.STDOUT, check=True, timeout=timeout)
            except Exception as exc:
                status(name, "budget_exhausted" if isinstance(exc, subprocess.TimeoutExpired) else "failed", gpu, error=str(exc))
                raise
        status(name, "complete", gpu)

    def stage(name, command, *options, gpu=None):
        entry = [sys.executable, REPO / "scripts/fit_cached_inputs.py"] if command == "fit" else [sys.executable, "-m", "reasoning_diff"]
        run(name, [*entry, command, *options, "--eval-mode", "scientific", "--resume"], gpu)

    def shards(paths, name):
        result = []
        for index, gpu in enumerate(args.gpus):
            if not paths[index::len(args.gpus)]:
                continue
            dest = root / "inputs" / name / f"gpu{gpu}"
            dest.mkdir(parents=True, exist_ok=True)
            for p in paths[index::len(args.gpus)]:
                shutil.copy2(p, dest / p.name)
            result.append((gpu, dest))
        return result

    # A truncated 4096-token pilot cannot estimate the required tail length.
    # Use the actual registered budget on all four op strata before scanning.
    pilot_inputs = shards(smoke, "pilot")
    with ThreadPoolExecutor(max_workers=len(args.gpus)) as pool:
        jobs = [pool.submit(run, f"pilot-gpu{gpu}", [sys.executable, Path(__file__), "--mode", "pilot-worker", "--dataset", path,
                     "--out-root", root / f"pilot-gpu{gpu}", "--model", args.model, "--max-new", args.max_new,
                     "--batch-size", args.batch_size, "--trajectory-protocol", args.trajectory_protocol], gpu) for gpu, path in pilot_inputs]
        for job in jobs:
            job.result()
    pilot_traces = [t for gpu, _ in pilot_inputs for t in read_jsonl(root / f"pilot-gpu{gpu}/traces.jsonl")]
    pilot_tasks = None
    by_op = {}
    for trace in pilot_traces:
        op = str(trace["metadata"].get("op"))
        by_op.setdefault(op, []).append(trace)
    completions = {op: sum(t["status"] == "natural_complete" for t in values) / len(values) for op, values in by_op.items()}
    pilot_checks = {"completion_rate": sum(t["status"] == "natural_complete" for t in pilot_traces) / max(len(pilot_traces), 1) >= 0.5,
                    "exact_boundaries": all(t["metadata"].get("boundary_status") == "ok" for t in pilot_traces),
                    "thinking_events": all(any(e.get("event_region") == "thinking" and e.get("event_kind") != "restatement" for e in t["events"]) for t in pilot_traces)}
    pilot_checks["completion_each_op"] = bool(completions) and all(rate >= 0.5 for rate in completions.values())
    if args.trajectory_protocol == "quantity_steps":
        pilot_tasks = [task for gpu, _ in pilot_inputs for task in read_jsonl(root / f"pilot-gpu{gpu}/tasks.jsonl")]
        owners = {t["task_id"]: Task.from_dict(t) for t in pilot_tasks}
        # Trace IDs are worker-local; preserve every shard's result, including failures.
        formats = [{"task_id": t["task_id"], "trace_id": t["id"], "seed": t["seed"],
                    **trace_format(t, owners[t["task_id"]])} for t in pilot_traces]
        write_json(root / "registered_step_formats.json", formats)
        pilot_checks["registered_step_format"] = bool(formats) and all(row["passed"] for row in formats)
    write_json(root / "length_pilot.json", {"checks": pilot_checks, "passed": all(pilot_checks.values()),
               "n_traces": len(pilot_traces), "completion_by_op": completions,
               "generated_lengths": [t["metadata"]["generated_tokens"] for t in pilot_traces],
               "right_censored": sum(t["status"] == "natural_truncated" for t in pilot_traces), "scientific_conclusion": None})
    if not all(pilot_checks.values()):
        write_json(root / "pipeline.json", {"status": "failed", "stage": "length_pilot", "error": "length/parser pilot failed",
                   "scientific_conclusion": None})
        raise RuntimeError("length/parser pilot failed; inspect length_pilot.json and pilot traces before spending on scans")
    if pilot_tasks is None:
        pilot_tasks = [task for gpu, _ in pilot_inputs for task in read_jsonl(root / f"pilot-gpu{gpu}/tasks.jsonl")]
    parser_rows = parser_coverage(pilot_traces, pilot_tasks)
    write_json(root / "parser_coverage.json", {"trajectories": parser_rows, "step_recall": "requires_annotated_steps"})
    by_problem = {}
    for row in parser_rows:
        by_problem.setdefault(row["problem_id"], []).append(row)
    if not by_problem or any(sum(r["variable_coverage"] or 0 for r in rows) / len(rows) < 0.5
                             or sum(r["target_present"] for r in rows) / len(rows) < 0.5 for rows in by_problem.values()):
        write_json(root / "pipeline.json", {"status": "failed", "stage": "parser_coverage", "scientific_conclusion": None})
        raise RuntimeError("parser coverage pilot failed; full premise scans have not started")
    with ThreadPoolExecutor(max_workers=len(args.gpus)) as pool:
        jobs = [pool.submit(run, f"paired-pilot-gpu{gpu}", [sys.executable, Path(__file__), "--mode", "pair-pilot-worker",
                "--dataset", path, "--out-root", root / f"pilot-gpu{gpu}", "--model", args.model,
                "--max-new", args.max_new, "--batch-size", args.batch_size,
                "--trajectory-protocol", args.trajectory_protocol], gpu) for gpu, path in pilot_inputs]
        for job in jobs:
            job.result()
    paired_reports = [read_json(root / f"pilot-gpu{gpu}/paired_measurement.json") for gpu, _ in pilot_inputs]
    write_json(root / "paired_pilot.json", {"passed": all(r["passed"] for r in paired_reports), "shards": paired_reports,
                                          "scientific_conclusion": None})
    if not all(r["passed"] for r in paired_reports):
        write_json(root / "pipeline.json", {"status": "failed", "stage": "paired_pilot", "scientific_conclusion": None})
        raise RuntimeError("paired measurement pilot failed; full premise scans have not started")
    if args.mode == "pilot":
        write_json(root / "pipeline.json", {"status": "complete", "mode": "pilot", "stage": "paired_pilot",
                   "full_scan_started": False, "scientific_conclusion": None})
        return 0

    def pipeline(paths, name):
        work = root / name
        inputs = shards(paths, name)
        with ThreadPoolExecutor(max_workers=len(args.gpus)) as pool:
            jobs = [pool.submit(run, f"{name}-prepare-gpu{gpu}", [sys.executable, REPO / "scripts/prepare_batched.py", "--batch-size", args.batch_size,
                    "prepare", "--fixture", path, "--out-dir", work / f"prepare-gpu{gpu}", "--kind", "igsm", "--backend", "frozen",
                    "--model-name", args.model, "--device", "cuda", "--max-new", args.max_new, "--eval-mode", "scientific",
                    "--premise-protocol", "sentence_graph", "--trajectory-protocol", args.trajectory_protocol,
                    "--noise-reference", "base_pairs", "--n-seeds", "3", "--behavior-repeats", "3",
                    "--split-fractions", *DEFAULT_FRACTIONS, "--checkpoint-traces", "--resume"], gpu) for gpu, path in inputs]
            for job in jobs:
                job.result()
        prep = work / "prepare"
        run(f"{name}-merge", [sys.executable, REPO / "scripts/merge_pr6_shards.py", "--out-dir", prep, *[work / f"prepare-gpu{g}" for g, _ in inputs]])
        labels = work / "label"
        measurements = measurement_report(read_jsonl(prep / "traces.jsonl"), read_jsonl(prep / "tasks.jsonl"),
                                          read_jsonl(prep / "observations.jsonl"), read_jsonl(prep / "splits.jsonl"))
        write_json(work / "measurement_report.json", measurements)
        write_jsonl(work / "p1_table.jsonl", measurements["trajectories"])
        if not measurements["passed"]:
            raise RuntimeError(f"{name} measurement failed before feature collection: {measurements['failures']}")
        layers = [0, 12, 24, 35] if args.model == "qwen3-8b" else [0, 9, 18, 27]
        layer_sweep(stage, work, args.dataset, prep, labels, args.model, args.gpus, layers)
        scores = []
        for layer in layers:
            fit = work / f"fit-layer{layer}"
            row = next((r for r in read_jsonl(fit / "probes.jsonl") if r.get("head") == "behavior" and "U" in r), {})
            scores.append(((row.get("metrics") or {}).get("dev") or {}).get("auc"))
        layer = select_dev_layer(layers, scores)
        write_json(work / "layer_selection.json", {"layer": layer, "layers": layers, "dev_behavior_auc": scores, "tie_rule": "lowest_layer"})
        collect, fit = work / f"collect-layer{layer}", work / "fit"
        finite = [(l, s) for l, s in zip(layers, scores) if s is not None]
        if len(finite) < 2:
            raise RuntimeError("fewer than two usable dev layers; weak-layer control unavailable")
        fit_options = ["--in-dir", collect, "--labels-dir", labels, "--dev-layer-ids", *[l for l, _ in finite],
                       "--dev-layer-scores", *[s for _, s in finite]]
        with ThreadPoolExecutor(max_workers=2) as pool:
            jobs = [pool.submit(stage, f"{name}-fit-{position}", "fit", *fit_options, "--out-dir", fit / position,
                                "--position", position) for position in ("pre_step", "pre_value", "post_step")]
            for job in jobs:
                job.result()
        stage(f"{name}-fit-all", "fit", *fit_options, "--out-dir", fit, "--position", "all")
        report = smoke_report(read_jsonl(prep / "traces.jsonl"), read_jsonl(prep / "tasks.jsonl"), read_jsonl(prep / "observations.jsonl"),
                              read_jsonl(collect / "event_rows.jsonl"), read_jsonl(fit / "probes.jsonl"))
        p1 = read_jsonl(fit / "p1_table.jsonl")
        expected = {r["trace_id"]: (r["rho"], r["support_cells"], r["eligible_cells"]) for r in measurements["trajectories"]}
        actual = {r["trace_id"]: (r["rho"], r["support_cells"], r["eligible_cells"]) for r in p1}
        report["checks"].update(measurements["checks"])
        report["checks"]["trajectory_p1"] = len(p1) == report["base_traces"] and len(actual) == len(p1) and actual == expected
        report["matched_cell_coverage"] = measurements["overall"]["matched_cell_coverage"]
        report["p1_estimability"] = measurements["p1_estimability"]
        report["failures"] = [k for k, v in report["checks"].items() if not v]
        report["passed"] = not report["failures"]
        write_json(work / "smoke_report.json", report)
        if not report["passed"]:
            raise RuntimeError(f"{name} feature/probe checks failed: {report['failures']}")
        if name == "full":
            stage("full-calibrate", "calibrate", "--in-dir", fit, "--features-dir", collect, "--labels-dir", labels, "--out-dir", work / "calibration")
        with ThreadPoolExecutor(max_workers=len(args.gpus)) as pool:
            jobs = [pool.submit(stage, f"{name}-intervene-gpu{gpu}", "intervene", "--in-dir", prep, "--features-dir", collect,
                    "--probes-dir", fit / "pre_step", "--labels-dir", labels, "--out-dir", work / f"intervention-gpu{gpu}",
                    "--backend", "frozen", "--model-name", args.model, "--device", "cuda", "--max-new", args.max_new,
                    "--all-source-pairs", "--pair-split", "dev" if name == "smoke" else "test",
                    "--pair-shard", index, len(args.gpus), gpu=gpu) for index, gpu in enumerate(args.gpus)]
            for job in jobs:
                job.result()
        intervention_paths = [work / f"intervention-gpu{gpu}/interventions.jsonl" for gpu in args.gpus]
        intervention = [row for path in intervention_paths for row in read_jsonl(path)]
        cli._write_stage(work / "intervention", "interventions", intervention, in_dir=collect,
                         config={"command": "merge_intervention_shards", "n_shards": len(args.gpus),
                                 "shard_hashes": {str(path.relative_to(root)): file_digest(path) for path in intervention_paths}})
        coverage = intervention_coverage(intervention)
        causal_ready = all(coverage["usable_by_kind"].get(kind, 0) > 0
                           for kind in ("same_value_diff_source", "same_source_diff_value"))
        write_json(work / "intervention_coverage.json", coverage)
        report["checks"]["causal_decode"] = causal_ready
        report["failures"] = [k for k, v in report["checks"].items() if not v]
        report["passed"] = all(report["checks"].values())
        write_json(work / "smoke_report.json", report)
        analysis = work / "analysis-input"
        analysis.mkdir(exist_ok=True)
        for source, filenames in ((prep, ["tasks.jsonl", "traces.jsonl", "splits.jsonl"]), (fit, ["p1_table.jsonl"]), (labels, ["labels.jsonl"])):
            for filename in filenames:
                shutil.copy2(source / filename, analysis / filename)
        shutil.copy2(work / "measurement_report.json", analysis / "measurement_report.json")
        shutil.copy2(work / "intervention/interventions.jsonl", analysis / "interventions.jsonl")
        stage(f"{name}-analyze", "analyze", "--in-dir", analysis, "--out-dir", work / "analysis")
        if not causal_ready:
            raise RuntimeError(f"no usable donor/decode for both source-pair kinds in {name}; inspect intervention_coverage.json")

    try:
        pipeline(smoke, "smoke")
        if args.mode == "full":
            pipeline(full, "full")
        write_json(root / "pipeline.json", {"status": "complete", "mode": args.mode, "scientific_conclusion": None})
    except Exception as exc:
        write_json(root / "pipeline.json", {"status": "budget_exhausted" if isinstance(exc, subprocess.TimeoutExpired) else "failed",
                   "error": str(exc), "scientific_conclusion": None})
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
