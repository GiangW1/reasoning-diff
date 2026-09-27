# Roadmap: Reasoning Diff

## Overview

2026-09-21 已获授权实施。用户已确认完整研究范围覆盖 T1–T4，本机不运行真实 GPU 实验。六阶段从 Pending 进入 GSD autonomous 推进。

阶段进展衡量代码与协议的可验收性，科学主张是否成立另行记录。真实数据、GPU、人工标注或预注册未就绪时，可以推进不依赖这些输入的代码工作，但不能伪造相应验收结果。

## Phases

- [x] **Phase 1: 数据真值与可核查测量** — 本机代码与回归已落地；官方全量数据 pending_server。
- [x] **Phase 2: 冻结模型采集与边界接口** — 微型模型接口已验证；真实权重 pending_server。
- [x] **Phase 3: 探针、公平基线与跨模型迁移** — 公式与 CLI 已接通；真实拟合 pending_server。
- [x] **Phase 4: 前瞻干预与成套对照** — 几何/对照代码已落地；真实 donor pending_server。
- [x] **Phase 5: C3 检验与附录重算** — 工具已实现；科学结论 not_evaluated。
- [ ] **Phase 6: 全链路验收与服务器交接** — CLI/文档已齐；两轮独立 A–F 尚未连续通过。

## Phase Details

### Phase 1: 数据真值与可核查测量
**Goal:** 研究者能追溯每个输入前提、独立任务标签、编辑机会和事件响应，并识别未知/结构变化。
**Depends on:** 无。
**Requirements:** DATA-01, DATA-02, DATA-03, MEAS-01, MEAS-02
**Success Criteria:**
1. T1 官方导出保留模数和正确依赖图；自建夹具、派生数据与官方来源分开；四档 op 与 500 题配置可检查。
2. T2/T3 有真实读取、独立标注导入、合法扰动/答案更新和域内评分契约；T4 明确缺信息、矛盾、无解与策略变化；缺真值不会变成假负例。
3. 同基础题、同源题、donor 与全部变体不跨拟合/测试角色，测试专用数据不会被分到拟合集。
4. 事件身份不使用输出数值；重复、作用域、未对齐、消失/合并、解析失败均可导出人工核查。
5. 观测到标签有完整谱系，S/M 分开，原始量/参照/有符号差值与分母并存；噪声协议未定时 corrected 为 null。
**Plans:** 7 plans

Plans:
- [ ] 01-01-PLAN.md — 包、产物清单与 T1 夹具端到端 tracer
- [ ] 01-02-PLAN.md — T1 官方形状适配、template 图、op/500 配置
- [ ] 01-03-PLAN.md — T2 GSM-Symbolic / GSM-Plus 与 test-only 锁
- [ ] 01-04-PLAN.md — T3 Hotpot/MuSiQue/HumanEval 与 T4 边界类型
- [ ] 01-05-PLAN.md — 独立图、SURF-01、六角色共组划分
- [ ] 01-06-PLAN.md — 事件身份、对齐状态、审计导出
- [ ] 01-07-PLAN.md — 观测、S/M/噪声、TO/CSP、CONE-01

Wave 1 *(no blocker)*: 01-01
Wave 2 *(blocked on Wave 1 completion)*: 01-02, 01-03, 01-04
Wave 3 *(blocked on Wave 1; 01-05 also waits on Wave 2 adapters)*: 01-05, 01-06
Wave 4 *(blocked on Wave 1 and 01-06)*: 01-07

### Phase 2: 冻结模型采集与边界接口
**Goal:** 在声明的模型/随机流下收集可重放轨迹和真正位于目标生成之前的特征。
**Depends on:** Phase 1 的产物与身份合同。
**Requirements:** MODEL-01
**Success Criteria:**
1. Qwen3-8B 与 R1-Distill-Qwen-7B 使用各自固定 revision 的模板/分词器；保存原生成 IDs、prompt、停止原因和截断/失败。
2. 步前、数值前与步尾分别采集；跨界 token 不泄漏目标，无法精确定位时有明确状态，离线/在线边界来源可区分。
3. 微型随机模型可核对完整前向与缓存步进、hook 所影响的层/位置、跨条件缓存隔离及独立随机流。
4. 首次采集、额外 Prefill、Decode、探针与端到端耗时分别计量；真实模型/设备的验证保持独立状态。
**Plans:** 尚未制定。服务器真实模型测试不会由 CPU 通过状态替代。

### Phase 3: 探针、公平基线与跨模型迁移
**Goal:** 使用公平监督与留出评估判断隐状态的额外信息、覆盖性及迁移范围。
**Depends on:** Phase 2；Phase 1 的完整划分及标签。
**Requirements:** PROBE-01, BASE-01, XFER-01
**Success Criteria:**
1. 任务/行为低秩双线性头和边界 MLP 使用未知标签掩码；拟合、层/秩选择、方向数据与最终测试可追溯且无交集。
2. 文本、注意力/rollout 和四档 verbalizer 共用标签/划分；同可见前缀对照，反思或步尾读数不混入前瞻比较。
3. 校准按完整轨迹/序列或声明的问题块取最大分数，使用有限样本顺序统计量；无标签、空真集与无穷阈值分别处理。
4. 维度兼容时才执行直接迁移；首批 4096→3584 直接模式明确不适用；无标签配对与监督适配分别报告，步骤/前提两类向量均正确转换。
5. 图组合/改名/数值留出、正确/错误轨迹分层和所有适用范围可报告，不据测试结果重新选方法。
**Plans:** 尚未制定。

### Phase 4: 前瞻干预与成套对照
**Goal:** 对预先指定的来源响应执行可核查干预，并比较两类控制与非目标损伤。
**Depends on:** Phase 3 的冻结特征/方向协议。
**Requirements:** CAUSAL-01, CAUSAL-02
**Success Criteria:**
1. donor/base 的来源—数值解耦与高层目标/非目标响应在运行前固定；等值与非等值条件分开，每个数值条件重新提取 donor。
2. 交换、INLP/选择性消融、救援发生在目标首 token 前；hook 层内位置和 KV 影响范围完整记录。
3. C-rand/C-layer 属于同一预定 cohort，匹配实际范数/维数/位置/随机流；C-layer 由开发集确定，退化和失败不丢弃。
4. 结果包含目标来源跟随、非目标响应、任务正确和无效输出；相对两控制的配对差为主，错误来源/随机救援与恒等恢复区分。
**Plans:** 尚未制定。50 条冒烟样本来自原方案建议，不能替代正式样本量与功效设计。

### Phase 5: C3 检验与附录重算
**Goal:** 在固定协议下产生可复查的 P1–P3 估计与附录重算结果，允许真实阴性结论。
**Depends on:** Phase 4；P1/P2 可在数据与探针到位后先实施，但 P3 不得缺对照。
**Requirements:** C3-01, REPAIR-01
**Success Criteria:**
1. P1 在留出基础题上报告相对链长+op 的预测增量、问题级区间和明确正类；不使用训练内 AUC 当结论。
2. P2 保留完整配对、注入位置/相关度、公共前提与新增前提统计及覆盖率，避免分母变化伪装效应。
3. P3 比较选择性消融相对基线和两控制的恢复，失败/无效输出在分母中，未检出效应不被写为反向因果。
4. Oracle/行为参考/探针/文本/随机/截断/提示/检索/全重推使用一致执行与成本口径；保留文本在新前缀重新 Prefill，无门控或验证器回退。
5. 单次/连续编辑预算、逐步合法性、最终正确率、失败类别及成本完整报告；C4、相图与相关辅助分析统一为附录资产。
**Plans:** 尚未制定。条件扩展实验的判据需预注册，不能把缺数据自动判为失败。

### Phase 6: 全链路验收与服务器交接
**Goal:** 同事能用有文档的命令复现完整流程，并清楚区分代码已验证和科学未验证。
**Depends on:** Phases 1–5。
**Requirements:** OPS-01, QA-01, DECIDE-01
**Success Criteria:**
1. CLI 贯通准备、采集、标注、拟合、校准、迁移、干预、重算与报告；清单、哈希、分片、恢复和失败计数可审计。
2. 本机离线夹具与随机微型模型覆盖关键边界；全模块审查有证据，未通过/无法运行项保留原因，真实数据与 GPU 测试单列。
3. 代码任务仅经明确隔离执行器；环境缺失时不回退宿主，不伪造执行通过；服务器说明记录设备、精度、软件、模型和数据版本。
4. Gate 0–2 未注册时输出数值或缺失原因，永不自动 pass/fail；Week-8 保留未运行、无效、不足、未注册及已按标准评估的状态。
5. 报告与叙事支持 C3/迁移优先及 C4 附录的分流，toy 或预期数值不会进入科学结论。
**Plans:** 尚未制定。

## Progress

| Phase | Plans Complete | Status | Code Evidence | Scientific Evidence |
|---|---|---|---|---|
| 1 | 7 / 7 summaries | Local code done | pytest 65 passed | pending_server |
| 2 | 1 / 1 | Local tiny-model done | hooks/cache/generate | pending_server |
| 3 | 1 / 1 | Local probe/transfer done | conformal/transfer tests | pending_server |
| 4 | 1 / 1 | Local intervention geometry done | INLP/C-rand tests | pending_server |
| 5 | 1 / 1 | Local analysis/repair done | P1/P3 tool tests | not_evaluated |
| 6 | 0 / 1 reviews | CLI done; A–F in progress | CLI e2e | pending_server |

16 项需求全部映射且各映射一次；详见 REQUIREMENTS.md。首个后续入口：`$gsd-plan-phase 1`。
