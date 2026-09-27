# E：端到端工程审查（round-21）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮其它通道报告。`ISSUES.md` 仅作作者声称，不采信关闭声明。

夹具烟测与 scientific tiny **不是** 科学全跑，也 **不是** OPS-01 / MODEL-01。本通道不把 `exit 0`、清单存在或 `report.json` 写成论文正确性。

**冻结核验：审查开始、CLI 套件结束、本报告落盘后再算均为 `HASH_MATCH`。** 本通道未改 `src/`、`tests/`、`pyproject.toml`。按本轮指令：`HASH_MISMATCH` → 本通道 `FAIL`。

八段实跑目录为独立命名的 `stage_a`…`stage_h`，**不用** `prep`。兄弟 `prep` / `lab` / `label` / `labels` 只作为 pair finder / labels finder 陷阱存在。

本轮相对 r20 不转移的两项独立加严：`cmd_calibrate` **函数实跑**（有/无兄目录 `lab/labels.jsonl`，间谍 finder 实参）；70 字 intervene **间谍 hook `prompt_ids` 长度**（不只看 `prefix_truncated`）。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 03:27–03:31 +08:00（CLI 套件）；报告落盘后复算冻结 |
| 声称冻结 hash | `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb`（用户给定；与 `.planning/audits/round-21/VERSION.md` 原文一致；61 文件） |
| 独立复算（审查开始） | **`HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**61** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb`。当时 `cli.py` **1268** 行 / **61734** 字节。 |
| 独立复算（CLI 套件结束） | **`HASH_MATCH`**。同一脚本仍 61 文件，同一摘要。 |
| 独立复算（本报告落盘后再算） | **`HASH_MATCH`**。仍 61 文件，同一摘要。写入本文件不进冻结集。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；产物 `environment.repo_root=C:\Users\22688\Desktop\diff`） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch` 供 tiny） |
| 审查范围 | 用户指定：夹具八段；scientific tiny 串联；collect 复制 `tasks.jsonl` **与** `edits.jsonl`；无本地 tasks 则 fit/calibrate raise；scientific `probes.jsonl` 四条 §8 行存在且为 `refused_not_section8`、无 score；`cmd_calibrate` 有/无兄 `lab` 输出相同且 finder 不收兄路径；70 字 intervene 间谍 hook `prompt_ids` 长度 >64；`ChildProcessExecutor.isolated_sandbox is False`；resume 保留成功清单；Plus 然后 Symbolic 新进程锁 `test`；T3 prepare；缺 `--in-dir` 失败 |
| 指定必读 | `cli.py`、`io.py`、`schema.py`、`executor.py`、`splits.py` |
| 实跑入口 | `python -m reasoning_diff`；产物根 `.planning/audits/round-21/_e_scratch/`（下文 `$E`），未写入 `src/` / `tests/` / `pyproject.toml` |
| pytest | 作者声称 167 passed。本通道 **未** 把 pytest 当作验收，也未重跑测试套件。 |

A10-04 期间快照并移走仓库锁文件 `.planning/research/.cache/gsm_test_only_families.json`（不在冻结集），测完按字节恢复。`lock_restore_ok=true`。

## 2. 逐文件覆盖

行号为 **本轮冻结快照**（`cli.py` 1268）。

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–1268 | 通读 + `python -m` 夹具八段 + scientific tiny + 复制 hunt + pair/lab 陷阱 + **`cmd_calibrate` 函数间谍** + **70 字 hook `prompt_ids` 间谍** + T3 + 缺 in-dir + resume | 八段可调度；collect 复制 `tasks.jsonl` **与** `edits.jsonl`；`_load_source_value_pair` 只读给定目录；`_find_labels_jsonl` / `_find_tasks_jsonl` 只看传入目录自己的文件；无本地 tasks 则 fit/calibrate raise；scientific fit **写出四条** `refused_not_section8` 且无 `score`；`cmd_calibrate` 有/无兄 `lab` 校准字节相同，finder 实参不含兄路径；70 字 hook `prompt_ids` 长度为 70（>64）；intervene 超 96 token 拒绝且不写干预行；T3 prepare 不被 pair 打断；缺 in-dir 失败；resume 不覆盖成功清单 |
| `src/reasoning_diff/io.py` | 1–133 | NPZ/NaN/`runtime_info` | JSON `allow_nan=False`；`encode(nan)` 抛 `ValueError`；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/schema.py` | 1–385 | 产物 `from_dict` / `record_id` | Event `record_id` 含 run + identity；T3 编辑行内嵌 task `task_id` 变了但 `record_id` 仍是基任务（§5 观察） |
| `src/reasoning_diff/executor.py` | 1–109 | 类属性 + `get_executor` + `score_code` | 默认 `UnavailableExecutor`；`ChildProcessExecutor.isolated_sandbox=False`；与 `IsolatedExecutor` 无继承；拒 `exec(`/`eval(` 字面量；无 host `exec(` 调用 |
| `src/reasoning_diff/splits.py` | 1–184 | CLI `require_split` + A10-04 两进程 | 锁写入 `.planning/research/.cache/gsm_test_only_families.json`；`family_locked_test` 并集磁盘；新进程 Symbolic 读到 `test` |
| `src/reasoning_diff/artifacts.py` | 1–85 | digest / `success_count` / shard | 各成功阶段 digest 自洽；失败清单 `success=0`；两枚 shard 进清单 |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code` 默认后端 | 默认 `executor_unavailable`，`eligibility=false`；文案含 `host exec is forbidden` |
| `src/reasoning_diff/__main__.py` | 1–4 | `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机 `shutil.which` = null |
| `docs/SERVER_RUNBOOK.md` | 1–51 | 对照实跑 | 八段顺序与 `--features-dir` / resume / scientific 拒 offline H 与实跑一致；隔离仍 `pending_server` |
| `src/reasoning_diff/edits.py` | — | prepare pair / 域编辑 | `_try_source_value_pair` 跳过 T3 / placeholder / paragraph / `composition_reference` |
| `src/reasoning_diff/events.py` | — | prepare 解析 | 夹具 `parse_fixture_events`；scientific `parse_events` + 约束生成 |
| `src/reasoning_diff/graphs.py` | — | `ancestors` | calibrate RSI 用图祖先 |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 observation 则无任务/行为标签 |
| `src/reasoning_diff/models/collect.py` | — | tiny collect + hook 间谍 | scientific `H` 全有限；`intervene_hidden_decode(prompt_ids)` 70 字路径收到 70 个 id |
| `src/reasoning_diff/models/generate.py` | — | scientific prepare + decode 间谍 | 约束追加 `\nq = <digits>`；`metadata.parse_status=constrained_target`；decode 张量宽 70 |
| `src/reasoning_diff/probes/bilinear.py` | — | `fit` | 掩码未知行；scientific task 头写出有限 `U`/`V`/`b` |
| `src/reasoning_diff/probes/calibrate.py` | — | `conformal_threshold` | 夹具/scientific 均为有限 `q` |
| `src/reasoning_diff/interventions.py` | — | `intervene` | CLI `_expressible_donor`；有 pair meta → 成对 donor；无本地 edits → fallback |
| `src/reasoning_diff/repair.py` | — | `repair` | fixture offline → `prefill_unavailable`；scientific tiny `k=1..5` 且 `refilled_prefix=true` |
| `src/reasoning_diff/analysis.py` | — | `analyze` | 无 `p1_table` → `p1=null` / `not_evaluated`；不从标签冒充 length/op/rho |
| `src/reasoning_diff/transfer.py` | — | `direct_transfer(4096,3584)` | `not_applicable_dimension_mismatch` |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | — | `--kind gsm_plus` | `register_test_only_family` 落盘；role=`test` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | — | `--kind` + `--sidecar` | **不**自行登记锁；读磁盘锁后可为 `test` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | — | `--kind hotpot` | `document` 编辑；CLI 不再强制 pair |
| `src/reasoning_diff/tasks/t3_musique.py` | — | `--kind t3_musique` | `expression=composition_reference`；pair 被跳过 |
| `src/reasoning_diff/baselines.py` | — | CLI `fit` | fixture 写 verbalizer/attention_*；scientific **拒绝** 编造 §8 分 |
| `src/reasoning_diff/rng.py` | — | intervene `StreamBank` | CLI intervene 使用 |

**抽样未做完整工程审查：** `models/tiny.py`、`models/adapters.py`、T1 official 内部、`t2_noop.py`。adapters **未被** 八段通用子命令调用。

## 3. 已执行检查与结果

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。产物 `$E=.planning/audits/round-21/_e_scratch`。夹具 `tests/fixtures/t1_tiny.json`。

### 3.1 用户 CLI 入口

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`$E`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir`、`--weight-seed` |
| `calibrate --help` | **0** | `--features-dir` **与** `--labels-dir`；`--in-dir` 在 argparse 层 **不是** `required`（运行期拒绝，见 §3.11） |
| `fit --help` | **0** | `--labels-dir`；`--in-dir` 同样非 argparse required |
| `prepare --help` | **0** | `--sidecar`、`--kind`、`--split-fractions` |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**；目录 `stage_a`…`stage_h`）

目录：`$E/fx/`。prepare=`stage_a`，collect=`stage_b`，label=`stage_c`，fit=`stage_d`，calibrate=`stage_e`，intervene=`stage_f`，repair=`stage_g`，analyze=`stage_h`。

| 阶段 | 退出码 | 清单 | 关键产物 |
|---|---|---|---|
| prepare `stage_a` | **0** | digest 自洽，`success_count=1` | `tasks.jsonl` 2 行；`edits.jsonl` 含 `value` + `source_value_pair` |
| collect tiny `stage_b` | **0** | 含 `tasks.jsonl`、`edits.jsonl`、`features.npz`、`event_rows.jsonl` | `H` `[2,32]` 全有限；`weight_source=random_init` |
| label `stage_c` | **0** | `labels.jsonl` | 消费 `stage_a` `observations.jsonl` |
| fit `--split probe_train` | **0** | `probes.jsonl` | `input_hashes` 含 `stage_b/tasks.jsonl` **与** `stage_b/edits.jsonl` **与** `stage_c/labels.jsonl` |
| calibrate `--features-dir stage_b` | **0** | `calibration.jsonl` | `scores≈[0.00502331, 0.00502337]`，`q=0.00502337`，`status=finite`，`unit=problem` |
| intervene | **0** | `interventions.jsonl` | `status=prospective_decode`；`relative.donor_kind=same_source_diff_value`；`prefix_truncated=false`；`prefix_n=14` |
| repair `--mask task_oracle` | **0** | `repairs.jsonl` | `record_id=repair:fix-t1-001:task_oracle:k1`；默认 backend=offline → `prefill_unavailable` |
| analyze | **0** | `report.json` 进清单 | `p1=p2=p3=null`，`status=not_evaluated`，`scientific_conclusion=null` |
| collect `--backend offline` | **0** | 另目录 | exit 0（offline prefix，不是 H） |
| collect `--shard` | **0** | 两枚 shard 进清单 | `traces-shard-0000.jsonl` / `0001.jsonl` |

**接线：** 每阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。各成功 `manifest.digest` 独立重算均为 True。

`analyze` `transfer`：`source_dim=4096`，`target_dim=3584`，`status=not_applicable_dimension_mismatch`。Week-8：`gate0/1/2.decision=unregistered`，`skip_p2_p3=true`。

### 3.3 scientific tiny 八段（同样 `stage_a`…`stage_h`，不用 `prep`）

runbook 本地 scientific：`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。目录：`$E/sc/`。

| 阶段 | 退出码 | 要点 |
|---|---|---|
| prepare | **0** | `n_traces=7`：base / t0p / edit / source / two extra edits / sham；皆 `metadata.parse_status=constrained_target` |
| collect `--backend tiny` | **0** | **写出 `stage_b/tasks.jsonl` 与 `stage_b/edits.jsonl`**；`H` `[7,32]` 全有限 |
| label | **0** | first-seen premise 顺序 **`p2`, `p1`**（再 `sham:q`） |
| fit `--eval-mode scientific` | **0** | `input_hashes` 含 `stage_b/tasks.jsonl`；§8 基线四行全部存在且 `refused_not_section8`（§3.6） |
| calibrate | **0** | 4 个 problem unit，`q=0.00502360`，`status=finite` |
| intervene | **0** | `prospective_decode`；`donor_kind=same_value_diff_source`（本地 pair meta）；`prefix_truncated=false`；`prefix_n=45` |
| repair `--backend tiny --eval-mode scientific` | **0** | `k=1..5`，皆 `refilled_prefix=true` |
| analyze | **0** | 同样 `p1=null` / `not_evaluated` / `scientific_conclusion=null` |
| collect `--backend offline` + scientific | **1** | `scientific collect refuses offline_prefix_ids as H`；**无** 可用 scientific H |

scientific 事件仍是约束 `\nq = <digit>`，**不是** §4.1 自然 CoT。tiny `random_init` **不是** MODEL-01。

**fit 用 collect 复制的 tasks，而不是 labels first-seen 顺序（独立确认）：**

1. 实跑 labels first-seen（跳过 `sham:`）：**`p2`, `p1`**。
2. `_find_tasks_jsonl(sc/stage_b, sc/stage_c)` 返回 **`sc/stage_b/tasks.jsonl`**。
3. `_e_premise_ids(task_from_that_file, labels)` = **`["p1","p2"]`**。
4. `_e_premise_ids(None, labels)` = **`["p2","p1"]`**（纯 first-seen）。两者 **不相等**。

### 3.4 collect 复制 `tasks.jsonl` **和** `edits.jsonl`

独立确认，不信作者表。夹具与 scientific 两条链路均成立。目录名是 `stage_a`/`stage_b`，不是 `prep`。

| 链路 | 文件 | `stage_b` 存在 | 与 `stage_a` 字节全等 | 进 collect `manifest.file_hashes` | SHA-256 |
|---|---|---|---|---|---|
| 夹具 | `tasks.jsonl` | 是 | 是 | 是 | `a6ca1a4d4f5ef4c950be39da00864229159b9edb9b74bd93fb6af367f1194eb7` |
| 夹具 | `edits.jsonl` | 是 | 是 | 是 | `848ce4bba2bd4f00fb3048f72b8bd29ca6bae3254830f899ff0c7eb700406aa4` |
| scientific | `tasks.jsonl` | 是 | 是 | 是 | `a6ca1a4d4f5ef4c950be39da00864229159b9edb9b74bd93fb6af367f1194eb7` |
| scientific | `edits.jsonl` | 是 | 是 | 是 | `8516404b179247e703fb92e43ada0004bb908728a6d7a30d486aa0750622f72f` |

夹具 / scientific fit `input_hashes` 同时含 `stage_b/tasks.jsonl` 与 `stage_b/edits.jsonl`。`_load_source_value_pair(fx/stage_b)` 与 `_load_source_value_pair(sc/stage_b)` 均为有 pair。夹具 intervene 用该本地 pair：`donor_kind=same_source_diff_value`。

### 3.5 pair finder 不走兄弟 `prep`

布局：`$E/hunts/pair_missing_local/`。

- `stage_b/`：夹具 collect 的拷贝，**删除** `edits.jsonl`。
- 兄弟 `prep/edits.jsonl`：原 pair 行（`kind=source_value_pair`）仍在。

| 检查 | 结果 |
|---|---|
| 兄弟 `prep/edits.jsonl` 存在且含 pair | 是 |
| `_load_source_value_pair(stage_b)` | **`None`**（不读兄弟 `prep`） |
| `intervene --in-dir stage_b` | **exit 0** |
| `relative.donor_kind` | **`same_identity_fallback`** |
| 对照：有本地 `edits.jsonl` 的 `fx/stage_f` | `donor_kind=same_source_diff_value` |

缺本地 pair meta 时 donor 只能走 `_expressible_donor` 的 identity/finite fallback。兄弟名叫 `prep` **不能** 把 pair 绑回来。这是用户 CLI 实跑，不是作者表。

### 3.6 scientific `probes.jsonl`：四条 §8 行存在、`refused_not_section8`、无分数

本轮冻结要求四条 §8 行 **必须写出**，不能靠空列表把 `all(...)` 做成空真。独立打开 `$E/sc/stage_d/probes.jsonl`：§8 玩具基线四行 **全部存在**，**只有** `baseline` / `status` / `reason`，**没有** `score` / `f1` / `accuracy`：

| baseline | status | reason | 有 `score`？ |
|---|---|---|---|
| verbalizer | `refused_not_section8` | `no dependency-label verbalizer on this prefix` | 否 |
| attention_mean | `refused_not_section8` | `no attention maps` | 否 |
| attention_rollout | `refused_not_section8` | `no attention maps` | 否 |
| attention_threshold | `refused_not_section8` | `no attention maps` | 否 |

四行键集均为 `{"baseline","reason","status"}`。对照：夹具 fit（非 scientific）**会** 写 verbalizer `status=generated` 且带 `score`。scientific 路径没有把这些玩具分冒充 §8。task 头仍写有限 `U`/`V`/`b`（双线性探测，不是 §8 基线）。`boundary_mlp` 带 `event-rows-only_no_negatives`，不是 §8。

### 3.7 无本地 `tasks.jsonl` 则 fit/calibrate raise；祖先 WRONG-TASK 不绑定

**无本地 tasks，兄弟 `prep` 不救命。** 把夹具 collect/label 拷到 `$E/hunts/no_tasks/`，删除 `col/tasks.jsonl`，**保留兄弟** `no_tasks/prep/tasks.jsonl`。给定目录是 `col` 与 `lab`。

`_find_tasks_jsonl(col, lab)` 独立 import 为 **`None`**。`_find_tasks_jsonl(prep)` 只有在把 `prep` 本身传入时才命中。

| 命令 | 退出码 | `failure.json` |
|---|---|---|
| `fit --in-dir no_tasks/col --labels-dir no_tasks/lab` | **1** | `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order` |
| `calibrate --in-dir probe_only --features-dir col --labels-dir lab`（`probes.jsonl` 在，三目录均无 tasks） | **1** | `ValueError: calibrate requires tasks.jsonl so E columns follow task.premises, not label order` |

`no_tasks/fit/probes.jsonl` **未写出**。

**祖先 `col` WRONG-TASK 不绑定。** 布局：`$E/hunts/ancestor/col/tasks.jsonl` 写成 `task_id=WRONG-TASK`，前提序对调；特征在 `ancestor/deep/x/feat`，标签在 `ancestor/deep/x/labs`。feat/labs **没有** `tasks.jsonl`。

| 检查 | 结果 |
|---|---|
| 祖先 `col/tasks.jsonl` 存在 | 是；`task_id=WRONG-TASK` |
| `_find_tasks_jsonl(feat, labs)` | **`None`** |
| `_find_tasks_jsonl(col)` | 命中该 WRONG-TASK 文件（只因 `col` 本身被传入） |
| `fit --in-dir feat --labels-dir labs` | **exit 1**；同上 ValueError |
| `probes.jsonl` | **未写出** |
| `calibrate --in-dir probe_only --features-dir feat --labels-dir labs` | **exit 1**；同样 ValueError |

旧搜索若走祖先 extras 会绑到 `col` 并把 \(E\) 列换成错题。本冻结只读传入目录自己的 `tasks.jsonl`，祖先 WRONG-TASK **不绑定**。

### 3.8 `cmd_calibrate` 有/无兄目录 `lab`：输出相同，finder 不收兄路径

本轮要求 **直接调用** `cmd_calibrate`，并间谍 finder 实参；不采信 `inspect.getsource`。布局：`$E/hunts/cal_sib/`。

- `with_lab/feat/`：夹具 collect 拷贝（无 `labels.jsonl`）。
- `with_lab/probe/probes.jsonl`：夹具 fit 拷贝。
- `with_lab/lab/labels.jsonl`：**存在**，写成 `p1` 正 / `p2` 负（若被绑入会改变 `truth_i`）。
- `no_lab/`：同样的 feat/probe，**没有** 兄弟 `lab`。

两次都 `labels_dir=None`（不传 `--labels-dir`），只给 `in_dir=probe`、`features_dir=feat`。对 `_find_labels_jsonl` 与 `_find_stage_file` 打补丁记录 `*dirs` 与返回值。

| 检查 | 有兄 `lab` | 无兄 `lab` |
|---|---|---|
| `cmd_calibrate(...)` 返回 | **0** | **0** |
| `calibration.jsonl` 字节 | 与无兄 **全等** | 与有兄 **全等** |
| `scores` / `q` | `[0.00502331, 0.00502337]` / `0.00502337` | 相同 |
| finder `*dirs` | `[None, …/with_lab/probe, …/with_lab/feat]` | `[None, …/no_lab/probe, …/no_lab/feat]` |
| finder 返回 | **`None`** | **`None`** |
| 兄路径出现在 finder 实参或返回？ | **否** | **否** |
| `_find_stage_file("labels.jsonl", …)` | 同样只有 probe/feat；返回 `None` | 同样 |
| `run_spec.input_hashes` 含 `lab/`？ | **否**（只有 `feat/*` 与 `probe/probes.jsonl`） | **否** |

独立对照（不经 `cmd_calibrate`）：

- `_find_labels_jsonl(feat)` → `None`
- `_find_labels_jsonl(probe, feat)` → `None`
- `_find_labels_jsonl(feat, lab)` → **命中** `with_lab/lab/labels.jsonl`（只因把 `lab` **本身传入**）

兄文件确实在盘上；finder **从未收到** 该路径。这不是读源码推断。

**CLI 对照：** `$E/hunts/labels_sib/` 同时放兄弟 `lab/`、`label/`、`labels/` 三份 WRONG 标签。`calibrate --in-dir probe --features-dir feat`（无 `--labels-dir`）exit 0；`input_hashes` 不含任何兄弟 `labels.jsonl`。

### 3.9 70 字 intervene：hook `prompt_ids` 长度 >64

tiny tokenizer 一字一 id。`_tiny_prefix_ids` 默认 `limit=96`：超长 **raise**，不 `ids[:64]`。本轮不把产物里的 `prefix_truncated=false` 当充分证据（源码仍写死 `False`）。独立把夹具 `stage_b` 的 **被使用** 前缀垫到 70 / 97 字符，再间谍 hook。

垫前：`want=q`，`trace-base` 原 `start=14`。垫后：`start=70` / `97`，`prefix_n` 分别为 70 / 97。

**函数间谍（`cmd_intervene`，补丁 `models.collect.intervene_hidden_decode`）：**

| 检查 | 结果 |
|---|---|
| `_tiny_prefix_ids("x"*70)` | 长度 **70** |
| `_tiny_prefix_ids("x"*97)` | **`ValueError: tiny intervene prefix exceeds context; refuse truncated prefixes`** |
| `cmd_intervene` 70 字 | 返回 **0**；`status=prospective_decode` |
| hook 实参 `prompt_ids` 长度 | **`[70, 70, 70, 70]`**（四次：swap / crand / inlp / rescue） |
| 全部 `> 64` | **是** |
| 产物 `prefix_n` | **70** |
| 产物 `prefix_truncated` | `false`（单独不足以证明；与 hook 长度一致） |

**更深一层（补丁 `collect.decode_loop`，同一 70 字目录再跑）：** 8 次 decode（4 种 mode × hooked/baseline）的输入张量宽与返回 `prompt_ids` 长度均为 **70**。`resid_post_hook` 的 `transform` 只吃 `tensor[:, -1:]`，所以 transform 侧 seq=1 **不是** 截断到 64，是 last-token 切片。

**CLI：**

| 检查 | 结果 |
|---|---|
| `intervene --in-dir hunts/trunc/ok70` | **exit 0**；`prefix_n=70`；`prefix_truncated=false`；`status=prospective_decode` |
| `intervene --in-dir hunts/trunc/bad97` | **exit 1**；`failure.json` 同上 ValueError；**未写出** `interventions.jsonl` |

70 个 hook id 证明不再静默 `cap=64`。97 token 失败证明超限拒绝而不是截断后继续写干预。

### 3.10 T3 `hotpot` / `t3_musique` prepare

仓库自带夹具，用户 CLI，不经 pytest。独立打开写出的 `edits.jsonl`。

| 命令 | 退出码 | 产物 |
|---|---|---|
| `prepare --kind hotpot --fixture tests/fixtures/t3_hotpot_one.json` | **0** | `source=hotpotqa`，`tier=T3`，`edits.jsonl` **1** 行 `kind=document`；**无** `source_value_pair` |
| `prepare --kind t3_musique --fixture tests/fixtures/t3_musique_pair.json` | **0** | `source=musique`，`tier=T3`；`edits.jsonl` **1** 行 `kind=paragraph`；**无** pair |

`_try_source_value_pair` 对 `hotpotqa` / `musique` / `tier==T3` / `composition_reference` 返回 `None`。

**ID 观察（不否决 T3 exit 0）：** hotpot 编辑内嵌 task `task_id=hp-1::DocA`，但内嵌 `record_id` 仍为 `hp-1`；musique 内嵌 `task_id=msq-9::answerable::p0`，`record_id` 仍为 `msq-9::answerable`。

### 3.11 缺 `--in-dir` 失败

argparse 把 `--in-dir` 标成可选；运行期拒绝。均带 `--out-dir`。

| 子命令 | 退出码 | `failure.json` | 清单 |
|---|---|---|---|
| fit | **1** | `fit requires --in-dir` | `success=0` / `failure=1` |
| calibrate | **1** | `calibrate requires --in-dir` | 同上 |
| intervene | **1** | `intervene requires --in-dir` | 同上 |
| repair | **1** | `repair requires --in-dir` | 同上 |
| analyze | **1** | `analyze requires --in-dir` | 同上；**无** `report.json` |
| collect | **1** | `collect requires --in-dir` | 同上 |
| label | **1** | `label requires --in-dir with observations.jsonl` | 同上 |

文件当作 `--in-dir`：`analyze --in-dir tests/fixtures/t1_tiny.json` → **1**，`NotADirectoryError: --in-dir must be a directory`。

### 3.12 `ChildProcessExecutor.isolated_sandbox is False`；无 host exec

独立 import + 调用，不经 pytest。

| 检查 | 结果 |
|---|---|
| `ChildProcessExecutor.isolated_sandbox` | **`False`** |
| `IsolatedExecutor.isolated_sandbox` | `True` |
| `isinstance(ChildProcessExecutor(), IsolatedExecutor)` | **False** |
| MRO | `ChildProcessExecutor` → `object`；**无** 沙箱基类 |
| `SubprocessExecutor is ChildProcessExecutor` | True（别名） |
| `get_executor()` 默认 | `UnavailableExecutor`（`IsolatedExecutor` 子类），`isolated_sandbox=True` |
| `get_executor("child_process")` | `ChildProcessExecutor`，`isolated_sandbox=False` |
| `score_code("print(1)","assert True")` 默认 | `status=executor_unavailable`，`value=null`，`eligibility=false`，reason=`no isolated backend configured; host exec is forbidden` |
| 显式 child：`score_code("x=1","assert x==1", executor=child)` | `status=ok`，`value=1.0`（普通子进程，**不是**沙箱） |
| child `submit` 含 `exec(` / `eval(` | `status=rejected` |
| `forbid_host_exec` | `RuntimeError: host execution of model/dataset code is forbidden` |
| `src/` 生产路径 `exec(` / `eval(` | 仅 `executor.py` 把 `"exec("` / `"eval("` 当拒绝字符串，外加 `forbid_host_exec` 定义；**无** 内建 host `exec(` 调用。`repair.py` / `models/*.py` 的 `model.eval()` 是 PyTorch 评估模式。`t3_humaneval.py` 的 `load_humaneval` 是函数名，不是 `eval(` |

默认评分路径 **不会** 落到 ChildProcess。Child 必须 `get_executor("subprocess"|"child_process")` 才构造。这不是 host `exec` 回退。Linux cgroup 仍 `pending_server`。

### 3.13 Resume 不覆盖成功清单

`$E/hunts/resume/stage_a` 先成功：`success_count=1`，digest `cd379ff1456ab2e9b54e7a40ee72d49ce55aad8460404f5afc1b781c87faf866`。

| 动作 | 退出码 | 清单 |
|---|---|---|
| `prepare --resume`（配置一致） | **0** | digest **相同**；`manifest.json` `st_mtime_ns` **相同** → **未重写** |
| `prepare --resume --edit-value 99` | **1** | `resume run_spec mismatch: edit_value`；写出 `failure.json`；digest / `success_count=1` **未变** |
| collect tiny 成功后 `--resume` | **0** | digest 相同；mtime 未变 |
| collect `--resume --backend offline` | **1** | `resume run_spec mismatch: backend`；`failure.json` 存在；`success_count` 仍为 1，digest 仍为成功值 |

`main()` 异常路径：已有 `success_count` 或 `record_counts.success` 则 **不** `write_manifest` 覆盖。与实跑一致。

### 3.14 Plus 然后 Symbolic，两个顺序 CLI 进程

夹具家族 `original_id=gsm8k-12`。独立哈希：`sha256("0:gsm8k-12")` 单位区间 **0.9557** → 默认六段落在 **`test`**。因此默认 `--split-seed 0` 的孤立 Symbolic 不能区分“哈希到 test”与“被 Plus 锁强制 test”。本通道用 `--split-seed 6`（`sha256("6:gsm8k-12")=0.2820` → **`probe_train`**）作可证伪对照。

方法：快照并移走仓库锁文件 → 新进程孤立 Symbolic → 新进程 Plus（写盘）→ **再一个新进程** Symbolic。RAM 在进程边界清空；若第二枚 Symbolic 仍为 `test`，只能来自磁盘 JSON。

| 进程 | 命令 | 退出码 | 锁文件 | `splits.jsonl` role |
|---|---|---|---|---|
| 0（准备） | 移走已有 `gsm_test_only_families.json` | — | **不存在** | — |
| 1 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（无先验 Plus） | **0** | 仍不存在（Symbolic **不** `register`） | **`probe_train`** |
| 2 | `prepare --kind gsm_plus --fixture t2_gsmplus_one.json` | **0** | 写出 `["gsm8k-12", "q:ada has 4 apples…"]` | **`test`**（source 自身 test-only） |
| 3 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（新进程） | **0** | 仍为上列 JSON | **`test`** |

进程 1 与进程 3 仅差中间 Plus 落盘。这是跨进程持久化，不是同进程 RAM。测完后按字节恢复审查开始时的锁文件。`lock_restore_ok=true`。

孤立无锁可为 `probe_train`（seed 6 实跑）；被持久 JSON 锁住后必须为 `test`。从未加载过 Plus 的孤立 Symbolic 进 `probe_train` **不是** A10-04 残留。默认 seed 0 哈希到 `test` 是分数赋值，不是锁。

### 3.15 其它接线

| 项 | 证据 |
|---|---|
| JSON 拒 NaN | `encode({'x': nan})` → `ValueError`（`allow_nan=False`） |
| 拒 `latest` | `write_run_spec(..., config.model='latest')` → `config.model cannot use mutable identity 'latest'` |
| 产物无 `.tmp` | `$E.rglob('*.tmp')` 为空 |
| scientific 拒 offline H | §3.3 |

## 4. 命令表

前缀：`python -m reasoning_diff`。夹具 `F=tests/fixtures/t1_tiny.json`。`$E=.planning/audits/round-21/_e_scratch`。

| tag | argv（相对） | exit | 秒 | 关键产物 |
|---|---|---|---|---|
| help | `--help` | 0 | 0.231 | 八段子命令 |
| help_collect | `collect --help` | 0 | 0.227 | `--backend` `--shard` `--in-dir` |
| help_fit | `fit --help` | 0 | 0.218 | `--labels-dir` |
| help_calibrate | `calibrate --help` | 0 | 0.222 | `--features-dir` `--labels-dir` |
| help_prepare | `prepare --help` | 0 | 0.245 | `--sidecar` `--kind` |
| help_from_scratch | `--help`（cwd=`$E`） | 0 | 0.229 | 不依赖 cwd |
| help_no_pythonpath | `--help`（无 PYTHONPATH） | **1** | 0.056 | `No module named reasoning_diff` |
| fx_prepare | `prepare --fixture F --out-dir $E/fx/stage_a` | **0** | 0.441 | `tasks.jsonl` `edits.jsonl` `manifest.json` |
| fx_collect | `collect --fixture F --in-dir …/stage_a --out-dir …/stage_b --backend tiny` | **0** | 9.409 | `features.npz` **复制** tasks+edits |
| fx_label | `label --in-dir …/stage_a --out-dir …/stage_c` | **0** | 0.509 | `labels.jsonl` |
| fx_fit | `fit --in-dir …/stage_b --labels-dir …/stage_c --out-dir …/stage_d --split probe_train` | **0** | 0.488 | hashes 含 tasks+edits |
| fx_calibrate | `calibrate --in-dir …/stage_d --features-dir …/stage_b --out-dir …/stage_e --split calibration` | **0** | 0.496 | 有限 q |
| fx_intervene | `intervene --in-dir …/stage_b --out-dir …/stage_f` | **0** | 8.903 | `same_source_diff_value`；`prefix_truncated=false` |
| fx_repair | `repair --in-dir …/stage_a --out-dir …/stage_g --mask task_oracle` | **0** | 0.418 | `repair:fix-t1-001:task_oracle:k1` |
| fx_analyze | `analyze --in-dir …/stage_c --out-dir …/stage_h` | **0** | 0.422 | `report.json` 进清单 |
| fx_collect_offline | `collect … --backend offline --out-dir …/collect_off` | **0** | 0.414 | offline prefix |
| fx_collect_shard | `collect … --backend tiny --shard --out-dir …/collect_shard` | **0** | 8.329 | `traces-shard-000{0,1}.jsonl` |
| sc_prepare | `prepare --fixture F --out-dir …/sc/stage_a --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1` | **0** | 8.123 | 7 traces，`constrained_target` |
| sc_collect | `collect --fixture F --in-dir …/stage_a --out-dir …/stage_b --eval-mode scientific --backend tiny` | **0** | 8.507 | **tasks+edits 字节=stage_a** |
| sc_label | `label --in-dir …/stage_a --out-dir …/stage_c` | **0** | 0.420 | first-seen `p2` 然后 `p1` |
| sc_fit | `fit --in-dir …/stage_b --labels-dir …/stage_c --out-dir …/stage_d --split probe_train --eval-mode scientific` | **0** | 0.512 | §8 四行存在且 `refused_not_section8`、无 score |
| sc_calibrate | `calibrate --in-dir …/stage_d --features-dir …/stage_b --labels-dir …/stage_c --out-dir …/stage_e --split calibration --eval-mode scientific` | **0** | 0.419 | 4 problem scores，有限 q |
| sc_intervene | `intervene --in-dir …/stage_b --out-dir …/stage_f` | **0** | 7.712 | `same_value_diff_source` |
| sc_repair | `repair --in-dir …/stage_a --out-dir …/stage_g --mask task_oracle --eval-mode scientific --backend tiny` | **0** | 7.894 | k=1..5，`refilled_prefix=true` |
| sc_analyze | `analyze --in-dir …/stage_c --out-dir …/stage_h` | **0** | 0.403 | `p1=null`，gates unregistered |
| sc_collect_offline | `collect … --eval-mode scientific --backend offline --out-dir …/collect_off` | **1** | 0.252 | `refuses offline_prefix_ids as H` |
| pair_missing_intervene | `intervene --in-dir hunts/pair_missing_local/stage_b`（无本地 edits；兄弟 `prep` 有 pair） | **0** | 8.389 | `donor_kind=same_identity_fallback` |
| labels_sib_calibrate | `calibrate --in-dir labels_sib/probe --features-dir labels_sib/feat`（无 `--labels-dir`；兄弟 `lab`/`label`/`labels` 有 WRONG） | **0** | 0.413 | hashes 不含兄弟 labels |
| no_tasks_fit | `fit --in-dir no_tasks/col --labels-dir no_tasks/lab` | **1** | 0.232 | 兄弟 `prep` 不救命 |
| no_tasks_calibrate | `calibrate --in-dir probe_only --features-dir col --labels-dir lab` | **1** | 0.300 | `calibrate requires tasks.jsonl` |
| ancestor_fit | `fit --in-dir ancestor/deep/x/feat --labels-dir …/labs` | **1** | 0.246 | 祖先 `col` WRONG-TASK 不绑定 |
| ancestor_calibrate | `calibrate --in-dir probe_only --features-dir feat --labels-dir labs` | **1** | 0.250 | 同上 |
| trunc_ok70 | `intervene --in-dir hunts/trunc/ok70`（前缀 70 token） | **0** | 8.095 | hook `prompt_ids` 长 70；`prefix_n=70` |
| trunc_bad97 | `intervene --in-dir hunts/trunc/bad97`（前缀 97 token） | **1** | 2.022 | 拒绝截断；无 `interventions.jsonl` |
| prep_hotpot | `prepare --kind hotpot --fixture tests/fixtures/t3_hotpot_one.json` | **0** | 0.464 | document edit，无 pair |
| prep_t3_musique | `prepare --kind t3_musique --fixture tests/fixtures/t3_musique_pair.json` | **0** | 0.453 | paragraph edit，无 pair |
| miss_fit | `fit --out-dir …/miss/fit --split probe_train` | **1** | 0.240 | `fit requires --in-dir` |
| miss_calibrate | `calibrate --out-dir …/miss/cal --split calibration` | **1** | 0.240 | `calibrate requires --in-dir` |
| miss_intervene | `intervene --out-dir …/miss/int` | **1** | 0.247 | `intervene requires --in-dir` |
| miss_repair | `repair --out-dir …/miss/rep` | **1** | 0.236 | `repair requires --in-dir` |
| miss_analyze | `analyze --out-dir …/miss/an` | **1** | 0.245 | `analyze requires --in-dir`；无 `report.json` |
| miss_collect | `collect --fixture F --out-dir …/miss/col` | **1** | 0.240 | `collect requires --in-dir` |
| miss_label | `label --out-dir …/miss/lab` | **1** | 0.230 | 缺 observations.jsonl |
| file_indir_analyze | `analyze --in-dir F --out-dir …/miss/file_an` | **1** | 0.296 | `--in-dir must be a directory` |
| res_prepare | `prepare --fixture F --out-dir …/resume/stage_a` | **0** | 0.444 | 成功清单 |
| res_prepare_resume | 同上 `--resume` | **0** | 0.229 | digest/mtime 未变 |
| res_prepare_mismatch | 同上 `--resume --edit-value 99` | **1** | 0.247 | 成功清单保留 |
| res_collect | `collect … --backend tiny --out-dir …/resume/stage_b` | **0** | 7.843 | 成功清单 |
| res_collect_resume | 同上 `--resume` | **0** | 0.230 | digest 未变 |
| res_collect_backend_mismatch | `--resume --backend offline` | **1** | 0.223 | 成功清单保留 |
| a10_iso_symbolic_seed6 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（无锁） | **0** | 0.486 | `role=probe_train`；未写锁 |
| a10_plus | `prepare --kind gsm_plus --fixture t2_gsmplus_one.json` | **0** | 0.439 | `role=test`；写出家族 JSON |
| a10_symbolic_locked_seed6 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（新进程） | **0** | 0.432 | `role=test`（磁盘锁） |

共 53 条用户 CLI 调用。另有进程内 `cmd_calibrate` 两次（有/无兄 `lab`）与 `cmd_intervene` hook 间谍，不列入上表。

## 5. 必做项判定

| # | 要求 | 判定 | 证据 |
|---|---|---|---|
| 1 | 夹具八段 prepare→…→analyze | **PASS** | §3.2 八段 exit 0，清单自洽；目录 `stage_a`…`stage_h` |
| 2 | scientific tiny `--in-dir` 串联 | **PASS** | §3.3 八段 exit 0 |
| 3 | collect 复制 `tasks.jsonl` **和** `edits.jsonl` | **PASS** | §3.4 字节全等 + 进清单 |
| 4 | 无本地 tasks 则 fit/calibrate raise | **PASS** | §3.7 find=`None`；两处 fit/calibrate exit 1；无 probes |
| 5 | scientific `probes.jsonl` 四条 §8 行存在且为 `refused_not_section8`、无 score | **PASS** | §3.6 四行均在，键集仅 baseline/status/reason |
| 6 | `cmd_calibrate` 有/无兄 `lab` 输出相同；finder 不收兄路径 | **PASS** | §3.8 函数实跑；`calibration.jsonl` 字节全等；间谍 `*dirs` 只有 probe/feat；返回 `None` |
| 7 | 70 字 intervene 间谍 hook `prompt_ids` 长度 >64 | **PASS** | §3.9 hook 四次均为 70；decode 张量宽 70；97 token 拒绝且不写干预 |
| 8 | `ChildProcessExecutor.isolated_sandbox is False`；无 host exec | **PASS** | §3.12 |
| 9 | resume 保留成功；Plus 然后 Symbolic 新进程锁 `test` | **PASS** | §3.13 / §3.14 |
| 10 | T3 hotpot/musique prepare；缺 `--in-dir` 失败 | **PASS** | §3.10 / §3.11 |
| — | 冻结 hash 复算 | **PASS** | 开始 / 套件结束 / 落盘后再算均为声明值 |

### 残留观察（不否决上表）

- **T3/T4 编辑 `record_id`：** 编辑内嵌 task `task_id` 变了，`record_id` 仍是基任务。不阻止 prepare exit 0。
- **`--in-dir` argparse 非 required：** 运行期 `ValueError` 已足够失败。
- **默认 seed 0 的 `gsm8k-12` 哈希到 `test`：** 不能单独当跨进程锁证据。本通道用 seed 6 作可证伪对照。
- **锁文件是仓库全局路径：** 并行审查/实验会互相污染家族角色。这是工程形状，不是本轮 fail。本通道已快照/恢复。
- **混用 dtype：** tiny `H` float64。形状与有限性成立。
- **scientific 约束 `\nq=`：** 本机可解析接口，不是自然 CoT，不是 §4.1。
- **`prefix_truncated` 仍写死 `False`：** 本轮用 hook `prompt_ids` 长度锁定，不把该布尔当充分证据。
- **resid transform seq=1：** `resid_post_hook` 只把 last token 交给 transform。decode 输入宽 70，不是 64-cap。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 冻结 hash 复现 | 开始 / 套件结束 / 落盘后再算 **HASH_MATCH** §1 |
| 夹具 + scientific 八段可调度 | §3.2 / §3.3；独立目录名，不用 `prep` |
| collect 复制 tasks **和** edits | §3.4 |
| 缺本地 edits 不读兄弟 `prep`；donor 仅 fallback | §3.5 |
| `cmd_calibrate` 缺本地 labels 不读兄弟 `lab` | §3.8 函数间谍 + CLI |
| 给定目录无 `tasks.jsonl` 则 fit/calibrate raise | §3.7 |
| 祖先 `col` WRONG-TASK 不绑定 | §3.7 |
| scientific 写出四条 §8 拒绝行且不编造分 | §3.6 |
| 70 字 hook `prompt_ids` 为 70，不 `ids[:64]` | §3.9 |
| intervene 超长前缀拒绝 | §3.9 |
| T3 prepare 不再被 pair 打断 | §3.10 |
| 缺 `--in-dir` 七段失败 | §3.11 |
| Child 非沙箱；默认不可用；无 host exec | §3.12 |
| resume 不覆盖成功清单 | §3.13 |
| Plus 家族锁跨进程约束 Symbolic | §3.14 |
| 无 Plus 锁的孤立 Symbolic 可按哈希进 `probe_train` | §3.14 seed 6 |
| JSON 拒 NaN；拒 `latest` | §3.15 |
| 各成功 `manifest.digest` 自洽 | §3.2 / §3.3 |
| shard 完整 | §3.2 |
| `report.json` 进清单 | analyze `file_hashes` |
| 直接迁移维度拒绝 | 4096≠3584 |
| Week-8 未注册 | `unregistered` / `scientific_conclusion=null` |
| analyze 不编造 P1–P3 | 仅有 labels 时 `p1=null` |
| `git -C` revision | 产物仍 `46a6e26…` |
| scientific 拒 offline H | §3.3 |

Gate 0–2 未注册与 `scientific_conclusion=None` **不是** 缺陷。tiny 随机权重 **不是** MODEL-01。约束 `\nq = <digit>` 是本机可解析接口，不是自然 CoT。从未加载过 Plus 的孤立 Symbolic 进 `probe_train` **不是** A10-04 残留。

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux cgroup 隔离执行器、真实 HumanEval | `pending_server`；本机 subprocess 仅证明子进程路径 |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；tiny 为 `random_init` |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 注册 Gate 0–2 / 实测 P1–P3 | `unregistered` / `not_evaluated` |

## 8. 结论

审查开始、CLI 套件结束与本报告落盘后再算均为 **`HASH_MATCH`** `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb`（61 文件）。全部 `python -m` 证据绑定该快照。本通道未改生产代码。

相对用户指定的独立复跑：夹具八段、scientific tiny 串联、collect 复制 `tasks.jsonl` **与** `edits.jsonl`、无本地 tasks 则 fit/calibrate raise、scientific `probes.jsonl` 四条 §8 行存在且为 `refused_not_section8` 且无 score、**`cmd_calibrate` 有/无兄 `lab` 输出相同且 finder 不收兄路径**、**70 字 intervene hook `prompt_ids` 长度为 70（>64）**、`ChildProcessExecutor.isolated_sandbox is False` 且无 host exec、resume 保留成功、Plus 然后 Symbolic 新进程锁 `test`、T3 hotpot/musique prepare、缺 `--in-dir` 失败——**全部成立**。

这只证明用户 CLI 在 tiny/fixture 上可调度且 fail-closed 行为与声明一致。**不是** OPS-01，**不是** 真实模型上的论文正确性。

**本通道：`PASS`（`HASH_MATCH`）。**
