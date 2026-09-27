# D-causal 独立审查报告（round-08）

通道 D：模型与因果（tiny generate/collect/hook、三时机、swap \(\Pi_Z\)、C-rand/C-layer——弱层是对照不是主干预、INLP/rescue、来源-数值、Prefill KV、权重 seed）。指定复跑 scientific `prepare`→`collect --backend tiny`→`intervene --backend tiny`。几何 `timing` 必须保持 `offline_hidden`，不得被 hook 改写成 `pre_step`。猎项：donor 配对、有限 \(H\)、`offline_hidden`、`source_value_pair`、`basis_seed`、C-layer 第二次 decode、Prefill hidden。tiny **不是** MODEL-01。

独立性声明：未阅读 round-08 其他通道报告；只把 `.planning/audits/round-08/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账；对照阅读了本通道 round-01–06 报告以便核对关闭项，结论以本机当前磁盘与本轮复跑为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试通过当作实现正确；不把作者 `local close` 或声称 144 passed 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01 完成（真实 HF 为 `pending_server`）。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。诚实的 `offline_prefix_ids` 在未被宣称为隐状态时不记缺陷。约束 `\nq = <digit>` 是本机可解析接口，不是 §4.1 自然 CoT。

对照原文：论文 §2.4（交换公式、前瞻定位、C-rand/C-layer 同批次）、§4.2（步前/值前/步尾与 span 池化）、§6（V-Probing 时机对照）、§8（科学评测含交换/消融/救援）；GOAL §5.6–5.11、§5.13、§5.15；`docs/EXPERIMENT_PROTOCOL.md` §4。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T02:13:22+08:00 |
| 声称冻结 hash | `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`（`.planning/audits/round-08/VERSION.md`；60 文件；POSIX relpath + NUL + bytes） |
| 独立复算 hash | **HASH_MATCH。** 按 VERSION 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → **60 文件** → `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e` |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏，`src/`/`tests/`/`pyproject.toml` 为未跟踪；审查对象是冻结脚本覆盖的 60 个文件字节） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载；无 CUDA |
| 作者 pytest 声称 | 144 passed。本通道只重跑所引用子集，不把 144 记为已验证 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / 卡片 `think_ids` / `load_frozen(..., local_files_only=True)`。无独立 `think_ids()` 函数 |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids` / `readout_layer_index`（60%–75% 带） / `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–199 | `collect_hidden_trace`：不可表达步前 **跳过**（不入 \(H\)）；`collect_tiny`；`intervene_tiny` / `intervene_swap_decode(..., basis_seed=)` |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)`；`assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–201 | `sample_next`；`decode_loop`；`append_target_assignment`；`generate_task_trace`（只解析生成区）；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` / `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / INLP / `rescue_controls` / `select_weak_layer` / `ie_z` / `intervention_report` |
| `src/reasoning_diff/repair.py` | 1–223 | `mask_prefix` / `execute_repair_tiny` Prefill hidden+KV / `run_repair` 拒绝无 hidden / `consecutive_repairs` |
| `src/reasoning_diff/cli.py` | 1–1164 | 重点 `cmd_prepare` 257–428、`cmd_collect` 431–534、`_expressible_donor` 775–793、`cmd_intervene` 796–909、`cmd_repair` 912–952 |
| `src/reasoning_diff/executor.py` | 1–109 | `IsolatedExecutor` unavailable；`ChildProcessExecutor.isolated_sandbox=False`；默认 Unavailable |
| `src/reasoning_diff/rng.py` | 41–53 | `StreamBank` 名 `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/edits.py` | 204–234 | `make_source_value_pair` / `apply_source_value_edit` |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理 |
| `tests/test_tiny_cache.py` | 1–26 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | 25–137、218–220 | readout 带；scientific collect span；offline 几何≠`pre_step`；repair Prefill；子进程非隔离 |
| `tests/test_round05_regressions.py` | 23–136 | scientific 事件；几何 timing≠`pre_step`；dummy 非 Prefill |
| `tests/test_round06_regressions.py` | 25–78 | 生成区事件；有限 \(H\) 与 donor；`offline_hidden`；`dev_weak_layer_decode`；prefix ids 非 Prefill |

支持性阅读：`events.py` `parse_events` 74–88、`boundary_index` 237–243、`extract_answer` 246–260；`scoring.py` `score_code` 19–30；`schema.py` `POSITION_KINDS` 39；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / EXEC-01 / REPAIR-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2 同批次。未逐行审计：`analysis.py` 统计、`probes/bilinear.py`、`transfer.py`。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（VERSION 脚本逐字） | **HASH_MATCH** `1b88bec2…91e257e`；60 文件 |
| X2 | pytest tiny/因果相关 6 个文件 | **52 passed / 17.14s**。通过只证明冒烟与回归锁，不证明因果协议或 MODEL-01 |
| X3 | `apply_swap` 与标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\)。全空间 \(I_2\) 则 \(H'=H_d=[0,1]\)（不是缺陷） |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.079\)、\(\Delta V_{\max}=0.111\)，且 **仅 last token**（earlyK=0）。`transform` 形状 `(1,1,32)` |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)`：`once=False` **3 次**；`once=True` **1 次** |
| X7 | hook `finally` 清理 | `RuntimeError` 后 `layer._forward_hooks` 为 0 |
| X8a | `collect_tiny("qwen2",[1,2,3],max_new=2)` | `weight_source=random_init`；`hidden_layer=1`；`hidden_all` `(5,32)`；三位置 token_index **2/3/4**；`sampling` 已写入 |
| X8b | `collect_hidden_trace` + fixture 文本 `"p1 = 4\\np2 = 0\\nq = 0\\n"` | 事件仅 `q` start/value/end = **14/18/19**；token_index **13/17/18**；\(H\) `(1,32)` 有限；三位置 \(\|\Delta\|\approx 0.158/0.239/0.185\)；`E` 两行 \(\|\Delta\|\approx 0.068\) |
| X8c | 空事件库层 | `h_position=no_event`，`H` 形状 `(0,32)`，**不再**塌成末 token |
| X8e | **指定** scientific `prepare`→`collect --backend tiny --weight-seed 0` | 6 条 `tiny-qwen2`，每条 1 个生成区 `q`（`start=45`，`parse_status=constrained_target`，`parse_region=generated`）。`H`/`H_pre_*` 皆 `(6,32)`，**全部有限、0 行 NaN**；`event_rows` 6 行皆 `node_id=q` 且与 \(H\) 行对齐；`hidden_layer=1`；`weight_source=random_init`；`weight_seed=0`。三位置互异（\(\|\Delta\|\approx 0.156/0.147\)），且 \(H[0]\neq\) 该轨迹末 token（\(\|\Delta\|\approx 0.147\)） |
| X8f | scientific collect 拒绝 | `--backend offline` → `scientific collect refuses offline_prefix_ids as H` |
| X8g | re-encode vs 生成 ids | 每条轨迹 51 token 中 **8** 个与 `encode_text(text)` 不同（恰为 `max_new=8` 乱码段）。collect 的 \(H\) 是对表面文本的二次前向 |
| X8h | 全序列步前 vs 前缀前向 | `H[0]` 与 `hidden[44]`（全序列）及 `encode_text(text[:45])` 末 token **逐位相等**（\(\Delta=0\)）。因果前缀一致 |
| X9 | `leaks_target` 能否为 True | 单 token `[[0,10]]` limit=5 → True 且 `token_index=None`。150 次随机偏移中 **30 True / 83 index 空** |
| X10 | `boundary_index(..., 2)` 的 `"before"` / `"end"` / `"value"` | 三者皆为 1；`position` 只做枚举校验 |
| X11 | INLP / rescue | steps=1 vs 8 最大差 **0.999**。`H@P8` 第一列范数 \(\approx 10^{-15}\)。`rescue([1,0],[0,1])=[1,1]`。`rescue_controls` 给出 matched / error_source / random，随机范数匹配 |
| X12 | C-rand / C-layer 范数与弱层选择 | 缺范数仍 `ValueError`。`select_weak_layer({0:0.2,1:0.1,2:0.4})=1`；`{0:0.05,1:0.9,2:0.8}=0`。三项可按同一 `target_norm` 对齐 |
| X13 | StreamBank vs 实际 hook 基 | `direction` 第一抽 113750710（随后被覆盖）；`basis_seed` 第二抽 **1153799966**；`perturb` 17172908。hook 收到同一 `basis_seed`；CLI 几何基与 hook 基 **allclose**。旧 `default_rng(1)` 最大元素差 **0.687** |
| X14a | `intervene_tiny` swap 是否施加 | `transform=pi_z_swap`，logits \(\Delta_{\max}=0.512\)，cache 对象隔离，层 1 |
| X14b | fixture tiny intervene | `H` `(2,32)` 有限；`status=prospective_decode`；几何 **`timing=offline_hidden`**；`--dev-layer-scores 0.05 0.9 0.8` 后 3 次 decode，层号 **1 / 0 / 1**；`weak_layer=0`；`clayer_status=dev_weak_layer_decode`；`donor_rows=[0,1]` |
| X14c | **指定** scientific collect→intervene + 分数 | `_expressible_donor` 返回 **`(0,1)`**（`trace-base` vs `trace-t0p`，同 `node_id=q`，\(\|H_0-H_1\|\approx 0.00778\)）。`status=prospective_decode`，几何 **`timing=offline_hidden`**（hook 内部 `hook_timing=pre_step`，未覆盖几何字段）。主 hook 层 **1=readout**；弱层第二次 decode 层 **0**；INLP 第三次 decode 层 **1**。前缀 45 token = `text[:45]`，**未**被 `[:64]` 截断。`followed_donor=false`；主四项 `invalid=1` 其余 0。`relative` **含** `hook_once`/`transform`/`hook_timing`/`weak_layer`/`donor_rows`/`inlp_followed_donor`/`clayer_followed_donor`。对照四项相对差 **null** |
| X14d | 无 `--dev-layer-scores` | 2 次 decode，层皆 1；`clayer_status=dev_scores_missing`（不写 `dev_weak_layer_decode`） |
| X14e | offline intervene | 仅 1 行前缀 id → `donor_missing` / `timing=unexpressible` / `dev_scores_missing`。不是 `pre_step` |
| X15 | thinking / 模板 / 调用图 | `extract_answer`：未闭合 think → None；闭合 think 后数字 → 3；boxed/#### → 7。`apply_model_template` / `load_frozen` / `clone_cache` / `assert_no_future_leak`：**CLI 无调用**。无 `think_ids()` 函数。`from_pretrained` 仅在 `load_frozen` |
| X16 | `clone_cache` / DynamicCache | 本机无 `.copy()`。clone ≠ 原对象；`data_ptr` 不同；改 clone 后原张量不变；`get_seq_length()=5`。生产路径不调用 |
| X17 | 读出层 vs resid_post | 3 层 → `readout_layer_index=1`。`hidden_states` 长度 4。`hidden_states[layer+1]` 与层 1 resid_post last-token **相等**（\(\Delta=0\)）；`hidden_states[-1]` 与 resid \(\Delta_{\max}=1.686\) |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False`；`SubprocessExecutor is ChildProcessExecutor`。默认 `score_code` → `executor_unavailable` / `value=None` |
| X19a | `execute_repair_tiny` Prefill hidden | 返回 32 维有限非零 `prefill_hidden`；`refilled_prefix=True`。dummy 无 hidden / 空 list / 仅 `prefix_token_ids` → `prefill_unavailable` 且 `refilled_prefix=False` |
| X19b | Prefill KV 与层 | `past_key_values.get_seq_length()==prefix_len`（本例 19=19）。hidden **取最后一层** last-token，与 readout 层 \(\|\Delta\|\approx 5.54\) |
| X19c | scientific CLI repair | `k=1..5` 均 `refilled_prefix=true` / `status=ok`；`extra_prefill_tokens` 皆 **32**；slots 随 k 增长至 `{p1,p2,q}`。落盘 **无** `prefill_hidden` 字段 |
| X20 | `weight_seed` | 同 seed 同 ids → \(\|\Delta H\|=0\)；异 seed 同 ids → 0.194；同 seed 异 ids → 0.199。CLI collect **读取** `--weight-seed` 并写入 spec |
| X21 | 来源-数值 | `edits.jsonl` 含 `kind=source_value_pair`（两条件 + `targets=["q"]`）。`cmd_intervene` **不读** `edits.jsonl`，donor 不是该 pair |
| X22 | scientific 事件跨度 | 问句不再进入事件；`p1`/`p2` 不在 \(H\)。`q` 在生成区 45/49/51。hook 前缀 45 token 完整 |
| X23 | donor 行间距离 | 六行皆 `q`。`base` vs `t0p` 0.00778（被选中）；`base` vs value-edit 0.0043；`trace-edit` 与 `trace-edit:p2:2` **全等**（同一默认编辑被 `_allowed_edits` 再生成一次） |
| X24 | INLP 第三次 decode 的 donor | `donor @ P` 范数 \(3.6\times 10^{-17}\)（2 点 32 维 INLP 把 base/donor 都投影到约 0）。hook 仍是 `apply_swap`，`transform=pi_z_swap` |
| X25 | `ie_z` | `ie_z([1,3],[0,0])=2`：向量均值差，不是 \(\mathbb E[g(Y)]\)。落盘 `ie_z\approx 0.00227` |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验卡片 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON。属 `pending_server` |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision 缓存；CLI 未调用。属 `pending_server` |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹；本机 donor 是同题 seed0/seed1 的 `q` 步前，不是来源-数值条件 |
| 全量 pytest（作者称 144） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| D6-02 / D6-07 / A6-02 | 不可表达 `pre_step` 不入 \(H\)；scientific 只解析生成区；intervene 按有限且同 `node_id` 配对；几何 `timing=offline_hidden` | **独立关闭（指定路径）。** \(H\) 6×32 全有限；事件仅生成区 `q`；配对 `(0,1)` 同 `q` 跨轨迹；几何字段 `offline_hidden`；hook 三次（X8e、X14c、X22） |
| D6-03 / D6-08 / D6-09 | `source_value_pair` 写入 `edits.jsonl`；hook 元数据与 report 合并；collect 读 `--weight-seed` | **接线关闭。** pair 已落盘（X21）；`relative` 含 hook 字段（X14c）；spec `weight_seed=0`（X8e、X20）。intervene **仍不消费** pair（残留，见 D8-03） |
| D6-04 / D6-05 / D6-06 | INLP 进第二次 decode；有分数才写 `dev_weak_layer_decode`；hook 基用 StreamBank `basis_seed` | **作者原句独立成立；机制残留。** INLP 确有第三次 decode（X14c）；无分数不写弱层标签（X14d）；`basis_seed` 与 hook 基一致（X13）。INLP 仍是对 \(\approx 0\) donor 做 \(\Pi_Z\) swap，rescue 无 decode，`ie_z` 仍是向量差（D8-04） |
| A5-08 / F5-02 / D5-04 几何 timing / 主 hook 层 | 几何 `timing` 保持 `offline_hidden`；主 hook 用 readout | **关闭。** 主层 1；弱层只作第二次 decode（X14b/c） |
| A5-09 / F6-04 Prefill hidden | `refilled_prefix` 只认有限 `prefill_hidden`；prefix ids 或空 hidden 不得冒充 | **接口关闭。** dummy / `[]` / `prefix_token_ids` 均诚实失败（X19a）。CLI jsonl 仍不落盘该向量 |
| A4-13 `ChildProcessExecutor` | 不是 `IsolatedExecutor` | **仍关闭**（X18） |
| A5-14 Gate 未注册 | 非缺陷 | **同意。** 不记缺陷 |
| pending_server | 真实权重 / Linux cgroup / 实测 P1–P3 / 50 条 C2 | **同意未关。** tiny 随机权重不是 MODEL-01 |

相对 r06 已关闭、本轮不再单列缺陷：scientific \(H[0]/H[1]\) 全 NaN 导致 hook 零次；不可表达前提行进入 donor 槽；`make_source_value_pair` 返回值丢弃；hook 元数据被 `intervention_report` 覆盖；collect 写死 `weight_seed=0`；有分数却无第二次前向仍写 `dev_weak_layer`；hook 基用 `default_rng(1)`；`ids[:16]` 切掉 `q` 前缀（本机 45<64）；空事件末 token 回退。

## 6. 发现

### D8-01 — 声称冻结 hash 已复现（本轮非缺陷）

- **状态：** closed / non-defect
- **严重度：** n/a
- **文件 / 符号 / 行号：** `.planning/audits/round-08/VERSION.md` 声称与本机 60 文件 rel+NUL+bytes 一致
- **对应要求：** QA-01 可复现冻结
- **证据：** X1。
- **影响：** 审查对象可锚定到声称快照。不因此放行科学实现或 MODEL-01。

### D8-02 — 指定 scientific collect→intervene：有限 \(H\)、同 `node_id` 配对、\(\Pi_Z\) 已施加、几何 `offline_hidden`

- **状态：** closed（相对 D6-02 / D6-07）
- **严重度：** n/a（关闭项）
- **文件 / 符号 / 行号：** `collect.py` **50–52**（不可表达步前 `continue`）；`generate.py` **148–155**（只解析生成区并平移到全文）；`cli.py` **775–793、814–838、864**
- **触发条件：** `prepare --eval-mode scientific` → `collect --backend tiny` → `intervene --backend tiny`
- **对应要求：** CAUSAL-01 接线；POS-01；论文 §2.4 执行协议（本机接口）
- **证据：** X8e、X8h、X14c、X22。6 行 \(H\) 全有限且皆为 `q`；配对 `(0,1)` 跨 `trace-base`/`trace-t0p`；hook 前缀是 `text[:45]` 的 45 个 re-encode id，不是 `"follow donor"`；主变换 `pi_z_swap`，`hook_fired` 后 `status=prospective_decode`。几何字段保持 `offline_hidden`，不被改写成 `pre_step`。`H[0]` 等于前缀末 token 隐状态，且 \(\neq\) 末 token。
- **影响：** r06「指定路径 hook 零次」本机关闭。这是 tiny 接口证明，不是真实模型上的前瞻因果实验。

### D8-03 — `source_value_pair` 已落盘；donor 仍是同题 seed0/seed1，intervene 不读该 pair

- **状态：** residual（CAUSAL-02 使用侧） / closed（持久化）
- **严重度：** medium（协议） / 不升格为本轮指定路径回归
- **文件 / 符号 / 行号：** `cli.py` **380–389**（写入）；**796–817**（`_expressible_donor` 只看 `H`+`event_rows`，不看 `edits.jsonl`）
- **触发条件：** 任何声称 C2 / 来源跟随的 intervene
- **对应要求：** CAUSAL-02；论文 §2.4 donor 协议；GOAL §5.10；协议 §4
- **证据：** X21、X23。pair 含 `same_source_diff_value` 与 `same_value_diff_source`，`targets=["q"]`。选中的是生成噪声对（\(\|H_0-H_1\|\approx 0.00778\)），比 base vs value-edit（0.0043）更大；改名条件没有对应轨迹。真实 50 条保持 `pending_server`。
- **建议：** 按来源-数值条件各提一次 donor；intervene 读取并校验 pair。在此之前不要把 tiny 配对写成 C2 已做。

### D8-04 — INLP 有第三次 decode，但变换仍是 \(\Pi_Z\) swap；rescue 未进生成；`ie_z` 不是 \(\mathbb E[g(Y)]\)

- **状态：** residual / 作者原句「进入 decode」成立
- **严重度：** medium（机制）
- **文件 / 符号 / 行号：** `cli.py` **839–840、876–877**；`collect.py` `intervene_swap_decode` **177–180**（只 `apply_swap`）；`interventions.py` `ie_z` **88–89**
- **触发条件：** tiny/scientific `intervene`
- **对应要求：** CAUSAL-01；INLP-01；IE-01
- **证据：** X11、X14c、X24、X25。2 行拟合的 \(P\) 秩 30，把 donor 投影到 \(\approx 0\)，再对残差做 `apply_swap`（即 \(H' = H - \Pi_Z H\)），不是 \(H' = HP\)。rescue 只服务 `ie_z` 向量差。对照四项保持 null。
- **建议：** 同一事件步前分别把 \(P\) 与 `rescue_controls` 写入 resid；由生成文本算四项；`ie_z` 用预指定 \(g\)。

### D8-05 — 主 hook 固定 readout；有分数才第二次弱层 decode；C-layer 几何基 ≠ decode 基；C-rand 无 decode

- **状态：** closed（作者原句接线） / residual（对照协议）
- **严重度：** medium（对照）
- **文件 / 符号 / 行号：** `cli.py` **825–834、863–875**；`interventions.py` **46–49**
- **触发条件：** `--dev-layer-scores 0.05 0.9 0.8` 的 tiny intervene
- **对应要求：** 论文 §2.4；GOAL §5.11；IE-01
- **证据：** X12、X14c、X14d。弱层选择为 0；主 decode 层 1；无分数时 `dev_scores_missing` 且只有主+INLP 两次。C-layer decode 使用 **readout donor + 同一 `basis_seed`**，不采集弱层 \(H\)，也不使用 `rng(5+weak)` 的 QR 基（`clayer_basis_eq_main=false`）。三项范数锁成 0.000371（按 `main_norm` 缩放）。C-rand 没有 decode；`relative.target` 为 null。
- **影响：** 「弱层不是主干预」成立。「有分数才写 `dev_weak_layer_decode`」成立。同批次行为对照仍不完整。
- **建议：** C-layer 用该弱层 \(H\) 另跑同秩、同位置、同范数、同采样流的 decode；C-rand 对称地跑；未算对照结局时保持相对差为 null。

### D8-06 — thinking 抽取仍正确；模板 / `load_frozen` / `clone_cache` 仍未接入；tiny 不是 MODEL-01

- **状态：** residual defect（模板路径） / closed（`extract_answer`） / non-defect（tiny 边界）
- **严重度：** medium（模板；真实 HF 为 pending_server）
- **文件 / 符号 / 行号：** `events.py` **246–260**；`generate.py` **195–201、122–132**；`adapters.py` **10、18、32–42**
- **证据：** X15、X16。思考区数字不再当答案。CLI 与 `generate_task_trace` 均不调用 `apply_model_template`。tiny 随机权重按口径不算 MODEL-01 完成。
- **建议：** 卡片 revision 走 `apply_chat_template`。在此之前不要把 tiny 路径写成模板已对齐或 MODEL-01 已完成。

### D8-07 — Prefill 必须有有限 hidden（接口关闭）；hidden 取末层、jsonl 不落盘、`extra` 恒 32

- **状态：** closed（F6-04 / A5-09 接口） / residual（层选择与落盘）
- **严重度：** low（残留）
- **文件 / 符号 / 行号：** `repair.py` **101–119、147–180**；`cli.py` **944–951**
- **证据：** X19a–c。`prefix_token_ids` 与空 hidden 不得标已 Prefill。`execute_repair_tiny` 产出有限 hidden 且 KV 长度等于前缀。CLI 连续 k 的 `extra_prefill_tokens` 皆 32（`ids[:32]`）；向量不进 `RepairRecord`。
- **建议：** 需要复查层时改用 readout；若声称可审计 Prefill 表征，应落盘或显式声明仅接口旗标。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | 卡片 `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载，未读官方 tokenizer JSON |
| U-02 | `transform` 若原地修改 `tensor[:, -1:]` | hook 先 clone 再写入 patched；现调用是新张量 `apply_swap` 结果 |
| U-03 | `clone` 后 `get_seq_length` 是否覆盖 DynamicCache 全部分支 | 本机 5.5.3 对拍已够；未读完 transformers 每一分支 |
| U-04 | Prefill hidden 用最后一层而非 readout | 用户口令是「有 hidden」；层选择偏差记在 D8-07，不另开与 X19 同级高严重度项 |
| U-05 | re-encode 与生成 ids 在乱码段的 8 处不一致 | 作者明确把 re-encode 当作修复；tiny 字级词表下这是二次教师强制，本轮 X8h 显示步前与前缀前向一致 |
| U-06 | scientific 连续 k 的 `extra_prefill_tokens` 皆 32 | 更偏修复预算/截断 |
| U-07 | `trace-edit` 与 `p2:2` 额外编辑 \(H\) 全等 | 默认编辑与 `_allowed_edits` 撞车；tiny 几何本就接近，不单独升格为因果缺陷 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 revision + tiny 架构 | 无权重/tokenizer 缓存；CLI 未调用加载器。tiny 随机权重 **不是** MODEL-01 完成 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone 对拍符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 向量公式与 fixture/scientific 步前 \(\Pi_Z\) decode | 无来源-数值 donor 队列，无四项对照实测结局 |

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
| N-11 | 关闭（过程） | 冻结 hash 按 VERSION 脚本复现（HASH_MATCH，60 文件） |
| N-12 | 非缺陷 | `--backend offline` 的 `H` 是前缀 id 且标注 `offline_prefix_ids`；scientific 拒绝把它当隐状态 |
| N-13 | 非缺陷（边界） | 默认 tiny \(H\) 是随机初始化隐状态并标注 `random_init`。这是本机接口证明，**不是** MODEL-01 完成 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是 `IsolatedExecutor`；默认不宿主 exec |
| N-15 | 关闭（标签） | 默认 `clayer_status=dev_scores_missing`；有分数且完成弱层 decode 才写 `dev_weak_layer_decode` |
| N-16 | 关闭（有事件且可表达） | fixture 与 scientific `q` 三位置是读出层隐状态，且 ≠ 末 token |
| N-17 | 关闭（算法 + 接线） | tiny hook 变换是 \(\Pi_Z\)；scientific/fixture 前缀是 `text[:event.start]` |
| N-18 | 关闭（接口） | `execute_repair_tiny` 重新 Prefill（含 hidden 与 KV）再 decode；无 hidden 诚实失败 |
| N-19 | 非缺陷 | Gate 未注册与 `scientific_conclusion=None` 不记缺陷 |
| N-20 | 关闭（本轮指定猎项） | 有限 \(H\)；同 `node_id` donor；几何 `offline_hidden`；`source_value_pair` 落盘；`basis_seed` 驱动 hook 基；C-layer 第二次 decode；Prefill 需要 hidden |
| N-21 | 关闭（库层） | 空事件不再写成 last-token `pre_step`；scientific collect 拒绝无事件 / offline 前缀 |
| N-22 | 非缺陷 | 约束 `\nq = <digit>` 是本机可解析接口，不是自然 CoT；`parse_status=constrained_target` 诚实 |
| S-01 | stub | `clone_cache` 功能正确但未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `load_frozen` / `assert_no_future_leak` / `forbid_host_exec` 无生产调用方 |
| S-03 | stub | `rescue_controls` 有 CLI numpy 调用，不进入 hook；INLP 进 decode 但仍是 swap |
| S-04 | stub | Linux cgroup 执行器未到；本机子进程仅为普通进程后端 |

## 10. 通道结论

**D 通道通过（PASS）。冻结：HASH_MATCH。**

相对 round-06，作者就本通道声称的关闭项在本机**独立成立**，指定 scientific `prepare`→`collect tiny`→`intervene tiny` 不再因 NaN donor 跳过：（1）\(H\) 只含可表达步前，6 行全有限、皆 `q`、按同 `node_id` 跨轨迹配对，hook 前缀是事件步前文本；（2）几何 `timing` 保持 **`offline_hidden`**，主 `resid_post` 在 readout 层 1；（3）`source_value_pair` 写入 `edits.jsonl`，collect 读取 `--weight-seed`，hook 元数据并入 `relative`；（4）hook 基来自 StreamBank `direction` 的 `basis_seed`，与 CLI 几何基一致；（5）仅当提供 `--dev-layer-scores` 时才对弱层另跑 decode 并写 `dev_weak_layer_decode`；（6）Prefill 必须有有限 hidden，prefix ids / 空 hidden 不得冒充。另：\(\Pi_Z\) 公式、once hook、KV 范围、空事件 `no_event`、scientific 拒绝 offline 前缀、`ChildProcessExecutor` 未冒称隔离、Gate 未注册——均保持。微型随机权重按口径**不是** MODEL-01 完成。

残留不得写成 CAUSAL-01/02 已验收：intervene 不消费来源-数值 pair，donor 是同题 T0/T0′；INLP/rescue 不是残差消融/救援；C-rand 无 decode，相对对照为 null；C-layer decode 不用弱层 \(H\) 也不用报告用的 QR 基；模板路径未接入。这些保持 residual / `pending_server`，不推翻本轮指定猎项与接线关闭。
