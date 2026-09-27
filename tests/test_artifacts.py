import math
from pathlib import Path

import numpy as np
import pytest

from reasoning_diff.artifacts import write_manifest, write_run_spec
from reasoning_diff.io import (
    encode,
    file_digest,
    read_json,
    read_jsonl,
    read_npz,
    write_jsonl,
    write_npz,
)
from reasoning_diff.schema import SCHEMA_VERSION
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def test_jsonl_roundtrip(tmp_path, t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    path = tmp_path / "tasks.jsonl"
    write_jsonl(path, [task.to_dict()])
    rows = read_jsonl(path)
    assert rows[0]["task_id"] == task.task_id
    assert rows[0]["source_kind"] == "fixture"


def test_npz_no_pickle(tmp_path):
    path = tmp_path / "arr.npz"
    write_npz(path, {"x": np.arange(4, dtype=np.int64)})
    loaded = read_npz(path)
    assert np.array_equal(loaded["x"], np.arange(4))


def test_run_spec_and_manifest(tmp_path, t1_tiny_path):
    write_jsonl(tmp_path / "tasks.jsonl", [{"ok": True}])
    spec_path = write_run_spec(
        tmp_path,
        {
            "input_hashes": {Path(t1_tiny_path).name: file_digest(t1_tiny_path)},
            "source_kinds": {Path(t1_tiny_path).name: "fixture"},
            "config": {"command": "prepare"},
            "rng": {"split_seed": 0},
            "code_revision": "testrev",
        },
    )
    spec = read_json(spec_path)
    assert spec["schema_version"] == SCHEMA_VERSION
    assert Path(t1_tiny_path).name in spec["input_hashes"]
    assert spec["code_revision"] == "testrev"
    assert "split_seed" in spec["rng"]
    with pytest.raises(ValueError):
        write_run_spec(tmp_path, {"code_revision": "latest", "source_kinds": {"a": "fixture"}})
    manifest_path = write_manifest(
        tmp_path,
        [tmp_path / "tasks.jsonl", spec_path],
        {"tasks": 1, "success": 1, "failure": 0},
        upstream_ids=["up-1"],
    )
    manifest = read_json(manifest_path)
    assert manifest["upstream_manifest_ids"] == ["up-1"]
    assert "tasks.jsonl" in manifest["file_hashes"]
    reconstructed = {k: v for k, v in manifest.items() if k != "digest"}
    from reasoning_diff.io import digest

    assert manifest["digest"] == digest(reconstructed)


def test_encode_rejects_nan():
    with pytest.raises(ValueError):
        encode({"x": math.nan})
