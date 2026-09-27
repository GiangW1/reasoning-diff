# C：数学与统计独立审查（round-06）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导 S/M/\(\rho\)、TO/CSP、P1 留出 logistic + 问题级 bootstrap（必须重算 \(\Delta\mathrm{AUC}\)，不能 \([\delta]*n\)）、P2 分母、P3、conformal \(a(X)\) 与 CLI \(R(s_i)\)、直接迁移 4096/3584、S3 共同维（不得静默截断）、Week-8 阈值比较。手算微例。独立复算 r05 声称：bootstrap 重采样；CLI calibrate 逐步 `truth_indices`；Gate 有阈值无测量 → `threshold_present_measurement_missing`。假说不要求正 AUC。Gate 未注册不是缺陷。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读 round-06 的 A/B/D/E/F。体例对照过 `round-05/C-math.md`，**结论全部由本轮对当前磁盘字节的公式推导与数值反例重做**，不沿用上一轮状态，不采信 ISSUES 的作者 `local close` / `fixed_pending_review`
- 声明冻结哈希：`dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563`（`.planning/audits/round-06/VERSION.md`，59 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**是 / HASH_MATCH（开审时）**；见 §1
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改（只写本文件）
- numpy：1.26.4；CPython 3.11.7

---

## 1. 冻结哈希

范围内文件数：**59**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 16 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「59 files」一致。相对 r05 的 58 文件，多出 `tests/test_round05_regressions.py`。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算（开审第一动作）：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 方法 | SHA-256 | 与声明值 |
|---|---|---|
| VERSION 脚本（开审独立执行） | `dc2ba459d21711e7999f8a9abb8c5dfb3cd8ea1b5740e7f10e5140e87e545563` | **HASH_MATCH** |

审查过程中工作区被**其他写入**改动（本审查未改生产树）。同一脚本随后复算不再等于声明值（曾见 `886c244c…`、`b04c7a66…`）。漂移集中在 `cli.py` 行数增长；下列公式库 digest 在本审查两次完整抽查中不变：

| 文件 | SHA-256（本审查绑定） |
|---|---|
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` |
| `measure.py` | `a6bcd893abedaf3bbe7a4804cde55a78b7d7fc1f68133e3c6643de346eb134dc` |
| `transfer.py` | `d31bcd499a51ca94c28dca6c97cdbd5c5e3f05db996d15934e5b7d0b5bb22407` |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` |
| `probes/bilinear.py` | `52de70553b37dec69822b790b006b7282e58ee926bb77006b3da40b419726e15` |
| `probes/boundary.py` | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` |

`cli.py` 的 \(a(X)\) 逐步循环在复读后与开审文本相同（`rsi` → 逐行 `truth_indices` → `sequence_score`）。公式结论绑定上表 digest；CLI 反例在实际 `cmd_calibrate` 上复跑。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | `52de7055…` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + 未知哨兵 |
| `src/reasoning_diff/probes/calibrate.py` | 1–45 | `e8b3ed34…` | `sequence_score`/`truth_indices`/`conformal_threshold`/`predict_set` | 全文；手算 \(k\)；C4-M-02 原调用 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `ce3b549b…` | Hidden=256；BCE 符号 | 全文 |
| `src/reasoning_diff/analysis.py` | 1–337 | `e4368b0a…` | `_auc`/`_fit_scores`/`p1_incremental`/`_bootstrap_p1`/`p2_paired`/`p3_recovery`/`cone_fit`/`week8_decision` | 全文；独立 IRLS + 簇重算 \(\Delta\mathrm{AUC}\) |
| `src/reasoning_diff/transfer.py` | 1–75 | `d31bcd49…` | `direct_transfer`/`fit_linear_map`/`_pca_project`/`common_dim_then_procrustes` | 全文；PCA vs 切片 |
| `src/reasoning_diff/measure.py` | 1–342 | `a6bcd893…` | `dependency_densities`/`event_density_sets`/`preservation_to_csp`/`lcs_overlap` | 全文；PITFALLS 微例 + TO/CSP 手算 |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb88…` | `inlp_remove`/`c_rand_delta`/`apply_swap` | 全文 |
| `src/reasoning_diff/cli.py` | `cmd_calibrate` / `cmd_analyze` | 漂移中 | 逐行 \(R(s_i)\)、`unique` 索引、`groups` | 循环复读 + 实际 CLI 反例 |
| `tests/test_science.py` | 1–101 | `bed01ffa…` | 校准规定例 / 4096≠3584 | 查是否独立 |
| `tests/test_measure.py` | 1–40 | `fbc68abd…` | 负 excess / 零分母 | 集合路径 |
| `tests/test_review_regressions.py` | — | `d3814498…` | C-01..C-04 | 查测试能否关闭缺陷 |
| `tests/test_round03_regressions.py` | 1–291 | `5698a410…` | 事件均值 / cone | 查是否独立 oracle |
| `tests/test_round04_regressions.py` | — | `25949c80…` | 0-hit / `truth_indices` / P1 字段 | 查是否独立 |
| `tests/test_round05_regressions.py` | 1–190 | `83a665a1…` | bootstrap 状态串 / Gate / `truncated` 旗标 | 查能否锁住宽度与列身份 |

调用链只读：`cli.cmd_fit` / `cmd_calibrate` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文：`Reasoning-Diff-修订方案-v3 (1).md` §2.5–2.6、§3、§5、§7、附录 S2–S3；PITFALLS 校准/P1/P2/跨维条；REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / DECIDE-01。

### 3.1 \(S/M/\rho\)

\[
S(s_i)=R_{\mathrm{behavior}}(s_i)\setminus R_{\mathrm{task}}(s_i),\quad
M(s_i)=R_{\mathrm{task}}(s_i)\setminus R_{\mathrm{behavior}}(s_i),
\]

\[
\rho_S(s_i)=\frac{|S(s_i)|}{|P\setminus R_{\mathrm{task}}(s_i)|},\qquad
\rho_S(T)=\frac1n\sum_i\rho_S(s_i).
\]

分母空 → N/A。缺 sham 协议 → excess null。已评估且 0-hit：\(N=\emptyset\)、\(\rho_S^{\mathrm{noise}}=0\)、excess \(=\) raw，不是缺失。\(\rho_S(T)\) 是事件均值，不是并集一次调用。

PITFALLS 规定例：\(T=\{p1,p2\}\)、\(B=\{p2,p3\}\)、\(P=\{p1,p2,p3,p4\}\) ⇒ \(S=\{p3\}\)、\(M=\{p1\}\)、两密度 \(1/2\)。

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

\(\mathcal K=\{i:\mathrm{mask}_i\land y_i\in\{0,1\}\}\)；空 \(\mathcal K\) 是 NaN / `no_known_labels`，不是 0。

### 3.4 Split conformal 与 \(a(X)\)

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。任务头与行为头**各自**标签分别校准。\(j\) 是前提身份在 \(\hat p\) 列上的位置，必须与 \(E\) 行（`task.premises` 顺序）对齐，不能是 `labels.jsonl` 首次出现序。

### 3.5 P1–P3

- **P1：** train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题上 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：重采样基础题，**每次重算** \(\Delta\mathrm{AUC}\)。禁止 \([\delta]*n\)。假说不要求 \(\Delta\mathrm{AUC}>0\)。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\) 共用分母；须有 `shared_premises` 且 \(|\mathrm{shared\_premises}|=\) 声称分母。
- **P3：** 相对 C-rand / C-layer；报告非目标与 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

### 3.6 迁移与 S3

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。附录 S3：不同维先学共同维映射，再 Procrustes。共同维必须是拟合（如 PCA），不得静默 `x[...,:k]`。配对行数须相同后才能正交 Procrustes。

### 3.7 Week-8

Gate 0–2 无预注册阈值 → `unregistered`，**不是缺陷**。有阈值无测量 → 不得标 `evaluated` / pass/fail。有阈值且有测量 → 比较并记录 side。`scientific_conclusion` 保持 `None`。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（误差 0） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | \(p=(0.8,0.2)\)，\(y=(1,0)\)：手算 \(1.2272895322281534\) | **通过** |
| CHK-04 | `y=-1` / 空 mask | 直接调用 | **通过**：`-1` 排除后 \(10(-\log 0.8)=2.231435513142097\)；空 mask → NaN |
| CHK-05 | `fit` 空 \(\mathcal K\) | `Y=-1` | **通过**：`no_known_labels`，`loss=None` |
| CHK-06 | `U00` 有限差 | 一步 vs \(\pm\varepsilon\) | **通过**（相对误差 \(5.09\times10^{-9}\)） |
| CHK-07 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | \(N=4,\alpha=0.4\Rightarrow k=3,q=0.3\)；\(\alpha=0.1\Rightarrow+\infty\)；\(N=1,\alpha=0.05\Rightarrow+\infty\)；\(N=3,\alpha=0.5\Rightarrow k=2,q=0.2\)；\(N=10,\alpha=0.05\Rightarrow+\infty\)；\(\alpha=0\Rightarrow+\infty\) | **通过** |
| CHK-08 | \(\alpha\ge1\)、\(\alpha<0\)、`None` | 直接调用 | **通过**（`invalid`） |
| CHK-09 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**（`+1e-12` 后 True） |
| CHK-10 | 库函数 \(a(X)\) | `[0.9,0.1,0.8]` | **通过**：`truth_indices=[0]` → \(0.1\)；无 indices → \(0.9\)；空真集 → \(0\) |
| CHK-11 | **r05 C5-M-02 两事件逐步 \(R(s_i)\)** | \(\hat p_0=(0.9,0.1,0.8)\)、\(\hat p_1=(0.1,0.9,0.8)\)，\(R(s_0)=\{p1\}\)、\(R(s_1)=\{p2\}\)；`unique`∥\(E\) | **通过**：逐步循环与实际 CLI 均得 \(a=0.1\)。旧并集仍为 \(0.9\) |
| CHK-12 | `unique` 序 ≠ \(E\) 列 | 同上 pred；`unique=[p3,p2,p1]`；实际 `cmd_calibrate` | **失败**（C6-M-01）：CLI `scores=[0.2]`，论文 \(0.1\) |
| CHK-13 | 仅编辑末前提（`unique=[p2]`） | 默认 `_default_edit` 是 `facts[-1]` | **失败**（C6-M-01）：\(s_1\) 用列 0 得 \(0.9\)，论文 \(0.1\) |
| CHK-14 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`(2,3)@(4,2)` | **通过**（N/A；`matmul` 形状错） |
| CHK-15 | labeled 缺张量 | `labeled=True, labels=None` | **通过** |
| CHK-16 | 监督 vs 无标签 | 平移 \(X'=X+c\) | **通过（程序已分列）**：unlabeled 回收 \(I\)；labeled 不回收。平衡 0/1 权重相同（C6-U-01） |
| CHK-17 | 常数 AUC；Mann–Whitney 平局 | `_auc` | **通过**（0.5；手算 \(0.875\)） |
| CHK-18 | 默认 P1；留出 logistic；`precomputed` | \(n=40\)，`len≡10`，`op~N(0,1000)`，`rho=y` | **通过**：默认 `requires_held_out`。留出 `auc_full=1`，`auc_base=0.71`，\(\delta=0.29\)。`precomputed`：`delta=0.5` |
| CHK-19 | 留出拟合是否忽略 eval \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 差 0；eval 变） |
| CHK-20 | 空/满 `held_out` | 全 True / 全 False | **通过**（`held_out_empty`） |
| CHK-21 | **P1 bootstrap 是否重算 \(\Delta\mathrm{AUC}\)** | 同上，`groups=i//2`，独立 IRLS 簇重算 | **通过（C5-M-01 关闭）**：代码区间 \([0.1109375, 0.7859933]\)，宽度 \(0.675\)，`status=resampled_delta_auc`，\(n=200\)。独立同算法区间**逐位相同**。不是 \([\delta,\delta]\)。r05 式“固定分数、只重采样留出簇”宽度 \(0.351\)，区间 \([0.12, 0.470]\) |
| CHK-22 | 仅传 `rng`、不传 `groups` | 同上 | **残留**（C6-U-02）：bootstrap 的是 \(\rho\) 均值 \(0.5\)，不是 \(\Delta\mathrm{AUC}\)。CLI `analyze` 始终传 `groups` |
| CHK-23 | 假说不要求正 AUC | \(\rho\sim N(0,1)\) 与 \(y\) 无关 | **通过**：`delta_auc=0.010`，`status=estimate`，不拒绝 |
| CHK-24 | P2 减法、None、支持集 | `p2_paired` | **asked 项通过**：无支持集 → `denominator_unverified`；`None` + 匹配支持集 → `missing_pair`；`99` vs 1 元列表 → `denominator_inconsistent`；有支持集差值 \(0.3/-0.2\)。**残留**：`0.9` 对分母 4 仍 `ok` |
| CHK-25 | P3 相对对照、非目标、禁句 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline_acc=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`nontarget=0.2`，`causal_reverse_claim is False` |
| CHK-26 | PITFALLS \(S/M\)；0-hit；并集 vs 均值 | 手算 | **通过**：无 sham → raw \(0.5/0.5\)、excess null。0-hit → `noise=0`、`excess=1`。r03 两事件 \(1/2\) 与 \(0\) → 均值 **0.25** |
| CHK-27 | 集合负 excess、零分母、矩阵缺 noise | 直接调用 | **通过** |
| CHK-28 | TO/CSP 微例 | tokens \([1,2,3,4,5]\) vs \([1,2,9,4,5]\)；干净 \(s_0\) 值不变、脏 \(s_1\) 变 | **通过**：手算 \(\mathrm{TO}=2\cdot4/10=0.8\)，\(\mathrm{CSP}=1\)。代码 `to_all=0.8`，`csp=1.0`，`dirty_change_rate=1.0`，`clean_alignment_coverage=1.0` |
| CHK-29 | INLP 更新 \(H\) | \(H=[[2,0],[2,0],[0,1],[0,1]]\) | **通过**：一步 \(HP=[[1.6,0.8],\ldots]\)；两步 \(\approx0\) |
| CHK-30 | C-rand 匹配主范数；交换 | 独立构造；\(e_1+\Pi_{e_2}(e_2-e_1)\) | **通过**（范数 `isclose`；交换 `[1,1]`） |
| CHK-31 | Boundary Hidden=256；BCE 符号 | \(y=0,p=\sigma(10)\) | **通过**：报告 \(10.000045398900186\)，与真 BCE 相同 |
| CHK-32 | `cone_fit` 是否拟合 | \(y=1-e^{-0.8(1-x)^{1.5}}\)，\(n=12\) | **通过**：`r2=0.9776421802579095`，\((\hat\lambda,\hat\gamma)=(0.6812920690579611,1.2)\)；`wording=descriptive_only` |
| CHK-33 | S3 共同维是否切片 | `eye(4)`/`eye(3)`；配对 \((8,4)/(8,3)\) | **通过（非截断）**：`a_map=pca`；PCA 与 `a[:,:3]` 最大差 \(1.45\) / \(4.32\)。等行配对后 Procrustes `adapted_geometry`，\(R\) 与独立 PCA+Procrustes 差 0。`truncated=False` 为写死旗标（C6-U-05） |
| CHK-34 | Week-8 阈值比较 | 默认 / 有阈无测 / 有阈有测 | **通过**：默认三门 `unregistered`，`scientific_conclusion is None`。有阈无测 → `threshold_present_measurement_missing`。`rho_S_excess=0.1` vs \(0.9\) → `compared/below`；负 \(\Delta\mathrm{AUC}\) → `compared/below`。不发明 pass/fail |
| CHK-35 | `pytest` 数学相关 | 六文件后全仓库 | 数学六文件 **107 passed + 1 failed**（失败项是 collect 行数，非本通道公式）。全仓库 **135 passed, 1 failed**（`test_scientific_collect_h_is_step_boundary_not_last_token`：`10==15`）。作者声称 136 passed **不成立** |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | C6-M-01 下列身份未对齐；真实权重属 pending_server |
| 阅读其他 round-06 通道 | 任务禁止 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用分数值域、污染 eval \(X\)、检出 \(\rho=y\) 代替 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\) |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | \(0\le\alpha<1\) 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | 一步 \(HP\) 与手算一致 |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm`；本轮范数 `isclose` |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels` |
| C2-M-02 默认 P1 非留出 | **关闭** | 省略 `held_out` 且非 `precomputed` → `requires_held_out` |
| C3-M-02 P1 非 logistic / `precomputed` 魔法系数 | **关闭** | IRLS；`precomputed` 是调用方分数 |
| C2-M-03 `1-0.7≰0.3` | **关闭** | `q+1e-12` |
| C3-M-01 并集 \(\rho_S(T)\) | **关闭** | r03 反例现得 0.25 |
| C2-M-05 监督/无标签同一 lstsq | **关闭（估计程序）** | 无标签 Procrustes；监督加权 lstsq |
| C2-M-06 P2 `None` TypeError | **关闭** | `missing_pair` |
| C3-M-03 共享分母 | **关闭 asked 项** | 无支持集 / 不一致均拒绝 |
| C3-M-04 / C4-M-02 / **C5-M-02** \(a(X)\) 并集 | **关闭（逐步 \(R(s_i)\)）** | 对齐 `unique` 时 CLI \(a=0.1\)。列身份见 C6-M-01 |
| C3-M-05 P3 非目标 | **关闭（接口）** | 字段存在 |
| C3-M-07 空袋+hits 伪造 0 | **关闭** | 未评估 → `noise_set_empty` |
| C4-M-01 0-hit → excess null | **关闭** | `noise=0`，`excess=1` |
| C4-M-03 Boundary BCE 符号 | **关闭** | \(+10.000045398900186\) |
| `cone_fit` 空壳 | **关闭** | grid 拟合 |
| **C5-M-01** P1 bootstrap \([\delta]*n\) | **关闭** | 见 CHK-21。不采信 ISSUES；本轮独立复算 |

---

## 7. 发现

状态：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

### C6-M-01 — CLI \(a(X)\) 的 `truth_indices` 是 `labels.jsonl` 首次出现序，不是 \(E\) 列（前提身份）

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `cli.cmd_calibrate`（复读后约 667–694）；`unique = dict.fromkeys(premise_id)`；`sequence_score(..., truth_indices=truth_i)`。`predict_matrix` 的列 \(j\) = `E` 行 \(j\) = `task.premises` 顺序。`_default_edit` 取 `facts[-1]`
- **原文：** §2.5：\(a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij})\)。\(j\) 是真依赖前提在探针输出中的列
- **反例 A（实际 CLI，本审查执行）：**
  - \(\hat p=\begin{bmatrix}0.9&0.1&0.8\\0.1&0.9&0.8\end{bmatrix}\)，\(E=I_3\) 对应 \((p1,p2,p3)\)
  - \(R(s_0)=\{p1\}\)、\(R(s_1)=\{p2\}\)
  - 论文：\(a=\max(1-0.9,1-0.9)=0.1\)
  - `unique=[p1,p2,p3]`（与 \(E\) 对齐）：CLI `scores=[0.1]` **正确**
  - `unique=[p3,p2,p1]`（仅打乱 labels 行序）：CLI `scores=[0.2]`。\(p1\) 的 unique 下标是 2，用了第三列 \(0.8\)
- **反例 B（默认编辑路径）：** `unique=['p2']`（只观察到末前提）
  - \(s_1\) 的 `truth_i=[0]`，取 \(\hat p_{1,0}=0.1\) ⇒ \(a=0.9\)
  - 论文应对 \(p2\) 列取 \(1-0.9=0.1\)
  - `_default_edit` 返回最后一个 fact，生产 `unique` 很容易从末前提起算
- **对照：** 逐步 \(R(s_i)\) 本身已实现（C5-M-02 并集关闭）。本条是列身份，不是并集
- **影响：** 命题 2 的 \(q_\alpha\) 会吃到错误前提的 \(1-\hat p\)。`cmd_fit` 用同一 `unique` 填 \(Y\)，与 \(E\) 行也不对齐
- **修复：** `truth_indices` 必须是前提 ID 在 \(E\)/premises 中的下标，禁止用 labels 首次出现序

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C6-U-01 | Medium | 监督适配用 \(\sqrt{\|y-\bar y\|+0.1}\)；平衡 0/1 的任意排列 \(W\) 相同 | `transfer.py` 25–28 | 估计程序已与 unlabeled 分列。非等权标签才会改 \(W\) |
| C6-U-02 | Low | 只传 `rng`、不传 `groups` 时仍 bootstrap \(\rho\) 均值 | `analysis.py` 87–88 | CLI `analyze` 始终传 `groups`，走 `_bootstrap_p1` |
| C6-U-03 | Low | P2 不在支持集上重算 \(\rho\)；`0.9` 对分母 4 仍 `ok` | `analysis.py` 160–168 | 支持集存在性与整数一致性已关 asked 项 |
| C6-U-04 | Low | `excess==0` 自动 `c3_negative_descriptive`+跳过 P2/P3 | `analysis.py` 244–256 | Gate 默认仍 `unregistered`。无发明通过线。PITFALLS 写过未定义判据不得自动跳过 |
| C6-U-05 | Low | `truncated: False` 写死，不由实现推断 | `transfer.py` 75 | 当前路径确为 PCA，不是切片 |
| C6-U-06 | Low | `event_sets` 对 None 密度跳过再平均：`[None, 1]` → `1.0` | `measure.py` 109–111 | 分母为空记 N/A 后，\(n\) 是否含 N/A 步原文未写死 |
| C6-U-07 | Low | 0-hit 时 `rho_M_noise=\|T\setminus N\|/\|T\|=1` | `measure.py` 139 | 论文对 \(\rho_M\) 噪声参照没有写出与 \(\rho_S\) 对称的集合公式。S 的 noise=0 已对 |
| C6-U-08 | Low | `t1_tiny` 上 0-hit 回归因夹具无 p3、分母空而 `rho_S is None` | `event_density_sets` | 生产三前提构造已对 |
| C6-U-09 | Low | calibrate 仍 `or behavior_label==1`，且 `rsi` 含 `{nid}` | `cmd_calibrate` | 在 `p in rsi` 过滤后，非祖先行为边进不来。任务/行为应分头校准，原文有要求但本轮清单主问逐步 \(R(s_i)\) |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C6-S-01 | 真实轨迹命题 2 覆盖 | C6-M-01 下列身份未对齐 |
| C6-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明直接迁移 N/A |
| C6-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）；真实轨迹未跑。库层 bootstrap 现可重算 \(\Delta\mathrm{AUC}\) |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`；`fit` 梯度有限差 \(5.09\times10^{-9}\)
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64
3. 未知哨兵不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
4. Conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) 拒绝
5. `predict_set([0.7], 0.3)` 为 True
6. `sequence_score(..., truth_indices=[0])` 得 \(0.1\)；空真集得 \(0\)
7. **C5-M-02 并集（对齐 unique 时）关闭：** 两事件逐步 \(R(s_i)\)，CLI \(a=0.1\)
8. `direct_transfer` 拒 4096≠3584
9. `_auc` Mann–Whitney，平局 1/2
10. 默认 P1 拒绝无留出；留出 IRLS 不吃 eval \(X\)；能检出被 op 淹没的 \(\rho=y\)
11. **C5-M-01 关闭：** 簇重采样后重算 \(\Delta\mathrm{AUC}\)；独立实现区间逐位相同；宽度 \(0.675\neq0\)
12. 假说不要求正 AUC：噪声 \(\rho\) 的 \(\delta\approx0.01\) 仍 `estimate`
13. P2 asked 项：无支持集 / 缺测 / 分母不一致
14. P3：`vs_crand`/`vs_clayer`/`vs_baseline`/`nontarget`；`causal_reverse_claim is False`
15. \(\rho_S(T)\) 事件均值 0.25；0-hit → `noise=0`、`excess=1`
16. TO/CSP 手算微例：\(0.8\) / \(1.0\)
17. INLP 在已投影 \(H\) 上迭代
18. C-rand 匹配主范数；交换 \(H+\Pi_Z(H_d-H_b)\)
19. Boundary BCE \(+10.000045\)；Hidden=256
20. `cone_fit` 真正拟合；措辞 `descriptive_only`
21. **S3 不是静默截断：** PCA 投影，等行后 Procrustes
22. **Week-8：** 默认 `unregistered`（**不是缺陷**）；有阈无测 → `threshold_present_measurement_missing`；有阈有测 → `compared` + side。`scientific_conclusion is None`

---

## 11. 测试质量（仅公式）

作者声称 136 passed。本审查重跑全仓库：**135 passed, 1 failed**（`test_scientific_collect_h_is_step_boundary_not_last_token` 断言 `10==15`，属采集行数，不是本通道估计量）。绿测**不能**证明公式正确。

- `test_p1_bootstrap_resamples_delta_auc`：**半有效**。锁住 `status==resampled_delta_auc` 与 `lo<=hi`，**不锁区间宽度**，也不对照独立 \(\Delta\mathrm{AUC}\) oracle。退化 \([\delta,\delta]\) 只要改状态串仍会过。本轮生产路径已用独立 IRLS 关掉 C5-M-01
- `test_week8_threshold_without_metric_is_not_evaluated`：**有效**（本轮 CHK-34）
- `test_week8_never_passes_unregistered`：**有效**（默认路径）
- `test_common_dim_is_not_silent_truncate`：**弱**。只查 `truncated is False` / `a_map==pca`。`eye(4)` vs `eye(3)` 行数不同，Procrustes 走 `not_applicable_shape_mismatch`，测不到成功对齐。本轮用等行 \((8,4)/(8,3)\) 与 PCA-vs-切片差独立关闭“静默截断”
- `test_sequence_score_uses_true_edges_only` 锁住 `truth_indices=[0]→0.1`，**同时锁住无 indices 时的 `0.9`**
- `test_c3_m01_event_mean_not_union` **有效**（0.25）
- `test_evaluated_zero_hit_sham_is_zero_noise_not_null`：**API 半有效**；`t1_tiny` 分母空
- **无** `unique` 序 ≠ \(E\) 列的 CLI oracle（C6-M-01 未被锁住）

---

## 12. 结论

开审冻结哈希 `dc2ba459…` **HASH_MATCH**（59 文件）。审查绑定该声明快照的公式库 digest；CLI \(a(X)\) 循环复读后未改语义。作者 pytest 声称 136 passed；本审查全仓库 **135 passed, 1 failed**（失败项非本通道公式）。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| \(S/M/\rho\) 事件均值；0-hit noise=0 | 通过 |
| TO/CSP 手算微例 | 通过 |
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | 通过 |
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | 通过 |
| \(a(X)=\max_{j\in R(s_i)}(1-p)\) 逐步 \(R(s_i)\) | **并集关闭**；**列身份失败**（C6-M-01） |
| P1 留出 logistic | 通过 |
| P1 问题级 bootstrap 重算 \(\Delta\mathrm{AUC}\) | **通过**（C5-M-01 关闭） |
| 假说不要求正 AUC | 通过 |
| P2 配对 + 支持集 | asked 项通过 |
| P3 vs 对照 | 通过 |
| 4096≠3584 直接迁移 N/A | 通过 |
| S3 共同维不得静默截断 | **通过**（PCA，非切片） |
| Week-8 阈值比较 | **通过**（有阈无测 → `threshold_present_measurement_missing`） |
| Gate 未注册 | **不是缺陷** |

**r05 声称独立复算：**

| r05 声称 | 本轮 |
|---|---|
| bootstrap 重采样并重算 \(\Delta\mathrm{AUC}\) | **成立**。C5-M-01 反例现宽度 \(0.675\)，独立 IRLS 区间逐位相同 |
| CLI calibrate 逐步 `truth_indices` / \(R(s_i)\) | **并集成立**（对齐 unique 时 \(a=0.1\)）。**列身份不成立**（C6-M-01） |
| Gate 有阈值无测量 → `threshold_present_measurement_missing` | **成立**。有测量时比较 side，不发明 pass/fail |

仍会污染论文数字的 confirmed defect：**C6-M-01**（`unique=['p3','p2','p1']` 时 CLI \(a=0.2\)；`unique=['p2']` 时 \(a=0.9\)；论文均为 \(0.1\)）。

**验收意见：** `FAIL_MATH_STATS`。C5-M-01 与 C5-M-02（并集）可关。在 C6-M-01 关闭并经独立复审前，不得把 CLI 校准写成命题 2 覆盖。Gate 保持 `unregistered` 不是缺陷。

---

## 附录：59 文件 SHA-256（POSIX relpath，仅 file bytes）

下列 digest 取自本审查第二次完整抽查（当时 `cli.py` 为 `2814e9b0…`）。开审汇总哈希为声明值 `dc2ba459…`。公式库八文件与下表一致并在此后保持不变。

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc
src/reasoning_diff/cli.py  2814e9b0c6af871e186a195cde8faf98a7bda9a274439238202f104c4acb3dc8
src/reasoning_diff/edits.py  bfd1632b50504c042640bcda85368b0c695fd3f843ea885200d080055aa107b6
src/reasoning_diff/events.py  fc5031a51e99a4b511450d03ded6dd5f205175eb263bf4cbaf8695ee47746e17
src/reasoning_diff/executor.py  481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  a6bcd893abedaf3bbe7a4804cde55a78b7d7fc1f68133e3c6643de346eb134dc
src/reasoning_diff/models/__init__.py  0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8
src/reasoning_diff/models/adapters.py  c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a
src/reasoning_diff/models/collect.py  2772257e0643b3c7ebce94eec039d82bcdcbff4fde9c8136dbcb602eaba8dd17
src/reasoning_diff/models/features.py  0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0
src/reasoning_diff/models/generate.py  f92f3ba61ec735fb52d29ea6a8f0768c855fded2ab0eef096c0ce22aeda72b5a
src/reasoning_diff/models/tiny.py  21725a183452bd06593789217745202863269cd7e9dea1ec144e4bbdb0a1ddb0
src/reasoning_diff/models/tokenize.py  b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332
src/reasoning_diff/probes/__init__.py  3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5
src/reasoning_diff/probes/bilinear.py  52de70553b37dec69822b790b006b7282e58ee926bb77006b3da40b419726e15
src/reasoning_diff/probes/boundary.py  ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034
src/reasoning_diff/probes/calibrate.py  e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334
src/reasoning_diff/repair.py  2600cd013d4446623de8d7f44bb701ceb2d9d70959ad216878746aea1d11268b
src/reasoning_diff/rng.py  2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908
src/reasoning_diff/schema.py  57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7
src/reasoning_diff/scoring.py  8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99
src/reasoning_diff/splits.py  35cd0e3f724ee850b4cf28a118717d51d188ae913a2917562fc29110ccd7cbdc
src/reasoning_diff/tasks/__init__.py  4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754
src/reasoning_diff/tasks/catalog.py  80e4db4b0241b9194216da74c60671916a9fa3c50f9f8d676b8f7cc17b53875d
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
tests/test_round05_regressions.py  83a665a16567884fda83584e3f847842c6cb541375cf90c25fad1338fb420882
tests/test_science.py  bed01ffa293f2c1f3d341e9b4ddbf375436eb77fa1a82c5093f12a7a402ca126
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```
