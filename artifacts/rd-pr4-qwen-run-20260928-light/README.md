# PR4 Qwen3-8B light run bundle

This bundle contains the small, auditable outputs from the PR4 Qwen3-8B run on GPUs 1, 3, and 6. The source revision is `1534e10e31c702d5d9a8a0371ae3f7dd80a208eb`; the model revision is `b968826d9c46dd6066d109eabc6255188de91218`.

The bundle keeps stage manifests, run specifications, trace-quality summaries, fit tables, calibration and repair summaries, analysis reports, and logs. It excludes model weights, `features.npz`, `probes.jsonl`, raw prepare traces, collect event rows, collect observations, and every other file larger than 10 MiB. `SUMMARY.json` contains the aggregate counts and the exact excluded categories. `SHA256SUMS` covers every file in this directory except itself.

The pipeline completed on all three shards. It produced 1,096 traces in total; trace-quality accounting marked 151 valid, and 150 were passed to hidden-state collection after excluding one source trace without a finite premise span. There were 189 correct traces and 2,724 scan opportunities: 48 changed, 256 no-change, 168 parse-failed, and 2,252 structural.

The analysis result is deliberately fail-closed: every shard reports `status=not_evaluated` and `scientific_conclusion=null`. The data did not provide enough valid natural traces or held-out/dev supervision for the registered scientific gates, so intervention was skipped because fit did not persist dev-layer scores. These outputs document execution and failure modes; they do not support a scientific conclusion.
