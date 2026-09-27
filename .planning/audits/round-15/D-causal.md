# D-causal 独立审查报告（round-15）

通道 D：模型与因果（token/prefix、thinking 模板、sampling、hook/KV、donor 来源、swap/消融/救援、两类对照、nontarget/invalid）。指定独立复跑 scientific `prepare`→`collect --backend tiny`→`intervene --backend tiny`（另跑 `--dev-layer-scores 0.05 0.9 0.8`）→`repair --eval-mode scientific`，夹具 `tests/fixtures/t1_tiny.json`，`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15`。猎项：`parse_region=generated` 且事件 `start ≥` 问句/`prompt_len`；生成区无 prompt `p1`/`p2`；有限 \(H\)、无 NaN `pre_step` 行、不可表达 `start=0` 跳过；**A13-01 donor 优先 `same_value_diff_source` / `trace-source`（有 source donor 时不是 rename-only，也不是 value-edit-only）**；INLP 为 \(h@P\) 不是 \(\Pi_Z\)；C-rand `add_delta`；rescue `replace`；`ie_z` 来自 target-follow \(g(Y)\)；Prefill 接受真实 32-d hidden，拒绝 `0`/`True`/`[0]`；教师强制 `q` 诚实标 `constrained_target`。tiny **不是** MODEL-01；约束 `\nq = <digit>` **不是** §4.1 自然 CoT。

独立性声明：未阅读 round-15 其他通道报告；只把 `.planning/audits/round-15/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账。对照读了本通道 round-13 报告仅作版式与猎单对照，不作本轮证据。猎项以开审 MATCH 窗口的独立复跑为准；交卷冻结以交卷复算为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试绿当作论文正确性；不把作者 `local close` 或声称 159 passed 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。

对照原文：论文 §2.4（交换公式、C-rand/C-layer 同批次）、§4.1（自然 CoT，本机不得冒称）、§4.2（三位置）、§6/§8（来源—数值 / 交换 / Knock-out / Rescue）；GOAL MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01；`docs/EXPERIMENT_PROTOCOL.md` §4。tiny 路径只验收接口与接线，不验收 MODEL-01。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结 **HASH_MATCH** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（61 文件，0 CRLF）。指定 scientific 路径点名项在该窗口立即复跑后全部成立。交卷再算同一脚本为 **HASH_MISMATCH**（61 文件 / `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`）。本通道未改冻结集；窗口内他方先后改写 `models/generate.py`、`models/tiny.py`、`edits.py`、`cli.py` 与 `tests/test_round07_regressions.py`。中间一次复算曾为 `5413a4bc…`（仅 generate/tiny）。tiny 不是 MODEL-01，不得写 §4.1。

**总裁决：FAIL。开审 HASH_MATCH。交卷 HASH_MISMATCH。指定猎项在开审 MATCH 窗口关闭。不得把本报告签在声称快照 `401e509b…` 上。不宣布 Goal 完成。不得启动连续通过计数。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21（Asia/Shanghai）；开审约 02:45，交卷约 03:15 |
| 声称冻结 hash | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（`.planning/audits/round-15/VERSION.md`；61 文件；POSIX relpath + NUL + bytes） |
| 开审复算 | **HASH_MATCH。** 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → **61** 文件 → `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` |
| 交卷复算 | **HASH_MISMATCH。** 同脚本 → 61 文件 / `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`。开审 CRLF=0。本通道未改冻结集。窗口内他方改写：`generate.py` 7712/`07493570…`→7750/`6e604039…`；`tiny.py` 3508/`21725a18…`→3510/`c75d0f53…`；`edits.py` 13521/`250055ab…`→13773/`1e5b97d6…`；`cli.py` 61010/`c1a274e2…`→61662/`b37fef2c…`；`tests/test_round07_regressions.py`。中间快照 `5413a4bc…` 只含前两文件 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；`src/`/`tests/`/`pyproject.toml` 为未跟踪。HEAD 不是冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载；无 CUDA |
| 作者 pytest 声称 | 159 passed。本机全量 **159 passed / 21.68s / exit 0**（MATCH 窗口）。因果相关 7 个文件 **67 passed / 18.70s**。绿只锁回归，不是论文正确性；交卷树未重跑 pytest |
| 明确未读 | `.planning/audits/round-15/` 下除 `VERSION.md` 与本文件外的其他通道报告 |

因果生产文件开审 SHA-256 前 16：`cli.py` `c1a274e233988aad`（61010 B / 1252 行）、`edits.py` `250055ab8257ea2e`（13521 B / 362）、`collect.py` `83658cd8ba879f20`（261）、`generate.py` `07493570c6410e6b`（201）、`tiny.py` `21725a183452bd06`（120）、`features.py` `0a9f0b8beb0185ae`（39）、`adapters.py` `c1992624026a1bf0`（42）、`tokenize.py` `b0cc8974af1010fa`（31）、`interventions.py` `0ffdbb8805be7649`（115）、`repair.py` `f76ff9998b9a6b17`（232）、`events.py` `290a4fd676ac0814`（274）、`executor.py` `481d6ed597c93e78`（109）、`rng.py` `2098c2c72a852eaa`（53）。交卷：`generate.py` `6e6040394ac641c7`（7750 B）、`tiny.py` `c75d0f5325766612`（3510 B）、`edits.py` `1e5b97d63a62ab78`（13773 B）、`cli.py` `b37fef2ce7998776`（61662 B）。`collect.py` / `interventions.py` / `repair.py` 开审=交卷。交卷 `generate.py` 删掉开审静默 `[:48]`，`>96` 则 raise；`tiny.py` `max_position_embeddings` 64→128；交卷 `apply_alt_source_same_value` 改为保留叶 `a`、新增固定名 `src_b`、去掉 `(alt source)` 标注。这些新字节**未经**本通道重跑指定路径。开审复跑用的是 `p2_src` + `(alt source)` + 丢掉旧叶。

复跑目录（本通道自建，不是他通道报告）：`.planning/audits/round-15/_d_sci_run/{s-prep,s-col,s-int,s-int-dev,s-rep}`。

## 2. 范围与逐文件覆盖

指派阅读并逐行核对（行号为开审阅读 / 复跑所用 `generate.py` `07493570…`、`tiny.py` `21725a18…`；交卷这两文件已变，见 D15-00。`cli.py` / `edits.py` 交卷未变）：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / 卡片 `think_ids` / `load_frozen(..., local_files_only=True)`。`revision=="latest"` 拒绝 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids`（**非互逆**）/ `readout_layer_index`（60%–75% 带）/ `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–261 | `collect_hidden_trace` 不可表达步前 **continue**；`intervene_hidden_decode` 四 mode：`pi_z_swap` / `inlp`（`vec @ proj`）/ `add_delta` / `replace` |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–201（开审） | `sample_next`；`decode_loop`（独立 `torch.Generator`）；`append_target_assignment`；开审 `generate_task_trace` 静默 `prompt_ids[:48]` 后只解析生成区；`apply_model_template`（定义存在，CLI / `generate_task_trace` **无调用**）。交卷字节已改，见 D15-00 |
| `src/reasoning_diff/models/tiny.py` | 1–120（开审） | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step`。开审 `max_position_embeddings=64`；交卷改为 128，见 D15-00 |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / `inlp_remove` / `rescue_controls` / `select_weak_layer` / 库函数 `ie_z`（隐向量均值）/ `intervention_report` |
| `src/reasoning_diff/edits.py` | 109–211、214–319 | `apply_value_edit`；`apply_rename_edit`；`apply_alt_source_same_value`（新前提、`(alt source)`、父节点必须变、目标值必须不变）；`make_source_value_pair` |
| `src/reasoning_diff/repair.py` | 1–232 | `_hidden_is_prefill` 拒绝标量/bool/`[0]`；`execute_repair_tiny`；`run_repair` |
| `src/reasoning_diff/cli.py` | 257–438、440–547、676–689、806–865、868–1011、1014–1054 | prepare/collect/pair/donor/intervene/repair |
| `src/reasoning_diff/executor.py` | 1–109 | `ChildProcessExecutor.isolated_sandbox=False`；默认 Unavailable |
| `src/reasoning_diff/rng.py` | 41–53 | StreamBank `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/events.py` | 27–89、251–274 | `parse_events`；`boundary_index`；`extract_answer` 去 think |
| `src/reasoning_diff/schema.py` | 39 | `POSITION_KINDS` |
| `tests/test_tiny_hooks.py` | 全文件 | 前向 + hook 清理（绿只作冒烟，不作通过证据） |
| `tests/test_tiny_cache.py` | 全文件 | cache 隔离冒烟 |
| `tests/test_generate_loop.py` | 全文件 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | scientific / Prefill / readout / pair 字段 | 字段锁，不替代本轮复跑 |
| `tests/test_round05_regressions.py` | scientific 事件 / 几何 timing | 同上 |
| `tests/test_round06_regressions.py` | `donor_kind`/`inlp`/`add_delta`/`replace`/`ie_z_g` | **不**比 \(h@P\) 数值 |
| `tests/test_round07_regressions.py` | 标量/`[0]` Prefill；pair 图 | 本通道另用 `run_repair` / 指定路径直接核验 |

支持性阅读：`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` 上列要求。未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次、自然 CoT。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`、`measure.py`、`splits.py`（他通道）。`cli.py` 校准/fit 段属其他通道。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | VERSION 脚本逐字复算 | **开审 HASH_MATCH** 61 / `401e509b…de88f716`（0 CRLF）。**交卷 HASH_MISMATCH** 61 / `5413a4bc…e661fc`。见 D15-00 |
| X2 | 因果相关 pytest 7 文件 | **67 passed / 18.70s**。绿只锁冒烟与字段名 |
| X2b | 全量 pytest | **159 passed / 21.68s / exit 0**，与作者数字一致。仍不是论文正确性，不把 159 写成 Goal 完成 |
| X3 | `apply_swap` 标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.171\)、\(\Delta V_{\max}=0.364\)，且 **仅 last token**（earlyK=0） |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3** 次；`once=True` **1** 次 |
| X7 | hook `finally` 清理 | 正常与 `RuntimeError` 后 `_forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)` |
| X8c | 空事件 / `start=0` | `h_position=no_event`，\(H\) `(0,32)`，不塌成末 token |
| X8e | **指定** scientific `prepare`→`collect --backend tiny --weight-seed 0` | 6 条轨迹：`trace-base` / `trace-t0p` / `trace-edit` / `trace-source` / `p1:0` / `p2:2`。每条 **1** 个生成区 `q`（base/edit `start=45`；source `57`；`parse_region=generated`，`parse_status=constrained_target`）。问句前提不进入事件。`H` `(6,32)` **6/6 行有限**（0 NaN）；`H_pre_step/value/post` 同样 0 NaN 行。`event_rows.jsonl` 6 行皆 `{node_id:q, trace_id:…}`。`hidden_layer=1`；`weight_source=random_init`；`weight_seed=0`。\(\\|H_0-H_1\\|\approx 0.00778\)（base vs t0p），\(\\|H_0-H_2\\|\approx 0.00430\)（base vs edit），\(\\|H_0-H_3\\|\approx 0.01174\)（base vs source）。`H_2\equiv H_5`（默认 edit 与 `_allowed_edits` 的 `p2:2` 撞车） |
| X8f | scientific collect 拒绝 | `--backend offline` → `ValueError: scientific collect refuses offline_prefix_ids as H`（exit 1） |
| X8g | re-encode vs 生成 ids | base 轨迹与 `encode_text(text)` 有 **8** 处不同（恰 `max_new=8` 乱码段，下标 36–43）。collect 的 \(H\) 是对表面文本的二次前向 |
| X8h | 步前 vs 前缀前向 | `H[0]` 与 `encode_text(text[:45])` 末 token **逐位相等**（\(\Delta=0\)）；与步尾 \(\\|\cdot\\|\approx 0.147\) |
| X9 | `leaks_target` | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None` |
| X10 | `boundary_index` | `start=0,"before"` → **None**。`limit=2` 的 `"before"` / `"end"` / `"value"` 皆为 1 |
| X11 | INLP / rescue 算法 | `rescue([1,0],[0,1])=[1,1]`。随机向量上 \(h@P\) 与 `apply_swap` 最大差 **1.29**（不是同一变换）。库函数 `ie_z(H_3,H_0)\approx -2.63\times 10^{-4}`；**CLI tiny 路径不写该值** |
| X12 | C-rand / C-layer 范数与弱层 | 缺范数仍 `ValueError`（`C-rand requires the actual main-intervention norm`）。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0`。三项范数经 `scale_to_norm` 锁成同一 `main_norm` \(1.2131109103817872\times 10^{-3}\)（与落盘逐位一致） |
| X13 | StreamBank vs hook 基 | `direction` 第一抽 113750710（丢弃）；第二抽 **basis_seed=1153799966**。`sample` 第一抽 **1191642646**。`perturb` 17172908 |
| X14c | **指定** collect→intervene（**无** `--dev-layer-scores`） | `_pair_source_value` 返回 **`(0, 3, same_value_diff_source)`** = `trace-base` / `trace-source` 的同身份 `q`（**不是** `trace-t0p`，**不是** `trace-edit`）。`status=prospective_decode`，几何 **`timing=offline_hidden`**。`relative.hook_once=resid_post`，`transform=pi_z_swap`，`hook_timing=pre_step`（hook 内部标签，几何字段未改写）。monkeypatch 记录 **4** 次 `intervene_hidden_decode`：层皆 **1**，模式 **`pi_z_swap` / `add_delta` / `inlp` / `replace`**，`hook_fired=true`。INLP **无 donor**、有 `projector` `(32,32)` rank 30。`clayer_status=dev_scores_missing`（无弱层 decode）。`ie_z=0.0`，`ie_z_g=target_follow`。对照四项因 clayer 空而 **null** |
| X14d | 另跑 `--dev-layer-scores 0.05 0.9 0.8` | **5** 次独立 decode，层 **1 / 1 / 0 / 1 / 1**，模式 **`pi_z_swap` / `add_delta`(C-rand) / `add_delta`(C-layer) / `inlp` / `replace`**。`clayer_status=dev_weak_layer_decode`，`weak_layer=0`。三项范数与独立重算及落盘一致。相对四项 `vs_crand=vs_clayer=0.0`。`donor_kind` 仍为 `same_value_diff_source`，`donor_rows=[0,3]` |
| X14e | A13-01 偏好对照 | 抹掉 pair 元数据里的 `same_value_diff_source` tid 后，同一 \(H\) 回退 **`(0, 2, same_source_diff_value)`**。生产路径 **没有** 走这条回退。无 rename 轨迹；`apply_alt_source_same_value` ≠ `apply_rename_edit` |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 后数字 → 7；未闭合 → None；`\\boxed{7}` → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 与 `generate_task_trace` 无调用**（`apply_model_template` 仅在 `generate.py` 195 行定义）。本轮不要求自然 CoT |
| X16 | `clone_cache` / DynamicCache | clone ≠ 原对象；`data_ptr` 不同；`add_` 后隔离；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.686\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False` |
| X19 | Prefill | `execute_repair_tiny` 返回 **32** 维有限非零（\(\\|h\\|\approx 5.65\)）。`run_repair` 接受该向量 → `refilled_prefix=True`/`ok`。`0` / `True` / `1.0` / `[0]` / `[0.0]` / `[]` / `None` / `False` / `"x"` / 仅 `prefix_token_ids` → `prefill_unavailable`。scientific CLI repair：k=1..5 皆 `refilled_prefix=True`、`status=ok`、`gated=False`、`extra_prefill_tokens=32`；jsonl **无** `prefill_hidden` 字段 |
| X20 | `weight_seed` | 同 seed 同 ids → \(\\|\Delta H\\|_{\max}=0\)；异 seed → 0.099；同 seed 异 ids → 0.072。CLI collect 写入 spec `weight_seed=0` |
| X21 | 来源-数值 / A13-01 图 | `edits.jsonl` 含 `kind=source_value_pair`：targets=`["q"]`，nontargets=`["p1"]`，`trace_ids={base:trace-base, same_source_diff_value:trace-edit, same_value_diff_source:trace-source}`。source 臂 `kind=same_value_diff_source`，问句 `p1 = 4. p2_src = 0 (alt source). What is q = p1 * p2_src?`，parents `q←{p1,p2_src}`（base 为 `{p1,p2}`），答案值仍为 **0**。value 臂改 `p2:0→2`，答案 **8**。rename 臂（库函数对照，生产未生成轨迹）问句为 `p2_src = 0.`，**无** `(alt source)` 标注。`make_source_value_pair` 调 `apply_alt_source_same_value`，不调 `apply_rename_edit`。`_try_source_value_pair` 对 T3 / paragraph 返回 None（代码路径；本轮夹具未触发） |
| X22 | 事件跨度 / hook 前缀 | 生成区 `q` 跨度 45–51（source 57–63），前缀 45（source 57）字符；`ids[:64]` **未截断**（`prefix_truncated=false`）。6/6 `start ≥ len(prompt_text)` 且 `start ≥ prompt_len`（本机 1 字符 = 1 token） |
| X23 | \(g(Y)\) / `ie_z` | donor/base 轨迹 `answer` 皆为约束赋值 **「82」**（seed=0 同权重抽样，不是金答案 0）。intervene 主/对照/INLP/rescue/C-layer 抽取答案皆 **「9」**，`followed_donor=false`。`ie_z=1{9==82}-1{9==82}=0`，`ie_z_g=target_follow`。库函数隐向量均值 **未被** CLI tiny 路径写入 |
| X24 | INLP hook 不是 swap | 间谍 `out == in @ P`（atol 1e-5），`out ≠ in`。CLI `mode="inlp"`，无 donor。2 点拟合 `inlp_rank=30` |
| X25 | 教师强制 / 采样 | `target_assignment='\nq = 82'`（t0p 为 `\nq = 53`）；`parse_status=constrained_target`；`correct=false`（金标 0）。6 条 `sampling={temperature:1.0,top_k:0,top_p:1.0}`。`decode_loop` 用独立 `Generator`，不用 `HF generate`。intervene decode **不再**教师强制 |
| X26 | 问句单独解析 | 对 6 条 `prompt_text` 跑 `parse_events` 会打出 p1/p2（source 问句为 p1/`p2_src`）。generate **不解析问句**，故这些不是生成事件 |
| X27 | 卡片 revision | `qwen3-8b` `b968826d9c…` think `(151667,151668)`；`r1-distill-qwen-7b` `916b56a4…` think `(151648,151649)`。本机未加载。缺名 `card` 抛 `KeyError` |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验卡片 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server`。本轮不要求自然 CoT |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存；CLI 未调用。属 `pending_server`。tiny **不是** MODEL-01 |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机是接口证明 |
| 把 159 passed 写成 Goal / MODEL-01 验收 | 绿测试不是论文正确性 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

`ISSUES.md` 只当作者主张。

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| A13-01 | `apply_alt_source_same_value`：新前提 `(alt source)`、目标值不变、必需父节点改变；intervene 优先 `trace-source` | **指定路径独立关闭。** X14c/d/e、X21。不是 rename-only，有 source donor 时不是 value-edit-only |
| A13-02 | 未知行为 → \(M=\emptyset\)，`rho_M_*=null` | **不裁定。** A/C |
| A13-03 | 任意 `sham:` 行 → `noise_set=None` | **不裁定。** A/B |
| A12-03 | `_find_tasks_jsonl` 只读传入目录 | **不裁定。** A/E/F |
| A10-04 Plus family persist-lock | `splits.py` / 磁盘并集 | **不裁定。** 非本通道猎项 |
| C6-M-01 / B9-01 | 无本题 `tasks.jsonl` → raise；sham 不广播 | **不裁定。** C/B |
| 先前 D 生成区事件、有限 \(H\)、INLP/C-rand/rescue/`ie_z`、几何 timing、Prefill | 须在 `401e509b…` 上重核 | **独立关闭（指定路径，本轮 MATCH 树）。** X8e、X14c/d、X19、X22–X25。交卷树未重核 |
| pending_server | 真实权重 / 50 条 C2 / 官方 CoT | **同意未关。** 约束 `q` 不是 §4.1；tiny 不是 MODEL-01 |
| Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |

## 6. 发现

### D15-00 — 声称冻结 hash 对交卷磁盘不成立

- **状态：** confirmed defect（过程 / QA-01）
- **严重度：** high
- **文件 / 符号 / 行号：** `.planning/audits/round-15/VERSION.md` 声称 61 文件 / `401e509b…de88f716`；交卷磁盘 61 文件 rel+NUL+bytes = `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`
- **触发条件：** 按 VERSION 脚本在开审、猎项复跑后、成文后、交卷前各复算
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。开审 MATCH。窗口内连续漂移：先 `5413a4bc…`（`generate.py`/`tiny.py`），再 `3d0a0764…`（另加 `edits.py` 13521/`250055ab…`→13773/`1e5b97d6…`，`cli.py` 61010/`c1a274e2…`→61662/`b37fef2c…`）。交卷 `apply_alt_source_same_value` 不再是开审的 `p2_src`+`(alt source)`+丢旧叶，而是保留 `a`、新增 `src_b`。本通道未改这些文件。`collect.py` `83658cd8…`、`interventions.py` `0ffdbb88…`、`repair.py` `f76ff999…` 开审=交卷
- **影响：** 不能把本报告说成「已在声称快照 `401e509b…` 上签字」。猎项锚定开审 MATCH 之后立即复跑的磁盘行为。交卷 A13-01 图构造**不是**本轮指定路径证据
- **建议：** 停写、重冻、审查者只对一个 hash 交卷。并行通道不得在审查窗口改冻结集合

### D15-01 — 只解析生成区；事件 `start ≥` 问句；问句 p1/p2 不是生成事件

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **148–191**（`parse_events(generated)` 再 `+= len(prompt)`；`parse_region="generated"`；赋值落在 `gen_text` 之后则 `constrained_target`）；`cli.py` **292–302**
- **对应要求：** POS-01 下限；本轮猎项「generated-region events」
- **证据：** X8e、X22、X25、X26。6/6 轨迹事件节点皆 `q`，`start` 45 或 57，问句 36 或 48 字符。生成区 p1/p2 = 0。表面无金标注串 `p1 = 4 | p2 = 0 | q = 0`。问句单独解析会出 p1/p2（source 为 p1/`p2_src`），说明排除靠「不解析问句」，不是问句里没有赋值
- **影响：** 指定路径不再把 prompt 前提写进 \(H\) 行。这不是自然 CoT，也不声称 MODEL-01

### D15-02 — \(H\) 全有限；不可表达 `start=0` 跳过；无 NaN pre_step 行

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **50–68**；`events.py` **251–257**
- **对应要求：** 可表达步前入 \(H\)；不可表达不塌成末 token
- **证据：** X8e、X8c、X8f、X10。科学 collect `H` 6×32，NaN 行 0；`H_pre_step/value/post` NaN 行 0。手工 `Event(start=0)` → `h_position=no_event`，`H.shape=(0,32)`，**不**塌成末 token。`boundary_index(...,0,"before")` 为 None。scientific `--backend offline` 拒绝把前缀 id 当 \(H\)
- **影响：** 指定路径不是 `donor_missing` 的 NaN 矩阵

### D15-03 — A13-01：donor 优先 `same_value_diff_source` / `trace-source`；不是 rename-only；有 source donor 时不是 value-edit-only

- **状态：** closed（点名配对与图构造） / residual（夹具级换源，不是 50 条独立计算源）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `edits.py` **219–289**（`apply_alt_source_same_value`：新 id `{premise}_src`、文本 `(alt source)`、丢掉旧叶、父节点集合必须变、目标值必须不变）；**292–301**（`make_source_value_pair` 调 alt-source，不调 rename）；`cli.py` **298–302、384–397**（落盘 `trace-source`）；**816–838**（键序 `same_value_diff_source` 先于 `same_source_diff_value`；`allclose` 才继续下一键）
- **对应要求：** CAUSAL-02「按 pair 取 donor」；作者 A13-01
- **证据：** X8e、X14c、X14e、X21。
  - pair 元数据 `base→trace-base`、`same_source_diff_value→trace-edit`、`same_value_diff_source→trace-source`
  - 选中行 `(0,3)`，\(\\|H_0-H_3\\|\approx 0.01174\)，`allclose=False`，两行有限
  - **未选** 更近的 base–edit \(0.00430\)，也 **未选** base–t0p \(0.00778\)
  - 人为去掉 source tid 后同一矩阵才回退 `(0,2,same_source_diff_value)`，证明生产偏好不是「谁近选谁」
  - source 问句含 `(alt source)`；rename 对照问句仅为 `p2_src = 0.`，无该标注；value 对照改值且答案 0→8
  - `required_sources_before=['p1','p2']`，`after=['p1','p2_src']`；答案值保持 `0`
  - 指定 prepare **不**生成 rename 轨迹；donor_kind 落盘为 `same_value_diff_source`，不是 `rename`，也不是 `same_identity_fallback`
- **残留：** 这是「同一代数结构、换叶名 + 标注」的夹具级不同源，不是第二条独立算式算出同一 \(q\)。不得写成 50 条 C2 同批次完成
- **影响：** r13 残留「只吃 `same_source_diff_value` / donor=`(0,2)`」在本冻结指定路径上不成立。有 source donor 时不再把 value-edit 或 seed1 轨迹当 donor

### D15-04 — INLP 是 \(h@P\)；C-rand `add_delta`；rescue `replace`；`ie_z` 为 target-follow \(g(Y)\)；有分数则弱层 `add_delta`

- **状态：** closed（点名接线） / residual（弱层 \(H\) 未另采；helper `ie_z` 仍是向量差；结局通道不是教师强制 \(q\)）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `collect.py` **189–208**；`cli.py` **915–984、964–965**；`interventions.py` **31–49、52–67、88–89**
- **对应要求：** CAUSAL-01 接线；INLP-01 下限；IE-01 接线；论文 §2.4
- **证据：** X11、X12、X14c、X14d、X23、X24。hook 间谍 `out = in @ P`。无 flag：4 次 decode `(pi_z_swap,1)/(add_delta,1)/(inlp,1)/(replace,1)`。有 flag：5 次，键集合恰好 `{(pi_z_swap,1),(add_delta,1),(add_delta,0),(inlp,1),(replace,1)}`。C-rand / C-layer 范数与独立 `c_rand_delta` / `c_layer_delta` 对拍，锁到主干预 \(1.2131109103817872\times 10^{-3}\)。rescue 是 `replace`，不是再 swap。落盘 `ie_z=0.0` ≠ helper \(-2.63\times 10^{-4}\)；`ie_z_g=target_follow`。\(g=1\) 当 `extract_answer(generated)==donor_ans`。本机 donor_ans=82、主/基线皆为 9
- **残留：** C-layer 的 \(\Delta\) 仍用 **readout 层** 的 base/donor（collect 层 1），只是施加在弱层 0。`ie_z()` 库函数仍是均值差，仅 CLI tiny 路径改 \(g(Y)\)。intervene 的 generated 是无约束 4 token，不是被强制的 `\nq =`
- **影响：** 指定路径接线成立。tiny 上 0 且无 follow 按口令为诚实，不得写成论文来源跟随

### D15-05 — 几何 `timing` 保持 `offline_hidden`，未写成 live `pre_step`

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `cli.py` **912、1004**；`collect.py` **227**（hook 内部 `timing`）
- **证据：** X14c、X14d、X8g、X8h。jsonl 顶栏 `timing=offline_hidden`。`relative.hook_timing=pre_step` 仅表示 `event_aligned=True` 时 hook 打在事件步前前缀上，前缀是 `text[:45]` 的 **re-encode**，不是原生成 KV 续写。collect \(H\) 与前缀末 token 一致，与生成 ids 有 8 处不同
- **影响：** 不得把 tiny 路径写成「已做 live 步前 hook」。本机接口是离线隐状态几何 + 二次前向 hook

### D15-06 — Prefill：真实 32-d tiny hidden 接受；`0`/`True`/`[0]` 拒绝

- **状态：** closed（接口） / residual（`extra=32` 与不落盘向量）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `repair.py` **14–23、159–173**；`cli.py` **1047–1050**
- **对应要求：** REPAIR-01「有限 hidden 才能 `refilled_prefix`」
- **证据：** X19。`isinstance(..., bool)` 先拒；`0`/`1.0` 走 `ndim==0`；`[0]`/`[]` 走 `size<2`。`run_repair` 对上述值写 `prefill_unavailable`，即使 execute 谎称 `refilled_prefix=True`。真实 `execute_repair_tiny` 给出 32 维有限向量后 `status=ok`。scientific CLI k=1..5 全部 `refilled_prefix=True`、`extra_prefill_tokens=32`
- **影响：** 标量/`[0]` 不再能把修复标成已 Prefill

### D15-07 — 教师强制 `q` 诚实为 `constrained_target`；不得写 MODEL-01 / §4.1

- **状态：** closed（诚实标签） / non-defect（tiny 边界） / residual（模板未接入）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **72–98、157–158、181–191**；`adapters.py` **32–42**
- **证据：** X15、X25、X27。`append_target_assignment` 写 `\nq = ` 再从 logits 采两位数字，注释写明 Not gold values。6 条 `parse_status=constrained_target`，`correct=false`。金标 0，写出 82/53。`apply_model_template` 不被 CLI/`generate_task_trace` 调用。卡片 `think_ids` 只在未调用的 `load_frozen` 路径
- **影响：** 本机可解析接口成立。把这条轨迹写成自然 CoT、官方模板对齐或 MODEL-01 **是缺陷**；当前代码与元数据没有那样写。本轮不要求发明自然 CoT

### D15-08 — nontarget/invalid 字段已接线；本机取值不能当机制结果

- **状态：** closed（schema / 相对对照） / residual（通道与 identifiability）
- **严重度：** n/a / residual
- **文件 / 符号 / 行号：** `cli.py` **950–967、983**；`interventions.py` **98–115**
- **证据：** X14c、X14d、X23、X25。有分数时四项相对 `vs_crand`/`vs_clayer` 均为 0.0（主与两对照答案都是 `"9"`）。无分数时相对四项 null（C-layer 未 decode）。`invalid=0` 因为垃圾 decode 仍能抽出数字。`nontarget` 定义为「答案=轨迹 answer 且 ≠ donor」；本机 base/donor 轨迹 answer 皆为同一 `seed=0` 教师强制 `"82"`，该比特结构上不能为 1。金标任务值 0 从未进入 `_outcomes`
- **影响：** 不得把四项 0 写成「无目标跟随」的科学结论。`acknowledged_effect=relative_to_controls_only` 诚实。CAUSAL-02 实测结局保持 `pending_server`

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载；本轮不要求自然 CoT |
| U-02 | `replace` 用参数名 `delta` 传入救援向量 | 调用与实现一致 |
| U-03 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够；生产路径不调用 |
| U-04 | Prefill hidden 用最后一层而非 readout | 口令是「有 hidden」；X19 已满足 |
| U-05 | re-encode 与生成 ids 在乱码段的 8 处不一致 | 作者把 re-encode 当作修复；tiny 字级词表下是二次教师强制；支持「非 live KV」 |
| U-06 | `_load_source_value_pair` 依赖兄弟目录名 `prep`/`prepare`/`s-prep` | 指定路径 `s-prep`/`s-col` 找到 pair |
| U-07 | `_expressible_donor` 在 pair `allclose` 时回退 | 本机 base/source 互异，未触发；人为去掉 source tid 才回退 value |
| U-08 | C-layer 把读出层 \(\Delta\) 加到弱层 residual | 猎项只要求 `c_layer_delta`+弱层 `add_delta`，已对拍 |
| U-09 | `extra_prefill_tokens` 恒 32（`ids[:32]`）且不落盘 hidden | 旗标与拒绝规则已核；声称可审计表征时再升格 |
| U-10 | 全文三事件里 p1 不入 \(H\) | 步前不可表达；科学路径只采生成区 `q` |
| U-11 | alt-source 仍是「同结构换叶名」而非第二条独立算式 | 猎项只要不同于 rename-only / value-only 且优先 source donor；已满足。50 条真实 C2 仍 `pending_server` |
| U-12 | rescue 向量范数等于 \(\\|H_{\mathrm{base}}-H_{\mathrm{source}}\\|\)（0.01174）而非主干预范数 | 猎项只要求 `mode=replace`；未写成范数匹配缺陷 |

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
| N-11 | 过程 | 开审 hash MATCH；交卷前 MISMATCH（D15-00）。不得写成 HASH_MATCH |
| N-12 | 非缺陷 | `--backend offline` 的 \(H\) 是前缀 id；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 是随机初始化隐状态并标注 `random_init`。**不是 MODEL-01**；本轮不要求 MODEL-01 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 无 `--dev-layer-scores` 时 `clayer_status=dev_scores_missing` |
| N-16 | 关闭 | scientific `q` 步前入 \(H\)；不可表达步前不入；空事件 `no_event` |
| N-17 | 关闭 | 主 hook 变换是 \(\Pi_Z\)；前缀是 `text[:event.start]`（本机 45 token）；主层 readout **1** |
| N-18 | 关闭 | `execute_repair_tiny` 重新 Prefill；dummy/offline/`0`/`True`/`1.0`/`[0]`/`[]`/`prefix_token_ids` 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册不记缺陷 |
| N-20 | 关闭（本轮猎项） | 生成区事件；有限 \(H\)；donor=`same_value_diff_source`/`trace-source`；INLP=\(h@P\)；C-rand/rescue/C-layer 独立 decode；`ie_z` target-follow 且 0 诚实；几何 `offline_hidden`；Prefill 拒 `0`/`True`/`[0]`；`constrained_target` 诚实 |
| N-21 | 非缺陷（本轮口径） | 不要求自然 CoT；约束 `\nq = ` 两位数字不是 §4.1 |
| N-22 | 关闭（A13-01） | source 臂不是 `apply_rename_edit`；有 source donor 时不选 value-edit 行 |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `think_ids` / `load_frozen` / `assert_no_future_leak` 无生产调用方 |
| S-03 | stub | `inlp_remove` 有 decode；`relative` 无 INLP 四项结局，只有 `inlp_followed_donor` |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道不通过（FAIL）。冻结：HASH_MISMATCH。指定猎项在开审 MATCH 窗口的独立复跑上全部关闭。tiny 不是 MODEL-01；自然 CoT 不是本通道通过条件。不宣布 Goal 完成。不得启动连续通过计数。**

开审复算冻结为 `401e509b…de88f716`（61，MATCH）。随即在该窗口对 `tests/fixtures/t1_tiny.json` 跑 scientific `prepare --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15` → `collect --backend tiny --weight-seed 0` → `intervene --backend tiny` → `intervene --dev-layer-scores 0.05 0.9 0.8` → `repair --eval-mode scientific --mask task_oracle`，并用 monkeypatch 记录每一次 `intervene_hidden_decode`。交卷再算同一脚本为 `3d0a0764…fbc6`（中间一度 `5413a4bc…`）。核验（锚定开审 MATCH 树）：

1. **生成区事件：** 6/6 `parse_region=generated`，仅生成区 `q`，`start` 不落入 prompt；问句 p1/p2 不是生成事件。
2. **有限 \(H\)：** `(6,32)` 全有限，与 `event_rows` 对齐；`start=0` 跳过；scientific 拒绝 offline 前缀 id。
3. **A13-01 donor：** `same_value_diff_source`，行 `(0,3)` = `trace-base`/`trace-source` 的 `q`，**不是** `trace-t0p`，**不是** `trace-edit`；\(\\|H_0-H_3\\|\approx 0.01174\)（有限、非恒等）。source 臂是 `apply_alt_source_same_value`（`(alt source)`、父节点改变、目标值不变），不是 rename-only。去掉 source tid 才回退 value-edit。
4. **INLP：** `mode=inlp`，\(h@P\)，无 donor，rank 30，与 \(\Pi_Z\) 不是同一变换。
5. **独立 decode：** 无 flag 四次（swap / C-rand `add_delta` / INLP / rescue `replace`）；有 flag 五次，C-layer 在弱层 0 用对拍过的 `c_layer_delta`。
6. **`ie_z`：** `target_follow`；本机无 follow，值为 **0**，按口令记为诚实。
7. **几何 timing：** 顶栏保持 **`offline_hidden`**；不得写成 tiny 上的 live `pre_step` hook。
8. **Prefill：** `0` / `True` / `[0]` 拒绝；scientific repair k=1..5 有真实 32 维 hidden。
9. **教师强制：** 6/6 `constrained_target`；不是 §4.1，也不是 MODEL-01。

这些仍不够支持把本报告签在声称快照 `401e509b…` 上：交卷磁盘是 `3d0a0764…`。也仍不够支持把指定路径写成论文同批次交换/消融/救援实验结果：五种模式都抽出 `9`，相对对照为 0，donor 轨迹答案是约束 `"82"` 不是金标 0。诚实的 tiny 接线证明 ≠ MODEL-01 / CAUSAL-01/02 完成。真实 HF / 官方 dump / CUDA / 50 条 C2 保持 `pending_server`。
