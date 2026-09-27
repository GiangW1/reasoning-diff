# Review freeze round-20

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `dc36f21713f2a8e021d44c992681c13aafd76ccd93a545c331fd984f787fbebb`
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
- pytest_author_claim: 167 passed. Reviewers must re-run cited commands.
- prior: r19 F independently confirmed F19-06: scientific-fit `all(... if baseline in S)` was vacuous if those rows were omitted or carried `score=1.0`. This freeze requires the four §8 rows to exist with `refused_not_section8` and no score, and adds CLI locks for 70-char intervene and calibrate sibling walk. r19 A/C PASS on `b6db632f…` do not transfer.
- consecutive_pass_count: 0
