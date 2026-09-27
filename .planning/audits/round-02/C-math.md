# C：数学与统计独立审查（round-02）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立推导双线性探针、加权 BCE、split conformal、迁移映射、P1–P3、有符号 excess、INLP、C-rand/C-layer；专查 off-by-one、未知标签泄漏、默认 P1 非留出、零分母、未截断负 excess
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读 round-02 的 A/B/D/E/F。体例对照过 round-01 `C-math.md`，**结论全部由本轮对当前磁盘字节的公式推导与反例重做**，不沿用上一轮状态
- 声明冻结哈希：`2676a0983f6b42148202eedfbfaea44ce207d1fd386b8d47cbc909e983c5cc38`（`.planning/audits/round-02/VERSION.md`，声称 55 文件、POSIX relpath + bytes）
- 本审查是否复现该汇总哈希：**否**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改
- numpy：1.26.4；CPython 3.11.7

---

## 1. 冻结哈希

范围内文件数：**55**（`src/reasoning_diff/**/*.py` 41 + `tests/**/*.py` 13 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「55 files」一致。全部为 LF、无 CRLF。

对「POSIX relpath + file bytes」的独立复算（字典序）：

| 方法 | SHA-256 | 与声明值 |
|---|---|---|
| A. `path.encode() \|\| bytes` | `4ce6fac512f19e2d4d03b6821d9fa2b46632d19265fd5a272b8910fde52ea992` | 否 |
| B. `path.encode() \|\| 0x00 \|\| bytes`（round-01 F 所述） | `7b6680d6d937097fd02841d5950df1a7b3498ebcd1965381220b5e429ec5c617` | 否 |
| 另试 | `io.digest(path→file_digest)`、sha256sum 列表、纯字节串、Windows 反斜杠、LF 再归一、merkle、`./` 前缀、长度前缀等 20+ 种 | 均否 |

**审查对象是当前磁盘字节**，不是未复现的声明聚合。逐文件 SHA-256 见附录。下列公式结论绑定这些 digest。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/__init__.py` | 1–3 | `3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5` | 再导出 | 全文 |
| `src/reasoning_diff/probes/bilinear.py` | 1–74 | `81451eb4c0d6945e5d89631667e21515cde3b3f0294c159f138a73409c1ffb17` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差梯度 + 未知标签反例 |
| `src/reasoning_diff/probes/boundary.py` | 1–23 | `a45ec29f20fc3b3c5f421c6b93bc66e909030e1d8854194137c3c0167a490347` | `BoundaryMLP` Hidden=256 | 全文（与 r1 字节相同） |
| `src/reasoning_diff/probes/calibrate.py` | 1–35 | `d753c94bc0467dd7df46ca912b02f36eee470231dadb6285f68bb9fa9585ebb3` | `sequence_score`/`conformal_threshold`/`predict_set` | 全文；手算 k；α≥1；浮点边 |
| `src/reasoning_diff/transfer.py` | 1–40 | `0020150ebf53663b1cb2204f27fc315ed4dbbdd572ef82733508fe12ee463d63` | `direct_transfer`/`fit_linear_map`/`apply_map`/`apply_bilinear_inputs` | 全文；已知 W 回收；维不匹配 |
| `src/reasoning_diff/analysis.py` | 1–131 | `146ca012939ed23c5044121bb45f56300677d47fc89e0e4f2ef896ac8e95c50b` | `_auc`/`_fit_scores`/`p1_incremental`/`p2_paired`/`p3_recovery` | 全文；AUC 排列；默认 P1 反例；留出泄漏 |
| `src/reasoning_diff/interventions.py` | 1–91 | `b971c432d1e2b2fd465fddbc673834e2a190a42b9ea44276631e7487c700a22e` | `inlp_remove`/`c_rand_delta`/`c_layer_delta`/`project_delta` | 全文；多步秩；范数匹配 |
| `src/reasoning_diff/measure.py` | 1–242 | `2d9272406879cbf9a21b367c75d52caf373f9d03ddb10c020026a3e2b599b3e7` | `dependency_densities`/`_matrix_densities` | 全文；缺失噪声；负 excess；并集 |
| `src/reasoning_diff/baselines.py` | 1–44 | `2d28ef1cdff3bd571bd91fccf73e2f87d3dc4fc6b20d7816febfa0d48f05399c` | `attention_rollout`/`verbalizer` | 全文（非本通道主公式） |
| `src/reasoning_diff/repair.py` | 1–57 | `54559ea4f50eda9a9902c2b8594d9dd843a71aae2f67d8e8b80d8e96d0fea043` | `repairability`/`run_repair` | 对照（与 r1 字节相同） |
| `tests/test_science.py` | 1–97 | `3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c` | 校准规定例 / 4096≠3584 | 查是否独立 |
| `tests/test_measure.py` | 1–40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | 负 excess / 零分母 | 集合路径 |
| `tests/test_review_regressions.py` | 1–315 | `30b02a41dca7288595827dbdedcbe3ceb681cd28bd8077d8abe53d1951648346` | C-01..C-04 / B-01 | 查测试能否关闭缺陷 |

调用链只读、不计入“已证明正确”：`cli.cmd_fit` / `cmd_calibrate` / `cmd_intervene` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

### 3.1 双线性

\[\hat p=\sigma(h^\top U V^\top e+b)=\sigma(\langle hU,\,eV\rangle+b),\quad (HU)(EV)^\top\text{ 为矩阵形式}.\]

默认 \(r=64\)，\(\lambda_{\mathrm{FN}}=10\)。未知标签不得进入 \(\mathcal K\)。空 \(\mathcal K\) 是无效损失，不是 0。

`score` / `predict_matrix` 与上式一致。`fit` 的 logit 梯度 \(w(p-y)/|\mathcal K|\) 与 \(dU=H^\top(dZ\,EV)\)、\(dV=E^\top(dZ^\top HU)\) 一致。未知哨兵若是 `-1`（矩阵路径用 `!= -1`），必须从 \(\mathcal K\) 排除；只滤 `isfinite` 不够。

### 3.2 Split conformal

校准分数升序 \(s_{(1)}\le\cdots\le s_{(N)}\)，\(k=\lceil(N+1)(1-\alpha)\rceil\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow q=+\infty\)。\(\alpha\notin[0,1)\) 必须拒绝。当 \(0\le\alpha<1\) 时 \(k\ge 1\)，故 `k<1` 分支在合法 α 下不可达。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。在同一浮点通道比较已算好的 \(1-p\) 与 \(q\)；十进制字面量 `0.7/0.3` 会破边。

### 3.3 迁移

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。无标签配对：`tgt @ W ≈ src`。监督适配必须是不同估计程序。双线性要成对映射 \(H\) 与 \(E\)。

### 3.4 P1–P3

- **P1：** 在 train 拟合控制模型 vs 控制+\(\rho\)；在**留出**基础题上比 Mann–Whitney AUC。平局贡献 \(1/2\)。默认路径若写死 `len+0.01*op` 则不是该估计量。OLS 线性概率 ≠ 指定的 logistic，但对秩 AUC 可以工作。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\) 必须共用分母 \(|P\setminus R_{\mathrm{task}}|\)；缺配对不得崩。
- **P3：** 相对 C-rand / C-layer；不得写“只是后果”。

### 3.5 Excess / INLP / 对照范数

缺失噪声协议 ⇒ excess = null，不得把参照当 0。excess 可负。集合 API 的 \(\rho_S(T)\) 若吃并集，不等于 \(\frac1n\sum\rho_S(s_i)\)。

INLP：每步在**已投影** \(H\) 上重拟合，再累乘 \(I-uu^\top\)。C-rand / C-layer 必须缩放到**该样本主干预实际** \(\|\Delta\|\)。

Boundary MLP：2 层 ReLU，Hidden=256。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（误差 0） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | 手算 1.2272895322281534 | **通过** |
| CHK-04 | 空 mask；`y=-1` 未知哨兵 | 直接调用 | **失败**（C2-M-01） |
| CHK-05 | `y=nan` 是否排除 | `weighted_bce` | **通过** |
| CHK-06 | `fit` 梯度 | \(U_{00}\) 解析 vs 有限差，相对误差 \(1.5\times10^{-8}\) | **通过**（已知 \(\{0,1\}\)） |
| CHK-07 | `fit(-1)` 是否等于 `fit(nan)` | 同初值一步 | **失败**（C2-M-01） |
| CHK-08 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | \(N=4,\alpha=0.4\Rightarrow k=3,q=0.3\)；\(\alpha=0.1\Rightarrow k=5,+\infty\)；\(N=1,\alpha=0.05\Rightarrow+\infty\)；\(N=3,\alpha=0.5\Rightarrow k=2\)；\(N=10,\alpha=0.05\Rightarrow k=11,+\infty\) | **通过** |
| CHK-09 | \(\alpha\ge 1\)、\(\alpha<0\) 不回绕 | \(\alpha=1,1.5,-0.1\) | **通过**（`invalid`，`q is None`；不再 `arr[-1]`） |
| CHK-10 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **失败**（C2-M-03） |
| CHK-11 | \(q=+\infty\) 全选；未知/空真集 | `predict_set` / `sequence_score` | **通过**（函数层）。`sequence_score` 仍是 `max(给定分数)`，不计算 \(1-p\) |
| CHK-12 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`(3,5)@(6,4)` | **通过**（N/A；`ValueError`，无静默切片） |
| CHK-13 | \(X_B W=X_A\) 回收；H 与 E 成对映射 | 已知 \(W\)；`apply_bilinear_inputs` | **通过**（\(\sim10^{-15}\)；\(H\mapsto 2H,\,E\mapsto 3E\)） |
| CHK-14 | `labeled=True` 是否改估计 | 同一 `lstsq` | **失败**（只改 status 字符串，C2-M-05） |
| CHK-15 | 常数分数 AUC 与排列 | `_auc(ones, y)` 三种排列 | **通过**（均为 0.5） |
| CHK-16 | Mann–Whitney 平局 | 手算 0.75 | **通过** |
| CHK-17 | 默认 P1 能否检出 \(\rho=y\)（`op` 大噪声） | \(n=40\)：`len≡10`，`op~N(0,1000)`，`rho=y` | **失败**：默认 `auc_full=0.4875,\Delta=0.025`；留出 OLS `auc_full=1,\Delta=0.65`（C2-M-02） |
| CHK-18 | 留出拟合是否忽略 eval 行的 \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 分数差 0） |
| CHK-19 | P1 排列不变（默认路径分数） | `test_c01` 同构 | **通过** |
| CHK-20 | P2 减法与 `shared_denominator` | `p2_paired(0.2,0.5,0.8,0.6,4)` | **部分通过**：差值正确；分母只回传；`None` → TypeError（C2-M-06） |
| CHK-21 | P3 相对对照、禁句 | `p3_recovery(0.5,0.4,0.3,0.1)` | **通过** asked 项（`vs_crand/vs_clayer`；`causal_reverse_claim is False`）。无 vs-baseline / nontarget |
| CHK-22 | INLP 更新 \(H\) | 三维混合信号；`steps=1` vs `8` | **通过**（`max\|P1-P8\|=0.735`；`rank(I-P)`：1→3；一步后 \(Hu\approx0\)） |
| CHK-23 | `test_c03` 是否真测迭代 | 弱例 \(H=[[2,0],[2,0],[0,1],[0,1]]\) | **通过（测试有效）**：\(u\propto[0.447,-0.894]\)；一步后 col0 非 0；两步后 \(\approx0\)。一步假实现过不了 |
| CHK-24 | C-rand / C-layer 匹配主范数 | 主基 seed=99 的 \(\|\Delta\|\) vs 对照 | **通过**（`actual_norm` 完全相等；缺 `target_norm` 抛错；不等于 rng(1) 哑范数） |
| CHK-25 | 交换公式 | \(e_1+\Pi_{e_2}(e_2-e_1)=e_1+e_2\) | **通过** |
| CHK-26 | 集合路径负 excess、零分母、缺 sham | 手算 −0.5；全祖先袋；无 protocol | **通过** |
| CHK-27 | 矩阵 `noise=None` | `task=[[0,0,1]], behavior=[[1,0,1]]` | **通过**：S/M 的 noise/excess 均为 `None`；raw 仍为 0.5 / 0.0；**不再伪造 0 参照** |
| CHK-28 | 并集 \(\rho\) vs \(\frac1n\sum\rho(s_i)\) | 两步均值 0.25 vs 并集 0 | **失败**（C2-M-04） |
| CHK-29 | Boundary Hidden=256；拒绝 128 | 形状 + `ValueError` | **通过** |
| CHK-30 | Repairability/RR 零分母；`run_repair` 预算 | 公式函数 vs 入口 | 公式 **通过**；入口仍 `generated_tokens=0`、`extra_prefill_tokens=len(chars)`（C2-M-08） |
| CHK-31 | Procrustes \(R=UV^H\) | 已知正交 \(R\) 回收 \(\|AR-B\|_F\sim10^{-15}\) | **通过** |
| CHK-32 | `pytest` 数学相关 | `tests/test_science.py tests/test_measure.py tests/test_review_regressions.py -q` | **37 passed，exit 0**。不覆盖 CHK-04/07/10/17/28 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 复现声明冻结汇总哈希 | 55 文件集合对得上；多种 path+bytes 聚合均 ≠ `2676a098…` |
| 全仓库 pytest（作者声称 65） | 本通道只跑公式相关；其余属 E |
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | CLI 校准仍用字面量/loss 拼分数（`cli.py` 287–292）；`cmd_analyze` 的 `p1/p2/p3` 为 `None` |
| 阅读其他 round-02 通道 | 任务禁止 |
| Abnar rollout 是否为论文承诺 | `attention_rollout` 是 \((A+I)\) 累乘，不是 \(\frac12 A+\frac12 I\)；未对原文验收 |

---

## 6. ISSUES C-01..C-04（独立确认，不采信 `fixed_pending_review`）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **部分关闭** | `_auc` 已是 \(P(s_+>s_-)+0.5P(=)\)，常数分与排列均为 0.5。**默认 P1 仍不是留出拟合**（C2-M-02） |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | `0<=α<1` 否则 `invalid`；不再 `arr[k-1]` 负索引 |
| C-03 INLP 不投影 H | **关闭** | `work = work @ step`；反例上 `steps=1` 与 `8` 可分；`test_c03` 第一步方向是混合轴，需要第二步 |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm`；CLI `cmd_intervene` 传入 `\|\|main-base\|\|`；C-layer 同样缩放 |

上一轮 C-M-05（矩阵缺噪声当 0）本轮 **关闭**（CHK-27）。

---

## 7. 发现

状态：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

### C2-M-01 — 未知哨兵 `-1` 进入加权 BCE / `fit`；空 \(\mathcal K\) 损失为 0

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `weighted_bce` `bilinear.py` **66–74**；`fit` **44–51**
- **触发：** `target=-1`（`measure._matrix_densities` 仍用 `-1` 表示未知，`measure.py` **134**）；或 `mask` 全假
- **原文：** 未知不进 \(\mathcal K\)；\(\lambda_{\mathrm{FN}}=10\) 只作用于正类
- **证据（独立于被测期望）：**
  - `pred=[0.2,0.8], target=[-1,1], mask=[1,1]` → `0.5341423516682081`
  - 仅正类项应为 \(10(-\log 0.8)=2.231435513142097\)
  - `y=-1` 有限，`y>0.5` 为假，于是 \(w=1\)，该项是 \(\log p-2\log(1-p)\)，不是 BCE
  - 同初值一步：`Y=-1` 与 `Y=nan` 的 \(\Delta U\) 不同
  - 空 mask → `0.0`
- **影响：** 矩阵未知格被当成负类；空批“完美损失”。`fit` 的 `known &= isfinite(Y)` 同样放行 `-1`
- **修复：** \(\mathcal K=\{\mathrm{mask}\land y\in\{0,1\}\}\)；空 \(\mathcal K\) 返回 NaN/raise

### C2-M-02 — 默认 P1 仍是写死线性组合，不是留出估计

- **严重度：** High
- **状态：** confirmed defect（留出分支本身可用；默认路径与指定估计量不符）
- **符号：** `p1_incremental` `analysis.py` **42–46**（对照 **47–55**、`_fit_scores` **27–30**、`_auc` **15–24**）
- **触发：** 任何未传 `held_out` 的调用。`test_c01_auc_is_rank_and_permutation_invariant` 走的就是这条路径
- **反例：** \(n=40\)，`length≡10`，`op~N(0,1000)`，`rho=y∈{0,1}`。真实增量信号只在 \(\rho\)。
  - 默认：`score=10+0.01\cdot op[+\rho]` → `auc_full=0.4875`，`delta_auc=0.025`，`held_out=False`
  - `held_out` 后半：OLS 控制 `len+op` 后 `auc_full=1.0`，`delta_auc=0.65`，`held_out=True`
  - 再造 \(n=60,\rho=y+\varepsilon\)：默认 \(\Delta=0.039\)；留出 \(\Delta=0.583\)，`auc_full=1`
- **留出分支核对：** 只污染 eval 行的 \(X\)，train 上的拟合分数不变。无 eval 泄漏。
- **仍缺：** 指定的是 logistic，实现是 `lstsq` 线性概率；无偏相关；`bootstrap_cluster` 未挂上；不强制 \(\rho_S^{\mathrm{excess}}\)
- **影响：** 省略 `held_out` 时，P1 可以“看不见”控制后仍存在的 \(\rho\) 信号。CLI `cmd_analyze` 目前写 `p1: None`，尚未用该函数出数
- **修复：** 默认必须留出；去掉 `0.01` 魔法系数；train 拟合、test 比 AUC

### C2-M-03 — `1-p<=q` 在十进制“相等”边上失败

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `predict_set` `calibrate.py` **32–35**
- **证据：** `1.0-0.7 = 0.30000000000000004 ≰ 0.3` → `[False]`。`0.5` 二进制精确，可通过
- **影响：** 真边落在阈值上被丢。CLI 校准字面量仍是 0.1/0.2/0.3/0.4
- **修复：** 比较已存储的非conformity；或同一表达式算 \(1-p\) 与 \(q\)

### C2-M-04 — 集合 API 不是 \(\rho_S(T)=\frac1n\sum\rho_S(s_i)\)

- **严重度：** High
- **状态：** confirmed defect（定义错用；矩阵路径按行平均更接近原文）
- **符号：** `dependency_densities` 集合分支 `measure.py` **91–99**。CLI `cmd_prepare` **145–151** 对一个 ancestor 袋调用一次
- **反例：** 步 1 \(\rho=1/2\)、步 2 \(\rho=0\)，均值 0.25；并集 \(T=B=\{1,2\}\) → `rho_S_raw=0`
- **影响：** 轨迹级依赖密度被并集压低/抬高
- **修复：** 逐步算再平均；N/A 步单独计数

### C2-M-05 — 监督适配与无标签适配是同一个 lstsq

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `fit_linear_map` `transfer.py` **19–32**
- **证据：** `labeled` 只改 `status` / `uses_labels`。已知 \(W\) 回收误差 \(\sim10^{-15}\)，两条路径 \(W\) 相同
- **影响：** 分列报告会把同一估计量写成两种方法
- **修复：** 监督路径必须用标签，或拒绝并改名

### C2-M-06 — P2 只回传分母，缺配对则崩

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `p2_paired` `analysis.py` **64–70**
- **证据：** `shared_denominator` 原样返回，不计算、不校验两 \(\rho\) 是否共用 \(|P\setminus T|\)。`p2_paired(None, 0.4, …)` → `TypeError`
- **影响：** 新前提改分母时，无法区分“共享支撑上的 \(\Delta\rho\)”与“注入列”。缺测直接异常
- **修复：** 在共享前提上重算两个 \(\rho\)；None → null + 缺失计数

### C2-M-07 — `sequence_score` / CLI 校准仍不是 \(a(X)=\max(1-\hat p)\)

- **严重度：** Medium
- **状态：** confirmed defect（接口/流水线）
- **符号：** `sequence_score` **9–16**；`cli.cmd_calibrate` **287–292**
- **证据：** 函数只 `max(edge_scores)`。CLI 默认 `[0.1,0.2,0.3,0.4]`，有探针时用 `abs(loss)` 拼四个标量，与边、轨迹、`base_group_id` 无关
- **影响：** 命题 2 的覆盖声明不能从数据成立。阈值公式本身已对

### C2-M-08 — `run_repair` 仍不供给 Repairability 输入（文件未变）

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `repair.py` **34–45**（SHA256 与 r1 相同 `54559ea4…`）
- **证据：** `run_repair(..., [3,4], "abcd")` → `generated_tokens=0`，`extra_prefill_tokens=4`（字符），`original_token_budget=7`。`repairability(1,0) is None` 公式函数本身正确
- **影响：** 走该入口的成本数字无定义。非本轮清单主项，但估计量仍在

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C2-U-01 | Medium | `apply_bilinear_inputs` 未被 CLI/analyze 调用；跨模型路径只跑 `direct_transfer(4096,3584)` | `transfer.py` 39–40；`cli.py` 355 | API 公式正确；误用取决于调用方 |
| C2-U-02 | Medium | `cmd_fit` 对 task/behavior 两个头用同一张 \(Y\)（且由 behavior 标签对角填） | `cli.py` 262–276 | 估计程序在 \(\{0,1\}\) 上正确；标签合同是流水线问题 |
| C2-U-03 | Low | `attention_rollout` 为 \((A+I)\) 累乘，不是 Abnar \(\frac12A+\frac12I\) | `baselines.py` 28–33 | 未核原文是否承诺官方 rollout |
| C2-U-04 | Low | INLP 默认 8 步在低维会把整空间投掉（本反例 `rank(I-P)=3`） | `interventions.py` 52–67 | 标准 INLP 会拟合残差噪声；高维 8 步可接受 |
| C2-U-05 | Low | `predict_set(q=None)` 会 TypeError | `calibrate.py` 32–35 | 非法 q 应由校准入口挡住 |
| C2-U-06 | Low | P1 正类方向未固定；ρ 是否 excess 由调用方决定 | `analysis.py` 33–61 | 无断言 |
| C2-U-07 | Low | 矩阵噪声数组含 NaN 且 `noise is not None` 时，`noise==1` 把 NaN 当未命中 | `measure.py` 143–146 | 未见到这种构造 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C2-S-01 | 真实轨迹命题 2 覆盖 | 校准不计算 \(a(X)\) |
| C2-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明 N/A，未跑 `apply_bilinear_inputs` |
| C2-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册；analyze 不调用 P1–P3 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`（`bilinear.py` 21–29）；`fit` 在 \(y\in\{0,1\}\) 上的梯度（有限差）
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64
3. Conformal \(k\) 公式、\(k>N\Rightarrow+\infty\)、\(\alpha\ge1\) 不再回绕；\(\alpha=0\Rightarrow+\infty\)
4. `direct_transfer` 拒 4096≠3584；`apply_map` 维不匹配抛错，无 pad/truncate；`apply_bilinear_inputs` 分别变换 H、E
5. `_auc` Mann–Whitney，平局 1/2，排列不变
6. 留出 `_fit_scores` 不用 eval 行的 \(X\)
7. 集合路径：零分母 None；缺 sham → excess None；负 excess −0.5 不截断
8. 矩阵路径：`noise=None` → noise/excess None（B-01 / 旧 C-M-05 关闭）
9. INLP 在已投影 \(H\) 上迭代
10. C-rand / C-layer 匹配传入的主干预范数；缺范数即失败
11. 交换 \(H+\Pi_Z(H_d-H_b)\)
12. `p3_recovery["causal_reverse_claim"] is False`；相对 crand/clayer
13. `BoundaryMLP` Hidden=256，非 256 拒绝；2 层 ReLU
14. Week-8 无阈值 → `unregistered`，`scientific_conclusion is None`
15. Procrustes 形状不等 N/A；同形状可回收 \(R\)
16. `verbalizer(supervised, trained=False)` 拒绝

---

## 11. 测试质量（仅公式）

`37 passed` **不能**证明本通道估计量正确。

- `test_c01` 排列测的是**默认魔法系数路径**，不测 CHK-17 的“\(\rho\) 被 op 淹没”
- `test_c01_held_out` 只断言 `held_out is True` 且 `auc_base is not None`，不断言未泄漏、不断言检出增量
- `test_c02` 覆盖 \(\alpha\ge1\)，不覆盖 `1-0.7` 浮点边、不覆盖按题去重的 \(N\)
- `test_c03` **有效**（第一步不是 \(e_1\)）
- `test_c04` / `test_b01` 有效关闭对应缺陷
- 无 `weighted_bce(-1)`、无空 mask、无并集 vs 逐步、无 P2 `None`、无 `predict_set(0.7,0.3)`

---

## 12. 结论

本通道**不通过**。声明冻结哈希 `2676a098…` **未能复现**；审查绑定 55 个文件的逐文件 SHA-256 与方法 A/B 聚合。

对照任务清单：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | 通过 |
| 未知 mask | **不通过**（`-1` / 空批） |
| conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\ge1\) 不回绕 | 通过 |
| 迁移无 pad；4096→3584 N/A；H 与 E 映射 API | 通过 |
| P1 留出 / 秩 AUC 排列不变 | AUC **通过**；默认路径 **不通过** |
| P2 共享分母 | 字段存在，**未计算/未强制** |
| P3 相对对照、无反向因果句 | 通过 |
| INLP 在投影 H 上；C-rand/C-layer 匹配主范数 | 通过 |
| 有符号 excess；缺噪声为 null 不是 0 | 通过 |
| Boundary hidden=256 | 通过 |

**可关闭（独立确认）：** C-02、C-03、C-04，以及旧 C-M-05。**不可把 C-01 标完全关闭。**

仍会污染论文数字的 confirmed defects：C2-M-01（未知 BCE）、C2-M-02（默认 P1）、C2-M-04（并集 \(\rho\)）。其次 C2-M-03/05/06/07/08。

**验收意见：** `FAIL_MATH_STATS`。在 C2-M-01/02/04 关闭并经独立复审前，不得把探针损失、默认 P1 ΔAUC、或集合路径 \(\rho_S(T)\) 写成可报告结果。C-rand / INLP / 缺噪声 null / conformal \(k\) 这几块本轮**不再**是拦路缺陷。

---

## 附录：55 文件 SHA-256（POSIX relpath）

```
pyproject.toml  64150ec08e6059e11a492e663d355a59d351c4bdbb28e6be603a6167598deb8e
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  146ca012939ed23c5044121bb45f56300677d47fc89e0e4f2ef896ac8e95c50b
src/reasoning_diff/artifacts.py  61dc639ead0eff1fc1d0679f334c1853881cde6cadd80c56f7c091c252234293
src/reasoning_diff/baselines.py  2d28ef1cdff3bd571bd91fccf73e2f87d3dc4fc6b20d7816febfa0d48f05399c
src/reasoning_diff/cli.py  9ae87fe24abfeb635eec192b84f2a28162a2015b19f45aa551250b336bffab48
src/reasoning_diff/edits.py  6226f3adc81dda92210fd8ea1b6e78651f492a74d041e7d71ce6c8f0c935c1cd
src/reasoning_diff/events.py  1d1d3413601c48343c26d6d6dcc0519e8cbbe537dec0a5fce9239a18a4d7897c
src/reasoning_diff/executor.py  d1760266a9a7606b3bd36eaf12d9fdde19a0533e3339842f32404773905b8d21
src/reasoning_diff/graphs.py  1e287cebf844cec0d055138224ae5a0b39c0358228c6587e8b4b6d4cfc604241
src/reasoning_diff/interventions.py  b971c432d1e2b2fd465fddbc673834e2a190a42b9ea44276631e7487c700a22e
src/reasoning_diff/io.py  c5c77a27d196e97da61947344a786137ee54cbaf4b2381208ce4d574da5b6897
src/reasoning_diff/measure.py  2d9272406879cbf9a21b367c75d52caf373f9d03ddb10c020026a3e2b599b3e7
src/reasoning_diff/models/__init__.py  0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8
src/reasoning_diff/models/adapters.py  a8680ef98b8075ce0f01cbcc43841a1974c1c93dfe7eb0ed248c50737c759ddc
src/reasoning_diff/models/collect.py  051e1b3005631c486b132b7889cfa7b91e85dc0dbcbd6d9d533907b8227815ad
src/reasoning_diff/models/features.py  ff5c6a79b9ecf0820be547e6dba39b6cfe9d705547d16587148e182e2d1e1e0e
src/reasoning_diff/models/generate.py  4fd7091842236d7a4249e41c7647ac13cece434f72f7f42c23a43b14cf02e012
src/reasoning_diff/models/tiny.py  3bf2200b9b71d191480e7747ba729c0a701be6f907488281a98ef79a4f954490
src/reasoning_diff/probes/__init__.py  3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5
src/reasoning_diff/probes/bilinear.py  81451eb4c0d6945e5d89631667e21515cde3b3f0294c159f138a73409c1ffb17
src/reasoning_diff/probes/boundary.py  a45ec29f20fc3b3c5f421c6b93bc66e909030e1d8854194137c3c0167a490347
src/reasoning_diff/probes/calibrate.py  d753c94bc0467dd7df46ca912b02f36eee470231dadb6285f68bb9fa9585ebb3
src/reasoning_diff/repair.py  54559ea4f50eda9a9902c2b8594d9dd843a71aae2f67d8e8b80d8e96d0fea043
src/reasoning_diff/rng.py  2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908
src/reasoning_diff/schema.py  c07301be5fabd647797c19ec32dc841c09dae26e8a7d7c027fc7ecd5146ff5c1
src/reasoning_diff/scoring.py  d05822c4fb784fe4a57d9f82f583eaa31c0f3b2e0e96c04b81f77db7413433f8
src/reasoning_diff/splits.py  a62d819bf99ceb137f326b980833b425f296cd3caff04b5971351628aa6fcc63
src/reasoning_diff/tasks/__init__.py  4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754
src/reasoning_diff/tasks/catalog.py  5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0
src/reasoning_diff/tasks/t1_config.py  e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94
src/reasoning_diff/tasks/t1_fixture.py  01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41
src/reasoning_diff/tasks/t1_official.py  2e83cc052a518d43bfebd3ab3899a37ad5f369f36a29d5eedb95cbd3e48e969b
src/reasoning_diff/tasks/t2_gsm_plus.py  0da626321ee5d786f3c3b4c7da52687b3c9ca2d233eebe81f2d43f22c0cf3a8f
src/reasoning_diff/tasks/t2_gsm_symbolic.py  e8fc9d046ba130066e0acd7948b27b44abd663bdc45e5fe03f81c53244657f19
src/reasoning_diff/tasks/t2_noop.py  26cf5c21b5838a6bf1a335bf8b0eb5bc767a77c2e4128fc8a36a8c482456c874
src/reasoning_diff/tasks/t3_hotpot.py  a79ab16c0ebdae7fde154df79bdfd8d0ae38d5337473a5f6a4241c2f7c3930c1
src/reasoning_diff/tasks/t3_humaneval.py  c77e136ceb6e6f7141d8b29470fc570851f7fb4bdf4c54a8a93e87be16cabeb6
src/reasoning_diff/tasks/t3_musique.py  095f10acc7c4600f607b2a6d5fbb6e0bd5962d0f7ccc881d79efbbfd136c3e58
src/reasoning_diff/tasks/t4_boundary.py  a2ca9188353b213d2c7c617dd27c60415adb0c16c40326ae8a7ecce03f94a5f9
src/reasoning_diff/transfer.py  0020150ebf53663b1cb2204f27fc315ed4dbbdd572ef82733508fe12ee463d63
tests/conftest.py  1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1
tests/test_artifacts.py  830953f379954233c76c9aab9f5f4b3860ea598579015a58bddd9909c5bd3278
tests/test_cli_pipeline.py  63b4c09f51f6c7d807e8928f27fa62ec54e3f4656229b3615371ae930b5de0b9
tests/test_generate_loop.py  ffe10b0d6812908ca34f446103b22a23c2e857a85172cc78e72caf005a979a46
tests/test_measure.py  fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab
tests/test_review_regressions.py  30b02a41dca7288595827dbdedcbe3ceb681cd28bd8077d8abe53d1951648346
tests/test_science.py  3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  54e57fea7417d901c75b7d17cfe9b90ee442f2d634a08d22272a678959ce9650
tests/test_tiny_cache.py  097a48534da1e870244bae2da2a849a65fda2c00233c3fe1b8792897e0fc5024
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
```
