# 审查报告 A：原文一致性（paper consistency）— round-10

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-10 |
| **审查时间** | 2026-09-21 02:21–04:15（UTC+8） |
| **声明冻结 hash** | `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`（61 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **HASH_MATCH。** 按 `VERSION.md` 原文 Python 逐字复算：文件数 **61**，摘要 `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`。相对 r08 的 60 文件 / `1b88bec2…` 与 r09 的 `9ffc4cd9…` 已变；审查对象即该冻结工作树。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `39CF907C0B66B9B26AE7355E394848CFA1FF41CE5166310E1DC0A9307F9AC498`（与账本 §0 一致） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-10/` 下除 `VERSION.md` 与本文件外的任何通道报告。**未把** `ISSUES.md` 作者关闭当作关闭。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |
| **作者声称 pytest** | VERSION 写 153 passed。本通道复跑 `python -m pytest -q --tb=line` → **153 passed**（19.91s）。绿测不关闭原文符合性。 |

**总判：不通过。** 冻结 hash 可核验。相对作者 r10 关闭表，本轮独立复跑后**不得原样重开**：`collect` 复制 `tasks.jsonl`；默认 scientific fit 在找得到任务文件时 $E$ 列跟 `task.premises`；改名对重写 id/parents/expression；analyze 不从 labels 伪造 P1；Gate 保持 `unregistered`；夹具不能标 official；T3 prepare 不再走 `source_value_pair`；PCA `n<min d` 标 `truncated`；生成区事件、$H$ 有限、`sham:` 前缀观测存在。

本轮仍 FAIL，因为：(1) scientific 仍把 teacher-force `\nq = <两位数字>` 当作 §4.1 成功事件；(2) 无编辑 sham 变化被盖到真实前提上，密度把 $N=\{p1,p2\}$ 记成已评估且 $\rho_M^{\mathrm{noise}}=0$；(3) Plus→Symbolic 家族锁只活在进程内 RAM，CLI 单任务 prepare Symbolic **不会**看到 Plus，`gsm8k-1` 等家族可进 `probe_train`。假说不要求正结果。Gate 0–2 保持 `unregistered`，**不是缺陷**。tiny 随机权重 **不是** MODEL-01。不把 Goal 标为完成。

---

## 0. 相对作者关闭表的独立复跑（避免把已修项当新缺陷）

`ISSUES.md` / `VERSION.md` 的 r10 local close **只作对照清单**。本通道在当前字节上重跑后：

| 作者声称已关 | 本轮复跑 |
|---|---|
| `collect` 复制 `tasks.jsonl`；fit/calibrate 搜 parent `prepare/` | **成立（默认路径）。** scientific collect 写出 `col/tasks.jsonl`；`_find_tasks_jsonl(col, lab)` 命中该副本。无任务时 helper 仍是首次出现序，见 A10-05。 |
| 标量/`[0]` Prefill 拒绝 | 源码 `_hidden_is_prefill` 拒标量/`bool`/`[0]`/空。本通道未当作原文主缺陷重开。 |
| T3 prepare 不再强制 `source_value_pair` | **成立。** hotpot prepare exit 0，`edits.kind=['document']`，无 SVP。 |
| 改名重写 id/表达式 | **成立。** SVP `same_value_diff_source`：`p2_src`，`expression=p1 * p2_src`，`parents=['p1','p2_src']`。**不得**按“rename-only”重开。 |
| Plus 锁族，Symbolic 共组到 test | **仅同进程先 load Plus 时成立。** CLI 单任务 / 新进程下 `gsm8k-1` → `probe_train`。见 A10-04。夹具 `gsm8k-12` 哈希本身就落在 `test`（$0.956$），不能证明锁有效。 |
| analyze 拒假 P1 | **成立。** 仅 `labels.jsonl`（含 length/op/rho/y）→ `p1=None`，`scientific_conclusion=None`。 |
| PCA `n<min d` → `truncated=True` | **成立。** `(2,5)` vs `(2,3)` → `not_applicable_too_few_rows`；`eye(4)` vs `eye(3)` → `truncated=False`。 |
| 映射真实前提的 hit 记入 $N$；`sham:` 仍 missing | **科学入口不成立。** CLI labels 把 `noise_ref=1.0` 盖到 `p1`/`p2`，密度 `null_reason=None`、`rho_M_noise=0.0`。见 A10-03。 |
| review merge | `merge_review` 存在。非本通道主缺陷。 |
| 约束 `\nq=` 是本机接口、不是 §4.1 | **作者声明，不是关闭。** scientific prepare 仍接受 `constrained_target` 为成功。见 A10-01。 |

---

## 1. 逐文件覆盖

每行：路径 — 磁盘 `splitlines()` 行数 — SHA-256 前 16 位 — 对照条款 — 覆盖结论。

| 文件 | 行 | digest | 对照条款 | 覆盖结论 |
|---|---:|---|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 517 | `f3c0ec087b5bf4e5` | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 86 | `83a9142dba4f7fcd` | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。L29：无编辑随机变化不得强加前提身份。Gate 保持 null。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 166 | `b9e0a8ea3fc87bf0` | GOAL §5 = L73–91 | 已通读。§5.3/5.5/5.7/5.14 在科学入口仍被降级或替身。 |
| `.planning/REQUIREMENTS.md` | 76 | `39cf907c0b66b9b2` | DATA/MEAS/MODEL/… 与 atomics | 复选框全空；状态表仍写 `implemented_local` / `implemented_local_tiny`。 |
| `.planning/PAPER_TRACEABILITY.md` | 抽样约定 + TR-0125/0135/0158/0206/0327/0400 | — | 账本不得当实现证据 | 528 条。`implemented_local=478`。可执行行 TR-0125=`partial_local_scientific`，TR-0135=`partial_local_tiny`；TR-0206/0327（MODEL-01）仍 `implemented_local`。协议/标题行仍 **70** 处 `python -m pytest -q`。 |
| `pyproject.toml` | 27 | `cb44851f7fbf7bf7` | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 有 `torch`/`transformers`。 |
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58d` | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 4 | `307299fda7b77d22` | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a45` | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。拒 `official`+自建夹具。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277` | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先正确。默认 cone 走任务祖先，不是 $\hat R^{\mathrm{val}}$。 |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814` | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 | `parse_events` 仍把前提与节点都当赋值。`merge_review` 可回填。策略只读 `status=="strategy_change"`。 |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccf` | §7 T1 重算；GOAL §5.2 | 值编辑+重算正确。`apply_rename_edit` **重写** id/parents/expression。 |
| `src/reasoning_diff/measure.py` | 388 | `c81e2402671228b6` | §2.6 $S/M/\rho$；协议 L29 | 差集/空分母公式在。`build_labels` 把 sham 变化盖到同事件全部前提行；`event_density_sets` 再把那些行当“已映射 $N$”。 |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63b` | §2.6 P1–P3；Gate；S2–S4 | P1 只吃 `p1_table.jsonl`。Gate `unregistered`。`scientific_conclusion=None`。 |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649` | §2.4 交换/对照/INLP/$\mathrm{IE}_Z$ | 库层公式正确。CLI 相对对照常为 `None`（无 `--dev-layer-scores`）。 |
| `src/reasoning_diff/probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec` | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、未知掩码正确。CLI tiny `rank=min(64,d)`。 |
| `src/reasoning_diff/probes/boundary.py` | 44 | `ce3b549be7d671ff` | §4.2 Hidden=256 ReLU | 架构符合。CLI 用全 1 标签。 |
| `src/reasoning_diff/probes/calibrate.py` | 45 | `e8b3ed3459bb22c5` | §2.5 命题 2 | 分位数与 $+\infty$ 正确。 |
| `src/reasoning_diff/probes/__init__.py` | 3 | `3065196db28e929c` | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4` | §8 四档自述；GOAL §5.7 | 库层走 `extract_answer`。CLI `generate_fn` 回显前缀。 |
| `src/reasoning_diff/transfer.py` | 86 | `5549f84bd1bd6240` | §5 Fig.2c；S3；GOAL §5.9 | 直接迁移拒 4096/3584。`n<dim` → `truncated=True`。 |
| `src/reasoning_diff/repair.py` | 232 | `f76ff9998b9a6b17` | §3/§9 嫁接；GOAL §5.13 | Prefill 拒标量/`[0]`。掩码仍改前缀字符串。无 Fig.6 五类失效分类器。 |
| `src/reasoning_diff/cli.py` | 1251 | `ba474e1fea1f7c5a` | §4 流水线；§8.2 scientific | scientific prepare **只拒** `parse_failed`，**接受** `constrained_target`。collect 复制 `tasks.jsonl`。fit 找得到任务则跟前提序。 |
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
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f` | §7 T2；评测专用 | `register_test_only_family` 写**进程内**集合。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354` | §7 T2 | 无侧车 placeholder + `unknown`。CLI 单任务 prepare **不**加载 Plus。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d56149` | §7 T2-noop | 可造配对。无注入句值扰动扫描。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb` | §7 T3 | supporting_facts ≠ DAG。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0` | §7 T3 | `composition_reference` 不可重算。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7` | §7 HumanEval；GOAL §5.15 | 无新解则 `needs_truth`。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f88` | §7 T4；Fig.6 | 四类状态枚举在。无相图分类器。 |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3` | — | 注释。 |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78` | GOAL §5.15 | 禁宿主 exec。`ChildProcessExecutor.isolated_sandbox=False`。 |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122` | §3 域内评分 | 数值/QA 精确匹配。代码经执行器。 |
| `src/reasoning_diff/splits.py` | 152 | `08f77e972927a996` | §4.1 共组；DATA-03 | 家族锁 = 模块级 `set`。默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 53 | `2098c2c72a852eaa` | GOAL §5.4 | 五流分离。 |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd3` | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 85 | `524657027e9b402f` | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb` | — | 夹具路径。 |
| `tests/test_round07_regressions.py` | 169 | `cad435add5103d94` | 作者 r10 锁 | 锁 in-process Plus→Symbolic、假 P1、rename 图、`n<d`。**不**锁 CLI 跨进程共组；**不**锁拒 `constrained_target`；噪声单测绕过 `build_labels`。 |
| 其余 `tests/*.py` | 见表下 | — | 替身锁 | 抽读 r05/r06/r07：锁生成区有 `q`、$H$ 有限、timing≠`pre_step`。 |

其余测试文件（行 / digest）：`test_artifacts.py` 73/`830953f379954233`；`test_cli_pipeline.py` 30/`ff826b3e553f003b`；`test_generate_loop.py` 17/`ffe10b0d6812908c`；`test_measure.py` 40/`fbc68abd89ed109e`；`test_review_regressions.py` 397/`d3814498fe52b28b`；`test_round03_regressions.py` 292/`61247e8a074944a3`；`test_round04_regressions.py` 311/`25949c80bbb55585`；`test_round05_regressions.py` 197/`bc837c0c3a6ea3ae`；`test_round06_regressions.py` 145/`ac7e4e88248ff49e`；`test_science.py` 103/`cdb5f1460502ba3c`；`test_t1_official.py` 31/`f4b3cbc1fcd5371e`；`test_t2_gsm.py` 33/`f66a95bb737dc973`；`test_t3_t4.py` 44/`d0381c097d04bc9d`；`test_tiny_cache.py` 26/`83ae0441140f7e17`；`test_tiny_hooks.py` 27/`e28e58b638568d89`；`test_tracer_t1_prepare.py` 100/`62a5e2f168a20e8f`。

第三方库：审查了本项目对 `numpy` / 可选 `torch`+`transformers` 的使用假设，未审查依赖源码。

夹具通读：`tests/fixtures/t1_tiny.json`、`t1_official_shape.json`、`t2_gsmplus_one.json`、`t2_symbolic_one.json`。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。L29 被 scientific 密度路径违反（A10-03）。Gate 保持 null。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 3、5、7 条在科学入口被替身。第 14、15 条持守。 |
| C4 | 账本约定 + TR-0125/0135/0158/0206/0327/0400 | TR-0125=`partial_local_scientific`。MODEL-01 行仍 `implemented_local`。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。 |
| C6 | 库函数手核：$R_{\mathrm{task}}$、差集、交换、分位数、直接迁移、P1、cone、PCA | 库层公式符合。PCA truncated 符合作者声称。噪声 **CLI 路径不符合** 协议 L29。 |
| C7 | §4.1 伪代码 vs scientific prepare/collect/label/fit | generate 在；解析区=生成段；对象是 teacher-force 目标行；`constrained_target` 被接受。 |
| C8 | 生成区事件、有限 $H$、SVP 图、`sham:` 前缀、密度 | 事件 `start≥prompt`；$H=(7,32)$ 全有限；SVP 图已改写；观测有 `sham:q`；密度把 sham 盖成真实 $N$。 |
| C9 | 首次出现序 / 假 P1 / Gate / 夹具官方 | 有任务时 $E$ 序=`[p1,p2]`；无任务 helper=`[p2,p1]`。假 P1 拒。Gate `unregistered`。夹具拒 official。 |
| C10 | Plus/Symbolic 家族 | 同进程先 Plus 则锁 test。Symbolic 单独、`original_id=gsm8k-1` → `probe_train`。夹具 `gsm8k-12` 哈希已是 test。 |
| C11 | `python -m pytest -q --tb=line` | **153 passed**。不作为原文关闭。 |
| C12 | VERSION 冻结脚本逐字复算 | **HASH_MATCH** 61 / `81308124…4b6d`。 |
| C13 | 论文/协议/GOAL/REQUIREMENTS SHA-256 | 四份与账本 §0 一致。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 真实 Qwen3-8B / R1-7B、GPU、官方 500 题 | 协议 §7：`pending_server`。tiny 不是替代。 |
| N2 | 人工复核事件映射小集 | 有 export/merge，无抽样协议实现。 |
| N3 | 独立数据重拟合探针/INLP/Procrustes | 标签对象不是生成步骤上的 $R_{\mathrm{behavior}}$。 |
| N4 | 其他 round-10 通道报告交叉 | 任务禁止阅读。 |
| N5 | `PAPER_TRACEABILITY.md` 全部 528 条逐字 | 已读约定与高风险行。其余多为同模板。 |
| N6 | 合格隔离沙箱跑 HumanEval | 无合格隔离后端。 |

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
| 论文 2.5 | 132–139 | $a(X)$ 列 = $E$ 行 | math | 有 `tasks.jsonl` 时跟前提序；无任务仍首次出现 | subst / ok-lib |
| 论文 2.6 / 协议 2 | 154–158 / L29 | 噪声先扣；不得给无编辑变化强加前提身份 | math/proto | sham 变化盖到 `p1`/`p2`，再当已评估 $N$ | subst |
| 论文 4.1 | 232–253 | `T0=generate` 后 `parse_events(T0)` | exec | 解析生成区；对象是 teacher-force 行 | subst |
| 论文 7 | 403–405 | Plus test-only；同族共组 | proto | 锁在进程内 set；CLI Symbolic 单独可进 train | subst |
| 论文 8.2 | 419–431 | scientific 自然轨迹 | exec | 开关在；后续标签/$H$ 不是论文对象 | subst |
| 论文 9 | 353 | Fig.6 五类失效 | exec | T4 枚举在；无相图分类器 | missing |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |
| DATA-01 | — | 夹具不得冒称官方 | proto | `t1_fixture` 拒 official；schema 拒 official+自建 | **ok** |

---

## 5. Findings

### A10-01 — scientific 事件是约束目标行，不是 §4.1 生成步骤

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/generate.py` `append_target_assignment` 72–98、`generate_task_trace` 135–160；`cli.py` `cmd_prepare` 296–297 |
| **Trigger** | 论文 §4.1 L232–248：`T0=generate` 之后 `parse_events` 的对象是**生成轨迹**上的变量/表达式/版本/作用域。§2.1：$T$ 是模型生成序列的步骤离散化，$P$ 不是 $T$。§8.2：自然轨迹。GOAL §5.3。作者 ISSUES 写“约束 `\nq=` 是本机接口、不是 §4.1”——**作者声明，不是关闭**。 |
| **Paper requirement** | 自然轨迹步骤事件。无自然步骤时应拒绝 scientific 或标 `unimplemented`，不得把约束接口写成已测 §4.1。 |
| **Repro / evidence** | 独立 `generate_task_trace(seed=0)`：文本 `'p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82'`，`parse_status=constrained_target`，`parse_region=generated`，`target_assignment='\nq = 82'`，事件仅 `q=82`（`start=45≥prompt_len=36`）。`prepare --eval-mode scientific` + 六比例 + `--sham-opportunities 1` → exit 0，**7** 条轨迹 **全部** `constrained_target`（含 source/extra/sham）。prepare **只拒** `parse_failed`。r06/r07 测试只锁“生成区、有 q、非题干预复述”。 |
| **Impact** | C1/C3 入口没有“生成步骤上的编辑响应”。约束数字是本机可解析接口，**不是** §4.1 自然 CoT；实现却把它当作 scientific 成功。 |
| **Suggested fix** | 只把自然 decode（或官方 CoT）解析为事件。`constrained_target` 时 scientific prepare/label/collect 拒绝或降级账本。不要 teacher-force 赋值行来凑事件。 |
| **Status** | **confirmed defect**；真实 CoT 质量 **pending_server** |

### A10-02 — $R_{\mathrm{behavior}}$ 比较的是约束数字，不是生成步骤值

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` `_observations` 229–254；`measure.py` `build_labels` 29–53；`generate.py` 72–98 |
| **Trigger** | 论文 §2.2 L74–78：固定 $M,u$ 下 $v_i(P\oplus\delta(p_j))\ne v_i(P)$。GOAL §5.3。事件定义见 A10-01。 |
| **Paper requirement** | 行为标签来自对齐生成步骤的语义值变化。未知不作答案。 |
| **Repro / evidence** | 本机 observations：`(q,p2)`/`(q,p1)` `82→82` `no_change`；sham `82→53` `changed`（`premise_id=sham:q`）。labels：`(q,p2)`/`(q,p1)` `task_label=1`，`behavior_label=None`。scientific `fit` 只写出 **task** 头（loss `0.05036`）；行为头 `no_known_labels`。 |
| **Impact** | 差集 $S$ 在本机是空行为集对满任务祖先。即使约束数字因提示词改写而变，那也是 teacher-force 采样对前缀的敏感，不是 §2.2 的 $v(s_i)$。 |
| **Suggested fix** | 先关闭 A10-01。无生成步骤则不写行为标签。 |
| **Status** | **confirmed defect** |

### A10-03 — 无编辑 sham 被盖到真实前提，$N$ 记成已评估 0

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `measure.py` `build_labels` 72–77；`event_density_sets` 327–345；`cli.py` `cmd_prepare` 308–329 |
| **Trigger** | 论文 §2.6 L158：同题不同随机流的表观 $\rho_S$ 必须先扣。协议 L29 / GOAL §5.4：**不能给一个无编辑随机变化强加具体前提身份**。作者声称“映射到真实前提的 hit 记入 $N$；仅 `sham:` 仍 `noise_set_missing`”。`test_c7_m01_mapped_noise_premise_is_deducted` **直接**喂 `noise_set=["p3"]`，绕过 `build_labels`。 |
| **Paper requirement** | `sham:` / 无编辑 seed 变化不得映射到 $p_j\in P$。未映射 hit → excess null，不得记已评估 0。 |
| **Repro / evidence** | scientific prepare 观测：`premise_id=sham:q`，`82→53` `changed`。labels：**三行** `noise_ref=1.0`，包括 `p1`/`p2`/`sham:q`。`event_density_sets`：`hits` 含 `p1,p2,sham:q` → `real_hits=[p1,p2]` → `noise_set={p1,p2}`、`evaluated=True`。$T=\{p1,p2\}=N$ → `rho_M_noise=0.0`，`rho_M_excess=1.0`，`null_reason=None`。这是把无编辑变化**强加**到真实前提后的 booked-zero 噪声，不是“`sham:` 保持 missing”。 |
| **Impact** | Week-8 / C3 若读到 `rho_M_noise=0` 会当成“噪声已评估且为零”。协议要求的 missing/null 被绕过。作者关闭项在科学入口为假。 |
| **Suggested fix** | `build_labels` 不得把 sham 变化写到真实 `premise_id` 行。`event_density_sets` 只把**观测本身**的 `premise_id∈P` 且非 `sham:` 记入 $N$。仅 `sham:` hit → `noise_set=None`。 |
| **Status** | **confirmed defect** |

### A10-04 — Plus/Symbolic 家族锁只在进程内；CLI 单任务 Symbolic 可进拟合划分

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `splits.py` `_TEST_ONLY_FAMILY_KEYS` 10、`register_test_only_family` 35–38、`split_for_task` 95–121；`tasks/t2_gsm_plus.py` 22；`cli.py` `_load_task` 168–184 |
| **Trigger** | 论文 §7 L403–405；DATA-03；GOAL §5.5：测试专用及同基础题全部变体共组，不得拟合。作者声称 Plus `register_test_only_family` 后 Symbolic → `test`。`test_plus_locks_symbolic_family_to_test` **先** `load_gsm_plus` **再** `load_gsm_symbolic`（同进程）。 |
| **Paper requirement** | 与 Plus 同族的 Symbolic 必须是 test。锁必须落在划分产物上，不能依赖“碰巧先 import 过 Plus”。 |
| **Repro / evidence** | `assign_split("gsm8k-1")` → **`probe_train`**（哈希 $0.156$）。`assign_split("gsm8k-12")` → `test`（哈希 $0.956$，夹具巧合）。清空锁后 `load_gsm_symbolic`（`original_id=fam-0`，哈希落在 train）→ `split_for_task=probe_train`，`family_locked_test=False`。同进程再 `load_gsm_plus` → 两者才是 `test`。CLI `_load_task` 一次只加载一个 snapshot；每次 `python -m reasoning_diff prepare` 是新进程，模块级 `set` 为空。CLI Symbolic 单独 prepare 在无侧车时先因“无非 placeholder 前提”崩溃（见 A10-09）；即便补上侧车，也不会去读 Plus 记录。 |
| **Impact** | 同 `gsm8k-1` 家族：Plus 永远 test，Symbolic 可进 `probe_train`。探针/校准可看到测试专用家族。作者测试锁住的是 in-process 副作用，不是论文共组。 |
| **Suggested fix** | 划分时按磁盘上的 Plus/test-only 家族表（或显式 siblings）锁族，不要用进程内全局 set。读不到家族表则拒绝拟合角色。 |
| **Status** | **confirmed defect** |

### A10-05 — 无任务文件时 $E$ 列仍是 labels 首次出现序

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `_e_premise_ids` 707–716；`cmd_fit` 614–618 |
| **Trigger** | 论文 §2.5 L132–134：列 $j$ 与 $E$ 同行 = 原始前提。作者声称 collect 复制 + 搜索 parent 已关 C6-M-01。 |
| **Paper requirement** | `predict_matrix` 列 = $E$ 行 = `task.premises`。读不到任务应拒绝，禁止回退首次出现序。 |
| **Repro / evidence** | 本机 labels 首次出现 `[p2,p1]`（`_default_edit` 先改零值 p2）。`_e_premise_ids(task, labels)=[p1,p2]`；`_e_premise_ids(None, labels)=[p2,p1]`。默认 scientific：collect 有 `tasks.jsonl`，`_find_tasks_jsonl` 命中。`cmd_fit` 在 `task_path is None` 时**不拒绝**。 |
| **Impact** | 默认路径的 0.2 反例保持关闭，**不得原样重开**。残留回退仍会把 $Y$ 的 p2 写到 $E$ 的 p1 列。 |
| **Suggested fix** | 找不到 `tasks.jsonl` 则 fit/calibrate 失败。 |
| **Status** | **confirmed defect**（无任务回退）；有任务的默认 scientific fit **本轮不重开** |

### A10-06 — CLI 四档 verbalizer 回显前缀，把约束数字当成自述命中

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_fit` 653–656；`baselines.py` 92–125 |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7。库层子串打分 **不得重开**。 |
| **Paper requirement** | 四档自述与探针同样本/划分/可见前缀，且是模型生成，不是回显轨迹。 |
| **Repro / evidence** | CLI `generate_fn=lambda p, t=prefix: t`。scientific fit：zeroshot/fiveshot/reflection `score=1.0`，`extracted='82'`。 |
| **Impact** | 第 8 节“说不出来”在 CLI 上仍不是同划分模型自述。 |
| **Suggested fix** | CLI 按同一划分调用真实生成；未接线不得标 `implemented_local`。 |
| **Status** | **confirmed defect**（CLI 替身）；子串打分 **本轮不重开** |

### A10-07 — 账本仍大量 `implemented_local`（含 MODEL-01）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` TR-0206、TR-0327、TR-0158、TR-0400；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：未实现不得标已实现。r07 可执行行验证列已改 `tests_exist_not_acceptance`，**不得**按“pytest 关闭可执行行”重开。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。tiny 不是 MODEL-01。 |
| **Repro / evidence** | `implemented_local=478`。TR-0125=`partial_local_scientific`、TR-0135=`partial_local_tiny`（相对诚实）。TR-0206/0327 仍把 MODEL-01 标 `implemented_local` 并指向 `tiny.py`。TR-0158/0400 仍指向 `intervention_report`。协议/标题行 **70** 处 `pytest -q`。 |
| **Impact** | 独立审查若信 `implemented_local` 会漏检 A10-01。 |
| **Suggested fix** | MODEL-01 / 未接到论文语义的可执行行改为 `unimplemented` / `pending_server` / 保持 `partial_*`。 |
| **Status** | **confirmed defect**（过称） |

### A10-08 — Fig.6 / FAIL-01 五类失效分类器缺失

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | 无生产符号。`events.py` `align_events` 187 只读 `status=="strategy_change"`；`tasks/t4_boundary.py` 仅四类枚举 |
| **Trigger** | 论文 §9 L353：横轴扰动深度、纵轴约束复杂度；区分漏检、重算错误、嫁接接口、策略分岔、约束退化。FAIL-01。 |
| **Paper requirement** | 失效分类可计算、可落盘；验证器不回退。不是“有 T4 状态字段即可”。 |
| **Repro / evidence** | `rg` 生产代码无漏检/嫁接/相图分类器。`repair.failures` 只有 `execute_without_prefill` 一类工程串。 |
| **Impact** | C4 主文相图与 FAIL-01 无实现。账本 TR-0043 仍 `implemented_local`。 |
| **Suggested fix** | 实现五类分类并写入 repair/analyze；未实现则标 `unimplemented`。 |
| **Status** | **confirmed defect**（遗漏段落/功能） |

### A10-09 — 无侧车官方 Symbolic 的 CLI prepare 崩溃

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `_default_edit` 158–165、`_domain_edit` 211–213、`cmd_prepare` 265–271；`tasks/t2_gsm_symbolic.py` 43–44 |
| **Trigger** | 论文 §7 / GOAL §5.2：GSM-Symbolic 路径要有读取与合法编辑；无图则显式 unknown，不是静默发明 DAG，也不是整段 prepare 失败。 |
| **Paper requirement** | 无侧车：placeholder + `graph_status=unknown` + 拒非法编辑，仍应能落盘任务/划分。 |
| **Repro / evidence** | `prepare --kind gsm_symbolic --fixture tests/fixtures/t2_symbolic_one.json` → `ValueError: no editable non-placeholder premise`（`_domain_edit` 与 except 里再次 `_default_edit`）。加载器本身能读出 `graph_status=unknown`。 |
| **Impact** | 官方 T2 快照无法走 CLI prepare，DATA-02 入口在无侧车时断开。 |
| **Suggested fix** | 无非 placeholder 前提时跳过值编辑，仍写 tasks/splits，编辑标 `unavailable`。 |
| **Status** | **confirmed defect** |

### A10-N1 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 215–257；`cli.py` `cmd_analyze` 1056–1150 |
| **Trigger** | 协议 §6；GOAL §5.14。任务：Gate 未注册 **不是** 缺陷。 |
| **Repro / evidence** | 仅 labels 的 analyze：`gates.*.decision=unregistered`，`scientific_conclusion=None`，`p1=p2=p3=None`，`status=not_evaluated`。有阈值才 `compared`，仍无 `pass`。 |
| **Status** | **non-defect** |

### A10-N2 — tiny 随机权重不是 MODEL-01；夹具不是官方（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `models/tiny.py`；`tasks/t1_fixture.py`；`schema.py` 138–140 |
| **Trigger** | DATA-01；MODEL-01。任务：tiny **不是** MODEL-01；fixture **不是** official。 |
| **Repro / evidence** | 全部 scientific 轨迹 `model=tiny-qwen2`，`weight_source=random_init`。`source_kind=fixture` 标 official → `Self-authored fixtures cannot be marked official`。官方快照拒裸 `G`、mod 23、答案 9 与 template 重算一致。 |
| **Status** | **non-defect** |

### A10-N3 — analyze 不从 labels 伪造 P1（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `cli.py` `cmd_analyze` 1067–1086 |
| **Trigger** | 论文 §2.6 P1：留出预测 + 链长/op。作者声称拒假 P1。 |
| **Repro / evidence** | 四行 labels 带 `length/op/rho/y`、无 `p1_table.jsonl` → `p1 is None`。scientific label 目录同样。 |
| **Status** | **non-defect** |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5。

1. **Gate 0–2**：无阈值、无 pass/fail（A10-N1）。
2. **`scientific_conclusion` 保持 `None`**。
3. **tiny 不是 MODEL-01**；**夹具不是 official**（A10-N2）。
4. **REST-01/02/03** 禁词列表存在；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
5. **身份对齐不含值**。
6. **$R_{\mathrm{task}}$ 祖先**、库层 $S/M$ 空分母→null。
7. **交换公式**、几何 **不**写 `timing=pre_step`（库/既有路径）。
8. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$。
9. **4096 vs 3584 直接迁移 N/A**。
10. **官方 iGSM** 拒裸 `G`、排除共享 RNG、mod 23。
11. **宿主 exec 被禁止**；`ChildProcessExecutor` 不冒称沙箱。
12. **假说不要求正结果**。
13. **scientific 调用 generate**；题干 `p1`/`p2` **不是**事件；`parse_region=generated`。
14. **scientific $H=(7,32)$ 全有限**，行=可表达事件，`hidden_layer=1`，$E=(2,32)$。
15. **`source_value_pair` 落盘且图 id/表达式已改写**（不得按 rename-only 重开）。
16. **有 `tasks.jsonl` 时 CLI $E$ 列跟 `task.premises`**（默认 scientific collect 已复制）。
17. **analyze 拒假 P1**。
18. **PCA `n<min d` → `truncated=True`**。
19. **T3 prepare 不强制 SVP**。
20. **verbalizer 库层** `17`/`70`/`boxed` 不再子串命中。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_scientific_prepare_emits_parseable_events` | 每条轨迹 ≥1 事件且含 `q` | 事件是生成步骤；拒绝 `constrained_target` |
| `test_generated_events_exclude_prompt_assignments` | `start≥prompt`；`parse_region=generated` | 非 teacher-force 目标行 |
| `test_scientific_h_is_finite_and_pairs_donor` | $H$ 有限；intervene `timing≠pre_step` | $H$ 对应自然步；$R_{\mathrm{behavior}}$ |
| `test_plus_locks_symbolic_family_to_test` | 同进程先 load Plus | CLI 新进程 / 只 prepare Symbolic |
| `test_c7_m01_mapped_noise_premise_is_deducted` | 手喂 `noise_set=["p3"]` | `build_labels` 把 sham 盖到 `p1`/`p2` |
| `test_analyze_refuses_fake_p1_from_labels` | 无 `p1_table` → `p1 is None` | （此项论文语义已锁） |
| `test_source_value_pair_rewrites_graph_ids` | rename 改表达式 | （此项已关，不重开） |
| `test_verbalizer_uses_extracted_answer_not_substring` | `17`/`70`/`boxed` | 同划分四档模型自述 |

---

## 8. 本审查复跑的命令（均可再跑）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → **61** / `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `python -m pytest -q --tb=line` → **153 passed**（19.91s）。
4. `generate_task_trace` + `prepare --eval-mode scientific --sham-opportunities 1` → 7 条 tiny 轨迹，全部 `constrained_target`，各 1 个 `q` 事件；SVP 图为 `p2_src` / `p1 * p2_src`；观测含 `sham:q`。
5. `collect --backend tiny --eval-mode scientific` → $H=(7,32)$ 全有限，`tasks.jsonl` 被复制，`event_rows` 7 行皆 `q`。
6. `label` / `fit`：task 头有限 $U$；行为头无已知标签；verbalizer 回显抽出 `82`。有任务 `_e_premise_ids=[p1,p2]`；无任务 `[p2,p1]`。
7. 密度：labels `noise_ref=1.0` 在 `p1`/`p2`/`sham:q`；`rho_M_noise=0.0`，`null_reason=None`。
8. analyze（仅 labels）→ `p1=None`，Gate `unregistered`。
9. Plus/Symbolic：`gsm8k-1` 无锁 → `probe_train`；同进程先 Plus → `test`。
10. 夹具标 official → 拒绝。PCA `(2,5)` vs `(2,3)` → `truncated=True`。

---

## 9. 结论

**冻结 hash：HASH_MATCH** `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`（61 文件）。

**原文一致性：不通过（FAIL）。**

作者 r10 关闭表中，下列在本冻结树上**接口已接通**，不得原样重开：collect 复制任务文件；有任务时 $E$ 列序；改名改图；拒假 P1；Gate 未注册；夹具≠官方；T3 不走 SVP；PCA truncated；生成区事件与有限 $H$。

科学入口仍在三处断开：

1. **概念偷换：** `constrained_target` 的 `\nq = 82` 被当成 §4.1 成功 $T$（A10-01/02）。
2. **噪声协议：** 无编辑 sham 被盖到真实前提，密度记已评估 $\rho_M^{\mathrm{noise}}=0$（A10-03）。协议 L29 被违反；作者“`sham:` 保持 missing”在 CLI 路径为假。
3. **划分泄漏：** Plus 家族锁是进程内 `set`。CLI 单独 prepare Symbolic 时，`gsm8k-1` 一类家族可进 `probe_train`（A10-04）。夹具 `gsm8k-12` 哈希碰巧是 test，不能当锁的证据。

另有 verbalizer 回显、账本过称、Fig.6 分类器缺失、无侧车 Symbolic prepare 崩溃。Gate 未注册、tiny 不是 MODEL-01、假说不要求正结果——这三条被遵守。作者关闭与 153 绿测不能关闭本通道。真实权重/官方全量是 `pending_server`，不能解释本机把约束赋值写成 $T$，也不能解释把 sham 写成真实 $N$。

独立复审关闭条件（本通道）：A10-01/02 必须在**同一冻结 hash** 上对照原文关闭（自然步骤事件，或对 `constrained_target` 诚实拒绝并降级账本）；A10-03 须让 `sham:` 保持 unmapped/missing；A10-04 须在 CLI/跨进程共组 Plus 家族。其余 medium 项至少改为诚实状态。

**不把 Goal 标为完成。**
