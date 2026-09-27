# 审查报告 A：原文一致性（paper consistency）

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent |
| **审查时间** | 2026-09-21 00:28–01:25（UTC+8） |
| **声明冻结 hash** | `532e05a8038e9862f219ab36927f7f7c0df59ef639045821a2cc801960b2b0c0`（`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`） |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与 `.planning/PAPER_TRACEABILITY.md` 登记一致） |
| **本审查实测代码 hash** | **未能复现**声明冻结值。对当前 52 个范围内文件尝试了：文件字节串联、文件 SHA-256 hex 串联、原始 digest 串联、sha256sum 风格。均不等于 `532e05a8…`。审查对象是下方逐文件清单中的**当前工作树**，不是一个已核验的冻结快照。 |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏） |
| **范围** | 论文全文；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5；`.planning/PAPER_TRACEABILITY.md`；`src/reasoning_diff/**/*.py`；对照测试只读，用于判断“被测行为是公式还是替身”。**未读**其他通道审查报告。 |
| **生产代码** | 未修改 |

**总判：** 当前仓库是一套**公式碎片 + 夹具冒烟 CLI**，不是论文要求的科学评测实现。若干核心公式（$R_{\mathrm{task}}$、TO/CSP、$S/M$、交换式、保形分位数、直接迁移拒维度）在库函数层写对了；但采集、训练、干预执行、修复嫁接、T2/T3 合法编辑、公平基线、P1 统计、附录拟合，几乎全部被**概念替换**或**空实现**。`.planning/PAPER_TRACEABILITY.md` 仍全部 `TBD` / `unimplemented`，不能当作覆盖证据。

---

## 1. 逐文件覆盖

每行：路径（行数）— 对照了哪些论文条款 — 结论摘要。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `pyproject.toml` | 26 | §8.1 模型依赖；GOAL §5.15 | 仅 `numpy`；`torch`/`transformers` 未声明。无 `--eval-mode scientific` 入口声明。 |
| `src/reasoning_diff/__init__.py` | 5 | — | 仅导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/schema.py` | 368 | §2.1–2.3 身份/标签枚举；GOAL §5.3 | 身份不含值；outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 实现。 |
| `src/reasoning_diff/graphs.py` | 44 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先集合与相交掩码正确。默认 cone 走任务祖先，不是行为头预测。 |
| `src/reasoning_diff/events.py` | 94 | §2.2–2.3、§4.1 对齐与表面提及 | 身份对齐正确；`merged`/`strategy_changed` 恒空；`surface_mentions=node.parents`；仅夹具正则解析。 |
| `src/reasoning_diff/edits.py` | 128 | §7 T1 重算；GOAL §5.2 | 表达式重算 + mod 可用。无改名/算子逆转/增删约束/Spec 编辑。 |
| `src/reasoning_diff/measure.py` | 217 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集与空分母/缺 sham→null、signed excess 正确。TO/CSP 无对错分层、无噪声配对。CLI 误用第一节点祖先。 |
| `src/reasoning_diff/analysis.py` | 108 | §2.6 P1–P3；§7 分流；附录 S2–S4；REST-01/02 | P1 被换成线性分数 AUC；`cone_fit`/`retrieval_scatter` 为空壳；Week-8 无分流树。 |
| `src/reasoning_diff/interventions.py` | 73 | §2.4 交换/对照/INLP/救援 | 交换式正确。C-rand 范数对 `default_rng(1)` 而非主干预基。无 C-layer 选择。INLP/救援降级。 |
| `src/reasoning_diff/probes/bilinear.py` | 45 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向形式与损失正确。**无训练**；双头未实现。 |
| `src/reasoning_diff/probes/boundary.py` | 23 | §4.2 Hidden=256 ReLU | 架构符合。**无训练**、无句法监督接入。 |
| `src/reasoning_diff/probes/calibrate.py` | 33 | §2.5 命题 2 | $\lceil(N+1)(1-\alpha)\rceil$ 与 $+\infty$ 正确。调用方未保证分数为 $1-\hat p$。 |
| `src/reasoning_diff/probes/__init__.py` | 3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 44 | §8 文本/注意力/四档自述 | 词面匹配替身，不是同监督训练器。 |
| `src/reasoning_diff/transfer.py` | 36 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。线性映射存在。未接到探针两输入，未先共同维再 Procrustes。 |
| `src/reasoning_diff/repair.py` | 57 | §3 Repairability/RR；§9 嫁接 | 掩码名枚举在。`run_repair` 不生成、不 Prefill、不重算。 |
| `src/reasoning_diff/cli.py` | 239 | §4 流水线；§8.2 scientific | 八阶段均为合成/硬编码冒烟。 |
| `src/reasoning_diff/models/adapters.py` | 29 | §8.1 模型卡/revision | 两张冻结卡。无加载、无 tokenizer、无采集。 |
| `src/reasoning_diff/models/collect.py` | 41 | §4.2 $h_i/e_j$；GOAL §5.6/5.10 | tiny 采集**不取隐状态**；干预是 `+0.01`，不是 $\Pi_Z$ 交换。 |
| `src/reasoning_diff/models/features.py` | 28 | §2.4 三时机；GOAL §5.6 | 跨界 token 排除正确。`pre_step` 与 `pre_value` 同字符则同索引。 |
| `src/reasoning_diff/models/generate.py` | 56 | §8.2 自然轨迹 | 显式 decode 循环存在。CLI 不用。无隐状态/层切片。 |
| `src/reasoning_diff/models/tiny.py` | 88 | 本机 hook 边界 | 随机 Qwen2/3 + resid_post 清理。不是论文模型路径。 |
| `src/reasoning_diff/models/__init__.py` | 1 | — | 注释。 |
| `src/reasoning_diff/tasks/t1_official.py` | 83 | §7 T1；FEATURES template≠G | 快照加载拒绝裸 `G`、排除共享 RNG、默认 mod 23。无 500 题生成、无官方 CoT 解析。 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | 官方/夹具分离 | 拒绝 `official`。 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | op∈{5,10,15,21}，n=500 | 配置校验。无数据生成。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 82 | §7 T2；GOAL §5.2 | 无侧车则假前提（前 8 字）。`apply_formula_edit` 只改答案，不改题干/节点值。无算子逆转/增删条件。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 51 | §7 T2；评测专用 | test-only 锁正确。前提=题目前 12 字。无合法编辑。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 66 | §7 T2-noop | 可造配对与分层元数据。无注入句值扰动，无 T1 图规则等价注入。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 59 | §7 T3；supporting_facts≠DAG | 标记正确。`document_edit` 只回 dict，不产出新 Task/真值。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 69 | §7 T3 组成引用 | 保留 answerable/unanswerable。`expression="composition_reference"` 不可重算。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 35 | §7 HumanEval-Perturb；GOAL §5.15 | 前提= prompt 前 40 字。无 Spec 编辑包。评分走不可用执行器。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 33 | §7 T4；Fig.6 | 四类状态强制区分。前提=前 10 字。无相图。 |
| `src/reasoning_diff/tasks/__init__.py` | 1 | — | 注释。 |
| `src/reasoning_diff/executor.py` | 59 | GOAL §5.15 | 禁止宿主 exec。无超时/资源限制的真实隔离后端。 |
| `src/reasoning_diff/scoring.py` | 30 | §3 域内评分 | 数值/QA 精确匹配。代码必经隔离接口。 |
| `src/reasoning_diff/splits.py` | 66 | §4.1 共组；GSM-Plus test-only | 六角色 + 家族共组。默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 53 | GOAL §5.4 | sample/direction/perturb/bootstrap/split 分离。CLI 基本不用。 |
| `src/reasoning_diff/io.py` | 108 | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 83 | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 11 | — | 夹具路径。 |
| `tests/test_cli_pipeline.py` | 18 | §4 流水线 | 只断言八阶段 exit 0，不验科学语义。 |
| `tests/test_science.py` | 97 | 校准/迁移/交换/Week-8 | 测到的是库函数微例，不测训练/采集/嫁接。 |
| `tests/test_measure.py` | 40 | $S/M$、联合编辑反例 | 与公式一致。 |
| `tests/test_tracer_t1_prepare.py` | 99 | T1 夹具准备 | 覆盖身份/重算/空分母。CLI prepare 祖先错误未被测。 |
| `tests/test_t1_official.py` | 31 | template≠G | 快照形状。 |
| `tests/test_t2_gsm.py` | 33 | T2 | 只验答案变成 8，不验题干/节点。 |
| `tests/test_t3_t4.py` | 40 | T3/T4 | 明确“supporting_facts 不是 DAG”；不验编辑真值。 |
| `tests/test_artifacts.py` | 73 | I/O | 工程。 |
| `tests/test_generate_loop.py` | 17 | 可重放采样 | tiny decode。 |
| `tests/test_tiny_hooks.py` | 27 | hook 清理 | 本机接口。 |
| `tests/test_tiny_cache.py` | 25 | 缓存隔离 | `intervene_tiny` 是平移，不是交换。 |

第三方库：审查了本项目对 `numpy` /（未声明的）`torch`+`transformers` 的**使用假设**，未审查依赖源码。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献清单 | 完成。实质条款见 §4 映射。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` 标签/划分/干预/P1–P3/Gate/本机边界 | 完成。Gate 保持 null 与实现一致。 |
| C3 | 通读 GOAL §5 十五条高风险索引 | 完成。第 1–2、7–13、15 条在代码中被降级或缺失。 |
| C4 | 通读 `PAPER_TRACEABILITY.md` 论文行 TR-0001–TR-0261 及协议/GOAL 行 | 完成。账本仍写 `impl_status=unimplemented`、`impl_file=TBD`，**不能**作为实现证据。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py`（含 `models/{adapters,collect,generate,tiny,features}.py`） | 完成。见上表。 |
| C6 | 对照公式手核：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1 | $R_{\mathrm{task}}$/TO/差集/交换/分位数/拒维度：**库函数层符合**。P1：**不符合**（见 A-P-03）。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | 无多 seed `generate`、无 `allowed_edits` 全扫描、无独立双标签流水线。`collect` 写零向量。 |
| C8 | 对照 §4.2 / §8 探针与基线 | 有随机初始化前向，无拟合；基线是子串打分。 |
| C9 | 对照 §2.4 / §6 干预与解耦任务构造 | 无来源—数值解耦资产；无层内 hook/KV 协议执行；无 C-layer。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 读取+合法编辑+更新真值 | T1 快照/夹具部分成立。T2/T3/T4 编辑与真值路径缺失或假前提。 |
| C11 | 对照附录 S1–S4、C4 掩码、连续编辑 $k\in\{1..5\}$、失效相图 | 仅有函数名/枚举/空返回。 |
| C12 | 抽读测试，判断其是否把替身固化为“已实现” | 是：`test_full_cli_smoke`、`test_verbalizer_supervision_contract`、`test_repair_reprefills_*`、`test_symbolic_sidecar_edit` 均不触及论文语义。 |
| C13 | 独立重算论文文件 SHA-256 | 与账本一致。 |
| C14 | 独立重算声明代码冻结 hash | **未匹配**。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | `pytest` / CLI 端到端实跑 | 本通道是原文对照，不宣称工程通过。VERSION 写明“reviewers must re-run commands they claim”；本报告不声称测试通过。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量数据 | 协议 §7：科学结论 `pending_server`。且代码中**没有**可调用的真实权重采集路径。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | 无训练循环可跑。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`n/a`。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | 探针/干预/分析/修复均冒烟 | stub |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `week8_decision` 禁词 | ok-lib |
| 论文 1 | 34–35 | 检索余弦 vs 答案变 | exec | `retrieval_scatter` 只汇总传入对 | stub |
| 论文 1 | 38 | 修复解码/Prefill/耗时 | exec | `Cost` 字段有；repair 填字符长度 | subst |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema + 夹具解析 | ok-lib |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | `build_labels` 有限扫描字段；CLI 单编辑合成轨迹 | stub |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | `surface_mentions=node.parents` | subst |
| 论文 2.3 | 88 | 消失/合并/策略分岔 | proto | `removed` 有；`merged`/`strategy_changed=[]` | stub |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap` | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ | math | 无期望估计 | missing |
| 论文 2.4 | 106–108 | 前瞻 hook/KV/前缀 | exec | tiny `+0.01`；CLI 随机向量 | subst |
| 论文 2.4 | 110 | 步前/数值前/步尾 | exec | 同字符则前两时机重合 | subst |
| 论文 2.4 | 114–117 | C-rand / C-layer 同幅度四项 | exec | C-rand 范数对象错；C-layer 无选择函数 | subst / missing |
| 论文 2.5 | 121–125 | cone / Oracle / 行为掩码 | math | `dirty_cone`/`oracle_mask`/`behavior_mask` | ok-lib |
| 论文 2.5 | 127–130 | 命题 1 + REST-03 | math | 仅 $xy$ 反例夹具 | ok-lib（限制） |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | `sequence_score`/`conformal_threshold` | ok-lib |
| 论文 2.5 | 141–142 | 原轨迹槽位、禁重拓扑 | exec | 无嫁接执行 | missing |
| 论文 2.6 | 148–156 | $S,M,\rho$，空分母 N/A | math | `dependency_densities` | ok-lib |
| 论文 2.6 | 158 | 噪声先扣除 | proto | 无 sham→excess null | ok-lib |
| 论文 2.6 | 164 | P1 logistic + 偏相关 + bootstrap | math | `length+0.01*op` 的 AUC | subst |
| 论文 2.6 | 165 | P2 配对 + 污染位置 | exec | 只减两个标量 | stub |
| 论文 2.6 | 166 | P3 Δacc + 对照 + 非目标 | exec | 无非目标；无消融执行 | stub |
| 论文 2.6 | 168 | REST-02 | proto | `causal_reverse_claim=False` | ok-lib |
| 论文 3 | 176–186 | TO_all/clean、CSP、覆盖、脏变、P/R/F1 | math | TO/CSP/覆盖/脏变有；无探针 P/R/F1；无对错分组 | partial |
| 论文 3 | 188 | TO/CSP 噪声参照与比值 | proto | 无 | missing |
| 论文 3 | 190 | 干预三项并列、前瞻/回溯分列 | proto | `intervention_report` 接受三 dict；CLI 硬编码 | stub |
| 论文 3 | 194–200 | Repairability、RR、成本分列 | math | 两公式有；成本未测 | stub |
| 论文 4.1 | 232–253 | 双标签流水线；NL 单调对齐；共组 | exec | 无 generate 循环；无 NL 对齐 | missing |
| 论文 4.2 | 257–267 | MLP 训练、双头、池化 $e_j$、60–75% 层、改名/未见组合 | exec | 架构常数在；训练/池化/层选/泛化测试无 | stub |
| 论文 5 Fig.1–2 | 291–299 | 热力图、三时机比较、跨模型迁移入口 | exec | 无导出 | missing |
| 论文 6 | 305–313 | 来源—数值解耦、INLP、救援对照 | exec | 无任务构造；INLP/救援降级 | missing / subst |
| 论文 7–8 | 317–337 | 噪声先行分流；注意力头聚合；四档 verbalizer；文本预测器 | exec | 词面打分；无分流执行 | subst |
| 论文 9 | 347–355 | Oracle 嫁接、5+3 掩码、同预算、Fig.6、连续编辑 Prefill | exec | 枚举名 + `generated_tokens=0` | stub |
| 论文 S2 | 363–367 | $1-\exp\{-\lambda(1-x)^\gamma\}$ 三锥拟合 | math | 只返回公式字符串 | stub |
| 论文 S3 | 371–373 | 先共同维映射再 Procrustes | exec | 两函数分离，维不同直接 N/A | stub |
| 论文 S4 | 375–377 | 嵌入余弦散点，不得删除 | exec | 不计算嵌入 | stub |
| 论文 6.2 | 394–395 | RL / Cone Gate / Fallback | excl | 修复路径拒 gated/fallback | n/a（符合排除） |
| 论文 7 | 403–407 | T1–T4 假设专用数据 | exec | 见 A-P-06 | stub |
| 论文 8.1–8.2 | 416–431 | 模型库；`--eval-mode scientific` | exec | 仅卡片；无该 flag | missing |
| 论文 9–12 | 437–503 | Week-1 三轨迹、50 条干预、清单 | proto | 无 | missing |
| 协议 §5–6 | 52–80 | Week-8 七条分流；Gate null | proto | Gate null 对；分流树无 | partial |
| GOAL §5.15 | 91 | 隔离执行器+超时/限额 | exec | Unavailable/Spy | stub |

假说行（F1>0.95、TO~0.25 等）不要求正结果；但**测量入口**必须存在。当前入口是硬编码数，不能测量假说。

---

## 5. 发现

### A-P-01 — 科学评测流水线被夹具冒烟替换

- **严重度：** critical  
- **状态：** confirmed defect  
- **位置：** `cli.py` `cmd_prepare` 57–119、`cmd_collect` 122–134、`cmd_label` 137–140、`cmd_fit` 143–151、`cmd_calibrate` 154–159、`cmd_intervene` 162–179、`cmd_repair` 182–185、`cmd_analyze` 188–197、`build_parser` 200–229  
- **触发：** 任意 `reasoning-diff {prepare,collect,…,analyze}`  
- **论文要求：** §4 流水线树；§8.2 `--eval-mode scientific`（自然轨迹与隐状态、双标签、探针校准、交换/消融/救援、无门控嫁接、离线评分与成本）；GOAL §6：禁止关键路径假返回/空 adapter。  
- **证据：** `collect` 写 `np.zeros(4)`；`label` 写死四前提密度；`fit` 对随机 $4\times4$ 探针算一次 loss；`calibrate` 用 `[0.1,0.2,0.3,0.4]`；`intervene` 用 `rng.normal` 向量 + 硬编码 0.8/0.2/0.25；`analyze` 用手写数组调用 P1–P3。无 `--eval-mode`。`tests/test_cli_pipeline.py` 只断言 exit 0。  
- **影响：** 该入口的产物不能当作 C1–C4 证据；若写入报告即伪造科学结果。  
- **建议：** 各子命令读取上一阶段清单，调用真实 generate/label/fit/hook/graft；scientific 模式拒绝 fixture 冒充 official。

### A-P-02 — 双线性探针与边界 MLP 无训练（双头未实现）

- **严重度：** critical  
- **状态：** confirmed defect  
- **位置：** `probes/bilinear.py` `BilinearProbe` 7–29、`weighted_bce` 37–45；`probes/boundary.py` `BoundaryMLP` 7–23；`cli.py` 143–151  
- **触发：** `cli fit` 或直接构造 `BilinearProbe`/`BoundaryMLP`  
- **论文要求：** §4.2：$\hat p_{ij}=\sigma(h_i^\top UV^\top e_j+b)$，$r=64$，加权 CE $\lambda_{FN}=10$，任务头/行为头分别学 $R_{\mathrm{task}}$ 与 $R_{\mathrm{behavior}}$；2 层 MLP Hidden=256 ReLU，iGSM 句法监督。  
- **证据：** 前向与 $\lambda_{FN}=10$ 正确；`U,V` 仅 `default_rng(0/1)` 初始化；无 `fit`/`step`/优化器；`head_type="unspecified"`；CLI 只写一个 `"head": "task"`。无 $e_j$ span 均池、无 60%–75% 层截取。  
- **影响：** C1「稀疏可解码」没有可训练对象；随机权重的 F1 无意义。  
- **建议：** 实现带未知掩码的训练循环；两个头独立参数与标签；层与池化按 §4.2。

### A-P-03 — P1 被换成「链长+0.01·op+ρ」的排序 AUC

- **严重度：** critical  
- **状态：** confirmed defect  
- **位置：** `analysis.py` `_auc` 19–28、`p1_incremental` 31–37  
- **触发：** `p1_incremental(...)` 或 `cli analyze`  
- **论文要求：** §2.6 表 P1 / 结果 §7：控制链长与 op 后，$\rho_S$ 对逐题正确性的 **logistic AUC** 与 **偏相关**，bootstrap 区间，与链长平凡因子比增量。协议 §5：留出题上比较「链长+op 基线」vs「加入虚假依赖的预测器」。  
- **证据：** `base=_auc(length+0.01*op,y)`，`full=_auc(length+0.01*op+rho,y)`。不是 logistic，不是留出拟合，不是偏相关。`0.01` 无论文依据。`bootstrap_cluster` 存在但 P1 不用。  
- **影响：** 把「控制协变量的分类器增量」偷换成「把 ρ 加进一个任意线性分数再算 AUC」。正/负结果都不能对应 P1。  
- **建议：** 留出题上拟合 logistic（仅 length+op vs length+op+ρ）；报告 ΔAUC、偏相关、问题级 bootstrap；单类保持 null。

### A-P-04 — 无真实（或接口完整的）隐状态采集；tiny 路径也不取 $h_i$

- **严重度：** critical  
- **状态：** confirmed defect（代码缺失）；真实权重运行为 pending_server  
- **位置：** `models/collect.py` `collect_tiny` 11–19、`intervene_tiny` 22–41；`models/adapters.py` 3–29；`models/generate.py` 28–48；`cli.py` 122–134；`pyproject.toml` 10  
- **触发：** `collect_tiny` / `cli collect` / 任何「采集 Qwen3-8B」意图  
- **论文要求：** §8.1 首批 Qwen3-8B 与 R1-Distill-Qwen-7B，记 revision；§4.2 $h_i$ 边界 token、$e_j$ 同层均池；GOAL §5.1/5.6/5.10。  
- **证据：** `adapters.MODELS` 只有卡片。`collect_tiny` 返回 token id 与 `select_prefix_index`，**无 hidden**。`cli collect` 写 `dummy` 零向量。`intervene_tiny` 对 residual `+0.01`，不是交换。`pyproject.toml` 无 torch/transformers。  
- **影响：** C1/C2 主证据链在本机接口层已经断。tiny 测试不能外推到论文模型。  
- **建议：** 实现冻结 revision 的 HF 加载、三时机隐状态、前提 span 池化；tiny 路径至少提取一层 hidden，干预走 `apply_swap`。

### A-P-05 — 无门控局部修复只有记录，没有嫁接/重算

- **严重度：** critical  
- **状态：** confirmed defect  
- **位置：** `repair.py` `run_repair` 34–45、`RepairRecord` 12–31；`cli.py` 182–185  
- **触发：** `run_repair(...)` / `cli repair`  
- **论文要求：** §9 / C4：Oracle 掩码嫁接；干净文本 Prefill；受损槽位自回归重算；同原始 token 预算比较 5 条主文 + 3 条附录掩码；逐步/最终正确率与成本；验证器不改路线。  
- **证据：** `generated_tokens=0`；`extra_prefill_tokens=len(new_prefix)`（字符数）；不调用模型。掩码名校验 ≠ 掩码构造。`test_repair_reprefills_and_refuses_gate` 只查 flag。  
- **影响：** Oracle「用于发现接口问题」的第一周优先实验不存在。C4 不能进入附录，因为它尚未被实现。  
- **建议：** 共用执行器：按槽位保留/重算、新前缀 Prefill、记录真实 decode/prefill/延迟；各掩码独立生成 `slots`。

### A-P-06 — T2/T3/T4「读取 + 合法编辑 + 更新真值」被假前提或元数据替换

- **严重度：** critical  
- **状态：** confirmed defect  
- **位置：**  
  - `t2_gsm_symbolic.py` 42–43、62–77  
  - `t2_gsm_plus.py` 22、11–46  
  - `t2_noop.py` 7–66  
  - `t3_hotpot.py` 51–59  
  - `t3_musique.py` 35–41  
  - `t3_humaneval.py` 21  
  - `t4_boundary.py` 26  
- **触发：** 无侧车的 Symbolic；任何 GSM-Plus/Hotpot 文档替换/HumanEval Spec 编辑/T4 相图；对 no-op 句做行为扫描  
- **论文要求：** §7 T2 数值微扰/算子逆转/增删条件；T2-noop 已知非祖先 + 行为矩阵；T3 换关键文档、HumanEval-Perturb 改一条 Spec 并以单测为裁判；T4 策略突变/无解画 Fig.6。GOAL §5.2：各域都有合法编辑与更新后真值。  
- **证据：**  
  - 无侧车：`Premise("q0", question[:8], …)`。  
  - `apply_formula_edit`：更新 `answer_spec`，**不改 question、不改 nodes[].value**；侧车 `a+b`、a=5 时期望答案 8（测试只断言答案）。  
  - GSM-Plus：前提=前 12 字；无编辑函数。  
  - Hotpot：`document_edit` 返回 `changed_premise_ids` dict，无新 Task。  
  - HumanEval：前提= prompt 前 40 字；夹具 `variant_id=strict_plus` 无编辑包（新 Spec/新测试/新参考）。  
  - T4：前提=前 10 字；无深度×复杂度相图。  
  - no-op：无对注入句的允许值替换（FEATURES 明确仅插入不足以形成行为矩阵）。  
- **影响：** 跨域 $R_{\mathrm{task}}$/编辑响应无法定义；T2/T3 迁移与 Table 1 无数据合同。  
- **建议：** 无图则 `graph_status=unknown` 且拒绝编辑；有侧车则同步题干 span、节点值、答案；Hotpot/HumanEval 产出完整 Edit+新 oracle；禁止用题目前 N 字冒充前提。

### A-P-07 — 公平基线与四档 verbalizer 被词面匹配替换

- **严重度：** high  
- **状态：** confirmed defect  
- **位置：** `baselines.py` `text_predictor` 16–19、`verbalizer` 36–44、`attention_mean`/`attention_rollout` 22–33  
- **触发：** 调用这些函数或宣称 Fig.5  
- **论文要求：** §8 / §4.2：同标签、同划分、同可见前缀的文本预测器与监督 verbalizer；四档（zero-shot / 5-shot / 反思 / 监督微调）并记训练预算；注意力均值、rollout、**开发集选头**；反思不得冒称前瞻。  
- **证据：** 文本=前提前 8 字是否出现在 prefix；verbalizer= gold 前 4 字，分数 0.4/0.6；无 ICL、无微调、无预算。注意力无 dev 头聚合、无 sink/语法分组。`Visibility` 未接入打分。`test_verbalizer_supervision_contract` 只查 `trained=False` 抛错。  
- **影响：** 「模型无法言说」与 R4 分叉无法检验；可用假基线制造「探针更强」。  
- **建议：** 实现与探针同分裂的可训练文本头；四档真实生成/微调协议；注意力阈值在 dev 选定。

### A-P-08 — C-rand 范数匹配的是 `default_rng(1)`，不是主干预

- **严重度：** high  
- **状态：** confirmed defect  
- **位置：** `interventions.py` `c_rand_delta` 31–36  
- **触发：** `c_rand_delta(base, donor, rank, rng)`  
- **论文要求：** §2.4 / 协议 §4：同层同位置同维 $r$，施加**同等范数**的交换；记录实际范数并匹配，而不只共用系数。  
- **证据：** 随机子空间用传入 `rng`；「主干预范数」用 `orthonormal_basis(..., np.random.default_rng(1))` 的另一次投影。与 `apply_swap` 的真实 $\Pi_Z$ 无关。CLI 分别算 `main` 与 `cr`，两范数不必相等。无 C-layer（开发集弱层）符号。  
- **影响：** 「相对对照的差值」建立在错误的对照幅度上，C2 主效应不可解释。  
- **建议：** 传入主干预实际 $\Delta$ 范数、层、token、rank、随机流；实现 `select_c_layer(dev_curve)`。

### A-P-09 — 前瞻干预与三时机被替身

- **严重度：** high  
- **状态：** confirmed defect  
- **位置：** `models/features.py` 8–23；`models/collect.py` 17–18、30–34；`events.py` `boundary_index` 74–80  
- **触发：** `collect_tiny`；`select_prefix_index(..., same_char, "pre_step"|"pre_value")`  
- **论文要求：** 主干预在目标步**首 token 未生成**时；比较步前 / 数值输出前 / 步尾；跨界 token 不得泄漏。  
- **证据：** 跨界排除本身正确。`collect_tiny` 用同一 `target=len(prompt_ids)` 填三个时机 → `pre_step` 与 `pre_value` 皆 `before`，索引相同。`intervene_tiny` 全序列 `+0.01`，不是步前边界 $\Pi_Z$。无 donor 按数值条件重提、无 KV 更新范围记录。  
- **影响：** Fig.2b / R7 分叉无法计算；「前瞻可控」无执行语义。  
- **建议：** 三时机使用 `event.start` / `value_start` / `event.end`；干预只在目标首 token 前、记录 hook 与 KV 范围。

### A-P-10 — $R^{\mathrm{surf}}$ 被图父节点替换

- **严重度：** high  
- **状态：** confirmed defect  
- **位置：** `events.py` `parse_fixture_events` 49  
- **触发：** 夹具/CLI 事件解析  
- **论文要求：** §2.3：表面提及是步骤**文本**中的前提名称与符号引用，与值响应分列，用于文本保留与符号替换。  
- **证据：** `surface_mentions=sorted({parent for parent in node.parents})`，即 DAG 父节点，不是文本提及。  
- **影响：** 干净步符号替换与「提及≠依赖」分析对象错误。  
- **建议：** 从 `event.text` 匹配前提别名/符号；与 `task_parents` 分字段保存。

### A-P-11 — 结构变化只记增删，合并与策略分岔恒空

- **严重度：** medium  
- **状态：** confirmed defect  
- **位置：** `events.py` `align_events` 63–70  
- **触发：** 任何 `align_events`  
- **论文要求：** §2.2/2.3/4.1：消失、合并、换路线单独记录，不并入值变化。GOAL §5.3。自然语言允许跳过与合并的单调对齐。  
- **证据：** `structural.merged=[]`、`strategy_changed=[]`。仅精确 identity key。无 NL 单调对齐。  
- **影响：** 策略分岔会被当成 unaligned/removed，污染 $R_{\mathrm{behavior}}$ 与 CSP。  
- **建议：** 实现合并/分岔检测器；NL 路径用可跳过单调对齐；身份不明进未对齐，不当 0。

### A-P-12 — `cli prepare` 用「第一个节点的祖先」当作 $R_{\mathrm{task}}$

- **严重度：** high  
- **状态：** confirmed defect  
- **位置：** `cli.py` 92–97  
- **触发：** `reasoning-diff prepare`  
- **论文要求：** $R_{\mathrm{task}}(q_i)$ 是**每个**任务节点的完整输入祖先。  
- **证据：** `task_set=next(iter(ancestors(task).values()), set())`。`dict` 插入顺序下这是**第一个**计算节点的祖先，不是逐步标签。`behavior_set` 在任意事件值变时设为被编辑前提全集。  
- **影响：** 唯一 CLI 标签产物系统性错；S/M 密度不可用。  
- **建议：** 按 event→node 映射逐事件写 `task_ancestors[node_id]`；行为标签按前提×事件。

### A-P-13 — INLP / 救援降级；$\mathrm{IE}_Z$ 缺失

- **严重度：** high  
- **状态：** confirmed defect  
- **位置：** `interventions.py` `inlp_remove` 39–51、`rescue` 54–55；全库无 `IE_Z`/`ie_z`  
- **触发：** 消融/救援/效应量  
- **论文要求：** §6 Fig.3c INLP 构造子空间并正交移除；救援补回匹配分量，并设**错误来源**与**随机分量**对照；§2.4 $\mathrm{IE}_Z$ 期望差。  
- **证据：** `lstsq(H, ±1)` 迭代，`p = p - outer(p@u, u)`，不是标准 INLP 分类器+$(I-uu^\top)$ 作用在表示上。`rescue` 只做加法。无错误来源/随机救援函数。无 $\mathbb{E}[g\mid do]$。  
- **影响：** Fig.3c/d 与 P3 没有机制实现。  
- **建议：** 实现 Ravfogel 式 INLP；`rescue_matched` / `rescue_wrong_source` / `rescue_random`；效应量相对对照。

### A-P-14 — 附录与主文图函数为空壳

- **严重度：** high  
- **状态：** confirmed defect  
- **位置：** `analysis.py` `cone_fit` 78–80、`retrieval_scatter` 91–94、`procrustes` 83–88；全库无连续编辑 $k=1..5$、无失效分类器、无 `--eval-mode`  
- **触发：** 附录 S1–S4、Fig.6、Table 1 同预算  
- **论文要求：** S2 两参数拟合三锥；S3 独立配对共同维再 Procrustes；S4 **计算**嵌入余弦（不得删除）；S1 连续编辑 + 新前缀 Prefill；Fig.6 五类失效；§8.2 scientific 模式。  
- **证据：** `cone_fit` 忽略 `x,y`，`r2=None`。`retrieval_scatter` 不调用任何编码器。`procrustes` 形状不同即 N/A，不先映射。无 `k` 循环。无 leak/recompute/graft/strategy/constraint 分类。  
- **影响：** 附录被 GOAL §5.13 明确要求「放附录不是删除代码」；当前等于删除。  
- **建议：** 实现拟合/嵌入/序列编辑/失效标签；scientific CLI 接通。

### A-P-15 — 隔离执行器没有可运行后端

- **严重度：** high  
- **状态：** confirmed defect（实现缺失）；真实沙箱部署 pending_server  
- **位置：** `executor.py` `IsolatedExecutor` 22–24、`UnavailableExecutor` 27–33、`SpyExecutor` 36–46、`get_executor` 49–52  
- **触发：** `score_code` / HumanEval  
- **论文要求：** GOAL §5.15：超时、资源限制、不可用、异常可报告；禁止宿主 exec；普通 subprocess / `reliability_guard` 不得冒称沙箱。  
- **证据：** 默认永远 `executor_unavailable`。无 timeout/cgroup/process 后端。诚实拒绝优于暗 exec，但 HumanEval-Perturb 客观裁判不存在。  
- **建议：** 增加显式隔离后端（独立进程 + 超时/内存上限），缺省仍不可用，不回退 host。

### A-P-16 — Week-8 / 第 7 节分流未实现

- **严重度：** medium  
- **状态：** confirmed defect  
- **位置：** `analysis.py` `week8_decision` 59–75  
- **触发：** `cli analyze`  
- **论文要求：** 扣除后 $\rho_S$ 不显著 → 不做 P2/P3、第 7 节转负结果；P1 不成立降附录；测量未可靠 →「测量待解决」；Gate 未注册无 pass/fail。  
- **证据：** Gate 保持 `unregistered` 正确；`scientific_conclusion=None` 正确。不读取 excess、不阻断 P2/P3、不写分流状态机。CLI 仍无条件调用 P1–P3。  
- **影响：** 协议决策规则无法从代码复现。  
- **建议：** 显式状态：`measurement_unresolved` / `c3_negative_descriptive` / `not_evaluated` / `evaluated`；禁词保留。

### A-P-17 — 成本口径把字符数当作 Prefill token

- **严重度：** medium  
- **状态：** confirmed defect  
- **位置：** `repair.py` 42  
- **触发：** `run_repair(..., new_prefix=...)`  
- **论文要求：** §3 成本分列解码 token、额外 Prefill token。  
- **证据：** `extra_prefill_tokens=len(new_prefix)`。  
- **影响：** Repairability/成本曲线单位错误。  
- **建议：** 用 tokenizer 计 token；无 tokenizer 则字段为 null 并写 `null_reason`。

### A-P-18 — 追踪账本与冻结 hash 不能支撑「逐条覆盖」

- **严重度：** medium  
- **状态：** confirmed defect（账本）；unconfirmed（hash 算法）  
- **位置：** `.planning/PAPER_TRACEABILITY.md` 6–8、73 行起全部 `TBD`/`unimplemented`；`.planning/audits/round-01/VERSION.md` 第 5 行  
- **触发：** 按 GOAL §4 用账本验收  
- **论文/GOAL 要求：** 每条实质段落有需求、实现符号与行号、验证证据。冻结 hash 可核验。  
- **证据：** 账本自述「仓库尚无生产模块」。本审查独立哈希未复现 `532e05a8…`。工作树含 `models/generate.py`、`collect.py`、`adapters.py`、`test_generate_loop.py`、`test_tiny_cache.py`（VERSION 亦写 generate/cache 后加）。  
- **影响：** 无法证明审查与作者声称的是同一快照；覆盖率声明无效。  
- **建议：** 公布 hash 命令并重算；按本报告回填账本，未实现行保持 `executable_function` 不得改成 background。

### A-P-19 — T1 官方 500 题 / 改名 / 未见组合 / 三轨迹采集缺失

- **严重度：** high  
- **状态：** confirmed defect（代码）；全量官方跑 pending_server  
- **位置：** `t1_official.py`（仅 `load_igsm_snapshot`）；`t1_config.py`（只校验）；`cli.py` 只 `load_t1_fixture`；无 rename/unseen 构造器；无 seed=0/1/pert 采集  
- **论文要求：** §7/§9：iGSM op 四档、500 题、两模型、三条基础轨迹；跨改名与未见依赖组合。  
- **证据：** 有快照加载与 op 校验；无生成器导出、无官方 CoT 事件解析、无改名编辑、CLI 不读 official。  
- **影响：** T1「解析真值基石」未接到实验入口。  
- **建议：** prepare 读官方快照目录；事件解析与改名变体进同一 `base_group_id`。

---

## 6. 已对齐、不升格为缺陷的项

| 项 | 证据 | 标签 |
|---|---|---|
| 官方 iGSM 用 template 不用 G；排除 `(-1,0,0,0)`；mod 23 | `t1_official.py` 18–19、24–25、62 | non-defect |
| 夹具不得标 official | `t1_fixture.py`、`schema.Task.validate` 138–139 | non-defect |
| GSM-Plus 锁定 test、solution≠DAG | `t2_gsm_plus.py` 40–51 | non-defect |
| Hotpot supporting_facts 显式非完备 DAG | `t3_hotpot.py` 35–38 | non-defect |
| MuSiQue 不去重丢掉 unanswerable | `t3_musique.py` 66–68 | non-defect |
| 空分母/缺 sham → null；signed excess 不截断 | `measure.py` 87–98、测试 `test_signed_excess_not_clipped` | non-defect |
| 保形顺序统计与 $+\infty$ | `calibrate.py` 19–27；手算 $\alpha=0.4,N=4\to k=3\to q=0.3$ 与测试一致 | non-defect |
| 直接迁移拒 4096/3584，不静默补零 | `transfer.py` 9–16 | non-defect |
| 交换代数形式 | `apply_swap`；测试 `[1,0]+Π([0,1]-[1,0])=[1,1]` | non-defect |
| Gate 0–2 默认 unregistered；不输出科学结论 | `week8_decision` | non-defect |
| REST-01/02/03 禁词与联合编辑反例 | `FORBIDDEN_CLAIMS`；`joint_edit_counterexample` | non-defect |
| 修复拒 Cone Gate / verifier fallback | `RepairRecord.__post_init__` | non-defect（符合 excl） |
| 代码评分不回退 host exec | `executor.py` / `scoring.score_code` | non-defect（后端仍缺，见 A-P-15） |
| 事件身份不含值 | `EventIdentity` | non-defect |
| RNG 流分离（库层） | `StreamBank.NAMES` | non-defect |

---

## 7. 结论

在当前工作树上，**论文实质条款多数没有「需求—实现—证据」三元组**。忠实的是若干可单测的代数/协议卫兵；被替换的是训练、采集、干预执行、修复、跨域真值、P1 统计与附录分析。在修复 A-P-01–A-P-07、A-P-08–A-P-10、A-P-12 之前，不能声称 C1–C4 或 T1–T4 已按原文实现。

空报告无效；本文件列出的 confirmed defect 即为本通道结论。
