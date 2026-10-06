# PR8 Smoke Failure Evidence

See [REPORT.zh-CN.md](REPORT.zh-CN.md) for the failure analysis, measured recovery results, and remaining work.

This package records the Qwen3-8B run based on PR #8 at `153c0fb`, using GPUs 2, 3, and 6 with eight smoke problems and a planned 32-problem exploratory cohort. The main workflow stopped before formal generation because matched-cell coverage was below the unchanged 50% engineering threshold.

The parser recovery reused all 335 saved traces. Strict all-step coverage remains insufficient. The last-explicit-thinking-assignment analysis is a separate, descriptive diagnostic and must not be used as evidence that the original protocol passed.

## Contents

- `original/`: run configuration, deadline, pilot, stage progress, smoke checks, layer selection, and the original 24-row P1 table.
- `reparse/`: before/after measurement report, strict 24-row P1 table, and the 24-row final-commitment diagnostic table.
- `controller-error.txt`: the controller's terminal exception.
- `validation.json`: test results and artifact verification.
- `checksums.sha256`: hashes of the published evidence files.

Weights, raw trajectories/token arrays, feature matrices, full checkpoints, and caches are excluded. Original data remains on the experiment server under `/mnt/mydata/wja/reasoning-diff/runs/`.
