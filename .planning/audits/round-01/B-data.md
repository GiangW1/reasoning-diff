# Review B — 数据与测量（独立审查，round-01）

本报告不假设实现正确。未阅读其他通道审查报告或 `ISSUES.md`。未修改任何生产代码、测试或夹具。未下载数据或权重。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent_id | `reviewer-B-data`（独立 subagent，数据与测量通道） |
| review_time | `2026-09-21T00:31:41+08:00`（复现脚本起始）— `2026-09-21T00:45:00+08:00`（成文） |
| frozen_code_hash_sha256 | `532e05a8038e9862f219ab36927f7f7c0df59ef639045821a2cc801960b2b0c0`（来自 `.planning/audits/round-01/VERSION.md`，本审查按此版本对象验收） |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏，与 VERSION 一致） |
| workspace | `C:\Users\22688\Desktop\diff` |
| response_language | zh-CN |
| production_code_modified | 否 |

**聚合 hash 核验：** VERSION 未给出 `532e05a…` 的具体聚合算法。本机对 `src/reasoning_diff/**/*.py + tests/**/*.py + pyproject.toml` 做路径+字节、纯字节等若干拼接，均得不到该值。因此**不以复现聚合 hash 作为文件未变的独立证明**，而以全文阅读 + 下表单文件 SHA-256 为审查对象指纹。审查结论绑定这些 digest，不绑定未文档化的聚合式。

## 2. 逐文件覆盖

状态：`full` = 全文阅读并对照协议；`callsite` = 为核对测量/划分调用链而通读；`fixture` = 对照适配器读完；`not_in_B_core` = 未作本通道主审。

| 文件 | 行数 | 独立 SHA-256 | 覆盖 | 本通道核对要点 |
|---|---:|---|---|---|
| `src/reasoning_diff/measure.py` | 217 | `f56d7fae9cb1e495de5a332f546ff8b50ea090dbfbbed386ac993a89bb1e351f` | full 1–217 | 标签、S/M、噪声、TO/CSP、有限扫描、分母 |
| `src/reasoning_diff/events.py` | 94 | `2183fc332fcb4d603960429b900ab19e82c4b5994541e0d19291d02c96e12a2e` | full 1–94 | 身份、对齐、结构变化、表面提及 |
| `src/reasoning_diff/graphs.py` | 44 | `1e287cebf844cec0d055138224ae5a0b39c0358228c6587e8b4b6d4cfc604241` | full 1–44 | 独立 R_task 祖先、unknown/complete、cone |
| `src/reasoning_diff/edits.py` | 128 | `092ab8256e8739abc2e7bcd62f5058b9e36e12562a8d91f70d9d26e14f5810a2` | full 1–128 | 编辑合法性、重算、禁止 lookup |
| `src/reasoning_diff/splits.py` | 66 | `b7cb9671479917fcfbaf08f12ac2abf2f7c693c29057d4ab15ab6d104fc9433b` | full 1–66 | 共组、六角色、test-only、泄漏 |
| `src/reasoning_diff/schema.py` | 368 | `6775635fb667d6515af295693e05291e991f4a708cca757365f66d91d678ddd1` | full 1–368 | 枚举、身份、scan_state、分母字段 |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full | 无隐藏注册器 |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full | op∈{5,10,15,21}、n=500、mod=23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full | fixture 不得标 official |
| `src/reasoning_diff/tasks/t1_official.py` | 83 | `2e83cc052a518d43bfebd3ab3899a37ad5f369f36a29d5eedb95cbd3e48e969b` | full | template≠G、shared RNG、lookup |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 51 | `0da626321ee5d786f3c3b4c7da52687b3c9ca2d233eebe81f2d43f22c0cf3a8f` | full | test-only、solution≠DAG、族 ID |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 82 | `61c33c838dbdda585e85c8363b3d4be470eafa2243fe6e9b03b0e4048c997395` | full | sidecar、公式编辑、unknown |
| `src/reasoning_diff/tasks/t2_noop.py` | 66 | `e851e6dd10496b1bb1e7d642372b46d49d8e22c70502f9741feb004b914b17dc` | full | 项目派生名、span、答案不变性 |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 59 | `a79ab16c0ebdae7fde154df79bdfd8d0ae38d5337473a5f6a4241c2f7c3930c1` | full | supporting_facts≠DAG、文档编辑真值 |
| `src/reasoning_diff/tasks/t3_musique.py` | 69 | `095f10acc7c4600f607b2a6d5fbb6e0bd5962d0f7ccc881d79efbbfd136c3e58` | full | 组成图粒度、可回答配对、编辑 |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 35 | `02b29bf04a11ed4b2fd3e52d7dc0d581fc071bd4ab1b32262f6a569f597eb6d3` | full | 族 ID、Spec 编辑、图 unknown |
| `src/reasoning_diff/tasks/t4_boundary.py` | 33 | `a2ca9188353b213d2c7c617dd27c60415adb0c16c40326ae8a7ecce03f94a5f9` | full | 四类状态不得互推 |
| `src/reasoning_diff/cli.py` | 239 | `099789e933bc2039839754428e3faffa3255185d8211c67358a59cf3366b3ee7` | callsite 57–140 | prepare/label 是否真正调用测量 API |
| `src/reasoning_diff/analysis.py` | 108 | `7346e1247d7257bbd5efe32b51eff23f764307c00d713ab51ec3f2b3e610d944` | callsite 40–46 | P2 分母是否只是透传 |
| `src/reasoning_diff/scoring.py` | 30 | `d05822c4fb784fe4a57d9f82f583eaa31c0f3b2e0e96c04b81f77db7413433f8` | callsite | 域内评分分母 |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | full | 覆盖缺口 |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40` | full | |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177` | full | |
| `tests/test_t3_t4.py` | 40 | `54e57fea7417d901c75b7d17cfe9b90ee442f2d634a08d22272a678959ce9650` | full | |
| `tests/test_tracer_t1_prepare.py` | 99 | `e62cd9e5d283c55a85ef6877b0f6c3374975449e90bd3a82746a3a1898a67528` | full | |
| `tests/test_science.py` | 97 | `3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c` | full | no-op / require_split |
| `tests/test_cli_pipeline.py` | 18 | `55e283c2ffc09b5179e603b2ac73f1039d527ccbfbb6e624688b45fdb3a256c8` | full | smoke 不验证标签语义 |
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1` | full | |
| `tests/fixtures/t1_tiny.json` | 31 | `3267db389ad63b50bcb461a643df2e4306d75249709ee798a1a78ae42de81b91` | fixture | |
| `tests/fixtures/t1_official_shape.json` | 22 | `2fbf6773689b13b58b1cda0a513599a8638d618d5152de3992d6073512f1c1c2` | fixture | |
| `tests/fixtures/t1_ops_config.json` | 1 | `bc08ae65668736e746d2ae88002ce5553d33fc46e0273d7ddf4d6d755472aa11` | fixture | |
| `tests/fixtures/t2_symbolic_one.json` | 9 | `481f654e135ae6641253d05a8e32fefcd77853e995fc71c93003facef729eb2a` | fixture | |
| `tests/fixtures/t2_formula_sidecar.json` | 10 | `8a0149400cb15bba8706916d4320a03b7cfcd16d6bf2e77f8a3047f708b5ec02` | fixture | |
| `tests/fixtures/t2_gsmplus_one.json` | 9 | `81ac53c42a698b3919096173f108013db84705592b69b2f2fe496caf9eb1ea71` | fixture | |
| `tests/fixtures/t3_hotpot_one.json` | 12 | `6821c1e107cb78d17fb99a6b41b6d201d00c718dfd52da9d1cb43705894a34e4` | fixture | |
| `tests/fixtures/t3_musique_pair.json` | 32 | `d65a90c91a02d7e110244763283322fb41c733d6db1a8ba72daea466b9bf4ce7` | fixture | |
| `tests/fixtures/t3_humaneval_one.json` | 9 | `31bd1371d6adca92465215b88f84ce7957398476735b52ba1b693085ecdf935b` | fixture | `HumanEval/0` |
| `tests/fixtures/t4_boundary.json` | 6 | `c5426cbd00ee39839ea98c0c946ec6e20550128ae104398880185e978bfed23d` | fixture | |
| `tests/test_tiny_hooks.py` / `test_tiny_cache.py` / `test_generate_loop.py` / `test_artifacts.py` | — | — | not_in_B_core | 模型/IO，非本通道主责 |
| 其他 review 报告 | — | — | **未读** | 按任务要求 |

`graphs.ancestors`、`schema.EventIdentity`、`Observation.scan_state`、`Edit.exhaustive`、`Alignment` 均纳入核对。

## 3. 已执行检查

| ID | 检查 | 命令 / 方法 | 结果 |
|---|---|---|---|
| X-01 | 数据/测量相关 pytest | `python -m pytest tests/test_measure.py tests/test_t1_official.py tests/test_t2_gsm.py tests/test_t3_t4.py tests/test_tracer_t1_prepare.py tests/test_science.py tests/test_cli_pipeline.py tests/test_artifacts.py -q --tb=short` | **37 passed**（exit 0）。通过**不能**证明下列缺陷不存在：现有测试未覆盖这些反例。 |
| X-02 | 全量本机 pytest | `python -m pytest tests -q --tb=line` | **42 passed**（exit 0，约 10.3s）。无 skip/xfail。同样不构成科学正确性证据。 |
| X-03 | 集合密度：缺 sham → excess null；负差不截断；零分母 null | 阅读 `test_measure.py` / `test_tracer_t1_prepare.py` + 对照 `dependency_densities` 集合路径 | 集合路径行为与协议一致（见 ND-01）。 |
| X-04 | 矩阵路径缺 `noise` | 独立调用 `dependency_densities(task=[[0,1,0]], behavior=[[1,1,0]], noise=None)` | `S.noise=0.0`，`S.excess=0.5`，`rho_S_excess=0.5`。见 B-01。 |
| X-05 | `build_labels` 有限扫描 | 仅 `outcome=no_change` + `scan_state=no_response_observed_in_scan` | `behavior_label=0` 且 `behavior_known=True`。见 B-02。 |
| X-06 | sham 污染行为标签 | 同组一条 no_change + 一条 `rng_pair=sham:0` 且 changed | `behavior_label=1`，`opportunities=2`，`noise_ref=1.0`。见 B-03。 |
| X-07 | CLI 事件键 vs `ancestors` 键 | `parse_fixture_events` 的 `identity.key()` 作为 `event_pair[0]`，`task_ancestors=ancestors(task)` | `task_known=False`，`task_label=None`。见 B-12。 |
| X-08 | 出现版本位移 | 基线 versions 1,2；扰动只剩后者（解析后变成 version 1） | 剩下的值 `2` 对齐到**被删的** version 1（值 `1`）；version 2 记 disappeared。见 B-04。 |
| X-09 | 结构字段 | 同上 `align_events` 输出 | `merged=[]`，`strategy_changed=[]` 恒空。见 B-05。 |
| X-10 | 表面提及 | `parse_fixture_events("q = 0\n mentions p1\n")` | `surface_mentions=['p1','p2']`，文本不含两前提名。见 B-06。 |
| X-11 | HumanEval 族 | `load_humaneval(tests/fixtures/t3_humaneval_one.json)` | `task_id=HumanEval/0`，`base_group_id=HumanEval`。`assign_split("HumanEval")=probe_train`。见 B-07。 |
| X-12 | 公式编辑陈旧题干 | `apply_formula_edit(..., "a", "5")` | 题干仍 `Ada has 4`；premise 文本仍 `"4"`、值 `"5"`；node `total` 仍 `"7"`；answer `"8"`。见 B-08。 |
| X-13 | 数值子串替换 | premise 文本 `has 13 apples`、声明值 `"3"`，编辑为 `"4"` | 题干变成 `has 14 apples`，答案按 4 重算为 8。见 B-09。 |
| X-14 | no-op `find` 抢 span | 注入 `"p1 = 4 is a red herring."` 于 front | `p1` 的 span 变成注入句开头 `[0,6]`，不是原题 `p1 = 4`。见 B-10。 |
| X-15 | `assign_family` 成员子集 | `assign_family(['A','B','C'])` vs `['B','C']`，seed=0 | 前者 `direction_fit`，后者 `probe_train`。见 B-13。 |
| X-16 | GSM-Plus 锁是否进入 `assign_split` | `lock_test_only("gsm_plus","probe_train")` 抛错；`assign_split("gsmplus-1")` | 得到 `transfer_pairs`。见 B-14。 |
| X-17 | 空 `task_parents` 当干净事件 | `preservation_to_csp`，两事件 `task_parents=[]`，值 1→9 | `csp=0.0`，`clean_alignment_coverage=1.0`（把未知当锥外干净）。见 B-11。 |
| X-18 | MuSiQue 组成图 | `ancestors(load_musique_records(...)[0])` | `{s1:{p0}, s2:{p0,p1}}`；两节点 `expression=="composition_reference"`。见 B-16。 |
| X-19 | 官方 iGSM 夹具语义 | `load_igsm_snapshot` + `ancestors` + 同值重算 | `source_kind=official`，忽略 `G`/`lookup=99`，`q` 祖先 `{a,b}`，同字面量重算答案仍为 9。见 ND-02。 |
| X-20 | 源码检索 | 全 `src/reasoning_diff` 搜 `build_labels` / `rename` / `apply_spec` / 人工复核导出 | `build_labels` 只定义未调用；无改名、无 Spec 编辑、无人工回填入口。 |

## 4. 未执行检查及原因

| ID | 检查 | 原因 |
|---|---|---|
| N-01 | 官方 iGSM 生成器 500 题 / op=5,10,15,21 全量快照 | 禁止下载；本机仅有 shape 夹具。**pending_server** |
| N-02 | 官方 GSM-Symbolic / GSM-Plus / Hotpot / MuSiQue / HumanEval 全量 | 同上 |
| N-03 | 自然语言独立事件 DAG 侧车（除公式夹具外） | 仓库无真实标注资产 |
| N-04 | 真实模型轨迹上的有限扫描、多随机流噪声配对、人工复核 | 无权重/GPU；属服务器科学验证 |
| N-05 | 跨数据集同源 GSM8K 题在真实 dump 上的碰撞率 | 无官方 dump，仅能指出族键不一致（B-15） |
| N-06 | 官方 iGSM 表达式是否出现除法（模逆 vs `truediv`） | FEATURES 称官方 `Num` 为加减乘；夹具为 `a * b`。未对真实 generator 表达式抽样。见 U-01 |
| N-07 | 复现 VERSION 聚合 hash 的未文档化算法 | 缺少配方；已用单文件 digest 代替 |

## 5. 发现

严重度：`critical` = 会静默写出错误科学标签/指标；`high` = 真值、对齐或划分会被污染；`medium` = 协议要求的适配/字段缺失；`low` = 次要或不完整映射。

状态取值仅限：`confirmed` / `unconfirmed` / `pending_server` / `non-defect`。

---

### B-01 矩阵密度在缺失噪声时把 excess 当成 raw

- **状态：** confirmed  
- **严重度：** critical  
- **符号：** `measure._matrix_densities`  
- **行号：** `src/reasoning_diff/measure.py` 116–130，尤其 119、128–130  
- **触发：** `dependency_densities(task=..., behavior=..., noise=None)`（文档字符串却写 missing sham → null excess，见 75 行）  
- **协议：** MEAS-02 / 论文 §2.6 / PITFALLS#3：未注册配对时 corrected/excess 必须为 null，不能用 0 冒充噪声参照。  
- **证据：** 独立调用得到 `S.noise=0.0`、`S.excess=0.5`。集合路径（87–92 行）在同样缺失时正确返回 null。两条路径不一致。  
- **影响：** 走矩阵 API 的 C3 会把「未扣噪声的 raw」写成已扣除量，抬高虚假依赖。  
- **建议：** `noise is None` 时 `ref`/`excess` 保持 `None`，并写 `null_reason`。不要 `zeros_like`。

---

### B-02 有限扫描的「未观察到变化」被写成已知负行为标签

- **状态：** confirmed  
- **严重度：** critical  
- **符号：** `measure.build_labels`  
- **行号：** `measure.py` 34–40, 58；`schema.py` 29 (`SCAN_STATES`)、241 (`scan_state`)、341 (`Edit.exhaustive`)  
- **触发：** 某 `(event, premise)` 只有 `outcome in {changed, no_change}` 且全部为 `no_change`，即使 `scan_state=no_response_observed_in_scan` 且 `exhaustive=False`  
- **协议：** 论文 L78、L251：一次未变化 ≠ 已排除全部允许扰动；「未观察到变化」与「已覆盖允许扰动且无变化」必须分记。PITFALLS#2：未扫描/失败为 unknown；仅当有限域被完全有效扫描才能宣称域内阴性。  
- **证据：** X-05：`behavior_label=0`，`behavior_known=True`。`scan_state` 从未读取。`Edit.exhaustive` 从未读取。`Observation.__post_init__`（`schema.py` 248–251）只校验 `outcome`，不校验 `scan_state`。  
- **影响：** 有限扫描的 M 和「无依赖」会被当成已证实的负例进入探针/ρ_M。  
- **建议：** 无 `exhaustive` 的 no_change → `behavior_label=None` 或显式 `no_response_observed_in_scan`；禁止把 unknown 当 0。

---

### B-03 sham / 无编辑噪声机会并入 R_behavior，并被赋予前提身份

- **状态：** confirmed  
- **严重度：** critical  
- **符号：** `measure.build_labels`  
- **行号：** `measure.py` 34–46, 58  
- **触发：** 同 `(event_id, premise_id)` 组内同时存在编辑观察与 `rng_pair.startswith("sham:")`  
- **协议：** MEAS-02 / PITFALLS#3：异 seed 无编辑变化**不能**强加具体前提身份；sham 次数必须与编辑扫描匹配且分开聚合；不得把 ANY-over-edits 与单次 sham 混在同一 usable 袋。  
- **证据：** X-06：一条编辑 no_change + 一条 sham changed → `behavior_label=1`（行为被噪声污染），`opportunities=2`（分母把 sham 算进去）。  
- **影响：** 噪声参照不再独立；S 会被无编辑随机波动抬高，并钉在某个 premise 上。  
- **建议：** 行为袋排除 sham；噪声袋单独计数；未满足机会数时 `noise_ref=None`。

---

### B-04 出现版本按单轨迹重编号，删除后错位对齐

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `events.parse_fixture_events` + `align_events`  
- **行号：** `events.py` 31–38（`occurrences[(expression, scope)] += 1`）、55–61（`identity.key()` 精确匹配）  
- **触发：** 同表达式两处出现；扰动轨迹丢掉先出现的一处后重新解析  
- **协议：** 论文 L72 / L250：用变量/表达式/**出现版本**/作用域对齐，值不决定对应。PITFALLS#1：插入或删除重复计算会使按出现序号硬配对偏移。  
- **证据：** X-08：留下的值 `2` 对上基线 version 1（值 `1`）；真正对应的 version 2 被标 disappeared。身份键不含稳定 `node.id` / 基础题 ID。  
- **影响：** 值变化标签、CSP、S/M 全部跟错事件。  
- **建议：** 版本绑定稳定任务节点 + 作用域；版本歧义标 `ambiguous`，禁止静默重编号后当 matched。

---

### B-05 合并 / 策略分岔 / 版本变化从未计数；自然语言单调对齐不存在

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `events.align_events`；未使用的 `schema.Alignment`  
- **行号：** `events.py` 66–70（`merged`/`strategy_changed` 恒为 `[]`）；`schema.py` 30–38, 219–226  
- **触发：** 任意对齐  
- **协议：** STRUCT-01 / 论文 L78, L88, L252：消失、合并、重复版本改变、策略分岔单独报告，不并入值变化。自然语言允许跳过与合并的单调序列对齐；身份不明进入未对齐，不默认值依赖。  
- **证据：** X-09；仓库无第二套对齐函数。`Alignment` 枚举有 `merged`/`split`/`version_changed`/`ambiguous`，`align_events` 不用它。  
- **影响：** 结构变化会被当成 removed/added 或（在 B-04 下）错误 matched，从而进入值标签。  
- **建议：** 实现结构分类；NL 路径使用可跳过/合并的单调对齐；禁止空列表冒充「已检测、无此类事件」。

---

### B-06 `R^surf` 被写成图父母，不是步骤文本中的提及

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `events.parse_fixture_events`  
- **行号：** `events.py` 49  
- **触发：** 任意夹具解析  
- **协议：** SURF-01 / 论文 L87：表面提及记录步骤文本中的前提名称与符号引用，与值响应分开。  
- **证据：** X-10：文本 `q = 0`，`surface_mentions=['p1','p2']`（`node.parents`）。  
- **影响：** 文本保留/符号替换会改错对象；surf 与 val 不再独立。  
- **建议：** 从 `event.text` 抽别名/符号；图父母只留在 `task_parents`。

---

### B-07 HumanEval 族 ID 砍成 `"HumanEval"`，整集可能进入 `probe_train`

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `tasks.t3_humaneval.load_humaneval`  
- **行号：** `t3_humaneval.py` 16  
- **触发：** 官方 `task_id` 形如 `HumanEval/0`（夹具即为如此）  
- **协议：** DATA-03：按基础题共组，不是按数据集名共组。PITFALLS#8：同题变体共组，**不同题不得被焊成同一组**。  
- **证据：** X-11。`assign_split("HumanEval") == "probe_train"`。HumanEval 不在 `TEST_ONLY_SOURCES`（`splits.py` 9）。  
- **影响：** 全部 HumanEval 题共享一个 `base_group_id`，会被划进同一角色；该角色在本机哈希下是训练集。Spec 变体无法按题隔离。  
- **建议：** `base_group_id` 用完整 `task_id`（如 `HumanEval/0`）。评测集另作 test-only 策略，与族键分开。

---

### B-08 GSM-Symbolic 公式编辑不更新题干 / 节点值 / span

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `tasks.t2_gsm_symbolic.apply_formula_edit`  
- **行号：** `t2_gsm_symbolic.py` 62–77  
- **触发：** 带 sidecar 的合法数值编辑  
- **协议：** DATA-02：合法扰动必须带更新后真值。FEATURES T2：只改内部数字却沿用旧题干/旧中间值是错误适配。  
- **证据：** X-12：answer=8（5+3）但 question 仍写 4，premise 文本 `"4"` 与值 `"5"` 矛盾，node `total` 仍 `"7"`。  
- **影响：** 模型看到的输入与 oracle 答案不一致；事件解析会读到旧数字。  
- **建议：** 与 T1 一样改可见题干、span、中间节点，再受限求值。

---

### B-09 `apply_value_edit` 用字面量 `str.replace`，子串会改错数

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `edits.apply_value_edit`（`t1_official.official_value_edit` 原样调用，`t1_official.py` 80–83）  
- **行号：** `edits.py` 96, 104, 126（`validity` 恒为 `"valid"`）  
- **触发：** `premise.value` 是 `premise.text` 的真子串（如文本 `13`、值 `3`）  
- **协议：** DATA-01：编辑必须落在声明的前提 span / 字面量上，并重算。FEATURES T1：冻结表达式后只改声明字面量。  
- **证据：** X-13：`has 13 apples` + value `3` → `has 14 apples`。  
- **影响：** 官方 iGSM 若字面量为个位数且句中另有含该数字的数，会改错前提并给出错误新答案。  
- **建议：** 只替换 `question[start:end]` 内与声明值对齐的整记号；失败则 `validity=invalid`，禁止默认 valid。

---

### B-10 no-op 用 `str.find` 重贴 span，且不核验答案/祖先不变

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `tasks.t2_noop.make_noop_pair`  
- **行号：** `t2_noop.py` 12–13（只收一个布尔「独立非祖先」）、46–63  
- **触发：** 注入句包含某条原前提文本（或原文重复）  
- **协议：** T2NOOP-01 / PITFALLS#10：须独立证明注入句不改变已有节点祖先与答案；模型对错不是裁判。位置与表面相关度分层（此项有）。  
- **证据：** X-14：`p1` span 落到注入句 `[0,6]`。`find` 取首次出现。无重算、无祖先相等断言。  
- **影响：** 后续数值编辑会改错 span；ρ_S 分母/共同前提集合错位。  
- **建议：** 按插入位移算 span；拒绝祖先或答案变化的注入。

---

### B-11 未知 / 空 `task_parents` 被 CSP 当成锥外干净事件

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `measure.preservation_to_csp`  
- **行号：** `measure.py` 164–176, 188–192  
- **触发：** `task_parents == []`（空列表不是 `None`）或未知图却仍解析出事件  
- **协议：** 论文 L186：CSP 只在匹配的干净事件上计算；缺失不能当 0。PITFALLS#1：任务祖先未知不能用空集合代替。  
- **证据：** X-17：值已变，仍 `csp=0.0` 且 `clean_alignment_coverage=1.0`。干净判定是 `task_parents is not None and not edited ∩ parents`，空集 ∩ 任何编辑 = 空 →「干净」。  
- **影响：** 无图任务（T2/T3 unknown）若硬解析事件，会得到虚假 CSP/覆盖率。  
- **建议：** `None` 与空集且 `graph_status!="complete"` 排除出干净集合；覆盖率分母不含未知。

---

### B-12 测量主 API 未被接线；CLI 用错 R_task / R_behavior 分母

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `measure.build_labels`（死代码）；`cli.cmd_prepare` / `cmd_label`  
- **行号：** `cli.py` 92–96, 104, 137–139；`events.py` 187–189（`EventIdentity.key` 为 JSON）；`graphs.py` 20（键为 `node.id`）  
- **触发：** `reasoning-diff prepare` / `label`  
- **协议：** MEAS-01/02：按事件身份对齐后写任务/行为/噪声标签；ρ 分母是该事件的 `P\R_task` 与 `R_task`。论文 L232–247 伪代码要求 `map_input_ancestors` + 逐前提编辑记录。  
- **证据：**  
  1. `build_labels` 全仓库无调用（X-20）。  
  2. prepare：`task_set=next(iter(ancestors(task).values()))` —— 多节点时取**字典中第一个节点**的祖先，不是 target。  
  3. `behavior_set={编辑前提}` 当且仅当**任一**事件 changed —— 轨迹级「有变化」被写成单前提行为集合。  
  4. X-07：若把 CLI 的 `identity.key()` 喂给 `build_labels(ancestors(task))`，全部 `task_known=False`。  
  5. `cmd_label` 写死 `p1..p4` / `{p1,p2}` / `{p2,p3}`，不读 observations。  
- **影响：** 端到端产物里的 densities 不是事件级标签；测试只检查 `rho_S_excess is None`（`test_tracer_t1_prepare.py` 94），会绿。  
- **建议：** 用 `node.id` 或身份键统一后调用 `build_labels`；禁止写死 label 子命令。

---

### B-13 `assign_family` 用成员排序后的第一个 ID 做哈希，不是稳定 `base_group_id`

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `splits.assign_family`  
- **行号：** `splits.py` 26–35  
- **触发：** 同一题族两次传入不同成员子集  
- **协议：** DATA-03 / PITFALLS#8：先按稳定基础题/来源家族 ID 分组再切分。  
- **证据：** X-15：`{A,B,C}` → `direction_fit`；`{B,C}` → `probe_train`。  
- **影响：** 后到的变体、donor、编辑序列可把整族打进另一角色（训练/测试泄漏）。  
- **建议：** 必须传入显式 `base_group_id`；禁止从成员列表推断。

---

### B-14 GSM-Plus test-only 锁可被 `assign_split` 绕过

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `splits.assign_split` / `lock_test_only`；`t2_gsm_plus.load_gsm_plus`  
- **行号：** `splits.py` 9, 12–14, 59–66；`t2_gsm_plus.py` 45, 49–51  
- **触发：** 调用方对 GSM-Plus 的 `task_id`/`base_group_id` 使用默认 `assign_split`（不传 `test_only=True`，也不走 `lock_test_only`）  
- **协议：** DATA-03；FEATURES T2 GSM-Plus：数据卡禁止训练，必须固定为评测来源。  
- **证据：** X-16：`assign_split("gsmplus-1")=="transfer_pairs"`。`refuse_fit_split` 是可选函数。`load_gsm_plus` 只把 `metadata.role="test"` 当贴纸。夹具的 `seed_question` 哈希碰巧为 `test`，现有测试看不出来。  
- **影响：** 公开 test 变体可进入 `transfer_pairs` / `probe_train` / `calibration`。  
- **建议：** `assign_split` 识别 test-only 来源；划分阶段强制 `lock_test_only`。

---

### B-15 跨数据集族键不一致，同源题会拆散

- **状态：** confirmed（机制）/ pending_server（真实 dump 碰撞率）  
- **严重度：** high  
- **符号：** `t2_gsm_symbolic.family_id` vs `t2_gsm_plus.load_gsm_plus`  
- **行号：** `t2_gsm_symbolic.py` 11–12, 46；`t2_gsm_plus.py` 25  
- **协议：** DATA-03 / FEATURES：不同数据集的同源 GSM8K 题仍属同一题族。  
- **证据：** 夹具中 Symbolic 族为 `gsm8k-12`，Plus 族为整段 `seed_question` 文本。无规范化、无跨集映射。  
- **影响：** 同题可一边 train 一边 test。  
- **建议：** 统一规范化 GSM8K ID；匹配失败保留 unmapped，不得静默各算各的。

---

### B-16 T3 缺少「合法编辑 + 更新真值」；Hotpot sidecar 只改状态名

- **状态：** confirmed  
- **严重度：** high  
- **符号：** `t3_hotpot.document_edit`；`t3_musique.load_musique_records`；`t3_humaneval`（无编辑函数）  
- **行号：** `t3_hotpot.py` 10, 33–48, 51–59；`t3_musique.py` 27–42, 61；`t3_humaneval.py` 全文无 spec edit  
- **协议：** DATA-02 / 论文 L406：Hotpot/MuSiQue 替换关键支撑文档后更新受影响答案；HumanEval-Perturb 改 Spec 并以新测试为裁判。FEATURES：文档编辑列出实际变更的多前提；新参考实现必须过新测试。  
- **证据：**  
  - `document_edit` 只返回 id 列表，不产出新 `Task`、不改答案、不检查桥接一致性。  
  - `sidecar` 参数使 `graph_status="partial"`，但**从不写入节点**。  
  - MuSiQue 无文档替换/答案更新；`question_decomposition` 被物化为可被 `ancestors()` 消费的节点（X-18）。  
  - HumanEval 无 Spec 编辑包（旧/新 clause、新测试、区分输入）。  
- **影响：** T3 无法做经核验的反事实；若有人把 MuSiQue `ancestors()` 当 R_task，组成图会被当成任务真值。  
- **建议：** 补编辑→新 oracle 路径；sidecar 必须物化或拒绝 `partial`；组成图保持 `composition_reference` 且默认不进入完整 ρ。

---

### B-17 用题干前 N 个字符伪造前提列

- **状态：** confirmed  
- **严重度：** medium  
- **符号：** `load_gsm_plus` / `load_gsm_symbolic`（无 sidecar）/ `load_humaneval` / `load_t4`  
- **行号：** `t2_gsm_plus.py` 22；`t2_gsm_symbolic.py` 43；`t3_humaneval.py` 21；`t4_boundary.py` 26  
- **协议：** 未知图应 unknown，不得填假前提列冒充可评估 P。PITFALLS#3：悄悄改分母后仍用完整密度名。  
- **证据：** Plus 名为 `seed` 的 12 字符切片；Symbolic 无 sidecar 时 `q0` 前 8 字符；HumanEval `spec` 前 40 字符；T4 `p0` 前 10 字符。`graph_status` 多为 unknown（此项正确），但 `Task` 仍要求至少一条 premise（`schema.py` 143–144），于是造了占位列。  
- **影响：** 若下游用 `premises` 当 P，ρ_S 分母是伪造的。  
- **建议：** 占位前提显式 `kind=placeholder` / 不可评估；密度 API 拒绝 placeholder。

---

### B-18 DATA-01 的改名与来源—数值变体未实现；无人工复核回填

- **状态：** confirmed  
- **严重度：** medium  
- **符号：** 缺失（`src/reasoning_diff` 无 rename / source-value constructor / review export）  
- **行号：** 全包检索为空（X-20）。T1 仅有 `apply_value_edit` / `official_value_edit`。  
- **协议：** DATA-01：数值/改名/no-op/来源—数值变体。MEAS-01：可导出与回填人工复核。论文 L305：先 a=b 再 a≠b 的来源解耦任务对。  
- **证据：** 无对应函数。T1 也无图规则 no-op（只有 T2 项目派生注入）。  
- **影响：** C2 解耦资产与改名泛化无法从数据层生成。  
- **建议：** 最小构造器 + 复核 JSONL 读写；未实现前禁止宣称 DATA-01 完成。

---

### B-19 官方 iGSM 答案采信 dump 字段，加载时不对照 template 重算

- **状态：** confirmed（缺校验）/ pending_server（真实 dump 是否已不一致）  
- **严重度：** medium  
- **符号：** `t1_official.load_igsm_snapshot`  
- **行号：** `t1_official.py` 62–63, 67–73；`graphs.graph_status` 23–28 未被 loader 调用  
- **协议：** DATA-01：保留运算语义；不把 lookup 当新答案（lookup 已忽略，正确）。FEATURES：按拓扑重算并核对。  
- **证据：** `answer_spec.value=str(data["answer"])`。本机夹具重算恰为 9（X-19），故测试通过。空 compute 节点仍标 `graph_status=complete`（53–64 行），`Task.validate` 不调用 `graph_status()`。  
- **建议：** 加载后 `recompute` 并与 dump 比对；失败则拒绝或标 invalid。

---

### B-20 MuSiQue 全部计算节点共享同一 `expression`，事件身份会撞车

- **状态：** confirmed（若走现有 parser）  
- **严重度：** medium  
- **符号：** `t3_musique.load_musique_records` + `parse_fixture_events` 身份键  
- **行号：** `t3_musique.py` 35–41；`events.py` 36–38  
- **协议：** 身份必须能区分不同子问题。FEATURES：组成图粒度是 `composition_reference`，不能覆盖任意 CoT。  
- **证据：** X-18：两节点都是 `"composition_reference"`。解析器身份 = `(expression or id, scope)`。  
- **影响：** 多跳步骤会变成同一表达式的 occurrence 1,2，再触发 B-04。  
- **建议：** 身份优先用稳定 `node.id`；expression 字段不要填占位常量。

---

### B-21 GSM-Plus 扰动类型映射不完整 / 空操作

- **状态：** confirmed  
- **严重度：** low  
- **符号：** `t2_gsm_plus.load_gsm_plus`  
- **行号：** `t2_gsm_plus.py` 15–21  
- **协议：** FEATURES：`reversing operation` 是改查询量，不是简单换算子；`critical thinking` ≠ 约束矛盾。  
- **证据：** `reversing operation` → `query_reversed`（不在 `T4_STATUSES`）。`if status in T4_STATUSES: pass` 为空。八类官方扰动大多无状态。  
- **影响：** 边界状态无法用于 T4 相图或过滤。  
- **建议：** 显式枚举官方 perturbation → 项目状态；未识别则 `status=None` 并保留原字段。

---

### B-22 P2 分母只是调用方传入的整数

- **状态：** confirmed（实现层）  
- **严重度：** medium  
- **符号：** `analysis.p2_paired`  
- **行号：** `analysis.py` 40–46  
- **协议：** P2 必须同时报告完整密度、共同已有前提变化、新增注入列；no-op 会改变 |P\T|。  
- **证据：** 函数只做 `noop_rho - base_rho`，`shared_denominator` 原样返回。`make_noop_pair` 不计算共同分母。  
- **影响：** 报告可以看起来「有分母」而没有共同支持集合。  
- **建议：** 从配对题的前提集合计算 shared / injected / full 三列。

---

## 6. 已确认非缺陷（non-defect）

| ID | 项 | 行号 | 说明 |
|---|---|---|---|
| ND-01 | 集合路径 S/M 定义与 null 过量 | `measure.py` 81–112 | S=B\T，M=T\B；空分母 None；缺 sham/noise_set 时 excess None；负差不截断。X-03 / 现有测试与此一致。 |
| ND-02 | T1 官方与夹具来源隔离 | `t1_fixture.py` 12–18；`t1_official.py` 15–19, 24–25, 71–73；`schema.py` 138–139 | fixture 拒 official；官方拒仅有 G；shared RNG 跳过；lookup 不进重算。夹具 `source=self_authored_arithmetic`。 |
| ND-03 | `R_task` 祖先只含输入前提 | `graphs.py` 7–20 | 中间节点不进入列索引。拓扑未就绪则抛错。 |
| ND-04 | 对齐不看值（在身份稳定时） | `events.py` 55–61；`schema.py` 179–181 | `test_identity_alignment_ignores_values` 在单事件下成立。不否定 B-04。 |
| ND-05 | 联合编辑反例挡住 soundness 宣称 | `measure.py` 200–209 | `soundness_claim_allowed` 恒 False。 |
| ND-06 | GSM-Plus 不把 solution 当 DAG | `t2_gsm_plus.py` 37–42 | `graph_status=unknown`，`solution_is_not_dag=True`。 |
| ND-07 | Hotpot 声明 supporting_facts ≠ 完整 DAG | `t3_hotpot.py` 35–38 | 元数据正确；不否定 B-16 缺更新真值。 |
| ND-08 | T4 四态必须显式给出 | `t4_boundary.py` 14–16；夹具四类齐全 | 不从标题推断。 |
| ND-09 | HumanEval 不在宿主 exec | `scoring.py` 19–29；`test_t3_t4.py` | `executor_unavailable`，value null。属执行隔离，非本通道主责，但数据侧评分分母在不可用时为 None（正确）。 |
| ND-10 | no-op 项目派生命名 | `t2_noop.py` 32–41 | `reasoning_diff_noop`，`official_noop_release=False`。 |
| ND-11 | 步前边界排除跨界 token | `events.py` 74–80 | `b <= limit`。POS-01 的测量侧约束成立。 |
| ND-12 | `require_split` / `assert_disjoint` / `assert_same_role` 存在 | `splits.py` 38–56 | 原语正确；不否定 B-13/B-14 调用链。 |
| ND-13 | T1 配置拒绝非 {5,10,15,21} 与非 500 / 非 23 | `t1_config.py` 9–21 | 不发明阈值。 |
| ND-14 | 重算拒绝无 expression 的 lookup | `edits.py` 56–58 | 符合「禁止用旧 lookup」。 |

## 7. 服务器 / 外部资产（pending_server）

| ID | 项 | 对应需求 | 本机已有路径 | 未验收原因 |
|---|---|---|---|---|
| S-01 | 官方 iGSM 500 题 × 四档 op 快照与 generator revision | DATA-01 | `load_igsm_snapshot` + 形状夹具 | 无全量 dump |
| S-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 官方 revision | DATA-02 | 各 `load_*` | 禁止下载 |
| S-03 | NL 独立事件 DAG / 公式侧车（除一条 symbolic 夹具） | DATA-02 / MEAS-01 | sidecar 参数 | 无标注资产 |
| S-04 | 真实轨迹上的有限扫描、多 seed 噪声机会、人工复核 | MEAS-02 | schema 字段 + `build_labels`（且见 B-02/B-03） | 无模型；API 本身仍有缺陷 |
| S-05 | 官方 iGSM 表达式算子集（是否仅 +−×） | DATA-01 | `_eval_expr` 含 `/` | 见 U-01 |

## 8. 未证实疑点（unconfirmed）

| ID | 疑点 | 为何未升格 |
|---|---|---|
| U-01 | `_eval_expr` 对 `/` 做 `int(truediv)%mod`（`edits.py` 32–35；5/2 mod 23 = 2，模逆应为 14） | FEATURES 称官方 Num 为加减乘；夹具无除法。若真实 template 出现除法则升为 confirmed。 |
| U-02 | 编辑后的 official 记录仍 `source_kind=official`（`edits.py` 107–115 拷贝 to_dict） | 可解释为「题源」而非「该行是官方发布」。需协议裁定。 |
| U-03 | 后续 stage 是否用 `task_id` 而不是 `base_group_id` 做划分 | CLI fit/calibrate 只信 `--split` 旗标（`cli.py` 143–158），本通道未跟完整特征管线。 |

## 9. 测试质量对本通道的含义

现有测试**全部通过**，但未包含能暴露 B-01–B-16 的反例：

- 无 `build_labels` 测试。  
- 无矩阵 `noise=None` 测试。  
- 无双出现事件删除对齐测试。  
- 无 `13`/`3` 子串编辑测试。  
- 无 no-op 文本碰撞测试。  
- 无 `HumanEval/0` 族键断言。  
- 无 `assign_family` 子集稳定性测试。  
- `test_gsm_plus_is_test_only` 只查 metadata 与 `assign_split(..., test_only=True)`。  
- `test_full_cli_smoke` 只查 exit 0 与文件存在。

因此 **42 passed ≠ 数据/测量正确**。

## 10. 通道结论

数据与测量通道**不能**在本冻结对象上给出通过意见。

已确认缺陷覆盖：标签分母与噪声（B-01/02/03/11/12/22）、事件身份与结构变化（B-04/05/06/20）、编辑有效性与独立真值（B-08/09/10/16/18/19）、划分泄漏（B-07/13/14/15）、占位前提（B-17）。

集合密度的 raw/null/signed 路径与 T1 来源隔离是少数已独立核实的正确片段（ND-01–ND-14），不能抵消标签主路径与 T2/T3 真值更新的缺口。

真实官方全量与模型轨迹保持 `pending_server`。即使服务器数据到达，B-01–B-16 仍会在本机逻辑层写错标签。
