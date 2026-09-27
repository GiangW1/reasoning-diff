# F：验证质量与反向质疑（round-09）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-09 其他通道报告。`ISSUES.md` 只当作者主张。点名替身（donor 仍是 t0p、INLP 仍是 swap、`ie_z` 仍是隐状态均值、C6-M-01 标签序、`prefix_ids` 当 Prefill）在进程内攻击，未向仓库加测试。`python -m pytest -q` 绿不是论文正确性，也不是 Goal 验收。

**先行结论：** 开审时按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（60 文件）。本机对该树 `python -m pytest -q` 为 **144 passed / exit 0**。这不是 Goal 通过。五个点名替身里：科学路径 donor **不是** `trace-t0p`（实现闭；测试锁的是 `donor_kind` 字符串 + `prep/` 兄目录启发式）；INLP hook 是 `h@P` 不是 swap（实现闭；decode 与 swap/基线同 token，测试只锁 `inlp` 名）；tiny 路径 `ie_z` **不是**隐均值（实现半闭；`ie_z_g=target_follow` 是标签，`g(Y)` 恒 0）；**C6-M-01 未闭**（CLI fit 无 `tasks.jsonl` → labels 首次出现序 `['p2','p1']`，E 仍是 `['p1','p2']`）；`prefix_token_ids` 已拒（闭），`prefill_hidden=0`/`True`/`[0.0]` 仍 True。交卷前工作区已漂离声明冻结（文件数 60→61，聚合不再是 `9ffc4cd9…`）。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20` |
| 开审复算 | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20` |
| 开审裁决 | **HASH_MATCH**（60 文件，0 CRLF） |
| 交卷复算 | 磁盘已漂。出现 `tests/test_round07_regressions.py`（冻结外）。`cli.py` 1241→1251 行并新增 `_find_tasks_jsonl` / collect 复制 `tasks.jsonl`；`repair.py` 新增 `_hidden_is_prefill`。后一次全量脚本给出 **61** 文件、聚合 `599f3b9d180ea9328b93e6cc5b50de3884dd42867e57ccb499d434178b1dff40` ≠ 声明。 |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明/开审 **60**。交卷盘 **61**。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest（开审冻结树） | **144 passed in 18.87s，exit 0。** Collect：**144 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 范围 | 开审时全部 `tests/**`（17 个 `.py` + 10 个夹具 JSON）及测试触及的生产符号。交卷后新出现的 `tests/test_round07_regressions.py` **不在声明冻结内**，只抽查确认它是事后补丁，不作本冻结套件。 |
| 明确未读 | `.planning/audits/round-09/{A,B,C,D,E}-*.md` |

审查对象首先是**声明冻结字节**（开审复算一致后对该树跑 pytest 与五个点名攻击）。交卷时磁盘已变，**不能**把事后补丁写成冻结已闭。作者 `pytest_author_claim: 144 passed` 仅作为开审命令结果被独立确认。

## 2. 逐文件覆盖

以下行数/SHA-256 是 **开审 HASH_MATCH 时** 的 60 文件（冻结树）。交卷后若干文件已改，见 F9-00。

### 2.1 测试（冻结树全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍 `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 397 | `d3814498fe52b28b…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 291 | `5698a410c0669b61…` | r03 节点；P1 泄漏用例仍绿；`ie_z` 单元仍是隐均值 helper |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline 几何仍只 `!= pre_step`；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；仍不比 last-token |
| `tests/test_round06_regressions.py` | 145 | `6c274aa6d25a36f4…` | 相对 r08 加字段名：`donor_kind`/`inlp_transform`/`ie_z_g` 等；C6-M-01 仍只锁 helper；prefix_ids 拒 |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only（开审）：**144 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r08：节点数仍 144。`test_round06_regressions.py` 136→145 行，加强的是 **字段名**，不是新 CE。

### 2.2 生产相对测试（开审冻结）

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | r04 常数 δ 仍 `[0.5,0.5]`；泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | `attention_mean`/`rollout` 无数值 oracle |
| `cli.py` | 1241 | `a33cf79079089e1d…` | smoke offline；scientific prepare/collect/fit/intervene | **fit 不读 prepare 的 `tasks.jsonl`**（只看 collect/label）；`_load_source_value_pair` 靠兄目录名 `prep`/`prepare`/`s-prep`；`ie_z_g` 写死字符串 |
| `edits.py` | 277 | `bfd1632b50504c04…` | value/rename/source-value 元数据 | 同值异源是否真改源 |
| `events.py` | 260 | `fc5031a51e99a4b5…` | 身份；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；**`ie_z` helper 仍是均值差** | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 345 | `1fa2360e680d37ad…` | 事件均值；sham hit | `soundness_claim_allowed` 恒 False |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token；不比各 mode 的 generated_ids |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 201 | `07493570c6410e6b…` | `start>=len(prompt)` | 事件全是教员强制 `q=` |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` 未断言 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | **CLI calibrate 无反序 labels 测试** |
| `repair.py` | 223 | `d547ab99e3179093…` | `prefix_token_ids` / 空 hidden → False | **`prefill_hidden=0`/`[0.0]`/`True` → True** |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 111 | `35cd0e3f724ee850…` | Plus→test | `assert_disjoint` **零测试** |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | `card` 无 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 81 | `8e58c5d22b41b87b…` | family / 隔离 `13`≠`19` | `"reversing operation"` 仍非 T4 |
| `tasks/t2_gsm_symbolic.py` | 84 | `b50db6533f18948d…` | sidecar | — |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` 未断言 |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；口语 `needs_truth` | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 75 | `d31bcd499a51ca94…` | 4096/3584；形状 | `apply_map` 数值恢复未锁 |

夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `9ffc4cd9…1b3bf20`（60 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 交卷再算 | 同脚本 | **HASH_MISMATCH**。61 文件；聚合 `599f3b9d…1dff40`。`cli.py`/`repair.py`/`edits.py`/`measure.py`/`splits.py`/`transfer.py`/T2 与若干测试已改；新增 `tests/test_round07_regressions.py`。 |
| 全量 pytest | 开审时仓库根 `python -m pytest -q`（`pythonpath=src`） | **144 passed in 18.87s，exit 0**。无 skip/xfail/deselected。 |
| Collect | `python -m pytest tests --collect-only -q` | 144 nodes，collect exit 0（开审） |
| skip/xfail/`assert True` | 对当时 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]` | **存在的单元断言**与独立算术一致 |
| 对抗：donor 仍 t0p | scientific prepare/collect/intervene tiny | **该替身作为「donor 行是 t0p」不复现。** 兄目录名 `prep`：`donor_kind=same_source_diff_value`，行 `(0,2)` = `trace-base`/`trace-edit`。孤立目录名 `alpha`/`beta`：`_load_source_value_pair` 为 False（collect **不**写 `edits.jsonl`），回退 `same_identity_fallback`，行仍是 base/edit（跳过 t0p）。`finite_fallback` 在 base≈edit 时仍可配对 `(base, t0p)`。测试锁 `donor_kind` 字符串 + `prep/edits.jsonl` 元数据，**不锁** `event_rows[i].trace_id`。 |
| 对抗：INLP 仍 swap | `intervene_hidden_decode` 同 seed | hook 向量：`apply_swap` ≠ `h@P`（maxabs≈2.33）。**decode ids 三者相同** `[16,59,4,8]`，且等于 baseline。CLI：`inlp_transform=inlp`，`inlp_followed_donor=False`，main/crand/clayer/rescue **答案全是 `'9'`**。测试只锁名字。 |
| 对抗：`ie_z` 仍隐均值 | 同上 CLI | tiny：`ie_z=0.0`，`ie_z_g=target_follow`。donor 轨迹 `answer='82'`（教员强制 `\nq = 82`），hook decode `answer='9'`，`g_int=g_base=0`。`ie_z(H_donor,H_base)≈4.91e-5` **≠** CLI `ie_z`。helper `ie_z()` 与非 tiny 分支 **仍是均值差**。测试只锁 `ie_z_g`。 |
| 对抗：C6-M-01 | helper + 真实 `collect→label→fit`（冻结树） | helper+假 task：`['p1','p2','p3']`。**CLI：`col/tasks.jsonl` 与 `lab/tasks.jsonl` 都不存在。** labels 首次出现 `['p2','p1']`。`_e_premise_ids(None, labels)==['p2','p1']`。E 序 `['p1','p2']`，`E.shape=(2,32)`。本夹具两条 `task_label` 都是 1，Y 全 1，错序在数值上不可见。fit 只查 `U` 有限。 |
| 对抗：`prefix_ids` 当 Prefill | `run_repair` | `prefix_token_ids` → False。空 hidden / 仅旗标 → False。**`prefill_hidden=0` / `1` / `[0.0]` / `True` → True。** |
| 对抗：NaN H / last-token | scientific collect | `H` 全有限（本通道 7×32 或 6×32）。`pre_idx=44`，token 数 51，**不是**末 token。测试不比 last。 |
| 对抗：题干事件 | `generate_task_trace` | 事件只有 `q`，`start=45≥len(prompt)`。`parse_events(prompt)` 仍得 p1/p2。`parse_status=constrained_target`。 |
| 对抗：fixture 八阶段 | `--backend offline` | `H=[[1..8]]`；intervene `donor_missing`/`unexpressible`；analyze `p1 is None` / 结论空。 |
| 对抗：scientific analyze | labels → analyze | `p1 is None`。 |
| 对抗：bootstrap | 噪声数据；r04 `ρ=y` | 噪声有宽度（既有测试）。r04 仍 `[0.5,0.5]`。 |
| 对抗：verbalizer / span | gold=7；跨界 | `17`→0；`[1,3]`→`[]`。 |
| 对抗：账本 | 528 行 TR | `verification_method=python -m pytest -q`：**69**。`local_verify_status=passed_local_tests`：**320**。`executable_function` **159** 行均为 `tests_exist_not_acceptance`。页眉写不得用 pytest 关可执行行；协议行仍用 pytest 关闭。 |
| 事后抽查（非冻结） | 漂后 `_find_tasks_jsonl` / collect 复制 `tasks.jsonl` / `_hidden_is_prefill` | 作者在**另一哈希**上补 C6-M-01/标量 Prefill。这不能回写本冻结为已闭。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-09 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 对漂后 61 文件套件重跑 pytest 当冻结证据 | 那已不是声明 hash |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 144 passed | `VERSION.md` | **开审命令是。** 当作阶段/Goal 证据：**否。** 交卷磁盘已不是该冻结。 |
| 来源—数值 donor / INLP 与对照分 decode / `ie_z` 来自 target-follow \(g(Y)\) | `VERSION.md` prior；ISSUES D7-03/04/05 | **部分。** donor 行在科学 tiny 上不是 t0p。INLP hook 不是 swap。tiny `ie_z` 不是隐均值。测试锁的是 **名字**。`g(Y)` 恒 0。C6-M-01 CLI **未闭**。 |
| `truth_indices` / fit Y 跟 `task.premises` | ISSUES C6-M-01 | **测试锁 helper。冻结树生产 fit 走首次出现序。** |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 忽略不足以建 P1 的 labels。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham∉R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击失败 = 实现侧闭合（测试仍可能是替身）：**

- **donor 不是 t0p（科学 tiny 行身份）。** 有 `prep` 兄目录时走 `source_value_pair`；无元数据时 `same_identity_fallback` 仍跳过 `trace-t0p`。把 donor 钉死成 t0p 行，现科学路径会红——但现测试 **没锁 trace_id**。
- **INLP hook 不是 swap。** `mode=inlp` 做 `h@P`。把 INLP 函数改回 `apply_swap` 而仍写 `transform=inlp`，现测试仍绿。
- **tiny `ie_z` 不是 `mean(H)`。** CLI 用答案是否等于 `donor_ans`。把 CLI 改回 `ie_z(hidden, hidden)` 且保留 `ie_z_g=target_follow`，现测试仍绿。
- **`prefix_token_ids` 不是 Prefill。** 该半边有真 oracle。

### 6.2 无效、自指或过弱（含本轮点名替身）

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_truth_indices_follow_e_columns_not_label_order` | **C6-M-01 替身。** 自带 `task.premises`。不跑 `cmd_fit`。冻结树 collect/label **无** `tasks.jsonl`，fit 走 `task=None` → 首次出现序。本夹具 Y 全 1，错序不可见。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 donor/INLP/`ie_z` 半边 | 锁 `donor_kind==same_source_diff_value`（依赖 `tmp/.../prep/edits.jsonl` 启发式）、`inlp_transform==inlp`、`ie_z_g==target_follow`、`donor_rows[0]!=[1]`。不读 `event_rows` 的 `trace_id`，不比 generated_ids，不比 `ie_z` 与隐均值，不要求 `g` 非恒 0。 |
| `test_generated_events_*` 的 `parse_region == "generated"` | 硬编码元数据。`any(q)` 被教员强制 `\nq = 82` 单独满足。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 名不副实。锁 `isfinite` 与行数。末 token 有限 H 也会绿。 |
| `test_intervene_geometry_is_not_pre_step` | offline 单行 H → `unexpressible`。`!= pre_step` 旧替身还在。 |
| `test_dummy_execute_is_not_prefill` / `test_prefix_ids_alone_are_not_prefill` | 不锁 `prefill_hidden=0` / `[0.0]` / `True`（冻结实现）。 |
| `test_ie_z_and_rescue_controls` | 仍测 **隐均值 helper**，与作者声称的 `g(Y)` 相反。 |
| `test_p1_returns_bootstrap_interval` | 非空即可。r04 仍 `[0.5,0.5]`。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_analyze_uses_labels_or_stays_null` | 不读 `p1`。scientific labels → `p1 is None`。 |
| `test_direct_transfer` | 形状。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]`；analyze 标签不够建 P1；smoke **要求** 空结论。
2. **C6-M-01 用带 task 的 helper 盖住 CLI 无 task。** 冻结树 collect/label 不写 `tasks.jsonl`。fit 只看这两个目录。
3. **donor「来源—数值」靠目录名。** `_load_source_value_pair` 找 `src.parent/{prep,prepare,s-prep}/edits.jsonl`。测试目录恰好叫 `prep`。孤立目录变成 `same_identity_fallback`（碰巧仍是 base/edit）。collect 不持久化 pair 元数据。
4. **INLP/C-rand/rescue「分 decode」是 mode 字符串。** 本通道同 seed 下 generated_ids 全相等。
5. **`ie_z_g=target_follow` 盖住恒 0 的 g。** 教员强制 `82` vs hook 抽到 `9`。非 tiny 仍调用隐均值 `ie_z()`。
6. **科学事件非空，来源是教员强制 `q=`。**
7. **步前 H 用有限行数冒充「不是末 token」。**
8. **`refilled_prefix` 认任意有限标量 hidden。** ids/空列表已拒。
9. **账本协议行仍 pytest；可执行行 `tests_exist_not_acceptance`。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已在 **声明冻结树** 上执行。本通道未加测试。

### CE-1 donor 仍 t0p（行身份攻击失败；测试仍是名字）

```text
prep/col 兄目录：
  pair_meta 经 parent/prep/edits.jsonl 读到
  donor_kind=same_source_diff_value
  donor_rows=(0,2) → trace-base / trace-edit
  不是 trace-t0p

孤立 alpha/beta：
  pair_meta=None（collect 无 edits.jsonl）
  donor_kind=same_identity_fallback
  仍是 base/edit（skip={trace-t0p}）

finite_fallback（base≈edit，只剩 t0p 可区分）：
  (0,1)=base/t0p     → 现测试不跑、不锁 trace_id

应：断言 event_rows[donor].trace_id == pair.trace_ids.same_source_diff_value
    且缺 edits.jsonl 时拒绝或显式 fallback，而不是靠目录名
```

### CE-2 INLP 仍 swap（函数攻击失败；decode/测试未锁）

```text
h@P 向量 ≠ apply_swap          实现有
同 seed generated_ids：
  inlp == swap == add_delta == baseline == [16,59,4,8]
CLI inlp_followed_donor=False
测试只锁 inlp_transform=="inlp"

应：至少锁 inlp decode ≠ swap decode，或锁 projector 被施加
```

### CE-3 ie_z 仍隐均值（tiny 数值攻击失败；标签替身仍在）

```text
CLI ie_z = 0.0
ie_z(H_d, H_b) ≈ 4.91e-5     不相等 → 不是隐均值
ie_z_g = "target_follow"     测试只锁这个
donor_ans=82（强制行）；decode ans=9；g≡0
非 tiny：ie_z(rescued.matched, base) 仍是均值
test_ie_z_and_rescue_controls 仍测均值 helper

应：锁 ie_z == g_int-g_base，且禁「只改标签」；或拒绝无可变 Y 的轨迹
```

### CE-4 C6-M-01 标签序（冻结树攻击成功）

```text
helper(task.premises=p1,p2,p3；labels=p3,p2,p1) → ['p1','p2','p3']   单元绿
cmd_fit(--in-dir collect, --labels-dir label)：
  collect/tasks.jsonl 不存在
  label/tasks.jsonl 不存在
  task_for_e is None
  unique = ['p2','p1']          # labels 首次出现序
  E 列 = ['p1','p2']            # collect 按 task.premises
  本夹具 task_label 全 1 → Y 全 1，错序不可见
应：fit 必须读到 task.premises（或拒绝）；CLI 反序 labels 断言 Y 列与 E 对齐
```

### CE-5 Prefill

```text
prefix_token_ids=[1,2,3]              → False   已锁
execute={prefill_hidden:[]}           → False   已锁
execute={refilled_prefix:True}        → False   已锁
execute={prefill_hidden:0}            → True    冻结树现测试绿
execute={prefill_hidden:[0.0]}        → True
execute={prefill_hidden:True}         → True
```

### CE-6 CLI analyze / e2e

```text
scientific labels → p1 is None
fixture 八阶段：offline H=[[1..8]]，结论空
```

## 9. 发现

### F9-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）。同类 D7-01。
- **文件：** `.planning/audits/round-09/VERSION.md` L5–23；开审 60 文件 = `9ffc4cd9…`；交卷 61 文件 = `599f3b9d…`
- **复现：** 开审脚本原文 MATCH。审查期间出现 `tests/test_round07_regressions.py`，且 `cli.py`/`repair.py` 等被改（collect 复制 `tasks.jsonl`、`_find_tasks_jsonl`、`_hidden_is_prefill`）。这是 **另一哈希上的补丁**，不能当作本冻结已闭。
- **注：** 夹具仍在摘要外（F9-12）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F9-01 donor 行不再是 t0p；测试锁 `donor_kind` 与 `prep/` 启发式

- **严重度：** Medium（验证残留）；点名「donor 仍 t0p」作为行身份 **本轮攻击失败**
- **状态：** confirmed defect（验证替身）；实现部分闭合
- **文件/行（冻结树）：** `cli.py` `_load_source_value_pair` / `_pair_source_value` / `_expressible_donor`；`tests/test_round06_regressions.py` L65–79
- **复现：** §3 CE-1。科学 tiny：`trace-base`/`trace-edit`。孤立目录无 pair 元数据 → `same_identity_fallback`。`finite_fallback` 仍可点到 t0p。
- **作者主张 D7-03：** **部分**（有 `prep` 名时走 source-value；不是「任意 collect 都读到 pair」）

### F9-02 INLP hook 不是 swap；decode 与测试仍把「名字」当闭合

- **严重度：** Medium
- **状态：** confirmed defect（验证）；实现函数闭合
- **文件/行：** `models/collect.py` `intervene_hidden_decode` `mode=inlp`；`cli.py` 写 `inlp_transform`；测试 L70
- **复现：** §3 CE-2。向量不同；token 相同。
- **作者主张 D7-04 INLP=`h@P`：** **函数是。** 不是「分 decode」的测试锁。

### F9-03 tiny `ie_z` 不是隐均值；`ie_z_g` 与恒 0 的 \(g(Y)\) 是替身

- **严重度：** High
- **状态：** confirmed defect（验证 + 科学接口）
- **文件/行：** `cli.py` `ie_z = g_int - g_base` + `ie_z_g="target_follow"`；`interventions.py` `ie_z` helper；`tests/test_round03_regressions.py` `test_ie_z_and_rescue_controls`；`test_round06` L73
- **复现：** §3 CE-3。强制 `82` vs hook `9`。非 tiny 仍均值。
- **作者主张 D7-04 `ie_z` 用 target-follow \(g(Y)\)：** **标签是。** 没有可变 Y。helper 与单元测试仍是隐均值。

### F9-04 C6-M-01：helper 锁带 task 的序；冻结树 CLI fit 回到 labels 首次出现序

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）。**冻结树未闭。**
- **文件/行（冻结树）：** `cli.py` `_e_premise_ids`、`cmd_fit`（只搜 collect/label 的 `tasks.jsonl`）；`tests/test_round06_regressions.py` L123–136；`models/collect.py` E 按 `task.premises`
- **触发：** 作者自己的 `collect --out-dir col` + `label --out-dir lab` + `fit --in-dir col --labels-dir lab`
- **复现：** §3 CE-4。`unique=['p2','p1']`。E=`['p1','p2']`。Y 全 1 盖住错序。
- **作者主张 C6-M-01：** **未闭合（本冻结）。** 交卷后另哈希上 collect 复制 `tasks.jsonl` **不得**记入本条关闭。

### F9-05 `prefix_token_ids` 已拒；冻结树任意有限 dummy hidden 仍是 Prefill

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）。点名 prefix_ids **闭合**。
- **文件/行（冻结树）：** `repair.py` `bool(np.isfinite(...).any())`；`tests/test_round06_regressions.py` L82–87
- **复现：** §3 CE-5。
- **作者主张 F6-04：** **部分**（ids/空 hidden 闭；`0`/`True` 未闭）。交卷后 `_hidden_is_prefill` 是 **另一哈希**。

### F9-06 科学事件已排除题干；测试仍接受强制 `q=`

- **严重度：** Medium
- **状态：** confirmed defect（验证残留）
- **复现：** 6–7 轨迹事件全是 `\nq = <digit>`。`parse_region` 硬编码。
- **作者主张 A6-01 / F6-01：** **部分**

### F9-07 NaN 行数已锁；「不是末 token」仍是测试名

- **严重度：** Medium
- **状态：** confirmed defect（验证残留）
- **复现：** `pre_idx=44≠51`。测试不比 last。

### F9-08 CLI / Goal e2e 仍接受未接通科学路径

- **严重度：** Critical
- **状态：** confirmed defect（验证）
- **文件：** `tests/test_cli_pipeline.py`；offline collect / analyze
- **复现：** §3 fixture 八阶段。

### F9-09 analyze 标签测试不锁 P1；科学路径 p1 仍为 None

- **严重度：** Medium
- **状态：** confirmed defect（验证）

### F9-10 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：69 行 `python -m pytest -q`；320 行 `passed_local_tests`；可执行 159 行 `tests_exist_not_acceptance`。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed**（本冻结作者称 144）。

### F9-11 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes`、`assert_disjoint`、`card`、`apply_model_template`

### F9-12 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个，开审已读）

### F9-13 点名旧 CE 本轮未复现（不要写成 Goal 验收）

- **严重度：** —
- **状态：** 非缺陷建议
- **作为行/函数未复现：** donor=t0p；INLP 函数=swap；tiny `ie_z`=隐均值；`prefix_token_ids` 当 Prefill。
- **作为测试仍活的替身：** C6-M-01 helper；donor/INLP/`ie_z` 字段名；标量 Prefill。

### F9-14 ISSUES / VERSION 作者关闭高于冻结验证力度

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为验证闭合：** F6-01 题干 span；F6-02 NaN 行入 H；F6-03 科学 `donor_missing`；F6-05 `[δ,δ]` 实现；F6-04 的 prefix_ids/空 hidden；donor **行**非 t0p；INLP **函数**非 swap；tiny `ie_z` **数值**非隐均值。
- **未闭：** C6-M-01 CLI（F9-04）；标量 Prefill（F9-05）；e2e（F9-08）；`g(Y)` 恒 0（F9-03）；账本（F9-10）；冻结交卷漂移（F9-00）。
- **不要用本通道把 Goal/需求标 Complete。**

### F9-15 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess **不是** pending_server。C6-M-01 与 dummy hidden 是有名字的本机缺口。交卷漂移也不是 pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 69 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F9-10）。C6-M-01 被 helper 填绿（F9-04）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F9-00、F9-04、F9-05、F9-08 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** 开审 `pytest -q` 确为 144/0。e2e 是 exit-code 烟测并断言空结论。点名项有测试，但锁替身。交卷磁盘已变，不能再引用该 144 为「当前树」。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 仍写 136 passed。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。本文件是审查日志，不改变被审摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：fit Y 错序、dummy hidden、offline 前缀 H、目录名 donor、恒 0 的 `g(Y)`。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F9-14）。开审本机 pytest 记录存在（144/0）。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。fit Y 与 E 在冻结 CLI 上对反。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。CLI 无 task 时回到首次出现序。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。测试锁 transform **名**。decode ids 不分。`hook_timing` 仍 `pre_step`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。analyze 常不建 P1。 |
| 13 附录修复 | 新前缀 Prefill | ids/空 hidden 拒；标量 0 仍 True（冻结树）。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **开审 144 passed，exit 0，18.87s，144 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **开审 HASH_MATCH `9ffc4cd9…`（60）。交卷 HASH_MISMATCH（61，`599f3b9d…`）。** |
| 独立性 | 真 oracle：题干排除、H 有限、科学 ≠`donor_missing`、prefix_ids 非 Prefill、噪声 `lo<hi`、donor **行**非 t0p、INLP **函数**非 swap、tiny `ie_z` **数值**非隐均值。**不独立：** C6-M-01 helper、donor/INLP/`ie_z` 字段名、offline H e2e、强制 `q=`、标量 hidden、`g≡0`。 |
| Mock/stub | offline 前缀 H + helper 自带 task + `prep/` 兄目录 + mode 字符串 + `ie_z_g` 标签 + `not_evaluated` 编码为成功。 |
| 论文行为仍未证明 | CLI 上 E/Y 同序（冻结树）、真 Prefill、可变 `g(Y)`、分 decode 的 token、从 labels 建的 P1、隔离执行、自然 CoT 事件 |
| 交付 vs 测试 | 「144 passed / D7-03/04/05 已接线 / C6-M-01 已锁」**超过** 冻结树测试力度 |
| 已确认问题？ | **是。** Critical：F9-00、F9-08。High：F9-04、F9-05、F9-03。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。交卷哈希已漂。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。即使 A–E 全写「通过」，两轮计数必须保持 0；修复后换 **新** hash 重开。 |

在声明冻结上用 CE 级测试锁住 C6-M-01 的 **CLI 列序**、标量 hidden、donor **trace_id**、INLP/swap 的 **decode 差**、以及非恒 0 的 \(g(Y)\) 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。事后在另一哈希上补 `tasks.jsonl` / `_hidden_is_prefill` **不能**把本轮改写成通过。
