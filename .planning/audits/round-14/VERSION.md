# Review freeze round-14

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`
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
- pytest_author_claim: 157 passed. Reviewers must re-run cited commands.
- prior: r12 A independently confirmed A12-03 on un-drifted `cli.py`: 4-level + extras search bound ancestor `col/tasks.jsonl` (WRONG-TASK, E=`[p2,p1]`). This freeze searches only the given stage directories. r13 A–F bound `0816fa5b…` and are stale.
- consecutive_pass_count: 0
