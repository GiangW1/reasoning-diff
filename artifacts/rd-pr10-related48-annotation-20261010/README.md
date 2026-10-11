# 48条相关干扰轨迹标注与独立复核交接

本目录保存48条已有`related_noop`轨迹的来源事件标注、分析报告和独立复核要求。没有新增实验输出，也不修改PR10原审计包。本次标注是待独立复核的判断，不是第二位标注者已经认可的金标准。

## 阅读入口

- [服务器独立复核说明](SERVER_REVIEW.zh-CN.md)：只检查既有轨迹；重点为P31、P69的解释回摆和P22、P47、V58的实际采用判定。
- [分析报告](related48-source-audit.md)：全队列结果、P31与V50比较、同题对照及研究路线的证据边界。
- [统一标注标准](related48-annotation-codebook.md)：区分错误重述、明确分离、疑问、假设、局部反推和后续实际采用。
- [48条逐例索引](related48/INDEX.md)与[24组同题对照](related48/paired-tasks.md)。
- [机器可读标注](related48/annotations.json)、[既有机械校验记录](related48/validation.json)和[证据包哈希](related48/manifest.json)。

## 数据与完整性

输入锁定为提交`c20e0461c7158ec66b1f69abfd8d132cd6b275c8`的`artifacts/rd-pr10-server-recurrence-review-20261010/`。48条来自24道题×seed 0/3，均为相关干扰条件。原始全文位于`related48/raw/`；带段号与标注锚点的全文位于`related48/paragraphs/`；`related48/cases/`保存逐例判断与证据。字符区间使用Python字符串位置，左闭右开，不是UTF-8字节位置。

分析报告、标准和整个`related48/`目录均从本次本地交付逐字节复制；只新增本README、复核说明、离线校验脚本与总哈希清单。不新增模型权重、激活、checkpoint或生成结果。

在仓库根目录运行下列确定性校验，不需要模型、GPU或网络：

```bash
python3 artifacts/rd-pr10-related48-annotation-20261010/verify_package.py
```

校验48条身份、两种子配对、源提交全文哈希、证据切片、清单和本目录相对链接。它不判定语义标签是否正确，也不把标注一致当作复核通过。源提交须存在于本地Git对象库。

## 保留原始判断

独立复核结果请新增到`artifacts/rd-pr10-related48-independent-review-20261010/`并回传PR10，保留本目录作为原始标注快照。只核查现有记录和确定性算术，不运行新生成、训练、探针或干预实验。
