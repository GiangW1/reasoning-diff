# PR10 服务器复核报告回传

[完整中文报告](REPORT.zh-CN.md) · [候选索引](candidate-index.zh-CN.md) · [覆盖表](coverage-all-records.csv) · [算术敏感性](task-sensitivity.json)

缺失的96条PR9全文全部找回并核对原文件/文本哈希与身份摘要；共恢复168条唯一轨迹。本轮重点复核24条，尚未确认严格的纠正后同源实际计算复发。24例共298个完整相关段落，含Python字符区间和逐字原文。此结果不是168条穷尽语义标注、总体复发率或第二位人类金标准。

本目录新增于PR10，原审计目录 `experiments/natural-recurrence-audit-20261010/` 保持原样。服务器审计基线提交为 `4c7cff043e652993e60503e8b94c6768c5cbd5e1`。

本次上传保留报告、覆盖/候选表、题目图及身份索引、168条全文、24例证据、核验信息和离线脚本。没有模型权重、激活或checkpoint等大文件。

- `SHA256SUMS` 校验本次上传目录的文件，运行 `sha256sum -c SHA256SUMS`。
- `SERVER_SHA256SUMS` 是服务器原始完整交付目录的校验清单，留作来源记录。其 `screening/`、`screening-index.json` 和 `source_data/` 属于服务器侧检索缓存及既有归档，不随本次报告重复上传；因此它不是此上传子集的可执行校验清单。
- `verification.json` 是服务器原始交付时的验证结果，源worktree提交/干净状态均指审计基线，上传新增提交不会改写这些历史信息。
- `scripts/` 保留服务器使用的只读恢复/确定性分析脚本，内部路径指向 `/mnt/mydata/wja/reasoning-diff`。恢复和原始验证需服务器的既有responses、PR9轻量导出及PR8归档；这些脚本不生成模型输出。

本轮为既有文本复核，没有新增模型生成、训练、探针、激活采集或干预。上传的报告、表格、全文和逐例证据与已核验服务器交付件逐字节一致。
