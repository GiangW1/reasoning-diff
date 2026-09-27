# F：验证质量与反向质疑（round-10）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-10 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 在进程内独立复跑，不把 `tests/test_round07_regressions.py` 当证明。

**先行结论：** 开审时按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`（61 文件，0 CRLF）。本机对该树 `python -m pytest -q --tb=line` 为 **153 passed / exit 0 / 20.19s**。这不是 Goal 通过。作者点名项里：标量/`bool`/`[0]` Prefill、T3 prepare 不崩、rename 后表达式为 `p1 * p2_src`、Plus 锁 `gsm8k-1` 使 Symbolic 进 `test`、labels 冒充 P1 被拒、`n < min d` 标 `truncated=True`——实现侧独立复现为闭。`collect` 默认会复制 `tasks.jsonl`。但 **`fit` 在无 `tasks.jsonl` 且目录不叫 `prep`/`lab` 时仍走 labels 首次出现序**（本夹具真实 labels 只有 `['p2']`）；作者测试只断言文件存在，不锁 E 列序。Fixture 八阶段仍是 offline：`H=[[1..8]]`，无 `H_pre_step`，intervene `unexpressible`/`donor_missing`，analyze 无 `p1_table` → `p1 is None`。科学事件仍只有教员强制 `\nq = <digit>`。账本把 C6-M-01 residual 标成已闭，而「无 tasks.jsonl → first-seen E」CE 仍失败，这是 **确认缺陷（账本超售 + 残留）**。交卷前 `measure.py` 与两份测试已漂离声明冻结。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d` |
| 开审复算 | `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689` |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明/开审/交卷都是 **61**。变的是字节，不是个数。 |
| 交卷漂移文件 | `src/reasoning_diff/measure.py` `c81e2402…`→`b15fb8a5…`；`tests/test_round07_regressions.py` `cad435ad…`→`e4228445…`（170→200 行）；`tests/test_review_regressions.py` `d3814498…`→`c1f02364…`。本通道未改这些文件。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| pytest（开审冻结树） | **153 passed in 20.19s，exit 0。** Collect：**153 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 153 passed`。命令结果独立确认。当作 Goal / 阶段验收：**否。** |
| 范围 | 开审 61 文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。交卷后多出的 r07 两例（sham broadcast / ρ_M）**不在声明冻结套件**，只记漂移，不作冻结证据。 |
| 明确未读 | `.planning/audits/round-10/{A,B,C,D,E}-*.md` |

审查对象首先是**声明冻结字节**。pytest 与点名 CE 在开审 MATCH 后执行（C7 的 `event_density_sets` 续跑时 `measure.py` 可能已开始漂；冻结逻辑以开审读到的原文为准，见 §3）。交卷磁盘已变，**不能**把事后补丁写成冻结已闭。

## 2. 逐文件覆盖

以下行数/SHA-256 前 16 是 **开审 HASH_MATCH** 时的 61 文件。

### 2.1 测试（开审全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍 `--backend offline`；**不读 p1 / H 来源** |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 399 | `d3814498fe52b28b…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a3…` | r03 节点；P1 泄漏用例仍绿；`ie_z` 单元仍是隐均值 helper |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline 几何仍只 `!= pre_step`；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；仍不比 last-token；analyze labels **不锁 p1** |
| `tests/test_round06_regressions.py` | 145 | `ac7e4e88248ff49e…` | `donor_kind`/`inlp_transform`/`ie_z_g` 字段名；C6 helper；prefix_ids 拒；sham 析取 |
| `tests/test_round07_regressions.py` | **170** | `cad435add5103d94…` | 见 §3 / §6。名字大于断言：`fit_follows_e_order` 只查文件；`c7_m01` 只打 `dependency_densities` helper |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only（开审）：**153 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。测试函数 152 + `tiny_hooks` 2 参数 = 153。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r09（144 / 60 文件）：本冻结多 `tests/test_round07_regressions.py`（开审 9 例）及生产补丁。交卷后又加 2 例，不计入 153。

### 2.2 生产相对测试（开审冻结）

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | r04 常数 δ 仍可能退化；泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | `attention_mean`/`rollout` 无数值 oracle |
| `cli.py` | 1251 | `ba474e1fea1f7c5a…` | smoke offline；scientific prepare/collect/fit/intervene；T3 prepare | **无 tasks.jsonl + 非 prep 名 → first-seen**；`ie_z_g` 写死字符串；analyze 只认 `p1_table.jsonl` |
| `edits.py` | 287 | `cacb63ac27cbcccf…` | value/rename/source-value 表达式重写 | — |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；**`ie_z` helper 仍是均值差** | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 389 | `c81e2402671228b6…` | 事件均值；unit 噪声扣除；sham 缺测 | `c7_m01` 测试不走 `event_density_sets`。**交卷已改字节。** |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token；不比各 mode 的 generated_ids |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 201 | `07493570c6410e6b…` | `start>=len(prompt)` | 事件全是教员强制 `q=` |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook 清理 + logits 变 | last-token / `once=True` 未断言 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | CLI 无 task 时回到首次出现序 |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | `prefix_token_ids` / 标量 hidden → False | `[0.0,1.0]` 仍 True（合法向量，不是缺陷） |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 152 | `08f77e972927a996…` | Plus→test；全局 family lock | `assert_disjoint` **零测试**；进程级 `_TEST_ONLY_FAMILY_KEYS` |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | `card` 无 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f…` | family / `register_test_only_family` | `"reversing operation"` 仍非 T4 |
| `tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354…` | sidecar；`shared_gsm_*` | — |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` 未断言 |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；口语 `needs_truth`；prepare 不崩 | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy；prepare 不崩 | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids；prepare 不崩 | `new_answer` 未断言 |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584；`n<d` truncated | `apply_map` 数值恢复未锁 |

夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `81308124…4b6d`（61 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 交卷再算 | 同脚本 | **HASH_MISMATCH** `7518e20b…7a41`。`measure.py` + `test_round07_regressions.py` + `test_review_regressions.py` 已改。 |
| 全量 pytest | 开审后仓库根 `python -m pytest -q --tb=line` | **153 passed in 20.19s，exit 0**。无 skip/xfail/deselected。 |
| Collect | `python -m pytest tests --collect-only -q` | 153 nodes，collect exit 0（开审） |
| skip/xfail/`assert True` | 对开审 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]` | **存在的单元断言**与独立算术一致 |
| **独立 CE（scratch，不跑测试文件当证明）** | `%TEMP%\f10_ce_scratch.py` + `f10_ce_scratch2.py` | 见下各行。未写入仓库。 |

### 3.1 作者 r07 点名 CE — 独立复跑（不信测试文件）

| CE | 独立结果 | 作者测试是否锁住 |
|---|---|---|
| collect 复制 `tasks.jsonl` | **是。** fixture collect 后 `col/tasks.jsonl` 存在。 | 锁存在。 |
| fit 跟 E 列序 | **测试不锁。** `test_collect_copies_tasks_so_fit_follows_e_order` 只断言 `probes.jsonl` 存在。删掉 copy 后，若兄目录名叫 `prep`，`_find_tasks_jsonl` 仍命中 `prep/tasks.jsonl`。 | **替身。** 名字说 follows E，身体不比列。 |
| 无 `tasks.jsonl` → first-seen E | **仍失败。** 目录名 `alpha`/`beta`/`gamma`（不在 extras 里）：删 `beta/tasks.jsonl` 后 `_find_tasks_jsonl(beta,gamma) is None`。`label` **不**复制 tasks。真实 fixture labels 首次出现 `['p2']`（默认编辑零值前提 p2）。`_e_premise_ids(None, labels)==['p2']`。反序 `[{p2},{p1}]` → `['p2','p1']`；带 task → `['p1','p2']`。`first_seen_mismatch=True`。补 `event_id` 后 fit 仍 exit 0。 | **缺失。** ISSUES 写已闭 → **账本超售。** |
| helper `_e_premise_ids(task, 反序)` | `['p1','p2','p3']`。 | `test_truth_indices_*` 只锁这个。 |
| `prefill_hidden=0/True/1.0/[0]/[]` | **皆 False** / `prefill_unavailable`。另：`[0.0]` False；`[0.0,0.0]` False（范数 0）；`False`/`"0"`/`None`/`np.array(0)`/`[[1]]` False；`[0.0,1.0]` 与 `[[1,2]]` True（≥2 维有限非零，合法）。 | 作者测 0/True/1.0/[0]/[]。**实现闭。** |
| T3 prepare crash | hotpot/musique/humaneval prepare **exit 0**，`tasks.jsonl` 在，edits kind 为 `document`/`paragraph`/`input_list`，**无** `source_value_pair`。`_try_source_value_pair` 对三者皆 None（T3 / `humaneval_derived` / `composition_reference`）。 | 锁 hotpot/musique exit + 无 pair kind。Humaneval 未进该测试，独立也不崩。**实现闭。** |
| rename 仍 `p1 * p2` | **否。** `make_source_value_pair(p2→2)` 与 `apply_rename_edit(p2→p2_src)` 表达式皆 `p1 * p2_src`，parents/ids 含 `p2_src`。`p1→alpha` 为 `alpha * p2`。 | 锁表达式。**实现闭。** |
| family `gsm8k-1` Plus vs Symbolic | 清全局锁后 Symbolic **单独** `split_for_task` = **`probe_train`**。load Plus 后同一 Symbolic → `test`（进程锁）。`siblings=[plus]` → `test`。无 `original_id` 的 official Plus 与 Symbolic 的 `shared_gsm_text` 相同，再 split Symbolic → `test`。 | 锁「先 Plus 再 Symbolic」。**不锁「仅 Symbolic 可进拟合」**（单独是 `probe_train`，符合「有 Plus 才锁」）。**实现闭。** |
| labels 冒充 P1 | analyze 仅 `labels.jsonl`（行内塞了 `length/op/rho/y`）→ `p1 is None`，`scientific_conclusion is None`，`status=not_evaluated`。 | 锁 `p1 is None`。**实现闭。** 更弱的 `test_analyze_uses_labels_or_stays_null` **不读 p1**。 |
| `n < d` truncated | `(2,5)` vs `(2,3)` → `truncated=True` / `not_applicable_too_few_rows`。`eye(4)` vs `eye(3)` → `truncated=False`。`(1,4)` vs `(1,3)` True。1-D → `not_applicable_shape_mismatch`。 | 锁 n=2 例。**实现闭。** |
| mapped noise 扣除 | **unit** `dependency_densities(..., noise_set=["p3"], ...)` → `rho_S_noise=1.0`，`rho_S_excess=0.0`。**`event_density_sets` + t1_tiny：** p1/p2 都是 q 的祖先，S 空，扣除空转。**sham:** `null_reason=noise_set_missing`，不记已评估 0。 | 作者测只打 unit helper。label 路径未锁「映射真实前提进 N」。 |
| review merge | `awaiting_human` → `filled`/`ok`。 | 锁。**实现闭。** |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **教员强制 `q=` 当唯一科学事件** | 3 条 tiny 轨迹事件全是 `['q']`，`target_assignment` 为 `\nq = 82/53/53`，`parse_status=constrained_target`，`parse_region=generated`，`start >= len(prompt)`。`test_generated_events_*` / `test_scientific_prepare_emits_parseable_events` 的 `any(q)` + `parse_region` **全部被这条强制行单独满足**。 |
| **offline H 当步前 / e2e** | 八阶段全 exit 0。`H.shape=(1,8)`，`H[0]=[1..8]`，`weight_source=offline_prefix_ids`，**无** `H_pre_step`。intervene `timing=unexpressible`，`status=donor_missing`。`test_intervene_geometry_is_not_pre_step` 的 `!= pre_step` 对此为真。analyze 入参是 `lab/`（无 `p1_table`），`p1 is None`。smoke **要求**空结论。`label` 不复制 `tasks.jsonl`。 |
| **analyze 无 p1_table** | smoke 与 `test_analyze_uses_labels_or_stays_null` 不断言 `p1`。假 P1 测试才锁 None。 |
| `timing != "pre_step"` | 任意其他字符串都绿。本通道 offline 实际是 `unexpressible`。 |
| `status in {prospective_decode, geometry_on_hidden}` | 两值都算过。 |
| `rho_S_noise is None or null_reason in {noise_set_missing, sham_protocol_missing}` | 析取过宽。 |
| `null_reason != noise_set_empty or rho_S_excess is not None` | 一边真即可。 |
| `lo <= hi`（r05 bootstrap） | 退化区间过。r06 才 `lo < hi`。 |
| `donor_kind` / `inlp_transform==inlp` / `ie_z_g==target_follow` | 仍是字段名。不锁 `trace_id`、decode 差、非恒 0 的 `g(Y)`。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 只锁 `isfinite` 与行数。本通道科学 `H` 为 7×32、7 个 `q` 行，**仍不比 last-token 下标**。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_c7_m01_*` | 手填 `noise_set=["p3"]`，不经 labels。 |

### 3.3 其他对抗（开审树 / 与冻结逻辑一致）

| 对抗 | 结果 |
|---|---|
| 科学 prepare 事件 | 7 条轨迹（base/t0p/edit/source/p1/p2/sham）事件全是强制 `q = 82` 或 `53`。 |
| 科学 collect | `H` 全有限 7×32。`event_rows` 全是 `node_id=q`。 |
| 科学 collect 拒 offline | 既有测试锁 `offline_prefix_ids`。fixture e2e **不**走 scientific。 |
| verbalizer / span | 既有 17/70/boxed 与跨界 `[]` 仍在。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：`python -m pytest -q` **70**；`passed_local_tests` **320**；`tests_exist_not_acceptance` **159**；`executable_function` 162。页眉写不得用 pytest 关可执行行；协议行仍用 pytest 关闭。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed**（本冻结作者称 153）。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-10 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 对交卷漂移树重跑 pytest 当冻结证据 | 那已不是声明 hash。r07 已变成 11 例。 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| 在冻结 `measure.py` 字节上重跑 label→density（续跑时文件已漂） | 开审读到的 sham/mapped 分支已足够判断测试替身；unit 扣除与 sham missing 在开审逻辑下同样成立 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 153 passed | `VERSION.md` | **开审命令是。** 当作阶段/Goal 证据：**否。** 交卷磁盘已不是该冻结。 |
| collect 复制 tasks；fit/calibrate 搜 `prepare/` | ISSUES C6-M-01 | **部分。** copy 与 `prep` 启发式独立确认。**不证明**无文件时拒绝 first-seen。作者测试不比 E 列。 |
| `_hidden_is_prefill` 拒标量/`bool`/`[0]` | ISSUES F6-04 | **是（独立 CE）。** |
| T3 prepare 不再强制 source-value | ISSUES E7-19 | **是（独立 CE）。** |
| rename 重写 id/表达式 | ISSUES B5-05 | **是（独立 CE）。** |
| Plus 注册 family 锁，Symbolic 同族 `test` | ISSUES B5-01 | **是（独立 CE）。** 单独 Symbolic 仍可 `probe_train`。 |
| analyze 不用标签冒充 P1 | ISSUES C7-M-02 | **是（独立 CE）。** 弱测试仍不读 p1。 |
| `n < min d` → truncated | ISSUES C7-M-03 | **是（独立 CE）。** |
| 映射真实前提扣除；`sham:` 仍 missing | ISSUES C7-M-01 | **unit 扣除是。** label 路径测试是 helper。sham missing 在 `event_density_sets` 上独立见到。 |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击失败 = 实现侧闭合（部分测试仍可能是替身）：**

- **标量 Prefill 不是 Prefill。** `0`/`True`/`[0]` 改回 `bool(np.isfinite(...).any())` 会让作者新测试红。独立 CE 同意。
- **T3 prepare 不经 `source_value_pair`。** 再强制 T3 走 `make_source_value_pair` 会红或崩；现跳过。
- **rename 不再留下 `p1 * p2`。** 钉死旧表达式会红。
- **Plus 先注册则 Symbolic 为 test。** 同族仍进 `probe_train` 会红（在「先 load Plus」顺序下）。
- **labels 不能造 P1。** `cmd_analyze` 改回用 task/behavior 填 `length/op/rho` 会红。
- **`n < d` 必须 truncated。** 静默 PCA 会红。
- **`prefix_token_ids` 不是 Prefill。** 该半边仍有真 oracle。
- **collect 会复制 `tasks.jsonl`。** 不复制会让「exists」断言红——**仍不证明列序**。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_collect_copies_tasks_so_fit_follows_e_order` | **C6-M-01 替身。** 只查 copy + probes 文件。目录名恰好是 `prep`/`col`/`lab`，父搜索能救命。不比 `unique` 与 `task.premises`。 |
| `test_truth_indices_follow_e_columns_not_label_order` | helper 自带 `task.premises`。不跑「无 tasks.jsonl」CLI。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set`。不经 `build_labels` / `event_density_sets`。t1_tiny 上 S 恒空。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 donor/INLP/`ie_z` 半边 | 锁字段名 + `prep/edits.jsonl`。不读 `event_rows.trace_id`，不比 generated_ids，不比 `ie_z` 与隐均值。 |
| `test_generated_events_*` / scientific prepare `any(q)` | 教员强制 `\nq = 82` 单独满足。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 名不副实。末 token 有限 H 也会绿。 |
| `test_intervene_geometry_is_not_pre_step` | offline 单行 H → `unexpressible`。`!= pre_step` 旧替身还在。 |
| `test_analyze_uses_labels_or_stays_null` | 不读 `p1`。结论空是 Week8 默认。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_p1_returns_bootstrap_interval` | 非空即可。 |
| `test_ie_z_and_rescue_controls` | 仍测 **隐均值 helper**。 |
| `test_tiny_hooks` L17 | 恒真。 |
| `test_joint_edit_blocks_soundness` | 旗标恒 False。 |
| 交卷后 `test_scientific_sham_does_not_book_rho_m_excess_one` | **不在开审冻结。** 且 `rho_M_excess != 1.0 or null_reason` 是弱析取。 |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]` = `[1..8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。不要写成「端到端科学路径已通」。
2. **C6-M-01 用 copy + `prep/` 启发式 + helper 自带 task 盖住 first-seen。** `label` 不写 `tasks.jsonl`。孤立目录名仍 first-seen。
3. **科学事件非空，来源是教员强制 `q=`。** `parse_region` 硬编码 `"generated"`。
4. **步前 H 用有限行数冒充「不是末 token」。**
5. **donor/INLP/`ie_z`「分 decode」是 mode 字符串。**
6. **`ie_z_g=target_follow` 盖住恒 0 的 g。** 教员强制 `82` vs hook 抽到的数字。
7. **C7-M-01 用 helper 的 `noise_set=["p3"]` 盖住 fixture 上 S 为空。**
8. **账本协议行仍 pytest；可执行行 `tests_exist_not_acceptance`。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 教员强制 `q` 是唯一科学事件（测试锁替身）

```text
generate_task_trace seeds 0..2:
  events = [['q'], ['q'], ['q']]
  target_assignment = '\nq = 82' / '\nq = 53' / '\nq = 53'
  parse_status = constrained_target
  parse_region = generated
  start >= len(prompt)

scientific prepare (7 traces): 每条只有一条 q 事件，文本 'q = 82' 或 'q = 53'

应：锁自然 CoT 前提赋值，或显式声明本机接口是 constrained_target，禁止把 any(q) 写成「科学事件已解析」
```

### CE-2 offline H 当 e2e / `!= pre_step`（测试锁替身）

```text
fixture 八阶段 --backend offline:
  H = [[1,2,3,4,5,6,7,8]]
  weight_source = offline_prefix_ids
  H_pre_step 不存在
  intervene timing = unexpressible, status = donor_missing
  analyze --in-dir lab: 无 p1_table, p1 is None
  scientific_conclusion is None   # smoke 要求这个

应：e2e 用 scientific+tiny 且断言 H 不是 token 前缀；timing 正匹配 hook；analyze 无表则拒或锁 p1 is None
```

### CE-3 fit 无 `tasks.jsonl` → first-seen E（CE 仍失败；账本写已闭）

```text
prepare alpha/ ; collect beta/ ; unlink beta/tasks.jsonl ; label gamma/
_find_tasks_jsonl(beta, gamma) is None
label 不复制 tasks.jsonl
真实 labels 首次出现 ['p2']          # 默认编辑 p2=0→2
_e_premise_ids(None, labels) == ['p2']
反序 labels [{p2},{p1}] → ['p2','p1']
带 task.premises → ['p1','p2']
prep/col 兄目录：删 copy 后仍找到 prep/tasks.jsonl

应：无 task 则拒绝 fit/calibrate；CLI 反序 labels 断言 Y 列与 E 对齐；测试不得只查 probes.jsonl
```

### CE-4 Prefill（点名 0/True 已闭）

```text
0 / True / False / 1.0 / [0] / [] / [0.0] / [0.0,0.0] / "0" / None / np.array(0) / [[1]]
  → refilled_prefix False
[0.0, 1.0] / [[1.0, 2.0]]
  → True   # 合法 ≥2 维非零有限向量
prefix_token_ids=[1,2,3] → False   已锁
```

### CE-5 T3 prepare（已闭）

```text
hotpot/musique/humaneval prepare exit 0
edits kinds = document / paragraph / input_list
_try_source_value_pair → None
```

### CE-6 rename（已闭） / family（已闭） / fake P1（已闭） / n<d（已闭）

```text
expression == 'p1 * p2_src'   不是 'p1 * p2'
Symbolic 单独 = probe_train ; 先 Plus 或 siblings=[plus] = test
labels 含 length/op/rho/y → p1 is None
(2,5) vs (2,3) truncated True ; eye(4) vs eye(3) False
```

### CE-7 C7-M-01 路径

```text
dependency_densities(noise_set=['p3']) → noise=1, excess=0     unit 闭
event_density_sets(t1_tiny, mapped p2) → S=[] 扣除空转         测试未锁
event_density_sets(sham:q) → noise_set_missing                 与 B6-02 一致
```

## 9. 发现

### F10-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）
- **文件：** `.planning/audits/round-10/VERSION.md` L5–23；开审 61 = `81308124…`；交卷 61 = `7518e20b…`
- **复现：** 开审脚本原文 MATCH。审查期间 `measure.py`（`event_density_sets` 增加 `sham_hits` 优先分支）、`tests/test_round07_regressions.py`（+2 例）、`tests/test_review_regressions.py` 被改。本通道未改这些文件。事后补丁不能回写本冻结为已闭。
- **注：** 夹具仍在摘要外（F10-16）。只要本通道提交已确认缺陷，连续通过计数不能开始。

### F10-01 绿 153 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** 开审 `153 passed / 0`。作者 `pytest_author_claim` 与命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 是 offline 烟测。

### F10-02 科学事件测试仍接受教员强制 `q=`

- **严重度：** Medium
- **状态：** confirmed defect（验证替身）
- **复现：** §3 CE-1。`any(node_id==q)` + `parse_region==generated` 被 `\nq = 82` 单独满足。
- **作者主张 A6-01 / 生成区事件：** **部分**（题干已排除；自然 CoT 未锁）

### F10-03 Fixture e2e 仍 offline；analyze 常无 `p1_table`

- **严重度：** Critical（验证）
- **状态：** confirmed defect（验证）
- **文件：** `tests/test_cli_pipeline.py`；`test_analyze_uses_labels_or_stays_null`
- **复现：** §3 CE-2。`H=[[1..8]]`，intervene `unexpressible`/`donor_missing`，`p1 is None`。不要写成端到端科学已通。

### F10-04 C6-M-01：copy/`prep` 启发式已接线；无 tasks.jsonl 仍 first-seen；账本超售

- **严重度：** High
- **状态：** confirmed defect（残留实现 + 验证替身 + 账本）。**点名 CE「fit without tasks.jsonl first-seen E」仍失败。**
- **文件：** `cli.py` `_find_tasks_jsonl` / `_e_premise_ids` / `cmd_collect` copy / `cmd_label` 不 copy；`tests/test_round07_regressions.py` L26–36；ISSUES 「Round-10 local close」C6-M-01
- **复现：** §3 CE-3。默认 `prep/col` 路径 copy 成功。孤立 `alpha/beta/gamma` 删除 copy 后 `unique=['p2']` 或 `['p2','p1']`，不是 `task.premises=['p1','p2']`。
- **作者主张 C6-M-01 closed：** **超售。** ISSUES 说已闭，CE 仍失败 → 本条为确认缺陷。

### F10-05 `prefill_hidden=0`/`True`/`[0]` 已拒（点名闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE）。验证现有测试覆盖作者点名集合。
- **作者主张 F6-04：** **本冻结实现同意。** 交卷漂移与此无关。

### F10-06 T3 prepare 不再被 `source_value_pair` 打断（点名闭）

- **严重度：** —
- **状态：** 实现闭合（hotpot/musique/humaneval 独立 prepare exit 0）
- **作者主张 E7-19：** **本冻结实现同意。**

### F10-07 rename 表达式已重写，不再是 `p1 * p2`（点名闭）

- **严重度：** —
- **状态：** 实现闭合
- **作者主张 B5-05：** **本冻结实现同意。**

### F10-08 Plus `gsm8k-1` 锁 Symbolic 到 test（点名闭）

- **严重度：** Medium（验证残留：进程全局锁）
- **状态：** 实现闭合；测试不覆盖「仅 Symbolic」
- **复现：** 单独 Symbolic = `probe_train`；先 Plus 或 siblings = `test`。全局 `_TEST_ONLY_FAMILY_KEYS` 是进程状态。
- **作者主张 B5-01：** **机制同意。** 不是「任意 Symbolic 永远 test」。

### F10-09 analyze 拒绝用 labels 造 P1（点名闭）

- **严重度：** Medium（验证残留）
- **状态：** 实现闭合；`test_analyze_uses_labels_or_stays_null` 仍不读 `p1`
- **作者主张 C7-M-02：** **实现同意。**

### F10-10 `n < min d` 标 truncated（点名闭）

- **严重度：** —
- **状态：** 实现闭合
- **作者主张 C7-M-03：** **本冻结实现同意。**

### F10-11 C7-M-01 测试是 helper；fixture 上 S 空；sham 仍 missing

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）。unit 算术闭合。sham missing 独立见到。
- **作者主张 C7-M-01 vs B6-02：** **部分。** 不得用 helper 绿写成 label 路径已证。

### F10-12 donor / INLP / `ie_z` 测试仍锁名字

- **严重度：** Medium
- **状态：** confirmed defect（验证残留）
- **文件：** `tests/test_round06_regressions.py` L65–74
- **注：** 本轮未把「donor 仍 t0p / INLP 仍 swap」写成实现缺陷；实现侧前轮已部分闭合。测试力度不够。

### F10-13 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：70 / 320 / 159。`06-VERIFICATION.md` 仍写 136 passed。

### F10-14 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes`、`assert_disjoint`、`card`、`apply_model_template`

### F10-15 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个，开审已读）

### F10-16 ISSUES / VERSION 作者关闭高于冻结验证力度

- **严重度：** Medium
- **状态：** confirmed defect（过程）
- **本冻结可作为实现闭合（独立 CE，不是 Goal）：** F6-04 标量 Prefill；E7-19 T3 prepare；B5-05 rename 表达式；B5-01 Plus→Symbolic lock；C7-M-02 假 P1；C7-M-03 truncated；collect 复制 `tasks.jsonl`；review merge；prefix_ids/空 hidden；科学拒 offline H。
- **未闭 / 超售：** C6-M-01 first-seen 残留（F10-04）；e2e offline（F10-03）；强制 `q=`（F10-02）；C7-M-01 label 路径（F10-11）；账本（F10-13）；交卷漂移（F10-00）。
- **不要用本通道把 Goal/需求标 Complete。**

### F10-17 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq = <digit>` **不是** pending_server。first-seen 残留、offline e2e、交卷漂移也不是 pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 70 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F10-13）。C6-M-01 被文件存在填绿（F10-04）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F10-00、F10-03、F10-04 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** 开审 `pytest -q` 确为 153/0。e2e 是 exit-code 烟测并断言空结论（F10-03）。点名项有测试，若干锁替身。交卷磁盘已变。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 仍写 136 passed。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。本文件是审查日志，不改变被审摘要。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：first-seen E、offline 前缀 H、强制 `q=`、目录名 donor、恒 0 的 `g(Y)`。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F10-16）。开审本机 pytest 记录存在（153/0）。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、rename 表达式有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 单元密度在。C7 helper 在；label 路径弱。 |
| 5 划分 | 测试专用不进拟合 | Plus→test、family lock 有。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。fit Y 与 E 在无 tasks 时仍可反。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。CLI 无 task 时回到首次出现序。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。测试锁 transform **名**。offline e2e 是 `unexpressible`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **开审 153 passed，exit 0，20.19s，153 collected。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。 |
| 冻结 | **开审 HASH_MATCH `81308124…`（61）。交卷 HASH_MISMATCH `7518e20b…`（仍 61 文件）。** |
| 独立性 | 真 oracle：标量 Prefill、T3 prepare、rename 表达式、Plus family lock、假 P1、n<d truncated、collect copy、review merge、prefix_ids、科学拒 offline、unit 噪声扣除。**不独立：** C6 文件存在测试、强制 `q=`、offline e2e、`!= pre_step`、donor/INLP/`ie_z` 字段名、C7 helper、analyze 不读 p1。 |
| Mock/stub | offline 前缀 H + helper 自带 task + `prep/` 兄目录 + mode 字符串 + `ie_z_g` 标签 + 教员强制 `q=` + `not_evaluated` 编码为成功。 |
| 论文行为仍未证明 | 无 tasks 时 E/Y 同序、真 Prefill 向量语义之外的 KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT 事件 |
| 交付 vs 测试 | 「153 passed / C6-M-01 已闭 / e2e 已通」**超过** 冻结树测试力度 |
| 已确认问题？ | **是。** Critical：F10-00、F10-03。High：F10-01、F10-04。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。first-seen CE 仍失败而账本写已闭。交卷哈希已漂。Fixture e2e 仍 offline。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。即使 A–E 全写「通过」，两轮计数必须保持 0；修复后换 **新** hash 重开。 |

在声明冻结上用 CE 级测试锁住 **无 `tasks.jsonl` 时拒绝 first-seen**、**e2e 非 offline 前缀 H**、以及 **非强制 `q=` 的科学事件** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。事后改 `measure.py` / 加 r07 两例 **不能**把本轮改写成通过。
