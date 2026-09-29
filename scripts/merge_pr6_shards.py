#!/usr/bin/env python3
"""Merge independent prepare shards while namespacing trace identities."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_rows(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def prefix_identity(value, prefix: str):
    return f"{prefix}:{value}" if value else value


def merge_prepare(inputs: list[Path], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    merged = {name: [] for name in ("tasks.jsonl", "edits.jsonl", "splits.jsonl", "traces.jsonl", "observations.jsonl")}
    for index, source in enumerate(inputs):
        prefix = f"shard{index}"
        merged["tasks.jsonl"].extend(read_rows(source / "tasks.jsonl"))
        merged["edits.jsonl"].extend(read_rows(source / "edits.jsonl"))
        merged["splits.jsonl"].extend(read_rows(source / "splits.jsonl"))
        for row in read_rows(source / "traces.jsonl"):
            row["id"] = prefix_identity(row.get("id"), prefix)
            row["run_id"] = prefix_identity(row.get("run_id"), prefix)
            row["record_id"] = prefix_identity(row.get("record_id"), prefix)
            for event in row.get("events") or []:
                event["run_id"] = prefix_identity(event.get("run_id"), prefix)
                event["record_id"] = prefix_identity(event.get("record_id"), prefix)
            merged["traces.jsonl"].append(row)
        for row in read_rows(source / "observations.jsonl"):
            row["reference_trace"] = prefix_identity(row.get("reference_trace"), prefix)
            row["comparison_trace"] = prefix_identity(row.get("comparison_trace"), prefix)
            row["observation_id"] = prefix_identity(row.get("observation_id"), prefix)
            row["run_id"] = prefix_identity(row.get("run_id"), prefix)
            row["record_id"] = prefix_identity(row.get("record_id"), prefix)
            merged["observations.jsonl"].append(row)
    for name, rows in merged.items():
        write_rows(output / name, rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("inputs", nargs="+", type=Path)
    args = parser.parse_args()
    merge_prepare(args.inputs, args.out_dir)


if __name__ == "__main__":
    main()
