# D-causal 独立审查报告（round-02）

通道 D：模型与因果（三位置/前瞻泄漏/跨界、thinking 模板与原始 token ids、offline vs online 边界、resid_post last-token vs 全序列、hook 清理、KV/cache 隔离、swap \(H'=H_{\mathrm{base}}+\Pi_Z(H_{\mathrm{donor}}-H_{\mathrm{base}})\)、INLP/rescue、C-rand/C-layer 同队列与实际范数、CLI intervene/analyze 不得虚构正确率、隔离执行器）。

独立性声明：未阅读 round-02 其他通道报告；只把 `.planning/audits/round-02/VERSION.md` 与 `.planning/audits/ISSUES.md` 当作冻结声明/作者台账；未修改生产代码、测试或配置；不把测试通过当作实现正确。对照阅读了本通道 round-01 报告以便核对关闭项，结论以本机当前磁盘为准。

## 1. 元数据

| 字段 | 值 |
|---|---|
| 通道 / 任务标识 | Independent reviewer D / model-and-causal |
| 审查时间 | 2026-09-21T00:52:00+08:00 |
| 声称冻结 hash | `2676a0983f6b42148202eedfbfaea44ce207d1fd386b8d47cbc909e983c5cc38`（`.planning/audits/round-02/VERSION.md`；55 文件；POSIX relpath + bytes） |
| 独立复算 hash | **未能复现声称值。** 当前树 55 文件均为 LF。`src/reasoning_diff/**/*.py` 排序 + `tests/**/*.py` 排序 + `pyproject.toml` 的 rel+bytes = `632bc1e3773ffd3ffb024afa0fd944539e83836e71c3b24e8a353141f4917787`。另试 all-sorted、bytes-only、rel+NL/NUL、LF 归一、sha256sum 列表、per-file hex、git-blob、`io.digest(path→file_digest)`、rglob，**无一匹配**。审查对象是当前工作区字节，不以声称 hash 已对齐为前提。 |
| git HEAD | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（与 VERSION 一致；工作区脏；`src/` `tests/` `pyproject.toml` 均未跟踪） |
| 本机环境 | Python 3.11.7, torch 2.7.1+cpu, transformers 5.5.3, numpy 1.26.4；无下载 |

## 2. 范围与逐文件覆盖

指派阅读并逐行核对：

| 文件 | 行区间 | 符号 / 覆盖内容 |
|---|---|---|
| `src/reasoning_diff/models/__init__.py` | 1–1 | 包说明；无导出、无加载器 |
| `src/reasoning_diff/models/adapters.py` | 1–29 | `MODELS`, `card`；revision / `think_ids`；无 `from_pretrained` |
| `src/reasoning_diff/models/collect.py` | 1–47 | `collect_tiny`, `intervene_tiny` |
| `src/reasoning_diff/models/features.py` | 1–43 | `select_prefix_index`, `assert_no_future_leak` |
| `src/reasoning_diff/models/generate.py` | 1–56 | `sample_next`, `decode_loop`, `apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 1–92 | `tiny_config`, `build_tiny`, `resid_post_hook`, `clone_cache`, `decode_step` |
| `src/reasoning_diff/interventions.py` | 1–91 | `project_delta`, `apply_swap`, `c_rand_delta`, `c_layer_delta`, `inlp_remove`, `rescue`, `intervention_report` |
| `src/reasoning_diff/cli.py` | 1–419 | 重点 `cmd_collect` 199–226、`cmd_intervene` 297–335、`cmd_analyze` 347–371 |
| `src/reasoning_diff/executor.py` | 1–59 | `IsolatedExecutor` stub、`UnavailableExecutor`、`SpyExecutor`、`forbid_host_exec` |
| `tests/test_tiny_hooks.py` | 1–27 | 前向 + hook 清理（未断言 last-token-only） |
| `tests/test_tiny_cache.py` | 1–25 | `use_cache=False` 污染；tiny collect/intervene 冒烟 |
| `tests/test_generate_loop.py` | 1–17 | generator 重放与 greedy |

支持性阅读（边界/评分/协议，非本通道主交付）：`events.py` `boundary_index` 105–111、`extract_answer` 114–125；`analysis.py` `p3_recovery` 73–80；`rng.py` `StreamBank` 41–53；`schema.py` `POSITION_KINDS` 39；`scoring.py` `score_code` 19–30；`repair.py` 34–45；`baselines.py` 10–44；`probes/boundary.py` 7–23；`tests/test_science.py` 42–88；`tests/test_review_regressions.py` 230–265；`tests/test_cli_pipeline.py` 1–29；`tests/test_t3_t4.py` 29–35；`docs/EXPERIMENT_PROTOCOL.md` §4；`.planning/research/STACK.md` 54–90；`.planning/REQUIREMENTS.md` MODEL-01 / CAUSAL-01 / CAUSAL-02 / POS-01 / INLP-01 / IE-01。

未覆盖且不得默认通过：真实权重加载、CUDA/长链 KV、官方 tokenizer JSON、50 条 C2 同批次。未逐行审计：`analysis.py` 其余统计、`probes/bilinear.py`、`transfer.py`。

## 3. 已执行检查与结果

| ID | 检查 | 结果 |
|---|---|---|
| X1 | 声称冻结 hash 复算（18 种拼接） | 失败，见 U-01。当前树锚点 `632bc1e3…` |
| X2 | `pytest tests/test_tiny_hooks.py tests/test_tiny_cache.py tests/test_generate_loop.py tests/test_science.py::test_boundary_excludes_straddle tests/test_science.py::test_swap_formula tests/test_review_regressions.py::test_c03_inlp_iterates_on_projected_h tests/test_review_regressions.py::test_c04_crand_matches_provided_main_norm_not_rng1 tests/test_review_regressions.py::test_d01_three_positions_differ_and_leak_flag_is_real tests/test_cli_pipeline.py tests/test_t3_t4.py::test_humaneval_never_host_exec -q` | **12 passed / 9.91s**。通过只证明冒烟，不证明因果协议 |
| X3 | `apply_swap` 与 `test_swap_formula` | \(H'=H_b+\Pi_Z(H_d-H_b)\) 在标准正交基下正确：`[1,0]+Π([0,1]-[1,0])=[1,1]` |
| X4 | tiny qwen2：`resid_post` 层 1 后 KV 范围 | 层 0/1 \(\Delta K=0\)，层 2 \(\Delta K_{\max}=0.130\)；此前 token KV 保持。与 STACK resid_post 契约一致 |
| X5 | 仅 last-token vs 全序列 | 独立捕获 resid：early \(\Delta=0\)，last \(\Delta=1\)（`+1` 变换）。`transform` 收到形状 `[1,1,32]` |
| X6 | decode 期间 hook 触发次数 | `decode_loop(..., max_new=3)` 期间 hook **触发 3 次**（非一次性） |
| X7 | hook `finally` 清理 | 正常退出与 `RuntimeError` 后 `layer._forward_hooks` 均为 0 |
| X8 | `collect_tiny("qwen2",[1,2,3],max_new=2)` 三位置 | `token_index` pre/pre_value/post = **2/3/4**（limit 3/4/5）；`leaks_target` 皆 False；`boundary_source` 皆 `offline_annotation` |
| X9 | `leaks_target` 能否为 True | 18 组偏移（含单 token 跨界）**全部 False**。跨界时 `token_index is None` 且列入 `straddling_excluded` |
| X10 | `boundary_index("before")` vs `"end"` | 同一 limit 下结果相同（`position` 只做枚举校验） |
| X11 | `inlp_remove` steps=1 vs 8 | 最大差 **0.8**（不再幂等）。`H@P` 第一列≈0，与 `test_c03` 同向 |
| X12 | `c_rand_delta` / `c_layer_delta` 范数 | 要求 `target_norm`；`actual_norm` 与 main 逐位匹配（2.723…）。旧 `rng(1)` 伪 main 范数 0.6617 **不再相等** |
| X13 | `python` 调 `cli.main(['collect'…/'intervene'…/'analyze'…])` | intervene 写 `status=geometry_only`，四项结局 **null**，范数三者相等；**无** 0.6/0.55。analyze：`p1/p2/p3=null`，`scientific_conclusion=null`，`not_evaluated` |
| X14 | CLI collect 三位置 + NPZ | 首事件 `start=0` → `pre_step.token_index=None` / `expressible=false`；`features.npz` 为 `I_4` |
| X15 | thinking / 原始 ids / 引用检索 | `decode_loop` 保存 `prompt_ids`/`generated_ids`/`token_ids`。`apply_model_template`、`think_ids`、`clone_cache`、`assert_no_future_leak`、`StreamBank`、`collect_tiny`、`inlp_remove`、`rescue` **均未被 CLI 调用** |
| X16 | `clone_cache` / DynamicCache | 本机 `transformers.cache_utils.DynamicCache` **无 `.copy()`**（仅有 `crop`/`reorder_cache`）。`clone_cache` **返回原对象** |
| X17 | `extract_answer` 与 thinking | `"<think>the number is 99</think>"` → **99**；无 boxed/#### 时思考区数字可当答案 |
| X18 | 执行器 | 默认 `UnavailableExecutor`；`score_code` → `executor_unavailable` / `value=None`；基类 `submit` 为 `NotImplementedError`；全库无 host `exec`/`eval` 回退 |

## 4. 未执行检查与原因

| 检查 | 原因 |
|---|---|
| 官方 Qwen3/R1 tokenizer 上校验 `think_ids` 与 chat template | 禁止下载；工作区无对应 tokenizer JSON |
| CUDA / 多 GPU / 长链 KV 与 position_ids | 本机 CPU tiny；属 `pending_server` |
| 真实 50 条来源解耦 C2 同批次 | 无真实轨迹、无 donor 配对实现 |
| 全量 pytest（作者称 65） | 本通道只重跑 tiny/因果相关；不把未跑项记为通过 |

## 5. ISSUES 台账处置（作者标 `fixed_pending_review`）

| 台账 ID | 作者摘要 | 本通道裁定 |
|---|---|---|
| D-01 | 三位置坍缩；泄漏硬编码 | **部分关闭 / 残留。** 不同 limit 时索引可分离（X8、`test_d01`）。`leaks_target` 仍不可能为 True（D-08）。CLI 不采集隐状态（D-02） |
| D-02 | hook 打在整段序列 | **部分关闭 / 残留。** 当前前向的 last-token 被改、更早位置不变（X5）。不是全局 token 门控，也不是一次性（D-07） |
| D-03 | 虚构 intervene/analyze 效应 | **关闭虚构正确率。** CLI 写 null + `geometry_only` / `not_evaluated`（X13）。结局仍未测量（D-13） |
| C-03 | INLP 未投影 H | **算法关闭，接入残留。** 迭代投影成立（X11）；CLI/隐状态未调用（D-06） |
| C-04 | C-rand 用 rng(1) 伪 main | **范数匹配关闭。** 必须传入实际范数（X12）。C-layer 仍不是弱层（D-04） |

## 6. 发现

### D-01 — 声称冻结 hash 无法复现

- **状态：** confirmed defect（过程/冻结）
- **严重度：** medium
- **文件 / 符号 / 行号：** `.planning/audits/round-02/VERSION.md` 声称 `2676a098…`；本机 55 文件 rel+bytes `632bc1e3…`
- **触发条件：** 按 VERSION 所述「POSIX relpaths + file bytes」复算
- **对应要求：** QA-01 可复现冻结
- **证据：** 见 §3 X1。文件数与范围一致，拼接算法变体均不匹配。
- **影响：** 不能证明审查对象等于作者冻结快照。
- **建议：** 公布逐文件 digest 与精确拼接脚本；审查以当前磁盘为准。

### D-02 — 生产 collect 仍是合成轨迹 + 单位阵特征，不采集三位置隐状态

- **状态：** confirmed defect
- **严重度：** critical
- **文件 / 符号 / 行号：** `cli.py` `cmd_collect` **199–226**（尤其 **221** `dummy`/`H`/`E` = `np.eye(4)`）；`_synthetic_trace` **37–54**（一字一 token）；`collect.py` **11–25** 只算索引、不保存 resid；全库无 `from_pretrained`（`tiny.py` **1** 仅注释禁止）
- **触发条件：** `reasoning-diff collect`；或期望 MODEL-01 隐状态
- **对应要求：** MODEL-01；POS-01；STACK 配置/词表同一 revision
- **证据：** 本机 NPZ 为 \(I_4\)。CLI 不调用 `collect_tiny` / `decode_loop` / tokenizer。`collect_tiny` 的三位置是 `len(prompt_ids)` 的人为错开，不是事件 `start`/`value_start`/`end`。
- **影响：** 后续 fit/intervene 吃到的「H」不是模型表示。
- **建议：** 加载路径（tiny 或本地 fixture）必须按三位置取出 last-safe token 的 resid 并写入 NPZ；卡片 revision 接入 `from_pretrained`。

### D-03 — donor 不是事件可配对样本，无来源—数值解耦

- **状态：** confirmed defect
- **严重度：** critical
- **文件 / 符号 / 行号：** `cli.py` **303–310**（`H[0]`/`H[1]` 或 `rng.normal(size=8)`）；全库无 donor 配对、无按数值条件重提取、无可见前缀记录
- **触发条件：** 任何 `cmd_intervene`
- **对应要求：** 原文/协议 §4；CAUSAL-02
- **证据：** 接 collect 时 donor = \(e_2\)（单位阵第二行）。无同值异源 / 异值来源矩阵。
- **影响：** 即使把向量写入 hook，也不能评价「跟随 donor 来源」。
- **建议：** 先按事件身份配对；每个数值条件独立提取；记录层、token 位置与可见前缀。

### D-04 — C-layer 是同向量上的随机子空间，不是弱层干预

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `c_layer_delta` **46–49**；`cli.py` **316–317**（`orthonormal_basis(..., default_rng(5))`）。无开发集选层、无浅层 hook
- **触发条件：** 任何声称含 C-layer 的 intervene
- **对应要求：** 协议 §4「C-layer 为开发集证实依赖信息较弱的层」；IE-01
- **证据：** 与 C-rand 一样对同一 `base`/`donor` 做 \(\Pi\) 再 `scale_to_norm`。本机 `clayer_norm == main_norm`，但 `layer_basis` 与 C-rand 基不同，层号不存在。
- **影响：** 「相对 C-layer」只是第二种随机投影，缺必做层对照。同队列只做到「同一对 numpy 向量」，不是同批次生成。
- **建议：** 在 `dev` 上按探测曲线选弱层；与主干预同秩、同位置、同范数、同采样流执行；写入实际层号。

### D-05 — Rescue 仍是向量相加，无错误来源 / 随机分量对照

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `rescue` **70–71**；CLI 未调用
- **触发条件：** 调用 `rescue` 或宣称 Fig.3d
- **对应要求：** 协议 §4；CAUSAL-01
- **证据：** `return ablated + component`。独立运行 `rescue([1,0],[0,1]) -> [1,1]`。无错误来源、无随机救援、无恢复率。
- **影响：** 加回原分量可成恒等重建，不能单独作机制证据。
- **建议：** 同一位置比较匹配分量 / 错误来源 / 随机分量；超参在 direction_fit/dev 固定。

### D-06 — INLP 已迭代投影，但从未作用于隐状态，四项结局仍空

- **状态：** residual defect
- **严重度：** high
- **文件 / 符号 / 行号：** `interventions.py` `inlp_remove` **52–67**（现对 `work` 逐步 `work @ (I-uu^T)`）；`cli.py` **297–335** 未调用；`intervention_report` **74–91** 未被 CLI 使用
- **触发条件：** 期望选择性消融 / P3 Knock-out
- **对应要求：** INLP-01；CAUSAL-01
- **证据：** steps=1 vs 8 差 0.8；`test_c03` 通过。生产路径无 `P@h`、无生成、无四项结局。
- **影响：** 算法名副其实，实验仍不存在。
- **建议：** CLI 对选定位置隐状态执行；报告目标/非目标/任务正确/无效。

### D-07 — hook 只改当前前向 last-token，无全局位置门控，非一次性

- **状态：** confirmed defect
- **严重度：** high
- **文件 / 符号 / 行号：** `tiny.py` `resid_post_hook` **59–69**（`patched[:, -1:] = transform(tensor[:, -1:])`）；`collect.py` `intervene_tiny` **36–40**（`t+0.01`，整段 prefill 的末 token）；未与 `decode_loop` 组合成「边界步一次」
- **触发条件：** 在 decode 循环外层保持 hook；或 `intervene_tiny`
- **对应要求：** 协议 §4 选定位置、目标首 token 之前；STACK 70–71「hook 必须一次生效，后续 decode 不得重复施加」
- **证据：** X5 证明不是全序列平移（相对 round-01 进步）。X6：`max_new=3` 触发 3 次。`intervene_tiny` 打在 prompt 最后一枚，不是 `pre_step` 边界。产物不记录 hook 名以外的全局位置或 KV 更新范围。
- **影响：** 不是「步前单点交换」。
- **建议：** 按全局 token 位置门控；只在边界步生效一次；随后卸 hook；记录层/位置/KV 范围。

### D-08 — `leaks_target` 仍恒为 False；`position` 不改变边界算法

- **状态：** residual defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `features.py` **25–29**（`leaks = b > limit`）；`events.py` `boundary_index` **105–111**（候选条件恒为 `b <= limit`）；`assert_no_future_leak` **41–43** 无调用方
- **触发条件：** 依赖泄漏标志或 `position="end"` 语义
- **对应要求：** POS-01；协议「跨界 token 不得泄漏目标内容」
- **证据：** 跨界被排除（`test_boundary_excludes_straddle`、X9）——排除本身正确。但选中 token 必有 `b<=limit`，故 `leaks_target` 永假。`test_d01` **263–265** 只断言 False。`"before"` 与 `"end"` 同 limit 同结果（X10）。
- **影响：** 标志不可区分「已排除跨界」与「未检查」。post_step 的不同只来自调用方传入的 `target_end`。
- **建议：** 跨界应显式 `leaks_target=True` 或 `expressible=False` 并强制调用 `assert_no_future_leak`；`boundary_index` 按 kind 改变极限。

### D-09 — thinking 模板未接入；思考区数字可被当成答案

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` `apply_model_template` **51–56**（不返回 `prompt_len` / think span；无调用方）；`adapters.py` **10、18** `think_ids` 未使用；`events.py` `extract_answer` **114–125** 全文找 boxed / `####` / 最后数字
- **触发条件：** Qwen3 `enable_thinking` 或 R1 提示已含 `<think>`；思考区有数字且无 boxed
- **对应要求：** MODEL-01；STACK 56–60
- **证据：** X15、X17。`model_kind=="qwen3"` 才传 `enable_thinking`（方向对）但无调用方。测试无 `apply_model_template`。
- **影响：** 前瞻边界可能落在模板/思考标记上；无效答案与思考区数字混淆。
- **建议：** 用卡片 revision 的 tokenizer 走 `apply_chat_template`；保存 prompt 长度、think 开闭 ID、原始生成 IDs；评分限制在闭合 think 之后（无闭合则 invalid）。

### D-10 — 缓存隔离辅助函数不安全且未使用

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `tiny.py` `clone_cache` **79–85**（无 `copy` 则返回原对象）；定义仅此文件。`collect.py` **41** 只断言两次前向的 cache 不是同一对象。`test_tiny_cache.py` **7–15** 记录 `use_cache=False` 仍写入传入 cache（与 STACK 73 一致）。`decode_loop` **36** 始终 `use_cache=True`，无克隆分支
- **对应要求：** 原文「此前位置 KV 保持 base」；STACK 72–73
- **证据：** X16。`DynamicCache` 无 `.copy()`。多条件若误用 `clone_cache` 会共享存储。
- **建议：** 每条件重新 prefill；或实现经验证的深拷贝。禁止把 `clone_cache` 当作隔离。

### D-11 — CLI 首事件 `pre_step` 不可表达，却硬写 `timing=pre_step`

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `cli.py` **210–218、331**。合成文本 `"q = 0\n"` 事件 `start=0`
- **触发条件：** 默认 fixture collect → intervene
- **对应要求：** POS-01
- **证据：** X14：`pre_step.expressible=false`，`token_index=null`；intervene 仍写 `"timing": "pre_step"`。
- **影响：** 产物看起来像做了步前干预。
- **建议：** 选有前缀的事件；inexpressible 时拒绝 intervene 或写明失败。

### D-12 — 采样配置与 StreamBank 未在条件间共享

- **状态：** confirmed defect
- **严重度：** medium
- **文件 / 符号 / 行号：** `generate.py` `decode_loop` **38** 不传 temperature/top_k/top_p（默认 temp=1 满核）；`cli.py` intervene 用 `default_rng(0/3/5)`，不用 `StreamBank`
- **触发条件：** 「所有处理条件同一采样流」（协议 / STACK 76–80）
- **证据：** 无 generator state / 逐步 uniform 落盘。C-rand 构造与采样流未隔离（当前也无真实采样）。
- **建议：** 记录并复用采样配置与 generator；方向流与采样流隔离。

### D-13 — 非目标 / 无效输出仍不是测出来的；P3 接口缺非目标

- **状态：** residual defect
- **严重度：** high
- **文件 / 符号 / 行号：** `cli.py` **326–330、364–367**（诚实 null，但无测量路径）；`analysis.py` `p3_recovery` **73–80**（只有 `invalid_rate`，无 `nontarget`）
- **触发条件：** 宣称 C2/P3 四项结局
- **对应要求：** CAUSAL-02；协议 117/190/192
- **证据：** `intervention_report` 结构正确，CLI 不调用。`p3_recovery(0.5,0.4,0.3,0.1)` 无 nontarget 键。
- **影响：** 无法排除平凡损伤；Week-8/P3 数字无测量含义。
- **建议：** 由生成文本计算四项；P3 签名加入 nontarget，缺测为 null。

### D-14 — `IsolatedExecutor.submit` 仍是 stub；默认路径不执行宿主代码（默认路径非缺陷）

- **状态：** confirmed stub / 默认路径 non-defect
- **严重度：** medium（stub）/ 信息（host exec）
- **文件 / 符号 / 行号：** `executor.py` **22–24** `raise NotImplementedError`；**27–33** Unavailable；**49–52** 默认 Unavailable；`scoring.py` **19–30**；`t3_humaneval.py` **34–35**
- **对应要求：** EXEC-01；OPS-01
- **证据：** X18；`test_humaneval_never_host_exec` 通过。`forbid_host_exec` **55–59** 无生产引用。`SpyExecutor` 只字符串拒绝 `exec(`，但仍不执行。
- **影响：** 代码题无法真实评分（pending_server）。未发现 host exec 回退。
- **建议：** 保持默认 Unavailable；基类不要 `NotImplementedError`；真实隔离后端标 pending_server。

## 7. 未证实疑点

| ID | 说明 | 为何未升格 |
|---|---|---|
| U-01 | 声称 hash 与本机复算不一致 | 无法区分算法不同与树在 VERSION 写入后漂移 |
| U-02 | `think_ids` (151667/151668, 151648/151649) 与 STACK 表一致 | 禁止下载，未读官方 tokenizer JSON |
| U-03 | `transform` 若原地修改 `tensor[:, -1:]` | hook 先 clone 再写入 patched，但 transform 吃的是**原**切片；现有调用是 `t+0.01` 非原地 |
| U-04 | 基线公平前瞻前缀 | `baselines.py` 仍不强制与探针同一前瞻对象；非本轮主清单，不升格为新 D 项 |

## 8. 外部待验证（pending_server）

| ID | 项目 | 已有代码 | 未验收原因 |
|---|---|---|---|
| P-01 | 真实 Qwen3-8B / R1-Distill-7B 模板、think 跨度、revision | 卡片 revision 与 tiny 架构 | 无权重/tokenizer，无加载器 |
| P-02 | CUDA、精度、长链 KV、position_ids | CPU tiny resid_post 范围符合预期 | 不能外推 GPU |
| P-03 | C2 50 条同批次交换/消融/救援 + 两类对照 | 向量公式与 `geometry_only` CLI | 无真实轨迹与 donor |

## 9. 非缺陷说明、已关闭项与残留 stub

| ID | 类型 | 说明 |
|---|---|---|
| N-01 | 非缺陷 | `apply_swap` / `project_delta`（`interventions.py` **9–16**）在标准正交基下正确；`test_swap_formula` 通过 |
| N-02 | 非缺陷 | tiny 上 resid_post(层1) 不改层 0/1 当前 KV、改层 2、此前 token 保持；`finally` 含异常路径清理有效 |
| N-03 | 非缺陷 | `card()` 拒绝 `revision=="latest"`（`adapters.py` **27–28**） |
| N-04 | 非缺陷 | `enable_thinking` 仅在 `model_kind=="qwen3"` 传入（函数仍未被调用，见 D-09） |
| N-05 | 关闭 | CLI `intervene`/`analyze` **不再写入** 0.8/0.2/0.25 或 `vs_crand=0.6`。本机 numeric outcomes 为空列表 |
| N-06 | 关闭 | `c_rand_delta` 拒绝缺省范数并匹配实际 main 范数；不再等于 `default_rng(1)` 伪 main |
| N-07 | 部分关闭 | 三位置在传入不同 limit 时可分离；跨界 token 不进入 `token_index` |
| N-08 | 非缺陷 | `decode_loop` 保留原始 `prompt_ids` / `generated_ids` / `token_ids` / `stop_reason` |
| N-09 | 非缺陷 | 默认代码评分走隔离执行器且不 host exec |
| S-01 | stub | `IsolatedExecutor.submit` → `NotImplementedError` |
| S-02 | stub | `features.npz` `dummy`/`H`/`E` = \(I_4\) |
| S-03 | stub | `clone_cache` 无 `copy` 时返回原引用 |
| S-04 | stub | `apply_model_template` / `think_ids` / `assert_no_future_leak` / `forbid_host_exec` 无调用方 |
| S-05 | stub | `rescue` 单行加法；`BoundaryMLP` 随机未拟合且不接入 collect（始终 `offline_annotation`） |
| S-06 | stub | `repair.run_repair` `generated_tokens=0`（非本通道主项，列出以免漏检） |
| S-07 | 非 stub | `t2_gsm_plus.py` **21** `pass` 仅为 `status in T4_STATUSES` 空分支 |

## 10. 通道结论

**D 通道不通过。**

相对 round-01，几何层有真实修复：swap 公式仍正确；C-rand 匹配实际范数；INLP 对已投影 H 迭代；CLI 不再虚构正确率；resid_post 改为当前前向 last-token 并在 tiny 上满足 KV 范围与 hook 清理；三位置在不同 limit 下可分开且跨界被排除。

仍不足以支持 CAUSAL-01/02 或 MODEL-01：无真实/tiny 隐状态采集、无事件 donor、C-layer 不是层、hook 非单点一次性、thinking/采样/KV 克隆未接通、四项结局未测量。`cmd_intervene` 产物只是 `geometry_only` 向量范数；`cmd_analyze` 的 p1–p3 为 null。二者现在诚实，但仍不是科学效应。
