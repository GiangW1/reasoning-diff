# F：验证质量与反向质疑（round-22）

独立审查通道 F。未改 `src/`、`tests/`、`pyproject.toml`。未读 round-22 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 写在 `.planning/audits/round-22/_f_scratch/`，不把 `tests/test_round06_regressions.py` / `tests/test_round07_regressions.py` 当证明（只抄断言原文）。

**先行结论：** 按 `VERSION.md` 原文复算，开审与交卷冻结哈希 **一致（HASH_MATCH）** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（61 文件，0 CRLF）。本机 `python -m pytest -q --tb=line` 为 **172 passed / exit 0 / 30.27s**，与作者 `pytest_author_claim: 172` 一致。这不是 Goal 通过。相对 r21，生产 42 个 `src/**/*.py` 摘要未变；变的是 `tests/test_round04_regressions.py`（319 / `dd541f91…`）、`tests/test_round06_regressions.py`（156 / `b9bece3e…`）、`tests/test_round07_regressions.py`（562 / `9ab6c6f6…`）、`tests/test_tiny_hooks.py`（24 / `a829677e…`）。

独立 CE（26 条，不 import r06/r07 测试模块）：**F21-08 合取 sham 锁已闭。** 抄出的 `_scientific_sham_lock` 在 `rho_M_excess=0.0`、`events=[]`、借口下账面 `1.0`、事件缺 `null_reason` 上失败；旧弱锁 `rho_M_excess != 1.0 or null_reason` 对 `0.0` 与空事件仍绿。作者科学 sham 关闭条件是合取锁，**不是**只靠该弱析取。单元 sham 断言是 excess/noise 皆 `None` **且** `null_reason == noise_set_missing`。**F20 点名重攻仍闭：** 70 字 CLI intervene 独立间谍五次 `prompt_ids` 皆 **79**，**无一 ≤64**；`cmd_calibrate` 有兄 `lab/WRONG` 与无兄：finder 实参 `(None, fit, feat)`，**未传入兄路径**，`calibration.jsonl` **相同**。不以 `prefix_truncated is not True` / `inspect.getsource` 为充分。**F19-06 仍闭：** 抄出的 §8 断言在省略四行或 `refused+score=1.0` 时失败。**点名 oracle 独立闭：** `card` 4096/3584；`forbid_host_exec` 不调用被包函数；Procrustes 恢复已知 90°；`attention_mean` 用前提下标（独立权重 `[0.05,0.80,0.10,0.05]`）；`apply_model_template` 只对 `qwen3` 把 `enable_thinking` 传给 tokenizer。Fixture 八段仍 offline 前缀 H；scientific tiny 仍 `constrained_target`——按任务口径这是诚实项，**不**开成缺陷，也 **不** 当 MODEL-01 / 自然 CoT。账本页眉写 pytest 不得关可执行行；本冻结 **没有** 新声称「协议行仅由 pytest 关闭」——**不**因此 FAIL F21-11。Plus persist 残留是测试卫生，不是冻结哈希缺陷。本通道 **通过**。**不宣布 Goal 完成。** 通道通过不是 Goal 验收。r21 A–E PASS 不转移到本树。停止条件第 5 条：连续通过仍须在 **本哈希** 上独立重做 A–E；本通道不再用 F21-08 阻断。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21 03:40–04:25（Asia/Shanghai） |
| 声明冻结 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` |
| 开审复算 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` |
| 交卷裁决 | **HASH_MATCH**（与声明同一摘要） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明 / 开审 / 交卷都是 **61**。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| pytest | **172 passed in 30.27s，exit 0。** Collect：**172 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 172 passed`。命令结果独立确认。当作 Goal / 阶段验收：**否。** |
| 范围 | 61 冻结文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**（协议，不是缺陷）。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。 |
| 明确未读 | `.planning/audits/round-22/{A,B,C,D,E}-*.md` |
| 独立 CE | `.planning/audits/round-22/_f_scratch/f22_ce.py` → `f22_ce_results.json`（26 条：26 闭 / 0 红）。未 import r06/r07 测试模块。首次 `attention_mean` 红是独立权重与全 token 均值撞数，不是实现红；改用可区分权重后闭。 |

审查对象是**声明冻结字节**。pytest 与点名 CE 均在 HASH_MATCH 盘上执行。交卷哈希未漂。相对 r21 冻结 `5097c831…`，本树生产文件摘要未变；测试侧 `test_round04` / `test_round06` / `test_round07` / `test_tiny_hooks` 变了。`cli.py` 仍是 1268 / `cc5eae53…`。

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
| `tests/test_round06_regressions.py` | 156 | `b9bece3ea0bc90cd…` | `start>=len(prompt)`；`prep`/`col` 上 `donor_kind`；scientific fit **集合相等四条 §8 + refused + `score is None`**（F19-06 仍锁）；sham **合取** excess/noise None + `null_reason` |
| `tests/test_round07_regressions.py` | 562 | `9ab6c6f669dc250d…` | r07 节点 + swap 题干；`_tiny_prefix_ids` helper 70/97；CLI intervene 间谍 `all(n > 64)` + `prefix_n`；`cmd_calibrate` 实跑 finder 不含兄 `lab`；**`_scientific_sham_lock` 合取 + 四伪造必须失败**；单元 sham 合取；**`card` / `forbid_host_exec` / Procrustes / `attention_mean` / `apply_model_template` oracle** |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer 形状、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 24 | `a829677e50795d36…` | hook 清理；r21 L17 恒真 **已不在** |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle。按任务：协议，不是缺陷。 |

Collect-only：**172 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。相对 r21（167）：+5 即五条点名 oracle。`test_tiny_hooks` 不再有 `assert layer.__class__.forward`。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。旧 `prefix_truncated is not True` 对 `{False, n_ids:64}` 仍绿——**本通道不接受它为充分**。作者套件 **无** `inspect.getsource(cmd_calibrate)`。弱析取 `rho_M_excess != 1.0 or null_reason` **只**出现在作者用来证明旧锁仍绿的 `weak = lambda`（L273），**不是**科学 sham 关闭条件。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8、**Procrustes 90° 恢复** | `ρ=y` 泄漏仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed；**`attention_mean` 下标** | fixture CLI **echo 前缀**无测试红（诚实项）；`attention_rollout` 作者仍无数值 oracle |
| `cli.py` | 1268 | `cc5eae53d7be27eb…` | smoke offline；scientific prepare/collect/fit/intervene；孤立 fit 拒；collect 复制 edits；CLI 70 间谍 hook ids；calibrate 实跑 finder | `cmd_intervene` 仍硬编码 `prefix_truncated=False`（L959），另写 `prefix_n`（L960） |
| `edits.py` | 367 | `cc8e2d23592a3ab8…` | value/alt-source 图；rename `{p1:alpha}`；swap 例 | 三前提集合碰撞仍非作者指纹 |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False`；**`forbid_host_exec` 不调用被包函数** | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP/范数 | `ie_z` helper 仍是均值差 |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 405 | `985b9d9328e4111f…` | 未知 \(M\)；`noise_ref=0` 手造；unit 噪声扣除 | C7 helper 不走 labels |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **`card` 4096/3584 + 未知 KeyError** | `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 200 | `6e6040394ac641c7…` | 全题干 + `>96` 拒；**`apply_model_template` 仅 qwen3 传 thinking** | 返回字典对非 qwen3 仍带 `enable_thinking` 键（kwargs 不含） |
| `models/tiny.py` | 120 | `c75d0f5325766612…` | hook 清理 + logits 变 | — |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | 一字一 token |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | — |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | `_hidden_is_prefill` 拒标量/`bool`/`[0]` | `[0.0,1.0]` 仍 True（合法向量） |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` 作者仍零测试 |
| `splits.py` | 184 | `40ab4021d4dccc6e…` | Plus→test；RAM∪磁盘 | `assert_disjoint` 作者仍零测试 |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | — |
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
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584 拒；`n<d` truncated | — |

夹具 JSON **不在冻结内**（协议）。`models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 仅包说明。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `1f5f3798…9c7bcdb`（61，0 CRLF） |
| 交卷再算 | 同脚本 | **HASH_MATCH** 同一摘要 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **172 passed in 30.27s，exit 0**。无 skip/xfail/deselected |
| Collect | `python -m pytest tests --collect-only -q` | 172 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对冻结 `tests/**` 检索 | 无 skip/xfail/mock；`assert True` 只在载荷字符串；未用 `monkeypatch` 一处 |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；顺序 swap 应变 `p2 * p1`；70/97 token；4096/3584；90° R | **存在的单元断言**与独立算术一致；swap/70/97/点名 oracle 另由独立 CE 核 |
| **独立 CE** | `_f_scratch/f22_ce.py`（`PYTHONPATH=src`） | 26 条：26 闭 / 0 红。见 §3.1。 |

### 3.1 点名独立 CE（不信测试文件）

| CE | 独立结果（本冻结） | 作者测试是否锁住 |
|---|---|---|
| **F21-08：合取 sham 锁必须拒绝四类伪造；旧弱析取仍绿 0.0/空事件** | **断言闭 + 实现闭。** 抄出 `_scientific_sham_lock`（不 import）：顶层任一 excess/noise 非 None → False；`events=[]` → False；事件 `rho_M_excess=1.0` 即使 `null_reason=noise_set_missing` → False；事件 `null_reason` 缺/None → False。诚实行 True。旧 `!= 1.0 or null_reason`：`rho_M_excess=0.0` True；`events=[]`（顶层仍 None）True。真实 scientific prepare 密度同样：锁 True；四种伪造 False；弱锁对 0.0/空事件仍 True。全 `tests/**` 检索：弱析取只剩作者 L273 的对照 `weak = lambda`。单元三例 + r06 sham + r04 零 hit 事件行都是合取，不是 `is None or null_reason`。 | 作者 `test_scientific_sham_does_not_book_rho_m_excess_one` 用合取锁关真实密度并 `assert not` 四伪造，另用弱锁证明旧关闭条件仍绿。**不是**只靠弱析取关闭。 |
| **F19-06：省略四条 §8 或 `refused+score=1.0` 必须让作者断言红** | **断言闭。** 从 `test_round06` L60–64 **抄出**：`needed` 四元集合、`section8` 过滤、`{baseline}==needed`、`status==refused_not_section8`、`score is None`。对 `[]` → False；省略 `verbalizer` → False；四行皆 `score=1.0` → False；四行中一行 `score=1.0` → False。对真实 scientific `probes.jsonl`：删掉四行或把 score 改成 1.0 → 作者断言失败。旧过滤 `all(... if baseline in S)`：`[]` → True，`{verbalizer,refused,score=1.0}` → True。**不当作充分。** | 作者断言锁存在性 + 无 score。独立同意。 |
| **scientific fit 必须写出四行 refused 且无分** | **实现闭。** 四条 `baseline∈{verbalizer,attention_mean,attention_rollout,attention_threshold}`，皆 `refused_not_section8`，`score is None`。echo `generate_fn=λp.prefix` 在同一科学前缀上 `status=generated`，`score=1.0`，抽出 `82`。 | 作者读 `probes.jsonl` 并锁集合/status/score。本通道不靠该例当 oracle。 |
| **intervene 不得静默 cap=64；70 ok。不以 `prefix_truncated is not True` 为充分** | **实现闭 + 作者 CLI 锁闭。** helper：`len(_tiny_prefix_ids("x"*70))==70`；`"x"*97` raise。源码无 `ids[:64]`。CLI 70 字 scientific 题干：独立间谍 `intervene_hidden_decode` 五次皆 **79 ids**，`any(n<=64)=False`，`prefix_n=79`。抄出的作者断言对 `seen=[64]` → False。旧替身 `prefix_truncated is not True` 对 `{False, n_ids:64}` **仍绿**——**不接受为充分**。 | 作者 `test_intervene_cli_hook_ids_exceed_64` 间谍 hook 并锁 `all(n > 64)` 与 `prefix_n`。helper 70/97 **仍在**（附加）。 |
| **calibrate / `_find_labels_jsonl` 不得绑兄 `lab`。不以 `inspect.getsource` 为充分** | **实现闭 + 作者 CLI 锁闭。** 独立 `cmd_calibrate`：有兄 `lab/WRONG` 时 finder 实参 `(None, fit, feat)`，**未传入兄路径**，`found is None`。有/无兄目录写出 **同一** toy `scores`（约 `0.0050235`）。`label_dirs.extend` / `parent / "lab"` / `joinpath("lab")` 不在 `cmd_calibrate` 源码。作者套件 **无** `inspect.getsource(cmd_calibrate)`。 | 作者 `test_calibrate_cli_ignores_sibling_lab` 实跑 CLI、wrap finder、断言兄路径不在实参、比 `calibration.jsonl`。helper `_find_labels_jsonl` 仍在（附加）。 |
| **点名 oracle：`card` / `forbid_host_exec` / Procrustes / `attention_mean` / `apply_model_template`** | **实现闭。** `card("qwen3-8b")["hidden_size"]==4096`；`card("r1-distill-qwen-7b")==3584`；未知名 KeyError；revision ≠ `latest`。`forbid_host_exec(boom)()` raise 且 `called==[]`。独立点集 `[[3,0],[0,1],[2,2],[1,-1]]` 右乘 90° `[[0,-1],[1,0]]`：`procrustes` 恢复 R，`apply_map` 回到 target。`attention_mean([[0.05,0.80,0.10,0.05]], [1])==0.80`；`[0,2]==0.075`；空权重/空下标 0；全 token 均值 0.25 **不相等**。tokenizer spy：`qwen3` kwargs 含 `enable_thinking=False`；`qwen2` 与 `r1-distill-qwen-7b` kwargs **不含**该键。 | 作者五例存在。本通道不把它们当唯一证明。 |
| **`stage_a` / `stage_b` 配对仍工作** | **闭。** collect 复制 edits。`donor_kind=same_value_diff_source`。 | 作者 `stage_a`/`stage_b` 不删 copy。 |
| **`apply_rename_edit({p1:p2,p2:p1})` 不得变 `p1 * p1`** | **实现闭。** 题干 `p2 = 4. p1 = 0. What is q = p2 * p1?`。 | 作者 swap 例锁同一题干。**不当 oracle。** |
| **自然 CoT / MODEL-01 / offline H / `constrained_target`** | **不要求，不开缺陷。** fixture collect `H.shape==(1,8)`。scientific prepare 7 条轨迹皆 `parse_status=constrained_target`。 | 测试不要求 §4.1 或 MODEL-01。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **`rho_M_excess != 1.0 or null_reason`** | `None != 1.0` 与 `0.0` 单独过；空 `events` 因不看事件也过。作者 **不再** 只用它关闭科学 sham。独立确认它对 0.0/空事件仍绿。 |
| **`is None or null_reason`** | **本冻结作者单元 sham 已不用。** 现为 excess/noise 皆 None **且** `null_reason == noise_set_missing`。 |
| **`all(status==refused_not_section8 for row if baseline in S)`** | 仍对 `[]` 与 `refused+score=1.0` 恒真。作者 **不再** 只用它。新断言有 `{baseline}==needed` 与 `score is None`。 |
| **`prefix_truncated is not True`** | 缺字段、硬编码 `False`、静默 `ids[:64]` 都绿。实现 L959 写死 False。**本通道不接受为充分。** 作者现另锁 hook `n>64` 与 `prefix_n`。独立间谍确认 79。 |
| **`inspect.getsource(cmd_calibrate)`** | **本冻结作者已不用。** |
| **`_tiny_prefix_ids` / `_find_labels_jsonl` helper** | helper 绿不能单独证明 CLI。本冻结另有 CLI 例。helper 仍在，只作附加。 |
| **`start>=len(prompt)`** | 若 `prompt_text` 被截，事件仍可在截断后。r07 全题干补了 alt-source。 |
| **教员强制 `q=`** | echo CE 前缀含答案数字。**不**开成自然 CoT 缺陷。 |
| **offline H 当 e2e** | 八段 exit 0。`H`←`token_ids[:8]`。smoke **要求**空结论。**诚实项。** |
| `timing != "pre_step"` | 任意其他字符串都绿。 |
| `test_plus_locks_*` | 同进程 RAM clear。**不**新进程。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| pytest / CE 后 persist 泄漏 | 172 passed 与独立 CE 之后磁盘为 `["gsm8k-12", "q:ada has 4 apples…"]`。该文件不在 61 摘要内。**测试卫生，不是冻结哈希缺陷。** |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：r22 页眉写独立 A–F 须在 `1f5f3798…` 上复核，且 `pytest` **仍不得**关闭可执行行；历史单元格 `python -m pytest -q`（71 处，含页眉）+ `passed_local_tests`（321 处）按任务 **不是** 通道 FAIL。本冻结 **没有** 新声称「协议行仅由 pytest 关闭」。`executable_function` 计数仍写 **159**。 |
| scientific calibrate | 对 tiny 探针写出有限非conformity 分数（约 `0.0050235`）。不是论文校准。有/无兄 `lab` 分数相同。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-22 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 `_f_scratch` 与 §8 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| Plus persist 新解释器 | 本通道只确认套件后磁盘仍有 Plus 键；作者也不 spawn。卫生项。 |
| 把 Goal 标 Complete | 本通道只评验证质量 |
| 把 offline H / `constrained_target` / fixture echo 开成缺陷 | 任务明确。不要求自然 CoT 或 MODEL-01。 |
| 把夹具 JSON 不进冻结开成缺陷 | 任务：协议，不是缺陷。 |
| 因历史账本单元格仍写 pytest 而 FAIL F21-11 | 任务：仅当本冻结 **新**声称协议行只由 pytest 关闭才 FAIL。页眉相反。 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 172 passed | `VERSION.md` | **命令是。** 当作 Goal：**否。** |
| F21-08 sham/噪声改为合取；`_scientific_sham_lock` 拒绝 0.0 / 空 events / 账面 1.0 / 缺 `null_reason`；旧弱析取不再单独关闭 | ISSUES | **独立同意。** 抄出锁对四伪造失败；弱锁对 0.0/空事件仍绿；作者关闭条件是合取锁。单元 sham 合取。 |
| F21-12 独立 oracle：`card` 4096/3584；`forbid_host_exec` 不调用被包函数；Procrustes 恢复已知旋转；`attention_mean` 用前提下标；`apply_model_template` 仅 qwen3 传 thinking | ISSUES | **独立同意。** 夹具 JSON 仍按协议不进冻结——**不开缺陷。** |
| F21-11 账本页眉已写 pytest 不得关闭可执行行；历史单元格不是关闭证据 | ISSUES | **独立同意到「本冻结未新声称 pytest 单独关协议行」。** 历史 71/321 字样仍在；按任务 **不** FAIL。 |
| F20-01 intervene CLI 间谍：70 字题干 hook `prompt_ids` 长度 >64，并写 `prefix_n` | ISSUES | **独立同意。** 独立间谍五次皆 79。不以 `prefix_truncated is not True` 为充分。 |
| F20-02 `cmd_calibrate` 实跑：兄 `lab` 不在 finder 参数里；有/无兄输出相同 | ISSUES | **独立同意。** 独立 spy 实参 `(None, fit, feat)`；输出相同。不以 `inspect.getsource` 为充分。 |
| F19-06 scientific fit 断言要求四条 §8 存在、`refused_not_section8`、无 `score` | ISSUES | **独立同意。** 省略行与 `score=1.0` 会红。 |
| F18-03 / F18-08 / F15-01 / A14-02 | ISSUES | **实现同意**（本通道独立重核未推翻）。 |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` | **本套件不能作证。** 本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`（scientific+tiny）；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击：**

- **科学 sham 锁必须合取，且拒绝 0.0 / 空事件 / 账面 1.0 / 缺 `null_reason`。** 抄出锁对四种伪造失败。旧弱析取对 0.0 与空事件仍绿——**不**当作关闭条件。作者关闭条件是 `_scientific_sham_lock`。**过滤猎项闭。**
- **scientific fit 断言必须因省略四行或 `score=1.0` 而红。** 抄出的作者断言对这两种突变失败。**过滤猎项闭。**
- **intervene 前缀必须完整或显式拒。不以 `prefix_truncated is not True` 为充分。** 独立间谍五次 79，无一 ≤64。**实现闭。作者 CLI 现锁 hook `n>64`。**
- **calibrate 不得读兄 `lab`。不以 `inspect.getsource` 为充分。** 独立 CLI spy 未绑 `WRONG`；有/无兄输出相同。**实现闭。作者实跑 CLI。**
- **`card` 必须钉 4096/3584。** 独立调用闭。
- **`forbid_host_exec` 不得调用被包函数。** 独立 spy `called==[]`。
- **Procrustes 必须恢复已知 90°。** 独立点集闭。
- **`attention_mean` 必须用前提下标，不能退回全 token 均值或恒 0。** 独立可区分权重闭。
- **`apply_model_template` 只对 qwen3 传 `enable_thinking`。** tokenizer kwargs 独立闭。
- **自然 CoT / MODEL-01。** 不要求。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_tiny_prefix_ids_refuse_silent_truncate` | 只调 helper。不经 `cmd_intervene`。本冻结另有 CLI 间谍例；本 helper **不是**关闭条件。 |
| `prefix_truncated is not True`（旧 r20 锁） | 对 `{False, n_ids:64}` 与缺字段为真。**本通道不接受。** |
| `inspect.getsource(cmd_calibrate)`（旧 r20 锁） | **本冻结已不在。** |
| `test_calibrate_does_not_bind_sibling_lab_labels` | 只调 `_find_labels_jsonl`。本冻结另有 CLI 例；本 helper **不是**关闭条件。 |
| `weak = lambda d: d.get("rho_M_excess") != 1.0 or d.get("null_reason")` | 作者故意保留以证明旧锁仍绿。**若只靠它关闭科学 sham，本通道会 FAIL。** 作者现不靠它关闭。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 §8 断言 | **锁存在性+无 score。** 独立突变确认省略/`score=1.0` 会红。本通道不把它当唯一证明。 |
| `test_generated_events_exclude_prompt_assignments` | 只锁 `start>=len(prompt)`。截断 `prompt_text` 仍绿。 |
| `test_rename_swap_is_simultaneous` | 锁对了实现合同。本通道不把它当证明；独立 CE 另核。 |
| `test_plus_locks_symbolic_family_to_test` | 不 spawn。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。诚实，不是 MODEL-01。 |
| `test_p1_held_out_logistic_detects_rho` | `ρ=y` 在全部行。`monkeypatch` 未用。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。作者已承认——**不要超售成科学 e2e。**
2. **F21-08 已不再用弱析取盖住「0.0 / 空事件 / 账面 1.0」。** 合取锁 + 四伪造。独立突变确认。
3. **F19-06 已不再用空真 `all` 盖住「必须存在且无 echo 分」。** 集合相等与 `score is None` 仍在。
4. **r06 用 start≥ 盖住全题干。** generate 实现已闭；作者 CLI 测试未升级。
5. **intervene 70：作者现间谍 hook ids，不再只用 `prefix_truncated is not True`。** helper 70/97 仍在，但是附加。实现仍写死 `prefix_truncated=False`。
6. **calibrate 兄 `lab`：作者现跑 `cmd_calibrate` 并查 finder 实参，不再用 `getsource`。**
7. **科学事件非空，来源仍是教员强制 `q=`。** echo CE 抽出 `\nq = 82`。**不**要求自然 CoT。
8. **A10-04 作者测试用同进程磁盘读盖住「新解释器」。**
9. **套件把 Plus 键写进仓库缓存且多数用例不 `clear`。** 卫生，不是冻结缺陷。
10. **账本历史单元格仍 pytest。** 页眉已写不得关可执行行；本冻结未新声称只靠 pytest 关闭协议行。

**作者现有点名 oracle 的符号：** `card`、`forbid_host_exec`、`procrustes` 数值恢复、`attention_mean`、`apply_model_template`。**仍无作者数值测试：** `attention_rollout`、`score_qa`、`assert_disjoint`。不够本通道 FAIL。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加生产测试。脚本：`_f_scratch/f22_ce.py`。

### CE-1 F21-08：合取 sham 锁必须拒绝四类伪造（闭）

```text
copied _scientific_sham_lock (test_round07 L244-257, not imported):
  any top-level excess/noise is not None → False
  events empty → False
  every event: excess AND noise all None AND null_reason == noise_set_missing

honest (all None + noise_set_missing + 1 event) → True
rho_M_excess=0.0, no null_reason override                 → False
events=[]                                                 → False
booked rho_M_excess=1.0 even if null_reason set           → False
event null_reason missing / None                          → False

real scientific prepare densities                         → True
same + rho_M_excess=0.0                                   → False
same + events=[]                                          → False
same + booked 1.0 with null_reason                        → False
same + event null_reason=None                             → False

old weak (rho_M_excess != 1.0 or null_reason):
  forged 0.0   → True   # still greens; not sufficient
  events=[]    → True
```

### CE-2 F20-01 intervene 前缀：独立间谍 hook ids；不以 flag 为充分（闭）

```text
scientific intervene on 70-char question:
  spy intervene_hidden_decode prompt_ids lens == [79,79,79,79,79]
  any(n<=64) == False
  prefix_n == 79

old surrogate prefix_truncated is not True:
  {relative:{prefix_truncated:False, n_ids:64}} → True   # NOT accepted

copied author test_intervene_cli_hook_ids_exceed_64:
  seen=[64] → False
```

### CE-3 F20-02 calibrate 不绑兄 `lab`：实跑 CLI；不以 getsource 为充分（闭）

```text
cmd_calibrate(--in-dir fit, --features-dir feat) with sibling lab/WRONG:
  _find_labels_jsonl dirs == [None, fit, feat]
  finder_passed_sibling == False
  found is None
  calibration.jsonl == same run without sibling lab/
  scores ≈ [0.0050236, 0.0050236, 0.0050236, 0.0050235]
  inspect.getsource ABSENT
```

### CE-4 F19-06：作者断言必须因省略行或 `score=1.0` 而红（闭）

```text
author assertion (copied from test_round06 L60-64, not imported):
  needed = {verbalizer, attention_mean, attention_rollout, attention_threshold}
  section8 = [row for row in probes if baseline in needed]
  {baseline} == needed
  all(status == refused_not_section8)
  all(score is None)

[]                                          → False
omit verbalizer                             → False
four refused + score=1.0                    → False
real scientific probes                      → True
same probes with §8 rows stripped           → False
same probes with score=1.0 written on §8    → False

vacuous all(... if baseline in S):
  []                          → True   # not sufficient
  {verbalizer, refused, 1.0}  → True
```

### CE-5 点名 oracle（闭）

```text
card("qwen3-8b").hidden_size == 4096
card("r1-distill-qwen-7b").hidden_size == 3584
card("not-a-registered-model") raises KeyError

forbid_host_exec(boom)() raises "host execution"; boom never called

procrustes(source @ R90) recovers R90 = [[0,-1],[1,0]]
apply_map(source, {W: R}) == source @ R90

attention_mean([[0.05,0.80,0.10,0.05]], [1]) == 0.80
attention_mean(..., [0,2]) == 0.075
all-tokens mean == 0.25   # distinct

apply_model_template(..., "qwen3", enable_thinking=False):
  tokenizer kwargs enable_thinking is False
apply_model_template(..., "qwen2" | "r1-distill-qwen-7b", enable_thinking=True):
  enable_thinking not in tokenizer kwargs
```

### CE-6 反向：CLI / 数学 — 独立 CE vs 烟测

| 分支 / 函数 | 本通道 | 作者套件 |
|---|---|---|
| prepare fixture | 烟测（作者） | 烟测 |
| prepare scientific | 独立：7×`constrained_target`（诚实）+ 合取 sham 锁 | 多例 + `_scientific_sham_lock` |
| collect scientific tiny / 拒 offline | 独立 | 锁 |
| fit scientific §8 拒绝 | 独立（行存在且无 score） | 存在性 + 无 score |
| calibrate scientific | 独立：有限玩具 \(q\)；兄 `lab` 不绑 | **CLI 实跑 + finder 实参 + 输出相等** |
| intervene 70 | **CLI 间谍 79 ids；无一 ≤64** | **CLI 间谍 n>64** |
| `card` / `forbid_host_exec` / Procrustes / `attention_mean` / template | **独立闭** | **作者五例** |
| `apply_rename_edit` 重叠 | **同时替换闭** | 作者有同字符串例（不当 oracle） |
| Plus persist 新进程 | 未 spawn | 未 spawn |

## 9. 发现

### F22-00 开审与交卷哈希可复算且一致

- **严重度：** —
- **状态：** HASH_MATCH（过程通过）
- **文件：** `.planning/audits/round-22/VERSION.md` L5–23；61 = `1f5f3798…9c7bcdb`；0 CRLF
- **复现：** 脚本原文开审与交卷同一摘要。

### F22-01 绿 172 不是 Goal / QA 验收

- **严重度：** High（验证口径）
- **状态：** standing note（ISSUES：不开成代码缺陷）。**不是**本通道 FAIL 条件。
- **复现：** `172 passed / 0 / 30.27s`，172 collected。作者主张与命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 仍是 offline 烟测。

### F22-02 F21-08：科学 sham / 噪声合取锁（点名闭）

- **严重度：** —
- **状态：** 测试设计闭合 + 实现闭合（独立抄锁 + 真实 prepare + 四伪造）
- **文件：** `tests/test_round07_regressions.py` L244–277；单元 sham L218–337；`tests/test_round06_regressions.py` L110–124
- **复现：** 抄出锁：诚实 True；`0.0` / `[]` / 账面 1.0+reason / 缺 `null_reason` 皆 False。弱锁对 `0.0` 与 `[]` 仍 True。作者 `assert _scientific_sham_lock(dens)` 且 `assert not` 四伪造；`only_weak_as_close=False`。单元三例合取。全测试检索弱析取只剩对照 `weak = lambda`。
- **作者主张 F21-08：** **独立同意。** 若作者仍只用 `!= 1.0 or null_reason` 关闭科学 sham，本条会 FAIL 通道——**没有。**

### F22-03 F20-01 / F18-08：70 字 CLI intervene hook ids >64（点名闭）

- **严重度：** —
- **状态：** 实现闭合 + 作者 CLI 测试闭合（独立间谍，不以 flag 为充分）
- **复现：** 独立间谍 ids 全是 79；`any(n<=64)=False`；`prefix_n=79`。旧 `prefix_truncated is not True` 对静默 cap **仍绿**——记下但不当作关闭条件。
- **作者主张 F20-01 / F18-08：** **独立同意。**

### F22-04 F20-02 / F18-12：`cmd_calibrate` 不绑兄 `lab`（点名闭）

- **严重度：** —
- **状态：** 实现闭合 + 作者 CLI 测试闭合（实跑，不以 getsource 为充分）
- **复现：** 独立 wrap：有兄 `lab/WRONG` 时 dirs=`[None, fit, feat]`，`finder_passed_sibling=False`，`found=None`。有/无兄 `calibration.jsonl` 全等，scores 约 `0.0050235`。作者套件无 `inspect.getsource(cmd_calibrate)`。
- **作者主张 F20-02 / F18-12：** **独立同意。**

### F22-05 F19-06：scientific-fit 断言因省略行或 `score=1.0` 而红（点名闭）

- **严重度：** —
- **状态：** 测试设计闭合（独立突变）。实现仍写四条 refused 且无 score。
- **复现：** 抄出的作者断言：空 / 省略一行 / `score=1.0` → False。真实 probes 上剥行或写分同样 False。旧 `all(... if baseline in S)` 对这两种输入仍 True——**不**当作充分。
- **作者主张 F19-06：** **独立同意。**

### F22-06 F21-12：点名 oracle（点名闭）；夹具不进冻结不是缺陷

- **严重度：** —
- **状态：** 测试/实现闭合（独立数字与 spy）。夹具 JSON 按任务为协议，**不开缺陷。**
- **复现：** 见 §8 CE-5。`attention_mean` 首次独立权重与全 token 均值撞数，改用 `[0.05,0.80,0.10,0.05]` 后与全 token `0.25` 可区分。
- **作者主张 F21-12：** **独立同意到点名符号。** `attention_rollout` 数值仍无作者 oracle——不够重开本条。

### F22-07 F20 helper-vs-CLI 猎项：本冻结仍闭

- **严重度：** —
- **状态：** 测试设计闭合。独立 CE 不靠 helper / `is not True` / `getsource`。
- **关闭此条不重置 hash。**

### F22-08 Fixture e2e 仍 offline；scientific tiny 仍 `constrained_target` — 诚实项，不开缺陷

- **严重度：** —
- **状态：** non-defect（验证口径）
- **注：** 任务与 ISSUES：八段是 offline 前缀 H；约束 `\nq=` 不是 §4.1；tiny 不是 MODEL-01。本通道 **不** 把它们写成已确认遗留缺陷。

### F22-09 Plus persist：作者缺 subprocess；套件泄漏缓存

- **严重度：** Low（测试卫生）
- **状态：** 机制前轮已见；172 passed 与独立 CE 后磁盘仍有 Plus 键。**不是冻结哈希缺陷。** 不因此 FAIL 通道。

### F22-10 账本历史单元格仍写 `pytest -q` / `passed_local_tests`

- **严重度：** —
- **状态：** **不 FAIL F21-11。** 页眉（r22 行）写 pytest 不得关可执行行，且历史单元格只表示曾跑过套件。本冻结 **没有** 新声称某一协议行仅由 pytest 关闭。`executable_function` 计数仍 **159**（本冻结作者称 172）——记下，不够本通道 FAIL。

### F22-11 ISSUES 点名关闭：F21-08/12 与 F20-01/02 / F19-06 独立同意

- **严重度：** —
- **状态：** 无「写已闭但点名 **实现或作者锁** CE 仍红」。
- **不要用本通道把 Goal/需求标 Complete。**

### F22-12 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq=` **不是** pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。通道通过不是 Goal 验收。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持 Goal。** 页眉已写 pytest 不得关可执行行；历史单元格仍 pytest。本通道不把历史单元格当新关闭。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道点名项不再阻断。** F21-08/12 独立闭。F21-01 是验收口径，不开成代码缺陷。本通道 **不** 据此宣布范围内无缺陷。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，Goal 实质仍失败。** `pytest -q` 确为 172/0。e2e 是 offline 烟测。点名 sham / 70 字 hook / 兄 `lab` / §8 / 五 oracle **现有** CE 级作者锁 + 独立间谍。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** 账本可执行计数仍 159。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **本通道不再用 F21-08 阻断。** 哈希匹配。r21 A–E PASS **不转移**。连续通过须在 `1f5f3798…` 上独立重做 A–E；`consecutive_pass_count` 仍为 0。本文件不能单独开始计数。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** offline H / `constrained_target` 按诚实项列出即可。已闭的 sham/oracle/hook/calibrate 锁 **不要** 再标 pending_server。 |
| 7 | 交付包 | **问题闭环未就绪到 Goal 句。** pytest 记录存在（172/0）。点名 CE 有独立记录。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行（诚实）。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、alt-source 图有。重叠 rename **实现闭**。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`（诚实）。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | `noise_ref=0` / 未知 \(M\) / sham missing **合取锁** 独立见。 |
| 5 划分 | 测试专用不进拟合 | Plus→test、family persist 有。跨进程无测试。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。intervene 长前缀 **实现拒截**；作者现锁 hook `n>64`。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。`attention_mean` **现有数值**。scientific 拒 §8 **实现有、作者存在性+无 score 仍闭**。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。scientific calibrate 出玩具有限 \(q\)；兄 `lab` 实现不绑；作者现跑 CLI。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。**Procrustes 90° 现有数值恢复。** `card` 4096/3584 现有。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。配对不靠 `prep` 名。长前缀实现闭；70 字 hook ids 作者+独立闭。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。**`forbid_host_exec` 现锁不调用。** T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **172 passed，exit 0，30.27s，172 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **HASH_MATCH `1f5f3798…9c7bcdb`（61，开审=交卷）。** |
| 独立性 | **独立闭：** F21-08 合取锁拒绝四伪造、弱锁仍绿 0.0/空事件、作者不以弱析取关闭；F19-06 作者断言对省略行与 `score=1.0` 失败；scientific fit 四行 refused 无 score；重叠 rename 同时替换；CLI intervene 79 ids / 无一 ≤64；calibrate CLI 不绑兄 `lab`；`card` 4096/3584；`forbid_host_exec` 不调用；Procrustes 90°；`attention_mean` 下标；template 仅 qwen3 传 thinking；`stage_a`/`stage_b`；孤立 fit。**独立红：无。** **不独立 / 套件缺口：** r06 `start>=`；同进程 persist；helper 仍在但是附加。**诚实非缺陷：** offline 前缀 H、`constrained_target`、fixture echo verbalizer。 |
| Mock/stub | offline 前缀 H + 教员强制 `q=` + `start>=` + 同进程 persist。**不再**用弱析取 / `prefix_truncated is not True` / `getsource` 冒充点名合同。 |
| 论文行为仍未证明 | 真 Prefill KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT（**未要求**） |
| 交付 vs 测试 | 「172 passed / F21-08/12 已闭 / F20-01/02 已闭 / F19-06 已闭」在**点名合同**上与独立 CE 一致。绿 172 **仍超过** Goal 验收。 |
| 已确认问题？ | **点名 CE 未失败。** High 口径笔记：F22-01（绿测试 ≠ Goal）。卫生：F22-09。F21-11 **不**因历史单元格 FAIL。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。通道通过不是 Goal 验收。 |
| 通道通过？ | **Pass。** 绿 pytest 不是验收。点名 F21-08 合取锁、F20 hook/calibrate、F19-06、五条 oracle 独立闭。不以弱析取 / `is not True` / `getsource` 为充分。offline H 与 `constrained_target` 按诚实项保留。 |
| 停止条件第 5 条 | **本通道不再阻断。** 哈希匹配。r21 A–E PASS 不转移；连续通过须在本哈希上独立重做 A–E。只补本文件不改变被审摘要。`consecutive_pass_count` 仍为 0。 |

点名重攻按任务口径已闭：合取 `_scientific_sham_lock` 拒绝 `rho_M_excess=0.0`、空 `events`、借口下账面 1.0、缺 `null_reason`；旧弱锁对 0.0 与空事件仍绿，且作者不再只用它关闭；单元 sham 是合取不是 `is None or`；独立间谍 `intervene_hidden_decode` 的 `prompt_ids` 无一 `len<=64`；独立 `cmd_calibrate` 有/无兄 `lab/WRONG` 输出相同且 finder 未收兄路径；作者 §8 断言在省略四行或 `refused+score=1.0` 时失败；`card` / `forbid_host_exec` / Procrustes / `attention_mean` / `apply_model_template` 独立数字与 spy 闭。**不**接受 `prefix_truncated is not True` 或 `inspect.getsource` 作为充分条件。offline 前缀 H 与 `constrained_target` 按诚实项保留，不在此要求 MODEL-01 或自然 CoT。夹具不进冻结是协议。Plus persist 残留是卫生。历史账本 pytest 字样不是本通道 FAIL。通道通过 **不是** Goal 验收，也 **不** 宣布 Goal 完成。
