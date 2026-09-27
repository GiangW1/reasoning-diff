# Review freeze round-19

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`
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
- pytest_author_claim: 165 passed. Reviewers must re-run cited commands.
- prior: r18 F independently confirmed F18-03 (sequential overlapping rename) and F18-08 (intervene silent `cap=64`). This freeze does simultaneous `_rewrite_ids` and refuses overlong intervene prefixes. Calibrate no longer walks sibling `lab`/`label`/`labels`. r18 A–E PASS on `3d0f1c10…` do not transfer.
- consecutive_pass_count: 0
