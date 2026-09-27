# 审查报告 A：原文一致性（paper consistency）— round-12

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-12 |
| **审查时间** | 2026-09-21 02:31–04:20（UTC+8） |
| **声明冻结 hash** | `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（61 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **开审 HASH_MATCH，交卷 HASH_MISMATCH。** 按 `VERSION.md` 原文 Python 逐字复算：开审文件数 **61**，摘要 `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`。交卷前同脚本：仍 61 文件，摘要 `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。漂移仅两文件：`src/reasoning_diff/splits.py`（开审 `08f77e972927a996` / 152 行 → 交卷 `40ab4021d4dccc6e` / 184 行）与 `tests/test_round07_regressions.py`（开审 `a59c236d5d007ae7` / 221 行 → 交卷 `1ffdbd7ef5803fb6` / 224 行）。其余 59 文件摘要与开审一致。本通道未改 `src/`、`tests/`、`pyproject.toml`。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `39CF907C0B66B9B26AE7355E394848CFA1FF41CE5166310E1DC0A9307F9AC498`（与账本 §0 一致） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-12/` 下除 `VERSION.md` 与本文件外的任何通道报告。**未把** `ISSUES.md` 作者关闭当作关闭。交卷前漂移的 `splits.py` / `test_round07_regressions.py` **不能**认证声明冻结上的划分结论。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |
| **作者声称 pytest** | VERSION 写 156 passed。本通道在开审 MATCH 树上复跑 `python -m pytest -q --tb=line` → **156 passed**（23.72s）。绿测不关闭原文符合性，也不认证已漂的树。 |

**总判：不通过。** 声明冻结在审查开始可核验，**交卷时不能认证**。相对作者 r12 关闭表，本通道在**仍匹配冻结的 59 文件**上独立复跑后**不得原样重开**：无 `tasks.jsonl` 且搜索锥为空时 fit/calibrate 抛 `ValueError`；collect 仍复制该文件；默认 scientific 有任务时 $E$ 列=`[p1,p2]`；`sham:` 的 `noise_ref` 不再盖到真实前提，密度不再把 $N=\{p1,p2\}$ 记成已评估 0；标量 Prefill 拒绝；T3 prepare 不走 SVP；改名改图；analyze 拒假 P1；PCA `n<min d` → `truncated`；夹具不能标 official。

本轮仍 FAIL，原因有两层，缺一即不通过：

1. **冻结完整性：** 交卷前 `splits.py` 与 `test_round07_regressions.py` 已从声明摘要漂走。对声明 hash 的通过意见不能交给漂移树。任务规定 HASH_MISMATCH → FAIL。
2. **原文语义（59 个未漂文件已足够）：** scientific 仍把 teacher-force `\nq = 82` 标成 `constrained_target` 后当作 §4.1 成功事件；$R_{\mathrm{behavior}}$ 比较的是约束数字。Plus/Symbolic 共组在 CLI 单任务 / 清空锁之后仍可让 `gsm8k-1` 进 `probe_train`。作者为关 C6 而把 `_find_tasks_jsonl` 做成向上 4 层 + 固定目录名搜索，能静默绑到**另一道题**的 `tasks.jsonl`，把 $E$ 列改成 `[p2,p1]`。

Gate 0–2 保持 `unregistered`，**不是缺陷**。tiny 随机权重 **不是** MODEL-01。假说不要求正结果。不把 Goal 标为完成。

---

## 0. 相对作者关闭表的独立复跑（避免把已修项当新缺陷）

`ISSUES.md` / `VERSION.md` 的 r12 local close **只作对照清单**。本通道在开审冻结字节（及注明的未漂文件）上重跑后：

| 作者声称已关 | 本轮复跑 |
|---|---|
| 无 `tasks.jsonl` → fit/calibrate `ValueError`；collect 复制；查找向上 4 层 | **缺文件且搜索锥为空时成立。** 孤立目录 `featbox`/`tagbox`：`_find_tasks_jsonl=None`，fit/calibrate 均 `ValueError: … not label order`。默认 scientific：collect 复制 `col/tasks.jsonl`，`_e_premise_ids(task)=[p1,p2]`。**不得**按“无任务仍首次出现序”原样重开。4 层 + `col`/`prep`/`lab` 等额外名可绑错题，见 A12-03。 |
| B9-01：sham `noise_ref` 只在 `sham:`；广播不再写入 $N$ | **成立（科学入口）。** labels：`p1`/`p2` 的 `noise_ref=None`，`sham:q` 为 `1.0`。事件密度 `null_reason=noise_set_missing`，`rho_M_noise=None`，`rho_M_excess=None`（不是 0 / 1.0）。**不得**按 A10-03 原文重开。 |
| 标量 Prefill、T3 不走 SVP、改名改图、假 P1、`n<d` truncated | **成立。** 标量/`bool`/`[0]`/空 → `prefill_unavailable`。Hotpot `edits.kind=['document']`，无 SVP。SVP 源臂 `p2_src` / `p1 * p2_src` / `parents=['p1','p2_src']`。仅 labels（含 length/op/rho/y）→ `p1=None`。`(2,5)` vs `(2,3)` → `truncated=True`。 |
| Plus 锁族 | **冻结树上不成立为跨进程/CLI 共组。** 开审 `splits.py` 与 r10 同摘要（152 行模块级 `set`）。`assign_split("gsm8k-1")` → `probe_train`。清空锁后只 load Symbolic → `probe_train`。同进程再 load Plus → 才是 `test`。CLI `_load_task` 一次一种 snapshot。见 A12-04。交卷后写入的磁盘 persist **不在**声明冻结内，不能关闭本条。 |
| 约束 `\nq=` 是本机接口、不是 §4.1 | **作者声明，不是关闭。** scientific prepare 仍接受 `constrained_target`。见 A12-01。 |

---

## 1. 逐文件覆盖

每行：路径 — 磁盘 `splitlines()` 行数 — SHA-256 前 16 位 — 对照条款 — 覆盖结论。行数/摘要以**开审冻结**为准；两处漂移在表内标明。

| 文件 | 行 | digest | 对照条款 | 覆盖结论 |
|---|---:|---|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 517 | `f3c0ec087b5bf4e5` | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 86 | `83a9142dba4f7fcd` | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。L29：无编辑随机变化不得强加前提身份——本轮 sham 路径已守。Gate 保持 null。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 166 | `b9e0a8ea3fc87bf0` | GOAL §5 = L73–91 | 已通读。§5.3/5.5/5.7 在科学入口仍被降级或替身。§5.14/5.15 持守。 |
| `.planning/REQUIREMENTS.md` | 76 | `39cf907c0b66b9b2` | DATA/MEAS/MODEL/… 与 atomics | 复选框全空；状态表仍写 `implemented_local` / `implemented_local_tiny`。 |
| `.planning/PAPER_TRACEABILITY.md` | 抽样约定 + TR-0125/0135/0158/0206/0327/0400 | — | 账本不得当实现证据 | 528 条。`implemented_local` 约 477–478。TR-0125=`partial_local_scientific`，TR-0135=`partial_local_tiny`；TR-0206/0327（MODEL-01）仍 `implemented_local`。协议/标题行仍 **70** 处 `python -m pytest -q`。 |
| `pyproject.toml` | 27 | `cb44851f7fbf7bf7` | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 有 `torch`/`transformers`。 |
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58d` | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 4 | `307299fda7b77d22` | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a45` | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。拒 `official`+自建夹具。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277` | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先正确。默认 cone 走任务祖先，不是 $\hat R^{\mathrm{val}}$。 |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814` | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 | `parse_events` 仍把前提与节点都当赋值。`merge_review` 可回填。策略只读 `status=="strategy_change"`。 |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccf` | §7 T1 重算；GOAL §5.2 | 值编辑+重算正确。`apply_rename_edit` **重写** id/parents/expression。 |
| `src/reasoning_diff/measure.py` | 392 | `b15fb8a5bb92220f` | §2.6 $S/M/\rho$；协议 L29 | 差集/空分母公式在。`noise_ref=1.0` 只写 `sham:` 行。`event_density_sets` 见 sham hit → `noise_set=None`。聚合层丢掉事件 `null_reason`（不重开广播）。 |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63b` | §2.6 P1–P3；Gate；S2–S4 | P1 只吃 `p1_table.jsonl`。Gate `unregistered`。`scientific_conclusion=None`。 |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649` | §2.4 交换/对照/INLP/$\mathrm{IE}_Z$ | 库层公式正确。CLI 无 `--dev-layer-scores` 时相对对照常为 `None`。 |
| `src/reasoning_diff/probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec` | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、未知掩码正确。CLI tiny `rank=min(64,d)`。 |
| `src/reasoning_diff/probes/boundary.py` | 44 | `ce3b549be7d671ff` | §4.2 Hidden=256 ReLU | 架构符合。CLI 用全 1 标签。 |
| `src/reasoning_diff/probes/calibrate.py` | 45 | `e8b3ed3459bb22c5` | §2.5 命题 2 | 分位数与 $+\infty$ 正确。 |
| `src/reasoning_diff/probes/__init__.py` | 3 | `3065196db28e929c` | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4` | §8 四档自述；GOAL §5.7 | 库层走 `extract_answer`。CLI `generate_fn` 回显前缀。 |
| `src/reasoning_diff/transfer.py` | 86 | `5549f84bd1bd6240` | §5 Fig.2c；S3；GOAL §5.9 | 直接迁移拒 4096/3584。`n<dim` → `truncated=True`。 |
| `src/reasoning_diff/repair.py` | 232 | `f76ff9998b9a6b17` | §3/§9 嫁接；GOAL §5.13 | Prefill 拒标量/`[0]`。掩码仍改前缀字符串。无 Fig.6 五类失效分类器。 |
| `src/reasoning_diff/cli.py` | 1254 | `175abf12f4c207c5` | §4 流水线；§8.2 scientific | scientific prepare **只拒** `parse_failed`，**接受** `constrained_target`。collect 复制 `tasks.jsonl`。无任务则 fit/calibrate 失败。`_find_tasks_jsonl` 向上 4 层 + `col`/`prep`/`lab` 等名，可绑错题。 |
| `src/reasoning_diff/models/adapters.py` | 42 | `c1992624026a1bf0` | §8.1 模型卡 | 两张冻结卡。CLI 不 `from_pretrained`。 |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20` | §4.2 $h_i/e_j$；GOAL §5.6 | 不可表达步前跳过。`followed_donor` 仍是 ids 是否变化。 |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185ae` | GOAL §5.6 三时机 | 跨界 token 排除正确。 |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6b` | §4.1 / §8.2 自然轨迹 | decode 后 **teacher-force** `\n{target} = ` 再采两位数。 |
| `src/reasoning_diff/models/tiny.py` | 120 | `21725a183452bd06` | 本机 hook；**不是 MODEL-01** | 随机 Qwen2/3。`weight_source=random_init`。 |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010fa` | §4.2 层带 / span | 3 层 → 读出层 1。跨界排除。 |
| `src/reasoning_diff/models/__init__.py` | 1 | `0b7dd6c4dd852065` | — | 注释。 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b` | §7 适配入口 | 快照分发。CLI 默认 `t1_fixture`。不生成 500 题。 |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f736969031` | §7 T1；template≠G | 拒裸 `G`、排除共享 RNG、mod 23。 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3` | 官方/夹具分离 | 拒绝非 `fixture`。 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d` | op∈{5,10,15,21}，n=500 | 只校验，不生成任务单。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f` | §7 T2；评测专用 | `register_test_only_family`。Plus 自身 `fit_eligible=False`。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354` | §7 T2 | **不**注册 test-only。无侧车 placeholder + `unknown`。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d56149` | §7 T2-noop | 可造配对。无注入句值扰动扫描。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb` | §7 T3 | supporting_facts ≠ DAG。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0` | §7 T3 | `composition_reference` 不可重算。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7` | §7 HumanEval；GOAL §5.15 | 无新解则 `needs_truth`。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f88` | §7 T4；Fig.6 | 四类状态枚举在。无相图分类器。 |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3` | — | 注释。 |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78` | GOAL §5.15 | 禁宿主 exec。`ChildProcessExecutor.isolated_sandbox=False`。 |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122` | §3 域内评分 | 数值/QA 精确匹配。代码经执行器。 |
| `src/reasoning_diff/splits.py` | **开审 152** | **开审 `08f77e972927a996`** | §4.1 共组；DATA-03 | 开审与 r10 同字节：家族锁 = 模块级 `set`。**交卷 184 行 / `40ab4021…` 写入磁盘 persist，不在声明冻结内。** 默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 53 | `2098c2c72a852eaa` | GOAL §5.4 | 五流分离。 |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd3` | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 85 | `524657027e9b402f` | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb` | — | 夹具路径。 |
| `tests/test_round07_regressions.py` | **开审 221** | **开审 `a59c236d5d007ae7`** | 作者 r12 锁 | 开审锁无任务拒绝、sham 不广播、in-process Plus→Symbolic、假 P1、rename、`n<d`。**不**锁拒 `constrained_target`；**不**锁 CLI 跨进程共组；**不**锁 4 层搜到错误 `col/`。交卷 +3 行不在冻结内。 |
| 其余 `tests/*.py` | 见表下 | — | 替身锁 | 抽读：锁生成区有 `q`、$H$ 有限、timing≠`pre_step`。生产测试字符串**无** `constrained_target`。 |

其余测试文件（开审行 / digest）：`test_artifacts.py` 73/`830953f379954233`；`test_cli_pipeline.py` 30/`ff826b3e553f003b`；`test_generate_loop.py` 17/`ffe10b0d6812908c`；`test_measure.py` 40/`fbc68abd89ed109e`；`test_review_regressions.py` 399/`c1f0236455f3f087`；`test_round03_regressions.py` 292/`61247e8a074944a3`；`test_round04_regressions.py` 311/`25949c80bbb55585`；`test_round05_regressions.py` 197/`bc837c0c3a6ea3ae`；`test_round06_regressions.py` 145/`ac7e4e88248ff49e`；`test_science.py` 103/`cdb5f1460502ba3c`；`test_t1_official.py` 31/`f4b3cbc1fcd5371e`；`test_t2_gsm.py` 33/`f66a95bb737dc973`；`test_t3_t4.py` 44/`d0381c097d04bc9d`；`test_tiny_cache.py` 26/`83ae0441140f7e17`；`test_tiny_hooks.py` 27/`e28e58b638568d89`；`test_tracer_t1_prepare.py` 100/`62a5e2f168a20e8f`。

第三方库：审查了本项目对 `numpy` / 可选 `torch`+`transformers` 的使用假设，未审查依赖源码。

夹具通读：`tests/fixtures/t1_tiny.json`、`t2_symbolic_one.json`；抽用 `t3_hotpot_one.json`。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。L29 在 sham 科学入口本轮守住（A12-N4）。Gate 保持 null。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 3、5、7 条在科学入口被替身。第 14、15 条持守。 |
| C4 | 账本约定 + TR-0125/0135/0158/0206/0327/0400 | TR-0125=`partial_local_scientific`。MODEL-01 行仍 `implemented_local`。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。`splits.py` 通读的是交卷漂移稿；开审 152 行与 r10 同摘要，未在覆盖前保存正文。 |
| C6 | 库函数手核：$R_{\mathrm{task}}$、差集、交换、分位数、直接迁移、P1、cone、PCA | 库层公式符合。PCA truncated 符合作者声称。噪声 **不再**把 sham 盖成真实 $N$。 |
| C7 | §4.1 伪代码 vs scientific prepare/collect/label/fit | generate 在；解析区=生成段；对象是 teacher-force 目标行；`constrained_target` 被接受。 |
| C8 | 生成区事件、有限 $H$、SVP 图、`sham:` 前缀、密度 | 事件 `start≥prompt`；$H=(7,32)$ 全有限；SVP 图已改写；观测有 `sham:q`；密度 **不再**把 sham 盖成真实 $N$。 |
| C9 | 无任务拒绝 / 假 P1 / Gate / 夹具官方 / 错题绑定 | 孤立无任务 → 拒绝。假 P1 拒。Gate `unregistered`。夹具拒 official。祖先 `col/tasks.jsonl`（前提序对调）→ fit 成功且 $E$=`[p2,p1]`。 |
| C10 | Plus/Symbolic 家族 | 无锁 / 只 Symbolic：`gsm8k-1` → `probe_train`。同进程先 Plus → `test`。夹具 `gsm8k-12` 哈希已是 test。 |
| C11 | `python -m pytest -q --tb=line` | **156 passed**（开审 MATCH 树，23.72s）。不作为原文关闭。 |
| C12 | VERSION 冻结脚本逐字复算 | **开审 HASH_MATCH** 61 / `598e6c8f…6bd4`。**交卷 HASH_MISMATCH** 61 / `0816fa5b…de3b`。 |
| C13 | 论文/协议/GOAL/REQUIREMENTS SHA-256 | 四份与账本 §0 一致。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 真实 Qwen3-8B / R1-7B、GPU、官方 500 题 | 协议 §7：`pending_server`。tiny 不是替代。 |
| N2 | 人工复核事件映射小集 | 有 export/merge，无抽样协议实现。 |
| N3 | 独立数据重拟合探针/INLP/Procrustes | 标签对象不是生成步骤上的 $R_{\mathrm{behavior}}$。 |
| N4 | 其他 round-12 通道报告交叉 | 任务禁止阅读。 |
| N5 | `PAPER_TRACEABILITY.md` 全部 528 条逐字 | 已读约定与高风险行。其余多为同模板。 |
| N6 | 合格隔离沙箱跑 HumanEval | 无合格隔离后端。 |
| N7 | 在交卷漂移树（`0816fa5b…`）上把划分修复写成冻结关闭 | 冻结已破；persist 字节不在声明 hash。 |
| N8 | 交卷后再跑全量 pytest | 树已漂，不能认证声明 hash。开审 156 passed 仍有效于当时 MATCH 树。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行；`math` 公式；`proto` 协议；`hyp` 假说（不要求正结果）；`bg` 背景；`excl` 排除。

状态：`ok-lib` 库忠实、未接到科学入口；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | 生成区/有限 $H$/Prefill 接口在；事件是约束目标 | subst |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 2.1 | 62–64 | $P$、$T$、$v(s_i)$ | math | schema 正确；scientific 的 $s_i$ 是 `\nq = 82` | subst |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+扰动 | math | 比较对象是约束数字；本机 `behavior_label=None` | subst |
| 论文 2.5 | 132–139 | $a(X)$ 列 = $E$ 行 | math | 有本任务文件时跟前提序；无文件拒绝；4 层搜索可绑错题 | subst / ok-lib |
| 论文 2.6 / 协议 2 | 154–158 / L29 | 噪声先扣；不得给无编辑变化强加前提身份 | math/proto | sham 只写 `sham:`；未映射 → `noise_set_missing` | **ok**（本轮） |
| 论文 4.1 | 232–253 | `T0=generate` 后 `parse_events(T0)` | exec | 解析生成区；对象是 teacher-force 目标行 | subst |
| 论文 7 | 403–405 | Plus test-only；同族共组 | proto | Plus 自身 test；Symbolic 单独可进 train | subst |
| 论文 8.2 | 419–431 | scientific 自然轨迹 | exec | 开关在；后续标签/$H$ 不是论文对象 | subst |
| 论文 9 | 353 | Fig.6 五类失效 | exec | T4 枚举在；无相图分类器 | missing |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |
| DATA-01 | — | 夹具不得冒称官方 | proto | `t1_fixture` 拒 official；schema 拒 official+自建 | **ok** |

---

## 5. Findings

### A12-H1 — 交卷时声明冻结不可认证

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `.planning/audits/round-12/VERSION.md` 声明；工作树 `src/reasoning_diff/splits.py`、`tests/test_round07_regressions.py` |
| **Trigger** | GOAL 第七节：每轮审查必须钉在同一固定代码版本。任务：HASH_MISMATCH → FAIL。 |
| **Paper requirement** | 独立审查意见只能覆盖已声明并复算一致的字节。树一变，旧通过不能覆盖新代码。 |
| **Repro / evidence** | VERSION 原文脚本。开审：`len=61` / `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`。交卷：`len=61` / `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。`splits.py` `08f77e97…`(152)→`40ab4021…`(184)；`test_round07_regressions.py` `a59c236d…`(221)→`1ffdbd7e…`(224)。`cli.py`/`measure.py`/`generate.py` 未漂。本通道未写生产文件。 |
| **Impact** | 不能宣布“已在 `598e6c8f…` 上连续通过”。作者对 Plus persist 的任何交卷后修改不能绑到声明冻结。 |
| **Suggested fix** | 停写生产/测试字节，重冻 VERSION，再开独立 A–F。 |
| **Status** | **confirmed defect**（过程/冻结） |

### A12-01 — scientific 事件是约束目标行，不是 §4.1 生成步骤

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/generate.py` `append_target_assignment` 72–98、`generate_task_trace` 135–160；`cli.py` `cmd_prepare` 296–297（开审摘要 `07493570…` / `175abf12…`，未漂） |
| **Trigger** | 论文 §4.1 L232–248：`T0=generate` 之后 `parse_events` 的对象是**生成轨迹**上的变量/表达式/版本/作用域。§2.1：$T$ 是模型生成序列的步骤离散化，$P$ 不是 $T$。§8.2：自然轨迹。GOAL §5.3。作者 ISSUES 写“约束 `\nq=` 是本机接口、不是 §4.1”——**作者声明，不是关闭**。生产测试无 `constrained_target` 字符串。 |
| **Paper requirement** | 自然轨迹步骤事件。无自然步骤时应拒绝 scientific 或标 `unimplemented`，不得把约束接口写成已测 §4.1。 |
| **Repro / evidence** | 独立 `generate_task_trace(seed=0)`：文本 `'p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82'`，`parse_status=constrained_target`，`parse_region=generated`，`target_assignment='\nq = 82'`，事件仅 `q=82`（`start=45`，`prompt_len=36`）。`prepare --eval-mode scientific` + 六比例 + `--sham-opportunities 1` → exit 0，**7** 条轨迹 **全部** `constrained_target`（含 source/extra/sham）。prepare **只拒** `parse_failed`。 |
| **Impact** | C1/C3 入口没有“生成步骤上的编辑响应”。约束数字是本机可解析接口，**不是** §4.1 自然 CoT；实现却把它当作 scientific 成功。 |
| **Suggested fix** | 只把自然 decode（或官方 CoT）解析为事件。`constrained_target` 时 scientific prepare/label/collect 拒绝或降级账本。不要 teacher-force 赋值行来凑事件。 |
| **Status** | **confirmed defect**；真实 CoT 质量 **pending_server** |

### A12-02 — $R_{\mathrm{behavior}}$ 比较的是约束数字，不是生成步骤值

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` `_observations` 229–254；`measure.py` `build_labels` 29–53；`generate.py` 72–98 |
| **Trigger** | 论文 §2.2 L74–78：固定 $M,u$ 下 $v_i(P\oplus\delta(p_j))\ne v_i(P)$。GOAL §5.3。事件定义见 A12-01。 |
| **Paper requirement** | 行为标签来自对齐生成步骤的语义值变化。未知不作负。 |
| **Repro / evidence** | 本机 observations：`(q,p2)`/`(q,p1)` `82→82` `no_change`；sham `82→53` `changed`（`premise_id=sham:q`）。labels：`(q,p2)`/`(q,p1)` `task_label=1`，`behavior_label=None`。scientific `fit` 只写出 **task** 头（loss `0.05036`）；行为头 `no_known_labels`。intervene `ie_z_g=target_follow`，抽出 `'9'` vs donor 约束答案。 |
| **Impact** | 差集 $S$ 在本机是空行为集对满任务祖先。即使约束数字因提示词改写而变，那也是 teacher-force 采样对前缀的敏感，不是 §2.2 的 $v(s_i)$。 |
| **Suggested fix** | 先关闭 A12-01。无生成步骤则不写行为标签。 |
| **Status** | **confirmed defect** |

### A12-03 — `_find_tasks_jsonl` 四层 + 固定目录名可绑错题，$E$ 列身份被换

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` `_find_tasks_jsonl` 692–705、`_e_premise_ids` 708–717、`cmd_fit` 614–620、`cmd_calibrate` 774–780 |
| **Trigger** | 论文 §2.5 L132–134：列 $j$ 与 $E$ 同行 = **本题**原始前提。作者为关 C6-M-01 把查找做成向上 4 层并枚举 `prep`/`col`/`lab` 等名。`test_fit_without_tasks_jsonl` 把 prepare 放在 `run/prep`（**不在** extras 名里），锁不住“祖先恰好有 `col/`”。 |
| **Paper requirement** | `predict_matrix` 列 = 当前题 `task.premises`。读不到**本题**任务应拒绝，禁止静默改用另一份 `tasks.jsonl`。 |
| **Repro / evidence** | 孤立 `featbox`+`tagbox`（锥内无任务文件）→ `ValueError`（作者关闭项在此路径成立）。另造 `bind/col/tasks.jsonl` 为 `WRONG-TASK`、前提序对调为 `[p2,p1]`，特征在 `bind/deep/x/feat`：`_find_tasks_jsonl` 命中祖先 `col/`，fit **exit 0**，`_e_premise_ids=[p2,p1]`。真实夹具前提序是 `[p1,p2]`。这是 C6 列对调的另一扇门，不是首次出现序。 |
| **Impact** | 多 run 共享父目录、或仓库里留着旧 `col/` 时，$Y$ 的 p1 可写到错题的 p2 列。作者“向上 4 层”把缺文件失败换成了错文件成功。 |
| **Suggested fix** | 只从本 stage 的 `--in-dir` / 显式 `--tasks` / collect 复制的那一份读取。读到的 `task_id` 必须与 traces/labels 一致，否则失败。不要按目录名在祖先里碰运气。 |
| **Status** | **confirmed defect**（新残留；无文件拒绝 **本轮不重开**） |

### A12-04 — Plus/Symbolic 家族锁不是 CLI/跨进程共组

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | 开审 `splits.py`（152 / `08f77e97…`，与 r10 同字节）；`tasks/t2_gsm_plus.py` 22（未漂）；`tasks/t2_gsm_symbolic.py` 9–16（未漂，**无** register）；`cli.py` `_load_task` 168–184 |
| **Trigger** | 论文 §7 L403–405；DATA-03；GOAL §5.5：测试专用及同基础题全部变体共组，不得拟合。作者声称 Plus 锁族。开审锁文件是进程内 `set`；交卷 persist **不在冻结内**。 |
| **Paper requirement** | 与 Plus 同族的 Symbolic 必须是 test。锁必须落在划分产物或磁盘家族表上，不能依赖“碰巧先 import 过 Plus”。 |
| **Repro / evidence** | `assign_split("gsm8k-1")` → **`probe_train`**（哈希）。清空锁后只 `load_gsm_symbolic(original_id=gsm8k-1)` → `split_for_task=probe_train`，`family_locked_test=False`。同进程再 `load_gsm_plus` → 两者才是 `test`。CLI 一次只加载一个 snapshot；新进程模块级 `set` 为空。`assign_split("gsm8k-12")` → `test` 是哈希巧合，不能当锁的证据。无侧车 Symbolic prepare 先因 A12-08 崩溃。 |
| **Impact** | 同 `gsm8k-1` 家族：Plus 永远 test，Symbolic 可进 `probe_train`。探针/校准可看到测试专用家族。 |
| **Suggested fix** | 划分时按磁盘上的 Plus/test-only 家族表（或显式 siblings）锁族，并写入 `splits.jsonl`。读不到家族表则拒绝拟合角色。不要用审查期间改 `splits.py` 来关闭已声明冻结。 |
| **Status** | **confirmed defect** |

### A12-05 — CLI 四档 verbalizer 回显前缀，把约束数字当成自述命中

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_fit` 655–656；`baselines.py` 92–125 |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7。库层子串打分 **不得重开**。 |
| **Paper requirement** | 四档自述与探针同样本/划分/可见前缀，且是模型生成，不是回显轨迹。 |
| **Repro / evidence** | 库：`verbalizer(..., generate_fn=λ:"17")` 对金标 `7` 得 0。CLI `generate_fn=lambda p, t=prefix: t`。scientific fit：zeroshot/fiveshot/reflection `score=1.0`，`extracted='82'`。 |
| **Impact** | 第 8 节“说不出来”在 CLI 上仍不是同划分模型自述。 |
| **Suggested fix** | CLI 按同一划分调用真实生成；未接线不得标 `implemented_local`。 |
| **Status** | **confirmed defect**（CLI 替身）；子串打分 **本轮不重开** |

### A12-06 — 账本仍大量 `implemented_local`（含 MODEL-01）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` TR-0206、TR-0327、TR-0158、TR-0400、TR-0043；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：未实现不得标已实现。可执行行验证列已改 `tests_exist_not_acceptance`，**不得**按“pytest 关闭可执行行”重开。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。tiny 不是 MODEL-01。 |
| **Repro / evidence** | `implemented_local` ≈477–478。TR-0125=`partial_local_scientific`、TR-0135=`partial_local_tiny`（相对诚实）。TR-0206/0327 仍把 MODEL-01 标 `implemented_local` 并指向 `tiny.py`。协议/标题行 **70** 处 `pytest -q`。 |
| **Impact** | 独立审查若信 `implemented_local` 会漏检 A12-01。 |
| **Suggested fix** | MODEL-01 / 未接到论文语义的可执行行改为 `unimplemented` / `pending_server` / 保持 `partial_*`。 |
| **Status** | **confirmed defect**（过称） |

### A12-07 — Fig.6 / FAIL-01 五类失效分类器缺失

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | 无生产符号。`events.py` `align_events` 187 只读 `status=="strategy_change"`；`tasks/t4_boundary.py` 仅四类枚举 |
| **Trigger** | 论文 §9 L353：横轴扰动深度、纵轴约束复杂度；区分漏检、重算错误、嫁接接口、策略分岔、约束退化。FAIL-01。 |
| **Paper requirement** | 失效分类可计算、可落盘；验证器不回退。不是“有 T4 状态字段即可”。 |
| **Repro / evidence** | 生产代码无漏检/嫁接/相图分类器。`repair.failures` 只有 `execute_without_prefill` 一类工程串。TR-0043 仍 `implemented_local`。 |
| **Impact** | C4 主文相图与 FAIL-01 无实现。 |
| **Suggested fix** | 实现五类分类并写入 repair/analyze；未实现则标 `unimplemented`。 |
| **Status** | **confirmed defect**（遗漏段落/功能） |

### A12-08 — 无侧车官方 Symbolic 的 CLI prepare 崩溃

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `_default_edit` 158–165、`_domain_edit` 211–213、`cmd_prepare` 265–271；`tasks/t2_gsm_symbolic.py` 43–44 |
| **Trigger** | 论文 §7 / GOAL §5.2：GSM-Symbolic 路径要有读取与合法编辑；无图则显式 unknown，不是静默发明 DAG，也不是整段 prepare 失败。 |
| **Paper requirement** | 无侧车：placeholder + `graph_status=unknown` + 拒非法编辑，仍应能落盘任务/划分。 |
| **Repro / evidence** | `prepare --kind gsm_symbolic --fixture tests/fixtures/t2_symbolic_one.json` → `ValueError: no editable non-placeholder premise`。加载器本身能读出 `graph_status=unknown`。 |
| **Impact** | 官方 T2 快照无法走 CLI prepare，DATA-02 入口在无侧车时断开。也使 A12-04 的 CLI 共组更难在产物上直接检查。 |
| **Suggested fix** | 无非 placeholder 前提时跳过值编辑，仍写 tasks/splits，编辑标 `unavailable`。 |
| **Status** | **confirmed defect** |

### A12-N1 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 215–257；`cli.py` `cmd_analyze` 1056–1150 |
| **Trigger** | 协议 §6；GOAL §5.14。任务：Gate 未注册 **不是** 缺陷。 |
| **Repro / evidence** | 仅 labels 的 analyze：`gates.*.decision=unregistered`，`scientific_conclusion=None`，`p1=None`，`status=not_evaluated`。`week8_decision({rho_S_excess:0})` → `c3_negative_descriptive`。 |
| **Status** | **non-defect** |

### A12-N2 — tiny 随机权重不是 MODEL-01；夹具不是官方（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `models/tiny.py`；`tasks/t1_fixture.py`；`schema.py` 138–140 |
| **Trigger** | DATA-01；MODEL-01。任务：tiny **不是** MODEL-01；fixture **不是** official。 |
| **Repro / evidence** | 全部 scientific 轨迹 `model=tiny-qwen2`，`weight_source=random_init`。`source_kind=official` 的夹具路径 → `T1 fixture loader requires source_kind=fixture`。schema `official`+`self_authored_arithmetic` → `Self-authored fixtures cannot be marked official`。 |
| **Status** | **non-defect** |

### A12-N3 — analyze 不从 labels 伪造 P1（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `cli.py` `cmd_analyze` 1067–1086 |
| **Trigger** | 论文 §2.6 P1：留出预测 + 链长/op。作者声称拒假 P1。 |
| **Repro / evidence** | 四行 labels 带 `length/op/rho/y`、无 `p1_table.jsonl` → `p1 is None`。scientific label 目录同样。 |
| **Status** | **non-defect** |

### A12-N4 — sham 不再盖到真实前提；$N$ 保持 missing（非缺陷 / 关闭 A10-03）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `measure.py` `build_labels` 72–80；`event_density_sets` 327–349 |
| **Trigger** | 协议 L29；作者 B9-01。 |
| **Repro / evidence** | scientific + sham：观测 `sham:q` `82→53` `changed`。labels 三行：`p1`/`p2` `noise_ref=None`，`sham:q` `1.0`。事件密度 `noise_set` 空、`null_reason=noise_set_missing`，`rho_M_noise`/`rho_M_excess` 为 `None`。**不是** r10 的 `rho_M_noise=0.0` / `rho_M_excess=1.0`。聚合层未复制事件 `null_reason`（顶层 `null_reason=None`），analyze 仍因 `rho_S_excess=None` 走 `not_evaluated`，本轮不升格。 |
| **Status** | **non-defect**（作者关闭成立） |

### A12-N5 — 搜索锥为空时 fit/calibrate 拒绝首次出现序（非缺陷 / 关闭 C6 缺文件路径）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `cli.py` `cmd_fit` 618–619；`cmd_calibrate` 775–776 |
| **Trigger** | 作者 C6-M-01 residual。 |
| **Repro / evidence** | 孤立目录无 `tasks.jsonl`：两阶段均 `ValueError`。有 collect 副本时 `_e_premise_ids=[p1,p2]`。helper `_e_premise_ids(None, labels)=[p2,p1]` 仍在，但默认入口不再调用。错题绑定见 A12-03，**不是**本条重开。 |
| **Status** | **non-defect**（缺文件路径关闭） |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5，也不能认证已漂的冻结。

1. **Gate 0–2**：无阈值、无 pass/fail（A12-N1）。
2. **`scientific_conclusion` 保持 `None`**。
3. **tiny 不是 MODEL-01**；**夹具不是 official**（A12-N2）。
4. **REST-01/02/03** 禁词列表存在；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
5. **身份对齐不含值**。
6. **$R_{\mathrm{task}}$ 祖先**、库层 $S/M$ 空分母→null。
7. **交换公式**、几何报告 **不**写 `timing=pre_step`（scientific intervene `timing=offline_hidden`）。
8. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$。[0.1, 0.2, 0.3, 0.4], α=0.4 → $q=0.3$；α=0.1 → $+\infty$。
9. **4096 vs 3584 直接迁移 N/A**。
10. **官方 iGSM** 拒裸 `G`、排除共享 RNG、mod 23。
11. **宿主 exec 被禁止**；`ChildProcessExecutor` 不冒称沙箱。
12. **假说不要求正结果**。
13. **scientific 调用 generate**；题干 `p1`/`p2` **不是**事件；`parse_region=generated`。
14. **scientific $H=(7,32)$ 全有限**，行=可表达事件，`hidden_layer=1`，$E=(2,32)$。
15. **`source_value_pair` 落盘且图 id/表达式已改写**。
16. **有本任务 `tasks.jsonl` 时 CLI $E$ 列跟 `task.premises`**（默认 collect 已复制）。
17. **无任务且搜索锥为空时 fit/calibrate 失败**（A12-N5）。
18. **analyze 拒假 P1**。
19. **PCA `n<min d` → `truncated=True`**。
20. **T3 prepare 不强制 SVP**。
21. **verbalizer 库层** `17` 不再子串命中。
22. **sham 不写入真实前提 $N$**（A12-N4）。
23. **标量 Prefill 拒绝**。
24. **donor=`same_source_diff_value`；INLP=`inlp`；`ie_z_g=target_follow`**（字段；对象仍受 A12-01 限制）。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_scientific_prepare_emits_parseable_events` | 每条轨迹 ≥1 事件且含 `q` | 事件是生成步骤；拒绝 `constrained_target` |
| `test_generated_events_exclude_prompt_assignments` | `start≥prompt`；`parse_region=generated` | 非 teacher-force 目标行 |
| `test_scientific_h_is_finite_and_pairs_donor` | $H$ 有限；intervene `timing≠pre_step` | $H$ 对应自然步；$R_{\mathrm{behavior}}$ |
| `test_plus_locks_symbolic_family_to_test` | 同进程先 load Plus（开审）；交卷后或再断言 persist | CLI 新进程 / 只 prepare Symbolic / 清空后的家族表 |
| `test_fit_without_tasks_jsonl_refuses_first_seen_order` | `run/prep` 与 `orphan/` 分离时拒绝 | 祖先名为 `col/`/`prep/` 的错题 `tasks.jsonl` |
| `test_sham_hits_do_not_broadcast_real_premises_into_n` | `build_labels` 不给 `p1`/`p2` 写 `noise_ref` | （此项论文语义已锁） |
| `test_analyze_refuses_fake_p1_from_labels` | 无 `p1_table` → `p1 is None` | （此项已锁） |
| `test_verbalizer_uses_extracted_answer_not_substring` | `17`/`70`/`boxed` | 同划分四档模型自述 |

---

## 8. 本审查复跑的命令（均可再跑；树已漂则划分结果不能认证声明 hash）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → 开审 **61** / `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`；交卷 **61** / `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `python -m pytest -q --tb=line` → **156 passed**（开审 MATCH 树，23.72s）。
4. `generate_task_trace` + `prepare --eval-mode scientific --sham-opportunities 1` → 7 条 tiny 轨迹，全部 `constrained_target`，各 1 个 `q` 事件；SVP 图为 `p2_src` / `p1 * p2_src`；观测含 `sham:q` `82→53`。
5. `collect --backend tiny --eval-mode scientific` → $H=(7,32)$ 全有限，`tasks.jsonl` 被复制，`event_rows` 7 行皆 `q`，`hidden_layer=1`。
6. `label` / `fit`：task 头有限 $U$；行为头无已知标签；verbalizer 回显抽出 `82`。有任务 `_e_premise_ids=[p1,p2]`；helper(None)=`[p2,p1]`。
7. 密度：`p1`/`p2` `noise_ref=None`；`sham:q` `1.0`；事件 `null_reason=noise_set_missing`。
8. 孤立无 `tasks.jsonl` → fit/calibrate `ValueError`。祖先 `col/WRONG-TASK`（前提对调）→ fit 0，$E$=`[p2,p1]`。
9. analyze（仅 labels / 假字段）→ `p1=None`，Gate `unregistered`。
10. Plus/Symbolic：`gsm8k-1` 无锁 → `probe_train`；同进程先 Plus → `test`。无侧车 Symbolic prepare → `no editable non-placeholder premise`。
11. 夹具标 official → 拒绝。PCA `(2,5)` vs `(2,3)` → `truncated=True`。保形 / $\Pi=I$ 交换 / 标量 Prefill：见 §5–§6。
12. `intervene --dev-layer-scores 0.05 0.9 0.8` → `timing=offline_hidden`，`donor_kind=same_source_diff_value`，`inlp_transform=inlp`，`ie_z_g=target_follow`。

---

## 9. 结论

**冻结 hash：开审 HASH_MATCH `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（61 文件）；交卷 HASH_MISMATCH `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（`splits.py` 与 `test_round07_regressions.py` 已改）。**

**原文一致性：不通过（FAIL）。**

作者 r12 关闭表中，下列在**未漂的 59 文件**上接口已接通，不得原样重开：无任务且搜索锥为空时拒绝首次出现序；collect 复制任务文件；有本任务时 $E$ 列序；sham 不写入真实 $N$；改名改图；拒假 P1；Gate 未注册；夹具≠官方；T3 不走 SVP；PCA truncated；标量 Prefill；生成区事件与有限 $H$。

科学入口仍在三处断开，且冻结已破：

1. **概念偷换：** `constrained_target` 的 `\nq = 82` 被当成 §4.1 成功 $T$（A12-01/02）。`generate.py` 未改。
2. **划分泄漏：** Plus 家族锁在声明冻结上是进程内 `set`。CLI 单独 Symbolic / 清空后，`gsm8k-1` 可进 `probe_train`（A12-04）。交卷 persist 不能关闭声明 hash。
3. **列身份新门：** 为关 C6 而做的 4 层目录名搜索，会静默使用祖先 `col/tasks.jsonl`，把 $E$ 写成错题的 `[p2,p1]`（A12-03）。

另有 verbalizer 回显、账本过称、Fig.6 分类器缺失、无侧车 Symbolic prepare 崩溃。Gate 未注册、tiny 不是 MODEL-01、假说不要求正结果——这三条被遵守。作者关闭与 156 绿测不能关闭本通道。真实权重/官方全量是 `pending_server`，不能解释本机把约束赋值写成 $T$，也不能解释把另一题的前提序写成 $E$。

独立复审关闭条件（本通道）：先重冻并在**同一 hash** 上再开 A–F；A12-01/02 必须对照原文关闭（自然步骤事件，或对 `constrained_target` 诚实拒绝并降级账本）；A12-03 须停止祖先目录碰运气，或校验 `task_id`；A12-04 须在 CLI/跨进程共组 Plus 家族。其余 medium 项至少改为诚实状态。A12-H1 关闭条件是 VERSION 与磁盘复算一致且审查期间不变。

**不把 Goal 标为完成。**
