# C：数学与统计独立审查（round-10）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性 \(\sigma(h^\top UV^\top e+b)\)、\(\lambda_{\mathrm{FN}}=10\)、未知/NaN 掩码、split conformal \(k=\lceil(N+1)(1-\alpha)\rceil\)（\(k>N\Rightarrow+\infty\)）、\(S=B\setminus T\) / \(M=T\setminus B\)、有符号 excess、空分母 null。必须在**当前字节**上独立攻击 C7-M-01 / C7-M-02 / C7-M-03；P1 留出 incremental AUC + 簇 bootstrap 重算 \(\Delta\mathrm{AUC}\)（禁止 \([\delta,\delta]\)）；4096→3584 直接迁移 N/A；C-rand/C-layer 范数匹配；INLP \(P=I-\hat Z\hat Z^\top\)；Week-8 无阈值 → `unregistered`。不发明 Gate 阈值。不采信 ISSUES 作者 close。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读任何 round-10 的 A/B/D/E/F。`round-07/C-math.md` 与 `round-08/C-math.md` 仅作猎单与格式，**结论全部由本轮对磁盘字节的公式推导与数值反例重做**。
- 声明冻结哈希：`813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`（`.planning/audits/round-10/VERSION.md`，61 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**开审 HASH_MATCH**；见 §1
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改 `src/`、`tests/`、`pyproject.toml`（只写本文件）
- numpy：1.26.4；CPython 3.11.7（Anaconda）

---

## 1. 冻结哈希

范围内文件数：**61**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 18 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「61 files」一致。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算（开审第一动作）：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 方法 | SHA-256 | 与声明值 |
|---|---|---|
| VERSION 脚本（开审独立执行） | `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d` | **HASH_MATCH** |

开审汇总哈希等于声明值。公式攻击绑定下表 digest（攻击脚本执行时所读）：

| 文件 | SHA-256（本审查绑定） | 行 |
|---|---|---|
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | 337 |
| `measure.py` | `b15fb8a5bb92220f5693b01acf6b60bd6640b57449e6419cb0e7b2bc6e4b6ba6` | 392 |
| `transfer.py` | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | 86 |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | 45 |
| `probes/bilinear.py` | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | 101 |
| `probes/boundary.py` | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | 44 |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | 115 |
| `cli.py`（analyze 攻击时） | `ba474e1fea1f7c5ab3488c90b32c776862d3651f281be38a543522e9ebeb5e98` | 1251 |

**并发漂移（本通道未改生产字节）：** 审查后半段同一 VERSION 脚本复算先后得到 `7518e20b…` 与 `598e6c8f…`（仍 61 文件）。`cli.py` 后来变为 `175abf12…`；`tests/test_round07_regressions.py` 也变过。复读当时的 `cmd_analyze`：无 `p1_table.jsonl` 仍不从 labels 造 P1。公式库 `analysis` / `measure` / `transfer` / `probes/*` / `interventions` 的 digest 在攻击后复算中未再变。结论绑定上表，不以漂移后的汇总哈希冒充声明冻结。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–101 | `b34ea3e5…` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + NaN 行掩码 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed34…` | `sequence_score`/`conformal_threshold`/`predict_set` | 全文；手算 9 组 \(k\) |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `ce3b549b…` | Hidden=256；BCE 符号 | 全文 |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a…` | `_auc`/`_fit_scores`/`p1_incremental`/`_bootstrap_p1`/`p2_paired`/`p3_recovery`/`week8_decision` | 全文；独立 IRLS 簇重算 \(\Delta\mathrm{AUC}\) |
| `src/reasoning_diff/transfer.py` | 1–86 | `5549f84b…` | `direct_transfer`/`_pca_project`/`common_dim_then_procrustes` | 全文；\(n=2,d=5/3\) 与 `eye(4)/eye(3)` |
| `src/reasoning_diff/measure.py` | 1–392 | `b15fb8a5…` | `dependency_densities`/`event_density_sets`/`lcs_overlap`/`preservation_to_csp` | 全文；C7-M-01 集合 + Label 路径 |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb88…` | `inlp_remove`/`c_rand_delta`/`c_layer_delta`/`apply_swap` | 全文 |
| `src/reasoning_diff/cli.py` | `cmd_fit` 577–671；`_e_premise_ids` 707–716；`cmd_calibrate` 728–805；`cmd_analyze` 1056–1153 | `ba474e1f…` | 无 `p1_table` 不得造 P1；`direct_transfer(4096,3584)` | 循环复读 + **实际 CLI 6 条混合标签** |
| `tests/test_science.py` | — | `cdb5f146…` | 校准规定例 / 4096≠3584 | 查是否独立 |
| `tests/test_round07_regressions.py` | — | 审查中变动 | C7-M-01 集合 API；C7-M-02 4 行 labels；\(n<d\) 旗标 | 查能否锁住指定反例 |

调用链只读：`cli.cmd_fit` / `cmd_calibrate` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文 / 协议：REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / DECIDE-01；PITFALLS 校准 / P1 / P2 / 跨维 / 有符号 excess 条。不发明 Gate 阈值。

### 3.1 \(S/M/\rho\) 与有符号 excess

\[
S(s_i)=R_{\mathrm{behavior}}(s_i)\setminus R_{\mathrm{task}}(s_i),\quad
M(s_i)=R_{\mathrm{task}}(s_i)\setminus R_{\mathrm{behavior}}(s_i),
\]

\[
\rho_S(s_i)=\frac{|S(s_i)|}{|P\setminus R_{\mathrm{task}}(s_i)|},\qquad
\rho_S(T)=\frac1n\sum_i\rho_S(s_i).
\]

\[
\mathrm{excess}=\mathrm{raw}-\mathrm{noise\_reference}.
\]

分母空 → N/A。缺 sham 协议或 `noise_set is None` → excess null（raw 仍可输出）。已评估且 0-hit：\(N=\emptyset\)、\(\rho_S^{\mathrm{noise}}=0\)、excess \(=\) raw，不是缺失。负差不截断。\(\rho_S(T)\) 是事件均值，不是并集一次调用。

PITFALLS 规定例：\(T=\{p1,p2\}\)、\(B=\{p2,p3\}\)、\(P=\{p1,p2,p3,p4\}\) ⇒ \(S=\{p3\}\)、\(M=\{p1\}\)、两密度 \(1/2\)。另：raw \(=0.25\)、noise \(=0.5\) ⇒ excess \(=-0.25\)。

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

### 3.2 TO / CSP

\[
\mathrm{TO}(T_0,T_{\mathrm{pert}})=\frac{2\cdot\mathrm{LCS}(T_0,T_{\mathrm{pert}})}{|T_0|+|T_{\mathrm{pert}}|},\qquad
\mathrm{CSP}_{\mathrm{matched}}=\frac1{|A_{\mathrm{clean}}|}\sum_{i\in A_{\mathrm{clean}}}\mathbf1[v_i(P')=v_i(P)].
\]

CSP 只在已对齐、父母已知且不交编辑前提的干净事件上计算。

### 3.3 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b),\quad \lambda_{\mathrm{FN}}=10,\ \mathrm{rank}=64.
\]

\(\mathcal K=\{i:\mathrm{mask}_i\land y_i\in\{0,1\}\}\)；空 \(\mathcal K\) 是 NaN / `no_known_labels`，不是 0。NaN \(H\) 行 / \(E\) 行不进 \(\mathcal K\)。加权 BCE：

\[
\frac1{|\mathcal K|}\sum_{k\in\mathcal K} w_k\bigl(-y\log p-(1-y)\log(1-p)\bigr),\quad w_k=\lambda_{\mathrm{FN}}\mathbf1[y=1]+1\cdot\mathbf1[y=0].
\]

对 logit 的梯度是 \(w(p-y)\)，与 `fit` 中 `weights * (pred - Y)` 一致。

### 3.4 Split conformal

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。

手算：\(N=4,\alpha=0.4\Rightarrow k=\lceil 5\cdot 0.6\rceil=3\)；分数 \(\{0.4,0.1,0.3,0.2\}\) 排序后 \(q=s_{(3)}=0.3\)。\(N=4,\alpha=0.1\Rightarrow k=5>4\Rightarrow+\infty\)。\(\alpha=0\Rightarrow k=N+1\Rightarrow+\infty\)。

### 3.5 P1–P3

- **P1：** train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题上 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：重采样基础题，**每次重算** \(\Delta\mathrm{AUC}\)。禁止 \([\delta]*n\)。假说不要求 \(\Delta\mathrm{AUC}>0\)。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\)；须有 `shared_premises` 且 \(|\mathrm{shared\_premises}|=\) 声称分母。
- **P3：** 相对 C-rand / C-layer；报告非目标与 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

**C7-M-02：** `cmd_analyze` 无 `p1_table.jsonl` 时不得用 task/behavior 标签冒充 `length≡1` / `op≡0` / \(\rho=\) behavior。\(p1\) 必须保持 `None`。

### 3.6 迁移与 S3

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。首批 **4096→3584** 直接模式明确不适用。附录 S3：不同维先学共同维映射（PCA，不是 \(x[:,:k]\)），再 Procrustes。

**C7-M-03：** \(n=2\)、\(d\in\{5,3\}\) ⇒ \(\min n=2<\mathrm{dim}=3\) ⇒ `truncated=True`。`eye(4)` vs `eye(3)`：\(\min n=3=\mathrm{dim}\) ⇒ `truncated=False`，且 PCA 不得等于前 3 列切片。

### 3.7 INLP / C-rand / C-layer

一步 INLP：\(\hat w=\arg\min\|Hw-y_{\pm1}\|\), \(u=\hat w/\|\hat w\|\), \(P=I-uu^\top\), \(H\leftarrow HP\)。C-rand / C-layer 必须把 \(\Delta\) 缩放到主干预的 `target_norm`；缺范数拒绝。

### 3.8 Week-8

Gate 0–2 无预注册阈值 → `unregistered`，**不是缺陷**。有阈值无测量 → 不得标 `evaluated` / pass/fail。`scientific_conclusion` 保持 `None`。本审查不发明阈值。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（误差 0；\(p=0.1242861816270772\)） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(1.2272895322281534\) | **通过** |
| CHK-04 | `y=-1` / 空 mask | 直接调用 | **通过**：`-1` 排除后 \(10(-\log 0.8)=2.231435513142097\)；空 mask → NaN |
| CHK-04b | NaN \(H\) 行不进 \(\mathcal K\) | `H[1]=[nan,1]` | **通过**：known 仅第一行 |
| CHK-05 | `fit` 空 \(\mathcal K\) | `Y=-1` | **通过**：`no_known_labels`，`loss=None` |
| CHK-06 | `U00` 有限差 | 一步 vs \(\pm\varepsilon\) | **通过**：\(\Delta U_{00}=+0.145501349514177\) 与数值梯度 \(-1.45501349502\) 相对误差 \(\sim 8\times10^{-11}\) |
| CHK-07 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | 9 组；\(N=4,\alpha=0.4\) 分数 \(\{0.4,0.1,0.3,0.2\}\Rightarrow q=0.3\) | **通过**（\(\alpha=0.1/0.05/0\Rightarrow+\infty\)） |
| CHK-08 | \(\alpha\ge1\)、\(\alpha<0\)、空袋 | 直接调用 | **通过**（`invalid`） |
| CHK-09 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**（`+1e-12` 后 True） |
| CHK-10 | 库函数 \(a(X)\) | `[0.9,0.1,0.8]` | **通过**：`truth_indices=[0]` → \(1-0.9=0.1\)（IEEE `0.0999…`）；空真集 → \(0\) |
| CHK-15 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`apply_map`；`cmd_analyze` | **通过**（库与 CLI 均为 `not_applicable_dimension_mismatch`；错形状 `ValueError`） |
| CHK-16 | 监督 vs 无标签 | `labels=None` 拒绝；两路 `W` | **通过**（无标签 Procrustes/lstsq；监督加权 lstsq） |
| CHK-17 | 常数 AUC；Mann–Whitney 平局 | `_auc` | **通过**（常数 0.5；手算 \(7.5/9=0.8333\ldots\)） |
| CHK-18 | 默认 P1；留出 logistic | \(n=40\)，`len≡10`，`op~N(0,1000)`，`rho=y` | **通过**：`auc_full=1`，`auc_base=0.4`，\(\delta=0.6\) |
| CHK-19 | 留出拟合是否忽略 eval \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 差 0；eval 变 \(0.314\)） |
| CHK-20 | 省略 `held_out` | 直接调用 | **通过**（`requires_held_out`） |
| CHK-21 | **P1 bootstrap 是否重算 \(\Delta\mathrm{AUC}\)** | 同上，`groups=i//2`，独立 IRLS 簇重算，同一 `rng(0)` | **通过**：代码区间 \([0.19968749999999996, 0.8418651964918199]\)，宽度 \(0.64218\)，`status=resampled_delta_auc`，\(n=200\)。独立同算法区间、均值 **逐位相同**。不是 \([\delta,\delta]\)（点估计 \(\delta=0.6\)） |
| CHK-22 | 仅传 `rng`、不传 `groups` | 同上 | **残留**（C10-U-02）：bootstrap 的是 \(\rho\) 均值 \(0.5\)，区间 \([0.35,0.625]\)，不是 \(\Delta\mathrm{AUC}\)。CLI `analyze` 有 `p1_table` 时始终传 `groups` |
| CHK-23 | 假说不要求正 AUC | \(\rho\sim N(0,1)\) 与 \(y\) 无关 | **通过**：`delta_auc=-0.05`，`status=estimate` |
| CHK-24 | P2 减法、None、支持集 | `p2_paired` | **asked 项通过**：无支持集 → `denominator_unverified`；`None` → `missing_pair`；分母不一致 → `denominator_inconsistent`；有支持集 \(\Delta\rho=0.3\)、\(\Delta\mathrm{acc}=-0.2\)。**残留**：`0.9` 对分母 4 仍 `ok` |
| CHK-25 | P3 相对对照 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline_acc=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`causal_reverse_claim is False` |
| CHK-26 | PITFALLS \(S/M\)；有符号 excess；0-hit；并集 vs 均值 | 手算 | **通过**：无 sham → raw \(0.5/0.5\)、excess null。raw \(0.25\) noise \(0.5\) → excess \(-0.25\)。空分母 → \(\rho_S\) null。0-hit → `noise=0`、`excess=raw`。两事件 \(1/2\) 与 \(0\) → 均值 **0.25** |
| CHK-27 | 矩阵缺 noise | `task=[[0,1,0]]` | **通过**：S 的 noise/excess 均为 `None` |
| CHK-28 | TO/CSP 微例 | tokens \([1,2,3,4,5]\) vs \([1,2,9,4,5]\)；干净值不变、脏值变 | **通过**：手算 \(\mathrm{TO}=0.8\)，`csp=1.0`，`dirty_change_rate=1.0` |
| CHK-29 | INLP \(P=I-uu^\top\) | \(H=[[2,0],[2,0],[0,1],[0,1]]\), \(y=(1,1,0,0)\) | **通过**：手算 \(w=(1/2,-1)\)，\(P=[[0.8,0.4],[0.4,0.2]]\)，\(HP=[[1.6,0.8],\ldots]\)；8 步 \(\|HP\|\approx 0\) |
| CHK-30 | C-rand/C-layer 匹配主范数 | 强制 `target_norm=3` | **通过**（缺范数拒绝；`actual_norm≈3`） |
| CHK-31 | Boundary Hidden=256；BCE 符号 | `hidden=128` 拒绝；\(y=0,p=\sigma(10)\) | **通过**：\(10.000045398900186\) |
| CHK-32 | `cone_fit` 是否拟合 | \(y=1-e^{-0.8(1-x)^{1.5}}\) | **通过**：`r2=0.9776421802579095` |
| CHK-C7M01-set | 集合 API \(N=\{p3\}\) | `dependency_densities` | **通过**：\(\rho_S^{\mathrm{raw}}=1\)、noise \(=1\)、excess \(=0\)；\(\rho_M^{\mathrm{excess}}=-1\) |
| CHK-C7M01-eds | **C7-M-01 Label 路径** | 自造 3 前提 Task；`noise_ref=1` 仅在 `p3` | **通过**：`event_density_sets` → excess \(=0\)、noise \(=1\)、`null_reason is None` |
| CHK-C7M01-sham | **仅 `sham:` hit** | `sham:ghost` + 行为 \(B=\{p1,p2,p3\}\) | **通过**：事件 `null_reason=noise_set_missing`，excess **null**，**不是** noise \(=0\) / excess \(=1\)。聚合层不复制 `null_reason`（C10-U-01） |
| CHK-C7M01-fb | 无 `event_id` 回退 | 空 event_id + 映射 `p3` | **通过**：excess \(=0\) |
| CHK-C7M01-fbs | 回退仅 sham | 空 event_id + `sham:ghost` | **通过**：excess null，`noise_set_missing` |
| CHK-C7M02 | **无 `p1_table`，6 条混合标签** | 实际 `cli.main(["analyze", …])`：s1/s2/s3 × 混合 0/1 task/behavior | **通过**：`p1 is None`，`status=not_evaluated`，三门 `unregistered`，`scientific_conclusion is None`，transfer 4096→3584 N/A |
| CHK-C7M02b | labels 自带 `length/op/rho/y` | 同一 6 行加上伪造列 | **通过**：仍 `p1 is None`（不读 labels 冒充表） |
| CHK-C7M02c | 有真 `p1_table` | CLI + `problem_id` | **通过**：\(\delta=0.55\)，区间 \([0.245,0.736]\)，`resampled_delta_auc`，不是 \([\delta,\delta]\) |
| CHK-C7M03-n2 | \(n=2,d=5/3\) | `common_dim_then_procrustes` | **通过**：`truncated=True`，`not_applicable_too_few_rows`，`common_dim=3` |
| CHK-C7M03-eye | `eye(4)` vs `eye(3)` | PCA vs \(A[:3,:3]\) | **通过**：`truncated=False`，`a_map=pca`，`b_map=identity`，`adapted_geometry`；\(\|ap-I_3\|_\infty=1.707\) |
| CHK-C7M03-pca8 | 等行 \(8\times4/8\times3\) | PCA vs \(A[:,:3]\) | **通过**：差 \(4.44\)；`truncated=False` |
| CHK-34 | Week-8 | 默认 / 有阈无测 / 有阈有测 | **通过**：默认三门 `unregistered`，`scientific_conclusion is None`。有阈无测 → `threshold_present_measurement_missing`。`0.1` vs \(0.9\) → `compared/below` |
| CHK-35 | `pytest` 全仓库 | 本审查重跑 | **155 passed**（作者声称 153；本通道独立得到 155，不以作者数为准） |

额外攻击（非指定关闭条件，记录）：同一事件上 **映射 `p3` 与 `sham:ghost` 并存** 时，活字节 `event_density_sets` 先走 `elif sham_hits: noise_set=None`，丢掉已映射的 \(N=\{p3\}\)，excess 变 null。指定 C7-M-01 微例（只有映射 \(N=\{p3\}\)，没有 `sham:` 行）不受影响。见 C10-U-03。

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | 真实 HF 权重属 pending_server；本轮只验证公式与 CLI |
| 阅读任何 round-10 其他通道 | 任务禁止 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用分数值域、污染 eval \(X\)、检出 \(\rho=y\)、独立同算法区间代替 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\) |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | \(0\le\alpha<1\) 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | 一步 \(P=I-uu^\top\) 与手算一致 |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm` |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels` |
| C2-M-02 默认 P1 非留出 | **关闭** | 省略 `held_out` → `requires_held_out` |
| C5-M-01 P1 bootstrap \([\delta]*n\) | **关闭** | 见 CHK-21 |
| C6-M-01 列身份 / 首次出现序 | **未作为本轮主攻** | `_e_premise_ids` 仍先写 `task.premises`；本轮主攻 C7 |
| **C7-M-01** 映射 \(N=\{p3\}\) 应扣除；仅 sham 不得记已评估 0 | **关闭（指定反例）** | 集合 API 与 `event_density_sets`（仅 `p3` 的 `noise_ref=1`）得 excess \(=0\)；仅 `sham:ghost` 得 `noise_set_missing`，不是 excess \(=1\) |
| **C7-M-02** 无 `p1_table` 用标签冒充 P1 | **关闭（实际 CLI）** | 6 条混合标签 + 带 `length/op/rho` 的毒化 labels，`p1 is None` |
| **C7-M-03** \(n<\min d\) 仍写 `truncated=False` | **关闭** | \(n=2,d=5/3\) → `truncated=True`；`eye(4)/eye(3)` 仍 False 且 PCA ≠ 切片 |

---

## 7. 发现

本轮**无新的 confirmed defect** 会污染指定论文数字。C7-M-01 / C7-M-02 / C7-M-03 规定反例在所绑定字节上关闭。

指定攻击（本审查实际执行，不采信 ISSUES）：

**C7-M-01**

- 手算：\(P=\{p1,p2,p3\}\), \(T=\{p1,p2\}\), \(B=\{p1,p2,p3\}\), \(N=\{p3\}\) ⇒ excess\(_S=1-1=0\)
- `dependency_densities(..., noise_set=["p3"], noise_evaluated=True)`：excess \(=0\)
- `event_density_sets`：三前提 Task，祖先 \(q\mapsto\{p1,p2\}\)；labels 仅 `p3.noise_ref=1`：excess \(=0\)
- 仅 `sham:ghost`（`noise_ref=1`，真实前提 `noise_ref=None`）：事件 `null_reason=noise_set_missing`，\(\rho_S^{\mathrm{raw}}=1\)，excess **null**。若误记已评估 0，会得到 excess \(=1\)

**C7-M-02**

- 写入 6 行混合 task/behavior（`s1/s2/s3`，标签 0/1 交错），**无** `p1_table.jsonl`
- `python -m` / `cli.main(["analyze", …])` → `report["p1"] is None`，`status=not_evaluated`
- 同一 6 行再写入 `length=1, op=0, rho=behavior, y=task`：仍 `p1 is None`
- 旧缺陷会造出 \(\mathrm{length}\equiv1\)、\(\mathrm{op}\equiv0\)、\(\rho=\) behavior，并可退化成 \([\delta,\delta]\)

**C7-M-03**

- \(A\in\mathbb{R}^{2\times5}\), \(B\in\mathbb{R}^{2\times3}\)：`truncated=True`，`not_applicable_too_few_rows`
- `eye(4)` vs `eye(3)`：`truncated=False`，`a_map=pca`；独立 PCA 与 \(I_3\) 的 \(\ell_\infty=1.707\)，不是静默列切片

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C10-U-01 | Low | 事件均值聚合不把 `null_reason` 提到顶层；仅 sham 时顶层 `null_reason is None`，事件层才是 `noise_set_missing` | `measure.py` 108–112 | excess 已是 null，未记已评估 0 |
| C10-U-02 | Low | 只传 `rng`、不传 `groups` 时仍 bootstrap \(\rho\) 均值 | `analysis.py` 87–88 | CLI `analyze` 有表时始终传 `groups` |
| C10-U-03 | Medium | 同一事件同时有映射真实 hit 与 `sham:` hit 时，`elif sham_hits` 先于 `elif real_hits`，丢掉 \(N=\{p3\}\) | `measure.py` 338–343 | 指定 C7-M-01 是「仅映射 \(N=\{p3\}\)」或「仅 sham」。生产 `build_labels` 不再把 `noise_ref=1` 广播到真实前提，混合行不是默认产物 |
| C10-U-04 | Low | P2 不在支持集上重算 \(\rho\)；`0.9` 对分母 4 仍 `ok` | `analysis.py` 160–168 | 支持集存在性与整数一致性已关 asked 项 |
| C10-U-05 | Low | `excess==0` 自动 `c3_negative_descriptive`+跳过 P2/P3 | `analysis.py` 244–256 | Gate 默认仍 `unregistered`。无发明通过线 |
| C10-U-06 | Low | 生产 `build_labels` 只给 `sham:` 行写 `noise_ref`；CLI prepare/label 默认走「仅 sham」→ excess null，不会自动产生映射 \(N=\{p3\}\) | `measure.py` 72–80 | 映射扣除是 `event_density_sets` 在真实 `premise_id` 上 `noise_ref==1` 的路径；指定微例用手建 Label 关闭 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C10-S-01 | 真实轨迹命题 2 覆盖 | 真实 HF 权重 pending_server；tiny 随机权重不是 MODEL-01 |
| C10-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明直接迁移 N/A |
| C10-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）；真实轨迹未跑 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`；`fit` 梯度有限差 \(\sim 8\times10^{-11}\)
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64；未知哨兵与 NaN \(H\) 行不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
3. Conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) 拒绝；`predict_set([0.7], 0.3)` 为 True
4. **C7-M-01 关闭（指定反例）：** 映射 \(N=\{p3\}\) 扣除 excess \(=0\)；仅 `sham:` 不记已评估 0
5. **C7-M-02 关闭（实际 CLI）：** 6 条混合标签、无 `p1_table` → `p1 is None`；毒化 `length/op/rho` 列仍忽略
6. **C7-M-03 关闭：** \(n=2,d=5/3\) → `truncated=True`；`eye(4)/eye(3)` → `truncated=False` 且 PCA ≠ 切片
7. `direct_transfer` 与 `cmd_analyze` 拒 4096≠3584
8. `_auc` Mann–Whitney，平局 1/2
9. 默认 P1 拒绝无留出；留出 IRLS 不吃 eval \(X\)；能检出被 op 淹没的 \(\rho=y\)
10. **P1 簇重算 \(\Delta\mathrm{AUC}\)：** 独立 IRLS 区间逐位相同，宽度 \(0.642\neq 0\)
11. 假说不要求正 AUC
12. P2 asked 项：无支持集 / 缺测 / 分母不一致
13. P3：`vs_crand`/`vs_clayer`/`vs_baseline`/`nontarget`；`causal_reverse_claim is False`
14. \(\rho_S(T)\) 事件均值 0.25；signed excess 不截断；0-hit → `noise=0`、`excess=raw`
15. TO/CSP 手算微例：\(0.8\) / \(1.0\)
16. INLP \(P=I-uu^\top\)；C-rand/C-layer 匹配主范数
17. Boundary BCE \(+10.000045\)；Hidden=256
18. **Week-8：** 默认 `unregistered`（**不是缺陷**）；有阈无测 → `threshold_present_measurement_missing`。`scientific_conclusion is None`

---

## 11. 测试质量（仅公式）

作者声称 153 passed。本审查重跑全仓库：**155 passed**。绿测**不能**单独证明公式正确。

- `test_c7_m01_mapped_noise_premise_is_deducted`：**半有效**。只锁集合 API `noise_set=["p3"]`，**不**走 `event_density_sets`。本轮用手建 3 前提 Task 关掉 Label 路径
- `test_analyze_refuses_fake_p1_from_labels`：**有效但偏窄**。4 行、同一 `event_id=q`，只断言 `p1 is None`。本轮用 6 行多事件 + 毒化 `length/op/rho` 列加强
- `test_common_dim_marks_truncated_when_n_lt_dim`：**有效**（\(n=2,d=5/3\)）
- `test_common_dim_is_not_silent_truncate`：**弱**。只查 `truncated is False` / `a_map==pca`，不对照切片数值。本轮用 \(\|ap-I_3\|_\infty=1.707\) 与 \(8\times4/8\times3\) 差 \(4.44\) 独立关闭
- `test_p1_bootstrap_interval_is_not_degenerate`：`lo<hi`，能挡住 \([\delta,\delta]\)，无独立 oracle。本轮独立 IRLS 对上逐位区间
- `test_week8_never_passes_unregistered`：**有效**
- `test_sham_hits_do_not_book_evaluated_zero_noise`：**半有效**。锁 `rho_S_noise is None`，不锁「映射 \(N=\{p3\}\) 必须扣除」

---

## 12. 结论

开审冻结哈希 `81308124…` **HASH_MATCH**（61 文件）。公式攻击绑定 §1 表中的库 digest。作者 pytest 声称 153 passed；本审查全仓库 **155 passed**。审查后半段工作区被其他写入者改过（交卷前汇总 `598e6c8f…` / 中间 `7518e20b…`），**本通道未改** `src/`、`tests/`、`pyproject.toml`。`cmd_analyze` 在漂移后的复读中仍不从 labels 造 P1。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\)，未知/NaN 掩码 | **通过** |
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | **通过**（9 组 + 规定 \(q=0.3\)） |
| \(S/M/\rho\) 事件均值；signed excess 不截断；空分母 null | **通过** |
| C7-M-01 映射 \(N=\{p3\}\) 扣除 excess \(=0\)；仅 sham 不记已评估 0 | **通过** |
| C7-M-02 `cmd_analyze` 无 `p1_table` 不从 ≥4 条混合标签造 P1 | **通过**（6 行 CLI + 毒化列） |
| C7-M-03 \(n=2,d=5/3\) → `truncated=True`；`eye(4)/eye(3)` 仍 False 且非切片 | **通过** |
| P1 留出 logistic + 簇重算 \(\Delta\mathrm{AUC}\)，区间不是 \([\delta,\delta]\) | **通过**（独立 IRLS 逐位相同，宽度 \(0.642\)） |
| 4096≠3584 直接迁移 N/A | **通过**（库 + CLI） |
| C-rand/C-layer 范数匹配；INLP \(P=I-uu^\top\) | **通过** |
| Week-8 无阈值 | **通过**（`unregistered`，**不是缺陷**） |

**验收意见：** `PASS_MATH_STATS`。开审冻结 `81308124…` 匹配。指定 C7-M-01/02/03、conformal \(k\)、P1 簇重算 \(\Delta\mathrm{AUC}\)、有符号 excess、4096→3584 N/A、INLP/C-rand、Week-8 未注册门均在所绑定公式字节上独立核对通过。Gate 保持 `unregistered` 不是缺陷。真实轨迹命题 2 / 注册 Gate 仍属 pending_server，不是本通道公式失败。

---

## 附录：61 文件 SHA-256（POSIX relpath，仅 file bytes）

开审汇总哈希为声明值 `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d`。

下列 digest 为公式攻击完成后、交卷前最后一次逐文件读取。`cli.py` 与 `tests/test_round07_regressions.py` 在审查窗口内被其他写入者改过；公式库文件与开审后第一次逐文件哈希一致。

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc
src/reasoning_diff/cli.py  175abf12f4c207c551c6f5c5910b002d62f7f9125f41226389d0acbde4083c17
src/reasoning_diff/edits.py  cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf
src/reasoning_diff/events.py  290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3
src/reasoning_diff/executor.py  481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  b15fb8a5bb92220f5693b01acf6b60bd6640b57449e6419cb0e7b2bc6e4b6ba6
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
src/reasoning_diff/splits.py  08f77e972927a9961885c09e0538f0c43d47ca6638944e1c80465cf6cc4af066
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
tests/test_round06_regressions.py  ac7e4e88248ff49edcd6f992cf48ff88409172c34ce7fa934ca288816fdf946c
tests/test_round07_regressions.py  a59c236d5d007ae77314fe80dee390d30c99e6706c9f285d40a03b4bdbfca328
tests/test_science.py  cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```
