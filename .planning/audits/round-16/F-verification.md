# F：验证质量与反向质疑（round-16）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-16 其他通道报告。开审时的 `ISSUES.md` 只当作者主张。审查窗口内该账本被他方改写成 r17/r18 话术，**不**回写本冻结为已闭。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 在 `%TEMP%\f16_ce_scratch.py` 独立复跑，不把 `tests/test_round07_regressions.py` 当证明。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（61 文件，0 CRLF）。开审后立即 `python -m pytest -q --tb=line` 为 **159 passed / exit 0 / 24.10s**，与作者 `pytest_author_claim: 159` 一致。这不是 Goal 通过。

点名 CE（scratch，不 import 测试文件）：**D14-05** `generate.py`（开审=交卷 `6e604039…`）已无 `cap=48`；`len(prompt_ids)>96` 抛 `ValueError: tiny prompt exceeds context`；source 问句 **整句**进入 `prompt_text`（49 字符，不被 48 截断）。作者开审主张「含完整 `* p2_src`」**失败**：现场题干与 `prompt_text` 均为 `p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?`。开审已读的 `edits.py`（`250055ab…`）本来就是 `src_b`、保留旧叶 `p2`、无 `(alt source)`。**A13-01** 父母改为 `{p1,src_b}`、目标值仍 `0`、与 rename 题干可区分；`_pair_source_value` 选 `(0,3,same_value_diff_source)`。**A13-02 / A13-03 / A12-03 / persist / Prefill / fake P1 / n<d** 独立闭。科学 sham 聚合层仍是弱析取。Fixture 八段仍 offline。

交卷再算为 `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（仍 61，0 CRLF）→ **HASH_MISMATCH**。漂移（本通道未写）：`cli.py`、`edits.py`、`measure.py`、`tests/test_round06_regressions.py`、`tests/test_round07_regressions.py`（后改锁 `src_b`，并加 F15-01 等例）。交卷 collect **162**。`ISSUES.md` 开审写 r16/`5413a4bc…`/`* p2_src`；交卷已改口 r18/`3d0f1c10…` 且删掉 `* p2_src`。事后补丁与新测 **不得**回写本冻结。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` |
| 开审复算 | `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` |
| 中间复算 | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（审查中途；其后 `cli.py` / r06 又变） |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明/开审/交卷都是 **61**。变的是字节，不是个数。 |
| 交卷漂移文件 | `cli.py` `c1a274e233988aad`/1252 → `9431b7768fda6a3c`/1260；`edits.py` `250055ab8257ea2e`/362 → `1e5b97d63a62ab78`/365；`measure.py` `8ec8cf09db149097`/408 → `985b9d9328e4111f`/405；`tests/test_round06_regressions.py` `280f9f71bc27b521`/145 → `b555ed24000400e1`/146；`tests/test_round07_regressions.py` `f942482ffd4b42f5`/302 → `8c23db4b637c8c70`/342。本通道未改。 |
| 冻结仍稳 | `generate.py` `6e6040394ac641c7`/200；`tiny.py` `c75d0f5325766612`/120。D14-05 生产路径按开审字节。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7。`pytest` `pythonpath=["src"]`。`Documents/paper-tracker/src` 在默认 `sys.path` 上但 **无** `reasoning_diff`。独立 CE 的 import 为仓库 `src/`。 |
| pytest | **159 passed in 24.10s，exit 0**（`python -m pytest -q --tb=line`）。跑在开审 MATCH 后、交卷漂移完成前。无 skip/xfail/deselected/`unittest.mock`。 |
| 作者主张 | 开审 `ISSUES.md`：D14-05 / A13-01 / A13-02 / A13-03 / A12-03 / A10-04「local close」。`pytest_author_claim: 159`。当作 Goal / 阶段验收：**否。** |
| 范围 | 开审 61 文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。 |
| 明确未读 | `.planning/audits/round-16/{A,B,C,D,E}-*.md` |
| scratch | `%TEMP%\f16_ce_scratch.py` → `%TEMP%\f16_ce_results.json`。未写入 `src/` / `tests/` / `pyproject.toml`。persist 文件 snapshot/restore。 |

审查对象首先是**声明冻结字节**。`generate.py` / 开审 `edits.py` 在 MATCH 时已读。pytest 按开审盘记载。点名 CE 在 live import 上执行；A13-01/02/03 的 `edits.py`/`measure.py` 交卷已漂，第二次读到的函数体与开审 `src_b` 故事一致，**不**把交卷新测写成冻结已闭。

## 2. 逐文件覆盖

以下行数 / SHA-256 前 16 除另行标明外，是 **开审 HASH_MATCH** 时的 61 文件。

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
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；analyze labels **不锁 p1**；`n≥d` eye 侧 `truncated is False` |
| `tests/test_round06_regressions.py` | **145（开审）** | `280f9f71bc27b521…` | donor/INLP/`ie_z` 字段名；C6 helper；prefix_ids 拒；sham 析取。**交卷 146 行 / `b555ed24…`，不是冻结。** |
| `tests/test_round07_regressions.py` | **302（开审）** | `f942482ffd4b42f5…` | 见 §3 / §6。含 A12-03、Prefill、假 P1、n<d、未知不进 M、sham 空 N、科学 sham **弱析取**。开审读到的 D14-05 例锁 `* p2_src` / `(alt source)`。**交卷 342 行 / `8c23db4b…`，改锁 `src_b` 并加 F15-01 / A14-04 例，不是冻结。** |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

开审 pytest **159 passed**。交卷 collect **162 nodes**（+`test_observed_real_noise_ref_without_sham_does_not_book_empty_n` + `test_load_source_value_pair_does_not_walk_sibling_prep` + `test_intervene_pairs_source_without_prep_sibling_name`）。零 `skip` / `xfail` / `skipif` / `unittest.mock`。恒真：`test_tiny_hooks.py` L17 `assert layer.__class__.forward`。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。`assert True` 两处均为执行器载荷，不是恒真断言。

### 2.2 生产相对测试（开审冻结）

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | 泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | `attention_mean`/`rollout` 无数值 oracle |
| `cli.py` | 1252 | `c1a274e233988aad…` | smoke offline；scientific prepare/collect/fit；T3 prepare；无 tasks **raise**；A12-03 不绑祖先 `col/` | `_load_source_value_pair` 开审仍搜兄 `prep/`；analyze 只认 `p1_table.jsonl`。**交卷 1260 / `9431b776…`，只读给定目录 `edits.jsonl`，不是冻结。** |
| `edits.py` | 362 | `250055ab8257ea2e…` | value/rename/source-value | 开审已是 `new_id="src_b"`、保留 `p2`、无 `(alt source)`。**交卷 365 行，不是冻结。** |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 硬编码 `"generated"` |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；**`ie_z` helper 仍是均值差** | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 408 | `8ec8cf09db149097…` | 事件均值；未知不进 M；sham 不广播 | `c7_m01` 手填 `noise_set`。**交卷 405 行，不是冻结。** |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | 200 | `6e6040394ac641c7…` | 无 48 帽；`>96` raise；`prompt_text` 整句 | 科学事件仍是教员强制 `q=` |
| `models/tiny.py` | 120 | `c75d0f5325766612…` | hook 清理；`max_position_embeddings=128` | last-token / `once=True` 未断言 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 1 字符 1 token；跨界 `[]` | — |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]` | CLI 无 task 现 raise（独立见） |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | 标量/`bool`/`[0]` Prefill 拒 | `[0.0,1.0]` 仍 True（合法向量） |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 184 | `40ab4021d4dccc6e…` | Plus→test；族锁；persist JSON | `assert_disjoint` **零测试** |
| `tasks/catalog.py` | 45 | `bcc83ec636ad207b…` | musique / t4 别名 | `card` 无 |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | 合法配置 | 拒 ops/mod |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12 | `shared_rng_excluded` 硬编码 |
| `tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f…` | family / `register_test_only_family` | — |
| `tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354…` | sidecar；`shared_gsm_*` | — |
| `tasks/t2_noop.py` | 100 | `850f779c81d56149…` | 前插 span | `answer_unchanged_proven` 未断言 |
| `tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb…` | support≠DAG；prepare 不崩 | — |
| `tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7…` | family；spy | 默认无隔离真执行 |
| `tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0…` | pair ids；prepare 不崩 | — |
| `tasks/t4_boundary.py` | 51 | `e4b34f3697825f88…` | 集合相等 | 非法 status |
| `transfer.py` | 86 | `5549f84bd1bd6240…` | 4096/3584 拒；`n<d` truncated | `apply_map` 数值恢复未锁 |

另有 `models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 计入 61。夹具 JSON **不在冻结内**。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `5413a4bc…e661fc`（61，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 交卷再算 | 同脚本 | **HASH_MISMATCH** `3d0f1c10…b7c0952f`。5 文件字节在开审后改变。 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **159 passed in 24.10s，exit 0**。无 skip/xfail/deselected。**开审盘。** |
| Collect | `python -m pytest --collect-only -q` | 交卷盘 **162**（不是冻结）。 |
| skip/xfail/`assert True` | 对 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| **独立 CE** | `%TEMP%\f16_ce_scratch.py` | 见下。未写入仓库。 |

### 3.1 作者点名 CE — 独立复跑（不信测试文件）

| CE | 独立结果 | 作者测试是否锁住 |
|---|---|---|
| **D14-05** 全题干 / 拒截断 | **部分。** `generate.py` 无 `cap=48`。`len(ids)>96` **raise**。source `prompt_text` == 整句，`prompt_len=49`，`truncated_at_48 is False`。**`* p2_src` 不在题干。** 现场为 `* src_b`。49>48，旧帽会切掉末尾。 | 开审 r07 例锁 `* p2_src`（与开审 `edits.py` 的 `src_b` 对不上）。交卷改锁 `* src_b`，**不是冻结。** |
| **A13-01** alt-source + donor | **图：是（src_b 语义）。作者 `p2_src`/`(alt source)`：否。** `parents=['p1','src_b']`，答案仍 `0`，保留叶 `p2`，`expr=p1 * src_b`。rename 对照为 `p2_src = 0.` / `p1 * p2_src`，**无** `(alt source)`。`_pair_source_value` → `(0,3,same_value_diff_source)`。CLI intervene 在 collect **未**带 `edits.jsonl`、目录也不叫 `prep/` 时 `donor_kind is None`（开审 `_load_source_value_pair` 只靠兄名 `prep/`）。 | 开审锁 `p2_src`。交卷改锁 `src_b` + collect 复制 edits。**不是冻结关闭。** |
| **A13-02** 未知不进 \(M\) | **是。** `behavior_known is False`；`M=[]`；`rho_M_raw is None`；`behavior_unknown is True`。 | 开审 `test_unknown_behavior_is_not_counted_as_m` 锁这组。 |
| **A13-03** `sham:` 空 \(N\) | **是。** `sham:q` 的 `noise_ref=0.0`；真实前提 `None`；`rho_M_excess`/`rho_M_noise` 皆 None。changed sham 不广播到 p1/p2。 | 开审 `test_sham_no_change_*` 锁。科学 CLI 仍弱析取。 |
| **A12-03** 祖先 `col/` WRONG-TASK | **是。** `_find_tasks_jsonl(feat, labs) is None`；fit `ValueError: fit requires tasks.jsonl…`；`E(real)=[p1,p2]` ≠ `E(swapped)=[p2,p1]`。兄 `prep/`、真祖先 `anc4/tasks.jsonl` 同样 None。给定目录自己的 `tasks.jsonl` 仍绑定。collect 复制；label 不复制。 | 锁祖先 `col/` + fit raise。**不锁**兄 `prep/`、真祖先、calibrate。 |
| **persist** Plus→Symbolic | **是。** 清 persist+RAM 后孤立 Symbolic = `probe_train`。load Plus 后 RAM `.clear()` 仍 `test`。新进程 RAM=`[]`、磁盘锁在 → `test`。wipe 后新进程孤立 = `probe_train`。 | 锁 RAM `.clear()`。**不锁**新进程、「从未 Plus」。 |
| **Prefill** | **是。** `0/True/False/1.0/[0]/[]/[0.0]/[0.0,0.0]/"0"/None/np.array(0)/[[1]]` → `refilled_prefix False` / `prefill_unavailable`。`[0.0,1.0]` True。`prefix_token_ids` False。 | 作者测 0/True/1.0/[0]/[]。 |
| **fake P1** | **是。** 仅 labels → `p1 is None`。塞 `length/op/rho/y/held_out` 仍 `p1 is None`。有 `p1_table.jsonl` 则出现 `auc_full`/`delta_auc` 等键。 | 锁弱标签。**不锁**塞协变量。 |
| **n<d** | **是。** `(2,5)` vs `(2,3)` → `truncated=True` / `not_applicable_too_few_rows` / `common_dim=3`。`eye(4)` vs `eye(3)` → False。 | 锁 n=2 例。 |
| T3 prepare | hotpot/musique/humaneval/t4 **exit 0**，edits kind = `document`/`paragraph`/`input_list`/`t4_question`，无 `source_value_pair`。 | 锁 hotpot/musique。**Humaneval/t4 未进该测试。** |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **D14-05 作者字符串 `* p2_src`** | 开审 ISSUES / `VERSION.md` prior 写「丢掉 `* p2_src?` / 含完整 `* p2_src`」。独立 `prompt_text` 只有 `* src_b`。把「不再 48 截断」写成「`* p2_src` 已闭」是账本超称。交卷 ISSUES 删掉该串、改口 A14-02，是审查中改账本，不是本冻结关闭。 |
| **科学 sham 弱析取** | `test_scientific_sham_does_not_book_rho_m_excess_one`：`rho_M_excess != 1.0 or null_reason`。独立：聚合层 `excess is None` 且 `null_reason is None` → 因 `None != 1.0` **仍绿**。事件层才是 `noise_set_missing`。 |
| **r06 sham 析取** | `rho_S_noise is None or null_reason in {noise_set_missing, sham_protocol_missing}`。 |
| **教员强制 `q=`** | scientific prepare 7 条轨迹事件全是 `['q']`，`assigned` 为 `\nq = 82/53`，`parse_status=constrained_target`。`any(q)` + `parse_region` 被这条强制行单独满足。 |
| **offline H 当 e2e** | 八段 exit 0。`H=[[1..8]]`，无 `H_pre_step`，intervene `unexpressible`/`donor_missing`，analyze `p1 is None`。 |
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + probes 文件。不比 Y 列与 `task.premises`。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set=["p3"]`。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 末 token 有限 H 也会绿。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| 科学 prepare sham=1 | exit 0。source 问句 `* src_b`，`prompt_len=49`。真实前提 `noise_ref` None。聚合弱 or 仍绿。 |
| fixture e2e | **仍是 offline 前缀 H。不要写成端到端科学已通。** |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：`python -m pytest -q` **70**；`passed_local_tests` **320**；`tests_exist_not_acceptance` **159**。页眉写不得用 pytest 关可执行行；协议行仍用 pytest 关闭。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed**（作者本冻结称 159）。开审 ISSUES 的 `* p2_src` 在独立 CE 上 **失败**。交卷 ISSUES 改口 r18，不接受为关闭。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-16 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 对交卷 61 文件套件重跑 pytest 当冻结证据 | 那已不是声明 hash。开审 159 不得写成「当前树」。交卷 collect 162。 |
| 用完整 Task 再跑恰好 96 token 的 generate | scratch 哑对象缺 `premises`；`>96` raise 已在真 `ValueError` 上见到。不是生产缺陷。 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 159 passed | `VERSION.md` | **开审命令是。** 当作 Goal / 冻结交卷证据：**否。** |
| D14-05：不再 48 截断；超上下文拒绝；`* p2_src` | 开审 ISSUES / VERSION prior | **截断/raise：独立 CE 是（`generate.py` 未漂）。`* p2_src`：独立 CE 否。** 账本超称。 |
| A13-01：`apply_alt_source_same_value`；intervene 优先 `trace-source` | 开审 ISSUES | **函数存在、父母变、保值、helper 选 source：是。** 不是 rename-only。**不是** r15 叙事里的 `p2_src`/`(alt source)`/丢掉旧叶。CLI 无 edits 副本时 `donor_kind` 可空。 |
| A13-02 / A13-03 / A12-03 / A10-04 | 开审 ISSUES | **独立 CE 是。** 不是 Goal。 |
| Prefill / fake P1 / n<d | 既有 ISSUES / r07 | **独立 CE 是。** |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。 |

**账本超称：** 开审点名「D14-05 已闭且 `prompt_text` 含 `* p2_src`」在独立 CE 上 **失败**。这是「声称已闭但 CE 仍红」的超称。A13-02/03、A12-03、persist、Prefill、假 P1、n<d、D14-05 的「无 48 帽 / raise」**没有**实现 CE 失败。交卷把 ISSUES 改成 A14-02/`src_b`、删 `* p2_src`，是改账本不是复核关闭。弱析取 / offline e2e / pytest 关协议行仍在。

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3 事件均值；空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离（源级）；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击失败 = 实现侧闭合（部分测试仍可能是替身）：**

- **D14-05 无 48 截断 / `>96` raise。** 改回 `prompt_ids[:48]` 会让独立 CE 红（source 49 字符）。把 raise 改成静默截断，超长题会绿。
- **A13-01 父母必须变、目标值不变、helper 先 source。** 改回 rename-only 或先 value-edit，helper CE 红。**钉死 `* p2_src` 不会红**——实现写的是 `src_b`。
- **A13-02 未知 → M 空。** 把未知行算进 M 会红。
- **A13-03 sham 空 N 不扣噪 / 不广播。** 给 p1/p2 写 `noise_ref=1.0` 会红。
- **A12-03 祖先 `col/` 不绑定。** 改回 4 层 extras 会红。
- **Plus persist：RAM `.clear()` 与新进程仍 test。**
- **标量 Prefill 不是 Prefill。**
- **labels 不能造 P1**（独立含塞协变量）。
- **`n < d` 必须 truncated。**

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| 开审 `test_source_value_pair_rewrites_graph_ids`（`p2_src`） | 与开审 `edits.py` 的 `src_b` 不一致。不能同时当「159 绿」和「冻结锁住 `* p2_src`」。 |
| 交卷同名例（`src_b`） | **不在声明冻结。** 是实现后改锁。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `!= 1.0 or null_reason`。聚合层两键皆 None 也绿。 |
| `test_sham_hits_do_not_book_evaluated_zero_noise` | `rho_S_noise is None or null_reason in {…}`。 |
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + probes。不比列序。 |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手填 `noise_set`。 |
| `test_analyze_refuses_fake_p1_from_labels` | 不塞 P1 协变量。实现比测试紧。 |
| `test_t3_prepare_survives_source_value_pair` | 无 humaneval。 |
| `test_plus_locks_symbolic_family_to_test` | 不锁新进程；不锁「从未 Plus」。 |
| `test_generated_events_*` / scientific prepare `any(q)` | 教员强制 `\nq = 82` 单独满足。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 末 token 有限 H 也会绿。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_tiny_hooks` L17 | 恒真。 |
| 交卷 `test_load_source_value_pair_*` / `test_intervene_pairs_source_*` / `test_observed_real_noise_ref_*` | **不在声明冻结。** |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`[1..8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。
2. **科学事件非空，来源是教员强制 `q=`。** `parse_region` 硬编码 `"generated"`。
3. **步前 H 用有限行数冒充「不是末 token」。**
4. **科学 sham 测试用弱析取盖住「聚合层没有 `null_reason`」。**
5. **账本协议行仍 pytest；可执行行 `tests_exist_not_acceptance`。**
6. **D14-05 用「不再截断」话术盖住「题干已不是 `p2_src`」。** 交卷再改 ISSUES / 测试对齐 `src_b`。
7. **Plus 锁依赖摘要外 JSON。**
8. **开审 `_load_source_value_pair` 靠兄目录名 `prep/`。** 目录不叫这个且 collect 不复制 edits 时，CLI donor 静默空。

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes` 数值恢复、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内已执行。本通道未加测试。

### CE-1 D14-05 全题干 / 拒 48 截断（实现部分闭；作者字符串失败）

```text
make_source_value_pair(t1_tiny, p2, "2").same_value_diff_source
  question = "p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?"   # 49 chars
generate_task_trace(...):
  prompt_text == question
  prompt_len == 49
  "* src_b" in prompt_text
  "* p2_src" not in prompt_text          # 开审 ISSUES / VERSION prior 失败
  prompt != question[:48]

generate.py: no cap=48
len(prompt_ids)>96 → ValueError tiny prompt exceeds context
```

### CE-2 A13-01（src_b 图 + helper 选 source）

```text
apply_alt_source_same_value / make_source_value_pair:
  parents {p1, src_b} ; keeps leaf p2 ; ans 0
  no "(alt source)" ; no p2_src
rename({"p2":"p2_src"}): "p2_src = 0." / p1 * p2_src

scientific collect tiny:
  _pair_source_value → (0, 3, same_value_diff_source)
CLI intervene on sci_col without edits.jsonl:
  donor_kind is None                    # 开审兄名 prep/ 才救命
```

### CE-3 A13-02 / A13-03 / A12-03 / persist / Prefill / fake P1 / n<d

```text
unknown no_change non-exhaustive → M=[] ; rho_M_raw=None ; behavior_unknown
sham:q no_change + proto hits=[] → noise_ref 0 only on sham:q ; excess/noise None
ancestor col WRONG-TASK → _find None ; fit ValueError
Plus persist: RAM clear + new process = test ; never-Plus = probe_train
0/True/[0]/prefix_ids → prefill_unavailable ; [0.0,1.0] True
labels ± covariates → p1 is None ; p1_table → auc keys
(2,5) vs (2,3) truncated True
```

### CE-4 弱析取 / 教员 `q=` / offline e2e

```text
scientific prepare sham=1:
  agg: rho_M_excess is None ; null_reason is None
  author: excess != 1.0 or null_reason  → 绿
  events: null_reason=noise_set_missing

generate_task_trace / sci traces:
  events=['q'] ; assigned='\nq = 82|53' ; constrained_target

fixture collect --backend offline:
  H=[[1..8]] ; no H_pre_step
  intervene unexpressible / donor_missing
  analyze lab: p1 is None
```

## 9. 发现

### F16-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）
- **文件：** `.planning/audits/round-16/VERSION.md` L5–23；开审 61 = `5413a4bc…`；交卷 61 = `3d0f1c10…`
- **复现：** 开审脚本原文 MATCH。审查期间 5 文件被改（本通道未写）：`cli.py`（`_load_source_value_pair` 不再走兄 `prep/`）、`edits.py`、`measure.py`、`test_round06_regressions.py`、`test_round07_regressions.py`（改锁 `src_b` + 3 新例）。中间哈希 `3d0a0764…` 也已不是声明冻结。事后补丁不能回写本冻结为已闭。
- **注：** 只要本通道提交已确认缺陷，连续通过计数不能开始。

### F16-01 绿 159 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** 开审 `159 passed / 0`。作者 claim 与该命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 是 offline 烟测。交卷已是另一 hash / 162 collect。

### F16-02 D14-05：无 48 截断与 raise 已闭；作者 `* p2_src` 超称

- **严重度：** High（账本）/ 实现部分闭
- **状态：** confirmed defect（ledger overclaim）。截断路径 **实现闭合**（`generate.py` 开审=交卷）。
- **文件：** 开审 ISSUES D14-05；`VERSION.md` L27；`generate.py` L122–125；开审 `edits.py` L219–292
- **复现：** §3 CE-1。`prompt_text` 含 `* src_b` 不含 `* p2_src`。开审 `edits.py`（与 r15 同哈希 `250055ab…`）本来就写 `src_b`。
- **作者主张 D14-05 closed：** **部分。** 「不再截断 / 超上下文拒绝」同意。「含完整 `* p2_src`」**不同意。**

### F16-03 科学事件测试仍接受教员强制 `q=`

- **严重度：** Medium
- **状态：** confirmed defect（验证替身）
- **复现：** §3 CE-4。7/7 轨迹 `events=['q']`，`\\nq = 82|53`。

### F16-04 Fixture e2e 仍 offline；analyze 常无 `p1_table`

- **严重度：** Critical（验证）
- **状态：** confirmed defect（验证）
- **复现：** `H=[[1..8]]`，intervene `unexpressible`/`donor_missing`，`p1 is None`。不要写成端到端科学已通。

### F16-05 A13-01：src_b 图与 helper 选 source 已闭；`p2_src`/`(alt source)` 不是本冻结

- **严重度：** Medium（账本 / CLI 残留）
- **状态：** 实现部分闭合（独立 CE）。作者 `p2_src` 叙事 **不** 闭合。
- **复现：** §3 CE-2。CLI 无 edits 副本时 `donor_kind is None`。交卷改为 collect 复制 + 只读 in-dir，**不是冻结。**

### F16-06 A13-02 / A13-03 点名闭

- **状态：** 实现闭合（独立 CE）
- **作者主张：** **实现同意。** 科学 sham 测试仍是弱析取（F16-10）。

### F16-07 A12-03：祖先 `col/` WRONG-TASK 已拒

- **状态：** 实现闭合（独立 CE，含兄 `prep/` / 真祖先）
- **作者主张 A12-03 closed：** **实现同意。** 作者未锁兄目录与 calibrate。

### F16-08 A10-04 persist：RAM `.clear()` 与新进程后仍锁

- **状态：** 实现闭合（独立 CE）。孤立从未 Plus = `probe_train` **不是**残留缺陷。
- **作者主张 A10-04 closed：** **实现同意。** persist JSON 不在 61 摘要内。

### F16-09 Prefill / fake P1 / n<d 点名闭

- **状态：** 实现闭合（独立 CE，含塞协变量与合法 2-d 向量）
- **作者主张：** **实现同意。**

### F16-10 科学 sham 测试仍是弱析取

- **严重度：** Medium（验证残留）
- **状态：** confirmed defect（验证）
- **文件：** 开审 `tests/test_round07_regressions.py` L241；`tests/test_round06_regressions.py` L114
- **复现：** 聚合层 `null_reason is None` 且 `excess is None` 仍绿。

### F16-11 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：70 / 320 / 159。`06-VERIFICATION.md` 仍写 136 passed。

### F16-12 审查窗口内 ISSUES / 测试改口，不得回写本冻结

- **严重度：** High（过程）
- **状态：** confirmed defect（账本协议）
- **复现：** 开审 ISSUES 为 r16 / `5413a4bc…` / `* p2_src`。交卷 ISSUES 为 r18 / `3d0f1c10…` / A14-02 `src_b`，D14-05 不再提 `p2_src`。r07 测试从锁 `p2_src` 改为锁 `src_b`。这是目标后移，不是独立关闭。

### F16-13 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes` 数值恢复、`assert_disjoint`、`card`、`apply_model_template`

### F16-14 夹具与 persist 排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个）；`.planning/research/.cache/gsm_test_only_families.json`

### F16-15 真模型 / 官方全量 / 隔离 Linux runner

- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `q = <digit>` **不是** pending_server。交卷漂移也不是 pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 70 行仍 `pytest -q`；320 行仍 `passed_local_tests`（F16-11）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F16-00、F16-02、F16-04 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** 开审 159/0。e2e 是 exit-code 烟测并断言空结论（F16-04）。D14-05 字符串 CE 失败。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 仍写 136 passed。ISSUES 审查中改口。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。修复后须对新 hash 重开连续计数。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：offline 前缀 H、强制 `q=`、`* p2_src` 超称。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪**（F16-02、F16-12）。开审本机 pytest 记录不能挂到交卷 hash。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语有。source 臂是 `src_b` 加叶，不是 `p2_src` 换叶。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 生成区只有强制 `q`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 未知不进 M、sham 不广播独立闭；科学 CLI 测试弱。 |
| 5 划分 | 测试专用不进拟合 | Plus→test 有。persist RAM-clear / 新进程独立闭。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。无 tasks 时 fit 现拒绝 first-seen。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。CLI 无 task 现 raise。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | helper 可优先 source。CLI 依赖 edits 是否在 in-dir。offline e2e 是 `unexpressible`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **159 passed，exit 0，24.10s（开审盘）。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。**不是**交卷 hash 上的记录。 |
| 冻结 | **开审 HASH_MATCH `5413a4bc…`（61）。交卷 HASH_MISMATCH `3d0f1c10…`（仍 61）。** |
| 独立性 | 真 oracle：无 48 截断 / `>96` raise；source 整句 `prompt_text`；A13-01 helper 选 source；A13-02/03；A12-03（含兄/祖先）；persist RAM+新进程；Prefill；假 P1（含塞协变量）；n<d。**失败 / 不独立：** 作者 `* p2_src`；科学 sham 弱析取；强制 `q=`；offline e2e；开审 r07 锁 `p2_src` 与开审 `edits.py` 不一致。 |
| Mock/stub | offline 前缀 H + 教员强制 `q=` + 弱析取 + 摘要外 persist JSON + 审查中改账本/改锁。 |
| 论文行为仍未证明 | 真 Prefill 向量语义之外的 KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT 事件、非 offline 的 e2e H、`p2_src` 来源臂 |
| 交付 vs 测试 | 「159 passed / D14-05 含 `* p2_src` / e2e 已通」**超过** 冻结树测试力度。D14-05 字符串是「称已闭但 CE 失败」。其余点名实现独立同意，不能写成 Goal。 |
| 已确认问题？ | **是。** Critical：F16-00、F16-04。High：F16-01、F16-02、F16-12。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。交卷哈希已漂。作者 `* p2_src` CE 失败。Fixture e2e 仍 offline。点名实现部分闭合 **不** 使本通道通过。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。即使 A–E 全写「通过」，两轮计数必须保持 0；修复后换 **新** hash 重开。 |

在声明冻结上用 CE 级测试锁住 **e2e 非 offline 前缀 H**、**非强制 `q=` 的科学事件**、**科学 sham 的事件层 `null_reason`（禁止弱析取）**、以及 **与实现一致且与账本一致的 source 题干（禁止一边写 `* p2_src` 一边交 `src_b`）** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。事后改 `cli.py` / `edits.py` / `measure.py` / r07 新例 / ISSUES 改口 r18 **不能**把本轮改写成通过。D14-05 的无截断/raise 与 A13-02/03、A12-03、persist、Prefill、假 P1、n<d 记在 F16-02 的实现半边与 F16-06…09，不是通道通过。
