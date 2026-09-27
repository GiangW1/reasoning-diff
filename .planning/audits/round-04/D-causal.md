# D-causal 独立审查报告（round-04）

通道 D：模型与因果（三位置/前瞻泄漏/跨界、thinking 模板与原始 token ids、offline vs online 边界、resid_post last-token vs 全序列、hook 一次性选项、KV/`clone_cache` 元数据与 `seq_length`、swap \(H'=H_{\mathrm{base}}+\Pi_Z(H_{\mathrm{donor}}-H_{\mathrm{base}})\)、INLP/rescue、C-rand/C-layer 弱层 vs 随机子空间、救援对照、CLI intervene/analyze 不得虚构正确率、collect `H` 是隐状态还是前缀 id、隔离执行器无宿主 exec）。

独立性声明：未阅读 round-04 其他通道报告；只把 `.planning/audits/round-04/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账；对照阅读了本通道 round-01 / round-02 / round-03 报告以便核对关闭项，结论以本机当前磁盘为准。未修改生产代码、测试或 `pyproject.toml`；不把测试通过当作实现正确；不把作者 `fixed_pending_review` 或 97 passed 当作本通道关闭。微型随机权重不是 MODEL-01 完成（真实 HF 为 `pending_server`）。诚实的 `offline_prefix_ids` 在未被宣称为隐状态时不记为缺陷。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T01:40:00+08:00 |
| 声称冻结 hash | `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`（`.planning/audits/round-04/VERSION.md`；56 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **复现。** 按 VERSION 脚本：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → 56 文件 → `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17` |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；审查对象是冻结脚本覆盖的 56 个文件字节） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| 作者 pytest 声称 | 97 passed。本通道只重跑所引用子集，不把 97 记为已验证 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / `think_ids` / `load_frozen(..., local_files_only=True)` |
| `src/reasoning_diff/models/collect.py` | 1–60 | `collect_tiny` 取 `hidden_states[-1]`；`intervene_tiny(..., once=True)` |
| `src/reasoning_diff/models/features.py` | 1–40 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–57 | `sample_next`；`decode_loop`；`apply_model_template` 返回 `prompt_len` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` 拷贝 metadata / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand / C-layer / INLP / `rescue_controls` / `select_weak_layer` / `ie_z` / `intervention_report` |
| `src/reasoning_diff/cli.py` | 1–658 | 重点 `cmd_collect` 288–349、`cmd_fit` 375–414、`cmd_intervene` 445–504、`cmd_analyze` 525–584 |
| `src/reasoning_diff/executor.py` | 1–99 | `IsolatedExecutor` 返回 unavailable；`SubprocessExecutor`；`get_executor` 默认 Unavailable |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理（未断言 last-token-only、未断言 `once`） |
| `tests/test_tiny_cache.py` | 1–26 | `use_cache=False` 污染；tiny collect/intervene 冒烟；**不调用** `clone_cache` |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |

支持性阅读：`events.py` `boundary_index` 131–137、`extract_answer` 140–154；`analysis.py` `p3_recovery` 140–156；`rng.py` `StreamBank` 41–53；`schema.py` `POSITION_KINDS` 39；`scoring.py` `score_code` 19–30；`tests/test_science.py` 42–88；`tests/test_review_regressions.py` 238–274、287–294；`tests/test_round03_regressions.py` 100–103、167–187；`tests/test_cli_pipeline.py` 1–29；`tests/test_t3_t4.py` 29–39；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/research/STACK.md` 54–90；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条 C2 同批次。未逐行审计：`analysis.py` 其余统计、`probes/bilinear.py`、`transfer.py`。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | **匹配** `fb1e3dfa…0c66d17`；56 文件 |
| X2 | `pytest tests/test_tiny_hooks.py tests/test_tiny_cache.py tests/test_generate_loop.py tests/test_science.py::test_boundary_excludes_straddle tests/test_science.py::test_swap_formula tests/test_review_regressions.py::test_c03_inlp_iterates_on_projected_h tests/test_review_regressions.py::test_c04_crand_matches_provided_main_norm_not_rng1 tests/test_review_regressions.py::test_d01_three_positions_differ_and_leak_flag_is_real tests/test_review_regressions.py::test_e04_analyze_manifest_includes_report tests/test_cli_pipeline.py tests/test_t3_t4.py::test_humaneval_never_host_exec tests/test_round03_regressions.py::test_extract_answer_ignores_open_think tests/test_round03_regressions.py::test_subprocess_executor_timeout_and_ok tests/test_round03_regressions.py::test_ie_z_and_rescue_controls tests/test_round03_regressions.py::test_p3_reports_nontarget -q` | **17 passed / 10.58s**。通过只证明冒烟，不证明因果协议 |
| X3 | `apply_swap` 与 `test_swap_formula` | \(H'=H_b+\Pi_Z(H_d-H_b)\) 在标准正交基下正确：`[1,0]+Π([0,1]-[1,0])=[1,1]` |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.228\)、\(\Delta V_{\max}=0.305\)，且 **仅 last token**（earlyK=0）。与 STACK resid_post 契约一致 |
| X5 | 仅 last-token vs 全序列 | `transform` 形状 `(1, 1, 32)`。层 1 early \(\Delta=0\)、last \(\Delta=1\)；层 2 仅 last 变（\(\Delta_{\max}\approx 1.008\)） |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3 次**；`once=True` **1 次** |
| X7 | hook `finally` 清理 | `RuntimeError` 后 `layer._forward_hooks` 为 0 |
| X8 | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_prefix` 形状 `(32,)`；`hidden_all` `(3,32)`（只对 **prompt** 再前向）；`hidden_layer=-1`；三位置 token_index **2/3/4**（limit 3/4/5）；`leaks_target` 皆 False；`boundary_source=offline_annotation` |
| X9 | `leaks_target` 能否为 True | 单 token `[[0,10]]` limit=3 → `leaks_target=True`、`token_index=None`。5 组 offsets × 10 limit × 3 kind = 150 次中 **72 True / 78 False**（51 次 `token_index is None`）。1:1 整数边界永假 |
| X10 | `boundary_index(..., 5)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 2；`position` 只做枚举校验，算法不随 kind 变 |
| X11 | INLP / rescue | steps=1 vs 8 最大差 **0.8**。`H@P` 第一列≈0。`rescue([1,0],[0,1])=[1,1]`。`rescue_controls` 给出 matched / error_source / random，随机分量范数匹配 |
| X12 | C-rand / C-layer 范数与弱层选择 | `actual_norm` 与 main 逐位匹配（2.723…）。缺范数仍 `ValueError`。`select_weak_layer({0:0.2,1:0.1,2:0.4})=1`（与 CLI 硬编码表相同） |
| X13 | CLI collect / intervene / analyze | 见 X14。tiny→intervene：三项范数皆 **1.9785**，四项结局 **null**，`status=geometry_on_hidden`，`clayer_status=dev_weak_layer`，`timing=pre_step`，`relative.weak_layer=1`，`relative.hook_once="resid_post"`（字符串，不是布尔）。offline→intervene 与无 `--in-dir`：`donor_missing` / `unexpressible` / 范数 null。analyze：`p1/p2/p3=null`，`scientific_conclusion=null`，`not_evaluated`。产物字符串 **不含** 0.6/0.55/0.8/0.2/0.25 |
| X14 | CLI collect 三位置 + NPZ | 文本 `"p1 = 4\np2 = 0\nq = 0\n"`；唯一事件 `q start=14,value_start=18,end=19`。三位置 token_index **13/17/18**，皆 `expressible=true`。`--backend tiny`：`H` 形状 `(2,32)` 有限浮点、两行不全等（\(\|\Delta\|\approx 8.43\)），`weight_source=random_init`，无 `token_prefix`。`--backend offline`：`H` 形状 `(1,8)=[1..8]`，`weight_source=offline_prefix_ids`。`--eval-mode scientific --backend offline` → `ValueError: scientific collect refuses offline_prefix_ids as H` |
| X15 | thinking / 模板 / 调用图 | `decode_loop` 保存 `prompt_ids`/`generated_ids`/`token_ids`。`apply_model_template` 对 qwen3 传入 `enable_thinking` 并返回 `prompt_len`；对 qwen2 不传该 kw。CLI **不调用** `apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak` / `StreamBank` / `inlp_remove` / `rescue_controls` / `ie_z`。`from_pretrained` 仅在 `load_frozen` |
| X16 | `clone_cache` / DynamicCache | 本机 `DynamicCache` **无 `.copy()`**。clone ≠ 原对象；`data_ptr` 不同；对 clone `add_` 后原张量不变。clone **`get_seq_length()=5`**（与原相同）、`is_initialized=True`、层 `dtype=float32` / `device=cpu`。下一步 decode 长度 6；clone-step vs 全前缀 last-logit \(\Delta_{\max}=4.47\times 10^{-8}\)。测试目录 **零引用** `clone_cache`；生产路径不调用 |
| X17 | `extract_answer` 与 thinking | `"<think>the number is 99</think>"` → **None**；未闭合 think → **None**；`</think>` 后 `#### 7` / `\boxed{7}` → **7**；无 think 的 `42` → 42 |
| X18 | 执行器 | 默认 `UnavailableExecutor`；基类 `submit` 返回 `executor_unavailable`（不再 `NotImplementedError`）；`score_code` → `value=None` / `host exec is forbidden`。`SubprocessExecutor` 是子进程，拒绝源中的 `exec(`/`eval(`。全库生产路径无宿主 `exec`/`eval` 回退 |
| X19 | collect `H` 作 donor | tiny：两行不同随机初始化模型的 `hidden_prefix` → 非零几何。offline：仅 1 行 → `donor_missing`。两行不是事件配对、不是来源—数值解耦、权重未设种子 |
| X20 | final hidden vs resid_post | 同一次前向：`hidden_states[-1]` 与末层 hook 输出 \(\Delta_{\max}=2.188\)，**不相等**。collect 写最终归一化隐状态；intervene hook 打在 resid_post |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存。属 `pending_server` |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹、无事件可对齐 donor 实现 |
| 全量 pytest（作者称 97） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| D-08 straddling `leaks_target` | 本地关闭 | **关闭。** `leaks_target=bool(straddling)`；`test_d01` 与 X9 可为 True。跨界 token 仍不进入 `token_index` |
| D-10 clone metadata | 本地关闭 | **功能关闭。** `seq_length` / `is_initialized` / dtype / device 正确；步进对拍成立（X16）。生产未调用、测试未覆盖，列为残留 stub 而非功能缺陷 |
| D-07 one-shot hook option | 本地关闭 | **选项关闭。** `once=True` 在 decode 中只触发 1 次（X6）。生产 intervene 仍是一次 prefill 的 `t+0.01`，不是边界步一次后卸 hook（D4-04） |
| collect prefix-id features | 本地关闭 | **按用户口径关闭。** `--backend offline` 写 `offline_prefix_ids` 且 scientific 拒绝把它当 `H`。默认 `--backend tiny` 写 `random_init` 隐状态。二者都未声称官方 HF 隐状态 |
| pending_server | 真实权重 / 隔离 Linux 执行器 / 实测 P1–P3 | **同意未关。** 微型随机权重不是 MODEL-01 完成；`load_frozen` 未跑通；无四项实测结局 |

相对 r03 已关闭、本轮不再单列缺陷：虚构 intervene/analyze 正确率；C-rand 范数匹配；INLP 迭代投影算法；resid_post last-token 与 hook 清理；CLI 首事件 `pre_step` 不可表达（默认 fixture 的 `q` 现可表达）。

## 6. 发现

### D4-01 — 声称冻结 hash 已复现（本轮非缺陷）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `.planning/audits/round-04/VERSION.md` 声称与本机 56 文件 rel+NUL+bytes 一致
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。
- **影响：** 审查对象可锚定到声称快照。不因此放行科学实现。

### D4-02 — C-layer 仍是同向量上的随机子空间，却被标成 `dev_weak_layer`

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **465–468、497**（硬编码 `layer_scores={0:0.2,1:0.1,2:0.4}` + `orthonormal_basis(..., default_rng(5+weak))` + `clayer_status="dev_weak_layer"`）；`interventions.py` `c_layer_delta` **46–49**、`select_weak_layer` **92–95**（选最小分数，本身正确）
- **触发条件：** 任何默认 tiny collect 之后的 `reasoning-diff intervene`
- **对应要求：** 协议 §4「C-layer 为开发集证实依赖信息较弱的层」；IE-01
- **证据：** X12、X13。弱层选择器在真实 dev 曲线上会返回 argmin，但 CLI 分数是字面常量，不是探针 dev 曲线。`c_layer_delta` 与 C-rand 一样对同一 `base`/`donor` 做 \(\Pi\) 再 `scale_to_norm`；差别只是 QR 种子变成 `5+weak`。三项范数完全相同（1.9785）。`intervene_tiny` 虽把 hook 打在 layer 1，变换是 `t+0.01`，不用该层表示、也不用 C-layer \(\Delta\)。相对 r03 的诚实标签 `placeholder_subspace_not_dev_layer`，本轮标签更自信、实现仍不是层对照。
- **影响：** 「相对 C-layer」只是第二种随机投影。同队列只做到「同一对 numpy 向量 + 同一范数」，不是同批次、同位置、弱层隐状态。
- **建议：** 在 `dev` 上按探测曲线选层；C-layer 的 \(H\) 必须来自该层；与主干预同秩、同位置、同范数、同采样流；写入实际层号。未做到时不要写 `dev_weak_layer`。

### D4-03 — 三位置索引可分离，但写入的 `H` 不是这三个位置的隐状态

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **299–322**（字符偏移三位置写入 metadata；`H` 取 `token_ids[:8]` 上两次 `hidden_prefix`）；`collect.py` **16–37**（三位置算在含生成 token 的 offsets 上，隐状态却只对 **prompt** 再前向，且只保存 `prefix_index=target-1`）；`tiny.py` 不参与按事件取层
- **触发条件：** `reasoning-diff collect`（tiny 或 offline）；或期望 POS-01 三位置采集
- **对应要求：** POS-01；MODEL-01 的三边界（本机 tiny 接口可测，不要求真实 HF）
- **证据：** X8、X14、X20。默认 fixture 事件 `q` 的三位置 13/17/18 且可表达（r03 D-11 已关）。tiny `H` 是截断 8 个字 token 的**最后一枚**最终 RMSNorm 向量（`hidden_layer=-1`），不是 token 13/17/18，也不是 resid_post。`collect_tiny` 自己的 post_step 可为生成 token（index 4），但 `hidden_all` 只有 3 行 prompt。CLI 丢弃 `collect_tiny["features"]`，另存字符偏移 feat。offline `H=[1..8]` 是前缀 id，已诚实标注，不另作缺陷。
- **影响：** 元数据看起来做了三位置；下游 fit/intervene 吃到的是单一位置（或前缀 id）的一行/两行向量。步前/值前/步尾无法被比较。
- **建议：** 在同一轨迹、同一层定义上按三个 `token_index` 取出 last-safe 表示并分键保存；tiny 路径用 resid_post 或明确记录与 hook 同一位置。

### D4-04 — 生产干预是几何范数 + 一次 `+0.01` hook，不是交换/消融/救援；四项结局仍空

- **状态：** confirmed defect（接线） / residual（诚实 null）
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **459–483、489–495**（`apply_swap` 只算范数；`intervene_tiny` 的 transform 为 `t+0.01`；`report["hook_once"]=hooked["hook"]` 即字符串 `"resid_post"`）；`collect.py` **49–52**；`interventions.py` `inlp_remove` **52–67**、`rescue_controls` **74–85** 均无 CLI 调用
- **触发条件：** 期望选定位置交换、INLP、救援或四项结局
- **对应要求：** CAUSAL-01；INLP-01；协议 §4
- **证据：** X6、X11、X13。`once=True` 选项本身有效，但 `intervene_tiny` 只有一次 prefill，随后不 decode、不卸-后再生成。swap \(\Delta\) 从未写入 hook。INLP / rescue / `ie_z` 有算法与单测，生产路径不执行。四项为 null，`intervention_report` 的相对项全 None。诚实空结果优于虚构，仍不是机制实验。
- **影响：** 不能评价「跟随 donor」「选择性消融」或救援对照。`hook_once` 字段名也不表示一次性已验证。
- **建议：** 在边界步把 \(H'\) 写入 resid_post 一次后卸 hook；同一位置跑 INLP 与 `rescue_controls`；由生成文本算四项。

### D4-05 — donor 是两次未设种子的随机初始化模型，不是事件可配对样本

- **状态：** residual / pending_server
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **316–319**；`collect.py` **12**（`build_tiny` 不设权重种子；`seed` 只给 decode generator）；全库无来源—数值解耦配对
- **触发条件：** 把 tiny collect 的两行 `H` 当作 C2 donor
- **对应要求：** 协议 §4；CAUSAL-02
- **证据：** X14、X19。两行不全等（\(\|\Delta\|\approx 8.43\)），故几何不再塌成 0（相对 r03 的单行前缀 id 是进步）。它们是两个独立随机 Qwen2-tiny 对同一 8-id 前缀的最终隐状态，不是同一模型、同一事件、不同来源条件。状态 `geometry_on_hidden` 部分诚实。无 collect 时不再用高斯伪造 donor（`donor_missing`）。
- **影响：** 本机可演示非零 \(\|\Delta\|\)，不能评价来源跟随。真实 50 条队列保持 `pending_server`。
- **建议：** 先按事件身份配对；每个数值条件独立提取；记录层、token、可见前缀与模型种子。

### D4-06 — thinking 抽取已修；模板 / `think_ids` / `load_frozen` 仍未接入

- **状态：** residual defect（模板路径） / closed（`extract_answer`）
- **严重度：** medium（模板）
- **文件 / 符号 / 行号：** `events.py` `extract_answer` **140–154**（去 think，未闭合返回 None）；`generate.py` `apply_model_template` **51–57**；`adapters.py` **10、18、32–42** `think_ids` / `load_frozen`；CLI 无调用方
- **触发条件：** Qwen3 `enable_thinking` 或 R1 提示已含 `<think>`；或声称 MODEL-01 模板对齐
- **对应要求：** MODEL-01；STACK 56–60
- **证据：** X15、X17。思考区内数字不再当答案。`prompt_len` 已返回但仍无生产调用。`think_ids` 未用于切 span。真实 HF 加载属 `pending_server`，不因 tiny 随机权重记 MODEL-01 完成。
- **影响：** 本机评分不再被未闭合/思考区数字误导。前瞻边界仍可能落在未应用的模板标记上（一旦接真实 tokenizer）。
- **建议：** 卡片 revision 走 `apply_chat_template`；保存 prompt 长度、think 开闭 ID、原始生成 IDs；评分限制在闭合 think 之后。

### D4-07 — 采样配置与 StreamBank 未在条件间共享

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` `decode_loop` **38** 不传 temperature/top_k/top_p（默认 temp=1 满核）；`cli.py` intervene 用 `default_rng(0/3/5)`，不用 `StreamBank`
- **触发条件：** 「所有处理条件同一采样流」（协议 / STACK 76–80）
- **证据：** 无 generator state / 逐步 uniform 落盘。当前也无真实条件采样；C-rand 构造流与采样流未隔离。
- **建议：** 记录并复用采样配置与 generator；方向流与采样流隔离。

### D4-08 — `IsolatedExecutor.submit` 默认不跑代码；默认路径无宿主 exec（默认路径非缺陷）

- **状态：** stub / 默认路径 non-defect
- **严重度：** medium（真实隔离未到）/ 信息（host exec）
- **文件 / 符号 / 行号：** `executor.py` **27–29** 基类返回 unavailable；**87–92** `get_executor()` → Unavailable；**55–84** 可选 `SubprocessExecutor`（子进程，非宿主 exec）；`scoring.py` **19–30**；`t3_humaneval.py` **61–62**
- **对应要求：** EXEC-01；OPS-01
- **证据：** X18；`test_humaneval_never_host_exec` 通过。`forbid_host_exec` 仍无生产引用。Linux cgroup 执行器保持 `pending_server`。
- **影响：** 代码题默认无法真实评分。未发现 host exec 回退。
- **建议：** 保持默认 Unavailable；真实隔离后端标 pending_server。不要把本机 subprocess 写成已验收沙箱。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载，未读官方 tokenizer JSON |
| U-02 | `transform` 若原地修改 `tensor[:, -1:]` | hook 先 clone 再写入 patched，但 transform 吃的是**原**切片。现有调用是 `t+0.01` / `t+1` 非原地 |
| U-03 | `cmd_fit` 不读 `weight_source` | offline 前缀 id 可被当成双线性 `H`。标签诚实；消费者忽略标签更偏探针通道，不单列新 D 项 |
| U-04 | `boundary_index` 的 `position` 不改变算法 | 三位置分离靠调用方传入不同 limit（X8/X14），不是 kind 语义。已由 POS-01 覆盖 |
| U-05 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够关闭 D-10；未读完 transformers 每一分支 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是** MODEL-01 完成 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 向量公式与 `geometry_on_hidden` CLI | 无真实轨迹与事件 donor |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta` 在标准正交基下正确；`test_swap_formula` 通过 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、只改层 2 last-token、此前 token 保持；`finally` 含异常路径清理有效 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`；`enable_thinking` 仅在 `model_kind=="qwen3"` 传入 |
| N-04 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `token_ids` / `stop_reason` |
| N-05 | 关闭 | CLI `intervene`/`analyze` **不再写入** 0.8/0.2/0.25 或 `vs_crand=0.6`。本机 numeric outcomes 为空 |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数 |
| N-07 | 关闭 | 三位置在传入不同 limit 时可分离；跨界 token 不进入 `token_index`；`leaks_target` 在存在 straddling 时可为 True（D-08） |
| N-08 | 关闭 | `extract_answer` 去掉闭合 think；未闭合 think 返回 None；思考区数字不再当答案 |
| N-09 | 关闭（选项） | `resid_post_hook(..., once=True)` 在 decode 中只生效一次（D-07） |
| N-10 | 关闭（功能） | `clone_cache` 隔离存储并保留 `seq_length`/`is_initialized`/dtype/device；步进 ≡ 全前缀（D-10） |
| N-11 | 关闭（过程） | 冻结 hash 按 VERSION 脚本复现 |
| N-12 | 非缺陷 | `--backend offline` 的 `H` 是前缀 id 且标注 `offline_prefix_ids`；scientific 拒绝把它当隐状态。按审查口径不记缺陷 |
| N-13 | 非缺陷（边界） | 默认 tiny `H` 是随机初始化隐状态并标注 `random_init`。这是本机接口证明，不是 MODEL-01 完成 |
| N-14 | 非缺陷 | 默认代码评分走隔离执行器且不 host exec；基类不再 `NotImplementedError` |
| N-15 | 部分关闭 | 默认 fixture 的 `q` 三位置可表达；intervene 仍硬写 `timing=pre_step`（见 D4-03） |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene；测试零引用 |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` / `forbid_host_exec` 无生产调用方 |
| S-03 | stub | `rescue_controls` / `inlp_remove` / `ie_z` 有函数与单测，CLI 不调用 |
| S-04 | stub | `features.npz` 的 `E` 是 `hidden_all.mean` 复制到前提行，不是前提嵌入 |
| S-05 | stub | Linux cgroup 执行器未到；本机 `SubprocessExecutor` 仅为子进程后端 |

## 10. 通道结论

**D 通道不通过。**

相对 round-03，本轮有可复核的接口关闭，且 freeze hash 已对齐：（1）`leaks_target` 在跨界时可为 True；（2）`clone_cache` 的 `seq_length`/初始化元数据正确，步进 logits 与全前缀一致；（3）`resid_post_hook(once=True)` 在 decode 中只触发一次；（4）`extract_answer` 不再把思考区数字当答案；（5）默认 collect 写 `random_init` 隐状态，offline 前缀 id 保持诚实标签，scientific 拒绝后者冒充 `H`；（6）CLI 仍不虚构正确率；默认执行器不宿主 exec。微型随机权重按口径不算 MODEL-01 完成。

这些不够支持 CAUSAL-01 或 POS-01 的本机协议。C-layer 仍是带硬编码分数的随机子空间，却写 `dev_weak_layer`。三位置只存在于 metadata，写入的 `H` 是截断前缀最后一枚最终 hidden，不是三个事件 token，也不是 resid_post。intervene 把 swap 停在范数上，hook 只做 `+0.01`，INLP/救援未接到生成，四项结局为 null。donor 是两次未设种子的随机模型。thinking 模板与 `load_frozen` 未接入。诚实的几何演示仍不是因果实验。
