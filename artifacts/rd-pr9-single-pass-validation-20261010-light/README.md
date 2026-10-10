# PR9 single-pass experiments and validation (2026-10-10)

Experiment source commit: `f9935256012b94482e9a958e20d03259d0e55a97`. Source PR: GiangW1/reasoning-diff#9.

Natural and constrained validation each generated 525/525 registered responses. Reference accuracy was 36/36 and 31/36 respectively. Natural matching coverage was 47.35% (base), 48.59% (related no-op), and 51.77% (neutral no-op). Common noise coverage was about 30%; rho coverage was 0%, 8.33%, and 0%. Constrained coverage was 100% by construction. The original natural matching problem remains unresolved.

Each registered reference/edit/noise condition is generated once; no matching retries or post-hoc response completion were used in the single-pass batches. Earlier pilot attempts are separate historical development evidence and are not pooled with validation.

The validation cohort has no test families, so P3 cannot be estimated. The controlled report was completed by representing its genuinely empty registered P3 shard; no new model generation occurred. Natural references are all correct, leaving no error class for error prediction evaluation in this cohort. The old 24-family formal candidates include only one test family and prior development exposure. The new formal directories contain plans only: no formal responses were generated.

The file named `semantic_audit.json` in historical runs counts placeholder text only; it is a quality screen, not an independent entity/value/relation semantic audit. The corrected supervisor requires measured natural and controlled coverage, a fresh formal test cohort, and independent semantic audit before launch. Actual time deadlines were removed via the recorded operational adapter while frozen configurations remain unchanged as provenance.

Original STATUS files and queue/launch logs are historical snapshots and may say running or contain old estimates. Use `summary.json`, `VALIDATION_RESULTS.zh-CN.md`, and each `CURRENT_SUMMARY.json` for this export’s status. Operational source snapshots are committed under `experiments/pr9-validation-20261010/operations/`; their absolute paths describe the actual server deployment and are not portable defaults.

Includes metrics, plans, configs, selected inputs, logs, failure diagnostics, checkpoint metadata/digests, and storage inventory. Model assets, binary tensors, raw checkpoint copies, expanded token/observation files, caches, and individual files over 5 MiB are omitted. `export_manifest.json` records exclusions; original manifests describe full runs and can reference omitted artifacts. Authoritative originals remain under `/mnt/mydata/wja/reasoning-diff/`. Verify this export with `sha256sum -c SHA256SUMS`.
