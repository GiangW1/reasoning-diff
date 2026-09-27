# E：端到端工程审查（round-15）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮其它通道报告。`ISSUES.md` 仅作作者声称，不采信关闭声明。

夹具烟测与 scientific tiny **不是** 科学全跑，也 **不是** OPS-01 / MODEL-01。本通道不把 `exit 0`、清单存在或 `report.json` 写成论文正确性。

**冻结核验：审查开始与 CLI 套件结束均为 `HASH_MATCH`。本报告落盘后再算为 `HASH_MISMATCH`。按本轮指令：`HASH_MISMATCH` → 本通道 `FAIL`。** 本通道未改 `src/`、`tests/`、`pyproject.toml`。漂移来自并行改冻结集（见 §1）。命令表绑定套件期间与声明值一致的快照。A10-04 期间快照并移走仓库锁文件 `.planning/research/.cache/gsm_test_only_families.json`（不在冻结集），测完按字节恢复。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 02:45–03:05 +08:00 |
| 声称冻结 hash | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（用户给定；与 `.planning/audits/round-15/VERSION.md` 原文一致；61 文件） |
| 独立复算（审查开始 / 实跑所绑定） | **`HASH_MATCH`**。按 VERSION 原文脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**61** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`。当时 `cli.py` **1252** 行 / **61010** 字节；`models/generate.py` **201** 行 / **7712** 字节；`models/tiny.py` **120** 行 / **3508** 字节；`tests/test_round07_regressions.py` **296** 行 / **13855** 字节。 |
| 独立复算（CLI 套件结束） | **`HASH_MATCH`**。同一脚本仍 61 文件，同一摘要。 |
| 独立复算（本报告落盘后再算） | **`HASH_MISMATCH`**。仍 61 文件，得到 `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`。相对开审：`models/generate.py` 变为 **200** 行 / **7750** 字节；`models/tiny.py` 仍 120 行但变为 **3510** 字节；`tests/test_round07_regressions.py` 变为 **302** 行 / **14207** 字节。`cli.py` 行数/大小仍 1252/61010。本通道 **未** 写这些文件。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（`io.runtime_info` 用 `git -C <repo_root>`；产物 `environment.repo_root=C:\Users\22688\Desktop\diff`） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`，本机 `torch 2.7.1+cpu` 供 tiny） |
| 审查范围 | 用户指定：夹具八段；scientific tiny 串联；collect 复制 `tasks.jsonl`；给定目录无图则 fit raise；祖先 `col` WRONG-TASK 不绑定（A12-03）；T3 hotpot/musique exit 0；缺 `--in-dir`；`ChildProcessExecutor.isolated_sandbox is False`；resume 不覆盖成功；Plus 然后 Symbolic 新进程锁 `test` |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md`、`executor.py`、`scoring.py`；A12-03 / A10-04 另读 `splits.py`、`tasks/t2_gsm_plus.py`、`tasks/t2_gsm_symbolic.py` |
| 实跑入口 | `python -m reasoning_diff`；产物根 `%TEMP%\rd-e-r15-k8n4q2\`（下文 `$E`），未写入 `src/` / `tests/` / `pyproject.toml` |
| pytest | 作者声称 159 passed。本通道 **未** 把 pytest 当作验收，也未重跑测试套件。 |

## 2. 逐文件覆盖

行号为 **本轮冻结快照**（`cli.py` 1252）。

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–1252 | 通读 + `python -m` 夹具八段 + scientific tiny + 无图 fit + A12-03 + T3 + 缺 in-dir + resume | 八段可调度；collect 复制 `tasks.jsonl`；`_find_tasks_jsonl` 只看传入目录自己的文件；无图则 raise；祖先 `col` 不绑定；T3 prepare 不被 pair 打断；缺 in-dir 失败；resume 不覆盖成功清单 |
| `src/reasoning_diff/artifacts.py` | 1–85 | digest / `success_count` / shard | 各成功阶段 digest 自洽；失败清单 `success=0`；两枚 shard 进清单 |
| `src/reasoning_diff/io.py` | 1–133 | NPZ/NaN/`runtime_info` | JSON `allow_nan=False`；`encode(nan)` 抛 `ValueError`；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–27 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机 `shutil.which` = null |
| `docs/SERVER_RUNBOOK.md` | 1–51 | 对照实跑 | 八段顺序与 `--features-dir` / resume / scientific 拒 offline H 与实跑一致；隔离仍 `pending_server` |
| `src/reasoning_diff/executor.py` | 1–109 | 类属性 + `get_executor` + `score_code` | 默认 `UnavailableExecutor`；`ChildProcessExecutor.isolated_sandbox=False`；与 `IsolatedExecutor` 无继承；拒 `exec(`/`eval(` 字面量；无 host `exec(` 调用 |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code` 默认后端 | 默认 `executor_unavailable`，`eligibility=false`；文案含 `host exec is forbidden` |
| `src/reasoning_diff/schema.py` | 1–385 | 产物 `from_dict` / `record_id` | Event `record_id` 含 run + identity；T1 编辑任务重写 `record_id`；T3 编辑行保留基任务 `record_id`（§5 观察） |
| `src/reasoning_diff/splits.py` | 1–184 | CLI `require_split` + A10-04 两进程 | 锁写入 `.planning/research/.cache/gsm_test_only_families.json`；`family_locked_test` 并集磁盘；新进程 Symbolic 读到 `test` |
| `src/reasoning_diff/edits.py` | 1–362 | prepare pair / 域编辑 | `_try_source_value_pair` 跳过 T3 / placeholder / paragraph / `composition_reference` |
| `src/reasoning_diff/events.py` | 1–274 | prepare 解析 | 夹具 `parse_fixture_events`；scientific `parse_events` + 约束生成 |
| `src/reasoning_diff/graphs.py` | 1–46 | `ancestors` | calibrate RSI 用图祖先 |
| `src/reasoning_diff/measure.py` | `build_labels` | label / prepare | 无 observation 则无任务/行为标签 |
| `src/reasoning_diff/models/collect.py` | 1–261 | tiny collect | scientific `H` 全有限 |
| `src/reasoning_diff/models/generate.py` | 1–201 | scientific prepare | 约束追加 `\nq = <digits>`；`parse_status=constrained_target` |
| `src/reasoning_diff/models/features.py` | 1–39 | collect prefix | 与 event_rows 对齐 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | collect 重分词 | `encode_text` 按字符 `ord` |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `fit` | 掩码未知行；scientific task 头写出有限 `U`/`V`/`b` |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `conformal_threshold` | 夹具/scientific 均为有限 `q` |
| `src/reasoning_diff/interventions.py` | 1–115 | `intervene` | CLI `_expressible_donor`；tiny 走到 `prospective_decode` |
| `src/reasoning_diff/repair.py` | 1–232 | `repair` | fixture offline → `prefill_unavailable`；scientific tiny `k=1..5` 且 `refilled_prefix=true` |
| `src/reasoning_diff/analysis.py` | 1–337 | `analyze` | 无 `p1_table` → `p1=null` / `not_evaluated`；不从标签冒充 length/op/rho |
| `src/reasoning_diff/transfer.py` | 1–86 | `direct_transfer(4096,3584)` | `not_applicable_dimension_mismatch` |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | `--kind` | `t3_musique` / `hotpot` 别名接通 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–84 | `--kind gsm_plus` | `register_test_only_family` 落盘；role=`test` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–85 | `--kind` + `--sidecar` | **不**自行登记锁；读磁盘锁后可为 `test` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 1–104 | `--kind hotpot` | `document` 编辑；CLI 不再强制 pair |
| `src/reasoning_diff/tasks/t3_musique.py` | 1–110 | `--kind t3_musique` | `expression=composition_reference`；pair 被跳过 |
| `src/reasoning_diff/rng.py` | 1–53 | intervene `StreamBank` | CLI intervene 使用 |
| `src/reasoning_diff/baselines.py` | 1–125 | CLI `fit` | verbalizer / attention_* |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | CLI fit | `baseline=boundary_mlp` |
| `tests/test_cli_pipeline.py` | — | 读，未当作验收 | 绿测不是 OPS-01 |

**抽样未做完整工程审查：** `models/tiny.py`、`models/adapters.py`、T1 official 内部、`t2_noop.py`。adapters **未被** 八段通用子命令调用。

## 3. 已执行检查与结果

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。产物 `$E=%TEMP%\rd-e-r15-k8n4q2`。夹具 `tests/fixtures/t1_tiny.json`。

### 3.1 用户 CLI 入口

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| 同上（cwd=`$E`，仍带 `PYTHONPATH=src`） | **0** | 入口不依赖进程 cwd |
| 同上（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（`shutil.which` = null） |
| `collect --help` | **0** | `--backend {tiny,offline}`、`--shard`、`--kind`、`--eval-mode`、`--in-dir`、`--weight-seed` |
| `calibrate --help` | **0** | `--features-dir` **与** `--labels-dir`；`--in-dir` 在 argparse 层 **不是** `required`（运行期拒绝，见 §3.6） |
| `fit --help` | **0** | `--labels-dir`；`--in-dir` 同样非 argparse required |
| `prepare --help` | **0** | `--sidecar`、`--kind`、`--split-fractions` |

`__main__.py` 转调 `main`。runbook 的 `python -m` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 夹具烟测（runbook 顺序；collect=**tiny**）

目录：`$E\fx\`。

| 阶段 | 退出码 | 清单 | 关键产物 |
|---|---|---|---|
| prepare | **0** | digest 自洽，`success_count=1` | `tasks.jsonl` 2 行；`edits.jsonl` 含 `value` + `source_value_pair`；默认 `p2→2` |
| collect tiny | **0** | 含 `tasks.jsonl`、`features.npz`、`event_rows.jsonl` | `H` `[2,32]` 全有限；`weight_source=random_init` |
| label | **0** | `labels.jsonl` | 消费 prepare `observations.jsonl` |
| fit `--split probe_train` | **0** | `probes.jsonl` | `input_hashes` 含 `collect/tasks.jsonl` **与** `label/labels.jsonl` |
| calibrate `--features-dir collect` | **0** | `calibration.jsonl` | `scores≈[0.00502331, 0.00502337]`，`q=0.00502337`，`status=finite`，`unit=problem` |
| intervene | **0** | `interventions.jsonl` | `status=prospective_decode`，`timing=offline_hidden`；`relative.donor_kind=same_source_diff_value`，`donor_rows=[0,1]` |
| repair `--mask task_oracle` | **0** | `repairs.jsonl` | `record_id=repair:fix-t1-001:task_oracle:k1`；默认 backend=offline → `prefill_unavailable` |
| analyze | **0** | `report.json` 进清单 | `p1=p2=p3=null`，`status=not_evaluated`，`scientific_conclusion=null` |
| collect `--backend offline` | **0** | 另目录 | `H` `[1,8]` |
| collect `--shard` | **0** | 两枚 shard 进清单 | `traces-shard-0000.jsonl` / `0001.jsonl` 各 1 行 |

**接线：** 每阶段 `run_spec.config.command` 分别为 `prepare` / `collect` / `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze`。各成功 `manifest.digest` 独立重算均为 True。

`analyze` `transfer`：`source_dim=4096`，`target_dim=3584`，`status=not_applicable_dimension_mismatch`。Week-8：`gate0/1/2.decision=unregistered`，`skip_p2_p3=true`。

### 3.3 scientific tiny 八段与 collect 复制 `tasks.jsonl`

runbook 本地 scientific：`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1`。目录：`$E\sc\`。

| 阶段 | 退出码 | 要点 |
|---|---|---|
| prepare | **0** | `n_traces=7`：base / t0p / edit / source / 两枚 extra edit / sham；皆 `parse_status=constrained_target` |
| collect `--backend tiny` | **0** | **写出 `s-col/tasks.jsonl`**；`H` `[7,32]` 全有限；`event_rows` 7 行，皆 `node_id=q` |
| label | **0** | first-seen premise 顺序 **`p2`, `p1`**（再 `sham:q`） |
| fit | **0** | `input_hashes` 含 `s-col/tasks.jsonl` |
| calibrate | **0** | 4 个 problem unit，`q=0.00502359`，`status=finite` |
| intervene | **0** | `prospective_decode` / `offline_hidden` |
| repair `--backend tiny --eval-mode scientific` | **0** | `k=1..5`，皆 `status=ok`，`refilled_prefix=true` |
| analyze | **0** | 同样 `p1=null` / `not_evaluated` / `scientific_conclusion=null` |
| collect `--backend offline` + scientific | **1** | `scientific collect refuses offline_prefix_ids as H`；**无** `features.npz` |

**collect 复制 `tasks.jsonl`（独立确认，不信作者表）：**

- `$E\fx\collect\tasks.jsonl` 与 `$E\sc\s-col\tasks.jsonl` **均存在**，进入各自 collect `manifest.file_hashes`。
- 与对应 prepare 目录 **字节全等**。SHA-256 均为 `a6ca1a4d4f5ef4c950be39da00864229159b9edb9b74bd93fb6af367f1194eb7`。
- 前提顺序 `["p1","p2"]`。

**fit 用该文件，而不是 labels first-seen 顺序（独立确认）：**

1. 实跑 labels first-seen（跳过 `sham:`）：**`p2`, `p1`**。
2. `_find_tasks_jsonl(s-col, s-lab)` 返回 **`s-col\tasks.jsonl`**。
3. `_e_premise_ids(task_from_that_file, labels)` = **`["p1","p2"]`**。
4. `_e_premise_ids(None, labels)` = **`["p2","p1"]`**（纯 first-seen）。两者 **不相等**。
5. scientific fit 的 `input_hashes` 含 `s-col/tasks.jsonl`。

scientific 事件仍是约束 `\nq = <digit>`，**不是** §4.1 自然 CoT。tiny `random_init` **不是** MODEL-01。

### 3.4 给定目录无 `tasks.jsonl` 则 fit raise

把夹具 collect/label 复制到 `$E\c6\without\`，删除 `col/tasks.jsonl`，**保留兄弟** `without/prep/tasks.jsonl`。给定目录是 `col` 与 `lab`。

`_find_tasks_jsonl(col, lab)` 独立 import 为 **`None`**（兄弟 `prep` 不在查找范围）。

| 命令 | 退出码 | `failure.json` |
|---|---|---|
| `fit --in-dir c6/with/col --labels-dir c6/with/lab`（保留 tasks） | **0** | —；find → `col/tasks.jsonl` |
| `fit --in-dir c6/without/col --labels-dir c6/without/lab` | **1** | `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order`；清单 `success=0`，只哈希 `failure.json` |
| `calibrate --in-dir c6/without/probe_only --features-dir col --labels-dir lab`（`probes.jsonl` 在，三目录均无 tasks） | **1** | `ValueError: calibrate requires tasks.jsonl so E columns follow task.premises, not label order` |

无图路径 **不会** 静默退回 first-seen，也 **不会** 因兄弟名叫 `prep` 而救命。这是用户 CLI 实跑，不是作者表。

**第一次 calibrate 对照（不作为本条否决）：** `--in-dir` 指向空的 `fit_in`（无 `probes.jsonl`）时，fixture 模式在碰到 `tasks.jsonl` 门槛之前就写成 `probe_weights_or_features_missing` 并 **exit 0**。上表第三行补了 probes 后再测，才走到 raise。

### 3.5 A12-03：祖先 `col` WRONG-TASK 不绑定

布局：`$E\a12\bind\col\tasks.jsonl` 写成 `task_id=WRONG-TASK`，前提序对调为 `[p2,p1]`；特征在 `bind/deep/x/feat`，标签在 `bind/deep/x/labs`。feat/labs **没有** `tasks.jsonl`。

| 检查 | 结果 |
|---|---|
| 祖先 `col/tasks.jsonl` 存在 | 是；`task_id=WRONG-TASK` |
| `_find_tasks_jsonl(feat, labs)` | **`None`** |
| `_find_tasks_jsonl(col)` | 命中该 WRONG-TASK 文件（只因 `col` 本身被传入） |
| `_e_premise_ids(real, labels)` | `["p1","p2"]` |
| `_e_premise_ids(WRONG-TASK, labels)` | `["p2","p1"]`（不相等） |
| `fit --in-dir feat --labels-dir labs` | **exit 1**；`fit requires tasks.jsonl so E columns follow task.premises, not label order` |
| `probes.jsonl` | **未写出** |

旧 4 层 + extras 搜索会绑到祖先 `col` 并把 \(E\) 列换成错题 `[p2,p1]`。本冻结只读传入目录自己的 `tasks.jsonl`，祖先 WRONG-TASK **不绑定**。

### 3.6 T3 `hotpot` / `t3_musique` prepare exit 0

仓库自带夹具，用户 CLI，不经 pytest。

| 命令 | 退出码 | 产物 |
|---|---|---|
| `prepare --kind hotpot --fixture tests/fixtures/t3_hotpot_one.json` | **0** | `source=hotpotqa`，`tier=T3`，`edits.jsonl` **1** 行 `kind=document`；**无** `source_value_pair` |
| `prepare --kind t3_musique --fixture tests/fixtures/t3_musique_pair.json` | **0** | `source=musique`，`tier=T3`，节点 `expression=composition_reference`；`edits.jsonl` **1** 行 `kind=paragraph`；**无** pair |

`_try_source_value_pair` 对 `hotpotqa` / `musique` / `tier==T3` / `composition_reference` 返回 `None`，因此域编辑成功后不再 `recompute` 算术 pair。

**ID 观察（不否决 T3 exit 0）：** hotpot 编辑行 `task_id=hp-1::DocA` 但 `record_id` 仍为 `hp-1`；musique `msq-9::answerable::p0` 的 `record_id` 仍为 `msq-9::answerable`。

### 3.7 缺 `--in-dir` 必须失败

argparse 把 `--in-dir` 标成可选；运行期拒绝。均带 `--out-dir`。

| 子命令 | 退出码 | `failure.json` | 清单 |
|---|---|---|---|
| fit | **1** | `fit requires --in-dir` | `success=0` / `failure=1`，只哈希 `failure.json` |
| calibrate | **1** | `calibrate requires --in-dir` | 同上 |
| intervene | **1** | `intervene requires --in-dir` | 同上 |
| repair | **1** | `repair requires --in-dir` | 同上 |
| analyze | **1** | `analyze requires --in-dir` | 同上；**无** `report.json` |
| collect（额外） | **1** | `collect requires --in-dir` | 同上 |
| label（额外） | **1** | `label requires --in-dir with observations.jsonl` | 同上 |

文件当作 `--in-dir`：`analyze --in-dir tests/fixtures/t1_tiny.json` → **1**，`NotADirectoryError: --in-dir must be a directory`。

### 3.8 `ChildProcessExecutor.isolated_sandbox is False`

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
| `src/` 生产路径 `exec(` | 仅 `executor.py` 把 `"exec("` / `"eval("` 当拒绝字符串；**无** 内建 host `exec(` 调用。`repair.py` 的 `model.eval()` 是 PyTorch 评估模式，不是 `eval(` |

默认评分路径 **不会** 落到 ChildProcess。Child 必须 `get_executor("subprocess"|"child_process")` 才构造。这不是 host `exec` 回退。Linux cgroup 仍 `pending_server`。

### 3.9 Resume 不覆盖成功清单

`$E\resume\prepare` 先成功：`success_count=1`，digest `1b41b2e39dcf9ee7b492577581c168e9c1e4394a4145e75ea757a1dfe367ffb6`。

| 动作 | 退出码 | 清单 |
|---|---|---|
| `prepare --resume`（配置一致） | **0** | digest **相同**；`manifest.json` `st_mtime_ns` **相同** → **未重写** |
| `prepare --resume --edit-value 99` | **1** | `resume run_spec mismatch: edit_value`；写出 `failure.json`；digest / `file_hashes` / `success_count=1` **未变** |
| collect tiny 成功后 `--resume` | **0** | digest `36e9764a…` 相同；mtime 未变 |
| collect `--resume --backend offline` | **1** | `resume run_spec mismatch: backend`；`failure.json` 存在；`success_count` 仍为 1，digest 仍为成功值 |

`main()` 异常路径：已有 `success_count` 或 `record_counts.success` 则 **不** `write_manifest` 覆盖。与实跑一致。

### 3.10 Plus 然后 Symbolic，两个顺序 CLI 进程

夹具家族 `original_id=gsm8k-12`。独立哈希：`sha256("0:gsm8k-12")` 的单位区间值 `0.9557`，默认六段分数下落在 **`test`**。因此 **默认 `--split-seed 0` 的孤立 Symbolic 不能区分“哈希到 test”与“被 Plus 锁强制 test”**。本通道另选 `--split-seed 6`（`sha256("6:gsm8k-12")=0.2820` → **`probe_train`**）作可证伪对照。

方法：快照并移走仓库锁文件 → 新进程孤立 Symbolic → 新进程 Plus（写盘）→ **再一个新进程** Symbolic。RAM 在进程边界清空；若第二枚 Symbolic 仍为 `test`，只能来自磁盘 JSON。

| 进程 | 命令 | 退出码 | 锁文件 | `splits.jsonl` role |
|---|---|---|---|---|
| 0（准备） | 移走已有 `gsm_test_only_families.json` | — | **不存在** | — |
| 1 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（无先验 Plus） | **0** | 仍不存在（Symbolic **不** `register`） | **`probe_train`** |
| 2 | `prepare --kind gsm_plus --fixture t2_gsmplus_one.json` | **0** | 写出 `["gsm8k-12", "q:ada has 4 apples…"]` | **`test`**（source 自身 test-only） |
| 3 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（新进程） | **0** | 仍为上列 JSON | **`test`** |

进程 1 与进程 3 的 `run_spec.config.role` 分别为 `probe_train` / `test`，`rng.split_seed` 均为 6。同一家族、同一分数、仅差中间 Plus 落盘。这是跨进程持久化，不是同进程 RAM。

测完后按字节恢复审查开始时的锁文件。`lock_restore_ok=true`。

孤立无锁可为 `probe_train`（seed 6 实跑）；被持久 JSON 锁住后必须为 `test`。从未加载过 Plus 的孤立 Symbolic 进 `probe_train` **不是** A10-04 残留。默认 seed 0 哈希到 `test` 是分数赋值，不是锁。

### 3.11 其它接线

| 项 | 证据 |
|---|---|
| JSON 拒 NaN | `encode({'x': nan})` → `ValueError`（`allow_nan=False`） |
| 拒 `latest` | `write_run_spec(..., config.model='latest')` → `config.model cannot use mutable identity 'latest'` |
| 产物无 `.tmp` | `$E.rglob('*.tmp')` 为空 |
| scientific 拒 offline H | §3.3 |

## 4. 命令表

前缀：`python -m reasoning_diff`。夹具 `F=tests/fixtures/t1_tiny.json`。`$E=%TEMP%\rd-e-r15-k8n4q2`。

| tag | argv（相对） | exit | 秒 | 关键产物 |
|---|---|---|---|---|
| help | `--help` | 0 | 0.37 | 八段子命令 |
| help_collect | `collect --help` | 0 | 0.23 | `--backend` `--shard` `--in-dir` |
| help_fit | `fit --help` | 0 | 0.25 | `--labels-dir` |
| help_calibrate | `calibrate --help` | 0 | 0.23 | `--features-dir` `--labels-dir` |
| help_prepare | `prepare --help` | 0 | 0.23 | `--sidecar` `--kind` |
| help_from_temp | `--help`（cwd=`$E`） | 0 | 0.24 | 不依赖 cwd |
| help_no_pythonpath | `--help`（无 PYTHONPATH） | **1** | 0.05 | `No module named reasoning_diff` |
| fx_prepare | `prepare --fixture F --out-dir $E/fx/prepare` | **0** | 0.43 | `tasks.jsonl` `manifest.json` |
| fx_collect | `collect --fixture F --in-dir …/prepare --out-dir …/collect --backend tiny` | **0** | 10.04 | `features.npz` `tasks.jsonl` `event_rows.jsonl` |
| fx_label | `label --in-dir …/prepare --out-dir …/label` | **0** | 0.42 | `labels.jsonl` |
| fx_fit | `fit --in-dir …/collect --labels-dir …/label --out-dir …/fit --split probe_train` | **0** | 0.43 | `probes.jsonl`；hashes 含 collect/tasks |
| fx_calibrate | `calibrate --in-dir …/fit --features-dir …/collect --out-dir …/cal --split calibration` | **0** | 0.42 | `calibration.jsonl` 有限 q |
| fx_intervene | `intervene --in-dir …/collect --out-dir …/intervene` | **0** | 8.43 | `prospective_decode` |
| fx_repair | `repair --in-dir …/prepare --out-dir …/repair --mask task_oracle` | **0** | 0.41 | `repair:fix-t1-001:task_oracle:k1` |
| fx_analyze | `analyze --in-dir …/label --out-dir …/analyze` | **0** | 0.40 | `report.json` 进清单 |
| fx_collect_offline | `collect … --backend offline --out-dir …/collect_off` | **0** | 0.42 | `H[1,8]` |
| fx_collect_shard | `collect … --backend tiny --shard --out-dir …/collect_shard` | **0** | 7.93 | `traces-shard-000{0,1}.jsonl` |
| sc_prepare | `prepare --fixture F --out-dir …/s-prep --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15 --sham-opportunities 1` | **0** | 8.05 | 7 traces，`constrained_target` |
| sc_collect | `collect --fixture F --in-dir …/s-prep --out-dir …/s-col --eval-mode scientific --backend tiny` | **0** | 7.86 | **`s-col/tasks.jsonl` 字节=prepare** |
| sc_label | `label --in-dir …/s-prep --out-dir …/s-lab` | **0** | 0.40 | first-seen `p2` 然后 `p1` |
| sc_fit | `fit --in-dir …/s-col --labels-dir …/s-lab --out-dir …/s-fit --split probe_train` | **0** | 0.42 | E 列序 `p1,p2`（非 first-seen） |
| sc_calibrate | `calibrate --in-dir …/s-fit --features-dir …/s-col --labels-dir …/s-lab --out-dir …/s-cal --split calibration` | **0** | 0.42 | 4 problem scores，有限 q |
| sc_intervene | `intervene --in-dir …/s-col --out-dir …/s-int` | **0** | 8.21 | `prospective_decode` |
| sc_repair | `repair --in-dir …/s-prep --out-dir …/s-rep --mask task_oracle --eval-mode scientific --backend tiny` | **0** | 8.86 | k=1..5，`refilled_prefix=true` |
| sc_analyze | `analyze --in-dir …/s-lab --out-dir …/s-an` | **0** | 0.40 | `p1=null`，gates unregistered |
| sc_collect_offline | `collect … --eval-mode scientific --backend offline --out-dir …/s-col-off` | **1** | 0.24 | `refuses offline_prefix_ids as H` |
| c6_fit_with | `fit --in-dir c6/with/col --labels-dir c6/with/lab` | **0** | 0.43 | find → col/tasks.jsonl |
| c6_fit_without | `fit --in-dir c6/without/col --labels-dir c6/without/lab` | **1** | 0.25 | 给定目录无图；兄弟 `prep` 不救命 |
| c6_cal_probes | `calibrate --in-dir c6/without/probe_only --features-dir col --labels-dir lab` | **1** | 0.27 | `calibrate requires tasks.jsonl` |
| a12_fit | `fit --in-dir bind/deep/x/feat --labels-dir bind/deep/x/labs` | **1** | 0.24 | 祖先 `col` WRONG-TASK 不绑定 |
| prep_hotpot | `prepare --kind hotpot --fixture tests/fixtures/t3_hotpot_one.json` | **0** | 0.43 | document edit，无 pair |
| prep_t3_musique | `prepare --kind t3_musique --fixture tests/fixtures/t3_musique_pair.json` | **0** | 0.43 | paragraph edit，无 pair |
| miss_fit | `fit --out-dir …/miss/fit --split probe_train` | **1** | 0.23 | `fit requires --in-dir` |
| miss_calibrate | `calibrate --out-dir …/miss/cal --split calibration` | **1** | 0.23 | `calibrate requires --in-dir` |
| miss_intervene | `intervene --out-dir …/miss/int` | **1** | 0.24 | `intervene requires --in-dir` |
| miss_repair | `repair --out-dir …/miss/rep` | **1** | 0.23 | `repair requires --in-dir` |
| miss_analyze | `analyze --out-dir …/miss/an` | **1** | 0.23 | `analyze requires --in-dir`；无 `report.json` |
| miss_collect | `collect --fixture F --out-dir …/miss/col` | **1** | 0.23 | `collect requires --in-dir` |
| miss_label | `label --out-dir …/miss/lab` | **1** | 0.23 | 缺 observations.jsonl |
| file_indir_analyze | `analyze --in-dir F --out-dir …/miss/file_an` | **1** | 0.24 | `--in-dir must be a directory` |
| res_prepare | `prepare --fixture F --out-dir …/resume/prepare` | **0** | 0.46 | 成功清单 |
| res_prepare_resume | 同上 `--resume` | **0** | 0.25 | digest/mtime 未变 |
| res_prepare_mismatch | 同上 `--resume --edit-value 99` | **1** | 0.24 | 成功清单保留 |
| res_collect | `collect … --backend tiny --out-dir …/resume/collect` | **0** | 8.62 | 成功清单 |
| res_collect_resume | 同上 `--resume` | **0** | 0.29 | digest 未变 |
| res_collect_backend_mismatch | `--resume --backend offline` | **1** | 0.27 | 成功清单保留 |
| a10_iso_symbolic_seed6 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（无锁） | **0** | 0.56 | `role=probe_train`；未写锁 |
| a10_plus_proc1 | `prepare --kind gsm_plus --fixture t2_gsmplus_one.json` | **0** | 0.53 | `role=test`；写出家族 JSON |
| a10_symbolic_proc2_seed6 | `prepare --kind gsm_symbolic --sidecar … --split-seed 6`（新进程） | **0** | 0.48 | `role=test`（磁盘锁） |

共 50 条用户 CLI 调用（含补测 `c6_cal_probes`）。进程内执行器 / JSON / `latest` 检查不列入上表。

## 5. 必做项判定

| # | 要求 | 判定 | 证据 |
|---|---|---|---|
| 1 | 夹具八段 prepare→…→analyze | **PASS** | §3.2 八段 exit 0，清单自洽 |
| 2 | scientific tiny `--in-dir` 串联 | **PASS** | §3.3 八段 exit 0 |
| 3 | collect 复制 `tasks.jsonl` | **PASS** | §3.3 字节全等 + 进清单 + HASH `a6ca1a4d…` |
| 4 | 给定目录无 `tasks.jsonl` 则 fit raise | **PASS** | §3.4 兄弟 `prep` 仍 exit 1 |
| 5 | 祖先 `col` WRONG-TASK 不绑定（A12-03） | **PASS** | §3.5 find=`None`；fit exit 1；无 probes |
| 6 | T3 `hotpot` / `t3_musique` exit 0 | **PASS** | §3.6 |
| 7 | 缺 `--in-dir` 失败 | **PASS** | §3.7 七段皆 exit 1 |
| 8 | `ChildProcessExecutor.isolated_sandbox is False` | **PASS** | §3.8 |
| 9 | resume 不覆盖成功清单 | **PASS** | §3.9 digest/mtime 不变；mismatch 只加 `failure.json` |
| 10 | Plus 然后 Symbolic 新进程锁 `test` | **PASS** | §3.10 seed 6：孤立 `probe_train`，进程 3 `test` |
| — | 冻结 hash 复算 | **FAIL** | 开始与套件结束 `HASH_MATCH`；落盘后再算 `5413a4bc…` ≠ 声明值 |

### 残留观察（不否决上表）

- **T3/T4 编辑 `record_id`：** 编辑行 `task_id` 变了，`record_id` 仍是基任务。不阻止 prepare exit 0。
- **`--in-dir` argparse 非 required：** 运行期 `ValueError` 已足够失败。
- **默认 seed 0 的 `gsm8k-12` 哈希到 `test`：** 不能单独当跨进程锁证据。本通道用 seed 6 作可证伪对照。
- **锁文件是仓库全局路径：** 并行审查/实验会互相污染家族角色。这是工程形状，不是本轮 fail。本通道已快照/恢复。
- **无 probes 的 fixture calibrate：** 缺 `tasks.jsonl` 之前就写成 missing 并 exit 0。有 probes 后才 raise。用户指定的是 **fit** raise，该项已独立成立。
- **冻结漂移：** 落盘后再算 `HASH_MISMATCH`。本通道未改生产文件。连续通过计数 **不能** 把写报告后的树标成 `401e509b…`。
- **混用 dtype：** tiny `H` float64。形状与有限性成立。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 套件期间冻结 hash 复现 | 开始 / 套件结束 **HASH_MATCH** §1；落盘后漂移见 §8 |
| 夹具 + scientific 八段可调度 | §3.2 / §3.3 |
| collect 复制 tasks；fit 按前提列序 | §3.3 |
| 给定目录无 `tasks.jsonl` 则 fit/calibrate raise | §3.4 |
| 祖先 `col` WRONG-TASK 不绑定 | §3.5 |
| T3 prepare 不再被 pair 打断 | §3.6 |
| 缺 `--in-dir` 七段失败 | §3.7 |
| Child 非沙箱；默认不可用；无 host exec | §3.8 |
| resume 不覆盖成功清单 | §3.9 |
| Plus 家族锁跨进程约束 Symbolic | §3.10 |
| 无 Plus 锁的孤立 Symbolic 可按哈希进 `probe_train` | §3.10 seed 6 |
| JSON 拒 NaN；拒 `latest` | §3.11 |
| 各成功 `manifest.digest` 自洽 | §3.2 / §3.3 |
| shard 完整 | §3.2 |
| `report.json` 进清单 | analyze `file_hashes` |
| 直接迁移维度拒绝 | 4096≠3584 |
| Week-8 未注册 | `unregistered` / `scientific_conclusion=null` |
| analyze 不编造 P1–P3 | 仅有 labels 时 `p1=null` |
| `git -C` revision | 产物仍 `46a6e26…` |
| repair `record_id` 含 group 与 k | 夹具 k1；scientific k1..k5 |
| 文件 `--in-dir` 拒绝 | §3.7 |
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
| 漂移后（`5413a4bc…`）树上的八段是否仍全部成立 | 本通道未在漂移后重跑；不得用套件期间的 exit 0 给当前树背书 |

## 8. 结论

审查开始与 CLI 套件结束均为 **`HASH_MATCH`** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（61 文件）。全部 `python -m` 证据绑定该快照。本报告落盘后再算 **`HASH_MISMATCH`** `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（仍 61 文件）。本通道未改生产代码。并行写入改了 `models/generate.py`、`models/tiny.py`、`tests/test_round07_regressions.py`。

相对用户指定的独立复跑（绑定开审快照）：夹具八段、scientific tiny 串联、collect 复制 `tasks.jsonl`、给定目录无图则 fit raise、祖先 `col` WRONG-TASK 不绑定（A12-03）、T3 hotpot/musique exit 0、缺 `--in-dir`、`ChildProcessExecutor.isolated_sandbox is False`、resume 不覆盖成功、Plus 然后 Symbolic 新进程锁 `test`——**在 MATCH 树上全部成立**。

这只证明用户 CLI 在 tiny/fixture 上可调度且 fail-closed 行为与声明一致。**不是** OPS-01，**不是** 真实模型上的论文正确性。按本轮硬规则，交卷树与声明冻结不一致则通道失败。

**本通道：`FAIL`（`HASH_MISMATCH`）。** 工程接线在开审快照上成立，但不能给 `5413a4bc…` 或写报告后的脏树背书。连续通过计数不得使用本报告。
