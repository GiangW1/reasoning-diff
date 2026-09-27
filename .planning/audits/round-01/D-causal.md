# D-causal 独立审查报告（round-01）

通道 D：模型与因果（token/前缀、thinking 模板、采样状态、hook/KV、donor、swap/ablation/rescue、C-rand/C-layer、非目标/无效输出）。

独立性声明：未阅读 round-01 其他通道报告；未修改生产代码、测试或配置；不把测试通过当作实现正确。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T00:31:20+08:00 |
| 声称冻结 hash | `532e05a8038e9862f219ab36927f7f7c0df59ef639045821a2cc801960b2b0c0`（`.planning/audits/round-01/VERSION.md`） |
| 独立复算 hash | 未能复现上述值。当前树 `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（52 文件）：rel+bytes = `954c5caccc3555e9e490701cf975dbd0fce696bd49148137ed4cdd7b136a923f`；纯拼接 = `0eaafa24217965cfc8323c1eb2e3a59124d3fe9bc4729ef05d498a9ae2c49e6e` |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏） |
| 审查对象 | 当前工作区源码，不以声称 hash 已对齐为前提 |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明；无导出、无加载器 |
| `src/reasoning_diff/models/adapters.py` | 1–29 | `MODELS`, `card`；revision / `think_ids`；无 `from_pretrained` |
| `src/reasoning_diff/models/collect.py` | 1–41 | `collect_tiny`, `intervene_tiny` |
| `src/reasoning_diff/models/features.py` | 1–28 | `select_prefix_index`, `assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–56 | `sample_next`, `decode_loop`, `apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–88 | `tiny_config`, `build_tiny`, `resid_post_hook`, `clone_cache`, `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–73 | `project_delta`, `apply_swap`, `c_rand_delta`, `inlp_remove`, `rescue`, `intervention_report` |
| `src/reasoning_diff/baselines.py` | 1–44 | `Visibility`, `text_predictor`, `attention_*`, `verbalizer` |
| `src/reasoning_diff/cli.py` | 1–239 | 重点 `cmd_collect` 122–134、`cmd_intervene` 162–179、`cmd_analyze` 188–197 |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理 |
| `tests/test_tiny_cache.py` | 1–25 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |

支持性阅读（为核对边界/评分/协议，非本通道主交付）：`events.py` `boundary_index` 74–80、`extract_answer` 83–94；`analysis.py` `p3_recovery` 49–56；`rng.py` `StreamBank` 41–53；`schema.py` `POSITION_KINDS` 39；`repair.py` 34–45；`tests/test_science.py` 42–88；`tests/test_cli_pipeline.py` 1–18；`docs/EXPERIMENT_PROTOCOL.md` §4；原文 `Reasoning-Diff-修订方案-v3 (1).md` §2.4 行 90–117、指标 190–192、Fig.3 307–313；`.planning/research/STACK.md` 54–90；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / BASE-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer 文件、50 条 C2 同批次实验。生产模块中与因果相关但本通道未逐行审计的有 `analysis.py` 其余统计、`probes/*`、`transfer.py`。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（多种拼接） | 失败，见 U-01 |
| X2 | `pytest tests/test_tiny_hooks.py tests/test_tiny_cache.py tests/test_generate_loop.py tests/test_science.py::test_boundary_excludes_straddle tests/test_science.py::test_swap_formula tests/test_cli_pipeline.py -q` | **8 passed / 10.13s**。通过只证明冒烟，不证明因果协议 |
| X3 | `apply_swap` 代数与 `test_swap_formula` | 公式 \(H'=H_b+\Pi_Z(H_d-H_b)\) 在标准正交基下正确 |
| X4 | tiny qwen2/qwen3：`resid_post` 层 1 后 KV 范围 | 层 0/1 dK=0，层 2 改变；hook `finally` 后 handle 数为 0。与 STACK resid_post 契约一致 |
| X5 | decode 期间 hook 触发次数 | `max_new=3` 时 hook **触发 3 次**（非一次性） |
| X6 | `collect_tiny("qwen2",[1,2,3],max_new=2)` 三位置 | `pre_step=pre_value=post_step=2`，`leaks_target` 均为 False |
| X7 | `inlp_remove` steps=1 vs 8 | 矩阵相同（差 \(1.58\times10^{-16}\)） |
| X8 | `c_rand_delta` 范数 vs 真实 main | main \(\|\\Delta\|=1.8669\)，C-rand=0.6617，且 **精确等于** `default_rng(1)` 伪 main |
| X9 | `python -c` 调用 `cli.main(['intervene', ...])` | 写出硬编码 `target.vs_crand=0.6`、`vs_clayer=0.55`；`timing` 仅为字符串 `"pre_step"` |
| X10 | 全 `src` 检索 `from_pretrained` / C-layer 实现 / donor 配对 | **无** HF 加载；**无** C-layer 干预函数；donor 仅为 `rng.normal` |
| X11 | thinking 模板、`think_ids`、`clone_cache`、`assert_no_future_leak`、`StreamBank` 是否接入 collect/intervene | 定义存在，**生产 CLI 与干预路径未调用** |
| X12 | 跨界 token | `boundary_index` 排除 straddling（测试通过）；`leaks_target` 仍被写死为 False |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹、无 donor 配对实现 |
| `DynamicCache.copy` 是否深拷贝无共享存储 | `clone_cache` 未被调用，未构造对抗用例 |
| 全量 pytest（39+） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. 发现

### D-01 — CLI `intervene` 写入虚构因果效应

- **状态：** confirmed defect
- **严重度：** critical
- **文件 / 符号 / 行号：** `src/reasoning_diff/cli.py` `cmd_intervene` **162–179**；指标字典 **169–172**；`_write_stage` 成功计数见 **47–54**（恒为 `success: 1, failure: 0`）
- **触发条件：** 运行生产入口 `reasoning-diff intervene --out-dir <dir>`（无模型、无轨迹、无 donor 参数）
- **对应要求：** 原文 104、117、190；CAUSAL-01/02；GOAL「不接受假返回值/固定答案」
- **复现 / 证据：** 本机写出一行 JSONL：`main_norm=1.8669`，`crand_norm=0.6617`，`report.target.vs_crand=0.6`，`vs_clayer=0.55`，`timing="pre_step"`。这些 0.8/0.2/0.25 等数是字面常量，不是生成或评分结果。`tests/test_cli_pipeline.py` **11、16** 只断言退出码 0。
- **影响：** 产物看起来像「主干预相对对照有效」，可被误当作 C2 正结果。
- **建议：** 删除硬编码指标。入口必须跑同前缀、同采样的 base/donor/main/C-rand/C-layer 生成，用预先指定的 \(g\) 打分；失败保留在分母。

### D-02 — donor 不是事件可配对样本，无来源—数值解耦

- **状态：** confirmed defect
- **严重度：** critical
- **文件 / 符号 / 行号：** `cli.py` **163–165**（`base`/`donor` = `rng.normal(size=8)`）；全库无 donor 配对、无可见前缀记录、无按数值条件重提取
- **触发条件：** 任何 `cmd_intervene` 调用
- **对应要求：** 原文 106、307；协议 §4「donor 来自事件可对齐的任务对」；CAUSAL-02
- **证据：** 向量与任务/事件/前缀无键。无同值异源 / 异值来源跟随矩阵。
- **影响：** 即使后续把向量写入 hook，也不能评价「跟随 donor 来源」。
- **建议：** 先按事件身份配对；每个数值条件独立提取 donor；记录提取层、token 位置与可见前缀。

### D-03 — C-rand 匹配的是 `default_rng(1)` 伪 main，不是实际主干预范数

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `c_rand_delta` **31–36**（尤其 **34–35**）；`cli.py` **166–177** 同时写出不相等的 `main_norm` 与 `crand_norm`
- **触发条件：** 调用 `c_rand_delta`；或跑 `cmd_intervene`
- **对应要求：** 原文 114「同等范数」；协议 §4「记录实际扰动范数并匹配，而不只共用一个系数」；CAUSAL-01
- **证据：** 独立计算 `main_norm=1.8669062123799591`，`crand_norm=0.661653371614149`，后者与 `orthonormal_basis(..., default_rng(1))` 的伪 main 范数逐位相同。
- **影响：** 对照幅度系统偏小；相对 C-rand 的差值不可解释为「同幅度对照」。
- **建议：** 传入真实 `main_delta` 的范数（及层/位置/秩/随机流）；禁止内部另造 seed=1 的「main」。

### D-04 — C-layer 干预不存在

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `intervention_report` **58–73** 只接收指标字典的 `clayer` 键；`cli.py` **172** 硬编码 `{"target": 0.25, ...}`。不存在弱层选择、不存在浅层交换。
- **触发条件：** 任何声称含 C-layer 的 intervene/analyze
- **对应要求：** 原文 115–117、309、496；IE-01；协议「C-layer 由开发集确定」
- **证据：** 源码检索无 `c_layer` / 开发集层选择 / 同幅度浅层 hook。
- **影响：** 缺少必做对照之一；相对 C-layer 的「效应」是编造的。
- **建议：** 在 `dev` 上按探测曲线选弱层；与主干预同秩、同位置、同范数、同采样流执行；写入实际层号。

### D-05 — INLP 不是迭代零空间投影，且从未作用于隐状态

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `inlp_remove` **39–51**。循环内 **H、labels 不变**，每步 `lstsq` 得到同一 \(u\)；`p \leftarrow p(I-uu^T)` 对单位 \(u\) 幂等。CLI **未调用**。无 `P @ h` 消融。
- **触发条件：** `steps>1`；或期望选择性消融 / P3 Knock-out
- **对应要求：** 原文 311；INLP-01；CAUSAL-01
- **证据：** `steps=1` 与 `steps=8` 矩阵 allclose。测试不含 `inlp_remove`。
- **影响：** 消融名不副实；P3 无真实 Knock-out。
- **建议：** 每步在已投影的 H 上重拟合；返回并应用投影；CLI 对隐状态执行；报告四项结局。

### D-06 — Rescue 只是向量相加，无错误来源 / 随机分量对照

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `rescue` **54–55**；CLI 未调用
- **触发条件：** 调用 `rescue(ablated, component)` 或宣称 Fig.3d
- **对应要求：** 原文 313「错误来源分量与随机分量作为对照」；48；CAUSAL-01
- **证据：** 函数体为 `return ablated + component`。独立运行 `rescue([1,0],[0,1]) -> [1,1]`。无错误来源、无随机救援、无恢复率。
- **影响：** 加回原分量可成恒等重建，不能单独作机制证据。
- **建议：** 同一位置比较匹配分量 / 错误来源 / 随机分量；超参在 direction_fit/dev 固定。

### D-07 — 无冻结 HF 后端；生产 collect 是合成轨迹 + 全零特征

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `adapters.py` **3–29** 仅卡片；`collect.py` 模块注释 **1**、`collect_tiny` **11–19**（`weight_source="random_init"`）；`cli.py` `cmd_collect` **122–134**（`text = "q = 0\n"`，`features.npz` 为 `dummy` 零向量）。全库无 `from_pretrained`。
- **触发条件：** `reasoning-diff collect`；或期望 MODEL-01 隐状态采集
- **对应要求：** MODEL-01；STACK「配置与词表同一 revision、AutoTokenizer」；GOAL「真实后端必须有实质实现」
- **证据：** collect 不调用 `collect_tiny` / `decode_loop` / tokenizer。`_synthetic_trace`（`cli.py` **27–44**）用「一字一 token」偏移。
- **影响：** 无法采集三位置隐状态，也无法做前瞻干预。卡片 revision 未接入加载路径。
- **建议：** 实现 `from_pretrained(id, revision=card["revision"])`；即使本机不下载，加载/hook/decode 路径也必须存在并可用 tiny 或本地 fixture 走通。

### D-08 — 三位置坍缩；`leaks_target` 恒为 False

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `features.py` `select_prefix_index` **8–23**（**13、19** 写死 `leaks_target: False`）；`collect.py` **16–18** 用同一 `target=len(prompt_ids)` 计算三个 kind；`events.py` `boundary_index` **74–80** 的 `position` **只做枚举校验，不改变 limit**；`assert_no_future_leak` **26–28** 未被调用
- **触发条件：** `collect_tiny`；或对同一 `target_char` 请求 `pre_value`/`post_step`
- **对应要求：** 原文 108–110；POS-01；协议「跨界 token 不得泄漏目标内容」
- **证据：** 本机 `collect_tiny`：`token_index` 三者皆为 2。`test_tiny_cache.py` **21** 只断言 `leaks_target is False`，无法抓住硬编码。`test_science.py` **42–46** 只覆盖 straddling 排除，不覆盖三位置区分。
- **影响：** 步前 / 数值前 / 步尾无法分开；泄漏标志不可信。
- **建议：** 分别传入 `event.start` / `value_start` / `event.end`；由偏移计算 `leaks_target`；`boundary_index` 按 kind 改变边界；强制调用 `assert_no_future_leak`。

### D-09 — hook 无位置门控、非一次性；干预打在整段序列上

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `tiny.py` `resid_post_hook` **54–72**（`transform(tensor)` 作用于整个 hidden）；`collect.py` `intervene_tiny` **30–34**（`return t + 0.01`，全位置）；未与 `decode_loop` 组合
- **触发条件：** 在 decode 循环外层保持 hook；或 `intervene_tiny`
- **对应要求：** 原文 106、108（选定位置、目标首 token 之前、此前 KV 保持 base）；STACK 70–71「hook 必须一次生效，后续 decode 不得重复施加」
- **证据：** `decode_loop(..., max_new=3)` 期间 hook 触发 3 次。首次前向会对 **全部 prompt 位置** +0.01。`intervene_tiny` 的 `cache_isolated`（**38**）只比较两次独立前向的对象身份。
- **影响：** 不是「步前单点交换」，而是整段 residual 平移；后续 token 被重复干预。
- **建议：** 按全局 token 位置门控；只在边界步生效一次；记录 hook 名、层号、位置、更新的 KV 范围；后续 decode 卸 hook。

### D-10 — thinking 模板未接入；无 think 跨度；答案可能读到思考区数字

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` `apply_model_template` **51–56**（未被 CLI/collect 调用）；`adapters.py` **10、18** `think_ids` 未使用；`events.py` `extract_answer` **83–94** 在全文找 `\\boxed` / `####` / 最后数字，不剥离 thinking
- **触发条件：** Qwen3 `enable_thinking` 或 R1 提示已含 `<think>`；思考区出现数字
- **对应要求：** MODEL-01；STACK 56–60（Qwen3 不预插 `<think>`；R1 opening tag 属于提示；须区分 prompt/generated）
- **证据：** 模板函数不返回 `prompt_len` / think span。`model_kind=="qwen3"` 才传 `enable_thinking`（对 R1/qwen2 是对的方向）但无调用方。测试无 `apply_model_template`。
- **影响：** 前瞻边界可能落在模板或思考标记上；无效/错误答案与思考区数字混淆。
- **建议：** 用卡片 revision 的 tokenizer 走 `apply_chat_template`；保存 prompt 长度、think 开闭 ID、原始生成 IDs；评分前限制在闭合 think 之后（无闭合则标 invalid）。

### D-11 — 采样状态未在条件间共享或落盘

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` `decode_loop` **28–48** 不接收/不记录 temperature、top_k、top_p，默认 temp=1 满核采样；`sample_next` **8–25** 有实现但 decode 不传；`cli.py` collect/intervene **不调用** `decode_loop`；`rng.py` `StreamBank`（sample/direction 分离）未被 intervene 使用（intervene 用 `default_rng(0)`，**163**）
- **触发条件：** 需要「所有处理条件同一采样配置和随机流」（原文 106）
- **对应要求：** 原文 106；STACK 76–80
- **证据：** 输出无 generator state / 逐步 uniform。成对条件无法从同一采样快照分叉。
- **建议：** 显式记录并复用采样配置与 generator/预抽样；方向流与采样流隔离；C-rand 构造不得消耗采样流。

### D-12 — 缓存隔离未实现为可用契约

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `tiny.py` `clone_cache` **75–81**（无 `copy` 时 **返回原对象**）；定义未被引用。`collect.py` **26–38** 只断言 `cache_a is not patched.past_key_values`。`test_tiny_cache.py` **7–15** 记录 `use_cache=False` 仍写入传入 cache（与 STACK 73 一致），但生产 `decode_loop` 始终 `use_cache=True`（`generate.py` **36**），没有分支克隆。
- **对应要求：** 原文 106「此前位置 KV 保持 base」；STACK 72–73
- **影响：** 多条件若复用同一 cache，存在静默污染；隔离测试过弱。
- **建议：** 每条件重新 prefill，或验证深拷贝无共享存储；禁止在 `use_cache=False` 时传入需保留的 cache。

### D-13 — 非目标 / 无效输出不是测出来的；P3 接口缺非目标

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **169–172、192**；`analysis.py` `p3_recovery` **49–56**（只有 `invalid_rate`，无 nontarget）；`scoring.py` 无干预无效类
- **触发条件：** `intervene` / `analyze`
- **对应要求：** 原文 117、166、190、192（四项必须同时报告；P3 须查非目标与无效，排除「损伤模型涨分」）
- **证据：** `p3_recovery(0.55, 0.54, 0.53, 0.1)` 为字面量。`intervention_report` 结构正确，输入是假的。
- **影响：** 无法排除平凡损伤；Week-8/P3 数字无测量含义。
- **建议：** 由生成文本计算目标/非目标/任务正确/无效/截断；P3 签名加入 nontarget，缺测为 null 而非 0。

### D-14 — 基线未强制公平前瞻前缀

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `baselines.py` `Visibility` **10–13** 未被 `text_predictor` **16–19** 使用；`verbalizer` **36–44** 用 `gold[:4] in prefix` 的子串启发，反思档只改标签为 retrospective
- **对应要求：** BASE-01 / VERB-01「按可见前缀区分前瞻与回顾」；GOAL 第 7 条
- **影响：** 回顾文本可被当成前瞻基线。
- **建议：** 所有基线接收与探针相同的前瞻前缀对象；拒绝带目标步内容的输入。

## 6. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | 声称冻结 hash 与本机多种复算不一致。VERSION 写明 generate/cache「后加」 | 无法区分算法不同与树漂移 |
| U-02 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致，但本审查未读官方 tokenizer JSON | 禁止下载 |
| U-03 | `DynamicCache.copy` 是否切断存储 | `clone_cache` 未走生产路径 |
| U-04 | hook 若传入原地 `transform` 可能破坏共享读数 | 现有调用是 `t+0.01` 非原地；STACK 要求克隆 |

## 7. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision 一致性 | 卡片 revision 与 tiny 架构 | 无权重/tokenizer 文件，且无加载器 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post 范围符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 仅有向量公式与假 CLI | 无真实轨迹与 donor |

## 8. 非缺陷说明与建议

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta`（`interventions.py` **9–16**）在标准正交基下正确；`test_swap_formula` 通过 |
| N-02 | 非缺陷 | tiny qwen2/qwen3 上 resid_post(层1) 不改层 0/1 当前 KV、改层 2；`finally` 清理有效 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`（`adapters.py` **27–28**） |
| N-04 | 非缺陷 | `enable_thinking` 仅在 `model_kind=="qwen3"` 传入，与 STACK 对 R1 的说明同向（但函数未被调用，见 D-10） |
| N-05 | 建议 | `scale_to_norm` 标注返回 `ndarray`，实际返回 `(delta, status)`（**24–28**）。建议在 `apply_swap` 断言基列正交 |

## 9. 通道结论

**D 通道不通过。**

已确认缺陷覆盖：虚构干预指标（D-01）、donor 协议缺失（D-02）、C-rand 范数错误（D-03）、C-layer 未实现（D-04）、INLP/救援名不副实（D-05/D-06）、无真实模型采集（D-07）、三位置/泄漏标记失效（D-08）、hook 非单点/非一次性（D-09）、thinking/采样/KV 隔离未接通（D-10–D-12）、非目标与无效输出未测量（D-13）。

Tiny 测试 8 通过、swap 公式正确、resid_post KV 范围在微型模型上符合 STACK，**不足以**支持 CAUSAL-01/02 或 C2。`cmd_intervene` / `cmd_analyze` 当前产物不能当作科学效应。
