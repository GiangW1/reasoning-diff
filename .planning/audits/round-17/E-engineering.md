# E：端到端工程审查（round-17）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮其它通道报告。`ISSUES.md` 仅作作者声称，不采信关闭声明。

夹具烟测与 scientific tiny **不是** 科学全跑，也 **不是** OPS-01 / MODEL-01。本通道不把 `exit 0`、清单存在或 `report.json` 写成论文正确性。

**冻结核验：审查开始 `HASH_MATCH`；CLI 套件结束与本报告落盘前均为 `HASH_MISMATCH`。按本轮指令：`HASH_MISMATCH` → 本通道 `FAIL`。** 本通道未改 `src/`、`tests/`、`pyproject.toml`。漂移来自并行改冻结集（见 §1）。命令表绑定套件期间实跑；不得把写报告后的树标成声明冻结。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 02:56–03:16 +08:00 |
| 声称冻结 hash | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（用户给定；与 `.planning/audits/round-17/VERSION.md` 原文一致；61 文件） |
| 独立复算（审查开始） | **`HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**61** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`。当时 `cli.py` **1259** 行 / **61662** 字节。 |
| 独立复算（CLI 套件结束 / 写报告前，两次） | **`HASH_MISMATCH`**。同一脚本仍 61 文件，得到 `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`。此时 `cli.py` **1260** 行 / **61646** 字节。审查窗口内仍在动的冻结集文件包括 `cli.py`、`edits.py`、`measure.py`、`models/generate.py`、`models/tiny.py`、`tests/test_round06_regressions.py`、`tests/test_round07_regressions.py`。本通道 **未** 写这些文件。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；产物 `environment.repo_root=C:\Users\22688\Desktop\diff`） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch 2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户指定：VERSION 脚本；`pytest -q --tb=line`；夹具与 scientific 八段 prepare→…→analyze；schema/shape/IDs；resume；manifest；shards；`tasks.jsonl` 复制规则；给定阶段目录自身无 `tasks.jsonl` 则 fit/calibrate fail-closed；A12-03；A14-03；label 不编造图；Plus persist leftover（F13-09，不自动当 A10-04）；StreamBank 隔离；隔离执行器不可用且无 host exec 回退；`__main__` 入口 |
| 指定必读 | `cli.py`、`io.py`、`schema.py`、`executor.py`、`splits.py`、`__main__.py`（通读）；实跑另及 `artifacts.py`、`rng.py`、`scoring.py`、`baselines.py`、`graphs.py`、`measure.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md` |
| 实跑入口 | `python -m reasoning_diff`；产物根 `.planning/audits/round-17/_e_scratch/`（下文 `$E`）。未写入 `src/` / `tests/` / `pyproject.toml` |
| pytest | 作者声称 160 passed。本通道独立重跑：`python -m pytest -q --tb=line` → **162 passed**，exit **0**，38.19s。绿测不是 OPS-01。 |

## 2. 逐文件覆盖

行号为 **开审通读快照**（`cli.py` Read 显示 1–1260；VERSION 脚本当时计 1259 行 / 61662 字节）。写报告时 `cli.py` 已是 1260/61646。

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–1260 | 通读 + `python -m` 夹具八段 + scientific tiny + A12-03 + A14-03 + resume + shard + 无图 fit/calibrate | 八段可调度；collect 复制 `tasks.jsonl`；`_find_tasks_jsonl` 只看传入目录自己的文件；无本地图 + 有 labels 则 raise；scientific fit 基线 `refused_not_section8` |
| `src/reasoning_diff/io.py` | 1–133 | NPZ/NaN/`runtime_info` | JSON `allow_nan=False`；`encode(nan)` 抛 `ValueError`；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/schema.py` | 1–385 | 产物 `from_dict` / `record_id` | Event `record_id` = `run_id` + identity JSON；Task 编辑行重写 `record_id`；Label `label:{event}:{premise}` |
| `src/reasoning_diff/executor.py` | 1–109 | 类属性 + `get_executor` + `score_code` | 默认 `UnavailableExecutor`；`ChildProcessExecutor.isolated_sandbox=False`；无 host `exec(` 调用 |
| `src/reasoning_diff/splits.py` | 1–184 | `require_split` + lock 路径 | fit/calibrate 用允许 split；Plus 锁写入 `.planning/research/.cache/gsm_test_only_families.json` |
| `src/reasoning_diff/__main__.py` | 1–4 | `python -m reasoning_diff --help` | 转调 `cli.main`；当文件直接执行则相对导入失败 |
| `src/reasoning_diff/artifacts.py` | 1–85 | digest / `success_count` / shard | 各成功阶段 digest 自洽；失败清单 `success=0`；两枚 shard 进清单 |
| `src/reasoning_diff/rng.py` | 1–53 | StreamBank 独立抽取 | sample 消耗后 direction/perturb/bootstrap/split 与新银行一致 |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code` 默认后端 | 默认 `executor_unavailable`，`eligibility=false`；文案含 `host exec is forbidden` |
| `src/reasoning_diff/baselines.py` | 1–125 | CLI `fit` 对照 | fixture 写入 dummy verbalizer/attention_*；scientific 分支不调用这些分数 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机 `shutil.which` = null |
| `docs/SERVER_RUNBOOK.md` | 1–51 | 对照实跑 | 八段顺序与 `--features-dir` / scientific 拒 offline H 与实跑一致；隔离仍 `pending_server` |
| `src/reasoning_diff/graphs.py` | 1–46 | `ancestors` | label 无 task 则不调用；calibrate RSI 有图才用 |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 graph 则 `task_known=false` / `task_label=null` |
| `src/reasoning_diff/models/collect.py` | tiny collect | collect | scientific `H` `[7,32]` 全有限 |
| `src/reasoning_diff/models/generate.py` | scientific prepare | prepare | 7 traces，皆 `parse_status=constrained_target` |
| `src/reasoning_diff/probes/bilinear.py` | `fit` | fit | 掩码未知行；scientific task 头写出有限 `U`/`V`/`b` |
| `src/reasoning_diff/probes/calibrate.py` | `conformal_threshold` | calibrate | 夹具/scientific 均为有限 `q` |
| `src/reasoning_diff/interventions.py` | CLI intervene | intervene | tiny 走到 `prospective_decode` |
| `src/reasoning_diff/repair.py` | CLI repair | repair | fixture offline → `prefill_unavailable`；scientific tiny `k=1..5` 且 `refilled_prefix=true` |
| `src/reasoning_diff/analysis.py` | CLI analyze | analyze | 无 `p1_table` → `p1=null` / `not_evaluated` |
| `src/reasoning_diff/transfer.py` | `direct_transfer(4096,3584)` | analyze | `not_applicable_dimension_mismatch` |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–84 | 读 persist | `register_test_only_family` 落盘；pytest 多处调用且多数不 `clear` |
| `src/reasoning_diff/probes/boundary.py` | CLI fit | fit | `baseline=boundary_mlp` |

**抽样未做完整工程审查：** `models/adapters.py`、T1 official 内部、`t2_noop.py`、T3/T4 全路径（本轮 named hunts 未要求 T3 prepare）。adapters **未被** 八段通用子命令调用。

## 3. 已执行检查与结果

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。产物 `$E=.planning/audits/round-17/_e_scratch`。夹具 `tests/fixtures/t1_tiny.json`。

### 3.1 VERSION 脚本与用户 CLI 入口

| 命令 | 退出码 | 结果 |
|---|---|---|
| VERSION 原文脚本（审查开始） | **0** | 61 文件；`3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` = 声明值 |
| VERSION 原文脚本（套件后 / 写报告前 ×2） | **0** | 61 文件；`3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` ≠ 声明值 |
| `python -m pytest -q --tb=line` | **0** | **162 passed** in 38.19s |
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`$E`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `python src/reasoning_diff/__main__.py --help` | **1** | `ImportError: attempted relative import with no known parent package` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir`、`--weight-seed` |
| `fit --help` | **0** | `--labels-dir`；`--in-dir` 在 argparse 层 **不是** `required` |
| `calibrate --help` | **0** | `--features-dir` **与** `--labels-dir` |
| `prepare --help` | **0** | `--sidecar`、`--kind`、`--split-fractions` |

`__main__.py` 转调 `main`。`python -m reasoning_diff` 是有效入口。把 `__main__.py` 当脚本直接跑会因相对导入失败——这是包布局，不是静默落到 host 路径。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**）

目录：`$E/fx/`。

| 阶段 | 退出码 | 清单 | 关键产物 |
|---|---|---|---|
| prepare | **0** | digest 自洽，`success_count=1` | `tasks.jsonl` 2 行：`fix-t1-001` / `fix-t1-001::p2=2`；`record_id` 同步改写；traces `trace-base`/`trace-edit` |
| collect tiny | **0** | 含 `tasks.jsonl`、`features.npz`、`event_rows.jsonl` | `H` `[2,32]` 全有限（float64）；`E` `[2,32]` float32 |
| label | **0** | `labels.jsonl` | 消费 prepare `observations.jsonl`；`record_id=label:q:p2`；**无** `tasks.jsonl` |
| fit `--split probe_train` | **0** | `probes.jsonl` | `input_hashes` 含 `collect/tasks.jsonl` **与** `label/labels.jsonl` |
| calibrate `--features-dir collect` | **0** | `calibration.jsonl` | `scores≈[0.00502331, 0.00502337]`，`q=0.00502337`，`status=finite`，`unit=problem` |
| intervene | **0** | `interventions.jsonl` | `status=prospective_decode`，`timing=offline_hidden`；`donor_kind=same_source_diff_value` |
| repair `--mask task_oracle` | **0** | `repairs.jsonl` | `record_id=repair:fix-t1-001:task_oracle:k1`；默认 backend=offline → `prefill_unavailable` |
| analyze | **0** | `report.json` 进清单 | `p1=p2=p3=null`，`status=not_evaluated`，`scientific_conclusion=null` |
| collect `--backend offline` | **0** | 另目录 | `H` `[1,8]`；`weight_source=offline_prefix_ids` |
| collect `--shard` | **0** | 两枚 shard 进清单 | `traces-shard-0000.jsonl` / `0001.jsonl` 各 1 行；`completed_shard_ok=true` |

**接线：** 每阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。抽查成功 `manifest.digest` 独立重算均为 True。Event `record_id=trace-base:{"entity_or_expression": "q", ...}`。

`analyze` `transfer`：`source_dim=4096`，`target_dim=3584`，状态为维度拒绝。Week-8：`gate0/1/2.decision=unregistered`，`skip_p2_p3=true`。

**shard concat：** 拼接两枚 shard 的 `id`/`text` 与 `traces.jsonl` 一致（`trace-base` + `trace-edit`）。**整行不全等**：shard 在 `cmd_collect` 给 `shard_rows[0]["metadata"]` 写入 `feature`/`weight_source`/`hidden_layer` **之前**落盘，因此 concat 缺这三项。这是元数据时序，不是丢 trace。清单仍收录两枚 shard。

### 3.3 scientific tiny 八段与 collect 复制 `tasks.jsonl`

runbook 本地 scientific：`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。目录：`$E/sc/`。fit/calibrate/repair 均显式带 `--eval-mode scientific`。

| 阶段 | 退出码 | 要点 |
|---|---|---|
| prepare | **0** | `n_traces=7`：base / t0p / edit / source / 两枚 extra edit / sham；皆 `parse_status=constrained_target` |
| collect `--backend tiny` | **0** | **写出 `s-col/tasks.jsonl`**；`H` `[7,32]` 全有限；`event_rows` 7 行，皆 `node_id=q` |
| label | **0** | first-seen premise 顺序 **`p2`, `p1`**（再 `sham:q`）；**无** `tasks.jsonl` |
| fit `--eval-mode scientific` | **0** | `input_hashes` 含 `s-col/tasks.jsonl`；见 §3.5 A14-03 |
| calibrate | **0** | 4 个 problem unit，`q=0.00502359`，`status=finite` |
| intervene | **0** | `prospective_decode` |
| repair `--backend tiny --eval-mode scientific` | **0** | `k=1..5`，皆 `status=ok`，`refilled_prefix=true` |
| analyze | **0** | 同样 `p1=null` / `not_evaluated` / `scientific_conclusion=null` |
| collect `--backend offline` + scientific | **1** | `scientific collect refuses offline_prefix_ids as H`；**无** `features.npz` |

**collect 复制 `tasks.jsonl`（独立确认）：**

- `$E/fx/collect/tasks.jsonl` 与 `$E/sc/s-col/tasks.jsonl` **均存在**，进入各自 collect `manifest.file_hashes`。
- 与对应 prepare 目录 **字节全等**。SHA-256 均为 `a6ca1a4d4f5ef4c950be39da00864229159b9edb9b74bd93fb6af367f1194eb7`。
- 前提顺序 `["p1","p2"]`。

**label 不编造图（独立确认）：**

- 夹具/scientific 的 label 输出目录 **都没有** `tasks.jsonl`（不复制、不发明）。
- `$E/label_nograph/src` 只有 `observations.jsonl`：label **exit 0**；`densities.null_reason=no_task`；`task_known=false`；`task_label=null`。空 `ancestors`，没有捏造 DAG。

**fit 用 collect 的图，而不是 labels first-seen（独立确认）：**

1. scientific labels first-seen（跳过 `sham:`）：**`p2`, `p1`**。
2. `_find_tasks_jsonl(s-col, s-lab)` 返回 **`s-col/tasks.jsonl`**。
3. `_e_premise_ids(task_from_that_file, labels)` = **`["p1","p2"]`**。
4. `_e_premise_ids(None, labels)` = **`["p2","p1"]`**。两者 **不相等**。
5. scientific fit 的 `input_hashes` 含 `s-col/tasks.jsonl`。

scientific 事件仍是约束 `\nq = <digit>`，**不是** §4.1 自然 CoT。tiny `random_init` **不是** MODEL-01。

### 3.4 A12-03：祖先 / 兄弟 `tasks.jsonl` 不得绑定；缺本地图 + 有 labels → fit/calibrate raise

**兄弟 `prep`：** 把夹具 collect/label 复制到 `$E/c6/without/`，删除 `col/tasks.jsonl`，**保留兄弟** `without/prep/tasks.jsonl`。给定目录是 `col` 与 `lab`。

`_find_tasks_jsonl(col, lab)` 独立 import 为 **`None`**（兄弟 `prep` 不在查找范围）。

| 命令 | 退出码 | `failure.json` |
|---|---|---|
| `fit --in-dir c6/with/col --labels-dir c6/with/lab`（保留 tasks） | **0** | —；find → `col/tasks.jsonl` |
| `fit --in-dir c6/without/col --labels-dir c6/without/lab` | **1** | `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order`；清单 `success=0`，只哈希 `failure.json` |
| `calibrate --in-dir probe_only --features-dir col --labels-dir lab`（`probes.jsonl` 在，三目录均无 tasks） | **1** | `ValueError: calibrate requires tasks.jsonl so E columns follow task.premises, not label order` |
| scientific 同构：`c6sc` 删 `col/tasks.jsonl` 后 fit / calibrate | **1** / **1** | 同上两条 ValueError |

无图路径 **不会** 静默退回 first-seen，也 **不会** 因兄弟名叫 `prep` 而救命。

**祖先 `col` WRONG-TASK：** 布局 `$E/a12/bind/col/tasks.jsonl` 写成 `task_id=WRONG-TASK`，前提序对调为 `[p2,p1]`；特征在 `bind/deep/x/feat`，标签在 `bind/deep/x/labs`。feat/labs **没有** `tasks.jsonl`。

| 检查 | 结果 |
|---|---|
| 祖先 `col/tasks.jsonl` 存在 | 是；`task_id=WRONG-TASK` |
| `_find_tasks_jsonl(feat, labs)` | **`None`** |
| `_find_tasks_jsonl(col)` | 命中该 WRONG-TASK 文件（只因 `col` 本身被传入） |
| `_e_premise_ids(real, labels)` | `["p1","p2"]` |
| `_e_premise_ids(WRONG-TASK, labels)` | `["p2","p1"]`（不相等） |
| `fit --in-dir feat --labels-dir labs` | **exit 1**；上述 ValueError；`probes.jsonl` **未写出** |
| `calibrate --in-dir fx/fit --features-dir feat --labels-dir labs` | **exit 1**；calibrate 同一门槛 |

旧 4 层 + extras 搜索会绑到祖先 `col` 并把 \(E\) 列换成错题 `[p2,p1]`。本冻结只读传入目录自己的 `tasks.jsonl`，祖先 WRONG-TASK **不绑定**。

### 3.5 A14-03：scientific `probes.jsonl` 不得发明 verbalizer/attention_* 分数

scientific fit（`--eval-mode scientific`）的 `s-fit/probes.jsonl`：

| baseline | status | score / f1 / shape |
|---|---|---|
| verbalizer | `refused_not_section8`（`no dependency-label verbalizer on this prefix`） | **无** |
| attention_mean | `refused_not_section8`（`no attention maps`） | **无** |
| attention_rollout | 同上 | **无** |
| attention_threshold | 同上 | **无** |

`sc_invented=false`，`sc_all_refused=true`。另有 bilinear task 头（有限 `U`/`V`/`b`）与 `boundary_mlp`（`event-rows-only_no_negatives`）。这不是 §8 基线分数。

**夹具 fit 仍写 dummy 基线（允许）：** `attention_mean.score=0.0`；`attention_rollout.shape=[2,2]`；`attention_threshold.f1=1.0`（`threshold=0.9`，`split=dev`）；verbalizer 三档 `score=1.0` / `status=generated`（把 fixture 前缀当 generate_fn 回放）。这些在 **`$E/fx/fit`**，与 scientific 目录分离（`a14_sc_dir_separate=true`）。**没有**写进 `s-fit/probes.jsonl`。

**是否漏进 scientific：** 指定的 scientific 八段 **没有**漏。`--eval-mode` 是每阶段自己的 flag，默认 `fixture`。对照：同一套 scientific collect/label，**省略** `--eval-mode scientific` 再 fit（`$E/sc/s-fit-default`）会写出与夹具同类的 dummy（`attention_mean.score=0.0`，verbalizer `score=1.0`，文本甚至是约束生成的 `q = 82`）。这是 **flag 默认值**，不是 scientific 命令污染了 `s-fit`。操作者必须在 fit 上重复 scientific 旗标。

### 3.6 缺 `--in-dir` 必须失败

argparse 把 `--in-dir` 标成可选；运行期拒绝。均带 `--out-dir`。

| 子命令 | 退出码 | `failure.json` | 清单 |
|---|---|---|---|
| fit | **1** | `fit requires --in-dir` | `success=0` / `failure=1`，只哈希 `failure.json` |
| calibrate | **1** | `calibrate requires --in-dir` | 同上 |
| intervene | **1** | `intervene requires --in-dir` | 同上 |
| repair | **1** | `repair requires --in-dir` | 同上 |
| analyze | **1** | `analyze requires --in-dir` | 同上；**无** `report.json` |
| collect | **1** | `collect requires --in-dir` | 同上 |
| label | **1** | `label requires --in-dir with observations.jsonl` | 同上 |

文件当作 `--in-dir`：`analyze --in-dir tests/fixtures/t1_tiny.json` → **1**，`NotADirectoryError: --in-dir must be a directory`。

### 3.7 隔离执行器不可用 → 报告，无 host exec 回退

独立 import + 调用，不经 pytest。

| 检查 | 结果 |
|---|---|
| `get_executor()` 默认 | `UnavailableExecutor`（`IsolatedExecutor` 子类），`isolated_sandbox=True` |
| `ChildProcessExecutor.isolated_sandbox` | **`False`** |
| `IsolatedExecutor.isolated_sandbox` | `True` |
| `isinstance(ChildProcessExecutor(), IsolatedExecutor)` | **False** |
| MRO | Child 只继承 `object`；**无共同实现基类** |
| `score_code("print(1)","assert True")` 默认 | `status=executor_unavailable`，`value=null`，`eligibility=false`，reason=`no isolated backend configured; host exec is forbidden` |
| 显式 child：`score_code("x=1","assert x==1", executor=child)` | `status=ok`，`value=1.0`（普通子进程，**不是**沙箱） |
| child `submit` 含 `exec(` | `status=rejected`，`submission mentions exec/eval` |
| `forbid_host_exec` | `RuntimeError: host execution of model/dataset code is forbidden` |
| `src/` 生产路径 `exec(` | 仅 `executor.py` 把 `"exec("` / `"eval("` 当拒绝字符串；**无** 内建 host `exec(` 调用。`repair.py` / `collect.py` 的 `model.eval()` 是 PyTorch 评估模式 |

默认评分路径 **不会** 落到 ChildProcess，也 **不会** 回退到 host `exec`。Linux cgroup 仍 `pending_server`。

### 3.8 Resume 身份 / 计数

`$E/resume/prepare` 先成功：`success_count=1`，digest `cd379ff1456ab2e9b54e7a40ee72d49ce55aad8460404f5afc1b781c87faf866`。

| 动作 | 退出码 | 清单 |
|---|---|---|
| `prepare --resume`（配置一致） | **0** | digest **相同**；`manifest.json` `st_mtime_ns` **相同** → **未重写** |
| `prepare --resume --edit-value 99` | **1** | `resume run_spec mismatch: edit_value`；写出 `failure.json`；digest / `success_count=1` **未变** |
| collect tiny 成功后 `--resume` | **0** | digest `17d4d79c…` 相同；mtime 未变 |
| collect `--resume --backend offline` | **1** | `resume run_spec mismatch: backend`；`success_count` 仍为 1，digest 仍为成功值 |

`main()` 异常路径：已有 `success_count` 则 **不** `write_manifest` 覆盖成功清单。与实跑一致。

### 3.9 StreamBank：sample / direction / perturb / bootstrap / split 隔离

`StreamBank.NAMES = ("sample","direction","perturb","bootstrap","split")`。独立构造两枚 `StreamBank(0)`：

- 先在 A 上抽 8 次 `sample`；随后 A/B 的 **direction / perturb / bootstrap / split 首次抽签全部相等**。
- 另两枚 `StreamBank(7)`：先抽 `direction`，再抽 `sample`，与未动 direction 的银行 **sample 首次相等**。
- 未知名 `other` → `KeyError`（文案列举 sample/direction/perturb/bootstrap；`split` 在 NAMES 里但未写入该句——观察，不影响隔离）。

CLI `intervene` 分别 `bank.get("direction")` / `sample` / `perturb`，不混用单一种子场。

### 3.10 Plus persist leftover after pytest = F13-09，不是自动 A10-04

开审已存在 `.planning/research/.cache/gsm_test_only_families.json`：`["gsm8k-12", "q:ada has 4 apples…"]`，SHA-256 `03168c26…`。pytest 与 CLI 套件之后 **仍在**，字节相同。

多个测试调用 `load_gsm_plus("tests/fixtures/t2_gsmplus_one.json")`（`test_t2_gsm.py`、`test_round03_regressions.py`、`test_round04_regressions.py`、`test_round05_regressions.py`、`test_review_regressions.py`），`register_test_only_family` 会落盘。`test_plus_locks_symbolic_family_to_test` 末尾 `clear_test_only_families()`，其它测试多数不清理。这是 **测试卫生（F13-09）**：全局锁文件在 pytest 后留下。

本通道 **不** 把该 leftover 判成 A10-04。A10-04 需要独立的 Plus 然后 **新进程** Symbolic、且能把哈希角色与磁盘锁分开。本轮 named hunt 只要区分 leftover ≠ 跨进程锁证明。本通道未另跑 Plus→Symbolic 两进程锁（避免与并行审查抢同一仓库锁）。

测前已把锁文件快照到 `$E/lock_before_pytest.json`。内容未改。本通道未删除该锁。

### 3.11 其它接线

| 项 | 证据 |
|---|---|
| JSON 拒 NaN | `encode({'x': nan})` → `ValueError: Out of range float values are not JSON compliant` |
| 拒 `latest` | `write_run_spec(..., config.model='latest')` → `config.model cannot use mutable identity 'latest'` |
| 产物无 `.tmp` | `$E.rglob('*.tmp')` 为空 |
| scientific 拒 offline H | §3.3 |
| 失败清单 | `miss/fit` 与 A12 fit：`success_count=0`，只哈希 `failure.json` |

## 4. 命令表

前缀：`python -m reasoning_diff`。夹具 `F=tests/fixtures/t1_tiny.json`。`$E=.planning/audits/round-17/_e_scratch`。

| tag | argv（相对） | exit | 秒 | 关键产物 |
|---|---|---|---|---|
| VERSION_start | VERSION.md 原文脚本 | 0 | 0.09 | 61 / `3d0a0764…` **MATCH** |
| pytest | `python -m pytest -q --tb=line` | **0** | 38.19 | **162 passed** |
| help | `--help` | 0 | 0.30 | 八段子命令 |
| help_collect | `collect --help` | 0 | 0.32 | `--backend` `--shard` `--in-dir` |
| help_fit | `fit --help` | 0 | 0.28 | `--labels-dir` |
| help_calibrate | `calibrate --help` | 0 | 0.35 | `--features-dir` `--labels-dir` |
| help_prepare | `prepare --help` | 0 | 0.29 | `--sidecar` `--kind` |
| help_from_scratch | `--help`（cwd=`$E`） | 0 | 0.37 | 不依赖 cwd |
| help_no_pythonpath | `--help`（无 PYTHONPATH） | **1** | 0.23 | `No module named reasoning_diff` |
| main_file_direct | `python src/reasoning_diff/__main__.py --help` | **1** | 0.14 | 相对导入失败 |
| fx_prepare | `prepare --fixture F --out-dir $E/fx/prepare` | **0** | 0.80 | `tasks.jsonl` `manifest.json` |
| fx_collect | `collect --fixture F --in-dir …/prepare --out-dir …/collect --backend tiny` | **0** | 14.60 | `features.npz` `tasks.jsonl` `event_rows.jsonl` |
| fx_label | `label --in-dir …/prepare --out-dir …/label` | **0** | 0.62 | `labels.jsonl`；无 tasks |
| fx_fit | `fit --in-dir …/collect --labels-dir …/label --out-dir …/fit --split probe_train` | **0** | 0.67 | dummy baselines（夹具） |
| fx_calibrate | `calibrate --in-dir …/fit --features-dir …/collect --out-dir …/cal --split calibration` | **0** | 0.64 | 有限 q |
| fx_intervene | `intervene --in-dir …/collect --out-dir …/intervene` | **0** | 13.06 | `prospective_decode` |
| fx_repair | `repair --in-dir …/prepare --out-dir …/repair --mask task_oracle` | **0** | 0.58 | `repair:fix-t1-001:task_oracle:k1` |
| fx_analyze | `analyze --in-dir …/label --out-dir …/analyze` | **0** | 0.60 | `report.json` 进清单 |
| fx_collect_offline | `collect … --backend offline --out-dir …/collect_off` | **0** | 0.68 | `H[1,8]` |
| fx_collect_shard | `collect … --backend tiny --shard --out-dir …/collect_shard` | **0** | 13.80 | `traces-shard-000{0,1}.jsonl` |
| sc_prepare | `prepare … --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1` | **0** | 9.46 | 7 traces，`constrained_target` |
| sc_collect | `collect … --eval-mode scientific --backend tiny` | **0** | 9.66 | **`s-col/tasks.jsonl` 字节=prepare** |
| sc_label | `label --in-dir …/s-prep --out-dir …/s-lab` | **0** | 0.45 | first-seen `p2` 然后 `p1` |
| sc_fit | `fit … --eval-mode scientific --split probe_train` | **0** | 0.60 | verbalizer/attention_* = `refused_not_section8` |
| sc_calibrate | `calibrate … --eval-mode scientific --split calibration` | **0** | 0.52 | 4 problem scores，有限 q |
| sc_intervene | `intervene --in-dir …/s-col --out-dir …/s-int` | **0** | 9.60 | `prospective_decode` |
| sc_repair | `repair … --eval-mode scientific --backend tiny` | **0** | 8.44 | k=1..5，`refilled_prefix=true` |
| sc_analyze | `analyze --in-dir …/s-lab --out-dir …/s-an` | **0** | 0.42 | `p1=null`，gates unregistered |
| sc_collect_offline | `collect … --eval-mode scientific --backend offline` | **1** | 0.25 | `refuses offline_prefix_ids as H` |
| sc_fit_default_eval | `fit` 同一 scientific 产物、**无** `--eval-mode scientific` | **0** | 0.41 | dummy scores（flag 默认 fixture） |
| c6_fit_with | `fit --in-dir c6/with/col --labels-dir c6/with/lab` | **0** | 0.44 | find → col/tasks.jsonl |
| c6_fit_without | `fit --in-dir c6/without/col --labels-dir c6/without/lab` | **1** | 0.25 | 兄弟 `prep` 不救命 |
| c6_cal_probes | `calibrate --in-dir probe_only --features-dir col --labels-dir lab` | **1** | 0.25 | `calibrate requires tasks.jsonl` |
| a12_fit | `fit --in-dir bind/deep/x/feat --labels-dir bind/deep/x/labs` | **1** | 0.24 | 祖先 `col` WRONG-TASK 不绑定 |
| a12_calibrate | `calibrate --features-dir feat --labels-dir labs` | **1** | 0.25 | 同上门槛 |
| c6sc_fit | scientific 无本地 tasks | **1** | 0.24 | fit raise |
| c6sc_cal | scientific 无本地 tasks | **1** | 0.28 | calibrate raise |
| label_nograph | `label --in-dir` 仅 observations | **0** | 0.45 | `null_reason=no_task` |
| miss_fit … miss_label | 缺 `--in-dir` | **1** | ~0.25 | 七段运行期失败 |
| file_indir_analyze | `--in-dir` 指向文件 | **1** | 0.27 | `must be a directory` |
| res_prepare | prepare 成功 | **0** | 0.50 | digest `cd379ff1…` |
| res_prepare_resume | `--resume` | **0** | 0.29 | digest/mtime 未变 |
| res_prepare_mismatch | `--resume --edit-value 99` | **1** | 0.25 | 成功清单保留 |
| res_collect | collect tiny | **0** | 8.66 | digest `17d4d79c…` |
| res_collect_resume | `--resume` | **0** | 0.26 | digest/mtime 未变 |
| res_collect_backend_mismatch | `--resume --backend offline` | **1** | 0.23 | 成功清单保留 |
| VERSION_end | VERSION.md 原文脚本 | 0 | 0.01 | 61 / `3d0f1c10…` **MISMATCH** |

共 50 条 `python -m reasoning_diff` 调用（含对照 `sc_fit_default_eval`）+ pytest + 两次 VERSION 脚本。进程内执行器 / StreamBank / JSON 检查不列入上表。

## 5. 必做项判定

| # | 要求 | 判定 | 证据 |
|---|---|---|---|
| 1 | VERSION 脚本复算 | **FAIL** | 开始 MATCH；套件后 / 落盘前 MISMATCH §1 |
| 2 | `pytest -q --tb=line` | **PASS** | 162 passed，exit 0（作者声称 160；以本通道实跑为准） |
| 3 | 夹具八段 prepare→…→analyze | **PASS** | §3.2 八段 exit 0，清单自洽 |
| 4 | scientific tiny 八段 | **PASS** | §3.3 八段 exit 0 |
| 5 | collect 复制 `tasks.jsonl` | **PASS** | §3.3 字节全等 + 进清单 + HASH `a6ca1a4d…` |
| 6 | label 不编造图 | **PASS** | label 目录无 `tasks.jsonl`；无图目录 `null_reason=no_task` |
| 7 | 给定阶段目录无 `tasks.jsonl` 则 fit/calibrate raise | **PASS** | §3.4 兄弟 `prep` 仍 exit 1 |
| 8 | 祖先/兄弟不绑定（A12-03） | **PASS** | §3.4 find=`None`；fit/calibrate exit 1；无 probes |
| 9 | A14-03 scientific 基线非发明分数 | **PASS** | §3.5 `refused_not_section8`；夹具 dummy **未**写入 `s-fit` |
| 10 | Plus leftover ≠ 自动 A10-04 | **PASS（卫生）** | §3.10 判 F13-09；不升级 A10-04 |
| 11 | StreamBank 五流隔离 | **PASS** | §3.9 |
| 12 | 隔离执行器不可用、无 host exec | **PASS** | §3.7 |
| 13 | resume 身份/计数 | **PASS** | §3.8 digest/mtime/success 不变 |
| 14 | shard concat | **PASS（带观察）** | 两枚 shard 进清单且 id/text 可拼接；整行因后写 metadata 不全等 §3.2 |
| 15 | `__main__` 入口 | **PASS** | `python -m` exit 0；直接跑文件 exit 1（相对导入） |
| — | 冻结 hash 复算（通道硬规则） | **FAIL** | `HASH_MISMATCH` |

### 残留观察（不否决上表工程项，但通道仍因 hash 失败）

- **shard 元数据时序：** concat ≠ `traces.jsonl` 整行，只差 collect 事后写入的 `feature`/`weight_source`/`hidden_layer`。
- **`--eval-mode` 默认 fixture：** 对 scientific collect 产物跑默认 fit 会写出 dummy 分数。指定 scientific fit **没有**这个问题。
- **`--in-dir` argparse 非 required：** 运行期 `ValueError` 已足够失败。
- **锁文件是仓库全局路径：** pytest leftover = F13-09。并行审查会互相看见同一 JSON。
- **混用 dtype：** tiny `H` float64，`E`/`H_pre_*` float32。形状与有限性成立。
- **未知 stream 报错文案**未点名 `split`。五流隔离仍成立。
- **冻结漂移：** 写报告树是 `3d0f1c10…`。本通道未改生产文件。连续通过计数 **不能** 把本报告绑到声明值 `3d0a0764…`。
- **pytest 162 vs 声称 160：** 审查窗口内 `tests/test_round06_regressions.py` / `test_round07_regressions.py` 仍在改。以本通道命令输出为准。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 开审冻结 hash 复现 | §1 `HASH_MATCH` |
| 夹具 + scientific 八段可调度 | §3.2 / §3.3 |
| collect 复制 tasks；fit 按前提列序 | §3.3 |
| 给定目录无 `tasks.jsonl` 则 fit/calibrate raise | §3.4 |
| 祖先/兄弟 WRONG-TASK 不绑定 | §3.4 |
| scientific verbalizer/attention_* 拒绝而非编分 | §3.5 |
| 夹具 dummy 不进入 scientific `s-fit` | §3.5 |
| label 无图不编 DAG | §3.3 |
| 缺 `--in-dir` 七段失败 | §3.6 |
| 默认执行器不可用；无 host exec | §3.7 |
| resume 不覆盖成功清单 | §3.8 |
| StreamBank 五流隔离 | §3.9 |
| Plus leftover 按 F13-09 而非 A10-04 | §3.10 |
| JSON 拒 NaN；拒 `latest` | §3.11 |
| 各成功 `manifest.digest` 自洽 | §3.2 / §3.3 |
| shard 完整入清单 | §3.2 |
| `report.json` 进清单 | analyze `file_hashes` |
| 直接迁移维度拒绝 | 4096≠3584 |
| Week-8 未注册 | `unregistered` / `scientific_conclusion=null` |
| analyze 不编造 P1–P3 | 仅有 labels 时 `p1=null` |
| `git -C` revision | 产物仍 `46a6e26…` |
| repair `record_id` 含 group 与 k | 夹具 k1；scientific k1..k5 |
| 文件 `--in-dir` 拒绝 | §3.6 |
| scientific 拒 offline H | §3.3 |
| `python -m reasoning_diff` | `__main__` 转调 |

Gate 0–2 未注册与 `scientific_conclusion=None` **不是** 缺陷。tiny 随机权重 **不是** MODEL-01。约束 `\nq = <digit>` 是本机可解析接口，不是自然 CoT。pytest 后 Plus 锁文件残留 **不是** A10-04。

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |
| Plus→Symbolic 跨进程锁（A10-04 本体） | 本轮按指令不把 leftover 当 A10-04；未另跑两进程锁 |
| 漂移后（`3d0f1c10…`）树上的八段是否仍全部成立 | 不得用开审 MATCH 树上的 exit 0 给当前树背书 |

## 8. 结论

审查开始 **`HASH_MATCH`** `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（61 文件）。CLI 套件结束与写报告前 **`HASH_MISMATCH`** `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（仍 61 文件）。本通道未改生产代码。并行写入改了至少 `cli.py`、`edits.py`、`measure.py`、`models/generate.py`、`models/tiny.py` 与两份 round-06/07 测试。

相对用户指定的独立复跑：pytest 162 passed；夹具与 scientific 八段可调度；collect 复制 `tasks.jsonl`；label 不编造图；缺本地 `tasks.jsonl` 则 fit/calibrate raise；祖先/兄弟不绑定（A12-03）；scientific `probes.jsonl` 基线为 `refused_not_section8` 而非发明分数（A14-03）；夹具 dummy 不泄漏进该 scientific 目录；StreamBank 五流隔离；默认执行器不可用且无 host exec；resume 保留成功身份/计数；shard 可拼接 id/text；`python -m` 入口成立。Plus 锁 leftover 记为 F13-09，不升级 A10-04。

这只证明用户 CLI 在 tiny/fixture 上可调度且 fail-closed 行为与声明一致。**不是** OPS-01，**不是** 真实模型上的论文正确性。按本轮硬规则，交卷树与声明冻结不一致则通道失败。

**本通道：`FAIL`（`HASH_MISMATCH`）。** 工程接线在套件实跑上成立，但不能给 `3d0f1c10…` 或写报告后的脏树背书。连续通过计数不得使用本报告。
