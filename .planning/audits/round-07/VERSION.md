# Review freeze round-07

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`
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
- pytest_author_claim: 143 passed. Reviewers must re-run cited commands.
- prior: round-06 A–F FAIL on `dc2ba459…` (C 未交卷). This freeze is the r06 confirmed-defect close-out: generated-region events, expressible H only, identity donor pairing, persist source_value_pair, StreamBank basis_seed, C-layer second decode, collect `--weight-seed`, sham hits not booked as evaluated-zero noise, Prefill requires hidden, catalog aliases, required `--in-dir` for calibrate/intervene/repair.
- consecutive_pass_count: 0
