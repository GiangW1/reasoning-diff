# E：端到端工程审查（round-14）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮其它通道报告。`ISSUES.md` 仅作作者声称，不采信关闭声明。

夹具烟测与 scientific tiny **不是** 科学全跑，也 **不是** OPS-01 / MODEL-01。本通道不把 `exit 0`、清单存在或 `report.json` 写成论文正确性。

**冻结核验：审查开始 `HASH_MATCH`；写报告前 `HASH_MISMATCH`。** 本通道未改 `src/`、`tests/`、`pyproject.toml`。漂移来自并行改生产树（见 §1）。下列用户 CLI 证据绑定审查开始时与声明值一致的快照；不能把写报告时的工作区当作同一冻结。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 02:40–02:50 +08:00 |
| 声称冻结 hash | `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`（用户给定；与 `.planning/audits/round-14/VERSION.md` 原文一致） |
| 独立复算（审查开始，实跑所绑定） | **`HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**61** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`。当时 `cli.py` **1249** 行 / **60895** 字节。 |
| 独立复算（写报告前） | **`HASH_MISMATCH`**。同一脚本仍为 61 文件，得到 `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`。此时 `cli.py` **1252** 行 / **61010** 字节。审查窗口内 mtime 仍在动的冻结集文件包括 `cli.py`、`edits.py`、`measure.py`、`tests/test_round06_regressions.py`、`tests/test_round07_regressions.py`。本通道 **未** 写这些文件。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；产物 `environment.repo_root=C:\Users\22688\Desktop\diff`） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，`torch=2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户指定：夹具八段；scientific tiny 八段与 `--in-dir` 串联；collect `tasks.jsonl`；无本题 `tasks.jsonl` 时 fit/calibrate 必须失败（C6-M-01）；祖先 `col/` WRONG-TASK 不得被用（A12-03）；T3/T4/`gsm_symbolic` sidecar；缺 `--in-dir`；`ChildProcessExecutor.isolated_sandbox is False`；resume 不覆盖成功清单；scientific `backend!=tiny` 拒绝；Plus→Symbolic 两进程锁（A10-04） |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md`、`executor.py`、`scoring.py`、`splits.py` |
| 实跑入口 | `python -m reasoning_diff`；产物根 `%TEMP%\rd-e-r14-w8q3n5\`（下文 `$E`）与隔离树 `$E\iso\`（下文 `$ISO`）。未写入 `src/` / `tests/` / `pyproject.toml`。A10 期间曾短暂删除再恢复 `.planning/research/.cache/gsm_test_only_families.json`（已还原为开审原文）。 |
| pytest | 作者声称 157 passed。本通道 **未** 把 pytest 当作验收，也未重跑测试套件。 |

**冻结说明：** 命令表与 §3 证据绑定审查开始时的 `1f61fd06…`。写报告时工作区已是 `401e509b…`。不得用开始时的 exit 0 给当前树背书。写报告前所读 `_find_tasks_jsonl` 仍为「只搜传入目录」，与开审通读一致。

## 2. 逐文件覆盖

行号为 **审查开始 / 实跑所读快照**（`cli.py` 1249），不是漂移后的未知字节。

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–1249 | 通读 + `python -m` 夹具八段 + scientific tiny + 负路径 + `--kind` + 缺 in-dir + 无 `tasks.jsonl` + 祖先 `col/` + resume + A10 两进程 | 八段可调度；collect 复制 `tasks.jsonl`；`_find_tasks_jsonl` 只读传入目录；有 labels 且 find=`None` 则 `ValueError`；T3 prepare 不被 pair 打断；缺 in-dir 失败；resume 失败保留成功清单 |
| `src/reasoning_diff/artifacts.py` | 1–85 | digest / `success_count` / shard | 各成功阶段 digest 自洽；失败清单 `success=0`；`--shard` 写出两枚 shard |
| `src/reasoning_diff/io.py` | 1–133 | NPZ/NaN/`runtime_info` | JSON `allow_nan=False`；`encode(nan)` 抛 `ValueError`；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机 `shutil.which` = null |
| `docs/SERVER_RUNBOOK.md` | 1–51 | 对照实跑 | 八段顺序与 `--features-dir` / scientific 拒 offline H 与实跑一致；隔离仍 `pending_server` |
| `src/reasoning_diff/executor.py` | 1–109 | 类属性 + `get_executor` + `score_code` | 默认 `UnavailableExecutor`；`ChildProcessExecutor.isolated_sandbox=False`；与 `IsolatedExecutor` 无继承；拒 `exec(`/`eval(` 字面量；无 host `exec(` 调用 |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code` 默认后端 | 默认 `executor_unavailable`，`eligibility=false`；文案含 `host exec is forbidden` |
| `src/reasoning_diff/schema.py` | 1–385 | 产物 `from_dict` / `record_id` | Event `record_id` 含 run + identity；T1 编辑任务重写 `record_id`；T3 编辑行保留基任务 `record_id`（§5 观察） |
| `src/reasoning_diff/splits.py` | 1–184 | CLI `require_split` + A10 锁文件 | Plus `register_test_only_family` 持久化 JSON；跨进程 `family_locked_test`；fit/calibrate 用允许 split |
| `src/reasoning_diff/edits.py` | `apply_value_edit` / pair | prepare pair / 域编辑 | `_try_source_value_pair` 跳过 T3 / placeholder / paragraph / `composition_reference` |
| `src/reasoning_diff/events.py` | 1–274 | prepare 解析 | 夹具 `parse_fixture_events`；scientific `parse_events` + 约束生成 |
| `src/reasoning_diff/graphs.py` | 1–46 | `ancestors` | calibrate RSI 用图祖先 |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 observation 则无任务/行为标签；sham `noise_ref` 仅 `sham:` |
| `src/reasoning_diff/models/collect.py` | 1–261 | tiny collect | scientific `H` 全有限 |
| `src/reasoning_diff/models/generate.py` | 1–201 | scientific prepare | 约束追加 `\nq = <digits>`；`parse_status=constrained_target` |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | 与 event_rows 对齐 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | collect 重分词 | `encode_text` 按字符 `ord` |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `fit` | 掩码未知行；scientific task 头写出有限 `U` |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `conformal_threshold` | 夹具/scientific 均为有限 `q` |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | tiny 走到 `prospective_decode` |
| `src/reasoning_diff/repair.py` | 1–232 | `repair` | fixture offline → `prefill_unavailable`；scientific tiny `k=1..5` 且 `refilled_prefix=true` |
| `src/reasoning_diff/analysis.py` | 1–337 | `analyze` | 无 `p1_table` → `p1=null` / `not_evaluated` |
| `src/reasoning_diff/transfer.py` | 1–86 | `direct_transfer(4096,3584)` | `not_applicable_dimension_mismatch` |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | `--kind` | `t3_musique` / `hotpot` 别名接通 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–85 | `--kind` + `--sidecar` | 无 sidecar 仅 placeholder → prepare 失败；有 sidecar 成功 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–84 | A10 Plus 锁 | `load_gsm_plus` 调用 `register_test_only_family` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 51–104 | `--kind hotpot` | `document_edit`；CLI 不再强制 pair |
| `src/reasoning_diff/tasks/t3_musique.py` | 10–110 | `--kind t3_musique` | `expression=composition_reference`；pair 被跳过 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 36–51 | `--kind t4_boundary` | `kind=t4_question` |
| `src/reasoning_diff/rng.py` | 1–53 | intervene `StreamBank` | CLI intervene 使用 |
| `src/reasoning_diff/baselines.py` | 1–125 | CLI `fit` | verbalizer / attention_* |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | CLI fit | `baseline=boundary_mlp` |
| `tests/test_cli_pipeline.py` | — | 读，未当作验收 | 绿测不是 OPS-01 |

**抽样未做完整工程审查：** `models/tiny.py`、`models/adapters.py`、T1 official 内部、`t2_noop.py`。adapters **未被** 八段通用子命令调用。

## 3. 已执行检查与结果

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。产物 `$E=%TEMP%\rd-e-r14-w8q3n5`。夹具 `tests/fixtures/t1_tiny.json`。

### 3.1 用户 CLI 入口

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`$E`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir` |
| `calibrate --help` | **0** | `--features-dir` **与** `--labels-dir`；`--in-dir` 在 argparse 层 **不是** `required`（运行期拒绝，见 §3.6） |
| `fit --help` | **0** | `--labels-dir`；`--in-dir` 同样非 argparse required |
| `prepare --help` | **0** | `--sidecar`、`--kind`、`--split-fractions` |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**）

目录：`$E\fx\`。

| 阶段 | 退出码 | 清单 | 关键产物 |
|---|---|---|---|
| prepare | **0** | digest 自洽，`success_count=1` | `tasks.jsonl` 2 行；默认 `role=probe_train` |
| collect tiny | **0** | 含 `tasks.jsonl`、`features.npz`、`event_rows.jsonl` | `H` `[2,32]` 全有限；`weight_source=random_init`；`H[0]≠H[1]`（maxabs≈0.00567） |
| label | **0** | `labels.jsonl` | `record_id=label:q:p2` |
| fit `--split probe_train` | **0** | `probes.jsonl` | task 头 `U` `[32,32]` 全有限 |
| calibrate `--features-dir collect` | **0** | `calibration.jsonl` | `scores≈[0.00502331, 0.00502337]`，`q=0.00502337`，`status=finite`，`unit=problem` |
| intervene | **0** | `interventions.jsonl` | `status=prospective_decode`，`timing=offline_hidden`；`relative.donor_kind=same_source_diff_value` |
| repair `--mask task_oracle` | **0** | `repairs.jsonl` | `record_id=repair:fix-t1-001:task_oracle:k1`；默认 backend=offline → `prefill_unavailable` |
| analyze | **0** | `report.json` 进清单 | `p1=p2=p3=null`，`status=not_evaluated`，`scientific_conclusion=null` |
| collect `--backend offline` | **0** | 另目录 | `H` `[1,8]`，`weight_source=offline_prefix_ids` |
| collect `--shard` | **0** | 两枚 shard | `traces-shard-0000.jsonl` / `0001.jsonl` |

**接线：** 每阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。抽查成功 `manifest.digest` 独立重算均为 True。`code_revision=46a6e26…`。

`analyze` `transfer`：`source_dim=4096`，`target_dim=3584`，`status=not_applicable_dimension_mismatch`。Week-8：`gate0/1/2.decision=unregistered`，`skip_p2_p3=true`。

### 3.3 scientific tiny 八段与 collect `tasks.jsonl`

runbook 本地 scientific：`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。目录：`$E\sc\`。`--in-dir` 串联：prepare→collect/label；fit 用 collect+label；calibrate 用 fit+collect+label；intervene 用 collect；repair 用 prepare；analyze 用 label。

| 阶段 | 退出码 | 要点 |
|---|---|---|
| prepare | **0** | `n_traces=7`：base / t0p / edit / source / 两枚 extra edit / sham；皆 `metadata.parse_status=constrained_target` |
| collect `--backend tiny` | **0** | **写出 `s-col/tasks.jsonl`**；`H` `[7,32]` 全有限；`event_rows` 7 行，皆 `node_id=q` |
| label | **0** | first-seen premise 顺序 **`p2`, `p1`**（跳过 `sham:`） |
| fit | **0** | `input_hashes` 含 `s-col/tasks.jsonl`；task 头有限 `U`；behavior 头 `no_known_labels` |
| calibrate | **0** | 4 个 problem unit，`q=0.00502359`，`status=finite` |
| intervene | **0** | `prospective_decode` / `offline_hidden` |
| repair `--backend tiny --eval-mode scientific` | **0** | `k=1..5`，皆 `status=ok`，`refilled_prefix=true` |
| analyze | **0** | 同样 `p1=null` / `not_evaluated` / `scientific_conclusion=null` |

**collect 复制 `tasks.jsonl`（独立确认）：**

- `$E\fx\collect\tasks.jsonl` 与 `$E\sc\s-col\tasks.jsonl` **均存在**，进入各自 collect `manifest.file_hashes`。
- 与对应 prepare 目录 **字节全等**。SHA-256 均为 `a6ca1a4d4f5ef4c950be39da00864229159b9edb9b74bd93fb6af367f1194eb7`。
- scientific fit 的 `input_hashes["s-col/tasks.jsonl"]` 对该文件做 HASH VERIFY，为 True。
- 前提顺序 `["p1","p2"]`。

**列序对照（有 `tasks.jsonl` 时；fit 用 collect 文件，不是 first-seen）：**

1. labels first-seen（跳过 `sham:`）：**`p2`, `p1`**。
2. `_find_tasks_jsonl(s-col, s-lab)` 返回 **`s-col\tasks.jsonl`**（不是 label 目录、也不是祖先）。
3. `_e_premise_ids(task_from_that_file, labels)` = **`["p1","p2"]`**。
4. `_e_premise_ids(None, labels)` = **`["p2","p1"]`**（纯 first-seen）。两者 **不相等**。

scientific 事件仍是约束 `\nq = <digit>`，**不是** §4.1 自然 CoT。tiny `random_init` **不是** MODEL-01。

### 3.4 无本题 `tasks.jsonl` 必须失败（C6-M-01）；祖先 `col/` WRONG-TASK 不得被用（A12-03）

隔离树 `$ISO`。从夹具 collect 复制特征后删除 `tasks.jsonl`；labels 副本同样无 `tasks.jsonl`。

| 命令 | `_find_tasks_jsonl` | 退出码 | `failure.json` |
|---|---|---|---|
| `fit --in-dir $ISO/feat_with --labels-dir $ISO/labs_copy`（保留 tasks） | `feat_with/tasks.jsonl` | **0** | 无 |
| `fit --in-dir $ISO/feat_none --labels-dir $ISO/labs_copy`（已删 tasks） | **`None`** | **1** | `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order` |
| `calibrate --in-dir $ISO/probe_only --features-dir feat_none --labels-dir labs_copy` | **`None`** | **1** | `ValueError: calibrate requires tasks.jsonl so E columns follow task.premises, not label order` |

`feat_none` 无 `tasks.jsonl`；`_find_tasks_jsonl(feat_none, labs_copy)` 独立 import 确认为 `None`。清单 `success_count=0`，写出 `failure.json`。这是用户 CLI 实跑，不是作者表，也不是 pytest。

**不是 first-seen 静默回退：** 开审源码 `cli.py` 612–619：有 labels 且 `task_path` 为空则立刻 `raise ValueError`，不再调用 `_e_premise_ids(None, labels)` 给 E 列赋 `j`。

**A12-03 祖先 `col/` WRONG-TASK（独立构造，不经 pytest）：**

树：`$ISO/a12/col/tasks.jsonl`（`task_id=WRONG-TASK`，前提对调为 **`[p2,p1]`**）；`$ISO/a12/nest/feat` 与 `nest/lab` 为夹具 collect/label 副本且 **无** `tasks.jsonl`。

| 检查 | 结果 |
|---|---|
| 当前 `_find_tasks_jsonl(nest/feat, nest/lab)` | **`None`** |
| 旧 4 层 + extras（`col`/`collect`/`prepare`/…）查找 | 命中 `$ISO/a12/col/tasks.jsonl`，文件含 `WRONG-TASK` |
| `fit --in-dir nest/feat --labels-dir nest/lab` | **exit 1**，文案同 C6；**未**写出 probes |
| `calibrate --in-dir probe_only --features-dir nest/feat --labels-dir nest/lab` | **exit 1**，同样 `calibrate requires tasks.jsonl …` |

因此：祖先 `col/tasks.jsonl` **没有**被绑定。若仍走 r12 的 4 层 extras，E 列会静默变成 `[p2,p1]`。本冻结只搜传入目录。

### 3.5 T3 `hotpot` / `t3_musique` prepare；gsm_symbolic sidecar；t4_boundary

仓库自带夹具，用户 CLI，不经 pytest。

| 命令 | 退出码 | 产物 |
|---|---|---|
| `prepare --kind hotpot --fixture tests/fixtures/t3_hotpot_one.json` | **0** | `source=hotpotqa`，`tier=T3`，3 前提；`edits.jsonl` **1** 行 `kind=document`；**无** `source_value_pair` |
| `prepare --kind t3_musique --fixture tests/fixtures/t3_musique_pair.json` | **0** | `source=musique`，`tier=T3`，节点 `expression=composition_reference`；`edits.jsonl` **1** 行 `kind=paragraph`；**无** pair |
| `prepare --kind gsm_symbolic`（无 `--sidecar`） | **1** | `failure.json`：`ValueError: no editable non-placeholder premise`；清单 `success_count=0` |
| 同上 + `--sidecar tests/fixtures/t2_formula_sidecar.json` | **0** | edits 含 `value` + `source_value_pair` |
| `prepare --kind t4_boundary --fixture tests/fixtures/t4_boundary.json` | **0** | `source=t4_boundary`；`kind=t4_question` |

`_try_source_value_pair` 对 `hotpotqa` / `musique` / `humaneval_derived` / `t4_boundary` / `tier==T3` / `composition_reference` 返回 `None`，因此域编辑成功后不再 `recompute` 算术 pair。

**ID 观察（不否决 T3 exit 0）：** hotpot 编辑行 `task_id=hp-1::DocA` 但 `record_id` 仍为 `hp-1`；musique `msq-9::answerable::p0` 的 `record_id` 仍为 `msq-9::answerable`。

### 3.6 缺 `--in-dir` 必须失败

argparse 把 `--in-dir` 标成可选；运行期拒绝。均带 `--out-dir`。

| 子命令 | 退出码 | `failure.json` | 清单 |
|---|---|---|---|
| fit | **1** | `fit requires --in-dir` | `success=0` / `failure=1` |
| calibrate | **1** | `calibrate requires --in-dir` | 同上 |
| intervene | **1** | `intervene requires --in-dir` | 同上 |
| repair | **1** | `repair requires --in-dir` | 同上 |
| analyze | **1** | `analyze requires --in-dir` | 同上；**无** `report.json` |
| collect（额外） | **1** | `collect requires --in-dir` | 同上 |
| label（额外） | **1** | `label requires --in-dir with observations.jsonl` | 同上 |

文件当作 `--in-dir`：`analyze --in-dir tests/fixtures/t1_tiny.json` → **1**，`NotADirectoryError: --in-dir must be a directory`。`$E\miss\an` 仅有 `failure.json` + 失败清单。

### 3.7 `ChildProcessExecutor.isolated_sandbox is False`

独立 import + 调用，不经 pytest。

| 检查 | 结果 |
|---|---|
| `ChildProcessExecutor.isolated_sandbox` | **`False`** |
| `IsolatedExecutor.isolated_sandbox` | `True` |
| `isinstance(ChildProcessExecutor(), IsolatedExecutor)` | **False** |
| `issubclass(ChildProcess, Isolated)` / 反向 | **False / False** |
| MRO | 两者都只继承 `object`；**无共同实现基类** |
| `SubprocessExecutor is ChildProcessExecutor` | True（别名） |
| `get_executor()` 默认 | `UnavailableExecutor`（`IsolatedExecutor` 子类），`isolated_sandbox=True` |
| `get_executor("child_process")` | `ChildProcessExecutor`，`isolated_sandbox=False` |
| `score_code("print(1)","assert True")` 默认 | `status=executor_unavailable`，`value=null`，`eligibility=false`，reason=`no isolated backend configured; host exec is forbidden` |
| 显式 child：`score_code("x=1","assert x==1", executor=child)` | `status=ok`，`value=1.0`（普通子进程，**不是**沙箱） |
| child `submit` 含 `exec(` / `eval(` | `status=rejected`，`submission mentions exec/eval` |
| `forbid_host_exec` | `RuntimeError: host execution of model/dataset code is forbidden` |
| `src/` 生产路径 `exec(` | 仅 `executor.py` 把 `"exec("` / `"eval("` 当拒绝字符串；**无** 内建 host `exec(` 调用。`repair.py` / tiny collect 的 `model.eval()` 是 PyTorch eval 模式，不是 `eval(` |

默认评分路径 **不会** 落到 ChildProcess。Child 必须 `get_executor("subprocess"|"child_process")` 才构造。这不是 host `exec` 回退。Linux cgroup 仍 `pending_server`。`ChildProcessExecutor` **不是** `IsolatedExecutor`。

### 3.8 resume 不覆盖成功清单

| 命令 | 退出码 | 清单 |
|---|---|---|
| `prepare --fixture F --out-dir $E/resume/prepare` | **0** | digest `1b41b2e39dcf9ee7…`，`success_count=1` |
| 同上 `--resume`（配置相同） | **0** | digest **未变**；无 `failure.json` |
| 同上 `--resume --edit-value 99` | **1** | `ValueError: resume run_spec mismatch: edit_value` |

失败后：成功清单 digest **仍为** `1b41b2e39dcf9ee7…`；`success_count=1`；`file_hashes` **不含** `failure.json`。`failure.json` 作为旁路文件存在，但 `main()` 在已有成功清单时 `preserve=True`，不调用失败清单覆盖。独立复核 `file_hashes` 与开审后成功跑的 9 个产物哈希一致。

### 3.9 scientific collect `backend!=tiny` 拒绝

`collect --eval-mode scientific --backend offline --in-dir s-prep --out-dir s-col-off` → **exit 1**，`ValueError: scientific collect refuses offline_prefix_ids as H`。目录无 `features.npz`；清单 `success=0` / `failure=1`，仅 `failure.json`。

### 3.10 A10-04：Plus 然后 Symbolic，两个顺序 CLI 进程

锁文件：`.planning/research/.cache/gsm_test_only_families.json`。审查开始原文 `["gsm8k-12", "q:ada has 4 apples and buys 3 more. how many apples?"]`。官方 Plus/Symbolic 夹具共享 `original_id=gsm8k-12` 与同一问句。

独立计算 `assign_split("gsm8k-12", seed=…, source="gsm_symbolic")`（**无锁、无 Plus**）：

- `seed=0` → `test`（哈希落入最后 15% 桶；**不能**用来证明锁）
- `seed=6` → **`probe_train`**

因此 A10 用 `--split-seed 6`，并在两进程之间清空再观察持久化 JSON。每个 `prepare` 都是新的 `python -m` 进程（RAM 不共享）。测完已把锁文件还原为开审原文。

| 进程 | 锁文件 | `splits.jsonl.role` |
|---|---|---|
| 删除锁后 | 不存在 | — |
| P1：`prepare --kind gsm_symbolic --sidecar … --split-seed 6`（孤立，无先前 Plus） | 结束后 **仍不存在**（Symbolic **不**写锁） | **`probe_train`** |
| P2：`prepare --kind gsm_plus --fixture t2_gsmplus_one.json --split-seed 6` | 写出 `["gsm8k-12", "q:ada has …"]` | **`test`**（Plus 本身 test-only） |
| P3：再跑同一 Symbolic CLI（新进程，只读已持久化 JSON） | 仍为上述 JSON | **`test`** |

P3 在 RAM 已空的新进程里得到 `test`，而同一 `seed=6` 在无锁时是 `probe_train`。这是持久化 JSON 锁，不是同进程集合、也不是 seed=0 的哈希巧合。

孤立 Symbolic-only（无 Plus 锁文件）**可以是** `probe_train`——本通道在 seed=6、锁已删时独立观察到。

### 3.11 其它接线（支持项）

| 项 | 证据 |
|---|---|
| 两次独立 prepare | `tasks.jsonl` hash 全等，digest 全等 |
| JSON 拒 NaN | `encode({'x': nan})` → `ValueError: Out of range float values are not JSON compliant` |
| 拒 `latest` | `write_run_spec(..., config.model='latest')` → `config.model cannot use mutable identity 'latest'` |
| 产物无 `.tmp` | `$E.rglob('*.tmp')` 为空 |

## 4. 命令表

前缀：`python -m reasoning_diff`。夹具 `F=tests/fixtures/t1_tiny.json`。`$E=%TEMP%\rd-e-r14-w8q3n5`。`$ISO=$E/iso`。

| tag | argv（相对） | exit | 秒 | 关键产物 |
|---|---|---|---|---|
| help | `--help` | 0 | 0.22 | 八段子命令 |
| help_collect | `collect --help` | 0 | 0.23 | `--backend` `--shard` `--in-dir` |
| help_fit | `fit --help` | 0 | 0.22 | `--labels-dir` |
| help_calibrate | `calibrate --help` | 0 | 0.23 | `--features-dir` `--labels-dir` |
| help_prepare | `prepare --help` | 0 | 0.23 | `--sidecar` `--kind` |
| help_from_temp | `--help`（cwd=`$E`） | 0 | 0.23 | 不依赖 cwd |
| help_no_pythonpath | `--help`（无 PYTHONPATH） | **1** | 0.05 | `No module named reasoning_diff` |
| fx_prepare | `prepare --fixture F --out-dir $E/fx/prepare` | **0** | 0.43 | `tasks.jsonl` `manifest.json` |
| fx_collect | `collect --fixture F --in-dir …/prepare --out-dir …/collect --backend tiny` | **0** | 11.75 | `features.npz` `tasks.jsonl` `event_rows.jsonl` |
| fx_label | `label --in-dir …/prepare --out-dir …/label` | **0** | 0.48 | `labels.jsonl` |
| fx_fit | `fit --in-dir …/collect --labels-dir …/label --out-dir …/fit --split probe_train` | **0** | 0.54 | `probes.jsonl`；有限 U |
| fx_calibrate | `calibrate --in-dir …/fit --features-dir …/collect --out-dir …/cal --split calibration` | **0** | 0.57 | `calibration.jsonl` 有限 q |
| fx_intervene | `intervene --in-dir …/collect --out-dir …/intervene` | **0** | 12.52 | `prospective_decode` |
| fx_repair | `repair --in-dir …/prepare --out-dir …/repair --mask task_oracle` | **0** | 0.62 | `repair:fix-t1-001:task_oracle:k1` |
| fx_analyze | `analyze --in-dir …/label --out-dir …/analyze` | **0** | 0.63 | `report.json` 进清单 |
| fx_collect_offline | `collect … --backend offline --out-dir …/collect_off` | **0** | 0.70 | `H[1,8]` offline_prefix_ids |
| fx_collect_shard | `collect … --backend tiny --shard --out-dir …/collect_shard` | **0** | 12.53 | `traces-shard-000{0,1}.jsonl` |
| sc_prepare | `prepare --fixture F --out-dir …/s-prep --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1` | **0** | 10.68 | 7 traces，`constrained_target` |
| sc_collect | `collect --fixture F --in-dir …/s-prep --out-dir …/s-col --eval-mode scientific --backend tiny` | **0** | 10.57 | **`s-col/tasks.jsonl` 字节=prepare** |
| sc_label | `label --in-dir …/s-prep --out-dir …/s-lab` | **0** | 0.53 | first-seen `p2` 然后 `p1` |
| sc_fit | `fit --in-dir …/s-col --labels-dir …/s-lab --out-dir …/s-fit --split probe_train` | **0** | 0.53 | hashes 含 s-col/tasks；VERIFY True |
| sc_calibrate | `calibrate --in-dir …/s-fit --features-dir …/s-col --labels-dir …/s-lab --out-dir …/s-cal --split calibration` | **0** | 0.53 | 4 problem scores，有限 q |
| sc_intervene | `intervene --in-dir …/s-col --out-dir …/s-int` | **0** | 9.87 | `prospective_decode` |
| sc_repair | `repair --in-dir …/s-prep --out-dir …/s-rep --mask task_oracle --eval-mode scientific --backend tiny` | **0** | 9.63 | k=1..5，`refilled_prefix=true` |
| sc_analyze | `analyze --in-dir …/s-lab --out-dir …/s-an` | **0** | 0.45 | `p1=null`，gates unregistered |
| sc_collect_offline | `collect … --eval-mode scientific --backend offline --out-dir …/s-col-off` | **1** | 0.43 | `refuses offline_prefix_ids as H` |
| iso_fit_with_tasks | `fit --in-dir $ISO/feat_with --labels-dir $ISO/labs_copy` | **0** | 0.59 | find → feat_with/tasks.jsonl |
| iso_fit_without_tasks | `fit --in-dir $ISO/feat_none --labels-dir $ISO/labs_copy` | **1** | 0.33 | find=`None`；`fit requires tasks.jsonl …` |
| iso_cal_without_tasks | `calibrate --in-dir $ISO/probe_only --features-dir feat_none --labels-dir labs_copy` | **1** | 0.32 | find=`None`；`calibrate requires tasks.jsonl …` |
| a12_fit_ancestor_col | `fit --in-dir $ISO/a12/nest/feat --labels-dir …/lab` | **1** | 0.27 | 祖先 `col/WRONG-TASK` **未**被用 |
| a12_cal_ancestor_col | `calibrate --in-dir probe_only --features-dir nest/feat --labels-dir nest/lab` | **1** | 0.25 | 同上 |
| prep_hotpot | `prepare --kind hotpot --fixture tests/fixtures/t3_hotpot_one.json` | **0** | 0.51 | document edit，无 pair |
| prep_t3_musique | `prepare --kind t3_musique --fixture tests/fixtures/t3_musique_pair.json` | **0** | 0.44 | paragraph edit，无 pair |
| prep_gsm_nosidecar | `prepare --kind gsm_symbolic --fixture tests/fixtures/t2_symbolic_one.json` | **1** | 0.23 | `no editable non-placeholder premise` |
| prep_gsm_sidecar | 同上 + `--sidecar tests/fixtures/t2_formula_sidecar.json` | **0** | 0.48 | `value` + `source_value_pair` |
| prep_t4_boundary | `prepare --kind t4_boundary --fixture tests/fixtures/t4_boundary.json` | **0** | 0.52 | `t4_question` |
| miss_fit | `fit --out-dir …/miss/fit --split probe_train` | **1** | 0.27 | `fit requires --in-dir` |
| miss_calibrate | `calibrate --out-dir …/miss/cal --split calibration` | **1** | 0.24 | `calibrate requires --in-dir` |
| miss_intervene | `intervene --out-dir …/miss/int` | **1** | 0.25 | `intervene requires --in-dir` |
| miss_repair | `repair --out-dir …/miss/rep` | **1** | 0.24 | `repair requires --in-dir` |
| miss_analyze | `analyze --out-dir …/miss/an` | **1** | 0.25 | `analyze requires --in-dir`；无 `report.json` |
| miss_collect | `collect --fixture F --out-dir …/miss/col` | **1** | 0.24 | `collect requires --in-dir` |
| miss_label | `label --out-dir …/miss/lab` | **1** | 0.37 | 缺 observations.jsonl |
| file_indir_analyze | `analyze --in-dir F --out-dir …/miss/file_an` | **1** | 0.35 | `--in-dir must be a directory` |
| res_prepare | `prepare --fixture F --out-dir …/resume/prepare` | **0** | 0.51 | 成功清单 |
| res_prepare_resume | 同上 `--resume` | **0** | 0.25 | digest 未变 |
| res_prepare_mismatch | 同上 `--resume --edit-value 99` | **1** | 0.33 | 成功清单保留 |
| repro_a / repro_b | `prepare --fixture F --out-dir …/repro/{a,b}` | **0** / **0** | 0.45 / 0.58 | tasks/digest 全等 |
| a10_iso_symbolic | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（无锁文件） | **0** | 0.49 | `role=probe_train`；**不**写锁 |
| a10_plus | `prepare --kind gsm_plus --fixture t2_gsmplus_one.json --split-seed 6` | **0** | 0.45 | `role=test`；写出锁 JSON |
| a10_seq_symbolic | 同 iso Symbolic，**新进程** | **0** | 0.43 | `role=test`（只靠持久化 JSON） |

共 52 条用户 CLI 调用。进程内执行器 / JSON / `latest` 检查不列入上表。

## 5. 必做项判定

| # | 要求 | 判定 | 证据 |
|---|---|---|---|
| 1 | 夹具八段 prepare→…→analyze | **PASS** | §3.2 八段 exit 0，清单自洽 |
| 2 | scientific tiny 八段；`--in-dir` 串联；collect 有 `tasks.jsonl`；fit 用该文件而非 first-seen | **PASS** | §3.3 字节复制 + HASH VERIFY；E=`[p1,p2]` ≠ first-seen `[p2,p1]` |
| 2b | 无本题 `tasks.jsonl` 时 fit/calibrate 失败（C6-M-01） | **PASS** | §3.4 隔离 find=`None` → exit 1 |
| 2c | 祖先 `col/` WRONG-TASK 不得被用（A12-03） | **PASS** | §3.4 旧查找会命中 WRONG-TASK；当前 CLI exit 1 |
| 3 | T3 `hotpot` / `t3_musique` exit 0；gsm_symbolic 无 sidecar fail-closed；有 sidecar / t4 exit 0 | **PASS** | §3.5 |
| 4 | 缺 `--in-dir` 失败 | **PASS** | §3.6 指定五段 + collect/label 皆 exit 1 |
| 5 | `ChildProcessExecutor.isolated_sandbox is False`；Isolated ≠ Child；无 host exec 回退 | **PASS** | §3.7 |
| 6 | Resume 不覆盖成功清单 | **PASS** | §3.8 digest/success 保留 |
| 7 | scientific collect `backend!=tiny` 拒绝 | **PASS** | §3.9 |
| 8 | Plus→Symbolic 两进程：锁后 Symbolic=`test`；孤立无锁可为 `probe_train`（A10-04） | **PASS** | §3.10 seed=6 |

### 残留观察（不否决上表）

- **冻结漂移：** 写报告时 `HASH_MISMATCH`。本通道未改生产文件。连续通过计数 **不能** 把写报告时的树标成 `1f61fd06…`。
- **`--in-dir` argparse 非 required：** 运行期 `ValueError` 已足够失败。
- **T3/T4 编辑 `record_id`：** 编辑行 `task_id` 变了，`record_id` 仍是基任务。不阻止 prepare exit 0。
- **calibrate 仍会在兄弟目录找 `labels.jsonl`**（`parent/label|lab|labels`）。A12-03 约束的是 `tasks.jsonl`，不是 labels 旁路。
- **seed=0 的官方 Symbolic 无锁也是 `test`：** 哈希桶，不是 A10。本通道用 seed=6 把无锁 `probe_train` 与有锁 `test` 拆开。
- **A10 测完已还原锁文件**，避免污染其它通道。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 开始时冻结 hash 复现 | 开始 **HASH_MATCH** §1 |
| 夹具 + scientific 八段可调度 | §3.2 / §3.3 |
| collect 复制 tasks；fit 绑定 collect 文件 | §3.3 |
| 无本题 tasks 且 find=`None` 时 fit/calibrate 失败 | §3.4 |
| 祖先 `col/` WRONG-TASK 不被绑定 | §3.4 |
| T3 prepare 不再被 pair 打断 | §3.5 |
| GSM-Symbolic 无 sidecar fail-closed | §3.5 |
| 缺 `--in-dir` 失败 | §3.6 |
| Child 非沙箱；默认不可用；无 host exec | §3.7 |
| resume 失败保留成功清单 | §3.8 |
| scientific 拒 offline H | §3.9 |
| Plus 锁跨进程迫使 Symbolic=`test` | §3.10 |
| JSON 拒 NaN；拒 `latest` | §3.11 |
| 同机同参数 prepare 可复现 | §3.11 |
| 各成功 `manifest.digest` 自洽 | §3.2 / §3.3 |
| shard 完整 | §3.2 |
| `report.json` 进清单 | analyze `file_hashes` |
| 直接迁移维度拒绝 | 4096≠3584 |
| Week-8 未注册 | `unregistered` / `scientific_conclusion=null` |
| analyze 不编造 P1–P3 | 仅有 labels 时 `p1=null` |
| `git -C` revision | 产物仍 `46a6e26…` |
| repair `record_id` 含 group 与 k | 夹具 k1；scientific k1..k5 |
| 文件 `--in-dir` 拒绝 | §3.6 |

Gate 0–2 未注册与 `scientific_conclusion=None` **不是** 缺陷。tiny 随机权重 **不是** MODEL-01。约束 `\nq = <digit>` 是本机可解析接口，不是自然 CoT。从未加载过 Plus 的孤立 Symbolic 在无锁且哈希落入训练桶时进 `probe_train` **不是** A10-04 残留。

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |
| 漂移后（`401e509b…`）树上的八段是否仍成立 | 本通道未在漂移后重跑全套；不得用开始时的 exit 0 给当前树背书 |

## 8. 结论

审查开始时 **`HASH_MATCH`** `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`（61 文件）。全部主套件 `python -m` 证据绑定该快照。写报告前 **`HASH_MISMATCH`** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（仍 61 文件）。本通道未改生产代码。

相对用户指定的独立复跑：夹具八段、scientific 八段与 `--in-dir` 串联、collect 复制 `tasks.jsonl` 且 fit 用该文件而非 first-seen、隔离无 `tasks.jsonl` 时 fit/calibrate 失败、祖先 `col/` WRONG-TASK 不被使用、T3 hotpot/musique 与 sidecar/t4 prepare、缺 `--in-dir` 失败、`ChildProcessExecutor.isolated_sandbox is False`、resume 不覆盖成功清单、scientific 拒 offline H、Plus 后新进程 Symbolic 被持久化 JSON 锁为 `test` 而孤立无锁可为 `probe_train`——**全部成立**。

这只证明用户 CLI 在 tiny/fixture 上可调度，且缺图时 fit 不再静默走 labels 首次出现序或祖先 `col/`。**不是** OPS-01，**不是** 真实模型上的论文正确性，也 **不能** 把写报告时的脏树标成声明冻结。

**本通道（指定工程接线，绑定开审快照）：`PASS`。**

下一步（建议，非本通道实施）：停止并行改冻结集后重新冻结，再在新 hash 上重跑 A–F；不要用本报告给 `401e509b…` 背书。
