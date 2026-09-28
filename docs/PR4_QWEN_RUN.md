# PR4 Qwen3-8B server run

This records the Qwen3-8B run made from PR4 commit `1534e10e31c702d5d9a8a0371ae3f7dd80a208eb` on GPUs 1, 3, and 6. The reusable entry point is [`scripts/run_pr4_qwen_experiment.sh`](../scripts/run_pr4_qwen_experiment.sh); it takes one GPU id and supports `FIXTURE_ROOT`, `OUTPUT_ROOT`, `RD_MODEL_ROOT`, `PYTHON_BIN`, and `LOG_DIR` overrides.

The light result bundle is under [`artifacts/rd-pr4-qwen-run-20260928-light`](../artifacts/rd-pr4-qwen-run-20260928-light) and the compressed copy is [`artifacts/reasoning-diff-pr4-qwen-run-20260928-light.tar.gz`](../artifacts/reasoning-diff-pr4-qwen-run-20260928-light.tar.gz). It contains stage manifests, run specifications, trace-quality summaries, fit tables, calibration/repair summaries, analysis reports, and stage logs. It deliberately excludes model weights, `features.npz`, `probes.jsonl`, raw traces, event rows, and other large intermediate files.

The run completed all requested stages. Across the three shards there were 1,096 generated traces; 151 were marked valid by trace-quality accounting, while 150 were passed to hidden-state collection after excluding one source trace without a finite premise span. The run recorded 189 correct traces and 2,724 scan opportunities (`changed=48`, `no_change=256`, `parse_failed=168`, `structural=2,252`).

These numbers are an execution audit, not a scientific finding. The analysis reports are `status=not_evaluated` with `scientific_conclusion=null`: the valid natural-trace and held-out/dev supervision was insufficient for the registered P1-P3 gates, and intervention was skipped because fit did not persist dev-layer scores. The bundle preserves these fail-closed statuses instead of presenting a conclusion.

To reproduce one shard after installing the project and model dependencies:

```bash
PYTHON_BIN=/path/to/python RD_MODEL_ROOT=/path/to/models \
  scripts/run_pr4_qwen_experiment.sh 1
```
