# Review freeze round-21

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb`
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
- prior: r20 F independently confirmed F20-01/02: 70-char intervene only locked `prefix_truncated is not True` (hardcoded False), and sibling-lab calibrate only used `inspect.getsource`. This freeze spies hook `prompt_ids` length (>64) and runs `cmd_calibrate` with a sibling `lab` present. r20 A–E PASS on `dc36f217…` do not transfer.
- consecutive_pass_count: 0
