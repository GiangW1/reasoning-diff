# D-causal 独立审查报告（round-17）

通道 D：模型与因果（token/prefix、thinking 模板、sampling、hook/KV、donor 来源、swap/消融/救援、两类对照、nontarget/invalid）。指定独立复跑 scientific `prepare`→`collect --backend tiny --weight-seed 0`→`intervene --backend tiny`（另跑 `--dev-layer-scores 0.05 0.9 0.8`）→`repair --eval-mode scientific`，夹具 `tests/fixtures/t1_tiny.json`，`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15`。猎项：`parse_region=generated`；事件 `start ≥` 问句；生成区无 prompt `p1`/`p2` 作为 \(s_i\)；有限 \(H\)、无 NaN `pre_step` 行、`start=0` 不可表达跳过；**D14-05** 无静默 48 字符帽，source `prompt_text` 含完整改写式（XOR 落地则 `* src_b`）；**A14-02** donor `same_value_diff_source` 为 keep-*a* add-*b* 而非 rename，配对跳过全 NaN \(H\) 行，有 source 时优先于 value-edit；INLP 为 \(h@P\)；swap \(H'=H_{\mathrm{base}}+\Pi_Z(H_{\mathrm{donor}}-H_{\mathrm{base}})\)；C-rand `add_delta` / rescue `replace`；C-rand/C-layer 锁实际范数；弱层来自 dev 不是 test；`ie_z` 用 target-follow \(g(Y)\)；Prefill 接受有限非零 32-d，拒绝 None/bool/str/scalar/`[0]`；教师强制诚实标 `constrained_target`。tiny **不是** MODEL-01。约束 `\nq = <digit>` **不是** §4.1 自然 CoT。不得写 §4.1 / MODEL-01 已验收。`IsolatedExecutor` ≠ `ChildProcessExecutor`；无 host exec。

独立性声明：未阅读 `.planning/audits/round-17/` 下除 `VERSION.md` 与本文件外的其他通道报告；只把 `.planning/audits/round-17/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账。对照读了本通道 round-14 / round-15 报告仅作版式与猎单，不作本轮证据。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试绿当作论文正确性；不把作者 `local close` 或声称 160 passed 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。

对照原文：论文 §2.4（交换公式、C-rand/C-layer 同批次）、§4.1（自然 CoT，本机不得冒称）、§4.2（三位置）、§6/§8（来源—数值 / 交换 / Knock-out / Rescue）；GOAL MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01；`docs/EXPERIMENT_PROTOCOL.md` §4。tiny 路径只验收接口与接线，不验收 MODEL-01。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结 **HASH_MATCH** `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（61 文件，0 CRLF）。该窗口立即开跑的指定 scientific 路径上，点名猎项全部成立：source `prompt_text` 含完整 `* src_b`（无 `p2_src` / `(alt source)` / 丢尾）；XOR keep-*a* add-*b*；donor `(0,3,same_value_diff_source)`；配对跳过全 NaN；INLP \(h@P\)；swap 公式逐位；四 mode 接线；C-rand/C-layer 范数与落盘逐位一致；弱层 0 来自 dev；生成区事件；Prefill 接受/拒绝；`constrained_target` 诚实。审查窗口内他方改写冻结集：`cli.py`（开审列目录 61662 B → 交卷 61646 B / `9431b776…`，mtime 02:57:30）与 `tests/test_round07_regressions.py`（14862 → 16262 B，mtime 02:57:36）。交卷同脚本为 **HASH_MISMATCH** `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（仍 61，0 CRLF）。本通道未改冻结集。tiny 不是 MODEL-01，不得写 §4.1。

**总裁决：FAIL。开审 HASH_MATCH。交卷 HASH_MISMATCH。指定猎项在开审后立即复跑的磁盘行为上关闭，但不能把本报告签在声称快照 `3d0a0764…` 上。不宣布 Goal 完成。不得启动连续通过计数。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21（Asia/Shanghai）；开审约 02:56，交卷约 03:08 |
| 声称冻结 hash | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（`.planning/audits/round-17/VERSION.md`；61 文件；POSIX relpath + NUL + bytes） |
| 开审复算 | **HASH_MATCH。** 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → **61** 文件 → `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`；CRLF **0** |
| 交卷复算 | **HASH_MISMATCH。** 同脚本 → 61 文件 / `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`；CRLF **0**。本通道未改冻结集 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；`src/`/`tests/`/`pyproject.toml` 为未跟踪。HEAD 不是冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载；无 CUDA |
| 作者 pytest 声称 | 160 passed。本机因果 7 文件 **70 passed / 24.29s**；其后全量 **162 passed / 37.02s / 162 collected**（交卷漂移树，含被加长的 `test_round07_regressions.py`）。绿只锁回归，不是论文正确性；**不得**把 162 绑到声称快照 `3d0a0764…` |
| 明确未读 | `.planning/audits/round-17/` 下除 `VERSION.md` 与本文件外的其他通道报告 |

因果生产文件（交卷 SHA-256 前 16 / 字节；开审列目录时的字节若不同则标出）：

| 文件 | 交卷 SHA-256 前 16 / 字节 | 开审→交卷 |
|---|---|---|
| `cli.py` | `9431b7768fda6a3c` / 61646 B | 开审列目录 **61662 B**；mtime 02:57:30。本通道未写 |
| `edits.py` | `1e5b97d63a62ab78` / 13773 B | 开审=交卷 |
| `collect.py` | `83658cd8ba879f20` / 9627 B / 261 行 | 同 |
| `generate.py` | `6e6040394ac641c7` / 7750 B | 同 |
| `tiny.py` | `c75d0f5325766612` / 3510 B | 同 |
| `features.py` | `0a9f0b8beb0185ae` / 1338 B | 同 |
| `adapters.py` | `c1992624026a1bf0` / 1313 B | 同 |
| `tokenize.py` | `b0cc8974af1010fa` / 1162 B | 同 |
| `interventions.py` | `0ffdbb8805be7649` / 4003 B / 115 行 | 同 |
| `repair.py` | `f76ff9998b9a6b17` / 7828 B / 232 行 | 同 |
| `events.py` | `290a4fd676ac0814` / 11563 B | 同 |
| `executor.py` | `481d6ed597c93e78` / 3861 B | 同 |
| `rng.py` | `2098c2c72a852eaa` / 1723 B | 同 |
| `tests/test_round07_regressions.py` | 交卷 16262 B | 开审列目录 **14862 B**；mtime 02:57:36。本通道未写 |

指定复跑目录（本通道自建）：`.planning/audits/round-17/_d_scratch/{prep,col,int,int-dev,rep}`。另：`col-off`（scientific+offline 拒绝）、`int-spy` / `int-dev-spy`（monkeypatch 记 mode/layer）。

## 2. 范围与逐文件覆盖

指派阅读并逐行核对（行号为交卷磁盘 = 本通道复跑所用字节；`cli.py` 开审列目录曾为 61662 B，复跑与阅读用的是 61646 B / `9431b776…`）：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / 卡片 `think_ids` / `load_frozen(..., local_files_only=True)`。`revision=="latest"` 拒绝 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids`（**非互逆**）/ `readout_layer_index`（60%–75% 带）/ `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–261 | `collect_hidden_trace` 不可表达步前 **continue**；`intervene_hidden_decode` 四 mode：`pi_z_swap` / `inlp`（`vec @ proj`）/ `add_delta` / `replace` |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–201 | `sample_next`；`decode_loop`（独立 `torch.Generator`）；`append_target_assignment`；`generate_task_trace` **无** `[:48]`；`len(prompt_ids)>96` 则 raise；只解析生成区；`apply_model_template` 有定义、CLI / `generate_task_trace` **无调用** |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step`。`max_position_embeddings=128` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / `inlp_remove`（在已投影 `work` 上迭代）/ `rescue_controls` / `select_weak_layer` / 库函数 `ie_z`（隐向量均值）/ `intervention_report` |
| `src/reasoning_diff/edits.py` | 109–365 | `apply_value_edit`；`apply_rename_edit`；`apply_alt_source_same_value`（保留叶 *a*、固定名 `src_b`、父节点改读 *b*、目标值不变）；`make_source_value_pair` |
| `src/reasoning_diff/repair.py` | 1–232 | `_hidden_is_prefill` 拒绝 None/bool/str/标量/`size<2`/`[0]`；`execute_repair_tiny`；`run_repair` |
| `src/reasoning_diff/cli.py` | 216–438、440–547、683–710、817–1062 | prepare/collect/pair/donor/intervene/repair。`_pair_source_value` 先 `same_value_diff_source` 再 `same_source_diff_value`，跳过非有限行 |
| `src/reasoning_diff/executor.py` | 1–109 | `ChildProcessExecutor` **不是** `IsolatedExecutor` 子类；`isolated_sandbox=False`；默认 `UnavailableExecutor`；`forbid_host_exec` |
| `src/reasoning_diff/rng.py` | 41–53 | StreamBank `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/events.py` | 74–89、251–274 | `parse_events`；`boundary_index`（`start=0`/`before` → None）；`extract_answer` 去 think |
| `src/reasoning_diff/schema.py` | 39 | `POSITION_KINDS` |
| `src/reasoning_diff/scoring.py` | 19–30 | `score_code` 走 `get_executor()`，默认不 host exec |
| `tests/test_tiny_hooks.py` | 全文件 | 前向 + hook 清理（绿只作冒烟） |
| `tests/test_tiny_cache.py` | 全文件 | cache 隔离冒烟 |
| `tests/test_generate_loop.py` | 全文件 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | scientific / Prefill / readout / pair 字段 | 字段锁，不替代本轮复跑 |
| `tests/test_round05_regressions.py` | scientific 事件 / 几何 timing | 同上 |
| `tests/test_round06_regressions.py` | `donor_kind`/`inlp`/`add_delta`/`replace`/`ie_z_g` | **不**比 \(h@P\) 数值 |
| `tests/test_round07_regressions.py` | 标量/`[0]` Prefill；XOR `src_b`；pair | 开审 14862 B；交卷 16262 B **未经**本通道按新字节重核全部断言 |

支持性阅读：`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` 上列要求；论文 §2.4 / §4.1 / §4.2 / §6 / §8 / §9。未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次、自然 CoT。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`、`measure.py`、`splits.py`（他通道）。`cli.py` 校准/fit 段属其他通道。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | VERSION 脚本逐字复算 | **开审 HASH_MATCH** 61 / `3d0a0764…f6fdfbc6`（0 CRLF）。**交卷 HASH_MISMATCH** 61 / `3d0f1c10…b7c0952f`。见 D17-00 |
| X2 | 因果相关 pytest 7 文件 | **70 passed / 24.29s**（`test_tiny_hooks` / `test_tiny_cache` / `test_generate_loop` / `test_round04–07_regressions`）。绿只锁冒烟与字段名 |
| X2b | 全量 pytest | **162 passed / 37.02s / 162 collected / exit 0**。作者声称 160。数字对交卷漂移树，**不得**绑到 `3d0a0764…`。仍不是论文正确性 |
| X3 | `apply_swap` 标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)。随机 3-d：`apply_swap` 与 \(H_b+\Pi_Z(H_d-H_b)\) 最大差 **0** |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV | DynamicCache，对象隔离。层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.178\)、\(\Delta V_{\max}=0.320\)，且 **仅 last token**（earlyK=0） |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3** 次；`once=True` **1** 次 |
| X7 | hook `finally` 清理 | `RuntimeError` 后 `_forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)` |
| X8c | 空事件 / `start=0` | `h_position=no_event`，\(H\) `(0,32)`，`event_ids=[]`，不塌成末 token |
| X8e | **指定** scientific `prepare`→`collect --backend tiny --weight-seed 0` | 6 条轨迹：`trace-base` / `trace-t0p` / `trace-edit` / `trace-source` / `p1:0` / `p2:2`。每条 **1** 个生成区 `q`（base/edit `start=45`；source `58`；`parse_region=generated`，`parse_status=constrained_target`）。问句前提不进入事件。`H` `(6,32)` **6/6 行有限**（0 NaN）；`H_pre_step/value/post` 同形、0 NaN 行；`H`≡`H_pre_step`（\(\Delta=0\)）。`event_rows.jsonl` 6 行皆 `{node_id:q, trace_id:…}`。`hidden_layer=1`；`weight_source=random_init`；`weight_seed=0`。行 2≡行 5（默认 edit 与 `_allowed_edits` 的 `p2:2` 撞车） |
| X8f | scientific collect 拒绝 | `--backend offline` → `ValueError: scientific collect refuses offline_prefix_ids as H`（exit 1） |
| X8g | re-encode vs 生成 ids | base 轨迹与 `encode_text(text)` 有 **8** 处不同（恰 `max_new=8` 乱码段）。collect 的 \(H\) 是对表面文本的二次前向 |
| X8h | 步前 vs 前缀前向 | `H[0]` 与 `encode_text(text[:45])` 末 token **逐位相等**（\(\Delta=0\)）；与步尾 \(\\|\cdot\\|\approx 0.147\) |
| X9 | `leaks_target` | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None` |
| X10 | `boundary_index` / 不可表达 | `start=0,"before"` → **None**。`select_prefix_index(...,0,"pre_step")`：`expressible=False`。`limit=2` 的 `"before"` / `"end"` / `"value"` 皆为 1 |
| X11 | INLP / rescue 算法 | `rescue([1,0],[0,1])=[1,1]`。间谍：`out == in @ P`（maxabs 0），`out ≠ in`（0.032）。`out` 与 `apply_swap` 差 **0.033**（不是同一变换）。2 点拟合 `inlp_rank=30`。库函数 `ie_z` 是隐向量均值；**CLI tiny 路径不写该值** |
| X12 | C-rand / C-layer 范数与弱层 | 缺范数仍 `ValueError`（`C-rand requires the actual main-intervention norm`）。空 dev 曲线 `ValueError`。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0`。指定路径三项范数与独立 StreamBank 重算及落盘 **逐位相等**：`main=0.0027914017810666864`，`crand=clayer=0.002791401781066686` |
| X13 | StreamBank vs hook 基 | `direction` 第一抽 113750710（丢弃）；第二抽 **basis_seed=1153799966**。`sample` 第一抽 **1191642646**。`perturb` 17172908 |
| X14c | **指定** collect→intervene（**无** `--dev-layer-scores`） | `_pair_source_value` 返回 **`(0, 3, same_value_diff_source)`** = `trace-base` / `trace-source` 的同身份 `q`（**不是** `trace-t0p`，**不是** `trace-edit`）。`status=prospective_decode`，几何 **`timing=offline_hidden`**。`relative.hook_once=resid_post`，`transform=pi_z_swap`，`hook_timing=pre_step`（hook 内部标签，几何字段未改写）。monkeypatch 记录 **4** 次：层皆 **1**，模式 **`pi_z_swap` / `add_delta` / `inlp` / `replace`**，`hook_fired=true`。INLP **无 donor**、有 `projector` rank 30。`clayer_status=dev_scores_missing`（无弱层 decode）。`ie_z=0.0`，`ie_z_g=target_follow`。对照四项因 clayer 空而 **null**。`prefix_truncated=false` |
| X14d | 另跑 `--dev-layer-scores 0.05 0.9 0.8` | **5** 次独立 decode，层 **1 / 1 / 0 / 1 / 1**，模式 **`pi_z_swap` / `add_delta`(C-rand) / `add_delta`(C-layer) / `inlp` / `replace`**。`clayer_status=dev_weak_layer_decode`，`weak_layer=0`。三项范数与独立重算及落盘一致。相对四项 `vs_crand=vs_clayer=0.0`。`donor_kind` 仍为 `same_value_diff_source`，`donor_rows=[0,3]` |
| X14e | A14-02 偏好 / NaN 跳过 | 抹掉 pair 元数据里的 `same_value_diff_source` tid 后，同一 \(H\) 回退 **`(0, 2, same_source_diff_value)`**。生产路径 **没有** 走这条回退。把 donor 行 3 置 NaN → 回退 `(0,2,same_source_diff_value)`（跳过全 NaN source 行）。把 base 行 0 置 NaN → `_pair_source_value` **None**。无 rename 轨迹 |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：闭合 think 后数字 → 7；未闭合 → None；`\\boxed{7}` → 7。`apply_model_template` / `think_ids` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 与 `generate_task_trace` 无调用**。本轮不要求自然 CoT |
| X16 | `clone_cache` / DynamicCache | clone ≠ 原对象；`data_ptr` 不同；`add_` 后隔离（maxabs 1.0）；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.686\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False`。`forbid_host_exec` 抛 `RuntimeError`。`score_code` 无 executor 参数时走默认 Unavailable |
| X19 | Prefill | `execute_repair_tiny` 返回 **32** 维有限非零（\(\\|h\\|\approx 5.65\)）。`run_repair` 接受该向量 → `refilled_prefix=True`/`ok`。`None` / `True` / `False` / `"x"` / `0` / `1.0` / `[0]` / `[0.0]` / `[]` / 标量 `array(3.)` / `array([0.])` / 仅 `prefix_token_ids` → `prefill_unavailable`。scientific CLI repair：k=1..5 皆 `refilled_prefix=True`、`status=ok`、`gated=False`、`extra_prefill_tokens=32`；jsonl **无** `prefill_hidden` 字段 |
| X20 | `weight_seed` | 同 seed 同 ids → \(\\|\Delta H\\|_{\max}=0\)；异 seed → 0.099；同 seed 异 ids → 0.072。CLI collect 写入 spec `weight_seed=0` |
| X21 | 来源-数值 / A14-02 图 | `edits.jsonl` 含 `kind=source_value_pair`：targets=`["q"]`，nontargets=`["p1"]`，`trace_ids={base:trace-base, same_source_diff_value:trace-edit, same_value_diff_source:trace-source}`。source 臂 `kind=same_value_diff_source`，问句 `p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?`，premises `{p1,p2,src_b}`，parents `q←{p1,src_b}`（base 为 `{p1,p2}`），表达式 `p1 * src_b`，答案值仍为 **0**。value 臂改 `p2:0→2`，答案 **8**。rename 库函数对照问句为 `p1 = 4. p2_src = 0. What is q = p1 * p2_src?`，**丢掉**叶 `p2`。`make_source_value_pair` 调 `apply_alt_source_same_value`，不调 `apply_rename_edit`。`_try_source_value_pair` 对 T3 / hotpotqa 返回 None |
| X22 | 事件跨度 / hook 前缀 | 生成区 `q` 跨度 45–51（source 58–64），前缀 45（source 58）字符；intervene `ids[:64]` **未截断**（`prefix_truncated=false`）。6/6 `start ≥ len(prompt_text)` 且 `start ≥ prompt_len`（本机 1 字符 = 1 token） |
| X23 | \(g(Y)\) / `ie_z` | donor/base 轨迹 `answer` 皆为约束赋值 **「82」**（seed=0 同权重抽样，不是金答案 0）。intervene 主/对照/INLP/rescue/C-layer 抽取答案皆 **「9」**，`followed_donor=false`。`ie_z=1{9==82}-1{9==82}=0`，`ie_z_g=target_follow`。库函数隐向量均值 **未被** CLI tiny 路径写入 |
| X24 | INLP hook 不是 swap | 间谍 `out == in @ P`（maxabs 0），`out ≠ in`。CLI `mode="inlp"`，无 donor，有 projector。2 点拟合 `inlp_rank=30` |
| X25 | 教师强制 / 采样 | `target_assignment='\nq = 82'`（t0p 为 `\nq = 53`）；`parse_status=constrained_target`；`correct=false`（金标 0）。6 条 `sampling={temperature:1.0,top_k:0,top_p:1.0}`。`decode_loop` 用独立 `Generator`，不用 `HF generate`。intervene decode **不再**教师强制 |
| X26 | 问句单独解析 | 对 6 条 `prompt_text` 跑 `parse_events` 会打出 p1/p2（source 问句为 p1/`p2`/`src_b`）。generate **不解析问句**，故这些不是生成事件 \(s_i\) |
| X27 | 卡片 revision | `qwen3-8b` `b968826d9c…` think `(151667,151668)`；`r1-distill-qwen-7b` `916b56a4…` think `(151648,151649)`。本机未加载。缺名 `card` 抛 `KeyError` |
| X28 | D14-05 题干帽 | `generate.py` **无** `[:48]`、无字面 `48`。`len(prompt_ids)>96` → `ValueError: tiny prompt exceeds context; refuse truncated source/value prompts`（97 个 `y` 复现）。tiny `max_position_embeddings=128`。source `prompt_text` 实字节见下 |

### 运行时证据（指定路径）

**source `prompt_text`（D14-05，UTF-8 49 字节，完整改写式）：**

```
p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?
```

hex: `7031203d20342e207032203d2030207372635f62203d20302e20576861742069732071203d207031202a207372635f623f`

- 含 `* src_b`，以 `src_b?` 结尾。
- **无** `p2_src`。**无** `(alt source)`。**无**丢尾。
- `prompt_len=49`。若仍有静默 48 帽，末字节 `?` 会丢；实际保留。

**parents / 图：**

| 臂 | question | premises | q.parents | expression | answer |
|---|---|---|---|---|---|
| base | `p1 = 4. p2 = 0. What is q = p1 * p2?` | p1,p2 | p1,p2 | `p1 * p2` | 0 |
| source (XOR) | 上列 49 字节 | p1,**p2**,**src_b** | p1,**src_b** | `p1 * src_b` | 0 |
| value-edit | `p1 = 4. p2 = 2. What is q = p1 * p2?` | p1,p2 | p1,p2 | `p1 * p2` | 8 |
| rename（库对照，生产未生成） | `p1 = 4. p2_src = 0. What is q = p1 * p2_src?` | p1,p2_src | p1,p2_src | `p1 * p2_src` | 0 |

**H / donor / transform：**

- \(H\) shape `(6,32)`，全部有限；`donor_kind=same_value_diff_source`；`donor_rows=[0,3]`。
- 主干预 `transform=pi_z_swap`；C-rand `add_delta`；C-layer（有 dev 分）`add_delta` 层 **0**；INLP `inlp`；rescue `replace`。
- 6/6 事件 `node_id=q`，`parse_region=generated`，`parse_status=constrained_target`。

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验卡片 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server`。本轮不要求自然 CoT |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存；CLI 未调用。属 `pending_server`。tiny **不是** MODEL-01 |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机是接口证明 |
| 把 160/162 passed 写成 Goal / MODEL-01 验收 | 绿测试不是论文正确性 |
| 交卷 `test_round07_regressions.py` 16262 B 的新增断言 | 窗口内他方写入；本通道不把新锁当独立关闭 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

`ISSUES.md` 只当作者主张。

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| A14-02 | `apply_alt_source_same_value` 保留叶 *a*，追加等值 `src_b`，父母改读 *b*；intervene 优先 `trace-source` | **指定路径独立关闭（开审后立即复跑的字节）。** X14c/d/e、X21。不是 rename。交卷冻结 hash 已漂，**不能**记为声称快照上的关闭 |
| D14-05 | tiny 不再 48 字符截断题干；超上下文则拒绝 | **指定路径独立关闭（同上）。** X28、source 实字节。交卷 hash 已漂 |
| A14-03 | scientific `fit` 对 verbalizer/attention_* 写 `refused_not_section8` | **不裁定。** A/E |
| A14-04 | `noise_ref=0` 且无 `sham:` 时 `noise_set=None` | **不裁定。** A/C |
| A13-01 | 来源臂不是 rename-only；优先 `trace-source` | 被 A14-02 吸收。指定路径行为成立，裁定同 A14-02 |
| A13-02 | 未知行为 → \(M=\emptyset\) | **不裁定。** A/C |
| A13-03 | 任意 `sham:` 行 → `noise_set=None` | **不裁定。** A/B |
| A12-03 | `_find_tasks_jsonl` 只读传入目录 | **不裁定。** A/E/F |
| A10-04 Plus family persist-lock | `splits.py` / 磁盘并集 | **不裁定。** 非本通道猎项 |
| pending_server | 真实权重 / 50 条 C2 / 官方 CoT | **同意未关。** 约束 `q` 不是 §4.1；tiny 不是 MODEL-01 |
| Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |

## 6. 发现

### D17-00 — 声称冻结 hash 对交卷磁盘不成立

- **状态：** confirmed defect（过程 / QA-01）
- **严重度：** high
- **文件 / 符号 / 行号：** `.planning/audits/round-17/VERSION.md` 声称 61 文件 / `3d0a0764…f6fdfbc6`；交卷磁盘 61 文件 rel+NUL+bytes = `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`
- **触发条件：** 按 VERSION 脚本在开审、猎项复跑后、成文后、交卷前各复算
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。开审 MATCH。窗口内他方写入：`src/reasoning_diff/cli.py` mtime 02:57:30（开审列目录 61662 B → 交卷 61646 B / `9431b776…`）；`tests/test_round07_regressions.py` mtime 02:57:36（14862 → 16262 B）。本通道未改这些文件。`generate.py` `6e604039…`、`tiny.py` `c75d0f53…`、`edits.py` `1e5b97d6…`、`collect.py` `83658cd8…`、`interventions.py` `0ffdbb88…`、`repair.py` `f76ff999…` 开审列目录字节=交卷
- **影响：** 不能把本报告说成「已在声称快照 `3d0a0764…` 上签字」。猎项锚定开审 MATCH 之后立即复跑的磁盘行为（`cli.py` 复跑用的是 61646 B）。不得启动连续通过计数
- **建议：** 停写、重冻、审查者只对一个 hash 交卷。并行通道不得在审查窗口改冻结集合

### D17-01 — D14-05：无静默 48 帽；source `prompt_text` 含完整 `* src_b`

- **状态：** closed（指定路径；绑定开审后复跑字节，不是声称快照）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **122–125**（`>96` raise；源中无 `[:48]` / 无字面 `48`）；`tiny.py` **32**（`max_position_embeddings=128`）；`edits.py` **219–292**
- **对应要求：** D14-05；CAUSAL-02 题干完整性
- **证据：** X28、X8e、X21。source `prompt_text` 49 字节 hex 见 §3。无 `p2_src`、无 `(alt source)`、无丢尾。97 字符问句 raise `tiny prompt exceeds context; refuse truncated source/value prompts`
- **影响：** 指定夹具不再静默砍 source 题干。这不是自然 CoT，也不声称 MODEL-01
- **残留：** `cli.py` **950–952** 仍对 intervene 前缀 `ids[:64]` 截断并写 `prefix_truncated`。本夹具 source 事件 start=58，`prefix_truncated=false`，未触发。不是本轮 D14-05 缺陷

### D17-02 — A14-02：XOR keep-*a* add-*b*；配对优先 source；跳过全 NaN \(H\) 行

- **状态：** closed（指定路径；绑定开审后复跑字节）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `edits.py` **219–292**、**295–304**；`cli.py` **827–850**、**298–302**
- **对应要求：** A14-02；CAUSAL-02
- **证据：** X14c/d/e、X21。保留叶 `p2`，新增 `src_b`，父母改读 `src_b` 不读 `p2`，目标值仍 0。生产 donor `(0,3,same_value_diff_source)`。抹掉 source tid 才回退 value-edit `(0,2)`。NaN 行 3 → 跳过 source；NaN 行 0 → 无 pair。`make_source_value_pair` 不调用 `apply_rename_edit`
- **影响：** 指定路径的来源臂不是 rename-only，有 source donor 时不是 value-edit-only

### D17-03 — 只解析生成区；问句 p1/p2 不是 \(s_i\)

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **147–157**（`parse_events(generated)` 再 `+= len(prompt)`；`parse_region="generated"`；赋值落在 `gen_text` 之后则 `constrained_target`）
- **对应要求：** POS-01 下限；猎项 generated-region events
- **证据：** X8e、X22、X25、X26。6/6 事件节点皆 `q`。问句单独解析会出 p1/p2/`src_b`，说明排除靠「不解析问句」
- **影响：** 指定路径不再把 prompt 前提写进 \(H\) 行。不是自然 CoT

### D17-04 — \(H\) 全有限；`start=0` 不可表达跳过；无 NaN `pre_step` 行

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `events.py` **251–257**；`features.py` **8–34**；`collect.py` **50–52**
- **对应要求：** POS-01；猎项 pre_step inexpressible
- **证据：** X8c、X8e、X10。`boundary_index(...,0,"before")` is None。`start=0` collect → `H` `(0,32)` / `no_event`。指定路径 6/6 `pre_step` 行有限

### D17-05 — 四 mode / INLP \(h@P\) / swap 公式 / 范数 / 弱层来自 dev

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `collect.py` **179–208**；`interventions.py` **9–16**、**31–49**、**52–67**、**92–95**；`cli.py` **906–992**
- **对应要求：** CAUSAL-01；INLP-01；MEDIATION-01；IE-01
- **证据：** X3、X11、X12、X14c/d、X23、X24。swap 公式 maxabs 0。INLP hook `in@P`。无 `--dev-layer-scores` 不跑弱层；有则层 0（dev 曲线最小，不是 test）。范数与落盘逐位一致。`ie_z_g=target_follow`

### D17-06 — Prefill 拒绝 None/bool/str/scalar/`[0]`；接受有限非零 32-d

- **状态：** closed
- **严重度：** n/a
- **文件 / 符号 / 行号：** `repair.py` **14–23**、**87–135**、**138–174**
- **对应要求：** REPAIR-01 Prefill
- **证据：** X19。scientific k=1..5 皆 `ok` / `refilled_prefix=True` / `gated=False`

### D17-07 — 教师强制诚实；`IsolatedExecutor` ≠ `ChildProcessExecutor`

- **状态：** closed（接口）
- **严重度：** n/a
- **文件 / 符号 / 行号：** `generate.py` **72–98**、**156–157**；`executor.py` **27–62**、**97–109**；`scoring.py` **19–30**
- **对应要求：** 猎项诚实 `constrained_target`；EXEC-01。**不**写 §4.1 / MODEL-01
- **证据：** X18、X25。6/6 `parse_status=constrained_target`，`target_assignment` 以 `\nq = ` 开头。ChildProcess 不是 Isolated 子类。默认 Unavailable。无 host exec 回退

## 7. 残留与不得升级

- intervene 前缀 `ids[:64]`（`cli.py` 950–952）对本夹具未触发。更长 source 前缀会静默截断并标 `prefix_truncated`。不是本轮 D14-05 复现。
- source 问句标点为 `p2 = 0 src_b = 0.`（原 `p2 = 0.` 的句点落到 `src_b` 后）。表达式完整，不记缺陷。
- 行 2≡行 5：默认 value-edit 与 `_allowed_edits` 的 `p2:2` 重复。不改变 source donor 选择。
- tiny 随机权重上主干预与对照答案皆为「9」、`ie_z=0`：接口证明，不是 C2 成立。
- `apply_model_template` / `load_frozen` / 官方 think 模板未接入 generate CLI：`pending_server`，不得写成 MODEL-01。
- 几何 `timing` 保持 `offline_hidden`。hook 内部 `hook_timing=pre_step` 不得写成 live 步前已证。

## 8. 总裁决

**FAIL。**

- 开审：**HASH_MATCH** `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（61 / 0 CRLF）。
- 交卷：**HASH_MISMATCH** `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（61 / 0 CRLF）。
- 指定猎项（D14-05 / A14-02 / 生成区事件 / 有限 \(H\) / `start=0` / 四 mode / INLP / 范数 / dev 弱层 / Prefill / `constrained_target` / Isolated≠Child）在开审后立即复跑的磁盘行为上成立。
- 不得把本报告签在声称快照上。不宣布 Goal / MODEL-01 / §4.1 完成。不得启动连续通过计数。
