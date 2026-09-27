---
reviewed: 2026-09-21
depth: deep
scope: model generation, collection, causal interventions, local repair, CLI callers
status: issues_found
---

# 模型、因果干预与局部修复独立审查

只读审查实际源码与调用链；未采用旧审计结论。依据原始方案 §2.4、§2.5、§8.2 与 docs/EXPERIMENT_PROTOCOL.md §1、§3、§4。读完 models/ 下全部七个 Python 文件、interventions.py、repair.py，并追踪 CLI、edits、事件解析相关接口。models/ 虽被 .gitignore 的 models/ 规则忽略，本次按明确指定范围检查。

以下 MC-01 是缺少实现，并非“没有 GPU 验证”。其余为源码和 CPU 检查可确认的独立错误。P1 对应 BLOCKER；P2 中的错误也明确标 BLOCKER。没有修改生产代码、测试或项目状态，没有下载或运行大模型。

## MC-01 — [P1][BLOCKER] 科学路径没有连接冻结真实模型，强制目标赋值不能代替自然 CoT

**位置：** `src/reasoning_diff/cli.py:283-301,461-475,1203-1227`；`src/reasoning_diff/models/generate.py:72-101,127-149`；`src/reasoning_diff/models/adapters.py:32-42`。

`load_frozen()` 和 `apply_model_template()` 没有生产调用者。scientific prepare 固定调用 `generate_task_trace`，默认构建随机 Qwen2 小模型；collect 的 scientific 模式只接受 tiny；intervene/repair 也只有 tiny/offline。即使在服务器已有冻结模型权重，也没有完整入口加载该模型及 tokenizer、生成自然轨迹并提取这些轨迹的隐状态。generate_task_trace 使用模 63 字符编码，超过 96 字符直接拒绝；随机生成 8 token 后，强制加入 `\n{target} = `，把词表限制到数字采样两位，parse_status 为 constrained_target。这是已标识随机权重的冒烟代码，不是伪造“真实模型结果”，但仍不能完成已授权实现的真实实验链路。

**CPU 证据：** t1_tiny.json 生成 `parse_status=constrained_target`、一个目标事件、answer=82。源码全局引用搜索只能找到真实 loader 的定义，模板只有测试调用。

**修复：** 保留 tiny 作为明确测试 backend，另接通冻结 checkpoint/tokenizer 的生成、真实 token offset、自然 CoT/答案解析、隐状态、干预和修复；使用对应聊天模板与停止规则。不得把强制写入目标赋值的轨迹作为自然 CoT。

## MC-02 — [P1][BLOCKER] collect 重新编码后处理的字符串，隐状态已不是生成轨迹的隐状态

**位置：** `src/reasoning_diff/cli.py:469-478`；`src/reasoning_diff/models/tokenize.py:9-16`。

collect 无条件 encode_text(trace.text)，只在文本为空时采用已经保存的 trace.token_ids。tiny 的 decode_ids 与 encode_text 不互逆，如 ID 1 解码为 `!`，再编码变成 34。所有自由采样 token 被替换，后续目标事件的前缀隐状态也变化。行为标签来自原生成序列，而特征来自另一条序列；来源交换也无法解释为交换生成时的状态。

**CPU 证据：** 默认 fixture 的自由采样位置 36–43，原 ID `[58,10,40,59,1,56,52,35]` 被替换为 `[28,43,10,29,34,26,22,5]`；同一权重下整段 layer 1 隐状态最大绝对差为 0.0732318312。

**修复：** 始终以采样实际 token_ids 为重放依据，并保存从实际解码到字符位置的正确映射；不要对渲染文本重新编码恢复 token。

## MC-03 — [P1][BLOCKER] 主交换方向随机，INLP 从当前测量样本和伪造标签拟合

**位置：** `src/reasoning_diff/cli.py:908-915,930`；`src/reasoning_diff/models/collect.py:179-186`。

main 和 C-rand 都是随机 QR 子空间，没有读取训练好的任务/行为探针或独立方向拟合产物。INLP 则只用当前 base、donor 两行和 `[0,1]` 区分二者，与要选择性移除的来源依赖/虚假依赖标签无关。每次测试都重新拟合，方向没有 train/dev/test 边界。因而这一入口不能检验选择性 Read-Set 控制，也不能支撑 C3 P3。

**修复：** 在指定 direction_fit 组上拟合并冻结有明确语义目标的方向/投影；保存模型、层、rank、训练组与版本，在留出干预批次只加载，不重新拟合。C-rand 才使用随机子空间。

## MC-04 — [P1][BLOCKER] 因果评分把模型旧答案当正确答案，把单个最终答案当目标和非目标分支

**位置：** `src/reasoning_diff/cli.py:952-979`；`src/reasoning_diff/models/collect.py:223-224`。

gold 取 base_row['answer']，而非任务独立真值；target 判定是新输出数字等于 donor 模型答案；nontarget 判定是该同一个数字等于 base 答案且不同于 donor。没有检查预先指定的非目标事件。对于来源解耦的等值 base/donor，非目标指标不可能为 1，正常保持目标数值也被计为 donor 跟随；错误 base 答案被保持时 task_correct 仍为 1。底层 followed_donor 更直接等同于任意 token 序列变化。

**CPU 证据：** 将两个 trace 的 answer 均设为 17，mock continuation 也输出 17，CLI 报 `target=1,nontarget=0,task_correct=1`。未提供或读取任务真值也得到“正确”。

**修复：** 按来源干预的高层反事实预期与独立任务真值评分；等值条件用于解耦，需要非等值探测条件/明确来源行为读数才能判定来源跟随。分别解析目标和非目标事件，缺失记无效/缺失。token_changed 应仅命名为变化，不作为 donor 跟随。

## MC-05 — [P1][BLOCKER] C-layer 未提取该层的 base/donor，复用了主层向量

**位置：** `src/reasoning_diff/cli.py:907,916-925,985-992`。

features.npz 只有所选 readout 层的 H。选择 weak 后，c_layer_delta(base, donor, ...) 仍用主层 base/donor 差分，只换随机 basis，然后把这个向量加在另一层。没有从弱层各自前缀提取对应表征，因此它并非协议中的“弱层同一交换”；范数一样不能保证这个对照的含义。任意命令行分数还可选中主层本身，代码不约束它确实是不同的弱层。

**修复：** 从相同冻结模型、各条件相同事件边界提取弱层 base/donor，并使用该层适配的方向；基于冻结 dev 曲线选出与主层不同的弱层，按真实 hook 差分记录并匹配幅度。

## MC-06 — [P1][BLOCKER] rescue 加回 donor-base 而非被移除分量，且关键对照没有运行

**位置：** `src/reasoning_diff/cli.py:930-931,982-1000`；`src/reasoning_diff/interventions.py:70-85`。

消融得到 `base @ proj`，应恢复的分量是 `base - base @ proj`；当前 matched 却是 donor-base，结果通常既非原状态也非匹配分量救援。错误来源/随机 rescue 虽在字典里算出来，只有 matched 被实际 decode。已有 C-rand/C-layer 是主交换的对照，并未给 INLP 消融运行范数匹配的两类对照，也未报告消融目标/非目标/正确性/无效输出全指标。

**CPU 证据：** base=[1,2,3]、donor=[3,4,1]，调用当前 INLP 和 rescue，matched 与 base 的 L2 距离为 5.0990195136。mock CLI 实际调用模式恰为 `pi_z_swap,add_delta,add_delta,inlp,replace`：只有一次 rescue，没有错误/随机 rescue 解码。

**修复：** 显式保存被去除的机制分量并用于匹配救援，同时 decode 错误来源/随机救援；消融分别配对自身实际范数的 C-rand/C-layer，保留每条件完整结果。

## MC-07 — [P1][BLOCKER] 干预丢失采集模型身份与 weight_seed

**位置：** `src/reasoning_diff/cli.py:474-480,549,961-996`；`src/reasoning_diff/models/collect.py:157-175`。

collect 可以接受 `--model-kind qwen3` 与任意 `--weight-seed` 并存储其 H；intervene 固定 `qwen2`、三层、默认 weight_seed=0，从不加载输入的模型元数据。换用 qwen3 或非零权重种子后，base/donor 特征与被 hook 的模型完全不同；但仍输出 prospective_decode。按旧特征计算的主范数也不再等于实际 hook 的主扰动范数，破坏控制匹配。

**修复：** 干预从采集产物读取并校验模型/权重/层/tokenizer/采样配置，重建同一个模型；hook 保存实际修改前后向量计算范数。身份不兼容时不得继续标记有效干预。

## MC-08 — [P1][BLOCKER] repair 没有执行输入编辑后的局部修复，full_recompute 甚至丢弃问题

**位置：** `src/reasoning_diff/cli.py:1037-1066`；`src/reasoning_diff/repair.py:61-84,102-108,126-134,207-220`。

repair 使用第一条原始 trace 全文作 new_prefix，不读取编辑后 task/prompt 或编辑集合；slots 是所有前提/节点或硬编码 q，不来自任务祖先与编辑交集，也不读预测 mask。不同方法仅加文字前缀、截断或反转字符串，随机 mask 并未随机选择步骤。执行统一短 decode，没有重算脏槽位并按原序嫁接干净文本，返回 text 还是输入 prompt，输出也未用于逐步/答案评分。连续 k=1..5 只是扩大 slots[:k]，每轮仍用相同原文和 token，没有级联输入编辑/修复。full_recompute 的 mask_prefix 直接返回空字符串，最终实际问题输入变为 `[1]`。

**CPU 证据：** `execute_repair_tiny('full_recompute',['q'],[1],'p1 = 2; q = 3',max_new=0)['prefix_token_ids']` 返回 `[1]`。

**修复：** 接入编辑后的完整问题和现有轨迹，独立计算/加载每种 mask，在原事件槽位依次保留或真实生成；完整重算输入仍须包含编辑后的题目。保存实际合成轨迹、离线评分、token 成本与失败；连续编辑要把上一轮结果与新一轮编辑传递下去。

## MC-09 — [P2][BLOCKER] repair 首个采样前重复将前缀最后一 token 加入 KV

**位置：** `src/reasoning_diff/repair.py:113-123`。

prefill 已把整个 prefix 写进 cache，首次循环又把 prefix 最后一个 token 加到同一 cache，之后才采样。正确首次采样应使用 prefill.logits；当前模型实际条件包含重复 token，计费也遗漏该重复处理。

**CPU 证据：** forward pre-hook 记录为 `forward([35,36,37,33,29,47,35,53,45,59,51,31],past=False); forward([31],past=True); sample`。这个顺序已证明重复，即使某一 seed 下生成 token 恰好未变化。

**修复：** 从 prefill.logits 采样第一 token，随后仅送入刚生成的 token；或共用正确的 decode_loop。

## MC-10 — [P2][BLOCKER] run_repair 的整数生成计数分支必然在到达前抛异常

**位置：** `src/reasoning_diff/repair.py:153-158`。

先 `list(result.get('generated_ids') or result.get('generated_tokens') or [])`，后检查 isinstance(produced,int)。当执行器仅返回 generated_tokens=3 时，list(3) 已 TypeError，该整数分支永远不可达。

**CPU 证据：** `run_repair('task_oracle',['q'],[1],'abc',execute=lambda *a:{'generated_tokens':3,'prefill_hidden':[1,2]})` 抛 `TypeError: 'int' object is not iterable`。

**修复：** 先取得原始值并区分计数和 ID 序列，再计算 n_gen；不要用 truthiness 混淆空列表和缺失。

## 关于 collect 跨 trace 平均 E 的额外证据

`cli.py:479` 对所有 trace 固定使用第一个 task 的 premise spans，`493` 对各变体的 E 平均。这造成编辑条件混入同一个 premise embedding，变长编辑/添加来源后还会用错 span。不能直接声称泄漏了未来 CoT：池化位置通常仍在 prompt，模型是因果结构。应把 E 按 task/trace/premise 身份保存，并使用每个变体自己的 spans；跨条件平均没有对应的自然预测输入语义。

## 最小 CPU 复现脚本

从仓库根目录设置 PYTHONPATH=src，运行下面代码。使用本地安装的 torch/transformers/numpy，随机微型模型，无下载。不要拿 fixture 的数字当科学结果。

```python
import numpy as np
import torch
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.models.generate import generate_task_trace
from reasoning_diff.models.tokenize import encode_text
from reasoning_diff.models.collect import _hidden_at_layer
from reasoning_diff.models.tiny import build_tiny
from reasoning_diff.interventions import inlp_remove, rescue_controls
from reasoning_diff.repair import execute_repair_tiny, run_repair

t = generate_task_trace(load_t1_fixture('tests/fixtures/t1_tiny.json'))
ids, _ = encode_text(t.text)
print(t.metadata['parse_status'], t.answer)
print([(i, a, b) for i, (a, b) in enumerate(zip(t.token_ids, ids)) if a != b])
torch.manual_seed(0)
m = build_tiny('qwen2')
print(np.max(np.abs(_hidden_at_layer(m, t.token_ids, 1)
                    - _hidden_at_layer(m, ids, 1))))
b, d = np.array([1.,2.,3.]), np.array([3.,4.,1.])
p = inlp_remove(np.vstack([b,d]), np.array([0.,1.]))
r = rescue_controls(b @ p, d-b, -d, np.random.default_rng(0))
print(np.linalg.norm(r['matched']-b))
print(execute_repair_tiny('full_recompute', ['q'], [1],
                         'p1 = 2; q = 3', max_new=0)['prefix_token_ids'])
try:
    run_repair('task_oracle', ['q'], [1], 'abc',
               execute=lambda *a: {'generated_tokens': 3, 'prefill_hidden': [1,2]})
except Exception as e:
    print(type(e).__name__, str(e))
```

结果中 0.07323 和 5.099 为本机版本输出，关键断言分别是实际 token 不一致、匹配救援不恢复原向量。实际设备精度可改变精确小数，不影响这些问题。
