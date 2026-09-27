# D-causal 独立审查报告（round-06）

通道 D：模型与因果（tiny generate/collect/hook、三时机、swap \(\Pi_Z\)、C-rand/C-layer——弱层是对照不是主干预、INLP/rescue、来源-数值、Prefill KV、权重 seed）。指定复跑 scientific tiny collect/intervene。几何 `timing` 必须保持 `offline_hidden`，不得被 hook 改写成 `pre_step`。独立核验 r05 声称：步边界 \(H\)；re-encode text；主 hook 用 readout 层；Prefill 有 hidden。

独立性声明：未阅读 round-06 其他通道报告；只把 `.planning/audits/round-06/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账；对照阅读了本通道 round-01–05 报告以便核对关闭项，结论以本机当前磁盘与本轮复跑为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试通过当作实现正确；不把作者 `local close` 或声称 136 passed 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01 完成（真实 HF 为 `pending_server`）。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。诚实的 `offline_prefix_ids` 在未被宣称为隐状态时不记缺陷。

对照原文：论文 §2.4（交换公式、前瞻定位、C-rand/C-layer 同批次）、§4.2（步前/值前/步尾与 span 池化）、§6（V-Probing 时机对照）、§8（科学评测含交换/消融/救援）；GOAL §5.6–5.11、§5.13、§5.15；`docs/EXPERIMENT_PROTOCOL.md` §4。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T02:20:00+08:00 |
| 声称冻结 hash | `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（`.planning/audits/round-06/VERSION.md`；59 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **HASH_MATCH。** 按 VERSION 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → **59 文件** → `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563` |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；审查对象是冻结脚本覆盖的 59 个文件字节） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |
| 作者 pytest 声称 | 136 passed。本通道只重跑所引用子集，不把 136 记为已验证 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / `think_ids` / `load_frozen(..., local_files_only=True)` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids` / `readout_layer_index`（60%–75% 带） / `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–192 | `collect_hidden_trace` 三位置与空事件 `no_event`；`collect_tiny`；`intervene_tiny` / `intervene_swap_decode` 的 \(\Pi_Z\) hook；`event_aligned` 只改 hook 字段 |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–191 | `sample_next`；`decode_loop`；`append_target_assignment`；`generate_task_trace`；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / INLP / `rescue_controls` / `select_weak_layer` / `ie_z` / `intervention_report` |
| `src/reasoning_diff/repair.py` | 1–217 | `mask_prefix` / `execute_repair_tiny` Prefill hidden+KV / `run_repair` / `consecutive_repairs` |
| `src/reasoning_diff/cli.py` | 1–1052 | 重点 `cmd_prepare` 252–411、`cmd_collect` 414–504、`cmd_intervene` 697–808、`cmd_repair` 811–842 |
| `src/reasoning_diff/executor.py` | 1–109 | `IsolatedExecutor` unavailable；`ChildProcessExecutor.isolated_sandbox=False`；默认 Unavailable |
| `src/reasoning_diff/rng.py` | 41–53 | `StreamBank` 名 `sample/direction/perturb/bootstrap/split` |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理 |
| `tests/test_tiny_cache.py` | 1–26 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | 25–137、218–220 | readout 带；scientific collect span；offline 几何≠`pre_step`；repair Prefill；子进程非隔离 |
| `tests/test_round05_regressions.py` | 23–136 | scientific 事件；步边界行数；几何 timing≠`pre_step`；dummy 非 Prefill |

支持性阅读：`events.py` `parse_events` 75–89、`boundary_index` 238–244、`extract_answer` 247–261；`scoring.py` `score_code` 19–30；`schema.py` `POSITION_KINDS` 39；`edits.py` `make_source_value_pair` 204–216；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | **HASH_MATCH** `dc2ba459…545563`；59 文件 |
| X2 | pytest tiny/因果相关 24 项 | **24 passed / 12.36s**。通过只证明冒烟与回归锁，不证明因果协议。`test_intervene_tiny_geometry_timing_stays_offline` 在 scientific 路径上只断言 `timing != "pre_step"`，对 `donor_missing`/`unexpressible` 也通过 |
| X3 | `apply_swap` 与标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.154\)、\(\Delta V_{\max}=0.349\)，且 **仅 last token**（earlyK=0）。`transform` 形状 `(1,1,32)` |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3 次**；`once=True` **1 次** |
| X7 | hook `finally` 清理 | `RuntimeError` 后 `layer._forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)`；三位置 token_index **2/3/4**；`sampling` 已写入 |
| X8b | `collect_hidden_trace` + fixture 文本 `"p1 = 4\\np2 = 0\\nq = 0\\n"` | 事件 `q` start/value/end = **14/18/19**；token_index **13/17/18**；三键与 `hidden[idx]` **逐位相等**；位置间 \(\|\Delta\|\approx 0.158/0.239/0.185\)；`E` 两行 \(\|\Delta\|\approx 0.068\) |
| X8c | 空事件库层 | `h_position=no_event`，`H` 形状 `(0,32)`，**不再**塌成末 token |
| X8d | fixture `prepare`→`collect --backend tiny` | 轨迹仍写序号 `token_ids=range(1,len+1)`；collect **re-encode** `trace.text`（`encode_text` ≠ 序号）；两文本不同 → `H` `(2,32)`，\(\|H_0-H_1\|\approx 0.011\)，不再 `allclose` |
| X8e | scientific `prepare`→`collect --backend tiny` | 6 条 `tiny-qwen2`，每条 3 事件，`parse_status=ok`；`H`/`H_pre_*` 皆 `(18,32)`（=事件数）；`hidden_layer=1`；`weight_source=random_init`。**12/18** 行 `H_pre_step` 全 NaN（p1/p2）；6 个 `q` 行有限，三位置互异（\(\|\Delta\|\approx 0.156/0.158/0.147\)），且 \(q\) 步前 \(\neq\) 该轨迹末 token（\(\|\Delta\|\approx 0.147\)） |
| X8f | scientific collect 拒绝 | 无事件 → `scientific collect requires step-boundary events`。`--backend offline` → `scientific collect refuses offline_prefix_ids as H` |
| X8g | re-encode vs 生成 ids | 每条轨迹 51 token 中 **8** 个与 `encode_text(text)` 不同（恰为 `max_new=8` 乱码段）；赋值段 `\nq = ..` 一致。collect 的 \(H\) 是对表面文本的二次前向，不是生成 `token_ids` 的隐状态 |
| X9 | `leaks_target` 能否为 True | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None`。150 次随机偏移中 **39 True / 102 index 空** |
| X10 | `boundary_index(..., 2)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 1；`position` 只做枚举校验 |
| X11 | INLP / rescue | steps=1 vs 8 最大差 **0.978**。`H@P8` 第一列范数 \(\approx 10^{-31}\)。`rescue([1,0],[0,1])=[1,1]`。`rescue_controls` 给出 matched / error_source / random，随机范数匹配 |
| X12 | C-rand / C-layer 范数与弱层选择 | 缺范数仍 `ValueError`。`select_weak_layer({0:0.2,1:0.1,2:0.4})=1`；`{0:0.05,1:0.9,2:0.8}=0`。三项可按同一 `target_norm` 对齐 |
| X13 | StreamBank vs 实际 hook 基 | CLI `direction` 抽出 113750710，`perturb` 抽出 17172908。同一 32 维示范向量：CLI 基范数 2.796；`intervene_swap_decode` 内部 `default_rng(1)` 基范数 1.023；两基最大元素差 **0.862**。`sample` 流从未读取 |
| X14a | `intervene_tiny` swap 是否施加 | `transform=pi_z_swap`，logits \(\Delta_{\max}=0.512\)，cache 对象隔离，层 1 |
| X14b | fixture tiny intervene（有可区分 \(H\)） | `status=prospective_decode`，**几何 `timing=offline_hidden`**（未被改写成 `pre_step`）。monkeypatch：`layer=1=readout_layer_index(3)`，`event_aligned=True`，前缀 14 ids = `encode_text(text[:14])`（`q` start=14），**不是** `"follow donor"`。`--dev-layer-scores 0.05 0.9 0.8` 后 `clayer_status=dev_weak_layer`，**主 hook 仍是层 1**（弱层本应为 0）。`followed_donor=false`；主四项 `invalid=1` 其余 0（`extract_answer` 对 4 个乱码 token）；对照四项仍 null。`relative` **不含** `hook_once`/`transform`/`hook_timing`/`weak_layer`（写入后被 `intervention_report` 覆盖） |
| X14c | **指定** scientific tiny collect→intervene | `H[0]` 与 `H[1]` 皆全 NaN（allclose `equal_nan=True`）→ **`status=donor_missing`，`timing=unexpressible`，三项范数 null，hook 一次都未调用**。传 `--dev-layer-scores` 亦然（短路径，不读分数） |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 内数字 → 7；未闭合 → None；`</think>` 后 boxed/#### → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 无调用**。`from_pretrained` 仅在 `load_frozen` |
| X16 | `clone_cache` / DynamicCache | 本机无 `.copy()`。clone ≠ 原对象；`data_ptr` 不同；`add_` 后原张量不变；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states` 长度 4。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.686\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False`；`SubprocessExecutor is ChildProcessExecutor`。默认 `score_code` → `executor_unavailable` / `value=None` |
| X19a | `execute_repair_tiny` Prefill hidden | 返回 32 维有限非零 `prefill_hidden`；`refilled_prefix=True`。dummy execute 无 hidden → `prefill_unavailable`。`prefix_token_ids` 旁路仍可把 `refilled_prefix=True` 且无 hidden |
| X19b | Prefill KV | `output_hidden_states=True` 后 `past_key_values.get_seq_length()==prefix_len`（本例 12=12）。decode 使用该 cache。hidden **取最后一层** last-token，与 readout 层 \(\|\Delta\|\approx 5.54\) |
| X19c | scientific CLI repair | `k=1..5` 均 `refilled_prefix=true` / `status=ok`；`extra_prefill_tokens` 皆 32；slots 随 k 增长至 `{p1,p2,q}`。落盘 **无** `prefill_hidden` 字段 |
| X20 | `weight_seed` | 同 seed 同 ids → \(\|\Delta H\|=0\)；异 seed 同 ids → 0.391；同 seed 异 ids → 0.199。CLI collect **写死** `weight_seed=0` |
| X21 | 来源-数值 | `cmd_prepare` 仍执行 `make_source_value_pair(...) if premise_id else None` 并丢弃返回值。donor 规则仍是 `H[0],H[1]` |
| X22 | scientific 事件跨度 | 问句单行：`p1`/`p2` 皆 `start=0,end=44,status=ambiguous`，span 吃进整行乱码；`q` 在 `\nq = 82`（45/49/51）。`ids[:16]` 对 `q` 前缀（45 token）会截断；本轮 scientific 因 X14c 未走到该 hook |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server` |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存。属 `pending_server` |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机 donor 不是来源-数值条件 |
| 全量 pytest（作者称 136） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| A5-08 / F5-02 / D5-04 几何 timing / 主 hook 层 | 几何 `timing` 保持 `offline_hidden`；hook 不把它改成 `pre_step`；主 hook 用 readout 不是弱层 | **接线关闭（有 donor 的路径）。** fixture tiny：hook 打在 readout 层 1，几何字段仍是 `offline_hidden`（X14b）。scientific 指定复跑未进入 hook（D6-02），该路径写的是 `unexpressible` 而不是 `pre_step` |
| E5-11 tiny collect re-encode `trace.text` | collect 对文本再编码 | **关闭。** CLI `encode_text(trace.text)` 后才 `collect_hidden_trace`（X8d/X8g） |
| E5-12 `H_pre_*` 跨轨迹堆叠 | 按事件行 vstack | **关闭。** scientific `(18,32)` = 6×3 事件（X8e） |
| A5-01 / D5-03 步边界 \(H\) / 禁末 token | scientific 有事件；collect 拒绝 last-token `pre_step` | **库层与行数关闭；配对未关。** 空事件为 `no_event` 空矩阵；scientific 拒绝无事件；`q` 行是步前隐状态且 ≠ 末 token。但 12 个前提事件步前不可表达，`H[0]/H[1]` 为 NaN（D6-02、D6-03） |
| A5-09 Prefill 有 hidden | `refilled_prefix` 需要 prefill hidden | **接口关闭。** `execute_repair_tiny` 产出有限 hidden 且 decode 用 Prefill KV（X19）。CLI jsonl 不落盘该向量；`prefix_token_ids` 旁路仍可不经 hidden 标已 Prefill |
| D5-02 C-layer | 弱层是对照不是主干预 | **主 hook 接线关闭 / 对照协议未关。** 有分数时主 decode 仍 readout（X14b）。C-layer 仍是同向量 QR，RNG 种子用 `5+weak`，并写 `dev_weak_layer`（D6-05） |
| D5-04 / D5-05 swap 接线与 donor | 假前缀 / 序号 ids / 非事件配对 | **假前缀在 fixture 关闭**（14-token 真步前）。scientific donor 规则仍毁实验（D6-02）。`make_source_value_pair` 仍丢弃（D6-04） |
| D5-07 StreamBank | 方向流 ≠ hook 基 | **未关**（X13、D6-06） |
| A4-13 `ChildProcessExecutor` | 不是 `IsolatedExecutor` | **仍关闭**（X18） |
| A5-14 Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |
| pending_server | 真实权重 / Linux cgroup / 实测 P1–P3 | **同意未关。** tiny 随机权重不是 MODEL-01 |

相对 r05 已关闭、本轮不再单列缺陷：空事件末 token 回退并自称 `pre_step`；CLI `"follow donor"` 假前缀（fixture 路径）；主 \(\Pi_Z\) 打到弱层；有事件时三位置只写 metadata；hook 为 `+0.01`；默认 `clayer_status=dev_weak_layer` 谎言标签。

## 6. 发现

### D6-01 — 声称冻结 hash 已复现（本轮非缺陷）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `.planning/audits/round-06/VERSION.md` 声称与本机 59 文件 rel+NUL+bytes 一致
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。
- **影响：** 审查对象可锚定到声称快照。不因此放行科学实现。

### D6-02 — 指定 scientific collect→intervene 因 `H[0]/H[1]` 全 NaN 跳过，\(\Pi_Z\) 未施加

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **712–713、732**（`allclose(..., equal_nan=True)` 后保持 `donor_missing` / `unexpressible`）；`collect.py` **50–54、55–58**（`token_index is None` → NaN 行仍进入 `H`）；`events.py` **39–41、75–89**（单行多赋值共享 `start=0`）
- **触发条件：** `prepare --eval-mode scientific` 之后的 `collect --backend tiny` 再 `intervene --backend tiny`（本通道指定复跑）
- **对应要求：** CAUSAL-01；论文 §2.4 执行协议
- **证据：** X8e、X14c、X22。6 条轨迹均可解析，18 个事件行已堆叠，6 个 `q` 步前有限且 ≠ 末 token——这关闭了 r05「scientific \(H\) 塌成末 token」的库层半截。但 `H` 按事件出现序压栈，前两行是同一问句里 `p1`/`p2` 的不可表达步前（全 NaN）。intervene 把它们当成 donor 对，`equal_nan=True` 判相同，**hook 零次**，范数/结局/relative 全空。`test_intervene_tiny_geometry_timing_stays_offline` 在此路径上因 `timing != "pre_step"` 而绿。相对 r05（当时末 token \(H\) 可区分、hook 会跑），这是步边界修复后的**配对回归**。
- **影响：** 作者用来关闭 D5-03 的 scientific 路径现在证明不了交换。有限的 `q` 行（下标 2/5/8/…）从未被选作 donor。
- **建议：** 只配对可表达、事件身份对齐的步前行；不可表达行不得进入 donor 槽。无合格对时保持 `donor_missing`，不要用测试 `!= pre_step` 冒充已干预。

### D6-03 — 来源-数值条件仍未写入；donor 仍是 `H` 前两行

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **321**（`make_source_value_pair(...)` 返回值丢弃）、**712–713**（`H[0],H[1]`）；`edits.py` **204–216**
- **触发条件：** 任何声称 C2 / 来源跟随的 intervene
- **对应要求：** CAUSAL-02；论文 §2.4 donor 协议；GOAL §5.10；协议 §4
- **证据：** X21、X8d、X14b。构造函数存在且被调用，产物不进 traces。fixture 因 re-encode 得到可区分的两个 `q` 步前（不同 `p2`/`q` 字面），这是「两条轨迹各取第一事件」，不是解耦队列。scientific 前两行甚至不是 `q`。真实 50 条保持 `pending_server`。
- **建议：** 按事件身份配对；每个数值条件独立提取；记录层、token、可见前缀与 `weight_seed`。

### D6-04 — INLP / rescue 未进入生成；`ie_z` 仍不是 \(\mathbb E[g(Y)]\)

- **状态：** residual / confirmed defect（接线）
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **733–740、775–781**；`collect.py` `intervene_swap_decode` **167–173**（hook 只 `apply_swap`）；`interventions.py` `ie_z` **88–89**
- **触发条件：** tiny/scientific `intervene`
- **对应要求：** CAUSAL-01；INLP-01；IE-01
- **证据：** X11、X14b、X_inlp_wiring。算法本身（迭代零空间、三项救援范数）可复核。CLI 只对 numpy 向量做 `inlp_remove`/`rescue_controls`，投影不进 `resid_post`。`ie_z` 是救援隐向量均值差。对照四项保持 null，相对 C-rand/C-layer 的差值无法计算。
- **建议：** 同一事件步前分别跑 swap / INLP / `rescue_controls` 的 decode；由生成文本算四项；`ie_z` 用预指定 \(g\)。

### D6-05 — 主 hook 已固定 readout；C-layer 仍无第二次前向却可写 `dev_weak_layer`

- **状态：** closed（主干预接线） / confirmed defect（对照协议）
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **719–728、763–764**（`main_layer = readout_layer_index(3)`；`c_layer_delta` 用 `rng(5+weak)`）；`interventions.py` **46–49**
- **触发条件：** `--dev-layer-scores 0.05 0.9 0.8` 的 fixture tiny intervene
- **对应要求：** 论文 §2.4；GOAL §5.11；IE-01；本轮口令「弱层是对照不是主干预」
- **证据：** X12、X14b。弱层选择正确为 0；**主 decode hook 仍是层 1**——r05「主干预被接到弱层」本机关闭。C-rand/C-layer 没有第二次前向；三项范数锁成同一值（fixture 0.003838）。有分数时标签改 `dev_weak_layer`，实际只是换了 QR 种子。
- **影响：** 「弱层不是主干预」成立。「弱层是对照」不成立——对照仍是同向量第二种随机投影。
- **建议：** 主干预固定读出层；C-layer 用该弱层 \(H\) 另跑同秩、同位置、同范数、同采样流的一次 decode。未做第二次前向时不要写 `dev_weak_layer`。

### D6-06 — StreamBank 只驱动几何 RNG；采样流与 hook 基未共享

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **702–718**；`collect.py` **167、175–178**
- **触发条件：** 「所有处理条件同一采样流」（论文 §2.4；GOAL §5.4/§5.10）
- **证据：** X13。落盘 `main_norm` 来自 StreamBank `direction` 基；实际 hook 用 `default_rng(1)`。`sample` 流空闲。patched/baseline 虽共用 torch seed，C-rand/C-layer 没有 decode 条件。
- **建议：** 记录并复用采样配置；方向流与采样流隔离；报告范数必须来自**实际写入 hook** 的那组基。

### D6-07 — scientific 同行多赋值使多数步前不可表达；`ids[:16]` 会切掉真 `q` 边界

- **状态：** confirmed defect（事件跨度 / hook 前缀）
- **严重度：** medium
- **文件 / 符号 / 行号：** `events.py` **39–41**（行首作 `start`）；`generate.py` **122–139**（问句保持单行 + 乱码无换行）；`cli.py` **756–764**（`events[0]` + `ids[:16]`）
- **触发条件：** scientific 问句 `p1 = 4. p2 = 0. What is q = ...`；或任何 `event.start > 16` 的 hook
- **对应要求：** POS-01；论文 §2.4 步前边界
- **证据：** X22、X14b。`p1`/`p2` 共享 `start=0,end=44`，status=`ambiguous`，`post_step` token=43（整行含生成乱码）。`q` 步前 index=44，前缀 45 token。fixture 碰巧 `start=14<16`，前缀完整。若 scientific 用 `q` 作 `events[0]`，hook 仍会切成前 16 字并自称 `event_aligned`（内部 `timing=pre_step`，几何字段另论）。
- **建议：** 赋值跨度用 match 行内边界，不要整行；hook 前缀取目标事件步前 token，禁止静默 `[:16]`。

### D6-08 — hook 元数据写入后被 `intervention_report` 覆盖

- **状态：** confirmed defect（可观测性）
- **严重度：** low
- **文件 / 符号 / 行号：** `cli.py` **765–779**
- **证据：** X14b。`hook_once`/`transform`/`hook_timing`/`weak_layer` 先写入 `report`，随即 `report = intervention_report(...)`。落盘 `relative` 只剩结局骨架与事后补回的 `ie_z`/`inlp_rank`/`followed_donor`。独立审查必须 monkeypatch 才能看见层号。
- **建议：** 合并字典，不要替换。

### D6-09 — CLI collect 写死 `weight_seed=0`

- **状态：** residual defect
- **严重度：** low
- **文件 / 符号 / 行号：** `cli.py` **448**；`cmd_prepare` **286–289** 读取 `--weight-seed`
- **证据：** X20。同 seed 契约本身成立。prepare 与 collect 默认都是 0 时本机对齐；一旦 prepare 传入非 0，collect 仍用 0，几何与生成权重脱钩。
- **建议：** collect 读同一 `weight_seed` 并写入 spec。

### D6-10 — thinking 抽取仍正确；模板 / `think_ids` / `load_frozen` / `clone_cache` 仍未接入

- **状态：** residual defect（模板路径） / closed（`extract_answer`）
- **严重度：** medium（模板；真实 HF 为 pending_server）
- **文件 / 符号 / 行号：** `events.py` **247–261**；`generate.py` **185–191、122–132**；`adapters.py` **10、18、32–42**
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
| U-06 | scientific 连续 k 的 `extra_prefill_tokens` 皆 32 | 更偏修复预算/截断，不单独升格为因果缺陷 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是** MODEL-01 完成 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 向量公式与 fixture 步前 \(\Pi_Z\) decode | 无来源-数值 donor，scientific hook 未跑，无四项对照实测 |

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
| N-11 | 关闭（过程） | 冻结 hash 按 VERSION 脚本复现（HASH_MATCH） |
| N-12 | 非缺陷 | `--backend offline` 的 `H` 是前缀 id 且标注 `offline_prefix_ids`；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 是随机初始化隐状态并标注 `random_init`。这是本机接口证明，不是 MODEL-01 完成 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 默认 `clayer_status=dev_scores_missing`（有分数时的过称见 D6-05） |
| N-16 | 关闭（有事件且可表达） | fixture 三位置与 span `E` 是读出层隐状态；scientific `q` 行亦然，且 ≠ 末 token |
| N-17 | 关闭（算法 + fixture 接线） | tiny hook 变换是 \(\Pi_Z\)；fixture 前缀是 `text[:event.start]` |
| N-18 | 关闭（接口） | `execute_repair_tiny` 重新 Prefill（含 hidden 与 KV）再 decode；dummy/offline 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| N-20 | 关闭（r05 声称，本轮独立核验） | collect **re-encode** `trace.text`；`H_pre_*` 跨轨迹按事件堆叠；主 hook **readout 层 1** 而非弱层；几何 `timing` 在 hook 路径保持 **`offline_hidden`** |
| N-21 | 关闭（库层） | 空事件不再写成 last-token `pre_step`；scientific collect 拒绝无事件 |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` / `forbid_host_exec` 无生产调用方 |
| S-03 | stub | `rescue_controls` / `inlp_remove` 有 CLI numpy 调用，不进入 hook |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道不通过（FAIL）。冻结：HASH_MATCH。**

相对 round-05，r05 四句声称在本机**独立成立**，不得按 r05 原文原样重开：（1）scientific / fixture collect 的 \(H\) 是事件步前隐状态并按事件堆叠，空事件为 `no_event` 空矩阵，scientific 拒绝 offline 前缀与无事件；可表达的 `q` 三位置互异且 ≠ 末 token；（2）tiny collect **re-encode** `trace.text`，fixture 不再因序号 ids 得到全等 \(H\)；（3）有 donor 时主 `resid_post` hook 打在 readout 层 1，传入弱层分数也不改主层；几何字段保持 `offline_hidden`，不被 hook 改写成 `pre_step`；（4）`execute_repair_tiny` 的 Prefill 带有限 hidden，且 KV `seq_length` 等于前缀。另：\(\Pi_Z\) 公式、once hook、KV 范围、`weight_seed` 复现、默认 `dev_scores_missing`、`ChildProcessExecutor` 未冒称隔离、Gate 未注册——均保持。微型随机权重按口径不算 MODEL-01 完成。

这些不够支持 CAUSAL-01/02 的指定复跑。scientific `H[0]/H[1]` 是同行 `p1`/`p2` 的 NaN 步前，intervene 整段 `donor_missing`，\(\Pi_Z\) **零次**施加；回归测试被 `timing != pre_step` 放行。来源-数值对仍丢弃。INLP/rescue 停在 numpy，`ie_z` 不是结果量。C-layer 仍无第二次前向。StreamBank 不解释 hook 基。`ids[:16]` 与同行事件跨度在 scientific `q` 上会切错边界。诚实的 fixture 几何/接口演示仍不是前瞻因果实验。
