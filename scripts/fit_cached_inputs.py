#!/usr/bin/env python3
"""Avoid repeatedly parsing the immutable event rows during probe fitting."""
from __future__ import annotations

from pathlib import Path
import sys
import time

from reasoning_diff import cli
from reasoning_diff.io import file_digest, write_json


def main(argv=None):
    args = cli.build_parser().parse_args(argv)
    if args.cmd != "fit" or not args.in_dir:
        raise ValueError("cached-input runner requires fit --in-dir")
    event_path = (Path(args.in_dir) / "event_rows.jsonl").resolve()
    original = cli.read_jsonl
    cached = None
    hits = 0
    reads = 0
    started = time.perf_counter()

    def read(path):
        nonlocal cached, hits, reads
        if Path(path).resolve() != event_path:
            return original(path)
        if cached is None:
            cached = original(path)
            reads += 1
        else:
            hits += 1
        return cached

    cli.read_jsonl = read
    try:
        result = cli.main(argv)
    finally:
        cli.read_jsonl = original
    write_json(Path(args.out_dir) / "input_cache.json", {
        "event_rows": str(event_path), "file_reads": reads, "cache_hits": hits,
        "sha256": file_digest(event_path) if event_path.exists() else None,
        "elapsed_seconds": time.perf_counter() - started,
    })
    return result


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
