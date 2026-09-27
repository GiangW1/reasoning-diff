# C：数学与统计独立审查（round-08）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导 conformal \(k\)、P1 问题级 bootstrap \(\Delta\mathrm{AUC}\)（禁止 \([\delta]*n\)）、有符号 excess、直接迁移 4096→3584 N/A。必须在**当前字节**上独立攻击 C6-M-01：labels 首次出现序 \([p3,p2,p1]\) vs \(E=[p1,p2,p3]\)，\(\hat p=(0.9,0.1,0.8)\)，\(R=\{p1\}\) 必须得 \(a=0.1\) 不得 \(0.2\)；仅含 p2 的 labels 仍须索引 \(E\) 第 1 列。手算微例。Gate 未注册不是缺陷。不发明 Gate 阈值。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读 round-08 的 A/B/D/E/F。`round-06/C-math.md` 仅作猎单，**结论全部由本轮对当前磁盘字节的公式推导与数值反例重做**，不沿用上一轮状态，不采信 ISSUES 的作者 `local close` / `fixed_pending_review`
- 声明冻结哈希：`1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`（`.planning/audits/round-08/VERSION.md`，60 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**是 / HASH_MATCH**；见 §1
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改（只写本文件）
- numpy：1.26.4；CPython 3.11.7

---

## 1. 冻结哈希

范围内文件数：**60**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 17 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「60 files」一致。相对 r06 的 59 文件，多出 `tests/test_round06_regressions.py`。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算（开审第一动作）：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 方法 | SHA-256 | 与声明值 |
|---|---|---|
| VERSION 脚本（开审独立执行） | `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e` | **HASH_MATCH** |

审查过程中同一脚本复算仍等于声明值。公式结论绑定下表 digest（本审查两次完整抽查一致）：

| 文件 | SHA-256（本审查绑定） |
|---|---|
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` |
| `measure.py` | `1fa2360e680d37ad086c9a81b3ec684c9d9d1e73affb0d906ff5a97231986df2` |
| `transfer.py` | `d31bcd499a51ca94c28dca6c97cdbd5c5e3f05db996d15934e5b7d0b5bb22407` |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` |
| `probes/bilinear.py` | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` |
| `probes/boundary.py` | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` |
| `cli.py` | `2f1fac48ebbcf1a1a212307e4981b9f1fa5d6b2013e3944eceedd854704587a4` |

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–102 | `b34ea3e5…` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + 未知哨兵 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed34…` | `sequence_score`/`truth_indices`/`conformal_threshold`/`predict_set` | 全文；手算 \(k\) |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `ce3b549b…` | Hidden=256；BCE 符号 | 全文 |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a…` | `_auc`/`_fit_scores`/`p1_incremental`/`_bootstrap_p1`/`p2_paired`/`p3_recovery`/`cone_fit`/`week8_decision` | 全文；独立 IRLS + 簇重算 \(\Delta\mathrm{AUC}\) |
| `src/reasoning_diff/transfer.py` | 1–75 | `d31bcd49…` | `direct_transfer`/`fit_linear_map`/`_pca_project`/`common_dim_then_procrustes` | 全文；PCA vs 切片 |
| `src/reasoning_diff/measure.py` | 1–346 | `1fa2360e…` | `dependency_densities`/`event_density_sets`/`preservation_to_csp`/`lcs_overlap` | 全文；PITFALLS 微例 + TO/CSP 手算 |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb88…` | `inlp_remove`/`c_rand_delta`/`apply_swap` | 全文 |
| `src/reasoning_diff/cli.py` | `cmd_fit` 564–659；`_e_premise_ids` 665–671；`cmd_calibrate` 683–772；`cmd_analyze` 955–1066 | `2f1fac48…` | 列身份、逐步 \(R(s_i)\)、`direct_transfer(4096,3584)` | 循环复读 + **实际 CLI 反例** |
| `tests/test_science.py` | — | `cdb5f146…` | 校准规定例 / 4096≠3584 | 查是否独立 |
| `tests/test_measure.py` | — | `fbc68abd…` | 负 excess / 零分母 | 集合路径 |
| `tests/test_round05_regressions.py` | — | `bc837c0c…` | bootstrap 状态串 / Gate / `truncated` 旗标 | 查能否锁住宽度与列身份 |
| `tests/test_round06_regressions.py` | 114–127 | `a4421f11…` | C6-M-01 辅助函数 | 查测试能否关闭缺陷 |

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

分母空 → N/A。缺 sham 协议 → excess null（raw 仍可输出）。已评估且 0-hit：\(N=\emptyset\)、\(\rho_S^{\mathrm{noise}}=0\)、excess \(=\) raw，不是缺失。负差不截断。\(\rho_S(T)\) 是事件均值，不是并集一次调用。

PITFALLS 规定例：\(T=\{p1,p2\}\)、\(B=\{p2,p3\}\)、\(P=\{p1,p2,p3,p4\}\) ⇒ \(S=\{p3\}\)、\(M=\{p1\}\)、两密度 \(1/2\)。另：raw \(=0.2\)、noise \(=0.3\) ⇒ excess \(=-0.1\)。

### 3.2 TO / CSP

\[
\mathrm{TO}(T_0,T_{\mathrm{pert}})=\frac{2\cdot\mathrm{LCS}(T_0,T_{\mathrm{pert}})}{|T_0|+|T_{\mathrm{pert}}|},\qquad
\mathrm{CSP}_{\mathrm{matched}}=\frac1{|A_{\mathrm{clean}}|}\sum_{i\in A_{\mathrm{clean}}}\mathbf1[v_i(P')=v_i(P)].
\]

CSP 只在已对齐、父母已知且不交编辑前提的干净事件上计算；同时报告覆盖率与脏事件变化率。

### 3.3 双线性与加权 BCE

\[
\hat p_{ij}=\sigma(h_i^\top U V^\top e_j+b),\quad \lambda_{\mathrm{FN}}=10,\ \mathrm{rank}=64.
\]

\(\mathcal K=\{i:\mathrm{mask}_i\land y_i\in\{0,1\}\}\)；空 \(\mathcal K\) 是 NaN / `no_known_labels`，不是 0。NaN \(H/E\) 行不进 \(\mathcal K\)。

### 3.4 Split conformal 与 \(a(X)\)

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。任务头与行为头应各自标签分别校准。\(j\) 是前提身份在 \(\hat p\) 列上的位置，必须与 \(E\) 行（`task.premises` 顺序）对齐，**不能**是 `labels.jsonl` 首次出现序。

规定反例：\(\hat p=(0.9,0.1,0.8)\)，\(E=(p1,p2,p3)\)，\(R=\{p1\}\) ⇒ \(a=1-0.9=0.1\)。若误用首次出现序 \([p3,p2,p1]\)，\(p1\) 下标 2，吃到 \(0.8\)，得 \(0.2\)。仅观察到 p2 时，p2 仍须是 \(E\) 列 1。

### 3.5 P1–P3

- **P1：** train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题上 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：重采样基础题，**每次重算** \(\Delta\mathrm{AUC}\)。禁止 \([\delta]*n\)。假说不要求 \(\Delta\mathrm{AUC}>0\)。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\) 共用分母；须有 `shared_premises` 且 \(|\mathrm{shared\_premises}|=\) 声称分母。
- **P3：** 相对 C-rand / C-layer；报告非目标与 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

### 3.6 迁移与 S3

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。首批 **4096→3584** 直接模式明确不适用。附录 S3：不同维先学共同维映射，再 Procrustes。共同维必须是拟合（如 PCA），不得静默 `x[...,:k]`。配对行数须相同后才能正交 Procrustes。

### 3.7 Week-8

Gate 0–2 无预注册阈值 → `unregistered`，**不是缺陷**。有阈值无测量 → 不得标 `evaluated` / pass/fail。有阈值且有测量 → 比较并记录 side。`scientific_conclusion` 保持 `None`。本审查不发明阈值。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（误差 0） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(1.2272895322281534\) | **通过** |
| CHK-04 | `y=-1` / 空 mask | 直接调用 | **通过**：`-1` 排除后 \(10(-\log 0.8)=2.231435513142097\)；空 mask → NaN |
| CHK-05 | `fit` 空 \(\mathcal K\) | `Y=-1` | **通过**：`no_known_labels`，`loss=None` |
| CHK-06 | `U00` 有限差 | 一步 vs \(\pm\varepsilon\) | **通过**：一步 \(\Delta U_{00}=+0.125\)（`lr=0.1`）与数值梯度 \(-1.2500000004\) 一致，相对误差 \(\sim 3\times10^{-10}\) |
| CHK-07 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | \(N=4,\alpha=0.4\Rightarrow k=3,q=0.3\)；\(\alpha=0.1\Rightarrow+\infty\)；\(N=1,\alpha=0.05\Rightarrow+\infty\)；\(N=3,\alpha=0.5\Rightarrow k=2,q=0.2\)；\(N=10,\alpha=0.05\Rightarrow+\infty\)；\(\alpha=0\Rightarrow+\infty\) | **通过** |
| CHK-08 | \(\alpha\ge1\)、\(\alpha<0\)、空袋 | 直接调用 | **通过**（`invalid`） |
| CHK-09 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**（`+1e-12` 后 True） |
| CHK-10 | 库函数 \(a(X)\) | `[0.9,0.1,0.8]` | **通过**：`truth_indices=[0]` → \(0.1\)；无 indices → \(0.9\)；空真集 → \(0\) |
| CHK-11 | **C6-M-01 规定反例 A（实际 `cmd_calibrate`）** | \(E=I_3\) 对应 \((p1,p2,p3)\)；\(\hat p=(0.9,0.1,0.8)\)（由 \(\mathrm{logit}\) 行经 \(U=V=I\) 重建，最大误差 \(<10^{-15}\)）；labels 行序 \([p3,p2,p1]\)；`tasks.jsonl` 前提序 \([p1,p2,p3]\)；事件 `s1` 祖先 \(\{p1\}\) | **通过**：`_e_premise_ids` → `[p1,p2,p3]`；逐步循环 `truth_i=[0]`；CLI `scores=[0.1]`。旧首次出现序仍为 `0.2` |
| CHK-12 | **C6-M-01 仅 p2 labels（实际 CLI）** | 同上 pred；labels 只有 `{p2}`；事件 `s2` 祖先 \(\{p2\}\) | **通过**：`unique.index("p2")==1`（\(E\) 列 1，不是列 0）；循环 `truth_i=[1]`；CLI `scores=[0.9]`（\(1-0.1\)）。旧 `unique=[p2]` 会吃列 0 得 \(0.1\) |
| CHK-13 | 两事件逐步 \(R(s_i)\) + 打乱 labels | \(\hat p_0=(0.9,0.1,0.8)\)、\(\hat p_1=(0.1,0.9,0.8)\)，\(R=\{p1\},\{p2\}\) | **通过**：CLI `scores=[0.1]`。旧并集仍为 \(0.9\) |
| CHK-14 | `cmd_fit` 的 \(Y\) 列身份 | 包装 `BilinearProbe.fit` 截获 \(Y\)；labels 行序 \([p3,p2,p1]\) | **通过**：\(Y[0]=(1,0,0)\)，p1 在列 0，p2 列 1，p3 列 2 |
| CHK-15 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`apply_map` 形状错；`cmd_analyze` | **通过**（库与 CLI 均为 `not_applicable_dimension_mismatch`；错形状 `ValueError`，无静默切片） |
| CHK-16 | labeled 缺张量；监督 vs 无标签 | `labels=None`；平移配对 | **通过**：拒绝无标签张量。unlabeled / supervised 分列，\(W\) 不相同 |
| CHK-17 | 常数 AUC；Mann–Whitney 平局 | `_auc` | **通过**（常数 0.5；手算 \(4/6+0.5/6=0.75\)，代码 0.75） |
| CHK-18 | 默认 P1；留出 logistic；`precomputed` | \(n=40\)，`len≡10`，`op~N(0,1000)`，`rho=y` | **通过**：默认 `requires_held_out`。留出 `auc_full=1`，`auc_base=0.71`，\(\delta=0.29\)。`precomputed`：`delta=0.5` |
| CHK-19 | 留出拟合是否忽略 eval \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 差 0；eval 变 \(0.209\)） |
| CHK-20 | 空/满 `held_out` | 省略 `held_out` | **通过**（`requires_held_out`） |
| CHK-21 | **P1 bootstrap 是否重算 \(\Delta\mathrm{AUC}\)** | 同上，`groups=i//2`，独立 IRLS 簇重算，同一 `rng(0)` | **通过**：代码区间 \([0.07372222222222223, 0.7262731481481484]\)，宽度 \(0.65255\)，`status=resampled_delta_auc`，\(n=200\)。独立同算法区间、均值 **逐位相同**。不是 \([\delta,\delta]\)（固定 \(\delta\) 重放宽度 \(0\)） |
| CHK-22 | 仅传 `rng`、不传 `groups` | 同上 | **残留**（C8-U-02）：bootstrap 的是 \(\rho\) 均值 \(0.5\)，区间 \([0.35,0.625]\)，不是 \(\Delta\mathrm{AUC}\)。CLI `analyze` 始终传 `groups` |
| CHK-23 | 假说不要求正 AUC | \(\rho\sim N(0,1)\) 与 \(y\) 无关 | **通过**：`delta_auc=-0.17`，`status=estimate`，不拒绝 |
| CHK-24 | P2 减法、None、支持集 | `p2_paired` | **asked 项通过**：无支持集 → `denominator_unverified`；`None` + 匹配支持集 → `missing_pair`；`99` vs 1 元列表 → `denominator_inconsistent`；有支持集差值 \(0.3/-0.2\)。**残留**：`0.9` 对分母 4 仍 `ok` |
| CHK-25 | P3 相对对照、非目标、禁句 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline_acc=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`nontarget=0.2`，`causal_reverse_claim is False` |
| CHK-26 | PITFALLS \(S/M\)；有符号 excess；0-hit；并集 vs 均值 | 手算 | **通过**：无 sham → raw \(0.5/0.5\)、excess null。raw \(0.2\) noise \(0.3\) → excess \(-0.1\)，不截断。0-hit → `noise=0`、`excess=0.5`（=raw）。两事件 \(1/2\) 与 \(0\) → 均值 **0.25** |
| CHK-27 | 矩阵缺 noise | `task=[[0,1,0]]` | **通过**：S 的 noise/excess 均为 `None` |
| CHK-28 | TO/CSP 微例 | tokens \([1,2,3,4,5]\) vs \([1,2,9,4,5]\)；干净 \(s_0\) 值不变、脏 \(s_1\) 变 | **通过**：手算 \(\mathrm{TO}=2\cdot4/10=0.8\)，\(\mathrm{CSP}=1\)。代码 `to_all=0.8`，`csp=1.0`，`dirty_change_rate=1.0`，`clean_alignment_coverage=1.0` |
| CHK-29 | INLP 更新 \(H\) | \(H=[[2,0],[2,0],[0,1],[0,1]]\) | **通过**：一步 \(HP=[[1.6,0.8],\ldots]\)；8 步 \(\|HP\|\approx0\) |
| CHK-30 | C-rand 匹配主范数；交换 | 强制 `target_norm`；\(e_1+\Pi(e_2-e_1)\) | **通过**（缺范数拒绝；`actual_norm≈3`；交换得 donor） |
| CHK-31 | Boundary Hidden=256；BCE 符号 | `hidden=128` 拒绝；\(y=0,p=\sigma(10)\) | **通过**：报告 \(10.000045398900186\)，与真 BCE 相同 |
| CHK-32 | `cone_fit` 是否拟合 | \(y=1-e^{-0.8(1-x)^{1.5}}\)，\(n=12\) | **通过**：`r2=0.9776421802579095`，\((\hat\lambda,\hat\gamma)=(0.6812920690579611,1.2)\)；`wording=descriptive_only` |
| CHK-33 | S3 共同维是否切片 | 配对 \((8,4)/(8,3)\) | **通过（非截断）**：`a_map=pca`；PCA 与 `a[:,:3]` 最大差 \(5.79\)。等行后 Procrustes `adapted_geometry`。`truncated=False` 为写死旗标（C8-U-05） |
| CHK-34 | Week-8 阈值比较 | 默认 / 有阈无测 / 有阈有测；`cmd_analyze` | **通过**：默认三门 `unregistered`，`scientific_conclusion is None`。有阈无测 → `threshold_present_measurement_missing`。`rho_S_excess=0.1` vs \(0.9\) → `compared/below`。不发明 pass/fail |
| CHK-35 | `pytest` 数学相关 + 全仓库 | 七文件后全仓库 | 数学七文件 **116 passed**。全仓库 **144 passed**。作者声称 144 passed **本轮成立** |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | 真实 HF 权重属 pending_server；本轮只验证公式与 CLI 列身份 |
| 阅读其他 round-08 通道 | 任务禁止 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用分数值域、污染 eval \(X\)、检出 \(\rho=y\)、独立同算法区间代替 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\) |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | \(0\le\alpha<1\) 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | 一步 \(HP\) 与手算一致 |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm`；本轮范数匹配 |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels` |
| C2-M-02 默认 P1 非留出 | **关闭** | 省略 `held_out` 且非 `precomputed` → `requires_held_out` |
| C3-M-02 P1 非 logistic / `precomputed` 魔法系数 | **关闭** | IRLS；`precomputed` 是调用方分数 |
| C2-M-03 `1-0.7≰0.3` | **关闭** | `q+1e-12` |
| C3-M-01 并集 \(\rho_S(T)\) | **关闭** | 两事件现得 0.25 |
| C2-M-05 监督/无标签同一 lstsq | **关闭（估计程序）** | 无标签 Procrustes；监督加权 lstsq；\(W\) 不同 |
| C2-M-06 P2 `None` TypeError | **关闭** | `missing_pair` |
| C3-M-03 共享分母 | **关闭 asked 项** | 无支持集 / 不一致均拒绝 |
| C3-M-04 / C4-M-02 / C5-M-02 \(a(X)\) 并集 | **关闭（逐步 \(R(s_i)\)）** | 对齐 \(E\) 时 CLI \(a=0.1\) |
| C3-M-05 P3 非目标 | **关闭（接口）** | 字段存在 |
| C4-M-01 0-hit → excess null | **关闭** | `noise=0`，`excess=raw` |
| C4-M-03 Boundary BCE 符号 | **关闭** | \(+10.000045398900186\) |
| `cone_fit` 空壳 | **关闭** | grid 拟合 |
| **C5-M-01** P1 bootstrap \([\delta]*n\) | **关闭** | 见 CHK-21。不采信 ISSUES；本轮独立复算 |
| **C6-M-01** `truth_indices` 用 labels 首次出现序 | **关闭（指定反例）** | 见 CHK-11/12/14。有 `tasks.jsonl` / \(E\) 身份时 CLI \(a=0.1\)，仅 p2 索引列 1，fit \(Y\) 跟 `task.premises`。不采信作者 close |

---

## 7. 发现

本轮**无新的 confirmed defect**。C6-M-01 规定反例在当前字节上关闭。

指定攻击（本审查实际执行，不采信 ISSUES）：

- \(\hat p=\sigma(\mathrm{logit}(0.9,0.1,0.8))\)，\(E=I_3\) 对应 \((p1,p2,p3)\)
- labels 磁盘行序 \([p3,p2,p1]\)
- `Task.premises` 序 \([p1,p2,p3]\)，`graph_kind=arithmetic_dag`，`ancestors(s1)=\{p1\}`
- 论文：\(a=1-0.9=0.1\)
- 旧缺陷：`dict.fromkeys` 首次出现序下 p1 下标 2，\(a=1-0.8=0.2\)
- **当前 `cmd_calibrate`：`scores=[0.1]`**
- 仅 `{p2}` labels：`_e_premise_ids` 仍为 `[p1,p2,p3]`，`index("p2")==1`；CLI \(a=0.9=1-0.1\)，不是列 0 的 \(0.1\)
- `cmd_fit` 截获 \(Y[0]=(1,0,0)\)：p1 进入列 0

`_e_premise_ids`（`cli.py` 665–671）先写 `task.premises`，再追加 labels 中未见且非 `sham:` 的 id。`cmd_fit` / `cmd_calibrate` 共用该函数。

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C8-U-01 | Medium | 无 `tasks.jsonl` 时 `_e_premise_ids(None, labels)` 退回首次出现序。若 `event_rows.node_id` 恰好是前提 id（如 `p1`），本审查复现 CLI `scores=[0.2]`。若 `node_id` 是图节点（`s1`），祖先空、`truth_i` 空，按空真集记 \(a=0\)（未知当空集） | `cli.py` 665–671、741–758 | 指定 C6-M-01 反例以 \(E=[p1,p2,p3]\) 为前提，依赖 `task.premises`。生产 `calibrate` 会搜 `prepare/` / `s-prep/`。缺任务文件时本应拒绝校准，而不是静默首次出现序或 \(a=0\) |
| C8-U-02 | Low | 只传 `rng`、不传 `groups` 时仍 bootstrap \(\rho\) 均值 | `analysis.py` 87–88 | CLI `analyze` 始终传 `groups`，走 `_bootstrap_p1` |
| C8-U-03 | Low | P2 不在支持集上重算 \(\rho\)；`0.9` 对分母 4 仍 `ok` | `analysis.py` 160–168 | 支持集存在性与整数一致性已关 asked 项 |
| C8-U-04 | Low | `excess==0` 自动 `c3_negative_descriptive`+跳过 P2/P3 | `analysis.py` 244–256 | Gate 默认仍 `unregistered`。无发明通过线 |
| C8-U-05 | Low | `truncated: False` 写死，不由实现推断 | `transfer.py` 75 | 当前路径确为 PCA，不是切片 |
| C8-U-06 | Low | `event_sets` 对 None 密度跳过再平均：`[None, 1]` → `1.0` | `measure.py` 109–111 | 分母为空记 N/A 后，\(n\) 是否含 N/A 步原文未写死 |
| C8-U-07 | Low | 0-hit 时 `rho_M_noise=\|T\setminus N\|/\|T\|=1` | `measure.py` 139 | 论文对 \(\rho_M\) 噪声参照没有写出与 \(\rho_S\) 对称的集合公式。S 的 noise=0 已对 |
| C8-U-08 | Low | `sequence_score` 默认 `nonconformity="prob"` 是 \(\max p\) 不是 \(\max(1-p)\) | `calibrate.py` 24–26 | CLI 始终传 `one_minus_p` |
| C8-U-09 | Low | calibrate 仍 `task_label==1 or behavior_label==1`，且 `rsi` 含 `{nid}` | `cmd_calibrate` 751–757 | 任务/行为应分头校准。本轮清单主问列身份 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C8-S-01 | 真实轨迹命题 2 覆盖 | 真实 HF 权重 pending_server；tiny 随机权重不是 MODEL-01 |
| C8-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明直接迁移 N/A |
| C8-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）；真实轨迹未跑。库层 bootstrap 现可重算 \(\Delta\mathrm{AUC}\) |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`；`fit` 梯度有限差 \(\sim 3\times10^{-10}\)
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64；未知哨兵不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
3. Conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) 拒绝
4. `predict_set([0.7], 0.3)` 为 True
5. `sequence_score(..., truth_indices=[0])` 得 \(0.1\)；空真集得 \(0\)
6. **C6-M-01 关闭（指定反例）：** labels 首次出现 \([p3,p2,p1]\) 时 CLI \(a=0.1\) 不是 \(0.2\)；仅 p2 索引 \(E\) 列 1；fit \(Y\) 跟 premises
7. 两事件逐步 \(R(s_i)\)，CLI \(a=0.1\)（并集仍关）
8. `direct_transfer` 与 `cmd_analyze` 拒 4096≠3584
9. `_auc` Mann–Whitney，平局 1/2
10. 默认 P1 拒绝无留出；留出 IRLS 不吃 eval \(X\)；能检出被 op 淹没的 \(\rho=y\)
11. **C5-M-01 仍关：** 簇重采样后重算 \(\Delta\mathrm{AUC}\)；独立实现区间逐位相同；宽度 \(0.65255\neq0\)
12. 假说不要求正 AUC：噪声 \(\rho\) 的 \(\delta=-0.17\) 仍 `estimate`
13. P2 asked 项：无支持集 / 缺测 / 分母不一致
14. P3：`vs_crand`/`vs_clayer`/`vs_baseline`/`nontarget`；`causal_reverse_claim is False`
15. \(\rho_S(T)\) 事件均值 0.25；signed excess \(-0.1\) 不截断；0-hit → `noise=0`、`excess=raw`
16. TO/CSP 手算微例：\(0.8\) / \(1.0\)
17. INLP 在已投影 \(H\) 上迭代；C-rand 匹配主范数
18. Boundary BCE \(+10.000045\)；Hidden=256
19. `cone_fit` 真正拟合；措辞 `descriptive_only`
20. **S3 不是静默截断：** PCA 投影，等行后 Procrustes
21. **Week-8：** 默认 `unregistered`（**不是缺陷**）；有阈无测 → `threshold_present_measurement_missing`；有阈有测 → `compared` + side。`scientific_conclusion is None`。不发明阈值

---

## 11. 测试质量（仅公式）

作者声称 144 passed。本审查重跑全仓库：**144 passed**。绿测**不能**单独证明公式正确。

- `test_truth_indices_follow_e_columns_not_label_order`：**半有效**。用 `SimpleNamespace` 锁 `_e_premise_ids` 与 `sequence_score` 的 \(0.1\) vs \(0.2\) 对照，以及 `only_last.index("p2")==1`。**不跑 `cmd_calibrate`**，不锁无 `tasks.jsonl` 回退。本轮用真实 `Task` + 实际 CLI 关掉指定反例
- `test_p1_bootstrap_resamples_delta_auc`：锁 `status==resampled_delta_auc` 与 `lo<=hi`，**不锁区间宽度**，也不对照独立 \(\Delta\mathrm{AUC}\) oracle
- `test_p1_bootstrap_interval_is_not_degenerate`：`lo<hi`，能挡住 \([\delta,\delta]\)，仍无独立 oracle。本轮生产路径已用独立 IRLS 对上逐位区间
- `test_week8_threshold_without_metric_is_not_evaluated` / `test_week8_never_passes_unregistered`：**有效**
- `test_common_dim_is_not_silent_truncate`：**弱**。只查 `truncated is False` / `a_map==pca`。`eye(4)` vs `eye(3)` 行数不同，Procrustes 走 `not_applicable_shape_mismatch`。本轮用等行 \((8,4)/(8,3)\) 与 PCA-vs-切片差独立关闭“静默截断”
- `test_c3_m01_event_mean_not_union` **有效**（0.25）
- `test_evaluated_zero_hit_sham_is_zero_noise_not_null`：**API 半有效**

---

## 12. 结论

开审冻结哈希 `1b88bec…` **HASH_MATCH**（60 文件）。审查绑定该声明快照的公式库 digest。作者 pytest 声称 144 passed；本审查全仓库 **144 passed**。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| \(S/M/\rho\) 事件均值；signed excess 不截断；0-hit noise=0 | 通过 |
| TO/CSP 手算微例 | 通过 |
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | 通过 |
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | **通过**（独立手算 9 组全匹配） |
| \(a(X)=\max_{j\in R(s_i)}(1-p)\) 逐步 \(R(s_i)\) + 列身份 | **通过**。C6-M-01 指定反例 CLI \(a=0.1\) 不是 \(0.2\)；仅 p2 索引列 1 |
| P1 留出 logistic | 通过 |
| P1 问题级 bootstrap 重算 \(\Delta\mathrm{AUC}\) | **通过**（独立 IRLS 区间逐位相同，宽度 \(0.65255\neq0\)） |
| 假说不要求正 AUC | 通过 |
| P2 配对 + 支持集 | asked 项通过 |
| P3 vs 对照 | 通过 |
| 4096≠3584 直接迁移 N/A | **通过**（库 + `cmd_analyze`） |
| S3 共同维不得静默截断 | **通过**（PCA，非切片） |
| Week-8 阈值比较 | **通过**（有阈无测 → `threshold_present_measurement_missing`） |
| Gate 未注册 | **不是缺陷** |

**r06 猎单独立复算（当前字节，不采信作者）：**

| 猎单项 | 本轮 |
|---|---|
| bootstrap 重采样并重算 \(\Delta\mathrm{AUC}\) | **成立**。独立 IRLS 区间逐位相同 |
| CLI calibrate 列身份 / C6-M-01 | **成立（指定反例）**。`[p3,p2,p1]` vs \(E=[p1,p2,p3]\) 得 \(0.1\)；仅 p2 列 1。无 `tasks.jsonl` 且 `node_id` 为前提 id 时仍可能 \(0.2\)（C8-U-01，未升格） |
| Gate 有阈值无测量 → `threshold_present_measurement_missing` | **成立**。有测量时比较 side，不发明 pass/fail |

无仍会污染论文数字的 confirmed defect。C6-M-01 在「\(E\) 身份来自 `task.premises`」的生产路径上关闭。

**验收意见：** `PASS_MATH_STATS`。conformal \(k\)、P1 簇重算 \(\Delta\mathrm{AUC}\)、有符号 excess、4096→3584 N/A、以及 C6-M-01 规定反例均在当前冻结字节上独立核对通过。Gate 保持 `unregistered` 不是缺陷。真实轨迹命题 2 / 注册 Gate 仍属 pending_server，不是本通道公式失败。

---

## 附录：60 文件 SHA-256（POSIX relpath，仅 file bytes）

开审汇总哈希为声明值 `1b88bec273d6234e9666fea8e5c6174e2a173f80e0a089ee0ef13541491e257e`。

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc
src/reasoning_diff/cli.py  2f1fac48ebbcf1a1a212307e4981b9f1fa5d6b2013e3944eceedd854704587a4
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
