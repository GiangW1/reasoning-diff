# E：端到端工程审查（round-06）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮 A–D/F 通道报告。`ISSUES.md` 作者本地关闭声明（E5-09/10/11/12/13/14/15）已独立复测，不采信作者关闭声明。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。

**冻结核验：`HASH_MATCH`。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 01:50–02:25 +08:00 |
| 声称冻结 hash | `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（用户给定；与 `.planning/audits/round-06/VERSION.md` 一致） |
| 独立复算冻结 hash | **`HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**59** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；从 `%TEMP%` cwd 调用相同） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch 2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户 CLI 跨模块路径：prepare→collect→label→fit→calibrate→intervene→repair→analyze，夹具 **与** scientific tiny；resume/manifest、`--features-dir`、`--labels-dir`、`--shard`、`--kind` 别名、缺 `--in-dir`、repair `record_id`；按 `docs/SERVER_RUNBOOK.md` 本机命令实跑 |
| r05 声称（独立复跑） | scientific 不再因 0 事件在 fit 处断裂；calibrate 认 `label`/`lab`；collect 必有 in-dir；`H_pre` 全轨迹堆叠 |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md` |
| 实跑入口 | `python -m reasoning_diff`（runbook 命令）；产物根 `%TEMP%\rd-e-r6-7zjpd59x\`，未写入 `src/` / `tests/` / `pyproject.toml` |

**冻结说明：** 审查对象是当前工作区字节，且与声称冻结 hash **一致**。本报告绑定该快照。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–1052 | 通读 + `python -m` 夹具八段 + scientific tiny + resume/负路径 + `--kind` + `--shard` + 缺 in-dir | collect/analyze 无 in-dir 失败；scientific 有事件但 fit 因 NaN JSON 断；calibrate 认 `label`/`lab`/`labels`，祖先只认 `prep` 不认 runbook `prepare` |
| `src/reasoning_diff/artifacts.py` | 1–85 | 通读 + digest / `success_count` / shard | digest 自洽；`success_count` 缺省 0；`completed_shard_ok` 函数正确，CLI 仍用刚算出的 hash 自检 |
| `src/reasoning_diff/io.py` | 1–133 | 通读 + NPZ/NaN/`runtime_info` | JSON/JSONL/NPZ 临时文件+`os.replace`；拒 object；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | 通读 + `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–52 | 对照实跑 | 现含 `--features-dir`；resume 说明与实跑一致；隔离仍 `pending_server`；calibrate 祖先回退目录名是代码里的 `prep`，不是 runbook 的 `runs/prepare` |
| `src/reasoning_diff/executor.py` | 1–109 | `get_executor` / subprocess | 默认 Unavailable；`ChildProcessExecutor.isolated_sandbox=False`；拒 `exec(`/`eval(` |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–385 | 通读 + 产物 `from_dict` | Event `record_id` 含 `run_id`；`Trace.from_dict` 把未知键并入 metadata |
| `src/reasoning_diff/splits.py` | 1–111 | CLI `require_split` | test 上 fit、probe_train 上 calibrate 仍拒绝 |
| `src/reasoning_diff/edits.py` | 默认 prepare `p2→2` | 夹具 prepare 实跑 | 重算答案 8；编辑 Task `task_id=fix-t1-001::p2=2` |
| `src/reasoning_diff/events.py` | 1–261 | prepare 解析 | 夹具 `parse_fixture_events`（仅 nodes）；scientific `parse_events`（premises+nodes）+ 约束 `q = <digits>` |
| `src/reasoning_diff/graphs.py` | 1–46 | prepare `ancestors` / calibrate `R(s_i)` | CLI calibrate 用 `anc.get`；无 tasks 则 RSI 为空 |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 observation 则无 task/behavior 标签 |
| `src/reasoning_diff/models/collect.py` | 1–192 | tiny collect / swap decode | 按传入 `token_ids` 取隐状态；CLI 现在先 `encode_text(trace.text)` |
| `src/reasoning_diff/models/generate.py` | 66–182 | scientific prepare | `append_target_assignment` 追加 `\nq = <digits>`；0 事件标 `parse_failed` |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | `pre_step` 在 `start=0` 时 `token_index=None` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | collect 重分词 | `encode_text` 按字符 `ord`；与夹具合成 `range(1,n)` 不等 |
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | `fit` | H 含 NaN 时 `U`/`V`/`b` 变 NaN，`encode` 拒绝 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `conformal_threshold` / `sequence_score` | `empty_truth→0.0`；`k>n` 返回 `q=inf`；CLI `_sanitize_cal` 写成 `q=null` + `infinity=true` |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | `allclose(..., equal_nan=True)` 把双 NaN 行当成无 donor |
| `src/reasoning_diff/repair.py` | 1–217 | `repair` | scientific `k=1..5` 且 `refilled_prefix=true`；CLI 覆写 `record_id` |
| `src/reasoning_diff/analysis.py` | 1–337 | `analyze` | 读 densities sidecar；标签不足 4 行双类 → `p1=null` / `not_evaluated` |
| `src/reasoning_diff/transfer.py` | 1–75 | analyze `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | prepare `--kind` | t2/t3 部分别名；`t3_musique`/`t4_boundary` 未知 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–84 | `--kind gsm_symbolic` | CLI 不传 sidecar；无非 placeholder 前提 → prepare 失败 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 50–76 | `--kind gsm_plus` / `t2_gsm_plus` | 隔离替换 `"4"→"5"` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–78 | `--kind humaneval` / `t3_humaneval` | `apply_spec_edit` 追加 `# variant` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 51–104 | `--kind hotpot` / `t3_hotpot` | `document_edit` |
| `src/reasoning_diff/tasks/t3_musique.py` | 72–110 | `--kind musique` | `paragraph_edit`（注解写 `-> Task`，运行返回 `Edit`） |
| `src/reasoning_diff/tasks/t4_boundary.py` | 36–51 | `--kind t4` | `apply_t4_question_edit` |
| `src/reasoning_diff/rng.py` | 1–53 | intervene `StreamBank` | CLI intervene 使用；prepare 未用 |
| `src/reasoning_diff/baselines.py` | 1–125 | CLI `fit` 调用 verbalizer / attention | 本轮 fit 产物含四档 verbalizer、BoundaryMLP、attention_* |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | CLI fit 调用 | 写入 `baseline=boundary_mlp` |
| `tests/test_cli_pipeline.py` | 1–31 | 读，未当作验收 | 只断言 exit 0 / `not_evaluated`；calibrate **无** `--features-dir` |

**抽样未做完整工程审查（非本通道主路径）：** `models/tiny.py`、`models/adapters.py`、T1 official 内部、`t2_noop.py`。确认 adapters **未被** 八段通用子命令调用。

## 3. 已执行检查与结果

### 3.1 用户 CLI 入口

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`%TEMP%`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir` |
| `calibrate --help` | **0** | 有 `--features-dir` **与** `--labels-dir`（runbook L29 写了前者） |
| `fit --help` | **0** | 有 `--labels-dir` |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**；另跑 offline 对照）

产物根：`%TEMP%\rd-e-r6-7zjpd59x\fx\`。夹具 `tests/fixtures/t1_tiny.json`。`--in-dir` 按 runbook 指向上一阶段。目录名用 runbook 的 `prepare` / `collect` / `label` / `fit` / `cal`。

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
| prepare | `{t1_tiny.json: …}` | `[]` | 夹具；默认 `p2→2` |
| collect tiny | prepare 全目录文件 + `upstream_manifest*`（与 prepare 字节 **全等**，HASH VERIFY 全 True） | 重算 prepare digest `2fdc2473…` | 读 `tasks.jsonl` + `traces.jsonl`；对 `trace.text` **重新** `encode_text`；`weight_source=random_init` |
| label | 哈希 prepare 全目录 | `[2fdc2473…]` | `observations.jsonl` + `tasks.jsonl`；`build_labels` |
| fit | collect 文件 **加** `label/labels.jsonl` 等 | collect + label 两枚重算 digest | 读 `H`/`E` + labels-dir；双头探针 + verbalizer/MLP/attention |
| calibrate（`--features-dir collect`） | fit + collect 文件 | 两枚 digest | `predict_matrix`；找到 `label/labels.jsonl` 但 RSI 空 → **空真理分数**（§3.2c） |
| intervene | collect | collect digest | tiny `H` 两行不等 → `status=prospective_decode`，`timing=offline_hidden` |
| repair | prepare 全目录 | prepare digest | 默认 backend≠tiny → `prefill_unavailable`；`record_id=repair:fix-t1-001:task_oracle:k1` |
| analyze | label 文件 | label digest | densities sidecar；`p1/p2/p3=null`，`status=not_evaluated` |

各阶段 `manifest.digest` 均自洽。八个阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。

`collect` 无 `--in-dir` exit **1**，`collect requires --in-dir`。`analyze` 无 `--in-dir` exit **1**（fixture 与 scientific 相同）。`calibrate` / `intervene` / `repair` 无 `--in-dir` 仍 exit **0**（§3.7）。

#### 3.2b tiny 对照（夹具 collect）

`collect --backend tiny` exit **0**：`weight_source=random_init`，`H`/`E`/`H_pre_*`/`H_post_step` 均为 `[2,32]`。`H[0]` 与 `H[1]` **不等**（`maxabs=0.0056705`）。写出的 `traces.jsonl` 仍保留 prepare 的合成 `token_ids=range(1,21)`（两条相等）；`encode_text(text)` 得到不同 ID（`[50,50,33,…]`），隐状态按重分词前向。`intervene --in-dir <tiny>` → `status=prospective_decode`，`followed_donor=false`，`invalid=1.0`，几何 `timing=offline_hidden`。

offline collect：`H` `[1,8]`，`token_prefix` 为合成 ID 前 8 项，`weight_source=offline_prefix_ids`。

#### 3.2c calibrate 目录名 / `--labels-dir` / 祖先目录

`--features-dir` 能让 `predict_matrix` 跑通。同一套 fit/collect（tiny，`pred≈0.995`），只改标签目录与内容：

用 **可区分** 标签（`premise_id=q`，使 RSI=`{q}` 在无祖先时也能命中）：

| 布局 | `scores` |
|---|---|
| 兄弟目录 `label/labels.jsonl` | `[0.00502325, 0.00502334]` |
| 仅 `lab/labels.jsonl` | 同上 |
| 仅 `labels/labels.jsonl` | 同上 |
| 仅 `othername/labels.jsonl`（无 flag） | `[0.0, 0.0]`（**未消费**） |
| `--labels-dir othername`（同样 q 标签） | `[0.00502325, 0.00502334]` |
| `--labels-dir` 指向不匹配 premise | `[0.0, 0.0]`（`empty_truth`） |

**runbook 真实标签**（`event_id=q`，`premise_id=p2`）：

| 祖先来源 | `scores` / `q` |
|---|---|
| 无 `tasks.jsonl`（fit 目录没有；代码也不读 `prepare/`） | `[0.0, 0.0]`，`q=0.0`，`status=finite` |
| 兄弟目录 `prep/tasks.jsonl`（代码写死） | `[0.00502325, 0.00502334]`，`q=0.00502334` |
| 兄弟目录 `prepare/tasks.jsonl`（runbook 名） | `[0.0, 0.0]`（**不认**） |

本轮第一次 runbook 烟测 `fx/cal` 的 `scores=[0.0,0.0]` 就是「找到了 `label/`，但 RSI 只有 `{q}`、`p2∉RSI` → `empty_truth=0.0`」。`input_hashes` **不含** 任何 labels 文件，即使传了 `--labels-dir`。

无 `--features-dir`：`status=probe_weights_or_features_missing`，`scores=null`，fixture 下 exit **0**。

offline 特征 + 对应 offline fit：`n=1`，`k=2`，`q=null`，`infinity=true`，JSON 可写。tiny-fit（32 维）配 offline 特征（8 维）→ `matmul` 维度错误 exit 1。

### 3.3 scientific tiny 八段

runbook 局部命令 + 本通道把后段也加上 `--eval-mode scientific`（calibrate/analyze）与 `--backend tiny`（collect/intervene/repair）。`--split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。

| 命令 | 退出码 | 要点 |
|---|---|---|
| `prepare --eval-mode scientific --split-fractions … --sham-opportunities 1` | **0** | 6 条 `tiny-qwen2` 轨迹；文本形如 `p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82`；`parse_status=ok`；**18** events（每迹 p1/p2/q），**12** observations，prepare 标签 7 行已知字段 |
| `collect --backend tiny --eval-mode scientific` | **0** | `H`/`H_pre_step` **`[18,32]`**（全轨迹事件堆叠）；`E` `[2,32]`（mean-pool）；`H` **12/18 行全 NaN**（p1/p2 的 `start=0`，`pre_step` 无前缀 token）；6 行 q 有限 |
| `label` | **0** | 8 行（7 标签 + densities）；其中 **5** 行 `task_label`/`behavior_label` ∈ {0,1} |
| `fit --labels-dir <s-lab>` | **1** | **不是**「0 事件 / identity labels」。`ValueError: Out of range float values are not JSON compliant`（NaN `U`/`V`/`b`）；失败清单 `success_count=0` |
| `calibrate --features-dir <s-col> --eval-mode scientific` | **1** | 无 `probes.jsonl` → `scientific calibrate refuses loss or literal scores` |
| `intervene --backend tiny` | **0** | `H[0]`/`H[1]` 皆 NaN，`allclose(..., equal_nan=True)` → `status=donor_missing`，`timing=unexpressible` |
| `repair --eval-mode scientific --backend tiny` | **0** | `k=1..5`，`refilled_prefix=true`，`record_id=repair:fix-t1-001:task_oracle:k{1..5}` |
| `analyze --eval-mode scientific --in-dir <label>` | **0** | `p1=p2=p3=null`，`scientific_conclusion=null`，`status=not_evaluated`（task 标签不足 4 行双类） |

**r05「不再因 0 事件在 fit 处断裂」：** 事件不再为空，fit **不再**抛 `fit refuses identity labels`。用户 CLI 科学八段 **仍在 fit 处断裂**，原因换成 NaN 权重无法 JSON。夹具 exit 0 不能掩盖这条断线。

### 3.4 schema / shape / ID

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `review_export.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

Observation（夹具精确一行）：`outcome=changed`，`raw_values=["0","8"]`，`record_id=prepare:{identity}:p2`，`run_id=prepare`，`base_group_id=fix-t1-001`。默认编辑仍为 **p2:0→2**。合成轨迹 `"p1 = 4\np2 = 0\nq = 0\n"` / `"p1 = 4\np2 = 2\nq = 8\n"`。这是夹具有效扰动，**不是**科学全量扫描。

身份合同（本轮实测）：

1. 夹具 `events.jsonl` 两行 `record_id` 为 `trace-base:{identity}` 与 `trace-edit:{identity}`，彼此不同。scientific 18 行按 `trace-*:{entity}` 区分。
2. 两行 Task：`fix-t1-001` 与 `fix-t1-001::p2=2`。
3. prepare Label：`record_id=prepare:q:p2`。label 阶段重写为 `record_id=label:q:p2`，`run_id=label`。
4. collect `Trace.from_dict` → 成功。仅首行 traces 被写入 feature metadata。
5. tiny 夹具 `H`/`H_pre_*` 均为 `[2,32]`（2 轨迹 × 1 事件）。scientific `H`/`H_pre_*` 均为 `[18,32]`（6 × 3），**不再**是最后一条轨迹的 `[1,32]`。`E` mean-pool 为 `[2,32]`。
6. Repair 夹具：`record_id=repair:fix-t1-001:task_oracle:k1`，`base_group_id=fix-t1-001`，`k=1`，`status=prefill_unavailable`。scientific：`k=1..5` 填齐，同一 `base_group_id`。无 `--in-dir` 时退回 `record_id=repair::task_oracle:k1`。
7. 夹具写出的 `token_ids` 仍是 `range(1, len(text)+1)`；collect 前向用的是 `encode_text(text)`。scientific `token_ids` 为 tiny 解码 ID（例：`[50,50,33,…]`）。

### 3.5 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：tasks/edits/splits/events/observations/labels/traces/run_spec/manifest **九文件 hash 全等**。
- `write_run_spec(..., code_revision="latest")` → `ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind` → `ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})` → `ValueError`（`allow_nan=False`）。这正是 scientific fit 的失败模式。
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

`main` 的 `except`（`cli.py:1025–1048`）仍写 `failure.json`；若已有 `success_count` 或 `record_counts.success`，**不再** `write_manifest` 覆盖成功清单。

### 3.7 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 不存在 | **1** `FileNotFoundError` | `failure.json` + 失败清单（`success_count=0`） |
| `collect` 无 `--in-dir` | **1** `collect requires --in-dir` | 失败清单 |
| `label` 无 `--in-dir` | **1** `label requires --in-dir with observations.jsonl` | 失败清单 |
| `analyze` 无 `--in-dir`（fixture **与** scientific） | **1** `analyze requires --in-dir` | 失败清单；**无** `report.json` |
| `fit` 无 `--in-dir` | **1** `fit requires features.npz from collect` | 失败清单（`src` 回落到空 `out`） |
| `calibrate` 无 `--in-dir`（fixture） | **0** | **成功**清单；`scores=null`，`status=probe_weights_or_features_missing` |
| `intervene` 无 `--in-dir` | **0** | **成功**清单；`status=donor_missing` |
| `repair` 无 `--in-dir` | **0** | **成功**清单；`record_id=repair::task_oracle:k1` |
| `calibrate` 无 `--in-dir` + scientific | **1** | `scientific calibrate refuses loss or literal scores` |
| `fit --split test` | **1** `probe fit cannot fit on test` | 失败清单 |
| `calibrate --split probe_train` | **1** `calibration cannot fit on probe_train` | 失败清单 |
| `--in-dir docs/SERVER_RUNBOOK.md` + collect / calibrate / intervene / repair / analyze | **1** `NotADirectoryError`（`_upstream` 或 analyze 先验） | 仅失败清单；**无** features / 阶段 jsonl / `report.json` |
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
| `collect --backend tiny --eval-mode scientific` | **0** | 接受 `random_init`；**不**拒绝全 NaN 的 `pre_step` 行 |
| `calibrate` 无 probes + scientific | **1** | `scientific calibrate refuses loss or literal scores` |
| `analyze` 无 `--in-dir` + scientific | **1** | `analyze requires --in-dir`（现与 fixture 相同） |
| 完整 scientific 八段 | fit/calibrate **1** | 见 §3.3；门禁挡了空标定，链路本身未接通 |

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
SubprocessExecutor + 合法 assert：ok
SubprocessExecutor + 失败 assert：failed
SubprocessExecutor + exec(：rejected
SubprocessExecutor + sleep + timeout=0.2：timeout
score_numeric("4","4") → 1.0；score_qa("Paris","paris") → 1.0
```

生产路径未见 `exec(` / `eval(` 作为评分回退。普通 subprocess **不能**冒称 Linux cgroup 沙箱（runbook 仍标 `pending_server`）。

### 3.10 T2–T4 `--kind`

| `--kind` | 退出码 | 编辑器 | 备注 |
|---|---|---|---|
| `gsm_plus` / `t2_gsm_plus` | **0** | `apply_plus_numeric_edit` `4→5` | 别名接通 |
| `gsm_plus`（问句无 `"4"`） | **1** | 域编辑抛错后回落到 `_default_edit` | `no editable non-placeholder premise` |
| `gsm_symbolic` / `t2_gsm_symbolic` / `symbolic` | **1** | 别名能进 catalog；无 sidecar、无域分支 | `no editable non-placeholder premise` |
| `hotpot` / `t3_hotpot` | **0** | `document_edit` | `DocA` → `"replacement"`；events/obs 空 |
| `humaneval` / `t3_humaneval` | **0** | `apply_spec_edit` / `kind=input_list` | after 为 prompt+`\n# variant` |
| `musique` | **0** | `paragraph_edit` | `p0` → `"replacement only"`；4 events / 2 obs |
| `t3_musique` | **1** | catalog 无此别名 | `unknown snapshot kind t3_musique` |
| `t4` | **0** | `apply_t4_question_edit` | 问句追加 ` ?` |
| `t4_boundary` | **1** | catalog 无此别名 | `unknown snapshot kind t4_boundary` |

label / fit / analyze **无** `--kind`。这不是与 T1 同等的域流水线。catalog 对 t2/t3 **部分**别名已接通；`t3_musique` / `t4_boundary` 与 `gsm_symbolic` 准备阶段仍失败。

### 3.11 atomic NPZ

`write_npz`：拒 object → `mkstemp` → `np.savez` → `os.replace`。成功后无残留。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 把 pytest / 作者「136 passed」当验收 | 夹具绿测不是科学全跑，也不是 OPS-01 |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境 |
| 真实模型 / GPU / 官方数据 | `pending_server` |
| 并发真实分片崩溃注入 | `--shard` 现为每轨迹一份副本，不是按组调度 |
| 阅读本轮 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。编号为本轮 `E6-##`。

---

### E6-01 声称冻结 hash 与当前树一致（closed）

- **状态：** **closed**
- **文件：** `.planning/audits/round-06/VERSION.md`；59 个范围内文件
- **复现 / 证据：** §1。独立复算 = 声称值 `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`。**`HASH_MATCH`**。

---

### E6-02 失败 `main` 不再覆盖成功清单（closed，原 E5-02 / E4-08）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `main` 1025–1048
- **复现 / 证据：** §3.6。篡改 traces 或删除 shard 后 `--resume`：写出 `failure.json`，`manifest.file_hashes` / `success_count=1` / `digest` 与失败前 **全等**。

---

### E6-03 `--resume` 的 command 键与写出 config 对齐（closed，原 E5-03 / E4-09）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `_resume` 54–58；`_write_stage` 141
- **复现 / 证据：** §3.6。prepare 默认 `--resume` 以及后七段完整产物 `--resume` **全部 exit 0**。

---

### E6-04 `--features-dir` 可消费权重；infinity 可 JSON（closed，原 E5-04 / E4-10）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `_sanitize_cal` 613–619；`cmd_calibrate` 622–694
- **复现 / 证据：** §3.2 / §3.2c。`--features-dir` 进入 `predict_matrix`。offline 路径 `n=1`：`q=null`，`infinity=true`，`status=infinity`。

---

### E6-05 `--shard` 按轨迹各写一份（closed，原 E5-05 / E4-11）

- **状态：** **closed**
- **复现 / 证据：** §3.6。`--shard` → 两个 1 行 shard；不加 flag → 无 shard 文件。

---

### E6-06 Event/Label `record_id` 含 `run_id` 且跨轨迹不碰撞（closed，原 E5-06）

- **状态：** **closed**
- **复现 / 证据：** §3.4。夹具 2 条、scientific 18 条 Event `record_id` 互异。

---

### E6-07 analyze 在写 `report.json` 之前拒绝文件 `--in-dir`（closed，原 E5-07 / E4-16）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `cmd_analyze` 850–851（先于 954 `write_json`）
- **复现 / 证据：** §3.7。fixture 与 scientific 的文件 `--in-dir` 均 **无** `report.json`。

---

### E6-08 `--eval-mode scientific` 门禁仍在（closed 存在性；不是科学全跑）

- **状态：** **closed**（缺 flag）
- **复现 / 证据：** §3.8。offline collect / 无 fractions / 无 features 的 scientific calibrate 均 exit 1。

---

### E6-09 scientific tiny 用户 CLI 仍在 label→fit→calibrate 处断裂（confirmed defect；E5-09 的 0 事件字面关闭，链路未接通）

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `models/generate.py` 137–151：约束追加 `\nq = <digits>`，`parse_events` 现能抽出 p1/p2/q
  - `cli.py` 291–292：0 事件才 `parse_failed`（本跑未触发）
  - `models/features.py` / `events.boundary_index`：`start=0` 的 `pre_step` → `token_index=None`
  - `models/collect.py` 51–52：缺失 index 写成 **NaN 行**，仍标 `h_position=pre_step`
  - `cli.py` 449–450：scientific collect 只拒 `shape[0]==0`，**不拒** NaN
  - `probes/bilinear.py` 48–66：`H` 含 NaN → `U`/`V`/`b` 非有限
  - `io.encode` `allow_nan=False`；`cli.py` `cmd_fit` 写 `probes.jsonl`
- **触发条件：** runbook「local scientific」prepare + 后续 label/fit/calibrate。
- **对应要求：** OPS-01 用户 CLI 跨模块路径。
- **复现 / 证据：** §3.3。18 events、12 obs、5 行 0/1 标签。fit **不再**报 `fit refuses identity labels`。fit exit 1：`Out of range float values are not JSON compliant`。`H` 18×32 中 **12 行全 NaN**（每条轨迹的 p1/p2 与问句同一行、`start=0`）。calibrate scientific 因无 probes 再断。
- **对 r05 声称：** 「不再因 0 事件在 fit 处断裂」——0 事件原因 **已消失**；**fit 仍失败**。不能把「有事件」写成「八段可调度」。
- **影响：** 作者 close-out 只证明 prepare 能写出可解析轨迹，**不能**证明 scientific 八段可走完。
- **建议：** 无前缀 token 的 `pre_step` 不得写入可拟合的 H 行；或 fit 在写出前拒绝非有限权重。

---

### E6-10 calibrate 认 `label`/`lab`/`labels` 与 `--labels-dir`（closed 目录发现，原 E5-10；消费残留见 E6-16）

- **状态：** **closed**（「认目录名 / 有 `--labels-dir`」字面）
- **文件 / 符号 / 行号：** `cli.py` 639–651
- **复现 / 证据：** §3.2c。`premise_id=q` 的可区分标签下，`label` / `lab` / `labels` / `--labels-dir` 得到非零 `one_minus_p`；兄弟目录 `othername` 无 flag 时分数为 `empty_truth` 的 `[0,0]`。
- **作者「E5-10」在「认 label/lab/labels + --labels-dir」字面范围独立关闭。**

---

### E6-11 夹具 tiny collect 重分词后 H 可区分（closed，原 E5-11）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` 443–448：`encode_text(trace.text)`
- **复现 / 证据：** §3.2b。`H[0]≠H[1]`（`maxabs=0.00567`）；intervene `prospective_decode`。写出 traces 仍带合成 `range` ID，这是残留记录，不重开本条。

---

### E6-12 多轨迹 `H_pre_*` 与 `H` 同样按事件堆叠（closed，原 E5-12）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` 440–465：`pre_s`/`pre_v`/`post` 按轨迹 `vstack`；`E` mean-pool
- **复现 / 证据：** 夹具 tiny：`H` 与 `H_pre_*` 均为 `[2,32]`。scientific：`H` 与 `H_pre_*` 均为 `[18,32]`（不再是 `[1,32]`）；`E` `[2,32]`。NaN 行是 E6-09，不重开堆叠合同。

---

### E6-13 T2/T3/T4 `--kind` 仍不是与 T1 同等的用户 CLI（confirmed defect，原 E5-13 残留）

- **严重度：** medium
- **状态：** confirmed defect（部分别名 **不能**关闭整条）
- **文件 / 符号 / 行号：** `cli.py` `_domain_edit` 182–208；`catalog.py` 15–45
- **复现 / 证据：** §3.10。`t2_gsm_plus` / `t3_hotpot` / `t3_humaneval` 别名 exit 0。`gsm_symbolic` 三个别名均 exit 1。`t3_musique` / `t4_boundary` 为 `unknown snapshot kind`。label/fit/analyze 无 `--kind`。
- **对应要求：** OPS-01 + DATA-02

---

### E6-14 collect / analyze 无 `--in-dir` 必须失败（closed，原 E5-14；其他阶段残留见 E6-17）

- **状态：** **closed**（collect / analyze / label）
- **文件 / 符号 / 行号：** `cli.py` 416–417；848–849；512–513
- **复现 / 证据：** §3.2 / §3.7。三条均 exit 1，分析不写 `report.json`。

---

### E6-15 Repair `record_id` 含 `base_group_id` 与 `k`（closed，原 E5-15）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `cmd_repair` 831–840
- **复现 / 证据：** §3.4。夹具 `repair:fix-t1-001:task_oracle:k1`；scientific `k1..k5`。不再出现 `kNone` 或空 `base_group_id`（有 traces 时）。

---

### E6-16 runbook calibrate 找到标签后仍走空真理（confirmed defect）

- **严重度：** high
- **状态：** confirmed defect（不重开 E6-10 的目录发现）
- **文件 / 符号 / 行号：** `cli.py` 663–666：祖先只读 `src/tasks.jsonl` 或 `features.parent/prep/tasks.jsonl`；runbook 目录是 `runs/prepare`，fit 也不写 tasks
- **触发条件：** 按 runbook：`label → runs/label`，`calibrate --in-dir runs/fit --features-dir runs/collect`，真实标签 `premise_id=p2`
- **对应要求：** OPS-01 校准阶段消费上游标签；runbook L27–29
- **复现 / 证据：** §3.2c。runbook 烟测 `scores=[0.0,0.0]`。手动放置 `prep/tasks.jsonl` 后变为 `0.005023…`。放置 `prepare/tasks.jsonl` **无效**。`empty_truth` 与「找到 label 目录」可以同时成立。`input_hashes` 仍不含 labels。
- **影响：** 文档路径看起来成功，分数是空真理 0，不是探针非conformity。第一次烟测不能当作 runbook 已接通 RSI。
- **建议：** 读 `prepare/`（或 `--labels-dir` 的上游 tasks）；把标签文件写入 `input_hashes`。

---

### E6-17 fixture 下 calibrate / intervene / repair 无 `--in-dir` 仍成功（confirmed defect，E5-14 残留）

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` `cmd_calibrate` 627（`src` 可空）；`cmd_intervene` 701；`cmd_repair` 815
- **触发条件：** 用户要求「缺 `--in-dir` 必须失败」；fixture 默认 `eval-mode`
- **复现 / 证据：** §3.7。三阶段 exit 0、`success_count=1`。scientific calibrate 无 in-dir 因门禁才失败。
- **影响：** 调度器无法把「缺上游」从成功阶段里区分出来。

---

### E6-18 scientific intervene 把 NaN 行当成无 donor（confirmed defect）

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 712：`np.allclose(..., equal_nan=True)`
- **复现 / 证据：** §3.3。scientific `H[0]`/`H[1]` 皆为 p1@`start=0` 的 NaN 行 → `donor_missing` / `timing=unexpressible`。夹具 tiny 因有限且不等，能走到 `prospective_decode`。
- **影响：** 有 18 行特征仍不能做干预；与 E6-09 同源。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 冻结 hash 复现 | **HASH_MATCH** E6-01 |
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError`；scientific fit 由此失败（缺陷在写入 NaN，不在拒 JSON） |
| `latest` 拒绝 | `write_run_spec(..., "latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `Unknown source_kind 'made_up'` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 |
| runbook 目录 `--in-dir` 文件哈希与上游字节一致 | §3.2 HASH VERIFY 全 True |
| `--labels-dir` 进入 **fit** `input_hashes` | §3.2 |
| `Trace.from_dict` 回载 | §3.4 |
| 完整产物 `--resume` 成功 | §3.6 八段 exit 0 |
| 篡改/缺 shard 时 `--resume` 拒绝且 **不覆盖** 成功清单 | E6-02 / E6-03 |
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
| 文件 `--in-dir` 不留半截 collect / 不先写 report | E6-07 |
| scientific 拒绝 offline H / 无 fractions / 字面量校准 | §3.8 |
| humaneval 不再 value-edit 成 `"2"` | §3.10 |
| infinity JSON | `q=null`，`infinity=true`（E6-04） |
| collect/analyze/label 缺 in-dir 失败 | E6-14 |
| tiny 重分词 + `H_pre` 堆叠 | E6-11 / E6-12 |
| calibrate 认 `label`/`lab`/`labels` | E6-10 |
| repair `record_id` 含 group 与 k | E6-15 |
| scientific prepare 非空事件 | 18 events；0 事件拒绝仍在代码里 |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |

## 8. 结论

**`HASH_MATCH`** `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（59 文件）。

夹具烟测按 runbook 八段（collect=**tiny**，calibrate 带 `--features-dir`）**全部退出码 0**。这只证明夹具能写文件，**不证明** OPS-01，也 **不是** 科学全跑。scientific tiny 按同一用户顺序：**prepare/collect/label/intervene/repair/analyze 为 0，fit 与 calibrate 为 1**。

相对 r05 声称，本通道独立确认：

| r05 声称 | 独立复跑 |
|---|---|
| scientific 不再因 **0 事件** 在 fit 处断裂 | **字面成立**（18 events，不再 `refuses identity labels`）；**链路不成立**（fit 改因 NaN JSON 失败，E6-09） |
| calibrate 认 `label`/`lab` | **成立**（E6-10）；runbook 真实 `p2` 标签仍走空真理（E6-16） |
| collect 必有 `--in-dir` | **成立**（E6-14）；analyze 现同样必有 |
| `H_pre` 全轨迹堆叠 | **成立**（E6-12） |

另独立关闭：失败不覆盖成功清单、resume command、`--features-dir` + infinity JSON、per-trace shard、Event `record_id`、analyze 文件 in-dir 先验、tiny 重分词、repair `record_id` 含 group/k。

仍不通过的核心缺陷：scientific 八段在 NaN `H`→fit JSON 处断开（E6-09）、runbook calibrate 的 RSI 不读 `prepare/`（E6-16）、缺 `--in-dir` 时 calibrate/intervene/repair 仍成功（E6-17）、`gsm_symbolic` / `t3_musique` / `t4_boundary` 不是同等 CLI（E6-13）。Exit 0 不能当作 OPS-01。

**本通道不通过** OPS-01。**FAIL**。空通过或「测试绿了」不能作为本通道结论。作者对 E5-10/11/12/14/15 的字面关闭在本通道 **独立确认**；E5-09 的「0 事件」字面关闭，**「scientific 八段可调度」不能关闭**。

下一步（建议，非本通道实施）：拒绝或丢弃 `start=0` 的 NaN `pre_step` 行；calibrate 祖先读 `prepare/`；缺 `--in-dir` 的 calibrate/intervene/repair 失败；`gsm_symbolic` 接入 sidecar。
