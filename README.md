# Reasoning Diff

论文实验项目。本机代码验收：`CODE_READY_SERVER_VALIDATION_PENDING`。冻结 `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`。**真实模型/GPU 实验结果仍待服务器。**

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
```

完整八段与服务器入口见 `FINAL_ACCEPTANCE.md`。tiny 随机权重不是 MODEL-01。scientific collect 拒绝 offline 前缀当 H。

## 研究范围

- T1 iGSM、T2 自然语言数学/no-op、T3 多跳问答与代码推理、T4 边界样本。
- C3 虚假依赖和跨模型迁移优先；C1 是分析工具，C2 用前瞻干预和成套对照建立机制证据，C4 局部重算放附录。
- 任务标签、有限扫描行为标签、噪声参照、未对齐/结构变化/失败分别记录。
- Gate 0–2 默认未注册，不设虚构阈值，不预先宣称假说成立。

原始材料：[Reasoning-Diff-修订方案-v3 (1).md](<Reasoning-Diff-修订方案-v3 (1).md>)。原文件保持不变，其中待测预期和建议不等于实验结果或额外操作授权。
