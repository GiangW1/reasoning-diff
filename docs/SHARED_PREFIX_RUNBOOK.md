# 共享前缀配对续写：独立条件 v1

`scripts/run_shared_prefix.py` 登记 `shared_prefix_assignment_v1`，测量**给定原始 pre-value 历史后，修改题目中的一个前提是否改变当前赋值的数值响应**。它为每次比较固定同一个赋值起点，避免自由生成两条完整轨迹后再猜测步骤对应。原有 `natural` 和 `quantity_steps_v1` 入口、结果及覆盖门槛保持独立。

这不是原自然轨迹匹配问题已经解决的证据。旧数据的自然匹配覆盖率仍为 2169/6822（31.79%），共同噪声支持仍为 1652/6822（24.22%）。新条件改变了测量对象，实际续写是否可解析必须由服务器 pilot 检验，不能用代码测试宣称覆盖率达标。

## 切点、对照与缺失

1. 校验旧 prepare 的 tasks/traces 文件哈希，从精确保存的 rendered prompt 之后重新解析所有 base thinking calculation/commit。每个已解析事件都登记切点，不按原值、答案正确性或后续续写筛选；没有事件的来源轨迹也保留并使检查失败。解析器仍可能漏掉未识别的自然步骤，因此本条件不估计全部自然步骤的召回率。
2. 在原始赋值结果数值的第一个字符之前截断。按原模板替换题目中的一个句子前提，随后附上完全相同的生成历史，再重新分词。跨越数值起点的原 token 不会被带入；tokenizer 的文本 round trip 必须精确。原模型和 revision 必须一致。不添加答案提示、格式示例、强制闭合或 finalizer。
3. 每个切点重新生成三个无编辑 baseline（seed 0/1/2）；每个前提有三个登记编辑，分别使用 seed 0/1/2。edit 和 baseline 使用对应 seed、独立 RNG，以及 T=0.6 / top_k=20 / top_p=0.95。原轨迹的旧数值不充当 baseline，也不混入噪声估计。
4. 续写到第一个换行、`</think>` 或自然 EOS；默认最多 256 新 token，并受剩余上下文限制。只读取固定赋值头上新产生的明确数值，不从后续另一条赋值补救。未完成数字、无法解析、前缀 round trip 失败、源边界失败、上下文耗尽以及缺失请求均保持失败/未知。
5. 主响应比较该 edit 与同 seed baseline；噪声比较相同历史下该 baseline 与另外两个 baseline。只有三个 baseline 和 edit 都可观测时才计算 `excess = response - noise`，保留负值。失败记录不缩小登记分母，未知不当作“不变”。

固定历史包含此前的结果、可能已经展开的操作数和当前等式左半部分，甚至可能与修改后的题目矛盾。因此，响应不变不能推出该前提在完整推理中未被使用；该条件只测量固定历史后的局部敏感性。不同切点、编辑及 seed 共享历史和 baseline，不能视为独立样本。报告的均值在共同支持集上按登记编辑机会等权，仅作描述；后续推断应以来源 problem 聚类。

## 服务器入口

在 PR8 分支最新代码上运行，使用已有 RPent Python；不向该环境安装包。每个参数在 plan、pilot、scan 中保持一致，输出必须与输入分开。所有新缓存、日志和检查点写入 `/mnt/mydata/wja/reasoning-diff`。

```bash
cd /home/wja/reasoning-diff-pr8
export PYTHONPATH="$PWD/src"
PY=/mnt/mydata/zm/projects/RPent/.venv/bin/python
SRC=/mnt/mydata/wja/reasoning-diff/runs/pr8-12h-20261006-r2/smoke/prepare
OUT=/mnt/mydata/wja/reasoning-diff/runs/pr8-shared-prefix-v1
ARGS=(--in-dir "$SRC" --out-root "$OUT" \
      --model qwen3-8b --model-root /mnt/mydata/wja/reasoning-diff/assets/models \
      --gpus 2 3 6 --batch-size 2 --max-new 256 --time-budget-hours 12)

# 只解析旧数据、登记请求与成本，不加载模型。
"$PY" scripts/run_shared_prefix.py --mode plan "${ARGS[@]}"

# 首个已解析赋值 × 每条来源轨迹，三个 baseline + 三个 seed-0 编辑。
"$PY" scripts/run_shared_prefix.py --mode pilot "${ARGS[@]}"

# 重新检查/复用 pilot；只有通过后才扫描本输入中的全部切点、全部前提。
"$PY" scripts/run_shared_prefix.py --mode scan "${ARGS[@]}"
```

当前保存输入含 8 道题、24 条 base，登记 944 个切点；pilot 为 144 条请求，完整 scan 为 39,066 条请求（含已登记 pilot）。这只是旧 smoke cohort 的续写扫描，**不等于正式 32 题或 200 题实验**。固定历史也需要每次 prefill，长轨迹切点可能昂贵；256 只是新 token 上限。`plan_summary.json` 列出请求数、decode 上限及精确前缀字符总量，字符数不是 tokenizer token 数或运行时长估计。

该输入的 pilot 前缀合计 392,319 字符，完整 scan 前缀合计 324,426,528 字符，最长前缀 19,626 字符。实现沿用 HF 批量解码，未实现跨请求 KV 前缀缓存。不要根据“只续写一个值”判断全扫描成本很低；先查看 pilot 的实际 prefill/decode 计数与耗时，再决定是否运行 scan。

pilot 的三个编辑沿用预先登记的第一个目标相关数值事实及两个无关事实，不根据本次响应选择。scan 自动先执行这一 pilot，即使直接调用 `--mode scan` 也不能跳过。源码、输入、模型、预算、GPU/批大小等参数变化后必须使用新输出目录。相同协议可以恢复；已完成请求不会重新采样，pilot 的请求 ID 在 scan 中复用。失败续写也不会通过反复重采样挑选成功结果。

时间预算从首次实际运行开始持久保存，跨 pilot/scan、暂停及恢复都不会延长。到期终止所有活动 worker，标记 `budget_exhausted`，保留已完成的逐请求检查点；任一 worker 异常也会终止其余 worker。完整缓存可以在预算到期后仅重新汇总，不启动模型。检查点内容哈希不匹配则停止并记录错误。

## 通过条件与输出解释

- 每条来源轨迹至少有一个登记切点，全部计划请求都有记录。
- 配对覆盖、共同噪声覆盖，以及非任务前提上的这两项覆盖均至少 50%；分别检查总体、每道题、每个 op 和每条来源轨迹。失败请求仍进入分母。非任务标记来自原任务 DAG，仅作分析注释，不输入模型。
- 不以响应必须改变、效应必须正、模型必须答对为通过条件。pilot 未通过就停止全扫描。

主要输出：`protocol.json`（输入/源码哈希与条件）、`plan.json`（固定历史与请求来源）、`plan_summary.json`、`responses/<request-id>.json`（精确 prefix/generated IDs、seed、状态、预算及哈希）、`pilot_report.json` / `scan_report.json`、同名 `*_contrasts.jsonl`、`pipeline.json` 与各卡日志。报告保留缺失请求、失败分类、按题/难度/来源轨迹覆盖及有符号 excess。

`pipeline.status=complete` 仅说明本条件的工程测量检查通过。`scientific_conclusion` 保持 null，`original_natural_matching_resolved` 保持 false。本条件不自动产出旧 C1 probe、P1 轨迹正确性回归、C2 隐状态干预、P3 或 C4，也不将新结果塞进旧 rho 表。需要研究这些问题时，必须另行定义相应的条件性假设与分析方案。

代码已做离线回归和旧轨迹切点检查；本次未运行真实 Qwen pilot、smoke 或 GPU 实验。
