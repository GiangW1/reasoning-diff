# F：验证质量与反向质疑（round-21）

独立审查通道 F。未改 `src/`、`tests/`、`pyproject.toml`。未读 round-21 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 写在 `.planning/audits/round-21/_f_scratch/`，不把 `tests/test_round06_regressions.py` / `tests/test_round07_regressions.py` 当证明。

**先行结论：** 按 `VERSION.md` 原文复算，开审与交卷冻结哈希 **一致（HASH_MATCH）** `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb`（61 文件，0 CRLF）。本机 `python -m pytest -q --tb=line` 为 **167 passed / exit 0 / 24.27s**，与作者 `pytest_author_claim: 167` 一致。这不是 Goal 通过。相对 r20，变的是 `cli.py`（1268 / `cc5eae53…`，写入 `prefix_n`）与 `test_round07`（444 / `fa9ac104…`）。`test_round06` 仍是 150 / `0c775fc2…`。

独立 CE（35 条，不 import r06/r07 测试模块）：**F20 点名重攻已闭，且不以 `prefix_truncated is not True` / `inspect.getsource` 为充分。** 70 字 CLI intervene 独立间谍 `intervene_hidden_decode`：五次 `prompt_ids` 长度皆 **79**，**无一 ≤64**。`cmd_calibrate` 有兄 `lab/WRONG` 与无兄目录：finder 实参只有 `(None, fit, feat)`，**未传入兄路径**，写出的 `calibration.jsonl` **相同**。F19-06：从作者源码抄出的 §8 断言在省略四行或 `refused+score=1.0` 时失败。旧 `all(... if baseline in S)` 对这两种输入仍恒真，**不当作充分**。作者新例 `test_intervene_cli_hook_ids_exceed_64` 间谍 hook 并锁 `all(n > 64)`；`test_calibrate_cli_ignores_sibling_lab` 实跑 CLI、查 finder 实参、比输出。helper 70/97 与 `_find_labels_jsonl` 仍在，只作附加。Fixture 八段仍 offline 前缀 H；scientific tiny 仍 `constrained_target`——按任务口径这是诚实项，**不**开成缺陷，也 **不** 当 MODEL-01 / 自然 CoT。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21 03:27–04:20（Asia/Shanghai） |
| 声明冻结 | `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb` |
| 开审复算 | `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb` |
| 交卷裁决 | **HASH_MATCH**（与声明同一摘要） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明 / 开审 / 交卷都是 **61**。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| pytest | **167 passed in 24.27s，exit 0。** Collect：**167 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 167 passed`。命令结果独立确认。当作 Goal / 阶段验收：**否。** |
| 范围 | 61 冻结文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。 |
| 明确未读 | `.planning/audits/round-21/{A,B,C,D,E}-*.md` |
| 独立 CE | `.planning/audits/round-21/_f_scratch/f21_ce.py` → `f21_ce_results.json`（35 条：35 闭 / 0 红）。未 import r06/r07 测试模块。 |

审查对象是**声明冻结字节**。pytest 与点名 CE 均在 HASH_MATCH 盘上执行。交卷哈希未漂。相对 r20 冻结 `dc36f217…`，本树变了 `src/reasoning_diff/cli.py`（1268 / `cc5eae53…`）与 `tests/test_round07_regressions.py`（444 / `fa9ac104…`）。`tests/test_round06_regressions.py` 未变（150 / `0c775fc2…`）。

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
| `tests/test_round06_regressions.py` | 150 | `0c775fc26b26aba8…` | `start>=len(prompt)`；`prep`/`col` 上 `donor_kind`；scientific fit **集合相等四条 §8 + refused + `score is None`**（F19-06 仍锁）；sham 析取 |
| `tests/test_round07_regressions.py` | 444 | `fa9ac104c8ba87e1…` | r07 节点 + swap 题干；`_tiny_prefix_ids` helper 70/97；**CLI intervene 间谍 `intervene_hidden_decode` 并锁 `all(n > 64)` + `prefix_n`**；**`cmd_calibrate` 实跑：finder 不含兄 `lab`，有/无兄输出相等**；helper `_find_labels_jsonl` 仍在；`stage_a`/`stage_b` 配对不删 copy |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer 形状、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only：**167 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。相对 r20：本冻结 `test_round07` 为 **23** 例；`test_intervene_cli_keeps_70_char_prefix` / `test_calibrate_cli_does_not_walk_sibling_lab` **已不在**；换成 `test_intervene_cli_hook_ids_exceed_64`、`test_calibrate_cli_ignores_sibling_lab`。这两例 **不是** 本通道证明；独立 CE 另跑。旧 `prefix_truncated is not True` 对 `{False, n_ids:64}` 仍绿——**本通道不接受它为充分**。旧 `inspect.getsource(cmd_calibrate)` **已不在**作者套件。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | `ρ=y` 泄漏仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed；无 generate 不可用 | fixture CLI **echo 前缀**无测试红（诚实项）；`attention_mean`/`rollout` 作者无数值 oracle（本通道独立补了 disjoint/score_qa） |
| `cli.py` | 1268 | `cc5eae53d7be27eb…` | smoke offline；scientific prepare/collect/fit/intervene；孤立 fit 拒；collect 复制 edits；`_tiny_prefix_ids` helper；`_find_labels_jsonl` helper；**CLI 70 间谍 hook ids**；**calibrate 实跑 finder 列表** | `cmd_intervene` 仍硬编码 `prefix_truncated=False`（L959），另写 `prefix_n`（L960）；scientific fit 四条 refused 无分 |
| `edits.py` | 367 | `cc8e2d23592a3ab8…` | value/alt-source 图；rename `{p1:alpha}`；swap 例 | 三前提集合碰撞仍非作者指纹 |
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
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `5097c831…a6f7aceb`（61，0 CRLF） |
| 交卷再算 | 同脚本 | **HASH_MATCH** 同一摘要 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **167 passed in 24.27s，exit 0**。无 skip/xfail/deselected |
| Collect | `python -m pytest tests --collect-only -q` | 167 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对冻结 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；顺序 swap 应变 `p2 * p1`；70/97 token | **存在的单元断言**与独立算术一致；swap/70/97 另由独立 CE 核 |
| **独立 CE** | `_f_scratch/f21_ce.py`（`PYTHONPATH=src`） | 35 条：35 闭 / 0 红。见 §3.1。 |

### 3.1 点名独立 CE（不信测试文件）

| CE | 独立结果（本冻结） | 作者测试是否锁住 |
|---|---|---|
| **F19-06：省略四条 §8 或 `refused+score=1.0` 必须让作者断言红** | **断言闭。** 从 `test_round06` L60–64 **抄出**（不 import 模块）：`needed` 四元集合、`section8` 过滤、`{baseline}==needed`、`status==refused_not_section8`、`score is None`。对 `[]` → False；省略 `verbalizer` → False；四行皆 `score=1.0` → False；四行中一行 `score=1.0` → False。对真实 scientific `probes.jsonl` 同样：删掉四行或把 score 改成 1.0 → 作者断言失败。旧过滤 `all(... if baseline in S)`：`[]` → True，`{verbalizer,refused,score=1.0}` → True。**不当作充分。** | 作者断言锁存在性 + 无 score。独立同意。残留：单独 `all(status)` 对空 `section8` 仍真——靠上一行集合相等救命。不锁 `extracted`。 |
| **scientific fit 必须写出四行 refused 且无分** | **实现闭。** 四条 `baseline∈{verbalizer,attention_mean,attention_rollout,attention_threshold}`，皆 `refused_not_section8`，`score is None`。echo `generate_fn=λp.prefix` 在同一科学前缀上 `status=generated`，`score=1.0`，抽出 `82`。 | 作者读 `probes.jsonl` 并锁集合/status/score。本通道不靠该例当 oracle。 |
| **intervene 不得静默 cap=64；70 ok；>96 raise。不以 `prefix_truncated is not True` 为充分** | **实现闭 + 作者 CLI 锁闭。** helper：`len(_tiny_prefix_ids("x"*70))==70`；`"x"*97` raise。源码无 `ids[:64]`。CLI 70 字 scientific 题干：独立间谍 `intervene_hidden_decode` 五次皆 **79 ids**，`any(n<=64)=False`，`prefix_n=79`。抄出的作者断言对 `seen=[64]` / `[79,64]` / `[]` / 缺 `prefix_truncated` → False；对真实 `[79×5]` → True。旧替身 `prefix_truncated is not True` 对 `{False, n_ids:64}` 与 `{}` **仍绿**——**不接受为充分**。traces 前缀垫到 100 字后 CLI **raise** `refuse truncated prefixes`。实现 L959 仍写死 `prefix_truncated=False`。 | 作者 `test_intervene_cli_hook_ids_exceed_64` 间谍 hook 并锁 `all(n > 64)` 与 `prefix_n`。helper 70/97 **仍在**（附加，不是唯一锁）。作者不锁 `>96` CLI；独立补了。 |
| **calibrate / `_find_labels_jsonl` 不得绑兄 `lab`。不以 `inspect.getsource` 为充分** | **实现闭 + 作者 CLI 锁闭。** `_find_labels_jsonl(feat)` 在兄 `lab`/`label`/`labels` 都有 `labels.jsonl` 时仍 `None`。独立 `cmd_calibrate`：有兄 `lab/WRONG` 时 finder 实参 `(None, fit, feat)`，**未传入兄路径**，`found is None`。有/无兄目录写出 **同一** toy `scores`（约 `0.0050235`）。`label_dirs.extend` / `parent / "lab"` / `joinpath("lab")` 不在 `cmd_calibrate` 源码。作者套件 **无** `inspect.getsource(cmd_calibrate)`。 | 作者 `test_calibrate_cli_ignores_sibling_lab` 实跑 CLI、wrap finder、断言兄路径不在实参、比 `calibration.jsonl`。helper `_find_labels_jsonl` 仍在（附加）。 |
| **`stage_a` / `stage_b` 配对仍工作** | **闭。** collect 复制 edits。`donor_kind=same_value_diff_source`，unit pair `(0,3,same_value_diff_source)`。兄 `prep`/`prepare`/`s-prep` 与父目录 edits **不**救命。删 `stage_b/edits.jsonl` → `same_identity_fallback`。 | 作者 `stage_a`/`stage_b` 不删 copy。loader 例只点名 `prep`。 |
| **`apply_rename_edit({p1:p2,p2:p1})` 不得变 `p1 * p1`** | **实现闭。** 题干 `p2 = 4. p1 = 0. What is q = p2 * p1?`。顺序 `str.replace` 对照是 `p1 = 4. p1 = 0. What is q = p1 * p1?`。三元循环同时成立；`p1`/`p11` 不互吃。 | 作者 swap 例锁同一题干。**不当 oracle。** |
| **自然 CoT / MODEL-01 / offline H / `constrained_target`** | **不要求，不开缺陷。** fixture collect `H.shape==(1,8)`。scientific prepare 7 条轨迹皆 `parse_status=constrained_target`。 | 测试不要求 §4.1 或 MODEL-01。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **`all(status==refused_not_section8 for row if baseline in S)`** | 仍对 `[]` 与 `refused+score=1.0` 恒真。作者 **不再** 只用它。新断言有 `{baseline}==needed` 与 `score is None`。独立突变确认省略行 / 骑 score 会红。 |
| **`prefix_truncated is not True`** | 缺字段、硬编码 `False`、静默 `ids[:64]` 都绿。实现 L959 写死 False。**本通道不接受为充分。** 作者现另锁 hook `n>64` 与 `prefix_n`。独立间谍确认 79。 |
| **`inspect.getsource(cmd_calibrate)`** | **本冻结作者已不用。** 若只查 `parent / "lab"` 字符串，仍会漏 `joinpath("lab")`。作者现跑 CLI 并查 finder 实参。 |
| **`_tiny_prefix_ids` / `_find_labels_jsonl` helper** | helper 绿不能单独证明 CLI。本冻结另有 CLI 例。helper 仍在，只作附加。 |
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
| pytest / CE 后 persist 泄漏 | 167 passed 与独立 CE 之后磁盘为 `["gsm8k-12", "q:ada has 4 apples…"]`。该文件不在 61 摘要内。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：页眉写 r21 须在 `5097c831…` 上独立复核且 pytest 不得关可执行行；协议行仍用 `python -m pytest -q`（70 处）+ `passed_local_tests`（320 处）；`executable_function` 计数仍写 **159**。 |
| scientific calibrate | 对 tiny 探针写出有限非conformity 分数（约 `0.0050235`）。不是论文校准。有/无兄 `lab` 分数相同。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-21 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 `_f_scratch` 与 §8 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| Plus persist 新解释器 | 本通道只确认套件后磁盘仍有 Plus 键；作者也不 spawn |
| 把 Goal 标 Complete | 本通道只评验证质量 |
| 把 offline H / `constrained_target` / fixture echo 开成缺陷 | 任务明确：除非作者把它们写成科学结果。不要求自然 CoT 或 MODEL-01。 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 167 passed | `VERSION.md` | **命令是。** 当作 Goal：**否。** |
| F20-01 intervene CLI 间谍：70 字题干 hook `prompt_ids` 长度 >64，并写 `prefix_n` | ISSUES | **独立同意。** 独立间谍五次皆 79。作者例锁 `all(n > 64)` + `prefix_n`。不以 `prefix_truncated is not True` 为充分。 |
| F20-02 `cmd_calibrate` 实跑：兄 `lab` 不在 finder 参数里；有/无兄输出相同 | ISSUES | **独立同意。** 独立 spy 实参 `(None, fit, feat)`；输出相同。作者例实跑 CLI。不以 `inspect.getsource` 为充分。 |
| F19-06 scientific fit 断言要求四条 §8 存在、`refused_not_section8`、无 `score` | ISSUES | **独立同意。** 省略行与 `score=1.0` 会红。旧 `all(... if baseline in S)` **不是**充分条件。 |
| F18-03 `_rewrite_ids` 同时替换；`{p1:p2,p2:p1}` → `p2 * p1` | ISSUES | **独立同意。** 作者 swap 例锁同一字符串；本通道不靠它。 |
| F18-08 intervene 不再 `ids[:64]`；超 96 拒绝 | ISSUES | **实现独立同意。** 作者 CLI 70 现锁 hook ids；`>96` CLI 仍只 helper，独立补了 raise。 |
| F18-12 `_find_labels_jsonl` 只读给定目录，不走兄 `lab` | ISSUES | **实现 + 作者 CLI 独立同意。** |
| F15-01 collect 复制 edits；配对只读 `in-dir` | ISSUES | **独立同意（含删 copy）。** |
| A14-03 scientific fit 拒写假 §8 行 | ISSUES | **实现同意。过滤猎项仍闭。** |
| A14-02 / A14-04 / D14-05 generate | ISSUES | 图 / `noise_ref=0` / generate 全题干：**实现同意。** |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` | **本套件不能作证。** 本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`（scientific+tiny）；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击：**

- **scientific fit 断言必须因省略四行或 `score=1.0` 而红。** 抄出的作者断言对这两种突变失败。旧 `all(... if baseline in S)` 仍空真——**不**当作关闭条件。**过滤猎项闭。**
- **重叠 rename 必须同时替换。** 回到顺序 `replace` 会让独立 CE 红（`p1 * p1`）。**实现闭。**
- **intervene 前缀必须完整或显式拒。不以 `prefix_truncated is not True` 为充分。** 回到 `ids[:64]`：独立间谍会看到 ≤64，抄出的作者断言也会红。100 字前缀必须 raise。**实现闭。作者 CLI 现锁 hook `n>64`。**
- **calibrate 不得读兄 `lab`/`label`/`labels`。不以 `inspect.getsource` 为充分。** 回到 `feat_dir.parent/"lab"` 会让独立 CLI spy 绑到 `WRONG` 或分数漂移，作者例也会红。**实现闭。作者实跑 CLI。**
- **配对不得靠兄目录名 `prep`。** 回到兄弟行走会让独立 loader CE 红。**实现闭。**
- **真实前提 `noise_ref=0` 不得当已评估空 \(N\)。** 独立仍闭。
- **generate 必须保留全题干，或拒截断。** 49/70/97 独立闭。
- **自然 CoT / MODEL-01。** 不要求。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_tiny_prefix_ids_refuse_silent_truncate` | 只调 helper。不经 `cmd_intervene`。本冻结另有 CLI 间谍例；本 helper **不是**关闭条件。 |
| `prefix_truncated is not True`（旧 r20 锁） | 对 `{False, n_ids:64}` 与缺字段为真。**本通道不接受。** 作者已不再只用它。 |
| `inspect.getsource(cmd_calibrate)`（旧 r20 锁） | **本冻结已不在。** |
| `test_calibrate_does_not_bind_sibling_lab_labels` | 只调 `_find_labels_jsonl`。本冻结另有 CLI 例；本 helper **不是**关闭条件。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 §8 断言 | **锁存在性+无 score。** 独立突变确认省略/`score=1.0` 会红。不锁 `extracted`；空 `all(status)` 仍靠集合行。本通道不把它当唯一证明。 |
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
2. **F19-06 已不再用空真 `all` 盖住「必须存在且无 echo 分」。** 集合相等与 `score is None` 仍在。独立突变确认。
3. **r06 用 start≥ 盖住全题干。** generate 实现已闭；作者 CLI 测试未升级。
4. **intervene 70：作者现间谍 hook ids，不再只用 `prefix_truncated is not True`。** helper 70/97 仍在，但是附加。`>96` CLI 作者仍不锁；独立 CE 锁了 raise。实现仍写死 `prefix_truncated=False`。
5. **calibrate 兄 `lab`：作者现跑 `cmd_calibrate` 并查 finder 实参，不再用 `getsource`。** helper 仍在，但是附加。
6. **r06 配对例用 `prep`/`col` 习惯名，靠 copy 绿，不攻击行走回归。**
7. **科学事件非空，来源仍是教员强制 `q=`。** echo CE 抽出 `\nq = 82`。**不**要求自然 CoT。
8. **A10-04 作者测试用同进程磁盘读盖住「新解释器」。**
9. **套件把 Plus 键写进仓库缓存且多数用例不 `clear`。**
10. **账本协议行仍 pytest。**

**仍无作者测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes` 恢复、`card`、`apply_model_template`。本通道对 `score_qa` / `assert_disjoint` 做了独立 CE，**不是**套件锁。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加生产测试。脚本：`_f_scratch/f21_ce.py`。

### CE-1 F19-06：作者断言必须因省略行或 `score=1.0` 而红（闭）

```text
author assertion (copied from test_round06 L60-64, not imported):
  needed = {verbalizer, attention_mean, attention_rollout, attention_threshold}
  section8 = [row for row in probes if baseline in needed]
  {baseline} == needed
  all(status == refused_not_section8)
  all(score is None)

[]                                          → False   # was vacuous True
omit verbalizer                             → False
four refused + score=1.0                    → False
four refused, one score=1.0                 → False
real scientific probes                      → True
same probes with §8 rows stripped           → False
same probes with score=1.0 written on §8    → False

vacuous all(... if baseline in S):
  []                          → True   # not sufficient
  {verbalizer, refused, 1.0}  → True
```

### CE-2 F20-01 intervene 前缀：独立间谍 hook ids；不以 flag 为充分（闭）

```text
_tiny_prefix_ids("x"*70) len==70
_tiny_prefix_ids("x"*97) raises "refuse truncated prefixes"
cli.cmd_intervene source has no ids[:64]
cli.cmd_intervene hardcodes prefix_truncated=False   # L959
cli.cmd_intervene writes prefix_n = len(ids)         # L960

scientific intervene on 70-char question:
  spy intervene_hidden_decode prompt_ids lens == [79,79,79,79,79]
  any(n<=64) == False
  prefix_n == 79

traces padded to 100-char prefix:
  ValueError tiny intervene prefix exceeds context

old surrogate prefix_truncated is not True:
  {relative:{prefix_truncated:False, n_ids:64}} → True   # NOT accepted
  {relative:{}}                                 → True   # NOT accepted

copied author test_intervene_cli_hook_ids_exceed_64:
  seen=[64]                         → False
  seen=[79,64]                      → False
  seen=[]                           → False
  seen=[79,79], prefix_n=79, False  → True
  helper test_tiny_prefix_ids_* still present (extra)
```

### CE-3 F20-02 calibrate 不绑兄 `lab`：实跑 CLI；不以 getsource 为充分（闭）

```text
_find_labels_jsonl(feat) is None
  even if sibling in {lab, label, labels} has labels.jsonl

cmd_calibrate(--in-dir fit, --features-dir feat) with sibling lab/WRONG:
  _find_labels_jsonl dirs == [None, fit, feat]
  finder_passed_sibling == False
  found is None
  calibration.jsonl == same run without sibling lab/
  scores ≈ [0.0050236, 0.0050236, 0.0050236, 0.0050235]

author test_calibrate_cli_ignores_sibling_lab:
  runs main(["calibrate", ...]) twice
  wrap _find_labels_jsonl; sibling path not in args
  compares calibration.jsonl
  inspect.getsource ABSENT
  helper _find_labels_jsonl test still present (extra)
```

### CE-4 配对不靠 `prep` 名（闭）

```text
_load_source_value_pair(features_only) is None
  even if sibling in {prep, prepare, s-prep} has edits.jsonl
  even if parent/edits.jsonl exists

stage_a / stage_b (copy):
  donor_kind == same_value_diff_source
  unit pair (0, 3, same_value_diff_source)

unlink(stage_b/edits.jsonl); sibling stage_a still has edits:
  donor_kind == same_identity_fallback
```

### CE-5 重叠 rename 必须同时替换（闭）

```text
apply_rename_edit({p1:p2, p2:p1}):
  question == "p2 = 4. p1 = 0. What is q = p2 * p1?"
sequential str.replace would be:
  "p1 = 4. p1 = 0. What is q = p1 * p1?"
```

### CE-6 反向：CLI / 数学 — 独立 CE vs 烟测

| 分支 / 函数 | 本通道 | 作者套件 |
|---|---|---|
| prepare fixture | 烟测（作者） | 烟测 |
| prepare scientific | 独立：7×`constrained_target`（诚实） | 多例，事件可被强制 `q=` 满足 |
| collect scientific tiny / 拒 offline | 独立 | 锁 |
| collect offline e2e | 作者烟测当成功 | 烟测（诚实 offline H） |
| fit scientific §8 拒绝 | 独立（行存在且无 score） | 存在性 + 无 score |
| fit 孤立无 tasks | 独立 | 锁 |
| calibrate scientific | 独立：有限玩具 \(q\)；兄 `lab` 不绑 | **CLI 实跑 + finder 实参 + 输出相等** |
| intervene tiny + 删 edits | 独立 fallback | 不删 |
| intervene 70 / >96 | **CLI 间谍 79 ids；>96 raise** | **CLI 间谍 n>64**；>96 仍 helper |
| `apply_rename_edit` 重叠 | **同时替换闭** | 作者有同字符串例（不当 oracle） |
| `score_qa` / `assert_disjoint` | 独立补 | 作者无 |
| Plus persist 新进程 | 未 spawn | 未 spawn |

## 9. 发现

### F21-00 开审与交卷哈希可复算且一致

- **严重度：** —
- **状态：** HASH_MATCH（过程通过）
- **文件：** `.planning/audits/round-21/VERSION.md` L5–23；61 = `5097c831…a6f7aceb`；0 CRLF
- **复现：** 脚本原文开审与交卷同一摘要。

### F21-01 绿 167 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** `167 passed / 0 / 24.27s`，167 collected。作者主张与命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 仍是 offline 烟测。

### F21-02 F18-03：重叠 rename 同时替换（点名实现闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE，含三元循环与 `p1`/`p11`）
- **作者主张 F18-03：** **实现同意。** 顺序改写对照仍是 `p1 * p1`。

### F21-03 F20-01 / F18-08：70 字 CLI intervene hook ids >64（点名闭）

- **严重度：** —
- **状态：** 实现闭合 + 作者 CLI 测试闭合（独立间谍，不以 flag 为充分）
- **文件：** `cli.py` `_tiny_prefix_ids` / `cmd_intervene` L958–960；`tests/test_round07_regressions.py` `test_intervene_cli_hook_ids_exceed_64`
- **复现：** 独立间谍 ids 全是 79；`any(n<=64)=False`；`prefix_n=79`。100 字前缀 raise `refuse truncated prefixes`。无 `ids[:64]`。抄出的作者断言对 `seen=[64]` 失败。旧 `prefix_truncated is not True` 对静默 cap **仍绿**——记下但不当作关闭条件。
- **作者主张 F20-01 / F18-08：** **独立同意。** helper 70/97 仍在，只作附加。作者不锁 `>96` CLI。

### F21-04 F20-02 / F18-12：`cmd_calibrate` 不绑兄 `lab`（点名闭）

- **严重度：** —
- **状态：** 实现闭合 + 作者 CLI 测试闭合（实跑，不以 getsource 为充分）
- **文件：** `cli.py` `cmd_calibrate` L771–775；`tests/test_round07_regressions.py` `test_calibrate_cli_ignores_sibling_lab`
- **复现：** 独立 wrap：有兄 `lab/WRONG` 时 dirs=`[None, fit, feat]`，`finder_passed_sibling=False`，`found=None`。有/无兄 `calibration.jsonl` 全等，scores 约 `0.0050235`。作者套件无 `inspect.getsource(cmd_calibrate)`。
- **作者主张 F20-02 / F18-12：** **独立同意。** helper `_find_labels_jsonl` 仍在，只作附加。

### F21-05 F15-01：`stage_a`/`stage_b` 配对仍工作（点名闭）

- **严重度：** —
- **状态：** 实现闭合（含兄名 `prep`/`prepare`/`s-prep`、父目录、删 copy）
- **作者主张 F15-01：** **实现同意。** 作者不删 copy。

### F21-06 F19-06：scientific-fit 断言因省略行或 `score=1.0` 而红（点名闭）

- **严重度：** —
- **状态：** 测试设计闭合（独立突变）。实现仍写四条 refused 且无 score。
- **文件：** `tests/test_round06_regressions.py` L60–64；`cli.py` `cmd_fit` L660–664
- **复现：** 抄出的作者断言：`author_fit([]) is False`；省略一行 False；四行或一行 `score=1.0` False。真实 probes 上剥行或写分同样 False。旧 `all(... if baseline in S)` 对这两种输入仍 True——**不**当作充分。
- **作者主张 F19-06：** **独立同意。** 残留：`all(status)` 对空 `section8` 仍真，靠 `{baseline}==needed`；不锁 `extracted`。不够重开本条。

### F21-07 F20-01/02 点名 helper-vs-CLI 猎项：本冻结已闭

- **严重度：** —
- **状态：** 测试设计闭合（相对 r20 F20-07）。独立 CE 不靠 helper / `is not True` / `getsource`。
- **文件：** `test_intervene_cli_hook_ids_exceed_64` L352–381；`test_calibrate_cli_ignores_sibling_lab` L384–418
- **复现：** 作者 CLI 70 间谍 `collect.intervene_hidden_decode` 并 `assert all(n > 64)`。作者 calibrate 实跑两次、wrap finder、比 JSONL。旧两例名已不在。helper 两例仍在——**不是**关闭条件。
- **关闭此条不重置 hash**（本冻结已含该测试）。连续通过仍不能开始，因为验证层残留见 F21-08/11/12，且本通道不宣布 Goal。

### F21-08 科学 sham / 噪声弱析取仍绿

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）
- **文件：** `test_scientific_sham_*`；`test_sham_hits_do_not_book_evaluated_zero_noise`；`test_sham_hits_do_not_broadcast_*`

### F21-09 Fixture e2e 仍 offline；scientific tiny 仍 `constrained_target` — 诚实项，不开缺陷

- **严重度：** —
- **状态：** non-defect（验证口径）
- **注：** 任务与 ISSUES：八段是 offline 前缀 H；约束 `\nq=` 不是 §4.1；tiny 不是 MODEL-01。本通道 **不** 把它们写成已确认遗留缺陷，也 **不** 把 smoke 写成科学 e2e。echo 对照 `score=1.0`/`extracted=82` 只用来说明 §8 过滤若空真会漏掉什么。

### F21-10 Plus persist：作者缺 subprocess；套件泄漏缓存

- **严重度：** Medium（验证卫生）
- **状态：** 机制前轮已见；167 passed 与独立 CE 后磁盘仍有 Plus 键。不在 61 摘要内。
- **作者主张 A10-04：** **机制同意。** 测试不覆盖新进程。

### F21-11 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：页眉写 pytest 不得关可执行行；行内仍 `python -m pytest -q`（70 处）+ `passed_local_tests`（320 处）。`executable_function` 计数 **159**（本冻结作者称 167）。

### F21-12 夹具排除在冻结外；仍有大块零测试符号

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议 / 覆盖）
- **文件：** `tests/fixtures/*.json`（10 个）
- **符号：** `card`、`apply_model_template`、`forbid_host_exec`、`procrustes` 数值恢复、非空 `attention_mean`

### F21-13 ISSUES 点名关闭：F20-01/02 与 F19-06 独立同意

- **严重度：** —
- **状态：** 无「写已闭但点名 **实现或作者锁** CE 仍红」。F20-01/02 / F19-06 作者主张与独立突变/间谍一致。不以旧替身复开。
- **不要用本通道把 Goal/需求标 Complete。**

### F21-14 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq=` **不是** pending_server。已闭的 helper-only CLI 锁 **不是** pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 协议行仍 `pytest -q`；可执行行仍 `passed_local_tests`（F21-11）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F21-08（sham 弱析取）为已确认验证缺陷。点名 F20-01/02 / F19-06 **已闭**，不再阻断本条的点名项。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 167/0。e2e 是 offline 烟测。70 字 hook ids 与兄 `lab` **现有** CE 级作者锁 + 独立间谍。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** 账本可执行计数仍 159。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 哈希匹配（好）。F20-01/02 / F19-06 已闭。本通道仍确认验证层残留（F21-08/11/12）且不宣布 Goal。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：弱析取、账本。offline H / `constrained_target` 按诚实项列出即可。已闭的 hook/calibrate 锁 **不要** 再标 pending_server。 |
| 7 | 交付包 | **问题闭环未就绪到 Goal 句。** pytest 记录存在（167/0）。点名 CE 有独立记录。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行（诚实）。alt-source 图+generate 题干有测。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、alt-source 图有。重叠 rename **实现闭**；作者有 swap 例。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`（诚实）。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | `noise_ref=0` / 未知 \(M\) / sham missing 独立见。弱析取仍在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test、family persist 有。跨进程无测试。`assert_disjoint` 作者无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。intervene 长前缀 **实现拒截**；作者现锁 hook `n>64`。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。scientific 拒 §8 **实现有、作者存在性+无 score 仍闭**。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。scientific calibrate 出玩具有限 \(q\)；兄 `lab` 实现不绑；作者现跑 CLI。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。配对不靠 `prep` 名。offline e2e 是 `unexpressible`。长前缀实现闭；70 字 hook ids 作者+独立闭。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **167 passed，exit 0，24.27s，167 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH `5097c831…a6f7aceb`（61，开审=交卷）。** |
| 独立性 | **独立闭：** F19-06 作者断言对省略行与 `score=1.0` 失败；scientific fit 四行 refused 无 score；重叠 rename 同时替换；CLI intervene 79 ids / 无一 ≤64 / >96 raise；calibrate CLI 不绑兄 `lab`（finder 未收兄路径，输出相同）；`stage_a`/`stage_b` 与删 copy；`noise_ref=0`≠已评估空 \(N\)；generate 49/70/97；孤立 fit；scientific collect 拒 offline。**独立红：无。** **不独立 / 套件缺口：** r06 `start>=`；科学 sham 弱析取；同进程 persist；helper 仍在但是附加。**诚实非缺陷：** offline 前缀 H、`constrained_target`、fixture echo verbalizer。 |
| Mock/stub | offline 前缀 H + 教员强制 `q=` + `start>=` + 弱析取 + 同进程 persist。**不再**用 `prefix_truncated is not True` 或 `getsource` 冒充 CLI 合同。 |
| 论文行为仍未证明 | 真 Prefill KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT（**未要求**） |
| 交付 vs 测试 | 「167 passed / F20-01/02 已闭 / F19-06 已闭」在**点名合同**上与独立 CE 一致。F19-06 **断言**不能写成「旧 `all(if in S)` 已够」。F20-01/02 **不能**写成「只锁了 `prefix_truncated is not True` / `getsource`」——作者现锁 hook ids 与 calibrate 行为；独立间谍同意。绿 167 **仍超过** Goal 验收。 |
| 已确认问题？ | **是。** High：F21-01。Medium：F21-08、F21-11、F21-12。点名 **F20-01/02 / F19-06** CE **未失败**。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。点名 F20 helper-vs-CLI 与 F19-06 断言猎项已闭。弱析取仍绿。账本仍用 pytest 关协议行。F18-03/08/12 与 F20-01/02 实现/测试闭合不是通道通过。 |
| 停止条件第 5 条 | **不能开始连续通过。** 哈希匹配（好）。F20-01/02 / F19-06 已在本冻结闭，不再单独阻断。本通道仍确认需改测试/账本的残留缺陷（F21-08/11）。修复后须对 **新** hash 重开计数；只补本文件不改变被审摘要。 |

点名 F20 重攻按任务口径已闭：独立间谍 `intervene_hidden_decode` 的 `prompt_ids` 无一 `len<=64`；独立 `cmd_calibrate` 有/无兄 `lab/WRONG` 输出相同且 finder 未收兄路径；作者 §8 断言在省略四行或 `refused+score=1.0` 时失败。**不**接受 `prefix_truncated is not True` 或 `inspect.getsource` 作为充分条件。offline 前缀 H 与 `constrained_target` 按诚实项保留，不在此要求 MODEL-01 或自然 CoT。在 Goal e2e 仍是 offline 烟测、sham 弱析取仍绿、账本仍用 pytest 关闭协议行之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。
