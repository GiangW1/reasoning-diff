# Review freeze round-13

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`
- files: 61 (`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`)
- hash_method (reproduce exactly):

```python
import hashlib
from pathlib import Path
root = Path(r"C:\Users\22688\Desktop\diff")
files = sorted(p for p in root.joinpath("src/reasoning_diff").rglob("*.py") if "__pycache__" not in p.parts)
files += sorted(p for p in root.joinpath("tests").rglob("*.py") if "__pycache__" not in p.parts)
files.append(root / "pyproject.toml")
h = hashlib.sha256()
for p in files:
    h.update(p.relative_to(root).as_posix().encode("utf-8"))
    h.update(b"\x00")
    h.update(p.read_bytes())
print(len(files))
print(h.hexdigest())
```

- git_head: 46a6e26da8637fe29d9f8f0667cb4e513538a59d (working tree dirty)
- pytest_author_claim: 156 passed. Reviewers must re-run cited commands.
- prior: r10 A independently confirmed A10-04 (Plus family lock was process-local RAM; new-process Symbolic `gsm8k-1` → `probe_train`). This freeze persists locks to `.planning/research/.cache/gsm_test_only_families.json`. r12 A–F bound `598e6c8f…` and are stale after this `splits.py` edit.
- consecutive_pass_count: 0
