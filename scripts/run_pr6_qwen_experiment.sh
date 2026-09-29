#!/usr/bin/env bash
set -euo pipefail

# Generate one PR6 Qwen shard. Run this once per GPU, then merge every prepare
# directory with merge_pr6_shards.py before label/collect/fit.
gpu="${1:?usage: $0 GPU_ID}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON_BIN:-python}"
fixture="${FIXTURE_ROOT:-/mnt/mydata/rd-pr6-pilot10-shard-gpu${gpu}}"
output_root="${OUTPUT_ROOT:-/mnt/mydata/rd-pr6-pilot10-qwen4096-v3}"
model_root="${RD_MODEL_ROOT:-/mnt/mydata/wja-reasoning-diff-models}"
code_revision="${RD_CODE_REVISION:-590bfa998200dbe3736b7a1d8947aff6bf7d9d3f}"
max_new="${MAX_NEW:-4096}"
temperature="${TEMPERATURE:-0.0}"
top_k="${TOP_K:-0}"
top_p="${TOP_P:-1.0}"
prep="${output_root}-prep-qwen-gpu${gpu}"

export CUDA_VISIBLE_DEVICES="$gpu"
export RD_MODEL_ROOT="$model_root"
export RD_LOCAL_FILES_ONLY="${RD_LOCAL_FILES_ONLY:-1}"
export PYTHONPATH="$repo_root/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$repo_root"
exec "$python_bin" -m reasoning_diff prepare \
  --fixture "$fixture" --out-dir "$prep" --eval-mode scientific --kind igsm \
  --backend frozen --model-name qwen3-8b --device cuda --max-new "$max_new" \
  --temperature "$temperature" --top-k "$top_k" --top-p "$top_p" \
  --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1 \
  --code-revision "$code_revision"
