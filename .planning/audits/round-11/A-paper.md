# 审查报告 A：原文一致性（paper consistency）— round-11

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-11 |
| **审查时间** | 2026-09-21 02:26 起（UTC+8） |
| **声明冻结 hash** | `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`（61 files） |
| **hash 方法（声明）** | SHA-256 over POSIX 相对路径 + `\x00` + 文件字节；`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__` |
| **本审查实测代码 hash** | **开始 HASH_MATCH。** 按 `VERSION.md` 原文 Python 逐字复算：文件数 **61**，摘要 `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`。**交卷 HASH_MISMATCH。** 同脚本在审查中途依次为 `929aa472…`、`4da0b2bd…`、`598e6c8f…`；写完本文件后再算为 61 文件 / `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。本通道未改 `src/`、`tests/`、`pyproject.toml`。Mismatch → 本通道 **FAIL**。 |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与账本 §0 一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `39CF907C0B66B9B26AE7355E394848CFA1FF41CE5166310E1DC0A9307F9AC498`（与账本 §0 一致） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读全文件以定位 §5）；`.planning/REQUIREMENTS.md`；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/GOAL/REQUIREMENTS 行抽样；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读** `.planning/audits/round-11/` 下除 `VERSION.md` 与本文件外的任何通道报告。**未把** `ISSUES.md` 作者关闭当作关闭。指定猎点：teacher-force 冒充 §4.1；Gate `unregistered` 冒充 pass；sham 广播冒充已扣噪声。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |
| **作者声称 pytest** | VERSION 写 155 passed。本通道在开始 MATCH 窗口独立复跑 `pytest -q` → **155 passed**。绿测不关闭原文符合性，也不认证已漂的树。 |

**总判：不通过（FAIL）。** 声明冻结在审查**开始**可核验，**交卷时不能认证**（A11-H1）。相对先前接线，MATCH 窗口独立复跑后**不得原样重开**：scientific 事件在生成区；`source_value_pair` 落盘且 `trace_ids` 指向 `trace-edit`/`trace-source`；collect 复制 `tasks.jsonl`，fit 有任务时 Y 列跟 `[p1,p2]`；scientific $H$ 有限且行=事件；Gate 保持 `unregistered`；**sham 命中不再广播进真实前提，也未写出 `rho_M_excess=1.0` from $N=\{p1,p2\}$**。

本轮仍 FAIL，缺一即不通过：

1. **冻结完整性：** 交卷树已从 `7518e20b…` 漂到 `598e6c8f…`。对声明 hash 的通过意见不能交给漂移树。
2. **原文语义（MATCH 窗口复跑）：** scientific 仍把 teacher-force `\nq = <两位数字>` 标成 `parse_status=constrained_target` 后**当作 §4.1 成功事件**。7 条轨迹各只有 `q`；随机 decode 段不可解析。$R_{\mathrm{behavior}}$ 比较的是约束数字是否变化（本机编辑后 82→82，`behavior_label=None`），不是固定随机流下生成步骤值。

Gate 0–2 保持 `unregistered`，**不是缺陷**，也**不是 pass**。tiny 随机权重 **不是** MODEL-01。假说不要求正结果。不把 Goal 标为完成。

---

## 0. 相对上一轮树的诚实变化（避免把已修项当新缺陷）

独立重读 MATCH 窗口字节并复跑后，下列 **不再** 作为本轮 confirmed defect 原样重开（不等于科学语义已齐；且交卷树 ≠ 声明冻结）：

| 先前问题 | 本审查复跑（开始 MATCH 窗口） |
|---|---|
| 题干 `p1 = 4` / `p2 = 0` 被收成生成事件 | `parse_events` 吃 `gen_text+assigned`；7 条轨迹事件均 `start≥prompt_len`，节点只有 `q`。题干单独解析仍能得到 `p1`/`p2`，**不再**写入 scientific 事件。 |
| 零事件 / 节点真值拼接 | 文本 `'…?Z*H[!XTC\nq = 82'`，`model=tiny-qwen2`，`generation=decode_loop`。**不是** `p1 = 4 \| p2 = 0 \| q = 0`。 |
| $H$ 含 NaN / 末 token 冒称 `pre_step` | scientific collect：$H=(7,32)$ **全有限**，`event_rows=7` 全为 `q`，`hidden_layer=1`，$E=(2,32)$ 行不同。 |
| `source_value_pair` 未落盘 / donor 不是来源—数值臂 | `edits.jsonl` 含 `kind=source_value_pair`；`trace_ids.same_source_diff_value=trace-edit`，`same_value_diff_source=trace-source`。 |
| C6-M-01：scientific fit 默认读不到 `tasks.jsonl` | collect **复制** `tasks.jsonl`；`_find_tasks_jsonl(col, lab)` 命中 collect 副本；`_e_premise_ids(task, labels)=[p1, p2]`。无任务时仍为 labels 首次出现序 `[p2, p1]`——**默认 scientific collect→fit 路径本轮不重开**。 |
| **B9-01：sham 广播 → $N=\{p1,p2\}$ → `rho_M_excess=1.0`** | `build_labels` 只把 `noise_ref=1.0` 写在 `sham:q`；`(q,p1)`/`(q,p2)` 的 `noise_ref=None`。`event_density_sets` 见 `sham:` hit → `noise_set=None`，`null_reason=noise_set_missing`，**`rho_M_excess=None`**。不是已映射 $N=\{p1,p2\}$ 后的扣除。**本轮不重开 B9-01。** |
| Gate 未注册 / tiny=MODEL-01 | **不是缺陷**（见 A11-N1 / A11-N2）。也不得把 `unregistered` 写成 pass。 |

**未关闭：** §4.1 的解析对象仍是约束目标行，不是自然生成步骤；由此 $R_{\mathrm{behavior}}$ 与 $\mathrm{IE}_Z$ 的 $g(Y)$ 都不是论文对象。未知行为被当成空 $B$，写出 `rho_M_raw=1.0`（与 B9-01 的 excess=1.0 **不是同一条**）。声明冻结在交卷时已失效。

---

## 1. 逐文件覆盖

每行：路径（磁盘 `splitlines()` 行数，MATCH 窗口读数；交卷树可能已变）— 对照条款 — 结论。行为结论以 MATCH 窗口复跑为准。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 1–517 | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 1–86 | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。Gate 保持 null 与代码一致。噪声“未注册配对不得强加前提身份”与 MATCH 窗口 sham 处理一致。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 1–166；§5 = 73–91 | GOAL §5.1–5.15 | 第 3、6–8、10–13 条在科学入口仍被约束目标降级。第 14、15 条持守。 |
| `.planning/REQUIREMENTS.md` | 1–76 | DATA/MEAS/MODEL/PROBE/… 与 atomics | 复选框全空；状态表仍写 `implemented_local`。MODEL-01 写成 `implemented_local_tiny`——tiny 不能关 MODEL-01。 |
| `.planning/PAPER_TRACEABILITY.md` | 1–50 约定；75–120、202–243、370–420 抽样 | 账本不得当实现证据 | 728 行 / 528 TR 行。`implemented_local` 478 处；仅 TR-0125 / TR-0135 为 `partial_*`。协议/标题行仍约 70 处 `python -m pytest -q`。 |
| `pyproject.toml` | 1–27 | §8.1；GOAL §5.15 | 默认只 `numpy`。`optional-dependencies.models` 有 `torch`/`transformers`。无强制 scientific 栈。 |
| `src/reasoning_diff/__init__.py` | 1–5 | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 1–4 | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 1–385 | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 1–46 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先与相交掩码正确。默认 cone 走任务祖先。 |
| `src/reasoning_diff/events.py` | 1–274 | §2.2–2.3；$R^{\mathrm{surf}}$；§4.1 对齐 | `parse_events` 仍把前提与节点都当赋值模式。scientific 调用方把文本限制在生成区。策略仍只读 `status=="strategy_change"`。 |
| `src/reasoning_diff/edits.py` | 1–287 | §7 T1 重算；GOAL §5.2 | 值编辑+表达式重算正确。`make_source_value_pair` 有同值异源；改名改写 id/expression/parents。 |
| `src/reasoning_diff/measure.py` | 1–392 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集、空分母、缺/空 sham→null、signed excess 正确。`noise_ref` **只写 `sham:` 行**。`event_density_sets` 见 `sham:` hit 则 $N$ missing。未知 $B$ 仍当空集 → `rho_M_raw=1.0`。 |
| `src/reasoning_diff/analysis.py` | 1–337 | §2.6 P1–P3；§7 分流；附录 S2–S4 | P1 留出 logistic + 偏相关。bootstrap 重算 $\Delta\mathrm{AUC}$。无阈值 → Gate `unregistered`，`scientific_conclusion=None`。`retrieval_scatter` 无嵌入则 BOW。 |
| `src/reasoning_diff/interventions.py` | 1–115 | §2.4 交换/对照/INLP/救援/$\mathrm{IE}_Z$ | 交换式、范数匹配、`ie_z`、`select_weak_layer` 库层正确。无 `--dev-layer-scores` 时相对 C-layer 为 `None`（诚实缺失）。 |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE、未知/NaN 掩码正确。CLI tiny 维 32 故 `rank=min(64,d)`。 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | §4.2 Hidden=256 ReLU | 架构+`fit` 符合。CLI 用全 1 标签、无负例。 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | §2.5 命题 2 | 分位数与 $+\infty$ 正确。`truth_indices` 可限制到指定列。 |
| `src/reasoning_diff/probes/__init__.py` | 1–3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 1–125 | §8 文本/注意力/四档自述；GOAL §5.7 | 监督 BOW。verbalizer 走 `extract_answer`。CLI `generate_fn` 回显前缀。 |
| `src/reasoning_diff/transfer.py` | 1–86 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。`common_dim_then_procrustes` 先 PCA 再 Procrustes；$n<d$ 标 `truncated`。 |
| `src/reasoning_diff/repair.py` | 1–232 | §3 Repairability/RR；§9 嫁接；GOAL §5.13 | `execute_repair_tiny` 真 Prefill+hidden。标量/`size<2` Prefill 被拒。掩码仍改前缀字符串。 |
| `src/reasoning_diff/cli.py` | 1–1254 | §4 流水线；§8.2 scientific | scientific prepare 拒 `parse_failed`，**接受** `constrained_target`。collect 拒 offline $H$、复制 `tasks.jsonl`。fit/calibrate 经 `_find_tasks_jsonl`。analyze 无 `p1_table` 不伪造 P1。 |
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
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–85 | §7 T2；GOAL §5.2 | 无侧车：placeholder + `graph_status=unknown`，拒编辑。有侧车：值编辑+算子逆转。写入 `shared_gsm_family`。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–84 | §7 T2；评测专用 | test-only 锁 + `register_test_only_family`。孤立数字替换成立；答案 `needs_truth`/`None`。 |
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
| `tests/conftest.py` | 夹具路径 | — | 只读。 |
| `tests/test_cli_pipeline.py` | 八阶段 | §4 流水线 | 仍强制 `--backend offline`。 |
| `tests/test_science.py` | 库微例 | 校准/迁移/交换/Week-8 | 不锁 §4.1 自然步骤。 |
| `tests/test_measure.py` | $S/M$ | 联合编辑反例 | 与公式一致。 |
| `tests/test_review_regressions.py` | 上轮回归 | 锁住若干库修补 | 含 sham `noise_ref` 不广播到真实前提。 |
| `tests/test_round03_regressions.py` | r03 | 仍锁 `precomputed_scores` | — |
| `tests/test_round04_regressions.py` | r04 | generate≠节点真值、span $E$、几何≠`pre_step`、Prefill | — |
| `tests/test_round05_regressions.py` | r05 | 锁事件非空、H 行数、抽答案 | **不**锁事件是生成步骤。 |
| `tests/test_round06_regressions.py` | r06 | 锁生成区、有限 $H$、helper 列序、donor/inlp/ie_z 字段 | **不**锁拒绝 `constrained_target`。 |
| `tests/test_round07_regressions.py` | r07 | 锁 sham 不广播；CLI 弱析取 `rho_M_excess != 1.0 or null_reason` | **不**锁拒绝 teacher-force。 |
| `tests/test_tracer_t1_prepare.py` | T1 夹具 | 身份/重算/空分母 | — |
| `tests/test_t1_official.py` | template≠G | 快照形状 | — |
| `tests/test_t2_gsm.py` | T2 | 侧车数值编辑 | — |
| `tests/test_t3_t4.py` | T3/T4 | supporting_facts ≠ DAG | — |
| `tests/test_artifacts.py` | I/O | 工程 | — |
| `tests/test_generate_loop.py` | 可重放采样 | tiny decode | — |
| `tests/test_tiny_hooks.py` | hook 清理 | 本机接口 | — |
| `tests/test_tiny_cache.py` | 缓存隔离 | `intervene_tiny` 断言 logits 因 $\Pi_Z$ 改变 | — |

第三方库：审查了本项目对 `numpy` / 可选 `torch`+`transformers` 的使用假设，未审查依赖源码。

夹具抽读：`tests/fixtures/t1_tiny.json`（全文）。$R_{\mathrm{task}}(q)=\{p1,p2\}$，金标答案 `0`。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献清单 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` | 完成。Gate 保持 null（非缺陷）。§2.6 噪声不得强加前提身份——MATCH 窗口 sham 路径遵守。 |
| C3 | 通读 GOAL §5 十五条 | 完成。第 3 条（事件与行为）在科学入口被约束目标替换。第 14 条 Gate 未注册无 pass/fail——遵守。 |
| C4 | 阅读 `PAPER_TRACEABILITY.md` 约定，抽样 TR-0001–0043、TR-0125–0137、TR-0158、TR-0400 | TR-0125 仍 `partial_local_scientific`。TR-0158/0400 仍 `implemented_local`。478 处 `implemented_local`。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。开始时 61 文件清单与 VERSION 一致。 |
| C6 | 对照公式手核 + 复跑：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1、cone | 库函数层：$R_{\mathrm{task}}$/差集/交换/分位数/拒维度 **符合**。`apply_swap` 在 $\Pi=I$ 得 donor。`conformal_threshold([0.1,0.2,0.3,0.4],0.4)→q=0.3`；$\alpha=0.1$ → $+\infty$。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | generate 在；解析区=生成段；**事件来自 teacher-force 目标行**，`constrained_target` 被接受。另生成 `trace-source`。 |
| C8 | 对照 §4.2 / §8 探针与基线 | $H$ 有限、行=事件、层=1、$E$ 行不同。行为头因无已知标签未写出 $U$。CLI verbalizer 回显前缀，抽出约束数字 82。 |
| C9 | 对照 §2.4 / §6 干预 | 代码接线仍在（donor/`inlp`/`ie_z_g`）。本通道本轮以 prepare/密度/Gate 为指定猎点，未再跑 intervene decode。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 | T1 值编辑在；Plus/T4/HumanEval 仍 `needs_truth`。未把读取器当已测全量。 |
| C11 | 对照附录 S1–S4 | S3 PCA 在源码中；$n<d$ 标 truncated。S4 仍 BOW。掩码仍改前缀字符串。 |
| C12 | 抽读测试是否固化替身 | 是：r05 只锁“有事件且含 q”；r06 锁生成区与字段名；r07 锁 sham 不广播，CLI 密度用弱析取 `!= 1.0 or null_reason`。**全仓库测试字符串不含 `constrained_target`。** |
| C13 | 独立重算论文/协议/GOAL/REQUIREMENTS SHA-256 | 四份与账本 §0 一致。 |
| C14 | 独立重算声明代码冻结 hash | **开始 HASH_MATCH** `7518e20b…`，61 文件。**交卷 HASH_MISMATCH** `598e6c8f…`（见页眉）。 |
| C15 | 复跑 scientific prepare `--sham-opportunities 1`；inspect densities；label/collect/fit/analyze | 见 §5。MATCH 窗口命令。 |
| C16 | `pytest -q` | **155 passed**（MATCH 窗口）。不作为原文关闭。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | 把全量绿测当作原文验收 | 原文符合性不由绿测关闭。本报告只声称 MATCH 窗口 155 passed。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量 500 题 | 协议 §7：科学结论 `pending_server`。tiny **不是** 该缺口的替代。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | 标签对象不是生成步骤上的 $R_{\mathrm{behavior}}$。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读 round-11 其他通道。 |
| N6 | `PAPER_TRACEABILITY.md` 全部 728 行逐字复读 | 已读约定与高风险可执行/GOAL/REQUIREMENTS 行。剩余多为同一模板重复。 |
| N7 | 真实隔离沙箱跑 HumanEval | 无合格隔离后端；`ChildProcessExecutor` 不能冒称沙箱。 |
| N8 | 在交卷漂移树上重跑科学流水线 | 冻结已破；再跑不能认证声明 hash。 |
| N9 | 本通道本轮未重跑 intervene decode | 指定猎点是 §4.1 / Gate / sham 密度。接线字段以上轮不得重开项对待，不以本轮未跑而新开。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | 生成区/有限 $H$/Prefill/donor 接线在；事件是约束目标 | subst |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema 正确；scientific 的 $s_i$ 是 `\nq = 82` | subst |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors`；$q\mapsto\{p1,p2\}$ | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | 比较对象是约束数字；本机 `behavior_label=None` | subst |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | id + aliases 词边界 | ok-lib |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap`；$\Pi=I$ 时得 donor | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ 用 $g(Y)$ | math | 字段 `ie_z_g=target_follow`。$Y$ 不是生成步骤 | subst / 接线 ok |
| 论文 2.4 / 6 | 311 | INLP 正交移除，不是再做 $\Pi_Z$ | exec | `mode=inlp` → $h@P$；与主交换分离 | ok-lib（对象仍是约束步） |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | helper 跟 `task.premises`；collect 复制任务后 fit 列序对齐 | ok-lib / 默认路径关闭 |
| 论文 2.6 | 148–158 | $S,M,\rho$，噪声先扣 | math | sham 不再写入真实 $N$；excess null。`rho_M_raw=1.0` 来自空 $B$（未知当漏读） | ok-lib（N） / subst（raw M） |
| 论文 4.1 | 232–253 | `T0=generate` 后 `parse_events(T0)` | exec | 解析生成区；对象是 teacher-force 目标行 | subst |
| 论文 4.2 | 257–267 | 步边界 $h_i$、双头、$e_j$ | exec | $h_i$ 对齐约束 `q`；行为头无已知 Y | subst |
| 论文 8.2 | 419–431 | `--eval-mode scientific` 自然轨迹 | exec | 开关在；后续标签/$H$/干预不是论文对象 | subst |
| 协议 §2.6 | 25–26 | 未注册配对不得强加前提身份 | proto | sham hit → $N$ missing，不广播 $p1/p2$ | **ok**（MATCH 窗口） |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 / 不是 pass | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |
| REQUIREMENTS MODEL-01 | 11 | 冻结 Qwen3 / R1 HF | exec | 卡在 `adapters.py`；CLI 走 tiny 随机权重 | pending_server / **非缺陷** |

---

## 5. Findings

### A11-H1 — 交卷时声明冻结不可认证

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `.planning/audits/round-11/VERSION.md` 声明；工作树 `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml` |
| **Trigger** | GOAL 第七节：每轮审查必须钉在同一固定代码版本。任务：Mismatch → FAIL。 |
| **Paper requirement** | 独立审查意见只能覆盖已声明并复算一致的字节。树一变，旧通过不能覆盖新代码。 |
| **Repro / evidence** | VERSION 原文脚本。开始：`len=61` / `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`。审查中途同脚本：`929aa472…`、`4da0b2bd…`、`598e6c8f…`。写完本文件后再算：`0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。本通道未写生产文件。 |
| **Impact** | 不能宣布“已在 `7518e20b…` 上连续通过”。MATCH 窗口的语义结论不能自动覆盖交卷树。 |
| **Suggested fix** | 停写生产/测试字节，重冻 VERSION，再开独立 A–F。不要在审查进行中改 61 文件集合。 |
| **Status** | **confirmed defect**（过程/冻结） |

### A11-01 — scientific 事件是约束目标行，不是 §4.1 生成步骤

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/generate.py` `append_target_assignment` 72–98、`generate_task_trace` 135–160；`cli.py` `cmd_prepare` 296–297 |
| **Trigger** | 论文 §4.1 L232–248：`T0=generate` 之后 `parse_events` 的对象是**生成轨迹**上的变量/表达式/版本/作用域。§2.1：$T$ 是模型生成序列的步骤离散化，$P$ 不是 $T$。§8.2：自然轨迹。指定猎点：teacher-force 冒充 §4.1。 |
| **Paper requirement** | 自然轨迹步骤事件；$R_{\mathrm{behavior}}$ 来自固定随机流下编辑后**对应步骤值**是否变化；$h_i$ 为这些步骤的步边界。无自然步骤时应拒绝 scientific 或标 `unimplemented`，不得把约束接口写成已测 §4.1。 |
| **Repro / evidence** | MATCH 窗口独立 `generate_task_trace(seed=0)`：文本 `'p1 = 4. p2 = 0. What is q = p1 * p2?Z*H[!XTC\nq = 82'`，`parse_status=constrained_target`，`parse_region=generated`，`target_assignment='\nq = 82'`，事件仅 `q=82`（`start=45≥prompt_len=36`）。`parse_events(question)` 仍能得到 `p1`/`p2`，scientific **不再**收录。`prepare --eval-mode scientific` + 六比例 + `--sham-opportunities 1` → exit 0，**7** 条轨迹（含 `trace-source`、`trace-sham`）**全部** `constrained_target`，各 1 个事件 `q`（82/53/82/82/82/82/53）。prepare **只拒** `parse_failed`，不拒 `constrained_target`。全仓库 `tests/**` **零处**出现 `constrained_target`。 |
| **Impact** | C1/C3 入口仍没有“生成步骤上的编辑响应”。TR-0125 标 `partial_local_scientific` 比全称诚实，但仍把该接口指向可执行覆盖。约束 `\nq = <digit>` 是本机可解析接口，**不是** §4.1 自然 CoT。 |
| **Suggested fix** | 只把自然 decode（或官方 CoT）解析为事件。`constrained_target` 时 scientific prepare/label/collect/intervene 拒绝或降级账本。不要 teacher-force 赋值行来凑事件。 |
| **Status** | **confirmed defect**（MATCH 窗口）；真实 CoT 质量 **pending_server**。交卷树未再认证。 |

### A11-02 — $R_{\mathrm{behavior}}$ 比较的是约束数字，不是生成步骤值

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` `_observations` 229–254；`measure.py` `build_labels` 29–53；`generate.py` 72–98 |
| **Trigger** | 论文 §2.2 L74–78：固定 $M,u$ 下 $v_i(P\oplus\delta(p_j))\ne v_i(P)$。GOAL §5.3：值变/有限扫描未变/未扫描分开。事件定义见 A11-01。 |
| **Paper requirement** | 行为标签来自对齐生成步骤的语义值变化。未知不作负。不得把提示词改写后的约束采样数字当作步骤响应。 |
| **Repro / evidence** | MATCH 窗口 observations：`(q,p2)` `82→82` `no_change`；`(q,p1)` `82→82` `no_change`；重复 p2 编辑仍 `82→82`；sham `82→53` `changed`（`premise_id=sham:q`）。labels：`(q,p2)`/`(q,p1)` `task_label=1`，`behavior_label=None`，`behavior_known=False`。scientific `fit` 只写出 **task** 头 `U`（loss `0.05036`）；行为头 `no_known_labels`。 |
| **Impact** | 差集 $S$ 在本机没有行为正例，不是“编辑后步骤值是否跟随前提”。即使将来约束数字因提示词改写而变化，那也是 teacher-force 采样对前缀的敏感，不是 §2.2 的 $v(s_i)$。 |
| **Suggested fix** | 先关闭 A11-01。无生成步骤则不写行为标签，保持 `unknown`。 |
| **Status** | **confirmed defect**（MATCH 窗口） |

### A11-03 — 未知行为被当成空 $B$，写出 `rho_M_raw=1.0`（不是 B9-01）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `measure.py` `event_density_sets` 354–356 |
| **Trigger** | 论文 §2.6：$M=R_{\mathrm{task}}\setminus R_{\mathrm{behavior}}$。协议 §2.4：有限扫描中的 $M$ 不等于已经证明“从未读取”。GOAL §5.3：未知不作负。指定猎点要求 `rho_M_excess` **不得**因 $N=\{p1,p2\}$ 而为 1.0——该 excess 条件本轮满足；本条是 **raw** 列的另一偷换。 |
| **Paper requirement** | 行为未知时 $M$ 应不可评或显式 unknown，不得把空观测写成漏读密度 1。 |
| **Repro / evidence** | MATCH 窗口 densities：`behavior_set` 只收 `behavior_label==1`，未知行不入 $B$。$T=\{p1,p2\}$，$B=\emptyset$ → $M=\{p1,p2\}$，`rho_M_raw=1.0`，`denominator_M=2`。同时 `rho_M_excess=None`，`null_reason=noise_set_missing`。analyze 报告同样写出 `rho_M_raw=1.0` 且顶层 `null_reason=None`（聚合行不复制事件级 reason）。 |
| **Impact** | 读者若只看 raw 会以为模型漏读全部任务祖先。这不是 sham 广播，也不是已扣噪声。 |
| **Suggested fix** | 无已知行为正/负时不要填 $B=\emptyset$；`rho_M_raw` 与 $M$ 一并 null，并写 `behavior_unknown`。 |
| **Status** | **confirmed defect**（描述量）；**不是** B9-01 重开 |

### A11-04 — 账本可执行行仍大量 `implemented_local`

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` TR-0158、TR-0400、TR-0125；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：未实现不得标已实现。r06 可执行行验证列已改 `tests_exist_not_acceptance`，**不得**按更早“pytest 关闭可执行行”原文重开。 |
| **Paper requirement** | 可执行条款对到真实符号与可复查证据。 |
| **Repro / evidence** | 728 行 / 528 TR。`implemented_local` **478** 处。TR-0125 `partial_local_scientific`、TR-0135 `partial_local_tiny`。TR-0158 / TR-0400（解耦任务构造）仍指向 `intervention_report` 且 `implemented_local`。协议/标题行仍 **70** 处 `python -m pytest -q`。REQUIREMENTS 复选框全空，状态表写 `implemented_local`。 |
| **Impact** | 覆盖率仍被制成 16/16。独立审查若信 `implemented_local` 会漏检 A11-01。 |
| **Suggested fix** | 未接到论文语义的可执行行改为 `unimplemented` / `ok-lib_unwired` / 保持 `partial_*`。 |
| **Status** | **confirmed defect**（过称）；pytest-关闭可执行行 **本轮不重开** |

### A11-05 — CLI 四档 verbalizer 回显前缀，把约束数字当成自述命中

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_fit` 653–656；`baselines.py` 92–125 |
| **Trigger** | 论文 §8 L333–337；GOAL §5.7。子串打分 **不得重开**（库层 `17` 为 0）。 |
| **Paper requirement** | 四档自述与探针同样本/划分/可见前缀。 |
| **Repro / evidence** | 库：`verbalizer(..., generate_fn=λ:"17")` 对金标 `7` 得 0。CLI `generate_fn=lambda p, t=prefix: t`。scientific fit：zeroshot/fiveshot/reflection `score=1.0`，`extracted='82'`（回显整段轨迹，抽出约束赋值）。supervised 拒未训练。BoundaryMLP：`note=event-rows-only_no_negatives`。 |
| **Impact** | 第 8 节“说不出来”在 CLI 上仍不是同划分模型自述。 |
| **Suggested fix** | CLI 按同一划分调用真实生成；未接线不得标 `implemented_local`。 |
| **Status** | **confirmed defect**（CLI 替身）；子串打分 **本轮不重开** |

### A11-N1 — Gate 0–2 保持未注册；科学结论保持空（非缺陷；也不是 pass）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 215–257；`cli.py` `cmd_analyze` 1087–1150 |
| **Trigger** | 协议 §6；GOAL §5.14。指定猎点：Gate `unregistered` 冒充 pass。 |
| **Paper requirement** | 用户未给阈值则不得编造 pass/fail。不得把 fixture 写入科学结论。 |
| **Repro / evidence** | `week8_decision({status:not_evaluated, rho_S_excess:None})` → 三门 `decision=unregistered`，`scientific_conclusion=None`，`skip_p2_p3=True`。有阈值有度量 → `compared`/`above`，**仍无 pass 字段**，`scientific_conclusion` 仍 `None`。`rho_S_excess=0` → `c3_negative_descriptive`，Gate 仍 `unregistered`。scientific analyze（`--in-dir` prepare）：`status=not_evaluated`，`p1=None`，三门 `unregistered`。 |
| **Impact** | 正确持守。指定猎点**未发生**。假说不要求正结果，本条不升格。 |
| **Suggested fix** | 不要添加阈值，也不要把 `unregistered` 写成通过。 |
| **Status** | **non-defect** |

### A11-N2 — tiny 随机权重不是 MODEL-01（非缺陷）

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

### A11-N3 — sham 命中不再当作已映射噪声前提（非缺陷；B9-01 本轮不重开）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `measure.py` `build_labels` 72–80；`event_density_sets` 328–349；`cli.py` prepare 362–376 |
| **Trigger** | VERSION / ISSUES 作者声称：本冻停止广播；r09 B 在漂移树上确认过 $N=\{p1,p2\}$ → `rho_M_excess=1.0`。指定猎点：sham 广播冒充已扣噪声。作者关闭**不当关闭**；本条依据本通道复跑。 |
| **Paper requirement** | 协议 §2.6：噪声参照必须有明确配对与共同支持；未注册配对不得强加具体前提身份。§2.6 / §3：先扣噪声再报告 excess。 |
| **Repro / evidence** | MATCH 窗口 scientific prepare `--sham-opportunities 1`：sham obs `82→53` `changed`，`premise_id=sham:q`。labels：`(q,p1)`/`(q,p2)` `noise_ref=None`；仅 `(q,sham:q)` `noise_ref=1.0`。densities：`rho_M_excess=None`，`rho_M_noise=None`，事件级 `null_reason=noise_set_missing`。手造“若仍广播 `noise_ref=1.0` 到 p1/p2”：`event_density_sets` **仍**给 `noise_set_missing` / excess null（`sham:` hit 优先于 `real_hits`）。`build_labels` 当前路径不会把 1.0 写到真实前提。 |
| **Impact** | 指定猎点的 **excess=1.0 from $N=\{p1,p2\}$** 在 MATCH 窗口**未再现**。`rho_M_raw=1.0` 见 A11-03，不得与本条合并。 |
| **Suggested fix** | 保持 sham 行隔离。测试应锁 `$N$ missing` 与 `p1/p2.noise_ref is None`，不要只写 `excess != 1.0 or null_reason`。 |
| **Status** | **non-defect**（相对 B9-01）；关闭条件已在 MATCH 窗口独立见到 |

---

## 6. 明确的非缺陷 / 持守项（避免空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5，也不能认证已漂的冻结。

1. **Gate 0–2**：无阈值、无 pass/fail（A11-N1）。`unregistered` **不是** pass。
2. **`scientific_conclusion` 保持 `None`**。analyze 无 `p1_table` 时 `p1=None`，不伪造 AUC。
3. **tiny 不是 MODEL-01**（A11-N2）。
4. **REST-01/02/03** 禁词列表存在；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
5. **身份对齐不含值**。
6. **$R_{\mathrm{task}}$ 祖先**、**$S/M$ 空分母→null**、**缺/空 sham→excess null**。
7. **sham 命中不把真实前提写入 $N$**；`rho_M_excess` 不是 1.0（A11-N3）。
8. **交换公式** $H^b+\Pi_Z(H^d-H^b)$ 在 $\Pi=I$ 时得 donor。
9. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$。`[0.1,0.2,0.3,0.4], α=0.4` → $q=0.3$；$\alpha=0.1$ → $+\infty$。
10. **4096 vs 3584 直接迁移 N/A**。$n<d$ PCA 标 `truncated`。
11. **官方 iGSM 快照拒裸 `G`、排除共享 RNG、mod 23**；夹具拒绝 `official`。
12. **宿主 exec 被禁止**；`ChildProcessExecutor` 不冒称沙箱。
13. **假说不要求正结果**：本通道不因无 F1/AUC 正数判失败。
14. **P1 留出路径为 IRLS logistic**；bootstrap **重算** $\Delta\mathrm{AUC}$。
15. **scientific 调用模型 generate**，不是节点真值轨迹；题干前提赋值不再当作生成事件。
16. **tiny $E$ 为读出层 span 均值**，行不相同；scientific 拒 offline $H$。
17. **scientific $H$ 有限**，行数=可表达事件。
18. **`source_value_pair` 写入 `edits.jsonl`**，并生成 `trace-source`。
19. **collect 复制 `tasks.jsonl`**；有任务时 `_e_premise_ids` 跟前提序（C6 默认 scientific fit **本轮不重开**）。
20. **verbalizer 抽答案**：`17` 不再当子串命中。
21. **可执行行不再用 pytest 关闭**（`tests_exist_not_acceptance`）。
22. **Plus 注册族锁**；T3 prepare 跳过 SVP（代码可见；本通道未把作者关闭当关闭，也未新开）。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_scientific_prepare_emits_parseable_events` | 每条轨迹 ≥1 事件且含 `q`；无节点真值拼接 | 事件是生成步骤；拒绝 `constrained_target` |
| `test_generated_events_exclude_prompt_assignments` | 事件 `start≥prompt`；`parse_region=generated` | 非 teacher-force 目标行 |
| `test_scientific_h_is_finite_and_pairs_donor` | $H$ 有限；`donor_kind`/`inlp_transform`/`ie_z_g` 字段 | $H$ 对应自然步；$R_{\mathrm{behavior}}$ |
| `test_truth_indices_follow_e_columns_not_label_order` | `_e_premise_ids(task, …)` 跟前提序 | 无任务时的列身份（本轮默认路径已有任务副本） |
| `test_verbalizer_uses_extracted_answer_not_substring` | `17`/`70`/`boxed` 不子串命中 | 同划分四档模型自述 |
| `test_sham_hits_do_not_broadcast_real_premises_into_n` | `p1/p2.noise_ref is None`；`rho_M_excess is None` | 未知 $B$ 不得写 `rho_M_raw=1.0` |
| `test_scientific_sham_does_not_book_rho_m_excess_one` | `excess != 1.0 or null_reason`；`p1/p2.noise_ref is None` | 弱析取：聚合行 `null_reason` 可为 None 而 excess 已是 None 即过 |
| `test_full_cli_smoke` | 八阶段返回 0；**offline** $H$ | generate、论文步边界、干预生成 |
| `pytest -q` 全集 | 155 passed（MATCH 窗口） | §4.1 自然轨迹；Gate 不是 pass |

---

## 8. 本审查复跑的命令（均可再跑；树已漂则结果不能认证声明 hash）

工作目录 `C:\Users\22688\Desktop\diff`，`$env:PYTHONPATH='src'`。

1. `VERSION.md` 原文 Python → 开始 **61** / `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`；写报告后再算 **61** / `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（中途还见 `929aa472…` / `4da0b2bd…` / `598e6c8f…`）。
2. SHA-256：论文 / 协议 / GOAL / REQUIREMENTS → 见页眉。
3. `python -m pytest -q` → **155 passed**（MATCH 窗口）。
4. `generate_task_trace` + `prepare --eval-mode scientific --sham-opportunities 1 --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15` → 7 条 tiny 轨迹，全部 `constrained_target`，各 1 个 `q` 事件；含 `trace-source` / `trace-sham`；`source_value_pair` 在 `edits.jsonl`。
5. 密度：`rho_M_excess=None`，`rho_M_raw=1.0`，`null_reason=noise_set_missing`；$N$ 不是 `{p1,p2}`。labels：真实前提 `noise_ref=None`，仅 `sham:q` 为 1.0。
6. `collect --backend tiny --weight-seed 0` → $H=(7,32)$ 全有限，行=事件，$E$ 行不同，`hidden_layer=1`，**写出 `tasks.jsonl`**。
7. `fit --in-dir collect --labels-dir label`：`_e_premise_ids(task)=[p1,p2]`；task 头有限 $U$；行为头无已知标签；verbalizer 回显前缀抽出 `82`。
8. `analyze --in-dir prepare` → `p1=None`，`scientific_conclusion=None`，Gate `unregistered`，`status=not_evaluated`。
9. 库微例：`conformal_threshold` / `apply_swap` / `verbalizer` / `week8_decision`：见 §5–§6。
10. 手造广播标签：即使 `noise_ref=1.0` 写在 p1/p2，`event_density_sets` 仍因 `sham:` hit 保持 $N$ missing。

---

## 9. 结论

**冻结 hash：审查开始 HASH_MATCH `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`（61 文件）；交卷 HASH_MISMATCH（最后一次复算 `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`）。**

**原文一致性：不通过（FAIL）。**

指定猎点的独立结论（MATCH 窗口）：

- **teacher-force 冒充 §4.1：成立（A11-01 / A11-02）。** scientific 接受 `constrained_target`，7 条轨迹只有约束 `q`。
- **Gate `unregistered` 冒充 pass：不成立（A11-N1）。** 三门保持 `unregistered`，`scientific_conclusion=None`。
- **sham 广播冒充已扣噪声：不成立（A11-N3）。** `rho_M_excess` 不是 1.0，也不是 $N=\{p1,p2\}$。`rho_M_raw=1.0` 来自未知 $B$ 当空集（A11-03），不得写成 B9-01 重开。

先前接线项（生成区 / 有限 $H$ / SVP / collect 任务副本 / Gate null / tiny≠MODEL-01）**不得当新缺陷原样重开**。它们也**不能**在声明冻结上关闭：交卷树已变。作者关闭与绿测不能关闭本通道。真实权重/官方全量是 `pending_server`，不能解释本机把约束赋值写成 $T$。

独立复审关闭条件（本通道）：先重冻并在**同一 hash** 上再开 A–F；A11-H1 关闭条件是 VERSION 与磁盘复算一致且审查期间不变；A11-01 与 A11-02 必须对照原文关闭（scientific 事件来自生成步骤，或对 `constrained_target` 诚实拒绝并降级账本）；A11-03 须在行为未知时不要写 `rho_M_raw=1.0`。其余 medium 项至少改为诚实状态。

**不把 Goal 标为完成。**
