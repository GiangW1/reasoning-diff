# 技术栈与模型适配契约

**项目：** Reasoning Diff

**核查日期：** 2026-09-20

**范围：** Qwen3-8B、DeepSeek-R1-Distill-Qwen-7B 的 HF 接口、tokenizer、residual hook、缓存、随机流及 CPU 集成验证。

**置信度：** MEDIUM。GSD `research-plan` 指向 Context7，但本环境没有对应 MCP/CLI，故回退官方网页、固定版本源码和本机验证；`classify-confidence --provider websearch --verified` 返回 MEDIUM。下文区分官方事实、实现建议与实际完成的接口测试。

## 推荐并已核查的版本

使用普通 PyTorch + Transformers 的显式前向与解码循环。模型冻结；探针独立训练；不额外引入推理服务或 hook 框架。JSONL 保存轨迹与协议，NPZ 保存数值数组。

| 组件 | 建议固定版本 | 本机观察 / 理由 |
|---|---|---|
| Python | 3.11 系列 | 本机 3.11.7；本表依赖支持该系列 |
| PyTorch | 2.7.1 | 本机 `2.7.1+cpu`，微型模型验证通过；服务器单独选择与 GPU/CUDA 匹配的构建 |
| Transformers | 5.5.3 | 本机已安装；本报告仅对这一版本的 hook / cache 契约负责 |
| tokenizers | 0.22.2 | 满足 Transformers 的 `>=0.22.0,<=0.23.0` |
| huggingface-hub | 1.9.2 | 满足 Transformers 的 `>=1.5.0,<2.0` |
| safetensors | 0.7.0 | 读取官方权重格式 |
| NumPy | 1.26.4 | 本机版本；数组与 NPZ |
| pytest | 9.1.1 | 本机版本；CPU 集成与回归验证 |

以上七个包的精确版本已通过 PyPI JSON API 核实存在，亦与本机 metadata 相符；不代表它们是最新版本。Transformers 5.5.3 发布于 2026-04-09，要求 Python >=3.10；官方说明支持 PyTorch >=2.4。[Transformers 5.5.3](https://pypi.org/project/transformers/5.5.3/)、[其依赖元数据](https://pypi.org/pypi/transformers/5.5.3/json)、[PyTorch 2.7.1 安装渠道](https://pytorch.org/get-started/previous-versions/)。

CPU 开发环境可采用以下安装契约；本次研究没有执行安装或改变环境：

```text
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install transformers==5.5.3 tokenizers==0.22.2 huggingface-hub==1.9.2 safetensors==0.7.0 numpy==1.26.4 pytest==9.1.1
```

服务器若改变 torch、CUDA、attention backend 或精度，应重新跑接口一致性测试并生成独立环境清单；本机结果不能证明 GPU 数值等价。

## 两种模型必须分别适配

| 官方配置事实 | Qwen3-8B | R1-Distill-Qwen-7B |
|---|---|---|
| 模型 ID | `Qwen/Qwen3-8B` | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` |
| 核查到的 revision | `b968826d9c46dd6066d109eabc6255188de91218` | `916b56a44061fd5cd7d6a8fb632557ed4f724f60` |
| HF 架构 / model_type | `Qwen3ForCausalLM` / `qwen3` | `Qwen2ForCausalLM` / `qwen2` |
| 层数 / hidden_size | 36 / 4096 | 28 / 3584 |
| Q heads / KV heads | 32 / 8 | 28 / 4 |
| tokenizer 元数据类名 | `Qwen2Tokenizer` | `LlamaTokenizerFast` |
| `<think>` / `</think>` ID | 151667 / 151668 | 151648 / 151649 |
| tokenizer 最大长度 / config 最大位置 | 131072 / 40960 | 16384 / 131072 |

配置、模板与词表必须取自同一 revision，以 `AutoTokenizer` 加载；不要根据模型架构猜 tokenizer 类、词表或上下文上限。上表中的长度差异是真实元数据差异，实验应显式规定并验证总上下文预算。Qwen 官方称原生上下文为 32768；不能因 tokenizer 的最大长度为 131072 就自动启用相同长度实验。[Qwen 配置](https://huggingface.co/Qwen/Qwen3-8B/blob/b968826d9c46dd6066d109eabc6255188de91218/config.json)、[R1 配置](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B/blob/916b56a44061fd5cd7d6a8fb632557ed4f724f60/config.json)、[Qwen 模型说明](https://huggingface.co/Qwen/Qwen3-8B)。

**迁移结论：** 4096 维探针不能原样乘上 3584 维表示。此模型对的原始坐标“直接迁移”应报告 `not_applicable_dimension_mismatch`；独立配对集上拟合的共同空间或矩形映射属于适配迁移。不得通过截断、补零后仍称无适配直接迁移。即使维度相同，坐标可比性也需要实测。这是由配置维度推得的接口约束。

### Thinking 与 token 边界

- Qwen3 使用 `apply_chat_template(..., add_generation_prompt=True, enable_thinking=True)` 时，提示以 assistant 起始标记结束，**没有预先插入 `<think>`**。`False` 会在提示尾追加空 thinking 块；需区分 prompt tokens 与 generated tokens。[Qwen 模板](https://huggingface.co/Qwen/Qwen3-8B/blob/b968826d9c46dd6066d109eabc6255188de91218/tokenizer_config.json)。
- R1 当前模板已经追加 assistant 标记和 `<think>\n`；`enable_thinking=False` 不控制这个模板。不要再手工追加一次。其 opening tag 属于提示，生成片段可能只有 closing tag。模型卡推荐温度 0.5–0.7、避免 system prompt；这是科学运行配置建议，不能把 CPU 的 greedy 冒烟配置当成正式基线。[R1 模板](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B/blob/916b56a44061fd5cd7d6a8fb632557ed4f724f60/tokenizer_config.json)、[R1 模型说明](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)。
- 两种模型的 think 标签均标为非 special token，不能指望 `skip_special_tokens=True` 删除它们。运行时应从实际 tokenizer 解析 ID 并校验；上表 ID 来自各自固定 revision 的 tokenizer JSON。[R1 tokenizer](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B/blob/916b56a44061fd5cd7d6a8fb632557ed4f724f60/tokenizer.json)。
- 优先让 `apply_chat_template` 直接 tokenize。若先渲染字符串再编码，使用 `add_special_tokens=False`，避免重复 BOS。R1 的模型 config 与 generation config 的 BOS ID 还存在差异，不能自行从 model config 猜提示 BOS。[HF chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating)、[R1 generation config](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B/blob/916b56a44061fd5cd7d6a8fb632557ed4f724f60/generation_config.json)。
- 实现建议：保存原始生成 token IDs、模板后的 prompt、prompt 长度、未经清洗的解码文本及 token/span 对应关系。前瞻特征取目标事件首 token 之前的最后安全 token；跨越事件起点的 token 含有目标内容，不能计入前瞻特征。重编码必须验证与原生成 IDs 一致；不一致或无精确边界时保留失败/较早边界及间隔，不默默向后取整。

## Residual hook 与缓存的精确契约

**5.5.3 已核查：** 两种模型均访问 `model.model.layers[i]`，零基索引。decoder layer 的 `forward` 返回一个 `[batch, sequence, hidden]` Tensor，**不是 tuple**。整个 layer 的 forward hook 位于 attention residual 与 MLP residual 两次加法之后、模型最终 RMSNorm 之前。命名建议为 `resid_post`，并把 hook 名称、层号、全局 token 位置写进产物。[Qwen3 固定版本源码](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/qwen3/modeling_qwen3.py)、[Qwen2 固定版本源码](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/models/qwen2/modeling_qwen2.py)。

选择 `resid_post(i)` 意味着当前 token 在层 `<=i` 的 KV 已计算，干预只改变其后层的 KV 及 logits；若要改变第 i 层的 KV，应选择该层输入 residual 的 pre-hook，并定义另一种干预契约。不要声称 layer-output hook 重算了本层 KV。读取和干预应使用同一位置定义；`hidden_states[-1]` 是最终归一化后的输出，与末层 raw residual 不同。[输出捕获实现](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/utils/output_capturing.py)。

实现步骤建议：

1. 用 base 前缀建立截止边界 token **之前**的缓存；再输入边界 token，hook 只修改该次调用指定位置，随后计算下一 token 的 logits。
2. 返回克隆后的修改 Tensor，避免原位破坏共享读数；用 `try/finally` 移除 handle。hook 必须一次生效，后续 decode 不得重复施加。[PyTorch hooks](https://docs.pytorch.org/docs/2.7/generated/torch.nn.Module.html#torch.nn.Module.register_forward_hook)。
3. 每个 base/donor/intervention/control 分支独立缓存。朴素、可靠的实现是重新 prefill base；若克隆 `DynamicCache`，需验证张量无共享存储。缓存长度、mask 总长度、position IDs 和已输入 token 数必须对应。[HF 缓存说明](https://huggingface.co/docs/transformers/main/en/cache_explanation)。
4. **已验证的陷阱：** 5.5.3 的这两种 attention 实现在 `past_key_values is not None` 时更新缓存；即使 `use_cache=False` 仍可能修改传入对象，只是不返回它。无缓存参考前向应传 `past_key_values=None`。
5. 输入编辑或嫁接保留文本后，基于当前完整前缀重新 prefill。旧轨迹中后缀的 KV/隐状态不能当作新前缀状态；记录额外 prefill 成本。增量 decode 的局部位置通常为 0，全局位置必须由前缀长度解释。

## RNG 与采样

Transformers 5.5.3 的普通采样调用 `torch.multinomial` 时没有显式 generator；本机两种微型模型的 `generate(..., generator=...)` 都直接报未使用参数错误。推荐显式解码循环，使用独立的 `torch.Generator` 和 `torch.multinomial(..., generator=...)`，并完整实现/记录 temperature、top-k、top-p、EOS 与长度限制。[HF 采样源码](https://github.com/huggingface/transformers/blob/v5.5.3/src/transformers/generation/utils.py)、[PyTorch multinomial](https://docs.pytorch.org/docs/2.7/generated/torch.multinomial.html)。

实现建议：采样、随机子空间、bootstrap、数据扰动采用不同随机流；成对条件从相同采样状态开始，保存 generator state 或可重放的逐步随机数。只记录同一 seed 不足以保证在不同 batch 排布、不同随机调用次数后仍使用相同流。若要求严格按输出步对齐，预生成每步 uniform 并用固定的逆 CDF 采样约定；不要把不同条件放进同一 multinomial batch 后声称它们共享同一随机流。C-rand/C-layer 应属于同一实验条件组，未必必须在一次张量前向中完成。

使用 `.eval()`、冻结参数、`torch.inference_mode()`；记录 dtype、attention backend、设备、库版本与确定性设置。PyTorch 明确不保证不同版本、平台及 CPU/GPU 间的完全复现。[PyTorch reproducibility](https://docs.pytorch.org/docs/2.7/notes/randomness.html)。

## 已完成的 CPU 接口验证与必要回归

本次运行的是**随机权重微型模型的代码验证**：Qwen2 和 Qwen3 各 3 层、hidden 32、intermediate 64、4 个 Q heads、2 个 KV heads、vocab 64、fp32/eager/单线程。Qwen3 显式 `head_dim=8`，否则默认维度不能代表预期的 tiny 配置；不调用 `from_pretrained`，不下载真实权重。

已通过：两种 layer 输出形状；完整前缀与缓存步进 logits 一致；在层 1 进行 post-residual 修改时，层 0/1 当前 KV 不变、层 2 改变、此前 token KV 全部保持；patched 全前缀与 cached-boundary logits 最大误差小于 `9e-8`；no-op hook logits 逐值相同；最终 hidden 与 raw residual 不同；generator 参数被拒绝；`use_cache=False` 修改传入缓存。

后续必须把上述检查迁入仓库测试，并增加：异常后的 hook 清理、跨条件缓存隔离、patch 恰好一次、token 跨界拒绝、缓存与无缓存解码对照、固定随机流不受 C-rand 构造影响、greedy 与 sampling 配置分别覆盖。采用本地构造的小词表/模板 fixture 做离线测试；可额外使用**官方 tokenizer 文件**验证真实模板，但不要让常规测试依赖网络。微型测试通过只能证明软件接口，不能支持 C1–C4、真实模型正确率或服务器性能结论。
