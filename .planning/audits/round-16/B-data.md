# Review B — 数据与测量（独立审查，round-16）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-16 通道报告。round-01–14 `B-data.md` 只用作待复验清单与行文格式，不作为证据。点名 CE 全部用独立 oracle 复跑，不调用作者 `test_*` 断言。审查过程中对 `.planning/research/.cache/gsm_test_only_families.json` 做了隔离清空/写锁，结束后已恢复开审内容 `["gsm8k-12", "q:ada has 4 apples…"]`。

**开审冻结核验：`HASH_MATCH`。交卷：`HASH_MISMATCH`。按指令 `HASH_MISMATCH → FAIL`。** 按 `.planning/audits/round-16/VERSION.md` 原文脚本（POSIX relpath + `\x00` + 文件字节）独立复得 `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（61 文件，0 CRLF），与声明一致。oracle 执行时 `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`。成文前最后一次 `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（仍 61 文件，0 CRLF）。相对开审已变：`edits.py`（362→365）、`measure.py`（408→405）、`cli.py`（1252→1260，oracle 时 1259）、`tests/test_round06_regressions.py`、`tests/test_round07_regressions.py`（oracle 后再加长）。`splits.py` / `events.py` / `graphs.py` / `schema.py` / 全部 `tasks/*.py` / `generate.py` / `tiny.py` / `analysis.py` 与开审同 digest。**点名 CE 中依赖未漂文件的结论绑定开审冻结字节**；A13-01 / A13-03 / B9-01 的可执行复跑发生在漂后树上，另注，不回写冻结关闭。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-16） |
| review_time | `2026-09-21T02:52:00+08:00`（复算 hash / 开读）— `2026-09-21T03:28:00+08:00`（交卷复算） |
| declared_frozen_hash | `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（`.planning/audits/round-16/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`。61 文件。配方与 VERSION 一致。0 CRLF。 |
| 交卷复算 | **`HASH_MISMATCH`** `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`。`edits.py` `250055ab…`→`1e5b97d6…`（362→365）；`measure.py` `8ec8cf09…`→`985b9d93…`（408→405）；`cli.py` `c1a274e2…`→`9431b776…`（1252→1260）；`test_round06_regressions.py` `280f9f71…`→`b555ed24…`；`test_round07_regressions.py` `f942482f…`→`8c23db4b…`（302→342）。oracle 中间树 `3d0a0764…`（`cli.py` 当时 `b37fef2c…` / 1259 行）。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（本通道只写本文件与 `.planning/audits/round-16/_b_scratch_*` 独立 oracle；审查中途的 `src/` / `tests/` 漂移不是本通道写入） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文/协议 §2.2–2.3、§2.6；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5 / §5.15；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02 |
| pytest_author_claim | VERSION 写 159 passed。本通道独立复跑 **160 passed / 28.37s / exit 0**。绿 ≠ 正确；主张「159」**不成立**。 |

相对 r14 开审：本冻结已含 `edits.py` 开审 `apply_alt_source_same_value`（`p2_src` + `(alt source)`）、`measure.py` `_has_sham_row`、`generate.py` tiny 拒超 96 token（不再 48 截断）。交卷时这三处生产文件中的前两处被他方改写。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度调用链而通读；`fixture` = 对照适配器读完。行数/SHA-256 为 **开审 HASH_MATCH** 冻结树，除非标明交卷漂移。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 408 | `8ec8cf09db1490978f5eacd7d90fd578cfe807bb2c6e09e2d002ae62ab83002c` | full 1–408 | **B9-01 / A13-03：** `noise_ref` 只写 `sham:`；`_has_sham_row` 或 `sham_hits` → `noise_set=None`。交卷漂至 405 / `985b9d93…`（0-hit 无 sham 不再记已评估空 \(N\)） |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`review_export` / `merge_review` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | 祖先只返回节点键；非算术 `graph_kind` → `{}` |
| `src/reasoning_diff/edits.py` | 362 | `250055ab8257ea2e24be885a389713e0c6d71c93936b44794a1ec821cf9e39db` | full 1–362 | **A13-01：** 开审删原叶、写 `p2_src = 0 (alt source)`、父母/表达式 remap。交卷漂至 365 / `1e5b97d6…`（保留 `p2`、加 `src_b`、无 `(alt source)`） |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | **A10-04：** 内存 ∪ `.planning/research/.cache/gsm_test_only_families.json`；`clear()` 删文件；`_TEST_ONLY_FAMILY_KEYS.clear()` 只清 RAM。**未漂。** |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | 身份、`scan_state`、placeholder |
| `src/reasoning_diff/cli.py` | 1252 | `c1a274e233988aad3c3390041cd40ad5e214ade82ba7579a3c7c8fc35156a71a` | callsite 257–417, 676–712, 823–856 | `split_for_task` **不传 `siblings`**；`sham:` 前缀；无 `merge_review` 命令。交卷漂至 1260 / `9431b776…`（oracle 时 1259 / `b37fef2c…`） |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173` | callsite 101–191 | `task_prompt=question`；`len(prompt_ids)>96` 拒绝截断。**未漂。** |
| `src/reasoning_diff/models/tiny.py` | 120 | `c75d0f53257666128facbfd1f2ab292edc3a99f9840e617bcce35d59d74c537f` | callsite | 随机权重 miniature。**未漂。** |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `register_test_only_family`；`fit_eligible=False` |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 写 `shared_gsm_family` / `shared_gsm_text`；不注册锁 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 拒非 fixture |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | 口述 `requires_independent_truth` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值；`graph_kind=composition_reference` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 注入非祖先 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | `hotpot` / `t3_musique` 加载器 |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169, 215–257 | P2 整数分母；Gate 未注册 |

夹具 SHA-256（与 r06–r14 相同）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

独立 JSON（非仓库夹具，`original_id=gsm8k-1`，题干 Bob/Cara，避免与缓存文本键 `q:ada has 4 apples…` 碰撞）：`.planning/audits/round-16/_b_scratch_run/plus_gsm8k1.json` 等。审查结束时把持久化锁文件恢复为开审内容。

## 3. 已执行检查

独立 oracle（`.planning/audits/round-16/_b_scratch_run/oracle.py`，不写入 `src/` / `tests/` / `pyproject.toml`）。`splits.py` / 全部 `tasks/*.py` / `events.py` / `graphs.py` / `schema.py` / `generate.py` 在开审与交卷间 **digest 未变**，A10-04 / T3 / Plus 孤立数字 / HE 分母绑定冻结。`measure.py` / `edits.py` / `cli.py` 在开读之后、oracle 执行之前被改写；库级 B9-01 / A13-03 在漂后树上仍通过；**A13-01 可执行复跑绑漂后 `edits.py`，失败。** 开审 `edits.py` 原文另作源读对照，不替代冻结字节上的执行。

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审 **HASH_MATCH** 61 文件 `5413a4bc…`。oracle **HASH_MISMATCH** `3d0a0764…`。交卷 **HASH_MISMATCH** `3d0f1c10…`。 |
| X-00 | 作者 pytest 主张 | `python -m pytest tests -q --tb=line` | **160 passed / 28.37s / exit 0**。VERSION「159 passed」**不成立**。绿 ≠ 正确。 |
| X-03 | 矩阵 `noise=None` | `dependency_densities(..., noise=None)` | `null_reason=noise_missing`。保持关闭。 |
| X-04 / X-05 | 有限扫描 / `exhaustive` | `build_labels` | 非 observed 或非穷尽 → unknown；`exhaustive`+`observed_response`+`no_change` → `behavior_label=0`。 |
| X-23 | 空 `noise_set` | 集合密度 API | 未评估 → `noise_set_empty`。 |
| **A10-04** | 族锁 / 持久化 / RAM-only clear / 子进程 / `siblings=` | 独立 JSON（非仓库夹具） | **点名 CE 通过。** 见 §3.1。 |
| **A13-01** | alt-source 文本与父母 | 库 API + fixture/scientific `edits.jsonl` + `trace-source` | **可执行复跑失败（漂后树）。** 见 §3.2。 |
| **B9-01** | 广播 / 仅 sham / 映射 p3 / CLI | 独立构造 + fixture/scientific prepare | **点名 CE 通过。** 见 §3.3。 |
| **A13-03** | sham `no_change` excess 必须为 null | 库 + fixture CLI | **点名 CE 通过。** 见 §3.4。 |
| X-18 | Plus 生产划分 | `refuse_fit_split` | `fit_eligible=False`，`split=test`；`probe_train` 拒绝。 |
| X-11 | 公式编辑 | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，answer=8。 |
| X-plus-sub | Plus 孤立数字 | 独立官方字段题干 | `3`→`9` 只改孤立 3，`13` 保留；仅 `13` 的题干拒 `3`。`needs_truth`。 |
| X-20 / **T3** | T3 口述 / 祖先 / prepare | `document_edit` / `paragraph_edit` / CLI | **点名 CE 通过。** 见 §3.5。 |
| X-26 | 官方夹具重算 | `load_igsm_snapshot` / fixture 加载器 | 官方 shape answer=9。fixture 加载器拒 official 形状。 |
| X-17 | `assign_family` | 缺 id | 缺 id 抛错。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-t4 / X-t1cfg / X-gate / X-p2 | 四态 / 格子 / Gate / P2 | 库 API | T4 四态 placeholder；op=7 拒；三门 `unregistered`；无 `shared_premises` → `denominator_unverified`。 |
| X-he | HE placeholder 分母 | `event_density_sets` | `kind=placeholder`，ρ 所用 premises=`[]`，`denominator_S=None`。 |
| X-0hit | 无 sham 的 0-hit（对照，非点名） | `p3` `noise_ref=0` | 开审源码会记已评估 \(N=∅\)。**漂后树** `null_reason=noise_set_missing`。见 U-18。不否决 A13-03。 |

### 3.1 A10-04 persist 独立复验（不信任作者测试）

构造独立 JSON（非仓库夹具）。仓库夹具 `original_id=gsm8k-12` 的 `assign_split("gsm8k-12")=="test"`，**不能**区分族锁与偶然划分。本通道用 `gsm8k-1`（`assign_split=="probe_train"`），题干为 Bob/Cara。

开审冻结 `splits.py`（184 行，**未漂**）：`register_test_only_family` 写内存并 `_save_persisted_locks()` 合并到 `.planning/research/.cache/gsm_test_only_families.json`；`family_locked_test` = 内存 ∪ 文件；`_TEST_ONLY_FAMILY_KEYS.clear()` **不**删文件；`clear_test_only_families()` 清内存并 `unlink` 文件。`cli.cmd_prepare` 仍不传 `siblings`。

1. **Plus `original_id=gsm8k-1` 然后 Symbolic 同 id。** Plus：`shared_gsm_family=gsm8k-1`，`fit_eligible=False`，`split=test`，持久化 `["gsm8k-1", "q:bob has 4 pears…"]`。随后 Symbolic：**`split=test`**，族键与文本键均相等。点名条件 **成立**。
2. **官方 Plus 字段（无 `original_id`，有 `seed_question`）。** Plus 族 ID 回退为 `q:` 文本键；与 Symbolic `original_id=gsm8k-1` **族 ID 不等、文本键相等**。Plus 加载后 Symbolic **锁 `test`**。点名条件 **成立**。
3. **`siblings=` 显式队列（清空持久化后）。** `split_for_task(symbolic, siblings=[plus])=="test"`；无 siblings 为 `probe_train`。无关 Plus（`gsm8k-99`）**不**锁 `gsm8k-1`。
4. **`_TEST_ONLY_FAMILY_KEYS.clear()`（只清 RAM）。** 文件仍在。`family_locked_test(...)==True`，Symbolic **`split=test`**。**A10-04 点名条件成立。**
5. **全新 Python 子进程（内存空，只读 JSON）。** stdout：`test` / `0` / `True`。点名条件 **成立**。
6. **生产 CLI：`prepare --kind gsm_plus`（独立 `gsm8k-1` JSON，exit 0）后新进程只 load Symbolic。** Plus `splits.jsonl` `role=test`；子进程 `split_for_task=test` 且 `_TEST_ONLY_FAMILY_KEYS` 长度为 0。点名生产路径 **成立**。
7. **`clear_test_only_families()` 后孤立 Symbolic（本进程无 Plus）。** `split_for_task=assign_split=probe_train`，锁文件不存在。作者主张「诚实、不是残留」：**同意**。不是 A10-04 失败。

**A10-04 persist：PASS。** 绑定未漂 `splits.py` `40ab4021…`。

### 3.2 A13-01 alt-source 文本与父母（不信任作者测试）

**开审冻结源读（`edits.py` 219–289，`250055ab…`，执行前已通读）：** `apply_alt_source_same_value` 删原叶、`new_id=f"{premise_id}_src"`、`new_text=f"{new_id} = {value} (alt source)"`、remap 父母与表达式，并断言 required sources 变化、目标值不变。按开审原文，点名条件（`(alt source)` 文本 + 父母 `{p1,p2_src}` + 表达式 `p1 * p2_src`）**会成立**。本通道 **没有**在该 digest 上再跑一遍可执行 oracle（文件在开读后、执行前被改写）。

**可执行复跑绑交卷 `edits.py` `1e5b97d6…`（365 行）。失败。**

`make_source_value_pair(t1_tiny, "p2", "2")` / `apply_alt_source_same_value(tiny, "p2")` / fixture 与 scientific `edits.jsonl` / `trace-source.prompt_text` 一致地写出：

- `kind=same_value_diff_source`（kind 仍对）
- 题干：`p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?`
- **没有** `(alt source)`
- **没有** `p2_src`；新叶为 `src_b`
- 原叶 `p2` **仍在** premises（`ids=['p1','p2','src_b']`）
- 父母：`['p1','src_b']`（相对 base `{p1,p2}` 已变，但不是点名要求的 `p2_src`）
- 表达式：`p1 * src_b`（不是 `p1 * p2_src`）
- 目标值仍为 `0`；值臂仍重算 `8`
- `rename` 对照仍是 `p2_src = 0.`、无 `(alt source)`；漂后源臂也无该标记，**不再**与 rename 在「alt-source 文本」上可区分
- `trace-source` 存在，`prompt_text` 为上述完整题干（49 token，未截断）。文本完整，但不是点名要求的 alt-source 文本。

fixture CLI：`a1301_cli_svp_alt_source` 失败，同上。scientific：`a1301_sci_source_trace_text_parents` 失败，同上。

**A13-01 点名 CE（alt-source 文本与父母）：FAIL（可执行树）。** 不得把开审源读记成冻结已关闭。不得把漂后 `src_b` 双叶图回写为声明冻结 `5413a4bc…` 的实现。

### 3.3 B9-01 独立复验（不信任作者测试）

开审冻结 `measure.py` 72–80：同事件 sham 命中后，**只有** `premise_id` 以 `sham:` 开头的标签行写 `noise_ref`；真实前提行保持 `None`。349–351：`_has_sham_row` 或 `sham_hits` 使 `noise_set=None` / `evaluated=False`，**不再**把广播后的 `real_hits` 写入 \(N\)。

1. **生产形态观测（p1 no_change + p2 changed + `sham:q` changed）。** `noise_ref`：`p1=None`，`p2=None`，`sham:q=1.0`。事件层 `null_reason=noise_set_missing`，`rho_M_excess=None`，`rho_M_noise=None`。
2. **仅 `sham:q` 行。** 同样 `noise_set_missing`。
3. **显式映射 `p3∈P\\T`、`noise_ref=1`、无 sham 行。** `rho_S_noise=1.0`，`rho_S_excess=-1.0`，`null_reason=None`。映射真实噪声前提仍入 \(N\)。
4. **手工重建旧广播（p1/p2 也被标 `noise_ref=1` 且存在 `sham:q`）。** 密度路径仍 `noise_set_missing`。双保险成立。
5. **CLI fixture sham**（`--sham-opportunities 1`，exit 0）：`(q,p2)` 的 `noise_ref=None`；`(q,sham:q)` 的 `noise_ref=0.0`（合成题干相同 → `no_change`）。`premise_id=sham:q`。不把 sham 身份写进真实前提。
6. **CLI scientific sham**（exit 0，漂后 `measure.py`）：`(q,p1)`/`(q,p2)` 的 `noise_ref=None`；`(q,sham:q)` 的 `noise_ref=1.0`（`changed`）。`null_reason=noise_set_missing`，`rho_M_excess=None`。同文件 note「sham hits are not mapped onto real premises」与数字一致。

漂后 `measure.py` 把「无 `real_hits`」一律打成 `noise_set=None`（删掉开审「0-hit → 已评估空 \(N\)」分支）。**B9-01 点名形态（changed sham / 映射 p3 / 广播）在两种实现上同结论。** 冻结判定按开审 408 行原文；可执行复跑在漂后树上再次成立。

**B9-01 点名 CE：PASS。** 作者主张「`noise_ref` 只在 `sham:`；广播不再写入 \(N\)」在开审源读与漂后执行上均成立。

### 3.4 A13-03 sham no-change excess 必须为 null

点名：存在 `sham:` 行且 outcome=`no_change`（`noise_ref=0`）时，**不得**把已评估空 \(N\) 记成 `rho_M_excess=-0.5`。

1. **库：`build_labels` + `event_density_sets`。** `p1`/`p2` 的 `noise_ref=None`，`sham:q=0.0`。`rho_M_excess is None`，`rho_M_noise is None`，`null_reason=noise_set_missing`，且 `!= -0.5`。
2. **显式标签（sham 行 `noise_ref=0`，真实行无 `noise_ref`）。** 同上。
3. **CLI fixture sham**（必然同文 `no_change`）：事件与顶层 `rho_M_excess is None`，`null_reason=noise_set_missing`。**不是** r13 的已评估空 \(N\) / `rho_M_excess=-0.5`。
4. **CLI scientific：** sham 为 `changed`，excess 仍为 null（与 B9-01 重合，不是本条的 no-change 形态）。

对照（非点名）：无 sham 行、`p3` `noise_ref=0`。开审源码走已评估空 \(N\)（`rho_S_noise=0`）。漂后树变为 `noise_set_missing`（U-18）。**不**否决 A13-03。

**A13-03 点名 CE：PASS。** 开审 `_has_sham_row` 已覆盖 sham 0-hit；漂后执行再次成立。

### 3.5 T3 prepare / 真值旗标

- 库：Hotpot `document_edit`（含 `new_answer="Spain"`）`validity=needs_truth`，`answer_spec.status=requires_independent_truth`，`ancestors(hotpot)=={}`。MuSiQue `paragraph_edit` 同旗标，`ancestors=={}`，分解节点值已清空。`_try_source_value_pair` 对 hotpot/musique/HE 返回 None。
- `python -m reasoning_diff prepare --kind hotpot --fixture tests/fixtures/t3_hotpot_one.json` → **exit 0**。`edits.kind=['document']`，无 SVP，`validity=needs_truth`，编辑题 `requires_independent_truth`。
- `--kind t3_musique` → **exit 0**。`edits.kind=['paragraph']`，无 SVP，`validity=needs_truth`，`requires_independent_truth`。记录 id `msq-9::answerable` / `msq-9::unanswerable` 不碰撞。

任务适配器文件 **未漂**。**T3 prepare / 真值旗标：PASS。**

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 A10-04 已在独立 JSON 上跑 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b` |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | 本机 tiny 解码不是科学噪声协议 |
| N-08 | 开审树干净全量 pytest | 交卷时 `measure.py` / `edits.py` / `cli.py` / 两份回归测试已漂；X-00 只绑交卷树 |
| N-09 | 在 `250055ab…` 字节上重跑 A13-01 可执行 oracle | 开读后文件已被改写；本通道不得改 `src/` 以恢复冻结 |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## / B9-## / A10-04 / A13-## 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。作者本轮主张关闭 A10-04、A13-01、A13-03。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | — | **closed** | X-03 |
| B-02 / B-23 | — | **closed** | X-04 / X-05 |
| B-08 | — | **closed** | X-11 |
| B-09 / B-24 / **B5-02** | — | **closed** | X-plus-sub |
| B-12 0-hit | — | **closed on freeze source**；漂后树见 U-18 | 开审 `else: noise_set=[]; evaluated=True`。交卷不再走该支 |
| B-13 / B-14 | — | **closed** | X-17 / X-18 |
| B-15 / **B5-01** / **A10-04** | Plus 锁持久化；仅清 RAM 后 Symbolic 仍 `test` | **closed** | §3.1。孤立 + `clear()` → `probe_train` 为诚实 |
| B-16 / **B5-03** / B-20 | T3 口述 / 祖先 | **closed** | X-20 / §3.5 |
| B-18 / **B5-05** / **A13-01** | alt-source 文本与父母 | **不能在声明冻结上关闭** | §3.2。开审源读会过；可执行复跑绑漂后树 **FAIL** |
| B-19 | — | **closed** | X-26 |
| B-22 | — | **closed** | X-p2 |
| **B5-04** / **B9-01** | sham `noise_ref` 只在 `sham:`；广播不再写入 \(N\) | **closed** | §3.3 |
| **A13-03** | `sham:` 空 \(N\) 不扣噪 | **closed** | §3.4 |
| **B6-01** | 生成区事件 | **closed**（原触发） | scientific 只解析生成区，事件均为 `q` |

未在本轮逐条复跑的 B-03/04/05/06/07/10/11/17/21/25/27：其依赖适配器文件相对开审未变；不新开，也不用作者测试回写关闭。

## 6. 发现（本轮开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

本轮 **没有** 在声明冻结 `5413a4bc…` 上新开、且能否决点名 CE 的 confirmed defect。A10-04 / B9-01 / A13-03 / T3 在未漂或开审语义上独立成立。

审查中途 `edits.py` / `measure.py` / `cli.py` / 两份回归测试被他方改写，见 §1 / §12。这是否决 **整树通过意见** 的过程缺陷。漂后树上 A13-01 点名文本/父母检查失败，**不能**回写成冻结字节上的新数据缺陷，也 **不能**把 A13-01 记为冻结已关。

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| **A10-04** | §3.1 RAM-only clear + 子进程 + CLI | U-14 规划缓存 |
| **B9-01** | §3.3 fixture `p2.noise_ref is None`；scientific `rho_M_excess is None` | U-13 空 `event_id` 回退 |
| **A13-03** | §3.4 fixture sham `no_change` → excess null，不是 −0.5 | U-18 漂后 0-hit |
| **T3 prepare / 真值旗标** | §3.5 | — |
| B-01/02/08/09/13/14/16/19/22/23；B5-02/03 | 本轮抽查 | — |
| **B6-01** | scientific 生成区仅 `q` | U-10 |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径缺协议 → null | 开审 `measure.py` 128–133 | 不否定已关的 B9-01 / A13-03。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | X-26。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-12 | `siblings=` / 文本键 / 持久化锁在 **被调用时** 正确 | `splits.py` 59–153 | 孤立 + `clear()` → `probe_train` 是诚实。 |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05。 |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `event_density_sets` | X-he。 |
| ND-21 | Plus/T3 Edit 缺核验不写 valid | 各 apply* | X-20 / X-plus-sub。 |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 124–134 | |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | `analysis.py` 215–257 | **不是缺陷。** |
| ND-26 | scientific 拒 0 事件 | `cli.py` 296–297 | |
| ND-27 | `_e_premise_ids` 跳过 `sham:` | `cli.py` 703–712 | |
| ND-28 | 约束 `\nq = <digit>` 是 tiny 可解析接口 | `generate.py` | 不是 §4.1 自然 CoT。 |
| ND-29 | `_try_source_value_pair` 跳过 T3 | `cli.py` 676–689 | |
| ND-32 | `clear_test_only_families()` 后孤立 Symbolic=`probe_train` | `splits.py` 69–73, 127–153 | ISSUES「不是 A10-04 残留」。独立同意。 |
| ND-34 | tiny 超上下文拒绝截断 | 开审 `generate.py` 124–125 | `len(prompt_ids)>96` raise。漂后 `src_b` 题干 49 token，未触发。 |

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
| U-08 | `event_density_sets` 把 `behavior_label!=1`（含 unknown）当作不在 B；`behavior_unknown` 把 M 置空 | 开审已有 `behavior_unknown`。scientific CLI M 为空。不重开 B9-01。 |
| U-10 | `parse_events` 仍把非 placeholder 前提登记为可解析实体 | 生产只喂生成区。tiny 未回显 `p1 =`。不重开 B6-01。 |
| U-12 | 开审 `same_value_diff_source` 是换 id 的单叶，不是协议级 A/B 双来源节点 | 点名 CE 要的是 `(alt source)` 文本 + remap 父母。开审源读满足；交卷改成保留 `p2`+`src_b`，见 §3.2。 |
| U-13 | 空 `event_id` fallback 仍可能把 `noise_ref=1` 的真实前提写入 N | 生产 label 行有 `event_id`。不并入已关的 B9-01。 |
| U-14 | 持久化锁写在 `.planning/research/.cache/` | 不是 run artifact；`clear()` 可删。不否决本冻结 A10-04。 |
| U-18 | 交卷 `measure.py` 把无 `real_hits` 一律打成 `noise_set_missing` | 无 sham 的 0-hit 不再写出 `rho_S_noise=0`。开审不是这样。冻结外。不并入 A13-03。 |

## 11. 测试质量对本通道的含义

**159 passed ≠ 数据/测量正确。交卷树是 160 passed，主张数字仍假。** 独立同意 **A10-04、B9-01、A13-03、T3 prepare** 可关（A10-04 绑未漂 `splits.py`；B9-01 / A13-03 开审源读与漂后执行同结论）。**不能**同意 A13-01 已关：

- 作者若只断言 `kind=same_value_diff_source` 或「父母已变」，弱于点名要求的 `(alt source)` 文本与 `p2_src` 父母/表达式。
- 夹具 `gsm8k-12` 的 `assign_split` 已是 `test`，不能单独证明 persist；本通道用 `gsm8k-1`。
- A13-03 必须查 `rho_M_excess is None` 且 `!= -0.5`，不能只查「不是 1.0」。
- 交卷加长的回归测试绑定漂后树，不能回写冻结关闭。

因此不能把 VERSION 的 159 绿回写为本通道通过。不能把交卷漂后的 `edits.py` / `measure.py` 记成声明冻结已改 U-12 / U-18。

## 12. 通道结论

数据与测量通道 **不能** 在声明冻结 `5413a4bc…` 上给出整树通过意见。**FAIL。**

1. **开审 `HASH_MATCH`（61 文件，`5413a4bc…`，0 CRLF）。交卷 `HASH_MISMATCH`（`3d0f1c10…`；oracle 中间 `3d0a0764…`）。** 按指令否决通过。结论只绑开审 digest。审查中 `edits.py`、`measure.py`、`cli.py` 与两份回归测试被他方改写；本通道未改 `src/` / `tests/` / `pyproject.toml`。连续通过计数 **不能开始**。
2. **点名 CE（独立 oracle，不信作者测试）：**
   - **A10-04 persist：PASS。** Plus `gsm8k-1`→Symbolic 同为 `test`；官方无 `original_id` 的文本键锁 test；`_TEST_ONLY_FAMILY_KEYS.clear()` 后仍 `test`（读 JSON）；全新子进程内存为 0 仍 `test`；CLI `prepare --kind gsm_plus` 后新进程 Symbolic 仍 `test`。`clear_test_only_families()` 后孤立 Symbolic 为 `probe_train`（诚实）。绑定未漂 `splits.py`。
   - **A13-01 alt-source 文本与父母：FAIL（可执行树）。** 漂后实现写出 `src_b`、保留 `p2`、题干无 `(alt source)`、父母/表达式为 `p1 * src_b`。fixture 与 scientific `trace-source` 一致。开审 `edits.py` 源读本为 `p2_src = 0 (alt source)` + 父母 `{p1,p2_src}`，**未**在该 digest 上可执行复跑，**不**记冻结关闭。
   - **B9-01：PASS。** 库级与 fixture/scientific CLI 均不把 sham 命中广播进真实前提或写入 \(N\)。`premise_id=sham:<node>`。映射 `p3` 仍入 \(N\)。scientific：`p1`/`p2` 的 `noise_ref=None`，`null_reason=noise_set_missing`，`rho_M_excess=None`。
   - **A13-03：PASS。** sham `no_change`（`noise_ref=0`）→ `rho_M_excess is None`，不是 −0.5。fixture CLI 为该形态。
   - **T3 prepare / 真值旗标：PASS。** `--kind hotpot` 与 `--kind t3_musique` 均 exit 0；口述答案 `requires_independent_truth` / `needs_truth`；`ancestors=={}`；无 `source_value_pair`。
   - **Plus 孤立数字：PASS。** `3`→`9` 不改 `13`；仅含 `13` 时拒子串 `3`。
   - **HE placeholder：PASS。** `kind=placeholder` 不进 ρ 分母。
   - **生成区事件（B6-01）：PASS。** scientific 只解析生成区，事件均为约束 `q`。
3. T1 来源隔离、有限扫描 unknown、身份不含值、Gate 未注册仍成立（ND-01–ND-34），不能抵消冻结漂移。官方全量保持 `pending_server`。Gate 0–2 未注册与 `scientific_conclusion=None` **不是缺陷。**
4. 作者 pytest 主张（159 passed）在交卷树上独立为假（160 passed）。绿测试不是本通道关闭依据。
