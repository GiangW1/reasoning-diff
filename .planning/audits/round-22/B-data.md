# Review B — 数据与测量（独立审查，round-22）

本报告不假设实现正确，不把 `.planning/audits/ISSUES.md` 的作者关闭当作已关闭。未修改 `src/`、`tests/`、`pyproject.toml`。未阅读其他 round-22 通道报告。点名 CE 全部用 `.planning/audits/round-22/_b_scratch/oracle.py` 独立复跑，不 `import tests.*`。审查中对 `.planning/research/.cache/gsm_test_only_families.json` 做了隔离清空/写锁，结束后已恢复开审内容 `["gsm8k-12", "q:ada has 4 apples and buys 3 more. how many apples?"]`。r21 A–E PASS 不转移到本树。通道 PASS 不是 Goal 验收。不宣布 Goal 完成。

**冻结核验：`HASH_MATCH`。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data-r22`（独立 subagent，数据与测量通道，round-22） |
| review_time | `2026-09-21T03:39:00+08:00`（开读 / 复算 hash）— `2026-09-21T03:44:30+08:00`（交卷复算） |
| declared_frozen_hash | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（`.planning/audits/round-22/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`。61 文件。配方与 VERSION 原文一致（POSIX relpath + `\x00` + 文件字节）。 |
| 交卷复算 | **`HASH_MATCH`** 同一摘要，仍 61 文件。本通道未改生产树。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件与 `.planning/audits/round-22/_b_scratch/`） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭。F21-08 作者合取锁主张在本通道用独立 conjunctive lock 复验，关闭权仍归汇总通道。 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§4.1、§6 来源—数值、§7 T1–T4；`docs/EXPERIMENT_PROTOCOL.md` §2–3；GOAL §5 项 1–5；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02 |
| pytest_author_claim | VERSION 写 172 passed。本通道独立复跑 **`python -m pytest -q --tb=line` → 172 passed / 26.53s / exit 0**。绿 ≠ 论文正确。 |

## 2. 逐文件覆盖

`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度/八段烟测调用链而通读。行数与 SHA-256 为交卷时冻结树（与开审相同）。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 405 | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | full 1–405 | `sham:` → `noise_set=None`；未知/未扫描不进 \(M\)；`noise_ref=0` 不评估空 \(N\) |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`align_events` 按 key 配对 |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `ancestors={}` |
| `src/reasoning_diff/edits.py` | 367 | `cc8e2d23592a3ab89bdd9c889ee3cb3d559b0f01047d3ad5679aa09669725b51` | full 1–367 | 保留叶 *a*、追加等值 `src_b`；异于 rename |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | 六角色互斥；Plus 持久化锁；孤立从未 Plus 的 Symbolic 可 `probe_train` |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | `source_kind` 枚举；身份无值；`SCAN_STATES` |
| `src/reasoning_diff/cli.py` | 1268 | `cc5eae53d7be27eb87a2813290a5bae0ebda5006ced5897906c3e829d5da2df3` | callsite 257–437, 440–551, 687–700 | scientific prepare 密度；offline `H=token_ids[:8]`；scientific collect 拒 offline H |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173` | callsite 105–191 | scientific 轨迹 `weight_source=random_init`，`parse_status=constrained_target` |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38` | callsite | 本通道八段走 offline，不把它写成 MODEL-01 |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0` | callsite | 跨界 token 不进前瞻（本通道不重开） |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332` | callsite | 八段 token 前缀来源 |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G；加载重算；拒非 official |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | 拒 official 形状 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 无 sidecar → unknown；不注册 Plus 锁 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `solution_is_not_dag`；`register_test_only_family` |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 无图不冒充证明 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | supporting_facts 只进 metadata |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | `composition_reference`；`ancestors={}` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | `reference_dfg_is_not_task_dag` |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | 加载器不造图 |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite | 八段 `scientific_conclusion=None`；本通道不审 P1–P3 公式 |

夹具只读：`t1_tiny.json`、`t1_official_shape.json`、`t2_symbolic_one.json`、`t2_formula_sidecar.json`、`t2_gsmplus_one.json`、`t3_hotpot_one.json`、`t3_musique_pair.json`、`t3_humaneval_one.json`、`t4_boundary.json`。独立 JSON（非仓库夹具）：`_b_scratch/iso_symbolic.json`（Nora r22-0 / figs）、`iso_plus.json` / `samefam_symbolic.json`（Mia r22 / `gsm8k-r22-lock`）、`official_g_only.json`（仅 G、无 template）。

阶段目录：scientific prepare → `_b_scratch/stage_a/`；夹具八段 → `_b_scratch/stage_b/{fx,col,lab,fit,cal,int,rep,an}`。未使用 `prep` / `prepare` / `s-prep` 作为阶段名。

## 3. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审/交卷 **HASH_MATCH** 61 文件 `1f5f3798…` |
| X-00 | 作者 pytest | `python -m pytest -q --tb=line` | **172 passed / 26.53s / exit 0**。绿 ≠ 论文正确 |
| **H-official** | 官方 iGSM vs 夹具 `source_kind` | 官方 shape / 夹具 / 仅 G / `validate` | **通过。** §3.1 |
| **H-T2T3-DAG** | 不用答案 / supporting facts / 参考 DFG / CoT 冒充完整 DAG | 适配器 + `ancestors()` + `parse_events` | **通过。** §3.2 |
| **H-identity** | 对齐靠身份不靠值 | `EventIdentity` 字段 + `align_events` 值 7 vs 99 | **通过。** §3.3 |
| **H-sham-N** | `sham:` 行 `noise_set=None`；真实前提不继承 sham `noise_ref` | 构造标签 + `event_density_sets` | **通过。** §3.4 |
| **H-unknown-M** | 未知/未扫描不进 \(M\) | `unscanned` / `parse_failed` + helper | **通过。** §3.4 |
| **H-sci-sham** | scientific prepare 不得账面 `rho_M_excess=0.0/1.0` 且缺 `null_reason=noise_set_missing` | `cmd_prepare` → `stage_a`；独立合取锁；伪造 0.0 / 空 events / 账面 1.0 / 缺 reason | **通过。** §3.5 |
| **H-XOR** | 保留 *a*、等值 *b*、异于 rename | 库 API + scientific/fixture prepare 写出 pair | **通过。** §3.6 |
| **H-plus-iso** | Plus 持久化锁 vs 孤立从未 Plus 的 Symbolic | 独立 JSON；独立 SHA-256 分位；锁文件隔离后恢复 | **通过。** 孤立角色=`probe_train`。§3.7 |
| **H-split** | 六角色互斥；同族共组；泄漏可检出 | `assign_family` / `assert_disjoint` | **通过。** §3.7 |
| **H-8stage** | 夹具八段 offline H 是诚实烟测，不是 MODEL-01 | `stage_b` 八段 CLI；`H=token_ids[:8]`；scientific collect 拒 offline | **通过，不开缺陷。** §3.8 |
| X-t4 | 四态 | `load_t4` | 四态齐全，`source_kind=fixture` |
| X-lock | 锁文件恢复 | 开审文本对照 | 已恢复 |

独立 oracle：`python .planning/audits/round-22/_b_scratch/oracle.py` → **49/49 PASS**（`oracle_report.json`）。

### 3.1 官方 iGSM vs 项目夹具

GOAL §5.1 / DATA-01：官方与自建 DAG 分开；官方 \(R_{\mathrm{task}}\) 来自 template，不是 G。

- `load_igsm_snapshot(t1_official_shape.json)`：`source_kind=official`，`source=facebookresearch/iGSM`，`graph_kind=igsm_template`。lookup `q=99` 与结构图 `G` 被忽略；template `a * b` 重算 answer=`9`，mod=23。`source_kind=fixture` 调用官方加载器被拒。仅有 `G`、无 `template` 的独立 JSON 被拒：`Official iGSM R_task must come from template, not G`。
- `load_t1_fixture(t1_tiny.json)`：`source_kind=fixture`，`source=self_authored_arithmetic`。官方 shape 被拒：`T1 fixture loader requires source_kind=fixture`。把自建记录标成 `official` 时 `Task.validate` 拒绝：`Self-authored fixtures cannot be marked official`。
- `validate_t1_prepare_config`：ops={5,10,15,21}、n=500、mod=23。

### 3.2 T2/T3 不冒充完整 DAG

| 适配器 | graph_status | graph_kind | `ancestors()` | 备注 |
|---|---|---|---|---|
| GSM-Symbolic 无 sidecar | unknown | none | `{}` | 无节点；源码不含 `register_test_only_family` |
| Symbolic+公式 sidecar | partial | formula_sidecar | `{total:{a,b}}` | 独立标注，非答案铸造 |
| GSM-Plus | unknown | none | `{}` | `solution_is_not_dag`；`4+3=7` 文本 `parse_events` 空 |
| Hotpot | unknown | supporting_facts_only | `{}` | facts 仅 metadata；CoT「answer is France」不造节点 |
| MuSiQue | partial | composition_reference | `{}` | 分解节点存在（2 / 1）但不进 \(R_{\mathrm{task}}\) |
| HumanEval | unknown | none | `{}` | `reference_dfg_is_not_task_dag` |
| T2 no-op（无图） | unknown | none | `{}` | `answer_unchanged_proven=False` |
| T2 no-op（有图） | complete | arithmetic_dag | 目标祖先不含 `noop` | `recompute_and_ancestors` |

T4 四态齐全，全部 `source_kind=fixture`。

### 3.3 事件身份不含值

`EventIdentity` 字段只有 `entity_or_expression` / `occurrence_version` / `scope`。`key()` 是这三项的 JSON，不含 value。`align_events` 把值 `7` 与 `99`、同一身份的两条事件配成一对，`unaligned=[]`。

### 3.4 Sham 协议与未知不进 \(M\)

论文 §2.2、§2.6；PROTOCOL §2.4、§2.6–7；GOAL §5.3–5.4。

生产形态（p1 `changed` + p2 `no_change` + `sham:q` `changed`）：

- `noise_ref`：`p1=None`，`p2=None`，`sham:q=1.0`。真实前提不继承 sham 噪声。
- `event_density_sets`：`noise_set=None`，`null_reason=noise_set_missing`，`rho_*_excess=None`。

未知/未扫描：`unscanned` + `parse_failed` → `behavior_label=None`，`behavior_known=False`。事件密度 `behavior_unknown=true`，`M=[]`，`rho_M_raw=None`。helper 在 `behavior_unknown=True` 时同样清空 \(M\)。

真实前提全为 `noise_ref=0.0` 且无 `sham:`：走 else 分支，`noise_set=None`，`null_reason=noise_set_missing`，**不**把空集当已评估 \(N\)。对照：`dependency_densities(..., noise_set=[], noise_evaluated=True)` 会写出 `rho_M_noise=1.0`、`rho_M_excess=0.0`；prepare/label 的 `event_density_sets` 不走该分支。

### 3.5 Scientific prepare 合取锁（F21-08 独立复验）

`cmd_prepare(..., eval_mode=scientific, sham_opportunities=1)` 写入 `stage_a/`（exit 0，7 条轨迹）。`labels.jsonl`：

- 真实前提 `p1`/`p2`：`noise_ref=None`，`behavior_known=false`。
- `sham:q`：`noise_ref=1.0`。
- 事件密度：`noise_set=null`，`null_reason=noise_set_missing`，`M=[]`，`behavior_unknown=true`，全部 `rho_*_excess` / `rho_*_noise` 为 null。
- 聚合层 `aggregation=mean_over_events` 的 `null_reason` 为 null（无事件均值可写），但 **没有账面 `rho_M_excess=0.0` 或 `1.0`**。

独立合取锁（不过作者测试）：顶层 excess/noise 皆为 None，**且**每个事件行 `null_reason==noise_set_missing`。活体密度通过。伪造攻击：

| 伪造 | 合取锁 | 弱析取 `excess != 1.0 or null_reason` |
|---|---|---|
| `rho_M_excess=0.0` | 失败 | 仍绿（`None != 1.0` / `0.0 != 1.0`） |
| `events=[]` | 失败 | 仍绿 |
| 事件行账面 `rho_M_excess=1.0` 且借口 `null_reason=noise_set_missing` | 失败 | — |
| 事件行 `null_reason=None` | 失败 | — |

旧 `!= 1.0 or null_reason` **不能**单独关闭本猎项。这是对作者 F21-08 主张的独立复验，不是采信 ISSUES 关闭。

scientific 轨迹 `weight_source=random_init`，`parse_status=constrained_target`：**不是** MODEL-01，也不是 §4.1 自然 CoT。不开缺陷。

### 3.6 XOR 来源（保留 *a*，等值 *b*，异于 rename）

论文 §6 / GOAL §5.2。`apply_alt_source_same_value(t1_tiny, p2)`：

- 来源臂：`premises=["p1","p2","src_b"]`，`p2.value==src_b.value=="0"`，`q.parents=["p1","src_b"]`，`kind=same_value_diff_source`。题干仍含 `p2 = 0` 并追加 `src_b = 0`。
- `apply_rename_edit({p2:src_b})`：`premises=["p1","src_b"]`（丢掉 *a*），`kind=rename`。
- 两臂不同构。scientific 与夹具 prepare 均写出 `source_value_pair`，`src_ids=["p1","p2","src_b"]`，`targets=["q"]`。

### 3.7 Plus 锁与划分互斥

独立 SHA-256 分位选中从未见 Plus 的 Symbolic（`original_id=iso-r22-never-plus`，题干 Nora r22-0 / figs）：`split_for_task` = **`probe_train`**，与本通道手算 `assign_split` 哈希一致，未被强制 `test`。

加载独立 Plus（Mia r22 / `gsm8k-r22-lock`）后：Plus 与同族 Symbolic 均为 `test`，`fit_eligible=False`。另一孤立族仍为 `probe_train`。锁文件已恢复开审内容。

六角色 `probe_train/dev/direction_fit/calibration/transfer_pairs/test`，分数和为 1。`assign_family` 同族同角色。七个独立族写入角色桶后 `assert_disjoint` 通过；把 `probe_train` 成员注入 `test` 后 `assert_disjoint` 抛错。

### 3.8 夹具八段 offline H（诚实烟测，不开缺陷）

`stage_b` 八段（prepare→collect offline→label→fit→calibrate→intervene→repair→analyze）全部 exit 0。collect：

- `H.shape==(1,8)`，`H[0]==[1,2,3,4,5,6,7,8]`，等于 `token_ids[:8]`。
- `weight_source=offline_prefix_ids`，`backend=offline`。
- `report.scientific_conclusion is None`，Gate 0 = `unregistered`。

这是夹具离线前缀烟测，**不是** MODEL-01，也不是真实隐状态。按任务口径 **不开成缺陷**。对照：`collect --eval-mode scientific --backend offline` 拒绝：`scientific collect refuses offline_prefix_ids as H`。

## 4. 发现

点名 CE **无已确认缺陷**。下列为额外观察，**不**把作者 ISSUES 行标为已关闭，也 **不**把诚实烟测升为 FAIL。

### B22-obs-1 — 聚合层 `null_reason` 可空（观察，非点名失败）

| 字段 | 值 |
|---|---|
| 严重度 | 观察 / 聚合字段语义 |
| 状态 | 已证实；事件层合取成立，不是本轮点名 CE 失败 |
| 位置 | `measure.py` `dependency_densities` 聚合支 112–116；`stage_a/labels.jsonl` 密度行 |
| 证据 | 事件行 `null_reason=noise_set_missing` 且 excess 全 null；聚合层 `null_reason=None`（`mean_over_events` 不复制事件原因）。弱析取对伪造 `rho_M_excess=0.0` 仍绿 |
| 影响 | 读聚合行不能单独当作「已声明 noise_set_missing」。本冻结事件层未账面 0.0/1.0 |
| 建议 | 科学报告读 `events[]`；测试锁必须合取事件 `null_reason` |

### B22-obs-2 — 八段 / tiny 约束轨迹不是 MODEL-01（诚实项）

夹具八段 H 来自 `token_ids[:8]`。scientific prepare 七条轨迹均为 `random_init` + `constrained_target`。把它们写成官方权重或 §4.1 自然 CoT 才是缺陷；当前产物没有那样写。**不开缺陷。**

未把上述两项升为 FAIL：点名 CE 通过；二者是聚合字段/证据边界，不是本冻结上「官方/夹具分离 / T2T3 不造完整 DAG / 身份不含值 / sham 空 N / 未知不进 M / scientific 不合账 0.0·1.0 / XOR 保留 a / Plus 锁 / 划分互斥」的反例。

## 5. 未执行 / 边界

- 真实 HF 权重、官方 dump、CUDA、长链 CoT、人工复核回填：`pending_server`。
- 未跑完整 scientific prepare→tiny collect→fit 端到端（属 E/D 通道）；本通道用库 API + scientific `cmd_prepare` + 夹具八段 + scientific collect 拒 offline。
- 未把 `ISSUES.md` 作者关闭当作独立关闭。F21-08/12 属 F 通道；本通道只复验数据/测量合取与 XOR/划分。关闭权仍归汇总通道。
- r21 A–E PASS、旧 hash `5097c831…` 的结论不转移到本树。
- 连续通过计数仍为 0。本通道单独不得启动连续通过。

## 6. 结论

| 项 | 裁决 |
|---|---|
| 冻结核验 | **HASH_MATCH** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（61） |
| pytest | 172 passed（独立复跑；绿 ≠ 论文正确） |
| 点名 CE | 全部通过（独立 oracle 49/49 + scientific `stage_a` + 夹具 `stage_b` 八段） |
| 已确认范围内缺陷 | 无 |
| **通道结论** | **PASS** |
| Goal / 连续通过 | **不是 Goal 验收。不宣布 Goal 完成。不得开始连续通过计数。** |

GOAL §5.1–5.5 在本机数据/测量范围内：官方与 fixture 分离；T2/T3 不以答案/supporting facts/参考 DFG/CoT 冒充完整事件 DAG；对齐靠身份不靠值；未知/未扫描不进 \(M\)；`sham:` 行保持 `noise_set=None`，真实前提不继承 sham `noise_ref`；scientific prepare 事件密度 excess 为 null 且 `null_reason=noise_set_missing`，独立合取锁拒绝伪造 0.0 / 空 events / 账面 1.0；来源—数值是保留 *a*、追加 `src_b` 的 XOR，不是 rename；同族共组与 Plus 测试锁成立，孤立从未 Plus 的 Symbolic 可为 `probe_train`；六划分角色互斥。夹具八段 offline H 是诚实烟测，不是 MODEL-01。
