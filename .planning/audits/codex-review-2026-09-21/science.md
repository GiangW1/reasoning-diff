---
phase: codex-review-2026-09-21
reviewed: 2026-09-21
depth: deep
files_reviewed: 8
files_reviewed_list:
  - src/reasoning_diff/analysis.py
  - src/reasoning_diff/baselines.py
  - src/reasoning_diff/transfer.py
  - src/reasoning_diff/probes/bilinear.py
  - src/reasoning_diff/probes/calibrate.py
  - src/reasoning_diff/probes/boundary.py
  - src/reasoning_diff/probes/__init__.py
  - src/reasoning_diff/cli.py
findings:
  critical: 12
  warning: 1
  info: 0
  total: 13
status: issues_found
---

# 独立科学计算与实验数据流审查

## Narrative Findings (AI reviewer)

按原始修订方案及 `docs/EXPERIMENT_PROTOCOL.md` 检查科学计算实现；未使用 Cursor 验收报告作为证据。CLI 范围为 fit/calibrate/analyze 及相邻输入连接。以下是软件实现缺陷，不能通过补跑 GPU 实验解决。所有路径相对于 `C:/Users/22688/Desktop/diff/`。

## Critical Issues

### CR-S01 — BLOCKER / P1：行为头校准实际使用任务祖先，并把未知标签当作已知

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/cli.py:765-810`，尤其 802–810。

**Issue:** 默认拿 `probes.jsonl` 第一个有 U 的模型，正常 fit 输出顺序意味着只校准任务头。即使提供行为头，真依赖列仍先限制在任务 DAG 祖先；标签通过 `task_label == 1 or behavior_label == 1` 混用。这样必然排除 `R_behavior \\ R_task`，正好丢掉 C3 的研究对象。无正标签时回退至 DAG，并无条件传 `labels_known=True`；缺少标签甚至仍产生有限校准阈值。输出也没有 head 标识，无法分开消费两个头的阈值。

**Verified reproducer:** 一层 rank-1 behavior probe：U=V=[[1]]、b=0；H 为 3×1 全 1，E=[[log(9)],[-log(9)]]；三个 problem 各有事件 q。任务 q 的 parents=['p1']；标签 p1=(task=1,behavior=0)，p2=(task=0,behavior=1)。运行 scientific calibrate 得到 scores=[0.1,0.1,0.1]、q=0.1；行为真依赖 p2 的预测概率是 0.1，正确 scores 与 q 应均为 0.9。删除 labels.jsonl 后再跑仍返回相同 finite q。反例输出保存在 `%TEMP%/rd_science_review_r00kank8/cal_output/` 和 `cal_missing/`。

**Fix:** 显式选择并分别保存 head；按事件/前提身份只使用该头的标签；行为真集不得受任务祖先约束；未知或不完整的校准单位应明确排除/拒绝并记覆盖对象，不得转成已知空集或 DAG 真值。

### CR-S02 — BLOCKER / P1：探针 F1 依赖标签文件排列，缺失项被强行补零

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/cli.py:1146-1154`。

**Issue:** 将 H×E 预测矩阵直接 flatten，取 label 文件顺序中的 task_label 配对；完全未用 event_id/premise_id/trace_id 连接。未知标签过滤后也没有同步筛选预测列，长度不足时补 0 进一步掩盖身份缺失。即使全部预测正确，调整 JSONL 行顺序就改变结果。

**Verified reproducer:** 一个事件、两个前提，p_hat=[0.9,0.1]，p1.task_label=1、p2.task_label=0。分析 [p1,p2] 顺序得到 F1=1、TP=1；仅将相同标签行反转得到 precision=recall=0、FP=FN=1、F1=null。输出在上述临时目录 `eval_a/`、`eval_b/`。

**Fix:** 通过明确的 feature row/column 身份连接标签，构造相同 known mask；缺失对应项应显式报告；按 head 分开评价；增加标签行排列不变性的回归测试。

### CR-S03 — BLOCKER / P1：P2/P3 静默只分析 JSONL 第一行，结论随行序翻转

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/cli.py:1112-1126`。

**Issue:** 两个表均使用 `read_jsonl(...)[0]`，后续题目全部丢弃；没有多行拒绝提示、题目级聚合或置信区间。原规范要求配对问题和问题级不确定性，因此不能把第一道题输出当成整批实验结果。

**Verified reproducer:** 供给有效 P1 table 和 densities.rho_S_excess=0.1。P2 两行分别为 (base_rho,noop_rho,base_acc,noop_acc)=(0,1,1,0) 与 (1,0,0,1)，共同前提均 ['p1']。P3 两行为 (main,crand,clayer)=(1,0,0) 与 (0,1,1)。预期总体差值都为 0；实际第一种顺序 P2 Δrho=+1、P3 vs_crand=+1，反转顺序两者均为 −1。输出：`%TEMP%/rd_science_p23_11da02hj/out0/`、`out1/`。

**Fix:** 消费所有逐题记录，验证配对身份与完整条件，按题聚合并做问题级 bootstrap；若只支持预聚合的单行汇总，必须拒绝多行并要求样本量/聚合协议，不能静默截断。

### CR-S04 — BLOCKER / P1：P1 允许同一问题同时训练和测试，却标记为 held-out

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/analysis.py:60-86`、`196-206`；CLI 来源 `cli.py:1098-1101`。

**Issue:** groups 只用于 bootstrap，不验证 train/held_out 两侧的 problem IDs 不相交。同题改名、no-op 或不同随机流若分别标为训练和测试，会被当作真正留出样本，bootstrap 又把泄漏关系一起重采样。实验协议明确规定基础题共组。

**Verified reproducer:** n=12，length=op=1，y=rho=[0,1]*6；前六行训练、后六行 held_out；groups=[str(i%6) for i in range(12)]。调用 p1_incremental 返回 held_out=True、auc_full=1、delta_auc=0.5、bootstrap interval=[0.5,0.5]，没有拒绝六个重复问题。这里不是声称随机数据证明增益虚假，而是验证其宣称的留出条件根本未成立。

**Fix:** 拟合前验证各 problem/base_group 只有一种角色；缺失问题身份不得默认为独立行；对不相交的题目组实施划分及 bootstrap。

### CR-S05 — BLOCKER / P1：无标签映射拟合时中心化，应用时漏掉均值平移

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/transfer.py:31-50`。

**Issue:** 用 centered target/source 求旋转或最小二乘，却只保存 W；apply_map 返回 vectors@W，丢失两侧均值。不同模型 activation 均值不同的正常情况会让适配输出处于错误坐标系，并污染双线性得分。

**Verified reproducer:** target=[[0,0],[1,0],[0,1],[1,1]]，source=target+[10,-5]。fit_linear_map(...,labeled=False) 学得单位矩阵，apply_map(target) 仍输出 target；预期应精确恢复 source。两者每行均差 [10,-5]。

**Fix:** 保存 target_mean/source_mean，应用 `(vectors-target_mean)@W+source_mean`；H 与 E 两路均验证平移和旋转的组合反例。

### CR-S06 — BLOCKER / P1：所谓监督适配在平衡标签上完全忽略监督

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/transfer.py:25-29`。

**Issue:** 标签只转成 `sqrt(abs(y-mean(y))+0.1)` 的样本权重；平衡二元标签下所有权重均为 sqrt(0.6)，结果与任何标签排列都无关。没有依赖预测损失或使用类别信息的适配头，却输出 status=supervised_adapt、uses_labels=True。这不能提供协议要求的监督适配对照。

**Verified reproducer:** 相同 source/target，labels=[0,0,1,1] 和 labels=[0,1,0,1] 两次拟合，W 完全相同；由公式可知任意平衡排列均如此。

**Fix:** 用真实依赖标签优化适配后的 probe/适配器，记录拟合角色与目标；若仅保留标签派生的加权几何映射，必须按实际算法另名并补齐监督适配，不得作为它的替代。

### CR-S07 — BLOCKER / P1：迁移报告固定返回两个写死的维度，没有实际迁移评价路径

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/cli.py:1090`、`1159`、`1173-1233`；`transfer.py:9-16`。

**Issue:** 所有 analyze 都调用 direct_transfer(4096,3584)，不读取源/目标模型、特征维度、映射或测试得分。即使输入是同维的 rank-1 小模型，也声称 4096→3584 不适用。direct_transfer 本身只比较整数；fit_linear_map/apply_bilinear_inputs 无生产调用者，CLI 无迁移命令。缺失的是可执行的直接/无标签/监督三种评估流程，而非尚缺服务器测量结果。

**Verified reproducer:** CR-S02 的真实 H/E 均为一维，两个 analyze 输出都固定为 source_dim=4096,target_dim=3584,status=not_applicable_dimension_mismatch。全源搜索只见 transfer helper 被测试调用。

**Fix:** 以实际模型/特征清单决定兼容性；连接三种迁移模式到固定源探针和目标留出标签，输出实测指标及身份。无对应输入时输出 not_evaluated，而不是写死的兼容性结果。

### CR-S08 — BLOCKER / P1：C3 没有从采集结果形成 P1–P3 实验表的数据管线

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/cli.py:1084-1085`、`1112-1126`；`analysis.py:114-188`。

**Issue:** 全源与 scripts 搜索，p1_table/p2_table/p3_table 仅有 analyze 的读取，没有生产者。label 产出 densities，intervene 产出干预明细，却都不能进入 P2/P3。p2_paired 只减调用者给的四个标量，不能从事件集合重算共同分母、污染位置/新增前提统计，也不计算 Δrho 与 Δacc 关联；p3_recovery 只减调用者给的正确率，没有逐题控制比较和区间。甚至缺失 invalid_rate 被 CLI 默认为 0.0，使缺失证据看似零无效输出。

**Evidence:** `rg -n 'p1_table|p2_table|p3_table' src scripts` 只返回上述三个读取点；CR-S03 可在没有任何实际干预输出的情况下让两个手写 summary 产生正/负恢复结果。完整常规 CLI 链只得到 null P1/P2/P3，无法由本软件已有实验产物执行这些检验。

**Fix:** 从 problem/trace/event/premise 键连接正确率、噪声协议、行为/任务标签、no-op 配对及每题每条件干预结果，生产可审计逐题表；P3 未观测的指标保持 null；在这些表上实现关联、分层、共同支持和问题级区间。与 CR-S03 的区别是这里缺少上游实验连接，CR-S03 是已有多行表仍被错误截断。

### CR-S09 — BLOCKER / P1：scientific fit 没有公平文本/注意力/自述基线，边界头也不可用

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/cli.py:659-682`；`baselines.py:24-46`；`probes/boundary.py:25-44`。

**Issue:** scientific 分支无条件输出四项 refused_not_section8；同监督文本预测器根本没有调用。切换 fixture 只得到重放 80 字前缀的 verbalizer、空注意力、2×2 identity rollout 和 [0.1,0.9] 的固定 dev 示例，不能填补科学基线。BoundaryMLP 只收到全 1 标签，训练 5 步后只保存 loss，不保存权重，也没有下游加载/使用；因此无法区分边界与非边界。规范 C1 基线与逐 token 边界训练所需的软件未完成。

**Evidence:** 代码分支是无条件的；`rg` 显示 fit_text_predictor 无 CLI 调用，BoundaryMLP 只有此处生产调用。相关回归测试仅断言四个 refused 状态，不能证明需求实现。此项没有把诚实的 refused 状态误解为伪造成功，而是指出原计划所需能力缺失。

**Fix:** 用同样的 problem split、边界前可见文本和依赖标签实现基线训练/留出评价；从真实注意力提取相同前提分数；自述目标应为依赖集合。边界分类器需要正负 token 样本及可加载权重；如果决定删去某组件，应明确记录未实现并调整完成范围。

### CR-S10 — BLOCKER / P2：文本基线拟合二元标签后额外 sigmoid，阈值改变了问题

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/baselines.py:28-46`。

**Issue:** 拟合使用最小二乘直接回归 y∈{0,1}，预测却把回归值当 logit 再 sigmoid。完全拟合的负例回归值 0 会变成概率 0.5，正例 1 变成 0.731；按通常 >=0.5 阈值，正确拟合的负类也预测为正类。此外训练特征只用 prefix，推理特征加入 premise，未形成一致的前提—步骤对表示。

**Verified reproducer:** fit_text_predictor(['alpha','beta'], array([0.,1.])); 用 text_predictor(s,'',weights) 在原训练点预测得到 [0.5,0.7310585786300049]。这是无泛化难度的训练点失真。

**Fix:** 使用一致的 prefix/premise 特征和 logistic BCE 拟合 logits，或保持概率回归并去掉额外 sigmoid；用包含正负边的训练点及留出边检查识别指标。

### CR-S11 — BLOCKER / P2：文本特征用随机化 Python hash，保存权重跨进程即换坐标

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/baselines.py:16-20`、`34-41`。

**Issue:** 内置 hash(str) 默认随进程变化；返回的模型仅包含 weights，没有词表/哈希种子。训练与评价若分进程运行，同一 token 进入不同列，保存的权重不再对应特征。研究可重复性与有效评价均被破坏。

**Verified reproducer:** 两个 Python 子进程分别 PYTHONHASHSEED=0 和 1，运行 `_bow('premise').argmax()`，结果 11 和 25。相同文本、相同代码，特征坐标改变。

**Fix:** 采用固定算法/固定种子的稳定哈希（如 hashlib）或拟合并保存词表；添加跨进程 save/load 预测一致性测试。

### CR-S12 — BLOCKER / P2：几何附录含 ndarray，analyze 无法写出 JSON

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/analysis.py:283-288`；`transfer.py:84-86`；`cli.py:1138-1141,1168`。

**Issue:** procrustes 返回 numpy.ndarray 类型的 R；common_dim_then_procrustes 原样返回；analyze 把它放进 report 后交给严格 JSON writer。io.encode 不支持 ndarray，因此有效几何配对输入会让整次分析失败，而不是产生几何附录。

**Verified reproducer:** geom_a.jsonl=[{'rows':[[1,0],[0,1]]}]，geom_b.jsonl 同样内容；analyze --in-dir ... --out-dir ...。应输出单位旋转，实际完整 CLI 执行确认报错 TypeError: Not JSON serializable: ndarray。

**Fix:** 在产物边界将 R 转为 list 或保存为 npz 并在报告引用；增加真实 analyze JSON 输出的几何集成测试。

## Warnings

### WR-S01 — WARNING / P2：校准风险水平固定为 0.4，无法执行其他预注册 alpha

**File:** `C:/Users/22688/Desktop/diff/src/reasoning_diff/cli.py:819-822,1221`。

**Issue:** CLI 和配置没有 alpha 输入，实际阈值及报告固定用 0.4。原始方案公式保留 alpha 为实验参数，实验协议要求阈值预注册；0.4 本身不违反保形数学公式，协议也没有给出必须使用的默认数值，因此这里不认定“应为 0.05”之类未经授权的要求。但任何预注册的其他风险水平都无法通过当前 CLI 执行。

**Fix:** 将 alpha 从冻结的实验配置传入并写入 run_spec/resume 身份；保留明确默认值也可，但不能覆盖已注册配置。

## Verification and limits

- 已运行纯 NumPy/临时目录反例：校准 head/未知标签、指标行序、P2/P3 多行、P1 共组泄漏、迁移均值、平衡监督标签、文本输出、跨进程哈希。
- 7 个现有定向回归测试通过：保形公式、维度拒绝、P1 bootstrap、E 列序辅助函数、文本 fit 合约、监督标签存在性、边界 BCE。上述通过只覆盖浅层合约，未触达已复现的生产连接错误。
- 双线性 U/V 梯度链路确实存在；本次没有把“只是随机投影”作为问题。conformal_threshold 有限样本顺序统计公式本身也未发现上述反例中的数学错误，错误位于 CLI 真值和单位输入。
- 未下载模型、未运行大型推理、未把任何测试输出视为科学实验结论。未修改源代码或旧审查报告。
- broader CLI split/resume 缺陷由主审查线程覆盖，本文件不重复列出。
