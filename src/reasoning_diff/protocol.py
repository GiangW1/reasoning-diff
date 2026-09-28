"""Shared audit contracts for stable identities, scoring, provenance and costs."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import time
from typing import Any, Iterable

import numpy as np

from .events import normalize_answer
from .io import file_digest


def stable_row_key(
    *,
    task_id: str | None = None,
    base_group_id: str | None = None,
    trace_id: str | None = None,
    event_id: str | None = None,
    identity_key: str | None = None,
    premise_id: str | None = None,
    edit_id: str | None = None,
    protocol: str | None = None,
    position: str | None = None,
) -> str:
    """Return a deterministic key for one persisted experiment row."""
    payload = {
        "task_id": task_id or "",
        "base_group_id": base_group_id or "",
        "trace_id": trace_id or "",
        "event_id": event_id or "",
        "identity_key": identity_key or "",
        "premise_id": premise_id or "",
        "edit_id": edit_id or "",
        "protocol": protocol or "",
        "position": position or "",
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def answer_score(
    prediction: str | None,
    gold: str | None,
    kind: str,
    aliases: Iterable[str] | None = None,
    *,
    executor=None,
    tests: str | None = None,
) -> dict:
    """Score one answer and preserve raw/normalized/status fields."""
    raw = prediction
    if kind == "code":
        if executor is None or tests is None or prediction is None:
            return {
                "answer_raw": raw,
                "answer_normalized": normalize_answer(prediction, kind),
                "gold_normalized": normalize_answer(gold, kind),
                "score_status": "executor_unavailable",
                "correct": None,
            }
        result = executor.submit(prediction, tests)
        return {
            "answer_raw": raw,
            "answer_normalized": normalize_answer(prediction, kind),
            "gold_normalized": normalize_answer(gold, kind),
            "score_status": result.status,
            "correct": None if result.tests_passed is None else bool(result.tests_passed),
            "executor": result.to_dict(),
        }
    candidates = {normalize_answer(gold, kind)}
    candidates.update(normalize_answer(item, kind) for item in aliases or [])
    normalized = normalize_answer(prediction, kind)
    if normalized is None or None in candidates:
        correct = None
        status = "missing_answer"
    else:
        correct = normalized in candidates
        status = "scored"
    return {
        "answer_raw": raw,
        "answer_normalized": normalized,
        "gold_normalized": normalize_answer(gold, kind),
        "score_status": status,
        "correct": correct,
    }


def recursive_manifest(path: str | Path, *, data_version: str | None = None, loader_version: str | None = None) -> dict:
    """Hash a file or directory without relying on a directory file hash."""
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(root)
    if root.is_file():
        files = [{"path": root.name, "sha256": file_digest(root), "bytes": root.stat().st_size}]
    else:
        files = []
        for item in sorted(p for p in root.rglob("*") if p.is_file()):
            rel = item.relative_to(root).as_posix()
            files.append({"path": rel, "sha256": file_digest(item), "bytes": item.stat().st_size})
    payload = {
        "root_name": root.name,
        "files": files,
        "data_version": data_version,
        "loader_version": loader_version,
    }
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {**payload, "manifest_hash": hashlib.sha256(encoded.encode("utf-8")).hexdigest()}


@dataclass
class CostTimer:
    """Small wall-clock timer whose zero values always have an explicit reason."""

    name: str
    started: float = 0.0
    elapsed_seconds: float | None = None
    status: str = "not_started"

    def __enter__(self) -> "CostTimer":
        self.started = time.perf_counter()
        self.status = "running"
        return self

    def __exit__(self, *_exc) -> None:
        self.elapsed_seconds = time.perf_counter() - self.started
        self.status = "measured"

    def to_dict(self) -> dict:
        return asdict(self)


def finite_matrix(matrix: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(matrix, dtype=float)
    if array.ndim != 2 or not np.isfinite(array).all():
        raise ValueError(f"{name} must be a finite two-dimensional matrix")
    return array
