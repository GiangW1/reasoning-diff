# Review B — 数据与测量（独立审查，round-03）

本报告不假设实现正确，不把 `ISSUES.md` 的「Closed locally / fixed_pending_review」当作已关闭。未修改任何生产代码、测试或夹具。未下载数据或权重。未阅读其他 round-03 通道报告。round-01/02 `B-data.md` 只用作待复验清单与行文格式，不作为证据。

**冻结核验：`HASH_MATCH`。** 按 `.planning/audits/round-03/VERSION.md` 文档化脚本（POSIX relpath + `\x00` + 文件字节，55 个范围内文件）独立复得 `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-03） |
| review_time | `2026-09-21T00:58:00+08:00`（复算 hash / 开读）— `2026-09-21T01:03:23+08:00`（成文） |
| declared_frozen_hash | `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`（`.planning/audits/round-03/VERSION.md`） |
| independently_recomputed_hash | **`HASH_MATCH`** `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`。55 个范围内文件。配方与 VERSION 一致。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿单独信任 HEAD） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对测量/划分调用链而通读；`fixture` = 对照适配器读完。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 248 | `fde5ec49294e5b7409b673bd3d2d37c6af6bd838cc7bfb01ef2090ca5c448d70` | full 1–248 | 标签、S/M、噪声、TO/CSP、有限扫描、分母 |
| `src/reasoning_diff/events.py` | 142 | `73e9b2667e489b546ec4782c1019c99c2f07dc3530a0ae4824dc7cfd66f5c403` | full 1–142 | 身份、对齐、结构变化、R_surf span |
| `src/reasoning_diff/graphs.py` | 44 | `1e287cebf844cec0d055138224ae5a0b39c0358228c6587e8b4b6d4cfc604241` | full 1–44 | 前提祖先、unknown/complete、cone |
| `src/reasoning_diff/edits.py` | 184 | `f201eb4931556ac03b1922ff132b3b7df5f49c9c7a5decf5308f45620276c3b2` | full 1–184 | 孤立记号、重算、改名/来源—数值 |
| `src/reasoning_diff/splits.py` | 78 | `fd871c0ae40ef72103d6ca6c61be809d559868e99f3fad949f95c7fcd78db436` | full 1–78 | 共组、test-only、family_id、默认泄漏 |
| `src/reasoning_diff/schema.py` | 373 | `5140f8b1687569b99cb3a3b728897ea8d9a825c9c2bc3371c42db43bf3f751fe` | full 1–373 | 枚举、身份、scan_state、exhaustive |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 39 | `5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0` | full | 加载分派，不补图 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 86 | `3267cf12bf9ef5e4578f98b7c01b20bdc5149385f603e3c2a8482b51daec1ab1` | full | template≠G、shared RNG、lookup、加载重算 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 51 | `6d396506526c52814ef5562d7a95fd9d6739fdbe2ea182d8bbf56fe1d528eaed` | full | test-only 贴纸、族键、占位前提 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 70 | `f0492a797e6d89a021092272bfc0cd31b386d7c99752160bc6078722879d0628` | full | sidecar、公式编辑、跨集族键 |
| `src/reasoning_diff/tasks/t2_noop.py` | 80 | `26cf5c21b5838a6bf1a335bf8b0eb5bc767a77c2e4128fc8a36a8c482456c874` | full | prefer_from span、无祖先证明 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 94 | `e5e7a9075ea64df98076d06b00ce88fce410c83cc52840ee8c7eba7949aa5bdd` | full | supporting_facts≠DAG、文档编辑真值 |
| `src/reasoning_diff/tasks/t3_musique.py` | 93 | `761c8bc8b7c77bfe3b55a558916ce92b70d3ae6a5095308e437c216a0f811aaa` | full | 组成图当 ancestors、段落编辑 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 61 | `3f74a52b59748db72da703d34229ad62d0bba833aed2bad21e2fc82e828e82de` | full | 完整 task_id 族、Spec 编辑 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 33 | `a2ca9188353b213d2c7c617dd27c60415adb0c16c40326ae8a7ecce03f94a5f9` | full | 四态显式、占位前提 |
| `src/reasoning_diff/cli.py` | 511 | `bcdf4f982b585f1da3751cd920bcd972ce433d93b256969af34a5ec7762dfd7b` | callsite 121–324 | prepare/label 是否真正调用测量 API |
| `src/reasoning_diff/analysis.py` | 157 | `bf3440b0fd0fd01cfb08314690efade13c45ada89e3abfd98a77f4f5336e86cc` | callsite 67–96 | P2 分母是否只是透传 |
| `src/reasoning_diff/scoring.py` | 30 | `d05822c4fb784fe4a57d9f82f583eaa31c0f3b2e0e96c04b81f77db7413433f8` | callsite | 域内评分分母 |
| `tests/test_review_regressions.py` | 371 | `1e91c98d55e645480f89599f7e12a1fb8bb02ca4929c463aa743de75e143c8c5` | full | 作者回归是否覆盖原触发 |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 40 | `54e57fea7417d901c75b7d17cfe9b90ee442f2d634a08d22272a678959ce9650` | full | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/test_science.py` | 97 | `3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c` | full | |
| `tests/test_cli_pipeline.py` | 29 | `63b4c09f51f6c7d807e8928f27fa62ec54e3f4656229b3615371ae930b5de0b9` | full | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256：`t1_tiny.json` `3267db38…`（与 r01/r02 同）；`t1_official_shape.json` `2fbf6773…`（同）；`t2_symbolic_one.json` `481f654e…`（同）；`t2_formula_sidecar.json` `8a014940…`（同）；**`t2_gsmplus_one.json` `86bdeb66…`（相对 r02 `81ac53c4…` 已改，新增 `original_id=gsm8k-12`）**；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

`graphs.py` / `t2_noop.py` / `t4_boundary.py` / `catalog.py` / `t1_config.py` / `t1_fixture.py` / `scoring.py` digest 与 round-02 相同。

## 3. 已执行检查

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-01 | 作者声明的数据回归 + 本通道测试 | `python -m pytest tests/test_review_regressions.py tests/test_measure.py tests/test_t1_official.py tests/test_t2_gsm.py tests/test_t3_t4.py tests/test_tracer_t1_prepare.py tests/test_science.py tests/test_cli_pipeline.py -q --tb=short` | **61 passed**，exit 0。通过不能关闭下列仍可用独立反例触发的缺陷。 |
| X-02 | 全量本机 pytest | `python -m pytest tests -q --tb=line` | **70 passed**，exit 0，约 10.0s。无 skip/xfail。与作者 `pytest_author_claim` 计数一致，仍不是科学正确性证据。 |
| X-03 | 矩阵 `noise=None`（原 B-01） | `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `S.noise=None`，`S.excess=None`，`rho_S_noise=None`，`null_reason=noise_missing`。原触发保持关闭。 |
| X-04 | 有限扫描 `no_response_observed_in_scan`（原 B-02） | 仅 `outcome=no_change` + 该 scan_state | `behavior_label=None`，`behavior_known=False`。原触发保持关闭。 |
| X-05 | 单次 `observed_response` + `no_change` 且 `exhaustive=False`（原 B-23） | 同上但 `scan_state=observed_response` | **`behavior_label=None`，`behavior_known=False`。原 B-23 触发关闭。** |
| X-05b | `exhaustive=True` + `observed_response` + `no_change` | 同上 | `behavior_label=0`，`behavior_known=True`。API 现要求两旗标同时成立。 |
| X-06 | sham 不进入 R_behavior（原 B-03） | 编辑 no_change + `sham:0` changed + 匹配协议 | `behavior_label=0`，`noise_ref=1.0`，`opportunities=1`。原触发保持关闭。`evidence_ids` 仍含 sham。 |
| X-07 | 出现删除后独立解析再对齐（原 B-04） | `parse_fixture_events("q = 1\\nq = 2\\n")` vs `"q = 2\\n"` | `pairs=[]`；`structural.merged` 非空；`ambiguous=[{q,2 vs 1}]`。删除错位保持关闭。 |
| X-08 | 等计数出现对仍按 version zip | `"q = 1\\nq = 2\\n"` vs `"q = 9\\nq = 2\\n"` | 配成 `(1,9),(2,2)`。等计数结构替换仍会静默对齐。 |
| X-09 | R_surf vs 图父母（原 B-06 / B-25） | `"q = 0\\n"`；`"q = 0 mentions p1\\n"`；`"using p1, q = 0\\n"` | 父母 `['p1','p2']`。裸赋值 surface `[]`。**值后 `mentions p1` 现为 `['p1']`，事件文本为整行。** 赋值前同样检出。下一行单独 `mentions p1` 不成事件。原 B-06/B-25 触发关闭。 |
| X-10 | HumanEval 族（原 B-07） | `load_humaneval(t3_humaneval_one.json)` | `base_group_id=HumanEval/0`。`assign_split("HumanEval")` 仍为 `probe_train`，加载器已不用该截断键。 |
| X-11 | 公式编辑（原 B-08） | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，premise 文本/值 `5`，node `8`，answer `8`。保持关闭。 |
| X-12 | 数值子串（原 B-09） | 文本 `has 13 apples`、值 `"3"` | `ValueError: value '3' is not an isolated token`。保持关闭。 |
| X-13 | 小数后缀（原 B-24） | 文本 `p1 = 3.5`、值 `"5"` → `"9"` | **抛 ValueError。原 3.5/5 触发关闭。** |
| X-13b | 整数声明值是小数的整数部分 | `_replace_isolated_value("p1 = 5.5","5","9")`；`"p1 = 5.0"` | **不抛错**；分别变成 `p1 = 9.5`、`p1 = 9.0`。见 B-24 残余。 |
| X-14 | no-op 抢 span（原 B-10） | 前端注入 `"p1 = 4 is a red herring."` | 原 p1 span `[25,31]`，切片等于 `"p1 = 4"`。原触发保持关闭。无祖先重算。 |
| X-15 | CSP 空父母（原 B-11） | `task_parents=[]` + `graph_status=unknown` | `csp=None`，`clean_matched=0`。保持关闭。 |
| X-16 | CSP 空父母 + `complete` | 同上但 `graph_status=complete` | `csp=0.0`，`clean_matched=1`，`coverage=1.0`（把空锥当干净）。 |
| X-17 | `assign_family`（原 B-13） | 不传 `family_id`；同 id 不同成员子集 | **缺 id 抛 `ValueError`。** `{A,B,C}` / `{B,C}` / `{Z}` 同 `family_id` 均为 `probe_train`。原 B-13 触发关闭。 |
| X-18 | GSM-Plus 默认划分（原 B-14） | `assign_split("gsmplus-1")`；`assign_split(loaded.base_group_id)`；自造 `original_id=gsm8k-1` | `gsmplus-1` → `test`（子串锁）。夹具 `base_group_id=gsm8k-12` 的裸 `assign_split` **碰巧也是 test**。`original_id=gsm8k-1` 的 Plus 记录：`metadata.role=test`，但 **`assign_split("gsm8k-1")=="probe_train"`**。见 B-14。 |
| X-19 | 跨集族键（原 B-15） | 同题夹具 Symbolic vs Plus | 两边均为 `gsm8k-12`（夹具新增 `original_id`）。去掉 `original_id` 后 Plus 退回 `gsmplus-1`。官方 Plus 字段无 `original_id`。见 B-15。 |
| X-20 | T3 编辑 / 组成图 | `document_edit`；`paragraph_edit`；`apply_spec_edit`；`ancestors(musique[0])` | 现产出 `Task`/`Edit`。无 `new_answer` 时 `needs_truth`。有答案则直接标 `valid`、不核验。`anc={s1:{p0},s2:{p0,p1}}`。文档替换把同一文档全部句子写成同一字符串。 |
| X-21 | CLI prepare/label | `main(["prepare", …, "--sham-opportunities","1"])`；再 `label` | 默认改 `p2`：真实 `changed`。sham `no_change` 仍 `scan_state=observed_response`，`premise_id=p2`。`behavior_label=1`，**`noise_ref=0.0`**（钉在编辑前提）。密度 `null_reason=noise_set_empty`。label 复用 hits。 |
| X-21b | CLI 已观察 no_change 的 scan_state | `--edit-premise p1 --edit-value 7`（q 仍为 0） | `outcome=no_change`，**`scan_state=no_response_observed_in_scan`**，`exhaustive=False`，`behavior_known=False`。合成轨迹其实观察到了值。 |
| X-22 | 多节点 target vs 第一祖先 | 内存 s=p1+p2、t=s+p3 | `next(iter)={p1,p2}`，`target={p1,p2,p3}`，`union={p1,p2,p3}`。CLI 现用 `anc.get(task.target)`，不再取第一项。仍是题级一袋，不是逐事件 T。 |
| X-23 | 空 `noise_set` + 有协议（原 B-26） | 集合密度 API | `noise_set=[]` 且无 truthy `hits` → `excess=None`，`null_reason=noise_set_empty`。**原触发关闭。** 若 `noise_set=[]` 但 `sham_protocol["hits"]=["p3"]`，则 **`rho_S_noise=0.0`，`excess=raw`**。 |
| X-24 | 多匹配行 / 非法 scan_state（原 B-27） | `"q = 0 q = 1\\n"`；`scan_state="not_a_real_state"` | 现保留两条 `status=ambiguous` 事件，不再静默丢弃。非法 scan_state 抛 `ValueError`。原静默丢弃 / 脏枚举关闭。 |
| X-25 | 源码检索 | `rename` / `source_value` / `apply_spec` / `review_export` / `exhaustive` | `apply_rename_edit` / `apply_source_value_edit` / `apply_spec_edit` 存在。**无 `review_export`。** `exhaustive` 只在 schema 默认与 `build_labels` / CLI 透传；`apply_value_edit` 从不置 True。改名不改节点表达式（题干 `alpha`，表达式仍 `p1 * p2`）。 |
| X-26 | 官方夹具重算（原 B-19） | `recompute(load_igsm_snapshot(...))`；篡改 dump 答案为 8 | 夹具 9=9。**答案不一致则拒绝。** 原缺校验关闭。 |
| X-27 | 除法模运算 | `_eval_expr("5 / 2", {}, 23)` | `2`（`int(truediv)%mod`），不是模逆 14。 |

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上 |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 | 无官方 dump；机制层 B-15 已确认 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b`。见 U-01 |
| N-07 | 复现声明聚合 hash | 本轮已按文档化配方复现，无需再搜未文档化算法 |

## 5. 作者 `fixed_pending_review` 的独立结论

不得因回归测试绿或 `ISSUES.md` 成文而关闭。下表针对 **round-01/02 原触发**；残余另列。

| 原 ID | 作者主张 | 独立结论 | 证据 |
|---|---|---|---|
| B-06 | fixed（span） | **原触发关闭** | X-09：不再抄父母；值后同句提及进入 surface。作者本轮补了 `test_b06_surface_mentions_include_text_after_value`，独立复现一致。 |
| B-13 | fixed（require family_id） | **原触发关闭** | X-17：缺 `family_id` 拒绝；同 id 不同子集角色相同。作者 `test_b13` 仍不测子集稳定性，但不妨碍独立关闭。 |
| B-14 | fixed（gsmplus token） | **未关闭（生产族键路径）** | X-18：`assign_split("gsmplus-1")=="test"` 只关原子串触发。加载后 `base_group_id` 是 `original_id`（官方 Plus 通常没有该字段，FEATURES 列出的是 `seed_question`）。`gsm8k-12` 哈希**碰巧**为 `test`（30 个 `gsm8k-i` 里仅 4 个 test；`gsm8k-1` → `probe_train`）。自造 Plus + `original_id=gsm8k-1`：`metadata.role=test`，裸 `assign_split(base_group_id)=="probe_train"`。作者 `test_b14` 只走 `source=` / `test_only=True`。 |
| B-23 | fixed（exhaustive） | **原触发关闭；CLI 仍写错 scan_state** | X-05：无 `exhaustive` 的 `observed_response`+`no_change` 现为 unknown。X-21b：prepare 把已观察的合成 no_change 写成 `no_response_observed_in_scan`，且从不把 `Edit.exhaustive` 置 True。 |
| B-24 | fixed（decimal） | **原触发关闭；残余仍缺陷** | X-13 关闭 3.5/5。X-13b：整数分支 lookahead 是 `(?!\d)` 不是 `(?![\d.])`，`5.5`/`5.0` 的声明值 `"5"` 仍被改成 `9.5`/`9.0`。作者 `test_b24` 只覆盖 3.5/5。 |
| B-26 | fixed（empty noise） | **原触发关闭；API/CLI 不一致仍在** | X-23：空 `noise_set` 且无 hits → null。X-21：密度 null，但 `Label.noise_ref=0.0` 且钉在编辑前提。空 `noise_set` + truthy `hits` 仍把噪声写成 0。 |

`ISSUES.md` 未要求本轮关闭的 B-05/12/15/16/17/18/21/22 及 B-04 等计数残余多数仍在。T3 编辑/iGSM 重算/改名函数的**存在**不等于协议完成。

## 6. 发现（本轮仍开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐或划分会被污染；`medium` = 协议要求的适配/字段缺失；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B-05 策略分岔从未检出；`scanned=True` 仍冒充已扫描

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `events.align_events`  
- **行号：** `events.py` 114（`strategy_changed` 只收集 `status=="strategy_change"`）；`events.py` 117（`scanned: True`）；`parse_fixture_events` 从不写该 status  
- **触发：** 任意对齐  
- **协议：** STRUCT-01：消失、合并、版本变化、策略分岔单独报告。  
- **证据：** X-07 现会填 `merged`（2→1）。X-25/B-05：普通值变化对齐 `strategy_changed=[]` 且 `scanned=True`。`schema.Alignment` 仍未被对齐函数使用。  
- **影响：** 空策略列表冒充「已检测、无此类事件」。合并计数本身已比 r02 完整。  
- **建议：** 实现策略分类或把 `scanned` 限于真实跑过的检测器。

---

### B-12 CLI 密度仍不是事件级标签；sham 被钉在编辑前提

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `cli.cmd_prepare` / `cmd_label`；`measure.build_labels`  
- **行号：** `cli.py` 154–155, 166–179, 188–199, 302–320；`measure.py` 54–59  
- **触发：** `reasoning-diff prepare`（尤其 `--sham-opportunities>0`）与 `label`  
- **协议：** MEAS-01/02：ρ 分母是该事件的 `P\R_task` 与 `R_task`；无编辑随机变化不得强加前提身份。  
- **证据：**  
  1. `task_set` 现取 `anc[target]`（X-22：多节点不再误取 s 的祖先）。仍是**题级一袋**，不是逐事件 T。  
  2. `behavior_set` 来自 `behavior_label==1` 的前提，比 r02「任一事件 changed」好，仍不是逐事件 R_behavior。  
  3. sham 观察写死 `premise_id=premise_id`（正在编辑的前提）。X-21：`noise_ref=0.0`，`evidence_ids` 含 `obs:sham:q:p2`。  
  4. 密度因 `hits=[]` 走 `noise_set_empty` → excess null，与标签层 `noise_ref=0.0` **互相矛盾**。  
  5. X-21b：已观察的合成 no_change 被标成 `no_response_observed_in_scan`。  
- **影响：** 端到端 densities 仍不是事件级；启用 sham 时标签层会写出钉在错误前提上的噪声 0。  
- **建议：** 按事件取 T；sham 不带 premise_id；label 与 density 共用同一 null 规则。

---

### B-14 GSM-Plus test-only 锁仍可被默认 `assign_split` 绕过

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `splits.assign_split`；`t2_gsm_plus.load_gsm_plus`  
- **行号：** `splits.py` 9, 19–21；`t2_gsm_plus.py` 25, 45  
- **触发：** 对已加载 Plus 记录的 `base_group_id`（`original_id` / 官方记录的 GSM8K 族键）调用裸 `assign_split`，或不传 `source` / `test_only`  
- **协议：** DATA-03；FEATURES：GSM-Plus 数据卡禁止训练，必须固定为评测来源。  
- **证据：**  
  1. 子串锁只认 token 里的 `gsmplus` / `gsm-plus`。生产族键在有 `original_id` 时是 `gsm8k-*`，**不含**该子串。  
  2. 夹具 `gsm8k-12` 的 sha256 划分**碰巧**落在最后 15% 的 `test`。`gsm8k-0..29`：13 个 `probe_train`、4 个 `test`。  
  3. 独立构造 `original_id=gsm8k-1` 的 Plus JSON：`lock_test_only` 贴纸为 `test`，`assign_split("gsm8k-1")=="probe_train"`。  
  4. 作者 `test_b14` / `test_gsm_plus_is_test_only` 不测裸 `assign_split(loaded.base_group_id)`。  
- **影响：** 公开 test 变体可进入 `probe_train` / `dev` / `direction_fit` / `calibration` / `transfer_pairs`。夹具碰巧为 test，回归全绿。  
- **建议：** `assign_split` 必须看 `source` / `fit_eligible`；禁止只靠 id 子串；测试用哈希到 `probe_train` 的族键。

---

### B-15 跨数据集族键在官方 Plus schema 上仍不一致

- **状态：** confirmed defect（机制）/ pending_server（真实 dump 碰撞率）  
- **严重度：** high  
- **符号：** `t2_gsm_symbolic.family_id` vs `t2_gsm_plus.load_gsm_plus`  
- **行号：** `t2_gsm_symbolic.py` 11–12, 46；`t2_gsm_plus.py` 25  
- **协议：** DATA-03 / FEATURES：以规范化 `seed_question` 连接 GSM8K ID；不同数据集同源题同族。  
- **证据：** X-19：夹具因**新增** `original_id` 而两边都是 `gsm8k-12`（夹具 digest 相对 r02 已变）。去掉该字段后 Plus 族键为 `gsmplus-1`。FEATURES 所列官方 Plus 字段是 `question/solution/answer/perturbation_type/seed_*`，**没有 `original_id`**。无 `seed_question` 规范化匹配。  
- **影响：** 真实 dump 上同题仍可一边 train 一边 test。夹具对齐不能外推。  

---

### B-16 T3「合法编辑 + 更新真值」仍是调用方口述

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `t3_hotpot.document_edit`；`t3_musique.paragraph_edit`；`t3_humaneval.apply_spec_edit`  
- **行号：** `t3_hotpot.py` 51–86；`t3_musique.py` 27–42, 72–93；`t3_humaneval.py` 34–56  
- **协议：** DATA-02：替换支撑文档后更新受影响答案；HumanEval-Perturb 改 Spec 并以新测试为裁判。  
- **证据：** X-20。无 `new_answer` 时标 `needs_truth`（比 r02 诚实）。传入任意字符串即 `validity=valid`，不对照文档/测试。Hotpot 把同一 `document_id` 的**全部句子**写成同一 replacement（`DocA:0` 与 `DocA:1` 均变成 Spain 句）。`ancestors(musique)` 仍把组成图当 R_task。`test_t3_t4.py` 不调用 `paragraph_edit` / `apply_spec_edit`，也不断言新答案。  
- **影响：** T3 仍无法做经核验的反事实；若消费 `ancestors(musique)` 则组成图进入 ρ。  

---

### B-17 用题干前 N 个字符伪造前提列

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `load_gsm_plus` / `load_gsm_symbolic`（无 sidecar）/ `load_humaneval` / `load_t4`  
- **行号：** `t2_gsm_plus.py` 22；`t2_gsm_symbolic.py` 43；`t3_humaneval.py` 21；`t4_boundary.py` 26  
- **协议：** 未知图应 unknown，不得填假前提列冒充可评估 P。  
- **证据：** X-18/X-20/T4：Plus `"Ada has 4 ap"` `kind=fact`；Symbolic `"Ada has "`；HumanEval spec 前 40 字符；T4 `"What is x "`。`graph_status` 多为 unknown（此项正确）。CLI prepare 只过滤 `kind=="placeholder"`，这些列进得了分母。  
- **影响：** 若下游用 `premises` 当 P，ρ_S 分母是伪造的。  

---

### B-18 DATA-01 的改名 / 来源—数值 / 人工复核仍不完整

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `edits.apply_rename_edit` / `apply_source_value_edit`；缺失 `review_export`  
- **行号：** `edits.py` 144–184  
- **协议：** DATA-01：数值/改名/no-op/来源—数值变体。MEAS-01：可导出与回填人工复核。论文：先 a=b 再 a≠b 的来源解耦对。  
- **证据：** X-25。改名后题干 `alpha = 4`，节点表达式仍 `p1 * p2`，`after` 是反向映射。`source_value` 只是给 `apply_value_edit` 打旗标并重算（p2:0→3，答案 12），不构造解耦对。全包无 `review_export`。  
- **影响：** C2 解耦资产无法从数据层按协议生成。函数存在不等于 DATA-01 完成。  

---

### B-21 GSM-Plus 扰动类型映射不完整 / 映射错误

- **状态：** confirmed defect  
- **严重度：** low  
- **符号：** `t2_gsm_plus.load_gsm_plus`  
- **行号：** `t2_gsm_plus.py` 15–21  
- **协议：** FEATURES / 01-03-PLAN：`reversing operation` 是改查询量（计划名 `query_target_change`）；`critical thinking` 含信息不足，**不是**约束矛盾。  
- **证据：** 独立喂八类名：`reversing operation` → `query_reversed`（**不在** `T4_STATUSES`）；`critical thinking` → `inconsistent_constraints`（与 FEATURES 相反）；其余六类 `status=None`。夹具 `numerical substitution` 的 `answer_spec.status is None`。  
- **影响：** 边界状态无法用于 T4 相图或过滤；critical thinking 会被错当成矛盾约束。  

---

### B-22 P2 分母仍可只是调用方传入的整数

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `analysis.p2_paired`  
- **行号：** `analysis.py` 67–96  
- **协议：** P2 必须同时报告完整密度、共同已有前提变化、新增注入列。  
- **证据：** `p2_paired(..., 99)` 原样返回 `shared_denominator=99`、空前提列表、`status=ok`。传入 `shared_premises` 时才会数长度。`make_noop_pair` 仍不计算共同分母。  
- **影响：** 报告可以看起来「有分母」而没有共同支持集合。  

---

### B-24 `apply_value_edit` 的整数隔离仍会改到小数的整数部分

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `edits._replace_isolated_value`  
- **行号：** `edits.py` 95–98（无点的 old 用 `(?<![\d.])…(?!\d)`，点不算数字）  
- **触发：** `premise.value="5"`，span 为 `p1 = 5.5` 或 `p1 = 5.0`  
- **协议：** DATA-01：只改声明字面量整记号。  
- **证据：** X-13b：`5.5`→`9.5`，`5.0`→`9.0`。原 3.5/5 因 lookbehind 看到点而关闭，覆盖不了「声明值等于小数的整数部分」。  
- **影响：** 带小数的 T2 sidecar / Plus 数值替换会改错数并重算错误新答案。  
- **建议：** 整数与小数统一 `(?<![\d.])…(?![\d.])`；失败则 invalid。  

---

### B-04 残余：等计数出现对仍按 version zip

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `events.align_events`  
- **行号：** `events.py` 94–95  
- **证据：** X-08。删除错位（不等计数）已关闭。等计数结构替换仍静默配成值变化。  
- **协议：** PITFALLS#1：插入/替换重复计算会使按出现序号硬配对偏移。  

---

### B-10 残余：no-op 仍无祖先 / 答案不变证明

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `t2_noop.make_noop_pair`  
- **行号：** `t2_noop.py` 14–20, 40–46（调用方布尔自证）；digest 与 r02 相同  
- **证据：** X-14 span 正确。无重算、无祖先相等断言。`injected_non_ancestor=True` 是传入 True 的回写。  

## 7. 已独立关闭的原触发（非本轮缺陷）

仅关闭 **已复现的原触发**。不把 ISSUES 整行标 closed。

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01 | X-03 矩阵缺噪声为 null | — |
| B-02 原 scan_state | X-04 | CLI 把已观察 no_change 写成该状态（X-21b） |
| B-03 | X-06 | sham 仍钉在 premise_id；label 写 noise 0 |
| B-04 删除错位 | X-07 | 等计数 zip（X-08） |
| B-06 / B-25 | X-09 整行 surface | 只匹配 `premise_id` 词（U-03） |
| B-07 | X-10：`HumanEval/0` | — |
| B-08 | X-11 | — |
| B-09 整数子串 | X-12 | B-24 残余 |
| B-10 span | X-14 | 无祖先/答案不变证明 |
| B-11 unknown 空父母 | X-15 | `complete`+`[]` 仍当干净（X-16） |
| B-13 | X-17 强制 `family_id` | CLI 仍不调用 `assign_family`（改用 `assign_split(base_group_id)`，可接受） |
| B-19 缺校验 | X-26 不一致 dump 被拒 | pending_server 真实 dump |
| B-20 解析器撞车 | 身份现用 `node.id`（`events.py` 44–46） | 组成图仍被 `ancestors()` 消费（B-16） |
| B-23 API | X-05 unknown | CLI 永不置 `exhaustive=True` |
| B-26 空集当 0 | X-23 `noise_set_empty` | hits/空集不一致；label `noise_ref=0.0` |
| B-27 静默丢弃 / 非法 scan_state | X-24 保留 ambiguous；枚举校验 | 歧义事件仍可进入 zip |

`build_labels` 已在 `cmd_prepare` / `cmd_label` 接线；prepare 用 `target` 祖先。这关闭了 r01/r02「第一节点当 T」的一半，**不**关闭 B-12 的题级分母与 sham 钉身份。

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径 S/M 与缺 sham → null | `measure.py` 100–112 | 缺协议或 `noise_set is None` 时 excess null；负差不截断。不否定 B-26 残余。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | fixture 拒 official；官方拒仅有 G；lookup 不进重算。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–20 | 中间节点不进入列索引。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | `EventIdentity.key()` 为 JSON of entity/version/scope。 |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 231–239 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` 37–42 | `graph_status=unknown`。不否定 B-14/15/17。 |
| ND-07 | Hotpot 声明 supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 35–38 | 不否定 B-16。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | 不从标题推断。 |
| ND-09 | HumanEval 不在宿主 exec | `scoring.py` 19–29 | `executor_unavailable` 时 value/denominator null。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` 37–45 | `reasoning_diff_noop`，`official_noop_release=False`。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 122–128 | `b <= limit`。 |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` | `splits.py` 50–68 | 原语正确；不否定 B-14。 |
| ND-13 | T1 配置拒绝非白皮书格子 | `t1_config.py` 9–21 | |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 56–58 | |
| ND-15 | `parse_failed` / 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05。 |
| ND-16 | 官方加载对照 template 重算 | `t1_official.py` 77–80 | X-26。不把「有校验」写成「全量官方数据已验收」。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；API 已关 B-23 原触发，CLI 仍写错字段 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod`（5/2 mod 23 = 2，模逆 14） | FEATURES 称官方 Num 为加减乘；夹具无除法。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official`（X-25：`after=official`，答案 12） | 可解释为题源而非「该行是官方发布」。需协议裁定。 |
| U-03 | `surface_mentions` 只匹配 `premise_id` 词，不抽符号/别名 | SURF-01 写「名称与符号引用」。官方 iGSM 夹具 id 即 `a`/`b`，X-25 能检出 `a`。未在真实题干别名上抽样。 |
| U-04 | 后续 stage 是否用 `task_id` 而不是 `base_group_id` 做划分 | CLI fit 只信 `--split` 旗标。prepare 写 `splits.jsonl` 但不被 fit 读取。 |
| U-05 | 同一步跨行的表面提及是否应并入赋值事件 | 解析器以换行切事件。协议写「步骤文本」。未升格，因本仓库事件=行。 |

## 11. 测试质量对本通道的含义

**70 passed ≠ 数据/测量正确。** 作者回归覆盖了若干原触发，但：

- `test_b14` 不测裸 `assign_split(loaded.base_group_id)`，也不用哈希到 `probe_train` 的族键。夹具 `gsm8k-12` 碰巧为 `test`。  
- `test_b24` 不测 `5.5`/`5.0`。  
- `test_b13` 不测同 id 不同子集（独立已关，但测试仍弱）。  
- 无 `test_b26`；无多节点逐事件 T；无官方 Plus 缺 `original_id` 的族键断言。  
- `test_t3_t4` 不跑 `paragraph_edit` / `apply_spec_edit`，Hotpot 编辑不断言新答案。  
- `test_full_cli_smoke` 只查 exit 0 与 `report.status==not_evaluated`。  
- Plus 夹具相对 r02 被改进 `original_id`，使 B-15 在夹具上「看起来齐」，与官方 schema 不符。

因此不能把 ISSUES 中 B-06/13/14/23/24/26 整行标为已关闭。B-06/13/23 的**原触发**可独立关闭；B-14 与 B-24 残余不能关。

## 12. 通道结论

数据与测量通道 **不能** 在本冻结对象上给出通过意见。

1. **`HASH_MATCH`：** 声明冻结 hash 已按 VERSION 配方复现；结论绑定上表逐文件 digest。  
2. **可独立关闭的原触发（本轮新关）：** B-06/B-25 span、B-13 `family_id`、B-23 API、B-26 空集当 0、B-19 加载重算。先前已关且仍关：B-01、B-02（仅该 scan_state）、B-03 行为袋、B-04 删除错位、B-07、B-08、B-09 整数子串、B-10 span、B-11 unknown 空父母、B-27 静默丢弃。  
3. **作者标 fixed 但独立复开 / 未关：** **B-14**（生产族键 + 夹具哈希巧合）、**B-24**（`5.5`/`5.0`）。  
4. **本轮仍确认的结构性缺口：** B-05 策略空扫描、B-12 sham/题级密度、B-15 官方 Plus 族键、B-16 T3 口述真值、B-17 占位前提、B-18 改名/解耦/复核不完整、B-21 扰动映射、B-22 P2 整数分母、B-04 等计数 zip、B-10 无祖先证明。  

集合密度 raw/null/signed 路径、T1 来源隔离、官方 dump 对照重算仍成立（ND-01–ND-16），不能抵消划分泄漏与编辑隔离残余。真实官方全量保持 `pending_server`。即使服务器数据到达，**B-14 会在 `gsm8k-*` 族键上把 Plus 划进 `probe_train`**，B-24 会在小数整数部分上改错数。
