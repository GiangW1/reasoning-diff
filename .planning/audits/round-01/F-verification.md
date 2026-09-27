# F：验证质量与反向质疑

独立审查通道 F。不修改生产代码。不把 pytest 通过当作行为正确。未阅读其他通道审查报告。

## 1. 元数据

| 字段 | 值 |
|---|---|
| agent / 任务标识 | Independent Reviewer F / verification quality and adversarial questioning |
| 审查时间 | 2026-09-21（Asia/Shanghai） |
| 冻结代码 hash | `532e05a8038e9862f219ab36927f7f7c0df59ef639045821a2cc801960b2b0c0`（本通道复算匹配） |
| hash 算法（复核） | 对 `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`（排除 `__pycache__`），按 `as_posix().lower()` 排序后，逐文件 `relpath.encode() + b"\0" + bytes` 做 SHA-256 |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d`（2026-09-20 23:54:47 +0800；工作区脏，与 `VERSION.md` 一致） |
| 审查范围 | `tests/**` 全部测试与夹具；测试所 import 的全部生产模块；为核对“未接通路径”而通读的 CLI / 探针 / 干预 / 修复入口 |
| 明确未读 | `.planning/audits/round-01/` 下除 `VERSION.md` 外的其他通道报告；`ISSUES.md` |

**结论先行：** 当前 42 个测试全部通过，只能证明所写断言成立。其中一批断言是自指、空断言或只检查退出码/文件存在；CLI 后段、P1、三位置、C-layer、探针训练、标签流水线、修复执行等论文行为没有独立 oracle。交付文档把“full CLI smoke / CLI pipeline / 39 passed”写成阶段通过，超过测试实际证明力。

## 2. 逐文件覆盖

### 2.1 测试（全部阅读）

| 文件 | 行 | 覆盖说明 |
|---|---:|---|
| `tests/conftest.py` | 1–11 | 仅 `t1_tiny_path` |
| `tests/test_artifacts.py` | 1–73 | JSONL/NPZ/run_spec/manifest/NaN |
| `tests/test_cli_pipeline.py` | 1–18 | 八阶段退出码 smoke |
| `tests/test_generate_loop.py` | 1–17 | Generator 重放 + greedy |
| `tests/test_measure.py` | 1–40 | ρ 符号差、零分母、联合编辑、cone 字段 |
| `tests/test_science.py` | 1–97 | 校准/迁移/边界/流/Week8/P1/verbalizer/repair/swap/noop |
| `tests/test_t1_official.py` | 1–31 | official 形状/mod23/配置/禁 tools |
| `tests/test_t2_gsm.py` | 1–33 | sidecar 编辑、unknown、GSM-Plus test-only |
| `tests/test_t3_t4.py` | 1–40 | Hotpot/MuSiQue/HumanEval/T4 |
| `tests/test_tiny_cache.py` | 1–25 | cache 变异 + collect/intervene tiny |
| `tests/test_tiny_hooks.py` | 1–27 | Qwen2/Qwen3 hook 清理 |
| `tests/test_tracer_t1_prepare.py` | 1–99 | fixture prepare、划分、对齐、密度、TO |
| `tests/fixtures/*.json` | 全部 10 个 | 手算对照用 |

### 2.2 生产模块（测试 import + 被 CLI smoke 间接调用）

| 文件 | 行 | 测试触及 | 未测/只被 stub 碰到 |
|---|---:|---|---|
| `src/reasoning_diff/__init__.py` | 1–5 | 间接 | — |
| `schema.py` | 1–368 | 枚举、Task、EventIdentity | `canonical_value` 分数/别名、`Cost`、多数 schema 负路径 |
| `io.py` | 1–108 | encode/jsonl/npz/digest | `runtime_info`、损坏 JSONL 行号 |
| `artifacts.py` | 1–83 | run_spec/manifest/latest | `completed_shard_ok` 整函数 |
| `graphs.py` | 1–44 | ancestors/cone 间接 | `graph_status` 空 complete 拒绝 |
| `edits.py` | 1–128 | 值编辑重算 | 非算术表达式、跨 span 位移多前提 |
| `events.py` | 1–94 | parse/align/boundary | `extract_answer`；merged/strategy 永远 `[]` |
| `measure.py` | 1–217 | set 密度、joint、cone、LCS | `build_labels`、`_matrix_densities`、`preservation_to_csp` 字段、`compare_pair` |
| `splits.py` | 1–66 | assign/require/test-only | `assign_family`、`assert_disjoint`、非法 fractions |
| `rng.py` | 1–53 | 两流不等 | snapshot/restore、同 bank 可重放未测 |
| `cli.py` | 1–239 | 退出码 | 阶段间数据流、报告内容 |
| `analysis.py` | 1–108 | 单类 P1、Week8 未注册、P3 旗标 | 真 logistic P1、P2、门槛比较、`cone_fit`/`procrustes`/`retrieval_scatter`/`bootstrap_cluster` |
| `interventions.py` | 1–73 | `apply_swap` 一向量 | `c_rand` 范数源、`inlp_remove`、`rescue`、`intervention_report`；**无 C-layer 函数** |
| `transfer.py` | 1–36 | 4096/3584 N/A + 形状 | 映射数值正确性、监督/无标签差异 |
| `baselines.py` | 1–44 | verbalizer 两档 + supervised 合同 | `text_predictor`、`attention_mean`、`attention_rollout`、fiveshot |
| `repair.py` | 1–57 | mask 校验 + refilled 旗标 | `repairability`/`recompute_ratio`；真实重算 |
| `executor.py` | 1–59 | Spy 被构造 | `spy.calls` 未断言；`forbid_host_exec` 未测 |
| `scoring.py` | 1–30 | `score_code` 状态 | `score_qa`；隔离真正执行 |
| `probes/bilinear.py` | 1–45 | 仅 CLI 随机初始化 | **无 fit/train**；unknown mask BCE |
| `probes/boundary.py` | 1–23 | 无测试 | Hidden=256 / ReLU 从未断言 |
| `probes/calibrate.py` | 1–33 | 两 α + sequence 三分支 | `predict_set`；α=1；p 与 1-p 合成 |
| `models/features.py` | 1–28 | 跨界一例 | `leaks_target` 恒 False；三位置同 index |
| `models/tiny.py` | 1–88 | 前向+hook 清理 | tuple 输出路径（空断言） |
| `models/collect.py` | 1–41 | 旗标 | `cache_isolated` 只比对象身份 |
| `models/generate.py` | 1–56 | 重放/greedy | `apply_model_template`、top-p/k、thinking |
| `models/adapters.py` | 1–29 | 无测试 | 卡片 revision/`latest` 死分支 |
| `tasks/t1_fixture.py` | 1–20 | 加载 | — |
| `tasks/t1_official.py` | 1–83 | ancestors/mod/编辑 12 | 元数据旗标硬编码；`official_value_edit` |
| `tasks/t1_config.py` | 1–21 | 合法配置 | 拒 ops/mod/n≠500 |
| `tasks/t2_gsm_symbolic.py` | 1–82 | sidecar 5+3=8 | 无 sidecar 占位前提 |
| `tasks/t2_gsm_plus.py` | 1–51 | test-only | `query_reversed∉T4_STATUSES` |
| `tasks/t2_noop.py` | 1–66 | 来源字段 | mid/back、文本丢失 |
| `tasks/t3_hotpot.py` | 1–59 | unknown + 两前提 id | 不写回 replacement、无新真值 |
| `tasks/t3_musique.py` | 1–69 | 可/不可答配对 | 组合参考当 expression 的重算 |
| `tasks/t3_humaneval.py` | 1–35 | unavailable | `score_submission` 不走 Spy |
| `tasks/t4_boundary.py` | 1–33 | 四状态集合 | 非法 status、家族共组 |

夹具 JSON **不在冻结 hash 范围内**。改 `tests/fixtures/*.json` 不会改变 `532e05a8…`，但会改测试“真值”。见 F-16。

## 3. 已执行检查与结果

| 检查 | 命令/方法 | 结果 |
|---|---|---|
| 冻结 hash | 见上算法 | 匹配 `532e05a8…` |
| 全量 pytest | `python -m pytest tests -q --tb=short`（仓库根，`pythonpath=src`） | **42 passed / 10.96s / exit 0**。无 skip/xfail/deselected |
| 收集清单 | `pytest tests --collect-only -q` | 42 node；含 `test_generate_loop` 与 `test_tiny_cache`（交付文档仍写 39） |
| 手算 oracle | iGSM `4*3 % 23 = 12`；fixture `7*0=0`；sidecar `5+3=8`；TO `2·LCS([1,2],[1,3])/4=0.5`；ρ 例见下 | 与**被测实现的公式**一致的用例，测试写对了 |
| 官方 span | `t1_official_shape.json` `question[0:30]` / `[31:56]` | `'The number of red apples is 3.'` / `'The number of boxes is 3.'`，与字面一致 |
| 对抗：CLI 数据流 | 读 `cli.py` + 跑 `analyze` | `label`/`fit`/`calibrate`/`intervene`/`analyze` **不读上一阶段目录**；`analyze` 的 `report.json` 由内存常数生成 |
| 对抗：三位置 | `select_prefix_index` 对 `[[0,2],[2,8],[8,9]]@6` 与 collect 风格 offsets | `pre_step`/`pre_value`/`post_step` 的 `token_index` **全部相同** |
| 对抗：校准 α=1 | `conformal_threshold([0.1,0.2,0.3,0.4], 1.0)` | `k=0`，`q=0.4`（`arr[-1]`，最大分） |
| 对抗：联合编辑恒 False | `f≡0` | `joint_changed=False` 仍 `soundness_claim_allowed=False` |
| 对抗：Week8 给门槛 | `week8_decision(..., {gate0/1/2:0.9})` | 三门标成 `evaluated`，**不比较任何测量值** |
| 对抗：P1 | 读源 + 跑 CLI 同输入 | `length+0.01*op` 不是留出 logistic；该合成数据 AUC 基线=满=1，`delta=0` |
| 对抗：Spy | 调用 `score_code(..., executor=spy)` | 实现会写入 `spy.calls`，但测试不断言 |
| 对抗：C-layer / 探针训练 | `dir(interventions)` / `BilinearProbe` | **无** `c_layer*`；探针仅有 `score`/`predict_matrix` |

## 4. 未执行检查及原因

| 未执行 | 原因 |
|---|---|
| 真实 HF 权重、官方全量 iGSM/GSM/Hotpot/MuSiQue/HumanEval、GPU/CUDA KV | 本机/范围外，`pending_server` |
| 隔离 Linux 执行器真正跑代码 | 仅有 `UnavailableExecutor`/`SpyExecutor` |
| 阅读其他审查报告做交叉质询 | 任务禁止 |
| 修改生产代码或新增回归测试 | 任务禁止；反例以协议形式写在第 8 节 |
| 对第三方 `transformers`/`torch` 源码逐行审计 | 只审查本仓库用法与版本假设 |

## 5. 交付声明 vs 测试实际证明力

| 声明位置 | 声明 | 测试是否撑住 |
|---|---|---|
| `.planning/phases/01-data-truth-measurement/01-VERIFICATION.md` L1–14 | `status: passed`；`39 passed`；“full CLI smoke” | **不能。** 现为 42 passed；smoke 只断言 `main==0` 与两个文件存在（`tests/test_cli_pipeline.py` L15–18）。后段 CLI 写死数据 |
| `.planning/phases/01-data-truth-measurement/01-01-SUMMARY.md` L3–9 | “implemented locally”；“CLI pipeline”；39 passed | **不能**当作端到端流水线已接通 |
| `docs/SERVER_RUNBOOK.md` L22–31 | 八条命令按阶段顺序，暗示真实流水线 | 命令可跑通，但 `label` 无输入、`analyze` 不消费 intervene/repair |
| `docs/HANDOFF.md` L24 | HumanEval 默认 `executor_unavailable`，无宿主 exec | **部分成立**：测试不断言未调用 `exec`/`eval`，只认状态字符串 |
| `.planning/STATE.md` L21–22 | Requirements implemented: 0/16 | 与代码 stub 程度更一致，**比阶段 verification 诚实** |
| `.planning/REQUIREMENTS.md` | 全部需求仍未勾选 | 与“阶段 passed”冲突 |
| `VERSION.md` | “39 passed earlier + generate/cache added；reviewers must re-run” | 本通道已重跑：42 passed。旧“39”不可再引用为当前证据 |

**复述：** 把 pytest 绿当作 QA-01 / OPS-01 / C3-01 已验收，是交付层错误，不是测试偶然失败。

## 6. 测试是否独立有效

### 6.1 有独立 oracle 的（可算对）

这些不断言“函数自己的报告字段”，而是用手算或协议字面量：

- `test_value_edit_recomputes_expression`：`p1=7,p2=0 → q=0`（`tests/test_tracer_t1_prepare.py` L32–38）。
- `test_symbolic_sidecar_edit`：`a:4→5`，`a+b=8`（`tests/test_t2_gsm.py` L9–16；夹具 sidecar L8）。
- `test_template_not_g_and_mod23` 的 **答案** `12`：手算 `4*3 % 23`（`tests/test_t1_official.py` L21）。`nodes[0].value != "99"` 过弱，但 `answer_spec.value == "12"` 能抓住仍用 lookup=99 的实现。
- `test_to_empty_is_null`：空 TO 为 null；`[1,2]` vs `[1,3]` → 0.5（`tests/test_tracer_t1_prepare.py` L80–82）。
- `test_signed_excess_not_clipped` / `test_pitfalls_densities_and_null_excess`：按**当前实现** `ρ_S=|B\T|/|P\T|`、`noise=|N\T|/|P\T|` 手算得 `0-0.5=-0.5`。这锁定实现公式，**不等于**论文“同题不同随机流、匹配机会”的噪声定义已被验证（见 F-11）。
- `test_zero_denominator_null`：`P=T={p1}` → `ρ_S`/`denominator_S` 为 null。
- `test_conformal_examples`：`n=4,α=0.4 → k=⌈5·0.6⌉=3 → q=0.3`；`α=0.1 → k=5>4 → +∞`。这两点独立正确。
- `test_swap_formula`：`H'= [1,0] + Π_{e2}([0,1]-[1,0]) = [1,1]`。
- `test_encode_rejects_nan`、`test_npz_no_pickle`、`test_fixture_is_never_official`、`test_no_tools_import`、`test_direct_transfer_rejects_4096_3584` 的 N/A 状态串、`test_gsm_plus_is_test_only` 的 `refuse_fit_split`。
- `test_tiny_forward_and_hook_cleanup` 的 **hook 生效与 remove 后 logits 复原**（L22–26）有效。L17 空断言除外。
- `test_explicit_generator_replay`：同 seed Generator 重放有效；greedy argmax=1 有效。

### 6.2 无效或弱独立（期望来自被测函数 / 硬编码旗标 / 空断言）

| 测试 | 问题 |
|---|---|
| `test_full_cli_smoke` L15–18 | 只认退出码与文件存在。错误实现只要 `return 0` 并 `write_json(report)` 即过。 |
| `test_joint_edit_blocks_soundness` | 不断言 `f(0,0)=0,f(1,0)=0,f(0,1)=0,f(1,1)=1`；只读 `joint_edit_counterexample` 自己的字段。`soundness_claim_allowed` 在实现里**恒为 False**（`measure.py` L207）。 |
| `test_week8_never_passes_unregistered` | 只喂 `{"status":"not_evaluated"}`。不测 REST 禁句拦截，不测给门槛后的行为。`p3_recovery` 只断言硬编码 `causal_reverse_claim is False`。 |
| `test_p1_null_on_single_class` | 只测单类返回 None。任意 `if unique(y)<2: return None` 的桩都过。 |
| `test_direct_transfer` 的 map | `np.ones` 拟合后只查 `mapped.shape==(5,4)`。`return np.ones((5,4))` 或 `vectors[:,:4]` 都会过。本通道实测 `allclose(ones)` 为 True。 |
| `test_cone_fields_separated` | 只查 `source` 字符串和 `"q" in cone`。`behavior_mask` 在 `predicted={}` 时仍标 `behavior_head`。 |
| `test_template_not_g_and_mod23` 旗标 | `shared_rng_excluded` 在 loader **写死 True**（`t1_official.py` L72），不是“节点已排除”的计算结果。`ignored_structure_graph` 只是 `"G" in data`（L71）。 |
| `test_config_ops` | 只送合法 `{5,10,15,21},500,23`。恒返回 `status=checked` 的桩能过。 |
| `test_collect_and_intervene_tiny` | `leaks_target is False` 是 `features.py` L13/L19 字面量；`cache_isolated` 是 `is not` 对象身份（`collect.py` L38）。 |
| `test_tiny_hooks` L17 | `assert layer.__class__.forward` 对任意类都真。 |
| `test_humaneval_never_host_exec` | 不检查 `spy.calls`；`score_submission` 不传入 spy。硬编码 `status=executor_unavailable` 即过。 |
| `test_repair_reprefills_and_refuses_gate` | `run_repair` 不重算，`generated_tokens=0`（`repair.py` L37–45）。只测旗标与非法 mask。 |
| `test_streams_are_independent` | 只断言两个标量不等，不测同流重放、snapshot、与 `torch.Generator` 隔离。 |
| `test_verbalizer_supervision_contract` | 不测 fiveshot、公平前缀、与探针同划分样本。 |
| `test_t4_statuses_distinct` | 集合相等；不测非法 status、共组划分。 |
| `test_hotpot_support_is_not_full_dag` | `document_edit` 不改 task、不算新答案（`t3_hotpot.py` L51–59）。 |
| `test_use_cache_false_still_mutates_passed_cache` | 把 cache 污染写成**期望行为**，没有对应的“干预条件必须内容隔离”失败测试。 |

## 7. Mock / stub 掩盖的未接通路径

仓库几乎不用 `unittest.mock`，但用**内部桩**达到同样效果。

1. **CLI 阶段互不消费（F-01，致命）。**  
   `test_full_cli_pipeline` 把每个子命令写到**不同** `out-dir`（`prep/col/lab/fit/cal/int/rep/an`），后段也没有 `--in-dir`。生产侧：
   - `cmd_collect` L127：`features.npz` 写入 `dummy` 全零；
   - `cmd_label` L137–139：密度写死 `p1..p4`，与 prepare 产物无关；
   - `cmd_fit` L145–150：随机 `BilinearProbe`，无训练循环；
   - `cmd_calibrate` L156–158：写死 `[0.1,0.2,0.3,0.4], α=0.4`；
   - `cmd_intervene` L169–172：目标/对照指标写死 `0.8/0.2/0.25`；
   - `cmd_analyze` L188–195：P1–P3 与 Week8 全部内存常数，本通道跑 `analyze` 后目录中**没有** `interventions.jsonl`。

2. **探针没有训练入口。** `BilinearProbe` 仅 `score`/`predict_matrix`。CLI fit 计算一次随机权重 BCE 即写入。测试不读 `probes.jsonl`。

3. **修复不执行嫁接。** `run_repair` 只填 `RepairRecord`。论文 C4（无门控重算、同预算比较、离线评分）未被测试触达。

4. **HumanEval 隔离是“不可用”不是“已隔离运行”。** Spy 可记录调用，测试不用。`score_submission`（`t3_humaneval.py` L34–35）走默认 `UnavailableExecutor`。

5. **tiny intervene 的隔离证明是身份比较。** `past_key_values=None` 开第二次前向，必然新对象。`test_use_cache_false_*` 反而证明传入 cache 会被原地改写——与“条件间缓存隔离”主张并立，测试未把二者收成失败。

6. **边界检测器、注意力/rollout、模型卡片、`apply_model_template`、INLP、rescue、P2、cone_fit、Procrustes、检索散点、`build_labels`、CSP 分母** 均无测试入口，却可被文档/CLI 名称暗示“已有”。

## 8. 缺失的论文行为（测试未覆盖，错误实现可绿）

对照 `REQUIREMENTS.md` / 协议 / Goal 高风险清单，下列行为**没有**能推翻错误实现的测试：

| 论文/协议行为 | 现状 | 测试 |
|---|---|---|
| P1：留出题、链长+op **logistic**、增量 AUC、问题级区间 | `p1_incremental` L34–36 用 `length+0.01*op` 线性分 | 只测单类 None |
| P2：no-op 配对 Δρ、新前提改分母 | `p2_paired` 存在，CLI 写死 | **零测试** |
| P3：相对 C-rand/C-layer 的恢复 + 非目标/无效 | 减法 + 恒 `causal_reverse_claim=False` | 只测该 False |
| C-rand/C-layer **同批次**、实际范数匹配 | 仅 `c_rand_delta`；主范数来自 `default_rng(1)`（`interventions.py` L34）**不是**主干预基 | 无 |
| C-layer | **无符号** | 无 |
| 交换公式在真实 residual/KV 上、目标首 token 前 | tiny 只 `+0.01`；CLI 在 numpy 向量上 swap | 无 token 时机测试 |
| 三位置分别采集（POS-01） | `boundary_index` **忽略** position，一律 `b<=limit`（`events.py` L74–80） | 只测 `pre_step` 一例 |
| 步前特征不含目标/跨界（POS-01） | `leaks_target` 恒 False | 只断言 False |
| 命题 2：`a=max(1-p)`，`q=⌈(N+1)(1-α)⌉` 顺序统计，`R̂={1-p≤q}` | `sequence_score` 取 `max(edge_scores)`（L16）；`predict_set` 用 `1-p`（L33）；单位未合成 | 不测 `predict_set`，不测 α=1 |
| 双线性低秩训练、unknown 掩码加权 BCE、双头 | 随机权重；无 unknown 测例 | 无 |
| 边界 MLP Hidden=256 ReLU | 类存在 | **零测试** |
| R^surf 与 R^val 分列（SURF-01） | `surface_mentions=node.parents`（`events.py` L49） | 无 |
| 结构变化消失/合并/策略分岔（STRUCT-01） | `merged`/`strategy_changed` 恒 `[]`（`events.py` L66–70） | 对齐测试只查一对 identity |
| 噪声：匹配机会 + sham 协议（MEAS-02） | `build_labels` 读 `sham:` 前缀 | **`build_labels` 零测试** |
| TO_all / TO_clean / CSP 覆盖率/脏变化率 | `preservation_to_csp` 存在 | prepare 写入但不断言字段 |
| 来源—数值解耦 donor（CAUSAL-02） | 无构造器测试 | 无 |
| INLP 四结局、救援、错误来源对照 | `inlp_remove`/`rescue` 无测试 | 无 |
| 跨模型：双输入都映射、禁止静默 pad | `apply_map` 只右乘 W | 只测 shape |
| 附录：Repairability、RR、成本分列、拓扑复用原槽 | 公式函数存在，repair 不跑 | 无 |
| 四档 verbalizer + 公平前缀 | reflection 以外未测 | 部分 |
| REST-01/02/03 报告器 | Week8 扫字符串；测试不注入禁句 | 缺 |
| 同基础题全变体共组、assert_disjoint | 函数在 | 只测同一 id 两次 assign |
| 官方 500 题 / 改名/no-op/来源—数值变体 | 仅配置 happy path | 无 |
| T2/T3 合法编辑 + 更新真值 | 仅 symbolic sidecar | Hotpot 编辑不更新答案 |
| 代码任务隔离执行（EXEC-01） | unavailable | 不证明沙箱 |

## 9. 反例设计（应使错误实现失败；当前测试不会）

下列反例均为**独立可计算**，可直接写成回归。本通道未改代码。

### CE-1 未接通 CLI

- 构造：`prepare` 写出 `labels.jsonl` 后，把该文件删掉或改成空，再跑 `analyze`（或现测试的分目录模式）。
- 期望：分析拒绝或 ρ/P1 与 prepare 一致。
- 当前：`analyze` 仍 exit 0，`p1.delta_auc==0`（内存数组）。
- 暴露：`test_full_cli_smoke` 与 01-VERIFICATION“pipeline”。

### CE-2 联合编辑自指

```text
独立断言: f(x,y)=x*y
f(0,0)=0, f(1,0)=0, f(0,1)=0, f(1,1)=1
再读 report["single_point_unchanged"] 与 report["joint_changed"]
恒等 f≡0 时不得仍算“已演示反例”
soundness_claim_allowed 必须由 (单点未变 ∧ 联合已变) 推出，或报告 invalid_fixture
```

- 当前：`f≡0` 仍 `soundness_claim_allowed=False`（REST-03 保守）但 `joint_changed=False`，测试仍绿。

### CE-3 三位置坍缩

- 输入：offsets `[[0,2],[2,8],[8,12]]`，步起点 char=2，步尾 char=12，数值起点 char=8。
- 期望：`pre_step` 为完全位于 2 之前的最后 token（无）；`pre_value` 用 8；`post_step` 可用含步尾的 token。三者 **token_index 不得全等**。
- 当前：`boundary_index` 忽略 `position`，本通道实测三者均为 0。
- 对应 POS-01 / `events.py` L74–80 / `features.py` L11–19。

### CE-4 泄漏旗标

- 若 `token_index` 对应区间满足 `a < target_char < b` 或 `a >= target_char`，`leaks_target` 必须为 True。
- 当前恒 False。测试 `test_boundary_excludes_straddle` 只查 excluded 列表，不查旗标计算。

### CE-5 校准单位与 α=1

```text
p_hat = [0.9, 0.1]
非符合分数 s = 1-p = [0.1, 0.9]
sequence 单位应取 max(s)=0.9（命题 2），不是 max(p)=0.9 碰巧同形
α=1, scores 升序 [0.1,0.2,0.3,0.4]: k=⌈5·0⌉=0
禁止 arr[-1]；应 invalid 或 q=-∞ / 空预测集
predict_set(p_hat, q) 必须与同一 s 定义合成
```

- 当前：`conformal_threshold(...,1.0)["q"]==0.4`（最大分）；`sequence_score` 与 `predict_set` 方向相反且无测试合成。

### CE-6 P1 置换

- 数据：链长完美预测 y，ρ 为噪声。
- 期望：控制链长+op 的 **logistic** 后，加入 ρ 的 ΔAUC≈0。
- 再反转：ρ 完美、长度无关，ΔAUC>0。
- 当前实现即使用户数据需要增量，也可能因 `+rho` 线性叠加得到 tautology；测试只有单类。
- CLI 同款数组给出 `auc_base=auc_full=1`，`delta_auc=0`，仍写成 estimate 进 `report.json`。

### CE-7 迁移映射

- `src = [[1,0],[0,1]]`，`tgt = [[2,0,0],[0,3,0]]`（或已知仿射）。
- 期望：`apply_map(tgt, W)` 数值接近 src，误差用独立 lstsq。
- 禁止：全 1 矩阵只查 shape。
- 再：`direct_transfer` 后静默 `pad/[:d]` 必须失败。

### CE-8 C-rand 范数与 C-layer

- 主干预基 `U` 与 C-rand 随机基同 r、同位置；`||Δ_rand||` 必须匹配 `||Π_U(h_d-h_b)||`，RNG 来自 direction 流，不是 `default_rng(1)`。
- C-layer 必须存在且层号来自 **dev**，测试集禁选层。
- 当前无测试；C-layer 无实现。

### CE-9 未知掩码 BCE

- `target` 含 `nan` 或 `mask=0` 的格子。
- 期望：loss 与手算仅 known 项的加权 BCE 相同；把 unknown 当 0 必须失败。
- 当前 `weighted_bce` 零测试。

### CE-10 官方元数据 vs 行为

- 在 snapshot 中保留 `shared_rng` 节点并**故意让 loader 收进 premises**，同时 metadata 仍 True。
- 期望：断言 `SHARED_RNG` 不在 `premises`/`nodes`，而不是 `metadata["shared_rng_excluded"] is True`。
- 再：`G.edges` 与 template 矛盾时，`ancestors` 必须跟 template，并有“若误用 G 则会错”的夹具。

### CE-11 HumanEval 真隔离

- 断言 `spy.calls` 长度为 1 且 `source`/`tests` 与入参相同。
- `score_submission` 必须接受 executor，或测试证明其调用 `score_code` 而非宿主 `exec`。
- 对含 `exec(` 的提交，Spy 返回 `rejected`（`executor.py` L44–45）——**当前测试不覆盖**。

### CE-12 噪声机会

- 构造 `Observation`：真编辑 `changed` 一次；`rng_pair="sham:1"` 的 no-edit 对照 `no_change`。
- 期望：`build_labels` 的 `noise_ref` 按协议机会数；缺 sham → `rho_*_excess is None`（prepare 已有一部分）。
- 把 `noise_set` 当又一个行为集合的密度公式，必须用观测对象而不是手写 set 才能暴露。

### CE-13 Week8 门槛

- `gate_thresholds={"gate0":0.9}` 且测量不足或未注册方法：决策不得为无比较的 `evaluated`。
- 测量文本含 `"already decided"`：必须进入 `forbidden_claims_blocked`（实现能拦，**测试没喂**）。

### CE-14 修复预算

- `repairability(generated=4, full=10)=0.6`；`full=0 → None`。
- `run_repair` 后 `generated_tokens` 不得恒 0（除非声明“只记协议、不执行”并退出交付“已实现 C4”）。

## 10. 发现清单

### F-01 CLI smoke 把未接通 stub 当成全链路

- **严重度：** Critical  
- **状态：** confirmed defect（验证缺陷；连带实现未接通）  
- **文件/符号/行：** `tests/test_cli_pipeline.py` `test_full_cli_smoke` L4–18；`cli.py` `cmd_collect` L127、`cmd_label` L137–139、`cmd_fit` L143–150、`cmd_calibrate` L154–158、`cmd_intervene` L169–172、`cmd_analyze` L188–195  
- **触发：** 八个命令分目录、只查 exit 0 与 `report.json`/`manifest.json` 存在  
- **对应要求：** OPS-01、QA-01、Goal §六“从生产入口验证跨模块数据流”；01-VERIFICATION“full CLI smoke”  
- **复现：** 见 CE-1；本通道 `analyze` 产物无上游 interventions  
- **影响：** 阶段 verification 可标 passed，论文流水线仍是八段独立写文件  
- **建议：** 单 run 目录串联；后段必须读前段 hash/记录数；对写死常数做负测试

### F-02 三位置与泄漏旗标：实现坍缩，测试不败

- **严重度：** Critical  
- **状态：** confirmed defect  
- **文件/符号/行：** `events.py` `boundary_index` L74–80（`position` 不改变 `limit`）；`features.py` `select_prefix_index` L11–19（`leaks_target: False` 两处）；`tests/test_science.py` L42–46 只测 `pre_step`  
- **触发：** 任意 kind 同一 `target_char`  
- **对应要求：** POS-01；Goal §五.6  
- **复现：** 第 3 节对抗 + CE-3/CE-4。`pre_step==pre_value==post_step==0`  
- **影响：** 步前/数值前/步尾对比无法成立；前瞻泄漏可被旗标瞒过  
- **建议：** 按位置定义 limit；`leaks_target` 由 index 与 offsets 计算；测试三者不等

### F-03 P1 被线性分顶替，测试只挡单类

- **严重度：** High  
- **状态：** confirmed defect  
- **文件/符号/行：** `analysis.py` `p1_incremental` L31–37；`tests/test_science.py` L64–66；`cli.py` L188–190  
- **触发：** 两类标签任意数据  
- **对应要求：** C3-01 / 协议 §5 P1“留出 + 链长/op 控制 logistic”  
- **复现：** CLI 同输入 `delta_auc=0` 仍 `status=estimate`；测试不读该路径  
- **影响：** 主文 P1 数字可从错误估计器产出  
- **建议：** 独立 logistic/AUC oracle（CE-6）；禁止用 `+0.01*op` 冒充控制

### F-04 校准：1-p 与 max(p) 未合成；α=1 踩到 `arr[-1]`

- **严重度：** High  
- **状态：** confirmed defect（α=1 索引）；合成单位为 confirmed 缺口  
- **文件/符号/行：** `probes/calibrate.py` `sequence_score` L9–16、`conformal_threshold` L19–27、`predict_set` L30–33；`tests/test_science.py` L20–27  
- **触发：** `alpha==1` → `k=0` → `arr[-1]`；或 sequence 喂 `p_hat` 再 `predict_set`  
- **对应要求：** PROP2-01  
- **复现：** `conformal_threshold([0.1,0.2,0.3,0.4], 1.0) == {q:0.4,k:0}`  
- **影响：** 保形覆盖可静默用错分数方向；α 边界错误  
- **建议：** CE-5；`k<1` 显式 invalid；测试必须调用 `predict_set`

### F-05 联合编辑夹具自指，soundness 旗标与证据脱钩

- **严重度：** High  
- **状态：** confirmed defect（验证）；实现旗标恒 False 对 REST-03 偏保守  
- **文件/符号/行：** `measure.py` `joint_edit_counterexample` L200–209；`tests/test_measure.py` L25–32  
- **触发：** 任意 `f`，包括联合也不变  
- **对应要求：** REST-03 / PROP1-01  
- **复现：** `f≡0` 仍 `soundness_claim_allowed=False`  
- **影响：** 测试不能证明夹具真的是反例；报告器即使证据失败也“阻止宣称”  
- **建议：** CE-2 独立手算

### F-06 C-layer 缺失；C-rand 范数对照用固定 RNG(1)

- **严重度：** High  
- **状态：** confirmed defect  
- **文件/符号/行：** `interventions.py` 全文件（仅 `c_rand_delta` L31–36）；`np.random.default_rng(1)` 在 L34；测试无引用  
- **触发：** 任何 intervene CLI / 科学对照  
- **对应要求：** CAUSAL-01、IE-01、协议 C-rand/C-layer 同批次  
- **复现：** `dir` 无 layer 符号；范数目标与主干预基解耦  
- **影响：** 主效应“相对两对照的差”无法被测试或实现支撑  
- **建议：** CE-8；测试读实际范数与层选择 split=`dev`

### F-07 探针/边界头/加权 BCE 无独立测试且无训练

- **严重度：** High  
- **状态：** confirmed defect  
- **文件/符号/行：** `probes/bilinear.py` L7–29；`probes/boundary.py` 全文；`weighted_bce` L37–45；`cli.py` `cmd_fit` L145–150  
- **触发：** `reasoning-diff fit`  
- **对应要求：** PROBE-01、BOUND-01  
- **复现：** 类无 `fit`/`train`；测试套件零引用 `BoundaryMLP`  
- **影响：** 交付可声称“已实现双线性头”，实际是随机权重一次前向  
- **建议：** CE-9；手算低秩分数；unknown 掩码

### F-08 HumanEval 测试不证明隔离路径接通

- **严重度：** High  
- **状态：** confirmed defect（验证）；实现“禁止宿主 exec”本身未观察到回退  
- **文件/符号/行：** `tests/test_t3_t4.py` L29–35；`executor.py` `SpyExecutor.submit` L42–46；`t3_humaneval.py` `score_submission` L34–35  
- **触发：** `score_code(..., executor=spy)` 后不断言 `calls`；`score_submission` 无 executor  
- **对应要求：** EXEC-01、QA-01  
- **复现：** 硬编码返回 `executor_unavailable` 即可过  
- **影响：** “从不宿主 exec”未被观测，只被状态串暗示  
- **建议：** CE-11；静态/动态禁止 `exec`/`eval`

### F-09 Week8：有门槛即 `evaluated`，REST 禁句测试未喂

- **严重度：** High  
- **状态：** confirmed defect  
- **文件/符号/行：** `analysis.py` `week8_decision` L59–75；`tests/test_science.py` L56–61  
- **触发：** `gate_thresholds` 非空  
- **对应要求：** DECIDE-01、REST-01/02/03  
- **复现：** 门槛 0.9 → 三门 `evaluated`，无测量比较；`"already decided"` 能进 `forbidden_claims_blocked` 但测试不覆盖  
- **影响：** 未预注册协议被“有数字就算评估过”  
- **建议：** CE-13

### F-10 修复/干预/分析测试接受记账 stub

- **严重度：** High  
- **状态：** confirmed defect  
- **文件/符号/行：** `repair.py` `run_repair` L34–45；`tests/test_science.py` L76–80；`cli.py` L182–195  
- **触发：** 任意合法 mask + 非空 prefix  
- **对应要求：** REPAIR-01、COST-01、CAUSAL-01  
- **复现：** `generated_tokens==0`；intervene 指标写死  
- **影响：** C2/C4 交付声明若引用这些测试则虚假  
- **建议：** 声明 stub 退出验收，或 CE-14 + 真实 slot 重算

### F-11 密度/噪声测试锁定了可能不等于论文的公式，且 `build_labels` 未测

- **严重度：** Medium  
- **状态：** 未证实疑点（公式是否有意简化）；**confirmed** 为验证缺口  
- **文件/符号/行：** `measure.py` `dependency_densities` L87–98；`build_labels` L21–61；`tests/test_measure.py` L6–16；`tests/test_tracer_t1_prepare.py` L58–77  
- **触发：** 传入 `noise_set` 而非 sham 观测  
- **对应要求：** MEAS-02、C3-01 ρ_S 噪声扣除  
- **复现：** 测试手算与实现一致，但从未构造 `Observation`/`sham:`  
- **影响：** 错误的机会配对实现会被现测试固定下来  
- **建议：** CE-12

### F-12 官方 loader 测试断言硬编码元数据

- **严重度：** Medium  
- **状态：** confirmed defect（验证）  
- **文件/符号/行：** `t1_official.py` L71–73；`tests/test_t1_official.py` L15–16  
- **触发：** 只要 JSON 含键 `G`，即使误用 G 构图  
- **对应要求：** DATA-01  
- **复现：** 旗标与 `premises==['a','b']` 脱钩；后者本通道加载为真，但测试没把它和 SHARED_RNG 排除绑在一起  
- **建议：** CE-10

### F-13 tiny hook 空断言 + cache 隔离身份化

- **严重度：** Medium  
- **状态：** confirmed defect（验证）  
- **文件/符号/行：** `tests/test_tiny_hooks.py` L17；`models/collect.py` L38；`tests/test_tiny_cache.py` L7–15, L18–25  
- **触发：** 任意 `nn.Module`；第二次前向 `past=None`  
- **对应要求：** MODEL-01、Goal §五.10–11  
- **复现：** L17 恒真；`cache_isolated` 对两个对象恒真  
- **建议：** 断言 tuple/tensor 两种 output；比较 cache **内容** clone；干预后 unhooked 前向

### F-14 迁移/verbalizer/noop/T4/Hotpot 仅 happy-path 表面合同

- **严重度：** Medium  
- **状态：** confirmed defect（验证缺口）  
- **文件/符号/行：** `tests/test_science.py` L30–37, L69–73, L91–97；`tests/test_t3_t4.py` L12–18, L38–40；`t2_gsm_plus.py` L18–21（`query_reversed` ∉ `T4_STATUSES`）  
- **对应要求：** XFER-01、BASE-01/VERB-01、T2NOOP-01、DATA-02  
- **复现：** 全 1 映射；Hotpot 不更新真值；GSM-Plus reversing 状态无测试  
- **建议：** CE-7；编辑必须写出新 `answer_spec`

### F-15 大量论文符号零测试（交付若宣称覆盖则虚假）

- **严重度：** Medium（集合缺口；其中若干单项已在 F-03/06/07 升级）  
- **状态：** confirmed defect（验证覆盖）  
- **符号：** `build_labels`、`preservation_to_csp`、`_matrix_densities`、`inlp_remove`、`rescue`、`intervention_report`、`attention_rollout`、`text_predictor`、`BoundaryMLP`、`predict_set`、`repairability`、`recompute_ratio`、`cone_fit`（且 `r2` 恒 None，`analysis.py` L78–80）、`procrustes`、`retrieval_scatter`、`bootstrap_cluster`、`assign_family`、`assert_disjoint`、`completed_shard_ok`、`apply_model_template`、`card`、`forbid_host_exec`、`extract_answer`、`score_qa`  
- **对应要求：** 见第 8 节表  
- **建议：** 按 CE 补**性质/反例**测试，禁止再为堆数量写镜像断言

### F-16 冻结 hash 不含测试夹具 JSON

- **严重度：** Medium  
- **状态：** confirmed defect（审查冻结协议）  
- **文件：** `VERSION.md` scope；`tests/fixtures/*.json`  
- **影响：** 改官方答案/sidecar/T4 状态不改 `532e05a8…`，独立审查会审错“真值”  
- **建议：** hash 纳入 fixtures，或单独 pinned digest

### F-17 交付计数过期且把 39/42 passed 当阶段通过

- **严重度：** Medium  
- **状态：** confirmed defect（文档 vs 证据）  
- **文件/行：** `01-VERIFICATION.md` L1–14；`01-01-SUMMARY.md` L9  
- **复现：** 本通道 42 passed，且通过不等于正确  
- **建议：** 重跑命令入档；软件通过与科学/流水线接通分开写

### F-18 真实模型/官方转储/隔离执行器

- **严重度：** —  
- **状态：** 外部待验证  
- **说明：** tiny 随机权重不能外推 Qwen3-8B/R1-7B；HumanEval 无 Linux 隔离后端。不得把 F-08 的本机状态串写成服务器已验收。

### F-19 非缺陷建议

- **状态：** 非缺陷建议  
- `test_use_cache_false_*` 作为 transformers 5.5.3 回归说明有价值，但应改名为记录已知污染，并另加“禁止把已污染 cache 传入第二条件”的失败测试。  
- `joint_edit` 恒禁止 soundness 宣称符合 REST-03 精神；仍需独立证明夹具有效。  
- STATE.md 的 0/16 比 phase verification 更可引用。

## 11. 通道结论

| 判定 | 内容 |
|---|---|
| pytest | 42 passed，exit 0。**不能**作为 QA-01 或全链路交付证据 |
| 冻结版本 | 与声明 hash 一致（仅 .py + pyproject） |
| 测试独立性 | 部分测量/编辑/TO/swap/N/A 迁移有手算；CLI、P1、三位置、校准合成、联合编辑、隔离、修复、探针训练 **无独立有效检验** |
| Mock/桩 | 主要是 CLI 写死与记账 stub，不是 unittest.mock；危害更大 |
| 论文行为 | C-layer、logistic P1、三位置区分、标签 sham、真实干预/修复、探针训练 **缺失或被替换** |
| 交付 vs 测试 | “full CLI smoke / implemented locally / 39 passed / status passed” **超过**测试证明力 |
| 是否发现已确认问题 | **是。** Critical: F-01, F-02。High: F-03–F-10。其余见上 |
| 本通道通过？ | **不通过。** 空报告或“看起来没问题”不适用 |

修复前，任何“代码验收通过、独立审查未发现已确认缺陷”的结束语都与本通道证据矛盾。
