# 审查报告 A：原文一致性（paper consistency）— round-05

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-05 |
| **审查时间** | 2026-09-21 01:33–03:20（UTC+8） |
| **声明冻结 hash** | `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（58 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **HASH_MATCH。** 按 `VERSION.md` 原文 Python 逐字复算：文件数 **58**，摘要 `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`。审查对象即该冻结工作树。相对 r04 新增 `src/reasoning_diff/models/tokenize.py` 与 `tests/test_round04_regressions.py`。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `E481EB84664E1F71EE5551FB3451F764B8FB7D21691B89E5DFFC67773B3090C4`（与账本 **§0** 及 TR-0322 段行内 hash **一致**；r04 的 A4-12 本轮不再成立） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-05/{B,C,D,E,F}-*.md`。**未把** `ISSUES.md` 作者关闭当作关闭。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |

**总判：不通过。** 冻结 hash 可核验。相对 r04，科学入口的五项猎点里有四项在**字面接口**上已接通：`--eval-mode scientific` 调用 `generate_task_trace`/`decode_loop`，不再拼节点真值；tiny collect 写 60–75% 层与前提 span 均值 $E$（行不再相同）；几何-only 干预写 `timing=offline_hidden` 而不写 `pre_step`；repair 在 scientific/tiny 上 Prefill/decode，offline 诚实 `refilled_prefix=False`。这四项**不得**按 r04 原文原样重开。

本轮仍 FAIL，因为：(i) scientific generate 的轨迹**没有解析出任何事件**（6 条轨迹 `n_events=0`，`n_obs=0`），$H$ 退化为整段末 token，却仍走“已测 scientific”路径；(ii) 账本仍用 `implemented_local` + `passed_local_tests` + `python -m pytest -q` 关闭可执行行（已去掉 “pytest 65” 计数，但关闭方法未改，且 TR-0125/0135/0158 等仍指到无关符号）；(iii) P1 bootstrap、域真值、四档 verbalizer/BoundaryMLP 的 CLI、槽位嫁接、干预四项结局等论文可执行条款仍是替身或未接线。假说不要求正结果——本通道不因 P1–P3 无正数判缺陷。Gate 0–2 保持 `unregistered`，**不是缺陷**。

---

## 0. 相对上一轮树的诚实变化（避免把已修项当新缺陷）

独立重读当前字节并复跑后，下列 **不再** 作为本轮 confirmed defect 原样重开（不等于科学语义已齐）：

| 先前问题（r04） | 当前树（本轮复跑） |
|---|---|
| `--eval-mode scientific` 拼 `"p1 = 4 \| p2 = 0 \| q = 0"` | scientific prepare 调用 `generate_task_trace`。产物 `model=tiny-qwen2`，`generation=decode_loop`，`weight_source=random_init`，文本为题干 + 随机 decode 字符。**不再**是节点真值拼接。 |
| 默认/scientific $H$=prefix id；$E$ 行复制 | scientific 拒 `offline_prefix_ids`。tiny：$E=(2,32)$ 且 `E_ROWS_IDENTICAL=False`，`hidden_layer=1`（3 层的 60–75% 带），`pooling=premise_span_mean`。offline 夹具路径仍写 prefix id（冒烟，非 scientific）。 |
| `intervene` 几何行写 `timing=pre_step` | 几何-only（`--backend offline` + 可区分的 $H$ 两行）：`status=geometry_on_hidden`，`timing=offline_hidden`。hook 路径才写 `pre_step`。 |
| `repair` 用 `split()` 词数冒充 Prefill | scientific：`execute_repair_tiny` + `decode_loop`，`generated_tokens=8`，`refilled_prefix=True`，$k\in\{1..5\}$。offline：`refilled_prefix=False`，`status=prefill_unavailable`。 |
| verbalizer = `gold[:4] in prefix` | 无 `generate_fn` → `status=generate_unavailable`，`score=None`。 |
| P1 无 bootstrap 键 | 有 `bootstrap` 键；但区间是常数列表，见 A5-03。 |
| Week-8 对 `excess=0` 仍 `not_evaluated` | `week8_decision({excess:0})` → `c3_negative_descriptive`。CLI 有 `null_reason` → `measurement_unresolved`。 |
| REQUIREMENTS 行内 hash `B0228A57…` | TR-0322 及后续 REQUIREMENTS 行现为 `E481EB84…`，与 §0 一致。 |
| `SubprocessExecutor` 挂在 Isolated 谱系 | `ChildProcessExecutor.isolated_sandbox=False`，不再是 `IsolatedExecutor` 子类。 |
| `apply_source_value_edit` 无同值异源 | `make_source_value_pair` 现同时构造两条件；元数据 `same_value_diff_source=True`。 |
| scientific sham 用同一 `base_text` | scientific sham 为 `generate(..., seed=2)`，文本/token 与 seed=0 不同。 |
| 无注意力 dev 阈值函数 | `fit_attention_threshold(..., split="dev")` 存在；CLI 不调用。 |
| 无三轨迹入口 | scientific 现产 $T_0(seed=0)$、$T'_0(seed=1)$、$T_{\mathrm{pert}}(seed=0)$，并扫 `allowed_edits`。 |

**未关闭：** §4.1 在 generate 之后仍无可用 `parse_events` / $R_{\mathrm{behavior}}$；账本仍用 pytest 关闭可执行行；P1 区间是假 bootstrap；域编辑常 `needs_truth`；CLI 不训 BoundaryMLP / verbalizer；修复不是槽位嫁接；干预四项结局为 `None`。

---

## 1. 逐文件覆盖

每行：路径（磁盘 `splitlines()` 行数）— 对照条款 — 结论。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 1–517 | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 1–86 | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。Gate 保持 null 与代码一致。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 1–166；§5 = 73–91 | GOAL §5.1–5.15 | 第 2、3、6–8、10–13 条在科学入口仍被降级或替身。第 14、15 条本轮更诚实。 |
| `.planning/REQUIREMENTS.md` | 1–76 | DATA/MEAS/MODEL/PROBE/… 与 atomics | 复选框全空；状态表仍写 `implemented_local`。行内 hash 已与 §0 对齐。 |
| `.planning/PAPER_TRACEABILITY.md` | 1–44 约定；75–120、202–243、370–420 抽样 | 账本不得当实现证据 | ≥100 处 `implemented_local` + `passed_local_tests`。`python -m pytest -q` 仍约 79 处。可执行行常指到无关符号。已去掉 “pytest 65”。 |
| `pyproject.toml` | 1–27 | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 有 `torch`/`transformers`。无强制 scientific 栈。 |
| `src/reasoning_diff/__init__.py` | 1–5 | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 1–4 | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 1–385 | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 1–46 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先与相交掩码正确。默认 cone 走任务祖先，不是行为头 $\hat R^{\mathrm{val}}$。 |
| `src/reasoning_diff/events.py` | 1–196 | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 对齐 | 身份对齐正确。`align_events_monotonic` 存在。`parse_fixture_events` 只认 `alias = NUMBER`；对题干 `q = p1 * p2` 与随机 decode **零事件**。策略仍只读 `status=="strategy_change"`。 |
| `src/reasoning_diff/edits.py` | 1–277 | §7 T1 重算；GOAL §5.2 | 值编辑+表达式重算正确。`make_source_value_pair` 现有同值异源。 |
| `src/reasoning_diff/measure.py` | 1–342 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集、空分母、缺/空 sham→null、signed excess、逐步平均正确。有 `to_noise`/`csp_noise` 与 `probe_prf1`。CLI 无事件时 CSP 面为 null。 |
| `src/reasoning_diff/analysis.py` | 1–283 | §2.6 P1–P3；§7 分流；附录 S2–S4 | P1 留出 logistic + 偏相关。bootstrap 键在，但是常数。`week8` 现能走出 `measurement_unresolved` / `c3_negative_descriptive`。`retrieval_scatter` 可对文本做 BOW。 |
| `src/reasoning_diff/interventions.py` | 1–115 | §2.4 交换/对照/INLP/救援/$\mathrm{IE}_Z$ | 交换式、范数匹配、`ie_z`、`select_weak_layer` 库层正确。CLI 几何行不再冒称 `pre_step`。四项结局仍由调用方填 `None`。 |
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、`fit` 形式正确。CLI tiny 维 32 故 `rank=32`。 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | §4.2 Hidden=256 ReLU | 架构+`fit` 符合。CLI 从不 import。 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | §2.5 命题 2 | 分位数与 $+\infty$ 正确。`truth_indices` 可限制到 $R(s_i)$。CLI 传入的是**全局**正列并集。 |
| `src/reasoning_diff/probes/__init__.py` | 1–3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 1–120 | §8 文本/注意力/四档自述；GOAL §5.7 | 监督 BOW。verbalizer 无生成器则拒。`fit_attention_threshold` 在。CLI 不调用本模块。 |
| `src/reasoning_diff/transfer.py` | 1–63 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。`common_dim_then_procrustes` **截断**到 `min(dim)`，不是先学共同维映射。 |
| `src/reasoning_diff/repair.py` | 1–189 | §3 Repairability/RR；§9 嫁接；GOAL §5.13 | 有 `execute_repair_tiny` 与诚实拒绝。掩码只改前缀字符串，不是原槽位嫁接。`consecutive_repairs` 循环 $k=1..5$，但 `slots=["q"]` 时 $k\ge2$ 与 $k=1$ 同执行。 |
| `src/reasoning_diff/cli.py` | 1–893 | §4 流水线；§8.2 scientific | scientific prepare/collect/repair 已接线 generate/span/Prefill。事件为空则后续 label/fit 崩或空转。`fit`/`calibrate`/`intervene` 仍有替身。 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | §8.1 模型卡/revision | 两张冻结卡 + `local_files_only=True`。CLI 不加载。无权重时属 pending_server。 |
| `src/reasoning_diff/models/collect.py` | 1–183 | §4.2 $h_i/e_j$；GOAL §5.6/5.10 | `collect_hidden_trace`：读出层 + span 均值。无事件时 $H$=末 token，返回值仍写 `h_position=pre_step`。`intervene_tiny` 现为 $\Pi_Z$，不是 `+0.01`。`intervene_swap_decode` 在 `"follow donor"` 提示上 hook。 |
| `src/reasoning_diff/models/features.py` | 1–39 | §2.4 三时机；GOAL §5.6 | 跨界 token 排除正确。 |
| `src/reasoning_diff/models/generate.py` | 1–143 | §8.2 自然轨迹 | 显式 decode 循环。CLI scientific prepare 调用它。`parse_fixture_events` 吃随机 decode → 零事件。 |
| `src/reasoning_diff/models/tiny.py` | 1–120 | 本机 hook 边界 | 随机 Qwen2/3 + resid_post。不是论文模型路径。 |
| `src/reasoning_diff/models/tokenize.py` | 1–32 | §4.2 层带 / span | `readout_layer_index`：3→1，32→21，36→23。`span_token_indices` 先含后交。1 字符 = 1 token。 |
| `src/reasoning_diff/models/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/tasks/catalog.py` | 1–39 | §7 适配入口 | 快照分发。CLI 默认 `t1_fixture`。不生成 500 题。 |
| `src/reasoning_diff/tasks/t1_official.py` | 1–92 | §7 T1；template≠G | 快照加载拒绝裸 `G`、排除共享 RNG、默认 mod 23。`load_igsm_directory` 存在。CLI 默认不走。 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | 官方/夹具分离 | 拒绝非 `fixture`。成立。 |
| `src/reasoning_diff/tasks/t1_config.py` | 1–21 | op∈{5,10,15,21}，n=500 | 配置校验。无数据生成。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–84 | §7 T2；GOAL §5.2 | 无侧车：placeholder + `graph_status=unknown`，拒编辑。有侧车：值编辑+算子逆转。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–79 | §7 T2；评测专用 | test-only 锁正确。`apply_plus_numeric_edit` 改字面，答案 `needs_truth`/`None`。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 1–100 | §7 T2-noop | 可造配对与分层元数据。无注入句值扰动扫描。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 1–104 | §7 T3；supporting_facts≠DAG | 标记正确。无独立新答案则 `needs_truth`。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 1–110 | §7 T3 组成引用 | 保留 answerable/unanswerable。`expression="composition_reference"` 不可重算。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–78 | §7 HumanEval-Perturb；GOAL §5.15 | `edit_kind=input_list` 有旗。无新解则 `needs_truth`。`invariant_behavior_unspecified=True`。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 1–51 | §7 T4；Fig.6 | 四类状态强制区分。前提=placeholder。`apply_t4_question_edit` 为 `needs_truth`。无相图。 |
| `src/reasoning_diff/tasks/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/executor.py` | 1–109 | GOAL §5.15 | 禁止宿主 exec。默认 `UnavailableExecutor`。`ChildProcessExecutor` 明确非沙箱。 |
| `src/reasoning_diff/scoring.py` | 1–30 | §3 域内评分 | 数值/QA 精确匹配。代码经执行器接口。 |
| `src/reasoning_diff/splits.py` | 1–110 | §4.1 共组；GSM-Plus test-only | 六角色 + 家族共组。默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 1–53 | GOAL §5.4 | sample/direction/perturb/bootstrap/split 分离。 |
| `src/reasoning_diff/io.py` | 1–133 | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 1–11 | — | 夹具路径。 |
| `tests/test_cli_pipeline.py` | 1–29 | §4 流水线 | 八阶段 exit 0；**仍强制** `--backend offline`。 |
| `tests/test_science.py` | 1–101 | 校准/迁移/交换/Week-8 | 库函数微例。`test_repair_reprefills_*` 现断言无 execute → `refilled_prefix=False`。 |
| `tests/test_measure.py` | 1–40 | $S/M$、联合编辑反例 | 与公式一致。 |
| `tests/test_review_regressions.py` | 1–394 | 上轮回归 | 锁住若干库修补；仍锁 `precomputed` 启发式。 |
| `tests/test_round03_regressions.py` | 1–291 | r03 回归 | 锁住逐步密度、placeholder、logistic；**同时**锁 `precomputed_scores`。 |
| `tests/test_round04_regressions.py` | 1–310 | r04 猎点 | 锁 generate≠节点真值、span $E$、几何≠`pre_step`、Prefill/k=1..5。**不**锁事件非空或 $R_{\mathrm{behavior}}$。`test_p1_returns_bootstrap_interval` 只断言键存在。 |
| `tests/test_tracer_t1_prepare.py` | 1–100 | T1 夹具准备 | 身份/重算/空分母。 |
| `tests/test_t1_official.py` | 1–31 | template≠G | 快照形状。 |
| `tests/test_t2_gsm.py` | 1–33 | T2 | 侧车数值编辑。 |
| `tests/test_t3_t4.py` | 1–44 | T3/T4 | supporting_facts ≠ DAG。 |
| `tests/test_artifacts.py` | 1–73 | I/O | 工程。 |
| `tests/test_generate_loop.py` | 1–17 | 可重放采样 | tiny decode。 |
| `tests/test_tiny_hooks.py` | 1–27 | hook 清理 | 本机接口。 |
| `tests/test_tiny_cache.py` | 1–26 | 缓存隔离 | `intervene_tiny` 现断言 logits 因 $\Pi_Z$ 改变。 |

第三方库：审查了本项目对 `numpy` / 可选 `torch`+`transformers` 的使用假设，未审查依赖源码。

夹具抽读：`tests/fixtures/t1_tiny.json`（全文）、`t2_gsmplus_one.json`、`t2_symbolic_one.json`、`t4_boundary.json`。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献清单 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。Gate 保持 null（非缺陷）。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 2、3、6–8、10–13 条在科学入口仍被降级或替身。 |
| C4 | 阅读 `PAPER_TRACEABILITY.md` 约定，抽样 TR-0001–0043、TR-0125–0137、TR-0158–0166、TR-0293–0346、TR-0400 | 账本把可执行缺口标成 `implemented_local`，验证列写 pytest / `passed_local_tests`。**不能**作为覆盖证据。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。 |
| C6 | 对照公式手核 + 复跑：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1、cone | $R_{\mathrm{task}}$/差集/交换/分位数/拒维度：**库函数层符合**。P1 留出路径：**符合 logistic**。P1 bootstrap：**常数区间**。$a(X)$ 库层有 `truth_indices`；CLI 用全局正列。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | scientific **调用** generate（seed 0/1/edit + allowed_edits + sham seed=2）。`parse_fixture_events` 零事件 → 0 条 observation。label 空；fit 拒 “identity labels”。 |
| C8 | 对照 §4.2 / §8 探针与基线 | 双线性可拟合（夹具路径）。tiny $E$ 行不同。BoundaryMLP / verbalizer / 注意力 **CLI 零引用**。 |
| C9 | 对照 §2.4 / §6 干预 | 几何-only 写 `offline_hidden`。tiny hook 写 `prospective_decode`/`pre_step`，对象是 `"follow donor"` 提示，不是对齐的 $s_k$。四项 `None`。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 | T1 值编辑成立。GSM-Plus 有改字面、无新 oracle。无侧车 Symbolic 拒编辑。T3/T4 常 `needs_truth`。 |
| C11 | 对照附录 S1–S4、C4 掩码、$k\in\{1..5\}$、失效相图 | scientific repair 循环 $k=1..5$ 但槽位名不改执行。S2 库在。S3 截断维。S4 为 BOW。无相图。 |
| C12 | 抽读测试是否固化替身 | 是：`test_full_cli_smoke` 强制 offline $H$；`test_p1_returns_bootstrap_interval` 只看键；`test_scientific_prepare_*` 不要求事件非空。 |
| C13 | 独立重算论文/协议/GOAL/REQUIREMENTS SHA-256 | 四份与账本 §0 一致。REQUIREMENTS 行内 hash 已跟上。 |
| C14 | 独立重算声明代码冻结 hash | **HASH_MATCH** `4c8769f3…`，58 文件。 |
| C15 | 复跑 CLI prepare/collect/fit/calibrate/intervene/repair/analyze 与库函数微例 | 见各 finding 的 Repro。命令已在本审查重跑，不是转述。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 全量 `pytest -q` 作为本通道验收 | 原文符合性不由绿测关闭。作者声称 120 passed；本报告不声称测试通过。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量 500 题 | 协议 §7：科学结论 `pending_server`。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | 科学入口无解析出的步骤，故无论文定义的逐步 $H$ 与分头标签矩阵。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读 round-05 B–F。 |
| N6 | `PAPER_TRACEABILITY.md` 全部 528 行逐字复读 | 已读约定与高风险可执行/GOAL/REQUIREMENTS 行。剩余多为同一模板重复。 |
| N7 | 真实隔离沙箱跑 HumanEval | 无合格隔离后端；`ChildProcessExecutor` 不能冒称沙箱。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | generate/span/Prefill 接口在；事件/标签/干预结局空 | subst |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 1 | 34–35 | 检索余弦 vs 答案变 | exec | `retrieval_scatter` 可吃文本→BOW；不是论文嵌入 | subst |
| 论文 1 | 38 | 修复解码/Prefill/耗时 | exec | tiny 路径有 generated/prefill 计数；不是槽位成本 | ok-lib / subst |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema + 夹具解析；scientific 无事件 | ok-lib / subst |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | 字段正确；scientific 0 条 observation | subst |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | id + aliases 词边界 | ok-lib |
| 论文 2.3 | 88 | 消失/合并/策略分岔 | proto | `removed` 有；策略 `status_field_only`/`scanned=False` | stub |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap`；手核 `[1,0]+Π([0,1]-[1,0])=[1,1]` | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ | math | `ie_z` 现被 CLI 写入 report（向量均值，不是 $g$） | ok-lib / subst |
| 论文 2.4 | 106–108 | 前瞻 hook/KV/前缀 | exec | tiny $\Pi_Z$ + decode；对象是 `"follow donor"` 不是 $s_k$ | subst |
| 论文 2.4 | 110 | 步前/数值前/步尾 | exec | 库函数区分；无事件时 $H$=末 token 且自称 `pre_step` | subst |
| 论文 2.4 | 114–117 | C-rand / C-layer 同幅度四项 | exec | 范数匹配在；无 `--dev-layer-scores` 时 `dev_scores_missing`（诚实）；四项 `None` | stub / ok |
| 论文 2.5 | 121–125 | cone / Oracle / 行为掩码 | math | `dirty_cone`/`oracle_mask`/`behavior_mask` | ok-lib |
| 论文 2.5 | 127–130 | 命题 1 + REST-03 | math | $xy$ 反例夹具 | ok-lib |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | 分位数 ok；CLI 用全局正列并集 | subst |
| 论文 2.5 | 141–142 | 原轨迹槽位、禁重拓扑 | exec | Prefill 整段前缀字符串，不复用槽位 | subst |
| 论文 2.6 | 148–156 | $S,M,\rho$，空分母 N/A | math | `dependency_densities` + event mean | ok-lib |
| 论文 2.6 | 158 | 噪声先扣除 | proto | scientific sham 真不同 seed；无事件 → `noise_set_empty` / excess null | ok / stub |
| 论文 2.6 | 164 | P1 logistic + 偏相关 + bootstrap | math | 留出 IRLS + 偏相关；bootstrap 为常数 | subst |
| 论文 2.6 | 165 | P2 配对 + 污染位置 | exec | 现收 `contamination_positions`；无表则 CLI `None` | ok-lib |
| 论文 2.6 | 166 | P3 Δacc + 对照 + 非目标 | exec | 库函数收 nontarget；CLI 无表则 `None` | ok-lib |
| 论文 2.6 | 168 | REST-02 | proto | `causal_reverse_claim=False` | ok |
| 论文 3 | 176–186 | TO_all/clean、CSP、覆盖、脏变、P/R/F1 | math | TO/CSP/覆盖/脏变/对错 facet 有；CLI analyze 用 probe **loss\<0.5** 冒充预测 | subst / ok-lib |
| 论文 3 | 188 | TO/CSP 噪声参照与比值 | proto | 有 `to_noise`；无事件则 `csp_noise=None` | stub |
| 论文 3 | 190 | 干预三项并列、前瞻/回溯分列 | proto | 范数三列有；结局硬编码 None | stub |
| 论文 3 | 194–200 | Repairability、RR、成本分列 | math | 两公式有；scientific 有 token 计数；非槽位预算 | stub |
| 论文 4.1 | 232–253 | 双标签流水线；NL 单调对齐；共组 | exec | generate 在；parse/align 对随机 decode 为空；NL 函数在、无 CoT 解析 | subst |
| 论文 4.2 | 257–267 | MLP 训练、双头、池化 $e_j$、60–75% 层 | exec | 层/池化在 tiny 接通；无事件则 $h_i$ 不是步边界；MLP 未进 CLI | subst |
| 论文 5 Fig.1–2 | 291–299 | 热力图、三时机比较、跨模型迁移入口 | exec | 无导出；analyze 只报 4096/3584 N/A | missing |
| 论文 6 | 301–313 | 解耦资产、前瞻交换、INLP、救援 | exec | 配对构造器在；执行仍是向量几何 + `"follow donor"` | stub |
| 论文 7 | 315–329 | P1–P3 测量入口（不要求正结果） | exec | 有表才算；默认 `p1=p2=p3=None` | stub |
| 论文 8 | 331–341 | 注意力/四档 verbalizer/监督文本 | exec | 库层不再子串；CLI 不调用 | stub |
| 论文 9 / Table 1 | 343–355 | 五条主对照 + 三条附录掩码实跑 | exec | 掩码改前缀字符串；decode 相同预算 | stub |
| 论文 Fig.6 | 353 | 失效相图五类 | exec | T4 状态枚举 ≠ 相图 | missing |
| 附录 S1 | 357–359 | $k\in\{1..5\}$ 连续编辑 | exec | 循环在；槽位不增长 | stub |
| 附录 S2 | 361–367 | 两参数锥拟合 | math | `cone_fit` 拟合；CLI 需 `cone_table.jsonl` | ok-lib |
| 附录 S3 | 371–373 | 共同维 + Procrustes | exec | `a[..., :dim]` 截断 | subst |
| 附录 S4 | 375–377 | 嵌入余弦散点 | exec | BOW 点积，不是文本嵌入模型 | subst |
| 论文 7 数据 | 399–409 | T1–T4 假设专用资产 | exec | 读取器+部分 apply*；真值常 `needs_truth` | stub |
| 论文 8.2 | 419–431 | `--eval-mode scientific` | exec | 开关调用 generate；后续无事件/无标签 | subst |
| 论文 9 | 435–445 | 第一周三轨迹/50 干预冒烟 | exec | 三轨迹入口在；50 条解耦干预无 | stub |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |

---

## 5. Findings

### A5-01 — scientific 已调用 generate，但解析零事件，$H$ 退化为末 token 并自称 `pre_step`

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` `cmd_prepare` 271–283；`models/generate.py` `generate_task_trace` 105–110；`events.py` `parse_fixture_events` 27–75；`models/collect.py` 55–58、78 |
| **Trigger** | 对照论文 §4.1 伪代码（232–248）与 §4.2 $h_i$（261–262）：`T0=generate` 之后必须 `parse_events`，再在步边界取 $h_i$。猎点“必须调用 generate、不得拼节点真值”**已满足**，不得按 A4-01 原文重开。 |
| **Paper requirement** | 自然轨迹上的步骤事件（变量/表达式/版本/作用域）；$R_{\mathrm{behavior}}$ 来自 `allowed_edits` 后再 generate 的值变化；$h_i$ 为步边界隐状态。 |
| **Repro / evidence** | 复跑：`prepare --eval-mode scientific` 无 `--split-fractions` → `ValueError: scientific mode requires explicit --split-fractions`。加上六比例 + `--sham-opportunities 1` → exit 0，**6** 条轨迹，全部 `model=tiny-qwen2`，`generation=decode_loop`，文本如 `'p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC'`，**不是** `p1 = 4 \| p2 = 0 \| q = 0`。`n_events=0`，`n_obs=0`，`n_labels=0`。`to_csp.csp=None`，`to_noise=0.86`。`collect --backend tiny`：$H=(6,32)$（每条轨迹 1 个末 token），`H_pre_step.shape=(1,32)`（只留最后一条 meta），`h_position` 库层仍写 `"pre_step"`。`label` 后 `fit` → `ValueError: fit refuses identity labels`。夹具路径仍拼节点真值（`model=fixture`），这是 fixture 模式，不是本条指控对象。 |
| **Impact** | C1/C3 的可执行入口仍没有步骤层标签与步边界 $H$。generate 被接通，但 §4.1 树在 parse 处断开。账本 TR-0125 指向 `measure.dependency_densities`，掩盖这一点。 |
| **Suggested fix** | 为 generate 文本提供能产出事件的解析（或在无事件时拒绝 scientific 的 collect/fit，并保持 `unimplemented`）。禁止把末 token 标成 `pre_step`。 |
| **Status** | **confirmed defect**；真实 CoT 质量 **pending_server** |

### A5-02 — 账本仍用 pytest 关闭可执行行（已去掉计数，关闭方法未改）

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` 例如 TR-0125（L202）、TR-0134–0135（L211–212）、TR-0158–0159（L235–236）、TR-0308、TR-0316、TR-0319、TR-0327–0334、TR-0346、TR-0400；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：账本必须能反向核验。账本自己写：“`pytest -q` 不得单独关闭可执行行”“fixture CLI 不得写成 scientific 已测”。猎点针对 **pytest 计数关闭**；本轮已无 “pytest 65 passed”，但 `impl_status=implemented_local` 且 `local_verify_status=passed_local_tests`，`verification_method` 仍大量是 `python -m pytest -q`。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。未实现不得标已实现。 |
| **Repro / evidence** | 本文件约 100 处 `implemented_local`，约 79 处 `python -m pytest -q`。抽样：TR-0125 要求多 seed generate + `allowed_edits` 全扫描，实现列仍是 `measure.dependency_densities`。TR-0135（$e_j$ 池化）仍指向 `bilinear.py`，不是 `collect.py`/`tokenize.py`。TR-0158 / TR-0400（解耦任务构造）指向 `intervention_report`。TR-0346（连续编辑）指向 `run_repair`（循环在，槽位语义无）。REQUIREMENTS 复选框全空，状态表写 `implemented_local`。 |
| **Impact** | 覆盖率仍被制成 16/16。独立审查若信账本会漏检 A5-01 及未接线条款。 |
| **Suggested fix** | 未接到科学语义的条款改回 `unimplemented` / `ok-lib_unwired`。禁止用 pytest 通过与否关闭可执行行；验证列写对照原文的复跑产物。 |
| **Status** | **confirmed defect** |

### A5-03 — P1 的 bootstrap 区间是常数列表（不要求正结果）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `p1_incremental` 76–77 |
| **Trigger** | 论文 2.6 表 P1；协议 §5；GOAL §5.12。假说不要求正 AUC，但区间必须是问题级重采样。 |
| **Paper requirement** | 留出 logistic AUC、偏相关、**问题级 bootstrap 区间**。 |
| **Repro / evidence** | 留出路径 `estimator=held_out_logistic`，偏相关键存在。`groups` 非空时：`bootstrap_cluster([float(delta)] * len(groups), groups, …)`。复跑 20 点、10 个问题组：`delta_auc=0.5`，`bootstrap.interval=[0.5, 0.5]`。`test_p1_returns_bootstrap_interval` 只断言键非空，锁住替身。无表时 CLI `p1=None`（本机复跑确认）。 |
| **Impact** | Week-8 不能表示“已按论文统计量给出问题级不确定性（含负结果）”。 |
| **Suggested fix** | 对问题聚类重算 $\Delta\mathrm{AUC}$，再取分位数。删除或隔离 `precomputed` 启发式。 |
| **Status** | **confirmed defect** |

### A5-04 — 校准入口仍不是逐步 $j\in R(s_i)$，并用变体扩大 $N$

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_calibrate` 578–593；`calibrate.py` `sequence_score` 20–25 |
| **Trigger** | 论文 2.5 L132–139；GOAL §5.8。库层 `truth_indices` 是相对 r04 的进步，不得把“无该参数”原样重开。 |
| **Paper requirement** | $a(X)=\max_{i,j\in R(s_i)}(1-\hat p_{ij})$；空真集取 0；交换单位是轨迹/序列或声明的问题块。不得把同题重复当独立样本扩大 $N$。 |
| **Repro / evidence** | 分位数公式正确（`[0.1,0.2,0.3,0.4], α=0.4` → $q=0.3$；$\alpha=0.1$ → $+\infty$）。`sequence_score(..., truth_indices=[0])` 对 `[0.9,0.1,0.2]` 得 `0.1`（库层符合）。CLI 把**全部** `task_label==1` 或 `behavior_label==1` 的前提列做成一个全局 `truth`，再对每行 $H$ 用同一集合。夹具 tiny 校准产物：`scores=[0.0, 0.0]`，`n_problems=2`（base 与 edit 两个 `task_id`，不是两道独立题），`unit=problem`。scientific 无探针权重时拒绝 loss/字面分数（卫兵成立）。 |
| **Impact** | 保形集合在 CLI 入口上仍不是命题 2 的 $R(s_i)$。 |
| **Suggested fix** | 逐步使用该步的 $R(s_i)$；一题的多种子/编辑不得扩大问题级 $N$。 |
| **Status** | **confirmed defect**（CLI）；库函数 `truth_indices` 本身非缺陷 |

### A5-05 — GSM-Plus / 无侧车 T2 / T4 没有“合法编辑 + 更新真值”

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t2_gsm_plus.py` `apply_plus_numeric_edit` 50–74；`t2_gsm_symbolic.py` 43–44, 68–70；`t4_boundary.py` 26, 36–50；`t3_humaneval.py` 34–74 |
| **Trigger** | 论文 §7 L403–407；GOAL §5.2；DATA-02。r04 的“无 apply*”对 Plus 不再成立。 |
| **Paper requirement** | 各域：读取、合法编辑、**更新后真值**、事件/独立标注、域内评分。缺失标注保持 unknown，不得凭空生成。 |
| **Repro / evidence** | Plus：`premises[0].kind=placeholder`；`apply_plus_numeric_edit(plus,"4","5")` → `validity=needs_truth`，`answer_spec.value=None`。Symbolic 无侧车：`graph_status=unknown`，`kind=placeholder`。T4：四状态齐全，前提仍 placeholder，`apply_t4_question_edit` → `needs_truth`。HumanEval `input_list` 有旗，无新解 → `needs_truth`，`invariant_behavior_unspecified=True`。Hotpot/MuSiQue 无新答案 → `needs_truth`（此项诚实）。 |
| **Impact** | 除 T1 值编辑与 T2 侧车外，行为扫描没有更新后的 $v$。 |
| **Suggested fix** | 每域提供编辑+新 oracle；缺失保持 `unknown`/`needs_truth`，不要把读取器标成域适配完成。 |
| **Status** | **confirmed defect** |

### A5-06 — 附录 S3/S4 与 Table 1 没有按论文口径的测量入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `transfer.py` `common_dim_then_procrustes` 57–63；`analysis.py` `retrieval_scatter` 253–257；`repair.py` `mask_prefix` 45–61；CLI analyze 764–779 |
| **Trigger** | 论文附录 S1–S4；S4“不得因精简而删除”。S2 库拟合与 scientific $k$ 循环不得按 r04“空壳/无循环”重开。 |
| **Paper requirement** | $k\in\{1..5\}$ 连续编辑并 Prefill 保留文本；两参数锥拟合；**先共同维映射再** Procrustes；$(P,P\oplus\Delta P)$ **文本嵌入**余弦 vs 答案是否改变；八条掩码实跑。 |
| **Repro / evidence** | `cone_fit` 返回 `lambda/gamma/r2` 且 `wording=descriptive_only`。`retrieval_scatter(texts_a=…)` 走 `_bow`（32 维哈希），不是嵌入模型。`common_dim_then_procrustes` 对 `a[..., :dim]` **静默截断**。CLI `analyze` 无表时 `appendix={}`。scientific repair：$k=1..5$ 但 `slots=["q"]`，`generated_tokens` 全是 8，`extra_prefill_tokens` 全是 32。Table 1 掩码只改前缀字符串。 |
| **Impact** | 附录主张没有从入口到图的论文口径路径。 |
| **Suggested fix** | S3 先拟合共同维；S4 用声明的嵌入；掩码按槽位执行；无资产保持 `not_evaluated`。 |
| **Status** | **confirmed defect**（S2 库函数本身非缺陷；S1 循环存在但语义弱） |

### A5-07 — 四档 verbalizer / BoundaryMLP / 注意力未进入 CLI

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `baselines.py` 92–120、69–89；`probes/boundary.py` 全程；`cli.py` 无引用 |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7；VERB-01 / BASE-01 / BOUND-01 / ATTN-01。子串打分 **本轮不再成立**。 |
| **Paper requirement** | 四档自述；监督档与探针同样本/划分/可见前缀。2 层 MLP 边界检测。注意力阈值在 dev 上选定。 |
| **Repro / evidence** | `verbalizer("zeroshot", …)` → `generate_unavailable` / `score=None`。传入 `generate_fn` 才生成。`fit_attention_threshold` 要求 `split="dev"`。对 `src/reasoning_diff/cli.py` 检索 `BoundaryMLP`/`verbalizer`/`fit_attention`：**零命中**。`cmd_fit` 只训双线性两头；夹具路径两头 **loss 同为 0.05036**（同一 $Y$ 广播到所有 $H$ 行）。 |
| **Impact** | 第 8 节“说不出来”与 Fig.2 边界/注意力列在可执行入口上不存在。 |
| **Suggested fix** | CLI 按同一划分调用四档与 MLP；未接线不得标 `implemented_local`。 |
| **Status** | **confirmed defect** |

### A5-08 — 干预四项结局仍为 None；hook 的 `pre_step` 不是对齐的 $s_k$

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_intervene` 617–663；`models/collect.py` `intervene_swap_decode` 143–183 |
| **Trigger** | 论文 2.4 L106–117；§6 L305–313；GOAL §5.10–5.11。猎点“几何-only 不得写 `pre_step`”**已满足**（本机：`timing=offline_hidden`）。 |
| **Paper requirement** | 目标步首 token 前交换 residual；恢复自回归；评价新生成 $s_k$ 是否跟随 donor。报告四项结局相对对照的差值。C-layer 由开发集弱层确定。 |
| **Repro / evidence** | `apply_swap` 手核通过。offline collect 后 intervene：`status=donor_missing`，`timing=unexpressible`（$H$ 1 行或两行相同）。夹具 tiny 的 $H$ 两行 **allclose=True**，同样 `donor_missing`。scientific tiny：$H$ 可区分 → hook 路径 `status=prospective_decode`，`timing=pre_step`，`followed_donor=false`，`target/nontarget/task_correct/invalid=None`，`clayer_status=dev_scores_missing`（未传 `--dev-layer-scores`，诚实）。hook 作用在 `encode_text("follow donor")` 的 decode，不是对齐步边界。`ie_z` 对救援向量做均值差，不是预指定 $g$。 |
| **Impact** | C2 主张入口仍不是“来源跟随”。几何不再冒称 `pre_step`，但 hook 成功标签过宽。 |
| **Suggested fix** | 在对齐的 $s_k$ 首 token 前 hook；按预注册矩阵评分；无 donor/dev 曲线保持 `unexpressible`/`dev_scores_missing`。 |
| **Status** | **confirmed defect** |

### A5-09 — 修复已 Prefill/decode，但不是原槽位嫁接

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `repair.py` `mask_prefix` 45–61；`execute_repair_tiny` 64–94；`cli.py` 688–708 |
| **Trigger** | 论文 §3 L194–200、§9 L347–355、附录 S1；GOAL §5.13。猎点“必须 Prefill/decode 或诚实 `refilled_prefix=False`”**已满足**。 |
| **Paper requirement** | 干净文本在当前前缀重新 Prefill，**受损槽位**自回归重算。主文 5 条 + 附录 3 条实跑。同原始 token 预算。 |
| **Repro / evidence** | scientific repair：5 条记录，$k=1..5$，`generated_tokens=8`，`extra_prefill_tokens=32`（`ids[:32]`），`refilled_prefix=True`。offline：`refilled_prefix=False`，`failures=["tokenizer_or_model_missing"]`。`mask_prefix` 只改字符串（截断/反转/加指令）。`slots=["q"]` 时 $k\ge2$ 仍只有 `["q"]`。库函数无 execute 时诚实拒绝。 |
| **Impact** | Repairability/RR/同预算曲线无法按槽位测量。C4 附录仍是前缀续写。 |
| **Suggested fix** | 按掩码在原轨迹槽位重算；无槽位资产不得标 Table 1 已跑。 |
| **Status** | **confirmed defect**（槽位语义）；Prefill 接口本身非本条猎点缺陷 |

### A5-10 — 自然语言事件对齐与官方 CoT 解析缺失

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `events.py` `parse_fixture_events` 27–75；`align_events` 119–126；`align_events_monotonic` 132–152 |
| **Trigger** | 论文 4.1 L250–252；2.3 L87–88。单调对齐函数 **本轮存在**，不得说“无该函数”。 |
| **Paper requirement** | 结构化：变量/表达式/版本/作用域。NL：抽实体后允许跳过与合并的单调序列对齐。消失/合并/策略分岔单独计数。 |
| **Repro / evidence** | 只有夹具 `alias = NUMBER` 正则。题干 `What is q = p1 * p2?` 与随机 decode 均 0 事件。无 iGSM 官方 CoT 解析。`strategy_changed` 仅 `status=="strategy_change"`；夹具解析只写 `ok`/`ambiguous`。元数据自标 `scanned=False`（诚实）。`t1_tiny` 步骤 `"q = 0"` 不含 `p1`/`p2` 词，surf 常为 `[]`。 |
| **Impact** | T2/T3 行为标签没有事件层；scientific T1 同样没有。 |
| **Suggested fix** | 分域解析器 + NL 单调对齐；未对齐进单独计数。 |
| **Status** | **confirmed defect** |

### A5-11 — CLI `fit` 把同一标签矩阵广播到所有 $H$ 行；analyze 用 loss 冒充探针 P/R/F1

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_fit` 519–531；`cmd_analyze` 780–784 |
| **Trigger** | 论文 4.2 L265：两头分别学习 $R_{\mathrm{task}}$ 与 $R_{\mathrm{behavior}}$，标签单独保存。§3 要求探针 P/R/F1。 |
| **Paper requirement** | 逐步、分头的标签矩阵；P/R/F1 来自预测集合与真标签。 |
| **Repro / evidence** | `cmd_fit` 对每个 label 的 $j$，把该标量写进 **所有** $i\in[0,H.shape[0])$。夹具 tiny 两头 loss 同为 `0.05036`。`cmd_analyze`：`pred = [1 if r.get("loss",1) < 0.5 else 0 for r in probes.jsonl]`，不是 $\hat p_{ij}$。 |
| **Impact** | 双头与 Fig.1 探针列在 CLI 上无定义。 |
| **Suggested fix** | 按 (event/trace, premise) 对齐 $Y$；P/R/F1 走 `predict_matrix`。 |
| **Status** | **confirmed defect** |

### A5-12 — T1 500 题 / 四档 op 没有 CLI 默认入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t1_config.py` 9–21；`cli.cmd_prepare` 默认 `t1_fixture`；`t1_official.load_igsm_directory` 89–92 未被默认 CLI 使用 |
| **Trigger** | 论文 §7 L403、§9 L437；WEEK1-01。三轨迹 **本轮 scientific 已产**，不得按 A4-16“无三轨迹”重开。 |
| **Paper requirement** | iGSM `op∈{5,10,15,21}`、500 题；$T_0(seed=0)$、$T'_0(seed=1)$、$T_{\mathrm{pert}}(seed=0)$。 |
| **Repro / evidence** | 配置校验存在。本机 scientific 仍一条夹具题。全量 500 属 pending_server；**任务单/四档 op 入口本身**仍是代码缺口。 |
| **Suggested fix** | 配置驱动的任务单；CLI 消费快照目录。 |
| **Status** | **confirmed defect**（入口）；全量跑数 **pending_server** |

### A5-13 — 默认划分比例未预注册

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

### A5-14 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 182–211；`cli.py` 740–794 |
| **Trigger** | 协议 §6；GOAL §5.14；DECIDE-01。任务：Gate 0–2 未注册 **不是** 缺陷。 |
| **Paper requirement** | 用户未给阈值则不得编造 pass/fail。不得把 fixture 写入科学结论。 |
| **Repro / evidence** | 复跑 analyze：`gates.*.decision=unregistered`，`threshold=None`，`scientific_conclusion=None`。本机 scientific 因 `null_reason=noise_set_empty` 得 `status=measurement_unresolved`，`skip_p2_p3=True`。`week8_decision({excess:0})` → `c3_negative_descriptive`。`test_week8_never_passes_unregistered` 锁住 Gate。 |
| **Impact** | 正确持守。假说不要求正结果，本条不升格。 |
| **Suggested fix** | 不要添加阈值。 |
| **Status** | **non-defect** |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5。

1. **Gate 0–2**：无阈值、无 pass/fail（A5-14）。
2. **`scientific_conclusion` 保持 `None`**；无可靠测量时 analyze 为 `not_evaluated` / `measurement_unresolved`。
3. **REST-01/02/03** 禁词列表存在；P3 不自动写“只是后果”；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
4. **身份对齐不含值**。
5. **$R_{\mathrm{task}}$ 祖先**、**$S/M$ 空分母→null**、**缺/空 sham→excess null**、**signed excess 不截断**、**逐步平均 $\rho$**。
6. **有限扫描**：`exhaustive=False` 时 `no_change` 不作已知负。
7. **交换公式** $H^b+\Pi_Z(H^d-H^b)$ 复跑 `[1,1]`。C-rand 拒绝缺主干预范数。几何-only **不**写 `pre_step`。
8. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$。
9. **4096 vs 3584 直接迁移 N/A**。
10. **官方 iGSM 快照拒裸 `G`、排除共享 RNG、mod 23**；夹具拒绝 `official`。
11. **GSM-Plus 锁定 test**；无侧车 Symbolic 拒编辑。
12. **no-op 派生名** `reasoning_diff_noop`。
13. **Hotpot 声明 supporting_facts 不是完整 DAG**。
14. **宿主 exec 被禁止**；`ChildProcessExecutor` 不冒称沙箱。
15. **INLP 在已投影表示上迭代**（库函数）。
16. **假说不要求正结果**：本通道不因无 F1/AUC 正数判失败。
17. **P1 留出路径现为 IRLS logistic**。
18. **T2/T3/T4 placeholder** 不再把前 N 字标成 fact。
19. **scientific 调用模型 generate**，不是节点真值轨迹。
20. **tiny $E$ 为读出层 span 均值**，行不相同；scientific 拒 offline $H$。
21. **repair 无模型时 `refilled_prefix=False`**；有 tiny execute 时走 decode。
22. **REQUIREMENTS 行内 hash 与 §0 一致**。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_full_cli_smoke` | 八阶段返回 0；**offline** $H$；`not_evaluated` | generate、论文步边界 $H/E$、干预生成、槽位嫁接 |
| `test_scientific_prepare_is_generated_not_node_values` | `model≠fixture` 且无节点真值拼接 | 事件非空、$R_{\mathrm{behavior}}$、步边界 $h_i$ |
| `test_scientific_collect_span_pool_and_refuses_offline` | $E$ 行不同、`hidden_layer==1` | $H$ 是步边界而不是末 token |
| `test_intervene_geometry_is_not_pre_step` | offline 几何 `timing≠pre_step` | 对齐 $s_k$、四项结局 |
| `test_scientific_repair_runs_k_1_to_5` | $k=1..5$ 且 `generated_tokens>0` | 槽位嫁接 / 掩码改变执行 |
| `test_p1_returns_bootstrap_interval` | `bootstrap` 键非空 | 问题级重算 $\Delta\mathrm{AUC}$ |
| `test_verbalizer_without_generate_is_unavailable` | 无生成器则 score=None | 同划分四档实跑 |
| `test_p1_precomputed_is_scores_not_magic` | `rho==length` ⇒ `delta_auc==0` | 论文 logistic 定义 |
| `test_collect_and_intervene_tiny` | logits 因 $\Pi_Z$ 改变 | 来源跟随 |

---

## 8. 本审查复跑的命令（均可再跑）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → **58** / `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `main(['prepare', …, '--eval-mode','scientific'])` 无 fractions → `ValueError`；有 fractions → 6 条 tiny decode 轨迹，**0 事件**。
4. `collect --backend offline` → `H=[1..8]`；`scientific --backend offline` → 拒绝；`scientific --backend tiny` → $E$ 行不同，`hidden_layer=1`，$H=(6,32)$ 末 token。
5. `fit` 在 scientific 空标签上拒绝；夹具 tiny 两头 loss 相同。
6. `intervene` offline 几何 → `timing=offline_hidden`；tiny hook → `timing=pre_step` / `"follow donor"`；四项 `None`。
7. `repair` scientific → $k=1..5$，`generated_tokens=8`；offline → `refilled_prefix=False`。
8. `analyze` → `p1=p2=p3=None`，`scientific_conclusion=None`，Gate `unregistered`，`measurement_unresolved`。
9. `verbalizer` / `sequence_score` / `apply_swap` / `cone_fit` / `ie_z` / `week8_decision` / `apply_source_value_edit` / 域加载器：见 §5。

---

## 9. 结论

**冻结 hash：HASH_MATCH** `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（58 文件）。

**原文一致性：不通过（FAIL）。**

r04 猎点中的 generate / span-$E$ / 几何不写 `pre_step` / Prefill-or-refuse，本轮在接口上已接通，不得原样重开。科学入口在 parse 处断开：tiny decode 零事件、零 $R_{\mathrm{behavior}}$、末 token 冒称步前 $H$。账本仍用 pytest 把可执行行标成 `implemented_local`。Gate 0–2 未注册、假说不要求正结果——这两条被遵守。作者关闭与绿测不能关闭本通道。

独立复审关闭条件（本通道）：A5-01 与 A5-02 必须在**同一冻结 hash** 上对照原文关闭（scientific 产出可解析事件与步边界 $H$，或诚实拒绝并降级账本；账本不再用 pytest 关闭可执行行）；其余 medium 项至少改为诚实状态或补上测量入口。
