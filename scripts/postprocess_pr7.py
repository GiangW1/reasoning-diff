#!/usr/bin/env python3
"""Run independent PR7 postprocessing stages in parallel after generation."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

from reasoning_diff import cli
from reasoning_diff.io import file_digest, read_json, read_jsonl, write_json
from reasoning_diff.next_round import select_dev_layer


@dataclass
class Job:
    name: str
    command: list
    dependencies: tuple[str, ...] = ()
    gpu: bool = False


def run_jobs(jobs, launch, gpu_ids, cpu_limit=2, update=lambda _states: None, gpu_ready=lambda _gpu: True, pause=time.sleep):
    pending = {job.name: job for job in jobs}
    if len(pending) != len(jobs) or any(dep not in pending for job in jobs for dep in job.dependencies):
        raise ValueError("job names must be unique and dependencies must exist")
    states = {job.name: "queued" for job in jobs}
    running = {}
    finished = set()
    failed = []
    while pending or running:
        for name, (process, _gpu) in list(running.items()):
            code = process.poll()
            if code is not None:
                del running[name]
                states[name] = "complete" if code == 0 else "failed"
                if code == 0:
                    finished.add(name)
                else:
                    failed.append(name)
                update(dict(states))
        if not failed:
            for name, job in list(pending.items()):
                if not set(job.dependencies) <= finished:
                    continue
                gpu = None
                if job.gpu:
                    occupied = {device for _process, device in running.values() if device is not None}
                    gpu = next((device for device in gpu_ids if device not in occupied and gpu_ready(device)), None)
                    if gpu is None:
                        continue
                elif sum(device is None for _process, device in running.values()) >= cpu_limit:
                    continue
                running[name] = (launch(job, gpu), gpu)
                del pending[name]
                states[name] = "running"
                update(dict(states))
        if not running and failed:
            raise RuntimeError(f"postprocessing jobs failed: {failed}")
        if pending and not running and not any(set(job.dependencies) <= finished for job in pending.values()):
            raise ValueError("postprocessing dependency cycle")
        if pending or running:
            pause(1)


def process_state(pid):
    try:
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return fields[0], fields[19]
    except FileNotFoundError:
        return None, None


def main():
    import fcntl
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-root", required=True, type=Path)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--model-root", required=True, type=Path)
    parser.add_argument("--model", default="qwen3-8b")
    parser.add_argument("--gpus", type=int, nargs="+", default=[2, 3, 6])
    parser.add_argument("--controller-pid", required=True, type=int)
    parser.add_argument("--prepare-pids", required=True, type=int, nargs="+")
    args = parser.parse_args()
    root = args.out_root.resolve()
    if not root.is_relative_to(Path("/mnt/mydata/wja")) or len(args.prepare_pids) != len(args.gpus):
        raise ValueError("invalid experiment output root or worker PID list")
    work = root / args.model
    snapshot = work / "code"
    lock = (root / "postprocess.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    base_env = {
        **os.environ, "PYTHONPATH": str(snapshot / "src"), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1",
        "RD_MODEL_ROOT": str(args.model_root), "RD_LOCAL_FILES_ONLY": "1", "HF_HUB_OFFLINE": "1",
        "HF_HOME": str(root / "cache"), "TMPDIR": str(root / "tmp"),
        "OMP_NUM_THREADS": "8", "OPENBLAS_NUM_THREADS": "8", "MKL_NUM_THREADS": "8", "NUMEXPR_NUM_THREADS": "8",
    }
    script_root = Path(__file__).resolve().parent
    write_json(root / "postprocess_execution.json", {
        "gpus": args.gpus, "cpu_jobs": 2, "blas_threads_per_job": 8,
        "source_code": str(snapshot / "src"), "measurement_parameters_unchanged": True,
        "script_hashes": {path.name: file_digest(path) for path in [Path(__file__), script_root / "fit_cached_inputs.py"]},
    })

    def status(state, **fields):
        payload = {"status": state, "updated_at": datetime.now(timezone.utc).isoformat(), **fields}
        write_json(root / "postprocess.json", payload)
        if state != "waiting_for_prepare":
            write_json(root / "pipeline.json", {**payload, "model": args.model, "gpus": args.gpus, "batch_size": 4})
        print(state, fields, flush=True)

    def gpu_ready(gpu):
        free = subprocess.check_output(["nvidia-smi", "-i", str(gpu), "--query-gpu=memory.free", "--format=csv,noheader,nounits"], text=True)
        return int(free.strip()) >= 25 * 1024

    def launch(job, gpu):
        if shutil.disk_usage(root).free < 2 * 1024**3:
            raise RuntimeError("insufficient disk space for postprocessing")
        command = [str(item) for item in job.command]
        env = {**base_env, **({"CUDA_VISIBLE_DEVICES": str(gpu)} if gpu is not None else {})}
        print("launch", job.name, "gpu", gpu, command, flush=True)
        with (root / "logs" / f"{args.model}-{job.name}.log").open("a") as handle:
            return subprocess.Popen(command, cwd=script_root.parent, env=env, stdout=handle, stderr=subprocess.STDOUT)

    def command(stage, *options):
        entry = [sys.executable, script_root / "fit_cached_inputs.py"] if stage == "fit" else [sys.executable, "-m", "reasoning_diff"]
        return [*entry, stage, *options, "--eval-mode", "scientific", "--resume"]

    def execute(jobs, phase):
        run_jobs(jobs, launch, args.gpus, update=lambda states: status("postprocessing", phase=phase, jobs=states), gpu_ready=gpu_ready)

    controller_stopped = False
    controller_retired = False
    old_start = None
    try:
        old_state, old_start = process_state(args.controller_pid)
        cmdline = Path(f"/proc/{args.controller_pid}/cmdline").read_bytes()
        if old_state is None or b"run_pr7_recovery.py" not in cmdline or str(root).encode() not in cmdline:
            raise ValueError("handoff PID is not the expected experiment controller")
        worker_starts = []
        for pid, gpu in zip(args.prepare_pids, args.gpus, strict=True):
            worker_cmdline = Path(f"/proc/{pid}/cmdline").read_bytes()
            if b"prepare_batched.py" not in worker_cmdline or str(work / f"prepare-gpu{gpu}").encode() not in worker_cmdline:
                raise ValueError(f"PID {pid} is not the expected prepare worker for GPU {gpu}")
            worker_starts.append(process_state(pid)[1])
        os.kill(args.controller_pid, signal.SIGSTOP)
        controller_stopped = True
        prepares = [work / f"prepare-gpu{gpu}" for gpu in args.gpus]
        while True:
            progress = [read_json(path / "progress.json") if (path / "progress.json").exists() else {} for path in prepares]
            worker_states = [process_state(pid) for pid in args.prepare_pids]
            active = [state not in {None, "Z"} and start == expected
                      for (state, start), expected in zip(worker_states, worker_starts, strict=True)]
            complete = [row.get("status") == "complete" and (path / "manifest.json").exists() for row, path in zip(progress, prepares, strict=True)]
            if any(not done and not alive for done, alive in zip(complete, active, strict=True)):
                raise RuntimeError("a prepare worker exited before completion; its trace checkpoints are preserved")
            status("waiting_for_prepare", completed_problems=sum(row.get("completed_tasks", 0) for row in progress),
                   total_problems=200, planned_gpu_jobs=3, planned_cpu_jobs=2)
            if all(complete) and not any(active):
                break
            time.sleep(30)
        for path in prepares:
            if not cli._resume(path, True, {"command": "prepare"}):
                raise ValueError(f"prepare manifest is incomplete: {path}")
        if process_state(args.controller_pid)[1] == old_start:
            os.kill(args.controller_pid, signal.SIGTERM)
            os.kill(args.controller_pid, signal.SIGCONT)
        controller_retired = True

        merged = work / "prepare-combined"
        execute([Job("merge", [sys.executable, snapshot / "scripts/merge_pr6_shards.py", "--out-dir", merged, *prepares])], "merge")
        traces = read_jsonl(merged / "traces.jsonl")
        bases = [row for row in traces if "trace-base" in row["id"] or "trace-t0p" in row["id"]]
        write_json(work / "generation_summary.json", {
            "n_problems": 200, "n_traces": len(traces), "statuses": dict(Counter(row["status"] for row in traces)),
            "execution_backends": dict(Counter((row.get("metadata") or {}).get("execution", {}).get("backend", "serial_decode") for row in traces)),
            "base_generations": len(bases), "base_correct": sum(row.get("correct") is True for row in bases),
            "base_accuracy_itt": sum(row.get("correct") is True for row in bases) / max(len(bases), 1), "scientific_conclusion": None,
        })
        del traces, bases
        labels = work / "label"
        layers = read_json(work / "protocol.json")["sweep_layers"]
        jobs = [Job("label", command("label", "--in-dir", merged, "--out-dir", labels)),
                Job("generation-analysis", command("analyze", "--in-dir", merged, "--out-dir", work / "generation-analysis"))]
        for layer in layers:
            collect = work / f"collect-layer{layer}"
            jobs.append(Job(f"collect-layer{layer}", command("collect", "--fixture", args.dataset, "--kind", "igsm", "--in-dir", merged,
                            "--out-dir", collect, "--backend", "frozen", "--model-name", args.model, "--device", "cuda", "--hidden-layer", layer), gpu=True))
            jobs.append(Job(f"fit-layer{layer}", command("fit", "--in-dir", collect, "--out-dir", work / f"fit-layer{layer}",
                            "--labels-dir", labels, "--split", "probe_train"), ("label", f"collect-layer{layer}")))
        execute(jobs, "layer_sweep")
        scores = []
        for layer in layers:
            behavior = next((row for row in read_jsonl(work / f"fit-layer{layer}/probes.jsonl") if row.get("head") == "behavior"), {})
            value = ((behavior.get("metrics") or {}).get("dev") or {}).get("auc")
            scores.append(float(value) if value is not None and math.isfinite(float(value)) else None)
        curve = [] if any(score is None for score in scores) else ["--dev-layer-scores", *scores, "--dev-layer-ids", *layers]
        write_json(work / "layer_sweep.json", {"layer_ids": layers, "dev_behavior_auc": scores, "status": "ready" if curve else "insufficient_dev_labels"})
        selected_layer = select_dev_layer(layers, scores)
        collect = work / f"collect-layer{selected_layer}"
        fit = work / "fit"
        fit_options = ["--in-dir", collect, "--labels-dir", labels, "--split", "probe_train", *curve]
        positions = ("pre_step", "pre_value", "post_step")
        jobs = [Job(f"fit-{position}", command("fit", *fit_options, "--out-dir", fit / position, "--position", position)) for position in positions]
        jobs.extend([
            Job("fit-all", command("fit", *fit_options, "--out-dir", fit, "--position", "all"), tuple(f"fit-{position}" for position in positions)),
            Job("calibrate", command("calibrate", "--in-dir", fit, "--out-dir", work / "calibration", "--features-dir", collect,
                "--labels-dir", labels, "--split", "calibration"), ("fit-all",)),
            Job("intervene", command("intervene", "--in-dir", merged, "--out-dir", work / "intervention", "--features-dir", collect,
                "--probes-dir", fit / "pre_step", "--labels-dir", labels, "--backend", "frozen", "--model-name", args.model,
                "--device", "cuda", "--max-new", "4096"), ("fit-all",), gpu=True),
            Job("repair", command("repair", "--in-dir", merged, "--out-dir", work / "repair", "--mask", "all", "--backend", "frozen",
                "--model-name", args.model, "--device", "cuda", "--max-new", "4096"), gpu=True),
        ])
        execute(jobs, "probe_positions_and_interventions")
        analysis_input = work / "analysis-input"
        analysis_input.mkdir(exist_ok=True)
        provenance = {}
        for source, names in [(merged, ["tasks.jsonl", "traces.jsonl", "splits.jsonl"]), (labels, ["labels.jsonl"]),
                              (fit, ["p1_table.jsonl"]), (work / "intervention", ["interventions.jsonl"]), (work / "repair", ["repairs.jsonl"])]:
            for name in names:
                shutil.copy2(source / name, analysis_input / name)
                provenance[name] = {"source": str(source / name), "sha256": file_digest(source / name)}
        write_json(analysis_input / "provenance.json", provenance)
        execute([Job("analyze", command("analyze", "--in-dir", analysis_input, "--out-dir", work / "analysis"))], "analysis")
        status("complete", report=str(work / "analysis/report.json"))
    except BaseException as exc:
        if controller_stopped and not controller_retired and process_state(args.controller_pid)[1] == old_start:
            os.kill(args.controller_pid, signal.SIGCONT)
        status("failed", error=f"{type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    main()
