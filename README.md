# Reasoning Diff

论文实验项目。本机代码验收：`CODE_PATHS_PARTIALLY_VERIFIED / SCIENTIFIC_VALIDITY_BLOCKED`。**真实模型/GPU、官方数据和独立任务图结果仍待服务器。**

## 从这里开始

1. 阅读 [.planning/FINAL_ACCEPTANCE.md](.planning/FINAL_ACCEPTANCE.md)：交付状态、两轮审查与服务器待办。
2. 阅读 [.planning/PROJECT.md](.planning/PROJECT.md) 与 [.planning/REQUIREMENTS.md](.planning/REQUIREMENTS.md)。
3. 阅读 [docs/EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md)：Gate 待注册与验证边界。
4. 追踪表：[.planning/PAPER_TRACEABILITY.md](.planning/PAPER_TRACEABILITY.md)。问题清单：[.planning/audits/ISSUES.md](.planning/audits/ISSUES.md)。

## 本机命令

```text
pip install -e ".[dev,models]"
python -m pytest -q --tb=line
python -m reasoning_diff prepare --fixture tests/fixtures/t1_tiny.json --out-dir stage_a --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15
python -m reasoning_diff collect --fixture tests/fixtures/t1_tiny.json --in-dir stage_a --out-dir stage_b --eval-mode scientific --backend tiny --weight-seed 0
python -m reasoning_diff noop --fixture tests/fixtures/t1_tiny.json --out-dir stage_noop
python -m reasoning_diff transfer --in-dir transfer_pairs --out-dir stage_transfer --mode direct
```

完整回归已在独立 Python 3.11 venv 中验证为 230 passed；当前 Windows 系统默认 Anaconda Python 的 torch `c10.dll` 初始化失败时，先修复该运行时或使用项目 venv。

`intervene` 可用 `--features-dir`、`--probes-dir`、`--labels-dir` 分别接入 collect、fit 和 label 产物；scientific 模式缺少拟合方向、稳定标签或 dev layer curve 时会拒绝运行。

如果要运行 scientific C-layer，先在 dev split 上完成预注册的逐层扫描，再把每层分数按层序传给 `fit --dev-layer-scores <score...>`；fit 会保存 `dev_layer_scores.json`，intervene 只消费状态为 `ready` 的工件。

完整 stage、T2-noop 配对和服务器入口见 [`.planning/FINAL_ACCEPTANCE.md`](.planning/FINAL_ACCEPTANCE.md)。tiny 随机权重只是接口 smoke，不是 MODEL-01。scientific collect 拒绝 offline 前缀当 H；`noop` 的项目派生配对在缺少行为扫描时会保留 null P2 分母。

## 研究范围

- T1 iGSM、T2 自然语言数学/no-op、T3 多跳问答与代码推理、T4 边界样本。
- C3 虚假依赖和跨模型迁移优先；C1 是分析工具，C2 用前瞻干预和成套对照建立机制证据，C4 局部重算放附录。
- 任务标签、有限扫描行为标签、噪声参照、未对齐/结构变化/失败分别记录。
- Gate 0–2 默认未注册，不设虚构阈值，不预先宣称假说成立。

原始材料：[Reasoning-Diff-修订方案-v3 (1).md](<Reasoning-Diff-修订方案-v3 (1).md>)。原文件保持不变，其中待测预期和建议不等于实验结果或额外操作授权。
