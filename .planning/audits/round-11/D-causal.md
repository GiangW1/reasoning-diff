# D-causal 独立审查报告（round-11）

通道 D：模型与因果（tiny generate/collect/hook、三时机、swap \(\Pi_Z\)、C-rand/C-layer、INLP/rescue、来源-数值、Prefill KV、权重 seed）。指定复跑 scientific `prepare`→`collect --backend tiny`→`intervene --backend tiny`（另跑 `--dev-layer-scores 0.05 0.9 0.8`）→`repair --eval-mode scientific`。本轮猎单（只作猎单，不作他通道证据）：生成区事件、有限 \(H\)、donor `source_value_pair`、INLP \(h@P\)、C-rand/rescue/C-layer **独立 decode**、`ie_z` target-follow（tiny 上 0 且无 follow 视为诚实）、Prefill 拒绝 `0`/`True`/`[0]`。**不要求**自然 CoT，**不把** tiny 随机权重写成 MODEL-01。

独立性声明：未阅读 round-11 其他通道报告；只把 `.planning/audits/round-11/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账。`.planning/audits/round-09/D-causal.md` 只作报告体例与猎单对照，不作本轮证据。结论以本机当前磁盘与本轮复跑为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试通过当作论文正确性；不把作者 `local close` 或声称 155 passed 当作本通道关闭。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。诚实的 `offline_prefix_ids` 在未被宣称为隐状态时不记缺陷。

对照原文：论文 §2.4（交换公式、前瞻定位、C-rand/C-layer 同批次）、§4.2（步前/值前/步尾）、§6（来源—数值 / 交换 / Knock-out / Rescue）、§8；`docs/EXPERIMENT_PROTOCOL.md` §4；REQUIREMENTS MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01。tiny 路径只验收接口与接线，不验收 MODEL-01。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T02:26:00+08:00 开审；交卷约 2026-09-21T02:38:00+08:00 |
| 声称冻结 hash | `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`（`.planning/audits/round-11/VERSION.md`；61 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **开审 MATCH。交卷 HASH_MISMATCH。** 开审按 VERSION 脚本逐字复算得 **61** 文件 / `7518e20be988ca76de910ed5b88ff5b9cba4a486ba185d70a94b50b37b28e689`。审查中同一脚本再算：`4da0b2bd42dae62f0bd693751119c135ced4845eed2c631915cf084618d2dd04` → `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`；成文后再算 **61** 文件 → `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。窗口内他方改写至少 `cli.py`、`measure.py`、`splits.py`、`tests/test_round07_regressions.py`、`tests/test_review_regressions.py`。本通道未改冻结集合。因果猎项锚定**开审 MATCH 之后立即复跑的磁盘行为**；声称冻结对交卷字节不成立 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；审查对象是冻结脚本覆盖文件的当前字节） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| 作者 pytest 声称 | 155 passed。本通道只重跑 tiny/因果相关子集（**63 passed / 18.55s**），不把 155 记为已验证 |

D 核心指纹（交卷时；mtime 均早于或等于开审阅读，`cmd_intervene` 函数体与开审阅读一致，仅 `cli.py` 行号因他处插入下移 3 行）：`models/collect.py` `83658cd8…`、`models/generate.py` `07493570…`、`interventions.py` `0ffdbb88…`、`repair.py` `f76ff999…`、`edits.py` `cacb63ac…`。`cli.py` 交卷 `175abf12…` / 61130 B / mtime 02:30:09。

## 2. 范围与逐文件覆盖

指派阅读并核对（行号为交卷时当前磁盘；`cmd_intervene` 相对开审下移 3 行）：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / `think_ids` / `load_frozen(..., local_files_only=True)` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids` / `readout_layer_index`（60%–75% 带） / `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–261 | `collect_hidden_trace` 跳过不可表达 `pre_step`；空事件 `no_event`；`collect_tiny`；`intervene_tiny`；**`intervene_hidden_decode` 四模式** `pi_z_swap` / `inlp`(\(h@P\)) / `add_delta` / `replace` |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–201 | `sample_next`；`decode_loop`；`append_target_assignment`；`generate_task_trace`（只解析生成区；`parse_region=generated`）；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / INLP / `rescue_controls` / `select_weak_layer` / 库函数 `ie_z`（隐向量均值） / `intervention_report` |
| `src/reasoning_diff/edits.py` | 214–226 | `make_source_value_pair`：value 臂 + rename 臂 |
| `src/reasoning_diff/repair.py` | 1–232 | `_hidden_is_prefill` 拒绝标量/bool/`[0]`；`execute_repair_tiny` Prefill hidden+KV；`run_repair` |
| `src/reasoning_diff/cli.py` | 1–1255 | 重点 `cmd_prepare` 257–438（scientific 生成 `trace-base`/`trace-t0p`/`trace-edit`/`trace-source`）、`cmd_collect` 440–547、`_try_source_value_pair` 676–689、`_load_source_value_pair` 811–818、`_pair_source_value` 821–841、`_expressible_donor` 844–867、`cmd_intervene` 870–1013、`cmd_repair` 1016–1056 |
| `src/reasoning_diff/executor.py` | 1–109 | `IsolatedExecutor` unavailable；`ChildProcessExecutor.isolated_sandbox=False` |
| `src/reasoning_diff/rng.py` | 41–53 | `StreamBank` 名 `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/events.py` | 27–89、251–274 | `parse_events`；`boundary_index`；`extract_answer` 去 think |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理 |
| `tests/test_tiny_cache.py` | 1–26 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 全文件 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | scientific prepare/collect/repair 相关 | 生成区；offline 拒绝；Prefill |
| `tests/test_round05_regressions.py` | scientific 事件 / 几何 timing / repair k |
| `tests/test_round06_regressions.py` | 有限 \(H\) + `donor_kind`/`inlp`/`add_delta`/`replace`/`ie_z_g` |
| `tests/test_round07_regressions.py` | `0`/`True`/`[0]` Prefill；T3 跳过 pair（窗口内被他方改写，**不**作通过证据） |

支持性阅读：`schema.py` `POSITION_KINDS`；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` 上列要求。未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次、自然 CoT。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`、`measure.py`（B 列）。`cli.py` 校准/fit 段属其他通道。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | 开审 **MATCH** `7518e20b…b28e689`（61）。交卷 **HASH_MISMATCH** 61 文件 / `0816fa5b…93de3b`（中间还见 `4da0b2bd…` / `598e6c8f…`）。见 D11-01 |
| X2 | pytest tiny/因果相关子集 | **63 passed / 18.55s**（`test_tiny_hooks`、`test_tiny_cache`、`test_generate_loop`、`test_round04/05/06/07_regressions`）。通过只证明冒烟与回归锁，不是论文正确性 |
| X3 | `apply_swap` 与标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.168\)、\(\Delta V_{\max}=0.387\)，且 **仅 last token**（earlyK=0） |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3** 次；`once=True` **1** 次 |
| X7 | hook `finally` 清理 | 新鲜模型上 `RuntimeError` 后 `_forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)` |
| X8b | `collect_hidden_trace` + 全文 `"p1 = 4\\np2 = 0\\nq = 0\\n"` | `parse_events` 跨度 **p1 0–6 / p2 7–13 / q 14–19**（`status=ok`）。\(H\) `(2,32)`：p1 步前不可表达（limit=0 无 fully-before token），正确跳过。**不是缺陷** |
| X8c | 空事件库层 | `h_position=no_event`，\(H\) `(0,32)`，不塌成末 token |
| X8e | **指定** scientific `prepare`→`collect --backend tiny` | 6 条轨迹：`trace-base` / `trace-t0p` / `trace-edit` / `trace-source` / 两条 extra value-edit。每条 **1** 个生成区 `q`（base/edit `start=45,end=51`；source `53–59`；`parse_region=generated`，`parse_status=constrained_target`）。问句前提不进入事件。`H` `(6,32)` **6/6 行有限**（0 NaN），`event_rows.jsonl` 6 行皆 `{node_id:q, trace_id:…}`。`hidden_layer=1`；`weight_source=random_init`；`weight_seed=0`。\(\|H_0-H_1\|\approx 0.00778\)（base vs t0p），\(\|H_0-H_2\|\approx 0.00430\)（base vs edit） |
| X8f | scientific collect 拒绝 | `--backend offline` → `scientific collect refuses offline_prefix_ids as H` |
| X8g | re-encode vs 生成 ids | 每条轨迹与 `encode_text(text)` 有 **8** 处不同（恰 `max_new=8` 乱码段）。collect 的 \(H\) 是对表面文本的二次前向 |
| X9 | `leaks_target` 能否为 True | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None` |
| X10 | `boundary_index(..., 2)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 1 |
| X11 | INLP / rescue 算法 | `rescue([1,0],[0,1])=[1,1]`。库层 `inlp_remove` 与 `apply_swap` 在随机向量上最大差 **1.19**（不是同一变换）。库函数 `ie_z` 仍是隐向量均值；**CLI tiny 路径不再调用它** |
| X12 | C-rand / C-layer 范数与弱层 | 缺范数仍 `ValueError`（`C-rand requires the actual main-intervention norm`）。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0`。三项范数经 `scale_to_norm` 锁成同一 `main_norm` |
| X13 | StreamBank vs hook 基 | `direction` 第一抽 113750710（丢弃）；第二抽 **basis_seed=1153799966**。`sample` 第一抽 **1191642646**。`perturb` 17172908 |
| X14a | `intervene_tiny` swap 是否施加 | `transform=pi_z_swap`，logits \(\Delta_{\max}=0.512\)，cache 对象隔离，层 1 |
| X14c | **指定** scientific collect→intervene（**无** `--dev-layer-scores`） | `_pair_source_value` 返回 **`(0, 2, same_source_diff_value)`** = `trace-base` / `trace-edit` 的同身份 `q`（**不是** `trace-t0p`）。`status=prospective_decode`，几何 **`timing=offline_hidden`**。`relative.hook_once=resid_post`，`transform=pi_z_swap`，`hook_timing=pre_step`（hook 内部标签，几何字段未改写）。monkeypatch 记录 **4** 次 `intervene_hidden_decode`：层皆 **1**，模式 **`pi_z_swap` / `add_delta` / `inlp` / `replace`**，`hook_fired=true`。INLP **无 donor**、有 `projector`。`clayer_status=dev_scores_missing`（无弱层 decode）。`ie_z=0.0`，`ie_z_g=target_follow`。对照四项因 clayer 空而 **null** |
| X14d | 另跑 `--dev-layer-scores 0.05 0.9 0.8` | **5** 次独立 decode，层 **1 / 1 / 0 / 1 / 1**，模式 **`pi_z_swap` / `add_delta`(C-rand) / `add_delta`(C-layer) / `inlp` / `replace`**。`clayer_status=dev_weak_layer_decode`，`weak_layer=0`。C-rand `delta` 头 4 维与独立重算 `c_rand_delta` **相等**；弱层 `delta` 与独立重算 `c_layer_delta(..., rng(5+0))` **相等**。三项范数与落盘一致（\(2.4187\times 10^{-4}\)）。`inlp` projector `(32,32)` rank 30；随机向量上 \(h@P\) 与 `apply_swap` 最大差 **1.87**。`rescue` 为 `replace`。相对四项 `vs_crand=vs_clayer=0.0` |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 内数字 → 7；未闭合 → None；`</think>` 后 boxed/#### → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 无调用**。本轮不要求自然 CoT |
| X16 | `clone_cache` / DynamicCache | clone ≠ 原对象；`data_ptr` 不同；`add_` 后原张量不变；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.746\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False` |
| X19 | Prefill | `execute_repair_tiny` 返回 32 维有限 `prefill_hidden`，`refilled_prefix=True`。`_hidden_is_prefill` / `run_repair(execute=…)` 对 **`0` / `True` / `[0]`**（以及 `1.0` / `[]` / `None` / `"x"` / `False`）一律 `refilled_prefix=False`、`status=prefill_unavailable`。`prefix_token_ids` 旁路同样诚实失败。scientific CLI repair：k=1..5，五条皆 `refilled_prefix=True`、`status=ok`、`gated=False`、`extra_prefill_tokens=32` |
| X20 | `weight_seed` | 同 seed 同 ids → \(\|\Delta H\|=0\)；异 seed → 0.194；同 seed 异 ids → 0.199。CLI collect 写入 spec `weight_seed=0` |
| X21 | 来源-数值 | `edits.jsonl` 含 `kind=source_value_pair`：targets=`["q"]`，nontargets=`["p1"]`，`trace_ids={base:trace-base, same_source_diff_value:trace-edit, same_value_diff_source:trace-source}`。donor 行是 base/edit，kind=`same_source_diff_value`。`make_source_value_pair` 改写图：`p1 * p2_src`，parents 不含 `p2`。`_try_source_value_pair` 对 T3 / paragraph 返回 None |
| X22 | 事件跨度 / hook 前缀 | 生成区 `q` 跨度 45–51，前缀 45 token；`ids[:64]` **未截断**（`prefix_truncated=false`） |
| X23 | \(g(Y)\) / `ie_z` | donor/base 轨迹 `answer` 皆为约束赋值 **「82」**（seed=0 同权重抽样，不是金答案 0/8）。intervene 主/对照/INLP/rescue 抽取答案皆 **「9」**，`followed_donor=false`。`ie_z=1{9==82}-1{9==82}=0`，`ie_z_g=target_follow`。**本轮口径：0 且无 follow 为诚实。** 库函数隐向量均值（对照 0.1）未被 CLI tiny 路径写入 |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server`。本轮不要求自然 CoT |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存。属 `pending_server`。tiny **不是** MODEL-01 |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机是接口证明 |
| 全量 pytest（作者称 155） | 本通道只重跑 tiny/因果相关 63 项；不把未跑项记为通过 |
| 窗口内被改写的 `tests/test_round07_regressions.py` 作为通过证据 | 他方改写；Prefill 拒绝已由本通道直接调用 `run_repair` 独立核验 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| F6-04 residual | 标量/`[0]` Prefill 拒绝 | **指定路径关闭。** `_hidden_is_prefill(0/True/[0])` 为 False；`run_repair` 写 `prefill_unavailable`（X19） |
| D7-03 | donor 优先 `source_value_pair.trace_ids` 的 `trace-base`/`trace-edit` | **指定路径关闭。** `(0,2)` / `same_source_diff_value`，不是 t0p（X8e、X14c、X21） |
| D7-04 | INLP 是 \(h@P\)；rescue 是 replace；`ie_z` 用 target-follow \(g(Y)\) | **接线关闭。** 第三次（无 flag）/第四次（有 flag）decode `mode=inlp` 且无 donor；rescue `mode=replace`；`ie_z_g=target_follow`。tiny 上 0 为诚实无 follow（X14c/d、X23） |
| D7-05 | C-rand 必跑 `add_delta` decode；C-layer 用 `c_layer_delta` 在弱层 `add_delta` | **指定路径关闭。** 无 flag 亦有 C-rand `add_delta`；有 flag 弱层 0 的 `delta` 与 `c_layer_delta` 对拍（X14c/d） |
| D7-01 / 过程冻结 | 声称 hash 交卷前漂 | **本轮重现。** 开审 MATCH，交卷 MISMATCH（X1、D11-01） |
| pending_server | 真实权重 / Linux cgroup / 实测 P1–P3 | **同意未关。** tiny 随机权重不是 MODEL-01；本轮不要求 MODEL-01 |
| A5-14 Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |
| B9-01 / C 列 / E 列 | 非本通道 | **不裁定。** 未读其他 r11 报告 |

## 6. 发现

### D11-01 — 声称冻结 hash 对当前磁盘不成立

- **状态：** confirmed defect（过程 / QA-01）
- **严重度：** high
- **文件 / 符号 / 行号：** `.planning/audits/round-11/VERSION.md` 声称 61 文件 / `7518e20b…b28e689`；交卷磁盘 61 文件 rel+NUL+bytes = `0816fa5b…93de3b`
- **触发条件：** 按 VERSION 脚本在开审、审查中、成文前后各复算
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。开审 MATCH。窗口内 `cli.py` mtime 02:30:09；其后 `splits.py`（02:32:06）与 `tests/test_round07_regressions.py`（02:32:14）再被改写；`measure.py`、`tests/test_review_regressions.py` 亦被他方改写。本通道未改这些文件。审查中至少观察到四个不同的 61 文件 digest（`7518e20b…` / `4da0b2bd…` / `598e6c8f…` / `0816fa5b…`）。
- **影响：** 不能把本报告说成「已在声称快照 `7518e20b…` 上签字」。D 核心（`collect.py` `intervene_hidden_decode`、`cmd_intervene` 函数体、指定路径复跑）与开审阅读一致，但冻结契约破了。
- **建议：** 停写、重冻、审查者只对一个 hash 交卷。并行通道不得在审查窗口改冻结集合。

### D11-02 — 生成区事件（猎项关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **148–191**；`cli.py` **292–302**
- **对应要求：** POS-01 下限（步前特征来自目标事件）；本轮猎项「generated-region events」
- **证据：** X8e。6/6 轨迹 `parse_region=generated`，`parse_status=constrained_target`，事件均为生成区 `q`，`start >= len(prompt_text)`。表面无金标注串 `p1 = 4 | p2 = 0 | q = 0`。问句里的 `p1`/`p2`/`q = p1 * p2` 不进入 scientific 事件。
- **影响：** 指定路径不再把 prompt 赋值写进 \(H\) 行。这不是自然 CoT，也不声称 MODEL-01。

### D11-03 — 有限 \(H\)（猎项关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **51–63**；`cli.py` **463–505**
- **对应要求：** 可表达步前入 \(H\)；不可表达不塌成末 token
- **证据：** X8e、X8c、X8f。scientific tiny：`H` `(6,32)` 全有限，行数 = `event_rows`。空事件 `no_event` / `(0,32)`。scientific `--backend offline` 拒绝把前缀 id 当 \(H\)。
- **影响：** 指定路径不是 `donor_missing` 的 NaN 矩阵。

### D11-04 — donor 是 `source_value_pair`，不是 `trace-t0p`（猎项关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **292–302、387–396、821–841、844–856、891**；`edits.py` **214–226**
- **对应要求：** CAUSAL-02「按 pair 取 donor」下限
- **证据：** X8e、X14c、X21。prepare 写 `trace-source` 与 `trace_ids`。`_pair_source_value` 用 `base`×`same_source_diff_value`（`trace-edit`）。回退显式 `skip={"trace-t0p"}`。本机 `(0,2)`，kind 字符串恰为 `same_source_diff_value`，node 皆 `q`。
- **影响：** 同题 seed0/seed1（t0p）不再冒充来源-数值 donor。这仍不是 50 条 C2 同批次完成。

### D11-05 — INLP 是 \(h@P\)，不是 swap（猎项关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **189–195**；`cli.py` **915、979–981**
- **对应要求：** INLP-01 接线下限（正交移除；本轮不要求四项结局块）
- **证据：** X14c、X14d、X11。`mode=="inlp"` 为 `vec @ proj`，调用不传 donor。projector `(32,32)` rank 30。同一随机向量上 \(h@P\) 与 `apply_swap` 最大差 1.87。落盘 `inlp_transform=inlp`。
- **影响：** 第二次前向不再是「再跑一次 \(\Pi_Z\)」。`relative` 仍无 INLP 四项结局，只有 `inlp_followed_donor`（S-03 stub，不重开本猎项）。

### D11-06 — C-rand / rescue / C-layer 是三次（或五次里的三次）独立 decode（猎项关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **968–984**；`collect.py` **197–208**；`interventions.py` **31–49**
- **对应要求：** 论文 §2.4；GOAL 同批次对照
- **证据：** X12、X14c、X14d。无 flag：4 次 decode `(pi_z_swap,1) / (add_delta,1) / (inlp,1) / (replace,1)`，弱层不 decode。有 flag：5 次，键集合恰好 `{(pi_z_swap,1),(add_delta,1),(add_delta,0),(inlp,1),(replace,1)}`。C-rand / C-layer 的 `delta` 与独立 `c_rand_delta` / `c_layer_delta` 对拍，范数锁到主干预 \(2.4187\times 10^{-4}\)。rescue 是 `replace`，不是再 swap。
- **影响：** r07「C-rand 零次 decode / 弱层仍是 swap」在指定路径上不成立。弱层施加的仍是读出层 \(\Delta\)（U-08），未升格。

### D11-07 — `ie_z` 是 target-follow；tiny 上 0 为诚实（猎项关闭）

- **状态：** closed / non-defect（本轮口径）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **952–967**
- **对应要求：** IE-01 接线；本轮明确「0 on tiny is honest if no follow」
- **证据：** X23、X14c。`ie_z_g="target_follow"`，值 = \(1\{\hat y=\text{donor\_ans}\}-1\{\hat y_0=\text{donor\_ans}\}\)，与库函数隐向量均值不同。本机 `followed_donor=false`，主/基线答案皆 `9`，donor 轨迹答案 `82`，故 `ie_z=0`。五种模式答案相同不是「伪造成功」，是随机权重下未跟随。
- **影响：** 不得把四项 0 或相对差 0 写成论文来源跟随结果。按本轮口令，这不重开 D7-04，也不记缺陷。

### D11-08 — Prefill 拒绝 `0` / `True` / `[0]`（猎项关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `repair.py` **14–23、159–173**；`cli.py` **1048–1050**
- **对应要求：** REPAIR-01「有限 hidden 才能 `refilled_prefix`」；F6-04
- **证据：** X19。`isinstance(True, bool)` 先拒；`0` 走 `ndim==0`；`[0]` 走 `size<2`。`run_repair` 对这三值（及 `1.0`/`[]`）写 `prefill_unavailable`，即使 execute 谎称 `refilled_prefix=True`。真实 `execute_repair_tiny` 给出 32 维有限向量后 `status=ok`。scientific CLI k=1..5 全部 `refilled_prefix=True`。
- **影响：** 标量/`[0]` 不再能把修复标成已 Prefill。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载；本轮不要求自然 CoT |
| U-02 | `replace` 用参数名 `delta` 传入救援向量 | 调用与实现一致 |
| U-03 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够 |
| U-04 | Prefill hidden 用最后一层而非 readout | 口令是「有 hidden」；X19 已满足 |
| U-05 | re-encode 与生成 ids 在乱码段的 8 处不一致 | 作者把 re-encode 当作修复；tiny 字级词表下是二次教师强制 |
| U-06 | `_load_source_value_pair` 依赖兄弟目录名 `prep`/`prepare`/`s-prep` | 指定路径 `s-prep`/`s-col` 找到 pair |
| U-07 | `_expressible_donor` 在 pair `allclose` 时回退 | 本机 base/edit 互异，未触发 |
| U-08 | C-layer 把读出层 \(\Delta\) 加到弱层 residual | 猎项只要求 `c_layer_delta`+弱层 `add_delta`，已对拍 |
| U-09 | 窗口内 `cli.py` 仍被他方改写 | `cmd_intervene` 函数体与开审复跑一致；记在 D11-01 |
| U-10 | 全文三事件里 p1 不入 \(H\) | 步前不可表达；科学路径只采生成区 `q`，不构成猎项失败 |

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
| N-11 | 过程 | 开审 hash MATCH；交卷前 MISMATCH（D11-01）。不得写成 HASH_MATCH |
| N-12 | 非缺陷 | `--backend offline` 的 \(H\) 是前缀 id；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 是随机初始化隐状态并标注 `random_init`。**不是 MODEL-01**；本轮不要求 MODEL-01 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 无 `--dev-layer-scores` 时 `clayer_status=dev_scores_missing` |
| N-16 | 关闭 | scientific `q` 步前入 \(H\)；不可表达步前不入；空事件 `no_event` |
| N-17 | 关闭 | 主 hook 变换是 \(\Pi_Z\)；前缀是 `text[:event.start]`（本机 45 token）；主层 readout **1** |
| N-18 | 关闭 | `execute_repair_tiny` 重新 Prefill；dummy/offline/`0`/`True`/`[0]`/`prefix_token_ids` 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| N-20 | 关闭（本轮猎项） | 生成区事件；有限 \(H\)；donor=`same_source_diff_value`；INLP=\(h@P\)；C-rand/rescue/C-layer 独立 decode；`ie_z` target-follow 且 0 诚实；Prefill 拒 `0`/`True`/`[0]` |
| N-21 | 非缺陷（本轮口径） | 不要求自然 CoT；约束 `\nq = ` 两位数字不是 §4.1 |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` 无生产调用方 |
| S-03 | stub | `inlp_remove` 有 decode；`relative` 无 INLP 四项结局，只有 `inlp_followed_donor` |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道不通过（FAIL）。冻结：HASH_MISMATCH。指定猎项在开审 MATCH 窗口的独立复跑上全部关闭。tiny 不是 MODEL-01；自然 CoT 不是本通道通过条件。**

开审复算冻结为 `7518e20b…`（61，MATCH）。随即在该窗口对 `tests/fixtures/t1_tiny.json` 跑 scientific `prepare --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15` → `collect --backend tiny --weight-seed 0` → `intervene --backend tiny` → `intervene --dev-layer-scores 0.05 0.9 0.8` → `repair --eval-mode scientific --mask task_oracle`，并用 monkeypatch 记录每一次 `intervene_hidden_decode`。核验：

1. **生成区事件：** 6/6 `parse_region=generated`，仅生成区 `q`，`start` 不落入 prompt。
2. **有限 \(H\)：** `(6,32)` 全有限，与 `event_rows` 对齐；scientific 拒绝 offline 前缀 id。
3. **donor：** `same_source_diff_value`，行 `(0,2)` = `trace-base`/`trace-edit` 的 `q`，**不是** `trace-t0p`；`trace-source` 已写入 pair。
4. **INLP：** `mode=inlp`，\(h@P\)，无 donor，rank 30，与 \(\Pi_Z\) 不是同一变换。
5. **独立 decode：** 无 flag 四次（swap / C-rand `add_delta` / INLP / rescue `replace`）；有 flag 五次，C-layer 在弱层 0 用对拍过的 `c_layer_delta`。
6. **`ie_z`：** `target_follow`；本机无 follow，值为 **0**，按口令记为诚实。
7. **Prefill：** `0` / `True` / `[0]` 拒绝；scientific repair k=1..5 有真实 32 维 hidden。

这些仍不够支持把本报告签在声称快照 `7518e20b…` 上：交卷磁盘是 `0816fa5b…`。微型随机权重不是真实 HF；指定路径上五种模式都抽出 `9`，相对对照为 0，不得写成论文同批次交换/消融/救援实验结果。诚实的 tiny 接线证明 ≠ MODEL-01 / CAUSAL-01/02 完成。
