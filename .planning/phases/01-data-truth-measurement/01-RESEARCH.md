# Phase 1: 数据真值与可核查测量 - Research

**Researched:** 2026-09-21
**Domain:** 离线科学实验数据真值、独立图、划分与测量合同
**Confidence:** MEDIUM（复用已有研究文档；本文件不重复做外部检索）
**Mode:** generic-agent workaround（Cursor 无 typed `gsd-planner` / `gsd-phase-researcher`）

<prior_research>
## Prior Research Already Exists — Do Not Re-litigate

本阶段**不再重新检索**官方仓库或模型接口。下列文档已在 2026-09-20 完成并锁定为实现约束源：

| 已有文档 | 本阶段用法 |
|---|---|
| `.planning/research/ARCHITECTURE.md` | 产物字段、manifest、六角色划分、观测/标签合同 |
| `.planning/research/FEATURES.md` | T1–T4 官方事实与最小接入合同 |
| `.planning/research/PITFALLS.md` | 身份/噪声/S/M/泄漏夹具 |
| `.planning/research/STACK.md` | 本机 Python/NumPy/pytest；**本阶段不引入 torch/transformers** |
| `.planning/research/SUMMARY.md` | 路线含义与待服务器项 |
| `docs/EXPERIMENT_PROTOCOL.md` | S/M、噪声、TO/CSP、划分边界 |
| `01-CONTEXT.md` | D-01..D-05 锁定决策 |

**Primary recommendation:** 从 git `8a1c6fa` 合同草稿起步，按 ARCHITECTURE.md 与 D-01..D-05 **扩展并改正**（尤其是 split 角色名、`source_kind`、图状态、sham 协议）。不要把撤回草稿当已验收实现。
</prior_research>

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01 来源分层：** 官方 iGSM 导出、项目派生、自建 fixture 必须分 `source_kind`；fixture 不得冒称官方。官方依赖图使用 `problem.template` 语义，模数 23；共享 RNG 节点 `(-1,0,0,0)` 不是全部常量的唯一前提。
- **D-02 T2/T3 真实适配：** GSM-Symbolic、GSM-Plus、HotpotQA、MuSiQue、HumanEval 均有读取、合法编辑、更新真值、独立标注导入和域内评分。缺失图真值为 `unknown`/`partial`；不得用答案、supporting facts、参考代码数据流或被测 CoT 冒充完整事件 DAG。
- **D-03 划分：** 角色 `probe_train` / `dev` / `direction_fit` / `calibration` / `transfer_pairs` / `test`。同基础题、同源题、全部变体、随机流、模型轨迹、编辑序列、donor 配对共组。GSM-Plus 与声明 test-only 来源固定评测，不参与拟合。
- **D-04 事件与测量：** 对齐靠身份/表达式/版本/作用域，不靠值相等。值变、有限扫描未变、未扫描、未对齐、结构变化、解析失败、生成失败分开。S 与 M 分开；原始量、参照、signed excess 并列；负差不截断；零分母或无 sham 协议为 null。
- **D-05 工程：** Python 包 + CLI + JSONL/NPZ；无 Web/DB/工作流框架。本机用 fixture 与离线快照验证；真实大数据/标注资产走导入+校验路径并列为 `pending_server`。

### the agent's Discretion
- 包名 `reasoning_diff`，CLI `reasoning-diff`。
- 阶段目录产物写入 `runs/`，不提交数据。
- 噪声 sham 协议：与行为扫描相同的 `(event, premise, edit_kind)` 机会集合和 ANY 聚合次数。

### Deferred Ideas (OUT OF SCOPE for this phase)
- 真实 GPU 采集、官方全量数据下载、Gate 阈值预注册、Linux 隔离执行器在服务器上的验收。
- 探针训练、干预执行、P1–P3（Phase 2+）。
</user_constraints>

<architectural_responsibility_map>
## Architectural Responsibility Map

Single-tier application — all Phase 1 capabilities reside in the Python package `reasoning_diff` (CLI → modules → JSONL/NPZ files). No browser, API server, or database tier.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Manifests / run_spec | Package IO | — | 身份与哈希，不决定科学标签 |
| T1–T4 adapters | Package `tasks` | — | 读取与合法编辑；真值不来自被测模型 |
| Independent graphs / SURF | Package `graphs` | — | 独立标注导入；缺失保持 unknown |
| Splits | Package `splits` | — | 基础题族角色，先于轨迹 |
| Events / alignment | Package `events` | — | 身份不含值 |
| Observations / S/M / TO/CSP | Package `measure` | — | 原始观测与派生量分开 |
</architectural_responsibility_map>

<research_summary>
## Summary

本阶段研究结论来自已有文档交叉核对，不是新的 web 调研。实现必须先冻结可追溯产物合同，再用本机 fixture 打通 T1 薄切片，然后按域扩展适配器。常规测试只读仓库内 fixture / 手写官方形状快照，禁止下载、禁止 GPU、禁止导入会拉 tokenizer 的官方 iGSM `tools.tools`。

**Primary recommendation:** 官方 iGSM 走预置快照 + `problem.template`；GSM-Plus 锁定 test-only；HumanEval 评分接口在本阶段只返回 `executor_unavailable`（隔离执行器后期）。
</research_summary>

<implementation_constraints>
## Implementation Constraints (honor exactly)

### 1. iGSM: `problem.template` vs `G`

官方任务依赖对象是 `id_gen.problem.template`（NetworkX DiGraph），**不是**结构图 `G`。两者不能互换。导出题干定义句 → 语义参数边，再接参数计算边。仅做 `nx.ancestors(q)` 并把参数当输入会漏掉定义句自身。共享 RNG 节点 `(-1,0,0,0)` 不是全部随机常量的唯一前提。官方算术域 `mod=23`。离线适配器延迟导入，接受预置快照；单元测试不得隐式联网。

### 2. GSM-Plus: test-only

数据卡禁止训练用途。GSM-Plus 及任何声明 test-only 的来源**固定评测**，不得进入 `probe_train` / `dev` / `direction_fit` / `calibration` / `transfer_pairs`。`solution` 不是逐步 DAG。`reversing operation` ≠ 简单换运算符；`critical thinking`（信息不足）≠ 约束矛盾。

### 3. Isolation later

HumanEval 官方 `execution.py` 的 `reliability_guard` **不是**沙箱。本阶段实现读取、Spec 编辑合同、新测试/区分输入字段，以及评分入口；默认后端返回 `executor_unavailable`。禁止宿主 `exec` / `subprocess` 跑模型或数据自带代码。Linux 隔离执行器属后续阶段 / 服务器验收。

### 4. Other Phase 1 constraints (from FEATURES / PITFALLS / PROTOCOL)

- `source_kind ∈ {official, project_derived, fixture}`；自建算术 DAG 必须是 `fixture`。
- 图状态 `complete | partial | unknown`；空图 ≠ 未知图；部分图不能把 unknown 当 false。
- 事件身份 = 实体/表达式 + occurrence_version + scope；值不参与匹配。
- Sham 机会必须与编辑扫描同 `(event, premise, edit_kind)` 集合与 ANY 次数；协议缺失时 `excess` / corrected 为 null。
- S 与 M 分开；`excess = raw - noise_reference` 保留负号；零分母 → null。
- TO：`2·LCS / (|T0|+|Tpert|)`，分 `TO_all` 与 `TO_clean`。CSP 只在已对齐干净事件上计算，并报覆盖率。
- 脏锥 `cone(ΔP)`、任务 Oracle 掩码、行为预测掩码分开存储（CONE-01 数据合同）；单点扫描反例夹具必须存在。不在本阶段实现嫁接执行。
- 表面提及 `R_surf` 与值依赖分开标注（SURF-01）。
- 撤回草稿 `8a1c6fa` 的 `SPLITS = (train, dev, direction, calibration, transfer, test)` **错误**，必须改为 D-03 六角色。
- 撤回草稿 `Node.parents` 只允许前提、不允许中间节点当父节点 — 实现时按完整 DAG 修正。
</implementation_constraints>

<standard_stack>
## Standard Stack (Phase 1 only)

| Library | Version (from STACK.md / 本机) | Purpose | Notes |
|---------|-------------------------------|---------|-------|
| Python | 3.11 | 运行时 | 本机 3.11.7 |
| NumPy | 1.26.4 | 数组、NPZ | `allow_pickle=False` |
| pytest | 9.1.1 | 本机验证 | 无 GPU、无下载 |

**Do not add in Phase 1:** torch、transformers、datasets、官方 iGSM 包、HumanEval 宿主执行路径。

**Installation:** 不新增 pip 包。`pyproject.toml` 只声明已在 STACK 核查过的 `numpy` 与 `pytest`。执行器用已安装解释器：`python -m pytest`。
</standard_stack>

<architecture_patterns>
## Architecture Patterns

```text
prepare(config, fixtures/snapshots)
  → run_spec.json + shard JSONL + manifest.json
       │
       ├─ Task (source_kind, graph_status, family/base_group)
       ├─ IndependentGraph / annotation sidecar (SURF + R_task)
       ├─ Edit (validity, new_oracle)
       ├─ Split role (six roles, test-only lock)
       ├─ Event + Alignment (identity, not value)
       └─ Observation → Label → rho_S/rho_M + TO/CSP
```

推荐目录（与 ARCHITECTURE 组件边界对齐，保持扁平，不建插件框架）：

```text
src/reasoning_diff/
  schema.py          # 共享记录字段与枚举
  artifacts.py       # run_spec / manifest / 哈希
  io.py              # JSONL / NPZ / 原子写
  cli.py             # reasoning-diff prepare
  tasks/             # t1_fixture, t1_official, t2, t3, t4
  graphs.py          # 独立图导入与覆盖
  edits.py           # 通用 Edit 记录
  splits.py          # 六角色与共组
  events.py          # 身份、对齐、审计导出
  measure.py         # 观测、S/M、噪声、TO/CSP、cone 掩码
tests/fixtures/      # 全部 source_kind=fixture，除非测试显式传入 official 语义开关
```
</architecture_patterns>

<dont_hand_roll>
## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON 原子写 / SHA-256 | 新存储层 | stdlib `hashlib` + `os.replace`（可参考 `8a1c6fa` io.py） | 已够用 |
| 图拓扑 | 自研图数据库 | 普通 dict/list DAG + 祖先闭包 | 本阶段规模小 |
| LCS / TO | 引入外部序列库 | 纯 Python LCS（草稿已有） | 避免新依赖 |
| HumanEval 执行 | 宿主 exec | `executor_unavailable` 状态 | 隔离后期 |
</dont_hand_roll>

<common_pitfalls>
## Common Pitfalls (Phase 1)

1. **用 `G` 当官方依赖图** — 必须用 `problem.template`。
2. **fixture 写成 official** — 破坏 D-01 与后续科学分层。
3. **GSM-Plus 被随机划进拟合角色** — 破坏 D-03 与数据卡。
4. **值相等当事件身份** — 破坏 D-04。
5. **缺 sham 仍输出 corrected=0** — 必须 null。
6. **把隔离执行器提前做进本阶段** — 超范围；接口拒绝即可。
7. **导入 iGSM `tools.tools`** — 会拉 GPT-2 tokenizer / 网络。
</common_pitfalls>

<open_questions>
## Open Questions (do not block Phase 1 code)

1. 真实官方全量 iGSM / 独立标注资产何时到达服务器 — 代码走导入+校验，状态 `pending_server`。
2. Gate 0–2 阈值 — 保持 null / unregistered。
3. 隔离执行器后端 — Phase 6 / 服务器，不在本阶段选择。
</open_questions>

<sources>
## Sources

- `.planning/research/ARCHITECTURE.md`, `FEATURES.md`, `PITFALLS.md`, `STACK.md`, `SUMMARY.md`（2026-09-20）
- `.planning/phases/01-data-truth-measurement/01-CONTEXT.md`（D-01..D-05）
- `docs/EXPERIMENT_PROTOCOL.md`
- git `8a1c6fa` 撤回合同草稿（起点，非已验收）
- 原文 `Reasoning-Diff-修订方案-v3 (1).md` §§2.3–2.5（SURF、cone、TO/CSP 定义）
</sources>

---

*Phase: 01-data-truth-measurement*
*Research completed: 2026-09-21*
*Ready for planning: yes*
*generic-agent workaround: yes*
