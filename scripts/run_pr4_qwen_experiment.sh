#!/usr/bin/env bash
set -uo pipefail

# Run the PR4 Qwen3-8B scientific pipeline for one data shard. The defaults
# match the server run; override the paths when reproducing elsewhere.
gpu="${1:?usage: $0 GPU_ID}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON_BIN:-python}"
fixture="${FIXTURE_ROOT:-/mnt/mydata/rd-pr4-shard-gpu${gpu}}"
output_root="${OUTPUT_ROOT:-/mnt/mydata/rd-pr4-full}"
model_root="${RD_MODEL_ROOT:-/mnt/mydata/wja-reasoning-diff-models}"
log_dir="${LOG_DIR:-/mnt/mydata/rd-pr4-logs}"
code_revision="${RD_CODE_REVISION:-1534e10e31c702d5d9a8a0371ae3f7dd80a208eb}"
repair_max_new="${REPAIR_MAX_NEW:-32}"

prep="${output_root}-prep-qwen-gpu${gpu}"
collect="${output_root}-collect-qwen-gpu${gpu}"
collect_input="${output_root}-collect-input-gpu${gpu}"
label="${output_root}-label-qwen-gpu${gpu}"
fit="${output_root}-fit-qwen-gpu${gpu}"
cal="${output_root}-cal-qwen-gpu${gpu}"
intervene="${output_root}-intervene-qwen-gpu${gpu}"
repair="${output_root}-repair-qwen-gpu${gpu}"
analyze="${output_root}-analyze-qwen-gpu${gpu}"
log="${log_dir}/pr4-qwen-gpu${gpu}.log"

export CUDA_VISIBLE_DEVICES="$gpu"
export RD_MODEL_ROOT="$model_root"
export RD_LOCAL_FILES_ONLY="${RD_LOCAL_FILES_ONLY:-1}"
export PYTHONPATH="$repo_root/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$repo_root" || exit 1
mkdir -p "$log_dir"
exec >>"$log" 2>&1

run_stage() {
  local name="$1"
  shift
  printf '[%s] stage=%s start\n' "$(date --iso-8601=seconds)" "$name"
  "$@"
  local status=$?
  printf '[%s] stage=%s exit_code=%s\n' "$(date --iso-8601=seconds)" "$name" "$status"
  return "$status"
}

run_stage prepare "$python_bin" -m reasoning_diff prepare \
  --fixture "$fixture" --out-dir "$prep" --eval-mode scientific --kind igsm \
  --backend frozen --model-name qwen3-8b --device cuda --max-new 4096 \
  --temperature 0.6 --top-k 20 --top-p 0.95 --disable-thinking \
  --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1 \
  --code-revision "$code_revision" || exit $?

# Keep failed traces in prepare for audit, but only pass parser-confirmed traces
# with events to hidden-state extraction. The source trace with no finite premise
# span remains in trace_quality.json and is excluded from collect.
mkdir -p "$collect_input"
cp "$prep/tasks.jsonl" "$prep/edits.jsonl" "$prep/splits.jsonl" "$collect_input/"
"$python_bin" - "$prep/traces.jsonl" "$collect_input/traces.jsonl" <<'PY'
import json
import sys

source, target = sys.argv[1:]
with open(target, "w", encoding="utf-8") as out:
    for line in open(source, encoding="utf-8"):
        row = json.loads(line)
        metadata = row.get("metadata") or {}
        if metadata.get("parse_status") == "ok" and row.get("events") and row.get("id") != "trace-source:90":
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
PY

run_stage collect "$python_bin" -m reasoning_diff collect \
  --fixture "$fixture" --in-dir "$collect_input" --out-dir "$collect" \
  --eval-mode scientific --backend frozen --kind igsm \
  --model-kind qwen2 --model-name qwen3-8b --device cuda || exit $?

run_stage label "$python_bin" -m reasoning_diff label \
  --in-dir "$prep" --out-dir "$label" --eval-mode scientific || exit $?

run_stage fit "$python_bin" -m reasoning_diff fit \
  --in-dir "$collect" --labels-dir "$label" --out-dir "$fit" \
  --eval-mode scientific --split probe_train --position all || exit $?

run_stage calibrate "$python_bin" -m reasoning_diff calibrate \
  --in-dir "$fit" --features-dir "$collect" --labels-dir "$label" \
  --out-dir "$cal" --eval-mode scientific --split calibration || exit $?

# Scientific intervention requires persisted dev-layer scores. Preserve an
# explicit skip artifact when fit has no held-out score vector.
dev_scores=""
if [ -f "$fit/p1_table.jsonl" ]; then
  dev_scores=$("$python_bin" - "$fit/p1_table.jsonl" <<'PY'
import json
import sys

scores = []
for line in open(sys.argv[1], encoding="utf-8"):
    row = json.loads(line)
    value = row.get("dev_score")
    if value is None:
        value = row.get("dev_f1")
    if value is not None:
        scores.append(str(float(value)))
print(" ".join(scores))
PY
)
fi
if [ -n "$dev_scores" ]; then
  # shellcheck disable=SC2086
  run_stage intervene "$python_bin" -m reasoning_diff intervene \
    --in-dir "$collect" --features-dir "$collect" --probes-dir "$fit" \
    --labels-dir "$label" --out-dir "$intervene" --eval-mode scientific \
    --backend frozen --model-name qwen3-8b --device cuda --max-new 4096 \
    --dev-layer-scores $dev_scores || true
else
  mkdir -p "$intervene"
  printf '%s\n' '{"status":"not_run","reason":"fit did not persist dev layer scores; scientific intervention requires them"}' > "$intervene/failure.json"
  printf '[%s] stage=intervene exit_code=skipped_missing_dev_scores\n' "$(date --iso-8601=seconds)"
fi

run_stage repair "$python_bin" -m reasoning_diff repair \
  --in-dir "$prep" --out-dir "$repair" --eval-mode scientific \
  --backend frozen --model-name qwen3-8b --device cuda --max-new "$repair_max_new" || true

run_stage analyze "$python_bin" -m reasoning_diff analyze \
  --in-dir "$label" --out-dir "$analyze" --eval-mode scientific || true

printf '[%s] pipeline gpu=%s finished\n' "$(date --iso-8601=seconds)" "$gpu"
