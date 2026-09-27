# Review freeze round-09

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`
- files: 60 (`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`)
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
- pytest_author_claim: 144 passed. Reviewers must re-run cited commands.
- prior: round-07 D reported HASH_MISMATCH on `9814019a…` and confirmed D7-03/04/05. This freeze wires source-value donor traces, INLP/C-rand/rescue/C-layer as distinct decodes, and `ie_z` from target-follow g(Y).
- consecutive_pass_count: 0
