# Review freeze round-17

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`
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
- pytest_author_claim: 160 passed. Reviewers must re-run cited commands.
- prior: r16 freeze `5413a4bc…` was invalidated by A14-02/03/04 edits to `edits.py` / `measure.py` / `cli.py` / tests. r16 A–F bound the old hash and are stale. This freeze is XOR `src_b` (keep *a*), scientific `refused_not_section8` for §8 toys, and empty-N no longer booked evaluated.
- consecutive_pass_count: 0
