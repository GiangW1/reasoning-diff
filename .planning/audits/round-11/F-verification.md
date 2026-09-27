# F：验证质量与反向质疑（round-11）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-11 其他通道报告。`ISSUES.md` 只当作者主张。点名项在 scratch 脚本里独立复跑，不以作者测试绿当作论文行为已锁。`python -m pytest -q` 绿不是论文正确性，也不是 Goal 验收。

**先行结论：** 开审时按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`（61 文件，0 CRLF）。本机对该树 `python -m pytest -q` 为 **155 passed / exit 0**。这不是 Goal 通过。七个点名独立攻击（scratch，不引用作者测试作证明）：**B9-01 sham 广播**在开审字节上不再把真实前提写入 \(N\)，scientific `rho_M_excess` 为 null；**标量 Prefill** 拒绝 `0`/`True`/`[0]`/`[0.0]`/`[]`；**假 P1** 不会从 labels 伪造；**T3 prepare** 不写 `source_value_pair`；**\(n<d\)** 标 `truncated` 且 \(n\ge d\) 不截断；**CLI `tasks.jsonl` 列序**在找得到任务文件时 Y/`scores` 跟 `task.premises`（\(a=0.1\) 不是 \(0.2\)）。**族锁未闭：** 孤立 `gsm8k-1` Symbolic 仍是 `probe_train`。作者测试仍锁替身：scientific sham 用 `excess!=1.0 or null_reason`；C6 只查 `tasks.jsonl` 存在与 `probes.jsonl` 存在；Plus 锁族先加载 Plus，不测孤立 `gsm8k-1`；\(n<d\) 单侧由 r05 互补。交卷前磁盘已漂离声明冻结（`cli.py` / `splits.py` / `tests/test_round07_regressions.py`），聚合 **`0816fa5b…` ≠ `7518e20b…`**。事后 persist 文件与「无 `tasks.jsonl` 则 raise」**不得**回写成冻结已闭。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689` |
| 开审复算 | `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | **`0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`**（仍 61 文件） |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明/开审/交卷皆 **61**。变的是字节，不是文件数。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest（开审冻结树） | **155 passed in 24.13s，exit 0。** Collect：**155 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 范围 | 开审时全部 `tests/**`（18 个 `.py` + 10 个夹具 JSON）及测试触及的生产符号。交卷后 `test_round07_regressions.py` 200→224 行、`cli.py`/`splits.py` 被第三方改写，**不作本冻结套件**。 |
| 明确未读 | `.planning/audits/round-11/{A,B,C,D,E}-*.md` |
| scratch | `%TEMP%\f11_verification_hunts.py`、`%TEMP%\f11_hunts_rest.py`。未写入 `src/` / `tests/` / `pyproject.toml`。 |

审查对象首先是**声明冻结字节**（开审复算一致后对该树跑 pytest 与七个点名攻击）。交卷时磁盘已变，**不能**把事后补丁写成冻结已闭。作者 `pytest_author_claim: 155 passed` 仅作为开审命令结果被独立确认。

漂变文件（开审 inventory SHA-256 → 交卷）：

| 文件 | 开审 | 交卷（观察） |
|---|---|---|
| `src/reasoning_diff/cli.py` | `29ad6e40…` / 1255 行 | `175abf12…` / 1254 行。`_find_tasks_jsonl` 改为向上 4 层并加入 `collect`/`col`；fit/calibrate 缺 `tasks.jsonl` 时 `raise` |
| `src/reasoning_diff/splits.py` | `08f77e97…` / 152 行 | `40ab4021…` / 184 行。进程锁外写 `.planning/research/.cache/gsm_test_only_families.json` |
| `tests/test_round07_regressions.py` | `e4228445…` / 200 行 | `1ffdbd7e…` / 224 行。新增 `test_fit_without_tasks_jsonl_refuses_first_seen_order`；Plus 测里 `_TEST_ONLY_FAMILY_KEYS.clear()` 后仍断言 `test` |

本通道未写这些文件。

## 2. 逐文件覆盖

以下行数/SHA-256 是 **开审 HASH_MATCH** 时的 61 文件（冻结树）。

### 2.1 测试（冻结树全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍 `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a3…` | r03 节点；P1 泄漏用例仍绿；`ie_z` 单元仍是隐均值 helper |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline 几何仍只 `!= pre_step`；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；**\(n\ge d\) `truncated is False`**（eye4/eye3） |
| `tests/test_round06_regressions.py` | 145 | `ac7e4e88248ff49e…` | 字段名 donor/INLP/`ie_z_g`；C6 helper；prefix_ids 拒 |
| `tests/test_round07_regressions.py` | 200 | `e422844573a17059…` | 点名项：collect 复制存在、标量 Prefill、T3 无 SVP、Plus 先加载再锁、analyze `p1 is None`、\(n<d\) True、sham 不广播、scientific 弱 or、C7-M-01 手填 `noise_set` |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only（开审）：**155 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r09 的 144 节点：+11，主要在 `test_round07_regressions.py`。

### 2.2 生产相对测试（开审冻结）

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | r04 常数 δ 仍 `[0.5,0.5]`；泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | `attention_mean`/`rollout` 无数值 oracle |
| `cli.py` | 1255 | `29ad6e40e2fb50df…` | smoke offline；scientific prepare/collect/fit/intervene | fit 靠 `_find_tasks_jsonl` 兄目录启发式；C6 测试不锁 Y/`scores`；analyze 只读 `p1_table.jsonl` |
| `edits.py` | 287 | `cacb63ac27cbcccf…` | value/rename/source-value 元数据 | 同值异源是否真第二来源 |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；`ie_z` helper 仍是均值差 | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 392 | `b15fb8a5bb92220f…` | 事件均值；sham 不广播（新测） | 聚合 dens **不**上提 `null_reason`；C7-M-01 手填 `noise_set` |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token；不比各 mode generated_ids |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 201 | `07493570c6410e6b…` | `start>=len(prompt)` | 事件全是教员强制 `q=` |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` 未断言 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | **CLI 反序 labels 无作者数值锁** |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | prefix_ids / 空 hidden / 标量 0/`True`/`[0]` | `[0.0]`/`size<2` 靠独立攻击补 |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 152 | `08f77e972927a996…` | Plus→test（先加载）；`assign_family` | **孤立 gsm8k-1 不测**；无持久化（开审） |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | `card` 无 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f…` | family / 隔离 | 官方无 `original_id` 仍 `q:` 族键 |
| `tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354…` | sidecar | 无 sidecar 的 CLI prepare 崩 |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` 未断言 |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；口语 `needs_truth` | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584；\(n<d\) truncated；eye4 不截断 | `apply_map` 数值恢复未锁 |

夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `7518e20b…b28e689`（61 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 交卷再算 | 同脚本 | **HASH_MISMATCH** `0816fa5b…93de3b`。`cli.py` / `splits.py` / `test_round07_regressions.py` 已改。 |
| 全量 pytest | 开审时仓库根 `python -m pytest -q`（`pythonpath=src`） | **155 passed in 24.13s，exit 0**。无 skip/xfail/deselected。 |
| Collect | `python -m pytest tests --collect-only -q` | 155 nodes，collect exit 0（开审） |
| skip/xfail/`assert True` | 对当时 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；TO 0.5；σ(1)；`[0.7,0.4]`；C6 \(1-0.9=0.1\) | **存在的单元断言**与独立算术一致 |
| **B9-01 sham 广播**（scratch） | `build_labels` + `event_density_sets` + scientific `prepare --sham-opportunities 1` | **实现闭合。** 真实行 `noise_ref is None`；`sham:q` 为 1.0；\(N\) 缺失；`rho_M_excess is None`；event `null_reason=noise_set_missing`。scientific：q `82→53`（changed），仍不入账。手填真实+sham 广播仍走 sham 分支，不入账。无 `sham:`、仅真实 `noise_ref=1` → C7-M-01 入账 `rho_M_excess=1.0`（作者声称的仅无 sham 路径）。 |
| **标量 Prefill**（scratch） | `run_repair` + `_hidden_is_prefill` | **实现闭合。** `0`/`1`/`1.0`/`True`/`False`/`[]`/`[0]`/`[0.0]`/`[1.0]`/`[0,0]`/`np.array(0)` → `refilled_prefix=False`。`[0.1,-0.2]` 与 2-向量 → True。`prefix_token_ids` 仍拒。 |
| **假 P1**（scratch） | `analyze` 只给 labels（含 length/op/rho/y/held_out） | **实现闭合。** `p1 is None`，`status=not_evaluated`。对照：`p1_table.jsonl` 混类 held-out → `p1.status=estimate`（不是「analyze 永不建 P1」）。 |
| **T3 prepare**（scratch） | CLI hotpot/musique/humaneval/t4 + `_try_source_value_pair` | **点名项闭合。** 四处 rc=0，无 `source_value_pair`。T3 函数返回 None；T1 仍能配对。作者测不覆盖 HumanEval。 |
| **\(n<d\) truncated**（scratch） | `common_dim_then_procrustes` + analyze `geom_*.jsonl` | **实现闭合。** (2,5)/(2,3) 与 (1,2) → `truncated=True` / `not_applicable_too_few_rows`。eye3、eye4/eye3、n=d=1 → False。1-D → shape_mismatch。CLI appendix 与库层一致。 |
| **族锁**（scratch） | `assign_split` / `split_for_task` / CLI prepare | **未闭。** `gsm8k-1` 孤立 = `probe_train`，`locked=False`。先 Plus 再 Symbolic → `test`。`gsm8k-12` **无锁也是 test**（哈希落入 15% test 桶）。无 sidecar 的 Symbolic CLI prepare：`ValueError: no editable non-placeholder premise`。官方 Plus 无 `original_id` 族键仍是 `q:`。 |
| **CLI `tasks.jsonl` 列序**（scratch） | 构造 \(E=I_3\)，\(\hat p=(0.9,0.1,0.8)\)，labels `[p3,p2,p1]`，\(R=\{p1\}\)；spy `BilinearProbe.fit` | **找得到 task 时实现闭合。** helper 有 task → `[p1,p2,p3]`，`a≈0.1`；无 task → 首次出现 `[p3,p2,p1]`，`a≈0.2`。孤立 calibrate `scores≈[0.1]`。仅 p2 + 事件 s2 → `0.9`。fit Y `[1,0,0]` 不是 `[0,0,1]`。作者路径 collect **确实复制** `tasks.jsonl`；label **不**复制。删掉 collect 副本后，开审 `_find_tasks_jsonl` 仍命中兄目录 `prep/tasks.jsonl`。 |
| 对抗：NaN H / last-token | 未作为本轮点名重跑；开审代码与 r09 同 collect 路径 | 测试仍不比 last-token |
| 对抗：fixture 八阶段 | 读 `test_full_cli_smoke` | 仍 `--backend offline`，断言空结论 |
| 账本 | `.planning/PAPER_TRACEABILITY.md` | `python -m pytest -q`：**70**。`passed_local_tests`：**100**。`tests_exist_not_acceptance`：**159**。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed**。 |
| 事后抽查（非冻结） | 漂后 fit/calibrate `raise`；`_find_tasks_jsonl` 上溯 4 层；persist JSON | 同一 temp 树里「无本地 tasks」的 odd/iso **仍找到** 兄目录 `col/tasks.jsonl`，**不 raise**。作者新拒测把 orphan 与 `run/prep` 错层，测不到这条启发式。persist 文件被写出（本通道 hunts / 漂后 `load_gsm_plus`）。**不得**记入冻结闭合。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-11 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 对漂后 61 文件套件重跑 pytest 当冻结证据 | 那已不是声明 hash。开审 155 不得写成「当前树」。 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| 把 persist 缓存当交付物验收 | 不在冻结摘要内 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 155 passed | `VERSION.md` | **开审命令是。** 当作阶段/Goal 证据：**否。** 交卷磁盘已不是该冻结。 |
| B9-01：sham 不广播进真实 \(N\) | `ISSUES.md` / `VERSION.md` prior | **实现：独立确认闭合。** 作者 scientific 测是弱 or；单元测锁 `noise_ref` 与 `rho_M_excess is None`，可用。 |
| 标量/`[0]` Prefill 拒绝 | ISSUES F6-04 | **实现闭合。** 作者测覆盖 `0`/`True`/`1.0`/`[0]`/`[]`。 |
| analyze 不伪造 P1 | ISSUES C7-M-02 | **实现闭合。** 测试只喂 4 行 labels，不喂 ρ 字段；代码路径只读 `p1_table.jsonl`，独立加字段仍不伪造。 |
| T3 prepare 跳过 SVP | ISSUES E7-19 | **实现闭合。** 测试只锁 hotpot/musique **无该 kind**，不锁 HumanEval，不锁「prepare 真的写出合法 task」。独立补了 HE/T4。 |
| \(n<d\) 标 truncated | ISSUES C7-M-03 | **实现闭合。** 作者新测只锁 True 侧；False 侧靠既有 `test_common_dim_is_not_silent_truncate`。 |
| Plus 注册族锁 | ISSUES B5-01 | **测试不支持孤立路径。** 先加载 Plus 再断言 Symbolic=`test`。孤立 `gsm8k-1` 仍 `probe_train`。夹具 `gsm8k-12` 无锁也是 `test`。 |
| collect 复制 `tasks.jsonl`；fit 跟 E 列 | ISSUES C6-M-01 | **复制有测。列序无测。** `test_collect_copies_tasks_so_fit_follows_e_order` 只断言文件存在 + fit exit 0。独立 spy 才看到 \(Y=[1,0,0]\)。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未全部重跑数值）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham∉R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键（有 `original_id` 的夹具）；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击 — 实现侧闭合（测试仍可能是替身）：**

- **B9-01 不再广播。** 把 `build_labels` 改回给真实前提写 `noise_ref=1.0`，现 `test_sham_hits_do_not_broadcast_real_premises_into_n` 会红。scientific 弱测仍可能绿（见 §6.2）。
- **标量 Prefill 已拒。** 把 `_hidden_is_prefill` 改回 `isfinite.any()`，`test_scalar_prefill_hidden_is_not_prefill` 会红。
- **假 P1。** 若 `cmd_analyze` 从 labels 的 rho/y 建 P1，`test_analyze_refuses_fake_p1_from_labels` 会红。
- **T3 无 SVP kind。** 若 hotpot prepare 写入 `source_value_pair`，现测会红。把 SVP 改成别的 kind 名仍绿。
- **\(n<d\) truncated=True。** 恒 `truncated=False` 会红。恒 `True` 则本测仍绿，r05 eye4 测会红。
- **有 `tasks.jsonl` 时列序。** 现测试**不会**因 Y 错序而红。

**本冻结点名攻击失败 = 实现未闭：**

- **孤立 Symbolic `gsm8k-1` = `probe_train`。** 现测试绿（根本不跑这条）。

### 6.2 无效、自指或过弱（含本轮点名替身）

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_scientific_sham_does_not_book_rho_m_excess_one` | **B9-01 弱 or。** `rho_M_excess != 1.0 or null_reason`。聚合 dens **没有**顶层 `null_reason`（只在 `events[]`）。`excess is None` 时 `None != 1.0` 为真；`excess=0.5` 也会绿。真正有力的是同行对 p1/p2 `noise_ref is None`。 |
| `test_sham_hits_do_not_book_evaluated_zero_noise` | 仍只查 `rho_S_noise is None` 或 null_reason。S 分母空时即使 N 被填满也绿。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set=["p3"]`。不经 `build_labels`，不经 sham 广播。 |
| `test_collect_copies_tasks_so_fit_follows_e_order` | **C6 替身。** 锁复制与 `probes.jsonl` 存在。不锁 Y 列、不锁 calibrate `0.1`、不锁反序 labels。兄目录名恰好是 `prep`，即使不复制也能 `_find_tasks_jsonl`。 |
| `test_truth_indices_follow_e_columns_not_label_order` | 仍是带 `task.premises` 的 helper。不跑 `cmd_fit`/`cmd_calibrate`。 |
| `test_plus_locks_symbolic_family_to_test` | **族锁替身。** 先 `load_gsm_plus` 再断言 Symbolic=`test`。不测 `clear` 后孤立 `gsm8k-1`。夹具族 `gsm8k-12` 无锁也是 `test`。官方 Plus 只锁文本键，不要求族 ID=`gsm8k-*`。 |
| `test_common_dim_marks_truncated_when_n_lt_dim` | 只锁 True。单独看是单侧；r05 `truncated is False` 补了另一侧。 |
| `test_t3_prepare_survives_source_value_pair` | 只锁「没有这个 kind 字符串」。不锁 HE，不锁 `_try_source_value_pair is None`。 |
| `test_analyze_refuses_fake_p1_from_labels` | 正确方向，但无阳性对照。本通道独立补了 `p1_table`。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 donor/INLP/`ie_z` | 仍锁字段名，不锁 `trace_id` / decode 差 / 非恒 0 的 \(g(Y)\)。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |
| （漂后）`test_fit_without_tasks_jsonl_refuses_first_seen_order` | **不在声明冻结。** 且 4 层上溯 + `col` 兄名可在同树静默找到 `tasks.jsonl`（本通道 `FIT_NOTASK NO_RAISE`）。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]`；analyze 标签不够建 P1；smoke **要求** 空结论。
2. **C6 用「文件存在」盖住列序。** collect 复制是真的；fit 测试不读 Y。开审缺文件时 `_e_premise_ids(None)` 回退首次出现序。
3. **族锁用加载顺序盖住孤立 prepare。** 寄存器是进程全局（开审）或外加未入冻结摘要的 JSON（漂后）。catalog 一次一种 snapshot；prepare **不传 siblings**。
4. **B9-01 scientific 用弱 or 盖住聚合层没有 `null_reason`。**
5. **INLP/C-rand/rescue「分 decode」仍是 mode 字符串**（本轮未点名重跑 decode）。
6. **科学事件非空，来源仍是教员强制 `q=`。**
7. **账本协议行仍 pytest；可执行行 `tests_exist_not_acceptance`。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes` 恢复、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已在 **声明冻结树** 上执行（族/列序的数值以 scratch 为准）。本通道未加测试。漂后行为标为「另一哈希」。

### CE-1 B9-01 sham 广播（实现攻击失败；scientific 测试偏弱）

```text
build_labels( sham changed 82→53, 真实 p1/p2 ):
  (q,p1).noise_ref = None
  (q,p2).noise_ref = None
  (q,sham:q).noise_ref = 1.0
  dens.rho_M_excess = None
  events[0].null_reason = noise_set_missing

scientific prepare --sham-opportunities 1:
  同样 change；顶层 dens.null_reason 缺省（聚合不上提）
  作者: excess!=1.0 or null_reason  → 因 excess is None 而绿

手填真实+sham 皆 noise_ref=1.0:
  仍 noise_set_missing（sham_hits 优先）

无 sham: 行、真实 noise_ref=1.0:
  N={p1,p2}, rho_M_excess=1.0     # C7-M-01 有意路径

应：scientific 断言 events[].null_reason 与 excess is None；禁止顶层弱 or
```

### CE-2 标量 Prefill（实现攻击失败；测试基本锁住）

```text
0 / True / 1.0 / [0] / [0.0] / [] / [1.0] / [0,0] → False
[0.1, -0.2] → True
prefix_token_ids → False
作者已锁 0/True/1.0/[0]/[]
```

### CE-3 假 P1（实现攻击失败）

```text
labels 带 length/op/rho/y/held_out、无 p1_table.jsonl → p1 is None
有 p1_table 且 held-out 两类 → p1.status=estimate
```

### CE-4 T3 prepare（点名项攻击失败）

```text
hotpot/musique/humaneval/t4 prepare rc=0，edits 无 source_value_pair
_try_source_value_pair(T3)=None；T1 仍非 None
```

### CE-5 \(n<d\) truncated（实现攻击失败；新测单侧）

```text
ones(2,5), ones(2,3) → truncated True
eye(4), eye(3) → False          # r05 已锁
ones(1,2) → True
向量 1-D → shape_mismatch
恒 True 会骗过 test_round07 新测，骗不过 r05
```

### CE-6 族锁（攻击成功 — 冻结未闭）

```text
assign_split("gsm8k-1", source=gsm_symbolic) = probe_train
clear 后孤立 Symbolic gsm8k-1: split=probe_train, locked=False
先 Plus(gsm8k-1) 再 Symbolic: test, locked=True     # 作者只锁这条
assign_split("gsm8k-12") = test                     # 夹具无锁也是 test
官方 Plus 无 original_id: family=q:… ≠ gsm8k-12
CLI symbolic 无 sidecar: ValueError no editable premise
CLI plus: role=test

应：孤立 gsm8k-1（及 CLI 无 siblings）不得进 probe_train；
    族键必须共组，失败显式 unmapped；锁持久化进冻结摘要内的清单，而不是模块 set / 摘要外 JSON
```

### CE-7 CLI 列序（有文件：实现攻击失败；作者测试不锁；无文件：开审回退）

```text
E=I_3, p-hat=(0.9,0.1,0.8), labels 序 [p3,p2,p1], R={p1}
  helper+task → cols=[p1,p2,p3], a=0.1
  helper 无 task → [p3,p2,p1], a=0.2
  孤立 CLI calibrate（collect 内有 tasks.jsonl）→ scores≈[0.1]
  仅 p2 + node s2 → 0.9
  CLI fit spy Y[0]=(1,0,0)

开审无 tasks.jsonl：首次出现序（C9-U-01）
作者 test_collect_copies_*：不读 Y/scores

漂后（不得计入冻结）：缺文件 raise；但 4 层上溯可找到兄 col/tasks.jsonl
  → 本通道 FIT_NOTASK / CAL_NOTASK 未 raise

应：fit/calibrate 断言反序 labels 的 Y 或 scores；缺任务文件拒绝；
    查找不得跨无关兄目录静默成功
```

## 9. 发现

### F11-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）
- **文件：** `.planning/audits/round-11/VERSION.md` L5–23；开审 61 文件 = `7518e20b…`；交卷 61 文件 = `0816fa5b…`
- **复现：** 开审脚本原文 MATCH。审查期间 `cli.py`、`splits.py`、`tests/test_round07_regressions.py` 被改（本通道未写）。这是 **另一哈希上的补丁**，不能当作本冻结已闭。
- **注：** 夹具仍在摘要外（F11-12）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F11-01 B9-01：sham 不再广播进真实 \(N\)；scientific 测试仍弱

- **严重度：** Medium（验证残留）；点名实现 **本轮攻击失败**
- **状态：** confirmed defect（验证替身）；实现闭合
- **文件/行（冻结树）：** `measure.py` `build_labels` 72–80；`event_density_sets` 328–349；`cli.py` scientific sham 观测；`tests/test_round07_regressions.py` `test_scientific_sham_does_not_book_rho_m_excess_one`
- **复现：** §3 / CE-1。`82→53` 仍发生，不入账。
- **作者主张 B9-01：** **实现同意关闭。** scientific 作者测不得单独当证明。

### F11-02 标量 Prefill 已拒

- **严重度：** —
- **状态：** 非缺陷（实现闭合；测试基本独立）
- **复现：** §3 / CE-2。作者主张 F6-04 residual：**本冻结同意关闭。**

### F11-03 analyze 不从 labels 伪造 P1

- **严重度：** —
- **状态：** 非缺陷（实现闭合）
- **复现：** §3 / CE-3。作者测无阳性对照，不升格。

### F11-04 T3 prepare 跳过 SVP

- **严重度：** Low（验证覆盖）
- **状态：** confirmed defect（覆盖缺口，非实现）
- **复现：** 作者不测 HumanEval；独立 HE/T4 亦无 SVP。
- **作者主张 E7-19：** **实现同意关闭。**

### F11-05 \(n<d\) 标 truncated；新测单侧

- **严重度：** Low（验证）
- **状态：** 非缺陷（实现闭合；r05 补了 False 侧）
- **复现：** §3 / CE-5。

### F11-06 族锁：孤立 `gsm8k-1` 仍 `probe_train`（B5-01 未闭）

- **严重度：** High
- **状态：** confirmed defect（实现 + 验证）
- **文件/行（冻结树）：** `splits.py` `assign_split` / `split_for_task` / `_TEST_ONLY_FAMILY_KEYS`；`t2_gsm_plus.py` `register_test_only_family`；`cli.py` `cmd_prepare` 不传 `siblings`
- **复现：** §3 / CE-6。`assign_split("gsm8k-1")=probe_train`。夹具 `gsm8k-12` 无锁=`test`（坏 oracle）。无 sidecar Symbolic CLI prepare 崩溃。
- **作者主张 B5-01：** **未闭合（本冻结）。** 交卷后 persist JSON **不得**记入本条关闭。

### F11-07 C6-M-01：有 `tasks.jsonl` 时列序正确；作者测试不锁；开审缺文件回退首次出现序

- **严重度：** High（验证）；开审缺文件为 Medium（实现残留）
- **状态：** confirmed defect（验证）。实现在 **找得到 task** 时闭合。
- **文件/行（冻结树）：** `cli.py` `_e_premise_ids`、`_find_tasks_jsonl`、`cmd_fit`/`cmd_calibrate`；`test_collect_copies_tasks_so_fit_follows_e_order`；`test_truth_indices_follow_e_columns_not_label_order`
- **复现：** §3 / CE-7。独立 calibrate \(a\approx0.1\)；fit \(Y=(1,0,0)\)。作者测不读这些数。
- **开审缺文件：** `_e_premise_ids(None)` → `[p3,p2,p1]` → \(a=0.2\)。
- **作者主张 C6-M-01 residual：** **部分**（复制+有文件列序闭；测试与缺文件未闭）。漂后 raise / 4 层查找 **不得**回写。

### F11-08 CLI / Goal e2e 仍接受未接通科学路径

- **严重度：** Critical
- **状态：** confirmed defect（验证）
- **文件：** `tests/test_cli_pipeline.py`
- **复现：** `--backend offline`；断言 `scientific_conclusion is None`。

### F11-09 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：70 行 `python -m pytest -q`；100 行 `passed_local_tests`；可执行 159 行 `tests_exist_not_acceptance`。`06-VERIFICATION.md` 仍写 **136 passed**（本冻结作者称 155）。

### F11-10 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes` 恢复、`assert_disjoint`、`card`、`apply_model_template`

### F11-11 donor / INLP / `ie_z` 字段名替身仍在（非本轮点名，残留）

- **严重度：** Medium
- **状态：** confirmed defect（验证残留）
- **文件：** `tests/test_round06_regressions.py` L65–74；`test_ie_z_and_rescue_controls` 仍测隐均值 helper

### F11-12 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个，开审已读）

### F11-13 点名旧 CE 本轮未复现（不要写成 Goal 验收）

- **严重度：** —
- **状态：** 非缺陷建议
- **作为实现未复现：** B9-01 广播；标量 Prefill；假 P1；T3 SVP；\(n<d\) 不标 truncated；有 `tasks.jsonl` 时 C6 错序。
- **作为测试仍活的替身 / 实现仍开：** 族锁孤立路径；C6 存在性测试；scientific sham 弱 or；开审缺 `tasks.jsonl` 回退。

### F11-14 ISSUES / VERSION 作者关闭高于冻结验证力度

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为验证/实现闭合：** B9-01 实现；F6-04 标量 Prefill；C7-M-02 假 P1；E7-19 T3 SVP；C7-M-03 \(n<d\)；C6 **有文件**列序（独立，非作者测）。
- **未闭：** B5-01 孤立族（F11-06）；C6 作者测与缺文件（F11-07）；e2e（F11-08）；账本（F11-09）；冻结交卷漂移（F11-00）。
- **不要用本通道把 Goal/需求标 Complete。**

### F11-15 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess **不是** pending_server。孤立族锁、开审缺文件列序、交卷漂移也不是 pending_server。

### F11-16 漂后 persist / 4 层查找（观察，非冻结缺陷）

- **严重度：** —（对声明冻结）
- **状态：** 非本冻结对象；若将来冻结包含它们，须单独立项：摘要外 JSON 锁、查找跨兄目录静默命中。
- **路径：** `.planning/research/.cache/gsm_test_only_families.json`（审查窗口出现 `["gsm8k-12", "q:ada has…"]`）。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 70 行仍 `pytest -q`；100 行仍 `passed_local_tests`（F11-09）。C6 被存在性测填绿（F11-07）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F11-00、F11-06、F11-07、F11-08 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** 开审 `pytest -q` 确为 155/0。e2e 是 exit-code 烟测并断言空结论。点名项有测试，族锁与 C6 锁替身。交卷磁盘已变，不能再引用该 155 为「当前树」。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 仍写 136 passed。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。本文件是审查日志，不改变被审摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：孤立族 `probe_train`、开审缺文件列序、offline 前缀 H。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F11-14）。开审本机 pytest 记录存在（155/0）。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语有。T3 prepare 无 SVP 有。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | B9-01 实现闭；scientific 作者测弱。 |
| 5 划分 | 测试专用不进拟合 | Plus→test（先加载）有。孤立 Symbolic **无**。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。C6 列序作者测不锁。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。CLI 反序无作者数值锁。 |
| 9 迁移 | 4096/3584 拒；两输入都映射；\(n<d\) 不静默 | 维拒与 truncated 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。测试锁 transform **名**。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与假 P1 拒有。analyze 常不建 P1。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒（本冻结独立确认）。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **开审 155 passed，exit 0，24.13s，155 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **开审 HASH_MATCH `7518e20b…`（61）。交卷 HASH_MISMATCH（61，`0816fa5b…`）。** |
| 独立性 | 真 oracle：B9-01 不广播、标量 Prefill、假 P1、T3 无 SVP、\(n<d\)/ \(n\ge d\)、有 tasks 时 C6 \(0.1\) / \(Y=(1,0,0)\)、孤立 `gsm8k-1=probe_train`。**不独立：** C6 存在性测、Plus 先加载再锁、scientific sham 弱 or、offline H e2e、强制 `q=`、donor/INLP/`ie_z` 字段名。 |
| Mock/stub | offline 前缀 H + helper 自带 task + `prep/` 兄目录 + 进程族寄存器 + mode 字符串 + `not_evaluated` 编码为成功。 |
| 论文行为仍未证明 | 孤立族共组、缺 `tasks.jsonl` 的冻结 CLI 列序、分 decode 的 token、从自然 CoT 建的 P1、隔离执行、可变 \(g(Y)\) |
| 交付 vs 测试 | 「155 passed / B9-01 与 C6/族锁已关」**超过** 冻结树测试力度；族锁实现也未关 |
| 已确认问题？ | **是。** Critical：F11-00、F11-08。High：F11-06、F11-07。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。交卷哈希已漂。孤立族锁仍开。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。即使 A–E 全写「通过」，两轮计数必须保持 0；修复后换 **新** hash 重开。 |

在声明冻结上用 CE 级测试锁住 **孤立 `gsm8k-1` 不得 `probe_train`**、C6 的 **CLI Y/`scores` 数值**、以及 scientific sham 的 **event 级 null** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。事后在另一哈希上补 persist JSON / 缺文件 `raise` / 4 层查找 **不能**把本轮改写成通过。
