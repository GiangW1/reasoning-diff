# E：端到端工程审查（round-07）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮 A–D/F 通道报告。`ISSUES.md` 作者本地关闭声明（E6-09/13/16/17/18 等）已独立复测，不采信作者关闭声明。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。`ChildProcessExecutor` **不是** `IsolatedExecutor`。

**冻结核验：`HASH_MISMATCH`。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 02:04–02:55 +08:00 |
| 声称冻结 hash | `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（用户给定；与 `.planning/audits/round-07/VERSION.md` 一致；声称 60 文件） |
| 开审独立复算 | **当时 `HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**60** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`。 |
| 交卷独立复算 | **`HASH_MISMATCH`**。同一脚本、仍 60 文件，得到 `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`。`cli.py` 从开审通读的 1143 行变为 **1164** 行（mtime 02:05:26，新增 `_e_premise_ids`）；`tests/test_round06_regressions.py` mtime 02:05:38。本通道 **未** 改 `src/` / `tests/` / `pyproject.toml`。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；从 `%TEMP%` cwd 调用相同） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch 2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户 CLI 跨模块路径：prepare→collect→label→fit→calibrate→intervene→repair→analyze，夹具 **与** scientific tiny；resume/manifest、`--features-dir`、`--labels-dir`、`--shard`、`--kind` 别名、`--sidecar`、缺 `--in-dir`；按 `docs/SERVER_RUNBOOK.md` 本机命令实跑；猎取 E6-09..E6-18 **当前字节** |
| r06 声称（独立复跑） | 见 §5。作者称关闭 E6-09/13/16/17/18；本通道对当前字节独立核实，不采信作者表 |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md`、`executor.py` |
| 实跑入口 | `python -m reasoning_diff`（runbook 命令）；产物根 `%TEMP%\rd-e-r7-k8w3n1qp\`，未写入 `src/` / `tests/` / `pyproject.toml` |

**冻结说明：** 声称冻结在开审瞬间可复现，但审查窗口内范围内文件被第三方改写。交卷对象是 **当前工作区字节**，与声称冻结 hash **不一致**。CLI 实跑发生在 `cli.py` 02:05:26 漂移之后。本报告同时记录开审 MATCH 与交卷 MISMATCH。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–1164（交卷） | 通读 + `python -m` 夹具八段 + scientific tiny + resume/负路径 + `--kind` + `--sidecar` + `--shard` + 缺 in-dir | 八段可调度；fit 拒 NaN（scientific）；calibrate 认 `prepare/`/`s-prep/`；缺 in-dir 七段均失败；`t3_musique`/`hotpot` prepare 因 `source_value_pair` 失败 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 通读 + digest / `success_count` / shard | digest 自洽；`success_count` 缺省 0；`completed_shard_ok` 函数正确，CLI 仍用刚算出的 hash 自检 |
| `src/reasoning_diff/io.py` | 1–133 | 通读 + NPZ/NaN/`runtime_info` | JSON/JSONL/NPZ 临时文件+`os.replace`；拒 object；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | 通读 + `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–51 | 对照实跑 | 现含 `--features-dir`；resume 说明与实跑一致；隔离仍 `pending_server`；祖先目录现含 `prepare/`（与 runbook `runs/prepare` 对齐） |
| `src/reasoning_diff/executor.py` | 1–109 | `get_executor` / subprocess | 默认 Unavailable；`ChildProcessExecutor.isolated_sandbox=False`；**不是** `IsolatedExecutor`；拒 `exec(`/`eval(` |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–385 | 通读 + 产物 `from_dict` | Event `record_id` 含 `run_id`；`Trace.from_dict` 把未知键并入 metadata |
| `src/reasoning_diff/splits.py` | 1–111 | CLI `require_split` | test 上 fit、probe_train 上 calibrate 仍拒绝 |
| `src/reasoning_diff/edits.py` | 默认 prepare `p2→2` + `make_source_value_pair` | 夹具 prepare / T3 kind | T1 重算答案 8；T3 域编辑成功后仍强制 SVP，hotpot/musique 崩 |
| `src/reasoning_diff/events.py` | 1–260 | prepare 解析 | 夹具 `parse_fixture_events`（仅 nodes）；scientific `parse_events` 只吃生成区 |
| `src/reasoning_diff/graphs.py` | 1–46 | prepare `ancestors` / calibrate `R(s_i)` | CLI calibrate 用 `anc.get`；无 tasks 则 RSI 为空 |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 observation 则无 task/behavior 标签；scientific 行为标签全未知（编辑未改变约束数字） |
| `src/reasoning_diff/models/collect.py` | 1–199 | tiny collect / swap decode | `pre_idx is None` **跳过**该事件，不再写入可拟合 H 行 |
| `src/reasoning_diff/models/generate.py` | 66–201 | scientific prepare | `parse_events(generated)`；`parse_region=generated`；约束 `\nq = <digits>` |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | `pre_step` 在 `start=0` 时 `token_index=None`，`expressible=false` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | collect 重分词 | `encode_text` 按字符 `ord`；夹具写出 traces 仍是合成 `range` |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `fit` | 未知/NaN 行掩码；`nan_to_num` 只用于梯度；无已知标签则不写 `U`/`V` |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `conformal_threshold` / `sequence_score` | `empty_truth→0.0`；`k>n` 返回 `q=inf`；CLI `_sanitize_cal` 写成 `q=null` + `infinity=true` |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | 几何与 hook；配对逻辑在 CLI `_expressible_donor` |
| `src/reasoning_diff/repair.py` | 1–223 | `repair` | scientific `k=1..5`；`refilled_prefix` 只认有限 `prefill_hidden` |
| `src/reasoning_diff/analysis.py` | 1–337 | `analyze` | 读 densities sidecar；标签不足 4 行双类 → `p1=null` / `not_evaluated` |
| `src/reasoning_diff/transfer.py` | 1–75 | analyze `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | prepare `--kind` | `t3_musique`/`t4_boundary` 别名存在；别名接通 ≠ prepare 成功 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–84 | `--kind` + `--sidecar` | 无 sidecar 仍无非 placeholder 前提；有 sidecar 可编辑 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 50–76 | `--kind gsm_plus` / `t2_gsm_plus` | 隔离替换 `"4"→"5"` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–78 | `--kind humaneval` / `t3_humaneval` | `apply_spec_edit` 追加 `# variant` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 51–104 | `--kind hotpot` / `t3_hotpot` | 域 `document_edit` 本身可构造；CLI 随后 SVP 失败 |
| `src/reasoning_diff/tasks/t3_musique.py` | 72–110 | `--kind musique` / `t3_musique` | `paragraph_edit` 返回 `Edit`；CLI 随后 `recompute` 失败 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 36–51 | `--kind t4` / `t4_boundary` | `apply_t4_question_edit`；两别名 exit 0 |
| `src/reasoning_diff/rng.py` | 1–53 | intervene `StreamBank` | CLI intervene 使用；prepare 未用 |
| `src/reasoning_diff/baselines.py` | 1–125 | CLI `fit` 调用 verbalizer / attention | 本轮 fit 产物含四档 verbalizer、BoundaryMLP、attention_* |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | CLI fit 调用 | 写入 `baseline=boundary_mlp` |
| `tests/test_cli_pipeline.py` | 1–30 | 读，未当作验收 | 只断言 exit 0 / `not_evaluated`；calibrate **无** `--features-dir`；collect=offline |

**抽样未做完整工程审查（非本通道主路径）：** `models/tiny.py`、`models/adapters.py`、T1 official 内部、`t2_noop.py`。确认 adapters **未被** 八段通用子命令调用（`cli.py` 无 `adapters` 引用）。

## 3. 已执行检查与结果

### 3.1 用户 CLI 入口

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`%TEMP%\rd-e-r7-k8w3n1qp`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir`、`--weight-seed` |
| `calibrate --help` | **0** | 有 `--features-dir` **与** `--labels-dir`（runbook L29 写了前者） |
| `fit --help` | **0** | 有 `--labels-dir` |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**；另跑 offline 对照）

产物根：`%TEMP%\rd-e-r7-k8w3n1qp\fx\`。夹具 `tests/fixtures/t1_tiny.json`。`--in-dir` 按 runbook 指向上一阶段。目录名用 runbook 的 `prepare` / `collect` / `label` / `fit` / `cal`。

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
| prepare | `{t1_tiny.json: …}` | `[]` | 夹具；默认 `p2→2`；另写 `source_value_pair` |
| collect tiny | prepare 全目录文件 + `upstream_manifest*`（与 prepare 字节 **全等**，HASH VERIFY 全 True） | 重算 prepare digest `75cd5fb3…` | 读 `tasks.jsonl` + `traces.jsonl`；对 `trace.text` **重新** `encode_text`；`weight_source=random_init`；`weight_seed=0` |
| label | 哈希 prepare 全目录 | `[75cd5fb3…]` | `observations.jsonl` + `tasks.jsonl`；`build_labels` |
| fit | collect 文件 **加** `label/labels.jsonl` 等 | collect + label 两枚重算 digest | 读 `H`/`E` + labels-dir；双头探针 + verbalizer/MLP/attention |
| calibrate（`--features-dir collect`） | fit + collect 文件 | 两枚 digest | `predict_matrix`；认兄弟 `prepare/tasks.jsonl` + `event_rows.jsonl` → **非空** `scores`（§3.2c） |
| intervene | collect | collect digest | tiny `H` 两行有限且不等 → `status=prospective_decode`，`timing=offline_hidden` |
| repair | prepare 全目录 | prepare digest | 默认 backend≠tiny → `prefill_unavailable`；`record_id=repair:fix-t1-001:task_oracle:k1` |
| analyze | label 文件 | label digest | densities sidecar；`p1/p2/p3=null`，`status=not_evaluated` |

各阶段 `manifest.digest` 均自洽。八个阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。

`collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze` 无 `--in-dir` **全部 exit 1**（§3.7）。

#### 3.2b tiny 对照（夹具 collect）

`collect --backend tiny` exit **0**：`weight_source=random_init`，`H`/`E`/`H_pre_*`/`H_post_step` 均为 `[2,32]`，**0 行 NaN**。`H[0]` 与 `H[1]` **不等**（`maxabs=0.0056705`）。写出的 `traces.jsonl` 仍保留 prepare 的合成 `token_ids=range(1,…)`（两条相等）；`encode_text(text)` 得到不同 ID（`[50,50,33,…]`），隐状态按重分词前向。`event_rows`：`q@trace-base`、`q@trace-edit`。`intervene --in-dir <tiny>` → `status=prospective_decode`，`followed_donor=false`，`invalid=1.0`，几何 `timing=offline_hidden`，`donor_rows=[0,1]`。

offline collect：`H` `[1,8]`，`token_prefix` 为合成 ID 前 8 项，`weight_source=offline_prefix_ids`。

#### 3.2c calibrate 目录名 / `--labels-dir` / 祖先目录

`--features-dir` 能让 `predict_matrix` 跑通。同一套 fit/collect（tiny），只改标签目录与内容：

用 **可区分** 标签（`premise_id=q`，使 RSI=`{q}` 在无祖先时也能命中）：

| 布局 | `scores` |
|---|---|
| 兄弟目录 `label/labels.jsonl` | `[0.00502325, 0.00502334]` |
| 仅 `lab/labels.jsonl` | 同上 |
| 仅 `labels/labels.jsonl` | 同上 |
| 仅 `othername/labels.jsonl`（无 flag） | `[0.0, 0.0]`（**未消费**） |
| `--labels-dir othername`（同样 q 标签） | `[0.00502325, 0.00502334]` |
| `--labels-dir` 指向不匹配 premise（`zzz`） | `[0.0, 0.0]`（`empty_truth`） |

**runbook 真实标签**（`event_id=q`，`premise_id=p2`）：

| 祖先来源 | `scores` / `q` |
|---|---|
| 无 `tasks.jsonl`（fit 目录没有） | `[0.0, 0.0]`，`q=0.0`，`status=finite` |
| 兄弟目录 `prep/tasks.jsonl`（代码仍列） | `[0.00502403, 0.00502409]`，`q=0.00502409` |
| 兄弟目录 `prepare/tasks.jsonl`（runbook 名） | 同上（**现认**） |
| 兄弟目录 `s-prep/tasks.jsonl` | 同上（**现认**） |

第一次 runbook 烟测 `fx/cal`：`scores=[0.00502403, 0.00502409]`，`status=finite`（找到 `fx/prepare/tasks.jsonl` + `event_rows`）。`input_hashes` **仍不含** 任何 labels 文件，即使传了 `--labels-dir`。

无 `--features-dir`：`status=probe_weights_or_features_missing`，`scores=null`，fixture 下 exit **0**。

offline 特征 + 对应 offline fit：`n=1`，`k=2`，`q=null`，`infinity=true`，JSON 可写。tiny-fit（32 维）配 offline 特征（8 维）→ `matmul` 维度错误 exit 1。

### 3.3 scientific tiny 八段

runbook 局部命令 + 本通道把后段也加上 `--eval-mode scientific`（calibrate/analyze）与 `--backend tiny`（collect/intervene/repair）。`--split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。

| 命令 | 退出码 | 要点 |
|---|---|---|
| `prepare --eval-mode scientific --split-fractions … --sham-opportunities 1` | **0** | 6 条 `tiny-qwen2` 轨迹；文本形如 `p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82`；`parse_status=constrained_target`；`parse_region=generated`；**6** events（每迹仅生成区 `q`，`start=45`），**4** observations |
| `collect --backend tiny --eval-mode scientific` | **0** | `H`/`H_pre_step` **`[6,32]`**（6 轨迹 × 1 可表达事件）；**0 行 NaN**；`E` `[2,32]` 有限；`event_rows` 全是 `node_id=q` |
| `label` | **0** | 3 行标签 + densities；task ∈ {1,1,0}；**behavior 全 null**（编辑轨迹约束数字同为 82，`outcome=no_change` 且非 exhaustive） |
| `fit --labels-dir <s-lab> --eval-mode scientific` | **0** | 写出 `probes.jsonl`；task 头 `loss≈0.050`，`U`/`V`/`b` **全有限**；behavior 头 `no_known_labels`（无 `U`）；**不是** NaN JSON |
| `calibrate --features-dir <s-col> --eval-mode scientific` | **0** | 认 `s-prep/tasks.jsonl`；`scores≈[0.00502358, 0.00502359, 0.00502353]`，`n_problems=3`，`q=0.00502359`，`status=finite` |
| `intervene --backend tiny` | **0** | `status=prospective_decode`（**不是** `donor_missing`）；`timing=offline_hidden`；`donor_rows=[0,1]`（同 `node_id=q`、不同 `trace_id`） |
| `repair --eval-mode scientific --backend tiny` | **0** | `k=1..5`，`refilled_prefix=true`，`record_id=repair:fix-t1-001:task_oracle:k{1..5}`，`status=ok` |
| `analyze --eval-mode scientific --in-dir <label>` | **0** | `p1=p2=p3=null`，`scientific_conclusion=null`，`status=not_evaluated`（behavior 未知 + 标签不足双类 4 行） |

人工注入 NaN 到 scientific `H` 后再 `fit --eval-mode scientific`：exit **1**，`scientific fit refuses NaN hidden rows`，**无** `probes.jsonl`。同一 NPZ + `--eval-mode fixture`：exit **0**（丢弃非有限行后拟合）。

**对 r06 E6-09：** 「scientific 因 NaN JSON 在 fit 处断裂」——**当前字节不再复现**。有事件、H 有限、probes 可 JSON。夹具/科学八段均为 exit 0。**exit 0 仍不是 OPS-01**（tiny `random_init`、analyze `not_evaluated`、约束赋值不是自然 CoT）。

### 3.4 schema / shape / ID

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `review_export.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

Observation（夹具精确一行）：`outcome=changed`，`raw_values=["0","8"]`，`record_id=prepare:{identity}:p2`，`run_id=prepare`，`base_group_id=fix-t1-001`。默认编辑仍为 **p2:0→2**。合成轨迹 `"p1 = 4\np2 = 0\nq = 0\n"` / `"p1 = 4\np2 = 2\nq = 8\n"`。`edits.jsonl` 第二行 `kind=source_value_pair`。这是夹具有效扰动，**不是**科学全量扫描。

身份合同（本轮实测）：

1. 夹具 `events.jsonl` 两行 `record_id` 为 `trace-base:{identity}` 与 `trace-edit:{identity}`，彼此不同。scientific 6 行按 `trace-*:{entity}` 区分（仅 `q`）。
2. 两行 Task：`fix-t1-001` 与 `fix-t1-001::p2=2`。
3. prepare Label：`record_id=prepare:q:p2`。label 阶段重写为 `record_id=label:q:p2`，`run_id=label`。
4. collect `Trace.from_dict` → 成功。仅首行 traces 被写入 feature metadata。
5. tiny 夹具 `H`/`H_pre_*` 均为 `[2,32]`（2 轨迹 × 1 事件）。scientific `H`/`H_pre_*` 均为 `[6,32]`（6 × 1 可表达 `q`），不可表达 `pre_step` **未入 H**。`E` mean-pool 为 `[2,32]`。
6. Repair 夹具：`record_id=repair:fix-t1-001:task_oracle:k1`，`base_group_id=fix-t1-001`，`k=1`，`status=prefill_unavailable`。scientific：`k=1..5` 填齐，同一 `base_group_id`，`refilled_prefix=true`。无 `--in-dir` 现 **失败**，不再写空 `base_group_id` 成功清单。
7. 夹具写出的 `token_ids` 仍是 `range(1, len(text)+1)`；collect 前向用的是 `encode_text(text)`。scientific 存储 `token_ids` 为 tiny 解码 ID（例：`[50,50,33,…]`），与 `encode_text(full_text)` 前缀相同、全序列不必相等（约束追加）。

### 3.5 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：tasks/edits/splits/events/observations/labels/traces/run_spec/manifest **九文件 hash 全等**。
- `write_run_spec(..., code_revision="latest")` → `ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind` → `ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})` → `ValueError`（`allow_nan=False`）。
- cwd=`%TEMP%` 调用 `runtime_info()["git_revision"]`：**`46a6e26…`**。
- `packages.reasoning-diff = null`。
- 后段 `run_spec.rng` 仅为 `{"stream": "<jsonl-name>"}`，无 seed、无输入 digest。
- `write_npz` 拒绝 object 数组。成功后无 `.features.npz*` 残留。
- `write_manifest(..., {tasks:10, edits:3, failure:0})` → `success_count=0`；显式 `"success": 1` → 1。

### 3.6 恢复 / 分片

| 检查 | 退出码 | 结果 |
|---|---|---|
| `--resume` prepare（仅默认参数） | **0** | 解析后的 `p2`/`2` 与已写 config 一致 |
| `--resume` prepare `--edit-premise p2 --edit-value 2` | **0** | 文件不变 |
| `--resume` collect / label / fit / calibrate / intervene / repair / analyze（完整产物） | **0** | `command` 键与写出值一致；`success_count` 仍为 1；无 `failure.json` |
| `--resume` + 篡改 `traces.jsonl` | **1** | `resume hash mismatch or missing file: traces.jsonl` |
| 上述失败后的 `manifest.json` | — | **`file_hashes` 原样保留**；`success_count=1`；另写 `failure.json`；`digest` 不变 |
| `--resume` + 清单 digest 改为 64 个 `0` | **1** | `resume manifest digest is not self-consistent` |
| `--resume` + 删除 `traces-shard-0000.jsonl` | **1** | 成功清单仍列出该 shard hash |
| `--shard` | **0** | `traces-shard-0000.jsonl`、`0001.jsonl` **各 1 行**；与 `traces.jsonl`（2 行）字节不同 |
| 不加 `--shard` | **0** | **无** shard 文件 |

`_resume`（`cli.py:38–65`）：比对 `file_hashes`、**跳过 `None` 的 config 键**、digest 自洽。`_write_stage`：`merged = {"command": name, **config}`。

`main` 的 `except` 仍写 `failure.json`；若已有 `success_count` 或 `record_counts.success`，**不再** `write_manifest` 覆盖成功清单。

### 3.7 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 不存在 | **1** `FileNotFoundError` | `failure.json` + 失败清单（`success_count=0`） |
| `collect` 无 `--in-dir` | **1** `collect requires --in-dir` | 失败清单 |
| `label` 无 `--in-dir` | **1** `label requires --in-dir with observations.jsonl` | 失败清单 |
| `fit` 无 `--in-dir` | **1** `fit requires --in-dir` | 失败清单 |
| `calibrate` 无 `--in-dir`（fixture **与** scientific） | **1** `calibrate requires --in-dir` | 失败清单（scientific **不再**先走到字面量门禁） |
| `intervene` 无 `--in-dir` | **1** `intervene requires --in-dir` | 失败清单 |
| `repair` 无 `--in-dir` | **1** `repair requires --in-dir` | 失败清单 |
| `analyze` 无 `--in-dir`（fixture **与** scientific） | **1** `analyze requires --in-dir` | 失败清单；**无** `report.json` |
| `fit --split test` | **1** `probe fit cannot fit on test` | 失败清单 |
| `calibrate --split probe_train` | **1** `calibration cannot fit on probe_train` | 失败清单 |
| `--in-dir docs/SERVER_RUNBOOK.md` + collect / calibrate / intervene / repair / analyze | **1** `NotADirectoryError` | 仅失败清单；**无** features / 阶段 jsonl / `report.json` |
| 同上 + label | **1** 缺 observations | 仅失败清单 |
| 同上 + fit | **1** 缺 features.npz | 仅失败清单 |
| `read_jsonl` 非法行 | `ValueError('…/bad.jsonl:1: invalid JSON')` | — |
| `IsolatedExecutor().submit` | `executor_unavailable` | — |
| `@forbid_host_exec` | `RuntimeError('host execution of model/dataset code is forbidden')` | 生产 CLI 未使用 |
| offline calibrate `n=1` | **0** | JSON 可写：`q=null`，`infinity=true` |
| `write_npz` object | 写入前 `ValueError` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits=…)` 回显 `limits`，不执行限额。

### 3.8 `--eval-mode scientific` 门禁

| 命令 | 退出码 | 结果 |
|---|---|---|
| `prepare --eval-mode scientific`（无 fractions） | **1** | `scientific mode requires explicit --split-fractions` |
| `collect --backend offline --eval-mode scientific` | **1** | `scientific collect refuses offline_prefix_ids as H` |
| `collect --backend tiny --eval-mode scientific` | **0** | 接受 `random_init`；本跑 H 无 NaN |
| `calibrate` 无 probes + scientific | **1** | `scientific calibrate refuses loss or literal scores` |
| `analyze` 无 `--in-dir` + scientific | **1** | `analyze requires --in-dir` |
| 完整 scientific 八段 | **全 0** | 见 §3.3；门禁仍在，链路在 tiny 上可走完。**不是**科学全跑 |

scientific 是门禁开关，不是科学全跑。

### 3.9 隔离执行器

```text
get_executor() / get_executor(None) → UnavailableExecutor
get_executor("spy") → SpyExecutor
get_executor("subprocess"|"child_process") → ChildProcessExecutor
ChildProcessExecutor.isolated_sandbox = False
IsolatedExecutor.isolated_sandbox = True，submit → executor_unavailable
isinstance(ChildProcessExecutor(), IsolatedExecutor) is False
score_code 默认：status=executor_unavailable, value=None, eligibility=False
SpyExecutor + exec(：rejected
SubprocessExecutor + 合法 assert：ok
SubprocessExecutor + 失败 assert：failed
SubprocessExecutor + exec( / eval(：rejected
SubprocessExecutor + sleep + timeout=0.2：timeout
score_numeric("4","4") → 1.0；score_qa("Paris","paris") → 1.0
```

生产路径未见 `exec(` / `eval(` 作为评分回退。普通 subprocess **不能**冒称 Linux cgroup 沙箱（runbook 仍标 `pending_server`）。`ChildProcessExecutor` **不是** `IsolatedExecutor`。

### 3.10 T2–T4 `--kind`

| `--kind` | 退出码 | 编辑器 | 备注 |
|---|---|---|---|
| `gsm_plus` / `t2_gsm_plus` | **0** | `apply_plus_numeric_edit` `4→5` | 别名接通 |
| `gsm_symbolic` / `t2_gsm_symbolic` / `symbolic` | **1** | 别名能进 catalog；无 sidecar | `no editable non-placeholder premise` |
| `gsm_symbolic` + `--sidecar tests/fixtures/t2_formula_sidecar.json` | **0** | `apply_value_edit` `b→2` | `graph_kind=formula_sidecar`；2 events / 1 obs |
| `hotpot` / `t3_hotpot` | **1** | 域 `document_edit` 之后 `make_source_value_pair` | `renamed premise DocA:0 missing from question`（相对 r06 exit 0 **回归**） |
| `humaneval` / `t3_humaneval` | **0** | `apply_spec_edit` / `kind=input_list` | after 为 prompt+`\n# variant` |
| `musique` / `t3_musique` | **1** | 别名接通；`paragraph_edit` 后 SVP/`recompute` | `Unknown name in expression: composition_reference`。`t3_musique` **不再**是 `unknown snapshot kind` |
| `t4` / `t4_boundary` | **0** | `apply_t4_question_edit` | 问句追加 ` ?`；`t4_boundary` 别名接通 |

label / fit / analyze **无** `--kind`。这不是与 T1 同等的域流水线。`t3_musique` / `t4_boundary` 别名与 `--sidecar` 字面存在；`t3_musique` prepare 仍失败；`hotpot`/`musique` 相对 r06 回归。

### 3.11 atomic NPZ

`write_npz`：拒 object → `mkstemp` → `np.savez` → `os.replace`。成功后无残留。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 把 pytest / 作者「143 passed」当验收 | 夹具绿测不是科学全跑，也不是 OPS-01 |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境 |
| 真实模型 / GPU / 官方数据 | `pending_server` |
| 并发真实分片崩溃注入 | `--shard` 现为每轨迹一份副本，不是按组调度 |
| 阅读本轮 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |
| 在声称冻结字节上重跑（`9814019a…`） | 范围内文件在审查窗口被改写，该快照已不在工作区 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。编号为本轮 `E7-##`。

---

### E7-01 声称冻结 hash 与交卷树不一致（confirmed defect）

- **严重度：** high（审查对象合同）
- **状态：** confirmed defect
- **文件：** `.planning/audits/round-07/VERSION.md`；60 个范围内文件
- **复现 / 证据：** §1。开审复算 = 声称值 `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`。交卷复算 = `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`。`cli.py` 增 `_e_premise_ids`（662–671）；`tests/test_round06_regressions.py` 同时被改。本通道未写这些文件。
- **影响：** 独立审查无法把结论钉在声称冻结上。后续通道若按 VERSION 声称值对照，会对错树。
- **建议：** 冻结后禁止改范围内文件；改完必须重写 VERSION 并重开 A–F。

---

### E7-02 失败 `main` 不再覆盖成功清单（closed，原 E6-02 / E5-02）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `main` 1132–1161
- **复现 / 证据：** §3.6。篡改 traces 或删除 shard 后 `--resume`：写出 `failure.json`，`manifest.file_hashes` / `success_count=1` / `digest` 与失败前 **全等**。

---

### E7-03 `--resume` 的 command 键与写出 config 对齐（closed，原 E6-03）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `_resume` 54–58；`_write_stage` 141
- **复现 / 证据：** §3.6。prepare 默认 `--resume` 以及后七段完整产物 `--resume` **全部 exit 0**。

---

### E7-04 `--features-dir` 可消费权重；infinity 可 JSON（closed，原 E6-04）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `_sanitize_cal` 674–680；`cmd_calibrate` 683–772
- **复现 / 证据：** §3.2 / §3.2c。`--features-dir` 进入 `predict_matrix`。offline 路径 `n=1`：`q=null`，`infinity=true`，`status=infinity`。

---

### E7-05 `--shard` 按轨迹各写一份（closed，原 E6-05）

- **状态：** **closed**
- **复现 / 证据：** §3.6。`--shard` → 两个 1 行 shard；不加 flag → 无 shard 文件。

---

### E7-06 Event/Label `record_id` 含 `run_id` 且跨轨迹不碰撞（closed，原 E6-06）

- **状态：** **closed**
- **复现 / 证据：** §3.4。夹具 2 条、scientific 6 条 Event `record_id` 互异。

---

### E7-07 analyze 在写 `report.json` 之前拒绝文件 `--in-dir`（closed，原 E6-07）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `cmd_analyze` 958–961（先于 `write_json`）
- **复现 / 证据：** §3.7。fixture 与 scientific 的文件 `--in-dir` 均 **无** `report.json`。

---

### E7-08 `--eval-mode scientific` 门禁仍在（closed 存在性；不是科学全跑）

- **状态：** **closed**（缺 flag）
- **复现 / 证据：** §3.8。offline collect / 无 fractions / 无 features 的 scientific calibrate 均 exit 1。

---

### E7-09 scientific tiny 用户 CLI 不再因 NaN JSON 在 fit 处断裂（closed，原 E6-09）

- **状态：** **closed**（作者「拒 NaN H / 不写 NaN 权重」字面；**不是** OPS-01）
- **文件 / 符号 / 行号：**
  - `models/collect.py` 50–52：`pre_idx is None` 则 `continue`，该事件不入 H
  - `models/generate.py` 148–191：只解析生成区；`parse_region=generated`
  - `cli.py` 578–580：scientific fit 拒非有限 H
  - `probes/bilinear.py` 44–51：掩码未知/NaN 行
- **复现 / 证据：** §3.3。6 events、H `[6,32]` 全有限、0 NaN 行。fit exit 0，`fit_nan_json=false`。强制 NaN 行 → `scientific fit refuses NaN hidden rows`。calibrate / intervene 不再因无 probes / `donor_missing` 断在同一处。
- **对作者 E6-09：** 字面关闭 **独立确认**。不能把「tiny 八段 exit 0」写成 OPS-01 或论文模型可调度。

---

### E7-10 calibrate 认 `label`/`lab`/`labels` 与 `--labels-dir`（closed，原 E6-10）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` 703–716
- **复现 / 证据：** §3.2c。与 r06 相同：三目录名 + `--labels-dir` 非零；`othername` 无 flag 为 `[0,0]`。

---

### E7-11 夹具 tiny collect 重分词后 H 可区分（closed，原 E6-11）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` 460–462：`encode_text(trace.text)`
- **复现 / 证据：** §3.2b。`H[0]≠H[1]`（`maxabs=0.00567`）；intervene `prospective_decode`。写出 traces 仍带合成 `range` ID，不重开本条。

---

### E7-12 多轨迹 `H_pre_*` 与 `H` 同样按事件堆叠（closed，原 E6-12）

- **状态：** **closed**
- **复现 / 证据：** 夹具 tiny：`H` 与 `H_pre_*` 均为 `[2,32]`。scientific：均为 `[6,32]`（6 条可表达 `q`，不再是最后一条的 `[1,32]`）；`E` `[2,32]`。

---

### E7-13 T2/T3/T4 `--kind` 仍不是与 T1 同等的用户 CLI（confirmed defect，原 E6-13；别名/sidecar 字面关闭）

- **严重度：** medium
- **状态：** confirmed defect（部分别名 **不能**关闭整条）
- **文件 / 符号 / 行号：** `cli.py` `_load_task` 178–182（`--sidecar`）；`_domain_edit` 187–213；`catalog.py` 39–42；`cmd_prepare` 298 / 328（`make_source_value_pair`）
- **复现 / 证据：** §3.10。`t4_boundary` / `t4` exit 0。`t3_musique` **不再** `unknown snapshot kind`，但 prepare exit 1：`Unknown name in expression: composition_reference`。`gsm_symbolic` 无 sidecar 仍 exit 1；**有** `--sidecar` 则 exit 0。`hotpot`/`musique` 现亦 exit 1（见 E7-19）。label/fit/analyze 无 `--kind`。
- **对应要求：** OPS-01 + DATA-02
- **对作者 E6-13：** 「别名 + sidecar」字面 **部分确认**；「与 T1 同等用户 CLI」**不能关闭**。

---

### E7-14 collect / label / analyze 无 `--in-dir` 必须失败（closed，原 E6-14）

- **状态：** **closed**
- **复现 / 证据：** §3.2 / §3.7。三条均 exit 1，分析不写 `report.json`。后段见 E7-17。

---

### E7-15 Repair `record_id` 含 `base_group_id` 与 `k`（closed，原 E6-15）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `cmd_repair` 928–929（当前树）
- **复现 / 证据：** §3.4。夹具 `repair:fix-t1-001:task_oracle:k1`；scientific `k1..k5`。

---

### E7-16 runbook calibrate 现能读 `prepare/` / `s-prep/` 祖先（closed，原 E6-16）

- **状态：** **closed**（祖先目录 / `event_rows` 优先；hashes 不含 labels 仍是残留观察，不重开本条）
- **文件 / 符号 / 行号：** `cli.py` 721–738
- **复现 / 证据：** §3.2c。`prepare/` 与 `s-prep/` 均得到非零 `one_minus_p`；无 tasks 仍是空真理 `[0,0]`。scientific 烟测 `s-cal` 非零。`input_hashes` 仍不含 labels。
- **对作者 E6-16：** 字面关闭 **独立确认**。

---

### E7-17 fixture 下 calibrate / intervene / repair 无 `--in-dir` 现失败（closed，原 E6-17）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` 689；801；917
- **复现 / 证据：** §3.7。三阶段 exit **1**，失败清单 `success_count=0`。scientific calibrate 无 in-dir 同样先报 `calibrate requires --in-dir`。
- **对作者 E6-17：** **独立确认**。

---

### E7-18 scientific intervene 不再把 NaN 行当成无 donor（closed，原 E6-18）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `_expressible_donor` 775–793；`collect.py` 50–52
- **复现 / 证据：** §3.3。scientific `H` 6 行全有限；按同 `node_id=q`、不同 `trace_id` 配对 → `prospective_decode` / `timing=offline_hidden`。**不是** `donor_missing`。
- **对作者 E6-18：** **独立确认**。几何 timing 仍为 `offline_hidden`（hook 元数据另有 `hook_timing=pre_step`），与「不被 hook 改写几何 timing」一致。

---

### E7-19 persist `source_value_pair` 打断 T3 prepare（confirmed defect；相对 r06 回归）

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 298、328：域编辑成功后无条件 `make_source_value_pair`；`edits.py` `apply_rename_edit` / `recompute`
- **触发条件：** `--kind hotpot|t3_hotpot|musique|t3_musique` + 官方夹具
- **对应要求：** OPS-01 + DATA-02
- **复现 / 证据：** §3.10。r06 同夹具 `hotpot`/`musique` 为 exit 0。当前：hotpot `renamed premise DocA:0 missing from question`；musique/t3_musique `Unknown name in expression: composition_reference`。T1 夹具 SVP 可写（`edits.jsonl` 第二行），不掩盖 T3 断线。
- **影响：** 作者 close-out「persist source_value_pair」在 T1 可演示，在 T3 用户 CLI 上把原先能跑的 prepare 打掉。`t3_musique` 别名因此无法单独关闭 E6-13。
- **建议：** 只在可 `recompute` 的完全图上写 SVP；域 `Edit` 已存在时不要再跑 `apply_value_edit`/`apply_rename_edit`。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 开审冻结可复现 | 开审 **HASH_MATCH** `9814019a…`；交卷漂移见 E7-01 |
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError` |
| `latest` 拒绝 | `write_run_spec(..., "latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `Unknown source_kind 'made_up'` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 |
| runbook 目录 `--in-dir` 文件哈希与上游字节一致 | §3.2 HASH VERIFY 全 True |
| `--labels-dir` 进入 **fit** `input_hashes` | §3.2 |
| `Trace.from_dict` 回载 | §3.4 |
| 完整产物 `--resume` 成功 | §3.6 八段 exit 0 |
| 篡改/缺 shard 时 `--resume` 拒绝且 **不覆盖** 成功清单 | E7-02 / E7-03 |
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
| 文件 `--in-dir` 不留半截 collect / 不先写 report | E7-07 |
| scientific 拒绝 offline H / 无 fractions / 字面量校准 | §3.8 |
| humaneval 不再 value-edit 成 `"2"` | §3.10 |
| infinity JSON | `q=null`，`infinity=true`（E7-04） |
| 七段缺 in-dir 失败 | E7-14 / E7-17 |
| tiny 重分词 + `H_pre` 堆叠 | E7-11 / E7-12 |
| calibrate 认 `label`/`lab`/`labels` + `prepare/`/`s-prep/` | E7-10 / E7-16 |
| repair `record_id` 含 group 与 k | E7-15 |
| scientific prepare 非空生成区事件 | 6 events；`parse_region=generated` |
| scientific fit 有限 probes | E7-09 |
| scientific intervene 有 donor | E7-18 |
| `--sidecar` 接通 GSM-Symbolic | §3.10 |
| `t4_boundary` 别名接通 | §3.10 |
| `ChildProcessExecutor is not IsolatedExecutor` | §3.9 |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径。`ChildProcessExecutor` 不是沙箱 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |
| 声称冻结 `9814019a…` 的原始 60 文件字节 | 已被覆盖，无法在本工作区重放 |

## 8. 结论

**`HASH_MISMATCH`**。声称 `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（60 文件）在开审可复现；交卷当前树为 `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`（仍 60 文件）。冻结未守住（E7-01）。

夹具烟测按 runbook 八段（collect=**tiny**，calibrate 带 `--features-dir`）**全部退出码 0**。scientific tiny 按同一用户顺序：**八段全部退出码 0**。fit 写出无 NaN 的 `probes.jsonl`；intervene **不是** `donor_missing`；calibrate 找到 `prepare/` / `s-prep/` 祖先。这只证明 tiny 夹具/约束接口能写文件，**不证明** OPS-01，也 **不是** 科学全跑。

相对 r06 作者 close-out，本通道独立确认：

| r06 / 作者声称 | 独立复跑（当前字节） |
|---|---|
| E6-09 scientific fit 拒 NaN、不写 NaN JSON | **成立**（E7-09） |
| E6-13 `t3_musique`/`t4_boundary` 别名 + `--sidecar` | 别名/`--sidecar`/`t4_boundary` **字面成立**；`t3_musique` prepare 仍失败；非整条关闭（E7-13） |
| E6-16 calibrate 祖先含 `prepare/`/`s-prep/`，优先 `event_rows` | **成立**（E7-16） |
| E6-17 calibrate/intervene/repair 无 `--in-dir` 失败 | **成立**（E7-17） |
| E6-18 不可表达行不入 H；intervene 按有限同 `node_id` 配对 | **成立**（E7-18） |

另独立关闭：失败不覆盖成功清单、resume command、`--features-dir` + infinity JSON、per-trace shard、Event `record_id`、analyze 文件 in-dir 先验、tiny 重分词、repair `record_id` 含 group/k。

仍不通过的核心项：声称冻结与交卷树不一致（E7-01）；T2/T3 不是与 T1 同等用户 CLI，且 `source_value_pair` 打断 hotpot/musique（E7-13 / E7-19）。Exit 0 不能当作 OPS-01。`ChildProcessExecutor` 不能当作 `IsolatedExecutor`。

**本通道不通过** OPS-01。**FAIL**。空通过或「测试绿了」或「tiny 八段 exit 0」不能作为本通道结论。作者对 E6-09/16/17/18 的字面关闭在当前字节 **独立确认**；E6-13 的别名/sidecar 字面关闭，**「同等 CLI」不能关闭**。

下一步（建议，非本通道实施）：重新冻结并重开审查；SVP 不要套在 T3 域编辑上；不要把 tiny exit 0 登记为 OPS-01。
