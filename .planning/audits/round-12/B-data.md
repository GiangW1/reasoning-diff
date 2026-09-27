# Review B — 数据与测量（独立审查，round-12）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-12 通道报告。round-01–10 `B-data.md` 只用作待复验清单与行文格式，不作为证据。点名 CE 全部用独立 oracle 复跑，不调用作者 `test_*` 断言。

**开审冻结核验：`HASH_MATCH`。交卷：`HASH_MISMATCH`。** 按 `.planning/audits/round-12/VERSION.md` 原文脚本（POSIX relpath + `\x00` + 文件字节）独立复得 `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（61 文件，0 CRLF），与声明一致。审查中途先漂到 `0816fa5b…`（`splits.py` + `test_round07`）。成文前最后一次 `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`（仍 61 文件）。相对开审已变：`splits.py`（152→184，`08f77e97…`→`40ab4021…`）、`cli.py`（1254→1249，`175abf12…`→`779cedd3…`）、`tests/test_round07_regressions.py`（221→256，`a59c236d…`→`68f32ca3…`）。`measure.py` / `edits.py` / `events.py` / `generate.py` / 全部 `tasks/*.py` 与开审同 digest。**点名 CE 结论绑定开审冻结字节**；交卷后的 `splits.py` 持久化锁与 `cli.py` 删行不得记为冻结已闭。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-12） |
| review_time | `2026-09-21T02:32:32+08:00`（复算 hash / 开读）— `2026-09-21T02:39:30+08:00`（交卷最后一次复算） |
| declared_frozen_hash | `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`（`.planning/audits/round-12/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `598e6c8fe371cf1a977f746f9f5c71ab195e4b2d0caf372311fdea757c4f6bd4`。61 文件。配方与 VERSION 一致。0 CRLF。 |
| 交卷复算 | **`HASH_MISMATCH`** 最后一次 `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`（中段曾为 `0816fa5b…`）。`splits.py` `08f77e97…`→`40ab4021…`（152→184）；`cli.py` `175abf12…`→`779cedd3…`（1254→1249）；`test_round07_regressions.py` `a59c236d…`→`68f32ca3…`（221→256）。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写本文件） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5 / §5.15；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02 |
| pytest_author_claim | VERSION 写 156 passed。开审冻结树上独立复跑 **156 passed / 22.94s / exit 0**。绿测试不是论文正确性。交卷树未再全量复跑。 |

相对 r10 开审 `81308124…`：本冻结已含当时交卷漂入的 `measure.py` `b15fb8a5…`（392）与 `cli.py` `175abf12…`（1254）。`edits.py` / `events.py` / 开审 `splits.py` / `generate.py` / 全部 `tasks/*.py` 与 r10 B 开审 digest 相同。夹具字节未变。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度调用链而通读；`fixture` = 对照适配器读完。行数/SHA-256 为 **开审 HASH_MATCH** 冻结树。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 392 | `b15fb8a5bb92220f5693b01acf6b60bd6640b57449e6419cb0e7b2bc6e4b6ba6` | full 1–392 | **B9-01：** `noise_ref` 只写 `sham:` 行；`sham_hits` 先于 `real_hits` |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`review_export` / `merge_review`；生成区解析仍登记前提实体 |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | 祖先只返回节点键；非算术 `graph_kind` → `{}` |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf` | full 151–226 | **B5-05：** `apply_rename_edit` 改写 id/parents/expression |
| `src/reasoning_diff/splits.py` | 152 | `08f77e972927a9961885c09e0538f0c43d47ca6638944e1c80465cf6cc4af066` | full 1–152 | **B5-01：** 进程内 `_TEST_ONLY_FAMILY_KEYS`；`siblings=`；**无持久化** |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | 身份、`scan_state`、placeholder |
| `src/reasoning_diff/cli.py` | 1254 | `175abf12f4c207c551c6f5c5910b002d62f7f9125f41226389d0acbde4083c17` | callsite 257–408, 674–716 | `split_for_task` **不传 `siblings`**；`sham:` 前缀；无 `merge_review` 命令 |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844` | callsite 105–192 | 只解析 `generated=gen_text+assigned`；`parse_region=generated` |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `register_test_only_family`；`fit_eligible=False` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 写 `shared_gsm_text`；不注册锁 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 拒非 fixture |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | 口述 `requires_independent_truth` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式 |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169, 215–257 | P2 整数分母；Gate 未注册 |
| `tests/test_round07_regressions.py` | 221 | `a59c236d5d007ae77314fe80dee390d30c99e6706c9f285d40a03b4bdbfca328` | callsite | 作者测试；**不作为本通道证据** |

夹具 SHA-256（与 r06–r10 相同）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

交卷后磁盘上的 `splits.py` 增加 `.planning/research/.cache/gsm_test_only_families.json` 持久化。该路径与补丁 **不在声明冻结内**。

## 3. 已执行检查

独立 oracle（临时脚本，不写入 `src/` / `tests/` / `pyproject.toml`）。`measure.py` / `edits.py` / `events.py` / `generate.py` / 全部 `tasks/*.py` 在开审与交卷间 **digest 未变**。scientific / fixture CLI oracle 跑在开审 `cli.py` `175abf12…` 上；交卷后 `cli.py` 已漂，但第 261 行仍不传 `siblings`。`splits.py` 在 B5-01 oracle 之后被改写；B5-01 点名 API 在两种实现上同结果，生产残留按 **开审 152 行原文** 判定。

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审 **HASH_MATCH** 61 文件 `598e6c8f…`。交卷 **HASH_MISMATCH** 最后一次 `1f61fd06…`（中段 `0816fa5b…`）。 |
| X-00 | 作者 pytest 主张 | `python -m pytest tests -q --tb=line` | 开审树 **156 passed / 22.94s / exit 0**。VERSION「156 passed」计数成立。绿 ≠ 正确。 |
| X-03 | 矩阵 `noise=None` | `dependency_densities(..., noise=None)` | `null_reason=noise_missing`。保持关闭。 |
| X-04 / X-05 | 有限扫描 / `exhaustive` | `build_labels` | 非 observed 或非穷尽 → unknown；`exhaustive`+`observed_response`+`no_change` → `behavior_label=0`。 |
| X-23 | 空 `noise_set` | 集合密度 API | 未评估 → `noise_set_empty`。已评估 → `rho_S_noise=0.0`。 |
| X-12e / **B9-01** | 广播 / 仅 sham / 映射 p3 / 0-hit / CLI | 独立构造 + scientific prepare | **点名 CE 通过。** 见 §3.1。 |
| X-19 / **B5-01** | 族锁 / `siblings=` / 孤立 Symbolic | 独立 JSON（非仓库夹具） | **点名 CE 通过；冻结生产路径仍不共组。** 见 §3.2。 |
| X-25 / **B5-05** | rename 重写表达式 | `make_source_value_pair(t1_tiny,"p2","2")` | **点名 CE 通过。** 见 §3.3。 |
| X-b601 / X-sci | 生成区事件 | `generate_task_trace` + scientific CLI | **原触发保持关闭。** 见 §3.4。 |
| X-18 | Plus 生产划分 | 夹具 / `refuse_fit_split` | `fit_eligible=False`，`split=test`；`probe_train` 拒绝。 |
| X-11 | 公式编辑 | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，a=5，answer=8。 |
| X-plus-sub | Plus 孤立数字 | 独立官方字段题干 | `3`→`9` 只改孤立 3；`13` 中的 `3` 拒。`needs_truth`。 |
| X-20 | T3 口述 / 祖先 | `document_edit` / `paragraph_edit` | Hotpot / MuSiQue `needs_truth` + `requires_independent_truth`。`ancestors=={}`。节点值已清空。 |
| X-26 | 官方夹具重算 | `load_igsm_snapshot` / fixture 加载器 | 官方 shape answer=9。fixture 加载器拒 official 形状。 |
| X-17 | `assign_family` | 缺 id；同 id | 缺 id 抛错。同 `family_id` 角色相同。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-t4 / X-t1cfg / X-gate / X-p2 | 四态 / 格子 / Gate / P2 | 库 API | T4 四态 placeholder；op=7 拒；三门 `unregistered`；无 `shared_premises` → `denominator_unverified`。 |
| X-21 | CLI fixture prepare + sham | `main(["prepare", …, "--sham-opportunities","1"])` | exit 0。`premise_id=sham:q`，`no_change`。`edits.jsonl` 含 remap 后的 `source_value_pair`。 |

### 3.1 B9-01 独立复验（不信任作者测试）

冻结 `measure.py` 72–80：同事件 sham 命中后，**只有** `premise_id` 以 `sham:` 开头的标签行写 `noise_ref`；真实前提行保持 `None`。328–349：先收集 `sham_hits`，有则 `noise_set=None` / `evaluated=False`，**不再**把广播后的 `real_hits` 写入 \(N\)。

1. **生产形态观测（p1 no_change + p2 changed + `sham:q` changed）。** `noise_ref`：`p1=None`，`p2=None`，`sham:q=1.0`。`broadcast_to_real=False`。事件层 `null_reason=noise_set_missing`，`rho_M_excess=None`。
2. **仅 `sham:q` 行。** 同样 `noise_set_missing`，excess 为 null。
3. **显式映射 `p3∈P\\T`、`noise_ref=1`、无 sham 行。** `rho_S_noise=1.0`，`rho_S_excess=-1.0`，`null_reason=None`。映射真实噪声前提仍入 \(N\)。
4. **0-hit 且已观察（`noise_ref=0.0`，p3∈P\\T）。** `rho_S_noise=0.0`，excess=0。未观察（全 `None`）走 `noise_set_empty`（null，不是 0）。
5. **手工重建旧广播（p1/p2 也被标 `noise_ref=1` 且存在 `sham:q`）。** 密度路径仍 `noise_set_missing`（`sham_hits` 优先）。双保险成立。
6. **空 `event_id` 回退 + 真实前提 `noise_ref=1`。** `_fallback_noise_set` 仍把 `{p1,p2}` 写入 \(N\)：`rho_M_noise=0.0`，`rho_M_excess=1.0`。生产 label 行有 `event_id`。保留为回退支（U-13），**不**否决点名 CE。
7. **CLI scientific prepare**（`--eval-mode scientific --sham-opportunities 1`，exit 0）：
   - 标签：`(q,p1)`/`(q,p2)` 的 `noise_ref=None`；`(q,sham:q)` 的 `noise_ref=1.0`。
   - sham 观测 `changed`，raw `82` vs `53`（tiny 跨 seed 抖动，不是前提编辑）。
   - 事件密度：`null_reason=noise_set_missing`，`rho_M_raw=1.0`，**`rho_M_noise=None`，`rho_M_excess=None`**。
   - 同文件 note「sham hits are not mapped onto real premises」与数字一致。
   - 对比 r09/r10 在旧广播树上的同一路径：当时写出 `rho_M_excess=1.0`。本冻结已独立证伪该入账。

CLI fixture sham 为 `no_change`（合成题干相同）：走已评估空 \(N\)，`rho_M_excess=-0.5`。这是 0-hit 记账（B-12），不是把 sham 命中映射到真实前提。

事件均值聚合不回传顶层 `null_reason`（只留在 `events[0]`）。不构成错误入账。

**B9-01 点名 CE：PASS。** 作者主张「`noise_ref` 只在 `sham:`；广播不再写入 \(N\)」在声明冻结上独立成立。

### 3.2 B5-01 独立复验（不信任作者测试）

构造独立 JSON（非仓库夹具）。仓库夹具 `original_id=gsm8k-12` 的 `assign_split("gsm8k-12")=="test"`（哈希落入 test 桶），**不能**区分族锁与偶然划分。本通道用 `gsm8k-1`（`assign_split=="probe_train"`）。

开审冻结 `splits.py`（152 行）：`register_test_only_family` 只写进程内 set；`clear_test_only_families` 只清内存；`cli.cmd_prepare` 第 261 行 `split_for_task(task, seed=…, fractions=…)`，**不传 `siblings`**。

1. **Plus `original_id=gsm8k-1` 然后 Symbolic 同 id。** Plus：`shared_gsm_family=gsm8k-1`，`shared_gsm_text=q:ada has 4 apples…`，`base_group_id=gsm_plus:gsm8k-1`，`fit_eligible=False`，`split=test`。随后 Symbolic：**`split=test`**，族键与文本键均相等。点名条件 **成立**。
2. **官方 Plus 字段（无 `original_id`，有 `seed_question`）。** Plus 族 ID 回退为 `q:` 文本键；与 Symbolic `original_question` 规范化后 **文本键相等、族 ID 不等**（`q:…` vs `gsm8k-1`）。Plus 加载后 Symbolic **锁 `test`**。点名条件 **成立**。无 seed→GSM8K ID 表。
3. **`siblings=` 显式队列。** `clear` 后 `split_for_task(symbolic, siblings=[plus])=="test"`；无 siblings 为 `probe_train`。无关 Plus（`gsm8k-99`）**不**锁 `gsm8k-1`。点名条件 **成立**。
4. **孤立 Symbolic `gsm8k-1`（清空寄存器）。** `split_for_task=assign_split=probe_train`。
5. **同进程 CLI：先 prepare Plus（`gsm8k-1`）再 prepare Symbolic。** 两者 `splits.jsonl` 均为 `role=test`。点名生产同进程路径 **成立**。
6. **冻结生产「只 prepare Symbolic」。** `cmd_prepare` 不传 `siblings`，寄存器不持久化。新进程孤立 `gsm8k-1` 仍是 `probe_train`。仓库夹具 `gsm8k-12` 的孤立 CLI 为 `test` **只因哈希**，不能当锁的证据。

交卷后的 `splits.py` 把锁写进 `.planning/research/.cache/gsm_test_only_families.json`。当前磁盘该文件为 `["gsm8k-12", "q:ada has 4 apples…"]`。新进程、同文本的孤立 `gsm8k-1` 会被锁成 `test`；**不同文本**的 `gsm8k-1` 仍是 `probe_train`。`clear_test_only_families()` 会删除该文件。这是冻结外补丁，且是规划缓存而不是可复查族表。**不能关闭冻结对象上的 B5-01-prod。**

**B5-01 点名 CE（family lock）：PASS。生产共组（冻结）：未闭（见发现 B5-01-prod）。**

### 3.3 B5-05 独立复验

`make_source_value_pair(t1_tiny, "p2", "2")`：

- `same_value_diff_source.kind=same_value_diff_source`
- `premise_id`：`['p1','p2_src']`（不再保留 `p2`）
- `expression`：`p1 * p2_src`（**不是**表面改名残留 `p1 * p2`）
- `parents`：`['p1','p2_src']`
- 题干：`p1 = 4. p2_src = 0. What is q = p1 * p2_src?`
- 值侧 `same_source_diff_value` 重算答案 `8`；源侧答案仍 `0`

`review_export`：`review=None`、`review_status=awaiting_human`。`merge_review` 按 `record_id` 回填并标 `filled`。`cli.py` **没有** `merge_review` 子命令。

scientific / fixture `edits.jsonl` 均含 `kind=source_value_pair`；scientific `trace_ids.same_value_diff_source=trace-source`；源臂题干/表达式/父母均为 `p2_src`。图上仍只有一个来源节点改名，没有协议级 A/B 双来源节点。

**B5-05 点名 CE（remap expression/id/parents + awaiting/merge 库函数）：PASS。** A/B 双来源图见 U-12，不重开点名 CE。

### 3.4 生成区事件（B6-01）

`generate_task_trace`：`parse_region=generated`，事件仅 `q`，`start=45 >= prompt_len=36`。题干 `parse_events` 仍能解析 `p1`/`p2`（解析器仍登记非 placeholder 前提）。

scientific prepare 七条轨迹（`trace-base` / `t0p` / `edit` / `source` / 两条 allowed edit / `sham`）全部 `parse_region=generated`，事件均为 `q`。`trace-source` 的 `start=53`（改名题干更长，prompt 44）。无 `p1`/`p2`/`p2_src` 生成事件。

**B6-01 原触发：保持关闭。**

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 B5-01 点名 CE 已在独立 JSON 上跑 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b` |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | 本机 tiny 解码不是科学噪声协议 |
| N-08 | 交卷树干净全量 pytest | `splits.py` 已漂；156 只绑开审树 |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## / B6-## / B9-## 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。作者本轮主张关闭 B9-01，并要求在 `598e6c8f…` 上重核 B5-01/05。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | — | **closed** | X-03 |
| B-02 / B-23 | — | **closed** | X-04 / X-05 |
| B-08 | — | **closed** | X-11 |
| B-09 / B-24 / **B5-02** | — | **closed** | X-plus-sub |
| B-12 0-hit | — | **closed** | X-12e 0-hit + p3 |
| B-13 / B-14 | — | **closed** | X-17 / X-18 |
| B-15 / **B5-01** | Plus 注册 family 锁，Symbolic 同族 `test` | **点名 CE closed**；**冻结生产路径 residual** | X-19 / §3.2 / 发现 B5-01-prod |
| B-16 / **B5-03** / B-20 | — | **closed** | X-20 |
| B-18 / **B5-05** | rename 改写 id/表达式 | **点名 CE closed** | X-25 / §3.3。A/B 图见 U-12 |
| B-19 | — | **closed** | X-26 |
| B-22 / B-26 | — | **closed** | X-p2 / X-23 |
| **B6-01** | — | **closed**（原触发） | X-b601 / X-sci |
| **B5-04** / **B6-02** / **B9-01** | sham `noise_ref` 只在 `sham:`；广播不再写入 \(N\) | **closed** | §3.1。冻结 scientific 不再写出 `rho_M_excess=1.0` |

未在本轮逐条复跑的 B-03/04/05/06/07/10/11/17/21/25/27：其依赖文件相对开审未变；不新开，也不用作者测试回写关闭。

## 6. 发现（本轮开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

---

### B5-01-prod 冻结生产 prepare 不共组同源 Symbolic

- **状态：** confirmed defect（机制：冻结生产调用方）/ pending_server（真实 dump 碰撞率）
- **严重度：** high
- **符号：** `cli.cmd_prepare`；`splits.split_for_task`；`splits._TEST_ONLY_FAMILY_KEYS`
- **行号（开审冻结）：** `cli.py` 261；`splits.py` 10, 35–46, 95–121
- **协议：** DATA-03 / GOAL §5.5：同基础题、同源题、全部变体共组；Plus 测试专用不得把同源 Symbolic 放进拟合再当未见题。
- **证据：**
  1. 点名 CE（同进程 Plus→Symbolic、官方文本键、`siblings=`、同进程 CLI）**通过**。
  2. 清空寄存器后孤立 Symbolic `gsm8k-1` → `probe_train`。`assign_split("gsm8k-1")==probe_train`。
  3. 生产 `prepare` 一次只加载一个 task，不传 `siblings`，开审 `splits.py` 无落盘族锁。
  4. 仓库夹具 `gsm8k-12` 孤立即为 `test`，是哈希桶，不是锁。作者若只用该夹具会假绿。
  5. 交卷 `splits.py` 的规划缓存持久化 **不在冻结内**，且 `clear()` 会删文件；不同文本的 `gsm8k-1` 在交卷树上仍是 `probe_train`。
- **影响：** 按分数据集、分进程 prepare 时，B5-01 点名 API 通过也仍会一边拟合、一边当未见测试。
- **建议：** 划分阶段显式读入整族并传 `siblings=`，或把 test-only 族键写进可复查清单再消费。不要依赖「先 import Plus」或规划目录下的隐藏 JSON。

B9-01 **不是**本轮开放缺陷。

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| **B9-01** / B6-02 广播入 \(N\) | §3.1 scientific `rho_M_excess is None` | U-13 空 `event_id` 回退 |
| **B5-01 点名 CE** | §3.2 | B5-01-prod；无 seed→ID 表 |
| **B5-05 点名 CE** | §3.3 | U-12 A/B 图；CLI 无 merge 命令 |
| **B6-01** | §3.4 | U-10 |
| B-01/02/08/09/12–14/16/19/22/23/26；B5-02/03 | 本轮抽查 | — |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径缺协议 → null | `measure.py` 126–137 | 不否定已关的 B9-01。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | X-26。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-12 | `siblings=` 与文本键锁在 **被调用时** 正确 | 开审 `splits.py` 95–121 | 不否定 B5-01-prod。 |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05。 |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `event_density_sets` | |
| ND-21 | Plus/T3 Edit 缺核验不写 valid | 各 apply* | X-20 / X-plus-sub。 |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 124–134 | |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | `analysis.py` 215–257 | **不是缺陷。** |
| ND-26 | scientific 拒 0 事件 | `cli.py` 296–297 | |
| ND-27 | `_e_premise_ids` 跳过 `sham:` | `cli.py` 708–716 | |
| ND-28 | 约束 `\nq = <digit>` 是 tiny 可解析接口 | `generate.py` | 不是 §4.1 自然 CoT。 |
| ND-31 | 事件均值密度不拷贝顶层 `null_reason` | `measure.py` 110–114 | 事件行仍有 `null_reason`；scientific 可查。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；tiny 命中不能当协议命中率 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 | 文本键机制已测；dump 上格式差仍会拆族 |
| S-07 | Linux cgroup / 容器隔离执行器 | EXEC-01 / GOAL §5.15 | 本机未验收 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-08 | `behavior_label!=1`（含 unknown）进入 M | scientific 上 `M={p1,p2}`、`rho_M_raw=1` 来自 tiny 未改数字。未升格；**不再掩盖噪声记账**（B9-01 已关）。 |
| U-10 | `parse_events` 仍把非 placeholder 前提登记为可解析实体 | 生产只喂生成区。tiny 未回显 `p1 =`。不重开 B6-01。 |
| U-12 | `same_value_diff_source` 仍是同图改名，不是第二来源节点 | 点名 CE 只要求 remap id/expression/parents，已满足。 |
| U-13 | 空 `event_id` fallback 仍把 `noise_ref=1` 的真实前提写入 N | 生产 label 行有 `event_id`。不并入已关的 B9-01。 |
| U-14 | 交卷持久化锁写在 `.planning/research/.cache/` | 不在冻结内；`clear()` 可删；不是可复查划分清单。不把它当 B5-01-prod 关闭证据。 |

## 11. 测试质量对本通道的含义

**156 passed ≠ 数据/测量正确。** 独立同意 **B9-01、B5-01 点名 family lock、B5-05 remap、B6-01 生成区** 在开审冻结上可关。缺口：

- `test_plus_locks_symbolic_family_to_test` 类用例若先加载 Plus，不测清空后的孤立 `gsm8k-1`，也不测 CLI 无 `siblings`。仓库夹具 `gsm8k-12` 孤立即为 `test`，会假绿。
- `test_source_value_pair_*` 若只查 kind，不能代替表达式/parents；本通道已独立查到 remap 成立。
- 交卷后对 `test_round07_regressions.py` 的改动绑定的是 **漂后** 树，不能回写冻结关闭。
- 作者 `test_scientific_sham_does_not_book_rho_m_excess_one` 的断言是 `rho_M_excess != 1.0 or null_reason`，弱于本通道要求的「`None` 且 `noise_set_missing`」。本通道已用更强 oracle 通过。

因此不能把 B5-01 的 **冻结生产共组** 标为已关闭。不能把交卷 `splits.py` 持久化记成声明冻结已闭。

## 12. 通道结论

数据与测量通道 **不能** 在声明冻结 `598e6c8f…` 上给出整树通过意见。**FAIL。**

1. **开审 `HASH_MATCH`（61 文件）。交卷 `HASH_MISMATCH`（最后一次 `1f61fd06…`）。** 结论只绑开审 digest。`splits.py`、`cli.py` 与一份测试在审查中被改写；事后持久化锁不是冻结关闭。连续通过计数 **不能开始**。
2. **点名 CE（独立 oracle，不信作者测试；绑定未漂源文件）：**
   - **B9-01：PASS。** 库级与 scientific CLI 均不再把 sham 命中广播进真实前提或写入 \(N\)。scientific：`p1`/`p2` 的 `noise_ref=None`，`null_reason=noise_set_missing`，`rho_M_excess=None`。映射 `p3` 仍入 \(N\)。
   - **B5-01 family lock：PASS。** Plus `gsm8k-1`→Symbolic 同为 `test`；官方无 `original_id` 的文本键锁 test；`siblings=` 显式队列锁 test，无关 Plus 不误锁；同进程 CLI Plus→Symbolic 均为 `test`。
   - **B5-05：PASS。** `same_value_diff_source` 重写 `premise_id`/`parents`/`expression` 为 `p2_src` / `p1 * p2_src`；`review_export` 为 `awaiting_human`；`merge_review` 按 `record_id` 回填。
   - **生成区事件（B6-01）：PASS。** scientific / `generate_task_trace`（含 `trace-source`）只解析生成区，事件均为约束 `q`，`start>=prompt`。
3. **仍确认的机制缺陷：**
   - **B5-01-prod（high）：** 点名 lock ≠ 冻结 DATA-03。生产 prepare 不传 `siblings`，开审 `splits.py` 无持久化；孤立 `gsm8k-1` 仍是 `probe_train`。交卷缓存锁在冻结外。
4. T1 来源隔离、有限扫描 unknown、身份不含值、Plus 孤立替换、Hotpot/MuSiQue 真值旗标、HE placeholder、Gate 未注册仍成立（ND-01–ND-31），不能抵消冻结漂移与生产划分缺口。官方全量保持 `pending_server`。Gate 0–2 未注册与 `scientific_conclusion=None` **不是缺陷。**
