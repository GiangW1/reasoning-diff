# C：数学与统计独立审查（round-07）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性 \(\sigma(h^\top UV^\top e+b)\)、\(\lambda_{\mathrm{FN}}=10\)、split conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)、\(k>N\Rightarrow+\infty\)、P1 留出 \(\Delta\mathrm{AUC}\) 簇 bootstrap、P2 配对 no-op 分母、P3 vs 对照、S/M/excess、交换/INLP/\(\mathrm{IE}_Z\)/C-rand/C-layer、repair 预算、`direct_transfer(4096,3584)` N/A、PCA 后 Procrustes 且 `truncated=False`。仍错则给反例。round-06 **无 C 交卷**；本通道对当前树独立审查，不沿用他通道、不采信 ISSUES 的作者 `local close`。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读任何 round-07 的 A/B/D/E/F。体例对照过 `round-05/C-math.md`，**结论全部由本轮对当前磁盘字节的公式推导与数值反例重做**。未读 round-06 `C-math.md`（任务声明该轮 C 未交卷）。
- 声明冻结哈希：`9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801`（`.planning/audits/round-07/VERSION.md`，60 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**否 / HASH_MISMATCH**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改（只写本文件）
- numpy：1.26.4；CPython 3.11.7

---

## 1. 冻结哈希

范围内文件数：**60**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 17 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「60 files」一致。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 时刻 | SHA-256 | 与声明值 |
|---|---|---|
| 审查开始（独立执行 VERSION 脚本） | `9814019a8401e727bd132fa5188ac42c0e1197feedacd87e3b7f8c2db4f95801` | **当时 HASH_MATCH** |
| 手检中途（同一脚本，连续两次） | `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e` | **HASH_MISMATCH** |
| 报告落盘后再算 | `129d5405595f32c03bcb4316e96f0bbb955eb6565e582f3380933efac2079965` | **HASH_MISMATCH** |

本通道未改 `src/`、`tests/`、`pyproject.toml`。工作区在审查进行中被其他进程改写（测试从 37 条变为 38 条；`cli.py` 在手检后从 `2f1fac48…` 变为 `de004c9d…`）。**不得把声明冻结 `9814019a…` 标为已复核通过。**

除 `cli.py` 外，§2 所列公式文件的逐文件 digest 在 `1b88bec2…` 与 `129d5405…` 之间未变。`cli.py` 的 fit/calibrate/analyze **被引缺陷逻辑未改**（仅行号下移）；C7-M-02 现指向 **1022–1046**。附录 `cli.py` 已改为交卷前最后一读的 `de004c9d…`。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | `score`/`predict_matrix`/`fit`/`weighted_bce`；NaN 行掩码 | 全文；独立数值 + 有限差 + 哨兵 + NaN/Inf 行 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | `sequence_score`/`conformal_threshold`/`predict_set` | 全文；手算 \(k\)；\(k>N\Rightarrow+\infty\) |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | Hidden=256；BCE 符号 | 全文；\(y=0,z=10\) |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | `_auc`/`_fit_scores`/`p1_incremental`/`_bootstrap_p1`/`p2_paired`/`p3_recovery`/`cone_fit`/`week8_decision` | 全文；r05 反例重跑；独立簇 bootstrap |
| `src/reasoning_diff/measure.py` | 1–345 | `1fa2360e680d37ad086c9a81b3ec684c9d9d1e73affb0d906ff5a97231986df2` | S/M/\(\rho\)/excess；`event_density_sets` | 全文；0-hit / hit / 空分母 / 负 excess |
| `src/reasoning_diff/transfer.py` | 1–75 | `d31bcd499a51ca94c28dca6c97cdbd5c5e3f05db996d15934e5b7d0b5bb22407` | `direct_transfer`/`fit_linear_map`/`_pca_project`/`common_dim_then_procrustes` | 全文；4096≠3584；PCA≠截断；\(n<d\) |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | `apply_swap`/`inlp_remove`/`ie_z`/`c_rand_delta`/`c_layer_delta` | 全文；手算投影与范数 |
| `src/reasoning_diff/baselines.py` | 1–125 | `3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc` | rollout / verbalizer / 文本对照 | 全文（非本通道主公式） |
| `src/reasoning_diff/repair.py` | 1–223 | `d547ab99e3179093348b84c0a65b48ee84d1eee9ff4a72703dd70c01fc7a113c` | `repairability`/`recompute_ratio`/`consecutive_repairs` | 预算公式；零分母 |
| `src/reasoning_diff/cli.py` | 573–1211 | `de004c9dac18c3aef0fb90db3f854d387708d3e5db6903ff6a71ff4e51f10946` | `cmd_fit`/`cmd_calibrate`/`cmd_analyze`（兼读 intervene/repair 调用） | 只读调用链；复现 \(a(X)\) 与 P1 回退表。手检后字节被外部改写，缺陷逻辑仍在 |
| `src/reasoning_diff/graphs.py` | 1–46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | `ancestors` = 前提祖先 \(R_{\mathrm{task}}\) | 对照校准 rsi |
| `tests/test_science.py` | 1–103 | `cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36` | conformal / 4096≠3584 | 查是否独立 oracle |
| `tests/test_measure.py` | 1–40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | 负 excess / 零分母 | 集合路径 |
| `tests/test_round05_regressions.py` | 1–197 | `bc837c0c3a6ea3ae440d6c939c210674070ca7bf80ee6c3cb2644d7b04c515a2` | P1 bootstrap 字段；PCA `truncated` | 查能否关闭缺陷 |
| `tests/test_round06_regressions.py` | 1–136 | `a4421f11d41e174369374ea26746e387e860d35edce9f380b077cab7e69ae0a4` | `lo<hi`；sham hit→null | 查是否锁错公式 |

调用链只读、不计入“已证明正确”：`cli.cmd_fit` / `cmd_calibrate` / `cmd_analyze` / `cmd_intervene` / `cmd_repair`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文：`Reasoning-Diff-修订方案-v3 (1).md` §2.4–2.6、§3、§4.2、§5–7、附录 S2–S3；PITFALLS 校准/P1/P2/噪声条；REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01 / BOUND-01 / FIT-01。

### 3.1 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b)=\sigma(\langle h_i U,\,e_j V\rangle+b),\quad
(HU)(EV)^\top\text{ 为矩阵形式}.
\]

默认 \(r=64\)，\(\lambda_{\mathrm{FN}}=10\)。未知不得进入 \(\mathcal K=\{i:\mathrm{mask}_i\land y_i\in\{0,1\}\land h_i,e_j\text{ 有限}\}\)。空 \(\mathcal K\) 是无效损失，不是 0。NaN/非有限隐状态行不得把 NaN 写入梯度或权重 JSON。

`score` / `predict_matrix` 与上式一致。`fit` **44–49** 与 `weighted_bce` **93–101** 把 \(\mathcal K\) 限制为有限且 \(y\in\{0,1\}\)；并对 \(H\) 行 / \(E\) 行做 `isfinite` 掩码。空 \(\mathcal K\) 分别返回 `no_known_labels` / NaN。`H_fit=nan_to_num` 只服务矩阵乘；梯度被 `known` 挡住。

### 3.2 Split conformal 与 \(a(X)\)

\[
a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij}),
\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow q=+\infty\)。\(\alpha\notin[0,1)\) 必须拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。任务头与行为头**分别**校准。\(N\) 是可交换问题/轨迹单位，不是 seed。

`conformal_threshold` 的 \(k\) 与非法 \(\alpha\) 分支与上式一致。`predict_set` 为 \((1-p)\le q+10^{-12}\)。`sequence_score(..., truth_indices=)` 可对指定列取 \(\max(1-p)\)；省略 indices 仍对传入全部列取 max。

CLI `cmd_calibrate` **761–768** 现按 `ancestors(nid)∪{nid}` 过滤列，再按问题取 max。祖先齐全时对齐 \(R_{\mathrm{task}}(s_i)\)；祖先缺失时退化为 \(a=0\)。仍只用第一条带 `U` 的探针（任务头），不单独校准行为头。

### 3.3 迁移与几何

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。无标签配对：中心化后正交 Procrustes（同维）或中心化 lstsq（异维）。监督适配必须是不同估计程序，且必须有标签张量。附录 S3：先在配对集合上学共同维映射，再 Procrustes；不得静默截断坐标。

`direct_transfer(4096,3584)` 返回 `not_applicable_dimension_mismatch`。`_pca_project` 是中心化 SVD，不是 `x[:,:d]`。`common_dim_then_procrustes` 把 `truncated=False` **写死**。当 \(n<\min(d_A,d_B)\) 时 PCA 秩不足，两路投影形状不一致，Procrustes 走 `not_applicable_shape_mismatch`，旗标仍称未截断。

### 3.4 P1–P3

- **P1：** 在 train 拟合控制模型 vs 控制+\(\rho\)（logistic / IRLS）；在**留出**基础题上比 Mann–Whitney AUC。平局贡献 \(1/2\)。须附**问题级聚类 bootstrap**：重采样基础题（簇），每次重算 \(\Delta\mathrm{AUC}\)，再取分位数。默认路径不得写死 `len+0.01*op`。`y` 是逐题对错，\(\rho\) 是 \(\rho_S(T)\)（或已声明的 excess），不是前提级 task/behavior 标签。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\) 必须共用分母 \(|P\setminus R_{\mathrm{task}}|\)；缺配对不得崩。须有 `shared_premises` 且 \(|\mathrm{shared\_premises}|=\) 声称分母。
- **P3：** 相对 C-rand / C-layer；报告非目标响应与相对基线 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

### 3.5 Excess / 交换 / INLP / 对照范数 / 锥 / 预算

\(S=B\setminus T\)，\(M=T\setminus B\)，\(\rho_S=|S|/|P\setminus T|\)，\(\rho_M=|M|/|T|\)。空分母 N/A。缺失噪声协议 ⇒ excess = null。已评估且 0-hit ⇒ \(N=\emptyset\)、noise \(=0\)、excess \(=\) raw。有 sham hit 时论文要求 \(N=\) 命中前提并扣除：\(\mathrm{excess}=\mathrm{raw}-|N\setminus T|/|P\setminus T|\)，**不是**把 excess 改成 null。excess 可负。\(\rho_S(T)=\frac1n\sum_i\rho_S(s_i)\)。

交换 \(H'=H_b+\Pi_Z(H_d-H_b)\)。\(\mathrm{IE}_Z\) 为下游 \(g\) 在 do 干预与 base 下的期望差；代码 `ie_z` 是已算好的 \(g\) 样本均值差。INLP：每步在**已投影** \(H\) 上重拟合，再累乘 \(I-uu^\top\)。C-rand / C-layer 必须缩放到该样本主干预实际 \(\|\Delta\|\)。

附录 S2：\(|\mathrm{cone}|/n\approx 1-\exp\{-\lambda(1-x)^\gamma\}\)，必须对 \((\lambda,\gamma)\) 做拟合；\(R^2\) 只作描述。Week-8 Gate 0–2 无预注册阈值时必须保持 `unregistered`，不得发明通过线。

论文 RR \(=|\hat D|/n\)（步数）；同预算按重算槽位的原始 token 数。代码 `recompute_ratio=slots/n`，`repairability=1-\mathrm{generated}/\mathrm{full\_recompute}`（token）。零分母 → null。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U`/`e@V` vs `score`/`predict_matrix` | **通过**（误差 0） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(1.2272895322281534\) | **通过** |
| CHK-04 | 空 mask；`y=-1`/`2`/`0.5`/`nan` | 直接调用 | **通过**：哨兵均等于仅正类项 \(2.231435513142097\)。空 mask → NaN |
| CHK-05 | `fit(-1)` 是否等于 `fit(nan)` | 同初值一步 | **通过**（\(\Delta U=0\)，loss 同 \(3.9363613530420953\)）。空 \(\mathcal K\) → `no_known_labels` |
| CHK-06 | `fit` 梯度 | \(U_{00}\) 解析 vs 有限差，相对误差 \(1.42\times10^{-9}\) | **通过** |
| CHK-07 | **bilinear NaN/Inf 行掩码** | 在已知 \(H\) 下追加全 NaN 行或含 \(+\infty\) 行，Y 仍标 0/1 | **通过**：\(\|U-U_0\|_\infty=0\)，\(U\) 有限 |
| CHK-08 | \(k=\lceil(N+1)(1-\alpha)\rceil\)；**\(k>N\Rightarrow+\infty\)** | \(N=4,\alpha=0.4\Rightarrow k=3,q=0.3\)；\(\alpha=0.1\Rightarrow+\infty\)；\(N=1,\alpha=0.05\Rightarrow+\infty\)；\(N=3,\alpha=0.5\Rightarrow k=2,q=0.2\)；\(N=10,\alpha=0.05\Rightarrow+\infty\)；\(\alpha=0\Rightarrow+\infty\) | **通过** |
| CHK-09 | \(\alpha\ge1\)、\(\alpha<0\)、`None` | \(\alpha=1,1.5,-0.1,\mathrm{None}\) | **通过**（`invalid`，`q is None`） |
| CHK-10 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**：无 slack 为 False（浮点），`+1e-12` 后为 True。`0.4` 排除；\(q=+\infty\) 全选 |
| CHK-11 | `sequence_score` / CLI \(a(X)\) | `[0.9,0.1,0.8]`；两事件异真边；复现 `cmd_calibrate` **761–768** | **库函数部分通过**：`truth_indices=[0]` → \(0.1\)；无 indices 仍 \(0.9\)。**CLI 祖先齐全：论文 0.1，代码 0.1**（C5-M-02 该反例关闭）。祖先缺失 → \(a=0\)（残留） |
| CHK-12 | **`direct_transfer(4096,3584)` N/A** | 直接调用 | **通过**（`not_applicable_dimension_mismatch`）。同维 `applicable` |
| CHK-13 | labeled 缺张量 | `labeled=True, labels=None` | **通过**（`supervised adapt requires a label tensor`） |
| CHK-14 | labeled vs unlabeled | 平移 \(X'=X+c\)；翻转 0/1 | **通过（程序已分列）**：unlabeled \(\|W-I\|_\infty=0\)；labeled \(0.424\)。翻转 \(\Delta W=0\)（C7-U-01） |
| CHK-15 | 常数分数 AUC 与平局 | `_auc(ones,[0,0,1,1])`；`[1,2,2,3]` vs `[0,0,1,1]` | **通过**（0.5；手算 0.875） |
| CHK-16 | 默认 P1；留出；`precomputed` | \(n=40\)，`len≡10`，`op~N(0,1000)`，`rho=y` | **默认通过**（`requires_held_out`）。**留出通过**：`auc_full=1`，`auc_base=0.71`，\(\delta=0.29\)。**`precomputed` 通过**：\(\delta=0.5\) |
| CHK-17 | 留出拟合是否忽略 eval 行的 \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 差 0；eval 分数变 \(0.598\)） |
| CHK-18 | **P1 bootstrap 是否重采样簇并重算 \(\Delta\mathrm{AUC}\)**（r05 反例） | 同上；`groups=i//2`；独立实现对照 | **通过**：代码区间 \([0.0737,0.7263]\)，宽度 \(0.653\)，**不是** \([0.29,0.29]\)。独立簇 200 次区间完全相同。`status=resampled_delta_auc`，\(n=200\)。仅传 `rng` 仍 bootstrap \(\rho\) 均值（C7-U-02） |
| CHK-19 | P2 减法、None、支持集 | `0.2/0.5`；无支持集；`None`+匹配列表；`99` vs `['p1']`；`0.9` 对分母 4 | **asked 项通过**：`denominator_unverified` / `missing_pair` / `denominator_inconsistent`；有支持集差值 \(0.3/-0.2\)。**残留**（C7-U-03）：`0.9` 对分母 4 仍 `ok` |
| CHK-20 | P3 相对对照、非目标、禁句 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline_acc=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`nontarget=0.2`，`causal_reverse_claim is False` |
| CHK-21 | INLP 更新 \(H\) | \(H=[[2,0],[2,0],[0,1],[0,1]]\)；手算 \(w=(0.5,-1)\) | **通过**：一步后 \(HP=\[[1.6,0.8],\ldots]\)；两步后 \(\approx0\)；`max\|P1-P8\|=0.8` |
| CHK-22 | C-rand / C-layer 匹配主范数；\(\mathrm{IE}_Z\) | seed=0 主范数 | **通过**：`actual_norm=3.5924442055345125` 与主范数 `isclose`；缺 `target_norm` 抛错；零 \(\Delta\) → `zero_norm`。`ie_z([1,3],[0,0])=2`（样本均值差） |
| CHK-23 | 交换公式 | \(e_1+\Pi_{e_2}(e_2-e_1)=e_1+e_2\) | **通过**（`[1,1]`） |
| CHK-24 | **空分母 → null**；**signed excess 不截断** | 手算 −0.5；\(P=T=\{p1\}\) | **通过**：`rho_S_excess=-0.5`；空分母 `rho_S_raw is None`，`denominator_S is None` |
| CHK-25 | 0-hit 已评估；缺 sham；矩阵缺 noise | 三前提；`noise_evaluated=True` | **通过**：raw=1、noise=0、excess=1。缺协议 / 矩阵 `noise=None` → excess null |
| CHK-26 | 并集 \(\rho\) vs 事件均值 | 两事件 \(1\) 与 N/A | **通过**（`aggregation=mean_over_events`）。N/A 被跳过再平均（C7-U-04） |
| CHK-27 | **有 sham hit 时 excess** | 论文 \(P=\{p1,p2,p3\},T=\{p1,p2\},B=N=\{p3\}\)；对照 `event_density_sets` | **失败**（C7-M-01）：手算 excess \(=1-1=0\)。`noise_set=['p3']` 得 0。`event_density_sets` 在 `noise_ref==1` 时把 `noise_set=None`，excess **null**（`noise_set_missing`） |
| CHK-28 | Boundary Hidden=256；BCE 符号 | \(y=0,z=10\) | **通过**：报告 \(10.000045398900186\)，与真 BCE 相同；`hidden=128` 拒绝 |
| CHK-29 | `cone_fit` 是否拟合 | \(y=1-e^{-0.8(1-x)^{1.5}}\)，\(n=12\) | **通过**：`r2=0.9776421802579095`，\((\hat\lambda,\hat\gamma)=(0.6812920690579611,1.2)\)。`wording=descriptive_only` |
| CHK-30 | Week-8 无发明门 | 默认；`excess==0`；传入阈值 | **默认通过**：三门 `unregistered`，`scientific_conclusion is None`。`excess==0` 自动 `c3_negative_descriptive`+跳过 P2/P3（C7-U-05）。传入阈值标 `compared`，**不**发明 pass/fail 通过线 |
| CHK-31 | **PCA 后 Procrustes，`truncated=False`** | `eye(4)` vs `eye(3)`；\(n=20,d=8/5\)；\(n=2,d=5/3\) | **部分通过**：投影 \(\neq\) 前 3 列（\(\|ap-a_{:,:3}\|_\infty=1.45\)），旗标 `truncated=False`。\(n=20\) 得 `adapted_geometry`。**\(n<\min d\)**：形状不一致，`not_applicable_shape_mismatch`，旗标仍 False（C7-M-03）。`eye(4)/eye(3)` 样本数也不等 |
| CHK-32 | repair 预算零分母 | `repairability(3,0)`；`recompute_ratio(1,0)` | **通过**（皆 None）。`1-3/10=0.7`，`2/5=0.4` |
| CHK-33 | CLI analyze 无 `p1_table` 时的估元 | 复现 **1022–1046**：6 行 task/behavior 标签，全 `event_id=q` | **失败**（C7-M-02）：\(y=\) task_label，\(\rho=\) behavior_label，`length≡1`，`op≡0`。\(\delta=-0.5\)。单一簇 bootstrap 区间 **\([-0.5,-0.5]\)** |
| CHK-34 | `pytest` 指定四文件 | `tests/test_science.py tests/test_measure.py tests/test_round05_regressions.py tests/test_round06_regressions.py -q --tb=line` | **38 passed，exit 0**（审查中途曾为 37；交卷为 38）。绿测试不是公式正确 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | 本机无论文权重；CLI 校准在祖先缺失时 \(a=0\)；analyze 回退估元错误（C7-M-02） |
| 阅读其他 round-07 通道 | 任务禁止 |
| 全仓库 pytest（作者声称 143） | 任务只要求四文件；未采信 143 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用分数值域、污染 eval \(X\)、检出 \(\rho=y\) 代替 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\) |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | \(0\le\alpha<1\) 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | `work = work @ step`；一步与手算 \(w=(0.5,-1)\) 一致 |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm`；匹配主范数 \(3.5924442055345125\) |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels`。NaN \(H\) 行亦掩码（CHK-07） |
| C2-M-02 默认 P1 非留出 | **关闭** | 省略 `held_out` 且非 `precomputed` → `requires_held_out` |
| C3-M-02 P1 非 logistic / `precomputed` 魔法系数 | **关闭（点估计）** | `_fit_scores` 为 30 步 IRLS；`precomputed` 把调用方分数当分数 |
| C5-M-01 P1 bootstrap 为 \([δ,δ]\) | **库函数关闭** | r05 反例宽度 \(0.653\)，与独立簇实现逐分位相同。CLI 在**正确** `p1_table`+`problem_id` 下会走该路径。标签回退再次退化，见 C7-M-02 |
| C2-M-03 `1-0.7≰0.3` | **关闭** | `q+1e-12` 保住该边 |
| C3-M-01 并集 \(\rho_S(T)\) | **关闭** | `event_sets` → `mean_over_events` |
| C2-M-05 监督/无标签同一 lstsq | **关闭（估计程序）** | 无标签：中心化 Procrustes/lstsq；监督：行加权未中心化 lstsq |
| C2-M-06 P2 `None` TypeError | **关闭** | `missing_pair`（`shared_denom=|shared_premises|` 时确认） |
| C3-M-03 共享分母 | **关闭 asked 项** | 无支持集 → `denominator_unverified` |
| C3-M-04 / C4-M-02 / C5-M-02 \(a(X)\) | **CLI 祖先齐全时关闭** | 两事件异真边现得 0.1。无 indices 的库默认仍 0.9；祖先缺失仍 0 |
| C3-M-05 P3 非目标 | **关闭（接口）** | `nontarget` / `vs_baseline` 存在。CLI intervene 对照结局仍为 None |
| C3-M-07 空袋+hits 伪造 0 | **关闭（未评估 API）** | 空 `noise_set` 且非 `noise_evaluated` → `noise_set_empty` |
| C4-M-01 0-hit → excess null | **关闭（集合 API）** | 已评估 0-hit → `noise=0`，`excess=1` |
| C4-M-03 Boundary BCE 符号 | **关闭** | 报告 \(+10.000045398900186\) |
| `cone_fit` 空壳 | **关闭** | grid 最小化 \(SS_{\mathrm{res}}\) |
| F6-05 / 作者“P1 禁止 \([δ,δ]\)” | **库函数独立确认** | 不采信 ISSUES；本轮重算。生产 analyze 回退除外 |

---

## 7. 发现

状态：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

### C7-M-01 — 有 sham hit 时 `event_density_sets` 丢掉 \(N\)，excess 变 null，而不是扣除 \(|N\setminus T|/|P\setminus T|\)

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `measure.event_density_sets` **289–302**；`dependency_densities` **124–141**。CLI `cmd_label` **558** 走该路径
- **原文：** §2.6 / §7 / PITFALLS-3：同题不同随机流的表观 \(\rho_S^{\mathrm{noise}}\) 必须先扣除；结论用 signed excess。有 hit 时 \(N\) 是命中前提集合，不是缺失协议
- **反例（独立手算，当前树）：**
  - \(P=\{p1,p2,p3\}\)，\(T=\{p1,p2\}\)，\(B=\{p3\}\)，\(N=\{p3\}\)
  - 论文：\(\rho_S=1\)，noise \(=1\)，excess \(=0\)
  - `dependency_densities(..., noise_set=['p3'], sham_protocol={...})`：**excess=0**（库函数本身会算）
  - `event_density_sets`：`noise_ref==1` ⇒ `hits` 非空 ⇒ `noise_set=None` ⇒ `null_reason=noise_set_missing`，**excess is None**
  - `test_sham_hits_do_not_book_evaluated_zero_noise` **锁住** null，不能关闭本条
- **影响：** 只在 0-hit 子集上才写出数值 excess（此时 excess=raw）。一旦 sham 真的打到噪声，论文最需要的“噪声解释了表观 \(\rho_S\)”（excess=0）被删成缺失。这是选择偏差，不是保守缺测
- **修复：** `hits` 非空时令 \(N=\{\)该事件 `noise_ref==1` 的 premise\(\}\)，再走集合扣除。禁止用“有 hit ⇒ 当作协议缺失”

### C7-M-02 — `cmd_analyze` 在无 `p1_table.jsonl` 时用前提级 task/behavior 标签冒充 P1，且可退化成 \([δ,δ]\)

- **严重度：** High
- **状态：** confirmed defect（流水线；`p1_incremental` 在正确表上估元正确）
- **符号：** `cli.cmd_analyze` **1022–1046**。仓库内没有任何命令写 `p1_table.jsonl`
- **原文：** §2.6 / C3-01 / PITFALLS-9：\(y=\) 逐题对错，\(\rho=\rho_S(T)\)（控制链长与 op），按基础题聚类 bootstrap
- **反例（复现当前 CLI 构造，当前树）：**
  - 6 行标签，`task_label`/`behavior_label` 混 0/1，全 `event_id="q"`（t1 形态）
  - 代码：`length≡1`，`op≡0`，`rho=behavior_label`，`y=task_label`，`problem_id=event_id`
  - 点估计 \(\delta=-0.5\)（这是“行为是否对齐任务边”，不是“\(\rho_S\) 是否预测答错”）
  - 唯一簇 `"q"`：bootstrap 200 次区间 **\([-0.5,-0.5]\)**，`status` 仍是 `resampled_delta_auc`
- **影响：** 默认 label→analyze 只要同时出现 task 0/1（sham 行的 `task_label=0` 即可满足），就会写出带区间的伪 P1，并标 `evaluated_descriptive`。库函数刚关掉的零宽度区间在这条回退上回来
- **修复：** 没有问题级 \(\rho_S\) 与对错表就保持 `p1=None` / `not_evaluated`。禁止用 `task_label`/`behavior_label` 填 P1

### C7-M-03 — 共同维 PCA 在 \(n<\min(d)\) 时不能对齐，却仍写 `truncated=False`

- **严重度：** Medium
- **状态：** confirmed defect（附录几何路径；直接迁移 N/A 本身正确）
- **符号：** `transfer._pca_project` **57–64**；`common_dim_then_procrustes` **67–75**
- **原文：** 附录 S3 / GEOM-01 / PITFALLS-6：先学共同维映射再 Procrustes；禁止静默截断/补零。首批模型 4096/3584
- **反例：**
  - \(A\in\mathbb{R}^{2\times5}\)，\(B\in\mathbb{R}^{2\times3}\)：`common_dim=3`，`a_map=pca`，`truncated=False`，`status=not_applicable_shape_mismatch`
  - 原因：`vt[:3]` 在 \(n=2\) 时只能给出 2 个成分，投影成 \((2,2)\)，与 \(B\) 的 \((2,3)\) 对不上
  - \(n=20,d=8/5\)：Procrustes 成功，`R.shape=(5,5)`
  - `eye(4)` vs `eye(3)`：样本数也不相等；`test_common_dim_is_not_silent_truncate` 只断言旗标，不要求对齐成功
- **影响：** 论文要点名的 4096→3584 共同维路径在现实 \(n\ll 3584\) 时不会给出 \(R\)，却带着 `truncated=False` 的成功语义。坐标截断检查本身是对的（\(\|ap-A_{:,:3}\|_\infty=1.45\)）
- **修复：** 共同维取 \(\min(d_A,d_B,n-1,n_{\mathrm{rank}})\)；\(n\) 必须成对相等；对齐失败时不要暗示映射已完成

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C7-U-01 | Medium | 监督适配用 \(\sqrt{\|y-\bar y\|+0.1}\)；`[0,1]` 与 `[1,0]` 的 \(W\) 相同 | `transfer.py` 25–28 | 估计程序已与 unlabeled 分列。非翻转标签会改 \(W\)（差 0.424） |
| C7-U-02 | Low | 只传 `rng`、不传 `groups` 时 bootstrap 的是 \(\rho\) 均值 | `analysis.py` 87–88 | CLI analyze 传了 `groups`。该分支不是生产默认 |
| C7-U-03 | Low | P2 不在支持集上重算 \(\rho\)；`0.9` 对分母 4 仍 `ok` | `analysis.py` 160–169 | 支持集存在性已关 asked 项。\(0.9\notin\{0,1/4,1/2,3/4,1\}\) |
| C7-U-04 | Low | `event_sets` 对 None 密度跳过再平均：`[None, 1]` → `1.0` | `measure.py` 109–111 | 分母为空记 N/A 后，\(n\) 是否含 N/A 步原文未写死 |
| C7-U-05 | Low | `excess==0` 自动 `c3_negative_descriptive`+跳过 P2/P3 | `analysis.py` 244–256 | 论文写过“扣除后不显著则转负结果”。未注册检验下用点估计 0 分流偏早。Gate 默认仍 `unregistered` |
| C7-U-06 | Low | `sequence_score` 无 `truth_indices` 仍对全列取 max | `calibrate.py` 20–25 | CLI 现传 indices。测试仍锁住无 indices → 0.9 |
| C7-U-07 | Low | 校准在 `ancestors` 缺失时 \(a=0\)；只拟合/校准第一头 | `cli.py` 705–772 | 祖先齐全的 C5-M-02 反例已对。行为头未单独出 \(q_\alpha\) |
| C7-U-08 | Low | `rsi` 含 `{nid}`；`event_id is None` 匹配所有事件 | `cli.py` 761–764 | 有祖先过滤后，行为正例若不在 \(R_{\mathrm{task}}\) 不会进列。nid 本身通常不是 E 列 |
| C7-U-09 | Low | CLI intervene 的 C-rand/C-layer **结局**为 None，只匹配了几何范数 | `cli.py` 878–882 | 库 `p3_recovery` 正确。真实对照 decode 属 pending_server |
| C7-U-10 | Low | analyze 的 `probe_prf1` 把展平 \(\hat P\) 前 \(k\) 个格子对标签行 | `cli.py` 1093–1097 | 附录字段；不是 P1 估元 |
| C7-U-11 | Low | `rho_M` 在 0-hit 时 noise=1，excess\(_M\le0\) | `measure.py` 139–141 | 论文未写出与 \(\rho_S\) 对称的 \(M\) 噪声公式。本轮清单要的是 S |
| C7-U-12 | Low | INLP 用 lstsq(\(\pm1\)) 不是 SVM | `interventions.py` 52–67 | 迭代投影本身已对 |
| C7-U-13 | Low | `ie_z` 不是 \(\mathbb E[g\mid do]\)，只是样本均值差 | `interventions.py` 88–89 | 在已提供的 \(g\) 上这是样本模拟。因果识别靠干预协议 |
| C7-U-14 | Low | `cmd_analyze` 恒写 `direct_transfer(4096,3584)`，不读本跑维度 | `cli.py` 1019 | 库函数对该维对是 N/A。真实同维模型会被这篇报告写成 N/A |
| C7-U-15 | Low | `cmd_fit` 的 BoundaryMLP 用全 1 标签 | `cli.py` 648–650 | 注记 `no_negatives`。库 BCE 符号已对 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C7-S-01 | 真实轨迹命题 2 覆盖 | 无论文权重；祖先缺失时 \(a=0\) |
| C7-S-02 | 4096↔3584 适配后的双线性 | 直接迁移 N/A 已对；共同维 PCA 在现实 \(n\) 下未通（C7-M-03） |
| C7-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册；真实轨迹未跑。即便有 `p1_table`，label→analyze 回退仍会污染 |
| C7-S-04 | 前瞻交换相对 C-rand/C-layer 的来源跟随差 | CLI 对照结局为 None；tiny 不是 MODEL-01 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`；`fit` 在 \(y\in\{0,1\}\) 上的梯度（有限差 \(1.42\times10^{-9}\)）
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64
3. 未知哨兵与 NaN/Inf **行**不进 BCE/梯度；空 \(\mathcal K\) 为 NaN / `no_known_labels`
4. Conformal \(k\) 公式、**\(k>N\Rightarrow+\infty\)**、\(\alpha\notin[0,1)\) 拒绝；\(\alpha=0\Rightarrow+\infty\)
5. `predict_set([0.7], 0.3)` 为 True（`1e-12` slack）
6. `sequence_score(..., truth_indices=[0], nonconformity="one_minus_p")` 得 \(0.1\)；空真集得 \(0\)
7. **`direct_transfer(4096,3584)` N/A**；`apply_map` 维不匹配无法乘
8. `labeled=True` 无张量即失败；无标签适配 ≠ 监督加权 lstsq
9. `_auc` Mann–Whitney，平局 1/2
10. 默认 P1 拒绝无留出；留出 IRLS 不吃 eval 行的 \(X\)；能检出被 op 淹没的 \(\rho=y\)
11. **P1 问题级 bootstrap（库函数）：** 重采样簇并重算 \(\Delta\mathrm{AUC}\)，r05 反例宽度 0.653，不是 \([δ,δ]\)
12. P2：无支持集 → `denominator_unverified`；缺测 → `missing_pair`；分母与列表不一致 → `denominator_inconsistent`
13. P3 接口：`vs_crand`/`vs_clayer`/`vs_baseline`/`nontarget`；`causal_reverse_claim is False`
14. **空分母 → `rho_S` null**；**signed excess −0.5 不截断**
15. 已评估 0-hit → `noise=0`、`excess=1`。空列表且未评估仍 null
16. INLP 在已投影 \(H\) 上迭代；交换 \(H+\Pi_Z(H_d-H_b)\)
17. C-rand / C-layer 匹配传入的主干预范数；缺范数即失败
18. Boundary 报告 BCE \(+10.000045\)；Hidden=256
19. `cone_fit` 对 \((\lambda,\gamma)\) 做 grid，措辞 `descriptive_only`
20. Week-8 默认三门 `unregistered`，`scientific_conclusion is None`，**不发明 Gate 通过线**
21. repair 零分母 → null；`consecutive_repairs` \(k=1..5\)
22. PCA 不是前 \(k\) 列截断（在 \(n\) 足够时 Procrustes 可完成）

---

## 11. 测试质量（仅公式）

指定四文件 **38 passed** **不能**证明本通道估计量正确。

- `test_conformal_examples` **有效**（\(k>N\Rightarrow+\infty\) 的 \(\alpha=0.1\) 例）
- `test_direct_transfer_rejects_4096_3584` **有效**
- `test_signed_excess_not_clipped` / `test_zero_denominator_null` **有效**
- `test_p1_bootstrap_resamples_delta_auc` **半有效**：有 `resampled_delta_auc`，**允许** `lo<=hi` 的 \([δ,δ]\)
- `test_p1_bootstrap_interval_is_not_degenerate` **对库函数有效**（`lo<hi`）；不覆盖 analyze 标签回退
- `test_sham_hits_do_not_book_evaluated_zero_noise` **锁错公式**：要求 hit ⇒ null，与 §2.6 扣除相反；夹具还是 t1（\(P=T\)，\(\rho_S\) 分母本就空）
- `test_common_dim_is_not_silent_truncate` **无效（对齐）**：`eye(4)` vs `eye(3)` 样本数不同；只断言 `truncated is False`
- `test_analyze_uses_labels_or_stays_null` **无效（P1）**：只查 `scientific_conclusion is None` 与 Gate `unregistered`，不查 `p1 is None` 或估元
- `test_sequence_score_uses_true_edges_only`（r06）锁住 E 列顺序，**同时**仍依赖传入的 `truth_indices`
- `test_cone_fit_returns_r2` 只断言 `r2>0.9`，不回收真 \((\lambda,\gamma)\)
- 无 CLI 标签回退 P1 oracle，无 “hit ⇒ excess=raw−noise” oracle，无 \(n<d\) PCA 形状 oracle

---

## 12. 结论

声明冻结 `9814019a…` **HASH_MISMATCH**。审查开始时同一脚本曾 MATCH；其后汇总先后为 `1b88bec2…` 与 `129d5405…`（均为 60 文件）。本通道未改生产字节。公式文件除 `cli.py` 外绑定手检 digest；`cli.py` 绑定最后一读 `de004c9d…`（C7-M-02 逻辑未变）。指定 pytest **38 passed**（本审查重跑）。作者 143 **未**复跑、**不**采信。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | 通过 |
| 未知 / NaN 行掩码；空 \(\mathcal K\) 为 NaN | 通过 |
| conformal \(k\)；**\(k>N\Rightarrow+\infty\)** | 通过 |
| P1 留出 logistic | **通过（点估计，库函数）** |
| P1 簇重采样并重算 \(\Delta\mathrm{AUC}\)，区间不是 \([δ,δ]\) | **库函数通过**（宽度 0.653）。**CLI 标签回退失败**（C7-M-02） |
| P2 配对 + 支持集 | **asked 项通过** |
| P3 vs 对照 | **通过（接口）** |
| 空分母 → null；signed excess 不截断 | 通过 |
| 0-hit 已评估 → noise=0 | 通过 |
| 有 hit 时扣除 \(N\) | **失败**（C7-M-01） |
| `direct_transfer(4096,3584)` N/A | 通过 |
| PCA 后 Procrustes，`truncated=False` | **\(n\) 足够时通过**；**\(n<\min d\) 失败**（C7-M-03） |
| 交换 / INLP / C-rand 范数 | 通过 |
| Week-8 无发明门 | **默认通过** |

**可关闭（独立确认，非采信 ISSUES）：** C-01…C-04、C2-M-01（含 NaN 行）、C2-M-02、C3-M-02（点估计）、C2-M-03、C3-M-01、C2-M-05、C2-M-06、C3-M-03（asked）、C3-M-05（接口）、C3-M-07（未评估 API）、C4-M-01、C4-M-03、**C5-M-01（库函数）**、**C5-M-02（祖先齐全的 CLI）**、`cone_fit` 空壳。

仍会污染论文数字的 confirmed defects：**C7-M-01**（hit ⇒ excess null，论文应为 0）；**C7-M-02**（analyze 用 task/behavior 冒充 P1，区间可再变 \([δ,δ]\)）；**C7-M-03**（4096/3584 共同维在 \(n<d\) 时对齐失败却写 `truncated=False`）。

**验收意见：** `FAIL_MATH_STATS`。不得为声明冻结 `9814019a…` 签通过。在 C7-M-01/C7-M-02 关闭并经独立复审前，不得把 `event_density_sets` 的 excess 或 CLI analyze 的 `p1.bootstrap.interval` 写成论文 P1/噪声扣除。Gate 0–2 继续未注册，本通道未发明阈值。

---

## 附录：60 文件 SHA-256（POSIX relpath，仅 file bytes；手检树 `1b88bec2…`，`cli.py` 已更新为最后一读）

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc
src/reasoning_diff/cli.py  de004c9dac18c3aef0fb90db3f854d387708d3e5db6903ff6a71ff4e51f10946
src/reasoning_diff/edits.py  bfd1632b50504c042640bcda85368b0c695fd3f843ea885200d080055aa107b6
src/reasoning_diff/events.py  fc5031a51e99a4b511450d03ded6dd5f205175eb263bf4cbaf8695ee47746e17
src/reasoning_diff/executor.py  481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  1fa2360e680d37ad086c9a81b3ec684c9d9d1e73affb0d906ff5a97231986df2
src/reasoning_diff/models/__init__.py  0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8
src/reasoning_diff/models/adapters.py  c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a
src/reasoning_diff/models/collect.py  2772257e0643b3c7ebce94eec039d82bcdcbff4fde9c8136dbcb602eaba8dd17
src/reasoning_diff/models/features.py  0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0
src/reasoning_diff/models/generate.py  07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844
src/reasoning_diff/models/tiny.py  21725a183452bd06593789217745202863269cd7e9dea1ec144e4bbdb0a1ddb0
src/reasoning_diff/models/tokenize.py  b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332
src/reasoning_diff/probes/__init__.py  3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5
src/reasoning_diff/probes/bilinear.py  b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9
src/reasoning_diff/probes/boundary.py  ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034
src/reasoning_diff/probes/calibrate.py  e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334
src/reasoning_diff/repair.py  d547ab99e3179093348b84c0a65b48ee84d1eee9ff4a72703dd70c01fc7a113c
src/reasoning_diff/rng.py  2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908
src/reasoning_diff/schema.py  57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7
src/reasoning_diff/scoring.py  8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99
src/reasoning_diff/splits.py  35cd0e3f724ee850b4cf28a118717d51d188ae913a2917562fc29110ccd7cbdc
src/reasoning_diff/tasks/__init__.py  4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754
src/reasoning_diff/tasks/catalog.py  bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5
src/reasoning_diff/tasks/t1_config.py  e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94
src/reasoning_diff/tasks/t1_fixture.py  01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41
src/reasoning_diff/tasks/t1_official.py  5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b
src/reasoning_diff/tasks/t2_gsm_plus.py  8e58c5d22b41b87b5f422fdbba10488eb42ad4af607610f8d674c4c094b7772e
src/reasoning_diff/tasks/t2_gsm_symbolic.py  b50db6533f18948d141a75a38970b491269a127b990bd818408f29a8e28219af
src/reasoning_diff/tasks/t2_noop.py  850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed
src/reasoning_diff/tasks/t3_hotpot.py  f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe
src/reasoning_diff/tasks/t3_humaneval.py  f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1
src/reasoning_diff/tasks/t3_musique.py  b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895
src/reasoning_diff/tasks/t4_boundary.py  e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2
src/reasoning_diff/transfer.py  d31bcd499a51ca94c28dca6c97cdbd5c5e3f05db996d15934e5b7d0b5bb22407
tests/conftest.py  1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1
tests/test_artifacts.py  830953f379954233c76c9aab9f5f4b3860ea598579015a58bddd9909c5bd3278
tests/test_cli_pipeline.py  ff826b3e553f003bf134d1ef9d6c06206a7b836e15c69cd1126bc1ae6d482123
tests/test_generate_loop.py  ffe10b0d6812908ca34f446103b22a23c2e857a85172cc78e72caf005a979a46
tests/test_measure.py  fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab
tests/test_review_regressions.py  d3814498fe52b28b7905dc2c07e86e8e893b285081e4c37724a67c0f61b164ee
tests/test_round03_regressions.py  5698a410c0669b6142f31d5b302ff8c7ef8ec66cc9ef429786d45e2418bfc278
tests/test_round04_regressions.py  25949c80bbb555851beeaa193e39e3e221759af4c986df8a05d3bdb8e7702666
tests/test_round05_regressions.py  bc837c0c3a6ea3ae440d6c939c210674070ca7bf80ee6c3cb2644d7b04c515a2
tests/test_round06_regressions.py  a4421f11d41e174369374ea26746e387e860d35edce9f380b077cab7e69ae0a4
tests/test_science.py  cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```
