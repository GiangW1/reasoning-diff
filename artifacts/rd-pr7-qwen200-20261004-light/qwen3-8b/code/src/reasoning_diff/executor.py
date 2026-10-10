"""Code-task executors. Host exec is never a fallback. Child process is not a sandbox."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable


@dataclass
class ExecutionResult:
    status: str
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    tests_passed: bool | None = None
    elapsed_seconds: float | None = None
    reason: str | None = None
    limits: dict | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class IsolatedExecutor:
    """Sandbox contract. Default and only local implementation is unavailable."""

    isolated_sandbox = True

    def submit(self, source: str, tests: str, limits: dict | None = None) -> ExecutionResult:
        return ExecutionResult(status="executor_unavailable", reason="base executor does not run code")


class UnavailableExecutor(IsolatedExecutor):
    def submit(self, source: str, tests: str, limits: dict | None = None) -> ExecutionResult:
        return ExecutionResult(
            status="executor_unavailable",
            tests_passed=None,
            reason="no isolated backend configured; host exec is forbidden",
            limits=limits or {},
        )


class SpyExecutor(IsolatedExecutor):
    """Test backend that records submissions and never executes host code."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def submit(self, source: str, tests: str, limits: dict | None = None) -> ExecutionResult:
        self.calls.append({"source": source, "tests": tests, "limits": limits or {}})
        if "exec(" in source or "exec(" in tests:
            return ExecutionResult(status="rejected", reason="submission mentions exec", limits=limits or {})
        return ExecutionResult(status="executor_unavailable", reason="spy backend cannot run code", limits=limits or {})


class ChildProcessExecutor:
    """Ordinary child process. Not an isolated sandbox (GOAL §5.15)."""

    isolated_sandbox = False
    name = "child_process"

    def submit(self, source: str, tests: str, limits: dict | None = None) -> ExecutionResult:
        limits = limits or {}
        timeout = float(limits.get("timeout", 2))
        if "exec(" in source or "exec(" in tests or "eval(" in source or "eval(" in tests:
            return ExecutionResult(status="rejected", reason="submission mentions exec/eval", limits=limits)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "submission_test.py"
            path.write_text(source + "\n" + tests + "\n", encoding="utf-8")
            try:
                proc = subprocess.run(
                    [sys.executable, str(path)],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                return ExecutionResult(status="timeout", reason="subprocess timeout", limits=limits)
            passed = proc.returncode == 0
            return ExecutionResult(
                status="ok" if passed else "failed",
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                tests_passed=passed,
                limits=limits,
            )


SubprocessExecutor = ChildProcessExecutor


class IsolatedBwrapExecutor(IsolatedExecutor):
    """Server-callable isolated backend. Unavailable unless bwrap (or RD_ISOLATED_BACKEND) exists."""

    isolated_sandbox = True
    name = "isolated"

    def submit(self, source: str, tests: str, limits: dict | None = None) -> ExecutionResult:
        limits = limits or {}
        if "exec(" in source or "exec(" in tests or "eval(" in source or "eval(" in tests:
            return ExecutionResult(status="rejected", reason="submission mentions exec/eval", limits=limits)
        backend = os.environ.get("RD_ISOLATED_BACKEND", "bwrap")
        exe = shutil.which(backend)
        if exe is None:
            return ExecutionResult(
                status="executor_unavailable",
                reason=f"isolated backend {backend!r} is not installed",
                limits=limits,
            )
        timeout = float(limits.get("timeout", 2))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "submission_test.py"
            path.write_text(source + "\n" + tests + "\n", encoding="utf-8")
            cmd = [exe, "--unshare-net", "--die-with-parent", "--tmpfs", "/tmp", sys.executable, str(path)]
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False, env={})
            except subprocess.TimeoutExpired:
                return ExecutionResult(status="timeout", reason="isolated timeout", limits=limits)
            passed = proc.returncode == 0
            return ExecutionResult(
                status="ok" if passed else "failed",
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                tests_passed=passed,
                limits=limits,
            )


def get_executor(name: str | None = None):
    if name == "spy":
        return SpyExecutor()
    if name in {"subprocess", "child_process"}:
        return ChildProcessExecutor()
    if name in {"isolated", "bwrap"}:
        return IsolatedBwrapExecutor()
    return UnavailableExecutor()


def forbid_host_exec(fn: Callable) -> Callable:
    def wrapped(*args, **kwargs):
        raise RuntimeError("host execution of model/dataset code is forbidden")

    return wrapped
