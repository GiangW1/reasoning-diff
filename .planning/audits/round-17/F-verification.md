# F：验证质量与反向质疑（round-17）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-17 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 在 `.planning/audits/round-17/_f_scratch/` 独立复跑，不把 `tests/test_round07_regressions.py` 当证明。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（61 文件，0 CRLF）。交卷再算为 `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（仍 61 文件）→ **HASH_MISMATCH**。审查期间 `cli.py`（02:57:30）与 `tests/test_round07_regressions.py`（02:57:36）mtime 更新；后者从开审所见 **318 行 / 16 例** 变成 **342 行 / 18 例**（多 `test_load_source_value_pair_does_not_walk_sibling_prep`、`test_intervene_pairs_source_without_prep_sibling_name`）。本通道未改这两文件。本机 `python -m pytest -q --tb=line` 为 **162 passed / exit 0 / 35.30s**，发生在漂移之后，**不能**写成交卷盘上对声明冻结的 160。作者 `pytest_author_claim: 160` 与交卷 collect **162** 不一致。

点名猎项（实现 vs 测试，不信作者 CE 文件）：

- **A14-02：** 测试已不再要 `p2_src` / `(alt source)`。它们锁的是「留叶 *a* + 新 `src_b` + `p1 * src_b`」。独立 CE：必读父母 `{p1,src_b}` **等于** `rename(p2→src_b)`；必读值多重集仍是 `{4,0}`；残留 `p2` **不在** `ancestors(q)`，改残留 *a* 答案不变。作者所谓 XOR `{p1,p2,src_b}` 是前提 **并集**，不是必读源 XOR。这是把锁改写成仍错的实现。
- **A14-03：** `test_scientific_h_is_finite_and_pairs_donor` **确实读了** `probes.jsonl`。同键 echo / 零分且无 `refused_not_section8` 会红。`all(... if baseline in S)` 在 **零行** 时恒真；带 `score=1.0` 的 refused 行仍绿。夹具 fit 仍写 echo `score=1.0`。
- **A14-04：** 库路径 `noise_ref=0`、无 `sham:` → `null_reason=noise_set_missing`，不把空 \(N\) 当已评估。对照「已评估空 \(N\)」会得到 `rho_M_noise=1.0`。`test_evaluated_zero_hit_sham_*` 弱析取在两种实现下都绿。
- **D14-05：** r07 单元测 **整题** `question == prompt_text`，不是只比 `start>=prompt_len`。49 字来源题在旧 `cap=48` 会丢掉 `?`。科学 CLI 测试仍只锁 `start>=`。`>96` 拒截断已独立见到。
- **教员强制 / Gate / tiny / 孤立 Symbolic：** 测试不要求 §4.1 或 MODEL-01。孤立从未 Plus 的 Symbolic = `probe_train`（诚实，不是 A10-04）。
- **反向：** 大量 CLI 分支与数学函数仍是 happy-path / 形状烟测。

本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai；开审约 02:56，交卷在 CE 与 162 pytest 之后） |
| 声明冻结 | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` |
| 开审复算 | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明 / 开审 / 交卷都是 **61**。变的是字节，不是个数。 |
| 交卷漂移文件 | `tests/test_round07_regressions.py` 02:57:36（318→342 行，+2 例）。`src/reasoning_diff/cli.py` 02:57:30。本通道未改。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；漂移文件对 git 为 `??`；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, numpy 1.26.4；无下载 |
| pytest（交卷漂移树） | **162 passed in 35.30s，exit 0。** Collect：**162 nodes**。无 skip/xfail/deselected/`unittest.mock`。开审 MATCH 盘 **未**跑全量 pytest。 |
| 作者主张 | `pytest_author_claim: 160 passed`。与交卷 collect **162** 对不上。当作 Goal / 阶段验收：**否。** 不能回写为声明 hash 上的 160。 |
| 范围 | 开审 61 文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存不在冻结内。库 CE（edits/measure/generate）绑开审已存在的文件（mtime 早于 02:56）。CLI 管线 CE 跑在交卷树上。 |
| 明确未读 | `.planning/audits/round-17/{A,B,C,D,E}-*.md` |
| 独立 CE | `.planning/audits/round-17/_f_scratch/f17_ce.py`、`f17_ce2.py`、`results.json`、`results2.json`。未把 r07 测试当 oracle。 |

审查对象首先是**声明冻结字节**。交卷哈希已漂。点名库 CE 在 edits/measure/generate 上仍对得上开审树；donor 目录名独立性只在交卷树上见到。

## 2. 逐文件覆盖

行数 / SHA-256 前 16 是 **交卷** 61 文件（`3d0f1c10…`）。开审 MATCH 时 `test_round07` 为 318 行。

### 2.1 测试（全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect `--backend offline` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a3…` | r03 节点；P1 泄漏用例仍绿；`ie_z` 单元仍是隐均值 helper |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；`test_evaluated_zero_hit_sham_*` **弱析取**；`test_source_value_pair_has_both_conditions` 只查 metadata 旗标 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | 科学事件 `any(q)`；H 有限；verbalizer 17/70/boxed |
| `tests/test_round06_regressions.py` | 146 | `b555ed24000400e1…` | 科学 fit **读** `probes.jsonl` 的 `refused_not_section8`（过滤 `all()`）；`start>=len(prompt_text)`；donor_kind；弱析取 sham |
| `tests/test_round07_regressions.py` | **342（交卷）** / **318（开审）** | `8c23db4b637c8c70…`（交卷） | 开审 16 例：alt-source 留 *a*+`src_b`、整题 `prompt_text`、`noise_ref=0` 不评空 \(N\)、孤立 fit 拒。交卷 +2 例锁兄 `prep` 与非 `prep` 名 donor——**不是声明冻结证据**。 |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer 形状、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only（交卷盘）：**162 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。`tiny_hooks` 2 参数 + 其余函数 = 162。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。

开审 MATCH 树上 `test_round07` 为 16 例 → 与作者 160 对齐（162−2）。交卷 18 例 → 162。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | `ρ=y` 泄漏仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | 科学路径拒写；夹具 fit 仍 echo。`attention_*` 无数值 oracle |
| `cli.py` | 1260 | `9431b7768fda6a3c…` | smoke offline；scientific prepare/collect/fit/intervene；A14-03 过滤 `all()` | 交卷才锁兄目录；analyze 只认 `p1_table.jsonl`；intervene `cap=64` |
| `edits.py` | 365 | `1e5b97d63a62ab78…` | 留 *a* + `src_b` + 表达式 | **不**拒「必读源 = rename(base)」 |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review` | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；`ie_z` helper 仍是均值差 | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 405 | `985b9d9328e4111f…` | 未知 \(M\)；`noise_ref=0` 无 sham → null；C7 helper | r04 弱析取仍绿 |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；hook 名 | 测试不比 last-token |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 200 | `6e6040394ac641c7…` | 整题 `prompt_text`；`>96` 拒 | `prompt_len` 是 token 数，tiny 1:1 |
| `models/tiny.py` | 120 | `c75d0f5325766612…` | hook 清理 + logits 变 | 随机权重 ≠ MODEL-01 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | 一字一 token |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头形状 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | — |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | 标量/`[0]`/`[]` 拒 Prefill | — |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 184 | `40ab4021d4dccc6e…` | Plus→test；RAM∪磁盘 | `assert_disjoint` **零测试**；作者不 spawn |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | `card` 无 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f…` | family / `register_test_only_family` | `"reversing operation"` 仍非 T4 |
| `tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354…` | sidecar；孤立角色无测试 | — |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` 未断言 |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；口语 `needs_truth` | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584；`n<d` truncated | `apply_map` 数值恢复未锁 |

夹具 JSON **不在冻结内**。`models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 仅包说明。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `3d0a0764…fdfbc6`（61 文件，0 CRLF） |
| 交卷再算 | 同脚本 | **HASH_MISMATCH** `3d0f1c10…c0952f`。`cli.py` / `test_round07` mtime 02:57:30–36。本通道未改。 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **162 passed in 35.30s，exit 0**。无 skip/xfail。**交卷漂移盘。** |
| Collect | `python -m pytest tests --collect-only -q` | **162 nodes**，collect exit 0 |
| skip/xfail/`assert True` | 对冻结 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17 |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；σ(1)；`repairability=0.6`；`[0.7,0.4]` | **存在的单元断言**与独立算术一致 |
| **独立 CE** | `_f_scratch/f17_ce.py` + `f17_ce2.py` | 见下。不 import r07 测试模块。 |

### 3.1 作者点名 CE — 独立复跑（不信测试文件）

| CE | 独立结果 | 作者测试是否锁住 |
|---|---|---|
| **A14-02 图：留 *a*、加 `src_b`、父母改读 *b*** | **实现按作者合同闭，按论文 XOR / A14-02 原拒绝标准未闭。** 题干 `p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?`（49）。前提 `{p1,p2,src_b}`。父母 / `ancestors(q)` = `{p1,src_b}`。`p2` 不在祖先。改残留 *a* 答案仍 `0`；改 `src_b=9` 答案 `36`。`apply_rename_edit({p2:src_b})` 父母集相同。必读值多重集 `{0,4}` = base。无 `p2_src`、无 `(alt source)`。 | `test_source_value_pair_rewrites_graph_ids` 锁并集 + 表达式 + 整题。`test_source_value_pair_has_both_conditions` 只锁旗标。**锁的是 rename+残留 *a*，不是必读源 XOR。** |
| **A14-03 scientific fit 拒 §8 玩具** | **实现闭（交卷树跑通；`cmd_fit` 科学分支与 VERSION 声明一致）。** 7 行 probes：4 条 `baseline∈{verbalizer,attention_*}` 皆 `refused_not_section8`，无 `score`/`f1`。夹具 fit 仍 echo：zeroshot/fiveshot/reflection `score=1.0`，`generate_fn` 回显前缀。 | **读了 `probes.jsonl`。** `all(status==refused if baseline in S)`：零匹配行恒真；`score` 可骑在 refused 行上。不锁「必须存在 4 行」。不锁夹具 fit。 |
| **A14-04 `noise_ref=0` 无 sham 不得评空 \(N\)** | **库路径闭。** `Label(q,p1/p2, noise_ref=0)`、`sham_protocol` 有名无 `sham:` 行：`null_reason=noise_set_missing`，`rho_M_noise/excess=None`，`rho_M_raw=1.0`。对照 `noise_set=[]`+`noise_evaluated=True`：`rho_M_noise=1.0`，`excess=0.0`。 | 新例锁 excess/noise 为 None。**不断言 `null_reason`。** r04 `test_evaluated_zero_hit_sham_*` 弱析取在 null 与已评估空 \(N\) 下都绿。 |
| **D14-05 整题，不只 `start>=`** | **generate 闭。** `question == prompt_text`，`* src_b` 在题内，`prompt_len=49=n_ids`。`>96` → `tiny prompt exceeds context`。科学 prepare `trace-source` 整题相等。旧帽 48 会切掉最后 `?`。intervene `prefix_truncated=false`（另一条 `cap=64` 未触发）。 | r07 单元测 **整题**。科学 r05/r06 仍只 `start>=len(prompt_text)`。 |
| **A12-03 / 兄 edits** | **交卷树闭。** `_load_source_value_pair(features)` 在只有兄 `prep/edits.jsonl` 时为 None。collect 复制 edits。独立目录名 `s_prep`/`s_col` → `donor_kind=same_value_diff_source`，`donor_rows=[0,3]`。 | 开审测试 **无** 这两例。交卷 +2 例不能回写声明冻结。 |
| **教员强制 `q=`** | 7 条轨迹皆 `parse_status=constrained_target`，事件只有 `['q']`，赋值 `\nq = 82/53`。 | `any(q)` + `start>=` **被强制行单独满足**。测试 **不** 要求 §4.1 / MODEL-01。 |
| **孤立 Symbolic** | 从未 Plus、`gsm8k-never-f17` → `split=probe_train`。 | 无测试把这写成缺陷。与 ISSUES 诚实口径一致。 |
| **Gate / 空结论** | smoke / analyze 仍 `unregistered` / `scientific_conclusion is None`。 | 测试要求这些值。**不**要求 Gate 通过。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **A14-02「XOR `{p1,p2,src_b}`」** | 并集锁得住；必读源仍是 rename。残留 *a* DAG 惰性。题干同时出现 `p2 = 0` 与 `src_b = 0`。机械「rename + 回贴未用 *a*」会满足作者断言。 |
| **A14-03 `all(... if baseline in S)`** | 零 §8 行 → 恒真。`{"baseline":"verbalizer","status":"refused_not_section8","score":1.0}` 仍绿。`baseline="verbalizer_zeroshot"` 的 echo 漏过滤。 |
| **A14-04 r04 弱析取** | `null_reason != noise_set_empty or rho_S_excess is not None`：当前 `noise_set_missing` 单独过；旧已评估空 \(N\) 也会过。 |
| **`rho_M_excess != 1.0 or null_reason`** | 科学 sham 仍弱。`None != 1.0` 单独过。 |
| **`start>=prompt_len` 冒充整题** | 截断后的 `prompt_text` 仍满足。r07 单元测不是这条。 |
| **教员强制 `q=` 当科学事件** | `any(q)` 全部被 `\nq = <digit>` 单独满足。 |
| **offline H 当 e2e** | 八段 `H=[[1..8]]`；analyze 无 `p1_table`；smoke **要求**空结论。 |
| **`test_tiny_hooks` L17** | 任何带 `forward` 的类都真。 |
| **`test_c7_m01_*`** | 手填 `noise_set=["p3"]`，不经 labels。 |
| **`test_plus_locks_*`** | 同进程 RAM clear。**不**新进程。 |
| **交卷 +2 donor 例** | **不在声明冻结。** |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| 科学 prepare 事件 | 7 条轨迹事件全是强制 `q = 82` 或 `53`。`trace-source` 题干完整（49 字）。 |
| 夹具 fit §8 | zeroshot/fiveshot/reflection **echo `score=1.0`**。作者只关 scientific。 |
| pytest 后 persist | 套件仍可能把 Plus 家族键写入 `.planning/research/.cache/gsm_test_only_families.json`（不在 61 文件内）。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md` 协议行仍 `python -m pytest -q` / `passed_local_tests`。审查中账本已写 r17 `3d0a0764…`「作废」并指向 r18 `3d0f1c10…`——与本通道交卷哈希相同，**不能**把未冻结的 r18 写成 r17 已过。`executable_function` 计数仍 159。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-17 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 `_f_scratch/` 与 §8 |
| 在开审 MATCH 字节上重跑 160 pytest | 交卷已离开声明冻结；本通道不还原测试文件 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| 把 Goal 标 Complete | 本通道只评验证质量 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 160 passed | `VERSION.md` | **交卷命令是 162。** 开审 160 未在 MATCH 盘上复跑。当作 Goal / 交卷盘证据：**否。** |
| A14-02 留 *a*、加等值 `src_b`、父母改读 *b* | ISSUES | **合同句独立同意。** 「XOR `{p1,p2,src_b}`」**超售**：那是并集；必读源仍是 rename。 |
| A14-03 scientific fit 写 `refused_not_section8` | ISSUES | **实现同意。** 测试弱（vacuous `all`）。夹具 fit 仍玩具。 |
| A14-04 真实前提 `noise_ref=0` 且无 `sham:` → 不评空 \(N\) | ISSUES | **库实现同意。** r04 旧名测试仍允许已评估空 \(N\)。 |
| D14-05 tiny 不再 48 字截断 | ISSUES | **generate 独立同意（整题）。** 科学 CLI 测试只锁 `start>=`。 |
| A13-01 / A13-02 / A13-03 / A12-03 / A10-04 | ISSUES | 前轮点名实现多数仍在。A12-03 兄 edits 的测试是交卷补丁。 |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表 helper；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；`prefix_ids`/空 hidden 非 Prefill。

**本冻结点名攻击：**

- **alt-source 必须留 *a* 且表达式读 `src_b`。** 回到纯 `p2_src` rename（丢掉残留 *a*）会让现例红。**这锁住了新合同，也锁住了「仍是 rename 必读源」的错实现。**
- **scientific fit 在 `baseline∈{verbalizer,attention_*}` 上不得写非 refused。** 同键 echo/零分会红。省略这些行或改键名仍绿。
- **`noise_ref=0` 无 sham 不得写出 `rho_M_noise=1`。** 新例会红。r04 弱析取不会红。
- **来源题干必须完整进入 `prompt_text`。** 开审 r07 单元测会红（`cap=48` 切 `?`）。科学 CLI `start>=` 不会红。
- **`>96` 必须拒绝。** 独立见到。无作者测试专打这条。
- **教员强制 / Gate 未注册 / 孤立 Symbolic=`probe_train`。** 测试不把它们写成 §4.1 / MODEL-01 / A10-04——**不要当缺陷开。**

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_source_value_pair_rewrites_graph_ids` | 锁并集/表达式/整题。不拒必读源 rename 同构。不查 `ancestors`、不查改残留 *a*。 |
| `test_source_value_pair_has_both_conditions` | 只查 metadata 旗标。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 §8 断言 | 读了 probes，但是 vacuous `all`。 |
| `test_scientific_h_*` / r05 collect 的 `start>=` | 截断 `prompt_text` 仍绿。 |
| `test_evaluated_zero_hit_sham_is_zero_noise_not_null` | 无 `sham:` 行。弱析取。名字还要求「已评估 0 击」。 |
| `test_sham_no_change_does_not_book_empty_n` | 与 A13-02 覆盖不足重叠风险仍在。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `!= 1.0 or null_reason`。 |
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + probes 存在。 |
| `test_plus_locks_symbolic_family_to_test` | 不 spawn。 |
| `test_generated_events_*` / scientific `any(q)` | 教员强制 `\nq = 82` 单独满足。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 末 token 有限 H 也会绿。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_p1_held_out_logistic_detects_rho` | `ρ=y` 在全部行。 |
| `test_tiny_hooks` L17 | 恒真。 |
| 交卷 `test_load_source_value_pair_*` / `test_intervene_pairs_source_*` | **不在声明冻结。** |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]`；analyze 无 `p1_table`；smoke **要求**空结论。
2. **A14-02 用并集+表达式盖住必读源仍是 rename。** 用「不是 `p2_src`」盖住「已经是论文 XOR」。
3. **A14-03 用过滤 `all()` 盖住「可以不写 §8 行 / 分数骑在 refused 上」。** 夹具 fit 仍 echo。
4. **A14-04 用弱析取盖住 r04「已评估空 \(N\)」旧合同。**
5. **科学事件非空，来源是教员强制 `q=`。**
6. **`start>=prompt_len` 冒充未截断题干（科学 CLI）。**
7. **C7-M-01 用 helper 的 `noise_set=["p3"]` 盖住 labels 路径。**
8. **交卷 +2 例不能回写开审冻结的 donor 一般性。**
9. **账本协议行仍 pytest；审查中已改口到另一 hash。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

已在 `_f_scratch/` 执行。本通道未加测试。

### CE-1 A14-02 并集闭 / 必读源仍是 rename

```text
apply_alt_source_same_value(p2):
  question == 'p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?'
  premises == {p1, p2, src_b}          # 作者称为 XOR — 这是并集
  parents == ancestors(q) == {p1, src_b}
  leftover p2 not in ancestors
  rename(p2→src_b).parents == {p1, src_b}
  required value multiset == {0, 4} == base
  recompute(p2=9) answer == 0          # 残留 a 惰性
  recompute(src_b=9) answer == 36
  no 'p2_src', no '(alt source)'

应：拒「必读源集合 / 值多重集是 base 的 rename」；或两张图分别只读已存在的 a 或 b。
现测锁并集，绿了仍错的实现。
```

### CE-2 A14-03 probes.jsonl（实现拒写；测试弱）

```text
scientific fit probes:
  4 rows baseline in {verbalizer, attention_*}
  status == refused_not_section8, no score/f1

existing: all(status==refused for row if baseline in S)
  []                          → True   (vacuous)
  {verbalizer, score=1.0}     → False  (echo 会被现测抓住)
  {verbalizer, refused, score=1.0} → True

fixture fit: zeroshot/fiveshot/reflection score=1.0 (echo prefix)

应：断言恰好 4 条 refused 且无 score；禁止其它键写玩具分数。
```

### CE-3 A14-04 空 \(N\)（库闭；r04 弱）

```text
noise_ref=0 on p1/p2, no sham: row:
  null_reason=noise_set_missing
  rho_M_noise=None, rho_M_excess=None

booked-empty counterfactual:
  rho_M_noise=1.0, excess=0.0, null_reason=None

r04: null_reason != noise_set_empty or excess is not None  → 两种都绿
```

### CE-4 D14-05 整题 / >96

```text
source question len == 49
prompt_text == question, contains '* src_b'
prompt_len == 49 == n_ids
cap=48 would drop trailing '?'

encode('…'+80*'x'+…) n_ids==117
generate_task_trace → ValueError tiny prompt exceeds context

scientific CLI start>=prompt_len 在截断 prompt_text 上仍绿
```

### CE-5 教员强制 / 孤立 Symbolic / 兄 edits（交卷树）

```text
7 traces: events=['q'], constrained_target, assigned='\nq = 82|53'
isolated Symbolic never-Plus → probe_train
_load_source_value_pair(features) is None   # 兄 prep 有 edits
collect copies edits.jsonl
s_col (not named col) donor_kind == same_value_diff_source
```

## 9. 发现

### F17-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）
- **文件：** `.planning/audits/round-17/VERSION.md` L5–23；开审 61 = `3d0a0764…`；交卷 61 = `3d0f1c10…`
- **复现：** 开审脚本原文 MATCH。审查期间 `cli.py` 02:57:30、`test_round07_regressions.py` 02:57:36（+2 例）。本通道未改。事后补丁不能回写本冻结为已闭。
- **注：** 只要本通道提交已确认缺陷，连续通过计数不能开始。

### F17-01 绿 pytest 不是 Goal / QA 验收；160 与 162 对不上

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** 交卷 `162 passed / 0`。作者主张 160。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 是 offline 烟测。

### F17-02 A14-02：测试已离开 `p2_src`，但锁的是 rename+残留 *a*，不是必读源 XOR

- **严重度：** High（验证 / 锁错实现）
- **状态：** confirmed defect（验证）。作者合同「留 *a*、加 `src_b`、父母改读 *b*」实现同意；「XOR `{p1,p2,src_b}`」**超售**。
- **文件：** `edits.py` `apply_alt_source_same_value`；`tests/test_round07_regressions.py` `test_source_value_pair_rewrites_graph_ids`
- **复现：** §3 CE-1。必读父母 = `rename(p2→src_b)`。残留 `p2` 不在 `ancestors(q)`。题干同时含两个等值叶。A14-02 原文要求拒绝「必读源 / 值多重集是 base 的 rename」——现测要求这个构造。
- **作者主张 A14-02：** **半句同意，XOR 半句不同意。**

### F17-03 A14-03：测试读了 probes.jsonl；echo 同键会红；vacuous `all` 与夹具 echo 仍在

- **严重度：** Medium（验证残留）
- **状态：** 科学 CLI **实现闭合**（4 条 refused，无 score）。测试不能在「不写这些行」时失败。夹具 fit 仍 `score=1.0`。
- **文件：** `cli.py` `cmd_fit`；`tests/test_round06_regressions.py` L57–60
- **作者主张 A14-03：** **科学实现同意。** 不得写成「§8 对照已锁」或「所有 fit 都拒玩具」。

### F17-04 A14-04：库路径不再把 `noise_ref=0` 当已评估空 \(N\)；r04 旧测试仍允许

- **严重度：** Medium（验证残留）
- **状态：** 库实现闭合。`test_observed_real_noise_ref_without_sham_does_not_book_empty_n` 会抓 booked-empty。`test_evaluated_zero_hit_sham_is_zero_noise_not_null` **仍绿两种实现**。
- **作者主张 A14-04：** **实现同意。** 不得用 r04 旧名写成「已评估 0 击」仍是合同。

### F17-05 D14-05：generate 整题闭；科学 CLI 测试仍只 `start>=`

- **严重度：** Medium（验证残留；生成实现闭）
- **状态：** `generate_task_trace` / 科学 `trace-source` 整题相等。r07 单元测锁整题。r05/r06 科学测试不锁整题。`>96` 拒截断独立见到。intervene 另有 `cap=64` 静默切前缀（本 fixture 未触发）。
- **作者主张 D14-05：** **generate 同意。** 不得把 `start>=` 写成整题已锁。

### F17-06 教员强制 / Gate / tiny / 孤立 Symbolic — 测试未越权

- **严重度：** —
- **状态：** non-defect（验证口径）
- **注：** 7 条轨迹皆 `constrained_target`。测试不要求自然 CoT / MODEL-01 / Gate 通过。孤立 Symbolic = `probe_train` 诚实。**不要**把这些开成缺陷。

### F17-07 Fixture e2e 仍 offline；analyze 常无 `p1_table`

- **严重度：** Critical（验证）
- **状态：** confirmed defect（验证）。作者 ISSUES 已承认八段是 offline 前缀 H — **不要超售成科学 e2e**。

### F17-08 弱析取 / helper / 同进程 persist 仍绿

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）
- **文件：** `test_scientific_sham_*`；`test_evaluated_zero_hit_sham_*`；`test_c7_m01_*`；`test_plus_locks_*`

### F17-09 账本仍用 pytest 关协议行；审查中改口到另一 hash

- **严重度：** Medium（验证账本）
- **状态：** confirmed defect（账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：协议行 `pytest -q` / `passed_local_tests`；`executable_function` 159。页眉已写 r17 `3d0a0764…` 作废、r18 `3d0f1c10…`。那是交卷漂移，不是本轮冻结通过。

### F17-10 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes`、`assert_disjoint`、`card`、`apply_model_template`

### F17-11 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个）

### F17-12 ISSUES 点名关闭：A14-02 XOR 超售；A14-03/04/D14-05 实现项与独立 CE 对齐（测试力度不等）

- **严重度：** Medium（过程）
- **状态：** A14-02 XOR **超售**。A14-03/04、D14-05 generate **无「已闭但 CE 仍红」**。作者测试分别弱 / 残留弱析取 / CLI 只锁 `start>=`。
- **不要用本通道把 Goal/需求标 Complete。**

### F17-13 交卷 +2 donor 例不能回写声明冻结

- **严重度：** Medium（过程）
- **状态：** 交卷树独立 CE 同意 collect 复制 edits、兄 `prep` 不救命。开审测试文件没有这两例。
- **文件：** 交卷 `tests/test_round07_regressions.py` L321–342

### F17-14 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq = <digit>` **不是** pending_server。交卷哈希漂移 **不是** pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 协议行仍 `pytest -q`；可执行行仍 `passed_local_tests`（F17-09）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F17-00、F17-02、F17-07 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** 交卷 pytest 162/0。e2e 是 offline 烟测。声明冻结上的 160 **未**在 MATCH 盘复跑。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** 账本已跳到另一 hash。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：offline 前缀 H、强制 `q=`、XOR 超售、vacuous `all`。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪到 Goal 句。** 点名 CE 有独立记录。交卷 pytest 不能绑声明 hash。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学事件来自强制目标行。来源臂并集有测；必读 XOR 无。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语有。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 生成区只有强制 `q`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | A14-04 库路径独立见。r04 弱析取仍在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。跨进程无测试。孤立 Symbolic=`probe_train` 无误锁。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。科学 CLI 拒写玩具。夹具 fit 仍 echo。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。donor 一般性测试是交卷补丁。offline e2e 是 `unexpressible`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **162 passed，exit 0，35.30s，162 collected（交卷漂移盘）。** 无 skip/xfail。**不是** QA-01 / Goal §九.3。**不是**声明 hash 上的 160。 |
| 冻结 | **开审 HASH_MATCH `3d0a0764…`（61）。交卷 HASH_MISMATCH `3d0f1c10…`（仍 61）。** |
| 独立性 | 真 oracle：来源臂整题 generate；`>96` 拒；`noise_ref=0` 无 sham 不评空 \(N\)；scientific 同键 echo 会被现测抓住；孤立 Symbolic=`probe_train`。**不独立 / 锁错：** A14-02 并集当 XOR；A14-03 vacuous `all`；r04 空 \(N\) 弱析取；科学 CLI `start>=`；强制 `q=`；offline e2e。交卷 +2 donor 例不是冻结证据。 |
| Mock/stub | offline 前缀 H + 教员强制 `q=` + vacuous `all` + 弱析取 + 并集冒充 XOR。 |
| 论文行为仍未证明 | 真 Prefill KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT、必读源 XOR（两已存在叶） |
| 交付 vs 测试 | 「160 passed / A14-02 XOR 已闭 / e2e 已通」**超过** 冻结树测试力度。留 *a*+`src_b` **不能**写成论文 XOR。 |
| 已确认问题？ | **是。** Critical：F17-00、F17-07。High：F17-01、F17-02。A14-03/04、D14-05 generate **实现 CE 未失败**。A14-02 XOR **超售**。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。交卷哈希已漂。A14-02 测试锁错实现。Fixture e2e 仍 offline。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。修复后须对 **新** hash 重开计数；只补本文件不改变被审摘要。 |

在声明冻结上用 CE 级测试锁住 **必读源不是 base 的 rename**（或显式拒绝值多重集同构）、**scientific probes 必须存在 4 条无分数的 `refused_not_section8`（禁止 vacuous `all`）**、**禁止 r04 弱析取把已评估空 \(N\) 保绿**、**科学 CLI 整题（不只 `start>=`）**、以及 **非 offline 前缀 H 的 e2e** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。交卷多出的兄目录 / 非 `prep` 名 donor 例 **不能**把本轮改写成通过。A14-03/04 与 D14-05 generate 的实现闭合记在 F17-03…05，不是通道通过。
