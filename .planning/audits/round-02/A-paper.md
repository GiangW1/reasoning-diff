# 审查报告 A：原文一致性（paper consistency）— round-02

| 字段 | 值 |
|---|---|
| **agent / task id** | independent-reviewer-A / paper-consistency / cursor-subagent / round-02 |
| **审查时间** | 2026-09-21 00:44–01:35（UTC+8） |
| **声明冻结 hash** | `2676a0983f6b42148202eedfbfaea44ce207d1fd386b8d47cbc909e983c5cc38` |
| **hash 方法（声明）** | SHA-256 over relative POSIX paths + bytes of `src/reasoning_diff/**/*.py`, `tests/**/*.py`, `pyproject.toml`（55 files） |
| **本审查实测代码 hash** | **HASH_MISMATCH**。范围内文件数为 **55**，与声明一致。对排序后的 POSIX 相对路径 + 文件字节尝试了：`path+bytes`、`path\\0+bytes`、`path\\n+bytes`、`path\\n+len\\n+bytes`、仅拼接字节、hex digest 串联、`path+digest`、`path+hexdigest`、sha256sum / `*path` 清单再哈希、JSONL path→sha256、长度前缀、按 glob 分组排序与未排序。均不等于声明值。本审查的 `path+bytes`（全路径字典序）结果为 `4ce6fac512f19e2d4d03b6821d9fa2b46632d19265fd5a272b8910fde52ea992`。**审查对象是下方清单中的当前工作树字节，不是一个已核验的冻结快照。** |
| **本审查实测 paper hash** | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`（`Reasoning-Diff-修订方案-v3 (1).md`，与 `PAPER_TRACEABILITY.md` §0 登记一致） |
| **本审查实测 protocol hash** | `83A9142DBA4F7FCD337A70EF8CD1A847ED7EB7FF110F2D77F466387AB491391D`（与账本一致） |
| **本审查实测 GOAL hash** | `B9E0A8EA3FC87BF00F1949BD8201407E097EF3E25660173275BA11E42A39EB7E`（与账本一致） |
| **本审查实测 REQUIREMENTS hash** | `E481EB84664E1F71EE5551FB3451F764B8FB7D21691B89E5DFFC67773B3090C4`（**与账本登记 `B0228A57…` 不一致**，见 A2-21） |
| **git_head（VERSION.md）** | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作树脏；不单独当作冻结） |
| **范围** | 论文全文 §0–12 + 公式/表/附录 S1–S4；`docs/EXPERIMENT_PROTOCOL.md`；`docs/CURSOR_GOAL_PROMPT.md` §5（并读目标文档前部以定位 §5）；`.planning/PAPER_TRACEABILITY.md` 约定/计数 + 可执行/数学行抽样；`.planning/REQUIREMENTS.md`；全部 `src/reasoning_diff/**/*.py`。对照测试只读，用于判断“被测行为是公式还是替身”。**未读**其他通道审查报告。 |
| **生产代码** | 未修改 `src/`、`tests/`、`pyproject.toml`、论文。仅写本文件。 |

**总判：** 当前树是**库函数碎片 + 夹具冒烟 CLI**，不是论文 §4 / §8.2 要求的科学评测实现。若干定义在孤立函数上写对了（$R_{\mathrm{task}}$ 祖先、$S/M$ 空分母→null、交换式、保形分位数、直接迁移拒维、Gate 保持未注册、`scientific_conclusion=None`）。采集、双头训练、前瞻生成干预、嫁接重算、T2/T3 合法编辑+更新真值、公平基线、P1 统计、附录拟合，在科学入口上仍是**空实现或概念替换**。`.planning/PAPER_TRACEABILITY.md` 把这些条款标成 `implemented_local` 并以“pytest 65 passed”作验收，**作者不能当唯一验收人**；绿测不构成原文符合。假说不要求正结果——本通道不因 P1–P3 无正结果判缺陷。Gate 0–2 保持 `unregistered`，此项**不是缺陷**。

---

## 1. 逐文件覆盖

每行：路径（实际读到的行区间）— 对照条款 — 结论。行数按磁盘 `splitlines()`。

| 文件 | 行 | 对照条款 | 覆盖结论 |
|---|---:|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 1–517 | 全文 §0–12、公式、表、附录 S1–S4、参考文献 | 已通读。条款映射见 §4。 |
| `docs/EXPERIMENT_PROTOCOL.md` | 1–86 | 标签/划分/干预/P1–P3/Gate/本机边界 | 已通读。Gate 默认 null 与代码一致。 |
| `docs/CURSOR_GOAL_PROMPT.md` | 1–100；§5 = 73–91 | GOAL §5.1–5.15 | 十五条中 1–2、7–13、15 在科学入口被降级或缺失。 |
| `.planning/REQUIREMENTS.md` | 1–76 | DATA/MEAS/MODEL/PROBE/… 与 atomics | 复选框全空；状态表写 `implemented_local`。文件 hash 已偏离账本。 |
| `.planning/PAPER_TRACEABILITY.md` | 1–80 约定；75–113、200–239、382–410、400–479 行抽样；528 行矩阵未逐字复读 | 账本不得当实现证据 | 可执行行普遍 `implemented_local` + pytest，映射常指到无关符号。 |
| `pyproject.toml` | 1–26 | §8.1 模型依赖；GOAL §5.15 | 仅 `numpy`。无 `torch`/`transformers`。无 `--eval-mode scientific`。 |
| `src/reasoning_diff/__init__.py` | 1–5 | — | 只导出 `SCHEMA_VERSION`。 |
| `src/reasoning_diff/__main__.py` | 1–4 | OPS-01 | `python -m` 入口存在。 |
| `src/reasoning_diff/schema.py` | 1–371 | §2.1–2.3 身份/枚举；GOAL §5.3 | 身份不含值。outcome/scan/graph/split/T4 枚举齐全。契约 ≠ 流水线语义。 |
| `src/reasoning_diff/graphs.py` | 1–44 | §2.2 $R_{\mathrm{task}}$；§2.5 cone | 祖先与相交掩码正确。默认 cone 走任务祖先，不是行为头 $\hat R^{\mathrm{val}}$。 |
| `src/reasoning_diff/events.py` | 1–125 | §2.2–2.3；§4.1 对齐与 $R^{\mathrm{surf}}$ | 身份对齐正确。`merged`/`strategy_changed` 恒 `[]`。`surface_mentions` 搜 `premise_id`，不是名称/符号引用。仅夹具正则解析。 |
| `src/reasoning_diff/edits.py` | 1–141 | §7 T1 重算；GOAL §5.2 | 表达式重算 + 隔离数值替换可用。无改名/算子逆转/增删约束/Spec 编辑。 |
| `src/reasoning_diff/measure.py` | 1–242 | §2.6 $S/M/\rho$；§3 TO/CSP；REST-03 | 差集、空分母、缺 sham→null、signed excess 正确。TO/CSP 无对错分层、无噪声配对。CLI 误用第一节点祖先（见 A2-03）。 |
| `src/reasoning_diff/analysis.py` | 1–131 | §2.6 P1–P3；§7 分流；附录 S2–S4 | P1 非 logistic。`cone_fit`/`retrieval_scatter` 为空壳。Week-8 禁词与 Gate 未注册正确；无论文分流树。 |
| `src/reasoning_diff/interventions.py` | 1–91 | §2.4 交换/对照/INLP/救援 | 交换式与“必须提供主干预范数”正确。无 $\mathrm{IE}_Z$ 期望。无 C-layer 层选择。库函数未接到生成。 |
| `src/reasoning_diff/probes/bilinear.py` | 1–74 | §4.2 $\sigma(h^\top UV^\top e+b)$，$r=64$，$\lambda_{FN}=10$ | 前向与加权 BCE 形式正确。有 `fit`。CLI 用 $I_4$ 且两头同一 $Y$。无 $e_j$ 池化、无层选。 |
| `src/reasoning_diff/probes/boundary.py` | 1–23 | §4.2 Hidden=256 ReLU | 架构符合。**无训练**、无句法监督。 |
| `src/reasoning_diff/probes/calibrate.py` | 1–35 | §2.5 命题 2 | $\lceil(N+1)(1-\alpha)\rceil$ 与 $+\infty$ 正确。CLI 传入的不是 $1-\hat p$。 |
| `src/reasoning_diff/probes/__init__.py` | 1–3 | — | 再导出。 |
| `src/reasoning_diff/baselines.py` | 1–44 | §8 文本/注意力/四档自述；GOAL §5.7 | 子串打分替身。注意力函数无 dev 阈值。监督 verbalizer 不是同划分训练器。 |
| `src/reasoning_diff/transfer.py` | 1–40 | §5 Fig.2c；附录 S3；GOAL §5.9 | 直接迁移拒 4096/3584。线性映射存在。未先共同维再 Procrustes；未接到真实两输入探针。 |
| `src/reasoning_diff/repair.py` | 1–57 | §3 Repairability/RR；§9 嫁接；GOAL §5.13 | 掩码名枚举在。`run_repair` 不生成、不 Prefill 模型、不重算。`extra_prefill_tokens=len(new_prefix)` 是字符数。 |
| `src/reasoning_diff/cli.py` | 1–419 | §4 流水线；§8.2 scientific | 八阶段均为夹具/硬编码冒烟。无 `--eval-mode scientific`。 |
| `src/reasoning_diff/models/adapters.py` | 1–29 | §8.1 模型卡/revision | 两张冻结卡。无加载、无 tokenizer、无采集。 |
| `src/reasoning_diff/models/collect.py` | 1–47 | §4.2 $h_i/e_j$；GOAL §5.6/5.10 | tiny 采集**不取隐状态**。干预是 `+0.01`，不是 $\Pi_Z$ 交换。 |
| `src/reasoning_diff/models/features.py` | 1–43 | §2.4 三时机；GOAL §5.6 | 跨界 token 排除正确。库函数可用。CLI collect 仍写 dummy 特征。 |
| `src/reasoning_diff/models/generate.py` | 1–56 | §8.2 自然轨迹 | 显式 decode 循环存在。CLI 不用。无隐状态/层切片。 |
| `src/reasoning_diff/models/tiny.py` | 1–92 | 本机 hook 边界 | 随机 Qwen2/3 + 末 token resid_post。不是论文模型路径。 |
| `src/reasoning_diff/models/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/tasks/catalog.py` | 1–39 | §7 适配入口 | 快照分发。不生成 500 题。 |
| `src/reasoning_diff/tasks/t1_official.py` | 1–83 | §7 T1；template≠G | 快照加载拒绝裸 `G`、排除共享 RNG、默认 mod 23。无 500 题生成、无官方 CoT 解析。 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 1–20 | 官方/夹具分离 | 拒绝 `official`。成立。 |
| `src/reasoning_diff/tasks/t1_config.py` | 1–21 | op∈{5,10,15,21}，n=500 | 配置校验。无数据生成。 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 1–70 | §7 T2；GOAL §5.2 | 无侧车则假前提（前 8 字）。有侧车时 `apply_formula_edit` 走值编辑+重算。无算子逆转/增删条件。 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 1–51 | §7 T2；评测专用 | test-only 锁正确。前提=题目前 12 字。无合法编辑、无更新真值。 |
| `src/reasoning_diff/tasks/t2_noop.py` | 1–80 | §7 T2-noop | 可造配对与分层元数据。无注入句值扰动扫描。无 T1 图规则等价注入。 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 1–59 | §7 T3；supporting_facts≠DAG | 标记正确。`document_edit` 只回 dict，不产出新 Task/真值。 |
| `src/reasoning_diff/tasks/t3_musique.py` | 1–69 | §7 T3 组成引用 | 保留 answerable/unanswerable。`expression="composition_reference"` 不可重算。无文档编辑。 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 1–35 | §7 HumanEval-Perturb；GOAL §5.15 | 前提=prompt 前 40 字。无 Spec 编辑包。评分走不可用执行器。 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 1–33 | §7 T4；Fig.6 | 四类状态强制区分。前提=前 10 字。无相图、无轨迹策略检测。 |
| `src/reasoning_diff/tasks/__init__.py` | 1–1 | — | 注释。 |
| `src/reasoning_diff/executor.py` | 1–59 | GOAL §5.15 | 禁止宿主 exec。默认 `executor_unavailable`。无超时/资源限制的真实隔离后端。 |
| `src/reasoning_diff/scoring.py` | 1–30 | §3 域内评分 | 数值/QA 精确匹配。代码必经隔离接口。 |
| `src/reasoning_diff/splits.py` | 1–75 | §4.1 共组；GSM-Plus test-only | 六角色 + 家族共组。默认比例未预注册。 |
| `src/reasoning_diff/rng.py` | 1–53 | GOAL §5.4 | sample/direction/perturb/bootstrap/split 分离。CLI 基本不用。 |
| `src/reasoning_diff/io.py` | 1–127 | 清单/哈希 | 原子写、拒 NaN。 |
| `src/reasoning_diff/artifacts.py` | 1–83 | 拒 `latest` | run_spec/manifest。 |
| `tests/conftest.py` | 1–11 | — | 夹具路径。 |
| `tests/test_cli_pipeline.py` | 1–29 | §4 流水线 | 只断言八阶段 exit 0 与 `not_evaluated`。 |
| `tests/test_science.py` | 1–97 | 校准/迁移/交换/Week-8 | 测库函数微例，不测训练/采集/嫁接语义。 |
| `tests/test_measure.py` | 1–40 | $S/M$、联合编辑反例 | 与公式一致。 |
| `tests/test_review_regressions.py` | 1–315 | 上轮回归 | 锁住若干库函数修补；**同时固化** P1 非 logistic 启发式、repair 不生成、verbalizer 契约即可。 |
| `tests/test_tracer_t1_prepare.py` | 1–100 | T1 夹具准备 | 覆盖身份/重算/空分母。不验 CLI 祖先/scan_state。 |
| `tests/test_t1_official.py` | 1–31 | template≠G | 快照形状。 |
| `tests/test_t2_gsm.py` | 1–33 | T2 | 有侧车时验答案变为 8。不验算子逆转。无侧车假前提未被当缺陷。 |
| `tests/test_t3_t4.py` | 1–40 | T3/T4 | 明确 supporting_facts 不是 DAG；不验编辑真值。 |
| `tests/test_artifacts.py` | 1–73 | I/O | 工程。 |
| `tests/test_generate_loop.py` | 1–17 | 可重放采样 | tiny decode。 |
| `tests/test_tiny_hooks.py` | 1–27 | hook 清理 | 本机接口。 |
| `tests/test_tiny_cache.py` | 1–25 | 缓存隔离 | `intervene_tiny` 是平移，不是交换。 |

第三方库：审查了本项目对 `numpy` /（未声明的）`torch`+`transformers` 的使用假设，未审查依赖源码。

夹具抽读：`tests/fixtures/t1_tiny.json`（全文）、`t2_gsmplus_one.json`、`t3_humaneval_one.json`。

---

## 2. 已执行检查与结果

| # | 检查 | 结果 |
|---|---|---|
| C1 | 通读论文 0–12 节、公式、表、附录 S1–S4、参考文献清单 | 完成。实质条款见 §4。 |
| C2 | 通读 `docs/EXPERIMENT_PROTOCOL.md` 标签/划分/干预/P1–P3/Gate/本机边界 | 完成。Gate 保持 null 与实现一致（非缺陷）。 |
| C3 | 通读 GOAL §5 十五条高风险索引 | 完成。第 1–2、7–13、15 条在科学入口被降级或缺失。 |
| C4 | 阅读 `PAPER_TRACEABILITY.md` 约定、计数，并抽样 TR-0001–0038、TR-0125–0164、TR-0307–0347、TR-0349–0404 | 账本把可执行缺口标成 `implemented_local`，验证列写 pytest 65。**不能**作为覆盖证据。 |
| C5 | 逐文件阅读全部 `src/reasoning_diff/**/*.py` | 完成。见上表。 |
| C6 | 对照公式手核：$R_{\mathrm{task}}$、TO、$S/M$、交换、$a(X)$ 分位数、直接迁移、P1、cone | $R_{\mathrm{task}}$/差集/交换/分位数/拒维度：**库函数层符合**。P1：**不符合**（A2-04）。cone 默认任务祖先。TO 公式在 `lcs_overlap` 符合。 |
| C7 | 对照 §4.1 伪代码与 CLI `prepare/collect/label` | 无多 seed `generate`、无 `allowed_edits` 全扫描。`collect` 写 $I_4$。`prepare` 用节点真值拼文本当“轨迹”。 |
| C8 | 对照 §4.2 / §8 探针与基线 | 双线性可拟合，但入口用假特征/假标签。边界 MLP 无训练。基线是子串。 |
| C9 | 对照 §2.4 / §6 干预与解耦任务构造 | 无来源—数值解耦资产。无层内 hook/KV 协议执行。CLI `geometry_only`。tiny 是 `+0.01`。 |
| C10 | 对照 §7 / GOAL §5.2 T1–T4 读取+合法编辑+更新真值 | T1 快照/夹具值编辑部分成立。T2 仅侧车数值编辑。T3/T4 编辑与真值路径缺失或假前提。 |
| C11 | 对照附录 S1–S4、C4 掩码、连续编辑 $k\in\{1..5\}$、失效相图 | 仅有函数名/枚举/空返回。 |
| C12 | 抽读测试，判断其是否把替身固化为“已实现” | 是：`test_full_cli_smoke`、`test_verbalizer_supervision_contract`、`test_repair_reprefills_*`、`test_c01_auc_*`、`test_pipeline_consumes_upstream` 均不触及论文语义。 |
| C13 | 独立重算论文/协议/GOAL SHA-256 | 论文与协议、GOAL 与账本一致。REQUIREMENTS 不一致。 |
| C14 | 独立重算声明代码冻结 hash | **HASH_MISMATCH**。 |

## 3. 未执行检查及原因

| # | 未执行 | 原因 |
|---|---|---|
| N1 | `pytest` / CLI 端到端实跑 | 本通道是原文对照。作者声称 65 passed；绿测不能当原文符合。本报告不声称测试通过。 |
| N2 | 真实 Qwen3-8B / R1-7B、GPU、官方全量数据 | 协议 §7：科学结论 `pending_server`。且代码中**没有**可调用的真实权重采集路径。 |
| N3 | 人工复核事件映射小集 | 无复核 UI/抽样协议实现。 |
| N4 | 用独立数据重拟合探针/INLP/Procrustes | 科学入口无真实 $H/E$ 与标签矩阵。 |
| N5 | 其他审查通道报告交叉 | 任务禁止阅读。 |
| N6 | `PAPER_TRACEABILITY.md` 全部 528 行逐字复读 | 已读约定与高风险可执行/GOAL/REQUIREMENTS 行。剩余多为同一模板重复。 |

---

## 4. 论文条款 → 实现映射（或缺失）

类别：`exec` 可执行功能；`math` 公式；`proto` 协议；`hyp` 待测假说（不要求正结果，但要有测量入口）；`bg` 背景；`excl` 用户排除。

状态：`ok-lib` 库函数忠实、未接到科学入口；`stub` 名称在、语义无；`subst` 偷换概念；`missing` 无符号；`ok` 协议持守。

| 来源 | 行 | 条款 | 类 | 实现 | 状态 |
|---|---|---|---|---|---|
| 论文 0 | 13–25 | C1–C4 可执行主张 | exec | 探针/干预/分析/修复均冒烟 | stub |
| 论文 0 | 16 | REST-01 可解码≠已决定 | proto | `FORBIDDEN_CLAIMS` / `scientific_conclusion=None` | ok |
| 论文 1 | 34–35 | 检索余弦 vs 答案变 | exec | `retrieval_scatter` 只汇总传入对 | stub |
| 论文 1 | 38 | 修复解码/Prefill/耗时 | exec | `Cost` 字段有；repair 填字符长度 | subst |
| 论文 2.1 | 62–64 | $P$、轨迹、$v(s_i)$ | math | schema + 夹具解析 | ok-lib |
| 论文 2.2 | 68–70 | $R_{\mathrm{task}}$ 祖先 | math | `graphs.ancestors` | ok-lib |
| 论文 2.2 | 74–78 | $R_{\mathrm{behavior}}$ 固定流+允许扰动 | math | `build_labels` 有限扫描字段；CLI 单编辑且把 no_change 标成已知负 | subst |
| 论文 2.3 | 87 | $R^{\mathrm{surf}}$ | exec | 正则搜 `premise_id` | subst |
| 论文 2.3 | 88 | 消失/合并/策略分岔 | proto | `removed` 有；`merged`/`strategy_changed=[]` | stub |
| 论文 2.4 | 96–98 | $H'=H^b+\Pi_Z(H^d-H^b)$ | math | `apply_swap` | ok-lib |
| 论文 2.4 | 100–102 | $\mathrm{IE}_Z$ | math | 无期望估计 | missing |
| 论文 2.4 | 106–108 | 前瞻 hook/KV/前缀 | exec | tiny `+0.01`；CLI 随机/特征行向量 | subst |
| 论文 2.4 | 110 | 步前/数值前/步尾 | exec | 库函数区分；collect 丢弃真实 $H$ | stub |
| 论文 2.4 | 114–117 | C-rand / C-layer 同幅度四项 | exec | 范数匹配在；C-layer 无弱层选择；CLI 不报告四项结局 | subst / missing |
| 论文 2.5 | 121–125 | cone / Oracle / 行为掩码 | math | `dirty_cone`/`oracle_mask`/`behavior_mask` | ok-lib |
| 论文 2.5 | 127–130 | 命题 1 + REST-03 | math | $xy$ 反例夹具 | ok-lib |
| 论文 2.5 | 132–139 | $a(X)$、分位数、$+\infty$ | math | `sequence_score`/`conformal_threshold` | ok-lib |
| 论文 2.5 | 141–142 | 原轨迹槽位、禁重拓扑 | exec | 无嫁接执行 | missing |
| 论文 2.6 | 148–156 | $S,M,\rho$，空分母 N/A | math | `dependency_densities` | ok-lib |
| 论文 2.6 | 158 | 噪声先扣除 | proto | 库函数缺协议→null；CLI sham 传 `noise_set=[]` | subst |
| 论文 2.6 | 164 | P1 logistic + 偏相关 + bootstrap | math | `length+0.01*op` 或 OLS | subst |
| 论文 2.6 | 165 | P2 配对 + 污染位置 | exec | 只减两个标量 | stub |
| 论文 2.6 | 166 | P3 Δacc + 对照 + 非目标 | exec | 只减正确率；CLI 写 None | stub |
| 论文 2.6 | 168 | REST-02 | proto | `causal_reverse_claim=False` | ok |
| 论文 3 | 176–186 | TO_all/clean、CSP、覆盖、脏变、P/R/F1 | math | TO/CSP/覆盖/脏变有；无探针 P/R/F1；无对错分组 | stub / ok-lib |
| 论文 3 | 188 | TO/CSP 噪声参照与比值 | proto | 无 | missing |
| 论文 3 | 190 | 干预三项并列、前瞻/回溯分列 | proto | `intervention_report` 接受三 dict；CLI 硬编码 geometry_only | stub |
| 论文 3 | 194–200 | Repairability、RR、成本分列 | math | 两公式有；成本未测 | stub |
| 论文 4.1 | 232–253 | 双标签流水线；NL 单调对齐；共组 | exec | 无 generate 循环；无 NL 对齐 | missing |
| 论文 4.2 | 257–267 | MLP 训练、双头、池化 $e_j$、60–75% 层、改名/未见组合 | exec | 架构常数在；训练/池化/层选/泛化测试无或假 | stub |
| 论文 5 Fig.1–2 | 291–299 | 热力图、三时机比较、跨模型迁移入口 | exec | 无导出 | missing |
| 论文 6 | 301–313 | 解耦资产、前瞻交换、INLP、救援 | exec | 向量几何 + 记录字段 | stub |
| 论文 7 | 315–329 | P1–P3 测量入口（不要求正结果） | exec | 函数签名在；analyze 写 `p1=p2=p3=None` | stub |
| 论文 8 | 331–341 | 注意力/四档 verbalizer/监督文本 | exec | 子串 | subst |
| 论文 9 / Table 1 | 343–355 | 五条主对照 + 三条附录掩码实跑 | exec | 枚举名 | stub |
| 论文 Fig.6 | 353 | 失效相图五类 | exec | T4 状态枚举 ≠ 相图 | missing |
| 附录 S1 | 357–359 | $k\in\{1..5\}$ 连续编辑 | exec | 无 | missing |
| 附录 S2 | 361–367 | 两参数锥拟合 | math | `cone_fit` 返回 `r2=None` | stub |
| 附录 S3 | 371–373 | 共同维 + Procrustes | exec | 两函数分立，无流水线 | stub |
| 附录 S4 | 375–377 | 嵌入余弦散点 | exec | 不计算嵌入 | stub |
| 论文 7 数据 | 399–409 | T1–T4 假设专用资产 | exec | 读取器+假前提；T1 无生成器 | stub |
| 论文 8.2 | 419–431 | `--eval-mode scientific` | exec | 不存在该开关 | missing |
| 论文 9 | 435–445 | 第一周三轨迹/50 干预冒烟 | exec | 夹具单编辑 | stub |
| 协议 §6 | 70–80 | Gate 0–2 未预注册 | proto | `unregistered` / 无阈值 | **ok** |
| GOAL §5.14 | 90 | 不把 fixture 写入科学结论 | proto | `not_evaluated` / `scientific_conclusion=None` | **ok** |

---

## 5. Findings

### A2-01 — 科学 CLI 把论文流水线换成夹具冒烟

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `src/reasoning_diff/cli.py` `cmd_prepare` 78–196；`cmd_collect` 199–226；`cmd_fit` 250–278；`cmd_calibrate` 281–294；`cmd_intervene` 297–335；`cmd_repair` 338–344；`cmd_analyze` 347–371 |
| **Trigger** | 对照论文 §4.1 伪代码（232–248）与 §8.2 scientific 流程（422–429） |
| **Paper requirement** | 自然轨迹 `generate(P, seed)`；对每个前提的 `allowed_edits` 再生成；采集隐状态；拟合并校准 $1-\hat p$；前瞻交换后自回归；无门控嫁接重算；分析 P1–P3 |
| **Repro / evidence** | `prepare` 用节点真值拼 `"q = 0\\n"` 当轨迹（89–94）。`collect` 写 `{"dummy": I_4, "H": I_4, "E": I_4}`（221）。`fit` 在 $I_4$ 上训练且两头共用同一 `y`（262–275）。`calibrate` 默认 `[0.1,0.2,0.3,0.4]` 或用 **probe loss** 当分数（287–292）。`intervene` 状态 `"geometry_only"`，四项结局全 `None`（323–332）。`repair` 调 `run_repair(..., generated_tokens=0)`（342）。`analyze` 固定 `p1=p2=p3=None`（364–367）。无 `--eval-mode scientific`。 |
| **Impact** | 八阶段 exit 0 不能代表 C1–C4 可执行。账本 TR-0014/TR-0125/TR-0327 把这些入口标成 `implemented_local` 是误覆盖。 |
| **Suggested fix** | 科学模式必须走模型 generate、真实 $H/E$、分头标签、轨迹级 $a(X)$、生成式干预与嫁接。夹具冒烟须显式 `source_kind=fixture` 且不得写入 `scientific_conclusion`。 |
| **Status** | **confirmed defect** |

### A2-02 — 有限单次扫描的 `no_change` 被标成已知负标签

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` 97–115；对照 `measure.build_labels` 43–53 |
| **Trigger** | 论文 2.2 L78：“不把一次未变化记为已经排除全部允许扰动。” §4.1 L251：有限扫描“未观察到变化”与“已覆盖全部允许扰动且没有变化”必须分记。GOAL §5.3。 |
| **Paper requirement** | `scan_state` 区分 `no_response_observed_in_scan` / 穷尽后的已知负；未知不作负标签。 |
| **Repro / evidence** | `prepare` 只做**一个**前提的**一次**值编辑。却写 `scan_state="observed_response" if outcome in {"changed", "no_change"}`（111）。`build_labels` 把 `no_change ∧ observed_response` 当作 `behavior_label=0, behavior_known=True`。库函数测试 `test_b02_*` 只覆盖调用方传入 `no_response_observed_in_scan` 的情形，不覆盖 CLI 自己把该字段写错。`Edit.exhaustive` 默认 `False`（`schema.py` 344）。 |
| **Impact** | 经验 $R_{\mathrm{behavior}}$ 与 $M$（漏读）会被一次无变化高估。C3 差集统计从入口就偏。 |
| **Suggested fix** | 非穷尽扫描的 `no_change` 必须是 `no_response_observed_in_scan` / `behavior_known=False`。只有声明的允许扰动集合扫完才写已知负。 |
| **Status** | **confirmed defect** |

### A2-03 — CLI 密度把“第一节点祖先 ∪ 曾变化前提”偷换成 $\rho_S(T)$

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` 145–151；`cmd_label` 240–244 |
| **Trigger** | 论文 2.6 L148–156：$\rho_S(s_i)$ 逐步计算再对轨迹平均。协议 §2.6：噪声参照必须有配对机会。 |
| **Paper requirement** | 逐步 $S=B\setminus T$；噪声来自同题不同随机流的共同支持，缺协议则 excess=null。 |
| **Repro / evidence** | `task_set=next(iter(anc.values()), set())` 只取字典**第一个**节点的祖先。`behavior_set` 是“任一 observation 值为 changed 的 premise_id 集合”，不是逐步 $R_{\mathrm{behavior}}(s_i)$。开启 sham 时 `noise_set=[]`（150），于是 $N=\emptyset$，`noise_s=0`，excess 被算成 raw−0，而不是 null 或真实 sham 密度。`label` 阶段不传 `sham_protocol`，excess 又变回 null，两阶段口径不一致。 |
| **Impact** | 即使夹具碰巧只有一个计算节点（`t1_tiny` 的 `q`），协议仍是错的；多节点任务会系统性错。sham 开关把“已扣除噪声”伪装成 0 参照。 |
| **Suggested fix** | 逐步调用 `dependency_densities`；轨迹 $\rho$ 对事件平均。sham 必须填入实际 sham 变化集合，或缺协议保持 null。禁止 `noise_set=[]` 表示“已测噪声”。 |
| **Status** | **confirmed defect** |

### A2-04 — P1 不是控制链长/op 的 logistic，也没有偏相关

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `analysis.py` `p1_incremental` 33–61；`tests/test_review_regressions.py` `test_c01_auc_is_rank_and_permutation_invariant` 198–208 |
| **Trigger** | 论文 2.6 表 P1（L164）；协议 §5 P1；GOAL §5.12；C3-01 |
| **Paper requirement** | 控制链长与 op 后，$\rho_S$ 对逐题正确性的 **logistic AUC** 及与链长的**偏相关**，附 bootstrap / 问题级区间。留出题目比较“链长+op 基线”与加入 $\rho_S$ 的增量。 |
| **Repro / evidence** | 无 `held_out` 时：`base = length + 0.01*op`，`full = base + rho`（43–44）。这是手写线性分数，不是 logistic。有 `held_out` 时：`np.linalg.lstsq` 把 **0/1 的 y** 当线性因变量（27–30, 52–53），是线性概率模型，不是 logistic，也不是偏相关。`bootstrap_cluster`（120–131）存在但未接入 P1。CLI `analyze` 根本不调用 P1。回归测试把“`rho==length` 则 `delta_auc==0`”锁成通过条件，固化了启发式。 |
| **Impact** | 任何将来写入报告的 P1 数字都不是论文定义的统计量。这是概念替换，不是“待服务器拟合”。 |
| **Suggested fix** | 实现（或显式依赖）logistic；报告偏相关与问题级 bootstrap；默认路径禁止 `0.01*op` 启发式。测试必须用独立 oracle（手算 logistic AUC），不能只测置换不变。 |
| **Status** | **confirmed defect** |

### A2-05 — 探针/采集：无 $h_i$、$e_j$ 池化、层选；双头共用假标签；边界 MLP 不训练

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `models/collect.py` 11–25；`cli.py` 221, 262–275；`probes/boundary.py` 1–23；`probes/bilinear.py` 7–58 |
| **Trigger** | 论文 4.2 L257–267；$h_i$ 取 60–75% 层；$e_j$ 为同层 span 均值池化；双头分别学 $R_{\mathrm{task}}$ 与 $R_{\mathrm{behavior}}$。GOAL §5.6–5.7。TR-0134/0135/0137 标 `implemented_local`。 |
| **Paper requirement** | 从冻结模型自然轨迹取边界隐状态与前提池化；两头分训；边界检测器用 iGSM 句法监督训练。 |
| **Repro / evidence** | `collect_tiny` 返回 token 下标，**从不读** `hidden_states`。CLI `H=E=I_4`。`cmd_fit` 两个 `BilinearProbe` 都 `fit(..., y)`，`y` 来自 behavior 行或单位阵（262–275）。`BoundaryMLP` 只有随机初始化的 `logits`/`predict`，无 `fit`。无 60–75% 层索引，无 span pooling。 |
| **Impact** | C1“从隐状态读出 Read-Set”在可执行路径上不存在。账本把 `bilinear.py` 当作 $e_j$ 与层选的实现是张冠李戴。 |
| **Suggested fix** | collect 必须写出层切片 $H$ 与前提池化 $E$；fit 分头、分标签、分层；BoundaryMLP 接入句法标签训练。未采集时拒绝 `implemented_local`。 |
| **Status** | **confirmed defect** |

### A2-06 — 前瞻干预没有生成、没有来源跟随、没有解耦资产；tiny 用平移冒充 $\Pi_Z$

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `cli.py` 297–335；`models/collect.py` `intervene_tiny` 28–47；全仓库无来源—数值解耦构造器（已搜 `apply_*` / `document_edit` / `make_noop_pair`） |
| **Trigger** | 论文 2.4 L106–117；§6 L305–313；GOAL §5.10–5.11；CAUSAL-02。TR-0158/0159/0331/0400 标已实现。 |
| **Paper requirement** | 目标步首 token 前交换；恢复自回归；评价新生成 $s_k$ 是否跟随 donor。等值不同来源 / 同来源不同值任务对事先列出目标/非目标。C-layer 由开发集弱层确定。报告四项结局相对对照的差值。 |
| **Repro / evidence** | `apply_swap` 公式本身正确（ok-lib）。CLI 只对特征行做几何，写 `status=geometry_only`，`target/nontarget/task_correct/invalid=None`。`c_layer_delta` 的 `layer_basis` 来自 `default_rng(5)` 的随机正交基（316–317），不是弱层。`intervene_tiny`：`patched[:, -1:] = t + 0.01`（36–39）。无 donor/base 任务对、无高层响应矩阵、无错误来源救援对照的执行。`intervention_report` 从未被 CLI 调用。 |
| **Impact** | C2 的主张入口不存在。对照范数匹配只证明“向量可以缩放到同一范数”，不能证明找到依赖子空间。 |
| **Suggested fix** | 实现解耦资产；在步前 hook 施加 $\Pi_Z$；继续解码；按预注册矩阵评分；C-layer 从 dev 曲线选层。几何冒烟不得叫 intervene 成功。 |
| **Status** | **confirmed defect** |

### A2-07 — 局部修复是记录对象，不是嫁接执行

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `repair.py` `run_repair` 34–45；`cli.py` 338–344 |
| **Trigger** | 论文 §3 L194–200、§9 L347–355、附录 S1；GOAL §5.13；REPAIR-01 / TABLE1-01 / CONT-01 / FAIL-01。TR-0037/0145/0319/0334 标已实现。 |
| **Paper requirement** | 无门控：干净文本在当前前缀重新 Prefill，受损槽位自回归重算。主文 5 条对照 + 附录 3 条实跑。同原始 token 预算。失效五类。连续 $k\in\{1..5\}$。 |
| **Repro / evidence** | `run_repair` 要求非空 `new_prefix` 后立刻返回：`generated_tokens=0`，`extra_prefill_tokens=len(new_prefix)`（字符），`failures=[]`，`refilled_prefix=True`。CLI 传入字面量 `"updated prefix"` 与槽位 `["q"]`。`test_repair_reprefills_and_refuses_gate` 只断言布尔字段。无 Table 1 执行器，无 Fig.6，无连续编辑。 |
| **Impact** | Repairability/RR/成本曲线无法测量。C4 附录路径未落地。 |
| **Suggested fix** | 同一执行器跑全部掩码；真实 Prefill/decode；记录逐步合法率与失败类型。字符长度不得写入 token 成本。 |
| **Status** | **confirmed defect** |

### A2-08 — T2/T3/T4 缺少“合法编辑 + 更新后真值”；用题目前 N 字冒充前提

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `t2_gsm_symbolic.py` 42–43；`t2_gsm_plus.py` 22；`t3_hotpot.py` `document_edit` 51–59；`t3_humaneval.py` 21；`t3_musique.py` 40；`t4_boundary.py` 26；`edits.py` 仅 `apply_value_edit` |
| **Trigger** | 论文 §7 L403–407；GOAL §5.1–5.2；DATA-02。TR-0308/0354/0390 标已实现。 |
| **Paper requirement** | GSM-Symbolic/Plus：数值微扰、算子逆转、增删限制条件，并更新真值。Hotpot/MuSiQue：替换关键支撑文档并更新可核查真值。HumanEval-Perturb：Spec 编辑包（新 Spec、新参考、新测试）。T4：策略突变/约束退化用于相图，不是截断字符串。 |
| **Repro / evidence** | 无侧车 Symbolic：`Premise("q0", question[:8], ...)`，`graph_status=unknown`。GSM-Plus：`question[:12]`，无编辑函数。Hotpot：`document_edit` 返回 `changed_premise_ids` dict，**不**构造新 `Task`、不改答案。HumanEval：`prompt[:40]`，文件头写 “spec edits” 但无编辑函数。MuSiQue 节点 `expression="composition_reference"`，`recompute` 会失败。T4：`question[:10]`。全仓库无 operator-reverse / spec-edit 符号。T2 侧车数值编辑是唯一完整路径。 |
| **Impact** | 除 T1 值编辑与 T2 侧车外，行为扫描没有合法 $P'$ 与更新 $v$。GOAL §5.2 未满足。 |
| **Suggested fix** | 每个域提供：读取、合法编辑、新 oracle、事件/未知图状态。缺失外部标注保持 `unknown`，但不得用前 N 个字符当前提并宣称域适配完成。 |
| **Status** | **confirmed defect** |

### A2-09 — 文本 / 注意力 / 四档 verbalizer 被换成子串打分

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `baselines.py` 16–44 |
| **Trigger** | 论文 §4.2 L267、§8 L331–337；GOAL §5.7；BASE-01 / VERB-01 / ATTN-01。TR-0139/0329/0340/0341 标已实现。 |
| **Paper requirement** | 同标签、同划分、截至当前边界的监督文本预测器；注意力均值 / Rollout / dev 头聚合与阈值；零样本 / 5-shot / 反思 / **监督微调** verbalizer，监督档与探针同样本。 |
| **Repro / evidence** | `text_predictor`：`premise[:8] in prefix` → 1.0 否则 0.1。`verbalizer`：`gold[:4] in prefix` → 0.4/0.6。`attention_mean`/`attention_rollout` 无 dev 选头、无阈值、无标签训练。CLI `fit` 不调用 baselines。`test_verbalizer_supervision_contract` 只查 `trained=False` 抛错与 visibility 字符串。 |
| **Impact** | 第 8 节“说不出来”的对照不存在。R4 分流无法计算。 |
| **Suggested fix** | 实现与探针共享划分/前缀的可训练文本头与四档 verbalizer；注意力阈值只在 dev 上选。子串函数不得叫 baseline 实现。 |
| **Status** | **confirmed defect** |

### A2-10 — 附录 S2–S4 与 Fig.1 检索对照只有空壳

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `cone_fit` 102–103；`procrustes` 106–111；`retrieval_scatter` 114–117；`transfer.py` 19–32 |
| **Trigger** | 论文附录 S2 L363–367、S3 L371–373、S4 L375–377（“不得因精简而删除”）。FIT-01 / GEOM-01 / RETR-01。TR-0343–0345 标已实现。 |
| **Paper requirement** | 两参数拟合 $|\mathrm{cone}|/n\approx 1-\exp\{-\lambda(1-x)^\gamma\}$（描述性，不用“定律”）；先独立配对学共同维再 Procrustes；对 $(P,P\oplus\Delta P)$ 算嵌入余弦 vs 答案是否改变。 |
| **Repro / evidence** | `cone_fit` 返回 `{"form": "...", "r2": None, "wording": "descriptive_only"}`，不拟合。`retrieval_scatter` 不计算嵌入。`procrustes` 要求已对齐同形矩阵；`fit_linear_map` 另置，无“先共同维再正交”流水线，无配对计数/是否用标签/测试划分报告。 |
| **Impact** | 附录主张没有测量入口。措辞约束存在不能代替拟合。 |
| **Suggested fix** | 实现拟合与嵌入散点；几何三档（直接 / 无标签 / 监督）分列；报告配对 $n$。 |
| **Status** | **confirmed defect** |

### A2-11 — 结构变化与表面提及仍是替身

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `events.py` `surface_mentions` 13–18；`align_events` 97–102 |
| **Trigger** | 论文 2.3 L87–88；SURF-01 / STRUCT-01。TR-0008/0338 标已实现。 |
| **Paper requirement** | $R^{\mathrm{surf}}$ 记录步骤文本中的前提**名称与符号引用**，与值响应分开，供文本保留/符号替换。消失、合并、版本变化、策略分岔单独计数。 |
| **Repro / evidence** | `surface_mentions` 只对 `premise.premise_id` 做词边界正则。`t1_tiny` 的步骤 `"q = 0"` 不含 `p1`/`p2`，故 `surface_mentions==[]`（`test_b06` 把“不是 parents”当成通过，不要求名称/符号）。`structural["merged"]` 与 `strategy_changed` 恒为 `[]`；发生次数不等时一律 `disappeared`+`added`+`ambiguous`。无 NL 单调对齐（论文 4.1 L252）。 |
| **Impact** | 文本保留/符号替换没有 $R^{\mathrm{surf}}$。合并与策略分岔无法报告。 |
| **Suggested fix** | 用 aliases/渲染名/符号匹配表面提及。实现合并/策略检测或显式 `unknown`，禁止空列表伪装“已分类”。 |
| **Status** | **confirmed defect** |

### A2-12 — TO/CSP 缺对错分层与噪声参照

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `measure.py` `preservation_to_csp` 187–222 |
| **Trigger** | 论文 §3 L176–188；Fig.1 要求噪声参照与正确/错误轨迹分组。 |
| **Paper requirement** | $\mathrm{TO}_{\mathrm{all}}/\mathrm{TO}_{\mathrm{clean}}$，$\mathrm{CSP}$ 在匹配干净事件上；正确与错误轨迹分组；$\mathrm{CSP}_{\mathrm{noise}}/\mathrm{TO}_{\mathrm{noise}}$ 及比值。 |
| **Repro / evidence** | LCS 公式与干净/脏划分在库函数层正确（空父母且图非 complete 不计干净，已修）。函数不接收配对噪声轨迹，不按 `trace.correct` 分层，不输出探针 P/R/F1。CLI 只对夹具真值轨迹调用一次。 |
| **Impact** | Fig.1 不能按论文口径制作。动机图入口缺失。 |
| **Suggested fix** | 增加噪声配对与 correct/incorrect facet；分母/覆盖已有字段保留。 |
| **Status** | **confirmed defect** |

### A2-13 — 校准入口把 probe loss 当作轨迹分数 $a(X)$

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `cli.py` `cmd_calibrate` 287–293；对照 `probes/calibrate.py` 9–35 |
| **Trigger** | 论文 2.5 L132–139：$a(X)=\max_{i,j\in R(s_i)}(1-\hat p_{ij})$，校准单位是完整轨迹/序列。GOAL §5.8。 |
| **Paper requirement** | 用交换单位上的最大 $1-\hat p$；不得把同题重复当独立 $N$。 |
| **Repro / evidence** | 分位数公式本身正确（ok-lib）。CLI 用 4 个常数或 `abs(loss)` 填 `scores`，`unit="full_trace"`。$N=4$ 的假分数会产出一个 $q_\alpha$ 并写入校准产物。 |
| **Impact** | 保形集合大小与漏检保证在入口上无定义。 |
| **Suggested fix** | 只接受按轨迹聚合的 $1-\hat p$；禁止 loss 冒充 nonconformity。 |
| **Status** | **confirmed defect** |

### A2-14 — 账本与 REQUIREMENTS 把未实现条款标成 `implemented_local`（作者自验收）

| 项 | 内容 |
|---|---|
| **Severity** | high |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` 多行，例如 TR-0125（L200）、TR-0134–0137（L208–212）、TR-0158–0159（L233–234）、TR-0308（L383）、TR-0316（L391）、TR-0327–0334（L402–409）；`.planning/REQUIREMENTS.md` 57–74 |
| **Trigger** | GOAL 第四节：账本必须能反向核验；作者不能当唯一验收人。 |
| **Paper requirement** | 可执行条款应对到真实符号与可复查证据。假说不得改成已实现正结果；也不得把未实现功能标成已实现。 |
| **Repro / evidence** | TR-0125 要求多 seed `generate` + `allowed_edits` 全扫描，`impl_file` 却是 `measure.dependency_densities`。TR-0135（$e_j$ 池化）指向 `bilinear.py`（无 pooling）。TR-0158（解耦任务构造）指向 `intervention_report`。几乎所有可执行行的 `verification_method` 是 `python -m pytest -q` / `local pytest 65 passed`。REQUIREMENTS 复选框全未勾，状态表却写 `implemented_local`。REQUIREMENTS 文件 hash 已不是账本 §0 的 `B0228A57…`（本审查 `E481EB84…`）。 |
| **Impact** | 覆盖率被制造成 16/16。独立审查若信账本就会漏检 A2-01–A2-09。 |
| **Suggested fix** | 未接到科学入口的条款改回 `unimplemented` 或 `ok-lib_unwired`。禁止用 pytest 计数关闭可执行行。更新源 hash。 |
| **Status** | **confirmed defect** |

### A2-15 — 隔离执行器只报告不可用；HumanEval 没有可评分裁判

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `executor.py` 22–52；`t3_humaneval.py` 34–35 |
| **Trigger** | 论文 §7 L406：单元测试为客观裁判。GOAL §5.15：可报告不可用，但被声明支持的路径必须有实质后端。 |
| **Paper requirement** | 显式隔离执行器（超时、资源限制）；不回退宿主 exec。 |
| **Repro / evidence** | `IsolatedExecutor.submit` 为 `NotImplementedError`。默认 `UnavailableExecutor`。`SpyExecutor` 仍返回 `executor_unavailable`。禁止宿主 exec 是对的。不存在带 cgroup/超时的后端。HumanEval 因此无法作为 T3 裁判。此项部分可标 `pending_server`（隔离后端部署），但**代码层也没有可配置的真实后端接口实现**，只有拒绝。 |
| **Impact** | T3 代码域评分恒为 null。与“已实现域内评分”不符。 |
| **Suggested fix** | 提供可插入的隔离后端（即使本机默认 unavailable），并实现 Spec 编辑包；不要把 docstring “spec edits” 当实现。 |
| **Status** | **confirmed defect**（实现缺口）；真实沙箱运行 **pending_server** |

### A2-16 — 无 `--eval-mode scientific`；声明依赖装不出论文模型栈

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `pyproject.toml` 10；全仓库无 `eval-mode` / `from_pretrained` |
| **Trigger** | 论文 8.2 L422；§8.1 模型库。MODEL-01。 |
| **Paper requirement** | 科学评测流程开关；冻结 Qwen3 / R1 推理与隐状态采集。 |
| **Repro / evidence** | 依赖只有 `numpy`。`models/*.py` 导入 `torch`/`transformers` 但未声明。无 HF `from_pretrained`。适配器只是 revision 字典。 |
| **Impact** | 按包装不出可运行科学栈。本机 tiny 测试不能冒充 MODEL-01 完成。 |
| **Suggested fix** | 声明可选 `torch`/`transformers` 依赖；实现带 revision 的加载器；CLI 增加 scientific 模式（本机可拒绝无权重）。 |
| **Status** | **confirmed defect**；权重下载 **pending_server** |

### A2-17 — 自然语言事件对齐与官方 CoT 解析缺失

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `events.py` `parse_fixture_events` 21–68；`align_events` 70–102 |
| **Trigger** | 论文 4.1 L250–252。 |
| **Paper requirement** | 结构化任务：变量/表达式/版本/作用域。NL：抽实体后允许跳过与合并的单调序列对齐，并人工复核小集。 |
| **Repro / evidence** | 只有夹具 `alias = value` 正则。无 iGSM 官方 CoT 解析。`align_events` 按 `(entity, scope)` 分组后按 occurrence zip；次数不等则全部消失，不做单调跳过/合并。 |
| **Impact** | T2/T3 行为标签没有事件层。 |
| **Suggested fix** | 分域解析器 + NL 单调对齐；未对齐进单独计数，不默认值依赖。 |
| **Status** | **confirmed defect** |

### A2-18 — P2/P3 测量入口不完整（不要求正结果）

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `analysis.py` `p2_paired` 64–70；`p3_recovery` 73–80；`cli.py` 364–367 |
| **Trigger** | 论文 2.6 L165–166、§7 L323–325。假说不要求正结果，但要有可调用测量。 |
| **Paper requirement** | P2：配对 $\Delta\rho_S$、$\Delta\mathrm{acc}$、**污染步骤位置分布**、共享/新增分母。P3：相对 C-rand/C-layer 的恢复，并报告非目标与无效输出。 |
| **Repro / evidence** | `p2_paired` 只做四标量减法 + 一句 note。无位置。`p3_recovery` 不接收 nontarget。CLI 不调用二者。`make_noop_pair` 不提供对注入前提的允许扰动扫描（FEATURES TR-0379 自己也写了这一点，却标 implemented）。 |
| **Impact** | Week-8 无法表示“已检验但负结果”与“未跑”以外的中间态——目前只能 `not_evaluated`。 |
| **Suggested fix** | 补位置直方图与 nontarget；analyze 在有表时计算、无表时保持 `not_evaluated`。 |
| **Status** | **confirmed defect** |

### A2-19 — $\mathrm{IE}_Z$ 与来源跟随评分目标未实现

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | 全 `src/reasoning_diff` 无 `IE_Z` / `ie_z` |
| **Trigger** | 论文 2.4 L100–104；MEDIATION-01 / IE-01。 |
| **Paper requirement** | $\mathrm{IE}_Z=\mathbb{E}[g(Y_{>i})\mid do(H\leftarrow H'),C_i^b]-\mathbb{E}[g(Y_{>i})\mid C_i^b]$；$g$ 为预指定来源跟随/分支值。效应量只报相对对照差值。 |
| **Repro / evidence** | 有 `apply_swap` 与 `intervention_report` 的相对差字典，无 $g$、无期望、无预注册响应矩阵资产。 |
| **Impact** | 中介定义不可计算。 |
| **Suggested fix** | 在干预执行后对预注册 $g$ 做配对期望；绝对值不单独入库为结论。 |
| **Status** | **confirmed defect** |

### A2-20 — T1 500 题 / 四档 op / 三轨迹配置没有生成入口

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `t1_config.py` 9–21；`t1_official.py` 14–77；`cli.cmd_prepare` 只读一条 fixture |
| **Trigger** | 论文 §7 L403、§9 L437；WEEK1-01。 |
| **Paper requirement** | iGSM `op∈{5,10,15,21}`、500 题；第一周 $T_0(seed=0)$、$T'_0(seed=1)$、$T_{\mathrm{pert}}(seed=0)$。 |
| **Repro / evidence** | `validate_t1_prepare_config` 只校验数字。加载器读单个 JSON 快照。CLI 默认一条夹具、一个 seed=0 合成轨迹。无官方生成器封装（避免 `tools.tools` 是对的，但不能用“校验通过”代替生成）。 |
| **Impact** | Week-1 配置不可运行。此项的**权重/数据下载**是 pending_server；**生成/导入入口本身**是代码缺口。 |
| **Suggested fix** | 离线快照目录导入 + 配置驱动的三轨迹任务单；生成器可放服务器，但 CLI 要能消费官方快照集而非单 fixture。 |
| **Status** | **confirmed defect**（入口）；全量 500 题跑数 **pending_server** |

### A2-21 — REQUIREMENTS 源 hash 与账本登记不一致

| 项 | 内容 |
|---|---|
| **Severity** | medium |
| **File / symbol / line** | `.planning/PAPER_TRACEABILITY.md` L19 vs 当前 `.planning/REQUIREMENTS.md` |
| **Trigger** | 账本 §0：“每行 source_hash 与上表一致”。 |
| **Paper requirement** | 追溯行必须钉住所读源文件字节。 |
| **Repro / evidence** | 账本：`B0228A5785681FA11E1742EB1A7CD84822E6657D52C8CE6BF690E86A62283789`。本审查：`E481EB84664E1F71EE5551FB3451F764B8FB7D21691B89E5DFFC67773B3090C4`。论文/协议/GOAL 三份一致，唯 REQUIREMENTS 漂移（状态表被改成 implemented_local）。 |
| **Impact** | 需求行 TR-0322 段全部钉在旧 hash 上。 |
| **Suggested fix** | 重算并回写 hash；或回滚对 REQUIREMENTS 的无证据状态改写。 |
| **Status** | **confirmed defect** |

### A2-22 — Gate 0–2 保持未注册；科学结论保持空（非缺陷）

| 项 | 内容 |
|---|---|
| **Severity** | n/a |
| **File / symbol / line** | `analysis.py` `week8_decision` 83–99；`cli.py` 356–367 |
| **Trigger** | 协议 §6；GOAL §5.14；DECIDE-01。任务要求 Gate 0–2 必须保持 unregistered。 |
| **Paper requirement** | 用户未给阈值则不得编造 pass/fail。 |
| **Repro / evidence** | 无阈值 → `decision=unregistered`。`scientific_conclusion` 恒 `None`。`test_week8_never_passes_unregistered` 锁住该行为。 |
| **Impact** | 正确持守。Week-8 **分流树**（C3 升格、C4 附录）仍未编码，属 A2-18 的协议记录缺口，不在此条升格为 Gate 缺陷。 |
| **Suggested fix** | 不要添加阈值。 |
| **Status** | **non-defect suggestion**（保持） |

### A2-23 — 默认划分比例未预注册（存疑）

| 项 | 内容 |
|---|---|
| **Severity** | low |
| **File / symbol / line** | `splits.py` `DEFAULT_FRACTIONS = (0.40, 0.15, 0.10, 0.10, 0.10, 0.15)` L8 |
| **Trigger** | 协议 §3：“具体比例在生成实验数据前注册。” |
| **Paper requirement** | 六角色分离；比例预注册。 |
| **Repro / evidence** | 代码内置比例并被 CLI `prepare` 使用。协议说尚未注册。可能被解释为“实现默认值 ≠ 已注册实验”。 |
| **Impact** | 若有人用该默认切真实数据，即未注册划分。 |
| **Suggested fix** | 科学模式拒绝默认比例，要求显式 protocol_ref。 |
| **Status** | **unconfirmed doubt** |

---

## 6. 明确的非缺陷 / 持守项（避免“看起来没问题”空判）

下列经原文对照后**成立**，不计入缺陷。它们不能抵消 §5。

1. **Gate 0–2**：无阈值、无 pass/fail（A2-22）。
2. **`scientific_conclusion` 保持 `None`**；analyze 默认 `not_evaluated`。不把 fixture 写成已测科学结论。
3. **REST-01/02/03** 禁词列表存在；P3 不自动写“只是后果”；联合编辑 soundness 被 `joint_edit_counterexample` 永久禁止。
4. **身份对齐不含值**；`EventIdentity` 文档与 key 均排除 value。
5. **$R_{\mathrm{task}}$ 祖先**、**$S/M$ 空分母→null**、**缺 sham→excess null**（库函数）、**signed excess 不截断**。
6. **交换公式** $H^b+\Pi_Z(H^d-H^b)$ 手核通过。
7. **保形** $\lceil(N+1)(1-\alpha)\rceil$，越界 $+\infty$；$\alpha\ge 1$ 为 invalid。
8. **4096 vs 3584 直接迁移 N/A**，无静默 pad/truncate。
9. **官方 iGSM 快照拒裸 `G`、排除共享 RNG、mod 23**；夹具拒绝 `official`。
10. **GSM-Plus 锁定 test**。
11. **no-op 派生名** `reasoning_diff_noop`，不冒称官方 NoOp。
12. **Hotpot 元数据声明 supporting_facts 不是完整 DAG**。
13. **宿主 exec 被禁止**。
14. **C-rand 必须传入主干预范数**（库函数）。
15. **INLP 在已投影表示上迭代**（库函数）。
16. **假说不要求正结果**：本通道不因无 F1/AUC 正数判失败。

---

## 7. 测试如何把替身写成“已实现”

| 测试 | 它实际锁住的行为 | 它没有锁住的论文语义 |
|---|---|---|
| `test_full_cli_smoke` | 八阶段返回 0，`not_evaluated` | generate、隐状态、干预生成、嫁接 |
| `test_pipeline_consumes_upstream` | 下游读到 jsonl 且 probes 有 `loss` | loss 来自 $I_4$ 与错标签 |
| `test_c01_auc_*` | 启发式分数置换不变；held-out OLS 能跑 | logistic、偏相关 |
| `test_verbalizer_supervision_contract` | 未训练监督档报错；reflection 标 retrospective | 同划分微调模型 |
| `test_repair_reprefills_and_refuses_gate` | 非空字符串 ⇒ `refilled_prefix` | Prefill/decode |
| `test_b06_surface_mentions_are_text_not_parents` | 不是 parents | 名称/符号 $R^{\mathrm{surf}}$ |
| `test_hotpot_support_is_not_full_dag` | 返回 changed ids | 新 Task / 新答案 |
| `test_collect_and_intervene_tiny` | logits 因 `+0.01` 改变 | $\Pi_Z$ 交换 |

---

## 8. 结论

**HASH_MISMATCH**（55 文件计数相符，聚合 digest 不符）。审查的是当前工作树。

**原文一致性：不通过。** 库层有一批忠实公式；科学入口与账本把冒烟、子串、空壳和第一节点密度标成论文实现。Gate 0–2 未注册、假说不要求正结果——这两条被遵守。作者与绿测不能关闭本通道。

独立复审关闭条件（本通道）：A2-01–A2-09、A2-14 必须在**同一冻结 hash** 上对照原文关闭；其余 medium 项至少改为诚实的 `unimplemented` 或补上测量入口。
