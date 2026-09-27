---
phase: 06-acceptance
review_date: 2026-09-21
depth: deep
status: issues_found
acceptance: NOT_CODE_READY
scope: current_workspace_all_production_modules_and_pipeline
source_hash: 1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb
fixes_applied: false
---

# Cursor 交付独立审查

结论：**当前不能接受 `CODE_READY_SERVER_VALIDATION_PENDING`。** 有真正的生产链路缺失，也有 CPU 即可复现、会改变科学结果的错误。缺少 GPU 可以解释实验尚未运行，不能解释真实后端、数据闭环和指标实现缺失。

本次依据用户确认的代码范围、原始论文、`docs/EXPERIMENT_PROTOCOL.md`、`docs/CURSOR_GOAL_PROMPT.md` 与项目 AGENTS.md 审查。Gate 0–2 的定义/阈值继续保持待预注册，本报告不要求编造门槛或取得正结果。

审查采用主线程工程复现 + 三路新上下文 reviewer（数据测量、数学统计、模型因果）。独立执行 `python -m pytest -q --tb=short`：**172 passed in 61.10s**。按 round-23/VERSION.md 的确切顺序复算 61 个源代码/测试/配置文件，hash 与 Cursor 交付完全一致。测试通过与本报告发现并不矛盾：现有测试覆盖的断言不足以证明论文实验已经实现。

没有修改生产代码、测试、原有验收状态或原有审查报告。仅新增本报告、分路报告与复现材料。未下载真实权重，未运行 GPU 实验。

完整分路证据（包含主表未展开的问题及复现）：

- [模型、因果与局部修复：MC-01–10](C:/Users/22688/Desktop/diff/.planning/audits/codex-review-2026-09-21/model-causal.md)
- [数据与测量：DM-01–16](C:/Users/22688/Desktop/diff/.planning/audits/codex-review-2026-09-21/data-measure.md)
- [数学统计与基线：CR-S01–12、WR-S01](C:/Users/22688/Desktop/diff/.planning/audits/codex-review-2026-09-21/science.md)
- [工程复现脚本](C:/Users/22688/Desktop/diff/.planning/audits/codex-review-2026-09-21/pipeline_repro.py)与[实际输出](C:/Users/22688/Desktop/diff/.planning/audits/codex-review-2026-09-21/pipeline_repro_results.json)

分路编号与主表有重叠，不应相加当作独立缺陷总数。BLOCKER 指阻止当前论文代码范围验收，并非声称所有条目都是 P0 紧急故障。

## 优先处理的验收问题

| 编号 | 优先级 | 发现与实际影响 | 位置 / 详细证据 |
|---|---|---|---|
| R01 | P1 | 正式模型没有接入生产链路。scientific collect 仍只接受 tiny，生成受控的两位数字；换服务器不能自动成为冻结预训练模型的自然长链实验。 | `src/reasoning_diff/cli.py:461–480,1207`；模型因果报告 |
| R02 | P1 | 训练/校准只检查用户传入的 split 字符串，未核验数据身份。实际 test 数据可同时用于 scientific fit 和 calibrate。 | `src/reasoning_diff/cli.py:585,756`；下方 E01 |
| R03 | P1 | 校准把行为依赖裁到任务祖先中，缺少观测标签时又回退到 DAG，并强制认为标签已知；恰好会漏掉研究关注的虚假依赖。 | `src/reasoning_diff/cli.py:803–810`；数学统计报告 |
| R04 | P1 | C2 主干预子空间是随机 QR 方向，INLP 在当前 base/donor 两行上临时拟合人造 0/1；没有训练好的依赖子空间输入。 | `src/reasoning_diff/cli.py:912,930`；模型因果报告 |
| R05 | P1 | 干预的 target/non-target/correct 是对最终模型答案的比较；把 base 模型答案当正确答案，来源改变但值相同的 donor 会把“未改变”记成成功。 | `src/reasoning_diff/cli.py:952,966–973`；模型因果报告 |
| R06 | P1 | C3 只读取预先手工提供的汇总表，生产链没有从测量、干预记录生成 P1/P2/P3 数据表的路径。迁移分析固定调用 `direct_transfer(4096,3584)`，不评估传入模型。 | `src/reasoning_diff/cli.py:1084–1126`；数学统计报告 |
| R07 | P1 | 观测把多次同名事件合并为 node_id，未对齐/消失的事件直接丢失；破坏步骤身份与结构变化分母。 | `src/reasoning_diff/cli.py:238–254`；数据测量报告 |
| R08 | P1 | 有限扫描中的 no_change 不形成对应有限协议的负例；没有观测支持或图未知时仍可能产生数值密度。 | `src/reasoning_diff/measure.py`；数据测量报告的具体行号与反例 |
| R09 | P1 | 附录 repair 使用原题前缀和固定解码，没有按编辑后的题目、依赖掩码与原轨迹槽位执行嫁接；full_recompute 还会丢掉题干。 | `src/reasoning_diff/cli.py:1037–1064`、`src/reasoning_diff/repair.py`；模型因果报告 |
| R10 | P1 | scientific 基线明确返回 refused；没有注意力采集和依赖集合 verbalizer 的完整调用路径，边界 MLP 只用全 1 标签训练。 | `src/reasoning_diff/cli.py:660–682`；需补齐 BASE-01/ATTN-01/VERB-01，而非标记服务器待验证 |
| R11 | P1 | 失败的 manifest 也被 resume 认作完成，退出码为 0，但所需模型文件不存在。 | `src/reasoning_diff/cli.py:38–65`；下方 E02 |
| R12 | P1 | resume 没有绑定全部影响结果的配置与当前输入；改变 split seed 后仍默默沿用旧数据划分。 | `src/reasoning_diff/cli.py:274–281`；下方 E03 |
| R13 | P1 | 多题输入只取第一题，500 题及 op 配置仅校验声明，没有执行完整数据批次。 | `src/reasoning_diff/cli.py:171–190`；DM-08 |
| R14 | P1 | collect 从渲染文本重新编码，tiny 编解码不互逆，重放 token 与实际生成 token 不同，隐状态和行为标签不再对应。 | `src/reasoning_diff/cli.py:471–478`；MC-02 |
| R15 | P1 | F1 通过 flatten 与 JSONL 行序匹配；仅反转相同标签的行序，F1 从 1 变为 null。 | `src/reasoning_diff/cli.py:1151–1154`；CR-S02 |
| R16 | P1 | P2/P3 对多行输入只读取第一行，配对效果随记录顺序发生符号翻转。 | `src/reasoning_diff/cli.py:1113,1125`；CR-S03 |

这是优先修复清单，不是全部发现。分路报告还列出真实 token 重放不一致、跨条件 E 混合、救援公式与对照缺失、数据集答案/ID 错误、标签与预测未按身份连接、迁移映射丢均值等独立缺陷，修复时不能只关闭上表。

## 主线程工程复现

复现脚本：`.planning/audits/codex-review-2026-09-21/pipeline_repro.py`。

运行：

```powershell
python .planning/audits/codex-review-2026-09-21/pipeline_repro.py
```

结果保存于同目录 `pipeline_repro_results.json`。脚本只在临时目录生成输入/产物，不更改生产代码。hash 配方与 Cursor round-23 完全一致。

### E01 [P1] 应从持久化数据身份验证 split，而非相信 CLI 默认值

位置：`src/reasoning_diff/cli.py:585`、`752–756`，以及 collect 未保留/校验 split 的路径。

用现有 T1 夹具、split seed=8 prepare 后，`splits.jsonl` 明确为 `role=test`。collect 后，分别以 scientific 模式调用 fit 和 calibrate，不伪造或修改任何 split 记录，两条命令均返回 0。fit 默认字符串是 probe_train，calibrate 默认字符串是 calibration；实际数据从未换过。校准 n=1 的无穷阈值是正确的小样本处理，但不能消除训练/校准/test 复用这一缺陷。

修复：在真实记录/base_group_id 上持久化并验证各角色，拒绝跨阶段复用与测试专用家族；模型拟合和校准须检查上游划分证据，不能仅依赖调用者字符串。

### E02 [P1] 仅成功且产物完整的阶段才能 resume 跳过

位置：`src/reasoning_diff/cli.py:44–65`，错误 manifest 写入于 `1259–1261`。

对不存在的 features 目录执行 fit，首次正确抛出 FileNotFoundError 并写 `success_count=0,failure_count=1` 的 manifest。原命令追加 `--resume` 后却返回 0，`probes.jsonl` 仍不存在。失败 manifest 的哈希当然可以自洽，但它不是完成证据。自动工作流会因此跳过真实失败阶段。

修复：恢复判定须核验成功状态与该阶段必需产物，再核验哈希；失败记录不能作为完成标记。

### E03 [P1] resume 必须比较全部科学配置及当前输入身份

位置：`src/reasoning_diff/cli.py:274–281`、`38–58`。

先 seed=8（test）prepare，再用同一输出目录 `--resume --split-seed 0`（应为 probe_train）。命令返回 0，manifest 字节不变，保存的仍是 test。原因是用于 resume 比对的 config 只有 command/edit_premise/edit_value/eval_mode/kind。其他阶段也有仅比较 command 的情况；当前输入路径/内容未进入恢复判定。

修复：比较完整、规范化的实验配置、输入内容身份及模型身份。不匹配时明确拒绝复用或生成新运行；不得悄悄返回旧产物。

### E04 [P1] HumanEval 所需隔离执行器尚未实现

位置：`src/reasoning_diff/executor.py:97–102`。

get_executor 只有 spy、普通 child_process 和 UnavailableExecutor。隔离类默认永远返回 executor_unavailable；唯一可执行实现明确 `isolated_sandbox=False`。没有可以配置后在服务器实际调用的隔离后端。这是 OPS-01 的代码缺口，不是仅等待服务器测量。当前诚实记录不可用是正确的，但不能据此把实现验收通过。

### E05 [P2] 交付时模型模块会被 Git 忽略

位置：`.gitignore:13`。

`git check-ignore -v -- src/reasoning_diff/models/adapters.py src/reasoning_diff/models/collect.py` 都命中 `models/`。当前生产模型目录未跟踪，普通 git add 不会收录；克隆后会缺少必需模块。这个 ignore 规则在 Cursor 实现前就存在，本报告不把规则本身归因为 Cursor 新增；但将新源码放入被忽略目录后，代码仓库交付需要修复该冲突。建议把权重目录规则锚定为仓库根目录 `/models/`，并确认所有生产 Python 文件被跟踪。

## 后续验收方式

1. 先补齐真实后端和按题批量的生产闭环，再修复事件身份、标签、数据划分和校准；这些会影响后续一切结论。
2. 用正确训练/校准产物接上迁移、干预、C3 和修复，不接受随机方向、固定维度或手工汇总数值充当实验实现。
3. 每个确认问题添加独立反例测试，覆盖记录重排、重复事件、unknown、失败恢复和分组重叠；不要只断言返回状态字段。
4. 修复后重新对同一最终代码做独立全链路审查。当前既有“连续两轮无问题”的验收结论应作废，但本次 review 不擅自修改原状态文件。
5. 服务器真实权重/长链/显存/运行时间及科学效果继续单列待运行。不能保证所有未来输入绝对无 bug；可以要求所有确认缺陷关闭且可执行需求有实证。
