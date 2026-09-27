# C：数学与统计独立审查（round-16）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性 \(\sigma(h^\top UV^\top e+b)\)、未知/NaN 掩码、\(\lambda_{\mathrm{FN}}=10\)、split conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)（\(k>N\Rightarrow+\infty\)）、\(S=B\setminus T\) / \(M=T\setminus B\) / 有符号 excess / 空分母 null。指定攻击 **C6-M-01**、**A12-03**、**C7-M-01/02/03**、**A13-02**（未知行为不进 \(M\)，\(\rho_M\) 全列 null）、**A13-03**（`sham:` 空 \(N\) 不扣噪）。P1 留出增量 AUC + 问题级 bootstrap 重算 \(\Delta\mathrm{AUC}\)；4096→3584 直接迁移 N/A；INLP \(P=I-\hat Z\hat Z^\top\)；Week-8 无阈值保持 `unregistered`（不是缺陷）。手算微例。不发明 Gate 阈值。HASH_MISMATCH → FAIL。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读任何 round-16 的 A/B/D/E/F。`ISSUES.md` 仅作作者声称，不采信 `local close`。结论全部由本轮对磁盘字节的公式推导与数值反例重做。
- 声明冻结哈希：`5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（`.planning/audits/round-16/VERSION.md`，61 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**开审第一动作 HASH_MATCH**；公式攻击脚本启动与交卷 **HASH_MISMATCH**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改 `src/`、`tests/`、`pyproject.toml`（只写本文件与审查草稿 `_c_hash.py` / `_c_scratch_math.py` / `_c_scratch_out.json`）
- numpy：1.26.4；CPython 3.11.7（Anaconda）

---

## 1. 冻结哈希

范围内文件数：**61**（`src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`，排除 `__pycache__`）。与 VERSION「61 files」一致。抽查公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 时刻 | 文件数 | SHA-256 | 与声明值 |
|---|---|---|---|
| 开审第一动作（独立执行 VERSION 脚本） | 61 | `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` | **HASH_MATCH** |
| 公式攻击脚本启动（修复有限差草稿后） | 61 | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` | **HASH_MISMATCH** |
| 攻击脚本结束 | 61 | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` | **HASH_MISMATCH** |
| 报告起草后复读 | 61 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` | **HASH_MISMATCH** |
| 交卷前最后一读（同一脚本） | 61 | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` | **HASH_MISMATCH** |

本通道未改 `src/`、`tests/`、`pyproject.toml`。工作区在开审 MATCH 与攻击启动之间被其他进程改写。

对照开审逐文件 digest，漂移文件：

| 文件 | 开审（绑定 `5413a4bc…`） | 攻击窗口 | 交卷 | 行 |
|---|---|---|---|---|
| `cli.py` | `c1a274e233988aad3c3390041cd40ad5e214ade82ba7579a3c7c8fc35156a71a` | `b37fef2ce7998776d1e21703284bc75699908a481c509d0a10f22760c0e449c1` | `9431b7768fda6a3c3c577f811b747f57f79f57b111dfe89c12281d1d23f95bb5` | 1252 → 1259 → 1260 |
| `measure.py` | `8ec8cf09db1490978f5eacd7d90fd578cfe807bb2c6e09e2d002ae62ab83002c` | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | 同攻击窗口 | 408 → 405 |
| `edits.py` | `250055ab8257ea2e24be885a389713e0c6d71c93936b44794a1ec821cf9e39db` | `1e5b97d63a62ab78a43ee9db33594a2cc1de3add5ad25aac81007b05af3efb91` | 同攻击窗口 | 362 → 365 |
| `tests/test_round06_regressions.py` | `280f9f71bc27b52107ac470b82a30534fcb4b3583a67454ba776f9a7b7f97954` | `b555ed24000400e19f84db2ad488698701b664986266254d8e2441e4ebc73084` | 同攻击窗口 | 145 → 146 |
| `tests/test_round07_regressions.py` | `f942482ffd4b42f5d3f8ef28a20d906838e4a55476668cbc022dd75848d0347e` | `9869e0b030858d2db3c4dad96f0c6d5224aea8da4493df5a42c26a2cc8bf4a79` | `8c23db4b637c8c7013f9f93564ed28d97bd7b7bd1302f72f75089e0ceace29de` | 302 → 318 → 342 |

全程未漂（开审 = 攻击 = 交卷）：

| 文件 | SHA-256 | 说明 |
|---|---|---|
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | P1 / Week-8 |
| `transfer.py` | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | 4096≠3584；C7-M-03 |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | conformal \(k\) |
| `probes/bilinear.py` | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | \(\sigma(h^\top UV^\top e+b)\) |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | C-rand/C-layer/INLP |

**不得把声明冻结 `5413a4bc…` 标为已复核通过的整树基线。** C6 / A12-03 / C7-M-02 绑定攻击窗口 `cli.py b37fef2c…`（交卷又漂到 `9431b776…`；`_find_tasks_jsonl` / 缺文件 `ValueError` 文本仍在）。C7-M-01 / A13-02 / A13-03 / \(S/M/\rho\) 绑定攻击窗口至交卷未再漂的 `measure.py 985b9d93…`。双线性 / conformal / P1 库函数 / 迁移 / INLP 绑定上表未漂 digest。

`measure.py` 开审读（408 行）在无 sham、已观察、无 mapped hit 时走 `noise_set=[]` 且 `evaluated=True`；交卷读（405 行）把该分支收成 `noise_set=None`、`evaluated=False`，且 `_fallback_noise_set` 无 mapped hit 时由 `[]` 改为 `None`。指定 A13-02 / A13-03 / C7-M-01 不依赖该分支，已在交卷字节上复打。

---

## 2. 范围与覆盖

| 文件 | 行（交卷） | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `b34ea3e5…` | `score` / `predict_matrix` / `fit` / `weighted_bce` | 全文；独立数值 + 有限差 + 哨兵 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed34…` | `sequence_score` / `conformal_threshold` / `predict_set` | 全文；手算 \(k\) 9 组 |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a…` | `_auc` / `_fit_scores` / `p1_incremental` / `_bootstrap_p1` / `p2_paired` / `p3_recovery` / `week8_decision` | 全文；独立 IRLS 簇重算 \(\Delta\mathrm{AUC}\) |
| `src/reasoning_diff/measure.py` | 1–405（交卷） | `985b9d93…` | `dependency_densities` / `event_density_sets` / `build_labels` | 全文；signed excess + C7-M-01 + A13-02/03 |
| `src/reasoning_diff/transfer.py` | 1–86 | `5549f84b…` | `direct_transfer` / `_pca_project` / `common_dim_then_procrustes` | 全文；4096≠3584；\(n<d\)；`eye(4)`/`eye(3)` |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb88…` | `c_rand_delta` / `c_layer_delta` / `inlp_remove` / `scale_to_norm` | 全文；范数锁 + \(I-\hat Z\hat Z^\top\) |
| `src/reasoning_diff/cli.py` | `cmd_fit`；`_find_tasks_jsonl`；`_e_premise_ids`；`cmd_calibrate`；`cmd_analyze`；`cmd_label` | 攻击 `b37fef2c…`；交卷 `9431b776…` | 缺任务文件拒绝、祖先 `col/` 不绑定、假 P1、label 记账 | **实际 CLI 反例（绑定攻击 digest）** |
| `tests/test_round07_regressions.py` 等 | — | 审查中被外部改写 | C6/C7/A13 回归 | 只评测试能否锁公式；**不采信绿测** |

调用链只读：`cli.cmd_fit` / `cmd_calibrate` / `cmd_analyze` / `cmd_label`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文 / 协议：REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01 / INLP-01 / DECIDE-01。不发明 Gate 阈值。

### 3.1 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b)=\sigma(\langle h_i U,\,e_j V\rangle+b),\quad
(HU)(EV)^\top\text{ 为矩阵形式}.
\]

默认 \(r=64\)，\(\lambda_{\mathrm{FN}}=10\)。已知集 \(\mathcal K=\{(i,j):\mathrm{mask}_{ij}\land y_{ij}\in\{0,1\}\land h_i,e_j\text{ 有限}\}\)；空 \(\mathcal K\) 是 NaN / `no_known_labels`，不是 0。加权 BCE 对正类乘 10。未知哨兵 \(y\notin\{0,1\}\) 与 NaN 行不进损失。

### 3.2 Split conformal 与 \(a(X)\)

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)（代码对 \(q\) 加 `1e-12`）。\(j\) 是前提身份在 \(\hat p\) 列上的位置，必须与 \(E\) 行（`task.premises` 顺序）对齐，**不能**是 `labels.jsonl` 首次出现序。

规定反例：\(\hat p=(0.9,0.1,0.8)\)，\(E=(p1,p2,p3)\)，\(R=\{p1\}\) ⇒ \(a=1-0.9=0.1\)。若误用首次出现序 \([p3,p2,p1]\)，p1 下标 2，吃到 \(0.8\)，得 \(0.2\)。仅观察到 p2 且 \(R=\{p2\}\) 时，p2 仍须是 \(E\) 列 1，\(a=1-0.1=0.9\)。

**C6-M-01 / A12-03：** 给定阶段目录自身没有 `tasks.jsonl` 时，fit/calibrate 必须拒绝，不得退回 labels 首次出现序，也不得读取祖先 `col/tasks.jsonl`（即使前提被对调成 \([p3,p2,p1]\)）。

### 3.3 \(S/M/\rho\) 与有符号 excess

\[
S=B\setminus T,\quad
M=T\setminus B,\quad
\rho_S=\frac{|S|}{|P\setminus T|},\quad
\mathrm{excess}=\mathrm{raw}-\mathrm{noise\_reference}.
\]

分母空 → N/A。缺 sham 协议或 `noise_set is None` → excess null。已评估且 0-hit（`noise_set=[]` 且 `noise_evaluated=True`）：\(N=\emptyset\)、noise \(=0\)、excess \(=\) raw。有 mapped sham hit 时 \(N=\) 命中的真实前提，excess 做减法，**不是**改成 null。负差不截断。\(\rho_S\) 事件均值。

PITFALLS：\(T=\{p1,p2\}\)、\(B=\{p2,p3\}\)、\(P=\{p1,p2,p3,p4\}\) ⇒ \(S=\{p3\}\)、\(M=\{p1\}\)、两密度 \(1/2\)。另：raw \(=0.2\)、noise \(=0.3\) ⇒ excess \(=-0.1\)。两事件 \(\rho_S\in\{1/2,0\}\) ⇒ 均值 \(0.25\)。

**C7-M-01：** \(P=\{p1,p2,p3\}\)，\(T=\{p1\}\)，\(B=\{p3\}\)，mapped \(N=\{p3\}\) ⇒ raw \(=0.5\)，noise \(=0.5\)，excess \(=0\)。`sham:`-only hits（id 以 `sham:` 开头、无 mapped 真实 hit）必须 **null**，不得写成 evaluated-zero（\(N=\emptyset\Rightarrow\) noise \(=0\)、excess \(=\) raw）。

### 3.4 A13-02：未知行为不进 \(M\)

\(M=T\setminus B\) 把未知前提当成「不在 \(B\)」，会把未扫全的任务祖先记成 miss，抬高 \(\rho_M\)。正确协议：任务祖先未全部 `behavior_known` 时 \(M=\emptyset\)，\(\rho_M^{\mathrm{raw}}=\rho_M^{\mathrm{noise}}=\rho_M^{\mathrm{excess}}=\mathrm{null}\)。\(S\) 仍可按已观察正类计算。

规定反例：\(T=\{p1,p2\}\)，\(B=\{p2\}\)。已知路径 \(M=\{p1\}\)、\(\rho_M=1/2\)。未知路径 \(M=\emptyset\)、\(\rho_M\) 全 null。生产 `build_labels`：`no_change` 且非 `exhaustive` → `behavior_known=False`。

### 3.5 A13-03：`sham:` 空 \(N\) 不扣噪

任意 `sham:` 行（含 `noise_ref=0` 的 miss）不得把 \(N=\emptyset\) 且 `noise_evaluated=True` 记成已评估 0。空 \(N\) 对 \(M\) 的噪声项是

\[
\rho_M^{\mathrm{noise}}=\frac{|T\setminus\emptyset|}{|T|}=1,\qquad
\mathrm{excess}_M=\rho_M-1.
\]

已知 \(T=B=\{p1\}\) 时 \(\rho_M=0\)，错误空 \(N\) 会扣出 \(\mathrm{excess}_M=-1\)。正确是 `noise_set` 缺失、excess null。

### 3.6 P1

train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题上 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：重采样基础题，**每次重算** \(\Delta\mathrm{AUC}\)。禁止把点估计复制 \(n\) 次得到 \([\delta,\delta]\)。假说不要求 \(\Delta\mathrm{AUC}>0\)。

**C7-M-02：** 无 `p1_table.jsonl` 时生产 analyze 必须保持 `p1=None`，不得用标签冒充 P1 再写出 \([\delta,\delta]\)。

### 3.7 迁移与 S3

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。首批 **4096→3584** 直接模式明确不适用。附录 S3：不同维先学共同维映射（PCA），再 Procrustes。不得静默 `x[...,:k]`。

**C7-M-03：** \(n=2\), \(d_A=5\), \(d_B=3\) ⇒ \(n<\min d\)，必须 `truncated=True`。`eye(4)` vs `eye(3)`：\(n=\min(4,3)=3=\dim\)，**不得**标 `truncated=True`。

### 3.8 C-rand / C-layer / INLP

C-rand 与 C-layer 必须把 \(\Delta\) 缩放到**主干预实际范数**；缺范数拒绝。INLP 逐步 \(u_t=\mathrm{normalize}(w_t)\)，\(P\leftarrow P(I-u_tu_t^\top)\)。在已投影残差上拟合时 \(u_t\) 彼此正交，故

\[
P=\prod_t(I-u_tu_t^\top)=I-\hat Z\hat Z^\top,\quad \hat Z=[u_1,\ldots,u_T].
\]

一步手算：\(H=[[2,0],[2,0],[0,1],[0,1]]\)，\(y_{\pm1}=(1,1,-1,-1)\) ⇒ \(\hat w=(1/2,-1)\)，\(P=[[4/5,2/5],[2/5,1/5]]\)。

### 3.9 Week-8

Gate 0–2 无预注册阈值 → `unregistered`，**不是缺陷**。有阈值无测量 → 不得标 `evaluated` / pass/fail。`scientific_conclusion` 保持 `None`。本审查不发明阈值。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（矩阵误差 0；`score` 逐位相同，\(p=0.06199510441187293\)） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(1.2272895322281534\) | **通过**（逐位相同） |
| CHK-04 | `y=-1` / 空 mask | 直接调用 | **通过**：`-1` 排除后 \(10(-\log 0.8)=2.231435513142097\)；空 mask → NaN |
| CHK-05 | `fit` 空 \(\mathcal K\) | `Y=-1` | **通过**：`no_known_labels`，`loss=None` |
| CHK-06 | `U00` 有限差 | 一步 vs \(\pm\varepsilon\) | **通过**：隐含梯度 \(-0.37612837795194254\) 对数值 \(-0.3761283779990521\)，相对误差 \(1.25\times10^{-10}\) |
| CHK-07 | \(\hat p=(0.9,0.1,0.8)\) 重建 | \(U=V=I\)，\(H=\mathrm{logit}\) 行，\(E=I_3\) | **通过**。最大重建误差 \(\sim10^{-16}\) |
| CHK-08 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | 手算 9 组 vs `conformal_threshold` | **通过**。\(N=4,\alpha=0.4\) 且分数 \([0.1,0.2,0.3,0.4]\) ⇒ \(k=3,q=0.3\)；袋 \([0,0.1,0.2,0.3]\) 得 \(q=0.2\)。\(\alpha=0.1/0/0.05\) 且 \(k>N\) ⇒ \(+\infty\)。另：\(N=1,\alpha=0.5\Rightarrow q=0.5\)；\(N=1,\alpha=0\Rightarrow+\infty\)；\(N=5,\alpha=0.2\Rightarrow q=0.5\)；未排序 \([0.2,0.4,0.1]\),\(\alpha=1/3\Rightarrow q=0.4\) |
| CHK-09 | \(\alpha\ge1\)、\(\alpha<0\)、空袋 | 直接调用 | **通过**（`invalid`） |
| CHK-10 | \(1-0.7\le 0.3\)；\(q=+\infty\) | `predict_set` | **通过**（`+1e-12` 后 True；无穷阈值全收） |
| CHK-11 | 库函数 \(a(X)\) | `[0.9,0.1,0.8]` | **通过**：`truth_indices=[0]` → \(0.1\)；列 1 → \(0.9\)；空真集 → \(0\)；未知标签 → `None` |
| CHK-12 | **C6 规定反例（实际 `cmd_calibrate`）** | \(E=I_3\)；\(\hat p=\sigma(\mathrm{logit}(0.9,0.1,0.8))\)；labels 行序 \([p3,p2,p1]\)；`Task.premises` \([p1,p2,p3]\)；`ancestors(q)=\{p1\}\) | **通过**。CLI `scores=[0.10000000000000009]`（**不是** \(0.2\)）。\(N=1,\alpha=0.4\Rightarrow k=2>N\)，落盘 `infinity` 与 conformal 公式一致 |
| CHK-13 | **C6 仅 p2 labels（实际 CLI）** | 同上 pred；labels 只有 `{p2}`；祖先 \(\{p2\}\) | **通过**：CLI `scores=[0.9]` |
| CHK-15 | `cmd_fit` 的 \(Y\) 列身份 | 包装 `BilinearProbe.fit`；labels 行序 \([p3,p2,p1]\) | **通过**：\(Y[0]=(1,0,0)\)，p1 在列 0 |
| CHK-16 | **C6-M-01 缺 `tasks.jsonl`（calibrate）** | 孤立 `deep/x/feat` + `labs`；祖先 `col/tasks.jsonl` 为对调前提 | **通过**。`ValueError: calibrate requires tasks.jsonl so E columns follow task.premises, not label order`。`_find_tasks_jsonl(feat,labs) is None` |
| CHK-17 | **C6-M-01 缺 `tasks.jsonl`（fit）** | 同上 | **通过**。`ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order` |
| CHK-18 | **A12-03 父目录 `col/`** | `in_dir=work/col/feat`，`work/col/tasks.jsonl` 为对调前提 | **通过**。`_find_tasks_jsonl(parent_feat,parent_labs) is None`。fit 与 calibrate 均 raise。仅当目录**自己**是 `col/` 时才读到该文件 |
| CHK-18b | `_e_premise_ids(None, labels)` | labels \([p3,p2,p1]\) | **残留（C16-U-01）**：仍返回首次出现序。生产 fit/calibrate 在缺文件且有 labels 时先 raise |
| CHK-19 | **P1 bootstrap 是否重算 \(\Delta\mathrm{AUC}\)** | \(n=40\)，`len≡10`，`op~N(0,1000)`（`rng(0)`），`rho=y`，`y` 交替，后 20 留出，`groups=i//2`，独立 IRLS 簇重算，同一 `rng(0)` | **通过**：代码区间 \([0.07372222222222223, 0.7262731481481484]\)，宽度 \(0.6525509259259261\)，`status=resampled_delta_auc`，\(n=200\)，点估计 \(\delta=0.29\)，`auc_base=0.71`，`auc_full=1`。独立同算法区间、均值 **逐位相同**。bootstrap 头五个 \(\Delta\) 互异，不是 \([\delta,\delta]\) |
| CHK-19b | `cmd_analyze` + `p1_table.jsonl` | 同上表写入磁盘 | **通过**：同一区间与均值 |
| CHK-20 | 默认拒绝无留出；假说不要求正 AUC | 省略 `held_out`；噪声 \(\rho\) | **通过**：`requires_held_out`；噪声 \(\delta=-0.14\) 仍 `estimate` |
| CHK-21 | 常数 AUC；平局 | `_auc` | **通过**：常数 AUC \(0.5\)。分数 \([1,2,2,3]\) vs 标签 \([0,0,1,1]\) 手算 \(0.875\) |
| CHK-22 | signed excess 不截断；0-hit；空分母；事件均值 | `dependency_densities` | **通过**：\(P\) 15 / \(T\) 5 / \(S=\{p6,p7\}\) / \(N=\{p6,p7,p8\}\) ⇒ raw \(0.2\)、noise \(0.3\)、excess \(-0.1\)，不截断。0-hit ⇒ `noise=0`、`excess=raw=1`。空分母 ⇒ `rho_S` null。两事件 \(1/2\) 与 \(0\) ⇒ 均值 **0.25**（草稿第一刀误把第二事件 \(T=P\) 做成空分母，均值变成 \(0.5\)；独立重算已用 \(T=\{p1,p2,p3\}\)、\(B=\{p1\}\) 关掉）。PITFALLS \(S=\{p3\}\)、\(M=\{p1\}\)、密度 \(1/2\)。缺协议 ⇒ `sham_protocol_missing` |
| CHK-23 | **C7-M-01 `event_density_sets`** | \(T=\{p1\}\)，\(B=\{p3\}\)，mapped `noise_ref(p3)=1`；经典 \(T=\{p1,p2\}\)、\(B=P\)、\(N=\{p3\}\)；`sham:x` hit-only；生产 `build_labels` | **通过**：mapped excess **0**。经典 excess\(_S=0\)、excess\(_M=-1\)。sham-only：`null_reason=noise_set_missing`，**未**记 evaluated-zero。生产路径真实前提 `noise_ref is None`，`sham:x=1`，excess null |
| CHK-24 | **C7-M-02 analyze 标签回退** | 6 行 task/behavior，含伪造 `length/op/rho/y`，无 `p1_table.jsonl` | **通过**：`report["p1"] is None`，`status=not_evaluated`，三门 `unregistered`，`scientific_conclusion is None`。同时 `transfer` 为 4096/3584 N/A |
| CHK-25 | **C7-M-03 \(n<\min d\) 与 `eye(4)`/`eye(3)`** | \(A\in\mathbb R^{2\times5}\)，\(B\in\mathbb R^{2\times3}\)；`np.eye(4)` vs `np.eye(3)` | **通过**：前者 `truncated=True`，`status=not_applicable_too_few_rows`，`common_dim=3`。后者 `truncated=False`，`status=adapted_geometry`，`a_map=pca`，`b_map=identity` |
| CHK-26 | S3 共同维是否切片；4096≠3584 | \(n=20,d=8/5\)；`direct_transfer`；`cmd_analyze` | **通过**：`a_map=pca`，中心化 PCA vs 切片最大差 \(>1\)；`truncated=False`。库与 CLI 均为 `not_applicable_dimension_mismatch` |
| CHK-27 | Week-8 无发明门 | 默认 / 有阈无测 / 有阈有测 | **通过**：默认三门 `unregistered`。有阈无测 → `threshold_present_measurement_missing`。`rho_S_excess=0.1` vs \(0.9\) → `compared/below`。`scientific_conclusion is None` |
| CHK-28 | P2 asked 项；P3 对照 | 直接调用 | **通过**：无支持集 → `denominator_unverified`；`None` + 匹配列表 → `missing_pair`；`99` vs 1 元列表 → `denominator_inconsistent`。`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`causal_reverse_claim is False` |
| CHK-A13-02 | **未知行为 \(\rho_M\) null** | API 开关；`event_density_sets` 缺 p1 已知；生产 `build_labels`；实际 `cmd_label` | **通过**。`behavior_unknown=True` ⇒ \(M=[]\)，\(\rho_M\) 三列 null；对照已知路径 \(M=\{p1\}\)、\(\rho_M=0.5\)。部分已知 + mapped \(N=\{p3\}\)：\(M\) 仍空，但 \(S\) excess 仍为 0。CLI label：`behavior_unknown=True`，`rho_M_raw is None` |
| CHK-A13-03 | **`sham:` miss 空 \(N\) 不扣噪** | 手造 `noise_ref=0`；生产 `build_labels`；实际 `cmd_label`；对照错误空 \(N\) | **通过**。事件 `null_reason=noise_set_missing`，\(\rho_M^{\mathrm{noise/excess}}\) null。错误 \(N=\emptyset\) evaluated 会给出 \(\rho_M^{\mathrm{noise}}=1\)、excess \(=-1\)。CLI：`sham:x` 的 `noise_ref=0`，真实前提均为 `None`，未扣噪 |
| CHK-INLP | \(P=I-\hat Z\hat Z^\top\) | 一步手算 + 独立收集逐步 \(u_t\) | **通过**：一步 \(P\) 与 \([[0.8,0.4],[0.4,0.2]]\) 一致；四步 \(\|P-(I-\hat Z\hat Z^\top)\|_\infty=2.43\times10^{-16}\)；\(\hat Z^\top\hat Z=I\) |
| CHK-CRAND | C-rand/C-layer 范数 | 主干预 \(\|\Pi_Z(h_d-h_b)\|\) 作 `target_norm` | **通过**：两路 `actual_norm` 均等于 \(2.3212413240152903\)。缺范数 `ValueError`。`select_weak_layer({0:0.05,1:0.9,2:0.8})=0` |
| CHK-29 | `pytest` | 全仓库（攻击窗口树） | **160 passed**。作者声称 159。绿测**不能**单独证明公式，也不能绑定声明冻结整树。`test_round06` / `test_round07` 在窗口内被外部改写 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1 | 真实 HF 权重属 pending_server |
| 阅读其他 round-16 通道 | 任务禁止 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用独立同算法区间代替 |
| 在声明冻结整树上重跑已漂的 `test_round07_regressions.py` | 该文件交卷前已不是开审字节；指定反例由本审查直接打生产 CLI/库 |
| 追查 `cli.py` / `edits.py` 多出的非公式行 | D 通道接线，不改变本轮公式数字 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮绑定字节 | 说明 |
|---|---|---|
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | **关闭** | CHK-08/09 |
| C5-M-01 P1 bootstrap \([\delta]*n\) | **库函数 + CLI 有表路径关闭** | CHK-19 / 19b。独立区间逐位相同 |
| C6-M-01 列身份（有 \(E\)） | **关闭（指定反例）** | CHK-12/13/15。CLI \(a\approx0.1\) 不是 \(0.2\) |
| **C6-M-01 缺 `tasks.jsonl` 首次出现序** | **关闭（生产路径）** | CHK-16/17。fit/calibrate 均 `ValueError` |
| **A12-03 祖先 `col/` 对调前提** | **关闭（生产路径）** | CHK-18。远祖 `work/col` 与父目录 `work/col/feat` 均不供给 \(E\) |
| signed excess 不截断；0-hit noise=0 | **关闭（集合 API）** | CHK-22 |
| **C7-M-01** mapped \(N=\{p3\}\) 扣除 | **关闭**（`measure.py 985b9d93…`） | CHK-23。excess \(=0\)，不是 null |
| **C7-M-01** sham:-only hits 记 evaluated-zero | **关闭**（同上） | CHK-23。`null_reason=noise_set_missing` |
| **C7-M-02** analyze 标签冒充 P1 | **关闭** | CHK-24。`p1 is None` |
| **C7-M-03** \(n<d\) 仍写 `truncated=False` | **关闭** | CHK-25。现为 `truncated=True` |
| **C7-M-03** `eye(4)` vs `eye(3)` 误标 truncated | **关闭** | CHK-25。`truncated=False` |
| **A13-02** 未知行为进 \(M\) | **关闭**（库 + `cmd_label`） | CHK-A13-02。\(\rho_M\) 全 null |
| **A13-03** `sham:` 空 \(N\) 扣噪 | **关闭**（库 + `cmd_label`） | CHK-A13-03。未出现 excess \(_M=-1\) |
| 4096→3584 直接迁移 N/A | **关闭** | CHK-26 / CHK-24 |
| C-rand/C-layer 范数；INLP \(I-\hat Z\hat Z^\top\) | **关闭（库函数）** | CHK-CRAND / CHK-INLP |
| Gate 未注册 | **不是缺陷** | CHK-27 |

---

## 7. 发现

### C16-H-01 — 声明冻结在审查中被外部改写，不得签整树通过

- **严重度：** High（过程 / 冻结完整性）
- **状态：** confirmed defect（本通道未改生产字节）
- **符号：** VERSION 脚本汇总哈希
- **事实：** 开审 `5413a4bc…`（61 文件）MATCH。攻击脚本启动已是 `3d0a0764…`。报告起草后复读 `3d0f1c10…`（`cli.py` 再漂 `b37fef2c…`→`9431b776…`；`test_round07` 318→342 行）。`measure.py` / `edits.py` 在攻击窗口后未再漂。
- **影响：** 不能把声明冻结当作已独立复核的**整树**论文数字基线。清单上的公式攻击绑定 §1 表中 digest。任务规定 **HASH_MISMATCH → FAIL**。
- **修复：** 停写生产树，重新冻结后再开一轮独立 C，才能把 `5413a4bc…` 换成可签的新哈希

指定公式攻击在绑定字节上**没有新的公式 confirmed defect**。C6-M-01 / A12-03、C7-M-01/02/03、A13-02/03 在攻击窗口字节上关闭。

指定攻击（本审查实际执行，不采信 ISSUES）：

- \(\hat p=\sigma(\mathrm{logit}(0.9,0.1,0.8))\)，\(E=I_3\) 对应 \((p1,p2,p3)\)
- labels 磁盘行序 \([p3,p2,p1]\)
- `Task.premises` 序 \([p1,p2,p3]\)，`ancestors(q)=\{p1\}\)
- 论文：\(a=1-0.9=0.1\)
- 旧缺陷：首次出现序下 p1 下标 2，\(a=1-0.8=0.2\)
- **当前 `cmd_calibrate`：`scores=[0.10000000000000009]`**（不是 \(0.2\)）
- 仅 `{p2}`：CLI \(a=0.9\)
- `cmd_fit` 截获 \(Y[0]=(1.0,0.0,0.0)\)
- 远祖 `work/col/tasks.jsonl`（对调前提）+ 孤立 `deep/x/{feat,labs}`：fit 与 calibrate 均 raise；`_find_tasks_jsonl` 为 `None`
- 父目录 `work/col/feat` 对 `work/col/tasks.jsonl`：同样 raise（A12-03）
- C7-M-01 mapped：`event_density_sets` 得 excess \(=0\)
- C7-M-01 sham-only hit：excess null，不是 noise \(=0\)
- C7-M-02：无 `p1_table` → `p1 is None`
- C7-M-03：\((2,5)/(2,3)\) → `truncated=True`；`eye(4)`/`eye(3)` → `truncated=False`
- A13-02：未知行为 \(M=[]\)，\(\rho_M\) 三列 null；CLI label 相同
- A13-03：`sham:` miss 不把空 \(N\) 记成 evaluated-zero，避免 \(\mathrm{excess}_M=-1\)

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C16-U-01 | Low | `_e_premise_ids(None, labels)` 仍返回首次出现序。本审查 `labels=[p3,p2,p1]` 得 `[p3,p2,p1]` | `cli.py` | 生产 `cmd_fit` / `cmd_calibrate` 在缺文件且有 labels 时先 `ValueError` |
| C16-U-02 | Low | 交卷 `event_density_sets` 对任意 `sham:` 行（含 miss）也 `noise_set=None` | `measure.py` 349–351 | 指定猎项是 hits / 空 \(N\) 不得扣噪；两条都已关。miss 过 null 是保守记账 |
| C16-U-03 | Low | mapped `p3` hit **同时**存在 `sham:` hit 时，sham 分支优先，整事件 excess null | `measure.py` 349–351 | 指定两刀是「纯 mapped」与「纯 sham-only」。混合未列入关闭条件。本审查混合例 excess null |
| C16-U-04 | Low | `build_labels` 只给 `sham:` 前提写 `noise_ref`；真实前提恒 `None`。生产 label 路径到不了 mapped \(N=\{p3\}\) | `measure.py` 72–80 | C7-M-01 原文反例是构造 `Label(noise_ref=1)`。该路径 excess=0 |
| C16-U-05 | Low | 交卷把「已观察、无 sham、无 mapped hit」从 evaluated-zero 收成 `noise_set=None`；`_fallback_noise_set` 无 mapped 时由 `[]` 改为 `None` | `measure.py` 313–360 | 指定 0-hit 关闭条件走集合 API `noise_set=[]` 且 `noise_evaluated=True`，该路径仍 excess=raw。生产无-hit 过 null 比错误扣噪更保守 |
| C16-U-06 | Low | `n==dim` 时中心化 PCA 秩 \(\le n-1\)，`eye(4)`/`eye(3)` 仍 `truncated=False` | `transfer.py` 76–86 | 指定猎项要求该例 **保持** `truncated=False`。门是 \(n<\dim\)，不是中心化数值秩 |
| C16-U-07 | Low | `cmd_calibrate` 仍在 `feat_dir.parent/{label,lab,labels}` 找 **labels**（不是 tasks） | `cli.py` | 缺 `tasks.jsonl` 仍 raise。标签祖先查找不是 A12-03 的 \(E\) 列 |
| C16-U-08 | Low | `sequence_score` 默认 `nonconformity="prob"` 是 \(\max p\) | `calibrate.py` 24–26 | CLI 始终传 `one_minus_p` |
| C16-U-09 | Low | calibrate 仍 `task_label==1 or behavior_label==1`，且 `rsi` 含 `{nid}` | `cmd_calibrate` | 本轮主问列身份与缺文件拒绝。任务/行为应分头校准 |
| C16-U-10 | Low | `_e_premise_ids` 在 `task.premises` 之后仍追加 labels 中未见的 id | `cli.py` | 有 \(E\) 时前缀已是 premises 序。`fit` 对 \(j\ge e.shape[0]\) 跳过 |
| C16-U-11 | Low | 只传 `rng`、不传 `groups` 时仍 bootstrap \(\rho\) 均值 | `analysis.py` 87–88 | 正确 `p1_table` 路径传 `groups`。analyze 无表则 `p1 is None` |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C16-S-01 | 真实轨迹命题 2 覆盖 | 真实 HF 权重 pending_server；tiny 不是 MODEL-01 |
| C16-S-02 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）。库层 bootstrap 现可重算 \(\Delta\mathrm{AUC}\)；analyze 无表不再伪造 P1 |
| C16-S-03 | 4096↔3584 适配后的双线性 | 直接迁移 N/A 已对；共同维在 \(n\) 足够时为 PCA。现实 \(n\ll 3584\) 走 `not_applicable_too_few_rows` |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`；`fit` 梯度有限差 \(\sim 1.3\times10^{-10}\)
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64；未知哨兵不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
3. Conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) 拒绝
4. `predict_set([0.7], 0.3)` 为 True；空真集 \(a=0\)
5. **C6-M-01 指定反例关闭：** labels \([p3,p2,p1]\) vs \(E=[p1,p2,p3]\) 得 CLI \(a\approx0.1\) 不是 \(0.2\)；仅 p2 得 \(0.9\)；fit \(Y=(1,0,0)\)
6. **C6-M-01 缺 `tasks.jsonl` 关闭：** 给定目录无本题文件时 fit/calibrate 均 FAIL
7. **A12-03 关闭：** 远祖与父目录 `col/tasks.jsonl`（对调前提）均不供给 \(E\)
8. **库层 + CLI P1：** 簇重采样后重算 \(\Delta\mathrm{AUC}\)；独立 IRLS 区间逐位相同；宽度 \(0.65255\neq0\)
9. 默认 P1 拒绝无留出；假说不要求正 AUC
10. **集合 API signed excess** \(-0.1\) 不截断；0-hit ⇒ `noise=0`、`excess=raw`；事件均值 \(0.25\)
11. **C7-M-01 关闭：** mapped \(N=\{p3\}\) 扣除，excess \(=0\)；sham:-only hits **不**记 evaluated-zero
12. **C7-M-02 关闭：** analyze 无 `p1_table` → `p1 is None`
13. **C7-M-03 关闭：** \(n<d\) → `truncated=True`；`eye(4)` vs `eye(3)` → `truncated=False`
14. **A13-02 关闭：** 未知行为 \(M=\emptyset\)，\(\rho_M\) 全 null（API + `event_density_sets` + `cmd_label`）
15. **A13-03 关闭：** `sham:` 空 \(N\) 不扣噪；对照错误空 \(N\) 会给出 excess\(_M=-1\)
16. `direct_transfer(4096,3584)` 与 `cmd_analyze` N/A；S3 在 \(n\) 足够时是 PCA 不是切片
17. C-rand/C-layer `actual_norm` 锁到主干预范数；INLP \(P=I-\hat Z\hat Z^\top\)
18. Week-8 默认 `unregistered`（**不是缺陷**）；有阈无测 → `threshold_present_measurement_missing`

---

## 11. 测试质量（仅公式）

作者声称 159 passed。本审查全仓库 **160 passed**（攻击窗口树）。绿测**不能**单独证明公式正确，也不能绑定声明冻结整树。`test_round06_regressions.py` / `test_round07_regressions.py` 审查中被外部改写，不能当作对 `5413a4bc…` 的锁。

- `test_truth_indices_follow_e_columns_not_label_order`：**半有效**。不跑 `cmd_calibrate`。本轮用真实 `Task` + 实际 CLI 关掉指定反例
- `test_fit_without_tasks_jsonl_refuses_first_seen_order`：**对 fit 有效**。**不锁 calibrate**。本轮独立打了 calibrate 同一拒绝
- `test_fit_does_not_bind_ancestor_col_tasks`：**对 fit + `_find_tasks_jsonl` 有效**（远祖 `col/`）。**不锁**父目录 `col/feat`，**不锁 calibrate**。本轮两处都打了
- `test_analyze_refuses_fake_p1_from_labels`：**有效**（`p1 is None`）
- `test_common_dim_marks_truncated_when_n_lt_dim`：**半有效**。只锁 \((2,5)/(2,3)\)，**不锁** `eye(4)` vs `eye(3)`。本轮补打后者 `truncated is False`
- `test_c7_m01_mapped_noise_premise_is_deducted`：**半有效**。只锁集合 API，**不跑 `event_density_sets`**。本轮用 `Label(noise_ref=1)` 关掉生产记账路径
- `test_sham_hits_do_not_book_evaluated_zero_noise`：**有效方向**。本轮用独立三前提图复打 hits 与 miss
- `test_unknown_behavior_is_not_counted_as_m` / `test_sham_no_change_does_not_book_empty_n`：**有效方向**。本轮另打 API 开关、部分已知 mapped、生产 `build_labels` 与实际 `cmd_label`
- `test_p1_bootstrap_resamples_delta_auc` / `test_p1_bootstrap_interval_is_not_degenerate`：锁 `lo<hi`，**不对照独立 \(\Delta\mathrm{AUC}\) oracle**。本轮生产库路径已用独立 IRLS 对上逐位区间
- `test_week8_never_passes_unregistered`：**有效**
- `test_conformal_examples`：只锁 2 组 \(k\)。本轮 9 组手算

---

## 12. 结论

开审冻结哈希 `5413a4bc…` **当时 HASH_MATCH**（61 文件）。攻击启动为 `3d0a0764…`。交卷前最后一读 `3d0f1c10…`（61 文件）。**HASH_MISMATCH。** 本通道未改生产字节。`measure.py` / `cli.py` / `edits.py` 与两份回归测试在审查中被外部改写；`cli.py` 与 `test_round07` 在报告起草后又漂一次。作者 pytest 声称 159 passed：本审查 **160 passed**；该结果对应审查中途的树，不能单独证明声明冻结整树。

对照本轮清单（绑定 §1 digest）：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\)，未知/NaN 掩码 | **通过** |
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | **通过**（9 组手算） |
| \(S/M/\rho\) 事件均值；signed excess 不截断；空分母 null | **通过**（均值 \(0.25\)） |
| P1 留出增量 AUC + 问题级 bootstrap 重算 \(\Delta\mathrm{AUC}\) | **通过**（宽度 \(0.65255\)，独立区间逐位相同） |
| 4096≠3584 直接迁移 N/A | **通过**（库 + `cmd_analyze`） |
| C-rand/C-layer 范数匹配；INLP \(P=I-\hat Z\hat Z^\top\) | **通过**（库函数） |
| C6-M-01：\([p3,p2,p1]\) vs \(E=[p1,p2,p3]\) | **通过**。CLI \(a\approx0.1\) 不是 \(0.2\) |
| C6-M-01：给定目录缺 `tasks.jsonl` 必须 FAIL | **通过**。fit/calibrate 均 `ValueError` |
| A12-03：祖先 `col/` 对调前提不得供给 \(E\) | **通过**（远祖与父目录） |
| C7-M-01 mapped \(N=\{p3\}\) 扣除 | **通过**（excess \(=0\)） |
| C7-M-01 sham:-only hits 不得 evaluated-zero | **通过**（excess null） |
| C7-M-02 禁止标签冒充 P1 | **通过**（`p1 is None`） |
| C7-M-03 \(n<d\) 不得 `truncated=False`；`eye(4)`/`eye(3)` 仍 False | **通过** |
| A13-02 未知行为 \(\rho_M\) null | **通过**（库 + CLI） |
| A13-03 `sham:` 空 \(N\) 不扣噪 | **通过**（库 + CLI） |
| Gate 未注册 | **不是缺陷** |
| 声明冻结整树 `5413a4bc…` | **HASH_MISMATCH → FAIL** |

污染**声明冻结整树**签核的 confirmed defect：**C16-H-01**（哈希已漂）。清单上的公式 confirmed defects 本轮未再现。

**验收意见：** `FAIL`（HASH_MISMATCH）。开审第一动作复现声明冻结 `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（61 文件）。公式攻击起为 `3d0a0764…`，交卷 `3d0f1c10…`。**不得为声明冻结整树签通过。** 指定公式猎项在绑定字节上独立关闭：`cli.py b37fef2c…`（C6/A12/C7-M-02 攻击时） / `measure.py 985b9d93…` / `analysis.py e4368b0a…` / `transfer.py 5549f84b…` / `calibrate.py e8b3ed34…` / `bilinear.py b34ea3e5…` / `interventions.py 0ffdbb88…`。C6-M-01 / A12-03、C7-M-01/02/03、A13-02/03、conformal \(k\)、P1 簇重算、有符号 excess、4096→3584 N/A、INLP、未注册 Gate 均在绑定字节上核对通过。Gate 保持 `unregistered` 不是缺陷。真实轨迹命题 2 / 注册 Gate 仍属 pending_server，不是本通道公式失败。

---

## 附录 A：开审 MATCH（声明冻结）

开审第一动作汇总哈希为声明值 `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`（61 文件）。当时逐文件 digest（仅 file bytes）：

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc
src/reasoning_diff/cli.py  c1a274e233988aad3c3390041cd40ad5e214ade82ba7579a3c7c8fc35156a71a
src/reasoning_diff/edits.py  250055ab8257ea2e24be885a389713e0c6d71c93936b44794a1ec821cf9e39db
src/reasoning_diff/events.py  290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3
src/reasoning_diff/executor.py  481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  8ec8cf09db1490978f5eacd7d90fd578cfe807bb2c6e09e2d002ae62ab83002c
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
tests/test_round06_regressions.py  280f9f71bc27b52107ac470b82a30534fcb4b3583a67454ba776f9a7b7f97954
tests/test_round07_regressions.py  f942482ffd4b42f5d3f8ef28a20d906838e4a55476668cbc022dd75848d0347e
tests/test_science.py  cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```

## 附录 B：交卷前最后一读（HASH_MISMATCH，不得替代声明冻结）

落盘前汇总 `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`。与附录 A 不同的文件：`cli.py`、`edits.py`、`measure.py`、`tests/test_round06_regressions.py`、`tests/test_round07_regressions.py`（digest 见 §1）。其余 56 个文件与开审逐位相同。`cli.py` 与 `test_round07` 在攻击窗口后又被改写，不得把交卷 `cli.py 9431b776…` 冒充 C6 反例当时的 `b37fef2c…`。
