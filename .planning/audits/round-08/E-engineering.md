# E：端到端工程审查（round-08）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮 A–D/F 通道报告。`ISSUES.md` 作者本地关闭声明（E6-09 / E6-13 / E6-16 / E6-17 / E6-18）已独立复测，不采信作者关闭声明。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。

**冻结核验：审查开始 `HASH_MATCH`；写报告前 `HASH_MISMATCH`（工作区在实跑后漂移）。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 02:06–03:10 +08:00 |
| 声称冻结 hash | `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`（用户给定；与 `.planning/audits/round-08/VERSION.md` 一致） |
| 独立复算（审查开始，实跑所绑定） | **`HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**60** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`。当时 `cli.py` **1164** 行、`models/collect.py` **199** 行。 |
| 独立复算（写报告前） | **`HASH_MISMATCH`**。同一脚本现得 `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（仍 60 文件）。相对开始时行数：`cli.py` 1164→**1241**，`models/collect.py` 199→**261**。其余抽样行数未变。本通道 **未** 在漂移后重跑八段。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；从 `%TEMP%` cwd 调用相同） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch 2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户 CLI：夹具八段 **与** scientific tiny prepare→collect→label→fit→calibrate→intervene→repair→analyze；猎 NaN JSON fit、缺 `--in-dir`、`prepare/` 祖先、`--kind` 别名；resume/shard/文件 in-dir |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md` |
| 实跑入口 | `python -m reasoning_diff`；产物根 `%TEMP%\rd-e-r8-k7m2q9xp\`，未写入 `src/` / `tests/` / `pyproject.toml` |

**冻结说明：** 下列 CLI 证据绑定审查开始时与声称值一致的快照 `1b88bec…`。写报告时工作区已不再是该字节。不能把当前树当成同一冻结。

## 2. 逐文件覆盖

行号为 **实跑快照**（`cli.py` 1164 / `collect.py` 199），不是漂移后的 1241 / 261。

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–1164 | 通读 + `python -m` 夹具八段 + scientific tiny + 负路径 + `--kind` + `--shard` + 缺 in-dir | 八段可调度；scientific fit 不再因 NaN JSON 断；calibrate 认 `prepare/`/`prep/`/`s-prep/`；缺 in-dir 七段皆失败；T3 prepare 被无条件 `source_value_pair` 打断 |
| `src/reasoning_diff/artifacts.py` | 1–85 | digest / `success_count` / shard | digest 自洽；缺 `success` 键 → `success_count=0`；显式 `success=1` → 1 |
| `src/reasoning_diff/io.py` | 1–133 | NPZ/NaN/`runtime_info` | JSON `allow_nan=False`；拒 object；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–51 | 对照实跑 | `--features-dir` 与 resume 说明与实跑一致；隔离仍 `pending_server`；目录名 `prepare`/`s-prep` 现被代码认 |
| `src/reasoning_diff/executor.py` | 1–109 | `get_executor` / subprocess | 默认 Unavailable；`ChildProcessExecutor.isolated_sandbox=False`；拒 `exec(`/`eval(` |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–385 | 产物 `from_dict` | Event `record_id` 含 run/trace；`Trace.from_dict` 回载 |
| `src/reasoning_diff/splits.py` | 1–111 | CLI `require_split` | test 上 fit、probe_train 上 calibrate 拒绝 |
| `src/reasoning_diff/edits.py` | 1–277 | 默认 prepare `p2→2` + `make_source_value_pair` | T1 重算答案 8 并写入 pair；T3 无条件 pair 使 hotpot/musique prepare 失败 |
| `src/reasoning_diff/events.py` | 1–260 | prepare 解析 | 夹具 `parse_fixture_events`（节点）；scientific `parse_events` 仅生成区 |
| `src/reasoning_diff/graphs.py` | 1–46 | `ancestors` | `composition_reference` / `supporting_facts_only` 返回 `{}` |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 observation 则无任务/行为标签 |
| `src/reasoning_diff/models/collect.py` | 1–199 | tiny collect | `pre_idx is None` 的事件 **跳过**，不再写入 NaN `H` 行 |
| `src/reasoning_diff/models/generate.py` | 72–180 | scientific prepare | 约束追加 `\nq = <digits>`；`parse_status=constrained_target` |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | `start=0` 的 `pre_step` → `token_index=None` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | collect 重分词 | `encode_text` 按字符 `ord` |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `fit` | 掩码未知/NaN 行；`U`/`V`/`b` 有限可 JSON；全 NaN → `no_known_labels` |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `conformal_threshold` | `k>n` → `q=inf`；CLI `_sanitize_cal` 写成 `q=null` + `infinity=true` |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | CLI 先用 `_expressible_donor` 配对有限同行 |
| `src/reasoning_diff/repair.py` | 1–223 | `repair` | scientific `k=1..5` 且 `refilled_prefix=true` |
| `src/reasoning_diff/analysis.py` | 1–337 | `analyze` | 标签不足双类 → `p1=null` / `not_evaluated` |
| `src/reasoning_diff/transfer.py` | 1–75 | `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | `--kind` | `t3_musique` / `t4_boundary` 别名存在；不再 `unknown snapshot kind` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–84 | `--kind` + `--sidecar` | 有 sidecar 可 prepare；无 sidecar 仍失败 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 50–76 | `--kind gsm_plus` / `t2_gsm_plus` | `"4"→"5"` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–78 | `--kind humaneval` / `t3_humaneval` | 追加 `# variant` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 51–104 | `--kind hotpot` | `document_edit` 本身可构造；CLI 随后 `make_source_value_pair` 失败 |
| `src/reasoning_diff/tasks/t3_musique.py` | 10–110 | `--kind musique` / `t3_musique` | 别名接通；`expression=composition_reference` 被 `recompute` 当公式 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 36–51 | `--kind t4` / `t4_boundary` | 问句追加 ` ?` |
| `src/reasoning_diff/rng.py` | 1–53 | intervene `StreamBank` | CLI intervene 使用 |
| `src/reasoning_diff/baselines.py` | 1–125 | CLI `fit` | 四档 verbalizer、attention_* |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | CLI fit | `baseline=boundary_mlp` |
| `tests/test_cli_pipeline.py` | — | 读，未当作验收 | 绿测不是 OPS-01 |

**抽样未做完整工程审查：** `models/tiny.py`、`models/adapters.py`、T1 official 内部、`t2_noop.py`。adapters **未被** 八段通用子命令调用。

## 3. 已执行检查与结果

### 3.1 用户 CLI 入口

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`%TEMP%`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir`、`--weight-seed` |
| `calibrate --help` | **0** | `--features-dir` **与** `--labels-dir` |
| `fit --help` | **0** | `--labels-dir` |
| `prepare --help` | **0** | `--sidecar`、`--kind`、`--split-fractions` |
| `label` / `fit` / `analyze --help` | **0** | **无** `--kind` |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**；另跑 offline 对照）

产物根：`%TEMP%\rd-e-r8-k7m2q9xp\fx\`。夹具 `tests/fixtures/t1_tiny.json`。目录名用 runbook 的 `prepare` / `collect` / `label` / `fit` / `cal`。

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
| prepare | `{t1_tiny.json: …}` | `[]` | 夹具；默认 `p2→2`；`edits.jsonl` 另有 `source_value_pair` |
| collect tiny | prepare 全目录文件（HASH VERIFY 全 True） | 重算 prepare digest | `tasks.jsonl` + `traces.jsonl`；`encode_text(trace.text)`；`event_rows.jsonl` 两行 `q`；`weight_source=random_init` |
| label | 哈希 prepare 全目录 | prepare digest | `observations.jsonl` + `tasks.jsonl` |
| fit | collect **加** `label/labels.jsonl` 等 | collect + label 两枚 digest | `H`/`E` + labels-dir；双头探针 + verbalizer/MLP/attention |
| calibrate（`--features-dir collect`） | fit + collect 文件 | 两枚 digest | `predict_matrix`；祖先读到兄弟 `prepare/tasks.jsonl` → **非空** RSI |
| intervene | collect | collect digest | 有限且不等的两行 `q` → `prospective_decode`，几何 `timing=offline_hidden` |
| repair | prepare 全目录 | prepare digest | 默认 backend≠tiny → `prefill_unavailable`；`record_id=repair:fix-t1-001:task_oracle:k1` |
| analyze | label 文件 | label digest | `report.json` 进清单；`p1/p2/p3=null`，`status=not_evaluated` |

各阶段 `manifest.digest` 均自洽。八个阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。

夹具 calibrate：`scores=[0.00502403, 0.00502409]`，`q=0.00502409`，`status=finite`。**不是** r06 的空真理 `[0,0]`。`input_hashes` **仍不含** labels / `prepare/tasks.jsonl`。

#### 3.2b tiny / offline 对照

`collect --backend tiny`：`H`/`H_pre_*`/`H_post_step` 均为 `[2,32]`，**全部有限**，`nan_rows=0`。`H[0]≠H[1]`（`maxabs=0.0056705`）。`event_rows`：`(trace-base,q)` / `(trace-edit,q)`。`intervene`：`status=prospective_decode`，`donor_rows=[0,1]`，`timing=offline_hidden`，`hook_timing=pre_step`（只在 relative 里），`invalid=1.0`。

offline collect：`H` `[1,8]`，`weight_source=offline_prefix_ids`。offline fit+calibrate：`n=1`，`k=2`，`q=null`，`infinity=true`，JSON 可写。tiny-fit（32 维）配 offline 特征（8 维）→ `matmul` 维度错误 exit 1。

#### 3.2c calibrate 祖先 / `--labels-dir` / `event_rows`

同一套夹具 fit/collect，只改兄弟目录：

| 布局 | `scores` / `q` |
|---|---|
| 兄弟 `prepare/tasks.jsonl` + `label/`（runbook 名） | `[0.00502403, 0.00502409]`，`q=0.00502409` |
| 兄弟 `prep/tasks.jsonl` + `label/` | 同上 |
| 兄弟 `s-prep/tasks.jsonl` + `label/` | 同上 |
| 仅 `label/`（无 tasks 祖先） | `[0.0, 0.0]`，`q=0.0`（空真理） |
| 仅 `othername/labels.jsonl`（无 flag、无 tasks） | `[0.0, 0.0]` |
| `--labels-dir othername`（真实 `p2` 标签、无 tasks） | `[0.0, 0.0]`（找到标签仍可空 RSI） |
| 仅 `label/` 且把 `premise_id` 改成 `q`（无 tasks） | `[0.00502325, 0.00502334]`（`nid=q` 自身命中） |
| 有 `prepare/`，强制改 `event_rows.node_id=p2` | 与 runbook 相同非零分 |
| 有 `prepare/`，删除 `event_rows.jsonl`（回退 traces） | 同上非零分 |
| 无 `--features-dir` | `scores=null`，`status=probe_weights_or_features_missing`，fixture 下 exit **0** |

**E6-16 目录名：** `prepare/` 与 `s-prep/` **独立确认可读**。无祖先 tasks 时，runbook 真实 `p2` 标签仍走空真理——这是「无图则 RSI={nid}」而不是「不认目录」。`event_rows` 优先在代码里先读该文件（`cli.py` 721–726）；本轮有 `prepare/` 时两种来源分数相同，**不能**用分数差单独证明优先。

### 3.3 scientific tiny 八段

runbook 局部命令 + 后段加 `--eval-mode scientific`（calibrate/analyze）与 `--backend tiny`（collect/intervene/repair）。`--split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。目录：`s-prep` / `s-col` / `s-lab` / `s-fit` / `s-cal` / `s-iv` / `s-rep` / `s-ana`。

| 命令 | 退出码 | 要点 |
|---|---|---|
| `prepare --eval-mode scientific --split-fractions … --sham-opportunities 1` | **0** | 6 条 `tiny-qwen2`；文本形如 `p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82`；**6** events（每迹仅 `q`，`start=45`）；`parse_status=constrained_target`；4 obs；prepare 标签 3 行（p2/p1/`sham:q`） |
| `collect --backend tiny --eval-mode scientific` | **0** | `H`/`H_pre_*` **`[6,32]` 全有限**，`nan_rows=0`；`E` `[2,32]` 有限；`event_rows` 6 行皆 `node_id=q`、不同 `trace_id` |
| `label` | **0** | 3 行已知字段；`behavior_label` 全 `null`；`task_label` ∈ {0,1} |
| `fit --labels-dir <s-lab> --eval-mode scientific` | **0** | **不再** `Out of range float values are not JSON compliant`。task 头 `U`/`V`/`b` **有限**，`loss=0.05035974`。behavior 头 `status=no_known_labels`（无 0/1 行为标签，无 `U`） |
| `calibrate --features-dir <s-col> --eval-mode scientific` | **0** | 用带 `U` 的 task 头；`scores` 三个非零 `one_minus_p`，`q=0.00502359`，`status=finite` |
| `intervene --backend tiny` | **0** | `donor_rows=[0,1]`（同 `node_id=q`、不同 trace），`status=prospective_decode`，`timing=offline_hidden` |
| `repair --eval-mode scientific --backend tiny` | **0** | `k=1..5`，`refilled_prefix=true`，`record_id=repair:fix-t1-001:task_oracle:k{1..5}` |
| `analyze --eval-mode scientific --in-dir <s-lab>` | **0** | `p1=p2=p3=null`，`scientific_conclusion=null`，`status=not_evaluated`（task 标签不足 4 行双类） |

`H[0]` 与 `H[1]` 不等（`maxabs=0.0032126`）。collect→s-prep HASH VERIFY 全 True。各阶段 digest 自洽。

这是 **tiny 随机权重 + 约束 `\nq = <digit>`** 的可调度链路，**不是** 论文 §4.1 自然 CoT，也 **不是** OPS-01 科学全跑。Exit 0 只证明这八个用户子命令在本机没有断线。

### 3.4 schema / shape / ID

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `review_export.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

夹具 Observation：`outcome=changed`，`raw_values=["0","8"]`，`record_id=prepare:{identity}:p2`。默认编辑 **p2:0→2**，重算答案 8。合成轨迹 `"p1 = 4\np2 = 0\nq = 0\n"` / `"p1 = 4\np2 = 2\nq = 8\n"`。夹具有效扰动，**不是** 科学全量扫描。

身份合同（本轮实测）：

1. 夹具 Event `record_id`：`trace-base:{q}` 与 `trace-edit:{q}` 互异。scientific 6 行按 `trace-*:{q}` 区分。
2. 两行 Task：`fix-t1-001` 与 `fix-t1-001::p2=2`。
3. prepare Label `record_id=prepare:q:p2`；label 阶段改写为 `label:q:p2`，`run_id=label`。
4. `Trace.from_dict` 回载成功。
5. 夹具 tiny `H`/`H_pre_*` `[2,32]`。scientific `[6,32]`（6 迹 × 1 个可表达 `q`），**不再** 是 18 行里 12 行 NaN。
6. Repair 夹具：`repair:fix-t1-001:task_oracle:k1`。scientific：`k1..k5`，同一 `base_group_id`。
7. 写出 traces 仍可带合成 `range` ID；collect 前向用 `encode_text(text)`。

### 3.5 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：tasks/edits/splits/events/observations/labels/traces/run_spec/manifest **九文件 hash 全等**。
- `write_run_spec(..., code_revision="latest")` → `ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind` → `ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})` → `ValueError`（`allow_nan=False`）。
- cwd=`%TEMP%` 调用 `runtime_info()["git_revision"]`：**`46a6e26…`**。
- `packages.reasoning-diff = null`。
- `write_npz` 拒绝 object；成功后无残留。
- `write_manifest(..., {tasks:10, edits:3, failure:0})` → `success_count=0`；显式 `"success": 1` → 1。

### 3.6 恢复 / 分片

| 检查 | 退出码 | 结果 |
|---|---|---|
| `--resume` prepare（仅默认） | **0** | 与已写 config 一致；`fx/` 无 `failure.json` |
| `--resume` prepare `--edit-premise p2 --edit-value 2` | **0** | 文件保留 |
| `--resume` collect / label / fit / calibrate / intervene / repair / analyze | **0** | `success_count` 仍为 1 |
| `--resume` + 篡改 `traces.jsonl` | **1** | `resume hash mismatch or missing file: traces.jsonl` |
| 上述失败后的 `manifest.json` | — | **`file_hashes` 与原成功清单全等**；`success_count=1`；另写 `failure.json`；`digest` 不变 |
| `--resume` + 清单 digest 改为 64 个 `0` | **1** | `resume manifest digest is not self-consistent` |
| `--resume` + 删除 `traces-shard-0000.jsonl` | **1** | 成功清单仍列出该 shard；`success_count=1` |
| `--shard` | **0** | `traces-shard-0000.jsonl`、`0001.jsonl` **各 1 行**；`traces.jsonl` 2 行 |
| 不加 `--shard` | **0** | **无** shard 文件 |

`_resume` 比对 `file_hashes`、跳过 `None` 的 config 键、digest 自洽。`main` 的 `except` 写 `failure.json`；已有 `success_count` 时 **不** 覆盖成功清单。

### 3.7 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 不存在 | **1** `FileNotFoundError` | 失败清单 `success_count=0` |
| `collect` 无 `--in-dir` | **1** `collect requires --in-dir` | 失败清单 |
| `label` 无 `--in-dir` | **1** `label requires --in-dir with observations.jsonl` | 失败清单 |
| `fit` 无 `--in-dir` | **1** `fit requires --in-dir` | 失败清单 |
| `calibrate` 无 `--in-dir`（fixture **与** scientific） | **1** `calibrate requires --in-dir` | 失败清单 |
| `intervene` 无 `--in-dir` | **1** `intervene requires --in-dir` | 失败清单 |
| `repair` 无 `--in-dir` | **1** `repair requires --in-dir` | 失败清单 |
| `analyze` 无 `--in-dir` | **1** `analyze requires --in-dir` | 失败清单；**无** `report.json` |
| `fit --split test` | **1** `probe fit cannot fit on test` | 失败清单 |
| `calibrate --split probe_train` | **1** `calibration cannot fit on probe_train` | 失败清单 |
| `--in-dir docs/SERVER_RUNBOOK.md` + collect / calibrate / intervene / repair / analyze | **1** `NotADirectoryError` | 仅失败清单；**无** features / 阶段 jsonl / `report.json` |
| 同上 + label | **1** 缺 observations | 仅失败清单 |
| 同上 + fit | **1** 缺 features.npz | 仅失败清单 |
| `read_jsonl` 非法行 | `ValueError('…/bad.jsonl:1: invalid JSON')` | — |
| `IsolatedExecutor().submit` | `executor_unavailable` | — |
| offline calibrate `n=1` | **0** | `q=null`，`infinity=true` |
| `write_npz` object | 写入前 `ValueError` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits=…)` 回显 `limits`，不执行限额。

### 3.8 `--eval-mode scientific` 门禁与 NaN fit

| 命令 | 退出码 | 结果 |
|---|---|---|
| `prepare --eval-mode scientific`（无 fractions） | **1** | `scientific mode requires explicit --split-fractions` |
| `collect --backend offline --eval-mode scientific` | **1** | `scientific collect refuses offline_prefix_ids as H` |
| `collect --backend tiny --eval-mode scientific` | **0** | 接受 `random_init`；本跑 `H` 全有限 |
| 完整 scientific 八段 | **全 0** | 见 §3.3 |
| 夹具 collect 注入 `H[0]=NaN` 后 `fit --eval-mode scientific` | **1** | `scientific fit refuses NaN hidden rows`；只写 `failure.json`，**无** `probes.jsonl` |
| 同上，fixture `fit`（不设 scientific） | **0** | 丢掉 NaN 行后写出；`U`/`V`/`b` 有限 |
| 库 `BilinearProbe.fit`（4×8，一行 NaN） | — | `U`/`V`/`b` 有限，`encode` 成功 |
| 库全 NaN `H` | — | `status=no_known_labels`，不写 NaN 权重 |

scientific 是门禁开关，不是科学全跑。

### 3.9 隔离执行器

```text
get_executor() / get_executor(None) → UnavailableExecutor
get_executor("spy") → SpyExecutor
get_executor("subprocess"|"child_process") → ChildProcessExecutor
ChildProcessExecutor.isolated_sandbox = False
IsolatedExecutor.isolated_sandbox = True，submit → executor_unavailable
score_code 默认：status=executor_unavailable, value=None, eligibility=False
SpyExecutor + exec(：rejected
ChildProcessExecutor + 合法 assert：ok
ChildProcessExecutor + 失败 assert：failed
ChildProcessExecutor + exec(：rejected
ChildProcessExecutor + sleep + timeout=0.2：timeout
score_numeric("4","4") → 1.0；score_qa("Paris","paris") → 1.0
```

生产路径未见 `exec(` / `eval(` 作为评分回退。普通 subprocess **不能** 冒称 Linux cgroup 沙箱（runbook 仍标 `pending_server`）。

### 3.10 T2–T4 `--kind`

| `--kind` | sidecar | 退出码 | 结果 |
|---|---|---|---|
| `gsm_plus` / `t2_gsm_plus` | 无 | **0** | `plus_numeric` `4→5`；0 events / 0 obs |
| `gsm_symbolic` / `t2_gsm_symbolic` / `symbolic` | 无 | **1** | 别名能进 catalog；`no editable non-placeholder premise` |
| `gsm_symbolic` / `t2_gsm_symbolic` | `--sidecar t2_formula_sidecar.json` | **0** | `kind=value`，`after b→2`；2 events / 1 obs |
| `hotpot` / `t3_hotpot` | 无 | **1** | **不是** `unknown snapshot kind`；`renamed premise DocA:0 missing from question` |
| `humaneval` / `t3_humaneval` | 无 | **0** | `input_list`，prompt+`\n# variant`；0 events |
| `musique` / `t3_musique` | 无 | **1** | **不是** `unknown snapshot kind`；`Unknown name in expression: composition_reference` |
| `t4` / `t4_boundary` | 无 | **0** | `t4_question`，问句追加 ` ?` |
| `not_a_kind` | 无 | **1** | `unknown snapshot kind not_a_kind` |

`t3_musique` / `t4_boundary` 别名 **已接通**。`--sidecar` **可** 传入 GSM-Symbolic。label / fit / analyze **无** `--kind`。这不是与 T1 同等的域流水线。

hotpot/musique 失败点在 `cmd_prepare` 于域编辑之后无条件调用 `make_source_value_pair`（`cli.py` 298 / 328）：`apply_rename_edit` 要求前提文本出现在 `question`（hotpot 的 `DocA:0` 在 context，不在问句）；`apply_value_edit`→`recompute` 把 musique 的 `expression="composition_reference"` 当 AST 公式。仓库自带夹具 `t3_hotpot_one.json` / `t3_musique_pair.json` 即触发。相对 r06「`hotpot`/`musique` prepare exit 0」这是 **回退**。

### 3.11 atomic NPZ

`write_npz`：拒 object → `mkstemp` → `np.savez` → `os.replace`。成功后无残留。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 把 pytest / 作者「144 passed」当验收 | 夹具绿测不是科学全跑，也不是 OPS-01 |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境 |
| 真实模型 / GPU / 官方数据 | `pending_server` |
| 在 `HASH_MISMATCH` 后的当前树上重跑八段 | 会把漂移后的字节与声明冻结混为一谈 |
| 阅读本轮 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。编号为本轮 `E8-##`。

---

### E8-01 声称冻结 hash：开始匹配，写报告前漂移（confirmed defect / 冻结完整性）

- **严重度：** high（审查对象不稳定）
- **状态：** confirmed defect
- **文件：** `.planning/audits/round-08/VERSION.md`；`cli.py`；`models/collect.py`
- **复现 / 证据：** §1。开始时按原文脚本 **60** 文件 = 声称值 `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`。写报告前同一脚本 = `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`。行数漂移仅 `cli.py`（1164→1241）与 `models/collect.py`（199→261）。本通道未改这些文件。
- **影响：** 声明冻结不再等于当前工作区。他通道若读「现在的树」，审的不是 VERSION 上的 hash。
- **对应要求：** OPS-01 可复现审查对象。

---

### E8-02 失败 `main` 不再覆盖成功清单（closed，原 E6-02 / E5-02）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `main` 1132–1160（实跑快照）
- **复现 / 证据：** §3.6。篡改 traces 或删除 shard 后 `--resume`：写出 `failure.json`，`file_hashes` / `success_count=1` / `digest` 与失败前 **全等**。

---

### E8-03 `--resume` 的 command 键与写出 config 对齐（closed，原 E6-03）

- **状态：** **closed**
- **复现 / 证据：** §3.6。prepare 默认 `--resume` 以及后七段完整产物 `--resume` **全部 exit 0**；`fx/` 无失败清单。

---

### E8-04 `--features-dir` 可消费权重；infinity 可 JSON（closed，原 E6-04）

- **状态：** **closed**
- **复现 / 证据：** §3.2 / §3.2c。`--features-dir` 进入 `predict_matrix`。offline `n=1`：`q=null`，`infinity=true`。

---

### E8-05 `--shard` 按轨迹各写一份（closed，原 E6-05）

- **状态：** **closed**
- **复现 / 证据：** §3.6。`--shard` → 两个 1 行 shard；不加 flag → 无 shard 文件。

---

### E8-06 Event/Label `record_id` 含身份且跨轨迹不碰撞（closed，原 E6-06）

- **状态：** **closed**
- **复现 / 证据：** §3.4。夹具 2 条、scientific 6 条 Event `record_id` 互异。

---

### E8-07 analyze 在写 `report.json` 之前拒绝文件 `--in-dir`（closed，原 E6-07）

- **状态：** **closed**
- **复现 / 证据：** §3.7。文件 `--in-dir` **无** `report.json`。

---

### E8-08 `--eval-mode scientific` 门禁仍在（closed 存在性；不是科学全跑）

- **状态：** **closed**（缺 flag / offline H）
- **复现 / 证据：** §3.8。

---

### E8-09 scientific / 注入 NaN 不再把 NaN 权重写入 JSON（closed，原 E6-09）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` 578–582；`probes/bilinear.py` 45–51；`models/collect.py` 51–52；`io.encode` `allow_nan=False`
- **复现 / 证据：** §3.3 / §3.8。scientific 用户八段 `H` `[6,32]` 全有限，fit exit **0**，task 头 `U`/`V`/`b` 有限。注入 NaN 后 scientific fit **拒绝** 并失败清单。bilinear 对 NaN 行掩码，`encode` 成功；全 NaN → `no_known_labels`。
- **作者「E6-09」在「拒绝 NaN H + 不写 NaN JSON」字面范围独立关闭。** 这不等于 OPS-01，也不等于自然 CoT。

---

### E8-10 calibrate 认 `label`/`lab`/`labels` 与 `--labels-dir`（closed，原 E6-10）

- **状态：** **closed**（目录发现）
- **复现 / 证据：** §3.2c。`premise_id=q` 的可区分标签下，无祖先也能得到非零分。真实 `p2` 标签仍要祖先 tasks，见 E8-16。

---

### E8-11 夹具 tiny collect 重分词后 H 可区分（closed，原 E6-11）

- **状态：** **closed**
- **复现 / 证据：** §3.2b。`H[0]≠H[1]`（`maxabs=0.00567`）。

---

### E8-12 多轨迹 `H_pre_*` 与 `H` 同样按事件堆叠（closed，原 E6-12）

- **状态：** **closed**
- **复现 / 证据：** 夹具 `[2,32]`；scientific `[6,32]`。行数 = 可表达事件数，不是「最后一条轨迹」。

---

### E8-13 T2/T3/T4 `--kind` 仍不是与 T1 同等的用户 CLI（confirmed defect，原 E6-13 残留 + 回退）

- **严重度：** high
- **状态：** confirmed defect（别名/sidecar **不能** 关闭整条）
- **文件 / 符号 / 行号：** `catalog.py` 39–42；`cli.py` `_load_task` 178–184、`_domain_edit` 187–213、`cmd_prepare` 298/328；`edits.py` `make_source_value_pair` 204–216、`apply_rename_edit` 151–162、`recompute` 52–61
- **触发条件：** `python -m reasoning_diff prepare --kind hotpot|t3_hotpot|musique|t3_musique --fixture <仓库自带夹具>`
- **对应要求：** OPS-01 + DATA-02
- **复现 / 证据：** §3.10。
  - `t4` / `t4_boundary` exit **0**（别名接通）。
  - `t3_musique` **不再** `unknown snapshot kind`，但与 `musique` 一样 exit **1**：`Unknown name in expression: composition_reference`。
  - `--sidecar` + `gsm_symbolic` / `t2_gsm_symbolic` exit **0**。无 sidecar 仍失败。
  - `hotpot` / `t3_hotpot` exit **1**：`renamed premise DocA:0 missing from question`。r06 同夹具为 exit 0。
  - label/fit/analyze 无 `--kind`。gsm_plus / humaneval / t4 即使 prepare 成功也是 0 events / 0 obs。
- **作者「E6-13」只证明别名键与 sidecar 开关存在。本通道独立确认这两点；「同等用户 CLI」否决。**
- **根因（本通道）：** 域编辑成功后仍无条件 `make_source_value_pair`。hotpot 的句子不在 `question` 里；musique 的 `composition_reference` 不是可 `ast.parse` 的算术式。
- **建议：** 非算术 DAG 不要走 `recompute`/`apply_rename_edit`；pair 失败不得毁掉已成功的域 `Edit`。

---

### E8-14 七段无 `--in-dir` 必须失败（closed，原 E6-14 + E6-17）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` collect 433–434；label 542–543；fit 569–570；calibrate 688–689；intervene 800–801；repair 916–917；analyze 958–959
- **复现 / 证据：** §3.2 / §3.7。七段 + scientific calibrate 无 in-dir **全部 exit 1**，`success_count=0`。分析不写 `report.json`。
- **作者「E6-17」独立关闭。**

---

### E8-15 Repair `record_id` 含 `base_group_id` 与 `k`（closed，原 E6-15）

- **状态：** **closed**
- **复现 / 证据：** §3.4。夹具 `k1`；scientific `k1..k5`。不再出现 `kNone`。

---

### E8-16 runbook calibrate 祖先认 `prepare/` / `s-prep/`（closed，原 E6-16）

- **状态：** **closed**（目录名 + 非空分数）
- **文件 / 符号 / 行号：** `cli.py` 732–738
- **复现 / 证据：** §3.2 / §3.2c。runbook 烟测 `fx/cal` 已是非零 `one_minus_p`。隔离复制 `prepare/`、`prep/`、`s-prep/` 分数相同。仅 `label/`、无 tasks → `[0,0]`。
- **作者「E6-16」在「祖先含 prepare/ 与 s-prep/」字面范围独立关闭。** `input_hashes` 仍不含 labels/tasks，记为非缺陷建议，不重开本条。
- **`event_rows` 优先：** 代码先读该文件。有 `prepare/` 时改/删 `event_rows` 分数相同，本通道不把「优先」写成已用分数差关闭。

---

### E8-17 fixture 下 calibrate / intervene / repair 无 `--in-dir` 仍成功（closed，原 E6-17）

- **状态：** **closed**
- **复现 / 证据：** §3.7。三条现均 exit 1。与 E8-14 合并关闭。

---

### E8-18 scientific intervene 不再把 NaN 行当成无 donor（closed，原 E6-18）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `models/collect.py` 51–52（跳过不可表达 `pre_step`）；`cli.py` `_expressible_donor` 775–793；intervene 814–838
- **复现 / 证据：** §3.3。scientific `H` 6 行全有限；`event_rows` 皆 `q` 且跨 trace；`donor_rows=[0,1]`；`status=prospective_decode`；几何 `timing=offline_hidden`（不是 `unexpressible` / `pre_step`）。夹具路径同样。
- **作者「E6-18」在「不可表达行不入 H + 有限同 node_id 配对 + 几何 timing=offline_hidden」字面范围独立关闭。** 事件仍是约束 `q = <digit>`，不是自然 CoT。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 开始时冻结 hash 复现 | 开始 **HASH_MATCH** §1 |
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError`；fit 不再写入 NaN 权重（E8-09） |
| `latest` 拒绝 | `write_run_spec(..., "latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `Unknown source_kind 'made_up'` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 / §3.3 |
| runbook `--in-dir` 文件哈希与上游字节一致 | HASH VERIFY 全 True |
| `--labels-dir` 进入 **fit** `input_hashes` | §3.2 |
| `Trace.from_dict` 回载 | §3.4 |
| 完整产物 `--resume` 成功 | §3.6 |
| 篡改/缺 shard 时 `--resume` 拒绝且 **不覆盖** 成功清单 | E8-02 / E8-03 |
| 损坏 digest 自洽检查 | `resume manifest digest is not self-consistent` |
| `require_split` | §3.7 |
| 代码评分不回退 host exec | 默认 `executor_unavailable`；Child 非沙箱 |
| 直接迁移维度拒绝 | `not_applicable_dimension_mismatch` 4096≠3584 |
| Week-8 未注册 | `gate0/1/2.decision=unregistered`，`scientific_conclusion=null`，`skip_p2_p3=true` |
| analyze 不编造 P1–P3 | `p1=p2=p3=null`，`status=not_evaluated` |
| 默认 prepare 不再 4×0 | `p2→2`，`raw_values=["0","8"]` |
| `report.json` 进清单 | analyze `file_hashes` 含 report |
| NPZ 原子替换且拒 object | §3.5 / §3.11 |
| `git -C` revision | cwd=TEMP 仍 `46a6e26…` |
| `python -m` 入口 | §3.1 |
| `success_count` 缺省 0 | 实验 ≠ 13 |
| 文件 `--in-dir` 不留半截 collect / 不先写 report | E8-07 |
| scientific 拒绝 offline H / 无 fractions | §3.8 |
| humaneval 不再 value-edit 成 `"2"` | §3.10 |
| infinity JSON | `q=null`，`infinity=true`（E8-04） |
| 七段缺 in-dir 失败 | E8-14 / E8-17 |
| tiny 重分词 + `H_pre` 堆叠 | E8-11 / E8-12 |
| calibrate 认 `label`/`lab`/`labels` 与 `prepare/`/`s-prep/` | E8-10 / E8-16 |
| repair `record_id` 含 group 与 k | E8-15 |
| scientific fit 可落盘有限权重 | E8-09 |
| scientific intervene 有限 donor | E8-18 |
| `t4_boundary` 别名 + GSM-Symbolic `--sidecar` | §3.10 部分 |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |
| 漂移后（`9ffc4cd…`）树上的八段是否仍成立 | 本通道未重跑；不得用开始时的 exit 0 给当前树背书 |

## 8. 结论

审查开始时 **`HASH_MATCH`** `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`（60 文件）。全部 `python -m` 证据绑定该快照。写报告前 **`HASH_MISMATCH`** `9ffc4cd…`（`cli.py`、`collect.py` 行数已变）。

夹具烟测按 runbook 八段（collect=**tiny**，calibrate 带 `--features-dir`）**全部退出码 0**，且 calibrate 已是非空 RSI 分数。scientific tiny 按同一用户顺序 **八段全部 exit 0**：`H` 全有限，fit 写出有限 JSON，intervene 走到 `prospective_decode`。这只证明 T1 tiny 用户子命令可调度，**不证明** OPS-01，也 **不是** 科学全跑。Exit 0 不能当作 OPS-01。

相对作者 close-out，本通道独立确认：

| 作者声称 | 独立复跑 |
|---|---|
| E6-09 scientific fit 拒绝 NaN H；不写 NaN JSON | **成立**（E8-09） |
| E6-13 `t3_musique`/`t4_boundary` 别名；`--sidecar` 可入 GSM-Symbolic | **别名键与 sidecar 成立**；`t4_boundary` prepare 通；**hotpot/musique prepare 失败**（E8-13） |
| E6-16 祖先含 `prepare/` / `s-prep/` | **成立**（E8-16） |
| E6-17 calibrate / intervene / repair 无 `--in-dir` 失败 | **成立**（E8-14 / E8-17） |
| E6-18 不可表达 `pre_step` 不入 H；有限同 `node_id` 配对；几何 `timing=offline_hidden` | **成立**（E8-18）；事件仍是约束 `q = <digit>` |

仍不通过：当前树已离开声明冻结（E8-01）；T2–T4 不是与 T1 同等的用户 CLI，仓库自带 hotpot/musique 夹具在 prepare 被 `source_value_pair` 打断（E8-13）。Gate 未注册与 `scientific_conclusion=None` **不是** 缺陷。

**本通道不通过** OPS-01。**FAIL**。空通过或「测试绿了」或「八段 exit 0」不能作为本通道结论。

下一步（建议，非本通道实施）：先重新冻结并停止并行改生产代码；T3 prepare 不要用算术 `recompute`/`rename` 写 pair；再在新冻结上重跑本通道。
