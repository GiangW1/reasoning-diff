# Review B — 数据与测量（独立审查，round-06）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-06 通道报告。round-01/02/03/04/05 `B-data.md` 只用作待复验清单与行文格式，不作为证据。

**冻结核验：`HASH_MATCH`。** 按 `.planning/audits/round-06/VERSION.md` 文档化脚本（POSIX relpath + `\x00` + 文件字节，59 个范围内文件）独立复得 `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`。与声明值一致。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-06） |
| review_time | `2026-09-21T01:50:00+08:00`（复算 hash / 开读）— `2026-09-21T03:25:00+08:00`（成文） |
| declared_frozen_hash | `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（`.planning/audits/round-06/VERSION.md`） |
| independently_recomputed_hash | **`HASH_MATCH`** `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`。59 个范围内文件。配方与 VERSION 一致。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿单独信任 HEAD） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3；GOAL §5.1–5.5 / §5.15；`FEATURES.md` T1–T4 合同；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02、T2NOOP-01、STRUCT-01、SURF-01 |

相对 r05 生产 digest 已变：`measure.py` / `events.py` / `splits.py` / `t2_gsm_plus.py` / `t3_hotpot.py` / `cli.py` / `analysis.py` / `catalog.py` / `executor.py`（本通道核对）。`graphs.py` / `edits.py` / `schema.py` / `t1_*` / `t2_gsm_symbolic.py` / `t2_noop.py` / `t3_musique.py` / `t3_humaneval.py` / `t4_boundary.py` / `scoring.py` 与 r05 同 digest。夹具字节与 r05 相同。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对测量/划分/scientific prepare 调用链而通读；`fixture` = 对照适配器读完。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 342 | `a6bcd893abedaf3bbe7a4804cde55a78b7d7fc1f68133e3c6643de346eb134dc` | full 1–342 | 标签、S/M、`noise_evaluated`、空 `N`、TO/CSP、`event_density_sets` |
| `src/reasoning_diff/events.py` | 261 | `20c57f55ec3c3571182a19a769f5a521b4842a98ad6c227f50b5bdcdfab9cd13` | full 1–261 | 前提+节点解析、身份不含值、等计数 `node_id`、`scanned=False` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | 祖先只返回节点键；非算术 `graph_kind` → `{}` |
| `src/reasoning_diff/edits.py` | 277 | `bfd1632b50504c042640bcda85368b0c695fd3f843ea885200d080055aa107b6` | full 1–277 | 孤立 token、重算、改名、`make_source_value_pair` |
| `src/reasoning_diff/splits.py` | 111 | `35cd0e3f724ee850b4cf28a118717d51d188ae913a2917562fc29110ccd7cbdc` | full 1–111 | `shared_gsm_family` 消费、`source` 锁 test、`assert_same_role` 无调用方 |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full 1–385 | 身份、`scan_state`、placeholder/spec、`Edit.exhaustive` |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full 1–109 | 默认 unavailable；child process `isolated_sandbox=False` |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full | 域内评分；默认不宿主 exec |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `80e4db4b0241b9194216da74c60671916a9fa3c50f9f8d676b8f7cc17b53875d` | full | 加载分派，不补图 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 81 | `8e58c5d22b41b87b5f422fdbba10488eb42ad4af607610f8d674c4c094b7772e` | full | 孤立替换、`requires_independent_truth`、`gsm_plus:` 前缀 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 84 | `b50db6533f18948d141a75a38970b491269a127b990bd818408f29a8e28219af` | full | sidecar、公式编辑、族键 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 注入后祖先、`noop_proof` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | 口述答案保持 `requires_independent_truth` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder；Spec `valid` 仅 `tests_passed` |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式、整题 placeholder |
| `src/reasoning_diff/cli.py` | 1052 | `45a11e124b1dda8c85780d9b2909eaa8fe3901cdede88f0db4f5d2fd70a54898` | callsite 94–122, 182–411, 507–528, 959–976 | prepare/label；scientific 拒 0 事件；sham 写 `node_id` |
| `src/reasoning_diff/models/generate.py` | 191 | `f92f3ba61ec735fb52d29ea6a8f0768c855fded2ab0eef096c0ce22aeda72b5a` | callsite 105–182 | 约束 `q = <digits>`；`parse_events` |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169 | P2 整数分母 → `denominator_unverified` |
| `tests/test_review_regressions.py` | 397 | `d3814498fe52b28b7905dc2c07e86e8e893b285081e4c37724a67c0f61b164ee` | full | 作者回归；不锁本轮独立反例 |
| `tests/test_round03_regressions.py` | 291 | `5698a410c0669b6142f31d5b302ff8c7ef8ec66cc9ef429786d45e2418bfc278` | full | |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb555851beeaa193e39e3e221759af4c986df8a05d3bdb8e7702666` | full | 夹具级 `shared_gsm_family`；不测共组角色 |
| `tests/test_round05_regressions.py` | 190 | `83a665a16567884fda83584e3f847842c6cb541375cf90c25fad1338fb420882` | full | 锁 Plus 孤立 / Hotpot status / scientific 非空 |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c` | full | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 r05 相同，未改字节）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

## 3. 已执行检查

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-01 | 本通道 + r03–r05 回归 pytest | `python -m pytest tests/test_review_regressions.py tests/test_measure.py tests/test_t1_official.py tests/test_t2_gsm.py tests/test_t3_t4.py tests/test_round03_regressions.py tests/test_tracer_t1_prepare.py tests/test_round04_regressions.py tests/test_round05_regressions.py tests/test_cli_pipeline.py -q --tb=line` | **117 passed**，exit 0。绿测试不能关闭下列独立反例。 |
| X-02 | 全量本机 pytest | `python -m pytest tests -q --tb=line` | **136 passed**，exit 0，约 15.7s。无 skip/xfail。与 VERSION `pytest_author_claim` 计数一致，仍不是科学正确性证据。 |
| X-03 | 矩阵 `noise=None`（B-01） | `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `S.noise=None`，`S.excess=None`，`rho_S_noise=None`，`null_reason=noise_missing`。保持关闭。 |
| X-04 | 有限扫描 `no_response_observed_in_scan`（B-02） | 仅 `outcome=no_change` + 该 scan_state | `behavior_label=None`，`behavior_known=False`。保持关闭。 |
| X-05 | `observed_response` + `no_change` ± `exhaustive`（B-23） | 同上两旗标 | 无 `exhaustive` → unknown；`exhaustive=True` → `behavior_label=0`。保持关闭。 |
| X-06 | sham 不进入 R_behavior（B-03） | 编辑 exhaustive no_change + `sham:0` changed | 行为袋 `(q,p2)=0`；`(q,"")` 行为 unknown；`noise_ref=1.0` 广播到两行。 |
| X-07 | 删除后对齐（B-04） | 两版 `q` vs 一版 | `pairs=[]`；`merged` 非空；`scanned=False`；`strategy_detector=status_field_only`。 |
| X-08 | 等计数同 `node_id` | 值 1/2 vs 9/2 | 配成 `(1,9),(2,2)`，双方 `node_id=q`。身份键不含 value。 |
| X-08b | 等计数不同 `node_id` | 左 `q`、右 `r` | `pairs=[]`，记 ambiguous。 |
| X-09 | R_surf vs 图父母（B-06/B-25） | 裸赋值 / 值后提及 / 赋值前 | 父母 `['p1','p2']`；裸 surface `[]`；值后与赋值前均为 `['p1']`。 |
| X-10 | HumanEval 族 / kind（B-07/B-17） | `load_humaneval` | `base_group_id=HumanEval/0`。前提 `kind=placeholder`，全文 42 字符。`assign_split("HumanEval")` 仍为 `probe_train`。 |
| X-11 | 公式编辑（B-08） | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，premise/node/answer 为 5/3/8/8。 |
| X-12 | 数值子串（B-09） | `"has 13 apples"`、值 `"3"` | `ValueError: not a unique isolated token`。T1 路径保持关闭。 |
| X-13 | 小数 3.5/5 与 5.5/5.0（B-24） | `_replace_isolated_value` | 完整孤立 token `3.5`→`9` 合法成功。`5` 对 `5.5`/`5.0`/`+5.5`/`15.5` 仍抛错。孤立 `p1 = 5` → `p1 = 9`。保持关闭。 |
| X-14 | no-op 证明（B-10） | 前端注入；有图 / 无图 | 缺独立判断拒绝。T1：注入后 `ancestors(q)={p1,p2}`，`noop_proof=recompute_and_ancestors`。Plus 无图：`unknown_without_graph`。 |
| X-15 | CSP 空父母 + unknown（B-11） | `task_parents=[]`，`graph_status=unknown` | `csp=None`，`clean_matched=0`。 |
| X-16 | CSP 空父母 + complete | 同上但 `complete` | `csp=1.0`，`clean_matched=1`。 |
| X-17 | `assign_family`（B-13） | 缺 id；同 id 不同子集 | 缺 id 抛错。`{A,B,C}` / `{B,C}` / `{Z}` 同 `family_id` 均为 `probe_train`。 |
| X-18 | GSM-Plus 生产划分（B-14） | 夹具 / 官方字段子集 / `refuse_fit_split` | 生产路径保持关闭。见细项。 |
| X-19 | 跨集族键（B-15 / B5-01） | 同题 Symbolic vs Plus；`gsm8k-1` | **消费方存在；共组角色仍失败。** 见细项与 B5-01。 |
| X-20 | T3 编辑 / 组成图（B-16 / B5-03） | `document_edit` + `new_answer` / `paragraph_edit` / `ancestors` | Hotpot 口述保持 `requires_independent_truth`。**B5-03 原触发关闭。** `ancestors(musique/hotpot/plus/he)=={}`。 |
| X-21 | CLI fixture prepare + sham（B-12） | `main(["prepare", …, "--sham-opportunities","1"])` | exit 0。真编辑 `p2`/`changed`。sham `premise_id="q"`（不再是 `""`）、`no_change`、`scan_state=observed_response`。标签另有 `(q,q)`。密度 `aggregation=mean_over_events`；t1_tiny 的 S 分母为空。 |
| X-21b | CLI 已观察 no_change | `--edit-premise p1 --edit-value 7` | `outcome=no_change`，`exhaustive=False`。 |
| X-21p | Plus 八类扰动（B-21） | 独立喂官方类名 | `critical thinking` / `missing information` → `insufficient_information`。`reversing operation` → `perturbation_status=query_target_change`。其余六类 `(None, None)`。 |
| X-22 | P2 分母（B-22） | `p2_paired(..., 99)` ± `shared_premises` | 只传 99 → `denominator_unverified`，`delta_rho=None`。99 vs `["p1"]` → `denominator_inconsistent`。一致时 `ok`。 |
| X-22n | 多节点祖先 | 内存 s=p1+p2、t=s+p1 | `anc[t]={p1,p2}`。 |
| X-23 | 空 `noise_set` ± `noise_evaluated`（B-26 / B-12） | 集合密度 API | 未评估空集 → `noise_set_empty`。已评估空集 → `rho_S_noise=0.0`，excess = raw − 0。 |
| X-12e | `event_density_sets` 0-hit / 缺失 / sham 命中 | 给 t1 加非祖先 `p3` | 0-hit：`noise=0`，`excess=raw`。无协议：`sham_protocol_missing`。**sham 命中（广播 `noise_ref=1.0`）：`N` 为空，`rho_S_noise=0`，`excess=1`。不再把 `p3` 写入 N。B5-04 原触发关闭。** |
| X-24 | 多匹配行 / 非法 scan_state（B-27） | `"q = 0 q = 1\\n"`；非法枚举 | 两条 `ambiguous`。非法 scan_state 抛 `ValueError`。 |
| X-25 | 改名 / 来源—数值 / 复核（B-18 / B5-05） | `make_source_value_pair` / `review_export` | 题干改 `p1_src`，**表达式仍 `p1 * p2`**。`review` 恒 `None`。保持 **B5-05**。 |
| X-26 | 官方夹具重算（B-19） | 夹具 9；篡改答案 8 | 9=9。不一致拒绝。fixture 加载器拒 official 形状。 |
| X-27 | 除法模运算 | `_eval_expr("5 / 2", {}, 23)` | `2`（`int(truediv)%mod`），不是模逆 14。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-plus-sub | Plus 孤立数字（B5-02） | 官方字段题干 `Ada has 13 apples and buys 3 more…`，`old="3"` | **题干变成 `Ada has 13 apples and buys 9 more…`。** `13` 未被改成 `19`。仅含 `13`、改 `3` 时 fail-closed。`validity=needs_truth`。**B5-02 关闭。** |
| X-he-rho | HumanEval 进 ρ（B-17） | `kind=placeholder` + `event_density_sets` | `denominator_S=None`，`rho_S_raw=None`。S 列表仍可能出现 `spec`，但不进分母。 |
| X-he-exec | Spec 裁判（B-16 HE） | 无解 / Unavailable / ChildProcess | 无解与不可用均为 `needs_truth`。`ChildProcessExecutor` 且测试通过 → `valid`；该后端 `isolated_sandbox=False`。默认 `get_executor()` 为 Unavailable。 |
| X-label | CLI label | `main(["label", "--in-dir", prepare_out])` | exit 0，写出标签 + densities。 |
| X-msq | MuSiQue 配对 id | 夹具两条 | `msq-9::answerable` / `msq-9::unanswerable`，同 `base_group_id`。 |
| X-t4 | T4 四态 | `load_t4` | 四态齐全；前提均为 placeholder。 |
| X-t1cfg | T1 格子 | `validate_t1_prepare_config` | 四档 op + n=500 + mod=23；op=7 拒绝。 |
| X-sci | scientific prepare | `main(["prepare", "--eval-mode","scientific", "--split-fractions", …, "--sham-opportunities","1"])` | exit 0。6 条轨迹均 `parse_status=ok`、每条 ≥1 事件（实际各 3：`p1`/`p2`/`q`）。sham 3 条观测。见细项。 |
| X-fallback | 空 `event_id` 回退 | 全标签 `event_id=""` 且 `noise_ref=1.0` | **仍把真实前提写入 N**：`rho_S_noise=1`，`excess=0`。生产 prepare 有 `node_id` 时不走此支。 |

**X-18 细项（独立，不信任 `test_b14`）：**

- 夹具（有 `original_id=gsm8k-12`）：`base_group_id=gsm_plus:gsm8k-12`，`shared_gsm_family=gsm8k-12`，`fit_eligible=False`，`metadata.role=test`，`kind=placeholder`。`split_for_task` / 裸 `assign_split(base_group_id)` 均为 `test`。`refuse_fit_split(..., "probe_train")` 拒绝。
- 仅官方字段（无 `original_id`/`id`）：`shared_gsm_family=unmapped:ada has 4 apples and buys 3 more. how many apples?`，`base_group_id=gsm_plus:` + 该串，划分仍 `test`。
- `gsm_family_id` 优先含 `gsm8k` 的 `original_id`/`id_orig`/`seed_id`/`gsm8k_id`；否则 `unmapped:` + 规范化 `seed_question`。**没有 seed 文本 → GSM8K ID 的匹配。**

**X-19 细项（B5-01 独立复验）：**

- `split_for_task` **确实**读取 `metadata.shared_gsm_family`，缺省回退 `base_group_id`。作者「消费方存在」属实。
- 同题夹具：Symbolic `base_group_id=shared_gsm_family=gsm8k-12`；Plus `shared_gsm_family=gsm8k-12` 但 `base_group_id=gsm_plus:gsm8k-12`。两边 `split_for_task` 碰巧都是 `test`（Plus 因 source 锁；Symbolic 因该哈希落在 test）。
- 换成 `original_id=gsm8k-1`：Plus `shared_gsm_family=gsm8k-1` 仍 **`test`**；Symbolic 同族键 **`probe_train`**。`assign_split("gsm8k-1")=="probe_train"`。
- 官方 Plus schema（无 `original_id`）：`shared_gsm_family` 与 Symbolic **不相等**。
- `assert_same_role` / `assign_family` 在 `src/` 无生产调用方。Plus 的 `source∈TEST_ONLY_SOURCES` 在哈希之前短路为 test，**不会**把同源 Symbolic 锁进同一角色。

**X-sci / 密度细项（独立复跑，不信任 `test_scientific_prepare_emits_parseable_events`）：**

- 轨迹：`trace-base`/`t0p`/`edit` + 两条 allowed value edit + `trace-sham`（seed=2）。文本为 tiny 解码 + 约束 `q = <digits>`，不是节点金标拼接。
- 事件非空：**成立**。`parse_events` 把题干里的 `p1 = 4`、`p2 = 0` 与生成的 `q = …` 都解析成事件。
- sham 有观测：**成立**。3 条，`scan_state=observed_response`。`p1`/`p2` 为 `no_change`；**`q` 为 `changed`（82 vs 53）**。
- sham `premise_id` 分别为 **`p1` / `p2` / `q`**（事件 `node_id`），不是空串。
- 标签：前提行事件 `task_known=False`；节点 `q` 的 `task_known=True`。sham 命中把 `q` 行 `noise_ref` 广播为 `1.0`。另有仅 sham 的 `(q,q)` 行，`task_label=0`（把节点 id 当成已知非祖先前提）。
- 密度（`mean_over_events`）：事件 `p1`/`p2` 的 `T=∅`（`ancestors` 只返回节点键），`S={p1}` / `{p2}`，`rho_S_raw=0.5`，`rho_S_noise=0.0`（空 N），`excess=0.5`。事件 `q` 的 `S` 分母为空，`M={p1,p2}`，`rho_M_raw=1.0`，`rho_M_noise=1.0`（空 N ⇒ `|T−N|/|T|=1`），`excess_M=0`。**聚合 `rho_S_excess=0.5` 完全来自把题干前提行当推理事件。** 见 B6-01。
- sham 命中未把 `p1`/`p2` 写入密度 `N`（`rho_S_noise=0` 而非 1）。B5-04 原触发在主路径关闭。命中被当成已评估 0，见 B6-02。

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 B5-01 已在夹具与官方字段子集确认 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b`。见 U-01 |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | 本机 tiny 解码不是科学噪声协议；机制（空 N、前提行事件）已在夹具+tiny 上确认 |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。下表针对 **round-01–05 原 ID**。作者本轮主张关闭 B5-02 / B5-03 / B5-04 / B5-01。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | — | **closed** | X-03 |
| B-02 | — | **closed** | X-04 |
| B-03 | — | **closed**（行为袋） / **residual**（身份字段） | X-06；CLI sham 现写 `node_id`（X-21 / X-sci）。见 B6-02。 |
| B-04 删除 / 异 node_id | — | **closed** | X-07 / X-08b |
| B-05 `scanned=True` | — | **closed** | X-07 |
| B-06 / B-25 | — | **closed** | X-09 |
| B-07 | — | **closed** | X-10 |
| B-08 | — | **closed** | X-11 |
| B-09 / B-24 | — | **closed** | X-12 / X-13。Plus 域见 B5-02（本轮关）。 |
| B-10 | — | **closed** | X-14 |
| B-11 | — | **closed** | X-15 |
| B-12 0-hit | — | **closed** | X-23 / X-12e 0-hit |
| B-13 | — | **closed** | X-17 |
| B-14 | — | **closed** | X-18 |
| B-15 / **B5-01** | closed locally（`split_for_task` 消费 `shared_gsm_family`） | **residual（仍 confirmed）** | X-19。消费方存在不等于共组。 |
| B-16 Edit 口述 valid | — | **closed** | X-20 Edit.validity |
| **B5-03** Hotpot status | closed locally | **closed** | X-20：`new_answer="Spain"` 时 `status=requires_independent_truth`。值仍写入（与 MuSiQue 相同，不单独升格）。 |
| B-17 | — | **closed** | X-he-rho |
| B-18 / **B5-05** | remain partial | **residual（仍 confirmed）** | X-25 |
| B-19 | — | **closed** | X-26 |
| B-20 | — | **closed** | X-20g |
| B-21 | — | **closed** | X-21p |
| B-22 | — | **closed** | X-22 |
| B-23 | — | **closed** | X-05 / X-21b |
| B-26 | — | **closed** | X-23 |
| B-27 | — | **closed** | X-24 |
| **B5-02** Plus 子串 | closed locally | **closed** | X-plus-sub |
| **B5-04** sham 命中写入 N | closed locally | **closed**（主路径） / **residual**（回退支 + 命中语义） | X-12e 主路径空 N；X-fallback 仍旧；X-sci 命中当 0。见 B6-02。 |

## 6. 发现（本轮开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B5-01 跨数据集 GSM 族键仍不共组（原 B-15；作者声称已关）

- **状态：** confirmed defect（机制）/ pending_server（真实 dump 碰撞率）
- **严重度：** high
- **符号：** `splits.split_for_task`；`splits.gsm_family_id`；`t2_gsm_plus.load_gsm_plus`；`t2_gsm_symbolic.family_id`
- **行号：** `splits.py` 12–22, 33–41, 71–80；`t2_gsm_plus.py` 20–46；`t2_gsm_symbolic.py` 12–13, 47, 63
- **协议：** DATA-03 / FEATURES T2：以规范化 `seed_question` **连接 GSM8K ID**；不同数据集同源题同族。GOAL §5.5：同基础题、同源题、全部变体共组；Plus 测试专用不得参与拟合，**但不能把同源 Symbolic 放进 `probe_train` 再拿 Plus 当未见题**。
- **证据：**
  1. X-19：`split_for_task` 现读取 `shared_gsm_family`。作者关闭主张的字面部分成立。
  2. 官方 Plus 字段只有 `question/solution/answer/perturbation_type/seed_*`。此时族键为 `unmapped:<seed_question>`，与 Symbolic 的 `gsm8k-*` **不相等**。无 seed→GSM8K 匹配。
  3. 同族键 `gsm8k-1`：Plus 因 `source=gsm_plus` 锁 `test`；Symbolic 按 `sha256(seed:family)` 得 `probe_train`。`assert_same_role` 无生产调用方。
  4. 作者 `test_plus_and_symbolic_share_gsm8k_family` 只断言夹具 metadata 相等，并允许 Plus `base_group_id` 带前缀。不测官方字段、不测 `gsm8k-1` 跨集角色。
- **影响：** 消费字段不能代替共组。服务器 dump 到达后，官方 Plus 仍无法与 Symbolic 共族；有 `original_id` 的派生快照也会一边拟合、一边当未见测试。
- **建议：** 规范化 seed 文本匹配 GSM8K ID；失败则 `unmapped` + 显式状态。同一族键必须得到同一角色；Plus 的 test-only 约束应把整族锁到 test，而不是只锁 Plus 行。

---

### B5-05 来源—数值对仍是表面改名（原 B-18；作者未声称本轮关闭）

- **状态：** confirmed defect
- **严重度：** medium
- **符号：** `edits.make_source_value_pair` / `apply_source_value_edit`；`events.review_export`
- **行号：** `edits.py` 151–234；`events.py` 220–235；`cli.py` 321
- **协议：** DATA-01 / FEATURES 来源—数值：同图族来源 A/B，先 `a=b` 再 `a≠b`；MEAS-01：可导出**与回填**人工复核。
- **证据：**
  1. X-25：`same_source_diff_value` 是普通值编辑；`same_value_diff_source` 是 `p1→p1_src` **表面改名**。表达式仍 `p1 * p2`，图上没有第二个来源节点。
  2. CLI prepare 写 `review_export.jsonl`，`review` 恒 `None`。全包无回填 / merge 入口。
- **影响：** C2 所需的同值异源图对无法从数据层按协议生成。ISSUES 已标 partial；独立审查同意仍未关。

---

### B6-01 scientific 把题干前提行当成推理事件并写入 ρ

- **状态：** confirmed defect
- **严重度：** high
- **符号：** `events.parse_events`；`graphs.ancestors`；`measure.event_density_sets`；`cli.cmd_prepare` scientific 支
- **行号：** `events.py` 75–89；`graphs.py` 7–22；`measure.py` 281–322；`cli.py` 278–366
- **协议：** MEAS-02 / 协议 §2：`R_task` 是输入前提到**任务节点**的祖先。S/M 描述推理步的虚假/缺失依赖，不是「题干里的前提赋值句是否被改写」。GOAL §5.3：任务依赖与经验行为分开。
- **证据：**
  1. X-sci：tiny scientific prepare 每条轨迹 3 个事件 `p1`/`p2`/`q`。`p1`/`p2` 来自题干 `p1 = 4` / `p2 = 0`，不是模型推理步。
  2. `ancestors` 只返回节点键。`event_density_sets` 对 `event_id=p1` 取 `T=∅`。编辑 `p1` 使该「事件」值变化 → `B={p1}` → `S={p1}`，`ρ_S raw=0.5`。
  3. 目标事件 `q` 的 S 分母为空（`P=T={p1,p2}`），不贡献 `ρ_S`。聚合 `rho_S_excess=0.5` **全部来自前提行事件**。
  4. fixture prepare 走 `parse_fixture_events`（只解析节点），同题看不到这条。scientific 与 fixture 测量对象不一致。
  5. 作者测试只断言「事件非空且含 `q`」，不检查事件清单是否混入前提、不检查密度分母。
- **影响：** 本机 scientific 入口会写出看起来像 C3 信号的 `ρ_S`，其实是「改了题干数字后题干那一行变了」。真实权重到达后同一解析/密度管线仍会复现。
- **建议：** 密度只对任务节点事件取平均；或 `parse_events` 的前提行不进入 `event_density_sets`。题干前提变化应记为编辑对齐，不记为 S。

---

### B6-02 sham 把真实前提/节点写入 `premise_id`，命中按已评估 0 入账

- **状态：** confirmed defect
- **严重度：** medium
- **符号：** `cli.cmd_prepare` sham 观测；`measure.event_density_sets`；`measure.build_labels`
- **行号：** `cli.py` 298–319, 329–350；`measure.py` 68–78, 288–320
- **协议：** 协议 §2.6 / GOAL §5.4：噪声参照必须对应明确且匹配的比较机会；**不能给无编辑随机变化强加具体前提身份**。已扫描 0-hit 是参照 0，不是 missing。命中若不能指认前提，应保持事件级 0/1 或单独噪声袋，而不是假装 0。
- **证据：**
  1. X-12e：主路径 `event_density_sets` 在 `observed` 时固定 `noise_set=[]`，`hits` 变量未使用。sham 命中不再把真实前提写入 N。**B5-04 原触发关闭。**
  2. X-sci：sham `q` 实际 `changed`（82 vs 53），但事件 `p1`/`p2` 的 `rho_S_noise=0`。事件 `q` 的 `rho_M_noise=1`（空 N ⇒ `|T−N|/|T|=1`），把 M 的 excess 抹成 0。命中与 0-hit 在 S 上无法区分。
  3. 观测字段：fixture sham `premise_id="q"`；scientific sham `premise_id∈{p1,p2,q}`。作者测试显式要求 `premise_id` 非空。这与「不把随机变化钉到前提身份」冲突。事件身份已在 `node_id` / `event_pair` / `alignment_ref`。
  4. X-fallback：当全部 `event_id` 为空时，回退支仍执行 `noise_set=[premise_id for noise_ref==1.0]`，复现旧的 excess=0。生产 prepare 当前不走此支。
- **影响：** 主路径不再用虚假依赖列吞掉 C3。但 scientific 已出现的真实 sham 命中被记成噪声 0，且观测行带着 `p1`/`p2`。空 N 对 M 的噪声公式是 1 不是 0，符号不对称。
- **建议：** sham 的 `premise_id` 保持空；噪声用事件级 0/1。空 list + `noise_evaluated` 只表示已观察 0。命中单独入账，且 M 的噪声定义与 S 对齐。删除或同样改写空 `event_id` 回退支。

## 7. 已独立关闭的原触发（非本轮缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01 | X-03 | — |
| B-02 | X-04 | — |
| B-03 行为袋 | X-06 | B6-02 身份字段 |
| B-04 / B-05 | X-07 / X-08b | — |
| B-06 / B-25 | X-09 | U-03 |
| B-07 | X-10 | — |
| B-08 | X-11 | — |
| B-09 / B-24 | X-12 / X-13 | — |
| B-10 | X-14 | — |
| B-11 | X-15 | X-16 |
| B-12 0-hit | X-23 / X-12e | B6-02 |
| B-13 / B-14 | X-17 / X-18 | B5-01 |
| B-16 Edit / **B5-03** | X-20 | 口述值仍写入，status 已诚实 |
| B-17 | X-he-rho | S 列表可含 `spec`，分母 null |
| B-19 / B-20 / B-21 | X-26 / X-20g / X-21p | pending_server 真实 dump |
| B-22 / B-23 / B-26 / B-27 | X-22 / X-05 / X-23 / X-24 | — |
| **B5-02** | X-plus-sub | — |
| **B5-04** 主路径 N | X-12e 空 N | B6-02；X-fallback |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径缺协议 → null | `measure.py` 124–135 | 不否定 B6-02。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | fixture 拒 official；官方拒仅有 G。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | 中间节点不进列索引。不否定 B6-01（节点键缺失导致前提事件 T=∅）。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 325–333 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` 36–37 | 不否定 B5-01。 |
| ND-07 | Hotpot supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 34–38 | `single_premise_claim=False`。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | |
| ND-09 | HumanEval 默认不宿主 exec | `scoring.py`；`executor.py` | `get_executor()` → Unavailable。Child process 诚实标 `isolated_sandbox=False`，不冒称沙箱。Linux cgroup 仍 pending_server。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` | `official_noop_release=False`；无图不写 proven。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 238–244 | |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` 原语 | `splits.py` 83–101 | 原语正确；不否定 B5-01（无人跨集调用）。 |
| ND-13 | T1 配置拒绝非白皮书格子 | `t1_config.py` | X-t1cfg。 |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 59–60 | |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05/X-21b。 |
| ND-16 | 官方加载对照 template 重算 | `t1_official.py` 77–80 | |
| ND-17 | 策略分岔 `scanned=False` | `events.py` 185–193 | STRUCT-01 分类器仍未实现，但不构成静默假阴性。 |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `measure.py` 285 | 原 B-17 假前提列不进分母。 |
| ND-19 | 已观察 0-hit 记 S 噪声 0 | `measure.py` 130–141, 294–296 | 关闭 B5-04 原触发。 |
| ND-20 | HE Spec `valid` 仅 `tests_passed` | `t3_humaneval.py` 44–67 | CLI 不传 child executor。隔离执行器仍 pending_server。 |
| ND-21 | Plus/T4/Hotpot/MuSiQue Edit 缺核验不写 valid | 各 apply* | Hotpot/Plus 口述保持 `requires_independent_truth`。 |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 124–134 | |
| ND-23 | MuSiQue answerable 配对保留 | `t3_musique.py` 43–68 | |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | 协议 §6 / DECIDE-01 | **不是缺陷。** |
| ND-25 | Plus 孤立替换与 T1 共用 `_replace_isolated_value` | `t2_gsm_plus.py` 50–55 | 关闭 B5-02。 |
| ND-26 | scientific 拒 0 事件 | `cli.py` 291–292 | 关闭「无事件则无 sham」的原触发；不否定 B6-01。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；tiny 命中不能当协议命中率 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 | 机制层 B5-01 已确认；dump 上匹配率 pending |
| S-07 | Linux cgroup / 容器隔离执行器 | EXEC-01 / GOAL §5.15 | 本机仅 Unavailable + 非沙箱子进程 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod` | FEATURES 称官方 Num 为加减乘；夹具无除法。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official` | 可解释为题源。需协议裁定。 |
| U-03 | `surface_mentions` 只匹配 `premise_id` / alias 词 | 未在真实题干别名上抽样。 |
| U-04 | 后续 stage 是否用 `task_id` 而不是族键做划分 | CLI fit 只信 `--split` 旗标。prepare 写 `splits.jsonl` 但不被 fit 读取。 |
| U-05 | 前提 span 同时含孤立整数与小数时整数编辑被拒 | 当前 fail-closed。 |
| U-06 | `assign_family` 不传 `fit_eligible` | Plus 生产走 `split_for_task` / source 锁。 |
| U-07 | `distinguishing_tests=True` 仅因 `new_tests` 非空 | 与 `validity=needs_truth` 并存。未见评分消费该旗标。 |
| U-08 | `event_density_sets` 把 `behavior_label!=1`（含 unknown）当作不在 B，从而进入 M | 协议「未知不作负标签」。scientific 事件 `q` 的 `M={p1,p2}`、`rho_M_raw=1` 可能部分来自 unknown 而非已知漏检。未在无 scientific 混入的纯节点袋上单独做对照，暂不升格。 |
| U-09 | `apply_spec_edit` 不检查 `isolated_sandbox` | 唯一能把 `valid` 写成真的本机后端是 child process。CLI 默认不走该路径；隔离器 pending_server。 |

## 11. 测试质量对本通道的含义

**136 passed ≠ 数据/测量正确。** 作者本轮补了 Plus 孤立 token、Hotpot status、`split_for_task` 读族键、scientific 非空事件、空 N 的 `event_density_sets`。独立复现同意 **B5-02 / B5-03 / B5-04 主路径** 可关。缺口仍在：

- `test_plus_and_symbolic_share_gsm8k_family` 只用带 `original_id` 的夹具，不测官方 Plus 字段，不测 `gsm8k-1` 上 Plus=`test` vs Symbolic=`probe_train`。
- `test_scientific_prepare_emits_parseable_events` 只查「有事件、有 `q`、sham `premise_id` 非空」。不查事件是否含题干前提，不查 `ρ` 分母，不查 sham 命中是否当 0。
- `test_plus_numeric_edit_is_isolated_token` / `test_hotpot_spoken_answer_stays_unverified` 锁住了本轮已关项；不能外推 B5-01 / B6-01。
- `test_source_value_pair_has_both_conditions` 仍只查 metadata 旗标。
- `test_evaluated_zero_hit_sham_is_zero_noise_not_null` 不测 sham **命中** 的事件级入账，也不测空 `event_id` 回退支。

因此不能把 ISSUES 中的 B5-01 标为已关闭。B5-02 / B5-03 / B5-04（主路径）可独立关闭。B5-05 作者也未主张关闭。

## 12. 通道结论

数据与测量通道 **不能** 在本冻结对象上给出通过意见。**FAIL。**

1. **`HASH_MATCH`：** 声明冻结 hash 已按 VERSION 配方复现（59 文件）；结论绑定上表逐文件 digest。全量 pytest **136 passed**，与作者计数一致，不是验收。
2. **本轮可独立关闭的作者主张：** **B5-02**（Plus `13` 中的 `3` 走孤立 token，改成 `9 more` 而不是 `19`）、**B5-03**（Hotpot 口述答案保持 `requires_independent_truth`）、**B5-04 主路径**（`event_density_sets` 命中不再把真实前提写入 `N`）。先前已关且仍关：B-01/02/04/05/06/07/08/09/10/11/12-0-hit/13/14/16-Edit/17/19/20/21/22/23/24/26/27。
3. **仍确认的机制缺陷：**
   - **B5-01 / B-15（high）：** `split_for_task` 虽读取 `shared_gsm_family`，官方 Plus 仍 `unmapped:`；同源 `gsm8k-1` 上 Plus=`test`、Symbolic=`probe_train`。消费字段 ≠ 共组。
   - **B6-01（high）：** scientific prepare 事件非空、sham 有观测（作者这两点成立），但题干前提行进入事件袋且 `T=∅`，写出 `ρ_S_excess=0.5` 的假 C3 信号。
   - **B6-02（medium）：** sham 观测写入 `p1`/`p2`/`q`；命中按空 N（S 噪声 0、M 噪声 1）入账。空 `event_id` 回退支仍会复现旧 N 污染。
   - **B5-05（medium）：** 来源—数值对仍是改名+值编辑；复核无回填。
4. 集合密度 raw/null/signed、T1 来源隔离、官方 dump 对照重算、有限扫描 unknown、身份不含值、HE placeholder 过滤、Plus 孤立替换、Hotpot status、Gate 未注册仍成立（ND-01–ND-26），不能抵消划分共组与 scientific 密度缺口。官方全量保持 `pending_server`。即使服务器数据到达，**B5-01 仍会把官方 Plus 与 Symbolic 拆成两族**，**B6-01 仍会在 scientific 解析管线上把题干前提写进 ρ**。
