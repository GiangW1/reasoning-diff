"""Immutable run specs, manifests, shards and resume rules."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import digest, file_digest, runtime_info, write_json
from .schema import SCHEMA_VERSION, SOURCE_KINDS


def _reject_latest(obj: Any, path: str = "") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            loc = f"{path}.{key}" if path else key
            if value == "latest":
                raise ValueError(f"{loc} cannot use mutable identity 'latest'")
            _reject_latest(value, loc)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            _reject_latest(value, f"{path}[{i}]")


def write_run_spec(out_dir: str | Path, spec: dict) -> Path:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "protocol_version": spec.get("protocol_version", "reasoning-diff/0.1"),
        "code_revision": spec.get("code_revision") or runtime_info()["git_revision"],
        "environment": spec.get("environment") or runtime_info(),
        "input_hashes": dict(spec.get("input_hashes") or {}),
        "source_kinds": dict(spec.get("source_kinds") or {}),
        "config": dict(spec.get("config") or {}),
        "rng": dict(spec.get("rng") or {}),
        "models": dict(spec.get("models") or {}),
    }
    for extra, value in spec.items():
        if extra not in payload:
            payload[extra] = value
    for kind in payload["source_kinds"].values():
        if kind not in SOURCE_KINDS:
            raise ValueError(f"Unknown source_kind {kind!r}")
    _reject_latest(payload)
    path = Path(out_dir) / "run_spec.json"
    write_json(path, payload)
    return path


def write_manifest(
    out_dir: str | Path,
    files: list[str | Path],
    counts: dict[str, int],
    upstream_ids: list[str] | None = None,
    extra: dict | None = None,
) -> Path:
    file_hashes = {}
    array_shapes = {}
    for item in files:
        path = Path(item)
        file_hashes[path.name] = file_digest(path)
        if path.suffix == ".npz":
            from .io import read_npz

            arrays = read_npz(path)
            array_shapes[path.name] = {
                name: {"shape": list(arr.shape), "dtype": str(arr.dtype)} for name, arr in arrays.items()
            }
    body = {
        "schema_version": SCHEMA_VERSION,
        "file_hashes": file_hashes,
        "record_counts": counts,
        "array_shapes": array_shapes,
        "success_count": counts.get("success", 0),
        "failure_count": counts.get("failure", 0),
        "upstream_manifest_ids": list(upstream_ids or []),
    }
    if extra:
        body.update(extra)
    body["digest"] = digest({k: v for k, v in body.items() if k != "digest"})
    path = Path(out_dir) / "manifest.json"
    write_json(path, body)
    return path


def completed_shard_ok(shard_path: str | Path, expected_hash: str) -> bool:
    path = Path(shard_path)
    return path.exists() and file_digest(path) == expected_hash
