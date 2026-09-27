# D-causal 独立审查报告（round-05）

通道 D：模型与因果（token/前缀/thinking 模板、采样与 StreamBank、hook/KV 隔离、donor 配对与同一 `weight_seed`、swap/INLP/rescue 是否真正施加、C-layer 来自真实 dev 分数或诚实缺失、三位置写成隐状态而非仅 metadata、repair Prefill/decode、`ChildProcessExecutor` 不得冒称 `IsolatedExecutor`）。

独立性声明：未阅读 round-05 其他通道报告；只把 `.planning/audits/round-05/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账；对照阅读了本通道 round-01–04 报告以便核对关闭项，结论以本机当前磁盘为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试通过当作实现正确；不把作者 `local close` 或声称 120 passed 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01 完成（真实 HF 为 `pending_server`）。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。诚实的 `offline_prefix_ids` 在未被宣称为隐状态时不记缺陷。

对照原文：论文 §2.4（交换公式、前瞻定位、C-rand/C-layer 同批次）、§4.2（步前/值前/步尾与 span 池化）、§6（V-Probing 时机对照）、§8（科学评测含交换/消融/救援与无门控修复）；GOAL §5.6–5.11、§5.13、§5.15。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T02:15:00+08:00 |
| 声称冻结 hash | `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（`.planning/audits/round-05/VERSION.md`；58 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **HASH_MATCH。** 按 VERSION 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → 58 文件 → `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4` |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；审查对象是冻结脚本覆盖的 58 个文件字节） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| 作者 pytest 声称 | 120 passed。本通道只重跑所引用子集，不把 120 记为已验证 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / `think_ids` / `load_frozen(..., local_files_only=True)` |
| `src/reasoning_diff/models/tokenize.py` | 1–32 | `encode_text` / `decode_ids` / `readout_layer_index`（60%–75% 带） / `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–183 | `collect_hidden_trace` 三位置隐状态与 span `E`；`collect_tiny`；`intervene_tiny` / `intervene_swap_decode` 的 \(\Pi_Z\) hook |
| `src/reasoning_diff/models/features.py` | 1–40 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–143 | `sample_next`；`decode_loop` 记录 sampling；`generate_task_trace`；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand / C-layer / INLP / `rescue_controls` / `select_weak_layer` / `ie_z` / `intervention_report` |
| `src/reasoning_diff/repair.py` | 1–190 | `mask_prefix` / `execute_repair_tiny` Prefill+decode / `run_repair` / `consecutive_repairs` |
| `src/reasoning_diff/cli.py` | 1–893 | 重点 `cmd_prepare` 271–307、`cmd_collect` 400–477、`cmd_intervene` 605–685、`cmd_repair` 688–708 |
| `src/reasoning_diff/executor.py` | 1–110 | `IsolatedExecutor` unavailable；`ChildProcessExecutor.isolated_sandbox=False`；`get_executor` 默认 Unavailable |
| `src/reasoning_diff/rng.py` | 41–53 | `StreamBank` 名 `sample/direction/perturb/bootstrap/split` |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理 |
| `tests/test_tiny_cache.py` | 1–26 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | 25–136、217–220、301+ | scientific collect 键存在；offline intervene 不得写 `pre_step`/`dev_weak_layer`；repair prefill；子进程非隔离 |

支持性阅读：`events.py` `parse_fixture_events` 27–67、`boundary_index` 173–179、`extract_answer` 182–196；`scoring.py` `score_code` 19–30；`schema.py` `POSITION_KINDS` 39；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/research/STACK.md` 54–90；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | **HASH_MATCH** `4c8769f3…cd6d56e4`；58 文件 |
| X2 | `pytest` tiny/因果相关子集 18 项 + `test_cli_pipeline` + `test_humaneval_never_host_exec` | **20 passed / 10.40s**。通过只证明冒烟，不证明因果协议 |
| X3 | `apply_swap` 与标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.171\)、\(\Delta V_{\max}=0.364\)，且 **仅 last token**（earlyK=0）。与 STACK resid_post 契约一致 |
| X5 | 仅 last-token vs 全序列 | `transform` 形状 `(1, 1, 32)` |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3 次**；`once=True` **1 次** |
| X7 | hook `finally` 清理 | `RuntimeError` 后 `layer._forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`（60%–75% 带）；`hidden_all` `(5,32)`（含生成 token）；三位置 token_index **2/3/4**；`sampling` 已写入 |
| X8b | `collect_hidden_trace` + fixture 文本 `"p1 = 4\\np2 = 0\\nq = 0\\n"` | 事件 `q` start/value/end = **14/18/19**；token_index **13/17/18**；三键与 `hidden[idx]` **逐位相等**；位置间 \(\|\Delta\|\approx 0.158/0.185/0.239\)；`E` 两行 \(\|\Delta\|\approx 0.068\)（span 均值，不是 metadata） |
| X8c | CLI `--backend tiny` 无 `--in-dir` | `features.npz` 含 `H/E/H_pre_*`；三位置 \(\|\Delta\|\approx 0.155/0.150/0.143\)；`H` 仅 1 行 → intervene `donor_missing` |
| X8d | fixture `prepare`→`collect` | 两轨迹文本不同（`p2=0,q=0` vs `p2=2,q=8`），但 `token_ids` 同为 `1..20`（`_synthetic_trace` 按长度填序号）；`H[0]==H[1]`；intervene 仍 `donor_missing` |
| X8e | scientific `prepare`→`collect` | 5 条 `tiny-qwen2` 轨迹，**事件数全 0**；`H` `(5,32)` 行间 \(\|\Delta\|\approx 0.132\)；`H_pre_step==H_pre_value==H_post_step==H[-1]`（末 token 回退） |
| X9 | `leaks_target` 能否为 True | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None`。150 次中 **72 True / 78 False**（60 次 index 空） |
| X10 | `boundary_index(..., 2)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 1；`position` 只做枚举校验 |
| X11 | INLP / rescue | steps=1 vs 8 最大差 **0.550**。`H@P8` 第一列≈0。`rescue([1,0],[0,1])=[1,1]`。`rescue_controls` 给出 matched / error_source / random，随机范数匹配 |
| X12 | C-rand / C-layer 范数与弱层 | 缺范数仍 `ValueError`。`select_weak_layer({0:0.2,1:0.1,2:0.4})=1`。默认 CLI：`clayer_status=dev_scores_missing`。传入 `--dev-layer-scores 0.2 0.1 0.4`：标签改 `dev_weak_layer`，`weak_layer=1`；传入 `0.05 0.9 0.8`：`weak_layer=0` 且 **主 decode hook 打在层 0**。三项范数仍完全相同（0.058423） |
| X13 | StreamBank vs 实际 hook 基 | CLI `direction` 抽出 113750710，`perturb` 抽出 17172908。同一 `H[0]/H[1]`：CLI 基 \(\|\Delta\|=0.058423\)（与落盘 `main_norm` 一致）；`intervene_swap_decode` 内部 `default_rng(1)` 基 \(\|\Delta\|=0.031214\)；两基最大元素差 **0.862**。`sample` 流从未读取 |
| X14 | swap 是否真正施加 | `intervene_tiny`：`transform=pi_z_swap`，logits \(\Delta_{\max}=0.263\)，cache 对象隔离。`intervene_swap_decode`：`hook_fired=True`，本例生成 ids 与基线相同（`followed_donor=false`）。CLI 前缀是 `encode_text("follow donor")[:8]`，**不是** collect 轨迹 |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 内数字 → None；未闭合 → None；`</think>` 后 boxed/#### → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 无调用**。`from_pretrained` 仅在 `load_frozen` |
| X16 | `clone_cache` / DynamicCache | 本机无 `.copy()`。clone ≠ 原对象；`data_ptr` 不同；`add_` 后原张量不变；`get_seq_length()=5`；步进 vs 全前缀 last-logit \(\Delta_{\max}=3.0\times 10^{-8}\)。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states` 长度 4。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.746\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False`；`SubprocessExecutor is ChildProcessExecutor`。默认 `score_code` → `executor_unavailable` / `value=None`。子进程可跑通 `assert`，源含 `exec(` 则 `rejected`。生产无宿主 `exec` 回退 |
| X19 | repair Prefill/decode | `--backend tiny`：`refilled_prefix=true`，`extra_prefill_tokens=20`，`generated_tokens=8`。`--backend offline`：诚实 `prefill_unavailable`。scientific：`k=1..5` 均 refilled，但 `task_oracle` 下五次 `extra_prefill_tokens` 皆 32（k 不改变前缀） |
| X20 | `weight_seed` | 同 seed 同 ids → \(\|\Delta H\|=0\)；异 seed 同 ids → 0.156；同 seed 异 ids → 0.055。`collect_hidden_trace` 与 `generate_task_trace` 默认 seed=0 对齐；CLI collect **写死** `weight_seed=0` |
| X21 | scientific intervene 落盘 | `status=prospective_decode`，`timing=pre_step`，`transform=pi_z_swap`，`hook_once="resid_post"`（字符串），四项结局 **null**，产物不含 0.6/0.55/0.8/0.2/0.25。`ie_z=-0.00234` 来自救援向量均值差，不是 \(g(Y)\) |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server` |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存。属 `pending_server` |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹、无事件可对齐 donor 队列 |
| 全量 pytest（作者称 120） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| D4-02 / A4-03 C-layer | 无 `--dev-layer-scores` 写 `dev_scores_missing`；有则 `dev_weak_layer` | **标签默认关闭。** 默认不再谎称 `dev_weak_layer`。协议未关：C-layer 仍是同向量 QR 子空间；提供分数时主 hook 打到弱层（D5-02） |
| D4-03 / A4-02 三位置隐状态 | 写 readout 层 `H_pre_*` 与 span `E` | **fixture 路径关闭。** 有事件时三键是 `hidden[token_index]`。scientific 无事件时三键塌成同一末 token（D5-03） |
| D4-04 swap/INLP/rescue | tiny `intervene_swap_decode` 施加 \(\Pi_Z\) | **swap 算法关闭 / 接线未关。** hook 不再是 `+0.01`，但是打在 `"follow donor"` 假前缀上；INLP/rescue 只做 numpy（D5-04） |
| D4-05 / D4-07 donor 与 StreamBank | 共享 `weight_seed`；intervene 用 StreamBank | **seed 关闭 / 配对与采样流未关。** 同 seed 可复现（X20）。fixture donor 因序号 `token_ids` 退化；StreamBank 不驱动 hook 基与采样（D5-05、D5-07） |
| A4-04 repair Prefill/decode | scientific/tiny `execute_repair_tiny` + `k=1..5` | **Prefill/decode 关闭。** tiny 路径重新编码当前前缀再 decode；offline 诚实不可用。连续 k 对 `task_oracle` 不改变前缀（残留） |
| A4-13 `ChildProcessExecutor` | 不是 `IsolatedExecutor` | **关闭。** 类旗标、继承与默认入口均未冒称隔离沙箱（D5-08） |
| A4-22 Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |
| pending_server | 真实权重 / Linux cgroup / 实测 P1–P3 | **同意未关。** tiny 随机权重不是 MODEL-01 |

相对 r04 已关闭、本轮不再单列缺陷：默认 C-layer 谎言标签；fixture 三位置仅 metadata；hook 为 `+0.01`；虚构 intervene/analyze 正确率；C-rand 缺范数仍构造；`leaks_target` 永假；`extract_answer` 把思考区当答案；`clone_cache` 丢 `seq_length`；默认宿主 exec。

## 6. 发现

### D5-01 — 声称冻结 hash 已复现（本轮非缺陷）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `.planning/audits/round-05/VERSION.md` 声称与本机 58 文件 rel+NUL+bytes 一致
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。
- **影响：** 审查对象可锚定到声称快照。不因此放行科学实现。

### D5-02 — C-layer 缺分时标签诚实，有分时主干预被接到弱层；对照仍是同向量子空间

- **状态：** confirmed defect（接线） / closed（默认标签）
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **616、627–636、656**（无分数：`weak=1` + `dev_scores_missing`；有分数：`select_weak_layer` 后 `intervene_swap_decode(..., layer=weak)`）；`interventions.py` `c_layer_delta` **46–49**（对同一 `base`/`donor` 做 \(\Pi\) 再按范数缩放）
- **触发条件：** 默认 `intervene`；或 `--dev-layer-scores 0.05 0.9 0.8`
- **对应要求：** 论文 §2.4 对照协议；GOAL §5.11；IE-01
- **证据：** X12。默认 scientific intervene 写 `clayer_status=dev_scores_missing`，不再出现 r04 的硬编码 `dev_weak_layer`。提供分数 `0.05,0.9,0.8` 后 `weak_layer=0`，且这是**唯一**一次 decode 的 hook 层——主干预被放到声称的弱层。C-rand/C-layer 没有第二次前向；三项范数锁成同一值 0.058423。`c_layer_delta` 不读取该层隐状态。
- **影响：** 「诚实缺失」满足审查口径的标签要求。一旦调用方给出 dev 曲线，落盘像做了层对照，实际是把主 \(\Pi_Z\) 换到弱层，C-layer 仍是第二种随机投影。
- **建议：** 主干预固定在读出层；C-layer 用该弱层的 \(H\) 另跑同秩、同位置、同范数、同采样流的一次 decode。未做第二次前向时不要写 `dev_weak_layer`。

### D5-03 — scientific 无事件时三位置键塌成同一末 token；有事件的 fixture 路径已写成隐状态

- **状态：** confirmed defect（scientific / 空事件回退） / closed（有事件的 tiny fixture）
- **严重度：** high
- **文件 / 符号 / 行号：** `collect.py` **39–73**（无事件则 `h_matrix=hidden[last:last+1]`，三键都指向它）；`cli.py` **424–438**（`H` 按轨迹 vstack，`H_pre_*` 只取**最后一条** `meta`）；`generate.py` **105–110**（tiny 乱码几乎解析不出 `q = <number>`）
- **触发条件：** `prepare --eval-mode scientific` 之后的 `collect --backend tiny`；或任何 `events==[]` 的 collect
- **对应要求：** POS-01；论文 §2.4/§4.2 步前/值前/步尾；GOAL §5.6
- **证据：** X8b–X8e、X22。fixture 文本事件 `q` 的 13/17/18 与 `hidden[idx]` 一致，三键互异（\(\|\Delta\|>0.14\)），`E` 为同层 span 均值——这关闭了 r04「只写 metadata、H 是截断末 hidden」的 fixture 半截。scientific 五条轨迹事件数为 0；`H_pre_step==H_pre_value==H_post_step==H[-1]`，有限浮点、无 NaN、无 `expressible=false`。空事件本可走已有的 `np.full(..., nan)` 分支，却被末 token 回退冒充三位置。
- **影响：** 读 `features.npz` 的下游会以为做了三时机。scientific 路径（作者宣称关闭 D4-03 的路径）比较的是同一向量。fixture 接口证明不能外推到 generate 轨迹。
- **建议：** 无事件或 `token_index is None` 时三键写 NaN 并记录 `expressible=false`；有事件时按轨迹堆叠三键，而不是只留最后一条 meta。

### D5-04 — 生产 swap 已写入 resid_post，但打在假前缀上；INLP/rescue 未进入生成

- **状态：** confirmed defect（接线） / residual（诚实 null 结局）
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **641–656、643–647**（`inlp_remove`/`rescue_controls`/`ie_z` 只写 report；decode 前缀 `"follow donor"`）；`collect.py` `intervene_swap_decode` **158–173**（`default_rng(1)` 构造基，`once=True` 包住 `decode_loop`）；`interventions.py` `ie_z` **88–89**
- **触发条件：** 对 scientific tiny collect 做 `reasoning-diff intervene --backend tiny`
- **对应要求：** CAUSAL-01；INLP-01；论文 §2.4 执行协议（对齐步前边界、保留 base 前缀与 KV）
- **证据：** X14、X21。相对 r04：`transform=pi_z_swap`，`hook_fired=True`，`intervene_tiny` logits 非零差，不再是 `t+0.01`。CLI 不把 collect 的 `token_ids` 或步前 index 传入 decode；donor 是某行 32 维向量，base 隐状态来自无关 8-id 假前缀。本例 `followed_donor=false` 仍写 `status=prospective_decode`、`timing=pre_step`。INLP/rescue 有算法与调用，投影从未进入 hook。`ie_z` 是救援隐向量均值差，不是 \(\mathbb E[g(Y_{>i})]\)。四项结局诚实为 null。
- **影响：** 可以证明 \(\Pi_Z\) hook 接口，不能评价「跟随 donor」或选择性消融。落盘 timing 比实际协议更强。
- **建议：** 在目标事件步前 token 上施加 \(H'\) 一次后卸 hook，再 decode；同一位置跑 INLP 与 `rescue_controls`；由生成文本算四项。未对齐事件时不要写 `pre_step`/`prospective_decode`。

### D5-05 — `weight_seed` 已共享；donor 仍不是事件可配对的来源—数值条件

- **状态：** residual / confirmed defect（fixture 退化）
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **104**（`token_ids=range(1,len+1)`）、**307**（`make_source_value_pair(...)` 返回值丢弃）、**426**（collect 写死 `weight_seed=0`）、**619–621**（`H[0],H[1]` 即 donor）；`collect.py` **33–34、83–84**
- **触发条件：** fixture `prepare`→`collect`→`intervene`；或把 scientific `H` 的前两行当作 C2 donor
- **对应要求：** 论文 §2.4 donor 协议；CAUSAL-02；GOAL §5.10
- **证据：** X8d、X8e、X20。同 `weight_seed` 同 ids 隐状态可复现，异 ids 有差——seed 契约本身成立。fixture 两条轨迹文本不同但序号 ids 相同，几何被 `allclose` 判成 `donor_missing`。scientific 用不同生成 ids 做出非零 \(\|\Delta\|\)，配对规则是 vstack 后的第 0/1 行（各轨迹末 token），不是事件身份、也不是来源—数值解耦。`make_source_value_pair` 已构造却不写入 traces。
- **影响：** 本机可演示「有/无两行向量」，不能评价来源跟随。真实 50 条队列保持 `pending_server`。
- **建议：** 按事件身份配对；每个数值条件独立提取；记录层、token、可见前缀与 `weight_seed`。合成轨迹的 ids 必须来自文本编码，不能按长度填序号。

### D5-06 — thinking 抽取仍正确；模板 / `think_ids` / `load_frozen` 仍未接入

- **状态：** residual defect（模板路径） / closed（`extract_answer`）
- **严重度：** medium（模板；真实 HF 为 pending_server）
- **文件 / 符号 / 行号：** `events.py` `extract_answer` **182–196**；`generate.py` `apply_model_template` **137–143**、`generate_task_trace` **83–88**（`encode_text(task.question)`，无 chat template）；`adapters.py` **10、18、32–42**
- **触发条件：** 声称 MODEL-01 模板对齐；或 Qwen3 `enable_thinking` / R1 提示已含 `<think>`
- **对应要求：** MODEL-01；GOAL §5.6；STACK 56–60
- **证据：** X15。思考区数字不再当答案。`prompt_len` / 原始 `prompt_ids`/`generated_ids` 已保存。CLI 与 `generate_task_trace` 均不调用 `apply_model_template`。tiny 随机权重按口径不算 MODEL-01 完成。
- **影响：** 本机评分不被未闭合 think 误导。一旦接真实 tokenizer，前瞻边界仍可能落在未应用的模板标记上。
- **建议：** 卡片 revision 走 `apply_chat_template`；保存 prompt 长度、think 开闭 ID、原始生成 IDs。在此之前不要把 tiny 路径写成模板已对齐。

### D5-07 — StreamBank 只驱动几何 RNG；采样流与 hook 基未共享

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **610–626、656**；`collect.py` **158、166–173**（hook 基 `default_rng(1)`；decode 用 `Generator.manual_seed(seed)`，不读 StreamBank）；`rng.py` **41–50**
- **触发条件：** 「所有处理条件同一采样流」（论文 §2.4；STACK 76–80；GOAL §5.4/§5.10）
- **证据：** X13。落盘 `main_norm` 等于 StreamBank `direction` 基，不等于实际施加的 `rng(1)` 基（0.058423 vs 0.031214）。`sample` 流空闲。patched/baseline 虽共用 torch seed，C-rand/C-layer 没有 decode 条件。无 generator state / 逐步 uniform 落盘。
- **建议：** 记录并复用采样配置与 generator；方向流与采样流隔离；报告范数必须来自**实际写入 hook** 的那组基。

### D5-08 — `ChildProcessExecutor` 未冒称 `IsolatedExecutor`（默认路径非缺陷）

- **状态：** closed / non-defect（命名） / stub（真实隔离未到）
- **严重度：** n/a（命名） / medium（真实沙箱 pending_server）
- **文件 / 符号 / 行号：** `executor.py` **27–33、59–63、94–102**；`scoring.py` **19–30**
- **对应要求：** GOAL §5.15；EXEC-01
- **证据：** X18；`test_child_process_is_not_isolated_executor` 通过。默认 Unavailable；子进程旗标为 False 且不进入隔离继承树。`score_code` 的 metric 名仍是 `isolated_unit`，但 `status/reason` 诚实，不把子进程写成已验收沙箱。
- **影响：** 代码题默认无法真实评分。未发现 host exec 回退。
- **建议：** 保持默认 Unavailable；Linux cgroup 标 pending_server。metric 名可改为按后端填写，以免与类名口径打架。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载，未读官方 tokenizer JSON |
| U-02 | `transform` 若原地修改 `tensor[:, -1:]` | hook 先 clone 再写入 patched；现调用是新张量 `apply_swap` 结果 |
| U-03 | `cmd_fit` 不读 `weight_source` | offline 前缀 id 可被当成双线性 `H`。标签诚实；消费者忽略标签更偏探针通道 |
| U-04 | `score_code` metric 恒为 `isolated_unit` | 默认走 Unavailable，未把 `ChildProcessExecutor` 标成 `IsolatedExecutor` |
| U-05 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够；未读完 transformers 每一分支 |
| U-06 | scientific 连续 k 对 `task_oracle` 五次 Prefill 相同 | 更偏修复协议/附录预算，不单独升格为因果缺陷 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是** MODEL-01 完成 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 向量公式与 dummy-prefix \(\Pi_Z\) decode | 无事件对齐 donor，无四项实测结局 |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta` 在一维标准正交基下正确 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、只改层 2 last-token；`finally` 含异常路径清理 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`；`enable_thinking` 仅在 `model_kind=="qwen3"` 传入 |
| N-04 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `token_ids` / `stop_reason` / `sampling` |
| N-05 | 关闭 | CLI `intervene`/`analyze` **不再写入** 虚构正确率；本机 numeric outcomes 为空 |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数 |
| N-07 | 关闭 | 跨界 token 不进入 `token_index`；`leaks_target` 在 straddling 时可为 True |
| N-08 | 关闭 | `extract_answer` 去掉闭合 think；未闭合返回 None |
| N-09 | 关闭（选项） | `resid_post_hook(..., once=True)` 在 decode 中只生效一次 |
| N-10 | 关闭（功能） | `clone_cache` 隔离存储并保留 `seq_length`；步进 ≡ 全前缀 |
| N-11 | 关闭（过程） | 冻结 hash 按 VERSION 脚本复现（HASH_MATCH） |
| N-12 | 非缺陷 | `--backend offline` 的 `H` 是前缀 id 且标注 `offline_prefix_ids`；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny `H` 是随机初始化隐状态并标注 `random_init`。这是本机接口证明，不是 MODEL-01 完成 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 默认 `clayer_status=dev_scores_missing`（见 D5-02 接线残留） |
| N-16 | 关闭（有事件时） | fixture 三位置与 span `E` 是读出层隐状态，不是 metadata-only（见 D5-03 scientific 残留） |
| N-17 | 关闭（算法） | tiny hook 路径的变换是 \(\Pi_Z\) swap，不是 `+0.01`（见 D5-04 接线残留） |
| N-18 | 关闭 | tiny/scientific repair 对当前前缀重新 Prefill 再 decode；offline 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` / `forbid_host_exec` 无生产调用方 |
| S-03 | stub | `rescue_controls` / `inlp_remove` 有 CLI numpy 调用，不进入 hook |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道不通过（FAIL）。冻结：HASH_MATCH。**

相对 round-04，本轮有可复核的接口关闭，且 freeze hash 已对齐：（1）有事件的 tiny fixture 把步前/值前/步尾写成读出层隐状态，`E` 为同层 span 均值；（2）默认 C-layer 写 `dev_scores_missing`，不再硬编码 `dev_weak_layer`；（3）tiny hook 施加 \(\Pi_Z\) 且 `once=True`，KV 范围符合 resid_post 契约；（4）`weight_seed` 可使同 ids 隐状态复现；（5）tiny repair 重新 Prefill 再 decode，offline 诚实不可用；（6）`ChildProcessExecutor` 未冒称隔离执行器；（7）仍不虚构四项正确率；Gate 未注册不记缺陷。微型随机权重按口径不算 MODEL-01 完成。

这些不够支持 CAUSAL-01 或 POS-01 的本机协议。scientific generate 轨迹解析不出事件时，三个位置键塌成同一末 token 还写成有限隐状态。生产 intervene 把 \(\Pi_Z\) 打在 `"follow donor"` 假前缀上，INLP/救援停在 numpy，`ie_z` 不是结果量。fixture donor 因序号 `token_ids` 退化为全等。StreamBank 只解释落盘范数，不解释实际 hook 基。给出 dev 分数时主 hook 被接到弱层，C-layer 仍无第二次前向。诚实的几何/接口演示仍不是前瞻因果实验。
