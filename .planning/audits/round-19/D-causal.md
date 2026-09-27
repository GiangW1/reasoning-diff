# D-causal 独立审查报告（round-19）

通道 D：模型与因果（token/prefix、thinking 模板、sampling、hook/KV、donor 来源、swap/消融/救援、两类对照、nontarget/invalid）。指定独立复跑 scientific `prepare`→`collect --backend tiny`→`intervene --backend tiny`（另跑 `--dev-layer-scores 0.05 0.9 0.8`）→`repair --eval-mode scientific`，夹具 `tests/fixtures/t1_tiny.json`，`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15`。复跑目录**必须**名为 `stage_a` / `stage_b`，**禁止**兄弟目录叫 `prep` / `prepare` / `s-prep`。

点名猎项：无静默 generate 48 截断；无静默 intervene 64 截断，超长前缀必须 raise 不得 slice；XOR 保留叶 *a*、追加等值 *b*；重叠 rename 必须同时替换；配对只读给定 `in-dir/edits.jsonl`；跳过全 NaN \(H\) 行；`pi_z_swap` / INLP \(h@P\) / `add_delta` / `replace`；C-rand/C-layer 锁到主干预实际范数；仅生成区事件且 `parse_region=generated`；Prefill 拒绝标量/bool/`[0]`；教师强制诚实标 `constrained_target`，不是 §4.1 / MODEL-01；`IsolatedExecutor` ≠ `ChildProcessExecutor`。

独立性声明：未阅读 `.planning/audits/round-19/` 下除 `VERSION.md` 与本文件外的其他通道报告。只把 `VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明 / 作者台账，不把作者 `local close` 当关闭。对照读了本通道 round-18 报告仅作版式与猎单结构，不作本轮证据。未修改 `src/`、`tests/` 或 `pyproject.toml`。绿测试不是论文正确性。微型随机权重是本地接口证明，**不是** MODEL-01。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。约束 `\nq = <digit>` **不是** §4.1 自然 CoT。

对照原文：论文 §2.4（\(H'=H_b+\Pi_Z(H_d-H_b)\)、C-rand/C-layer 同批次）、§4.1（自然 CoT，本机不得冒称）、§4.2 / 第 5–6 节（三位置；前瞻交换）、第 6/8 节（来源—数值 / Knock-out / Rescue）；GOAL MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01；`docs/EXPERIMENT_PROTOCOL.md` §4；GOAL §5.15（普通子进程不得冒称隔离沙箱）。tiny 路径只验收接口与接线，不验收 MODEL-01。

**先行结论：** 按 `.planning/audits/round-19/VERSION.md` 原文脚本复算，开审与交卷均为 **HASH_MATCH** `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`（61 文件，0 CRLF）。指定 scientific 路径在无 `prep` 兄弟的 `stage_a`/`stage_b` 上独立复跑，点名猎项全部成立，含本轮新增的 intervene 超长 raise 与重叠 rename 同时替换。未发现需改冻结集的本通道缺陷。

**总裁决：PASS。HASH_MATCH。点名猎项关闭。tiny 不是 MODEL-01。不宣布 Goal 完成。本通道单独不得启动连续通过计数。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal（孤立 subagent 上下文） |
| 审查时间 | 2026-09-21（Asia/Shanghai）；开审约 03:09，交卷约 03:28 |
| 声称冻结 hash | `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`（`.planning/audits/round-19/VERSION.md`；61 文件；POSIX relpath + NUL + bytes） |
| 开审复算 | **HASH_MATCH。** 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → **61** 文件 → `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb` |
| 交卷复算 | **HASH_MATCH。** 同脚本 → 61 文件 / 同一 digest。开审与交卷之间本通道未改冻结集 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；`src/`/`tests/`/`pyproject.toml` 为未跟踪。HEAD 不是冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载；无 CUDA |
| 作者 pytest 声称 | 165 passed。本机全量 **165 passed / 20.12s / exit 0**。绿只锁回归，不是论文正确性 |
| 明确未读 | `.planning/audits/round-19/` 下除 `VERSION.md` 与本文件外的其他通道报告 |

因果生产文件 SHA-256（交卷 = 开审）：`cli.py` `95c58b934e1aceeb`（61685 B / 1267 行）、`edits.py` `cc8e2d23592a3ab8`（13905 B / 367）、`collect.py` `83658cd8ba879f20`（261）、`generate.py` `6e6040394ac641c7`（200）、`tiny.py` `c75d0f5325766612`（120）、`features.py` `0a9f0b8beb0185ae`（39）、`adapters.py` `c1992624026a1bf0`（42）、`tokenize.py` `b0cc8974af1010fa`（31）、`interventions.py` `0ffdbb8805be7649`（115）、`repair.py` `f76ff9998b9a6b17`（232）、`events.py` `290a4fd676ac0814`（274）、`executor.py` `481d6ed597c93e78`（109）、`rng.py` `2098c2c72a852eaa`（53）。全部 0 CRLF。相对 r18 冻结，本轮实质改动在 `cli.py`（intervene 拒截断）与 `edits.py`（`_rewrite_ids` 同时替换）。

复跑目录（本通道自建）：`.planning/audits/round-19/_d_scratch/{stage_a,stage_b,stage_int,stage_int_dev,stage_rep,stage_off,stage_no_edits}`。兄弟名只有这些加 hunt 脚本；**没有** `prep` / `prepare` / `s-prep`。`stage_a` = prepare，`stage_b` = collect（`--in-dir stage_a`），intervene / repair 的 `--in-dir` 是 `stage_b`。

## 2. 范围与逐文件覆盖

指派阅读并逐行核对（行号为本冻结字节）：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / 卡片 `think_ids` / `load_frozen(..., local_files_only=True)`。`revision=="latest"` 拒绝 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids`（**非互逆**）/ `readout_layer_index`（60%–75% 带）/ `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–261 | `collect_hidden_trace` 不可表达步前 **continue**；`intervene_hidden_decode` 四 mode：`pi_z_swap` / `inlp`（`vec @ proj`）/ `add_delta` / `replace`。`_hidden_at_layer` 仍按 `max_position_embeddings`（tiny=128）切片，不是点名的 48/64 |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–200 | `sample_next`；`decode_loop`（独立 `torch.Generator`）；`append_target_assignment`；`len(prompt_ids)>96` **raise**，无 `[:48]`；只解析生成区；`apply_model_template` 有定义，CLI / `generate_task_trace` **无调用** |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step`。`max_position_embeddings=128` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / `inlp_remove` / `rescue_controls` / `select_weak_layer` / 库函数 `ie_z`（隐向量均值）/ `intervention_report` |
| `src/reasoning_diff/edits.py` | 109–367 | `apply_value_edit`；`_rewrite_ids` 一次正则同时替换；`apply_rename_edit`；`apply_alt_source_same_value`（保留叶 *a*、固定名 `src_b`、父母改读 *b*）；`make_source_value_pair` |
| `src/reasoning_diff/repair.py` | 1–232 | `_hidden_is_prefill` 拒绝标量/bool/`[0]`；`execute_repair_tiny`；`run_repair` |
| `src/reasoning_diff/cli.py` | 187–226、257–551、687–700、722–728、817–1062 | `_domain_edit` / `_allowed_edits`；prepare（含 `trace-source`）；collect 复制 `edits.jsonl`；`_tiny_prefix_ids` 超 `limit=96` **raise**；`_load_source_value_pair` 只读 `in-dir/edits.jsonl`；`_pair_source_value` 跳过非有限行；intervene / repair |
| `src/reasoning_diff/executor.py` | 1–109 | `ChildProcessExecutor.isolated_sandbox=False`；**不是** `IsolatedExecutor` 子类；默认 `UnavailableExecutor` |
| `src/reasoning_diff/rng.py` | 41–53 | StreamBank `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/events.py` | 27–89、251–274 | `parse_events`；`boundary_index`；`extract_answer` 去 think |
| `src/reasoning_diff/schema.py` | 39 | `POSITION_KINDS` |

支持性阅读：论文 §2.4 / 第 6、8 节；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` 上列要求；`docs/CURSOR_GOAL_PROMPT.md` §5.10–5.15。未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次、自然 CoT。未逐行审计：`analysis.py`、`probes/bilinear.py`、`transfer.py`、`measure.py`、`splits.py`（他通道）。`cli.py` 校准/fit 段属其他通道。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | VERSION 脚本逐字复算 | **开审 HASH_MATCH** 61 / `b6db632f…96569eeb`（0 CRLF）。**交卷 HASH_MATCH** 同一 digest |
| X2 | 全量 pytest | **165 passed / 20.12s / exit 0**，与作者数字一致。仍不是论文正确性 |
| X3 | `apply_swap` 标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\) |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.178\)、\(\Delta V_{\max}=0.320\)，且 **仅 last token**（earlyK=0） |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3** 次；`once=True` **1** 次 |
| X7 | hook `finally` 清理 | 正常与 `RuntimeError` 后 `_forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)` |
| X8c | 空事件 / `start=0` | `h_position=no_event`，\(H\) `(0,32)`，不塌成末 token。`boundary_index(...,0,"before")` 为 None；`select_prefix_index` `expressible=False` |
| X8e | **指定** scientific `prepare`→`collect --backend tiny --weight-seed 0`，目录 `stage_a`→`stage_b` | 6 条轨迹：`trace-base` / `trace-t0p` / `trace-edit` / `trace-source` / `trace-edit:…:p1:0` / `trace-edit:…:p2:2`。每条 **1** 个生成区 `q`（base/edit `start=45`；source `58`；`parse_region=generated`，`parse_status=constrained_target`）。问句前提不进入事件。`H` `(6,32)` **6/6 行有限**（0 NaN）；`H_pre_step/value/post` 同样 0 NaN 行。`event_rows.jsonl` 6 行皆 `{node_id:q, trace_id:…}`。`hidden_layer=1`；`weight_source=random_init`；`weight_seed=0`。\(\\|H_0-H_1\\|\approx 0.00778\)，\(\\|H_0-H_2\\|\approx 0.00430\)，\(\\|H_0-H_3\\|\approx 0.01049\) |
| X8f | scientific collect 拒绝 | `--backend offline` → `ValueError: scientific collect refuses offline_prefix_ids as H`（exit 1，`stage_off`） |
| X8g | re-encode vs 生成 ids | base 轨迹与 `encode_text(text)` 有 **8** 处不同（恰 `max_new=8` 乱码段）。collect 的 \(H\) 是对表面文本的二次前向 |
| X8h | 步前 vs 前缀前向 | `H[0]` 与 `encode_text(text[:45])` 末 token **逐位相等**（\(\Delta=0\)）；与步尾 \(\\|\cdot\\|\approx 0.147\) |
| X9 | `leaks_target` | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None` |
| X10 | `boundary_index` | `start=0,"before"` → **None** |
| X11 | INLP / rescue 算法 | 随机向量上 \(h@P\) 与 `apply_swap` 最大差 **0.655**（不是同一变换）。库函数 `ie_z(H_3,H_0)\approx -3.07\times 10^{-4}`；**CLI tiny 路径不写该值** |
| X12 | C-rand / C-layer 范数与弱层 | 缺范数仍 `ValueError`（`C-rand requires the actual main-intervention norm`）。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0`。独立重算 `crand_norm=clayer_norm=0.002791401781066686`，与 `stage_int` / `stage_int_dev` 落盘逐位一致；主干预范数 `0.0027914017810666864`（`scale_to_norm` 后对照锁到该值） |
| X13 | StreamBank vs hook 基 | `direction` 第一抽丢弃；第二抽 **basis_seed=1153799966**。`sample` 第一抽 **1191642646** |
| X14c | **指定** collect→intervene（**无** `--dev-layer-scores`），`--in-dir stage_b` | `_load_source_value_pair(stage_b)` 读到 pair（`edits.jsonl` 与 `stage_a` 逐字节相同，4629 B）。`_pair_source_value` 返回 **`(0, 3, same_value_diff_source)`** = `trace-base` / `trace-source`。`status=prospective_decode`，几何 **`timing=offline_hidden`**。`relative.hook_once=resid_post`，`transform=pi_z_swap`，`hook_timing=pre_step`。`clayer_status=dev_scores_missing`。`ie_z=0.0`，`ie_z_g=target_follow`。对照四项因 clayer 空而 **null**。`prefix_truncated=false`。无 `prep` 兄弟 |
| X14d | 另跑 `--dev-layer-scores 0.05 0.9 0.8` | 独立复放 5 次 decode，层 **1 / 1 / 0 / 1 / 1**，模式 **`pi_z_swap` / `add_delta`(C-rand) / `add_delta`(C-layer) / `inlp` / `replace`**。`clayer_status=dev_weak_layer_decode`，`weak_layer=0`。相对四项 `vs_crand=vs_clayer=0.0`。`donor_kind` 仍为 `same_value_diff_source`，`donor_rows=[0,3]` |
| X14e | 跳过全 NaN 行 | 把 source 行 `H[3]` 置为全 NaN 后，同一 pair 元数据返回 **`(0, 2, same_source_diff_value)`**（跳过不可用 source 行）。全矩阵 NaN → `_pair_source_value` / `_expressible_donor` 皆 **None**（不选 NaN donor） |
| X14f | 无 `edits.jsonl` 的目录 | `_load_source_value_pair(stage_no_edits)` → **None**。不走兄弟 `stage_a` |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 后数字 → 7；未闭合 → None；`\\boxed{7}` → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 与 `generate_task_trace` 无调用**。本轮不要求自然 CoT |
| X16 | `clone_cache` | clone ≠ 原对象；`get_seq_length()=3`。生产路径不调用 |
| X17 | 读出层 | 3 层 → `readout_layer_index=1` |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类（`issubclass=False`），`isolated_sandbox=False` vs 基类 `True` |
| X19 | Prefill | `execute_repair_tiny` 返回 **32** 维有限非零（\(\\|h\\|\approx 5.65\)）。`run_repair` 接受该向量。`0` / `True` / `False` / `1.0` / `[0]` / `[0.0]` / `[]` / `None` / `"x"` / 长度 1 向量 → `_hidden_is_prefill=False`；谎称 `refilled_prefix=True` 仍写 `prefill_unavailable`。scientific CLI repair k=1..5 皆 `refilled_prefix=True`、`status=ok`、`gated=False`、`extra_prefill_tokens=32`；jsonl **无** `prefill_hidden` 字段 |
| X20 | `weight_seed` | 同 seed 同 ids → \(\\|\Delta H\\|_{\max}=0\)；异 seed → 0.099；同 seed 异 ids → 0.072。CLI collect 写入 spec `weight_seed=0` |
| X21 | 来源-数值 / keep-*a* add-*b* | `edits.jsonl` 含 `kind=source_value_pair`：`trace_ids={base:trace-base, same_source_diff_value:trace-edit, same_value_diff_source:trace-source}`。source 臂 `kind=same_value_diff_source`，问句 `p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?`（**49** 字符，含完整 `* src_b`），premises 保留 `p2` **且** 有 `src_b`，parents `q←{p1,src_b}`，表达式 `p1 * src_b`，答案值仍 **0**。rename 对照问句为 `p1 = 4. src_b = 0. What is q = p1 * src_b?`，**丢掉**叶 `p2`。`make_source_value_pair` 调 `apply_alt_source_same_value`，不调 `apply_rename_edit` |
| X22 | 事件跨度 / 无 generate 48 截断 | 生成区 `q` 跨度 45–（source 58）；`prefix_truncated=false`。6/6 `start ≥ len(prompt_text)` 且 `start ≥ prompt_len`。`generate.py` 无 `[:48]`；`>96` raise。source `prompt_len=49`（若仍静默切 48 会丢掉 `* src_b` 尾部）。127 token 问句独立调用 `generate_task_trace` → `ValueError: tiny prompt exceeds context; refuse truncated source/value prompts` |
| X22b | **无 intervene 64 截断；超长 raise** | `src/reasoning_diff` 无 `ids[:64]` / `[:64]`。`_tiny_prefix_ids` 默认 `limit=96`：65 token 前缀原样返回（旧 64-cap 会切开）；97 token → `ValueError: tiny intervene prefix exceeds context; refuse truncated prefixes`。CLI intervene 写 `prefix_truncated=false`，本夹具 base 前缀 45 token |
| X22c | **重叠 rename 同时替换** | `_rewrite_ids("p1 = 4. p2 = 0. What is q = p1 * p2?", {p1:p2,p2:p1})` = `p2 = 4. p1 = 0. What is q = p2 * p1?`。`apply_rename_edit` 同结果；premises `[p2,p1]`，parents `{p2,p1}`，表达式 `p2 * p1`。顺序替换会塌成全 `p1`，本实现是一次正则 |
| X23 | \(g(Y)\) / `ie_z` | donor/base 轨迹 `answer` 皆为约束赋值 **「82」**（seed=0，不是金答案 0）。intervene 主/对照/INLP/rescue/C-layer 抽取答案皆 **「9」**，`followed_donor` 对主干预为 false。`ie_z=1{9==82}-1{9==82}=0`，`ie_z_g=target_follow` |
| X24 | INLP hook 不是 swap | 间谍 `out == in @ P`（atol 1e-5，最大差 0），`out ≠ in`。CLI `mode="inlp"`，无 donor。2 点拟合 `inlp_rank=30` |
| X25 | 教师强制 / 采样 | `target_assignment='\nq = 82'`（t0p 为 `\nq = 53`）；`parse_status=constrained_target`；`correct=false`（金标 0）。6 条 `sampling={temperature:1.0,top_k:0,top_p:1.0}`。`decode_loop` 用独立 `Generator`。intervene decode **不再**教师强制 |
| X26 | 问句单独解析 | 对 6 条 `prompt_text` 用对应 task 跑 `parse_events` 会打出 p1/p2（source 问句为 p1/`p2`/`src_b`）。generate **不解析问句**，故这些不是生成事件 |
| X27 | 卡片 revision | `qwen3-8b` `b968826d9c…` think `(151667,151668)`；`r1-distill-qwen-7b` `916b56a4…` think `(151648,151649)`。本机未加载。缺名 `card` 抛 `KeyError` |
| X28 | collect 复制 edits | `stage_b/edits.jsonl` 存在且与 `stage_a/edits.jsonl` **逐字节相同**。intervene 只读 `stage_b` |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验卡片 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server`。本轮不要求自然 CoT |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存；CLI 未调用。属 `pending_server`。tiny **不是** MODEL-01 |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机是接口证明 |
| 把 165 passed 写成 Goal / MODEL-01 验收 | 绿测试不是论文正确性 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

`ISSUES.md` 只当作者主张。

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| F18-03 | `_rewrite_ids` 同时替换；`{p1:p2,p2:p1}` → `p2 = 4. p1 = 0. What is q = p2 * p1?` | **指定路径独立关闭。** X22c |
| F18-08 | intervene 不再 `ids[:64]`；超 96 token 拒绝 | **指定路径独立关闭。** X22b。65 token 不被切开；97 token raise |
| F18-12 | `_find_labels_jsonl` 只读给定目录 | **不裁定。** 非本通道猎项（校准/标签查找） |
| F15-01 | collect 复制 `edits.jsonl`；`_load_source_value_pair` 只读给定 `in-dir` | **指定路径独立关闭。** X14c/f、X28。无 `prep` 兄弟时 donor 仍为 `same_value_diff_source` |
| A14-02 | 保留叶 *a*，追加等值 `src_b`，父母改读 *b* | **指定路径独立关闭。** X21、X22。不是 rename |
| D14-05 | generate 不再 48 字符截断 | **指定路径独立关闭。** X22。source 问句 49 字符且含完整 `* src_b`；超 96 raise |
| A13-01 | 来源臂不是 rename-only；intervene 优先 `trace-source` | **指定路径独立关闭。** X14c/d、X21。有 source donor 时不是 value-edit-only |
| A14-03 / A14-04 | fit / excess | **不裁定。** 非本通道猎项 |
| pending_server | 真实权重 / 50 条 C2 / 官方 CoT | **同意未关。** 约束 `q` 不是 §4.1；tiny 不是 MODEL-01 |
| Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |

## 6. 发现

### D19-01 — 无静默 generate 48 截断；超长 prompt raise

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **124–125**（`len(prompt_ids)>96` raise；全文无 `[:48]`）；**122–123、183**（整段 `task.question` 编码）
- **对应要求：** 点名猎项「No silent generate 48-cap」；作者 D14-05
- **证据：** X8e、X21、X22。source `prompt_text='p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?'`，长度 **49**，`prompt_len=49`，尾部 `t is q = p1 * src_b?`。若仍静默 `[:48]`，会切掉 `* src_b` 的尾字符。127 token 问句 raise，不切片。`src/reasoning_diff` 内无 `[:48]`。`tiny.max_position_embeddings=128`，本条 64 token 全文未触顶
- **影响：** 指定路径不再用 48 字符丢掉改写式。这不是自然 CoT

### D19-02 — 无静默 intervene 64 截断；超长前缀 raise 不 slice

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **722–728**（`_tiny_prefix_ids`：`len(ids)>limit` → `ValueError`；默认 `limit=96`）；**958–959**（intervene 调用后写 `prefix_truncated=false`）
- **对应要求：** 点名猎项「No silent intervene 64-cap. Overlong prefix must raise, not slice」；作者 F18-08
- **证据：** X14c、X22b。冻结树无 `ids[:64]` / `[:64]`。65 token 前缀长度保持 65（旧 64-cap 会切开）。97 token 前缀 raise `tiny intervene prefix exceeds context; refuse truncated prefixes`。本夹具落盘 `prefix_truncated=false`
- **影响：** 指定 intervene 路径不再静默切 64。collect `_hidden_at_layer` 仍按 128 切（见 U-05），不是本猎项

### D19-03 — XOR 保留 *a*、追加 *b*；重叠 rename 同时替换；配对不依赖兄弟 `prep`

- **状态：** closed（点名配对、图构造、重叠 rename） / residual（夹具级换源，不是 50 条独立计算源）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `edits.py` **151–157**（`_rewrite_ids`：按长度降序一次正则，`mapping[match]` 同时替换）；**160–213**（`apply_rename_edit`）；**221–294**（`apply_alt_source_same_value`：固定 `src_b`、保留原叶、父母改读 *b*、目标值不变）；**297–304**（`make_source_value_pair` 不调 rename）；`cli.py` **521–524**（collect 复制 `edits.jsonl`）；**826–830**（只读 `in-dir/edits.jsonl`）；**833–856**（键序 `same_value_diff_source` 先于 `same_source_diff_value`；非有限行不入 index）
- **对应要求：** CAUSAL-02；点名「XOR keep-a add-b；overlapping rename simultaneous」；作者 F18-03 / F15-01 / A14-02
- **证据：** X14c/d/f、X21、X22c、X28。
  - 复跑目录无 `prep`/`prepare`/`s-prep`；intervene `--in-dir stage_b`
  - pair 元数据 `base→trace-base`、`same_source_diff_value→trace-edit`、`same_value_diff_source→trace-source`
  - 选中行 `(0,3)`，\(\\|H_0-H_3\\|\approx 0.01049\)，`allclose=False`，两行有限
  - **未选** 更近的 base–edit \(0.00430\)，也 **未选** base–t0p \(0.00778\)
  - 缺 `edits.jsonl` 的目录返回 None，不读兄弟 `stage_a`
  - source 问句保留 `p2 = 0` 并追加 `src_b = 0`；rename 对照丢掉 `p2`
  - `required_sources_before=['p1','p2']`，`after=['p1','src_b']`；答案值保持 `0`
  - 落盘 `donor_kind=same_value_diff_source`，不是 `rename`，也不是 `same_identity_fallback`
  - `{p1:p2,p2:p1}` 同时替换得 `p2 = 4. p1 = 0. What is q = p2 * p1?`，不是顺序塌缩
- **残留：** 这是「同一代数结构、保留旧叶 + 新叶」的夹具级不同源，不是第二条独立算式算出同一 \(q\)。不得写成 50 条 C2 同批次完成
- **影响：** r15 F15-01「兄弟目录名 `prep` 才能配对」与 r18 F18-03 顺序 rename 在本冻结指定路径上不成立

### D19-04 — \(H\) 全有限；全 NaN 行跳过；不可表达 `start=0` 跳过

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **50–68**；`events.py` **251–257**；`cli.py` **839–841、854–873**
- **对应要求：** 可表达步前入 \(H\)；点名「Skip all-NaN H rows」
- **证据：** X8e、X8c、X8f、X10、X14e。科学 collect `H` 6×32，NaN 行 0。手工 `Event(start=0)` → `h_position=no_event`，`H.shape=(0,32)`。source 行全 NaN 后改选 value 臂 `(0,2)`；全 NaN 矩阵返回 None。scientific `--backend offline` 拒绝把前缀 id 当 \(H\)
- **影响：** 指定路径不是 `donor_missing` 的 NaN 矩阵；NaN donor 不会被当成可表达配对

### D19-05 — INLP 是 \(h@P\)；C-rand `add_delta`；rescue `replace`；范数锁到主干预

- **状态：** closed（点名接线） / residual（弱层 \(H\) 未另采；helper `ie_z` 仍是向量差；结局通道不是教师强制 \(q\)）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `collect.py` **189–208**；`cli.py` **915–991**；`interventions.py` **31–49、52–67、88–89**
- **对应要求：** CAUSAL-01；INLP-01 下限；IE-01 接线；论文 §2.4
- **证据：** X11、X12、X14c、X14d、X23、X24。hook 间谍 `out = in @ P`（最大差 0）。五次 decode 键集合恰好 `{(pi_z_swap,1),(add_delta,1),(add_delta,0),(inlp,1),(replace,1)}`。C-rand / C-layer 范数与独立 `c_rand_delta` / `c_layer_delta` 对拍。rescue 是 `replace`，不是再 swap。落盘 `ie_z=0.0` ≠ helper \(-3.07\times 10^{-4}\)；`ie_z_g=target_follow`。本机 donor_ans=82、主/基线/对照皆为 9
- **残留：** C-layer 的 \(\Delta\) 仍用 **readout 层** 的 base/donor（collect 层 1），只是施加在弱层 0。`ie_z()` 库函数仍是均值差，仅 CLI tiny 路径改 \(g(Y)\)。intervene 的 generated 是无约束 4 token
- **影响：** 指定路径接线成立。tiny 上 0 且无 follow 按口令为诚实，不得写成论文来源跟随

### D19-06 — 仅生成区事件；几何 `timing` 保持 `offline_hidden`

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **147–189**；`cli.py` **929、1019**；`collect.py` **227**
- **对应要求：** POS-01 下限；点名 `parse_region=generated`
- **证据：** X8e、X14c、X22、X25、X26。6/6 轨迹事件节点皆 `q`，`start` 45 或 58，问句 36 或 49 字符。生成区 p1/p2 = 0。问句单独解析会出 p1/p2/`src_b`，说明排除靠「不解析问句」。jsonl 顶栏 `timing=offline_hidden`。`relative.hook_timing=pre_step` 仅表示 hook 打在事件步前前缀的 **re-encode** 上
- **影响：** 不得把 tiny 路径写成「已做 live 步前 hook」。指定路径不再把 prompt 前提写进 \(H\) 行

### D19-07 — Prefill：真实 32-d tiny hidden 接受；标量/bool/`[0]` 拒绝

- **状态：** closed（接口） / residual（`extra=32` 与不落盘向量）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `repair.py` **14–23、159–173**；`cli.py` **1054–1056**
- **对应要求：** REPAIR-01；点名「Prefill rejects scalar/bool/[0]」
- **证据：** X19。`isinstance(..., bool)` 先拒；`0`/`1.0` 走 `ndim==0`；`[0]`/`[]` 走 `size<2`。`run_repair` 对上述值写 `prefill_unavailable`。scientific CLI k=1..5 全部 `ok` / `refilled_prefix=True`
- **影响：** 标量/`[0]` 不再能把修复标成已 Prefill

### D19-08 — 教师强制诚实为 `constrained_target`；不得写 MODEL-01 / §4.1

- **状态：** closed（诚实标签） / non-defect（tiny 边界） / residual（模板未接入）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **72–98、157–158、181–191**；`adapters.py` **32–42**
- **证据：** X15、X25、X27。`append_target_assignment` 写 `\nq = ` 再从 logits 采两位数字，注释写明 Not gold values。6 条 `parse_status=constrained_target`，`correct=false`。金标 0，写出 82/53。`apply_model_template` 不被 CLI/`generate_task_trace` 调用
- **影响：** 把这条轨迹写成自然 CoT、官方模板对齐或 MODEL-01 **是缺陷**；当前代码与元数据没有那样写。本轮不要求发明自然 CoT

### D19-09 — `IsolatedExecutor` ≠ `ChildProcessExecutor`

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `executor.py` **27–33、59–63、97–102**
- **对应要求：** GOAL §5.15；EXEC-01；点名猎项
- **证据：** X18。`issubclass(ChildProcessExecutor, IsolatedExecutor) is False`；`isolated_sandbox` 分别为 `False` / `True`；默认 `get_executor()` 是 `UnavailableExecutor`。普通子进程不冒称隔离沙箱
- **影响：** 本机没有把 ChildProcess 标成 Isolated。Linux cgroup 仍 `pending_server`

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` 与 STACK 表一致 | 禁止下载；本轮不要求自然 CoT |
| U-02 | `replace` 用参数名 `delta` 传入救援向量 | 调用与实现一致 |
| U-03 | Prefill hidden 用最后一层而非 readout | 口令是「有 hidden」；X19 已满足 |
| U-04 | re-encode 与生成 ids 在乱码段的 8 处不一致 | 作者把 re-encode 当作修复；支持「非 live KV」 |
| U-05 | collect `_hidden_at_layer` 仍 `token_ids[:cap]`，`cap=max_position_embeddings`（tiny=128，缺省回退 64） | 点名猎项是 generate 48 与 intervene 64。本夹具全文 ≤64 token，未触发。不是静默 48/64 前缀 cap |
| U-06 | C-layer 把读出层 \(\Delta\) 加到弱层 residual | 猎项只要求 `c_layer_delta`+弱层 `add_delta`，已对拍 |
| U-07 | `extra_prefill_tokens` 恒 32 且不落盘 hidden；`execute_repair_tiny` 仍 `ids[:32]` | 旗标与拒绝规则已核；不是 generate/intervene 猎项 |
| U-08 | alt-source 仍是同结构换叶，不是第二条独立算式 | 猎项只要 keep-*a* add-*b* 且优先 source donor；50 条真实 C2 仍 `pending_server` |
| U-09 | rescue 向量范数等于 \(\\|H_{\mathrm{base}}-H_{\mathrm{source}}\\|\) 而非主干预范数 | 猎项只要求 `mode=replace` |
| U-10 | source 问句 `p2 = 0 src_b = 0` 少一个句点 | 完整 `* src_b` 已在问句中；未丢掉表达式 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是 MODEL-01** |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 五模式独立 decode 与指定路径接线 | 无真实来源-数值 donor；本机 \(g(Y)\) 无跟随 |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta` 在一维标准正交基下正确 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、只改层 2 last-token；`finally` 含异常路径清理 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"` |
| N-04 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `sampling` |
| N-05 | 关闭 | 几何 `timing` 保持 **`offline_hidden`** |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数 |
| N-07 | 关闭 | 跨界 token 不进入 `token_index` |
| N-08 | 关闭 | `extract_answer` 去掉闭合 think；未闭合返回 None |
| N-09 | 关闭 | `resid_post_hook(..., once=True)` 在 decode 中只生效一次 |
| N-10 | 关闭（功能） | `clone_cache` 隔离存储；步进路径未接入 |
| N-11 | 过程 | 开审与交卷均为 HASH_MATCH，可签在声称快照 `b6db632f…` 上 |
| N-12 | 非缺陷 | `--backend offline` 的 \(H\) 是前缀 id；scientific 拒绝 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 标注 `random_init`。**不是 MODEL-01** |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭 | 无 `--dev-layer-scores` 时 `clayer_status=dev_scores_missing` |
| N-16 | 关闭 | scientific `q` 步前入 \(H\)；不可表达步前不入 |
| N-17 | 关闭 | 主 hook 变换是 \(\Pi_Z\)；前缀是 `text[:event.start]`；主层 readout **1** |
| N-18 | 关闭 | `0` / `True` / `[0]` 诚实失败 Prefill |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| N-20 | 关闭（本轮猎项） | 无 generate 48 截断；无 intervene 64 截断（超长 raise）；重叠 rename 同时替换；keep-*a* add-*b*；无 `prep` 配对；有限 \(H\)；跳过 NaN；INLP=\(h@P\)；C-rand/rescue/C-layer；生成区事件；Prefill 拒绝；`constrained_target`；执行器不等价 |
| N-21 | 非缺陷（本轮口径） | 不要求自然 CoT；约束 `\nq = ` 两位数字不是 §4.1 |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` 无生产调用方 |
| S-03 | stub | `relative` 无 INLP 四项结局，只有 `inlp_followed_donor` |
| S-04 | stub | Linux cgroup 执行器未到 |

## 10. 通道结论

**D 通道通过（PASS）。冻结：HASH_MATCH `b6db632fe07e2763eea003e9c09f0a5d18272fda76c7bba7d1c8a40596569eeb`（61 文件）。指定猎项在独立复跑上关闭。tiny 不是 MODEL-01；自然 CoT 不是本通道通过条件。不宣布 Goal 完成。本通道单独不得启动连续通过计数。**

开审与交卷复算冻结均为 `b6db632f…96569eeb`。在 `.planning/audits/round-19/_d_scratch/` 对 `tests/fixtures/t1_tiny.json` 跑 scientific `prepare --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15` → `collect --backend tiny --weight-seed 0` → `intervene --backend tiny` → `intervene --dev-layer-scores 0.05 0.9 0.8` → `repair --eval-mode scientific --mask task_oracle`。目录名为 `stage_a`/`stage_b`，**没有**兄弟 `prep`。核验：

1. **无 generate 48 截断：** source 问句 49 字符，完整 `What is q = p1 * src_b?`。`generate.py` 超 96 则 raise。
2. **无 intervene 64 截断：** `_tiny_prefix_ids` 65 token 不切片；97 token raise。无 `ids[:64]`。
3. **重叠 rename 同时替换：** `{p1:p2,p2:p1}` → `p2 = 4. p1 = 0. What is q = p2 * p1?`。
4. **keep-*a* add-*b*：** 保留 `p2`，追加 `src_b`，父母 `{p1,src_b}`；不是 rename（rename 丢掉 `p2`）。
5. **无 prep 配对：** collect 把 `edits.jsonl` 拷进 `stage_b`；intervene 只读该文件；donor=`same_value_diff_source` 行 `(0,3)`。
6. **有限 \(H\) / NaN / start=0：** `(6,32)` 全有限；source 行全 NaN 则改选 value 臂；全 NaN 不配对；`start=0` → `no_event`。
7. **INLP / 对照：** `mode=inlp` 为 \(h@P\)；C-rand/C-layer `add_delta` 范数与独立重算落盘一致；rescue `replace`。
8. **生成区事件：** 6/6 `parse_region=generated`，仅 `q`，`start` 不落入 prompt。
9. **Prefill：** `0` / `True` / `[0]` 拒绝；scientific repair k=1..5 有真实 32 维 hidden。
10. **教师强制：** 6/6 `constrained_target`；不是 §4.1，也不是 MODEL-01。
11. **执行器：** `ChildProcessExecutor` 不是 `IsolatedExecutor`。

这些仍不够支持把指定路径写成论文同批次交换/消融/救援实验结果：五种模式都抽出 `9`，相对对照为 0，donor 轨迹答案是约束 `"82"` 不是金标 0。诚实的 tiny 接线证明 ≠ MODEL-01 / CAUSAL-01/02 完成。真实 HF / 官方 dump / CUDA / 50 条 C2 保持 `pending_server`。
