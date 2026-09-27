# Requirements: Reasoning Diff

定义于 2026-09-20。以下为同事后续实现的验收需求，不是本次初始化已交付的功能。代码验证与科学验证分别记录。

## v1 Requirements
- [ ] **DATA-01**: 可导出并适配官方 iGSM，保留运算语义、DAG 和前提映射；支持 op=5/10/15/21、500 题配置及数值/改名/no-op/来源—数值变体。独立测试夹具不得冒称官方数据。
- [ ] **DATA-02**: 可适配 GSM-Symbolic/GSM-Plus、HotpotQA、MuSiQue、HumanEval，并导入独立标注、构造经核验的扰动；T4 支持策略变化/约束退化标注。缺失图真值显式 unknown。
- [ ] **DATA-03**: 基础题及全部变体共组划分，遵守测试专用限制，记录文件/记录身份和来源。
- [ ] **MEAS-01**: 按事件身份/版本/作用域对齐，保存结构变化、失败和未知；可导出与回填人工复核。
- [ ] **MEAS-02**: 同随机流编辑、配对噪声机会；分开保存任务/有限行为/噪声标签、S/M 原始量/参照/有符号差值；TO/CSP 带完整分母与覆盖率。
- [ ] **MODEL-01**: 支持冻结 Qwen3 与 Qwen2/R1 的 HF 推理，按需采集隐状态和三种边界位置；精确 token 对齐、独立随机流、断点续跑及真实 token/耗时计量。
- [ ] **PROBE-01**: 实现任务/行为双线性低秩头、带未知掩码的加权 BCE、两层边界 MLP、开发集选择与独立完整轨迹/序列校准。
- [ ] **BASE-01**: 实现监督文本、attention/rollout、零样本/少样本/反思/监督 verbalizer 对照；相同标签和划分，按可见前缀区分前瞻与回顾层级。
- [ ] **XFER-01**: 仅在维度兼容时执行冻结直接迁移；不兼容时明确 N/A，无标签配对适配与监督适配分别拟合、留出评估和报告。
- [ ] **CAUSAL-01**: 实现目标首 token 前的交换、选择性消融/INLP、救援与错误来源对照；同批次 C-rand/C-layer 并匹配实际范数。
- [ ] **CAUSAL-02**: 干预前保存来源—数值解耦 donor 和高层响应矩阵，报告目标/非目标/任务正确/无效输出及全部失败。
- [ ] **C3-01**: P1 使用留出预测、链长/op 控制与问题级区间；P2 使用 no-op 配对效果；P3 使用对照后的选择性消融恢复效果。
- [ ] **REPAIR-01**: 附录实现无门控嫁接，Oracle/预测/文本/截断/随机/提示/全重推及检索对照；以原始 token 控制预算，记录逐轮成本及离线失败类型。
- [ ] **OPS-01**: 提供准备/采集/标注/拟合/校准/干预/修复/分析 CLI、清单、配置校验、断点与分片、服务器运行说明；代码任务用隔离执行器评分。
- [ ] **QA-01**: 单元/回归及随机微型 HF CPU 集成测试不依赖真实权重或网络；全模块审查，可复现性、适用条件与未验证项有文档。
- [ ] **DECIDE-01**: Gate 0–2 默认为未预注册，实施 Week-8 分流，C3/迁移优先、C4 附录；不输出未经验证的肯定结论。

## Paper-derived atomics (indexed from source, not in the original 16)
- [ ] **SURF-01**: 表面提及 $R^{surf}$ 与值依赖分开标注，供文本保留/符号替换。
- [ ] **CONE-01**: 脏锥 $\mathrm{cone}(\Delta P)$、任务 Oracle 与行为预测掩码分开；单点扫描反例阻止联合编辑 soundness 宣称。
- [ ] **ATTN-01**: 前提注意力均值、Attention Rollout、开发集头聚合，阈值在 dev 上选定。
- [ ] **VERB-01**: 零样本 / 5-shot / 反思 / 监督 verbalizer 四档，监督档与探针同样本、划分、可见前缀。
- [ ] **COST-01**: 首次索引、额外 Prefill、Decode、探针、调度、端到端延迟分列。
- [ ] **GEOM-01**: 附录跨模型几何：独立配对共同维映射 + Procrustes；直接/无标签/监督分列。
- [ ] **RETR-01**: 附录检索余弦相似度 vs 答案是否改变，不得删除。
- [ ] **FIT-01**: 附录锥传播两参数拟合，禁止“定律”措辞进入报告。
- [ ] **CONT-01**: 连续编辑 $k\in\{1..5\}$、序列级校准、保留文本重新 Prefill。
- [ ] **FAIL-01**: 失效分类：漏检、重算错误、嫁接接口、策略分岔、约束退化；验证器不回退。
- [ ] **STRUCT-01**: 消失/合并/版本变化/策略分岔单独计数，不并入值变化标签。
- [ ] **POS-01**: 步前 / 数值前 / 步尾三位置分别采集与报告；跨界 token 不得进入前瞻特征。
- [ ] **PROP1-01**: 过近似条件下干净步值保持的 soundness 命题作为可检查协议，不用单点扫描宣称联合成立。
- [ ] **PROP2-01**: 整链/序列保形覆盖按 max(1-p) 与 ceil((N+1)(1-α)) 顺序统计量实现。
- [ ] **TOPO-01**: 局部重算复用原轨迹槽位顺序，不重新拓扑排序。
- [ ] **MEDIATION-01**: 交换公式 H' = H_base + Π_Z(H_donor − H_base) 与 IE_Z 定义可计算。
- [ ] **IE-01**: 干预效应相对 C-rand/C-layer 差值报告，绝对值不单独作结论。
- [ ] **INLP-01**: INLP 构造子空间并正交移除；四项结局齐全。
- [ ] **BOUND-01**: 2 层 MLP Hidden=256 ReLU 步尾边界检测器。
- [ ] **T2NOOP-01**: 原版/注入配对，位置与表面相关度分层；项目派生名不得冒称官方 NoOp。
- [ ] **TABLE1-01**: 主文 5 条对照与附录 3 条基线分列实现。
- [ ] **WEEK1-01**: 三轨迹配置、50 条干预冒烟、噪声扣除后的首次 ρ 计数作为可运行入口，不是已测结果。
- [ ] **EXEC-01**: 科学评测禁用门控/Fallback；验证器只离线评分。
- [ ] **R7-01**: 步前显著低于步尾时记录主张回退分叉，不伪造“已经决定”。
- [ ] **R4-01**: 监督文本接近探针时记录主文重心转移，不删除功能证据路径。
- [ ] **REST-01**: 步前可解码不得写成已经决定。
- [ ] **REST-02**: P3 未检出不得写成虚假依赖只是后果。
- [ ] **REST-03**: 单点无响应不得写成任意联合编辑 soundness。

## Out of Scope
Real GPU experiments, dataset/weight downloads on this machine, RL, production gates/fallback, publication.

## Traceability
| Requirement | Phase | Status |
|---|---|---|
| DATA-01 | 1 | implemented_local / pending_server |
| DATA-02 | 1 | implemented_local / pending_server |
| DATA-03 | 1 | implemented_local |
| MEAS-01 | 1 | implemented_local |
| MEAS-02 | 1 | implemented_local |
| MODEL-01 | 2 | implemented_local_tiny / pending_server_weights |
| PROBE-01 | 3 | implemented_local / pending_server_fit |
| BASE-01 | 3 | implemented_local |
| XFER-01 | 3 | implemented_local |
| CAUSAL-01 | 4 | implemented_local / pending_server_donors |
| CAUSAL-02 | 4 | implemented_local_schema / outcomes pending_server |
| C3-01 | 5 | tools_implemented / not_evaluated |
| REPAIR-01 | 5 | implemented_local |
| OPS-01 | 6 | implemented_local |
| QA-01 | 6 | local_tests_exist_not_acceptance / independent_review_round06 |
| DECIDE-01 | 6 | unregistered_null_path |

Coverage: 16 requirements, 16 mapped, 0 unmapped. Status only becomes Complete after implemented and verified.
