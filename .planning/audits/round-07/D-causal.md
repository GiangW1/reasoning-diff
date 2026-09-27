# D-causal 独立审查报告（round-07）

通道 D：模型与因果（tiny generate/collect/hook、三时机、swap \(\Pi_Z\)、C-rand/C-layer——弱层是对照不是主干预、INLP/rescue、来源-数值、Prefill KV、权重 seed）。指定复跑 scientific tiny collect/intervene。几何 `timing` 必须保持 `offline_hidden`，不得被 hook 改写成 `pre_step`。C-layer 第二次 decode **仅当** `--dev-layer-scores`。指定路径下若存在 \(\ge 2\) 行有限且同身份 \(H\)，intervene 不得停在 `donor_missing`。

独立性声明：未阅读 round-07 其他通道报告；只把 `.planning/audits/round-07/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账。`.planning/audits/round-06/D-causal.md` **只作猎单**（D6-02..D6-10），不作证据。结论以本机当前磁盘与本轮复跑为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试通过当作实现正确；不把作者 `local close` 或声称 143 passed 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01 完成（真实 HF 为 `pending_server`）。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。诚实的 `offline_prefix_ids` 在未被宣称为隐状态时不记缺陷。

对照原文：论文 §2.4（交换公式、前瞻定位、C-rand/C-layer 同批次）、§4.2（步前/值前/步尾与 span 池化）、§6（V-Probing 时机对照；结果规划中的来源—数值解耦 / 交换 / Knock-out / Rescue）、§8（科学评测含交换/消融/救援）；GOAL §5.6–5.11、§5.13、§5.15；`docs/EXPERIMENT_PROTOCOL.md` §4。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T03:20:00+08:00 |
| 声称冻结 hash | `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（`.planning/audits/round-07/VERSION.md`；60 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **HASH_MISMATCH。** 开审时按 VERSION 脚本逐字复算得 60 文件 / `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（当时 MATCH）。交卷前同一脚本再算：**60 文件** → `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`。本通道未改冻结集合；审查窗口内 `cli.py` 增补 `_e_premise_ids`（校准 E 列顺序），`tests/test_round06_regressions.py` 增补 `test_truth_indices_follow_e_columns_not_label_order`。D 核心（`models/*`、`interventions.py`、`repair.py`、`events.py` 解析、`rng.py`、`executor.py`）mtime 早于该漂移；`cmd_intervene` 逻辑未改，仅行号下移。因果结论锚定**当前磁盘**；声称冻结对当前字节不成立 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；审查对象是冻结脚本覆盖的 60 个文件的**当前**字节） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| 作者 pytest 声称 | 143 passed。本通道只重跑所引用子集，不把 143 记为已验证 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对（行号为交卷时当前磁盘）：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / `think_ids` / `load_frozen(..., local_files_only=True)` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids` / `readout_layer_index`（60%–75% 带） / `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–200 | `collect_hidden_trace` 跳过不可表达 `pre_step`；空事件 `no_event`；`collect_tiny`；`intervene_tiny` / `intervene_swap_decode` 的 \(\Pi_Z\) hook + `basis_seed` |
| `src/reasoning_diff/models/features.py` | 1–40 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–201 | `sample_next`；`decode_loop`；`append_target_assignment`；`generate_task_trace`（只解析生成区）；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–121 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / INLP / `rescue_controls` / `select_weak_layer` / `ie_z` / `intervention_report` |
| `src/reasoning_diff/repair.py` | 1–224 | `mask_prefix` / `execute_repair_tiny` Prefill hidden+KV / `run_repair`（无有限 hidden 不得 `refilled_prefix`） / `consecutive_repairs` |
| `src/reasoning_diff/cli.py` | 1–1165 | 重点 `cmd_prepare` 257–428、`cmd_collect` 431–534、`_expressible_donor` 775–793、`cmd_intervene` 796–910、`cmd_repair` 912–931 |
| `src/reasoning_diff/executor.py` | 1–110 | `IsolatedExecutor` unavailable；`ChildProcessExecutor.isolated_sandbox=False`；默认 Unavailable |
| `src/reasoning_diff/rng.py` | 41–53 | `StreamBank` 名 `sample/direction/perturb/bootstrap/split` |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理 |
| `tests/test_tiny_cache.py` | 1–26 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | 25–137、218–220 | readout 带；scientific collect span；offline 几何≠`pre_step`；repair Prefill；子进程非隔离 |
| `tests/test_round05_regressions.py` | 23–141 | scientific 事件；步边界行数；几何 timing≠`pre_step`；现亦断言 `status != donor_missing` 且 `hook_once`/`transform` |
| `tests/test_round06_regressions.py` | 25–136 | 生成区事件；有限 \(H\) + donor 配对；Prefill；`--weight-seed`；另含与 D 无关的 E 列顺序回归 |

支持性阅读：`events.py` `parse_events` / `_parse_assignments` 27–89（`start=match.start()`，不是行首）、`boundary_index` 237–243、`extract_answer` 246–260；`scoring.py` `score_code` 19–30；`schema.py` `POSITION_KINDS` 39；`edits.py` `make_source_value_pair` 204–234；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`。`cli.py` 校准段 `_e_premise_ids` 属 E 列顺序，不作本通道通过项。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | 开审 **MATCH** `9814019a…f95801`（60）。交卷前 **HASH_MISMATCH** `1b88bec2…1e257e`（60）。见 D7-01 |
| X2 | pytest tiny/因果相关子集 | **52 passed / 17.44s**（`--collect-only` 亦 52，含 `test_truth_indices_follow_e_columns_not_label_order`）。通过只证明冒烟与回归锁。`test_intervene_tiny_geometry_timing_stays_offline` 现要求 `status != donor_missing` 且 `hook_once`/`transform`，仍允许 `geometry_on_hidden` |
| X3 | `apply_swap` 与标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.178\)、\(\Delta V_{\max}=0.320\)，且 **仅 last token**（earlyK=0）。`transform` 形状 `(1,1,32)` |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3 次**；`once=True` **1 次** |
| X7 | hook `finally` 清理 | `RuntimeError` 后 `layer._forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)`；三位置 token_index **2/3/4**；`sampling` 已写入 |
| X8b | `collect_hidden_trace` + 全文 `"p1 = 4\\np2 = 0\\nq = 0\\n"` | `parse_events` 跨度为 **p1 0–6 / p2 7–13 / q 14–19**（`status=ok`，不再整行）。`start=0` 的 p1 步前不可表达，**不入** \(H\)；`event_ids=['p2','q']`，\(H\) `(2,32)` 全有限 |
| X8c | 空事件库层 | `h_position=no_event`，`H` 形状 `(0,32)`，不塌成末 token |
| X8e | scientific `prepare`→`collect --backend tiny` | 5 条 `tiny-qwen2`（base / t0p / edit / 两条 extra value-edit），每条 **1** 个生成区 `q`（`start=45,end=51,status=ok`，`parse_region=generated`，`parse_status=constrained_target`）。`H`/`H_pre_*` 皆 `(5,32)`，**5/5 行有限**（0 NaN）。`event_rows.jsonl` 5 行，皆 `{node_id:q, trace_id:…}`。`hidden_layer=1`；`weight_source=random_init`。三位置互异（\(\|\Delta\|\approx 0.156/0.158/0.147\)）；步前 \(\neq\) 该轨迹末 token（\(\|\Delta\|\approx 0.147\)） |
| X8f | scientific collect 拒绝 | 无事件 → `scientific collect requires step-boundary events`（代码路径仍在）。`--backend offline` → `scientific collect refuses offline_prefix_ids as H`（r04 回归锁） |
| X8g | re-encode vs 生成 ids | 每条轨迹 51 token 中 **8** 个与 `encode_text(text)` 不同（恰为 `max_new=8` 乱码段）。collect 的 \(H\) 是对表面文本的二次前向 |
| X9 | `leaks_target` 能否为 True | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None`。150 次随机偏移中 **39 True / 102 index 空** |
| X10 | `boundary_index(..., 2)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 1；`position` 只做枚举校验 |
| X11 | INLP / rescue 算法 | steps=1 vs 8 最大差 **1.000**。`H@P8` 第一列范数 \(\approx 10^{-15}\)。`rescue([1,0],[0,1])=[1,1]`。`rescue_controls` 给出 matched / error_source / random，随机范数匹配 |
| X12 | C-rand / C-layer 范数与弱层选择 | 缺范数仍 `ValueError`。`select_weak_layer({0:0.2,1:0.1,2:0.4})=1`；`{0:0.05,1:0.9,2:0.8}=0`。几何三项可按同一 `target_norm` 对齐 |
| X13 | StreamBank vs hook 基 | `direction` 第一抽 113750710（CLI 785 行丢弃）；第二抽 **basis_seed=1153799966**。`perturb` 17172908。同 seed 两基 \(\Delta=0\)；相对 `default_rng(1)` 最大差 **0.687**。`sample` 流从未读取 |
| X14a | `intervene_tiny` swap 是否施加 | `transform=pi_z_swap`，logits 可区分，cache 对象隔离，层可指定 |
| X14c | **指定** scientific tiny collect→intervene（**无** `--dev-layer-scores`） | `_expressible_donor` 选 `(0,1)` = `trace-base`/`trace-t0p` 的同身份 `q`。`status=prospective_decode`，**几何 `timing=offline_hidden`**。`relative.hook_once=resid_post`，`transform=pi_z_swap`，`hook_timing=pre_step`（hook 内部标签，几何字段未改写）。decode **2 次**（主 + INLP），层皆 **1**，`basis_seed` 皆 1153799966，`hook_fired=true`。`clayer_status=dev_scores_missing`（无弱层第二次前向）。主四项 `invalid=1` 其余 0；对照四项 **null**。三项范数锁成 **0.000371** |
| X14d | 另跑 `--dev-layer-scores 0.05 0.9 0.8` | decode **3 次**，层 **1 / 0 / 1**（主 readout、弱层 0、INLP readout）。`clayer_status=dev_weak_layer_decode`，`weak_layer=0`。弱层 decode 仍是 `apply_swap` + **同一** `basis_seed`，不是 `c_layer_delta` 的 `rng(5+weak)` 基。C-rand **零次** decode |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 内数字 → 7；未闭合 → None；`</think>` 后 boxed/#### → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 无调用**。`from_pretrained` 仅在 `load_frozen` |
| X16 | `clone_cache` / DynamicCache | 本机无 `.copy()`。clone ≠ 原对象；`data_ptr` 不同；`add_` 后原张量不变；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states` 长度 4。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.686\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False`；`SubprocessExecutor is ChildProcessExecutor`。默认 `score_code` → `executor_unavailable` / `value=None` |
| X19a | `execute_repair_tiny` Prefill hidden | 返回 32 维有限非零 `prefill_hidden`；`refilled_prefix=True`。dummy / 空 hidden → `prefill_unavailable`。`prefix_token_ids` 旁路 → `refilled_prefix=False` / `prefix_ids_without_hidden` |
| X19b | Prefill KV | `output_hidden_states=True` 后 `past_key_values.get_seq_length()==prefix_len`（本例 11=11）。hidden **取最后一层** last-token，与 readout 层 \(\|\Delta\|\approx 5.51\) |
| X19c | scientific CLI repair | `k=1..5` 均 `refilled_prefix=true` / `status=ok`；`extra_prefill_tokens` 皆 32；slots 随 k 增长至 `{p1,p2,q}`。落盘 **无** `prefill_hidden` 字段 |
| X20 | `weight_seed` | 同 seed 同 ids → \(\|\Delta H\|=0\)；异 seed → 0.179；同 seed 异 ids → 0.177。CLI collect **读取** `--weight-seed`；`--weight-seed 7` 写入 spec 且与 seed 0 的 \(H\) \(\|\Delta\|=0.397\) |
| X21 | 来源-数值 | `edits.jsonl` **含** `kind=source_value_pair`（value + rename 两臂）。`cmd_intervene` **不读** `edits.jsonl`。donor 是有限同 `node_id` 的 \(H\) 行（本机 base seed0 vs t0p seed1 的 `q`），不是解耦任务对 |
| X22 | 事件跨度 / hook 前缀 | 生成区 `q` 跨度 45–51，前缀 45 token；`ids[:64]` **未截断**。问句前提不再进入 scientific 事件。库层 `parse_events` 用 match 边界，不再整行 |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server` |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存。属 `pending_server` |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机 donor 不是来源-数值条件 |
| 全量 pytest（作者称 143） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| D6-02 / D6-07 | 不可表达 `pre_step` 不再入 \(H\)；scientific 只解析生成区；按有限且同 `node_id` 配对；几何 `timing` 仍为 `offline_hidden` | **指定路径关闭。** 5 行有限同身份 `q`，`status=prospective_decode`，几何 `offline_hidden`，hook 已施加（X8e、X14c、X22）。`ids[:64]` 仍是静默上限，本 fixture 未触发 |
| D6-03 | `source_value_pair` 写入 `edits.jsonl` | **落盘关闭 / 协议未关。** 文件有 pair（X21）。intervene 不读它；donor 是两条同题不同 seed 的 `q` 步前 \(H\) |
| D6-08 | hook 元数据与 `intervention_report` 合并 | **关闭。** `relative` 含 `hook_once`/`transform`/`hook_timing`/`donor_rows`（X14c） |
| D6-09 | collect 读 `--weight-seed` | **关闭。** X20 |
| D6-04 | INLP 进入第二次 decode | **半关。** 有第二次 `intervene_swap_decode`，但是 \(\Pi_Z\) 换向投影后的 donor，不是残差 INLP；rescue 仍无 decode；`ie_z` 仍是隐向量均值（X14c、D7-04） |
| D6-05 | 有 `--dev-layer-scores` 才弱层另跑 decode 并写 `dev_weak_layer_decode` | **门控关闭 / 对照协议未关。** 指定路径无 flag → 2 次 decode、`dev_scores_missing`。有 flag → 层 0 第三次 decode 且改标签。C-rand 仍无 decode；弱层 decode ≠ `c_layer_delta`；对照四项仍 null（X14d、D7-05） |
| D6-06 | hook 基用 StreamBank `basis_seed` | **共享关闭 / 采样流未关。** 几何 QR 与 hook 共用第二抽 `direction`（\(\Delta=0\)）。`sample` 空闲；direction 第一抽丢弃；C-layer 几何种子 `5+weak` 与 decode 的 `basis_seed` 不是同一基（X13、X14d） |
| A5-08 / F5-02 / D5-04 | 几何 `timing` 不被 hook 改写成 `pre_step`；主 hook 用 readout | **保持关闭。** 几何 `offline_hidden`；主层 1；弱层分数不改主层 |
| A5-09 / F6-04 | Prefill 需要有限 hidden | **接口关闭。** `execute_repair_tiny` 产出有限 hidden + KV；旁路/空 hidden 不得冒充（X19） |
| A4-13 | `ChildProcessExecutor` 不是隔离 | **仍关闭**（X18） |
| A5-14 Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |
| pending_server | 真实权重 / Linux cgroup / 实测 P1–P3 | **同意未关。** tiny 随机权重不是 MODEL-01 |

相对 r06 已关闭、本轮不再单列缺陷：scientific `H[0]/H[1]` 全 NaN 导致 hook 零次；`make_source_value_pair` 返回值丢弃不落盘；`relative` 被 `intervention_report` 整表覆盖以致看不到 hook 元数据；CLI collect 写死 `weight_seed=0`；问句同行多赋值把 p1/p2 步前写成不可表达并选作 donor；无分数时写 `dev_weak_layer` 谎言标签。

## 6. 发现

### D7-01 — 声称冻结 hash 对当前磁盘不成立

- **状态：** confirmed defect（过程 / QA-01）
- **严重度：** high
- **文件 / 符号 / 行号：** `.planning/audits/round-07/VERSION.md` 声称 `9814019a…f95801`；当前 60 文件 rel+NUL+bytes = `1b88bec2…1e257e`
- **触发条件：** 按 VERSION 脚本在交卷前复算
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。开审时曾 MATCH。漂移为 `cli.py` `_e_premise_ids`（663–671）与 `tests/test_round06_regressions.py` `test_truth_indices_follow_e_columns_not_label_order`。本通道未改这些文件。
- **影响：** 不能把本报告说成「已在声称快照 `9814019a…` 上签字」。D 核心因果字节与开审阅读一致，但冻结契约破了。
- **建议：** 停写、重冻、审查者只对一个 hash 交卷。

### D7-02 — 指定 scientific collect→intervene 已对有限同身份行施加 \(\Pi_Z\)（D6-02 关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **50–53**（不可表达 `pre_step` `continue`）；`cli.py` **775–793、814–885**
- **对应要求：** CAUSAL-01 的「能跑到 hook」下限；作者 D6-02 关闭声称
- **证据：** X8e、X14c、X22。5 行有限 `q`，跨 ≥2 条轨迹；`status` 不是 `donor_missing`；几何 `timing=offline_hidden`；`hook_once`/`transform` 在 `relative`。
- **影响：** r06「配对回归导致 hook 零次」在指定路径上不再成立。这不够变成 CAUSAL-01/02 完成。

### D7-03 — `source_value_pair` 已落盘，但 donor 仍不是来源—数值条件（D6-03 残留）

- **状态：** residual / confirmed defect（协议）
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **380–390**（写入）、**814–817、859–860**（不读 edits；`donor_ans=traces[1].answer`）；`edits.py` **204–216**
- **触发条件：** 任何声称 C2 / 来源跟随的 intervene
- **对应要求：** CAUSAL-02；论文 §2.4 / §6 来源—数值解耦；GOAL §5.10；协议 §4
- **证据：** X21、X14c。pair 在 `edits.jsonl`。donor 行是 `trace-base` 与 `trace-t0p`（同题、seed 0/1、约束 `\nq = 82` vs `53`）。`_expressible_donor` 在身份组 `allclose` 时回退到任意两行有限 \(H\)（790–792），不要求来源/数值臂。
- **影响：** 落盘关闭了「构造函数返回值丢弃」。没有高层预先指定的目标/非目标来源矩阵，也没有「每个数值条件独立提取 donor」。
- **建议：** intervene 读 pair 任务的同身份步前；记录层、token、可见前缀与 `weight_seed`；禁止用「另一条随机流」冒充解耦 donor。

### D7-04 — INLP/rescue 仍不是论文中的生成干预；`ie_z` 仍不是 \(\mathbb E[g(Y)]\)（D6-04 未关）

- **状态：** residual / confirmed defect（接线）
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **839–841、876–882**；`collect.py` `intervene_swap_decode` **174–180**（hook 只 `apply_swap`）；`interventions.py` `ie_z` **88–89**
- **触发条件：** tiny/scientific `intervene`
- **对应要求：** CAUSAL-01；INLP-01；IE-01；论文 §2.4 / §6 Knock-out / Rescue
- **证据：** X11、X14c、X_iez=2.0（均值差）。INLP 第二次 decode 的 donor 为 `donor @ proj`（32×32，条件 `donor.shape==(proj.shape[0],)` 为真），然后仍走 \(\Pi_Z\) swap。rescue 只在 numpy `rescue_controls` 上算 `ie_z`。`intervention_report` 的 crand/clayer 四项显式传 `None`，故 `relative.target/nontarget/task_correct/invalid` 为 null。`followed_donor` 是 `generated_ids != baseline`，不是来源跟随。
- **建议：** 同一事件步前分别跑 swap / 残差 INLP / `rescue_controls` 的 decode；由生成文本算四项；`ie_z` 用预指定 \(g\)。未做残差消融时不要把第二次 swap 叫做 INLP。

### D7-05 — C-layer 第二次 decode 的门控已守；对照协议仍未成立（D6-05 残留）

- **状态：** closed（门控） / confirmed defect（对照协议）
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **825–836、871–875、878–882**
- **触发条件：** 指定路径无 `--dev-layer-scores`；对照路径有该 flag
- **对应要求：** 论文 §2.4；GOAL §5.11；IE-01
- **证据：** X12、X14c、X14d。指定路径：2 次 decode、`dev_scores_missing`、主层 1——符合口令「C-layer 第二次 decode 只在有 flag 时」。有 flag：弱层 0 另跑一次，标签 `dev_weak_layer_decode`。但该 decode 与主干预同一 `apply_swap`/`basis_seed`，不是 `c_layer_delta`；C-rand 无 decode；落盘三项范数因 `scale_to_norm` 锁死；相对对照差值无法计算。
- **影响：** 「无分数不谎称弱层 decode」成立。「弱层是同幅度、同位置、同采样的对照」不成立。
- **建议：** 主干预固定读出层；C-rand/C-layer 各跑同秩、同位置、同范数、同采样流的 decode，并填四项。未做第二次前向时保持 `dev_scores_missing`。

### D7-06 — hook 基已共享 `basis_seed`；采样流与 C-layer 几何基仍脱钩（D6-06 残留）

- **状态：** closed（hook 基） / residual defect（流隔离）
- **严重度：** low（相对 r06 的「hook 用 `default_rng(1)`」）
- **文件 / 符号 / 行号：** `cli.py` **803–821、864、872**；`collect.py` **174–175**
- **证据：** X13、X14c。几何 `orthonormal_basis(..., default_rng(basis_seed))` 与 hook 同 seed、同秩 2，基 \(\Delta=0\)。`sample` 未读；decode 用 `torch.Generator().manual_seed(0)`。C-layer 几何用 `rng(5+weak)`。
- **建议：** 报告范数必须来自实际写入 hook 的那组基；对照 decode 用自己的对照基；采样走 `sample` 流。

### D7-07 — 生成区 match 跨度已修复指定路径；`ids[:64]` 仍是静默帽（D6-07 残留）

- **状态：** closed（指定路径跨度） / residual defect（截断）
- **严重度：** low
- **文件 / 符号 / 行号：** `events.py` **39–41**；`generate.py` **148–155**；`cli.py` **857–862**
- **证据：** X8b、X22。scientific `q` 前缀 45 < 64。更长事件仍会被静默切掉并自称 `event_aligned`。
- **建议：** hook 前缀取目标事件步前 token，禁止静默 `[:64]`。

### D7-08 — hook 元数据不再被覆盖（D6-08 关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **883**（`report = {**hook_meta, **rel, ...}`）
- **证据：** X14c。

### D7-09 — CLI collect 读取 `--weight-seed`（D6-09 关闭）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **471、532、1108**
- **证据：** X20。

### D7-10 — thinking 抽取仍正确；模板 / `think_ids` / `load_frozen` / `clone_cache` 仍未接入（D6-10 残留）

- **状态：** residual defect（模板路径） / closed（`extract_answer`）
- **严重度：** medium（模板；真实 HF 为 pending_server）
- **文件 / 符号 / 行号：** `events.py` **246–260**；`generate.py` **195–201、122–132**；`adapters.py` **10、18、32–42**
- **证据：** X15、X16。思考区数字不再当答案。CLI 与 `generate_task_trace` 均不调用 `apply_model_template`。tiny 随机权重按口径不算 MODEL-01 完成。
- **建议：** 卡片 revision 走 `apply_chat_template`。在此之前不要把 tiny 路径写成模板已对齐。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载，未读官方 tokenizer JSON |
| U-02 | `transform` 若原地修改 `tensor[:, -1:]` | hook 先 clone 再写入 patched；现调用是新张量 `apply_swap` 结果 |
| U-03 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够；未读完 transformers 每一分支 |
| U-04 | Prefill hidden 用最后一层而非 readout | 用户口令是「有 hidden」；层选择偏差未单独升格为与 X19 同级缺陷 |
| U-05 | re-encode 与生成 ids 在乱码段的 8 处不一致 | 作者明确把 re-encode 当作修复；tiny 字级词表下这是二次教师强制，不另开高严重度项 |
| U-06 | scientific 连续 k 的 `extra_prefill_tokens` 皆 32 | 更偏修复预算/截断（`ids[:32]`），不单独升格为因果缺陷 |
| U-07 | `_expressible_donor` 在同身份 `allclose` 时回退到任意有限行 | 本机 5 个 `q` 互异，未触发；已记在 D7-03，不另开编号 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是** MODEL-01 完成 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 向量公式与指定路径 \(\Pi_Z\) decode | 无来源-数值 donor，无四项对照实测 |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta` 在一维标准正交基下正确 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、只改层 2 last-token；`finally` 含异常路径清理 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`；`enable_thinking` 仅在 `model_kind=="qwen3"` 传入 |
| N-04 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `token_ids` / `stop_reason` / `sampling` |
| N-05 | 关闭 | CLI 不再写入虚构 0.6/0.55 类正确率；tiny 主结局来自 `extract_answer`（本机 invalid=1）；对照仍 null |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数 |
| N-07 | 关闭 | 跨界 token 不进入 `token_index`；`leaks_target` 在 straddling 时可为 True |
| N-08 | 关闭 | `extract_answer` 去掉闭合 think；未闭合返回 None |
| N-09 | 关闭（选项） | `resid_post_hook(..., once=True)` 在 decode 中只生效一次 |
| N-10 | 关闭（功能） | `clone_cache` 隔离存储并保留 `seq_length`；步进路径未接入 |
| N-11 | 过程 | 开审 hash 曾 MATCH；交卷前 MISMATCH（D7-01）。不得写成 HASH_MATCH |
| N-12 | 非缺陷 | `--backend offline` 的 `H` 是前缀 id 且标注 `offline_prefix_ids`；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 是随机初始化隐状态并标注 `random_init`。这是本机接口证明，不是 MODEL-01 完成 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 无 `--dev-layer-scores` 时 `clayer_status=dev_scores_missing` |
| N-16 | 关闭（有事件且可表达） | scientific `q` 三位置是读出层隐状态且 ≠ 末 token；不可表达步前不入 \(H\) |
| N-17 | 关闭（算法 + 指定路径接线） | tiny hook 变换是 \(\Pi_Z\)；前缀是 `text[:event.start]`（本机 45 token） |
| N-18 | 关闭（接口） | `execute_repair_tiny` 重新 Prefill（含 hidden 与 KV）再 decode；dummy/offline/`prefix_token_ids` 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| N-20 | 关闭（r06 猎单项，本轮独立核验） | collect **re-encode** `trace.text`；`H_pre_*` 按可表达事件堆叠；主 hook **readout 层 1**；几何 `timing` 保持 **`offline_hidden`** |
| N-21 | 关闭（库层） | 空事件不再写成 last-token `pre_step`；scientific collect 拒绝无事件 |
| N-22 | 关闭（指定复跑检查清单） | \(H\) 行有限；`event_rows.jsonl` 存在且与行数一致；intervene 非 `donor_missing`；`hook_once`/`transform` 在 `relative`；C-layer 第二次 decode 仅当 `--dev-layer-scores`；`basis_seed` 主/INLP 共享；`source_value_pair` 在 `edits.jsonl`；Prefill 要求有限 hidden |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` / `forbid_host_exec` 无生产调用方 |
| S-03 | stub | `rescue_controls` / `inlp_remove` 有 CLI numpy 调用；INLP「第二次 decode」仍是 swap |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道不通过（FAIL）。冻结：HASH_MISMATCH。**

相对 round-06，指定 scientific 路径上 D6-02 的「NaN 前两行 → hook 零次」**本机关闭**：\(H\) 五行全有限、`event_rows` 对齐、同身份 `q` 配对、`status=prospective_decode`、几何 `timing=offline_hidden`、`relative` 含 `hook_once`/`transform`、无 `--dev-layer-scores` 时不做弱层第二次 decode、有 flag 时弱层才 decode、hook 基与 CLI 几何共用 `basis_seed`、`edits.jsonl` 有 `source_value_pair`、Prefill 无有限 hidden 不得冒充。collect `--weight-seed`、生成区事件、match 跨度、不可表达步前不入 \(H\)——本机成立。微型随机权重按口径不算 MODEL-01 完成。Gate 未注册不记缺陷。

这些仍不够支持 CAUSAL-01/02。声称冻结 `9814019a…` 对当前磁盘不成立。donor 不是来源—数值对。INLP 第二次前向仍是 \(\Pi_Z\)，rescue 停在 numpy，`ie_z` 不是结果量。C-rand 无 decode；C-layer decode 不是 C-layer 几何。对照四项为 null，相对差值算不出来。诚实的 tiny 前瞻 decode 仍不是论文里的同批次交换/消融/救援实验。
