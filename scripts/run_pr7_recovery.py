#!/usr/bin/env python3
"""Resume the 200-problem experiment under the user's shared data directory."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import fcntl
import importlib.metadata
import math
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time

from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, write_json
from reasoning_diff.models.adapters import card
from reasoning_diff.next_round import select_dev_layer


REPO = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", required=True, type=Path)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--model-root", required=True, type=Path)
    parser.add_argument("--model", default="qwen3-8b")
    parser.add_argument("--gpus", nargs="+", type=int, default=[2, 3, 6])
    parser.add_argument("--batch-size", type=int, default=1)
    args = parser.parse_args()
    root = args.out_root.resolve()
    if not root.is_relative_to(Path("/mnt/mydata/wja")):
        raise ValueError("experiment outputs must be under /mnt/mydata/wja")
    if len(args.gpus) != len(set(args.gpus)):
        raise ValueError("GPU IDs must be unique")
    if args.batch_size < 1:
        raise ValueError("batch size must be positive")
    root.mkdir(parents=True, exist_ok=True)
    filesystem = subprocess.check_output(["findmnt", "-n", "-o", "SOURCE", "-T", str(root)], text=True).strip()
    lock = (root / "controller.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    logs = root / "logs"
    logs.mkdir(exist_ok=True)
    for name in ("tmp", "cache"):
        (root / name).mkdir(exist_ok=True)
    env = {
        **os.environ, "PYTHONPATH": str(REPO / "src"),
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1",
        "RD_MODEL_ROOT": str(args.model_root), "RD_LOCAL_FILES_ONLY": "1",
        "HF_HUB_OFFLINE": "1", "HF_HOME": str(root / "cache"),
        "TMPDIR": str(root / "tmp"), "OMP_NUM_THREADS": "8", "MKL_NUM_THREADS": "8",
    }
    info = card(args.model)
    model_dir = args.model_root / info["id"].split("/")[-1]
    work = root / args.model
    work.mkdir(exist_ok=True)

    def state(status, **fields):
        write_json(root / "pipeline.json", {
            "status": status, "model": args.model, "gpus": args.gpus, "batch_size": args.batch_size,
            "updated_at": datetime.now(timezone.utc).isoformat(), **fields,
        })
        print(status, fields, flush=True)

    def space_check(required=512 * 1024**2):
        available = shutil.disk_usage(root).free
        quota = subprocess.run(["quota", "-w", "-u", "wja"], capture_output=True, text=True, check=True)
        for line in quota.stdout.splitlines():
            parts = line.split()
            if parts and parts[0] == filesystem:
                used, _soft, hard = [int(value.rstrip("*")) for value in parts[1:4]]
                if hard:
                    available = min(available, max(hard - used, 0) * 1024)
        if available < required:
            raise RuntimeError(f"insufficient output disk space: need {required} bytes, available {available} bytes")

    def wait_gpu(gpu):
        while True:
            result = subprocess.run([
                "nvidia-smi", "-i", str(gpu), "--query-gpu=memory.free", "--format=csv,noheader,nounits",
            ], capture_output=True, text=True, check=True)
            if int(result.stdout.strip()) >= 25 * 1024:
                return
            state("waiting_for_gpu", gpu=gpu)
            time.sleep(45)

    def launch(name, command, gpu=None):
        space_check()
        if gpu is not None:
            wait_gpu(gpu)
        command = [str(value) for value in command]
        state("running", stage=name, command=command)
        print(shlex.join(command), flush=True)
        with (logs / f"{name}.log").open("a") as handle:
            return subprocess.Popen(command, cwd=REPO, env={**env, **({"CUDA_VISIBLE_DEVICES": str(gpu)} if gpu is not None else {})},
                                    stdout=handle, stderr=subprocess.STDOUT)

    def run(name, command, gpu=None):
        process = launch(name, command, gpu)
        if process.wait() != 0:
            raise RuntimeError(f"{name} failed; see {logs / (name + '.log')}")

    def stage(name, *options, gpu=None):
        run(name, [sys.executable, "-m", "reasoning_diff", *options, "--eval-mode", "scientific", "--resume"], gpu)

    try:
        space_check()
        dataset = sorted(args.dataset.glob("igsm-official-*.json"))
        if len(dataset) != 200:
            raise ValueError(f"expected 200 official snapshots, found {len(dataset)}")
        protocol = {
            "model": info, "gpus": args.gpus, "n_problems": len(dataset), "max_new": 4096,
            "temperature": 0.6, "top_k": 20, "top_p": 0.95, "thinking": True,
            "generation_seeds": [0, 1, 2], "behavior_repeats": 3, "sham_opportunities": 3,
            "split_fractions": [0.4, 0.15, 0.1, 0.1, 0.1, 0.15],
            "sweep_layers": [0, 12, 24, 35] if args.model == "qwen3-8b" else [0, 9, 18, 27],
            "source_hashes": {p.relative_to(REPO).as_posix(): file_digest(p) for p in sorted((REPO / "src").rglob("*.py"))},
            "script_hashes": {name: file_digest(REPO / "scripts" / name) for name in
                              ("merge_pr6_shards.py", "run_pr7_recovery.py", "prepare_batched.py", "trace_batching.py")},
            "data_hashes": {p.name: file_digest(p) for p in dataset},
            "packages": {name: importlib.metadata.version(name) for name in ("torch", "transformers", "numpy")},
        }
        protocol_path = work / "protocol.json"
        if protocol_path.exists():
            previous = read_json(protocol_path)
            if digest({k: v for k, v in previous.items() if k != "script_hashes"}) != digest({k: v for k, v in protocol.items() if k != "script_hashes"}):
                raise ValueError("experiment protocol changed; use a new output root")
            if digest(previous) != digest(protocol):
                write_json(work / "protocol.before-batching.json", previous)
                write_json(work / "scheduling_change.json", {
                    "updated_at": datetime.now(timezone.utc).isoformat(), "batch_size": args.batch_size,
                    "previous_script_hashes": previous.get("script_hashes"), "script_hashes": protocol["script_hashes"],
                    "measurement_parameters_unchanged": True,
                })
        write_json(protocol_path, protocol)
        snapshot = work / "code"
        for relative, expected in {
            **protocol["source_hashes"],
            **{f"scripts/{name}": value for name, value in protocol["script_hashes"].items()},
        }.items():
            target = snapshot / relative
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO / relative, target)
            if file_digest(target) != expected:
                if relative.startswith("scripts/"):
                    shutil.copy2(target, target.with_suffix(target.suffix + ".before-batching"))
                    shutil.copy2(REPO / relative, target)
                else:
                    raise ValueError(f"code snapshot mismatch: {relative}")
        env["PYTHONPATH"] = str(snapshot / "src")
        while not (model_dir / "verified.json").exists():
            state("waiting_for_model", model_dir=str(model_dir))
            time.sleep(45)
        verified = read_json(model_dir / "verified.json")
        if verified["model_id"] != info["id"] or verified["revision"] != info["revision"]:
            raise ValueError("verified model revision mismatch")

        workers = []
        prepares = []
        for index, gpu in enumerate(args.gpus):
            fixture = root / "inputs" / f"shard-gpu{gpu}"
            fixture.mkdir(parents=True, exist_ok=True)
            for source in dataset[index::len(args.gpus)]:
                target = fixture / source.name
                if target.exists() and file_digest(target) != file_digest(source):
                    raise ValueError(f"shard input changed: {target}")
                if not target.exists():
                    shutil.copy2(source, target)
            prep = work / f"prepare-gpu{gpu}"
            prepares.append(prep)
            entrypoint = [sys.executable, "-m", "reasoning_diff"] if args.batch_size == 1 else [
                sys.executable, snapshot / "scripts/prepare_batched.py", "--batch-size", str(args.batch_size),
            ]
            command = [*entrypoint, "prepare", "--fixture", fixture,
                       "--out-dir", prep, "--eval-mode", "scientific", "--kind", "igsm", "--backend", "frozen",
                       "--model-name", args.model, "--device", "cuda", "--max-new", "4096",
                       "--temperature", "0.6", "--top-k", "20", "--top-p", "0.95",
                       "--split-fractions", "0.4", "0.15", "0.1", "0.1", "0.1", "0.15",
                       "--n-seeds", "3", "--behavior-repeats", "3", "--sham-opportunities", "3",
                       "--checkpoint-traces", "--resume"]
            workers.append(launch(f"{args.model}-prepare-gpu{gpu}", command, gpu))
        state("generating", shard_outputs=[str(path) for path in prepares])
        failures = [gpu for gpu, process in zip(args.gpus, workers, strict=True) if process.wait() != 0]
        if failures:
            raise RuntimeError(f"prepare workers failed on GPUs {failures}; saved traces can be resumed")

        merged = work / "prepare-combined"
        run(f"{args.model}-merge", [sys.executable, snapshot / "scripts/merge_pr6_shards.py", "--out-dir", merged, *prepares])
        traces = read_jsonl(merged / "traces.jsonl")
        base_traces = [row for row in traces if "trace-base" in row["id"] or "trace-t0p" in row["id"]]
        write_json(work / "generation_summary.json", {
            "n_problems": len(dataset), "n_traces": len(traces),
            "statuses": dict(Counter(row["status"] for row in traces)),
            "execution_backends": dict(Counter((row.get("metadata") or {}).get("execution", {}).get("backend", "serial_decode") for row in traces)),
            "base_generations": len(base_traces), "base_correct": sum(row.get("correct") is True for row in base_traces),
            "base_accuracy_itt": sum(row.get("correct") is True for row in base_traces) / max(len(base_traces), 1),
            "scientific_conclusion": None,
        })
        labels = work / "label"
        stage(f"{args.model}-label", "label", "--in-dir", merged, "--out-dir", labels)
        stage(f"{args.model}-generation-analysis", "analyze", "--in-dir", merged, "--out-dir", work / "generation-analysis")
        gpu = args.gpus[0]
        layers = protocol["sweep_layers"]
        scores = []
        # Four event-position matrices plus premise embeddings and JSON sidecars.
        event_count = sum(len(row.get("events") or []) for row in traces)
        estimated = max(512 * 1024**2, event_count * info["hidden_size"] * 20 + event_count * 50000)
        for layer in layers:
            collect = work / f"collect-layer{layer}"
            fit = work / f"fit-layer{layer}"
            space_check(estimated)
            stage(f"{args.model}-collect-layer{layer}", "collect", "--fixture", args.dataset, "--kind", "igsm",
                  "--in-dir", merged, "--out-dir", collect, "--backend", "frozen", "--model-name", args.model,
                  "--device", "cuda", "--hidden-layer", layer, gpu=gpu)
            stage(f"{args.model}-fit-layer{layer}", "fit", "--in-dir", collect, "--out-dir", fit,
                  "--labels-dir", labels, "--split", "probe_train")
            behavior = next((row for row in read_jsonl(fit / "probes.jsonl") if row.get("head") == "behavior"), {})
            score = ((behavior.get("metrics") or {}).get("dev") or {}).get("auc")
            scores.append(float(score) if score is not None and math.isfinite(float(score)) else None)
        curve = [] if any(score is None for score in scores) else ["--dev-layer-scores", *scores, "--dev-layer-ids", *layers]
        write_json(work / "layer_sweep.json", {"layer_ids": layers, "dev_behavior_auc": scores,
                   "status": "ready" if curve else "insufficient_dev_labels"})
        selected_layer = select_dev_layer(layers, scores)
        collect = work / f"collect-layer{selected_layer}"
        fit = work / "fit"
        stage(f"{args.model}-fit-all", "fit", "--in-dir", collect, "--out-dir", fit,
              "--labels-dir", labels, "--split", "probe_train", "--position", "all", *curve)
        stage(f"{args.model}-calibrate", "calibrate", "--in-dir", fit, "--out-dir", work / "calibration",
              "--features-dir", collect, "--labels-dir", labels, "--split", "calibration")
        stage(f"{args.model}-intervene", "intervene", "--in-dir", merged, "--out-dir", work / "intervention",
              "--features-dir", collect, "--probes-dir", fit / "pre_step", "--labels-dir", labels,
              "--backend", "frozen", "--model-name", args.model, "--device", "cuda", "--max-new", "4096", gpu=gpu)
        stage(f"{args.model}-repair", "repair", "--in-dir", merged, "--out-dir", work / "repair", "--mask", "all",
              "--backend", "frozen", "--model-name", args.model, "--device", "cuda", "--max-new", "4096", gpu=gpu)
        analysis_input = work / "analysis-input"
        analysis_input.mkdir(exist_ok=True)
        sources = {}
        for source, names in [
            (merged, ["tasks.jsonl", "traces.jsonl", "splits.jsonl"]), (labels, ["labels.jsonl"]),
            (fit, ["p1_table.jsonl"]), (work / "intervention", ["interventions.jsonl"]),
            (work / "repair", ["repairs.jsonl"]),
        ]:
            for name in names:
                shutil.copy2(source / name, analysis_input / name)
                sources[name] = {"source": str(source / name), "sha256": file_digest(source / name)}
        write_json(analysis_input / "provenance.json", sources)
        stage(f"{args.model}-analyze", "analyze", "--in-dir", analysis_input, "--out-dir", work / "analysis")
        state("complete", report=str(work / "analysis/report.json"))
    except BaseException as exc:
        state("failed", error=f"{type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    main()
