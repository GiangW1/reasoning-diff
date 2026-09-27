# Review B — 数据与测量（独立审查，round-05）

本报告不假设实现正确，不把 `ISSUES.md` 的「Closed locally / fixed_pending_review」当作已关闭。未修改任何生产代码、测试、夹具或 `pyproject.toml`。未下载数据或权重。未阅读其他 round-05 通道报告。round-01/02/03/04 `B-data.md` 只用作待复验清单与行文格式，不作为证据。

**冻结核验：`HASH_MATCH`。** 按 `.planning/audits/round-05/VERSION.md` 文档化脚本（POSIX relpath + `\x00` + 文件字节，58 个范围内文件）独立复得 `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`。与声明值一致。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-05） |
| review_time | `2026-09-21T01:33:00+08:00`（复算 hash / 开读）— `2026-09-21T02:12:00+08:00`（成文） |
| declared_frozen_hash | `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（`.planning/audits/round-05/VERSION.md`） |
| independently_recomputed_hash | **`HASH_MATCH`** `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`。58 个范围内文件。配方与 VERSION 一致。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿单独信任 HEAD） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3；GOAL §5.1–5.5；`FEATURES.md` T1–T4 合同；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02、T2NOOP-01、STRUCT-01、SURF-01 |

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对测量/划分调用链而通读；`fixture` = 对照适配器读完。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 342 | `5102a7dd0a2d0e99a4941c50cf6705355c83c32fdebb507314a0323ffec57d5b` | full 1–342 | 标签、S/M、`noise_evaluated`、TO/CSP、有限扫描、`event_density_sets` |
| `src/reasoning_diff/events.py` | 196 | `2ac8624cc77bdf6f5e259c08568ce635921561df8372ac03ed1f0cedeea3ec3b` | full 1–196 | 身份（不含值）、等计数 `node_id`、`scanned=False`、`review_export` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `{}` |
| `src/reasoning_diff/edits.py` | 277 | `bfd1632b50504c042640bcda85368b0c695fd3f843ea885200d080055aa107b6` | full 1–277 | 小数隔离、重算、改名、`make_source_value_pair` |
| `src/reasoning_diff/splits.py` | 110 | `f8b08a69810e32448e6238230a8161e1068ade3b70f2714b81b3a140f15de5ef` | full 1–110 | `gsm_family_id`、`source` / `fit_eligible`、`lock_test_only` |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full 1–385 | 身份、`scan_state`、placeholder/spec、`Edit.exhaustive` |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 39 | `5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0` | full | 加载分派，不补图 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 79 | `e1a2b4098152857155877a787725fb3c70c2d872446eb14ee79619b2d5d60c81` | full | `gsm_family_id`、`gsm_plus:` 前缀、placeholder、`apply_plus_numeric_edit` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 84 | `b50db6533f18948d141a75a38970b491269a127b990bd818408f29a8e28219af` | full | sidecar、公式编辑、族键 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | span、注入后祖先、`noop_proof` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `baa832df548138753f383c324630f993b676cac0f1aa5c1df443557cbc18ced9` | full | 文档编辑、`needs_truth` vs `answer_spec.status` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值、组成图不进 `ancestors` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | `kind=placeholder`、Spec 仅在执行器 1.0 时 `valid` |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式、整题 placeholder、`needs_truth` |
| `src/reasoning_diff/cli.py` | 893 | `b1d801f16bc651e26c44a13f5c9c3fac837647c0de359033cc453d3fdfb06ab7` | callsite 92–370, 480–504, 711–759 | prepare/label 测量 API；sham `premise_id=""`；P2 透传 |
| `src/reasoning_diff/analysis.py` | 283 | `3593254605792c6e13fe45ec658c67f1f55af35c224df84f77dd5ce1c2e14730` | callsite 105–160 | P2 整数分母 → `denominator_unverified` |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | callsite | 域内评分分母；代码不宿主 exec |
| `tests/test_review_regressions.py` | 394 | `37414926677d059610794b4f64ec3bcbf7c242ecce9c563bc8e549abc5d3a60c` | full | 与 r04 同 digest；未锁本轮新反例 |
| `tests/test_round03_regressions.py` | 291 | `5698a410c0669b6142f31d5b302ff8c7ef8ec66cc9ef429786d45e2418bfc278` | full | r03 作者 oracle；独立另造反例 |
| `tests/test_round04_regressions.py` | 310 | `93f04cc13c39d6b0a906194ef6ef784642c9f0b7613b7807deb8f7947e08ed56` | full | 作者对 B-12/B-15/B-22/来源对的弱锁 |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c` | full | 不测 Hotpot `new_answer` 的 status |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 r04 相同，未改字节）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`（含 `original_id` + `seed_question`）；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

相对 r04 生产 digest 已变：`measure.py` / `events.py` / `edits.py` / `splits.py` / `schema.py` / `t2_gsm_plus.py` / `t2_gsm_symbolic.py` / `t2_noop.py` / `t3_hotpot.py` / `t3_musique.py` / `t3_humaneval.py` / `t4_boundary.py` / `cli.py` / `analysis.py` / `scoring.py`。`graphs.py` / `t1_config.py` / `t1_fixture.py` / `t1_official.py` / `catalog.py` / `__init__.py` 未变。`test_review_regressions.py` 与 r04 同 digest。

## 3. 已执行检查

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-01 | 本通道 + r04 回归 pytest | `python -m pytest tests/test_review_regressions.py tests/test_measure.py tests/test_t1_official.py tests/test_t2_gsm.py tests/test_t3_t4.py tests/test_round03_regressions.py tests/test_tracer_t1_prepare.py tests/test_round04_regressions.py -q --tb=line` | **100 passed**，exit 0。绿测试不能关闭下列独立反例。 |
| X-02 | 全量本机 pytest | `python -m pytest tests -q --tb=line` | **120 passed**，exit 0，约 13.3s。无 skip/xfail。与 VERSION `pytest_author_claim` 计数一致，仍不是科学正确性证据。 |
| X-03 | 矩阵 `noise=None`（B-01） | `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `S.noise=None`，`S.excess=None`，`rho_S_noise=None`，`null_reason=noise_missing`。保持关闭。 |
| X-04 | 有限扫描 `no_response_observed_in_scan`（B-02） | 仅 `outcome=no_change` + 该 scan_state | `behavior_label=None`，`behavior_known=False`。保持关闭。 |
| X-05 | `observed_response` + `no_change` ± `exhaustive`（B-23） | 同上两旗标 | 无 `exhaustive` → unknown；`exhaustive=True` → `behavior_label=0`。API 保持关闭。 |
| X-06 | sham 不进入 R_behavior（B-03） | 编辑 exhaustive no_change + `sham:0` changed | 行为袋 `(q,p2)=0`；`(q,"")` 行为 unknown；`noise_ref=1.0` 广播到两行。 |
| X-07 | 删除后对齐（B-04） | `"q = 1\\nq = 2\\n"` vs `"q = 2\\n"` | `pairs=[]`；`merged` 非空；`scanned=False`；`strategy_detector=status_field_only`。 |
| X-08 | 等计数同 `node_id` | `"q = 1\\nq = 2\\n"` vs `"q = 9\\nq = 2\\n"` | 配成 `(1,9),(2,2)`，双方 `node_id=q`。身份键不含 value。 |
| X-08b | 等计数不同 `node_id` | entity `q` 左 `node_id=q`、右 `node_id=r` | `pairs=[]`，记 ambiguous。 |
| X-09 | R_surf vs 图父母（B-06/B-25） | 裸赋值 / 值后提及 / 赋值前 | 父母 `['p1','p2']`；裸 surface `[]`；值后与赋值前均为 `['p1']`。保持关闭。 |
| X-10 | HumanEval 族 / kind（B-07/B-17） | `load_humaneval` | `base_group_id=HumanEval/0`。前提 `kind=placeholder`，全文 42 字符。`assign_split("HumanEval")` 仍为 `probe_train`（加载器不用该截断键）。 |
| X-11 | 公式编辑（B-08） | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，premise/node/answer 均为 5/8/8。保持关闭。 |
| X-12 | 数值子串（B-09） | `"has 13 apples"`、值 `"3"` | `ValueError: not a unique isolated token`。**T1 路径保持关闭。** Plus 域编辑见 X-plus-sub。 |
| X-13 | 小数 3.5/5 与 5.5/5.0（B-24） | `_replace_isolated_value` | `3.5`/`5.5`/`5.0`/`+5.5`/`15.5` 均抛错。孤立 `p1 = 5` → `p1 = 9`。 |
| X-14 | no-op 证明（B-10） | 前端注入；有图 / 无图 | 见下段。**原空证明触发关闭。** |
| X-15 | CSP 空父母 + unknown（B-11） | `task_parents=[]`，`graph_status=unknown` | `csp=None`，`clean_matched=0`。保持关闭。 |
| X-16 | CSP 空父母 + complete | 同上但 `complete` | `csp=1.0`，`clean_matched=1`，`coverage=1.0`。 |
| X-17 | `assign_family`（B-13） | 缺 id；同 id 不同子集 | 缺 id 抛错。`{A,B,C}` / `{B,C}` / `{Z}` 同 `family_id` 均为 `probe_train`。保持关闭。 |
| X-18 | GSM-Plus 生产划分（B-14） | 夹具 / 官方字段子集 / `refuse_fit_split` | **生产路径保持关闭。** 见细项。 |
| X-19 | 跨集族键（B-15） | 同题 Symbolic vs Plus | 见细项。**机制仍 confirmed。** |
| X-20 | T3 编辑 / 组成图（B-16/B-20） | `document_edit` / `paragraph_edit` / `apply_spec_edit` / `ancestors` | Edit 层不再因口述答案变 `valid`。Hotpot **任务** status 仍污染。见 B5-03。`ancestors(musique/hotpot/plus/he)=={}`。 |
| X-21 | CLI prepare + sham（B-12） | `main(["prepare", …, "--sham-opportunities","1"])` | 真编辑 `p2`/`changed`；sham `premise_id=""`、`no_change`、`scan_state=observed_response`、`exhaustive=False`。标签 `(q,p2)` `noise_ref=0.0`，另有 `(q,"")`。密度 `aggregation=mean_over_events`；t1_tiny 的 S 分母为空，故 `rho_S_noise=None`（空分母，不是 B-12 回归）。写 `review_export.jsonl`（3 行）。exit 0。 |
| X-21b | CLI 已观察 no_change | `--edit-premise p1 --edit-value 7`（q 仍 0） | `outcome=no_change`，`scan_state=observed_response`，`exhaustive=False`。 |
| X-21p | Plus 八类扰动（B-21） | 独立喂官方类名 | `critical thinking` / `missing information` → `insufficient_information`。`reversing operation` → `answer_spec.status=None`，`metadata.perturbation_status=query_target_change`。其余六类 `(None, None)`。 |
| X-22 | P2 分母（B-22） | `p2_paired(..., 99)` ± `shared_premises` | **只传 99 → `status=denominator_unverified`，`delta_rho=None`。** 99 vs `["p1"]` → `denominator_inconsistent`。一致时用集合长度，`ok`。原触发关闭。 |
| X-22n | 多节点祖先 | 内存 s=p1+p2、t=s+p1 | `anc[t]={p1,p2}`。`ancestors` 对 `composition_reference` / `supporting_facts_only` 返回 `{}`。 |
| X-23 | 空 `noise_set` ± `noise_evaluated`（B-26 / B-12） | 集合密度 API | 未评估空集 → `noise_set_empty`、excess null。**已评估空集 → `rho_S_noise=0.0`，excess = raw − 0。** 原「空集当缺失」与「0-hit 当空」已区分。 |
| X-12e | `event_density_sets` 0-hit / 缺失 / sham 命中 | 给 t1 加非祖先 `p3` | 0-hit：`noise=0`，`excess=raw`。缺失：`noise_set_empty`。**sham 命中且行为在 p3：`rho_S_noise=1.0`，`excess=0.0`（B5-04）。** |
| X-24 | 多匹配行 / 非法 scan_state（B-27） | `"q = 0 q = 1\\n"`；非法枚举 | 两条 `status=ambiguous`。非法 scan_state 抛 `ValueError`。保持关闭。 |
| X-25 | 改名 / 来源—数值 / 复核（B-18） | `apply_rename_edit` / `make_source_value_pair` / `review_export` | 题干改为 `alpha` / `p1_src`，**表达式仍 `p1 * p2`**。值条件重算答案。`review` 字段恒 `None`。无回填入口。`apply_value_edit.exhaustive` 恒 False。 |
| X-26 | 官方夹具重算（B-19） | 夹具 9；篡改答案 8 | 9=9。不一致拒绝。fixture 加载器拒 official 形状。保持关闭。 |
| X-27 | 除法模运算 | `_eval_expr("5 / 2", {}, 23)` | `2`（`int(truediv)%mod`），不是模逆 14。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-plus-sub | Plus 合法数值编辑 | 官方字段题干 `Ada has 13 apples…`，`apply_plus_numeric_edit(..., "3", "9")` | **题干变成 `Ada has 19 apples and buys 3 more…`。** `validity=needs_truth`。夹具机制 bug。 |
| X-he-rho | HumanEval 进 ρ（B-17） | `kind=placeholder` + `event_density_sets` | `denominator_S=None`，`rho_S_raw=None`（不是假 0）。原 N 字符 / spec 列触发关闭。 |
| X-he-exec | Spec 裁判（B-16 HE） | 无解 / PassExec / FailExec / 默认不可用 | 无解与不可用、失败均为 `needs_truth`。仅 `tests_passed=True` → `valid`。 |
| X-label | CLI label | `main(["label", "--in-dir", prepare_out])` | exit 0，写出标签 + densities。 |
| X-msq | MuSiQue 配对 id | 夹具两条 | `msq-9::answerable` / `msq-9::unanswerable`，同 `base_group_id`。 |
| X-t4 | T4 四态 | `load_t4` | 四态齐全；前提均为 placeholder。 |
| X-t1cfg | T1 格子 | `validate_t1_prepare_config` | 四档 op + n=500 + mod=23；op=7 拒绝。 |

**X-14 细项（独立，不信任作者回归）：**

- 缺 `independent_non_ancestor` → 拒绝。
- T1 有图：注入后 `ancestors(q)={p1,p2}`，不含 `noop`；`recompute` 答案仍 0；`noop_proof=recompute_and_ancestors`，`answer_unchanged_proven=True`，`injected_non_ancestor=True`。span 切到 `"p1 = 4 is a red herring."`；原 `p1` 切片仍 `"p1 = 4"`。`source=reasoning_diff_noop`，`official_noop_release=False`。
- Plus 无图：`noop_proof=unknown_without_graph`，`answer_unchanged_proven=False`，`injected_non_ancestor=None`。不再把无图写成已证明。

**X-18 细项（独立，不信任 `test_b14`）：**

- 夹具（有 `original_id=gsm8k-12`）：`base_group_id=gsm_plus:gsm8k-12`，`shared_gsm_family=gsm8k-12`，`fit_eligible=False`，`metadata.role=test`，`kind=placeholder`。`split_for_task` / 裸 `assign_split(base_group_id)` 均为 `test`。`refuse_fit_split(..., "probe_train")` 拒绝。
- 仅官方字段（无 `original_id`/`id`）：`shared_gsm_family=unmapped:ada has 4 apples and buys 3 more. how many apples?`，`base_group_id=gsm_plus:` + 该串，划分仍 `test`。
- `gsm_family_id` 优先含 `gsm8k` 的 `original_id`/`id_orig`/`seed_id`/`gsm8k_id`；否则 `unmapped:` + 规范化 `seed_question`。**没有 seed 文本 → GSM8K ID 的匹配。**
- 裸 `assign_split("gsm8k-1")=="probe_train"`；`assign_family(..., family_id="gsm8k-1")` 角色 `probe_train`。这不是 Plus 生产键，但是 Symbolic 生产键。

**X-19 细项：**

- 同题夹具：Symbolic `base_group_id=shared_gsm_family=gsm8k-12`；Plus `shared_gsm_family=gsm8k-12` 但 `base_group_id=gsm_plus:gsm8k-12`。`equal_base=False`，`equal_shared_fixture=True`。
- 官方 Plus schema（无 `original_id`）：`shared_gsm_family` 与 Symbolic **不相等**。
- 本夹具 `gsm8k-12` 的哈希角色碰巧两边都是 `test`。换成 `gsm8k-1`：Symbolic → `probe_train`，Plus（即使带同一 original_id）仍因 `source=gsm_plus` 锁 `test`。
- `shared_gsm_family` **只写入 metadata，生产路径没有任何共组 / `assert_same_role` 消费方。** `split_for_task` 用 `base_group_id`，不是共享族键。

**X-12e / sham 命中（独立）：**

- 给 t1 增加非祖先 `p3`。行为 `p3∈B`，任务祖先 `{p1,p2}`，`ρ_S raw=1`。
- 0-hit（`noise_ref=0.0`）：`rho_S_noise=0.0`，`rho_S_excess=1.0`。原 B-12 触发关闭。
- 未观察：`noise_set_empty`，excess null。与 0-hit 已分开。
- **sham 命中**（`noise_ref=1.0` 广播到 `(q,p3)`）：`hits` 只收集 `noise_ref==1.0` 且非空 `premise_id`，于是 `N={p3}`，`ρ_S_noise=1.0`，**`excess=0.0`**。无编辑随机变化被安到真实前提列，虚假依赖被噪声项吃掉。

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 B5-01 已在夹具与官方字段子集确认 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b`。见 U-01 |
| N-07 | scientific prepare 的 sham seed=2 在真实权重上的命中率 | 本机 tiny 解码不是科学噪声协议；B5-04 已在密度 API 上确认 |

官方全量保持 `pending_server`。夹具上可复现的机制错误记为 confirmed defect，不降级为 pending_server。

## 5. 既有 B-## 独立结论（closed / residual / reopened）

不得因回归绿或 `ISSUES.md` 成文而关闭。下表针对 **round-01/02/03/04 原 ID**。作者本轮主张关闭 B-15 / B-10 / B-17 / B-22 / B-12 / B-16 等，下列为独立 oracle。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | 未本轮重开 | **closed** | X-03 |
| B-02 | — | **closed** | X-04 |
| B-03 | — | **closed** | X-06；CLI  sham `premise_id=""`（X-21） |
| B-04 删除 / 异 node_id | — | **closed** | X-07 / X-08b |
| B-05 `scanned=True` | — | **closed** | X-07 |
| B-06 / B-25 | — | **closed** | X-09 |
| B-07 | — | **closed** | X-10 |
| B-08 | — | **closed** | X-11 |
| B-09 | — | **closed** | X-12（T1 `_replace_isolated_value`）。Plus 域编辑是新洞，见 B5-02。 |
| B-10 祖先/答案证明 | closed locally | **closed** | X-14：无图写 `unknown_without_graph`；有图做注入后祖先 + 重算。 |
| B-11 | — | **closed** | X-15 |
| B-12 0-hit sham → 空噪声集 | closed locally | **closed**（原触发） / **residual**（命中身份） | X-23 / X-12e 0-hit：`noise_evaluated` 后 excess = raw − 0。sham **命中** 仍把真实前提写入 `N`，见 B5-04。 |
| B-13 | — | **closed** | X-17 |
| B-14 生产族键 + `fit_eligible` | — | **closed** | X-18 |
| B-15 跨集族键 | closed locally（`gsm_family_id` / `shared_gsm_family`） | **residual（仍 confirmed）** | X-19。见 §6 B5-01。作者测试只锁「夹具带 original_id 时 metadata 相等」。 |
| B-16 T3 口述 valid | closed locally（QA/Plus/T4 保持 `needs_truth`；HE 仅执行器 1.0） | **closed**（Edit.validity 原触发） / **residual**（Hotpot 任务 status） | X-20：Edit 不再因 `new_answer` 变 valid。Hotpot 仍把口述答案写成 `status=None`。见 B5-03。 |
| B-17 HumanEval spec 进 ρ | closed locally（`kind=placeholder`） | **closed** | X-10 / X-he-rho：P 列被过滤，密度 raw/denom 为 null。 |
| B-18 改名/解耦/复核 | closed locally（`make_source_value_pair` / `review_export`） | **residual（仍 confirmed）** | X-25。见 B5-05。 |
| B-19 | — | **closed** | X-26 / X-26b / X-26c |
| B-20 | — | **closed** | X-20 / X-22n：`ancestors=={}` |
| B-21 | — | **closed** | X-21p |
| B-22 P2 整数分母 | closed locally | **closed** | X-22：`denominator_unverified`，`delta_rho=None` |
| B-23 | — | **closed** | X-05 / X-21b |
| B-24 | — | **closed** | X-13 |
| B-26 空集当 0 | — | **closed** | X-23 未评估空集仍 null |
| B-27 | — | **closed** | X-24 |

## 6. 发现（本轮开放，B5-##）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B5-01 跨数据集 GSM 族键在官方 Plus schema 上仍不一致（原 B-15）

- **状态：** confirmed defect（机制）/ pending_server（真实 dump 碰撞率）
- **严重度：** high
- **符号：** `splits.gsm_family_id`；`t2_gsm_plus.load_gsm_plus`；`t2_gsm_symbolic.family_id`；`splits.split_for_task`
- **行号：** `splits.py` 12–22, 71–79；`t2_gsm_plus.py` 20–24, 42；`t2_gsm_symbolic.py` 12–13, 47, 63
- **协议：** DATA-03 / FEATURES T2：以规范化 `seed_question` **连接 GSM8K ID**；不同数据集同源题同族。GOAL §5.5：同基础题、同源题、全部变体共组；Plus 测试专用不得参与拟合，但不能把同源 Symbolic 放进 `probe_train` 再拿 Plus 当未见题。
- **证据：**
  1. X-19：同题夹具 Symbolic `base_group_id=gsm8k-12`，Plus `gsm_plus:gsm8k-12`。`shared_gsm_family` 仅在夹具带 `original_id` 时相等。
  2. 官方 Plus 字段只有 `question/solution/answer/perturbation_type/seed_*`，没有 `original_id`。此时 `gsm_family_id` 写成 `unmapped:<seed_question>`，与 Symbolic 的 `gsm8k-*` **不相等**。无 seed→GSM8K 匹配。
  3. `shared_gsm_family` 无消费方。划分走 `base_group_id` + `source`。Plus 锁 test；Symbolic `gsm8k-1` 为 `probe_train`（X-18）。同源题可一边拟合、一边当测试。
  4. 作者 `test_plus_and_symbolic_share_gsm8k_family` 只断言夹具 metadata 相等，并允许 Plus `base_group_id` 带前缀。不测官方字段、不测共组划分。
- **影响：** 即使服务器 dump 到达，官方 Plus 仍无法与 Symbolic 共族；有 `original_id` 的派生快照也会因 `base_group_id` 不同而拆分。Plus 自身 test-only 锁（B-14，已关）不能代替共组。
- **建议：** 规范化 seed 文本匹配 GSM8K ID；失败则 `unmapped` + 文本哈希并显式状态。划分与 `assert_same_role` 必须消费同一族键，禁止静默各算各的。

---

### B5-02 GSM-Plus 域数值编辑用子串替换，破坏孤立 token 不变量

- **状态：** confirmed defect
- **严重度：** high
- **符号：** `t2_gsm_plus.apply_plus_numeric_edit`
- **行号：** `t2_gsm_plus.py` 50–74；对照 `edits.py` 93–106
- **协议：** DATA-02 / FEATURES：数值编辑检查孤立数字；只改题干数字而沿用错位替换属于错误适配。GOAL §5.2：合法编辑。B-09 已要求 T1 拒绝 `"13"` 中的 `"3"`。
- **证据：**
  1. 实现是 `task.question.replace(old, new, 1)`，不走 `_replace_isolated_value`。
  2. X-plus-sub：官方字段题干 `Ada has 13 apples and buys 3 more. How many apples?`，`old="3"` → **`Ada has 19 apples and buys 3 more…`**（`13` 被改成 `19`，后面的孤立 `3` 未动）。
  3. T1 同输入仍正确拒绝（X-12）。这是 Plus 域编辑器的新洞，不是 B-09 回归。
- **影响：** 夹具即可写出「合法数值编辑」而改错了另一个数。官方 Plus 含位数扩展与多位数，此路径会在真实 dump 上复现。
- **建议：** 与 T1 共用孤立 token 替换；不唯一则 fail-closed。

---

### B5-03 Hotpot 口述新答案写进任务真值且 `status=None`（原 B-16 残余）

- **状态：** confirmed defect
- **严重度：** medium（Edit.validity 已诚实；Task 金标被污染）
- **符号：** `t3_hotpot.document_edit`；对照 `t3_musique.paragraph_edit` / `t3_humaneval.apply_spec_edit`
- **行号：** `t3_hotpot.py` 74–104
- **协议：** DATA-02 / FEATURES：替换支撑文档后更新**经核验**的答案；不能把调用方口述当已确认金标。GOAL §5.1–5.2：T2/T3 不得用答案或模型轨迹冒充真值。
- **证据：**
  1. X-20：无 `new_answer` 时 `Edit.validity=needs_truth`，`answer_spec.status=requires_independent_truth`，`value=None`。这是正确的 fail-closed。
  2. 传入 `new_answer="Spain"`：`Edit.validity` 仍为 `needs_truth`（原「口述即 valid」已关），但 **`task.answer_spec.status=None`（看起来像普通金标）**，`value="Spain"`，`answer_updated=True`。
  3. MuSiQue 清空分解节点值并保持 `requires_independent_truth`，但仍把口述 `London` 写入 `answer_spec.value`。
  4. HumanEval：无执行器 / 失败 / 无新解 → `needs_truth`；仅 `tests_passed=True` → `valid`（X-he-exec）。Plus/T4 编辑恒 `needs_truth`。
  5. 作者 `test_spec_and_paragraph_need_truth` / `test_hotpot_support_is_not_full_dag` 不传入 `new_answer`，锁不住本条。
- **影响：** 下游若读 `task.answer_spec` 而不读 `Edit.validity`，会把未核验的 Hotpot 反事实当成金标评分。机制 bug，不是 pending_server。
- **建议：** 有口述答案时任务 status 必须保持 `requires_independent_truth`，直到独立核验回填；核验 API 尚未存在则不要写 `status=None`。

---

### B5-04 已观察 sham **命中** 把真实前提列写入噪声集（原 B-12 残余）

- **状态：** confirmed defect
- **严重度：** high
- **符号：** `measure.build_labels`；`measure.event_density_sets`；`dependency_densities(..., noise_evaluated=)`
- **行号：** `measure.py` 68–78, 124–142, 281–310；`cli.py` 284–345
- **协议：** MEAS-02 / 协议 §2.6 / GOAL §5.4：噪声参照必须对应明确且匹配的比较机会；**不能给无编辑随机变化强加具体前提身份**。已扫描 0-hit 是参照 0，不是 missing。
- **证据：**
  1. 0-hit 原触发已关：X-23 / X-12e 在 `noise_evaluated=True` 且 `noise_set=[]` 时 `ρ_S_noise=0`，excess = raw − 0。CLI fixture sham 同文，写成 `noise_ref=0.0`（X-21）。
  2. `build_labels` 按 **事件** 广播 `noise_ref`：sham 一变，该事件所有前提行（含真实编辑列）都变成 `1.0`。
  3. `event_density_sets` 的 `hits` 收集 `noise_ref==1.0` 且 **非空** `premise_id`。sham 观察的 `premise_id=""` 被丢掉，于是 `N` = 该事件已有的真实前提。
  4. 独立构造：`P={p1,p2,p3}`，`T={p1,p2}`，`B={p3}`，sham 命中 → `ρ_S_raw=1`，`ρ_S_noise=1`，**`ρ_S_excess=0`**。同一行为在 0-hit 下 excess=1。无编辑波动被安到虚假依赖列，C3 信号被抹平。
- **影响：** 协议要的「0-hit = 0」已实现；「命中但不能指认前提」未实现。scientific prepare 用 seed=2 生成 sham，命中时走同一 API。t1_tiny 的 S 分母为空，CLI 冒烟看不到本条。
- **建议：** 噪声保持事件级 0/1 或单独噪声袋，禁止把 sham 广播成真实 `premise_id∈N`。空 list + `noise_evaluated=True` 只表示已观察 0。

---

### B5-05 来源—数值对仍是表面改名，不是论文的 A/B 解耦资产（原 B-18 残余）

- **状态：** confirmed defect
- **严重度：** medium
- **符号：** `edits.make_source_value_pair` / `apply_source_value_edit`；`events.review_export`
- **行号：** `edits.py` 151–234；`events.py` 155–170；`cli.py` 307, 362
- **协议：** DATA-01 / FEATURES 来源—数值：同图族来源 A/B，先 `a=b` 再 `a≠b`；MEAS-01：可导出**与回填**人工复核。论文 §2.3 / C2：等值异源与同值条件分开。
- **证据：**
  1. X-25：`same_source_diff_value` 是普通值编辑；`same_value_diff_source` 是 `p1→p1_src` **表面改名**。表达式仍 `p1 * p2`，图上没有第二个来源节点，也没有 `q` 从 A 改读 B。
  2. `apply_source_value_edit` 只返回值编辑，靠 metadata 声称存在 companion。作者测试只断言旗标为 True。
  3. CLI prepare 写 `review_export.jsonl`，`review` 恒 `None`。全包无回填 / merge 入口。
  4. 改名后表达式保持 `premise_id` 是作者 `test_rename_keeps_expression` 显式锁定，**不单独升格**；升格的是「有一对函数 ≠ 有解耦资产」。
- **影响：** C2 所需的同值异源图对无法从数据层按协议生成。函数存在不等于 DATA-01 完成。

## 7. 已独立关闭的原触发（非本轮缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01 | X-03 | — |
| B-02 | X-04 | — |
| B-03 | X-06 / X-21 sham `premise_id=""` | 空前提标签行；B5-04 |
| B-04 删除 / 异 node_id | X-07 / X-08b | — |
| B-05 假扫描 | X-07 `scanned=False` | 无策略分类（ND-17） |
| B-06 / B-25 | X-09 | U-03 |
| B-07 | X-10 | — |
| B-08 | X-11 | — |
| B-09 / B-24 | X-12 / X-13 | **B5-02 Plus 子串** |
| B-10 | X-14 有图证明 / 无图 unknown | — |
| B-11 | X-15 | X-16 `complete`+`[]` |
| B-12 0-hit → 空集当缺失 | X-23 / X-12e 0-hit | **B5-04 sham 命中身份** |
| B-13 | X-17 | — |
| B-14 | X-18 生产键 / `fit_eligible` / refuse | B5-01 |
| B-16 Edit 口述 valid | X-20 Edit.validity；HE 执行器门槛 | **B5-03 Hotpot status** |
| B-17 N 字符 / spec 列 | X-he-rho placeholder 过滤 | — |
| B-19 | X-26b | pending_server 真实 dump |
| B-20 | X-20g `ancestors=={}` | B5-03 分解值清空后仍无核验更新 |
| B-21 错映射 | X-21p | 六类无状态（可接受） |
| B-22 整数分母 `ok` | X-22 `denominator_unverified` | — |
| B-23 | X-05 / X-21b | CLI 永不置 `exhaustive=True`（保守） |
| B-26 空集当 0 | X-23 未评估仍 null | B5-04 |
| B-27 | X-24 | — |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径 S/M 与缺 sham → null | `measure.py` 124–135 | 缺协议或 `noise_set is None` 时 excess null；负差不截断。不否定 B5-04。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | fixture 拒 official；官方拒仅有 G；lookup 不进重算。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | 中间节点不进入列索引；非算术 `graph_kind` 返回 `{}`。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | `EventIdentity.key()` 为 entity/version/scope。X-08 同节点 zip 符合「值不决定对应」。 |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 325–333 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` 36–37 | `graph_status=unknown`，`graph_kind=none`。不否定 B5-01。 |
| ND-07 | Hotpot 声明 supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 34–38 | 文档级多句替换且 `single_premise_claim=False`。不否定 B5-03。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | 不从标题推断。 |
| ND-09 | HumanEval 不在宿主 exec | `scoring.py` 19–29 | `executor_unavailable` 时 value/denominator null。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` 41–50, 96–99 | `reasoning_diff_noop`，`official_noop_release=False`；无图不写 proven。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 173–179 | `b <= limit`。 |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` | `splits.py` 82–100 | 原语正确；不否定 B5-01（无人调用跨集族键）。 |
| ND-13 | T1 配置拒绝非白皮书格子 | `t1_config.py` 9–21 | |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 59–60 | |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05/X-21b。 |
| ND-16 | 官方加载对照 template 重算 | `t1_official.py` 77–80 | X-26。不把「有校验」写成「全量官方数据已验收」。 |
| ND-17 | 策略分岔 `scanned=False` | `events.py` 119–127 | 空 `strategy_changed` 现表示未扫描。STRUCT-01 分类器仍未实现，但不构成静默假阴性。 |
| ND-18 | Plus/T4/HE placeholder 过滤 | `measure.py` 285；`cli.py` 93, 157, 207 | 原 B-17 假前提列不再进编辑或 P 分母。 |
| ND-19 | 已观察 0-hit 记噪声 0 | `measure.py` 130–141 | 与未评估空集分开。关闭 B-12 原触发，不关闭 B5-04。 |
| ND-20 | HE Spec `valid` 仅执行器 1.0 | `t3_humaneval.py` 44–67 | 默认 UnavailableExecutor 不能冒充通过。 |
| ND-21 | Plus/T4/MuSiQue Edit 恒 `needs_truth` | 各 apply* | 缺独立核验时不写 valid。不否定 B5-03 的 Task.status。 |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 115–125 | 关闭 B-22。 |
| ND-23 | MuSiQue answerable 配对保留 | `t3_musique.py` 43–68 | 同 `base_group_id`，不同 `task_id`。 |
| ND-24 | CLI fixture sham 不钉编辑前提 | `cli.py` 318–336 | 原 B-03/B-12 钉 `p2` 已关。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；0-hit API 已关，命中身份仍有 B5-04 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 | 机制层 B5-01 已确认；dump 上匹配率 pending |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod`（5/2 mod 23 = 2，模逆 14） | FEATURES 称官方 Num 为加减乘；夹具无除法。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official` | 可解释为题源而非「该行是官方发布」。需协议裁定。 |
| U-03 | `surface_mentions` 只匹配 `premise_id` / alias 词 | SURF-01 写「名称与符号引用」。官方 iGSM 夹具 id 即 `a`/`b`。未在真实题干别名上抽样。 |
| U-04 | 后续 stage 是否用 `task_id` 而不是 `base_group_id` 做划分 | CLI fit 只信 `--split` 旗标。prepare 写 `splits.jsonl` 但不被 fit 读取。 |
| U-05 | 前提 span 同时含孤立整数 `5` 与小数 `5.5` 时整数编辑被拒 | 当前 fail-closed。未见生产 span 同时含两者。 |
| U-06 | `assign_family` 不传 `fit_eligible` | Plus 生产走 `split_for_task` / `lock_test_only`。缺 source 的 `gsm8k-*` 是 Symbolic 路径。 |
| U-07 | `distinguishing_tests=True` 仅因 `new_tests` 非空 | 与 `validity=needs_truth` 并存。未见评分消费该旗标当已区分。 |
| U-08 | scientific sham seed=2 在 tiny 上是否改变 | 作者测试允许文本或 token 不同。本通道用 fixture 同文 sham；B5-04 不依赖 tiny 是否命中。 |

## 11. 测试质量对本通道的含义

**120 passed ≠ 数据/测量正确。** 作者本轮补了 0-hit `noise_evaluated`、P2 `denominator_unverified`、夹具级 `shared_gsm_family`、来源对旗标、HE placeholder。独立复现同意这些**原触发**中 B-10 / B-12-0-hit / B-14 / B-16-Edit / B-17 / B-22 可关。缺口仍在：

- `test_plus_and_symbolic_share_gsm8k_family` 只用带 `original_id` 的夹具，不测官方 Plus 字段，不测 `split_for_task` 共组，不测 `gsm8k-1` vs Plus test。
- `test_evaluated_zero_hit_sham_is_zero_noise_not_null` 直接喂 `dependency_densities(..., noise_evaluated=True)`；不测 `event_density_sets` 在 sham **命中** 时把 `p3` 写入 `N`。
- `test_source_value_pair_has_both_conditions` 只查 metadata 旗标，不查是否存在第二来源节点。
- `test_spec_and_paragraph_need_truth` / Hotpot 测试不传 `new_answer`，不锁 `status=None`。
- 无 Plus `replace("3")` 对 `13` 的断言。
- 无 no-op 无图 `unknown_without_graph` 以外的跨集族键断言。
- `test_review_regressions.py` 与 r04 **同 digest**，未覆盖本轮新反例。

因此不能把 ISSUES 中 B-15 / B-16 整行 / B-12 整行 / B-18 标为已关闭。B-10、B-17、B-22、B-12 的 **0-hit 原触发**、B-16 的 **Edit.validity 原触发** 可独立关闭。

## 12. 通道结论

数据与测量通道 **不能** 在本冻结对象上给出通过意见。**FAIL。**

1. **`HASH_MATCH`：** 声明冻结 hash 已按 VERSION 配方复现（58 文件）；结论绑定上表逐文件 digest。
2. **本轮可独立关闭的作者主张：** **B-10**（无图 unknown / 有图注入后祖先+重算）、**B-12 原触发**（已观察 0-hit → 噪声 0 而非 missing）、**B-16 Edit.validity**（口述答案不再把 Edit 标 valid；HE 仅执行器 1.0）、**B-17**（HumanEval `kind=placeholder`，ρ 分母 null）、**B-22**（整数分母 `denominator_unverified`）。先前已关且仍关：B-01/02/03/04/05/06/07/08/09/11/13/14/19/20/21/23/24/26/27。
3. **仍确认的机制缺陷（夹具或官方字段子集可复现）：**
   - **B5-01 / B-15** 跨集族键：官方 Plus 无匹配；`shared_gsm_family` 无消费方；同源 Symbolic 可进 `probe_train`。
   - **B5-02** Plus `str.replace` 把 `13` 改成 `19`。
   - **B5-03 / B-16 残余** Hotpot `new_answer` 写入 `answer_spec.status=None`。
   - **B5-04 / B-12 残余** sham 命中把真实前提写入噪声集，可把 `ρ_S_excess` 抹成 0。
   - **B5-05 / B-18 残余** 来源—数值对是改名+值编辑，不是 A/B 解耦图；复核无回填。
4. 集合密度 raw/null/signed、T1 来源隔离、官方 dump 对照重算、有限扫描 unknown、身份不含值、HE placeholder 过滤仍成立（ND-01–ND-24），不能抵消划分共组、Plus 合法编辑与噪声身份缺口。官方全量保持 `pending_server`。即使服务器数据到达，**B5-01 仍会把官方 Plus 与 Symbolic 拆成两族**，B5-02 仍会改错多位数字，B5-04 仍会在 sham 命中时吃掉虚假依赖。
