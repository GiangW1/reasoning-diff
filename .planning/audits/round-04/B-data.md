# Review B — 数据与测量（独立审查，round-04）

本报告不假设实现正确，不把 `ISSUES.md` 的「Closed locally / fixed_pending_review」当作已关闭。未修改任何生产代码、测试、夹屏或 `pyproject.toml`。未下载数据或权重。未阅读其他 round-04 通道报告。round-01/02/03 `B-data.md` 只用作待复验清单与行文格式，不作为证据。

**冻结核验：`HASH_MATCH`。** 按 `.planning/audits/round-04/VERSION.md` 文档化脚本（POSIX relpath + `\x00` + 文件字节，56 个范围内文件）独立复得 `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-04） |
| review_time | `2026-09-21T01:15:00+08:00`（复算 hash / 开读）— `2026-09-21T01:45:00+08:00`（成文） |
| declared_frozen_hash | `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`（`.planning/audits/round-04/VERSION.md`） |
| independently_recomputed_hash | **`HASH_MATCH`** `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`。56 个范围内文件。配方与 VERSION 一致。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿单独信任 HEAD） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对测量/划分调用链而通读；`fixture` = 对照适配器读完。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 320 | `b287249e03b493546e378175d4945e2d99bf129b1cc2ed0227db1f26dc7f13f9` | full 1–320 | 标签、S/M、噪声、TO/CSP、有限扫描、`event_density_sets` |
| `src/reasoning_diff/events.py` | 154 | `c7f9c33ecb97d1d85b2e5d0c388fc62456c4a0b4d4ec711ddbd2759a1b23486e` | full 1–154 | 身份（不含值）、等计数 `node_id`、`scanned=False` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `{}` |
| `src/reasoning_diff/edits.py` | 258 | `0e8365ca08ea3db3fa9cb190ae14cf15975973a9345281a6a7002a6a91e04b77` | full 1–258 | 小数隔离、重算、改名/来源—数值 |
| `src/reasoning_diff/splits.py` | 97 | `2bc45ed0bbce3a5c8bcaa97aedf506ae5469e5db0d0fcba2ce0c23ac71ed2f1b` | full 1–97 | `source` / `fit_eligible` / `gsm_plus` token、`split_for_task` |
| `src/reasoning_diff/schema.py` | 384 | `b61ee242b0a5bcbc520c75ace00a9f23dd5b3012c0a4d4c55b68bd44c8291091` | full 1–384 | 身份、`scan_state`、`exhaustive`、placeholder/spec |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 39 | `5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0` | full | 加载分派，不补图 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 52 | `606e4a09cfcbd8d9b3ab771d8648a10d0798f2ee937fb0818ae8d7a5ca1bfc78` | full | `gsm_plus:` 族键、placeholder、扰动映射、`fit_eligible` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 83 | `067af473ddb143b7dc017cd3ab0ab92276edd8cfbd15ae5b33eff64ba7787751` | full | sidecar、公式编辑、跨集族键 |
| `src/reasoning_diff/tasks/t2_noop.py` | 93 | `9329d9b1e2e91dadfedde51687ccc1325f5560881cfc3c9c720424c71719110f` | full | span、`recompute`、祖先检查 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `b86ca7dffd774606d4f0b9ad1f831d949b1a8434eb95bbbc5d14969e12e62f2b` | full | 文档编辑、`needs_truth`、supporting_facts≠DAG |
| `src/reasoning_diff/tasks/t3_musique.py` | 103 | `9587aa9662b1c1d7f67b8adb8d82838e636ba51f2df8ed27f0e7bcc8d635e7a4` | full | 段落编辑、组成图不进 `ancestors` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 62 | `398a8ab68104fb98170e75487d9b62625c9e26b194a9d6d0ba5e736deecc3468` | full | 完整 `task_id`、Spec 编辑、kind=spec |
| `src/reasoning_diff/tasks/t4_boundary.py` | 33 | `aab4821f407c0f06d52d69abca581c1b067a1748327c67b2391a6978c0dbd2ba` | full | 四态显式、整题 placeholder |
| `src/reasoning_diff/cli.py` | 658 | `c7b8061e036c9f83a84b13df01e96e73fc89e9f66b47bd3010349441f0f11c45` | callsite 88–158, 169–372, 525–561 | prepare/label 是否调用测量 API；sham `premise_id=""` |
| `src/reasoning_diff/analysis.py` | 253 | `18adcce069d4b50e4e77d92525335951f2feb57282bdaa194bda3b07f7103875` | callsite 97–137 | P2 分母一致性 vs 整数透传 |
| `src/reasoning_diff/scoring.py` | 30 | `d05822c4fb784fe4a57d9f82f583eaa31c0f3b2e0e96c04b81f77db7413433f8` | callsite | 域内评分分母 |
| `tests/test_review_regressions.py` | 394 | `37414926677d059610794b4f64ec3bcbf7c242ecce9c563bc8e549abc5d3a60c` | full | 作者回归是否覆盖原触发 |
| `tests/test_round03_regressions.py` | 288 | `70475c77edce6844cad811c010f4ecb29aa764dc11b24ccb5d3de1dd14b09e51` | full | r03 作者 oracle；独立另造反例 |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c` | full | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256：`t1_tiny.json` `3267db38…`（与 r01–r03 同）；`t1_official_shape.json` `2fbf6773…`（同）；`t2_symbolic_one.json` `481f654e…`（同）；`t2_formula_sidecar.json` `8a014940…`（同）；`t2_gsmplus_one.json` `86bdeb66…`（与 r03 同，含 `original_id` + `seed_question`）；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

相对 r03 生产 digest 已变：`measure.py` / `events.py` / `graphs.py` / `edits.py` / `splits.py` / `schema.py` / `t1_official.py` / `t2_gsm_plus.py` / `t2_gsm_symbolic.py` / `t2_noop.py` / `t3_hotpot.py` / `t3_musique.py` / `t3_humaneval.py` / `t4_boundary.py` / `cli.py` / `analysis.py`。`t1_config.py` / `t1_fixture.py` / `catalog.py` / `scoring.py` / `__init__.py` 未变。

## 3. 已执行检查

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-01 | 作者指定的本通道 pytest | `python -m pytest tests/test_review_regressions.py tests/test_measure.py tests/test_t1_official.py tests/test_t2_gsm.py tests/test_t3_t4.py tests/test_round03_regressions.py tests/test_tracer_t1_prepare.py -q --tb=short` | **77 passed**，exit 0。绿测试不能关闭下列独立反例。 |
| X-02 | 全量本机 pytest | `python -m pytest tests -q --tb=line` | **97 passed**，exit 0，约 11.4s。无 skip/xfail。与 VERSION `pytest_author_claim` 计数一致，仍不是科学正确性证据。 |
| X-03 | 矩阵 `noise=None`（B-01） | `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `S.noise=None`，`S.excess=None`，`rho_S_noise=None`，`null_reason=noise_missing`。保持关闭。 |
| X-04 | 有限扫描 `no_response_observed_in_scan`（B-02） | 仅 `outcome=no_change` + 该 scan_state | `behavior_label=None`，`behavior_known=False`。保持关闭。 |
| X-05 | `observed_response` + `no_change` ± `exhaustive`（B-23） | 同上两旗标 | 无 `exhaustive` → unknown；`exhaustive=True` → `behavior_label=0`。API 保持关闭。 |
| X-06 | sham 不进入 R_behavior（B-03） | 编辑 no_change + `sham:0` changed | 行为袋 `0`；`noise_ref=1.0`。CLI 现写 `premise_id=""`（X-06b 多一条空前提标签）。 |
| X-07 | 删除后对齐（B-04 原触发） | `"q = 1\\nq = 2\\n"` vs `"q = 2\\n"` | `pairs=[]`；`merged` 非空；`scanned=False`；`strategy_detector=status_field_only`。 |
| X-08 | 等计数同 `node_id` | `"q = 1\\nq = 2\\n"` vs `"q = 9\\nq = 2\\n"` | 配成 `(1,9),(2,2)`，双方 `node_id=q`。这是身份（实体/版本/作用域）对齐，不是按值配对。 |
| X-08b | 等计数不同 `node_id`（作者 B-04 修复） | entity `q` 左 `node_id=q`、右 `node_id=r` | `pairs=[]`，记 ambiguous。 |
| X-09 | R_surf vs 图父母（B-06/B-25） | 裸赋值 / 值后提及 / 赋值前 | 父母 `['p1','p2']`；裸 surface `[]`；值后与赋值前均为 `['p1']`。保持关闭。 |
| X-10 | HumanEval 族（B-07） | `load_humaneval` | `base_group_id=HumanEval/0`。`assign_split("HumanEval")` 仍为 `probe_train`，加载器不用该截断键。前提 `kind=spec`，全文 42 字符。 |
| X-11 | 公式编辑（B-08） | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，premise/node/answer 均为 5/8/8。保持关闭。 |
| X-12 | 数值子串（B-09） | `"has 13 apples"`、值 `"3"` | `ValueError: not a unique isolated token`。保持关闭。 |
| X-13 | 小数 3.5/5 与 5.5/5.0（B-24） | `_replace_isolated_value` + `apply_value_edit` | `3.5`/`5.5`/`5.0`/`+5.5`/`15.5` 均抛错。孤立 `p1 = 5` → `p1 = 9`。原 5.5/5.0 触发关闭。 |
| X-14 | no-op span + 证明旗标（B-10） | 前端注入 `"p1 = 4 is a red herring."` | 原 span `[25,31]` 切片 `"p1 = 4"`。`answer_unchanged_proven=True`（同表达式重算）。`injected_non_ancestor=True` 来自注入**前** `"noop" not in target_anc`（基图祖先是 `{p1,p2}`）。缺 caller 布尔则拒绝。 |
| X-15 | CSP 空父母 + unknown（B-11） | `task_parents=[]`，`graph_status=unknown` | `csp=None`，`clean_matched=0`。保持关闭。 |
| X-16 | CSP 空父母 + complete | 同上但 `complete` | `csp=0.0`，`clean_matched=1`，`coverage=1.0`。 |
| X-17 | `assign_family`（B-13） | 缺 id；同 id 不同子集 | 缺 id 抛错。`{A,B,C}` / `{B,C}` / `{Z}` 同 `family_id` 均为 `test`。保持关闭。 |
| X-18 | GSM-Plus 生产划分（B-14） | 夹具 / 官方字段子集 / `original_id=gsm8k-1` / 裸 `assign_split` | 见下段。**生产路径关闭。** |
| X-19 | 跨集族键（B-15） | 同题 Symbolic vs Plus | Symbolic `base_group_id=gsm8k-12`；Plus `gsm_plus:ada has 4 apples…`。`shared_gsm_family` 分别为 `gsm8k-12` 与题干规范化文本。不相等。 |
| X-20 | T3 编辑 / 组成图（B-16/B-20） | `document_edit` / `paragraph_edit` / `apply_spec_edit` / `ancestors` | 无 `new_answer` → `needs_truth`。有答案 → `valid`，不核验、不跑测试、不改 MuSiQue 分解节点。`ancestors(musique/hotpot/plus/he)=={}`。 |
| X-21 | CLI prepare + sham（B-12） | `main(["prepare", …, "--sham-opportunities","1"])` | 真编辑 `changed`；sham `premise_id=""`、`no_change`、`scan_state=observed_response`、`exhaustive=False`。标签 `(q,p2)` `noise_ref=0.0`，另有 `(q,"")`。密度 `aggregation=mean_over_events`，事件行 `null_reason=noise_set_empty`。 |
| X-21b | CLI 已观察 no_change | `--edit-premise p1 --edit-value 7`（q 仍 0） | `outcome=no_change`，`scan_state=observed_response`，`exhaustive=False`，`behavior_known=False`。不再误写 `no_response_observed_in_scan`。 |
| X-21p | Plus 八类扰动（B-21） | 独立喂官方类名 | `critical thinking` / `missing information` → `insufficient_information`。`reversing operation` → `answer_spec.status=None`，`metadata.perturbation_status=query_target_change`。其余六类 `(None, None)`。 |
| X-22 | P2 分母（B-22） | `p2_paired(..., 99)` ± `shared_premises` | 只传 99 → `shared_denominator=99`，空列表，`status=ok`。`99` vs `["p1"]` → `denominator_inconsistent`。一致时用集合长度。 |
| X-22n | 多节点祖先 | 内存 s=p1+p2、t=s+p3 | `anc[t]={p1,p2,p3}`。`ancestors` 对 `composition_reference` 返回 `{}`。 |
| X-23 | 空 `noise_set` + 协议 hits（B-26） | 集合密度 API | `rho_S_noise=None`，`null_reason=noise_set_empty`。保持关闭。 |
| X-24 | 多匹配行 / 非法 scan_state（B-27） | `"q = 0 q = 1\\n"`；非法枚举 | 两条 `status=ambiguous`。非法 scan_state 抛 `ValueError`。保持关闭。 |
| X-25 | 改名 / 来源—数值 / 复核（B-18） | `apply_rename_edit` / `apply_source_value_edit` / 全包搜 `review_export` | 题干 `alpha = 4` 且 `q = alpha * p2`，**表达式仍 `p1 * p2`**。`source_value` 只是打旗的值编辑，`same_value_diff_source=False`。无 `review_export`。`apply_value_edit.exhaustive` 恒 False。 |
| X-26 | 官方夹具重算（B-19） | 夹具 9；篡改答案 8 | 9=9。不一致拒绝。保持关闭。 |
| X-27 | 除法模运算 | `_eval_expr("5 / 2", {}, 23)` | `2`（`int(truediv)%mod`），不是模逆 14。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。对齐不读 value。 |

**X-18 细项（独立，不信任 `test_b14`）：**

- 夹具生产键：`base_group_id=gsm_plus:ada has 4 apples and buys 3 more. how many apples?`（优先 `seed_question`，不是 `original_id`）。`source=gsm_plus`，`fit_eligible=False`，`kind=placeholder`。
- `assign_split(loaded.base_group_id)` **不传 source** → `test`（token 含 `gsm_plus`）。
- `split_for_task(loaded)` → `test`。
- 仅官方字段（无 `original_id`/`id`）→ 同样 `gsm_plus:<seed_question>`，裸 `assign_split` 与 `split_for_task` 均为 `test`。
- 自造 `original_id=gsm8k-1` 但仍有 `seed_question` → 生产键仍是题干，不是 `gsm8k-1`。`assign_split("gsm8k-1")=="probe_train"`（13/30 个 `gsm8k-0..29` 为 `probe_train`；`gsm8k-12` 碰巧 `test`）。该裸调用**不再是 Plus 加载器输出的族键**。
- `assign_family(..., family_id="gsm8k-1")` 不传 `fit_eligible`，角色 `probe_train`。

**X-12e/f（`event_density_sets` 独立）：** sham no_change → 标签 `noise_ref=0.0`，但 hits 只收集 `noise_ref==1.0`，于是 `noise_set=[]` → `noise_set_empty`，excess null。sham changed 时空前提也进入 hits。t1_tiny 的 S 分母为空（P=T={p1,p2}），CLI 看不到非空 S。

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 | 无官方 dump；机制层 B-15 已在夹具确认 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b`。见 U-01 |

## 5. 既有 B-## 独立结论（closed / residual / reopened）

不得因回归绿或 `ISSUES.md` 成文而关闭。下表针对 **round-01/02/03 原 ID**。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | 未本轮重开 | **closed** | X-03 |
| B-02 | — | **closed** | X-04 |
| B-03 | — | **closed** | X-06；CLI 不再把 sham 钉在编辑前提（X-21） |
| B-04 删除错位 | closed locally | **closed** | X-07 |
| B-04 等计数 zip | closed locally（要求同 `node_id`） | **closed** | X-08b 不同 `node_id` 拒配。X-08 同节点等计数 zip 是身份对齐（值不决定对应），不升格。 |
| B-05 `scanned=True` | closed locally | **closed** | X-07：`scanned=False`，`strategy_detector=status_field_only`。不再冒充已扫描。策略分类仍未实现，见 ND-17。 |
| B-06 / B-25 | — | **closed** | X-09 |
| B-07 | — | **closed** | X-10 |
| B-08 | — | **closed** | X-11 |
| B-09 | — | **closed** | X-12 |
| B-10 span | closed locally | **closed** | X-14 span |
| B-10 祖先/答案证明 | closed locally（answer proof） | **residual** | X-14：`recompute` 只证明表达式/声明值未改；`"noop" in target_anc` 在注入前检查，基图不可能已有 `noop`。caller 布尔仍是真正的「证明」。见 §6 B-10。 |
| B-11 | — | **closed** | X-15 |
| B-12 事件级密度 + sham 钉前提 | closed locally | **closed**（原触发） / **residual**（sham 阴性） | X-21：`event_density_sets` + sham `premise_id=""`。X-12e：已观察 sham 阴性写成 `noise_set=[]` → excess null，与标签 `noise_ref=0.0` 不一致。 |
| B-13 | — | **closed** | X-17 |
| B-14 生产族键 + `fit_eligible` | closed locally | **closed** | X-18/X-18b：生产 `base_group_id` 带 `gsm_plus:` 前缀；裸 `assign_split(base_group_id)`、`split_for_task`、`fit_eligible=False` 均为 `test`。夹具哈希巧合不再是关闭条件。 |
| B-15 跨集族键 | 未主张关闭 | **residual（仍 confirmed）** | X-19。见 §6。 |
| B-16 T3 口述真值 | 未主张关闭 | **residual（仍 confirmed）** | X-20。见 §6。 |
| B-17 N 字符假前提 | closed locally | **closed**（原触发） / **residual**（HumanEval spec） | Plus/Symbolic-无侧车/T4 现为整题 `kind=placeholder`，`event_density_sets` 与 CLI 编辑过滤 placeholder。HumanEval `kind=spec` 仍进入 P（X-17e `denominator_S=1`）。 |
| B-18 改名/解耦/复核 | 未主张关闭 | **residual（仍 confirmed）** | X-25。见 §6。 |
| B-19 官方加载不重算 | — | **closed** | X-26 / X-26b |
| B-20 组成图身份撞车 / 被 `ancestors` 消费 | — | **closed** | X-20g：`graph_kind in {composition_reference, supporting_facts_only, none}` → `{}`。解析身份用 `node.id`。 |
| B-21 扰动映射 | closed locally | **closed** | X-21p：不再把 `critical thinking` 标成矛盾约束；`reversing operation` 不再写成非法 `query_reversed`。 |
| B-22 P2 分母 | closed locally（consistency） | **residual** | X-22：不一致会 null；**只传整数 99 仍 `status=ok`**。 |
| B-23 API | — | **closed** | X-05；CLI 现写 `observed_response`+`exhaustive=False` → unknown（X-21b）。 |
| B-24 `5.5`/`5.0` | closed locally | **closed** | X-13 / X-13c / X-13d。作者 `test_b24` 现覆盖两例；独立复现一致。 |
| B-26 空集当 0 | — | **closed** | X-23。与 B-12 残余（已观察 0 → 空 hits）分开。 |
| B-27 | — | **closed** | X-24 |

## 6. 发现（本轮仍开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐或划分会被污染；`medium` = 协议要求的适配/字段缺失；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B-15 跨数据集族键在官方 Plus schema 上仍不一致

- **状态：** confirmed defect（机制）/ pending_server（真实 dump 碰撞率）  
- **严重度：** high  
- **符号：** `t2_gsm_symbolic.family_id` vs `t2_gsm_plus.load_gsm_plus`  
- **行号：** `t2_gsm_symbolic.py` 11–13, 47, 63；`t2_gsm_plus.py` 20–24, 42  
- **协议：** DATA-03 / FEATURES T2：以规范化 `seed_question` **连接 GSM8K ID**；不同数据集同源题同族。  
- **证据：**  
  1. X-19：同题夹具 Symbolic `base_group_id=gsm8k-12`，Plus `gsm_plus:ada has 4 apples and buys 3 more. how many apples?`。  
  2. Plus 优先 `seed_question` 文本，**不**把 `original_id`/`gsm8k-*` 写成族键（即使夹具有 `original_id=gsm8k-12`）。FEATURES 所列官方 Plus 字段是 `question/solution/answer/perturbation_type/seed_*`，没有 `original_id`。无 seed→GSM8K ID 匹配。  
  3. `metadata.shared_gsm_family` 两边也不相等（`gsm8k-12` vs 题干）。无消费该字段的共组函数。  
- **影响：** 同 GSM8K 题可一边（Symbolic）进 `probe_train`，一边（Plus）进 `test`，且无法按族断言 `assert_same_role`。Plus 自身的 test-only 锁（B-14）不能代替共组。  
- **建议：** 规范化 seed 文本匹配 GSM8K ID；失败则 `unmapped` + 文本哈希，禁止静默各算各的。

---

### B-16 T3「合法编辑 + 更新真值」仍是调用方口述

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `t3_hotpot.document_edit`；`t3_musique.paragraph_edit`；`t3_humaneval.apply_spec_edit`  
- **行号：** `t3_hotpot.py` 51–104；`t3_musique.py` 72–103；`t3_humaneval.py` 34–58  
- **协议：** DATA-02 / FEATURES：替换支撑文档后更新**受影响子问题答案**与最终答案；HumanEval-Perturb 以**新测试为裁判**。  
- **证据：**  
  1. X-20：无 `new_answer` 时 `validity=needs_truth`、`status=requires_independent_truth`（比口述缺失诚实）。  
  2. 传入任意 `new_answer` 即 `validity=valid`，不对照文档/桥接/别名。  
  3. MuSiQue `paragraph_edit` 只改段落与最终 `answer_spec`，**分解节点仍留旧答案**（Colette/Paris）。  
  4. `apply_spec_edit(..., new_solution=..., new_tests=...)` 标 `valid` 且 `distinguishing_tests=True`，**不调用** `score_code` / 隔离执行器。  
  5. `ancestors(musique)=={}`（B-20 关闭）：组成图不再进入 ρ。此项不抵消未更新的分解真值。  
- **影响：** 夹具上即可写出「已更新且 valid」的反事实，而节点/测试裁判未变。机制 bug，不是 pending_server。  
- **建议：** QA 无独立核验则保持 `needs_truth`；HumanEval 必须对新测试跑隔离评分后才能 `valid`；MuSiQue 同步子问题答案或清空。

---

### B-10 残余：no-op「祖先/答案不变」证明是空的

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `t2_noop.make_noop_pair`  
- **行号：** `t2_noop.py` 21–26, 86–92  
- **协议：** T2NOOP-01：须**独立证明**注入句不改变已有节点祖先与答案；模型对错不是裁判。  
- **证据：** X-14。span 正确。`if "noop" in target_anc` 在注入前求值，基图祖先是前提 id，不会含 `"noop"`。`recompute` 用原表达式与原声明值，答案必然不变（除非调用方已改值）。`injected_non_ancestor` 回写同一空检查。无节点的 T2 题根本不跑 `recompute`。  
- **影响：** 元数据可读成「已证明非祖先 / 答案未变」，实际只是 caller 布尔 + 同图重算。  
- **建议：** 注入后比较 `ancestors`（注入列不得进入 target）；无图则 `unknown`，禁止写 `*_proven=True`。

---

### B-22 残余：P2 分母仍可只是调用方整数

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `analysis.p2_paired`  
- **行号：** `analysis.py` 97–137；`cli.py` 551–560 透传 `shared_denom`  
- **协议：** P2 必须同时报告完整密度、共同已有前提变化、新增注入列。  
- **证据：** X-22：`p2_paired(..., 99)`（无 `shared_premises`）→ `shared_denominator=99`、`shared_premises=[]`、`status=ok`。仅当**同时**传入集合且长度冲突才 `denominator_inconsistent`。`make_noop_pair` 仍不计算共同分母。  
- **影响：** 报告可以看起来「有分母」而没有共同支持集合。一致性检查不能关闭原触发。  

---

### B-12 残余：已观察 sham 阴性被密度层当成空噪声集

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `measure.event_density_sets` / `build_labels`  
- **行号：** `measure.py` 72–78, 273–280；`cli.py` 214–245  
- **协议：** MEAS-02：配对噪声机会单独计量；已扫描且无变化是参照 0，不是 missing。  
- **证据：** X-21 / X-12e。sham 不再钉 `p2`（原触发关闭）。标签在 sham 已跑且 no_change 时写 `noise_ref=0.0`，同时多一条 `premise_id=""` 的标签。`event_density_sets` 的 `hits` 只收 `noise_ref==1.0`，于是 `noise_set=[]` → `noise_set_empty` → excess null。  
- **影响：** 标签层说噪声是 0，密度层说噪声缺失。有非空 S 分母的题会拒绝扣除已观察的 0。  
- **建议：** 已观察 sham 用「该事件的噪声前提袋」（可空集但 `noise_set is not None`），空 list 只表示 missing。

---

### B-17 残余：HumanEval spec 仍进入 ρ 的 P 列

- **状态：** confirmed defect  
- **严重度：** low  
- **符号：** `t3_humaneval.load_humaneval`；`measure.event_density_sets`  
- **行号：** `t3_humaneval.py` 21；`measure.py` 269  
- **协议：** 未知图应 unknown，不得填假前提列冒充可评估 P。  
- **证据：** X-17e：`kind=spec` 不被 placeholder 过滤；`denominator_S=1`，`rho_S_raw=0.0`。Plus/T4/Symbolic-无侧车已改为 placeholder 并被过滤（原 N 字符触发关闭）。  
- **影响：** 对 HumanEval 调用密度 API 会得到看起来完整的 0 密度。  

---

### B-18 DATA-01 的改名 / 来源—数值 / 人工复核仍不完整

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `edits.apply_rename_edit` / `apply_source_value_edit`；缺失 `review_export`  
- **行号：** `edits.py` 151–216  
- **协议：** DATA-01：数值/改名/no-op/来源—数值变体。MEAS-01：可导出与回填人工复核。论文：先 a=b 再 a≠b 的来源解耦对。  
- **证据：** X-25。改名后可见文本为 `alpha`，节点表达式仍 `p1 * p2`（`recompute` 仍认 `p1`）。`source_value` 只是 `apply_value_edit` + 旗标，不构造同值异源对。全包无 `review_export`。  
- **影响：** C2 解耦资产无法从数据层按协议生成。函数存在不等于 DATA-01 完成。  

## 7. 已独立关闭的原触发（非本轮缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01 | X-03 | — |
| B-02 | X-04 | — |
| B-03 | X-06 / X-21 sham `premise_id=""` | B-12 空前提标签 |
| B-04 删除 / 异 node_id | X-07 / X-08b | — |
| B-05 假扫描 | X-07 `scanned=False` | 无策略分类（ND-17） |
| B-06 / B-25 | X-09 | U-03 |
| B-07 | X-10 | — |
| B-08 | X-11 | — |
| B-09 / B-24 | X-12 / X-13 | — |
| B-10 span | X-14 | 空祖先证明 |
| B-11 | X-15 | X-16 `complete`+`[]` |
| B-12 题级袋 / 钉前提 | X-21 `event_density_sets` | sham 阴性 → 空集 |
| B-13 | X-17 | — |
| B-14 | X-18 生产键 / `fit_eligible` / 裸 `assign_split(base)` | B-15；裸 `assign_split("gsm8k-1")` 仍哈希（非 Plus 生产键） |
| B-17 N 字符 | Plus/T4/Symbolic placeholder | HumanEval spec |
| B-19 | X-26b | pending_server 真实 dump |
| B-20 | X-20g `ancestors=={}` | B-16 分解答案未更新 |
| B-21 错映射 | X-21p | 六类无状态（可接受） |
| B-23 | X-05 / X-21b | CLI 永不置 `exhaustive=True`（保守） |
| B-26 空集当 0 | X-23 | B-12 残余 |
| B-27 | X-24 | — |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径 S/M 与缺 sham → null | `measure.py` 122–140 | 缺协议或 `noise_set is None` 时 excess null；负差不截断。不否定 B-12 残余。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | fixture 拒 official；官方拒仅有 G；lookup 不进重算。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | 中间节点不进入列索引；非算术 `graph_kind` 返回 `{}`。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | `EventIdentity.key()` 为 entity/version/scope。X-08 同节点 zip 符合「值不决定对应」。 |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 303–312 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` 36–37 | `graph_status=unknown`，`graph_kind=none`。不否定 B-15。 |
| ND-07 | Hotpot 声明 supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 34–38 | 文档级多句替换且 `single_premise_claim=False` 符合「一文档多前提」。不否定 B-16 口述答案。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | 不从标题推断。 |
| ND-09 | HumanEval 不在宿主 exec | `scoring.py` 19–29 | `executor_unavailable` 时 value/denominator null。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` 43–51 | `reasoning_diff_noop`，`official_noop_release=False`。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 131–137 | `b <= limit`。 |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` | `splits.py` 69–87 | 原语正确；不否定 B-15。 |
| ND-13 | T1 配置拒绝非白皮书格子 | `t1_config.py` 9–21 | |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 59–60 | |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05/X-21b。 |
| ND-16 | 官方加载对照 template 重算 | `t1_official.py` 77–80 | X-26。不把「有校验」写成「全量官方数据已验收」。 |
| ND-17 | 策略分岔 `scanned=False` | `events.py` 119–126 | 空 `strategy_changed` 现表示未扫描，不是「已检测为零」。STRUCT-01 仍未实现分类器，但不构成静默假阴性。 |
| ND-18 | Plus/T4 placeholder 过滤 | `measure.py` 269；`cli.py` 89, 151–157 | 原 B-17 N 字符列不再进编辑或 P 分母。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；API 已关 B-23，密度层仍有 B-12 残余 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 碰撞率 | DATA-03 | 机制层 B-15 已确认；dump 上匹配率 pending |

官方全量保持 `pending_server`。夹具上可复现的机制错误记为 confirmed defect，不降级为 pending_server。

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod`（5/2 mod 23 = 2，模逆 14） | FEATURES 称官方 Num 为加减乘；夹具无除法。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official` | 可解释为题源而非「该行是官方发布」。需协议裁定。 |
| U-03 | `surface_mentions` 只匹配 `premise_id` / alias 词 | SURF-01 写「名称与符号引用」。官方 iGSM 夹具 id 即 `a`/`b`。未在真实题干别名上抽样。 |
| U-04 | 后续 stage 是否用 `task_id` 而不是 `base_group_id` 做划分 | CLI fit 只信 `--split` 旗标。prepare 写 `splits.jsonl` 但不被 fit 读取。 |
| U-05 | 前提 span 同时含孤立整数 `5` 与小数 `5.5` 时整数编辑被拒 | 当前 fail-closed。未见生产 span 同时含两者。 |
| U-06 | `assign_family` 不传 `fit_eligible` | Plus 生产走 `split_for_task` 不走 `assign_family`。缺 source 的 `gsm8k-*` 族是 Symbolic 路径，不是 Plus 泄漏。 |

## 11. 测试质量对本通道的含义

**97 passed ≠ 数据/测量正确。** 作者本轮补了 B-14 生产键、B-24 `5.5`/`5.0`、等计数异 `node_id`、P2 不一致分母。独立复现同意这些原触发已关。缺口仍在：

- 无跨集族键断言（Symbolic `gsm8k-12` vs Plus `gsm_plus:<seed_question>`）。`test_b14` / `test_b14_plus_family_key` 不测 B-15。  
- `test_spec_and_paragraph_need_truth` 只测缺答案；不测「有答案即 valid、分解节点不更新、新测试未执行」。  
- 无 no-op 祖先 vacuity 断言；`test_b10` 只查 span。  
- 无 `p2_paired(..., 99)` 整数-only 拒绝。  
- 无 sham 阴性 → `noise_set_empty` 与 `noise_ref=0.0` 对照。  
- 无 HumanEval `event_density_sets` 分母断言。  
- `test_full_cli_smoke` 只查 exit 0 与 `report.status`。

因此不能把 ISSUES 中 B-10/B-12/B-15/B-16/B-17/B-18/B-22 整行标为已关闭。B-14 与 B-24 的**原触发**可独立关闭。

## 12. 通道结论

数据与测量通道 **不能** 在本冻结对象上给出通过意见。

1. **`HASH_MATCH`：** 声明冻结 hash 已按 VERSION 配方复现（56 文件）；结论绑定上表逐文件 digest。  
2. **本轮可独立关闭的作者主张：** **B-14**（生产 `gsm_plus:` 族键 + `fit_eligible` + 裸 `assign_split(base_group_id)`）、**B-24**（`5.5`/`5.0`）、**B-05**（`scanned=False`）、**B-04** 等计数异 `node_id`、**B-21** 错映射、**B-17** N 字符假前提、**B-12** 原触发（事件均值 + sham 不钉编辑前提）、**B-20**（组成图不再进 `ancestors`）。先前已关且仍关：B-01/02/03/06/07/08/09/11/13/19/23/26/27。  
3. **仍确认的机制缺陷（夹具可复现）：** **B-15** 跨集族键、**B-16** T3 口述 valid / 分解答案不更新 / Spec 不跑测试、**B-10** 空祖先证明、**B-22** 整数分母仍 `ok`、**B-12** sham 阴性→空噪声集、**B-18** 改名不改表达式且无解耦对/复核、**B-17** HumanEval spec 列。  
4. 集合密度 raw/null/signed、T1 来源隔离、官方 dump 对照重算、有限扫描 unknown、身份不含值仍成立（ND-01–ND-18），不能抵消划分共组与 T3 真值更新缺口。官方全量保持 `pending_server`。即使服务器数据到达，**B-15 仍会把同源 Symbolic/Plus 拆成两族**，B-16 仍会把未核验答案写成 `valid`。
