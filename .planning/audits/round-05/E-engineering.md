# E：端到端工程审查（round-05）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮 A–D/F 通道报告。`ISSUES.md` 中作者标为本地已关的「E4-08 失败不覆盖成功清单、E4-09 resume command、E4-10 `--features-dir` + infinity JSON、E4-11 per-trace shard、E4-12 record_id 含 run_id、E4-14 域编辑器、E4-16 analyze 先验 in-dir」已独立复测，不采信作者关闭声明。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。

**冻结核验：`HASH_MATCH`。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 01:33–02:20 +08:00 |
| 声称冻结 hash | `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（用户给定；与 `.planning/audits/round-05/VERSION.md` 一致） |
| 独立复算冻结 hash | **`HASH_MATCH`**。按 VERSION 脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**58** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；从 `%TEMP%` cwd 调用相同） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch 2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户 CLI 跨模块路径；schema/shape/ID、run_spec/manifest、resume（command 键必须对齐）、失败不得覆盖成功清单、shards、异常、隔离、T2–T4 `--kind`、calibrate `--features-dir` + infinity JSON、analyze in-dir 校验；夹具烟测 **与** scientific tiny 八段 |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md` |
| 实跑入口 | `python -m reasoning_diff`（runbook 命令）；产物根 `%TEMP%\rd-e-r5-qkxdiukl\`，未写入 `src/` / `tests/` / `pyproject.toml` |

**冻结说明：** 审查对象是当前工作区字节，且与声称冻结 hash **一致**。本报告绑定该快照。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–893 | 通读 + `python -m` 夹具八段 + scientific tiny + resume/负路径 + `--kind` + `--shard` | resume `command` 与写出值对齐；失败保留成功清单；scientific prepare 事件为空导致 fit/calibrate 断；calibrate 标签路径写死 `lab`；tiny collect 不重分词 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 通读 + digest / `success_count` / shard 校验 | digest 自洽；`success_count` 缺省 0；`completed_shard_ok` 函数本身正确，CLI 仍用刚算出的 hash 自检 |
| `src/reasoning_diff/io.py` | 1–133 | 通读 + NPZ/NaN/`runtime_info` | JSON/JSONL/NPZ 临时文件+`os.replace`；拒 object；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | 通读 + `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–52 | 对照实跑 | 现含 `--features-dir`；resume 说明与实跑一致；隔离仍 `pending_server`；`runs/label` **不是** calibrate 代码所认的 `lab` |
| `src/reasoning_diff/executor.py` | 1–109 | `get_executor` / subprocess | 默认 Unavailable；`ChildProcessExecutor.isolated_sandbox=False`；拒 `exec(`/`eval(` |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–385 | 通读 + 产物 `from_dict` | Event `record_id` 含 `run_id`；`Trace.from_dict` 把未知键并入 metadata |
| `src/reasoning_diff/splits.py` | 1–110 | CLI `require_split` | test 上 fit、probe_train 上 calibrate 仍拒绝 |
| `src/reasoning_diff/edits.py` | 109–148 | 默认 prepare `p2→2` | 重算答案 8；编辑 Task `record_id=fix-t1-001::p2=2` |
| `src/reasoning_diff/events.py` | 27–75 | prepare 解析 | 夹具合成文本可解析；scientific 生成文本无 `q = <数>` → 0 事件 |
| `src/reasoning_diff/graphs.py` | 1–46 | prepare `ancestors` | CLI 用 `anc.get` |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 observation 则无 task/behavior 标签 |
| `src/reasoning_diff/models/collect.py` | 1–183 | tiny collect / swap decode | 按传入 `token_ids` 取隐状态，不重新 encode 文本 |
| `src/reasoning_diff/models/generate.py` | 66–134 | scientific prepare | `model=tiny-qwen2`，`decode_loop`；token 为模型 ID |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | offline `expressible` 仍相对字符偏移 |
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | `fit` | 持久化 `U`/`V`/`b`；双头 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `conformal_threshold` | `k>n` 返回 `q=inf`；CLI `_sanitize_cal` 写成 `q=null` + `infinity=true` |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | 效应字段仍 `null`；scientific tiny 走到 `prospective_decode` |
| `src/reasoning_diff/repair.py` | 1–189 | `repair` | scientific `k=1..5` 且 `refilled_prefix=true`；`base_group_id` CLI 传空 |
| `src/reasoning_diff/analysis.py` | 1–283 | `analyze` | 读 densities sidecar；无 `p1_table` → `not_evaluated` |
| `src/reasoning_diff/transfer.py` | 1–63 | analyze `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/catalog.py` | 1–39 | prepare `--kind` | 仅 prepare/collect 经 `_load_task` 分派 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–84 | `--kind gsm_symbolic` | CLI 不传 sidecar；无非 placeholder 前提 → prepare 失败 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 50–74 | `--kind gsm_plus` | CLI 写死 `"4"→"5"` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–78 | `--kind humaneval` | `apply_spec_edit` 追加 `# variant`，不再改成 `"2"` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 51–104 | `--kind hotpot` | `document_edit` |
| `src/reasoning_diff/tasks/t3_musique.py` | 72–110 | `--kind musique` | `paragraph_edit`（注解写 `-> Task`，运行返回 `Edit`） |
| `src/reasoning_diff/tasks/t4_boundary.py` | 36–51 | `--kind t4` | `apply_t4_question_edit` |
| `src/reasoning_diff/rng.py` | 1–53 | intervene `StreamBank` | CLI intervene 使用；prepare 未用 |
| `src/reasoning_diff/baselines.py` | 1–120 | 抽样 | **未被** CLI 子命令调用 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | 通读 | CLI 未调用 `BoundaryMLP.fit` |
| `tests/test_cli_pipeline.py` | 1–29 | 读，未当作验收 | 只断言 exit 0 / `not_evaluated` |
| `tests/test_round04_regressions.py` | — | 未当作验收 | 作者关闭锁；本通道以 CLI 实跑为准 |

**抽样未做完整工程审查（非本通道主路径）：** `models/tiny.py`、`models/tokenize.py`、`models/adapters.py`、T1 official 内部。确认 adapters / baselines **未被** 八段通用子命令调用。

## 3. 已执行检查与结果

### 3.1 用户 CLI 入口

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode` |
| `calibrate --help` | **0** | 有 `--features-dir`（runbook L29 已写） |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（指定顺序；collect=offline；calibrate 带 `--features-dir`）

产物根：`%TEMP%\rd-e-r5-qkxdiukl\fx\`。夹具 `tests/fixtures/t1_tiny.json`。`--in-dir` 按 runbook 指向上一阶段。

| 命令 | 退出码 |
|---|---|
| `prepare --fixture … --out-dir prep` | **0** |
| `collect … --in-dir prep --out-dir col --backend offline` | **0** |
| `label --in-dir prep --out-dir lab` | **0** |
| `fit --in-dir col --labels-dir lab --out-dir fit --split probe_train` | **0** |
| `calibrate --in-dir fit --features-dir col --out-dir cal --split calibration` | **0** |
| `intervene --in-dir col --out-dir iv` | **0** |
| `repair --in-dir prep --out-dir rep --mask task_oracle` | **0** |
| `analyze --in-dir lab --out-dir ana` | **0** |

**接线实测：**

| 阶段 | `input_hashes` | `upstream_manifest_ids` | 实际消费 |
|---|---|---|---|
| prepare | `{t1_tiny.json: …}` | `[]` | 夹具；默认 `p2→2` |
| collect | prep 全目录文件 + `upstream_manifest*`（与 prep 字节 **全等**，HASH VERIFY 全 True） | 重算 prep digest `2fdc2473…` | 读 `tasks.jsonl` 第一行 + `traces.jsonl`；**offline** `H[0]=[1..8]`，`weight_source=offline_prefix_ids` |
| label | 哈希 prep 全目录 | `[2fdc2473…]` | `observations.jsonl` + `tasks.jsonl`；`build_labels` |
| fit | collect 文件 **加** `lab/labels.jsonl` 等 | collect + label 两枚重算 digest | 读 `H`/`E` + labels-dir；双头探针 |
| calibrate（`--features-dir col`） | fit + collect 文件 | 两枚 digest | `predict_matrix`；本布局目录名恰好是 `lab`，因此吃到了标签（见 §3.2c / E5-10） |
| intervene | collect | collect digest | offline `H` 仅 1 行 → `donor_missing`；效应 `null` |
| repair | prep 全目录 | prep digest | 读 traces `token_ids`/`text`；fixture 默认 backend≠tiny → `prefill_unavailable` |
| analyze | label 文件 | label digest | densities sidecar；`p1/p2/p3=null`，`status=not_evaluated` |

各阶段 `manifest.digest` 均自洽。`_write_stage` 先 `_upstream` 再写 jsonl。八个阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`（不再写成 jsonl 基名 `traces`/`probes`）。

`collect` 无 `--in-dir` 仍 exit **0**，`input_hashes={}`。`analyze` 无 `--in-dir` 仍 exit **0**；`report.densities=null`，与带 `--in-dir` 的报告 **字节不等**。

#### 3.2b tiny 对照（夹具 collect）

`collect --backend tiny` exit **0**：`weight_source=random_init`，`H`/`E` shape `[2,32]`/`[2,32]`，另有 `H_pre_*`。`H[0]` 与 `H[1]` **逐元素相等**（`maxabs=0`），因两条夹具轨迹 `token_ids` 都是 `range(1,21)`（等长合成文本）且 `weight_seed=0`。`intervene --in-dir <tiny>` → 仍 `status=donor_missing`（`allclose` 把双行当成无 donor）。轨迹 `token_ids` 不是模型分词。

#### 3.2c calibrate 目录名对照

同一套 fit/collect 字节，只改标签目录名：

| 布局 | `scores` | `q` / `infinity` |
|---|---|---|
| `…/lab/labels.jsonl`（代码写死；本烟测 `fx/lab` 碰巧命中） | `[0.005023388252051175]` | `q=null`，`infinity=true`，`k=2`，`n=1` |
| `…/label/labels.jsonl`（runbook `runs/label`） | `[0.0]`（`empty_truth`） | 同上 infinity，**未消费标签** |

`--features-dir` 本身能让 `predict_matrix` 跑通，且 `inf` 不再炸 JSON。标签查找不是 `--labels-dir`，而是 `fit/labels.jsonl` 或 `features.parent/lab/labels.jsonl`。

无 `--features-dir`：`status=probe_weights_or_features_missing`，`scores=null`，fixture 下 exit **0**。

### 3.3 scientific tiny 八段

runbook 局部命令 + 本通道把后段也加上 `--eval-mode scientific`（calibrate/analyze）与 `--backend tiny`（collect/intervene/repair）。`--split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。

| 命令 | 退出码 | 要点 |
|---|---|---|
| `prepare --eval-mode scientific --split-fractions … --sham-opportunities 1` | **0** | 6 条 `tiny-qwen2` 轨迹（base/t0p/edit/两额外编辑/sham）；文本形如 `p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC`；`events.jsonl`/`observations.jsonl` 哈希 `e3b0c442…`（**空文件**）；`n_events=0`，`observations=0` |
| `collect --backend tiny --eval-mode scientific` | **0** | `H` `[6,32]` float64，`E` `[2,32]` float32，`weight_source=random_init`，`hidden_layer=1` |
| `label` | **0** | **只有** densities sidecar，无 `task_label`/`behavior_label` 行 |
| `fit --labels-dir <sc/lab>` | **1** | `ValueError: fit refuses identity labels; provide known task/behavior labels`；失败清单 |
| `calibrate --features-dir <sc/col> --eval-mode scientific` | **1** | 无 `probes.jsonl` → `scientific calibrate refuses loss or literal scores` |
| `intervene --backend tiny` | **0** | `H` 行间不等；`status=prospective_decode`，`timing=pre_step`，`hook_once=resid_post`，`transform=pi_z_swap`；`target/nontarget/task_correct/invalid` 仍 `null` |
| `repair --eval-mode scientific --backend tiny` | **0** | `k=1..5`，`refilled_prefix=true`，`record_id=repair:task_oracle:k{1..5}`；`base_group_id=""` |
| `analyze --eval-mode scientific --in-dir <label>` | **0** | `p1=p2=p3=null`，`scientific_conclusion=null`，`status=not_evaluated` |

scientific **不是** 可走完的用户 CLI 全链路：生成轨迹不能被同一套 `parse_fixture_events` 抽到 `q = <数>`，观测与标签为空，fit/calibrate 按设计拒绝。

### 3.4 schema / shape / ID

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `review_export.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

Observation（夹具精确一行）：`outcome=changed`，`raw_values=["0","8"]`，`record_id=prepare:{identity}:p2`，`run_id=prepare`，`base_group_id=fix-t1-001`。默认编辑仍为 **p2:0→2**。合成轨迹 `"p1 = 4\np2 = 0\nq = 0\n"` / `"p1 = 4\np2 = 2\nq = 8\n"`。这是夹具有效扰动，**不是**科学全量扫描。

身份合同（本轮实测）：

1. `events.jsonl` 两行 `record_id` 为 `trace-base:{identity}` 与 `trace-edit:{identity}`，**彼此不同**；`Event.from_dict` 成功。
2. 两行 Task：`fix-t1-001` 与 `fix-t1-001::p2=2`。
3. prepare Label：`record_id=prepare:q:p2`，`run_id=prepare`，`base_group_id=fix-t1-001`。label 阶段重写为 `record_id=label:q:p2`，`run_id=label`。第二行仍是 densities sidecar。
4. collect `Trace.from_dict` → 成功（`record_id=trace-base`，`metadata` 含 `feature`/`weight_source`）。仅首行 traces 被写入 metadata。
5. offline `features.npz`：`H`/`E`/`token_prefix` = `[1,8]`/`[2,8]`/`[8]`，`H[0]=[1..8]`。manifest `array_shapes` 含 dtype。
6. tiny fixture `H`/`E` `[2,32]`/`[2,32]`；`H_pre_step` 仅 `[1,32]`（最后一条轨迹）。scientific `H` `[6,32]`，`H_pre_*` 仍 `[1,32]`。
7. Repair fixture：`record_id=repair:task_oracle:kNone`，`run_id=repair`，`base_group_id=""`，`status=prefill_unavailable`。scientific：`k` 填齐，`base_group_id` 仍空。
8. 夹具 `token_ids = range(1, len(text)+1)`，不是模型 token。scientific prepare 的 `token_ids` 为 tiny 解码 ID（例：`[50,50,33,…]`）。

### 3.5 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：tasks/edits/splits/events/observations/labels/traces/run_spec/manifest **九文件 hash 全等**。
- 两次 `fit`：`probes.jsonl` hash 全等。输入是 prefix-id（offline），不是隐状态复现。
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
| `--resume` prepare（仅默认参数） | **0** | 不再因 `edit_premise=None` 失败；解析后的 `p2`/`2` 与已写 config 一致 |
| `--resume` prepare `--edit-premise p2 --edit-value 2` | **0** | 文件不变 |
| `--resume` collect / label / fit / calibrate / intervene / repair / analyze（完整产物） | **0** | `command` 键与写出值一致；`success_count` 仍为 1；无 `failure.json` |
| `--resume` + 篡改 `traces.jsonl` | **1** | `resume hash mismatch or missing file: traces.jsonl` |
| 上述失败后的 `manifest.json` | — | **`file_hashes` 原样保留**（features/traces/run_spec）；`success_count=1`；另写 `failure.json`；`digest` 不变 |
| `--resume` + 清单 digest 改为 64 个 `0` | **1** | `resume manifest digest is not self-consistent` |
| `--resume` + 删除 `traces-shard-0000.jsonl` | **1** | `… traces-shard-0000.jsonl`；成功清单仍列出该 shard hash |
| `--shard` | **0** | `traces-shard-0000.jsonl`、`0001.jsonl` **各 1 行**；与 `traces.jsonl`（2 行）字节不同 |
| 不加 `--shard` | **0** | **无** shard 文件 |

`_resume`（`cli.py:36–63`）：比对 `file_hashes`、**跳过 `None` 的 config 键**、digest 自洽。`_write_stage`：`merged = {"command": name, **config}`，config 里的 `command=collect|label|…` 覆盖 jsonl 基名。

`main` 的 `except`（`cli.py:866–888`）仍写 `failure.json`；若已有 `success_count` 或 `record_counts.success`，**不再** `write_manifest` 覆盖成功清单。

`completed_shard_ok(shard, file_digest(shard))` 对正确文件为 True、对 `0*64` 为 False；CLI 在写出后立刻传入**自己刚算的 hash**，对内容错误不构成独立校验。

### 3.7 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 不存在 | **1** `FileNotFoundError` | `failure.json` + 失败清单（`success_count=0`） |
| `label` 无 `--in-dir` | **1** `label requires --in-dir with observations.jsonl` | 失败清单 |
| `fit --split test` | **1** `probe fit cannot fit on test` | 失败清单 |
| `calibrate --split probe_train` | **1** `calibration cannot fit on probe_train` | 失败清单 |
| `--in-dir docs/SERVER_RUNBOOK.md` + collect / calibrate / intervene / repair | **1** `NotADirectoryError`（`_upstream`） | 仅失败清单；**无** features/阶段 jsonl |
| 同上 + label / fit | **1** 缺 observations / features.npz | 仅失败清单 |
| 同上 + analyze（fixture **与** scientific） | **1** `NotADirectoryError`（`cmd_analyze` 先于 `write_json`） | **无** `report.json` |
| `analyze` 无 `--in-dir`（fixture） | **0** | 成功清单；`densities=null` |
| `analyze` 无 `--in-dir`（scientific） | **1** `scientific analyze requires --in-dir` | 失败清单 |
| `read_jsonl` 非法行 | `ValueError('…/bad.jsonl:1: invalid JSON')` | — |
| `IsolatedExecutor().submit` | `executor_unavailable` | — |
| `@forbid_host_exec` | `RuntimeError('host execution of model/dataset code is forbidden')` | 生产 CLI 未使用 |
| `calibrate --features-dir`（n=1） | **0** | JSON 可写：`q=null`，`infinity=true`；不再 `Out of range float` |
| `write_npz` object | 写入前 `ValueError` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits=…)` 回显 `limits`，不执行限额。

### 3.8 `--eval-mode scientific` 门禁

| 命令 | 退出码 | 结果 |
|---|---|---|
| `prepare --eval-mode scientific`（无 fractions） | **1** | `scientific mode requires explicit --split-fractions` |
| `collect --backend offline --eval-mode scientific` | **1** | `scientific collect refuses offline_prefix_ids as H` |
| `collect --backend tiny --eval-mode scientific` | **0** | 接受 `random_init` |
| `calibrate` 无 features + scientific | **1** | `scientific calibrate refuses loss or literal scores` |
| `analyze` 无 `--in-dir` + scientific | **1** | `scientific analyze requires --in-dir` |
| 完整 scientific 八段 | fit/calibrate **1** | 见 §3.3；门禁挡了空标定，但链路本身未接通 |

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
| `humaneval` | **0** | `apply_spec_edit` / `kind=input_list` | after 为 prompt+`\n# variant`，**不是**字面 `"2"`；events/obs 空 |
| `gsm_plus` | **0** | `apply_plus_numeric_edit` `4→5` | 夹具问句含 `"4"` |
| `gsm_plus`（问句无 `"4"` 的临时 JSON） | **1** | 域编辑抛错后回落到 `_default_edit` | `no editable non-placeholder premise` |
| `gsm_symbolic` | **1** | 无 sidecar、无域分支 | 同上 |
| `hotpot` | **0** | `document_edit` | `DocA` → `"replacement"`；events/obs 空 |
| `musique` | **0** | `paragraph_edit` | `p0` → `"replacement only"`；合成节点句 → 4 events / 2 obs |
| `t4` | **0** | `apply_t4_question_edit` | 问句追加 ` ?`；只取快照第一题；events/obs 空 |

label / fit / analyze **无** `--kind`。这不是与 T1 同等的域流水线。

### 3.11 atomic NPZ

`write_npz`：拒 object → `mkstemp` → `np.savez` → `os.replace`。成功后无残留。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 把 pytest / 作者「120 passed」当验收 | 夹具绿测不是科学全跑，也不是 OPS-01 |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境 |
| 真实模型 / GPU / 官方数据 | `pending_server` |
| 并发真实分片崩溃注入 | `--shard` 现为每轨迹一份副本，不是按组调度 |
| 阅读本轮 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。编号为本轮 `E5-##`。

---

### E5-01 声称冻结 hash 与当前树一致（closed）

- **状态：** **closed**
- **文件：** `.planning/audits/round-05/VERSION.md`；58 个范围内文件
- **复现 / 证据：** §1。独立复算 = 声称值 `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`。**`HASH_MATCH`**。

---

### E5-02 失败 `main` 不再覆盖成功清单（closed，原 E4-08）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `main` 866–888
- **复现 / 证据：** §3.6。篡改 traces 或删除 shard 后 `--resume`：写出 `failure.json`，`manifest.file_hashes` / `success_count=1` / `digest` 与失败前 **全等**。`manifest_replaced_with_only_failure=false`。
- **对照：** 首次失败（缺夹具）仍写失败清单，`success_count=0`。

---

### E5-03 `--resume` 的 command 键与写出 config 对齐（closed，原 E4-09）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `_resume` 52–56（跳过 `None`）；`_write_stage` 139 `merged = {"command": name, **config}`；各 `cmd_*` 传入 `command=collect|label|…`
- **复现 / 证据：** §3.6。prepare 默认 `--resume` 以及后七段完整产物 `--resume` **全部 exit 0**，无 `run_spec mismatch: command`。
- **残留：** 后段 rng 仍无 seed；不重开 command 合同。

---

### E5-04 `--features-dir` 可消费权重；infinity 可 JSON（closed 字面，原 E4-10；残留见 E5-10）

- **状态：** **closed**（缺 flag / `q=inf` 炸 `encode`）
- **文件 / 符号 / 行号：** `cli.py` `_sanitize_cal` 545–551；`cmd_calibrate` 554–602；`probes/calibrate.py` 37–38
- **复现 / 证据：** §3.2 / §3.2c。`calibrate --features-dir` exit 0，行内 `q=null`，`infinity=true`，`status=infinity`。`conformal_threshold([0.0], 0.4)` 仍返回 Python `inf`，CLI 写出前剥离。
- **作者「E4-10」在「有 --features-dir 且 inf 可持久化」字面范围独立关闭。**

---

### E5-05 `--shard` 按轨迹各写一份（closed，原 E4-11）

- **状态：** **closed**（全量副本 / 无 flag 也写 shard）
- **文件 / 符号 / 行号：** `cli.py` 453–458
- **复现 / 证据：** §3.6。`--shard` → 两个 1 行 shard；不加 flag → 无 shard 文件；`traces.jsonl` ≠ `traces-shard-0000.jsonl`。
- **残留：** `assert completed_shard_ok(shard, file_digest(shard))` 恒对刚写出文件为真。

---

### E5-06 Event/Label `record_id` 含 `run_id` 且跨轨迹不碰撞（closed，原 E4-12 主缺陷；残留见 E5-15）

- **状态：** **closed**（跨轨迹 Event 碰撞 / 空 `record_id`）
- **文件 / 符号 / 行号：** `schema.py` Event 212–215；`cli.py` `_synthetic_trace` 100–103；label 497–500
- **复现 / 证据：** §3.4。`unique_record=true`。`Event.from_dict` / `Trace.from_dict` 成功。Label `run_id`/`base_group_id` 已填。

---

### E5-07 analyze 在写 `report.json` 之前拒绝文件 `--in-dir`（closed，原 E4-16）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `cli.py` `cmd_analyze` 714–717（先于 796 `write_json`）
- **复现 / 证据：** §3.7。fixture 与 scientific 的文件 `--in-dir` 均 **无** `report.json`，仅失败清单。

---

### E5-08 `--eval-mode scientific` 门禁仍在（closed 存在性；不是科学全跑）

- **状态：** **closed**（缺 flag）
- **复现 / 证据：** §3.8。offline collect / 无 fractions / 无 in-dir analyze / 无 features 的 scientific calibrate 均 exit 1。
- **影响：** 不能把 scientific 夹具路径当成已测 P1–P3。完整 scientific 八段见 E5-09。

---

### E5-09 scientific tiny 用户 CLI 在 label→fit→calibrate 处断裂（confirmed defect）

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `cli.py` `cmd_prepare` 271–278：`generate_task_trace`（`tiny-qwen2`，`max_new=8`）
  - `events.py` `parse_fixture_events` 35–38：要求 `alias = <NUMBER>`
  - `cli.py` `cmd_fit` 532–533：无已知标签则拒绝
  - `cli.py` `cmd_calibrate` 595–596：scientific 拒绝字面分数
- **触发条件：** runbook「local scientific」prepare + 后续 label/fit/calibrate（本通道按用户要求跑满八段）。
- **对应要求：** OPS-01 用户 CLI 跨模块路径；ARCHITECTURE「每个命令接收输入 manifest」并消费上游标签/权重。
- **复现 / 证据：** §3.3。6 条轨迹文本含 `What is q = p1 * p2?` + 随机解码后缀，**没有** `q = <数>`。`events.jsonl`/`observations.jsonl` 为空（SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`）。label 只写 densities。fit exit 1；calibrate scientific exit 1。intervene/repair 能跑是因为不依赖这些标签。
- **影响：** 作者「scientific generate」只证明 prepare 能写 tiny 解码轨迹，**不能**证明 scientific 八段可调度。夹具烟测 exit 0 掩盖了这条断线。
- **建议：** scientific 事件抽取必须能在生成文本上落地，或 fit 明确要求「prepare 已写出非空已知标签」并在 prepare 阶段失败而不是拖到 fit。

---

### E5-10 calibrate 标签目录写死为 `lab`，runbook `label` 走空真理（confirmed defect）

- **严重度：** high
- **状态：** confirmed defect（不重开 E5-04 的 JSON/`--features-dir` 字面关闭）
- **文件 / 符号 / 行号：** `cli.py` 571–575：`feat_dir.parent / "lab" / "labels.jsonl"`；无 `--labels-dir`
- **触发条件：** 按 runbook：`label → runs/label`，`calibrate --in-dir runs/fit --features-dir runs/collect`。
- **对应要求：** OPS-01 校准阶段消费上游标签；runbook L27–29。
- **复现 / 证据：** §3.2c。`…/label/labels.jsonl` → `scores=[0.0]`（`sequence_score(..., empty_truth=True)`）。`…/lab/labels.jsonl`（及本烟测碰巧命名的 `fx/lab`）→ `scores=[0.005023…]`。两边都 exit 0、都写 infinity。`input_hashes` **不含** labels 文件。
- **影响：** 文档路径与代码路径不一致时，校准看起来成功，分数是「空真理 = 0」而不是探针非conformity。本通道第一次烟测因目录名 `lab` **碰巧**走了有标签分支，不能当作 runbook 已接通。
- **建议：** 增加 `--labels-dir` 或同时接受 `label`/`labels`；把标签文件写入 `input_hashes`。

---

### E5-11 夹具 tiny collect 不重分词，双轨迹 H 全等，intervene 无 donor（confirmed defect）

- **严重度：** medium
- **状态：** confirmed defect（E4-13 / MODEL-01 残留的 CLI 接线）
- **文件 / 符号 / 行号：** `cli.py` 412–426：直接把 prepare 的 `trace.token_ids` 送进 `collect_hidden_trace`；`cli.py` 104：合成 `range(1, len(text)+1)`；`cli.py` 620：`allclose` → `donor_missing`
- **触发条件：** `prepare`（fixture）→ `collect --backend tiny` → `intervene`
- **复现 / 证据：** §3.2b。两条 traces 的 `token_ids` 均为 `[1..20]`；`H[0]==H[1]`（`maxabs=0`）；intervene `status=donor_missing`，与 offline 单行路径产物同形。scientific collect 因解码 ID 不同，intervene 能到 `prospective_decode`（效应仍 null）。
- **影响：** runbook 默认 `collect --backend tiny` 在夹具上 **不能** 给干预提供可区分 donor。tiny 隐状态是「假 ID 的 random_init 前向」，不是文本的模型 token。
- **建议：** tiny collect 对 `text` 重新 `encode_text`；或拒绝把合成 `range` ID 标成可干预隐状态。

---

### E5-12 多轨迹 `features.npz` 的 `H_pre_*` / `E` 不是全轨迹堆叠（confirmed defect）

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 425–437：`H=vstack(h_blocks)`，但 `E=e_blocks[0]`，`H_pre_*=meta`（循环最后一次）
- **触发条件：** `collect --backend tiny` 且 `--in-dir` 含 ≥2 条 traces。
- **复现 / 证据：** 夹具 tiny：`H[2,32]` 对 `H_pre_step[1,32]`。scientific：`H[6,32]` 对 `H_pre_*[1,32]`、`E[2,32]`（第一条轨迹的前提数）。
- **影响：** 清单 `array_shapes` 无法表达「每条轨迹的 pre_step」；后段若按 `H_pre_step` 对齐行号会错位。
- **建议：** 与 `H` 同样按轨迹堆叠，或按 `trace_id` 分键。

---

### E5-13 T2/T3/T4 `--kind` 仍不是与 T1 同等的用户 CLI（confirmed defect，原 E4-14 残留）

- **严重度：** medium
- **状态：** confirmed defect（humaneval 不再改成 `"2"` **不能**关闭整条）
- **文件 / 符号 / 行号：** `cli.py` `_domain_edit` 175–201；`_load_task` 166–172；`catalog.py` 无 sidecar 参数
- **复现 / 证据：** §3.10。`gsm_symbolic` exit 1。`gsm_plus` 写死 `"4","5"`，问句无 `4` 则失败。label/fit/analyze 无 `--kind`。humaneval/hotpot/t4 的 events/obs 多为 0。
- **对应要求：** OPS-01 + DATA-02

---

### E5-14 fixture 下 analyze/collect 无 `--in-dir` 仍成功（confirmed defect，原 E4-15 残留）

- **严重度：** medium
- **状态：** confirmed defect（ISSUES **未**声称关闭 E4-15）
- **文件 / 符号 / 行号：** `cli.py` `cmd_analyze` 714–715 只拦 scientific；`cmd_collect` 402–407 允许 `src=None`
- **复现 / 证据：** §3.2 / §3.7。`analyze` 无 in-dir exit 0，`densities=null`，与有 in-dir 报告哈希不同。`collect` 无 in-dir exit 0，`input_hashes={}`。
- **影响：** 调度器无法把「缺上游」从成功阶段里区分出来（scientific 门禁只盖住一部分）。

---

### E5-15 Repair 身份字段不完整（confirmed defect，E4-12 残留）

- **严重度：** low
- **状态：** confirmed defect（不重开 E5-06 的 Event/Label）
- **文件 / 符号 / 行号：** `cli.py` `cmd_repair` 702–706：`base_group_id=""`；fixture `k=None` → `record_id=repair:task_oracle:kNone`
- **复现 / 证据：** §3.4。scientific 填了 `k` 与 `run_id`，`base_group_id` 仍空。ARCHITECTURE「记录以 ID 关联」。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 冻结 hash 复现 | **HASH_MATCH** E5-01 |
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError` |
| `latest` 拒绝 | `write_run_spec(..., "latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `Unknown source_kind 'made_up'` |
| JSONL 坏行带路径行号 | `bad.jsonl:1: invalid JSON` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 |
| runbook 目录 `--in-dir` 文件哈希与上游字节一致 | §3.2 HASH VERIFY 全 True |
| `--labels-dir` 进入 fit `input_hashes` | §3.2 / hash_verify |
| `Trace.from_dict` 回载 | §3.4 |
| 完整产物 `--resume` 成功 | §3.6 八段 exit 0 |
| 篡改/缺 shard 时 `--resume` 拒绝且 **不覆盖** 成功清单 | E5-02 / E5-03 |
| 损坏 digest 自洽检查 | `resume manifest digest is not self-consistent` |
| `require_split` | §3.7 |
| 代码评分不回退 host exec | 默认 `executor_unavailable`；`ChildProcessExecutor.isolated_sandbox is False` |
| 直接迁移维度拒绝 | `not_applicable_dimension_mismatch` 4096≠3584 |
| Week-8 未注册 | `gate0/1/2.decision=unregistered`，`scientific_conclusion=null`，`skip_p2_p3=true` |
| analyze 不编造 P1–P3 | `p1=p2=p3=null`，`status=not_evaluated` |
| intervene 不编造正确率 | 效应字段 null；scientific 只报几何/hook |
| 默认 prepare 不再 4×0 | `p2→2`，`raw_values=["0","8"]` |
| `report.json` 进清单 | analyze `file_hashes` 含 report |
| NPZ 原子替换且拒 object | §3.5 / §3.11 |
| `git -C` revision | cwd=TEMP 仍 `46a6e26…` |
| `python -m` 入口 | §3.1 |
| `success_count` 缺省 0 | 实验 ≠ 13 |
| 文件 `--in-dir` 不留半截 collect / 不先写 report | E5-07 |
| scientific 拒绝 offline H / 无 in-dir analyze / 字面量校准 | §3.8 |
| humaneval 不再 value-edit 成 `"2"` | §3.10 |
| infinity JSON | `q=null`，`infinity=true`（E5-04） |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |

## 8. 结论

**`HASH_MATCH`** `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（58 文件）。

夹具烟测按 runbook 八段（collect=offline，calibrate 带 `--features-dir`）**全部退出码 0**。这只证明夹具能写文件，**不证明** OPS-01，也 **不是** 科学全跑。scientific tiny 按同一用户顺序：**prepare/collect/label/intervene/repair/analyze 为 0，fit 与 calibrate 为 1**。

相对 round-04，本通道独立关闭：冻结 hash（E5-01）、失败不覆盖成功清单（E5-02 / E4-08）、resume command 对齐（E5-03 / E4-09）、`--features-dir` + infinity JSON（E5-04 / E4-10 字面）、per-trace shard（E5-05 / E4-11）、Event/Label 跨轨迹 `record_id`（E5-06 / E4-12 主）、analyze 文件 in-dir 先验（E5-07 / E4-16）、scientific 门禁存在（E5-08）。humaneval 不再改成 `"2"`。

仍不通过的核心缺陷：scientific 八段在空事件/空标签处断开（E5-09）、calibrate 不认 runbook 的 `runs/label`（E5-10）、夹具 tiny 的 H 不可作 donor（E5-11）、多轨迹 feature 形状错位（E5-12）、T2 `gsm_symbolic` `--kind` 失败（E5-13）、fixture 缺 in-dir 仍成功（E5-14）。Exit 0 不能当作 OPS-01。

**本通道不通过** OPS-01。**FAIL**。空通过或「测试绿了」不能作为本通道结论。作者对 E4-08/09/10/11/12/16 的字面关闭在本通道 **独立确认**；E4-10/14 的「校准吃标签 / T2–T4 同等 CLI」**不能**关闭。

下一步（建议，非本通道实施）：接通 scientific 事件或在 prepare 失败；calibrate 增加 `--labels-dir`（接受 `label`）；tiny collect 对文本重新分词；`gsm_symbolic` 接入 sidecar/域编辑。
