# Review B — 数据与测量（独立审查，round-17）

本报告不假设实现正确，不把 `ISSUES.md` 的作者关闭当作已关闭。未修改 `src/`、`tests/`、`pyproject.toml` 或论文。未下载数据或权重。未阅读其他 round-17 通道报告。round-01–15 `B-data.md` 只用作待复验清单与行文格式，不作为证据。点名检查全部用 `.planning/audits/round-17/_b_scratch/` 独立 oracle 复跑，**不 import 任何 `tests.test_*` 模块**。审查中途对共享锁 `.planning/research/.cache/gsm_test_only_families.json` 做了快照/清空/恢复；交卷时该文件不存在（与开审一致）。该锁不在冻结集。

**开审冻结核验：`HASH_MATCH`。交卷：`HASH_MISMATCH`。按用户规则 → 本通道 `FAIL`。** 按 `.planning/audits/round-17/VERSION.md` 原文脚本（POSIX relpath + `\x00` + 文件字节）开审独立复得 `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（61 文件，0 CRLF），与声明一致。oracle 开跑与成文前最后一次复算均为 `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`（仍 61 文件，0 CRLF）。本通道未改冻结集。mtime 显示开审后被他方改写：`src/reasoning_diff/cli.py`（02:57:30）、`tests/test_round07_regressions.py`（02:57:36）。点名 CE 中依赖 `edits.py` / `measure.py` / `splits.py` / `events.py` / `graphs.py` / `schema.py` / 全部 `tasks/*.py` 的结论绑定开审焦点字节（这些文件 mtime 早于开审复算）。CLI / A12-03 / E 列 / persist-CLI 在交卷 `cli.py` 上复跑仍成立，**不得回写声明冻结已闭**。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道，round-17） |
| review_time | `2026-09-21T02:56:00+08:00`（复算 hash / 开读）— `2026-09-21T03:03:00+08:00`（成文前最后一次复算） |
| declared_frozen_hash | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（`.planning/audits/round-17/VERSION.md`，61 文件） |
| 开审复算 | **`HASH_MATCH`** `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`。61 文件，0 CRLF。配方与 VERSION 一致。 |
| oracle 开跑 / 交卷复算 | **`HASH_MISMATCH`** `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`。61 文件，0 CRLF。 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；勿把 HEAD 当冻结） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否（只写 `.planning/audits/round-17/B-data.md` 与 `_b_scratch/`；oracle 不写入 `src/` / `tests/`） |
| ISSUES.md | 仅作作者主张清单；每条须独立 oracle 才能关闭 |
| 对照文本 | 论文 §2.2–2.3、§2.6、§7 数据；`docs/EXPERIMENT_PROTOCOL.md` §1–3 / §6；GOAL §5.1–5.5；`REQUIREMENTS.md` DATA-01/02/03、MEAS-01/02、T2NOOP-01、STRUCT-01 |
| pytest_author_claim | VERSION 写 160 passed。本通道独立复跑 **`162 passed in 24.54s` / exit 0**。绿测试 **不是** 论文正确性，也 **不是** 点名 CE 关闭依据。作者计数过时。 |

相对 r15 开审焦点（本冻结已含 A14-02/04）：`edits.py` 365 / `1e5b97d6…`（保留叶 *a* + 追加 `src_b`）；`measure.py` 405 / `985b9d93…`（`noise_ref=0` 且无 `sham:` 不再评估空 \(N\)）；`splits.py` 仍 `40ab4021…`（184）。夹具字节与 r06–r15 相同。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对 prepare/label/划分/密度调用链而通读；`fixture` = 对照适配器读完。行数/SHA-256 为 **交卷树**（oracle `file_hashes`）。标「开审后漂」的文件不得当作声明冻结字节。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 405 | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | full 1–405 | **A13-02：** `behavior_unknown` → \(M=\emptyset\)；**A13-03：** `_has_sham_row` → `noise_set=None`；**A14-04：** 真实前提 `noise_ref=0` 且无 sham → 不评估空 \(N\) |
| `src/reasoning_diff/edits.py` | 365 | `1e5b97d63a62ab78a43ee9db33594a2cc1de3add5ad25aac81007b05af3efb91` | full 1–365 | **A14-02：** `apply_alt_source_same_value` 保留 *a*、追加等值 `src_b`、父母/表达式改读 *b* |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full 1–274 | `EventIdentity.key()` 无 value；`review_export` / `merge_review` |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full 1–46 | `composition_reference` / `supporting_facts_only` / `none` → `{}` |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full 1–184 | **A10-04：** RAM ∪ 磁盘锁；`clear()` 删文件；六角色 |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full | 身份、`SPLIT_ROLES`、`GRAPH_STATUSES`、placeholder/spec |
| `src/reasoning_diff/cli.py` | 1260 | `9431b7768fda6a3c3c577f811b747f57f79f57b111dfe89c12281d1d23f95bb5` | callsite 158–437, 550–720, 780–786 | **开审后漂。** prepare/label；`sham:`；**A12-03** `_find_tasks_jsonl`；**E 列** `_e_premise_ids`；`_try_source_value_pair` 跳过 T3 |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | callsite | 默认 unavailable |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full | 域内评分 |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full | `t3_musique` / `t4_boundary` 别名 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full | template≠G、加载重算核对 |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full | `register_test_only_family` 写 RAM∪磁盘；solution 不是 DAG |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full | 写 `shared_gsm_*`；不自己注册锁 |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full | 注入后祖先、`noop_proof` |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full | supporting_facts 不是完整 DAG |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full | composition_reference；`ancestors=={}` |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full | placeholder；参考 DFG 不是任务 DAG |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full | 四态显式 |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173` | callsite | scientific 只解析 generated |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38` | callsite 72–83 | E 行按传入 `premises` 顺序 |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | callsite 114–169, 215–257 | P2 整数分母；Gate 未注册 |
| `tests/test_round07_regressions.py` | 342 | `8c23db4b637c8c7013f9f93564ed28d97bd7b7bd1302f72f75089e0ceace29de` | skip | **开审后漂。不作为本通道证据。** |
| `tests/*.py`（其余） | — | 见 `_b_scratch/report.json` | skip | **不 import、不当证据** |
| `tests/fixtures/*.json` | — | 见下表 | fixture | |

夹具 SHA-256（与 r06–r15 相同，未改字节）：`t1_tiny.json` `3267db38…`；`t1_official_shape.json` `2fbf6773…`；`t1_ops_config.json` `bc08ae65…`；`t2_symbolic_one.json` `481f654e…`；`t2_formula_sidecar.json` `8a014940…`；`t2_gsmplus_one.json` `86bdeb66…`；`t3_hotpot_one.json` `6821c1e1…`；`t3_musique_pair.json` `d65a90c9…`；`t3_humaneval_one.json` `31bd1371…`；`t4_boundary.json` `c5426cbd…`。

独立 JSON（非仓库夹具）：`_b_scratch/plus_gsm8k1.json` / `sym_gsm8k1.json`（`original_id=gsm8k-1`，Dana/plums，避免 Ada/`gsm8k-12` 哈希角色已是 `test` 的假绿）；`plus_seed_only.json` / `sym_eli.json`（无 `original_id` 的官方 Plus 字段）。

未列入主表但纳入聚合的文件：`__init__.py` / `__main__.py` / `artifacts.py` / `baselines.py` / `interventions.py` / `io.py` / `rng.py` / `repair.py` / `transfer.py` / `models/*` / `probes/*`。本通道不把它们当数据正确性证据。

## 3. 已执行检查

独立 oracle：`.planning/audits/round-17/_b_scratch/oracle.py` + `persist_child.py`。138/138 子断言通过，0 crash。不调用作者 `test_*`。

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-hash | VERSION 原文复算 | POSIX relpath + NUL + bytes | 开审 **HASH_MATCH** `3d0a0764…`。oracle/交卷 **HASH_MISMATCH** `3d0f1c10…`。 |
| X-00 | 作者 pytest 主张 | `python -m pytest -q --tb=line` | **162 passed / 24.54s / exit 0**。VERSION「160 passed」不成立。绿 ≠ 正确。 |
| X-srcb / **A14-02** | 保留 *a* + 等值 `src_b`；父母/表达式改读 *b*；≠ rename | `make_source_value_pair` / `apply_alt_source_same_value` vs `apply_rename_edit` | **点名 CE 通过。** 见 §3.1。 |
| X-a1302 / **A13-02** | 未知/未扫描不得进 \(M\) | `build_labels` + `event_density_sets` + 直接 API | **点名 CE 通过。** 见 §3.2。 |
| X-a1303 / **A13-03** | 任意 `sham:` 行（change / no-change）`noise_set=None` | 库构造 + fixture/scientific CLI | **点名 CE 通过。** 见 §3.3。 |
| X-a1404 / **A14-04** | 真实前提 `noise_ref=0`、无 sham 行，不得评估空 \(N\) | 手工构造 `Label`（不经 `build_labels`） | **点名 CE 通过。** 见 §3.4。 |
| X-a1203 / **A12-03** | `_find_tasks_jsonl` 只读 `Path(folder)/"tasks.jsonl"` | `inspect` + 独立目录树 | **点名 CE 通过。** 见 §3.5。 |
| X-e | E 列跟 `task.premises` 序，不跟 first-seen labels | `_e_premise_ids` 逆序前提 | **点名 CE 通过。** 见 §3.6。 |
| X-19 / **A10-04** | Plus 锁：清 RAM 仍 test；新进程仍 test；孤立可 probe_train | 独立 `gsm8k-1` JSON + 子进程 + CLI | **点名 CE 通过。** 见 §3.7。独立同意孤立 Symbolic **不是** A10-04 残留。 |
| X-t2t3 | T2/T3 不得从答案 / supporting facts / 参考 DFG / CoT 冒充完整 DAG | 适配器 + `ancestors` | **点名 CE 通过。** 见 §3.8。 |
| X-id | 身份不含值 | `EventIdentity("q",1,"global").key()` | JSON 仅 entity/version/scope。 |
| X-sm | S/M 分开；原始/参照/signed excess；负差不截 | `dependency_densities` | \(\rho_S^{ex}=-1\)、\(\rho_M^{ex}=-0.5\)。矩阵 `noise=None` → `noise_missing`。 |
| X-split | 六角色 | `SPLIT_ROLES` + 400 id | 六角色齐；`assign_family` 缺 id 抛错；`gsm8k-1=probe_train`，`gsm8k-12=test`。 |
| X-t3prep | T3 prepare | `prepare --kind hotpot` / `t3_musique` | 两者 exit 0；无 SVP。 |
| X-20 | 口述 / 祖先 | `document_edit` / `paragraph_edit` | `needs_truth` + `requires_independent_truth`。`ancestors=={}`。 |
| X-he-rho | HE placeholder 进 ρ | `event_density_sets` | `denominator_S=None`，`rho_S_raw=None`。 |
| X-plus-sub | Plus 孤立数字 | 独立题干 | `4`→`9` 只改孤立 4；题干无孤立 `3` 则拒。`needs_truth`。 |
| X-11 | 公式编辑 | sidecar `a`→`5` | `Ada has 5…`，answer=8。无 sidecar 拒编辑。 |
| X-26 | 官方/夹具隔离 | `load_igsm_snapshot` / `load_t1_fixture` | 官方 answer=9，忽略 G/lookup。夹具拒 official 形状；官方加载器拒 fixture。 |
| X-18 | Plus 拒拟合 | `refuse_fit_split(..., "probe_train")` | 拒绝。`fit_eligible=False`。 |
| X-04 | 有限扫描 | `build_labels` | `unscanned` / `unknown` / `no_response_observed_in_scan` → unknown。穷尽 `observed_response`+`no_change` 才记 0。 |
| X-t4 / X-t1cfg | 四态 / 格子 | 库 API | T4 四态 placeholder；op=7 拒。 |
| X-svp-skip | T3/HE 跳过 SVP | `_try_source_value_pair` | hotpot/musique/HE 为 None；t1 非空。 |
| X-sci | scientific prepare + sham | `--eval-mode scientific --sham-opportunities 1 --split-fractions …` | exit 0。7 条轨迹 `parse_region=generated`。`p1`/`p2` `noise_ref=None`，`sham:q=1.0`，`noise_set_missing`，\(M=\emptyset\)。 |
| X-rev | 复核导出 | `review_export` | `review=None`，`review_status=awaiting_human`。 |

### 3.1 A14-02 / same_value_diff_source（保留 *a* + `src_b`）

`make_source_value_pair(t1_tiny, "p2", "2")` 与 `apply_alt_source_same_value(tiny, "p2")`：

- `kind=same_value_diff_source`（**不是** `rename`）
- 前提 ID：`['p1','p2','src_b']` — **保留叶 *a*=p2**，追加等值 **`src_b`**
- `src_b.value == p2.value == "0"`；`p1` 仍 `4`；答案仍 `0`；节点 `q` 值仍 `0`
- `parents=['p1','src_b']`；`expression='p1 * src_b'`；`ancestors(q)={p1,src_b}`；**p2 不再是目标父母**
- 题干：`p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?`（*a* 与 *b* 同时在场）
- 对照 `apply_rename_edit({"p2":"src_b"})`：前提变为 `['p1','src_b']`，**丢掉 p2**；题干不含并列的 `p2 = 0`。两题干不等，kind 不等。点名「必须不同于 rename」**成立**。
- 值臂 `same_source_diff_value` 重算答案 `8`

fixture CLI `edits.jsonl` 的 `source_value_pair`：同样保留 `p2`+`src_b`，父母 `['p1','src_b']`，表达式 `p1 * src_b`。

图上是「保留旧叶 + 新增等值叶并改读」，不是协议级两个并行必读来源节点。见 U-12。

**A14-02 点名 CE：PASS。**

### 3.2 A13-02：未知 / 未扫描不得进入 \(M\)

1. **只扫描 p2（changed），p1 无观测。** `event_density_sets`：`behavior_unknown=true`，**`M=[]`**，`rho_M_raw=None`。单前提扫描不能把未扫祖先记成漏读。
2. **p1 `no_change` + `scan_state=unscanned`。** `behavior_known=False`，`behavior_label=None`。密度路径仍 unknown，**M 不是 {p1}**。
3. **`scan_state=unknown` / `no_response_observed_in_scan`**（即使 `exhaustive=True`）→ 不记已知负例。
4. **直接 API** `behavior_unknown=True`：`M=[]`，`rho_M_raw=None`。
5. **对照：已知 miss**（p1=0 且 `behavior_known`，p2=1，\(T\subseteq\) known）：`M=['p1']`。A13-02 不禁止已知漏读。
6. **scientific CLI**：只标了编辑前提，`behavior_unknown=true`，`M=[]`，`rho_M_raw=None`。

**A13-02 点名 CE：PASS。**

### 3.3 A13-03：任意 `sham:` 行保持 `noise_set=None`

库路径（已知行为 + `sham:q`）：

- `outcome=no_change`：真实前提 `noise_ref=None`，`sham:q=0.0`，`noise_set=None`，`rho_M_excess is None`（**不是 −0.5**）
- `outcome=changed`：同样 `noise_set=None`，excess null

fixture CLI：`sham:q` `noise_ref=0.0`（同文 no-edit），出现的真实前提 `p2=None`。密度 `noise_set` 全 None。

scientific CLI：`sham:q=1.0`（seed=2 命中 change），`p1`/`p2=None`，`null_reason=noise_set_missing`。

**A13-03 点名 CE：PASS。**

### 3.4 A14-04：真实前提 `noise_ref=0`、无 sham 行，不得评估空 \(N\)

手工构造（不经 `build_labels`）：

```
Label(q,p1, task=1, beh=0, known, noise_ref=0.0)
Label(q,p2, task=1, beh=1, known, noise_ref=0.0)
```

无 `sham:` 行。`event_density_sets`：`noise_set=None`，`rho_S_noise=None`，`rho_M_noise=None`，`null_reason=noise_set_missing`。**不是** 已评估空 \(N\)（旧路径会写出 `rho_S_noise=0.0` / `rho_M_noise=1.0`）。

空 `event_id` 走 fallback：同样 noise/excess 全 null。

对照：映射真实噪声前提 `p3` 且 `noise_ref=1`、无 sham：`rho_S_noise=1.0`，`rho_S_excess=0.0`，`rho_M_excess=-1.0`（负差不截）。A14-04 只禁止「全 0、无 sham」把空 \(N\) 当已评估。

**A14-04 点名 CE：PASS。**

### 3.5 A12-03：`_find_tasks_jsonl` 只读给定目录的 `tasks.jsonl`

`inspect.getsource`：无 `rglob`/`glob`/`parent`；字面 `Path(folder) / "tasks.jsonl"`。

独立目录树：`ancestor/tasks.jsonl`、`ancestor/given/`（无文件）、`ancestor/given/nested/tasks.jsonl`、`sibling/tasks.jsonl`。

- `_find_tasks_jsonl(given)` → **None**（不爬祖先、不进 nested）
- `_find_tasks_jsonl(given, ancestor)` → `ancestor/tasks.jsonl`（仅因 ancestor 被传入）
- `_find_tasks_jsonl(nested)` → `nested/tasks.jsonl`（该目录本身被传入）

`cmd_fit` / `cmd_calibrate` 只把 `src` / `labels_dir` / `feat_dir` 交给该函数。calibrate 另有一条 **labels.jsonl** 的 parent 候选列表，不是 `_find_tasks_jsonl`，见 U-19。

**A12-03 点名 CE：PASS**（绑定交卷 `cli.py` `9431b776…`；函数体与开审阅读一致，文件整树已漂）。

### 3.6 E 列顺序

构造 `task.premises=['p2','p1']`，labels first-seen `p1,p2,sham:q`。`_e_premise_ids` → `['p2','p1']`。不含 `sham:q`。与 first-seen `['p1','p2']` 不等。`collect_hidden_trace` 按传入 `premises` 顺序堆 E。无 `tasks.jsonl` 且有 labels 时 fit/calibrate 抛 `fit/calibrate requires tasks.jsonl so E columns follow task.premises`。

**E 列点名 CE：PASS。**

### 3.7 A10-04 persist；孤立 Symbolic 不是残留

每步前 `clear_test_only_families()`，除非该步正在测残留锁。独立 JSON：`original_id=gsm8k-1`，题干 Dana/plums。`assign_split("gsm8k-1")=="probe_train"`。仓库夹具 `gsm8k-12` **不能**单独证明锁。

1. **从未加载 Plus、无 persist 文件的孤立 Symbolic（新进程）。** `role=probe_train`，`RAM=[]`，`disk=[]`，`locked=false`。作者主张「诚实、不是 A10-04 残留」：**独立同意。非缺陷。**
2. **Plus 然后同进程 Symbolic。** 两者 `test`。磁盘 `["gsm8k-1", "q:dana has 4 plums…"]`。
3. **仅 `_TEST_ONLY_FAMILY_KEYS.clear()`。** RAM `[]`，磁盘仍在，`family_locked_test==True`，Symbolic **仍 `test`**。
4. **全新子进程只加载 Symbolic。** RAM `[]`，`SPLIT test`，`locked true`。
5. **官方 Plus 无 `original_id`、有 `seed_question`。** 族 ID 回退文本键；与 Symbolic `original_question` 规范化后文本键相等。Plus 后 Symbolic **锁 `test`**。
6. **`siblings=`。** 清空磁盘后 `split_for_task(sym, siblings=[plus])=="test"`；无 siblings 为 `probe_train`。
7. **生产 CLI。** `prepare --kind gsm_plus` exit 0；新进程只加载 Symbolic：`role=test`，`ram=0`，`locked=true`。
8. **再 `clear` 后孤立 Symbolic。** 回到 `probe_train`。

**A10-04 persist 点名 CE：PASS。** 从未登记 Plus 且无 persist 文件的孤立 Symbolic 进 `probe_train` **不是缺陷，不重开 A10-04。**

### 3.8 T2/T3 不得发明完整 DAG

| 适配器 | `graph_status` | `graph_kind` | `ancestors()` | 备注 |
|---|---|---|---|---|
| GSM-Plus | unknown | none | `{}` | placeholder；`solution_is_not_dag` |
| Symbolic 无 sidecar | unknown | none | `{}` | 无节点 |
| Symbolic + sidecar | partial | formula_sidecar | 公式祖先 | 独立侧车，不是答案/CoT |
| Hotpot | unknown | supporting_facts_only | `{}` | supporting_facts 只进 metadata |
| MuSiQue | partial | composition_reference | `{}` | 分解节点存在但不展开为 \(R_{task}\) |
| HumanEval | unknown | none | `{}` | `reference_dfg_is_not_task_dag`；canonical_solution 不是图 |
| T1 official | complete | igsm_template | 模板祖先 | 拒 G；lookup 忽略；重算=9 |
| T1 fixture | complete | arithmetic_dag | 自建 DAG | `source_kind=fixture`；官方加载器拒 |

空节点 + `graph_status=complete` 被 `graph_status()` 拒绝。T3 prepare 不发明 SVP。GOAL §5.1：**成立（机制层）。** 官方全量仍 `pending_server`。

**T2/T3 DAG 点名 CE：PASS。**

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 500 题 × op=5,10,15,21 全量快照 | 禁止下载；仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上。**pending_server** |
| N-03 | 自然语言独立事件 DAG 侧车（除一条公式夹具） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声、人工复核回填 | 无权重/GPU |
| N-05 | 真实 dump 上跨数据集 GSM8K 碰撞率 / seed 匹配率 | 无官方 dump；机制层 A10-04 已在独立 JSON 上跑 |
| N-06 | 官方 template 是否出现除法 | 夹具为 `a * b` |
| N-07 | scientific sham seed=2 在真实权重上的命中率 | 本机 tiny 命中不能当协议命中率 |
| N-08 | 交卷树干净全量 pytest 绑定声明冻结 | 冻结已漂；162 passed 不能回写声明 hash |

官方全量保持 `pending_server`。夹具或官方字段子集上可复现的机制错误记为 confirmed defect，不降级为 pending_server。Gate 0–2 未注册不是缺陷。

## 5. 既有 B-## / A1x-## 独立结论

不得因回归绿或 `ISSUES.md` 成文而关闭。作者本轮主张关闭 A14-02/04、A13-02/03、A12-03、A10-04。

| 原 ID | 作者主张（ISSUES） | 独立结论 | 证据 |
|---|---|---|---|
| **A14-02** | 保留叶 *a*，追加等值 `src_b`，父母改读 *b* | **closed**（绑定开审 `edits.py`） | §3.1 |
| **A14-04** | 真实前提 `noise_ref=0` 且无 sham 不评估空 \(N\) | **closed**（绑定开审 `measure.py`） | §3.4 |
| **A13-02** | 未知行为不进 \(M\) | **closed** | §3.2 |
| **A13-03** | 任意 `sham:` 行 `noise_set=None` | **closed** | §3.3 |
| **A12-03** | `_find_tasks_jsonl` 只读传入目录 | **closed on drifted cli.py；不回写冻结** | §3.5 |
| **A10-04** | persist 锁；孤立可 probe_train | **closed**；孤立 **非缺陷** | §3.7 |
| B-16 / B5-03 / B-20 | Hotpot/MuSiQue 口述 `needs_truth`；祖先空 | **closed** | X-20 / X-t3prep |
| B-17 | HE placeholder 不进 ρ | **closed** | X-he-rho |
| B5-04 / B9-01 | sham `noise_ref` 只在 `sham:` | **closed** | §3.3 / X-sci |
| B-01 / B-02 / B-08 / B-11 / B-18 / B-26 | 抽查 | **closed** | X-sm / X-04 / X-11 / X-26 / X-id |

## 6. 发现（本轮开放）

本轮在声明冻结的数据/测量焦点文件上 **没有新的 confirmed defect**。交卷整树 hash 漂离使冻结作废，按用户规则通道失败。下列不升格为数据 CE。

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐、划分或 ρ 会被污染；`medium` = 协议要求的适配/字段缺失或半完成；`low` = 次要或不完整映射。

状态取值仅限：`confirmed defect` / `unconfirmed doubt` / `pending_server` / `non-defect`。

（空。开放项见 §10 / §9。）

## 7. 已独立关闭的原触发（非本轮开放缺陷）

| 原 ID | 独立证据 | 仍须跟踪 |
|---|---|---|
| **A14-02** | §3.1 | U-12 协议级双来源图 |
| **A14-04** | §3.4 | 映射 `noise_ref=1` 的真实前提仍评估 \(N\)（有意） |
| **A13-02** | §3.2 | 已知 miss 仍可进 \(M\)（有意） |
| **A13-03** | §3.3 | — |
| **A12-03** | §3.5 | 交卷 `cli.py` 已漂；U-19 labels 搜索 |
| **A10-04** | §3.7 | 无 seed→ID 表；锁文件在 `.planning` |
| **T2/T3 DAG** | §3.8 | 官方全量 pending_server |

## 8. 已确认非缺陷（non-defect）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py`；`t1_official.py` | X-26。 |
| ND-03 | 非算术 `graph_kind` 祖先为空 | `graphs.py` 7–22 | 不把 supporting facts / composition / 参考代码当 \(R_{task}\)。 |
| ND-04 | 身份键不含值 | `schema.py` 179–189 | |
| ND-15 | 非穷尽 / unscanned no_change 不记已知行为 | `build_labels` | X-04 / A13-02。 |
| ND-18 | Plus/T4/HE placeholder 过滤进 P | `event_density_sets` | X-he-rho。 |
| ND-21 | Plus/T3 Edit 缺核验不写 valid | 各 apply* | X-20 / X-plus-sub。 |
| ND-24 | Gate 未注册 / `scientific_conclusion=None` | `analysis.py` | **不是缺陷。** |
| ND-29 | `_try_source_value_pair` 跳过 T3 | `cli.py` 687–700 | |
| ND-30 | 磁盘 ∪ RAM 锁在 **被调用时** 正确 | `splits.py` 59–78, 127–153 | 孤立无 Plus、无 persist 进 `probe_train` 是诚实。**不是 A10-04 残留。** |
| ND-32 | 夹具 `gsm8k-12` 的 `assign_split` 已是 `test` | `splits.assign_split` | 不能用夹具 CLI 单独证明 persist。 |
| ND-33 | 任意 `sham:` 行不评估空 \(N\) | `measure.py` 309–360 | 关闭 A13-03。 |
| ND-34 | `same_value_diff_source` 保留 *a* + `src_b` | `edits.py` 219–292 | 关闭 A14-02；与 rename 可区分。 |
| ND-35 | 真实 0-hit 无 sham 不再评估空 \(N\) | `measure.py` 358–360 | 关闭 A14-04。 |
| ND-36 | 未知/未扫描不进 \(M\) | `measure.py` 123, 369 | 关闭 A13-02。 |

## 9. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 未验收原因 |
|---|---|---|---|
| S-01 | 官方 iGSM 500×四档 op | DATA-01 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车 | DATA-02 / MEAS-01 | 无标注资产 |
| S-04 | 真实轨迹有限扫描与多 seed 噪声 | MEAS-02 | 无模型；tiny 命中不能当协议命中率 |
| S-06 | 官方 Plus `seed_question` → GSM8K ID 匹配率 | DATA-03 | 文本键机制已测；dump 上格式差仍会拆族 |
| S-07 | Linux cgroup / 容器隔离执行器 | EXEC-01 / GOAL §5.15 | 本机仅 Unavailable + 非沙箱子进程 |

## 10. 未证实疑点（unconfirmed doubt）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-12 | `same_value_diff_source` 仍是「留 *a*、加 *b*、改读 *b*」，不是两个并行必读来源 | 点名 CE 要求 keep *a* + `src_b` + 改父母 + 保值 + ≠ rename，已满足。 |
| U-14 | 无 `seed_question`→GSM8K ID 表 | 点名 CE 只要求共享文本键/族锁，已满足。 |
| U-16 | persist 路径写死为仓库 `.planning/research/.cache/` | 可复查、跨进程有效。并行审查/prepare 会互清或互写。隔离复跑仍通过。 |
| U-17 | 并行 prepare 同时读写锁 JSON | 无文件锁。本通道串行隔离后通过。不否决 A10-04。 |
| U-19 | `cmd_calibrate` 搜 `labels.jsonl` 时仍试 `feat_dir.parent / "label"|"lab"|"labels"` | **不是** A12-03（A12-03 只约束 `_find_tasks_jsonl`）。未在本轮构造错贴 labels 的端到端污染。 |
| U-20 | 交卷 `cli.py` / `test_round07_regressions.py` 开审后被他方改写 | 本通道未写入。A12-03/E 列函数体复读未变，但整树冻结已废，不得关闭声明 hash。 |

## 11. 测试质量对本通道的含义

**162 passed ≠ 数据/测量正确。** 独立同意 **A14-02、A14-04、A13-02、A13-03、A12-03（交卷 cli）、A10-04、T2/T3 DAG、E 列、六角色、身份不含值** 在 **已跑字节** 上可关。作者测试仍不能替代：

- persist 必须自己构造 `gsm8k-1`（夹具 `gsm8k-12` 的哈希角色已是 `test`）。
- 必须测「只清 RAM」「全新子进程 RAM 为空」「从未 Plus 且无 persist → 诚实 `probe_train`」。
- A14-02 必须同时查 **p2 仍在**、`src_b` 等值、父母/表达式、答案，以及与 `apply_rename_edit` 的差异；不能只查 kind。
- A13-02 必须在 **只扫部分 \(T\)** 时确认 \(M=\emptyset\)，并与已知 miss 对照。
- A13-03 必须覆盖 sham **change 与 no-change**。
- A14-04 必须 **手工构造** `noise_ref=0` 的真实前提标签，不能只靠 `build_labels`（后者对真实前提本来就不写 `noise_ref`）。
- A12-03 必须用「给定目录无文件、祖先有文件」证明不爬升。
- 交卷漂后的 `cli.py` / `test_round07_regressions.py` 不能回写冻结关闭。

## 12. 通道结论

数据与测量通道 **不能** 在声明冻结 `3d0a0764…` 上给出整树通过意见。**FAIL。**

1. **开审 `HASH_MATCH`（61 文件，0 CRLF）。oracle 开跑与交卷 `HASH_MISMATCH`（`3d0f1c10…`）。** 用户规则：HASH_MISMATCH → FAIL。mtime 指向开审后改写的 `cli.py` 与 `tests/test_round07_regressions.py`。`edits.py` / `measure.py` / `splits.py` / `events.py` / `graphs.py` / `schema.py` / 全部 `tasks/*.py` 的 mtime 早于开审复算。连续通过计数 **不能开始**。
2. **点名 CE（独立 oracle，不信作者测试）：**
   - **A14-02：PASS。** 保留 `p2`，追加等值 `src_b`，父母/表达式改读 `src_b`，答案仍 0；与 `apply_rename_edit` 题干和前提集都不同。
   - **A13-02：PASS。** 未知/未扫描/`behavior_unknown` → \(M=\emptyset\)，`rho_M_raw=None`；已知 miss 仍可进 \(M\)。
   - **A13-03：PASS。** sham change 与 no-change 均 `noise_set=None`；fixture `sham:q=0.0`；scientific `sham:q=1.0`；真实前提不广播。
   - **A14-04：PASS。** 构造 `noise_ref=0` 的真实前提、无 sham 行 → 不评估空 \(N\)，excess null。
   - **A12-03：PASS**（交卷 `cli.py`）。只读传入目录下的 `tasks.jsonl`，不爬祖先、不 rglob。
   - **E 列：PASS。** 跟 `task.premises` 序，不跟 labels first-seen。
   - **A10-04 persist：PASS。** 清 RAM 后磁盘仍强制 test；新进程仍 test；CLI Plus 后新进程 Symbolic 仍 test。**从未加载 Plus、无 persist 的孤立 Symbolic = `probe_train`：独立同意，不是 A10-04 残留。**
   - **T2/T3 不发明完整 DAG：PASS。** Plus/Symbolic/Hotpot/MuSiQue/HE 的 `graph_status` 为 unknown/partial；`ancestors` 对 supporting_facts / composition_reference / none 返回 `{}`。
3. **无新的数据/测量 confirmed defect。** 通道失败原因是整树冻结漂离，不是点名 CE 失败。
4. 官方全量保持 `pending_server`。Gate 0–2 未注册 **不是缺陷。** pytest 162 passed **不能** 关闭任何 CE，也不能掩盖 HASH_MISMATCH。
