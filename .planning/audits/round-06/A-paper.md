# 审查报告 A：原文一致性（paper consistency）— round-06

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-06 |
| **审查时间** | 2026-09-21 01:50–03:10（UTC+8） |
| **声明冻结 hash** | `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（59 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **HASH_MATCH。** 按 `VERSION.md` 原文 Python 逐字复算：文件数 **59**，摘要 `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`。相对 r05 新增 `tests/test_round05_regressions.py`。审查对象即该冻结工作树。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `39CF907C0B66B9B26AE7355E394848CFA1FF41CE5166310E1DC0A9307F9AC498`（与账本 **§0** 及 TR-0322 行内 hash **一致**；相对 r05 的 `E481EB84…` 已因 QA-01 措辞重算） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-06/{B,C,D,E,F}-*.md`。**未把** `ISSUES.md` 作者关闭当作关闭。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |

**总判：不通过。** 冻结 hash 可核验。相对 r05，下列猎点经本轮独立复跑后**不得原样重开**：scientific 轨迹不再是 `p1 = 4 | p2 = 0 | q = 0` 且不再零事件；无事件时 $H$ 不再冒称 `pre_step`；几何-only `timing` 不写 `pre_step`；verbalizer 不再用子串；P1 bootstrap 重算 $\Delta\mathrm{AUC}$；dummy execute 无 hidden 不得 `refilled_prefix=True`；跨界 span 无回退；Prefill 有 `prefill_hidden`。

本轮仍 FAIL，因为 scientific 的“事件”不是论文 §4.1 的生成步骤：题干前提赋值被当成 $s_i$，目标行是 teacher-force `\nq = ` 再采两位数，不是自然 CoT 解析。由此 $R_{\mathrm{behavior}}$ 把提示词改写记成行为响应；2/3 的步前 $H$ 为 NaN 仍标 `pre_step`；scientific `fit` 因 NaN 无法落盘。假说不要求正结果——本通道不因 P1–P3 无正数判缺陷。Gate 0–2 保持 `unregistered`，**不是缺陷**。

---

## 0. 相对上一轮树的诚实变化（避免把已修项当新缺陷）

独立重读当前字节并复跑后，下列 **不再** 作为本轮 confirmed defect 原样重开（不等于科学语义已齐）：

| 先前问题（r05） | 当前树（本轮复跑） |
|---|---|
| scientific generate 零事件 | 6 条轨迹各 3 个事件（`p1`,`p2`,`q`），`parse_status=ok`。无事件则 prepare 拒。**不得**按“零事件”重开。事件来源见 A6-01。 |
| 末 token 自称 `pre_step` | 无事件：`h_position=no_event`，$H=(0,d)$。有事件：按事件堆叠，行数=事件数（18=18）。**不得**按“末 token 冒称步前”重开。步前不可表达时写 NaN，见 A6-02。 |
| 子串 verbalizer | `17`/`70`/`boxed{8} also 7` 对金标 `7` 均为 score=0。无生成器 → `generate_unavailable`。 |
| 常数 bootstrap | `_bootstrap_p1` 对问题组重采样并重算 `_p1_delta_only`。构造 40 点：`status=resampled_delta_auc`，区间宽度 0.78，不是 `[δ,δ]`。 |
| dummy execute → `refilled_prefix=True` | 仅 `generated_ids`、无 hidden → `refilled_prefix=False`，`status=prefill_unavailable`。 |
| span 跨界回退 | `[1,3)` 对 `[[0,2],[2,6]]` → `[]`。重叠非全含 → `[]`。 |
| 几何行写 `timing=pre_step` | 可区分有限 $H$：`timing=offline_hidden`。scientific 因 NaN 行 allclose → `unexpressible`，仍不是 `pre_step`。 |
| Prefill 无证据 | `execute_repair_tiny` 返回 32 维 `prefill_hidden`，`refilled_prefix=True`。offline 诚实 `False`。 |
| REQUIREMENTS 行内 hash `E481EB84…` | 现为 `39CF907C…`，与 §0 一致。 |
| S3 静默截断 | 同 $n$、异维：`a_map=pca`，`truncated=False`，`status=adapted_geometry`。 |
| 账本用 pytest 关闭**可执行行** | 159 条 `executable_function` 的 `local_verify_status` 均为 `tests_exist_not_acceptance`；可执行行 `passed_local_tests=0`。关闭方法已改，不得按 A5-02 原文重开。过称 `implemented_local` 见 A6-03。 |

---

## 1. 逐文件覆盖

每行：路径（磁盘 `splitlines()` 行数）— 对照条款 — 结论。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 1–517 | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 1–86 | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。Gate 保持 null 与代码一致。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 1–166；§5 = 73–91 | GOAL §5.1–5.15 | 第 2、3、6–8、10–13 条在科学入口仍被降级或替身。第 14、15 条持守。 |
| `.planning/REQUIREMENTS.md` | 1–76 | DATA/MEAS/MODEL/PROBE/… 与 atomics | 复选框全空；状态表仍写 `implemented_local`。行内 hash 已与 §0 对齐。 |
| `.planning/PAPER_TRACEABILITY.md` | 1–44 约定；75–120、202–243、370–420 抽样 | 账本不得当实现证据 | 528 行。可执行行验证列已改为 `tests_exist_not_acceptance`。157/159 可执行行仍 `implemented_local`。协议/标题行仍大量 `pytest -q` + `passed_local_tests`。 |
| `pyproject.toml` | 1–27 | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 有 `torch`/`transformers`。无强制 scientific 栈。 |
| `src/reasoning_diff/__init__.py` | 1–5 | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 1–4 | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 1–385 | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 1–46 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先与相交掩码正确。默认 cone 走任务祖先，不是行为头 $\hat R^{\mathrm{val}}$。 |
| `src/reasoning_diff/events.py` | 1–261 | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 对齐 | `parse_events` 把**前提赋值**和节点一起当事件；行起点对齐使同题 `p1`/`p2` 共享 `start=0`。`extract_answer` 认 boxed/`####`/末数。策略仍只读 `status=="strategy_change"`。 |
| `src/reasoning_diff/edits.py` | 1–277 | §7 T1 重算；GOAL §5.2 | 值编辑+表达式重算正确。`make_source_value_pair` 有同值异源。 |
| `src/reasoning_diff/measure.py` | 1–342 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集、空分母、缺/空 sham→null、signed excess、逐步平均正确。`event_density_sets` 算出 sham `hits` 后丢弃，观测到 sham 时 `noise_set=[]` 且 `evaluated=True` → 噪声记 0。 |
| `src/reasoning_diff/analysis.py` | 1–337 | §2.6 P1–P3；§7 分流；附录 S2–S4 | P1 留出 logistic + 偏相关。bootstrap **重算** $\Delta\mathrm{AUC}$。`retrieval_scatter` 无嵌入则 BOW。 |
| `src/reasoning_diff/interventions.py` | 1–115 | §2.4 交换/对照/INLP/救援/$\mathrm{IE}_Z$ | 交换式、范数匹配、`ie_z`、`select_weak_layer` 库层正确。CLI 几何行不写 `pre_step`。四项结局在几何路径仍为 `None`。 |
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、`fit` 形式正确。CLI tiny 维 32 故 `rank=min(64,d)`。 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | §4.2 Hidden=256 ReLU | 架构+`fit` 符合。CLI 用全 1 标签、无负例。 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | §2.5 命题 2 | 分位数与 $+\infty$ 正确。`truth_indices` 可限制到 $R(s_i)$。 |
| `src/reasoning_diff/probes/__init__.py` | 1–3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 1–125 | §8 文本/注意力/四档自述；GOAL §5.7 | 监督 BOW。verbalizer 走 `extract_answer`，不再子串。CLI `generate_fn` 回显前缀。 |
| `src/reasoning_diff/transfer.py` | 1–75 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。`common_dim_then_procrustes` 先 PCA 再 Procrustes。 |
| `src/reasoning_diff/repair.py` | 1–217 | §3 Repairability/RR；§9 嫁接；GOAL §5.13 | `execute_repair_tiny` 真 Prefill+hidden。无 hidden 的 execute 被拒。掩码仍改前缀字符串。 |
| `src/reasoning_diff/cli.py` | 1–1052 | §4 流水线；§8.2 scientific | scientific prepare 拒零事件。collect 拒 offline $H$。fit 对齐事件键，但 scientific $H$ 含 NaN 则无法写 JSON。intervene 几何 timing 保持 `offline_hidden`。 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | §8.1 模型卡/revision | 两张冻结卡 + `local_files_only=True`。CLI 不加载。无权重时属 pending_server。 |
| `src/reasoning_diff/models/collect.py` | 1–192 | §4.2 $h_i/e_j$；GOAL §5.6/5.10 | 按事件取三时机；无事件不写 `pre_step`。不可表达位置填 NaN。`intervene_swap_decode` 的 `followed_donor` 仍是 ids 是否变化。 |
| `src/reasoning_diff/models/features.py` | 1–39 | §2.4 三时机；GOAL §5.6 | 跨界 token 排除正确。 |
| `src/reasoning_diff/models/generate.py` | 1–191 | §8.2 自然轨迹 | 显式 decode 后 **teacher-force** `\n{target} = ` 再采两位数字。注释写明 Not gold values。 |
| `src/reasoning_diff/models/tiny.py` | 1–120 | 本机 hook 边界 | 随机 Qwen2/3 + resid_post。不是论文模型路径。 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | §4.2 层带 / span | `readout_layer_index`：3→1，32→21，36→24；空带拒绝。span 只收全含 token。1 字符 = 1 token。 |
| `src/reasoning_diff/models/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | §7 适配入口 | 快照分发。CLI 默认 `t1_fixture`。不生成 500 题。 |
| `src/reasoning_diff/tasks/t1_official.py` | 1–92 | §7 T1；template≠G | 快照加载拒绝裸 `G`、排除共享 RNG、默认 mod 23。`load_igsm_directory` 存在。CLI 默认不走。 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | 官方/夹具分离 | 拒绝非 `fixture`。成立。 |
| `src/reasoning_diff/tasks/t1_config.py` | 1–21 | op∈{5,10,15,21}，n=500 | 配置校验。`--t1-ops` 只校验，不生成任务单。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–84 | §7 T2；GOAL §5.2 | 无侧车：placeholder + `graph_status=unknown`，拒编辑。有侧车：值编辑+算子逆转。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–81 | §7 T2；评测专用 | test-only 锁正确。孤立数字替换成立；答案 `needs_truth`/`None`。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 1–100 | §7 T2-noop | 可造配对与分层元数据。无注入句值扰动扫描。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 1–104 | §7 T3；supporting_facts≠DAG | 标记正确。无独立新答案则 `needs_truth`。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 1–110 | §7 T3 组成引用 | 保留 answerable/unanswerable。`expression="composition_reference"` 不可重算。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–78 | §7 HumanEval-Perturb；GOAL §5.15 | `edit_kind=input_list` 有旗。无新解则 `needs_truth`。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 1–51 | §7 T4；Fig.6 | 四类状态强制区分。前提=placeholder。`apply_t4_question_edit` 为 `needs_truth`。无相图。 |
| `src/reasoning_diff/tasks/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/executor.py` | 1–109 | GOAL §5.15 | 禁止宿主 exec。默认 `UnavailableExecutor`。`ChildProcessExecutor.isolated_sandbox=False`。 |
| `src/reasoning_diff/scoring.py` | 1–30 | §3 域内评分 | 数值/QA 精确匹配。代码经执行器接口。 |
| `src/reasoning_diff/splits.py` | 1–111 | §4.1 共组；GSM-Plus test-only | 六角色 + 家族共组。默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 1–53 | GOAL §5.4 | sample/direction/perturb/bootstrap/split 分离。 |
| `src/reasoning_diff/io.py` | 1–133 | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 1–11 | — | 夹具路径。 |
| `tests/test_cli_pipeline.py` | 1–30 | §4 流水线 | 八阶段 exit 0；**仍强制** `--backend offline`。 |
| `tests/test_science.py` | 1–101 | 校准/迁移/交换/Week-8 | 库函数微例。 |
| `tests/test_measure.py` | 1–40 | $S/M$、联合编辑反例 | 与公式一致。 |
| `tests/test_review_regressions.py` | 1–397 | 上轮回归 | 锁住若干库修补。 |
| `tests/test_round03_regressions.py` | 1–291 | r03 回归 | 仍锁 `precomputed_scores`。 |
| `tests/test_round04_regressions.py` | 1–311 | r04 猎点 | 锁 generate≠节点真值、span $E$、几何≠`pre_step`、Prefill。 |
| `tests/test_round05_regressions.py` | 1–190 | r05 猎点 | 锁事件非空、H 行数=事件数、抽取答案、重采样键、dummy 非 Prefill。**不**锁事件是生成步骤、步前可表达、或 $R_{\mathrm{behavior}}$ 非题干预复述。 |
| `tests/test_tracer_t1_prepare.py` | 1–100 | T1 夹具准备 | 身份/重算/空分母。 |
| `tests/test_t1_official.py` | 1–31 | template≠G | 快照形状。 |
| `tests/test_t2_gsm.py` | 1–33 | T2 | 侧车数值编辑。 |
| `tests/test_t3_t4.py` | 1–44 | T3/T4 | supporting_facts ≠ DAG。 |
| `tests/test_artifacts.py` | 1–73 | I/O | 工程。 |
| `tests/test_generate_loop.py` | 1–17 | 可重放采样 | tiny decode。 |
| `tests/test_tiny_hooks.py` | 1–27 | hook 清理 | 本机接口。 |
| `tests/test_tiny_cache.py` | 1–26 | 缓存隔离 | `intervene_tiny` 断言 logits 因 $\Pi_Z$ 改变。 |

第三方库：审查了本项目对 `numpy` / 可选 `torch`+`transformers` 的使用假设，未审查依赖源码。

夹具抽读：`tests/fixtures/t1_tiny.json`（全文）、`t2_gsmplus_one.json`、`t2_symbolic_one.json`、`t4_boundary.json`。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献清单 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。Gate 保持 null（非缺陷）。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 2、3、6–8、10–13 条在科学入口仍被降级或替身。 |
| C4 | 阅读 `PAPER_TRACEABILITY.md` 约定，抽样 TR-0001–0043、TR-0125–0137、TR-0158–0166、TR-0293–0346、TR-0400 | 可执行行不再用 pytest 关闭；仍大量 `implemented_local`。TR-0125 现指向 generate/parse，状态 `partial_local_scientific`。TR-0158/0400 仍指向 `intervention_report`。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。 |
| C6 | 对照公式手核 + 复跑：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1、cone | $R_{\mathrm{task}}$/差集/交换/分位数/拒维度：**库函数层符合**。P1 bootstrap：**重算 $\Delta\mathrm{AUC}$**。噪声：观测 sham 后仍记 noise=0。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | scientific 调用 generate + 拒零事件。事件来自题干赋值 + teacher-force 目标行，不是自然步骤解析。 |
| C8 | 对照 §4.2 / §8 探针与基线 | tiny $E$ 行不同、`hidden_layer=1`。scientific $H$ 行数=事件数，但 12/18 行 NaN。CLI verbalizer 回显前缀。 |
| C9 | 对照 §2.4 / §6 干预 | 几何-only 写 `offline_hidden`。scientific tiny：$H$ 前两行 NaN → `donor_missing`/`unexpressible`。四项几何结局 `None`。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 | T1 值编辑成立。Plus 孤立数字替换成立、无新 oracle。无侧车 Symbolic 拒编辑。T3/T4 常 `needs_truth`。 |
| C11 | 对照附录 S1–S4、C4 掩码、$k\in\{1..5\}$、失效相图 | S3 PCA 接通。S4 仍 BOW。scientific repair $k=1..5$ 且 Prefill；$k\ge3$ 槽位不再增长。无相图。 |
| C12 | 抽读测试是否固化替身 | 是：`test_scientific_prepare_emits_parseable_events` 只要求事件非空与含 `q`；`test_scientific_collect_h_is_step_boundary_*` 只比行数；`test_intervene_tiny_geometry_timing_stays_offline` 在 `donor_missing` 下也因 `timing≠pre_step` 通过。 |
| C13 | 独立重算论文/协议/GOAL/REQUIREMENTS SHA-256 | 四份与账本 §0 一致。 |
| C14 | 独立重算声明代码冻结 hash | **HASH_MATCH** `dc2ba459…`，59 文件。 |
| C15 | 复跑 CLI prepare/collect/fit/calibrate/intervene/repair/analyze 与库函数微例 | 见各 finding 的 Repro。命令已在本审查重跑，不是转述。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 全量 `pytest -q` 作为本通道验收 | 原文符合性不由绿测关闭。作者声称 136 passed；本报告不声称测试通过。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量 500 题 | 协议 §7：科学结论 `pending_server`。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | scientific $H$ 含 NaN，fit 无法落盘；即使可拟合，标签也不是生成步骤上的 $R_{\mathrm{behavior}}$。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读 round-06 B–F。 |
| N6 | `PAPER_TRACEABILITY.md` 全部 528 行逐字复读 | 已读约定与高风险可执行/GOAL/REQUIREMENTS 行。剩余多为同一模板重复。 |
| N7 | 真实隔离沙箱跑 HumanEval | 无合格隔离后端；`ChildProcessExecutor` 不能冒称沙箱。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | generate/span/Prefill/事件接口在；事件不是生成步骤 | subst |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 1 | 34–35 | 检索余弦 vs 答案变 | exec | `retrieval_scatter` 无嵌入 → BOW | subst |
| 论文 1 | 38 | 修复解码/Prefill/耗时 | exec | tiny 有 generated/prefill/hidden；不是槽位成本 | ok-lib / subst |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema 正确；scientific 把 $P$ 的题干赋值当成 $s_i$ | subst |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | 字段在；值变化来自提示词改写，不是生成步响应 | subst |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | id + aliases 词边界 | ok-lib |
| 论文 2.3 | 88 | 消失/合并/策略分岔 | proto | `removed`/`merged` 有；策略 `status_field_only`/`scanned=False` | stub |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap`；$\Pi=I$ 时得 donor | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ | math | `ie_z` 为向量均值差，不是预指定 $g$ | ok-lib / subst |
| 论文 2.4 | 106–108 | 前瞻 hook/KV/前缀 | exec | tiny $\Pi_Z$ + decode；scientific 因 NaN $H$ 未进入 hook | subst |
| 论文 2.4 | 110 | 步前/数值前/步尾 | exec | 三阵写入；步前不可表达填 NaN 且总标 `pre_step` | subst |
| 论文 2.4 | 114–117 | C-rand / C-layer 同幅度四项 | exec | 范数匹配在；无 dev 曲线诚实 `dev_scores_missing`；四项 `None` | stub / ok |
| 论文 2.5 | 121–125 | cone / Oracle / 行为掩码 | math | `dirty_cone`/`oracle_mask`/`behavior_mask` | ok-lib |
| 论文 2.5 | 127–130 | 命题 1 + REST-03 | math | $xy$ 反例夹具 | ok-lib |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | 分位数 ok；CLI 尝试按行 $R(s_i)$；scientific 无探针权重则拒 | ok-lib |
| 论文 2.5 | 141–142 | 原轨迹槽位、禁重拓扑 | exec | Prefill 整段前缀字符串，不复用槽位 | subst |
| 论文 2.6 | 148–156 | $S,M,\rho$，空分母 N/A | math | `dependency_densities` + event mean | ok-lib |
| 论文 2.6 | 158 | 噪声先扣除 | proto | sham 轨迹真不同；密度把观测到的 sham 写成 noise=0 | subst |
| 论文 2.6 | 164 | P1 logistic + 偏相关 + bootstrap | math | 留出 IRLS + 偏相关；bootstrap **重算** $\Delta\mathrm{AUC}$ | ok-lib |
| 论文 2.6 | 165 | P2 配对 + 污染位置 | exec | 库函数收 `contamination_positions`；无表则 CLI `None` | ok-lib |
| 论文 2.6 | 166 | P3 Δacc + 对照 + 非目标 | exec | 库函数收 nontarget；CLI 无表则 `None` | ok-lib |
| 论文 2.6 | 168 | REST-02 | proto | `causal_reverse_claim=False` | ok |
| 论文 3 | 176–186 | TO/CSP/覆盖/脏变/P/R/F1 | math | 公式在；CLI analyze 在有 features 时走 `predict_matrix` | ok-lib |
| 论文 3 | 188 | TO/CSP 噪声参照 | proto | `to_noise`/`csp_noise` 有数；密度噪声仍被写成 0 | subst |
| 论文 3 | 190 | 干预三项并列、前瞻/回溯分列 | proto | 范数三列有；结局硬编码 None | stub |
| 论文 3 | 194–200 | Repairability、RR、成本分列 | math | 两公式有；scientific 有 token/hidden；非槽位预算 | stub |
| 论文 4.1 | 232–253 | 双标签流水线；NL 单调对齐；共组 | exec | generate+拒空事件在；解析对象是题干+强制目标行 | subst |
| 论文 4.2 | 257–267 | MLP、双头、池化 $e_j$、60–75% 层 | exec | 层/池化在 tiny 接通；步前 $h_i$ 大量 NaN；MLP 全正例 | subst |
| 论文 5 Fig.1–2 | 291–299 | 热力图、三时机、跨模型迁移入口 | exec | 无导出；analyze 只报 4096/3584 N/A | missing |
| 论文 6 | 301–313 | 解耦资产、前瞻交换、INLP、救援 | exec | 配对构造器在；scientific 干预未执行交换 | stub |
| 论文 7 | 315–329 | P1–P3 测量入口（不要求正结果） | exec | 库入口在；默认 CLI `p1=None`（标签不足 4 条已知类） | stub |
| 论文 8 | 331–341 | 注意力/四档 verbalizer/监督文本 | exec | 库层抽答案；CLI 回显前缀当“生成” | subst |
| 论文 9 / Table 1 | 343–355 | 五条主对照 + 三条附录掩码实跑 | exec | 掩码改前缀字符串；decode 相同预算 | stub |
| 论文 Fig.6 | 353 | 失效相图五类 | exec | T4 状态枚举 ≠ 相图 | missing |
| 附录 S1 | 357–359 | $k\in\{1..5\}$ 连续编辑 | exec | 循环在；槽位不超事件名列表 | stub |
| 附录 S2 | 361–367 | 两参数锥拟合 | math | `cone_fit` 拟合；CLI 需 `cone_table.jsonl` | ok-lib |
| 附录 S3 | 371–373 | 共同维 + Procrustes | exec | PCA 后 Procrustes；同 $n$ 可对齐 | ok-lib |
| 附录 S4 | 375–377 | 嵌入余弦散点 | exec | BOW 点积，不是文本嵌入模型 | subst |
| 论文 7 数据 | 399–409 | T1–T4 假设专用资产 | exec | 读取器+部分 apply*；真值常 `needs_truth` | stub |
| 论文 8.2 | 419–431 | `--eval-mode scientific` | exec | 开关调用 generate 并拒空事件；后续标签/$H$ 不是论文对象 | subst |
| 论文 9 | 435–445 | 第一周三轨迹/50 干预冒烟 | exec | 三轨迹入口在；50 条解耦干预无 | stub |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |

---

## 5. Findings

### A6-01 — scientific 已有可解析事件，但事件是题干预复述 + teacher-force 目标行，不是 §4.1 生成步骤

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/generate.py` `append_target_assignment` 72–98、`generate_task_trace` 135–149；`events.py` `parse_events` 75–89；`cli.py` `cmd_prepare` 287–292 |
| **Trigger** | 论文 §4.1 L232–248：`T0=generate` 之后 `parse_events` 的对象是**生成轨迹**上的变量/表达式/版本/作用域。§2.1：$T=(s_1,\ldots,s_n)$ 是模型生成序列的步骤离散化，前提集合是 $P$ 不是 $T$。r05“零事件 / 节点真值拼接”**已满足关闭条件，不得原样重开**。 |
| **Paper requirement** | 自然轨迹步骤事件；$R_{\mathrm{behavior}}$ 来自固定随机流下编辑后**对应步骤值**是否变化；$h_i$ 为这些步骤的步边界。 |
| **Repro / evidence** | 复跑：`prepare --eval-mode scientific` 无 `--split-fractions` → `ValueError`。加上六比例 + `--sham-opportunities 1` → exit 0，**6** 条轨迹，全部 `model=tiny-qwen2`，`generation=decode_loop`。文本例：`'p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82'`。**不是** `p1 = 4 \| p2 = 0 \| q = 0`。各迹 `n_events=3`，`node_ids=['p1','p2','q']`，`q` 值为 82/53（模型采样数字，不是金标 0）。`p1`/`p2` 的 span 同为 `start=0,end=44`（整行题干+乱码），`pre_step` 不可表达。观测：改 `p2` 时 `event_pair=['p2','p2']` 为 `changed` `0→2`（提示词被改），`['q','q']` 为 `no_change` `82→82`。标签：`(p2,p2)` `behavior=1` 且 `task_label=None`；`(q,p2)` `task_label=1` 且 `behavior_label=None`。 |
| **Impact** | C1/C3 的可执行入口仍没有“生成步骤上的编辑响应”。账本 TR-0125 现指向 generate/parse，比 r05 诚实，但仍把该替身标成可执行覆盖。`test_scientific_prepare_emits_parseable_events` 只锁“有事件且含 q”。 |
| **Suggested fix** | 只把 decode 段（或官方 CoT）解析为事件；题干前提留在 $P$。无生成步骤时拒绝 scientific 的 label/collect，或标 `parse_failed`/`unimplemented`。不要 teacher-force 赋值行来凑事件。 |
| **Status** | **confirmed defect**；真实 CoT 质量 **pending_server** |

### A6-02 — $H$ 行数等于事件数且自称 `pre_step`，但多数步前行是 NaN；scientific fit 无法落盘

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/collect.py` `collect_hidden_trace` 55–66；`cli.py` `cmd_collect` 449–450、`cmd_fit` 534–609 |
| **Trigger** | 论文 §4.2 L261–262：$h_i$ 是第 $i$ 步边界 token 隐状态。GOAL §5.6：步前特征必须可表达且不含目标。r05“末 token 自称 pre_step”**不得重开**（无事件现为 `no_event`）。 |
| **Paper requirement** | 每个生成步骤一条可表达的步前/数值前/步尾 $H$。不可表达应拒绝或标 `unexpressible`，不得当作已测步前矩阵。 |
| **Repro / evidence** | scientific tiny collect：$H=(18,32)$，$n_{\mathrm{events}}=18$，`H_EQUALS_EVENTS=True`，`hidden_layer=1`，$E$ 行不同。库层 `h_position=pre_step`。`H`/`H_pre_step` 的 NaN 比例 **2/3**；有限行 6（仅各迹的 `q`）。`p1`/`p2`：`pre_idx=None`，`expressible=False`。scientific `fit` → `ValueError: Out of range float values are not JSON compliant`。scientific `calibrate` → `probe_weights_or_features_missing` 后拒绝 loss/字面分数（卫兵成立）。 |
| **Impact** | 步前探针入口在本机 scientific 路径上不可训练。测试只断言行数，不断言有限/可表达。 |
| **Suggested fix** | 不可表达的步前行不要写入 $H$ 或不要标 `pre_step`。scientific collect 在有限步前行数 < 事件数时拒绝。 |
| **Status** | **confirmed defect** |

### A6-03 — 账本可执行行不再用 pytest 关闭，但仍把替身标成 `implemented_local`

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` TR-0158、TR-0308、TR-0316、TR-0319、TR-0322、TR-0346、TR-0400；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：未实现不得标已实现。r05 猎点是 **pytest 关闭可执行行**；本轮 159 条可执行行 `local_verify_status=tests_exist_not_acceptance`，**不得**按 A5-02 原文重开。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。 |
| **Repro / evidence** | 528 行：`implemented_local=477`。可执行 159 条中 157 条仍 `implemented_local`，仅 TR-0125/0135 为 `partial_*`。TR-0158 / TR-0400（解耦任务构造）仍指向 `intervention_report`。TR-0308（完整域适配+更新真值）仍 `implemented_local`。协议/标题行仍约 78 处 `python -m pytest -q` 且 `passed_local_tests`。REQUIREMENTS 复选框全空，状态表写 `implemented_local`。 |
| **Impact** | 覆盖率仍被制成 16/16。独立审查若信 `implemented_local` 会漏检 A6-01。 |
| **Suggested fix** | 未接到论文语义的可执行行改为 `unimplemented` / `ok-lib_unwired` / 保持 `partial_*`。验证列写对照原文的复跑产物。 |
| **Status** | **confirmed defect**（过称）；pytest-关闭可执行行 **本轮不重开** |

### A6-04 — 噪声参照在“已评估 sham”时被写成 0（不要求正结果）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `measure.py` `event_density_sets` 289–309 |
| **Trigger** | 论文 2.6 L158；协议 §2.6–§5：同题不同随机流必须先扣除。r05 因零事件得到 `noise_set_empty`，不得把“无噪声键”原样重开。 |
| **Paper requirement** | 噪声集合来自匹配比较机会上的实际变化；不得把已评估的空变化与“没把 hits 写进集合”混成 noise=0。 |
| **Repro / evidence** | scientific 标签：`q` 的 `noise_ref=1.0`（82 vs 53）。`event_density_sets` 算出 `hits` 后不用，`observed=True` 时 `noise_set=[]` 且 `noise_evaluated=True`。密度：`rho_S_noise=0.0`，`rho_S_excess=0.5`。`to_csp.to_noise=0.84` 说明 sham 轨迹确实不同。 |
| **Impact** | Week-8 若读到 excess=0.5，会把题干预复述密度当成已扣除噪声的量。本机 analyze 因标签不足未走 P1，`status=not_evaluated`（尚未把该数写成科学结论）。 |
| **Suggested fix** | 把 sham 变化前提写入 `noise_set`；无变化且已评估才是 noise=0。 |
| **Status** | **confirmed defect** |

### A6-05 — GSM-Plus / 无侧车 T2 / T4 没有“合法编辑 + 更新真值”

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t2_gsm_plus.py` `apply_plus_numeric_edit` 50–76；`t2_gsm_symbolic.py` 43–44, 68–70；`t4_boundary.py` 26, 36–50；`t3_humaneval.py` 34–74 |
| **Trigger** | 论文 §7 L403–407；GOAL §5.2；DATA-02。Plus 孤立数字替换**本轮成立**（`13` 保留，`3→9`），不得按“无 apply*”或“13 被改成 19”重开。 |
| **Paper requirement** | 各域：读取、合法编辑、**更新后真值**、事件/独立标注、域内评分。缺失标注保持 unknown，不得凭空生成。 |
| **Repro / evidence** | Plus：`validity=needs_truth`，`answer_spec.value=None`。Symbolic 无侧车：`graph_status=unknown`，`kind=placeholder`。T4：四状态齐全，前提 placeholder，`apply_t4_question_edit` → `needs_truth`。HumanEval 无新解 → `needs_truth`。Hotpot 给口头新答案仍 `needs_truth`（此项诚实）。 |
| **Impact** | 除 T1 值编辑与 T2 侧车外，行为扫描没有更新后的 $v$。 |
| **Suggested fix** | 每域提供编辑+新 oracle；缺失保持 `unknown`/`needs_truth`，不要把读取器标成域适配完成。 |
| **Status** | **confirmed defect**（更新真值）；孤立 Plus 编辑本身非缺陷 |

### A6-06 — 附录 S4 与 Table 1 没有按论文口径的测量入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `retrieval_scatter` 300–305；`repair.py` `mask_prefix` 47–70；CLI analyze 919–923 |
| **Trigger** | 论文附录 S1–S4；S4“不得因精简而删除”。S3 PCA 与 S1 $k$ 循环、Prefill **不得**按 r05“截断/无循环/无 Prefill”重开。 |
| **Paper requirement** | $k\in\{1..5\}$ 连续编辑并 Prefill 保留文本；先共同维映射再 Procrustes；$(P,P\oplus\Delta P)$ **文本嵌入**余弦 vs 答案是否改变；八条掩码按槽位实跑。 |
| **Repro / evidence** | `retrieval_scatter(texts_a=…)` → `embedding_kind=bow_descriptive_not_paper_embed`。同 $n$ S3：`truncated=False`，`adapted_geometry`。scientific repair：$k=1..5$，`refilled_prefix=True`，`prefill_hidden` 长 32；`k=4,5` 的 `slots` 与 $k=3$ 相同。Table 1 掩码只改前缀字符串。 |
| **Impact** | S4/Table 1 没有从入口到图的论文口径路径。 |
| **Suggested fix** | S4 用声明的嵌入；掩码按槽位执行；无资产保持 `not_evaluated`。 |
| **Status** | **confirmed defect**（S4/掩码语义）；S2 库函数、S3 PCA、S1 循环/Prefill 本身非本条猎点缺陷 |

### A6-07 — CLI 四档 verbalizer / BoundaryMLP / 注意力仍是替身（子串已关）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_fit` 592–608；`baselines.py` 92–125；`probes/boundary.py` |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7。子串打分 **本轮不再成立**（独立复跑 17/70/boxed）。 |
| **Paper requirement** | 四档自述；监督档与探针同样本/划分/可见前缀。2 层 MLP 边界检测（token 级正负例）。注意力阈值在 dev 上选定。 |
| **Repro / evidence** | 库：`verbalizer(..., generate_fn=λ:"17")` 对金标 `7` 得 0；`70` 得 0；`\boxed{8} also 7` 得 0（抽出 8）。CLI `generate_fn` 为 `lambda p, t=prefix: t`（回显前缀）。夹具 fit：zeroshot/fiveshot/reflection `score=1.0`，`extracted='0'`（题干末数）。supervised 拒未训练。BoundaryMLP：`y_b = ones`，`note=event-rows-only_no_negatives`。attention_mean 对空权重得 0；threshold 用两只手写点。 |
| **Impact** | 第 8 节“说不出来”在 CLI 上仍不是同划分模型自述。 |
| **Suggested fix** | CLI 按同一划分调用真实生成与 token 级 MLP；未接线不得标 `implemented_local`。 |
| **Status** | **confirmed defect**（CLI 替身）；子串打分 **本轮不重开** |

### A6-08 — 干预四项结局仍为 None；scientific 路径因 NaN $H$ 未交换

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_intervene` 707–786；`models/collect.py` `intervene_swap_decode` 186 |
| **Trigger** | 论文 2.4 L106–117；§6 L305–313；GOAL §5.10–5.11。猎点“几何-only 不得写 `pre_step`”**已满足**（手造有限 $H$：`timing=offline_hidden`）。 |
| **Paper requirement** | 目标步首 token 前交换 residual；评价新生成 $s_k$ 是否跟随 donor。报告四项结局相对对照的差值。 |
| **Repro / evidence** | `apply_swap`：$H^b=[1,0]$，$H^d=[0,1]$，$\Pi=I$ → `[0,1]`。scientific tiny intervene：`status=donor_missing`，`timing=unexpressible`（$H[0]$ 与 $H[1]$ 皆 NaN，`allclose(..., equal_nan=True)`）。手造 2×8 有限 $H$ + offline：`geometry_on_hidden` / `offline_hidden`，`target/nontarget/task_correct/invalid=None`。`followed_donor` 定义为 generated_ids 是否变化。 |
| **Impact** | C2 主张入口仍不是“来源跟随”。几何不再冒称 `pre_step`。 |
| **Suggested fix** | 在对齐的 $s_k$ 首 token 前 hook；按预注册矩阵评分；无 donor 保持 `unexpressible`。 |
| **Status** | **confirmed defect**（结局/对齐）；几何 timing 猎点 **本轮不重开** |

### A6-09 — 修复已 Prefill/decode，但不是原槽位嫁接

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `repair.py` `mask_prefix` 47–70；`execute_repair_tiny` 73–121；`cli.py` 811–841 |
| **Trigger** | 论文 §3 L194–200、§9 L347–355、附录 S1；GOAL §5.13。猎点“必须 Prefill/decode 或诚实 `refilled_prefix=False`”**已满足**（本机：`prefill_hidden` 32 维；dummy 无 hidden → False）。 |
| **Paper requirement** | 干净文本在当前前缀重新 Prefill，**受损槽位**自回归重算。主文 5 条 + 附录 3 条实跑。同原始 token 预算。 |
| **Repro / evidence** | scientific repair：5 条记录，$k=1..5$，`generated_tokens=8`，`extra_prefill_tokens=32`，`refilled_prefix=True`。`k=1` slots=`[p1]`，$k=2`=`[p1,p2]`，$k\ge3`=`[p1,p2,q]`。offline：`refilled_prefix=False`。`mask_prefix` 只改字符串。 |
| **Impact** | Repairability/RR/同预算曲线无法按槽位测量。 |
| **Suggested fix** | 按掩码在原轨迹槽位重算；无槽位资产不得标 Table 1 已跑。 |
| **Status** | **confirmed defect**（槽位语义）；Prefill 接口本身非本条猎点缺陷 |

### A6-10 — 自然语言事件对齐与官方 CoT 解析缺失

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `events.py` `parse_events` 75–89；`align_events_monotonic` 197–217 |
| **Trigger** | 论文 4.1 L250–252；2.3 L87–88。单调对齐函数存在；夹具 `alias = NUMBER` 存在。不得说“无解析/无单调函数”。 |
| **Paper requirement** | 结构化：变量/表达式/版本/作用域。NL：抽实体后允许跳过与合并的单调序列对齐。消失/合并/策略分岔单独计数。 |
| **Repro / evidence** | 题干 `p1 = 4` / `p2 = 0` 被收成事件。`q = p1 * p2` 因不是数字而不匹配，改由 teacher-force `\nq = 82` 补上。无 iGSM 官方 CoT 解析。`strategy_changed` 仅 `status=="strategy_change"`；夹具解析只写 `ok`/`ambiguous`。`scanned=False`（诚实）。 |
| **Impact** | T2/T3 没有事件层；scientific T1 的“事件”也不是生成 CoT。 |
| **Suggested fix** | 分域解析器只吃生成段 + NL 单调对齐；未对齐进单独计数。 |
| **Status** | **confirmed defect** |

### A6-11 — T1 500 题 / 四档 op 没有 CLI 默认入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t1_config.py` 9–21；`cli.cmd_prepare` 默认 `t1_fixture`；`--t1-ops` 282–285 |
| **Trigger** | 论文 §7 L403、§9 L437；WEEK1-01。三轨迹 **scientific 已产**，不得按“无三轨迹”重开。 |
| **Paper requirement** | iGSM `op∈{5,10,15,21}`、500 题；$T_0(seed=0)$、$T'_0(seed=1)$、$T_{\mathrm{pert}}(seed=0)$。 |
| **Repro / evidence** | 配置校验存在。`--t1-ops` 只 `validate_t1_prepare_config`，仍一条夹具题。全量 500 属 pending_server；**任务单/四档 op 入口本身**仍是代码缺口。 |
| **Suggested fix** | 配置驱动的任务单；CLI 消费快照目录。 |
| **Status** | **confirmed defect**（入口）；全量跑数 **pending_server** |

### A6-12 — 默认划分比例未预注册

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

### A6-13 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 215–257；`cli.py` 845–956 |
| **Trigger** | 协议 §6；GOAL §5.14；DECIDE-01。任务：Gate 0–2 未注册 **不是** 缺陷。 |
| **Paper requirement** | 用户未给阈值则不得编造 pass/fail。不得把 fixture 写入科学结论。 |
| **Repro / evidence** | 复跑 analyze（scientific labels）：`gates.*.decision=unregistered`，`threshold=None`，`scientific_conclusion=None`，`p1=p2=p3=None`，`status=not_evaluated`，`skip_p2_p3=True`。`week8_decision({rho_S_excess:0})` → `c3_negative_descriptive`。有阈值无度量 → `threshold_present_measurement_missing`。 |
| **Impact** | 正确持守。假说不要求正结果，本条不升格。 |
| **Suggested fix** | 不要添加阈值。 |
| **Status** | **non-defect** |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5。

1. **Gate 0–2**：无阈值、无 pass/fail（A6-13）。
2. **`scientific_conclusion` 保持 `None`**。
3. **REST-01/02/03** 禁词列表存在；P3 不自动写“只是后果”；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
4. **身份对齐不含值**。
5. **$R_{\mathrm{task}}$ 祖先**、**$S/M$ 空分母→null**、**缺/空 sham→excess null**、**signed excess 不截断**。
6. **有限扫描**：`exhaustive=False` 时 `no_change` 不作已知负。
7. **交换公式** $H^b+\Pi_Z(H^d-H^b)$ 在 $\Pi=I$ 时得 donor。C-rand 拒绝缺主干预范数。几何-only **不**写 `pre_step`。
8. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$。`[0.1,0.2,0.3,0.4], α=0.4` → $q=0.3$；$\alpha=0.1$ → $+\infty$。
9. **4096 vs 3584 直接迁移 N/A**。
10. **官方 iGSM 快照拒裸 `G`、排除共享 RNG、mod 23**；夹具拒绝 `official`。
11. **GSM-Plus 锁定 test**；孤立数字替换不误改 `13`；无侧车 Symbolic 拒编辑。
12. **no-op 派生名** `reasoning_diff_noop`。
13. **Hotpot 声明 supporting_facts 不是完整 DAG**。
14. **宿主 exec 被禁止**；`ChildProcessExecutor` 不冒称沙箱。
15. **INLP 在已投影表示上迭代**（库函数）。
16. **假说不要求正结果**：本通道不因无 F1/AUC 正数判失败。
17. **P1 留出路径为 IRLS logistic**；bootstrap **重算** $\Delta\mathrm{AUC}$。
18. **scientific 调用模型 generate**，不是节点真值轨迹；零事件被拒绝。
19. **tiny $E$ 为读出层 span 均值**，行不相同；scientific 拒 offline $H$。
20. **无事件时 $h_{\mathrm{position}}=\mathrm{no\_event}$**，不写末 token 为 `pre_step`。
21. **repair 无模型时 `refilled_prefix=False`**；dummy execute 无 hidden 不得冒充 Prefill。
22. **verbalizer 抽答案**：`17`/`70`/`boxed` 不再当子串命中。
23. **span 跨界排除**；60–75% 空带拒绝。
24. **S3 先 PCA 再 Procrustes**（同 $n$）。
25. **REQUIREMENTS 行内 hash 与 §0 一致**。
26. **可执行行不再用 pytest 关闭**（`tests_exist_not_acceptance`）。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_full_cli_smoke` | 八阶段返回 0；**offline** $H$；`not_evaluated` | generate、论文步边界 $H/E$、干预生成、槽位嫁接 |
| `test_scientific_prepare_emits_parseable_events` | 每条轨迹 ≥1 事件且含 `q`；无节点真值拼接 | 事件是生成步骤；$R_{\mathrm{behavior}}$ 不是题干预复述 |
| `test_scientific_collect_h_is_step_boundary_not_last_token` | $H$ 行数=事件数 | 步前可表达、有限、对应生成步 |
| `test_span_no_straddle_fallback` | 跨界 → `[]` | $e_j$ 来自真实 tokenizer 边界 |
| `test_verbalizer_uses_extracted_answer_not_substring` | `17`/`70`/`boxed` 不子串命中 | 同划分四档模型自述 |
| `test_dummy_execute_is_not_prefill` | 无 hidden → `refilled_prefix=False` | 槽位嫁接 |
| `test_p1_bootstrap_resamples_delta_auc` | `status=resampled_delta_auc` 且 `lo≤hi` | CLI 用 $\rho_S$ 表计算 P1 |
| `test_intervene_tiny_geometry_timing_stays_offline` | `timing≠pre_step` | 交换已执行、四项结局、对齐 $s_k$ |
| `test_scientific_repair_runs_k_1_to_5` / `test_repair_k_changes_masked_prefix` | $k=1..5$ 且 Prefill | 槽位执行改变 |
| `test_p1_precomputed_is_scores_not_magic` | `rho==length` ⇒ `delta_auc==0` | 论文 logistic 定义 |

---

## 8. 本审查复跑的命令（均可再跑）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → **59** / `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `main(['prepare', …, '--eval-mode','scientific'])` 无 fractions → `ValueError`；有 fractions → 6 条 tiny decode 轨迹，各 3 事件，文本含 teacher-force `\nq = 82`，不是节点真值拼接。
4. `collect --backend tiny` + scientific → $H=(18,32)$ 行数=事件数，NaN 比例 2/3，`h_position=pre_step`，`hidden_layer=1`，$E$ 行不同；scientific offline → 拒绝。
5. scientific `fit` → JSON NaN；夹具 offline fit 两头 loss 同为 `0.05036`，verbalizer 回显前缀得 `extracted=0`。
6. scientific `intervene` → `donor_missing` / `unexpressible`；手造有限 $H$ → `timing=offline_hidden`，四项 `None`。
7. scientific `repair` → $k=1..5$，`refilled_prefix=True`，`prefill_hidden` 存在；offline → `False`；dummy execute → `False`。
8. `analyze` → `p1=p2=p3=None`，`scientific_conclusion=None`，Gate `unregistered`。
9. `verbalizer` 17/70/boxed、`p1_incremental` bootstrap、`span_token_indices`、`apply_swap`、`sequence_score`、`week8_decision`、域加载器：见 §5。

---

## 9. 结论

**冻结 hash：HASH_MATCH** `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（59 文件）。

**原文一致性：不通过（FAIL）。**

r05 猎点中的“有事件 / 非节点真值拼接 / 非末 token 自称 pre_step / 几何不写 pre_step / 非子串 verbalizer / 真 bootstrap / dummy 非 Prefill / span 不跨界回退 / Prefill 有 hidden”，本轮在接口上已接通，不得原样重开。科学入口改在**事件定义**处断开：题干前提被当成步骤，目标行被 teacher-force，于是 $R_{\mathrm{behavior}}$ 与步前 $H$ 都不是论文对象。Gate 0–2 未注册、假说不要求正结果——这两条被遵守。作者关闭与绿测不能关闭本通道。真实权重/官方全量是 `pending_server`，不能解释本机把 $P$ 写成 $T$。

独立复审关闭条件（本通道）：A6-01 与 A6-02 必须在**同一冻结 hash** 上对照原文关闭（scientific 事件来自生成步骤且步前 $H$ 可表达，或诚实拒绝并降级账本）；其余 medium 项至少改为诚实状态或补上测量入口。
