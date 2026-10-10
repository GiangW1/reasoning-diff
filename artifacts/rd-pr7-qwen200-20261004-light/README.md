# PR7 Qwen3-8B 200-problem run

These are lightweight artifacts from the run rooted at
`/mnt/mydata/wja/reasoning-diff/runs/pr7-200-20261004`.
The pipeline finished on 2026-10-05 at 05:01 China Standard Time.
Its completion status means that the scheduled stages exited, not that every
scientific comparison produced usable evidence. See `SUMMARY.md` and
`diagnostics.json` for the observed limitations.

The runtime is based on PR7 commit
`c35b00b1d28388577535619374c8a72abfb1ad78`, with the checkpoint and scheduling
changes uploaded alongside these results. `qwen3-8b/protocol.json` records
the frozen scientific source hashes, model revision, dataset hashes, seeds,
sampling parameters, and persisted split fractions. The frozen source snapshot
and separate postprocessing scripts are included. The borrowed Python
environment was not modified.

## Contents

The bundle retains reports, calibration and intervention records, repair
records, protocol and run specifications, source manifests, audits, logs,
dataset snapshots, and per-trace and probe-metric summaries.
`qwen3-8b/trace_summary.jsonl` preserves the 3051 trace identities, outcome and
eligibility fields, stopping reasons, lengths, and hashes of the original text.
`probe_metrics.jsonl` files preserve recorded metrics without probe weights.

## Exclusions

No retained file exceeds 10 MiB. The export omits model weights, hidden-state
arrays, fitted probe weights, full generated trajectories, expanded event and
P1 tables, observations, per-trace checkpoints, caches, temporary files, and
duplicated analysis staging. Original large artifacts remain at the run root.
`excluded_files.json` records omitted data files and their original hashes.

Original stage manifests still refer to full run artifacts, including files
excluded here. They are provenance records, not an assertion that this bundle
is a resumable full run. `SHA256SUMS` verifies the actual exported files.

The companion archive is
`reasoning-diff-pr7-qwen200-20261004-light.tar.gz`, with a separate SHA-256 file.
