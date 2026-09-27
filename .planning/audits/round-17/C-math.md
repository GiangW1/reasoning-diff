# C：数学与统计独立审查（round-17）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性 \(\sigma(h^\top UV^\top e+b)\)、\(\lambda_{\mathrm{FN}}=10\)、split conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)（拒绝 \(k=\lceil N(1-\alpha)\rceil\)；\(k>N\Rightarrow+\infty\)）、\(S=B\setminus T\) / \(M=T\setminus B\)、有符号 excess、4096→3584 直接迁移 N/A、INLP、C-rand/C-layer 匹配主范数、P1 留出链长+op vs 链长+op+\(\rho\)、P2 配对分母、P3 相对对照。指定猎取 A14-04 / A13-02 / A13-03 / fallback 空 \(N\) / 未知与空分母 / 0-hit vs 缺协议。假说不要求正结果。Gate 保持 `unregistered`（不是缺陷）。不发明 Gate 阈值。不采信 ISSUES 作者 close。不读任何 round-17 其他通道。
- 审查时间：2026-09-21 03:05（UTC+8）
- 审查者 / agent id：`independent-reviewer-C`（round-17 math/stat subagent）
- 审查者上下文：独立 subagent。只读生产代码。未读任何 round-17 的 A/B/D/E/F。`ISSUES.md` 仅作作者声称。结论全部由本轮对磁盘字节的公式推导与手算反例重做；期望值写在 `.planning/audits/round-17/_c_scratch/oracle.py`，**不**由被测单元生成。
- 声明冻结哈希：`3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6`（`.planning/audits/round-17/VERSION.md`，61 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**开审 HASH_MATCH；交卷 HASH_MISMATCH → FAIL**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改 `src/`、`tests/`、`pyproject.toml`（只写本文件与 `.planning/audits/round-17/_c_scratch/`）
- numpy：1.26.4；CPython 3.11.7（Anaconda）

---

## 1. 冻结哈希

范围内文件数：**61**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 18 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「61 files」一致。抽查公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算（开审第一动作；交卷前最后一次同一脚本）：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 时刻 | SHA-256 | 与声明值 |
|---|---|---|
| 开审（第一动作，独立执行 VERSION 脚本） | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` | **HASH_MATCH** |
| 公式攻击执行时 / 交卷前最后一次 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` | **HASH_MISMATCH** |

开审 61 文件等于声明值。本通道未改 `src/`、`tests/`、`pyproject.toml`。写报告期间其他写入者改过树。任务规定 **HASH_MISMATCH → FAIL**。不得把交卷哈希冒充声明冻结 `3d0a0764…`，也不得在已漂汇总上记连续通过。

公式攻击绑定下表 digest（**攻击执行时所读的交卷树**，汇总 `3d0f1c10…`；不是声明冻结）：

| 文件 | SHA-256（本审查绑定） | 行 |
|---|---|---|
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | 337 |
| `measure.py` | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | 405 |
| `transfer.py` | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | 86 |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | 115 |
| `baselines.py` | `3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc` | 125 |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | 45 |
| `probes/bilinear.py` | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | 101 |
| `probes/boundary.py` | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | 44 |
| `cli.py` | `9431b7768fda6a3c3c577f811b747f57f79f57b111dfe89c12281d1d23f95bb5` | 1260 |

`cli.py` 最可能是漂移源（1260 行）。`measure.py` / 探针 / `analysis.py` / `transfer.py` 在本通道两次读盘中内容未再变。开审时未逐文件存档，故不能把交卷树冒充声明冻结 `3d0a0764…`。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `b34ea3e5…` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + NaN 行掩码 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed34…` | `sequence_score`/`conformal_threshold`/`predict_set` | 全文；手算 10 组 \(k\)，含 \((N+1)\) 与 \(N\) 公式分叉 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `ce3b549b…` | Hidden=256；BCE 符号 | 全文 |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a…` | `_auc`/`_fit_scores`/`p1_incremental`/`_bootstrap_p1`/`p2_paired`/`p3_recovery`/`week8_decision` | 全文；独立 IRLS 簇重算 \(\Delta\mathrm{AUC}\) |
| `src/reasoning_diff/transfer.py` | 1–86 | `5549f84b…` | `direct_transfer`/`_pca_project`/`common_dim_then_procrustes` | 全文；\(n=2,d=5/3\) 与 `eye(4)/eye(3)` |
| `src/reasoning_diff/measure.py` | 1–405 | `985b9d93…` | `dependency_densities`/`event_density_sets`/`build_labels`/`_fallback_noise_*` | 全文；A14-04、A13-02、A13-03、fallback |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb88…` | `inlp_remove`/`c_rand_delta`/`c_layer_delta` | 全文 |
| `src/reasoning_diff/baselines.py` | 1–125 | `3d7ec3ba…` | 文本/attention/verbalizer 合同（本通道只核公平划分与未知掩码，不核玩具分数） | 抽查 |
| `src/reasoning_diff/cli.py` | `cmd_label` 554–578；`cmd_analyze` 1065–1162 | `9431b776…` | 无 `p1_table` 不得造 P1；`direct_transfer(4096,3584)`；label 密度 | **实际 CLI** |
| `tests/test_science.py` / `tests/test_round07_regressions.py` | — | 查是否独立锁住指定反例 | 绿测**不是**公式正确性 |

调用链只读：`cli.cmd_label` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

草稿：`.planning/audits/round-17/_c_scratch/{oracle.py,attack.py,hash_freeze.py}`。oracle 只进口 `math`/`numpy`；86 项对照写在 `attack_out.json`。

---

## 3. 独立推导（先公式，后对代码）

原文 / 协议：修订方案 §2.5 / §4.2；REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01 / INLP-01 / DECIDE-01；PITFALLS 校准 / P1 / 有符号 excess / unknown 计入 M / 跨维条。不发明 Gate 阈值。

### 3.1 \(S/M/\rho\) 与有符号 excess

\[
S(s_i)=R_{\mathrm{behavior}}(s_i)\setminus R_{\mathrm{task}}(s_i),\quad
M(s_i)=R_{\mathrm{task}}(s_i)\setminus R_{\mathrm{behavior}}(s_i),
\]

\[
\rho_S(s_i)=\frac{|S(s_i)|}{|P\setminus R_{\mathrm{task}}(s_i)|},\qquad
\rho_M(s_i)=\frac{|M(s_i)|}{|R_{\mathrm{task}}(s_i)|},\qquad
\rho_S(T)=\frac1n\sum_i\rho_S(s_i).
\]

\[
\mathrm{excess}=\mathrm{raw}-\mathrm{noise\_reference}.
\]

分母空 → 密度 null。缺 sham 协议或 `noise_set is None` → excess null（raw 仍可输出）。已评估且 0-hit：\(N=\emptyset\)、\(\rho_S^{\mathrm{noise}}=0\)、excess \(=\) raw，不是缺失。负差不截断。\(\rho_S(T)\) 是事件均值，不是并集一次调用。

PITFALLS 规定例：\(T=\{p1,p2\}\)、\(B=\{p2,p3\}\)、\(P=\{p1,p2,p3,p4\}\) ⇒ \(S=\{p3\}\)、\(M=\{p1\}\)、两密度 \(1/2\)。另：raw \(=0.2\)、noise \(=0.3\) ⇒ excess \(=-0.1\)。

本通道手算对照几何（A14-04 / 0-hit / 映射 \(N\) 共用）：

\[
P=\{p1,p2,p3\},\quad T=\{p1,p2\},\quad B=\{p1,p2,p3\}.
\]

\[
S=\{p3\},\quad |P\setminus T|=1,\quad \rho_S^{\mathrm{raw}}=1,\qquad
M=\emptyset,\quad \rho_M^{\mathrm{raw}}=0.
\]

| 噪声解释 | \(N\) | \(\rho_S^{\mathrm{noise}}\) | \(\rho_M^{\mathrm{noise}}\) | excess\(_S\) | excess\(_M\) |
|---|---|---|---|---|---|
| 映射 \(N=\{p3\}\)（C7-M-01） | \(\{p3\}\) | \(1\) | \(1\) | \(0\) | \(-1\) |
| **已评估 0-hit** | \(\emptyset\) | \(0\) | \(1\) | \(1\) | \(-1\) |
| **缺协议 / `noise_set is None`** | — | null | null | null | null |

A14-04 的错误模式就是把「真实前提 `noise_ref=0`、无 sham」误记成上表第二行。

### 3.2 A14-04：真实前提 `noise_ref=0`、无 sham → excess null

手算错误值（若把 \(N=\emptyset\) 当已评估）：

\[
\rho_M^{\mathrm{noise}}=\frac{|T\setminus\emptyset|}{|T|}=1,\qquad
\mathrm{excess}_M=0-1=-1.
\]

同时 \(\rho_S^{\mathrm{noise}}=0\)、excess\(_S=1\)。正确：`noise_set=None`，noise/excess 全 null，**不是** \(\rho_M^{\mathrm{noise}}=1\) / excess\(=-1\)。

`noise_ref=0` 不是「已评估零命中」。0-hit 只在调用方显式传入 `noise_set=[]` 且 `noise_evaluated=True` 时成立。`build_labels` 对真实前提从不写 `noise_ref=0`（只写 `None`；`0.0` 只出现在 `sham:` 行）。A14-04 打的是 `event_density_sets` 对**已写成 0 的真实行**的解释。

事件路径（有 `event_id`）：`observed=True`（0 不是 None）、`real_hits=[]`（只认 `noise_ref==1`）→ `else: noise_set=None, evaluated=False`。

### 3.3 Fallback：`_fallback_noise_set` / `_fallback_noise_evaluated`

无 `event_id` 时走 fallback。本通道对 A14-04 标签**先读 helper 再喂** `dependency_densities`，不让 UUT 倒推期望：

- `_fallback_noise_set` → `None`（无 mapped `noise_ref==1`）
- `_fallback_noise_evaluated` → **`True`**（`observed` 且无 sham / 无未映射 hit）
- `dependency_densities(..., noise_set=None, noise_evaluated=True)` 仍走 `noise_set is None` 分支 → `noise_set_missing`，**不得**把空列表当已评估 \(N\)

`None` 优先于 `noise_evaluated` 标志。若调用方把 `None` 改写成 `[]` 且保留 `evaluated=True`，会得到上表第二行（excess\(_M=-1\)）。见 C17-U-01。

### 3.4 A13-02：unknown / \(T\not\subseteq K\) → \(M=[]\)，\(\rho_M\) null

PITFALLS：unknown 不得计入 \(M\)。旧失败：\(B=\emptyset\) ⇒ \(M=T\) ⇒ \(\rho_M=1.0\)。

\[
\texttt{behavior\_unknown}\implies M=\emptyset,\;\rho_M^{\mathrm{raw}}=\rho_M^{\mathrm{noise}}=\mathrm{excess}_M=\mathrm{null}.
\]

`event_density_sets`：

\[
\texttt{behavior\_unknown}=\neg K \;\lor\; \bigl(T\neq\emptyset \land T\not\subseteq K\bigr).
\]

\(T=\{p1,p2\}\) 只知 \(p1\) 时也必须 null，不能写成 \(1/2\)。对照：exhaustive + observed_response + no_change ⇒ 确认漏读 \(\rho_M=1.0\)。

### 3.5 A13-03：sham 行不得扣除空 \(N\)

任意 `sham:` 行（含 no-change，`noise_ref=0`）⇒ `noise_set=None`、`evaluated=False` ⇒ excess null。不得记已评估 0 而给出 excess \(=\) raw。对照：无 sham 且显式 `noise_evaluated=True` 的空 \(N\) 才是合法 0-hit。

### 3.6 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b),\quad \lambda_{\mathrm{FN}}=10,\ \mathrm{rank}=64.
\]

\(\mathcal K=\{i:\mathrm{mask}_i\land y_i\in\{0,1\}\}\)；空 \(\mathcal K\) 是 NaN / `no_known_labels`。加权 BCE：

\[
\frac1{|\mathcal K|}\sum_{k\in\mathcal K} w_k\bigl(-y\log p-(1-y)\log(1-p)\bigr),\quad w_k=\lambda_{\mathrm{FN}}\mathbf1[y=1]+1\cdot\mathbf1[y=0].
\]

对 logit 的梯度是 \(w(p-y)\)。手算：\(h=[1,0]\)，\(e=[0,1]\)，\(U=I\)，\(V=\begin{bmatrix}0&1\\1&0\end{bmatrix}\)，\(b=0\) ⇒ logit \(=1\)，\(\sigma(1)=0.7310585786300049\)。\(p=(0.8,0.2)\)，\(y=(1,0)\) ⇒ BCE \(=1.2272895322281534\)。

### 3.7 Split conformal（拒绝 \(k=\lceil N(1-\alpha)\rceil\)）

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)（1-index）；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。\(\hat R=\{j:1-\hat p_j\le q\}\)。

PITFALLS：\(N=4\)、scores \(=\{0.1,0.2,0.3,0.4\}\)、\(\alpha=0.4\) ⇒ \(k=\lceil 5\cdot 0.6\rceil=3\)，\(q=0.3\)。该点 **锁不住** 错公式：\(\lceil 4\cdot 0.6\rceil=3\) 相同。

本通道手算分叉（错公式 \(k'=\lceil N(1-\alpha)\rceil\)）：

| \(N\) | \(\alpha\) | 论文 \(k\) | 错 \(k'\) | \(q\) |
|---|---|---|---|---|
| 4 | 0.4 | 3 | 3 | 0.3 |
| 4 | 0.25 | 4 | 3 | 0.4 |
| 5 | 0.2 | 5 | 4 | 0.5 |
| 10 | 0.1 | 10 | 9 | 1.0 |
| 4 | 0.1 | 5 | 4 | \(+\infty\) |
| 4 | 0 | 5 | 4 | \(+\infty\) |

### 3.8 P1–P3

- **P1：** train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：**每次重算** \(\Delta\mathrm{AUC}\)。禁止 \([\delta]*n\)。假说不要求 \(\Delta\mathrm{AUC}>0\)。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\)；须有 `shared_premises` 且 \(|\mathrm{shared\_premises}|=\) 声称分母。
- **P3：** 相对 C-rand / C-layer；报告非目标与 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

本通道独立 IRLS（不调用 UUT 取期望）：\(n=40\)，`length≡10`，`op~N(0,1000)` seed 7，\(y=1_{i<20}\)，\(\rho=y\)，偶数下标留出，`groups=i//2`，`rng(0)`，\(n_{\mathrm{boot}}=200\)：

\[
\Delta\mathrm{AUC}=0.63,\quad
\mathrm{CI}=[0.10660416666666668,\,0.8542410714285714],\quad
\mathrm{width}=0.7476369047619047.
\]

负向夹具（`precomputed`，基线分数 \(=y\)，\(\rho=1-y\)）：\(\Delta\mathrm{AUC}=-1\)，`status=estimate`。Gate 仍 `unregistered`。

### 3.9 迁移与 S3

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。首批 **4096→3584** 直接模式不适用。附录 S3：不同维先 PCA 到共同维（不是 \(x[:,:k]\)），再 Procrustes。\(n=2\)、\(d\in\{5,3\}\) ⇒ `truncated=True`。`eye(4)[:3]` PCA 到 3 维：\(\|ap-I_3\|_\infty=1.7071067811865477\)，不是前 3 列切片。

### 3.10 INLP / C-rand / C-layer

一步 INLP：\(\hat w=\arg\min\|Hw-y_{\pm1}\|\), \(u=\hat w/\|\hat w\|\), \(P=I-uu^\top\)。手算：\(H=[[2,0],[2,0],[0,1],[0,1]]\), \(y_{\pm1}=(1,1,-1,-1)\) ⇒ \(\hat w=(1/2,-1)\)，\(P=[[4/5,2/5],[2/5,1/5]]\)。C-rand / C-layer 必须缩放到主干预 `target_norm`；缺范数拒绝。

### 3.11 Week-8

Gate 0–2 无预注册阈值 → `unregistered`，**不是缺陷**。有阈值无测量 → 不得标 `evaluated` / pass/fail。`scientific_conclusion` 保持 `None`。本审查不发明阈值。

---

## 4. 已执行检查

独立脚本：`_c_scratch/oracle.py` 先冻结数字，`attack.py` 再对照库与 CLI。**86/86 通过**（攻击绑定交卷树 `3d0f1c10…`）。

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 手算 \(\sigma(1)\) vs `score`/`predict_matrix` | **通过**（标量与矩阵逐位相同） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(1.2272895322281534\) | **通过** |
| CHK-04 | `y=-1` / 空 mask | 直接调用 | **通过**：排除后 \(2.231435513142097\)；空 → NaN |
| CHK-04b | NaN \(H\) 行不进 \(\mathcal K\) | `H[1]=[nan,1]`，`lr=0` | **通过** |
| CHK-05 | `fit` 空 \(\mathcal K\) | `Y=-1` | **通过**：`no_known_labels` |
| CHK-06 | `U00` 有限差 | 解析 \(w(p-y)\) vs \(\pm\varepsilon\) | **通过**：相对误差 \(5.09\times10^{-9}\) |
| CHK-07 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | 10 组；分叉组拒绝错 \(k\) | **通过**（\(N=5,\alpha=0.2\Rightarrow k=5\neq4\)；\(N=4,\alpha=0.25\Rightarrow k=4\neq3\)） |
| CHK-08 | \(\alpha\ge1\)、\(\alpha<0\)、空袋 | 直接调用 | **通过**（`invalid`） |
| CHK-09 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过** |
| CHK-10 | \(a(X)=\max(1-p)\) | `[0.9,0.1,0.8]`，真边 0 | **通过**：\(0.1\)；空真集 \(0\)；未知 `None` |
| HUNT-conf | 拒绝 \(k=\lceil N(1-\alpha)\rceil\) | \(N=5,\alpha=0.2\) | **通过**（论文 \(k=5\)，naive \(k=4\)） |
| CHK-15 | 4096≠3584 无 pad | 库 + `cmd_analyze` | **通过**（`not_applicable_dimension_mismatch`） |
| HUNT-no-slice | 不同隐维不得切片 | `direct_transfer` 保留两维 | **通过** |
| CHK-C7M03-n2 | \(n=2,d=5/3\) | `common_dim_then_procrustes` | **通过**：`truncated=True` |
| CHK-C7M03-eye | `eye(4)/eye(3)` PCA ≠ 切片 | 独立 SVD | **通过**：`truncated=False`，\(\ell_\infty=1.7071067811865477\) |
| CHK-17 | 常数 AUC；平局 | `_auc` | **通过**：常数 0.5；7 严格 + 2 平局 ⇒ \(8/9\) |
| CHK-18 | 留出 logistic | 上节独立 IRLS | **通过**：\(\delta=0.63\) 逐位相同 |
| CHK-20 | 省略 `held_out` | 直接调用 | **通过**（`requires_held_out`） |
| CHK-21 | 簇 bootstrap 重算 \(\Delta\mathrm{AUC}\) | 同 `rng(0)` 独立 IRLS | **通过**：区间逐位相同，宽度 \(0.748\neq0\)，不是 \([\delta,\delta]\) |
| CHK-23 / HUNT-hyp | 假说不要求正 AUC | `precomputed`：基线 \(=y\)，\(\rho=1-y\) | **通过**：\(\Delta\mathrm{AUC}=-1\)，`status=estimate`；`week8` 仍 `unregistered`，`scientific_conclusion is None` |
| CHK-24 | P2 支持集 | `p2_paired` | **通过**：无支持集 / 缺测 / 分母不一致；有支持集 \(\Delta\rho=0.3\)、\(\Delta\mathrm{acc}=-0.2\)（IEEE 误差 \(<10^{-15}\)） |
| CHK-25 | P3 相对对照 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`causal_reverse_claim is False` |
| CHK-26 | PITFALLS \(S/M\)；signed excess；事件均值 | 手算 | **通过**：无 sham → excess null。raw \(0.2\)/noise \(0.3\) ⇒ excess \(-0.1\)。空分母 \(\rho_S\) null。两事件均值 **0.25** |
| CHK-empty-denom | \(P=T\) | 集合 API | **通过**：\(\rho_S\) null，\(M=\{p2\}\)，\(\rho_M=1/2\) |
| CHK-0hit | 已评估空 \(N\) | `noise_set=[]` + `evaluated=True` | **通过**：noise\(_M=1\)，excess\(_M=-1\)（合法 0-hit） |
| CHK-missing-beats-flag | `noise_set=None` 即使 `evaluated=True` | 集合 API | **通过**：`noise_set_missing` |
| CHK-C7M01-api | 映射 \(N=\{p3\}\) | 集合 API | **通过**：excess\(_S=0\)，excess\(_M=-1\) |
| HUNT-A13-02-api | `behavior_unknown=True` | 集合 API | **通过**：\(M=[]\)，\(\rho_M\) 全 null，**不是 1.0** |
| CHK-A1302-confirm | 对照确认阴性 | `behavior_unknown=False` | **通过**：\(\rho_M=1.0\) |
| HUNT-A13-02-partial | \(T\not\subseteq K\) | eds：只知 p1 | **通过**：\(\rho_M\) null，不是 \(0.5\) |
| HUNT-A13-02-prod | `build_labels` 非 exhaustive | 生产路径 | **通过**：`behavior_known=False`，\(\rho_M\) null |
| CHK-A1302-exh | exhaustive no_change | 生产路径 | **通过**：确认漏读 \(\rho_M=1.0\) |
| CHK-A1302-cli | 实际 `label` CLI | 自造 3 前提 Task | **通过**：顶层 `rho_M_raw is None`，\(M=[]\) |
| HUNT-A13-03 | sham no-change | `build_labels` + eds | **通过**：真实 `noise_ref=None`，sham `0.0`；excess null，`noise_set_missing` |
| CHK-A1303-cli | 实际 `label` CLI | 真实 changed + `sham:` no_change | **通过**：excess null |
| **HUNT-A14-04-eds** | 真实前提 `noise_ref=0`，无 sham，\(B\supseteq T\) | 手建 Label + eds | **通过**：\(S=\{p3\}\)，\(M=[]\)，\(\rho_S^{\mathrm{raw}}=1\)，\(\rho_M^{\mathrm{raw}}=0\)，noise/excess **null**，**不是** \(\rho_M^{\mathrm{noise}}=1\) / excess\(=-1\) |
| HUNT-fallback-set | helper 返回值 | 直接调用 | **通过**：`set=None`，`evaluated=True`，`observed=True` |
| **HUNT-fallback-no-book** | helper 输出喂回密度 | `None` + `True` | **通过**：仍 `noise_set_missing`，未记账空 \(N\) |
| **HUNT-A14-04-fallback-eds** | 空 `event_id` 走 fallback | eds | **通过**：与事件路径相同，excess null |
| CHK-C7M02 | 无 `p1_table` | 实际 `analyze` | **通过**：`p1 is None` |
| CHK-C7M02c | 有真 `p1_table` | CLI + 独立 IRLS | **通过**：\(\delta=0.63\)，区间逐位相同 |
| HUNT-cli-gates | 默认 Gate | `analyze` | **通过**：三门 `unregistered`，`scientific_conclusion is None` |
| CHK-28 | TO | LCS 手算 | **通过**：\(0.8\) |
| CHK-29 | INLP \(P=I-uu^\top\) | 上节手算 | **通过**：一步矩阵差 \(<10^{-12}\) |
| CHK-30 | C-rand/C-layer 匹配主范数 | `target_norm=3`；缺范数 | **通过** |
| CHK-31 | Hidden=256；BCE | `hidden=128` 拒绝；\(y=0,z=10\) | **通过**：loss \(10.000045398900186\) |
| CHK-35 | `pytest` 全仓库 | 本审查重跑 | **162 passed**（作者声称 160；本通道独立得到 162，不以作者数为准） |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | 真实 HF 权重属 pending_server；本轮只验证公式与 CLI |
| 阅读任何 round-17 其他通道 | 任务禁止 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用独立同算法区间代替 |
| 对声明冻结 `3d0a0764…` 再跑一遍攻击 | 交卷树已漂；无法在已消失字节上复跑 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮（交卷树 `3d0f1c10…`） | 说明 |
|---|---|---|
| **A14-04** 真实前提 `noise_ref=0`、无 sham → excess null | **关闭（指定反例，非声明冻结）** | eds + fallback + helper 组合均 null，不是 \(\rho_M^{\mathrm{noise}}=1\) / excess\(=-1\)。合法 0-hit 对照仍给出 \(-1\) |
| **A13-02** unknown / \(T\not\subseteq K\) 计入 \(M\) | **关闭（API + 部分覆盖 + 生产 labels + label CLI）** | \(\rho_M\) null；确认 exhaustive 阴性仍为 1.0 |
| **A13-03** sham 空 \(N\) 当已评估扣除 | **关闭（生产 labels + CLI）** | `sham:` ⇒ excess null |
| Fallback 不得把 `noise_set is None` 记成已评估空 \(N\) | **关闭（helper 输出回放）** | `None`+`True` 仍 missing |
| conformal 错一位 \(k=\lceil N(1-\alpha)\rceil\) | **关闭** | 分叉组 \(k\) 与 \(q\) 跟手算一致 |
| 4096→3584 切片 | **关闭（库 + CLI）** | `not_applicable_dimension_mismatch` |
| P1 假说必须为正 | **关闭** | \(\Delta\mathrm{AUC}=-1\) 仍 `estimate` |
| Gate 未注册 | **非缺陷** | 默认 `unregistered` |

这些关闭**绑定交卷树**，**不**转移到声明冻结 `3d0a0764…`。

---

## 7. 发现

对本通道**攻击时所绑定**的 `measure.py 985b9d93…` / `cli.py 9431b776…` 等 digest：无新的 confirmed defect 会污染指定论文数字。A14-04 / A13-02 / A13-03 / fallback / conformal / 跨维 N/A 规定反例在**该**字节上关闭。交卷汇总已不是声明冻结。整体验收因 HASH_MISMATCH 为 FAIL。

指定猎取（本审查实际执行，不采信 ISSUES）：

**A14-04**

- 手算错误：\(T=\{p1,p2\}\)、\(B=\{p1,p2,p3\}\)、\(N=\emptyset\) 已评估 ⇒ \(\rho_M^{\mathrm{noise}}=1\)、excess\(_M=-1\)
- 自造 3 前提 Task（`e1` 父母 `p1,p2`），真实行 `noise_ref=0.0`，无 `sham:`，`sham_protocol` 仍传入
- `event_density_sets`：\(S=\{p3\}\)，\(M=[]\)，raw \(1/0\)，noise/excess **null**，`null_reason=noise_set_missing`
- 空 `event_id` fallback 路径：相同 null，不是 \(\rho_M^{\mathrm{noise}}=1\)
- helper：`_fallback_noise_set=None`，`_fallback_noise_evaluated=True`；二者喂回密度仍 missing
- 对照已评估空 \(N\)：同一几何得到 excess\(_M=-1\)（说明本通道**能**检出该错误值，A14-04 路径没有把它写出来）

**A13-02**

- `behavior_unknown=True`：\(M=[]\)，\(\rho_M\) 全 null
- \(T\not\subseteq K\)：只知 p1 ⇒ null，不是 \(0.5\)
- 生产 `build_labels` 非 exhaustive `no_change`：`behavior_known=False`
- 实际 `label` CLI：顶层 `rho_M_raw is None`
- exhaustive 对照：\(\rho_M=1.0\) 未被过度 null

**A13-03**

- 生产 labels：`sham:ghost.noise_ref=0`，真实前提 `None`
- eds / `label` CLI：excess null，`noise_set_missing`
- 若误记空 \(N\) 已评估，本几何会给出 excess\(_S=1\)

**Fallback**

- 活字节在 `noise_set is None` 时不看 `noise_evaluated`，不会记账空 \(N\)
- helper 标志不一致见 C17-U-01

**Conformal / 迁移 / 假说 / Gate**

- \(N=5,\alpha=0.2\)：库 \(k=5\)，拒绝 naive \(k=4\)
- `direct_transfer(4096,3584)` 与 CLI 均为 N/A，无切片字段
- \(\Delta\mathrm{AUC}=-1\) 保持 `estimate`；三门 `unregistered`

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C17-U-01 | Low | A14-04 下 `_fallback_noise_evaluated` 返回 `True`，而 `_fallback_noise_set` 为 `None` | `measure.py` 313–327 | 现调用方把 `None` 交给密度函数，excess 仍 null。若将来把 `None` 改写成 `[]` 并保留 True，会得到 excess\(_M=-1\) |
| C17-U-02 | Medium | 同一事件同时有映射真实 hit 与 `sham:` 行时，`_has_sham_row` 先丢掉 \(N=\{p3\}\) | `measure.py` 346–351 | 指定 A14-04 / A13-03 不是混合行。默认 `build_labels` 对真实前提保持 `noise_ref=None` |
| C17-U-03 | Low | 矩阵密度 API 把 unknown 编成 `0` 时 \(\rho_M=1.0\) | `measure.py` 167–200 | 生产 label/analyze 走集合 API + `behavior_unknown` |
| C17-U-04 | Low | P2 不在支持集上重算 \(\rho\)；声称 `0.9` 对分母 4 仍 `ok` | `analysis.py` 160–168 | 支持集存在性与整数一致性已关 asked 项 |
| C17-U-05 | Low | 只传 `rng`、不传 `groups` 时 bootstrap 的是 \(\rho\) 均值 | `analysis.py` 87–88 | CLI `analyze` 有表时始终传 `groups` |
| C17-U-06 | Low | `sequence_score` 默认 `nonconformity="prob"`（\(\max p\)）不是命题 2 的 \(\max(1-p)\) | `calibrate.py` 13–26 | CLI calibrate 显式传 `one_minus_p` |
| C17-U-07 | Low | 事件均值聚合不把 `behavior_unknown` 提到顶层 | `measure.py` 112–116 | \(\rho_M\) 已是 null |
| C17-U-08 | Low | 仓库 `test_observed_real_noise_ref_without_sham_does_not_book_empty_n` 用确认阴性（\(B=\emptyset\)）。错记账时空 excess\(_M=0\) 而不是命名的 \(-1\) | `tests/test_round07_regressions.py` | 本通道改用 \(B\supseteq T\) 锁住 \(\rho_M^{\mathrm{noise}}=1\) / excess\(=-1\) |
| C17-U-09 | Low | `test_conformal_examples` 的 \(N=4,\alpha=0.4\) 下两公式同 \(k=3\) | `tests/test_science.py` | 本通道用 \(N=5,\alpha=0.2\) 与 \(N=4,\alpha=0.25\) 锁分叉 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C17-S-01 | 真实轨迹命题 2 覆盖 | 真实 HF 权重 pending_server；tiny 随机权重不是 MODEL-01 |
| C17-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明直接迁移 N/A |
| C17-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）；真实轨迹未跑 |

---

## 10. 非缺陷 / 本轮独立核对通过（交卷树）

1. 双线性评分与 `predict_matrix`；`fit` 梯度有限差 \(\sim 10^{-9}\)
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64；未知哨兵与 NaN \(H\) 行不进 BCE
3. Conformal 论文 \(k\)；分叉组拒绝 \(\lceil N(1-\alpha)\rceil\)；\(k>N\Rightarrow+\infty\)
4. **A14-04：** 真实 `noise_ref=0`、无 sham → excess null，不是 \(\rho_M^{\mathrm{noise}}=1\) / excess\(=-1\)
5. **Fallback：** `noise_set is None` 不记账已评估空 \(N\)
6. **A13-02：** unknown / \(T\not\subseteq K\) → \(\rho_M\) null
7. **A13-03：** `sham:` 空 \(N\) 不扣除
8. 0-hit vs 缺协议可区分；空分母 null；signed excess 不截断
9. `direct_transfer` 与 CLI 拒 4096≠3584，无切片
10. \(n<d\) → `truncated=True`；等行 PCA ≠ 列切片
11. P1 留出 IRLS + 簇重算区间，不是 \([\delta,\delta]\)
12. 假说允许 \(\Delta\mathrm{AUC}=-1\)
13. P2 支持集 / P3 相对对照；`causal_reverse_claim is False`
14. INLP \(P=I-uu^\top\)；C-rand/C-layer 匹配主范数
15. **Week-8：** 默认 `unregistered`（**不是缺陷**）。`scientific_conclusion is None`

---

## 11. 测试质量（仅公式）

作者声称 160 passed。本审查重跑全仓库：**162 passed**。绿测**不能**单独证明公式正确，也不能解释 +2（可能是审查期间测试文件漂移）。

- `test_observed_real_noise_ref_without_sham_does_not_book_empty_n`：**半有效**。锁 `rho_M_noise/excess is None`，但 \(B=\emptyset\) 时错记账的特征是 excess\(_M=0\) 而不是命名的 \(-1\)。本轮用 \(B\supseteq T\) 手算锁 \(-1\)
- `test_unknown_behavior_is_not_counted_as_m`：**有效但只锁非 exhaustive `no_change`**。本轮另锁 API、部分 \(T\)、exhaustive 对照、CLI
- `test_sham_no_change_does_not_book_empty_n`：**有效但偏 \(\rho_M\)**。本轮另锁 \(\rho_S\) 与「若误记空 \(N\) 会得 excess\(_S=1\)」
- `test_conformal_examples`：**有效但锁不住错一位**（\(N=4,\alpha=0.4\) 两公式同 \(k\)）。默认 `sequence_score` 仍是 \(\max p\)。本轮对 `one_minus_p` 与分叉 \(k\) 独立关闭
- `test_direct_transfer_rejects_4096_3584`：**有效**
- `test_p1_bootstrap_interval_is_not_degenerate`：`lo<hi` 能挡 \([\delta,\delta]\)，无独立 oracle。本轮独立 IRLS 对上逐位区间
- `test_week8_never_passes_unregistered`：**有效**
- `test_c7_m01_mapped_noise_premise_is_deducted`：**半有效**。只锁集合 API，不走 eds

---

## 12. 结论

开审冻结哈希 `3d0a0764…` **HASH_MATCH**（61 文件）。公式攻击与独立 pytest（162 passed）跑在交卷树 `3d0f1c10…` 上。交卷前最后一次同一脚本仍为 `3d0f1c10…`，**HASH_MISMATCH**。本通道未改 `src/`、`tests/`、`pyproject.toml`。

对照本轮清单（数字对交卷树成立，不对声明冻结成立）：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\)，未知/NaN 掩码 | **通过** |
| conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)；拒绝 \(\lceil N(1-\alpha)\rceil\)；\(k>N\Rightarrow+\infty\) | **通过** |
| \(S/M/\rho\) 事件均值；signed excess 不截断；空分母 null；0-hit ≠ 缺协议 | **通过** |
| A14-04 真实 `noise_ref=0`、无 sham → excess null，不是 \(\rho_M^{\mathrm{noise}}=1\) / excess\(=-1\) | **通过**（eds + fallback） |
| Fallback `None` 不记账已评估空 \(N\) | **通过**（helper 回放） |
| A13-02 unknown / \(T\not\subseteq K\) → \(\rho_M\) null | **通过** |
| A13-03 sham 空 \(N\) 不得扣除 | **通过** |
| P1 留出 logistic + 簇重算 \(\Delta\mathrm{AUC}\) | **通过**（独立 IRLS 逐位相同） |
| 假说不要求正结果 | **通过**（\(\Delta\mathrm{AUC}=-1\)） |
| 4096≠3584 直接迁移 N/A，不切片 | **通过**（库 + CLI） |
| \(n<d\) truncated vs 维不匹配 | **通过** |
| C-rand/C-layer 范数匹配；INLP \(P=I-uu^\top\) | **通过** |
| Week-8 无阈值 | **通过**（`unregistered`，**不是缺陷**） |

**验收意见：** `FAIL`（`HASH_MISMATCH`）。开审声明冻结 `3d0a0764…` **HASH_MATCH**。指定公式反例在交卷树 `3d0f1c10…` 上独立核对通过（见上表与 §4），但任务规定 HASH_MISMATCH → FAIL。不得把交卷树或本通道攻击结果记为对声明冻结的连续通过。Gate 保持 `unregistered` 不是缺陷。真实轨迹命题 2 / 注册 Gate 仍属 pending_server。

---

## 附录：61 文件 SHA-256（POSIX relpath，仅 file bytes）

下列 digest 为**交卷 / 公式攻击时所读**（汇总 `3d0f1c10…`）。开审汇总曾是声明值 `3d0a0764…`。

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc
src/reasoning_diff/cli.py  9431b7768fda6a3c3c577f811b747f57f79f57b111dfe89c12281d1d23f95bb5
src/reasoning_diff/edits.py  1e5b97d63a62ab78a43ee9db33594a2cc1de3add5ad25aac81007b05af3efb91
src/reasoning_diff/events.py  290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3
src/reasoning_diff/executor.py  481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5
src/reasoning_diff/models/__init__.py  0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8
src/reasoning_diff/models/adapters.py  c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a
src/reasoning_diff/models/collect.py  83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38
src/reasoning_diff/models/features.py  0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0
src/reasoning_diff/models/generate.py  6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173
src/reasoning_diff/models/tiny.py  c75d0f53257666128facbfd1f2ab292edc3a99f9840e617bcce35d59d74c537f
src/reasoning_diff/models/tokenize.py  b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332
src/reasoning_diff/probes/__init__.py  3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5
src/reasoning_diff/probes/bilinear.py  b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9
src/reasoning_diff/probes/boundary.py  ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034
src/reasoning_diff/probes/calibrate.py  e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334
src/reasoning_diff/repair.py  f76ff9998b9a6b1716c0136239fb8ca6cd4e15c17b18a1debaeff6483cf6409b
src/reasoning_diff/rng.py  2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908
src/reasoning_diff/schema.py  57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7
src/reasoning_diff/scoring.py  8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99
src/reasoning_diff/splits.py  40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3
src/reasoning_diff/tasks/__init__.py  4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754
src/reasoning_diff/tasks/catalog.py  bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5
src/reasoning_diff/tasks/t1_config.py  e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94
src/reasoning_diff/tasks/t1_fixture.py  01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41
src/reasoning_diff/tasks/t1_official.py  5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b
src/reasoning_diff/tasks/t2_gsm_plus.py  493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153
src/reasoning_diff/tasks/t2_gsm_symbolic.py  c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276
src/reasoning_diff/tasks/t2_noop.py  850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed
src/reasoning_diff/tasks/t3_hotpot.py  f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe
src/reasoning_diff/tasks/t3_humaneval.py  f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1
src/reasoning_diff/tasks/t3_musique.py  b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895
src/reasoning_diff/tasks/t4_boundary.py  e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2
src/reasoning_diff/transfer.py  5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2
tests/conftest.py  1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1
tests/test_artifacts.py  830953f379954233c76c9aab9f5f4b3860ea598579015a58bddd9909c5bd3278
tests/test_cli_pipeline.py  ff826b3e553f003bf134d1ef9d6c06206a7b836e15c69cd1126bc1ae6d482123
tests/test_generate_loop.py  ffe10b0d6812908ca34f446103b22a23c2e857a85172cc78e72caf005a979a46
tests/test_measure.py  fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab
tests/test_review_regressions.py  c1f0236455f3f087d67a58d56e4f5d9ad7085a3300d591a372f806bb938ab7b3
tests/test_round03_regressions.py  61247e8a074944a33933f5d6cba276745e191cbb22b13d13a8faf19af8d86b01
tests/test_round04_regressions.py  25949c80bbb555851beeaa193e39e3e221759af4c986df8a05d3bdb8e7702666
tests/test_round05_regressions.py  bc837c0c3a6ea3ae440d6c939c210674070ca7bf80ee6c3cb2644d7b04c515a2
tests/test_round06_regressions.py  b555ed24000400e19f84db2ad488698701b664986266254d8e2441e4ebc73084
tests/test_round07_regressions.py  8c23db4b637c8c7013f9f93564ed28d97bd7b7bd1302f72f75089e0ceace29de
tests/test_science.py  cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```
