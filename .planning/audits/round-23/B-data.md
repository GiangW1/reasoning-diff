# Review B — 数据与测量（独立审查，round-23）

本报告不假设实现正确，不把 `.planning/audits/ISSUES.md` 的作者关闭当作已关闭。未修改 `src/`、`tests/`、`pyproject.toml`。未阅读其他 round-23 通道报告。未把 `.planning/audits/round-22/{A,B,C,D,E,F}-*.md` 当作本树证据。点名 CE 全部用 `.planning/audits/round-23/_b_scratch/oracle.py` 独立复跑，不 `import tests.*`。审查中对 `.planning/research/.cache/gsm_test_only_families.json` 做了隔离清空/写锁，结束后已恢复开审内容 `["gsm8k-12", "q:ada has 4 apples and buys 3 more. how many apples?"]`。CLI 阶段目录只用 `stage_a` / `stage_b`，不用 `prep` / `prepare` / `s-prep`。绿 pytest ≠ 论文正确。通道 PASS ≠ Goal 接受。

**冻结核验：`HASH_MATCH`。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data-r23`（独立 subagent，数据与测量通道，round-23） |
| review_time | `2026-09-21T03:48:00+08:00`（开读 / 复算 hash）— `2026-09-21T03:53:50+08:00`（交卷复算） |
| declared_frozen_hash | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（`.planning/audits/round-23/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`。61 文件。配方与 VERSION 原文一致（POSIX relpath + `\x00` + 文件字节）。 |
| 交卷复算 | **`HASH_MATCH`** 同一摘要，仍 61 文件。本通道未改生产树。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件与 `.planning/audits/round-23/_b_scratch/`） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§4.1、§6 来源—数值、§7 T1–T4；`docs/EXPERIMENT_PROTOCOL.md` §2–3；GOAL §5 项 1–5；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02 |
| pytest_author_claim | VERSION 写 172 passed。本通道独立复跑 **`python -m pytest -q --tb=line` → 172 passed / 29.05s / exit 0**。绿 ≠ 论文正确。 |

## 2. 逐文件覆盖

`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度/E 列调用链而通读。行数与 SHA-256 为交卷时冻结树（与开审相同）。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 405 | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | full 1–405 | 未知/未扫描不进 \(M\)；`sham:` → `noise_set=None`；真实前提不继承 sham `noise_ref`；`noise_ref=0` 不评估空 \(N\) |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`graph_status!=complete` 且空父母 → 未知 |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `ancestors={}` |
| `src/reasoning_diff/edits.py` | 367 | `cc8e2d23592a3ab89bdd9c889ee3cb3d559b0f01047d3ad5679aa09669725b51` | full 1–367 | 保留叶 *a*、追加等值 `src_b`；`_rewrite_ids` 一次替换 |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | Plus 持久化锁；六角色互斥；孤立从未 Plus 的 Symbolic 可 `probe_train` |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | `source_kind` / `scan_state` / 身份不含值 |
| `src/reasoning_diff/cli.py` | 1268 | `cc5eae53d7be27eb87a2813290a5bae0ebda5006ced5897906c3e829d5da2df3` | callsite 94–437, 440–575, 687–831 | scientific/fixture prepare 密度；`stage_a`/`stage_b` 绑定；offline H 标烟测 |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38` | callsite 25–93 | `E` 按传入 `premises` 顺序 span-mean |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173` | callsite 101–191 | `task_prompt=question`；解析只用已有 alias |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0` | callsite | 跨界 token 不进前瞻 |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332` | callsite | `span_token_indices` 只收全包含 |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G；加载重算；`source_kind=official` |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | 拒 official 形状与 official 标记 |
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

夹具只读：`t1_tiny.json`、`t1_official_shape.json`、`t2_symbolic_one.json`、`t2_formula_sidecar.json`、`t2_gsmplus_one.json`、`t3_hotpot_one.json`、`t3_musique_pair.json`、`t3_humaneval_one.json`、`t4_boundary.json`。独立 JSON（非仓库夹具）：`_b_scratch/iso_symbolic.json`（Nora r23-5 / figs）、`iso_plus.json` / `samefam_symbolic.json`（Mia r23 / gsm8k-r23-lockfam）。

## 3. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审/交卷 **HASH_MATCH** 61 文件 `1f5f3798…` |
| X-00 | 作者 pytest | `python -m pytest -q --tb=line` | **172 passed / 29.05s / exit 0**。绿 ≠ 论文正确 |
| **H-official** | 官方 iGSM vs 项目夹具 `source_kind` | 官方 shape / fixture / 伪造 official 标记 | **通过。** §3.1 |
| **H-T2T3-DAG** | 不用答案 / supporting facts / 参考 DFG / CoT 冒充完整 DAG | 适配器 + `ancestors()` + CoT 解析 | **通过。** §3.2 |
| **H-id** | 事件身份不含值 | `EventIdentity` 字段 + `align_events` 7 vs 99 | **通过。** §3.3 |
| **H-unknown-M** | 未知/未扫描不进 \(M\) | `build_labels` + `event_density_sets` | **通过。** §3.4 |
| **H-sham-N** | `sham:` 行 `noise_set=None`；真实前提不继承 sham `noise_ref` | 构造标签 + fixture/scientific prepare | **通过。** §3.4–3.5 |
| **H-sci-sham** | scientific prepare 不得把 `rho_M_excess` 记成 0.0/1.0 且缺少 `null_reason=noise_set_missing` | `stage_a` scientific prepare `--sham-opportunities 1` | **通过。** §3.5 |
| **H-XOR** | 保留 *a*、等值 *b*、异于 rename | 库 API + fixture `prepare` | **通过。** §3.6 |
| **H-plus-iso** | Plus 测试专用族锁 vs 孤立从未 Plus 的 Symbolic | 独立 JSON；独立 SHA-256 分位；锁文件隔离后恢复 | **通过。** 孤立角色=`probe_train`。§3.7 |
| **H-split** | 六角色互斥、同族共组 | `assign_family` / `assert_disjoint` / `source=gsm_plus` | **通过。** §3.7 |
| **H-find** | `_find_*` 只读给定 `stage_a`/`stage_b` | `inspect` + 空 `stage_b` 对兄弟 `stage_a` | **通过。** §3.8 |
| **H-offline-H** | fixture 离线 H 是诚实烟测，不是 MODEL-01 | fixture collect `--backend offline`；scientific 拒 offline | **通过，不升缺陷。** §3.9 |
| X-t1-config | op/n/mod | `validate_t1_prepare_config` | ops={5,10,15,21}、n=500、mod=23 |
| X-t4 | 四态 | `load_t4` | 四态齐全，`source_kind=fixture` |
| X-sim-rename | 重叠改名一次替换 | 手写期望 vs `_rewrite_ids` | 通过 |
| X-E-order | E 列跟随 `task.premises` | `_e_premise_ids` | `["p1","p2"]`，不含 `sham:q` |
| X-deep | 深层 DAG 上 XOR | 合成 mid→q | `_try_source_value_pair` → None（限制，见 §4） |
| X-lock | 锁文件恢复 | 开审文本对照 | 已恢复 |

独立 oracle：`python .planning/audits/round-23/_b_scratch/oracle.py` → **58/58 PASS**（点名 57 + 深层 XOR 限制记录 1；`oracle_report.json`）。CLI：`stage_a` scientific prepare + sham；`stage_b` fixture offline collect。

### 3.1 官方 iGSM vs 项目夹具

论文 GOAL §5.1 / DATA-01：官方与自建 DAG 分开标记。

- `load_igsm_snapshot(t1_official_shape)`：`source_kind=official`，`source=facebookresearch/iGSM`，`graph_kind=igsm_template`。template 重算 `q=9`，与 dump `answer=9` 一致；忽略 `lookup.q=99` 与结构图 `G`（`ignored_structure_graph=True`，`lookup_ignored=True`）。mod=23。
- `load_t1_fixture(t1_tiny)`：`source_kind=fixture`，`source=self_authored_arithmetic`。
- fixture 加载器拒 official shape（缺 `source_kind=fixture`），也拒把 `t1_tiny` 改标 `official`。
- `Task.validate`：`source=self_authored_arithmetic` 且 `source_kind=official` 抛 `Self-authored fixtures cannot be marked official`。
- `validate_t1_prepare_config`：ops∈{5,10,15,21}、n=500、mod=23。

### 3.2 T2/T3 不冒充完整 DAG

| 适配器 | graph_status | graph_kind | `ancestors()` | 备注 |
|---|---|---|---|---|
| GSM-Symbolic 无 sidecar | unknown | none | `{}` | 无节点；答案不造图 |
| Symbolic + 公式 sidecar | partial | formula_sidecar | `{total:{a,b}}` | 独立标注，非 CoT |
| GSM-Plus | unknown | none | `{}` | `solution_is_not_dag`；`4+3=7` 不进节点 |
| Hotpot | unknown | supporting_facts_only | `{}` | facts 仅 metadata（含 `DocA:0`） |
| MuSiQue | partial | composition_reference | `{}` | 分解节点存在但不进 \(R_{\mathrm{task}}\) |
| HumanEval | unknown | none | `{}` | `reference_dfg_is_not_task_dag` |
| Hotpot + CoT 文本 | — | — | — | `parse_events` 空，不造节点 |
| T2 no-op（无图） | unknown | none | `{}` | `answer_unchanged_proven=False` |
| T2 no-op（有图） | complete | arithmetic_dag | 目标祖先不含 `noop` | `recompute_and_ancestors` |
| T4 | unknown | — | — | 四态显式，`source_kind=fixture` |

### 3.3 事件身份不含值

`EventIdentity` 字段仅 `entity_or_expression` / `occurrence_version` / `scope`，无 `value`。同一身份、值 7 vs 99：`align_events` 成对。`parse_events("q = 99")` 身份仍为 `q`，值另存。

### 3.4 未知 / 未扫描不是 \(M\)；sham 协议

论文 §2.2、§2.6、§4.1；PROTOCOL §2.4–2.7；GOAL §5.3–5.4。

- `unscanned` / `unknown` / `parse_failed` → `behavior_label=None`。`behavior_unknown=True` 时 `M=[]`、`rho_M_raw=None`。同一集合在 `behavior_unknown=False` 且 \(B=\emptyset\) 时才得 \(M=T\)。
- 穷尽 `no_change` ∧ `observed_response` → 行为 0，不是未知。
- 构造 `sham:q` 观察（`rng_pair=sham:`，outcome=changed）：真实前提 `p1`/`p2` 的 `noise_ref` 仍为 `None`；仅 `sham:q` 得 `noise_ref=1.0`。`event_density_sets`：`noise_set=None`，`rho_*_excess=None`，`null_reason=noise_set_missing`。
- 真实前提全为 `noise_ref=0` 且无 `sham:` 行：`noise_set=None`，**不**把空集当已评估 \(N\)。
- 对照：直接 API `noise_set=[]` 且 `noise_evaluated=False` → `null_reason=noise_set_empty`，excess 仍为 null。

### 3.5 Scientific prepare 不得虚报 \(\rho_M^{\mathrm{excess}}\)

`cmd_prepare --eval-mode scientific --sham-opportunities 1 --out-dir stage_a`（exit 0）：

- 标签：`p1`/`p2` 的 `noise_ref=null`；存在 `sham:q`（`noise_ref=1.0`）。
- 事件密度：`M=[]`，`behavior_unknown=true`，`rho_M_excess=rho_S_excess=rho_M_noise=rho_S_noise=null`，`null_reason=noise_set_missing`。顶层聚合同样四量为 null。
- **未**把 `rho_M_excess` 记成 `0.0` 或 `1.0`。缺 `noise_set_missing` 而记账数值才会构成本点名失败。

fixture prepare + sham 同样：`source_value_pair` 写出，`noise_set=null`，`null_reason=noise_set_missing`。

### 3.6 来源—数值是真 XOR，不是改名

论文 §6 / GOAL §5.2。对 `t1_tiny` 编辑叶 `p2`：

- 来源臂：`premises=["p1","p2","src_b"]`，`p2.value==src_b.value=="0"`，`q.parents=["p1","src_b"]`，`kind=same_value_diff_source`，答案不变。
- `apply_rename_edit({p2:src_b})`：`premises=["p1","src_b"]`（丢掉 *a*），`kind=rename`。
- 两臂不同构。`make_source_value_pair` 同时给出 value 臂与 source 臂。CLI fixture prepare 写出 `source_value_pair`，与库结果一致。

重叠改名（额外）：`{p1:p2,p2:p1}` 一次替换得 `p2 = 4. p1 = 0. What is q = p2 * p1?`；顺序替换会塌缩。不是本轮点名失败条件，但是对「身份按原串映射」的独立复验。

### 3.7 Plus 测试锁与划分互斥

独立 SHA-256 分位（seed=0，分数 (0.40,0.15,0.10,0.10,0.10,0.15)）选中从未见 Plus 的 Symbolic（`original_id=iso-r23-never-plus`，题干 Nora r23-5 / figs，分位 ≈0.205）：`split_for_task` = **`probe_train`**，与本通道手算 `assign_split` 一致，未被强制 `test`。`load_gsm_symbolic` 源码不含 `register_test_only_family`。

加载独立 Plus（Mia r23 / `gsm8k-r23-lockfam`）后：Plus 与同族 Symbolic 均为 `test`，`fit_eligible=False`。另一孤立族仍为 `probe_train`。`assign_split(..., source="gsm_plus")` 恒为 `test`。

同族三成员经 `assign_family` 同一角色。`assert_disjoint({"probe_train":{x},"test":{x}})` 报 `Base-problem leakage`。六角色为 `probe_train / dev / direction_fit / calibration / transfer_pairs / test`。锁文件已恢复开审内容。

### 3.8 `stage_a` / `stage_b` 目录绑定

`_find_stage_file` 源码只检查传入目录下的同名文件，无 `rglob` / `parent` / `prep` / `lab`。空 `stage_b/` 不绑定兄弟 `stage_a/tasks.jsonl`、`stage_a/labels.jsonl`、`stage_a/edits.jsonl`。`_load_source_value_pair` 只读 `in-dir/edits.jsonl`。`_e_premise_ids` 在标签先见序 `p2,p1,sham:q` 时仍为 `["p1","p2"]`。

### 3.9 Fixture 离线 H 是诚实烟测，不是 MODEL-01

`collect --eval-mode fixture --backend offline --out-dir stage_b`：`run_spec.config.weight_source=offline_prefix_ids`，`hidden_layer=null`。这是八段 CLI 烟测用的离线前缀 H，**不**冒称冻结真实权重或 MODEL-01。`scientific collect` 在 `backend=offline` 时拒绝：`scientific collect refuses offline_prefix_ids as H`。本通道**不**把 fixture 离线 H 开成缺陷。

## 4. 发现

点名 CE **无已确认缺陷**。下列为额外观察，**不**把作者 ISSUES 行标为已关闭。

### B23-obs-1 — 深层 DAG 上 XOR 构造失败（限制，非点名失败）

| 字段 | 值 |
|---|---|
| 严重度 | 观察 / 构造覆盖缺口 |
| 状态 | 已证实限制，不是本轮点名 CE 失败 |
| 位置 | `edits.py` `apply_alt_source_same_value` 270–271；`cli.py` `_try_source_value_pair` 697–700 |
| 触发 | 目标直接父母不含被改叶子（`mid→q`，改 `p2`） |
| 证据 | oracle `X-deep-xor-limitation`：`ValueError: same_value_diff_source must change required sources`；`_try_source_value_pair` → `None`（静默不写 pair） |
| 原文 | §6 来源—数值解耦；官方 iGSM 常有多跳 |
| 影响 | 叶为 target 直接父母时（`t1_tiny`、官方 shape `q←a,b`）点名 CE 成立。更深图不产 `source_value_pair` |
| 建议 | 用祖先集合而非仅 `_target_parents` 判定来源是否改变；或对失败显式记录 |

### B23-obs-2 — T3 Hotpot 前提 span 相对题干，不相对文档（限制）

| 字段 | 值 |
|---|---|
| 严重度 | 观察 / tiny collect 下 T3 E 内容不可当作文档嵌入 |
| 状态 | 已证实测量限制；**不**否定「E 列顺序跟随 `task.premises`」 |
| 位置 | `t3_hotpot.py` 41–47；`collect.py` 72–78 |
| 证据 | 加载后各句 `start=0`，`text` 是文档句而 `question` 是问句；`span_token_indices` 在 question-only prompt 下对不上文档 |
| 原文 | §2.2 列索引为原始输入前提 |
| 影响 | 列顺序正确，但 tiny/question-only prompt 下 E 不是文档句向量 |
| 建议 | 科学 collect 须把 context 编进可对齐 span；当前不得宣称 T3 探针 E 已对齐文档 |

未把上述两项升为 FAIL：点名 CE 通过，且二者是覆盖/后端边界，不是本冻结上「官方/夹具分离 / T2T3 不造完整 DAG / 身份不含值 / 未知不进 M / sham 空 N / scientific 不虚报 excess / XOR 保留 a / Plus 锁 / 划分互斥」的反例。

## 5. 未执行 / 边界

- 真实 HF 权重、官方 dump、CUDA、长链 CoT、人工复核回填：`pending_server`。
- 未跑完整 scientific prepare→collect→fit→calibrate→intervene→repair→analyze 八端（属 E 通道）。本通道用库 API + `stage_a` scientific prepare 与 `stage_b` fixture offline collect。
- Fixture 八段 offline H 已核对其诚实烟测标签，**不**开缺陷，也**不**当作 MODEL-01 已满足。
- 未把 `ISSUES.md` 作者关闭或 r22 通道 PASS 当作本树独立关闭。
- 关闭权仍归汇总通道。本通道结论只覆盖数据/测量点名 CE。

## 6. 结论

| 项 | 裁决 |
|---|---|
| 冻结核验 | **HASH_MATCH** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（61） |
| pytest | 172 passed（独立复跑；绿 ≠ 论文正确） |
| 点名 CE | 全部通过（独立 oracle 58/58 + `stage_a`/`stage_b` CLI） |
| 已确认范围内缺陷 | 无 |
| **通道结论** | **PASS** |

通道 PASS 不是 Goal 接受，也不宣布 Goal complete。GOAL §5.1–5.5 在本机数据/测量范围内：官方与 fixture `source_kind` 分离；T2/T3 不以答案/supporting facts/参考 DFG/CoT 冒充完整事件 DAG；对齐靠身份不靠值；未知/未扫描不进 \(M\)；`sham:` 行空 \(N\) 且真实前提不继承 sham `noise_ref`；scientific prepare sham 密度不把 `rho_M_excess` 记成 0.0/1.0（`null_reason=noise_set_missing`）；来源—数值保留 *a* 并追加 `src_b`，不是改名；同族共组与 Plus 测试锁成立，孤立从未 Plus 的 Symbolic 可为 `probe_train`；六划分角色互斥。
