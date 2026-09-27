# Review B — 数据与测量（独立审查，round-14）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-14 通道报告。round-01–12 `B-data.md` 只用作待复验清单与行文格式，不作为证据。点名 CE 全部用独立 oracle 复跑，不调用作者 `test_*` 断言。

**开审冻结核验：`HASH_MATCH`。交卷：`HASH_MISMATCH`。** 按 `.planning/audits/round-14/VERSION.md` 原文脚本（POSIX relpath + `\x00` + 文件字节）独立复得 `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`（61 文件，0 CRLF），与声明一致。成文前最后一次 `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（仍 61 文件）。相对开审已变：`measure.py`（392→408）、`edits.py`（287→362）、`cli.py`（1249→1252）。`splits.py` / `events.py` / `graphs.py` / `schema.py` / 全部 `tasks/*.py` / `generate.py` / `analysis.py` 与开审同 digest。**点名 CE 中依赖未漂文件的结论绑定开审冻结字节**；B5-05 / B9-01 的库级结论在开审字节上独立成立，并在交卷漂后树再核一次（仍成立，不回写冻结关闭）。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-14） |
| review_time | `2026-09-21T02:40:00+08:00`（复算 hash / 开读）— `2026-09-21T02:46:34+08:00`（交卷复算） |
| declared_frozen_hash | `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`（`.planning/audits/round-14/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637`。61 文件。配方与 VERSION 一致。0 CRLF。 |
| 交卷复算 | **`HASH_MISMATCH`** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`。`measure.py` `b15fb8a5…`→`8ec8cf09…`（392→408）；`edits.py` `cacb63ac…`→`250055ab…`（287→362）；`cli.py` `779cedd3…`→`c1a274e2…`（1249→1252）。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（本通道只写本文件与 `.planning/audits/round-14/_b_scratch_*` 独立 oracle；审查中途的 `src/` 漂移不是本通道写入） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文/协议 §2.2–2.3、§2.6；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5 / §5.15；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02 |
| pytest_author_claim | VERSION 写 157 passed。交卷树上独立复跑 **1 failed / 158 passed / 22.91s / exit 1**（`tests/test_round06_regressions.py::test_scientific_h_is_finite_and_pairs_donor`，`donor_kind` 期望 `same_source_diff_value`、实得 `same_value_diff_source`）。绿 ≠ 正确；红也 **不是** 点名 CE 证据。该失败绑交卷树，不能回写开审冻结。 |

相对 r12 开审：本冻结已含 `splits.py` 184 行持久化锁（`40ab4021…`）与 `cli.py` A12-03 目录绑定（开审 `779cedd3…`）。`measure.py` / `edits.py` 开审 digest 与 r12 B 开审相同；交卷时被他方改写。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度调用链而通读；`fixture` = 对照适配器读完。行数/SHA-256 为 **开审 HASH_MATCH** 冻结树，除非标明交卷漂移。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 392 | `b15fb8a5bb92220f5693b01acf6b60bd6640b57449e6419cb0e7b2bc6e4b6ba6` | full 1–392 | **B9-01：** `noise_ref` 只写 `sham:` 行；`sham_hits` 先于 `real_hits`。交卷漂至 408 / `8ec8cf09…`（`behavior_unknown` / `_has_sham_row`） |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`review_export` / `merge_review`；生成区解析仍登记前提实体 |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | 祖先只返回节点键；非算术 `graph_kind` → `{}` |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf` | full 1–287 | **B5-05：** 开审 `apply_rename_edit` 改写 id/parents/expression。交卷漂至 362 / `250055ab…`（`apply_alt_source_same_value`） |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | **B5-01 / A10-04：** 内存 ∪ `.planning/research/.cache/gsm_test_only_families.json`；`clear()` 删文件；`_TEST_ONLY_FAMILY_KEYS.clear()` 只清 RAM |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | 身份、`scan_state`、placeholder |
| `src/reasoning_diff/cli.py` | 1249 | `779cedd373a8a509af8efa6cf387b9b9ec9467a842223e4d26f73e13219e060d` | callsite 158–437, 550–574, 676–712, 1154–1172 | `split_for_task` **不传 `siblings`**；`sham:` 前缀；无 `merge_review` 命令。交卷漂至 1252 / `c1a274e2…` |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844` | callsite 105–192 | 只解析 `generated=gen_text+assigned`；`parse_region=generated` |
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

夹具 SHA-256（与 r06–r12 相同）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

独立 JSON（非仓库夹具，`original_id=gsm8k-1`，题干与 Ada 夹具不同，避免文本键假绿）：`.planning/audits/round-14/_b_scratch_run/plus_gsm8k1.json` 等。审查结束时把持久化锁文件恢复为开审内容 `["gsm8k-12", "q:ada has 4 apples…"]`。

## 3. 已执行检查

独立 oracle（临时脚本，不写入 `src/` / `tests/` / `pyproject.toml`）。`splits.py` / 全部 `tasks/*.py` / `events.py` / `graphs.py` / `schema.py` 在开审与交卷间 **digest 未变**，B5-01 / A10-04 / T3 / Plus 孤立数字 / HE 分母绑定冻结。`measure.py` / `edits.py` / `cli.py` 在 fixture sham / 库级 B9-01 / B5-05 之后被改写；这些点名 API 在两种实现上同结论，冻结判定按 **开审 392/287/1249 行原文**。scientific prepare 跑在漂后 `measure.py` 上，单独标注。

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审 **HASH_MATCH** 61 文件 `1f61fd06…`。交卷 **HASH_MISMATCH** `401e509b…`。 |
| X-00 | 作者 pytest 主张 | `python -m pytest tests -q --tb=line` | 交卷树 **1 failed / 158 passed / 22.91s / exit 1**。VERSION「157 passed」**不成立**。绿 ≠ 正确。 |
| X-03 | 矩阵 `noise=None` | `dependency_densities(..., noise=None)` | `null_reason=noise_missing`。保持关闭。 |
| X-04 / X-05 | 有限扫描 / `exhaustive` | `build_labels` | 非 observed 或非穷尽 → unknown；`exhaustive`+`observed_response`+`no_change` → `behavior_label=0`；`unscanned` → unknown。 |
| X-23 | 空 `noise_set` | 集合密度 API | 未评估 → `noise_set_empty`。已评估 → `rho_S_noise=0.0`。 |
| X-12e / **B9-01** | 广播 / 仅 sham / 映射 p3 / 0-hit / CLI | 独立构造 + fixture/scientific prepare | **点名 CE 通过。** 见 §3.1。 |
| X-19 / **B5-01** / **A10-04** | 族锁 / 持久化 / RAM-only clear / 子进程 / `siblings=` | 独立 JSON（非仓库夹具） | **点名 CE 通过。** 见 §3.2。 |
| X-25 / **B5-05** | rename 重写表达式 | `make_source_value_pair(t1_tiny,"p2","2")` | **点名 CE 通过。** 见 §3.3。 |
| X-b601 / X-sci | 生成区事件 | scientific CLI | **原触发保持关闭。** 见 §3.4。scientific 跑在漂后 `measure.py`。 |
| X-18 | Plus 生产划分 | `refuse_fit_split` | `fit_eligible=False`，`split=test`；`probe_train` 拒绝。 |
| X-11 | 公式编辑 | `apply_formula_edit(..., "a", "5")` | 题干 `Ada has 5…`，answer=8。 |
| X-plus-sub | Plus 孤立数字 | 独立官方字段题干 | `3`→`9` 只改孤立 3，`13` 保留；仅 `13` 的题干拒 `3`。`needs_truth`。 |
| X-20 | T3 口述 / 祖先 | `document_edit` / `paragraph_edit` | Hotpot / MuSiQue `needs_truth` + `requires_independent_truth`。`ancestors(musique)=={}`。节点值已清空。 |
| X-26 | 官方夹具重算 | `load_igsm_snapshot` / fixture 加载器 | 官方 shape answer=9。fixture 加载器拒 official 形状。 |
| X-17 | `assign_family` | 缺 id；同 id | 缺 id 抛错。同 `family_id` 角色相同。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-t4 / X-t1cfg / X-gate / X-p2 | 四态 / 格子 / Gate / P2 | 库 API | T4 四态 placeholder；op=7 拒；三门 `unregistered`；无 `shared_premises` → `denominator_unverified`。 |
| X-21 | CLI fixture prepare + sham | `main prepare --sham-opportunities 1` | exit 0。`premise_id=sham:q`，`no_change`，`noise_ref=0.0`。真实前提 `noise_ref=None`。`edits.jsonl` 含 remap 后的 `source_value_pair`。 |
| X-t3cli | T3 prepare | `--kind hotpot`；`--kind t3_musique` | **两者 exit 0。** 见 §3.5。 |
| X-he | HE placeholder 分母 | `event_density_sets` | `kind=placeholder`，ρ 所用 premises=`[]`，`denominator_S=None`。 |

### 3.1 B9-01 独立复验（不信任作者测试）

开审冻结 `measure.py` 72–80：同事件 sham 命中后，**只有** `premise_id` 以 `sham:` 开头的标签行写 `noise_ref`；真实前提行保持 `None`。328–349：先收集 `sham_hits`，有则 `noise_set=None` / `evaluated=False`，**不再**把广播后的 `real_hits` 写入 \(N\)。

1. **生产形态观测（p1 no_change + p2 changed + `sham:q` changed）。** `noise_ref`：`p1=None`，`p2=None`，`sham:q=1.0`。事件层 `null_reason=noise_set_missing`，`rho_M_excess=None`，`rho_M_noise=None`。
2. **仅 `sham:q` 行。** 同样 `noise_set_missing`，excess 为 null。
3. **显式映射 `p3∈P\\T`、`noise_ref=1`、无 sham 行。** `rho_S_noise=1.0`，`rho_S_excess=-1.0`，`null_reason=None`。映射真实噪声前提仍入 \(N\)。
4. **0-hit 且已观察（`noise_ref=0.0`，p3∈P\\T）。** `rho_S_noise=0.0`，excess=0。未观察（全 `None`）走 `noise_set_empty`（null，不是 0）。
5. **手工重建旧广播（p1/p2 也被标 `noise_ref=1` 且存在 `sham:q`）。** 密度路径仍 `noise_set_missing`（`sham_hits` 优先）。双保险成立。
6. **空 `event_id` 回退 + 真实前提 `noise_ref=1`。** `_fallback_noise_set` 仍把 `{p1,p2}` 写入 \(N\)：`rho_M_noise=0.0`，`rho_M_excess=1.0`。生产 label 行有 `event_id`。保留为回退支（U-13），**不**否决点名 CE。
7. **CLI fixture sham**（`--sham-opportunities 1`，exit 0，跑在开审 `measure.py`）：
   - 标签：`(q,p2)` 的 `noise_ref=None`；`(q,sham:q)` 的 `noise_ref=0.0`（合成题干相同 → `no_change`）。
   - `premise_id=sham:q`。
   - 0-hit 已评估空 \(N\)：`null_reason=None`，`rho_M_noise=1.0`，`rho_M_excess=-0.5`。这是 0-hit 记账（B-12），不是把 sham 命中映射到真实前提。
   - `edits.jsonl` `same_value_diff_source`：`premise_id=['p1','p2_src']`，`expression=p1 * p2_src`。
8. **CLI scientific sham**（exit 0；**跑在交卷漂后 `measure.py`**，不回写冻结）：
   - 标签：`(q,p1)`/`(q,p2)` 的 `noise_ref=None`；`(q,sham:q)` 的 `noise_ref=1.0`。
   - sham 观测 `changed`，raw `82` vs `53`（tiny 跨 seed 抖动，不是前提编辑）。
   - 事件密度：`null_reason=noise_set_missing`，**`rho_M_noise=None`，`rho_M_excess=None`**。漂后树额外写出 `behavior_unknown=true` 并把 \(M\) 置空——这是冻结外补丁，**不能**记成冻结已改 U-08。
   - 同文件 note「sham hits are not mapped onto real premises」与数字一致。

交卷 `measure.py` 增加 `_has_sham_row`：任意 `sham:` 行（含 0-hit）也使 fallback `noise_set=None`。库级点名形态（changed sham / 映射 p3 / 广播）在漂后树上 **再次成立**。不把它当冻结关闭的新证据。

**B9-01 点名 CE：PASS。** 作者主张「`noise_ref` 只在 `sham:`；广播不再写入 \(N\)」在声明冻结上独立成立。

### 3.2 B5-01 / A10-04 独立复验（不信任作者测试）

构造独立 JSON（非仓库夹具）。仓库夹具 `original_id=gsm8k-12` 的 `assign_split("gsm8k-12")=="test"`（哈希落入 test 桶），**不能**区分族锁与偶然划分。本通道用 `gsm8k-1`（`assign_split=="probe_train"`），题干为 Bob/Cara，避免与已有缓存文本键 `q:ada has 4 apples…` 碰撞。

开审冻结 `splits.py`（184 行，未漂）：`register_test_only_family` 写内存并 `_save_persisted_locks()` 合并到 `.planning/research/.cache/gsm_test_only_families.json`；`family_locked_test` = 内存 ∪ 文件；`_TEST_ONLY_FAMILY_KEYS.clear()` **不**删文件；`clear_test_only_families()` 清内存并 `unlink` 文件。`cli.cmd_prepare` 仍不传 `siblings`。

1. **Plus `original_id=gsm8k-1` 然后 Symbolic 同 id。** Plus：`shared_gsm_family=gsm8k-1`，`fit_eligible=False`，`split=test`，持久化 `["gsm8k-1", "q:bob has 4 pears…"]`。随后 Symbolic：**`split=test`**，族键与文本键均相等。点名条件 **成立**。
2. **官方 Plus 字段（无 `original_id`，有 `seed_question`）。** Plus 族 ID 回退为 `q:` 文本键；与 Symbolic `original_id=gsm8k-1` **族 ID 不等、文本键相等**。Plus 加载后 Symbolic **锁 `test`**。点名条件 **成立**。
3. **`siblings=` 显式队列（清空持久化后）。** `split_for_task(symbolic, siblings=[plus])=="test"`；无 siblings 为 `probe_train`。无关 Plus（`gsm8k-99`）**不**锁 `gsm8k-1`。
4. **`_TEST_ONLY_FAMILY_KEYS.clear()`（只清 RAM）。** 文件仍在。`family_locked_test(...)==True`，Symbolic **`split=test`**。**A10-04 点名条件成立。**
5. **全新 Python 子进程（内存空，只读 JSON）。** stdout：`test` / `0` / `True`。点名条件 **成立**。
6. **生产 CLI：`prepare --kind gsm_plus`（独立 `gsm8k-1` JSON，exit 0）后新进程只 load Symbolic。** Plus `splits.jsonl` `role=test`；子进程 `split_for_task=test` 且 `_TEST_ONLY_FAMILY_KEYS` 长度为 0。点名生产路径 **成立**。
7. **`clear_test_only_families()` 后孤立 Symbolic（本进程无 Plus）。** `split_for_task=assign_split=probe_train`，锁文件不存在。作者主张「诚实、不是残留」：**同意**。不是 A10-04 失败。

**B5-01 点名 CE（family lock）：PASS。A10-04 持久化：PASS。** r12 的 B5-01-prod（无落盘、跨进程孤立仍 `probe_train`）在本冻结 `splits.py` 上 **关闭**。规划缓存路径与 `clear()` 可删仍记为 U-14，不否决点名 CE。

### 3.3 B5-05 独立复验

开审 `make_source_value_pair` → `apply_rename_edit({p2: p2_src})`：

- `same_value_diff_source.kind=same_value_diff_source`
- `premise_id`：`['p1','p2_src']`（不再保留 `p2`）
- `expression`：`p1 * p2_src`（**不是**表面改名残留 `p1 * p2`）
- `parents`：`['p1','p2_src']`
- 题干：`p1 = 4. p2_src = 0. What is q = p1 * p2_src?`
- 值侧 `same_source_diff_value` 重算答案 `8`；源侧答案仍 `0`

`review_export`：`review=None`、`review_status=awaiting_human`（fixture 1 条；scientific 7 条全 `awaiting_human`）。`merge_review` 按 `record_id` 回填并标 `filled`；未匹配行保持 `awaiting_human`。`cli.py` **没有** `merge_review` 子命令。

fixture / scientific `edits.jsonl` 均含 `kind=source_value_pair`；scientific `trace_ids.same_value_diff_source=trace-source`；源臂题干/表达式/父母均为 `p2_src`。

交卷 `edits.py` 把源臂改成 `apply_alt_source_same_value`（删原叶、加 `p2_src = 0 (alt source)`，并断言 required sources 变化、目标值不变）。漂后树上再核：ids/expression/parents 仍为 `p2_src` / `p1 * p2_src`。这是冻结外补丁，**不**回写 U-12 在冻结上已关。

**B5-05 点名 CE（remap expression/id/parents + awaiting/merge 库函数）：PASS。**

### 3.4 生成区事件（B6-01）

scientific prepare 七条轨迹（`trace-base` / `t0p` / `edit` / `source` / 两条 allowed edit / `sham`）全部 `parse_region=generated`，事件均为 `q`。`trace-source` 的 `start=57`（改名/换源题干更长，prompt 48）。无 `p1`/`p2`/`p2_src` 生成事件。`start >= prompt_len`。

**B6-01 原触发：保持关闭。**

### 3.5 T3 prepare 点名 CLI

- `python -m reasoning_diff prepare --fixture tests/fixtures/t3_hotpot_one.json --kind hotpot --out-dir …/hotpot_prep` → **exit 0**。`edits.jsonl`：`kind=document`，`validity=needs_truth`，`changed_premise_ids=['DocA:0','DocA:1']`。编辑题 `answer_spec.status=requires_independent_truth`。库级 `ancestors(hotpot)=={}`（`graph_kind=supporting_facts_only`）。
- `python -m reasoning_diff prepare --fixture tests/fixtures/t3_musique_pair.json --kind t3_musique --out-dir …/musique_prep` → **exit 0**。`edits.jsonl`：`kind=paragraph`，`validity=needs_truth`，`changed_premise_ids=['p0']`。编辑题 `requires_independent_truth`。库级 `ancestors(musique)=={}`（`graph_kind=composition_reference`）。编辑后 decomposition 节点值为 `""`。记录 id `msq-9::answerable` / `msq-9::unanswerable` 不碰撞。

**T3 prepare 点名：PASS。**

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 B5-01 / A10-04 已在独立 JSON 上跑 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b` |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | 本机 tiny 解码不是科学噪声协议 |
| N-08 | 开审树干净全量 pytest | 交卷时 `measure.py` / `edits.py` / `cli.py` 已漂；X-00 只绑交卷树 |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## / B6-## / B9-## / A10-04 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。作者本轮主张关闭 A10-04、B9-01，并要求在 `1f61fd06…` 上重核 B5-01/05。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-01 | — | **closed** | X-03 |
| B-02 / B-23 | — | **closed** | X-04 / X-05 |
| B-08 | — | **closed** | X-11 |
| B-09 / B-24 / **B5-02** | — | **closed** | X-plus-sub |
| B-12 0-hit | — | **closed** | X-12e 0-hit + p3 |
| B-13 / B-14 | — | **closed** | X-17 / X-18 |
| B-15 / **B5-01** | Plus 注册 family 锁，Symbolic 同族 `test` | **点名 CE closed** | X-19 / §3.2 |
| **A10-04** | Plus 锁持久化；仅清 RAM 后 Symbolic 仍 `test` | **closed** | §3.2 步骤 4–6。孤立 + `clear()` → `probe_train` 为诚实 |
| B-16 / **B5-03** / B-20 | — | **closed** | X-20 / X-t3cli |
| B-18 / **B5-05** | rename 改写 id/表达式 | **点名 CE closed** | X-25 / §3.3。冻结仍是同图改名（U-12） |
| B-19 | — | **closed** | X-26 |
| B-22 / B-26 | — | **closed** | X-p2 / X-23 |
| **B6-01** | — | **closed**（原触发） | X-b601 / X-sci |
| **B5-04** / **B6-02** / **B9-01** | sham `noise_ref` 只在 `sham:`；广播不再写入 \(N\) | **closed** | §3.1 |
| **B5-01-prod**（r12 残留） | 生产 prepare 跨进程不共组 | **closed on this freeze** | 持久化 JSON + CLI Plus 后新进程 Symbolic=`test` |

未在本轮逐条复跑的 B-03/04/05/06/07/10/11/17/21/25/27：其依赖适配器文件相对开审未变；不新开，也不用作者测试回写关闭。

## 6. 发现（本轮开放）

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

本轮 **没有** 在声明冻结 `1f61fd06…` 上新开、且能否决点名 CE 的 confirmed defect。B5-01-prod 在本冻结持久化路径上关闭。

审查中途 `measure.py` / `edits.py` / `cli.py` 被他方改写，见 §1 / §12。这是否决 **整树通过意见** 的过程缺陷，不是一条新的数据标签 bug。

B9-01 / B5-01 / A10-04 / B5-05 **不是**本轮开放缺陷。

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| **B9-01** / B6-02 广播入 \(N\) | §3.1 fixture `p2.noise_ref is None`；scientific `rho_M_excess is None` | U-13 空 `event_id` 回退 |
| **B5-01 点名 CE** | §3.2 | 无 seed→ID 表（S-06） |
| **A10-04** | §3.2 RAM-only clear + 子进程 + CLI | U-14 规划缓存 |
| **B5-01-prod** | 持久化锁 | U-14 |
| **B5-05 点名 CE** | §3.3 | U-12 冻结仍是改名；CLI 无 merge 命令 |
| **B6-01** | §3.4 | U-10 |
| B-01/02/08/09/12–14/16/19/22/23/26；B5-02/03 | 本轮抽查 | — |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径缺协议 → null | 开审 `measure.py` 126–137 | 不否定已关的 B9-01。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | X-26。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-12 | `siblings=` / 文本键 / 持久化锁在 **被调用时** 正确 | 开审 `splits.py` 59–153 | 孤立 + `clear()` → `probe_train` 是诚实。 |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05。 |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `event_density_sets` | X-he。注入 label 的 `spec` 可出现在 S 集合，但不进 ρ 分母。 |
| ND-21 | Plus/T3 Edit 缺核验不写 valid | 各 apply* | X-20 / X-plus-sub。 |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 124–134 | |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | `analysis.py` 215–257 | **不是缺陷。** |
| ND-26 | scientific 拒 0 事件 | `cli.py` 296–297 | |
| ND-27 | `_e_premise_ids` 跳过 `sham:` | `cli.py` 703–712 | |
| ND-28 | 约束 `\nq = <digit>` 是 tiny 可解析接口 | `generate.py` | 不是 §4.1 自然 CoT。 |
| ND-32 | `clear_test_only_families()` 后孤立 Symbolic=`probe_train` | `splits.py` 69–73, 127–153 | ISSUES「不是 A10-04 残留」。独立同意。 |
| ND-33 | fixture sham 0-hit 写出 `rho_M_excess=-0.5` | X-21 | 已评估空 \(N\)，不是广播。 |

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
| U-08 | 开审树上 `behavior_label!=1`（含 unknown）进入 M | 冻结 `event_density_sets` 把 `behavior_label==1` 以外都当不在 B。scientific 漂后树用 `behavior_unknown` 把 M 置空——**不在冻结内**。不重开 B9-01。 |
| U-10 | `parse_events` 仍把非 placeholder 前提登记为可解析实体 | 生产只喂生成区。tiny 未回显 `p1 =`。不重开 B6-01。 |
| U-12 | 开审 `same_value_diff_source` 仍是同图改名，不是第二来源节点 | 点名 CE 只要求 remap id/expression/parents，已满足。交卷 `apply_alt_source_same_value` 是冻结外。 |
| U-13 | 空 `event_id` fallback 仍把 `noise_ref=1` 的真实前提写入 N | 生产 label 行有 `event_id`。不并入已关的 B9-01。 |
| U-14 | 持久化锁写在 `.planning/research/.cache/` | 不是 run artifact；`clear()` 可删；跨干净 checkout 仍依赖「曾经 load 过 Plus」。不否决本冻结 A10-04 点名 CE。 |

## 11. 测试质量对本通道的含义

**157 passed ≠ 数据/测量正确。交卷树甚至没有 157 passed。** 独立同意 **B9-01、B5-01、A10-04、B5-05、B6-01、T3 prepare** 在开审冻结上可关。缺口：

- `test_plus_locks_symbolic_family_to_test` 类用例若只用仓库 `gsm8k-12`，孤立即为 `test`（哈希桶），会假绿。本通道用 `gsm8k-1` + 不同题干。
- 作者未单独断言「RAM-only clear 后仍 test」与「`clear()` 后可 probe_train」两条相反诚实路径；本通道都跑了。
- `test_source_value_pair_*` 若只查 kind，不能代替表达式/parents；本通道已独立查到 remap 成立。
- 交卷 `test_scientific_h_is_finite_and_pairs_donor` 断言 `donor_kind==same_source_diff_value`，弱于/反于 `_pair_source_value` 先试 `same_value_diff_source` 的生产顺序。这是作者测试与干预 donor 选择的问题，**不**否决 B5-05 remap。
- 作者若断言 `rho_M_excess != 1.0 or null_reason`，弱于本通道要求的「changed sham ⇒ `None` 且 `noise_set_missing`」。本通道已用更强 oracle 通过。

因此不能把 VERSION 的 157 绿回写为本通道通过。不能把交卷漂后的 `measure.py` / `edits.py` 记成声明冻结已改 U-08 / U-12。

## 12. 通道结论

数据与测量通道 **不能** 在声明冻结 `1f61fd06…` 上给出整树通过意见。**FAIL。**

1. **开审 `HASH_MATCH`（61 文件，`1f61fd06…`）。交卷 `HASH_MISMATCH`（`401e509b…`）。** 结论只绑开审 digest。审查中 `measure.py`、`edits.py`、`cli.py` 被他方改写；本通道未改 `src/` / `tests/` / `pyproject.toml`。连续通过计数 **不能开始**。
2. **点名 CE（独立 oracle，不信作者测试；绑定未漂源文件，另注漂后复核）：**
   - **B5-01 family lock：PASS。** Plus `gsm8k-1`→Symbolic 同为 `test`；官方无 `original_id` 的文本键锁 test；`siblings=` 显式队列锁 test，无关 Plus 不误锁。
   - **A10-04 persist：PASS。** `_TEST_ONLY_FAMILY_KEYS.clear()` 后 Symbolic 仍 `test`（读 JSON）。全新子进程内存为 0 仍 `test`。CLI `prepare --kind gsm_plus` 后新进程 Symbolic 仍 `test`。`clear_test_only_families()` 后孤立 Symbolic 为 `probe_train`（诚实）。
   - **B5-05：PASS。** 开审 `same_value_diff_source` 重写 `premise_id`/`parents`/`expression` 为 `p2_src` / `p1 * p2_src`；`review_export` 为 `awaiting_human`；`merge_review` 按 `record_id` 回填。fixture/scientific `edits.jsonl` 一致。
   - **B9-01：PASS。** 库级与 fixture/scientific CLI 均不把 sham 命中广播进真实前提或写入 \(N\)。`premise_id=sham:<node>`。映射 `p3` 仍入 \(N\)。scientific（漂后树）：`p1`/`p2` 的 `noise_ref=None`，`null_reason=noise_set_missing`，`rho_M_excess=None`。
   - **T3 prepare：PASS。** `--kind hotpot` 与 `--kind t3_musique` 均 exit 0；口述答案 `requires_independent_truth` / `needs_truth`；`ancestors(musique)=={}`。
   - **Plus 孤立数字：PASS。** `3`→`9` 不改 `13`；仅含 `13` 时拒子串 `3`。
   - **HE placeholder：PASS。** `kind=placeholder` 不进 ρ 分母。
   - **生成区事件（B6-01）：PASS。** scientific 只解析生成区，事件均为约束 `q`。
3. **冻结上不再确认 B5-01-prod。** 持久化锁关闭 r12 的跨进程缺口。规划缓存在 U-14，不是点名失败。
4. T1 来源隔离、有限扫描 unknown、身份不含值、Gate 未注册仍成立（ND-01–ND-33），不能抵消冻结漂移。官方全量保持 `pending_server`。Gate 0–2 未注册与 `scientific_conclusion=None` **不是缺陷。**
5. 作者 pytest 主张（157 passed）在交卷树上独立为假（1 failed / 158 passed）。该失败是干预 `donor_kind` 测试，不是本通道点名 CE。
