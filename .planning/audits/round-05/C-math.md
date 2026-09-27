# C：数学与统计独立审查（round-05）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性 \(\sigma(h^\top UV^\top e+b)\)、\(\lambda_{\mathrm{FN}}=10\)、split conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)、\(k>N\Rightarrow+\infty\)、\(a(X)=\max_{j\in R(s_i)}(1-p)\)、S/M/\(\rho\) 事件均值、已评估 0-hit sham → noise=0 不是 null、P1 留出 logistic + bootstrap、P2 配对 + 支持集、P3 vs 对照、交换 \(H+\Pi_Z(H_d-H_b)\)、C-rand 范数匹配、INLP 在已投影 \(H\)、Boundary BCE 符号、`cone_fit`、4096≠3584 N/A、Week-8 无发明门。仍错则给反例。在当前树重跑 r04 C4-M-01/02/03 数值反例。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读 round-05 的 A/B/D/E/F。体例对照过 `round-04/C-math.md`，**结论全部由本轮对当前磁盘字节的公式推导与数值反例重做**，不沿用上一轮状态，不采信 ISSUES 的作者 `local close` / `fixed_pending_review`
- 声明冻结哈希：`4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4`（`.planning/audits/round-05/VERSION.md`，58 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**是 / HASH_MATCH**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改（只写本文件）
- numpy：1.26.4；CPython 3.11.7

---

## 1. 冻结哈希

范围内文件数：**58**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 15 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「58 files」一致。相对 r04 的 56 文件，多出 `src/reasoning_diff/models/tokenize.py` 与 `tests/test_round04_regressions.py`。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 方法 | SHA-256 | 与声明值 |
|---|---|---|
| VERSION 脚本（本审查独立执行） | `4c8769f3b212006ac663cfeca1bcd60e4af65ea4cb8b4cafd4a147e7cd6d56e4` | **HASH_MATCH** |

审查对象绑定该冻结快照。逐文件 SHA-256 见附录。下列公式结论绑定这些 digest。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | `52de70553b37dec69822b790b006b7282e58ee926bb77006b3da40b419726e15` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + 未知哨兵 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | `sequence_score`/`truth_indices`/`conformal_threshold`/`predict_set` | 全文；手算 \(k\)；C4-M-02 原调用 + `R(s_i)` |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | `BoundaryMLP` Hidden=256；BCE 符号 | 全文；C4-M-03 原反例 |
| `src/reasoning_diff/analysis.py` | 1–283 | `3593254605792c6e13fe45ec658c67f1f55af35c224df84f77dd5ce1c2e14730` | `_auc`/`_fit_scores`/`p1_incremental`/`bootstrap_cluster`/`p2_paired`/`p3_recovery`/`cone_fit`/`week8_decision` | 全文；IRLS；退化区间反例 |
| `src/reasoning_diff/transfer.py` | 1–63 | `d72e1dd1c4192b0936fb661405151447bcb3a100a40d6fb4ba577b8d161b1665` | `direct_transfer`/`fit_linear_map`/`apply_map`/`common_dim_then_procrustes` | 全文；监督加权 lstsq |
| `src/reasoning_diff/measure.py` | 1–342 | `5102a7dd0a2d0e99a4941c50cf6705355c83c32fdebb507314a0323ffec57d5b` | `dependency_densities`/`event_density_sets`/`noise_evaluated` | 全文；0-hit 三前提构造 |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | `inlp_remove`/`c_rand_delta`/`c_layer_delta`/`apply_swap` | 全文；与 r04 字节相同 |
| `src/reasoning_diff/repair.py` | 1–189 | `418d804da3da8bf073b418addc7c34f0bc4ad04a53bd631c9e15270ab43ebc23` | `repairability`/`run_repair` | 对照 |
| `src/reasoning_diff/baselines.py` | 1–120 | `f99d32f1e5c59e48af95d94f33b58ab33ea06a6331c5bf2e7a6ce5457a6ff190` | rollout / verbalizer | 全文（非本通道主公式） |
| `src/reasoning_diff/cli.py` | 352–798 | `b1d801f16bc651e26c44a13f5c9c3fac837647c0de359033cc453d3fdfb06ab7` | `cmd_label`/`cmd_calibrate`/`cmd_analyze`/`cmd_intervene` | 只读调用链；`a(X)` 真边构造 |
| `tests/test_science.py` | 1–101 | `bed01ffa293f2c1f3d341e9b4ddbf375436eb77fa1a82c5093f12a7a402ca126` | 校准规定例 / 4096≠3584 | 查是否独立 |
| `tests/test_measure.py` | 1–40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | 负 excess / 零分母 | 集合路径 |
| `tests/test_review_regressions.py` | 1–394 | `37414926677d059610794b4f64ec3bcbf7c242ecce9c563bc8e549abc5d3a60c` | C-01..C-04 / 未知 BCE / 事件均值 | 查测试能否关闭缺陷 |
| `tests/test_round03_regressions.py` | 1–291 | `5698a410c0669b6142f31d5b302ff8c7ef8ec66cc9ef429786d45e2418bfc278` | C3-M-01/02/03/05/07 / cone / labeled | 查是否独立 oracle |
| `tests/test_round04_regressions.py` | 1–310 | `93f04cc13c39d6b0a906194ef6ef784642c9f0b7613b7807deb8f7947e08ed56` | 0-hit / `truth_indices` / BCE 符号 / P1 bootstrap 字段 | 查是否独立 oracle |

调用链只读、不计入“已证明正确”：`cli.cmd_fit` / `cmd_calibrate` / `cmd_intervene` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文：`Reasoning-Diff-修订方案-v3 (1).md` §2.5–2.6、§4.2、§5–7、附录 S2–S3；PITFALLS 校准/P1/P2 条；REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01 / MEDIATION-01 / BOUND-01 / FIT-01 / DECIDE-01。

### 3.1 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b)=\sigma(\langle h_i U,\,e_j V\rangle+b),\quad
(HU)(EV)^\top\text{ 为矩阵形式}.
\]

默认 \(r=64\)，\(\lambda_{\mathrm{FN}}=10\)。未知不得进入 \(\mathcal K=\{i:\mathrm{mask}_i\land y_i\in\{0,1\}\}\)。空 \(\mathcal K\) 是无效损失，不是 0。

对 \(y\in\{0,1\}\)：

\[
\ell=\frac1{|\mathcal K|}\sum_{i\in\mathcal K} w_i\bigl[-y_i\log p_i-(1-y_i)\log(1-p_i)\bigr],
\quad w_i=\lambda_{\mathrm{FN}}\mathbf 1[y_i=1]+1\cdot\mathbf 1[y_i=0].
\]

logit 梯度 \(w(p-y)/|\mathcal K|\)，\(dU=H^\top(dZ\,EV)\)，\(dV=E^\top(dZ^\top HU)\)。

`score` / `predict_matrix` 与上式一致。`weighted_bce` **87–95** 与 `fit` **44–47** 把 \(\mathcal K\) 限制为有限且 \(y\in\{0,1\}\)；空 \(\mathcal K\) 分别返回 NaN / `loss=None`。本轮字节与 r04 的 bilinear digest 相同。

### 3.2 Split conformal 与 \(a(X)\)

\[
a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij}),
\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow q=+\infty\)。\(\alpha\notin[0,1)\) 必须拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。等于 \(q\) 的边须保留。

`conformal_threshold` 的 \(k\) 与非法 \(\alpha\) 分支与上式一致。`predict_set` 为 \((1-p)\le q+10^{-12}\)。`sequence_score` 在传入 `truth_indices` 且 `nonconformity="one_minus_p"` 时对**指定列**取 \(\max(1-p)\)；省略 `truth_indices` 仍对传入的全部列取 max。CLI `cmd_calibrate` **570–592** 把全部 `task_label==1` **或** `behavior_label==1` 的前提并成**一条全局索引**，再套到 `predict_matrix` 的每一行——这不是逐事件 \(j\in R(s_i)\)。

### 3.3 迁移

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。无标签配对：中心化后正交 Procrustes（同维）或中心化 lstsq（异维）。监督适配必须是不同估计程序，且必须有标签张量。本轮 `labeled=True` 用 \(|y-\bar y|+0.1\) 做行加权 lstsq；0/1 翻转不改变权重。

### 3.4 P1–P3

- **P1：** 在 train 拟合控制模型 vs 控制+\(\rho\)（logistic / IRLS）；在**留出**基础题上比 Mann–Whitney AUC。平局贡献 \(1/2\)。须附**问题级聚类 bootstrap 区间**：重采样基础题（簇），在每次重抽样上重算 \(\Delta\mathrm{AUC}\)，再取分位数。默认路径不得写死 `len+0.01*op`。`precomputed` 必须是调用方已算好的分数。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\) 必须共用分母 \(|P\setminus R_{\mathrm{task}}|\)；缺配对不得崩。整数 `shared_denom` 本身不是支持集；须有 `shared_premises` 且 \(|\mathrm{shared\_premises}|=\) 声称分母。
- **P3：** 相对 C-rand / C-layer；报告非目标响应与相对基线 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

### 3.5 Excess / INLP / 对照范数 / 锥

缺失噪声协议 ⇒ excess = null。空 `noise_set` 且**未评估** ⇒ null。已评估且 0-hit ⇒ \(N=\emptyset\)、noise \(=0\)、excess \(=\) raw，**不是**缺失。excess 可负。\(\rho_S(T)=\frac1n\sum_i\rho_S(s_i)\)，不是并集一次调用。

INLP：每步在**已投影** \(H\) 上重拟合，再累乘 \(I-uu^\top\)。C-rand / C-layer 必须缩放到该样本主干预实际 \(\|\Delta\|\)。交换 \(H'=H_b+\Pi_Z(H_d-H_b)\)。

附录 S2：\(|\mathrm{cone}|/n\approx 1-\exp\{-\lambda(1-x)^\gamma\}\)，必须对 \((\lambda,\gamma)\) 做拟合；\(R^2\) 只作描述。Week-8 Gate 0–2 无预注册阈值时必须保持 `unregistered`，不得发明通过线。

Boundary MLP：2 层 ReLU，Hidden=256；报告损失须是 BCE \(-\bigl[y\log p+(1-y)\log(1-p)\bigr]\)。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（误差 0） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(0.5(10(-\log 0.8)+(-\log 0.8))=1.2272895322281534\) | **通过** |
| CHK-04 | 空 mask；`y=-1` / `y=2` / `y=0.5` | 直接调用 | **通过**：`-1`/`2`/`0.5`/`nan` 均等于仅正类项 \(10(-\log 0.8)=2.231435513142097\)。空 mask → NaN |
| CHK-05 | `y=nan` 是否排除 | `weighted_bce` | **通过** |
| CHK-06 | `fit` 梯度 | \(U_{00}\) 解析 vs 有限差，相对误差 \(1.12\times10^{-8}\) | **通过**（已知 \(\{0,1\}\)） |
| CHK-07 | `fit(-1)` 是否等于 `fit(nan)` | 同初值一步 | **通过**（\(\Delta U=0\)，loss 同 \(4.740825819202817\)）。空 \(\mathcal K\) → `no_known_labels` |
| CHK-08 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | \(N=4,\alpha=0.4\Rightarrow k=3,q=0.3\)；\(\alpha=0.1\Rightarrow+\infty\)；\(N=1,\alpha=0.05\Rightarrow+\infty\)；\(N=3,\alpha=0.5\Rightarrow k=2,q=0.2\)；\(N=10,\alpha=0.05\Rightarrow+\infty\)；\(\alpha=0\Rightarrow+\infty\) | **通过** |
| CHK-09 | \(\alpha\ge 1\)、\(\alpha<0\)、`None` 不回绕 | \(\alpha=1,1.5,-0.1,\mathrm{None}\) | **通过**（`invalid`，`q is None`） |
| CHK-10 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**：`1.0-0.7=0.30000000000000004`，无 slack 为 False，`+1e-12` 后为 True。`0.4` 边排除；\(q=+\infty\) 全选 |
| CHK-11 | `sequence_score` / \(a(X)\)；**重跑 C4-M-02** | `[0.9,0.1,0.8]`；两事件异真边 | **库函数部分通过**：`truth_indices=[0]` → \(0.1\)。**精确 r04 调用**（无 indices）仍 \(0.9\)。CLI 并集见 C5-M-02：两事件论文 \(0.1\)，并集 \(0.9\) |
| CHK-12 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`(2,3)@(4,2)` | **通过**（N/A；`matmul` 形状错） |
| CHK-13 | labeled 缺张量 | `labeled=True, labels=None` | **通过**（`ValueError: supervised adapt requires a label tensor`） |
| CHK-14 | labeled vs unlabeled 是否改估计 | 平移 \(X'=X+c\)；`[0,1]` vs `[1,0]` | **通过（程序已分列）**：unlabeled \(\|W-I\|_\infty\sim10^{-16}\)；labeled \(\|W-I\|_\infty=0.989\)。翻转 0/1 的 \(\|W\|_\infty\) 差为 **0**（C5-U-01）；非翻转模式差 \(0.257\) |
| CHK-15 | 常数分数 AUC 与排列 | `_auc(ones, y)` | **通过**（0.5） |
| CHK-16 | Mann–Whitney 平局 | 分数 `[1,2,2,3]`，标签 `[0,0,1,1]` | **通过**（手算 \(0.875\)） |
| CHK-17 | 默认 P1；留出 logistic；`precomputed` | \(n=40\)，`len≡10`，`op~N(0,1000)`，`rho=y` | **默认通过**（`requires_held_out`）。**留出通过**：`estimator=held_out_logistic`，`auc_full=1`，`auc_base=0.71`，`delta=0.29`。**`precomputed` 通过**：`auc_base=0.5`，`auc_full=1`，`delta=0.5`。旧魔法 `10+0.01*op` 在 held 上 AUC=0.71，现不是这条路径的估计量 |
| CHK-18 | 留出拟合是否忽略 eval 行的 \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 分数差 0；eval 分数变 \(0.187\)） |
| CHK-19 | 空/满 `held_out` | 全 True / 全 False | **通过**（`held_out_empty`） |
| CHK-20 | P1 bootstrap 是否为问题级 \(\Delta\mathrm{AUC}\) 区间 | 同上 \(n=40\)，`groups=i//2`；独立簇重算 AUC | **失败**（C5-M-01）：代码区间 \([0.29,0.29]\)，宽度 0。独立簇 bootstrap 宽度 \(0.3305\)，区间 \([0.120,0.450]\)。仅传 `rng` 时 bootstrap 的是 \(\rho\)（均值 0.5），不是 \(\Delta\mathrm{AUC}\) |
| CHK-21 | P2 减法、None、支持集、整数分母 | `p2_paired(0.2,0.5,0.8,0.6,4)`；`None`；`99` vs `['p1']`；`list('abcd')` | **asked 项通过**：无支持集 → `denominator_unverified`；`None` + 匹配支持集 → `missing_pair`；`99` vs 1 元列表 → `denominator_inconsistent`；有支持集差值 \(0.3/-0.2\)。**残留**（C5-U-03）：`0.9` 对分母 4 仍 `ok` |
| CHK-22 | P3 相对对照、非目标、禁句 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline_acc=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`nontarget=0.2`，`causal_reverse_claim is False` |
| CHK-23 | INLP 更新 \(H\) | r04 矩阵 \(H=[[2,0],[2,0],[0,1],[0,1]]\)；手算 \(w=(0.5,-1)\) | **通过**：一步后 \(HP=\[[1.6,0.8],[1.6,0.8],[0.4,0.2],[0.4,0.2]]\)；两步后 \(\approx 0\)；`max\|P1-P8\|=0.8` |
| CHK-24 | C-rand / C-layer 匹配主范数 | r04 构造 seed=0 / 基 seed=99 | **通过**（`actual_norm=2.7233772766385282` 与主范数 `isclose`；缺 `target_norm` 抛错；dummy rng(1) 范数 0.662；零 \(\Delta\) → `zero_norm`） |
| CHK-25 | 交换公式 | \(e_1+\Pi_{e_2}(e_2-e_1)=e_1+e_2\) | **通过**（`[1,1]`） |
| CHK-26 | 集合路径负 excess、零分母、缺 sham | 手算 −0.5；无 protocol | **通过** |
| CHK-27 | 矩阵 `noise=None` | `task=[[0,1]], behavior=[[1,0]]` | **通过**（null） |
| CHK-28 | 并集 \(\rho\) vs \(\frac1n\sum\rho(s_i)\) | r03 两事件：\(1/2\) 与 \(0\)，均值 **0.25** | **通过**（`aggregation=mean_over_events`） |
| CHK-29 | 空 `noise_set` 未评估一律 null | `[]` + protocol `hits=['p3']`，`noise_evaluated` 缺省 | **通过**：`rho_S_noise is None`，`null_reason=noise_set_empty` |
| CHK-30 | **重跑 C4-M-01** 已评估 0-hit sham | 三前提任务 \(P=\{p1,p2,p3\}\)，\(T=\{p1,p2\}\)，\(B=\{p3\}\)，`noise_ref=0` | **通过**：手算 \(\rho=1\)、noise=0、excess=1；`event_density_sets` 得 `raw=1`、`noise=0`、`excess=1`、`null_reason=None`。API `noise_evaluated=True` 且 `noise_set=[]` 同。`t1_tiny`（无 p3 列）分母空 → `rho_S=None`，不是本条反例 |
| CHK-31 | Boundary Hidden=256；拒绝 128 | 形状 + `ValueError` | **通过** |
| CHK-32 | **重跑 C4-M-03** Boundary 报告损失 | \(y=0,p=\sigma(10)\) | **通过**：报告 \(10.000045398900186\)，与真 BCE 相同，不再为负 |
| CHK-33 | `cone_fit` 是否拟合 | \(y=1-e^{-0.8(1-x)^{1.5}}\)，\(n=12\) | **通过**：`r2=0.972108180856696`，\((\hat\lambda,\hat\gamma)=(0.6812920690579611,1.2)\)（grid 最近元）。\(n<2\) → `r2=None`。`wording=descriptive_only` |
| CHK-34 | Week-8 无发明门 | 默认；`excess==0`；传入阈值 | **默认通过**：三门 `threshold=None`/`unregistered`，`scientific_conclusion is None`。`excess==0` 把分流标成 `c3_negative_descriptive` 并 `skip_p2_p3`（C5-U-04）。传入阈值标 `evaluated` 但不比较测量（C5-U-04） |
| CHK-35 | CLI `a(X)` 是否逐事件 \(R(s_i)\) | 复现 `cmd_calibrate` **578–583** 的并集规则 | **失败**（C5-M-02）：`task∪behavior` 得到列 `[0,1,2]`；两事件异真边论文 \(0.1\)、并集 \(0.9\) |
| CHK-36 | `pytest` 数学相关 | `tests/test_science.py tests/test_measure.py tests/test_review_regressions.py tests/test_round03_regressions.py tests/test_round04_regressions.py -q` | **92 passed，exit 0**。不覆盖 CHK-20 区间宽度、CHK-35 并集、CHK-14 翻转不变 |
| CHK-37 | 作者声称全仓库 120 | `python -m pytest tests -q`（本审查重跑，非采信） | **120 passed，13.52s**。不等于公式正确 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | CLI 校准不按逐事件 \(R(s_i)\)（C5-M-02）；真实权重属 pending_server |
| 阅读其他 round-05 通道 | 任务禁止 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数；高维功效属外部 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用分数值域、污染 eval \(X\)、检出 \(\rho=y\) 代替 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\) |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | \(0\le\alpha<1\) 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | `work = work @ step`；一步 \(HP\) 与手算 \(w=(0.5,-1)\) 一致 |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm`；匹配主范数 \(2.7233772766385282\) |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels` |
| C2-M-02 默认 P1 非留出 | **关闭** | 省略 `held_out` 且非 `precomputed` → `requires_held_out` |
| C3-M-02 P1 非 logistic / `precomputed` 魔法系数 | **关闭（点估计）** | `_fit_scores` 为 30 步 IRLS logistic；`precomputed` 把 `length`/`rho` 当调用方分数。区间见 C5-M-01 |
| C2-M-03 `1-0.7≰0.3` | **关闭** | `q+1e-12` 保住该边 |
| C3-M-01 并集 \(\rho_S(T)\) | **关闭** | `event_sets` → `mean_over_events`；r03 反例现得 0.25 |
| C2-M-05 监督/无标签同一 lstsq | **关闭（估计程序）** | 无标签：中心化 Procrustes；监督：行加权未中心化 lstsq |
| C2-M-06 P2 `None` TypeError | **关闭** | `missing_pair` |
| C3-M-03 共享分母 | **关闭 asked 项** | 无支持集 → `denominator_unverified`；整数≠列表长度 → `denominator_inconsistent` |
| C3-M-04 / C4-M-02 \(a(X)\) | **库函数部分关闭** | `truth_indices` 可使单行 \(a=0.1\)。CLI 并集未关（C5-M-02） |
| C3-M-05 P3 非目标 | **关闭（接口）** | `nontarget` / `vs_baseline` 字段存在 |
| C3-M-07 空袋+hits 伪造 0 | **关闭（未评估 API）** | 空 `noise_set` 且非 `noise_evaluated` → `noise_set_empty` |
| C4-M-01 0-hit → excess null | **关闭** | 三前提构造：`noise=0`，`excess=1`。不采信 ISSUES；本轮独立复算 |
| C4-M-03 Boundary BCE 符号 | **关闭** | 报告 \(+10.000045398900186\)。不采信 ISSUES；本轮独立复算 |
| `cone_fit` 空壳 | **关闭** | grid 最小化 \(SS_{\mathrm{res}}\) |

---

## 7. 发现

状态：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

### C5-M-01 — P1 的 `bootstrap` 不是问题级 \(\Delta\mathrm{AUC}\) 区间

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `p1_incremental` `analysis.py` **76–79**；`bootstrap_cluster` **272–283**。CLI `cmd_analyze` **737–738** 始终传入 `groups`，走退化分支
- **原文：** §2.6 / §7 / C3-01 / PITFALLS：控制链长与 op 后的 logistic AUC **附问题级聚类 bootstrap 区间**；重采样基础题时带走该题全部变体，再重算增量
- **反例（独立手算，当前树）：**
  - \(n=40\)，`length≡10`，`op~N(0,1000)`，`rho=y`，后 20 行留出，`groups=i//2`
  - 点估计：`auc_full=1`，`auc_base=0.71`，\(\delta=0.29\)（留出 IRLS 本身正确）
  - 代码：`bootstrap_cluster([δ]*40, groups)` → `interval=[0.29, 0.29]`，宽度 **0**
  - 独立实现：在留出簇上重采样并重算 \(\Delta\mathrm{AUC}\)（200 次）→ 均值 \(0.282\)，区间 \([0.120, 0.450]\)，宽度 \(0.331\)
  - 不传 `groups` 只传 `rng`：bootstrap 的是原始 \(\rho\)（均值 \(0.5\)，区间 \([0.35,0.625]\)），**不是** \(\Delta\mathrm{AUC}\)
- **影响：** 生产 analyze 路径会把零宽度区间写成 P1 的不确定性。常数列表的簇 bootstrap 在代数上不可能产生非退化区间。`test_p1_returns_bootstrap_interval` 只断言字段非空，锁不住宽度
- **修复：** 按基础题（簇）重采样留出单元，每次重算 `auc_full-auc_base`（或至少重算该次样本的 Mann–Whitney），再报分位数。禁止把标量 \(\delta\) 复制 \(n\) 次冒充区间

### C5-M-02 — CLI 校准的 \(a(X)\) 仍是全局 `task∪behavior` 并集，不是 \(\max_{j\in R(s_i)}(1-p)\)

- **严重度：** Medium
- **状态：** confirmed defect（流水线；库函数在传入 `truth_indices` 后可以对单行算对）
- **符号：** `cli.cmd_calibrate` **578–592**；`sequence_score` 默认仍全列
- **原文：** §2.5（134）：\(a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij})\)。任务头与行为头**各自**标签分别校准
- **重跑 C4-M-02（当前树）：**
  - 一行 \(\hat p=(0.9,0.1,0.8)\)，真依赖只有第 0 列
  - 论文：\(a=0.1\)
  - `sequence_score(..., nonconformity="one_minus_p")`（r04 原调用，无 indices）：**仍 \(0.9\)**
  - `truth_indices=[0]`：\(0.1\)（库函数现可对齐）
- **CLI 并集反例：** 两行 \(\hat p_0=(0.9,0.1)\)、\(\hat p_1=(0.1,0.9)\)，\(R(s_0)=\{0\}\)、\(R(s_1)=\{1\}\)
  - 论文：\(a=\max(0.1,0.1)=0.1\)
  - 把并集 `[0,1]` 套到每一行：\(\max(0.9,0.9)=0.9\)
  - 复现 CLI：`task_label==1 or behavior_label==1` 对 `{p1,p2,p3}` 得到索引 `[0,1,2]`
- **证据：** 同一 `truth` 用于 `pred` 的每一行，再按 `task_id` 取 max。不读逐事件 \(R(s_i)\)，并把行为正例并进任务真边
- **影响：** 命题 2 的 \(q_\alpha\) 被他步真边或虚假行为边抬高；覆盖事件与可交换单位都不是原文定义。scientific 模式已拒绝字面量，不再是 loss 拼数
- **修复：** 每行只用该事件的任务头（或行为头）真列；空真集才为 0；\(N=\) 独立基础题或已声明的块

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C5-U-01 | Medium | 监督适配用 \(\sqrt{\|y-\bar y\|+0.1}\) 加权；`[0,1]` 与 `[1,0]` 的 \(W\) 相同 | `transfer.py` 25–28 | 估计程序已与 unlabeled 分列，且非翻转标签会改 \(W\)（差 \(0.257\)）。若“监督”必须吃任务/行为方向，则目标仍是加权 lstsq 不是分类损失 |
| C5-U-02 | Low | P1 偏相关用全样本不是留出 | `analysis.py` 74 | 原文要偏相关，未写死留出。\(\rho=y\) 时全样本与留出都是 1 |
| C5-U-03 | Low | P2 不在支持集上重算 \(\rho\)；`0.9` 对分母 4 仍 `ok` | `analysis.py` 151–160 | 支持集存在性与整数一致性已关 asked 项。\(0.9\notin\{0,1/4,1/2,3/4,1\}\) |
| C5-U-04 | Low | `excess==0` 自动 `c3_negative_descriptive`+跳过 P2/P3；传入 `gate_thresholds` 标 `evaluated` 但不比较测量 | `analysis.py` 182–211 | Gate 0–2 默认仍 `unregistered`，`scientific_conclusion is None`。本轮“无发明通过线”默认路径成立。PITFALLS 写过未定义判据不得自动跳过 |
| C5-U-05 | Low | `event_sets` 对 None 密度跳过再平均：`[None, 1]` → `1.0` 不是 `1/2` | `measure.py` 109–111 | 分母为空记 N/A 后，\(n\) 是否含 N/A 步原文未写死 |
| C5-U-06 | Low | 0-hit 时 `rho_M_noise=\|T\setminus N\|/\|T\|=1`，excess\(_M=\rho_M-1\le 0\) | `measure.py` 137–141 | 论文对 \(\rho_M\) 噪声参照没有写出与 \(\rho_S\) 对称的集合公式。本轮清单要的是 S 的 noise=0，该项已对 |
| C5-U-07 | Low | INLP 用 lstsq(\(\pm1\)) 不是 SVM；低维 8 步可投掉整空间 | `interventions.py` 52–67 | 迭代投影本身已对 |
| C5-U-08 | Low | `predict_set(q=None)` TypeError | `calibrate.py` 42–45 | 非法 q 应由校准入口挡住；入口对 \(+\infty\) 已写成 JSON `null` |
| C5-U-09 | Low | `t1_tiny` 上的 0-hit 回归用缺 p3 的任务，分母空、`rho_S is None`；断言是 `null_reason!=empty or excess is not None` | `tests/test_round04_regressions.py` 155–175 | 生产三前提构造已对。测试不能关闭 C4-M-01，但不构成新的生产公式错误 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C5-S-01 | 真实轨迹命题 2 覆盖 | 校准不按逐事件真边算 \(a(X)\) |
| C5-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明 N/A |
| C5-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册；真实轨迹未跑；即便跑了，当前 bootstrap 也不能用 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`（`bilinear.py` 21–29）；`fit` 在 \(y\in\{0,1\}\) 上的梯度（有限差 \(1.12\times10^{-8}\)）
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64
3. 未知哨兵 `-1` / 非 \(\{0,1\}\) / NaN 不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
4. Conformal \(k\) 公式、\(k>N\Rightarrow+\infty\)、\(\alpha\notin[0,1)\) 拒绝；\(\alpha=0\Rightarrow+\infty\)
5. `predict_set([0.7], 0.3)` 为 True（`1e-12` slack）
6. `sequence_score(..., truth_indices=[0], nonconformity="one_minus_p")` 得 \(0.1\)；空真集得 \(0\)
7. `direct_transfer` 拒 4096≠3584；`apply_map` 维不匹配无法乘
8. `labeled=True` 无张量即失败；无标签适配 ≠ 监督加权 lstsq（平移回收 \(I\)，监督不回收）
9. `_auc` Mann–Whitney，平局 1/2
10. 默认 P1 拒绝无留出；留出 IRLS logistic 不吃 eval 行的 \(X\)；能检出被 op 淹没的 \(\rho=y\)；`precomputed` 是调用方分数
11. P2：无支持集 → `denominator_unverified`；缺测 → `missing_pair`；分母与列表不一致 → `denominator_inconsistent`
12. P3：`vs_crand`/`vs_clayer`/`vs_baseline`/`nontarget`；`causal_reverse_claim is False`
13. `event_sets` 均值 0.25，不是并集 0
14. **C4-M-01 当前树关闭：** 已评估 0-hit → `noise=0`、`excess=1`。空列表且未评估仍 null
15. 集合/矩阵：零分母 None；缺 sham → excess None；负 excess −0.5 不截断
16. INLP 在已投影 \(H\) 上迭代
17. C-rand / C-layer 匹配传入的主干预范数；缺范数即失败
18. 交换 \(H+\Pi_Z(H_d-H_b)\)
19. **C4-M-03 当前树关闭：** `BoundaryMLP` 报告 BCE \(+10.000045\)；Hidden=256，非 256 拒绝
20. `cone_fit` 对 \((\lambda,\gamma)\) 做 \(25\times20\) grid，返回 r2/参数；措辞 `descriptive_only`
21. Week-8 默认三门 `unregistered`，`scientific_conclusion is None`，不发明 Gate 通过线

---

## 11. 测试质量（仅公式）

数学五文件 `92 passed` 与全仓库 `120 passed` **不能**证明本通道估计量正确。

- `test_c_unknown_label_is_masked` **有效**
- `test_p1_requires_held_out_by_default` / `test_p1_held_out_logistic_detects_rho` **有效**（点估计）
- `test_p1_precomputed_is_scores_not_magic` **有效**
- `test_p1_returns_bootstrap_interval` **无效（区间）**：只断言 `bootstrap`/`interval` 非空，退化 \([δ,δ]\) 也会过
- `test_c3_m01_event_mean_not_union` **有效**（0.25）
- `test_c3_m07_empty_noise_ignores_hits` **有效（未评估 API）**
- `test_evaluated_zero_hit_sham_is_zero_noise_not_null`：**API 半有效**（`noise_evaluated=True` 的 `dependency_densities` 锁住 excess=1）；`event_density_sets(t1_tiny, …)` 因夹具无 p3、分母为空而 `rho_S is None`，OR 断言仍通过
- `test_p2_integer_denom_without_set_is_unverified` **有效**
- `test_p3_reports_nontarget` **有效（字段）**
- `test_sequence_score_uses_true_edges_only` 锁住 `truth_indices=[0]→0.1`，**同时锁住无 indices 时的 `0.9`**
- `test_boundary_bce_not_negative` **有效**（本轮 C4-M-03 反例）
- `test_cone_fit_returns_r2` 只断言 `r2>0.9`，不回收真 \((\lambda,\gamma)\)
- `test_labeled_transfer_needs_labels` 不验翻转是否改变 \(W\)
- 无 CLI 并集 \(a(X)\) oracle，无独立簇 AUC 宽度 oracle

---

## 12. 结论

冻结哈希 `4c8769f3…` **HASH_MATCH**。审查绑定该 58 文件快照。全仓库 pytest **120 passed**（本审查重跑）。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | 通过 |
| 未知 mask / 空 \(\mathcal K\) 为 NaN 不是 0 | 通过 |
| conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) | 通过 |
| `predict_set` \(1-p\le q\)（含 0.7/0.3） | 通过 |
| \(a(X)=\max_{j\in R(s_i)}(1-p)\) | 库函数在传入 `truth_indices` 后通过；**CLI 失败**（C5-M-02） |
| P1 留出 logistic，不是 `length+0.01*op` | **通过（点估计）** |
| P1 问题级 bootstrap | **失败**（C5-M-01） |
| P2 配对 + 支持集 | **asked 项通过** |
| P3 vs 对照 | **通过（接口）** |
| \(\rho_S(T)=\) 事件均值不是并集 | 通过 |
| 0-hit 已评估 sham → noise=0 不是 null | **通过**（C4-M-01 关闭） |
| INLP 在投影 H 上；C-rand 匹配主范数 | 通过 |
| 交换 \(H+\Pi_Z(H_d-H_b)\) | 通过 |
| 4096≠3584 直接迁移 N/A | 通过 |
| Boundary BCE 符号 | **通过**（C4-M-03 关闭） |
| `cone_fit` 真正拟合 | 通过 |
| Week-8 无发明门 | **默认通过** |

**可关闭（独立确认，非采信 ISSUES）：** C-01、C-02、C-03、C-04、C2-M-01、C2-M-02、C3-M-02（点估计）、C2-M-03、C3-M-01、C2-M-05、C2-M-06、C3-M-03（asked）、C3-M-05（接口）、C3-M-07（未评估 API）、**C4-M-01**、**C4-M-03**、`cone_fit` 空壳。

仍会污染论文数字的 confirmed defects：**C5-M-01**（P1 bootstrap 宽度恒为 0，独立簇区间宽度 0.33）；**C5-M-02**（CLI \(a(X)\) 0.9 vs 论文 0.1）。

**r04 反例重跑：** C4-M-01 在三前提任务上现得 excess=1；C4-M-03 现得 BCE \(+10.000045\)；C4-M-02 的**原函数调用**仍返回 0.9，生产校准入口仍用并集。

**验收意见：** `FAIL_MATH_STATS`。在 C5-M-01 关闭并经独立复审前，不得把 analyze 的 `bootstrap.interval` 写成 P1 不确定性。在 C5-M-02 关闭前，不得把 CLI 校准写成命题 2 覆盖。

---

## 附录：58 文件 SHA-256（POSIX relpath，仅 file bytes）

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  3593254605792c6e13fe45ec658c67f1f55af35c224df84f77dd5ce1c2e14730
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  f99d32f1e5c59e48af95d94f33b58ab33ea06a6331c5bf2e7a6ce5457a6ff190
src/reasoning_diff/cli.py  b1d801f16bc651e26c44a13f5c9c3fac837647c0de359033cc453d3fdfb06ab7
src/reasoning_diff/edits.py  bfd1632b50504c042640bcda85368b0c695fd3f843ea885200d080055aa107b6
src/reasoning_diff/events.py  2ac8624cc77bdf6f5e259c08568ce635921561df8372ac03ed1f0cedeea3ec3b
src/reasoning_diff/executor.py  481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  5102a7dd0a2d0e99a4941c50cf6705355c83c32fdebb507314a0323ffec57d5b
src/reasoning_diff/models/__init__.py  0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8
src/reasoning_diff/models/adapters.py  c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a
src/reasoning_diff/models/collect.py  509ba704c6c67a037b285e1575a9aa2e73676d088e6393956a5e2d687677e361
src/reasoning_diff/models/features.py  0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0
src/reasoning_diff/models/generate.py  b236dbb63239ddd7b99403df5693773a315a209b1e8e3bb38115ef92d051ba20
src/reasoning_diff/models/tiny.py  21725a183452bd06593789217745202863269cd7e9dea1ec144e4bbdb0a1ddb0
src/reasoning_diff/models/tokenize.py  1bb7d6cf19171a901b5f72e8d7515a830fab8632a08a83ec93244047f916bceb
src/reasoning_diff/probes/__init__.py  3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5
src/reasoning_diff/probes/bilinear.py  52de70553b37dec69822b790b006b7282e58ee926bb77006b3da40b419726e15
src/reasoning_diff/probes/boundary.py  ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034
src/reasoning_diff/probes/calibrate.py  e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334
src/reasoning_diff/repair.py  418d804da3da8bf073b418addc7c34f0bc4ad04a53bd631c9e15270ab43ebc23
src/reasoning_diff/rng.py  2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908
src/reasoning_diff/schema.py  57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7
src/reasoning_diff/scoring.py  8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99
src/reasoning_diff/splits.py  f8b08a69810e32448e6238230a8161e1068ade3b70f2714b81b3a140f15de5ef
src/reasoning_diff/tasks/__init__.py  4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754
src/reasoning_diff/tasks/catalog.py  5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0
src/reasoning_diff/tasks/t1_config.py  e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94
src/reasoning_diff/tasks/t1_fixture.py  01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41
src/reasoning_diff/tasks/t1_official.py  5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b
src/reasoning_diff/tasks/t2_gsm_plus.py  e1a2b4098152857155877a787725fb3c70c2d872446eb14ee79619b2d5d60c81
src/reasoning_diff/tasks/t2_gsm_symbolic.py  b50db6533f18948d141a75a38970b491269a127b990bd818408f29a8e28219af
src/reasoning_diff/tasks/t2_noop.py  850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed
src/reasoning_diff/tasks/t3_hotpot.py  baa832df548138753f383c324630f993b676cac0f1aa5c1df443557cbc18ced9
src/reasoning_diff/tasks/t3_humaneval.py  f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1
src/reasoning_diff/tasks/t3_musique.py  b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895
src/reasoning_diff/tasks/t4_boundary.py  e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2
src/reasoning_diff/transfer.py  d72e1dd1c4192b0936fb661405151447bcb3a100a40d6fb4ba577b8d161b1665
tests/conftest.py  1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1
tests/test_artifacts.py  830953f379954233c76c9aab9f5f4b3860ea598579015a58bddd9909c5bd3278
tests/test_cli_pipeline.py  0cedc6188e5f64b1ad6c97620c8c31ad18a6d8b48e6f511a930e0700f31c31a1
tests/test_generate_loop.py  ffe10b0d6812908ca34f446103b22a23c2e857a85172cc78e72caf005a979a46
tests/test_measure.py  fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab
tests/test_review_regressions.py  37414926677d059610794b4f64ec3bcbf7c242ecce9c563bc8e549abc5d3a60c
tests/test_round03_regressions.py  5698a410c0669b6142f31d5b302ff8c7ef8ec66cc9ef429786d45e2418bfc278
tests/test_round04_regressions.py  93f04cc13c39d6b0a906194ef6ef784642c9f0b7613b7807deb8f7947e08ed56
tests/test_science.py  bed01ffa293f2c1f3d341e9b4ddbf375436eb77fa1a82c5093f12a7a402ca126
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```
