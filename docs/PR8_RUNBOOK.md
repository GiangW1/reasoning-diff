# PR8：先验证测量链路，再跑正式数据

2026-10-06 的真实 smoke 因测量覆盖不足而停止，正式 32 题未启动。对 `241cd31` 的复核确认：373 项测试通过，但保存轨迹仍不满足测量检查，行首项目符号还会漏解析。本次修订修复这些代码问题；全量旧轨迹离线复测和缓存配对检查**仍失败，不建议重启正式实验**。没有重新运行真实 Qwen smoke 或正式实验，见 [本次离线复核](../artifacts/rd-pr8-sequence-audit-20261007-light/REPORT.zh-CN.md)。

后续补丁修复了 `So:` 换行后接项目符号的声明遗漏，避免同一操作数在 base/edit 中得到不同身份；并增加部分共同支持的描述统计。最新数值和具体修复路径见 [后续复核](../artifacts/rd-pr8-support-followup-20261007-light/REPORT.zh-CN.md)，主测量依然失败。

2026-10-07 增加独立的受控条件 `--trajectory-protocol quantity_steps`，可使用下方入口先验证。它让模型在预先登记的数量步骤内自由计算，每个数量明确提交一次结果，解决自由文本中重复确认和表达式变化导致的单位身份不确定。旧数据保持原自然条件；不能重新贴上新条件的标签，也不能把新条件的结果解释为原自然全步骤实验已成功。422 项 CPU 回归通过，见 [代码验证记录](../artifacts/rd-pr8-quantity-steps-codecheck-20261007-light/REPORT.zh-CN.md)。真实模型是否遵循格式、以及实际测量和 C2 能否通过，仍由服务器 pilot/smoke 判定。

## 服务器命令

使用 PR7 已有的 Python 环境、200 题输入和固定 revision 的 Qwen3-8B 权重。源码放 `/home/wja`，所有模型、输出、日志、检查点和缓存放 `/mnt/mydata/wja`。从此 PR 的源码 checkout 执行：

```bash
export PYTHONPATH="$PWD/src"
PY=/mnt/mydata/zm/projects/RPent/.venv/bin/python

# 新受控条件：先运行长度/格式、配对、特征和干预 smoke。
"$PY" scripts/run_pr8.py --mode smoke \
  --trajectory-protocol quantity_steps \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/pr8-quantity-steps-v1

# 正式运行：先自动执行/恢复同协议的 smoke，通过后才启动剩余题目。
"$PY" scripts/run_pr8.py --mode full \
  --trajectory-protocol quantity_steps \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/pr8-quantity-steps-v1
```

默认数据目录为 `/mnt/mydata/wja/reasoning-diff/runs/pr7-200-20261004/inputs/igsm-pilot200`，权重根目录为 `/mnt/mydata/wja/reasoning-diff/assets/models`，需包含 `Qwen3-8B/verified.json`。

预算默认 `--max-new 32768`；实际生成预算取该值与模型卡片剩余上下文的较小值，保存实际预算和长度。输入也占上下文，不强制关闭 thinking。可以指定 `--dataset`、`--model-root`、`--gpus`、`--batch-size`。输入、代码或协议改变后使用新输出目录，不能复用旧结果。DeepSeek 对照使用 `--model r1-distill-qwen-7b` 和自己的已验证权重/上下文预算。

不要使用 PR7 的 PID 接管脚本启动 PR8；两个实验使用独立目录和指纹。

启动器保留上一轮的并行优化：长度/配对 pilot 与 prepare 均按每卡 batch size 批量解码；四层特征收集分配到三张卡，收集完成即提交 CPU 拟合；同时最多运行两个 CPU 任务，每个任务使用 8 个 BLAS 线程。三个特征位置并行拟合后，`fit --position all --resume` 复用结果并汇总，拟合入口缓存只读 event rows，避免重复解析。层选择和标签规则保持不变，所选生成条件贯穿 pilot、prepare、解析与干预，测量质量检查提前并按题目/难度分层。`execution_progress.json` 记录每个阶段的状态，CPU 阶段不访问 GPU。上述环境只用于运行，不向 RPent 环境安装或修改包。

来源对干预也按 `--pair-shard INDEX COUNT` 分配到三卡；同一来源对的两种配置与全部对照保持在同一进程内，合并时保留原始 pair index。`--formal-limit 32` 可选取探索性小集：每个 op 有 4 道 probe_train、1 道 dev、1 道 calibration 和 2 道 test，仍使用既有 split hash，按与模型结果无关的 family hash 选题；8 道 smoke 题及其 family 保持独立。该子集不使用本轮暂缓的 direction_fit/transfer_pairs，不能代表完整论文检验。

12 小时配置示例：`--mode full --gpus 2 3 6 --batch-size 4 --max-new 12288 --formal-limit 32 --time-budget-hours 12`。token 上限控制长尾和 KV 显存，遇到截断仍如实记录；不能强制闭合 thinking 或绕过 smoke。`execution_budget.json` 保存首次启动的预算起点，恢复不延长预算；到期停止当前子进程并标记 `budget_exhausted`，保留检查点，不标记为实验完成。代码、生成预算与样本选择均不同，必须使用新的输出目录。

变量缩写只从生成文本中的声明解析：支持实体标题下的项目、`Let X be ENTITY`、`Let me denote ENTITY as X`、反向声明，以及明确实体主语后的 `So/Then/Therefore X = ...` 或跨行的 `Let me write that as:`。跨行主语与引入语必须在同一段落内，不继承另一赋值 RHS 中的实体。行首项目符号和配对粗体/代码标记按版式处理，原文跨度保持不变。不按数值或标准答案猜测实体，不使用后续声明标注较早步骤，冲突声明保持未解析。等式链只读取明确打印出的末端数值；不替模型计算尚未写出结果的表达式，不将 RHS 中的操作数误当新赋值。

## smoke 内容与停止条件

按固定 split hash，在 op5/10/15/21 各选一个 probe_train 和一个 dev 题，共 8 题；选题发生在生成前，不看准确率。这些题的整个 family 从正式 cohort 排除，正式运行剩余 192 题。

第一阶段只生成 24 条 base 轨迹，用正式预算检查长度和解析。每个 op 的自然完成率至少 50%，每条轨迹需要精确 token 边界和可解析的 thinking calculation/commit 事件。此外，每题跨 seed 的目标变量覆盖率和目标 DAG 中间变量覆盖率均至少 50%，避免“仅解析到一个事件”就通过。缺失变量逐条写入 `parser_coverage.json`。DAG 变量覆盖是工程诊断，不是经过全句人工标注的步骤召回率。

第二阶段复用 base pilot 检查点，每题只对预先选定的第一个相关数值事实和两个无关事实各编辑一次（seed 0），共新增 24 条轨迹；seed 1/2 的 base 作为匹配噪声参照。CPU 上检查事件匹配、共同噪声支持、rho 和解析变量覆盖，不采集隐状态、不拟合探针。`paired_pilot.json` 保存各卡检查结果，配对 pilot 的支持分母仅包含登记的三个事实，不把尚未扫描的事实算作缺失或已观测。失败就停止全前提扫描。

第三阶段对 smoke 的全部句子前提扫描，先在 CPU 上写 `measurement_report.json` 和轨迹表，测量检查通过后才采集四层特征并拟合。扫描 0/12/24/35 层，在 dev 上选 behavior AUC 最高的层（并列选低层）；最终 fit、calibrate、intervention 使用该层。检查：

- 全前提有扫描记录，截断 thinking 前缀没有误丢弃。
- train/dev 有两类有效 behavior 标签，至少两个 dev 层有可用 AUC。
- P1 每条 base 轨迹一行，没有三种位置重复或零长度哨兵。
- 已观察非任务格、带共同噪声支持的格、可用 rho 轨迹、目标 DAG 变量和目标变量的覆盖率均至少 50%，同时检查总体、每个 op 和每道题。单个有 rho 的 seed 不能掩盖其余缺失。
- 两类来源对各至少有一个可用 contrast，其 baseline、main、随机对照和 C-layer 对照全部自然结束且有有效答案；三种干预范数均有限且非零。每个条件恰好一行，按同一来源对核对，不能跨对拼接或重复计数。

smoke 失败保留诊断、不启动正式生成。正式 cohort 也执行上述检查；C2 不可用时先保存分析中的失败/缺失记录，再将 pipeline 标记失败。50% 是防止大面积截断/无法测量的工程检查，**不是论文验收阈值**；本修订没有降低阈值，但新增按题检查及共同噪声/rho/变量覆盖检查，已登记在 `protocol.json`。没有“必须准确”“AUC 必须高”“效应必须正”的门槛。48 条小 pilot 仍消耗算力，但能在全前提扫描之前暴露配对测量问题。

依次查看 `length_pilot.json`、`parser_coverage.json`、`paired_pilot.json`、`smoke/measurement_report.json`、`smoke/smoke_report.json`、`smoke/layer_selection.json`、`smoke/intervention_coverage.json` 和 `logs/`。相同源码和参数可以恢复；本次修订改变解析和匹配协议，旧运行目录不能直接 resume，必须使用新输出根目录。

## 数据与测量协议

`--trajectory-protocol natural` 是默认的旧自然条件。新条件必须显式指定 `quantity_steps`，同时使用 `--premise-protocol sentence_graph`；启动器已经传递这两个参数。`protocol.json`、任务/轨迹 metadata、prepare 配置、检查点指纹和测量报告分别记录条件、匹配规则与测量对象，混合条件不能共用测量表。

受控条件的格式为 `<step node="登记ID">自由推理 <commit>整数</commit></step>`。提示提供任务 DAG 中已有数量的 ID、名称和计算顺序，不提供节点数值、标准答案或依赖集合；顺序来自已知任务结构，属于显式控制，不是自然条件中模型自行发现的步骤。每个节点一次提交，块内可以推敲和修改。匹配对象是这次明确提交的数量结果，不包含每个算术微步骤、复述或反复确认。C1 需要和同样知道节点计划的文本/任务成员基线比较；本条件不能单独证明自由推理中的潜在依赖可解码。

匹配使用 `registered_quantity_steps_v1`，按登记节点、作用域和区域配对，不依赖结果值、标准答案、表达式形式或位置距离。重复提交保持歧义，缺失步骤保留在登记支持分母；不会因模型少输出步骤而提高覆盖率。格式检查从生成文本重算，排除提示中的示例标签；未登记 ID、重复、缺失、乱序、损坏标签或 answer 区域中的 step 都记录为失败。24 条 base 的格式检查在新增配对生成之前执行，写入 `registered_step_formats.json`；配对 pilot 和全扫描也检查编辑及噪声轨迹。原有覆盖和 C2 检查不降低。

受控条件的 `rho` 是“每个登记数量一次提交”的响应率超额，保留有符号噪声扣除、共同支持及缺失状态；不替换旧自然轨迹的 `rho`。`pre_step` 在整个 step 开始之前，`pre_value` 在提交整数之前；不把已经生成的算术推理误当成步骤之前的信息。C2 使用精确 token 前缀续写，解析时恢复完整已生成上下文并剥离提示，解决缩写声明和跨切点标签丢失；只把切点后新提交的节点用于 donor-follow 判定，完整上下文用于格式检查。解码答案虽存在但格式无效时仍标记 invalid。受控条件的非目标集合改为编辑脏锥之外的计算节点；`nontarget_observable_nodes` 记录切点后实际观察到的节点，没有观测时 `nontarget=null`，不能用提示前提或已经固定在前缀中的结果虚构保留率。

`--premise-protocol sentence_graph` 从官方模板 DAG 重建自然语言题：每个数值事实、每个运算关系各占一个句子，并加入两个不在目标 DAG 中的数值事实。隐含聚合关系显式化，真值从独立表达式重算，原题和模板保留在 metadata。

这是新的 **project_derived** 条件，不能冒充原始官方题或与 PR7 混池。它先检验明确事实/关系层面的归因测量。

每题每个前提扫描 3 次，使用不同合法数值；关系事实使用非零增量，同时修改自然语言和表达式。edit 与对应 base 共享 seed。扫描不是穷尽枚举，未对齐仍未知。`--noise-reference base_pairs` 用已有 base seeds 的有向比较，不额外生成 sham；共享轨迹的 pairs 不能当独立样本，推断按 problem 聚类。

解析区分 restatement/calculation/commit，科学主探针排除 restatement 和边界失败轨迹，原始轨迹全部保留。Unicode 跨 token 时按原始 bytes 对齐；重编码或 byte round trip 失败就保留失败，不能回退到虚构游标。

事件匹配使用 `region_structure_forced_sequence_v3`：thinking/answer 分开，兼容条件仍要求相同实体、作用域、事件类型、阶段和不含数值的表达式结构。先在各区域的完整事件序列上求最优单调匹配，只保留所有最优匹配共有的事件对。重复结构还需要另一个实体的共有对应作为上下文；孤立的重复确认、多个最优对应、阶段/结构不兼容继续保持未知。记录 `alignment_method` 和 `alignment_certificate`（事件身份、匹配序号、最优长度及上下文实体数量）；主比较、跨 seed 噪声和 C2 使用相同规则。

该规则**假设同一区域内步骤次序保持**。在此假设下对应唯一，不等于语义步骤身份已经经过人工验证；模型可以改变策略或重复确认的含义。开发回归验证了算法没有任选并列对应，没有估计真实步骤配对 precision/recall。主测量不切换到最后一次赋值，不按数值、标准答案、位置距离或删除表达式结构来补配。不能匹配的 reference 事件仍进入缺失分母，已知任务依赖标签保留，行为标签保持未知。

行为标签绑定 reference trace/seed，不把一个 seed 的变化传播到所有 seeds。只收集主 probe 和来源对 donor 特征，避免所有扫描变体形成无标签的大矩阵。文本基线、预测下一变量后映射 DAG 的基线、`restatement + R_task` 诊断基线均只用 probe_train 拟合，并在与 probe 相同的格子上报告 dev/test。

标签文件的密度摘要先逐轨迹计算，再取有观测轨迹的平均，保留 `per_trace` 和观测分母；跨 seed 的正例不取并集。噪声记录 ID 包含题目、两条轨迹及完整事件身份。`intervention_coverage.json` 记录每个来源对未通过的具体条件，预算耗尽的解码不算自然完成。

## P1 的解释范围与暂未执行的检验

`probe_predictions.jsonl` 保存事件 × 前提格的预测/依赖标签，只用于 C1。`p1_table.jsonl` 保存 base 轨迹的正确性和密度，三个特征位置不重复写入，位置间结果必须一致。P1 回归仅用 probe_train 和 test，按 problem 聚类；dev 用于选层。smoke 全部答对/全部答错时记录 `single_class` 和类别数量，只能检查测量链路，不能检验密度对正确率的预测；训练集单一类别也不输出有效回归结果。工程 smoke 不为制造正误两类而改 prompt 或采样结果。

密度协议是 `matched_cell_response_rate_excess_v1`：每个事件的已观察非任务前提格上，计算编辑引发值变化的比例，减去相同 reference/event 上 base seeds 的噪声比例，再对事件取平均。负 excess 保留，表中同时记录 raw 密度、支持格数和覆盖率。

这是有限扫描、共同支持集上的**描述性响应率 excess**，不证明整个前提全集上的因果虚假依赖。未观察格不当成 0；缺少匹配噪声时 rho=null。失败/截断在 ITT 正确率计为 0，但缺失 rho 无法进入归因回归，报告缺失分母；不能将该回归称作完整 ITT 因果效应。

原有 `rho` 在任一已观测事件缺噪声时将整条轨迹置空。`common_support_diagnostic` 另报 edit/noise 同时支持的子集：raw、noise、signed excess 使用完全相同的事件和权重，保留事件/格数及覆盖率。其状态为 `descriptive_only` 或 `no_common_support`，不替换 P1 的 rho，也不改变运行检查；非空诊断不能视为整条轨迹满足分析条件。

C2 遍历所选 split 的所有来源对，分别执行同值换来源/同来源换值，使用各自前缀。donor 先在完整原始事件上使用与主测量相同的区域、阶段、表达式结构和序列匹配，再筛选 thinking 计算/提交事件并定位特征行；特征过滤后看似唯一的重复步骤不算可用。同值换来源时，只将已登记的来源替换映射用于对应计算阶段的结构比较，不改写输出、不按结果寻找 donor、不任意替换其他操作数。数值来源可经多层 DAG 到达目标，下游自然语言和 DAG 同步换来源。同值条件的数值 target-follow 无法区分来源，保留 null，不能据此声称模型遵循了 donor 来源。最终分析输入包含干预记录与测量质量报告，分别报告两类来源对的可用/失败数量及同对的描述性对照差值；不把 C2 记录计入 P3。

本入口暂不执行旧 P3/INLP 与 C4 repair：前者需要 S 专属、仅在 direction_fit 拟合的消融方向，后者需要真正的旧轨迹增量修复和连续编辑。输出标为未评估，不把 main swap 当 P3 或同槽位 repair 当成功。没有引入 vLLM；继续使用已有 HF 独立 RNG/batched decoder，避免迁移后混用采样语义。

## 保存轨迹的离线重测

`scripts/reparse_pr8.py --in-dir OLD_PREPARE --out-dir NEW_PREPARE` 校验原始 manifest，从保存的精确 prompt 边界之后解析文本，复用原 token IDs、offsets、答案评分和生成状态，重建编辑比较以及所有注册的有向 base-seed 噪声对。不加载模型或生成新 token，要求使用新的输出目录。

先复核服务器上原始保存数据，可只导出报告，避免复制大体积轨迹和标签：

```bash
"$PY" scripts/reparse_pr8.py \
  --in-dir /mnt/mydata/wja/reasoning-diff/runs/pr8-12h-20261006-r2/smoke/prepare \
  --out-dir /mnt/mydata/wja/reasoning-diff/runs/pr8-sequence-audit/prepare \
  --report-only
```

`measurement_report.json` 对照原始测量与当前测量的事件数、支持格及可用 rho，并保存按题/难度的检查。`cached_paired_screen` 从旧比较中精确选取每题 seed 0 的登记相关事实及两个无关事实，使用 seed 1/2 噪声；缺少或重复的编辑比较也记为失败，不重新生成。报告模式只输出测量报告、来源 spec 和 manifest，不能用作 collect 的 prepare 输入。命令成功只代表重测成功，是否满足测量门槛看报告中的 `passed`，`formal_launch_ready` 仍为 false。

当前全量复核：335 条保存轨迹、24 条 base，匹配 1955/5965（32.77%），共同噪声支持 1458/5965（24.44%），原有 rho 1/24。缓存配对检查：8 条 base、24 个编辑均存在，匹配 193/567（34.04%），共同噪声支持 147/567（25.93%），原有 rho 0/8，另有一题变量覆盖不足。共同支持描述统计分别在 23/24、7/8 条上非空；这不改变两项主测量仍未通过 50% 检查的结果，不能启动全扫描。更早版本的分母不同，不能把新旧百分比直接解释成同口径性能提升。

主测量保留 50% 阈值；重解析成功不等于正式运行就绪。必须先解决步骤对应的可识别性并人工审查配对，再验证登记的小检查；通过后才能重新验证特征采集、拟合和因果 smoke。这是新的测量版本，旧结果保留在故障报告中，不能静默覆盖或混池。

附加的 `final_commitment_p1_table.jsonl` 仅用于诊断：按文本位置选每个实体/作用域在 thinking 区域最后一次明确赋值，再重建比较。选择不使用赋值数值或标准答案，但该口径测量实体最终结果，不能替代所有推理步骤的依赖测量，不得用于绕过原 smoke 检查。解析修复支持内联的 `实体名 (变量) = ...` 和带明确数值结果的符号等式链，歧义声明及未给出明确结果的表达式仍不推断。

2026-10-06 真实运行在覆盖率检查失败后停止，正式 32 题未启动。完整故障说明与轻量证据见 [PR8 实验故障报告](../artifacts/rd-pr8-smoke-20261006-light/REPORT.zh-CN.md)。

## 代码验证

```bash
"$PY" -m pytest -q --tb=line
"$PY" -m compileall -q src scripts tests
git diff --check
```

回归覆盖截断区域、操作数误解析、最后层误选、P1 哨兵混入，以及逐 seed 标签、全题扫描/批量计划、Unicode 边界、校准位置、来源对遍历、四个 op 层的事实转换与 pilot 失败时不启动正式生成。

本次新增的 `tests/fixtures/pr8_saved_excerpt_audit.json` 包含 8 道真实 smoke 题的 9 个原文片段（四个 op），保存原有声明上下文、来源轨迹 ID、文本哈希和逐条检查的 13 个明确赋值跨度，以及一个操作数负例。测试核对实体、值、阶段和 offsets，并验证修改标准答案不会改变提取或匹配。它们是发现故障后选取的开发回归，**不是独立标注的整批解析 precision/recall 估计**；报告将未经人工全句标注的步骤召回率保留为未评估。模型自然重述和策略变化可能仍然造成不可识别的步骤对，新的配对 pilot 应如实停止，不能通过最后赋值口径或将未知置零绕过。
