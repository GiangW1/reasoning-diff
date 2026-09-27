# 审查报告 A：原文一致性（paper consistency）— round-07

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-07 |
| **审查时间** | 2026-09-21 02:04–03:20（UTC+8） |
| **声明冻结 hash** | `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（60 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **HASH_MATCH。** 按 `VERSION.md` 原文 Python 逐字复算：文件数 **60**，摘要 `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`。相对 r06 冻结新增 `tests/test_round06_regressions.py`。审查对象即该冻结工作树。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `39CF907C0B66B9B26AE7355E394848CFA1FF41CE5166310E1DC0A9307F9AC498`（与账本 §0 及 TR-0322 行内 hash 一致） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-07/{B,C,D,E,F}-*.md`。**未把** `ISSUES.md` 作者关闭当作关闭。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |
| **独立性** | 本通道在独立上下文中对照原文与当前字节复跑。不继承 r06 措辞为事实；每条猎点均在本轮磁盘上重新取证。作者在 `ISSUES.md` 的“local close”只作对照清单，不作关闭裁定。 |

**总判：不通过。** 冻结 hash 可核验。相对 r06 声明的关闭项，本轮独立复跑后**不得原样重开**：题干 `p1`/`p2` 赋值不再进入 scientific 事件；步前 $H$ 有限且不是末 token / NaN 行冒称 `pre_step`；假说噪声 hits 不再被记成已评估 0；`edits.jsonl` 含 `source_value_pair`；几何 `timing` 仍为 `offline_hidden`；P1 bootstrap 重算 $\Delta\mathrm{AUC}$；Prefill 仍要求有限 hidden。

本轮仍 FAIL，因为 scientific 的“事件”仍不是论文 §4.1 的生成步骤：decode 出乱码后 **teacher-force** `\nq = ` 再采两位数字，`parse_status=constrained_target`。由此 $R_{\mathrm{behavior}}$ 比较的是约束数字，不是自然步值；账本仍把 157/159 条可执行行标成 `implemented_local`，并把 tiny 随机权重写成 MODEL-01。假说不要求正结果——本通道不因 P1–P3 无正数判缺陷。Gate 0–2 保持 `unregistered`，**不是缺陷**。tiny `weight_source=random_init` **不是** MODEL-01。

---

## 0. 相对上一轮树的诚实变化（避免把已修项当新缺陷）

独立重读当前字节并复跑后，下列 **不再** 作为本轮 confirmed defect 原样重开（不等于科学语义已齐）：

| 先前问题（r06 及更早） | 当前树（本轮复跑） |
|---|---|
| scientific 事件是题干预复述 `p1`/`p2` | 6 条轨迹各 **1** 个事件，仅 `q`；`parse_region=generated`；`start=45 ≥ prompt_len=36`。题干 `p1 = 4` / `p2 = 0` **不是**事件。**不得**按“提示词赋值当 $s_i$”重开。事件对象见 A7-01。 |
| $H$ 行自称 `pre_step` 但多数为 NaN | scientific tiny collect：$H=(6,32)$，**全部有限**，`nan_frac=0`；`event_rows` 6 行皆 `q`；`pre_step.token_index=44`（事件 `start=45`），`post_step=50`，不是末 token。scientific `fit` 落盘。**不得**按“NaN 行标 pre_step / fit 无法落盘”重开。 |
| $R_{\mathrm{behavior}}$ 把提示词改写记成行为 | 改 `p2`：`event_pair=['q','q']` 为 `no_change` `82→82`；标签 `(q,p2)` `behavior=None`（非 exhaustive 的无变化不作已知负）。**不得**按“题干预复述当行为”重开。比较对象仍是约束数字，见 A7-01。 |
| sham hits 记成已评估噪声 0 | 本轮 sham `q`：`82→53` `changed`，`premise_id=sham:q`。密度 `null_reason=noise_set_missing`，`rho_S_noise=None`，**不是** 0。手造 `noise_ref=1.0` 同样走 missing。**不得**按“已评估零噪声”重开。 |
| `source_value_pair` 未落盘 | `edits.jsonl` 含 `kind=source_value_pair`，`targets=['q']`。 |
| 几何 `timing=pre_step` | 手造有限 $H$ + offline：`timing=offline_hidden`。scientific tiny：`timing=offline_hidden`，`status=prospective_decode`。 |
| 子串 verbalizer | `17`/`70`/`boxed{8} also 7` 对金标 `7` 均为 score=0。无生成器 → `generate_unavailable`。 |
| 常数 bootstrap / 退化区间 | `_bootstrap_p1`：`status=resampled_delta_auc`，区间 `[0.11, 0.89]`，不是 `[δ,δ]`。 |
| dummy / 仅 prefix_ids 冒充 Prefill | 无 hidden → `refilled_prefix=False`；`prefix_token_ids` → `prefix_ids_without_hidden`。tiny execute 有 32 维有限 `prefill_hidden`。 |
| 跨界 span 回退 | `[1,3)` 对 `[[0,2],[2,6]]` → `[]`。 |
| S3 静默截断 | 同 $n$、异维：`a_map=pca`，`truncated=False`。 |
| 可执行行用 pytest 关闭 | 159 条 `executable_function` 的 `local_verify_status` 均为 `tests_exist_not_acceptance`。过称 `implemented_local` 见 A7-03。 |

---

## 1. 逐文件覆盖

每行：路径（磁盘 `splitlines()` 行数）— 对照条款 — 结论。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 1–517 | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 1–86 | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。Gate 保持 null 与代码一致。tiny ≠ 科学结论。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 1–166；§5 = 73–91 | GOAL §5.1–5.15 | 第 2、3、6–8、10–13 条在科学入口仍被降级或替身。第 14、15 条持守。 |
| `.planning/REQUIREMENTS.md` | 1–76 | DATA/MEAS/MODEL/PROBE/… 与 atomics | 复选框全空；状态表仍写 `implemented_local` / `implemented_local_tiny`。行内 hash 与 §0 对齐。 |
| `.planning/PAPER_TRACEABILITY.md` | 1–46 约定；75–120、202–243、370–420 抽样 | 账本不得当实现证据 | 726 行 / 528 条。可执行行验证列均为 `tests_exist_not_acceptance`。157/159 可执行行仍 `implemented_local`。协议/标题行仍大量 `pytest -q`。 |
| `pyproject.toml` | 1–27 | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 有 `torch`/`transformers`。无强制 scientific 栈。 |
| `src/reasoning_diff/__init__.py` | 1–5 | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 1–4 | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 1–385 | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 1–46 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先与相交掩码正确。默认 cone 走任务祖先，不是行为头 $\hat R^{\mathrm{val}}$。 |
| `src/reasoning_diff/events.py` | 1–260 | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 对齐 | `parse_events` 仍把前提与节点都列成可匹配实体；scientific 调用方只把生成区送入。策略仍只读 `status=="strategy_change"`。 |
| `src/reasoning_diff/edits.py` | 1–277 | §7 T1 重算；GOAL §5.2 | 值编辑+表达式重算正确。`make_source_value_pair` 有同值异源；CLI 已写入 `edits.jsonl`。 |
| `src/reasoning_diff/measure.py` | 1–345 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集、空分母、缺/空 sham→null、signed excess、逐步平均正确。`event_density_sets`：有 `noise_ref=1` 的 hits 时 `noise_set=None`（missing），无 hits 且已观察才 `[]`+evaluated。 |
| `src/reasoning_diff/analysis.py` | 1–337 | §2.6 P1–P3；§7 分流；附录 S2–S4 | P1 留出 logistic + 偏相关。bootstrap **重算** $\Delta\mathrm{AUC}$。`retrieval_scatter` 无嵌入则 BOW。 |
| `src/reasoning_diff/interventions.py` | 1–115 | §2.4 交换/对照/INLP/救援/$\mathrm{IE}_Z$ | 交换式、范数匹配、`ie_z`、`select_weak_layer` 库层正确。CLI 几何行不写 `pre_step`。对照结局在报告相对列仍为 `None`。 |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、未知/NaN 掩码、`fit` 形式正确。CLI tiny 维 32 故 `rank=min(64,d)`。 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | §4.2 Hidden=256 ReLU | 架构+`fit` 符合。CLI 用全 1 标签、无负例。 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | §2.5 命题 2 | 分位数与 $+\infty$ 正确。`truth_indices` 可限制到 $R(s_i)$。 |
| `src/reasoning_diff/probes/__init__.py` | 1–3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 1–125 | §8 文本/注意力/四档自述；GOAL §5.7 | 监督 BOW。verbalizer 走 `extract_answer`，不再子串。CLI `generate_fn` 回显前缀。 |
| `src/reasoning_diff/transfer.py` | 1–75 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。`common_dim_then_procrustes` 先 PCA 再 Procrustes。 |
| `src/reasoning_diff/repair.py` | 1–223 | §3 Repairability/RR；§9 嫁接；GOAL §5.13 | `execute_repair_tiny` 真 Prefill+hidden。`refilled_prefix` 只认有限 `prefill_hidden`。掩码仍改前缀字符串。 |
| `src/reasoning_diff/cli.py` | 1–1164 | §4 流水线；§8.2 scientific | scientific prepare 拒零事件/`parse_failed`，**接受** `constrained_target`。collect 拒 offline $H$、要求可表达步前行。fit 拒 NaN。intervene 按同 `node_id` 有限行配对；有 `--dev-layer-scores` 才第二次 decode。calibrate/intervene/repair 无 `--in-dir` 失败。 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | §8.1 模型卡/revision | 两张冻结卡 + `local_files_only=True`。CLI 不加载。无权重时属 pending_server。 |
| `src/reasoning_diff/models/collect.py` | 1–199 | §4.2 $h_i/e_j$；GOAL §5.6/5.10 | 不可表达 `pre_step` **跳过**该事件，不写入 $H$。`intervene_swap_decode` 的 `followed_donor` 仍是 ids 是否变化；`basis_seed` 进入正交基。 |
| `src/reasoning_diff/models/features.py` | 1–39 | §2.4 三时机；GOAL §5.6 | 跨界 token 排除正确。 |
| `src/reasoning_diff/models/generate.py` | 1–201 | §8.2 自然轨迹 | 显式 decode 后 **teacher-force** `\n{target} = ` 再采两位数字。只解析 `generated` 区。注释写明 Not gold values。 |
| `src/reasoning_diff/models/tiny.py` | 1–120 | 本机 hook 边界 | 随机 Qwen2/3 + resid_post。**不是**论文模型路径，不是 MODEL-01。 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | §4.2 层带 / span | `readout_layer_index`：3→1，32→21，36→24；空带拒绝。span 只收全含 token。1 字符 = 1 token。 |
| `src/reasoning_diff/models/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | §7 适配入口 | 快照分发；含 `t3_musique` / `t4_boundary` 别名。CLI 默认 `t1_fixture`。不生成 500 题。 |
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
| `tests/test_science.py` | 1–103 | 校准/迁移/交换/Week-8 | 库函数微例。 |
| `tests/test_measure.py` | 1–40 | $S/M$、联合编辑反例 | 与公式一致。 |
| `tests/test_review_regressions.py` | 1–397 | 上轮回归 | 锁住若干库修补。 |
| `tests/test_round03_regressions.py` | 1–291 | r03 回归 | 仍锁 `precomputed_scores`。 |
| `tests/test_round04_regressions.py` | 1–311 | r04 猎点 | 锁 generate≠节点真值、span $E$、几何≠`pre_step`、Prefill。 |
| `tests/test_round05_regressions.py` | 1–197 | r05 猎点 | 锁事件非空、H 有限、抽取答案、重采样、dummy 非 Prefill。**不**锁事件是自然生成步骤。 |
| `tests/test_round06_regressions.py` | 1–136 | r06 猎点 | 锁生成区、有限 $H$、donor 同 `node_id`、sham hits→missing、`--in-dir` 必填。**不**锁 $\backslash\mathrm{n}q=$ 约束行不是 §4.1 步骤。 |
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
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。Gate 保持 null（非缺陷）。tiny 只证明本机接口。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 2、3、6–8、10–13 条在科学入口仍被降级或替身。 |
| C4 | 阅读 `PAPER_TRACEABILITY.md` 约定，抽样 TR-0001–0043、TR-0125–0137、TR-0158–0166、TR-0293–0346、TR-0400 | 可执行行不再用 pytest 关闭；仍大量 `implemented_local`。TR-0125 为 `partial_local_scientific`。TR-0158/0400 仍指向 `intervention_report`。TR-0206/0327（MODEL-01）仍 `implemented_local`。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。 |
| C6 | 对照公式手核 + 复跑：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1、cone | $R_{\mathrm{task}}$/差集/交换/分位数/拒维度：**库函数层符合**。P1 bootstrap：**重算 $\Delta\mathrm{AUC}$**。噪声：hits → missing，不是 evaluated-zero。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | scientific 调用 generate + 拒 `parse_failed`。事件来自生成区，但是 teacher-force 目标行，不是自然步骤解析。 |
| C8 | 对照 §4.2 / §8 探针与基线 | tiny $E$ 行不同、`hidden_layer=1`。scientific $H$ 有限、行数=可表达事件数。CLI verbalizer 回显前缀，对自身抽出的 `82` 得 1.0。 |
| C9 | 对照 §2.4 / §6 干预 | 几何-only 写 `offline_hidden`。scientific tiny：`prospective_decode` / `offline_hidden`；相对对照四项仍 `None`。有 `--dev-layer-scores` 时 `clayer_status=dev_weak_layer_decode`。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 | T1 值编辑成立。Plus 孤立数字替换成立、无新 oracle。无侧车 Symbolic 拒编辑。T3/T4 常 `needs_truth`。 |
| C11 | 对照附录 S1–S4、C4 掩码、$k\in\{1..5\}$、失效相图 | S3 PCA 接通。S4 仍 BOW。scientific repair $k=1..5$ 且 Prefill；$k\ge3$ 槽位不再增长。无相图。 |
| C12 | 抽读测试是否固化替身 | 是：r05/r06 测只要求生成区有 `q`、H 有限、timing≠`pre_step`；不断言事件是自然 CoT 步骤。 |
| C13 | 独立重算论文/协议/GOAL/REQUIREMENTS SHA-256 | 四份与账本 §0 一致。 |
| C14 | 独立重算声明代码冻结 hash | **HASH_MATCH** `9814019a…f95801`，60 文件。 |
| C15 | 复跑 CLI prepare/collect/fit/intervene/repair/analyze 与库函数微例 | 见各 finding 的 Repro。命令已在本审查重跑，不是转述。 |
| C16 | 独立复跑 `pytest tests/test_round05_regressions.py tests/test_round06_regressions.py -q --tb=line` | **24 passed**（12.65s）。不把绿测当作原文正确。作者声称 143 passed **未**在本通道全量复跑，也不采信为验收。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 全量 `pytest -q` 作为本通道验收 | 原文符合性不由绿测关闭。作者声称 143 passed；本报告只记录指定两文件 24 passed。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量 500 题 | 协议 §7：科学结论 `pending_server`。tiny 随机权重不是 MODEL-01。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | 即使可拟合，标签对象仍是约束目标行上的 $R_{\mathrm{behavior}}$。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读 round-07 B–F。 |
| N6 | `PAPER_TRACEABILITY.md` 全部 528 行逐字复读 | 已读约定与高风险可执行/GOAL/REQUIREMENTS 行。剩余多为同一模板重复。 |
| N7 | 真实隔离沙箱跑 HumanEval | 无合格隔离后端；`ChildProcessExecutor` 不能冒称沙箱。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | generate/span/Prefill/生成区事件接口在；事件是约束目标行 | subst |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 1 | 34–35 | 检索余弦 vs 答案变 | exec | `retrieval_scatter` 无嵌入 → BOW | subst |
| 论文 1 | 38 | 修复解码/Prefill/耗时 | exec | tiny 有 generated/prefill/hidden；不是槽位成本 | ok-lib / subst |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema 正确；scientific 的 $T$ 是 `\nq = <digit>`，不是生成步骤序列 | subst |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | 字段在；比较的是约束数字是否变化，不再是题干预复述 | subst |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | id + aliases 词边界 | ok-lib |
| 论文 2.3 | 88 | 消失/合并/策略分岔 | proto | `removed`/`merged` 有；策略 `status_field_only`/`scanned=False` | stub |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap`；$\Pi=I$ 时得 donor | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ | math | `ie_z` 为向量均值差，不是预指定 $g$ | ok-lib / subst |
| 论文 2.4 | 106–108 | 前瞻 hook/KV/前缀 | exec | tiny $\Pi_Z$ + decode；`hook_timing` 可写 `pre_step`，报告 `timing` 保持 `offline_hidden` | ok-lib / subst |
| 论文 2.4 | 110 | 步前/数值前/步尾 | exec | 三阵写入；不可表达步前不再入 $H$ | ok-lib |
| 论文 2.4 | 114–117 | C-rand / C-layer 同幅度四项 | exec | 范数匹配在；无 dev 曲线诚实 `dev_scores_missing`；有分数则第二次 decode；相对列仍 `None` | stub / ok |
| 论文 2.5 | 121–125 | cone / Oracle / 行为掩码 | math | `dirty_cone`/`oracle_mask`/`behavior_mask` | ok-lib |
| 论文 2.5 | 127–130 | 命题 1 + REST-03 | math | $xy$ 反例夹具 | ok-lib |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | 分位数 ok；CLI 尝试按行 $R(s_i)$ | ok-lib |
| 论文 2.5 | 141–142 | 原轨迹槽位、禁重拓扑 | exec | Prefill 整段前缀字符串，不复用槽位 | subst |
| 论文 2.6 | 148–156 | $S,M,\rho$，空分母 N/A | math | `dependency_densities` + event mean | ok-lib |
| 论文 2.6 | 158 | 噪声先扣除 | proto | sham `premise_id` 带 `sham:`；hits → missing，不是 0 | ok-lib |
| 论文 2.6 | 164 | P1 logistic + 偏相关 + bootstrap | math | 留出 IRLS + 偏相关；bootstrap **重算** $\Delta\mathrm{AUC}$ | ok-lib |
| 论文 2.6 | 165 | P2 配对 + 污染位置 | exec | 库函数收 `contamination_positions`；无表则 CLI `None` | ok-lib |
| 论文 2.6 | 166 | P3 Δacc + 对照 + 非目标 | exec | 库函数收 nontarget；CLI 无表则 `None` | ok-lib |
| 论文 2.6 | 168 | REST-02 | proto | `causal_reverse_claim=False` | ok |
| 论文 3 | 176–186 | TO/CSP/覆盖/脏变/P/R/F1 | math | 公式在；CLI analyze 在有 features 时走 `predict_matrix` | ok-lib |
| 论文 3 | 188 | TO/CSP 噪声参照 | proto | `to_noise=0.84` / `csp_noise=0.0` 有数；密度 excess 因 hits 为 null | ok-lib |
| 论文 3 | 190 | 干预三项并列、前瞻/回溯分列 | proto | 范数三列有；相对对照结局仍 None | stub |
| 论文 3 | 194–200 | Repairability、RR、成本分列 | math | 两公式有；scientific 有 token/hidden；非槽位预算 | stub |
| 论文 4.1 | 232–253 | 双标签流水线；NL 单调对齐；共组 | exec | generate+生成区解析在；对象是约束 `\nq = <digit>` | subst |
| 论文 4.2 | 257–267 | MLP、双头、池化 $e_j$、60–75% 层 | exec | 层/池化在 tiny 接通；步前 $h_i$ 有限；MLP 全正例 | subst |
| 论文 5 Fig.1–2 | 291–299 | 热力图、三时机、跨模型迁移入口 | exec | 无导出；analyze 只报 4096/3584 N/A | missing |
| 论文 6 | 301–313 | 解耦资产、前瞻交换、INLP、救援 | exec | 配对构造器+`source_value_pair` 落盘；跟随判据是 ids 是否变化 | stub |
| 论文 7 | 315–329 | P1–P3 测量入口（不要求正结果） | exec | 库入口在；默认 CLI `p1=None`（行为标签皆未知） | stub |
| 论文 8 | 331–341 | 注意力/四档 verbalizer/监督文本 | exec | 库层抽答案；CLI 回显前缀当“生成” | subst |
| 论文 9 / Table 1 | 343–355 | 五条主对照 + 三条附录掩码实跑 | exec | 掩码改前缀字符串；decode 相同预算 | stub |
| 论文 Fig.6 | 353 | 失效相图五类 | exec | T4 状态枚举 ≠ 相图 | missing |
| 附录 S1 | 357–359 | $k\in\{1..5\}$ 连续编辑 | exec | 循环在；槽位不超事件名列表 | stub |
| 附录 S2 | 361–367 | 两参数锥拟合 | math | `cone_fit` 拟合；CLI 需 `cone_table.jsonl` | ok-lib |
| 附录 S3 | 371–373 | 共同维 + Procrustes | exec | PCA 后 Procrustes；同 $n$ 可对齐 | ok-lib |
| 附录 S4 | 375–377 | 嵌入余弦散点 | exec | BOW 点积，不是文本嵌入模型 | subst |
| 论文 7 数据 | 399–409 | T1–T4 假设专用资产 | exec | 读取器+部分 apply*；真值常 `needs_truth` | stub |
| 论文 8.2 | 419–431 | `--eval-mode scientific` | exec | 开关调用 generate 并拒空事件；事件对象仍是约束目标行 | subst |
| 论文 9 | 435–445 | 第一周三轨迹/50 干预冒烟 | exec | 三轨迹入口在；50 条解耦仍无 | stub |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |

---

## 5. Findings

### A7-01 — scientific 事件在生成区，但仍是 teacher-force `\nq = <digit>`，不是 §4.1 生成步骤

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/generate.py` `append_target_assignment` 72–98、`generate_task_trace` 135–160；`cli.py` `cmd_prepare` 296–297 |
| **Trigger** | 论文 §4.1 L232–248：`T0=generate` 之后 `parse_events` 的对象是**生成轨迹**上的变量/表达式/版本/作用域。§2.1：$T=(s_1,\ldots,s_n)$ 是模型生成序列的步骤离散化。r06“题干预复述当事件”**已满足关闭条件，不得原样重开**。作者把“约束目标行”写成 tiny 接口关闭——**本通道不接受**该关闭：论文 §8.2 科学评测写的是自然轨迹，不是强制赋值语法。 |
| **Paper requirement** | 自然轨迹步骤事件；$R_{\mathrm{behavior}}$ 来自固定随机流下编辑后**对应步骤值**是否变化；$h_i$ 为这些步骤的步边界。 |
| **Repro / evidence** | 复跑：`prepare --eval-mode scientific` 无 `--split-fractions` → `ValueError: scientific mode requires explicit --split-fractions`。加上六比例 + `--sham-opportunities 1` → exit 0，**6** 条轨迹，全部 `model=tiny-qwen2`，`generation=decode_loop`，`weight_source=random_init`，`parse_region=generated`，`parse_status=constrained_target`。文本例：`'p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82'`。`prompt_text` 止于 `?`（长度 36）。各迹 **1** 个事件：`q`，span `(45,51)`，`in_prompt=False`，值 82/53（采样数字，不是金标 0）。`target_assignment='\nq = 82'`。改 `p2`：`['q','q']` `no_change` `82→82`。标签：`(q,p2)`/`(q,p1)` `task_label=1`，`behavior_label=None`。 |
| **Impact** | C1 的可执行入口仍没有“生成步骤上的编辑响应”。账本 TR-0125 标 `partial_local_scientific` 比全称 `implemented_local` 诚实，但流水线把 `constrained_target` 当成功（只拒 `parse_failed`）。`test_generated_events_exclude_prompt_assignments` 只锁 `start ≥ prompt` 与含 `q`。 |
| **Suggested fix** | 只把自然 decode 段解析为事件；不要 teacher-force 赋值行来凑事件。仅有约束目标行时拒绝 scientific 的 label/collect，或保持 `unimplemented` / `partial_*`，不要跑满后续阶段冒称 §4.1。 |
| **Status** | **confirmed defect**；真实 CoT 质量 **pending_server**；“题干预复述当事件” **本轮不重开** |

### A7-02 — 账本可执行行不再用 pytest 关闭，但仍把替身（含 tiny≠MODEL-01）标成 `implemented_local`

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` TR-0158、TR-0206、TR-0308、TR-0316、TR-0319、TR-0322、TR-0327、TR-0346、TR-0400；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：未实现不得标已实现。r06 猎点是过称 `implemented_local`；可执行行验证列改为 `tests_exist_not_acceptance` **不得**按“pytest 关闭可执行行”重开。tiny 随机权重 **不是** MODEL-01。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。MODEL-01 是冻结 Qwen3/R1 推理，不是 `Qwen2ForCausalLM` 随机初始化。 |
| **Repro / evidence** | 528 行：`implemented_local=477`。可执行 159 条中 **157** 条仍 `implemented_local`，仅 TR-0125/`partial_local_scientific`、TR-0135/`partial_local_tiny`。TR-0158 / TR-0400（解耦任务构造）仍指向 `intervention_report`。TR-0206 / TR-0327（MODEL-01）`impl` 指向 `tiny,generate,collect,adapters`，状态仍 `implemented_local`。协议/标题行仍 **69** 处 `python -m pytest -q`。REQUIREMENTS 复选框全空，状态表写 `implemented_local` / `implemented_local_tiny`。本轮 collect `weight_source=random_init`。 |
| **Impact** | 覆盖率仍被制成 16/16。独立审查若信 `implemented_local` 会把 tiny 当成 MODEL-01，并漏检 A7-01。 |
| **Suggested fix** | MODEL-01 与未接到论文语义的可执行行改为 `unimplemented` / `ok-lib_unwired` / `partial_*`。验证列写对照原文的复跑产物。 |
| **Status** | **confirmed defect**（过称）；pytest-关闭可执行行 **本轮不重开**；tiny≠MODEL-01 **本条覆盖** |

### A7-03 — GSM-Plus / 无侧车 T2 / T4 没有“合法编辑 + 更新真值”

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t2_gsm_plus.py` `apply_plus_numeric_edit` 50–76；`t2_gsm_symbolic.py` 43–44, 68–70；`t4_boundary.py` 26, 36–50；`t3_humaneval.py` 34–74 |
| **Trigger** | 论文 §7 L403–407；GOAL §5.2；DATA-02。Plus 孤立数字替换**本轮成立**（`13` 保留，`3→9`），不得按“无 apply*”或“13 被改成 19”重开。 |
| **Paper requirement** | 各域：读取、合法编辑、**更新后真值**、事件/独立标注、域内评分。缺失标注保持 unknown，不得凭空生成。 |
| **Repro / evidence** | Plus：`validity=needs_truth`，`answer_spec.value=None`。Symbolic 无侧车：`graph_status=unknown`，`kind=placeholder`，编辑抛 `Cannot legally edit without a formula sidecar`。T4：四状态齐全，前提 placeholder，`apply_t4_question_edit` → `needs_truth`。HumanEval 无新解 → `needs_truth`。Hotpot 给口头新答案仍 `needs_truth`（此项诚实）。 |
| **Impact** | 除 T1 值编辑与 T2 侧车外，行为扫描没有更新后的 $v$。 |
| **Suggested fix** | 每域提供编辑+新 oracle；缺失保持 `unknown`/`needs_truth`，不要把读取器标成域适配完成。 |
| **Status** | **confirmed defect**（更新真值）；孤立 Plus 编辑本身非缺陷 |

### A7-04 — 附录 S4 与 Table 1 没有按论文口径的测量入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `retrieval_scatter` 300–305；`repair.py` `mask_prefix` 47–70；CLI analyze 1008–1012 |
| **Trigger** | 论文附录 S1–S4；S4“不得因精简而删除”。S3 PCA 与 S1 $k$ 循环、Prefill **不得**按“截断/无循环/无 Prefill”重开。 |
| **Paper requirement** | $k\in\{1..5\}$ 连续编辑并 Prefill 保留文本；先共同维映射再 Procrustes；$(P,P\oplus\Delta P)$ **文本嵌入**余弦 vs 答案是否改变；八条掩码按槽位实跑。 |
| **Repro / evidence** | `retrieval_scatter(texts_a=…)` → `embedding_kind=bow_descriptive_not_paper_embed`。同 $n$ S3：`truncated=False`，`adapted_geometry`。scientific repair：$k=1..5$，`refilled_prefix=True`，`prefill_hidden` 长 32；`k=4,5` 的 `slots` 与 $k=3$ 相同（`[p1,p2,q]`）。Table 1 掩码只改前缀字符串。 |
| **Impact** | S4/Table 1 没有从入口到图的论文口径路径。 |
| **Suggested fix** | S4 用声明的嵌入；掩码按槽位执行；无资产保持 `not_evaluated`。 |
| **Status** | **confirmed defect**（S4/掩码语义）；S2 库函数、S3 PCA、S1 循环/Prefill 本身非本条猎点缺陷 |

### A7-05 — CLI 四档 verbalizer / BoundaryMLP / 注意力仍是替身（子串已关）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_fit` 636–649；`baselines.py` 92–125；`probes/boundary.py` |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7。子串打分 **本轮不再成立**（独立复跑 17/70/boxed）。 |
| **Paper requirement** | 四档自述；监督档与探针同样本/划分/可见前缀。2 层 MLP 边界检测（token 级正负例）。注意力阈值在 dev 上选定。 |
| **Repro / evidence** | 库：`verbalizer(..., generate_fn=λ:"17")` 对金标 `7` 得 0；`70` 得 0；`\boxed{8} also 7` 得 0（抽出 8）。CLI `generate_fn` 为 `lambda p, t=prefix: t`（回显前缀）。scientific fit：zeroshot/fiveshot/reflection `score=1.0`，`extracted='82'`（轨迹文本里的约束赋值，金标取自 `traces[0].answer=82`）。supervised 拒未训练。BoundaryMLP：`y_b = ones`，`note=event-rows-only_no_negatives`。attention_mean 对空权重得 0。 |
| **Impact** | 第 8 节“说不出来”在 CLI 上仍不是同划分模型自述；scientific 路径把约束数字回显打成满分。 |
| **Suggested fix** | CLI 按同一划分调用真实生成与 token 级 MLP；未接线不得标 `implemented_local`。 |
| **Status** | **confirmed defect**（CLI 替身）；子串打分 **本轮不重开** |

### A7-06 — 干预相对对照四项仍为 None；`followed_donor` 仍是 ids 是否变化

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_intervene` 821–862；`models/collect.py` `intervene_swap_decode` 193 |
| **Trigger** | 论文 2.4 L106–117；§6 L305–313；GOAL §5.10–5.11。猎点“几何-only 不得写 `pre_step`”**已满足**（手造有限 $H$：`timing=offline_hidden`，`status=geometry_on_hidden`）。 |
| **Paper requirement** | 目标步首 token 前交换 residual；评价新生成 $s_k$ 是否跟随 donor。报告四项结局相对对照的差值。 |
| **Repro / evidence** | `apply_swap`：$H^b=[1,0]$，$H^d=[0,1]$，$\Pi=I$ → `[0,1]`。scientific tiny intervene：`status=prospective_decode`，`timing=offline_hidden`，`hook_once=resid_post`，`donor_rows=[0,1]`（两条 `q`）。`target/nontarget/task_correct=0`，`invalid=1.0`；`relative.target/nontarget/task_correct/invalid` 皆 `None`（对照字典硬编码 None）。`followed_donor=False`（定义：`generated_ids != baseline`）。有 `--dev-layer-scores 0.05 0.9 0.8`：`clayer_status=dev_weak_layer_decode`，`weak_layer=0`，`inlp_followed_donor` 有键。 |
| **Impact** | C2 主张入口仍不是“来源跟随”。几何不再冒称 `pre_step`。 |
| **Suggested fix** | 在对齐的 $s_k$ 首 token 前 hook；按预注册矩阵评分；对照四项写入相对列。 |
| **Status** | **confirmed defect**（结局/跟随定义）；几何 timing 猎点 **本轮不重开** |

### A7-07 — 修复已 Prefill/decode，但不是原槽位嫁接

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `repair.py` `mask_prefix` 47–70；`execute_repair_tiny` 75–123；`cli.py` 891–930 |
| **Trigger** | 论文 §3 L194–200、§9 L347–355、附录 S1；GOAL §5.13。猎点“必须 Prefill/decode 或诚实 `refilled_prefix=False`”**已满足**。 |
| **Paper requirement** | 干净文本在当前前缀重新 Prefill，**受损槽位**自回归重算。主文 5 条 + 附录 3 条实跑。同原始 token 预算。 |
| **Repro / evidence** | scientific repair：5 条记录，$k=1..5$，`generated_tokens=8`，`extra_prefill_tokens=32`，`refilled_prefix=True`。`k=1` slots=`[p1]`，$k=2`=`[p1,p2]`，$k\ge3`=`[p1,p2,q]`。offline/dummy：`refilled_prefix=False`。`mask_prefix` 只改字符串。 |
| **Impact** | Repairability/RR/同预算曲线无法按槽位测量。 |
| **Suggested fix** | 按掩码在原轨迹槽位重算；无槽位资产不得标 Table 1 已跑。 |
| **Status** | **confirmed defect**（槽位语义）；Prefill 接口本身非本条猎点缺陷 |

### A7-08 — 自然语言事件对齐与官方 CoT 解析缺失

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `events.py` `parse_events` 74–88；`align_events_monotonic` 196–216 |
| **Trigger** | 论文 4.1 L250–252；2.3 L87–88。单调对齐函数存在。不得说“无解析/无单调函数”。不得按“题干赋值被收成事件”重开。 |
| **Paper requirement** | 结构化：变量/表达式/版本/作用域。NL：抽实体后允许跳过与合并的单调序列对齐。消失/合并/策略分岔单独计数。 |
| **Repro / evidence** | scientific 只解析生成区，故题干 `p1`/`p2` 不再入事件。生成区无自然赋值，只靠 teacher-force `\nq = 82`。无 iGSM 官方 CoT 解析。`strategy_changed` 仅 `status=="strategy_change"`；`scanned=False`（诚实）。 |
| **Impact** | T2/T3 没有事件层；scientific T1 的“事件”也不是生成 CoT。 |
| **Suggested fix** | 分域解析器只吃生成段 + NL 单调对齐；未对齐进单独计数。 |
| **Status** | **confirmed defect** |

### A7-09 — T1 500 题 / 四档 op 没有 CLI 默认入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t1_config.py` 9–21；`cli.cmd_prepare` 默认 `t1_fixture`；`--t1-ops` 287–290 |
| **Trigger** | 论文 §7 L403、§9 L437；WEEK1-01。三轨迹 **scientific 已产**，不得按“无三轨迹”重开。 |
| **Paper requirement** | iGSM `op∈{5,10,15,21}`、500 题；$T_0(seed=0)$、$T'_0(seed=1)$、$T_{\mathrm{pert}}(seed=0)$。 |
| **Repro / evidence** | 配置校验存在。`--t1-ops` 只 `validate_t1_prepare_config`，仍一条夹具题。全量 500 属 pending_server；**任务单/四档 op 入口本身**仍是代码缺口。 |
| **Suggested fix** | 配置驱动的任务单；CLI 消费快照目录。 |
| **Status** | **confirmed defect**（入口）；全量跑数 **pending_server** |

### A7-10 — 默认划分比例未预注册

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

### A7-11 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 215–257；`cli.py` 934–1044 |
| **Trigger** | 协议 §6；GOAL §5.14；DECIDE-01。任务：Gate 0–2 未注册 **不是** 缺陷。 |
| **Paper requirement** | 用户未给阈值则不得编造 pass/fail。不得把 fixture 写入科学结论。 |
| **Repro / evidence** | 复跑 analyze（scientific labels）：`gates.*.decision=unregistered`，`threshold=None`，`scientific_conclusion=None`，`p1=p2=p3=None`，`status=not_evaluated`，`skip_p2_p3=True`。`week8_decision({rho_S_excess:0})` → `c3_negative_descriptive`。有阈值无度量 → `threshold_present_measurement_missing`。 |
| **Impact** | 正确持守。假说不要求正结果，本条不升格。 |
| **Suggested fix** | 不要添加阈值。 |
| **Status** | **non-defect** |

### A7-12 — $H$ 有限步前行 / sham hits 不记 evaluated-zero（非本轮缺陷；猎点核销）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `models/collect.py` `collect_hidden_trace` 50–52；`measure.py` `event_density_sets` 289–302 |
| **Trigger** | 本轮指定猎点：H 是否有限且非末 token / NaN 标 `pre_step`；sham 是 evaluated-zero 还是 unmapped hits。 |
| **Paper requirement** | $h_i$ 为可表达步边界；噪声不得把未映射 hits 写成已评估 0。 |
| **Repro / evidence** | $H=(6,32)$ 全有限；`pre_step.token_index=44` ≠ 序列末（50）。scientific fit 两头写出（behavior `no_known_labels`，因行为标签皆未知——诚实）。sham hits：`q` `82 vs 53`，密度 `noise_set_missing`，`rho_S_excess=None`。手造 `noise_ref=1.0` 同行。 |
| **Impact** | 这两条猎点在当前字节上**不成立为缺陷**。不能抵消 A7-01。 |
| **Suggested fix** | 不要把已评估 0 与 unmapped hits 重新绑在一起。 |
| **Status** | **non-defect**（本轮猎点核销） |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5。

1. **Gate 0–2**：无阈值、无 pass/fail（A7-11）。
2. **`scientific_conclusion` 保持 `None`**。
3. **REST-01/02/03** 禁词列表存在；P3 不自动写“只是后果”；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
4. **身份对齐不含值**。
5. **$R_{\mathrm{task}}$ 祖先**、**$S/M$ 空分母→null**、**缺/空 sham→excess null**、**signed excess 不截断**。
6. **有限扫描**：`exhaustive=False` 时 `no_change` 不作已知负（本轮 scientific 行为标签皆 `None`）。
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
17. **P1 留出路径为 IRLS logistic**；bootstrap **重算** $\Delta\mathrm{AUC}$，区间非退化。
18. **scientific 调用模型 generate**，不是节点真值轨迹；零事件 / `parse_failed` 被拒绝。
19. **tiny $E$ 为读出层 span 均值**，行不相同；scientific 拒 offline $H$。
20. **不可表达步前不入 $H$**；有事件时有限行标 `pre_step` 且对应事件起点之前，不是末 token。
21. **repair 无模型 / 无 hidden / 仅 prefix_ids 时 `refilled_prefix=False`**。
22. **verbalizer 抽答案**：`17`/`70`/`boxed` 不再当子串命中。
23. **span 跨界排除**；60–75% 空带拒绝。
24. **S3 先 PCA 再 Procrustes**（同 $n$）。
25. **REQUIREMENTS 行内 hash 与 §0 一致**。
26. **可执行行不再用 pytest 关闭**（`tests_exist_not_acceptance`）。
27. **`source_value_pair` 写入 `edits.jsonl`**。
28. **sham hits 不记 evaluated-zero**（A7-12）。
29. **tiny `weight_source=random_init` 不是 MODEL-01**（实现层诚实；账本过称见 A7-02）。
30. **calibrate / intervene / repair 无 `--in-dir` 失败**。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_full_cli_smoke` | 八阶段返回 0；**offline** $H$；`not_evaluated` | generate、论文步边界 $H/E$、干预生成、槽位嫁接 |
| `test_scientific_prepare_emits_parseable_events` | 每条轨迹 ≥1 事件且含 `q`；无节点真值拼接；sham `premise_id` 带前缀 | 事件是生成步骤；$R_{\mathrm{behavior}}$ 不是约束数字 |
| `test_generated_events_exclude_prompt_assignments` | `start ≥ prompt`；`parse_region=generated` | 禁止 teacher-force `\nq =` |
| `test_scientific_collect_h_is_step_boundary_not_last_token` / `test_scientific_h_is_finite_and_pairs_donor` | $H$ 有限；行数≤事件数；donor 同 `node_id` | 步前对应自然生成步 |
| `test_span_no_straddle_fallback` | 跨界 → `[]` | $e_j$ 来自真实 tokenizer 边界 |
| `test_verbalizer_uses_extracted_answer_not_substring` | `17`/`70`/`boxed` 不子串命中 | 同划分四档模型自述 |
| `test_dummy_execute_is_not_prefill` / `test_prefix_ids_alone_are_not_prefill` | 无 hidden → `refilled_prefix=False` | 槽位嫁接 |
| `test_p1_bootstrap_resamples_delta_auc` / `test_p1_bootstrap_interval_is_not_degenerate` | `resampled_delta_auc` 且 `lo<hi` | CLI 用 $\rho_S$ 表计算 P1 |
| `test_intervene_tiny_geometry_timing_stays_offline` | `timing≠pre_step`；`status` 为 decode/geometry | 四项相对对照、来源跟随定义 |
| `test_sham_hits_do_not_book_evaluated_zero_noise` | hits → `noise_set_missing` | 噪声集合有匹配前提身份 |
| `test_scientific_repair_runs_k_1_to_5` / `test_repair_k_changes_masked_prefix` | $k=1..5` 且 Prefill | 槽位执行改变 |

---

## 8. 本审查复跑的命令（均可再跑）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → **60** / `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `python -m pytest tests/test_round05_regressions.py tests/test_round06_regressions.py -q --tb=line` → **24 passed**。
4. `main(['prepare', …, '--eval-mode','scientific'])` 无 fractions → `ValueError`；有 fractions + sham 1 → 6 条 tiny decode 轨迹，各 1 个生成区 `q` 事件，`parse_status=constrained_target`，文本含 `\nq = 82`，不是题干预复述。
5. `collect --backend tiny` + scientific → $H=(6,32)$ 全有限，`hidden_layer=1`，$E$ 行不同，`event_rows` 6×`q`，`pre_step.token_index=44`；scientific offline → 拒绝。
6. scientific `fit` → task loss `0.05036`，behavior `no_known_labels`；verbalizer 回显前缀得 `extracted=82` `score=1.0`。
7. scientific `intervene` → `prospective_decode` / `offline_hidden`，四项相对 `None`；手造有限 $H$ + offline → `geometry_on_hidden` / `offline_hidden`。
8. scientific `repair` → $k=1..5$，`refilled_prefix=True`，`prefill_hidden` 存在；dummy / prefix_ids → `False`。
9. `analyze` → `p1=p2=p3=None`，`scientific_conclusion=None`，Gate `unregistered`；密度 `noise_set_missing`。
10. `verbalizer` 17/70/boxed、`p1_incremental` bootstrap、`span_token_indices`、`apply_swap`、`sequence_score`、`week8_decision`、域加载器：见 §5。

---

## 9. ISSUES 处置（作者关闭 ≠ 本通道关闭）

`ISSUES.md` 将 A6-01/A6-02/A6-04 等列为作者 local close。本通道独立裁定：

| 作者声称关闭 | 本轮独立裁定 |
|---|---|
| 题干赋值不再当生成事件 | **同意核销**（不得原样重开） |
| 可表达 $H$ only | **同意核销**（$H$ 有限，非末 token / 非 NaN 冒称） |
| sham hits 不记 evaluated-zero | **同意核销**（hits → missing） |
| `source_value_pair` 落盘 | **同意核销** |
| 约束 `\nq = <digit>` 只是 tiny 接口、可关 A6-01 | **拒绝关闭**。见 A7-01：这仍不是 §4.1 生成步骤。 |
| tiny 不是 MODEL-01 | **实现层同意**；账本仍过称，见 A7-02 |
| Gate 未注册不是缺陷 | **同意**（A7-11） |

---

## 10. 结论

**冻结 hash：HASH_MATCH** `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（60 文件）。

**原文一致性：不通过（FAIL）。**

r06 猎点中的“生成区事件 / 非题干预复述 / 有限步前 $H$ / 非末 token / sham 不记 0 / 几何不写 pre_step / 非子串 verbalizer / 真 bootstrap / dummy 非 Prefill / Prefill 有 hidden / source_value_pair 落盘”，本轮在接口上已接通，不得原样重开。科学入口改在**事件定义**处断开：生成区只有 teacher-force 的 `\nq = <digit>`，于是 $R_{\mathrm{behavior}}$ 与步前 $H$ 对齐的是约束赋值，不是论文 §4.1 步骤。Gate 0–2 未注册、假说不要求正结果、tiny 不是 MODEL-01——这三条被遵守（后一条在代码元数据上遵守，在账本上仍过称）。作者关闭与绿测不能关闭本通道。真实权重/官方全量是 `pending_server`，不能解释本机把约束目标行写成 $T$。

独立复审关闭条件（本通道）：A7-01 必须在**同一冻结 hash** 上对照原文关闭（scientific 事件来自生成步骤，或诚实拒绝 `constrained_target` 并停止后续科学阶段）；A7-02 至少把 MODEL-01 与未接线可执行行降为诚实状态。其余 medium 项至少改为诚实状态或补上测量入口。
