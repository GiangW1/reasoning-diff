# FINAL_ACCEPTANCE

**状态：`POST_REVIEW_FIXES_IN_PROGRESS / SERVER_VALIDATION_PENDING`**

在声明范围与本机验证条件下，代码验收通过；独立多路审查未发现已确认遗留缺陷。真实模型 / 服务器科学验证仍待运行。这不等于形式证明所有输入和环境绝对无错误，也不意味着论文假说成立。

- 日期：2026-09-24（后续修复工作区）
- 工作区：`C:\Users\22688\Desktop\diff`
- 历史冻结：`1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`；该 hash 已被后续未提交修复修改，不能作为当前工作区冻结证明。
- 连续通过：2（round-22 与 round-23，同一冻结，新 reviewer 上下文）
- 当前工作区本机 pytest：218 passed。绿测试不是论文正确性。

## 停止条件 1–7

| # | 要求 | 证据 | 裁决 |
|---|---|---|---|
| 1 | 原文/协议逐项有归属；原子需求有实现、入口、验证证据 | `.planning/PAPER_TRACEABILITY.md`；论文 hash `F3C0EC08…312EA57C`。可执行行关闭证据是 r22/r23 独立 CLI/CE，不是历史单元格里的 `pytest -q` / `passed_local_tests`。 | **满足（代码层）。** 科学行仍 `pending_server`，已标明。 |
| 2 | 无已确认未解范围内缺陷；无未裁定正确性疑点 | r22 与 r23 的 A–F 均 PASS，无 confirmed in-scope defect。残留：C22/C23-U-01 fallback 旗标不改 excess；F22-01 绿测试≠Goal；Plus persist 卫生；offline H / `constrained_target` 诚实项。 | **满足。** |
| 3 | 本机必要检查实际通过；e2e/边界/失败覆盖；未跑项不伪装通过 | 当前工作区 218 pytest；夹具八段与 scientific tiny 八段仅是 smoke；缺 `tasks.jsonl` 失败；`>96` 拒截断；`isolated_sandbox is False`；`forbid_host_exec` 不执行被包函数。未跑：真实 HF、CUDA、官方 dump、自然 CoT、cgroup 隔离。 | **满足（本机代码层）。** |
| 4 | GSD 阶段与文档一致；软件通过 ≠ 科学通过 | `.planning/STATE.md` 现记代码验收完成、科学未评。REQUIREMENTS 科学复选框保持未勾。 | **满足。** |
| 5 | 连续两轮独立全量 A–F，同一 hash，无新确认缺陷 | r22 报告：`.planning/audits/round-22/{A,B,C,D,E,F}-*.md`。r23 报告：`.planning/audits/round-23/{A,B,C,D,E,F}-*.md`。两轮开审/交卷均为 `1f5f3798…`。r23 未读 r22 通道报告当证据。 | **满足。** |
| 6 | 服务器待验证、外部资产、Gate 未注册全部列明 | 见下方清单。路径已实现；未藏缺失代码。 | **满足。** |
| 7 | 运行说明、依赖、追踪、问题闭环、审查报告、本机记录、服务器入口 | `README.md`、`pyproject.toml`、本文件、`ISSUES.md`、r22/r23 报告、`docs/EXPERIMENT_PROTOCOL.md`。 | **满足。** |

## 两轮审查

| 轮 | 冻结 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| 22 | `1f5f3798…` | PASS | PASS | PASS | PASS | PASS | PASS |
| 23 | `1f5f3798…`（未改） | PASS | PASS | PASS | PASS | PASS | PASS |

r01–r21 绑定旧 hash，不计连续通过。

## 本机入口

```text
python -m pytest -q --tb=line
python -m reasoning_diff prepare --fixture tests/fixtures/t1_tiny.json --out-dir stage_a --eval-mode scientific --split-fractions 0.4 0.15 0.1 0.1 0.1 0.15
python -m reasoning_diff collect --fixture tests/fixtures/t1_tiny.json --in-dir stage_a --out-dir stage_b --eval-mode scientific --backend tiny --weight-seed 0
python -m reasoning_diff label --in-dir stage_a --out-dir stage_c --eval-mode scientific
python -m reasoning_diff fit --in-dir stage_b --labels-dir stage_c --out-dir stage_d --split probe_train --eval-mode scientific
python -m reasoning_diff calibrate --in-dir stage_d --features-dir stage_b --out-dir stage_e --split calibration
python -m reasoning_diff transfer --in-dir stage_d --out-dir stage_f
python -m reasoning_diff intervene --in-dir stage_b --out-dir stage_g --backend tiny --dev-layer-scores 0.05 0.9 0.8
python -m reasoning_diff repair --in-dir stage_b --out-dir stage_h --eval-mode scientific
python -m reasoning_diff analyze --in-dir stage_c --out-dir stage_i
```

夹具八段用 `--eval-mode fixture` 与 `--backend offline`。scientific collect **拒绝** offline 前缀当 H。tiny 随机权重 **不是** MODEL-01。

依赖：`pyproject.toml`（numpy；可选 torch/transformers）。本机已用 Python 3.11.7、torch 2.7.1+cpu、transformers 5.5.3、numpy 1.26.4。

## 服务器 / 数据 / Gate 待办

| 项 | 对应需求 | 已实现路径 | 未验收原因 | 将来命令 / 产物 |
|---|---|---|---|---|
| Qwen3-8B / R1-Distill-Qwen-7B | MODEL-01 | `models/adapters.card` / `load_frozen(..., local_files_only=True)`；revision 钉死 | 本机无权重 | `load_frozen("qwen3-8b")` 或 `r1-distill-qwen-7b`；记录 revision 与 hidden 4096/3584 |
| 官方 iGSM dump | DATA-01 | `tasks/t1_official.py` | 无官方全量 | 按协议导入；`source_kind=official` |
| CUDA / 长链 KV | CAUSAL-01 | tiny hook/KV 接口 | 无 GPU | 服务器上真实 generate + hook |
| 自然 CoT §4.1 | MODEL-01 | `parse_events` 生成区；tiny 现为 `constrained_target` | 诚实非 §4.1 | 真实模型解码后再解析 |
| T2/T3 外部标注 | DATA-02 | GSM-Symbolic/Plus、Hotpot、MuSiQue、HumanEval 适配器 | 缺独立事件图资产 | 导入 sidecar / 人工复核；不得用答案冒充 DAG |
| 隔离代码执行 | EXEC-01 | `IsolatedExecutor` / `UnavailableExecutor`；子进程 `isolated_sandbox=False` | 无 cgroup 后端 | 配置隔离后端后跑 HumanEval |
| Gate 0–2 | 协议 §6 | Week-8 `unregistered` | 阈值未预注册 | 注册后再跑 `analyze`；不得事后选阈值 |
| P1–P3 真实轨迹 | C3 | `analysis.py` 公式入口 | 无真实标签/轨迹 | 服务器数据上 `analyze`；假说不是必现正结果 |
| C2 50 条来源解耦 | CAUSAL-02 | intervene CLI + swap/INLP/rescue | 无真实 donor 队列 | 预定 cohort 后跑 intervene |

缺失代码没有放进本表冒充待服务器。

## 明确非结论

- 论文假说未成立也未证伪。
- fixture / tiny 输出不是科学结论。
- Gate 未注册，没有 pass/fail。
- 作者不是唯一验收者；关闭依据是 r22+r23 独立审查。
