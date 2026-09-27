# Review freeze round-18

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`
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
- pytest_author_claim: 162 passed. Reviewers must re-run cited commands.
- prior: r15 A–F bound `401e509b…` and drifted; they do not count. r15 F independently confirmed F15-01: `_load_source_value_pair` walked sibling `prep`/`prepare`/`s-prep`, so independently named collect dirs fell back to `same_identity_fallback`. This freeze copies `edits.jsonl` on collect and reads only `in-dir/edits.jsonl`. r17 freeze `3d0a0764…` is stale.
- consecutive_pass_count: 0
