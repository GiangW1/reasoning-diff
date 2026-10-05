"""Persist natural traces before the prepare stage finishes."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .io import digest, read_json, write_json
from .schema import Trace


class TraceCheckpoints:
    def __init__(self, out: Path, spec: dict, *, resume: bool = False):
        self.out = out
        self.root = out / "checkpoints"
        self.fingerprint = digest(spec)
        spec_path = self.root / "spec.json"
        if spec_path.exists():
            if read_json(spec_path)["fingerprint"] != self.fingerprint:
                raise ValueError("trace checkpoint specification mismatch; use a new output directory")
            if not resume:
                raise ValueError("existing trace checkpoints require --resume")
        else:
            write_json(spec_path, {"fingerprint": self.fingerprint, "spec": spec})
        self.keys = {path.stem for path in (self.root / "traces").glob("*.json")}
        progress_path = out / "progress.json"
        previous = read_json(progress_path) if progress_path.exists() else {}
        self.completed_tasks = set(previous.get("completed_task_ids") or [])
        self.n_tasks = spec["config"]["n_tasks"]

    def _progress(self, status: str, **fields) -> None:
        write_json(self.out / "progress.json", {
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "fingerprint": self.fingerprint,
            "total_tasks": self.n_tasks,
            "completed_tasks": len(self.completed_tasks),
            "completed_task_ids": sorted(self.completed_tasks),
            "saved_traces": len(self.keys),
            **fields,
        })

    def wrap(self, generate):
        def cached_generate(task, **kwargs):
            identity = {"task": task.to_dict(), "seed": kwargs["seed"], "run_id": kwargs["run_id"]}
            key = digest(identity)
            path = self.root / "traces" / f"{key}.json"
            current = {"current_task": task.base_group_id, "current_trace": kwargs["run_id"]}
            if path.exists():
                row = read_json(path)
                if row.get("fingerprint") != self.fingerprint or row.get("identity") != identity:
                    raise ValueError(f"trace checkpoint identity mismatch: {path.name}")
                if digest(row["trace"]) != row.get("trace_hash"):
                    raise ValueError(f"trace checkpoint hash mismatch: {path.name}")
                trace = Trace.from_dict(row["trace"])
                print(f"resume {task.base_group_id} {kwargs['run_id']}", flush=True)
            else:
                self._progress("generating", **current)
                print(f"generate {task.base_group_id} {kwargs['run_id']}", flush=True)
                trace = generate(task, **kwargs)
                payload = trace.to_dict()
                write_json(path, {
                    "fingerprint": self.fingerprint, "identity": identity,
                    "trace_hash": digest(payload), "trace": payload,
                })
                self.keys.add(key)
                print(f"saved {task.base_group_id} {kwargs['run_id']} status={trace.status}", flush=True)
            self._progress("trace_saved", **current)
            return trace

        return cached_generate

    def task_complete(self, task) -> None:
        self.completed_tasks.add(task.task_id)
        self._progress("task_complete", current_task=task.base_group_id)
        print(f"completed {len(self.completed_tasks)}/{self.n_tasks} problems", flush=True)

    def finish(self) -> None:
        self._progress("complete")
