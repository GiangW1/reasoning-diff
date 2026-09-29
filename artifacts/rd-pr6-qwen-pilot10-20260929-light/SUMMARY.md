# PR6 Qwen3-8B pilot summary

## Configuration

- Base problems: 30 total, 10 each on GPUs 1, 3, and 6
- Generation: Qwen3-8B, greedy decoding, `max_new=4096`
- Hidden-state sweep: layers 0, 12, 24, and 35
- Selected layer: 12, chosen only from the held-out dev curve

## Generation quality

- Valid traces: 83/83
- Parser successes: 83/83
- Traces with an extracted answer: 83/83
- Traces with events: 83/83, 1,652 events total
- Traces ending at the finalizer limit: 16/83
- Missing target events: 5/83
- Correct traces: 16/83
- Correct base-problem traces: 2/30
- Generated tokens: min 944, mean 1,254.9, max 1,952

All traces used the bounded-thinking finalizer. This makes the trajectories suitable
for this protocol but distinguishes them from unconstrained natural generations.

## Labels and features

- Event-premise labels: 1,091
- Known behavior labels: 226 (94 positive, 132 negative)
- Hidden rows per layer: 1,652 x 4,096
- Premise rows per layer: 110 x 4,096

Held-out dev AUC by layer at `pre_step`:

| Layer | AUC |
| ---: | ---: |
| 0 | 0.556 |
| 12 | 0.699 |
| 24 | 0.689 |
| 35 | 0.402 |

## P1 descriptive results

| Position | Head | Baseline AUC | Full AUC | Delta AUC |
| --- | --- | ---: | ---: | ---: |
| pre_step | behavior | 0.474 | 0.539 | 0.065 |
| pre_value | behavior | 0.474 | 0.622 | 0.148 |
| post_step | behavior | 0.474 | 0.685 | 0.211 |
| pre_step | task | 0.207 | 0.368 | 0.161 |
| pre_value | task | 0.207 | 0.519 | 0.311 |
| post_step | task | 0.207 | 0.615 | 0.407 |

These are pilot estimates. The calibration split contains only 3 independent
problem units, below the preregistered minimum of 5, so no conformal threshold
was reported.

## Intervention and repair

- The intervention hook fired at layer 12 and token 696 before the aligned event.
- The main and INLP interventions changed generated tokens; the weak-layer control
  at layer 35 did not.
- The single donor problem had zero target-follow effect versus baseline, random,
  and weak-layer controls. P3 has only one problem unit and no usable interval.
- Oracle repair completed for k=1 through k=5. All five outputs were legal and
  correct for the edited task, and all five matched their full-recompute controls.

## Artifacts

- Combined prepare: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-prep`
- Labels: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-label`
- Selected layer features: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-collect-layer12`
- Final probes: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-fit-selected`
- Calibration: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-cal-selected`
- Intervention: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-intervene-selected`
- Repair: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-repair-v2`
- Analysis: `/mnt/mydata/rd-pr6-pilot10-qwen4096-v3-combined-analyze-v2`

## Validation

- Full repository test suite: 237 passed
- Diff whitespace validation: passed
