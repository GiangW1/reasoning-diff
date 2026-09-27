# Architecture Patterns — Reasoning Diff

**Domain:** 前提依赖表征与干预的离线科学实验

**Researched:** 2026-09-20

**Confidence:** MEDIUM；官方接口已核对，具体模型 hook 与科学有效性仍需后续验证。

**Scope:** 本次仅初始化文档；以下为同事后续实现的契约，不表示代码、数据或实验已经完成。

## Recommended Architecture

采用一个 Python 包、分阶段 CLI 和可追溯的文件产物。JSONL 保存结构化记录，NPZ 保存数值数组；不引入 Web 服务、数据库或通用工作流框架。模块按证据的生产与消费划分，CLI 只负责参数解析及阶段调用。

```text
prepare ──> tasks + edits + independent graphs + frozen splits
                 │
collect ──> traces + raw events + selected hidden features
                 │
label ────> aligned observations + task/behavior/noise labels
                 ├──> fit ──> probes + text baselines + transfer mapping
                 │             └──> calibrate ──> fixed calibration artifact
                 ├──> intervene ──> controlled continuations + response records
                 └──> repair ──> appendix continuations + cost records
                               │
analyze <── immutable artifacts ┴──> metrics + intervals + decisions + report
```

箭头表示产物依赖，不要求全部数据驻留内存。每个命令接收输入 manifest 与配置，输出一个新阶段目录；离线分析不反向影响生成。任务 DAG 与任务真值在观察待评模型输出之前建立。

### Component Boundaries

| 组件 | 输入 → 输出 | 责任边界 |
|---|---|---|
| `artifacts` | 配置、上游 manifest → 校验后的读取器、完成 manifest | 身份、哈希、版本、shard 与恢复；不决定科学标签 |
| `tasks` | 本地数据快照、独立标注 → Task、Edit、split manifest | T1–T4 适配及合法变体；自建算术与官方 iGSM 明确区分 |
| `models` | Task、生成协议、随机流 → Trace、Feature | 冻结 HF 模型、精确 token 位置、显式 residual hook；不调用评分器 |
| `events` | Trace、任务实体目录 → Event、Alignment | 身份/版本/作用域匹配，导出人工核查；不按数值相等判定身份 |
| `measure` | 原版/扰动/sham 事件 → Observation、Label | 原始观测与有限协议汇总分开；保留结构变化和未知 |
| `probes` | Feature、Label、指定 split → Probe、Prediction、Calibration | 双头低秩探针、边界 MLP、拟合与校准；不接触测试拟合 |
| `baselines` | 同一标签/划分/可见前缀 → Prediction | 文本、注意力与自述方法，共用评分接口；反思另列可见性档 |
| `interventions` | 冻结方向、donor plan、base prefix → Intervention | 来源交换、消融/INLP、救援与配对对照；不据结果重选方向 |
| `repair` | 编辑、原槽位、预定掩码 → RepairRecord | 同一执行器处理各掩码，无门控/回退；评分在生成后进行 |
| `executor` | 代码候选、测试、隔离配置 → ExecutionResult | 只在显式隔离环境内执行代码；独立于模型推理进程 |
| `analysis` | 已完成产物 → Report | TO/CSP、S/M、迁移、P1–P3、成本、失败与决策；不调用模型 |

这些是包内职责，不要求每个组件单独成为服务、类层次或插件系统。

## Canonical Artifact Contracts

所有记录至少包含 `schema_version, record_id, run_id, base_group_id, status`；阶段相关字段缺失必须给出原因。记录以 ID 关联，不依赖 JSONL 行号；数组索引用 ID 映射行号。

| 产物 | 最小内容 | 不变量 |
|---|---|---|
| **Task** | `task_id, base_group_id, variant_id, tier, source, upstream_id, upstream_split, premises[], question, answer_spec, graph_ref, edit_ref` | 前提有稳定 ID、原文本与字符区间；图状态为 complete/partial/unknown；空图不同于未知图 |
| **Trace** | `trace_id, task_id, model_ref, tokenizer_ref, prompt_bytes_ref, token_ids, decoded_text, generation_config, rng_ref, stop_reason, cost` | 保存实际模板化输入及实际生成 ID；失败/截断仍是一条轨迹；不以再编码文本替代原 token |
| **Event** | `event_id, trace_id, semantic_key, char_span, token_span, value, value_kind, task_node_ref, parser_version, audit_ref` | `semantic_key=(entity/expression, occurrence_version, scope)`；值可未知；事件位置与身份分开 |
| **Observation** | `observation_id, reference_trace, comparison_trace, edit_id, premise_id, rng_pair, event_pair, outcome, raw_values, alignment_ref` | outcome 区分 changed/no_change/structural/unaligned/parse_failed/generation_failed；每次计划机会都有记录 |
| **Label** | `event_id, premise_id, task_label, task_known, behavior_label, behavior_known, noise_ref, protocol_ref, evidence_ids, opportunities` | 任务标签、有限行为标签、噪声参照独立；未知不填 0；每个标签能回溯原始观测 |
| **Feature** | `trace_id, event_id/premise_id, layer, hook_name, position_kind, token_index, visible_prefix_end, array_ref, dtype, shape` | 三位置明确为 pre_step/pre_value/post_step；特征产物不混入标签和答案；跨界 token 有处理状态 |
| **Probe** | `head_type, feature_spec, rank, weights_ref, fit_split_ref, selection_split_ref, label_protocol, training_config` | task/behavior 两头及权重分开；边界 MLP、方向与迁移映射保存各自拟合谱系 |
| **Intervention** | `experiment_plan_ref, condition_id, control_group_id, base/donor refs, target_event, hook, prefix_ref, direction_ref, actual_norm, continuation_ref` | 保存未干预、主干预、C-rand、C-layer、救援/错误来源结果及失败；主干预必须在目标首 token 前 |
| **Report** | `input_manifest_ids, metric_spec, split_ref, numerator, denominator, n_base_groups, interval_spec, exclusions, decision_status` | 能仅从固定输入重建；零分母为 N/A；代码验收与科学结论分列 |

补充产物不另造平行身份体系：

- **Edit** 保存被修改的前提、操作、前后值、合法性证据、变体家族与生成随机流；no-op 保存注入位置和独立的非祖先判定。
- **Alignment** 显式保存 matched、missing、merged、split、version_changed、ambiguous；合并或分岔不悄悄当作普通值变化。
- **Calibration** 保存已冻结 probe ID、校准 base groups、轨迹/序列单位、分数、分位数规则、alpha 和标签可用范围。
- **Prediction** 保存 event/premise、头类型、原始 score、阈值或校准 ID、可见性档；不得只保存最终二元集合。
- **RepairRecord** 保存轮次、槽位掩码及来源、原始 token 预算、实际生成/额外 prefill、失败类别和离线评分。

## Immutable Manifests and Resume

每阶段先固定 `run_spec.json`，包含输入文件哈希、配置、协议版本、代码 revision、环境锁定信息、模型/分词器 revision、精度、硬件、模板和所有随机流设置。身份字段不使用可变的 latest 名称。

处理过程写入临时 shard 和尝试日志；shard 完成后原子发布，最后生成只读 `manifest.json`，列出文件哈希、记录数、数组 shape/dtype、成功/失败计数及上游 manifest ID。manifest 自身摘要不递归包含自己。

恢复只复用与当前 run spec 一致且校验通过的完成 shard；残缺 shard 不作为分析输入。重试保留原失败和 `attempt_id`，预先定义重复结果的计数规则，不能从多次生成中选最成功的一次。

改变任务、标注、划分、模型、hook、前缀或协议时产生新产物，旧产物保留。修正标注附上旧版本引用与原因；不在原 JSONL 中静默覆盖。

JSONL 存变长 metadata；NPZ 只存数值数组，读取使用 `allow_pickle=False`，避免对象数组触发 pickle。数组按有界 shard 加载，不假设压缩 NPZ 可直接内存映射。[NumPy load](https://numpy.org/doc/stable/reference/generated/numpy.load.html)

## Base-Level Splits

先给原始基础题分组，再生成变体、轨迹和跨模型对应样本。数值改动、改名、no-op、连续编辑、不同随机流和不同模型输出继承同一 `base_group_id` 与角色。

| 角色 | 允许使用 | 禁止用途 |
|---|---|---|
| `probe_train` | 探针、文本基线、边界 MLP 和 P1 预测器拟合 | 替代校准或测试 |
| `dev` | 层/秩/超参数、C-layer 选择、文本阈值与诊断 | 作为最终无偏报告集 |
| `direction_fit` | 交换/INLP/选择性消融方向拟合 | 与最终测试题共享变体 |
| `calibration` | 冻结打分器后的完整轨迹/编辑序列校准 | 再选模型、方向或指标 |
| `transfer_pairs` | 无标签模型间表示配对拟合 | 使用目标测试表示或标签学习映射 |
| `test` | 一次固定协议下的预测、干预及最终分析 | 拟合以上任意对象 |

六种角色按 base group 互斥；比例和样本量在数据准备阶段确定，500 题配置不自动保证各角色有足够统计能力。数据源只允许测试使用的部分只能进入 test，不能被全局随机划分重新分到训练。

结构/OOD 留出使用冻结的题目或模板/图家族规则；同时保存 upstream split。跨模型配对继承基础题角色；donor/base 都来自对应实验允许的同一角色，成对选择不跨训练与测试。

区间按基础题聚类；同题多变体、多个 event 或多个随机流不是独立样本。P1 AUC 在留出题上计算，logistic 模型及特征处理不得在被报告的测试题上拟合。

## Independently Annotated Natural-Language DAGs

T1 自建算术 DAG 可作本机解析夹具，来源写明自建；官方 iGSM 需要实际生成器版本与导出证据。两者共用 Task 契约，报告时分层。

T2/T3 自然语言题采用独立标注产物：标注者根据题面、独立参考解及证据建立 `premise → assertion/operator → target` 图，记录节点身份、作用域、关系证据、标注者、修订和复核状态。待评模型的 CoT、probe 分数与干预效果不参与真值构建。

支持句、答案或单元测试只能提供其实际覆盖的证据；不能自动扩展成全部中间事件的完整祖先图。无法确定的节点映射或边保留 unknown。只有祖先集合已确认完整时，未列入集合的前提才能成为可靠 task negative。

新变体重新确认参考答案和依赖结构；只改名且语义保持的变体可引用已审计的身份映射。no-op 的无关性须按任务语义核查，不能仅凭生成提示宣告。

原始标注与模型事件映射分开审计，保留分歧和未对齐样本。T4 允许 strategy_changed、unsatisfiable、unknown；不强行把所有推理建成同一 DAG。

图未知的样本仍可采集行为响应、结构变化和答案表现，但不能进入需要完整 task truth 的 S/M 或任务 Oracle 主表。报告这些指标覆盖的子集与排除原因。

## Measurement and Visibility Protocol

`label` 从逐次 Observation 汇总，不从探针预测反推真标签。同随机流语义编辑与零扰动配对噪声参照使用一致的事件/前提机会规则；保存尝试数、成功对齐数和值可判定数。

行为正例表示声明的有限扰动集合内观察到变化；行为 0 表示在已实施且可判定的扫描中未观察到变化，并附覆盖度。未对齐、失败或未扫描不等于负例；有限扫描也不证明全部允许编辑均无影响。

S、M 分别在所需标签已知的交集上计算。保存原始密度、同机会噪声密度及有符号 excess，不能把负差截为零或制造一个“去噪真值图”。空分母记 N/A，结构变化独立计数。

TO/CSP 同时报出全链/干净区域、对齐覆盖率和分母；干净事件由独立任务图选定，不以“值碰巧没变”选取。审计抽样同时覆盖成功、失败及未知。

每个样本/条件保存隔离的生成随机流；配对条件采用同一声明的逐步随机数序列。编辑生成、划分和随机方向使用独立随机流；仅把全局 seed 重置一次不足以定义跨 batch、分叉长度与恢复后的配对协议。

## Feature Extraction and Model Adapter

冻结模型的自然生成是 Trace 的来源。隐状态只保留所需前提池化和事件位置的选层特征，避免长期保存全部层×全部 token；边界检测训练另外保存预定 token 子集。

保留 chat template、特殊 token、思考模式、padding、attention mask 与位置约定。官方 Tokenizers 提供原输入 offsets，但生成 ID 到解码字符的精确映射仍须单独核验；无法一致映射时标记 boundary_unknown。[Encoding](https://huggingface.co/docs/tokenizers/en/api/encoding)

设目标开始字符为 c，所有与 c 或之后目标内容相交的 token 均不可用于 pre_step 特征；取完全位于目标前的最后 token 状态，记录有效可见前缀。pre_value 同理排除首个数值 token；post_step 单独标识为回溯读数。

离线使用完整轨迹确定事件位置，只能用于标注索引，不能把未来 token、事件内容或答案送入特征。记录 `boundary_source=offline_annotation/prefix_detector`；在线边界检测必须只见当前前缀，两者不混报定位能力。

每模型适配器显式给出 residual hook 的完整模块名及层内位置。HF 通用 hidden_states 与末层输出可能存在归一化差异，不能把二者默认等同。[Model outputs](https://huggingface.co/docs/transformers/en/main_classes/output)

干预时保留目标前边界以前的 base KV，在选定位置重新前向并应用 hook，再计算受影响后续层和该位置 KV，然后继续采样。缓存长度、attention mask、position 与更新范围都进入记录；不直接把保存的隐藏向量当作完整 KV。[HF cache](https://huggingface.co/docs/transformers/en/cache_explanation)

同维模型仅在输入形状兼容时尝试冻结的直接迁移；同维并不保证坐标一致。异维先在独立无标签配对集拟合映射，冻结后在留出题评估，明确写作 paired adaptation；不把适配后结果称为直接迁移。

校准单位为完整轨迹或完整编辑序列，task/behavior 两头分别校准；若标签仅部分可用，只能声明对该观测范围的覆盖，不能承诺全真实依赖覆盖。

## Intervention Contract

实验执行前冻结 donor/base 列表、目标事件、高层来源预测与非目标响应矩阵。来源相异但数值相同的例子用于解耦；真正评价来源跟随后，还需可区分来源的数值条件，且每个条件重新提取 donor 特征。

一个 `control_group_id` 绑定未干预、主干预、C-rand、C-layer；消融和救援沿用匹配协议。这里“同批次”指同一预定实验 cohort 与运行协议，可受显存限制顺序执行，但不能结果出来后补选对照。

记录实际扰动范数、维数、hook、token、采样配置与随机流。C-rand 在同层同位置同秩并匹配范数；C-layer 层由 dev 预定，位置/幅度协议固定，零范数及无法匹配的情况保留。

救援补回同位置匹配分量，另含错误来源和随机分量。不得对未来已生成 token 做手术后标为前瞻实验。

所有条件报告目标来源跟随、非目标分支响应、任务正确率和无效输出率，并报告相对两个对照的差。P3 失败只限制该干预协议的证据，不自动证明虚假依赖是后果。

## Explicitly Isolated Code-Task Executor

代码评分通过一个窄接口提交 source/test 哈希、语言、运行镜像摘要、输入和资源限额，返回 exit/timeout/resource_limit/executor_error、截断的 stdout/stderr、测试结果和耗时。

推荐后续在专用 Linux 隔离运行器中执行：无网络、无宿主工作区/凭据挂载、只读运行环境、临时可写目录、非特权用户、CPU/内存/进程/墙钟限制。具体隔离后端在实施阶段验证，不把普通 Python subprocess 称为沙箱。

宿主只负责提交及读取结果；执行器缺失或隔离不满足契约时输出 executor_unavailable。禁止回退到宿主 exec，也不把“没有执行”当测试通过或候选程序错误。

HumanEval 官方执行文件明确说明 reliability_guard 不是安全沙箱，因此不能直接复用其宿主执行路径。[HumanEval execution](https://github.com/openai/human-eval/blob/master/human_eval/execution.py)

## Appendix Repair and Reporting

所有掩码共用原轨迹槽位执行器：Task Oracle、Behavior Reference、probe、监督文本、截断、匹配预算随机、prompt instruction 与 full recomputation。每类的可用标签范围单独记录。

保留槽位文本在编辑后的当前前缀中重新 prefill；连续编辑亦重新提取状态，不能沿用旧前缀隐藏状态。预算按选中槽位的原始 token 数匹配，实际生成长度另计。

评分器在运行结束后读取输出；不触发门控、动态重选掩码或 verifier fallback。成本分列首次建索引、每轮解码、额外 prefill、probe、调度与端到端时长，保存硬件及缓存协议。

Report 同时输出机器可读 JSON/CSV 和简短 Markdown。Gate 0–2 的未注册阈值保留 null，decision 为 unregistered；Week-8 输出测量、区间与适用规则状态，不能默认成功。C3 与迁移优先，C4 全部置于附录。

## Build Order and Acceptance

下面是后续实现顺序及验收设计，本次不创建实现或运行这些测试。

| 顺序 | 构建内容 | 本机 CPU 代码验收 | 服务器科学验收 |
|---|---|---|---|
| 1 | 身份/manifest、T1–T4 适配契约、独立图、划分、事件和观测 | 本地夹具贯通已知/未知/结构变化，变体不跨角色，hash 可追溯 | 官方数据真实来源与独立标注审计、对齐误差估计 |
| 2 | 模型适配、边界、随机流和成本 | tiny 随机初始化 HF 模型离线运行；核验位置、缓存、恢复与无目标泄漏 | 固定真实模型 revision；真实生成/offset/hook 一致性及资源测量 |
| 3 | 双头探针、文本/注意力/自述、校准与迁移 | 小矩阵检查标签 mask、角色限制、形状与预测谱系 | 同题留出评估、基线公平性、跨模型结果和覆盖范围 |
| 4 | 来源交换、INLP/消融、救援、C-rand/C-layer | 预声明响应矩阵、配对记录和实际范数；完整保留失败 | 主干预相对对照、非目标损伤与救援的真实证据 |
| 5 | C3 P1–P3 与附录 repair | 合成统计夹具验证分母/区间协议/不截断 excess；离线评分不改变轨迹 | no-op 配对、留出 AUC、聚类区间、干预及修复失败分布 |
| 6 | 全 CLI、分片恢复、报告、交接 | 无网络离线 smoke、所有模块审查、可复现目录及服务器配方 | 在已注册协议下报告 Gate/Week-8；科学阴性同样完整保留 |

代码执行类样本即使在 CPU 验收中也只进入显式隔离执行器；无执行器可验收接口拒绝路径，但代码执行能力必须标为未验证。

验收状态至少区分 `code_verified`、`real_data_verified`、`scientific_evaluated`。toy/mock 与随机模型只能证明实现路径，不进入论文效应表；服务器运行失败、阴性和未注册都不改写为成功。

## Patterns, Risks and Scale

| 采用的模式 | 避免的反模式 | 扩展条件 |
|---|---|---|
| 单阶段纯产物输入/输出 | 一个脚本边采集边拟合边筛选好结果 | 单机先按 base group 分 shard，再分配多个进程/设备 |
| 小型模型专属 adapter | 以统一层号假装不同架构 hook 相同 | 每个新增模型先核验位置及续写等价 |
| 有界数组 shard 与 ID 索引 | 全量隐状态放进 JSON 或一次加载所有 NPZ | 只有实测 I/O/内存不足后再替换存储，不先建数据库 |
| 原始观测与派生标签分开 | 用 probe 预测或生成链填补任务真值 | 更多数据集复用契约，保留各自缺失范围 |
| 未注册/未知/失败显式记录 | 用默认阈值、丢弃样本或回退掩盖问题 | 报告按有效分母和完整尝试数并列 |

## Sources and Confidence

- 项目约束：`.planning/PROJECT.md`、`.planning/REQUIREMENTS.md`；原始研究材料：`Reasoning-Diff-修订方案-v3 (1).md`。材料中的数值和科学推论不视为已验证结果。
- 官方接口：[HF cache](https://huggingface.co/docs/transformers/en/cache_explanation)、[Model outputs](https://huggingface.co/docs/transformers/en/main_classes/output)、[Tokenizers Encoding](https://huggingface.co/docs/tokenizers/en/api/encoding)。
- 产物与执行：[NumPy load](https://numpy.org/doc/stable/reference/generated/numpy.load.html)、[HumanEval execution](https://github.com/openai/human-eval/blob/master/human_eval/execution.py)、[HumanEval README](https://github.com/openai/human-eval/blob/master/README.md)。
- 已调用 research-plan；其选择的 Context7/Jina 与 ctx7 CLI 不可用，使用官方站点 websearch 回退并缓存摘要。classify-confidence(provider=websearch, verified=true) 返回 **MEDIUM**。
- 上述分层、字段、拆分与顺序均为依据项目约束和官方接口作出的架构建议，置信度 MEDIUM，非已验证实现。待专项验证：Qwen 各层 hook/KV 行为、生成 ID/字符映射、自然语言 DAG 标注可靠性、样本量与校准条件、隔离后端。
