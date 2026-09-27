# Review freeze round-22

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`
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
- pytest_author_claim: 172 passed. Reviewers must re-run cited commands.
- prior: r21 A–E independently PASS on `5097c831…`. r21 F FAIL on F21-08 (scientific sham / noise used `rho_M_excess != 1.0 or null_reason` and other `is None or null_reason` disjunctions). This freeze replaces those with conjunctive locks (`excess/noise is None` AND `null_reason == noise_set_missing`, plus a `_scientific_sham_lock` that rejects forged 0.0 / empty events / booked 1.0). Also adds oracles for `card`, `forbid_host_exec`, Procrustes recovery, `attention_mean`, and `apply_model_template`. r21 A–E PASS do not transfer.
- consecutive_pass_count: 1
- consecutive_note: After independent A–F reports on this hash all PASS with no confirmed in-scope defects. Second consecutive round is r23 on the unchanged freeze.
