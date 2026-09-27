# Review freeze round-10

- date: 2026-09-21
- workspace: C:\Users\22688\Desktop\diff
- code_hash_sha256: `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`
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
- pytest_author_claim: 153 passed. Reviewers must re-run cited commands.
- prior: r07/r08 reports bound stale hashes. r09 A–F bound `9ffc4cd9…` and are stale after this edit. This freeze closes: collect copies `tasks.jsonl`; fit/calibrate search parent prepare/; scalar/`[0]` Prefill rejected; T3 prepare no longer forced through `source_value_pair`; rename remaps ids/expressions; Plus registers family locks so Symbolic co-groups to `test`; analyze refuses fake P1 from labels; PCA `truncated=True` when `n < min d`; mapped real-premise noise deducted, `sham:` hits stay missing; review merge path exists.
- consecutive_pass_count: 0
