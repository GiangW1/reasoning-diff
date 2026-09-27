# E：端到端工程审查（round-11）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮 A–D/F 通道报告。`ISSUES.md` 作者本地关闭声明不采信，本通道独立复测。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。`ChildProcessExecutor` **不是** `IsolatedExecutor`。

**冻结核验：开审 `HASH_MATCH`；交卷 `HASH_MISMATCH`（窗口内范围内文件被第三方改写）。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 02:27–03:10 +08:00 |
| 声称冻结 hash | `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`（用户给定；与 `.planning/audits/round-11/VERSION.md` 一致；声称 61 文件） |
| 开审独立复算 | **`HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**61** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`。开审 `cli.py` **60749** 字节 / **1251** 行（mtime 1789928313.23）；`tests/test_round07_regressions.py` **8897** 字节 / **200** 行。 |
| 审计脚本收尾复算 | **`HASH_MISMATCH`**。同一脚本仍为 **61** 文件，得到 `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`。`cli.py` 变为 **61130** 字节 / **1254** 行（mtime 1789929009.13）：`cmd_fit` 增加 `elif labels: raise ValueError("fit requires tasks.jsonl …")`；`_find_tasks_jsonl` 向上走 4 层并新增 `collect`/`col`。`tests/test_round07_regressions.py` 变为 **10047** 字节。 |
| 交卷独立复算 | **仍 `HASH_MISMATCH`，且继续漂移。** 写报告前再算为 `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（61 文件）。`test_round07_regressions.py` 再变为 **10192** 字节 / **224** 行。本通道 **未** 改 `src/` / `tests/` / `pyproject.toml`。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；从 `%TEMP%` cwd 调用相同） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch 2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户 CLI 跨模块路径：prepare→collect→label→fit→calibrate→intervene→repair→analyze，夹具 **与** scientific tiny；resume/manifest、`--features-dir`、`--labels-dir`、`--shard`、`--kind` 别名、`--sidecar`、缺 `--in-dir`、NaN JSON、`source_value_pair` / `trace-source`、T3 hotpot / t3_musique、`ChildProcessExecutor.isolated_sandbox`；按 `docs/SERVER_RUNBOOK.md` 本机命令实跑 |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md`、`executor.py` |
| 实跑入口 | `python -m reasoning_diff`（runbook 命令）；产物根 `%TEMP%\rd-e-r11-audit\`，未写入 `src/` / `tests/` / `pyproject.toml` |

**冻结说明：** 声称冻结在开审瞬间可复现。夹具八段、scientific tiny 八段、缺 `--in-dir`、T3 `--kind`、执行器合同均在开审 `7518e20b…` 上启动；`python -m` 每次从磁盘重载，窗口后半 `cli.py` / `test_round07_regressions.py` 被第三方改写。交卷对象是 **当前工作区字节**，与声称冻结 hash **不一致**。后续通道若按 VERSION 声称值对照，会对错树。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 开审 1–1251；交卷 1–1254 | 通读 + `python -m` 夹具八段 + scientific tiny + resume/负路径 + `--kind` + `--sidecar` + `--shard` + 缺 in-dir + NaN + SVP | 八段可调度；collect **复制** `tasks.jsonl`；fit 拒 NaN（scientific）；缺 in-dir 七段均失败；夹具 SVP 的 `trace-source` 为 null；scientific 写出 `trace-source`；T3 `_try` 跳过 SVP；窗口内出现 `fit requires tasks.jsonl` 新门槛 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 通读 + digest / `success_count` / shard | digest 自洽；`success_count` 缺省 0；`completed_shard_ok` 函数正确 |
| `src/reasoning_diff/io.py` | 1–133 | 通读 + NPZ/NaN/`runtime_info` | JSON `allow_nan=False`；拒 object；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | 通读 + `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–51 | 对照实跑 | 含 `--features-dir`；resume 说明与实跑一致；隔离仍 `pending_server` |
| `src/reasoning_diff/executor.py` | 1–109 | `get_executor` / subprocess | 默认 Unavailable；`ChildProcessExecutor.isolated_sandbox=False`；**不是** `IsolatedExecutor`；拒 `exec(`/`eval(` |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–385 | 通读 + 产物 `from_dict` | Event `record_id` 含 `run_id`；`Trace.from_dict` 成功 |
| `src/reasoning_diff/splits.py` | CLI `require_split` | test 上 fit、probe_train 上 calibrate 仍拒绝 |
| `src/reasoning_diff/edits.py` | `make_source_value_pair` / `apply_rename_edit` | 夹具/scientific prepare + T3 kind | T1 可写 SVP；夹具不生成 `trace-source`；T3 `_try` 跳过 |
| `src/reasoning_diff/events.py` | prepare 解析 | 夹具 `parse_fixture_events`；scientific `parse_events` 只吃生成区 |
| `src/reasoning_diff/graphs.py` | prepare `ancestors` / calibrate `R(s_i)` | 无 tasks 则 RSI 空、分数 0 |
| `src/reasoning_diff/measure.py` | `build_labels` / `event_density_sets` | label / prepare | scientific：`noise_ref` 只在 `sham:` 行；`rho_M_excess=null` |
| `src/reasoning_diff/models/collect.py` | 1–261 | tiny collect / 多 mode decode | `pre_idx is None` 跳过该事件；INLP/`add_delta`/`replace`/`pi_z_swap` 分路 |
| `src/reasoning_diff/models/generate.py` | 66–201 | scientific prepare | `parse_region=generated`；约束 `\nq = <digits>`；`trace-source` 文本含 `p2_src` |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | `pre_step` 在 `start=0` 时 `token_index=None` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | collect 重分词 | `encode_text` 按字符 `ord` |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `fit` | 未知/NaN 行掩码；无已知标签则不写 `U`/`V` |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `conformal_threshold` | `k>n` → `q=inf`；CLI `_sanitize_cal` 写成 `q=null` + `infinity=true` |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | 几何与 hook；配对在 CLI `_pair_source_value` / `_expressible_donor` |
| `src/reasoning_diff/repair.py` | CLI `repair` | scientific `k=1..5`；`refilled_prefix` 只认有限 prefill |
| `src/reasoning_diff/analysis.py` | `analyze` | 标签不足 → `p1=null` / `not_evaluated` |
| `src/reasoning_diff/transfer.py` | analyze `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | prepare `--kind` | 别名接通 ≠ 与 T1 同等流水线 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | `--kind` + `--sidecar` | 无 sidecar 仍失败；有 sidecar 可编辑并写 SVP |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | `--kind gsm_plus` | 隔离替换；无 SVP 行 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | `--kind humaneval` | `apply_spec_edit`；无 SVP |
| `src/reasoning_diff/tasks/t3_hotpot.py` | `--kind hotpot` / `t3_hotpot` | 域编辑成功；`_try` 跳过 SVP；**exit 0** |
| `src/reasoning_diff/tasks/t3_musique.py` | `--kind musique` / `t3_musique` | 别名接通；`_try` 跳过 SVP；**exit 0** |
| `src/reasoning_diff/tasks/t4_boundary.py` | `--kind t4` / `t4_boundary` | 两别名 exit 0 |
| `src/reasoning_diff/rng.py` | intervene `StreamBank` | CLI intervene 使用 |
| `src/reasoning_diff/baselines.py` | CLI `fit` | 四档 verbalizer、attention_* |
| `src/reasoning_diff/probes/boundary.py` | CLI fit | `baseline=boundary_mlp` |
| `tests/test_cli_pipeline.py` | 1–30 | 读，未当作验收 | 只断言 exit 0 / `not_evaluated` |

**抽样未做完整工程审查（非本通道主路径）：** `models/tiny.py`、`models/adapters.py`、T1 official 内部、`t2_noop.py`。确认 adapters **未被** 八段通用子命令调用（`cli.py` 无 `adapters` import）。

## 3. 已执行检查与结果

### 3.1 用户 CLI 入口

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`%TEMP%\rd-e-r11-audit`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir`、`--weight-seed` |
| `calibrate --help` | **0** | 有 `--features-dir` **与** `--labels-dir` |
| `fit --help` | **0** | 有 `--labels-dir` |
| `intervene --help` | **0** | 有 `--backend`、`--dev-layer-scores` |
| `label` / `analyze` / `fit` `--help` | **0** | **无** `--kind` |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**；另跑 offline 对照）

产物根：`%TEMP%\rd-e-r11-audit\fx\`。夹具 `tests/fixtures/t1_tiny.json`。`--in-dir` 按 runbook 指向上一阶段。目录名用 runbook 的 `prepare` / `collect` / `label` / `fit` / `cal`。

**跑在开审冻结字节上启动。**

| 命令 | 退出码 |
|---|---|
| `prepare --fixture … --out-dir prepare` | **0** |
| `collect … --in-dir prepare --out-dir collect --backend tiny` | **0** |
| `label --in-dir prepare --out-dir label` | **0** |
| `fit --in-dir collect --labels-dir label --out-dir fit --split probe_train` | **0** |
| `calibrate --in-dir fit --features-dir collect --out-dir cal --split calibration` | **0** |
| `intervene --in-dir collect --out-dir intervene` | **0** |
| `repair --in-dir prepare --out-dir repair --mask task_oracle` | **0** |
| `analyze --in-dir label --out-dir analyze` | **0** |
| `collect … --backend offline --out-dir collect_off` | **0** |

**接线实测：**

| 阶段 | `input_hashes` | `upstream_manifest_ids` | 实际消费 |
|---|---|---|---|
| prepare | `{t1_tiny.json}` | `[]` | 夹具；默认 `p2→2`；另写 `source_value_pair`，**无** `trace-source` |
| collect tiny | prepare 全目录文件 + `upstream_manifest*`（与 prepare 字节 **全等**，HASH VERIFY 全 True） | 重算 prepare digest `8501110a…` | 读 `tasks.jsonl` + `traces.jsonl`；对 `trace.text` **重新** `encode_text`；`weight_source=random_init`；**写出** `tasks.jsonl`（与 prepare **字节全等**，hash `a6ca1a4d…`，进入 collect manifest） |
| label | 哈希 prepare 全目录 | `[8501110a…]` | `observations.jsonl` + `tasks.jsonl`；`build_labels` |
| fit | collect 文件 **加** `label/labels.jsonl` 等（含 `collect/tasks.jsonl`） | collect + label 两枚重算 digest | 读 `H`/`E` + labels-dir；双头探针 + verbalizer/MLP/attention |
| calibrate（`--features-dir collect`） | fit + collect 文件（含 `collect/tasks.jsonl`） | 两枚 digest | `predict_matrix`；认兄弟 `prepare/tasks.jsonl` / collect 副本 → 非空 `scores` |
| intervene | collect | collect digest | `donor_kind=same_source_diff_value`，`donor_rows=[0,1]`，`status=prospective_decode` |
| repair | prepare 全目录 | prepare digest | 默认 backend≠tiny → `prefill_unavailable`；`record_id=repair:fix-t1-001:task_oracle:k1` |
| analyze | label 文件 | label digest | `p1/p2/p3=null`，`status=not_evaluated`；`report.json` 进清单 |

各阶段 `manifest.digest` 均自洽。八个阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。

`collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze` 无 `--in-dir` **全部 exit 1**（§3.7）。

#### 3.2b tiny 对照（夹具 collect）

`collect --backend tiny` exit **0**：`weight_source=random_init`，`H`/`E`/`H_pre_*`/`H_post_step` 均为 `[2,32]`，**0 行 NaN**。`H[0]` 与 `H[1]` **不等**（`maxabs=0.0056705`）。`event_rows`：`q@trace-base`、`q@trace-edit`。**没有** `trace-source` 行。**有** `tasks.jsonl`。

offline collect：`weight_source=offline_prefix_ids`。

#### 3.2c calibrate 目录名 / `--labels-dir` / 祖先目录

runbook 烟测 `fx/cal`（兄弟 `prepare/` + collect 已复制 `tasks.jsonl`）：`scores=[0.00502331, 0.00502337]`，`q=0.00502337`，`status=finite`。`input_hashes` **不含** 任何 labels 文件（含 `--labels-dir` 时亦然）。

| 布局 | `scores` |
|---|---|
| 兄弟 `label/` 且 `premise_id=q`（runbook） | `[0.00502331, 0.00502337]` |
| `--labels-dir othername`（父目录仍有 `label/`） | 同非零（祖先/`label/` 仍可发现） |
| 无 `--features-dir` | `status=probe_weights_or_features_missing`，`scores=null`，fixture 下 exit **0** |

`--labels-dir` 仍 **不** 进入 calibrate `input_hashes`。这是残留观察，不单独升格。

### 3.3 scientific tiny 八段

runbook 局部命令 + 本通道把后段也加上 `--eval-mode scientific`（calibrate/analyze）与 `--backend tiny`（collect/intervene/repair）。`--split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。

**跑在开审冻结字节上启动。**

| 命令 | 退出码 | 要点 |
|---|---|---|
| `prepare --eval-mode scientific --split-fractions … --sham-opportunities 1` | **0** | **7** 条轨迹：`trace-base` / `trace-t0p` / `trace-edit` / **`trace-source`** / 两条 extra / `trace-sham`。文本形如 `p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82`；`trace-source` 为 `p2_src`。`parse_status=constrained_target`；`parse_region=generated`；**7** events（每迹仅 `q`），**4** observations |
| `collect --backend tiny --eval-mode scientific` | **0** | `H`/`H_pre_step` **`[7,32]`**；**0 行 NaN**；`E` `[2,32]` 有限；`event_rows` 含 `trace-source`；**写出** `tasks.jsonl`（与 s-prep 字节全等，进清单） |
| `label` | **0** | 3 行标签 + densities；task ∈ {1,1,0}；behavior 全 null；`noise_ref` **仅** `sham:q=1.0`，真实前提为 null；`rho_M_excess=null`，`null_reason=noise_set_missing` |
| `fit --labels-dir <s-lab> --eval-mode scientific` | **0** | task 头 `loss≈0.050`，`U` **全有限**；behavior 头 `no_known_labels`（无 `U`）；**不是** NaN JSON |
| `calibrate --features-dir <s-col> --eval-mode scientific` | **0** | `scores` 四枚约 `0.005024`，`n_problems=4`，`status=finite` |
| `intervene --backend tiny` | **0** | `donor_kind=same_source_diff_value`，`donor_rows=[0,2]`（`trace-base` vs `trace-edit`，**不是** `trace-source`）；`status=prospective_decode`；`ie_z_g=target_follow`；`transform=pi_z_swap` / `crand=add_delta` / `inlp=inlp` / `rescue=replace`；默认 **无** `clayer_transform`（`clayer_status=dev_scores_missing`） |
| `repair --eval-mode scientific --backend tiny` | **0** | `k=1..5`，`refilled_prefix=true`，`status=ok` |
| `analyze --eval-mode scientific --in-dir <label>` | **0** | `p1=p2=p3=null`，`scientific_conclusion=null`，`status=not_evaluated` |

另：`--dev-layer-scores 0.9 0.1 0.8` → `clayer_status=dev_weak_layer_decode`，`clayer_transform=add_delta`，`weak_layer=1`。四路 decode 仅在该 flag 下齐。

人工注入 NaN 到 scientific `H` 后再 `fit --eval-mode scientific`：exit **1**，`scientific fit refuses NaN hidden rows`，**无** `probes.jsonl`。同一 NPZ + `--eval-mode fixture`：exit **0**。

**exit 0 仍不是 OPS-01**（tiny `random_init`、analyze `not_evaluated`、约束赋值不是自然 CoT、无隔离执行器）。

### 3.4 schema / shape / ID / `source_value_pair` 轨迹

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `review_export.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

Observation（夹具精确一行）：`outcome=changed`，`raw_values=["0","8"]`，`record_id=prepare:{identity}:p2`，`run_id=prepare`，`base_group_id=fix-t1-001`。默认编辑仍为 **p2:0→2**。`edits.jsonl` 第二行 `kind=source_value_pair`，`trace_ids.same_value_diff_source=null`。这是夹具有效扰动，**不是**科学全量扫描。

身份合同（本轮实测）：

1. 夹具 `events.jsonl` 两行 `record_id` 为 `trace-base:{identity}` 与 `trace-edit:{identity}`。scientific 7 行按 `trace-*:{entity}` 区分（仅 `q`），含 `trace-source:{…}`。
2. 两行 Task：`fix-t1-001` 与 `fix-t1-001::p2=2`。
3. prepare Label：`record_id=prepare:q:p2`。label 阶段重写为 `record_id=label:q:p2`。
4. collect `Trace.from_dict` → 成功。
5. tiny 夹具 `H`/`H_pre_*` 均为 `[2,32]`。scientific 均为 `[7,32]`（7 条可表达 `q`，含 source）。`E` `[2,32]`。
6. Repair 夹具：`record_id=repair:fix-t1-001:task_oracle:k1`，`status=prefill_unavailable`。scientific：`k=1..5`，`refilled_prefix=true`。
7. **SVP 轨迹：** 夹具只写元数据、**不**生成 `trace-source`（`same_value_diff_source=null`）。scientific 生成 `trace-source` 且 collect 写入 H 第 4 行（`event_rows` 含该 id），但 intervene donor **固定**走 `same_source_diff_value`（base/edit），不取 source 臂。这与 ISSUES「夹具 prepare 仍可不写 `trace-source`（scientific 写）」一致，**不作为本轮新缺陷重开**。

### 3.5 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：tasks/edits/splits/events/observations/labels/traces/run_spec/manifest **九文件 hash 全等**。
- `write_run_spec(..., code_revision="latest")` → `ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind` → `ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})` → `ValueError`（`allow_nan=False`）。
- cwd=`%TEMP%` 调用 `runtime_info()["git_revision"]`：**`46a6e26…`**。
- `packages.reasoning-diff = null`。
- `write_npz` 拒绝 object 数组。
- `write_manifest(..., {tasks:10, edits:3, failure:0})` → `success_count=0`；显式 `"success": 1` → 1。

### 3.6 恢复 / 分片

| 检查 | 退出码 | 结果 |
|---|---|---|
| `--resume` prepare（仅默认参数） | **0** | 解析后的 `p2`/`2` 与已写 config 一致 |
| `--resume` prepare `--edit-premise p2 --edit-value 2` | **0** | 文件不变 |
| `--resume` collect / label / fit / calibrate / intervene / repair / analyze（完整产物） | **0** | `command` 键与写出值一致；`success_count` 仍为 1 |
| `--resume` + 篡改 `traces.jsonl` | **1** | `resume hash mismatch or missing file: traces.jsonl` |
| 上述失败后的 `manifest.json` | — | **`file_hashes` 原样保留**；`success_count=1`；另写 `failure.json`；`digest` 不变 |
| `--resume` + 清单 digest 改为 64 个 `0` | **1** | `resume manifest digest is not self-consistent` |
| `--shard` | **0** | `traces-shard-0000.jsonl`、`0001.jsonl` **各 1 行** |
| 不加 `--shard` | **0** | **无** shard 文件 |

`main` 的 `except` 仍写 `failure.json`；若已有 `success_count`，**不再**覆盖成功清单。

### 3.7 异常 / 资源 / 缺 `--in-dir` / NaN JSON

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 不存在 | **1** `FileNotFoundError` | `failure.json` + 失败清单 |
| `collect` 无 `--in-dir` | **1** `collect requires --in-dir` | `success_count=0` |
| `label` 无 `--in-dir` | **1** `label requires --in-dir with observations.jsonl` | 失败清单 |
| `fit` 无 `--in-dir` | **1** `fit requires --in-dir` | 失败清单 |
| `calibrate` 无 `--in-dir`（fixture **与** scientific） | **1** `calibrate requires --in-dir` | 失败清单 |
| `intervene` 无 `--in-dir` | **1** `intervene requires --in-dir` | 失败清单 |
| `repair` 无 `--in-dir` | **1** `repair requires --in-dir` | 失败清单 |
| `analyze` 无 `--in-dir`（fixture **与** scientific） | **1** `analyze requires --in-dir` | **无** `report.json` |
| `fit --split test` | **1** `probe fit cannot fit on test` | 失败清单 |
| `calibrate --split probe_train` | **1** `calibration cannot fit on probe_train` | 失败清单 |
| `--in-dir docs/SERVER_RUNBOOK.md` + collect / calibrate / intervene / repair / analyze | **1** `NotADirectoryError` | 仅失败清单；**无** features / `report.json` |
| scientific `H` 注入 NaN 后 fit | **1** `scientific fit refuses NaN hidden rows` | **无** `probes.jsonl` |
| 同上 + `--eval-mode fixture` | **0** | 丢弃非有限行后写出 probes |
| `write_npz` object | 写入前 `ValueError` | — |
| `encode(nan)` | `ValueError` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits=…)` 回显 `limits`，不执行限额。

### 3.8 `--eval-mode scientific` 门禁

| 命令 | 退出码 | 结果 |
|---|---|---|
| `prepare --eval-mode scientific`（无 fractions） | **1** | `scientific mode requires explicit --split-fractions` |
| `collect --backend offline --eval-mode scientific` | **1** | `scientific collect refuses offline_prefix_ids as H` |
| `collect --backend tiny --eval-mode scientific` | **0** | 接受 `random_init`；本跑 H 无 NaN |
| `calibrate` 无 probes + scientific | **1** | `scientific calibrate refuses loss or literal scores` |
| `analyze` 无 `--in-dir` + scientific | **1** | `analyze requires --in-dir` |
| 完整 scientific 八段 | **全 0** | 见 §3.3。**不是**科学全跑 |

scientific 是门禁开关，不是科学全跑。

### 3.9 隔离执行器

```text
get_executor() / get_executor(None) → UnavailableExecutor
get_executor("spy") → SpyExecutor
get_executor("subprocess"|"child_process") → ChildProcessExecutor
ChildProcessExecutor.isolated_sandbox = False
IsolatedExecutor.isolated_sandbox = True，submit → executor_unavailable
isinstance(ChildProcessExecutor(), IsolatedExecutor) is False
score_code 默认：status=executor_unavailable
SpyExecutor + exec(：rejected
SubprocessExecutor + 合法 assert：ok
SubprocessExecutor + 失败 assert：failed
SubprocessExecutor + exec( / eval(：rejected
SubprocessExecutor + sleep + timeout=0.2：timeout
score_numeric("4","4") → value=1.0；score_qa("Paris","paris") → value=1.0
@forbid_host_exec → RuntimeError('host execution of model/dataset code is forbidden')
```

生产路径未见 `exec(` / `eval(` 作为评分回退（`repair.py` 的 `model.eval()` 是 PyTorch eval 模式，不是 Python `eval(`）。普通 subprocess **不能**冒称 Linux cgroup 沙箱。`ChildProcessExecutor` **不是** `IsolatedExecutor`。

### 3.10 T2–T4 `--kind`

| `--kind` | 退出码 | 编辑器 / SVP | 备注 |
|---|---|---|---|
| `hotpot` / `t3_hotpot` | **0** | `document` | `_try` 跳过 SVP；无 `trace-source`；0 events |
| `musique` / `t3_musique` | **0** | `paragraph` | 无 SVP；4 events |
| `humaneval` / `t3_humaneval` | **0** | `input_list` / `# variant` | 无 SVP |
| `gsm_plus` / `t2_gsm_plus` | **0** | `plus_numeric` `4→5` | **无** SVP 行；无 `trace-source` |
| `gsm_symbolic` / `t2_gsm_symbolic` / `symbolic` | **1** | 别名能进 catalog；无 sidecar | `no editable non-placeholder premise` |
| `gsm_symbolic` + `--sidecar` | **0** | `value` + `source_value_pair` | SVP 的 `same_value_diff_source=null`；无 `trace-source` |
| `t4` / `t4_boundary` | **0** | `t4_question` | 无 SVP |

用户指定猎取：`hotpot` 与 `t3_musique` prepare **均为 exit 0**。作者 E7-19「`_try_source_value_pair` 跳过 T3」字面 **独立确认**。这不是与 T1 同等的域流水线：label / fit / analyze **无** `--kind`。

### 3.11 atomic NPZ

`write_npz`：拒 object → `mkstemp` → `np.savez` → `os.replace`。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 把 pytest / 作者「155 passed」当验收 | 夹具绿测不是科学全跑，也不是 OPS-01 |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境 |
| 真实模型 / GPU / 官方数据 | `pending_server` |
| 并发真实分片崩溃注入 | `--shard` 现为每轨迹一份副本，不是按组调度 |
| 阅读本轮 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |
| 在声称冻结字节上重跑交卷 kinds 之后的 `fit requires tasks.jsonl` 新门槛 | 该门槛是窗口内第三方写入，不在 `7518e20b…` 开审快照上 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。编号为本轮 `E11-##`。

---

### E11-01 声称冻结 hash 与交卷树不一致（confirmed defect）

- **严重度：** high（审查对象合同）
- **状态：** confirmed defect
- **文件：** `.planning/audits/round-11/VERSION.md`；`src/reasoning_diff/cli.py`；`tests/test_round07_regressions.py`
- **复现 / 证据：** §1。开审复算 = 声称值 `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`（61 文件）。审计收尾 = `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`。写报告前再算 = `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。`cli.py` 开审 1251 行 / 60749 字节 → 1254 行 / 61130 字节（`fit requires tasks.jsonl`；`_find_tasks_jsonl` 上溯 4 层 + `collect`/`col`）。`test_round07_regressions.py` 开审 8897 → 审计收尾 10047 → 交卷 10192 字节。本通道未写这些文件。
- **影响：** 独立审查无法把全部结论钉在声称冻结上。夹具/scientific 八段与缺 `--in-dir`/T3 kinds 绑开审快照；交卷树已含未在冻结上复测的 fit 新门槛。后续通道若按 VERSION 声称值对照，会对错树。
- **建议：** 冻结后禁止改范围内文件；改完必须重写 VERSION 并重开 A–F。

---

### E11-02 collect 写出 `tasks.jsonl`（closed，原 C6-M-01 residual / 本轮指定猎取）

- **状态：** **closed**
- **复现 / 证据：** §3.2。夹具 collect 目录含 `tasks.jsonl`，与 prepare **字节全等**（hash `a6ca1a4d…`），进入 `manifest.file_hashes`。scientific collect 同样复制且进清单。fit `input_hashes` 含 `collect/tasks.jsonl`。

---

### E11-03 T3 `hotpot` / `t3_musique` prepare 退出 0（closed，原 E7-19）

- **状态：** **closed**（字面猎取）
- **复现 / 证据：** §3.10。`hotpot` / `t3_hotpot` / `musique` / `t3_musique` 均为 exit **0**；编辑器分别为 `document` / `paragraph`；`_try_source_value_pair` 跳过，无 SVP、无 `trace-source`。
- **对作者 E7-19：** 「跳过 T3 以免崩溃」字面 **独立确认**。不能把「prepare exit 0」写成与 T1 同等 CLI 或 CAUSAL-02 已接线。

---

### E11-04 失败 `main` 不再覆盖成功清单（closed，原 E7-02 / E9-02）

- **状态：** **closed**
- **复现 / 证据：** §3.6。篡改 traces 后 `--resume`：写出 `failure.json`，`manifest.file_hashes` / `success_count=1` / `digest` 与失败前 **全等**。

---

### E11-05 `--resume` 的 command 键与写出 config 对齐（closed，原 E7-03）

- **状态：** **closed**
- **复现 / 证据：** §3.6。prepare 默认 `--resume` 以及后七段完整产物 `--resume` **全部 exit 0**。

---

### E11-06 `--features-dir` 可消费权重；infinity 可 JSON（closed，原 E7-04）

- **状态：** **closed**
- **复现 / 证据：** §3.2 / §3.2c。`--features-dir` 进入 `predict_matrix`。无 features：`scores=null`，`status=probe_weights_or_features_missing`。

---

### E11-07 `--shard` 按轨迹各写一份（closed，原 E7-05）

- **状态：** **closed**
- **复现 / 证据：** §3.6。`--shard` → 两个 1 行 shard；不加 flag → 无 shard 文件。

---

### E11-08 Event/Label `record_id` 含 `run_id` 且跨轨迹不碰撞（closed，原 E7-06）

- **状态：** **closed**
- **复现 / 证据：** §3.4。夹具 2 条、scientific 7 条 Event `record_id` 互异，含 `trace-source`。

---

### E11-09 analyze 在写 `report.json` 之前拒绝文件 `--in-dir`（closed，原 E7-07）

- **状态：** **closed**
- **复现 / 证据：** §3.7。fixture 与 scientific 的文件 `--in-dir` 均 **无** `report.json`。

---

### E11-10 `--eval-mode scientific` 门禁仍在（closed 存在性；不是科学全跑）

- **状态：** **closed**（缺 flag）
- **复现 / 证据：** §3.8。offline collect / 无 fractions / 无 features 的 scientific calibrate 均 exit 1。

---

### E11-11 scientific tiny 用户 CLI 不再因 NaN JSON 在 fit 处断裂（closed，原 E7-09；**不是** OPS-01）

- **状态：** **closed**（「拒 NaN H / 不写 NaN 权重」字面）
- **复现 / 证据：** §3.3。7 events、H `[7,32]` 全有限、0 NaN 行。fit exit 0，probes 可 JSON，task `U` 有限。强制 NaN 行 → `scientific fit refuses NaN hidden rows`，不写 `probes.jsonl`。
- **不能**把「tiny 八段 exit 0」写成 OPS-01。

---

### E11-12 collect / label / analyze / 后四段无 `--in-dir` 必须失败（closed，原 E7-14 / E7-17；本轮指定猎取）

- **状态：** **closed**
- **复现 / 证据：** §3.7。七段均 exit 1，`success_count=0`；analyze 不写 `report.json`。scientific calibrate / analyze 无 in-dir 同样先报 `requires --in-dir`。

---

### E11-13 Repair `record_id` 含 `base_group_id` 与 `k`（closed，原 E7-15）

- **状态：** **closed**
- **复现 / 证据：** §3.4。夹具 `repair:fix-t1-001:task_oracle:k1`；scientific `k1..k5`。

---

### E11-14 scientific intervene 不再把有限 H 当成无 donor（closed，原 E7-18）

- **状态：** **closed**
- **复现 / 证据：** §3.3。scientific `H` 7 行全有限；按 SVP `trace-base`/`trace-edit` 配对 → `same_source_diff_value` / `prospective_decode` / `timing=offline_hidden`。**不是** `donor_missing`。donor **不是** `trace-source`。`ie_z_g=target_follow`。

---

### E11-15 `ChildProcessExecutor.isolated_sandbox is False`（closed 合同；本轮指定猎取）

- **状态：** **closed**（存在性）
- **复现 / 证据：** §3.9。`ChildProcessExecutor.isolated_sandbox is False`；`isinstance(..., IsolatedExecutor) is False`。默认 `score_code` 为 `executor_unavailable`。这 **满足**「不得冒称沙箱」合同，**不满足** OPS-01「代码任务用隔离执行器评分」。

---

### E11-16 夹具 SVP 可省略 `trace-source`；scientific 必须有（closed 合同；本轮指定猎取）

- **状态：** **closed**（与 ISSUES / 本轮指令一致；**不是** OPS-01）
- **复现 / 证据：** §3.2 / §3.3 / §3.4。夹具 `edits.jsonl` 有 SVP，但 `same_value_diff_source=null`，traces 仅 `trace-base`/`trace-edit`。scientific：7 条轨迹、SVP 指向 `trace-source`、collect `event_rows` 含该 id。intervene 两侧都走 value 臂。sidecar GSM-Symbolic 同样 `same_value_diff_source=null`。
- **不重开** E9-19：本轮指令与 ISSUES 明确允许夹具省略。T3 用户 CLI 仍无来源臂，见 E11-17。

---

### E11-17 T2/T3/T4 `--kind` 仍不是与 T1 同等的用户 CLI（confirmed defect，原 E7-13 / E9-13）

- **严重度：** medium
- **状态：** confirmed defect（部分别名 **不能**关闭整条）
- **复现 / 证据：** §3.10。`t3_hotpot` / `t3_musique` / hotpot / humaneval / t4 字面 exit 0；`gsm_symbolic` 无 sidecar 仍 exit 1；有 `--sidecar` 则 exit 0 并写 SVP（source 臂仍 null）。label/fit/analyze 无 `--kind`。
- **对应要求：** OPS-01 + DATA-02
- **对作者 E7-19 / E6-13：** 「T3 prepare 不崩」与「别名 + sidecar」字面 **部分确认**；「与 T1 同等用户 CLI」**不能关闭**。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 开审冻结可复现 | 开审 **HASH_MATCH** `7518e20b…`；交卷漂移见 E11-01 |
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError` |
| `latest` 拒绝 | `write_run_spec(..., "latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `Unknown source_kind 'made_up'` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 |
| runbook 目录 `--in-dir` 文件哈希与上游字节一致 | §3.2 HASH VERIFY 全 True |
| `--labels-dir` 进入 **fit** `input_hashes` | §3.2 |
| collect 复制 `tasks.jsonl` | E11-02 |
| `Trace.from_dict` 回载 | §3.4 |
| 完整产物 `--resume` 成功 | §3.6 八段 exit 0 |
| 篡改时 `--resume` 拒绝且 **不覆盖** 成功清单 | E11-04 / E11-05 |
| 损坏 digest 自洽检查 | `resume manifest digest is not self-consistent` |
| `require_split` | §3.7 |
| 代码评分不回退 host exec | 默认 `executor_unavailable`；`ChildProcessExecutor.isolated_sandbox is False` |
| 直接迁移维度拒绝 | `not_applicable_dimension_mismatch` 4096≠3584 |
| Week-8 未注册 | `gate0/1/2.decision=unregistered`，`scientific_conclusion=null`，`skip_p2_p3=true` |
| analyze 不编造 P1–P3 | `p1=p2=p3=null`，`status=not_evaluated` |
| 默认 prepare 不再 4×0 | `p2→2`，`raw_values=["0","8"]` |
| `report.json` 进清单 | analyze `file_hashes` 含 report |
| NPZ 原子替换且拒 object | §3.5 / §3.11 |
| `git -C` revision | cwd=TEMP 仍 `46a6e26…` |
| `python -m` 入口 | §3.1 |
| `success_count` 缺省 0 | 实验 ≠ 13 |
| 文件 `--in-dir` 不留半截 collect / 不先写 report | E11-09 |
| scientific 拒绝 offline H / 无 fractions / 字面量校准 | §3.8 |
| 七段缺 in-dir 失败 | E11-12 |
| tiny 重分词 + `H_pre` 堆叠 | 夹具 `[2,32]`；scientific `[7,32]` |
| repair `record_id` 含 group 与 k | E11-13 |
| scientific prepare 非空生成区事件 | 7 events；`parse_region=generated` |
| scientific fit 有限 probes | E11-11 |
| scientific intervene 有 donor | E11-14 |
| scientific 生成 `trace-source` | §3.3 / §3.4 / E11-16 |
| 夹具可省略 `trace-source` | E11-16 |
| `ie_z` 标注 `target_follow` | §3.3 |
| INLP / C-rand / rescue 分路 decode | `inlp` / `add_delta` / `replace`；C-layer 需 `--dev-layer-scores` |
| `--sidecar` 接通 GSM-Symbolic | §3.10 |
| T3 prepare 不因 SVP 崩溃 | E11-03 |
| `ChildProcessExecutor is not IsolatedExecutor` | §3.9 / E11-15 |
| adapters 未被八段调用 | `cli.py` 无 import |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径。`ChildProcessExecutor` 不是沙箱 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |
| 声称冻结 `7518e20b…` 的原始 61 文件字节 | 已被覆盖；窗口内继续漂移到 `0816fa5b…` |

## 8. 结论

**开审 `HASH_MATCH`，交卷 `HASH_MISMATCH`。** 声称 `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`（61 文件）在开审可复现；审计收尾为 `598e6c8f…`；写报告前为 `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。冻结未守住（E11-01）。

本轮指定猎取（开审冻结上启动）结果：

| 猎取项 | 结果 |
|---|---|
| 夹具八段 | **全部 exit 0**（collect=tiny） |
| scientific tiny 八段 | **全部 exit 0** |
| collect 含 `tasks.jsonl` | **是**；夹具与 scientific 均与 prepare 字节全等并进清单 |
| T3 `hotpot` / `t3_musique` prepare | **exit 0** |
| 缺 `--in-dir` | 七段 **全部 exit 1**；analyze 不写 `report.json` |
| `ChildProcessExecutor.isolated_sandbox` | **`False`**；不是 `IsolatedExecutor` |
| 夹具 SVP / scientific `trace-source` | 夹具 **省略**；scientific **有** |
| `exit 0` 是否 OPS-01 | **不是** |

夹具烟测按 runbook 八段 **全部退出码 0**。scientific tiny 按同一用户顺序：**八段全部退出码 0**。fit 写出无 NaN 的 `probes.jsonl`。这只证明 tiny 夹具/约束接口能写文件，**不证明** OPS-01，也 **不是** 科学全跑。

仍不通过的核心项：声称冻结与交卷树不一致（E11-01）；T2/T3 不是与 T1 同等用户 CLI（E11-17）；隔离执行器未交付（E11-15）；tiny `random_init` + `not_evaluated` 不能登记为 OPS-01。Exit 0 不能当作 OPS-01。`ChildProcessExecutor` 不能当作 `IsolatedExecutor`。

作者对 E7-19（T3 prepare 不崩）、C6-M-01 residual（collect 复制 `tasks.jsonl`）、缺 `--in-dir`、夹具可省略 `trace-source` 的字面关闭在开审字节 **独立确认**。E6-13 / E7-13 的「同等 CLI」**不能关闭**。

**本通道不通过** OPS-01。**FAIL**。空通过或「测试绿了」或「tiny 八段 exit 0」不能作为本通道结论。

下一步（建议，非本通道实施）：重新冻结并重开审查；不要把 tiny exit 0 登记为 OPS-01。
