# Review B — 数据与测量（独立审查，round-13）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-13 通道报告。round-01–10 `B-data.md` 只用作待复验清单与行文格式，不作为证据。点名 CE 全部用独立 oracle 复跑，不调用作者 `test_*` 断言。审查过程中对 `.planning/research/.cache/gsm_test_only_families.json` 做了隔离清空/写锁，结束后已恢复开审内容 `["gsm8k-12", "q:ada has 4 apples…"]`。

**开审冻结核验：`HASH_MATCH`。交卷：`HASH_MISMATCH`。** 按 `.planning/audits/round-13/VERSION.md` 原文脚本（POSIX relpath + `\x00` + 文件字节）独立复得 `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（61 文件，0 CRLF），与声明一致。成文前最后一次复算 `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`。相对开审已变：`cli.py`（1254→1249，`_find_tasks_jsonl` 不再向上 4 层）、`tests/test_round07_regressions.py`（224→256）。**本通道焦点** `splits.py` / `edits.py` / `measure.py` / `events.py` / 全部 `tasks/*.py` / `graphs.py` / `schema.py` **与开审同 digest**。prepare/label 正文与开审逐行一致。**结论绑定开审冻结焦点字节**；交卷 `cli.py` 查找补丁不得记为冻结已闭。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-13） |
| review_time | `2026-09-21T02:34:00+08:00`（复算 hash / 开读）— `2026-09-21T03:25:00+08:00`（成文） |
| declared_frozen_hash | `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（`.planning/audits/round-13/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。61 文件，0 CRLF。配方与 VERSION 一致。 |
| 交卷复算 | **`HASH_MISMATCH`** `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`。`cli.py` `175abf12…`→`779cedd3…`（1254→1249）；`test_round07_regressions.py` `1ffdbd7e…`→`68f32ca3…`（224→256）。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件；oracle 在 `%TEMP%`，不写入 `src/` / `tests/`） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5 / §5.15；`FEATURES.md` T1–T4 与 `seed_question`→GSM8K ID；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02、T2NOOP-01、STRUCT-01、SURF-01 |
| pytest_author_claim | VERSION 写 156 passed。本通道未把作者测试当证据，未用全量绿关闭任何 CE。 |

相对 r10 开审树：`splits.py`（152→184，新增磁盘锁）、`measure.py`（已是不广播版 `b15fb8a5…`）、`cli.py` / 若干测试已变。`edits.py` / `events.py` / 全部 `tasks/*.py` / `graphs.py` / `schema.py` 与 r10 交卷后同 digest。夹具字节与 r06–r10 相同。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度调用链而通读；`fixture` = 对照适配器读完。行数/SHA-256 为 **开审 HASH_MATCH** 冻结树，除非另注。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 392 | `b15fb8a5bb92220f5693b01acf6b60bd6640b57449e6419cb0e7b2bc6e4b6ba6` | full 1–392 | 仅 `sham:` 行写 `noise_ref`；`sham_hits` 先于 `real_hits`；空 `event_id` 回退 |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`review_export` / `merge_review`；等计数 `node_id` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `{}` |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf` | full 1–287 | `apply_rename_edit` 改写 id/parents/expression；`make_source_value_pair` |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | `gsm_text_key`；RAM ∪ `.planning/research/.cache/gsm_test_only_families.json`；`siblings=` |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | 身份、`scan_state`、placeholder/spec |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full | 默认 unavailable；child `isolated_sandbox=False` |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full | 域内评分；默认不宿主 exec |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | `t3_musique` / `t4_boundary` 别名；不补图 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `register_test_only_family` 写 RAM∪磁盘；`requires_independent_truth` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 写 `shared_gsm_text`；不自己注册锁 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 注入后祖先、`noop_proof` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | 口述答案保持 `requires_independent_truth` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值；`graph_kind=composition_reference` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder；Spec `valid` 仅 `tests_passed` |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式、整题 placeholder |
| `src/reasoning_diff/cli.py` | 1254 | `175abf12f4c207c551c6f5c5910b002d62f7f9125f41226389d0acbde4083c17` | callsite 94–436, 550–574, 676–716, 1156–1174 | prepare/label；`sham:`；`split_for_task` 不传 `siblings`；无 `merge_review` 命令。交卷 1249/`779cedd3…` 只改 `_find_tasks_jsonl` |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844` | callsite 72–192 | 只解析 `generated=gen_text+assigned` |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169, 215–257 | P2 整数分母；Gate 未注册 → `scientific_conclusion=None` |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087d67a58d56e4f5d9ad7085a3300d591a372f806bb938ab7b3` | callsite | **不作为本通道证据** |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a33933f5d6cba276745e191cbb22b13d13a8faf19af8d86b01` | callsite | |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb555851beeaa193e39e3e221759af4c986df8a05d3bdb8e7702666` | callsite | |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae440d6c939c210674070ca7bf80ee6c3cb2644d7b04c515a2` | callsite | |
| `tests/test_round06_regressions.py` | 145 | `ac7e4e88248ff49edcd6f992cf48ff88409172c34ce7fa934ca288816fdf946c` | callsite | |
| `tests/test_round07_regressions.py` | 224 | `1ffdbd7ef5803fb6533564da4f2004f117229e3f41ea6630a861e9580b6c4033` | callsite | 开审字节。交卷已改，**不信任** |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c` | full | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | full | |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003bf134d1ef9d6c06206a7b836e15c69cd1126bc1ae6d482123` | full | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 r06–r10 相同，未改字节）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

未列入主表但开审纳入聚合的文件：`__init__.py` / `__main__.py` / `artifacts.py` / `baselines.py` / `interventions.py` / `io.py` / `rng.py` / `repair.py` / `transfer.py` / `models/*` / `probes/*` / 其余测试。本通道不把它们当数据正确性证据。

## 3. 已执行检查

独立 oracle（`%TEMP%\r13_b_oracle.py`，不写入 `src/` / `tests/` / `pyproject.toml`）。先 `clear_test_only_families()` 隔离，用独立 JSON（非仓库夹具）构造 `gsm8k-1`。`splits.py` / `edits.py` / `measure.py` / `events.py` / 全部 `tasks/*.py` 在开审与交卷间 **digest 未变**，这些 CE 绑定冻结。CLI prepare/label 正文未变；T3/scientific 调用链可绑冻结。

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审 **HASH_MATCH** 61 文件 `0816fa5b…`，0 CRLF。交卷 **HASH_MISMATCH** `1f61fd06…`。 |
| X-00 | 作者 pytest 主张 | 未跑全量绿当证据 | VERSION「156 passed」**不是**本通道关闭依据。 |
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
| X-19 | 跨集族键 + **A10-04 persist**（B5-01） | 独立 `gsm8k-1` JSON；RAM clear；新进程 | **点名 CE 通过。** 见 §3.1。 |
| X-20 | T3 编辑 / 组成图（B-16 / B5-03） | `document_edit` + `new_answer="Spain"` / `paragraph_edit` / `ancestors` | Hotpot / MuSiQue 口述 `needs_truth` + `requires_independent_truth`。`ancestors(musique/hotpot/plus/he)=={}`。节点值已清空。 |
| X-21 | CLI fixture prepare + sham（B-12） | `main(["prepare", …, "--sham-opportunities","1"])` | exit 0。`premise_id="sham:q"`。p1/p2 的 `noise_ref=None`。`edits.jsonl` 含 `kind=source_value_pair`，表达式 `p1 * p2_src`。`review_export=awaiting_human`。fixture 同文 sham 为 **miss**（`noise_ref=0.0`）→ 已评估空 N，见 §3.3。 |
| X-21p | Plus 八类扰动（B-21） | 独立喂官方类名 | `critical thinking` / `missing information` → `insufficient_information`。`reversing operation` → `perturbation_status=query_target_change`。其余六类 `(None, None)`。 |
| X-22 | P2 分母（B-22） | `p2_paired(..., 99)` ± `shared_premises` | 只传 99 → `denominator_unverified`。99 vs `["p1"]` → `denominator_inconsistent`。一致时 `ok`，`delta_rho≈0.1`。 |
| X-22n | 多节点祖先 | 内存 s=p1+p2、t=s+p1 | `anc[t]={p1,p2}`。 |
| X-23 | 空 `noise_set` ± `noise_evaluated`（B-26） | 集合密度 API | 未评估空集 → `noise_set_empty`。已评估空集且 `P=T` → `rho_S_*` 分母空为 None，`rho_M_noise=1.0`。 |
| X-12e | 0-hit / 缺失 / 命中 | t1+p3 标签 | **0-hit（`noise_ref=0`，p3∈P\\T）：** `rho_S_noise=0.0`，excess=0。**显式 `p3` `noise_ref=1`：** `rho_S_noise=1.0`，excess=−1，**未丢、未记空 0**。**仅 `sham:q` 命中：** 事件级 `null_reason=noise_set_missing`。 |
| X-24 | 多匹配行 / 非法 scan_state（B-27） | `"q = 0 q = 1\\n"`；非法枚举 | 两条 `ambiguous`。非法 scan_state 抛 `ValueError`。 |
| X-25 | 改名 / 来源—数值 / 复核（B-18 / **B5-05**） | `make_source_value_pair(t1_tiny, "p2", "2")`；`review_export`+`merge_review` | **点名 CE 通过。** 见 §3.2。 |
| X-26 | 官方夹具重算（B-19） | 夹具 9；fixture 加载器 | answer=9。fixture 加载器拒 official 形状。 |
| X-27 | 除法模运算 | `_eval_expr("5 / 2", {}, 23)` | `2`（`int(truediv)%mod`）。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-plus-sub | Plus 孤立数字（B5-02） | 题干 `Ada has 13 apples and buys 3 more…`，`old="3"` | 变成 `…buys 9 more…`，保留 13。`validity=needs_truth`，`status=requires_independent_truth`。子串 `1` 拒。 |
| X-he-rho | HumanEval 进 ρ（B-17） | `kind=placeholder` + `event_density_sets` | `denominator_S=None`，`rho_S_raw=None`。S 列表仍可出现 `spec`。 |
| X-he-exec | Spec 裁判（B-16 HE） | 无解 / Unavailable / ChildProcess | 无解与不可用均为 `needs_truth`。`ChildProcessExecutor` 且测试通过 → `valid`；`isolated_sandbox=False`。默认 `UnavailableExecutor`。 |
| X-label | CLI label | `main(["label", "--in-dir", fixture_prepare])` | exit 0。密度与 fixture prepare 一致（sham miss → 已评估空 N）。 |
| X-msq | MuSiQue 配对 id | 夹具两条 | `msq-9::answerable` / `msq-9::unanswerable`，同 `base_group_id`。 |
| X-t4 | T4 四态 | `load_t4` | 四态齐全；前提均为 placeholder。 |
| X-t1cfg | T1 格子 | `validate_t1_prepare_config` | 四档 op + n=500 + mod=23；op=7 拒绝。 |
| X-cat | catalog 别名 | `load_snapshot("t3_musique")` / `t4_boundary` | 可加载。 |
| X-gate | Gate 0–2 | `week8_decision({})` 与带 `rho_S_excess=0.5` | 三门均为 `unregistered`；`scientific_conclusion=None`。**不是缺陷。** |
| X-t3prep | T3 prepare（E7-19） | `main(["prepare","--kind","hotpot",…])` 与 `--kind t3_musique` | **两者 exit 0。** 无 `source_value_pair`。`_try_source_value_pair` 对 hotpot/musique/plus/HE 返回 None，对 t1 非空。 |
| X-sci | scientific prepare | `main(["prepare", "--eval-mode","scientific", "--split-fractions", …, "--sham-opportunities","1"])` | exit 0。7 条轨迹均 `parse_region=generated`、仅事件 `q`。sham `premise_id=sham:q`，`changed` 82 vs 53。p1/p2 `noise_ref=None`。事件级 `null_reason=noise_set_missing`，`rho_M_excess=None`。 |
| X-b601 | 生成区事件（B6-01） | 上条 traces | 事件仅 `q`。原触发保持关闭。 |
| X-fallback | 空 `event_id` 回退 | 全标签 `event_id=""` 且 `noise_ref=1.0` 的 p1/p2 | 走 fallback；映射前提写入 N；`rho_M_noise=0`。生产 label 行有 `event_id`。见 U-13。 |
| X-svp-skip | T3 跳过 SVP | `_try_source_value_pair` | hotpot/musique/HE/plus 为 None；t1 非空。 |

### 3.1 B5-01 / A10-04 persist 独立复验（不信任作者测试）

构造独立 JSON（非仓库夹具）。每步前 `clear_test_only_families()`，除非该步正在测残留锁。`assign_split("gsm8k-1")=="probe_train"`（独立哈希）。

1. **Plus `original_id=gsm8k-1` 然后 Symbolic 同 id。** Plus：`shared_gsm_family=gsm8k-1`，`shared_gsm_text=q:ada has 4 apples…`，`split_for_task=test`。随后 Symbolic：同族键、同文本键，**`split_for_task=test`**。磁盘写成 `["gsm8k-1", "q:ada has 4 apples…"]`。点名条件 **成立**。
2. **官方 Plus 字段（无 `original_id`，有 `seed_question`）。** `gsm_family_id` 回退为 `gsm_text_key`。与 Symbolic `original_question` 规范化后 **文本键相等**。Plus 加载后 Symbolic **锁 `test`**。磁盘仅有文本键。点名条件 **成立**。
3. **`_TEST_ONLY_FAMILY_KEYS.clear()`（仅内存）。** RAM 变 `[]`，磁盘仍有文本键。`family_locked_test(...)==True`，Symbolic **仍 `test`**。点名条件 **成立**。
4. **`clear_test_only_families()` 后孤立 Symbolic（本进程无 Plus）。** 锁文件删除。`split_for_task=probe_train`，与 `assign_split("gsm8k-1")` 一致。作者主张「诚实」：**成立**。
5. **全新 Python 子进程。** 父进程 `load_gsm_plus` 写盘后，子进程 RAM `[]`，只加载 Symbolic：`SPLIT test`，`FAMILY gsm8k-1`。点名条件 **成立**。
6. **生产 CLI。** `prepare --kind gsm_plus` 后，新进程 `prepare --kind gsm_symbolic --sidecar …` 写出 `ROLE test`。夹具族 `gsm8k-12` 的 `assign_split` **本身就是 `test`**，因此夹具 CLI 不能单独证明 persist；**独立 `gsm8k-1` 子进程（上条）才是 persist 证据。**
7. **`siblings=`。** 清空后 `split_for_task(symbolic, siblings=[plus])=="test"`；无 siblings 为 `probe_train`。无关 Plus `gsm8k-99` **不**锁 `gsm8k-1`。
8. **FEATURES / DATA-03 残余：** 无 `seed_question`→GSM8K ID 对照表，也无「未解析」状态字段。官方 dump 文本若与 Symbolic `original_question` 规范化后不一致，文本键仍拆族。`assert_same_role` / `assign_family` 在 `src/` 无生产调用方。`cmd_prepare` 仍不传 `siblings=`；现由磁盘锁补齐「先 Plus、后新进程 Symbolic」。

**B5-01 / A10-04 persist 点名 CE：PASS。** r10 的 B5-01-prod（进程内 RAM、新进程 Symbolic `gsm8k-1`→`probe_train`）在本冻结上 **独立关闭**。从未登记 Plus 的孤立 Symbolic 进 `probe_train` **不是缺陷**（点名 CE 第 4 步）。无 seed→ID 表见 U-14 / S-06。

### 3.2 B5-05 独立复验

`make_source_value_pair(t1_tiny, "p2", "2")`：

- `same_value_diff_source.kind=same_value_diff_source`
- `premise_id`：`['p1','p2_src']`（不再保留 `p2`）
- `expression`：`p1 * p2_src`（**不是**表面改名残留 `p1 * p2`）
- `parents`：`['p1','p2_src']`
- 题干：`p1 = 4. p2_src = 0. What is q = p1 * p2_src?`
- 值侧 `same_source_diff_value` 重算答案 `8`；源侧答案仍 `0`

`review_export`：`review=None`、`review_status=awaiting_human`。`merge_review` 按 `record_id` 回填 `review` 并标 `filled`。CLI **没有** `merge_review` 子命令（`cli.py` 只写 export）。fixture prepare 的 `edits.jsonl` 含 `source_value_pair`，表达式同样是 `p1 * p2_src`。

图上仍只有节点 `q`、两个前提，**没有**协议级第二来源节点 A/B。

**B5-05 点名 CE（remap + awaiting/merge 库函数）：PASS。** 协议级 A/B 双来源图：仍未实现（U-12，不重开点名 CE）。

### 3.3 Sham / 噪声分母 / B9-01（点名 CE 3）

**格式：** CLI fixture 与 scientific 的 sham `premise_id` 均为 `sham:q`（`sham:<node>`）。**成立。**

**仅未映射 sham 命中**（`premise_id=sham:q`，`noise_ref=1`，无真实前提 `noise_ref`）：事件级 `null_reason=noise_set_missing`，`rho_*_excess=None`，不记已评估 0。**成立。** 事件均值顶层 **不复制** `null_reason`（`top_null_reason=None`），但 `rho_M_excess` 保持 None。见 U-15。

**映射真实前提 `p3∈P`、`noise_ref=1`：** `rho_S_noise=1.0`（`P\\T={p3}`），excess=−1，`null_reason=None`。不是空集 0，也不是丢弃。**成立。**

**0-hit 且 `p3∈P\\T`、标签 `noise_ref=0`：** `rho_S_noise=0.0`，excess=0。

**B9-01 不广播：** `build_labels` 在 sham `changed` 时只给 `sham:` 行写 `noise_ref=1.0`，p1/p2 为 `None`。scientific prepare（82 vs 53）：`sci_noise={'p2': None, 'p1': None, 'sham:q': 1.0}`，事件级 `noise_set_missing`，**`rho_M_excess=None`**。与 r10 冻结树上的广播+`rho_M_excess=1.0` **相反**。本冻结 `measure.py` 开审即为此版。

**fixture sham miss：** 合成轨迹与 base 同文 → `outcome=no_change`，`sham:q` 的 `noise_ref=0.0`，p2 仍为 `None`（不广播）。`event_density_sets` 见「已观察、无 `noise_ref==1`」→ 已评估空 N → `rho_M_noise=1.0`，`rho_M_excess=-0.5`。这是 **未映射 miss 记成已评估空集**，不是把 sham 身份写进真实前提。与「命中→missing / miss→N=∅」可读一致，不升格为 B9-01。见 ND-31。

**点名 CE 3：PASS**（格式 + 未映射命中 missing + 映射 p3 入 N + 不广播）。

### 3.4 T3 prepare（E7-19）

`--kind hotpot` → exit 0，`edits.kind=['document']`，无 SVP，无 `failure.json`。  
`--kind t3_musique` → exit 0，`edits.kind=['paragraph']`，无 SVP。  
`_try_source_value_pair` 跳过 placeholder / paragraph / T3 / `composition_reference`。  
**作者主张 E7-19 关闭：独立确认。**

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 B5-01 已在独立 JSON 上跑 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b`。见 U-01 |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | 本机 tiny 解码不是科学噪声协议 |
| N-08 | 开审冻结树上的干净全量 pytest | 不把绿测试当论文正确性；交卷测试已漂 |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## / B6-## / A10-04 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。下表针对 **round-01–10 原 ID**。作者本轮主张关闭 A10-04 / B9-01 / B5-01/05。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | — | **closed** | X-03 |
| B-02 | — | **closed** | X-04 |
| B-03 | — | **closed**（行为袋 + `sham:` 前缀） | X-21 / X-sci |
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
| B-15 / **B5-01** / **A10-04** | persist 锁：仅清 RAM 后仍 test；新进程仍 test；孤立可 probe_train | **closed** | X-19 / §3.1 |
| B-16 Edit 口述 valid | — | **closed** | X-20 |
| **B5-03** Hotpot status | — | **closed** | X-20：`new_answer="Spain"` 时 `status=requires_independent_truth` |
| B-17 | — | **closed** | X-he-rho |
| B-18 / **B5-05** | rename 改写 id/表达式；`merge_review` 可回填 | **closed** | X-25 / §3.2。A/B 双来源图见 U-12 |
| B-19 | — | **closed** | X-26 |
| B-20 | — | **closed** | X-20 `ancestors=={}` |
| B-21 | — | **closed** | X-21p |
| B-22 | — | **closed** | X-22 |
| B-23 | — | **closed** | X-05 |
| B-26 | — | **closed** | X-23 |
| B-27 | — | **closed** | X-24 |
| **B5-02** Plus 子串 | — | **closed** | X-plus-sub |
| **B5-04** / **B6-02** / **B9-01** | sham 不广播；未映射命中 missing；映射入 N | **closed** | §3.3 / X-sci / X-12e |
| **B6-01** 题干前提当生成事件 | — | **closed**（原触发） | X-sci。见 U-10 |
| **B5-01-prod**（r10） | 新进程 Symbolic 仍 probe_train | **closed** | X-19f 子进程 RAM 空仍 test |
| E7-19 T3 prepare | 不再强制 SVP/recompute | **closed** | X-t3prep |

## 6. 发现（本轮开放）

本轮在声明冻结的数据/测量焦点上 **没有新的 confirmed defect**。r10 的 B6-02-freeze / B5-01-prod 在 `0816fa5b…` 上被独立证伪为已修。下列不升格。

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

（空。开放项见 §10 / §9。）

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| B-01–B-14, B-16, B-17, B-19–B-27 | X-03…X-26 等 | U-14 seed→ID |
| **B5-02** | X-plus-sub | — |
| **B5-03** | X-20 | 口述值仍写入，status 已诚实 |
| **B5-01 / A10-04 persist** | §3.1 | 无 seed→ID 表；锁文件在 `.planning` |
| **B5-05 点名 CE** | §3.2 | U-12 A/B 图；CLI 无 merge 命令 |
| **B9-01 / B6-02** | §3.3 / X-sci | U-13 fallback；U-15 顶层 null_reason |
| **B6-01** | X-sci | U-10 |
| **E7-19** | X-t3prep | 无 sidecar 的 Symbolic prepare 仍失败（非 T3） |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径缺协议 → null | `measure.py` 124–135 | 与 B9-01 关闭一致。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | fixture 拒 official；官方拒仅有 G。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | 中间节点不进列索引。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-05 | 联合编辑挡住 soundness | `measure.py` 375–383 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` | |
| ND-07 | Hotpot supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 34–38 | `single_premise_claim=False`。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16 | |
| ND-09 | HumanEval 默认不宿主 exec | `scoring.py`；`executor.py` | `get_executor()` → Unavailable。Child 标 `isolated_sandbox=False`。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` | `official_noop_release=False`；无图不写 proven。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 251–257 | |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` 原语 | `splits.py` 156–184 | 原语正确；生产未跨集调用。 |
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
| ND-27 | `_e_premise_ids` 跟 `task.premises` 序且跳过 `sham:` | `cli.py` 703–712 | sham 身份不进拟合列。 |
| ND-28 | 约束 `\nq = <digit>` 是 tiny 可解析接口 | `generate.py` | 不是 §4.1 自然 CoT。 |
| ND-29 | `_try_source_value_pair` 跳过 T3 | `cli.py` 676–689 | 关闭 E7-19。 |
| ND-30 | 磁盘 ∪ RAM 锁在 **被调用时** 正确 | `splits.py` 69–78, 127–153 | 关闭 A10-04。孤立无 Plus 进 `probe_train` 是诚实。 |
| ND-31 | fixture sham miss → 已评估空 N | `measure.py` 338–349；`cli.py` 339–341 | 同文合成轨迹必然 no_change。不广播。与 scientific 命中→missing 可并存。 |
| ND-32 | 夹具 `gsm8k-12` 的 `assign_split` 已是 `test` | `splits.assign_split` | 不能用夹具 CLI 单独证明 persist；`gsm8k-1` 才是 probe_train。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；tiny 命中不能当协议命中率 |
| S-05 | 官方表达式算子集 | DATA-01 | 见 U-01 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 / FEATURES T2 | 文本键机制已测；dump 上格式差仍会拆族 |
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
| U-11 | tiny scientific 上约束数字不随前提编辑变化 | X-sci：base/edit 均可为与编辑无关的数字。属 tiny 接口。 |
| U-12 | `same_value_diff_source` 仍是同图改名，不是第二来源节点 | 点名 CE 只要求 remap id/expression/parents，已满足。FEATURES 来源 A/B 图仍未构造。不重开 B5-05。 |
| U-13 | 空 `event_id` fallback 仍把 `noise_ref=1` 的真实前提写入 N | 生产 label 行有 `event_id`。X-fallback：`rho_M_noise=0`。不并入已关闭的 B9-01。 |
| U-14 | 无 `seed_question`→GSM8K ID 表，也无 FEATURES 要求的未解析状态 | 官方无 `original_id` 时族键=文本键。点名 CE 只要求共享文本键，已满足。dump 匹配率 pending_server。 |
| U-15 | 事件均值顶层省略 `null_reason` | scientific/库 API 顶层 `null_reason=None`，事件行有 `noise_set_missing`。`rho_*_excess` 仍为 None，不会写出伪造 excess。 |
| U-16 | persist 路径写死为仓库 `.planning/research/.cache/` | 可复查、跨进程有效。安装到 site-packages 或删掉 `.planning` 会丢锁。未在本机安装布局上测。 |
| U-17 | 并行 prepare 同时读写锁 JSON | 无文件锁。未复现危害。 |

## 11. 测试质量对本通道的含义

**156 passed ≠ 数据/测量正确。** 作者本轮主张 persist 锁与 sham 不广播。独立 oracle 同意二者在 **开审冻结焦点文件** 上成立。作者测试仍不能替代：

- persist 必须自己构造 `gsm8k-1`（夹具 `gsm8k-12` 的哈希角色已是 `test`）。
- 必须测「只清 RAM」「全新子进程 RAM 为空」「`clear_test_only_families` 后诚实 `probe_train`」。
- B5-05 必须查 `expression`/`parents`，不能只查 kind。
- B9-01 必须查 p1/p2 的 `noise_ref is None` 以及 scientific 命中后的 `rho_M_excess is None`。
- 交卷后加长的 `test_round07_regressions.py` 绑定漂后测试树，不能回写冻结关闭。

## 12. 通道结论

数据与测量通道在声明冻结 `0816fa5b…` 的焦点文件上给出通过意见。**PASS。**

1. **开审 `HASH_MATCH`（61 文件，0 CRLF）。交卷 `HASH_MISMATCH`（`1f61fd06…`）。** 结论只绑开审 digest。交卷仅 `cli.py`（`_find_tasks_jsonl`，A12-03，非 prepare/label）与 `test_round07_regressions.py` 漂离。`splits.py` / `measure.py` / `edits.py` / `events.py` / 全部 `tasks/*.py` 未变。
2. **点名 CE（独立 oracle，不信作者测试）：**
   - **B5-01 / A10-04 persist：PASS。** Plus `gsm8k-1`→Symbolic 同为 `test`；官方无 `original_id` 的 `q:` 文本键与 Symbolic `original_question` 共享并锁 test；仅清 RAM 后仍 test（磁盘）；`clear_test_only_families()` 后孤立 Symbolic 为 `probe_train`（诚实）；全新子进程 RAM 空仍 test。
   - **B5-05：PASS。** `same_value_diff_source` 重写 `premise_id`/`parents`/`expression` 为 `p2_src` / `p1 * p2_src`；`review_export` 为 `awaiting_human`；`merge_review` 按 `record_id` 回填。
   - **Sham / B9-01：PASS。** `sham:<node>`；未映射命中 `noise_set_missing`；映射 `p3` 入 N（非空 0、非丢弃）；scientific 不广播，`rho_M_excess=None`。
   - **Hotpot/MuSiQue 口述 `needs_truth` / `requires_independent_truth`，`ancestors(musique)=={}`：PASS。**
   - **Plus 孤立数字 token；HE placeholder 不进 ρ 分母：PASS。**
   - **T3 `prepare --kind hotpot` 与 `t3_musique` exit 0：PASS。**
3. **r10 残留：** B5-01-prod 与 B6-02-freeze / B9-01 在本冻结上 **独立关闭**。无新的 confirmed defect。
4. 集合密度 raw/null/signed、T1 来源隔离、官方 dump 对照重算、有限扫描 unknown、身份不含值、HE placeholder 过滤、Plus 孤立替换、Hotpot/MuSiQue/Plus 真值旗标、T3 prepare、Gate 未注册仍成立（ND-01–ND-32）。官方全量保持 `pending_server`。Gate 0–2 未注册与 `scientific_conclusion=None` **不是缺陷。** 从未加载 Plus 的孤立 Symbolic 进 `probe_train` **不是缺陷。** FEATURES 的 seed→ID 表与未解析状态仍缺（U-14 / S-06），不推翻点名 CE。连续通过计数是否开始取决于整树冻结是否被其他通道或交卷漂文件否决；**本通道不因交卷 `cli.py` 查找改动重开数据 CE。**
