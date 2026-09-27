# D-causal 独立审查报告（round-03）

通道 D：模型与因果（三位置/前瞻泄漏/跨界、thinking 模板与原始 token ids、offline vs online 边界、resid_post last-token vs 全序列、hook 清理、KV/`clone_cache`、swap \(H'=H_{\mathrm{base}}+\Pi_Z(H_{\mathrm{donor}}-H_{\mathrm{base}})\)、INLP/rescue、C-rand/C-layer 同队列与实际范数、CLI intervene/analyze 不得虚构正确率、collect 特征诚实、隔离执行器）。

独立性声明：未阅读 round-03 其他通道报告；只把 `.planning/audits/round-03/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账；对照阅读了本通道 round-01 / round-02 报告以便核对关闭项，结论以本机当前磁盘为准。未修改生产代码、测试或配置；不把测试通过当作实现正确；不把作者 `fixed_pending_review` /「collect prefix-id features」本地关闭当作本通道关闭。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T01:20:00+08:00 |
| 声称冻结 hash | `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`（`.planning/audits/round-03/VERSION.md`；55 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **复现。** 按 VERSION 脚本：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → 55 文件 → `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e` |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；`src/` `tests/` `pyproject.toml` 均未跟踪） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| 作者 pytest 声称 | 70 passed。本通道只重跑所引用子集，不把 70 记为已验证 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明；无导出、无加载器 |
| `src/reasoning_diff/models/adapters.py` | 1–29 | `MODELS`, `card`；revision / `think_ids`；无 `from_pretrained` |
| `src/reasoning_diff/models/collect.py` | 1–47 | `collect_tiny`, `intervene_tiny`；不算 resid、不调用 `clone_cache` |
| `src/reasoning_diff/models/features.py` | 1–43 | `select_prefix_index`, `assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–56 | `sample_next`, `decode_loop`, `apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–104 | `tiny_config`, `build_tiny`, `resid_post_hook`, `clone_cache`, `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–91 | `project_delta`, `apply_swap`, `c_rand_delta`, `c_layer_delta`, `inlp_remove`, `rescue`, `intervention_report` |
| `src/reasoning_diff/cli.py` | 1–511 | 重点 `cmd_collect` 248–289、`cmd_fit` 327–357、`cmd_intervene` 379–419、`cmd_analyze` 439–463 |
| `src/reasoning_diff/executor.py` | 1–59 | `IsolatedExecutor` stub、`UnavailableExecutor`、`SpyExecutor`、`forbid_host_exec` |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理（未断言 last-token-only、未断言一次性） |
| `tests/test_tiny_cache.py` | 1–25 | `use_cache=False` 污染；tiny collect/intervene 冒烟；**不调用** `clone_cache` |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |

支持性阅读（边界/评分/协议，非本通道主交付）：`events.py` `boundary_index` 122–128、`extract_answer` 131–142；`analysis.py` `p3_recovery` 99–106；`rng.py` `StreamBank` 41–53；`schema.py` `POSITION_KINDS` 39；`scoring.py` `score_code` 19–30；`repair.py` 34–45；`baselines.py` 10–44；`probes/boundary.py` 7–23；`tests/test_science.py` 42–88；`tests/test_review_regressions.py` 233–268、351–371；`tests/test_cli_pipeline.py` 1–29；`tests/test_t3_t4.py` 29–35；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/research/STACK.md` 54–90；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条 C2 同批次。未逐行审计：`analysis.py` 其余统计、`probes/bilinear.py`、`transfer.py`。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | **匹配** `67bb9c90…d5756e`；55 文件 |
| X2 | `pytest tests/test_tiny_hooks.py tests/test_tiny_cache.py tests/test_generate_loop.py tests/test_science.py::test_boundary_excludes_straddle tests/test_science.py::test_swap_formula tests/test_review_regressions.py::test_c03_inlp_iterates_on_projected_h tests/test_review_regressions.py::test_c04_crand_matches_provided_main_norm_not_rng1 tests/test_review_regressions.py::test_d01_three_positions_differ_and_leak_flag_is_real tests/test_cli_pipeline.py tests/test_t3_t4.py::test_humaneval_never_host_exec tests/test_review_regressions.py::test_e04_analyze_manifest_includes_report -q` | **13 passed / 9.25s**。通过只证明冒烟，不证明因果协议 |
| X3 | `apply_swap` 与 `test_swap_formula` | \(H'=H_b+\Pi_Z(H_d-H_b)\) 在标准正交基下正确：`[1,0]+Π([0,1]-[1,0])=[1,1]` |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.192\)、\(\Delta V_{\max}=0.403\)，且 **仅 last token**（earlyK=0）。与 STACK resid_post 契约一致 |
| X5 | 仅 last-token vs 全序列 | 独立捕获层输出：early \(\Delta=0\)，last \(\Delta=1\)。`transform` 收到形状 `(1, 1, 32)` |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)` 期间 hook **触发 3 次**（非一次性） |
| X7 | hook `finally` 清理 | 正常退出与 `RuntimeError` 后 `layer._forward_hooks` 均为 0 |
| X8 | `collect_tiny("qwen2",[1,2,3],max_new=2)` 三位置 | `token_index` pre/pre_value/post = **2/3/4**（limit 3/4/5）；`leaks_target` 皆 False；`boundary_source` 皆 `offline_annotation`；返回键无 resid/`H` |
| X9 | `leaks_target` 能否为 True | 5 组 offsets × 9 limit × 3 kind = **135 次，全部 False**（57 次 `token_index is None`） |
| X10 | `boundary_index(..., 3)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 1；`position` 只做枚举校验 |
| X11 | `inlp_remove` steps=1 vs 8 | 最大差 **0.8**（非幂等）。`H@P` 第一列≈0，与 `test_c03` 同向。`rescue([1,0],[0,1])=[1,1]` |
| X12 | `c_rand_delta` / `c_layer_delta` 范数 | 要求 `target_norm`；`actual_norm` 与 main 逐位匹配（2.723…）。旧 `rng(1)` 伪 main 范数 0.6617 **不再相等** |
| X13 | `cli.main(['collect'…/'intervene'…/'analyze'…])` | collect→intervene：**三项范数皆 0.0**，四项结局 **null**，`status=geometry_only`，`clayer_status=placeholder_subspace_not_dev_layer`，`timing=pre_step`。无 collect 的 intervene：三项范数 1.8669，结局仍 null。analyze：`p1/p2/p3=null`，`scientific_conclusion=null`，`not_evaluated`。产物字符串 **不含** 0.6/0.55/0.8/0.2/0.25 |
| X14 | CLI collect 三位置 + NPZ | 文本 `"q = 0\n"`；事件 `start=0,value_start=4,end=5`；`pre_step.token_index=None` / `expressible=false`；`pre_value=3`；`post_step=4`。`weight_source=offline_prefix_ids`。`H` 形状 `(1,8)` = `[1,0,0,0,0,0,0,0]`（前缀 token id，不是隐状态）；`E` 为前提文本长度对角；`token_prefix=[1.]` |
| X15 | thinking / 原始 ids / 引用检索 | `decode_loop` 保存 `prompt_ids`/`generated_ids`/`token_ids`。`apply_model_template`、`think_ids`、`clone_cache`、`assert_no_future_leak`、`StreamBank`、`collect_tiny`、`inlp_remove`、`rescue`、`intervention_report` **均未被 CLI 调用**。`from_pretrained` 仅出现在 `tiny.py` 第 1 行注释 |
| X16 | `clone_cache` / DynamicCache | 本机 `DynamicCache` **无 `.copy()`**。新实现拷贝 `layers[].keys/values`：对象不同、`data_ptr` 不同、对 clone `add_` 后原张量不变。但 clone **`get_seq_length()=0`、`is_initialized=False`**，缺 `dtype`/`device`。下一步 decode 把 cache **写成长度 1**（不是 5）；clone-step 与全前缀 last-logit \(\Delta_{\max}=0.275\)。测试目录 **零引用** `clone_cache` |
| X17 | `extract_answer` 与 thinking | `"<think>the number is 99</think>"` → **99**；有 `\\boxed{7}` 时取 7 |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`score_code` → `executor_unavailable` / `value=None`；基类 `submit` 为 `NotImplementedError`；全库生产路径无 host `exec`/`eval` 回退 |
| X19 | collect `H` 作 donor | `H` 仅 1 行 → `donor is base` → `apply_swap` 零扰动。这是 X13 范数为 0 的直接原因 |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹、无 donor 配对实现 |
| 全量 pytest（作者称 70） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| collect prefix-id features | 本地关闭 | **诚实标签关闭；MODEL-01/POS-01 不关闭。** `weight_source=offline_prefix_ids` 不再假装 \(I_4\) 隐状态（X14）。`H` 仍是前缀 token id；fit/intervene 不读该标签（D-02、D-03） |
| D-01（r2）三位置 / 泄漏 | 未单列本轮 | **部分关闭 / 残留。** 不同 limit 可分离（X8、`test_d01`）。`leaks_target` 仍不可能为 True（D-08）。CLI 首事件 `pre_step` 不可表达（D-11） |
| D-02（r2）hook 整段序列 | 未单列本轮 | **部分关闭 / 残留。** last-token 成立（X5）。不是全局 token 门控，也不是一次性（D-07） |
| D-03（r2）虚构 intervene/analyze | 未单列本轮 | **关闭虚构正确率**（X13）。结局仍未测量（D-13）。接 collect 后几何也塌成 0（D-03） |
| C-03 INLP | 未单列本轮 | **算法关闭，接入残留。** 迭代投影成立（X11）；CLI 未调用（D-06） |
| C-04 C-rand rng(1) | 未单列本轮 | **范数匹配关闭**（X12）。C-layer 仍不是弱层（D-04） |
| pending_server | 真实权重 / 隔离 Linux 执行器 / 实测 P1–P3 | **同意未关。** 本机无加载器、无可用执行器、无四项结局 |

## 6. 发现

### D-01 — 声称冻结 hash 已复现（本轮非缺陷）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `.planning/audits/round-03/VERSION.md` 声称与本机 55 文件 rel+NUL+bytes 一致
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。相对 round-02 的 hash 漂移，本轮脚本与磁盘对齐。
- **影响：** 审查对象可锚定到声称快照。不因此放行科学实现。

### D-02 — 生产 collect 仍是合成轨迹 + 前缀 token id，不采集三位置隐状态

- **状态：** confirmed defect
- **严重度：** critical
- **文件 / 符号 / 行号：** `cli.py` `cmd_collect` **248–289**（尤其 **269–277** `H`/`E`/`token_prefix`）；`_synthetic_trace` **64–81**（一字一 token）；`collect.py` **11–25** 只算索引、不保存 resid；全库无 `from_pretrained`（`tiny.py` **1** 仅注释禁止）
- **触发条件：** `reasoning-diff collect`；或期望 MODEL-01 隐状态
- **对应要求：** MODEL-01；POS-01；STACK 配置/词表同一 revision
- **证据：** X14。`weight_source=offline_prefix_ids` **诚实**，本机 NPZ 的 `H` 是 `[1,0,…]` 不是 resid。CLI 不调用 `collect_tiny` / `decode_loop` / tokenizer。`collect_tiny` 的三位置是 `len(prompt_ids)` 人为错开，返回值无隐状态。`cmd_fit` **334–337** 把该 `H` 当双线性探针输入，不读 `weight_source`。
- **影响：** 后续 fit/intervene 吃到的「H」不是模型表示。标签诚实 ≠ 采集完成。作者台账「collect prefix-id features」只覆盖命名，不覆盖 MODEL-01。
- **建议：** tiny 或本地 fixture 必须按三位置取出 last-safe token 的 resid 并写入 NPZ；卡片 revision 接入 `from_pretrained`；产物拒绝把 token id 键成 `H` 除非消费者强制分支。

### D-03 — donor 不是事件可配对样本；接 collect 后交换范数塌成 0

- **状态：** confirmed defect
- **严重度：** critical
- **文件 / 符号 / 行号：** `cli.py` **385–392**（`H[0]` / `H[min(1,n-1)]` 或 `rng.normal(size=8)`）；全库无 donor 配对、无按数值条件重提取、无可见前缀记录
- **触发条件：** 任何 `cmd_intervene`；尤其 `--in-dir` 指向本轮 collect
- **对应要求：** 协议 §4；CAUSAL-02
- **证据：** X14、X19。collect 的 `H` 仅 1 行 → `donor is base` → `main_norm=crand_norm=clayer_norm=0.0`。无 collect 时 donor = `default_rng(0)` 的第二条高斯，与任务/事件无关。相对 round-02 的 \(I_4\) 第二行，本轮「诚实前缀」使几何演示退化成恒等。
- **影响：** 即使把向量写入 hook，也不能评价「跟随 donor 来源」。接官方 collect 产物时连 \(\|\Delta\|\) 都是 0。
- **建议：** 先按事件身份配对；每个数值条件独立提取；`H` 至少两行且来自不同轨迹；记录层、token 位置与可见前缀。

### D-04 — C-layer 是同向量上的随机子空间，不是弱层干预

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `c_layer_delta` **46–49**；`cli.py` **398–399、413**（`orthonormal_basis(..., default_rng(5))` + `clayer_status="placeholder_subspace_not_dev_layer"`）。无开发集选层、无浅层 hook
- **触发条件：** 任何声称含 C-layer 的 intervene
- **对应要求：** 协议 §4「C-layer 为开发集证实依赖信息较弱的层」；IE-01
- **证据：** 与 C-rand 一样对同一 `base`/`donor` 做 \(\Pi\) 再 `scale_to_norm`。无 collect 时 `clayer_norm == main_norm == 1.8669`，但层号不存在。状态字符串比 round-02 **更诚实**，实现仍不是层对照。
- **影响：** 「相对 C-layer」只是第二种随机投影。同队列只做到「同一对 numpy 向量」，不是同批次生成。
- **建议：** 在 `dev` 上按探测曲线选弱层；与主干预同秩、同位置、同范数、同采样流执行；写入实际层号。

### D-05 — Rescue 仍是向量相加，无错误来源 / 随机分量对照

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `rescue` **70–71**；CLI 未调用
- **触发条件：** 调用 `rescue` 或宣称 Fig.3d
- **对应要求：** 协议 §4；CAUSAL-01
- **证据：** `return ablated + component`。独立运行 `rescue([1,0],[0,1]) -> [1,1]`。无错误来源、无随机救援、无恢复率。
- **影响：** 加回原分量可成恒等重建，不能单独作机制证据。
- **建议：** 同一位置比较匹配分量 / 错误来源 / 随机分量；超参在 direction_fit/dev 固定。

### D-06 — INLP 已迭代投影，但从未作用于隐状态，四项结局仍空

- **状态：** residual defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `inlp_remove` **52–67**（对 `work` 逐步 `work @ (I-uu^T)`）；`cli.py` **379–419** 未调用；`intervention_report` **74–91** 未被 CLI 使用
- **触发条件：** 期望选择性消融 / P3 Knock-out
- **对应要求：** INLP-01；CAUSAL-01
- **证据：** steps=1 vs 8 差 0.8；`test_c03` 通过。生产路径无 `P@h`、无生成、无四项结局。
- **影响：** 算法名副其实，实验仍不存在。
- **建议：** CLI 对选定位置隐状态执行；报告目标/非目标/任务正确/无效。

### D-07 — hook 只改当前前向 last-token，无全局位置门控，非一次性

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `tiny.py` `resid_post_hook` **54–76**（`patched[:, -1:] = transform(tensor[:, -1:])`）；`collect.py` `intervene_tiny` **36–40**（`t+0.01`，整段 prefill 的末 token）；未与 `decode_loop` 组合成「边界步一次」
- **触发条件：** 在 decode 循环外层保持 hook；或 `intervene_tiny`
- **对应要求：** 协议 §4 选定位置、目标首 token 之前；STACK 70–71「hook 必须一次生效，后续 decode 不得重复施加」
- **证据：** X5 证明不是全序列平移。X6：`max_new=3` 触发 3 次。`intervene_tiny` 打在 prompt 最后一枚，不是 `pre_step` 边界。产物不记录 hook 名以外的全局位置或 KV 更新范围。
- **影响：** 不是「步前单点交换」。last-token 修复不能冒充一次性门控。
- **建议：** 按全局 token 位置门控；只在边界步生效一次；随后卸 hook；记录层/位置/KV 范围。

### D-08 — `leaks_target` 仍恒为 False；`position` 不改变边界算法

- **状态：** residual defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `features.py` **25–29**（`leaks = b > limit`）；`events.py` `boundary_index` **122–128**（候选条件恒为 `b <= limit`）；`assert_no_future_leak` **41–43** 无调用方
- **触发条件：** 依赖泄漏标志或 `position="end"` 语义
- **对应要求：** POS-01；协议「跨界 token 不得泄漏目标内容」
- **证据：** 跨界被排除（`test_boundary_excludes_straddle`、X9）——排除本身正确。选中 token 必有 `b<=limit`，故 `leaks_target` 永假。`test_d01` **266–268** 只断言 False。`"before"` 与 `"end"` 同 limit 同结果（X10）。
- **影响：** 标志不可区分「已排除跨界」与「未检查」。post_step 的不同只来自调用方传入的 `target_end`。
- **建议：** 跨界应显式 `leaks_target=True` 或 `expressible=False` 并强制调用 `assert_no_future_leak`；`boundary_index` 按 kind 改变极限。

### D-09 — thinking 模板未接入；思考区数字可被当成答案

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` `apply_model_template` **51–56**（不返回 `prompt_len` / think span；无调用方）；`adapters.py` **10、18** `think_ids` 未使用；`events.py` `extract_answer` **131–142** 全文找 boxed / `####` / 最后数字
- **触发条件：** Qwen3 `enable_thinking` 或 R1 提示已含 `<think>`；思考区有数字且无 boxed
- **对应要求：** MODEL-01；STACK 56–60
- **证据：** X15、X17。`model_kind=="qwen3"` 才传 `enable_thinking`（方向对）但无调用方。测试无 `apply_model_template`。
- **影响：** 前瞻边界可能落在模板/思考标记上；无效答案与思考区数字混淆。
- **建议：** 用卡片 revision 的 tokenizer 走 `apply_chat_template`；保存 prompt 长度、think 开闭 ID、原始生成 IDs；评分限制在闭合 think 之后（无闭合则 invalid）。

### D-10 — `clone_cache` 切断了张量存储，但不是可用的 cache 克隆

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `tiny.py` `clone_cache` **79–97**（`cache.__class__()` + 逐层 `keys/values.clone()`；不能克隆则 `TypeError`）。定义仅此文件。`collect.py` **41** 只断言两次前向的 cache 不是同一对象。`test_tiny_cache.py` **7–15** 记录 `use_cache=False` 仍写入传入 cache（与 STACK 73 一致），**不调用** `clone_cache`。`decode_loop` **36** 始终 `use_cache=True`，无克隆分支
- **对应要求：** 原文「此前位置 KV 保持 base」；STACK 72–73「若克隆 DynamicCache，需验证张量无共享存储」且「缓存长度、mask、position IDs 和已输入 token 数必须对应」
- **证据：** X16。相对 round-02「无 `copy` 则返回原对象」：张量隔离 **已做到**。功能克隆 **未做到**：clone `get_seq_length()=0`、`is_initialized=False`，缺 layer `dtype`/`device`；下一步 decode 覆盖成长度 1，last-logit 与重 prefill 差 0.275。`DynamicCache` 仍无 `.copy()`。
- **影响：** 若有人按函数名复用「隔离 cache」，会静默丢掉前缀 KV。当前生产未调用，危险在接口契约，不在已落地路径。
- **建议：** 每条件重新 prefill；或复制 `is_initialized`/长度元数据并做「clone 后步进 ≡ 全前缀」对拍。在对拍之前禁止把 `clone_cache` 当作隔离。补测试。

### D-11 — CLI 首事件 `pre_step` 不可表达，却硬写 `timing=pre_step`

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **256–268、414**。合成文本 `"q = 0\n"`（fixture 只有节点 `q`）事件 `start=0`
- **触发条件：** 默认 fixture collect → intervene
- **对应要求：** POS-01
- **证据：** X14：`pre_step.expressible=false`，`token_index=null`；intervene 仍写 `"timing": "pre_step"`。
- **影响：** 产物看起来像做了步前干预。三位置元数据与干预记录互相矛盾。
- **建议：** 选有前缀的事件；inexpressible 时拒绝 intervene 或写明失败。

### D-12 — 采样配置与 StreamBank 未在条件间共享

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` `decode_loop` **38** 不传 temperature/top_k/top_p（默认 temp=1 满核）；`cli.py` intervene 用 `default_rng(0/3/5)`，不用 `StreamBank`
- **触发条件：** 「所有处理条件同一采样流」（协议 / STACK 76–80）
- **证据：** 无 generator state / 逐步 uniform 落盘。C-rand 构造与采样流未隔离（当前也无真实采样）。
- **建议：** 记录并复用采样配置与 generator；方向流与采样流隔离。

### D-13 — 非目标 / 无效输出仍不是测出来的；P3 接口缺非目标

- **状态：** residual defect
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **408–411、456–459**（诚实 null，但无测量路径）；`analysis.py` `p3_recovery` **99–106**（只有 `invalid_rate`，无 `nontarget`）
- **触发条件：** 宣称 C2/P3 四项结局
- **对应要求：** CAUSAL-02；协议 117/190/192
- **证据：** `intervention_report` 结构正确，CLI 不调用。`p3_recovery(0.5,0.4,0.3,0.1)` 无 nontarget 键。X13 四项为 null。
- **影响：** 无法排除平凡损伤；Week-8/P3 数字无测量含义。诚实 null 优于虚构，仍不是科学效应。
- **建议：** 由生成文本计算四项；P3 签名加入 nontarget，缺测为 null。

### D-14 — `IsolatedExecutor.submit` 仍是 stub；默认路径不执行宿主代码（默认路径非缺陷）

- **状态：** confirmed stub / 默认路径 non-defect
- **严重度：** medium（stub）/ 信息（host exec）
- **文件 / 符号 / 行号：** `executor.py` **22–24** `raise NotImplementedError`；**27–33** Unavailable；**49–52** 默认 Unavailable；`scoring.py` **19–30**；`t3_humaneval.py` **60–61**
- **对应要求：** EXEC-01；OPS-01
- **证据：** X18；`test_humaneval_never_host_exec` 通过。`forbid_host_exec` **55–59** 无生产引用。`SpyExecutor` 只字符串拒绝 `exec(`，但仍不执行。
- **影响：** 代码题无法真实评分（pending_server）。未发现 host exec 回退。
- **建议：** 保持默认 Unavailable；基类不要 `NotImplementedError`；真实隔离后端标 pending_server。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | （本轮关闭）声称 hash 与磁盘一致 | 已复现，不再列为疑点 |
| U-02 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载，未读官方 tokenizer JSON |
| U-03 | `transform` 若原地修改 `tensor[:, -1:]` | hook 先 clone 再写入 patched，但 transform 吃的是**原**切片。独立 `add_` 会改层输出 last-token 视图；现有调用是 `t+0.01` / `t+1` 非原地 |
| U-04 | 基线公平前瞻前缀 | `baselines.py` 仍不强制与探针同一前瞻对象；非本轮主清单，不升格为新 D 项 |
| U-05 | clone 后 `get_seq_length()=0` 是否仅因未设 `is_initialized` | 已用步进对拍证明功能失败（D-10）；未读完 transformers `DynamicLayer.update` 源码的每一分支 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | 卡片 revision 与 tiny 架构 | 无权重/tokenizer，无加载器 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post 范围符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 向量公式与 `geometry_only` CLI | 无真实轨迹与 donor |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta`（`interventions.py` **9–16**）在标准正交基下正确；`test_swap_formula` 通过 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、只改层 2 last-token、此前 token 保持；`finally` 含异常路径清理有效 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`（`adapters.py` **27–28**） |
| N-04 | 非缺陷 | `enable_thinking` 仅在 `model_kind=="qwen3"` 传入（函数仍未被调用，见 D-09） |
| N-05 | 关闭 | CLI `intervene`/`analyze` **不再写入** 0.8/0.2/0.25 或 `vs_crand=0.6`。本机 numeric outcomes 为空列表 |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数；不再等于 `default_rng(1)` 伪 main |
| N-07 | 部分关闭 | 三位置在传入不同 limit 时可分离；跨界 token 不进入 `token_index` |
| N-08 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `token_ids` / `stop_reason` |
| N-09 | 非缺陷 | 默认代码评分走隔离执行器且不 host exec |
| N-10 | 关闭（过程） | 冻结 hash 按 VERSION 脚本复现 |
| N-11 | 部分关闭（诚实） | collect 标注 `offline_prefix_ids`；intervene 标注 `geometry_only` / `placeholder_subspace_not_dev_layer`。诚实不等于实现 |
| N-12 | 部分关闭 | `clone_cache` 不再在无 `copy` 时返回原引用；无 layers/copy 时 `TypeError`。功能克隆仍失败（D-10） |
| S-01 | stub | `IsolatedExecutor.submit` → `NotImplementedError` |
| S-02 | stub | `features.npz` `H` = 前缀 token id 填进 `(1,8)`；不是 resid |
| S-03 | stub | `clone_cache` 未接入 decode/intervene；无功能测试 |
| S-04 | stub | `apply_model_template` / `think_ids` / `assert_no_future_leak` / `forbid_host_exec` 无调用方 |
| S-05 | stub | `rescue` 单行加法；`BoundaryMLP` 随机未拟合且不接入 collect（始终 `offline_annotation`） |
| S-06 | stub | `repair.run_repair` 仍可被 CLI 用固定 `generated=[1,2]` 调用（非本通道主项，列出以免漏检） |
| S-07 | 非 stub | `t2_gsm_plus.py` 空分支仅为状态枚举，非本通道 |

## 10. 通道结论

**D 通道不通过。**

相对 round-02，有三处真实、可复核的进步，且 freeze hash 已对齐：（1）CLI 仍不虚构正确率，并显式写出 `geometry_only` / `placeholder_subspace_not_dev_layer` / `offline_prefix_ids`；（2）resid_post last-token、KV 范围、hook 清理、swap / INLP 迭代 / C-rand 范数匹配保持成立；（3）`clone_cache` 不再把原对象当克隆返回，张量 `data_ptr` 已分离。

这些不够支持 CAUSAL-01/02 或 MODEL-01。生产 collect 采集的是一字一 token 的前缀 id，不是三位置隐状态；把该 NPZ 送进 intervene 会使 donor=base、三项范数为 0。C-layer 不是层。hook 非单点一次性。`clone_cache` 的 `seq_length`/`is_initialized` 错误，下一步 decode 丢前缀。thinking / 采样流 / 四项结局 / 事件 donor 仍未接通。`cmd_analyze` 的 p1–p3 为 null。诚实的空结果仍不是科学效应。
