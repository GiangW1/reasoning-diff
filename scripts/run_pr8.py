#!/usr/bin/env python3
"""Server PR8: length pilot -> measurement smoke -> optionally full cohort.

Run from the source checkout; outputs and model assets stay in /mnt/mydata/wja.
The pilot/smoke groups are excluded from the formal cohort.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import shutil
import subprocess
import sys

from reasoning_diff import cli
from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, write_json, write_jsonl
from reasoning_diff.next_round import intervention_coverage, select_dev_layer, smoke_report
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


def pilot_worker(args):
    """Cheap base-only length/parser check before paying for perturbations."""
    from reasoning_diff.models.generate import generate_task_trace
    opts = cli.build_parser().parse_args(["prepare", "--fixture", str(args.dataset), "--kind", "igsm",
                                         "--out-dir", str(args.out_root), "--premise-protocol", "sentence_graph",
                                         "--eval-mode", "scientific", "--backend", "frozen", "--model-name", args.model, "--device", "cuda"])
    tasks = cli._load_tasks(opts)
    out = args.out_root
    out.mkdir(parents=True, exist_ok=True)
    spec = {"source": {p.relative_to(REPO).as_posix(): file_digest(p) for p in sorted((REPO / "src").rglob("*.py"))},
            "tasks": [digest(t.to_dict()) for t in tasks], "model": args.model, "max_new": args.max_new, "seeds": [0, 1, 2]}
    if (out / "pilot_spec.json").exists() and read_json(out / "pilot_spec.json") != spec:
        raise ValueError("pilot inputs/code changed; use a new output root")
    write_json(out / "pilot_spec.json", spec)
    packed = None
    traces = []
    for index, task in enumerate(tasks):
        for seed in range(3):
            path = out / f"trace-{index}-seed{seed}.json"
            if path.exists():
                traces.append(read_json(path))
                continue
            if packed is None:
                packed = cli._load_frozen_runtime(opts)
            trace = generate_task_trace(task, seed=seed, run_id=f"trace-base:{index}:seed{seed}", backend="frozen",
                                        model_name=args.model, packed=packed, device="cuda", max_new=args.max_new,
                                        temperature=0.6, top_k=20, top_p=0.95, enable_thinking=True, allow_forced_target=False)
            trace.metadata["op"] = task.metadata.get("op")
            write_json(path, trace.to_dict())
            traces.append(trace.to_dict())
    write_jsonl(out / "traces.jsonl", traces)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("smoke", "full", "pilot-worker"), default="smoke")
    parser.add_argument("--dataset", type=Path, default=SERVER / "runs/pr7-200-20261004/inputs/igsm-pilot200")
    parser.add_argument("--model-root", type=Path, default=SERVER / "assets/models")
    parser.add_argument("--out-root", type=Path, default=SERVER / "runs/pr8-sentence-facts")
    parser.add_argument("--model", choices=("qwen3-8b", "r1-distill-qwen-7b"), default="qwen3-8b")
    parser.add_argument("--gpus", type=int, nargs="+", default=[2, 3, 6])
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-new", type=int, default=32768)
    args = parser.parse_args(argv)
    if args.mode == "pilot-worker":
        pilot_worker(args)
        return 0
    import fcntl
    root = args.out_root.resolve()
    if not root.is_relative_to(SERVER) or not args.gpus or len(set(args.gpus)) != len(args.gpus) or args.max_new < 1 or args.batch_size < 1:
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
           "OMP_NUM_THREADS": "8", "OPENBLAS_NUM_THREADS": "8", "MKL_NUM_THREADS": "8"}
    smoke, full = cohorts(args.dataset.glob("igsm-official-*.json"))
    protocol = {"premise_protocol": "sentence_graph_v1", "noise": "directed_base_seed_pairs_common_cells",
                "max_new": args.max_new, "context_policy": "budget_clipped_to_remaining_card_context",
                "seeds": [0, 1, 2], "temperature": 0.6, "top_k": 20, "top_p": 0.95,
                "batch_size": args.batch_size, "gpus": args.gpus, "model": args.model,
                "model_root": str(args.model_root.resolve()),
                "smoke_inputs": {p.name: file_digest(p) for p in smoke}, "formal_inputs": {p.name: file_digest(p) for p in full},
                "source_hashes": {p.relative_to(REPO).as_posix(): file_digest(p) for directory in ("src", "scripts") for p in sorted((REPO / directory).rglob("*.py"))},
                "scientific_conclusion": None, "P3": "deferred_S_specific_ablation", "C4": "deferred_genuine_incremental_repair"}
    if (root / "protocol.json").exists() and read_json(root / "protocol.json") != protocol:
        raise ValueError("PR8 protocol changed; use a new output root to avoid stale checkpoints")
    write_json(root / "protocol.json", protocol)

    def run(name, command, gpu=None):
        with (root / "logs" / f"{name}.log").open("a") as handle:
            print(name, flush=True)
            subprocess.run([str(x) for x in command], cwd=REPO, env={**env, **({"CUDA_VISIBLE_DEVICES": str(gpu)} if gpu is not None else {})},
                           stdout=handle, stderr=subprocess.STDOUT, check=True)

    def stage(name, command, *options, gpu=None):
        run(name, [sys.executable, "-m", "reasoning_diff", command, *options, "--eval-mode", "scientific", "--resume"], gpu)

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
                     "--out-root", root / f"pilot-gpu{gpu}", "--model", args.model, "--max-new", args.max_new], gpu) for gpu, path in pilot_inputs]
        for job in jobs:
            job.result()
    pilot_traces = [t for gpu, _ in pilot_inputs for t in read_jsonl(root / f"pilot-gpu{gpu}/traces.jsonl")]
    by_op = {}
    for trace in pilot_traces:
        op = str(trace["metadata"].get("op"))
        by_op.setdefault(op, []).append(trace)
    completions = {op: sum(t["status"] == "natural_complete" for t in values) / len(values) for op, values in by_op.items()}
    pilot_checks = {"completion_rate": sum(t["status"] == "natural_complete" for t in pilot_traces) / max(len(pilot_traces), 1) >= 0.5,
                    "exact_boundaries": all(t["metadata"].get("boundary_status") == "ok" for t in pilot_traces),
                    "thinking_events": all(any(e.get("event_region") == "thinking" and e.get("event_kind") != "restatement" for e in t["events"]) for t in pilot_traces)}
    pilot_checks["completion_each_op"] = bool(completions) and all(rate >= 0.5 for rate in completions.values())
    write_json(root / "length_pilot.json", {"checks": pilot_checks, "passed": all(pilot_checks.values()),
               "n_traces": len(pilot_traces), "completion_by_op": completions,
               "generated_lengths": [t["metadata"]["generated_tokens"] for t in pilot_traces],
               "right_censored": sum(t["status"] == "natural_truncated" for t in pilot_traces), "scientific_conclusion": None})
    if not all(pilot_checks.values()):
        raise RuntimeError("length/parser pilot failed; inspect length_pilot.json and pilot traces before spending on scans")

    def pipeline(paths, name):
        work = root / name
        inputs = shards(paths, name)
        with ThreadPoolExecutor(max_workers=len(args.gpus)) as pool:
            jobs = [pool.submit(run, f"{name}-prepare-gpu{gpu}", [sys.executable, REPO / "scripts/prepare_batched.py", "--batch-size", args.batch_size,
                    "prepare", "--fixture", path, "--out-dir", work / f"prepare-gpu{gpu}", "--kind", "igsm", "--backend", "frozen",
                    "--model-name", args.model, "--device", "cuda", "--max-new", args.max_new, "--eval-mode", "scientific",
                    "--premise-protocol", "sentence_graph", "--noise-reference", "base_pairs", "--n-seeds", "3", "--behavior-repeats", "3",
                    "--split-fractions", *DEFAULT_FRACTIONS, "--checkpoint-traces", "--resume"], gpu) for gpu, path in inputs]
            for job in jobs:
                job.result()
        prep = work / "prepare"
        run(f"{name}-merge", [sys.executable, REPO / "scripts/merge_pr6_shards.py", "--out-dir", prep, *[work / f"prepare-gpu{g}" for g, _ in inputs]])
        labels = work / "label"
        stage(f"{name}-label", "label", "--in-dir", prep, "--out-dir", labels)
        layers = [0, 12, 24, 35] if args.model == "qwen3-8b" else [0, 9, 18, 27]
        scores = []
        for layer in layers:
            collect, fit = work / f"collect-layer{layer}", work / f"fit-layer{layer}"
            stage(f"{name}-collect-{layer}", "collect", "--fixture", args.dataset, "--kind", "igsm", "--in-dir", prep, "--out-dir", collect,
                  "--backend", "frozen", "--model-name", args.model, "--device", "cuda", "--hidden-layer", layer, gpu=args.gpus[0])
            stage(f"{name}-fit-{layer}", "fit", "--in-dir", collect, "--labels-dir", labels, "--out-dir", fit)
            row = next((r for r in read_jsonl(fit / "probes.jsonl") if r.get("head") == "behavior" and "U" in r), {})
            scores.append(((row.get("metrics") or {}).get("dev") or {}).get("auc"))
        layer = select_dev_layer(layers, scores)
        write_json(work / "layer_selection.json", {"layer": layer, "layers": layers, "dev_behavior_auc": scores, "tie_rule": "lowest_layer"})
        collect, fit = work / f"collect-layer{layer}", work / "fit"
        finite = [(l, s) for l, s in zip(layers, scores) if s is not None]
        if len(finite) < 2:
            raise RuntimeError("fewer than two usable dev layers; weak-layer control unavailable")
        stage(f"{name}-fit-all", "fit", "--in-dir", collect, "--labels-dir", labels, "--out-dir", fit, "--position", "all",
              "--dev-layer-ids", *[l for l, _ in finite], "--dev-layer-scores", *[s for _, s in finite])
        report = smoke_report(read_jsonl(prep / "traces.jsonl"), read_jsonl(prep / "tasks.jsonl"), read_jsonl(prep / "observations.jsonl"),
                              read_jsonl(collect / "event_rows.jsonl"), read_jsonl(fit / "probes.jsonl"))
        p1 = read_jsonl(fit / "p1_table.jsonl")
        report["checks"]["trajectory_p1"] = len(p1) == report["base_traces"] and len({r["trace_id"] for r in p1}) == len(p1) and any(r["rho"] is not None for r in p1)
        observed = sum(r["support_cells"] for r in p1)
        possible = sum(r["eligible_cells"] for r in p1)
        report["matched_cell_coverage"] = observed / possible if possible else 0
        report["checks"]["matched_cell_coverage"] = possible > 0 and observed / possible >= 0.5
        report["failures"] = [k for k, v in report["checks"].items() if not v]
        report["passed"] = not report["failures"]
        write_json(work / "smoke_report.json", report)
        if name == "smoke" and not report["passed"]:
            raise RuntimeError("measurement smoke failed; full generation has not started")
        if name == "full":
            stage("full-calibrate", "calibrate", "--in-dir", fit, "--features-dir", collect, "--labels-dir", labels, "--out-dir", work / "calibration")
        stage(f"{name}-intervene", "intervene", "--in-dir", prep, "--features-dir", collect, "--probes-dir", fit / "pre_step",
              "--labels-dir", labels, "--out-dir", work / "intervention", "--backend", "frozen", "--model-name", args.model,
              "--device", "cuda", "--max-new", args.max_new, "--all-source-pairs", "--pair-split", "dev" if name == "smoke" else "test", gpu=args.gpus[0])
        intervention = read_jsonl(work / "intervention/interventions.jsonl")
        coverage = intervention_coverage(intervention)
        usable = coverage["usable_main_contrasts"]
        write_json(work / "intervention_coverage.json", coverage)
        if name == "smoke" and not usable:
            report["checks"]["causal_decode"] = False
            report["passed"] = False
            report["failures"].append("causal_decode")
            write_json(work / "smoke_report.json", report)
            raise RuntimeError("no usable donor/decode in smoke; full generation has not started")
        report["checks"]["causal_decode"] = usable > 0
        report["passed"] = all(report["checks"].values())
        write_json(work / "smoke_report.json", report)
        analysis = work / "analysis-input"
        analysis.mkdir(exist_ok=True)
        for source, filenames in ((prep, ["tasks.jsonl", "traces.jsonl", "splits.jsonl"]), (fit, ["p1_table.jsonl"]), (labels, ["labels.jsonl"])):
            for filename in filenames:
                shutil.copy2(source / filename, analysis / filename)
        stage(f"{name}-analyze", "analyze", "--in-dir", analysis, "--out-dir", work / "analysis")

    try:
        pipeline(smoke, "smoke")
        if args.mode == "full":
            pipeline(full, "full")
        write_json(root / "pipeline.json", {"status": "complete", "mode": args.mode, "scientific_conclusion": None})
    except Exception as exc:
        write_json(root / "pipeline.json", {"status": "failed", "error": str(exc), "scientific_conclusion": None})
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
