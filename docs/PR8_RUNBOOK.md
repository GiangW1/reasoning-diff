# PR8：先验证测量链路，再跑正式数据

此 PR 提供代码和服务器入口，没有运行真实 Qwen smoke 或正式实验。单元/回归测试不构成实验结果。

## 服务器命令

使用 PR7 已有的 Python 环境、200 题输入和固定 revision 的 Qwen3-8B 权重。源码放 `/home/wja`，所有模型、输出、日志、检查点和缓存放 `/mnt/mydata/wja`。从此 PR 的源码 checkout 执行：

```bash
export PYTHONPATH="$PWD/src"
PY=/mnt/mydata/zm/projects/RPent/.venv/bin/python

# 只运行 smoke；默认 GPU 2/3/6，batch size 2。
"$PY" scripts/run_pr8.py --mode smoke \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/pr8-sentence-facts

# 正式运行：先自动执行/恢复同协议的 smoke，通过后才启动剩余题目。
"$PY" scripts/run_pr8.py --mode full \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/pr8-sentence-facts
```

默认数据目录为 `/mnt/mydata/wja/reasoning-diff/runs/pr7-200-20261004/inputs/igsm-pilot200`，权重根目录为 `/mnt/mydata/wja/reasoning-diff/assets/models`，需包含 `Qwen3-8B/verified.json`。

预算默认 `--max-new 32768`；实际生成预算取该值与模型卡片剩余上下文的较小值，保存实际预算和长度。输入也占上下文，不强制关闭 thinking。可以指定 `--dataset`、`--model-root`、`--gpus`、`--batch-size`。输入、代码或协议改变后使用新输出目录，不能复用旧结果。DeepSeek 对照使用 `--model r1-distill-qwen-7b` 和自己的已验证权重/上下文预算。

不要使用 PR7 的 PID 接管脚本启动 PR8；两个实验使用独立目录和指纹。

启动器已接入上一轮的并行优化：长度 pilot 与 prepare 均按每卡 batch size 批量解码；四层特征收集分配到三张卡，收集完成即提交 CPU 拟合；同时最多运行两个 CPU 任务，每个任务使用 8 个 BLAS 线程。三个特征位置并行拟合后，`fit --position all --resume` 复用结果并汇总，拟合入口缓存只读 event rows，避免重复解析。层选择、标签、生成预算和 smoke 检查保持原协议。`execution_progress.json` 记录每个阶段的状态，CPU 阶段不访问 GPU。上述环境只用于运行，不向 RPent 环境安装或修改包。

来源对干预也按 `--pair-shard INDEX COUNT` 分配到三卡；同一来源对的两种配置与全部对照保持在同一进程内，合并时保留原始 pair index。`--formal-limit 32` 可选取探索性小集：每个 op 有 4 道 probe_train、1 道 dev、1 道 calibration 和 2 道 test，仍使用既有 split hash，按与模型结果无关的 family hash 选题；8 道 smoke 题及其 family 保持独立。该子集不使用本轮暂缓的 direction_fit/transfer_pairs，不能代表完整论文检验。

12 小时配置示例：`--mode full --gpus 2 3 6 --batch-size 4 --max-new 12288 --formal-limit 32 --time-budget-hours 12`。token 上限控制长尾和 KV 显存，遇到截断仍如实记录；不能强制闭合 thinking 或绕过 smoke。`execution_budget.json` 保存首次启动的预算起点，恢复不延长预算；到期停止当前子进程并标记 `budget_exhausted`，保留检查点，不标记为实验完成。代码、生成预算与样本选择均不同，必须使用新的输出目录。

变量缩写只从生成文本中明确的声明解析，允许已识别实体标题下的项目名与符号对应；不按数值或标准答案猜测实体，不使用后续声明标注较早步骤，冲突声明保持未解析。

## smoke 内容与停止条件

按固定 split hash，在 op5/10/15/21 各选一个 probe_train 和一个 dev 题，共 8 题；选题发生在生成前，不看准确率。这些题的整个 family 从正式 cohort 排除，正式运行剩余 192 题。

第一阶段只生成 24 条 base 轨迹，用正式预算检查长度和解析，避免先花费扫描算力。每个 op 的自然完成率至少 50%，每条轨迹需要精确 token 边界和可解析的 thinking calculation/commit 事件。失败写入 `length_pilot.json`，不启动扫描。

第二阶段对 smoke 的全部句子前提扫描，训练 probe，扫描 0/12/24/35 层，再在 dev 上选 behavior AUC 最高的层（并列选低层）。最终 fit、calibrate、intervention 使用该层。检查：

- 全前提有扫描记录，截断 thinking 前缀没有误丢弃。
- train/dev 有两类有效 behavior 标签，至少两个 dev 层有可用 AUC。
- P1 每条 base 轨迹一行，没有三种位置重复或零长度哨兵。
- 已观察非任务依赖格覆盖率至少 50%，至少一条轨迹有匹配噪声后的密度。
- 至少一个来源对的 baseline、main、随机对照和 C-layer 对照全部自然结束且有有效答案；三种干预范数均有限且非零。按同一来源对核对，不能将不同来源对的条件拼成一次成功。

失败保留诊断、不启动正式生成。50% 是防止大面积截断/无法测量的工程检查，**不是论文验收阈值**。没有“必须准确”“AUC 必须高”“效应必须正”的门槛。真实 smoke 也消耗算力，分两阶段让预算/解析问题尽早暴露。

查看 `length_pilot.json`、`smoke/smoke_report.json`、`smoke/layer_selection.json`、`smoke/intervention_coverage.json` 和 `logs/`。失败后可用相同源码和参数重启，prepare 使用 PR7 的逐轨迹检查点。

## 数据与测量协议

`--premise-protocol sentence_graph` 从官方模板 DAG 重建自然语言题：每个数值事实、每个运算关系各占一个句子，并加入两个不在目标 DAG 中的数值事实。隐含聚合关系显式化，真值从独立表达式重算，原题和模板保留在 metadata。

这是新的 **project_derived** 条件，不能冒充原始官方题或与 PR7 混池。它先检验明确事实/关系层面的归因测量。

每题每个前提扫描 3 次，使用不同合法数值；关系事实使用非零增量，同时修改自然语言和表达式。edit 与对应 base 共享 seed。扫描不是穷尽枚举，未对齐仍未知。`--noise-reference base_pairs` 用已有 base seeds 的有向比较，不额外生成 sham；共享轨迹的 pairs 不能当独立样本，推断按 problem 聚类。

解析区分 restatement/calculation/commit，科学主探针排除 restatement 和边界失败轨迹，原始轨迹全部保留。Unicode 跨 token 时按原始 bytes 对齐；重编码或 byte round trip 失败就保留失败，不能回退到虚构游标。

行为标签绑定 reference trace/seed，不把一个 seed 的变化传播到所有 seeds。只收集主 probe 和来源对 donor 特征，避免所有扫描变体形成无标签的大矩阵。文本基线、预测下一变量后映射 DAG 的基线、`restatement + R_task` 诊断基线均只用 probe_train 拟合，并在与 probe 相同的格子上报告 dev/test。

标签文件的密度摘要先逐轨迹计算，再取有观测轨迹的平均，保留 `per_trace` 和观测分母；跨 seed 的正例不取并集。噪声记录 ID 包含题目、两条轨迹及完整事件身份。`intervention_coverage.json` 记录每个来源对未通过的具体条件，预算耗尽的解码不算自然完成。

## P1 的解释范围与暂未执行的检验

`probe_predictions.jsonl` 保存事件 × 前提格的预测/依赖标签，只用于 C1。`p1_table.jsonl` 保存 base 轨迹的正确性和密度，三个特征位置不重复写入。P1 回归仅用 probe_train 和 test，按 problem 聚类；dev 用于选层。

密度协议是 `matched_cell_response_rate_excess_v1`：每个事件的已观察非任务前提格上，计算编辑引发值变化的比例，减去相同 reference/event 上 base seeds 的噪声比例，再对事件取平均。负 excess 保留，表中同时记录 raw 密度、支持格数和覆盖率。

这是有限扫描、共同支持集上的**描述性响应率 excess**，不证明整个前提全集上的因果虚假依赖。未观察格不当成 0；缺少匹配噪声时 rho=null。失败/截断在 ITT 正确率计为 0，但缺失 rho 无法进入归因回归，报告缺失分母；不能将该回归称作完整 ITT 因果效应。

C2 遍历所选 split 的所有来源对，分别执行同值换来源/同来源换值，使用完整 occurrence identity 和各自前缀。数值来源可经多层 DAG 到达目标，下游自然语言和 DAG 同步换来源。同值条件的数值 target-follow 无法区分来源，保留 null，不能据此声称模型遵循了 donor 来源。

本入口暂不执行旧 P3/INLP 与 C4 repair：前者需要 S 专属、仅在 direction_fit 拟合的消融方向，后者需要真正的旧轨迹增量修复和连续编辑。输出标为未评估，不把 main swap 当 P3 或同槽位 repair 当成功。没有引入 vLLM；继续使用已有 HF 独立 RNG/batched decoder，避免迁移后混用采样语义。

## 保存轨迹的离线重测

`scripts/reparse_pr8.py --in-dir OLD_PREPARE --out-dir NEW_PREPARE` 校验原始 manifest，从保存的精确 prompt 边界之后解析文本，复用原 token IDs、offsets、答案评分和生成状态，重建编辑比较以及所有注册的有向 base-seed 噪声对。不加载模型或生成新 token，要求使用新的输出目录。

`measurement_report.json` 对照修复前后的事件数、匹配格覆盖率和可用 rho 数量。主测量仍使用严格 occurrence-count 对齐，保留原 50% 覆盖率检查，重解析成功不等于正式运行就绪；特征采集、拟合和因果 smoke 仍需重新验证。

附加的 `final_commitment_p1_table.jsonl` 仅用于诊断：按文本位置选每个实体/作用域在 thinking 区域最后一次明确赋值，再重建比较。选择不使用赋值数值或标准答案，但该口径测量实体最终结果，不能替代所有推理步骤的依赖测量，不得用于绕过原 smoke 检查。解析修复支持内联的 `实体名 (变量) = ...` 和带明确数值结果的符号等式链，歧义声明及未给出明确结果的表达式仍不推断。

2026-10-06 真实运行在覆盖率检查失败后停止，正式 32 题未启动。完整故障说明与轻量证据见 [PR8 实验故障报告](../artifacts/rd-pr8-smoke-20261006-light/REPORT.zh-CN.md)。

## 代码验证

```bash
"$PY" -m pytest -q --tb=line
"$PY" -m compileall -q src scripts tests
git diff --check
```

回归覆盖截断区域、操作数误解析、最后层误选、P1 哨兵混入，以及逐 seed 标签、全题扫描/批量计划、Unicode 边界、校准位置、来源对遍历、四个 op 层的事实转换与 pilot 失败时不启动正式生成。
