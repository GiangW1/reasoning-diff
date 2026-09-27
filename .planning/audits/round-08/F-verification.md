# F：验证质量与反向质疑（round-08）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-08 其他通道报告。`ISSUES.md` 只当作者主张；声称的 r06 闭合从测试对生产符号重核，再用进程内反例攻击（未向仓库加测试）。`python -m pytest -q` 绿不是论文正确性，也不是 Goal 验收。

**先行结论：** 冻结哈希 **复算一致（HASH_MATCH）**。本机 `python -m pytest -q` 为 **144 passed / exit 0**。这不是 Goal 通过。六个点名替身里，题干赋值当事件、NaN 行冒充步前 H、科学路径 `donor_missing` 靠 `timing!=pre_step` 过关、`prefix_token_ids` 当 Prefill、噪声数据上的 `[δ,δ]` bootstrap——本通道攻击这些旧 CE **不再复现**，对应新测试有真 oracle。**C6-M-01 未闭：** `test_truth_indices_follow_e_columns_not_label_order` 只喂带 `task.premises` 的 `SimpleNamespace`；作者自己的 `collect→label→fit` 目录里 **没有** `tasks.jsonl`，`cmd_fit` 于是 `_e_premise_ids(None, labels)`，Y 列回到 labels 首次出现序 `['p2','p1']`，而 `E` 仍按 `task.premises` 的 `['p1','p2']`。该 fit 测试只查 `U` 有限。另：`prefill_hidden=0` 仍标 Prefill；e2e 仍是 offline 前缀 H。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：本通道提交已确认缺陷，连续两轮 A–F 通过计数 **不能开始**。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e` |
| 复算聚合 | `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e` |
| 哈希裁决 | **HASH_MATCH** |
| 哈希方法 | 60 个文件：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。按 POSIX `relpath` 排序。`SHA-256.update(relpath.encode() + b"\0" + file_bytes)`。`VERSION.md` 脚本原文。范围内 0 处 CRLF。 |
| 文件数 | 60，与 `round-08/VERSION.md` 一致（r06 为 59；本冻结含 `tests/test_round06_regressions.py`） |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest | **144 passed in 18.72s，exit 0。** Collect：**144 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只出现在 HumanEval/`SubprocessExecutor` 载荷字符串里。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。一处 `@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 范围 | 全部 `tests/**`（17 个 `.py` + 10 个夹具 JSON）及测试导入/CLI 烟测触及的生产符号 |
| 明确未读 | `.planning/audits/round-08/{A,B,C,D,E}-*.md` |

审查对象是**当前工作区字节**。作者 `pytest_author_claim: 144 passed` 仅作为命令结果被独立确认。

## 2. 逐文件覆盖

### 2.1 测试（全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍是 `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 397 | `d3814498fe52b28b…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 291 | `5698a410c0669b61…` | r03 节点；P1 泄漏用例仍绿 |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline 几何仍只 `!= pre_step`；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | 相对 r06 加强：H `isfinite`、科学 intervene `!= donor_missing`；仍不比 last-token |
| `tests/test_round06_regressions.py` | 136 | `a4421f11d41e1743…` | 8 个新节点；独立与替身混杂（见 §6） |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 现锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only：**144 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r06 的 136 节点：+8，全部在 `tests/test_round06_regressions.py`。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声数据 `lo<hi`、Week8、BOW | r04 常数 δ 仍 `[0.5,0.5]`；泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed；无 generate 拒答 | `attention_mean`/`attention_rollout` 无数值 oracle |
| `cli.py` | 1164 | `2f1fac48ebbcf1a1…` | smoke offline；scientific prepare/collect/fit/intervene/repair；无 `--in-dir` 拒 | **fit 不读 prepare 的 `tasks.jsonl`** → C6-M-01 回退首次出现序；analyze 标签 `<4` → `p1 is None`；hook_timing 未断言 |
| `edits.py` | 277 | `bfd1632b50504c04…` | value/rename/op-reverse/5.5；source-value 元数据 | 同值异源是否真改源 |
| `events.py` | 260 | `fc5031a51e99a4b5…` | 身份；`parse_events(prompt)` 仍得 p1/p2；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP/范数 | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 345 | `1fa2360e680d37ad…` | 事件均值；空 N；sham hit 不记已评估 0 | `soundness_claim_allowed` 恒 False |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 199 | `2772257e0643b3c7…` | 有限 H；跳过不可表达行 | 测试不比 last-token；`intervene_swap_decode` 仍写 `timing=pre_step` |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 201 | `07493570c6410e6b…` | `start>=len(prompt)`；`parse_region` 旗标 | 事件全是教员强制 `q=`；`apply_model_template` 无测试 |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` 未断言 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号；`status==ok`+shape | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | **CLI calibrate 无反序 labels 测试** |
| `repair.py` | 223 | `d547ab99e3179093…` | `prefix_token_ids` / 空 hidden → False | **`prefill_hidden=0`/`[0.0]`/`True` → True** |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | `Event.from_dict` extras |
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
| `transfer.py` | 75 | `d31bcd499a51ca94…` | 4096/3584；PCA 不截断；**形状** | `apply_map` 数值恢复未锁 |

夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `1b88bec2…`（60 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 全量 pytest | 仓库根 `python -m pytest -q`（`pythonpath=src`） | **144 passed in 18.72s，exit 0**。无 skip/xfail/deselected。 |
| Collect | `python -m pytest tests --collect-only -q` | 144 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM `4*3 % 23 = 12`；sidecar 8；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]`；BCE 符号 | **存在的单元断言**与独立算术一致 |
| 对抗：prompt-as-events | `generate_task_trace` + scientific prepare | 6 轨迹各 **1** 个事件，全是教员强制 `q = <digit>`。`start>=len(prompt)`。题干 `p1`/`p2` **不**入事件。`parse_events(prompt)` 仍得 p1/p2。`parse_full_text` 再 `+=len(prompt)` **仍会**让测试的 `start>=len(prompt)` 变绿（会带上 p1/p2）。`parse_region` 硬编码 `"generated"`。 |
| 对抗：NaN H | scientific collect tiny | `H.shape=(6,32)`，**NaN 比例 0**。`n_events=6`（每迹一条 q）。`event_rows` 全是 `q`。t0：`pre_idx=44`，last=50，`maxabs(H vs last_token)=0.076`。**不是**末 token，也不是 NaN 行。测试只锁 `isfinite` + 行数，不比 last。 |
| 对抗：donor_missing / `!=pre_step` | 作者 scientific collect → intervene tiny | **无** `--dev-layer-scores`：`status=prospective_decode`，`timing=offline_hidden`，`hook_timing=pre_step`。有 dev 分数：同上 + `dev_weak_layer_decode`。offline 路径仍 `donor_missing`/`unexpressible`，`test_intervene_geometry_is_not_pre_step` 仍绿。 |
| 对抗：prefix_ids / dummy hidden | `run_repair` | `prefix_token_ids` → False。空 hidden / 仅旗标 / 无 hidden → False。**`prefill_hidden=0` / `1` / `[0.0]` / `True` → True。** |
| 对抗：bootstrap | 作者噪声数据；r04 `ρ=y` 常数 length | 噪声：`[0.112, 0.891]`，`lo<hi`。`[δ,δ]` 实现会红。r04：仍 **`[0.5, 0.5]`**，旧测试只查非空。`ρ=y` 全行：`auc_full=1`，`delta=0.29`。 |
| 对抗：C6-M-01 | helper + 真实 `collect→label→fit` | helper+假 task：`['p1','p2','p3']`，分数 0.1 vs 首次出现 0.2。**CLI：`col/tasks.jsonl` 与 `lab/tasks.jsonl` 都不存在。`task_for_e is None`。`unique=['p2','p1']`。正确 E 序 `['p1','p2']`。`E.shape=(2,32)`。** `task=None` 时 helper 就是首次出现序。 |
| 对抗：fixture 八阶段 | prepare→…→analyze，`--backend offline` | `H=[[1..8]]`；calibrate `scores=None`；intervene `donor_missing`/`unexpressible`；repair `refilled_prefix=False` / tokens=0；analyze `p1 is None` / `scientific_conclusion is None`。 |
| 对抗：scientific analyze | prepare scientific → label → analyze | 3 条含 `premise_id` 的 label（门限 ≥4）→ `p1 is None`。 |
| 对抗：scientific repair k | k=1..5 | `refilled_prefix` 全 True；`generated_tokens` 全 8；`extra_prefill` 全 32。 |
| 对抗：verbalizer / span | gold=7；跨界 | `17`→0；`[[0,2],[2,6]]×[1,3]`→`[]`。前轮 CE 仍闭合。 |
| 对抗：账本 | 解析 `PAPER_TRACEABILITY.md` 528 行 TR | `verification_method=python -m pytest -q`：**69**。`local_verify_status=passed_local_tests`：**320**。`executable_function`：**159** 行均为 `tests_exist_not_acceptance`（0 行 `pytest -q`）。页眉写不得用 pytest 关闭可执行行；协议行仍用 pytest 关闭。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-08 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 144 passed | `VERSION.md` | **命令是。** 当作阶段/Goal 证据：**否。** |
| r06 已在本地关闭，待独立复核 | `ISSUES.md` | **部分。** 题干不入事件、H 有限、科学 intervene 非 `donor_missing`、`prefix_ids` 非 Prefill、噪声 bootstrap `lo<hi`——单元或实现成立。**C6-M-01 CLI 未闭。** `prefill_hidden=0` 未闭。e2e / analyze P1 / 账本协议行未闭。 |
| `truth_indices` / fit Y 跟 `task.premises` | `ISSUES.md` C6-M-01 | **测试锁 helper。生产 fit 路径用首次出现序。** |
| CLI 流水线消费上游 | `test_full_cli_smoke`；`test_pipeline_consumes_upstream` | 文件被读。科学没有：offline H、`scores=None`、analyze 忽略不足以建 P1 的 labels。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham∉R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语。

**本冻结新增且独立（点名攻击失败 = 闭合）：**

- `test_generated_events_exclude_prompt_assignments` 的 **`start >= len(prompt)`**：旧 CE「parse 全文且不平移」会红。本通道：事件不在题干 span。**F6-01 旧 CE 作为「题干赋值入事件」闭合。**
- `test_scientific_collect_h_is_step_boundary_not_last_token` / `test_scientific_h_is_finite_and_pairs_donor` 的 **`np.isfinite(H).all()`**：全 NaN 或 2/3 NaN 会红。**F6-02 NaN 行数替身闭合。**
- `test_intervene_tiny_geometry_timing_stays_offline` 的 **`status != donor_missing`** 且 `in {prospective_decode, geometry_on_hidden}`：`unexpressible` 不再够。本通道 scientific 路径为 `prospective_decode`/`offline_hidden`。**F6-03 该替身闭合。**
- `test_prefix_ids_alone_are_not_prefill` / `test_science.py` 的 `prefix_token_ids` 半边：无 hidden 的 ids → False。**点名 prefix_ids 替身闭合。**
- `test_p1_bootstrap_interval_is_not_degenerate`：`lo < hi`。`[δ,δ]` 实现在该噪声数据上会红。**F6-05 作为「测试不禁退化实现」闭合。**
- `test_sham_hits_do_not_book_evaluated_zero_noise`；`test_catalog_aliases_musique_and_t4`；`test_missing_in_dir_fails_for_downstream`：对应作者 E/B 关闭项的入口/别名/sham hit。

### 6.2 无效、自指或过弱（含本轮仍活的替身）

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_truth_indices_follow_e_columns_not_label_order` | **C6-M-01 替身。** 自带 `task.premises`。不跑 `cmd_fit`/`cmd_calibrate`。真实 `collect`/`label` 目录无 `tasks.jsonl`，fit 走 `task=None` → 首次出现序。只锁 helper 在「已经有 task」时的行为。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 fit 半边 | 正是会触发 C6-M-01 回退的路径。只断言 `U` 有限。 |
| `test_generated_events_*` 的 `parse_region == "generated"` | 硬编码元数据，不是解析区域证明。`any(node_id==q)` 被教员强制 `\nq = 82` 单独满足。`full_text` 解析再平移仍过 `start>=len(prompt)`。 |
| `test_scientific_prepare_emits_parseable_events` | 只禁管道串、要求 `events>=1` 与存在 `q`。不要求 decode 后缀可解析，不禁「只有强制目标行」。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | **名不副实。** 锁 `isfinite` 与行数。不比 `token_index != last`。末 token 有限 H 也会绿。本通道实现不是末 token，测试没锁住。 |
| `test_intervene_geometry_is_not_pre_step` | 仍走 offline 单行 H → `unexpressible`。`!= pre_step` 旧替身还在。 |
| `test_intervene_tiny_geometry_timing_stays_offline` | 不读 `relative.hook_timing`（实现写 `pre_step`）。`geometry_on_hidden` + 元数据 `hook_once=resid_post`（即使 hook 未触发）也可绿。 |
| `test_dummy_execute_is_not_prefill` / `test_prefix_ids_alone_are_not_prefill` | 不锁 `prefill_hidden=0` / `[0.0]` / `True`。 |
| `test_p1_returns_bootstrap_interval` / `test_p1_bootstrap_resamples_delta_auc` | 前者只要求非空（r04 仍 `[0.5,0.5]`）。后者 `lo<=hi`。宽度只在新测试的噪声数据上锁。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_full_cli_smoke` | offline H 当成功。本通道复现 `H=[[1..8]]`、`scores=None`、`p1 is None`。仍断言空结论。 |
| `test_analyze_uses_labels_or_stays_null` | 只锁 `scientific_conclusion is None`。不读 `p1`。scientific labels → `p1 is None`。 |
| `test_analyze_uses_p1_table` | 手写 `p1_table.jsonl`。不读 `labels.jsonl`。 |
| `test_direct_transfer` / labeled map | 形状。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_align_equal_count_*` `scanned is False` | 镜像硬编码常量。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |
| `test_calibrate_infinity_is_json_safe` | `q is None or isinstance(q,(int,float))` 几乎恒真。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline（F8-08）。** `H`←`token_ids[:8]`；无 `--features-dir` 则 `scores=None`；analyze 标签不够建 P1；smoke **要求** 空结论。
2. **C6-M-01 用带 task 的 helper 盖住 CLI 无 task（F8-06）。** collect/label 不写 `tasks.jsonl`。fit 只看这两个目录。`_e_premise_ids` 在 `task is None` 时就是 labels 首次出现序。作者关闭测试不经过这条。
3. **科学事件非空，来源是教员强制 `q=`（残留 F6-01）。** 题干赋值已排除（好）。`any(q)` + `parse_region` 常量把强制行当 generate 闭合。
4. **步前 H 用「有限行数」冒充「不是末 token」（残留 F6-02 验证）。** 实现会跳过不可表达行（好）。测试名声称 last-token，断言没有。
5. **行字段 `timing=offline_hidden` 盖住 `hook_timing=pre_step`。**
6. **`refilled_prefix` 认任意有限 hidden。** ids/空列表已拒（好）。标量 `0` 仍过。
7. **P1 新测试锁噪声数据宽度。** 旧测试仍接受真退化区间；泄漏用例仍绿。
8. **账本页眉与可执行行 status 仍是 r06 状态：** 协议行 pytest；可执行行 `tests_exist_not_acceptance`。

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 题干事件（旧 CE 攻击失败；残留弱 oracle）

```text
generate_task_trace / scientific prepare:
  事件不在 prompt span；节点只有 q；parse_status=constrained_target
  题干 p1/p2 不再入 events     → 旧 prompt-as-events 不再复现
仍绿：
  parse_region 恒为 generated
  仅教员强制 "\nq = 82" 满足 any(q)
  parse(full_text) 后 start += len(prompt) 仍过 start>=len(prompt)，且会带回 p1/p2
```

### CE-2 NaN H（旧 CE 攻击失败；测试仍不锁 last-token）

```text
scientific collect: H.shape == (6, 32)，NaN 比例 = 0
event_rows 全 q；pre_idx=44 ≠ last 50
全 NaN 但行数对 → 现测试会红（已锁）
有限末 token 冒充步前 → 现测试仍绿
```

### CE-3 科学 intervene（旧 donor_missing 替身攻击失败）

```text
scientific tiny：status=prospective_decode，timing=offline_hidden
  → != pre_step 且 != donor_missing，作者新断言绿
relative.hook_timing = pre_step   → 现测试不读
offline 单行 H：donor_missing/unexpressible
  → test_intervene_geometry_is_not_pre_step 仍绿
```

### CE-4 Prefill

```text
prefix_token_ids=[1,2,3]              → False   已锁
execute={prefill_hidden:[]}           → False   已锁
execute={refilled_prefix:True}        → False   已锁
execute={prefill_hidden:0}            → True    现测试绿
execute={prefill_hidden:[0.0]}        → True
execute={prefill_hidden:True}         → True
```

### CE-5 bootstrap

```text
噪声数据：interval [0.11, 0.89]，lo<hi     已锁 [δ,δ] 实现
r04 ρ=y 常数 length：interval [0.5, 0.5]  旧测试绿（估计量常数，不是 [δ]*n 实现）
```

### CE-6 C6-M-01 标签序（本轮攻击成功）

```text
helper(task.premises=p1,p2,p3；labels=p3,p2,p1) → ['p1','p2','p3']   单元绿
cmd_fit(--in-dir collect, --labels-dir label)：
  collect/tasks.jsonl 不存在
  label/tasks.jsonl 不存在
  task_for_e is None
  unique = ['p2','p1']          # labels 首次出现序
  E 列 = ['p1','p2']            # collect 按 task.premises
  Y 与 E 对反
应：fit/calibrate 必须读到 task.premises（或拒绝），truth_indices / Y 列与 E 同序
```

### CE-7 CLI analyze / e2e

```text
scientific labels 仅 3 条二元 task_label（门限 4）→ p1 is None
fixture 八阶段：offline H=[[1..8]]，scores=None，结论空
```

## 9. 发现

### F8-00 声明冻结哈希可复算

- **严重度：** —
- **状态：** 非缺陷建议（本轮过程正确）
- **文件：** `.planning/audits/round-08/VERSION.md` L5–23；工作区 60 文件
- **复现：** §1。本地 `1b88bec2…` == 声明。0 CRLF。
- **注：** 夹具仍在摘要外（F8-12）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F8-01 科学事件已排除题干 span；测试仍接受强制 `q=` 与「全文+平移」

- **严重度：** Medium
- **状态：** confirmed defect（验证残留；旧 prompt-as-events **不再复现**）
- **文件/行：** `tests/test_round06_regressions.py` L25–35；`tests/test_round05_regressions.py` L23–51；`models/generate.py` L137–190
- **复现：** §3 CE-1。6 轨迹事件全是 `\nq = <digit>`。`parse_region` 硬编码。
- **作者主张 A6-01 / B6-01 / F6-01：** **部分**（题干赋值不再当生成事件；generate 闭合仍是约束目标行）
- **修复：** 断言事件文本不在 `prompt_text`；或接受 `parse_status=constrained_target` 为 tiny 接口、不要把它写成 §4.1 自然 CoT 已测。

### F8-02 NaN 行数替身已锁；「不是末 token」仍是测试名

- **严重度：** Medium
- **状态：** confirmed defect（验证残留；NaN 行数 **不再复现**）
- **文件/行：** `tests/test_round05_regressions.py` L56–67；`models/collect.py` L50–62
- **复现：** H 全有限；本通道 `pre_idx=44≠50`。测试不比 last。
- **作者主张 D6-02 / F6-02：** **部分**（不可表达行不再入 H；步前≠末 token 没有 oracle）

### F8-03 科学路径不再用 `donor_missing` 满足 `!=pre_step`；`hook_timing` 仍是 `pre_step`

- **严重度：** Medium
- **状态：** confirmed defect（验证残留；点名 donor_missing 替身 **不再复现**）
- **文件/行：** `tests/test_round05_regressions.py` L118–131；`tests/test_round04_regressions.py` L115–124；`cli.py` L805–902；`models/collect.py` `intervene_swap_decode` L196
- **复现：** 行字段 `timing=offline_hidden`，`status=prospective_decode`。`relative.hook_timing=pre_step`。offline 测试仍锁 `unexpressible`。
- **作者主张 D6-02 / F6-03 / A5-08：** **部分**（科学行字段不再是 `unexpressible`；hook 元数据仍写步前；offline 旧替身还在）

### F8-04 `prefix_token_ids` 已拒；任意有限 dummy hidden 仍是 Prefill

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）
- **文件/行：** `repair.py` L147–149、L166–180；`tests/test_round06_regressions.py` L73–78
- **要求：** Goal §五.13；作者 F6-04「`prefix_token_ids` 或空 hidden 不得冒充 Prefill」
- **复现：** §3 CE-4。作者锁的 ids/空 hidden 为 False。`prefill_hidden=0`/`[0.0]`/`True` 为 True。
- **作者主张 F6-04：** **部分**（点名 prefix_ids 闭合；原 CE 的 `prefill_hidden=0` 未闭）

### F8-05 噪声数据上 `[δ,δ]` 已禁；旧测试仍接受真退化区间

- **严重度：** Low
- **状态：** 非缺陷建议（实现会重采样；r04 `[0.5,0.5]` 是常数 δ 的分位，不是 `[δ]*n` 短路）
- **文件/行：** `analysis.py` L196–212；`tests/test_round06_regressions.py` L81–93；`tests/test_round04_regressions.py` L192–200
- **作者主张 F6-05：** **作为「禁止退化实现」闭合。** 旧测试力度仍弱，不单独开缺陷。

### F8-06 C6-M-01：helper 测试锁住带 task 的序；CLI fit 回到 labels 首次出现序

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）
- **文件/行：** `cli.py` `_e_premise_ids` L662–671；`cmd_fit` L599–626；`tests/test_round06_regressions.py` L114–127；`models/collect.py` L72–80
- **触发：** 作者测试自己的 `collect --out-dir col` + `label --out-dir lab` + `fit --in-dir col --labels-dir lab`
- **要求：** 作者 C6-M-01「`truth_indices` / fit Y 列跟随 `task.premises`（E 序），不再用 labels 首次出现序」
- **复现：** §3 CE-6。`col/tasks.jsonl`、`lab/tasks.jsonl` 均不存在。`unique=['p2','p1']`。E 序 `['p1','p2']`。`_e_premise_ids(None, labels)` 就是首次出现序。calibrate 另有 `parent/prep` 启发式，fit **没有**。
- **影响：** 可以引用「已锁 E 序 / 0.1 vs 0.2」，同时生产 dual-head Y 与前提池化列对反。
- **修复：** fit/calibrate 必须从 prepare 上游或 traces 恢复 `task.premises`；缺 task 则拒。测试必须跑 CLI 反序 labels，断言 Y/truth 列与 E 对齐，而不是只调 helper。
- **作者主张 C6-M-01：** **未闭合**

### F8-07 analyze 标签测试不锁 P1；科学路径 p1 仍为 None

- **严重度：** Medium
- **状态：** confirmed defect（验证）
- **文件/行：** `tests/test_round05_regressions.py` L188–197；`cli.py` `cmd_analyze` L975–1062
- **复现：** scientific labels 仅 3 条二元 `task_label`（门限 4）→ `p1 is None`。测试不读 `p1`。
- **作者主张 A5-11：** **未闭合**

### F8-08 CLI / Goal e2e 仍接受未接通科学路径

- **严重度：** Critical
- **状态：** confirmed defect（验证）
- **文件/行：** `tests/test_cli_pipeline.py` L4–30；`cli.py` offline collect / analyze
- **复现：** §3 fixture 八阶段。与 F6-08 同类。
- **作者主张 F4-01 / F5-01 / F6-08 e2e：** **未闭合**

### F8-09 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：69 行 `verification_method=python -m pytest -q`；320 行 `passed_local_tests`。可执行行 159 条仍为 `tests_exist_not_acceptance`。`.planning/phases/06-acceptance/06-VERIFICATION.md` L8 仍写 **136 passed**（本冻结是 144）。
- **作者主张 A5-02 / F6-06：** **部分**（可执行行 status 未退回 pytest；协议行与 06-VERIFICATION 数字仍旧）

### F8-10 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes`、`assert_disjoint`、`card`、`apply_model_template`

### F8-11 点名旧 CE 本轮未复现（不要写成 Goal 验收）

- **严重度：** —
- **状态：** 非缺陷建议
- **闭合的点名替身：** 题干赋值入事件；NaN H 行数；科学 intervene 靠 `donor_missing`+`!=pre_step`；`prefix_token_ids` 当 Prefill；噪声数据上的 `[δ,δ]` 实现。verbalizer 17/70/boxed、span `[]`、analyze 无 in-dir、Week8 阈值无测量仍在。

### F8-12 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`；`VERSION.md` 范围
- **影响：** oracle 字节可动而不改 `.py`+toml 聚合

### F8-13 ISSUES `author closed` 高估 C6-M-01 与 Prefill

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为验证闭合：** F6-01 题干 span；F6-02 NaN 行入 H；F6-03 科学路径 `donor_missing` 替身；F6-05 `[δ,δ]` 实现；F6-04 的 prefix_ids/空 hidden；前轮 B/C/D 单元 oracle。
- **未闭：** C6-M-01 CLI（F8-06）；`prefill_hidden=0`（F8-04）；e2e（F8-08）；analyze P1（F8-07）；账本协议行（F8-09）。
- **不要用本通道把 Goal/需求标 Complete。** 上表单元闭合 ≠ 科学验收。作者关闭无效。

### F8-14 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、`offline_prefix_ids`、宿主 `subprocess`、`executor_unavailable` 不得改写成服务器验收。C6-M-01 CLI 错序与 dummy hidden 是 **有名字的本机代码** 缺口，不是 `pending_server`。

### F8-15 非缺陷说明

- **状态：** 非缺陷建议
- `VERSION.md` 算法可复现。保持脚本冻结。
- 相对本通道 r06：generated-region 解析、跳过不可表达 H、科学 intervene 真正做几何/hook、prefix_ids 拒答、bootstrap `lo<hi`、catalog 别名、下游无 `--in-dir` 拒——这些是真改进。
- `consecutive_pass_count: 0` 与「144 passed ≠ Goal」比把套件当验收更诚实。
- 约束 `\nq = <digit>` 作者已标为 tiny 接口、不是自然 CoT；本通道同意不把它升格为 High 实现洞，但测试不得暗示 generate 已闭合。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**当前测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 69 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F8-09）。C6-M-01 行被 helper 填绿（F8-06）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F8-06、F8-04、F8-08 为已确认遗留。ISSUES 作者关闭无效。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 144/0，无 skip 伪装。e2e 是 exit-code 烟测并断言空结论。C6-M-01 有测试，但锁替身。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** 账本页眉仍禁止用 pytest 关可执行行（好）。`06-VERIFICATION.md` 仍写 136 passed（坏）。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 哈希匹配（好）。`VERSION.md` `consecutive_pass_count: 0`。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。本文件属于审查日志，不改变 60 文件摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：fit Y 错序、dummy hidden、offline 前缀 H、宿主 subprocess 都是 **有名字的代码** 缺口。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F8-13）。本机 pytest 记录存在（144/0）。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。sham hit 不记已评估 0 有测。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。collect 跳过不可表达行。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。fit Y 与 E 在 CLI 上对反。rollout 无数值测试。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。helper 上的 `truth_indices` 有。CLI 无 task 时回到首次出现序。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；C-layer **开发集** | 科学路径现做几何+hook。行 timing 为 `offline_hidden`。`hook_timing` 仍 `pre_step`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。噪声 bootstrap 有宽度。analyze 常不建 P1。 |
| 13 附录修复 | 新前缀 Prefill；几何/锥 | ids/空 hidden 拒；标量 0 仍 True。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册 / 阈值无测量有测。 |
| 15 代码任务 | 显式隔离执行器；普通 subprocess ≠ 沙箱 | spy + `isolated_sandbox is False` 已锁。默认仍 Unavailable。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **144 passed，exit 0，18.72s，144 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH。** 声明与复算均为 `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`（60 文件）。逐文件 SHA-256 见 §2。 |
| 独立性 | 新真 oracle：题干 span 排除、H 有限、科学 intervene 非 `donor_missing`、`prefix_ids` 非 Prefill、噪声 bootstrap `lo<hi`、无 `--in-dir` 拒、catalog 别名。**不独立：** C6-M-01 helper、offline H e2e、强制 `q=` 当 generate、H 测试名 vs last-token、`hook_timing`、dummy 有限 hidden、offline `unexpressible` 几何测试。 |
| Mock/stub | offline 前缀 H + calibrate `scores=None` + analyze 忽略不足 labels + helper 自带 task + repair 有限标量 hidden + `not_evaluated` 编码为成功。比 `unittest.mock` 更差。 |
| 论文行为仍未证明 | CLI 上 E/Y 同序、真 Prefill（非任意有限数组）、从 labels 建的 P1、隔离执行、T2 reversing、自然 CoT 事件 |
| 交付 vs 测试 | 「144 passed / r06 已本地关闭 / C6-M-01 已锁」**超过** 测试力度 |
| 已确认问题？ | **是。** Critical：F8-08。High：F8-06、F8-04。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 空的「看起来没问题」不适用。绿 pytest 不是验收。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷。即使 A–E 全写「通过」，只要 F 确认缺陷，两轮计数必须保持 0；修复后换 hash 重开。 |

在 CE 级测试锁住 C6-M-01 的 **CLI fit/calibrate 列序**、dummy 有限 hidden、以及 e2e 不再用 offline 前缀 H 冒充闭合之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。
