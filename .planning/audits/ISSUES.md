# Issues Ledger

最终冻结 `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（61 文件）。round-22 与 round-23 独立 A–F 均 PASS，无已确认范围内缺陷。连续通过计数 = 2。r01–r21 旧 hash 不计。

交付状态：`CODE_READY_SERVER_VALIDATION_PENDING`。见 `.planning/FINAL_ACCEPTANCE.md`。

## Standing residuals (not defects)

- C22-U-01 / C23-U-01：fallback 旗标不改 excess
- F22-01：绿 pytest ≠ Goal / 论文正确性
- Plus persist 文件：测试卫生，不在冻结内
- Fixture 八段 offline 前缀 H；tiny `constrained_target` 不是 §4.1 / MODEL-01
- Gate 未注册不是缺陷
- 真实 HF / 官方 dump / CUDA / cgroup / Gate 0–2 / 真实 P1–P3 / 官方 CoT：`pending_server`

## Closed on this freeze (independent)

点名项由 r22/r23 各通道独立 CLI/CE 关闭，不由作者 `local close` 单独关闭。包括 F21-08 合取 sham 锁、F20 hook/calibrate、F19-06 §8 行、XOR `src_b`、同时改名、in-dir pairing、`card` / `forbid_host_exec` / Procrustes / `attention_mean` / `apply_model_template`。
