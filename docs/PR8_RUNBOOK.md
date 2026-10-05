# PR8：先验证测量链路，再跑正式数据

此 PR 提供代码和服务器入口，没有运行真实 Qwen smoke 或正式实验。单元/回归测试不构成实验结果。

## 服务器命令

使用 PR7 已有的 Python 环境、200 题输入和固定 revision 的 Qwen3-8B 权重。源码放 `/home/wja`，所有模型、输出、日志、检查点和缓存放 `/mnt/mydata/wja`。从此 PR 的源码 checkout 执行：

```bash
export PYTHONPATH="$PWD/src"
PY=/home/wja/reasoning-diff/.venv/bin/python

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

## smoke 内容与停止条件

按固定 split hash，在 op5/10/15/21 各选一个 probe_train 和一个 dev 题，共 8 题；选题发生在生成前，不看准确率。这些题的整个 family 从正式 cohort 排除，正式运行剩余 192 题。

第一阶段只生成 24 条 base 轨迹，用正式预算检查长度和解析，避免先花费扫描算力。每个 op 的自然完成率至少 50%，每条轨迹需要精确 token 边界和可解析的 thinking calculation/commit 事件。失败写入 `length_pilot.json`，不启动扫描。

第二阶段对 smoke 的全部句子前提扫描，训练 probe，扫描 0/12/24/35 层，再在 dev 上选 behavior AUC 最高的层（并列选低层）。最终 fit、calibrate、intervention 使用该层。检查：

- 全前提有扫描记录，截断 thinking 前缀没有误丢弃。
- train/dev 有两类有效 behavior 标签，至少两个 dev 层有可用 AUC。
- P1 每条 base 轨迹一行，没有三种位置重复或零长度哨兵。
- 已观察非任务依赖格覆盖率至少 50%，至少一条轨迹有匹配噪声后的密度。
- 至少一个来源对完成非零干预、有效答案解码及 C-layer 对照。

失败保留诊断、不启动正式生成。50% 是防止大面积截断/无法测量的工程检查，**不是论文验收阈值**。没有“必须准确”“AUC 必须高”“效应必须正”的门槛。真实 smoke 也消耗算力，分两阶段让预算/解析问题尽早暴露。

查看 `length_pilot.json`、`smoke/smoke_report.json`、`smoke/layer_selection.json`、`smoke/intervention_coverage.json` 和 `logs/`。失败后可用相同源码和参数重启，prepare 使用 PR7 的逐轨迹检查点。

## 数据与测量协议

`--premise-protocol sentence_graph` 从官方模板 DAG 重建自然语言题：每个数值事实、每个运算关系各占一个句子，并加入两个不在目标 DAG 中的数值事实。隐含聚合关系显式化，真值从独立表达式重算，原题和模板保留在 metadata。

这是新的 **project_derived** 条件，不能冒充原始官方题或与 PR7 混池。它先检验明确事实/关系层面的归因测量。

每题每个前提扫描 3 次，使用不同合法数值；关系事实使用非零增量，同时修改自然语言和表达式。edit 与对应 base 共享 seed。扫描不是穷尽枚举，未对齐仍未知。`--noise-reference base_pairs` 用已有 base seeds 的有向比较，不额外生成 sham；共享轨迹的 pairs 不能当独立样本，推断按 problem 聚类。

解析区分 restatement/calculation/commit，科学主探针排除 restatement 和边界失败轨迹，原始轨迹全部保留。Unicode 跨 token 时按原始 bytes 对齐；重编码或 byte round trip 失败就保留失败，不能回退到虚构游标。

行为标签绑定 reference trace/seed，不把一个 seed 的变化传播到所有 seeds。只收集主 probe 和来源对 donor 特征，避免所有扫描变体形成无标签的大矩阵。文本基线、预测下一变量后映射 DAG 的基线、`restatement + R_task` 诊断基线均只用 probe_train 拟合，并在与 probe 相同的格子上报告 dev/test。

## P1 的解释范围与暂未执行的检验

`probe_predictions.jsonl` 保存事件 × 前提格的预测/依赖标签，只用于 C1。`p1_table.jsonl` 保存 base 轨迹的正确性和密度，三个特征位置不重复写入。P1 回归仅用 probe_train 和 test，按 problem 聚类；dev 用于选层。

密度协议是 `matched_cell_response_rate_excess_v1`：每个事件的已观察非任务前提格上，计算编辑引发值变化的比例，减去相同 reference/event 上 base seeds 的噪声比例，再对事件取平均。负 excess 保留，表中同时记录 raw 密度、支持格数和覆盖率。

这是有限扫描、共同支持集上的**描述性响应率 excess**，不证明整个前提全集上的因果虚假依赖。未观察格不当成 0；缺少匹配噪声时 rho=null。失败/截断在 ITT 正确率计为 0，但缺失 rho 无法进入归因回归，报告缺失分母；不能将该回归称作完整 ITT 因果效应。

C2 遍历所选 split 的所有来源对，分别执行同值换来源/同来源换值，使用完整 occurrence identity 和各自前缀。数值来源可经多层 DAG 到达目标，下游自然语言和 DAG 同步换来源。同值条件的数值 target-follow 无法区分来源，保留 null，不能据此声称模型遵循了 donor 来源。

本入口暂不执行旧 P3/INLP 与 C4 repair：前者需要 S 专属、仅在 direction_fit 拟合的消融方向，后者需要真正的旧轨迹增量修复和连续编辑。输出标为未评估，不把 main swap 当 P3 或同槽位 repair 当成功。没有引入 vLLM；继续使用已有 HF 独立 RNG/batched decoder，避免迁移后混用采样语义。

## 代码验证

```bash
"$PY" -m pytest -q --tb=line
"$PY" -m compileall -q src scripts tests
git diff --check
```

回归覆盖截断区域、操作数误解析、最后层误选、P1 哨兵混入，以及逐 seed 标签、全题扫描/批量计划、Unicode 边界、校准位置、来源对遍历、四个 op 层的事实转换与 pilot 失败时不启动正式生成。
