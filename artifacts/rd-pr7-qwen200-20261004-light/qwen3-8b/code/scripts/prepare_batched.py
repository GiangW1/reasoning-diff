#!/usr/bin/env python3
"""Schedule frozen prepare requests in batches while reusing trace checkpoints."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import sys
from threading import RLock, local

from reasoning_diff import cli
from reasoning_diff.checkpoints import TraceCheckpoints
from reasoning_diff.io import digest, file_digest, read_json, write_json
from reasoning_diff.models import generate
from trace_batching import BatchDecoder


def prepare_requests(args):
    tasks = cli._load_tasks(args)
    repeats = max(3, int(args.n_seeds or 3))
    opportunities = max(1, int(args.sham_opportunities or 0), int(args.behavior_repeats or 3))
    requests = []
    for index, task in enumerate(tasks):
        edit = cli._domain_edit(task, args)
        if index == 0:
            for seed in range(repeats):
                run = "trace-base" if seed == 0 else "trace-t0p" if seed == 1 else f"trace-base:seed{seed}"
                requests.append((task, seed, run))
            for seed in range(repeats):
                requests.append((edit.task, seed, "trace-edit" if seed == 0 else f"trace-edit:seed{seed}"))
        else:
            for seed in range(repeats):
                suffix = "" if seed == 0 else f":seed{seed}"
                requests.extend([(task, seed, f"trace-base:{index}{suffix}"), (edit.task, seed, f"trace-edit:{index}{suffix}")])
        pair = cli._try_source_value_pair(task, edit.changed_premise_ids[0] if edit.changed_premise_ids else "",
                                         next(iter(edit.after.values()), "2"))
        if index == 0:
            if pair:
                requests.append((pair["same_value_diff_source"].task, 0, "trace-source"))
            for extra in cli._allowed_edits(task, int(args.behavior_repeats or 3)):
                requests.append((extra.task, int(extra.metadata.get("rng_seed", 0)), f"trace-{extra.id}"))
        for seed in range(repeats):
            for opportunity in range(opportunities):
                if index == 0:
                    sham_seed = 1000 + seed * opportunities + opportunity
                    run = "trace-sham" if seed == 0 and opportunity == 0 else f"trace-sham:{seed}:{opportunity}"
                else:
                    sham_seed = 2000 + index * repeats * opportunities + seed * opportunities + opportunity
                    run = f"trace-sham:{index}:{seed}:{opportunity}"
                requests.append((task, sham_seed, run))
        if index and pair:
            requests.append((pair["same_value_diff_source"].task, 0, f"trace-source:{index}"))
    return requests


def request_key(task, seed, run_id):
    return digest({"task": task.to_dict(), "seed": seed, "run_id": run_id})


class ScheduledTraces:
    def __init__(self, requests, generate, batch_size, executor):
        self.requests = requests
        self.generate = generate
        self.batch_size = batch_size
        self.executor = executor
        self.index = 0
        self.pending = {}

    def __call__(self, task, **kwargs):
        expected_task, seed, run_id = self.requests[self.index]
        key = request_key(task, kwargs["seed"], kwargs["run_id"])
        if key != request_key(expected_task, seed, run_id):
            raise ValueError("batched request plan differs from the frozen prepare protocol")
        if not self.pending:
            common = {name: value for name, value in kwargs.items() if name not in {"seed", "run_id"}}
            for next_task, next_seed, next_run in self.requests[self.index:self.index + self.batch_size]:
                next_key = request_key(next_task, next_seed, next_run)
                self.pending[next_key] = self.executor.submit(self.generate, next_task, seed=next_seed, run_id=next_run, **common)
        result = self.pending.pop(key).result()
        self.index += 1
        return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=4)
    options, stage_args = parser.parse_known_args(argv)
    args = cli.build_parser().parse_args(stage_args)
    if options.batch_size < 1 or args.cmd != "prepare" or args.backend != "frozen" or args.eval_mode != "scientific" or not args.checkpoint_traces:
        raise ValueError("batched runner requires positive batch size and frozen scientific prepare with trace checkpoints")
    requests = prepare_requests(args)
    output = Path(args.out_dir)
    spec_path = output / "checkpoints/spec.json"
    previous = read_json(spec_path)["fingerprint"] if spec_path.exists() else None
    prior = len(list((output / "checkpoints/traces").glob("*.json")))
    execution = {
        "backend": "shared_model_batched_decode", "batch_size": options.batch_size,
        "started_at": datetime.now(timezone.utc).isoformat(), "prior_saved_traces": prior,
        "prior_checkpoint_fingerprint": previous,
        "measurement_parameters_unchanged": True,
        "numerical_note": "Batched kernels may change sampled tokens relative to serial decoding; each trace records its batch.",
        "script_hashes": {path.name: file_digest(path) for path in [Path(__file__), Path(__file__).with_name("trace_batching.py")]},
    }
    write_json(output / "batch_execution.json", execution)
    decoder = BatchDecoder(options.batch_size)
    thread_state = local()
    original_decode = generate.decode_loop
    original_wrap = TraceCheckpoints.wrap
    original_progress = TraceCheckpoints._progress
    lock = RLock()

    def decode(*args, **kwargs):
        result = decoder(*args, **kwargs)
        thread_state.execution = result["batch_execution"]
        return result

    def progress(store, status, **fields):
        with lock:
            return original_progress(store, status, batch_size=options.batch_size, **fields)

    with ThreadPoolExecutor(max_workers=options.batch_size) as executor:
        def wrap(store, generate_trace):
            def recorded(task, **kwargs):
                trace = generate_trace(task, **kwargs)
                trace.metadata["execution"] = {**execution, **thread_state.execution}
                return trace
            cached = original_wrap(store, recorded)
            return ScheduledTraces(requests, cached, options.batch_size, executor)

        generate.decode_loop = decode
        TraceCheckpoints.wrap = wrap
        TraceCheckpoints._progress = progress
        try:
            return cli.main(stage_args)
        finally:
            executor.shutdown(wait=True, cancel_futures=True)
            generate.decode_loop = original_decode
            TraceCheckpoints.wrap = original_wrap
            TraceCheckpoints._progress = original_progress
            decoder.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
