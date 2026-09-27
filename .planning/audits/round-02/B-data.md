# Review B — 数据与测量（独立审查，round-02）

本报告不假设实现正确，不把 `ISSUES.md` 的 `fixed_pending_review` 当作已关闭。未修改任何生产代码、测试或夹具。未下载数据或权重。未阅读其他 round-02 通道报告。round-01 `B-data.md` 只用作待复验清单与行文格式，不作为证据。

**冻结核验：`HASH_MISMATCH`。** 声明值 `2676a0983f6b42148202eedfbfaea44ce207d1fd386b8d47cbc909e983c5cc38` 无法用已文档化的「POSIX relpath + 文件字节」聚合复现。审查对象是下方逐文件 SHA-256 所锚定的当前工作树，不是已核验的冻结快照。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-02） |
| review_time | `2026-09-21T00:44:00+08:00`（复算 hash / 开读）— `2026-09-21T00:55:00+08:00`（成文） |
| declared_frozen_hash | `2676a0983f6b42148202eedfbfaea44ce207d1fd386b8d47cbc909e983c5cc38`（`.planning/audits/round-02/VERSION.md`） |
| independently_recomputed_hash | **`HASH_MISMATCH`**。55 个范围内文件集合与 VERSION「55 files」一致。按 `as_posix()` 排序后逐文件 `relpath.encode() + b"\0" + bytes` 得到 `7b6680d6d937097fd02841d5950df1a7b3498ebcd1965381220b5e429ec5c617`。另试：纯字节、path+bytes、path+NL+bytes、sha256sum 列表、LF 规范化、长度前缀、merkle hex、path+filedigest 等，均不等于声明值。范围内文件无 CRLF。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿单独信任 HEAD） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否 |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对测量/划分调用链而通读；`fixture` = 对照适配器读完。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 242 | `2d9272406879cbf9a21b367c75d52caf373f9d03ddb10c020026a3e2b599b3e7` | full 1–242 | 标签、S/M、噪声、TO/CSP、有限扫描、分母 |
| `src/reasoning_diff/events.py` | 125 | `1d1d3413601c48343c26d6d6dcc0519e8cbbe537dec0a5fce9239a18a4d7897c` | full 1–125 | 身份、对齐、结构变化、R_surf span |
| `src/reasoning_diff/graphs.py` | 44 | `1e287cebf844cec0d055138224ae5a0b39c0358228c6587e8b4b6d4cfc604241` | full 1–44 | 前提祖先、unknown/complete、cone |
| `src/reasoning_diff/edits.py` | 141 | `6226f3adc81dda92210fd8ea1b6e78651f492a74d041e7d71ce6c8f0c935c1cd` | full 1–141 | 孤立记号、重算、禁止 lookup |
| `src/reasoning_diff/splits.py` | 75 | `a62d819bf99ceb137f326b980833b425f296cd3caff04b5971351628aa6fcc63` | full 1–75 | 共组、test-only、family_id、默认泄漏 |
| `src/reasoning_diff/schema.py` | 371 | `c07301be5fabd647797c19ec32dc841c09dae26e8a7d7c027fc7ecd5146ff5c1` | full 1–371 | 枚举、身份、scan_state、exhaustive |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 39 | `5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0` | full | 加载分派，不补图 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 83 | `2e83cc052a518d43bfebd3ab3899a37ad5f369f36a29d5eedb95cbd3e48e969b` | full | template≠G、shared RNG、lookup、加载不重算 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 51 | `0da626321ee5d786f3c3b4c7da52687b3c9ca2d233eebe81f2d43f22c0cf3a8f` | full | test-only 贴纸、族键、占位前提 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 70 | `e8fc9d046ba130066e0acd7948b27b44abd663bdc45e5fe03f81c53244657f19` | full | sidecar、公式编辑、跨集族键 |
| `src/reasoning_diff/tasks/t2_noop.py` | 80 | `26cf5c21b5838a6bf1a335bf8b0eb5bc767a77c2e4128fc8a36a8c482456c874` | full | prefer_from span、无祖先证明 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 59 | `a79ab16c0ebdae7fde154df79bdfd8d0ae38d5337473a5f6a4241c2f7c3930c1` | full | supporting_facts≠DAG、无更新真值 |
| `src/reasoning_diff/tasks/t3_musique.py` | 69 | `095f10acc7c4600f607b2a6d5fbb6e0bd5962d0f7ccc881d79efbbfd136c3e58` | full | 组成图当 ancestors、无文档编辑 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 35 | `c77e136ceb6e6f7141d8b29470fc570851f7fb4bdf4c54a8a93e87be16cabeb6` | full | 完整 task_id 族、无 Spec 编辑 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 33 | `a2ca9188353b213d2c7c617dd27c60415adb0c16c40326ae8a7ecce03f94a5f9` | full | 四态显式、占位前提 |
| `src/reasoning_diff/cli.py` | 419 | `9ae87fe24abfeb635eec192b84f2a28162a2015b19f45aa551250b336bffab48` | callsite 78–247 | prepare/label 是否真正调用测量 API |
| `src/reasoning_diff/analysis.py` | 131 | `146ca012939ed23c5044121bb45f56300677d47fc89e0e4f2ef896ac8e95c50b` | callsite 64–70 | P2 分母是否只是透传 |
| `src/reasoning_diff/scoring.py` | 30 | `d05822c4fb784fe4a57d9f82f583eaa31c0f3b2e0e96c04b81f77db7413433f8` | callsite | 域内评分分母 |
| `tests/test_review_regressions.py` | 315 | `30b02a41dca7288595827dbdedcbe3ceb681cd28bd8077d8abe53d1951648346` | full | 作者回归是否覆盖原触发 |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 40 | `54e57fea7417d901c75b7d17cfe9b90ee442f2d634a08d22272a678959ce9650` | full | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/test_science.py` | 97 | `3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c` | full | |
| `tests/test_cli_pipeline.py` | 29 | `63b4c09f51f6c7d807e8928f27fa62ec54e3f4656229b3615371ae930b5de0b9` | full | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 round-01 相同，未改真值）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `81ac53c4…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

`graphs.py` / `t1_official.py` / `t2_gsm_plus.py` / `t3_hotpot.py` / `t3_musique.py` 的 digest 与 round-01 相同：这些适配器本轮没有针对 B-15/16/19/21 的生产修复。

## 3. 已执行检查

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-01 | 作者声明的数据回归 + 本通道测试 | `python -m pytest tests/test_review_regressions.py tests/test_measure.py tests/test_t1_official.py tests/test_t2_gsm.py tests/test_t3_t4.py tests/test_tracer_t1_prepare.py tests/test_science.py tests/test_cli_pipeline.py -q --tb=short` | **56 passed**，exit 0。通过不能关闭下列仍可用独立反例触发的缺陷。 |
| X-02 | 全量本机 pytest | `python -m pytest tests -q --tb=line` | **65 passed**，exit 0，约 10.0s。无 skip/xfail。与作者 `pytest_author_claim` 计数一致，仍不是科学正确性证据。 |
| X-03 | 矩阵 `noise=None`（原 B-01 / X-04） | `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `S.noise=None`，`S.excess=None`，`rho_S_noise=None`，`null_reason=noise_missing`。原触发关闭。 |
| X-04 | 有限扫描 `no_response_observed_in_scan`（原 B-02 / X-05） | 仅 `outcome=no_change` + 该 scan_state | `behavior_label=None`，`behavior_known=False`。原触发关闭。 |
| X-05 | 单次 `observed_response` + `no_change`（B-02 残余） | 同上但 `scan_state=observed_response`；`Edit.exhaustive` 未读 | `behavior_label=0`，`behavior_known=True`。见 B-23。 |
| X-06 | sham 不进入 R_behavior（原 B-03 / X-06） | 编辑 no_change + `sham:0` changed + 匹配协议 | `behavior_label=0`，`noise_ref=1.0`，`opportunities=1`。原触发关闭。`evidence_ids` 仍含 sham。 |
| X-07 | 出现删除后独立解析再对齐（原 B-04 / X-08） | `parse_fixture_events("q = 1\\nq = 2\\n")` vs `"q = 2\\n"` | 左 version 1,2；右重编号为 version 1 值 `2`；`pairs=0`，`ambiguous=[{q,2 vs 1}]`。原触发关闭。`merged=[]`，`strategy_changed=[]`。 |
| X-08 | 等计数出现对仍按 version zip | `"q = 1\\nq = 2\\n"` vs `"q = 9\\nq = 2\\n"` | 配成 `(1,9),(2,2)`。等计数结构替换仍会静默对齐。 |
| X-09 | R_surf vs 图父母（原 B-06 / X-10） | `"q = 0\\n"`；`"q = 0 mentions p1\\n"`；`surface_mentions("q = 0 mentions p1")` | 父母 `['p1','p2']`，`"q = 0"` 的 surface `[]`（不再抄父母）。同句值后的 `mentions p1` 因事件 span 止于数值匹配而 **surface 仍为 []**；对完整行调用 `surface_mentions` 则得到 `['p1']`。见 B-06 / B-25。 |
| X-10 | HumanEval 族（原 B-07 / X-11） | `load_humaneval(t3_humaneval_one.json)` | `base_group_id=HumanEval/0`。`assign_split("HumanEval")` 仍为 `probe_train`，但加载器已不再使用该截断键。 |
| X-11 | 公式编辑（原 B-08 / X-12） | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，premise 文本/值 `5`，node `8`，answer `8`。原触发关闭。 |
| X-12 | 数值子串（原 B-09 / X-13） | 文本 `has 13 apples`、值 `"3"` | `ValueError: value '3' is not an isolated token`。原触发关闭。 |
| X-13 | 小数后缀（B-09 残余） | 文本 `p1 = 3.5`、值 `"5"` → `"9"` | **不抛错**；题干变成 `p1 = 3.9`。见 B-24。 |
| X-14 | no-op 抢 span（原 B-10 / X-14） | 前端注入 `"p1 = 4 is a red herring."` | 原 p1 span `[25,31]`，注入 `[0,…)`，切片等于 `"p1 = 4"`。原触发关闭。无祖先重算。 |
| X-15 | CSP 空父母（原 B-11 / X-17） | `task_parents=[]` + `graph_status=unknown` | `csp=None`，`clean_matched=0`。原触发关闭。 |
| X-16 | CSP 空父母 + `complete` | 同上但 `graph_status=complete` | `csp=0.0`，`clean_matched=1`，`coverage=1.0`（把空锥当干净）。 |
| X-17 | `assign_family` | 同 `family_id` 不同成员子集；无 `family_id` 的子集 | 有 `family_id` 时角色相同。无 id 时 `{A,B,C}→test`、`{B,C}→calibration`。见 B-13。 |
| X-18 | GSM-Plus 默认划分（原 B-14 / X-16） | `assign_split("gsmplus-1")` 不传 source | **`transfer_pairs`**。`source="gsm_plus"` 或 `test_only=True` 才是 `test`。`load_gsm_plus` 只把 `metadata.role="test"` 当贴纸。见 B-14。 |
| X-19 | 跨集族键（原 B-15） | 同题夹具 Symbolic vs Plus | Symbolic `gsm8k-12`；Plus 整段 `seed_question`。不相等。 |
| X-20 | T3 编辑 / 组成图 | `document_edit`；`ancestors(musique[0])`；HumanEval 符号表 | 仍只返回 id 列表；`anc={s1:{p0},s2:{p0,p1}}`；无 `apply_spec` / `document_edit`（MuSiQue）。 |
| X-21 | CLI prepare/label | `main(["prepare", …])`；带 `--sham-opportunities 1`；再 `label` | 默认 prepare 会调用 `build_labels`，`(q,p2)` 标签接通。`task_set=next(iter(anc.values()))`。sham 时 `noise_set=[]`。label 不传 `sham_protocol`，`noise_ref=None`。 |
| X-22 | 多节点第一祖先当 T | 内存构造 s=p1+p2、t=s+p3 | `next(iter(anc.values()))={p1,p2}`，target `{p1,p2,p3}`。 |
| X-23 | 空 `noise_set` + 有协议 | 集合密度 API | `rho_S_raw=0.5`，`rho_S_noise=0.0`，`rho_S_excess=0.5`，`null_reason=None`。见 B-26。 |
| X-24 | 多匹配行 / 非法 scan_state | `"q = 0 q = 1\\n"`；`scan_state="not_a_real_state"` | 事件数 0（静默丢弃）；Observation 接受非法 scan_state。见 B-27。 |
| X-25 | 源码检索 | `rename` / `source_value` / `apply_spec` / `review_export` / `exhaustive` | 无改名/来源—数值/Spec 编辑/复核导出。`exhaustive` 只出现在 `schema.Edit` 默认字段。 |
| X-26 | 官方夹具重算 | `recompute(load_igsm_snapshot(...))` | dump 答案 9 与重算 9 一致；加载路径仍不核对。 |
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
| N-07 | 复现声明聚合 hash 的未文档化算法 | 已穷尽文档化配方；报告 HASH_MISMATCH |

## 5. 作者 `fixed_pending_review` 的独立结论

不得因回归测试绿而关闭。下表只针对 **round-01 原触发**。

| 原 ID | 作者主张 | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | fixed | **原触发关闭** | X-03：缺噪声为 null，不再 `zeros_like` |
| B-02 | fixed | **原触发关闭；残余仍缺陷** | X-04 关闭 `no_response_observed_in_scan→0`。X-05 / B-23：`exhaustive` 仍未读 |
| B-03 | fixed | **原触发关闭** | X-06：sham 不进入 `behavior_label` |
| B-04 | fixed | **原触发关闭；等计数仍 zip** | X-07 关闭删除错位。X-08 / B-04 残余 |
| B-06 | fixed | **未关闭** | X-09：不再抄父母，但值后提及被截断。作者 `test_b06` 只断言 `"q = 0\\n"` 的空 surface |
| B-07 | fixed | **原触发关闭** | X-10：`HumanEval/0` |
| B-08 | fixed | **原触发关闭** | X-11 |
| B-09 | fixed | **原触发关闭；小数残余** | X-12 关闭 13/3。X-13 / B-24 |
| B-10 | fixed | **原触发关闭；仍无祖先证明** | X-14。布尔旗标仍是调用方自证 |
| B-11 | fixed | **原触发关闭** | X-15。`complete`+空父母见 ND 旁注 |
| B-13 | fixed | **未关闭（默认路径）** | X-17：显式 `family_id` 稳定；缺省仍按成员集合哈希。`test_b13` 不测同 id 不同子集 |
| B-14 | fixed | **未关闭** | X-18：`assign_split("gsmplus-1") == "transfer_pairs"`。作者测试只走 `source=` / `test_only=True` |

`ISSUES.md` 未列的 B-05/12/15/16/17/18/19/20/21/22 本轮多数仍在。

## 6. 发现（本轮仍开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐或划分会被污染；`medium` = 协议要求的适配/字段缺失；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B-05 合并 / 策略分岔从未计数

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `events.align_events`  
- **行号：** `events.py` 101（`merged=[]`，`strategy_changed=[]` 写死）；`schema.py` 30–38, 219–226（`Alignment` 未用）  
- **触发：** 任意对齐  
- **协议：** STRUCT-01 / 论文 L78, L88：消失、合并、版本变化、策略分岔单独报告，不并入值变化。  
- **证据：** X-07。仓库无第二套对齐函数。  
- **影响：** 空列表冒充「已检测、无此类事件」。  
- **建议：** 实现结构分类；禁止用恒空列表表示已扫描。

---

### B-06 / B-25 `R^surf` 只看赋值到数值为止的截断 span

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `events.parse_fixture_events` + `surface_mentions`  
- **行号：** `events.py` 13–18, 34–35, 62  
- **触发：** 步骤文本在数值之后提及前提，如 `q = 0 mentions p1`  
- **协议：** SURF-01：表面提及记录步骤文本中的前提名称与符号引用，与图父母分开。  
- **证据：** X-09。`surface_mentions("q = 0 mentions p1") == ['p1']`，但解析器 `end=match.end()` 使事件文本变成 `"q = 0"`，surface 为空。`using p1, q = 0` 能检出（提及在赋值前）。作者回归只覆盖无提及行。  
- **影响：** 文本保留/符号替换会漏掉值后引用；surf 覆盖依赖书写位置。  
- **建议：** 对整步/整行抽提及；图父母只留在 `task_parents`。

---

### B-12 / B-26 CLI 密度仍不是事件级标签；sham 参照被写成空集 0

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `cli.cmd_prepare` / `cmd_label`  
- **行号：** `cli.py` 145–150, 238–244  
- **触发：** `reasoning-diff prepare`（尤其 `--sham-opportunities>0`）与 `label`  
- **协议：** MEAS-01/02：ρ 分母是该事件的 `P\R_task` 与 `R_task`；缺真实 sham 命中时 excess 必须 null，不能用 0 冒充噪声。  
- **证据：**  
  1. `task_set=next(iter(anc.values()), set())`：X-22 多节点时取 **s 的 {p1,p2}**，不是 target `{p1,p2,p3}`。单节点夹具碰巧正确，故测试绿。  
  2. `behavior_set` 仍是「任一事件 changed → 该编辑前提」的轨迹袋，不是逐事件 R_behavior。  
  3. prepare 在存在 `sham_protocol` 时传 `noise_set=[]`。X-23：集合 API 把空集当成噪声 0，`excess=raw`。t1_tiny 的 S 分母为空，故 CLI 输出里 excess 为 null，**测不到这条路径**。  
  4. `cmd_label` 不传 `sham_protocol`，且 `behavior_set` **不过滤 sham**。X-21：label 的 `noise_ref=None`，`evidence_ids` 含 `obs:sham:q:p2`。  
- **影响：** 端到端 densities 在多节点或启用 sham 时写错 T / 噪声；label 阶段丢掉 prepare 已算的噪声协议。  
- **建议：** 用 `target` 祖先；从 sham 观察构造 `noise_set` 或保持 null；label 复用同一协议。

---

### B-13 `assign_family` 缺 `family_id` 时仍随成员子集漂移

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `splits.assign_family`  
- **行号：** `splits.py` 42–43  
- **触发：** 不传 `family_id`；同一题族两次传入不同成员子集  
- **协议：** DATA-03 / PITFALLS#8：先按稳定基础题 ID 分组再切分。  
- **证据：** X-17。显式 `family_id` 路径独立核实稳定。默认 `key=sha256(sorted(members))`，`{A,B,C}` 与 `{B,C}` 角色不同。CLI **从不调用** `assign_family`。`test_b13` 不断言同 id 子集不变。  
- **影响：** 后到的变体可把整族打进另一角色。  
- **建议：** 强制 `family_id` / `base_group_id`；禁止从成员列表推断。

---

### B-14 GSM-Plus test-only 锁仍可被默认 `assign_split` 绕过

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `splits.assign_split`；`t2_gsm_plus.load_gsm_plus`  
- **行号：** `splits.py` 12–20, 59–66；`t2_gsm_plus.py` 45, 49–51  
- **触发：** `assign_split("gsmplus-1")` 或不传 `source` / `test_only`  
- **协议：** DATA-03；FEATURES：GSM-Plus 数据卡禁止训练，必须固定为评测来源。  
- **证据：** X-18。作者 `test_b14` 只测加了锁的调用。`load_gsm_plus` 的 `metadata.role="test"` 不进入 `assign_split`。`t2_gsm_plus.py` digest 与 round-01 相同。  
- **影响：** 公开 test 变体可进入 `transfer_pairs` / `probe_train` / `calibration`。  
- **建议：** 默认识别 test-only 来源；划分阶段强制 `lock_test_only`。

---

### B-15 跨数据集族键不一致

- **状态：** confirmed defect（机制）/ pending_server（真实 dump 碰撞率）  
- **严重度：** high  
- **符号：** `t2_gsm_symbolic.family_id` vs `t2_gsm_plus.load_gsm_plus`  
- **行号：** `t2_gsm_symbolic.py` 11–12, 46；`t2_gsm_plus.py` 25  
- **协议：** DATA-03 / FEATURES：不同数据集的同源 GSM8K 题仍属同一题族。  
- **证据：** X-19。夹具同题：Symbolic `gsm8k-12`，Plus 整段 seed 题干。无规范化、无跨集映射。  
- **影响：** 同题可一边 train 一边 test。  

---

### B-16 T3 仍无「合法编辑 + 更新真值」

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `t3_hotpot.document_edit`；`t3_musique.load_musique_records`；`t3_humaneval`  
- **行号：** `t3_hotpot.py` 51–59（sidecar 参数仍不写节点）；`t3_musique.py` 27–42, 61；`t3_humaneval.py` 无 spec edit  
- **协议：** DATA-02：替换支撑文档后更新受影响答案；HumanEval-Perturb 改 Spec 并以新测试为裁判。  
- **证据：** X-20。`document_edit` 返回 dict，不产出新 `Task`、不改答案。MuSiQue 无文档替换。HumanEval 无旧/新 clause、新测试、区分输入。三文件 digest 与 round-01 相同（HumanEval 仅族键改动）。  
- **影响：** T3 无法做经核验的反事实；`ancestors(musique)` 仍把组成图当 R_task。  

---

### B-17 用题干前 N 个字符伪造前提列

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `load_gsm_plus` / `load_gsm_symbolic`（无 sidecar）/ `load_humaneval` / `load_t4`  
- **行号：** `t2_gsm_plus.py` 22；`t2_gsm_symbolic.py` 43；`t3_humaneval.py` 21；`t4_boundary.py` 26  
- **协议：** 未知图应 unknown，不得填假前提列冒充可评估 P。  
- **证据：** X-20 占位：Plus `"Ada has 4 ap"`；Symbolic `"Ada has "`；HumanEval spec 前 40 字符；T4 `"What is x "`。`graph_status` 多为 unknown（此项正确），但 `Task` 仍要求至少一条 premise。  
- **影响：** 若下游用 `premises` 当 P，ρ_S 分母是伪造的。  

---

### B-18 DATA-01 的改名与来源—数值变体仍未实现

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** 缺失  
- **行号：** 全包检索为空（X-25）  
- **协议：** DATA-01：数值/改名/no-op/来源—数值变体。MEAS-01：可导出与回填人工复核。  
- **证据：** 无 `rename` / `source_value` / `review_export`。T1 仍只有 `apply_value_edit`。  
- **影响：** C2 解耦资产无法从数据层生成。未实现前不能宣称 DATA-01 完成。  

---

### B-19 官方 iGSM 加载仍采信 dump 答案、不对照 template 重算

- **状态：** confirmed defect（缺校验）/ pending_server（真实 dump 是否已不一致）  
- **严重度：** medium  
- **符号：** `t1_official.load_igsm_snapshot`  
- **行号：** `t1_official.py` 62–63；`graphs.graph_status` 未被 loader 调用  
- **协议：** DATA-01：按拓扑重算并核对；不把 lookup 当新答案（lookup 已忽略，仍正确）。  
- **证据：** X-26。本机夹具重算恰为 9。`t1_official.py` digest 与 round-01 相同。  
- **建议：** 加载后 `recompute` 并与 dump 比对；失败则拒绝。  

---

### B-21 GSM-Plus 扰动类型映射不完整 / 空操作

- **状态：** confirmed defect  
- **严重度：** low  
- **符号：** `t2_gsm_plus.load_gsm_plus`  
- **行号：** `t2_gsm_plus.py` 15–21  
- **协议：** FEATURES：`reversing operation` 是改查询量；`critical thinking` ≠ 约束矛盾。  
- **证据：** `reversing operation` → `query_reversed`（不在 `T4_STATUSES`）。`if status in T4_STATUSES: pass` 为空。夹具 `numerical substitution` 的 `answer_spec.status is None`。  
- **影响：** 边界状态无法用于 T4 相图或过滤。  

---

### B-22 P2 分母只是调用方传入的整数

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `analysis.p2_paired`  
- **行号：** `analysis.py` 64–70  
- **协议：** P2 必须同时报告完整密度、共同已有前提变化、新增注入列。  
- **证据：** 函数原样返回 `shared_denominator=99`。`make_noop_pair` 不计算共同分母。  
- **影响：** 报告可以看起来「有分母」而没有共同支持集合。  

---

### B-23 有限扫描的单次已观察 no_change 仍写成已知域内阴性

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `measure.build_labels`；未使用的 `Edit.exhaustive`  
- **行号：** `measure.py` 43–53；`schema.py` 344  
- **触发：** 一条 `outcome=no_change` 且 `scan_state=observed_response`，无论允许扰动域是否穷尽  
- **协议：** 论文 L78 / PITFALLS#2：一次未变化 ≠ 已排除全部允许扰动；仅当有限域被完全有效扫描才能宣称域内阴性。  
- **证据：** X-05。`exhaustive` 全仓库除 schema 默认值外无读取。作者 `test_b02` 只覆盖 `no_response_observed_in_scan`。  
- **影响：** 单点扫描的「无依赖」会作为已知 0 进入探针 / ρ_M。  
- **建议：** 无 `exhaustive` 的 no_change 保持 unknown；不要把 `observed_response` 当成域穷尽。  

---

### B-24 `apply_value_edit` 的整数隔离会改到小数的小数部分

- **状态：** confirmed defect  
- **严重度：** high  
- **符号：** `edits._replace_isolated_value`  
- **行号：** `edits.py` 95–101（整数分支 `(?<!\d)…(?!\d)`，点不算数字）  
- **触发：** `premise.value="5"`，span 为 `p1 = 3.5`  
- **协议：** DATA-01：只改声明字面量整记号。  
- **证据：** X-13：题干变成 `p1 = 3.9`。作者 `test_b09` 只用 `14` 中的 `4`（左侧是数字，会被挡住）。  
- **影响：** 带小数的 T2 sidecar / 派生题会改错数并重算错误新答案。  
- **建议：** 整数与小数统一用 `(?<![\d.])…(?![\d.])`；失败则 invalid。  

---

### B-27 歧义解析行被静默丢弃，不是 `parse_failed` / `ambiguous`

- **状态：** confirmed defect  
- **严重度：** medium  
- **符号：** `events.parse_fixture_events`  
- **行号：** `events.py` 26–27, 42–43  
- **触发：** 同一行两个赋值（`q = 0 q = 1`）；或别名不唯一  
- **协议：** MEAS-01：歧义进入未对齐/parse_failed，不丢弃分母。  
- **证据：** X-24：事件列表为空。`Observation.__post_init__` 不校验 `scan_state`（非法值 `"not_a_real_state"` 被接受）。  
- **影响：** 分母缩小且无失败计数；扫描状态可被写脏。  

---

## 7. 已独立关闭的原触发（非本轮缺陷）

仅关闭 **已复现的原触发**。不把 ISSUES 整行标 closed。

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01 | X-03 矩阵缺噪声为 null | B-26 空 `noise_set` |
| B-02 原 scan_state | X-04 | B-23 |
| B-03 | X-06 | sham 仍钉在 premise_id；label 丢协议 |
| B-04 删除错位 | X-07 | 等计数 zip（X-08） |
| B-07 | X-10 | — |
| B-08 | X-11 | — |
| B-09 整数子串 | X-12 | B-24 |
| B-10 span | X-14 | 无祖先/答案不变证明 |
| B-11 unknown 空父母 | X-15 | `complete`+`[]` 仍当干净（X-16） |
| B-20 解析器撞车 | 身份现用 `node.id`（`events.py` 44–46） | 组成图仍被 `ancestors()` 消费（B-16） |

`build_labels` 已在 `cmd_prepare` / `cmd_label` 接线，且 prepare 用 `node_id` 对齐 `ancestors` 键。这关闭了 round-01「死代码 + identity.key 对不上 node.id」的那一半，**不**关闭 B-12/B-26 的分母错误。

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径 S/M 与缺 sham → null | `measure.py` 100–112 | X-27 对照：`excess is None`，`S={p2}`，`M={p1}`。负差不截断见既有测试。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | fixture 拒 official；官方拒仅有 G；lookup 不进重算。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–20 | 中间节点不进入列索引。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | `EventIdentity.key()` 为 JSON of entity/version/scope。 |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 225–233 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` 37–42 | `graph_status=unknown`。不否定 B-14/15/17。 |
| ND-07 | Hotpot 声明 supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 35–38 | 不否定 B-16。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | 不从标题推断。 |
| ND-09 | HumanEval 不在宿主 exec | `scoring.py` 19–29 | `executor_unavailable` 时 value/denominator null。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` 37–45 | `reasoning_diff_noop`，`official_noop_release=False`。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 105–111 | `b <= limit`。 |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` | `splits.py` 47–65 | 原语正确；不否定 B-13/B-14。 |
| ND-13 | T1 配置拒绝非白皮书格子 | `t1_config.py` 9–21 | |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 56–58 | |
| ND-15 | `parse_failed` 不记已知行为 | `build_labels` | X-24：`behavior_known=False`。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；API 仍有 B-23/B-26 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod`（5/2 mod 23 = 2，模逆 14） | FEATURES 称官方 Num 为加减乘；夹具无除法。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official`（X-27：`after=official`） | 可解释为题源而非「该行是官方发布」。需协议裁定。 |
| U-03 | `surface_mentions` 只匹配 `premise_id` 词，不抽符号/别名 | SURF-01 写「名称与符号引用」。T1 夹具 id 即名称；官方 iGSM 用 `a`/`b`。未在真实题干上抽样。 |
| U-04 | 后续 stage 是否用 `task_id` 而不是 `base_group_id` 做划分 | CLI fit 只信 `--split` 旗标。 |

## 11. 测试质量对本通道的含义

**65 passed ≠ 数据/测量正确。** 作者回归覆盖了若干 round-01 窄触发，但：

- `test_b06` 不测值后提及。  
- `test_b09` 不测 `3.5`/`5`。  
- `test_b13` 不测同 `family_id` 不同子集。  
- `test_b14` 不测裸 `assign_split(id)`。  
- `test_b02` 不测 `exhaustive` / 单次 `observed_response`。  
- 无多节点 `task_set`、无 `noise_set=[]`、无 HumanEval Spec 编辑、无跨集族键断言。  
- `test_full_cli_smoke` 只查 exit 0 与 `report.status==not_evaluated`。

因此不能把 ISSUES 中 B 行标为已关闭，除非对应残余也有独立反例测试。

## 12. 通道结论

数据与测量通道 **不能** 在本对象上给出通过意见。

1. **`HASH_MISMATCH`**：声明冻结 hash 无法复现；结论绑定上表逐文件 digest。  
2. **可独立关闭的原触发：** B-01、B-02（仅 `no_response_observed_in_scan`）、B-03、B-04（仅不等计数删除）、B-07、B-08、B-09（仅整数真子串）、B-10（仅 span 偷窃）、B-11（仅 unknown 空父母）。  
3. **作者标 fixed 但独立复开：** B-06、B-13（默认路径）、B-14。  
4. **本轮仍确认的结构性缺口：** B-05、B-12/B-26、B-15、B-16、B-17、B-18、B-19、B-21、B-22，以及新确认的 B-23、B-24、B-27。  

集合密度 raw/null/signed 路径与 T1 来源隔离仍成立（ND-01–ND-15），不能抵消划分泄漏、T3 真值更新缺失、以及 CLI 密度/有限扫描分母错误。真实官方全量保持 `pending_server`。即使服务器数据到达，B-14/B-23/B-26 仍会在本机逻辑层写错标签。
