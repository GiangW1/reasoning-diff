#!/usr/bin/env python3
"""Measure shared-model decoding throughput and per-seed reproducibility."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import math
from pathlib import Path
import time

import torch

from reasoning_diff.io import write_json
from reasoning_diff.models.adapters import load_frozen
from reasoning_diff.models.generate import decode_loop
from trace_batching import DecodeRequest, decode_batch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--tokens", default=256, type=int)
    parser.add_argument("--workers", nargs="+", type=int, default=[1, 2, 4])
    parser.add_argument("--prompt-lengths", nargs="+", type=int, default=[0, 3840])
    parser.add_argument("--mode", choices=["shared", "batch"], default="shared")
    args = parser.parse_args()
    payload = json.loads(args.checkpoint.read_text())
    row = payload.get("trace", payload)
    packed = load_frozen("qwen3-8b", device="cuda")
    model = packed["model"]
    sequences = [row["token_ids"][:length or row["metadata"]["prompt_len"]] for length in args.prompt_lengths]
    requests_per_setting = math.lcm(*args.workers)
    results = []
    for prompt in sequences:
        def decode(seed):
            return decode_loop(model, torch.tensor([prompt]), torch.Generator(device="cuda").manual_seed(seed),
                               max_new=args.tokens, temperature=0.6, top_k=20, top_p=0.95)["generated_ids"]
        decode(99)
        baseline = None
        for workers in args.workers:
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
            torch.cuda.synchronize()
            started = time.perf_counter()
            if args.mode == "shared" or workers == 1:
                with ThreadPoolExecutor(max_workers=workers) as pool:
                    tokens = list(pool.map(decode, range(requests_per_setting)))
            else:
                tokens = []
                for start in range(0, requests_per_setting, workers):
                    requests = [DecodeRequest(model, torch.tensor([prompt]), torch.Generator(device="cuda").manual_seed(seed),
                                              args.tokens, temperature=0.6, top_k=20, top_p=0.95)
                                for seed in range(start, min(start + workers, requests_per_setting))]
                    tokens.extend(result["generated_ids"] for result in decode_batch(requests))
            torch.cuda.synchronize()
            elapsed = time.perf_counter() - started
            if workers == 1:
                baseline = tokens
            result = {"mode": args.mode, "prompt_tokens": len(prompt), "workers": workers, "elapsed_seconds": elapsed,
                      "tokens_per_second": sum(map(len, tokens)) / elapsed,
                      "peak_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
                      "peak_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
                      "exact_tokens_match_serial": None if baseline is None else tokens == baseline}
            results.append(result)
            write_json(args.out, {"results": results})
            print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
