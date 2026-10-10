# PR9 正式协议首轮运行

本轮使用正式 C3 流程执行较大规模实验。此前 smoke 验证了真实模型生成、答案筛查和检查点，但没有验证测量、拟合或干预；本轮仍须保留不可估计结果和人工审计要求，不能预先认定完整链路或科学假说成立。

## 固定设计

- PR9 基线：`98ab254822246cace2877ff827ebec7c95d873ba`。
- 本地运行提交：`07cac0c4a8759966acbcf4c355667766f7b8e05b`。
- 源码：`/home/wja/reasoning-diff-pr9-formal`，分支 `codex/pr9-formal-optimized`。优化提交尚未推送。
- 模型：Qwen3-8B，固定 revision `b968826d9c46dd6066d109eabc6255188de91218`，复用本地权重。
- 新数据：`/mnt/mydata/wja/reasoning-diff/inputs/pr9-fresh-20261008/igsm64`。
- 官方生成器 revision：`a1ed1d04600add811beb08b58d9912ed30999642`。
- 生成 seed：2026100800–2026100863；题目 ID 前缀 `igsm-pr9-20261008`。
- 共 64 道新题，op5/op10/op15/op21 各 16 道。全部通过图与答案独立重算验证；与旧 PR7 200 题池的 ID、题面和 seed 均无重合。未根据模型结果挑题。
- 正式划分 seed 7319：probe_train 26、dev 13、calibration 5、direction_fit 6、transfer_pairs 10、test 4。该规模不是经功效分析确认足够的确认性样本量。
- 三条件：base、related_noop、neutral_noop。
- 参考 seed `[0, 1, 2]`，独立噪声 seed `[3, 4, 5]`，全部前提各两个编辑值，保留所有失败与未知。
- 生成上限 32768 tokens；temperature 0.6、top_k 20、top_p 0.95；四层 0、12、24、35。
- 共冻结 15,198 个生成请求：参考 576、噪声 576、编辑 13,926、来源 120；生成上限合计 498,008,064 decode tokens。后续干预调用另计。

## 执行与优化

- 实际 GPU：0、3、6；每卡批量大小 2。
- Qwen3-8B 的 BF16 KV cache 每 token、每轨迹约 144 KiB。32k 输出、批量 4 仅 KV cache 已约 18 GiB，加上权重超过 32GB 卡容量，因此长输出使用批量 2。
- 三卡并行生成和并行层特征采集；GPU 子进程每个 CPU 线程池设为 1，CPU 分析子进程设为 8。
- 复用既有 `fit_cached_inputs.py` 减少事件 JSON 重读；三种特征位置以两个 CPU 作业并行拟合，再使用已完成检查点聚合。
- 缓存 helper 纳入源码哈希；优化不改变标签、采样、题量、编辑次数或划分。
- 优化后相关测试 39 passed（7.42 秒）；全仓库 666 passed（83.51 秒）。
- 先生成全部参考答案。完整可解析答案若仍只有一种正误类别，程序按原协议停止；截断和解析失败不会制造真正的推理错误类别。
- 答案筛查满足条件后，自动继续完整扫描、测量、拟合和干预。各阶段仍可能因不可估计条件停止。

## 时间窗口与续跑

后台启动时间：2026-10-08 20:57:37，Asia/Shanghai。

按上一轮使用 12 小时执行窗口，预计在 2026-10-09 08:57:37 到达窗口上限。这是算力执行窗口，不是全流程完成保证。当前规模远大于上一轮，按 smoke 吞吐外推，全量生成很可能需要数十小时至数天，拟合和干预另计。

`protocol.json` 内的 `time_budget_hours` 保持 null，由外部 launcher 限定本次窗口：超时会结束本轮所有子进程，保存已落盘结果及执行状态。这样下次可以在相同科学协议和源码下续跑，不重置或篡改冻结协议中的预算。恢复仍会检查数据、源码、请求和轨迹校验和。

恢复入口：

```bash
/mnt/mydata/zm/projects/RPent/.venv/bin/python \
  /mnt/mydata/wja/reasoning-diff/launchers/pr9_formal_20261008.py \
  --config /mnt/mydata/wja/reasoning-diff/configs/pr9-formal-20261008-r2.json \
  --out-root /mnt/mydata/wja/reasoning-diff/runs/pr9-formal-20261008-r2 \
  --seconds 43200
```

运行期间不能修改本地源码或科学配置；重复启动会被同目录进程锁阻止。launcher 的 `execution_status.json` 记录本轮进程、代码提交、配置与 launcher 校验和、退出状态。`pipeline.json` 由正式入口记录阶段结果；尚不存在该文件不代表未启动。

## 首次启动的资源冲突

最初按 2、3、6 卡启动，日志保存在 `/mnt/mydata/wja/reasoning-diff/runs/pr9-formal-20261008`。2 卡在模型加载时被另一个任务占用约 21 GiB，发生 CUDA OOM。只结束了本轮自己的进程组，没有停止其他用户任务。该次没有保存参考轨迹。

切换 0、3、6 后使用新输出目录重新冻结。已核验两个计划的源码哈希、数据哈希、完整请求设计与划分一致，仅物理 GPU 配置改变。原失败日志保留。

## 结果与日志

- 本轮输出：`/mnt/mydata/wja/reasoning-diff/runs/pr9-formal-20261008-r2`。
- 配置：`/mnt/mydata/wja/reasoning-diff/configs/pr9-formal-20261008-r2.json`。
- 运行状态：`execution_status.json`。
- 总日志：`logs/launcher.log`。
- 答案筛查日志：`logs/answers-0.log`、`logs/answers-1.log`、`logs/answers-2.log`。
- 原始检查点：`responses/`。
- 完整协议和请求：`protocol.json`、`design.json`、`plan_summary.json`。
- 答案筛查完成后：`answer_screen.json`。

正式协议运行不自动等于确认性证据。最小有意义效应、样本量/功效、多重比较、人工审计和缺失敏感性分析仍按 PR9 文档保留为研究判断；本轮不发布假说成立的自动结论。
