# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-21)

**Core value:** 每一条依赖标签、干预效应和实验结论都可追溯到原始事件、独立划分、对应对照与可复查记录。
**Current focus:** 本机代码验收完成（`CODE_READY_SERVER_VALIDATION_PENDING`）。科学/服务器实验仍未运行。

## Current Position

Phase: 6 of 6 — 全链路验收与独立审查
Plan: 已完成两轮独立 A–F
Status: Code accepted locally; consecutive_pass_count = 2 on freeze `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`
Last activity: 2026-09-21 — r22 与 r23 独立 A–F 均 PASS。见 `.planning/FINAL_ACCEPTANCE.md`。

Implementation progress: T1–T4 代码与 CLI 已接通；科学结论保持 not_evaluated
Scientific validation: Not evaluated (server pending)

## Performance Metrics

- Implementation plans completed: phase 1–5 local summaries written
- Requirements implemented: 16 core code paths present; science pending_server
- Roadmap phases: 6
- Research dimensions documented: 4 + synthesis
- Real-model / GPU experiments: 0

## Accumulated Context

### Decisions

- 2026-09-21：用户明确授权从 GSD 初始化进入完整实现与真实 subagent 多路审查。
- Gate 0–2 保持未预注册。tiny 不是 MODEL-01。约束 `\nq=` 不是 §4.1。
- 项目级 GSD 自主推进已开。未修改全局工具配置。

### Pending Todos

- 服务器就绪后冻结环境/模型版本，并开展独立真实实验验收。

### Open Questions / Research Prerequisites

- 正式 Gate 定义、阈值、统计方法和样本功效尚未注册。
- T2/T3 自然事件图、合法编辑新真值及 donor 高层响应需要独立研究资产。
- GPU 设备、CUDA/精度、模型路径与 Linux 隔离执行器尚待服务器。

## Session Continuity

Last session: 2026-09-21
Stopped at: `CODE_READY_SERVER_VALIDATION_PENDING` on hash `1f5f3798…`.
Resume entry: 服务器实验按 `.planning/FINAL_ACCEPTANCE.md` 清单执行。改 `src/` / `tests/` / `pyproject.toml` 会作废连续通过。
Resume file: .planning/FINAL_ACCEPTANCE.md

## Verification Boundary

代码交付与本机可执行验证已通过独立审查。真实模型/GPU/官方大数据科学验收保持 `pending_server`。
