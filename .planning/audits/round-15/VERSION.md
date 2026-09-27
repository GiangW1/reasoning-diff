# Review freeze round-15

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`
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
- pytest_author_claim: 159 passed. Reviewers must re-run cited commands.
- prior: r13 A independently confirmed A13-01 (rename labeled as source–value), A13-02 (unknown counted as M), A13-03 (sham no-change books empty N). This freeze: alt-source same-value graph; unknown → rho_M null; sham: rows never evaluate empty N. r14 A–F bound `1f61fd06…` and are stale.
- consecutive_pass_count: 0
