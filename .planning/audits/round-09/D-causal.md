# D-causal 独立审查报告（round-09）

通道 D：模型与因果（tiny generate/collect/hook、三时机、swap \(\Pi_Z\)、C-rand/C-layer——弱层是对照不是主干预、INLP/rescue、来源-数值、Prefill KV、权重 seed）。指定复跑 scientific `prepare`→`collect --backend tiny`→`intervene --backend tiny`，并另跑 `--dev-layer-scores 0.05 0.9 0.8`。几何 `timing` 必须保持 `offline_hidden`，不得被 hook 改写成 `pre_step`。`relative` 须含 `hook_once`/`transform`。猎项（仅作猎单，不作证据）：D7-03 `donor_kind==same_source_diff_value`（不得用 `trace-t0p` 冒充）；D7-04 INLP 是 \(h@P\) 不是 swap，rescue 是 replace，`ie_z` 来自 \(g(Y)\) `target_follow`；D7-05 C-rand 必跑 `add_delta` decode，C-layer 用 `c_layer_delta` 在弱层 `add_delta`。微型随机权重 **不是** MODEL-01。

独立性声明：未阅读 round-09 其他通道报告；只把 `.planning/audits/round-09/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账。`.planning/audits/round-07/D-causal.md` **只作猎单**（D7-03/04/05），不作证据。结论以本机当前磁盘与本轮复跑为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试通过当作实现正确；不把作者 `local close` 或声称 144 passed 当作本通道关闭。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。诚实的 `offline_prefix_ids` 在未被宣称为隐状态时不记缺陷。

对照原文：论文 §2.4（交换公式、前瞻定位、C-rand/C-layer 同批次）、§4.2（步前/值前/步尾）、§6（V-Probing 时机；来源—数值 / 交换 / Knock-out / Rescue）、§8；GOAL §5.6–5.11、§5.13、§5.15；`docs/EXPERIMENT_PROTOCOL.md` §4；REQUIREMENTS MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T02:14:00+08:00 开审；交卷约 2026-09-21T02:21:00+08:00 |
| 声称冻结 hash | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（`.planning/audits/round-09/VERSION.md`；60 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **HASH_MISMATCH。** 开审按 VERSION 脚本逐字复算得 **60** 文件 / `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（MATCH）。审查中同一脚本再算：**61** 文件 → `57b43360…` / `fea2565f…` / `c29ad0dd…`；交卷前最后一次 **61** 文件 → `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`。新增 `tests/test_round07_regressions.py`；排除该文件后 60 文件仍 ≠ 声称 hash。窗口内 `cli.py`（增 `_try_source_value_pair`，`cmd_intervene` 行号下移）、`edits.py` / `events.py` / `repair.py` 等 mtime 被他方改写。本通道未改冻结集合。因果结论锚定**已复跑的磁盘行为**；声称冻结对交卷字节不成立 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；审查对象是冻结脚本覆盖文件的当前字节） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| 作者 pytest 声称 | 144 passed。本通道只重跑所引用子集（52 passed），不把 144 记为已验证 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对（行号为交卷时当前磁盘；`cmd_intervene` 相对开审下移）：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / `think_ids` / `load_frozen(..., local_files_only=True)` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids` / `readout_layer_index`（60%–75% 带） / `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–261 | `collect_hidden_trace` 跳过不可表达 `pre_step`；空事件 `no_event`；`collect_tiny`；`intervene_tiny`；**`intervene_hidden_decode` 四模式** `pi_z_swap` / `inlp`(\(h@P\)) / `add_delta` / `replace`；`intervene_swap_decode` 转调 swap |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–201 | `sample_next`；`decode_loop`；`append_target_assignment`；`generate_task_trace`（只解析生成区；`run_id` 写入轨迹）；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / INLP / `rescue_controls` / `select_weak_layer` / `ie_z`（库函数仍是隐向量均值） / `intervention_report` |
| `src/reasoning_diff/edits.py` | 204–226（现 214–226） | `make_source_value_pair`：value 臂 + rename 臂 |
| `src/reasoning_diff/repair.py` | 1–232 | `mask_prefix` / `execute_repair_tiny` Prefill hidden+KV / `run_repair`（无有限 hidden 不得 `refilled_prefix`） |
| `src/reasoning_diff/cli.py` | 1–1251 | 重点 `cmd_prepare` 257–438（scientific 生成 `trace-base`/`trace-t0p`/`trace-edit`/`trace-source`）、`cmd_collect` 440–543、`_try_source_value_pair` 674–687、`_load_source_value_pair` 808–815、`_pair_source_value` 818–838、`_expressible_donor` 841–864、`cmd_intervene` 867–1010、`cmd_repair` 1013– |
| `src/reasoning_diff/executor.py` | 1–109 | `IsolatedExecutor` unavailable；`ChildProcessExecutor.isolated_sandbox=False` |
| `src/reasoning_diff/rng.py` | 41–53 | `StreamBank` 名 `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/events.py` | 27–89、237–260 | `parse_events` match 跨度；`extract_answer` 去 think |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理（行为：摘钩后 logits 回基线） |
| `tests/test_tiny_cache.py` | 1–26 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | 25–137、218–220 | readout 带；scientific collect span；offline 几何≠`pre_step`；repair Prefill |
| `tests/test_round05_regressions.py` | 23–141 | scientific 事件；几何 timing≠`pre_step`；`hook_once`/`transform` |
| `tests/test_round06_regressions.py` | 37–79 | 有限 \(H\) + `donor_kind`/`inlp`/`add_delta`/`replace`/`ie_z_g` 回归锁 |

支持性阅读：`schema.py` `POSITION_KINDS`；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` 上列要求。未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`。`cli.py` 校准段与 `_find_tasks_jsonl` 属 E 列/路径发现，不作本通道通过项。窗口内新增的 `tests/test_round07_regressions.py` **未**纳入本通道通过证据。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | 开审 **MATCH** `9ffc4cd9…f619e10a4e582740fd6eb8d1b3bf20`（60）。交卷前 **HASH_MISMATCH** 61 文件 / `81308124…4b6d`。见 D9-01 |
| X2 | pytest tiny/因果相关子集 | **52 passed / 18.97s**（`test_tiny_hooks`、`test_tiny_cache`、`test_generate_loop`、`test_round04/05/06_regressions`）。通过只证明冒烟与回归锁，不是论文正确性 |
| X3 | `apply_swap` 与标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.168\)、\(\Delta V_{\max}=0.387\)，且 **仅 last token**（earlyK=0） |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3** 次；`once=True` **1** 次 |
| X7 | hook `finally` 清理 | 新鲜模型上 `RuntimeError` 后 `_forward_hooks` 为 0。`test_tiny_hooks` 摘钩后 logits 回基线 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)` |
| X8b | `collect_hidden_trace` + 全文 `"p1 = 4\\np2 = 0\\nq = 0\\n"` | `parse_events` 跨度 **p1 0–6 / p2 7–13 / q 14–19**（`status=ok`） |
| X8c | 空事件库层 | `h_position=no_event`，\(H\) `(0,32)`，不塌成末 token |
| X8e | **指定** scientific `prepare`→`collect --backend tiny` | 6 条轨迹：`trace-base` / `trace-t0p` / `trace-edit` / `trace-source` / 两条 extra value-edit。每条 **1** 个生成区 `q`（base/edit `start=45,end=51`；source `53–59`；`parse_region=generated`，`parse_status=constrained_target`）。`H` `(6,32)` **6/6 行有限**（0 NaN）。`event_rows.jsonl` 6 行，皆 `{node_id:q, trace_id:…}`。`hidden_layer=1`；`weight_source=random_init`；`weight_seed=0`。\(\|H_0-H_1\|\approx 0.00778\)（base vs t0p），\(\|H_0-H_2\|\approx 0.00430\)（base vs edit） |
| X8f | scientific collect 拒绝 | `--backend offline` → `scientific collect refuses offline_prefix_ids as H` |
| X8g | re-encode vs 生成 ids | 每条轨迹与 `encode_text(text)` 有 **8** 处不同（恰 `max_new=8` 乱码段）。collect 的 \(H\) 是对表面文本的二次前向 |
| X9 | `leaks_target` 能否为 True | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None` |
| X10 | `boundary_index(..., 2)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 1 |
| X11 | INLP / rescue 算法 | `rescue([1,0],[0,1])=[1,1]`。`rescue_controls` 给出 matched。库层 `ie_z(rescued, base)` 仍是隐向量均值（本机 \(\approx 0.00237\)），**CLI tiny 路径不再调用它** |
| X12 | C-rand / C-layer 范数与弱层 | 缺范数仍 `ValueError`（`C-rand requires the actual main-intervention norm`）。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0`；`{0:0.2,1:0.1,2:0.4}=1`。三项范数经 `scale_to_norm` 锁成同一 `main_norm` |
| X13 | StreamBank vs hook 基 | `direction` 第一抽 113750710（丢弃）；第二抽 **basis_seed=1153799966**。`sample` 第一抽 **1191642646**（现写入 decode `seed`）。`perturb` 17172908 |
| X14a | `intervene_tiny` swap 是否施加 | `transform=pi_z_swap`，logits \(\Delta_{\max}=0.512\)，cache 对象隔离，层 1 |
| X14c | **指定** scientific collect→intervene（**无** `--dev-layer-scores`） | `_pair_source_value` / `_expressible_donor` 返回 **`(0, 2, same_source_diff_value)`** = `trace-base` / `trace-edit` 的同身份 `q`（**不是** `trace-t0p`）。`status=prospective_decode`，几何 **`timing=offline_hidden`**。`relative.hook_once=resid_post`，`transform=pi_z_swap`，`hook_timing=pre_step`（hook 内部标签，几何字段未改写）。monkeypatch 记录 **4** 次 `intervene_hidden_decode`：层皆 **1**，模式 **`pi_z_swap` / `add_delta` / `inlp` / `replace`**，`hook_fired=true`，`event_aligned=true`，前缀 45 token。`clayer_status=dev_scores_missing`（无弱层 decode）。`ie_z=0.0`，`ie_z_g=target_follow`。对照四项因 clayer 空而 **null** |
| X14d | 另跑 `--dev-layer-scores 0.05 0.9 0.8` | **5** 次 decode，层 **1 / 1 / 0 / 1 / 1**，模式 **`pi_z_swap` / `add_delta`(C-rand) / `add_delta`(C-layer) / `inlp` / `replace`**。`clayer_status=dev_weak_layer_decode`，`weak_layer=0`。C-rand 的 `delta` 头 4 维与独立重算 `c_rand_delta` **相等**；弱层 `delta` 与独立重算 `c_layer_delta(..., rng(5+0))` **相等**。三项范数与落盘一致（\(2.4187\times 10^{-4}\)）。`inlp` **无 donor**、`projector` `(32,32)` rank 30；随机向量上 \(h@P\) 与 `apply_swap` 最大差 **1.22**（不是同一变换）。`rescue` 为 `replace`。相对四项 `vs_crand=vs_clayer=0.0`（不再 null）。cli.py 漂移后对同一 `s-col` 再跑一次，上述标签复现 |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 内数字 → 7；未闭合 → None；`</think>` 后 boxed/#### → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 无调用**。`from_pretrained` 仅在 `load_frozen` |
| X16 | `clone_cache` / DynamicCache | clone ≠ 原对象；`data_ptr` 不同；`add_` 后原张量不变；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states` 长度 4。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.746\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False` |
| X19 | Prefill | `execute_repair_tiny` 返回 32 维有限 `prefill_hidden`，`refilled_prefix=True`。dummy / `prefix_token_ids` 旁路 → `prefill_unavailable` / `refilled_prefix=False` |
| X20 | `weight_seed` | 同 seed 同 ids → \(\|\Delta H\|=0\)；异 seed → 0.197；同 seed 异 ids → 0.175。CLI collect 写入 spec `weight_seed=0` |
| X21 | 来源-数值 | `edits.jsonl` 含 `kind=source_value_pair`：`ssdv` 为 value 臂 `p2:0→2`，`svds` 为 rename `p2→p2_src`，`targets=["q"]`，`nontargets=["p1"]`，`trace_ids={base:trace-base, same_source_diff_value:trace-edit, same_value_diff_source:trace-source}`。`cmd_intervene` **读取** pair（`_load_source_value_pair` 经兄弟目录 `s-prep`/`prep`/`prepare`）。donor 行是 base/edit，kind=`same_source_diff_value` |
| X22 | 事件跨度 / hook 前缀 | 生成区 `q` 跨度 45–51，前缀 45 token；`ids[:64]` **未截断**（`prefix_truncated=false`）。问句前提不进入 scientific 事件 |
| X23 | \(g(Y)\) 实测 | donor/base 轨迹 `answer` 皆为约束赋值 **「82」**（seed=0 同权重抽样，不是金答案 0/8）。intervene 生成 4 token `=9-V`，`extract_answer`→`9`。五种模式与各自 baseline 的 `generated_ids` **完全相同** `[29,25,13,54]`，`followed_donor=false`。`ie_z=1{9==82}-1{9==82}=0`。落盘主/对照四项均为 target/nontarget/task_correct/invalid = 0/0/0/0（`9` 被当成合法数字，故 `invalid=0`） |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server` |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存。属 `pending_server` |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机是接口证明 |
| 全量 pytest（作者称 144） | 本通道只重跑 tiny/因果相关 52 项；不把未跑项记为通过 |
| 窗口内新增 `tests/test_round07_regressions.py` | 非本通道冻结声明的一部分；不引用为通过证据 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| D7-01 | 过程项：r07 声称 hash 交卷前已漂 | **本轮重现。** 开审 MATCH，交卷 MISMATCH（X1、D9-01）。不继承为已关 |
| D7-02 | 指定 scientific 路径 \(\Pi_Z\) 已施加 | **保持关闭。** `prospective_decode`，hook 已施加（X14c） |
| D7-03 | donor 优先 `source_value_pair.trace_ids` 的 `trace-base`/`trace-edit`；准备生成 `trace-source` | **指定路径关闭。** `donor_kind=same_source_diff_value`，行 `(0,2)`，不是 t0p；`trace-source` 已生成（X8e、X14c、X21）。评价量退化见 D9-05，不重开身份配对 |
| D7-04 | INLP decode 是 \(h@P\)；rescue 是 replace；`ie_z` 用 target-follow \(g(Y)\) | **接线关闭。** 第三次（无 flag）/第四次（有 flag）decode `mode=inlp` 且无 donor；rescue `mode=replace`；`ie_z_g=target_follow`，值等于 \(g_{\mathrm{int}}-g_{\mathrm{base}}\)，不是库函数隐向量均值（X14c/d、X23）。\(g(Y)\) 在本机无信息量见 D9-05 |
| D7-05 | C-rand 必跑 `add_delta` decode；C-layer 用 `c_layer_delta` 在弱层 `add_delta` | **指定路径关闭。** 无 flag 亦有 C-rand `add_delta`；有 flag 弱层 0 的 `delta` 与 `c_layer_delta` 对拍（X14c/d）。弱层 \(H\) 仍是读出层向量见 U-08 |
| D6-02 / D6-07 / A5-08 | 不可表达步前不入 \(H\)；几何 `timing=offline_hidden` | **保持关闭。** 6 行有限 `q`；几何字段 `offline_hidden`；`hook_once`/`transform` 在 `relative` |
| D6-08 / D6-09 | hook 元数据合并；collect 读 `--weight-seed` | **保持关闭**（X14c、X20） |
| D6-06 | hook 基用 StreamBank `basis_seed` | **共享关闭 / 对照几何仍用 `rng(5+weak)`。** `sample` 流现已写入 decode seed（相对 r07 前进一步） |
| A5-14 Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |
| pending_server | 真实权重 / Linux cgroup / 实测 P1–P3 | **同意未关。** tiny 随机权重不是 MODEL-01 |

## 6. 发现

### D9-01 — 声称冻结 hash 对当前磁盘不成立

- **状态：** confirmed defect（过程 / QA-01）
- **严重度：** high
- **文件 / 符号 / 行号：** `.planning/audits/round-09/VERSION.md` 声称 60 文件 / `9ffc4cd9…b3bf20`；交卷前 61 文件 rel+NUL+bytes = `81308124…4b6d`
- **触发条件：** 按 VERSION 脚本在开审与交卷前各复算一次
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。开审 MATCH。窗口内出现 `tests/test_round07_regressions.py`；`cli.py` 增补 `_try_source_value_pair`（674–687）；排除新测试后 60 文件仍 ≠ 声称。本通道未改这些文件。审查中至少观察到三个不同的 61 文件 digest。
- **影响：** 不能把本报告说成「已在声称快照 `9ffc4cd9…` 上签字」。D 核心（`collect.py` `intervene_hidden_decode`、`cmd_intervene` 逻辑、指定路径复跑）与开审阅读一致，但冻结契约破了。
- **建议：** 停写、重冻、审查者只对一个 hash 交卷。并行通道不得在审查窗口改冻结集合。

### D9-02 — D7-03：donor 已是 `same_source_diff_value`，不是 `trace-t0p`（猎项关闭）

- **状态：** closed / non-defect（指定路径身份配对）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **292–302、392–396、818–838、841–853、888**；`edits.py` **214–226**；`generate.py` **105–192**
- **对应要求：** CAUSAL-02 的「按 pair 取 donor」下限；作者 D7-03 关闭声称
- **证据：** X8e、X14c、X21。prepare 写 `trace-source` 与 `source_value_pair.trace_ids`。`_pair_source_value` 用 `base`×`same_source_diff_value`（`trace-edit`）。回退显式 `skip={"trace-t0p"}`。本机 `(0,2)`，kind 字符串恰为 `same_source_diff_value`。`_try_source_value_pair` 对 t1 fixture 仍落到 `make_source_value_pair`。
- **影响：** r07「donor 是同题 seed0/seed1」在指定路径上不再成立。这不够变成 CAUSAL-02 完成（见 D9-05）。

### D9-03 — D7-04：INLP 是 \(h@P\)，rescue 是 replace，`ie_z` 来自 \(g(Y)\)（猎项关闭）

- **状态：** closed / non-defect（接线）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **189–208**；`cli.py` **960–981**
- **对应要求：** INLP-01 / IE-01 的接线下限；作者 D7-04 关闭声称
- **证据：** X14c、X14d、X23。`mode=="inlp"` 为 `vec @ proj`，调用不传 donor。`mode=="replace"` 整段替换 last-token。`ie_z_g="target_follow"`，值 = \(1\{\hat y=\text{donor\_ans}\}-1\{\hat y_0=\text{donor\_ans}\}\)，与库函数 `ie_z` 隐向量均值（0.00237）不同。
- **影响：** 第二次前向不再是「再跑一次 \(\Pi_Z\)」。INLP 仍无独立四项结局块（只有 `inlp_followed_donor`），见 S-03。

### D9-04 — D7-05：C-rand / C-layer 已是独立的 `add_delta` decode（猎项关闭）

- **状态：** closed / non-defect（指定路径对照接线）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **897–907、965–975**；`collect.py` **197–202**；`interventions.py` **31–49**
- **对应要求：** 论文 §2.4；GOAL §5.11
- **证据：** X12、X14c、X14d。无 flag：C-rand 仍 decode，弱层不 decode，`dev_scores_missing`。有 flag：弱层 0 的 `delta` 与 `c_layer_delta` 对拍，不是主干预那组 `apply_swap`/`basis_seed`。相对四项可算（本机全 0）。
- **影响：** r07「C-rand 零次 decode / 弱层仍是 swap」在指定路径上不再成立。弱层施加的是读出层 \(\Delta\)，不是弱层自己的 \(H\)（U-08）。

### D9-05 — 指定路径 \(g(Y)\) 接线成立，但评价量无信息（不重开 D7-03/04）

- **状态：** residual defect（测量 / CAUSAL-02 评价）
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` **72–98、137–138**（`append_target_assignment` 只在 prepare）；`cli.py` **949–964**；`collect.py` **213–216**（intervene 仅 `decode_loop` `max_new=4`）
- **触发条件：** 指定 scientific tiny intervene
- **对应要求：** CAUSAL-02；论文 §2.4 \(g\) 为预先指定的来源跟随；IE-01
- **证据：** X23。base 与 value-edit 的 `answer` 同为 **82**（同 seed/同权重的约束两位数字，不是金答案 0 与 8），故 `nontarget` 结构上不可达（`ans==gold and ans!=donor_ans` 永假）。intervene 不教师强制 `\nq = `，五种模式输出相同乱码 `=9-V`。`ie_z=0` 是「两个都不是 82」，不是对照后的效应。
- **影响：** 猎项字符串已满足；不能把本机四项 0 或相对差 0 写成来源跟随实验结果。tiny 口径下这是测量空洞，不是 MODEL-01/CAUSAL 完成。
- **建议：** \(g\) 用干预前冻结的任务金/来源标签，不要用同 seed 抽到的两位数字；intervene 续写须与评价协议同一约束。未解耦时不要报告 nontarget。

### D9-06 — 模板 / `load_frozen` / `clone_cache` 仍未接入（D7-10 残留）

- **状态：** residual defect（模板路径） / closed（`extract_answer`）
- **严重度：** medium（模板；真实 HF 为 pending_server）
- **文件 / 符号 / 行号：** `events.py` **246–260**；`generate.py` **195–201、122–132**；`adapters.py` **10、18、32–42**
- **证据：** X15、X16。思考区数字不再当答案。CLI 与 `generate_task_trace` 均不调用 `apply_model_template`。tiny 随机权重按口径不算 MODEL-01 完成。
- **建议：** 卡片 revision 走 `apply_chat_template`。在此之前不要把 tiny 路径写成模板已对齐。

### D9-07 — `ids[:64]` 仍是静默帽（D7-07 残留）

- **状态：** residual defect（截断） / closed（本 fixture 未触发）
- **严重度：** low
- **文件 / 符号 / 行号：** `cli.py` **941–943**
- **证据：** X22。本机 45 < 64。更长事件仍会被静默切掉并自称 `event_aligned`。
- **建议：** hook 前缀取目标事件步前 token，禁止静默 `[:64]`。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载，未读官方 tokenizer JSON |
| U-02 | `replace` 用参数名 `delta` 传入救援向量 | 调用与实现一致；不另开缺陷 |
| U-03 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够 |
| U-04 | Prefill hidden 用最后一层而非 readout | 用户口令是「有 hidden」；不与 X19 同级 |
| U-05 | re-encode 与生成 ids 在乱码段的 8 处不一致 | 作者明确把 re-encode 当作修复；tiny 字级词表下是二次教师强制 |
| U-06 | `_load_source_value_pair` 依赖兄弟目录名 `prep`/`prepare`/`s-prep` | 指定路径 `s-prep`/`s-col` 找到 pair；换名会落到 `same_identity_fallback`（仍跳过 t0p）。已关 D7-03 的指定路径，不另开编号 |
| U-07 | `_expressible_donor` 在 pair `allclose` 时回退 | 本机 base/edit 互异，未触发 |
| U-08 | C-layer 把读出层 \(\Delta\) 加到弱层 residual | 猎项只要求 `c_layer_delta`+弱层 `add_delta`，已对拍。层不一致属协议残留，未升格为与 D7-05 同级重开 |
| U-09 | 窗口内 `cli.py`/`edits.py` 仍在被他方改写 | D 核心 intervene 逻辑复跑仍复现；记在 D9-01 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是** MODEL-01 完成 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 五模式独立 decode 与指定路径接线 | 无真实来源-数值 donor；本机 \(g(Y)\) 无信息量 |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta` 在一维标准正交基下正确 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、只改层 2 last-token；`finally` 含异常路径清理 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`；`enable_thinking` 仅在 `model_kind=="qwen3"` 传入 |
| N-04 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `token_ids` / `stop_reason` / `sampling` |
| N-05 | 关闭 | 几何 `timing` 保持 **`offline_hidden`**；`relative` 含 `hook_once=resid_post` 与 `transform=pi_z_swap`；hook 内部 `hook_timing=pre_step` 不覆盖几何字段 |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数 |
| N-07 | 关闭 | 跨界 token 不进入 `token_index`；`leaks_target` 在 straddling 时可为 True |
| N-08 | 关闭 | `extract_answer` 去掉闭合 think；未闭合返回 None |
| N-09 | 关闭（选项） | `resid_post_hook(..., once=True)` 在 decode 中只生效一次 |
| N-10 | 关闭（功能） | `clone_cache` 隔离存储并保留 `seq_length`；步进路径未接入 |
| N-11 | 过程 | 开审 hash MATCH；交卷前 MISMATCH（D9-01）。不得写成 HASH_MATCH |
| N-12 | 非缺陷 | `--backend offline` 的 \(H\) 是前缀 id；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 是随机初始化隐状态并标注 `random_init`。这是本机接口证明，**不是 MODEL-01 完成** |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 无 `--dev-layer-scores` 时 `clayer_status=dev_scores_missing` |
| N-16 | 关闭（有事件且可表达） | scientific `q` 步前入 \(H\)；不可表达步前不入；空事件 `no_event` |
| N-17 | 关闭（算法 + 指定路径接线） | 主 hook 变换是 \(\Pi_Z\)；前缀是 `text[:event.start]`（本机 45 token）；主层 readout **1** |
| N-18 | 关闭（接口） | `execute_repair_tiny` 重新 Prefill（含 hidden 与 KV）；dummy/offline/`prefix_token_ids` 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| N-20 | 关闭（猎单项，本轮独立核验） | donor **不是** t0p；INLP **不是** swap；C-rand/C-layer **是** `add_delta`；C-layer `delta` **是** `c_layer_delta`；`ie_z` **是** target-follow \(g(Y)\) |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` 无生产调用方 |
| S-03 | stub | `inlp_remove` 有 decode；`relative` 无 INLP 四项结局，只有 `inlp_followed_donor` |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道不通过（FAIL）。冻结：HASH_MISMATCH。猎项 D7-03/04/05 在指定 scientific 路径上独立关闭。tiny 不是 MODEL-01。**

相对 round-07 猎单，本机指定 `prepare --eval-mode scientific`→`collect --backend tiny`→`intervene --backend tiny`（及 `--dev-layer-scores 0.05 0.9 0.8`）核验：

1. donor 身份是 `same_source_diff_value`（`trace-base`/`trace-edit` 的 `q`），**不是** `trace-t0p`；`trace-source` 已生成并写入 pair。
2. INLP decode 是 \(h@P\)（无 donor），rescue 是 `replace`，`ie_z` 来自 target-follow \(g(Y)\)，不再是第二次 \(\Pi_Z\) 或隐向量均值。
3. C-rand **必定** `add_delta` decode；C-layer 仅在有 flag 时于弱层 0 用 `c_layer_delta` 做 `add_delta`；无 flag 保持 `dev_scores_missing`。
4. 几何 `timing=offline_hidden`；`relative` 含 `hook_once`/`transform`。\(H\) 六行全有限，非 `donor_missing`。

这些仍不够支持 MODEL-01 或 CAUSAL-01/02 完成：声称冻结 `9ffc4cd9…` 对交卷磁盘不成立；微型随机权重不是真实 HF；指定路径上 \(g(Y)\) 无信息（base/edit 答案同为 82，五模式输出相同乱码）。诚实的 tiny 五模式接线证明不得写成论文里的同批次交换/消融/救援实验结果。
