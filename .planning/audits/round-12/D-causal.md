# D-causal 独立审查报告（round-12）

通道 D：模型与因果（token/prefix、thinking 模板、sampling、hook/KV、donor 来源、swap/消融/救援、两类对照、nontarget/invalid）。指定独立复跑 scientific `prepare`→`collect --backend tiny`→`intervene --backend tiny`→`repair --backend tiny`，夹具 `tests/fixtures/t1_tiny.json`，`--eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15`。猎项：`parse_region=generated` 且事件 `start ≥` 问句；有限 \(H\)、不可表达 `start=0` 跳过；donor 来自 `source_value_pair` 的 `trace-base`/`trace-edit`（非全 NaN、非恒等 \(H\)）；INLP 为 \(h@P\) 不是 \(\Pi_Z\)；C-rand `add_delta`；rescue `replace`；`ie_z` 来自 target-follow \(g(Y)\)；有 `--dev-layer-scores` 时 C-layer 弱层 `add_delta`；几何 `timing` 保持 `offline_hidden`（不得写成 tiny 上的 live `pre_step` hook）；Prefill 接受真实 32-d hidden，拒绝 `0`/`True`/`1.0`/`[0]`/`[]`；教师强制 `q` 诚实标 `constrained_target`。tiny **不是** MODEL-01；约束 `\nq = <digit>` **不是** §4.1 自然 CoT。

独立性声明：未阅读 round-12 其他通道报告（交卷时该目录除 `VERSION.md` 外本通道只写本文件）；只把 `.planning/audits/round-12/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账。对照读了本通道 round-10 报告仅作版式，结论以本机磁盘与本轮复跑为准。未修改 `src/`、`tests/` 或 `pyproject.toml`。不把测试绿当作论文正确；不把作者 `local close` 或 `156 passed` 当作本通道关闭。微型随机权重是本地接口证明，**不是** MODEL-01。Gate 未注册与 `scientific_conclusion=None` 不记缺陷。

对照原文：论文 §2.4（交换公式、C-rand/C-layer 同批次）、§4.1（自然 CoT，本机不得冒称）、§4.2（三位置）、§8（交换/消融/救援）；GOAL CAUSAL-01/02、INLP-01、IE-01、POS-01、MODEL-01、REPAIR-01、EXEC-01；`docs/EXPERIMENT_PROTOCOL.md` §4。

**先行结论：** 开审按 `VERSION.md` 原文复算，冻结 **HASH_MATCH** `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（61 文件，0 CRLF）。指定 scientific 路径点名项本机全部成立：生成区事件、有限 \(H\)、`trace-base`/`trace-edit` donor、INLP \(h@P\)、C-rand/rescue/C-layer 接线、几何 `offline_hidden`、Prefill 接受/拒绝、`constrained_target` 诚实。交卷再算同一脚本为 **HASH_MISMATCH** `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`（仍 61 文件，0 CRLF）。窗口内他方改写了 `splits.py` 与 `tests/test_round07_regressions.py`（mtime 02:32，开审后）；本通道未改冻结集。§1 所列因果生产文件开审后 mtime 未动，中检 SHA-256 前 16 = 交卷同一值。本机全量 pytest **156 passed**，与作者声称同数，但树已漂，**不得**绑到声明冻结 `598e6c8f…`。tiny 不是 MODEL-01，不得写 §4.1。

**总裁决：PASS（科学点名项）。开审 HASH_MATCH。交卷 HASH_MISMATCH。不得用本报告启动连续通过计数。不宣布 Goal 完成。**

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 声称冻结 hash | `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（`.planning/audits/round-12/VERSION.md`；61 文件；POSIX relpath + NUL + bytes） |
| 开审复算 | **HASH_MATCH。** 脚本逐字：`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` → **61 文件** → `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4` |
| 交卷复算 | **HASH_MISMATCH。** 同脚本 → 61 文件 → `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b`。0 CRLF。并发写盘（见 D12-00），本通道未改冻结集。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；`src/`/`tests/`/`pyproject.toml` 为未跟踪。HEAD 不是冻结） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载；无 CUDA |
| 作者 pytest 声称 | 156 passed。本机交卷全量 **156 passed / 33.54s / exit 0**。数字对得上当前漂移树，不记为声明冻结 `598e6c8f…` 的验收。因果相关 7 个文件 **64 passed / 22.75s** |
| 明确未读 | `.planning/audits/round-12/{A,B,C,E,F}-*.md`（开审时目录中不存在这些文件） |

因果生产文件（中检 SHA-256 前 16 = 交卷同一值）：`cli.py` `175abf12f4c207c5`（1254 行）、`collect.py` `83658cd8ba879f20`（261）、`generate.py` `07493570c6410e6b`（201）、`interventions.py` `0ffdbb8805be7649`（115）、`repair.py` `f76ff9998b9a6b17`（232）、`tiny.py` `21725a183452bd06`（120）、`features.py` `0a9f0b8beb0185ae`（39）、`adapters.py` `c1992624026a1bf0`（42）、`tokenize.py` `b0cc8974af1010fa`（31）、`edits.py` `cacb63ac27cbcccf`（287）、`events.py` `290a4fd676ac0814`（274）、`executor.py` `481d6ed597c93e78`（109）、`rng.py` `2098c2c72a852eaa`（53）。科学复跑在开审 MATCH 之后、聚合已漂时执行；上述字节交卷未变。

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明 |
| `src/reasoning_diff/models/adapters.py` | 1–42 | `MODELS` / `card` / 卡片 `think_ids` / `load_frozen(..., local_files_only=True)`。无独立 `think_ids()` |
| `src/reasoning_diff/models/tokenize.py` | 1–31 | `encode_text` / `decode_ids`（**非互逆**）/ `readout_layer_index`（60%–75%）/ `span_token_indices` |
| `src/reasoning_diff/models/collect.py` | 1–261 | `collect_hidden_trace` 不可表达步前 **continue**；`intervene_hidden_decode` 四 mode：`pi_z_swap` / `inlp`（`vec @ proj`）/ `add_delta` / `replace` |
| `src/reasoning_diff/models/features.py` | 1–39 | `select_prefix_index`；`leaks_target=bool(straddling)` |
| `src/reasoning_diff/models/generate.py` | 1–201 | `sample_next`；`decode_loop`（独立 `torch.Generator`）；`append_target_assignment`；`generate_task_trace` 只解析生成区；`apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–120 | `tiny_config` / `build_tiny` / `resid_post_hook(once=)` / `clone_cache` |
| `src/reasoning_diff/interventions.py` | 1–115 | swap / C-rand/C-layer / `inlp_remove` / `rescue_controls` / `select_weak_layer` / `ie_z`（helper 仍是均值差）/ `intervention_report` |
| `src/reasoning_diff/repair.py` | 1–232 | `_hidden_is_prefill`；`execute_repair_tiny`；`run_repair` |
| `src/reasoning_diff/cli.py` | 257–438、440–547、674–687、808–864、867–1010、1013–1056 | prepare/collect/pair/donor/intervene/repair |
| `src/reasoning_diff/executor.py` | 1–109 | `ChildProcessExecutor.isolated_sandbox=False`；默认 Unavailable |
| `src/reasoning_diff/rng.py` | 41–53 | StreamBank `sample/direction/perturb/bootstrap/split` |
| `src/reasoning_diff/edits.py` | 214–244 | `make_source_value_pair` / `apply_source_value_edit` |
| `src/reasoning_diff/events.py` | 74–88、251–274 | `parse_events`；`boundary_index`；`extract_answer` think/boxed |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理 |
| `tests/test_tiny_cache.py` | 1–26 | cache 隔离冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |
| `tests/test_round04_regressions.py` | 1–311 | readout；Prefill；source_value_pair 形状 |
| `tests/test_round05_regressions.py` | 1–197 | scientific 事件；几何 ≠ `pre_step` |
| `tests/test_round06_regressions.py` | 1–145 | 字段名锁 `donor_kind`/`inlp_transform`/`ie_z_g`；**不**比 \(h@P\) 数值 |
| `tests/test_round07_regressions.py` | 61–71 | 标量/`[0]`/`[]` Prefill 拒（该文件在审查窗口被他方改写，不引用为声明冻结证据） |

支持性：`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01 / REPAIR-01。未逐行审计：`analysis.py`、`probes/bilinear.py`、`transfer.py`（非本通道猎项）。`splits.py` 仅确认 prepare 写划分角色，不纳入本通道通过项。

未覆盖且不得默认通过：真实权重、CUDA/长链 KV、官方 tokenizer JSON、50 条来源解耦 C2。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | VERSION 脚本逐字复算 | **开审 HASH_MATCH** `598e6c8f…4f6bd4`，61 文件，0 CRLF。**交卷 HASH_MISMATCH** `0816fa5b…f293de3b` |
| X2 | 因果相关 pytest 7 文件 | **64 passed / 22.75s**。绿只锁冒烟与字段名 |
| X2b | 交卷全量 pytest | **156 passed / 33.54s** = 作者声称。跑在漂移树上，不绑声明冻结 |
| X3 | `apply_swap` 标准正交基 | \(H_b=[1,0],H_d=[0,1],Z=e_2\) → \(H'=[1,1]\) |
| X4 | resid_post 层 1 后 KV（`+1` 探针） | 层 0/1 \(\Delta K=\Delta V=0\)；层 2 \(\Delta K_{\max}=0.172\)、\(\Delta V_{\max}=0.392\)，seq=5 |
| X6 | decode hook 次数 | `once=False` **3**；`once=True` **1**（`max_new=3`） |
| X7 | hook `finally` | `RuntimeError` 后各层 `_forward_hooks` 为空（leftover=0） |
| X8e | **指定** scientific prepare→collect `--backend tiny` | 6 条 `tiny-qwen2`；每条 1 个生成区 `q`；`parse_region=generated`；`parse_status=constrained_target`；`H`/`H_pre_*` 皆 `(6,32)` **全有限、0 行 NaN**；`event_rows` 6 行皆 `node_id=q`；`hidden_layer=1`；`weight_source=random_init` |
| X8f | scientific collect `--backend offline` | `ValueError: scientific collect refuses offline_prefix_ids as H` |
| X8g | re-encode vs 生成 ids | 每条 **8** 处不同（恰 `max_new=8`）。collect \(H\) 是表面文本二次前向 |
| X8h | 步前 vs 前缀前向 | `H[0]` 与 `encode_text(text[:45])` 末 token **逐位相等**（\(\Delta=0\)）；\(\|H[0]-\mathrm{last}\|\approx 0.147\) |
| X8i | 三位置 | 行 0 \(\\|\Delta\\|\) pre–value / pre–post / value–post \(\approx 0.156/0.147/0.158\)；`H is H_pre_step` |
| X9 | `leaks_target` | `[[0,10]]` limit=5 → True 且 `token_index=None` |
| X10 | `boundary_index(..., 0, "before")` | **None**（不可表达） |
| X11 | INLP 数学 vs \(\Pi_Z\) | 2 点拟合 `inlp_rank=30`。随机 \(h\)：\(\max\|h@P-\mathrm{swap}\|=0.780\)。hook 间谍：`out == in @ P`，`out ≠ swap`（\(\max\|diff\|=0.898\)） |
| X12 | 弱层 / 范数 | `select_weak_layer({0:0.05,1:0.9,2:0.8})=0`。缺范数 `c_rand_delta` → `ValueError`。三项范数锁成 \(2.4186946959171496\times 10^{-4}\)，与落盘逐位相等 |
| X13 | StreamBank | `direction` 第一抽 113750710；第二抽 **1153799966**（`basis_seed`）。`sample` 第一抽 1191642646。`perturb` 17172908 |
| X14c | **指定** collect→intervene + `--dev-layer-scores 0.05 0.9 0.8` | donor **`(0, 2)`** = `trace-base` / `trace-edit`，`donor_kind=same_source_diff_value`，\(\|H_0-H_2\|\approx 0.00430\)（非 0、非 NaN）。`status=prospective_decode`。几何 **`timing=offline_hidden`**。`hook_timing=pre_step` 仅在 `relative` 内，**未**覆盖几何字段。`transform=pi_z_swap`；`inlp_transform=inlp`；`crand_transform=add_delta`；`rescue_transform=replace`；`clayer_transform=add_delta`；`weak_layer=0`；`clayer_status=dev_weak_layer_decode`。`ie_z=0.0`，`ie_z_g=target_follow`。`prefix_truncated=false`。主/对照/救援结局皆 `answer=9`，四项 0；相对差 vs 两对照皆 0。`followed_donor=false` |
| X14d | 无 `--dev-layer-scores` | `clayer_status=dev_scores_missing`；`clayer_transform` 缺；`clayer_outcomes` 四项 **null**；相对 `target` **null**。几何仍 `offline_hidden`。C-rand/INLP/rescue 仍 decode |
| X15 | thinking / 模板 | 未闭合 think → None；闭合 think 后数字 → 3；boxed → 7。`apply_model_template`：定义 1 处，**CLI 与 `generate_task_trace` 无调用**。`load_frozen` / `clone_cache`：CLI 无引用 |
| X16 | `clone_cache` | 生产路径不调用 |
| X17 | 读出层 | 3 层 → `readout_layer_index=1`。collect `hidden_layer=1` |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`ChildProcessExecutor` **不是** `IsolatedExecutor` 子类，`isolated_sandbox=False` |
| X19a | Prefill 接受/拒绝 | `execute_repair_tiny` 返回 **32** 维有限非零（\(\\|h\\|\approx 5.65\)）。`run_repair` 接受该向量 → `refilled_prefix=True`/`ok`。`0` / `True` / `1.0` / `[0]` / `[0.0]` / `[]` / `None` / 仅 `prefix_token_ids` → `prefill_unavailable` |
| X19c | scientific CLI repair | k=1..5 均 `refilled_prefix=true` / `status=ok`；`extra_prefill_tokens` 皆 **32**；jsonl **无** `prefill_hidden` 字段 |
| X21 | `source_value_pair` 落盘 | `trace_ids.base=trace-base`，`same_source_diff_value=trace-edit`，`same_value_diff_source=trace-source`；`targets=["q"]`，`nontargets=["p1"]`。intervene **读取** pair 并选 (0,2) |
| X22 | 生成区事件 | 6 条轨迹事件仅 `q`；`start` 45 或 53；问句长 36 或 44；**0** 条生成区 `p1`/`p2`。对问句跑 `parse_events` 打出 p1@0、p2@8，但 generate **不解析问句** |
| X23 | \(H\) 行距 | base–edit 0.00430；base–t0p 0.00778（**未被选**）；base–source 0.00832；`trace-edit` 与 `p2:2` 额外编辑 **全等**（同一默认编辑） |
| X24 | INLP hook 不是 swap | 间谍 `eq_inP=True`，`eq_swap=False`。CLI `mode="inlp"`。2 点拟合 `inlp_rank=30` |
| X25 | `ie_z` | 落盘 `0.0`（主/基线答案皆 ≠ donor `82`）。helper `ie_z(rescued, base)\approx 0.00237` **不等于**落盘值。CLI 用 \(g_{\mathrm{int}}-g_{\mathrm{base}}\)，`ie_z_g=target_follow` |
| X26 | 教师强制 | `target_assignment='\nq = 82'`（t0p 为 53）；`parse_status=constrained_target`；`correct=false`（金标 0）。intervene decode **不再**教师强制，经 `decode_ids`+`extract_answer` 得 `"9"` |
| X27 | 采样 | 6 条轨迹 `sampling={temperature:1.0,top_k:0,top_p:1.0}`。`decode_loop` 用独立 `Generator`，不用 `HF generate` |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验卡片 `think_ids` 与 chat template | 禁止下载；无官方 tokenizer JSON。`pending_server` |
| `load_frozen` 实际读盘 | `local_files_only=True`；本机无该 revision；CLI 未调用。`pending_server` |
| CUDA / 多 GPU / 长链 KV | 本机 CPU tiny。`pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹。本机 donor 是 fixture 上 `p2:0→2` 的步前 \(H\)，不是论文队列 |
| 把 156 passed 写成声明冻结验收 | 交卷树已漂；作者声称对应当前漂移树，不是 `598e6c8f…` |

## 5. ISSUES 台账处置（作者标本地关闭 / pending_server）

`ISSUES.md` 只当作者主张。

| 台账项 | 作者摘要 | 本通道裁定 |
|---|---|---|
| 先前生成区事件、有限步前 \(H\)、donor 身份、INLP/C-rand/rescue、`ie_z` | 须在 `598e6c8f…` 上重核 | **独立关闭（指定路径；D 生产字节与开审 MATCH 树相同）。** X8e、X14c、X22、X24、X25 |
| F6-04 / 标量 Prefill | `_hidden_is_prefill` 拒标量/`[0]`/空 | **独立关闭。** X19a |
| A5-08 几何 timing | 保持 `offline_hidden` | **关闭。** 顶栏 `timing=offline_hidden`；`hook_timing=pre_step` 不覆盖几何（X14c） |
| pending_server | 真实权重 / 50 条 C2 / 官方 CoT | **同意未关。** 约束 `q` 不是 §4.1；tiny 不是 MODEL-01 |
| C6-M-01 / B9-01 / 假 P1 / PCA / Plus family | 他通道 | **本通道不裁定** |

## 6. 发现

### D12-00 — 开审冻结可锚定；交卷聚合已漂（元数据，非因果回归）

- **状态：** residual（冻结绑定） / non-defect（因果实现）
- **严重度：** process（连续通过计数）
- **文件 / 符号 / 行号：** `.planning/audits/round-12/VERSION.md` 声称 `598e6c8f…`；交卷脚本输出 `0816fa5b…`。窗口内 `src/reasoning_diff/splits.py`、`tests/test_round07_regressions.py` mtime 02:32（开审后）
- **对应要求：** QA-01
- **证据：** X1、X2b。本通道未改 `src/`/`tests/`/`pyproject.toml`。§1 所列因果生产哈希中检=交卷；这些文件 mtime 均早于开审。全量 pytest 156 跑在漂移树上。
- **影响：** 科学点名项仍按未变因果字节成立。**不能**把交卷磁盘写成声明冻结已通过，**不能**开始连续通过。
- **建议：** 停写冻结集后再冻一轮；各通道绑同一聚合。

### D12-01 — 声称冻结 hash 开审已复现

- **状态：** closed / non-defect（开审）
- **严重度：** n/a
- **证据：** X1 开审。不因此放行 MODEL-01 或真实 C2。

### D12-02 — 只解析生成区；事件 `start ≥` 问句；问句 p1/p2 不是生成事件

- **状态：** closed
- **文件 / 符号 / 行号：** `generate.py` **148–155、157–158、190**（`parse_events(generated)` 再 `+= len(prompt)`；`parse_region="generated"`；赋值落在 `gen_text` 之后则 `constrained_target`）
- **触发条件：** scientific prepare
- **对应要求：** POS-01；协议「目标首 token 之前」的事件定位
- **证据：** X22、X26。6 条轨迹事件节点皆 `q`，`start` 45 或 53，问句 36 或 44 字符。生成区 p1/p2 = 0。问句单独解析会出 p1/p2，说明排除靠「不解析问句」，不是问句里没有赋值。
- **影响：** 指定路径不再把 prompt 前提写进 \(H\) 行。

### D12-03 — \(H\) 全有限；不可表达 `start=0` 跳过；无 NaN pre_step 行

- **状态：** closed
- **文件 / 符号 / 行号：** `collect.py` **50–52、66–68**；`events.py` **251–257**
- **证据：** X8e、X10。科学 collect `H` 6×32，NaN 行 0；`H_pre_step/value/post` NaN 行 0。手工 `Event(start=0)` → `h_position=no_event`，`H.shape=(0,32)`，**不**塌成末 token。`boundary_index(...,0,"before")` 为 None。
- **影响：** 「全 NaN donor / 不可表达行入槽」本机关闭。

### D12-04 — donor 来自 `source_value_pair` 的 `trace-base` / `trace-edit`，非全 NaN、非恒等 \(H\)

- **状态：** closed（点名配对） / residual（`same_value_diff_source` 未作第二 donor）
- **文件 / 符号 / 行号：** `cli.py` **384–397**（落盘 `trace_ids`）；**811–841**（`_load_source_value_pair` + `_pair_source_value`）；**844–847**（pair 优先于 t0p/finite fallback）
- **对应要求：** CAUSAL-02 接线；协议 §4 donor
- **证据：** X14c、X21、X23。pair 元数据 `base→trace-base`、`same_source_diff_value→trace-edit`。选中行 `(0,2)`，\(\\|H_0-H_2\\|\approx 0.00430\)，`allclose=False`，两行有限。更大的 base–t0p 距离 0.00778 **未被选**（不再是「同题 seed0/seed1」）。`trace-source` 已生成（\(\\|H_0-H_3\\|\approx 0.00832\)）但配对函数只吃 `same_source_diff_value`。`trace-edit` 与 `_allowed_edits` 的 `p2:2` \(H\) 全等，是默认编辑撞车，不是本对 donor 恒等。
- **建议：** 若声称来源跟随，另用 `trace-source` 提一次 donor。在此之前不要写「两种条件都做了交换」。真实 50 条仍 `pending_server`。

### D12-05 — INLP 是 \(h@P\)；C-rand `add_delta`；rescue `replace`；`ie_z` 为 target-follow \(g(Y)\)；有分数则弱层 `add_delta`

- **状态：** closed（点名接线） / residual（弱层 \(H\) 未采集；helper `ie_z` 仍是向量差；结局通道不是教师强制 \(q\)）
- **文件 / 符号 / 行号：** `collect.py` **189–208**；`cli.py` **912–983、960–967**；`interventions.py` **52–67、88–89**
- **对应要求：** CAUSAL-01；INLP-01；IE-01
- **证据：** X11、X12、X14c、X14d、X24、X25。hook 间谍 `out = in @ P` 且 \(\neq \Pi_Z\) swap。独立重算三项范数与落盘逐位相等（\(2.4186946959171496\times 10^{-4}\)）。CLI：主 `pi_z_swap`；INLP `mode=inlp`；C-rand `add_delta(cr["delta"])`；rescue `replace(rescued["matched"])`；有分数时层 **0** `add_delta(cl["delta"])` 并写 `dev_weak_layer_decode`；无分数不写弱层 decode，相对四项 null。落盘 `ie_z=0.0` ≠ helper 0.00237；`ie_z_g=target_follow`。\(g=1\) 当 `extract_answer(generated)==donor_ans`。本机 donor_ans=82、主/基线皆非 82。
- **残留：** C-layer 的 \(\Delta\) 仍用 **readout 层** 的 base/donor（collect 层 1），只是施加在弱层 0，不是弱层隐状态另采。`ie_z()` 库函数仍是均值差，仅 CLI tiny 路径改 \(g(Y)\)。intervene 的 generated 是无约束 4 token，不是被强制的 `\nq =`。
- **建议：** 需要弱层对照时另采该层 \(H\) 再算 \(\Delta\)。需要与 prepare 同一通道比结局时，对 intervene 也走 `append_target_assignment` 或显式声明「只比无约束 decode」。

### D12-06 — 几何 `timing` 保持 `offline_hidden`，未写成 live `pre_step`

- **状态：** closed
- **文件 / 符号 / 行号：** `cli.py` **914、1006**；`collect.py` **227**（hook 内部 `timing`）
- **证据：** X14c、X14d、X8h。jsonl 顶栏 `timing=offline_hidden`。`relative.hook_timing=pre_step` 仅表示 `event_aligned=True` 时 hook 打在事件步前前缀上，前缀是 `text[:45]` 的 **re-encode**，不是原生成 KV 续写。collect \(H\) 与前缀末 token 一致，与生成 ids 有 8 处不同（X8g）。
- **影响：** 不得把 tiny 路径写成「已做 live 步前 hook」。本机接口是离线隐状态几何 + 二次前向 hook。

### D12-07 — Prefill：真实 32-d tiny hidden 接受；`0`/`True`/`1.0`/`[0]`/`[]` 拒绝

- **状态：** closed（接口） / residual（`extra=32` 与不落盘向量）
- **文件 / 符号 / 行号：** `repair.py` **14–23、159–173**
- **证据：** X19a、X19c。`_hidden_is_prefill` 拒 0 维/size&lt;2/非有限/零范数/bool/str。CLI 五条 `refilled_prefix=true`。`extra_prefill_tokens` 恒 32（`ids[:32]`）；`RepairRecord` 无 hidden 字段。
- **建议：** 若声称可审计 Prefill 表征，落盘或声明仅旗标。

### D12-08 — 教师强制 `q` 诚实为 `constrained_target`；不得写 MODEL-01 / §4.1

- **状态：** closed（诚实标签） / non-defect（tiny 边界） / residual（模板未接入）
- **文件 / 符号 / 行号：** `generate.py` **72–98、157–158、195–201**；`adapters.py` **32–42**
- **证据：** X15、X26、X27。`append_target_assignment` 写 `\nq = ` 再从 logits 采两位数字，注释写明 Not gold values。6 条 `parse_status=constrained_target`，`correct=false`。金标 0，写出 82/53。`apply_model_template` 不被 CLI/`generate_task_trace` 调用。卡片 `think_ids` 只在未调用的 `load_frozen` 路径。产物与代码中 **无** MODEL-01 声称。
- **影响：** 本机可解析接口成立。把这条轨迹写成自然 CoT、官方模板对齐或 MODEL-01 **是缺陷**；当前代码与元数据没有那样写。

### D12-09 — nontarget/invalid 字段已接线；本机取值不能当机制结果

- **状态：** closed（schema / 相对对照） / residual（通道与 identifiability）
- **文件 / 符号 / 行号：** `cli.py` **952–960、985**；`interventions.py` **98–115**
- **证据：** X14c、X14d、X26。有分数时四项相对 `vs_crand`/`vs_clayer` 均为 0.0（主与两对照答案都是 `"9"`）。无分数时相对四项 null（C-layer 未 decode）。`invalid=0` 因为垃圾 decode 仍能抽出数字。`nontarget` 定义为「答案=gold 且 ≠ donor」；本机 gold=donor=`82`（同一 `seed=0` 教师强制），该比特结构上不能为 1。
- **影响：** 不得把四项 0 写成「无目标跟随」的科学结论。`acknowledged_effect=relative_to_controls_only` 诚实。CAUSAL-02 实测结局保持 `pending_server`。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | 卡片 `think_ids` 与 STACK 表 | 禁止下载，未读官方 tokenizer JSON |
| U-02 | `transform` 原地改 `tensor[:, -1:]` | hook 先 clone 再写入；现调用给新张量 |
| U-03 | 无约束 4-token 下 INLP/swap/add/replace 产出同一 `answer=9` | 间谍已证变换数学不同；tiny + \(\\|\Delta\\|\\approx 2.4\\times 10^{-4}\) 不足以改采样。不升格为「INLP 仍是 swap」 |
| U-04 | Prefill hidden 取 `hidden_states[-1]` 而非 readout | 点名项是「有真实 hidden」；层选择保持 residual，不另开高严重度 |
| U-05 | re-encode 与生成 ids 8 处不一致 | 与 X8h 步前=前缀前向同时成立；已标 `offline_hidden` |
| U-06 | `extra_prefill_tokens` 恒 32 | 修复预算/截断，见 D12-07 |
| U-07 | `trace-edit` 与 `p2:2` \(H\) 全等 | 默认编辑与 `_allowed_edits` 撞车；选中 donor 不是这对称对 |
| U-08 | C-layer 把读出层 \(\Delta\) 加到弱层 residual | 猎项只要求弱层 `add_delta`；范数已对拍。层不一致属协议残留 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | `load_frozen` + 卡片 + tiny 架构 | 无权重缓存；CLI 未加载。tiny **不是** MODEL-01 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post / clone | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 本机 fixture 接线与四 mode decode | 无真实来源-数值队列；结局通道是无约束 decode |
| P-04 | §4.1 自然 CoT 事件 | `parse_events` + 教师强制接口 | 本机只有 `\nq = <digit>` |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta` 在一维标准正交基下正确 |
| N-02 | 非缺陷 | resid_post(层1) 不改层 0/1 当前 KV，改层 2；`finally` 含异常清理 |
| N-03 | 非缺陷 | `card()` 拒 `revision=="latest"`；`enable_thinking` 仅 `qwen3` |
| N-04 | 非缺陷 | `decode_loop` 保留 `prompt_ids` / `generated_ids` / `sampling`；独立 Generator |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配 main 范数 |
| N-07 | 关闭 | 跨界 token 不进 `token_index`；`leaks_target` 可为 True |
| N-08 | 关闭 | `extract_answer` 去闭合 think；未闭合 None |
| N-09 | 关闭 | `once=True` 在 decode 中只生效一次 |
| N-12 | 非缺陷 | scientific 拒绝 offline 前缀当 \(H\) |
| N-13 | 非缺陷（边界） | \(H\) 标 `random_init`。**不是** MODEL-01 |
| N-14 | 关闭 | `ChildProcessExecutor` 不是隔离执行器 |
| N-15 | 关闭 | 无分数 → `dev_scores_missing`；有分数且弱层 decode → `dev_weak_layer_decode` |
| N-16 | 关闭 | 三位置互异且 ≠ 末 token；步前 = 前缀末 token |
| N-19 | 非缺陷 | Gate 未注册与 `scientific_conclusion=None` |
| N-22 | 非缺陷 | `\nq = <digit>` 是本机可解析接口，不是自然 CoT |
| N-23 | 关闭（本轮点名） | 生成区事件；有限 \(H\)；pair donor (0,2)；INLP \(h@P\)；C-rand/rescue/C-layer mode；`ie_z` 为 \(g(Y)\)；几何 `offline_hidden`；Prefill 接受 32-d、拒标量/`[0]`/`[]` |
| S-01 | stub | `clone_cache` 功能在、未接入 decode/intervene |
| S-02 | stub | `apply_model_template` / `load_frozen` / `assert_no_future_leak` 无生产调用方 |
| S-03 | stub | 库函数 `ie_z` 仍是向量差；弱层 \(\Delta\) 仍用 readout \(H\) |
| S-04 | stub | Linux cgroup 执行器未到 |

相对先前已关闭、本轮不再当缺陷：INLP decode 仍走 `apply_swap`；donor 只吃 t0p；`ie_z` 只是隐均值；C-rand 无 decode；Prefill 接受 `0`/`[0]`。

## 10. 通道结论

**D 通道通过（PASS）。开审冻结：HASH_MATCH `598e6c8f…`。交卷冻结：HASH_MISMATCH `0816fa5b…`。**

指定 scientific `prepare`→`collect tiny`→`intervene tiny`→`repair tiny` 在未变的因果生产字节上独立复跑，点名项成立：

1. 事件只来自生成区，`start ≥` 问句，无 prompt p1/p2；`parse_status=constrained_target` 诚实。
2. \(H\) 6×32 全有限；`start=0` 不入矩阵。
3. donor 是 `source_value_pair` 的 `trace-base`/`trace-edit`（行 0/2），不是全 NaN，不是恒等 \(H\)，也不是 t0p。
4. INLP hook 为 \(h@P\)；C-rand `add_delta`；rescue `replace`；`ie_z` 为 target-follow \(g(Y)\)；有 `--dev-layer-scores` 时弱层 0 再跑 `add_delta`。
5. 几何 `timing=offline_hidden`，未被改写成 live `pre_step`。
6. 真实 32-d tiny hidden 可标 Prefill；`0`/`True`/`1.0`/`[0]`/`[]` 与裸 prefix ids 不可。

微型随机权重 **不是** MODEL-01。约束 `\nq = <digit>` **不是** §4.1。交卷 hash 已漂，**不能**开始连续通过，**不能**宣布 Goal。残留（第二 donor 未交换、弱层 \(H\) 未另采、结局通道无约束、Prefill 不落盘向量、模板未接入、真实 C2）保持 residual / `pending_server`，不推翻本轮点名接线。
