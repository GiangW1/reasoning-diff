# Review B — 数据与测量（独立审查，round-09）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-09 通道报告。round-01–08 `B-data.md` 只用作待复验清单与行文格式，不作为证据。

**冻结核验：`HASH_MISMATCH`。** 按 `.planning/audits/round-09/VERSION.md` 文档化脚本（POSIX relpath + `\x00` + 文件字节）独立复算：

| 时刻 | 范围内文件数 | 复得 SHA-256 | 对声明 `9ffc4cd93e…` |
|---|---:|---|---|
| 开读（T0） | 60 | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20` | **当时 MATCH** |
| 中段（生产已改、测试仍 60） | 60 | `57baf7b59208e09fd09850be906a9baf3a529d19082f124654a17d7cea60413e` | 不匹配 |
| 成文（T_write） | **61** | **`813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`** | **不匹配** |

VERSION 声明 60 文件、`pytest_author_claim=144`。成文对象是 61 文件（新增 `tests/test_round07_regressions.py`），全量 pytest **153 passed**。审查期间还观察到一次撕裂写入：`event_density_sets` 调用尚未定义的 `_fallback_noise_set` 而 `NameError`。声明冻结对象已不在磁盘上。**下列结论绑定成文时磁盘 digest，不能为 `9ffc4cd93e…` 背书。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-09） |
| review_time | `2026-09-21T02:14:00+08:00`（复算 hash / 开读）— `2026-09-21T02:50:00+08:00`（成文） |
| declared_frozen_hash | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（`.planning/audits/round-09/VERSION.md`，声称 60 文件） |
| independently_recomputed_hash | **`HASH_MISMATCH`**。T0 曾复得声明值；成文 **`813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`**（61 文件）。配方与 VERSION 一致。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿单独信任 HEAD） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5 / §5.15；`FEATURES.md` T1–T4 合同；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02、T2NOOP-01、STRUCT-01、SURF-01、DECIDE-01 |

相对 T0 冻结快照，成文时已变：`measure.py` / `events.py` / `edits.py` / `splits.py` / `cli.py` / `t2_gsm_plus.py` / `t2_gsm_symbolic.py` / `repair.py` / `transfer.py` / `test_round03_regressions.py` / `test_round06_regressions.py`；新增 `tests/test_round07_regressions.py`。`graphs.py` / `schema.py` / `generate.py` / `t1_*` / `t2_noop.py` / `t3_*` / `t4_boundary.py` / `catalog.py` / `analysis.py` / `executor.py` / `scoring.py` 与 T0 同 digest。夹具字节未变。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对测量/划分/scientific prepare 调用链而通读；`fixture` = 对照适配器读完。digest 为成文时独立 SHA-256。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 388 | `c81e2402671228b6ac8b42437b9d48b2ef1834f41b82275c2975114dab1063d6` | full 1–388 | 广播 `noise_ref`；`real_hits` 写入 N；空 `event_id` 回退 |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`review_status`；`merge_review` 无 CLI |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | 祖先只返回节点键；非算术 `graph_kind` → `{}` |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf` | full 1–287 | 改名现改 id/父母/表达式；仍是单源改名 |
| `src/reasoning_diff/splits.py` | 152 | `08f77e972927a9961885c09e0538f0c43d47ca6638944e1c80465cf6cc4af066` | full 1–152 | `q:` 文本键；进程内 `_TEST_ONLY_FAMILY_KEYS`；`siblings` 无生产传入 |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full 1–385 | 身份、`scan_state`、placeholder/spec |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full 1–109 | 默认 unavailable；child `isolated_sandbox=False` |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full | 域内评分；默认不宿主 exec |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | 别名；不补图；不传 `siblings` |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `register_test_only_family`；`shared_gsm_text` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 写 `shared_gsm_text`；不注册锁 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 注入后祖先、`noop_proof` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | 口述保持 `requires_independent_truth` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder；Spec `valid` 仅 `tests_passed` |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式、整题 placeholder |
| `src/reasoning_diff/cli.py` | 1251 | `ba474e1fea1f7c5ab3488c90b32c776862d3651f281be38a543522e9ebeb5e98` | callsite 257–410, 546–561, 671–688, 784–840 | `trace-source`；`sham:`；`trace_ids`；`split_for_task` 无 siblings |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844` | callsite 105–192 | 只解析 `generated`；`parse_region=generated` |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169, 215–257 | P2 整数分母；Gate 未注册 |
| `tests/test_review_regressions.py` | 397 | `d3814498fe52b28b7905dc2c07e86e8e893b285081e4c37724a67c0f61b164ee` | full | 不锁本轮独立反例 |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a33933f5d6cba276745e191cbb22b13d13a8faf19af8d86b01` | full | |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb555851beeaa193e39e3e221759af4c986df8a05d3bdb8e7702666` | full | 夹具族键；不测孤立 Symbolic |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae440d6c939c210674070ca7bf80ee6c3cb2644d7b04c515a2` | full | 锁 `sham:` 与 pair kind |
| `tests/test_round06_regressions.py` | 145 | `ac7e4e88248ff49edcd6f992cf48ff88409172c34ce7fa934ca288816fdf946c` | full | 生成区；`trace_ids`；不测广播 N |
| `tests/test_round07_regressions.py` | 169 | `cad435add5103d94bb6d660ca6599d42f5f650c152d142b4e38c5dc284ee860e` | full | 先加载 Plus 再锁 Symbolic；不测孤立路径 |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c` | full | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003bf134d1ef9d6c06206a7b836e15c69cd1126bc1ae6d482123` | full | |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36` | callsite | 非本通道主证据 |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 r06–r08 相同，未改字节）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

## 3. 已执行检查

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-01 | 本通道切片 pytest | `python -m pytest tests/test_review_regressions.py tests/test_measure.py tests/test_t1_official.py tests/test_t2_gsm.py tests/test_t3_t4.py tests/test_round03_regressions.py tests/test_tracer_t1_prepare.py tests/test_round04_regressions.py tests/test_round05_regressions.py tests/test_round06_regressions.py tests/test_cli_pipeline.py tests/test_science.py -q --tb=line` | **135 passed**，exit 0。绿测试不能关闭下列独立反例。 |
| X-02 | 全量本机 pytest | `python -m pytest tests -q --tb=line` | **153 passed**，exit 0，约 18.9s。无 skip/xfail。VERSION 声称 144；范围内已多 1 个测试文件。仍不是科学正确性证据。 |
| X-03 | 矩阵 `noise=None`（B-01） | `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `S.noise=None`，`S.excess=None`，`rho_S_noise=None`，`null_reason=noise_missing`。保持关闭。 |
| X-04 | 有限扫描 `no_response_observed_in_scan`（B-02） | 仅 `outcome=no_change` + 该 scan_state | `behavior_label=None`，`behavior_known=False`。保持关闭。 |
| X-05 | `observed_response` + `no_change` ± `exhaustive`（B-23） | 同上两旗标 | 无 `exhaustive` → unknown；`exhaustive=True` → `behavior_label=0`。保持关闭。 |
| X-06 | sham 不进入 R_behavior（B-03） | 编辑 exhaustive no_change + `sham:q` changed | 行为袋 `(q,p2)=0`；`(q,sham:q)` 行为 unknown、`task_label=0`；`noise_ref=1.0` **仍广播到两行**。 |
| X-07 | 删除后对齐（B-04） | 两版 `q` vs 一版 | `pairs=[]`；`merged` 非空；`scanned=False`；`strategy_detector=status_field_only`。 |
| X-08 | 等计数同 `node_id` | 值 1/2 vs 9/2 | 配成 `(1,9),(2,2)`，双方 `node_id=q`。身份键不含 value。 |
| X-08b | 等计数不同 `node_id` | 左 `q`、右 `r` | `pairs=[]`，记 ambiguous。 |
| X-09 | R_surf vs 图父母（B-06/B-25） | 裸赋值 / 值后提及 / 赋值前 | 父母 `['p1','p2']`；裸 surface `[]`；值后与赋值前均为 `['p1']`。 |
| X-10 | HumanEval 族 / kind（B-07/B-17） | `load_humaneval` | `base_group_id=HumanEval/0`。前提 `kind=placeholder`，全文 42 字符。`assign_split("HumanEval")` 仍为 `probe_train`。 |
| X-11 | 公式编辑（B-08） | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，premise/node/answer 为 5/3/8/8。 |
| X-12 | 数值子串（B-09） | `"has 13 apples"`、值 `"3"` | `ValueError: not a unique isolated token`。T1 路径保持关闭。 |
| X-13 | 小数 3.5/5 与 5.5/5.0（B-24） | `_replace_isolated_value` | 完整孤立 token `3.5`→`9` 合法成功。`5` 对 `5.5`/`5.0`/`+5.5`/`15.5` 仍抛错。孤立 `p1 = 5` → `p1 = 9`。 |
| X-14 | no-op 证明（B-10） | 前端注入；有图 / 无图 | 缺独立判断拒绝。T1：注入后 `ancestors(q)={p1,p2}`，`noop_proof=recompute_and_ancestors`。Plus 无图：`unknown_without_graph`。 |
| X-15 | CSP 空父母 + unknown（B-11） | `task_parents=[]`，`graph_status=unknown` | `csp=None`，`clean_matched=0`。 |
| X-16 | CSP 空父母 + complete | 同上但 `complete` | `csp=1.0`，`clean_matched=1`。 |
| X-17 | `assign_family`（B-13） | 缺 id；同 id 不同子集 | 缺 id 抛错。同 `family_id` 角色相同。 |
| X-18 | GSM-Plus 生产划分（B-14） | 夹具 / 官方字段子集 / `refuse_fit_split` | Plus 行仍锁 `test`。见细项。 |
| X-19 | 跨集族键 / 共组（B-15 / B5-01） | 孤立 Symbolic；官方 Plus；`siblings`；进程寄存器 | **文本键可对齐；族 ID 仍不等；孤立 Symbolic 仍 `probe_train`。** 见细项。 |
| X-20 | T3 编辑 / 组成图（B-16 / B5-03） | `document_edit` + `new_answer` / `paragraph_edit` / `ancestors` | Hotpot / MuSiQue 口述保持 `requires_independent_truth`。`ancestors(musique/hotpot/plus/he)=={}`。 |
| X-21 | CLI fixture prepare + sham（B-12） | `main(["prepare", …, "--sham-opportunities","1"])` | exit 0。sham `premise_id="sham:q"`。`trace_ids.same_value_diff_source=None`（无 `trace-source`）。 |
| X-21b | CLI 已观察 no_change | `--edit-premise p1 --edit-value 7` | `outcome=no_change`，`exhaustive=False`，`raw_values=["0","0"]`。 |
| X-21p | Plus 八类扰动（B-21） | 独立喂官方类名 | `critical thinking` / `missing information` → `insufficient_information`。`reversing operation` → `query_target_change`。其余六类 `(None, None)`。 |
| X-22 | P2 分母（B-22） | `p2_paired(..., 99)` ± `shared_premises` | 只传 99 → `denominator_unverified`。99 vs `["p1"]` → `denominator_inconsistent`。一致时 `ok`。 |
| X-22n | 多节点祖先 | 内存 s=p1+p2、t=s+p1 | `anc[t]={p1,p2}`。 |
| X-23 | 空 `noise_set` ± `noise_evaluated`（B-26） | 集合密度 API | 未评估空集 → `noise_set_empty`。已评估空集 → `rho_S_noise=0.0`。 |
| X-12e | `event_density_sets` 0-hit / 命中 | 构造标签；scientific CLI | 0-hit：`rho_M_noise=1`，`excess_M=0`。**命中+广播：N={p1,p2}，`rho_M_noise=0`，`rho_M_excess=1.0`，`null_reason=None`。** 仅 `sham:q` 行：`noise_set_missing`。 |
| X-24 | 多匹配行 / 非法 scan_state（B-27） | `"q = 0 q = 1\\n"`；非法枚举 | fixture 两条 `ambiguous`。`parse_events` 两版本 `ok`。非法 scan_state 抛 `ValueError`。 |
| X-25 | 改名 / 来源—数值 / 复核（B-18 / B5-05） | `make_source_value_pair` / CLI / `merge_review` | 表达式现为 `p1 * p2_src`，前提 id 现为 `p2_src`。**仍是单源改名。** `review` 导出恒 `None`；`merge_review` 仅 API。 |
| X-26 | 官方夹具重算（B-19） | 夹具 9；篡改答案 8 | 9=9。不一致拒绝。fixture 加载器拒 official 形状。 |
| X-27 | 除法模运算 | `_eval_expr("5 / 2", {}, 23)` | `2`（`int(truediv)%mod`），不是模逆 14。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-plus-sub | Plus 孤立数字（B5-02） | 官方字段题干含 13 与 3 | `3`→`9` 只改孤立 3。仅含 `13`、改 `3` fail-closed。`validity=needs_truth`。 |
| X-he-rho | HumanEval 进 ρ（B-17） | `kind=placeholder` | placeholder 不进 P。 |
| X-he-exec | Spec 裁判（B-16 HE） | 无解 / Unavailable / ChildProcess | 无解与不可用均为 `needs_truth`。ChildProcess + `assert True` → `valid`；`isolated_sandbox=False`。默认 Unavailable。 |
| X-label | CLI label | `main(["label", "--in-dir", sci_prepare])` | exit 0。密度与 prepare 一致：命中后 `rho_M_excess=1.0`。 |
| X-msq | MuSiQue 配对 id | 夹具两条 | `msq-9::answerable` / `msq-9::unanswerable`，同 `base_group_id`。 |
| X-t4 | T4 四态 | `load_t4` | 四态齐全；前提均为 placeholder。 |
| X-t1cfg | T1 格子 | `validate_t1_prepare_config` | 四档 op + n=500 + mod=23；op=7 拒绝。 |
| X-cat | catalog 别名 | `load_snapshot("t3_musique")` / `t4_boundary` | 可加载。 |
| X-gate | Gate 0–2 | `week8_decision({})` 与带 `rho_S_excess=0.5` | 三门 `unregistered`；`scientific_conclusion=None`。**不是缺陷。** |
| X-sci | scientific prepare | `main(["prepare", "--eval-mode","scientific", "--split-fractions", …, "--sham-opportunities","1"])` | exit 0。7 条轨迹均 `parse_region=generated`、各仅事件 `q`。含 `trace-source`。见细项。 |
| X-b601 | 生成区事件（B6-01） | `generate_task_trace` + CLI 七条轨迹 | 事件仅 `q`，`start>=len(prompt)`。题干 `parse_events` 仍能解析 `p1`/`p2`。原触发保持关闭。 |
| X-fallback | 空 `event_id` 回退 | 全标签 `event_id=""` 且 `noise_ref=1.0` | **`_mapped_noise_hits` 把 p1/p2 写入 N**，`rho_M_noise=0`，不再 `noise_set_missing`。 |
| X-tids | `source_value_pair.trace_ids` | scientific / fixture `edits.jsonl` | scientific：`base=trace-base`，`same_source_diff_value=trace-edit`，`same_value_diff_source=trace-source`。fixture：第三臂 `None`。`_pair_source_value` 只用 value 臂。 |

**X-18 / X-19 细项（独立；先 `clear_test_only_families()`）：**

- 夹具 Plus（有 `original_id=gsm8k-12`）：`shared_gsm_family=gsm8k-12`，`shared_gsm_text=q:ada has 4 apples…`，`base_group_id=gsm_plus:gsm8k-12`，`split=test`。
- 官方 Plus 字段（无 `original_id`）：`shared_gsm_family=shared_gsm_text=q:ada has 4 apples and buys 3 more. how many apples?`。**没有 seed 文本 → GSM8K ID 的匹配。**
- 孤立 Symbolic `original_id=gsm8k-1`（未先加载 Plus）：`shared_gsm_family=gsm8k-1`，`shared_gsm_text` 与官方 Plus 文本键相等，但 **`split_for_task=probe_train`**。`assign_split("gsm8k-1")==probe_train`。
- 同进程先 `load_gsm_plus`（官方或带 id）后：Symbolic 因 `_TEST_ONLY_FAMILY_KEYS` 变成 `test`。`clear` 之后再次孤立 → 又是 `probe_train`。
- `split_for_task(symbolic, siblings=[plus])` 在清空寄存器后也能锁 `test`。**`cli.cmd_prepare` 只调用 `split_for_task(task)`，不传 siblings。**
- 官方 Plus 族 ID 与 Symbolic `gsm8k-*` **不相等**（`keys_equal_off=False`）；只共享 `q:` 文本键。

**X-sci / X-b601 / X-tids / X-12e 细项（不信任作者测试）：**

- 轨迹 id：`trace-base` / `trace-t0p` / `trace-edit` / **`trace-source`** / 两条 allowed value edit / `trace-sham`。文本为 tiny 解码 + 约束 `\nq = <digits>`。
- `parse_region=generated`：**成立。** 七条均仅事件 `q`，`start>=prompt_len`。`trace-source` 的 `start=53`（改名题干更长）。无 `p1`/`p2`/`p2_src` 事件。
- sham：`premise_id=sham:q`，`changed`（82 vs 53），`node_id=q`。`_e_premise_ids` 仍为 `['p1','p2']`。
- 标签：`(q,p1)`/`(q,p2)` 的 `task_label=1`、`behavior_label=None`、**`noise_ref=1.0`（广播）**；`(q,sham:q)` 的 `task_label=0`。
- 密度：**`rho_M_raw=1.0`，`rho_M_noise=0.0`，`rho_M_excess=1.0`，`null_reason=None`。** `labels.jsonl` 的 note 仍写「sham hits are not mapped onto real premises」，与数字矛盾。
- `edits.jsonl`：`kind=source_value_pair`，`trace_ids` 三键齐全。`same_value_diff_source.task` 题干/表达式/前提 id 均为 `p2_src`。donor API 返回 `(base, edit, "same_source_diff_value")`，**不读 `trace-source`**。
- fixture prepare：`same_value_diff_source=None`，轨迹只有 base/edit/sham。

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU；`merge_review` 无 CLI 入口 |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 B5-01 已在夹具与官方字段子集确认 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b`。见 U-01 |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | tiny 解码不是科学噪声协议；**广播入账已在本机确认** |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## / B6-## 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。下表针对 **round-01–06 原 ID**。作者主张关闭 B6-01 / B6-02，以及 `source_value_pair` 写入 `edits.jsonl` / `trace_ids`。ISSUES 未主张关闭 B5-01。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | — | **closed** | X-03 |
| B-02 | — | **closed** | X-04 |
| B-03 | — | **closed**（行为袋 + 身份前缀） | X-06；CLI sham 写 `sham:` + `node_id` |
| B-04 删除 / 异 node_id | — | **closed** | X-07 / X-08b |
| B-05 `scanned=True` | — | **closed** | X-07 |
| B-06 / B-25 | — | **closed** | X-09 |
| B-07 | — | **closed** | X-10 |
| B-08 | — | **closed** | X-11 |
| B-09 / B-24 | — | **closed** | X-12 / X-13 |
| B-10 | — | **closed** | X-14 |
| B-11 | — | **closed** | X-15 |
| B-12 0-hit | — | **closed** | X-23 / X-12e 0-hit |
| B-13 | — | **closed** | X-17 |
| B-14 | — | **closed**（Plus 行） | X-18 |
| B-15 / **B5-01** | 未主张关闭 | **residual（仍 confirmed）** | X-19。文本键 ≠ 生产共组。 |
| B-16 Edit 口述 valid | — | **closed** | X-20 |
| **B5-03** Hotpot status | — | **closed** | X-20 |
| B-17 | — | **closed** | X-he-rho |
| B-18 / **B5-05** | 落盘 / `trace_ids` / 图 id 改写 | **residual（仍 confirmed）** | X-25。一致改名 ≠ A/B 来源。 |
| B-19 | — | **closed** | X-26 |
| B-20 | — | **closed** | X-20 `ancestors=={}` |
| B-21 | — | **closed** | X-21p |
| B-22 | — | **closed** | X-22 |
| B-23 | — | **closed** | X-05 / X-21b |
| B-26 | — | **closed** | X-23 |
| B-27 | — | **closed** | X-24 |
| **B5-02** Plus 子串 | — | **closed** | X-plus-sub |
| **B5-04** / **B6-02** 命中不入账 | closed locally | **reopened（见 B9-01）** | X-12e / X-sci / X-fallback |
| **B6-01** 题干前提当生成事件 | closed locally | **closed**（原触发） | X-b601 / X-sci |

## 6. 发现（本轮开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B9-01 sham 命中经广播把真实前提写入 N 并入账 excess（重开 B6-02 / B5-04）

- **状态：** confirmed defect
- **严重度：** critical
- **符号：** `measure.build_labels`；`measure.event_density_sets`；`cli.cmd_prepare`
- **行号：** `measure.py` 72–78, 281–345；`cli.py` 367–376, 405–408
- **协议：** MEAS-02：噪声机会与任务/行为标签分开；命中不得把空 N 或**未观测到的真实前提**记成已评估参照。
- **证据：**
  1. `build_labels` 仍把某事件上任意 sham `changed` 广播为该事件**所有**标签行的 `noise_ref=1.0`，包括 `(q,p1)` / `(q,p2)`。
  2. 新逻辑 `real_hits = [h for h in hits if h in premises and not sham:]` 于是得到 `N={p1,p2}`，`noise_evaluated=True`。
  3. X-sci：scientific prepare + sham seed=2，`q` 从 82 变 53（不同随机流的约束数字，不是前提编辑）。写出 `rho_M_raw=1.0`，`rho_M_noise=0.0`，**`rho_M_excess=1.0`**，`null_reason=None`。
  4. 同文件 note 仍声称「sham hits are not mapped onto real premises」。
  5. 仅保留 `(q,sham:q)` 行时才走 `noise_set_missing`。空 `event_id` 回退经 `_mapped_noise_hits` 同样把 p1/p2 写入 N。
  6. 作者 `test_c7_m01_mapped_noise_premise_is_deducted` 直接喂 `noise_set=["p3"]`，不测广播，不测 CLI。
- **影响：** 本机 scientific 资产会把「生成数字跨 seed 抖动」记成已评估噪声参照，并给出非空有符号 excess。这是静默错误科学指标。
- **建议：** 噪声身份只来自 `sham:` 行；广播不得把真实前提标成 hit。有 hit 且无法映射到独立噪声前提时保持 `noise_set=None`。

---

### B5-01 跨数据集 GSM 族仍不在生产路径共组（原 B-15）

- **状态：** confirmed defect（机制）/ pending_server（真实 dump 碰撞率）
- **严重度：** high
- **符号：** `splits.split_for_task`；`splits.gsm_family_id` / `gsm_text_key`；`t2_gsm_plus.load_gsm_plus`；`cli.cmd_prepare`
- **行号：** `splits.py` 13–32, 35–46, 95–121；`t2_gsm_plus.py` 20–22, 44–45；`t2_gsm_symbolic.py` 63–64；`cli.py` 261
- **协议：** DATA-03 / FEATURES T2：以规范化 `seed_question` **连接 GSM8K ID**；同源题同族。GOAL §5.5：Plus 测试专用不得把同源 Symbolic 放进 `probe_train` 再当未见题。
- **证据：**
  1. 新增 `q:` 文本键。官方 Plus（无 `original_id`）与 Symbolic 的 `shared_gsm_text` 可相等；**`shared_gsm_family` 仍分别为 `q:…` 与 `gsm8k-*`。无 seed→GSM8K 匹配。**
  2. Plus 加载时 `register_test_only_family` 写入**进程全局**集合。先加载 Plus 再划分 Symbolic → `test`（作者 `test_plus_locks_symbolic_family_to_test` 只锁这条）。
  3. X-19：`clear` 后孤立 Symbolic `gsm8k-1` → **`probe_train`**。`assign_split("gsm8k-1")==probe_train`。
  4. `siblings=` 可锁，但 prepare **不传 siblings**，catalog 一次只加载一种 snapshot。Symbolic-only 生产 prepare 走孤立路径。
  5. 寄存器可 `clear`；划分随加载顺序变。这不是可复现的族表。
- **影响：** 服务器 dump 若按数据集分批 prepare，同源 Symbolic 仍进拟合、Plus 当未见测试。消费字段 / 进程锁不能代替共组。
- **建议：** 规范化 seed 匹配 GSM8K ID，失败则显式 `unmapped`。同一族键必须得到同一角色，且 Plus 的 test-only **持久化到整族**（文件/清单），而不是模块级 set。

---

### B5-05 来源—数值对仍是单源改名（原 B-18）

- **状态：** confirmed defect
- **严重度：** medium
- **符号：** `edits.make_source_value_pair` / `apply_rename_edit`；`cli.cmd_prepare`；`events.merge_review`
- **行号：** `edits.py` 151–226；`cli.py` 298–302, 384–396, 674–687；`events.py` 219–248
- **协议：** DATA-01 / FEATURES 来源—数值：同图族来源 A/B，先 `a=b` 再 `a≠b`；MEAS-01：可导出**与回填**人工复核。
- **证据：**
  1. X-25 / X-tids：scientific **确实**写入 `kind=source_value_pair` 与 `trace_ids`（含 `trace-source`）。fixture 第三臂为 `None`。
  2. 改名现改写 `premise_id` / parents / `expression`（`p1 * p2_src`）。图内部一致，**但仍是一个来源节点改名**，没有第二来源节点，也没有 A/B 解耦图。
  3. `trace-source` 进入 `traces.jsonl` / collect 的 H 行；观测/标签循环不包含该臂。donor 只用 `same_source_diff_value`=`trace-edit`。
  4. `review_export` 的 `review` 恒 `None`，`review_status=awaiting_human`。`merge_review` 在 `src/` 无 CLI / 生产调用方。
- **影响：** C2 所需的同值异源图对仍不能从数据层按协议生成。落盘 + `trace_ids` + 表达式改写 ≠ DATA-01 完成。

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01 | X-03 | — |
| B-02 | X-04 | — |
| B-03 行为袋 + `sham:` 前缀 | X-06 / X-sci | 广播仍污染 N（B9-01） |
| B-04 / B-05 | X-07 / X-08b | — |
| B-06 / B-25 | X-09 | U-03 |
| B-07 | X-10 | — |
| B-08 | X-11 | — |
| B-09 / B-24 | X-12 / X-13 | — |
| B-10 | X-14 | — |
| B-11 | X-15 | X-16 |
| B-12 0-hit | X-23 / X-12e | — |
| B-13 / B-14 | X-17 / X-18 | B5-01 |
| B-16 Edit / **B5-03** | X-20 | 口述值仍写入，status 已诚实 |
| B-17 | X-he-rho | S 列表可含 `spec`，分母 null |
| B-19 / B-20 / B-21 | X-26 / X-20 / X-21p | pending_server 真实 dump |
| B-22 / B-23 / B-26 / B-27 | X-22 / X-05 / X-23 / X-24 | — |
| **B5-02** | X-plus-sub | — |
| **B6-01** | X-b601 / X-sci：事件仅生成区 `q` | U-10 |
| **B6-02 身份前缀** | X-21 `sham:q`；E 列跳过 | **入账路径已重开为 B9-01** |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径缺协议 → null | `measure.py` 124–135 | 不否定 B9-01。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 371–379 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` 38 | 不否定 B5-01。 |
| ND-07 | Hotpot supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 34–38 | |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | |
| ND-09 | HumanEval 默认不宿主 exec | `scoring.py`；`executor.py` | Child process 标 `isolated_sandbox=False`。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` | `official_noop_release=False`。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 251–257 | |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` | `splits.py` 124–142 | 原语正确；不否定 B5-01。 |
| ND-13 | T1 配置拒绝非白皮书格子 | `t1_config.py` | |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 59–60 | |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05/X-21b。 |
| ND-16 | 官方加载对照 template 重算 | `t1_official.py` 77–80 | |
| ND-17 | 策略分岔 `scanned=False` | `events.py` 184–192 | |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `measure.py` 324 | |
| ND-20 | HE Spec `valid` 仅 `tests_passed` | `t3_humaneval.py` 44–67 | |
| ND-21 | Plus/T4/Hotpot/MuSiQue Edit 缺核验不写 valid | 各 apply* | |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 124–134 | |
| ND-23 | MuSiQue answerable 配对保留 | `t3_musique.py` 43–68 | |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | `analysis.py` 215–257 | **不是缺陷。** |
| ND-25 | Plus 孤立替换与 T1 共用 `_replace_isolated_value` | `t2_gsm_plus.py` 53–58 | |
| ND-26 | scientific 拒 0 事件 | `cli.py` 296–297 | |
| ND-27 | `_e_premise_ids` 跳过 `sham:` | `cli.py` 707–716 | sham 身份不进拟合列。 |
| ND-28 | 约束 `\nq = <digit>` 是 tiny 可解析接口 | `generate.py` 72–98, 148–190 | 不是 §4.1 自然 CoT；不因此判 B6-01 未关。 |
| ND-29 | T3/placeholder 跳过 `source_value_pair` | `cli.py` 674–687 | `_try_source_value_pair` fail-closed。Hotpot/MuSiQue prepare 不写该 kind。 |
| ND-30 | scientific 生成 `trace-source` 并写 `trace_ids` | `cli.py` 298–302, 392–396 | 持久化成立；不否定 B5-05。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产；`merge_review` 无生产入口 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；tiny 命中不能当协议命中率 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 | 机制层 B5-01 已确认；dump 上匹配率 pending |
| S-07 | Linux cgroup / 容器隔离执行器 | EXEC-01 / GOAL §5.15 | 本机仅 Unavailable + 非沙箱子进程 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod` | FEATURES 称官方 Num 为加减乘；夹具无除法。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official` | 可解释为题源。 |
| U-03 | `surface_mentions` 只匹配 `premise_id` / alias 词 | 未在真实题干别名上抽样。 |
| U-04 | 后续 stage 是否用 `task_id` 而不是族键做划分 | CLI fit 只信 `--split` 旗标。 |
| U-05 | 前提 span 同时含孤立整数与小数时整数编辑被拒 | 当前 fail-closed。 |
| U-07 | `distinguishing_tests=True` 仅因 `new_tests` 非空 | 与 `validity=needs_truth` 并存。 |
| U-08 | `behavior_label!=1`（含 unknown）进入 M | 协议「未知不作负标签」。scientific 上 `M={p1,p2}`、`rho_M_raw=1` 来自 tiny 未改数字。未升格；**不掩盖 B9-01 把该 M 的噪声记成 0。** |
| U-09 | `apply_spec_edit` 不检查 `isolated_sandbox` | CLI 默认不走 child process。 |
| U-10 | `parse_events` 仍把非 placeholder 前提登记为可解析实体 | 生产只喂生成区。tiny 未回显 `p1 =`。暂不重开 B6-01。 |
| U-11 | collect 用 **base** `task.premises` span 对 `trace-source`（改名题干）做 E 池化 | H 行含 source 臂；E 为跨轨迹均值。未见评分把该 E 当科学结论。未升格。 |
| U-12 | 进程全局 `_TEST_ONLY_FAMILY_KEYS` 使 pytest 顺序可改变后续划分 | 已在 B5-01 记为机制缺陷的一部分；单独复现危害取决于加载顺序。 |

## 11. 测试质量对本通道的含义

**135 / 153 passed ≠ 数据/测量正确。** 作者补了生成区、`sham:` 前缀、`trace_ids`、图 id 改写、先加载 Plus 再锁 Symbolic、`merge_review` API。独立同意 **B6-01 原触发** 仍关。缺口：

- `test_plus_locks_symbolic_family_to_test` **先加载 Plus**（或依赖寄存器），再断言 Symbolic=`test`。不测 `clear` 后的孤立 Symbolic-only prepare，不测 CLI 无 `siblings`，不要求族 ID 相等。
- `test_plus_and_symbolic_share_gsm8k_family` 仍只用带 `original_id` 的夹具。
- `test_source_value_pair_rewrites_graph_ids` / `trace_ids` 只锁改名一致性与 JSON 键，不锁第二来源节点。
- `test_c7_m01_mapped_noise_premise_is_deducted` 手填 `noise_set`，**不测广播、不测 scientific sham**。
- `test_sham_hits_do_not_book_evaluated_zero_noise` 仍只查 `rho_S_noise is None`，在 S 分母为空时即使 N 被填满也会绿。
- `test_review_export_can_merge_human_rows` 只测函数，不测 CLI 回填。

因此不能关闭 B5-01 / B5-05。B6-02 原「命中不入账」在当前磁盘上已独立证伪。

## 12. 通道结论

数据与测量通道 **不能** 在声明冻结 `9ffc4cd93e…` 或成文磁盘 `81308124…` 上给出通过意见。**FAIL。**

1. **`HASH_MISMATCH`：** 开读时声明 hash 可复现（60 文件）；审查中生产与测试被改写，成文为 61 文件 `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`。连续通过计数必须保持 0。全量 pytest **153 passed**（作者声称 144），不是验收。
2. **猎项独立结论：**
   - **生成区事件（B6-01）：** 仍成立。scientific / `generate_task_trace`（含新 `trace-source`）只解析生成区，事件均为约束 `q`。
   - **`sham:` 前缀：** 身份仍写 `sham:<node>`，E 列仍跳过。**入账路径已坏（B9-01）。**
   - **`source_value_pair.trace_ids`：** scientific 落盘齐全且生成 `trace-source`；fixture 第三臂为 `None`。donor 读 value 臂。**不关闭 B5-05。**
   - **族共组（B5-01）：** 文本键与进程锁是半成品。孤立 Symbolic 与无 `siblings` 的 prepare 仍把 `gsm8k-1` 划为 `probe_train`。官方 Plus 族 ID 仍是 `q:` 而非 GSM8K ID。
3. **本轮确认的机制缺陷：**
   - **B9-01（critical）：** sham 命中广播 → `N={p1,p2}` → `rho_M_excess=1.0`。重开 B6-02 / B5-04。
   - **B5-01 / B-15（high）：** 生产共组仍失败。
   - **B5-05（medium）：** 图 id/表达式已随改名改写，对已落盘，语义仍是单源改名；复核无生产回填。
4. T2/T3 真值旗标、T1 来源隔离、有限扫描 unknown、身份不含值、HE placeholder、Gate 未注册仍成立（ND-01–ND-30），不能抵消冻结漂移、划分共组、来源—数值语义与噪声入账缺口。Gate 0–2 未注册与 `scientific_conclusion=None` **不是缺陷。**
