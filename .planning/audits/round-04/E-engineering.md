# E：端到端工程审查（round-04）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮 A–D/F 通道报告。`ISSUES.md` 中作者标为本地已关的「E-05 Event/Label/Trace identities、E-09 failure manifest + success_count、E-16 `_upstream` before write、E-17 labels-dir hashed、`--eval-mode scientific`、subprocess executor」已独立复测，不采信作者关闭声明。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 01:15–01:45 +08:00 |
| 声称冻结 hash | `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`（`.planning/audits/round-04/VERSION.md`） |
| 独立复算冻结 hash | **复现成功**。按 VERSION 脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**56** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（仓库根与 `%TEMP%\rd-e-r4b` cwd 相同；`io.runtime_info` 用 `git -C <repo_root>`） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机另有 `torch 2.7.1+cpu` 供 tiny 对照） |
| 审查范围 | 用户 CLI 跨模块路径；schema/shape/ID、run_spec/manifest、resume 哈希校验、shards、atomic NPZ、`python -m`、隔离执行器、可复现性、异常、`--eval-mode scientific` |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md` |
| 实跑入口 | `python -m reasoning_diff`（runbook 命令）；产物根 `%TEMP%\rd-e-r4\` 与干净续跑对照 `%TEMP%\rd-e-r4b\`，未写入 `src/` / `tests/` |

**冻结说明：** 审查对象是当前工作区字节，且与声称冻结 hash **一致**。本报告绑定该快照。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–658 | 通读 + `python -m` 八段实跑 + resume/负路径 + `--in-dir` 文件 + scientific + `--shard` | `--in-dir` 目录时写 input_hashes（含 `--labels-dir`）；`--resume` 校验 file_hashes 与 digest，但 command 键与写出值不一致；`--shard` 存在但两分支同形；失败 `main` 覆盖成功清单 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 通读 + 各阶段 manifest + `success_count` 实验 | digest 自洽；`success_count` 缺省为 0；`array_shapes` 现含 dtype；`upstream_manifest_ids` 为重算 digest |
| `src/reasoning_diff/io.py` | 1–133 | 通读 + NPZ/NaN/`runtime_info` cwd 实验 | JSON/JSONL/NPZ 临时文件+`os.replace`；object 数组写入拒绝；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | 通读 + `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–47 | 对照实跑 | 命令形状可执行；默认 collect 为 `--backend tiny`，本通道主跑按任务要求 `--backend offline`；runbook calibrate **无** `--features-dir`；隔离执行器仍 `pending_server`（subprocess 为可选本地后端） |
| `src/reasoning_diff/executor.py` | 1–99 | 通读 + `get_executor` / `score_code` / subprocess | 默认 Unavailable；`get_executor("subprocess")` 子进程跑源+测，拒 `exec(`/`eval(`；`forbid_host_exec` 无生产引用 |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–384 | 通读 + 产物 `from_dict` | Event/Label `record_id` 已填；`Trace.from_dict` 把未知键并入 metadata；Event 两行 `record_id` 相同 |
| `src/reasoning_diff/splits.py` | 1–97 | CLI `require_split` | test 上 fit、probe_train 上 calibrate 仍拒绝 |
| `src/reasoning_diff/edits.py` | 1–258 | 默认 prepare `p2→2`；编辑 Task 新 `record_id` | 重算答案 8；`record_id=fix-t1-001::p2=2` |
| `src/reasoning_diff/events.py` | 1–154 | prepare/collect 解析 | 合成文本现含前提句；事件仍只匹配节点别名；`surface_mentions=[]` |
| `src/reasoning_diff/graphs.py` | 1–46 | prepare `ancestors` | CLI 用 `anc.get(event_id)`；单节点夹具任务集=`{p1,p2}` |
| `src/reasoning_diff/measure.py` | 1–320 | prepare/label `build_labels` | CLI 调用 `build_labels` |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | offline 轨迹 `pre_step.expressible=true`（字符偏移假 token） |
| `src/reasoning_diff/models/collect.py` | 1–60 | 对照 CLI | **`--backend tiny` 调用** `collect_tiny`；offline 路径不调用 |
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | `fit` | 持久化 `U`/`V`/`b`/loss/rank/split；双头 |
| `src/reasoning_diff/probes/calibrate.py` | 1–42 | `calibrate` | runbook 路径未走到 `predict_matrix`；`q=inf` 无法 JSON |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | offline 单行 H → `donor_missing`；tiny 两行 → 几何范数，效应仍 `null` |
| `src/reasoning_diff/repair.py` | 1–73 | `repair` | 读 `--in-dir` traces；`record_id` 已填；`run_id`/`base_group_id` 空 |
| `src/reasoning_diff/analysis.py` | 1–253 | `analyze` | 现读 labels 的 densities sidecar；`p1_table.jsonl` 不存在 → `not_evaluated`；P1–P3 为 null |
| `src/reasoning_diff/transfer.py` | 1–52 | analyze `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | prepare/collect | fixture 拒绝 official |
| `src/reasoning_diff/tasks/catalog.py` | 1–39 | prepare `--kind` | 仅 prepare/collect 经 `_load_task` 分派 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–62 | `--kind humaneval` + `score_code` | prepare 当 T1 价值编辑；无宿主 exec |
| `src/reasoning_diff/models/adapters.py` | 1–42 | 通读 | 冻结 revision 卡片；CLI 未用 |
| `src/reasoning_diff/rng.py` | 1–53 | 通读 | CLI 未用 `StreamBank` |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | 通读 | CLI 未调用 `BoundaryMLP.fit` |
| `src/reasoning_diff/baselines.py` | 1–80 | 抽样 | **未被** CLI 子命令调用 |
| `tests/test_cli_pipeline.py` | 1–29 | 读，未当作验收 | 只断言 exit 0、`not_evaluated`、report 进清单 |
| `tests/test_artifacts.py` | 1–73 | 读 | 不覆盖 resume/CLI 接线 |
| `tests/test_review_regressions.py` | 381–394 | 读作者关闭用例 | `test_pipeline_consumes_upstream` 仍不断言 `input_hashes` / `Trace.from_dict` / `--labels-dir` 入哈希 |

**抽样未做完整工程审查（非本通道主路径）：** `models/generate.py`、`models/tiny.py`、T1 official / T2 / T3 / T4 适配器内部。确认它们**未被**八段通用子命令在默认路径调用（`--kind` 仅 prepare/collect）。

## 3. 已执行检查与结果

### 3.1 用户 CLI 入口

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| `python -m reasoning_diff --help`（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（包未安装） |
| `collect --help` | **0** | 有 `--backend {tiny,offline}`、`--shard`、`--kind`/`--snapshot`、`--eval-mode` |
| `fit --help` | **0** | 有 `--labels-dir`、`--split`、`--eval-mode` |
| `calibrate --help` | **0** | 有 `--features-dir`（**runbook 未写**） |

`__main__.py` 存在并转调 `main`。runbook 的 `python -m reasoning_diff …` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 真实跨模块 CLI（指定顺序，collect=offline）

产物根：`%TEMP%\rd-e-r4\`。夹具 `tests/fixtures/t1_tiny.json`。`--in-dir` 按 `docs/SERVER_RUNBOOK.md` 指向上一阶段目录。collect 按任务要求加 `--backend offline`（runbook 默认 tiny；tiny 另作对照，见 §3.2b）。

| 命令 | 退出码 |
|---|---|
| `prepare --fixture tests/fixtures/t1_tiny.json --out-dir <tmp>/prep` | **0** |
| `collect --fixture … --in-dir <tmp>/prep --out-dir <tmp>/collect --backend offline` | **0** |
| `label --in-dir <tmp>/prep --out-dir <tmp>/label` | **0** |
| `fit --in-dir <tmp>/collect --labels-dir <tmp>/label --out-dir <tmp>/fit --split probe_train` | **0** |
| `calibrate --in-dir <tmp>/fit --out-dir <tmp>/cal --split calibration` | **0** |
| `intervene --in-dir <tmp>/collect --out-dir <tmp>/intervene` | **0** |
| `repair --in-dir <tmp>/prep --out-dir <tmp>/repair --mask task_oracle` | **0** |
| `analyze --in-dir <tmp>/label --out-dir <tmp>/analyze` | **0** |

**接线实测（不是源码猜测）：**

| 阶段 | `input_hashes` | `upstream_manifest_ids` | 实际消费 |
|---|---|---|---|
| prepare | `{t1_tiny.json: 3267db38…}` | `[]` | 夹具 |
| collect | 上游 prep 全部文件 + `upstream_manifest` + `upstream_manifest_recomputed`（与 prep 文件字节 **全等**） | `[b4d86687…]` = **重算** prep digest（= `manifest.digest`） | 若有 `tasks.jsonl` 取第一行 Task，否则再读夹具；**不读** prepare traces/events；`features.npz` = prefix id 向量；`weight_source=offline_prefix_ids` |
| label | 同 collect，哈希 prep 全目录 | `[b4d86687…]` | 读 prepare `observations.jsonl` + `tasks.jsonl`；`build_labels` |
| fit | collect 目录文件 **加** `label/labels.jsonl` 等 labels-dir 键 | `[e1d13561…, 106cb1c0…]` = collect digest + label digest | 读 `H`/`E` + `--labels-dir` 的 task/behavior 标签；写出双头 `U`/`V`/`b` |
| calibrate | `{fit/probes.jsonl, run_spec, upstream_manifest*}` | `[eb354a69…]` | **不读** collect `features.npz`（无 `--features-dir`）；`scores=null`，`status=probe_weights_or_features_missing` |
| intervene | collect 清单 | `[e1d13561…]` | 读 `H`（仅 1 行）→ `status=donor_missing`；效应字段 `null` |
| repair | 哈希 prep 全目录 | `[b4d86687…]` | 读 `traces.jsonl` 的 `token_ids`/`text`；`original_token_budget=20` |
| analyze | `{label/labels.jsonl, run_spec, upstream_manifest*}` | `[106cb1c0…]` | 读 labels 的 densities sidecar；**不找** `p1_table.jsonl` 以外的 P1 表（label 从不写）；`p1/p2/p3=null`；`status=not_evaluated` |

`collect` 无 `--in-dir` 仍 exit **0**，`input_hashes={}`。`analyze` 无 `--in-dir` 仍 exit **0**；`report.json` 与带 `--in-dir` 的报告 **不再字节全等**（无 in-dir 时 `densities=null`，有 in-dir 时带上 sidecar）。

八个阶段 `manifest.digest` 均等于 `digest(body without digest)`。`upstream_manifest_ids` 现为 **重算** digest，不再抄 `digest` 字段。

`_write_stage` 先 `_upstream` 再写 jsonl。`_upstream` 对文件路径抛 `NotADirectoryError`。

#### 3.2b tiny 对照（非主跑）

`collect --backend tiny` exit **0**：`weight_source=random_init`，`H`/`E` shape `[2,32]`/`[2,32]`，调用 `collect_tiny`。`intervene --in-dir <tiny>` → `status=geometry_on_hidden`，`main_norm=crand_norm=clayer_norm≈1.036`，目标/非目标/任务正确/无效仍为 `null`，`hook_once=resid_post`。轨迹文本与 token_ids 仍是合成字符偏移，不是 tiny 解码 ID。

### 3.3 schema / shape / ID

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

Observation（精确一行）：

```text
{"alignment_ref": "{\"entity_or_expression\": \"q\", ...}", "edit_id": "edit:fix-t1-001:p2:2", "event_pair": ["q","q"], "node_id": "q", "observation_id": "obs:q:p2", "outcome": "changed", "premise_id": "p2", "raw_values": ["0","8"], "record_id": "obs:q:p2", "run_id": "prepare", "scan_state": "observed_response", ...}
```

默认编辑仍为 **p2:0→2**，`outcome=changed`，`raw_values=["0","8"]`。合成轨迹文本现为 `"p1 = 4\np2 = 0\nq = 0\n"` / `"p1 = 4\np2 = 2\nq = 8\n"`。这是夹具上的有效扰动，**不是**科学全量扫描。

身份合同（本轮实测）：

1. `events.jsonl` 两行 `record_id` 均为 identity JSON，**彼此相同**；`run_id` 为 `trace-base` / `trace-edit`；`base_group_id=fix-t1-001`。`Event.from_dict` 成功。
2. 两行 Task：`task_id`/`record_id` 分别为 `fix-t1-001` 与 `fix-t1-001::p2=2`（不再碰撞）；`run_id=""`。
3. prepare/label 的 Label：`record_id="q:p2"`（已填）；`run_id=""`，`base_group_id=""`。第二行仍是 densities sidecar，不是 `Label`。
4. collect `traces.jsonl` 把 `feature`/`weight_source` 放进 `metadata`。`Trace.from_dict` → **成功**（`record_id=collect-0`，`metadata` 含 `feature`）。
5. `features.npz`（offline）键 `H`/`E`/`token_prefix`，形状 `[1,8]` / `[2,8]` / `[14]`，`float64`。`H[0]=[1,2,…,8]`（字符偏移假 token 前缀）。manifest `array_shapes` **含 dtype**。
6. offline `feature.pre_step.token_index=13`，`expressible=true`（相对字符偏移，不是模型 token）。
7. `RepairRecord` 现有 `schema_version`/`record_id`/`status`；`record_id=repair:task_oracle:q`；`run_id=""`，`base_group_id=""`。
8. 合成 `token_ids = range(1, len(text)+1)`，不是模型 token。

### 3.4 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：`tasks/edits/splits/events/observations/labels/traces/run_spec/manifest` **九文件 hash 全等**。
- 两次 `fit`：`probes.jsonl` hash 全等（双头 `loss=0.05036047880765435`）。这是对 **prefix-id 向量** 的优化，不是隐状态复现。
- `write_run_spec(..., code_revision="latest")` → `ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind` → `ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})` → `ValueError: Out of range float values are not JSON compliant`。
- cwd=`%TEMP%\rd-e-r4b` 调用 `runtime_info()["git_revision"]`：**`46a6e26…`**。
- `packages.reasoning-diff = null`。
- 后段 `run_spec.rng` 仅为 `{"stream": "<stage-jsonl-name>"}`，无 seed、无输入 digest。
- `write_npz` 拒绝 object 数组：`ValueError: object arrays are not allowed: x`。成功后无临时残留。

### 3.5 恢复 / 分片

对照目录：`%TEMP%\rd-e-r4b\`（干净阶段，避免失败 `main` 污染）。

| 检查 | 退出码 | 结果 |
|---|---|---|
| CLI `--resume` | — | help 中存在 |
| CLI `--shard` | **0** | **存在**；与不加 flag 一样写出 `traces-shard-0000.jsonl`，且与 `traces.jsonl` **字节相同**（hash `0d438ea9…`） |
| `completed_shard_ok` 生产调用 | — | `cli.py:336–339`：写出 shard 后立刻用**自己刚算的 hash** assert（恒真）；`--shard` 两分支同形 |
| `--resume` prepare（仅默认参数） | **1** | `ValueError: resume run_spec mismatch: edit_premise`（args=`None` vs 已解析 `p2`） |
| `--resume` prepare `--edit-premise p2 --edit-value 2` | **0** | 文件 hash 不变 |
| `--resume` prepare + 清单 digest 改为 64 个 `0` + 匹配 config | **1** | `resume manifest digest is not self-consistent` |
| `--resume` collect 完整产物 | **1** | `resume run_spec mismatch: command`（检查 `collect`，写出为 `traces`） |
| `--resume` label / fit 完整产物 | **1** | 同上：`label`≠`labels`，`fit`≠`probes` |
| `--resume` + 篡改 `traces.jsonl`（干净 collect） | **1** | `resume hash mismatch or missing file: traces.jsonl`；篡改保留 |
| `--resume` + 删除 shard | **1** | `… traces-shard-0000.jsonl` |
| 上述任一失败之后的 `manifest.json` | — | **被覆盖**为只含 `failure.json` 的失败清单（`success_count=0`, `failure_count=1`）；原 `file_hashes` 丢失 |

`_resume`（`cli.py:34-59`）：有 `--resume` 且存在 `manifest.json` 后，比对 `file_hashes`、可选 `run_spec.config` 键、以及 digest 自洽。hash/digest 失败会抛错。config 比较用的是**调用参数**对**已写出 config**，后段 command 名与 `_write_stage` 的 jsonl 名不一致。

`main` 的 `except`（`cli.py:644-654`）在 `out_dir` 上写 `failure.json` 并 `write_manifest(..., {success:0, failure:1})`，**覆盖**已完成阶段的成功清单。

### 3.6 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 指向不存在文件 | 进程 **1**，`FileNotFoundError` | `failure.json` + 失败 `manifest.json`（`success_count=0`, `failure_count=1`）；无空目录 |
| `label` 无 `--in-dir` | **1** `FileNotFoundError: label requires --in-dir with observations.jsonl` | 失败清单 |
| `fit --split test` | **1** `ValueError: probe fit cannot fit on test; expected ('probe_train',)` | 失败清单 |
| `calibrate --split probe_train` | **1** `ValueError: calibration cannot fit on probe_train; expected ('calibration',)` | 失败清单 |
| `--in-dir docs/SERVER_RUNBOOK.md` + collect | **1** `NotADirectoryError: --in-dir must be a directory`（`_upstream` 先于写 features） | 仅 `failure.json` + 失败清单；**无** `features.npz` / traces |
| 同上 + label / fit | **1** `FileNotFoundError`（缺 observations / features.npz） | 仅失败清单 |
| 同上 + calibrate / intervene / repair | **1** `NotADirectoryError`（`_write_stage` 先 `_upstream`） | 仅失败清单；**无** 阶段 jsonl |
| 同上 + analyze | **1** `NotADirectoryError` | 留下 `report.json`（先写）+ 失败清单 |
| `analyze` 无 `--in-dir`（fixture） | **0** | 完整成功清单；densities=null |
| `read_jsonl` 非法行 | `ValueError('.../bad.jsonl:1: invalid JSON')` | — |
| `IsolatedExecutor().submit(...)` | `status=executor_unavailable`（不再 `NotImplementedError`） | — |
| `@forbid_host_exec` 包装函数 | `RuntimeError('host execution of model/dataset code is forbidden')` | 生产 CLI/评分未使用 |
| `write_manifest(..., {"tasks":10,"edits":3,"failure":0})` | `success_count=0` | **不再**把记录数加总 |
| 同上 + 显式 `"success": 1` | `success_count=1` | 仅用显式键 |
| `calibrate --features-dir <collect>`（offline，n=1） | **1** `ValueError: Out of range float values are not JSON compliant` | 失败清单（`q=inf` / 非有限分数无法 `encode`） |
| `write_npz` object 数组 | 写入前 `ValueError` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits={"timeout":1,"mem":1})` 现把 `limits` 回显进 `ExecutionResult`，仍不执行限额。

### 3.7 `--eval-mode scientific`

| 命令 | 退出码 | 结果 |
|---|---|---|
| `prepare --eval-mode scientific`（无 fractions） | **1** | `scientific mode requires explicit --split-fractions` + failure 清单 |
| `prepare --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15` | **0** | 写出与 fixture 同形的夹具产物 |
| `collect --backend offline --eval-mode scientific` | **1** | `scientific collect refuses offline_prefix_ids as H` |
| `collect --backend tiny --eval-mode scientific` | **0** | 接受 `random_init` 隐状态，不拒绝 |
| `calibrate` runbook 路径 + scientific | **1** | `scientific calibrate refuses loss or literal scores` |
| `analyze` 无 `--in-dir` + scientific | **1** | `scientific analyze requires --in-dir` |
| `analyze --in-dir <label> --eval-mode scientific` | **0** | 仍 `p1=p2=p3=null`，`status=not_evaluated` |

scientific 是门禁开关，不是科学全跑。

### 3.8 隔离执行器

```text
get_executor() / get_executor(None) → UnavailableExecutor
get_executor("spy") → SpyExecutor
get_executor("subprocess") → SubprocessExecutor
score_code(合法源, 测试) 默认：
  status=executor_unavailable, value=None, denominator=None, eligibility=False,
  failure_reason="no isolated backend configured; host exec is forbidden"
SpyExecutor + 源含 "exec("：status=rejected
SubprocessExecutor + 合法 assert：status=ok, value=1.0
SubprocessExecutor + 失败 assert：status=failed, value=0.0
SubprocessExecutor + exec(：status=rejected
SubprocessExecutor + sleep + timeout=0.2：status=timeout
score_numeric("4","4") → value=1.0
score_qa("Paris","paris") → value=1.0
```

全库生产路径未见 `exec(` / `eval(` 作为代码评分回退（仅字符串拒绝）。`forbid_host_exec` 无引用。HumanEval `score_submission` 走 `score_code`。普通 subprocess **不能**冒称 Linux cgroup 沙箱（runbook 仍标 `pending_server`）。

### 3.9 `--kind humaneval`

`prepare --kind humaneval --fixture tests/fixtures/t3_humaneval_one.json` exit **0**。走 T1 `apply_value_edit`：把 spec 前提改成字面 `"2"`，`events.jsonl`/`observations.jsonl` **空**。这不是 HumanEval 评分入口。

### 3.10 atomic NPZ

`write_npz`（`io.py:82-103`）为拒绝 object → `mkstemp` → `np.savez(temp)` → `os.replace`。成功后无 `.feat.npz.*` 残留。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 把 `tests/test_cli_pipeline.py` / 作者「97 passed」当验收 | 夹具烟测与绿测不是科学全跑；`test_pipeline_consumes_upstream` 不断言 input_hashes、Trace 回载或 `--labels-dir` 哈希 |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境；已证实未安装时 `python -m` 需 `PYTHONPATH=src` |
| 真实模型 / GPU / 官方数据下载 | 本机 `pending_server`；夹具烟测不得冒充 |
| 并发真实分片崩溃注入 | `--shard` 不切分任务；现有 shard 是 traces 副本 |
| 阅读本轮 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。编号为本轮 `E4-##`。

---

### E4-01 声称冻结 hash 与当前树一致（closed）

- **状态：** **closed**
- **文件：** `.planning/audits/round-04/VERSION.md`；56 个范围内文件
- **复现 / 证据：** §1。独立复算 = 声称值 `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`。

---

### E4-02 fit 已把 `--labels-dir` 记入 `input_hashes`（closed，原 E-17）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `cmd_fit` 413：`_write_stage(..., extra_dir=labels_dir)`；`_upstream` 62–85
- **复现 / 证据：** §3.2 / §3.2 哈希核对。`fit` 的 `input_hashes` 含 `label/labels.jsonl`（及 label 目录其余文件），字节与 `%TEMP%\rd-e-r4\label\labels.jsonl` **全等**；`upstream_manifest_ids` 含 label digest `106cb1c0…`。
- **残留：** `_upstream` 仍是目录列举，不是实际读取集（collect 哈希 prepare traces 但不读）。不重开空哈希。

---

### E4-03 `Trace.from_dict` 与 Event/Label `record_id` 已可回载（closed，原 E-05 主缺陷；残留见 E4-12）

- **状态：** **closed**（空身份 / collect traces 拒 `feature`）
- **文件 / 符号 / 行号：** `schema.py` `Event.__post_init__` 212–214；`Label.__post_init__` 284–286；`Trace.from_dict` 334–344；`cli.py` 331–332（feature 进 metadata）
- **复现 / 证据：** §3.3。`Trace.from_dict(collect traces[0])` 成功。Event/Label 持久化 `record_id` 非空。编辑 Task `record_id=fix-t1-001::p2=2`。
- **作者「E-05 identities」在「可 from_dict / 非空 record_id」字面范围独立关闭。**

---

### E4-04 失败路径写 `failure.json`；`success_count` 不再加总记录数（closed，原 E-09 记账；覆盖见 E4-08）

- **状态：** **closed**（缺 failure 清单 / 缺省加总）
- **文件 / 符号 / 行号：** `cli.py` `main` 642–654；`artifacts.py` 71
- **复现 / 证据：** 缺夹具、`fit --split test`、文件 `--in-dir` 均写出 `failure.json` 且 `success_count=0`。`write_manifest(..., {tasks:10, edits:3, failure:0})` → `success_count=0`（不再 =13）。

---

### E4-05 `--in-dir` 指向文件时不再留下半截 collect 产物（closed，原 E-16 主缺陷；analyze 残留见 E4-16）

- **状态：** **closed**（collect/fit 半截 features+traces）
- **文件 / 符号 / 行号：** `cli.py` `_upstream` 68–69；`_write_stage` 128 先哈希
- **复现 / 证据：** `--in-dir docs/SERVER_RUNBOOK.md` 的 collect **无** `features.npz` / jsonl；calibrate/intervene/repair 无阶段 jsonl。

---

### E4-06 `--eval-mode scientific` 已挂上门禁（closed 存在性；不是科学全跑）

- **状态：** **closed**（缺 flag）；科学全跑仍 `not_evaluated`
- **文件 / 符号 / 行号：** `cli.py` 181–182、311–312、435–436、530–531、598、609
- **复现 / 证据：** §3.7。offline collect / 无 in-dir analyze / runbook calibrate 在 scientific 下 exit 1。tiny+scientific 仍 exit 0（接受 `random_init`）。
- **影响：** 不能把 scientific 夹具路径当成已测 P1–P3。

---

### E4-07 `python -m reasoning_diff` 与可选 subprocess 执行器（closed；host exec 未破）

- **状态：** **closed**（模块入口 / 默认不回退 host exec / 可选子进程后端存在）
- **文件 / 符号 / 行号：** `__main__.py` 1–4；`executor.py` 55–92；`scoring.py` 19–30
- **复现 / 证据：** §3.1、§3.8。默认 `score_code` 为 `executor_unavailable`。`get_executor("subprocess")` 对合法/失败/exec/超时行为符合契约。Linux cgroup 仍 `pending_server`；普通 subprocess 不得冒称隔离沙箱。

---

### E4-08 失败 `main` 用失败清单覆盖已完成阶段（confirmed defect）

- **严重度：** high
- **状态：** confirmed defect（E-09 关闭后的回归）
- **文件 / 符号 / 行号：** `cli.py` `main` 644–654：`write_manifest(path, [failure.json], {success:0, failure:1})`
- **触发条件：** 对**已有成功** `manifest.json` 的目录再跑失败的 `--resume`（或任何会进 `except` 的命令且 `--out-dir` 相同）。
- **对应要求：** OPS-01「清单、断点与分片」；ARCHITECTURE「重试保留原失败…不在原清单静默覆盖」。
- **复现 / 证据：** §3.5。干净 collect 上 `--resume`（command 不匹配）或篡改 traces 后 `--resume`：原 `file_hashes`（features/traces/run_spec）被替换为只含 `failure.json`。成功产物文件仍在，但调度器无法再凭清单证明它们。
- **影响：** 续跑失败比「只抛错、保留原清单」更差：完成阶段失去可审计 digest。
- **建议：** 失败写到独立 `failure.json` / 旁路清单，或换 `attempt_id` 目录；禁止覆盖已自洽的成功 `manifest.json`。

---

### E4-09 `--resume` 的 run_spec 键与写出 config 对不上，完整产物无法续跑（confirmed defect）

- **严重度：** high
- **状态：** confirmed defect（相对 r03「hash 校验已关」的回归）
- **文件 / 符号 / 行号：**
  - `cli.py` `_resume` 47–52
  - `cli.py` `_write_stage` 137：`config.command = name`（jsonl 名：`traces`/`labels`/`probes`/…）
  - `cli.py` 292 / 354 / 377 / 419：resume 传入 `command=collect|label|fit|calibrate`
  - `cli.py` `cmd_prepare` 171–177：resume config 用未解析的 `args.edit_premise`
- **触发条件：** 对刚成功的 collect/label/fit 加 `--resume`；或对 prepare 只加 `--resume` 不加已解析编辑参数。
- **对应要求：** OPS-01「断点」；ARCHITECTURE「恢复只复用与当前 run spec 一致且校验通过的完成 shard」；SERVER_RUNBOOK「Resume a completed stage with `--resume` if `manifest.json` already exists」。
- **复现 / 证据：** §3.5。完整 collect `--resume` → `command` 不匹配。prepare 默认 `--resume` → `edit_premise` 不匹配。仅当 prepare 显式 `--edit-premise p2 --edit-value 2` 时 resume 才 exit 0。file_hashes 校验本身在干净篡改路径上 **仍然有效**（`traces.jsonl` / 缺 shard）。
- **影响：** runbook 字面「有 manifest 就 resume」对后段全部失败，并触发 E4-08 覆盖清单。hash 校验关不掉这条。
- **建议：** resume 比较的 command 必须与写出值相同；prepare 用已解析 config 或只比较用户显式传入且非 None 的键。

---

### E4-10 runbook calibrate 不消费探针权重；补上 `--features-dir` 后无法持久化（confirmed defect）

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` `cmd_calibrate` 422–441；`probes/calibrate.py` `conformal_threshold` 34–35（`q=math.inf`）；`io.encode` `allow_nan=False`
- **触发条件：** runbook `calibrate --in-dir runs/fit`（无 `--features-dir`）；或 `--features-dir` 指向 offline collect（n=1 分数 → k>n）。
- **对应要求：** OPS-01 校准阶段；ARCHITECTURE「每个命令接收输入 manifest」并消费上游权重。
- **复现 / 证据：** §3.2 `status=probe_weights_or_features_missing`，`scores=null`，exit 0。`--features-dir <collect>` exit **1**，`Out of range float values are not JSON compliant`。scientific 下 runbook 路径 exit 1（拒绝字面量分数）——门禁对，但正确接线仍不能写出。
- **影响：** 八段 exit 0 的校准步是「承认缺特征」，不是校准。补接线会在小 n 上因 `inf` 崩溃。
- **建议：** runbook/默认把 collect 的 features 列入 calibrate 输入；JSON 用 `infinity:true` 且 `q=null`，不要编码 `inf`。

---

### E4-11 `--shard` 存在但是 traces 全量副本（confirmed defect）

- **严重度：** medium
- **状态：** confirmed defect（flag 已出现，语义未落地）
- **文件 / 符号 / 行号：** `cli.py` 334–339、621
- **触发条件：** `collect --shard` 或不加 `--shard`
- **对应要求：** OPS-01「断点与分片」；ARCHITECTURE「shard 完成后原子发布」。
- **复现 / 证据：** §3.5。两种调用都写 `traces-shard-0000.jsonl`，与 `traces.jsonl` 字节相同；`completed_shard_ok` 自校验刚写出的文件。
- **影响：** 长任务仍无按任务/组切分与崩溃恢复。

---

### E4-12 Event `record_id` 跨轨迹碰撞；Label/Repair 身份字段仍空（confirmed defect，E-05 残留）

- **严重度：** medium
- **状态：** confirmed defect（不重开 E4-03 的 from_dict）
- **文件 / 符号 / 行号：** `schema.py` Event 212–214（`record_id=identity.key()`）；`repair.py` 31–35、60；label 写出未填 `run_id`
- **复现 / 证据：** §3.3。两行 Event `record_id` 相同，`unique_record=false`。Label/Repair `run_id=""`、`base_group_id=""`。ARCHITECTURE「记录以 ID 关联，不依赖行号」。
- **影响：** 仅靠 `record_id` 无法区分基线/编辑事件。

---

### E4-13 collect 默认/offline 仍不是可外推的模型采集（confirmed defect，原 E-14 残留）

- **严重度：** medium（tiny 已接线，offline 主跑仍是假 token）
- **状态：** confirmed defect。作者「prefix-id / collect_tiny」**不能**把 offline 烟测关成 MODEL-01。
- **文件 / 符号 / 行号：** `cli.py` 313–330（tiny 调 `collect_tiny`；else 写 prefix ids）；`cli.py` 297–298 仍合成轨迹
- **触发条件：** 本通道指定的 `collect --backend offline`；以及 tiny 对照
- **对应要求：** MODEL-01；OPS-01 采集阶段
- **复现 / 证据：** offline `H[0]=[1..8]`，`weight_source=offline_prefix_ids`。tiny 有 `random_init` 隐状态，但 traces `token_ids` 仍是 `range(1,n)`。fit/intervene（offline）吃假前缀；intervene 因单行 H 为 `donor_missing`。
- **影响：** 主跑八段的后段数字不能外推到权重。

---

### E4-14 T2/T3/T4 未进入与 T1 同等的用户 CLI（confirmed defect，原 E-12 残留）

- **严重度：** medium
- **状态：** confirmed defect（`--kind` 不是域流水线）
- **文件 / 符号 / 行号：** `cli.py` `_load_task` 160–166；`cmd_prepare` 仍走 `_default_edit` + `apply_value_edit`
- **复现 / 证据：** `--help` 仍是八段通用命令。`prepare --kind humaneval` exit 0，但把 spec 改成 `"2"`，events/observations 为空。label/fit/analyze 无 `--kind`。
- **对应要求：** OPS-01 + DATA-02

---

### E4-15 后段「可复现」与 analyze 无 in-dir 仍是夹具复现（confirmed defect，原 E-11 残留）

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 324–330、422–438、525–583
- **复现 / 证据：** prepare 同机可复现（§3.4）。fit 数字稳定因为输入是 prefix-id。analyze 无 `--in-dir` 仍 exit 0。P1–P3 为 null 是正确的「未评估」，**不是** OPS-01 通过。
- **影响：** 不能用后段 hash 证明科学步骤可重放。

---

### E4-16 analyze 在校验 `--in-dir` 之前写 `report.json`（confirmed defect，E-16 残留）

- **严重度：** low
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 582–583 先 `write_json(report)`，再 `_write_stage` → `_upstream`
- **复现 / 证据：** `--in-dir` 文件时留下 `report.json` + 失败清单，无 `analysis.jsonl`。
- **建议：** 先校验目录再写任何阶段文件。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 冻结 hash 复现 | E4-01 closed |
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError` |
| `latest` 拒绝 | `write_run_spec(..., code_revision="latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `ValueError("Unknown source_kind 'made_up'")` |
| JSONL 坏行带路径行号 | `bad.jsonl:1: invalid JSON` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 |
| runbook 目录 `--in-dir` 的文件哈希与上游字节一致 | §3.2 HASH VERIFY 全 True |
| `--labels-dir` 进入 fit `input_hashes` | E4-02 |
| `Trace.from_dict` 回载 collect traces | E4-03 |
| 篡改/缺文件时 `--resume` 拒绝 file_hashes | §3.5 exit 1（在 command 检查之前的 hash 路径） |
| 损坏 digest 自洽检查 | `resume manifest digest is not self-consistent` |
| `require_split` 阻止 test 上 fit、probe_train 上 calibrate | §3.6 |
| 代码评分不回退 host exec | 默认 `executor_unavailable`；subprocess 可选且拒 exec |
| 直接迁移维度拒绝 | `not_applicable_dimension_mismatch` 4096≠3584 |
| Week-8 未注册 | `gate0/1/2.decision=unregistered`，`scientific_conclusion=null`，`skip_p2_p3=true` |
| analyze 不编造 P1–P3 | `p1=p2=p3=null`，`status=not_evaluated` |
| intervene 不编造效应 | offline `donor_missing` / tiny `geometry_on_hidden`，效应字段 null |
| 默认 prepare 不再 4×0 | `p2→2`，`raw_values=["0","8"]` |
| 合成轨迹含前提句 | `"p1 = 4\np2 = 0\nq = 0\n"` |
| `report.json` 进清单 | analyze `file_hashes` 含 report |
| NPZ 原子替换且拒 object | §3.4 / §3.10 |
| `git -C` revision | cwd=TEMP 仍 `46a6e26…` |
| `python -m` 入口 | §3.1 |
| label 拒绝无 `--in-dir` | exit 1 + failure.json |
| `success_count` 缺省 0 | 实验 ≠ 13 |
| 文件 `--in-dir` 不再写 collect 半截产物 | E4-05 |
| scientific 拒绝 offline H / 无 in-dir analyze / 字面量校准 | §3.7 |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |

## 8. 结论

`python -m reasoning_diff` 按指定八段（collect=offline）**全部退出码 0**。这只证明夹具烟测能写文件，**不证明** OPS-01 端到端工程成立，也 **不是** 科学全跑。

相对 round-03，本通道独立关闭：冻结 hash（E4-01）、labels-dir 入哈希（E4-02 / 原 E-17）、Trace 回载与非空 `record_id`（E4-03 / 原 E-05 主缺陷）、failure.json + `success_count` 不再加总（E4-04 / 原 E-09 记账）、文件 `--in-dir` 不再留下 collect 半截产物（E4-05 / 原 E-16 主缺陷）、scientific 门禁存在（E4-06）、`python -m` 与可选 subprocess 且无 host exec（E4-07）。默认编辑、report 进清单、NPZ 原子、`git -C` 保持关闭。tiny 后端现调用 `collect_tiny`。

仍不通过的核心缺陷：失败 resume **覆盖成功清单**（E4-08）、完整产物因 command 键对不上而无法 `--resume`（E4-09）、runbook calibrate 不消费权重且补接线后 JSON 崩（E4-10）、无真实分片（E4-11）、offline 采集仍是 prefix-id（E4-13）、T2–T4 无同等 CLI（E4-14）。Exit 0 不能当作 OPS-01。

**本通道不通过** OPS-01。空通过或「测试绿了」不能作为本通道结论。作者「labels-dir hashed / Trace identities / failure.json / scientific / subprocess」在本通道 **独立关闭其字面范围**；「resume hashes」的 file_hashes 校验仍在，但 **不能**关闭断点续跑合同。

下一步（建议，非本通道实施）：resume 比较与写出相同的 command，且失败不得覆盖成功 manifest；calibrate 默认带上 features 并安全序列化 infinity；offline 明确标非测量，tiny traces 改用模型 token。
