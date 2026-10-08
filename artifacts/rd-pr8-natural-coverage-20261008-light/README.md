# PR8 natural coverage results (2026-10-08)

Code: `91b87d0bf1271794ff0f26e88f801624a3c781c9`; source PR: GiangW1/reasoning-diff#8.

The final acquisition reuses 128 trajectories and adds 280, all naturally complete. Matching is 1406/1758 (79.98%); common noise support is 1396/1758 (79.41%); 20/24 reference trajectories have complete rho. Per-problem rho coverage still fails for problem 0007. The original natural matching issue remains unresolved; formal feature/fit/intervention experiments did not launch.

Includes v7/v8/v9 remeasurement reports, provenance, plans, logs, audits, final acquisition results, per-trajectory summaries, checkpoint indexes and the local code patch. No model assets, tensors, full token trajectories, expanded observation tables, individual checkpoint copies, test temporary directories, or files over 5 MiB are included.

Original run manifests describe the full server runs and therefore reference omitted files. `export_manifest.json` describes inclusion/exclusion; `SHA256SUMS` verifies the exported files.

Verify the bundle with `sha256sum -c SHA256SUMS` from its directory. Authoritative raw runs remain under `/mnt/mydata/wja/reasoning-diff/runs/`.
