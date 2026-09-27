# Review B — 数据与测量（独立审查，round-15）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改任何生产代码、测试、夹具、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-15 通道报告。round-01–13 `B-data.md` 只用作待复验清单与行文格式，不作为证据。点名 CE 全部用独立 oracle 复跑，不调用作者 `test_*` 断言。审查过程中对 `.planning/research/.cache/gsm_test_only_families.json` 做了隔离清空/快照恢复；该文件不在冻结集。

**开审冻结核验：`HASH_MATCH`。交卷：`HASH_MISMATCH`。按用户规则 → 本通道 `FAIL`。** 按 `.planning/audits/round-15/VERSION.md` 原文脚本（POSIX relpath + `\x00` + 文件字节）开审独立复得 `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（61 文件，0 CRLF），与声明一致。oracle 收束时仍为该 digest。成文前最后一次复算 `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`。相对开审已变：`models/generate.py`（201→200，`07493570…`→`6e604039…`）：开审为 `cap=48` 截断题干，交卷改为 `len(prompt_ids)>96` 则拒绝。**本通道焦点** `splits.py` / `edits.py` / `measure.py` / `events.py` / 全部 `tasks/*.py` / `graphs.py` / `schema.py` / `cli.py` prepare/label **与开审同 digest**。点名 CE 绑定开审焦点字节；交卷 `generate.py` 不得记为冻结已闭。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-15） |
| review_time | `2026-09-21T02:45:00+08:00`（复算 hash / 开读）— `2026-09-21T03:20:00+08:00`（成文前最后一次复算） |
| declared_frozen_hash | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（`.planning/audits/round-15/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`。61 文件，0 CRLF。配方与 VERSION 一致。 |
| oracle 收束 | **`HASH_MATCH`** 同 digest（独立 oracle 写盘时）。 |
| 交卷复算 | **`HASH_MISMATCH`** `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`。`models/generate.py` `07493570…`→`6e604039…`（201→200）。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写 `.planning/audits/round-15/B-data.md` 与 `_b_scratch_*`；oracle 不写入 `src/` / `tests/`） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5 / §5.15；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02、T2NOOP-01、STRUCT-01、SURF-01 |
| pytest_author_claim | VERSION 写 159 passed。本通道未把作者测试当证据，未用全量绿关闭任何 CE。 |

相对 r13 开审焦点：`edits.py`（287→362，`apply_alt_source_same_value` + `(alt source)` 文本）、`measure.py`（392→408，任意 `sham:` 行不再评估空 \(N\)）、`cli.py`（1254→1252）。`splits.py` 仍 `40ab4021…`（184）。夹具字节与 r06–r13 相同。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度调用链而通读；`fixture` = 对照适配器读完。行数/SHA-256 为 **开审 HASH_MATCH** 冻结树，除非另注。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 408 | `8ec8cf09db1490978f5eacd7d90fd578cfe807bb2c6e09e2d002ae62ab83002c` | full 1–408 | **B9-01：** `noise_ref` 只写 `sham:`；**A13-03：** `_has_sham_row` → `noise_set=None`，不评估空 \(N\)；`behavior_unknown` → \(M=\emptyset\) |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | 身份不含值；`review_export` / `merge_review` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `{}` |
| `src/reasoning_diff/edits.py` | 362 | `250055ab8257ea2e24be885a389713e0c6d71c93936b44794a1ec821cf9e39db` | full 1–362 | **A13-01 / B5-05：** `apply_alt_source_same_value` 写 `(alt source)`、改父母、保值 |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | **A10-04：** RAM ∪ 磁盘锁；`siblings=` |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | 身份、`scan_state`、placeholder/spec |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | callsite | 默认 unavailable |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full | 域内评分；默认不宿主 exec |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | `t3_musique` / `t4_boundary` 别名 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `register_test_only_family` 写 RAM∪磁盘 |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 写 `shared_gsm_text`；不自己注册锁 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | callsite | 注入后祖先、`noop_proof` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | 口述答案保持 `requires_independent_truth` |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | 段落编辑清空分解值 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder；不进 ρ 分母 |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式 |
| `src/reasoning_diff/cli.py` | 1252 | `c1a274e233988aad3c3390041cd40ad5e214ade82ba7579a3c7c8fc35156a71a` | callsite 158–437, 676–716 | prepare/label；`sham:`；`split_for_task` 不传 `siblings`；`_try_source_value_pair` 跳过 T3 |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844` | callsite 105–192 | 开审：`cap=48` 截断；只解析 `generated`。**交卷 200/`6e604039…`：超 96 token 拒绝** |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169, 215–257 | P2 整数分母；Gate 未注册 → `scientific_conclusion=None` |
| `tests/test_review_regressions.py` | 399 | `c1f0236455f3f087d67a58d56e4f5d9ad7085a3300d591a372f806bb938ab7b3` | callsite | **不作为本通道证据** |
| `tests/test_round07_regressions.py` | — | 交卷树 302/`f942482f…`（未在开审逐文件核） | skip | **不信任** |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | callsite | 不作为证据 |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | callsite | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | callsite | |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c` | callsite | |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca` | callsite | |
| `tests/test_cli_pipeline.py` | 30 | `ff826b3e553f003bf134d1ef9d6c06206a7b836e15c69cd1126bc1ae6d482123` | callsite | |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | callsite | |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 r06–r13 相同，未改字节）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

未列入主表但开审纳入聚合的文件：`__init__.py` / `__main__.py` / `artifacts.py` / `baselines.py` / `interventions.py` / `io.py` / `rng.py` / `repair.py` / `transfer.py` / `models/*`（除上表 generate）/ `probes/*` / 其余测试。本通道不把它们当数据正确性证据。

## 3. 已执行检查

独立 oracle（`.planning/audits/round-15/_b_scratch_oracle.py`，不写入 `src/` / `tests/` / `pyproject.toml`）。先 `clear_test_only_families()` 隔离，用独立 JSON（非仓库夹具）构造 `gsm8k-1`（`assign_split==probe_train`）。`splits.py` / `edits.py` / `measure.py` / `events.py` / 全部 `tasks/*.py` / `cli.py` 在开审与交卷间 **digest 未变**（仅 `generate.py` 漂）。scientific CLI 跑在开审 `generate.py` `07493570…` 上。

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审 / oracle 收束 **HASH_MATCH** 61 文件 `401e509b…`，0 CRLF。交卷 **HASH_MISMATCH** `5413a4bc…`（`generate.py`）。 |
| X-00 | 作者 pytest 主张 | 未跑全量绿当证据 | VERSION「159 passed」**不是**本通道关闭依据。 |
| X-19 / **A10-04** | Plus → RAM 清；新进程；孤立 never-Plus | 独立 `gsm8k-1` JSON + 子进程 + CLI prepare | **点名 CE 通过。** 见 §3.1。 |
| X-25 / **B5-05 / A13-01** | remap 父母 + 非改名文本 + 保值 | `make_source_value_pair` / `apply_alt_source_same_value` vs `apply_rename_edit` | **点名 CE 通过。** 见 §3.2。 |
| X-12e / **B9-01** | `noise_ref` 只在 `sham:`；不广播 | 库构造 + fixture/scientific CLI | **点名 CE 通过。** 见 §3.3。 |
| X-a1303 / **A13-03** | sham no-change 不得记已评估空 \(N\)（−0.5） | 库构造 + fixture CLI `no_change` | **点名 CE 通过。** 见 §3.4。 |
| X-t3prep | T3 prepare exit 0 | `prepare --kind hotpot` / `t3_musique` | **两者 exit 0。** 见 §3.5。 |
| X-20 | Hotpot/MuSiQue 口述 | `document_edit` / `paragraph_edit` | `needs_truth` + `requires_independent_truth`。`ancestors=={}`。 |
| X-he-rho | HumanEval placeholder 进 ρ | `event_density_sets` | `denominator_S=None`，`rho_S_raw=None`。 |
| X-plus-sub | Plus 孤立数字 | 独立题干 `13`+`3` | `3`→`9` 只改孤立 3；`13` 中的 `3` 拒。`needs_truth`。 |
| X-03 | 矩阵 `noise=None` | `dependency_densities(..., noise=None)` | `null_reason=noise_missing`。 |
| X-04 / X-05 | 有限扫描 | `build_labels` | 非穷尽 → unknown；`exhaustive`+`observed_response`+`no_change` → `behavior_label=0`。 |
| X-18 | Plus 拒拟合 | `refuse_fit_split(..., "probe_train")` | 拒绝。`fit_eligible=False`。 |
| X-11 | 公式编辑 | sidecar `a`→`5` | 题干 `Ada has 5…`，answer=8。 |
| X-26 | 官方夹具重算 | `load_igsm_snapshot` / fixture 加载器 | answer=9。fixture 拒 official。 |
| X-17 | `assign_family` | 缺 id | 缺 id 抛错。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 无 value。 |
| X-t4 / X-t1cfg / X-gate / X-p2 | 四态 / 格子 / Gate / P2 | 库 API | T4 四态 placeholder；op=7 拒；三门 `unregistered`；无 `shared_premises` → `denominator_unverified`。 |
| X-svp-skip | T3/HE 跳过 SVP | `_try_source_value_pair` | hotpot/musique/HE 为 None；t1 非空。 |
| X-sci | scientific prepare + sham | `--eval-mode scientific --sham-opportunities 1` | exit 0。`parse_region=generated`，事件仅 `q`。`p1`/`p2` `noise_ref=None`，`sham:q=1.0`，`rho_M_excess=None`。 |

### 3.1 A10-04 persist 独立复验（不信任作者测试）

构造独立 JSON（非仓库夹具）。题干 `Dana has 4 plums…`。`assign_split("gsm8k-1")=="probe_train"`。仓库夹具 `gsm8k-12` 的哈希角色已是 `test`，**不能**单独证明锁。每步前 `clear_test_only_families()`，除非该步正在测残留锁。

1. **Plus `original_id=gsm8k-1` 然后 Symbolic 同 id。** Plus：`shared_gsm_family=gsm8k-1`，`shared_gsm_text=q:dana has 4 plums…`，`split_for_task=test`。随后 Symbolic：同族键、同文本键，**`split_for_task=test`**。磁盘写成 `["gsm8k-1", "q:dana has 4 plums…"]`。点名条件 **成立**。
2. **`_TEST_ONLY_FAMILY_KEYS.clear()`（仅内存）。** RAM 变 `[]`，磁盘仍有族键+文本键。`family_locked_test(...)==True`，Symbolic **仍 `test`**。点名条件 **成立**。
3. **全新 Python 子进程（库路径）。** 父进程 `load_gsm_plus` 写盘后，子进程 RAM `[]`，只加载 Symbolic：`SPLIT test`，`RAM 0`，`locked True`。点名条件 **成立**。
4. **官方 Plus 字段（无 `original_id`，有 `seed_question`）。** Plus 族 ID 回退为文本键；与 Symbolic `original_question` 规范化后 **文本键相等、族 ID 不等**（`q:eli…` vs `gsm8k-1`）。Plus 加载后 Symbolic **锁 `test`**。点名条件 **成立**。
5. **`clear_test_only_families()` 后孤立 Symbolic（本进程无 Plus）。** 锁文件删除。`split_for_task=probe_train`，与 `assign_split("gsm8k-1")` 一致。作者主张「诚实」：**成立。不是缺陷。**
6. **`siblings=`。** 清空后 `split_for_task(symbolic, siblings=[plus])=="test"`；无 siblings 为 `probe_train`。无关 Plus `gsm8k-99` **不**锁 `gsm8k-1`。
7. **生产 CLI（隔离复跑）。** `prepare --kind gsm_plus` exit 0，磁盘 `["gsm8k-1", "q:dana…"]`。新进程只加载 Symbolic：`role=test`，`ram=0`，`locked=true`。点名条件 **成立**。捆绑 oracle 里同序检查曾一次得到 `probe_train`：当时共享锁文件被并行进程写成/清成 `["gsm8k-12", "q:ada has 4 apples…"]`。隔离复跑通过，**不**升格为 A10-04 残留。见 U-16。
8. **FEATURES / DATA-03 残余：** 无 `seed_question`→GSM8K ID 对照表。官方 dump 文本若与 Symbolic `original_question` 规范化后不一致，文本键仍拆族。`cmd_prepare` 仍不传 `siblings=`；现由磁盘锁补齐「先 Plus、后新进程 Symbolic」。

**A10-04 persist 点名 CE：PASS。** 从未登记 Plus 的孤立 Symbolic 进 `probe_train` **不是缺陷**。

### 3.2 B5-05 / A13-01 独立复验（非改名）

`make_source_value_pair(t1_tiny, "p2", "2")` 与 `apply_alt_source_same_value(tiny, "p2")`：

- `kind=same_value_diff_source`（**不是** `rename`）
- `premise_id`：`['p1','p2_src']`（不再保留 `p2`）
- `expression`：`p1 * p2_src`
- `parents`：`['p1','p2_src']`；基图 `['p1','p2']`；`required_sources_before != required_sources_after`
- **题干（源臂）：** `p1 = 4. p2_src = 0 (alt source). What is q = p1 * p2_src?`
- **对照 `apply_rename_edit({"p2":"p2_src"})`：** `p1 = 4. p2_src = 0. What is q = p1 * p2_src?` —— **无** `(alt source)`，两题干不等。点名「不是 rename-only」**成立**。
- **值不变：** `p2_src` 值 `0` = 原 `p2`；`p1` 仍 `4`；答案仍 `0`；节点 `q` 值仍 `0`；`before[p2]==after[p2_src]=="0"`；`metadata.values_unchanged=True`
- 值臂 `same_source_diff_value` 重算答案 `8`

`review_export`：`review=None`、`review_status=awaiting_human`。`merge_review` 按 `record_id` 回填 `filled`。CLI **没有** `merge_review` 子命令。

fixture prepare `edits.jsonl` 的 `source_value_pair`：题干同样含 `(alt source)`，父母 `['p1','p2_src']`，表达式 `p1 * p2_src`。

图上仍只有一个来源节点改名+标注，**没有**协议级第二来源节点 A/B。

**B5-05 / A13-01 点名 CE（remap parents + 独立 alt-source 文本 + 保值）：PASS。** 协议级 A/B 双来源图：仍未实现（U-12，不重开点名 CE）。

### 3.3 B9-01 不广播

**格式：** fixture / scientific 的 sham `premise_id` 均为 `sham:q`。**成立。**

**库：p1 no_change + p2 changed + `sham:q` changed。** `noise_ref`：`p1=None`，`p2=None`，`sham:q=1.0`。事件层 `null_reason=noise_set_missing`，`rho_M_excess=None`。**成立。**

**仅 `sham:q` 行。** 同样 `noise_set_missing`。**成立。**

**映射真实前提 `p3∈P\\T`、`noise_ref=1`、无 sham 行。** `rho_S_noise=1.0`，excess=−1，`null_reason=None`。映射真实噪声前提仍入 \(N\)。**成立。**

**手工重建旧广播**（p1/p2 也被标 `noise_ref=1` 且存在 `sham:q`）：密度路径仍 `noise_set_missing`（`_has_sham_row` 优先）。

**CLI scientific**（`--eval-mode scientific --sham-opportunities 1`，exit 0）：
- 标签：`p1=None`，`p2=None`，`sham:q=1.0`（命中 `changed`）
- 事件密度：`null_reason=noise_set_missing`，**`rho_M_excess=None`**
- 七条轨迹 `parse_region=generated`，事件均为 `q`

**CLI fixture sham：** `sham:q` `noise_ref=0.0`（同文 `no_change`），出现的真实前提 `p2=None`。不广播。

**点名 CE B9-01：PASS**（只写 `sham:`；不广播进真实前提；未映射命中 missing；映射 `p3` 仍入 \(N\)）。

### 3.4 A13-03：sham no-change → `rho_M_excess` 为 null

r13 冻结上，fixture sham miss 走「已观察、无 `noise_ref==1`」→ 已评估空 \(N\) → `rho_M_noise=1.0`，`rho_M_excess=-0.5`（\(T=\{p1,p2\}\)，\(B=\{p2\}\)，\(\rho_M=0.5\)，空 \(N\) 的 \(\rho_M^{noise}=1\)）。

本冻结 `measure.py` 349–351：任意 `sham:` 行（含 `noise_ref=0.0`）→ `noise_set=None`，`evaluated=False` → `null_reason=noise_set_missing`。

1. **库：已知行为 + sham no-change。** `build_labels`：`p1=None`，`p2=None`，`sham:q=0.0`。`event_density_sets`：`rho_M_raw=0.5`（\(M=\{p1\}\)，**不是** unknown 抹掉 \(M\)），**`rho_M_excess=None`**，`rho_M_noise=None`，`null_reason=noise_set_missing`。**不是 −0.5。** 点名条件 **成立**。
2. **显式标签**（p1/p2 无 `noise_ref`，`sham:q=0.0`）：同样 excess null。
3. **对照：无 sham 行的 0-hit**（`p3` `noise_ref=0`）：`rho_S_noise=0.0`，`null_reason=None`。A13-03 只约束 `sham:` 行，不禁止真实 0-hit 记账。
4. **CLI fixture `--sham-opportunities 1`：** sham 观测 `no_change`。密度 `rho_M_excess=None`（顶层亦 None），`null_reason=noise_set_missing`。**不是 −0.5。** 该 CLI 行同时 `behavior_unknown=true`（只标了 p2，\(T\not\subseteq\) known）——库路径（上条）才是「有 \(M\) 但不扣空 \(N\)」的干净证据。

**A13-03 点名 CE：PASS。** 作者主张「任意 `sham:` 行（含 no-change）不把空 \(N\) 当已评估扣除」在开审 `measure.py` `8ec8cf09…` 上独立成立。

### 3.5 T3 prepare / 口述 / HE ρ

`--kind hotpot` → exit 0，`edits.kind=['document']`，`validity=needs_truth`，无 SVP。  
`--kind t3_musique` → exit 0，`edits.kind=['paragraph']`，`validity=needs_truth`，无 SVP。  
`document_edit(..., new_answer="Spain")` 与默认口述替换：`validity=needs_truth`，`status=requires_independent_truth`。  
`paragraph_edit`：同样 `needs_truth` / `requires_independent_truth`；节点值已清空。  
`ancestors(hotpot)=={}`，`ancestors(musique)=={}`（`graph_kind` 为 supporting_facts_only / composition_reference）。  
HumanEval 前提 `kind=placeholder`，过滤后 P 为空，`denominator_S=None`，`rho_S_raw=None`。`_try_source_value_pair(he)==None`。

**T3 / 口述 / HE ρ：PASS。**

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
| N-08 | 交卷树干净全量 pytest | 不把绿测试当论文正确性；`generate.py` 已漂 |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / B5-## / A10-04 / A13-## 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。作者本轮主张关闭 A13-01 / A13-03 / A10-04 / B9-01。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| B-15 / **B5-01** / **A10-04** | persist 锁：仅清 RAM 后仍 test；新进程仍 test；孤立可 probe_train | **closed**（绑定开审 `splits.py`） | X-19 / §3.1 |
| B-18 / **B5-05** / **A13-01** | 改父母 + 独立 alt-source 文本 + 保值；不是 rename-only | **closed** | X-25 / §3.2 |
| **B5-04** / **B9-01** | sham `noise_ref` 只在 `sham:`；不广播进真实 \(N\) | **closed** | §3.3 / X-sci |
| **A13-03** | 任意 `sham:` 行（含 no-change）不评估空 \(N\)，excess 不为 −0.5 | **closed** | §3.4 |
| B-16 / **B5-03** / B-20 | Hotpot/MuSiQue 口述 `needs_truth`；祖先空 | **closed** | X-20 / X-t3prep |
| B-17 | HE placeholder 不进 ρ | **closed** | X-he-rho |
| E7-19 T3 prepare | 不再强制 SVP | **closed** | X-t3prep |
| B-01 / B-02 / B-08 / B-09 / B-13 / B-14 / B-19 / B-23 / B-26 | — | **closed**（抽查） | X-03 / X-04 / X-11 / X-plus-sub / X-17 / X-18 / X-26 |
| **A13-02** | 未知 → \(M=\emptyset\)，`rho_M_*=null` | **未作本通道点名关闭**（ISSUES 标 A/C） | fixture CLI 见到 `behavior_unknown=true`；库 A13-03 路径上 \(M=\{p1\}\) 仍算出 `rho_M_raw=0.5` |

## 6. 发现（本轮开放）

本轮在声明冻结的数据/测量焦点文件上 **没有新的 confirmed defect**。交卷 `generate.py` 漂离使整树冻结作废，按用户规则通道失败。下列不升格为数据 CE。

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect suggestion`。

（空。开放项见 §10 / §9。）

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| **A10-04 persist** | §3.1 | 无 seed→ID 表；锁文件在 `.planning`；并行 prepare 可互清 |
| **A13-01 / B5-05** | §3.2 | U-12 A/B 图；CLI 无 merge 命令 |
| **A13-03** | §3.4 | 无 sham 的真实 0-hit 仍评估空/零 \(N\)（有意） |
| **B9-01** | §3.3 | U-13 空 `event_id` 回退未在本轮重做 |
| **E7-19 / B5-03 / B-17** | §3.5 | 口述值仍可写入，status 已诚实 |

## 8. 已确认非缺陷（non-defect suggestion）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | X-26。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–22 | 非算术 `graph_kind` → `{}`。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-15 | 非穷尽 no_change 不记已知行为 | `build_labels` | X-04/X-05。 |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `event_density_sets` | X-he-rho。 |
| ND-21 | Plus/T3 Edit 缺核验不写 valid | 各 apply* | X-20 / X-plus-sub。 |
| ND-22 | P2 整数分母拒绝计算 | `analysis.py` 124–134 | |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | `analysis.py` 215–257 | **不是缺陷。** |
| ND-26 | scientific 拒 0 事件 | `cli.py` 296–297 | |
| ND-27 | `_e_premise_ids` 跳过 `sham:` | `cli.py` 703–712 | |
| ND-29 | `_try_source_value_pair` 跳过 T3 | `cli.py` 676–689 | 关闭 E7-19。 |
| ND-30 | 磁盘 ∪ RAM 锁在 **被调用时** 正确 | `splits.py` 59–78, 127–153 | 关闭 A10-04。孤立无 Plus 进 `probe_train` 是诚实。 |
| ND-32 | 夹具 `gsm8k-12` 的 `assign_split` 已是 `test` | `splits.assign_split` | 不能用夹具 CLI 单独证明 persist；`gsm8k-1` 才是 probe_train。 |
| ND-33 | 任意 `sham:` 行（含 miss）不评估空 \(N\) | `measure.py` 309–351 | 关闭 A13-03。与无 sham 的真实 0-hit 可并存。 |
| ND-34 | `same_value_diff_source` 文本含 `(alt source)` | `edits.py` 219–289 | 关闭 A13-01；与 `apply_rename_edit` 题干可区分。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；tiny 命中不能当协议命中率 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 / FEATURES T2 | 文本键机制已测；dump 上格式差仍会拆族 |
| S-07 | Linux cgroup / 容器隔离执行器 | EXEC-01 / GOAL §5.15 | 本机仅 Unavailable + 非沙箱子进程 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-08 | `behavior_label!=1`（含 unknown）进入 M 的旧路径 | 本冻结 `behavior_unknown` 可把 \(M\) 置空。A13-02 非本通道点名。库 A13-03 路径上已知行为仍算出 \(M=\{p1\}\)。 |
| U-10 | `parse_events` 仍把非 placeholder 前提登记为可解析实体 | 生产 scientific 只喂生成区。不重开 B6-01。 |
| U-12 | `same_value_diff_source` 仍是同图换叶 + `(alt source)` 标注，不是第二来源节点 | 点名 CE 要求 remap + 非改名文本 + 保值，已满足。 |
| U-14 | 无 `seed_question`→GSM8K ID 表 | 点名 CE 只要求共享文本键/族锁，已满足。 |
| U-16 | persist 路径写死为仓库 `.planning/research/.cache/` | 可复查、跨进程有效。并行审查/prepare 会互清或互写该 JSON。隔离复跑仍通过。 |
| U-17 | 并行 prepare 同时读写锁 JSON | 无文件锁。捆绑 oracle 一次 CLI persist 假阴，隔离复跑真阳。不否决 A10-04。 |
| U-18 | 交卷 `generate.py` 拒绝超 96 token 的 tiny prompt | 不在本通道点名 CE。开审 scientific 用短 T1 题干，未触发。不得回写冻结关闭。 |

## 11. 测试质量对本通道的含义

**159 passed ≠ 数据/测量正确。** 独立同意 **A10-04、A13-01/B5-05、A13-03、B9-01、T3/HE** 在 **开审焦点文件** 上可关。作者测试仍不能替代：

- persist 必须自己构造 `gsm8k-1`（夹具 `gsm8k-12` 的哈希角色已是 `test`）。
- 必须测「只清 RAM」「全新子进程 RAM 为空」「`clear_test_only_families` 后诚实 `probe_train`」。
- A13-01 必须同时查 `parents`、题干是否含 `(alt source)`、以及与 `apply_rename_edit` 的差异；不能只查 kind。
- A13-03 必须在 **已知行为** 下构造 sham no-change，确认 `rho_M_excess is None` 且 **不是** −0.5；不能只看 CLI fixture 的 `behavior_unknown`。
- B9-01 必须查 p1/p2 的 `noise_ref is None`。
- 交卷 `generate.py` 与可能漂后的 `test_round07_regressions.py` 不能回写冻结关闭。

## 12. 通道结论

数据与测量通道 **不能** 在声明冻结 `401e509b…` 上给出整树通过意见。**FAIL。**

1. **开审 `HASH_MATCH`（61 文件，0 CRLF）。oracle 收束仍 `HASH_MATCH`。交卷 `HASH_MISMATCH`（`5413a4bc…`）。** 用户规则：HASH_MISMATCH → FAIL。漂移文件：`models/generate.py`（201/`07493570…` → 200/`6e604039…`）。`splits.py` / `edits.py` / `measure.py` / `events.py` / `cli.py` / 全部 `tasks/*.py` 未变。连续通过计数 **不能开始**。
2. **点名 CE（独立 oracle，不信作者测试；绑定开审焦点字节）：**
   - **A10-04 persist：PASS。** Plus `gsm8k-1`→Symbolic 同为 `test`；仅清 RAM 后仍 test（磁盘）；全新子进程 RAM 空仍 test；CLI Plus 后新进程 Symbolic 仍 test（隔离复跑）；`clear` 后孤立 Symbolic 为 `probe_train`（诚实）。
   - **B5-05 / A13-01：PASS。** `same_value_diff_source` 重写父母/表达式为 `p2_src` / `p1 * p2_src`；题干为 `p2_src = 0 (alt source)`，与 rename-only `p2_src = 0` 可区分；值与答案不变。
   - **B9-01：PASS。** `noise_ref` 只在 `sham:`；scientific `p1`/`p2` 为 None，`sham:q=1.0`，`rho_M_excess=None`。
   - **A13-03：PASS。** 库路径 sham no-change：`rho_M_raw=0.5` 且 **`rho_M_excess is None`**（不是 −0.5）。CLI fixture sham miss 同样 excess null。
   - **T3 `prepare --kind hotpot` / `t3_musique` exit 0：PASS。** 口述保持 `needs_truth` / `requires_independent_truth`。HE placeholder 不进 ρ 分母。
3. **无新的数据/测量 confirmed defect。** 通道失败原因是整树冻结漂离，不是点名 CE 失败。
4. 官方全量保持 `pending_server`。Gate 0–2 未注册与 `scientific_conclusion=None` **不是缺陷。** 从未加载 Plus 的孤立 Symbolic 进 `probe_train` **不是缺陷。** FEATURES 的 seed→ID 表仍缺（U-14 / S-06），不推翻点名 CE。
