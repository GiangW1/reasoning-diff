# F：验证质量与反向质疑（round-19）

独立审查通道 F。未改 `src/`、`tests/`、`pyproject.toml`。未读 round-19 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 写在 `.planning/audits/round-19/_f_scratch/`，不把 `tests/test_round06_regressions.py` / `tests/test_round07_regressions.py` 当证明。

**先行结论：** 按 `VERSION.md` 原文复算，开审与交卷冻结哈希 **一致（HASH_MATCH）** `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`（61 文件，0 CRLF）。本机 `python -m pytest -q --tb=line` 为 **165 passed / exit 0 / 23.91s**，与作者 `pytest_author_claim: 165` 一致。这不是 Goal 通过。

独立 CE（31 条，不跑 r06/r07 测试模块）：r18 点名实现项 **实现闭**——`apply_rename_edit({p1:p2,p2:p1})` → `p2 = 4. p1 = 0. What is q = p2 * p1?`（顺序改写会变成 `p1 * p1`）；CLI intervene 70 字题干实际喂给 hook 的 ids **79**（不是 `[:64]`），`>96` 前缀 `ValueError` 拒截；`cmd_calibrate` 只查 `(labels_dir, src, feat_dir)`，兄 `lab/` 的 `WRONG_LAB` **未绑定**，有/无兄目录分数相同；`stage_a`/`stage_b` 与 `alpha`/`omega` 都能配上 `same_value_diff_source`，删 copy 后 fallback。scientific fit **写出** 四条 `refused_not_section8` 且无 score。**一条点名仍红：** 作者 `all(status==refused if baseline in S)` 在省略这些行时恒真，在 `refused+score=1.0` 时也真——过滤本身可空真。Fixture 八段仍 offline 前缀 H；scientific tiny 仍 `constrained_target`——按任务口径这是诚实项，**不**开成缺陷，也 **不** 当 MODEL-01 / 自然 CoT。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21 03:10–03:35（Asia/Shanghai） |
| 声明冻结 | `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb` |
| 开审复算 | `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb` |
| 交卷裁决 | **HASH_MATCH**（与声明同一摘要） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明 / 开审 / 交卷都是 **61**。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| pytest | **165 passed in 23.91s，exit 0。** Collect：**165 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 165 passed`。命令结果独立确认。当作 Goal / 阶段验收：**否。** |
| 范围 | 61 冻结文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。 |
| 明确未读 | `.planning/audits/round-19/{A,B,C,D,E}-*.md` |
| 独立 CE | `.planning/audits/round-19/_f_scratch/f19_ce.py` → `f19_ce_results.json`（31 条：30 闭 / 1 红）。未 import r06/r07 测试模块。 |

审查对象是**声明冻结字节**。pytest 与点名 CE 均在 HASH_MATCH 盘上执行。交卷哈希未漂。相对 r18 冻结，本树变了 `cli.py`（1267 / `95c58b93…`）、`edits.py`（367 / `cc8e2d23…`）、`tests/test_round07_regressions.py`（374 / `21340627…`）。

## 2. 逐文件覆盖

行数 / SHA-256 前 16 是本冻结 61 文件。

### 2.1 测试（全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍 `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a3…` | r03 节点；`apply_rename_edit({p1:alpha})` 单键；P1 泄漏用例仍绿 |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04；`timing != pre_step`；helper 上合法已评估空 \(N\)；bootstrap 非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；analyze 不锁 p1 |
| `tests/test_round06_regressions.py` | 146 | `b555ed24000400e1…` | `start>=len(prompt)`；`prep`/`col` 上 `donor_kind`；scientific fit 过滤 `status==refused_not_section8`（**可空真**）；sham 析取 |
| `tests/test_round07_regressions.py` | 374 | `21340627d362128d…` | r07 节点 + 本冻结三例：swap 题干/表达式；`_tiny_prefix_ids` 70/97 **只锁 helper**；`_find_labels_jsonl(feat)` **只锁 helper**；`stage_a`/`stage_b` 配对不删 copy |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer 形状、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only：**165 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。相对 r18（162）：本冻结 `test_round07` 为 **21** 例（+`test_rename_swap_is_simultaneous`、`test_tiny_prefix_ids_refuse_silent_truncate`、`test_calibrate_does_not_bind_sibling_lab_labels`）。这三例 **不是** 本通道证明；独立 CE 另跑。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | `ρ=y` 泄漏仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed；无 generate 不可用 | fixture CLI **echo 前缀**无测试红（诚实项）；`attention_mean`/`rollout` 作者无数值 oracle（本通道独立补了 disjoint/score_qa） |
| `cli.py` | 1267 | `95c58b934e1aceeb…` | smoke offline；scientific prepare/collect/fit/intervene；孤立 fit 拒；collect 复制 edits；`_tiny_prefix_ids` helper；`_find_labels_jsonl` helper | **CLI intervene 70/>96 无作者测试**；**`cmd_calibrate` 兄 `lab` 无作者测试**；scientific fit 过滤可空真；scientific calibrate 出有限 \(q\) |
| `edits.py` | 367 | `cc8e2d23592a3ab8…` | value/alt-source 图；rename `{p1:alpha}`；作者另有 swap 例（不当 oracle） | 三前提集合碰撞仍非作者指纹 |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP/范数 | `ie_z` helper 仍是均值差 |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 405 | `985b9d9328e4111f…` | 未知 \(M\)；`noise_ref=0` 手造；unit 噪声扣除 | 科学聚合层弱析取；C7 helper 不走 labels |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 200 | `6e6040394ac641c7…` | 全题干 + `>96` 拒 | r06 仍只锁 `start>=` |
| `models/tiny.py` | 120 | `c75d0f5325766612…` | hook 清理 + logits 变 | — |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | 一字一 token |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | — |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | `_hidden_is_prefill` 拒标量/`bool`/`[0]` | `[0.0,1.0]` 仍 True（合法向量） |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **作者零测试**（本通道独立：Spain/spain=1，Madrid≠Spain） |
| `splits.py` | 184 | `40ab4021d4dccc6e…` | Plus→test；RAM∪磁盘 | `assert_disjoint` 作者零测试（本通道独立会拒重叠）；作者不 spawn |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | `card` 无 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f…` | family / `register_test_only_family` | `"reversing operation"` 仍非 T4 |
| `tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354…` | sidecar；`shared_gsm_*` | — |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` 未断言 |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；口语 `needs_truth` | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy；prepare 不崩 | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids；prepare 不崩 | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584 拒；`n<d` truncated | `apply_map` 数值恢复未锁 |

夹具 JSON **不在冻结内**。`models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 仅包说明。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `b6db632f…96569eeb`（61，0 CRLF） |
| 交卷再算 | 同脚本 | **HASH_MATCH** 同一摘要 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **165 passed in 23.91s，exit 0**。无 skip/xfail/deselected |
| Collect | `python -m pytest tests --collect-only -q` | 165 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对冻结 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；顺序 swap 应变 `p2 * p1`；70/97 token | **存在的单元断言**与独立算术一致；swap/70/97 另由独立 CE 核 |
| **独立 CE** | `_f_scratch/f19_ce.py`（`PYTHONPATH=src`） | 31 条：30 闭 / 1 红。见 §3.1。 |

### 3.1 点名独立 CE（不信测试文件）

| CE | 独立结果（本冻结） | 作者测试是否锁住 |
|---|---|---|
| **`apply_rename_edit({p1:p2,p2:p1})` 不得变 `p1 * p1`** | **实现闭。** 题干 `p2 = 4. p1 = 0. What is q = p2 * p1?`，表达式 `p2 * p1`，父母 `[p2,p1]`，值 `p2=4`/`p1=0`。顺序 `str.replace` 对照是 `p1 = 4. p1 = 0. What is q = p1 * p1?`。三元循环 `{p1:p2,p2:p3,p3:p1}` 同时成立；`p1`/`p11` 不互吃。 | 作者新例锁同一题干。**不当 oracle。** `{p1:alpha}` 仍不锁重叠。 |
| **intervene 不得静默 cap=64；70 ok；>96 raise** | **实现闭（含 CLI）。** helper：`len(_tiny_prefix_ids("x"*70))==70`；`"x"*97` → `tiny intervene prefix exceeds context; refuse truncated prefixes`。源码无 `ids[:64]`。CLI 70 字 scientific 题干：spy `intervene_hidden_decode` 五次皆 **79 ids**（题干 70 + 生成区到事件），`prefix_truncated=False`。把 traces 前缀垫到 100 字后 CLI **raise**，不是截断。generate 70 完整、97 拒。 | 作者只锁 `_tiny_prefix_ids` helper。**不锁** `cmd_intervene` 是否仍切片、是否把 70 字题干喂进 hook。r06 仍只 `start>=`。 |
| **calibrate / `_find_labels_jsonl` 不得绑兄 `lab`** | **实现闭（helper + CLI）。** `_find_labels_jsonl(feat)` 在兄 `lab`/`label`/`labels` 都有 `labels.jsonl` 时仍 `None`。`cmd_calibrate` 实参只有 `(None, fit, feat)`，找到 `None`。兄目录种 `WRONG_LAB` 与干净布局写出 **同一** toy `scores`。`label_dirs.extend(parent/lab)` 已不在源码。 | 作者只锁 helper：`_find_labels_jsonl(feat) is None`。**不跑** `cmd_calibrate`。若 CLI 仍把 `feat_dir.parent/"lab"` 塞进查找，该例仍绿。 |
| **`stage_a` / `stage_b` 配对仍工作** | **闭。** collect 复制 edits。`donor_kind=same_value_diff_source`，unit pair `(0,3,same_value_diff_source)`。`alpha`/`omega` 同。兄 `prep`/`prepare`/`s-prep` 与父目录 edits **不**救命。删 `stage_b/edits.jsonl` → `same_identity_fallback`。 | 作者 `stage_a`/`stage_b` 不删 copy。loader 例只点名 `prep`。 |
| **scientific fit 过滤不得因省略 refused 行而空真** | **实现写出四行且无 score（闭）。作者过滤仍空真（红）。** 四条 baseline 皆 `refused_not_section8`，`score is None`。同一过滤函数：`[]` → True；`{verbalizer, refused, score=1.0}` → True。echo `generate_fn=λp.prefix` 在科学前缀上 `status=generated`，`score=1.0`，抽出 `82`。 | `test_scientific_h_is_finite_and_pairs_donor` L60 仍是 `all(... if baseline in S)`。不要求行存在，不禁 score 骑在 refused 上。 |
| **自然 CoT / MODEL-01 / offline H / `constrained_target`** | **不要求，不开缺陷。** fixture collect `H.shape==(1,8)`（`token_ids[:8]`）。scientific prepare 7 条轨迹皆 `parse_status=constrained_target`。作者 ISSUES 已承认。 | 测试不要求 §4.1 或 MODEL-01。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **`all(status==refused_not_section8 for row if baseline in {verbalizer,…})`** | 无此类行 → 空真。`refused+score=1.0` → 仍真。本冻结实现写了四行无分，所以作者绿是碰巧真的；过滤本身不要求存在。**点名仍红。** |
| **`_tiny_prefix_ids` helper 冒充 CLI 前缀合同** | helper 绿不能证明 `cmd_intervene` 不再切片。独立 spy 补上了。 |
| **`_find_labels_jsonl(feat)` 冒充 calibrate 不走兄 `lab`** | helper 绿不能证明 CLI 查找列表不含 `parent/lab`。独立 spy 补上了。 |
| **`start>=len(prompt)`** | 若 `prompt_text` 被截，事件仍可在截断后。r07 全题干补了 alt-source；70/97 作者不锁 generate CLI。 |
| **`prep`/`col` 目录名** | 复制 edits 后不再必要。删 col 的 edits 后 fallback。 |
| **`{p.premise_id}=={p1,p2,src_b}`** | 三前提 rename 也能凑出该集。作者还锁父母/表达式。 |
| **`rho_M_excess != 1.0 or null_reason`** | `None != 1.0` 单独过。 |
| **`null_reason in {…} or rho_M_noise is None`** | `noise is None` 单独过。 |
| **`rho_S_noise is None or null_reason in {…}`** | r06 析取仍在。 |
| **教员强制 `q=`** | echo CE 前缀含答案数字。科学事件 `any(q)` 仍可被强制行单独满足。**不**开成自然 CoT 缺陷。 |
| **offline H 当 e2e** | 八段 exit 0。`H`←`token_ids[:8]`。analyze 无 P1 表。smoke **要求**空结论。**诚实项。** |
| `timing != "pre_step"` | 任意其他字符串都绿。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_plus_locks_*` | 同进程 RAM clear。**不**新进程。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| pytest 后 persist 泄漏 | 165 passed 之后磁盘为 `["gsm8k-12", "q:ada has 4 apples…"]`。该文件不在 61 摘要内。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：页眉写 r19 须在 `b6db632f…` 上独立复核且 pytest 不得关可执行行；协议行仍用 `python -m pytest -q` + `passed_local_tests`；`executable_function` 计数仍写 **159**。 |
| scientific calibrate | 对 tiny 探针写出有限非conformity 分数（约 `0.005`）。不是论文校准。有/无兄 `lab` 分数相同。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-19 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 `_f_scratch` 与 §8 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| Plus persist 新解释器 | 本通道只确认套件后磁盘仍有 Plus 键；作者也不 spawn |
| 把 Goal 标 Complete | 本通道只评验证质量 |
| 把 offline H / `constrained_target` / fixture echo 开成缺陷 | 任务明确：除非作者把它们写成科学结果 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 165 passed | `VERSION.md` | **命令是。** 当作 Goal：**否。** |
| F18-03 `_rewrite_ids` 同时替换；`{p1:p2,p2:p1}` → `p2 * p1` | ISSUES | **独立同意。** 作者新例锁同一字符串；本通道不靠它。 |
| F18-08 intervene 不再 `ids[:64]`；超 96 拒绝 | ISSUES | **实现独立同意（CLI spy 79 ids + 100 字 raise）。** 作者只锁 helper。 |
| F18-12 `_find_labels_jsonl` 只读给定目录，不走兄 `lab` | ISSUES | **实现独立同意（CLI 查找列表无兄路径）。** 作者只锁 helper。 |
| F15-01 collect 复制 edits；配对只读 `in-dir` | ISSUES | **独立同意（含 prepare/s-prep/父目录/删 copy/`alpha`/`omega`）。** |
| A14-03 scientific fit 拒写假 §8 行 | ISSUES | **实现同意。** 作者过滤可空真——点名过滤猎项 **未闭**。 |
| A14-02 / A14-04 / D14-05 generate | ISSUES | 图 / `noise_ref=0` / generate 全题干：**实现同意。** |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` | **本套件不能作证。** 本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`（scientific+tiny）；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击：**

- **重叠 rename 必须同时替换。** 回到顺序 `replace` 会让独立 CE 红（`p1 * p1`）。**实现闭。**
- **intervene 前缀必须完整或显式拒。** 回到 `ids[:64]`：70 字题干会让 spy 看到 ≤64 或旧 `prefix_truncated=True`。100 字前缀必须 raise。**实现闭。**
- **calibrate 不得读兄 `lab`/`label`/`labels`。** 回到 `feat_dir.parent/"lab"` 会让 CLI spy 绑到 `WRONG_LAB` 或分数漂移。**实现闭。**
- **配对不得靠兄目录名 `prep`。** 回到兄弟行走会让独立 loader CE 红。`stage_a`/`stage_b` 在有 copy 时会红若配对丢了。**实现闭。**
- **scientific fit 必须写出 refused 行且无 generated/echo 分。** 实现写了。作者过滤在省略行时 **不红**。**过滤猎项未闭。**
- **真实前提 `noise_ref=0` 不得当已评估空 \(N\)。** 独立仍闭。
- **generate 必须保留全题干，或拒截断。** 49/70/97 独立闭。
- **自然 CoT / MODEL-01。** 不要求。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_scientific_h_is_finite_and_pairs_donor` 的 §8 断言 | 读了 probes，但是 vacuous `all`。省略四行仍绿。`score` 可骑在 refused 上。 |
| `test_tiny_prefix_ids_refuse_silent_truncate` | 只调 helper。不经 `cmd_intervene`，不 spy hook ids。 |
| `test_calibrate_does_not_bind_sibling_lab_labels` | 只调 `_find_labels_jsonl`。不经 `cmd_calibrate`。 |
| `test_generated_events_exclude_prompt_assignments` | 只锁 `start>=len(prompt)`。截断 `prompt_text` 仍绿。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 `donor_kind` | 目录名 `prep`/`col`。现在靠 copy 也能绿。不删 edits。 |
| `test_source_value_pair_rewrites_graph_ids` 的集合行 | 单独不够（三前提 rename 碰撞）。整例还锁父母/表达式/全题干，**该例整体仍独立。** |
| `test_rename_keeps_expression` | 单键非重叠。 |
| `test_rename_swap_is_simultaneous` | 锁对了实现合同。本通道不把它当证明；独立 CE 另核。 |
| `test_load_source_value_pair_does_not_walk_sibling_prep` | 只点名 `prep`。 |
| `test_intervene_pairs_source_without_prep_sibling_name` | 不删 copy。不证明无行走。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `!= 1.0 or null_reason`。 |
| `test_observed_real_noise_ref_without_sham_*` | 不锁 `null_reason`。 |
| `test_unknown_behavior_is_not_counted_as_m` | 只锁全未知。 |
| `test_plus_locks_symbolic_family_to_test` | 不 spawn。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。诚实，不是 MODEL-01。 |
| `test_p1_held_out_logistic_detects_rho` | `ρ=y` 在全部行。`monkeypatch` 未用。 |
| `test_tiny_hooks` L17 | 恒真。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。作者已承认——**不要超售成科学 e2e。**
2. **scientific fit 用「若存在则 refused」盖住「必须存在且无 echo 分」。** 点名过滤仍空真。
3. **r06 用 start≥ 盖住全题干。** generate 实现已闭；作者 CLI 测试未升级。
4. **intervene 70/>96 用 helper 测试盖住 CLI 路径。** 实现已走 helper 且无切片；套件不能单独证明这一点。
5. **calibrate 兄 `lab` 用 helper 测试盖住 `cmd_calibrate` 查找列表。** 实现列表已收紧；套件不能单独证明。
6. **r06 配对例用 `prep`/`col` 习惯名，靠 copy 绿，不攻击行走回归。**
7. **科学事件非空，来源仍是教员强制 `q=`。** echo CE 抽出 `\nq = 82`。**不**要求自然 CoT。
8. **A10-04 作者测试用同进程磁盘读盖住「新解释器」。**
9. **套件把 Plus 键写进仓库缓存且多数用例不 `clear`。**
10. **账本协议行仍 pytest。**

**仍无作者测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes` 恢复、`card`、`apply_model_template`。本通道对 `score_qa` / `assert_disjoint` 做了独立 CE，**不是**套件锁。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加生产测试。脚本：`_f_scratch/f19_ce.py`。

### CE-1 重叠 rename 必须同时替换（实现闭）

```text
apply_rename_edit({p1:p2, p2:p1}):
  question == "p2 = 4. p1 = 0. What is q = p2 * p1?"
  expression == "p2 * p1"
  parents == [p2, p1]
  values p2=4, p1=0
sequential str.replace would be:
  "p1 = 4. p1 = 0. What is q = p1 * p1?"   # r18 红

three-cycle {p1:p2,p2:p3,p3:p1}:
  "p2 = 4. p3 = 0. p1 = 1. What is q = p2 * p3?"
_rewrite_ids("p1 and p11 stay", {p1:aa, p11:bb}) == "aa and bb stay"
```

### CE-2 intervene 前缀：70 完整，>96 拒（实现闭；作者只锁 helper）

```text
_tiny_prefix_ids("x"*70) len==70
_tiny_prefix_ids("x"*97) raises "refuse truncated prefixes"
cli.cmd_intervene source has no ids[:64]

scientific intervene on 70-char question:
  spy intervene_hidden_decode prompt_ids lens == [79,79,79,79,79]
  prefix_truncated is not True

traces padded to 100-char prefix:
  ValueError tiny intervene prefix exceeds context
```

### CE-3 calibrate 不绑兄 `lab`（实现闭；作者只锁 helper）

```text
_find_labels_jsonl(feat) is None
  even if sibling in {lab, label, labels} has labels.jsonl

cmd_calibrate(--in-dir fit, --features-dir feat):
  _find_labels_jsonl dirs == [None, fit, feat]
  found is None
  scores == scores without sibling lab/
```

### CE-4 配对不靠 `prep` 名（实现闭）

```text
_load_source_value_pair(features_only) is None
  even if sibling in {prep, prepare, s-prep} has edits.jsonl
  even if parent/edits.jsonl exists

stage_a / stage_b (copy):
  donor_kind == same_value_diff_source
  unit pair (0, 3, same_value_diff_source)

alpha / omega: same_value_diff_source

unlink(stage_b/edits.jsonl); sibling stage_a still has edits:
  donor_kind == same_identity_fallback
```

### CE-5 scientific fit：行必须存在；作者过滤可空真（实现闭；过滤红）

```text
scientific probes:
  exactly {verbalizer, attention_mean, attention_rollout, attention_threshold}
  status == refused_not_section8
  score is None

author filter all(status==refused for row if baseline in S):
  []                          → True   # FAIL hunt
  {verbalizer, refused, score=1.0} → True

echo generate_fn(prefix) on same scientific prefix:
  status=generated, score=1.0, extracted=82
```

### CE-6 反向：CLI / 数学 — 独立 CE vs 烟测

| 分支 / 函数 | 本通道 | 作者套件 |
|---|---|---|
| prepare fixture | 烟测（作者） | 烟测 |
| prepare scientific | 独立：7×`constrained_target`（诚实） | 多例，事件可被强制 `q=` 满足 |
| collect scientific tiny / 拒 offline | 独立 | 锁 |
| collect offline e2e | 作者烟测当成功 | 烟测（诚实 offline H） |
| fit scientific §8 拒绝 | 独立（要求行存在且无 score） | 过滤可空真 |
| fit 孤立无 tasks | 独立 | 锁 |
| calibrate scientific | 独立：有限玩具 \(q\)；兄 `lab` 不绑 | helper only |
| intervene tiny + 删 edits | 独立 fallback | 不删 |
| intervene 70 / >96 | **CLI spy 闭** | helper only |
| `apply_rename_edit` 重叠 | **同时替换闭** | 作者有同字符串例（不当 oracle） |
| `score_qa` / `assert_disjoint` | 独立补 | 作者无 |
| Plus persist 新进程 | 未 spawn | 未 spawn |

## 9. 发现

### F19-00 开审与交卷哈希可复算且一致

- **严重度：** —
- **状态：** HASH_MATCH（过程通过）
- **文件：** `.planning/audits/round-19/VERSION.md` L5–23；61 = `b6db632f…96569eeb`；0 CRLF
- **复现：** 脚本原文开审与交卷同一摘要。

### F19-01 绿 165 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** `165 passed / 0 / 23.91s`，165 collected。作者主张与命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 仍是 offline 烟测。

### F19-02 F18-03：重叠 rename 同时替换（点名实现闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE，含三元循环与 `p1`/`p11`）
- **作者主张 F18-03：** **实现同意。** 顺序改写对照仍是 `p1 * p1`。
- **作者新例 `test_rename_swap_is_simultaneous`：** 锁对合同。本通道不把它当证明。

### F19-03 F18-08：intervene 不再静默 cap=64；70 ok；>96 raise（点名实现闭）

- **严重度：** —
- **状态：** 实现闭合（helper + CLI spy + 垫长 traces）
- **文件：** `cli.py` `_tiny_prefix_ids` / `cmd_intervene`；`models/generate.py` `>96`
- **复现：** spy ids 全是 79；100 字前缀 raise `refuse truncated prefixes`。无 `ids[:64]`。
- **作者主张 F18-08：** **实现同意。** 作者测试只覆盖 helper。套件缺口见 F19-07。

### F19-04 F18-12：calibrate 不绑兄 `lab`（点名实现闭）

- **严重度：** —
- **状态：** 实现闭合（helper + `cmd_calibrate` spy；有/无兄目录分数相同）
- **作者主张 F18-12：** **实现同意。** 作者测试只覆盖 helper。套件缺口见 F19-07。

### F19-05 F15-01：`stage_a`/`stage_b` 配对仍工作（点名闭）

- **严重度：** —
- **状态：** 实现闭合（含 `alpha`/`omega`、兄名 `prep`/`prepare`/`s-prep`、父目录、删 copy）
- **作者主张 F15-01：** **实现同意。** 作者不删 copy。

### F19-06 A14-03 / 点名：scientific fit 过滤仍可空真

- **严重度：** High（验证）
- **状态：** confirmed defect（测试设计）。实现写出四条 refused 且无 score。
- **文件：** `tests/test_round06_regressions.py` L60；`cli.py` `cmd_fit` L660–664
- **复现：** `author_fit_filter([]) is True`；`author_fit_filter([{baseline:verbalizer,status:refused_not_section8,score:1.0}]) is True`。省略这些行或改键名，作者例仍绿。
- **作者主张 A14-03：** 实现半句 **同意**。「过滤已锁 §8 对照」**超售。** 关闭此条需要改测试（存在性 + 无 score），会重置连续通过计数。

### F19-07 作者新例只锁 helper，不锁 CLI 合同

- **严重度：** Medium（验证残留）
- **状态：** confirmed defect（测试设计）。实现已由独立 CLI CE 闭合。
- **文件：** `test_tiny_prefix_ids_refuse_silent_truncate`；`test_calibrate_does_not_bind_sibling_lab_labels`
- **复现：** 若 `cmd_intervene` 仍 `ids[:64]` 但保留 helper，或 `cmd_calibrate` 仍 `extend(parent/lab)`，这两例仍绿。

### F19-08 科学 sham / 噪声弱析取仍绿

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）
- **文件：** `test_scientific_sham_*`；`test_sham_hits_do_not_book_evaluated_zero_noise`；`test_sham_hits_do_not_broadcast_*`

### F19-09 Fixture e2e 仍 offline；scientific tiny 仍 `constrained_target` — 诚实项，不开缺陷

- **严重度：** —
- **状态：** non-defect（验证口径）
- **注：** 任务与 ISSUES：八段是 offline 前缀 H；约束 `\nq=` 不是 §4.1；tiny 不是 MODEL-01。本通道 **不** 把它们写成已确认遗留缺陷，也 **不** 把 smoke 写成科学 e2e。echo 对照 `score=1.0`/`extracted=82` 只用来说明过滤若空真会漏掉什么。

### F19-10 Plus persist：作者缺 subprocess；套件泄漏缓存

- **严重度：** Medium（验证卫生）
- **状态：** 机制前轮已见；165 passed 后磁盘仍有 Plus 键。不在 61 摘要内。
- **作者主张 A10-04：** **机制同意。** 测试不覆盖新进程。

### F19-11 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：页眉写 pytest 不得关可执行行；行内仍 `python -m pytest -q` + `passed_local_tests`。`executable_function` 计数 **159**（本冻结作者称 165）。

### F19-12 夹具排除在冻结外；仍有大块零测试符号

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议 / 覆盖）
- **文件：** `tests/fixtures/*.json`（10 个）
- **符号：** `card`、`apply_model_template`、`forbid_host_exec`、`procrustes` 数值恢复、非空 `attention_mean`

### F19-13 ISSUES 点名关闭：F18-03/08/12 与 F15-01 实现 CE 对齐；A14-03 过滤超售

- **严重度：** Medium（过程）
- **状态：** 无「写已闭但点名实现 CE 仍红」。**有**「写过滤已锁但独立过滤 CE 仍红」：F19-06。
- **不要用本通道把 Goal/需求标 Complete。**

### F19-14 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq=` **不是** pending_server。vacuous `all` **不是** pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 协议行仍 `pytest -q`；可执行行仍 `passed_local_tests`（F19-11）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F19-06（过滤可空真）为已确认验证缺陷，关闭需改测试。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 165/0。e2e 是 offline 烟测。CLI 70/>96 与 calibrate 兄目录无作者测试。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** 账本可执行计数仍 159。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 哈希匹配（好）。本通道 **提交已确认验证缺陷**（F19-06 需改测试）。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：vacuous `all`、helper-only 新例、弱析取。offline H / `constrained_target` 按诚实项列出即可。 |
| 7 | 交付包 | **问题闭环未就绪到 Goal 句。** pytest 记录存在（165/0）。点名 CE 有独立记录。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行（诚实）。alt-source 图+generate 题干有测。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、alt-source 图有。重叠 rename **实现闭**；作者有 swap 例。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`（诚实）。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | `noise_ref=0` / 未知 \(M\) / sham missing 独立见。弱析取仍在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test、family persist 有。跨进程无测试。`assert_disjoint` 作者无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。intervene 长前缀 **实现拒截**；作者不锁 CLI。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。scientific 拒 §8 **实现有、作者过滤弱**。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。scientific calibrate 出玩具有限 \(q\)；兄 `lab` 实现不绑。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。配对不靠 `prep` 名。offline e2e 是 `unexpressible`。长前缀实现闭。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **165 passed，exit 0，23.91s，165 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH `b6db632f…96569eeb`（61，开审=交卷）。** |
| 独立性 | **独立闭：** 重叠 rename 同时替换；CLI intervene 79 ids / >96 raise；calibrate CLI 不绑兄 `lab`；`stage_a`/`stage_b` 与删 copy；scientific fit 四行 refused 无 score；`noise_ref=0`≠已评估空 \(N\)；generate 49/70/97；孤立 fit；scientific collect 拒 offline。**独立红：** 作者 scientific-fit 过滤可空真。**不独立 / 套件缺口：** helper-only 70/97 与 calibrate；r06 `start>=`；科学 sham 弱析取；同进程 persist。**诚实非缺陷：** offline 前缀 H、`constrained_target`、fixture echo verbalizer。 |
| Mock/stub | offline 前缀 H + 教员强制 `q=` + 可空真过滤 + `start>=` + helper 冒充 CLI + 弱析取 + 同进程 persist。 |
| 论文行为仍未证明 | 真 Prefill KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT（**未要求**） |
| 交付 vs 测试 | 「165 passed / 点名全闭 / e2e 已通」**超过** 冻结树测试力度。F18-03/08/12/F15-01 **实现**不能写成「作者过滤已锁 §8」或「CLI 70/>96 已有套件锁」。 |
| 已确认问题？ | **是。** High：F19-01、F19-06。Medium：F19-07、F19-08、F19-11、F19-12。点名 **实现** CE 未失败。点名 **过滤** CE 失败。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。scientific fit 作者过滤仍可空真（省略行仍绿）。作者 70/>96 与兄 `lab` 新例只锁 helper。弱析取仍绿。F18-03/08/12 实现闭合不是通道通过。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交需改 **测试** 的已确认缺陷（F19-06）。修复后须对 **新** hash 重开计数；只补本文件不改变被审摘要。 |

在用 CE 级测试锁住 **scientific fit 行必须存在且无 echo/zeros 分（禁止可空真 `all`）**、**`cmd_intervene` 70-token 前缀进入 hook 且 >96 拒（禁止只测 helper）**、以及 **`cmd_calibrate` 查找列表不含兄 `lab`（禁止只测 helper）** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。F18-03/08/12 与 F15-01 的实现闭合记在 F19-02…05，不是通道通过。offline 前缀 H 与 `constrained_target` 按诚实项保留，不在此要求 MODEL-01 或自然 CoT。
