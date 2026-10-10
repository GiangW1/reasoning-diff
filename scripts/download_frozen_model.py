#!/usr/bin/env python3
"""Download a pinned public checkpoint and verify its published LFS hashes."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import time

from reasoning_diff.io import file_digest, write_json
from reasoning_diff.models.adapters import card


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--out-root", required=True, type=Path)
    parser.add_argument("--endpoint", default="https://hf-mirror.com")
    args = parser.parse_args()
    info = card(args.model)
    endpoint = args.endpoint.rstrip("/")
    response = subprocess.run([
        "curl", "--fail", "--location", "--silent", "--show-error", "--retry", "3", "--max-time", "60",
        f"{endpoint}/api/models/{info['id']}/revision/{info['revision']}?blobs=true",
    ], capture_output=True, text=True, check=True)
    metadata = json.loads(response.stdout)
    if metadata["sha"] != info["revision"]:
        raise ValueError("download metadata does not match the pinned revision")
    destination = args.out_root / info["id"].split("/")[-1]
    destination.mkdir(parents=True, exist_ok=True)
    files = [item for item in metadata["siblings"] if item["rfilename"].endswith((".json", ".txt", ".safetensors"))]
    write_json(destination / "download_metadata.json", {"model": info, "endpoint": endpoint, "files": files})

    def download(item):
        name = item["rfilename"]
        path = destination / name
        expected_hash = (item.get("lfs") or {}).get("sha256")
        if path.is_file() and path.stat().st_size == item["size"]:
            if not expected_hash or file_digest(path) == expected_hash:
                print(f"already verified {name}", flush=True)
                return
        url = f"{endpoint}/{info['id']}/resolve/{info['revision']}/{name}?download=true&rd_attempt={int(time.time())}"
        subprocess.run([
            "aria2c", "--continue=true", "--allow-overwrite=true", "--auto-file-renaming=false",
            "--max-connection-per-server=8", "--split=8", "--min-split-size=16M",
            "--max-tries=12", "--retry-wait=5", "--connect-timeout=30", "--timeout=60",
            "--summary-interval=30", "--console-log-level=warn", "--download-result=hide",
            "--show-console-readout=false",
            "--dir", str(path.parent), "--out", path.name, url,
        ], check=True)
        if path.stat().st_size != item["size"]:
            raise ValueError(f"size mismatch for {name}")
        if expected_hash and file_digest(path) != expected_hash:
            raise ValueError(f"SHA-256 mismatch for {name}")
        print(f"verified {name} ({item['size']} bytes)", flush=True)

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(download, files))
    write_json(destination / "verified.json", {
        "model_id": info["id"], "revision": info["revision"],
        "file_hashes": {item["rfilename"]: file_digest(destination / item["rfilename"]) for item in files},
    })
    print(f"checkpoint ready: {destination}", flush=True)


if __name__ == "__main__":
    main()
