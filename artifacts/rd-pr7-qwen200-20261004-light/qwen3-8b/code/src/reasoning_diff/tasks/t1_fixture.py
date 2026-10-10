"""Self-authored T1 arithmetic fixtures. Never labeled official."""
from __future__ import annotations

from pathlib import Path

from ..io import read_json
from ..schema import Task


def load_t1_fixture(path: str | Path) -> Task:
    data = read_json(path)
    if data.get("source_kind") != "fixture":
        raise ValueError("T1 fixture loader requires source_kind=fixture")
    if data.get("source_kind") == "official":
        raise ValueError("Fixture path cannot be marked official")
    task = Task.from_dict(data)
    if task.source_kind != "fixture":
        raise ValueError("load_t1_fixture refuses non-fixture records")
    task.validate()
    return task
