# F：验证质量与反向质疑（round-12）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-12 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 在进程内独立复跑（`%TEMP%\f12_ce_scratch.py`），不把 `tests/test_round07_regressions.py` 当证明。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（61 文件，0 CRLF）。交卷再算为 `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（仍 61 文件）→ **HASH_MISMATCH**。漂移文件 mtime 在开审之后：`src/reasoning_diff/splits.py`（02:32:06）、`tests/test_round07_regressions.py`（02:32:14）。本通道未改这两文件。本机 `python -m pytest -q --tb=line` 为 **156 passed / exit 0 / 23.85s**，发生在漂移之后，**不能**写成声明冻结上的 156。这不是 Goal 通过。

作者点名六项，在**开审后仍未改字节的生产文件**上独立复现为闭：无 `tasks.jsonl` 且目录不叫 extras 时 **fit 与 calibrate 皆 raise**；sham 不把 `noise_ref` 广播到真实前提，N 不收真实前提；标量/`bool`/`[0]` Prefill 拒；T3 prepare（含 humaneval）不崩且无 `source_value_pair`；labels 塞 `length/op/rho/y` 仍 `p1 is None`；`n < min d` 标 `truncated=True`。`collect` 仍复制 `tasks.jsonl`；`label` 不复制。兄目录名叫 `prep` 时 4 层搜索仍能救命（作者写明「向上 4 层」，不是点名 CE 失败）。Fixture 八阶段仍是 offline：`H=[[1..8]]`，无 `H_pre_step`，intervene `unexpressible`/`donor_missing`，analyze `p1 is None`。科学事件仍只有教员强制 `q = <digit>`。账本协议行仍用 pytest 关闭。交卷哈希已漂。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4` |
| 开审复算 | `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b` |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明/开审/交卷都是 **61**。变的是字节，不是个数。 |
| 交卷漂移文件 | `src/reasoning_diff/splits.py` mtime 02:32:06；`tests/test_round07_regressions.py` mtime 02:32:14。本通道未改。当前盘：splits `40ab4021…` 184 行；r07 `1ffdbd7e…` 224 行。交卷 `splits.py` 把 Plus 锁持久化到 `.planning/research/.cache/gsm_test_only_families.json`。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest | **156 passed in 23.85s，exit 0**（`python -m pytest -q --tb=line`）。Collect：**156 nodes**。跑在交卷漂移之后。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 156 passed`。命令结果在**漂移后磁盘**上独立见到。当作 Goal / 阶段验收：**否。** 不能回写为声明 hash 上的 156。 |
| 范围 | 开审 61 文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。点名六项 CE 走的生产符号（`cli.py` / `measure.py` / `repair.py` / `transfer.py` / T3 任务模块）mtime 均在开审前，交卷未改。Plus 族锁的独立观察用了交卷后的 `splits.py`，**不作冻结证据**。 |
| 明确未读 | `.planning/audits/round-12/{A,B,C,D,E}-*.md` |

审查对象首先是**声明冻结字节**。点名 CE 的生产路径在开审 MATCH 后、交卷漂移前已读完且未再改。pytest 与 r07 测试文件的「套件证明力」按交卷盘记载，并标明不是冻结。

## 2. 逐文件覆盖

以下行数/SHA-256 前 16 除另行标明外，是 **开审 HASH_MATCH 时仍保持的字节**（mtime < 02:31）。`splits.py` 与 `test_round07_regressions.py` 为交卷盘。

### 2.1 测试

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍 `--backend offline`；**不读 p1 / H 来源** |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a3…` | r03 节点；P1 泄漏用例仍绿；`ie_z` 单元仍是隐均值 helper |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline 几何仍只 `!= pre_step`；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；仍不比 last-token；analyze labels **不锁 p1** |
| `tests/test_round06_regressions.py` | 145 | `ac7e4e88248ff49e…` | `donor_kind`/`inlp_transform`/`ie_z_g` 字段名；C6 helper；prefix_ids 拒；sham 析取 |
| `tests/test_round07_regressions.py` | **224（交卷）** | `1ffdbd7e…`（交卷） | 见 §3 / §6。`fit_without_tasks` 现是真 raise。`collect_copies` 仍只查文件。sham 科学例仍是弱析取。假 P1 不塞协变量。T3 无 humaneval。Plus 例在交卷盘上测磁盘锁。 |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only（交卷盘）：**156 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。测试函数 155 + `tiny_hooks` 多 1 参数 = 156。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。`assert True` 两处均为执行器载荷，不是恒真断言。

相对 r10 开审（153 / 61）：本冻结多 r07 点名例（缺 tasks raise、sham 不广播等）。交卷后又改 r07 Plus 例与 `splits.py`，不把交卷 Plus 持久化写成冻结已闭。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | 泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | `attention_mean`/`rollout` 无数值 oracle |
| `cli.py` | 1254 | `175abf12f4c207c5…` | smoke offline；scientific prepare/collect/fit/intervene；T3 prepare；无 tasks **raise** | 兄目录 `prep` 4 层搜索仍救命；`ie_z_g` 写死字符串；analyze 只认 `p1_table.jsonl` |
| `edits.py` | 287 | `cacb63ac27cbcccf…` | value/rename/source-value 表达式重写 | — |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；**`ie_z` helper 仍是均值差** | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 392 | `b15fb8a5bb92220f…` | 事件均值；unit 噪声扣除；**独立 CE：不广播** | `c7_m01` 测试不走 `event_density_sets` 的 mapped 真前提 |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token；不比各 mode 的 generated_ids |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 201 | `07493570c6410e6b…` | `start` 偏移 | 事件全是教员强制 `q=` |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` 未断言 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | CLI 无 task 现 raise（独立见） |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | `prefix_token_ids` / 标量 hidden → False | `[0.0,1.0]` 仍 True（合法向量，不是缺陷） |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | **184（交卷）** | `40ab4021…`（交卷） | Plus→test；族锁 | 开审冻结字节未知。交卷盘持久化到 `.planning/research/.cache/`。`assert_disjoint` **零测试** |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | `card` 无 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f…` | family / `register_test_only_family` | `"reversing operation"` 仍非 T4 |
| `tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354…` | sidecar；`shared_gsm_*` | — |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` 未断言 |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；口语 `needs_truth`；prepare 不崩 | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy；**独立 prepare 不崩** | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids；prepare 不崩 | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584；`n<d` truncated | `apply_map` 数值恢复未锁 |

另有 `models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 计入 61。夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `598e6c8f…6bd4`（61 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 交卷再算 | 同脚本 | **HASH_MISMATCH** `0816fa5b…3de3b`。`splits.py` + `test_round07_regressions.py` mtime 在开审后。 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **156 passed in 23.85s，exit 0**。无 skip/xfail/deselected。**漂移后磁盘。** |
| Collect | `python -m pytest tests --collect-only -q` | 156 nodes，collect exit 0（交卷盘） |
| skip/xfail/`assert True` | 对 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]` | **存在的单元断言**与独立算术一致（未推翻前轮） |
| **独立 CE（scratch，不跑测试文件当证明）** | `%TEMP%\f12_ce_scratch.py` | 见下。未写入仓库。 |

### 3.1 作者点名 CE — 独立复跑（不信测试文件）

| CE | 独立结果 | 作者测试是否锁住 |
|---|---|---|
| 无 `tasks.jsonl` → fit raise | **是。** 目录名 `alpha`/`beta`/`gamma`/`zeta`（不在 extras）：`_find_tasks_jsonl(odd, isolated) is None`。`fit` 抛 `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order`。**calibrate** 同样 raise。真实 labels 首次出现若走 helper 仍是 `['p2']`，带 task 是 `['p1','p2']`；raise 挡住这条路。 | `test_fit_without_tasks_jsonl_refuses_first_seen_order` 锁 fit raise。**不锁 calibrate。** 现是真 oracle，不是 r10 的「只查文件」。 |
| collect 复制 `tasks.jsonl` | **是。** fixture collect 后 copy 存在。`label` **不**复制。 | 锁存在。 |
| 兄目录名叫 `prep` | **仍救命。** `omega/featbox` + `omega/labbox` 无 tasks，但 `omega/prep/tasks.jsonl` 存在 → `_find_tasks_jsonl` 命中，fit **exit 0**。 | **未锁。** 作者主张「向上 4 层」与此一致；测试用 `prep/col/lab` 名仍可能盖住「in-dir 缺文件」。 |
| sham 不广播 | **是。** `build_labels`：`p1`/`p2` 的 `noise_ref is None`，仅 `sham:q` 为 `1.0`。`event_density_sets`：`noise_set is None`，`null_reason=noise_set_missing`，`rho_M_excess is None`，`rho_M_noise is None`。科学 prepare `--sham-opportunities 1`：真实前提 `noise_ref` 全 None；事件层 `null_reason=noise_set_missing`，`S=[]`，`M=['p1','p2']`，`rho_M_excess is None`。聚合层 `null_reason` 键为 None（只均值 excess），`rho_M_excess is None`。 | 单元锁 `p1/p2` None + sham 1.0 + excess None。科学例是 `rho_M_excess != 1.0 or null_reason` **弱析取**——聚合层 `null_reason is None` 时仍绿。 |
| `prefill_hidden=0/True/1.0/[0]/[]` | **皆 False** / `prefill_unavailable`。另：`False`/`[0.0]`/`[0.0,0.0]`/`"0"`/`None`/`np.array(0)`/`[[1]]` False；`[0.0,1.0]` 与 `[[1,2]]` True（≥2 维有限非零，合法）。`prefix_token_ids` False。 | 作者测 0/True/1.0/[0]/[]。**实现闭。** |
| T3 prepare crash | hotpot/musique/**humaneval** prepare **exit 0**，`tasks.jsonl` 在，edits kind 为 `document`/`paragraph`/`input_list`，**无** `source_value_pair`。`_try_source_value_pair` 对三者皆 None。 | 锁 hotpot/musique exit + 无 pair kind。**Humaneval 未进该测试**，独立也不崩。**实现闭。** |
| labels 冒充 P1 | 仅 `labels.jsonl`（弱：只有 task/behavior；强：行内塞 `length/op/rho/y/held_out`）→ `p1 is None`，`scientific_conclusion is None`，`status=not_evaluated`。对照：有 `p1_table.jsonl` 则 `p1` 有 `auc_full`/`delta_auc` 等键。 | 锁弱标签的 `p1 is None`。**不锁塞协变量。** 独立强攻击仍拒。 |
| `n < d` truncated | `(2,5)` vs `(2,3)` → `truncated=True` / `not_applicable_too_few_rows` / `common_dim=3`。`eye(4)` vs `eye(3)` → `truncated=False`。`(1,4)` vs `(1,3)` True。1-D → `not_applicable_shape_mismatch`。`(3,5)` vs `(3,4)` True。`(3,3)` vs `(3,3)` False。 | 锁 n=2 例。**实现闭。** |
| rename 仍 `p1 * p2` | **否。** `make_source_value_pair(p2→2)` 与 `apply_rename_edit(p2→p2_src)` 表达式皆 `p1 * p2_src`。 | 锁表达式。冻结 `edits.py`。**实现闭。** |
| family Plus vs Symbolic | **交卷 `splits.py`，不是冻结证据。** `clear_test_only_families()` 后单独 Symbolic = `probe_train`；先 Plus 再 Symbolic = `test`。 | 交卷例还断言内存 `.clear()` 后仍 test（磁盘锁）。冻结字节未独立见到。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **教员强制 `q=` 当唯一科学事件** | seeds 0..2：事件全是 `['q']`，文本 `q = 82/53/53`，`parse_status=constrained_target`，`parse_region=generated`。`any(q)` + `parse_region` **全部被这条强制行单独满足**。 |
| **offline H 当步前 / e2e** | 六阶段（prepare/collect/label/fit/intervene/analyze）全 exit 0。`H.shape=(1,8)`，`H[0]=[1..8]`，`weight_source=offline_prefix_ids`，**无** `H_pre_step`。intervene `timing=unexpressible`，`status=donor_missing`。analyze `--in-dir lab`：`p1 is None`。smoke **要求**空结论。 |
| **analyze 无 p1_table** | smoke 与 `test_analyze_uses_labels_or_stays_null` 不断言 `p1`。假 P1 测试才锁 None。 |
| `timing != "pre_step"` | 任意其他字符串都绿。本通道 offline 实际是 `unexpressible`。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `rho_M_excess != 1.0 or null_reason`：聚合层 `null_reason is None` 且 excess 为 None 即绿。独立见到的是事件层 `noise_set_missing`。 |
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + `probes.jsonl`。不比 Y 列与 `task.premises`。目录名恰好是 `prep/col/lab`。 |
| `test_truth_indices_follow_e_columns_not_label_order` | helper 自带 `task.premises`。不跑「无 tasks.jsonl」CLI（现 CLI 会 raise，该例仍不测 raise）。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set=["p3"]`。不经 `build_labels` / `event_density_sets`。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `rho_S_noise is None or null_reason in {noise_set_missing, sham_protocol_missing}` | r06 析取仍在。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| 科学 prepare（独立，sham=1） | exit 0。真实前提 `noise_ref` None。事件密度 `noise_set_missing`。 |
| fixture e2e | 见 §3.2。 |
| verbalizer / span | 既有 17/70/boxed 与跨界 `[]` 仍在（未推翻）。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：`python -m pytest -q` **70**；`passed_local_tests` **320**；`tests_exist_not_acceptance` **159**；`executable_function` 162。页眉写不得用 pytest 关可执行行；协议行仍用 pytest 关闭。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed**（作者本冻结称 156）。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-12 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 对声明冻结字节单独重跑 pytest | 开审后、本通道跑 pytest 前，`splits.py` / r07 已漂。156 不能挂到 `598e6c8f…` |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| 把交卷 Plus 磁盘锁写成冻结已闭 | `splits.py` 不是声明 hash |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 156 passed | `VERSION.md` | **漂移后命令是。** 当作冻结证据 / Goal：**否。** |
| 无 `tasks.jsonl` → fit/calibrate `ValueError` | ISSUES C6-M-01 residual | **独立 CE 是（fit+calibrate）。** 作者测试锁 fit，不锁 calibrate。 |
| collect 复制；查找向上 4 层 | ISSUES C6-M-01 | **是。** copy 独立确认。4 层 + extras 使兄目录 `prep` 仍能 fit。 |
| sham `noise_ref` 只在 `sham:`；不写入 N | ISSUES B9-01 | **独立 CE 是。** 科学 CLI 测试是弱析取。 |
| `_hidden_is_prefill` 拒标量/`bool`/`[0]` | ISSUES F6-04 | **是（独立 CE）。** |
| T3 prepare 不再强制 source-value | ISSUES E7-19 | **是（独立 CE，含 humaneval）。** |
| analyze 不用标签冒充 P1 | ISSUES C7-M-02 | **是（独立 CE，含塞协变量）。** 作者测试较弱。 |
| `n < min d` → truncated | ISSUES C7-M-03 | **是（独立 CE）。** |
| rename / Plus 锁族 | ISSUES B5-05 / B5-01 | rename：**冻结实现同意。** Plus：**交卷 `splits.py`，不作冻结闭合。** |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离（源级）；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击失败 = 实现侧闭合（部分测试仍可能是替身）：**

- **无 tasks.jsonl → fit/calibrate raise。** 改回 first-seen 且不 raise，作者新 fit 例会红；calibrate 作者未锁，独立会红。
- **sham 不广播到真实前提 / 不写入 N。** `build_labels` 对 p1/p2 写 `noise_ref=1.0` 会让 r07 单元红。科学 CLI 弱析取仍可能绿。
- **标量 Prefill 不是 Prefill。** `0`/`True`/`[0]` 改回 `bool(np.isfinite(...).any())` 会红。
- **T3 prepare 不经 `source_value_pair`。** 再强制 T3 走 `make_source_value_pair` 会红或崩。
- **labels 不能造 P1。** `cmd_analyze` 改回用 labels 填 `length/op/rho` 会红。作者例不塞这些键，独立塞了仍拒。
- **`n < d` 必须 truncated。** 静默 PCA 会红。
- **rename 不再留下 `p1 * p2`。** 钉死旧表达式会红。
- **`prefix_token_ids` 不是 Prefill。** 该半边仍有真 oracle。
- **collect 会复制 `tasks.jsonl`。** 不复制会让「exists」断言红——**仍不证明列序**。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + probes 文件。目录名 `prep/col/lab`，父搜索能救命。不比 `unique` 与 `task.premises`。 |
| `test_truth_indices_follow_e_columns_not_label_order` | helper 自带 `task.premises`。不跑无 tasks 的 CLI raise。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `!= 1.0 or null_reason`。聚合层 `null_reason is None` 也能绿。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set`。不经 labels。 |
| `test_analyze_refuses_fake_p1_from_labels` | 不塞 P1 协变量。实现比测试紧。 |
| `test_t3_prepare_survives_source_value_pair` | 无 humaneval。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 donor/INLP/`ie_z` 半边 | 锁字段名 + `prep/edits.jsonl`。不读 `trace_id`，不比 generated_ids。 |
| `test_generated_events_*` / scientific prepare `any(q)` | 教员强制 `\nq = 82` 单独满足。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 名不副实。末 token 有限 H 也会绿。 |
| `test_intervene_geometry_is_not_pre_step` | offline 单行 H → `unexpressible`。`!= pre_step` 旧替身还在。 |
| `test_analyze_uses_labels_or_stays_null` | 不读 `p1`。结论空是 Week8 默认。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_ie_z_and_rescue_controls` | 仍测 **隐均值 helper**。 |
| `test_tiny_hooks` L17 | 恒真。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |
| 交卷 `test_plus_locks_symbolic_family_to_test` 的内存 `.clear()` | **不在声明冻结。** 测的是磁盘锁。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]` = `[1..8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。不要写成「端到端科学路径已通」。
2. **C6-M-01 的 copy + 4 层 extras 启发式** 仍让 `prep/` 兄目录在 in-dir 缺文件时 fit 成功。孤立目录现 raise——这是真闭合。测试「follows E」仍不比列。
3. **科学事件非空，来源是教员强制 `q=`。** `parse_region` 硬编码 `"generated"`。
4. **步前 H 用有限行数冒充「不是末 token」。**
5. **donor/INLP/`ie_z`「分 decode」是 mode 字符串。**
6. **`ie_z_g=target_follow` 盖住恒 0 的 g。**
7. **C7-M-01 用 helper 的 `noise_set=["p3"]` 盖住 fixture 上 S 为空。**
8. **科学 sham 测试用弱析取盖住「聚合层没有 `null_reason`」。**
9. **账本协议行仍 pytest；可执行行 `tests_exist_not_acceptance`。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`（只经 `common_dim` 形状/truncated）、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 无 `tasks.jsonl` → fit/calibrate raise（点名闭）

```text
prepare alpha/ ; collect beta/ ; label gamma/
copy features+labels → zeta/hidden_features + zeta/isolated_labels
_find_tasks_jsonl(...) is None
fit → ValueError tasks.jsonl
calibrate → ValueError tasks.jsonl
helper 若被调用：first_seen=['p2']  vs task=['p1','p2']

兄目录 prep：
  omega/featbox 无 tasks；omega/prep/tasks.jsonl 在
  fit exit 0     # 4 层 extras，作者主张内

应：孤立缺文件必须 raise（已闭）；「follows E」应比 Y 列，不得只查 probes.jsonl
```

### CE-2 sham 不广播（点名闭；科学测试弱）

```text
build_labels(p1 no_change, p2 changed, sham:q changed):
  noise_ref: p1=None, p2=None, sham:q=1.0
event_density_sets:
  noise_set=None, null_reason=noise_set_missing
  rho_M_excess=None, rho_M_noise=None
scientific prepare sham=1:
  真实前提 noise_ref 全 None
  事件层 null_reason=noise_set_missing, M=[p1,p2], excess=None
  聚合层 null_reason 键为 None，excess=None
  作者：excess != 1.0 or null_reason  → 弱
```

### CE-3 Prefill（点名 0/True/[0] 已闭）

```text
0 / True / False / 1.0 / [0] / [] / [0.0] / [0.0,0.0] / "0" / None / np.array(0) / [[1]]
  → refilled_prefix False
[0.0, 1.0] / [[1.0, 2.0]]
  → True   # 合法 ≥2 维非零有限向量
prefix_token_ids=[1,2,3] → False   已锁
```

### CE-4 T3 prepare（已闭，含 humaneval）

```text
hotpot/musique/humaneval prepare exit 0
edits kinds = document / paragraph / input_list
_try_source_value_pair → None
```

### CE-5 fake P1（已闭，强于作者例） / n<d（已闭）

```text
labels 仅 task/behavior → p1 is None
labels 塞 length/op/rho/y/held_out → p1 is None
p1_table.jsonl 对照 → p1 有 auc/delta 键
(2,5) vs (2,3) truncated True ; eye(4) vs eye(3) False
(1,4) vs (1,3) True ; 1-D shape_mismatch
```

### CE-6 教员强制 `q` / offline e2e（测试锁替身）

```text
generate_task_trace seeds 0..2:
  events = [['q'], ['q'], ['q']]
  text values = 'q = 82' / 'q = 53' / 'q = 53'
  parse_status = constrained_target

fixture collect --backend offline:
  H = [[1,2,3,4,5,6,7,8]]
  weight_source = offline_prefix_ids
  H_pre_step 不存在
  intervene timing = unexpressible, status = donor_missing
  analyze lab: p1 is None
```

## 9. 发现

### F12-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）
- **文件：** `.planning/audits/round-12/VERSION.md` L5–23；开审 61 = `598e6c8f…`；交卷 61 = `0816fa5b…`
- **复现：** 开审脚本原文 MATCH。审查期间 `splits.py`（02:32:06）与 `tests/test_round07_regressions.py`（02:32:14）被改。本通道未改这些文件。交卷 `splits.py` 增加 `.planning/research/.cache/gsm_test_only_families.json` 持久化。事后补丁不能回写本冻结为已闭。
- **注：** 夹具仍在摘要外（F12-14）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F12-01 绿 156 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** 漂移后 `156 passed / 0`。作者 `pytest_author_claim` 与该命令一致，但命令不在声明 hash 上。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 是 offline 烟测。

### F12-02 科学事件测试仍接受教员强制 `q=`

- **严重度：** Medium
- **状态：** confirmed defect（验证替身）
- **复现：** §3 CE-6。`any(node_id==q)` + `parse_region==generated` 被 `q = 82` 单独满足。
- **作者主张 A6-01 / 生成区事件：** **部分**（题干已排除；自然 CoT 未锁）

### F12-03 Fixture e2e 仍 offline；analyze 常无 `p1_table`

- **严重度：** Critical（验证）
- **状态：** confirmed defect（验证）
- **文件：** `tests/test_cli_pipeline.py`；`test_analyze_uses_labels_or_stays_null`
- **复现：** §3 CE-6。`H=[[1..8]]`，intervene `unexpressible`/`donor_missing`，`p1 is None`。不要写成端到端科学已通。

### F12-04 C6-M-01 residual：孤立缺文件已 raise（点名闭）；`prep` 启发式与「follows E」测试仍弱

- **严重度：** Medium（验证残留）。点名「missing tasks.jsonl → fit raises」**实现闭合**。
- **状态：** 实现闭合（独立 CE：fit + calibrate）。验证：copy 测试不比列；4 层 extras 未作为失败路径锁。
- **文件：** `cli.py` `_find_tasks_jsonl` / `cmd_fit` L619 / `cmd_calibrate` L776；`tests/test_round07_regressions.py`（交卷盘）
- **复现：** §3 CE-1。
- **作者主张 C6-M-01 residual closed：** **实现同意（孤立路径）。** 不是「任意缺 in-dir 文件都 raise」。

### F12-05 sham 不广播（点名闭）；科学 CLI 测试是弱析取

- **严重度：** Medium（验证残留）
- **状态：** 实现闭合（独立 CE）。`test_scientific_sham_*` 仍是 `!= 1.0 or null_reason`。
- **作者主张 B9-01：** **实现同意。**

### F12-06 `prefill_hidden=0`/`True`/`[0]` 已拒（点名闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE）
- **作者主张 F6-04：** **本冻结实现同意。**

### F12-07 T3 prepare 不再被 `source_value_pair` 打断（点名闭）

- **严重度：** —
- **状态：** 实现闭合（hotpot/musique/humaneval 独立 prepare exit 0）
- **作者主张 E7-19：** **本冻结实现同意。** 作者测试无 humaneval。

### F12-08 analyze 拒绝用 labels 造 P1（点名闭）

- **严重度：** Medium（验证残留）
- **状态：** 实现闭合；作者例不塞协变量，独立塞了仍 `p1 is None`
- **作者主张 C7-M-02：** **实现同意。**

### F12-09 `n < min d` 标 truncated（点名闭）

- **严重度：** —
- **状态：** 实现闭合
- **作者主张 C7-M-03：** **本冻结实现同意。**

### F12-10 C7-M-01 测试是 helper；fixture 上 S 空

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）。unit 算术未推翻。
- **作者主张 C7-M-01：** **部分。** 不得用 helper 绿写成 label 路径已证。

### F12-11 donor / INLP / `ie_z` 测试仍锁名字

- **严重度：** Medium
- **状态：** confirmed defect（验证残留）
- **文件：** `tests/test_round06_regressions.py` L65–74
- **注：** 本轮未把「donor 仍 t0p / INLP 仍 swap」写成实现缺陷。测试力度不够。

### F12-12 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：70 / 320 / 159。`06-VERIFICATION.md` 仍写 136 passed。

### F12-13 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes` 数值恢复、`assert_disjoint`、`card`、`apply_model_template`

### F12-14 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个）

### F12-15 ISSUES / VERSION 点名关闭可独立同意；Goal / 连续通过不能开始

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为实现闭合（独立 CE，不是 Goal）：** C6-M-01 孤立 raise；B9-01 sham 不广播；F6-04 标量 Prefill；E7-19 T3 prepare；C7-M-02 假 P1；C7-M-03 truncated；B5-05 rename；collect 复制 `tasks.jsonl`。
- **未闭 / 不能当作 Goal：** 交卷漂移（F12-00）；e2e offline（F12-03）；强制 `q=`（F12-02）；C7 helper（F12-10）；账本（F12-12）；Plus 磁盘锁（交卷，非冻结）。
- **不要用本通道把 Goal/需求标 Complete。**

### F12-16 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `q = <digit>` **不是** pending_server。交卷漂移也不是 pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 70 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F12-12）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F12-00、F12-03 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** 156/0 在漂移盘上。e2e 是 exit-code 烟测并断言空结论（F12-03）。点名六项独立闭，若干作者测试仍锁替身。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 仍写 136 passed。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。本文件是审查日志，不改变被审摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：offline 前缀 H、强制 `q=`、目录名 donor、恒 0 的 `g(Y)`。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F12-15）。开审本机 pytest 记录不能挂到声明 hash。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、rename 表达式有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。sham 不广播独立闭；科学 CLI 测试弱。C7 helper 在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。冻结 Plus 族锁被交卷 `splits.py` 污染。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。无 tasks 时 fit 现拒绝 first-seen。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。CLI 无 task 现 raise。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。测试锁 transform **名**。offline e2e 是 `unexpressible`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **156 passed，exit 0，23.85s，156 collected（漂移后磁盘）。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。**不是**声明 hash 上的记录。 |
| 冻结 | **开审 HASH_MATCH `598e6c8f…`（61）。交卷 HASH_MISMATCH `0816fa5b…`（仍 61）。** |
| 独立性 | 真 oracle：孤立缺 tasks → fit/calibrate raise；sham 不广播；标量 Prefill；T3 prepare（含 humaneval）；假 P1（含塞协变量）；n<d truncated；rename 表达式；collect copy。**不独立：** copy「follows E」、科学 sham 弱析取、强制 `q=`、offline e2e、`!= pre_step`、donor/INLP/`ie_z` 字段名、C7 helper、analyze 弱例不读协变量。Plus 磁盘锁 = 交卷。 |
| Mock/stub | offline 前缀 H + `prep/` 兄目录 + mode 字符串 + `ie_z_g` 标签 + 教员强制 `q=` + `not_evaluated` 编码为成功 + 科学 sham 弱析取。 |
| 论文行为仍未证明 | 真 Prefill 向量语义之外的 KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT 事件、非 offline 的 e2e H |
| 交付 vs 测试 | 「156 passed / 点名全闭 / e2e 已通」**超过** 冻结树测试力度。点名六项**实现**独立同意，不能写成 Goal。 |
| 已确认问题？ | **是。** Critical：F12-00、F12-03。High：F12-01。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。交卷哈希已漂。Fixture e2e 仍 offline。点名六项实现闭合 **不** 使本通道通过。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。即使 A–E 全写「通过」，两轮计数必须保持 0；修复后换 **新** hash 重开。 |

在声明冻结上用 CE 级测试锁住 **e2e 非 offline 前缀 H**、**非强制 `q=` 的科学事件**、以及 **科学 sham 的事件层 `null_reason`（禁止弱析取）** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。事后改 `splits.py` / r07 Plus 例 **不能**把本轮改写成通过。点名六项的实现闭合记在 F12-04…09，不是通道通过。
