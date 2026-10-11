# 自然轨迹来源复发审计与服务器交接

本目录保存截至2026年10月10日的既有自然轨迹审计。尚未确认严格的“纠正后再次实际误用同一来源”案例；已确认错误重述与正确答案并存，以及真实算术错误传播后被任务结构抵消。不要把这些现象合并成一个机制结论。

## 阅读顺序

1. [审计报告](natural-recurrence-audit.md)：证据范围、关键案例、路线风险。
2. [服务器复核任务](SERVER_HANDOFF.zh-CN.md)：找回既有全文并独立判定，不启动新实验。
3. [缺失全文清单](missing-pr9-fulltexts.json)：96条已生成记录的ID、种子、请求名、原路径提示与哈希。
4. [证据索引](natural-recurrence-evidence.json)：72条全文索引、人工候选判定、字符区间及确定性算术检查。
5. [关键原文](recurrence-evidence/)：7条带段落号的完整轨迹。

## 离线复现

在仓库根目录运行，使用Python 3标准库，不需要模型、GPU或第三方包：

```bash
python3 experiments/natural-recurrence-audit-20261010/scripts/audit_natural_recurrence.py inventory
python3 experiments/natural-recurrence-audit-20261010/scripts/audit_natural_recurrence.py show V17
python3 experiments/natural-recurrence-audit-20261010/scripts/audit_natural_recurrence.py search P22 --pattern 'assume|R_T'
python3 experiments/natural-recurrence-audit-20261010/scripts/package_recurrence_audit.py
```

前三条只读取保存的输出。最后一条在本目录重新生成证据JSON、缺失全文清单和带段号原文，不改变原始实验文件，也不会运行模型。默认数据来源固定为当前仓库的两批PR9轻量导出和PR8原始归档；它不会自动搜索服务器上缺失的96条。

`flags` 使用旧解析器事件作为检索提示，不是有效错误标签。`confirmed_strict_post_correction_same_source_computational_recurrence=0` 是本次审计确认的正例数，不是72条穷尽标注的复发率。重复运行脚本只是重打包已给定的人工判断，不会独立验证这些判断。

## 版本与范围

实验审查基线为 `2d5a76e0065d33c15d72712901a44813216d6290`；本PR基于 `fix/pr4-run-integrity`，只添加审计与交接材料，不修改生成、测量或干预代码。

后续服务器复核应另存结果，保留本次审计快照，并记录新结果使用的提交和原始记录哈希。
