# Phase 1: 数据真值与可核查测量 - Context

**Gathered:** 2026-09-21
**Status:** Ready for planning
**Mode:** Autonomous smart discuss; grey areas resolved from user-confirmed decisions in PROJECT.md / EXPERIMENT_PROTOCOL.md / CURSOR_GOAL_PROMPT.md

<domain>
## Phase Boundary

交付可追溯的数据真值、事件身份、合法编辑、共组划分和噪声参照。研究者能追溯每个输入前提、独立任务标签、编辑机会和事件响应，并识别未知/结构变化。不含模型采集、探针训练或干预执行（Phase 2+）。

</domain>

<decisions>
## Implementation Decisions

- **D-01:** 官方 / 派生 / fixture 分 `source_kind`；官方依赖用 `problem.template`、模数 23；RNG 节点 `(-1,0,0,0)` 不是全部常量的唯一前提。
- **D-02:** T2/T3 真实读取、合法编辑、更新真值、独立标注导入与域内评分；缺图为 `unknown`/`partial`，不得用答案、supporting facts、参考数据流或被测 CoT 冒充完整事件 DAG。
- **D-03:** 六角色 `probe_train` / `dev` / `direction_fit` / `calibration` / `transfer_pairs` / `test`；同基础题及变体共组；GSM-Plus 与 test-only 来源固定评测。
- **D-04:** 事件对齐靠身份/表达式/版本/作用域；值变、未变、未扫描、未对齐、结构变化、解析/生成失败分开；S 与 M 分开；raw / 参照 / signed excess 并列；负差不截断；零分母或无 sham 协议为 null。
- **D-05:** Python 包 + CLI + JSONL/NPZ；本机 fixture/离线快照验证；真实大数据与标注为导入+校验并标 `pending_server`。

### D-01 来源分层
- 官方 iGSM 导出、项目派生、自建 fixture 必须分 `source_kind`；fixture 不得冒称官方。
- 官方依赖图使用 `problem.template` 语义，模数 23；共享 RNG 节点 `(-1,0,0,0)` 不是全部常量的唯一前提。

### D-02 T2/T3 真实适配
- GSM-Symbolic、GSM-Plus、HotpotQA、MuSiQue、HumanEval 均有读取、合法编辑、更新真值、独立标注导入和域内评分。
- 缺失图真值为 `unknown`/`partial`；不得用答案、supporting facts、参考代码数据流或被测 CoT 冒充完整事件 DAG。

### D-03 划分
- 角色：`probe_train` / `dev` / `direction_fit` / `calibration` / `transfer_pairs` / `test`。
- 同基础题、同源题、全部变体、随机流、模型轨迹、编辑序列、donor 配对共组。
- GSM-Plus 与声明 test-only 来源固定评测，不参与拟合。

### D-04 事件与测量
- 对齐靠身份/表达式/版本/作用域，不靠值相等。
- 值变、有限扫描未变、未扫描、未对齐、结构变化、解析失败、生成失败分开。
- S 与 M 分开；原始量、参照、signed excess 并列；负差不截断；零分母或无 sham 协议为 null。

### D-05 工程
- Python 包 + CLI + JSONL/NPZ；无 Web/DB/工作流框架。
- 本机用 fixture 与离线快照验证；真实大数据/标注资产走导入+校验路径并列为 pending_server。

### the agent's Discretion
- 包名 `reasoning_diff`，CLI `reasoning-diff`。
- 阶段目录产物写入 `runs/`，不提交数据。
- 噪声 sham 协议：与行为扫描相同的 `(event, premise, edit_kind)` 机会集合和 ANY 聚合次数。

</decisions>

<code_context>
## Existing Code Insights

当前交付树无生产 `.py`。Git `8a1c6fa` 曾有合同草稿（schema/events/measurement/splits/io）后被撤回，可作起点但必须按原文与 ARCHITECTURE.md 扩展，不能当作已验收实现。

</code_context>

<specifics>
## Specific Ideas

- 四档 op ∈ {5,10,15,21} 与 500 题配置可检查。
- T4 区分 `insufficient_information` / `inconsistent_constraints` / `no_solution` / `strategy_change`。
- 追踪账本：`.planning/PAPER_TRACEABILITY.md`。

</specifics>

<deferred>
## Deferred Ideas

- 真实 GPU 采集、官方全量数据下载、Gate 阈值预注册、Linux 隔离执行器在服务器上的验收。
- 探针、干预、P1–P3 执行属后续阶段，但本阶段须留下它们消费的身份/标签合同。

</deferred>
