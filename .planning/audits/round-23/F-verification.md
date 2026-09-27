# F：验证质量与反向质疑（round-23）

独立审查通道 F。未改 `src/`、`tests/`、`pyproject.toml`。未读 round-23 其他通道报告。未把 `.planning/audits/round-22/{A,B,C,D,E,F}-*.md` 当本树证据。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 写在 `.planning/audits/round-23/_f_scratch/`，不把 `tests/test_round06_regressions.py` / `tests/test_round07_regressions.py` 当证明；只抄断言文本。

**先行结论：** 按 `VERSION.md` 原文复算，开审与交卷冻结哈希 **一致（HASH_MATCH）** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（61 文件，0 CRLF）。本机 `python -m pytest -q --tb=line` 为 **172 passed / exit 0 / 24.30s**，与作者 `pytest_author_claim: 172` 一致。这不是 Goal 通过。

独立 CE（35 条，不 import r06/r07 测试模块）：**点名重攻已闭，且不以 `prefix_truncated is not True` / `inspect.getsource` 为充分。**

1. **Sham lock。** 抄出的 `_scientific_sham_lock` 在 `rho_M_excess=0.0`、`events=[]`、借口下账面 `1.0`、事件缺 `null_reason` 上失败。旧弱锁 `rho_M_excess != 1.0 or null_reason` 对 `0.0` 与空事件仍绿。作者科学 sham 关闭条件是合取锁 + `assert not` 四伪造，**不是**只靠该弱析取。单元 sham 五例是 excess/noise 皆 `None` **且** `null_reason == noise_set_missing`，不是 `is None or null_reason`。
2. **70 字 CLI intervene。** 独立间谍 `intervene_hidden_decode`：五次 `prompt_ids` 长度皆 **79**，**无一 ≤64**。`cmd_calibrate` 有兄 `lab/WRONG` 与无兄：finder 实参 `(None, fit, feat)`，**未传入兄路径**，写出的 `calibration.jsonl` **相同**。
3. **§8。** 从作者源码抄出的断言在省略四行或 `refused+score=1.0` 时失败。旧 `all(... if baseline in S)` 对这两种输入仍恒真——**不当作充分**。
4. **点名 oracle。** `card` 4096/3584；`forbid_host_exec` 不调用被包函数；Procrustes 恢复独立 90°；`attention_mean` 用前提下标（权重 `[0.05,0.80,0.10,0.05]`）；`apply_model_template` 只对 `qwen3` 把 `enable_thinking` 传给 tokenizer。
5. Fixture 八段仍 offline 前缀 H；scientific tiny 仍 `constrained_target`——按任务口径这是诚实项，**不**开成缺陷，也 **不** 当 MODEL-01 / 自然 CoT。夹具不进冻结是协议。Plus persist 残留是卫生。账本页眉写 pytest 不得关可执行行；本冻结 **没有** 新声称「协议行仅由 pytest 关闭」。

本通道 **通过**。通道通过 **不是** Goal 验收，也 **不** 宣布 Goal 完成。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21 03:48–04:20（Asia/Shanghai） |
| 声明冻结 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` |
| 开审复算 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` |
| 交卷裁决 | **HASH_MATCH**（与声明同一摘要） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明 / 开审 / 交卷都是 **61**。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| pytest | **172 passed in 24.30s，exit 0。** Collect：**172 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。未用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 172 passed`。命令结果独立确认。当作 Goal / 阶段验收：**否。** `ISSUES.md` 称 r22 A–F 已 PASS、连续通过 = 1——**只当作者主张，不当本树证据。** |
| 范围 | 61 冻结文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。 |
| 明确未读 | `.planning/audits/round-23/{A,B,C,D,E}-*.md`；未把 `.planning/audits/round-22/{A,B,C,D,E,F}-*.md` 当证据 |
| 独立 CE | `.planning/audits/round-23/_f_scratch/f23_ce.py` → `f23_ce_results.json`（35 条：35 闭 / 0 红）。未 import r06/r07 测试模块。 |

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
| `tests/test_round04_regressions.py` | 319 | `dd541f91c2f9061e…` | r04；`timing != pre_step`；helper 上合法已评估空 \(N\)；bootstrap 非空；零 hit 事件行 **合取** None + `noise_set_missing` |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；analyze 不锁 p1 |
| `tests/test_round06_regressions.py` | 156 | `b9bece3ea0bc90cd…` | `start>=len(prompt)`；`prep`/`col` 上 `donor_kind`；scientific fit **集合相等四条 §8 + refused + `score is None`**；sham **合取** excess/noise None + `null_reason` |
| `tests/test_round07_regressions.py` | 562 | `9ab6c6f669dc250d…` | r07 节点 + swap 题干；`_tiny_prefix_ids` helper 70/97；**CLI intervene 间谍 `all(n > 64)` + `prefix_n`**；**`cmd_calibrate` 实跑 finder 不含兄 `lab`**；**`_scientific_sham_lock` 合取 + 四伪造必须失败**；单元 sham 合取；**`card` / `forbid_host_exec` / Procrustes / `attention_mean` / `apply_model_template` oracle** |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer 形状、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 24 | `a829677e50795d36…` | hook 清理；无恒真 `assert layer.__class__.forward` |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle。协议，不是缺陷。 |
| `pyproject.toml` | 27 | `cb44851f7fbf7bf7…` | pytest `testpaths`/`pythonpath`；integration marker |

Collect-only：**172 nodes**（`test_tiny_hooks` 1 函数 × 2 kind = 2 nodes；其余 `def test_` 合计 171 函数节点）。零 `skip` / `xfail` / `skipif` / `unittest.mock`。弱析取 `rho_M_excess != 1.0 or null_reason` **只**出现在作者用来证明旧锁仍绿的 `weak = lambda`（`test_round07` L273），**不是**科学 sham 关闭条件。旧 `prefix_truncated is not True` 对 `{False, n_ids:64}` 仍绿——**本通道不接受它为充分**。作者套件 **无** `inspect.getsource(cmd_calibrate)`。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8、**Procrustes 数值** | `ρ=y` 泄漏仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed；**`attention_mean` 下标** | fixture CLI **echo 前缀**；`attention_rollout` 作者无数值 oracle |
| `cli.py` | 1268 | `cc5eae53d7be27eb…` | smoke offline；scientific prepare/collect/fit/intervene；孤立 fit 拒；collect 复制 edits；CLI 70 间谍；calibrate 实跑 finder；scientific fit 四条 refused 无分 | `cmd_intervene` 仍硬编码 `prefix_truncated=False`（L959），另写 `prefix_n`（L960） |
| `edits.py` | 367 | `cc8e2d23592a3ab8…` | value/alt-source 图；rename `{p1:alpha}`；swap 例 | 三前提集合碰撞仍非作者指纹 |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False`；**`forbid_host_exec` 不调用** | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP/范数 | `ie_z` helper 仍是均值差 |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 405 | `985b9d9328e4111f…` | 未知 \(M\)；`noise_ref=0` 手造；unit 噪声扣除 | C7 helper 不走 labels |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **`card` 4096/3584** | `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 200 | `6e6040394ac641c7…` | 全题干 + `>96` 拒；**`apply_model_template` qwen3-only thinking** | r06 仍只锁 `start>=` |
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
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584 拒；`n<d` truncated；`apply_map` 经独立 Procrustes | — |

夹具 JSON **不在冻结内**。`models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 仅包说明。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `1f5f3798…19c7bcdb`（61，0 CRLF） |
| 交卷再算 | 同脚本 | **HASH_MATCH** 同一摘要 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **172 passed in 24.30s，exit 0**。无 skip/xfail/deselected |
| Collect | `python -m pytest tests --collect-only -q` | 172 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对冻结 `tests/**` 检索 | 无 skip/xfail/mock；`assert True` 只在载荷字符串 |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；顺序 swap 应变 `p2 * p1`；70/97 token | **存在的单元断言**与独立算术一致；swap/70/97 另由独立 CE 核 |
| **独立 CE** | `_f_scratch/f23_ce.py`（`PYTHONPATH=src`） | 35 条：35 闭 / 0 红。见 §3.1。 |

### 3.1 点名独立 CE（不信测试文件）

| CE | 独立结果（本冻结） | 作者测试是否锁住 |
|---|---|---|
| **合取 sham 锁必须拒绝四类伪造；旧弱析取仍绿 0.0/空事件** | **断言闭 + 实现闭。** 抄出 `_scientific_sham_lock`（不 import）：顶层任一 excess/noise 非 None → False；`events=[]` → False；事件 `rho_M_excess=1.0` 即使 `null_reason=noise_set_missing` → False；事件 `null_reason` 缺/None → False。诚实行 True。旧 `!= 1.0 or null_reason`：`rho_M_excess=0.0` True；`events=[]`（顶层仍 None）True。活体 scientific prepare 密度同样：锁 True；四种伪造 False；弱锁对 0.0/空事件仍 True。全 `tests/**` 检索：弱析取只剩作者 L273 的对照 `weak = lambda`。单元五例都是合取，不是 `is None or null_reason`。 | 作者 `test_scientific_sham_does_not_book_rho_m_excess_one` 用合取锁关真实密度并 `assert not` 四伪造，另用弱锁证明旧关闭条件仍绿。**不是**只靠弱析取关闭。若只靠弱析取关闭，本通道会 **FAIL**——**没有。** |
| **F19-06：省略四条 §8 或 `refused+score=1.0` 必须让作者断言红** | **断言闭。** 从 `test_round06` L60–64 **抄出**（不 import）：`needed` 四元集合、`section8` 过滤、`{baseline}==needed`、`status==refused_not_section8`、`score is None`。对 `[]` → False；省略一行 → False；四行皆 `score=1.0` → False；四行中一行 `score=1.0` → False。活体 scientific `probes.jsonl`：四行 `refused_not_section8`、score 全 `None`；剥掉四行或把 score 改成 1.0 → 作者断言失败。旧过滤 `all(... if baseline in S)`：`[]` → True，省略行 → True。**不当作充分。** | 作者断言锁存在性 + 无 score。独立同意。 |
| **intervene 不得静默 cap=64；70 ok；>96 raise。不以 `prefix_truncated is not True` 为充分** | **实现闭 + 作者 CLI 锁闭。** helper：`len(_tiny_prefix_ids("x"*70))==70`；`"x"*97` raise。源码无 `ids[:64]`。CLI 70 字 scientific 题干：独立间谍 `intervene_hidden_decode` 五次皆 **79 ids**，`any(n<=64)=False`，`prefix_n=79`。抄出的作者断言对 `seen=[64]` / `[79,64]` / `[]` → False；对真实 `[79×5]` → True。旧替身 `prefix_truncated is not True` 对 `{False, n_ids:64}` 与 `{}` **仍绿**——**不接受为充分**。traces 前缀垫到 100 字后 CLI **raise** `refuse truncated prefixes`。实现 L959 仍写死 `prefix_truncated=False`。 | 作者 `test_intervene_cli_hook_ids_exceed_64` 间谍 hook 并锁 `all(n > 64)` 与 `prefix_n`。helper 70/97 **仍在**（附加，不是唯一锁）。 |
| **calibrate / `_find_labels_jsonl` 不得绑兄 `lab`。不以 `inspect.getsource` 为充分** | **实现闭 + 作者 CLI 锁闭。** `_find_labels_jsonl(feat)` 在兄 `lab` 有 `labels.jsonl` 时仍 `None`。独立 `cmd_calibrate`：有兄 `lab/WRONG` 时 finder 实参 `(None, fit, feat)`，**未传入兄路径**。有/无兄目录写出 **同一** toy `scores`（约 `0.0050235`）。`label_dirs.extend` / `parent / "lab"` / `joinpath("lab")` 不在 `cmd_calibrate` 源码。作者套件 **无** `inspect.getsource(cmd_calibrate)`。 | 作者 `test_calibrate_cli_ignores_sibling_lab` 实跑 CLI、wrap finder、断言兄路径不在实参、比 `calibration.jsonl`。helper `_find_labels_jsonl` 仍在（附加）。 |
| **`card` / `forbid_host_exec` / Procrustes / `attention_mean` / `apply_model_template`** | **独立闭。** `card("qwen3-8b")["hidden_size"]==4096`；`card("r1-distill-qwen-7b")==3584`；未知名 `KeyError`；revision ≠ `latest`。`forbid_host_exec(boom)()` 抛 `host execution` 且 `called==[]`。独立 90°：`source=[[2,0],[0,3],[1,2],[4,1]]`，`R=[[0,-1],[1,0]]`，`source @ R` 恢复且 `apply_map` 一致。`attention_mean([[0.05,0.80,0.10,0.05]], [1])==0.80`；`[0,2]==0.075`。tokenizer kwargs：`qwen3` 有 `enable_thinking=False`；`qwen2` / `r1-distill-qwen-7b` **无**该键。 | 作者五例锁同类合同。本通道用独立权重/矩阵/第三种 model_kind，不当作者例当 oracle。 |
| **`stage_a` / `stage_b` 配对仍工作** | **闭。** 有 copy：`donor_kind=same_value_diff_source`。兄 `prep` 不救命。删 `stage_b/edits.jsonl` → `same_identity_fallback`。 | 作者 `stage_a`/`stage_b` 不删 copy。 |
| **`apply_rename_edit({p1:p2,p2:p1})` 不得变 `p1 * p1`** | **实现闭。** 题干 `p2 = 4. p1 = 0. What is q = p2 * p1?`。顺序 `str.replace` 对照是 `p1 = 4. p1 = 0. What is q = p1 * p1?`。 | 作者 swap 例锁同一题干。**不当 oracle。** |
| **自然 CoT / MODEL-01 / offline H / `constrained_target`** | **不要求，不开缺陷。** 活体 scientific prepare 7 条轨迹皆 `parse_status=constrained_target`。 | 测试不要求 §4.1 或 MODEL-01。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **`rho_M_excess != 1.0 or null_reason`** | `None != 1.0` 与 `0.0` 单独过；空 `events` 因不看事件也过。作者 **不再** 只用它关闭科学 sham。独立确认它对 0.0/空事件仍绿。 |
| **`is None or null_reason`** | **本冻结作者单元 sham 已不用。** 现为 excess/noise 皆 None **且** `null_reason == noise_set_missing`。 |
| **`all(status==refused_not_section8 for row if baseline in S)`** | 仍对 `[]` 与省略行恒真。作者 **不再** 只用它。新断言有 `{baseline}==needed` 与 `score is None`。独立突变确认省略行 / 骑 score 会红。 |
| **`prefix_truncated is not True`** | 缺字段、硬编码 `False`、静默 `ids[:64]` 都绿。实现 L959 写死 False。**本通道不接受为充分。** 作者现另锁 hook `n>64` 与 `prefix_n`。独立间谍确认 79。 |
| **`inspect.getsource(cmd_calibrate)`** | **本冻结作者已不用。** |
| **`_tiny_prefix_ids` / `_find_labels_jsonl` helper** | helper 绿不能单独证明 CLI。本冻结另有 CLI 例。helper 仍在，只作附加。 |
| **`start>=len(prompt)`** | 若 `prompt_text` 被截，事件仍可在截断后。r07 全题干补了 alt-source；70/97 作者不锁 generate CLI。 |
| **`prep`/`col` 目录名** | 复制 edits 后不再必要。删 col 的 edits 后 fallback。 |
| **教员强制 `q=`** | 科学事件 `any(q)` 仍可被强制行单独满足。**不**开成自然 CoT 缺陷。 |
| **offline H 当 e2e** | 八段 exit 0。`H`←`token_ids[:8]`。analyze 无 P1 表。smoke **要求**空结论。**诚实项。** |
| `timing != "pre_step"` | 任意其他字符串都绿。 |
| `test_plus_locks_*` | 同进程 RAM clear。**不**新进程。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| pytest / CE 后 persist 泄漏 | 172 passed 与独立 CE 之后磁盘为 `["gsm8k-12", "q:ada has 4 apples…"]`。该文件不在 61 摘要内。**卫生，不是冻结哈希缺陷。** |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：页眉写 pytest 不得关可执行行；历史单元格仍有 `python -m pytest -q`（协议行 69 处提及）+ `passed_local_tests`。页眉把这些写成「曾跑过套件，不是协议行关闭证据」。本冻结 **没有** 新声称「协议行仅由 pytest 关闭」（`newly_closed_by_pytest_only=0`）。按任务口径 **不** 因此 FAIL。 |
| scientific calibrate | 对 tiny 探针写出有限非conformity 分数（约 `0.0050235`）。不是论文校准。有/无兄 `lab` 分数相同。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-23 通道报告；r22 A–F 当证据 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 `_f_scratch` 与 §8 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| Plus persist 新解释器 | 本通道只确认套件后磁盘仍有 Plus 键；作者也不 spawn。卫生，不是缺陷。 |
| 把 Goal 标 Complete | 本通道只评验证质量 |
| 把 offline H / `constrained_target` / fixture echo 开成缺陷 | 任务明确：除非作者把它们写成科学结果。不要求自然 CoT 或 MODEL-01。 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 172 passed | `VERSION.md` | **命令是。** 当作 Goal：**否。** |
| 科学 sham 合取锁拒绝 0.0 / 空 events / 账面 1.0 / 缺 `null_reason`；旧弱析取不再单独关闭 | ISSUES / 作者测试 | **独立同意。** 抄出锁对四伪造失败；弱锁对 0.0/空事件仍绿；作者关闭条件是合取锁。单元 sham 合取。 |
| F20-01 intervene CLI 间谍：70 字题干 hook `prompt_ids` 长度 >64，并写 `prefix_n` | 作者测试 | **独立同意。** 独立间谍五次皆 79。不以 `prefix_truncated is not True` 为充分。 |
| F20-02 `cmd_calibrate` 实跑：兄 `lab` 不在 finder 参数里；有/无兄输出相同 | 作者测试 | **独立同意。** 独立 spy 实参 `(None, fit, feat)`；输出相同。不以 `inspect.getsource` 为充分。 |
| F19-06 scientific fit 断言要求四条 §8 存在、`refused_not_section8`、无 `score` | 作者测试 | **独立同意。** 省略行与 `score=1.0` 会红。旧 `all(... if baseline in S)` **不是**充分条件。 |
| `card` 4096/3584；`forbid_host_exec`；Procrustes 90°；`attention_mean` 下标；template 只对 qwen3 传 thinking | 作者测试 | **独立同意**（独立数字/第三种 kind）。 |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` | **本套件不能作证 Goal 完成。** 本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**本冻结点名攻击：**

- **科学 sham 锁必须合取，且拒绝 0.0 / 空事件 / 账面 1.0 / 缺 `null_reason`。** 抄出锁对四种伪造失败。旧弱析取对 0.0 与空事件仍绿——**不**当作关闭条件。作者关闭条件是 `_scientific_sham_lock`。**若作者仍只用弱析取关闭，本通道会 FAIL——没有。**
- **单元 sham 必须合取。** 五例：`test_sham_hits_do_not_broadcast_*`、`test_sham_no_change_*`、`test_observed_real_noise_ref_without_sham_*`、`test_sham_hits_do_not_book_evaluated_zero_noise`、`test_evaluated_zero_hit_sham_*` 都是 excess/noise 皆 None **且** `null_reason == noise_set_missing`，无 `is None or`。
- **scientific fit 断言必须因省略四行或 `score=1.0` 而红。** 抄出的作者断言对这两种突变失败。旧 `all(... if baseline in S)` 仍空真——**不**当作关闭条件。
- **intervene 前缀必须完整或显式拒。不以 `prefix_truncated is not True` 为充分。** 独立间谍五次 79；`any(n<=64)=False`。100 字前缀必须 raise。
- **calibrate 不得读兄 `lab`。不以 `inspect.getsource` 为充分。** 独立 CLI spy：finder 未收兄路径；有/无兄输出相等。
- **`card` 4096/3584；`forbid_host_exec` 不调用；Procrustes 恢复已知 90°；`attention_mean` 用前提下标；thinking 只传给 qwen3。** 独立数字与 spy 闭。
- **重叠 rename 必须同时替换。** 回到顺序 `replace` 会让独立 CE 红（`p1 * p1`）。
- **配对不得靠兄目录名 `prep`。** 删 copy 后 fallback。
- **自然 CoT / MODEL-01。** 不要求。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_tiny_prefix_ids_refuse_silent_truncate` | 只调 helper。不经 `cmd_intervene`。本冻结另有 CLI 间谍例；本 helper **不是**关闭条件。 |
| `prefix_truncated is not True`（旧锁） | 对 `{False, n_ids:64}` 与缺字段为真。**本通道不接受。** 作者已不再只用它。 |
| `inspect.getsource(cmd_calibrate)`（旧锁） | **本冻结已不在。** |
| `test_calibrate_does_not_bind_sibling_lab_labels` | 只调 `_find_labels_jsonl`。本冻结另有 CLI 例；本 helper **不是**关闭条件。 |
| `weak = lambda d: d.get("rho_M_excess") != 1.0 or d.get("null_reason")` | 作者故意保留以证明旧锁仍绿。**若只靠它关闭科学 sham，本通道会 FAIL。** 作者现不靠它关闭。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 §8 断言 | **锁存在性+无 score。** 独立突变确认省略/`score=1.0` 会红。本通道不把它当唯一证明。 |
| `test_generated_events_exclude_prompt_assignments` | 只锁 `start>=len(prompt)`。截断 `prompt_text` 仍绿。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 `donor_kind` | 目录名 `prep`/`col`。现在靠 copy 也能绿。不删 edits。 |
| `test_rename_swap_is_simultaneous` | 锁对了实现合同。本通道不把它当证明；独立 CE 另核。 |
| `test_plus_locks_symbolic_family_to_test` | 不 spawn。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。诚实，不是 MODEL-01。 |
| `test_p1_held_out_logistic_detects_rho` | `ρ=y` 在全部行。`monkeypatch` 未用。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。作者已承认——**不要超售成科学 e2e。** 按任务口径 **不** 开成缺陷。
2. **科学 sham 已不再用弱析取盖住「未账面 0.0/1.0」。** 合取锁拒绝四伪造。独立突变确认。
3. **F19-06 已不再用空真 `all` 盖住「必须存在且无 echo 分」。** 集合相等与 `score is None` 仍在。
4. **intervene 70：作者现间谍 hook ids，不再只用 `prefix_truncated is not True`。** helper 70/97 仍在，但是附加。实现仍写死 `prefix_truncated=False`。
5. **calibrate 兄 `lab`：作者现跑 `cmd_calibrate` 并查 finder 实参，不再用 `getsource`。** helper 仍在，但是附加。
6. **科学事件非空，来源仍是教员强制 `q=`。** **不**要求自然 CoT。
7. **套件把 Plus 键写进仓库缓存且多数用例不 `clear`。** 卫生。
8. **账本历史单元格仍 pytest。** 页眉已声明不得关可执行行。

**作者测试现已点名的符号：** `card`、`forbid_host_exec`、Procrustes 恢复、`attention_mean` 数值、`apply_model_template`。本通道独立重核。**仍无作者测试：** `score_qa`、`assert_disjoint`——本通道独立补了，**不是**套件锁，也 **不** 因此 FAIL（不在点名失败条件里）。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加生产测试。脚本：`_f_scratch/f23_ce.py`。

### CE-1 合取 sham 锁必须拒绝四伪造；弱锁仍绿 0.0/空事件（闭）

```text
copied _scientific_sham_lock (test_round07 L244-257, not imported):
  top-level excess AND noise all None
  events nonempty
  every event: excess AND noise all None AND null_reason == noise_set_missing

honest (all None + noise_set_missing + 1 event) → True
rho_M_excess=0.0, no null_reason override                 → False
events=[]                                                 → False
booked rho_M_excess=1.0 even if null_reason set           → False
event null_reason missing / None                          → False

live scientific dens: lock True; same four forgeries False

old weak (rho_M_excess != 1.0 or null_reason):
  rho_M_excess=0.0 → True    # still greens
  events=[]        → True    # still greens

author close: assert _scientific_sham_lock(dens)
              assert not lock(four forgeries)
              weak used only as negative control
only_weak_as_close = False

unit sham (5 fns): conjunctive; no `is None or`
```

### CE-2 intervene 前缀：独立间谍 hook ids；不以 flag 为充分（闭）

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
```

### CE-3 calibrate 不绑兄 `lab`：实跑 CLI；不以 getsource 为充分（闭）

```text
_find_labels_jsonl(feat) is None
  even if sibling lab/ has labels.jsonl

cmd_calibrate(--in-dir fit, --features-dir feat) with sibling lab/WRONG:
  _find_labels_jsonl dirs == [None, fit, feat]
  finder_passed_sibling == False
  calibration.jsonl == same run without sibling lab/
  scores ≈ [0.0050236, 0.0050236, 0.0050235, 0.0050236]

inspect.getsource ABSENT
```

### CE-4 §8 作者断言必须因省略行或 `score=1.0` 而红（闭）

```text
author assertion (copied from test_round06 L60-64, not imported):
  needed = {verbalizer, attention_mean, attention_rollout, attention_threshold}
  section8 = [row for row in probes if baseline in needed]
  {baseline} == needed
  all(status == refused_not_section8)
  all(score is None)

[]                                          → False
omit one                                    → False
four refused + score=1.0                    → False
four refused, one score=1.0                 → False
real scientific probes                      → True
same probes with §8 rows stripped           → False
same probes with score=1.0 written on §8    → False

vacuous all(... if baseline in S):
  [] / omit one → True   # not sufficient
```

### CE-5 点名 oracle（闭）

```text
card("qwen3-8b").hidden_size == 4096
card("r1-distill-qwen-7b").hidden_size == 3584
card("not-a-registered-model") raises KeyError
revisions != "latest" and unequal

forbid_host_exec(boom)() raises "host execution"; called == []

procrustes([[2,0],[0,3],[1,2],[4,1]], that @ 90°)
  R ≈ [[0,-1],[1,0]]; apply_map recovers

attention_mean([[0.05,0.80,0.10,0.05]], [1]) == 0.80
attention_mean(..., [0,2]) == 0.075
empty weights or empty idx → 0.0

apply_model_template(..., "qwen3", enable_thinking=False):
  tokenizer kwargs has enable_thinking=False
apply_model_template(..., "qwen2" / "r1-distill-qwen-7b", True):
  enable_thinking NOT in tokenizer kwargs
```

### CE-6 配对 / rename（闭）

```text
apply_rename_edit({p1:p2, p2:p1}):
  question == "p2 = 4. p1 = 0. What is q = p2 * p1?"
sequential str.replace would be:
  "p1 = 4. p1 = 0. What is q = p1 * p1?"

_load_source_value_pair(features_only) is None
  even if sibling prep has edits.jsonl

stage_a / stage_b (copy): donor_kind == same_value_diff_source
unlink(stage_b/edits.jsonl): donor_kind == same_identity_fallback
```

## 9. 发现

### F23-00 开审与交卷哈希可复算且一致

- **严重度：** —
- **状态：** HASH_MATCH（过程通过）
- **文件：** `.planning/audits/round-23/VERSION.md` L5–23；61 = `1f5f3798…19c7bcdb`；0 CRLF
- **复现：** 脚本原文开审与交卷同一摘要。HASH_MISMATCH 会 FAIL 本通道——**没有。**

### F23-01 绿 172 不是 Goal / QA 验收

- **严重度：** —（验证口径；站立残留，不是本通道缺陷）
- **状态：** non-defect（任务与 ISSUES 站立残留：绿 pytest ≠ Goal）
- **复现：** `172 passed / 0 / 24.30s`，172 collected。作者主张与命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 仍是 offline 烟测。**不**把绿 pytest 写成 Goal 通过，也 **不** 因此 FAIL 本通道。

### F23-02 科学 sham / 噪声合取锁（点名闭）

- **严重度：** —
- **状态：** 实现闭合 + 作者测试闭合（独立抄锁 + 活体密度）
- **文件：** `tests/test_round07_regressions.py` L244–277；单元 sham 在 r04/r06/r07
- **复现：** 抄出锁：诚实 True；`0.0` / `[]` / 账面 1.0+reason / 缺 `null_reason` 皆 False。弱锁对 `0.0` 与 `[]` 仍 True。活体 scientific dens：`rho_M_excess is None`，1 个事件，`null_reason=noise_set_missing`。作者 `assert _scientific_sham_lock(dens)` 且 `assert not` 四伪造；`only_weak_as_close=False`。单元五例合取。全测试检索弱析取只剩对照 `weak = lambda`。
- **若作者仍只用 `!= 1.0 or null_reason` 关闭科学 sham，本条会 FAIL 通道——没有。**

### F23-03 70 字 CLI intervene hook ids >64（点名闭）

- **严重度：** —
- **状态：** 实现闭合 + 作者 CLI 测试闭合（独立间谍，不以 flag 为充分）
- **复现：** 独立间谍 ids 全是 79；`any(n<=64)=False`；`prefix_n=79`。100 字前缀 raise `refuse truncated prefixes`。无 `ids[:64]`。旧 `prefix_truncated is not True` 对静默 cap **仍绿**——记下但不当作关闭条件。

### F23-04 `cmd_calibrate` 不绑兄 `lab`（点名闭）

- **严重度：** —
- **状态：** 实现闭合 + 作者 CLI 测试闭合（实跑，不以 getsource 为充分）
- **复现：** 独立 wrap：有兄 `lab/WRONG` 时 dirs=`[None, fit, feat]`，`finder_passed_sibling=False`。有/无兄 `calibration.jsonl` 全等，scores 约 `0.0050235`。作者套件无 `inspect.getsource(cmd_calibrate)`。

### F23-05 scientific-fit §8 断言因省略行或 `score=1.0` 而红（点名闭）

- **严重度：** —
- **状态：** 测试设计闭合（独立突变）。实现仍写四条 refused 且无 score。
- **复现：** 抄出的作者断言：`author_fit([]) is False`；省略一行 False；四行或一行 `score=1.0` False。真实 probes 上剥行或写分同样 False。旧 `all(... if baseline in S)` 对这两种输入仍 True——**不**当作充分。

### F23-06 点名 oracle：card / forbid / Procrustes / attention_mean / template（点名闭）

- **严重度：** —
- **状态：** 实现闭合（独立数字与 spy）
- **复现：** 见 §8 CE-5。作者有同名例；本通道用独立 90° 矩阵、独立权重、第三种 `r1-distill-qwen-7b` kind。

### F23-07 Fixture e2e 仍 offline；scientific tiny 仍 `constrained_target` — 诚实项，不开缺陷

- **严重度：** —
- **状态：** non-defect（验证口径）
- **注：** 任务：八段是 offline 前缀 H；约束 `\nq=` 不是 §4.1；tiny 不是 MODEL-01。活体 7 条轨迹皆 `constrained_target`。本通道 **不** 把它们写成已确认遗留缺陷，也 **不** 把 smoke 写成科学 e2e。

### F23-08 Plus persist：套件泄漏缓存 — 卫生，不是冻结哈希缺陷

- **严重度：** —
- **状态：** non-defect（任务明确）
- **复现：** pytest 与独立 CE 后 `.planning/research/.cache/gsm_test_only_families.json` 仍有 `gsm8k-12` 与问题键。不在 61 摘要内。

### F23-09 账本历史单元格仍提及 pytest — 不是本通道 FAIL

- **严重度：** —
- **状态：** non-defect（任务明确：页眉已声明 pytest 不得关可执行行）
- **复现：** 页眉 r22 行：`pytest` **仍不得**关闭可执行行；历史单元格只表示曾跑过套件。协议行 69 处仍写 `python -m pytest -q`。`newly_closed_by_pytest_only=0`。若本冻结**新**声称「协议行仅由 pytest 关闭」，本条会 FAIL——**没有。**

### F23-10 夹具排除在冻结外 — 协议，不是缺陷

- **严重度：** —
- **状态：** non-defect（任务明确）

### F23-11 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq=` **不是** pending_server。已闭的 hook/calibrate/sham/oracle 锁 **不是** pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。通道通过 ≠ 这些条件已满足。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **本套件不能单独支撑 Goal。** 页眉已声明 pytest 不得关可执行行；历史单元格仍写 pytest。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道未确认新的范围内缺陷。** 点名 sham / CLI / §8 / oracle **已闭**。这不是全量 A–F 结论。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，Goal 实质仍失败。** `pytest -q` 确为 172/0。e2e 是 offline 烟测。点名 CE 级锁 + 独立间谍已跑。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂，但本通道不因此 FAIL。** REQUIREMENTS 复选框仍未勾。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **本通道 PASS，不宣布 Goal。** 哈希匹配。连续通过由全量 A–F 共同计数；Channel PASS 不是 Goal 验收。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里。offline H / `constrained_target` 按诚实项列出即可。已闭的锁 **不要** 再标 pending_server。 |
| 7 | 交付包 | **问题闭环未就绪到 Goal 句。** pytest 记录存在（172/0）。点名 CE 有独立记录。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行（诚实）。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、alt-source 图有。重叠 rename **实现闭**。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`（诚实）。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | `noise_ref=0` / 未知 \(M\) / sham missing 独立见。合取锁现为关闭条件。 |
| 5 划分 | 测试专用不进拟合 | Plus→test、family persist 有。跨进程无测试。`assert_disjoint` 作者无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。intervene 长前缀 **实现拒截**；作者现锁 hook `n>64`。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。scientific 拒 §8 **实现有、作者存在性+无 score 仍闭**。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。scientific calibrate 出玩具有限 \(q\)；兄 `lab` 实现不绑；作者现跑 CLI。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。Procrustes 数值恢复现有作者+独立锁。`card` 4096/3584 有。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。配对不靠 `prep` 名。offline e2e 是 `unexpressible`。长前缀实现闭；70 字 hook ids 作者+独立闭。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。Gate 未注册不是缺陷。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` + `forbid_host_exec` 已锁。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **172 passed，exit 0，24.30s，172 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH `1f5f3798…19c7bcdb`（61，开审=交卷）。** |
| 独立性 | **独立闭：** 合取 sham 锁对四伪造失败、弱锁对 0.0/空事件仍绿且作者不用它关闭、单元 sham 合取、§8 断言对省略行与 `score=1.0` 失败、CLI intervene 79 ids / 无一 ≤64 / >96 raise、calibrate CLI 不绑兄 `lab`、`card` 4096/3584、`forbid_host_exec` 不调用、Procrustes 90°、`attention_mean` 下标、template 只对 qwen3 传 thinking、重叠 rename、`stage_a`/`stage_b` 与删 copy。**独立红：无。** **诚实非缺陷：** offline 前缀 H、`constrained_target`、fixture echo verbalizer、Plus persist 卫生、夹具不进冻结、账本历史 pytest 字样。 |
| Mock/stub | offline 前缀 H + 教员强制 `q=` + `start>=` + 同进程 persist。**不再**用弱析取 / `prefix_truncated is not True` / `getsource` 冒充关闭条件。 |
| 论文行为仍未证明 | 真 Prefill KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT（**未要求**） |
| 交付 vs 测试 | 「172 passed / 合取 sham / CLI 70 / calibrate 兄 lab / §8 / 点名 oracle」在**点名合同**上与独立 CE 一致。绿 172 **仍超过** Goal 验收。 |
| 已确认范围内缺陷？ | **无。** |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Pass。** 哈希匹配。点名攻击按任务口径已闭。绿 pytest 不是验收。Channel PASS 不是 Goal 验收。 |
| 停止条件第 5 条 | **本通道不独自开始或结束连续通过。** 哈希匹配。本通道无新确认范围内缺陷。连续通过须全量独立 A–F 在同一 hash 上均无新确认缺陷；只补本文件不改变被审摘要。 |

点名重攻按任务口径已闭：合取 `_scientific_sham_lock` 拒绝 `rho_M_excess=0.0`、空 `events`、借口下账面 1.0、缺 `null_reason`；旧弱锁对 0.0 与空事件仍绿，且作者不再只用它关闭；单元 sham 是合取不是 `is None or`；独立间谍 `intervene_hidden_decode` 的 `prompt_ids` 无一 `len<=64`；独立 `cmd_calibrate` 有/无兄 `lab/WRONG` 输出相同且 finder 未收兄路径；作者 §8 断言在省略四行或 `refused+score=1.0` 时失败；`card` / `forbid_host_exec` / Procrustes / `attention_mean` / `apply_model_template` 独立数字与 spy 闭。**不**接受 `prefix_truncated is not True` 或 `inspect.getsource` 作为充分条件。offline 前缀 H 与 `constrained_target` 按诚实项保留，不在此要求 MODEL-01 或自然 CoT。夹具不进冻结是协议。Plus persist 残留是卫生。历史账本 pytest 字样不是本通道 FAIL。通道通过 **不是** Goal 验收，也 **不** 宣布 Goal 完成。
