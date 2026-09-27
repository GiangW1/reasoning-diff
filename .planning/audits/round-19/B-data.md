# Review B — 数据与测量（独立审查，round-19）

本报告不假设实现正确，不把 `.planning/audits/ISSUES.md` 的作者关闭当作已关闭。未修改 `src/`、`tests/`、`pyproject.toml`。未阅读其他 round-19 通道报告。点名 CE 全部用 `.planning/audits/round-19/_b_scratch/oracle.py` 独立复跑，不 `import tests.*`。审查中对 `.planning/research/.cache/gsm_test_only_families.json` 做了隔离清空/写锁，结束后已恢复开审内容 `["gsm8k-12", "q:ada has 4 apples…"]`。

**冻结核验：`HASH_MATCH`。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data-r19`（独立 subagent，数据与测量通道，round-19） |
| review_time | `2026-09-21T03:09:00+08:00`（开读 / 复算 hash）— `2026-09-21T03:15:33+08:00`（交卷复算） |
| declared_frozen_hash | `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`（`.planning/audits/round-19/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`。61 文件。配方与 VERSION 原文一致（POSIX relpath + `\x00` + 文件字节）。 |
| 交卷复算 | **`HASH_MATCH`** 同一摘要，仍 61 文件。本通道未改生产树。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件与 `.planning/audits/round-19/_b_scratch/`） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§4.1、§6 来源—数值、§7 T1–T4；`docs/EXPERIMENT_PROTOCOL.md` §2–3；GOAL §5 项 1–5；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02 |
| pytest_author_claim | VERSION 写 165 passed。本通道独立复跑 **`python -m pytest -q --tb=line` → 165 passed / 20.05s / exit 0**。绿 ≠ 论文正确。 |

## 2. 逐文件覆盖

`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度/E 列调用链而通读。行数与 SHA-256 为交卷时冻结树（与开审相同）。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 405 | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | full 1–405 | 未知行为不进 \(M\)；`sham:` → `noise_set=None`；`noise_ref=0` 不评估空 \(N\) |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`graph_status!=complete` 且空父母 → 未知 |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `ancestors={}` |
| `src/reasoning_diff/edits.py` | 367 | `cc8e2d23592a3ab89bdd9c889ee3cb3d559b0f01047d3ad5679aa09669725b51` | full 1–367 | 保留叶 *a*、追加等值 `src_b`；`_rewrite_ids` 一次替换（重叠改名） |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | Plus 持久化锁；孤立从未 Plus 的 Symbolic 可 `probe_train` |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | `scan_state` / placeholder / 身份 |
| `src/reasoning_diff/cli.py` | 1267 | `95c58b934e1aceebc58b4e076b2a416ad176626e65bd15f7c254c750d5722906` | callsite 257–578, 616–740, 752–831 | 标注/配对；`_find_tasks_jsonl` / `_find_labels_jsonl` 只读给定目录；`_e_premise_ids` |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38` | callsite 25–93 | `E` 按传入 `premises` 顺序 span-mean |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173` | callsite 101–191 | `task_prompt=question`；解析只用已有 alias |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0` | callsite | 跨界 token 不进前瞻 |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332` | callsite | `span_token_indices` 只收全包含 |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G；加载重算 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | 拒 official 形状 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 无 sidecar → unknown；不注册 Plus 锁 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `solution_is_not_dag`；`register_test_only_family` |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 注入非祖先；无图不冒充证明 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | supporting_facts 只进 metadata |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | `composition_reference`；`ancestors={}` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | `reference_dfg_is_not_task_dag` |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | 加载器不造图 |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite | 本通道不审 P1–P3 公式细节 |

夹具只读：`t1_tiny.json`、`t1_official_shape.json`、`t2_symbolic_one.json`、`t2_formula_sidecar.json`、`t2_gsmplus_one.json`、`t3_hotpot_one.json`、`t3_musique_pair.json`、`t3_humaneval_one.json`、`t4_boundary.json`。独立 JSON（非仓库夹具）：`_b_scratch/iso_symbolic.json`（Nora r19-0 / plums）、`iso_plus.json` / `samefam_symbolic.json`（Mia r19 / lockfam-r19）。

## 3. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审/交卷 **HASH_MATCH** 61 文件 `b6db632f…` |
| X-00 | 作者 pytest | `python -m pytest -q --tb=line` | **165 passed / 20.05s / exit 0** |
| **H-XOR** | 保留 *a*、等值 *b*、异于 rename | 库 API + fixture `prepare` | **通过。** §3.1 |
| **H-sim-rename** | 重叠改名一次替换，禁止顺序塌缩 | 独立 token 映射 vs `_rewrite_ids` / `apply_rename_edit` | **通过。** §3.2 |
| **H-unknown-M** | 未知/未扫描不进 \(M\) | `build_labels` + `event_density_sets` | **通过。** §3.3 |
| **H-sham-N** | 任一 `sham:` 行 `noise_set=None` | 构造标签 + `build_labels` + CLI prepare | **通过。** §3.4 |
| **H-noise0** | 真实前提 `noise_ref=0` 且无 sham 不评估空 \(N\) | `event_density_sets` / 直接 API | **通过。** §3.4 |
| **H-find** | `_find_tasks_jsonl` / `_find_labels_jsonl` 只读给定目录 | `inspect` + 兄弟 `prep`/`lab`/`label`/`labels` / 子目录 `lab` | **通过。** §3.5 |
| **H-pair-bind** | `_load_source_value_pair` 只读 `in-dir/edits.jsonl` | `inspect` + 兄弟 `prep` | **通过。** §3.5 |
| **H-plus-iso** | Plus 持久化锁 vs 孤立从未 Plus 的 Symbolic | 独立 JSON；独立 SHA-256 分位；锁文件隔离后恢复 | **通过。** 孤立角色=`probe_train`。§3.6 |
| **H-E-order** | E 列跟随 `task.premises` 而非 labels 先见序 | `_e_premise_ids` + `collect_hidden_trace` + `cmd_fit` 拒缺 tasks | **通过。** §3.7 |
| **H-T2T3-DAG** | 不用答案 / supporting facts / 参考 DFG / CoT 冒充完整 DAG | 适配器 + `ancestors()` + CoT 解析 | **通过。** §3.8 |
| X-id | 对齐靠身份不靠值 | `align_events` 值 7 vs 99 | 成对，值不同 |
| X-t1 | 官方 template≠G；fixture 拒 official | 夹具加载 | official answer=9；fixture 抛错 |
| X-t4 | 四态 | `load_t4` | 四态齐全 |
| X-deep | 深层 DAG 上 XOR | 合成 mid→q | `_try_source_value_pair` 返回 None（限制，见 §4） |

独立 oracle：`python .planning/audits/round-19/_b_scratch/oracle.py` → **47/47 PASS**（`oracle_report.json`）。CLI 烟测：`cmd_prepare` fixture + `sham_opportunities=1` → `edits.jsonl` 含 `source_value_pair`，`src_ids=["p1","p2","src_b"]`，`q.parents=["p1","src_b"]`，1 条 `sham:` 标签，密度 `noise_set=null`、`M=[]`、`behavior_unknown=true`。

### 3.1 XOR 来源（保留 *a*，等值 *b*，异于 rename）

论文 §6 / GOAL §5.2：等值不同来源。实现：`apply_alt_source_same_value`（`edits.py` 221–294）。

对 `t1_tiny` 编辑 `p2`：

- 来源臂：`premises=["p1","p2","src_b"]`，`p2.value==src_b.value=="0"`，`q.parents=["p1","src_b"]`，`kind=same_value_diff_source`。
- `apply_rename_edit({p2:src_b})`：`premises=["p1","src_b"]`（丢掉 *a*），`kind=rename`。
- 两臂不同构。CLI `prepare` 写出 `source_value_pair`，与库结果一致。

### 3.2 同时重叠改名

独立期望：标识符按**原串**一次性映射，禁止顺序二次替换。对 `t1_tiny` 题干 `p1 = 4. p2 = 0. What is q = p1 * p2?`：

| 映射 | 一次替换（期望） | 顺序替换（反例） |
|---|---|---|
| `{p1:p2, p2:p1}` | `p2 = 4. p1 = 0. What is q = p2 * p1?` | p1 先：全塌成 `p1`；p2 先：全塌成 `p2` |
| `{p1:p2, p2:p3}` | `p2 = 4. p3 = 0. What is q = p2 * p3?` | 全塌成 `p3` |
| `{p1:p10, p10:p1}` | `p10 = 1. p1 = 2. What is q = p10 * p1?` | 前缀重叠塌缩 |

`_rewrite_ids` 与 `apply_rename_edit` 均命中一次替换：交换后前提身份 `p2=4` / `p1=0`，`q.parents=["p2","p1"]`，`expression="p2 * p1"`，答案不变。这是对作者 F18-03 主张的**独立复验**，不是采信 ISSUES 关闭。

### 3.3 未知 / 未扫描不得成为 \(M\)

论文 §2.2、§4.1；PROTOCOL §2.4；GOAL §5.3。`build_labels` 仅在 `outcome=changed` 或（`no_change` ∧ `exhaustive` ∧ `observed_response`）时给出已知行为。`unscanned` / `unknown` / `parse_failed` / 非穷尽 `no_change` → `behavior_label=None`。`event_density_sets` 在 `behavior_unknown` 时 `M=[]`。`dependency_densities(..., behavior_unknown=True)` 清空 \(M\)；同一集合在 `behavior_unknown=False` 且 \(B=\emptyset\) 时才会得到 \(M=T\)。CLI sham prepare 密度同样 `M=[]`。

### 3.4 `sham:` 与 `noise_ref=0`

论文 §2.6 / PROTOCOL §2.6–7。任一 `sham:` 行：`event_density_sets` 置 `noise_set=None`，`rho_*_excess=None`，`null_reason=noise_set_missing`。由 `rng_pair=sham:` 观察经 `build_labels` 生成的 `sham:` 行同样空 \(N\)。真实前提全为 `noise_ref=0` 且无 `sham:`：走 `else` 分支，`noise_set=None`，**不**把空集当已评估 \(N\)。直接 API `noise_set=[]` 且 `noise_evaluated=False` → `null_reason=noise_set_empty`。对照：`evaluated=True` 的空 \(N\) 会把噪声参照记成 0（本冻结的 `noise_ref=0` 路径不走该分支）。

### 3.5 目录绑定

`_find_stage_file` / `_find_tasks_jsonl` / `_find_labels_jsonl` 源码只检查传入目录下的同名文件，无 `rglob` / `parent` / `prep` / `lab`。空 `given/` 不绑定：

- 兄弟 `prep/tasks.jsonl`、`lab/labels.jsonl`、`label/labels.jsonl`、`labels/labels.jsonl`
- 父目录 `tasks.jsonl` / `labels.jsonl`
- 子目录 `given/lab/labels.jsonl`

`cmd_calibrate` 源码只把 `_find_labels_jsonl(labels_dir, src, feat_dir)` 当作查找；无 `src.parent`、无字面量 `"lab"` / `"label"` 兄弟行走。`_find_labels_jsonl(None, cal_src, cal_feat)` 在仅有兄弟 `lab/labels.jsonl` 时返回 `None`。

`_load_source_value_pair` 只读 `Path(src)/edits.jsonl`。collect 目录无该文件时，兄弟 `prep/edits.jsonl` 的 `source_value_pair` **不绑定**；写入本目录后才绑定 `mark=GIVEN`。

### 3.6 Plus 锁 vs 孤立 Symbolic

独立 SHA-256 分位选中从未见 Plus 的 Symbolic（`original_id=iso-r19-never-plus`，题干 Nora r19-0 / plums）：`split_for_task` = **`probe_train`**，与本通道手算 `assign_split` 哈希一致，未被强制 `test`。

加载独立 Plus（Mia r19 / `lockfam-r19`）后：Plus 与同族 Symbolic 均为 `test`，`fit_eligible=False`。另一孤立族仍为 `probe_train`。锁文件已恢复开审内容。

### 3.7 E 列顺序

`_e_premise_ids`：标签先见序为 `p2,p1,sham:q` 时，输出仍为 `["p1","p2"]`，不含 `sham:`。`collect_hidden_trace` 对 `t1_tiny` 得 `E.shape=(2,32)`，与 `task.premises` 等长。`cmd_fit` 在缺 `tasks.jsonl` 仅有 labels 时拒绝：`fit requires tasks.jsonl so E columns follow task.premises, not label order`。

### 3.8 T2/T3 不冒充完整 DAG

| 适配器 | graph_status | graph_kind | `ancestors()` | 备注 |
|---|---|---|---|---|
| GSM-Symbolic 无 sidecar | unknown | none | `{}` | 无节点 |
| GSM-Plus | unknown | none | `{}` | `solution_is_not_dag` |
| Hotpot | unknown | supporting_facts_only | `{}` | facts 仅 metadata |
| MuSiQue | partial | composition_reference | `{}` | 分解节点存在但不进 \(R_{\mathrm{task}}\) |
| HumanEval | unknown | none | `{}` | `reference_dfg_is_not_task_dag` |
| Symbolic+公式 sidecar | partial | formula_sidecar | `{total:{a,b}}` | 独立标注，非 CoT |
| Hotpot + CoT 文本 | — | — | — | `parse_events` 空，不造节点 |

官方 iGSM：template 重算 answer=9，忽略 `G`/`lookup`。fixture 加载器拒 official 形状。

## 4. 发现

点名 CE **无已确认缺陷**。下列为额外观察，**不**把作者 ISSUES 行标为已关闭。

### B19-obs-1 — 深层 DAG 上 XOR 构造失败（限制，非点名失败）

| 字段 | 值 |
|---|---|
| 严重度 | 观察 / 构造覆盖缺口 |
| 状态 | 已证实限制，不是本轮点名 CE 失败 |
| 位置 | `edits.py` `apply_alt_source_same_value` 270–271；`cli.py` `_try_source_value_pair` 697–700 |
| 触发 | 目标直接父母不含被改叶子（`mid→q`，改 `p2`） |
| 证据 | oracle `X-XOR-deep-dag-limitation`：`ValueError: same_value_diff_source must change required sources`；`_try_source_value_pair` → `None`（静默不写 pair） |
| 原文 | §6 来源—数值解耦；官方 iGSM 常有多跳 |
| 影响 | 叶为 target 直接父母时（`t1_tiny`、官方 shape `q←a,b`）点名 CE 成立。更深图不产 `source_value_pair`，intervene 可能落到 `same_identity_fallback` |
| 建议 | 用祖先集合而非仅 `_target_parents` 判定来源是否改变；或对失败显式记录 |

### B19-obs-2 — T3 Hotpot 前提 span 相对题干，不相对文档（限制）

| 字段 | 值 |
|---|---|
| 严重度 | 观察 / tiny collect 下 T3 E 内容不可当作文档嵌入 |
| 状态 | 已证实测量限制；**不**否定「E 列顺序跟随 `task.premises`」 |
| 位置 | `t3_hotpot.py` 41–47；`collect.py` 72–78 |
| 证据 | 三句 premise 均 `start=0`；`text not in question`；`span_token_indices` 池化的是题干前缀 |
| 原文 | §2.2 列索引为原始输入前提 |
| 影响 | 列顺序正确，但 tiny/question-only prompt 下 E 不是文档句向量。真实 HF 轨迹若仍只用 `task.question` 则同样缺上下文 |
| 建议 | 科学 collect 须把 context 编进可对齐 span；当前不得宣称 T3 探针 E 已对齐文档 |

未把上述两项升为 FAIL：点名 CE 通过，且二者是覆盖/后端边界，不是本冻结上「保留 a / 同时重叠改名 / 未知不进 M / sham 空 N / 目录绑定 / Plus 锁 / E 列序 / 不造完整 DAG」的反例。

## 5. 未执行 / 边界

- 真实 HF 权重、官方 dump、CUDA、长链 CoT、人工复核回填：`pending_server`。
- 未跑完整 scientific prepare→collect→fit 端到端（属 E 通道）；本通道用库 API + fixture `cmd_prepare` / `cmd_fit` 拒写。
- 未把 `ISSUES.md` 作者关闭当作独立关闭。F18-03 / F18-12 / A14-02 / A14-04 的行为在本冻结上被独立复验，关闭权仍归汇总通道。

## 6. 结论

| 项 | 裁决 |
|---|---|
| 冻结核验 | **HASH_MATCH** `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`（61） |
| pytest | 165 passed（独立复跑） |
| 点名 CE | 全部通过（独立 oracle 47/47 + prepare 烟测） |
| 已确认范围内缺陷 | 无 |
| **通道结论** | **PASS** |

GOAL §5.1–5.5 在本机数据/测量范围内：官方与 fixture 分离；T2/T3 不以答案/supporting facts/参考 DFG/CoT 冒充完整事件 DAG；未知/未扫描不进 \(M\)；噪声缺协议或 `sham:` / `noise_ref=0` 时 excess 为 null；同族共组与 Plus 测试锁成立，孤立从未 Plus 的 Symbolic 可为 `probe_train`；重叠改名按原串一次替换，不顺序塌缩；tasks/labels 查找只绑定给定目录。
