# 实施交接

## 本次边界

2026-09-20 仅建立 `gsd-new-project`。2026-09-21 用户授权从初始化进入完整实现、本机验证与真实 subagent 多路审查。

原始论文文件 SHA-256：`F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C`。

## 本机验证（2026-09-21）

- `python -m pytest -q` → 167 passed, exit 0（作者复跑；独立审查须自跑）。
- 当前冻结：`5097c8310b023492eda617986ce11a956309a6452cc00121e0e90167a6f7aceb`（61 files，见 `.planning/audits/round-21/VERSION.md`）。
- F20-01/02：intervene hook 长度间谍；calibrate 实跑忽略兄 `lab`。r01–r20 旧 hash 不计连续通过。Goal 未完成。

## 当前代码入口

```
pip install -e .[dev]
python -m pytest tests -q --tb=short
reasoning-diff prepare --fixture tests/fixtures/t1_tiny.json --out-dir runs/prepare
```

其余子命令见 `docs/SERVER_RUNBOOK.md`。

## 已确认

- 完整范围含 T2/T3 真实适配器；缺图为 unknown/partial。
- 本机没有真实实验条件；GPU/权重/官方全量数据等待服务器。
- Gate 0–2 保持未预注册。
- HumanEval 默认 `executor_unavailable`，无宿主 exec。

## 需要研究者补齐的资产

- 自然语言任务的独立事件 DAG 侧车。
- 每个语义编辑的有效性与更新答案。
- Gate 正式定义与 P1–P3 预注册规则。
- Linux 隔离执行器与服务器路径。
