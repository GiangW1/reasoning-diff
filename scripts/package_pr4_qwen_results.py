#!/usr/bin/env python3
"""Copy only the light, auditable portion of a PR4 Qwen run."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


STAGES = {
    "prep": ("manifest.json", "run_spec.json", "trace_quality.json"),
    "collect": ("manifest.json", "run_spec.json", "failure.json"),
    "label": ("manifest.json", "run_spec.json"),
    "fit": ("manifest.json", "run_spec.json", "p1_table.jsonl"),
    "cal": ("manifest.json", "run_spec.json", "calibration.jsonl"),
    "intervene": ("failure.json",),
    "repair": ("manifest.json", "run_spec.json", "repairs.jsonl"),
    "analyze": ("manifest.json", "run_spec.json", "analysis.jsonl", "report.json"),
}

README = """# PR4 Qwen3-8B light run bundle

This bundle contains the small, auditable outputs from the PR4 Qwen3-8B run on GPUs 1, 3, and 6. The source revision is `1534e10e31c702d5d9a8a0371ae3f7dd80a208eb`; the model revision is `b968826d9c46dd6066d109eabc6255188de91218`.

The bundle keeps stage manifests, run specifications, trace-quality summaries, fit tables, calibration and repair summaries, analysis reports, and logs. It excludes model weights, `features.npz`, `probes.jsonl`, raw prepare traces, collect event rows, collect observations, and every other file larger than 10 MiB. `SUMMARY.json` contains the aggregate counts and the exact excluded categories. `SHA256SUMS` covers every file in this directory except itself.

The pipeline completed on all three shards. It produced 1,096 traces in total; trace-quality accounting marked 151 valid, and 150 were passed to hidden-state collection after excluding one source trace without a finite premise span. There were 189 correct traces and 2,724 scan opportunities: 48 changed, 256 no-change, 168 parse-failed, and 2,252 structural.

The analysis result is deliberately fail-closed: every shard reports `status=not_evaluated` and `scientific_conclusion=null`. The data did not provide enough valid natural traces or held-out/dev supervision for the registered scientific gates, so intervention was skipped because fit did not persist dev-layer scores. These outputs document execution and failure modes; they do not support a scientific conclusion.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path("/mnt/mydata/rd-pr4-full"))
    parser.add_argument("--log-dir", type=Path, default=Path("/mnt/mydata/rd-pr4-logs"))
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--max-file-bytes", type=int, default=10 * 1024 * 1024)
    return parser.parse_args()


def copy_checked(source: Path, destination: Path, max_file_bytes: int) -> int:
    if not source.is_file():
        return 0
    size = source.stat().st_size
    if size > max_file_bytes:
        raise ValueError(f"refusing large result file: {source} ({size} bytes)")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return size


def main() -> None:
    args = parse_args()
    if args.destination.exists():
        shutil.rmtree(args.destination)
    args.destination.mkdir(parents=True)
    selected: list[dict[str, object]] = []

    for gpu in (1, 3, 6):
        for stage, names in STAGES.items():
            source_dir = args.source_root.parent / f"{args.source_root.name}-{stage}-qwen-gpu{gpu}"
            for name in names:
                source = source_dir / name
                if not source.exists():
                    continue
                relative = Path(f"gpu{gpu}") / stage / name
                size = copy_checked(source, args.destination / relative, args.max_file_bytes)
                selected.append({"path": relative.as_posix(), "bytes": size})

        for name in (f"pipeline-gpu{gpu}.log", f"tail-gpu{gpu}.log"):
            source = args.log_dir / name
            if not source.exists():
                continue
            relative = Path("logs") / name
            size = copy_checked(source, args.destination / relative, args.max_file_bytes)
            selected.append({"path": relative.as_posix(), "bytes": size})

    summary = {
        "model": "Qwen3-8B",
        "model_revision": "b968826d9c46dd6066d109eabc6255188de91218",
        "code_revision": "1534e10e31c702d5d9a8a0371ae3f7dd80a208eb",
        "gpus": [1, 3, 6],
        "total_traces": 1096,
        "valid_traces_in_quality": 151,
        "collect_traces": 150,
        "correct_traces": 189,
        "scan_opportunities": {"changed": 48, "no_change": 256, "parse_failed": 168, "structural": 2252},
        "analysis_status": "not_evaluated",
        "scientific_conclusion": None,
        "intervention": "not_run: fit did not persist dev layer scores",
        "excluded_patterns": [
            "model weights",
            "features.npz",
            "probes.jsonl",
            "prepare/traces.jsonl",
            "collect/event_rows.jsonl",
            "collect/observations.jsonl",
        ],
        "selected_files": selected,
    }
    (args.destination / "SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.destination / "README.md").write_text(README, encoding="utf-8")

    checksums = []
    for path in sorted(p for p in args.destination.rglob("*") if p.is_file()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checksums.append(f"{digest}  {path.relative_to(args.destination).as_posix()}")
    (args.destination / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
