# C：数学与统计独立审查（round-01）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立推导双线性探针、加权 BCE、split conformal、迁移映射、P1–P3、区间、预算、Repairability/RR；专查 off-by-one、零分母、未截断负 excess、泄漏
- 审查时间：2026-09-21
- 审查者上下文：新独立 subagent，未读取 A/B/D/E/F 或其他 round-01 审查报告
- 声明冻结哈希：`532e05a8038e9862f219ab36927f7f7c0df59ef639045821a2cc801960b2b0c0`（`.planning/audits/round-01/VERSION.md`）
- 本审查是否复现该汇总哈希：**否**。对 `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml` 尝试了字节拼接、posix `sha256sum` 列表、`io.digest(path→file_digest)` 等聚合，均得不到声明值。审查对象是**当前磁盘字节**；下列逐文件 SHA256 是可复核锚点
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏：`src/reasoning_diff/`、`tests/`、`pyproject.toml` 均为未跟踪）
- 生产代码：本审查只读，未修改
- 原文：`Reasoning-Diff-修订方案-v3 (1).md`（独立按公式推导后再对源码）
- numpy：1.26.4

---

## 1. 范围与逐文件覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 覆盖深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/__init__.py` | 1–3 | `3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5` | 再导出 | 全文 |
| `src/reasoning_diff/probes/bilinear.py` | 1–45 | `bf711813236c1f9f3b89ba2728cc5a57930cb58cb025bd494d7c307b48a42a32` | `BilinearProbe.score/predict_matrix`、`weighted_bce`、`_sigmoid` | 全文；独立数值核对 |
| `src/reasoning_diff/probes/boundary.py` | 1–23 | `a45ec29f20fc3b3c5f421c6b93bc66e909030e1d8854194137c3c0167a490347` | `BoundaryMLP` | 全文（结构，非本通道主公式） |
| `src/reasoning_diff/probes/calibrate.py` | 1–33 | `1f0e2c29944197984eb833ba723f8bd04a4363ea84555c11cb71bf3d26a335f0` | `sequence_score`、`conformal_threshold`、`predict_set` | 全文；手算 k 与反例 |
| `src/reasoning_diff/transfer.py` | 1–36 | `7a6a5fa00606985bf029004110ee70c9035451d52d67f040526237d2883160fe` | `direct_transfer`、`fit_linear_map`、`apply_map` | 全文；已知 W 回收 |
| `src/reasoning_diff/analysis.py` | 1–108 | `7346e1247d7257bbd5efe32b51eff23f764307c00d713ab51ec3f2b3e610d944` | `_auc`、`p1_incremental`、`p2_paired`、`p3_recovery`、`week8_decision`、`bootstrap_cluster`、`procrustes`、`cone_fit` | 全文；AUC/P1 反例 |
| `src/reasoning_diff/measure.py` | 1–217 | `f56d7fae9cb1e495de5a332f546ff8b50ea090dbfbbed386ac993a89bb1e351f` | `dependency_densities`、`_matrix_densities`、`lcs_overlap`、`preservation_to_csp` | 全文；集合/矩阵两条路径 |
| `src/reasoning_diff/interventions.py` | 1–73 | `c9d78ed7fad53b76db97c38fd32a63a5d7bf51edc1dcaf581cc68ea1bd2cd16c` | `project_delta`、`apply_swap`、`c_rand_delta`、`inlp_remove`、`rescue`、`intervention_report` | 全文；INLP 迭代与范数匹配 |
| `src/reasoning_diff/repair.py` | 1–57 | `54559ea4f50eda9a9902c2b8594d9dd843a71aae2f67d8e8b80d8e96d0fea043` | `repairability`、`recompute_ratio`、`run_repair` | 全文 |
| `tests/test_science.py` | 1–97 | `3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c` | 校准/迁移/P1 单类/P3 禁句 等 | 全文（查测试是否独立、是否漏反例） |

调用链只读（不计入本通道“已证明正确”）：`cli.py` 的 `cmd_fit` / `cmd_calibrate` / `cmd_analyze` / `cmd_repair`；`splits.require_split`；`schema.finite_or_none`；`graphs.dirty_cone`。

未覆盖（明确排除）：模型 hook/KV、数据适配器内部、executor 沙箱。这些不是本通道公式对象。

---

## 2. 独立推导（先公式，后对代码）

### 2.1 双线性探针

原文 §4.2：

\[\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b),\quad U\in\mathbb R^{d_h\times r},\;V\in\mathbb R^{d_e\times r},\;r=64.\]

低秩因式：\(h^\top U V^\top e=\langle hU,\,eV\rangle\)。矩阵形式：\((HU)(EV)^\top\)。

**结论：** `score`（`bilinear.py` 21–26）与 `predict_matrix`（28–29）与上式一致。独立随机 \(h,e,U,V\) 最大绝对误差为 0。默认 `rank=64`、`fn_weight=10` 与原文 \(\lambda_{\mathrm{FN}}=10\) 一致。`BoundaryMLP` Hidden=256 + ReLU（`boundary.py` 8–19）结构正确。

**缺口：** 类内无拟合/更新；`U,V` 仅 `default_rng(0)` 正态初始化（11–14）。加权 BCE 不回写参数。`head_type="unspecified"`（19），任务头/行为头不是两个已训练对象。

### 2.2 加权 BCE

对 \(y\in\{0,1\}\)：

\[\ell=\frac1{|\mathcal K|}\sum_{i\in\mathcal K} w_i\bigl[-y_i\log p_i-(1-y_i)\log(1-p_i)\bigr],\quad w_i=\lambda_{\mathrm{FN}}\mathbf 1[y_i=1]+1\cdot\mathbf 1[y_i=0].\]

`weighted_bce`（37–45）在 \(y\in\{0,1\}\) 且 mask 正确时与该式一致（独立例：1.1301337284593955）。未知标签应排除出 \(\mathcal K\)。空 \(\mathcal K\) 应是无效损失，不应是 0。

### 2.3 Split conformal（命题 2）

\[a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij})\]

空真集 \(a=0\)。校准分数 \(s_{(1)}\le\cdots\le s_{(N)}\)，\(k=\lceil(N+1)(1-\alpha)\rceil\)。若 \(1\le k\le N\)，\(q=s_{(k)}\)；若 \(k>N\)，\(q=+\infty\)。预测集 \(\hat R=\{p_j:1-\hat p_{ij}\le q\}\)。\(k<1\)（\(\alpha\ge 1\)）在 1-index 下没有第 0 个顺序统计量；Python `arr[k-1]` 会回绕到末尾。

手算与代码一致的例子：\(N=4\)，分数 \([0.1,0.2,0.3,0.4]\)，\(\alpha=0.4\Rightarrow k=3,\,q=0.3\)；\(\alpha=0.1\Rightarrow k=5>4,\,q=+\infty\)；\(N=1,\alpha=0.05\Rightarrow q=+\infty\)。

### 2.4 迁移

直接迁移：仅当源/目标特征维相等才适用；4096≠3584 必须 N/A，禁止截断/补零。

无标签配对：在 `transfer_pairs` 上解 \(X_B W\approx X_A\)（目标坐标 → 源坐标），\(W\in\mathbb R^{d_B\times d_A}\)。监督适配必须是**不同估计程序**或至少使用标签，不能只改状态字符串。双线性有 \(h\) 与 \(e\) 两个输入，映射必须成对。

正交 Procrustes：\(A^\top B=USV^\top\Rightarrow R=UV^\top\) 最小化 \(\|AR-B\|_F\)（形状相同）。`np.linalg.svd` 返回 \(V^H\)，故 `ua @ va` 正确。

### 2.5 \(\rho_S,\rho_M\) 与有符号 excess

\[
S=R_{\mathrm{behavior}}\setminus R_{\mathrm{task}},\quad
\rho_S(s_i)=\frac{|S(s_i)|}{|P\setminus R_{\mathrm{task}}(s_i)|},\quad
\rho_S(T)=\frac1n\sum_i\rho_S(s_i).
\]

分母空 → N/A。噪声参照是**同公式**在 sham/另一随机流上的 \(\rho\)，不是把缺失噪声当成 0。excess \(=\rho^{\mathrm{raw}}-\rho^{\mathrm{noise}}\)，允许为负，禁止截成 0。集合并集上的 \(\rho\) **不等于**逐步平均：两步 \(\rho\in\{1/2,0\}\) 的并集可得到 0 而非 \(1/4\)。

### 2.6 P1–P3 与区间

- **P1：** 在 `probe_train` 拟合 logistic：\(\mathrm{logit}=\beta_0+\beta_L\mathrm{len}+\beta_o\mathrm{op}\) 对 \(\beta_0+\beta_L\mathrm{len}+\beta_o\mathrm{op}+\beta_\rho\rho_S^{\mathrm{excess}}\)；在**留出基础题**比较 AUC 与 \(\Delta\)AUC；偏相关单独报；区间用基础题聚类 bootstrap。正类须预先固定（出错 vs 正确）。AUC 在平局时必须是 Mann–Whitney（常数分数 → 0.5，与标签排列无关）。
- **P2：** 同基础题配对 \(\Delta\rho_S=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\)，\(\Delta\mathrm{acc}=\mathrm{acc}_{\mathrm{noop}}-\mathrm{acc}_{\mathrm{base}}\)；再报二者相关与污染步位置；新前提改分母，共同支持与注入列分开；缺配对/非法 no-op 不得 silently inner-join。
- **P3：** 相对基线的 \(\Delta\mathrm{acc}\)，以及相对 C-rand / C-layer 的差值；同时报非目标响应与无效输出率；分母变化要可见。P3 未检出不得写“只是后果”。
- **区间：** 重采样基础题，题内全部 seed/变体跟随；点估计与区间的 estimand 必须声明是轨迹微平均还是先题内再平均。

### 2.7 交换、INLP、预算、RR

\[
H'=H^{\mathrm{base}}+\Pi_Z(H^{\mathrm{donor}}-H^{\mathrm{base}}).
\]

列正交时 \(\Pi_Z=QQ^\top\)。C-rand 必须匹配**该样本主干预实际** \(\|\Delta\|\)，不是另一个固定种子子空间的范数。

INLP：每步在**已投影**表示上重拟合方向，再累乘 \(I-uu^\top\)。若始终对原始 \(H\) 做 `lstsq`，则 \(u\) 不变，第 2 步起 \(Pu=0\)。

\[
\mathrm{Repairability}=1-\frac{\text{修复解码 token}}{\text{全量重推解码 token}},\quad
\mathrm{RR}=|\hat D|/n.
\]

分母 0 → N/A。预算是重算槽位对应的**原始 token 数**，不是生成串字符数；实际解码长度另计。

---

## 3. 已执行检查与结果

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | 双线性 \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（误差 0） |
| CHK-02 | \(\lambda_{\mathrm{FN}}=10\) 的 \(y\in\{0,1\}\) BCE | 手算加权均值 vs `weighted_bce` | **通过**（该子集） |
| CHK-03 | 空 mask / \(y=-1\) | 直接调用 | **失败**：空 → 0.0；\(y=-1\) 进入有限项且单项可为负（见 C-M-08） |
| CHK-04 | \(k=\lceil(N+1)(1-\alpha)\rceil\)，规定例 | 手算 vs `conformal_threshold` | **通过**（\(\alpha=0.4/0.1\)；\(N=1,\alpha=0.05/0.5\)） |
| CHK-05 | \(k<1\) / \(\alpha>1\) | \(\alpha=1\Rightarrow k=0\)；\(\alpha=1.5\Rightarrow k=-2\) | **失败**（负索引回绕，C-M-01） |
| CHK-06 | \(1-p\le q\) 含相等 | `predict_set([0.7], 0.3)`；`[0.5],0.5` | **部分失败**：0.5 通过；`1-0.7=0.3000…04 ≰ 0.3`（C-M-02） |
| CHK-07 | \(q=+\infty\) 全选；未知/空真集分数 | `predict_set` / `sequence_score` | **通过**（inf；unknown→None；empty_truth→0） |
| CHK-08 | 直接迁移 4096≠3584 | `direct_transfer` | **通过** |
| CHK-09 | \(X_B W=X_A\) 回收 | 已知 \(W\) 合成配对 | **通过**（\(\sim 10^{-14}\)） |
| CHK-10 | `labeled=True` 是否改变估计 | 同一 `lstsq` | **失败**（只改 status 字符串，C-M-10） |
| CHK-11 | 常数分数 AUC=0.5 | `_auc(ones, y)` 三种排列 | **失败**：1.0 / 0.0 / 0.75（C-M-04） |
| CHK-12 | P1 是否 logistic / 留出 / 偏相关 | 读 `p1_incremental`；`len+0.01*op+rho` 例 | **失败**（C-M-03） |
| CHK-13 | 集合路径负 excess、零分母 | 手算 \(\rho_S=0,\rho_{\mathrm{noise}}=0.5\)；全祖先袋 | **通过**（该路径：excess=-0.5；denom_S=None） |
| CHK-14 | 并集 \(\rho\) vs \((1/n)\sum\rho(s_i)\) | 两步手算 0.25 vs 并集 0 | **失败**（C-M-06） |
| CHK-15 | 矩阵路径 `noise=None` | `_matrix_densities` | **失败**：S excess 伪造成 raw；M excess=-1.0（C-M-05） |
| CHK-16 | INLP `steps=8` vs `steps=1` | 同 \(H,y\) | **失败**：差 \(\sim 10^{-16}\)；\(I-P\) 秩=1（C-M-07） |
| CHK-17 | C-rand 范数是否对主干预 | 主基 seed=123 vs `c_rand_delta` | **失败**：主范数 2.654 vs 对照 0.662=seed(1)（C-M-13） |
| CHK-18 | 交换公式 | 手算 \(\,e_1+\Pi_{e_2}(e_2-e_1)=e_1+e_2\) | **通过**（与 `test_swap_formula` 一致） |
| CHK-19 | Repairability / RR 零分母 | `repairability(1,0)`、`recompute_ratio(0,0)` | **通过**（公式函数） |
| CHK-20 | `run_repair` 是否供给真实解码/token 预算 | 调用 `new_prefix="abcd"` | **失败**：`generated_tokens=0`；`extra_prefill_tokens=4`（字符）（C-M-09） |
| CHK-21 | P2 `None` rho | `p2_paired(None, …)` | **失败**：TypeError（C-M-11） |
| CHK-22 | Week-8 未注册；P3 禁句 | `week8_decision` / `p3_recovery` | **通过**（threshold=null→unregistered；`causal_reverse_claim` 恒 False） |
| CHK-23 | 聚类 bootstrap 空组 | `bootstrap_cluster([],[])` | **通过**（mean/interval=None） |
| CHK-24 | `pytest` | `python -m pytest tests/test_science.py tests/test_measure.py tests/test_tracer_t1_prepare.py -q` | **22 passed，exit 0**。现有测试不覆盖 CHK-05/06/11/12/14/15/16/17/20 |

---

## 4. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 复现声明冻结汇总哈希 | 多种常见聚合均不匹配 `532e05a8…`；已改用逐文件 SHA256 |
| 全仓库 pytest | 本通道只跑公式相关测试；其余属 E |
| 真实模型轨迹上的 \(a(X)\)、logistic P1、配对迁移 | 无真实权重/数据；CLI 校准/分析为硬编码夹具（`cli.py` 154–158、188–196） |
| 阅读其他审查报告 | 任务禁止 |
| 前瞻 token 越界（除 `test_science` 已断言的 `select_prefix_index`） | 通道 D |

---

## 5. 发现

状态取值：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

### C-M-01 — conformal `k<1` 负索引回绕（off-by-one）

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `conformal_threshold` — `src/reasoning_diff/probes/calibrate.py` **24–27**
- **触发：** \(\alpha\ge 1\)（或使 \(k=\lceil(N+1)(1-\alpha)\rceil\le 0\) 的非法 \(\alpha\)）。\(\alpha=1\Rightarrow k=0\)，`arr[k-1]=arr[-1]`=最大分数，status 仍为 `finite`
- **原文：** §2.5 命题 2（约 135–136 行）；PROP2-01；PITFALLS 校准条
- **证据：** 分数 `[0.1,0.2,0.3,0.4]`，\(\alpha=1\) → `{'q': 0.4, 'k': 0}`；\(\alpha=1.5\) → `k=-2, q=0.2`。正确：\(k<1\) 应拒绝或 \(q=-\infty\)（空预测集），绝不是最大顺序统计量
- **影响：** 要 0% 覆盖时反而得到最宽阈值，覆盖方向与 \(\alpha\) 相反
- **修复：** 校验 \(\alpha\in(0,1)\)；`k < 1` 与 `k > n` 分开；禁止负下标

### C-M-02 — `1-p<=q` 在“看起来相等”的十进制上失败

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `predict_set` — `calibrate.py` **30–33**
- **触发：** `p_hat=0.7`、`q=0.3`（IEEE：`1.0-0.7=0.30000000000000004 ≰ 0.3`）。`0.5` 这类二进制精确值可通过
- **原文：** \(\hat R=\{p_j:1-\hat p\le q\}\)；协议要求“等于 q 的边被保留”
- **证据：** `predict_set(np.array([0.7]), 0.3) → [False]`
- **影响：** 真边落在阈值上被丢弃，有限样本覆盖可被破坏。CLI 校准字面量正是 0.1/0.2/0.3/0.4
- **修复：** 在同一浮点通道里比较已算好的 `1-p`；或带 ulp 容差；不要对字面量 `q` 重算 `1-p`

### C-M-03 — P1 不是留出 logistic，也不是偏相关

- **严重度：** Critical
- **状态：** confirmed defect
- **符号：** `p1_incremental` — `analysis.py` **31–37**（调用 `_auc` 19–28）
- **触发：** 任何 P1 调用。分数为 `length + 0.01*op` 与 `length + 0.01*op + rho`，系数写死，无拟合、无 split、无 excess 约束、无 bootstrap
- **原文：** §2.6 表 P1（164）；§7（321）；C3-01；协议 §5
- **证据：** 代码无 logistic。例：`len=[10,10], op=[1,100], rho=[0.9,0.1], y=[1,0]` → base/full AUC 均为 0（op 项淹没 \(\rho\)）。若拟合 \(\beta_\rho\)，\(\rho\) 可被放大
- **影响：** 报出的 AUC/ΔAUC 不是“控制链长与 op 后的增量预测力”；可正可负，与假设无关
- **修复：** train 上拟合两个 logistic，test 基础题上比概率 AUC；另报偏相关；`bootstrap_cluster` 挂在题级；强制 \(\rho_S^{\mathrm{excess}}\) 与正类定义

### C-M-04 — `_auc` 平局随标签排列变化

- **严重度：** Critical
- **状态：** confirmed defect
- **符号：** `_auc` — `analysis.py` **19–28**
- **触发：** 分数常数或有平局（\(\rho_S\)、链长均为粗离散量，平局是常态）
- **原文：** 同上；Wilcoxon–Mann–Whitney AUC 在平局时贡献 1/2
- **证据（独立于被测函数的期望）：** `scores≡1` 时，`y=[1,1,0,0]→1.0`，`[0,0,1,1]→0.0`，`[1,0,1,0]→0.75`。正确值均为 0.5
- **影响：** P1 可仅因题序得到任意 AUC；`np.trapz` 沿 `argsort` 路径积分，不处理平局
- **修复：** 实现 \(P(s_+>s_-)+0.5P(s_+=s_-)\)，或调用独立实现的 `roc_auc_score`

### C-M-05 — 矩阵密度在缺失噪声时当成全 0（伪造 excess）

- **严重度：** Critical
- **状态：** confirmed defect
- **符号：** `_matrix_densities` — `measure.py` **116–130**（由 76–77 行转入）。对比集合路径 **87–92**（缺失 sham → excess=None）
- **触发：** `dependency_densities(task=..., behavior=..., noise=None)`
- **原文：** §2.6 / §3：无噪声协议则 corrected 为 N/A；负差不截断，但也不得伪造参照
- **证据：** `task=[[0,0,1]], behavior=[[1,0,1]], noise=None` → S `{raw:0.5, noise:0.0, excess:0.5}`；M `{raw:0.0, noise:1.0, excess:-1.0}`
- **影响：** M 的 -1 excess 看起来像“未截断负差”，实际是把缺失参照当成“sham 从未命中”。C3 会把“没测噪声”写成“扣除后仍有信号 / 大负 M”
- **修复：** 与集合路径对齐：无 sham/noise → `noise/excess=None` 并写 `null_reason`。不要 `np.zeros_like`

### C-M-06 — 集合 API 不是 \(\rho_S(T)=\frac1n\sum\rho_S(s_i)\)

- **严重度：** High
- **状态：** confirmed defect（定义错用风险；矩阵路径按行平均更接近原文）
- **符号：** `dependency_densities` 集合分支 — `measure.py` **78–86、140–143**。CLI `cmd_prepare`（`cli.py` 92–97）对**一个** ancestor 袋调用一次
- **触发：** 多步轨迹把并集 \(T,B\) 一次性传入
- **原文：** §2.6（154–156）
- **证据：** 步1 \(\rho=1/2\)、步2 \(\rho=0\)，平均 0.25；并集 \(T=\{1,2\}=B\) → `rho_S_raw=0`
- **影响：** 轨迹级虚假依赖密度可被系统性压低或抬高
- **修复：** 逐步算 \(\rho_S(s_i)\) 再平均；N/A 步单独计数；不要把并集差当 \(\rho_S(T)\)

### C-M-07 — INLP 不更新 \(H\)，`steps>1` 无效

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `inlp_remove` — `interventions.py` **39–51**
- **触发：** 默认 `steps=8`
- **原文：** §6 Knock-out / INLP-01：迭代构造子空间并正交移除
- **证据：** `steps=1` 与 `steps=8` 的 \(P\) 最大差 \(\sim 5.6\times10^{-17}\)；`rank(I-P)=1`。`lstsq` 始终对原始 `H`（45），故 \(u\) 不变；一步之后 \(Pu=0\)
- **影响：** P3/Knock-out 只删一个线性方向，与声明的 8 步 INLP 不符；功效被低估或机制被误读
- **修复：** 每步 `H ← H @ P`（或等价）再重拟合；记录有效秩

### C-M-08 — 加权 BCE：空批次为 0；未知哨兵不屏蔽

- **严重度：** High
- **状态：** confirmed defect（函数行为）。调用方是否传入 `-1`：**未证实疑点**（矩阵标签用 -1，见 `measure.py` 120；`Label` 用 None）
- **符号：** `weighted_bce` — `bilinear.py` **37–45**。文档第 1 行称 unknown 已掩码
- **触发：** `mask` 全假；或 `target=-1` 且 `mask=1`（`-1` 有限，`y>0.5` 为假）
- **原文：** PROBE-01；§4.2 未知不进入损失
- **证据：** 空 mask → `0.0`；`pred=[0.2,0.8], target=[-1,1], mask=[1,1]` → 0.534，其中 \(y=-1\) 项 \(\log p-2\log(1-p)\) 不是 BCE
- **影响：** 未知当负类 → 召回偏向被污染；空批“完美损失”可 skew 训练（一旦接上优化器）
- **修复：** \(\mathcal K=\{mask\land y\in\{0,1\}\}\)；空 \(\mathcal K\) 返回 NaN/raise，不要 0

### C-M-09 — 修复记录不实现 Repairability/RR/同预算

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `run_repair` **34–45**；`repairability` **48–51**；`recompute_ratio` **54–57**（`repair.py`）
- **触发：** 任何 `run_repair`。公式函数本身在给定整数时正确，但入口不供给它们
- **原文：** §3（194–198）；REPAIR-01；COST-01
- **证据：** `run_repair(..., [3,4], "abcd")` → `generated_tokens=0`（Repairability 恒为 1）、`extra_prefill_tokens=4`（字符）、`original_token_budget=7`。无跨掩码预算对齐，不调用 `repairability`/`recompute_ratio`
- **影响：** 附录 Table 1 / 成本曲线若走该入口，数字无定义
- **修复：** 写入真实解码与 extra prefill token；按原始槽位 token 对齐预算；RR=槽位数/n

### C-M-10 — 监督适配与无标签适配是同一个 lstsq

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `fit_linear_map` — `transfer.py` **19–32**（`uses_labels` 仅 31 行）
- **触发：** `labeled=True` 与 `False`
- **原文：** §5 / 附录几何；XFER-01；GEOM-01
- **证据：** 两调用同一 `np.linalg.lstsq(tgt, src)`；status 分别为 `supervised_adapt` / `unlabeled_pair_adapt`
- **影响：** 分列报告会把同一估计量写成两种方法
- **修复：** 监督路径必须用标签（或明确拒绝并改名）；映射对象含 `h` 与 `e`

### C-M-11 — P2 只有一对减法，缺相关、位置、缺失处理

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `p2_paired` — `analysis.py` **40–46**
- **触发：** 任意 P2；`base_rho is None` 即崩
- **原文：** §2.6 表 P2；§7（323）；C3-01
- **证据：** 只返回 `noop-base`。`shared_denominator` 原样回传。`p2_paired(None, 0.4, ...)` → TypeError
- **影响：** 不能检验“抬高量与准确率下降相关”，也不能定位污染步；零分母/缺配对不可报告
- **修复：** 配对向量上的相关/回归；位置分层；None → 指标 null + 缺失计数

### C-M-12 — P3 缺非目标、缺相对基线 \(\Delta acc\)、缺分母审计

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `p3_recovery` — `analysis.py` **49–56**。`intervention_report`（`interventions.py` 58–73）有四项相对对照，但 P3 入口不用它
- **触发：** `p3_recovery(main, crand, clayer, invalid)`
- **原文：** §2.6 表 P3；§7（325）；REST-02（禁句开关 **54–55** 行做对了）
- **证据：** 仅 `vs_crand/vs_clayer/invalid_rate`。无 nontarget、无 vs-baseline、无 invalid 是否改变意向分母
- **影响：** 无法排除“靠损伤模型提分”；与干预报告合同分裂
- **修复：** 与 `intervention_report` 合并；保留 REST-02

### C-M-13 — C-rand 匹配 `default_rng(1)` 的范数，不是主干预范数

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `c_rand_delta` — `interventions.py` **31–36**
- **触发：** 任何 C-rand
- **原文：** §2.4 对照；CAUSAL-01；协议 §4：按样本匹配主 \(\Delta\) 实际范数
- **证据：** 主基 seed=123 时 \(\|\Delta_{\mathrm{main}}\|=2.654\)；`c_rand_delta` 的 `actual_norm=0.662`，等于 `default_rng(1)` 子空间投影范数
- **影响：** 对照更弱或更强都不是“同等范数”；P3/C2 相对差值不可解释
- **修复：** 传入主干预已实现的 \(\|\Delta\|\)；零范数走已有 `"zero_norm"` 分支

### C-M-14 — 探针参数不被加权 BCE 估计

- **严重度：** High
- **状态：** confirmed defect（缺失估计量，不是评分公式错）
- **符号：** `BilinearProbe.__init__` **8–19**；`cli.cmd_fit` 143–150（只对随机头算一次 loss）
- **原文：** §4.2；PROBE-01
- **证据：** 无 `fit`/`step`/`backward`。`cmd_fit` 写 `rank=2` 随机头 + `np.eye` 损失
- **影响：** F1/校准/迁移若走该头，读的是噪声方向
- **修复：** 在 `probe_train` 上对已知标签最小化 `weighted_bce`；任务/行为头分开存

### C-M-15 — `sequence_score` 不是 \(a(X)=\max(1-\hat p)\)；CLI 校准不计算分数

- **严重度：** Medium
- **状态：** confirmed defect（接口/流水线）。调用方是否已传入 \(1-p\)：除 CLI 硬编码外未证实
- **符号：** `sequence_score` — `calibrate.py` **9–16**；`cli.cmd_calibrate` **154–158**
- **触发：** 传入 \(\hat p\) 而非 \(1-\hat p\)；或走 CLI
- **原文：** §2.5（132–136）；PROP2-01。N 必须是可交换轨迹/序列，不是边
- **证据：** 函数只 `max(edge_scores)`。CLI 分数恒为 `[0.1,0.2,0.3,0.4]`，与探针输出无关，也不按 `base_group_id` 去重
- **影响：** 命题 2 的覆盖声明当前无法从数据成立
- **修复：** 只在已知真边上算 `1-p`，轨迹/序列取 max；N=独立基础题或已声明的块；空真集才 0

---

## 6. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C-U-01 | Medium | `apply_map` 是单流；无 API 强制双线性的 \(h\) 与 \(e\) 都映射 | `transfer.py` 35–36 | 泛型函数；误用取决于调用方。Pitfall 6 要求双输入 |
| C-U-02 | Low | `bootstrap_cluster` 点估计是轨迹微平均；题内变体多的题权重大 | `analysis.py` 97–108 | 聚类重采样本身正确；estimand 未写明。P1 还没调用它 |
| C-U-03 | Low | `project_delta` 假定列正交，不检查 \(Q^\top Q=I\) | `interventions.py` 9–12 | 公式在假定下正确 |
| C-U-04 | Medium | P1 正类方向未固定；CLI `y` 与链长同向，更像“正确”而非“出错” | `analysis.py` 31–37；`cli.py` 189–190 | 无文档/断言 |
| C-U-05 | Low | 集合路径 `noise_set` 中不在 \(P\) 的元素仍可进入 \(\|N\setminus T\|\) | `measure.py` 94–95 | 未见到如此构造的调用 |
| C-U-06 | Low | `week8_decision` 在传入阈值时标 `evaluated` 却不比较测量 | `analysis.py` 59–66 | Gate 现为 null；比较逻辑不存在 |
| C-U-07 | Low | `sequence_score(..., empty_truth=True)` 忽略已给边分数，返回 0 | `calibrate.py` 12–13 | 矛盾输入；空真集=0 本身正确 |
| C-U-08 | Low | `fit_linear_map` 无截距；均值差被塞进 \(W\) | `transfer.py` 23–24 | 协议写“线性映射”，未要求仿射 |

---

## 7. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C-S-01 | 真实轨迹上命题 2 覆盖 | 无模型分数；当前校准不计算 \(a(X)\) |
| C-S-02 | 4096↔3584 适配后的双线性迁移 | 映射器未绑 \(h,e\)；无真实隐状态 |
| C-S-03 | 预注册后的 P1–P3 区间与功效 | Gate 未注册；估计量本身尚未实现 |

---

## 8. 非缺陷建议 / 已核对为正确的项

以下**不是缺陷**（本通道独立核对通过）：

1. 双线性评分与 `predict_matrix`（`bilinear.py` 21–29）
2. \(y\in\{0,1\}\) 且 mask 正确时的加权 BCE（37–45）
3. \(1\le k\le N\) 与 \(k>N\) 的 conformal 规定例（`calibrate.py` 24–27）；`test_conformal_examples` 的期望值是手写 0.3 / \(+\infty\)，不是用被测函数生成期望
4. `direct_transfer` 拒绝维不等（`transfer.py` 9–15）；lstsq 在配对行上可回收 \(W\)
5. 集合路径：零分母 → None；缺失 sham → excess None；负 excess 不截断（`measure.py` 85–108；`finite_or_none` 只丢非有限值）。`test_signed_excess_not_clipped` / `test_zero_denominator_null` 与手算一致
6. TO \(=2\mathrm{LCS}/(|T_0|+|T_1|)\)；双空 → None（`lcs_overlap` 148–159）。CSP 为已对齐干净事件的值保持率，空分母 None（162–197）
7. 交换 \(H+\Pi_Z(H_d-H_b)\)（`interventions.py` 9–16）
8. Repairability / RR 在分母为 0 时返回 None（`repair.py` 48–57）
9. `p3_recovery["causal_reverse_claim"] is False`；Week-8 无阈值 → `unregistered` 且 `scientific_conclusion is None`
10. `procrustes` 在形状不等时 N/A；`R=U V^H` 形式正确（`analysis.py` 83–88）。`cone_fit` 不报定律（78–80）
11. `require_split("test", ("transfer_pairs",))` 拒绝在 test 上拟合映射

建议（非必须）：`_auc` 的 `np.trapz` 在 numpy 2 将移除；INLP 文档写 `I-PP^T stacked`（`interventions.py` 40）与返回的累乘投影不符。

---

## 9. 测试质量（仅就本通道公式）

`tests/test_science.py` **不能**作为这些估计量的正确性证明：

- 校准只覆盖两个已手算正确的 \((\alpha,N)\)，不覆盖 \(k=0\)、浮点相等、按题去重的 \(N\)
- P1 只测单类 → None，不测 AUC 平局、不测“\(\rho\) 无增量”
- 无 `weighted_bce`、无矩阵 `noise=None`、无 INLP 多步、无 Repairability、无 P2
- `test_measure.py` 覆盖集合路径的负 excess / 零分母，**不**覆盖并集 vs 逐步平均，也**不**覆盖矩阵缺失噪声

因此：22 passed ≠ 公式正确。

---

## 10. 结论

本通道**不通过**。在声明冻结哈希未能复现的前提下，对当前磁盘源码的独立推导与反例表明：若干**将进入论文数字**的估计量是错的或不完整，而不是“尚未接真实模型”。

必须先修的 confirmed defects：

- P1 AUC（C-M-03、C-M-04）
- 矩阵 excess 在无噪声时的伪造（C-M-05）
- conformal \(k<1\) 回绕（C-M-01）
- INLP 非迭代（C-M-07）
- C-rand 范数锚错（C-M-13）
- \(\rho_S(T)\) 并集误用（C-M-06）
- 探针无估计、修复预算为 stub、加权 BCE 未知标签（C-M-14、C-M-09、C-M-08）

已核对**正确**的核心碎片：双线性评分形式、规定 conformal 例、直接迁移拒维、集合路径有符号 excess / 零分母、交换公式、RR/Repairability 的零分母、Week-8 禁句。这些不足以支持 C3/校准/迁移/修复的科学声明。

**验收意见：** `FAIL_MATH_STATS`。在 C-M-01–15 关闭并经独立复审前，不得把 P1–P3、整链覆盖、跨模型适配或 Repairability 写成可报告结果。
