---
status: passed_local
updated: 2026-09-21
---

# Phase 1 Verification

## Automated

```
python -m pytest tests -q --tb=short
```

Result: 65 passed, exit 0 (2026-09-21). Includes T1 fixture prepare, artifacts, official-shape/mod-23, T2 sidecar + GSM-Plus test-only, T3/T4, conformal examples, transfer dim reject, tiny Qwen2/Qwen3 hooks, CLI `--in-dir` pipeline, and round-01 defect regressions.

## Human

None required for this phase's code contracts.

## Deferred to server

Official iGSM generator dumps, GSM/Hotpot/MuSiQue/HumanEval full snapshots, GPU traces.
