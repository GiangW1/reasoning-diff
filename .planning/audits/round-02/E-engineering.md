# E：端到端工程审查（round-02）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读 A–D/F 通道报告。`ISSUES.md` 中作者标为 `fixed_pending_review` 的 E 行已独立复测，不采信作者关闭声明。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 00:44–01:05 +08:00 |
| 声称冻结 hash | `2676a0983f6b42148202eedfbfaea44ce207d1fd386b8d47cbc909e983c5cc38`（`.planning/audits/round-02/VERSION.md`） |
| 独立复算冻结 hash | **未复现**。范围内 **55** 个文件（与 VERSION 计数一致），全部 LF、无 `__pycache__`。用户指定的「POSIX relpath + bytes」：按 posix 路径排序后对每个文件 `relpath.encode("utf-8") + file_bytes` 做 SHA-256，得到 `4ce6fac512f19e2d4d03b6821d9fa2b46632d19265fd5a272b8910fde52ea992`。round-01 F 记载的 `relpath + b"\0" + bytes` 得到 `7b6680d6d937097fd02841d5950df1a7b3498ebcd1965381220b5e429ec5c617`。另试 bytes-only、`io.digest(path→file_digest)`、sha256sum 行、`./` 前缀、长度前缀等，均 ≠ 声称值。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（仓库根与 `%TEMP%` cwd 相同；`io.runtime_info` 现用 `git -C <repo_root>`） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`） |
| 审查范围 | 用户 CLI 跨模块路径；schema/shape/ID、run_spec/manifest、resume、shards、atomic NPZ、`python -m`、隔离执行器、可复现性、异常 |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md` |
| 实跑入口 | `python -m reasoning_diff`（runbook 命令；临时目录 `%TEMP%\rd-e-r2\`，未写入 `src/` / `tests/`） |

**冻结说明：** 审查对象是**当前工作区字节**。声称 hash 未核验，不能把本报告绑定到一个已证明的冻结快照。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–419 | 通读 + `python -m` 八段实跑 + resume/负路径 | `--in-dir`/`--resume` 已挂；后段 provenance 仍空；resume 只看 manifest 是否存在 |
| `src/reasoning_diff/artifacts.py` | 1–83 | 通读 + 各阶段 run_spec/manifest + `success_count` 实验 | digest 自洽；`upstream_manifest_ids` 生产未传；`success_count` 缺省仍加总 |
| `src/reasoning_diff/io.py` | 1–127 | 通读 + NPZ/NaN/`runtime_info` cwd 实验 | JSON/JSONL/NPZ 均走临时文件+`os.replace`；`git -C` 已修 cwd 依赖 |
| `src/reasoning_diff/__main__.py` | 1–4 | 通读 + `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–26 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–45 | 对照实跑 | 命令形状已可执行；`--resume` 语义弱于文档；隔离执行器仍 `pending_server` |
| `src/reasoning_diff/executor.py` | 1–59 | 通读 + `get_executor` / `score_code` / 基类 | 默认 Unavailable；`limits` 忽略；`forbid_host_exec` 无生产引用 |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–371 | 通读 + 产物 `from_dict` | Event/Label 身份空；collect `Trace` 拒 `feature`；编辑 Task `record_id` 碰撞 |
| `src/reasoning_diff/splits.py` | 1–75 | CLI `require_split` | test 上 fit、probe_train 上 calibrate 仍拒绝 |
| `src/reasoning_diff/edits.py` | 1–141 | 默认 prepare `p2→2` | 重算答案 8；`from_dict` 保留原 `record_id` |
| `src/reasoning_diff/events.py` | 1–125 | prepare/collect 解析 | 合成文本只渲染节点，前提句不进轨迹 |
| `src/reasoning_diff/graphs.py` | 1–44 | prepare `ancestors` | 单节点夹具下 `next(iter(anc.values()))` 碰巧等于 `{p1,p2}` |
| `src/reasoning_diff/measure.py` | 1–242 | prepare/label `build_labels` | CLI 现调用 `build_labels`；densities 仍用第一节点祖先集 |
| `src/reasoning_diff/models/features.py` | 1–43 | collect prefix | `pre_step.token_index=null`，`expressible=false` |
| `src/reasoning_diff/models/collect.py` | 1–47 | 对照 CLI | **未被** `cli.py` 调用；CLI collect 写 `np.eye(4)` |
| `src/reasoning_diff/probes/bilinear.py` | 1–74 | `fit` | 只持久化 loss/rank/split，无权重 |
| `src/reasoning_diff/probes/calibrate.py` | 1–35 | `calibrate` | 分数 = `\|loss\|, \|loss\|+0.1, 0.3, 0.4` |
| `src/reasoning_diff/interventions.py` | 1–91 | `intervene` | 对 dummy `I_4` 做几何；效应字段全 `null` |
| `src/reasoning_diff/repair.py` | 1–57 | `repair` | 忽略 `--in-dir`；`RepairRecord` 无 schema 身份字段 |
| `src/reasoning_diff/analysis.py` | 1–131 | `analyze` | `p1_table.jsonl` 不存在 → `not_evaluated`；P1–P3 为 null |
| `src/reasoning_diff/transfer.py` | 1–40 | analyze `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | prepare/collect | fixture 拒绝 official |
| `src/reasoning_diff/tasks/catalog.py` | 1–39 | 通读 | 无 CLI 分派 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–35 | 对照 `score_code` | 无宿主 exec；无 CLI |
| `src/reasoning_diff/models/adapters.py` | 1–29 | 通读 | 冻结 revision 卡片；CLI 未用 |
| `src/reasoning_diff/rng.py` | 1–53 | 通读 | CLI 未用 `StreamBank` |
| `tests/test_cli_pipeline.py` | 1–29 | 读，未当作验收 | 只断言 exit 0、`not_evaluated`、report 进清单 |
| `tests/test_artifacts.py` | 1–73 | 读 | 不覆盖 resume/CLI 接线 |
| `tests/test_review_regressions.py` | 268–315 | 读作者关闭用例 | `test_pipeline_consumes_upstream` 不断言 input_hashes / Trace.roundtrip |

**抽样未做完整工程审查（非本通道主路径）：** `models/generate.py`、`models/tiny.py`、`baselines.py`、`probes/boundary.py`、T1 official / T2 / T3 / T4 适配器。确认它们**未被** `cli.py` 子命令调用。

## 3. 已执行检查与结果

### 3.1 用户 CLI 入口

环境：cwd=`C:\Users\22688\Desktop\diff`，`PYTHONPATH=src`，除非另注。

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python -m reasoning_diff --help` | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze。prepare 有 `--resume`；其余有 `--in-dir`/`--resume`。**无 `--shard` / `--manifest`** |
| `python -m reasoning_diff --help`（清空 `PYTHONPATH`） | **1** | `No module named reasoning_diff` |
| `reasoning-diff --help` | **未启动** | 本机无 console script（包未安装） |

`__main__.py` 存在并转调 `main`。runbook 的 `python -m reasoning_diff …` 在 `PYTHONPATH=src` 或 `pip install -e .` 后可用；本只读审查未改环境。

### 3.2 真实跨模块 CLI（runbook 顺序）

产物根：`%TEMP%\rd-e-r2\`。夹具 `tests/fixtures/t1_tiny.json`。

| 命令 | 退出码 |
|---|---|
| `prepare --fixture tests/fixtures/t1_tiny.json --out-dir <tmp>/prep` | 0 |
| `collect --fixture … --in-dir <tmp>/prep --out-dir <tmp>/collect` | 0 |
| `label --in-dir <tmp>/prep --out-dir <tmp>/label` | 0 |
| `fit --in-dir <tmp>/collect --labels-dir <tmp>/label --out-dir <tmp>/fit --split probe_train` | 0 |
| `calibrate --in-dir <tmp>/fit --out-dir <tmp>/cal --split calibration` | 0 |
| `intervene --in-dir <tmp>/collect --out-dir <tmp>/intervene` | 0 |
| `repair --in-dir <tmp>/prep --out-dir <tmp>/repair --mask task_oracle` | 0 |
| `analyze --in-dir <tmp>/label --out-dir <tmp>/analyze` | 0 |

**接线实测（不是源码猜测）：**

| 阶段 | `input_hashes` | `upstream_manifest_ids` | 实际消费 |
|---|---|---|---|
| prepare | `{t1_tiny.json: 3267db38…}` | `[]` | 夹具 |
| collect | `{}` | `[]` | 若有 `tasks.jsonl` 则取第一行 Task，否则再读夹具；**不读** prepare traces/events；`features.npz` = `I_4` |
| label | `{}` | `[]` | 读 prepare `observations.jsonl` + `tasks.jsonl`；`build_labels` |
| fit | `{}` | `[]` | 读 `features.npz` 的 `H`/`E`（dummy `I_4`）+ labels 的 `behavior_label` |
| calibrate | `{}` | `[]` | 读第一条 probe `loss`，再拼写死 `0.3, 0.4` |
| intervene | `{}` | `[]` | 读 `H[0]`/`H[1]`（`I_4` 两行）；`status=geometry_only`；target/nontarget/task_correct/invalid 全 `null` |
| repair | `{}` | `[]` | **不读** `--in-dir`；`run_repair("task_oracle", ["q"], [4,4,4], "updated prefix")` |
| analyze | `{}` | `[]` | 寻找 `p1_table.jsonl`（label **从不写**）；`p1/p2/p3=null`；`status=not_evaluated` |

`collect` 无 `--in-dir` 仍 exit 0。`analyze` 无 `--in-dir` 仍 exit 0，且 `report.json` 与带 `--in-dir` 的报告 **532 字节同形**。

八个阶段 `manifest.digest` 均等于 `digest(body without digest)`。

### 3.3 schema / shape / ID

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

Observation（精确一行）：

```text
{"alignment_ref": "{\"entity_or_expression\": \"q\", ...}", "edit_id": "edit:fix-t1-001:p2:2", "event_pair": ["q","q"], "node_id": "q", "observation_id": "obs:q:p2", "outcome": "changed", "premise_id": "p2", "raw_values": ["0","8"], "record_id": "obs:q:p2", "run_id": "prepare", "scan_state": "observed_response", ...}
```

相对 round-01：默认编辑现为 **p2:0→2**，`outcome=changed`，`raw_values=["0","8"]`。这是夹具上的有效扰动，**不是**科学全量扫描。

仍破裂的身份合同：

1. `events.jsonl` 两行 `record_id=""`, `run_id=""`, `base_group_id=""`。`Event.from_dict` 成功但身份仍空。
2. 两行 Task：`task_id` 分别为 `fix-t1-001` 与 `fix-t1-001::p2=2`，但 **`record_id` 均为 `fix-t1-001`**；`run_id=""`。
3. prepare/label 的 Label：`record_id=""`, `run_id=""`, `base_group_id=""`。第二行是 densities sidecar，不是 `Label`。
4. collect `traces.jsonl` 含额外键 `feature`。`Trace.from_dict` → `TypeError: unexpected keyword argument 'feature'`。去掉该键后可回载。
5. `features.npz` 键 `dummy`/`H`/`E`，各 `shape [4,4]` `float64`。manifest `array_shapes` **无 dtype**。trace 无 `array_ref`。
6. `feature.pre_step.token_index=null`，`expressible=false`；`pre_value=3`，`post_step=4`。
7. `RepairRecord` 无 `schema_version` / `record_id` / `run_id` / `base_group_id` / `status`。
8. 合成轨迹文本为 `"q = 0\n"` / `"q = 8\n"`（只渲染节点，不含前提句）。`token_ids = range(1, len(text)+1)`，不是模型 token。

### 3.4 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：`tasks/edits/splits/events/observations/labels/traces/run_spec/manifest` **九文件 hash 全等**。
- 两次 `fit`：`probes.jsonl` hash 全等（`loss=0.14174393701671076`）。这是对 **dummy `I_4`** 的优化，不是隐状态复现。
- `write_run_spec(..., code_revision="latest")` → `ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind` → `ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})` → `ValueError: Out of range float values are not JSON compliant`。
- cwd=`%TEMP%` 调用 `runtime_info()["git_revision"]`：**`46a6e26…`**（不再依赖进程 cwd）。
- `packages.reasoning-diff = null`。
- 后段 `run_spec.rng` 仅为 `{"stream": "<stage>"}`，无 seed、无输入 digest。

### 3.5 恢复 / 分片

| 检查 | 结果 |
|---|---|
| CLI `--resume` | help 中存在（除 prepare 外与 `--in-dir` 一起） |
| CLI `--shard` | **不存在** |
| `completed_shard_ok` 生产调用 | 仅 `cli.py:224`：写出 `traces-shard-0000.jsonl` 后立刻用**自己刚算的 hash** assert（恒真） |
| collect shard | 与 `traces.jsonl` **字节相同**（hash `d412f675…`）；不是按任务/组切分 |
| `--resume` + 篡改 `traces.jsonl` | exit **0**；篡改保留；manifest 不变 |
| `--resume` + 删除 shard | exit **0**；shard 仍缺失 |
| `--resume` + 删除 `observations.jsonl` | exit **0**；观测仍缺失 |
| `--resume` + 新 `--edit-value 9` | exit **0**；edits hash **不变**（忽略新参数） |
| 无 `--resume` 重跑 collect | exit 0；覆盖写回原 hash |

`_resume`（`cli.py:33-34`）实现为：`bool(resume) and (out / "manifest.json").exists()`。不校验 digest、不比对 run_spec、不检查清单内文件。

### 3.6 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 指向不存在文件 | 进程 **1**，未捕获 `FileNotFoundError`（`io.py:64` ← `t1_fixture.py:11` ← `cli.py:83`） | 先 `mkdir`（`cli.py:82`），留下**空目录** `badprep/`，无 `manifest.json` |
| `label` 无 `--in-dir` | **1** `FileNotFoundError: label requires --in-dir with observations.jsonl` | 无目录 |
| `fit --split test` | **1** `ValueError: probe fit cannot fit on test; expected ('probe_train',)` | 无产物 |
| `calibrate --split probe_train` | **1** `ValueError: calibration cannot fit on probe_train; expected ('calibration',)` | 无产物 |
| `fit --in-dir <prep>`（无 features.npz） | **1** `FileNotFoundError: fit requires features.npz from collect` | 无产物 |
| `read_jsonl` 非法行 | `ValueError('.../bad.jsonl:1: invalid JSON')` | — |
| `IsolatedExecutor().submit(...)` | `NotImplementedError()` | — |
| `@forbid_host_exec` 包装函数 | `RuntimeError('host execution of model/dataset code is forbidden')` | 生产 CLI/评分未使用 |
| `write_manifest(..., {"tasks":10,"edits":3,"failure":0})` | `success_count=13` | 把记录数加总成成功数 |
| `write_npz` object 数组后 `read_npz` | 写出成功；读入 `ValueError('Object arrays cannot be loaded when allow_pickle=False')` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits={"timeout":1,"mem":1})` 仍只返回 `executor_unavailable`，`limits` 不进 `ExecutionResult`。

### 3.7 隔离执行器

```text
get_executor() / get_executor(None) → UnavailableExecutor
get_executor("spy") → SpyExecutor
score_code(合法源, 测试) 默认：
  status=executor_unavailable, value=None, denominator=None, eligibility=False,
  failure_reason="no isolated backend configured; host exec is forbidden"
SpyExecutor + 源含 "exec("：status=rejected
score_numeric("4","4") → value=1.0
score_qa("Paris","paris") → value=1.0
```

全库生产路径未见 `exec(` / `eval(` 作为代码评分回退。`forbid_host_exec` 无引用。HumanEval `score_submission` 走 `score_code`。

### 3.8 atomic NPZ

`write_npz`（`io.py:82-97`）现为 `mkstemp` → `np.savez(temp)` → `os.replace`。成功后无 `.feat.npz.*` 残留。这关闭了 round-01「直接 `np.savez(path)`」的半截文件问题。写出 object 数组仍被允许，读回失败（§3.6）。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 对照声称冻结 hash 逐字节复验同一快照 | 独立复算不匹配；无官方 hash 脚本可执行 |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境；已证实未安装时 `python -m` 需 `PYTHONPATH=src` |
| 真实模型 / GPU / 官方数据下载 | 本机 `pending_server`；夹具烟测不得冒充 |
| 并发 shard 崩溃注入 | 无真实分片写入器；现有 shard 是 traces 副本 |
| 阅读 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |
| 把 `tests/test_cli_pipeline.py` 当验收 | 该测试不断言 input_hashes、Trace 回载或 resume |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。

---

### E-01 后段仍无清单级流水线（reopened）

- **严重度：** high
- **状态：** confirmed defect（reopened）。作者 `fixed_pending_review` / `test_pipeline_consumes_upstream` **不足以关闭**。
- **文件 / 符号 / 行号：**
  - `cli.py` `_write_stage` 57–68：只写本阶段 jsonl + **空** `input_hashes` 的 run_spec
  - `cli.py` `cmd_collect` 199–226：合成 `"q = …\n"` + `np.eye(4)`；不读 prepare traces
  - `cli.py` `cmd_calibrate` 287–292：`scores = [abs(loss), abs(loss)+0.1, 0.3, 0.4]`
  - `cli.py` `cmd_repair` 338–344：**忽略** `args.in_dir`
  - `cli.py` `cmd_analyze` 351–358：只认 `p1_table.jsonl`（label 不写）
  - `artifacts.py` `write_manifest` 71：`upstream_manifest_ids` 默认 `[]`；CLI 从不传入
- **触发条件：** 按 `docs/SERVER_RUNBOOK.md` 跑八段。
- **对应要求：** OPS-01；ARCHITECTURE「每个命令接收输入 manifest」；SERVER_RUNBOOK「Each stage writes run_spec.json, manifest.json」。
- **复现 / 证据：** §3.2：prepare 以外 `input_hashes={}`、`upstream_manifest_ids=[]`。label 确实读 observations（相对 round-01 有接线），但 collect 特征、fit 权重、calibrate 分数、repair 槽位、analyze P1–P3 **都不构成可审计输入图**。
- **影响：** exit 0 与「consumes upstream」测试会把 dummy `I_4` + 写死分数记成全链路。不能作为复现实验。
- **建议：** 每个命令校验上游 `manifest.digest`，把上游文件列入 `input_hashes`/`upstream_manifest_ids`；禁止用 `np.eye` / 字面量分数充当阶段输出。接线完成前不要把 CLI smoke 当作 OPS-01 通过。

---

### E-02 默认 prepare 不再是 4×0 空操作（closed）

- **严重度：** （原 high）
- **状态：** **closed**（本夹具路径独立确认）
- **文件 / 符号 / 行号：** `cli.py` `_default_edit` 71–75；`cmd_prepare` 85–87
- **复现 / 证据：** `run_spec.config.edit_premise=p2`, `edit_value=2`；`outcome=changed`；`raw_values=["0","8"]`；编辑题 `answer_spec.value=8`。
- **残留：** 合成文本仍只渲染 `task.nodes`（§3.3）；`task_set=next(iter(anc.values()), set())`（`cli.py:147`）在多节点图上仍会取错列。单节点 `t1_tiny` 碰巧正确。不重开 E-02，记入 E-15。

---

### E-03 `--resume` / shard 未实现恢复语义（reopened）

- **严重度：** high
- **状态：** confirmed defect（reopened）。作者以「`--resume`；`traces-shard-0000.jsonl`」标 fixed，**否决**。
- **文件 / 符号 / 行号：**
  - `cli.py` `_resume` 33–34
  - `cli.py` `cmd_collect` 221–224（自校验 shard）
  - `cli.py` `build_parser` 387–408：无 `--shard`
  - `artifacts.py` `completed_shard_ok` 81–83
- **触发条件：** `--resume`；或寻找可恢复分片。
- **对应要求：** OPS-01「断点与分片」；ARCHITECTURE「恢复只复用与当前 run spec 一致且校验通过的完成 shard」。
- **复现 / 证据：** §3.5。SERVER_RUNBOOK L37「Resume a completed stage with `--resume` if `manifest.json` already exists」与实现一致，但该语义**不安全**：有残缺/被改清单也会跳过。
- **影响：** 长任务「续跑」会吞掉损坏或不完整产物；换参数不重跑。
- **建议：** resume 必须校验清单内每个 hash 与当前 run_spec；缺文件或 hash 变则重算。先写临时 shard，校验后再发布。

---

### E-04 `report.json` 已进 analyze manifest（closed）

- **状态：** **closed**
- **证据：** `%TEMP%\rd-e-r2\analyze\manifest.json` 的 `file_hashes` 含 `analysis.jsonl`、`report.json`、`run_spec.json`。`cli.py` 369–370。

---

### E-05 schema / ID / shape 合同仍破裂

- **严重度：** high
- **状态：** confirmed defect（round-01 未在 ISSUES 标 fixed；本轮仍在）
- **文件 / 符号 / 行号：**
  - `schema.py` `Event` 192–217：无 `__post_init__` 填 `record_id`
  - `schema.py` `Trace.from_dict` 324–331：`cls(**data)`，拒未知键
  - `cli.py` 223 / 225：`trace.to_dict() | {"feature": feat}`
  - `edits.py` 120–129：`Task.from_dict({**task.to_dict(), "task_id": …})` 保留旧 `record_id`
  - `repair.py` `RepairRecord` 12–31
  - `artifacts.py` 63：`array_shapes` 只存 shape
- **触发条件：** 按 schema 回载默认 CLI 产物。
- **复现 / 证据：** §3.3。
- **影响：** 事件无法用身份字段区分基线/编辑；编辑 Task 与基线共享 `record_id`；collect traces 不能 `from_dict`。
- **建议：** Event/Label 持久化身份；feature 进 metadata 或侧车；编辑 Task 使用新 `record_id`；manifest 记录 dtype。

---

### E-06 NPZ 已原子发布（closed，残留 object 数组）

- **状态：** **closed**（原子写）；object 数组读写不对等为残留 `confirmed defect`（medium）
- **文件 / 符号 / 行号：** `io.py` `write_npz` 82–97；`read_npz` 100–102
- **证据：** 成功后无临时残留；object 写出成功、读入 `allow_pickle=False` 失败。
- **建议：** 写入前拒绝非数值 dtype。

---

### E-07 `git_revision` 不再依赖进程 cwd（closed）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `io.py` `runtime_info` 114–125：`git -C str(root)`，`root = Path(__file__).resolve().parents[2]`
- **证据：** cwd=`%TEMP%` 仍得到 `46a6e26…` 与 `repo_root=C:\Users\22688\Desktop\diff`。

---

### E-08 `python -m reasoning_diff` 入口已存在（closed，残留未安装）

- **状态：** **closed**（模块入口）；未安装 console script 为环境事实，不是缺文件
- **文件 / 符号 / 行号：** `src/reasoning_diff/__main__.py` 1–4；`pyproject.toml` 15–16
- **证据：** §3.1。runbook 假定 `pip install -e .`；本机未装时必须设 `PYTHONPATH=src`。

---

### E-09 失败路径不落 failure manifest；`success_count` 缺省膨胀

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `cli.py` `main` 412–415：无 try/except
  - `cli.py` `cmd_prepare` 82–83：先 `mkdir` 再读夹具
  - `artifacts.py` 69：`success_count = counts.get("success", sum(... if k != "failure"))`
- **复现 / 证据：** §3.6。空 `badprep/`；`success_count` 实验 = 13。
- **影响：** 调度器无法区分未跑与失败；误把任务/编辑条数当成成功次数。

---

### E-10 隔离执行器无后端、limits 无效；host exec 未回退

- **严重度：** medium（缺后端 / limits）；host-exec 禁令本身 **未破**
- **状态：** confirmed defect（能力缺口）；禁止 host exec 为正确行为，见 §6
- **文件 / 符号 / 行号：** `executor.py` 22–33、49–59；`scoring.py` 19–30
- **复现 / 证据：** §3.7。`limits` 不出现在 `ExecutionResult`。
- **对应要求：** OPS-01 / EXEC-01 / SERVER_RUNBOOK Isolated code executor。

---

### E-11 后段「可复现」仍是 dummy 复现

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 220–221、250–277、347–370
- **复现 / 证据：** prepare 同机可复现（§3.4）。fit/analyze 数字稳定，因为输入是 `I_4` 与字面量维度，不是测量。
- **影响：** 不能用后段 hash 证明科学步骤可重放。

---

### E-12 T2/T3/T4 适配器未进入用户 CLI

- **严重度：** medium
- **状态：** confirmed defect（入口缺失）
- **文件 / 符号 / 行号：** `cli.py` 374–408 仅 T1 fixture 的 prepare/collect
- **对应要求：** OPS-01 + DATA-02
- **复现 / 证据：** `--help` 只有八段通用命令；catalog loaders 无子命令。

---

### E-13 声称冻结 hash 与当前树不一致

- **严重度：** medium
- **状态：** 未证实疑点（聚合算法未公开）+ 工作区漂移事实
- **文件：** `.planning/audits/round-02/VERSION.md`；当前 55 个范围内文件
- **复现 / 证据：** §1。`4ce6fac5…` / `7b6680d6…` ≠ `2676a098…`。
- **影响：** 本报告不能无条件绑定到声称冻结快照。

---

### E-14 collect 特征合同与模型采集路径断开

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `cli.py` 207–225：合成字符偏移 + `np.eye(4)`
  - `models/collect.py` 11–25：`collect_tiny` **无调用方**（CLI）
- **触发条件：** runbook `collect`
- **对应要求：** MODEL-01；OPS-01 采集阶段
- **复现 / 证据：** `features.npz` 三键皆 `I_4`；`pre_step` 不可表达；`Trace.from_dict` 失败。
- **影响：** fit/intervene 吃的是单位阵，不是残差流。夹具烟测不能外推到权重。

---

### E-15 合成轨迹与 `task_set` 仍用节点捷径

- **严重度：** medium
- **状态：** confirmed defect（E-02 关闭后的残留）
- **文件 / 符号 / 行号：** `cli.py` 89–94、147；`events.py` `parse_fixture_events` 21–35
- **复现 / 证据：** 轨迹文本无 `p1`/`p2` 句；`surface_mentions=[]`；`to_csp.clean_total=0`，`csp=null`。
- **影响：** 有限扫描对象只有 `q`；densities 的 M=`["p1"]` 来自「行为集={p2}、任务集=第一节点祖先」，不是完整前提事件扫描。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError` |
| `latest` 拒绝 | `write_run_spec(..., code_revision="latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `ValueError("Unknown source_kind 'made_up'")` |
| JSONL 坏行带路径行号 | `bad.jsonl:1: invalid JSON` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 |
| `require_split` 阻止 test 上 fit、probe_train 上 calibrate | §3.6 |
| 代码评分不回退 host exec | 默认 `executor_unavailable` |
| 直接迁移维度拒绝 | `not_applicable_dimension_mismatch` 4096≠3584 |
| Week-8 未注册 | `gate0/1/2.decision=unregistered`，`scientific_conclusion=null` |
| analyze 不编造 P1–P3 | `p1=p2=p3=null`，`status=not_evaluated` |
| intervene 不编造效应 | `geometry_only`，效应字段 null |
| 默认 prepare 不再 4×0 | E-02 closed |
| `report.json` 进清单 | E-04 closed |
| NPZ 原子替换 | E-06 closed（主缺陷） |
| `git -C` revision | E-07 closed |
| `python -m` 入口 | E-08 closed（有 PYTHONPATH 时） |
| label 拒绝无 `--in-dir` | exit 1，不再写死 p1–p4 |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux 隔离执行器、超时/cgroup、真实 HumanEval | `pending_server` |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；`models/collect.py` 不在 CLI |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |
| 声称 hash 的官方聚合脚本 | 未公布；独立复算失败 |

## 8. 结论

`python -m reasoning_diff` 按 runbook 八段 **全部退出码 0**。这只证明夹具烟测能写文件，**不证明** OPS-01 端到端工程成立，也 **不是** 科学全跑。

相对 round-01，本通道确认关闭：E-02（本夹具默认编辑）、E-04（report 进清单）、E-06 主缺陷（NPZ 原子）、E-07（revision 锚定代码树）、E-08（`__main__.py`）。analyze/intervene 不再编造效应数字。

仍不通过的核心缺陷：后段 provenance 为空（E-01）、resume 只看文件是否存在（E-03）、schema/ID 破裂（E-05）、collect 与模型采集断开（E-14）、失败记账（E-09）、T2–T4 无 CLI（E-12）。声称冻结 hash **未复现**（E-13）。

**本通道不通过** OPS-01。`fixed_pending_review` 的 E-01 / E-03 **重开**。空通过或「测试绿了」不能作为本通道结论。

下一步（建议，非本通道实施）：先修清单级 `--in-dir` 哈希与 resume 校验，再把 collect 接到真实特征合同；公布 hash 脚本后重跑本通道。
