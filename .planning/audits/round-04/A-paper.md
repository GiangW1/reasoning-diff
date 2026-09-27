# 审查报告 A：原文一致性（paper consistency）— round-04

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-04 |
| **审查时间** | 2026-09-21 01:15–02:40（UTC+8） |
| **声明冻结 hash** | `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`（56 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **HASH_MATCH。** 按 `VERSION.md` 原文 Python 逐字复算：文件数 **56**，摘要 `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`。审查对象即该冻结工作树。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `E481EB84664E1F71EE5551FB3451F764B8FB7D21691B89E5DFFC67773B3090C4`（与账本 **§0** 一致；与 TR-0322 段行内 hash `B0228A57…` **不一致**，见 A4-12） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-04/{B,C,D,E,F}-*.md`。**未把** `ISSUES.md` 作者关闭当作关闭。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |

**总判：不通过。** 冻结 hash 可核验。相对 r03，若干**库函数**更接近原文（逐步 ρ、IRLS logistic、cone 拟合、`--eval-mode scientific` 卫兵、placeholder 前提、分头 `y`）。这些修补没有把 §4.1 / §8.2 科学入口接到自然轨迹、论文 $h_i/e_j$、前瞻生成干预或无门控嫁接。`--eval-mode scientific` 仍用节点真值拼轨迹；默认 smoke 仍把 prefix token id 当 $H$；tiny 路径把两 seed 末层均值复制成每个 $e_j$；`intervene` 在隐向量上做几何并写 `timing=pre_step`；`repair` 不 Prefill/decode。账本仍用 `implemented_local` + “pytest 65 passed” 关闭可执行行。假说不要求正结果——本通道不因 P1–P3 无正数判缺陷。Gate 0–2 保持 `unregistered`，**不是缺陷**。

---

## 0. 相对上一轮树的诚实变化（避免把已修项当新缺陷）

独立重读当前字节后，下列 **不再** 作为本轮 confirmed defect 原样重开（不等于科学入口已接通）：

| 先前问题 | 当前树（本轮复跑） |
|---|---|
| 无 `--eval-mode scientific` | 开关存在。scientific prepare 无 `--split-fractions` 会拒；scientific collect 拒 `offline_prefix_ids`；scientific calibrate 拒 loss/字面分数。 |
| CLI 密度 = 目标祖先 ∪ 曾变化前提 | `event_density_sets` → `mean_over_events`。本机 `prepare` 产物 `aggregation=mean_over_events`。 |
| P1 默认 `length+0.01*op`；无留出当 logistic | 无 `held_out` 且非 `precomputed` → `requires_held_out`。有留出时 IRLS logistic + 偏相关。 |
| `BilinearProbe` 无 `fit` | 加权 BCE 梯度步存在；CLI 分 `task`/`behavior` 两头。 |
| `collect_tiny` 不读 hidden | 现读 `hidden_states[-1]`。层仍是末层，不是 60–75%。 |
| `cone_fit` 空壳 | 现网格拟合 $\lambda,\gamma$；措辞 `descriptive_only`。 |
| T2/T3/T4 用题目前 N 字冒充 fact | Symbolic/Plus/T4 现为 `kind=placeholder`（整题）。不再把前 N 字标成事实前提。 |
| 校准入口用 probe loss 当 $a(X)$ | 有权重时走 `predict_matrix` + `one_minus_p`。分数支持集仍不是 $j\in R(s_i)$。 |
| `ie_z` 缺失 | 库函数 `mean(g')-mean(g)` 存在；CLI 不调用。 |
| `BoundaryMLP` 无训练 | 现有 `fit`；CLI 从不调用。 |

**未关闭：** 论文可执行条款（自然 `generate`、span 池化 $e_j$、分头真实标签矩阵、前瞻自回归、嫁接 Prefill、域编辑+新真值、P1 bootstrap、附录流水线）仍缺或被替身。账本未降级。

---

## 1. 逐文件覆盖

每行：路径（磁盘 `splitlines()` 行数）— 对照条款 — 结论。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 1–517 | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 1–86 | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。Gate 默认 null 与代码一致。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 1–166；§5 = 73–91 | GOAL §5.1–5.15 | 第 2、7、8、10–13、15 条在科学入口被降级或替身。 |
| `.planning/REQUIREMENTS.md` | 1–76 | DATA/MEAS/MODEL/PROBE/… 与 atomics | 复选框全空；状态表写 `implemented_local`。§0 hash 已更新；TR 行未跟。 |
| `.planning/PAPER_TRACEABILITY.md` | 1–26 约定；75–113、190–249、370–420、430–480 抽样 | 账本不得当实现证据 | ≥100 处 `implemented_local` + “pytest 65”。可执行行常指到无关符号。 |
| `pyproject.toml` | 1–27 | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 现有 `torch`/`transformers`。无强制 scientific 栈。 |
| `src/reasoning_diff/__init__.py` | 1–5 | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 1–4 | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 1–384 | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 1–46 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先与相交掩码正确。默认 cone 走任务祖先，不是行为头 $\hat R^{\mathrm{val}}$。 |
| `src/reasoning_diff/events.py` | 1–154 | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 对齐 | 身份对齐正确。`surface_mentions` 现含 aliases。策略分岔仍只读 `status=="strategy_change"`，并自标 `scanned=False`。仅夹具正则。 |
| `src/reasoning_diff/edits.py` | 1–258 | §7 T1 重算；GOAL §5.2 | 值编辑+表达式重算正确。有改名与 `operator_reverse`。`apply_source_value_edit` 只改值并打旗，不能构造同值异源对。 |
| `src/reasoning_diff/measure.py` | 1–320 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集、空分母、缺/空 sham→null、signed excess、逐步平均正确。TO 有对错 facet。无噪声配对轨迹。 |
| `src/reasoning_diff/analysis.py` | 1–253 | §2.6 P1–P3；§7 分流；附录 S2–S4 | P1 留出路径是 logistic。无 bootstrap 键。`cone_fit`/`retrieval_scatter` 库层可用。Week-8 不因 excess=0 转负结果。 |
| `src/reasoning_diff/interventions.py` | 1–115 | §2.4 交换/对照/INLP/救援/$\mathrm{IE}_Z$ | 交换式、范数匹配、`ie_z`、`select_weak_layer` 库层正确。未接到生成。 |
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、`fit` 形式正确。CLI tiny 维 32 故 `rank=32`。无 $e_j$ 池化。 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | §4.2 Hidden=256 ReLU | 架构+`fit` 符合。CLI 不训练、无句法监督接入。 |
| `src/reasoning_diff/probes/calibrate.py` | 1–42 | §2.5 命题 2 | $\lceil(N+1)(1-\alpha)\rceil$ 与 $+\infty$ 正确。调用方传入的不是 $j\in R(s_i)$ 的 $1-\hat p$。 |
| `src/reasoning_diff/probes/__init__.py` | 1–3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 1–80 | §8 文本/注意力/四档自述；GOAL §5.7 | 监督文本现为 BOW+logistic。零样本/5-shot/反思仍是 `gold[:4] in prefix`。注意力无标签阈值。CLI 不调用。 |
| `src/reasoning_diff/transfer.py` | 1–52 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。线性映射与双输入 `apply_bilinear_inputs` 存在。无“先共同维再 Procrustes”流水线。CLI 只报 N/A。 |
| `src/reasoning_diff/repair.py` | 1–73 | §3 Repairability/RR；§9 嫁接；GOAL §5.13 | 掩码名枚举在。`run_repair` 不生成、不 Prefill 模型。`extra_prefill_tokens=len(new_prefix.split())`。掩码名不改变执行。 |
| `src/reasoning_diff/cli.py` | 1–658 | §4 流水线；§8.2 scientific | 八阶段仍是夹具/几何冒烟。scientific 只加少量拒门。 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | §8.1 模型卡/revision | 两张冻结卡 + `load_frozen(..., local_files_only=True)`。CLI 不加载。无权重时属 pending_server。 |
| `src/reasoning_diff/models/collect.py` | 1–60 | §4.2 $h_i/e_j$；GOAL §5.6/5.10 | tiny 采集末层 prompt hidden。`intervene_tiny` 仍是 `+0.01`，不是 $\Pi_Z$。 |
| `src/reasoning_diff/models/features.py` | 1–39 | §2.4 三时机；GOAL §5.6 | 跨界 token 排除正确。库函数可用。 |
| `src/reasoning_diff/models/generate.py` | 1–57 | §8.2 自然轨迹 | 显式 decode 循环存在。CLI prepare/collect 不用它生成论文轨迹。 |
| `src/reasoning_diff/models/tiny.py` | 1–120 | 本机 hook 边界 | 随机 Qwen2/3 + 末 token resid_post。不是论文模型路径。 |
| `src/reasoning_diff/models/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/tasks/catalog.py` | 1–39 | §7 适配入口 | 快照分发。CLI 默认 `t1_fixture`。不生成 500 题。 |
| `src/reasoning_diff/tasks/t1_official.py` | 1–92 | §7 T1；template≠G | 快照加载拒绝裸 `G`、排除共享 RNG、默认 mod 23。`load_igsm_directory` 存在。CLI 默认不走。 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | 官方/夹具分离 | 拒绝非 `fixture`。成立。 |
| `src/reasoning_diff/tasks/t1_config.py` | 1–21 | op∈{5,10,15,21}，n=500 | 配置校验。无数据生成。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–84 | §7 T2；GOAL §5.2 | 无侧车：placeholder + `graph_status=unknown`，拒编辑。有侧车：值编辑+算子逆转。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–52 | §7 T2；评测专用 | test-only 锁正确。前提=`placeholder`。`apply*` 符号为零。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 1–93 | §7 T2-noop | 可造配对与分层元数据。无注入句值扰动扫描。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 1–104 | §7 T3；supporting_facts≠DAG | 标记正确。`document_edit` 回 Task；无独立新答案则 `needs_truth`。CLI 不走。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 1–103 | §7 T3 组成引用 | 保留 answerable/unanswerable。`expression="composition_reference"` 不可重算。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–62 | §7 HumanEval-Perturb；GOAL §5.15 | 前提=整段 spec。`apply_spec_edit` 无区分输入/不变行为包。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 1–33 | §7 T4；Fig.6 | 四类状态强制区分。前提=placeholder。无相图。 |
| `src/reasoning_diff/tasks/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/executor.py` | 1–99 | GOAL §5.15 | 禁止宿主 exec。默认 `UnavailableExecutor`。`SubprocessExecutor` 是普通子进程，GOAL 禁止冒称隔离沙箱。 |
| `src/reasoning_diff/scoring.py` | 1–30 | §3 域内评分 | 数值/QA 精确匹配。代码经执行器接口。 |
| `src/reasoning_diff/splits.py` | 1–97 | §4.1 共组；GSM-Plus test-only | 六角色 + 家族共组。默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 1–53 | GOAL §5.4 | sample/direction/perturb/bootstrap/split 分离。CLI 基本不用。 |
| `src/reasoning_diff/io.py` | 1–133 | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 1–11 | — | 夹具路径。 |
| `tests/test_cli_pipeline.py` | 1–29 | §4 流水线 | 八阶段 exit 0；**强制** `--backend offline`。 |
| `tests/test_science.py` | 1–97 | 校准/迁移/交换/Week-8 | 测库函数微例。`test_repair_reprefills_*` 只断言布尔字段。 |
| `tests/test_measure.py` | 1–40 | $S/M$、联合编辑反例 | 与公式一致。 |
| `tests/test_review_regressions.py` | 1–394 | 上轮回归 | 锁住若干库修补；仍锁 `precomputed` 启发式。 |
| `tests/test_round03_regressions.py` | 1–288 | r03 回归 | 锁住逐步密度、placeholder、logistic 留出路径；**同时**锁 `precomputed_scores`。 |
| `tests/test_tracer_t1_prepare.py` | 1–100 | T1 夹具准备 | 身份/重算/空分母。 |
| `tests/test_t1_official.py` | 1–31 | template≠G | 快照形状。 |
| `tests/test_t2_gsm.py` | 1–33 | T2 | 侧车数值编辑。 |
| `tests/test_t3_t4.py` | 1–44 | T3/T4 | supporting_facts ≠ DAG。 |
| `tests/test_artifacts.py` | 1–73 | I/O | 工程。 |
| `tests/test_generate_loop.py` | 1–17 | 可重放采样 | tiny decode。 |
| `tests/test_tiny_hooks.py` | 1–27 | hook 清理 | 本机接口。 |
| `tests/test_tiny_cache.py` | 1–26 | 缓存隔离 | `intervene_tiny` 是平移，不是交换。 |

第三方库：审查了本项目对 `numpy` / 可选 `torch`+`transformers` 的使用假设，未审查依赖源码。

夹具抽读：`tests/fixtures/t1_tiny.json`（全文）、`t2_gsmplus_one.json`、`t2_symbolic_one.json`、`t4_boundary.json`。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献清单 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。Gate 保持 null（非缺陷）。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 2、7、8、10–13、15 条在科学入口被降级或替身。 |
| C4 | 阅读 `PAPER_TRACEABILITY.md` 约定，抽样 TR-0001–0043、TR-0125–0139、TR-0158–0174、TR-0294–0347、TR-0378–0404 | 账本把可执行缺口标成 `implemented_local`，验证列写 pytest 65。**不能**作为覆盖证据。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。 |
| C6 | 对照公式手核 + 复跑：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1、cone | $R_{\mathrm{task}}$/差集/交换/分位数/拒维度：**库函数层符合**。P1 留出路径：**符合 logistic**。$a(X)$ 入口：全列 max，**不符合**。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | 无多 seed `generate`、无 `allowed_edits` 全扫描。`prepare --eval-mode scientific` 仍拼 `"p1 = 4 \| p2 = 0 \| q = 0"`。 |
| C8 | 对照 §4.2 / §8 探针与基线 | 双线性可拟合。tiny $E$ 各行相同。边界 MLP 未接入 CLI。三档 verbalizer 仍是子串。 |
| C9 | 对照 §2.4 / §6 干预 | 无来源—数值解耦资产。CLI `geometry_on_hidden` + `timing=pre_step`。tiny hook 是 `+0.01`。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 | T1 值编辑成立。T2 仅侧车。GSM-Plus 无 `apply*`。T3 真值常 `needs_truth`。T4 placeholder。 |
| C11 | 对照附录 S1–S4、C4 掩码、$k\in\{1..5\}$、失效相图 | S2 拟合库存在。S3 未串联。S4 不从文本算嵌入。连续编辑/相图无。掩码名不改执行。 |
| C12 | 抽读测试是否固化替身 | 是：`test_full_cli_smoke` 强制 offline $H$；`test_repair_reprefills_*` 只看布尔；`test_verbalizer_*` 不测微调；`test_p1_precomputed_*` 锁启发式。 |
| C13 | 独立重算论文/协议/GOAL/REQUIREMENTS SHA-256 | 前三份与账本 §0 一致。REQUIREMENTS 文件=§0；TR-0322 段钉旧 hash。 |
| C14 | 独立重算声明代码冻结 hash | **HASH_MATCH** `fb1e3dfa…`，56 文件。 |
| C15 | 复跑 CLI prepare/collect/fit/calibrate/intervene/repair/analyze 与库函数微例 | 见各 finding 的 Repro。命令已在本审查重跑，不是转述。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 全量 `pytest -q` 作为本通道验收 | 原文符合性不由绿测关闭。作者声称 97 passed；本报告不声称测试通过。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量 500 题 | 协议 §7：科学结论 `pending_server`。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | 科学入口无论文定义的 $H/E$ 与分头标签矩阵。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读 round-04 B–F。 |
| N6 | `PAPER_TRACEABILITY.md` 全部 528 行逐字复读 | 已读约定与高风险可执行/GOAL/REQUIREMENTS 行。剩余多为同一模板重复。 |
| N7 | 真实隔离沙箱跑 HumanEval | 无合格隔离后端；`SubprocessExecutor` 不能冒称沙箱。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | 探针/干预/分析/修复均冒烟 | subst |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 1 | 34–35 | 检索余弦 vs 答案变 | exec | `retrieval_scatter` 可吃预计算嵌入；CLI 不产 Fig.S4 | ok-lib |
| 论文 1 | 38 | 修复解码/Prefill/耗时 | exec | `Cost` 字段有；repair 填 `split()` 词数 | subst |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema + 夹具解析 | ok-lib |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | `build_labels` 字段正确；CLI 单编辑合成轨迹 | subst |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | id + aliases 词边界 | ok-lib |
| 论文 2.3 | 88 | 消失/合并/策略分岔 | proto | `removed` 有；策略 `status_field_only`/`scanned=False` | stub |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap`；手核 `[1,0]+Π([0,1]-[1,0])=[1,1]` | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ | math | `ie_z` 库函数；CLI 不调用 | ok-lib |
| 论文 2.4 | 106–108 | 前瞻 hook/KV/前缀 | exec | tiny `+0.01`；CLI 几何行向量写 `pre_step` | subst |
| 论文 2.4 | 110 | 步前/数值前/步尾 | exec | 库函数区分；collect 用 prompt 末 token | stub |
| 论文 2.4 | 114–117 | C-rand / C-layer 同幅度四项 | exec | 范数匹配在；C-layer 用硬编码 `{0:0.2,1:0.1,2:0.4}`；四项结局 `None` | subst |
| 论文 2.5 | 121–125 | cone / Oracle / 行为掩码 | math | `dirty_cone`/`oracle_mask`/`behavior_mask` | ok-lib |
| 论文 2.5 | 127–130 | 命题 1 + REST-03 | math | $xy$ 反例夹具 | ok-lib |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | 分位数 ok；CLI 对**全部**列取 max$(1-p)$ | subst |
| 论文 2.5 | 141–142 | 原轨迹槽位、禁重拓扑 | exec | 无嫁接执行 | missing |
| 论文 2.6 | 148–156 | $S,M,\rho$，空分母 N/A | math | `dependency_densities` + event mean | ok-lib |
| 论文 2.6 | 158 | 噪声先扣除 | proto | 库函数缺/空 sham→null；CLI sham 是同一段合成文本 | subst |
| 论文 2.6 | 164 | P1 logistic + 偏相关 + bootstrap | math | 留出 IRLS + 偏相关；无 bootstrap；`precomputed` 仍是原分数 | ok-lib / subst |
| 论文 2.6 | 165 | P2 配对 + 污染位置 | exec | 标量减法 + 分母字段；无位置 | stub |
| 论文 2.6 | 166 | P3 Δacc + 对照 + 非目标 | exec | 库函数收 nontarget；CLI 无表则 `None` | ok-lib |
| 论文 2.6 | 168 | REST-02 | proto | `causal_reverse_claim=False` | ok |
| 论文 3 | 176–186 | TO_all/clean、CSP、覆盖、脏变、P/R/F1 | math | TO/CSP/覆盖/脏变/对错 facet 有；无探针 P/R/F1 | stub / ok-lib |
| 论文 3 | 188 | TO/CSP 噪声参照与比值 | proto | 无配对噪声轨迹 | missing |
| 论文 3 | 190 | 干预三项并列、前瞻/回溯分列 | proto | `intervention_report` 接受三 dict；CLI 硬编码 None + geometry | stub |
| 论文 3 | 194–200 | Repairability、RR、成本分列 | math | 两公式有；成本未测 | stub |
| 论文 4.1 | 232–253 | 双标签流水线；NL 单调对齐；共组 | exec | 无 generate 循环；无 NL 对齐 | missing |
| 论文 4.2 | 257–267 | MLP 训练、双头、池化 $e_j$、60–75% 层 | exec | 架构/`fit` 在；池化/层选无或假 | subst |
| 论文 5 Fig.1–2 | 291–299 | 热力图、三时机比较、跨模型迁移入口 | exec | 无导出；analyze 只报 4096/3584 N/A | missing |
| 论文 6 | 301–313 | 解耦资产、前瞻交换、INLP、救援 | exec | 向量几何 + 记录字段 | stub |
| 论文 7 | 315–329 | P1–P3 测量入口（不要求正结果） | exec | 有表才算；默认 `p1=p2=p3=None` | stub |
| 论文 8 | 331–341 | 注意力/四档 verbalizer/监督文本 | exec | 监督 BOW；其余子串 | subst |
| 论文 9 / Table 1 | 343–355 | 五条主对照 + 三条附录掩码实跑 | exec | 枚举名；执行相同 | stub |
| 论文 Fig.6 | 353 | 失效相图五类 | exec | T4 状态枚举 ≠ 相图 | missing |
| 附录 S1 | 357–359 | $k\in\{1..5\}$ 连续编辑 | exec | 无 | missing |
| 附录 S2 | 361–367 | 两参数锥拟合 | math | `cone_fit` 现拟合；CLI 不调用 | ok-lib |
| 附录 S3 | 371–373 | 共同维 + Procrustes | exec | 两函数分立 | stub |
| 附录 S4 | 375–377 | 嵌入余弦散点 | exec | 不计算文本嵌入 | stub |
| 论文 7 数据 | 399–409 | T1–T4 假设专用资产 | exec | 读取器+placeholder；T1 无生成器 | stub |
| 论文 8.2 | 419–431 | `--eval-mode scientific` | exec | 开关在；流程仍是夹具 | subst |
| 论文 9 | 435–445 | 第一周三轨迹/50 干预冒烟 | exec | 夹具单编辑 | stub |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |

---

## 5. Findings

### A4-01 — `--eval-mode scientific` 仍把节点真值轨迹称作科学流水线

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` `_trace_text` 88–91；`_synthetic_trace` 94–115；`cmd_prepare` 181–190；`cmd_collect` 298 |
| **Trigger** | 对照论文 §4.1 伪代码（232–248）与 §8.2 scientific 流程（422–429） |
| **Paper requirement** | 自然轨迹 `T0 = generate(P, seed)`；对每个前提的 `allowed_edits` 再 `generate`；采集隐状态。夹具不得写成 scientific 已测（账本自己也写了这句）。 |
| **Repro / evidence** | 复跑：`prepare --eval-mode scientific` 无 `--split-fractions` → `ValueError: scientific mode requires explicit --split-fractions`。加上六比例后 **exit 0**。`traces.jsonl`：`model=fixture`，`seed=0`，文本 `p1 = 4 \| p2 = 0 \| q = 0`（节点真值拼接，不是模型 CoT），`token_ids=[1,2,3,…]`（字符下标，不是 tokenizer）。单编辑、单 seed。`collect` 对同一合成轨迹再走一遍。 |
| **Impact** | 科学开关只增加划分拒门，不实现 §8.2 树。C1–C4 入口仍是夹具冒烟。 |
| **Suggested fix** | scientific 必须调用模型 `generate` 与真实 $H/E$；否则拒绝并保持 `unimplemented`。夹具路径不得接受 `eval_mode=scientific`。 |
| **Status** | **confirmed defect** |

### A4-02 — 采集把 prefix-id / 末层均值复制当成 $h_i$ 与 $e_j$

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` 309–330；`models/collect.py` 26–37 |
| **Trigger** | 论文 4.2 L261–263：$h_i$ 为 60–75% 层步边界；$e_j$ 为同层前提 span 均值池化。GOAL §5.6–5.7。 |
| **Paper requirement** | 冻结模型自然轨迹上的边界隐状态与前提池化；两头分训。 |
| **Repro / evidence** | 默认/测试路径 `--backend offline`：`H.shape=(1,8)=[1..8]`（prefix token id），`E` 全零，`weight_source=offline_prefix_ids`。`scientific --backend offline` 复跑拒绝（卫兵成立）。`scientific --backend tiny`：`H=(2,32)` 为两 seed 的 **prompt 末 token、末层**；`E=(2,32)` 且 `E_ROWS_IDENTICAL=True`（同一 `hidden_all.mean` 复制到每个前提）。`hidden_layer=-1`，不是 60–75%。`run_spec.source_kinds={'cli':'fixture'}`。CLI 无 `BoundaryMLP`。`cmd_fit` 两头 loss 同为 `3.17e-5`（同一 tiny 矩阵）。 |
| **Impact** | C1“从隐状态读出 Read-Set”在可执行路径上仍是替身。账本 TR-0134/0135 指向 `bilinear.py` 是张冠李戴。 |
| **Suggested fix** | collect 写出层切片与 span 池化 $E$；禁止把 token id 或复制均值叫 $H/E$。未采集时拒绝 `implemented_local`。 |
| **Status** | **confirmed defect**；真实权重 **pending_server** |

### A4-03 — 干预是隐向量几何，却写入 `timing=pre_step` 与 `dev_weak_layer`

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` 458–503；`models/collect.py` `intervene_tiny` 49–50 |
| **Trigger** | 论文 2.4 L106–117；§6 L305–313；GOAL §5.10–5.11 |
| **Paper requirement** | 目标步首 token 前交换 residual；恢复自回归；评价新生成 $s_k$ 是否跟随 donor。C-layer 由开发集弱层确定。报告四项结局相对对照的差值。 |
| **Repro / evidence** | `apply_swap` 手核通过（ok-lib）。offline collect 后 `intervene`：`status=donor_missing`，四项 `None`（$H$ 只有 1 行）。tiny collect 后：`status=geometry_on_hidden`，`timing=pre_step`，`clayer_status=dev_weak_layer`，`target/nontarget/task_correct/invalid=None`。源码 `layer_scores = {0: 0.2, 1: 0.1, 2: 0.4}`（465–466），不是 dev 曲线。`intervene_tiny`：`patched[:, -1:] = t + 0.01`。`apply_source_value_edit` 复跑：`same_value_diff_source=False`，只是改值打旗。 |
| **Impact** | C2 主张入口不存在。把几何冒烟标成前瞻干预是概念替换。 |
| **Suggested fix** | 解耦资产；步前 hook 施加 $\Pi_Z$；继续解码；按预注册矩阵评分。几何行不得写 `pre_step` 成功。 |
| **Status** | **confirmed defect** |

### A4-04 — 局部修复是记录对象，掩码名不改变执行

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `repair.py` `run_repair` 41–61；`cli.py` 507–521 |
| **Trigger** | 论文 §3 L194–200、§9 L347–355、附录 S1；GOAL §5.13 |
| **Paper requirement** | 干净文本在当前前缀重新 Prefill，受损槽位自回归重算。主文 5 条 + 附录 3 条实跑。同原始 token 预算。连续 $k\in\{1..5\}$。 |
| **Repro / evidence** | CLI repair 产物：`generated_tokens=0`，`extra_prefill_tokens=9`（`p1 = 4 / p2 = 0 / q = 0` 的 `split()` 词数），`refilled_prefix=True`，`failures=[]`，`status=ok`。库函数对 `retrieval_of_thought` 同样：`generated_tokens=0`，`extra_prefill_tokens=3`（`"hello world tokens".split()`）。掩码只写入名字。`test_repair_reprefills_and_refuses_gate` 只断言布尔字段。全仓库无 $k\in\{1..5\}$ 循环。 |
| **Impact** | Repairability/RR/成本曲线无法按论文测量。C4 附录未落地。 |
| **Suggested fix** | 同一执行器按掩码真跑 Prefill/decode；无 tokenizer 则成本为 null，且不得标 `refilled_prefix=True`。 |
| **Status** | **confirmed defect** |

### A4-05 — 账本把未实现条款标成 `implemented_local`，并用过期 pytest 65 关闭

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` 例如 TR-0125、TR-0134–0137、TR-0158–0159、TR-0166、TR-0308、TR-0316、TR-0319、TR-0327–0334、TR-0346、TR-0400；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：账本必须能反向核验。账本自己写：“`pytest -q` 不得单独关闭可执行行”“fixture CLI 不得写成 scientific 已测”。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。未实现不得标已实现。 |
| **Repro / evidence** | 抽样：TR-0125 要求多 seed `generate` + `allowed_edits` 全扫描，实现列是 `measure.dependency_densities`。TR-0135（$e_j$ 池化）指向 `bilinear.py`。TR-0158 / TR-0400（解耦任务构造）指向 `intervention_report`。TR-0346（连续编辑 $k\in\{1..5\}$）指向 `run_repair`。几乎所有可执行行 `verification_method=python -m pytest -q` / `local pytest 65 passed`。VERSION 作者声称 97 passed。REQUIREMENTS 复选框全空，状态表写 `implemented_local`。 |
| **Impact** | 覆盖率被制成 16/16。独立审查若信账本会漏检 A4-01–A4-04。 |
| **Suggested fix** | 未接到科学入口的条款改回 `unimplemented` / `ok-lib_unwired`。禁止用 pytest 计数关闭可执行行。 |
| **Status** | **confirmed defect** |

### A4-06 — 零样本 / 5-shot / 反思 verbalizer 仍是子串打分

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `baselines.py` `verbalizer` 69–80 |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7；VERB-01 / BASE-01 |
| **Paper requirement** | 四档自述；监督档与探针同样本/划分/可见前缀。不能只用简陋替身。 |
| **Repro / evidence** | 复跑：`verbalizer("zeroshot", "goldxxxx prefix", "gold", False)` → `score=0.4`（`gold[:4] in prefix`）。`fiveshot` 对 `"xxxx"` → `0.0`。无 ICL 例子、无反思生成。监督档可走 BOW `fit_text_predictor`（库层最小实现）。CLI `fit` 不调用 baselines。`test_verbalizer_supervision_contract` 只查未训练报错与 visibility 字符串。 |
| **Impact** | 第 8 节“说不出来”的对照不存在。R4 分流无法计算。 |
| **Suggested fix** | 实现四档真实生成/训练；子串函数不得叫 verbalizer 实现。 |
| **Status** | **confirmed defect** |

### A4-07 — 校准入口把整行 $\hat p_{\cdot j}$ 当作 $a(X)=\max_{j\in R(s_i)}(1-\hat p_{ij})$，并用同题两 seed 当 $N$

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_calibrate` 426–441；`calibrate.py` `sequence_score` 21–22 |
| **Trigger** | 论文 2.5 L132–139；GOAL §5.8：不得把同题重复当独立样本扩大 $N$。 |
| **Paper requirement** | $a(X)=\max_{i,j\in R(s_i)}(1-\hat p_{ij})$；空真集取 0；交换单位是轨迹/序列。 |
| **Repro / evidence** | 分位数公式本身正确（`[0.1,0.2,0.3,0.4], α=0.4` → $q=0.3$；$\alpha=0.1$ → $+\infty$）。CLI：`sequence_score(pred[i].tolist(), True, False, …)` —— `labels_known=True` 恒成立，对**全部**前提列取 max$(1-p)$。手核：`[0.9,0.1,0.2]` → `0.9`，若真依赖只有第一列应为 `0.1`。tiny 校准产物：`scores=[3.17e-6, 0.996]`，$N=2$（两 seed 同一 prompt），`unit=full_trace`，`q=0.996`。 |
| **Impact** | 保形集合与漏检保证在入口上无定义。 |
| **Suggested fix** | 只对已知 $R(s_i)$ 聚合；一题多 seed 不得扩大 $N$。 |
| **Status** | **confirmed defect** |

### A4-08 — GSM-Plus / 无侧车 T2 / T4 没有“合法编辑 + 更新真值”

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t2_gsm_plus.py` 1–52（`apply*` 为空）；`t2_gsm_symbolic.py` 43–44, 68–70；`t4_boundary.py` 26；`t3_humaneval.py` 34–57 |
| **Trigger** | 论文 §7 L403–407；GOAL §5.2；DATA-02 |
| **Paper requirement** | 各域：读取、合法编辑、更新后真值、事件/独立标注、域内评分。 |
| **Repro / evidence** | 复跑：GSM-Plus `premises[0].kind=placeholder`，模块 `PLUS_APPLY_FNS=[]`。Symbolic 无侧车：`graph_status=unknown`，`kind=placeholder`。T4：`kind=placeholder`。HumanEval `apply_spec_edit` 无区分输入列表（`invariant_behavior_unspecified`）。Hotpot/MuSiQue 无新答案 → `needs_truth`（此项诚实）。前 N 字冒充 fact **本轮不再成立**。 |
| **Impact** | 除 T1 值编辑与 T2 侧车外，行为扫描没有合法 $P'$ 与更新 $v$。 |
| **Suggested fix** | 每域提供编辑+新 oracle；缺失标注保持 `unknown`，不要把读取器标成域适配完成。 |
| **Status** | **confirmed defect** |

### A4-09 — 附录 S1–S4 与 Table 1 没有测量入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `cone_fit` 191–211、`procrustes` 214–219、`retrieval_scatter` 222–239；`repair.py` 9–11；CLI 无调用 |
| **Trigger** | 论文附录 S1–S4；S4“不得因精简而删除”。FIT-01 / GEOM-01 / RETR-01 / CONT-01 / TABLE1-01 |
| **Paper requirement** | $k\in\{1..5\}$；两参数锥拟合；先共同维再 Procrustes；$(P,P\oplus\Delta P)$ 文本嵌入余弦 vs 答案是否改变；八条掩码实跑。 |
| **Repro / evidence** | `cone_fit([0.2,0.5,0.8],[0.1,0.4,0.7])` 返回 `lambda/gamma/r2` 且 `wording=descriptive_only`（库层不再空壳）。`retrieval_scatter` 只对已给 embedding 做点积；不计算文本嵌入。`procrustes` 要求已同形；与 `fit_linear_map` 未串联。CLI `analyze` 不调用三者。无连续编辑。Table 1 掩码名见 A4-04。 |
| **Impact** | 附录主张没有从入口到图的路径。 |
| **Suggested fix** | CLI 导出 S2–S4；几何三档分列并报告配对 $n$。 |
| **Status** | **confirmed defect**（S2 库函数本身非缺陷） |

### A4-10 — P1 缺问题级 bootstrap；P2 无污染位置（不要求正结果）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `p1_incremental` 41–81；`p2_paired` 97–137；`cli.py` 541–564 |
| **Trigger** | 论文 2.6 表 P1–P2；协议 §5；GOAL §5.12 |
| **Paper requirement** | P1：留出 logistic AUC、偏相关、**bootstrap / 问题级区间**。P2：配对 $\Delta\rho_S/\Delta\mathrm{acc}$ **与污染步骤位置分布**。假说不要求正结果，但要有可调用测量。 |
| **Repro / evidence** | 留出路径 `estimator=held_out_logistic`，返回 `partial_corr_rho_y_given_len_op`。复跑 P1 keys **无** interval/bootstrap。`bootstrap_cluster` 存在但未接入。`precomputed=True` 仍是 `length` vs `rho` 原分数（测试锁住 `delta_auc==0`）。`p2_paired` 无位置字段。CLI 无 `p1_table.jsonl` 时 `p1=p2=p3=None`（本机复跑确认）。 |
| **Impact** | Week-8 不能表示“已按论文统计量检验（含负结果）”。 |
| **Suggested fix** | P1 接入问题级 bootstrap；P2 加位置直方图；无表保持 `not_evaluated`。删除或隔离 `precomputed` 启发式。 |
| **Status** | **confirmed defect** |

### A4-11 — Week-8 分流树未按 excess / 协议七条编码

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `week8_decision` 159–188；`cli.py` 565–580 |
| **Trigger** | 论文 §7 L319、L329；协议 §5 |
| **Paper requirement** | 扣除后 $\rho_S$ 不显著 → 负结果、不做 P2/P3；P1 不成立降附录；测量未可靠 →「测量待解决」。 |
| **Repro / evidence** | Gate 保持 `unregistered` **正确**。复跑 `week8_decision({"status":"not_evaluated","rho_S_excess":0.0})` → 仍 `status=not_evaluated`，`skip_p2_p3=True`，**不会**写成 `c3_negative_descriptive`。分支只读调用方预置的 `c3_negative`/`p1_failed` 旗。CLI 从不根据 dens 置旗。 |
| **Impact** | 协议决策规则无法从代码复现。不能用 Gate 持守抵消分流缺失。 |
| **Suggested fix** | 显式状态机：`measurement_unresolved` / `c3_negative_descriptive` / `not_evaluated` / `evaluated`。 |
| **Status** | **confirmed defect**（分流）；Gate 本身见 A4-24 |

### A4-12 — REQUIREMENTS 行内 source_hash 与文件 / 账本 §0 不一致

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `PAPER_TRACEABILITY.md` L20 vs L26 vs TR-0322 段（约 L398+） |
| **Trigger** | 账本 §0：“每行 `source_hash` 与上表一致”。 |
| **Paper requirement** | 追溯行必须钉住所读源文件字节。 |
| **Repro / evidence** | 本审查对 `.planning/REQUIREMENTS.md` 复算 `E481EB84…`，与 §0 一致。TR-0322 及后续 REQUIREMENTS 行仍写 `B0228A5785681FA11E1742EB1A7CD84822E6657D52C8CE6BF690E86A62283789`。 |
| **Impact** | 需求原子行钉在旧字节上。 |
| **Suggested fix** | 回写行内 hash，或回滚无证据的状态表改写。 |
| **Status** | **confirmed defect** |

### A4-13 — `SubprocessExecutor` 被放在 `IsolatedExecutor` 谱系里

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `executor.py` 27–29, 55–84, 87–92 |
| **Trigger** | 论文 §7 L406；GOAL §5.15：“普通 subprocess … 不能冒称隔离沙箱”。 |
| **Paper requirement** | 显式隔离执行器（超时、资源限制）；不回退宿主 exec。 |
| **Repro / evidence** | 默认 `get_executor()` → `UnavailableExecutor`（诚实）。`SubprocessExecutor.submit` 写临时文件后 `subprocess.run([sys.executable, path], timeout=…)`。禁止宿主 `exec` 是对的。把该后端标成 Isolated 违反 GOAL 原文。 |
| **Impact** | HumanEval 若走 `name="subprocess"` 会被账本 TR-0321/0391 写成已实现隔离。 |
| **Suggested fix** | 改名并文档化为 non-sandbox child process；隔离后端保持 unavailable / pending。 |
| **Status** | **confirmed defect**（命名/宣称）；真实沙箱 **pending_server** |

### A4-14 — TO/CSP 仍无噪声参照与探针 P/R/F1

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `measure.py` `preservation_to_csp` 215–262 |
| **Trigger** | 论文 §3 L176–188；Fig.1 |
| **Paper requirement** | $\mathrm{TO}_{\mathrm{all}}/\mathrm{TO}_{\mathrm{clean}}$；正确/错误分组；$\mathrm{CSP}_{\mathrm{noise}}/\mathrm{TO}_{\mathrm{noise}}$ 及比值；探针 P/R/F1。 |
| **Repro / evidence** | 现有 `to_correct`/`to_incorrect` facet（相对 r03 的进步）。函数不接收配对噪声轨迹，不输出探针 P/R/F1。CLI 只对夹具真值轨迹调用一次。 |
| **Impact** | Fig.1 不能按论文口径制作。 |
| **Suggested fix** | 增加噪声配对与探针 facet。 |
| **Status** | **confirmed defect** |

### A4-15 — 自然语言事件对齐与官方 CoT 解析缺失

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `events.py` `parse_fixture_events` 27–75；`align_events` 78–128 |
| **Trigger** | 论文 4.1 L250–252 |
| **Paper requirement** | 结构化：变量/表达式/版本/作用域。NL：抽实体后允许跳过与合并的单调序列对齐。 |
| **Repro / evidence** | 只有夹具 `alias = value` 正则。无 iGSM 官方 CoT 解析。occurrence 不等则全部 disappeared+merged，不做单调跳过。`structural.detector=occurrence_count`。 |
| **Impact** | T2/T3 行为标签没有事件层。 |
| **Suggested fix** | 分域解析器 + NL 单调对齐；未对齐进单独计数。 |
| **Status** | **confirmed defect** |

### A4-16 — T1 500 题 / 四档 op / 三轨迹配置没有 CLI 入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t1_config.py` 9–21；`cli.cmd_prepare` 默认单 fixture；`t1_official.load_igsm_directory` 89–92 未被默认 CLI 使用 |
| **Trigger** | 论文 §7 L403、§9 L437；WEEK1-01 |
| **Paper requirement** | iGSM `op∈{5,10,15,21}`、500 题；$T_0(seed=0)$、$T'_0(seed=1)$、$T_{\mathrm{pert}}(seed=0)$。 |
| **Repro / evidence** | 配置校验存在。本机 scientific prepare 仍一条夹具、一个 seed=0 合成轨迹。全量 500 属 pending_server；**任务单/三轨迹入口本身**是代码缺口。 |
| **Suggested fix** | 配置驱动的三轨迹任务单；CLI 消费快照目录。 |
| **Status** | **confirmed defect**（入口）；全量跑数 **pending_server** |

### A4-17 — 表面提及/策略分岔仍弱于论文 2.3

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `events.py` `surface_mentions` 13–24；`align_events` 119–126 |
| **Trigger** | 论文 2.3 L87–88；SURF-01 / STRUCT-01 |
| **Paper requirement** | $R^{\mathrm{surf}}$ 记录名称与符号引用。消失/合并/版本/策略分岔单独计数。 |
| **Repro / evidence** | 现匹配 `premise_id` 与 node aliases（相对只搜 id 的进步）。`t1_tiny` 步骤 `"q = 0"` 不含 `p1`/`p2`，故 surf 仍常为 `[]`。`strategy_changed` 仅 `status=="strategy_change"`；夹具解析只写 `ok`/`ambiguous`。元数据自标 `scanned=False`（诚实）。 |
| **Impact** | 文本保留/符号替换与策略分岔报告不可用。 |
| **Suggested fix** | 用渲染名/符号；策略检测或显式 `unknown`。 |
| **Status** | **confirmed defect** |

### A4-18 — 来源—数值解耦资产与 $\mathrm{IE}_Z$ 未进入执行

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `edits.py` `apply_source_value_edit` 204–216；`interventions.py` `ie_z` 88–89；CLI 不调用 |
| **Trigger** | 论文 2.4 L100–104；§6 L305；CAUSAL-02 / MEDIATION-01 |
| **Paper requirement** | 同值异源 / 同源异值任务对事先列出目标/非目标。$\mathrm{IE}_Z$ 对预指定 $g$ 可计算。 |
| **Repro / evidence** | 复跑 `apply_source_value_edit`：`same_source_diff_value=True`，`same_value_diff_source=False`。`ie_z([1,0],[0,0])=0.5`（公式对）。无 donor/base 构造器、无高层响应矩阵资产、CLI 不调 `ie_z`。 |
| **Impact** | 中介定义在执行路径上不可计算。 |
| **Suggested fix** | 成对资产 + 干预后对 $g$ 做配对期望。 |
| **Status** | **confirmed defect** |

### A4-19 — 默认划分比例未预注册

| 项 | 内容 |
|---|---|
| **Severity** | low |
| **File / symbol / line** | `splits.py` `DEFAULT_FRACTIONS = (0.40, 0.15, 0.10, 0.10, 0.10, 0.15)` L8 |
| **Trigger** | 协议 §3：“具体比例在生成实验数据前注册。” |
| **Paper requirement** | 六角色分离；比例预注册。 |
| **Repro / evidence** | scientific prepare **要求**传入六比例（卫兵），但接受任意和为 1 的数组，无 `protocol_ref`。默认 fixture prepare 仍用内置比例。 |
| **Impact** | 若用该默认切真实数据，即未注册划分。 |
| **Suggested fix** | 科学模式要求显式 protocol_ref，而不仅是六个数字。 |
| **Status** | **unconfirmed doubt** |

### A4-20 — CLI sham 用同一段合成文本冒充“同题不同随机流”

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` 214–234 |
| **Trigger** | 论文 2.6 L158；协议 §2 第 6 条 |
| **Paper requirement** | 噪声参照必须是同题不同随机流、匹配比较机会。 |
| **Repro / evidence** | `--sham-opportunities 1` 时 `sham_trace = _synthetic_trace(task, base_text, "trace-sham", 1)` —— **同一 `base_text`**。值不可能变。本机 dens：`rho_S_excess=None`（空 hits → 库层 null，未伪装成 0）。协议名叫 `no_edit_matched`。 |
| **Impact** | 噪声协议有名字、无测量。excess=null 是诚实的，但入口仍像“已跑 sham”。 |
| **Suggested fix** | 真不同 seed 生成，或缺协议不写 sham 名。 |
| **Status** | **confirmed defect** |

### A4-21 — 注意力基线没有 dev 阈值到标签的通路

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `baselines.py` 49–67 |
| **Trigger** | 论文 §8 L333；ATTN-01 |
| **Paper requirement** | 前提注意力均值、Rollout、开发集头聚合；阈值在验证集确定。 |
| **Repro / evidence** | `attention_mean`/`attention_rollout`/`select_attention_heads` 存在。无“对依赖标签选阈值”的函数。CLI 不调用。 |
| **Impact** | Fig.5 注意力列无法制作。 |
| **Suggested fix** | 仅在 dev 上选阈值并冻结。 |
| **Status** | **confirmed defect** |

### A4-22 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 159–188；`cli.py` 571–580 |
| **Trigger** | 协议 §6；GOAL §5.14；DECIDE-01。任务：Gate 0–2 未注册 **不是** 缺陷。 |
| **Paper requirement** | 用户未给阈值则不得编造 pass/fail。不得把 fixture 写入科学结论。 |
| **Repro / evidence** | 复跑 analyze：`gates.*.decision=unregistered`，`threshold=None`，`scientific_conclusion=None`，`status=not_evaluated`。`test_week8_never_passes_unregistered` 锁住该行为。 |
| **Impact** | 正确持守。分流缺口见 A4-11，不在此条升格为 Gate 缺陷。 |
| **Suggested fix** | 不要添加阈值。 |
| **Status** | **non-defect** |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5。

1. **Gate 0–2**：无阈值、无 pass/fail（A4-22）。
2. **`scientific_conclusion` 保持 `None`**；无表时 analyze 为 `not_evaluated`。
3. **REST-01/02/03** 禁词列表存在；P3 不自动写“只是后果”；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
4. **身份对齐不含值**。
5. **$R_{\mathrm{task}}$ 祖先**、**$S/M$ 空分母→null**、**缺/空 sham→excess null**、**signed excess 不截断**、**逐步平均 $\rho$**。
6. **有限扫描**：`exhaustive=False` 时 `no_change` 不作已知负。
7. **交换公式** $H^b+\Pi_Z(H^d-H^b)$ 复跑 `[1,1]`。C-rand 拒绝缺主干预范数。
8. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$。
9. **4096 vs 3584 直接迁移 N/A**。
10. **官方 iGSM 快照拒裸 `G`、排除共享 RNG、mod 23**；夹具拒绝 `official`。
11. **GSM-Plus 锁定 test**；无侧车 Symbolic 拒编辑。
12. **no-op 派生名** `reasoning_diff_noop`。
13. **Hotpot 声明 supporting_facts 不是完整 DAG**。
14. **宿主 exec 被禁止**。
15. **INLP 在已投影表示上迭代**（库函数）。
16. **假说不要求正结果**：本通道不因无 F1/AUC 正数判失败。
17. **P1 留出路径现为 IRLS logistic**（不再把“P1 不是 logistic”原样重开）。
18. **T2/T3/T4 placeholder** 不再把前 N 字标成 fact。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_full_cli_smoke` | 八阶段返回 0；**offline** $H$；`not_evaluated` | generate、论文 $H/E$、干预生成、嫁接 |
| `test_repair_reprefills_and_refuses_gate` | 非空字符串 ⇒ `refilled_prefix` | Prefill/decode |
| `test_verbalizer_supervision_contract` | 未训练监督档报错；reflection 标 retrospective | 同划分微调 / 四档生成 |
| `test_p1_precomputed_is_scores_not_magic` | `rho==length` ⇒ `delta_auc==0` | 论文 logistic 定义 |
| `test_p1_held_out_logistic_detects_rho` | 留出 IRLS 能分开 $\rho$ | bootstrap / 问题级区间 |
| `test_collect_and_intervene_tiny` | logits 因 `+0.01` 改变 | $\Pi_Z$ 交换 |
| `test_c3_m01_event_mean_not_union` | 逐步平均 | CLI 仍用合成轨迹 |

---

## 8. 本审查复跑的命令（均可再跑）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → **56** / `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `main(['prepare', …, '--eval-mode','scientific'])` 无 fractions → `ValueError`；有 fractions → fixture 文本轨迹。
4. `collect --backend offline` → `H=[1..8]`；`scientific --backend offline` → 拒绝；`scientific --backend tiny` → 相同 $E$ 行。
5. `intervene` offline → `donor_missing`；tiny → `geometry_on_hidden` / `timing=pre_step`。
6. `repair` → `generated_tokens=0`，`extra_prefill_tokens=split() 词数`。
7. `analyze` → `p1=p2=p3=None`，`scientific_conclusion=None`，Gate `unregistered`。
8. `verbalizer` / `sequence_score` / `apply_swap` / `cone_fit` / `ie_z` / `week8_decision({excess:0})` / `apply_source_value_edit` / 域加载器：见 §5。

---

## 9. 结论

**冻结 hash：HASH_MATCH** `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`（56 文件）。

**原文一致性：不通过（FAIL）。**

库层有一批忠实公式，且本轮修好了逐步 ρ、P1 默认启发式、placeholder 前提、scientific 拒 offline-$H$/loss 等卫兵。科学入口与账本仍把夹具轨迹、复制均值 $E$、几何 `pre_step`、不生成的 repair 和过期 pytest 65 标成论文实现。Gate 0–2 未注册、假说不要求正结果——这两条被遵守。作者关闭与绿测不能关闭本通道。

独立复审关闭条件（本通道）：A4-01–A4-06 必须在**同一冻结 hash** 上对照原文关闭（科学入口不再替身，或账本诚实降级为 `unimplemented`/`fixture_only`）；其余 medium 项至少改为诚实状态或补上测量入口。
