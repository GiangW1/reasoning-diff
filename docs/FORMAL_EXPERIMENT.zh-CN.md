# 正式 C3 实验入口

`scripts/run_formal.py` 从已合并 PR8 的自然生成后端继续，覆盖 T1 的完整前提扫描、C1 三时机探针、C2 来源/数值对照，以及轨迹级 P1、配对 P2、独立方向拟合的 P3。C4 保留既有附录入口。当前代码没有真实模型正结果；本地 fixture 和随机微型模型只验证实现。

## 服务器运行

沿用 `/mnt/mydata/wja/reasoning-diff` 的数据/模型存储和 GPU 2、3、6。使用项目虚拟环境与已验证的模型快照；不修改其他项目环境。配置模板为 `experiments/formal_c3.json`。

模板指向已有 PR7 数据池以便直接使用，但明确标为开发数据。发表确认性结论前，将 `dataset` 改为新导出的独立 iGSM 快照，将 `dataset_exposure` 写成真实来源；过去观察过的全部题目族放入 `exclude_groups`。模板已经排除本次反复调试的 8 道题，不能把这解释为其余旧数据从未接触过。

```bash
python scripts/run_formal.py --mode plan \
  --config experiments/formal_c3.json \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/formal-c3-qwen

python scripts/run_formal.py --mode answers \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/formal-c3-qwen

python scripts/run_formal.py --mode all \
  --config experiments/formal_c3.json \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/formal-c3-qwen
```

`plan` 不加载权重，不生成轨迹，输出完整请求数和 decode token 上限。默认 64 道独立题、3 个参考 seed、每前提 2 个合法编辑值 × 3 个配对 seed，以及每参考轨迹 3 个独立 base 噪声 donor。三种条件都扫描全部前提，规模远大于此前仅 3 个前提的 pilot；请先根据 `plan_summary.json` 确定算力预算。配置可在首次 plan 前设 `time_budget_hours`；计时从第一次子进程运行开始，恢复不会重置预算。

`answers` 只生成三种条件的参考答案，保留所有失败，并分别输出按条件和划分统计的 ITT 正误、完整答案正误及失败类型。`all` 自动先复用/完成这个阶段；如果完整且可解析的答案全体仍只有一种正误类别，写 `stopped_unestimable` 并停止扫描。解析失败或截断不能单独制造“模型答错”样本；不自动换题、降预算制造错误或补种子追求正结果。研究者可用显式 `generate` 继续固定样本的测量性研究，但其统计限制仍保留。

每条生成即时保存。相同命令恢复会验证协议、源码、输入数据、请求身份和轨迹校验和；协议改变须使用新输出目录。各阶段也可单独运行：`generate`、`measure`、`fit`、`intervene`、`report`。日志在输出目录 `logs/`。`pipeline.json` 的 complete 只表示请求阶段完成，不表示科学假说成立。

第二模型独立运行：

```bash
python scripts/run_formal.py --mode all \
  --config experiments/formal_c3.json --model r1-distill-qwen-7b \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/formal-c3-r1
```

两模型使用同一题目族与划分；覆盖层自动改成 0/9/18/27。两个模型不要同时抢占同一组 GPU。每个模型独立训练属于模型内复现，不能写成探针零样本迁移；迁移仍使用项目独立 transfer 入口与专用 transfer_pairs 划分。

## 测量与实验定义

- 原题为显式句子前提的项目派生 iGSM 条件。相关 no-op 是关于目标主题的独立纪念标签数量，中性 no-op 使用相同句式与单词数。图和答案不变由独立重算检查；自然语言无关性仍须人工审计。控制仅匹配新增单词数，不能声称 tokenizer 长度精确相同。
- 每个前提的编辑值与随机种子分别变化。没有单独的大批 sham 生成；噪声是同题未编辑的预定独立 seed。固定采样参数、thinking、无 finalizer、无答案提示。所有失败与截断保留，不能算作测量负标签。
- `rho` 定义为可匹配非任务依赖格子的响应率超额，扣除相应事件的采样变化率。P1 先在每个事件的已支持前提格子上平均，再对事件等权平均；P2 在跨条件共同支持的格子上比较并平均。有限扫描不证明完整 read set，也不证明未响应的前提永远不会被读取。输出原始量、signed excess、缺失与覆盖率。
- P1 主检验使用 base 轨迹，失败按 ITT 计为答错；全条件检验控制条件，另报仅完整可解析答案的稳健性分析。预测目标为最终错误。仅 probe_train 拟合，最终 test 评估；开发/方向拟合/校准题不会进入预测器拟合。比较 length+op、加入复述/计算比例与测量覆盖率的更强基线，以及增加 rho 的模型。输出 AUC、PR-AUC、Brier 和按题目聚类的增量 AUC 区间。这个 rho 使用完整轨迹，是事后诊断；不是在线提前预警指标。缺失 rho 不填 0，不进入归因回归，但按结果/划分留在 ITT 统计。
- P2 的准确率使用所有预定配对；rho 只比较相同的已对齐事件 × 原始前提格子。相关/中性条件直接比较使用三臂共同支持集合；新增 no-op 的响应另报。缺失与结构变化单列，不写作零效应。效应先在同一道题内平均，再按题目等权聚类 bootstrap。
- C1 复用既有 task/behavior 双头和公平基线，记录 pre_step/pre_value/post_step。只用 dev 行为 AUC 选主层与不同的弱信息层；少于两个层有可估计的 dev AUC 时，保存 `insufficient_dev_layers`，停止无法构造完整对照的干预，保留此前测量结果。完整轨迹校准使用独立 calibration 题目；小样本的无穷阈值保留，不伪称有效保证。
- C2 的两来源事实同时出现在两个路由条件中，物理顺序按题目族固定反平衡；只改变下游文本和图的来源。两种数值层都保持两可选事实等值；数值条件同时更新两事实，属于明确的联合数值控制。比较同值异来源、同来源异值并保存等值条件无法用数值输出识别来源的限制。主 swap 和 C-rand/C-layer 同 cohort，报告目标、非目标、准确率、无效输出与真实范数。主统计保留已执行四个条件中的截断或无效答案，按答错计入配对 ITT；缺 donor、边界或合格对照的来源对保持不可估计。仅四条件答案全部完整的统计另列为次要诊断。
- P3 单独用 direction_fit 题目拟合“观察到额外依赖”的线性方向。正标签是存在已观察非祖先响应；负标签要求该事件全部非祖先均已扫描且未响应；未知保持未知。普通行为探针方向不会被冒充 S 专用方向。单类方向拟合输出不可估计，不以随机方向替代。
- P3 对所有预定 test 参考轨迹执行同一选择策略：在离线标注的边界中，选择第一个仅凭步前特征超过固定 0.5 分数阈值的事件；不按最终对错或 test 行为标签选事件。边界来自离线解析，所以不能声称在线边界检测。没有选中边界就保持原输出；方向不可用另报缺失。
- P3 在同一保存前缀、同一采样 seed 上比较 baseline、定向消融、同秩同范数随机消融、开发集弱层消融、相反方向，以及匹配/随机救援。这里的 `wrong_direction` 是相反方向对照，不冒称错误来源 donor。保存 hook 位置、实际范数、生成 IDs、无效输出和非目标变化。基线重新采样继续前缀，估计的是配对条件续写效应；原始正确率也保留。加回原成分的匹配救援是恒等重建，仅为诊断，不独自支撑强因果结论。

## 输出与人工审计

`measurement.json`、`p1_table.jsonl`、`p1.json`、`p2.json`、`s_direction-layer*.json`、`p3-gpu*.jsonl`、`p3.json`、`c2.json` 和最终 `experiment_report.json` 保留估计、不可估计原因及覆盖。P3 每条参考轨迹完成后落盘，并验证输入和拟合方向指纹，避免混用版本。

`audit_sample.jsonl` 按条件/响应/噪声分层抽取事件与对齐案例；`parser_recall_audit.jsonl` 保存完整轨迹供独立查漏；`semantic_audit.jsonl` 保存未编辑 no-op 条件供语言语义复核。人工字段初始均为 null，不让模型或待验证解析器给自己打“正确”标签。人工标注完成后保存为独立文件，并与实验报告一起发布。

工程覆盖阈值与 Gate 0–2 的科学决策标准分别记录。当前没有自动的“可以投稿/假说成立”判定。正式测试前还须冻结最小有意义效应、样本量/功效、多重比较和缺失敏感性分析；当前 bootstrap 区间是描述性估计。最终结论须检查人工审计与选择偏差，不可仅看一个区间是否跨零。

自然语言数学、问答、代码的独立 DAG/合法编辑资产需要各域单独提供；当前入口不把未知图的数据自动伪装成完整 T1 真值。

## 本次代码验证

2026-10-08：服务器隔离临时目录、`CUDA_VISIBLE_DEVICES=` 下全仓库 CPU 回归为 **653 passed**，其中新增 26 项正式入口测试包含随机微型 Qwen 的真实 hook/对照解码。Windows 新增测试为 26 passed；原仓库另有 12 项 Linux `fcntl` 依赖测试无法在 Windows 导入。未运行真实权重 smoke 或 GPU 实验。

使用已有 200 题快照仅验证 `plan`：默认 64 题设计共 15,276 个请求，其中参考 576、噪声 576、编辑 14,052、来源 72；32k 上限为 500,563,968 decode tokens。划分为 probe_train 21、dev 10、calibration 7、direction_fit 6、transfer_pairs 9、test 11 道独立题。64 是可修改的配置模板，不是经功效分析确认足够的正式样本量。
