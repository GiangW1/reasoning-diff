# E：端到端工程审查（round-01）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读其他审查通道报告。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 00:28–00:34 +08:00 |
| 声称冻结 hash | `532e05a8038e9862f219ab36927f7f7c0df59ef639045821a2cc801960b2b0c0`（`.planning/audits/round-01/VERSION.md`） |
| 独立复算冻结 hash | **未复现**。对当前树 `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（排除 `__pycache__`，52 文件，posix 路径排序）做内容拼接 SHA256，得到 `3f8ee943577ac8dea8f56f0639957428e1e22353093c8b519bf25c8b01431462`。path+bytes / 路径列表 / digest 拼接、排除 generate/cache 后仍不匹配。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/reasoning_diff`、`tests`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision`（在仓库根执行） | `46a6e26da8637fe29d9f8f0667cb4e513538a59d` |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`run_spec.environment.packages.reasoning-diff = null`） |
| 审查范围 | 用户 CLI 跨模块路径；schema/shape/ID、配置、持久化、恢复、分片、异常、资源、可复现性、隔离执行器 |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`executor.py`、`scoring.py` |
| 指定测试 | `tests/test_cli_pipeline.py` `tests/test_artifacts.py` `tests/test_t3_t4.py` |

**冻结说明：** `VERSION.md` 写明 generate/cache 在冻结后加入。当前树含 `models/generate.py`、`models/collect.py`、`models/adapters.py`、`tests/test_generate_loop.py`、`tests/test_tiny_cache.py`。本报告针对**实际读到并执行到的当前工作区**，不把未复现的冻结 hash 当作已核验身份。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–239 | 通读 + `python -m` / `cli.main` 全阶段实跑 | 阶段互不消费；默认 prepare 无效编辑；无 resume/shard；`report.json` 不进清单 |
| `src/reasoning_diff/artifacts.py` | 1–83 | 通读 + prepare/collect/analyze 产物 + 负路径 | `completed_shard_ok` 无调用方；`success_count` 缺省会加总记录数 |
| `src/reasoning_diff/io.py` | 1–108 | 通读 + JSONL/NPZ/NaN/`runtime_info` cwd 实验 | JSON 原子写有效；NPZ 非原子；`git_revision` 依赖进程 cwd |
| `src/reasoning_diff/executor.py` | 1–59 | 通读 + `get_executor` / `SpyExecutor` / 基类 | 默认不可用且不回退 host exec；`limits` 被忽略；`forbid_host_exec` 未挂到生产路径 |
| `src/reasoning_diff/scoring.py` | 1–30 | 通读 + `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–368 | 通读 + 产物字段核对 | Event 无自动 `record_id`；`Trace.from_dict` 拒额外键 |
| `src/reasoning_diff/splits.py` | 1–66 | CLI `assign_split`/`require_split` 实跑 | 划分守卫有效；CLI 不读上游 split 文件 |
| `src/reasoning_diff/edits.py` | 1–128 | prepare 调用 `apply_value_edit` | 编辑 ID 稳定；默认 p1=7 在本夹具上不改 q |
| `src/reasoning_diff/events.py` | 1–94 | prepare/collect 解析 | 只解析节点别名，不解析前提句 |
| `src/reasoning_diff/graphs.py` | 1–44 | prepare `ancestors` | 返回键是 `node.id`，不是 event identity |
| `src/reasoning_diff/measure.py` | 1–217 | prepare densities/CSP；对照 `build_labels` | CLI 不调用 `build_labels`；event_id 命名空间会错位 |
| `src/reasoning_diff/models/features.py` | 1–28 | collect `select_prefix_index` | 默认轨迹 `token_index=null` |
| `src/reasoning_diff/probes/bilinear.py` | 1–45 | `fit` | 只写 loss，不持久化权重 |
| `src/reasoning_diff/probes/calibrate.py` | 1–33 | `calibrate` | 使用写死分数，不读 fit |
| `src/reasoning_diff/interventions.py` | 1–73 | `intervene` | 合成向量 + 写死报告，不读隐状态 |
| `src/reasoning_diff/repair.py` | 1–57 | `repair` | 不读上游；`RepairRecord` 无 schema 身份字段 |
| `src/reasoning_diff/analysis.py` | 1–108 | `analyze` | 写死数组；Week-8 `not_evaluated` |
| `src/reasoning_diff/transfer.py` | 1–36 | analyze `direct_transfer(4096,3584)` | 维度不匹配声明正确 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | prepare/collect | fixture 拒绝 official |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–35 | `test_t3_t4` + `score_code` | 无宿主 exec |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 1–59 | `test_t3_t4` | `document_edit` 不产出 Task/Edit；无 CLI |
| `src/reasoning_diff/tasks/t3_musique.py` | 1–69 | `test_t3_t4` | 无 CLI |
| `src/reasoning_diff/tasks/t4_boundary.py` | 1–33 | `test_t3_t4` | 无 CLI |
| `pyproject.toml` | 1–26 | 读入口声明 | `reasoning-diff` 脚本未安装；无 `__main__.py` |
| `tests/test_cli_pipeline.py` | 1–18 | 执行 | 只断言 exit 0 与两文件存在 |
| `tests/test_artifacts.py` | 1–73 | 执行 | 覆盖 run_spec/manifest/NaN，不覆盖 resume/CLI 接线 |
| `tests/test_t3_t4.py` | 1–40 | 执行 | 适配器级，不经 CLI |

**抽样未做完整工程审查（非本通道主路径）：** `models/generate.py`、`models/collect.py`、`models/adapters.py`、`models/tiny.py`、`baselines.py`、`rng.py`、`probes/boundary.py`、T1 official / T2 适配器。确认它们**未被** `cli.py` 子命令调用。

## 3. 已执行检查与结果

### 3.1 指定 pytest

```text
命令: python -m pytest tests/test_cli_pipeline.py tests/test_artifacts.py tests/test_t3_t4.py -q --tb=short
cwd:  C:\Users\22688\Desktop\diff
退出码: 0
stdout: ......... [100%]  9 passed in 1.04s
```

测试通过**不能**推出流水线正确。`test_full_cli_smoke` 只检查 `main(argv)==0`、`report.json` 与 `manifest.json` 存在，不检查阶段输入、schema、ID、清单完整性或恢复。

### 3.2 用户 CLI 入口

| 命令 | cwd | 退出码 | 结果 |
|---|---|---|---|
| `python -m reasoning_diff --help`（`PYTHONPATH=src`） | 仓库根 | **1** | `No module named reasoning_diff.__main__; 'reasoning_diff' is a package and cannot be directly executed` |
| `python -m reasoning_diff.cli --help` | 仓库根 | **0** | 子命令：prepare/collect/label/fit/calibrate/intervene/repair/analyze。无 `--resume` / `--shard` / `--in-dir` / `--manifest` |
| `reasoning-diff --help` | 仓库根 | **未启动** | `FileNotFoundError(2)`。`pyproject.toml:16` 声明了脚本，但本机未安装发行包 |
| `cli.main([...])` 八段 | 进程内 | 各 **0** | 与 `python -m reasoning_diff.cli` 行为一致 |

`SERVER_RUNBOOK.md` 记载的用户命令是 `reasoning-diff ...`，本机按该文档无法调用。

### 3.3 真实跨模块 CLI（`python -m reasoning_diff.cli`）

环境：`PYTHONPATH=src`，cwd=仓库根，夹具 `tests/fixtures/t1_tiny.json`。产物目录：`%TEMP%\rd-e-review\pipe_m\`。

| 命令 | 退出码 |
|---|---|
| `prepare --fixture tests/fixtures/t1_tiny.json --out-dir .../prep` | 0 |
| `collect --fixture tests/fixtures/t1_tiny.json --out-dir .../col` | 0 |
| `label --out-dir .../lab` | 0 |
| `fit --out-dir .../fit --split probe_train` | 0 |
| `calibrate --out-dir .../cal --split calibration` | 0 |
| `intervene --out-dir .../int` | 0 |
| `repair --out-dir .../rep --mask task_oracle` | 0 |
| `analyze --out-dir .../an` | 0 |

同一八段经 `reasoning_diff.cli.main` 再跑一遍，退出码同样全 0。

**接线实测（不是源码猜测）：**

- `label` / `fit` / `calibrate` / `intervene` / `repair` / `analyze` 的 `run_spec.input_hashes` 均为 `{}`，`upstream_manifest_ids` 均为 `[]`。
- `collect` 虽要求 `--fixture`，`run_spec.input_hashes` 仍为 `{}`，夹具未入清单。
- `label` 写出硬编码 `p1–p4` 密度（`S=["p3"]`, `M=["p1"]`），与 prepare 的 `p1/p2`、observations 无关。
- `fit` 写出 `loss=2.253189260033166`，无权重、无 features 引用。
- `calibrate` 写出写死 `scores=[0.1,0.2,0.3,0.4]`。
- `analyze` 的 P1/P2/P3 来自 `cli.py` 字面量数组，不读任何上游目录。

### 3.4 schema / shape / ID

默认 `prepare` 产物目录文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

精确观察行（`.../pipe_m/prep/observations.jsonl`）：

```text
{"alignment_ref": "{\"entity_or_expression\": \"p1 * p2\", \"occurrence_version\": 1, \"scope\": \"global\"}", "base_group_id": "fix-t1-001", "comparison_trace": "trace-edit", "edit_id": "edit:fix-t1-001:p1:7", "event_pair": ["{\"entity_or_expression\": \"p1 * p2\", \"occurrence_version\": 1, \"scope\": \"global\"}", "{\"entity_or_expression\": \"p1 * p2\", \"occurrence_version\": 1, \"scope\": \"global\"}"], "observation_id": "obs:{\"entity_or_expression\": \"p1 * p2\", \"occurrence_version\": 1, \"scope\": \"global\"}:p1", "outcome": "no_change", "premise_id": "p1", "raw_values": ["0", "0"], "record_id": "obs:{\"entity_or_expression\": \"p1 * p2\", \"occurrence_version\": 1, \"scope\": \"global\"}:p1", "reference_trace": "trace-base", "rng_pair": "stream:0", "run_id": "prepare", "scan_state": "no_response_observed_in_scan", "schema_version": 1, "status": "ok"}
```

`events.jsonl` 两行值均为 `"0"`，且 `record_id=""`, `run_id=""`, `base_group_id=""`（基线与编辑事件无法用身份字段区分）。

`prepare/labels.jsonl` **不是** `Label` 记录，而是 densities+to_csp 包装；`rho_M_raw=1.0`，`csp=null`，`clean_total=0`。

`collect/traces.jsonl` 含额外键 `feature`。对该行执行 `Trace.from_dict`：

```text
TypeError: Trace.__init__() got an unexpected keyword argument 'feature'
```

同文件 `feature.token_index=null`，`expressible=false`。`features.npz` 键为 `dummy`，shape `[4]`，dtype `float64`，与 traces 无 `array_ref`。

### 3.5 配置 / 持久化 / 可复现性

- 同 cwd、同参数连续两次 `prepare --split-seed 0`：`tasks/edits/splits/events/observations/labels/run_spec/manifest` 八个文件 hash **全部相同**。
- `manifest.digest` 与去掉 digest 后的 `digest(body)` 一致。
- `write_run_spec` 拒绝 `code_revision="latest"`：`ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind`：`ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})`：`ValueError: Out of range float values are not JSON compliant`。
- 在 `C:\Users\22688\AppData\Local\Temp` 为 cwd 调用 `runtime_info()["git_revision"]`：**`None`**（退出码 0）。同一解释器在仓库根得到 `46a6e26...`。
- 同目录第二次 `prepare --edit-value 8`：`edits.jsonl` hash 改变；`p1=7` 记录消失；`n_edits=1`。无旧版本引用。

### 3.6 恢复 / 分片

| 检查 | 结果 |
|---|---|
| CLI `--resume` / `--shard` | help 文本中不存在 |
| 全仓库 `completed_shard_ok` 引用 | **仅** `artifacts.py:81-83` 定义，无调用方 |
| `completed_shard_ok(path, 正确hash)` | `True` |
| `completed_shard_ok(path, 错误hash)` | `False` |
| `completed_shard_ok(缺失, hash)` | `False` |
| 阶段临时 shard / attempt_id | 不存在 |

### 3.7 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 指向不存在文件 | 进程退出码 **1**，未捕获 `FileNotFoundError`（`io.py:64` ← `t1_fixture.py:11` ← `cli.py:60`） | 无 `manifest.json`，无 `failure_count` |
| `cli.main(["fit", ..., "--split", "test"])` | `ValueError("probe fit cannot fit on test; expected ('probe_train',)")` | 无产物 |
| `cli.main(["calibrate", ..., "--split", "probe_train"])` | `ValueError("calibration cannot fit on probe_train; expected ('calibration',)")` | 无产物 |
| `read_jsonl` 非法行 | `ValueError('.../bad.jsonl:1: invalid JSON')` | — |
| `IsolatedExecutor().submit(...)` | `NotImplementedError()` | — |
| `@forbid_host_exec` 包装函数 | `RuntimeError('host execution of model/dataset code is forbidden')` | 生产 CLI/评分未使用该包装 |
| `write_manifest(..., {"tasks":10,"edits":3,"failure":0})`（无 `success` 键） | `success_count=13` | 把记录数加总成成功数 |
| `write_npz` object 数组后 `read_npz` | 写出成功；读入 `ValueError('Object arrays cannot be loaded when allow_pickle=False')` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits={"timeout":1,"mem":1})` 仍只返回 `executor_unavailable`，不记录、不执行 limits。

### 3.8 隔离执行器

```text
get_executor() / get_executor(None) → UnavailableExecutor
get_executor("spy") → SpyExecutor
score_code(合法源, 测试) 默认：
  status=executor_unavailable, value=None, denominator=None, eligibility=False,
  failure_reason="no isolated backend configured; host exec is forbidden"
SpyExecutor + 源含 "exec("：
  status=rejected, eligibility=False, denominator=1
score_numeric("4","4") → value=1.0
score_qa("Paris","paris") → value=1.0
```

全库生产路径未见 `exec(` / `eval(` 作为代码评分回退（`executor.py:44` 仅字符串拒绝）。`forbid_host_exec` 无引用。HumanEval `score_submission` 走 `score_code`，与 `test_humaneval_never_host_exec` 一致。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 对照声称冻结 hash 逐字节复验同一快照 | 独立复算不匹配；树已含冻结后文件；无官方 hash 脚本 |
| 安装 `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境；当前已证实脚本不在 PATH |
| 真实模型 / GPU / 官方数据下载 | 本机 `pending_server`；非本通道可证项 |
| 并发 shard 崩溃注入 / 部分写恢复 | 无 shard 写入器可测 |
| 阅读 A–D/F 报告 | 任务禁止 |
| 修改生产代码或加回归测试 | 任务禁止 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

---

### E-01 用户 CLI 八段不是跨模块流水线

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `cli.py` `_write_stage` 47–54（各阶段只写自己的 jsonl + 空输入 run_spec）
  - `cli.py` `cmd_collect` 122–134（忽略 prepare 产物；写死 `"q = 0\n"`）
  - `cli.py` `cmd_label` 137–140（写死 `p1..p4`，不读 observations）
  - `cli.py` `cmd_fit` 143–151（新 `BilinearProbe`，不读 features.npz）
  - `cli.py` `cmd_calibrate` 154–159（写死 scores）
  - `cli.py` `cmd_intervene` 162–179（`np.random.default_rng(0)` + 写死四项指标）
  - `cli.py` `cmd_repair` 182–185（不读 edits/traces）
  - `cli.py` `cmd_analyze` 188–197（写死 P1–P3 数组）
- **触发条件：** 按文档顺序调用任意后续子命令，或不传上游目录。
- **对应要求：** OPS-01（准备→采集→标注→拟合→校准→干预→修复→分析）；`.planning/research/ARCHITECTURE.md` 产物依赖箭头与「每个命令接收输入 manifest」；`docs/CURSOR_GOAL_PROMPT.md` §六「从生产入口验证跨模块数据流」。
- **复现 / 证据：** §3.3 全阶段 exit 0，但 `input_hashes={}`、`upstream_manifest_ids=[]`；`label` 样本含 `p3`（prepare 夹具没有 p3）。
- **影响：** pytest smoke 与 CLI 退出码会把未接通的桩路径记成“全链路可用”。fit/analyze 数字与数据无关，不能作为复现实验。
- **建议：** 每个命令接收 `--in-dir`/`--manifest`，校验上游 digest，只消费清单内文件；禁止用字面量数组充当阶段输出。在接线完成前不要把 CLI smoke 当作 OPS-01 通过。

---

### E-02 默认 `prepare` 编辑在官方夹具上是无效扰动，却写成完整观测

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `cli.py` 62–70：默认 `edit_premise=premises[0]`（p1），`edit_value="7"`；合成文本**只渲染 `task.nodes`**
  - `cli.py` 93–97：`task_set=next(iter(ancestors(task).values()), set())`（取**第一个节点**祖先，不是 `target`）
  - `tests/fixtures/t1_tiny.json`：`q = p1 * p2` 且 `p2=0`，故 p1→7 后 q 仍为 0
  - `events.py` `parse_fixture_events` 13–18：只匹配节点别名
- **触发条件：** `reasoning-diff prepare --fixture tests/fixtures/t1_tiny.json`（不传 `--edit-premise`）。
- **对应要求：** MEAS-01/02（有限扫描与行为标签）；ARCHITECTURE「任务 DAG 在观察模型前建立」且轨迹须覆盖被编辑前提。
- **复现 / 证据：**
  - 默认：`outcome=no_change`，`raw_values=["0","0"]`，`rho_M_raw=1.0`（把 {p1,p2} 全部记成 M）。
  - 对照：`--edit-premise p2 --edit-value 7` 退出 0，`edited_answer=28`，`outcome=changed`，`raw_values=["0","28"]`。
- **影响：** 默认用户路径制造「行为未覆盖全部任务依赖」的假密度；合成轨迹看不到前提事件，扫描对象只有 q。
- **建议：** 合成文本必须含前提句；默认编辑选能改变 target 的前提，或拒绝无效编辑；`task_set` 用 `ancestors(task)[task.target]`。

---

### E-03 断点、分片、恢复未接到 CLI；重跑静默覆盖

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `artifacts.py:1` 模块声明 “shards and resume rules”
  - `artifacts.py` `completed_shard_ok` 81–83（全库唯一出现）
  - `cli.py` `build_parser` 200–228：无 resume/shard/in-dir
  - `cli.py` 58–59 / 48：`mkdir` + `write_jsonl` 直接覆盖同名文件
- **触发条件：** 对已有 `out-dir` 再跑同一命令；或寻找 `--resume`。
- **对应要求：** OPS-01「清单、配置校验、断点与分片」；ARCHITECTURE「恢复只复用与当前 run spec 一致且校验通过的完成 shard；不在原 JSONL 静默覆盖」。
- **复现 / 证据：** help 无 flag；同目录 `--edit-value 7` 再 `--edit-value 8`，旧 edit 不保留；`completed_shard_ok` 手工调用行为正确但无生产调用。
- **影响：** 长任务无法续跑；失败重试会丢掉先前记录；无法按清单跳过已完成 shard。
- **建议：** 先写临时 shard，hash 校验后原子发布；resume 比对 run_spec；覆盖必须换新 run_id 并保留旧目录。

---

### E-04 `analyze` 主报告不进 manifest

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` `cmd_analyze` 195–196：先 `write_json(.../report.json)`，再 `_write_stage(..., "analysis", ...)`（只登记 `analysis.jsonl` 与 `run_spec.json`）。
- **触发条件：** `analyze --out-dir DIR`。
- **对应要求：** ARCHITECTURE「manifest 列出文件哈希」；SERVER_RUNBOOK「Each stage writes run_spec.json, manifest.json, and stage JSONL/NPZ」。
- **复现 / 证据：** `%TEMP%\rd-e-review\pipe_m\an\manifest.json` 精确内容：`file_hashes` 仅 `analysis.jsonl`、`run_spec.json`；目录里存在 `report.json`。`report_in_manifest=false`。
- **影响：** 用户/后续分析无法用清单证明 `report.json` 未被替换。
- **建议：** 把 `report.json` 列入 `write_manifest` 的 files；或只保留一份清单内报告。

---

### E-05 schema / ID / shape 合同在 CLI 产物上破裂

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `schema.py` `Event` 192–208：无 `__post_init__` 填充 `record_id`；无 `event_id`
  - `schema.py` `Trace.from_dict` 320–328：`cls(**data)`，拒未知键
  - `cli.py` 130–132：`trace.to_dict() | {"feature": feat}`
  - `cli.py` 77：`event_pair=[left.identity.key(), ...]`
  - `graphs.py` 21：`ancestors` 键为 `node.id`
  - `measure.py` `build_labels` 29–33：用 `event_pair[0]` 查 `task_ancestors`
  - `repair.py` `RepairRecord` 12–31：无 `schema_version/record_id/run_id/base_group_id/status`
  - `artifacts.py` 63：`array_shapes` 只存 shape，不存 dtype
  - `cli.py` 47–54 / 127–133：collect 不写 fixture hash
- **触发条件：** 读取默认 CLI 产物并按 schema/ARCHITECTURE 身份字段或 `from_dict` 回载。
- **对应要求：** ARCHITECTURE「所有记录至少包含 schema_version, record_id, run_id, base_group_id, status；记录以 ID 关联」；Feature 需 `array_ref`/`shape`；Label 须能回溯 Observation。
- **复现 / 证据：**
  1. Event：`record_id/run_id/base_group_id` 为空字符串（§3.4）。
  2. Task：`run_id=""`。
  3. `Trace.from_dict(collect traces 行)` → `TypeError ... unexpected keyword argument 'feature'`。
  4. `features.npz["dummy"]` 与 feature 元数据无公共键；`token_index=null`。
  5. prepare/label 的 labels 均非 `Label`（无 `event_id`/`task_label`）。
  6. 若将来调用 `build_labels(prepare_obs, ancestors(task))`，`event_id` 是 identity JSON，祖先表键是 `"q"`，`task_known` 会为 False。
- **影响：** 产物不能作为稳定身份图；后续阶段即使接线也会对不上事件与任务列。
- **建议：** Event 持久化 `event_id` + 填身份字段；feature 放到侧车或合法 metadata；labels 走 `build_labels`；manifest 记录 dtype；collect 写入 fixture hash。

---

### E-06 NPZ 非原子，且可写出不可读回的 object 数组

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `io.py` `atomic_text` 44–56（JSON/JSONL 用 tempfile+fsync+replace）
  - `io.py` `write_npz` 82–85：直接 `np.savez(path, **arrays)`
  - `io.py` `read_npz` 88–90：`allow_pickle=False`
- **触发条件：** `collect` 写 `features.npz`；或向 `write_npz` 传入 object 数组。
- **对应要求：** ARCHITECTURE「shard 完成后原子发布」；「NPZ 读取 allow_pickle=False」。
- **复现 / 证据：** 探测脚本 `write_npz(obj.npz, {"x": object array})` 写出成功；`read_npz` 失败 `Object arrays cannot be loaded when allow_pickle=False`。源码对比显示 NPZ 无原子替换。
- **影响：** 崩溃可留下半截 npz；清单可能指向损坏文件。写出与读入不对等。
- **建议：** 与 `atomic_text` 一样写临时文件再 `os.replace`；写入前拒绝非数值 dtype。

---

### E-07 `code_revision` / `git_revision` 取决于进程 cwd，不是代码位置

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `io.py` `runtime_info` 102–107：`subprocess.run(["git", "rev-parse", "HEAD"], ...)` 无 `cwd=`。
- **触发条件：** 从非仓库目录调用 CLI（或任何写 run_spec 的 API）。
- **对应要求：** OPS-01 / ARCHITECTURE run_spec 必须锁定代码 revision。
- **复现 / 证据：** 仓库根 → `46a6e26da8637fe29d9f8f0667cb4e513538a59d`；cwd=`%TEMP%` → stdout `None`，退出码 0。
- **影响：** 同一二进制在不同启动目录得到不同或空 revision；跨机器/调度器不可比。
- **建议：** `git -C <package_root 或 repo_root> rev-parse HEAD`；失败写明确 `null_reason`。

---

### E-08 文档中的用户入口本机不可用

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - 仓库无 `src/reasoning_diff/__main__.py`
  - `pyproject.toml` 15–16：`reasoning-diff = "reasoning_diff.cli:main"`
  - `docs/SERVER_RUNBOOK.md` 23–30 使用 `reasoning-diff ...`
- **触发条件：** 按 runbook 或 `python -m reasoning_diff` 调用。
- **对应要求：** OPS-01「提供 … CLI」；目标文档要求从用户 CLI 跑通。
- **复现 / 证据：** §3.2 退出码 1 / FileNotFoundError。`python -m reasoning_diff.cli` 在 `PYTHONPATH=src` 下可用。
- **建议：** 增加 `__main__.py` 转调 `main`；文档同时给出 `python -m reasoning_diff`；安装后验证 console script。

---

### E-09 失败路径不落 failure manifest；`success_count` 缺省膨胀

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `cli.py` `main` 232–235：无 try/except，异常即 traceback
  - `cli.py` `cmd_prepare` 58–60：先 `mkdir` 再读夹具
  - `artifacts.py` 69：`success_count = counts.get("success", sum(... if k != "failure"))`
- **触发条件：** 缺失夹具；错误 `--split`；调用方漏传 `success`。
- **对应要求：** ARCHITECTURE「成功/失败计数」；失败须保留。
- **复现 / 证据：** 缺失夹具退出码 1，无 manifest；`success_count` 实验得到 13（10+3）。
- **影响：** 调度器无法区分「未跑」与「失败」；误把任务/编辑条数当成成功次数。
- **建议：** 失败也写 manifest（`failure_count>=1`）；`success_count` 仅使用显式键，缺省为 0。

---

### E-10 隔离执行器无后端、limits 无效；host exec 未回退（部分符合）

- **严重度：** medium（缺后端 / limits）；host-exec 禁令本身 **未破**
- **状态：** confirmed defect（能力缺口）；host exec 禁止为 **非缺陷的正确行为**，见 §6
- **文件 / 符号 / 行号：**
  - `executor.py` `IsolatedExecutor.submit` 22–24：`NotImplementedError`
  - `executor.py` `UnavailableExecutor` 27–33：忽略 `limits`
  - `executor.py` `get_executor` 49–52：非 `"spy"` 一律 Unavailable
  - `executor.py` `forbid_host_exec` 55–59：无引用
  - `scoring.py` `score_code` 19–30
- **触发条件：** HumanEval / `score_code` 默认路径；传入 limits。
- **对应要求：** OPS-01 / EXEC-01 / CURSOR_GOAL §五.15「超时、资源限制、无可用执行器可报告，不回退宿主 exec」。
- **复现 / 证据：** §3.8。`limits` 不出现在 `ExecutionResult`。
- **影响：** 代码题本机永远不可评分（符合 pending_server），但资源限制契约未实现；基类误用会炸而不是结构化失败。
- **建议：** 默认路径保持 Unavailable；实现 limits 字段回显；基类 `submit` 返回 `executor_unavailable` 而非 `NotImplementedError`；生产评分显式包 `forbid_host_exec`。真实隔离后端标 `pending_server`。

---

### E-11 后段「可复现」是硬编码，不是数据复现

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 143–197；`_write_stage` rng 仅 `{"stream": name}`。
- **触发条件：** 两次 `fit`/`analyze` 得到相同数字。
- **对应要求：** QA-01 可复现性；run_spec 须锁定输入哈希与随机流。
- **复现 / 证据：** prepare 同机可复现（§3.5）；fit/analyze 不读输入，故数字稳定没有信息量。`packages.reasoning-diff=null`。
- **影响：** 不能用后段 hash 证明科学步骤可重放。
- **建议：** 先修 E-01；run_spec 记录真实 seed/输入 digest/权重文件 hash。

---

### E-12 T2/T3/T4 适配器未进入用户 CLI

- **严重度：** medium
- **状态：** confirmed defect（入口缺失）；适配器行为另见测试
- **文件 / 符号 / 行号：** `cli.py` 200–228 仅 T1 fixture 的 prepare/collect；无 t2/t3/t4 子命令。
- **触发条件：** 尝试从 CLI 跑 Hotpot/MuSiQue/HumanEval/T4。
- **对应要求：** OPS-01 + DATA-02「T2/T3 全套接入与实验入口」。
- **复现 / 证据：** `--help` 只有八段通用命令；T3/T4 仅 pytest 直接 import。
- **影响：** 用户无法从 CLI 对 T3/T4 做与 T1 同等的准备/评分。
- **建议：** 为各域增加 prepare/score 入口或统一 `--task` 分派，并写 manifest。

---

### E-13 声称冻结 hash 与当前树不一致

- **严重度：** medium
- **状态：** 未证实疑点（hash 算法未知）+ 工作区漂移事实
- **文件：** `.planning/audits/round-01/VERSION.md`；当前 52 个范围内文件
- **触发条件：** 按 VERSION 范围独立哈希。
- **对应要求：** 审查必须钉住稳定内容 hash。
- **复现 / 证据：** §1。当前拼接 hash `3f8ee943577ac8dea8f56f0639957428e1e22353093c8b519bf25c8b01431462` ≠ `532e05a8...`。
- **影响：** 本报告结论不能无条件绑定到声称冻结快照；修复后须重算并重审。
- **建议：** 公布 hash 脚本（路径排序、换行、包含/排除规则）；冻结后禁止静默加文件。

---

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError`；`test_encode_rejects_nan` 通过 |
| `latest` 拒绝 | `write_run_spec(..., code_revision="latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `ValueError("Unknown source_kind 'made_up'")` |
| JSONL 坏行带路径行号 | `bad.jsonl:1: invalid JSON` |
| 同机同 cwd prepare 可复现 | 八文件 hash 全等 |
| prepare `manifest.digest` 自洽 | `digest_ok=true` |
| `require_split` 阻止 test 上 fit、probe_train 上 calibrate | 见 §3.7 |
| 代码评分不回退 host exec | 默认 `executor_unavailable`；HumanEval 测试通过 |
| 直接迁移维度拒绝 | analyze：`not_applicable_dimension_mismatch` 4096≠3584 |
| Week-8 未注册 | `gate0/1/2.decision=unregistered`，`scientific_conclusion=null` |
| Hotpot 不把 supporting facts 当完整 DAG | `test_hotpot_support_is_not_full_dag` 通过 |
| MuSiQue 保留 unanswerable 共组 | `test_musique_keeps_unanswerable_pair` 通过 |
| T4 四状态分立 | `test_t4_statuses_distinct` 通过 |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux 隔离执行器、超时/cgroup、真实 HumanEval | `pending_server`（`docs/SERVER_RUNBOOK.md` Isolated code executor） |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；`models/collect.py` 不在 CLI |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装；见 E-08 |

## 8. 结论

指定测试 **9 passed / 退出码 0**，且 `python -m reasoning_diff.cli` 八段 **退出码 0**。这只证明桩命令能写文件，**不证明** OPS-01 端到端工程成立。

已确认缺陷集中在：阶段未接线（E-01）、默认 prepare 测量对象错误（E-02）、resume/shard 未落地（E-03）、清单漏文件与 ID/schema 破裂（E-04/E-05）、NPZ/revision/入口/失败记账（E-06–E-09）。隔离执行器**没有**回退到宿主 exec，但后端与资源限制未实现（E-10）。

**本通道不通过** OPS-01 端到端工程验收。空通过或「测试绿了」不能作为本通道结论。

下一步（建议，非本通道实施）：先修 CLI 输入 manifest 接线与默认 prepare 编辑/文本，再补 shard/resume 与清单完整性；冻结 hash 脚本公开后重跑本通道。
