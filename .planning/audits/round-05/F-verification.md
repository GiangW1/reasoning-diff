# F：验证质量与反向质疑（round-05）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-05 其他通道报告。`ISSUES.md` 只当作者主张；每条声称的 r04 闭合都从测试对生产符号重核，再用进程内反例攻击（未向仓库加测试）。`python -m pytest -q` 绿不是论文正确性，也不是 Goal 验收。

**先行结论：** 冻结哈希 **复算一致（HASH_MATCH）**。本机 `python -m pytest -q` 为 **120 passed / exit 0**。这不是 Goal 通过。r04 之后新增的 23 个节点里，有若干真 oracle（Boundary BCE 符号、P2 无集合分母、`ChildProcessExecutor` 非沙箱、无 `generate_fn` 的 verbalizer 拒答、scientific 拒 offline、resume 不覆盖成功 manifest、analyze 文件入口不写半成品）。但作者用来“关闭 F4-01 / A4-01–04 / A4-06”的科学路径测试，锁定的是**替身**：offline 前缀 ID 当 H、零事件 decode 当 generate、`refilled_prefix=True` 当 Prefill、子串命中当 verbalizer、`precomputed` 当正文 P1、offline `unexpressible` 当“几何不是 pre_step”。独立跑 scientific prepare→tiny collect→tiny intervene 时，6 条轨迹 **事件数全为 0**，而 intervene 仍把 `timing` 写成 **`pre_step`**。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：本通道提交已确认缺陷，连续两轮 A–F 通过计数 **不能开始**。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4` |
| 复算聚合 | `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4` |
| 哈希裁决 | **HASH_MATCH** |
| 哈希方法 | 58 个文件：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。按 POSIX `relpath` 排序。`SHA-256.update(relpath.encode() + b"\0" + file_bytes)`。范围内 0 处 CRLF。 |
| 文件数 | 58，与 `round-05/VERSION.md` 一致（r04 为 56；新增 `models/tokenize.py`、`tests/test_round04_regressions.py`） |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest | **120 passed in 13.11s，exit 0。** Collect：**120 nodes**。无 skip/xfail/deselected/`unittest.mock`/`assert True` 断言。一处未用 `monkeypatch`。一处 `@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 范围 | 全部 `tests/**`（15 个 `.py` + 10 个夹具 JSON）及测试导入/CLI 烟测触及的生产符号；其余生产模块扫未测入口 |
| 明确未读 | `.planning/audits/round-05/{A,B,C,D,E}-*.md` |

审查对象是**当前工作区字节**。作者 `pytest_author_claim: 120 passed` 仅作为命令结果被独立确认。

## 2. 逐文件覆盖

### 2.1 测试（全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 29 | `0cedc6188e5f64b1…` | 八阶段 exit 0 + `report.status==not_evaluated`；collect 仍是 `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 394 | `37414926677d0596…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 291 | `5698a410c0669b61…` | r03 节点；P1 泄漏用例仍绿；`run_repair` 无 execute → `refilled_prefix is False` |
| `tests/test_round04_regressions.py` | 310 | `93f04cc13c39d6b0…` | 23 个新节点；独立与替身混杂（见 §6） |
| `tests/test_science.py` | 101 | `bed01ffa293f2c1f…` | conformal 形状、transfer **形状**、Week8 未注册、verbalizer 可见性、repair 拒答、swap |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only：**120 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。`assert True` 只出现在 HumanEval/`SubprocessExecutor` 载荷字符串里。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r04 的 97 节点：+23，全部在 `tests/test_round04_regressions.py`。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 283 | `3593254605792c6e…` | P1 门、ρ 探测、precomputed 作者例、P2 分母、P3 回声、Week8 子串/零 excess、cone `r2>0.9`、bootstrap **非空** | 留出泄漏 oracle；bootstrap **重算 AUC**；Gate **阈值比较**；`procrustes`/`retrieval_scatter` 无直接测试 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 120 | `f99d32f1e5c59e48…` | verbalizer 无 generate 拒答；dev 阈值区间 | **子串计分仍在**（L119）；`attention_mean`/`attention_rollout` 零测试 |
| `cli.py` | 893 | `b1d801f16bc651e2…` | smoke offline；scientific prepare/collect/repair；resume；analyze 文件拒 | scientific **零事件**未断言；tiny intervene 写 `timing=pre_step`；analyze 读 labels 仍无 P1 |
| `edits.py` | 277 | `bfd1632b50504c04…` | value/rename/op-reverse/5.5；source-value **元数据旗标** | 同值异源是否真改源、未改值 |
| `events.py` | 196 | `2ac8624cc77bdf6f…` | 身份对齐；monotonic 版本；open-think | `scanned` 仍是常量；scientific 文本 **解析不出事件** |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False`；子进程超时 | 宿主 CPython 子进程 ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP/范数 | CLI C-layer 无 `--dev-layer-scores` → `dev_scores_missing` + 硬编码 layer=1 |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 342 | `5102a7dd0a2d0e99…` | 事件均值；空 N；`noise_evaluated` 单元 | scientific 路径 **没有 labels/obs**；`soundness_claim_allowed` 恒 False |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 183 | `509ba704c6c67a03…` | flags；CLI tiny 有 `H_pre_step` 键 | 无事件时 H=末 token；`intervene_swap_decode` 写 `timing=pre_step` |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 143 | `b236dbb63239ddd7…` | replay/greedy；scientific 调 `generate_task_trace` | 生成后缀不可解析；`apply_model_template` 无测试 |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` **实现了、未断言** |
| `models/tokenize.py` | 32 | `1bb7d6cf19171a90…` | n=3→1；contained span | n=2 落到 100% 层；**跨界回退**未测 |
| `probes/bilinear.py` | 95 | `52de70553b37dec6…` | σ / λ_FN | CLI 双头同 Y |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号已锁；`status==ok`+shape | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；`truth_indices` | `+1e-12`；smoke 仍 `scores=None` |
| `repair.py` | 189 | `418d804da3da8bf0…` | `repairability(4,10)`；有 execute → 旗标 True | **任意 execute 都标 Prefill**；`task_oracle` 不改前缀 |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | `Event.from_dict` extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 110 | `f8b08a69810e3244…` | Plus→test；`gsm_family_id` | `assert_disjoint` **零测试** |
| `tasks/catalog.py` | 39 | `5d3918394b1603bb…` | **零测试** | `load_snapshot` |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 79 | `e1a2b40981528571…` | family / test-only | `"reversing operation"` 仍非 T4；**无测试** |
| `tasks/t2_gsm_symbolic.py` | 84 | `b50db6533f18948d…` | sidecar | 无 sidecar 占位前提 |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` **实现了、未断言** |
| `tasks/t3_hotpot.py` | 104 | `baa832df54813875…` | support≠DAG | `new_answer` 回写未断言 |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 63 | `d72e1dd1c4192b09…` | 4096/3584；labeled 需标签；**形状** | `apply_map(tgt)≈src` 实现已恢复，**未断言** |

夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `4c8769f3…`（58 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 全量 pytest | 仓库根 `python -m pytest -q`（`pythonpath=src`） | **120 passed in 13.11s，exit 0**。无 skip/xfail/deselected。 |
| Collect | `python -m pytest tests --collect-only -q` | 120 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM `4*3 % 23 = 12`；sidecar 8；TO 0.5；σ(1)；10·(-log 0.8)；`repairability=0.6`；`[0.7,0.4]`；BCE 符号 | **存在的单元断言**与独立算术一致 |
| 对抗：fixture 八阶段（测试路径） | prepare→…→analyze，`--backend offline` | `H=[[1..8]]`，`weight_source=offline_prefix_ids`；双头 **同一 loss** `0.05036…`；calibrate `scores=None`；intervene `timing=unexpressible` / `donor_missing`；repair `refilled_prefix=False` / `generated_tokens=0`；analyze `p1=None` / `not_evaluated` |
| 对抗：scientific prepare | `--eval-mode scientific --sham-opportunities 1` | `model=tiny-qwen2`，`generation=decode_loop`（测试锁这个）。文本仍含题干 `p1 = 4`。**6 条轨迹 events=0，observations=0，无 Label 行。** sham 观测 0。densities `null_reason=noise_set_empty` |
| 对抗：scientific collect tiny | 同上 + collect tiny | `H` 形 `(6,32)`（每条轨迹 **最后一个 hidden**，因无事件）；`E` `(2,32)`（第一条轨迹两个前提 span）；`H_pre_step` `(1,32)` **等于 H 最后一行**（meta 被最后一条覆盖） |
| 对抗：tiny intervene | scientific collect 后 `--backend tiny` | `timing=pre_step`，`status=prospective_decode`，`clayer_status=dev_scores_missing`。作者测试走 offline，断言 `!= pre_step`，**绿在替身上** |
| 对抗：几何测试路径 | 与 `test_intervene_geometry_is_not_pre_step` 相同 | `timing=unexpressible`，`status=donor_missing`。该测试 **通过** |
| 对抗：P1 泄漏 | n=80，train ρ 噪声、eval ρ=y | 诚实 ΔAUC=`-0.2125`（0.47/0.2575）；全量拟合泄漏 Δ=`+0.096`（0.6525/0.557）。作者 `rho=y` 全行用例诚实与泄漏 **都是** `auc_full=1`、`delta=0.29` |
| 对抗：precomputed | length=`[1,0,1,0]`，y=ρ=`[0,0,1,1]` | 当前 Δ=`0.5`；旧魔术 `len+ρ` Δ=`0.375`。作者 `length==ρ` 例两种都是 Δ=`0` |
| 对抗：bootstrap | 作者 `test_p1_returns_bootstrap_interval` 数据 | `interval=[0.5,0.5]`。实现是 `bootstrap_cluster([delta]*n_groups)`，重采样相同标量 |
| 对抗：verbalizer | gold=`7` | `answer 7`→1.0（作者测试）；`17`→1.0；`answer 70`→1.0；`\boxed{8} also 7`→1.0（抽取是 8，子串仍命中） |
| 对抗：repair 旗标 | `execute=lambda: {generated_ids:[1], extra_prefill:0}` | `refilled_prefix is True`。`task_oracle` 的 `mask_prefix` **原样返回** `hello world tokens` |
| 对抗：scientific repair | k=1..5 | 全部 `refilled_prefix=True`，`generated_tokens=8`，`extra_prefill_tokens=32`（`ids[:32]`）。k 只改 slots 切片，oracle 掩码忽略 slots |
| 对抗：span 回退 | offsets `[[0,2],[2,6]]`，span `[1,3]` | 无 contained → 回退 **`[0,1]`（含跨界）** |
| 对抗：Week8 | `{gate0:0.9}` | `gates.gate0.decision==evaluated`，无测量比较。`rho_S_excess==0` → `c3_negative_descriptive`（单元已锁） |
| 对抗：BoundaryMLP | 2 点 y=0、logits≈10 | impl loss `10.000045…` = 正确 BCE。**r04 F4-05 作为实现已闭合** |
| 对抗：E-16 | analyze `--in-dir` 文件 / scientific 无 `--in-dir` | 先拒，**不写** `report.json`。**r04 F4-17 文件入口已闭合** |
| 对抗：hook | `once=True`，两次 `decode_step` | transform 输入 `(1,1,32)`（只末 token）；只触发 1 次。**无测试** |
| 对抗：transfer | `src=I`，`tgt=diag(2,3)` | `apply_map` 恢复 I。套件只查 shape |
| 对抗：joint `f≡0` | | `joint_changed=False` 但 `soundness_claim_allowed=False`（常量） |
| 对抗：readout | n=2 | 返回 1，即 **最后一层 / 100%**，不是 60–75% 带。测试只锁 n=3→1 与 n=32 范围 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-05 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 120 passed | `VERSION.md` L26 | **命令是。** 当作阶段/Goal 证据：**否。** |
| r04 已在本地关闭，待独立复核 | `ISSUES.md` | **部分。** BCE / E-16 文件 / Child 非沙箱 / scientific 拒 offline / 无 generate 拒答，单元成立。A4-01 generate、A4-02 span-pool H、A4-03 几何 timing、A4-04 Prefill、A4-06 子串、F4-01 e2e、C3-M-02 泄漏 **未闭。** |
| scientific generate / span-pool E / Prefill / 诚实账本 | `ISSUES.md` F4-01/F4-18 行 | 测试存在，但锁的是零事件 decode、末 token H、`refilled_prefix` 旗标。账本仍把 `pytest -q` 写成行级 `verification_method`（`PAPER_TRACEABILITY.md` TR-0002+）。`06-VERIFICATION.md` L8 仍写 **65 passed**。 |
| CLI 流水线消费上游 | `test_full_cli_smoke`；`test_pipeline_consumes_upstream` | 文件被读。科学没有：offline H、`scores=None`、analyze 忽略 labels。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham∉R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 **span**（不是答案证明）；B-11 空父母；B-13 `family_id`；B-14 source=/test_only + 生产 key；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]` + `predict_set`；bilinear σ/λ_FN；spy.calls / `exec(`；E-17 labels-dir hash。

**本冻结新增且独立：**

- `test_boundary_bce_not_negative`：旧符号公式在该点为负，现实现 = 手算 BCE `10.000045…`。**F4-05 实现闭合。**
- `test_p2_integer_denom_without_set_is_unverified`：`99` 无集合 → `denominator_unverified`。
- `test_sequence_score_uses_true_edges_only`：`truth_indices=[0]` 得 0.1，无下标得 0.9。
- `test_verbalizer_without_generate_is_unavailable` 的 **拒答半边**：无 `generate_fn` → `generate_unavailable` / `score is None`。
- `test_child_process_is_not_isolated_executor`：`isolated_sandbox is False`；`SubprocessExecutor is ChildProcessExecutor`。
- `test_scientific_collect_span_pool_and_refuses_offline` 的 **拒答半边**：scientific+offline 抛 `offline_prefix_ids`。
- `test_week8_zero_excess_is_descriptive_negative`：`ρ_S=0` → `c3_negative_descriptive`，Gate `unregistered`。
- `test_plus_and_symbolic_share_gsm8k_family`：两边 `gsm8k-12`。
- `test_nl_monotonic_keeps_matching_versions`：只配 occurrence 2。
- `test_failed_resume_does_not_clobber_success_manifest`：坏 traces 后原 hash 仍在 + `failure.json`。
- `test_analyze_requires_directory`：scientific 无 `--in-dir` / `--in-dir` 文件 → 无 `report.json`。**F4-17 文件入口闭合。**
- `test_source_value_pair_has_both_conditions`：元数据键存在（不证明源真解耦）。

### 6.2 无效、自指或过弱（含本轮点名的五类替身）

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_full_cli_smoke` | **offline H 当成功。** 本通道复现 `H=[[1..8]]`、`scores=None`、`p1 is None`。仍断言 `not_evaluated`。 |
| `test_e04_analyze_manifest_includes_report` | **把 stub 编码成期待**（`status==not_evaluated`）。 |
| `test_pipeline_consumes_upstream` / `test_fit_hashes_labels_dir` | 停在 fit；offline 前缀 ID 上任意有限 loss 都过。双头同 loss。 |
| `test_analyze_uses_p1_table` | 只要求 `p1 is not None`。`if table: p1={}` 的桩会过。不读 `labels.jsonl`。 |
| `test_scientific_prepare_is_generated_not_node_values` | 只禁管道串 `p1 = 4 \| p2 = 0 \| q = 0`，不禁题干里的 `p1 = 4`。**不要求任何事件。** 本通道：6 条轨迹 events=0、obs=0。 |
| `test_scientific_collect_span_pool_and_refuses_offline` 的 **成功半边** | 有 `H_pre_step` 键、`E[0]≠E[1]`（同一题两个前提）。无事件时 H 是 **末 token**，`H_pre_step` 是 **最后一条轨迹的末 token**。不是论文步前 H。 |
| `test_intervene_geometry_is_not_pre_step` | **几何当 pre_step 的反面替身。** 走 offline 单行 H → `unexpressible`/`donor_missing`，于是 `!= pre_step`。真 tiny 路径写 `timing=pre_step`。 |
| `test_repair_tiny_prefills_and_masks_differ` / `test_scientific_repair_runs_k_1_to_5` | **`refilled_prefix` 无 Prefill。** `run_repair(..., execute=)` 无条件 `True`。哑 execute 也过。`task_oracle` 不改前缀。k=1..5 生成数全是 8。 |
| `test_verbalizer_without_generate` 的 **成功半边** | `generate_fn=lambda p: "answer 7"`，gold=`7`。**子串** `gold in text`（`baselines.py` L119）。`17`/`70`/`boxed{8} also 7` 全是 1.0。作者 ISSUES 写“substring scorer removed”——**源码仍在**。 |
| `test_p1_precomputed_is_scores_not_magic` / `test_c01_auc_*` | **precomputed 当正文 P1。** `length==ρ` 时旧魔术 Δ 也是 0。区分例 Δ 0.5 vs 0.375，测试碰不到。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在 **全部** 行。泄漏拟合同样 `auc_full=1`、`delta>0`。 |
| `test_p1_returns_bootstrap_interval` | 只要求 `bootstrap`/`interval` 非空。实现是 `[delta]*n`，区间退化为 `[δ,δ]`。 |
| `test_p1_null_on_single_class` | 任意 `unique(y)<2 → None` 桩都过。 |
| `test_boundary_mlp_trains` | 仍只 `status==ok` + shape（符号由新测试补）。 |
| `test_week8_blocks_already_decided` | 子串。阈值不比较测量。 |
| `test_week8_never_passes_unregistered` | 空阈值。 |
| `test_evaluated_zero_hit_sham_*` | 先构造 labels 却不用；`dependency_densities(..., noise_evaluated=True)` 直接喂空 N。第二句是 `null_reason != noise_set_empty or excess is not None`（析取）。scientific 路径根本没有 sham 观测。 |
| `test_attention_threshold_uses_dev_split` | `split=="dev"` 且阈值 ∈[0,1]。桩 `threshold=0.5` 过。 |
| `test_readout_layer_is_60_75_band` | n=3→1 合理；n=32 只查范围。n=2 → 最后一层。 |
| `test_span_pool_uses_contained_tokens` | 只测 contained 命中。回退路径纳入跨界 token。 |
| `test_direct_transfer` / labeled map | 形状。`return ones_like` 也会过。本通道 `apply_map` 已恢复 I。 |
| `test_align_equal_count_*` `scanned is False` | 镜像硬编码常量。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。last-token / once 未测。 |
| `test_collect_and_intervene_tiny` `cache_isolated` | `past_key_values=None` 保证新对象。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。`f≡0` 仍 False。 |
| `test_repair_reprefills_and_refuses_gate` 无 execute 半边 | 诚实拒答。有 `prefix_token_ids` 半边仍是 `len(list)`。 |
| `test_calibrate_infinity_is_json_safe` | `q is None or isinstance(q,(int,float))` 几乎恒真；infinity 分支视数据。 |
| `test_resume_collect_matches_written_command` | 只比 `file_hashes` 相等，不比 command 字段。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline（F5-01）。** 文档化绿路径：`H`←`token_ids[:8]`；无 `--features-dir` 则 `scores=None`；analyze 不从 labels 建 P1；`test_full_cli_smoke` **要求** `not_evaluated`。
2. **scientific 入口已接线，语义是空的（F5-07）。** `generate_task_trace` 把题干 + 随机 decode 交给 `parse_fixture_events`。解析器要 `q = <数字>`；题干是 `q = p1 * p2?`，后缀是乱码。于是事件/观测/标签全空。测试把它当“不是 node-value dump”的成功。
3. **`refilled_prefix` 是函数参数的副作用（F5-03）。** 有 `execute` 就 True。不是 KV Prefill，也不是“保留文本在新前缀上重预填”的可观察量。`execute_repair_tiny` 用 char-ord 编码 + 新随机 tiny `decode_loop`。
4. **verbalizer 子串（F5-04）。** 无 generate 的拒答是真的；有 generate 的 1.0 不是。
5. **几何测试躲开了会写 `pre_step` 的分支（F5-02）。** `cmd_intervene` 在 hook 触发后把 `offline_hidden` **改写成** `pre_step`（`cli.py` L661–663；`intervene_swap_decode` L180 本来就是 `"pre_step"`）。
6. **P1 测试锁估计器名字（F5-05）。** `precomputed_scores` / `held_out_logistic` / bootstrap 非空。泄漏与魔术与退化区间都绿。
7. **HumanEval spy 已观察，子进程不是沙箱（仍成立）。** Goal §五.15 禁止把这个叫隔离沙箱。新测试正确否定了 Isolated 身份。
8. **仍无测试提及的符号：** `attention_rollout`、`attention_mean`、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`retrieval_scatter`、`card`、`catalog.load_snapshot`、`apply_model_template`、`clone_cache`。`bootstrap_cluster` 只经 P1 间接碰到，且被喂常数。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 科学 prepare 必须产出可对齐事件，或拒绝宣称 generate

- 构造：`prepare --eval-mode scientific` + `t1_tiny`（题干 `What is q = p1 * p2?`）。
- 期望：每条轨迹至少一个 `q = <值>` 事件，或 `status=parse_failed` 且 analyze 拒科学结论；sham 有 `rng_pair=sham:*` 观测。
- 当前：events=0，obs=0，无 Label，densities `noise_set_empty`。
- `test_scientific_prepare_*` **绿**。

### CE-2 CLI analyze 必须消费 labels 或拒绝

- 构造：prepare 写了 `labels.jsonl`（fixture 路径有；scientific 路径几乎没有），analyze `--in-dir` 该目录。
- 期望：拒绝，或用这些 labels 给出冻结 P1。
- 当前：exit 0，`p1 is None`，`not_evaluated`。`test_e04` / smoke **要求** 这个 stub。
- tiny collect + `--features-dir` 校准可以写出分数；analyze 仍不读 labels 建 P1。

### CE-3 留出 P1 + 非魔术 precomputed + 真 bootstrap

```text
n=80, length/op ~ N(0,1), y 交替, held_out=后半
rho = 噪声(train), rho = y (eval)
诚实 ΔAUC = -0.2125；泄漏全拟合 Δ = +0.096
作者 rho=y 全行：诚实与泄漏都 auc_full=1、delta=0.29  → 现测试绿

precomputed: length=[1,0,1,0], y=rho=[0,0,1,1]
当前 Δ=0.5；旧魔术 len+rho Δ=0.375
作者 length==rho → 两种都是 0

bootstrap: 实现 [delta]*groups → interval [0.5,0.5]
应重采样 (length,op,rho,y,group) 再算 ΔAUC
```

### CE-4 verbalizer 不是子串

```text
gold="7", generate="answer 7"     → 作者测试给 1.0（子串）
gold="7", generate="17"          → 现 1.0；抽取 "17" 应 0
gold="7", generate="answer 70"   → 现 1.0；抽取 "70" 应 0
gold="7", generate=r"\boxed{8} also 7" → 现 1.0；抽取 "8" 应 0
```

### CE-5 Prefill 不是旗标

```text
run_repair(..., execute=dummy) → refilled_prefix True   现测试会绿
task_oracle 的 mask_prefix("hello world tokens") == 原文
scientific k=1..5：generated_tokens 全 8，extra_prefill 全 32
应：新前缀 token 上对保留文本做一次模型 Prefill（可见 KV/前向），
    掩码必须按 mask 改变前缀；k 增加应改变 slots 或预算
```

### CE-6 几何 / 步前

```text
测试路径（offline 1 行 H）：timing=unexpressible  → 测试断言 != pre_step，绿
scientific tiny + hook：timing=pre_step, status=prospective_decode
几何若在已采集 H 上算，应保持 offline_hidden / 非步前，且不得被 hook 覆盖
C-layer 无 --dev-layer-scores 不得冒称 dev_weak_layer（当前 missing，测试只禁弱层名）
```

### CE-7 span 跨界回退

```text
span_token_indices([[0,2],[2,6]], 1, 3) == [0, 1]   # 现实现，含跨界
Goal §五.6：步前/前提池化不得纳入跨界目标内容
contained 命中路径已被测试；回退路径没有
```

### CE-8 空噪声 / scientific sham

```text
noise_set=[] + hits → 单元 null（仍锁）
scientific --sham-opportunities 1：0 条 sham 观测，0 条事件
observed N=∅ 与 missing N 在 CLI 科学路径上仍分不清
fixture sham 仍写 premise_id=""（代码 L294 / L325）
```

### CE-9 hook last-token / once / 双头 Y

```text
resid_post_hook: transform 见 (1,1,32)；前缀不传入   实现有，无测试
once=True: 两次 decode_step → 1 次 transform
CLI fixture fit：task/behavior 同一 loss 0.05036
```

## 9. 发现

### F5-00 声明冻结哈希可复算

- **严重度：** —
- **状态：** 非缺陷建议（本轮过程正确）
- **文件：** `.planning/audits/round-05/VERSION.md` L5–23；工作区 58 文件
- **复现：** §1。本地 `4c8769f3…` == 声明。0 CRLF。
- **注：** 夹具仍在摘要外（F5-12）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F5-01 CLI / Goal e2e 与“科学 generate”测试仍接受未接通科学路径

- **严重度：** Critical
- **状态：** confirmed defect（验证 + 科学 prepare 的实现空洞）
- **文件/行：** `tests/test_cli_pipeline.py` L4–29；`tests/test_review_regressions.py` L381–394、L287–294；`tests/test_round04_regressions.py` L30–63、L66–111；`cli.py` `cmd_prepare` L271–306、`cmd_collect` L419–450、`cmd_calibrate` L594–598、`cmd_analyze` L720–739；`models/generate.py` `generate_task_trace` L66–134；`events.py` `parse_fixture_events` L27–75
- **触发：** 文档化八命令（offline，被测路径）；或 `--eval-mode scientific` prepare
- **要求：** Goal §六“从生产入口验证跨模块数据流”；§五.1/§五.3 事件；OPS-01 / QA-01
- **复现：** §3。offline `H=[[1..8]]`；scientific 6 轨迹 **events=0 / obs=0 / 无 Label**；analyze 忽略 labels
- **影响：** 120 passed + runbook 可被写成“pipeline / scientific generate 已通”，而 P1–P3 从未见到标签，科学轨迹没有事件
- **修复：** CE-1 + CE-2；禁止把 `not_evaluated` 当 e2e 成功；scientific 无事件必须失败或显式 `parse_failed`，不得当闭合 A4-01
- **作者主张 A4-01 / F4-01 / F4-18：** **未闭合。** 测试锁的是“不是管道串 / 不是 offline H 键名”，不是论文 generate

### F5-02 几何测试锁住 unexpressible 替身；真 tiny 路径把 timing 写成 pre_step

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）
- **文件/行：** `tests/test_round04_regressions.py` L114–124；`cli.py` L615–663；`models/collect.py` `intervene_swap_decode` L174–183
- **触发：** intervene 默认/tiny 且 `H` 至少两行且 hook 触发
- **要求：** Goal §五.6/§五.10；作者 A4-03（几何行应为 `offline_hidden`，不得当步前）
- **复现：** 与测试相同的 offline 路径 → `unexpressible`，测试绿。scientific tiny → `timing=pre_step` / `prospective_decode`
- **影响：** 可以引用“已锁几何不是 pre_step”，同时生产在论文关心的路径上写 `pre_step`
- **修复：** CE-6；测试必须走会做几何/解码的 H；hook 成功不得把离线几何改名为步前
- **作者主张 A4-03：** **未闭合**（测试选了不会触发该写入的后端）

### F5-03 `refilled_prefix` 无 Prefill；C4 仍是账本加旗标

- **严重度：** High
- **状态：** confirmed defect
- **文件/行：** `repair.py` L111–131、L45–61、L64–94；`tests/test_round04_regressions.py` L126–135、L301–310；`cli.py` L688–707
- **要求：** Goal §五.13 / REPAIR-01；作者 A4-04
- **复现：** 哑 `execute` → `refilled_prefix=True`。`mask_prefix("task_oracle", …)` 等于原文。scientific k=1..5 生成数与 extra_prefill 全相同。fixture 默认 backend=offline → 0 token / `prefill_unavailable`（smoke 不查这个）
- **修复：** CE-5；或正式把 C4 标成未实现 Prefill
- **作者主张 A4-04 / F4-06：** **部分**（无模型时拒答是真的；Prefill 主张为假）

### F5-04 verbalizer 子串计分仍在；测试把它锁成 1.0

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）
- **文件/行：** `baselines.py` L115–120；`tests/test_round04_regressions.py` L202–208；`tests/test_science.py` L69–73
- **要求：** Goal §五.7；作者 A4-06“substring scorer removed”
- **复现：** gold=`7` 命中 `17` / `70` / `\boxed{8} also 7`
- **修复：** CE-4；只用 `extract_answer` 相等（或规范数值），禁止 `gold in text`
- **作者主张 A4-06：** **未闭合**

### F5-05 P1 测试锁名字，不锁留出、非魔术分数或真区间

- **严重度：** High
- **状态：** confirmed defect
- **文件/行：** `analysis.py` `p1_incremental` L41–89、`bootstrap_cluster` L272–283；`tests/test_round03_regressions.py` L72–91；`tests/test_round04_regressions.py` L191–199；`tests/test_review_regressions.py` L206–230
- **要求：** Goal §五.12 / C3-01：链长+op 基线，**留出**增量 AUC；问题级聚类不确定度
- **复现：** §3 CE-3。IRLS 与默认 `requires_held_out` 仍在。bootstrap 是常数 δ 的分位
- **影响：** 正文 P1 数字可以来自泄漏拟合 + 退化区间，套件仍绿
- **修复：** CE-3
- **作者主张 A4-10 / C3-M-02：** **部分**（有 bootstrap 键；不是论文区间）

### F5-06 `span_token_indices` 回退纳入跨界 token

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证缺口）
- **文件/行：** `models/tokenize.py` L28–32；`tests/test_round04_regressions.py` L246–247
- **要求：** Goal §五.6；D-01 跨界排除
- **复现：** `[[0,2],[2,6]]` × span `[1,3]` → `[0,1]`。测试只锁 contained=`[1]`
- **修复：** CE-7；无 contained 应空/拒，不得 overlap 回退

### F5-07 scientific sham / 空事件使噪声协议落空

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）
- **文件/行：** `cli.py` L284–306、L338–352；`measure.py` L281–322；`tests/test_round04_regressions.py` L155–175
- **复现：** scientific+sham：0 sham 观测。单元测试用手写 `noise_evaluated=True` 绕过 CLI。fixture sham 仍 `premise_id=""`
- **作者主张 C4-M-01 / B-12 / A4-20：** **单元可闭“空 N 且 evaluated→噪声 0”；CLI 科学路径未闭**

### F5-08 Week8 Gate 有阈值即 `evaluated`，不做比较

- **严重度：** Medium
- **状态：** confirmed defect（实现 + 验证）
- **文件/行：** `analysis.py` `week8_decision` L182–211；`tests/test_round04_regressions.py` L178–182；`tests/test_science.py` L56–61
- **要求：** Goal §五.14 / DECIDE-01
- **复现：** `{gate0:0.9}` → `decision==evaluated`。零 excess 分支已锁，不能抵消这条
- **作者主张 A4-11：** **部分**（零 excess / 未注册 Gate 是真的；阈值树仍死）

### F5-09 联合 soundness 常量、迁移只查形状、H_pre 被最后一条覆盖、hook 未锁

- **严重度：** Medium
- **状态：** confirmed defect（验证；H_pre 覆盖兼实现）
- **文件/行：** `measure.py` L325–334；`tests/test_measure.py` L25–32；`tests/test_science.py` L30–37；`cli.py` `cmd_collect` L424–437；`models/tiny.py` L55–73；`tests/test_tiny_hooks.py` L17
- **复现：** `f≡0` 仍禁 soundness。`apply_map` 恢复 I 未断言。scientific `H_pre_*` 来自最后一条轨迹的 meta。once/last-token 形状 `(1,1,32)` 无测试
- **作者主张 D-07：** 实现在，**验证未闭**

### F5-10 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout`、`attention_mean`、`forbid_host_exec`、`score_qa`、`procrustes`、`retrieval_scatter`、`assert_disjoint`、`card`、`catalog.load_snapshot`、`apply_model_template`、`clone_cache`
- **要求：** Goal §六独立 oracle；§四反向覆盖
- **注：** `apply_source_value_edit` 现有元数据测试，不再算零提及

### F5-11 追踪账本仍把 `pytest -q` 当行级证据

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md` TR-0002+（`verification_method=python -m pytest -q`，`local_verify_status=passed_local_tests`）。`.planning/phases/06-acceptance/06-VERIFICATION.md` L8 仍 **`65 passed`**
- **影响：** Goal §九.1 可被纸面勾成“已填”，而该行没有对应行为测试
- **作者主张 A4-05 / F4-13：** 页眉声明改善了；**行级样板未清**

### F5-12 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`；`VERSION.md` 范围
- **影响：** oracle 字节可动而不改 `.py`+toml 聚合

### F5-13 ISSUES `fixed_pending_review` 高估验证闭合

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为单元验证闭合：** Boundary BCE 符号（C4-M-03 / F4-05）；E-16 文件入口（F4-17）；`ChildProcessExecutor` 非 Isolated（A4-13 / F4-04 验证半边）；scientific **拒绝** offline H；无 `generate_fn` 拒答；P2 无集合分母；Week8 零 excess + 未注册 Gate；gsm 家族键；monotonic 版本；resume 不覆盖成功 manifest；`truth_indices`；前轮 B-01–14/23/24、C3-M-01/03/07、D-08、E-17、bilinear、spy 等。
- **实现在、验证未闭：** B-10 答案证明；D-07 once/last-token；D-10 clone；noop `answer_unchanged_proven`；attention rollout/mean。
- **未闭（错或镜像）：** A4-01 零事件 generate（F5-01/07）；A4-02 span-pool H（末 token）；A4-03 timing=pre_step（F5-02）；A4-04 Prefill 旗标（F5-03）；A4-06 子串（F5-04）；A4-10/C3-M-02 泄漏+假 bootstrap（F5-05）；A4-11 Gate 树（F5-08）；B-12 CLI sham（F5-07）；B-21 reversing；C3-M-05 nontarget 回声；C4 账本；F4-01 e2e；跨界 span 回退（F5-06）。
- **不要用本通道把 Goal/需求标 Complete。** 上表单元闭合 ≠ 科学验收。

### F5-14 双头仍可在同一 Y 上拟合；fit 把标签广播到所有 H 行

- **严重度：** Medium
- **状态：** confirmed defect（验证；fixture 路径实现）
- **文件/行：** `cli.py` `cmd_fit` L519–540
- **复现：** offline smoke 两头 loss 同为 `0.05036…`。`for i in range(h.shape[0])` 复制同一 label
- **作者主张 dual-head Y：** **未闭**

### F5-15 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、`offline_prefix_ids`、宿主 `subprocess`、`executor_unavailable` 不得改写成服务器验收。零事件 scientific decode 也 **不是** pending_server，是本机代码缺口。

### F5-16 非缺陷说明

- **状态：** 非缺陷建议
- `VERSION.md` 算法可复现。保持脚本冻结。
- 相对本通道 r04：BCE 符号、E-16 文件入口、Child 非沙箱断言、scientific 拒 offline、无 generate 拒答、P2 unverified、Week8 零 excess、家族键、resume 失败不覆盖——这些是真改进。
- `consecutive_pass_count: 0` 与“120 passed ≠ Goal”比把套件当验收更诚实。
- last-token hook、`once=True`、clone metadata、scientific 拒答看起来已实现；缺测试或被替身测试盖住，故不闭。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**当前测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 账本仍 `pytest -q` / `passed_local_tests`；`06-VERIFICATION.md` 仍 **65 passed**（F5-11）。反向覆盖失败（F5-10）。scientific 行被空事件测试“填绿”。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F5-01、F5-02、F5-03、F5-04、F5-05、F5-06、F5-07 为已确认遗留。ISSUES 仍 `fixed_pending_review`。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 120/0，无 skip 伪装。e2e 是 exit-code 烟测并 **断言** `not_evaluated`。科学路径有测试，但锁替身。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** 页眉有“不是服务器权重证据”（好）。行级与 06-VERIFICATION 仍旧数字（坏）。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 哈希匹配（好）。`VERSION.md` `consecutive_pass_count: 0`。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。只补审查日志不改变被审 hash——本文件属于审查日志，不改变 58 文件摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：零事件 generate、offline 前缀 H、Prefill 旗标、子串 verbalizer、宿主 subprocess 都是 **有名字的代码** 缺口。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F5-13）。本机 pytest 记录存在（120/0）。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。scientific 轨迹 **无事件**，谈不上真值对齐。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus test-only 有。reversing / `new_answer` 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 解析器对 `q = p1 * p2?` 得到 **空列表**。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。scientific sham **零观测**。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 下标有。span **回退跨界**（F5-06）。collect 无事件时用末 token 冒充 `H_pre_step`。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE 符号有。verbalizer **子串**。双头同 Y。rollout 无测试。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。smoke `scores=None`。`truth_indices` 单元有。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；C-layer **开发集** | swap 公式有。CLI 无 dev 分数 → missing，随后仍跑 hook 并标 `pre_step`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。泄漏/魔术/假 bootstrap 绿。analyze 不读 labels。 |
| 13 附录修复 | 新前缀 Prefill；几何/锥 | 旗标 + char decode。锥 `r2>0.9` 弱。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。阈值即 evaluated。 |
| 15 代码任务 | 显式隔离执行器；普通 subprocess ≠ 沙箱 | spy + `isolated_sandbox is False` 已锁。默认仍 Unavailable。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **120 passed，exit 0，13.11s，120 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH。** 声明与复算均为 `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（58 文件）。逐文件 SHA-256 见 §2。 |
| 独立性 | 新真 oracle：BCE 符号、P2 unverified、Child 非沙箱、无 generate 拒、scientific 拒 offline、零 excess、家族键、monotonic、resume 不覆盖、analyze 文件入口、`truth_indices`。**不独立：** offline H e2e、零事件 scientific generate、末 token 当 span-pool H、`refilled_prefix`、verbalizer 子串、precomputed-as-P1、几何测试路径、假 bootstrap。 |
| Mock/stub | offline 前缀 H + calibrate `scores=None` + analyze 忽略 labels + repair 旗标 + 空事件 decode + `not_evaluated` 编码为成功。比 `unittest.mock` 更差。 |
| 论文行为仍未证明 | 有事件的科学 generate、步前 H、泄漏不进的 P1、非魔术分数、真 Prefill、非子串 verbalizer、dev 上的 C-layer、隔离执行、T2 reversing、R^surf 超夹具行 |
| 交付 vs 测试 | “120 passed / r04 已本地关闭 / scientific generate·span-pool·Prefill 已锁” **超过** 测试力度 |
| 已确认问题？ | **是。** Critical：F5-01。High：F5-02、F5-03、F5-04、F5-05、F5-06、F5-07。 |
| Goal 完成？ | **否。** |
| 通道通过？ | **Fail。** 空的“看起来没问题”不适用。绿 pytest 不是验收。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷。即使 A–E 全写“通过”，只要 F 确认缺陷，两轮计数必须保持 0；修复后换 hash 重开。 |

在 CE 级测试锁住 Critical/High 项、并且 A4-01 零事件 / A4-03 `pre_step` / A4-04 旗标 / A4-06 子串 / P1 泄漏真正修掉之前，任何“代码验收通过；独立审查未发现已确认遗留缺陷”的结束句都与本通道证据矛盾。
