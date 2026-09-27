# Project Research Summary

**项目：** Reasoning Diff

**日期：** 2026-09-20

**状态：** 初始化研究完成；实现未开始；科学实验未运行。

**综合置信度：** MEDIUM。外部事实主要来自固定版本官方源码、模型配置和数据说明；架构与协议仍须实现和实验验证。

## Executive Summary

后续应建设一个小型 Python 科学实验包，以 CLI 和可追溯文件产物贯通数据、轨迹、事件、标签、探针、干预与分析。科学核心是区分任务结构依赖与模型有限扰动响应，优先检验 C3 和跨模型迁移；C1 是测量工具，C2 提供带对照的功能证据，C4 放附录。

完整 T2/T3 的主要缺口不只是模型适配，而是独立任务真值和有效编辑资产。现有数据并不普遍提供逐事件 DAG；缺失必须显式保留，不能由被测 CoT 或 probe 预测补造。先导实验应先建立可靠的 T1 数据/测量链路，再把同样的契约扩展到各任务域。

本次仅交付 GSD 初始化文档，后续代码由用户同事实现。所有需求为 Pending，关闭自动推进。本机接口预研不能替代服务器验证；Gate 0–2 的正式定义及阈值保持未注册。

## Key Findings

### Stack

- 建议使用 Python 3.11、PyTorch、Transformers、JSONL 和数值 NPZ。普通显式前向/解码循环便于核对 hook、随机流和缓存；不需要先引入推理服务、数据库或通用调度框架。
- 本机核查对象为 PyTorch 2.7.1+cpu / Transformers 5.5.3。版本建议来自现有可验证组合，不意味着最新版或适合所有 GPU；服务器构建另行锁定。
- Qwen3 和 R1 Distill 的 thinking 模板、tokenizer 元数据与 token IDs 不同，不能共用手写模板。保存实际输入、原生成 token、精确前缀与边界。
- 在核查版本中，decoder-layer 输出为 Tensor；post-residual hook 不重算本层已经得到的 KV，仅影响后续层。条件之间必须隔离缓存；`use_cache=False` 不保证传入缓存不被修改。

详见 [STACK.md](STACK.md)。其中微型随机模型检查仅为一次性 API 可行性研究；后续仍需纳入正式可重复测试。

### Features and Data

| 数据 | 已核对事实 | 对后续实现的影响 |
|---|---|---|
| iGSM | 官方 `facebookresearch/iGSM` 提供生成器；依赖对象为 `problem.template`；默认算术模数 23 | 导出真实题干前提到参数的映射，保留模数，不能用结构图 G 或共享 RNG 节点替代输入依赖 |
| GSM-Symbolic | 公开模板与预生成题；parser/generator 未发布，当前核查树无可直接复用的 NoOp 目录 | 实现本项目受限公式/标注合同及派生 no-op 资产，不能承诺调用不存在的官方生成 API |
| GSM-Plus | 数据卡包含禁止训练用途的说明；没有完整逐事件 DAG | 固定为评测来源，保留同源题族；不用于探针、方向、校准或适配拟合 |
| HotpotQA | `supporting_facts` 是答案证据，不是所有推理事件的完整祖先图 | 完整 C3/Oracle 需要独立标注子集；支持文档外的句子不能一律视作已知无关 |
| MuSiQue | `question_decomposition` 的引用可恢复组成关系；Full 中同 ID 有可回答/不可回答变体 | 记录参考分解粒度、变体身份和共同题族，不能把参考分解等同于所有合法推理路线 |
| HumanEval | 测试判断程序行为；官方执行 guard 不是沙箱 | Spec 编辑要带新参考实现/区分测试；隔离环境缺失时记不可用，不在宿主执行 |

每个域需要真实读取、合法扰动、独立真值、事件映射、域内评分及适用实验入口，不只交付空 schema。文档未核实到与其语义编辑要求完全对应的官方 HumanEval-Perturb 资产，暂按项目派生集设计，不能声称该资产不存在。细节见 [FEATURES.md](FEATURES.md)。

### Cross-Model Transfer

首批 Qwen3-8B 的 hidden size 为 4096，R1-Distill-Qwen-7B 为 3584，因此此模型对在原始坐标上的冻结直接迁移不适用。必须报告维度不兼容，或在独立配对数据上学习映射并明确标记为适配；不得补零、截断后仍称直接迁移。步骤向量与前提向量两个输入均需正确映射。

如要正式检验同维直接迁移，需在后续计划中额外选择并核查可兼容模型对，先明确预算；不凭本次研究强加新模型。即便同维，也不保证语义坐标相同。

### Architecture

以 `Task → Trace/Event → Observation → Label/Feature → Probe/Calibration → Intervention/Repair → Report` 为产物链。数据真值独立建立；测量与派生标签分开；预测器拟合与最终测试分开。每个阶段冻结输入与配置清单，并保存失败/未知记录。

按基础题族划分训练、开发、方向拟合、校准、迁移配对和测试。真实的样本/模板独立性和统计功效不能由 500 题配置自动保证。校准单位是完整轨迹/编辑序列或明确的问题块，不能把同题多随机流当成独立样本增加 N。完整合同见 [ARCHITECTURE.md](ARCHITECTURE.md)。

### Critical Pitfalls

1. **假负标签：** 有限扫描未变化、未扫描、未对齐与结构变化必须分开；经验 M 不能被描述为已经证明没有读取。
2. **噪声身份：** 异 seed 的一步值变化没有天然 premise 身份。必须先定义匹配编辑机会的 sham 协议；缺少协议时 corrected 量为 null。保留有符号差值。
3. **前瞻泄漏：** 目标首 token 或跨界 token 均不可进入步前特征。事后人工定位边界与在线预测边界分开报告。
4. **对照失真：** C-rand/C-layer 同 cohort、同样本、同随机流并匹配实际注入范数；主结论比较相对对照差异，并保留非目标损伤和无效输出。
5. **统计误判：** P1 比较相对链长+op 的留出增量；P2 处理新增前提改变分母；P3 无效不能推出“虚假依赖只是后果”。
6. **覆盖夸大：** 逐边分位数不是整链校准；单点无响应不证明联合编辑 soundness；预测集合覆盖不保证文本嫁接正确。

风险、预防机制与未来验收夹具详见 [PITFALLS.md](PITFALLS.md)。

## Implications for Roadmap

1. **数据与测量先行：** 先确保来源、语义真值、事件身份、划分和噪声机会可复核，随后模型采集才有可靠评价对象。
2. **模型接口独立验收：** 用无权重下载的微型模型核对 cache/hook/边界，再在服务器验证真实模型。
3. **探针与公平基线同阶段：** 避免只有可解码性没有额外信息价值；迁移、校准和拟合谱系一起设计。
4. **干预独立阶段：** 在 P3 前就实现来源解耦及两类对照，不能观察效果后补控制。
5. **C3 和附录功能分析：** 区分代码可算出指标与科学现象成立，所有决策处理未运行/不足/未注册状态。
6. **最后整体验收与交接：** CLI、恢复、失败统计和服务器协议完整闭合，科学结论另待真实运行。

## Open Decisions and Prerequisites

- Gate 0–2 的正式定义、阈值、样本量与检验标准：用户确认留待预注册。
- 噪声机会构造、部分图的可识别范围、自然语言人工核查方案：第一阶段明确并冻结。
- 独立标注、合法语义编辑、新答案与 donor 响应表：后续研究资产，不由程序猜测。
- 同维直接迁移模型对、校准功效、P1–P3 多重比较与条件扩展规则：在真实测试前确定。
- GPU/CUDA 构建、真实上下文长度、精度、attention backend、代码隔离执行器：服务器阶段验证。

## Sources

以下仅列影响路线的主要一手来源；固定 revision 和逐条核查入口保留在四份研究文档中。

- [iGSM 官方仓库](https://github.com/facebookresearch/iGSM)、[默认运算参数](https://github.com/facebookresearch/iGSM/blob/a1ed1d04600add811beb08b58d9912ed30999642/const/params.py)：T1 导出与运算语义。
- [GSM-Symbolic 官方仓库](https://github.com/apple-aiml-research/ml-gsm-symbolic)、[GSM-Plus 官方数据卡](https://huggingface.co/datasets/qintongli/GSM-Plus/blob/main/README.md)：公开资产边界与数据使用要求。
- [HotpotQA](https://github.com/hotpotqa/hotpot)、[MuSiQue](https://github.com/StonyBrookNLP/musique)、[HumanEval](https://github.com/openai/human-eval)：任务格式、真值粒度与评分边界。
- [Qwen3-8B 配置](https://huggingface.co/Qwen/Qwen3-8B/blob/b968826d9c46dd6066d109eabc6255188de91218/config.json)、[R1-Distill-Qwen-7B 配置](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B/blob/916b56a44061fd5cd7d6a8fb632557ed4f724f60/config.json)：模型形状与直接迁移限制。
- [Qwen3 固定版本实现](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/qwen3/modeling_qwen3.py)、[HF cache 文档](https://huggingface.co/docs/transformers/en/cache_explanation)：hook 和缓存契约。
- [Conformal tutorial](https://arxiv.org/html/2107.07511v6)、[Subspace patching illusion](https://arxiv.org/abs/2311.17030v2)：校准条件与干预证据限制。
