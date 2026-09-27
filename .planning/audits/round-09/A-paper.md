# 审查报告 A：原文一致性（paper consistency）— round-09

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-09 |
| **审查时间** | 2026-09-21 02:14 起（UTC+8）；交卷前工作树仍在变动 |
| **声明冻结 hash** | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（60 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **HASH_MISMATCH（交卷时）。** 审查**开始**按 `VERSION.md` 原文逐字复算：文件数 **60**，摘要 `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`，与声明一致。交卷前同脚本：**排除**后增 `tests/test_round07_regressions.py` 仍为 60 文件，摘要已变为 `57b43360c354ede2caf4a99adae7a0b33c082ec534f675b295709890931427bd`；**计入**该文件则为 61 文件，摘要从 `fea2565f…` 再变为 `c29ad0dd4a1f5fd161fb3459433d7af4f5f9dd987d0120f800f0c545c106d124`。本通道未改 `src/`、`tests/`、`pyproject.toml`。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `39CF907C0B66B9B26AE7355E394848CFA1FF41CE5166310E1DC0A9307F9AC498`（与账本 §0 一致） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`（开始时 60 文件清单）。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-09/` 下除 `VERSION.md` 与本文件外的任何通道报告。**未把** `ISSUES.md` 作者关闭当作关闭。后增 `tests/test_round07_regressions.py` **不在**声明 60 文件冻结内，未当作本轮验收对象。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |
| **作者声称 pytest** | VERSION 写 144 passed。本通道复跑指定命令：`tests/test_round05_regressions.py` + `tests/test_round06_regressions.py` → **24 passed**（审查前段、仍为 60 文件时）。绿测不关闭原文符合性，也不认证已漂的树。 |

**总判：不通过。** 声明冻结在审查开始可核验，**交卷时不能认证**。相对 r08，本通道独立复跑后**不得原样重开**的接线项：scientific 事件在生成区；`source_value_pair.trace_ids` 指向 `trace-edit`/`trace-source`；`donor_kind=same_source_diff_value`；INLP decode 的 `inlp_transform=inlp`（主交换仍为 `pi_z_swap`）；`ie_z_g=target_follow`；几何 `timing=offline_hidden`；有限 $H$ 行=事件。

本轮仍 FAIL，原因有两层，缺一即不通过：

1. **冻结完整性：** 交卷前源+既有测试已从 `9ffc4cd9…` 漂到 `57b43360…`，并新增第 61 个测试文件。对声明 hash 的通过意见不能交给漂移树。
2. **原文语义：** scientific 仍把 teacher-force `\nq = <两位数字>` 标成 `parse_status=constrained_target` 后**当作 §4.1 成功事件**。7 条轨迹各只有 `q`；随机 decode 段不可解析。$R_{\mathrm{behavior}}$ 比较的是约束数字是否变化（本机编辑后 82→82，`behavior_label=None`），不是固定随机流下生成步骤值。`cmd_fit` 默认 `--in-dir=collect --labels-dir=label` 读不到 `tasks.jsonl`，Y 列退回 labels 首次出现序 `[p2,p1]`，与 $E$ 的 `[p1,p2]` 对调。

Gate 0–2 保持 `unregistered`，**不是缺陷**。tiny 随机权重 **不是** MODEL-01。假说不要求正结果。不把 Goal 标为完成。

---

## 0. 相对上一轮树的诚实变化（避免把已修项当新缺陷）

独立重读当前字节并复跑后，下列 **不再** 作为本轮 confirmed defect 原样重开（不等于科学语义已齐；且交卷树 ≠ 声明冻结）：

| 先前问题 | 本审查复跑（开始 MATCH 之后、文件数变为 61 之前） |
|---|---|
| 题干 `p1 = 4` / `p2 = 0` 被收成生成事件 | `parse_events` 吃 `gen_text+assigned`；7 条轨迹事件均 `start≥prompt_len`，节点只有 `q`。题干单独解析仍能得到 `p1`/`p2`，**不再**写入 scientific 事件。 |
| 零事件 / 节点真值拼接 | 文本 `'…?Z*H[!XTC\nq = 82'`，`model=tiny-qwen2`，`generation=decode_loop`。**不是** `p1 = 4 \| p2 = 0 \| q = 0`。 |
| $H$ 含 NaN / 末 token 冒称 `pre_step` | scientific collect：$H=(7,32)$ **全有限**，`event_rows=7` 全为 `q`，`hidden_layer=1`，$E=(2,32)$ 行不同。 |
| `source_value_pair` 未落盘 / donor 不是来源—数值臂 | `edits.jsonl` 含 `kind=source_value_pair`；`trace_ids.same_source_diff_value=trace-edit`，`same_value_diff_source=trace-source`。`_pair_source_value` → `(0, 2, 'same_source_diff_value')`。intervene `donor_kind=same_source_diff_value`，`donor_rows=[0,2]`。 |
| INLP 仍是 $\Pi_Z$ 交换 | 主 hook `transform=pi_z_swap`；`inlp_transform=inlp`；`crand_transform=add_delta`；`rescue_transform=replace`。有 `--dev-layer-scores 0.05 0.9 0.8` 时 `clayer_transform=add_delta`，`weak_layer=0`，`clayer_status=dev_weak_layer_decode`。 |
| `ie_z` 用隐向量差冒充 $g(Y)$ | tiny 路径：`ie_z_g=target_follow`，`ie_z=g_int-g_base`（本机 `0.0`）。**字段接线**成立；比较对象仍是 4-token decode 抽出的数字 vs donor 约束答案，见 A9-01。 |
| 几何-only 写 `timing=pre_step` | `timing=offline_hidden`。 |
| Gate 未注册 / tiny=MODEL-01 | **不是缺陷**（见 A9-N1 / A9-N2）。 |

**未关闭：** §4.1 的解析对象仍是约束目标行，不是自然生成步骤；由此 $R_{\mathrm{behavior}}$ 与 $\mathrm{IE}_Z$ 的 $g(Y)$ 都不是论文对象；scientific `fit` 在标准 `--in-dir=collect --labels-dir=label` 下仍用 labels 首次出现序对齐 Y。声明冻结在交卷时已失效。

---

## 1. 逐文件覆盖

每行：路径（磁盘 `splitlines()` 行数，交卷前读数）— 对照条款 — 结论。行数可能已随漂移变化；行为结论以审查中段复跑为准。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 1–517 | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 1–86 | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。Gate 保持 null 与代码一致。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 1–166；§5 = 73–91 | GOAL §5.1–5.15 | 第 3、6–8、10–13 条在科学入口仍被降级或替身。第 14、15 条持守。 |
| `.planning/REQUIREMENTS.md` | 1–76 | DATA/MEAS/MODEL/PROBE/… 与 atomics | 复选框全空；状态表仍写 `implemented_local`。MODEL-01 写成 `implemented_local_tiny`——tiny 不能关 MODEL-01。 |
| `.planning/PAPER_TRACEABILITY.md` | 1–44 约定；75–120、202–243、370–420 抽样 | 账本不得当实现证据 | 726 行 / 528 TR 行。TR-0125 仍 `partial_local_scientific`；TR-0135 仍 `partial_local_tiny`。TR-0158 / TR-0400 仍 `implemented_local`。协议/标题行仍约 70 处 `pytest -q`。 |
| `pyproject.toml` | 1–27 | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 有 `torch`/`transformers`。无强制 scientific 栈。 |
| `src/reasoning_diff/__init__.py` | 1–5 | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 1–4 | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 1–385 | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 1–46 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先与相交掩码正确。默认 cone 走任务祖先。 |
| `src/reasoning_diff/events.py` | 1–274 | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 对齐 | `parse_events` 仍把前提与节点都当赋值模式。scientific 调用方把文本限制在生成区。策略仍只读 `status=="strategy_change"`。 |
| `src/reasoning_diff/edits.py` | 1–277 | §7 T1 重算；GOAL §5.2 | 值编辑+表达式重算正确。`make_source_value_pair` 有同值异源。 |
| `src/reasoning_diff/measure.py` | 1–388 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集、空分母、缺/空 sham→null、signed excess 正确。sham 命中带 `sham:` 前缀时不把空 $N$ 记成已评估 0；映射到真实前提的 noise hit 另计。 |
| `src/reasoning_diff/analysis.py` | 1–337 | §2.6 P1–P3；§7 分流；附录 S2–S4 | P1 留出 logistic + 偏相关。bootstrap 重算 $\Delta\mathrm{AUC}$。`retrieval_scatter` 无嵌入则 BOW。 |
| `src/reasoning_diff/interventions.py` | 1–115 | §2.4 交换/对照/INLP/救援/$\mathrm{IE}_Z$ | 交换式、范数匹配、`ie_z`、`select_weak_layer` 库层正确。无 `--dev-layer-scores` 时相对 C-layer 为 `None`（诚实缺失）。 |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、未知/NaN 掩码正确。CLI tiny 维 32 故 `rank=min(64,d)`。 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | §4.2 Hidden=256 ReLU | 架构+`fit` 符合。CLI 用全 1 标签、无负例。 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | §2.5 命题 2 | 分位数与 $+\infty$ 正确。`truth_indices` 可限制到指定列。 |
| `src/reasoning_diff/probes/__init__.py` | 1–3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 1–125 | §8 文本/注意力/四档自述；GOAL §5.7 | 监督 BOW。verbalizer 走 `extract_answer`。CLI `generate_fn` 回显前缀。 |
| `src/reasoning_diff/transfer.py` | 1–75 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。`common_dim_then_procrustes` 先 PCA 再 Procrustes。 |
| `src/reasoning_diff/repair.py` | 1–223 | §3 Repairability/RR；§9 嫁接；GOAL §5.13 | `execute_repair_tiny` 真 Prefill+hidden。无 hidden 的 execute 被拒。掩码仍改前缀字符串。 |
| `src/reasoning_diff/cli.py` | 1–1251 | §4 流水线；§8.2 scientific | scientific prepare 拒 `parse_failed`，**接受** `constrained_target`。collect 拒 offline $H$、跳过不可表达行。fit 只在 collect/labels 目录找 `tasks.jsonl`。intervene 优先 `source_value_pair` 的 `trace-base`/`trace-edit`。 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | §8.1 模型卡/revision | 两张冻结卡 + `local_files_only=True`。CLI 不加载。无权重时属 pending_server。 |
| `src/reasoning_diff/models/collect.py` | 1–261 | §4.2 $h_i/e_j$；GOAL §5.6/5.10 | 按事件取三时机；`pre_idx is None` 则整行跳过。`intervene_hidden_decode` 分 `pi_z_swap`/`inlp`/`add_delta`/`replace`。`followed_donor` 仍是 ids 是否变化。 |
| `src/reasoning_diff/models/features.py` | 1–39 | §2.4 三时机；GOAL §5.6 | 跨界 token 排除正确。 |
| `src/reasoning_diff/models/generate.py` | 1–201 | §8.2 自然轨迹；§4.1 | 显式 decode 后 **teacher-force** `\n{target} = ` 再采两位数。`parse_region=generated`；有赋值行则 `constrained_target`。注释写 Not gold values。 |
| `src/reasoning_diff/models/tiny.py` | 1–120 | 本机 hook 边界；**不是 MODEL-01** | 随机 Qwen2/3 + resid_post。`weight_source=random_init`。 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | §4.2 层带 / span | `readout_layer_index`：3→1；空带拒绝。span 只收全含 token。1 字符 = 1 token。 |
| `src/reasoning_diff/models/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/tasks/catalog.py` | 1–45 | §7 适配入口 | 快照分发；含 `t3_musique` / `t4_boundary` 别名。CLI 默认 `t1_fixture`。不生成 500 题。 |
| `src/reasoning_diff/tasks/t1_official.py` | 1–92 | §7 T1；template≠G | 快照加载拒绝裸 `G`、排除共享 RNG、默认 mod 23。CLI 默认不走。 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | 官方/夹具分离 | 拒绝非 `fixture`。成立。 |
| `src/reasoning_diff/tasks/t1_config.py` | 1–21 | op∈{5,10,15,21}，n=500 | 配置校验。`--t1-ops` 只校验，不生成任务单。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–85 | §7 T2；GOAL §5.2 | 无侧车：placeholder + `graph_status=unknown`，拒编辑。有侧车：值编辑+算子逆转。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–84 | §7 T2；评测专用 | test-only 锁正确。孤立数字替换成立；答案 `needs_truth`/`None`。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 1–100 | §7 T2-noop | 可造配对与分层元数据。无注入句值扰动扫描。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 1–104 | §7 T3；supporting_facts≠DAG | 标记正确。无独立新答案则 `needs_truth`。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 1–110 | §7 T3 组成引用 | 保留 answerable/unanswerable。`expression="composition_reference"` 不可重算。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–78 | §7 HumanEval-Perturb；GOAL §5.15 | `edit_kind=input_list` 有旗。无新解则 `needs_truth`。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 1–51 | §7 T4；Fig.6 | 四类状态强制区分。前提=placeholder。`apply_t4_question_edit` 为 `needs_truth`。无相图。 |
| `src/reasoning_diff/tasks/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/executor.py` | 1–109 | GOAL §5.15 | 禁止宿主 exec。默认 `UnavailableExecutor`。`ChildProcessExecutor.isolated_sandbox=False`。 |
| `src/reasoning_diff/scoring.py` | 1–30 | §3 域内评分 | 数值/QA 精确匹配。代码经执行器接口。 |
| `src/reasoning_diff/splits.py` | 1–152 | §4.1 共组；GSM-Plus test-only | 六角色 + 家族共组。`gsm_text_key` / 测试专用家族锁存在。默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 1–53 | GOAL §5.4 | sample/direction/perturb/bootstrap/split 分离。 |
| `src/reasoning_diff/io.py` | 1–133 | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 1–85 | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 1–11 | — | 夹具路径。 |
| `tests/test_cli_pipeline.py` | 1–30 | §4 流水线 | 八阶段 exit 0；**仍强制** `--backend offline`。 |
| `tests/test_science.py` | 1–103 | 校准/迁移/交换/Week-8 | 库函数微例。 |
| `tests/test_measure.py` | 1–40 | $S/M$、联合编辑反例 | 与公式一致。 |
| `tests/test_review_regressions.py` | 1–397 | 上轮回归 | 锁住若干库修补。 |
| `tests/test_round03_regressions.py` | 1–292 | r03 回归 | 仍锁 `precomputed_scores`。 |
| `tests/test_round04_regressions.py` | 1–311 | r04 猎点 | 锁 generate≠节点真值、span $E$、几何≠`pre_step`、Prefill。 |
| `tests/test_round05_regressions.py` | 1–197 | r05 猎点 | 锁事件非空、H 行数、抽答案、重采样。**不**锁事件是生成步骤。 |
| `tests/test_round06_regressions.py` | 1–145 | r06 猎点 | 锁生成区、有限 $H$、helper 列序、**以及** `donor_kind`/`inlp_transform`/`ie_z_g` 字段。**不**锁拒绝 `constrained_target`；**不**锁 `cmd_fit` 实际读到 $E$ 序。 |
| `tests/test_round07_regressions.py` | 1–185 | 后增 | **不在** VERSION 60 文件冻结。本通道不据其关闭或新开缺陷。 |
| `tests/test_tracer_t1_prepare.py` | 1–100 | T1 夹具准备 | 身份/重算/空分母。 |
| `tests/test_t1_official.py` | 1–31 | template≠G | 快照形状。 |
| `tests/test_t2_gsm.py` | 1–33 | T2 | 侧车数值编辑。 |
| `tests/test_t3_t4.py` | 1–44 | T3/T4 | supporting_facts ≠ DAG。 |
| `tests/test_artifacts.py` | 1–73 | I/O | 工程。 |
| `tests/test_generate_loop.py` | 1–17 | 可重放采样 | tiny decode。 |
| `tests/test_tiny_hooks.py` | 1–27 | hook 清理 | 本机接口。 |
| `tests/test_tiny_cache.py` | 1–26 | 缓存隔离 | `intervene_tiny` 断言 logits 因 $\Pi_Z$ 改变。 |

第三方库：审查了本项目对 `numpy` / 可选 `torch`+`transformers` 的使用假设，未审查依赖源码。

夹具抽读：`tests/fixtures/t1_tiny.json`（全文）。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献清单 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。Gate 保持 null（非缺陷）。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 3 条（事件与行为）在科学入口被约束目标替换。 |
| C4 | 阅读 `PAPER_TRACEABILITY.md` 约定，抽样 TR-0001–0043、TR-0125–0137、TR-0158、TR-0400 | TR-0125 仍 `partial_local_scientific`。TR-0158/0400 仍 `implemented_local`。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。开始时 60 文件清单与 VERSION 一致。 |
| C6 | 对照公式手核 + 复跑：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1、cone | 库函数层：$R_{\mathrm{task}}$/差集/交换/分位数/拒维度 **符合**。P1 bootstrap **重算** $\Delta\mathrm{AUC}$。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | generate 在；解析区=生成段；**事件来自 teacher-force 目标行**，`constrained_target` 被接受。另生成 `trace-source`。 |
| C8 | 对照 §4.2 / §8 探针与基线 | $H$ 有限、行=事件、层=1、$E$ 行不同。行为头因无已知标签未写出 $U$。CLI verbalizer 回显前缀，抽出约束数字 82。 |
| C9 | 对照 §2.4 / §6 干预 | `timing=offline_hidden`；`donor_kind=same_source_diff_value`；INLP=`inlp`；`ie_z_g=target_follow`。有 dev 分数时四项主结局有数（本机 target=0，抽出 `'9'`）；无 dev 分数时相对对照 `None`。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 | 当前字节：T1 值编辑在；Plus/T4/HumanEval 仍 `needs_truth`。未把读取器当已测全量。 |
| C11 | 对照附录 S1–S4 | S3 PCA 在源码中。S4 仍 BOW。掩码仍改前缀字符串。 |
| C12 | 抽读测试是否固化替身 | 是：r05 只锁“有事件且含 q”；r06 锁生成区、字段名 `donor_kind`/`inlp`/`ie_z_g`，不锁拒绝 `constrained_target`，不锁 fit 读到 $E$ 序。 |
| C13 | 独立重算论文/协议/GOAL/REQUIREMENTS SHA-256 | 四份与账本 §0 一致。 |
| C14 | 独立重算声明代码冻结 hash | **开始 HASH_MATCH** `9ffc4cd9…`，60 文件。**交卷 HASH_MISMATCH**（见页眉）。 |
| C15 | 复跑 scientific prepare/collect/fit/calibrate/intervene/analyze | 见 §5。命令已在本审查重跑。 |
| C16 | `pytest tests/test_round05_regressions.py tests/test_round06_regressions.py -q --tb=line` | **24 passed**（前段）。不作为原文关闭。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 全量 `pytest -q` 作为本通道验收 | 原文符合性不由绿测关闭。作者声称 144 passed；本报告只声称指定两文件 24 passed。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量 500 题 | 协议 §7：科学结论 `pending_server`。tiny **不是** 该缺口的替代。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | 标签对象不是生成步骤上的 $R_{\mathrm{behavior}}$。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读 round-09 其他通道。 |
| N6 | `PAPER_TRACEABILITY.md` 全部 726 行逐字复读 | 已读约定与高风险可执行/GOAL/REQUIREMENTS 行。剩余多为同一模板重复。 |
| N7 | 真实隔离沙箱跑 HumanEval | 无合格隔离后端；`ChildProcessExecutor` 不能冒称沙箱。 |
| N8 | 在交卷树（61 文件 / `c29ad0dd…`）上重跑科学流水线 | 冻结已破；再跑不能认证声明 hash。后增 r07 测试未读作证据。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | 生成区/有限 $H$/Prefill/donor 接线在；事件是约束目标 | subst |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema 正确；scientific 的 $s_i$ 是 `\nq = 82` | subst |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | 比较对象是约束数字；本机 `behavior_label=None` | subst |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | id + aliases 词边界 | ok-lib |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap`；$\Pi=I$ 时得 donor | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ 用 $g(Y)$ | math | 字段 `ie_z_g=target_follow`；tiny 用抽出答案指示。$Y$ 不是生成步骤 | subst / 接线 ok |
| 论文 2.4 | 106–117 | 前瞻 hook / 四项 / 对照 | exec | hook 在；有 dev 分数时四项有数；无分数时 C-layer `None`；invalid/target 来自乱码 decode | subst |
| 论文 2.4 / 6 | 311 | INLP 正交移除，不是再做 $\Pi_Z$ | exec | `mode=inlp` → $h@P$；与主交换分离 | ok-lib（对象仍是约束步） |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | helper 跟 `task.premises`；scientific fit 列序不对 | subst / ok-lib |
| 论文 2.6 | 148–158 | $S,M,\rho$，噪声先扣 | math | 公式在；本机 $B$ 空 → $\rho_S$ 无行为正例（诚实） | ok-lib |
| 论文 4.1 | 232–253 | `T0=generate` 后 `parse_events(T0)` | exec | 解析生成区；对象是 teacher-force 目标行 | subst |
| 论文 4.2 | 257–267 | 步边界 $h_i$、双头、$e_j$ | exec | $h_i$ 对齐约束 `q`；行为头无已知 Y | subst |
| 论文 8.2 | 419–431 | `--eval-mode scientific` 自然轨迹 | exec | 开关在；后续标签/$H$/干预不是论文对象 | subst |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |
| REQUIREMENTS MODEL-01 | 11 | 冻结 Qwen3 / R1 HF | exec | 卡在 `adapters.py`；CLI 走 tiny 随机权重 | pending_server / **非缺陷** |

---

## 5. Findings

### A9-H1 — 交卷时声明冻结不可认证

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `.planning/audits/round-09/VERSION.md` 声明；工作树 `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml` |
| **Trigger** | GOAL 第七节：每轮审查必须钉在同一固定代码版本。r07 D 已因交卷前漂移报 HASH_MISMATCH。 |
| **Paper requirement** | 独立审查意见只能覆盖已声明并复算一致的字节。树一变，旧通过不能覆盖新代码。 |
| **Repro / evidence** | VERSION 原文脚本。开始：`len=60` / `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`。交卷前去掉后增 `test_round07_regressions.py`：`len=60` / `57b43360c354ede2caf4a99adae7a0b33c082ec534f675b295709890931427bd`。计入该文件：`len=61`，摘要在交卷窗口内从 `fea2565f…` 变为 `c29ad0dd4a1f5fd161fb3459433d7af4f5f9dd987d0120f800f0c545c106d124`。本通道未写生产文件。 |
| **Impact** | 不能宣布“已在 `9ffc4cd9…` 上连续通过”。作者对 D7-03/04/05 的关闭不能绑到声明冻结。 |
| **Suggested fix** | 停写生产/测试字节，重冻 VERSION，再开独立 A–F。不要在审查进行中改 60 文件集合。 |
| **Status** | **confirmed defect**（过程/冻结） |

### A9-01 — scientific 事件是约束目标行，不是 §4.1 生成步骤

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/generate.py` `append_target_assignment` 72–98、`generate_task_trace` 135–160；`cli.py` `cmd_prepare` 292–297 |
| **Trigger** | 论文 §4.1 L232–248：`T0=generate` 之后 `parse_events` 的对象是**生成轨迹**上的变量/表达式/版本/作用域。§2.1：$T$ 是模型生成序列的步骤离散化，$P$ 不是 $T$。§8.2：自然轨迹。r06/r08“题干预复述入事件”**已满足关闭条件，不得原样重开**。 |
| **Paper requirement** | 自然轨迹步骤事件；$R_{\mathrm{behavior}}$ 来自固定随机流下编辑后**对应步骤值**是否变化；$h_i$ 为这些步骤的步边界。无自然步骤时应拒绝 scientific 或标 `unimplemented`，不得把约束接口写成已测 §4.1。 |
| **Repro / evidence** | 独立 `generate_task_trace(seed=0)`：文本 `'p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82'`，`parse_status=constrained_target`，`parse_region=generated`，`target_assignment='\nq = 82'`，事件仅 `q=82`（`start=45≥prompt_len=36`）。`parse_events(question)` 仍能得到 `p1`/`p2`，scientific **不再**收录。`prepare --eval-mode scientific` + 六比例 + `--sham-opportunities 1` → exit 0，**7** 条轨迹（含 `trace-source`）**全部** `constrained_target`，各 1 个事件 `q`（82/53/82/82/82/82/53）。prepare **只拒** `parse_failed`，不拒 `constrained_target`。`test_scientific_prepare_emits_parseable_events` / `test_generated_events_exclude_prompt_assignments` 只锁“生成区、有 q、非节点真值拼接”。 |
| **Impact** | C1/C3 入口仍没有“生成步骤上的编辑响应”。TR-0125 标 `partial_local_scientific` 比全称诚实，但仍把该接口指向可执行覆盖。约束 `\nq = <digit>` 是本机可解析接口，**不是** §4.1 自然 CoT。干预里 `g(Y)` 比较的是 4-token 乱码抽出的 `'9'` 与 donor 约束答案 `82`，不是新生成 $s_k$ 的来源跟随。 |
| **Suggested fix** | 只把自然 decode（或官方 CoT）解析为事件。`constrained_target` 时 scientific prepare/label/collect/intervene 拒绝或降级账本。不要 teacher-force 赋值行来凑事件。 |
| **Status** | **confirmed defect**；真实 CoT 质量 **pending_server** |

### A9-02 — $R_{\mathrm{behavior}}$ 比较的是约束数字，不是生成步骤值

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` `_observations` 229–254；`measure.py` `build_labels` 29–53；`generate.py` 72–98 |
| **Trigger** | 论文 §2.2 L74–78：固定 $M,u$ 下 $v_i(P\oplus\delta(p_j))\ne v_i(P)$。GOAL §5.3：值变/有限扫描未变/未扫描分开。事件定义见 A9-01。 |
| **Paper requirement** | 行为标签来自对齐生成步骤的语义值变化。未知不作负。不得把提示词改写后的约束采样数字当作步骤响应。 |
| **Repro / evidence** | 本机 observations：`(q,p2)` `82→82` `no_change`；`(q,p1)` `82→82` `no_change`；重复 p2 编辑仍 `82→82`；sham `82→53` `changed`（`premise_id=sham:q`）。labels：`(q,p2)`/`(q,p1)` `task_label=1`，`behavior_label=None`，`behavior_known=False`。scientific `fit` 只写出 **task** 头 `U`（loss `0.05036`）；行为头 `no_known_labels`。 |
| **Impact** | 差集 $S$ 在本机没有行为正例，不是“编辑后步骤值是否跟随前提”。即使将来约束数字因提示词改写而变化，那也是 teacher-force 采样对前缀的敏感，不是 §2.2 的 $v(s_i)$。 |
| **Suggested fix** | 先关闭 A9-01。无生成步骤则不写行为标签，保持 `unknown`。 |
| **Status** | **confirmed defect** |

### A9-03 — C6-M-01：helper 跟 $E$ 列；scientific fit 仍用 labels 首次出现序

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `_e_premise_ids` 671–680；`cmd_fit` 608–615 |
| **Trigger** | 论文 §2.5 L132–134：$a(X)=\max_{j\in R(s_i)}(1-\hat p_{ij})$，列 $j$ 是原始前提（与 $E$ 同行）。r06/r08 C6-M-01：`unique` 用 labels 首次出现序。`test_truth_indices_follow_e_columns_not_label_order` **只测 helper**。 |
| **Paper requirement** | `predict_matrix` 列 = $E$ 行 = `task.premises` 序。不得用 labels 首次出现序。读不到任务应拒绝。 |
| **Repro / evidence** | scientific 标准路径：`fit --in-dir col --labels-dir lab` 两处都 **没有** `tasks.jsonl`。本机 labels 首次出现 `[p2, p1]`（`_default_edit` 先改零值 p2），`_e_premise_ids(None, labels)=[p2, p1]`，而 $E$ 行是 `[p1, p2]`。`_e_premise_ids(task, labels)=[p1, p2]`。无任务 calibrate 手造 $H$：`scores=[0.0]`（`rsi={s1}` 当空真集），不是旧的 0.2，但是错的。有任务的 0.1 反例在 helper 层关闭，本轮未再造合法三前提 `tasks.jsonl` CLI（手造 span 校验失败，不升格为新缺陷）。 |
| **Impact** | C6-M-01 的 **0.2 反例在 helper / 任务文件可见时关闭**，不得原样重开。默认 scientific fit 仍把 $Y$ 的 p2 写到 $E$ 的 p1 列。 |
| **Suggested fix** | fit/calibrate 必须从 prepare 产物或 `--in-dir` 祖先读取 `tasks.jsonl`；读不到则拒绝，禁止回退 labels 序。 |
| **Status** | **confirmed defect**（scientific fit / 无任务 calibrate）；helper 与有任务列序 **本轮不重开** |

### A9-04 — 账本可执行行仍大量 `implemented_local`（pytest 关闭可执行行不重开）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` TR-0158、TR-0400、TR-0125；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：未实现不得标已实现。r06 可执行行验证列已改 `tests_exist_not_acceptance`，**不得**按 A5-02 原文重开。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。 |
| **Repro / evidence** | 726 行 / 528 TR。TR-0125 `partial_local_scientific`、TR-0135 `partial_local_tiny`。TR-0158 / TR-0400（解耦任务构造）仍指向 `intervention_report` 且 `implemented_local`。协议/标题行仍 **70** 处 `python -m pytest -q`。REQUIREMENTS 复选框全空，状态表写 `implemented_local`。 |
| **Impact** | 覆盖率仍被制成 16/16。独立审查若信 `implemented_local` 会漏检 A9-01。 |
| **Suggested fix** | 未接到论文语义的可执行行改为 `unimplemented` / `ok-lib_unwired` / 保持 `partial_*`。 |
| **Status** | **confirmed defect**（过称）；pytest-关闭可执行行 **本轮不重开** |

### A9-05 — CLI 四档 verbalizer 回显前缀，把约束数字当成自述命中

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_fit` 650–655；`baselines.py` 92–125 |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7。子串打分 **不得重开**（库层 `17` 为 0）。 |
| **Paper requirement** | 四档自述与探针同样本/划分/可见前缀。 |
| **Repro / evidence** | 库：`verbalizer(..., generate_fn=λ:"17")` 对金标 `7` 得 0。CLI `generate_fn=lambda p, t=prefix: t`。scientific fit：zeroshot/fiveshot/reflection `score=1.0`，`extracted='82'`（回显整段轨迹，抽出约束赋值）。supervised 拒未训练。BoundaryMLP：`note=event-rows-only_no_negatives`。 |
| **Impact** | 第 8 节“说不出来”在 CLI 上仍不是同划分模型自述。 |
| **Suggested fix** | CLI 按同一划分调用真实生成；未接线不得标 `implemented_local`。 |
| **Status** | **confirmed defect**（CLI 替身）；子串打分 **本轮不重开** |

### A9-N1 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 215–257；`cli.py` `cmd_analyze` |
| **Trigger** | 协议 §6；GOAL §5.14。任务：Gate 0–2 未注册 **不是** 缺陷。 |
| **Paper requirement** | 用户未给阈值则不得编造 pass/fail。不得把 fixture 写入科学结论。 |
| **Repro / evidence** | scientific analyze（`--in-dir lab`）：`gates.*.decision=unregistered`，`scientific_conclusion=None`，`p1=None`，`skip_p2_p3=True`。`week8_decision({rho_S_excess:0})` → `c3_negative_descriptive`。有阈值无度量 → `threshold_present_measurement_missing`。 |
| **Impact** | 正确持守。假说不要求正结果，本条不升格。 |
| **Suggested fix** | 不要添加阈值。 |
| **Status** | **non-defect** |

### A9-N2 — tiny 随机权重不是 MODEL-01（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `models/tiny.py`；`models/adapters.py`；`models/generate.py` metadata `weight_source` |
| **Trigger** | REQUIREMENTS MODEL-01：冻结 Qwen3 / R1 HF。任务：tiny **不是** MODEL-01。 |
| **Paper requirement** | 真实权重/revision 在服务器验证。本机微型随机模型只证明接口。 |
| **Repro / evidence** | 全部 scientific 轨迹 `model=tiny-qwen2`，`weight_source=random_init`。collect `run_spec.weight_source=random_init`，`hidden_layer=1`。`adapters.MODELS` 有冻结 revision，CLI 不 `from_pretrained`。 |
| **Impact** | 把 tiny 绿测写成 MODEL-01 才是缺陷；本通道不把“没有真实权重”判为代码缺陷。 |
| **Suggested fix** | 保持 `pending_server_weights`。不要把 tiny 标成已测论文模型。 |
| **Status** | **non-defect** |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5，也不能认证已漂的冻结。

1. **Gate 0–2**：无阈值、无 pass/fail（A9-N1）。
2. **`scientific_conclusion` 保持 `None`**。
3. **tiny 不是 MODEL-01**（A9-N2）。
4. **REST-01/02/03** 禁词列表存在；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
5. **身份对齐不含值**。
6. **$R_{\mathrm{task}}$ 祖先**、**$S/M$ 空分母→null**、**缺/空 sham→excess null**、**`sham:` 命中不把空 $N$ 记成已评估 0**。
7. **交换公式** $H^b+\Pi_Z(H^d-H^b)$ 在 $\Pi=I$ 时得 donor。几何报告 **不**写 `timing=pre_step`。
8. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$。`[0.1,0.2,0.3,0.4], α=0.4` → $q=0.3$；$\alpha=0.1$ → $+\infty$。
9. **4096 vs 3584 直接迁移 N/A**。
10. **官方 iGSM 快照拒裸 `G`、排除共享 RNG、mod 23**；夹具拒绝 `official`。
11. **宿主 exec 被禁止**；`ChildProcessExecutor` 不冒称沙箱。
12. **假说不要求正结果**：本通道不因无 F1/AUC 正数判失败。
13. **P1 留出路径为 IRLS logistic**；bootstrap **重算** $\Delta\mathrm{AUC}$。
14. **scientific 调用模型 generate**，不是节点真值轨迹；题干前提赋值不再当作生成事件。
15. **tiny $E$ 为读出层 span 均值**，行不相同；scientific 拒 offline $H$。
16. **scientific $H$ 有限**，行数=可表达事件；不可表达步前不入 $H$。
17. **`source_value_pair` 写入 `edits.jsonl`**，并生成 `trace-source`。
18. **donor 优先 `same_source_diff_value`（`trace-base`/`trace-edit`）**；本机配对 `(0,2)`。
19. **INLP decode 是 `inlp`（$h@P$），不是再跑 `pi_z_swap`**；C-rand/`add_delta`、rescue/`replace` 分路。
20. **`ie_z_g=target_follow`**（字段；对象仍受 A9-01 限制）。
21. **有 `task` 时 `_e_premise_ids` 跟前提序**（C6 的 0.2 helper 反例关闭）。
22. **verbalizer 抽答案**：`17` 不再当子串命中。
23. **可执行行不再用 pytest 关闭**（`tests_exist_not_acceptance`）。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_scientific_prepare_emits_parseable_events` | 每条轨迹 ≥1 事件且含 `q`；无节点真值拼接 | 事件是生成步骤；拒绝 `constrained_target` |
| `test_generated_events_exclude_prompt_assignments` | 事件 `start≥prompt`；`parse_region=generated` | 非 teacher-force 目标行 |
| `test_scientific_h_is_finite_and_pairs_donor` | $H$ 有限；`donor_kind`/`inlp_transform`/`ie_z_g` 字段；`timing≠pre_step` | $H$ 对应自然步；$R_{\mathrm{behavior}}$；$\mathrm{IE}_Z$ 的 $g$ 是来源跟随 |
| `test_truth_indices_follow_e_columns_not_label_order` | `_e_premise_ids(task, …)` 跟前提序 | `cmd_fit` 在无 `tasks.jsonl` 时的列身份 |
| `test_verbalizer_uses_extracted_answer_not_substring` | `17`/`70`/`boxed` 不子串命中 | 同划分四档模型自述 |
| `test_full_cli_smoke` | 八阶段返回 0；**offline** $H$ | generate、论文步边界、干预生成 |

---

## 8. 本审查复跑的命令（均可再跑；树已漂则结果不能认证声明 hash）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → 开始 **60** / `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`；交卷前不含 r07 测试 **60** / `57b43360…`；含 r07 **61** / `c29ad0dd…`。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `python -m pytest tests/test_round05_regressions.py tests/test_round06_regressions.py -q --tb=line` → **24 passed**（前段）。
4. `generate_task_trace` + `prepare --eval-mode scientific` → 7 条 tiny 轨迹，全部 `constrained_target`，各 1 个 `q` 事件，题干前提不入事件；含 `trace-source`；`source_value_pair` 在 `edits.jsonl`。
5. `collect --backend tiny --weight-seed 0` → $H=(7,32)$ 全有限，行=事件，$E$ 行不同，`hidden_layer=1`。`_pair_source_value` → `(0, 2, same_source_diff_value)`。
6. `fit`：task 头有限 $U$；行为头无已知标签；verbalizer 回显前缀抽出 `82`。`_e_premise_ids(None, labels)=[p2,p1]` ≠ $E$ 序。
7. `calibrate` 写出有限 $q$；手造无任务 `scores=[0.0]`。
8. `intervene --dev-layer-scores 0.05 0.9 0.8` → `timing=offline_hidden`，`donor_kind=same_source_diff_value`，`inlp_transform=inlp`，`ie_z_g=target_follow`，`ie_z=0.0`，`weak_layer=0`，主/对照抽出 `'9'`。无 dev 分数：`clayer_status=dev_scores_missing`，相对对照 `None`。
9. `analyze` → `p1=None`，`scientific_conclusion=None`，Gate `unregistered`。
10. 库微例：`conformal_threshold` / `apply_swap` / `verbalizer` / `week8_decision`：见 §5–§6。

---

## 9. 结论

**冻结 hash：审查开始 HASH_MATCH `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（60 文件）；交卷 HASH_MISMATCH（60 文件已变为 `57b43360…`，并出现第 61 个测试文件）。**

**原文一致性：不通过（FAIL）。**

r08/r07 猎点中的“生成区而非题干预复述 / 有限步前 $H$ / `source_value_pair` 落盘 / 几何不写 `pre_step` / donor=`same_source_diff_value` / INLP=`inlp` 而非 `pi_z_swap` / `ie_z_g=target_follow`”，本通道在**中段复跑**上见到字段与配对，**不得把这些接线项当作新缺陷原样重开**。它们也**不能**在声明冻结上关闭：交卷树已变。科学入口仍在 **约束目标** 处断开：`parse_status=constrained_target` 被当作 §4.1 成功，于是 $R_{\mathrm{behavior}}$ 与 $\mathrm{IE}_Z$ 的 $g(Y)$ 比较的都不是生成步骤。C6-M-01 在 helper 上关闭，在默认 scientific fit 上仍用 labels 首次出现序。Gate 0–2 未注册、tiny 不是 MODEL-01、假说不要求正结果——这三条被遵守。作者关闭与绿测不能关闭本通道。真实权重/官方全量是 `pending_server`，不能解释本机把约束赋值写成 $T$。

独立复审关闭条件（本通道）：先重冻并在**同一 hash** 上再开 A–F；A9-01 与 A9-02 必须对照原文关闭（scientific 事件来自生成步骤，或对 `constrained_target` 诚实拒绝并降级账本）；A9-03 须让 scientific fit 的 Y 列与 $E$/`task.premises` 一致，读不到任务则拒绝。其余 medium 项至少改为诚实状态。A9-H1 关闭条件是 VERSION 与磁盘复算一致且审查期间不变。

**不把 Goal 标为完成。**
