# Review B — 数据与测量（独立审查，round-10）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-10 通道报告。round-01–08 `B-data.md` 只用作待复验清单与行文格式，不作为证据。点名 CE 全部用独立 oracle 复跑，不调用作者 `test_*` 断言。

**开审冻结核验：`HASH_MATCH`。交卷：`HASH_MISMATCH`。** 按 `.planning/audits/round-10/VERSION.md` 原文脚本（POSIX relpath + `\x00` + 文件字节）独立复得 `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`（61 文件，0 CRLF），与声明一致。审查中途磁盘连续漂离：中段复算 `7518e20b…`；成文前最后一次 `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`。相对开审已变：`measure.py`、`cli.py`（1251→1254）、`tests/test_review_regressions.py`、`tests/test_round07_regressions.py`。`splits.py` / `edits.py` / `events.py` / 全部 `tasks/*.py` 仍与开审同 digest。**结论绑定开审冻结字节**；事后补丁不得记为冻结已闭。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-10） |
| review_time | `2026-09-21T02:21:00+08:00`（复算 hash / 开读）— `2026-09-21T03:10:00+08:00`（成文） |
| declared_frozen_hash | `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`（`.planning/audits/round-10/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`。61 文件。配方与 VERSION 一致。 |
| 交卷复算 | **`HASH_MISMATCH`** 最后一次 `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（中段曾为 `7518e20b…`）。`measure.py` `c81e2402…`→`b15fb8a5…`（388→392）；`cli.py` `ba474e1f…`→`175abf12…`（1251→1254）；`test_review_regressions.py` `d3814498…`→`c1f02364…`（397→399）；`test_round07_regressions.py` `cad435ad…`→`a59c236d…`（169→221）。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5 / §5.15；`FEATURES.md` T1–T4 与来源—数值合同；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02、T2NOOP-01、STRUCT-01、SURF-01、DECIDE-01 |
| pytest_author_claim | VERSION 写 153 passed。本通道未在未漂冻结树上拿到干净全量绿。混树一次 **154 passed / 1 failed**（`test_b03` `None == 1.0`）。交卷树 **155 passed**。绿测试不是论文正确性。 |

相对 r08：`splits.py` / `edits.py` / `events.py` / `t2_gsm_plus.py` / `t2_gsm_symbolic.py` / `measure.py` / `cli.py` 已变。`graphs.py` / `schema.py` / `t1_*` / `t2_noop.py` / `t3_*` / `t4_boundary.py` / `scoring.py` / `executor.py` / `analysis.py` 与 r08 同 digest。夹具字节与 r08 相同。范围内新增 `tests/test_round07_regressions.py`（60→61）。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度调用链而通读；`fixture` = 对照适配器读完。行数/SHA-256 为 **开审 HASH_MATCH** 冻结树。交卷后 `measure.py` 与两份测试已改，见 §1。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 388 | `c81e2402671228b6ac8b42437b9d48b2ef1834f41b82275c2975114dab1063d6` | full 1–388 | 标签、S/M、`real_hits`→N、空 `event_id` 回退、TO/CSP；**冻结广播 `noise_ref` 到全部同行** |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`review_export` / `merge_review`；等计数 `node_id` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | 祖先只返回节点键；`composition_reference` / `supporting_facts_only` / `none` → `{}` |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf` | full 1–287 | `apply_rename_edit` 改写 id/parents/expression；`make_source_value_pair` |
| `src/reasoning_diff/splits.py` | 152 | `08f77e972927a9961885c09e0538f0c43d47ca6638944e1c80465cf6cc4af066` | full 1–152 | `gsm_text_key`；进程内 `_TEST_ONLY_FAMILY_KEYS`；`siblings=` |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | 身份、`scan_state`、placeholder/spec、`Edit.exhaustive` |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full | 默认 unavailable；child `isolated_sandbox=False` |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full | 域内评分；默认不宿主 exec |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | `t3_musique` / `t4_boundary` 别名；不补图 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `register_test_only_family`；孤立替换；`requires_independent_truth` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | sidecar、公式编辑、`shared_gsm_text` |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 注入后祖先、`noop_proof` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | 口述答案保持 `requires_independent_truth` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder；Spec `valid` 仅 `tests_passed` |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式、整题 placeholder |
| `src/reasoning_diff/cli.py` | 1251 | `ba474e1fea1f7c5ab3488c90b32c776862d3651f281be38a543522e9ebeb5e98` | callsite 94–436, 550–574, 674–716, 1156–1174 | prepare/label；`sham:` 前缀；`_try_source_value_pair` 跳过 T3；**`split_for_task` 不传 `siblings`**；无 `merge_review` 命令 |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844` | callsite 72–192 | 只解析 `generated=gen_text+assigned` |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169, 215–257 | P2 整数分母；Gate 未注册 → `scientific_conclusion=None` |
| `tests/test_review_regressions.py` | 397 | `d3814498fe52b28b7905dc2c07e86e8e893b285081e4c37724a67c0f61b164ee` | full | 冻结期望 sham 广播 `noise_ref=1.0`；**不作为本通道证据** |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a33933f5d6cba276745e191cbb22b13d13a8faf19af8d86b01` | callsite | 非本通道主证据 |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb555851beeaa193e39e3e221759af4c986df8a05d3bdb8e7702666` | callsite | |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae440d6c939c210674070ca7bf80ee6c3cb2644d7b04c515a2` | callsite | `sham:` 前缀 |
| `tests/test_round06_regressions.py` | 145 | `ac7e4e88248ff49edcd6f992cf48ff88409172c34ce7fa934ca288816fdf946c` | callsite | |
| `tests/test_round07_regressions.py` | 169 | `cad435add5103d94bb6d660ca6599d42f5f650c152d142b4e38c5dc284ee860e` | callsite | 作者补丁；**不信任** |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c` | full | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003bf134d1ef9d6c06206a7b836e15c69cd1126bc1ae6d482123` | full | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 r06/r08 相同，未改字节）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

未列入主表但开审纳入聚合的文件：`__init__.py` / `__main__.py` / `artifacts.py` / `baselines.py` / `interventions.py` / `io.py` / `rng.py` / `repair.py` / `transfer.py` / `models/*` / `probes/*` / 其余测试。本通道不把它们当数据正确性证据。

## 3. 已执行检查

独立 oracle（临时脚本，不写入 `src/` / `tests/` / `pyproject.toml`）。`splits.py` / `edits.py` / `events.py` / `cli.py` / 全部 `tasks/*.py` 在开审与交卷间 **digest 未变**，这些 CE 绑定冻结。`measure.py` 在第一次 pytest 前已漂；密度/噪声条同时给出 **冻结源码重建** 与 **交卷运行值**。

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审 **HASH_MATCH** 61 文件 `81308124…`。交卷 **HASH_MISMATCH** `7518e20b…`。 |
| X-00 | 作者 pytest 主张 | `python -m pytest tests -q --tb=line` | 混树 **154 passed / 1 failed**（`test_b03`）。交卷树 **155 passed / 26.38s / exit 0**。VERSION「153 passed」**未独立成立**。绿 ≠ 正确。 |
| X-03 | 矩阵 `noise=None`（B-01） | `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `null_reason=noise_missing`，S.noise/excess 均为 None。保持关闭。 |
| X-04 | 有限扫描 `no_response_observed_in_scan`（B-02） | 仅 `outcome=no_change` + 该 scan_state | `behavior_label=None`，`behavior_known=False`。保持关闭。 |
| X-05 | `observed_response` + `no_change` ± `exhaustive`（B-23） | 同上两旗标 | 无 `exhaustive` → unknown；`exhaustive=True` → `behavior_label=0`。保持关闭。 |
| X-07 | 删除后对齐（B-04） | 两版 `q` vs 一版 | `pairs=[]`；`merged` 非空；`scanned=False`；`strategy_detector=status_field_only`。 |
| X-08 | 等计数同 `node_id` | 值 1/2 vs 9/2 | 配成 `(1,9),(2,2)`，双方 `node_id=q`。身份键不含 value。 |
| X-08b | 等计数不同 `node_id` | 左 `q`、右 `r` | `pairs=[]`，记 ambiguous。 |
| X-09 | R_surf vs 图父母（B-06/B-25） | 裸赋值 / 值后提及 / 赋值前 | 父母 `['p1','p2']`；裸 surface `[]`；值后与赋值前均为 `['p1']`。 |
| X-11 | 公式编辑（B-08） | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，a=5，answer=8。 |
| X-12 | 数值子串（B-09） | `"has 13 apples"`、值 `"3"` | `ValueError: not a unique isolated token`。 |
| X-13 | 小数 3.5/5 与 5.5（B-24） | `_replace_isolated_value` | `3.5`→`9` 成功。`5` 对 `5.5` 抛错。 |
| X-14 | no-op 证明（B-10） | 前端注入；有图 / 无图 | 缺独立判断拒绝。T1：`ancestors(q)={p1,p2}`，`noop_proof=recompute_and_ancestors`。Plus 无图：`unknown_without_graph`。 |
| X-15 | CSP 空父母 + unknown（B-11） | `task_parents=[]`，`graph_status=unknown` | `csp=None`，`clean_matched=0`。 |
| X-16 | CSP 空父母 + complete | 同上但 `complete` | `csp=1.0`，`clean_matched=1`。 |
| X-17 | `assign_family`（B-13） | 缺 id；同 id 不同成员 | 缺 id 抛错。同 `family_id` 角色相同。 |
| X-18 | GSM-Plus 生产划分（B-14） | 夹具 / `refuse_fit_split` | `fit_eligible=False`，`split_for_task=test`，`kind=placeholder`。`refuse_fit_split(..., "probe_train")` 拒绝。 |
| X-19 | 跨集族键（B-15 / **B5-01**） | 独立构造 `gsm8k-1` / 官方字段 / `siblings=` | **点名 CE 通过；生产 CLI 仍不共组。** 见 §4。 |
| X-20 | T3 编辑 / 组成图（B-16 / B5-03） | `document_edit` + `new_answer="Spain"` / `paragraph_edit` / `ancestors` | Hotpot / MuSiQue 口述 `needs_truth` + `requires_independent_truth`。`ancestors(musique/hotpot/plus/he)=={}`。节点值已清空。 |
| X-21 | CLI fixture prepare + sham（B-12） | `main(["prepare", …, "--sham-opportunities","1"])` | exit 0。`premise_id="sham:q"`，fixture 路径 `no_change`。`edits.jsonl` 含 `kind=source_value_pair`。`review_export.review_status=awaiting_human`。 |
| X-21p | Plus 八类扰动（B-21） | 独立喂官方类名 | `critical thinking` / `missing information` → `insufficient_information`。`reversing operation` → `perturbation_status=query_target_change`。其余六类 `(None, None)`。 |
| X-22 | P2 分母（B-22） | `p2_paired(..., 99)` ± `shared_premises` | 只传 99 → `denominator_unverified`。99 vs `["p1"]` → `denominator_inconsistent`。一致时 `ok`，`delta_rho=0.1`。 |
| X-22n | 多节点祖先 | 内存 s=p1+p2、t=s+p1 | `anc[t]={p1,p2}`。 |
| X-23 | 空 `noise_set` ± `noise_evaluated`（B-26） | 集合密度 API | 未评估空集 → `noise_set_empty`。已评估空集 → `rho_S_noise=0.0`。 |
| X-12e | 0-hit / 缺失 / 命中 | t1+p3 标签 | **0-hit（p3∈P\\T）：** `rho_S_noise=0.0`，excess=0。**显式 `p3` `noise_ref=1`：** `rho_S_noise=1.0`，excess=−1，**未丢、未记空 0**。**仅 `sham:q` 命中：** `null_reason=noise_set_missing`。 |
| X-24 | 多匹配行 / 非法 scan_state（B-27） | `"q = 0 q = 1\\n"`；非法枚举 | 两条 `ambiguous`。非法 scan_state 抛 `ValueError`。 |
| X-25 | 改名 / 来源—数值 / 复核（B-18 / **B5-05**） | `make_source_value_pair(t1_tiny, "p2", "2")`；`review_export`+`merge_review` | **点名 CE 通过。** 见 §4。 |
| X-26 | 官方夹具重算（B-19） | 夹具 9；fixture 加载器 | answer=9。fixture 加载器拒 official 形状。 |
| X-27 | 除法模运算 | `_eval_expr("5 / 2", {}, 23)` | `2`（`int(truediv)%mod`）。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-plus-sub | Plus 孤立数字（B5-02） | 题干 `Ada has 13 apples and buys 3 more…`，`old="3"` | 变成 `…buys 9 more…`，保留 13。`validity=needs_truth`，`status=requires_independent_truth`。子串 `1` 拒。保持关闭。 |
| X-he-rho | HumanEval 进 ρ（B-17） | `kind=placeholder` + `event_density_sets` | `denominator_S=None`，`rho_S_raw=None`。S 列表仍可出现 `spec`。 |
| X-he-exec | Spec 裁判（B-16 HE） | 无解 / Unavailable / ChildProcess | 无解与不可用均为 `needs_truth`。`ChildProcessExecutor` 且测试通过 → `valid`；`isolated_sandbox=False`。默认 `UnavailableExecutor`。 |
| X-label | CLI label | `main(["label", "--in-dir", fixture_prepare])` | exit 0，写出标签 + densities。 |
| X-msq | MuSiQue 配对 id | 夹具两条 | `msq-9::answerable` / `msq-9::unanswerable`，同 `base_group_id`。 |
| X-t4 | T4 四态 | `load_t4` | 四态齐全；前提均为 placeholder。 |
| X-t1cfg | T1 格子 | `validate_t1_prepare_config` | 四档 op + n=500 + mod=23；op=7 拒绝。 |
| X-cat | catalog 别名 | `load_snapshot("t3_musique")` / `t4_boundary` | 可加载。 |
| X-gate | Gate 0–2 | `week8_decision({})` 与带 `rho_S_excess=0.5` | 三门均为 `unregistered`；`scientific_conclusion=None`。**不是缺陷。** |
| X-t3prep | T3 prepare（E7-19） | `main(["prepare","--kind","hotpot",…])` 与 `--kind t3_musique` | **两者 exit 0。** 无 `source_value_pair`。`_try_source_value_pair` 对 hotpot/musique/plus/HE 返回 None，对 t1 非空。 |
| X-sci | scientific prepare | `main(["prepare", "--eval-mode","scientific", "--split-fractions", …, "--sham-opportunities","1"])` | exit 0。7 条轨迹均 `parse_region=generated`、仅事件 `q`。sham `premise_id=sham:q`，`changed` 82 vs 53。**密度解释见 SHAM。** |
| X-b601 | 生成区事件（B6-01） | 上条 traces + `parse_events` | 事件 `start=45 >= prompt` 量级；仅 `q`。原触发保持关闭。 |
| X-fallback | 空 `event_id` 回退 | 全标签 `event_id=""` 且 `noise_ref=1.0` 的 p1/p2 | 走 fallback；映射前提写入 N；`rho_M_noise=0`。空 event_id 仍能把真实前提记进 N。 |

### 3.1 B5-01 独立复验（不信任作者测试）

构造独立 JSON（非仓库夹具），`clear_test_only_families()` 隔离寄存器。

1. **Plus `original_id=gsm8k-1` 然后 Symbolic 同 id。** Plus：`shared_gsm_family=gsm8k-1`，`shared_gsm_text=q:ada has 4 apples…`，`base_group_id=gsm_plus:gsm8k-1`，`fit_eligible=False`，`split_for_task=test`。随后加载的 Symbolic：`shared_gsm_family=gsm8k-1`，同文本键，**`split_for_task=test`**。点名条件 **成立**。
2. **官方 Plus 字段（无 `original_id`，有 `seed_question`）。** `gsm_family_id` 回退为 `gsm_text_key` = `q:`+`canonical_value(seed_question)`。与 Symbolic `original_question` 规范化后 **文本键相等**。Plus 加载后 Symbolic **锁 `test`**。点名条件 **成立**。
3. **`siblings=` 显式队列。** `clear_test_only_families()` 后，`split_for_task(symbolic, siblings=[plus_official])=="test"`；无 siblings 为 `probe_train`。无关 Plus（`gsm8k-99`）**不**锁 `gsm8k-1`。点名条件 **成立**。
4. **孤立 Symbolic `gsm8k-1`（新进程，未加载 Plus）。** `split_for_task=assign_split=probe_train`。`cmd_prepare` 第 261 行调用 `split_for_task(task, seed=…, fractions=…)`，**不传 `siblings`**。`register_test_only_family` 只在 `load_gsm_plus` 写入进程内 set，CLI 新进程看不到。生产「只 prepare Symbolic」仍把同源题放进 `probe_train`。
5. **FEATURES / DATA-03 残余：** 无 `seed_question`→GSM8K ID 对照表。官方 dump 文本若与 Symbolic `original_question` 规范化后不一致，文本键仍拆族。`assert_same_role` / `assign_family` 在 `src/` 无生产调用方。

**B5-01 点名 CE：PASS。生产共组：未闭（见发现 B5-01-prod）。**

### 3.2 B5-05 独立复验

`make_source_value_pair(t1_tiny, "p2", "2")`：

- `same_value_diff_source.kind=same_value_diff_source`
- `premise_id`：`['p1','p2_src']`（不再保留 `p2`）
- `expression`：`p1 * p2_src`（**不是**表面改名残留 `p1 * p2`）
- `parents`：`['p1','p2_src']`
- 题干：`p1 = 4. p2_src = 0. What is q = p1 * p2_src?`
- 值侧 `same_source_diff_value` 重算答案 `8`；源侧答案仍 `0`

`review_export`：全部 `review=None`、`review_status=awaiting_human`。`merge_review` 按 `record_id` 回填 `review` 并标 `filled`，未点名行保持 awaiting。CLI **没有** `merge_review` 子命令（`cli.py` 只写 export）。

图上仍只有节点 `q`、两个前提，**没有**协议要求的第二来源节点 A/B。落盘成立（X-21 `edits.jsonl` 含 `source_value_pair`）。

**B5-05 点名 CE（remap + awaiting/merge 库函数）：PASS。协议级 A/B 双来源图：仍未实现（U-12，不单独重开点名 CE）。**

### 3.3 Sham / 噪声分母（点名 CE 3）

**格式：** CLI fixture 与 scientific 的 sham `premise_id` 均为 `sham:q`（`sham:<node>`）。**成立。**

**仅未映射 sham 行（`premise_id=sham:q`, `noise_ref=1`，无真实前提命中）：** `null_reason=noise_set_missing`，不记已评估 0。**成立。**

**映射真实前提 `p3∈P`、`noise_ref=1`：** `rho_S_noise=1.0`（`P\\T={p3}`），excess=−1，`null_reason=None`。不是空集 0，也不是丢弃。**成立。**

**0-hit 且 `p3∈P\\T`：** `rho_S_noise=0.0`，excess=0。空分母的纯 T1（`P=T={p1,p2}`）上 `rho_S_*` 为 None 是分母空，不是 0-hit 记账错误。

**冻结树上的生产路径（开审 `measure.py` 原文，digest `c81e2402…`）：**

```
build_labels: 同事件任意 sham 命中 → 该事件全部 label 行 noise_ref=1.0
event_density_sets: real_hits = [h in P and not sham:] 优先于未映射 hits
```

scientific 轨迹（`generate.py` 未漂）sham 为 `changed` 82 vs 53。冻结逻辑会把 `(q,p1)`/`(q,p2)` 标成 `noise_ref=1.0`，于是 `real_hits=['p1','p2']`，`N={p1,p2}=T`。重建 `dependency_densities`：**`rho_M_raw=1.0`，`rho_M_noise=0.0`，`rho_M_excess=1.0`，`null_reason=None`**。这是把 **未映射 sham 命中记成已评估噪声并扣 M**，与作者「仅 sham:/未映射 hit 仍 `noise_set_missing`」直接相反。

交卷后的 `measure.py` 改为只给 `sham:` 行写 `noise_ref`，并先判断 `sham_hits` 再置 missing。交卷运行 X-sci：p1/p2 的 `noise_ref=None`，密度 `noise_set_missing`。**这是冻结外补丁，不能关闭冻结对象上的缺陷。**

**点名 CE 3 在声明冻结上：FAIL**（库级仅-sham / 显式 p3 两分支通过；CLI/scientific 广播+`real_hits` 优先把 sham 写成已评估 N）。

### 3.4 T3 prepare（E7-19）

`--kind hotpot` → exit 0，`edits.kind=['document']`，无 SVP，无 `failure.json`。  
`--kind t3_musique` → exit 0，`edits.kind=['paragraph']`，无 SVP。  
`_try_source_value_pair` 跳过 placeholder / paragraph / T3 / `composition_reference`。  
**作者主张 E7-19 关闭：独立确认。**

无 sidecar 的 Symbolic prepare 仍因「无可编辑非 placeholder 前提」抛错（本通道不把它算进 E7-19）。

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 B5-01 点名 CE 已在独立 JSON 上跑 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b`。见 U-01 |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | 本机 tiny 解码不是科学噪声协议 |
| N-08 | 开审冻结树上的干净全量 pytest | `measure.py` 在首次 pytest 前已漂；不能把 154/1 或 155 记成冻结 153 |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## / B6-## 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。下表针对 **round-01–06 原 ID**。作者本轮主张关闭 B5-01 / B5-05 / C7-M-01 vs B6-02 / E7-19。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | — | **closed** | X-03 |
| B-02 | — | **closed** | X-04 |
| B-03 | — | **closed**（行为袋 + `sham:` 前缀） | X-21 / X-sci；sham 不进行为袋 |
| B-04 / B-05 | — | **closed** | X-07 / X-08b |
| B-06 / B-25 | — | **closed** | X-09 |
| B-07 | — | **closed** | X-he-rho `base_group_id=HumanEval/0` |
| B-08 | — | **closed** | X-11 |
| B-09 / B-24 | — | **closed** | X-12 / X-13 |
| B-10 | — | **closed** | X-14 |
| B-11 | — | **closed** | X-15 / X-16 |
| B-12 0-hit | — | **closed** | X-12e 0-hit + p3 |
| B-13 | — | **closed** | X-17 |
| B-14 | — | **closed** | X-18 |
| B-15 / **B5-01** | `gsm_text_key` + register + siblings 共组 | **点名 CE closed**；**生产路径 residual** | X-19 / §3.1 / 发现 B5-01-prod |
| B-16 Edit 口述 valid | — | **closed** | X-20 |
| **B5-03** Hotpot status | — | **closed** | X-20：`new_answer="Spain"` 时 `status=requires_independent_truth` |
| B-17 | — | **closed** | X-he-rho |
| B-18 / **B5-05** | rename 改写 id/表达式；`merge_review` 可回填 | **点名 CE closed** | X-25 / §3.2。A/B 双来源图见 U-12 |
| B-19 | — | **closed** | X-26 |
| B-20 | — | **closed** | X-20 `ancestors=={}` |
| B-21 | — | **closed** | X-21p |
| B-22 | — | **closed** | X-22 |
| B-23 | — | **closed** | X-05 |
| B-26 | — | **closed** | X-23 |
| B-27 | — | **closed** | X-24 |
| **B5-02** Plus 子串 | — | **closed** | X-plus-sub |
| **B5-04** / **B6-02** / C7-M-01 | 映射真实前提入 N；sham 未映射 missing | **residual（冻结 confirmed）** | §3.3。库级两分支对；CLI/scientific 在冻结上写出 `rho_M_excess=1.0` |
| **B6-01** 题干前提当生成事件 | — | **closed**（原触发） | X-b601 / X-sci。见 U-10 |
| E7-19 T3 prepare | 不再强制 SVP/recompute | **closed** | X-t3prep |

## 6. 发现（本轮开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B6-02-freeze 冻结树上 sham 命中被记成已评估 N（C7-M-01 作者关闭不成立）

- **状态：** confirmed defect
- **严重度：** high / critical（会写出带符号的 ρ 而不是 null）
- **符号：** `measure.build_labels`；`measure.event_density_sets`；`cli.cmd_prepare` scientific sham
- **行号（开审冻结）：** `measure.py` 72–78（广播），328–345（`real_hits` 优先）；`cli.py` 308–330, 371–376
- **协议：** MEAS-02：噪声是配对随机流机会，不是把 sham 命中映射到真实前提列再扣 M。作者主张「仅 `sham:` / 未映射 hit 仍 `noise_set_missing`」。
- **证据：**
  1. 开审原文：同事件 sham `changed` → **所有** label 行 `noise_ref=1.0`（含 `p1`/`p2`）。
  2. 随后 `real_hits` 收集 `noise_ref==1` 且 `premise_id∈P` 的行，**优先于** sham 行，把 `{p1,p2}` 写入 N。
  3. 用未漂的 `generate.py` 轨迹（82 vs 53）重建 `dependency_densities`：`rho_M_excess=1.0`，`null_reason=None`。
  4. 仅 `sham:q` 行、或显式 `p3` 映射，在库 API 上行为符合主张。生产 prepare **不是**「仅 sham 行」。
- **影响：** scientific / fixture+命中 路径会把「答案无编辑却变了」记成对真实前提的噪声密度，而不是 missing。C3 的 excess 会被伪造。
- **建议：** 冻结对象必须先修广播或先判 `sham:` hits。交卷后的 `measure.py` 看起来在做这件事，**但不在声明冻结内**，本通道不关闭。

---

### B5-01-prod 生产 prepare 不共组同源 Symbolic

- **状态：** confirmed defect（机制：生产调用方）/ pending_server（真实 dump 碰撞率）
- **严重度：** high
- **符号：** `cli.cmd_prepare`；`splits.split_for_task`；`splits._TEST_ONLY_FAMILY_KEYS`
- **行号：** `cli.py` 261；`splits.py` 10, 35–46, 95–121
- **协议：** DATA-03 / FEATURES T2 / GOAL §5.5：同基础题、同源题、全部变体共组；Plus 测试专用不得把同源 Symbolic 放进拟合再拿 Plus 当未见题。
- **证据：**
  1. 点名 CE（同进程 Plus→Symbolic、官方文本键、`siblings=`）**通过**。
  2. 新进程孤立 Symbolic `gsm8k-1` → `probe_train`。`assign_split("gsm8k-1")=="probe_train"`。
  3. 生产 `prepare` 一次只加载一个 task，不传 `siblings`，也不读已落盘的 Plus 族锁。
  4. 寄存器是进程内 set，无持久化、无 `clear` 的生产调用。
- **影响：** 按 SERVER_RUNBOOK 分别 prepare Plus 与 Symbolic 时，B5-01 点名 API 通过也仍会一边拟合、一边当未见测试。
- **建议：** 划分阶段显式读入整族（Plus+Symbolic+变体）并传 `siblings=`，或把 test-only 族键写进可复查清单再消费。不要依赖「先 import Plus」。

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01–B-14, B-16, B-17, B-19–B-27 | X-03…X-26 等 | B5-01-prod |
| **B5-02** | X-plus-sub | — |
| **B5-03** | X-20 | 口述值仍写入，status 已诚实 |
| **B5-01 点名 CE** | §3.1 | B5-01-prod；无 seed→ID 表 |
| **B5-05 点名 CE** | §3.2 | U-12 A/B 图；CLI 无 merge 命令 |
| **B6-01** | X-b601 / X-sci | U-10 |
| **E7-19** | X-t3prep | 无 sidecar 的 Symbolic prepare 仍失败（非 T3） |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径缺协议 → null | `measure.py` 124–135 | 不否定 B6-02-freeze。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | fixture 拒 official；官方拒仅有 G。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | 中间节点不进列索引。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 371–380 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` | 不否定 B5-01-prod。 |
| ND-07 | Hotpot supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 34–38 | `single_premise_claim=False`。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | |
| ND-09 | HumanEval 默认不宿主 exec | `scoring.py`；`executor.py` | `get_executor()` → Unavailable。Child 标 `isolated_sandbox=False`。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` | `official_noop_release=False`；无图不写 proven。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 251–257 | |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` 原语 | `splits.py` 124–152 | 原语正确；生产未跨集调用。 |
| ND-13 | T1 配置拒绝非白皮书格子 | `t1_config.py` | X-t1cfg。 |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 59–60 | |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05。 |
| ND-16 | 官方加载对照 template 重算 | `t1_official.py` 77–80 | |
| ND-17 | 策略分岔 `scanned=False` | `events.py` 184–192 | STRUCT-01 分类器仍未实现，但不构成静默假阴性。 |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `event_density_sets` premises 过滤 | 原 B-17 假前提列不进分母。 |
| ND-20 | HE Spec `valid` 仅 `tests_passed` | `t3_humaneval.py` 44–67 | CLI 不传 child executor。 |
| ND-21 | Plus/T4/Hotpot/MuSiQue Edit 缺核验不写 valid | 各 apply* | 口述保持 `requires_independent_truth`。 |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 124–134 | |
| ND-23 | MuSiQue answerable 配对保留 | `t3_musique.py` 43–68 | |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | `analysis.py` 215–257 | **不是缺陷。** |
| ND-25 | Plus 孤立替换与 T1 共用 `_replace_isolated_value` | `t2_gsm_plus.py` 53–58 | 关闭 B5-02。 |
| ND-26 | scientific 拒 0 事件 | `cli.py` 296–297 | |
| ND-27 | `_e_premise_ids` 跟 `task.premises` 序且跳过 `sham:` | `cli.py` 707–716 | sham 身份不进拟合列。 |
| ND-28 | 约束 `\nq = <digit>` 是 tiny 可解析接口 | `generate.py` | 不是 §4.1 自然 CoT。 |
| ND-29 | `_try_source_value_pair` 跳过 T3 | `cli.py` 674–687 | 关闭 E7-19。 |
| ND-30 | `siblings=` 与文本键锁在 **被调用时** 正确 | `splits.py` 95–121 | 不否定 B5-01-prod。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；tiny 命中不能当协议命中率 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 | 文本键机制已测；dump 上格式差仍会拆族 |
| S-07 | Linux cgroup / 容器隔离执行器 | EXEC-01 / GOAL §5.15 | 本机仅 Unavailable + 非沙箱子进程 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod` | FEATURES 称官方 Num 为加减乘；夹具无除法。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official` | 可解释为题源。需协议裁定。 |
| U-03 | `surface_mentions` 只匹配 `premise_id` / alias 词 | 未在真实题干别名上抽样。 |
| U-04 | 后续 stage 是否用 `task_id` 而不是族键做划分 | CLI fit 只信 `--split` 旗标。prepare 写 `splits.jsonl` 但不被 fit 读取。 |
| U-05 | 前提 span 同时含孤立整数与小数时整数编辑被拒 | 当前 fail-closed。 |
| U-07 | `distinguishing_tests=True` 仅因 `new_tests` 非空 | 与 `validity=needs_truth` 并存。 |
| U-08 | `event_density_sets` 把 `behavior_label!=1`（含 unknown）当作不在 B，从而进入 M | 协议「未知不作负标签」。scientific 上 `M={p1,p2}`、`rho_M_raw=1` 来自 unknown。未升格。 |
| U-09 | `apply_spec_edit` 不检查 `isolated_sandbox` | 唯一能把 `valid` 写成真的本机后端是 child process。CLI 默认不走该路径。 |
| U-10 | `parse_events` 仍把非 placeholder 前提登记为可解析实体 | 生产 scientific 只把生成区送入解析器。若真实 CoT 复述 `p1 = 4`，仍可能以 `T=∅` 进入事件袋。暂不重开 B6-01。 |
| U-11 | tiny scientific 上约束数字不随前提编辑变化 | X-sci：base/edit 均可为 `q=82`，真实编辑 `behavior_label=None`。属 tiny 接口。 |
| U-12 | `same_value_diff_source` 仍是同图改名，不是第二来源节点 | 点名 CE 只要求 remap id/expression/parents，已满足。FEATURES 来源 A/B 图仍未构造。不重开 B5-05 点名。 |
| U-13 | 空 `event_id` fallback 仍把 `noise_ref=1` 的真实前提写入 N | 生产 label 行有 `event_id`。保留为回退支疑点，不并入 B6-02-freeze 主证据。 |

## 11. 测试质量对本通道的含义

**153/155 passed ≠ 数据/测量正确。** 作者本轮补了文本键、族寄存器、rename 重写、T3 SVP 跳过、映射噪声入 N。独立复现同意 **B5-01 点名 CE、B5-05 点名 CE、E7-19、B5-02、B5-03、口述真值旗标、HE 分母过滤** 可关。缺口：

- 冻结 `test_b03` 锁的是 **广播 `noise_ref=1.0`**，与 ISSUES「sham 不映射到真实前提」相反。作者测试不能为 C7-M-01 作证。
- `test_plus_and_symbolic_share_gsm8k_family` 类用例即使存在，也不测「新进程只 prepare Symbolic」。点名 CE 必须像本通道一样自己构造 `gsm8k-1` 与官方字段。
- `test_source_value_pair_*` 若只查 kind/旗标，不能代替表达式/parents 检查；本通道已独立查到 remap 成立。
- 交卷后新增的「不广播」测试绑定的是 **漂后** `measure.py`，不能回写冻结关闭。

因此不能把 C7-M-01 / B6-02 在 **声明冻结** 上标为已关闭。不能把 B5-01 的生产共组标为已关闭。

## 12. 通道结论

数据与测量通道 **不能** 在声明冻结 `81308124…` 上给出通过意见。**FAIL。**

1. **开审 `HASH_MATCH`（61 文件）。交卷 `HASH_MISMATCH`（最后一次 `598e6c8f…`）。** 结论只绑开审 digest。`measure.py`、`cli.py` 与两份测试在审查中被改写；事后补丁不是冻结关闭。
2. **点名 CE（独立 oracle，不信作者测试）：**
   - **B5-01：PASS**（Plus `gsm8k-1`→Symbolic 同为 `test`；官方无 `original_id` 的 `q:` 文本键与 Symbolic `original_question` 共享并锁 test；`siblings=` 显式队列锁 test，无关 Plus 不误锁）。
   - **B5-05：PASS**（`same_value_diff_source` 重写 `premise_id`/`parents`/`expression` 为 `p2_src` / `p1 * p2_src`；`review_export` 为 `awaiting_human`；`merge_review` 按 `record_id` 回填）。
   - **Sham 格式 + 库级未映射 missing + 映射 p3 入 N：库 API PASS。冻结生产路径 FAIL**（广播 + `real_hits` 优先 → `rho_M_excess=1.0`）。
   - **Hotpot/MuSiQue 口述 `needs_truth` / `requires_independent_truth`，`ancestors(musique)=={}`：PASS。**
   - **Plus 孤立数字 token；HE placeholder 不进 ρ 分母：PASS。**
   - **T3 `prepare --kind hotpot` 与 `t3_musique` exit 0：PASS**（E7-19 独立关闭）。
3. **仍确认的机制缺陷：**
   - **B6-02-freeze / C7-M-01（high）：** 声明冻结上 sham 命中会污染真实前提列并扣 M。作者关闭不成立。
   - **B5-01-prod（high）：** 点名 API 通过 ≠ DATA-03。生产 prepare 不传 `siblings`，新进程 Symbolic `gsm8k-1` 仍是 `probe_train`。
4. 集合密度 raw/null/signed、T1 来源隔离、官方 dump 对照重算、有限扫描 unknown、身份不含值、HE placeholder 过滤、Plus 孤立替换、Hotpot/MuSiQue/Plus 真值旗标、T3 prepare、Gate 未注册仍成立（ND-01–ND-30），不能抵消冻结噪声记账与生产划分缺口。官方全量保持 `pending_server`。Gate 0–2 未注册与 `scientific_conclusion=None` **不是缺陷。** 连续通过计数 **不能开始**。
