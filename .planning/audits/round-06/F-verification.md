# F：验证质量与反向质疑（round-06）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-06 其他通道报告。`ISSUES.md` 只当作者主张；每条声称的 r05 闭合都从测试对生产符号重核，再用进程内反例攻击（未向仓库加测试）。`python -m pytest -q` 绿不是论文正确性，也不是 Goal 验收。

**先行结论：** 冻结哈希 **复算一致（HASH_MATCH）**。本机 `python -m pytest -q` 为 **136 passed / exit 0**。这不是 Goal 通过。r05 之后新增的 16 个节点里，有若干真 oracle（verbalizer `17`/`70`/`boxed{8} also 7` → 0、span 跨界回退 `[]`、analyze 无 `--in-dir` 不写半成品、Week8 有阈值无测量 → `threshold_present_measurement_missing`、Plus 隔离数字、Hotpot 口语答案保持 `requires_independent_truth`）。但作者用来关闭 F5-01 / F5-02 / F5-03 / F5-05 / F5-11 的测试，锁定的仍是**替身**：题干赋值 + 约束 `q = <digit>` 当科学事件；`H.shape[0]==n_events` 当步前 H（本通道 18 行里 **12 行 NaN**）；科学路径 intervene 因 NaN H 落到 `unexpressible`/`donor_missing`，测试只断言 `!= pre_step`；哑 `execute` 只要带 `prefill_hidden` 或 `refilled_prefix` 仍把旗标打成 True；P1 bootstrap 测试不禁 `[δ,δ]`。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：本通道提交已确认缺陷，连续两轮 A–F 通过计数 **不能开始**。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563` |
| 复算聚合 | `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563` |
| 哈希裁决 | **HASH_MATCH** |
| 哈希方法 | 59 个文件：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。按 POSIX `relpath` 排序。`SHA-256.update(relpath.encode() + b"\0" + file_bytes)`。`VERSION.md` 脚本原文。范围内 0 处 CRLF。 |
| 文件数 | 59，与 `round-06/VERSION.md` 一致（r05 为 58；新增 `tests/test_round05_regressions.py`） |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest | **136 passed in 16.54s，exit 0。** Collect：**136 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只出现在 HumanEval/`SubprocessExecutor` 载荷字符串里。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。一处 `@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 范围 | 全部 `tests/**`（16 个 `.py` + 10 个夹具 JSON）及测试导入/CLI 烟测触及的生产符号 |
| 明确未读 | `.planning/audits/round-06/{A,B,C,D,E}-*.md` |

审查对象是**当前工作区字节**。作者 `pytest_author_claim: 136 passed` 仅作为命令结果被独立确认。

## 2. 逐文件覆盖

### 2.1 测试（全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍是 `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 397 | `d3814498fe52b28b…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H）；analyze 无 `--in-dir` 拒 |
| `tests/test_round03_regressions.py` | 291 | `5698a410c0669b61…` | r03 节点；P1 泄漏用例仍绿；`prefix_token_ids` 半边仍要求 `refilled_prefix` |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；科学 prepare 现要求 `events>=1`；几何测试仍走 offline；repair 旗标；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 190 | `83a665a16567884f…` | 16 个新节点；独立与替身混杂（见 §6） |
| `tests/test_science.py` | 101 | `bed01ffa293f2c1f…` | conformal 形状、transfer **形状**、Week8 未注册、verbalizer 可见性、repair 拒答半边 **仍锁旗标 True**、swap |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only：**136 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r05 的 120 节点：+16，全部在 `tests/test_round05_regressions.py`。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、precomputed、P2 分母、P3 回声、Week8 零 excess / 阈值无测量、bootstrap **键名**、BOW retrieval、PCA Procrustes | 留出泄漏 oracle；bootstrap **非退化区间**；Gate **阈值比较**；`procrustes` 无直接测试 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 抽答案相等（17/70/boxed 已锁）；无 generate 拒答；dev 阈值区间 | `attention_mean`/`attention_rollout` 仅 CLI 烟测写入，无数值 oracle |
| `cli.py` | 1052 | `45a11e124b1dda8c…` | smoke offline；scientific prepare/collect/repair；resume；analyze 文件/无 in-dir 拒 | 科学 **NaN H** 未断言；tiny intervene 科学路径 `unexpressible`；analyze 读 labels 仍常 `p1 is None` |
| `edits.py` | 277 | `bfd1632b50504c04…` | value/rename/op-reverse/5.5；source-value 元数据旗标 | 同值异源是否真改源 |
| `events.py` | 261 | `20c57f55ec3c3571…` | 身份对齐；monotonic；open-think；`parse_events` 手写 `"p1 = 4. p2 = 0.\\nq = 9"` | 科学文本的 p1/p2 来自**题干**；`scanned` 仍是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False`；子进程超时 | 宿主 CPython 子进程 ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP/范数 | CLI C-layer 无 `--dev-layer-scores` → `dev_scores_missing` + 硬编码 layer=1 |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 342 | `a6bcd893abedaf3b…` | 事件均值；空 N；`noise_evaluated` 单元 | `soundness_claim_allowed` 恒 False |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 192 | `b9e14fcbc92d2743…` | 行数==事件数；拒 offline | 无 token 的 pre_step 写成 NaN 仍标 `h_position=pre_step`；`intervene_swap_decode` 的 `timing=pre_step` 不进 CLI 行字段 |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 191 | `f92f3ba61ec735fb…` | replay/greedy；scientific 调 `generate_task_trace` | 后缀乱码；`append_target_assignment` 教员强制；`apply_model_template` 无测试 |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` **实现了、未断言** |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | n=3→1；contained；跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 95 | `52de70553b37dec6…` | σ / λ_FN | CLI 双头同 Y |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号已锁；`status==ok`+shape | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；`truth_indices` | smoke `scores=None` |
| `repair.py` | 217 | `2600cd013d444662…` | 无 hidden 的哑 execute → False；`task_oracle` 掩码 `q = ?` | 空列表/`0`/`refilled_prefix` 旗标仍 True；`prefix_token_ids` 无条件 True |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | `Event.from_dict` extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 111 | `35cd0e3f724ee850…` | Plus→test；`gsm_family_id` | `assert_disjoint` **零测试** |
| `tasks/catalog.py` | 45 | `80e4db4b0241b919…` | **零测试** | `load_snapshot` / aliases |
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
| 冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `dc2ba459…`（59 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 全量 pytest | 仓库根 `python -m pytest -q`（`pythonpath=src`） | **136 passed in 16.54s，exit 0**。无 skip/xfail/deselected。 |
| Collect | `python -m pytest tests --collect-only -q` | 136 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM `4*3 % 23 = 12`；sidecar 8；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]`；BCE 符号 | **存在的单元断言**与独立算术一致 |
| 对抗：fixture 八阶段 | prepare→…→analyze，`--backend offline` | `H=[[1..8]]`；双头 **同一 loss** `0.05036…`；calibrate `scores=None`；intervene `unexpressible`/`donor_missing`；repair `refilled_prefix=False` / `generated_tokens=0`；analyze `p1 is None` / `not_evaluated` |
| 对抗：scientific prepare | `--eval-mode scientific --sham-opportunities 1` | 6 条轨迹 **各 3 事件**（非空）。文本例：`p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82`。p1/p2 来自**题干**；`q` 来自教员强制 `append_target_assignment`。decode 后缀不可解析。sham 3 条，`premise_id` 为 p1/p2/q。仅对题干 `parse_events` 已得 p1、p2。 |
| 对抗：scientific collect tiny | 同上 + collect tiny | `H`/`H_pre_step` 形 `(18,32)`（= 事件数）。**NaN 比例 2/3**。p1/p2：`token_index=None`，`expressible=False`。q：index 44 ≠ last 50，有限。`h_position` 仍写 `pre_step`。 |
| 对抗：tiny intervene（作者测试路径） | scientific collect 后 `--backend tiny` | **`timing=unexpressible`，`status=donor_missing`**，`hook_timing=None`。因 H[0]/H[1] 皆 NaN，`allclose(..., equal_nan=True)` 为真，几何/hook 不跑。`test_intervene_tiny_geometry_timing_stays_offline` 只断言 `!= pre_step`，**绿在替身上**。 |
| 对抗：tiny intervene（有限异 H） | 手写 `H=ones/twos` | `timing=offline_hidden`，`status=prospective_decode`。实现上 hook **没有**把行字段改成 `pre_step`。作者测试碰不到这条路径。 |
| 对抗：哑 execute | 见 §8 CE-5 | 无 hidden/旗标 → False（作者测试锁这个）。`prefill_hidden=[]` / `refilled_prefix=True` / `prefill_hidden=0` / `prefix_token_ids=[…]` → **仍 True**。 |
| 对抗：verbalizer | gold=`7` | `answer 7`→1.0；`17`→0；`70`→0；`\boxed{8} also 7`→0。**r05 子串 CE 不再复现。** |
| 对抗：P1 bootstrap | 作者 r05 数据 | `δ=0.56`，区间 `[0.112, 0.891]`，`status=resampled_delta_auc`。**不是** `[δ]*n` 实现。r04 完美 ρ=y 数据仍得 **`[0.5, 0.5]`**。测试只要求 `lo<=hi` 与 `n>=1`，`[δ,δ]` 仍绿。 |
| 对抗：span 跨界 | `[[0,2],[2,6]]` × `[1,3]` | **`[]`**。overlap-only 亦 `[]`。n=2 readout 拒。 |
| 对抗：analyze 无 in-dir | scientific 无 `--in-dir`；`--in-dir` 文件 | 先拒，**不写** `report.json`。 |
| 对抗：analyze + scientific labels | prepare scientific → label → analyze | `p1 is None`，`status=not_evaluated`。二元 `task_label` 只有 3 条（门限 ≥4）。测试只锁 `scientific_conclusion is None`。 |
| 对抗：账本 | 解析 `PAPER_TRACEABILITY.md` 528 行 TR | `verification_method=python -m pytest -q`：**69 行**。`local_verify_status=passed_local_tests`：**320 行**。`executable_function`：**159 行**均为 `tests_exist_not_acceptance`（0 行 `passed_local_tests`）。页眉写不得用 pytest 关闭可执行行；协议行仍用 pytest 关闭。 |
| 对抗：k repair | `consecutive_repairs` + tiny | k=1..5 slots 增长；`generated_tokens` 全 4，`extra_prefill` 全 19，`refilled_prefix` 全 True。 |
| 对抗：Week8 | `{gate0:0.9}` 无测量 | `threshold_present_measurement_missing`。有测量则 `compared`。零 excess 仍 `c3_negative_descriptive`。 |
| 对抗：Plus / Hotpot | 与作者测试相同构造 | `13` 保留、无 `19`；`needs_truth` / `requires_independent_truth`。 |
| 对抗：transfer | `src=I`，`tgt=diag(2,3,4,5)` | `apply_map` **不**恢复 I（maxabs≈2.50）。套件只查 shape。 |
| 对抗：P1 泄漏 | 作者 ρ=y 全行 | `auc_full=1`，`delta=0.29`。现测试仍绿。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-06 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 136 passed | `VERSION.md` L26 | **命令是。** 当作阶段/Goal 证据：**否。** |
| r05 已在本地关闭，待独立复核 | `ISSUES.md` | **部分。** verbalizer 抽答案、span 跨界、analyze 入口、Week8 阈值无测量、Plus 隔离、Hotpot 口语、无 hidden 的哑 execute、有限 H 上 timing 保持 `offline_hidden`——单元或实现成立。A5-01 事件来源、A5-08/F5-02 科学路径 timing、A5-09/F5-03 Prefill 旗标、A5-03/F5-05 bootstrap 非退化、A5-02/F5-11 账本行级 pytest、F5-01 e2e **未闭。** |
| scientific generate / 步边界 H / Prefill / 重采样区间 / 诚实账本 | `ISSUES.md` A5-01/08/09/03/02 | 测试存在。锁的是非空事件、行数、无 hidden 的那一种 dummy、`lo<=hi`、可执行行的 `tests_exist_not_acceptance`。 |
| CLI 流水线消费上游 | `test_full_cli_smoke`；`test_pipeline_consumes_upstream` | 文件被读。科学没有：offline H、`scores=None`、analyze 忽略不足以建 P1 的 labels。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham∉R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 **span**（不是答案证明）；B-11 空父母；B-13 `family_id`；B-14 source=/test_only + 生产 key；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]` + `predict_set`；bilinear σ/λ_FN；spy.calls / `exec(`；E-17 labels-dir hash；Boundary BCE 符号；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess + 未注册 Gate；gsm 家族键；monotonic 版本；resume 不覆盖成功 manifest；`truth_indices`；analyze 文件入口。

**本冻结新增且独立：**

- `test_verbalizer_uses_extracted_answer_not_substring`：`17`/`70`/`boxed{8} also 7` → 0。本通道独立复现。**A5-07 / F5-04 作为实现+该 CE 闭合。**
- `test_span_no_straddle_fallback`：`[1,3]` → `[]`。本通道独立复现。**F5-06 实现+该 CE 闭合。**
- `test_readout_rejects_empty_band`：n=2 抛 `60-75`。
- `test_week8_threshold_without_metric_is_not_evaluated`：`{gate0:0.9}` → `threshold_present_measurement_missing`。本通道独立复现。**F5-08 该分支闭合。**
- `test_plus_numeric_edit_is_isolated_token`：`13` 在、`19` 不在。本通道独立复现。**B5-02 单元闭合。**
- `test_hotpot_spoken_answer_stays_unverified`：`needs_truth` / `requires_independent_truth`。**B5-03 单元闭合。**
- `test_analyze_requires_directory` / `test_e04` 无 `--in-dir`：先拒、无 `report.json`。本通道独立复现。**E5-14 / F4-17 入口闭合。**
- `test_dummy_execute_is_not_prefill` 的 **无 hidden 半边**：`{"generated_ids":[1],"extra_prefill_tokens":0}` → False。只锁这一种 dummy。
- `test_common_dim_is_not_silent_truncate`：4×3 → PCA、`truncated is False`。
- `test_retrieval_scatter_marks_bow_fallback`：BOW 降级旗标。
- `test_parse_events_reads_premises_and_target`：手写含 `q = 9` 的文本。

### 6.2 无效、自指或过弱（含本轮点名的替身）

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_full_cli_smoke` | **offline H 当成功。** 本通道复现 `H=[[1..8]]`、`scores=None`、`p1 is None`。仍断言 `scientific_conclusion is None`。 |
| `test_e04_analyze_manifest_includes_report` | 空目录 analyze → `not_evaluated` 编码为成功。 |
| `test_pipeline_consumes_upstream` / `test_fit_hashes_labels_dir` | 停在 fit；offline 前缀 ID 上任意有限 loss 都过。双头同 loss。 |
| `test_analyze_uses_p1_table` | 只要求 `p1 is not None`。手写 `p1_table.jsonl`。不读 `labels.jsonl`。 |
| `test_analyze_uses_labels_or_stays_null` | 只锁 `scientific_conclusion is None` 与 Gate `unregistered`。**不读 `p1`。** 本通道 scientific labels → `p1 is None`。 |
| `test_scientific_prepare_emits_parseable_events` / `test_scientific_prepare_is_generated_not_node_values` | 只禁管道串、要求 `events>=1` 与存在 `q`。题干 `p1 = 4` 已能解析；`q` 由约束解码教员强制。**不要求 decode 后缀可解析。** |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 只比 `H.shape[0]==n_events`。不比有限、不比 token≠last。本通道 12/18 行为 NaN。全 NaN 只要行数对也会绿。 |
| `test_scientific_collect_span_pool_and_refuses_offline` 的成功半边 | `E` 两行不等 + 有 `H_pre_step` 键。拒 offline 半边独立。 |
| `test_intervene_tiny_geometry_timing_stays_offline` | **科学路径 timing=`unexpressible`。** 断言 `!= pre_step` 与 r04 offline `unexpressible` 是同一替身。 |
| `test_intervene_geometry_is_not_pre_step` | 仍走 offline 单行 H → `unexpressible`。 |
| `test_dummy_execute_is_not_prefill` 的成功半边 | 只锁一种 dummy。空 `prefill_hidden` / 旗标仍 True。 |
| `test_repair_tiny_prefills_and_masks_differ` / `test_repair_k_changes_masked_prefix` / `test_scientific_repair_runs_k_1_to_5` | 要求 `refilled_prefix` 全 True。k 不改 generated/extra_prefill。 |
| `test_repair_reprefills_and_refuses_gate` 有 `prefix_token_ids` 半边 | **把无 Prefill 的 True 锁成期待。** |
| `test_p1_bootstrap_resamples_delta_auc` | 只要求 `status==resampled_delta_auc`、`lo<=hi`、`n>=1`。`interval=[δ,δ]` 仍过。 |
| `test_p1_returns_bootstrap_interval` | 只要求 interval 非空。r04 数据本通道仍是 `[0.5,0.5]`。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_p1_precomputed_is_scores_not_magic` | `length==ρ` 时旧魔术 Δ 也是 0。 |
| `test_direct_transfer` / labeled map | 形状。本通道 `apply_map` 不恢复 I。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。last-token / once 未测。 |
| `test_align_equal_count_*` `scanned is False` | 镜像硬编码常量。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |
| `test_calibrate_infinity_is_json_safe` | `q is None or isinstance(q,(int,float))` 几乎恒真。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline（F6-08 / 遗留 F5-01）。** `H`←`token_ids[:8]`；无 `--features-dir` 则 `scores=None`；analyze 标签不够建 P1；smoke **要求** 空结论。
2. **scientific 事件非空，来源是题干+教员强制（F6-01）。** `generate_task_trace` 把题干交给 `parse_events`（已有 `p1 = 4`），再 `append_target_assignment` 写 `\nq = <logits digit>`。测试把它当“可解析 generate”。
3. **步前 H 用行数冒充（F6-02）。** 事件在 char 0 时 `boundary_index` 为空 → NaN 行仍 `h_position=pre_step`。collect 只拒“零行或非 pre_step 名”。
4. **几何测试躲开了会做几何的 H（F6-03）。** 科学 H 前两行 NaN → `donor_missing`。有限异 H 时实现写 `offline_hidden`，但关闭测试不走那条。
5. **`refilled_prefix` 仍是键存在（F6-04）。** `prefilled = bool(refilled_prefix) or prefill_hidden is not None`。空列表与 `0` 都算有 hidden。`prefix_token_ids` 无条件 True。
6. **P1 测试锁名字与不等式方向（F6-05）。** 实现会重算 ΔAUC（好）。测试不锁区间宽度。
7. **账本页眉与可执行行 status 改善，协议行仍 pytest（F6-06）。**
8. **HumanEval spy / Child 非沙箱仍成立。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`card`、`catalog.load_snapshot`、`apply_model_template`。`clone_cache` 本冻结生产树中 **不存在**。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 科学 prepare 的事件必须来自生成，或拒绝宣称 generate

- 构造：`prepare --eval-mode scientific` + `t1_tiny`（题干已含 `p1 = 4. p2 = 0.`）。
- 期望：decode 后缀可解析出步骤；或 `parse_status=parse_failed` 且 prepare 拒。仅题干赋值不得算科学轨迹事件。教员强制 `q = <digit>` 不得单独满足“有 q 事件”。
- 当前：events=3，obs=12，sham 有 premise_id。文本含乱码 + `\nq = 82`。仅题干已得 p1、p2。
- `test_scientific_prepare_*` **绿**。

### CE-2 步前 H 必须有限且不是末 token

```text
scientific collect: H.shape == (18, 32)
NaN 比例 = 2/3
p1/p2: token_index is None  → 现测试只比行数，绿
q: index 44 ≠ last 50        → 实现有，测试没锁
全 NaN 但 n_events>1 的 H    → 现测试会绿
```

### CE-3 科学 tiny intervene 必须做几何，或拒绝；不得用 unexpressible 满足 `!= pre_step`

```text
作者路径（scientific H，前两行 NaN）：timing=unexpressible, status=donor_missing
  → test_intervene_tiny_geometry_timing_stays_offline 绿
有限异 H：timing=offline_hidden, status=prospective_decode
  → 实现已不把行字段改成 pre_step；关闭测试碰不到
```

### CE-4 CLI analyze 必须消费 labels 或拒绝

- 构造：scientific prepare+label（本通道 3 条二元 task_label）后 analyze。
- 期望：拒绝，或用这些 labels 给出冻结 P1。
- 当前：exit 0，`p1 is None`。`test_analyze_uses_labels_or_stays_null` **要求** 空结论。

### CE-5 Prefill 不是旗标 / 空 hidden

```text
execute={generated_ids:[1], extra_prefill:0}     → False   作者测试锁这个
execute={generated_ids:[1], prefill_hidden:[]}   → True    现测试绿
execute={generated_ids:[1], refilled_prefix:True}→ True
execute={generated_ids:[1], prefill_hidden:0}    → True
run_repair(..., prefix_token_ids=[1,2,3])       → True    test_science 锁这个
```

### CE-6 P1 bootstrap 非退化

```text
r05 噪声数据：interval [0.11, 0.89]   实现会重算
r04 ρ=y 常数 length：interval [0.5, 0.5]
test_p1_bootstrap_resamples_delta_auc：lo<=hi 即可
应：在会变化的数据上 lo < hi，或断言重采样后的 δ 不全等
```

### CE-7 verbalizer / span / analyze 入口（本轮攻击失败 = 闭合）

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
页眉声明 ≠ 行级清零
```

## 9. 发现

### F6-00 声明冻结哈希可复算

- **严重度：** —
- **状态：** 非缺陷建议（本轮过程正确）
- **文件：** `.planning/audits/round-06/VERSION.md` L5–23；工作区 59 文件
- **复现：** §1。本地 `dc2ba459…` == 声明。0 CRLF。
- **注：** 夹具仍在摘要外（F6-12）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F6-01 科学“可解析事件”测试锁住题干赋值 + 教员强制 `q = <digit>`

- **严重度：** High
- **状态：** confirmed defect（验证；空事件实现洞已不复现）
- **文件/行：** `tests/test_round05_regressions.py` L23–51；`tests/test_round04_regressions.py` L30–64；`models/generate.py` `generate_task_trace` L105–182、`append_target_assignment` L72–98；`events.py` `parse_events` L75–89；`cli.py` `cmd_prepare` L278–292
- **触发：** `prepare --eval-mode scientific` + `t1_tiny`
- **要求：** Goal §五.1/§五.3；作者 A5-01 / F5-01“parseable events / generate appends constrained target”
- **复现：** §3。6 轨迹各 3 事件。仅题干已解析 p1/p2。`q` 来自约束 2 位数字，不是自由 decode。后缀 `Z*H[!XTC` 不可解析。
- **影响：** 可以引用“科学 prepare 事件非空已锁”，同时轨迹没有模型生成的推理步骤。
- **修复：** CE-1；禁止把题干 `p1 = 4` 与教员强制行当成 generate 闭合。
- **作者主张 A5-01 / F5-01 / F5-07：** **部分**（空事件 CE 不再复现；来源仍是替身）

### F6-02 `H.shape[0]==n_events` 不是步边界；2/3 行为 NaN

- **严重度：** High
- **状态：** confirmed defect（验证；兼实现：无 token 仍标 `pre_step`）
- **文件/行：** `tests/test_round05_regressions.py` L54–64；`models/collect.py` L55–66；`cli.py` L448–450；`models/features.py` L23–34
- **要求：** Goal §五.6；作者 A5-01“collect refuses last-token `pre_step`”；E5-12 stacked `H_pre_*`
- **复现：** 18 行 H，NaN 比例 2/3。p1/p2 `expressible=False`。collect 只要事件列表非空就把 `h_position` 写成 `pre_step`。
- **修复：** CE-2；无 expressible 步前应拒或显式 `inexpressible`，不得计入步前矩阵。
- **作者主张 A5-01 / E5-12：** **部分**（行数对齐、跨轨迹堆叠在；不是论文步前）

### F6-03 科学 tiny intervene 测试仍锁 `unexpressible` 替身

- **严重度：** High
- **状态：** confirmed defect（验证）
- **文件/行：** `tests/test_round05_regressions.py` L115–124；`cli.py` L707–786
- **触发：** 作者自己的 scientific collect → intervene tiny
- **要求：** Goal §五.6/§五.10；作者 A5-08 / F5-02
- **复现：** 行字段 `timing=unexpressible`，`status=donor_missing`。测试 `!= pre_step` 绿。有限异 H 时实现写 `offline_hidden`（本通道独立跑到），**关闭测试不覆盖**。
- **影响：** 与 r05 F5-02 同类：可以引用“已锁几何不是 pre_step”，同时论文关心的科学路径根本没做几何。
- **修复：** CE-3；测试必须用有限、互异、会触发 geometry/hook 的 H。
- **作者主张 A5-08 / F5-02 / D5-04：** **未闭合**（测试选了不会触发几何的科学产物）

### F6-04 哑 execute 仍能把 `refilled_prefix` 打成 True

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）
- **文件/行：** `repair.py` L138–175；`tests/test_round05_regressions.py` L85–89；`tests/test_science.py` L76–82
- **要求：** Goal §五.13 / REPAIR-01；作者 A5-09 / F5-03
- **复现：** §3 CE-5。作者锁的那种 dummy 为 False。`prefill_hidden=[]`、`refilled_prefix=True`、`prefill_hidden=0`、`prefix_token_ids` 均为 True。`test_science.py` 仍断言后一条为 True。
- **修复：** 只有真实 Prefill hidden（非空、来自模型前向）才能标 True；删掉或改掉把旗标锁成成功的测试。
- **作者主张 A5-09 / F5-03：** **未闭合**

### F6-05 P1 bootstrap 测试不禁 `[δ,δ]`

- **严重度：** High
- **状态：** confirmed defect（验证；实现已会重算 ΔAUC）
- **文件/行：** `analysis.py` `_bootstrap_p1` L196–212；`tests/test_round05_regressions.py` L92–107；`tests/test_round04_regressions.py` L192–200
- **要求：** Goal §五.12；作者 A5-03 / F5-05
- **复现：** 作者 r05 数据区间有宽度。r04 ρ=y 数据区间 `[0.5,0.5]`。测试 `lo<=hi` 对两者都绿。
- **修复：** CE-6。
- **作者主张 A5-03 / C5-M-01 / F5-05：** **部分**（不是 `[δ]*n` 常数实现；测试仍接受退化区间）

### F6-06 账本仍用 `pytest -q` / `passed_local_tests` 关闭行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：69 行 `verification_method=python -m pytest -q`（TR-0002 等协议行）；320 行 `local_verify_status=passed_local_tests`。可执行行 159 条已改为 `tests_exist_not_acceptance`。`.planning/phases/06-acceptance/06-VERIFICATION.md` L8 现写 136 passed **不是** Goal（比 r05 的“65 passed”诚实）。
- **要求：** Goal §九.1；作者 A5-02 / F5-11“executable rows no longer treat pytest as acceptance”
- **复现：** §3。页眉禁止 ≠ 行级清零。
- **作者主张 A5-02 / F5-11：** **部分**（可执行行 status 字段改了；协议行仍用 pytest 关闭）

### F6-07 analyze 标签测试不锁 P1；科学路径 p1 仍为 None

- **严重度：** Medium
- **状态：** confirmed defect（验证）
- **文件/行：** `tests/test_round05_regressions.py` L181–190；`cli.py` `cmd_analyze` L845–889
- **复现：** scientific labels 仅 3 条二元 `task_label`（门限 4）→ `p1 is None`。测试不读 `p1`。
- **作者主张 A5-11：** **未闭合**（无 `predict_matrix` / PR/F1 测试；`probe_prf1` 零提及）

### F6-08 CLI / Goal e2e 仍接受未接通科学路径

- **严重度：** Critical
- **状态：** confirmed defect（验证）
- **文件/行：** `tests/test_cli_pipeline.py` L4–30；`cli.py` offline collect / analyze
- **复现：** §3 fixture 八阶段。与 F5-01 e2e 同类。
- **作者主张 F4-01 / F5-01 e2e：** **未闭合**

### F6-09 双头同 Y、k 不改 token 预算、apply_map 只查形状

- **严重度：** Medium
- **状态：** confirmed defect（验证）
- **复现：** offline 两头 loss 同为 `0.05036…`。scientific k=1..5 生成数全 4、extra_prefill 全 19。`apply_map` 不恢复 I，套件只查 shape。
- **作者主张 A5-11 双头 / A5-09 k 增长：** **部分**（slots 集合有变化；预算与 Y 未锁）

### F6-10 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes`、`assert_disjoint`、`card`、`catalog.load_snapshot`、`apply_model_template`
- **注：** `clone_cache` 本冻结源树中不存在，不再记为零提及。

### F6-11 Week8 / verbalizer / span / analyze 入口 — 本轮攻击未复现

- **严重度：** —
- **状态：** 非缺陷建议（这些 r05 CE 作为实现+独立 oracle 闭合）
- **复现：** §3 CE-7。不要把本条写成 Goal 验收。

### F6-12 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`；`VERSION.md` 范围
- **影响：** oracle 字节可动而不改 `.py`+toml 聚合

### F6-13 ISSUES `author closed` 高估验证闭合

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为单元验证闭合：** F5-04 子串 CE（17/70/boxed）；F5-06 跨界 `[]`；F5-08 阈值无测量；F4-17 / E5-14 analyze 入口；B5-02 Plus 隔离；B5-03 Hotpot 口语；无 hidden 的那一种 dummy；有限 H 上 hook 不把行 timing 改成 `pre_step`（无测试锁住）；P1 实现会重采样（测试不锁宽度）；前轮 B-01–14/23/24、C3-M-01/03/07、D-08、E-17、bilinear、spy、BCE、Child 非沙箱等。
- **未闭（错或镜像）：** A5-01 事件来源（F6-01）；步前 H 行数替身（F6-02）；A5-08 科学路径 `unexpressible`（F6-03）；A5-09 旗标 Prefill（F6-04）；A5-03 退化区间测试（F6-05）；A5-02 账本协议行 pytest（F6-06）；A5-11 analyze P1/PR（F6-07）；F5-01 e2e（F6-08）。
- **不要用本通道把 Goal/需求标 Complete。** 上表单元闭合 ≠ 科学验收。作者关闭无效。

### F6-14 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、`offline_prefix_ids`、宿主 `subprocess`、`executor_unavailable` 不得改写成服务器验收。题干+教员强制事件也 **不是** pending_server，是本机验证缺口。

### F6-15 非缺陷说明

- **状态：** 非缺陷建议
- `VERSION.md` 算法可复现。保持脚本冻结。
- 相对本通道 r05：verbalizer 抽答案、span contained-only、analyze 入口、Week8 阈值树、Plus 隔离、Hotpot 旗标、P1 真重采样实现、有限 H 上 timing 不改名——这些是真改进。
- `consecutive_pass_count: 0` 与“136 passed ≠ Goal”比把套件当验收更诚实。
- last-token hook、`once=True` 看起来已实现；缺测试，故不闭。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**当前测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 69 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F6-06）。反向覆盖失败（F6-10）。科学行被题干+强制数字“填绿”（F6-01）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F6-01、F6-02、F6-03、F6-04、F6-05、F6-08 为已确认遗留。ISSUES 作者关闭无效。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 136/0，无 skip 伪装。e2e 是 exit-code 烟测并断言空结论。科学路径有测试，但锁替身。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 现写 136 不是验收（好）。账本协议行仍 `passed_local_tests`（坏）。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 哈希匹配（好）。`VERSION.md` `consecutive_pass_count: 0`。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。只补审查日志不改变被审 hash——本文件属于审查日志，不改变 59 文件摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：题干事件、NaN 步前 H、`unexpressible` 替身、Prefill 旗标、offline 前缀 H、宿主 subprocess 都是 **有名字的代码** 缺口。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F6-13）。本机 pytest 记录存在（136/0）。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自题干+强制行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 解析器吃题干 `p1 = 4`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。scientific sham 现有 premise_id（比 r05 好）。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。collect 把不可表达步前写成 NaN 并计入 H。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。双头同 Y。rollout 无数值测试。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。smoke `scores=None`。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒有。数值恢复未锁且本通道不恢复。 |
| 10–11 干预/对照 | 步前 swap；C-layer **开发集** | swap 公式有。科学 CLI 路径 `donor_missing`。无 dev 分数。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。泄漏/退化区间绿。analyze 常不建 P1。 |
| 13 附录修复 | 新前缀 Prefill；几何/锥 | 一种 dummy 拒；空 hidden/旗标仍 True。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册 / 阈值无测量有测。 |
| 15 代码任务 | 显式隔离执行器；普通 subprocess ≠ 沙箱 | spy + `isolated_sandbox is False` 已锁。默认仍 Unavailable。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **136 passed，exit 0，16.54s，136 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH。** 声明与复算均为 `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（59 文件）。逐文件 SHA-256 见 §2。 |
| 独立性 | 新真 oracle：verbalizer 17/70/boxed、span `[]`、n=2 readout 拒、Week8 阈值无测量、Plus 隔离、Hotpot 口语、analyze 无 in-dir、无 hidden dummy、PCA 不截断、BOW 降级旗标。**不独立：** offline H e2e、题干+强制数字当 generate、行数当步前 H、科学 intervene `unexpressible`、空 hidden Prefill、`[δ,δ]` bootstrap、`prefix_token_ids` 旗标。 |
| Mock/stub | offline 前缀 H + calibrate `scores=None` + analyze 忽略不足 labels + repair 旗标 + 教员强制 `q =` + `not_evaluated` 编码为成功。比 `unittest.mock` 更差。 |
| 论文行为仍未证明 | 生成推理上的事件、有限步前 H、会做几何的科学 intervene、真 Prefill、非退化问题级区间、从 labels 建的 P1、隔离执行、T2 reversing |
| 交付 vs 测试 | “136 passed / r05 已本地关闭 / scientific events·步前 H·Prefill·bootstrap 已锁” **超过** 测试力度 |
| 已确认问题？ | **是。** Critical：F6-08。High：F6-01、F6-02、F6-03、F6-04、F6-05。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 空的“看起来没问题”不适用。绿 pytest 不是验收。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷。即使 A–E 全写“通过”，只要 F 确认缺陷，两轮计数必须保持 0；修复后换 hash 重开。 |

在 CE 级测试锁住 Critical/High 项、并且科学路径不再用 `unexpressible`/`NaN H`/`教员强制 q`/`空 hidden` 冒充闭合之前，任何“代码验收通过；独立审查未发现已确认遗留缺陷”的结束句都与本通道证据矛盾。
