# E：端到端工程审查（round-03）

审查通道只读生产代码。本文件是本通道唯一写入物。未阅读本轮 A–D/F 通道报告。`ISSUES.md` 中作者标为本地已关的「CLI provenance/resume hashes, collect prefix-id features」已独立复测，不采信作者关闭声明。

夹具烟测 **不是** 科学全跑。本通道不把 `exit 0`、pytest 绿或 `report.json` 存在当作 OPS-01 通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer E（end-to-end engineering），独立子代理，只读审查 |
| 审查时间 | 2026-09-21 00:58–01:25 +08:00 |
| 声称冻结 hash | `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`（`.planning/audits/round-03/VERSION.md`） |
| 独立复算冻结 hash | **复现成功**。按 VERSION 脚本：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`，**55** 个文件；对每个文件 `posix_relpath.encode("utf-8") + b"\x00" + file_bytes` 做 SHA-256，得到 `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 均未跟踪） |
| 运行时 `code_revision` / `environment.git_revision` | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（仓库根与 `%TEMP%\rd-e-r3` cwd 相同；`io.runtime_info` 用 `git -C <repo_root>`） |
| Python | 3.11.7（Anaconda），`PYTHONPATH=src`；包未 editable 安装（`packages.reasoning-diff = null`，`numpy=1.26.4`） |
| 审查范围 | 用户 CLI 跨模块路径；schema/shape/ID、run_spec/manifest、resume 哈希校验、shards、atomic NPZ、`python -m`、隔离执行器、可复现性、异常 |
| 指定必读 | `cli.py`、`artifacts.py`、`io.py`、`__main__.py`、`pyproject.toml`、`docs/SERVER_RUNBOOK.md` |
| 实跑入口 | `python -m reasoning_diff`（runbook 命令）；产物根 `%TEMP%\rd-e-r3\`，未写入 `src/` / `tests/` |

**冻结说明：** 审查对象是当前工作区字节，且与声称冻结 hash **一致**。本报告绑定该快照。

## 2. 逐文件覆盖

| 文件 | 行 | 覆盖方式 | 结论 |
|---|---|---|---|
| `src/reasoning_diff/cli.py` | 1–511 | 通读 + `python -m` 八段实跑 + resume/负路径 + `--in-dir` 文件 | `--in-dir` 目录时写 input_hashes；`--resume` 校验 file_hashes；`--in-dir` 指向文件则 `_upstream` 崩；无 `--shard` |
| `src/reasoning_diff/artifacts.py` | 1–83 | 通读 + 各阶段 manifest + `success_count` 实验 | digest 自洽；`upstream_manifest_ids` 现由 CLI 传入 digest 字段；`success_count` 缺省仍加总 |
| `src/reasoning_diff/io.py` | 1–127 | 通读 + NPZ/NaN/`runtime_info` cwd 实验 | JSON/JSONL/NPZ 均临时文件+`os.replace`；`git -C` 不依赖进程 cwd |
| `src/reasoning_diff/__main__.py` | 1–4 | 通读 + `python -m reasoning_diff --help` | 转调 `cli.main`；无 `PYTHONPATH`/未安装则失败 |
| `pyproject.toml` | 1–26 | 读入口 | 声明 `reasoning-diff = reasoning_diff.cli:main`；本机未装 |
| `docs/SERVER_RUNBOOK.md` | 1–45 | 对照实跑 | 命令形状可执行；L37 resume 语义弱于实现（实现已校 hash，但仍不比 run_spec）；隔离执行器仍 `pending_server` |
| `src/reasoning_diff/executor.py` | 1–59 | 通读 + `get_executor` / `score_code` / 基类 | 默认 Unavailable；`limits` 忽略；`forbid_host_exec` 无生产引用 |
| `src/reasoning_diff/scoring.py` | 1–30 | `score_code`/`score_numeric`/`score_qa` | 代码分默认 `executor_unavailable`；无宿主 exec |
| `src/reasoning_diff/schema.py` | 1–373 | 通读 + 产物 `from_dict` | Event/Label 身份空；collect `Trace` 拒 `feature`；编辑 Task `record_id` 碰撞 |
| `src/reasoning_diff/splits.py` | 1–78 | CLI `require_split` | test 上 fit、probe_train 上 calibrate 仍拒绝 |
| `src/reasoning_diff/edits.py` | 1–184 | 默认 prepare `p2→2` | 重算答案 8；`from_dict` 保留原 `record_id` |
| `src/reasoning_diff/events.py` | 1–142 | prepare/collect 解析 | 合成文本只渲染节点，前提句不进轨迹 |
| `src/reasoning_diff/graphs.py` | 1–44 | prepare `ancestors` | CLI 现用 `anc.get(task.target)`；单节点夹具下任务集=`{p1,p2}` |
| `src/reasoning_diff/measure.py` | 1–248 | prepare/label `build_labels` | CLI 调用 `build_labels` |
| `src/reasoning_diff/models/features.py` | 1–43 | collect prefix | `pre_step.token_index=null`，`expressible=false` |
| `src/reasoning_diff/models/collect.py` | 1–47 | 对照 CLI | **未被** `cli.py` 调用 |
| `src/reasoning_diff/probes/bilinear.py` | 1–76 | `fit` | 只持久化 loss/rank/split，无权重 |
| `src/reasoning_diff/probes/calibrate.py` | 1–42 | `calibrate` | CLI 把 `\|loss\|, \|loss\|+0.1, 0.3, 0.4` 再做 `1-p` |
| `src/reasoning_diff/interventions.py` | 1–91 | `intervene` | 对单行 prefix 向量做几何；`main_norm=0`；效应字段全 `null` |
| `src/reasoning_diff/repair.py` | 1–64 | `repair` | 现读 `--in-dir` 的 `traces.jsonl`；`RepairRecord` 无 schema 身份字段 |
| `src/reasoning_diff/analysis.py` | 1–157 | `analyze` | `p1_table.jsonl` 不存在 → `not_evaluated`；P1–P3 为 null |
| `src/reasoning_diff/transfer.py` | 1–50 | analyze `direct_transfer(4096,3584)` | 维度拒绝正确 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | prepare/collect | fixture 拒绝 official |
| `src/reasoning_diff/tasks/catalog.py` | 1–39 | 通读 | 无 CLI 分派 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–61 | 对照 `score_code` | 无宿主 exec；无 CLI |
| `src/reasoning_diff/models/adapters.py` | 1–29 | 通读 | 冻结 revision 卡片；CLI 未用 |
| `src/reasoning_diff/rng.py` | 1–53 | 通读 | CLI 未用 `StreamBank` |
| `tests/test_cli_pipeline.py` | 1–29 | 读，未当作验收 | 只断言 exit 0、`not_evaluated`、report 进清单 |
| `tests/test_artifacts.py` | 1–73 | 读 | 不覆盖 resume/CLI 接线 |
| `tests/test_review_regressions.py` | 358–371 | 读作者关闭用例 | `test_pipeline_consumes_upstream` 仍不断言 `input_hashes` / `Trace.from_dict` / `--labels-dir` |

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

产物根：`%TEMP%\rd-e-r3\`。夹具 `tests/fixtures/t1_tiny.json`。`--in-dir` 按 `docs/SERVER_RUNBOOK.md` 指向上一阶段目录。另测 `--in-dir` **等于该 runbook 文件本身**（§3.5 / §3.6）。

| 命令 | 退出码 |
|---|---|
| `prepare --fixture tests/fixtures/t1_tiny.json --out-dir <tmp>/prep` | **0** |
| `collect --fixture … --in-dir <tmp>/prep --out-dir <tmp>/collect` | **0** |
| `label --in-dir <tmp>/prep --out-dir <tmp>/label` | **0** |
| `fit --in-dir <tmp>/collect --labels-dir <tmp>/label --out-dir <tmp>/fit --split probe_train` | **0** |
| `calibrate --in-dir <tmp>/fit --out-dir <tmp>/cal --split calibration` | **0** |
| `intervene --in-dir <tmp>/collect --out-dir <tmp>/intervene` | **0** |
| `repair --in-dir <tmp>/prep --out-dir <tmp>/repair --mask task_oracle` | **0** |
| `analyze --in-dir <tmp>/label --out-dir <tmp>/analyze` | **0** |

**接线实测（不是源码猜测）：**

| 阶段 | `input_hashes` | `upstream_manifest_ids` | 实际消费 |
|---|---|---|---|
| prepare | `{t1_tiny.json: 3267db38…}` | `[]` | 夹具 |
| collect | 上游目录全部文件 + `upstream_manifest`（9 键，与 prep 文件字节 **全等**） | `[ff4ecc93…]` = prep `manifest.digest` | 若有 `tasks.jsonl` 取第一行 Task，否则再读夹具；**不读** prepare traces/events；`features.npz` = prefix id 向量 |
| label | 同 collect，哈希 prep 全目录 | `[ff4ecc93…]` | 读 prepare `observations.jsonl` + `tasks.jsonl`；`build_labels` |
| fit | collect 目录文件（`features.npz`/`traces*`/`run_spec`/`upstream_manifest`） | `[cc805789…]` = collect digest | 读 `H`/`E` + **`--labels-dir` 的 labels**；**labels 不进 `input_hashes`** |
| calibrate | `{probes.jsonl, run_spec.json, upstream_manifest}` | `[a920258c…]` | 读第一条 probe `loss`，再拼字面量 `0.3, 0.4`，再 `one_minus_p` |
| intervene | 同 fit 的 collect 清单 | `[cc805789…]` | 读 `H[0]` 与 `H[min(1,n-1)]`（仅 1 行 → base=donor，`main_norm=0`）；效应字段 `null` |
| repair | 哈希 prep 全目录 | `[ff4ecc93…]` | 读 `traces.jsonl` 的 `token_ids`/`text`；`original_token_budget=21` |
| analyze | `{labels.jsonl, run_spec.json, upstream_manifest}` | `[7f9a7d43…]` | **不读** `labels.jsonl`；只找不存在的 `p1_table.jsonl`；`p1/p2/p3=null`；`status=not_evaluated` |

`collect` 无 `--in-dir` 仍 exit **0**，`input_hashes={}`，`upstream_manifest_ids=[]`。`analyze` 无 `--in-dir` 仍 exit **0**，`report.json` 与带 `--in-dir` 的报告 **字节全等**。

八个阶段 `manifest.digest` 均等于 `digest(body without digest)`。

`_upstream` 把 `manifest.digest` **字段**写入 `upstream_manifest_ids`，不重算、不校验该字段与文件体是否一致。

### 3.3 schema / shape / ID

默认 prepare 文件：`tasks.jsonl` `edits.jsonl` `splits.jsonl` `events.jsonl` `traces.jsonl` `observations.jsonl` `labels.jsonl` `run_spec.json` `manifest.json`。

Observation（精确一行）：

```text
{"alignment_ref": "{\"entity_or_expression\": \"q\", ...}", "edit_id": "edit:fix-t1-001:p2:2", "event_pair": ["q","q"], "node_id": "q", "observation_id": "obs:q:p2", "outcome": "changed", "premise_id": "p2", "raw_values": ["0","8"], "record_id": "obs:q:p2", "run_id": "prepare", "scan_state": "observed_response", ...}
```

默认编辑仍为 **p2:0→2**，`outcome=changed`，`raw_values=["0","8"]`。这是夹具上的有效扰动，**不是**科学全量扫描。

仍破裂的身份合同：

1. `events.jsonl` 两行 `record_id=""`, `run_id=""`, `base_group_id=""`。`Event.from_dict` 成功但身份仍空。
2. 两行 Task：`task_id` 分别为 `fix-t1-001` 与 `fix-t1-001::p2=2`，但 **`record_id` 均为 `fix-t1-001`**；`run_id=""`。
3. prepare/label 的 Label：`record_id=""`, `run_id=""`, `base_group_id=""`。第二行是 densities sidecar，不是 `Label`。
4. collect `traces.jsonl` 含额外键 `feature`、`weight_source`。`Trace.from_dict` → `TypeError: unexpected keyword argument 'feature'`。去掉未知键后可回载。
5. `features.npz` 键 `H`/`E`/`token_prefix`，形状 `[1,8]` / `[2,8]` / `[1]`，`float64`。`H[0]=[1,0,…]`（字符偏移假 token 的前缀），`E[0,0]=6`（`len("p1 = 4")`）。manifest `array_shapes` **无 dtype**。
6. `feature.pre_step.token_index=null`，`expressible=false`；`pre_value=3`，`post_step=4`；`weight_source=offline_prefix_ids`。
7. `RepairRecord` 无 `schema_version` / `record_id` / `run_id` / `base_group_id` / `status`。
8. 合成轨迹文本为 `"q = 0\n"` / `"q = 8\n"`（只渲染节点，不含前提句）。`token_ids = [1,2,3,4,5,6]`，不是模型 token。

### 3.4 配置 / 持久化 / 可复现性

- 两次独立 `prepare --split-seed 0`：`tasks/edits/splits/events/observations/labels/traces/run_spec/manifest` **九文件 hash 全等**。
- 两次 `fit`：`probes.jsonl` hash 全等（`loss=0.0005594629761805861`）。这是对 **prefix-id 向量** 的优化，不是隐状态复现。
- `write_run_spec(..., code_revision="latest")` → `ValueError("code_revision cannot use mutable identity 'latest'")`。
- 未知 `source_kind` → `ValueError("Unknown source_kind 'made_up'")`。
- `encode({"x": nan})` → `ValueError: Out of range float values are not JSON compliant`。
- cwd=`%TEMP%\rd-e-r3` 调用 `runtime_info()["git_revision"]`：**`46a6e26…`**。
- `packages.reasoning-diff = null`。
- 后段 `run_spec.rng` 仅为 `{"stream": "<stage>"}`，无 seed、无输入 digest。

### 3.5 恢复 / 分片

| 检查 | 退出码 | 结果 |
|---|---|---|
| CLI `--resume` | — | help 中存在（除 prepare 外与 `--in-dir` 一起） |
| CLI `--shard` | — | **不存在** |
| `completed_shard_ok` 生产调用 | — | 仅 `cli.py:280`：写出 `traces-shard-0000.jsonl` 后立刻用**自己刚算的 hash** assert（恒真） |
| collect shard | — | 与 `traces.jsonl` **字节相同**（hash `3cecd8d960aa…`）；不是按任务/组切分 |
| `--resume` 完整产物 | **0** | 文件 hash 不变 |
| `--resume` + 篡改 `traces.jsonl` | **1** | `ValueError: resume hash mismatch or missing file: traces.jsonl`；篡改保留；**不重算** |
| `--resume` + 删除 shard | **1** | `… traces-shard-0000.jsonl`；shard 仍缺失 |
| `--resume` + 删除 `observations.jsonl` | **1** | `… observations.jsonl`；观测仍缺失 |
| `--resume` + 新 `--edit-value 9` | **0** | edits hash **不变**；`run_spec.config.edit_value` 仍为 `2`（忽略新参数） |
| 无 `--resume` 重跑 prepare `--edit-value 9` | **0** | `edit_value=9`，`raw_values=["0","36"]` |
| `--resume` + 只改 `manifest.digest` 为 64 个 `0` | **0** | 不校验 digest 自洽；照常跳过 |

`_resume`（`cli.py:33-46`）实现为：有 `--resume` 且存在 `manifest.json` 后，对 `file_hashes` 逐项比对 `file_digest`。缺文件或 hash 变则抛 `ValueError`。不比对当前 CLI/run_spec，不重算 `manifest.digest`。

### 3.6 异常 / 资源

| 触发 | 退出 / 异常 | 清单 |
|---|---|---|
| `prepare --fixture` 指向不存在文件 | 进程 **1**，未捕获 `FileNotFoundError` | 先 `mkdir`（`cli.py:125`），留下**空目录** `badprep/`，无 `manifest.json` |
| `label` 无 `--in-dir` | **1** `FileNotFoundError: label requires --in-dir with observations.jsonl` | 无目录 |
| `fit --split test` | **1** `ValueError: probe fit cannot fit on test; expected ('probe_train',)` | 无产物 |
| `calibrate --split probe_train` | **1** `ValueError: calibration cannot fit on probe_train; expected ('calibration',)` | 无产物 |
| `fit --in-dir <prep>`（无 features.npz） | **1** `FileNotFoundError: fit requires features.npz from collect` | 无产物 |
| `--in-dir docs/SERVER_RUNBOOK.md` + collect | **1** `NotADirectoryError`（`_upstream` → `Path.iterdir`） | 留下 `features.npz` + 两条 traces，**无** `run_spec`/`manifest` |
| 同上 + calibrate / intervene / repair | **1** `NotADirectoryError` | 各留下对应 jsonl，无清单 |
| 同上 + analyze | **1** `NotADirectoryError` | 留下 `analysis.jsonl` + `report.json`，无清单 |
| 同上 + label | **1** `FileNotFoundError: label requires --in-dir with observations.jsonl` | 无目录 |
| 同上 + fit | **1** `FileNotFoundError: fit requires features.npz from collect` | 无目录 |
| `read_jsonl` 非法行 | `ValueError('.../bad.jsonl:1: invalid JSON')` | — |
| `IsolatedExecutor().submit(...)` | `NotImplementedError()` | — |
| `@forbid_host_exec` 包装函数 | `RuntimeError('host execution of model/dataset code is forbidden')` | 生产 CLI/评分未使用 |
| `write_manifest(..., {"tasks":10,"edits":3,"failure":0})` | `success_count=13` | 把记录数加总成成功数 |
| `write_npz` object 数组后 `read_npz` | 写出成功；读入 `ValueError('Object arrays cannot be loaded when allow_pickle=False')` | — |

资源：CLI 无超时/内存上限。`UnavailableExecutor.submit(..., limits={"timeout":1,"mem":1})` 仍只返回 `executor_unavailable`，`limits` 不进 `ExecutionResult`。`main` 无 try/except，失败不写 failure manifest。

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

`write_npz`（`io.py:82-97`）为 `mkstemp` → `np.savez(temp)` → `os.replace`。成功后无 `.feat.npz.*` 残留。写出 object 数组仍被允许，读回失败（§3.6）。

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 把 `tests/test_cli_pipeline.py` / 作者「70 passed」当验收 | 夹具烟测与绿测不是科学全跑；`test_pipeline_consumes_upstream` 不断言 input_hashes、Trace 回载或 `--labels-dir` |
| `pip install -e .` 后再测 `reasoning-diff` | 只读审查，不改环境；已证实未安装时 `python -m` 需 `PYTHONPATH=src` |
| 真实模型 / GPU / 官方数据下载 | 本机 `pending_server`；夹具烟测不得冒充 |
| 并发 shard 崩溃注入 | 无真实分片写入器；现有 shard 是 traces 副本 |
| 阅读本轮 A–D/F 报告 | 任务禁止；round-03 当时亦无他通道文件 |
| 修改生产代码或加回归测试 | 任务禁止 |

## 5. 发现

状态枚举：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。对 ISSUES 行：`closed` = 本通道独立确认关闭；`reopened` = 作者标 fixed 但本通道否决。

---

### E-01 后段 `input_hashes` / `upstream_manifest_ids` 已写入（closed，残留消费图）

- **严重度：** （原 high；残留 medium）
- **状态：** **closed**（空 provenance）。作者「CLI provenance hashes」在 **runbook 目录 `--in-dir` 路径**上独立成立：collect/label/fit/calibrate/intervene/repair/analyze 的 `input_hashes` 非空，且与上游文件字节一致；`upstream_manifest_ids[0]` 等于上游 `manifest.digest`。`test_pipeline_consumes_upstream` **仍不足以**证明消费图，但不阻止关闭「空字典」缺陷。
- **文件 / 符号 / 行号：** `cli.py` `_upstream` 49–61；`_write_stage` 84–111
- **残留（不重开空哈希，另见 E-14 / E-17）：**
  1. `_upstream` 是目录列举，不是实际读取集。collect 哈希 prepare `traces.jsonl` 但不读它；analyze 哈希 `labels.jsonl` 但不读它。
  2. `_upstream` 把 `digest` **字段**抄进 `upstream_manifest_ids`，不重算。
  3. 无 `--in-dir` 时 collect/analyze/repair/intervene 仍 exit 0 且 provenance 为空。
- **对应要求：** OPS-01；SERVER_RUNBOOK「Each stage writes run_spec.json, manifest.json」。
- **影响：** 目录级哈希现在可审计「读了哪个上游目录」；仍不能从清单推出「科学步骤消费了哪些记录」。

---

### E-02 默认 prepare 不再是 4×0 空操作（closed）

- **状态：** **closed**（保持）
- **证据：** `run_spec.config.edit_premise=p2`, `edit_value=2`；`outcome=changed`；`raw_values=["0","8"]`；编辑题 `answer_spec.value=8`。

---

### E-03 `--resume` 已校验清单 file_hashes（closed，残留 run_spec 与分片）

- **严重度：** （原 high；残留 high 仅分片 / medium 仅 run_spec）
- **状态：** **closed**（存在即跳过）。篡改 `traces.jsonl`、删除 shard、删除 `observations.jsonl` 后 `--resume` 均为 **exit 1**，`ValueError: resume hash mismatch or missing file: …`。作者「resume hashes」在 file_hashes 层面独立成立。
- **文件 / 符号 / 行号：** `cli.py` `_resume` 33–46
- **残留（不重开 hash 校验）：**
  1. `--resume --edit-value 9` 仍 exit **0**，忽略新 run_spec（§3.5）。
  2. 只改 `manifest.digest` 仍 exit **0**。
  3. 无 CLI `--shard`；`traces-shard-0000.jsonl` 与 `traces.jsonl` 字节相同；`completed_shard_ok` 仍自校验刚写出的文件（`cli.py:280`）。
  4. hash 失败只抛错，不重建、不写 failure manifest。
- **对应要求：** OPS-01「断点与分片」；ARCHITECTURE「恢复只复用与当前 run spec 一致且校验通过的完成 shard」。
- **影响：** 损坏产物不会再被当成完成阶段；换参数续跑仍会吞掉重算；长任务仍无真实分片。

---

### E-04 `report.json` 已进 analyze manifest（closed）

- **状态：** **closed**
- **证据：** `%TEMP%\rd-e-r3\analyze\manifest.json` 的 `file_hashes` 含 `analysis.jsonl`、`report.json`、`run_spec.json`。`cli.py` 461–462。

---

### E-05 schema / ID / shape 合同仍破裂

- **严重度：** high
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `schema.py` `Event` 192–217：无 `__post_init__` 填 `record_id`
  - `schema.py` `Trace.from_dict` 326–333：`cls(**data)`，拒未知键
  - `cli.py` 279 / 284：`trace.to_dict() | {"feature": feat, "weight_source": …}`
  - `edits.py` 120–129：保留旧 `record_id`
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

---

### E-07 `git_revision` 不再依赖进程 cwd（closed）

- **状态：** **closed**
- **文件 / 符号 / 行号：** `io.py` `runtime_info` 114–125
- **证据：** cwd=`%TEMP%\rd-e-r3` 仍得到 `46a6e26…` 与 `repo_root=C:\Users\22688\Desktop\diff`。

---

### E-08 `python -m reasoning_diff` 入口已存在（closed，残留未安装）

- **状态：** **closed**（模块入口）；未安装 console script 为环境事实，不是缺文件
- **文件 / 符号 / 行号：** `src/reasoning_diff/__main__.py` 1–4；`pyproject.toml` 15–16
- **证据：** §3.1。

---

### E-09 失败路径不落 failure manifest；`success_count` 缺省膨胀

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：**
  - `cli.py` `main` 504–507：无 try/except
  - `cli.py` `cmd_prepare` 125–126：先 `mkdir` 再读夹具
  - `cli.py` `_write_stage` 92–97：先写 jsonl 再 `_upstream`
  - `artifacts.py` 69：`success_count` 缺省加总
- **复现 / 证据：** §3.6。空 `badprep/`；`--in-dir` 文件路径留下半截产物；`success_count` 实验 = 13。
- **影响：** 调度器无法区分未跑、失败与半截目录；误把任务/编辑条数当成成功次数。

---

### E-10 隔离执行器无后端、limits 无效；host exec 未回退

- **严重度：** medium（缺后端 / limits）；host-exec 禁令本身 **未破**
- **状态：** confirmed defect（能力缺口）；禁止 host exec 为正确行为，见 §6
- **文件 / 符号 / 行号：** `executor.py` 22–33、49–59；`scoring.py` 19–30
- **复现 / 证据：** §3.7。
- **对应要求：** OPS-01 / EXEC-01 / SERVER_RUNBOOK Isolated code executor。

---

### E-11 后段「可复现」仍是 dummy 复现

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 269–277、360–375、439–462
- **复现 / 证据：** prepare 同机可复现（§3.4）。fit/analyze 数字稳定，因为输入是 prefix-id 与字面量维度，不是测量。analyze 带/不带 `--in-dir` 的 `report.json` **字节全等**。
- **影响：** 不能用后段 hash 证明科学步骤可重放。

---

### E-12 T2/T3/T4 适配器未进入用户 CLI

- **严重度：** medium
- **状态：** confirmed defect（入口缺失）
- **文件 / 符号 / 行号：** `cli.py` 466–500 仅 T1 fixture 的 prepare/collect
- **对应要求：** OPS-01 + DATA-02
- **复现 / 证据：** `--help` 只有八段通用命令；catalog loaders 无子命令。

---

### E-13 声称冻结 hash 与当前树一致（closed）

- **状态：** **closed**
- **文件：** `.planning/audits/round-03/VERSION.md`；55 个范围内文件
- **复现 / 证据：** §1。独立复算 = 声称值 `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`。

---

### E-14 collect 特征合同与模型采集路径仍断开

- **严重度：** high
- **状态：** confirmed defect。作者「collect prefix-id features」只替换了 `np.eye(4)`，**不能**关闭采集合同。
- **文件 / 符号 / 行号：**
  - `cli.py` 256–288：合成字符偏移 + `token_ids[:max(start,1)]` 填 `H`；`E` 用前提文本长度
  - `models/collect.py` 11–25：`collect_tiny` **无调用方**（CLI）
- **触发条件：** runbook `collect`
- **对应要求：** MODEL-01；OPS-01 采集阶段
- **复现 / 证据：** `weight_source=offline_prefix_ids`；`H[0]=[1,0,…]`；`pre_step` 不可表达；`Trace.from_dict` 失败。
- **影响：** fit/intervene 吃的是假 token 前缀，不是残差流。夹具烟测不能外推到权重。`I_4` 已不在默认产物中，但合同仍未接上。

---

### E-15 合成轨迹仍用节点捷径

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` 132–137、256；`events.py` `parse_fixture_events` 21–68
- **复现 / 证据：** 轨迹文本无 `p1`/`p2` 句；`surface_mentions=[]`。`task_set` 本轮已改 `anc.get(task.target)`，单节点夹具下为 `{p1,p2}`，不再取错列。
- **影响：** 有限扫描对象只有 `q`；不是完整前提事件扫描。

---

### E-16 `--in-dir` 指向文件时 `_upstream` 崩溃并留下半截产物

- **严重度：** medium
- **状态：** confirmed defect
- **文件 / 符号 / 行号：** `cli.py` `_upstream` 50–60（`in_dir.exists()` 对文件为真，随后 `iterdir`）
- **触发条件：** `--in-dir docs/SERVER_RUNBOOK.md`（或任意文件）
- **复现 / 证据：** §3.6。collect exit **1** `NotADirectoryError`；`col-file/` 含 `features.npz` + traces，无 manifest。analyze 留下 `report.json` + `analysis.jsonl`，无清单。
- **影响：** 误把文件当输入目录时，调度器看到半截「成功文件」且无 digest 可驳回。
- **建议：** `_upstream` 要求 `in_dir.is_dir()`；先校验再写；失败写 failure manifest。

---

### E-17 fit 消费 `--labels-dir` 但不记入 `input_hashes`

- **严重度：** medium
- **状态：** confirmed defect（E-01 关闭后的清单缺口）
- **文件 / 符号 / 行号：** `cli.py` `cmd_fit` 332–356：读 `labels_dir / "labels.jsonl"`；`_write_stage(..., in_dir=src)` 只哈希 collect 目录
- **触发条件：** runbook `fit --in-dir <collect> --labels-dir <label>`
- **复现 / 证据：** §3.2。`fit` 的 `input_hashes` 键为 `features.npz` / `traces*` / `run_spec` / `upstream_manifest`，**无** `labels.jsonl`。
- **影响：** 换一套标签重跑 fit，清单仍显示同一 collect 输入；无法从 run_spec 审计标签来源。

## 6. 非缺陷 / 经验证的正确行为

| 项 | 证据 |
|---|---|
| 冻结 hash 复现 | E-13 closed |
| JSON `allow_nan=False` | `encode(nan)` 抛 `ValueError` |
| `latest` 拒绝 | `write_run_spec(..., code_revision="latest")` → `ValueError` |
| 未知 `source_kind` 拒绝 | `ValueError("Unknown source_kind 'made_up'")` |
| JSONL 坏行带路径行号 | `bad.jsonl:1: invalid JSON` |
| 同机同参数 prepare 可复现 | 九文件 hash 全等 |
| 各阶段 `manifest.digest` 自洽 | §3.2 |
| runbook 目录 `--in-dir` 的文件哈希与上游字节一致 | §3.2 HASH VERIFY 全 True |
| `--resume` 拒绝被改/缺失的 file_hashes 项 | §3.5 exit 1 |
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
| label 拒绝无 `--in-dir` | exit 1 |

## 7. 外部待验证

| 项 | 状态 |
|---|---|
| Linux 隔离执行器、超时/cgroup、真实 HumanEval | `pending_server` |
| 真实 HF 权重、KV/hook、长链 collect | `pending_server`；`models/collect.py` 不在 CLI |
| 官方 iGSM / GSM / QA 全量快照 | 本机仅 fixture |
| 安装后 `reasoning-diff` console script | 本机未装 |

## 8. 结论

`python -m reasoning_diff` 按 runbook 八段 **全部退出码 0**。这只证明夹具烟测能写文件，**不证明** OPS-01 端到端工程成立，也 **不是** 科学全跑。

相对 round-02，本通道确认关闭：E-01 空 provenance、E-03 存在即跳过的 resume、E-13 冻结 hash。E-02 / E-04 / E-06 主缺陷 / E-07 / E-08 保持关闭。collect 默认产物不再是 `I_4`，改为 `offline_prefix_ids`（E-14 仍开）。`--in-dir` 目录路径上的 `input_hashes` 与上游字节一致；`--resume` 能拒绝被改文件。

仍不通过的核心缺陷：collect 未接模型采集（E-14）、schema/ID 破裂（E-05）、无真实分片且 resume 不比 run_spec（E-03 残留）、fit 漏记 `--labels-dir`（E-17）、文件 `--in-dir` 半截产物（E-16）、失败记账（E-09）、T2–T4 无 CLI（E-12）。

**本通道不通过** OPS-01。空通过或「测试绿了」不能作为本通道结论。作者「provenance/resume hashes」在本通道 **独立关闭其字面范围**；「prefix-id features」**不能**关闭采集合同。

下一步（建议，非本通道实施）：把 `--labels-dir` 与真实读取集写入 `input_hashes`；resume 比对当前 run_spec；collect 接到 `collect_tiny` 或明确标 `offline_prefix_ids` 为非测量；失败先写 failure manifest 再退出。
