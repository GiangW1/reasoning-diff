# Observed results and limitations

## Configuration and timing

- Model: Qwen3-8B, pinned revision
  `b968826d9c46dd6066d109eabc6255188de91218`.
- Dataset: 200 official iGSM problems; thinking enabled; max_new=4096.
- GPUs: 2, 3, 6; sampling temperature=0.6, top_k=20, top_p=0.95.
- Main generation seeds: 0, 1, 2; behavior repeats=3; sham opportunities=3.
- Split fractions: 0.4, 0.15, 0.1, 0.1, 0.1, 0.15.
- Hidden-state layers: 0, 12, 24, 35.
- Generation finished: 2026-10-05 02:48 China Standard Time.
- Postprocessing finished: 2026-10-05 05:01; approximately 2 h 13 min.
- The run combines 1326 previously saved serial-decoder traces and 1725
  batched-decoder traces. The batching transition preserves the protocol and
  existing traces, but GPU kernel changes can change exact sampled tokens.

## Generation

There are 3051 trajectories, including base, edited, source, and sham traces:

| Status | Count | Percentage |
| --- | ---: | ---: |
| natural_complete | 255 | 8.36% |
| natural_truncated | 2679 | 87.81% |
| parse_failed | 117 | 3.83% |

110 of the parse_failed traces also stopped at the token limit. Overall,
2789/3051 traces (91.41%) exhausted the 4096-token budget. The generation
samples contain repeated reasoning and reconsideration of the iGSM aggregate
meaning; budget exhaustion is an observed outcome, not a recovered answer.

The 600 base generations have 43 correct recorded outcomes. The intention to
treat accuracy is 7.17%, including retained failures. This is not an estimate
of accuracy conditional on completing a valid answer.

## Fitting and calibration

All four layers and all three event positions were collected and fitted.
The behavior-probe dev AUC values are 0.4735, 0.8215, 0.6061, and 0.4922 for
layers 0, 12, 24, and 35 respectively. Calibration produced six finite records.
These are descriptive outputs: event eligibility and known labels reduce the
effective number of independent problems. For example, layer 12's behavior
test metric covers only five problem groups despite the 200-problem input.
Neither the dev maximum nor these small held-out metrics establish a stable
scientific finding.

## Intervention limitations

The intervention output contains one donor_missing record and no usable
causal intervention. The CLI selects only the first source_value_pair record.
Its three trace IDs have zero collected eligible event rows, so an aligned
donor cannot be chosen. Four of the 39 recorded pairs actually have aligned,
distinct finite donor features (indices 1, 6, 23, 27), but the selection does
not iterate over them. This is a downstream selection limitation, in addition
to the generation and event-eligibility problems.

## Repair limitations

The repair CLI evaluates one selected problem, not all 200. It produces 30
records: six masks times k=1..5. There are 26 ok statuses and four
mask_unmatched statuses caused by slot_not_found:p_1_0_0_1.
The run specification explicitly records learned_mask_unavailable with reason
features_probes_or_identity_rows_missing because repair reads the merged
prepare directory without the collected features and fitted probe inputs.
The five records labelled learned therefore do not demonstrate an available
learned mask; their execution status must not be interpreted as a successful
learned-method comparison.

## Interpretation and validation

The final report is evaluated_descriptive and scientific_conclusion is null.
The run is useful for diagnosing stopping, event alignment, probe behavior,
and downstream coverage. It does not complete the intended causal or learned
repair evaluation. DeepSeek-R1-Distill-Qwen-7B was not run.

Sixteen focused tests for batching, checkpoint resume, shard identities,
cached fitting, parallel scheduling, artifacts, and the CLI pipeline passed
before uploading. Cached and uncached fixture fitting outputs match, and
assembling completed position fits reuses them without refitting. No new
scientific-method fixes or reruns are included in this export.
