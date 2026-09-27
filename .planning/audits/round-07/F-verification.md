# F：验证质量与反向质疑（round-07）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-07 其他通道报告。`ISSUES.md` 只当作者主张；每条声称的 r06 闭合都从测试对生产符号重核，再用进程内反例攻击（未向仓库加测试）。`python -m pytest -q` 绿不是论文正确性，也不是 Goal 验收。

**先行结论：** 冻结哈希 **复算一致（HASH_MATCH）**。本机 `python -m pytest -q` 为 **143 passed / exit 0**。这不是 Goal 通过。相对 r06，作者用来关闭 F6-02 / F6-03 / F6-04 / F6-05 的若干 **原 CE 本通道攻击失败**（科学 H 有限、科学 intervene 不再 `donor_missing`、`prefix_token_ids`/空 hidden/旗标不再冒充 Prefill、噪声数据上区间有宽度）。但测试仍锁替身：**教员强制 `\nq = <digit>` 当唯一科学事件**（题干赋值不再入 `trace.events`，F6-01 原 CE 不复现）；`test_intervene_geometry_is_not_pre_step` 仍走 offline 单行 H → `unexpressible`/`donor_missing` 只断言 `!= pre_step`；`prefill_hidden=0`/`True` 仍把 `refilled_prefix` 打成 True；r04 ρ=y 数据区间仍 `[0.5,0.5]`；fixture 八阶段仍是 offline 前缀 H + `scores=None` + `p1 is None`。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：本通道提交已确认缺陷，连续两轮 A–F 通过计数 **不能开始**。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801` |
| 复算聚合 | `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801` |
| 哈希裁决 | **HASH_MATCH** |
| 哈希方法 | 60 个文件：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。按 POSIX `relpath` 排序。`SHA-256.update(relpath.encode() + b"\0" + file_bytes)`。`VERSION.md` 脚本原文。范围内 0 处 CRLF。 |
| 文件数 | 60，与 `round-07/VERSION.md` 一致（r06 为 59；新增 `tests/test_round06_regressions.py`） |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest | **143 passed in 19.06s，exit 0。** Collect：**143 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只出现在 HumanEval/`SubprocessExecutor` 载荷字符串里。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。一处 `@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 范围 | 全部 `tests/**`（17 个 `.py` + 10 个夹具 JSON）及测试导入/CLI 烟测触及的生产符号 |
| 明确未读 | `.planning/audits/round-07/{A,B,C,D,E}-*.md` |

审查对象是**当前工作区字节**。作者 `pytest_author_claim: 143 passed` 仅作为命令结果被独立确认。

## 2. 逐文件覆盖

### 2.1 测试（全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍是 `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 397 | `d3814498fe52b28b…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H）；analyze 无 `--in-dir` 不写半成品 |
| `tests/test_round03_regressions.py` | 291 | `5698a410c0669b61…` | r03 节点；P1 泄漏用例仍绿；`prefix_token_ids` 只锁 token 计数，不锁 Prefill |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline intervene 仍只 `!= pre_step`；bootstrap 只查非空；scientific prepare 仍 `events>=1` |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | 相对 r06 加强：collect 现要求 `isfinite`；tiny intervene 现禁 `donor_missing`；prepare 要求 sham:` 前缀与 `source_value_pair`。**仍不锁** decode 后缀可解析、token≠last、P1 宽度 |
| `tests/test_round06_regressions.py` | 117 | `6eb0a0ed0f3fefd1…` | 7 个新节点：题干起点、有限 H + `offline_hidden`、`prefix_token_ids` 拒、`lo<hi`、sham hits 空噪声、catalog 两个别名、下游无 `--in-dir` 拒。独立与替身混杂（见 §6） |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、verbalizer 可见性、`prefix_token_ids` 现锁 False、swap |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only：**143 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r06 的 136 节点：+7，全部在 `tests/test_round06_regressions.py`。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、precomputed、P2 分母、P3 回声、Week8 零 excess / 阈值无测量、bootstrap **键名+一处 `lo<hi`**、BOW retrieval、PCA Procrustes | 留出泄漏 oracle；r04 数据退化区间；Gate **阈值比较**；`procrustes` 无直接测试 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 抽答案相等（17/70/boxed 已锁）；无 generate 拒答；dev 阈值区间 | `attention_mean`/`attention_rollout` 仅 CLI 烟测写入，无数值 oracle |
| `cli.py` | 1143 | `8986a0d8aa696c6e…` | smoke offline；scientific prepare/collect/fit/intervene/repair；resume；analyze 文件/无 in-dir 拒；calibrate/intervene/repair 无 in-dir 拒 | 科学 **行为头** `no_known_labels`；analyze 科学 labels → `p1 is None`；offline intervene `unexpressible`；`_expressible_donor` 跨 node 回退 |
| `edits.py` | 277 | `bfd1632b50504c04…` | value/rename/op-reverse/5.5；source-value 元数据旗标 | 同值异源是否真改源 |
| `events.py` | 260 | `fc5031a51e99a4b5…` | 身份对齐；monotonic；open-think；`parse_events` 手写 `"p1 = 4. p2 = 0.\\nq = 9"` | 解析器仍吃题干；科学路径改在 generate 切片，不在解析器 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False`；子进程超时 | 宿主 CPython 子进程 ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP/范数 | CLI C-layer 无 `--dev-layer-scores` → `dev_scores_missing` |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 345 | `1fa2360e680d37ad…` | 事件均值；空 N；`noise_evaluated` 单元；sham hits → 噪声 null | `soundness_claim_allowed` 恒 False；hits 测试接受 `null_reason` 即可 |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 199 | `2772257e0643b3c7…` | 有限 H；拒 offline；`event_rows` 行数 | 无 token 的事件被 `continue` 丢掉（好）；`intervene_swap_decode` 在 `event_aligned` 时写 `hook_timing=pre_step` |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 201 | `07493570c6410e6b…` | replay/greedy；scientific 调 `generate_task_trace`；事件起点 ≥ prompt | 后缀乱码；`append_target_assignment` 教员强制；`apply_model_template` 无测试 |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` / `clone_cache` **实现了、未断言** |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | n=3→1；contained；跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 行掩码（科学 fit 侧写） | CLI 科学路径行为头无已知标签 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号已锁；`status==ok`+shape | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；`truth_indices` | smoke `scores=None` |
| `repair.py` | 223 | `d547ab99e3179093…` | 无 hidden / 空 hidden / 旗标 / `prefix_token_ids` → False | `prefill_hidden=0`/`True`/`1.0` 仍 True |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | `Event.from_dict` extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 111 | `35cd0e3f724ee850…` | Plus→test；`gsm_family_id` | `assert_disjoint` **零测试** |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | `t3_musique` / `t4_boundary` 别名 | `musique`/`t4` 短名无测试；`LOADERS` 其余键无直接测 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 81 | `8e58c5d22b41b87b…` | family / test-only / 隔离 `13`≠`19` | `"reversing operation"` 仍非 T4 |
| `tasks/t2_gsm_symbolic.py` | 84 | `b50db6533f18948d…` | sidecar | 无 sidecar 占位前提 |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` **实现了、未断言** |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；口语 `needs_truth` | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 75 | `d31bcd499a51ca94…` | 4096/3584；labeled 需标签；PCA 不静默截断；**形状** | `apply_map(tgt)≈src` **本通道数值不恢复** |

夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `9814019a…f95801`（60 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 全量 pytest | 仓库根 `python -m pytest -q`（`pythonpath=src`） | **143 passed in 19.06s，exit 0**。无 skip/xfail/deselected。 |
| Collect | `python -m pytest tests --collect-only -q` | 143 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM `4*3 % 23 = 12`；sidecar 8；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]`；BCE 符号 | **存在的单元断言**与独立算术一致 |
| 对抗：F6-01 题干当事件 | `generate_task_trace(t1_tiny)`；scientific prepare | **原 CE 不复现。** `trace.events` 仅 `q`，`start=45≥len(prompt)`，`parse_region=generated`。`parse_events(prompt)` 仍得 p1/p2。全文解析仍含题干，但 generate 只切片生成区。 |
| 对抗：教员强制 q | 同上 | decode 后缀 `'Z*H[!XTC'` 不可解析。唯一事件来自 `assigned='\nq = 82'`，`parse_status=constrained_target`。6 条科学轨迹 **各 1 个 q**。`test_generated_events_*` / `test_scientific_prepare_*` **绿**。 |
| 对抗：F6-02 NaN H | scientific collect tiny | **原 CE 不复现。** `H.shape=(6,32)`，`nan_frac=0`，`event_rows==6` 全是 `q`。`H_pre_*` 亦有限。p1/p2 不再入 H（因不再是事件）。q 的 `token_index=44≠last 50`。测试仍不锁 ≠last。全 NaN 现会被 `isfinite` 打红。 |
| 对抗：F6-03 科学 intervene | 作者路径 + `--dev-layer-scores 0.05 0.9 0.8` | **原 CE 不复现。** `timing=offline_hidden`，`status=prospective_decode`，`clayer_status=dev_weak_layer_decode`，`donor_rows=[0,1]` 同 `node_id=q` 跨轨迹。`relative.hook_timing=pre_step`（decode 函数自己的字段；行字段不是 `pre_step`）。无 dev 分数时 `clayer_status=dev_scores_missing`，行 timing 仍 `offline_hidden`。 |
| 对抗：offline intervene | fixture collect offline → intervene | **`timing=unexpressible`，`status=donor_missing`。** `test_intervene_geometry_is_not_pre_step` 只断言 `!= pre_step`，**仍绿在替身上。** |
| 对抗：F6-04 Prefill | `run_repair` 哑 execute | 无 hidden / `prefill_hidden=[]` / `refilled_prefix=True` / `prefix_token_ids` → **False**（作者新测试锁这些）。**`prefill_hidden=0` / `True` / `1.0` → True。** |
| 对抗：F6-05 bootstrap | 作者 r06 噪声数据；r04 ρ=y | 噪声：`[0.112, 0.891]`，`lo<hi`。r04：`[0.5, 0.5]`。`test_p1_returns_bootstrap_interval` 仍绿。实现会重算 ΔAUC（`analysis.py` 哈希与 r06 相同）。 |
| 对抗：verbalizer / span / Week8 / analyze 入口 | gold=`7`；跨界 span；无 in-dir | `17`/`70`/`boxed{8} also 7`→0；`[1,3]`→`[]`；`threshold_present_measurement_missing`；无 `--in-dir` / 文件 in-dir **不写** `report.json`。**这些 r05 CE 仍不复现。** |
| 对抗：fixture 八阶段 | prepare→…→analyze，`--backend offline` | `H=[[1..8]]`；双头 **同一 loss** `0.05036…`；calibrate `scores=None`；intervene `unexpressible`/`donor_missing`；repair `refilled_prefix=False` / `generated_tokens=0`；analyze `p1 is None` / `not_evaluated` |
| 对抗：scientific labels → analyze | prepare scientific → label（3 条二元 `task_label`）→ analyze | exit 0，`p1 is None`。手写 4 条同类对半划分 → `p1.status=single_class`。交错 1/0/1/0 → `estimate`，`delta_auc=0.5`。测试不读 `p1`。 |
| 对抗：scientific fit | collect tiny 后 fit | **行为头 `status=no_known_labels`，无 `U`。** 任务头 `loss≈0.05036`。`test_scientific_h_is_finite_and_pairs_donor` 用 `next(... if "U" in row)`，只碰到任务头。 |
| 对抗：`_expressible_donor` | 异 node 各 1 条轨迹 | 回退配对 `(0,1)` = p1 与 q。全 q 的科学产物使“同 node_id”无法被测试独立证伪。 |
| 对抗：k repair | scientific repair k=1..5 | slots 集合有变化；`generated_tokens` 全 8，`extra_prefill` 全 32，`refilled_prefix` 全 True。 |
| 对抗：账本 | 解析 `PAPER_TRACEABILITY.md` 528 行 TR | `verification_method=python -m pytest -q`：**69 行**。`local_verify_status=passed_local_tests`：**320 行**（其中 `experiment_protocol` 296 行）。`executable_function`：**159 行**均为 `tests_exist_not_acceptance`（0 行 `passed_local_tests`）。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed** 与 “Round-06 starting”。 |
| 对抗：Plus / Hotpot | 与作者测试相同构造 | `13` 保留、无 `19`；`needs_truth` / `requires_independent_truth`。 |
| 对抗：transfer | `src=I`，`tgt=diag(2,3,4,5)` | `apply_map` **不**恢复 I（maxabs≈2.50）。套件只查 shape。 |
| 对抗：P1 泄漏 | 作者 ρ=y 全行 | `auc_full=1`，`delta=0.29`。现测试仍绿。 |
| 对抗：sham hits | 作者 r06 构造 | `rho_S_noise is None`，`null_reason=noise_set_missing`。测试的 `or null_reason in {…}` 在 `rho=0.0` 且带该 reason 时仍绿。 |
| 对抗：catalog | `musique` / `t4` 短名 | 实现可用。测试只锁 `t3_musique` / `t4_boundary`。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-07 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 143 passed | `VERSION.md` L26 | **命令是。** 当作阶段/Goal 证据：**否。** |
| r06 已在本地关闭，待独立复核 | `ISSUES.md` | **部分。** F6-02 有限 H、F6-03 科学路径不再 `donor_missing`、F6-04 的 prefix/空 hidden/旗标、F6-05 噪声数据 `lo<hi`、sham hits 不记评估 0、catalog 两个别名、下游无 in-dir、source_value_pair、`--weight-seed`、C-layer 二次 decode——单元或本通道复现成立。A6-01/F6-01 **题干事件**闭合，**生成推理步骤**未闭。F6-04 标量 hidden、F6-05 r04 退化区间、F6-06 账本、F6-07 analyze P1、F6-08 e2e **未闭。** |
| scientific generate / 步边界 H / Prefill / 重采样区间 / 诚实账本 | `ISSUES.md` A6-01 / F6-01–05 | 测试存在。锁的是生成区起点、有限行、一种 dummy、一处 `lo<hi`、可执行行的 `tests_exist_not_acceptance`。 |
| CLI 流水线消费上游 | `test_full_cli_smoke`；`test_pipeline_consumes_upstream` | 文件被读。科学没有：offline H、`scores=None`、analyze 忽略不足以建 P1 的 labels。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham∉R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 **span**（不是答案证明）；B-11 空父母；B-13 `family_id`；B-14 source=/test_only + 生产 key；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]` + `predict_set`；bilinear σ/λ_FN；spy.calls / `exec(`；E-17 labels-dir hash；Boundary BCE 符号；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess + 未注册 Gate + 阈值无测量；gsm 家族键；monotonic 版本；resume 不覆盖成功 manifest；`truth_indices`；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语。

**本冻结新增或加强且独立：**

- `test_generated_events_exclude_prompt_assignments` 的 **题干半边**：`start >= len(prompt)` + `parse_events(prompt)` 仍能读到 p1/p2。若 generate 再把题干写进 `trace.events`，本测试会红。**F6-01 题干 CE 作为实现+该断言闭合。**
- `test_scientific_h_is_finite_and_pairs_donor` / 加强后的 `test_scientific_collect_h_is_step_boundary_not_last_token`：`np.isfinite(H).all()`。全 NaN 行矩阵会红。**F6-02 NaN-in-H CE 闭合。**
- 同上 + 加强后的 `test_intervene_tiny_geometry_timing_stays_offline`：`status==prospective_decode`、`timing==offline_hidden`、`!= donor_missing`。科学路径再返回 r06 的 `unexpressible` 会红。**F6-03 科学路径原 CE 闭合。**
- `test_prefix_ids_alone_are_not_prefill` + `test_science.py` `prefix_token_ids` 半边：无 hidden / 空列表 / 旗标 / 仅 ids → False。**F6-04 这四种 CE 闭合。**
- `test_p1_bootstrap_interval_is_not_degenerate`：作者噪声数据上 `lo < hi`。`[δ,δ]` 实现会红。**F6-05 在该数据集上闭合。**
- `test_sham_hits_do_not_book_evaluated_zero_noise`：当前实现 `rho_S_noise is None`。独立复现。测试析取偏弱（见 §6.2）。
- `test_catalog_aliases_musique_and_t4`：`t3_musique`/`t4_boundary` 能 load。**E6-13 这两个别名单元闭合。**
- `test_missing_in_dir_fails_for_downstream`：calibrate/intervene/repair 无 `--in-dir` 抛 `ValueError`。**E6-17 入口闭合。**
- `test_scientific_prepare_emits_parseable_events` 现锁 `sham:` 前缀与 `source_value_pair`。

### 6.2 无效、自指或过弱（含本轮点名的替身）

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_full_cli_smoke` | **offline H 当成功。** 本通道复现 `H=[[1..8]]`、`scores=None`、`p1 is None`。仍断言 `scientific_conclusion is None`。 |
| `test_e04_analyze_manifest_includes_report` | 空目录 analyze → `not_evaluated` 编码为成功。 |
| `test_pipeline_consumes_upstream` / `test_fit_hashes_labels_dir` | 停在 fit；offline 前缀 ID 上任意有限 loss 都过。双头同 loss。 |
| `test_analyze_uses_p1_table` | 只要求 `p1 is not None`。手写 `p1_table.jsonl`。不读 `labels.jsonl`。 |
| `test_analyze_uses_labels_or_stays_null` | 只锁 `scientific_conclusion is None` 与 Gate `unregistered`。**不读 `p1`。** 本通道 scientific labels → `p1 is None`。 |
| `test_scientific_prepare_*` / `test_generated_events_exclude_prompt_assignments` 的成功半边 | 禁题干事件、要求存在 `q`。`q` 由约束解码教员强制。**不要求 decode 后缀可解析。** 6 轨迹各 1 事件即可绿。 |
| `test_parse_events_reads_premises_and_target` | 手写全文 `"p1 = 4. p2 = 0.\\nq = 9"`。锁的是解析器吃题干，不是 generate。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 名称为 last-token，断言是有限 + `shape[0]<=n_events`。不比 `token_index≠last`。 |
| `test_scientific_h_is_finite_and_pairs_donor` | 有限 H 与 `donor_rows` 下标不同。科学事件全是 `q`，同 node 无法被证伪。`next("U" in row)` 不锁行为头。`inlp_followed_donor` 只查键。 |
| `test_intervene_geometry_is_not_pre_step` | **仍走 offline 单行 H → `unexpressible`。** 断言 `!= pre_step`。与 r06 F6-03 同类替身，只是不在科学路径。 |
| `test_dummy_execute_is_not_prefill` / `test_prefix_ids_alone_are_not_prefill` | 不锁 `prefill_hidden=0`/`True`。 |
| `test_repair_*` / `test_scientific_repair_runs_k_1_to_5` | 要求 `refilled_prefix` 全 True。k 不改 generated/extra_prefill。 |
| `test_p1_bootstrap_resamples_delta_auc` | 仍 `lo<=hi`。`test_p1_returns_bootstrap_interval` 只要求 interval 非空。r04 数据 `[0.5,0.5]` 绿。假宽度 `[μ-ε,μ+ε]` 也能过新测试。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_p1_precomputed_is_scores_not_magic` | `length==ρ` 时旧魔术 Δ 也是 0。 |
| `test_direct_transfer` / labeled map | 形状。本通道 `apply_map` 不恢复 I。 |
| `test_sham_hits_do_not_book_evaluated_zero_noise` | `rho is None or null_reason in {noise_set_missing, sham_protocol_missing}`。`rho=0.0` 且带 reason 仍过。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。last-token / once 未测。 |
| `test_align_equal_count_*` `scanned is False` | 镜像硬编码常量。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |
| `test_calibrate_infinity_is_json_safe` | `q is None or isinstance(q,(int,float))` 几乎恒真。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline（F7-08 / 遗留 F6-08）。** `H`←`token_ids[:8]`；无 `--features-dir` 则 `scores=None`；analyze 标签不够建 P1；smoke **要求** 空结论。
2. **scientific 事件非空，来源是教员强制 q（F7-01 / F6-01 残留）。** `generate_task_trace` 现只 `parse_events(generated)`（题干不再入列，好）。`append_target_assignment` 仍写 `\nq = <logits digit>`。测试把它当“可解析 generate”。
3. **步前 H 有限（F6-02 原 CE 闭合）。** 不可表达行被 `continue` 丢掉。测试仍不锁 last-token。本通道该夹具 `index=44≠50`。
4. **科学几何测试现碰到几何（F6-03 科学路径闭合）。** offline 几何测试仍躲开（F7-03）。`_expressible_donor` 在同 node 不够时跨 node 回退；全 q 事件使身份配对不可独立证伪。
5. **`refilled_prefix` 认任意有限 hidden（F7-04）。** `bool(np.isfinite(np.asarray(hidden)).any())`。`0`/`True`/`1.0` 都算有 hidden。prefix_ids / 空列表 / 旗标已拒。
6. **P1 一处锁 `lo<hi`，其余锁名字（F7-05）。** 实现会重算 ΔAUC（好）。r04 测试不禁 `[δ,δ]`。
7. **账本页眉与可执行行 status 维持 r06；协议行仍 pytest；06-VERIFICATION 仍写 136（F7-06）。**
8. **HumanEval spy / Child 非沙箱仍成立。**
9. **科学 fit 行为头空标签被 `next(U)` 盖住（F7-09）。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`card`、`apply_model_template`、`clone_cache`、`probe_prf1`。`catalog.load_snapshot` 本冻结有测试。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 科学事件必须来自自由 decode，或拒绝宣称 generate

- 构造：`generate_task_trace` / `prepare --eval-mode scientific` + `t1_tiny`。
- 期望：decode 后缀可解析出步骤；或 `parse_status=parse_failed` 且 prepare 拒。仅教员强制 `\nq = <digit>` 不得单独满足“有 q 事件 / generated”。
- 当前：events=1（q），`parse_status=constrained_target`，后缀乱码。题干 p1/p2 **不再**入 `trace.events`（F6-01 原 CE 失败）。
- `test_generated_events_*` / `test_scientific_prepare_*` **绿**。

### CE-2 步前 H（F6-02 原 CE 本轮攻击失败）

```text
scientific collect: H.shape == (6, 32), nan_frac = 0, 全是 q
q: token_index 44 ≠ last 50     → 实现有，测试没锁
全 NaN 但 n_events>1 的 H       → 现测试会红（isfinite）
```

### CE-3 科学 tiny intervene（原 CE 失败）vs offline 替身（仍在）

```text
作者科学路径：timing=offline_hidden, status=prospective_decode
  → 新测试绿，且本通道独立跑到几何/hook
offline 单行 H：timing=unexpressible, status=donor_missing
  → test_intervene_geometry_is_not_pre_step 仍绿
异 node 有限 H：_expressible_donor 回退跨 node
  → 无测试锁同 node_id
```

### CE-4 CLI analyze 必须消费 labels 或拒绝

- 构造：scientific prepare+label（本通道 3 条二元 task_label）后 analyze。
- 期望：拒绝，或用这些 labels 给出冻结 P1。
- 当前：exit 0，`p1 is None`。`test_analyze_uses_labels_or_stays_null` **要求** 空结论。
- 手写 4 条 `1,1,0,0`（对半 held-out）→ `single_class`。交错 `1,0,1,0` 才能 `estimate`。

### CE-5 Prefill 不是标量 / 布尔

```text
execute={generated_ids:[1], extra_prefill:0}      → False   已锁
execute={generated_ids:[1], prefill_hidden:[]}    → False   已锁
execute={generated_ids:[1], refilled_prefix:True} → False   已锁
run_repair(..., prefix_token_ids=[1,2,3])        → False   已锁
execute={generated_ids:[1], prefill_hidden:0}     → True    现测试绿
execute={generated_ids:[1], prefill_hidden:True}  → True
execute={generated_ids:[1], prefill_hidden:1.0}   → True
```

### CE-6 P1 bootstrap 非退化

```text
r06 噪声数据：interval [0.11, 0.89]   新测试 lo<hi 锁这个
r04 ρ=y 常数 length：interval [0.5, 0.5]
test_p1_returns_bootstrap_interval：非空即可
应：在会变化的数据上 lo<hi（已有），并禁假宽度；或对常数数据显式接受/拒绝
```

### CE-7 verbalizer / span / analyze 入口（本轮攻击失败 = 仍闭合）

```text
gold=7, "17" / "answer 70" / "\boxed{8} also 7" → 0
span [[0,2],[2,6]] × [1,3] → []
analyze 无 --in-dir / 文件 in-dir → 无 report.json
```

### CE-8 账本行级

```text
528 TR 行：69 行 verification_method=python -m pytest -q
320 行 local_verify_status=passed_local_tests（几乎全是 experiment_protocol）
executable_function 159 行 status=tests_exist_not_acceptance
06-VERIFICATION.md 仍写 136 passed / Round-06 starting
页眉声明 ≠ 行级清零
```

## 9. 发现

### F7-00 声明冻结哈希可复算

- **严重度：** —
- **状态：** 非缺陷建议（本轮过程正确）
- **文件：** `.planning/audits/round-07/VERSION.md` L5–23；工作区 60 文件
- **复现：** §1。本地 `9814019a…f95801` == 声明。0 CRLF。
- **注：** 夹具仍在摘要外（F7-12）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F7-01 / F6-01 题干赋值不再入科学事件；测试改锁教员强制 `q = <digit>`

- **严重度：** High
- **状态：** confirmed defect（验证；题干事件实现洞已不复现）
- **文件/行：** `tests/test_round06_regressions.py` L22–31；`tests/test_round05_regressions.py` L23–53；`tests/test_round04_regressions.py` L30–64；`models/generate.py` `generate_task_trace` L148–159、`append_target_assignment` L72–98；`cli.py` `cmd_prepare` L292–297
- **触发：** `prepare --eval-mode scientific` + `t1_tiny`
- **要求：** Goal §五.1/§五.3；作者 A6-01 / F6-01“题干前提赋值不再当作生成事件”
- **复现：** §3。6 轨迹各 1 事件 `q`。仅题干解析仍得 p1/p2，但 **不**写入 `trace.events`。`q` 来自约束 2 位数字，不是自由 decode。后缀不可解析。`parse_status=constrained_target` 被 prepare 接受。
- **影响：** 可以引用“科学 prepare 已排除题干”，同时轨迹没有模型生成的推理步骤。
- **修复：** CE-1；禁止把教员强制行当成 generate 闭合。
- **作者主张 A6-01 / B6-01 / F6-01：** **部分**（题干 CE 不再复现；作者亦承认约束赋值不是自然 CoT。测试仍把该接口锁成成功。）

### F7-02 / F6-02 `H` 不再含 NaN 行；测试仍不锁 last-token

- **严重度：** Medium（残留验证缺口）；原 High NaN CE **本轮攻击失败**
- **状态：** 原 confirmed defect 作为实现+`isfinite` 测试闭合；残留弱断言
- **文件/行：** `tests/test_round05_regressions.py` L56–67；`tests/test_round06_regressions.py` L44–49；`models/collect.py` L50–52；`cli.py` L473–474
- **要求：** Goal §五.6；作者 D6-02 / F6-02“不可表达 pre_step 不再入 H”
- **复现：** 6 行 H 全有限。不可表达事件 `continue`。本通道 q 的 index 44≠50。测试名称写 last-token，断言没有这项。
- **作者主张 D6-02 / F6-02 / E6-18：** **实现+有限矩阵闭合。** 不是论文步前的完整测试锁。

### F7-03 / F6-03 科学 tiny intervene 不再用 `unexpressible` 过关；offline 测试仍如此

- **严重度：** Medium（offline 替身残留）；原 High 科学路径 CE **本轮攻击失败**
- **状态：** 科学路径闭合；offline 验证缺陷仍确认
- **文件/行：** `tests/test_round06_regressions.py` L57–67；`tests/test_round05_regressions.py` L118–131；`tests/test_round04_regressions.py` L115–124；`cli.py` `_expressible_donor` L775–793、`cmd_intervene` L796–905
- **触发：** 科学 collect → intervene tiny（闭合）；fixture offline collect → intervene（未闭）
- **要求：** Goal §五.6/§五.10；作者 A5-08 / F6-03
- **复现：** 科学路径 `prospective_decode` / `offline_hidden` / 同 q 跨轨迹配对。offline 路径 `unexpressible`/`donor_missing`，旧测试 `!= pre_step` 绿。异 node 有限行回退跨 node；科学全 q 使身份配对不可独立证伪。`relative.hook_timing` 仍为 `pre_step`（行字段不是）。
- **作者主张 A5-08 / F6-03 / D6-02：** **科学路径部分闭合；offline 几何测试未闭。**

### F7-04 / F6-04 哑 execute 的 ids/空 hidden/旗标已拒；标量有限值仍 True

- **严重度：** Medium
- **状态：** confirmed defect（实现 + 验证残留）；原 prefix_ids CE 闭合
- **文件/行：** `repair.py` L147–151；`tests/test_round06_regressions.py` L70–75；`tests/test_round05_regressions.py` L88–92；`tests/test_science.py` L76–83
- **要求：** Goal §五.13 / REPAIR-01；作者 F6-04
- **复现：** §3 CE-5。作者锁的四种 dummy 为 False。`prefill_hidden=0`/`True`/`1.0` 为 True。
- **修复：** 只有非空有限向量（来自模型前向）才能标 True；补测标量/布尔。
- **作者主张 F6-04：** **部分**（声称“只认有限 prefill_hidden”——`0` 在 IEEE 意义下有限，测试没排除）

### F7-05 / F6-05 新测试禁噪声数据上的 `[δ,δ]`；r04 测试仍接受

- **严重度：** Medium（残留）；原 High“测试不禁 `[δ,δ]`”**在新节点上闭合**
- **状态：** 部分闭合
- **文件/行：** `analysis.py` `_bootstrap_p1` L196–212（哈希与 r06 相同）；`tests/test_round06_regressions.py` L78–90；`tests/test_round05_regressions.py` L95–109；`tests/test_round04_regressions.py` L192–200
- **要求：** Goal §五.12；作者 F6-05
- **复现：** 噪声数据有宽度。r04 ρ=y 仍 `[0.5,0.5]`。假宽度实现能过新测试。
- **作者主张 F6-05 / A5-03：** **部分**（不是 `[δ]*n` 常数实现；一处 `lo<hi`；旧测试仍弱）

### F7-06 / F6-06 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：69 行 `verification_method=python -m pytest -q`；320 行 `local_verify_status=passed_local_tests`（296 行 `experiment_protocol`）。可执行行 159 条仍为 `tests_exist_not_acceptance`。`.planning/phases/06-acceptance/06-VERIFICATION.md` L8 仍写 **136 passed** 与 “Round-06 starting”（本冻结作者已称 143）。
- **要求：** Goal §九.1；作者 A5-02 / F5-11
- **复现：** §3。页眉禁止 ≠ 行级清零。阶段验证文档过期。
- **作者主张 A5-02 / F5-11：** **部分**（可执行行 status 未回退；协议行与 06-VERIFICATION 未更新）

### F7-07 / F6-07 analyze 标签测试不锁 P1；科学路径 p1 仍为 None

- **严重度：** Medium
- **状态：** confirmed defect（验证）
- **文件/行：** `tests/test_round05_regressions.py` L188–197；`cli.py` `cmd_analyze` L975–997
- **复现：** scientific labels 仅 3 条二元 `task_label`（门限 ≥4）→ `p1 is None`。对半 4 条 → `single_class`。测试不读 `p1`。`probe_prf1` 仍零提及。
- **作者主张 A5-11：** **未闭合**

### F7-08 / F6-08 CLI / Goal e2e 仍接受未接通科学路径

- **严重度：** Critical
- **状态：** confirmed defect（验证）
- **文件/行：** `tests/test_cli_pipeline.py` L4–30；`cli.py` offline collect / analyze
- **复现：** §3 fixture 八阶段。与 F5-01 / F6-08 e2e 同类。
- **作者主张 F4-01 / F5-01 e2e：** **未闭合**（ISSUES 也未声称关闭，正确）

### F7-09 双头同 Y、科学行为头空标签、k 不改 token 预算、apply_map 只查形状

- **严重度：** Medium
- **状态：** confirmed defect（验证）
- **复现：** offline 两头 loss 同为 `0.05036…`。scientific fit 行为头 `no_known_labels`。k=1..5 生成数全 8、extra_prefill 全 32。`apply_map` 不恢复 I，套件只查 shape。
- **作者主张 A5-11 双头 / A5-09 k 增长 / D6-04 二次 decode：** **部分**（slots 与 C-layer 状态有变化；预算、双头 Y、数值 map 未锁）

### F7-10 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes`、`assert_disjoint`、`card`、`apply_model_template`、`clone_cache`、`probe_prf1`
- **注：** `catalog.load_snapshot` 本冻结不再记为零提及。

### F7-11 Week8 / verbalizer / span / analyze 入口 / 题干事件 / 有限 H / 科学 `donor_missing` / prefix Prefill — 本轮攻击未复现

- **严重度：** —
- **状态：** 非缺陷建议（这些 CE 作为实现+独立 oracle 闭合或维持闭合）
- **复现：** §3 CE-2/3/7 与 F6-01 题干半边。不要把本条写成 Goal 验收。

### F7-12 / F6-12 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`；`VERSION.md` 范围
- **影响：** oracle 字节可动而不改 `.py`+toml 聚合

### F7-13 / F6-13 ISSUES `author closed` 对照本通道

- **严重度：** Medium
- **状态：** confirmed defect（过程：关闭表高于验证力度）
- **本冻结可作为单元验证闭合：** F6-02 NaN-in-H；F6-03 科学路径 `donor_missing`；F6-04 prefix/空 hidden/旗标；F6-05 噪声数据非退化；F6-01 题干事件；E6-13 两个 catalog 别名；E6-17 下游 in-dir；A6-04 sham:` 前缀 + hits 不记评估 0（实现）；D6-03 `source_value_pair` 写入；D6-03 `--weight-seed`；D6-04 有 dev 分数时 `dev_weak_layer_decode`；F5-04/06/08、F4-17、B5-02/03、前轮 B-01–14/23/24、C3-M-01/03/07、D-08、E-17、bilinear、spy、BCE、Child 非沙箱等。
- **未闭（错或镜像）：** 教员强制 q 当 generate（F7-01）；offline 几何 `unexpressible`（F7-03）；标量 Prefill（F7-04）；r04 退化区间测试（F7-05）；账本协议行 pytest（F7-06）；analyze P1（F7-07）；F6-08 e2e（F7-08）；双头/k/map（F7-09）。
- **不要用本通道把 Goal/需求标 Complete。** 上表单元闭合 ≠ 科学验收。作者对 F6-01 的文字（约束赋值不是自然 CoT）比测试名称诚实。

### F7-14 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、`offline_prefix_ids`、宿主 `subprocess`、`executor_unavailable` 不得改写成服务器验收。教员强制事件也 **不是** pending_server，是本机验证缺口。

### F7-15 非缺陷说明

- **状态：** 非缺陷建议
- `VERSION.md` 算法可复现。保持脚本冻结。
- 相对本通道 r06：题干不再入科学事件、H 丢掉不可表达行、科学 intervene 真做几何、Prefill 拒 ids/空/旗标、bootstrap 一处 `lo<hi`、catalog 别名、下游 in-dir——这些是真改进。
- `consecutive_pass_count: 0` 与“143 passed ≠ Goal”比把套件当验收更诚实。
- last-token hook、`once=True`、`clone_cache` 看起来已实现；缺测试，故不闭。
- Gate 0–2 未注册与 `scientific_conclusion=None` **不是**缺陷（与 ISSUES 一致）。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**当前测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 69 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F7-06）。反向覆盖失败（F7-10）。科学行被教员强制数字“填绿”（F7-01）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F7-01、F7-04、F7-07、F7-08 为已确认遗留。ISSUES 作者关闭不能代替本表。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 143/0，无 skip 伪装。e2e 是 exit-code 烟测并断言空结论。科学路径有更强测试，仍锁教员强制 q。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 写 136 不是验收（过期）。账本协议行仍 `passed_local_tests`。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 哈希匹配（好）。`VERSION.md` `consecutive_pass_count: 0`。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。只补审查日志不改变被审 hash——本文件属于审查日志，不改变 60 文件摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：教员强制事件、offline 前缀 H、标量 Prefill、宿主 subprocess 都是 **有名字的代码** 缺口。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F7-13）。本机 pytest 记录存在（143/0）。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 解析器切片生成区；生成区只有强制 q。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。scientific sham `premise_id` 带 `sham:`。hits 不记评估 0（实现）。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。collect 丢掉不可表达行。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。offline 双头同 Y。科学行为头空标签。rollout 无数值测试。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。smoke `scores=None`。科学+features-dir 本通道有有限 q。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒有。数值恢复未锁且本通道不恢复。 |
| 10–11 干预/对照 | 步前 swap；C-layer **开发集** | swap 公式有。科学 CLI 现做几何。offline 路径 `donor_missing`。无 dev 分数则弱层不 decode。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。泄漏/退化区间绿。analyze 常不建 P1。 |
| 13 附录修复 | 新前缀 Prefill；几何/锥 | 四种 dummy 拒；标量 hidden 仍 True。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册 / 阈值无测量有测。 |
| 15 代码任务 | 显式隔离执行器；普通 subprocess ≠ 沙箱 | spy + `isolated_sandbox is False` 已锁。默认仍 Unavailable。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **143 passed，exit 0，19.06s，143 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH。** 声明与复算均为 `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（60 文件）。逐文件 SHA-256 见 §2。 |
| 独立性 | 新真 oracle：题干事件排除、有限 H、科学 `!= donor_missing`、prefix/空 hidden/旗标 Prefill、噪声 bootstrap `lo<hi`、catalog 两别名、下游无 in-dir。**不独立：** offline H e2e、教员强制数字当 generate、offline intervene `unexpressible`、标量 Prefill、r04 `[δ,δ]`、analyze 不读 p1、全 q 的“身份配对”。 |
| Mock/stub | offline 前缀 H + calibrate `scores=None` + analyze 忽略不足 labels + 教员强制 `q =` + `not_evaluated` 编码为成功 + `next(U)` 盖住空行为头。比 `unittest.mock` 更差。 |
| 论文行为仍未证明 | 生成推理上的事件、会做几何的 **offline/Goal e2e**、真向量 Prefill、非退化问题级区间（r04 路径）、从科学 labels 建的 P1、双头不同 Y、隔离执行、T2 reversing |
| 交付 vs 测试 | “143 passed / r06 已本地关闭 / scientific events·步前 H·Prefill·bootstrap 已锁” **超过** 测试力度（题干/NaN/`donor_missing`/ids 那些点除外） |
| 已确认问题？ | **是。** Critical：F7-08。High：F7-01。Medium：F7-04、F7-06、F7-07、F7-09、F7-12。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 空的“看起来没问题”不适用。绿 pytest 不是验收。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷。即使 A–E 全写“通过”，只要 F 确认缺陷，两轮计数必须保持 0；修复后换 hash 重开。 |

在 CE 级测试锁住 Critical/High 项、并且科学路径不再用 `教员强制 q`/`offline 前缀 H`/`标量 hidden` 冒充闭合之前，任何“代码验收通过；独立审查未发现已确认遗留缺陷”的结束句都与本通道证据矛盾。
