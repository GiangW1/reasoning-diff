# Domain Pitfalls: Reasoning Diff

**Domain:** C3 虚假依赖、跨模型探针迁移及前瞻干预的科学实现
**Researched:** 2026-09-20
**Confidence:** MEDIUM。`gsd-tools query classify-confidence --provider websearch --verified` 返回 MEDIUM；以下是原方案约束与一手资料交叉核查后的实现建议，不是已获得的科学结果。

依据 `.planning/PROJECT.md` 和原方案 §§2–5、7–12。项目后续约定优先：C3 与跨模型迁移为主线，C4 全部在附录，Gate 0–2 未预注册。以下数值仅为验收夹具，不是科学阈值或实验结果。

## Critical Pitfalls

### 1. 用值或文本相似度代替事件身份

**风险：** 相同数字来自不同变量、版本或作用域；数值编辑改变表达式文本；插入一次重复计算使按出现序号硬配对发生偏移。错误对齐随后污染行为标签、S/M、探针与干预。

**预防：** 身份至少保存基础题、任务节点/规范符号表达式、变量、版本、作用域及解析证据。规范表达式引用稳定 premise ID，不能把被编辑数值本身作为唯一身份。版本对应不明确时保留歧义。`matched`、`unmatched`、`ambiguous`、`parse_failure`、`disappeared/merged/strategy_changed` 分开；结构变化不能自动成为值响应。任务祖先未知也不能用空集合代替。自然语言任务允许部分真值，不能从支持文档标签臆造完整步骤 DAG。

**必须通过的检查：**

- 两个作用域的 `x=3`、同作用域不同版本的 `x=3` 不互相匹配；交换数值大小不改变匹配结果。
- `q=p1+p2` 中 p1 的值变化仍对齐到同一任务事件；两个不同任务节点恰好同值不能对齐。
- 删除、合并、解析失败只增加对应状态计数，不增加行为正例或负例；保留全部原始事件及分母。

### 2. 把有限扰动与固定 seed 当成完备因果真值

**风险：** 没观察到变化被解释为不存在依赖；共享全局 RNG 被执行顺序、不同长度、批次和对照采样消耗，导致所谓同 seed 实际没有复用同一随机流。

**预防：** 每条记录保存允许编辑域、实际编辑、执行/有效比较数、响应数、模型/tokenizer/代码版本、生成参数、随机流及环境。区分 `observed_response`、`no_response_observed_in_scan`、`unknown`；有限扫描可定义有明确范围的 empirical zero，不能将其称为绝对无依赖。未扫描、无对齐或失败必须 mask 为 unknown。只有已定义有限域被完全有效扫描时才可声明该域内阴性。按样本保存并重置独立采样状态，方向生成与 rollout 使用独立 RNG。

PyTorch 明确不保证同 seed 在不同平台、版本或 CPU/GPU 间完全复现；因此单个 seed 字段不足以建立随机流协议。[PyTorch reproducibility](https://docs.pytorch.org/docs/2.14/notes/randomness.html)

**必须通过的检查：**

- 未扫描一列、扫描失败一列、扫描后未变化一列，序列化后仍是三种证据状态；训练 loss 不把 unknown 当 0。
- 基础函数 `f(x,y)=xy` 在 `(0,0)` 单独编辑 x 或 y 都不变，联合编辑到 `(1,1)` 却改变。该夹具必须阻止把单点扫描推广为任意联合编辑 soundness。
- 同环境下相同输入与完整采样状态重放一致；改变任务调度顺序不改变每个样本的随机流。跨设备/版本没有通过重放验证时明确标记不可比较。

### 3. C3 的 S/M 与噪声扣除改变了被测对象

**风险：** `S=B\T` 与 `M=T\B` 混成不一致率；unknown 被计入 M；异 seed 的事件变化没有 premise 身份，却被广播成每个 premise 的噪声依赖；将负的扣除结果裁成 0，系统性抬高现象。

**预防：** 保存任务集合 T、经验行为集合 B、逐边可评估掩码和标签协议。完整可评估数据用 `rho_S=|B\T|/|P\T|`，并显式定义 `rho_M=|T\B|/|T|`；M 应称该有限扫描下未观察到响应的任务边。空分母为 null。部分观测分别报告观察下界/未知比例或已声明的可评估子集统计，不能悄悄改分母后沿用完整密度名。

原方案尚未定义如何把异 seed 比较映射到 `(event,premise,edit)` 的噪声机会。必须保存显式 sham/no-edit 配对协议，并匹配扰动扫描的比较次数与 ANY 聚合规则；不可把一对异 seed 轨迹的值差直接当成有 premise 身份的因果标签。该参照包含合法随机路线差异，扣除量是相对于所选参照的 operational excess，并非可识别的逐边去噪真值。协议缺失时仍可输出 raw，但 noise/excess 为 null。

同一基础题、同一可评估事件/前提集合上计算并保存 `raw`、`noise_reference`、`excess=raw-noise_reference`、配对数、覆盖率与不确定性；按问题聚合后给区间。完整数据与共同可评估子集结果并列，避免幸存者选择。

**必须通过的检查：**

- T={p1,p2}，B={p2,p3}，P={p1,p2,p3,p4} 时 S={p3}、M={p1}，两种密度均为 1/2；若 p1 未扫描，不能宣称它是已确认漏读。
- raw=0.2、noise=0.3 得 excess=-0.1；零分母、缺噪声、缺配对返回 null 与原因，不能返回 0。
- 同一事件在噪声条件消失时，不能比较两个不同事件分母的均值；结构变化和共同集合覆盖率仍输出。
- 增加每前提的编辑尝试数时，同时增加 sham 机会；不得把 ANY-over-10 的响应率减去单次 sham 率。

### 4. “步前”特征实际含目标首 token

**风险：** 使用目标首 token 的 hidden state、对完整续文重新分词得到不一致边界、跨界 token 部分包含目标内容，或边界检测器读到目标后才决定位置。

**预防：** 以实际生成 token IDs、字符/字节跨度和 chat template 保存边界。前瞻特征与 donor 提取都仅见目标第一个 token 之前的前缀。选取最后一个完整落在前缀中的 token；跨界 token 整体排除，无可用位置时标记不可表达。步前、数值前、步尾单独存储。事后 oracle 边界可用于离线测量，但应标记，不得冒称在线边界预测。

**必须通过的检查：**

- 固定前缀、替换两种不同目标续文，前瞻特征完全相同；包含空格/换行及目标文本的一个 token 不能被池化进入前瞻特征。
- 干预发生时生成长度严格不含目标首 token。仅修改目标后缀不能改变被选前缀的特征或 donor 来源。
- 保存 hook 相对 attention/MLP/residual 的位置；零扰动重放与无 hook 的 logits/轨迹相符，KV 更新仅覆盖该 hook 实际可影响的位置和后续层。

步前可解码支持“生成前含预测信息”，不能单独推出依赖已经不可逆地决定；来源跟随干预也需下列控制。

### 5. 同超参数不等于等范数干预

**风险：** C-rand/C-layer 投影后的实际范数不同；随机控制事后补跑；只报告输出变化而隐藏非目标损伤；救援只是代数上撤销消融。

**预防：** 同批次锁定主条件、C-rand、C-layer 的 base/donor、位置、随机流、rank 与采样参数。C-layer 仅改变预先声明的层与对应方向，在开发集选取弱编码层。记录实际 delta 的注入前后范数、相对 residual 范数与有效 rank；控制 delta 按样本匹配主 delta 的实际范数。随机子空间基满足 Q^TQ=I，不要把“正交基”误写为必然与候选子空间正交。零投影单列退化状态，不能除零后丢样本。

四项结局同时报告：目标来源响应、非目标响应、任务正确率、无效输出率；主效应是相对两种对照的配对差。正确来源、错误来源、随机分量救援分开；原位补回恰好撤销消融只能作为实现 sanity check。a=b 的任务对用于来源/数值解耦，真正判别来源跟随还需 a!=b 且每个条件重取 donor。

子空间 patching 可通过非预期通路改变输出，控制与救援只能增强定位证据，不能证明唯一中介。[Subspace activation patching illusion, v2](https://arxiv.org/abs/2311.17030v2)

**必须通过的检查：** 同一试验缺任一对照即不生成完整因果比较；注入后实际范数在预先声明的数值容差内一致；rank/零范数异常仍计数；全部条件使用相同配对 ID；只改变非目标或只使输出失效不能算来源跟随成功。

### 6. 跨模型维度不兼容被静默“修好”

**风险：** 源探针输入 d_A、目标表示 d_B 不同，靠截断/补零后称直接迁移；只映射步骤 h，不映射双线性探针的 premise e；用测试配对拟合归一化或共同空间。

**预防：** 冻结源模型探针的直接迁移只在特征形状与已声明输入约定兼容时运行；否则 `not_applicable: incompatible_feature_space`。同宽本身也不证明两个坐标系有相同语义。无标签配对适配、监督适配分别标记：在独立配对集拟合 d_B→d_A 映射，或先建共同 k 维表示再训练该空间中的源探针；步骤与 premise 两类输入都要遵循对应映射。没有标签参与还须禁止用标签选层、rank、归一化或映射超参数后称“完全无标签”。

SciPy 标准 `orthogonal_procrustes` 要求两矩阵形状相同，不能直接处理两种隐维；共同空间降维、中心化与变换都属于适配。[SciPy official reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.orthogonal_procrustes.html)

**必须通过的检查：** 例如 d_A=4、d_B=6 的直接模式明确拒绝；适配模式可输出兼容形状且保留训练 split hash；篡改测试表示、测试标签或打乱测试配对不能改变已拟合映射；仅映射 h、遗漏 e 的配置报维度错误。直接、无标签配对、监督结果不得合并一列。

### 7. 逐边校准冒充整链覆盖

**风险：** 平铺 event/premise 行后取分位数、插值或差一位索引、遗漏序列后续轮次、把未知标签当空真集，得到没有所称保证的高覆盖率。

**预防：** 固定探针和打分规则后，每条完整轨迹取所有已定义真边的最大 `(1-p)`；连续编辑取完整序列内最大值。N 必须计独立可交换单位，不能把同题多 seed/变体当独立轨迹重复扩大 N：可每基础题取一条轨迹，或将全部重复构成问题块后取块内最大值并声明更换了覆盖单位。任务头/行为头分别校准；行为头只对所用经验标签协议主张覆盖。预测集合覆盖不等于重算正确，也不保证跨模型/跨任务分布漂移后覆盖。

使用 k=ceil((N+1)(1-alpha))，k≤N 时直接取排序后第 k 项，k>N 时 +infinity；预测边使用 `1-p<=q`。真正已知空真集分数才为 0；标签缺失、无校准数据、alpha 未定义不能作为有效校准。此为 split conformal 的完整轨迹打分，不应与重拟合的 full conformal 算法混称。[Conformal tutorial v6, Appendix D](https://arxiv.org/html/2107.07511v6#A4)

**必须通过的检查：**

- N=4、scores=[0.1,0.2,0.3,0.4]、alpha=0.4 时 q=0.3；alpha=0.1 时 q=+infinity，并选择全部有限分数的候选边。
- 一条轨迹其他边全好但一条真边分数 0.9，轨迹分数必须为 0.9；连续编辑最后一轮出现该边时序列分数也为 0.9。
- 等于 q 的边被保留；unknown-only 轨迹不记作空真集；JSON 将 infinity 以明确状态/表示保存，不能偷偷变成未经解释的 null 或 1。

### 8. 同题变体、拟合工件与测试之间泄漏

**风险：** 数值编辑、改名、no-op、seed、不同模型轨迹或编辑序列跨划分；测试集参与 INLP、标准化、层选择、迁移配对、阈值选择。

**预防：** 先按稳定基础题/来源家族 ID 分组，再切 `train/dev/direction_fit/calibration/transfer_pairs/test`。若主张未见模板/图组合泛化，还需按对应家族留出。每个拟合工件保存输入组 ID、配置与 hash；校准在选模型/层/超参数后进行。测试 S 可用于最终测量；依赖测试 S 选择 P3 方向的结果只能标为单独的 oracle 分析。[Grouped cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)

**必须通过的检查：** 为同题构造改名、no-op、两个 seed、两个模型、连续编辑变体，它们只能有一个 split；所有拟合工件的组集合与 test 无交集；改变测试标签不能改变任何训练/校准/方向/适配工件。

## Statistical and Decision Pitfalls

### 9. P1 的 AUC 高于 0.5 不证明增量预测力

**预防：** 预先固定以错误还是正确为正类；在独立训练数据拟合 `length+op` 基线与 `length+op+rho_S_excess` 完整模型，再在相同 held-out 基础题比较 AUC、delta-AUC 与区间。不能用训练内 AUC。偏相关采用明确的协变量处理，并与 logistic 系数/预测价值区分；它们均不构成因果识别。按基础题聚类 bootstrap，保留全部 seed/变体一起重采样。层/任务分面探索与预先指定检验分开，避免反复挑层后只报最好一项。

**检查：** 仅 length 能完美预测的夹具，加入复制 length 的 rho 不应被判为有额外信息；单类别测试集 AUC 为 null；bootstrap 抽中的基础题带走全部成对条件；未注册显著性标准时只输出估计量与区间。

### 10. P2 混淆 no-op 真值、分母变化和配对缺失

**预防：** 先用任务语义验证注入前后答案及所有已有节点祖先集合不变；改变约束、消歧义、引入矛盾的句子不算 no-op。记录注入位置与表面相关度；模型是否保持答案不是 no-op 真值裁判。GSM-Symbolic 提供变体敏感性的动机，不提供本项目事件级因果标签。[GSM-Symbolic v2](https://arxiv.org/abs/2410.05229v2)

no-op 增加 P，也增加 rho_S 分母；同时报告完整定义密度、共同已有前提上的配对变化和新注入列响应。固定 delta 符号，例如 `delta_acc=acc_noop-acc_base`，不要与“准确率下降量”混用。相同基础题/随机流做配对；invalid、结构改变、缺失配对全部保留并报告，不靠静默内连接挑幸存题。

**检查：** 加一条完全无响应的非祖先时，完整密度可以下降，但共同前提响应必须不变；仅改变分母不能被写为已清除依赖。缺 base 或 noop 的题不参与配对差，但计入缺失；注入导致任务答案变化的夹具拒绝 no-op 标签。

### 11. P3 的恢复率由选择偏差或全面损伤驱动

**预防：** 消融目标与方向在独立拟合/开发数据定义；不能观察测试响应后挑方向、挑失败题再将结果当总体提升。若研究失败子集，预先声明筛选规则，并同时给全体结果。比较与同 seed 基线、C-rand、C-layer 的配对正确率差；无效输出保留在意向评估分母。INLP 删除某可解码特征并不自动等于只删除 S，仍需目标与非目标响应检验。

**检查：** 干预使难题解析失败而删除这些行时，评估必须检测分母变化；主条件与随机控制同样改善时不能宣布特异效应；P3 未检出恢复只能记“该干预未提供支持”，不得生成“虚假依赖是后果而非原因”的句子。

### 12. Week-8 把 null 当 false 或偷偷发明 Gate 阈值

**预防：** Gate 0–2 维持 `threshold=null`、`decision=unregistered`；测量照常输出，代码验收照常推进。Week-8 区分未运行、数据不足、协议无效、未预注册、探索性测量及按已注册标准作出的结论。只有有效数据与预先登记规则齐备，才可给有方向的科学判定；不能把缺 P2/P3 当“不成立”，不能因为 corrected rho 没显著就自动补一个默认 alpha。后续实验的条件执行规则本身也须显式记录，不能在未定义判据时自动跳过必需实现。

| 输入情形 | 必须输出 |
|---|---|
| Gate 阈值为 null，测量看起来很强 | 数值、区间、`unregistered`；无 pass/fail |
| 没有真实模型数据或只有 toy fixtures | `not_evaluated`；无 P1/P2/P3 科学结论 |
| 噪声协议缺失或事件身份无效 | 对应指标 null 与原因；保留 raw/失败记录 |
| P2 有支持，P3 未检出效应 | 分别报告；不推导反向因果或“只是后果” |
| P1 未达到已注册标准 | 报告该检验未支持；不等于不存在依赖 |
| 所有预注册检验与控制支持主张 | 才能推荐主文地位；同时保留效应区间与适用范围 |

**检查：** 将每个阈值/指标依次设为 null，报告器不能崩溃、转换成 0、触发通过或写入负结果；所有分流保留 protocol version、decision reason 和 evidence IDs。

## Moderate Pitfalls

- **把代码验证写成科学结果：** fake/toy/mock、随机初始化模型、真实权重 smoke test 和正式实验运行分开标记。报告器拒绝将 fixture 的 AUC/F1/正确率汇入论文主表；不得抄原方案预期 F1、TO、CSP 数字作为已测值。
- **数据真值来源混淆：** 自建 arithmetic DAG 标为自建，不能冒充官方 iGSM；T2/T3 不完整解析必须保留 partial/unknown。数据来源、版本、派生编辑及人工核查记录进入 provenance。
- **C4 把验证器变成执行门控：** Oracle 与预测掩码共用无门控执行器；离线评分不能触发回退或筛掉错误。掩码正确不证明嫁接正确，联合编辑也无单点扫描 soundness。测试校验器输出不改变执行路线；保留重算、额外 prefill、探针与实际耗时。
- **代码任务在宿主机运行：** T3 生成代码必须交给明确隔离且有超时/资源限制的执行器。隔离后端不可用时记录 unavailable，不能退回宿主机 `exec`；验收用不能启动宿主执行的 spy backend。

## Phase-Specific Warnings

| 阶段主题 | 必须先解决的风险 | 验收证据 |
|---|---|---|
| 数据/轨迹基础 | 身份、版本、作用域、unknown、来源 | 重复变量/结构改变夹具；六类 split 清单 |
| 行为标签/C3 | 有限扫描、随机流、sham 机会、密度分母 | 重放记录；raw/noise/excess；覆盖与失败计数 |
| 探针/迁移 | token 泄漏、双输入维度、测试拟合 | 跨界 token 夹具；4→6 维直迁拒绝；工件泄漏检查 |
| 轨迹校准 | 单位错置、有限样本分位数、partial truth | 第 k 项/+infinity/整序列末轮夹具 |
| 前瞻干预/P3 | 等实际范数、同批控制、非目标损伤 | 三条件配对矩阵、KV/zero-hook 校验 |
| P1/P2/Week-8 | 分母与分组统计、null-safe 决策 | held-out 增量比较；no-op 共同宇宙；null 真值表 |
| C4 附录/T3 执行 | 未证 soundness、隐藏回退、宿主执行 | 联合编辑反例、全失败计数、隔离后端记录 |

## Sources and Remaining Gaps

一手外部来源均于 2026-09-20 核查；研究 seam 选择 jina，但本环境无该工具，已用内置 WebSearch 检索及官方页面交叉核对，摘要已缓存。原方案中的待测/预期数值未当作证据。

- [PyTorch reproducibility](https://docs.pytorch.org/docs/2.14/notes/randomness.html)：文档标记更新 2026-05-14；随机性与平台边界。
- [Conformal tutorial, arXiv v6](https://arxiv.org/html/2107.07511v6)：版本日期 2022-12-07，采用 Appendix D 的精确定义；HTML 顶部另有生成日期，不能当作新论文版本。
- [Subspace patching illusion, v2](https://arxiv.org/abs/2311.17030v2)：2023-12-06；控制不等于机制唯一定位。
- [SciPy orthogonal Procrustes](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.orthogonal_procrustes.html)：同形状输入约束。
- [scikit-learn grouped validation](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data)：依赖组不能跨训练/验证。
- [GSM-Symbolic, v2](https://arxiv.org/abs/2410.05229v2)：2025-08-27；模板变体评估背景。

仍须在阶段协议中落实：噪声对照到 premise/edit 机会的构造与有效性；自然语言/多跳事件真值覆盖；真实 tokenizer 边界及各模型 hook/KV 行为；跨模型配对适配方案；P1–P3 的检验与多重比较规则。Gate 0–2 阈值继续未预注册，不能由这些研究建议补定。
