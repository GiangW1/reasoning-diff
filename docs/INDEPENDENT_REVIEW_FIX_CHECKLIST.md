# 独立代码与科学实验审查修改清单

**审查日期：** 2026-09-24  
**审查对象：** 当前仓库 `reasoning_diff` 代码、测试、配置、文档，以及 `Reasoning-Diff-修订方案-v4.md`   
**当前结论：** `CODE_PATHS_PARTIALLY_VERIFIED / SCIENTIFIC_VALIDITY_BLOCKED`  
**用途：** 将独立开放式审查发现的问题转成可追踪的代码、实验和文档修改项。

这份清单不把论文假说、预期数字、排期或建议当作实验结果。每一项关闭时都必须留下代码、产物或服务器运行证据。

## 使用规则

### 状态含义

- `[ ]` 未完成。
- `[~]` 有部分代码或 fixture/tiny 证据，但还不能关闭问题。
- `[x]` 已完成，并有可复查的验证证据。
- `BLOCKER`：会使科学结果无法解释或使主实验链路失效。
- `P1`：可能产生错误比较、虚假指标或不可复现结果。
- `P2`：工程、文档、统计或服务器验证缺口。

### 证据等级

每个关闭项都要标明证据等级：

1. `LOCAL_CODE_TEST`：本机代码和测试验证。
2. `FIXTURE_TINY`：fixture 或随机 tiny 模型验证，只能证明接口路径。
3. `REAL_MODEL_GPU`：真实 Qwen3-8B / DeepSeek-R1、真实 GPU 或服务器。
4. `INDEPENDENT_DATA`：独立数据、独立任务图、独立测试或人工复核。

`FIXTURE_TINY` 不能关闭需要 `REAL_MODEL_GPU` 或 `INDEPENDENT_DATA` 的项目。

## 当前基线记录

- [x] 本机完整测试：`python -m pytest -q --tb=line`，修改后结果为 `218 passed in 31.04s`。证据等级：`LOCAL_CODE_TEST`。
- [x] 工作区在审查时没有未提交修改。
- [x] offline/fixture CLI smoke 路径可以完成并写出 manifest。证据等级：`FIXTURE_TINY`。
- [~] scientific tiny 的 `prepare → collect → label → fit` 可以运行。证据等级：`FIXTURE_TINY`。
- [~] scientific tiny 的 `calibrate` 若没有独立 calibration 角色现在会写出 `status=insufficient_calibration_split`、`n_calibration_units=0`，不再把 probe_train 当 calibration；独立多题 calibration 仍待真实运行。
- [ ] 真实模型权重、官方全量数据、CUDA、自然 CoT、隔离代码执行和服务器成本均未在本机验证。
- [x] 更新 `.planning/FINAL_ACCEPTANCE.md` 的历史冻结说明和本机测试数；旧的两轮审查结论仅适用于历史 hash。证据等级：`LOCAL_CODE_TEST`。

### 本轮已落地的代码修复

- `[~]` `Observation`/`Label` 增加稳定 `task_id`；label 构造物化 generator、按任务隔离事件分组，并保留无 ID 旧 fixture 的 sham 兼容路径。新增跨任务和 generator 回归测试。证据：`LOCAL_CODE_TEST`。
- `[~]` collect 为 T3 sentence/paragraph 将局部 span 映射到渲染 prompt，并输出 `premise_spans.jsonl` 的对应记录；E 不再静默复用第一条 trace，而是显式记录跨 trace pooling。证据：`FIXTURE_TINY`；真实 T3 仍待 `INDEPENDENT_DATA`。
- `[~]` calibration 使用每个 event row 自身的 task/base key；fit/calibrate 对 scientific 的非有限 H/E 显式拒绝。证据：`LOCAL_CODE_TEST`；独立 calibration split 仍待多题运行。
- `[~]` 主干预把拟合 basis 传入 hook；scientific 模式缺少 fitted direction 时拒绝随机 basis；新增 supplied-basis 回归测试。证据：`LOCAL_CODE_TEST`；真实 hook 位置仍待 `REAL_MODEL_GPU`。
- `[~]` repair 的连续 `k` 从同一干净 prefix 开始；tiny/frozen 生成和 tokenizer offset 保存成本与 boundary fallback 证据；目录 hash 支持稳定递归摘要；统一 span answer normalization。证据：`LOCAL_CODE_TEST`/`FIXTURE_TINY`。
- `[~]` 普通 labels 不再生成伪造的 P2 base/no-op 相同密度；P3 汇总增加有效分母和 `vs_crand` 键统一；attention threshold 没有持久 dev labels 时拒绝硬编码标签；transfer 监督适配拒绝 malformed/single-class 输入。证据：`LOCAL_CODE_TEST`。
- `[~]` stage provenance 继承 upstream `source_kinds`；T1 ops 校验使用实际载入题数，fixture 被标记为 pilot，而不是硬编码为 500 题。证据：`LOCAL_CODE_TEST`/`FIXTURE_TINY`。
- `[~]` tiny forced-target 产物在 collect/fit run spec 中显式标为 `fixture/tiny_only_forced_target`；干预记录方向 hash、rank、范数、donor key、hook layer/token；INLP 不再按 label 行号切片；repair 将执行后未匹配的 task-oracle slot 标记为失败。证据：`LOCAL_CODE_TEST`/`FIXTURE_TINY`。
- `[~]` boundary MLP 没有持久化边界标签时不再用 `pre_step=1/post_step=0` 伪造监督，改为明确拒绝状态。证据：`LOCAL_CODE_TEST`。

## BLOCKER：科学结果当前不可解释

### FIX-P0-01 tiny scientific 轨迹必须停止强制追加目标赋值

- [ ] 删除或隔离 `append_target_assignment` 对 scientific 轨迹的 teacher-forcing 行为。
- [ ] tiny 路径若只用于接口 smoke，必须明确标记为 `fixture/tiny_only`，禁止进入 scientific 结果目录。
- [ ] natural trajectory 的 parse 状态只能由模型实际生成文本决定，不能为了通过校验追加目标事件。
- [ ] `parse_status="constrained_target"` 不得被当作自然轨迹或科学样本。
- [ ] 为“自然生成无事件”“目标事件缺失”“事件重复”“结构变化”分别增加失败样本和统计。
- **当前证据：** `src/reasoning_diff/models/generate.py:83`, `:296`, `:316`；本机轨迹出现 `target_assignment` 和 `constrained_target`。
- **关闭标准：** 至少一批真实模型自然轨迹在不追加目标赋值的情况下完成事件解析，报告解析覆盖率、缺失率和结构变化率。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P0-02 修正 T3 premise span 到完整 prompt 的坐标系

- [ ] 统一 premise span 的定义：要么全部是完整 prompt 坐标，要么在 collect 时显式转换，禁止混用局部文本坐标和完整 prompt 坐标。
- [ ] 保留标题、换行、chat template 和 prompt 前缀的长度映射。
- [ ] 对每个 premise 保存 `prompt_start/prompt_end`，并验证切片文本与 premise 文本一致。
- [ ] 对 HotpotQA、MuSiQue、no-op 前后变体分别做 span round-trip 测试。
- **当前证据：** `src/reasoning_diff/tasks/t3_hotpot.py:46` 将 span 重置为 0；`src/reasoning_diff/models/collect.py:96` 直接使用该 span；实际 prompt 中同一文本的首次出现位置不同。
- **关闭标准：** 所有 T3 premise 的 E pooling 能回读到对应原文；测试中不能只检查 shape 或有限值。
- **验证等级：** `LOCAL_CODE_TEST` + `INDEPENDENT_DATA`。

### FIX-P0-03 为所有 hidden、E、label 和 event row 建立稳定的样本键

- [ ] hidden row 必须携带 `trace_id`、`task_id`、`base_group_id`、`event_id`、`identity_key`、`premise_id` 和 timing。
- [ ] E 必须按 trace/task 保存，不能把第一条 trace 的 E 复用于所有 trace。
- [ ] `build_labels` 分组键必须至少包含 `base_group_id`、event identity、premise identity 和 observation protocol。
- [ ] `cmd_label` 不得把所有 label 的 `base_group_id` 设置为 `tasks[0]`。
- [ ] 跨任务写入和读取时必须按稳定键 join，禁止按行号或 first-seen 顺序 join。
- [ ] 增加两道回归测试：不同题同 event/premise 不得合并；同题多随机流必须按预定聚合规则合并。
- **当前证据：** `src/reasoning_diff/measure.py:53`, `:89` 忽略题目身份且二次迭代输入；`src/reasoning_diff/cli.py:708`, `:712`, `:806` 存在 first-trace E 和 first-task label 风险。
- **关闭标准：** 构造跨题、跨随机流、跨编辑的混合输入，输出行数、标签和 E 列均能按稳定键逐条复核。
- **验证等级：** `LOCAL_CODE_TEST` + `INDEPENDENT_DATA`。

### FIX-P0-04 主干预必须实际使用拟合出的方向

- [ ] 将 probe/inlp 拟合出的 basis 或 projector 显式传入 decode hook。
- [ ] 禁止仅传 `basis_seed` 后在 hook 内重新生成随机 basis。
- [ ] 记录实际 hook 使用的方向 hash、rank、范数、layer、token position 和 donor event key。
- [ ] `main_norm` 必须从实际干预向量计算，而不是从另一套方向计算。
- [ ] 增加测试：改变 fitted basis 但保持 seed 不变时，decode hook 的实际 delta 必须改变。
- **当前证据：** `src/reasoning_diff/cli.py:1259` 计算 basis；`src/reasoning_diff/cli.py:1381` 只传 seed；`src/reasoning_diff/models/collect.py:202` 重新创建随机 basis。
- **关闭标准：** 报告中的主干预与 hook dump 的方向、范数完全一致。
- **验证等级：** `LOCAL_CODE_TEST` + `REAL_MODEL_GPU`。

### FIX-P0-05 实现可审计的目标步骤第一个 token 前干预

- [ ] 明确保存目标 event 的 `prefix_token_ids`、目标第一个 token 边界、hook layer、residual stream 位置和 KV 更新范围。
- [ ] 证明目标内容没有进入被干预的 prefix 或 donor 表征。
- [ ] `event_aligned` 不能只改变 metadata；它必须改变实际 hook 输入和边界。
- [ ] 分开记录 `offline_hidden`、回溯式 hook、前瞻式 hook，禁止用一个 `timing` 字符串混淆三者。
- [ ] 对同一 prefix 做 baseline、main、C-rand、C-layer 的逐 token 对齐检查。
- [ ] 增加 dose curve：单层单位置、多位置、多层，并记录每个剂量点的干预范数。
- **当前证据：** `src/reasoning_diff/models/collect.py:240` 只设置 timing 元数据；`tests/test_round05_regressions.py:118` 明确 tiny 路径不能当作真正 `pre_step` 证据。
- **关闭标准：** 服务器产物能让审查者从 prefix、token、layer 和 hook log 重建干预位置。
- **验证等级：** `REAL_MODEL_GPU`。

## P1：标签、评估和实验接线问题

### FIX-P1-01 修正 scientific split 和 calibration 的目录契约

- [ ] 明确一个 stage 是否允许包含多个 split role。
- [ ] calibration 必须从完整 persisted split 中选出 calibration rows，而不是要求整个目录只包含 calibration。
- [ ] 为单题 smoke、最小多题 split、完整科学 split 分别提供可运行命令。
- [ ] 校准输入必须拒绝 test family，但不能误拒绝同目录中的 train/dev 记录。
- [ ] 记录实际 `n_calibration_units`、`n_test_units` 和 split hash。
- **当前证据：** `src/reasoning_diff/splits.py:181`；scientific tiny `calibrate` 实际报 `probe_train` 与 `calibration` 不匹配。
- **关闭标准：** 单题 smoke 可以明确返回“样本不足”而不是 pipeline exception；多题实验能完成独立 calibration。
- **验证等级：** `LOCAL_CODE_TEST` + `REAL_MODEL_GPU`。

### FIX-P1-02 校准单位必须按真实 trace/problem/sequence 分组

- [ ] 每个 prediction row 使用自身 `trace_id` 或 `base_group_id`。
- [ ] 禁止 `traces[0]["task_id"]` 作为所有 event 的 key。
- [ ] 对连续编辑使用完整编辑序列作为一个 calibration unit。
- [ ] 报告单位数、每单位 event 数、最大 nonconformity 和集合大小。
- **当前证据：** `src/reasoning_diff/cli.py:1140` 到 `:1142` 会把事件归到第一条 trace。
- **关闭标准：** 构造两题、两条 trace 的测试，校准输出必须有两个问题单位。
- **验证等级：** `LOCAL_CODE_TEST`。

### FIX-P1-03 为 probe 添加真正的 held-out 训练/开发/校准/测试流程

- [ ] probe fit 只读取 `probe_train`。
- [ ] layer、rank、方向、阈值和特征预处理只能读取 dev。
- [ ] calibration 只用于 conformal threshold。
- [ ] test 只用于最终报告。
- [ ] 输出 AUC、PR-AUC、recall、precision、F1、集合大小和 bootstrap/cluster interval。
- [ ] 报告 task head 与 behavior head 分开指标。
- [ ] `analyze` 不得用训练集重新计算 PR/F1 并将其当作泛化指标。
- **当前证据：** `src/reasoning_diff/probes/bilinear.py:65` 只返回训练 loss；`src/reasoning_diff/cli.py:1664` 重新用同一批数据分析。
- **关闭标准：** 报告中每个指标都带 `split`、`n_units` 和 `held_out=true/false`。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P1-04 重写公平的 text、attention、verbalizer 基线

- [ ] text baseline 使用与 probe 完全相同的可见 prefix、event boundary 和 premise 原文。
- [ ] 不得把 `premise_id` 当作 premise 文本。
- [ ] attention baseline 使用真实 attention map 和真实 dev label。
- [ ] 删除 hardcoded `[0, 1]` threshold label。
- [ ] verbalizer 必须定义训练、开发、测试和生成预算。
- [ ] 所有 baseline 报告相同 split、相同可见信息、相同任务标签和相同统计单位。
- **当前证据：** `src/reasoning_diff/cli.py:900`, `:906`, `:909`, `:925`。
- **关闭标准：** baseline 与 probe 的输入可见性和样本键可以逐行对照。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P1-05 实现“下一变量 → DAG”和 parser baseline

- [ ] 训练 next-variable predictor。
- [ ] 将预测变量通过独立任务 DAG 映射成 premise set。
- [ ] 在 `R_behavior` 和 `S` 上分别与行为头比较。
- [ ] parser baseline 只使用文本表面提及，不使用 hidden state。
- [ ] 预先规定步前被该 baseline 追平时的论文主张降级规则。
- **当前证据：** v4 §1、§4.2、§5 要求该 baseline；当前源码没有对应可执行模块和 CLI 入口。
- **关闭标准：** `p1_table.jsonl` 同时包含 probe、text、parser、next-variable→DAG 四类预测结果。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P1-06 让 T2-noop 真正进入数据生产流水线

- [ ] `make_noop_pair` 生成原题/no-op 配对并保存配对 ID。
- [ ] 固定 front/mid/back 和 low/medium/high 表面相关度。
- [ ] 保存独立非祖先证明、答案不变证明和新增 premise ID。
- [ ] 对 base/no-op 使用同一基础题 split 和规定的随机流。
- [ ] 产出真实 `p2_table.jsonl`，包含共同 premise 分母、新增 premise 分母、Δrho、Δacc 和污染位置。
- [ ] 普通 labels 目录不得自动生成 `base_rho == noop_rho` 的伪配对。
- **当前证据：** `src/reasoning_diff/cli.py:996` 把 base/noop 填成同一密度；`src/reasoning_diff/tasks/t2_noop.py:36` 只有未接入的构造函数。
- **关闭标准：** `p2_table.jsonl` 每一行都能回溯到两个真实 trace 和一个 no-op pair。
- **验证等级：** `INDEPENDENT_DATA` + `REAL_MODEL_GPU`。

### FIX-P1-07 完整实现 P3 的目标、非目标、任务正确性和 invalid 统计

- [ ] 每个干预 item 保存 baseline/main/C-rand/C-layer/rescue 的完整输出。
- [ ] 目标节点按 event identity 解析，不把一个全局最终答案复制给所有节点。
- [ ] INLP ablation 也必须经过同一套 outcome scorer。
- [ ] 报告任务正确率、目标响应、非目标响应、invalid、截断和执行失败。
- [ ] 保留每个问题的记录，不能只保留一行标量汇总。
- [ ] `p3_from_rows` 输出问题级区间、有效分母和失败分类。
- **当前证据：** `src/reasoning_diff/cli.py:1390`, `:1451`; `src/reasoning_diff/cli.py:1021` 只派生单行统计。
- **关闭标准：** 任意一条 P3 结论均可回溯到同一问题的四种条件和完整输出。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P1-08 扩大 R_behavior 扰动和随机流协议

- [ ] 为每个 premise 预注册允许的扰动集合 `D_j`。
- [ ] 每个扰动使用多个固定随机流，并保存变化频率而非一次性的 0/1。
- [ ] 将 `changed`、`no_change`、`structural`、`unaligned`、`parse_failed`、`unscanned` 分开统计。
- [ ] 不把一次未变化当成“没有行为依赖”。
- [ ] 保存扫描覆盖率、机会数、有效比较数和缺失原因。
- [ ] R_behavior 标签只在同一 event identity 可对齐时成立。
- **当前证据：** `src/reasoning_diff/cli.py:431` 目前只生成少量单编辑和 seed；`src/reasoning_diff/measure.py:61` 将任一 changed 聚合成行为正例。
- **关闭标准：** 结果中有每个 premise 的扰动次数、变化比例和置信区间。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P1-09 修正官方目录输入的哈希和 provenance

- [ ] 对目录生成稳定的递归 manifest hash，不能调用文件 hash API 读取目录。
- [ ] manifest 记录文件列表、相对路径、字节 hash、数据版本和 loader 版本。
- [ ] 所有 stage 的 `source_kinds` 从 upstream provenance 继承，不能硬编码成 fixture。
- [ ] `prepare` 和 `_write_stage` 使用同一套 provenance schema。
- [ ] 增加官方目录的 prepare 回归测试。
- **当前证据：** `src/reasoning_diff/cli.py:404`, `:602`；本机对目录执行 `file_digest` 得到 `PermissionError`；`_write_stage` 在 `cli.py:184` 写死 `fixture`。
- **关闭标准：** 官方目录可以 prepare、resume，并且 manifest 能在另一台机器重建。
- **验证等级：** `LOCAL_CODE_TEST` + `INDEPENDENT_DATA`。

### FIX-P1-10 让 T1 的 500 题和 op 网格检查真实反映输入

- [ ] `validate_t1_prepare_config` 使用实际任务数，不得硬编码 `n_problems=500`。
- [ ] 记录实际 `op` 分布、题数、seed 数和每个 family 数量。
- [ ] 500 题不足时明确失败或标记为 pilot，不能通过配置检查伪装为 500 题。
- [ ] 每个基础题及其变体共享 family split。
- **当前证据：** `src/reasoning_diff/cli.py:429` 传入固定 `500`；当前 fixture 只有 tiny 题。
- **关闭标准：** run spec 的题数与 tasks、traces、labels、test units 的实际数量一致。
- **验证等级：** `INDEPENDENT_DATA`。

### FIX-P1-11 修正连续 repair 的 k=1…5 语义

- [ ] 每个 k 从同一干净 retained prefix 开始，不能使用上一轮已经带 marker 的文本。
- [ ] `slots[:k]` 必须与当前文本中的真实 slot 一一对应。
- [ ] mask 未匹配时应显式失败，不能通过拼接 `[mask:...]` 继续生成并记为成功。
- [ ] 增加 k=1、k=2、k=5 的文本、slot、prefix hash 回归检查。
- **当前证据：** `src/reasoning_diff/repair.py:68`, `:298`；当前实现会把 `rec.text` 作为下一轮 `current`。
- **关闭标准：** k 曲线只表示“同时重算 k 个原始槽位”，不包含上一轮人工 marker。
- **验证等级：** `LOCAL_CODE_TEST` + `REAL_MODEL_GPU`。

### FIX-P1-12 repair 必须有任务正确性和真实 prefill 证据

- [ ] tiny/frozen repair 都输出逐步合法率、最终答案正确率和与 full recompute 的一致率。
- [ ] `refilled_prefix` 只能在真实 hidden shape、dtype、token length 和 model provenance 全部通过时为 true。
- [ ] 不接受任意非空 list 作为 prefill hidden。
- [ ] frozen repair 检查第一次 prefill 后的 KV 是否被重复 prefill 或重复计费。
- [ ] HumanEval repair 必须使用同一个隔离 executor 和同一个测试预算。
- **当前证据：** `src/reasoning_diff/repair.py:130`, `:237`; 当前 tiny repair 只返回 token 数和 hidden 存在性。
- **关闭标准：** repair report 中每条记录都有 answer、legal、full_recompute_match、invalid 和 cost 字段。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P1-13 明确 T3 独立任务图和 HumanEval executor 边界

- [ ] HotpotQA/MuSiQue 没有完整图时必须保持 `R_task=null` 或 partial，不得用 supporting facts 冒充完整 DAG。
- [ ] sidecar 图必须有版本、生成方法和人工复核记录。
- [ ] HumanEval 默认 unavailable 时不能生成代码正确率数字。
- [ ] 真实 executor 必须具备 timeout、资源隔离和 host exec 禁止证明。
- **当前证据：** `src/reasoning_diff/tasks/t3_hotpot.py:34` 标记 supporting facts 不是完整 DAG；服务器 runbook 将 HumanEval executor 留为 pending。
- **关闭标准：** T3 报告明确列出每个任务的 graph status、truth source 和可评估比例。
- **验证等级：** `INDEPENDENT_DATA` + `REAL_MODEL_GPU`。

### FIX-P1-14 修正 sham/noise 与 S/M 的共同支持集

- [ ] sham 必须和真实 observation 共享明确的 event、premise 和 scan protocol。
- [ ] noise hits 不能只保留 `sham:*` premise 后再丢失到真实 premise 映射之外。
- [ ] `rho_S_raw`、`rho_M_raw`、noise reference 和 signed excess 分开保存。
- [ ] 共同支持为空时返回 null，并保留 `null_reason`、有效机会数和覆盖率。
- [ ] 不得把负差值截成 0，也不得把有限扫描结果称为真实依赖真值。
- [ ] `build_labels` 支持 list 和 generator 时结果必须一致，或显式物化输入。
- **当前证据：** `src/reasoning_diff/measure.py:89` 二次迭代 `Iterable`；generator 输入时 sham noise 会从 `1.0` 变成 `None`。
- **关闭标准：** list/generator、空支持集、结构变化和 unaligned case 都有等价回归测试。
- **验证等级：** `LOCAL_CODE_TEST` + `INDEPENDENT_DATA`。

### FIX-P1-15 加强事件解析、身份对齐和 token boundary

- [ ] 对自然 CoT 中重复赋值、回溯、alias、同名实体、作用域和版本号增加人工复核集。
- [ ] event identity 不得由数值相等决定。
- [ ] 对 added/removed/merged/route-change 事件保存结构 taxonomy 和覆盖率。
- [ ] token boundary 必须报告跨界 token、special token 和 offset reconstruction 失败数。
- [ ] `offsets_from_tokenizer` 找不到 piece 时不能静默用 cursor 代替而不报警。
- [ ] 事件解析失败不能进入 probe 或干预分母。
- **当前证据：** `src/reasoning_diff/events.py:27`, `:236`; `src/reasoning_diff/models/tokenize.py:29` 使用单 token `decode + find`。
- **关闭标准：** 输出包含 aligned、unaligned、structural、parse_failed 和 boundary_failed 的逐类计数。
- **验证等级：** `INDEPENDENT_DATA` + `REAL_MODEL_GPU`。

### FIX-P1-16 统一答案评分协议

- [ ] numeric、text、span、short、code 使用各自的 canonicalization 和 scorer。
- [ ] span answer 支持别名、大小写、标点和数据集规定的等价形式。
- [ ] code answer 只在 executor 有效时计算正确率。
- [ ] `Trace.correct` 为 null 时必须保留原因，不能默认 false 或 true。
- [ ] intervention、repair、P3 使用同一个答案 scorer，不能统一调用 numeric extractor。
- **当前证据：** `src/reasoning_diff/events.py:245`; `src/reasoning_diff/models/generate.py:221` 使用直接字符串相等。
- **关闭标准：** 每条结果有 `answer_raw`、`answer_normalized`、`gold_normalized`、`score_status` 和 `correct`。
- **验证等级：** `LOCAL_CODE_TEST` + `INDEPENDENT_DATA`。

### FIX-P1-17 填充完整成本统计

- [ ] 记录 decode tokens、额外 prefill tokens、probe time、scheduling time、index time、wall time 和 GPU utilization。
- [ ] 预填充、生成、探针、索引和端到端阶段使用统一计时器和同步规则。
- [ ] tiny/frozen 结果不能把默认零值当成已测成本。
- [ ] repair 的 full recompute、oracle、predicted mask、random mask 使用相同硬件、精度、batch 和 context protocol。
- **当前证据：** `src/reasoning_diff/schema.py:294`; `src/reasoning_diff/models/generate.py:222` 只填少数 Cost 字段。
- **关闭标准：** 每个成本数字都有非零/零的原因、计时范围和硬件配置。
- **验证等级：** `REAL_MODEL_GPU`。

### FIX-P1-18 完成 transfer 的入口、留出评估和几何边界

- [ ] 增加明确的 `transfer` CLI 或等价 stage，不再要求手工准备 `transfer_pairs.npz`。
- [ ] direct transfer、unlabeled pair adaptation、supervised adaptation 分开报告。
- [ ] 所有 map、PCA、Procrustes、标准化和特征选择只在 transfer train 上拟合。
- [ ] transfer test 不得复用 paired rows。
- [ ] 监督适配不能只把每个样本映射到 label class mean；需要明确模型和统计目标。
- [ ] `common_dim_then_procrustes` 不得按行数静默截断未验证配对；必须保存 pair IDs。
- [ ] Qwen3-8B 4096 与 R1 3584 的 direct mismatch 必须明确标为 not applicable，而不是性能数字。
- **当前证据：** CLI 没有 `transfer` 子命令；`src/reasoning_diff/cli.py:1605` 只读取外部文件；`src/reasoning_diff/transfer.py:19`, `:74` 无 held-out 约束。
- **关闭标准：** 报告包含 model/revision/dim、pair count、label use、split、held-out metric 和 not-applicable reason。
- **验证等级：** `REAL_MODEL_GPU` + `INDEPENDENT_DATA`。

### FIX-P1-19 完善 P1–P3 统计和决策键

- [ ] P1 输出链长、op、难度控制后的 held-out AUC、增量 AUC、偏相关和问题级 bootstrap interval。
- [ ] P2 输出配对 Δrho、Δacc、共同分母、新增 premise 分母和污染位置分布。
- [ ] P3 输出相对 C-rand/C-layer 的效应、非目标响应、invalid rate 和问题级 interval。
- [ ] P2/P3 不能只用跨问题平均值；保留每题 row 和失败分母。
- [ ] 明确多重比较、停止规则和功效分析。
- [ ] 修正 `week8_decision` 的指标键，使 P3 输出 `vs_crand` 与 decision gate 使用同一字段。
- [ ] Gate 0–2 在正式预注册前保持 `unregistered`，不能根据结果临时加阈值。
- **当前证据：** `src/reasoning_diff/analysis.py:124`, `:208`, `:285`；当前 gate 使用 `p3_vs_crand`，P3 汇总使用 `vs_crand`。
- **关闭标准：** 每个统计量都带统计单位、有效样本数、区间方法、比较方向和 preregistration ID。
- **验证等级：** `INDEPENDENT_DATA`。

### FIX-P1-20 完成三种时间位置的真实比较

- [ ] 依赖 probe 在 `pre_step`、`pre_value`、`post_step` 三个位置分别训练和评估。
- [ ] 三个位置使用相同任务、相同 event identity、相同 split 和相同 rank/超参数协议。
- [ ] 不能只把三组数组写入 NPZ，却只用 `H` 拟合。
- [ ] 报告每个位置的 task head、behavior head、S、M 和 next-variable baseline 指标。
- **当前证据：** `src/reasoning_diff/models/collect.py:107` 会写三种 H；`src/reasoning_diff/cli.py:835` 默认只读取 `H`。
- **关闭标准：** Fig. 2b 或对应产物可以直接从 stage 文件重建三位置比较。
- **验证等级：** `REAL_MODEL_GPU`。

### FIX-P1-21 修正 C-rand、C-layer、ablation、rescue 和剂量协议

- [ ] C-rand 与主干预使用同层、同 token、同 rank、同实际范数和同采样流。
- [ ] C-layer 的弱层只能由 dev set 预先选择，不能从 test 结果反推。
- [ ] C-layer 方向和主方向的构造方式必须写入产物。
- [ ] swap、INLP knockout、rescue 都报告 baseline/main/C-rand/C-layer。
- [ ] rescue 增加 error-source、matched、random 和 identity-reconstruction 对照。
- [ ] 所有失败、截断、invalid 和无效 donor 留在分母中。
- [ ] 记录多剂量点，而不是只记录一个 scalar mean。
- **当前证据：** `src/reasoning_diff/cli.py:1270`, `:1279`, `:1431`; 当前 dev layer 可缺省、主方向和实际 hook 方向也不一致。
- **关闭标准：** 每个剂量点有成对 control、实际 norm、位置、层和完整 outcome matrix。
- **验证等级：** `REAL_MODEL_GPU`。

### FIX-P1-22 完善 INLP 输入检查和行为标签对齐

- [ ] INLP 输入必须检查 labels 为二元、有限、与 hidden row 稳定键一一对应。
- [ ] 禁止用 `lab_rows[:matrix.shape[0]]` 这种按行号切片代替 key join。
- [ ] two-row fallback 必须单独标记为 smoke-only，不能进入科学汇总。
- [ ] INLP 输出必须经过同一任务/行为 scorer 和 control protocol。
- **当前证据：** 当前 intervene 路径存在 two-row fallback，标签和 hidden 的 join 可能依赖行顺序。
- **关闭标准：** 删除 fallback 或将其严格隔离到 fixture 测试；科学报告中没有 fallback 样本。
- **验证等级：** `LOCAL_CODE_TEST` + `REAL_MODEL_GPU`。

### FIX-P1-23 使用真实边界真值训练 boundary detector

- [ ] boundary detector 的正负标签来自任务步边界或人工复核边界，不能只把 `H_pre_step` 标成 1、`H_post_step` 标成 0。
- [ ] `pre_value`、`post_step` 和真正的 step boundary 要分别定义，不能把位置名称当成监督真值。
- [ ] 检查 boundary 输入中的 NaN、空事件、重复边界和跨界 token。
- [ ] 在独立问题和独立模型上报告 boundary precision、recall、F1 和误差位置。
- [ ] boundary detector 的训练、层选择和阈值选择不能读取最终测试标签。
- **当前证据：** `src/reasoning_diff/cli.py:936` 使用预先拼接的 pre/post 数组和人为 1/0 标签；没有真实 boundary annotation。
- **关闭标准：** 产物包含每个 boundary 的文本位置、token 位置、真值来源和误差分类。
- **验证等级：** `INDEPENDENT_DATA` + `REAL_MODEL_GPU`。

### FIX-P1-24 修正多任务 prepare、source/value pair 和 edit provenance

- [ ] `prepare` 对每一个输入 task 生成独立的 edit、trace、observation、label 和 split row。
- [ ] source/value pair 必须保存 base、same-source/different-value、same-value/different-source 的完整 task/event 对齐。
- [ ] 不得用第一条 task 的 premise、answer、ancestor 或 base group 解释后续 task。
- [ ] 每种 edit 都记录是否 exhaustive、允许的扰动集合、随机流和独立真值来源。
- [ ] 无法生成完整 pair 时返回结构化缺失状态，不用单条 pair 继续生成科学汇总。
- **当前证据：** `src/reasoning_diff/cli.py:371` 先取 `tasks[0]`；后续 task 处理和 `_observations` 仍需要稳定键、独立 E 和独立 label 约束。
- **关闭标准：** 多任务 stage 中任何 row 都能通过 `task_id/base_group_id/edit_id/trace_id` 唯一回溯。
- **验证等级：** `LOCAL_CODE_TEST` + `INDEPENDENT_DATA`。

## P2：工程、复现和文档问题

### FIX-P2-01 隔离随机数流和成本影响

- [ ] 不要在每条 trace/intervention 中用 `torch.manual_seed` 重置全局 RNG。
- [ ] model weight、sampling、direction、perturbation、split 和 repair 分别使用命名 RNG stream。
- [ ] 记录每个 stream 的 seed 和消费顺序。
- [ ] `decode_loop` 中 logits 在 CPU/GPU 间移动时，要把传输时间和设备记录写入 Cost。
- **当前证据：** `src/reasoning_diff/models/generate.py:286` 等路径重置全局 seed；CPU generator 与模型设备之间的传输成本未纳入报告。
- **关闭标准：** 改变一个 stream 不会改变其他 stream 的结果，且成本记录包含设备传输。
- **验证等级：** `LOCAL_CODE_TEST` + `REAL_MODEL_GPU`。

### FIX-P2-02 校验冻结 checkpoint 的结构与 model card

- [ ] 加载后检查 hidden size、layer count、context limit、tokenizer special IDs 与 card 一致。
- [ ] 将实际 model config、tokenizer revision、dtype、device 和 attention backend 写入 run spec。
- [ ] revision 一致但结构不一致时必须失败，不能只信 card 元数据。
- **当前证据：** adapter 有固定 revision/card，但当前主要依赖 card 字段。
- **关闭标准：** 错误 checkpoint 在 preflight 阶段被拒绝。
- **验证等级：** `REAL_MODEL_GPU`。

### FIX-P2-03 实现 analyze 中的 embedding 路径或明确删除入口

- [ ] `embed_a.npy` 分支不能只有 `pass`。
- [ ] 如果保留 retrieval scatter，明确 embedding 来源、模型、归一化和 pair split。
- [ ] BOW fallback 必须与 provided embedding 明确分开，并在报告中标记。
- **当前证据：** `src/reasoning_diff/cli.py:1649` 是空实现。
- **关闭标准：** analyze 只在有完整输入时输出 retrieval 结果，否则返回带原因的 null。
- **验证等级：** `LOCAL_CODE_TEST` + `INDEPENDENT_DATA`。

### FIX-P2-04 修正 Procrustes 的配对和截断语义

- [ ] 保存并检查 source/target pair IDs。
- [ ] row 数不一致时显式失败或按 key join，不得静默取 `min(n)`。
- [ ] PCA、中心化和 Procrustes 只在 transfer train 拟合。
- [ ] 输出 pair count、discarded IDs、common dim 和 held-out geometry error。
- **当前证据：** `src/reasoning_diff/transfer.py:74` 会按行数取最小值并直接拟合。
- **关闭标准：** 任何截断都产生显式 discarded report，不能作为正常迁移结果。
- **验证等级：** `INDEPENDENT_DATA`。

### FIX-P2-05 修正 provenance 和 stage metadata 漂移

- [ ] `_write_stage` 不再写死 `source_kinds: {"cli": "fixture"}`。
- [ ] label、fit、calibrate、intervene、repair、analyze 都继承 upstream source kind、model kind、weight source 和 eval mode。
- [ ] manifest 中记录输入 artifact hash、代码版本、schema version 和 run spec digest。
- **当前证据：** `src/reasoning_diff/cli.py:184`。
- **关闭标准：** 任意下游 artifact 都能从 manifest 追溯到真实输入和模型来源。
- **验证等级：** `LOCAL_CODE_TEST`。

### FIX-P2-06 更新过时的验收文档和命令

- [ ] `.planning/FINAL_ACCEPTANCE.md` 的测试数量、commit hash 和可执行命令与当前仓库一致。
- [ ] 删除或修正不存在的 `transfer` CLI 命令。
- [ ] README 明确 scientific tiny 是随机权重 smoke，不是 MODEL-01。
- [ ] 文档把“代码路径可运行”和“科学实验已验证”分成两个状态。
- [ ] 每次代码修改后重新生成 test count 和 server pending 清单。
- **当前证据：** README 和 FINAL_ACCEPTANCE 的边界声明总体诚实，但命令和测试数量已经漂移。
- **关闭标准：** 从干净 checkout 按 README 执行的每条命令都存在，或明确标注为 server-only。
- **验证等级：** `LOCAL_CODE_TEST`。

## v4 T1–T4 / C1–C4 对照清单

| v4 项目 | 修改前状态 | 关闭条件 |
|---|---|---|
| T1 iGSM | fixture/loader 有；官方目录 hash 和真实 500 题未完成 | 官方数据、op 网格、500 题、family split、自然轨迹产物齐全 |
| T2 GSM-Symbolic/GSM-Plus | adapter 有；多项 graph/answer truth 需独立验证 | 数据版本、编辑协议、独立真值、自然模型轨迹和留出结果齐全 |
| T2-noop | 构造函数有；没有 producer 和 P2 真实配对 | 原题/no-op 配对、front/mid/back、surface strata、共同分母和 Δ 指标齐全 |
| T3 Hotpot/MuSiQue/HumanEval | adapter 有；图真值和 executor 不完整 | sidecar/人工复核、正确 span、隔离 executor 和独立评分齐全 |
| T4 boundary | adapter 有；没有真实失效相图 | 失效类型、边界扫描、策略突变和无解样本有独立真值 |
| C1 前瞻识别 | head 可训练；无 held-out 和关键 baseline | 三位置、task/behavior、next-variable、parser、text、attention 全部留出评估 |
| C2 因果控制 | hook/swap/ablation/rescue 接口有；方向/位置不闭合 | exact prefix、target first token、layer/KV、donor、主干预和两类 control 可复查 |
| C3 虚假依赖 | S/M helper 有；P1/P2/P3 数据缺失 | noise-corrected S/M、P1、真实 P2、真实 P3、问题级区间齐全 |
| C4 局部修复 | tiny repair scaffold 有 | Oracle/predicted/matched/random、答案正确、合法率、一致率和成本齐全 |
| `R_task` | T1 fixture 可用；T3/T4 partial/unknown | 任务图来源、版本、完整性和未知边界明确 |
| `R_behavior` | 单编辑、小随机流、有限扫描 | 扰动集合、重复随机流、变化频率、结构变化和覆盖率齐全 |
| S/M | 公式和 null 处理存在 | 共同支持、噪声参照、原始值、signed excess 和有效分母可复核 |
| 三种时间位置 | 数组会写出；probe 只用 H | 三位置相同 split、相同标签、相同统计协议的比较产物齐全 |
| 探针 | 可拟合；只有训练 loss | held-out AUC、PR/F1、集合大小、interval 和 split provenance 齐全 |
| 基线 | text/attention 部分不公平；next-variable 缺失 | 相同可见前缀、parser、next-variable、attention、text、verbalizer 全部可运行 |
| 校准 | helper 有；CLI 单 fixture 失败且单位可能串用 | calibration/test split、full trace/sequence unit、coverage、set size 齐全 |
| 迁移 | 工具函数有；无 CLI/留出结果 | direct/unlabeled/supervised 分开、pair IDs、held-out、dimension mismatch 明确 |
| swap/ablation/rescue | 接口有；主方向和 outcome 不可靠 | 每个条件有目标/非目标/任务/invalid/rescue 结果 |
| C-rand/C-layer | 有函数名；公平性和剂量未证明 | 同层同位置同维同范数、dev 选层、每个剂量点成对运行 |
| P1 | helper 有；无 table producer | held-out AUC、链长/op control、问题级 bootstrap interval |
| P2 | helper 有；默认可能生成伪 pair | 真实 no-op pair、共同/新增分母、Δrho、Δacc、位置分布 |
| P3 | helper 有；单行派生统计 | per-problem outcomes、C-rand/C-layer、invalid、non-target、interval |
| 局部修复 | 生成 token 和 prefill metadata | 逐步合法率、答案、full recompute 一致率、失败分类、成本 |
| 成本 | schema 有；大量字段为零 | decode/prefill/probe/scheduling/index/E2E 和硬件配置齐全 |

## 关闭前必须执行的验证

### 本机回归

- [ ] `python -m pytest -q --tb=line`
- [ ] list/generator labels 等价性测试。
- [ ] 跨任务同 event/premise 不串 label 测试。
- [ ] T3 prompt span round-trip 测试。
- [ ] official directory prepare/resume 测试。
- [ ] scientific single fixture 明确返回样本不足，不产生未声明 scientific 结果。
- [ ] calibration 两题两 trace 单位测试。
- [ ] repair k=1…5 prefix 独立性测试。
- [ ] intervention fitted-basis 与实际-hook delta 一致性测试。
- [ ] `--help` 中的每条文档命令都存在。

### 真实模型/服务器验收

- [ ] 记录 GPU、CUDA、dtype、attention backend、model revision、tokenizer revision。
- [ ] 运行真实自然轨迹，禁止 forced target assignment。
- [ ] 运行 T1 pilot，再运行注册的 500 题/op 网格。
- [ ] 运行 T2-noop 配对和独立任务图检查。
- [ ] 运行三位置 probe、四类 baseline 和 held-out test。
- [ ] 运行 C2 主干预、C-rand、C-layer、INLP、rescue 和 dose curve。
- [ ] 运行 P1、P2、P3，保存逐题明细和失败分母。
- [ ] 运行 repair correctness/cost matrix。
- [ ] 运行跨模型 transfer；对 4096/3584 维 direct transfer 明确报告不适用。
- [ ] 若运行 HumanEval，保存 executor isolation、timeout 和测试版本。

## 结果发布前的禁止事项

- [ ] 不把 `218 passed` 写成论文实验通过。
- [ ] 不把 tiny 随机权重写成 Qwen3-8B 或 R1 结果。
- [ ] 不把 `constrained_target` 写成自然 CoT 解析结果。
- [ ] 不把训练 loss、同训练集 PR/F1、伪 P2 row 或单次干预输出写成泛化或因果证据。
- [ ] 不把 `Gate unregistered` 写成 pass/fail。
- [ ] 不把 v4 的目标数字、预期层、预期恢复率或排期写成已获得结果。
- [ ] 所有 null、unknown、unaligned、structural、invalid、executor unavailable 和 split mismatch 必须保留在结果中。

## 建议的实现顺序

1. 先完成 `FIX-P0-01` 至 `FIX-P0-05`，否则任何 hidden/probe/intervention 数字都不应进入科学报告。
2. 再完成 stable row identity、T3 span、split/calibration、held-out probe 和公平 baseline。
3. 然后接通 T2-noop、P1–P3、三位置和 C-rand/C-layer 真实产物。
4. 最后运行 transfer、repair、HumanEval、成本统计和 T3/T4 扩展。
5. 只有当服务器证据和独立数据满足对应关闭条件后，才更新 v4 的实验结论或 Gate 状态。
