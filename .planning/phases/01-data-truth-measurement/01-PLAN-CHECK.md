---
phase: 01-data-truth-measurement
checker: gsd-plan-checker
mode: generic-agent workaround
typed_agent: unavailable
date: 2026-09-21
status: issues_found
plans_checked: 7
implementation_compared: true
---

# Phase 1 Plan Check

**角色：** `gsd-plan-checker`（generic-agent workaround；本会话无 typed `gsd-plan-checker`）。  
**对照：** `.planning/phases/01-data-truth-measurement/*PLAN.md` + `01-CONTEXT.md` ↔ `src/reasoning_diff` + `tests`。  
**生产代码：** 未修改。  
**判定口径：** 只认可核查覆盖，不认意图。`PARTIAL` 在汇总里不算通过。

## 总判

**ISSUES FOUND** — 计划文档本身大体可执行，且覆盖了 ROADMAP 的 DATA-01/02/03、MEAS-01/02；但**当前实现未兑现全部 must_have**，阶段目标还不能算达成。

| 层面 | 结果 |
|------|------|
| 计划结构 / 可执行性 | 通过（有 WARNING） |
| 计划 vs 阶段目标（若完整执行） | 可通过 |
| 当前实现 vs 各 plan `must_haves.truths` | **29 条中 12 PASS / 9 PARTIAL / 8 FAIL** |
| 阶段目标是否已被代码锁住 | **否** |

最大缺口在 **01-05（独立标注 / SURF / 共组泄漏）** 与 **01-06（对齐状态 / 审计导出）**。01-02/03/04/07 有适配器与测量骨架，但合同名、拒绝路径和夹具锁不齐。树内已有 Phase 2+ 模块（`probes/`、`interventions.py`、`repair.py`、`cli` 的 fit/intervene），这与 CONTEXT 延期项冲突；naive 重跑 01-01 会覆盖现有 CLI。

`01-VERIFICATION.md` 写 39 passed；此刻 `pytest --collect-only` 为 **42**。通过数不能替代 must_have 覆盖。

---

## 评分规则

- **PASS：** 语义已实现，且有测试或 prepare 路径锁住。
- **PARTIAL：** 有入口或字段，但缺计划写明的拒绝/分层/夹具，或 API 名漂移导致合同不可机械核对。
- **FAIL：** 计划产物或行为不存在，或实现与锁定决策相反。

---

## 1. 各 plan must_have 对照实现

### 01-01 包、产物、T1 fixture tracer

| # | must_have | 结果 | 证据 |
|---|-----------|------|------|
| T1 | D-01：夹具 `source_kind=fixture`，不得写成 official | **PASS** | `tests/fixtures/t1_tiny.json` 为 `fixture`；`load_t1_fixture` 拒绝非 fixture；`test_fixture_is_never_official` / prepare CLI 断言无 official |
| T2 | D-05：无 GPU/下载可跑 T1 prepare | **PASS** | `test_prepare_cli` 走 `reasoning-diff prepare` → JSONL + manifest |
| T3 | D-03：六角色；同 `base_group_id` 不变体分角 | **PARTIAL** | `SPLIT_ROLES` 正确；`assign_split` 只哈希 `base_group_id`。无 `assign_group_role`；无改名/no-op/donor/双模型共组测试 |
| T4 | D-04：`Observation.outcome` + 分列 S/M raw/noise/excess；无 sham 时 excess 为 JSON null | **PASS** | `Observation.outcome` 受 `OUTCOMES` 约束；`dependency_densities` 无协议时 excess `None`；tracer 与 prepare 已断言 |

**产物：** `pyproject.toml`、`cli.py`、`schema.py`、`artifacts.py`、`test_tracer_t1_prepare.py`、`t1_tiny.json` 均在。  
**关键链路：** `prepare → Task/Edit/Split/Event/Observation → runs/ JSONL + manifest` **PASS**。  
**可执行性：** 结构可执行，且已有 `01-01-SUMMARY.md`。对当前树 **不宜整计划重跑**：`cli.py` 已含 collect/fit/calibrate/intervene/repair/analyze。

### 01-02 T1 官方形状与 op/500 配置

| # | must_have | 结果 | 证据 |
|---|-----------|------|------|
| T1 | D-01：依赖来自 template，不是名为 G 的结构图 | **PARTIAL** | `load_igsm_snapshot` 读 `template`，元数据 `ignored_structure_graph`。夹具 `G.edges=[]`，**没有**计划要求的“RNG 连到全部常量”误导图，也无 template vs G 祖先差集断言 |
| T2 | D-01：`modulus=23`；`(-1,0,0,0)` 不是全部常量唯一前提 | **PARTIAL** | `SHARED_RNG` 被跳过；`answer_spec.mod==23`。无 `22+2 → 1` 环绕测试；编辑走通用 `apply_value_edit`，不是 `apply_igsm_literal_edit` |
| T3 | DATA-01：`validate_t1_prepare_config` 接受 op∈{5,10,15,21} 且 n=500 | **PARTIAL** | `ALLOWED_OPS` / `DEFAULT_N_PROBLEMS=500` 会拒非法 op 与非 500。不校验必填 `source_kind`；缺 `generator_revision` 时不标 `pending_server`；无 `tests/test_t1_config.py` |
| T4 | 官方形状 `source_kind=official`；同目录夹具仍为 fixture | **PASS** | 官方加载器写出 official；T1 fixture 走独立加载器且拒绝升格。但 `source_kind` 默认 `"official"`，缺参不抛错；`source_kind="fixture"` 反而 `ValueError`（与计划行为相反） |

**产物缺口：** `tests/test_t1_config.py` 不存在（逻辑挤在 `test_t1_official.py::test_config_ops`）。  
**可执行性：** 文档可执行。对当前树只应 **补洞**，不要按计划函数名重写加载器。

### 01-03 T2 GSM-Symbolic / GSM-Plus

| # | must_have | 结果 | 证据 |
|---|-----------|------|------|
| T1 | D-02：两源均有读取、合法编辑、更新 `answer_spec`、公式侧车、域内评分 | **PARTIAL** | Symbolic：`load_gsm_symbolic` + 侧车 dict + `apply_formula_edit` + `score_numeric`。Plus：**只有读取**，无合法编辑/侧车/更新真值。无 `load_formula_sidecar` / `apply_gsm_numeric_edit` / `score_gsm_answer` 合同名。两侧车硬编码 `source_kind=official`，调用方不能传入 |
| T2 | D-02：无逐步图则为 `unknown`/`partial`，不用 solution 填满 DAG | **PASS** | 无侧车 → `unknown`；有侧车 → `partial`；Plus `graph_status=unknown` 且 `solution_is_not_dag` |
| T3 | D-03：Plus `fit_eligible=false`、默认 test，**不能被 `assign_split` 划进拟合角色** | **FAIL** | 元数据与 `refuse_fit_split` / `lock_test_only` 有。`assign_split(base_group_id)` **不读** `fit_eligible`，缺 `test_only=True` 时仍可落到 `probe_train` 等。计划写明的是 `assign_split` 合同 |
| T4 | DATA-02：`reversing operation` 与 critical-thinking / `insufficient_information` 分状态 | **FAIL** | 代码有分支（reversing → `query_reversed`，不是计划的 `query_target_change`）。夹具 `t2_gsmplus_one.json` 的 `perturbation_type` 是 `numerical substitution`，**无 reversing / critical 测试** |

**其它缺口：** 无 `seed_text_hash` / `match_status`；无 `####` 抽取测试；canary 进 metadata（question 未写入，可接受）。  
**可执行性：** 文档可执行。当前树需补 Plus 编辑锁、`assign_split` 强制 test、扰动分型夹具。

### 01-04 T3 / T4

| # | must_have | 结果 | 证据 |
|---|-----------|------|------|
| T1 | D-02：Hotpot `supporting_facts` 不自动变成全部祖先；未覆盖边 unknown | **PASS** | `graph_status` 无侧车时 `unknown`；`supporting_facts_are_not_complete_dag` / `unknown_non_support`；`document_edit` 记录多 `changed_premise_ids` |
| T2 | D-02：MuSiQue `composition_reference`；同 id 的 answerable/unanswerable 不去重丢失 | **PASS** | `graph_kind=composition_reference`；`task_id` 带 variant；`test_musique_keeps_unanswerable_pair`。缺“替换 supporting 段后更新子答案/`answer_spec`” |
| T3 | D-02：HumanEval 默认 `executor_unavailable`，宿主不 exec | **PASS** | `UnavailableExecutor` / `SpyExecutor`；`score_code` 默认不可用。无计划中的 spec-edit pack（old/new clause、new_tests、`distinguishing_inputs`）；测试未 spy `builtins.exec` |
| T4 | T4 四类：`insufficient_information` / `inconsistent_constraints` / `no_solution` / `strategy_change` | **PARTIAL** | `t4_boundary.json` + `load_t4` 锁四枚举。无“`parse_failed` 不映射到四类”测试 |

**产物：** 四个适配器与 `scoring.py` / `executor.py` 在。`NullExecutor` 名为 `UnavailableExecutor`。`score_qa` 只有 EM，不是 `score_qa_em_f1`。  
**可执行性：** 文档可执行。对当前树补 spec-edit 合同与 parse_failed 分离即可。

### 01-05 独立图、SURF-01、六角色共组

| # | must_have | 结果 | 证据 |
|---|-----------|------|------|
| T1 | D-02：独立标注导入后 graph 可为 complete/partial/unknown；unknown 节点不当 task negative | **FAIL** | **无** `annotations.py`、`import_annotation_jsonl`、`IndependentGraph`、`tests/test_graphs_annotations.py`、`annotation_sidecar.jsonl`。无 `model_cot` 拒绝 |
| T2 | SURF-01：每步 `R_surf` 与值依赖 / `R_task` 分字段 | **FAIL** | `Event.surface_mentions` 存在，但 `parse_fixture_events` 填的是 `node.parents`（与值依赖同源）。无“提到 p1 但不依赖 p1”用例 |
| T3 | D-03：同 `base_group_id` 的数值/改名/no-op/编辑序列/donor/双模型轨迹同一角色 | **FAIL** | 只有 `assign_family(list[str])`。无 `assign_group_role`（members 含 rng/model/edit_seq/donor/`fit_eligible`）。无 `tests/test_splits.py` |
| T4 | D-03：`fit_eligible=false` 强制 test，与拟合组无交集 | **PARTIAL** | `assert_disjoint` 存在但无泄漏测试。Plus 锁未接入 `assign_split`（见 01-03 T3） |

**可执行性：** **仍应执行（或按缺口改写后执行）**。这是阶段目标第 2–3 条的主缺口。

### 01-06 事件身份、对齐、审计

| # | must_have | 结果 | 证据 |
|---|-----------|------|------|
| T1 | D-04：两作用域同值 x=3 不对齐；交换两事件数值不改变匹配 | **FAIL** | 无 `tests/test_events.py`、无 `tests/fixtures/traces/dup_scope.json`。解析把同 scope 别名绑到节点；无双 scope 夹具 |
| T2 | D-04：`q=p1+p2` 中 p1 改值仍对齐；不同节点同值不能对齐 | **PARTIAL** | tracer `test_identity_alignment_ignores_values` 覆盖同身份改值。无“不同节点同值不对齐” |
| T3 | MEAS-01：alignment 显式 `matched/missing/merged/split/version_changed/ambiguous` | **FAIL** | `ALIGNMENT_STATUSES` 有这些词。`align_events` 只返回 `pairs/removed/added` 与空的 `merged`。重复身份 **raise**（允许），但歧义行被 **跳过** 而非 `parse_failed`/`ambiguous` |
| T4 | 删除/合并/解析失败只增加对应状态计数，不增加行为正负例 | **FAIL** | 无 merge/split 检测；歧义行静默丢弃；无审计导出，无法人工回填 |

**产物缺口：** `export_audit_jsonl` / `import_audit_jsonl` 不存在。  
**可执行性：** **仍应执行。** 这是 MEAS-01 / 成功标准 4 的主缺口。

### 01-07 观测、S/M/噪声、TO/CSP、CONE-01

| # | must_have | 结果 | 证据 |
|---|-----------|------|------|
| T1 | D-04：S/M 分开；raw / noise_reference / signed excess；负 excess 不截断 | **PASS** | `dependency_densities` 分键；`test_signed_excess_not_clipped`（-0.5） |
| T2 | D-04：零分母或未声明 sham 时 excess/corrected 为 JSON null | **PASS** | 空分母 → `None`；无协议 → `null_reason=sham_protocol_missing` |
| T3 | MEAS-02：sham 与扫描同 `(event, premise, edit_kind)` 集合与相同 ANY 次数 | **FAIL** | `build_labels` 仅当 sham 条数 == `opportunities` 才写 noise。无协议名 `sham_matched_opportunities`；无“行为 ANY-over-10 对单次 sham”失败测试；`Observation` **无** `protocol_ref`（在 `Label` 上） |
| T4 | `TO_all` 与 `TO_clean` 分开；CSP 只在已对齐干净事件上并带覆盖率 | **PARTIAL** | `preservation_to_csp` 有 `to_all` / `to_clean` / `csp` / `clean_alignment_coverage`。`test_measure.py` **不测** TO 分键；干净事件用 `task_parents ∩ edited`，符合“独立 R_task”方向 |
| T5 | CONE-01：cone / oracle_mask / behavior_mask 分字段；xy=0 单点反例阻止联合 soundness | **PARTIAL** | `cone_bundle` + `joint_edit_counterexample` 有测试。无 `tests/fixtures/measure/xy_zero.json` / `sm_example.json`；函数名不是 `claim_joint_soundness_from_singletons` |

**可执行性：** 文档可执行。对当前树补 sham 次数锁、观测序列化三态、夹具文件，不要重写已通过的 S/M 符号差。

---

## 2. 覆盖缺口（相对阶段目标 / CONTEXT / 需求）

### 实现相对 must_have / 成功标准

| 缺口 | 对应 | 严重度 |
|------|------|--------|
| 独立标注 JSONL 导入；拒绝 `model_cot`；unknown ≠ task 0 | D-02，DATA-02，成功标准 2，01-05 | BLOCKER |
| SURF 与 `R_task` 独立字段 + 分叉用例 | SURF-01，01-05 | BLOCKER |
| 六角色共组（变体/rng/model/edit_seq/donor）+ 拟合/测试泄漏测试 | D-03，DATA-03，成功标准 3，01-05 | BLOCKER |
| `assign_split` 对 `fit_eligible=false` / GSM-Plus **强制 test** | D-03，01-03 | BLOCKER |
| 对齐状态机 + 双 scope / 换值夹具 + 歧义不丢弃 | D-04，MEAS-01，成功标准 4，01-06 | BLOCKER |
| 审计 JSONL 导出/回填（不原地覆盖） | MEAS-01，01-06 | BLOCKER |
| sham 同机会集合与 ANY 次数；观测三态序列化 | D-04，MEAS-02，成功标准 5，01-07 | BLOCKER |
| GSM-Plus 合法编辑 + reversing / critical-thinking 分状态测试 | D-02，DATA-02，01-03 | WARNING（读取已有，合同不完整） |
| 官方 template vs 误导 G、mod 环绕、`source_kind` 必填、`pending_server` | D-01，D-05，01-02 | WARNING |
| HumanEval spec-edit pack；T4 `parse_failed` 分离测试 | 01-04 任务行为 | WARNING |
| DATA-01 改名 / 来源—数值变体（T1）；MuSiQue 段替换更新真值 | DATA-01 全文；01-04 行为 | WARNING |
| `PAPER_TRACEABILITY.md` 仍写“尚无生产模块”、行状态 `unimplemented` | 01-01 任务 3 | WARNING |
| CONTEXT / RESEARCH 写“交付树无生产 `.py`” | 计划上下文过期 | INFO |

### 计划相对 ROADMAP 需求（文档层）

| 需求 | 声明于 | 任务是否覆盖 |
|------|--------|----------------|
| DATA-01 | 01-01, 01-02 | 官方形状 + 配置 + 数值编辑。改名/来源—数值变体只在 01-05 当共组成员，无构造任务 |
| DATA-02 | 01-03, 01-04, 01-05 | 有。独立标注全在 01-05 |
| DATA-03 | 01-01, 01-03, 01-05 | 有 |
| MEAS-01 | 01-01, 01-06 | 有 |
| MEAS-02 | 01-01, 01-07 | 有 |
| SURF-01 | 01-05 | 有 |
| CONE-01 | 01-07 | 有 |

ROADMAP 五条 Success Criteria 在计划中都有对应任务；**缺口在实现，不在漏写计划。**

### 延期项 vs 当前树

CONTEXT / RESEARCH 明确延期：GPU 采集、全量下载、探针训练、干预、P1–P3。  
**计划未纳入这些项（合规）。**  
**实现已包含：** `probes/`、`interventions.py`、`repair.py`、`analysis.py`、`transfer.py`、`models/`、`test_science.py`、`test_tiny_hooks.py`、`test_cli_pipeline.py`。这不是计划缺陷，但是执行器若按 01-01 重写 `cli.py` 会误删或冲突。

---

## 3. 计划是否可执行

**结论：七份计划作为 GSD 执行稿可跑；对当前仓库不能当“空树从头执行”。**

| Plan | wave | depends_on | 任务完整 | 对空树 | 对当前树 |
|------|------|------------|----------|--------|----------|
| 01-01 | 1 | [] | Files/Action/Verify/Done 齐 | 可执行 | **不要整单重跑**（CLI 已膨胀） |
| 01-02 | 2 | 01-01 | 齐 | 可执行 | 补洞；勿按旧函数名重写 |
| 01-03 | 2 | 01-01 | 齐 | 可执行 | 补洞（Plus 锁/编辑/分型） |
| 01-04 | 2 | 01-01 | 齐 | 可执行 | 补洞（spec-edit / parse_failed） |
| 01-05 | 3 | 01-01..04 | 齐 | 可执行 | **需要执行** |
| 01-06 | 3 | 01-01 | 齐 | 可执行 | **需要执行** |
| 01-07 | 4 | 01-01, 01-06 | 齐 | 可执行 | 补洞（sham / 夹具 / 观测字段） |

依赖图无环。01-02/03/04 无文件重叠，可并行。  
01-06 `wave: 3` 但只依赖 01-01（按公式应为 wave 2）。与 ROADMAP“Wave 3 放 05+06”一致，不是环；属声明不一致。

**当前树上，下列计划内 `<verify>` 会直接失败（文件或 `-k` 零匹配）：**

- 01-02：`tests/test_t1_config.py` 不存在；`-k "edit or recompute or cancel"` 匹配 0
- 01-05：`tests/test_graphs_annotations.py`、`tests/test_splits.py` 不存在
- 01-06：`tests/test_events.py` 不存在
- 01-07：`-k "obs or sham or unscanned or protocol"` 匹配 0；`tests/fixtures/measure/*.json` 不存在

这些命令是“任务完成后”的验收，不是计划语法错误。执行前应先改 CONTEXT（删除“无生产 `.py`”），并改成 **gap-closure**，避免按空树假设覆盖已有模块。

---

## 4. GSD 维度

| 维度 | 结果 | 说明 |
|------|------|------|
| 1 Requirement coverage | PASS（计划） / FAIL（实现） | 计划 frontmatter 认领了全部阶段需求 ID |
| 2 Task completeness | PASS | 无 checkpoint；auto/tdd/tracer 均有 files/action/verify/done |
| 3 Dependency correctness | PASS + INFO | 无环、无悬空依赖。01-06 wave 与 depends_on 不一致 |
| 3b Undeclared coupling | PASS | 同波次 02/03/04 无共享可变资源；05 改 schema、06 改 events |
| 4 Key links planned | PASS（计划） | 实现上 05/06 链路未接通 |
| 5 Scope sanity | WARNING | 01-01：3 任务但 `files_modified` 16（≥15）。各 plan 3 任务。estimate 55k–90k、confidence=low |
| 6 must_haves derivation | PASS | truths 可观察，对齐 D-xx |
| 7 Context compliance | PASS（计划） / FAIL（实现） | 计划落实 D-01..D-05，未做延期项。实现缺 D-02 标注、D-03 split 锁、D-04 对齐/sham；并提前做了延期的探针/干预 |
| 7b Scope reduction | PASS | “不生成 500 题 / 隔离后期 / 不嫁接”符合 D-05 与延期，不是静默缩水 |
| 7c Architectural tier | PASS | 能力都在 `reasoning_diff` 包内 |
| 8 Nyquist / failing direction | PASS | 均有 `<automated>` + `<fails_when>` |
| 9 Cross-plan data contracts | PASS | 无互相清洗同一流 |
| 10 AGENTS.md | PASS | pytest、最小改动、无 Web/DB；计划未引入 torch |
| 11 Research resolution | WARNING | `## Open Questions` 无 `(RESOLVED)`。三条是服务器时机，CONTEXT 已定为 `pending_server`，不阻塞代码 |
| 12 Pattern compliance | SKIPPED | 无 `PATTERNS.md` |
| Verify path sanity | WARNING | 见上节：若干 verify 路径在当前树不存在 |
| Numeric authority | INFO | `01-VERIFICATION.md` 的 39 与当前 42 collected 不一致 |

Dimension 7c: RESEARCH 有 Architectural Responsibility Map，未 SKIP。

---

## 5. Structured Issues

```yaml
issues:
  - plan: "01-05"
    dimension: requirement_coverage
    severity: blocker
    required_property: "独立标注可导入；unknown 节点不得写成 task negative；禁止 model_cot 真值"
    description: "无 annotations.py / import_annotation_jsonl / IndependentGraph / test_graphs_annotations.py / annotation_sidecar.jsonl"
    fix_hint: "按 01-05 任务 1 补导入与覆盖测试，或把缺口写进新的 gap plan"

  - plan: "01-05"
    dimension: requirement_coverage
    severity: blocker
    required_property: "SURF-01：R_surf 与 R_task 分字段且集合可不同"
    description: "Event.surface_mentions 被填成 node.parents，与值依赖重合；无分叉测试"
    fix_hint: "导入或解析时独立写 surface_mention_premise_ids"

  - plan: "01-05"
    dimension: requirement_coverage
    severity: blocker
    required_property: "同 base_group 的全部变体/轨迹/donor 同一角色，且拟合与测试无交集"
    description: "无 assign_group_role 与 tests/test_splits.py；assert_disjoint 未接泄漏夹具"
    fix_hint: "先分组再切角色，并加 probe_train∩test 失败用例"

  - plan: "01-03"
    dimension: context_compliance
    severity: blocker
    required_property: "fit_eligible=false 时 assign_split 只能返回 test"
    description: "assign_split 只认 test_only 旗标，不读 Task.fit_eligible；GSM-Plus 家族 id 可被哈希进拟合角色"
    fix_hint: "assign_split 接收记录/组元数据，或在分配前强制 lock_test_only"

  - plan: "01-06"
    dimension: requirement_coverage
    severity: blocker
    required_property: "对齐状态含 missing/merged/split/version_changed/ambiguous；身份不含值；可导出人工核查"
    description: "align_events 仍是 removed/added；无 dup_scope 夹具；歧义行 continue 丢弃；无 export/import_audit_jsonl"
    fix_hint: "按 01-06 三任务补齐状态机与审计，不原地覆盖 events.jsonl"

  - plan: "01-07"
    dimension: requirement_coverage
    severity: blocker
    required_property: "sham 与行为扫描同 (event, premise, edit_kind) 与相同 ANY 次数"
    description: "无 sham_matched_opportunities 合同测试；无 10 vs 1 次数失败用例；Observation 无 protocol_ref"
    fix_hint: "把协议挂到 Observation，并锁次数相等"

  - plan: "01-03"
    dimension: requirement_coverage
    severity: warning
    required_property: "GSM-Plus 具备合法编辑/更新真值，且 reversing 与 insufficient_information 分状态可测"
    description: "Plus 无编辑入口；夹具 perturbation 为 numerical substitution；状态串为 query_reversed 而非 query_target_change"
    fix_hint: "补 Plus 编辑或明确仅 Symbolic 可编辑，并加两条扰动夹具"

  - plan: "01-02"
    dimension: context_compliance
    severity: warning
    required_property: "官方依赖来自 template 且可证明忽略误导 G；source_kind 必填；缺官方 revision 为 pending_server"
    description: "G 夹具无误导边；source_kind 默认 official；配置不写 pending_server；无 22+2≡1"
    fix_hint: "按 01-02 行为补快照与校验，不改已通过的 fixture/official 分层"

  - plan: "01-04"
    dimension: task_completeness
    severity: warning
    required_property: "HumanEval spec-edit 合同字段齐全；parse_failed 不落入 T4 四类"
    description: "load_humaneval 无 spec-edit pack；test_t3_t4 无 parse_failed 用例；未 spy builtins.exec"
    fix_hint: "加字段与一条 parse_failed 夹具"

  - plan: "01-01"
    dimension: scope_sanity
    severity: warning
    required_property: "单计划文件数保持在可执行预算内"
    description: "01-01 files_modified=16，超过 15 的 blocker 阈值；作为 tracer 可理解"
    metrics: {tasks: 3, files: 16}

  - plan: null
    dimension: research_resolution
    severity: warning
    required_property: "RESEARCH.md Open Questions 均有 RESOLVED 标记"
    description: "01-RESEARCH.md 为 '## Open Questions (do not block Phase 1 code)'，三条无 RESOLVED。内容已被 D-05 定为 pending_server"
    file: "01-RESEARCH.md"

  - plan: "01-06"
    dimension: dependency_correctness
    severity: info
    required_property: "wave 与 depends_on 一致"
    description: "01-06 wave=3 但 depends_on 仅 01-01（计算波次为 2）"

  - plan: null
    dimension: context_compliance
    severity: info
    required_property: "CONTEXT 对代码树的描述与仓库一致"
    description: "01-CONTEXT.md 写无生产 .py；src/reasoning_diff 已有 30+ 模块，且含 CONTEXT 延期的探针/干预"

  - plan: "01-05"
    dimension: dependency_correctness
    severity: info
    required_property: "Ordering between same-wave plans is declared, not implied"
    description: "01-05 与 01-06 同为 wave 3、互不 depends_on。05 写 schema.Event 字段，06 读 EventIdentity。当前无共享可变键；若并行执行需避免同时改 schema.py"
    plans: ["01-05", "01-06"]
```

---

## 6. 建议

1. **不要**把 01-01..01-04 当空树重执行。  
2. **要**按缺口执行 01-05、01-06，并对 01-02/03/04/07 做 gap-closure（保留现有函数名或加别名，避免双合同）。  
3. 执行前更新 `01-CONTEXT.md` 的 Existing Code Insights，以及 `PAPER_TRACEABILITY.md` 的“无生产模块”句。  
4. `assign_split` 与标注导入未修好之前，不要把 Phase 1 标 Complete，也不要用 `01-VERIFICATION.md` 的 pytest 绿作为科学/合同验收。  
5. Phase 2+ 文件保留即可，但不要算进本阶段 must_have。

**修订需求：** 有 blocker + warning，计划不必整阶段重写；实现必须补洞。若走 `$gsd-plan-phase --gaps`，应用本文件而不是再生成一套平行计划。

---

*Phase: 01-data-truth-measurement*  
*Checker: gsd-plan-checker (generic-agent workaround)*  
*Typed dispatch: unavailable*  
*Production code unmodified*
