# PR2 Server Run Results

This directory contains the lightweight artifacts from the 2026-09-27 server run
against PR #2 of `GiangW1/reasoning-diff`.

## Code and environment

- PR #2 head: `baf4853e3788a62f4106325ab9bc2724bb9462f6`
- PR #2 merge: `62db25bfbc7c5805b540dfa264f56f4ffd52b1b9`
- Model: local Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`
- Dataset: official iGSM snapshot, 500 tasks, split into two 250-task shards
- GPUs: RTX 5090, CUDA devices 3 and 6

## Results

| Run | Outcome |
| --- | --- |
| Qwen single-task scientific prepare | Passed: 7/7 traces had answers, events, and `eos` stop; max 1802 generated tokens |
| Qwen direct generation seed 0/1 | Seed 0 and seed 1 smoke traces were recorded; the unconstrained thinking variants hit `max_new` |
| Qwen prospective BF16 hook | Hook fired successfully after float32 NumPy conversion |
| Qwen 250-task shard, GPU 3 | Fail-closed: many traces had `parse_failed` |
| Qwen 250-task shard, GPU 6 | Fail-closed: many traces had `parse_failed` |
| DeepSeek-R1 smoke | Stopped on request; the earlier 2048-token smoke hit `max_new` with an incorrect answer |

The full Qwen runs are retained as failure artifacts rather than being presented
as scientific results. The diagnostic trace shows the model using shorthand
variables such as `R3` and `T_V`; the event parser requires assignments using the
exact names from the question.

## Excluded files

Model weights, tokenizer caches, GPU memory dumps, intermediate tensor files,
and other large files are intentionally excluded. Every file in this directory
is a text or JSON artifact and is below 1 MB.
