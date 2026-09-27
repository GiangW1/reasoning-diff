# C：数学与统计独立审查（round-22）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性 \(\sigma(h^\top UV^\top e+b)\)、未知/NaN 掩码、\(\lambda_{\mathrm{FN}}=10\)、split conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)（\(k>N\Rightarrow+\infty\)）、\(S=B\setminus T\) / \(M=T\setminus B\) / 有符号 excess / 空分母 null。指定猎项：**缺 sham 协议或缺 `noise_set` → excess null 不是 0**、**sham/unmapped hit 不得记已评估空 \(N=0\)**、**E 列跟 `task.premises` 不是 labels 首次出现序**、**Procrustes 恢复已知 90° 旋转（独立数值）**、**`attention_mean` 用前提下标（独立数值）**、**4096→3584 直接迁移 N/A**、**P1 留出增量**、**Week-8 / Gate unregistered 不是缺陷**、**假说不要求正结果**。手算微例。期望值由本审查独立 oracle 生成，**不**让被测单元产生期望数字。不发明 Gate 阈值。HASH_MISMATCH → FAIL。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读任何 round-22 的 A/B/D/E/F。`ISSUES.md` 仅作作者声称，不采信 `local close`。r21 A–E 对旧 hash `5097c831…` 的 PASS **不转移**。结论全部由本轮对磁盘字节的公式推导与数值反例重做。
- 声明冻结哈希：`1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（`.planning/audits/round-22/VERSION.md`，61 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**HASH_MATCH**（开审第一动作、攻击脚本启动、攻击结束、交卷前最后一读，四次同一脚本）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改 `src/`、`tests/`、`pyproject.toml`（只写本文件与 `.planning/audits/round-22/_c_scratch/`）
- numpy：1.26.4；CPython 3.11.7（Anaconda）

---

## 1. 冻结哈希

范围内文件数：**61**（`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`）。与 VERSION「61 files」一致。公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 时刻 | 文件数 | SHA-256 | 与声明值 |
|---|---|---|---|
| 开审第一动作（独立执行 VERSION 脚本） | 61 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` | **HASH_MATCH** |
| 公式攻击脚本启动 | 61 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` | **HASH_MATCH** |
| 攻击脚本结束 | 61 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` | **HASH_MATCH** |
| 交卷前最后一读（同一脚本） | 61 | `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` | **HASH_MATCH** |

本通道未改 `src/`、`tests/`、`pyproject.toml`。审查窗口内汇总哈希未漂。公式文件逐文件 digest 开审 = 交卷：

| 文件 | SHA-256 | 行 |
|---|---|---|
| `probes/bilinear.py` | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | 101 |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | 45 |
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | 337 |
| `measure.py` | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | 405 |
| `transfer.py` | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | 86 |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | 115 |
| `baselines.py` | `3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc` | 125 |
| `cli.py` | `cc5eae53d7be27eb87a2813290a5bae0ebda5006ced5897906c3e829d5da2df3` | 1268 |

整树哈希相对 r21 的 `5097c831…` 已变（测试与作者声称的合取锁/oracle 夹具）。r21 PASS 不转移到本树。本轮全部猎项在 `1f5f3798…` 上独立重做。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `b34ea3e5…` | `score` / `predict_matrix` / `fit` / `weighted_bce` | 全文；独立数值 + 有限差 + 哨兵 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed34…` | `sequence_score` / `conformal_threshold` / `predict_set` | 全文；手算 \(k\) 13 组，含能区分缺 \(+1\) 的组 |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a…` | `_auc` / `_fit_scores` / `p1_incremental` / `_bootstrap_p1` / `p2_paired` / `p3_recovery` / `procrustes` / `week8_decision` | 全文；独立 IRLS 簇重算 \(\Delta\mathrm{AUC}\)；独立 90° Procrustes |
| `src/reasoning_diff/measure.py` | 1–405 | `985b9d93…` | `dependency_densities` / `event_density_sets` / `_fallback_noise_*` / `build_labels` | 全文；signed excess + empty-N + unknown/sham/unmapped + fallback 旗标 |
| `src/reasoning_diff/transfer.py` | 1–86 | `5549f84b…` | `direct_transfer` / `_pca_project` / `common_dim_then_procrustes` | 全文；4096≠3584；\(n<d\)；`eye(4)`/`eye(3)` |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb88…` | `c_rand_delta` / `c_layer_delta` / `inlp_remove` / `scale_to_norm` | 全文；范数锁 + \(I-\hat Z\hat Z^\top\) |
| `src/reasoning_diff/baselines.py` | 1–125 | `3d7ec3ba…` | `attention_mean` 前提下标为指定猎项；其余只读对照 | `attention_mean` 独立数值；不发明评分 |
| `src/reasoning_diff/cli.py` | `cmd_fit` / `cmd_calibrate` / `cmd_analyze` / `cmd_label` / `_find_tasks_jsonl` / `_e_premise_ids` | `cc5eae53…` | 列身份、缺任务文件、假 P1、label 记账 | **实际 CLI 反例** |

调用链只读：`cli.cmd_fit` / `cmd_calibrate` / `cmd_analyze` / `cmd_label`。未覆盖：模型 hook/KV、数据适配器、executor。`card` / `forbid_host_exec` / `apply_model_template` 属 F 工程猎项，不进本通道公式结论。

草稿：`.planning/audits/round-22/_c_scratch/_c_scratch_math.py`（独立 oracle 先算期望，再比生产）、`_c_scratch_out.json`、`_c_hash.py`。

---

## 3. 独立推导（先公式，后对代码）

原文 / 协议：REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01 / INLP-01 / DECIDE-01；PITFALLS \(\rho_S,\rho_M\)、conformal Appendix D。不发明 Gate 阈值。

### 3.1 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b)=\sigma(\langle h_i U,\,e_j V\rangle+b),\quad
(HU)(EV)^\top\text{ 为矩阵形式}.
\]

默认 \(r=64\)，\(\lambda_{\mathrm{FN}}=10\)。已知集 \(\mathcal K=\{(i,j):\mathrm{mask}_{ij}\land y_{ij}\in\{0,1\}\land h_i,e_j\text{ 有限}\}\)；空 \(\mathcal K\) 是 NaN / `no_known_labels`，不是 0。加权 BCE 对正类乘 10。未知哨兵 \(y\notin\{0,1\}\) 与 NaN 行不进损失。

手算：\(p=(0.8,0.2)\)，\(y=(1,0)\) ⇒ \(\mathrm{BCE}=5.5(-\ln 0.8)=1.2272895322281534\)。\(y=-1\) 排除后只剩 \(10(-\ln 0.8)=2.231435513142097\)。

### 3.2 Split conformal 与 \(a(X)\)

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)（0-index `arr[k-1]`）；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)（代码对 \(q\) 加 `1e-12`）。

离一错误：\(k=\lceil N(1-\alpha)\rceil\)（缺 \(+1\)）。能区分的组：

| \(N,\alpha\) | 论文 \(k\) | 缺 \(+1\) 的 \(k\) | 论文 \(q\)（给定排序袋） |
|---|---|---|---|
| \(4,0.25\) | 4 | 3 | \(s_{(4)}=0.4\) 不是 \(0.3\) |
| \(5,0.2\) | 5 | 4 | \(s_{(5)}=0.55\)（本轮袋）不是第 4 项 |
| \(6,1/6\) | 6 | 5 | \(s_{(6)}=0.3\) 不是 \(0.25\) |
| \(8,0.2\) | 8 | 7 | \(s_{(8)}=0.24\) 不是第 7 项 |
| \(10,0.1\) | 10 | 9 | \(s_{(10)}=0.20\) 不是第 9 项 |
| \(4,0.1\) / \(4,0\) / \(1,0\) | \(N+1\) | \(N\) | \(+\infty\) 不是袋内最大 |

另一错误：`arr[k]` 而不是 `arr[k-1]`。\(N=4,\alpha=0.4,k=3\) 时论文 \(q=s_{(3)}=0.3\)，错索引会吃到 \(0.4\)。

规定反例：\(\hat p=(0.9,0.1,0.8)\)，\(E=(p1,p2,p3)\)，\(R=\{p1\}\) ⇒ \(a=1-0.9=0.1\)。若误用首次出现序 \([p3,p2,p1]\)，p1 下标 2，吃到 \(0.8\)，得 \(0.2\)。

### 3.3 \(S/M/\rho\) 与有符号 excess

\[
S=B\setminus T,\quad
M=T\setminus B,\quad
\rho_S=\frac{|S|}{|P\setminus T|},\quad
\rho_M=\frac{|M|}{|T|},\quad
\mathrm{excess}=\mathrm{raw}-\mathrm{noise\_reference}.
\]

分母空 → N/A。**缺 sham 协议或 `noise_set is None` → excess null，不是 0。** 已评估且 0-hit（`noise_set=[]` 且 `noise_evaluated=True`）：\(N=\emptyset\)、noise \(=0\)、excess \(=\) raw。负差不截断。\(\rho_S\) 事件均值。

PITFALLS：\(T=\{p1,p2\}\)、\(B=\{p2,p3\}\)、\(P=\{p1,p2,p3,p4\}\) ⇒ \(S=\{p3\}\)、\(M=\{p1\}\)、两密度 \(1/2\)。另：raw \(=0.2\)、noise \(=0.3\) ⇒ excess \(=-0.1\)。两事件 \(\rho_S\in\{1/2,0\}\) ⇒ 均值 \(0.25\)。

**empty-N booking：** \(T=B=\{p1\}\) 且错误地记 \(N=\emptyset\) evaluated ⇒

\[
\rho_M^{\mathrm{noise}}=\frac{|T\setminus\emptyset|}{|T|}=1,\qquad
\mathrm{excess}_M=0-1=-1.
\]

该危险记账只应出现在**显式** `noise_set=[]` 且 `noise_evaluated=True` 的 0-hit 协议。`sham:` 行、unmapped hit、真实前提 `noise_ref=0` 且无 `sham:`、未观察，都不得走这条。

### 3.4 unknown not M

\(M=T\setminus B\) 把未知前提当成「不在 \(B\)」，会把未扫全的任务祖先记成 miss，抬高 \(\rho_M\)。正确：任务祖先未全部 `behavior_known` 时 \(M=\emptyset\)，\(\rho_M\) 三列 null。\(S\) 仍可按已观察正类计算。

规定反例：\(T=\{p1,p2\}\)，\(B=\{p2\}\)。已知路径 \(M=\{p1\}\)、\(\rho_M=1/2\)。未知路径 \(M=\emptyset\)、\(\rho_M\) 全 null。生产 `build_labels`：`no_change` 且非 `exhaustive` → `behavior_known=False`。

### 3.5 sham / unmapped 不得记已评估空 \(N\)

任意 `sham:` 行（含 `noise_ref=0` 的 miss，以及 sham-only hit）不得把 \(N=\emptyset\) 且 `noise_evaluated=True` 记成已评估 0。已知 \(T=B=\{p1,p2\}\) 时 \(\rho_M=0\)，错误空 \(N\) 会扣出 \(\mathrm{excess}_M=-1\)。正确是 `noise_set` 缺失、excess null。

前提不在 \(P\) 内、`noise_ref=1` 的 **unmapped hit** 同样不得走已评估空 \(N\)。正确仍是 `noise_set=None`、`null_reason=noise_set_missing`。

### 3.6 fallback 旗标 vs excess

`event_density_sets` 在 `event_id` 全空时走 `_fallback_noise_*`。对真实前提 `noise_ref=0`、无 `sham:`、无 mapped hit、`observed=True`：

- 事件路径：`noise_set=None`，`evaluated=False`
- fallback：`noise_set=None`，`evaluated=True`

`dependency_densities` 先判断 `noise_set is None`，两条都给出 `null_reason=noise_set_missing`、excess null。旗标不一致，**当前数字一致**。若以后把 `None + evaluated=True` 收成空 \(N\) 已评估，就会触发 §3.3 的 \(\mathrm{excess}_M=-1\)。

### 3.7 P1；假说不要求正增量

train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题上 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：重采样基础题，**每次重算** \(\Delta\mathrm{AUC}\)。禁止把点估计复制 \(n\) 次得到 \([\delta,\delta]\)。

\(\Delta\mathrm{AUC}<0\) 仍是 `estimate`，不是失败/拒绝。注意：\(\rho=1-y\) 不够，logistic 可学负系数仍得正 AUC。本审查用手造：train \(\rho=y\)、held-out \(\rho=1-y\)，常数 length/op ⇒ 基线 AUC \(=1/2\)，完整模型在留出上反向排序 AUC \(=0\)，\(\Delta=-1/2\)。

无 `p1_table.jsonl` 时 analyze 必须 `p1=None`。

### 3.8 迁移：4096→3584 N/A 与 \(n<d\) truncated

维不等 ⇒ `direct_transfer` 状态 `not_applicable_dimension_mismatch`，禁止 pad/truncate。首批 **4096→3584** 直接模式明确不适用。这与共同维适配的 `truncated` **不是同一个门**：

- \(n<\min(d_A,d_B)\) ⇒ `truncated=True`，`not_applicable_too_few_rows`
- \(n=\dim\)（`eye(4)` vs `eye(3)`：\(n=\min(4,3)=3=\dim\)）⇒ `truncated=False`
- 附录 S3：不同维先 PCA 到共同维，再 Procrustes；不得静默 `x[...,:k]`

### 3.9 正交 Procrustes 恢复已知 90° 旋转

\[
\min_R\|AR-B\|_F,\quad R^\top R=I,\qquad
A^\top B=U\Sigma V^\top\Rightarrow R=UV^\top.
\]

行向量约定下，顺时针 90° 为 \(R_{\mathrm{cw}}=\begin{bmatrix}0&-1\\1&0\end{bmatrix}\)，逆时针 90° 为 \(R_{\mathrm{ccw}}=\begin{bmatrix}0&1\\-1&0\end{bmatrix}\)，绕 \(z\) 的三维 90° 为 \(\mathrm{diag}(R_{\mathrm{cw}},1)\)。对本审查独立源点（`default_rng(20260921)`，**不是**单测三角 \(\{(1,0),(0,2),(1,1)\}\)）应逐位恢复 \(R\)，且 \(\det R=+1\)、\(\|AR-B\|_\infty\sim 10^{-16}\)。形状不等 → `not_applicable_shape_mismatch`。同宽 `common_dim_then_procrustes` 走 identity 再同一 Procrustes。

### 3.10 `attention_mean` 用前提下标

\[
\mathrm{attention\_mean}(W,I)=\mathrm{mean}(W_{\ldots,I}).
\]

空 \(W\) 或空 \(I\) → 0。独立权重（**不是**单测行 \([0.1,0.8,0.1]\)）

\[
W=\begin{bmatrix}0.05&0.91&0.22&0.40\\0.12&0.77&0.33&0.18\end{bmatrix},\quad I=\{1,3\}
\]

期望 \(\mathrm{mean}\{0.91,0.40,0.77,0.18\}=0.565\)。全体 token 均值 \(0.3725\)、末列均值 \(0.29\) 必须能被区分。

### 3.11 C-rand / C-layer / INLP

C-rand 与 C-layer 必须把 \(\Delta\) 缩放到**主干预实际范数**；缺范数拒绝。INLP 逐步 \(u_t=\mathrm{normalize}(w_t)\)，\(P\leftarrow P(I-u_tu_t^\top)\)。在已投影残差上拟合且 \(u_t\) 彼此正交时

\[
P=\prod_t(I-u_tu_t^\top)=I-\hat Z\hat Z^\top,\quad \hat Z=[u_1,\ldots,u_T].
\]

一步手算：\(H=[[2,0],[2,0],[0,1],[0,1]]\)，\(y_{\pm1}=(1,1,-1,-1)\) ⇒ \(\hat w=(1/2,-1)\)，\(P=[[4/5,2/5],[2/5,1/5]]\)。二维满秩后的额外步会再收进非正交数值方向；此时朴素 \(I-Z_{4}Z_{4}^\top\) 不再等于逐步积，但逐步 \(P\) 仍等于两步正交投影。

### 3.12 Week-8 / Gates unregistered

Gate 0–2 无预注册阈值 → `unregistered`，**不是缺陷**。有阈值无测量 → 不得标 `evaluated` / pass/fail。`scientific_conclusion` 保持 `None`。本审查不发明阈值。假说（P1 正增量、C3 正 excess）不是必须出现的正结果。

---

## 4. 已执行检查

期望值全部由 `_c_scratch_math.py` 内独立 oracle 先算，再调用生产函数比较。83/83 通过。

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix`（`rng(22)`） | **通过**。矩阵逐位相同；24 对 `score` 最大绝对差 \(2.22\times10^{-16}\)；首对 \(p=0.8450377988830485\) |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | 手算 \(5.5(-\ln 0.8)=1.2272895322281534\) | **通过**（逐位相同） |
| CHK-04 | `y=-1` / 空 mask | 手算 \(10(-\ln 0.8)=2.231435513142097\) | **通过**；空 mask → NaN |
| CHK-05 | `fit` 空 \(\mathcal K\) | `Y=-1` | **通过**：`no_known_labels`，`loss=None` |
| CHK-06 | `U00` 有限差 | 独立损失 \(\pm\varepsilon\) vs 一步隐含梯度 | **通过**：数值 \(-0.03936675052607086\) vs 隐含 \(-0.03936675042878532\)，相对误差 \(2.47\times10^{-9}\) |
| CHK-07 | \(\hat p=(0.9,0.1,0.8)\) 重建 | \(U=V=I\)，\(H=\mathrm{logit}\) 行，\(E=I_3\) | **通过**（\(\sim10^{-16}\)） |
| CHK-08 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | 手算 13 组 vs `conformal_threshold` | **通过**。能区分缺 \(+1\)：\(N=4,\alpha=0.25\Rightarrow q=0.4\) 不是 \(0.3\)；\(N=5,\alpha=0.2\Rightarrow q=0.55\)；\(N=6,1/6\Rightarrow q=0.3\)；\(N=8,\alpha=0.2\Rightarrow q=0.24\)；\(N=10,\alpha=0.1\Rightarrow q=0.20\)。\(N=4,\alpha=0.4\) 袋 \([0.1,0.2,0.3,0.4]\) ⇒ \(k=3,q=0.3\)；移位袋 \(q=0.25\)。\(k>N\)（\(\alpha=0.1/0/0.05\)，\(N=1,\alpha=0\)）⇒ \(+\infty\)。未排序 \([0.25,0.45,0.05]\)，\(\alpha=1/3\Rightarrow q=0.45\)。13 组中 10 组 \(k_{\mathrm{paper}}\ne\lceil N(1-\alpha)\rceil\) |
| CHK-09 | \(\alpha\ge1\)、\(\alpha<0\)、空袋 | 直接调用 | **通过**（`invalid`） |
| CHK-10 | \(1-0.7\le 0.3\)；\(q=+\infty\) | `predict_set` | **通过**（`+1e-12` 后 True；无穷阈值全收） |
| CHK-11 | 库函数 \(a(X)\) | `[0.9,0.1,0.8]` | **通过**：列 0 → \(0.1\)；列 1 → \(0.9\)；空真集 → \(0\)；未知标签 → `None` |
| CHK-12 | 规定反例（实际 `cmd_calibrate`） | \(E=I_3\)；labels 行序 \([p3,p2,p1]\)；`Task.premises` \([p1,p2,p3]\)；祖先 \(\{p1\}\) | **通过**。CLI `scores=[0.10000000000000009]`（**不是** \(0.2\)）。独立 \(N=1,\alpha=0.4\Rightarrow k=2>N\)，落盘 `infinity` |
| CHK-13 | 仅 p2 labels（实际 CLI） | 同上 pred；祖先 \(\{p2\}\) | **通过**：CLI `scores=[0.9]` |
| CHK-16 | 缺 `tasks.jsonl` | 孤立 feat + 祖先 `col/tasks.jsonl` 对调前提 | **通过**。fit/calibrate 均 `ValueError`；`_find_tasks_jsonl` 为 `None` |
| CHK-18 | 父目录 `col/` | `col/feat` 对 `col/tasks.jsonl` | **通过**。`_find_tasks_jsonl` 为 `None`；fit raise |
| CHK-E | `_e_premise_ids(task, [p3,p2,p1])` | 独立对照 | **通过**：`[p1,p2,p3]`。`None` 任务仍返回首次出现序（残留 C22-U-02） |
| CHK-19 | P1 bootstrap 是否重算 \(\Delta\mathrm{AUC}\) | \(n=36\)，独立 IRLS 簇重算，同一 `rng(22)` | **通过**：区间 \([0.08357142857142864, 0.8125578703703704]\)，宽度 \(0.7289864417989418\)，均值 \(0.43238871751886454\)，点估计 \(\delta=0.4444\ldots\)，`auc_base=0.555\ldots`，`auc_full=1`。独立同算法区间、均值 **逐位相同**。bootstrap 头五个 \(\Delta\) 互异，不是 \([\delta,\delta]\) |
| CHK-19b | `cmd_analyze` + `p1_table.jsonl` | 同上表；CLI 合同种子 `rng(0)` | **通过**：独立 seed-0 区间 \([0.126948051948052, 0.833482142857143]\)，均值 \(0.4532238056746762\)，与 CLI **逐位相同** |
| CHK-20a | 默认拒绝无留出 | 省略 `held_out` | **通过**：`requires_held_out` |
| CHK-20b | 负增量仍估计 | train \(\rho=y\)、held-out \(\rho=1-y\)，常数 length/op | **通过**。独立 \(\Delta=-0.5\)（基线 \(0.5\)、完整 \(0\)）；代码 `status=estimate`，\(\delta=-0.5\) |
| CHK-21 | 常数 AUC；平局 | `_auc` | **通过**：常数 \(0.5\)。分数 \([1,2,2,3]\) vs \([0,0,1,1]\) 手算 \(0.875\) |
| CHK-22 | signed excess；0-hit；空分母；事件均值；缺协议/缺 `noise_set` | 独立集合 oracle vs `dependency_densities` | **通过**：raw \(0.2\)、noise \(0.3\)、excess \(-0.1\) 不截断。0-hit ⇒ `noise=0`、`excess=raw=1`。空分母 ⇒ `rho_S` null。两事件 \(1/2\) 与 \(0\) ⇒ 均值 **0.25**。PITFALLS \(S=\{p3\}\)、\(M=\{p1\}\)、密度 \(1/2\)。缺协议 ⇒ `sham_protocol_missing`、excess **null 不是 0**。缺 `noise_set` ⇒ `noise_set_missing`、excess **null 不是 0**（raw 仍 \(1.0\)） |
| CHK-EN | **empty-N booking** | 独立：\(T=B=\{p1\}\)、\(N=\emptyset\) ⇒ \(\mathrm{excess}_M=-1\) | **通过对照**。API `[]`+`evaluated=True` **会**记账 \(-1\)（危险形态，仅作 0-hit 协议）。`[]`+`evaluated=False` → `noise_set_empty`、excess null |
| CHK-A13-02 | **unknown not M** | API 开关；生产 `build_labels`；实际 `cmd_label` | **通过**。`behavior_unknown=True` ⇒ \(M=[]\)，\(\rho_M\) 三列 null；对照已知 \(M=\{p1\}\)、\(\rho_M=0.5\)。CLI label 相同 |
| CHK-A13-03 | **sham empty N** | `sham:x` miss `noise_ref=0`；生产 + `cmd_label` | **通过**。真实前提 `noise_ref is None`；`null_reason=noise_set_missing`；未出现 \(\mathrm{excess}_M=-1\)。CLI：`sham:x=0`，`p1`/`p2` 为 `None` |
| CHK-C7 | mapped / sham-only hit | 构造 `Label(noise_ref=1)`；双前提 + sham hit | **通过**。mapped \(N=\{p3\}\) excess\(_S=0\)。sham-only hit：excess null，不是 evaluated-zero |
| CHK-UNMAP | **unmapped hit** | `premise_id=ghost`、`noise_ref=1` | **通过**。`null_reason=noise_set_missing`，excess/noise 全 null，**不是** 已评估空 \(N\) |
| CHK-A14-04 | 真实 `noise_ref=0` 无 sham | 构造 Label | **通过**。\(\rho_M=0\) 但 excess/noise null，**不是** \(-1\) |
| CHK-FB | **fallback 旗标 vs excess** | 空 `event_id` + `noise_ref=0` | **旗标不一致，数字仍 null**。`_fallback_noise_set is None` 且 `_fallback_noise_evaluated is True`。excess 仍 `noise_set_missing`。fallback mapped 仍扣除，excess\(_S=0\) |
| CHK-24 | analyze 标签冒充 P1 | 6 行含伪造 `length/op/rho/y`，无 `p1_table` | **通过**：`report["p1"] is None`，三门 `unregistered`，`scientific_conclusion is None`。同时 `transfer` 为 4096/3584 N/A |
| CHK-25 | **\(n<d\) vs dim mismatch** | \((2,5)/(2,3)\)；`eye(4)`/`eye(3)` | **通过**。前者 `truncated=True`，`not_applicable_too_few_rows`，**不是** `dimension_mismatch`。后者 `truncated=False`，`adapted_geometry` |
| CHK-26 | S3 非切片；4096≠3584 | \(n=20,d=8/5\)；`direct_transfer`；`cmd_analyze` | **通过**：`a_map=pca` vs 切片最大差 \(3.82\)；库与 CLI 均为 `not_applicable_dimension_mismatch` |
| CHK-PROC | **90° 旋转恢复** | 独立源 `rng(20260921)` 的 \(9\times2\) / \(11\times3\)；独立 SVD oracle | **通过**。顺/逆时针 \(\|R-R_{\mathrm{true}}\|_\infty=2.22\times10^{-16}\)，相对独立 oracle \(0\)，重建 \(4.44\times10^{-16}\)，\(\det\approx 1\)。绕 \(z\) 同量级。形状不等 → N/A。同宽 `common_dim` identity 后同样恢复 |
| CHK-ATT | **`attention_mean` 前提下标** | 独立 \(2\times4\) 与 1D 袋 | **通过**。\(I=\{1,3\}\) → \(0.565\)（全体均值 \(0.3725\)、末列 \(0.29\) 可区分）。1D → \(0.755\)（全体 \(0.336\)）。空 \(W\) / 空 \(I\) → \(0\) |
| CHK-27 | Week-8 无发明门 | 默认 / 有阈无测 / 有阈有测 | **通过**：默认三门 `unregistered`（**不是缺陷**）。有阈无测 → `threshold_present_measurement_missing`。`rho_S_excess=0.1` vs \(0.9\) → `compared/below` |
| CHK-28 | P2 asked 项；P3 对照 | 直接调用 | **通过**：无支持集 → `denominator_unverified`；`None` + 匹配列表 → `missing_pair`；`99` vs 1 元列表 → `denominator_inconsistent`。`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`causal_reverse_claim is False` |
| CHK-INLP | \(P=I-\hat Z\hat Z^\top\) | 一步手算 + 两步正交 + 四步逐步积 | **通过**：一步 \(P\) 与 \([[0.8,0.4],[0.4,0.2]]\) 一致。两步 \(\|P-(I-\hat Z\hat Z^\top)\|_\infty=3.04\times10^{-17}\)，\(\hat Z^\top\hat Z=I\)。四步逐步积与两步差 \(1.14\times10^{-16}\)；朴素四列 \(I-Z_4Z_4^\top\) 差 \(1.0\)（见 C22-U-03） |
| CHK-CRAND | C-rand/C-layer 范数 | 主干预 \(\|\Pi_Z(h_d-h_b)\|=5\) | **通过**：两路 `actual_norm=5`。缺范数 `ValueError`。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0` |
| CHK-29 | `pytest` | 全仓库 | **172 passed**。与作者声称一致。绿测**不能**单独证明公式 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1 | 真实 HF 权重属 pending_server |
| 阅读其他 round-22 通道 | 任务禁止 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用独立同算法区间代替 |
| 发明 Gate 0–2 阈值并判 pass/fail | DECIDE-01：未注册保持 `unregistered`，不是缺陷 |
| `card` / `forbid_host_exec` / `apply_model_template` | 属 F 工程猎项，不是本通道公式 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger / 猎项 | 本轮绑定字节 | 说明 |
|---|---|---|
| conformal \(k\)；\(k>N\Rightarrow+\infty\)；off-by-one | **关闭** | CHK-08/09。13 组中 10 组能区分缺 \(+1\) |
| 双线性形式 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | **关闭** | CHK-01–07 |
| signed excess 不截断；0-hit noise=0 | **关闭（集合 API）** | CHK-22 |
| 缺 sham 协议 / 缺 `noise_set` → excess null 不是 0 | **关闭** | CHK-22f/22g |
| **empty-N booking**（sham / unmapped / `noise_ref=0` 不得走 `[]`+evaluated） | **关闭** | CHK-EN + A13-03 + UNMAP + A14-04。危险记账只在显式 API 0-hit |
| **unknown not M** | **关闭**（库 + `cmd_label`） | CHK-A13-02。\(\rho_M\) 全 null |
| **sham / unmapped empty N** | **关闭**（库 + `cmd_label`） | CHK-A13-03 / CHK-UNMAP。未出现 excess\(_M=-1\) |
| E 列跟 `task.premises` | **关闭（有任务文件）** | CHK-E + CHK-12。首次出现序残留只在 `task is None` |
| Procrustes 恢复已知 90° | **关闭** | CHK-PROC。独立源，不是单测三角 |
| `attention_mean` 前提下标 | **关闭（库函数）** | CHK-ATT。独立权重，能区分全体/末列均值 |
| **fallback 旗标 vs excess** | **旗标残留，数字关闭** | CHK-FB。excess 仍 null。见 C22-U-01 |
| 负 \(\Delta\mathrm{AUC}\) 仍估计 | **关闭** | CHK-20b。\(\Delta=-0.5\) 仍 `estimate` |
| P1 bootstrap 重算 \(\Delta\mathrm{AUC}\) | **库 + CLI 有表路径关闭** | CHK-19 / 19b。独立区间逐位相同 |
| analyze 标签冒充 P1 | **关闭** | CHK-24。`p1 is None` |
| **\(n<d\) truncated vs 4096→3584 dim mismatch** | **关闭** | CHK-25/26。两门不混用 |
| C-rand/C-layer 范数；INLP \(I-\hat Z\hat Z^\top\) | **关闭（库函数）** | CHK-CRAND / CHK-INLP。两步正交身份成立 |
| Gate 未注册 | **不是缺陷** | CHK-27 |

---

## 7. 发现

本轮**没有新的公式 confirmed defect**。声明冻结整树哈希四次 MATCH。指定猎项在绑定字节上独立关闭或（fallback 旗标）降为残留。

指定攻击（本审查实际执行，不采信 ISSUES）：

- \(\hat p=\sigma(\mathrm{logit}(0.9,0.1,0.8))\)，\(E=I_3\) 对应 \((p1,p2,p3)\)
- labels 磁盘行序 \([p3,p2,p1]\)；`Task.premises` 序 \([p1,p2,p3]\)；祖先 \(\{p1\}\)
- 论文 \(a=1-0.9=0.1\)；首次出现序会得 \(0.2\)
- **当前 `cmd_calibrate`：`scores=[0.10000000000000009]`**（不是 \(0.2\)）；\(k=2>N\) → infinity
- 仅 `{p2}`：CLI \(a=0.9\)
- empty-N：API `[]`+evaluated 得 \(\mathrm{excess}_M=-1\)；`sham:` miss / unmapped hit / 真实 `noise_ref=0` **不**走该记账
- unknown：\(M=[]\)，\(\rho_M\) 三列 null（API + `build_labels` + `cmd_label`）
- fallback：`noise_set is None` 且 `evaluated=True`；两边 excess null
- conformal：\(N=4,\alpha=0.25\Rightarrow q=0.4\)（缺 \(+1\) 会给 \(0.3\)）；\(N=10,\alpha=0.1\Rightarrow q=0.20\)（缺 \(+1\) 会给第 9 项）
- \(n<d\)：`(2,5)/(2,3)` → `truncated=True`，状态不是 dim-mismatch；`eye(4)`/`eye(3)` → `truncated=False`
- 4096→3584 直接迁移：`not_applicable_dimension_mismatch`（库 + `cmd_analyze`）
- P1：负增量 \(\Delta=-0.5\) 仍 `estimate`（假说不要求正结果）
- Procrustes：独立 \(9\times2\) 源恢复顺/逆时针 90°，\(\ell_\infty=2.22\times10^{-16}\)
- `attention_mean`：独立 \(W,I=\{1,3\}\) 得 \(0.565\)，不是全体 \(0.3725\)
- Gates：默认 `unregistered`，`scientific_conclusion is None`

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C22-U-01 | Low | fallback 在真实 `noise_ref=0`、无 sham 时设 `noise_set=None` 且 `evaluated=True`；事件路径同输入是 `evaluated=False` | `measure.py` 313–360 | 猎项数字是 excess null。`noise_set is None` 先短路，当前不会空 \(N\) 扣噪。潜在：若以后把 `None+True` 收成已评估空集，会再现 \(\mathrm{excess}_M=-1\) |
| C22-U-02 | Low | `_e_premise_ids(None, labels)` 仍返回首次出现序。本审查 `labels=[p3,p2,p1]` 得 `[p3,p2,p1]` | `cli.py` 731–740 | 生产 `cmd_fit` / `cmd_calibrate` 在缺文件且有 labels 时先 `ValueError` |
| C22-U-03 | Low | 维数耗尽后继续 INLP 步会收进非正交数值 \(u_t\)；朴素 \(I-Z_4Z_4^\top\) 与逐步积差 \(1.0\) | `interventions.py` 52–67 | 论文身份要求正交 \(\hat Z\)。两步 \(\hat Z^\top\hat Z=I\) 且 \(P=I-\hat Z\hat Z^\top\)。四步逐步积仍等于两步（\(\ell_\infty\sim10^{-16}\)） |
| C22-U-04 | Low | `sequence_score` 默认 `nonconformity="prob"` 是 \(\max p\) | `calibrate.py` 24–26 | CLI 始终传 `one_minus_p` |
| C22-U-05 | Low | calibrate 仍 `task_label==1 or behavior_label==1`，且 `rsi` 含 `{nid}` | `cmd_calibrate` | 本轮主问列身份与 \(k\)。任务/行为应分头校准 |
| C22-U-06 | Low | \(n=\dim\) 时中心化 PCA 秩 \(\le n-1\)，`eye(4)`/`eye(3)` 仍 `truncated=False` | `transfer.py` 76–86 | 指定猎项要求该例 **保持** `truncated=False`。门是 \(n<\dim\)，不是中心化数值秩 |
| C22-U-07 | Low | mapped hit **同时**存在 `sham:` 行时 sham 分支优先，整事件 excess null | `measure.py` 349–351 | 指定两刀是「纯 mapped」与「纯 sham」。混合未列入关闭条件 |
| C22-U-08 | Low | `build_labels` 只给 `sham:` 前提写 `noise_ref`；真实前提恒 `None`。生产 label 到不了 mapped \(N=\{p3\}\) | `measure.py` 72–80 | mapped 反例是构造 `Label(noise_ref=1)`。该路径 excess=0 |
| C22-U-09 | Low | 只传 `rng`、不传 `groups` 时仍 bootstrap \(\rho\) 均值 | `analysis.py` 87–88 | 正确 `p1_table` 路径传 `groups`。analyze 无表则 `p1 is None` |
| C22-U-10 | Low | fixture `cmd_fit` 写 `attention_mean(np.zeros((0,)), [])` → \(0\) | `cli.py` 672 | 库函数猎项已用独立 \(W,I\) 关闭。CLI 空图 0 不是前提下标均值 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C22-S-01 | 真实轨迹命题 2 覆盖 | 真实 HF 权重 pending_server；tiny 不是 MODEL-01 |
| C22-S-02 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）。库层 bootstrap 现可重算 \(\Delta\mathrm{AUC}\)；analyze 无表不再伪造 P1 |
| C22-S-03 | 4096↔3584 适配后的双线性 | 直接迁移 N/A 已对；共同维在 \(n\) 足够时为 PCA。现实 \(n\ll 3584\) 走 `not_applicable_too_few_rows` |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`；`fit` 梯度有限差 \(\sim 2.5\times10^{-9}\)
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64；未知哨兵不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
3. Conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) 拒绝；能区分缺 \(+1\) 与错索引
4. `predict_set([0.7], 0.3)` 为 True；空真集 \(a=0\)
5. CLI \(a\approx0.1\) 不是首次出现序 \(0.2\)；仅 p2 得 \(0.9\)
6. 缺 `tasks.jsonl` 与祖先/父目录 `col/` 均不供给 \(E\)
7. 库层 + CLI P1：簇重采样后重算 \(\Delta\mathrm{AUC}\)；独立 IRLS 区间逐位相同；宽度 \(0.72899\neq0\)
8. 默认 P1 拒绝无留出；负 \(\Delta\mathrm{AUC}=-0.5\) 仍 `estimate`
9. 集合 API signed excess \(-0.1\) 不截断；0-hit ⇒ `noise=0`、`excess=raw`；事件均值 \(0.25\)
10. 缺 sham 协议或缺 `noise_set` → excess **null 不是 0**
11. **empty-N：** 生产 sham / unmapped / `noise_ref=0` 不扣噪；仅显式 API 0-hit 记账
12. **unknown not M：** \(M=\emptyset\)，\(\rho_M\) 全 null
13. **sham / unmapped empty N：** 不出现 excess\(_M=-1\)
14. mapped \(N=\{p3\}\) 扣除，excess \(=0\)；sham-only / unmapped hit 不记 evaluated-zero
15. analyze 无 `p1_table` → `p1 is None`
16. \(n<d\) → `truncated=True`（不是 dim-mismatch）；`eye(4)`/`eye(3)` → `truncated=False`；4096→3584 直接 N/A
17. Procrustes 独立源恢复顺/逆时针及绕 \(z\) 的 90°
18. `attention_mean` 用前提下标，不是全体/末列均值
19. C-rand/C-layer `actual_norm` 锁到主干预范数；INLP 两步 \(P=I-\hat Z\hat Z^\top\)
20. Week-8 默认 `unregistered`（**不是缺陷**）；有阈无测 → `threshold_present_measurement_missing`

---

## 11. 测试质量（仅公式）

作者声称 172 passed。本审查全仓库 **172 passed**。绿测**不能**单独证明公式正确。本轮期望值由独立 oracle 生成，不从测试断言抄数字。

- `test_conformal_examples`：只锁 2 组 \(k\)（\(N=4,\alpha=0.4\) 与 \(\alpha=0.1\)）。前者**不能**区分缺 \(+1\)（两种公式都得 \(k=3\)）。本轮 13 组，含 \(N=4,\alpha=0.25\)、\(N=6,1/6\)、\(N=8,\alpha=0.2\) 与 \(N=10,\alpha=0.1\)
- `test_p1_bootstrap_*`：锁 `lo<hi` / `lo<=hi`，**不对照独立 \(\Delta\mathrm{AUC}\) oracle**。本轮独立 IRLS 对上逐位区间
- `test_unknown_behavior_is_not_counted_as_m` / `test_sham_no_change_does_not_book_empty_n`：**有效方向**。本轮另打 API 开关、mapped、unmapped、fallback 旗标、生产 `build_labels` 与实际 `cmd_label`
- `test_c7_m01_mapped_noise_premise_is_deducted`（若存在）/ 构造 `Label(noise_ref=1)`：本轮关掉 `event_density_sets`
- `test_common_dim_marks_truncated_when_n_lt_dim`：**半有效**。只锁 \((2,5)/(2,3)\)，**不锁**与 `dimension_mismatch` 的区分。`test_common_dim_is_not_silent_truncate` 锁 `eye(4)`/`eye(3)`。本轮两门对照打
- `test_analyze_refuses_fake_p1_from_labels`：**有效**（`p1 is None`）
- `test_week8_never_passes_unregistered`：**有效**
- `test_evaluated_zero_hit_sham_is_zero_noise_not_null`：锁的是集合 API 0-hit，**不是**生产 `event_density_sets` 的 sham/`noise_ref=0` 路径。本轮把两条分开打
- `test_procrustes_recovers_known_rotation`：锁单测三角 \(\{(1,0),(0,2),(1,1)\}\) 与 \(R=[[0,-1],[1,0]]\)。本轮用独立 `rng(20260921)` 的 \(9\times2\) / \(11\times3\) 源，并对照独立 SVD oracle
- `test_attention_mean_uses_premise_indices_not_empty_zero`：锁行 \([0.1,0.8,0.1]\)。本轮用独立 \(2\times4\) 与 1D 袋，并显式对照全体/末列均值

---

## 12. 结论

声明冻结哈希 `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（61 文件）开审、攻击、交卷三读 **HASH_MATCH**。本通道未改生产字节。作者 pytest 声称 172 passed：本审查 **172 passed**；绿测不能单独证明公式。r21 A–E 对旧 hash `5097c831…` 的 PASS 不转移到本树。

对照本轮清单（绑定 §1 digest）：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\)，未知/NaN 掩码 | **通过** |
| conformal \(k\)；\(k>N\Rightarrow+\infty\)；off-by-one | **通过**（13 组手算；10 组能区分缺 \(+1\)） |
| \(S/M/\rho\) 事件均值；signed excess 不截断；空分母 null | **通过**（均值 \(0.25\)） |
| 缺 sham 协议 / 缺 `noise_set` → excess null 不是 0 | **通过** |
| empty-N booking | **通过**。生产 sham / unmapped / `noise_ref=0` 不扣噪；API 0-hit 仍记账 |
| unknown not M | **通过**（库 + CLI） |
| sham / unmapped empty N | **通过**（库 + CLI） |
| E 列跟 `task.premises` | **通过**（CLI \(a\approx0.1\) 不是 \(0.2\)） |
| Procrustes 恢复已知 90° | **通过**（独立源；\(\ell_\infty=2.22\times10^{-16}\)） |
| `attention_mean` 前提下标 | **通过**（\(0.565\) 不是 \(0.3725\)） |
| fallback 旗标 `None` vs `evaluated=True` | **旗标不一致，数字通过**（excess null） |
| P1 留出增量 AUC + 问题级 bootstrap 重算 \(\Delta\mathrm{AUC}\) | **通过**（库宽 \(0.72899\)；CLI seed-0 区间逐位相同） |
| 负 \(\Delta\mathrm{AUC}\) 仍估计（假说不要求正结果） | **通过**（\(\Delta=-0.5\) 仍 `estimate`） |
| 4096≠3584 直接迁移 N/A | **通过**（库 + `cmd_analyze`） |
| \(n<d\) truncated **不是** dim-mismatch | **通过** |
| C-rand/C-layer 范数匹配；INLP \(P=I-\hat Z\hat Z^\top\) | **通过**（两步正交） |
| Gate 未注册 | **不是缺陷** |
| 声明冻结整树 `1f5f3798…` | **HASH_MATCH** |

污染整树签核的 confirmed defect：**无**。

**验收意见：** `PASS`。开审至交卷复现声明冻结 `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb`（61 文件）。指定公式猎项在绑定字节上独立关闭：`cli.py cc5eae53…` / `measure.py 985b9d93…` / `analysis.py e4368b0a…` / `transfer.py 5549f84b…` / `calibrate.py e8b3ed34…` / `bilinear.py b34ea3e5…` / `interventions.py 0ffdbb88…` / `baselines.py 3d7ec3ba…`。empty-N / unknown-not-M / sham·unmapped empty N / conformal off-by-one / \(n<d\) vs 4096→3584 / 双线性 \(\lambda_{\mathrm{FN}}=10\) / E 列身份 / 90° Procrustes / `attention_mean` 下标 / 未注册 Gate，均在绑定字节上核对通过。fallback 旗标 `None` vs `True` 是残留（C22-U-01），当前不改变 excess。Gate 保持 `unregistered` 不是缺陷。假说不要求正 \(\Delta\mathrm{AUC}\)。真实轨迹命题 2 / 注册 Gate 仍属 pending_server，不是本通道公式失败。

通道 `PASS` **不是** Goal 验收。
