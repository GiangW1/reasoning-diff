# F：验证质量与反向质疑（round-14）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-14 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 在进程内独立复跑（`%TEMP%\f14_ce_scratch.py`），不把 `tests/test_round07_regressions.py` 当证明。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`（61 文件，0 CRLF）。开审后立即 `python -m pytest -q --tb=line` 为 **157 passed / exit 0 / 20.99s / 157 collected**，与作者 `pytest_author_claim: 157` 一致。这不是 Goal 通过。

点名 CE 在 scratch 中独立复跑（不 import 测试文件）：**A12-03** 深目录 + 祖先/兄 `col/tasks.jsonl`（WRONG-TASK，E=`[p2,p1]`）`_find_tasks_jsonl is None` 且 fit **raise**；兄目录 `prep/` 与真祖先 `tasks.jsonl` 同样 raise；给定目录自己的 / `labels_dir` 的 `tasks.jsonl` 仍绑定。无本题 `tasks.jsonl` 时 **fit 与 calibrate 皆 raise**；helper 无 task 为 first-seen `['p2']`，有 task 为 `['p1','p2']`。collect 复制、label 不复制。**Plus 锁：** 清 RAM 后 Symbolic 仍 `test`；新进程空 RAM + 磁盘锁仍 `test`；从未加载 Plus 且无 persist 的孤立 Symbolic = `probe_train`（作者写明不是 A10-04 残留，独立同意）。标量/`bool`/`[0]` Prefill 拒；T3/T4 prepare（含 humaneval）无 `source_value_pair`；labels 塞协变量仍 `p1 is None`；`n<d` truncated；rename / pair 表达式 `p1 * p2_src`。sham 不广播。**Fixture 八段仍是 offline：** `H=[[1..8]]`，无 `H_pre_step`，intervene `unexpressible`/`donor_missing`，analyze `p1 is None`。科学事件仍只有教员强制 `q = <digit>`。

交卷再算为 `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（仍 61 文件，0 CRLF）→ **HASH_MISMATCH**。漂移文件（本通道未写）：`cli.py` 1249→1252、`edits.py` 287→362（新增 `apply_alt_source_same_value`）、`measure.py` 392→408（`behavior_unknown`）、`tests/test_round06_regressions.py` 字节变、`tests/test_round07_regressions.py` 256→296（新增 unknown-M / sham no_change 两例）。交卷 collect **159**。点名 CE 的 `_find_tasks_jsonl` 正文与开审冻结相同；事后补丁与新测 **不得**回写本冻结。账本协议行仍用 pytest 关闭。ISSUES 点名「已闭」在独立 CE 上 **未出现「声称已闭但 CE 仍失败」**；绿套件与 e2e 替身仍在。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637` |
| 开审复算 | `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明/开审/交卷都是 **61**。变的是字节，不是个数。 |
| 交卷漂移文件 | 见上。本通道未改。开审 `cli.py` `779cedd373a8a509` / 1249 行；交卷 `c1a274e233988aad` / 1252 行。`_find_tasks_jsonl` 开审已读、交卷仍只查传入目录。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest | **157 passed in 20.99s，exit 0**（`python -m pytest -q --tb=line`）。Collect：**157 nodes**。跑在开审 MATCH 后、交卷漂移前。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 157 passed`。开审命令独立见到。当作 Goal / 阶段验收：**否。** 不能回写为交卷盘上的 157。交卷 collect 已是 159。 |
| 范围 | 开审 61 文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。 |
| 明确未读 | `.planning/audits/round-14/{A,B,C,D,E}-*.md` |
| scratch | `%TEMP%\f14_ce_scratch.py` → `%TEMP%\f14_ce_results.json`。未写入 `src/` / `tests/` / `pyproject.toml`。 |

审查对象首先是**声明冻结字节**。`_find_tasks_jsonl` / `cmd_fit` raise / `splits.py` persist 在开审 MATCH 时已读。pytest 按开审盘记载。点名 CE 在 live import 上执行；A12-03 查找函数开审与交卷正文相同。`edits.py` / `measure.py` 交卷已变，其上的 rename/sham 第二次 scratch **标明可能已离开冻结**，不把交卷 `apply_alt_source_same_value` 写成冻结已闭。

## 2. 逐文件覆盖

以下行数/SHA-256 前 16 除另行标明外，是 **开审 HASH_MATCH** 时的 61 文件。

### 2.1 测试

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍 `--backend offline`；**不读 p1 / H 来源** |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a3…` | r03 节点；P1 泄漏用例仍绿；`ie_z` 单元仍是隐均值 helper；`test_rename_keeps_expression` 锁 `alpha * p2` |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline 几何仍只 `!= pre_step`；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= pre_step` / `!= donor_missing`；analyze labels **不锁 p1**；`n≥d` eye4 `truncated is False` |
| `tests/test_round06_regressions.py` | 145 | `ac7e4e88248ff49e…` | `donor_kind`/`inlp_transform`/`ie_z_g` 字段名；C6 helper；prefix_ids 拒；sham 析取。**交卷字节已变，不作冻结套件。** |
| `tests/test_round07_regressions.py` | **256（开审）** | `68f32ca36bf99513…` | 见 §3 / §6。含 `test_fit_does_not_bind_ancestor_col_tasks`（A12-03）。Plus 例锁 `_TEST_ONLY_FAMILY_KEYS.clear()` 后仍 test。**交卷 296 行 / `e8ba9102…`，多 unknown-M 与 sham no_change，不是冻结。** |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only（开审）：**157 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。测试函数 155 + `tiny_hooks` 多 1 参数 = 157。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。`assert True` 两处均为执行器载荷，不是恒真断言。

交卷 collect **159**（+`test_unknown_behavior_is_not_counted_as_m` + `test_sham_no_change_does_not_book_empty_n`）。不能写成声明冻结套件。

### 2.2 生产相对测试（开审冻结）

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | 泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | `attention_mean`/`rollout` 无数值 oracle |
| `cli.py` | 1249 | `779cedd373a8a509…` | smoke offline；scientific prepare/collect/fit/intervene；T3 prepare；无 tasks **raise**；A12-03 不绑祖先 `col/` | analyze 只认 `p1_table.jsonl`；`_load_source_value_pair` 仍搜兄 `prep/` edits（不是 tasks） |
| `edits.py` | 287 | `cacb63ac27cbcccf…` | value/rename/source-value 表达式重写 | 交卷改为 `apply_alt_source_same_value`，**不是冻结** |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 不在本文件（generate 写死 `"generated"`） |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；**`ie_z` helper 仍是均值差** | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 392 | `b15fb8a5bb92220f…` | 事件均值；unit 噪声扣除；sham 不广播 | `c7_m01` 手填 `noise_set`；交卷加 `behavior_unknown` |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 201 | `07493570c6410e6b…` | `start` 偏移 | 事件全是教员强制 `q=` |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` 未断言 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | CLI 无 task 现 raise（独立见）；作者未锁 calibrate |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | `prefix_token_ids` / 标量 hidden → False | `[0.0,1.0]` 仍 True（合法向量） |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 184 | `40ab4021d4dccc6e…` | Plus→test；族锁；persist JSON | `assert_disjoint` **零测试**；persist **不在 61 文件摘要内** |
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
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `1f61fd06…d91637`（61 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 交卷再算 | 同脚本 | **HASH_MISMATCH** `401e509b…de88f716`。5 文件 mtime 在开审后。 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **157 passed in 20.99s，exit 0**。无 skip/xfail/deselected。**开审盘。** |
| Collect | `python -m pytest tests --collect-only -q` | 开审 **157**。交卷盘 **159**（不是冻结）。 |
| skip/xfail/`assert True` | 对开审 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；TO 0.5；σ(1)；`[0.7,0.4]` | **存在的单元断言**与独立算术一致（未推翻前轮） |
| **独立 CE（scratch，不跑测试文件当证明）** | `%TEMP%\f14_ce_scratch.py` | 见下。未写入仓库。persist 文件开审/交卷均 snapshot/restore。 |

### 3.1 作者点名 CE — 独立复跑（不信测试文件）

| CE | 独立结果 | 作者测试是否锁住 |
|---|---|---|
| **A12-03** 深 feat + 祖先/兄 `col/tasks.jsonl` WRONG-TASK | **是。** `feat=work/deep/x/feat`，`col/tasks.jsonl` 为 WRONG-TASK 且 premises 对调。`_find_tasks_jsonl(feat, labs) is None`。fit → `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order`。helper：真 task E=`['p1','p2']`，swapped E=`['p2','p1']`。另：兄目录 `prep/tasks.jsonl` **不再救命**；真祖先 `anc4/tasks.jsonl` **不绑定**。给定 `feat/tasks.jsonl` 与 `labels_dir/tasks.jsonl` 仍绑定且 fit exit 0。 | `test_fit_does_not_bind_ancestor_col_tasks` 锁 `_find is None` + fit raise + E 不等。**不锁**兄 `prep/`、真祖先、calibrate。 |
| 无 `tasks.jsonl` → fit raise / first-seen E | **是。** 目录名 `alpha`/`beta`/`gamma`/`orphan/hidden_features`（不在 extras）：`_find is None`。fit raise 同上。`_e_premise_ids(None, labels)=['p2']`，带 task=`['p1','p2']`。**calibrate** 同样 raise（`calibrate requires tasks.jsonl…`）。 | `test_fit_without_tasks_jsonl_refuses_first_seen_order` 锁 fit raise。**不锁 calibrate，不比 first-seen 列。** |
| collect 复制 `tasks.jsonl` | **是。** fixture collect 后 copy 存在。`label` **不**复制。 | 锁存在。不比 Y 列。 |
| sham 不广播 | **是。** `build_labels`：`p1`/`p2` 的 `noise_ref is None`，仅 `sham:q` 为 `1.0`。`event_density_sets`：`null_reason=noise_set_missing`，`rho_M_excess is None`。科学 prepare `--sham-opportunities 1`：真实前提 `noise_ref` 全 None；聚合层 `null_reason is None`，`rho_M_excess is None`。弱析取 `excess != 1.0 or null_reason` 因 `None != 1.0` **仍绿**。 | 单元锁 p1/p2 None + sham 1.0。科学例是弱析取。 |
| `prefill_hidden=0/True/1.0/[0]/[]` | **皆 False** / `prefill_unavailable`。另：`False`/`[0.0]`/`[0.0,0.0]`/`"0"`/`None`/`np.array(0)`/`[[1]]` False；`[0.0,1.0]` True（合法 ≥2 维非零）。`prefix_token_ids` False。 | 作者测 0/True/1.0/[0]/[]。**实现闭。** |
| T3 prepare crash | hotpot/musique/**humaneval**/t4 prepare **exit 0**，edits kind 为 `document`/`paragraph`/`input_list`/`t4_question`，**无** `source_value_pair`。`_try_source_value_pair` 对四者皆 None。 | 锁 hotpot/musique exit + 无 pair kind。**Humaneval/t4 未进该测试。** |
| labels 冒充 P1 | 仅 labels（弱）与行内塞 `length/op/rho/y/held_out`（强）→ `p1 is None`，`scientific_conclusion is None`。对照：有 `p1_table.jsonl` 则 `p1` 有 `auc_full`/`delta_auc` 等键，`status=evaluated_descriptive`。 | 锁弱标签的 `p1 is None`。**不锁塞协变量。** 独立强攻击仍拒。 |
| `n < d` truncated | `(2,5)` vs `(2,3)` → `truncated=True` / `not_applicable_too_few_rows` / `common_dim=3`。`eye(4)` vs `eye(3)` → False。`(1,4)` vs `(1,3)` True。1-D → `not_applicable_shape_mismatch`。`(3,5)` vs `(3,4)` True。`(3,3)` vs `(3,3)` False。 | 锁 n=2 例。r05 锁 False 侧。**实现闭。** |
| rename 仍 `p1 * p2` | **否。** `make_source_value_pair(p2→2)` 与 `apply_rename_edit(p2→p2_src)` 表达式皆 `p1 * p2_src`。第二次 scratch 时 `edits.py` 可能已漂（交卷 `make_source_value_pair` 改走 `apply_alt_source_same_value`）；开审已读的 `apply_rename_edit` 仍重写表达式。 | r07 锁 pair 表达式；r03 锁 `alpha * p2`。 |
| **persist-lock after RAM clear** | **是。** 先 wipe persist+RAM：孤立 Ada/`gsm8k-1` Symbolic = `probe_train`。`load_gsm_plus` 后 persist=`['gsm8k-1', 'q:ada has…']`。`_TEST_ONLY_FAMILY_KEYS.clear()` 后 RAM=`[]`，persist 仍在，`split_for_task(symbolic)=='test'`。官方 Plus 路径同样。 | `test_plus_locks_symbolic_family_to_test` 末段锁 `.clear()` 后 test。 |
| **new-process Plus→Symbolic** | **是。** 子进程 RAM=`[]`，只 `load_gsm_symbolic`，persist 有文本键 → `split=test`。wipe persist 后新进程孤立 Symbolic = `probe_train`。 | **未锁新进程。** 独立补了。 |
| 孤立 Symbolic 从未 Plus | **`probe_train`。** persist 不存在。作者主张「不是 A10-04 残留」：独立同意这条不是缺陷。 | 作者测先加载 Plus，不测这条。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **教员强制 `q=` 当唯一科学事件** | seeds 0..2：事件全是 `['q']`，文本 `q = 82/53/53`，`parse_status=constrained_target`，`parse_region=generated`。`any(q)` + `parse_region` **全部被这条强制行单独满足**。`append_target_assignment` 教员强制 `\n{target} = `。 |
| **offline H 当步前 / e2e** | 八段（prepare/collect/label/fit/calibrate/intervene/repair/analyze）全 exit 0。`H.shape=(1,8)`，`H[0]=[1..8]`，`weight_source=offline_prefix_ids`，**无** `H_pre_step`。intervene `timing=unexpressible`，`status=donor_missing`。analyze `--in-dir lab`：`p1 is None`。smoke **要求**空结论。 |
| **analyze 无 p1_table** | smoke 与 `test_analyze_uses_labels_or_stays_null` 不断言 `p1`。假 P1 测试才锁 None。 |
| `timing != "pre_step"` | 任意其他字符串都绿。fixture offline 实际是 `unexpressible`；tiny 科学路径是 `offline_hidden`。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `rho_M_excess != 1.0 or null_reason`：聚合层 `null_reason is None` 且 excess 为 None 即绿。独立见到的是事件层 `noise_set_missing`。 |
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + `probes.jsonl`。不比 Y 列与 `task.premises`。 |
| `test_truth_indices_follow_e_columns_not_label_order` | helper 自带 `task.premises`。不跑「无 tasks.jsonl」CLI raise。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set=["p3"]`。不经 `build_labels` / `event_density_sets`。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `rho_S_noise is None or null_reason in {noise_set_missing, sham_protocol_missing}` | r06 析取仍在。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 名不副实。末 token 有限 H 也会绿。只比 `H.shape[0]==H_pre_step.shape[0]` 与 `>1`。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| 科学 prepare（独立，sham=1） | exit 0。真实前提 `noise_ref` None。事件密度 `noise_set_missing`。聚合弱 or 仍绿。 |
| fixture e2e | 见 §3.2。**仍是 offline 前缀 H。不要写成端到端科学已通。** |
| verbalizer / span | 既有 17/70/boxed 与跨界 `[]` 仍在（未推翻）。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：`python -m pytest -q` **70**；`passed_local_tests` **320**；`tests_exist_not_acceptance` **159**。页眉写不得用 pytest 关可执行行；协议行仍用 pytest 关闭。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed**（作者本冻结称 157）。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-14 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 对交卷 61 文件套件重跑 pytest 当冻结证据 | 那已不是声明 hash。开审 157 不得写成「当前树」。交卷 collect 159。 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| 把 persist 缓存当交付物验收 | 不在冻结摘要内 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 157 passed | `VERSION.md` | **开审命令是。** 当作 Goal / 冻结交卷证据：**否。** |
| A12-03：只读传入目录 `tasks.jsonl`；祖先 `col/` 对调不再静默绑定 | ISSUES | **独立 CE 是。** 作者新测锁 raise。兄 `prep/` / 真祖先独立也 raise，作者未锁。 |
| A10-04：Plus 锁持久化；仅清 RAM 后 Symbolic 仍 test | ISSUES | **独立 CE 是（RAM clear + 新进程）。** persist 文件不在 61 摘要内。孤立从未 Plus = `probe_train`，作者正确排除。 |
| 无本题 `tasks.jsonl` → fit/calibrate `ValueError`；collect 复制 | ISSUES C6 residual | **独立 CE 是（fit+calibrate+copy）。** 作者测试锁 fit 与 copy，不锁 calibrate、不比列。 |
| sham `noise_ref` 只在 `sham:`；不写入 N | ISSUES B9-01 | **独立 CE 是。** 科学 CLI 测试是弱析取。 |
| `_hidden_is_prefill` 拒标量/`bool`/`[0]` | ISSUES F6-04 | **是（独立 CE）。** |
| T3 prepare 不再强制 source-value | ISSUES E7-19 | **是（独立 CE，含 humaneval/t4）。** |
| analyze 不用标签冒充 P1 | ISSUES C7-M-02 | **是（独立 CE，含塞协变量）。** 作者测试较弱。 |
| `n < min d` → truncated | ISSUES C7-M-03 | **是（独立 CE）。** |
| rename 表达式 | ISSUES B5-05 | **开审 `apply_rename_edit` 同意。** 交卷 pair 改走 alt-source，不作冻结新闭。 |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

**账本超称：** 点名「已闭」项独立 CE **没有失败**。本通道不把 ISSUES 点名关闭记成「声称已闭但 CE 仍红」。超称在于用绿 pytest / 弱析取 / offline e2e 去顶 Goal，不在于 A12-03/A10-04 实现 CE 失败。

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离（源级）；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击失败 = 实现侧闭合（部分测试仍可能是替身）：**

- **A12-03 祖先 `col/` WRONG-TASK 不绑定。** 改回 4 层 extras 会让独立 CE 与作者新测红。
- **无 tasks.jsonl → fit/calibrate raise。** 改回 first-seen 且不 raise，作者 fit 例会红；calibrate 作者未锁，独立会红。
- **sham 不广播到真实前提 / 不写入 N。** `build_labels` 对 p1/p2 写 `noise_ref=1.0` 会让 r07 单元红。科学 CLI 弱析取仍可能绿。
- **标量 Prefill 不是 Prefill。** `0`/`True`/`[0]` 改回 `bool(np.isfinite(...).any())` 会红。
- **T3 prepare 不经 `source_value_pair`。** 再强制 T3 走 `make_source_value_pair` 会红或崩。
- **labels 不能造 P1。** `cmd_analyze` 改回用 labels 填 `length/op/rho` 会红。作者例不塞这些键，独立塞了仍拒。
- **`n < d` 必须 truncated。** 静默 PCA 会红。
- **rename 不再留下 `p1 * p2`。** 钉死旧表达式会红。
- **Plus persist：RAM `.clear()` 后仍 test。** 若只写 RAM、不写磁盘，作者 Plus 末段与独立 RAM-clear / 新进程会红。
- **`prefix_token_ids` 不是 Prefill。** 该半边仍有真 oracle。
- **collect 会复制 `tasks.jsonl`。** 不复制会让「exists」断言红——**仍不证明列序**。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + probes 文件。不比 `unique` 与 `task.premises`。 |
| `test_truth_indices_follow_e_columns_not_label_order` | helper 自带 `task.premises`。不跑无 tasks 的 CLI raise。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `!= 1.0 or null_reason`。聚合层 `null_reason is None` 也能绿。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set`。不经 labels。 |
| `test_analyze_refuses_fake_p1_from_labels` | 不塞 P1 协变量。实现比测试紧。 |
| `test_t3_prepare_survives_source_value_pair` | 无 humaneval。 |
| `test_fit_without_tasks_jsonl_refuses_first_seen_order` | 不锁 calibrate；不比 first-seen 列值。 |
| `test_plus_locks_symbolic_family_to_test` | 不锁新进程；不锁「从未 Plus」。RAM `.clear()` 半边是真 oracle。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 donor/INLP/`ie_z` 半边 | 锁字段名 + `prep/edits.jsonl`。不读 `trace_id`，不比 generated_ids。 |
| `test_generated_events_*` / scientific prepare `any(q)` | 教员强制 `\nq = 82` 单独满足。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 末 token 有限 H 也会绿。 |
| `test_intervene_geometry_is_not_pre_step` | offline 单行 H → `unexpressible`。`!= pre_step` 旧替身还在。 |
| `test_analyze_uses_labels_or_stays_null` | 不读 `p1`。结论空是 Week8 默认。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_ie_z_and_rescue_controls` | 仍测 **隐均值 helper**。 |
| `test_tiny_hooks` L17 | 恒真。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |
| 交卷 `test_unknown_behavior_*` / `test_sham_no_change_*` | **不在声明冻结。** |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]` = `[1..8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。不要写成「端到端科学路径已通」。
2. **C6-M-01 的 copy 测试不比列。** 孤立缺文件现 raise——真闭合。测试「follows E」仍不比 Y。
3. **科学事件非空，来源是教员强制 `q=`。** `parse_region` 硬编码 `"generated"`。
4. **步前 H 用有限行数冒充「不是末 token」。**
5. **donor/INLP/`ie_z`「分 decode」是 mode 字符串。**
6. **`ie_z_g=target_follow` 盖住恒 0 的 g。**
7. **C7-M-01 用 helper 的 `noise_set=["p3"]` 盖住 fixture 上 S 为空。**
8. **科学 sham 测试用弱析取盖住「聚合层没有 `null_reason`」。**
9. **账本协议行仍 pytest；可执行行 `tests_exist_not_acceptance`。**
10. **Plus 锁依赖摘要外 JSON。** 只拷 61 文件不会带上 `.planning/research/.cache/`。

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`（只经 `common_dim` 形状/truncated）、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 A12-03 祖先 `col/` WRONG-TASK（点名闭）

```text
prepare work/prep ; collect work/col ; label work/lab
copy features+traces → work/deep/x/feat   # 无 tasks.jsonl
copy labels → work/deep/x/labs
write WRONG-TASK + reversed premises → work/col/tasks.jsonl
_find_tasks_jsonl(feat, labs) is None
fit → ValueError tasks.jsonl
E(real)=[p1,p2]  E(swapped)=[p2,p1]

sibling prep:
  work/deep/x/prep/tasks.jsonl 在；feat 无
  _find is None ; fit raise     # 旧 4 层 extras 会救命

true ancestor:
  anc4/a/b/c/feat ；anc4/tasks.jsonl = WRONG-TASK
  _find is None ; fit raise

given-dir own / labels_dir tasks.jsonl:
  _find hits ; fit exit 0
```

### CE-2 无 `tasks.jsonl` first-seen E（点名闭；calibrate 作者未锁）

```text
prepare alpha/ ; collect beta/ ; label gamma/
copy features+labels → orphan/hidden_features + orphan/isolated_labels
_find_tasks_jsonl(...) is None
fit → ValueError tasks.jsonl
calibrate (probes+features+labels, 无 tasks) → ValueError tasks.jsonl
helper: first_seen=['p2']  vs task=['p1','p2']
collect copies tasks.jsonl ; label does not
```

### CE-3 sham 不广播（点名闭；科学测试弱）

```text
build_labels(p1 no_change, p2 changed, sham:q changed):
  noise_ref: p1=None, p2=None, sham:q=1.0
event_density_sets:
  null_reason=noise_set_missing ; rho_M_excess=None
scientific prepare sham=1:
  真实前提 noise_ref 全 None
  聚合层 null_reason 键为 None，excess=None
  作者：excess != 1.0 or null_reason  → 弱
```

### CE-4 Prefill / T3 / fake P1 / n<d / rename

```text
0 / True / False / 1.0 / [0] / [] / [0.0] / [0.0,0.0] / "0" / None / np.array(0) / [[1]]
  → refilled_prefix False
[0.0, 1.0] → True
prefix_token_ids=[1,2,3] → False

hotpot/musique/humaneval/t4 prepare exit 0
edits kinds = document / paragraph / input_list / t4_question
_try_source_value_pair → None

labels 仅 task/behavior → p1 is None
labels 塞 length/op/rho/y/held_out → p1 is None
p1_table.jsonl 对照 → p1 有 auc/delta 键

(2,5) vs (2,3) truncated True ; eye(4) vs eye(3) False
rename / pair 表达式 = p1 * p2_src   # 开审 apply_rename_edit
```

### CE-5 Plus persist / 新进程（点名 RAM-clear 闭；新进程作者未锁）

```text
wipe persist + RAM
孤立 Symbolic gsm8k-1 / Ada text = probe_train     # 不是缺陷
load Plus → persist [gsm8k-1, q:ada…]
_TEST_ONLY_FAMILY_KEYS.clear() → RAM []
split_for_task(Symbolic) = test                    # persist

new process, RAM [], persist present:
  load Symbolic only → test
new process, persist wiped:
  load Symbolic only → probe_train
```

### CE-6 教员强制 `q` / offline e2e（测试锁替身）

```text
generate_task_trace seeds 0..2:
  events = [['q'], ['q'], ['q']]
  assigned = '\nq = 82' / '\nq = 53' / '\nq = 53'
  parse_status = constrained_target
  parse_region = generated

fixture collect --backend offline:
  H = [[1,2,3,4,5,6,7,8]]
  weight_source = offline_prefix_ids
  H_pre_step 不存在
  intervene timing = unexpressible, status = donor_missing
  analyze lab: p1 is None
```

## 9. 发现

### F14-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）
- **文件：** `.planning/audits/round-14/VERSION.md` L5–23；开审 61 = `1f61fd06…`；交卷 61 = `401e509b…`
- **复现：** 开审脚本原文 MATCH。审查期间 5 文件被改（本通道未写）：`cli.py`、`edits.py`（+`apply_alt_source_same_value`）、`measure.py`（`behavior_unknown`）、`tests/test_round06_regressions.py`、`tests/test_round07_regressions.py`（+2 例）。事后补丁不能回写本冻结为已闭。
- **注：** 夹具与 persist JSON 仍在摘要外。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F14-01 绿 157 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** 开审 `157 passed / 0`。作者 claim 与该命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 是 offline 烟测。交卷已是另一 hash / 159 collect。

### F14-02 科学事件测试仍接受教员强制 `q=`

- **严重度：** Medium
- **状态：** confirmed defect（验证替身）
- **复现：** §3 CE-6。`any(node_id==q)` + `parse_region==generated` 被 `\nq = 82` 单独满足。
- **作者主张 A6-01 / 生成区事件：** **部分**（题干已排除；自然 CoT 未锁）

### F14-03 Fixture e2e 仍 offline；analyze 常无 `p1_table`

- **严重度：** Critical（验证）
- **状态：** confirmed defect（验证）
- **文件：** `tests/test_cli_pipeline.py`；`test_analyze_uses_labels_or_stays_null`
- **复现：** §3 CE-6。`H=[[1..8]]`，intervene `unexpressible`/`donor_missing`，`p1 is None`。不要写成端到端科学已通。

### F14-04 A12-03：祖先 `col/` WRONG-TASK 已拒（点名闭）

- **严重度：** —（实现）；Medium（验证残留：兄 `prep/` / calibrate / 列序未锁）
- **状态：** 实现闭合（独立 CE）。`_find_tasks_jsonl` 开审已读、交卷正文未改。
- **文件：** 开审 `cli.py` L692–700 / L619；`tests/test_round07_regressions.py` `test_fit_does_not_bind_ancestor_col_tasks`
- **复现：** §3 CE-1。
- **作者主张 A12-03 closed：** **实现同意。** 不是 Goal。

### F14-05 A10-04：persist 在 RAM `.clear()` 与新进程后仍锁（点名闭）

- **严重度：** Medium（协议：锁文件不在 61 摘要）
- **状态：** 实现闭合（独立 CE：RAM clear + 新进程）。孤立从未 Plus = `probe_train` **不是**残留缺陷。
- **文件：** 开审 `splits.py` `_save_persisted_locks` / `family_locked_test`；缓存 `.planning/research/.cache/gsm_test_only_families.json`
- **作者主张 A10-04 closed：** **实现同意。** 作者未锁新进程。摘要外 JSON 不是冻结产物。

### F14-06 C6 residual：孤立缺文件 fit/calibrate raise；collect 复制

- **严重度：** Medium（验证残留）。点名 raise **实现闭合**。
- **状态：** 实现闭合（独立 CE：fit + calibrate）。验证：copy 测试不比列。
- **作者主张 C6-M-01 residual closed：** **实现同意（孤立路径）。**

### F14-07 sham 不广播（点名闭）；科学 CLI 测试是弱析取

- **严重度：** Medium（验证残留）
- **状态：** 实现闭合（独立 CE）。`test_scientific_sham_*` 仍是 `!= 1.0 or null_reason`。
- **作者主张 B9-01：** **实现同意。** 第二次 sham scratch 时 `measure.py` 可能已漂；开审已读的 `build_labels` sham 分支与独立 unit 结果一致。

### F14-08 `prefill_hidden=0`/`True`/`[0]` 已拒（点名闭）

- **状态：** 实现闭合（独立 CE）
- **作者主张 F6-04：** **本冻结实现同意。**

### F14-09 T3 prepare 不再被 `source_value_pair` 打断（点名闭）

- **状态：** 实现闭合（hotpot/musique/humaneval/t4 独立 prepare exit 0）
- **作者主张 E7-19：** **本冻结实现同意。** 作者测试无 humaneval。

### F14-10 analyze 拒绝用 labels 造 P1（点名闭）

- **严重度：** Medium（验证残留）
- **状态：** 实现闭合；作者例不塞协变量，独立塞了仍 `p1 is None`
- **作者主张 C7-M-02：** **实现同意。**

### F14-11 `n < min d` 标 truncated（点名闭）

- **状态：** 实现闭合
- **作者主张 C7-M-03：** **本冻结实现同意。**

### F14-12 C7-M-01 测试是 helper；fixture 上 S 空

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）。unit 算术未推翻。
- **作者主张 C7-M-01：** **部分。** 不得用 helper 绿写成 label 路径已证。

### F14-13 donor / INLP / `ie_z` 测试仍锁名字

- **严重度：** Medium
- **状态：** confirmed defect（验证残留）
- **文件：** `tests/test_round06_regressions.py` L65–74（开审字节）
- **注：** 本轮未把「donor 仍 t0p / INLP 仍 swap」写成实现缺陷。测试力度不够。

### F14-14 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：70 / 320 / 159。`06-VERIFICATION.md` 仍写 136 passed。

### F14-15 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes` 数值恢复、`assert_disjoint`、`card`、`apply_model_template`

### F14-16 夹具与 persist 排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个）；`.planning/research/.cache/gsm_test_only_families.json`

### F14-17 ISSUES 点名关闭可独立同意实现；Goal / 连续通过不能开始

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为实现闭合（独立 CE，不是 Goal）：** A12-03；A10-04 persist（RAM+新进程）；C6 孤立 raise + collect copy；B9-01；F6-04；E7-19；C7-M-02；C7-M-03；B5-05 rename（开审 `apply_rename_edit`）。
- **未出现「ISSUES 称已闭但独立 CE 仍失败」。** 那条账本超称规则本轮未触发。
- **未闭 / 不能当作 Goal：** 交卷漂移（F14-00）；e2e offline（F14-03）；强制 `q=`（F14-02）；C7 helper（F14-12）；账本（F14-14）；科学 sham 弱析取。
- **不要用本通道把 Goal/需求标 Complete。**

### F14-18 真模型 / 官方全量 / 隔离 Linux runner

- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `q = <digit>` **不是** pending_server。交卷漂移也不是 pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 70 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F14-14）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F14-00、F14-03 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** 开审 157/0。e2e 是 exit-code 烟测并断言空结论（F14-03）。点名实现独立闭，若干作者测试仍锁替身。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 仍写 136 passed。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。本文件是审查日志，不改变被审摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：offline 前缀 H、强制 `q=`、目录名 donor、恒 0 的 `g(Y)`。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F14-17）。开审本机 pytest 记录不能挂到交卷 hash。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、rename 表达式有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。sham 不广播独立闭；科学 CLI 测试弱。C7 helper 在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。persist RAM-clear / 新进程独立闭。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。无 tasks 时 fit 现拒绝 first-seen。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。CLI 无 task 现 raise（独立；作者未锁）。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。测试锁 transform **名**。offline e2e 是 `unexpressible`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **157 passed，exit 0，20.99s，157 collected（开审盘）。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。**不是**交卷 hash 上的记录。 |
| 冻结 | **开审 HASH_MATCH `1f61fd06…`（61）。交卷 HASH_MISMATCH `401e509b…`（仍 61）。** |
| 独立性 | 真 oracle：A12-03 不绑祖先 `col/`；孤立缺 tasks → fit/calibrate raise；sham 不广播；标量 Prefill；T3 prepare（含 humaneval）；假 P1（含塞协变量）；n<d truncated；rename 表达式；collect copy；Plus persist RAM-clear + 新进程。**不独立：** copy「follows E」、科学 sham 弱析取、强制 `q=`、offline e2e、`!= pre_step`、donor/INLP/`ie_z` 字段名、C7 helper、analyze 弱例不读协变量。 |
| Mock/stub | offline 前缀 H + mode 字符串 + `ie_z_g` 标签 + 教员强制 `q=` + `not_evaluated` 编码为成功 + 科学 sham 弱析取 + 摘要外 persist JSON。 |
| 论文行为仍未证明 | 真 Prefill 向量语义之外的 KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT 事件、非 offline 的 e2e H |
| 交付 vs 测试 | 「157 passed / 点名全闭 / e2e 已通」**超过** 冻结树测试力度。点名实现独立同意，不能写成 Goal。ISSUES 点名项 **没有**「称已闭但 CE 失败」。 |
| 已确认问题？ | **是。** Critical：F14-00、F14-03。High：F14-01。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。交卷哈希已漂。Fixture e2e 仍 offline。点名实现闭合 **不** 使本通道通过。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。即使 A–E 全写「通过」，两轮计数必须保持 0；修复后换 **新** hash 重开。 |

在声明冻结上用 CE 级测试锁住 **e2e 非 offline 前缀 H**、**非强制 `q=` 的科学事件**、以及 **科学 sham 的事件层 `null_reason`（禁止弱析取）** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。事后改 `edits.py` / `measure.py` / r07 新例 **不能**把本轮改写成通过。点名实现闭合记在 F14-04…11，不是通道通过。
