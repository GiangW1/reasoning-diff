# C：数学与统计独立审查（round-15）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性 \(\sigma(h^\top UV^\top e+b)\)、split conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)（\(k>N\Rightarrow+\infty\)）、\(S=B\setminus T\) / \(M=T\setminus B\)、有符号 excess。必须在**当前字节**上独立攻击 C7-M-01 / C7-M-02 / C7-M-03 / C6-M-01（给定目录无 `tasks.jsonl` → raise；祖先 `col` **不得绑定**）、A13-02（unknown → \(\rho_M\) null 不是 1.0）、A13-03（sham 空 \(N\) 不得当已评估扣除）。P1 留出 incremental AUC + 簇 bootstrap 重算 \(\Delta\mathrm{AUC}\)（禁止 \([\delta,\delta]\)）；4096→3584 直接迁移 N/A；INLP \(P=I-\hat Z\hat Z^\top\)；Week-8 无阈值 → `unregistered`。不发明 Gate 阈值。不采信 ISSUES 作者 close。不读任何 round-15 其他通道。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读任何 round-15 的 A/B/D/E/F。`ISSUES.md` 仅作作者声称。结论全部由本轮对磁盘字节的公式推导与数值反例重做。
- 声明冻结哈希：`401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`（`.planning/audits/round-15/VERSION.md`，61 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**开审 HASH_MATCH；交卷 HASH_MISMATCH → FAIL**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改 `src/`、`tests/`、`pyproject.toml`（只写本文件与 `.planning/audits/round-15/_c_*.py` 草稿）
- numpy：1.26.4；CPython 3.11.7（Anaconda）

---

## 1. 冻结哈希

范围内文件数：**61**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 18 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「61 files」一致。抽查公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算（开审第一动作）：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 时刻 | SHA-256 | 与声明值 |
|---|---|---|
| 开审（第一动作，独立执行 VERSION 脚本） | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` | **HASH_MATCH** |
| 公式攻击与全仓库 pytest 之后（攻击仍跑在声明树上） | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` | **HASH_MATCH** |
| 写完本文件后交卷前最后一次 | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` | **HASH_MISMATCH** |

开审 61 文件等于声明值。本通道未改 `src/`、`tests/`、`pyproject.toml`。写报告期间其他写入者改过树。任务规定 **HASH_MISMATCH → FAIL**。不得把交卷哈希冒充声明冻结 `401e509b…`，也不得在已漂汇总上记连续通过。

相对开审/攻击绑定，交卷时下列 digest 已变（本通道未改）：

| 文件 | 开审 / 攻击绑定 | 交卷 |
|---|---|---|
| `cli.py` | `c1a274e2…`（1252 行） | `b37fef2c…`（1259 行） |
| `measure.py` | `8ec8cf09…`（408 行） | `985b9d93…`（405 行） |
| `edits.py` | `250055ab…`（362 行） | `1e5b97d6…`（365 行） |
| `models/generate.py` | `07493570…` | `6e604039…` |
| `models/tiny.py` | `21725a18…` | `c75d0f53…` |
| `tests/test_round06_regressions.py` | `280f9f71…` | `b555ed24…` |
| `tests/test_round07_regressions.py` | `e8ba9102…` | `9869e0b0…` |

`measure.py` 与 `cli.py` 是 A13-02 / A13-03 / C6-M-01 / C7-M-01/02 的活字节。交卷树已不是攻击所绑定的公式实现。`analysis.py` / `bilinear.py` / `calibrate.py` / `transfer.py` / `interventions.py` 交卷时仍等于开审 digest。

公式攻击绑定下表 digest（**攻击执行时所读**；其后 `measure.py` / `cli.py` 已漂）：

| 文件 | SHA-256（本审查绑定） | 行 |
|---|---|---|
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | 337 |
| `measure.py` | `8ec8cf09db1490978f5eacd7d90fd578cfe807bb2c6e09e2d002ae62ab83002c` | 408 |
| `transfer.py` | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | 86 |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | 45 |
| `probes/bilinear.py` | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | 101 |
| `probes/boundary.py` | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | 44 |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | 115 |
| `cli.py` | `c1a274e233988aad3c3390041cd40ad5e214ade82ba7579a3c7c8fc35156a71a` | 1252 |

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `b34ea3e5…` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + NaN 行掩码 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed34…` | `sequence_score`/`conformal_threshold`/`predict_set` | 全文；手算 9 组 \(k\) |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `ce3b549b…` | Hidden=256；BCE 符号 | 全文 |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a…` | `_auc`/`_fit_scores`/`p1_incremental`/`_bootstrap_p1`/`p2_paired`/`p3_recovery`/`week8_decision` | 全文；独立 IRLS 簇重算 \(\Delta\mathrm{AUC}\) |
| `src/reasoning_diff/transfer.py` | 1–86 | `5549f84b…` | `direct_transfer`/`_pca_project`/`common_dim_then_procrustes` | 全文；\(n=2,d=5/3\) 与 `eye(4)/eye(3)` |
| `src/reasoning_diff/measure.py` | 1–408 | `8ec8cf09…` | `dependency_densities`/`event_density_sets`/`build_labels` | 全文；C7-M-01、A13-02、A13-03 |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb88…` | `inlp_remove`/`c_rand_delta`/`c_layer_delta` | 全文 |
| `src/reasoning_diff/cli.py` | `cmd_fit` 577–673；`_find_tasks_jsonl` 692–700；`_e_premise_ids` 703–712；`cmd_calibrate` 724–803；`cmd_label` 550–574；`cmd_analyze` 1057–1154 | `c1a274e2…` | 无本题 `tasks.jsonl` 必须 ValueError；祖先不得绑定；无 `p1_table` 不得造 P1；`direct_transfer(4096,3584)` | **实际 CLI** |
| `tests/test_science.py` / `tests/test_round07_regressions.py` | — | 查是否独立锁住指定反例 | 绿测**不是**公式正确性 |

调用链只读：`cli.cmd_fit` / `cmd_calibrate` / `cmd_analyze` / `cmd_label`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文 / 协议：REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01 / INLP-01 / DECIDE-01；PITFALLS 校准 / P1 / 有符号 excess / unknown 计入 M / 跨维条。不发明 Gate 阈值。

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

**C7-M-01 规定微例（本通道手算）：**

\[
P=\{p1,p2,p3\},\quad T=\{p1,p2\},\quad B=\{p1,p2,p3\},\quad N=\{p3\}.
\]

\[
S=\{p3\},\quad |P\setminus T|=1,\quad \rho_S^{\mathrm{raw}}=1,
\quad |N\setminus T|=1,\quad \rho_S^{\mathrm{noise}}=1,
\quad \mathrm{excess}_S=0.
\]

\[
M=\emptyset,\quad \rho_M^{\mathrm{raw}}=0,\quad |T\setminus N|=2,\quad \rho_M^{\mathrm{noise}}=1,
\quad \mathrm{excess}_M=-1.
\]

仅 `sham:` / 未映射 hit：不得把 \(N=\emptyset\) 且 `noise_evaluated=True` 记成已评估 0（那会给出 excess \(=\) raw）。正确是 `noise_set` 缺失、excess null。

### 3.2 A13-02：unknown → \(\rho_M\) null，不是 1.0

PITFALLS：unknown 不得计入 \(M\)；未扫描的任务边不能宣称已确认漏读。

旧失败模式：行为未知时把 \(B=\emptyset\)，于是 \(M=T\setminus\emptyset=T\)，\(|T|>0\) 时 \(\rho_M=1.0\)。

正确：

\[
\texttt{behavior\_unknown}\implies M=\emptyset,\;\rho_M^{\mathrm{raw}}=\rho_M^{\mathrm{noise}}=\mathrm{excess}_M=\mathrm{null}.
\]

`event_density_sets` 判定：

\[
\texttt{behavior\_unknown}=\neg K \;\lor\; \bigl(T\neq\emptyset \land T\not\subseteq K\bigr),
\]

其中 \(K\) 是该事件上 `behavior_known` 且 premise 属于 \(P\) 的集合。因此 \(T=\{p1,p2\}\) 只知 \(p1\)、不知 \(p2\) 时也必须 null，不能写成 \(\rho_M=1/2\)。

对照：两边都是 **exhaustive + observed_response + no_change** 的确认阴性 ⇒ \(K=T\)、\(B=\emptyset\)、\(M=T\)、\(\rho_M=1.0\)。这是已确认漏读，不是 unknown。

生产 `build_labels`：`no_change` 且非 exhaustive 不得进入 `known_negatives`，`behavior_known=False`。

### 3.3 A13-03：sham 空 \(N\) 不得扣除

旧失败模式：存在 `sham:` 行但 outcome=`no_change`（`noise_ref=0`）时，把 \(N=\emptyset\) 记成已评估 0-hit ⇒ \(\rho^{\mathrm{noise}}=0\)、excess \(=\) raw。

正确：任意 `sham:` 行（含 no-change）⇒ `noise_set=None`、`noise_evaluated=False` ⇒ excess null（`noise_set_missing`）。API 上 `noise_set=[]` 且 `noise_evaluated=False` ⇒ `noise_set_empty`，同样不得扣除。

对照：无 sham、且明确 `noise_evaluated=True` 的空 \(N\) 才是合法 0-hit。

### 3.4 TO / CSP

\[
\mathrm{TO}(T_0,T_{\mathrm{pert}})=\frac{2\cdot\mathrm{LCS}(T_0,T_{\mathrm{pert}})}{|T_0|+|T_{\mathrm{pert}}|},\qquad
\mathrm{CSP}_{\mathrm{matched}}=\frac1{|A_{\mathrm{clean}}|}\sum_{i\in A_{\mathrm{clean}}}\mathbf1[v_i(P')=v_i(P)].
\]

CSP 只在已对齐、父母已知且不交编辑前提的干净事件上计算。

### 3.5 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b),\quad \lambda_{\mathrm{FN}}=10,\ \mathrm{rank}=64.
\]

\(\mathcal K=\{i:\mathrm{mask}_i\land y_i\in\{0,1\}\}\)；空 \(\mathcal K\) 是 NaN / `no_known_labels`，不是 0。NaN \(H\) 行 / \(E\) 列不进 \(\mathcal K\)。加权 BCE：

\[
\frac1{|\mathcal K|}\sum_{k\in\mathcal K} w_k\bigl(-y\log p-(1-y)\log(1-p)\bigr),\quad w_k=\lambda_{\mathrm{FN}}\mathbf1[y=1]+1\cdot\mathbf1[y=0].
\]

对 logit 的梯度是 \(w(p-y)\)，与 `fit` 中 `weights * (pred - Y)` 一致。

手算：\(p=(0.8,0.2)\)，\(y=(1,0)\) ⇒
\(\mathrm{mean}(10(-\log 0.8),\;-\log(1-0.2))=\mathrm{mean}(2.231435513142097,\;0.2231435513142097)=1.2272895322281534\)。

### 3.6 Split conformal

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)（1-index，代码 `arr[k-1]`）；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。

手算：\(N=4,\alpha=0.4\Rightarrow k=\lceil 5\cdot 0.6\rceil=3\)；分数 \(\{0.4,0.1,0.3,0.2\}\) 排序后 \(q=s_{(3)}=0.3\)。\(N=4,\alpha=0.1\Rightarrow k=\lceil 4.5\rceil=5>4\Rightarrow+\infty\)。\(\alpha=0\Rightarrow k=N+1\Rightarrow+\infty\)。

### 3.7 P1–P3

- **P1：** train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题上 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：重采样基础题，**每次重算** \(\Delta\mathrm{AUC}\)。禁止 \([\delta]*n\)。假说不要求 \(\Delta\mathrm{AUC}>0\)。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\)；须有 `shared_premises` 且 \(|\mathrm{shared\_premises}|=\) 声称分母。
- **P3：** 相对 C-rand / C-layer；报告非目标与 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

**C7-M-02：** `cmd_analyze` 无 `p1_table.jsonl` 时不得用 task/behavior 标签冒充 `length≡1` / `op≡0` / \(\rho=\) behavior。\(p1\) 必须保持 `None`。

### 3.8 迁移与 S3

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。首批 **4096→3584** 直接模式明确不适用。附录 S3：不同维先学共同维映射（PCA，不是 \(x[:,:k]\)），再 Procrustes。

**C7-M-03：** \(n=2\)、\(d\in\{5,3\}\) ⇒ \(\min n=2<\mathrm{dim}=3\) ⇒ `truncated=True`。`eye(4)` vs `eye(3)`：\(\min n=3=\mathrm{dim}\) ⇒ `truncated=False`，且 PCA 不得等于前 3 列切片。

### 3.9 INLP / C-rand / C-layer

一步 INLP：\(\hat w=\arg\min\|Hw-y_{\pm1}\|\), \(u=\hat w/\|\hat w\|\), \(P=I-uu^\top=I-\hat Z\hat Z^\top\), \(H\leftarrow HP\)。C-rand / C-layer 必须把 \(\Delta\) 缩放到主干预的 `target_norm`；缺范数拒绝。

手算：\(H=[[2,0],[2,0],[0,1],[0,1]]\), \(y_{\pm1}=(1,1,-1,-1)\) ⇒ \(\hat w=(1/2,-1)\)，
\(u=(1/\sqrt5,-2/\sqrt5)\)，\(P=[[4/5,2/5],[2/5,1/5]]\)。

### 3.10 Week-8

Gate 0–2 无预注册阈值 → `unregistered`，**不是缺陷**。有阈值无测量 → 不得标 `evaluated` / pass/fail。`scientific_conclusion` 保持 `None`。本审查不发明阈值。

### 3.11 C6-M-01（本轮指定：给定目录 + 祖先不得绑定）

labels 存在且**给定 stage 目录**找不到 `tasks.jsonl` 时，fit/calibrate **必须 ValueError**，不得按 `labels.jsonl` 首次出现序给 \(E/Y\) 列编号。祖先目录里的 `tasks.jsonl`（含名为 `col` 的祖先/旁路）**不得绑定**。有本题 `tasks.jsonl` 时列序必须是 `task.premises`。

反例：\(E=I_3\)，\(\hat p=\sigma(\mathrm{logit}(0.9,0.1,0.8))=(0.9,0.1,0.8)\)；labels 行序 \([p3,p2,p1]\)；`Task.premises` \([p1,p2,p3]\)；事件祖先 \(\{p1\}\)。任务序 \(a=1-0.9=0.1\)；首次出现序会吃到列 2 得 \(a=1-0.8=0.2\)。

`_find_tasks_jsonl` 活字节只检查传入目录自己的 `tasks.jsonl`（A12-03），不走祖先 extras。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（标量差 0；矩阵 maxabs \(0\)） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(1.2272895322281534\) | **通过**（逐位相同） |
| CHK-04 | `y=-1` / 空 mask | 直接调用 | **通过**：`-1` 排除后 \(10(-\log 0.8)=2.231435513142097\)；空 mask → NaN |
| CHK-04b | NaN \(H\) 行不进 \(\mathcal K\) | `H[1]=[nan,1]`，`lr=0` 仍有 finite loss | **通过** |
| CHK-05 | `fit` 空 \(\mathcal K\) | `Y=-1` | **通过**：`no_known_labels`，`loss=None` |
| CHK-06 | `U00` 有限差 | 一步 vs \(\pm\varepsilon\) | **通过**：相对误差 \(1.69\times10^{-8}\) |
| CHK-07 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | 9 组；\(N=4,\alpha=0.4\) 分数 \(\{0.4,0.1,0.3,0.2\}\Rightarrow q=0.3\) | **通过**（\(\alpha=0.1/0.05/0\Rightarrow+\infty\)；另 \(N=3,\alpha=0.5\Rightarrow k=2,q=0.2\)；\(N=5,\alpha=0.2\Rightarrow k=5,q=0.5\)；\(N=8,\alpha=0.25\Rightarrow k=7,q=0.7\)） |
| CHK-08 | \(\alpha\ge1\)、\(\alpha<0\)、空袋、`None` | 直接调用 | **通过**（`invalid`） |
| CHK-09 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**（`+1e-12` 后 True） |
| CHK-10 | 库函数 \(a(X)\) | `[0.9,0.1,0.8]` | **通过**：`truth_indices=[0]` → \(1-0.9=0.1\)（IEEE `0.0999…`）；空真集 → \(0\)；未知标签 → `None` |
| CHK-15 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`cmd_analyze` | **通过**（库与 CLI 均为 `not_applicable_dimension_mismatch`） |
| CHK-17 | 常数 AUC；Mann–Whitney 平局 | `_auc` | **通过**：常数 0.5。正分 \(\{3,2,2\}\) 负分 \(\{2,1,0\}\)：9 对中 7 严格大于、2 平局 ⇒ \(8/9=0.888\ldots\) |
| CHK-18 | 默认 P1；留出 logistic | \(n=40\)，`len≡10`，`op~N(0,1000)`，`rho=y`，偶数下标留出 | **通过**：`auc_full=1`，`auc_base=0.44`，\(\delta=0.56\)，`held_out_logistic` |
| CHK-19 | 留出拟合是否忽略 eval \(X\) | 独立 IRLS：只改 held-out \(\rho\) | **通过**（train 差 0；eval 变 \(0.999999\)） |
| CHK-20 | 省略 `held_out` | 直接调用 | **通过**（`requires_held_out`） |
| CHK-21 | **P1 bootstrap 是否重算 \(\Delta\mathrm{AUC}\)** | 同上，`groups=i//2`，独立 IRLS 簇重算，同一 `rng(0)` | **通过**：代码区间 \([0.20980050505050502, 0.7982323232323233]\)，宽度 \(0.588\)，`status=resampled_delta_auc`，\(n=200\)。独立同算法区间、均值 **逐位相同**。不是 \([\delta,\delta]\)（点估计 \(\delta=0.56\)） |
| CHK-22 | 仅传 `rng`、不传 `groups` | 同上 | **残留**（C15-U-02）：bootstrap 的是 \(\rho\) 均值 \(0.5\)，区间 \([0.325,0.625]\)，不是 \(\Delta\mathrm{AUC}\)。CLI `analyze` 有 `p1_table` 时始终传 `groups` |
| CHK-23 | 假说不要求正 AUC | \(\rho\sim N(0,1)\) 与 \(y\) 无关 | **通过**：`delta_auc=-0.01`，`status=estimate` |
| CHK-24 | P2 减法、None、支持集 | `p2_paired` | **asked 项通过**：无支持集 → `denominator_unverified`；`None` → `missing_pair`；分母不一致 → `denominator_inconsistent`；有支持集 \(\Delta\rho=0.3\)、\(\Delta\mathrm{acc}=-0.2\)。**残留**：`0.9` 对分母 4 仍 `ok`（C15-U-04） |
| CHK-25 | P3 相对对照 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline_acc=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`causal_reverse_claim is False` |
| CHK-26 | PITFALLS \(S/M\)；有符号 excess；0-hit；并集 vs 均值 | 手算 | **通过**：无 sham → raw \(0.5/0.5\)、excess null。\(P=15,T=5,S=\{p6,p7\},N=\{p6,p7,p8\}\) ⇒ raw \(0.2\)、noise \(0.3\)、excess \(-0.1\)（浮点 \(-0.0999\ldots\)），不截断。空分母 → \(\rho_S\) null。0-hit → `noise=0`、`excess=raw`。两事件 \(1/2\) 与 \(0\) → 均值 **0.25** |
| CHK-27 | 矩阵缺 noise | `task=[[0,1,0]]` | **通过**：S 的 noise/excess 均为 `None` |
| CHK-28 | TO/CSP 微例 | tokens \([1,2,3,4,5]\) vs \([1,2,9,4,5]\)；干净值不变、脏值变 | **通过**：手算 \(\mathrm{TO}=0.8\)，`csp=1.0`，`dirty_change_rate=1.0` |
| CHK-29 | INLP \(P=I-uu^\top\) | 上节手算 | **通过**：`w=(0.5,-1)`，\(P=[[0.8,0.4],[0.4,0.2]]\)，一步矩阵差 0；8 步 \(\|HP\|\approx 3.6\times10^{-64}\) |
| CHK-30 | C-rand/C-layer 匹配主范数 | 强制 `target_norm=3` | **通过**（缺范数：`C-rand requires the actual main-intervention norm`；`actual_norm≈3`） |
| CHK-31 | Boundary Hidden=256；BCE 符号 | `hidden=128` 拒绝；\(y=0,p=\sigma(10)\) | **通过**：手算 loss \(10.000045398899218\) |
| CHK-C7M01-set | 集合 API \(N=\{p3\}\) | `dependency_densities` | **通过**：\(\rho_S^{\mathrm{raw}}=1\)、noise \(=1\)、excess \(=0\)；\(\rho_M^{\mathrm{excess}}=-1\) |
| CHK-C7M01-eds | **C7-M-01 Label 路径** | 自造 3 前提 Task；仅 `p3.noise_ref=1` | **通过**：`event_density_sets` → excess \(=0\)、noise \(=1\)、`null_reason is None` |
| CHK-C7M01-sham | **仅 `sham:` hit（生产 `build_labels`）** | 三真实前提 `changed` + `sham:ghost` `changed` | **通过**：事件 `null_reason=noise_set_missing`，\(S=\{p3\}\)，\(\rho_S^{\mathrm{raw}}=1\)，excess **null** |
| CHK-A1302-api | **unknown API** \(T=\{p1,p2\},B=\emptyset\) | `behavior_unknown=True` | **通过**：\(M=[]\)，\(\rho_M^{\mathrm{raw/noise/excess}}\) 皆 null，**不是 1.0** |
| CHK-A1302-confirm | 对照：确认阴性 | `behavior_unknown=False` | **通过**：\(M=\{p1,p2\}\)，\(\rho_M=1.0\) |
| CHK-A1302-partial | \(T\) 只覆盖一半已知 | eds：p1 known 0，p2 unknown | **通过**：\(\rho_M\) null，不是 \(0.5\) |
| CHK-A1302-prod | 生产 `build_labels` + eds | `no_change` 非 exhaustive | **通过**：`behavior_known=False`，\(\rho_M\) null，\(M=[]\) |
| CHK-A1302-cli | **实际 `label` CLI** | 自造 observations + 3 前提 Task | **通过**：顶层 `rho_M_raw is None`；事件层 `behavior_unknown=True` |
| CHK-A1302-exh | exhaustive no_change 对照 | 生产路径 | **通过**：确认漏读 \(\rho_M=1.0\)，未被过度 null |
| CHK-A1303-prod | **sham no-change 不得空 \(N\) 扣除** | `build_labels` + eds | **通过**：`sham:ghost.noise_ref=0`；真实前提 `noise_ref=None`；excess null，`noise_set_missing`，**不是** noise=0 / excess=raw=1 |
| CHK-A1303-api | `noise_set=[]` 且未评估 | 集合 API | **通过**：`noise_set_empty`，excess null |
| CHK-A1303-0hit | 对照：已评估空 \(N\) | `noise_evaluated=True` | **通过**：noise=0，excess=1（合法 0-hit） |
| CHK-A1303-cli | **实际 `label` CLI** | 真实 `changed` + `sham:` `no_change` | **通过**：excess null，`noise_set_missing` |
| CHK-C7M02 | **无 `p1_table`，6 条混合标签** | 实际 `cli.main(["analyze", …])` | **通过**：`p1 is None`，`status=not_evaluated`，三门 `unregistered`，`scientific_conclusion is None`，transfer 4096→3584 N/A |
| CHK-C7M02b | labels 自带 `length/op/rho/y` | 同一目录毒化列 | **通过**：仍 `p1 is None` |
| CHK-C7M02c | 有真 `p1_table` | CLI + `problem_id`，与 CHK-18 同数据 | **通过**：\(\delta=0.56\)，区间与独立 IRLS **逐位相同** \([0.2098,0.7982]\)，`resampled_delta_auc`，\(n=200\)，不是 \([\delta,\delta]\) |
| CHK-C7M03-n2 | \(n=2,d=5/3\) | `common_dim_then_procrustes` | **通过**：`truncated=True`，`not_applicable_too_few_rows`，`common_dim=3` |
| CHK-C7M03-eye | `eye(4)` vs `eye(3)` | PCA vs \(I_3\) / \(A[:3,:3]\) | **通过**：`truncated=False`，`a_map=pca`，`b_map=identity`；\(\|ap-I_3\|_\infty=1.7071067811865477\) |
| CHK-C7M03-pca8 | 等行 \(8\times4/8\times3\) | PCA vs \(A[:,:3]\) | **通过**：差 \(6.88\)；`truncated=False` |
| CHK-C6M01-eids | `_e_premise_ids` | labels \([p3,p2,p1]\) | **通过**：`task=None` → 首次出现 \([p3,p2,p1]\)；有 Task → \([p1,p2,p3]\)。孤立目录 `_find_tasks_jsonl` 为 `None` |
| CHK-C6M01-fit | **labels 在、给定目录无 `tasks.jsonl`** | 实际 `fit`，系统临时目录 | **通过**：`ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order`；未写出 `probes.jsonl` |
| CHK-C6M01-cal | 同上 calibrate | 实际 `calibrate` + probes/features/labels | **通过**：同类 `ValueError` |
| CHK-C6M01-anc | **祖先 `tasks.jsonl` + 祖先 `col/tasks.jsonl` 不得绑定** | 父目录写入对调 premise 序的 decoy；给定 feat/labs 无任务文件 | **通过**：`_find_tasks_jsonl(feat,labs) is None`；fit **ValueError**，未吃祖先列序 |
| CHK-C6M01-anc-cal | 同上 calibrate | 匹配维探针；任务只在父目录 | **通过**：`_find_tasks_jsonl` 为 `None`；calibrate **ValueError** |
| CHK-C6M01-order | 有本题 `tasks.jsonl` 列身份 | \(E=I_3\)，\(\hat p=(0.9,0.1,0.8)\)，祖先 \(\{p1\}\) | **通过**：CLI `scores=[0.10000000000000009]`，手算任务序 \(0.1\)；首次出现序会是 \(0.2\) |
| CHK-34 | Week-8 | 默认 / 有阈无测 / 有阈有测 | **通过**：默认三门 `unregistered`，`scientific_conclusion is None`。有阈无测 → `threshold_present_measurement_missing`。`0.1` vs \(0.9\) → `compared/below` |
| CHK-35 | `pytest` 全仓库 | 本审查重跑 | **159 passed**（与作者声称 159 一致；本通道独立得到，不以作者数为准） |

额外攻击（非指定关闭条件，记录）：同一事件上 **映射 `p3` 与 `sham:` 行并存** 时，活字节 `event_density_sets` 因 `_has_sham_row` 先把 `noise_set=None`，丢掉已映射的 \(N=\{p3\}\)，excess 变 null。指定 C7-M-01 微例（只有映射 \(N=\{p3\}\)）与 A13-03（只有 sham）不受影响。见 C15-U-03。

矩阵 API 把 unknown 编成 `0` 时 \(\rho_M=1.0\)；编成 `-1` 则从 support 排除、\(\rho_M\) null。生产 `cmd_label` / `event_density_sets` 走集合 API + `behavior_unknown`，不走该矩阵编码。见 C15-U-08。

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | 真实 HF 权重属 pending_server；本轮只验证公式与 CLI |
| 阅读任何 round-15 其他通道 | 任务禁止 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用分数值域、污染 eval \(X\)、检出 \(\rho=y\)、独立同算法区间代替 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\) |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | \(0\le\alpha<1\) 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | 一步 \(P=I-uu^\top\) 与手算一致；函数返回 \(P\)，调用方做 \(HP\) |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm` |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels` |
| C2-M-02 默认 P1 非留出 | **关闭** | 省略 `held_out` → `requires_held_out` |
| C5-M-01 P1 bootstrap \([\delta]*n\) | **关闭** | 见 CHK-21 |
| **C6-M-01** labels 在、给定目录无 `tasks.jsonl`；祖先不得绑定 | **关闭（实际 CLI）** | 孤立目录 fit/calibrate 均 ValueError。祖先 `tasks.jsonl` 与祖先 `col/tasks.jsonl` **未绑定**。有本题任务文件时 \(a=0.1\) 不是 \(0.2\) |
| **C7-M-01** 映射 \(N=\{p3\}\) 应扣除；仅 sham 不得记已评估 0 | **关闭（指定反例）** | 集合 API 与 `event_density_sets` 得 excess \(=0\)；生产 `build_labels` + 仅 sham 得 `noise_set_missing` |
| **C7-M-02** 无 `p1_table` 用标签冒充 P1 | **关闭（实际 CLI）** | 6 条混合标签 + 毒化 `length/op/rho` 列，`p1 is None` |
| **C7-M-03** \(n<\min d\) 仍写 `truncated=False` | **关闭** | \(n=2,d=5/3\) → `truncated=True`；`eye(4)/eye(3)` 仍 False 且 PCA ≠ 切片 |
| **A13-02** unknown 计入 \(M\) 得 \(\rho_M=1.0\) | **关闭（API + eds + 生产 build_labels + label CLI）** | unknown / \(T\not\subseteq K\) → \(\rho_M\) null；确认 exhaustive 阴性仍为 1.0 |
| **A13-03** sham no-change 把空 \(N\) 当已评估扣除 | **关闭（生产 build_labels + eds + label CLI）** | `sham:` 行 ⇒ excess null，不是 noise=0 / excess=raw |

---

## 7. 发现

对本通道**攻击时所绑定**的 `measure.py 8ec8cf09…` / `cli.py c1a274e2…` 等 digest：无新的 confirmed defect 会污染指定论文数字。C7-M-01 / C7-M-02 / C7-M-03 / C6-M-01 / A13-02 / A13-03 规定反例在**该**字节上关闭。交卷树已漂（`measure.py 985b9d93…` / `cli.py b37fef2c…`），这些关闭**不**转移到交卷哈希。整体验收仍因 HASH_MISMATCH 为 FAIL。

指定攻击（本审查实际执行，不采信 ISSUES）：

**A13-02**

- 手算旧缺陷：\(T=\{p1,p2\}\)、\(B=\emptyset\)（unknown）会得 \(M=T\)、\(\rho_M=1.0\)
- `dependency_densities(..., behavior_unknown=True)`：\(M=[]\)，\(\rho_M^{\mathrm{raw/noise/excess}}\) 皆 **null**
- 对照 `behavior_unknown=False`：\(\rho_M=1.0\)（确认漏读）
- `event_density_sets`：三前提 Task，标签全未知 → \(\rho_M\) null；只知 p1、不知 p2 → 仍 null，不是 \(0.5\)
- 生产 `build_labels`：`no_change` 非 exhaustive → `behavior_known=False` → eds \(\rho_M\) null
- 实际 `cli.main(["label", …])`：顶层 `rho_M_raw is None`

**A13-03**

- 生产 `build_labels` + `sham:ghost` / `no_change`：sham 行 `noise_ref=0.0`，真实前提 `noise_ref=None`
- eds：`null_reason=noise_set_missing`，\(\rho_S^{\mathrm{raw}}=1\)，excess **null**。若误记已评估空 \(N\)，会得到 excess \(=1\)
- API `noise_set=[]` + `noise_evaluated=False` → `noise_set_empty`
- 实际 `label` CLI：excess null
- 对照已评估空 \(N\) 仍是合法 0-hit（noise=0，excess=raw）

**C7-M-01**

- 手算：\(P=\{p1,p2,p3\}\), \(T=\{p1,p2\}\), \(B=\{p1,p2,p3\}\), \(N=\{p3\}\) ⇒ excess\(_S=0\)，excess\(_M=-1\)
- 集合 API 与 3 前提 Label 路径：逐位相同
- 仅 `sham:ghost` changed：excess null，不是 excess \(=1\)

**C7-M-02**

- 写入 6 行混合 task/behavior，**无** `p1_table.jsonl` → `p1 is None`
- 毒化 `length/op/rho/y` 列：仍 `p1 is None`
- 有真表：\(\delta=0.56\)，区间与独立 IRLS 逐位相同，不是 \([\delta,\delta]\)

**C7-M-03**

- \(A\in\mathbb{R}^{2\times5}\), \(B\in\mathbb{R}^{2\times3}\)：`truncated=True`
- `eye(4)` vs `eye(3)`：`truncated=False`，\(\ell_\infty(ap,I_3)=1.7071067811865477\)，不是静默列切片

**C6-M-01**

- 孤立临时目录（确认 `_find_tasks_jsonl` 为 `None`）：fit 与 calibrate 均 ValueError
- **祖先绑定：** 父目录写入对调 premise 序的 `tasks.jsonl`，并另放 `parent/col/tasks.jsonl`。给定 feat/labs **没有**任务文件。`_find_tasks_jsonl` 仍为 `None`；fit/calibrate 仍 ValueError，**没有**吃祖先 decoy 列序
- 有本题 `tasks.jsonl`：CLI `scores=[0.1]`，不是首次出现序的 `0.2`

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C15-U-01 | Low | 事件均值聚合不把 `behavior_unknown` / `null_reason` 提到顶层；CLI label 顶层 `behavior_unknown is None`，事件层才是 True | `measure.py` 112–116 | \(\rho_M\) 已是 null，未记成 1.0 |
| C15-U-02 | Low | 只传 `rng`、不传 `groups` 时仍 bootstrap \(\rho\) 均值 | `analysis.py` 87–88 | CLI `analyze` 有表时始终传 `groups` |
| C15-U-03 | Medium | 同一事件同时有映射真实 hit 与 `sham:` 行时，`_has_sham_row` 先于 mapped hits，丢掉 \(N=\{p3\}\) | `measure.py` 346–351 | 指定 C7-M-01 是「仅映射 \(N=\{p3\}\)」；A13-03 是「仅 sham」。混合行不是默认 `build_labels` 产物（真实前提 `noise_ref` 保持 None） |
| C15-U-04 | Low | P2 不在支持集上重算 \(\rho\)；`0.9` 对分母 4 仍 `ok` | `analysis.py` 160–168 | 支持集存在性与整数一致性已关 asked 项 |
| C15-U-05 | Low | `excess==0` 自动 `c3_negative_descriptive`+跳过 P2/P3 | `analysis.py` 244–256 | Gate 默认仍 `unregistered`。无发明通过线 |
| C15-U-06 | Low | `_e_premise_ids` 在已有 `task.premises` 后仍按 labels 首次出现 **追加** 未出现的真实 premise_id | `cli.py` 703–712 | 指定攻击是「无本题 tasks.jsonl」。追加列若 \(j\ge E.shape[0]\) 会被跳过 |
| C15-U-07 | Low | `sequence_score` 默认 `nonconformity="prob"`（\(\max p\)）不是命题 2 的 \(\max(1-p)\) | `calibrate.py` 13–26 | CLI calibrate 显式传 `one_minus_p` |
| C15-U-08 | Low | 矩阵密度 API 把 unknown 编成 `0` 时 \(\rho_M=1.0\)；编成 `-1` 才排除 | `measure.py` 167–200 | 生产 label/analyze 走集合 API + `behavior_unknown`。指定 A13-02 在该路径关闭 |
| C15-U-09 | Low | 仓库测试 `test_fit_does_not_bind_ancestor_col_tasks` 把 decoy 写在**兄弟** `work/col`，不是给定目录的祖先 | `tests/test_round07_regressions.py` 48–77 | 本通道把 decoy 放进**父目录** `tasks.jsonl` 与 `parent/col/tasks.jsonl` 后仍 ValueError |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C15-S-01 | 真实轨迹命题 2 覆盖 | 真实 HF 权重 pending_server；tiny 随机权重不是 MODEL-01 |
| C15-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明直接迁移 N/A |
| C15-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）；真实轨迹未跑 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`；`fit` 梯度有限差 \(\sim 10^{-8}\)
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64；未知哨兵与 NaN \(H\) 行不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
3. Conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) 拒绝；`predict_set([0.7], 0.3)` 为 True
4. **C7-M-01 关闭：** 映射 \(N=\{p3\}\) 扣除 excess \(=0\)；仅 `sham:` 不记已评估 0
5. **C7-M-02 关闭：** 6 条混合标签、无 `p1_table` → `p1 is None`；毒化列仍忽略
6. **C7-M-03 关闭：** \(n=2,d=5/3\) → `truncated=True`；`eye(4)/eye(3)` → PCA ≠ 切片
7. **C6-M-01 关闭：** 给定目录无 `tasks.jsonl` 时 fit/calibrate ValueError；**祖先 `col` / 父目录任务文件不绑定**；有本题任务文件时 \(a=0.1\) 不是 \(0.2\)
8. **A13-02 关闭：** unknown / \(T\not\subseteq K\) → \(\rho_M\) null，不是 1.0
9. **A13-03 关闭：** 任意 `sham:` 行（含 no-change）不把空 \(N\) 当已评估扣除
10. `direct_transfer` 与 `cmd_analyze` 拒 4096≠3584
11. `_auc` Mann–Whitney，平局 1/2
12. 默认 P1 拒绝无留出；留出 IRLS 不吃 eval \(X\)；能检出被 op 淹没的 \(\rho=y\)
13. **P1 簇重算 \(\Delta\mathrm{AUC}\)：** 独立 IRLS 区间逐位相同，宽度 \(0.588\neq 0\)
14. 假说不要求正 AUC
15. P2 asked 项：无支持集 / 缺测 / 分母不一致
16. P3：`vs_crand`/`vs_clayer`/`vs_baseline`/`nontarget`；`causal_reverse_claim is False`
17. \(\rho_S(T)\) 事件均值 0.25；signed excess 不截断；0-hit → `noise=0`、`excess=raw`
18. TO/CSP 手算微例：\(0.8\) / \(1.0\)
19. INLP \(P=I-uu^\top=I-\hat Z\hat Z^\top\)；C-rand/C-layer 匹配主范数
20. Boundary BCE \(\approx 10.000045\)；Hidden=256
21. **Week-8：** 默认 `unregistered`（**不是缺陷**）；有阈无测 → `threshold_present_measurement_missing`。`scientific_conclusion is None`

---

## 11. 测试质量（仅公式）

作者声称 159 passed。本审查重跑全仓库：**159 passed**。绿测**不能**单独证明公式正确。

- `test_c7_m01_mapped_noise_premise_is_deducted`：**半有效**。只锁集合 API `noise_set=["p3"]`，**不**走 `event_density_sets`。本轮用手建 3 前提 Task 关掉 Label 路径
- `test_analyze_refuses_fake_p1_from_labels`：**有效但偏窄**。4 行、同一 `event_id=q`，只断言 `p1 is None`。本轮用 6 行多事件 + 毒化列加强
- `test_common_dim_marks_truncated_when_n_lt_dim`：**有效**（\(n=2,d=5/3\)）
- `test_p1_bootstrap_interval_is_not_degenerate`：`lo<hi`，能挡住 \([\delta,\delta]\)，无独立 oracle。`test_p1_bootstrap_resamples_delta_auc` 只用 `lo<=hi`，**挡不住**退化区间。本轮独立 IRLS 对上逐位区间
- `test_week8_never_passes_unregistered`：**有效**
- `test_fit_without_tasks_jsonl_refuses_first_seen_order`：**有效但只锁 fit**。本轮另跑 calibrate ValueError + 有任务文件时 \(a=0.1\)
- `test_fit_does_not_bind_ancestor_col_tasks`：**名义强、布置弱**。decoy 写在兄弟 `work/col`，不是给定目录祖先。本轮把 decoy 放进父目录后仍拒绝
- `test_unknown_behavior_is_not_counted_as_m`：**有效但只锁非 exhaustive `no_change`**。本轮另锁 API `behavior_unknown`、部分 \(T\) 覆盖、确认 exhaustive 对照、以及 `label` CLI
- `test_sham_no_change_does_not_book_empty_n`：**有效但只锁 \(\rho_M\)**。本轮另锁 \(\rho_S\) excess null 与「若误记空 \(N\) 会得 excess=1」的对照
- `test_conformal_examples`：**有效但默认 `sequence_score` 用 \(\max p\)**，不是命题 2 的 \(\max(1-p)\)。本轮对 `one_minus_p` 与 9 组 \(k\) 独立关闭

---

## 12. 结论

开审冻结哈希 `401e509b…` **HASH_MATCH**（61 文件）。公式攻击与独立 pytest（159 passed）跑在该树上。交卷前最后一次同一脚本得 `3d0a0764…`，**HASH_MISMATCH**。本通道未改 `src/`、`tests/`、`pyproject.toml`。漂移含 `measure.py` 与 `cli.py`。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\)，未知/NaN 掩码 | **通过** |
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | **通过**（9 组 + 规定 \(q=0.3\)） |
| \(S/M/\rho\) 事件均值；signed excess 不截断；空分母 null | **通过** |
| C7-M-01 映射 \(N=\{p3\}\) 扣除 excess \(=0\)；仅 sham 不记已评估 0 | **通过** |
| C7-M-02 `cmd_analyze` 无 `p1_table` 不从混合标签造 P1 | **通过**（6 行 CLI + 毒化列） |
| C7-M-03 \(n=2,d=5/3\) → `truncated=True`；`eye(4)/eye(3)` 仍 False 且非切片 | **通过** |
| C6-M-01 给定目录无 `tasks.jsonl` → ValueError；祖先 `col` 不得绑定 | **通过**（孤立 + 父目录 decoy + 有任务文件 \(a=0.1\)） |
| A13-02 unknown → \(\rho_M\) null，不是 1.0 | **通过**（API + 部分覆盖 + 生产 labels + CLI） |
| A13-03 sham 空 \(N\) 不得扣除 | **通过**（生产 labels + CLI；对照合法 0-hit） |
| P1 留出 logistic + 簇重算 \(\Delta\mathrm{AUC}\)，区间不是 \([\delta,\delta]\) | **通过**（独立 IRLS 逐位相同，宽度 \(0.588\)） |
| 4096≠3584 直接迁移 N/A | **通过**（库 + CLI） |
| C-rand/C-layer 范数匹配；INLP \(P=I-\hat Z\hat Z^\top\) | **通过** |
| Week-8 无阈值 | **通过**（`unregistered`，**不是缺陷**） |

**验收意见：** `FAIL`（`HASH_MISMATCH`）。开审声明冻结 `401e509b…` **HASH_MATCH**，指定公式反例在该字节上独立核对通过（见上表与 §4）。交卷汇总已漂到 `3d0a0764…`，且漂移包含 `measure.py` / `cli.py`。任务规定 HASH_MISMATCH → FAIL。不得把交卷树或本通道攻击结果记为对声明冻结的连续通过。Gate 保持 `unregistered` 不是缺陷。真实轨迹命题 2 / 注册 Gate 仍属 pending_server。

---

## 附录：61 文件 SHA-256（POSIX relpath，仅 file bytes）

下列 digest 为**开审 / 公式攻击时所读**（汇总 `401e509b…`）。交卷汇总已是 `3d0a0764…`；已变文件见 §1。

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
src/reasoning_diff/models/generate.py  07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844
src/reasoning_diff/models/tiny.py  21725a183452bd06593789217745202863269cd7e9dea1ec144e4bbdb0a1ddb0
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
tests/test_round07_regressions.py  e8ba910213e1ba55ee2d51c7acdd6a539f8b02f1dc275a06f950c5b3c47fe07f
tests/test_science.py  cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```
