# F：验证质量与反向质疑（round-18）

独立审查通道 F。未改 `src/`、`tests/`、`pyproject.toml`。未读 round-18 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 写在 `.planning/audits/round-18/_f_scratch/`，不把 `tests/test_round06_regressions.py` / `tests/test_round07_regressions.py` 当证明。

**先行结论：** 按 `VERSION.md` 原文复算，开审与交卷冻结哈希 **一致（HASH_MATCH）** `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（61 文件，0 CRLF）。本机 `python -m pytest -q --tb=line` 为 **162 passed / exit 0 / 35.53s**，与作者 `pytest_author_claim: 162` 一致。这不是 Goal 通过。

独立 CE（34 条，不跑 r06/r07 测试文件）：F15-01 兄弟 `prep` 行走 **已闭**——`stage_a`/`stage_b`、`alpha`/`omega` 都能配上 `same_value_diff_source`；删掉 collect 里的 `edits.jsonl` 后即使兄目录仍叫 `prep` 也落到 `same_identity_fallback`。**没有**剩下的测试「只因为兄目录名叫 `prep` 才绿」。A14-02 图（留叶 *a*、加等值 `src_b`、父母改读 *b*）**实现闭**；`{p1,p2,src_b}` 集合相等不是唯一指纹（三前提 rename `p3→src_b` 同集）。A14-03 scientific fit 写出四条 `refused_not_section8` 且无 score **实现闭**；同一前缀上的 echo verbalizer 会打出 `score=1.0`，作者过滤在省略行时空真。A14-04：真实前提 `noise_ref=0` 且无 `sham:` **不**记成已评估空 \(N\)（对照合法 `noise_evaluated=True` 得 `rho_M_noise=1.0`）。D14-05：**generate** 全题干闭（49 字 alt-source、70 字不截、97 字拒）；`start>=prompt_len` 单独不够。**两条本通道确认缺陷：** (1) `apply_rename_edit({p1:p2,p2:p1})` 顺序改写把题干变成 `p1 = 4. p1 = 0. What is q = p1 * p1?`；(2) `cmd_intervene` 仍 `ids=ids[:64]`，70 字题干 `prefix_truncated=True`。Fixture 八段仍 offline；fixture fit 仍 echo 前缀打 1.0；科学 sham 弱析取仍在。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21 03:06（Asia/Shanghai） |
| 声明冻结 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` |
| 开审复算 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` |
| 交卷裁决 | **HASH_MATCH**（与声明同一摘要） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明 / 开审 / 交卷都是 **61**。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| pytest | **162 passed in 35.53s，exit 0。** Collect：**162 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 162 passed`。命令结果独立确认。当作 Goal / 阶段验收：**否。** |
| 范围 | 61 冻结文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。 |
| 明确未读 | `.planning/audits/round-18/{A,B,C,D,E}-*.md` |
| 独立 CE | `.planning/audits/round-18/_f_scratch/f18_ce.py` → `f18_ce_results.json`（34 条：32 闭 / 2 红）。未 import r06/r07 测试模块。 |

审查对象是**声明冻结字节**。pytest 与点名 CE 均在 HASH_MATCH 盘上执行。交卷哈希未漂。

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
| `tests/test_round06_regressions.py` | 146 | `b555ed24000400e1…` | `start>=len(prompt)`；`prep`/`col` 上 `donor_kind`；scientific fit 过滤 `status==refused_not_section8`；sham 析取 |
| `tests/test_round07_regressions.py` | 342 | `8c23db4b637c8c70…` | 祖先 tasks 拒；alt-source 图+全题干；未知不进 \(M\)；`noise_ref=0` 手造 Label；`_load_source_value_pair` 兄 `prep`；`stage_a`/`stage_b` 配对 |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer 形状、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only：**162 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r15（159 / `test_round07` 15 例）：本冻结 `test_round07` 为 18 例（加 `noise_ref=0` 手造、loader 不走兄 `prep`、`stage_a`/`stage_b` 配对）。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | `ρ=y` 泄漏仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed；无 generate 不可用 | fixture CLI **echo 前缀**无测试红；`attention_mean`/`rollout` 作者无数值 oracle（本通道独立补了 rollout） |
| `cli.py` | 1260 | `9431b7768fda6a3c…` | smoke offline；scientific prepare/collect/fit/intervene；孤立 fit 拒；A12-03；collect 复制 edits；`_load_source_value_pair` 只读 in-dir | **intervene `cap=64` 无测试**；calibrate 仍搜兄 `lab`/`label`/`labels`；scientific calibrate 出有限 \(q\) |
| `edits.py` | 365 | `1e5b97d63a62ab78…` | value/alt-source 图；rename `{p1:alpha}` | **重叠映射顺序改写未锁** |
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
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584；`n<d` truncated | `apply_map` 数值恢复未锁 |

夹具 JSON **不在冻结内**。`models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 仅包说明。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `3d0f1c10…c0952f`（61，0 CRLF） |
| 交卷再算 | 同脚本 | **HASH_MATCH** 同一摘要 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **162 passed in 35.53s，exit 0**。无 skip/xfail/deselected |
| Collect | `python -m pytest tests --collect-only -q` | 162 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对冻结 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]` | **存在的单元断言**与独立算术一致 |
| **独立 CE** | `_f_scratch/f18_ce.py`（`PYTHONPATH=src`） | 34 条：32 闭 / 2 红。见 §3.1。 |

### 3.1 点名独立 CE（不信测试文件）

| CE | 独立结果（本冻结） | 作者测试是否锁住 |
|---|---|---|
| **兄弟 `prep` / `stage_a`/`stage_b` 配对** | **闭（配对不再靠目录名）。** `_load_source_value_pair` 对兄 `prep`/`prepare`/`s-prep` 与父目录 `edits.jsonl` 皆 `None`。collect 复制 edits。`stage_a`→`stage_b`：`donor_kind=same_value_diff_source`，unit pair `(0,3,same_value_diff_source)`。`alpha`/`omega` 同。**删** `stage_b/edits.jsonl` 后 `same_identity_fallback`。`prep`/`col` 布局但 col 无 edits → **也是 fallback**。 | `test_load_source_value_pair_*` 只锁兄名 `prep`。`test_intervene_pairs_source_without_prep_sibling_name` 锁 copy+配对，**不**删 edits。`test_scientific_h_is_finite_and_pairs_donor` 仍用 `prep`/`col` 名，但独立证明它**不是**唯一救命条件。 |
| **XOR `{p1,p2,src_b}` vs rename** | **图闭；rename 原语未闭。** alt-source：集 `{p1,p2,src_b}`，父母 `[p1,src_b]`，表达式 `p1 * src_b`，题干 `p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?`。rename(`p2→src_b`)：集 `{p1,src_b}`，XOR=`{p2}`，题干不再含 `p2 = 0`。三前提 rename(`p3→src_b`)：**同集** `{p1,p2,src_b}` 但父母仍 `[p1,p2]`。**swap `{p1:p2,p2:p1}` 顺序改写：** 题干 `p1 = 4. p1 = 0. What is q = p1 * p1?`，表达式 `p1 * p1`，id 集仍 `{p1,p2}`。 | 作者锁 alt-source 图+全题干，以及 `{p1:alpha}`。**不锁** rename≠alt-source（同映射 `src_b`），**不锁** 重叠映射，**不锁** 三前提集合碰撞。 |
| **scientific fit vs zeros/echo** | **实现闭；作者过滤弱。** scientific probes：1 条 verbalizer + 3 条 attention，皆 `refused_not_section8`，`score is None`。同一 scientific 前缀上 echo `generate_fn=λp.prefix` → `status=generated`，`score=1.0`，抽出 `82`（教员行 `\nq = 82`）。zeros/`generated` 同样会被本 CE 红。fixture fit：**四档里三档 echo 打 1.0**（抽出夹具 `0`）。 | `all(status==refused if baseline in {…})`：**省略这些行则空真**。不要求行存在，不禁 `score=0` 且 status 仍 refused。 |
| **`noise_ref=0` 真实前提** | **闭。** 手造 Label `p1/p2` `noise_ref=0.0`、\(T\) 已覆盖、无 sham：`rho_M_raw=1.0`，`rho_M_noise/excess=None`，`null_reason=noise_set_missing`。对照合法已评估空 \(N\)：`rho_M_noise=1.0`，`excess=0.0`。`build_labels` 对真实前提永不写 0。scientific prepare 真实前提 `noise_ref is None`。 | 作者手造 Label 锁 excess/noise 为 None。**不锁** `null_reason`。空集+`noise_evaluated=False` 也会让作者绿。 |
| **D14-05 全题干** | **generate 闭；intervene 未闭。** alt-source 49 字：`prompt_text==question`，含 `* src_b` 与 `p2 = 0`，`prompt_len=49`。70 字不截。97 字 `ValueError: tiny prompt exceeds context`。事件 `q` start=58≥49。**intervene** 对 70 字题干 `prefix_truncated=True`（`cli.py` L950–952 `cap=64`）。 | r07 锁 alt-source 全题干。r06 **只** `start>=len(prompt)`。**无** 70 字 / 97 字 / intervene cap 测试。 |
| **A13-02 \(T\) 未覆盖** | **闭。** 仅 p1 已知：`M=[]`，`rho_M_raw=None`，`behavior_unknown=True`。 | 作者只锁全未知。 |
| **A13-03 \(T\) 覆盖 + sham no-change** | **闭。** `rho_M_raw=0.0`，`noise/excess=None`，`null_reason=noise_set_missing`；sham 行 `noise_ref=0.0`。 | 作者混杂例偏弱；科学 CLI 弱析取。 |
| **A12-03 / 孤立 fit** | **闭。** 孤立 feat/labs → `ValueError: … tasks.jsonl`。`_find_tasks_jsonl` 不读祖先。 | 锁祖先 `col/`。兄 prep 作者不锁；独立已拒。 |
| **A10-04 persist** | **半闭。** Plus 后 Symbolic=`test`；RAM `.clear()` 后磁盘仍锁。 | 锁同进程。**不 spawn。** 套件后磁盘仍含 `gsm8k-12` + Ada 键。 |
| **scientific collect 拒 offline** | **闭。** | 作者锁。 |
| **scientific calibrate** | **跑通且写出有限 \(q=0.005…\)**（tiny bilinear 玩具分数）。不是 §8 校准科学结果。 | 作者无 scientific calibrate 数值 oracle。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **`all(status==refused_not_section8 for row if baseline in {verbalizer,…})`** | 无此类行 → 空真。本冻结实现写了四行，所以作者绿是真的；过滤本身不要求存在。 |
| **`start>=len(prompt)`** | 若 `prompt_text` 被截，事件仍可在截断后。r07 全题干补了 alt-source；70/97 与 intervene cap 仍未锁。 |
| **`prep`/`col` 目录名** | 复制 edits 后不再必要。删 col 的 edits 后 fallback——说明 r06 配对例现在靠 copy，不是靠兄名。 |
| **`{p.premise_id}=={p1,p2,src_b}`** | 三前提 rename 也能凑出该集。作者还锁父母/表达式，所以**该测试**不是纯集合替身。 |
| **`rho_M_excess != 1.0 or null_reason`** | `None != 1.0` 单独过。 |
| **`null_reason in {…} or rho_M_noise is None`** | `noise is None` 单独过。 |
| **`rho_S_noise is None or null_reason in {…}`** | r06 析取仍在。 |
| **教员强制 `q=`** | echo CE 前缀含 `\nq = 82`。科学事件 `any(q)` 仍可被该行单独满足。 |
| **offline H 当 e2e** | 八段 exit 0。`H`←`token_ids[:8]`。analyze 无 P1 表。smoke **要求**空结论。 |
| `timing != "pre_step"` | 任意其他字符串都绿。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_plus_locks_*` | 同进程 RAM clear。**不**新进程。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| pytest 后 persist 泄漏 | 162 passed 之后磁盘为 `["gsm8k-12", "q:ada has 4 apples…"]`。该文件不在 61 摘要内。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：页眉写 r18 须独立复核且 pytest 不得关可执行行；协议行仍用 `python -m pytest -q` + `passed_local_tests`；`executable_function` 计数仍写 **159**。 |
| scientific calibrate | 对 tiny 探针写出有限非conformity 分数。不是论文校准。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-18 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 `_f_scratch` 与 §8 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| Plus persist 新解释器 | 本通道只做了同进程 RAM clear；作者也不 spawn |
| 把 Goal 标 Complete | 本通道只评验证质量 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 162 passed | `VERSION.md` | **命令是。** 当作 Goal：**否。** |
| F15-01 collect 复制 edits；loader 不走兄 `prep` | ISSUES | **独立同意（含 prepare/s-prep/父目录/删 copy）。** 作者 loader 例只点名 `prep`。 |
| A14-02 留叶 *a*，追加等值 `src_b` | ISSUES | **图独立同意。** 集合相等不是唯一指纹。rename 重叠映射 **超售为「rename 原语已正确」。** |
| A14-03 scientific fit 对 §8 玩具写 `refused_not_section8` | ISSUES | **实现同意。** 作者过滤可空真。fixture fit 仍 echo。 |
| A14-04 真实前提 `noise_ref=0` 且无 sham → excess null | ISSUES | **独立同意。** 作者不锁 `null_reason`。 |
| D14-05 tiny 不再 48 字符截断 | ISSUES | **generate 同意。** intervene 仍 64 字静默截。r06 只锁 start。 |
| A13-01 / A13-02 / A13-03 / A12-03 / A10-04 | ISSUES | 图 / \(M\) / 空 \(N\) / tasks 查找 / persist 机制：**实现同意。** CLI 一般性与作者测力度见上。 |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` | **本套件不能作证。** 本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`（scientific+tiny）；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击：**

- **配对不得靠兄目录名 `prep`。** 回到兄弟行走会让独立 loader CE 红，也会让「删 copy」intervene 再变成 source 臂。作者 `stage_a`/`stage_b` 在 **有 copy** 时会红若配对丢了；**有 copy 时不证明无行走**。独立删 edits 补上了。
- **alt-source 必须留 *a*、加 *b*、改父母。** 钉死旧表达式或改答案会红。**实现闭。**
- **rename(`p2→src_b`) 不得等于 alt-source。** 作者不锁。实现目前不等（XOR=`{p2}`）。
- **重叠 rename 必须同时替换。** 当前顺序改写。作者 `{p1:alpha}` 不红。**独立 CE 红。**
- **scientific fit 必须写出 refused 行且无 generated/echo 分。** 作者过滤可空真。实现写了行。echo 对照 `score=1.0`。
- **真实前提 `noise_ref=0` 不得当已评估空 \(N\)。** 独立与作者都红那种错实现。
- **generate 必须保留全题干，或拒截断。** 49/70/97 独立闭。r06 的 start 锁不够。
- **intervene 前缀必须完整或显式拒。** `cap=64` 静默截。**作者不锁。独立红。**

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_generated_events_exclude_prompt_assignments` | 只锁 `start>=len(prompt)`。截断 `prompt_text` 仍绿。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 `donor_kind` | 目录名 `prep`/`col`。现在靠 copy 也能绿；**不是**「只因兄名」——但也**不**攻击删 edits / 行走回归。fit 过滤可空真。 |
| `test_source_value_pair_rewrites_graph_ids` 的集合行 | 单独不够（三前提 rename 碰撞）。整例还锁父母/表达式/全题干，**该例整体仍独立。** |
| `test_rename_keeps_expression` | 单键非重叠。重叠 swap 仍绿。 |
| `test_load_source_value_pair_does_not_walk_sibling_prep` | 只点名 `prep`。独立见到 `prepare`/`s-prep`/父目录同样不走——实现更严，测试偏窄。 |
| `test_intervene_pairs_source_without_prep_sibling_name` | 不删 copy。不证明无行走。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `!= 1.0 or null_reason`。 |
| `test_observed_real_noise_ref_without_sham_*` | 不锁 `null_reason`。 |
| `test_unknown_behavior_is_not_counted_as_m` | 只锁全未知。 |
| `test_plus_locks_symbolic_family_to_test` | 不 spawn。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_p1_held_out_logistic_detects_rho` | `ρ=y` 在全部行。 |
| `test_tiny_hooks` L17 | 恒真。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。
2. **scientific fit 用「若存在则 refused」盖住「必须存在且无 echo 分」。**
3. **r06 用 start≥ 盖住全题干；intervene 用 37 字夹具盖住 64 cap。**
4. **r06 配对例用 `prep`/`col` 习惯名，靠 copy 绿，不攻击行走回归。**
5. **A14-02 用集合+父母锁图，不锁 rename 重叠映射。**
6. **科学事件非空，来源仍是教员强制 `q=`。** echo CE 直接吃到 `\nq = 82`。
7. **A10-04 作者测试用同进程磁盘读盖住「新解释器」。**
8. **套件把 Plus 键写进仓库缓存且多数用例不 `clear`。**
9. **账本协议行仍 pytest。**
10. **calibrate 仍搜兄 `lab`/`label`/`labels`（A12-03 只收紧了 tasks）。**

**仍无作者测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes` 恢复、`card`、`apply_model_template`。本通道对 `score_qa` / `assert_disjoint` / rollout 做了独立 CE，**不是**套件锁。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加生产测试。脚本：`_f_scratch/f18_ce.py`。

### CE-1 配对不靠 `prep` 名（实现闭；作者测窄）

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

prep/col but col has no edits:
  donor_kind == same_identity_fallback
```

### CE-2 rename XOR / 顺序改写（图闭；swap 红）

```text
alt-source: premises {p1,p2,src_b}, parents [p1,src_b], expr p1 * src_b
rename(p2→src_b): {p1,src_b}, XOR={p2}, question has no "p2 = 0"
rename 3-premise (p3→src_b): set == {p1,p2,src_b} but parents [p1,p2]

apply_rename_edit({p1:p2, p2:p1}):
  question == "p1 = 4. p1 = 0. What is q = p1 * p1?"   # FAIL simultaneous
  should be "p2 = 4. p1 = 0. What is q = p2 * p1?"
```

### CE-3 scientific fit vs echo/zeros（实现闭；作者过滤弱）

```text
scientific probes:
  verbalizer/attention_* exist
  status == refused_not_section8
  score is None

echo generate_fn(prefix) on same scientific prefix:
  status=generated, score=1.0, extracted=82

fixture fit verbalizer zeroshot/fiveshot/reflection:
  status=generated, score=1.0, extracted=0
```

### CE-4 `noise_ref=0` ≠ 已评估空 \(N\)（实现闭）

```text
Labels p1,p2 noise_ref=0.0, T covered, no sham:
  rho_M_noise=None, excess=None, null_reason=noise_set_missing
legal empty N (noise_set=[], evaluated=True):
  rho_M_noise=1.0, excess=0.0
build_labels real premises: noise_ref is None
```

### CE-5 D14-05 全题干（generate 闭；intervene 红）

```text
alt-source question len 49 == prompt_text == prompt_len
70-char question: prompt_text intact
97-char: ValueError refuse truncated
intervene 70-char fixture: prefix_truncated=True  # cap=64
```

### CE-6 反向：CLI / 数学 — 独立 CE vs 烟测

| 分支 / 函数 | 本通道 | 作者套件 |
|---|---|---|
| prepare fixture | 烟测（作者） | 烟测 |
| prepare scientific | 独立跑 + 事件/labels | 多例，事件可被强制 `q=` 满足 |
| collect scientific tiny / 拒 offline | 独立 | 锁 |
| collect offline e2e | 作者烟测当成功 | 烟测 |
| fit scientific §8 拒绝 | 独立（要求行存在） | 过滤可空真 |
| fit fixture verbalizer | 独立：echo 1.0 | **不锁** |
| fit 孤立无 tasks | 独立 | 锁 |
| calibrate scientific | 独立：有限玩具 \(q\) | 无数值 oracle |
| calibrate 兄 `lab/` 行走 | 读到代码仍走 | **不锁** |
| intervene tiny + 删 edits | 独立 fallback | 不删 |
| intervene 长前缀 | **截断** | 不锁 |
| repair k=1..5 | 作者 | 锁形状 |
| analyze 假 P1 / 空结论 | 作者 | 锁弱 |
| `apply_rename_edit` 重叠 | **顺序破坏** | 不锁 |
| `score_qa` / `assert_disjoint` / rollout 数值 | 独立补 | 作者无 |
| `attention_mean` 非空权重 / `procrustes` 恢复 / `card` / `apply_model_template` / `forbid_host_exec` | 无独立数值 oracle | 无 |
| Plus persist 新进程 | 未 spawn | 未 spawn |

## 9. 发现

### F18-00 开审与交卷哈希可复算且一致

- **严重度：** —
- **状态：** HASH_MATCH（过程通过）
- **文件：** `.planning/audits/round-18/VERSION.md` L5–23；61 = `3d0f1c10…c0952f`；0 CRLF
- **复现：** 脚本原文开审与交卷同一摘要。

### F18-01 绿 162 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** `162 passed / 0 / 35.53s`，162 collected。作者主张与命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 是 offline 烟测。

### F18-02 F15-01：配对不再靠兄目录名 `prep`（点名闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE，含 `prepare`/`s-prep`/父目录/删 copy/`alpha`/`omega`）
- **作者主张 F15-01：** **实现同意。** 作者 loader 例偏窄；`stage_a`/`stage_b` 不删 copy。
- **点名问题「是否还有测试只因兄名 `prep` 才绿」：** **否。** r06 `prep`/`col` 现在靠 collect 复制。删 col edits 后 fallback，说明不是行走救命。

### F18-03 `apply_rename_edit` 对重叠映射做顺序改写（点名红）

- **严重度：** High（正确性 / 验证）
- **状态：** confirmed defect
- **文件：** `edits.py` `_rewrite_ids` / `apply_rename_edit`
- **复现：** `{p1:p2, p2:p1}` → `p1 = 4. p1 = 0. What is q = p1 * p1?`，表达式 `p1 * p1`。同时替换应是 `p2 = 4. p1 = 0. What is q = p2 * p1?`。
- **作者主张 A14-02：** 图半句 **同意**。不得写成「rename 原语已与 alt-source 可区分且替换正确」——重叠映射未锁且实现错。

### F18-04 `{p1,p2,src_b}` 集合相等不是 alt-source 唯一指纹

- **严重度：** Medium（验证设计）
- **状态：** confirmed（测试设计）。实现上 alt-source ≠ rename(`p2→src_b`)（XOR=`{p2}`）。
- **复现：** 三前提任务 rename `p3→src_b` 得到同一集合，父母仍 `[p1,p2]`。作者整例还锁父母/表达式，故 **该测试整体仍独立**；单行集合断言不够。

### F18-05 A14-03 scientific fit 拒绝 §8 玩具（实现闭；作者过滤弱）

- **严重度：** Medium（验证残留）
- **状态：** 实现闭合。作者 `all(... if baseline in …)` 可空真。
- **复现：** §3 CE-3。echo 对照 `score=1.0`。本 CE 要求行存在且 `score is None`——echo/zeros/`generated` 会红。

### F18-06 fixture fit 仍把 trace 前缀 echo 成 verbalizer，并打 1.0

- **严重度：** High（验证 / 科学口径）
- **状态：** confirmed defect（fixture 路径）。A14-03 只主张 scientific。
- **文件：** `cli.py` `cmd_fit` `gen = (lambda p, t=prefix: t)`
- **复现：** zeroshot/fiveshot/reflection 皆 `generated` / `score=1.0` / `extracted=0`（夹具文本里的答案）。

### F18-07 A14-04：真实前提 `noise_ref=0` 不记已评估空 \(N\)（点名闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE + 合法空 \(N\) 对照）
- **作者主张 A14-04：** **实现同意。** 作者不锁 `null_reason`。

### F18-08 D14-05：generate 全题干闭；intervene 仍 64 字静默截断

- **严重度：** High（正确性 / 验证）
- **状态：** generate 闭合。intervene **confirmed defect**。
- **文件：** `models/generate.py` `>96` 拒绝（闭）；`cli.py` L950–952 `cap=64`（未闭）
- **复现：** 49/70/97 见 §3。70 字 scientific intervene `prefix_truncated=True`，`event_aligned` 因而为假。夹具 37 字题干碰不到此 cap，所以 r06/r07 仍绿。
- **作者主张 D14-05：** generate **同意。** 「tiny 不再截断」若包含 intervene 前缀 **超售。** r06 `start>=prompt_len` **不够。**

### F18-09 科学 sham / 噪声弱析取仍绿

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）
- **文件：** `test_scientific_sham_*`；`test_sham_hits_do_not_book_evaluated_zero_noise`；`test_sham_hits_do_not_broadcast_*`

### F18-10 Fixture e2e 仍 offline；科学事件仍接受教员强制 `q=`

- **严重度：** Critical（验证）
- **状态：** confirmed defect（验证）。作者 ISSUES 已承认八段是 offline 前缀 H、约束 `\nq=` 不是 §4.1 — **不要超售成科学 e2e / 自然 CoT。**
- **复现：** smoke 要求空结论。echo CE 前缀含 `\nq = 82`。

### F18-11 Plus persist：RAM clear 闭；作者缺 subprocess；套件泄漏缓存

- **严重度：** Medium（验证卫生）
- **状态：** 机制闭合；测试不覆盖新进程。162 passed 后磁盘仍有 Plus 键。
- **作者主张 A10-04：** **机制同意。**

### F18-12 calibrate 仍搜兄 `lab`/`label`/`labels`

- **严重度：** Medium（验证 / A12-03 残余）
- **状态：** confirmed defect（范围：labels 查找，不是 tasks）
- **文件：** `cli.py` `cmd_calibrate` `label_dirs.extend(..., feat_dir.parent / "lab", ...)`
- **注：** A12-03 主张只谈 `_find_tasks_jsonl`。独立同意 tasks 半句。labels extras 是另一条。

### F18-13 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：页眉自相矛盾（r18 写 pytest 不得关可执行行；行内仍 `python -m pytest -q` + `passed_local_tests`）。`executable_function` 计数 **159**（本冻结作者称 162）。

### F18-14 夹具排除在冻结外；仍有大块零测试符号

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议 / 覆盖）
- **文件：** `tests/fixtures/*.json`（10 个）
- **符号：** `card`、`apply_model_template`、`forbid_host_exec`、`procrustes` 数值恢复、非空 `attention_mean`

### F18-15 ISSUES 点名关闭：F15-01 / A14-02 图 / A14-03 实现 / A14-04 / D14-05 generate 与独立 CE 对齐；rename 重叠与 intervene cap **超售或未主张**

- **严重度：** Medium（过程）
- **状态：** 见上。无「写已闭但点名 generate/配对/噪声 CE 仍红」。**有**「未写闭但独立红」：F18-03、F18-08 intervene。
- **不要用本通道把 Goal/需求标 Complete。**

### F18-16 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq=`、intervene 64 字截断 **不是** pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 协议行仍 `pytest -q`；可执行行仍 `passed_local_tests`（F18-13）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F18-03、F18-08、F18-10 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 162/0。e2e 是 offline 烟测。重叠 rename 与 intervene cap 无测试。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** 账本可执行计数仍 159。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 哈希匹配（好）。本通道 **提交已确认缺陷**。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：offline 前缀 H、强制 `q=`、intervene 64 cap、顺序 rename、fixture echo verbalizer。 |
| 7 | 交付包 | **问题闭环未就绪到 Goal 句。** pytest 记录存在（162/0）。点名 CE 有独立记录。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。alt-source 图+generate 题干有测。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、alt-source 图有。重叠 rename **未锁且错**。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | `noise_ref=0` / 未知 \(M\) / sham missing 独立见。弱析取仍在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test、family persist 有。跨进程无测试。`assert_disjoint` 作者无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。intervene 长前缀被 64 cap 切。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。scientific 拒 §8 **实现有、作者过滤弱**。fixture echo 打满分。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。scientific calibrate 出玩具有限 \(q\)，无独立 oracle。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。配对不再靠 `prep` 名。offline e2e 是 `unexpressible`。长前缀截断。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **162 passed，exit 0，35.53s，162 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH `3d0f1c10…c0952f`（61，开审=交卷）。** |
| 独立性 | **独立闭：** 配对不靠 `prep` 名（含删 copy）；alt-source 留 *a* 加 *b*；rename(`p2→src_b`)≠alt-source；scientific fit 拒绝行存在且无 score；`noise_ref=0`≠已评估空 \(N\)；generate 全题干 49/70/97；\(T\) 未覆盖不进 \(M\)；\(T\) 覆盖+sham 不评空 \(N\)；孤立 fit；scientific collect 拒 offline。**独立红 / 不独立：** 重叠 rename 顺序改写；intervene `cap=64`；作者 scientific-fit 过滤可空真；r06 `start>=`；科学 sham 弱析取；强制 `q=`；offline e2e；fixture echo verbalizer；作者缺 subprocess。 |
| Mock/stub | offline 前缀 H + 教员强制 `q=` + echo generate_fn + 可空真过滤 + `start>=` + 短夹具盖住 64 cap + 弱析取 + 同进程 persist。 |
| 论文行为仍未证明 | 真 Prefill KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT 事件、同时替换的 rename、未截断的 intervene 前缀 |
| 交付 vs 测试 | 「162 passed / 点名全闭 / e2e 已通」**超过** 冻结树测试力度。F15-01/A14-02 图/A14-03 实现/A14-04/D14-05 generate **不能**写成 rename 原语与 intervene 前缀已闭。 |
| 已确认问题？ | **是。** Critical：F18-10。High：F18-01、F18-03、F18-06、F18-08。点名作者关闭项除 rename 重叠与 intervene cap 外 **实现 CE 未失败**。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。重叠 rename 顺序破坏。intervene 仍静默截 64。Fixture e2e 仍 offline。弱析取与可空真过滤仍绿。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷。修复后须对 **新** hash 重开计数；只补本文件不改变被审摘要。 |

在用 CE 级测试锁住 **同时替换的 `apply_rename_edit`**、**intervene 全前缀或显式拒截断（禁止只靠 `start>=prompt_len`）**、**scientific fit 行必须存在且无 echo/zeros 分（禁止可空真过滤）**、**非 offline 前缀 H 的 e2e**、以及 **非强制 `q=` 的科学事件（或显式 constrained_target 合同）** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。F15-01 配对、A14-02 图、A14-03 实现、A14-04、D14-05 generate 的闭合记在 F18-02/05/07/08 前半，不是通道通过。
