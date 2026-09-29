# PR6 Qwen3-8B pilot artifacts

This directory contains the lightweight, reviewable outputs from the PR6 pilot.
The experiment used code commit `e550e226a88db1c7de74e9d65a416a37452ba20e`.

## Run configuration

- Model: Qwen3-8B
- GPUs: 1, 3, and 6
- Workload: 10 base problems per GPU, 30 total
- Decoding: greedy, with `max_new=4096`
- Hidden-state layers: 0, 12, 24, and 35
- Dev-selected layer: 12

See `SUMMARY.md` for the main metrics and scientific limitations. The original
`run_spec.json`, manifests, dev-layer scores, calibration output, intervention
output, repair output, and final analysis report are retained here.

## Full run archive

`../reasoning-diff-pr6-qwen-pilot10-20260929-light.tar.gz` contains the run
directories from `/mnt/mydata` after removing large or redundant files. Its
digest is stored in the adjacent `.sha256` file.

The archive excludes:

- `features.npz` hidden-state matrices
- `probes.jsonl` fitted probe weights
- `event_rows.jsonl` and `p1_table.jsonl` expanded analysis tables
- duplicate `traces.jsonl` files from per-GPU prepare and collect directories
- the duplicated `combined-analysis-input` staging directory
- failed outputs superseded by `combined-repair-v2` and `combined-analyze-v2`
- model weights and caches, which were never stored in the run directories

The canonical merged `combined-prep/traces.jsonl` remains in the archive so the
generated trajectories can still be inspected. `SHA256SUMS` covers every file
in this lightweight review directory.
