#!/usr/bin/env python3
"""Plan or run a separate shared-prefix response assay on saved natural traces."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import subprocess
import sys
import time

from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, write_json, write_jsonl
from reasoning_diff.models.generate import task_prompt
from reasoning_diff.schema import Task
from reasoning_diff.shared_prefix import (ESTIMAND, PROTOCOL, SAMPLING, SEEDS, make_plan, requests_for,
                                         run_request, summarize)

REPO = Path(__file__).resolve().parents[1]
SERVER = Path("/mnt/mydata/wja/reasoning-diff")


def load_source(source):
    manifest = read_json(source / "manifest.json")
    hashes = {name: file_digest(source / name) for name in ("tasks.jsonl", "traces.jsonl")}
    if any(manifest["file_hashes"].get(name) != value for name, value in hashes.items()):
        raise ValueError("source manifest mismatch")
    plan = make_plan(read_jsonl(source / "traces.jsonl"), read_jsonl(source / "tasks.jsonl"))
    if hashes != {name: file_digest(source / name) for name in hashes}:
        raise ValueError("source changed during planning")
    return plan, hashes


def saved_result(root, request, fingerprint):
    path = root / "responses" / f"{request['id']}.json"
    if not path.exists():
        return None
    envelope = read_json(path)
    result = envelope["result"]
    if (envelope.get("fingerprint") != fingerprint or envelope.get("result_hash") != digest(result)
            or result.get("request") != request):
        raise ValueError(f"response checkpoint mismatch: {request['id']}")
    return result


def worker(args):
    from reasoning_diff.models.adapters import load_frozen
    from trace_batching import BatchDecoder

    root = args.out_root
    envelope = read_json(root / "protocol.json")
    spec, fingerprint = envelope["spec"], envelope["fingerprint"]
    if digest(spec) != fingerprint:
        raise ValueError("protocol fingerprint mismatch")
    if not 0 <= args.shard_index < len(spec["gpus"]):
        raise ValueError("invalid worker shard")
    plan = read_json(root / "plan.json")
    if digest(plan) != spec["plan_hash"]:
        raise ValueError("plan checkpoint mismatch")
    if spec["source_hashes"] != source_hashes():
        raise ValueError("worker source differs from registered protocol")
    requests = requests_for(plan, args.phase)[args.shard_index::len(spec["gpus"])]
    pending = [r for r in requests if saved_result(root, r, fingerprint) is None]
    if not pending:
        return 0
    anchors = {a["id"]: a for a in plan["anchors"]}
    tasks = {t["task_id"]: Task.from_dict(t) for t in plan["tasks"]}
    variants = {v["id"]: Task.from_dict(v["task"]) for v in plan["variants"]}
    packed = load_frozen(spec["model"], device="cuda", local_files_only=True)
    decoder = BatchDecoder(spec["batch_size"])
    try:
        def execute(request):
            anchor = anchors[request["anchor_id"]]
            print("start", request["id"], flush=True)
            result = run_request(request, anchor, tasks[anchor["task_id"]], variants[request["variant_id"]],
                                 packed, spec["max_new"], decoder)
            write_json(root / "responses" / f"{request['id']}.json",
                       {"fingerprint": fingerprint, "result_hash": digest(result), "result": result})
            print(request["id"], result["status"], flush=True)
        with ThreadPoolExecutor(max_workers=spec["batch_size"]) as pool:
            for start in range(0, len(pending), spec["batch_size"]):
                list(pool.map(execute, pending[start:start + spec["batch_size"]]))
    finally:
        decoder.close()
    return 0


def source_hashes():
    return {p.relative_to(REPO).as_posix(): file_digest(p) for folder in ("src", "scripts")
            for p in sorted((REPO / folder).rglob("*.py"))}


def collect_report(root, plan, phase, fingerprint):
    requests = requests_for(plan, phase)
    results = [row for request in requests if (row := saved_result(root, request, fingerprint)) is not None]
    report = summarize(plan, requests, results, phase)
    write_json(root / f"{phase}_report.json", report)
    write_jsonl(root / f"{phase}_contrasts.jsonl", report["contrasts"])
    return report


def run_workers(root, phase, gpus, env, deadline):
    """Stop sibling GPU workers on the first failure or persisted deadline."""
    children, logs = [], []
    try:
        for index, gpu in enumerate(gpus):
            command = [sys.executable, str(Path(__file__).resolve()), "--mode", "worker", "--out-root", str(root),
                       "--phase", phase, "--shard-index", str(index)]
            if deadline is not None and time.time() >= deadline:
                raise subprocess.TimeoutExpired(command, 0)
            handle = (root / "logs" / f"{phase}-gpu{gpu}.log").open("a")
            logs.append(handle)
            children.append(subprocess.Popen(command, cwd=REPO, env={**env, "CUDA_VISIBLE_DEVICES": str(gpu)},
                                             stdout=handle, stderr=subprocess.STDOUT))
        while True:
            codes = [child.poll() for child in children]
            for child, code in zip(children, codes):
                if code not in (None, 0):
                    raise subprocess.CalledProcessError(code, child.args)
            if all(code == 0 for code in codes):
                return
            if deadline is not None and time.time() >= deadline:
                raise subprocess.TimeoutExpired("shared-prefix workers", 0)
            time.sleep(0.2)
    finally:
        for child in children:
            if child.poll() is None:
                child.terminate()
        for child in children:
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
        for handle in logs:
            handle.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("plan", "pilot", "scan", "worker"), default="plan")
    parser.add_argument("--in-dir", type=Path, help="Immutable saved natural prepare directory")
    parser.add_argument("--out-root", type=Path, required=True)
    parser.add_argument("--model", default="qwen3-8b", choices=("qwen3-8b", "r1-distill-qwen-7b"))
    parser.add_argument("--model-root", type=Path, default=SERVER / "assets/models")
    parser.add_argument("--gpus", type=int, nargs="+", default=[2, 3, 6])
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-new", type=int, default=256)
    parser.add_argument("--time-budget-hours", type=float)
    parser.add_argument("--phase", choices=("pilot", "scan"), default="pilot")
    parser.add_argument("--shard-index", type=int, default=0)
    args = parser.parse_args(argv)
    if args.mode == "worker":
        return worker(args)
    if (args.in_dir is None or args.max_new < 1 or args.batch_size < 1 or not args.gpus
            or min(args.gpus) < 0 or len(set(args.gpus)) != len(args.gpus)
            or (args.time_budget_hours is not None and args.time_budget_hours <= 0)):
        raise ValueError("invalid source, GPU list, batch size or budget")
    root, source = args.out_root.resolve(), args.in_dir.resolve()
    if root == source or root.is_relative_to(source) or source.is_relative_to(root):
        raise ValueError("output must be a separate directory outside the source tree")
    if args.mode != "plan" and not root.is_relative_to(SERVER):
        raise ValueError("server runs must write under /mnt/mydata/wja/reasoning-diff")
    root.mkdir(parents=True, exist_ok=True)
    lock = None
    if args.mode != "plan":
        import fcntl
        lock = (root / "run.lock").open("a")
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        plan, hashes = load_source(source)
        spec = {"protocol": PROTOCOL, "estimand": ESTIMAND, "source": str(source), "input_hashes": hashes,
                "plan_hash": digest(plan), "source_hashes": source_hashes(), "model": args.model,
                "model_root": str(args.model_root.resolve()), "max_new": args.max_new, "batch_size": args.batch_size,
                "gpus": args.gpus, "seeds": list(SEEDS), "sampling": SAMPLING, "time_budget_hours": args.time_budget_hours,
                "cut": "exact_pre_value_char_prefix_retokenized_without_target_value",
                "noise": "same_history_fresh_baselines_other_two_seeds_on_common_support",
                "coverage_threshold": 0.5, "downstream_old_probe_and_P1": "not_applicable"}
        fingerprint = digest(spec)
        spec_path = root / "protocol.json"
        if spec_path.exists() and read_json(spec_path) != {"fingerprint": fingerprint, "spec": spec}:
            raise ValueError("shared-prefix protocol changed; use a new output directory")
        if not spec_path.exists() and any(p.name != "run.lock" for p in root.iterdir()):
            raise ValueError("output is nonempty without a shared-prefix protocol")
        write_json(spec_path, {"fingerprint": fingerprint, "spec": spec})
        write_json(root / "plan.json", plan)
        phase_requests = {phase: requests_for(plan, phase) for phase in ("pilot", "scan")}
        counts = {phase: len(requests) for phase, requests in phase_requests.items()}
        anchors = {a["id"]: a for a in plan["anchors"]}
        question_lengths = {t["task_id"]: len(task_prompt(Task.from_dict(t))) for t in plan["tasks"]}
        variant_lengths = {v["id"]: len(task_prompt(Task.from_dict(v["task"]))) for v in plan["variants"]}
        def prefix_chars(request):
            anchor = anchors[request["anchor_id"]]
            return (len(anchor["rendered_prompt"]) + len(anchor["history"]) - question_lengths[anchor["task_id"]]
                    + variant_lengths[request["variant_id"]])
        write_json(root / "plan_summary.json", {"protocol": PROTOCOL, "estimand": ESTIMAND, "n_sources": len(plan["sources"]),
                   "n_problems": len({s['problem_id'] for s in plan['sources']}), "n_anchors": len(plan["anchors"]),
                   "n_usable_anchors": sum(a["source_usable"] for a in plan["anchors"]),
                   "requests": counts, "max_decode_tokens": {phase: n * args.max_new for phase, n in counts.items()},
                   "total_prefix_characters": {phase: sum(map(prefix_chars, requests)) for phase, requests in phase_requests.items()},
                   "max_prefix_characters": max(map(prefix_chars, phase_requests["scan"]), default=0),
                   "prefill_tokens": "not_measured_by_CPU_plan; long_prefixes_are_prefilled_for_each_request",
                   "pilot_selection": "first_parsed_thinking_assignment_per_source; three_registered_facts_seed0",
                   "source_anchor_coverage": plan["sources"], "model_generation_run": False, "scientific_conclusion": None})
        if args.mode == "plan":
            print(counts, flush=True)
            return 0
        for name in ("logs", "cache", "tmp"):
            (root / name).mkdir(exist_ok=True)
        deadline = None
        if args.time_budget_hours is not None:
            budget_path = root / "execution_budget.json"
            budget = read_json(budget_path) if budget_path.exists() else {"started_at": time.time(), "seconds": args.time_budget_hours * 3600}
            write_json(budget_path, budget)
            deadline = budget["started_at"] + budget["seconds"]
        env = {**os.environ, "PYTHONPATH": str(REPO / "src"), "RD_MODEL_ROOT": spec["model_root"],
               "RD_LOCAL_FILES_ONLY": "1", "HF_HUB_OFFLINE": "1", "HF_HOME": str(root / "cache"),
               "TMPDIR": str(root / "tmp"), "PYTHONDONTWRITEBYTECODE": "1", "CUDA_DEVICE_ORDER": "PCI_BUS_ID"}
        for phase in ("pilot", "scan") if args.mode == "scan" else ("pilot",):
            write_json(root / "pipeline.json", {"protocol": PROTOCOL, "status": "running", "phase": phase, "scientific_conclusion": None})
            try:
                if any(saved_result(root, r, fingerprint) is None for r in phase_requests[phase]):
                    run_workers(root, phase, args.gpus, env, deadline)
                report = collect_report(root, plan, phase, fingerprint)
            except Exception as exc:
                report_error = None
                try:
                    collect_report(root, plan, phase, fingerprint)
                except Exception as audit_exc:
                    report_error = str(audit_exc)
                write_json(root / "pipeline.json", {"protocol": PROTOCOL, "phase": phase,
                           "status": "budget_exhausted" if isinstance(exc, subprocess.TimeoutExpired) else "failed",
                           "error": str(exc), "report_error": report_error, "scientific_conclusion": None})
                raise
            if not report["passed"]:
                write_json(root / "pipeline.json", {"protocol": PROTOCOL, "status": "failed", "phase": phase,
                           "checks": report["checks"], "scientific_conclusion": None})
                raise RuntimeError(f"shared-prefix {phase} failed; inspect {phase}_report.json before further generation")
        write_json(root / "pipeline.json", {"protocol": PROTOCOL, "status": "complete", "phase": phase, "scientific_conclusion": None})
        return 0
    finally:
        if lock is not None:
            lock.close()


if __name__ == "__main__":
    raise SystemExit(main())
