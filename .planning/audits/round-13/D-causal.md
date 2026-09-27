# D-causal 独立审查报告（round-13）

通道 D：模型与因果（token/prefix、thinking 模板、sampling、hook/KV、donor 来源、swap/消融/救援、两类对照、nontarget/invalid）。指定独立复跑 scientific `prepare`→`collect --backend tiny`→`intervene --backend tiny`（另跑 `--dev-layer-scores 0.05 0.9 0.8`）→`repair --eval-mode scientific`，夹具 `tests/fixtures/t1_tiny.json`，`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15`。猎项：`parse_region=generated` 且事件 `start ≥` 问句/`prompt_len`；生成区无 prompt `p1`/`p2`；有限 \(H\)、无 NaN `pre_step` 行、不可表达 `start=0` 跳过；donor 来自 `source_value_pair` 的 `trace-base`/`trace-edit`（非全 NaN、非恒等 \(H\)）；INLP 为 \(h@P\) 不是 \(\Pi_Z\)；C-rand `add_delta`；rescue `replace`；`ie_z` 来自 target-follow \(g(Y)\)；有 `--dev-layer-scores` 时 C-layer 弱层 `add_delta`；几何 `timing` 保持 `offline_hidden`（不得写成 tiny 上的 live `pre_step` hook）；Prefill 接受真实 32-d hidden，拒绝 `0`/`True`/`1.0`/`[0]`/`[]`；教师强制 `q` 诚实标 `constrained_target`。tiny **不是** MODEL-01；约束 `\nq = <digit>` **不是** §4.1 自然 CoT。

独立性声明：未阅读 round-13 其他通道报告；只把 `.planning/audits/round-13/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账。对照读了本通道 round-10 / round-11 报告仅作版式与猎单对照，不作本轮证据。结论以本机当前磁盘与本轮复跑为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试绿当作论文正确性；不把作者 `local close` 或声称 156 passed 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。

对照原文：论文 §2.4（交换公式、C-rand/C-layer 同批次）、§4.1（自然 CoT，本机不得冒称）、§4.2（三位置）、§6/§8（来源—数值 / 交换 / Knock-out / Rescue）；GOAL MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01；`docs/EXPERIMENT_PROTOCOL.md` §4。tiny 路径只验收接口与接线，不验收 MODEL-01。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结 **HASH_MATCH** `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（61 文件，0 CRLF）。指定 scientific 路径点名项在该窗口立即复跑后全部成立。交卷再算同一脚本为 **HASH_MISMATCH**（61 文件 / `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`）。本通道未改冻结集；窗口内他方改写 `cli.py` 与 `tests/test_round07_regressions.py`。D 核心（`collect.py` / `generate.py` / `interventions.py` / `repair.py` / `tiny.py`）哈希未变；`cmd_intervene` 函数体与开审阅读一致，仅行号上移约 5 行。tiny 不是 MODEL-01，不得写 §4.1。

**总裁决：FAIL。开审 HASH_MATCH。交卷 HASH_MISMATCH。指定猎项在开审 MATCH 窗口关闭。不得把本报告签在声称快照 `0816fa5b…` 上。不宣布 Goal 完成。不得启动连续通过计数。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21（Asia/Shanghai）；开审约 02:34，交卷约 02:52 |
| 声称冻结 hash | `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（`.planning/audits/round-13/VERSION.md`；61 文件；POSIX relpath + NUL + bytes） |
| 开审复算 | **HASH_MATCH。** 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → **61** 文件 → `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b` |
| 交卷复算 | **HASH_MISMATCH。** 同脚本 → 61 文件 / `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`。CRLF 计数开审为 0。本通道未改冻结集。他方改写 `cli.py`（`175abf12…` / 61130 B → `779cedd3…` / 60895 B，mtime 02:38:44）与 `tests/test_round07_regressions.py`（mtime 02:38:53） |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；`src/`/`tests/`/`pyproject.toml` 为未跟踪。HEAD 不是冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载；无 CUDA |
| 作者 pytest 声称 | 156 passed。本机全量 **156 passed / 21.37s / exit 0**。因果相关 7 个文件 **64 passed / 18.78s**。绿只锁回归，不是论文正确性 |
| 明确未读 | `.planning/audits/round-13/` 下除 `VERSION.md` 与本文件外的其他通道报告 |

因果生产文件开审 SHA-256 前 16：`cli.py` `175abf12f4c207c5`（61130 B）、`collect.py` `83658cd8ba879f20`（261 行）、`generate.py` `07493570c6410e6b`（201）、`tiny.py` `21725a183452bd06`（120）、`features.py` `0a9f0b8beb0185ae`（39）、`adapters.py` `c1992624026a1bf0`（42）、`tokenize.py` `b0cc8974af1010fa`（31）、`interventions.py` `0ffdbb8805be7649`（115）、`repair.py` `f76ff9998b9a6b17`（232）、`edits.py` `cacb63ac27cbcccf`（287）、`events.py` `290a4fd676ac0814`（274）、`executor.py` `481d6ed597c93e78`（109）、`rng.py` `2098c2c72a852eaa`（53）。交卷时除 `cli.py` 变为 `779cedd373a8a509`（60895 B）外，上列其余文件哈希不变。`cmd_intervene` / `_pair_source_value` / `_expressible_donor` / `cmd_repair` 函数体与开审阅读一致，行号约 −5。

## 2. 范围与逐文件覆盖

指派阅读并逐行核对（行号为开审阅读 / 复跑所用 `cli.py` `175abf12…`；交卷 `cli.py` 行号约 −5，`cmd_intervene` 函数体未变）：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / 卡片 `think_ids` / `load_frozen(..., local_files_only=True)`。`revision=="latest"` 拒绝 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids`（**非互逆**）/ `readout_layer_index`（60%–75% 带）/ `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–261 | `collect_hidden_trace` 不可表达步前 **continue**；`intervene_hidden_decode` 四 mode：`pi_z_swap` / `inlp`（`vec @ proj`）/ `add_delta` / `replace` |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–201 | `sample_next`；`decode_loop`（独立 `torch.Generator`）；`append_target_assignment`；`generate_task_trace` 只解析生成区；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / `inlp_remove` / `rescue_controls` / `select_weak_layer` / 库函数 `ie_z`（隐向量均值）/ `intervention_report` |
| `src/reasoning_diff/edits.py` | 151–226 | `apply_rename_edit`；`make_source_value_pair`：value 臂 + rename 臂 |
| `src/reasoning_diff/repair.py` | 1–232 | `_hidden_is_prefill` 拒绝标量/bool/`[0]`；`execute_repair_tiny`；`run_repair` |
| `src/reasoning_diff/cli.py` | 257–438、440–547、676–689、811–867、870–1013、1016–1056 | prepare/collect/pair/donor/intervene/repair |
| `src/reasoning_diff/executor.py` | 1–109 | `ChildProcessExecutor.isolated_sandbox=False`；默认 Unavailable |
| `src/reasoning_diff/rng.py` | 41–53 | StreamBank `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/events.py` | 27–89、251–274 | `parse_events`；`boundary_index`；`extract_answer` 去 think |
| `tests/test_tiny_hooks.py` | 全文件 | 前向 + hook 清理（绿只作冒烟，不作通过证据） |
| `tests/test_tiny_cache.py` | 全文件 | cache 隔离冒烟 |
| `tests/test_generate_loop.py` | 全文件 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | scientific / Prefill / readout 相关 | 字段锁，不替代本轮复跑 |
| `tests/test_round05_regressions.py` | scientific 事件 / 几何 timing | 同上 |
| `tests/test_round06_regressions.py` | `donor_kind`/`inlp`/`add_delta`/`replace`/`ie_z_g` | **不**比 \(h@P\) 数值 |
| `tests/test_round07_regressions.py` | 标量/`[0]` Prefill | 本通道另用 `run_repair` 直接核验 |

支持性阅读：`schema.py` `POSITION_KINDS`；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` 上列要求。未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次、自然 CoT。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`、`measure.py`、`splits.py`（他通道）。`cli.py` 校准/fit 段属其他通道。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | VERSION 脚本逐字复算 | **开审 HASH_MATCH** 61 / `0816fa5b…93de3b`（0 CRLF）。**交卷 HASH_MISMATCH** 61 / `1f61fd06…b91637`。见 D13-00 |
| X2 | 因果相关 pytest 7 文件 | **64 passed / 18.78s**。绿只锁冒烟与字段名 |
| X2b | 全量 pytest | **156 passed / 21.37s / exit 0**，与作者数字一致。仍不是论文正确性，不把 156 写成 Goal 完成 |
| X3 | `apply_swap` 标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.168\)、\(\Delta V_{\max}=0.387\)，且 **仅 last token**（earlyK=0） |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3** 次；`once=True` **1** 次 |
| X7 | hook `finally` 清理 | 正常与 `RuntimeError` 后 `_forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)` |
| X8c | 空事件库层 | `h_position=no_event`，\(H\) `(0,32)`，不塌成末 token |
| X8e | **指定** scientific `prepare`→`collect --backend tiny --weight-seed 0` | 6 条轨迹：`trace-base` / `trace-t0p` / `trace-edit` / `trace-source` / `p1:0` / `p2:2`。每条 **1** 个生成区 `q`（base/edit `start=45`；source `53`；`parse_region=generated`，`parse_status=constrained_target`）。问句前提不进入事件。`H` `(6,32)` **6/6 行有限**（0 NaN）；`H_pre_step/value/post` 同样 0 NaN 行。`event_rows.jsonl` 6 行皆 `{node_id:q, trace_id:…}`。`hidden_layer=1`；`weight_source=random_init`；`weight_seed=0`。\(\\|H_0-H_1\\|\approx 0.00778\)（base vs t0p），\(\\|H_0-H_2\\|\approx 0.00430\)（base vs edit），\(\\|H_0-H_3\\|\approx 0.00832\)（base vs source） |
| X8f | scientific collect 拒绝 | `--backend offline` → `ValueError: scientific collect refuses offline_prefix_ids as H` |
| X8g | re-encode vs 生成 ids | 每条轨迹与 `encode_text(text)` 有 **8** 处不同（恰 `max_new=8` 乱码段，下标 36–43 或 source 的 44–51）。collect 的 \(H\) 是对表面文本的二次前向 |
| X8h | 步前 vs 前缀前向 | `H[0]` 与 `hidden[44]` 及 `encode_text(text[:45])` 末 token **逐位相等**（\(\Delta=0\)）；\(\\|H[0]-\mathrm{last}\\|\approx 0.147\) |
| X9 | `leaks_target` | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None` |
| X10 | `boundary_index` | `start=0,"before"` → **None**。`limit=2` 的 `"before"` / `"end"` / `"value"` 皆为 1 |
| X11 | INLP / rescue 算法 | `rescue([1,0],[0,1])=[1,1]`。随机向量上 \(h@P\) 与 `apply_swap` 最大差 **1.22**（不是同一变换）。库函数 `ie_z(donor,base)\approx 4.91\times 10^{-5}`；**CLI tiny 路径不写该值** |
| X12 | C-rand / C-layer 范数与弱层 | 缺范数仍 `ValueError`（`C-rand requires the actual main-intervention norm`）。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0`。三项范数经 `scale_to_norm` 锁成同一 `main_norm` \(2.4187\times 10^{-4}\) |
| X13 | StreamBank vs hook 基 | `direction` 第一抽 113750710（丢弃）；第二抽 **basis_seed=1153799966**。`sample` 第一抽 **1191642646**。`perturb` 17172908 |
| X14c | **指定** collect→intervene（**无** `--dev-layer-scores`） | `_pair_source_value` 返回 **`(0, 2, same_source_diff_value)`** = `trace-base` / `trace-edit` 的同身份 `q`（**不是** `trace-t0p`）。`status=prospective_decode`，几何 **`timing=offline_hidden`**。`relative.hook_once=resid_post`，`transform=pi_z_swap`，`hook_timing=pre_step`（hook 内部标签，几何字段未改写）。monkeypatch 记录 **4** 次 `intervene_hidden_decode`：层皆 **1**，模式 **`pi_z_swap` / `add_delta` / `inlp` / `replace`**，`hook_fired=true`。INLP **无 donor**、有 `projector` `(32,32)` rank 30。`clayer_status=dev_scores_missing`（无弱层 decode）。`ie_z=0.0`，`ie_z_g=target_follow`。对照四项因 clayer 空而 **null** |
| X14d | 另跑 `--dev-layer-scores 0.05 0.9 0.8` | **5** 次独立 decode，层 **1 / 1 / 0 / 1 / 1**，模式 **`pi_z_swap` / `add_delta`(C-rand) / `add_delta`(C-layer) / `inlp` / `replace`**。`clayer_status=dev_weak_layer_decode`，`weak_layer=0`。C-rand `delta` 头 4 维与独立重算 `c_rand_delta` **相等**；弱层 `delta` 与独立重算 `c_layer_delta(..., rng(5+0))` **相等**。三项范数与落盘一致。相对四项 `vs_crand=vs_clayer=0.0` |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 内数字 → 7；未闭合 → None；`</think>` 后 boxed → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 与 `generate_task_trace` 无调用**。本轮不要求自然 CoT |
| X16 | `clone_cache` / DynamicCache | clone ≠ 原对象；`data_ptr` 不同；`add_` 后原张量不变；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.746\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False` |
| X19 | Prefill | `execute_repair_tiny` 返回 **32** 维有限非零（\(\\|h\\|\approx 5.65\)）。`run_repair` 接受该向量 → `refilled_prefix=True`/`ok`。`0` / `True` / `1.0` / `[0]` / `[0.0]` / `[]` / `None` / `False` / `"x"` / 仅 `prefix_token_ids` → `prefill_unavailable`。scientific CLI repair：k=1..5 皆 `refilled_prefix=True`、`status=ok`、`gated=False`、`extra_prefill_tokens=32`；jsonl **无** `prefill_hidden` 字段 |
| X20 | `weight_seed` | 同 seed 同 ids → \(\\|\Delta H\\|_{\max}=0\)；异 seed → 0.078；同 seed 异 ids → 0.090。CLI collect 写入 spec `weight_seed=0` |
| X21 | 来源-数值 | `edits.jsonl` 含 `kind=source_value_pair`：targets=`["q"]`，nontargets=`["p1"]`，`trace_ids={base:trace-base, same_source_diff_value:trace-edit, same_value_diff_source:trace-source}`。donor 行是 base/edit，kind=`same_source_diff_value`。`make_source_value_pair` 改写图：`p1 * p2_src`，parents 不含 `p2`。`_try_source_value_pair` 对 T3 / paragraph 返回 None（代码路径；本轮夹具未触发） |
| X22 | 事件跨度 / hook 前缀 | 生成区 `q` 跨度 45–51（source 53–59），前缀 45（source 53）字符；`ids[:64]` **未截断**（`prefix_truncated=false`）。6/6 `start ≥ len(prompt_text)` 且 `start ≥ prompt_len`（本机 1 字符 = 1 token） |
| X23 | \(g(Y)\) / `ie_z` | donor/base 轨迹 `answer` 皆为约束赋值 **「82」**（seed=0 同权重抽样，不是金答案 0）。intervene 主/对照/INLP/rescue/C-layer 抽取答案皆 **「9」**（`decode_ids([29,25,13,54])='=9-V'`），`followed_donor=false`。`ie_z=1{9==82}-1{9==82}=0`，`ie_z_g=target_follow`。库函数隐向量均值 **未被** CLI tiny 路径写入 |
| X24 | INLP hook 不是 swap | 间谍 `out == in @ P`，`out ≠ swap`。CLI `mode="inlp"`。2 点拟合 `inlp_rank=30` |
| X25 | 教师强制 / 采样 | `target_assignment='\nq = 82'`（t0p 为 `\nq = 53`）；`parse_status=constrained_target`；`correct=false`（金标 0）。6 条 `sampling={temperature:1.0,top_k:0,top_p:1.0}`。`decode_loop` 用独立 `Generator`，不用 `HF generate`。intervene decode **不再**教师强制 |
| X26 | 问句单独解析 | 对 6 条 `prompt_text` 跑 `parse_events` 会打出 p1/p2（source 问句只有 p1，因 `p2` 已改名为 `p2_src`）。generate **不解析问句**，故这些不是生成事件 |
| X27 | 卡片 revision | `qwen3-8b` `b968826d9c…` think `(151667,151668)`；`r1-distill-qwen-7b` `916b56a4…` think `(151648,151649)`。本机未加载 |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验卡片 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server`。本轮不要求自然 CoT |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存；CLI 未调用。属 `pending_server`。tiny **不是** MODEL-01 |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机是接口证明 |
| 把 156 passed 写成 Goal / MODEL-01 验收 | 绿测试不是论文正确性 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

`ISSUES.md` 只当作者主张。

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| A10-04 Plus family persist-lock | `splits.py` / 磁盘并集 | **不裁定。** 非本通道猎项；未读 A/B 报告 |
| C6-M-01 / F10 first-seen | 无 `tasks.jsonl` → fit/calibrate 失败 | **不裁定。** C/E/F |
| B9-01 sham `noise_ref` | 只在 `sham:` | **不裁定。** B 列 |
| F6-04 / 标量 Prefill | `_hidden_is_prefill` 拒 `0`/`True`/`[0]` | **指定路径独立关闭。** X19 |
| E7-19 / C7-M-02 / C7-M-03 / B5-01/05 | T3 prepare、假 P1、`n<d`、改名表达式 | **不裁定。** 非本通道 |
| 先前 D7/D10/D11 生成区事件、有限 \(H\)、donor 身份、INLP/C-rand/rescue/`ie_z`、几何 timing | 须在 `0816fa5b…` 上重核 | **独立关闭（指定路径，本轮 MATCH 树）。** X8e、X14c/d、X22–X25 |
| pending_server | 真实权重 / 50 条 C2 / 官方 CoT | **同意未关。** 约束 `q` 不是 §4.1；tiny 不是 MODEL-01 |
| Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |

## 6. 发现

### D13-00 — 声称冻结 hash 对交卷磁盘不成立

- **状态：** confirmed defect（过程 / QA-01）
- **严重度：** high
- **文件 / 符号 / 行号：** `.planning/audits/round-13/VERSION.md` 声称 61 文件 / `0816fa5b…93de3b`；交卷磁盘 61 文件 rel+NUL+bytes = `1f61fd06…b91637`
- **触发条件：** 按 VERSION 脚本在开审、成文后、交卷前各复算
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。开审 MATCH。窗口内 `cli.py` mtime 02:38:44（61130 B / `175abf12…` → 60895 B / `779cedd3…`）；`tests/test_round07_regressions.py` mtime 02:38:53。本通道未改这些文件。D 核心 `collect.py` `83658cd8…`、`generate.py` `07493570…`、`interventions.py` `0ffdbb88…`、`repair.py` `f76ff999…`、`tiny.py` `21725a18…` 开审=交卷。`cmd_intervene` 函数体与开审复跑一致。
- **影响：** 不能把本报告说成「已在声称快照 `0816fa5b…` 上签字」。猎项锚定开审 MATCH 之后立即复跑的磁盘行为。
- **建议：** 停写、重冻、审查者只对一个 hash 交卷。并行通道不得在审查窗口改冻结集合。

### D13-01 — 开审冻结可锚定；因果实现未在窗口内改写

- **状态：** closed / non-defect（开审树与 D 核心字节）
- **严重度：** n/a
- **证据：** X1 开审 MATCH；上列 D 核心哈希交卷未变。不因此放行 MODEL-01 或真实 C2，也不把交卷聚合写成 MATCH。

### D13-02 — 只解析生成区；事件 `start ≥` 问句；问句 p1/p2 不是生成事件

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **148–191**（`parse_events(generated)` 再 `+= len(prompt)`；`parse_region="generated"`；赋值落在 `gen_text` 之后则 `constrained_target`）；`cli.py` **292–302**
- **对应要求：** POS-01 下限；本轮猎项「generated-region events」
- **证据：** X8e、X22、X25、X26。6/6 轨迹事件节点皆 `q`，`start` 45 或 53，问句 36 或 44 字符。生成区 p1/p2 = 0。表面无金标注串 `p1 = 4 | p2 = 0 | q = 0`。问句单独解析会出 p1/p2，说明排除靠「不解析问句」，不是问句里没有赋值。
- **影响：** 指定路径不再把 prompt 前提写进 \(H\) 行。这不是自然 CoT，也不声称 MODEL-01。

### D13-03 — \(H\) 全有限；不可表达 `start=0` 跳过；无 NaN pre_step 行

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **50–68**；`events.py` **251–257**
- **对应要求：** 可表达步前入 \(H\)；不可表达不塌成末 token
- **证据：** X8e、X8c、X8f、X10。科学 collect `H` 6×32，NaN 行 0；`H_pre_step/value/post` NaN 行 0。手工 `Event(start=0)` → `h_position=no_event`，`H.shape=(0,32)`，**不**塌成末 token。`boundary_index(...,0,"before")` 为 None。scientific `--backend offline` 拒绝把前缀 id 当 \(H\)。
- **影响：** 指定路径不是 `donor_missing` 的 NaN 矩阵。

### D13-04 — donor 来自 `source_value_pair` 的 `trace-base` / `trace-edit`，非全 NaN、非恒等 \(H\)

- **状态：** closed（点名配对） / residual（`same_value_diff_source` 未作第二 donor）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `cli.py` **384–397**（落盘 `trace_ids`）；**811–841**（`_load_source_value_pair` + `_pair_source_value`）；**844–867**（pair 优先；回退显式 `skip={"trace-t0p"}`）；`edits.py` **214–226**
- **对应要求：** CAUSAL-02「按 pair 取 donor」下限
- **证据：** X8e、X14c、X21。pair 元数据 `base→trace-base`、`same_source_diff_value→trace-edit`、`same_value_diff_source→trace-source`。选中行 `(0,2)`，\(\\|H_0-H_2\\|\approx 0.00430\)，`allclose=False`，两行有限。更大的 base–t0p 距离 0.00778 **未被选**。`trace-source` 已生成（\(\\|H_0-H_3\\|\approx 0.00832\)）但配对函数只吃 `same_source_diff_value`。`trace-edit` 与 `_allowed_edits` 的 `p2:2` 问句/赋值/seed 全同，是默认编辑撞车，不是本对 donor 恒等。
- **影响：** 同题 seed0/seed1（t0p）不再冒充来源-数值 donor。这仍不是 50 条 C2 同批次完成。

### D13-05 — INLP 是 \(h@P\)；C-rand `add_delta`；rescue `replace`；`ie_z` 为 target-follow \(g(Y)\)；有分数则弱层 `add_delta`

- **状态：** closed（点名接线） / residual（弱层 \(H\) 未另采；helper `ie_z` 仍是向量差；结局通道不是教师强制 \(q\)）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `collect.py` **189–208**；`cli.py` **915–984、966–967**；`interventions.py` **31–49、52–67、88–89**
- **对应要求：** CAUSAL-01 接线；INLP-01 下限；IE-01 接线；论文 §2.4
- **证据：** X11、X12、X14c、X14d、X23、X24。hook 间谍 `out = in @ P` 且 \(\neq \Pi_Z\)。无 flag：4 次 decode `(pi_z_swap,1)/(add_delta,1)/(inlp,1)/(replace,1)`。有 flag：5 次，键集合恰好 `{(pi_z_swap,1),(add_delta,1),(add_delta,0),(inlp,1),(replace,1)}`。C-rand / C-layer 的 `delta` 与独立 `c_rand_delta` / `c_layer_delta` 对拍，范数锁到主干预 \(2.4187\times 10^{-4}\)。rescue 是 `replace`，不是再 swap。落盘 `ie_z=0.0` ≠ helper \(4.91\times 10^{-5}\)；`ie_z_g=target_follow`。\(g=1\) 当 `extract_answer(generated)==donor_ans`。本机 donor_ans=82、主/基线皆为 9。
- **残留：** C-layer 的 \(\Delta\) 仍用 **readout 层** 的 base/donor（collect 层 1），只是施加在弱层 0。`ie_z()` 库函数仍是均值差，仅 CLI tiny 路径改 \(g(Y)\)。intervene 的 generated 是无约束 4 token，不是被强制的 `\nq =`。
- **影响：** r07「C-rand 零次 decode / 弱层仍是 swap / INLP 再跑 \(\Pi_Z\)」在指定路径上不成立。tiny 上 0 且无 follow 按口令为诚实，不得写成论文来源跟随。

### D13-06 — 几何 `timing` 保持 `offline_hidden`，未写成 live `pre_step`

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **914、1006**；`collect.py` **227**（hook 内部 `timing`）
- **证据：** X14c、X14d、X8g、X8h。jsonl 顶栏 `timing=offline_hidden`。`relative.hook_timing=pre_step` 仅表示 `event_aligned=True` 时 hook 打在事件步前前缀上，前缀是 `text[:45]` 的 **re-encode**，不是原生成 KV 续写。collect \(H\) 与前缀末 token 一致，与生成 ids 有 8 处不同。
- **影响：** 不得把 tiny 路径写成「已做 live 步前 hook」。本机接口是离线隐状态几何 + 二次前向 hook。

### D13-07 — Prefill：真实 32-d tiny hidden 接受；`0`/`True`/`1.0`/`[0]`/`[]` 拒绝

- **状态：** closed（接口） / residual（`extra=32` 与不落盘向量）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `repair.py` **14–23、159–173**；`cli.py` **1048–1050**
- **对应要求：** REPAIR-01「有限 hidden 才能 `refilled_prefix`」；F6-04
- **证据：** X19。`isinstance(..., bool)` 先拒；`0`/`1.0` 走 `ndim==0`；`[0]`/`[]` 走 `size<2`。`run_repair` 对上述值写 `prefill_unavailable`，即使 execute 谎称 `refilled_prefix=True`。真实 `execute_repair_tiny` 给出 32 维有限向量后 `status=ok`。scientific CLI k=1..5 全部 `refilled_prefix=True`。
- **影响：** 标量/`[0]` 不再能把修复标成已 Prefill。

### D13-08 — 教师强制 `q` 诚实为 `constrained_target`；不得写 MODEL-01 / §4.1

- **状态：** closed（诚实标签） / non-defect（tiny 边界） / residual（模板未接入）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **72–98、157–158、181–191**；`adapters.py` **32–42**
- **证据：** X15、X25、X27。`append_target_assignment` 写 `\nq = ` 再从 logits 采两位数字，注释写明 Not gold values。6 条 `parse_status=constrained_target`，`correct=false`。金标 0，写出 82/53。`apply_model_template` 不被 CLI/`generate_task_trace` 调用。卡片 `think_ids` 只在未调用的 `load_frozen` 路径。
- **影响：** 本机可解析接口成立。把这条轨迹写成自然 CoT、官方模板对齐或 MODEL-01 **是缺陷**；当前代码与元数据没有那样写。本轮不要求发明自然 CoT。

### D13-09 — nontarget/invalid 字段已接线；本机取值不能当机制结果

- **状态：** closed（schema / 相对对照） / residual（通道与 identifiability）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `cli.py` **952–967、985**；`interventions.py` **98–115**
- **证据：** X14c、X14d、X23、X25。有分数时四项相对 `vs_crand`/`vs_clayer` 均为 0.0（主与两对照答案都是 `"9"`）。无分数时相对四项 null（C-layer 未 decode）。`invalid=0` 因为垃圾 decode `=9-V` 仍能抽出数字。`nontarget` 定义为「答案=轨迹 answer 且 ≠ donor」；本机 base/donor 轨迹 answer 皆为同一 `seed=0` 教师强制 `"82"`，该比特结构上不能为 1。金标任务值 0 从未进入 `_outcomes`。
- **影响：** 不得把四项 0 写成「无目标跟随」的科学结论。`acknowledged_effect=relative_to_controls_only` 诚实。CAUSAL-02 实测结局保持 `pending_server`。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载；本轮不要求自然 CoT |
| U-02 | `replace` 用参数名 `delta` 传入救援向量 | 调用与实现一致 |
| U-03 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够；生产路径不调用 |
| U-04 | Prefill hidden 用最后一层而非 readout | 口令是「有 hidden」；X19 已满足 |
| U-05 | re-encode 与生成 ids 在乱码段的 8 处不一致 | 作者把 re-encode 当作修复；tiny 字级词表下是二次教师强制；支持「非 live KV」 |
| U-06 | `_load_source_value_pair` 依赖兄弟目录名 `prep`/`prepare`/`s-prep` | 指定路径 `s-prep`/`s-col` 找到 pair |
| U-07 | `_expressible_donor` 在 pair `allclose` 时回退 | 本机 base/edit 互异，未触发 |
| U-08 | C-layer 把读出层 \(\Delta\) 加到弱层 residual | 猎项只要求 `c_layer_delta`+弱层 `add_delta`，已对拍 |
| U-09 | `extra_prefill_tokens` 恒 32（`ids[:32]`）且不落盘 hidden | 旗标与拒绝规则已核；声称可审计表征时再升格 |
| U-10 | 全文三事件里 p1 不入 \(H\) | 步前不可表达；科学路径只采生成区 `q` |
| U-11 | rescue 向量范数等于 \(\\|H_{\mathrm{base}}-H_{\mathrm{edit}}\\|\)（0.00430）而非主干预范数 | 猎项只要求 `mode=replace`；未写成范数匹配缺陷 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是 MODEL-01**（本轮不要求） |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 五模式独立 decode 与指定路径接线 | 无真实来源-数值 donor；本机 \(g(Y)\) 无跟随 |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta` 在一维标准正交基下正确 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、只改层 2 last-token；`finally` 含异常路径清理 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`；`enable_thinking` 仅在 `model_kind=="qwen3"` 传入 |
| N-04 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `token_ids` / `stop_reason` / `sampling` |
| N-05 | 关闭 | 几何 `timing` 保持 **`offline_hidden`**；`relative` 含 `hook_once=resid_post` 与 `transform=pi_z_swap` |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数 |
| N-07 | 关闭 | 跨界 token 不进入 `token_index`；`leaks_target` 在 straddling 时可为 True |
| N-08 | 关闭 | `extract_answer` 去掉闭合 think；未闭合返回 None |
| N-09 | 关闭（选项） | `resid_post_hook(..., once=True)` 在 decode 中只生效一次 |
| N-10 | 关闭（功能） | `clone_cache` 隔离存储并保留 `seq_length`；步进路径未接入 |
| N-11 | 过程 | 开审 hash MATCH；交卷前 MISMATCH（D13-00）。不得写成 HASH_MATCH |
| N-12 | 非缺陷 | `--backend offline` 的 \(H\) 是前缀 id；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 是随机初始化隐状态并标注 `random_init`。**不是 MODEL-01**；本轮不要求 MODEL-01 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 无 `--dev-layer-scores` 时 `clayer_status=dev_scores_missing` |
| N-16 | 关闭 | scientific `q` 步前入 \(H\)；不可表达步前不入；空事件 `no_event` |
| N-17 | 关闭 | 主 hook 变换是 \(\Pi_Z\)；前缀是 `text[:event.start]`（本机 45 token）；主层 readout **1** |
| N-18 | 关闭 | `execute_repair_tiny` 重新 Prefill；dummy/offline/`0`/`True`/`1.0`/`[0]`/`[]`/`prefix_token_ids` 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| N-20 | 关闭（本轮猎项） | 生成区事件；有限 \(H\)；donor=`same_source_diff_value`；INLP=\(h@P\)；C-rand/rescue/C-layer 独立 decode；`ie_z` target-follow 且 0 诚实；几何 `offline_hidden`；Prefill 拒 `0`/`True`/`1.0`/`[0]`/`[]`；`constrained_target` 诚实 |
| N-21 | 非缺陷（本轮口径） | 不要求自然 CoT；约束 `\nq = ` 两位数字不是 §4.1 |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` 无生产调用方 |
| S-03 | stub | `inlp_remove` 有 decode；`relative` 无 INLP 四项结局，只有 `inlp_followed_donor` |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道不通过（FAIL）。冻结：HASH_MISMATCH。指定猎项在开审 MATCH 窗口的独立复跑上全部关闭。tiny 不是 MODEL-01；自然 CoT 不是本通道通过条件。不宣布 Goal 完成。不得启动连续通过计数。**

开审复算冻结为 `0816fa5b…`（61，MATCH）。随即在该窗口对 `tests/fixtures/t1_tiny.json` 跑 scientific `prepare --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15` → `collect --backend tiny --weight-seed 0` → `intervene --backend tiny` → `intervene --dev-layer-scores 0.05 0.9 0.8` → `repair --eval-mode scientific --mask task_oracle`，并用 monkeypatch 记录每一次 `intervene_hidden_decode`。交卷再算同一脚本为 `1f61fd06…`。核验：

1. **生成区事件：** 6/6 `parse_region=generated`，仅生成区 `q`，`start` 不落入 prompt；问句 p1/p2 不是生成事件。
2. **有限 \(H\)：** `(6,32)` 全有限，与 `event_rows` 对齐；`start=0` 跳过；scientific 拒绝 offline 前缀 id。
3. **donor：** `same_source_diff_value`，行 `(0,2)` = `trace-base`/`trace-edit` 的 `q`，**不是** `trace-t0p`；\(\\|H_0-H_2\\|\approx 0.00430\)（有限、非恒等）；`trace-source` 已写入 pair。
4. **INLP：** `mode=inlp`，\(h@P\)，无 donor，rank 30，与 \(\Pi_Z\) 不是同一变换。
5. **独立 decode：** 无 flag 四次（swap / C-rand `add_delta` / INLP / rescue `replace`）；有 flag 五次，C-layer 在弱层 0 用对拍过的 `c_layer_delta`。
6. **`ie_z`：** `target_follow`；本机无 follow，值为 **0**，按口令记为诚实。
7. **几何 timing：** 顶栏保持 **`offline_hidden`**；不得写成 tiny 上的 live `pre_step` hook。
8. **Prefill：** `0` / `True` / `1.0` / `[0]` / `[]` 拒绝；scientific repair k=1..5 有真实 32 维 hidden。
9. **教师强制：** 6/6 `constrained_target`；不是 §4.1，也不是 MODEL-01。

这些仍不够支持把本报告签在声称快照 `0816fa5b…` 上：交卷磁盘是 `1f61fd06…`。也仍不够支持把指定路径写成论文同批次交换/消融/救援实验结果：五种模式都抽出 `9`，相对对照为 0，donor 轨迹答案是约束 `"82"` 不是金标 0。诚实的 tiny 接线证明 ≠ MODEL-01 / CAUSAL-01/02 完成。真实 HF / 官方 dump / CUDA / 50 条 C2 保持 `pending_server`。
