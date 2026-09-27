# F：验证质量与反向质疑（round-15）

独立审查通道 F。未改生产树、测试与 `pyproject.toml`。未读 round-15 其他通道报告。`ISSUES.md` 只当作者主张。绿 pytest 不是论文正确性，也不是 Goal 验收。点名 CE 在进程内与新进程独立复跑，不把 `tests/test_round07_regressions.py` 当证明。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结哈希 **一致（HASH_MATCH）** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（61 文件，0 CRLF）。交卷再算为 `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（仍 61 文件）→ **HASH_MISMATCH**。漂移文件 mtime 在开审与独立 CE 之后：`src/reasoning_diff/models/tiny.py`（02:51:18）、`src/reasoning_diff/models/generate.py`（02:51:19）、`tests/test_round07_regressions.py`（02:51:20）。本通道未改这三文件。本机 `python -m pytest -q --tb=line` 为 **159 passed / exit 0 / 21.50s**，发生在漂移之前，**不能**写成交卷盘上的 159。这不是 Goal 通过。

开审冻结上独立 CE：A13-01 **图重写闭**（`(alt source)`、目标值不变、父母 `{p1,p2}→{p1,p2_src}`）；**生成路径未闭**——`generate_task_trace` 把 57 字 alt-source 题干静默截到 48，`trace-source` 的 `prompt_text` 变成 `…What is q = p1 `，丢掉 `* p2_src?`。`_pair_source_value` 在有 pair_meta 时优先 `same_value_diff_source`；CLI collect→intervene 只在兄目录名叫 `prep`/`prepare` 或 collect 自带 `edits.jsonl` 时才加载该 meta，独立目录名落到 `same_identity_fallback`。A13-02（未知 / \(T\) 未覆盖 → \(M=\emptyset\)，`rho_M_*=null`）、A13-03（\(T\) 已覆盖 + `sham:` no-change → `null_reason=noise_set_missing`，不把空 \(N\) 当已评估）、A12-03（`_find_tasks_jsonl` 只读传入目录）、persist（RAM clear + 新进程）、假 P1、Prefill、`n<d` **实现闭**。作者 A13-03 测试与 A13-02 混杂；科学 sham 与若干噪声断言仍是弱析取。Fixture 八段仍是 offline：`H=[[1..8]]`，intervene `unexpressible`/`donor_missing`。科学事件仍只有教员强制 `\nq = <digit>`。账本协议行仍用 pytest 关闭。ISSUES 对 A13-01「intervene 优先 trace-source」在 collect 产物上 **超售**。本通道 **不通过**，**不宣布 Goal 完成**。停止条件第 5 条：**不能开始**连续通过。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务 | Independent Reviewer F / 验证质量与反向质疑 |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声明冻结 | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` |
| 开审复算 | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` |
| 开审裁决 | **HASH_MATCH**（61 文件，0 CRLF） |
| 交卷复算 | `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` |
| 交卷裁决 | **HASH_MISMATCH**（交卷对象不是声明冻结） |
| 哈希方法 | `VERSION.md` 脚本原文：`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（不含 `__pycache__`）。POSIX `relpath` + `NUL` + bytes。 |
| 文件数 | 声明 / 开审 / 交卷都是 **61**。变的是字节，不是个数。 |
| 交卷漂移文件 | `tiny.py` 02:51:18（`c75d0f53…`，`clone_cache` 多拷属性）；`generate.py` 02:51:19（`6e604039…`，`>96` 拒截断，删 `cap=48`）；`test_round07_regressions.py` 02:51:20（`f942482f…`，加 source prompt 未截断断言）。本通道未改。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；不要把 HEAD 当冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| pytest（声明冻结树） | **159 passed in 21.50s，exit 0。** Collect：**159 nodes**。无 skip/xfail/deselected/`unittest.mock`。`assert True` 只在 HumanEval/`SubprocessExecutor` 载荷字符串。一处未用 `monkeypatch`（`test_p1_held_out_logistic_detects_rho`）。`@pytest.mark.integration`（tiny hooks，2 参数）**实际跑了**。 |
| 作者主张 | `pytest_author_claim: 159 passed`。命令结果在**开审 MATCH 盘**上独立确认。当作 Goal / 阶段验收：**否。** 不能回写为交卷 hash 上的 159。 |
| 范围 | 开审 61 文件 + 测试触及的生产符号。夹具 JSON **不在冻结内**。persist 缓存 `.planning/research/.cache/gsm_test_only_families.json` **不在冻结内**。点名 CE 在开审 MATCH 后、02:51 漂移前跑完。 |
| 明确未读 | `.planning/audits/round-15/{A,B,C,D,E}-*.md` |
| 独立 CE | `%TEMP%\f15_ce_scratch.py` + child subprocess。未写入仓库。 |

审查对象首先是**声明冻结字节**。pytest 与点名 CE 在开审 MATCH 后、交卷漂移前执行。交卷哈希已漂。

## 2. 逐文件覆盖

以下行数 / SHA-256 前 16 是 **开审 HASH_MATCH** 时的 61 文件。交卷三文件已标出。

### 2.1 测试（全部读完）

| 文件 | 行数 | SHA-256（前 16） | 实际锁住的行为 |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest；**无** `success_count` |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003b…` | 八阶段 exit 0 + `scientific_conclusion is None` + Gate `unregistered`；collect 仍 `--backend offline`；**不读 p1 / H 来源** |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator 重放 + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | 集合密度、联合 `f=xy`、锥来源字符串 |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087…` | r01/r02 oracle；默认 P1 门；pipeline 到 fit（offline H） |
| `tests/test_round03_regressions.py` | 292 | `61247e8a074944a3…` | r03 节点；P1 泄漏用例仍绿；`ie_z` 单元仍是隐均值 helper |
| `tests/test_round04_regressions.py` | 311 | `25949c80bbb55585…` | r04 节点；offline 几何仍只 `!= pre_step`；`noise_set=[]` 已评估 0；bootstrap 只查非空 |
| `tests/test_round05_regressions.py` | 197 | `bc837c0c3a6ea3ae…` | H `isfinite`；科学 intervene `!= donor_missing`；仍不比 last-token；analyze labels **不锁 p1** |
| `tests/test_round06_regressions.py` | 145 | `280f9f71bc27b521…` | `donor_kind==same_value_diff_source` **在 prep/col 名下**；INLP/`ie_z_g` 字段名；C6 helper；prefix_ids 拒；sham 析取 |
| `tests/test_round07_regressions.py` | **296（开审）** | `e8ba9102…`（开审） | 15 例。祖先 `col/tasks.jsonl` 拒；alt-source 图重写；未知 → \(M=\emptyset\)；sham no-change **不查 `null_reason`**；科学 sham 弱析取；假 P1 不塞协变量；Plus 同进程 persist。交卷加 generate 未截断断言，**不是冻结证据**。 |
| `tests/test_science.py` | 103 | `cdb5f1460502ba3c…` | conformal 形状、transfer **形状**、Week8 未注册、`prefix_token_ids` 锁 False |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | 官方形状/mod23/答案 12 |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8；Plus `fit_eligible`/`role`；**不** `clear_test_only_families` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot 旗标；HumanEval spy + `exec(` 拒 |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache 变异；`cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook 清理；L17 恒真 |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare、身份、密度、TO |
| `tests/fixtures/*.json` | 10 个 | **不在冻结内** | 手写 oracle |

Collect-only（开审盘）：**159 nodes**。零 `skip` / `xfail` / `skipif` / `unittest.mock`。`tiny_hooks` 2 参数 + 其余函数 = 159。恒真：`assert layer.__class__.forward`（`tests/test_tiny_hooks.py` L17）。未使用的 `monkeypatch`：`test_p1_held_out_logistic_detects_rho`。

相对 r13（156 / `test_round07` 12 例）：本冻结 `test_round07` 为 15 例（加祖先 tasks 拒、未知不进 \(M\)、sham no-change）。

### 2.2 生产相对测试

| 文件 | 行 | SHA-256（前 16） | 测试触及 | 未测或只被替身碰到 |
|---|---:|---|---|---|
| `__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` | argv/`SystemExit` |
| `analysis.py` | 337 | `e4368b0a386da63b…` | P1 门、ρ 探测、噪声 `lo<hi`、Week8 | r04 常数 δ 仍可能退化；泄漏 `ρ=y` 仍绿 |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest | `success_count` 未断言 |
| `baselines.py` | 125 | `3d7ec3ba60f894b4…` | verbalizer 17/70/boxed | `attention_mean`/`rollout` 无数值 oracle |
| `cli.py` | 1252 | `c1a274e233988aad…` | smoke offline；scientific prepare/collect/fit/intervene；T3 prepare；孤立 fit 拒；A12-03 祖先拒 | `_load_source_value_pair` 仍走兄 `prep/`；analyze 只认 `p1_table.jsonl` |
| `edits.py` | 362 | `250055ab8257ea2e…` | value/rename/alt-source 图重写 | 生成路径截断未锁（开审） |
| `events.py` | 274 | `290a4fd676ac0814…` | 身份；`merge_review`；generate 只解析 generated | `parse_region` 是常量 |
| `executor.py` | 109 | `481d6ed597c93e78…` | spy；`isolated_sandbox is False` | 宿主 subprocess ≠ 沙箱 |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors | 空 complete 拒 |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap/INLP 公式/范数；**`ie_z` helper 仍是均值差** | — |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | 坏 JSONL 行 |
| `measure.py` | 408 | `8ec8cf09db149097…` | 未知 \(M\)；sham 行 → `noise_set=None`；unit 噪声扣除 | 科学聚合层不抄 `null_reason`；C7 helper 不走 labels |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **零测试** | `card` / `load_frozen` |
| `models/collect.py` | 261 | `83658cd8ba879f20…` | 有限 H；`mode=inlp`/`add_delta`/`replace` | 测试不比 last-token |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 / D-08 | — |
| `models/generate.py` | **201（开审）** | `07493570…`（开审） | `start>=len(prompt)` | **`cap=48` 静默截断**。交卷改拒截断，不是冻结。 |
| `models/tiny.py` | **120（开审）** | `21725a18…`（开审） | hook 清理 + logits 变 | 交卷 `clone_cache` 多属性，不是冻结 |
| `models/tokenize.py` | 31 | `b0cc8974af1010fa…` | 跨界 `[]`；n=2 拒 | 一字一 token，48 cap = 48 字符 |
| `probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec…` | σ / λ_FN；NaN 掩码 | CLI 双头 |
| `probes/boundary.py` | 44 | `ce3b549be7d671ff…` | 符号 | Hidden=256 / ReLU 仍弱 |
| `probes/calibrate.py` | 45 | `e8b3ed3459bb22c5…` | `[0.7,0.4]`；helper 上的 `truth_indices` | — |
| `repair.py` | 232 | `f76ff9998b9a6b17…` | `_hidden_is_prefill` 拒标量/`bool`/`[0]` | `[0.0,1.0]` 仍 True（合法向量，不是缺陷） |
| `rng.py` | 53 | `2098c2c72a852eaa…` | 两标量不等 | snapshot/restore |
| `schema.py` | 385 | `57c69c6f58cc9a45…` | 枚举、身份不含值 | extras |
| `scoring.py` | 30 | `8a7a3c0777240122…` | code via spy | `score_qa` **零测试** |
| `splits.py` | 184 | `40ab4021d4dccc6e…` | Plus→test；RAM∪磁盘并集；`clear` 删文件 | `assert_disjoint` **零测试**；作者测试不 spawn 新进程 |
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

夹具 JSON **不在冻结内**。`models/__init__.py` / `probes/__init__.py` / `tasks/__init__.py` 仅包说明。

## 3. 已做检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 开审冻结哈希 | `VERSION.md` 脚本原文 | **HASH_MATCH** `401e509b…de88f716`（61 文件，POSIX relpath + NUL + bytes）。0 CRLF。 |
| 交卷再算 | 同脚本 | **HASH_MISMATCH** `5413a4bc…e661fc`。三文件 mtime 02:51:18–20。本通道未改。 |
| 全量 pytest | 仓库根 `python -m pytest -q --tb=line` | **159 passed in 21.50s，exit 0**。无 skip/xfail/deselected。**开审 MATCH 盘。** |
| Collect | `python -m pytest tests --collect-only -q` | 159 nodes，collect exit 0 |
| skip/xfail/`assert True` | 对冻结 `tests/**` 检索 | 无 skip/xfail/mock；恒真 `test_tiny_hooks.py` L17；未用 `monkeypatch` |
| 手算 oracle | iGSM 编辑后 `4*3=12`；sidecar `5+3=8`；TO 0.5；σ(1)；`repairability=0.6`；`[0.7,0.4]` | **存在的单元断言**与独立算术一致 |
| **独立 CE（scratch，不跑测试文件当证明）** | `%TEMP%\f15_ce_scratch.py` + child | 见下。未写入仓库。 |

### 3.1 作者点名 CE — 独立复跑（不信测试文件）

| CE | 独立结果（开审冻结） | 作者测试是否锁住 |
|---|---|---|
| **A13-01 图：`(alt source)` / 值不变 / 父母变** | **闭。** `apply_alt_source_same_value(p2)`：题干含 `(alt source)` 与 `p2_src`；`answer_spec.value` 仍 `0`；父母 `{p1,p2}→{p1,p2_src}`；表达式 `p1 * p2_src`；`kind=same_value_diff_source`。rename 映射父母但不写 `(alt source)`。value 臂答案变为 `8`。 | `test_source_value_pair_rewrites_graph_ids` 锁图。**实现闭。** |
| **A13-01 生成 alt-source 题干** | **未闭。** pair 任务题干 57 字。scientific `trace-source`：`prompt_len=48`，`prompt_text='p1 = 4. p2_src = 0 (alt source). What is q = p1 '`，**丢掉 `* p2_src?`**。`encode_text` 一字一 token；开审 `generate.py` `cap=48` 静默截断。 | **开审无测试。** 交卷才加断言，不能回写本冻结。 |
| **A13-01 intervene 优先 trace-source** | **有 pair_meta 时算法闭。** 两边都与 base 不同 → `(0,2,same_value_diff_source)`；source 与 base allclose → 落到 value 臂。**CLI collect→intervene 不一般闭：** collect **不**复制 `edits.jsonl`；`_load_source_value_pair` 仍搜兄 `prepare`/`prep`/`s-prep`。独立目录名 `sci_prep`/`sci_col` → `donor_kind=same_identity_fallback`。作者布局 `prep`/`col` → `same_value_diff_source`。 | `test_scientific_h_is_finite_and_pairs_donor` **只锁 prep/col 名。** 替身。 |
| **A13-02 未知 / \(T\) 未覆盖 → \(M=\emptyset\)，`rho_M_*=null`** | **闭。** 全未知：`behavior_known=False`，`M=[]`，`rho_M_raw/noise/excess` 皆 None。仅 p1 已知 exhaustive、\(T=\{p1,p2\}\)：**`behavior_unknown=True`，`M=[]`，`rho_M_raw=None`**（不把未覆盖的 p2 记进 \(M\)）。直接 API `behavior_unknown=True` 即使 `noise_set=["p3"]` 仍 null 全部 `rho_M_*`；`False` 时 \(M=\{p1,p2\}\)，`rho_M_raw=1.0`。 | 作者只锁全未知。**不锁 \(T\) 未覆盖。** 独立更强，实现同意。 |
| **A13-03 任意 `sham:`（含 no-change）→ 不把空 \(N\) 当已评估** | **闭（须 \(T\) 已覆盖才能与 A13-02 分离）。** \(T\) 已覆盖 + sham no-change：真实前提 `noise_ref=None`，`sham:q` `noise_ref=0.0`；`behavior_unknown=False`，`rho_M_raw=0.5`，`rho_M_noise/excess=None`，`null_reason=noise_set_missing`。对照：空 \(N\) 已评估会得到 `rho_M_noise=1.0`、`excess=-0.5`。sham hit 同样 `noise_set_missing`。 | 作者 `test_sham_no_change_*` 只有 p2 已知 → **\(T\) 未覆盖，A13-02 已把 `rho_M_*` 置空**，不断言 `null_reason`。科学 CLI 测试是弱析取。 |
| **A12-03 `_find_tasks_jsonl` 只读传入目录** | **闭。** 祖先 `col/WRONG-TASK` 找不到；兄 `prep/` 不再救命；只传入目录自己的 `tasks.jsonl`。孤立 fit/calibrate 皆 `ValueError: … tasks.jsonl`。helper 无 task 仍 first-seen `['p2','p1']`。 | `test_fit_does_not_bind_ancestor_col_tasks` 锁祖先。**不锁兄 prep。** 独立见到兄 prep 已拒。 |
| **persist / A10-04** | **闭。** 从未 Plus 的 `gsm8k-never-plus-f15` = `probe_train`。Plus 后 Symbolic = `test`。RAM `.clear()` 后磁盘仍锁，Symbolic 仍 `test`。**新进程**只 load Symbolic：`role=test`，`ram=[]`，`locked=True`。全清后新进程 = `probe_train`。 | 锁同进程 RAM clear。**不 spawn。** |
| **假 P1** | **闭。** labels 塞 `length/op/rho/y/held_out` → `p1 is None`，`status=not_evaluated`。对照 `p1_table.jsonl` → `p1` 有 `auc_full`/`delta_auc`。 | 锁弱标签。**不塞协变量。** |
| **Prefill `0/True/1.0/[0]/[]`** | **皆 False** / `prefill_unavailable`。另：`False`/`[0.0]`/`[0.0,0.0]`/`"0"`/`None`/`np.array(0)`/`[[1]]` False；`[0.0,1.0]` 与 `[[1,2]]` True。`prefix_token_ids` False。 | 作者测 0/True/1.0/[0]/[]。**实现闭。** |
| **`n<d` truncated** | `(2,5)` vs `(2,3)` → `truncated=True` / `not_applicable_too_few_rows`。`eye(4)` vs `eye(3)` → False / `adapted_geometry`。`(1,4)` vs `(1,3)` True。1-D → `not_applicable_shape_mismatch`。`eye(3)` vs `eye(3)` False。 | 锁 n=2 例。**实现闭。** |
| collect 复制 `tasks.jsonl` | **是。** `label` **不**复制。 | 锁存在。 |
| T3 prepare | hotpot/musique/humaneval **exit 0**，kinds `document`/`paragraph`/`input_list`，无 `source_value_pair`。 | 锁 hotpot/musique。Humaneval 独立不崩。 |
| review merge | `awaiting_human` → `filled`/`ok`。 | 锁。 |

### 3.2 点名替身 / 弱析取（现有测试绿、错实现也可绿）

| 替身 | 独立观察 |
|---|---|
| **A13-01 generate 截断** | 开审 `cap=48`。alt-source 57 字被切成 48。作者开审测试不读 `prompt_text`。 |
| **A13-01 donor_kind 目录名** | `prep`/`col` 让 `_load_source_value_pair` 命中兄 `prep/edits.jsonl`。独立名 → `same_identity_fallback`。 |
| **A13-03 作者用例混 A13-02** | 缺 p1 已知 → `behavior_unknown` 已把 `rho_M_*` 置空。空 \(N\) 已评估也会绿。 |
| **`rho_M_excess != 1.0 or null_reason`** | 科学 prepare 事件层 `null_reason=noise_set_missing`，`behavior_unknown=True`。聚合层 **不抄** `null_reason`（`None`），`excess` 也是 `None`。`None != 1.0` 单独过。错实现若写 `excess=1.0` 且任意 `null_reason` 仍绿。 |
| **`null_reason in {…} or rho_M_noise is None`** | `noise is None` 单独过。 |
| **`rho_S_noise is None or null_reason in {…}`** | r06 析取仍在。 |
| **`null_reason != noise_set_empty or rho_S_excess is not None`** | r04 析取仍在。 |
| **教员强制 `q=` 当唯一科学事件** | seeds 0..2：事件全是 `['q']`，文本 `\nq = 82/53/53`，`parse_status=constrained_target`。scientific 7 条轨迹每条只有一条 `q`。`any(q)` + `parse_region` **全部被这条强制行单独满足**。 |
| **offline H 当步前 / e2e** | 八阶段全 exit 0。`H=[[1..8]]`，键 `H/E/token_prefix`，**无** `H_pre_step`。intervene `timing=unexpressible`，`status=donor_missing`。analyze `p1 is None`。smoke **要求**空结论。 |
| `timing != "pre_step"` | 任意其他字符串都绿。 |
| `test_tiny_hooks` L17 | 任何带 `forward` 的类都真。 |
| `test_c7_m01_*` | 手填 `noise_set=["p3"]`，不经 labels。 |
| `test_plus_locks_*` | 同进程 RAM clear。**不**新进程。 |
| `test_collect_copies_*` | 只查 copy + probes 文件。 |

### 3.3 其他对抗

| 对抗 | 结果 |
|---|---|
| 科学 prepare 事件 | 7 条轨迹事件全是强制 `q = 82` 或 `53`。`trace-source` 题干被截断（§3.1）。 |
| pytest 后 persist 泄漏 | 159 passed 之后磁盘为 `["gsm8k-12", "q:ada has 4 apples…"]`。`test_plus_locks` 结束时 `clear`；**更后的** `load_gsm_plus` 用例再写入且不清理。 |
| 科学 collect 拒 offline | 既有测试锁 `offline_prefix_ids`。fixture e2e **不**走 scientific。 |
| 账本 | `.planning/PAPER_TRACEABILITY.md`：`python -m pytest -q` **70**；`passed_local_tests` **100**；`tests_exist_not_acceptance` **100**；`executable_function` **159**。页眉写不得用 pytest 关可执行行；协议行仍用 pytest 关闭。`.planning/phases/06-acceptance/06-VERIFICATION.md` 仍写 **136 passed**（本冻结作者称 159）。 |

## 4. 未做检查，及原因

| 未做 | 原因 |
|---|---|
| 真 HF 权重、官方全量、GPU/CUDA KV | 范围外 / `pending_server` |
| Linux cgroup / 真隔离 HumanEval | 只有 `UnavailableExecutor` / `SpyExecutor` / 宿主 `subprocess` |
| 其他 round-15 通道报告 | 禁止 |
| 改生产或加回归 | 禁止；反例只在 §8 作协议 |
| 对交卷漂移字节单独重跑 pytest / 点名 CE | 交卷已离开声明冻结。159 与 CE 挂在 `401e509b…`。 |
| 逐行审计 `transformers`/`torch` | 只审项目用法 |
| 把 Goal 标 Complete | 本通道只评验证质量 |

## 5. 交付主张 vs 测试实际证明

| 主张 | 位置 | 测试是否支持 |
|---|---|---|
| `python -m pytest -q` → 159 passed | `VERSION.md` | **开审命令是。** 当作 Goal / 交卷盘证据：**否。** |
| A13-01 alt-source 图 + intervene 优先 trace-source | ISSUES | **图：独立同意。生成：开审截断，主张超售。intervene：算法同意；CLI 测试是 `prep/` 替身。** |
| A13-02 未知或 \(T\) 未覆盖 → \(M=\emptyset\)，`rho_M_*=null` | ISSUES | **实现独立同意（含 \(T\) 未覆盖）。** 作者测试只锁全未知。 |
| A13-03 任意 `sham:` → `noise_set=None`，不把空 \(N\) 当已评估 | ISSUES | **\(T\) 已覆盖时独立同意。** 作者测试与 A13-02 混杂；科学 CLI 弱析取。 |
| A12-03 `_find_tasks_jsonl` 只读传入目录 | ISSUES | **独立同意（含兄 prep）。** 作者只锁祖先 `col/`。`_load_source_value_pair` 仍 extras，**不是**本条。 |
| Plus 锁写入内存 ∪ 磁盘；仅清 RAM 后 Symbolic 仍 `test` | ISSUES A10-04 | **是（独立 CE + 作者测 RAM 半边）。** 跨进程独立闭，作者不锁。 |
| 无本题 `tasks.jsonl` → fit/calibrate raise；sham 不广播 | ISSUES C6 / B9 | **孤立是（独立 CE）。** 作者只锁 fit。 |
| CLI 流水线消费上游 | `test_full_cli_smoke` | 文件被读。科学没有：offline H、analyze 无 P1 表。 |
| Goal §九 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **本套件不能作证。** 见 §10。本通道不宣布 Goal 完成。 |

账本对照：A13-01 **生成截断** 与 **intervene CLI 一般性** 是「写已闭但独立 CE 未一般成立」的超售。A13-02/03、A12-03、persist、假 P1、Prefill、`n<d` **没有**「写已闭但 CE 仍红」。

## 6. 测试是否独立有效

### 6.1 独立 oracle（错实现会红）

**前轮仍闭合（本轮重核，未推翻）：** B-01 缺噪声 null；B-02/B-23 unknown；B-03 sham 不进入 R_behavior；B-04 删除不对齐；B-06 表面≠parents；B-07 HumanEval/0；B-08 sidecar 8；B-09 数字隔离；B-10 span；B-11 空父母；B-13 `family_id`；B-14 source=/test_only；B-24 `5.5`/`5.0`；C-02 α≥1；C-03 INLP 公式；C-04 范数；D-01/D-08 下标；默认 P1 `requires_held_out`；`-1` BCE mask；夹具算术/TO；swap 公式；encode NaN；C3-M-01 事件均值；C3-M-03 不一致分母；C3-M-07 空列表不把 hits 当 N；conformal `[0.7,0.4]`；bilinear σ/λ_FN；spy / `exec(`；E-17 labels-dir hash；Boundary BCE；P2 无集合分母；Child 非沙箱；scientific **拒绝** offline H；无 `generate_fn` 拒答；Week8 零 excess / 阈值无测量 / 未注册 Gate；gsm 家族键；monotonic；resume 不覆盖；analyze 文件入口；verbalizer 17/70/boxed；span 跨界 `[]`；Plus 隔离；Hotpot 口语；题干不入事件；H 有限；科学 intervene ≠ `donor_missing`（scientific+tiny）；`prefix_ids`/空 hidden 非 Prefill；噪声 bootstrap `lo<hi`。

**本冻结点名攻击：**

- **alt-source 图必须改父母且保值。** 钉死旧表达式 `p1 * p2` 或改答案会红。**实现闭。**
- **alt-source 生成题干必须完整。** 开审 `cap=48` 会切掉 `* p2_src?`。作者开审测试不红。交卷新断言会红——**那是漂移后的测试，不是冻结证据。**
- **有 pair_meta 时 donor 必须先 source。** 改循环顺序会让独立 unit 红。作者 CLI 例在无 `prep` 兄目录时仍绿（fallback）。
- **未知或 \(T\) 未覆盖不得进 \(M\)。** 把未知当 \(M\) 会让独立 CE 红。作者全未知例会红；\(T\) 未覆盖作者不锁。
- **\(T\) 已覆盖 + sham 行不得把空 \(N\) 写成已评估。** 作者混杂例不锁。独立会红。
- **`_find_tasks_jsonl` 不得走祖先/兄 extras。** 回到 4 层 walk 会让祖先例红；兄 prep 作者仍不锁。
- **Plus persist：仅清 RAM 不够。** 跨进程实现闭；作者删 persist 读写仍可靠同进程 RAM 绿。
- **labels 不能造 P1。** 作者不塞协变量；独立塞了仍拒。
- **标量 Prefill / `n<d` truncated。** 独立同意。

### 6.2 无效、自指或过弱

| 测试 | 为何不能证明论文行为 |
|---|---|
| `test_source_value_pair_rewrites_graph_ids`（开审） | 锁图，不读 generate `prompt_text` / `prompt_len`。截断仍绿。 |
| `test_scientific_h_is_finite_and_pairs_donor` 的 `donor_kind` | 目录名 `prep`/`col` 救命。不锁独立 collect 目录。 |
| `test_unknown_behavior_is_not_counted_as_m` | 只锁全未知。不锁「\(T\) 有已知行但仍未覆盖」。 |
| `test_sham_no_change_does_not_book_empty_n` | 与 A13-02 混杂。不查 `null_reason`。 |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `!= 1.0 or null_reason`。聚合层 `null_reason is None` 也能绿。 |
| `test_collect_copies_tasks_so_fit_follows_e_order` | 只查 copy + probes。不比列序。 |
| `test_plus_locks_symbolic_family_to_test` | 不 spawn。 |
| `test_analyze_refuses_fake_p1_from_labels` | 不塞 P1 协变量。 |
| `test_generated_events_*` / scientific prepare `any(q)` | 教员强制 `\nq = 82` 单独满足。 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | 名不副实。末 token 有限 H 也会绿。 |
| `test_intervene_geometry_is_not_pre_step` | offline 单行 H → `unexpressible`。 |
| `test_analyze_uses_labels_or_stays_null` | 不读 `p1`。 |
| `test_full_cli_smoke` | offline H 当成功。仍断言空结论。 |
| `test_p1_held_out_logistic_detects_rho` / `test_c01_held_out_*` | `ρ=y` 在全部行。泄漏拟合同样 `auc_full=1`。 |
| `test_tiny_hooks` L17 | 恒真。 |
| 交卷 `test_source_value_pair` 的 generate 断言 | **不在声明冻结。** |

## 7. Mock / stub 如何盖住未接通路径

几乎没有 `unittest.mock`。内部 stub 在干同样的事。

1. **Goal e2e 仍是 fixture/offline。** `H`←`token_ids[:8]` = `[1..8]`；无 `H_pre_step`；analyze 无 `p1_table`；smoke **要求**空结论。
2. **A13-01 用图断言盖住截断的 generate 题干。** 用 `prep/` 兄目录盖住「collect 产物上 donor 不是 fallback」。
3. **A13-03 用与 A13-02 重叠的构造盖住「空 \(N\) 已评估」。**
4. **科学 sham 用弱析取盖住聚合层没有 `null_reason`。**
5. **科学事件非空，来源是教员强制 `q=`。**
6. **步前 H 用有限行数冒充「不是末 token」。**
7. **C7-M-01 用 helper 的 `noise_set=["p3"]` 盖住 fixture 上 S 为空。**
8. **A10-04 作者测试用同进程磁盘读盖住「新解释器」。**
9. **套件把 Plus 键写进仓库缓存且多数用例不 `clear`。**
10. **账本协议行仍 pytest；可执行行 `tests_exist_not_acceptance`。**

**仍无测试提及的符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`assert_disjoint`、`score_qa`、`procrustes`、`card`、`apply_model_template`。

## 8. 应让错实现失败的反例（现有测试不过这些）

进程内 / 子进程已执行。本通道未加测试。

### CE-1 A13-01 图闭 / 生成截断（开审未锁）

```text
apply_alt_source_same_value(p2):
  question contains '(alt source)' and p2_src
  answer_spec.value == '0'
  parents == ['p1','p2_src']
  expression == 'p1 * p2_src'

scientific prepare trace-source (声明冻结 cap=48):
  pair task question len == 57
  prompt_text == 'p1 = 4. p2_src = 0 (alt source). What is q = p1 '
  prompt_len == 48
  missing '* p2_src?'

应：锁 prompt_text == 全题干，或拒截断。开审测试不锁。交卷补丁不能回写本冻结。
```

### CE-2 A13-01 donor（算法闭；CLI 替身）

```text
_pair_source_value(both differ) == (0, 2, 'same_value_diff_source')
_pair_source_value(source allclose) == (0, 1, 'same_source_diff_value')

collect 不复制 edits.jsonl
_load_source_value_pair(sci_col) is None     # 无兄 prep
intervene donor_kind == same_identity_fallback

prep/col 布局:
  _load_source_value_pair(col) 命中 ../prep/edits.jsonl
  donor_kind == same_value_diff_source

应：collect 写出 edits，或 intervene --in-dir 必须显式 pair；测试不得依赖目录名 prep
```

### CE-3 A13-02 / A13-03（实现闭；作者测弱）

```text
全未知: M=[], rho_M_*=None, behavior_unknown=True
仅 p1 已知, T={p1,p2}: M=[], rho_M_raw=None, behavior_unknown=True
T 覆盖 + sham no-change:
  rho_M_raw=0.5, null_reason=noise_set_missing, rho_M_noise=None
空 N 已评估对照: rho_M_noise=1.0, excess=-0.5

科学 prepare 事件层: behavior_unknown=True, null_reason=noise_set_missing
聚合层: null_reason 键缺失/None, excess=None
作者: excess != 1.0 or null_reason  → 弱
```

### CE-4 A12-03 / persist / 假 P1 / Prefill / n<d（点名闭）

```text
_find_tasks_jsonl(feat, labs) is None          # 即使祖先 col/ 或兄 prep/ 有 tasks
fit / calibrate 孤立 → ValueError tasks.jsonl
Plus 后 RAM.clear → Symbolic test；新进程只 Symbolic → test
labels 塞 length/op/rho/y → p1 is None
0/True/[0]/[] → prefill_unavailable
(2,5) vs (2,3) truncated True
```

### CE-5 教员强制 `q` / offline e2e（测试锁替身）

```text
generate seeds 0..2: events=['q'], assigned='\nq = 82/53/53', constrained_target
fixture --backend offline: H=[[1..8]], no H_pre_step, intervene unexpressible/donor_missing, p1 is None
```

## 9. 发现

### F15-00 开审哈希可复算；交卷时磁盘已离开声明冻结

- **严重度：** Critical（过程）
- **状态：** confirmed defect（冻结协议）
- **文件：** `.planning/audits/round-15/VERSION.md` L5–23；开审 61 = `401e509b…`；交卷 61 = `5413a4bc…`
- **复现：** 开审脚本原文 MATCH。审查期间 `tiny.py` / `generate.py` / `test_round07_regressions.py` mtime 02:51:18–20。本通道未改。交卷 `generate.py` 把 `cap=48` 改成 `>96` 拒绝。事后补丁不能回写本冻结为已闭。
- **注：** 只要本通道提交已确认缺陷，连续通过计数不能开始。

### F15-01 绿 159 不是 Goal / QA 验收

- **严重度：** High（验证）
- **状态：** confirmed defect（验收口径）
- **复现：** 开审 `159 passed / 0`。作者 `pytest_author_claim` 与命令一致。Goal §九.3 要求有意义的 e2e/边界/失败覆盖；本套件 e2e 是 offline 烟测。

### F15-02 A13-01：图重写闭；声明冻结 generate 静默截断 alt-source 题干

- **严重度：** High（正确性 / 验证）
- **状态：** confirmed defect（声明冻结实现）。作者 ISSUES 图半句同意；生成半句 **超售**。
- **文件：** 开审 `models/generate.py` `cap=48`；`edits.py` `apply_alt_source_same_value`
- **复现：** pair 题干 57 字。scientific `trace-source` `prompt_text` 止于 `What is q = p1 `。交卷才改拒绝截断——**不是本冻结**。
- **作者主张 A13-01：** **图同意。生成不同意。**

### F15-03 A13-01 intervene「优先 trace-source」在 collect 产物上不一般成立

- **严重度：** Medium（验证替身 + 主张超售）
- **状态：** 算法闭合（独立 unit）。CLI：作者 `prep/col` 替身。独立目录名 `same_identity_fallback`。
- **文件：** `cli.py` `_load_source_value_pair` L806–813；`_pair_source_value` L816–839
- **复现：** §3 CE-2。collect 不复制 `edits.jsonl`。A12-03 已收紧 tasks 查找，edits 查找仍 extras。
- **作者主张 A13-01 intervene 半句：** **超售。**

### F15-04 A13-02 未知 / \(T\) 未覆盖不进 \(M\)（点名闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE，含 \(T\) 未覆盖）
- **作者主张 A13-02：** **实现同意。** 作者测试偏弱。

### F15-05 A13-03 sham 行不把空 \(N\) 当已评估（点名闭；作者测混杂）

- **严重度：** Medium（验证残留）
- **状态：** 实现闭合（\(T\) 已覆盖独立 CE）。作者例与 A13-02 重叠。科学 CLI 弱析取。
- **作者主张 A13-03：** **实现同意。** 不得用作者例绿写成「已评估空 \(N\)」路径已独立锁住。

### F15-06 A12-03 `_find_tasks_jsonl` 只读传入目录（点名闭）

- **严重度：** —
- **状态：** 实现闭合（祖先 + 兄 prep 独立 CE）
- **作者主张 A12-03：** **实现同意。** `_load_source_value_pair` extras 是另一条（F15-03）。

### F15-07 科学事件测试仍接受教员强制 `q=`

- **严重度：** Medium
- **状态：** confirmed defect（验证替身）
- **复现：** §3 CE-5。作者主张约束 `\nq=` 不是 §4.1 — 诚实口径。**不得**把 `any(q)` 写成科学事件已解析。

### F15-08 Fixture e2e 仍 offline；analyze 常无 `p1_table`

- **严重度：** Critical（验证）
- **状态：** confirmed defect（验证）。作者 ISSUES 已承认八段是 offline 前缀 H — **不要超售成科学 e2e**。
- **复现：** `H=[[1..8]]`，intervene `unexpressible`/`donor_missing`，`p1 is None`。

### F15-09 Plus persist：RAM clear 与新进程均闭；作者测试缺 subprocess

- **严重度：** Medium（验证缺口）
- **状态：** 实现闭合；**测试不覆盖新进程**。孤立从未 Plus 的 Symbolic 进拟合角色 — 诚实，不是 A10-04 残留。
- **作者主张 A10-04：** **机制同意。**

### F15-10 pytest 把 Plus 家族键泄漏进仓库缓存

- **严重度：** Medium
- **状态：** confirmed defect（验证卫生）
- **复现：** 159 passed 后磁盘含 `gsm8k-12` + Ada 文本键。该文件不在 61 文件摘要内。

### F15-11 假 P1 / Prefill / `n<d`（点名闭）

- **严重度：** —
- **状态：** 实现闭合（独立 CE，假 P1 含塞协变量）
- **作者主张：** **实现同意。** 假 P1 作者例较弱。

### F15-12 C7 helper / 弱析取仍绿

- **严重度：** Medium（验证）
- **状态：** confirmed defect（验证替身）
- **文件：** `test_scientific_sham_*`；`test_sham_hits_do_not_book_evaluated_zero_noise`；`test_evaluated_zero_hit_sham_*`；`test_c7_m01_*`

### F15-13 账本仍用 `pytest -q` / `passed_local_tests` 关闭协议行

- **严重度：** Medium
- **状态：** confirmed defect（验证账本）
- **文件：** `.planning/PAPER_TRACEABILITY.md`：70 / 100 / 100；`executable_function` 159。`06-VERIFICATION.md` 仍写 136 passed。

### F15-14 仍有大块零测试符号

- **严重度：** Medium（集合）
- **状态：** confirmed defect（覆盖）
- **符号：** `attention_rollout` 数值、`attention_mean` 数值、`forbid_host_exec`、`score_qa`、`procrustes`、`assert_disjoint`、`card`、`apply_model_template`

### F15-15 夹具排除在冻结外

- **严重度：** Medium
- **状态：** confirmed defect（冻结协议）
- **文件：** `tests/fixtures/*.json`（10 个）

### F15-16 ISSUES 点名关闭：A13-01 部分超售；其余点名实现项与独立 CE 对齐

- **严重度：** Medium（过程）
- **状态：** A13-01 生成/CLI intervene **超售**。A13-02/03、A12-03、A10-04、C6 孤立拒、B9 不广播、假 P1、Prefill、`n<d` **无「已闭但 CE 仍红」**。
- **不要用本通道把 Goal/需求标 Complete。**

### F15-17 真模型 / 官方全量 / 隔离 Linux runner

- **严重度：** —
- **状态：** 外部待验证
- **注：** tiny 随机权重、offline 前缀 H、宿主 subprocess、constrained `\nq = <digit>`、声明冻结 48 字截断、交卷漂移 **不是** pending_server。

## 10. Goal §九 第 1–7 条 — 只评验证质量

这 **不是** Goal-complete 声明。只问：**声明冻结上的测试与已记录命令** 能否支撑各停止条件。

| 条 | 停止条件（节略） | 验证质量 |
|---|---|---|
| 1 | 论文/协议原子有实现、入口、**验证证据**；追踪无未解释缺口 | **不支持。** 协议行仍 `pytest -q`；可执行行仍 `passed_local_tests`（F15-13）。 |
| 2 | 范围内无已确认未解缺陷；无可影响正确性的未裁定疑点 | **本通道不支持。** F15-00、F15-02、F15-08 为已确认遗留。 |
| 3 | 适用的本机检查实际跑过且通过；有意义的 e2e/边界/失败被覆盖；未跑项不伪装通过 | **命令部分成立，实质失败。** `pytest -q` 确为 159/0（开审盘）。e2e 是 offline 烟测。A13-01 生成截断无测试。 |
| 4 | GSD 阶段与现实一致；软件通过 ≠ 科学/服务器通过 | **文档混杂。** `06-VERIFICATION.md` 仍写 136 passed。 |
| 5 | 连续两轮独立全量 A–F，无新确认缺陷，**同一 hash** | **不能开始一轮通过。** 开审匹配（好）。交卷 **HASH_MISMATCH**。本通道 **提交已确认缺陷**。 |
| 6 | 服务器待办列出真实路径/原因/将来命令 | **不是测试套件问题。** 不得把本机缺口藏进这里：offline 前缀 H、强制 `q=`、48 字截断、目录名 donor、套件 persist 泄漏。 |
| 7 | 交付包：runbook、配置、追踪、问题闭环、审查、本机记录、服务器入口 | **问题闭环未就绪到 Goal 句。** 开审 pytest 记录存在（159/0）。点名 CE 有独立记录。 |

## 11. Goal §五 高风险项 vs 本套件

| §五 | 要锁的行为 | 测试现状 |
|---:|---|---|
| 1 来源/真值 | 官方图与夹具分开；T2/T3 不把答案当 DAG | 夹具/官方形状有测。科学轨迹事件来自强制目标行。alt-source 图有测；生成题干开审被截。 |
| 2 域适配 | 读/合法编辑/更新真值 | sidecar 8、Plus 隔离、Hotpot 口语、alt-source 图有。reversing 无。 |
| 3 事件/行为 | 身份对齐，不靠值 | fixture 路径有。scientific 已排除题干 span；生成区只有强制 `q`。 |
| 4 随机/噪声 | 匹配机会与共同支持；空分母 null | 未知 \(M\) / sham missing 独立见。作者 A13-03 弱。C7 helper 在。 |
| 5 划分 | 测试专用不进拟合 | Plus→test、family persist 有。跨进程无测试。`assert_disjoint` 无。 |
| 6 三时机/可见性 | 步前不含目标首 token / 跨界 | D-01 与 span `[]` 有。last-token 无断言。 |
| 7 探针/基线 | 双头、双线性、MLP、四档 verbalizer | σ/λ_FN、BCE、17/70/boxed 有。孤立无 tasks 已拒。 |
| 8 校准 | 序列最大分；精确顺序统计 | 单元有。孤立 calibrate 实现拒，作者无测试。 |
| 9 迁移 | 4096/3584 拒；两输入都映射 | 维拒与 n<d 有。数值恢复未锁。 |
| 10–11 干预/对照 | 步前 swap；对照分 decode | 科学路径做 hook。donor 测试锁 `prep/` 名。offline e2e 是 `unexpressible`。 |
| 12 C3 | 留出 P1；配对 P2；对照 P3 | 门与若干 null 有。无 `p1_table` 时不建 P1。假 P1 已拒。 |
| 13 附录修复 | 新前缀 Prefill | ids/空/标量/`[0]` 拒。 |
| 14 边界/结论 | 单点≠联合 soundness；Gate 未注册 | 旗标恒 False。零 excess / 未注册有测。 |
| 15 代码任务 | 显式隔离执行器 | spy + `isolated_sandbox is False` 已锁。T3 prepare 不崩。 |

## 12. 通道裁决

| 判断 | 内容 |
|---|---|
| pytest | **159 passed，exit 0，21.50s，159 collected（开审 MATCH 盘）。** 无 skip/xfail。**不是** QA-01 / Goal §九.3 证据。**不是**交卷 hash 上的记录。 |
| 冻结 | **开审 HASH_MATCH `401e509b…`（61）。交卷 HASH_MISMATCH `5413a4bc…`（仍 61）。** |
| 独立性 | 真 oracle：alt-source 图；未知 / \(T\) 未覆盖不进 \(M\)；\(T\) 覆盖 + sham 不评空 \(N\)；`_find_tasks_jsonl` 只读传入目录；Plus persist（含 RAM clear 与 subprocess）；假 P1（含塞协变量）；Prefill；n<d；孤立 fit/calibrate 拒。**不独立 / 开审未锁：** generate 48 字截断；donor_kind 的 `prep/` 名；A13-03 作者混杂例；科学 sham 弱析取；强制 `q=`；offline e2e；作者缺 subprocess。 |
| Mock/stub | offline 前缀 H + `prep/` 兄目录 edits + 教员强制 `q=` + 截断 prompt + 弱析取 + 同进程 persist 冒充跨进程。 |
| 论文行为仍未证明 | 真 Prefill 向量语义之外的 KV、可变 `g(Y)`、分 decode 的 token、从真实轨迹建的 P1、隔离执行、自然 CoT 事件、完整 alt-source 题干上的 generate/intervene |
| 交付 vs 测试 | 「159 passed / A13-01 全闭 / e2e 已通」**超过** 冻结树测试力度。A13-01 图闭 **不能** 写成 generate/CLI intervene 已闭。 |
| 已确认问题？ | **是。** Critical：F15-00、F15-08。High：F15-01、F15-02。A13-02/03、A12-03、persist、假 P1、Prefill、n<d **实现 CE 未失败**。A13-01 生成与 CLI intervene **超售**。 |
| Goal 完成？ | **否。** 本通道只评验证质量，不宣布 Goal 完成。 |
| 通道通过？ | **Fail。** 绿 pytest 不是验收。交卷哈希已漂。声明冻结 generate 截断 alt-source 题干。Fixture e2e 仍 offline。弱析取仍绿。 |
| 停止条件第 5 条 | **不能开始连续通过。** 本通道提交已确认缺陷，且交卷 hash ≠ 声明 hash。修复后须对 **新** hash 重开计数；只补本文件不改变被审摘要。 |

在声明冻结上用 CE 级测试锁住 **完整（未截断）alt-source 题干的 generate**、**不依赖目录名 `prep` 的 trace-source donor**、**非 offline 前缀 H 的 e2e**、**非强制 `q=` 的科学事件（或显式 constrained_target 合同）**、以及 **科学 sham 的事件层 `null_reason`（禁止弱析取）** 之前，任何「代码验收通过；独立审查未发现已确认遗留缺陷」的结束句都与本通道证据矛盾。事后改 `generate.py` / r07 截断例 **不能**把本轮改写成通过。A13-02/03、A12-03、persist 的实现闭合记在 F15-04…09，不是通道通过。
