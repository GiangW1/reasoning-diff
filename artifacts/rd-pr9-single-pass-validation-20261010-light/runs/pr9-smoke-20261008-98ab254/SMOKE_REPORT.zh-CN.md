# PR9 真实模型 Smoke 报告

日期：2026-10-08（Asia/Shanghai）。

## 结论

真实模型生成及答案筛查已完成，进程退出码为 0，没有 CUDA OOM 或程序崩溃。
正式入口按设计在 `answer_screen` 停止，状态为 `stopped_unestimable`：23 条完整答案全部正确，没有完整且可解析的答错样本。另有 1 条截断，不能用它制造真正的推理错误类别。

因此，本轮验证了计划冻结、三卡批量生成、逐条落盘、结果身份校验和单类别停止机制；没有验证完整前提扫描、真实权重特征采集、探针拟合、C2 或 P3 干预，不能宣称全链路通过或科学假说成立。

## 代码与配置

- PR：https://github.com/GiangW1/reasoning-diff/pull/9
- 提交：`98ab254822246cace2877ff827ebec7c95d873ba`
- 本地源码：`/home/wja/reasoning-diff-pr9`，工作区干净，未修改 PR 代码。
- 模型：Qwen3-8B，固定 revision `b968826d9c46dd6066d109eabc6255188de91218`，使用既有本地缓存。
- GPU：2、3、6，每卡批量大小 4；本轮结束后这些实验进程已退出，显存已释放。
- Smoke 配置：`/mnt/mydata/wja/reasoning-diff/configs/pr9-smoke-20261008-98ab254.json`。
- 8 道题，四个难度层各 2 道；参考 seed `[0]`，独立噪声 seed `[3]`，每个前提 1 个编辑值，生成上限 8192 tokens。
- Smoke 划分 seed 为 2，用于覆盖 probe_train、dev、calibration、direction_fit、test；未按模型输出选择题目或调整划分。
- 四层为 0、12、24、35；预算上限 2 小时，实际生成与筛查约 11 分钟。
- 数据来自过去使用过的 PR7 开发池。本轮为工程验证，不是独立确认性实验。

## 实测结果

| 条件 | 预定参考数 | 自然完成且答对 | 截断 |
| --- | ---: | ---: | ---: |
| base | 8 | 8 | 0 |
| related_noop | 8 | 7 | 1 |
| neutral_noop | 8 | 8 | 0 |
| 合计 | 24 | 23 | 1 |

完整答案准确率为 23/23；按所有预定参考、截断计失败的 ITT 正确率为 23/24（95.83%）。二者均只是小样本描述。

截断题目：`igsm-official-0030-op15`，条件 `related_noop`，请求 `trace-reference:120e01aaa7e0ffc858904db2`，停止原因 `max_new`，没有有效最终答案。

实际生成 86,606 tokens。冻结计划共 354 个生成请求：参考 24、噪声 24、编辑 274、来源 32。答案筛查停止后，剩余 330 个请求未运行，没有追加题目、seed 或更改 token 预算。

## 验证与证据

- 本轮新增测试：`tests/test_formal_experiment.py` 和 `tests/test_formal_review_regressions.py`，36 passed，7.22 秒。
- 真实模型运行命令：`scripts/run_formal.py --mode all --config /mnt/mydata/wja/reasoning-diff/configs/pr9-smoke-20261008-98ab254.json --out-root /mnt/mydata/wja/reasoning-diff/runs/pr9-smoke-20261008-98ab254`。
- 完成后重新验证源码哈希、数据哈希、冻结设计以及全部 24 个参考请求的模型 revision、请求身份和轨迹校验和，全部通过。
- `protocol.json`、`design.json`、`plan_summary.json`：冻结协议与请求计划。
- `responses/`：24 条原始参考轨迹及身份校验信息。
- `logs/answers-0.log`、`logs/answers-1.log`、`logs/answers-2.log`：三卡运行日志。
- `answer_screen.json`：完整答案类别、ITT 分类和截断统计。
- `pipeline.json`：`stopped_unestimable`，原因 `answered_references_have_fewer_than_two_correctness_classes`。

后续若需要验证测量和拟合，可按运行手册显式运行固定样本的 `generate`/`measure` 等阶段；单类别的统计限制仍须保留。正式错误预测研究需要独立、足够规模的数据和冻结的决策规则。本轮未启动后续实验。
