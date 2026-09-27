# Feature Landscape: Reasoning Diff

**Domain:** 推理依赖、虚假依赖与跨模型迁移的科学实验代码仓库
**Researched:** 2026-09-20
**Scope:** GSD 初始化研究；本文件是后续实现要求，不是已交付代码或实验结果。
**Confidence:** MEDIUM。通过 `gsd-tools query research-plan` 获取六组 `websearch` 查询，核对官方仓库、源代码、数据卡与论文；`classify-confidence --provider websearch --verified` 返回 MEDIUM，未交叉验证的检索返回 LOW。下文官方事实采用 MEDIUM；设计建议明确作为本项目建议。未下载大数据集或权重，未运行模型或生成代码。

## 核心建议

先建设能保留来源、独立任务标签、实测行为、事件对齐和失败的共享流水线，再接入每个任务域。完整 T2/T3 范围包括读取、合法扰动、真值更新、轨迹采集、标签、评分、探针迁移及适用的干预／修复实验入口，不能止于 JSON schema 或空适配器。

数据读取器齐全不代表依赖真值齐全。iGSM 有可导出的生成器图；MuSiQue 有组成子问题关系；GSM 与 HotpotQA 需要项目补注；HumanEval 测试只判程序行为。未知标签保持未知，禁止由被测模型的答案或编辑响应反推 `R_task`。

优先 C3 与跨模型迁移，C1 提供测量工具，C2 提供功能检验；C4 完整保留为附录功能与边界实验。任务代码、外部数据资产、真实 GPU 实验分别验收。

## Table Stakes

| 功能 | 为什么必须有 | 复杂度 | 后续验收要求 |
|---|---|---|---|
| 来源与运行清单 | 原始数据、项目派生和测试夹具必须区分 | 中 | 保存来源 URL/revision/hash、原始 ID、派生过程、模型版本、随机流和配置 |
| 六类真实数据适配器 | T1/T2/T3 是已确认范围 | 高 | iGSM、GSM-Symbolic、GSM-Plus、HotpotQA、MuSiQue、HumanEval 均有读取和域内评分路径 |
| 独立任务图与标注侧车 | C3 的差集必须有独立参照 | 高 | 图／公式／人工标注有来源；缺失用 null/unknown，不能填全零 |
| 合法扰动与真值更新 | 改输入后原答案常常失效 | 高 | 数值、查询量、约束、no-op、文档、Spec 编辑有对应新真值与保留条件 |
| 基础题族划分 | 防止同题变体进入训练与测试两边 | 中 | 同题、模板实例、编辑序列、donor 配对、跨数据集同源题共同分组 |
| 事件身份和对齐 | 相同数值不代表相同事件 | 高 | 保留变量/表达式/版本/作用域、未对齐、重复、合并、消失与路线改变 |
| 多扰动行为记录与噪声参照 | 一次不变不能证明无依赖 | 高 | 原轨迹、同题异随机流、同随机流编辑轨迹和逐次响应可复查 |
| 任务头、行为头与文本基线 | 标签对象和可见信息需公平 | 高 | 同划分、同边界可见前缀；不混用任务与行为标签 |
| 跨模型迁移 | 主线结果必须能复现 | 高 | 独立配对集合；直接迁移、无标签映射、监督映射分别标识 |
| C3 P1/P2/P3 | 用户指定主线 | 高 | 原始量和噪声参照并存；部分真值只报告可识别子集；P3 不由测试结果拟合方向 |
| 来源交换、消融、救援 | 检验信息是否参与行为 | 高 | 目标首 token 前干预；同批次 C-rand/C-layer、范数、非目标响应与无效输出 |
| 域内离线评分及成本 | 正确率与执行失败不能互相遮盖 | 高 | 数值／QA／程序评分分开；所有失败进入计数；代码通过隔离执行器 |
| 无门控局部重算和 T4 | 保留附录与边界科学范围 | 高 | Oracle 与预测掩码共用执行器；记录 Prefill、Decode、延迟、结构变化及无解 |
| 本机轻量验收 | 当前没有真实实验机器 | 中 | 离线夹具覆盖全流程，输出明确标记 fixture；真实科学状态保持未验证 |

## 官方数据事实与最小接入合同

以下事实置信度均为 MEDIUM；“实现建议”是根据已核查资源形成的项目设计。

### T1：iGSM-Diff

**官方资源：** [facebookresearch/iGSM](https://github.com/facebookresearch/iGSM)，核查 revision `a1ed1d04600add811beb08b58d9912ed30999642`。原材料的 FAIR 归属与仓库相符，不应改成“非官方”。`IdGen` 有 `op` 参数；`max_op` 只是上限。官方生成器的任务依赖对象是 `id_gen.problem.template`（NetworkX DiGraph）；`G` 是结构图，两者不能互换。[生成器入口](https://github.com/facebookresearch/iGSM/blob/a1ed1d04600add811beb08b58d9912ed30999642/data_gen/pretrain/id_gen.py)

**可导出对象：** `prob_dict`、`problem_order`、`sketch`、`lookup`、`ques_idx`、`N`、`name_dict`、`topological_order`，以及图节点和边。`sketch` 含表达式，`lookup` 值是 `Num`；题干只输出对应 instance parameter 的定义句。`whole_template` 还扩展了参数集合，不能不加选择地把所有节点当成题干前提。[Problem 源码](https://github.com/facebookresearch/iGSM/blob/a1ed1d04600add811beb08b58d9912ed30999642/math_gen/problem_gen.py)

**关键语义：** 官方 `mod=23`，`Num` 加减乘均按该模数运算。通用模型提示与评分应明确记录这一算术域；普通整数算术变体只能作为注明变更的派生任务。[参数定义](https://github.com/facebookresearch/iGSM/blob/a1ed1d04600add811beb08b58d9912ed30999642/const/params.py)

**实现建议：**

- 导出源生成器状态再建立本项目任务 IR；记录确切 `op ∈ {5,10,15,21}`，验证实际 `n_op`。不得以自建算术 DAG 冒充官方 iGSM。
- 用实际题干定义句构成 `premise_id`，建立“定义句 → 对应语义参数”的边，再接上参数计算边。这样直接引用前提的事件也包含该前提；仅做 `nx.ancestors(q)` 并把参数当输入会漏掉自身定义句。
- `(-1,0,0,0)` 是共享 RNG 节点，不能把它当所有随机常量的唯一输入前提。常量、乘数和关系定义归属各自题干句；采用参数 ID 和表达式位置稳定定位编辑。
- 导出表达式中的参数引用与字面量，不把缓存的旧 `lookup` 当新编辑的答案。冻结图、名称、表达式顺序后只改声明的字面量，按拓扑顺序重算并同步渲染；重新调用随机 `parse` 可能引入额外随机变化。
- 图中的结构祖先不保证每个具体数值扰动都会改变输出；零值、抵消与模碰撞都允许，保留 `R_task` 与有限扫描的 `R_behavior` 差异。
- 原包导入 `tools.tools` 会加载 GPT-2 tokenizer。离线适配器应延迟导入并接受预置的来源快照；正常单元测试不隐式联网。[tools.py](https://github.com/facebookresearch/iGSM/blob/a1ed1d04600add811beb08b58d9912ed30999642/tools/tools.py)

### T2：GSM-Symbolic 与项目 no-op 配对集

**官方资源：** 原 `apple/ml-gsm-symbolic` 已重定向到 [apple-aiml-research/ml-gsm-symbolic](https://github.com/apple-aiml-research/ml-gsm-symbolic)，核查 revision `3b645c25d200bf950fb84e8cdcbfeccd91d6a8af`。README 明确生成器／parser 尚未发布。当前树提供 `symbolic`、`p1`、`p2` 模板及预生成数据，未提供可直接复用的 NoOp 目录；不能承诺调用不存在的官方生成 API。

**记录字段：** `id`、`instance`、`question`、`answer`、`original_id`、`original_question`、`original_answer`、`canary`。答案最终行采用 `####`。模板含 `id_orig`、`id_shuffled`、`question_annotated`、`answer_annotated`，可见初始化、合法性条件和答案表达式，但不提供任意自然 CoT 的事件身份与完整 DAG。[README](https://github.com/apple-aiml-research/ml-gsm-symbolic/blob/3b645c25d200bf950fb84e8cdcbfeccd91d6a8af/README.md)；[官方模板样例](https://github.com/apple-aiml-research/ml-gsm-symbolic/blob/3b645c25d200bf950fb84e8cdcbfeccd91d6a8af/templates/symbolic/0000.json)

**实现建议：**

- 读取全部官方 JSONL；按 GSM8K `original_id` / `id_orig` 建立共享题族，跨 P1/P2/symbolic 分组。`instance` 是抽样序号，不能作为独立划分键。
- 另建显式公式／关系侧车，写明变量绑定、单位、输入句 span、运算、约束和中间语义事件。通过受限表达式解释器重算真值；不对外部模板字符串直接 `eval`，不假装复现尚未发布的官方 parser。
- 数值编辑检查正负、整除、单位、取值域；新增运算、逆向求解和删约束使用对应公式版本。只改题干数字而继续沿用原 `answer` 属于错误适配。
- `reasoning_diff_noop` 是项目派生数据名，保留原数据来源，不冒称官方 GSM-NoOp 发布集。先独立证明注入句对声明目标无关，再固定题干位置与表面相关度；同时保留原始配对。
- 为测量注入前提的行为依赖，还需对注入句做允许的值／实体替换。仅插入一句并观察最终错误不足以形成前提—步骤行为矩阵。
- 插入会增加前提数。P2 同时报告新增前提响应、公共前提集合变化及分母；不要把不同分母的密度差直接当污染效应。
- 原始预生成数据目录标注 CC BY-NC-ND 4.0；仓库根软件许可不同。保留各资源许可元数据，优先交付适配代码与自写夹具，外部派生数据的分发另行处理。[数据许可入口](https://github.com/apple-aiml-research/ml-gsm-symbolic/blob/3b645c25d200bf950fb84e8cdcbfeccd91d6a8af/generated_data/README.md)

### T2：GSM-Plus

**官方资源：** 作者维护的 [qintongli/GSM-Plus](https://huggingface.co/datasets/qintongli/GSM-Plus)；数据卡与单条 viewer 记录交叉核查。字段为 `question`、`solution`、`answer`、`perturbation_type`、`seed_question`、`seed_solution`、`seed_answer`。官方描述为 1,319 基础题的 10,552 变体，涵盖数值替换、位数扩展、整数／小数／分数转换、增添运算、逆向运算、改写、干扰句、缺失必要信息八类。[数据卡](https://huggingface.co/datasets/qintongli/GSM-Plus/blob/main/README.md)；[原论文](https://arxiv.org/abs/2402.19255)

**实现建议：**

- 读取官方 test split 或用户提供本地快照。原数据未提供逐步 DAG，`solution` 不能直接当依赖标注；补注公式和输入句映射的子集才用于任务头与完整 C3。
- 以规范化 `seed_question` 的可复查匹配连接 GSM8K ID；找不到唯一匹配时保留来源文本哈希及未解析状态。不同数据集同源 GSM8K 题仍属同一题族。
- `reversing operation` 是改变被查询的量，不等价于简单把 `+` 换成 `-`。`critical thinking` 包含信息不足，不等价于约束矛盾；两类结果状态分开。
- 数据卡额外明确禁止训练用途。路线图应把 GSM-Plus 固定为评测来源；探针、方向、校准和迁移映射的拟合使用另有授权且划分独立的数据。这个安排也避免用公开 test 变体拟合后再报告迁移。

### T3-QA：HotpotQA

**官方资源：** [hotpotqa/hotpot](https://github.com/hotpotqa/hotpot)，核查 revision `3635853403a8735609ee997664e1528f4480762a`。原始格式为 JSON 数组；字段 `_id`、`question`、`answer`、`supporting_facts=[[title,sent_id],…]`、`context=[[title,[sentence,…]],…]`，以及 `type`、`level`。测试文件缺答案／支撑标注。支撑事实是答案证据集合，没有任意模型步骤的完整依赖 DAG。[官方格式与数据入口](https://github.com/hotpotqa/hotpot/blob/3635853403a8735609ee997664e1528f4480762a/README.md)

**实现建议：**

- 先接 labeled train/dev distractor 格式，避免把全 Wikipedia 检索工程误加为本任务前置条件。保存原段落标题、句索引和稳定 premise ID；文本编辑后保留 ID 映射。
- 项目侧车补充 bridge/comparison 的语义节点、支撑句到节点的边、独立答案与替代证据检查。`supporting_facts` 以外的句子不能自动标为所有事件的已知非祖先。
- “替换一个关键文档”可能同时改变多条事实，按文档编辑记录实际改变的多个 premise ID；若声称单前提编辑，必须限制到一条已标注事实。
- 替换后检查桥接实体、答案别名和其他文档的一致性；明确这是给定上下文中的反事实任务，不把新增事实当现实世界知识。答案变更、不可回答、矛盾分别保存。
- 复用官方答案 EM/F1 和 support 评分口径，事件级值与对齐由项目层单独评分；最终答案正确不能推出每个中间事件正确。[官方评分器](https://github.com/hotpotqa/hotpot/blob/3635853403a8735609ee997664e1528f4480762a/hotpot_evaluate_v1.py)

### T3-QA：MuSiQue

**官方资源：** [StonyBrookNLP/musique](https://github.com/StonyBrookNLP/musique)，核查 revision `922ac98f19a201998dbdae6d7f2887a5258dbdeb`。官方转换脚本提供 `id/question/answer/answer_aliases/answerable`；段落为 `idx/title/paragraph_text/is_supporting`；`question_decomposition` 每项含 `id/question/answer/paragraph_support_idx`。子问题中 `#k` 引用先前答案，可恢复已声明的组成关系；不可回答版本可缺对应支撑段落。[格式定义源码](https://github.com/StonyBrookNLP/musique/blob/922ac98f19a201998dbdae6d7f2887a5258dbdeb/raw_data_to_official_format.py)

**实现建议：**

- 将核查后的占位符引用转成子问题边，支撑段落成为输入；验证引用范围和拓扑顺序。保存该图的粒度为 `composition_reference`，不能宣称它覆盖任意自然 CoT 或所有替代解法。
- 细化到支撑句、断言和自然模型事件的映射仍需侧车标注。替换支撑文档后更新受影响子问题答案、最终答案、别名与可回答性，不能保留旧分解答案。
- MuSiQue-Full 的同一个 question ID 有 answerable/unanswerable 两条，官方评分器按这一配对设计。内部 `record_id` 加 variant/context fingerprint，`family_id` 保持同组，禁止按 `id` 去重丢记录。[官方评分器](https://github.com/StonyBrookNLP/musique/blob/922ac98f19a201998dbdae6d7f2887a5258dbdeb/evaluate_v1.0.py)
- 使用官方发布格式而非依赖其历史 AllenNLP 训练栈。数据包中的 dev/test 单跳来源排除清单需要进入防泄漏检查；相同组成单跳来源的独立性声明也要单独审计。[数据说明](https://github.com/StonyBrookNLP/musique/blob/922ac98f19a201998dbdae6d7f2887a5258dbdeb/README.md)

### T3-code：HumanEval 派生 Spec 编辑集

**官方资源：** [openai/human-eval](https://github.com/openai/human-eval)，核查 revision `6d43fb980f9fee3c892a914eda09951f772ad10d`。任务字段 `task_id/prompt/canonical_solution/test/entry_point`；生成结果为任务 ID 和 completion。测试提供最终功能判分，未提供前提—推理事件 DAG。[官方格式样例](https://github.com/openai/human-eval/blob/6d43fb980f9fee3c892a914eda09951f772ad10d/data/example_problem.jsonl)

未核实到与原材料“单条 Spec 语义约束改变”精确对应的官方 `HumanEval-Perturb` 发布资产；这是 LOW 置信度的检索缺口，不是“不存在”的结论。建议明确命名为本项目 HumanEval 派生集。[ReCode](https://github.com/amazon-science/recode) 与其[论文](https://arxiv.org/abs/2212.10264)主要研究保持语义的改写、命名、语法与格式扰动，可作控制组，不能提供新 Spec 的正确答案。

**实现建议：**

- 每个语义编辑包包含原任务 ID、原/新 Spec clause、修改 span、更新参考实现、新测试、预先列出的区分输入和不应改变的行为。诸如严格／非严格比较、排序方向、重复值策略可作为有限而明确的编辑族。
- 新参考实现必须通过新测试；预先选定的区分输入应能区别原/新规范。对无法区分的编辑保留原因，不伪造干预成功。
- 单元测试通过只说明已执行测试覆盖的行为。参考程序的数据流不自动等于任务依赖图，更不等于模型 CoT 的依赖。C3 所需 clause→语义事件关系必须独立标注；没有事件真值时仍可运行程序行为评测，但不能生成完整 C3 密度。
- 当前官方 `execution.py` 实际启用 `exec`，README 仍称其注释；源码也明确 `reliability_guard` 不是 sandbox，并使用 Unix `SIGALRM/setitimer`。不能依赖 README 或普通子进程保护宿主。[执行源码](https://github.com/openai/human-eval/blob/6d43fb980f9fee3c892a914eda09951f772ad10d/human_eval/execution.py)
- 所有模型生成程序及数据携带的测试必须交给显式隔离的执行器。后续代码应提供 Linux 容器执行路径、资源与超时限制、网络隔离、有限输入输出和完整状态；环境缺失记 `executor_unavailable`，不回退宿主执行、不记通过。

## 跨域最小合同（设计建议）

使用少量共享记录和任务域函数，避免建立通用插件平台。所有适配器至少提供读取、渲染可见输入、合法编辑、加载独立真值和域内评分；共享采集／探针／干预／修复模块消费统一对象。

| 记录 | 最小字段 | 不变量 |
|---|---|---|
| 来源记录 | dataset, revision/hash, native_id, family_id, variant_id, source_kind | `official/project_derived/fixture` 分开；外部缺标签不补造 |
| 前提 | premise_id, 原始 span, 文档/句/变量/条款定位, 类型 | 保留跨编辑映射；模型提示不含金标或 canary 元数据 |
| 任务参照 | provenance, graph_kind, nodes/edges, expressions, answer, coverage | 由生成器／作者标注／项目独立标注提供，不能来自被测行为 |
| 任务标签 | event_id, premise_id, true/false/unknown, annotation_ref | 部分图不能把 unknown 当 false；保留已知负例与标注范围 |
| 编辑 | edit_id, changed_premise_ids, before/after, edit_unit, validity, new_oracle | 多前提文档编辑不能冒充单前提；合法失败也可追溯 |
| 事件 | identity, semantic_value/type, scope/version, text/token_span, boundary | 值不进入身份匹配；边界不能包含目标首 token |
| 响应 | base/edited_run_id, random_stream_id, event_pair, response, status | 值变、未变、未对齐、结构变化、生成失败分开 |
| 评分 | metric, value/null, denominator, eligibility, failure_reason | 缺少科学依据时记 null；不伪造阈值判定 |

完整 `rho_S/rho_M` 只在相应事件的任务参照和测量覆盖条件明确时报告。仅确认注入句无关的样本，可报告这条已知负例的响应率，不能外推全前提集合的虚假依赖密度。MuSiQue 的组成图指标应表述为相对该参考分解的依赖，避免把另一条合法证据路线直接称为错误机制。

## 来源—数值解耦资产（设计建议）

这些资产不由上述数据集现成提供，需在任务编译层构造并先于模型实验锁定：

1. 同图族的来源 A/B 两种目标关系，先令 `a=b`，形成相同数值、不同依赖来源的配对；再提供同来源、不同数值对照。
2. 用 `a!=b` 的独立数值条件评分来源跟随，且让目标运算后的结果可区分；模 23 下也检查碰撞。每个条件重新提取 donor 表示。
3. 固定目标事件映射、高层交换后预期结果、非目标分支预期不变项，以及 base/donor 可见前缀。等值条件单独不能判定来源跟随成功。
4. 平衡来源位置、变量名、题面和分支；方向拟合、迁移配对与测试题族分离。自然 QA／代码只有独立来源标注充分的子集才进入交换实验，不使用简单句序替换假装来源任务。

## T4 边界与离线夹具（设计建议）

T4 同时包含策略分岔、缺失信息、明确矛盾、不可满足约束、事件删除／合并及多轮编辑。保留 `insufficient_information`、`inconsistent_constraints`、`no_solution`、`strategy_change` 的区别；数据集名称或一次解析失败不能直接确定类别。

后续实现应建立小而完整的自写夹具包，全部标记 `fixture`：

| 夹具 | 验证重点 |
|---|---|
| 算术 DAG：分支、无关项、零乘、抵消、模数环绕 | 完整祖先、自定义图来源、单点不变与结构依赖区别 |
| GSM 形状记录＋独立公式：数字、逆向、增删约束、no-op | 题族归组、合法性、重算答案、原始与变体前提映射 |
| Hotpot 形状的自写 bridge/comparison 文档 | 支撑标签不能自动生成所有事件边；替换后真值更新 |
| MuSiQue 形状分解：2/3/4 跳、缺失支持、重复问题 ID | 引用 DAG、null 标签、answerable 配对保留 |
| HumanEval 形状的微型 Spec 编辑 | 新旧测试区分、超时/语法错/执行器不可用；只经隔离器执行 |
| 预录轨迹：值变、结构变、未对齐、失败 | 行为矩阵、统计分母、修复计数和报告不漏失败 |

夹具可检验端到端代码连通性，不证明真实数据正确率、机制假说或模型迁移成立。真实来源读取可用少量获准快照做集成验收，不能把改写的夹具标成官方样本。

## Differentiators

| 功能 | 价值 | 复杂度 |
|---|---|---|
| 独立任务依赖与实测行为双标签 | 能区分任务结构、错误行为与噪声 | 高 |
| 已知无关前提配对与 P1/P2/P3 | 把最终掉点拆解为可定位、可干预的假说 | 高 |
| 来源与当前值解耦 | 减少只探出答案／数值的替代解释 | 高 |
| 同一标签协议下跨模型迁移 | 比较共享结构与模型特定行为 | 高 |
| 缺失和结构失败成为正式结果 | 避免只在成功对齐样本上得出过强结论 | 中 |

## Anti-Features

| 不建设／不采用 | 原因 | 采用什么 |
|---|---|---|
| 从模型输出推回 DAG 并当任务金标 | 形成循环标签 | 独立生成器、明确公式或人工侧车 |
| 缺金标时填空图或全零标签 | 会制造大量虚假依赖 | unknown 与指标适用范围 |
| 全数据集任意文本自动扰动 | 难以保证单前提与真值 | 声明支持的编辑族和独立新真值 |
| 无监督自动宣告来源交换成功 | 输出变化不等于来源跟随 | 区分数值条件与预先登记目标／非目标响应 |
| 测试或校准题用于方向与迁移拟合 | 污染结论 | 题族与用途分离 |
| 宿主执行 HumanEval 生成程序 | 违反项目明确隔离要求 | 独立隔离执行器 |
| 生产门控、Verifier Fallback、RL | 用户当前范围排除 | 无门控实验、离线评分 |
| 夹具指标或预期阈值当科学结果 | 不具备实测证据 | 测量值、来源标识、未判定状态 |

## Feature Dependencies 与路线图建议

```text
来源清单 + 题族划分 → 前提与独立任务参照 → 合法编辑和新真值
合法编辑 → 轨迹/事件/噪声参照 → 经验行为标签
两套标签 + 明确覆盖范围 → C3 P1/P2
独立拟合集 + 来源配对资产 → C2/P3 + 同批次对照
独立跨模型配对集 + 特征协议 → 跨模型迁移
共享采集/标签/评分 → T2/T3 全套实验适配
任务域 Oracle + 事件槽位 → C4 重算 → T4 失效分析
```

最先完成共同来源与标签合同、T1 官方导出和轻量全链验证；然后完成 C3 与跨模型测量工具；T2 的独立标注及 no-op 资产应提前准备，不能等到 P2 周才开始。T3 优先 MuSiQue 组成图和 HotpotQA 独立标注，再完成代码任务隔离执行与 Spec 编辑资产。完整 T2/T3 功能留在本项目路线图内，真实数据注释质量与真实 GPU 实验作为明确的后续工作记录。C4/T4 在共同标签和执行器可用后实现，不作为 C3 代码交付的额外生产门槛。

## 尚缺资产与置信度边界

- 需要作者标注或项目独立审阅的真实 T2/T3 premise→event 侧车；原数据不能自动补齐这一点。
- 需要项目 no-op 分层样本、来源—数值解耦配对和 HumanEval 语义编辑包；这些不是现成官方数据功能。
- 自然长 CoT 的事件抽取／对齐覆盖率、QA 替代证据、代码逐步语义标注的可行质量仍需阶段研究与真实样本检查。
- 模 23 任务提示、完整运算语义和真实模型适配需实验前核查；本轮只验证官方源码，不验证推理性能。
- 未注册 Gate 阈值保持 null；本轮不产生通过判断。原材料对步前“已经决定”、P3 失败“只能是后果”、有限单点编辑推出任意联合编辑 soundness 的推断均不能当代码验收事实。

以上调研 digest 已通过 research-store 缓存；仅本文件属于本研究员输出，未提交 Git。
