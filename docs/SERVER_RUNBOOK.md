# Server runbook

This machine only proves code paths. Real weights, official dumps, and GPU numbers stay `pending_server`.

## Environment lock (record, do not guess)

```text
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cu124   # choose the CUDA build that matches the box
python -m pip install transformers==5.5.3 tokenizers==0.22.2 huggingface-hub==1.9.2 safetensors==0.7.0 numpy==1.26.4 pytest==9.1.1
python -m pip install -e .[dev]
```

Record: GPU model, CUDA, dtype, attention backend, model revisions

- Qwen3-8B `b968826d9c46dd6066d109eabc6255188de91218` (hidden 4096)
- DeepSeek-R1-Distill-Qwen-7B `916b56a44061fd5cd7d6a8fb632557ed4f724f60` (hidden 3584)

Direct transfer of this pair must report `not_applicable_dimension_mismatch`.

## Commands

```text
python -m reasoning_diff prepare --fixture tests/fixtures/t1_tiny.json --out-dir runs/prepare
python -m reasoning_diff collect --fixture tests/fixtures/t1_tiny.json --in-dir runs/prepare --out-dir runs/collect --backend tiny
# fixture smoke: add --backend offline (writes prefix ids, not hidden states)
# scientific local: add --eval-mode scientific (refuses offline H and loss-as-score)
python -m reasoning_diff label --in-dir runs/prepare --out-dir runs/label
python -m reasoning_diff fit --in-dir runs/collect --labels-dir runs/label --out-dir runs/fit --split probe_train
python -m reasoning_diff calibrate --in-dir runs/fit --features-dir runs/collect --out-dir runs/cal --split calibration
python -m reasoning_diff intervene --in-dir runs/collect --out-dir runs/intervene
python -m reasoning_diff repair --in-dir runs/prepare --out-dir runs/repair --mask task_oracle
python -m reasoning_diff analyze --in-dir runs/label --out-dir runs/analyze

# local scientific (tiny random weights; not paper models)
python -m reasoning_diff prepare --fixture tests/fixtures/t1_tiny.json --out-dir runs/s-prep --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1
python -m reasoning_diff collect --fixture tests/fixtures/t1_tiny.json --in-dir runs/s-prep --out-dir runs/s-col --eval-mode scientific --backend tiny
```

Replace fixtures with official snapshots after they are frozen. Do not download weights on the laptop.

Optional matched no-edit noise: add `--sham-opportunities 1` to `prepare`.

Resume a completed stage with `--resume` if `manifest.json` already exists and `run_spec.config` matches (prepare uses the resolved edit; later stages use `command=collect|label|fit|…`). A failed resume writes `failure.json` and must not replace a successful manifest.

## Isolated code executor

Default HumanEval scoring is `executor_unavailable`. Optional local child-process backend: `get_executor("subprocess")` with timeout. Linux cgroup isolation stays `pending_server`. Never fall back to host `exec`.

## Expected artifacts

Each stage writes `run_spec.json`, `manifest.json` (content hashes), and stage jsonl/npz. `analyze` writes `report.json` and includes it in the manifest. Gate 0–2 stay `unregistered` until a protocol is frozen. Week-8 `scientific_conclusion` stays null until real measurements exist.
