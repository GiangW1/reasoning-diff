# C：数学与统计独立审查（round-03）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性/加权 BCE 未知掩码、split conformal、`predict_set` 的 \(1-p\le q\)、P1 留出、P2 None-safe、迁移 labeled vs unlabeled、INLP、C-rand 范数、\(\rho\) nulls。仍错则给反例。重跑数学测试。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读 round-03 的 A/B/D/E/F。体例对照过既有 `C-math.md`，**结论全部由本轮对当前磁盘字节的公式推导与数值反例重做**，不沿用上一轮状态，不采信 ISSUES 的 `fixed_pending_review`
- 声明冻结哈希：`67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e`（`.planning/audits/round-03/VERSION.md`，55 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**是**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改（只写本文件）
- numpy：1.26.4；CPython 3.11.7

---

## 1. 冻结哈希

范围内文件数：**55**（`src/reasoning_diff/**/*.py` 41 + `tests/**/*.py` 13 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「55 files」一致。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 方法 | SHA-256 | 与声明值 |
|---|---|---|
| VERSION 脚本（本审查独立执行） | `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e` | **是** |

审查对象绑定该冻结快照。逐文件 SHA-256 见附录。下列公式结论绑定这些 digest。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/__init__.py` | 1–3 | `3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5` | 再导出 | 全文 |
| `src/reasoning_diff/probes/bilinear.py` | 1–76 | `35e8d6ff7425f818e609cf527390c158c825ce019932b1664c3f9778ebd742e6` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + 未知哨兵 |
| `src/reasoning_diff/probes/boundary.py` | 1–23 | `a45ec29f20fc3b3c5f421c6b93bc66e909030e1d8854194137c3c0167a490347` | `BoundaryMLP` Hidden=256 | 全文 |
| `src/reasoning_diff/probes/calibrate.py` | 1–42 | `16609e8f7007aab433b2ea12f13587582676d0ab103742a842ed82a801c8c864` | `sequence_score`/`conformal_threshold`/`predict_set` | 全文；手算 \(k\)；`1-0.7` 边 |
| `src/reasoning_diff/transfer.py` | 1–50 | `cffe4791564fbb9ca19561691faac2fee106dc48d1b05cfcdd0ef000892697b4` | `direct_transfer`/`fit_linear_map`/`apply_map`/`apply_bilinear_inputs` | 全文；labeled≠unlabeled 反例 |
| `src/reasoning_diff/analysis.py` | 1–157 | `bf3440b0fd0fd01cfb08314690efade13c45ada89e3abfd98a77f4f5336e86cc` | `_auc`/`_fit_scores`/`p1_incremental`/`p2_paired`/`p3_recovery` | 全文；默认留出；OLS≠logistic |
| `src/reasoning_diff/interventions.py` | 1–91 | `b971c432d1e2b2fd465fddbc673834e2a190a42b9ea44276631e7487c700a22e` | `inlp_remove`/`c_rand_delta`/`c_layer_delta`/`project_delta` | 全文；多步秩；范数匹配 |
| `src/reasoning_diff/measure.py` | 1–248 | `fde5ec49294e5b7409b673bd3d2d37c6af6bd838cc7bfb01ef2090ca5c448d70` | `dependency_densities`/`_matrix_densities` | 全文；null；并集；empty+hits |
| `src/reasoning_diff/baselines.py` | 1–44 | `2d28ef1cdff3bd571bd91fccf73e2f87d3dc4fc6b20d7816febfa0d48f05399c` | `attention_rollout`/`verbalizer` | 全文（非本通道主公式） |
| `src/reasoning_diff/repair.py` | 1–64 | `55cbcf07d0f42bbd3dfd36e194463c78e8b8b0eff0ee29623f6d4fcc22bb8d9e` | `repairability`/`run_repair` | 对照 |
| `src/reasoning_diff/cli.py` | 327–463 | `bcdf4f982b585f1da3751cd920bcd972ce433d93b256969af34a5ec7762dfd7b` | `cmd_fit`/`cmd_calibrate`/`cmd_analyze` | 只读调用链 |
| `tests/test_science.py` | 1–97 | `3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c` | 校准规定例 / 4096≠3584 | 查是否独立 |
| `tests/test_measure.py` | 1–40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | 负 excess / 零分母 | 集合路径 |
| `tests/test_review_regressions.py` | 1–371 | `1e91c98d55e645480f89599f7e12a1fb8bb02ca4929c463aa743de75e143c8c5` | C-01..C-04 / 未知 BCE / 默认 P1 | 查测试能否关闭缺陷 |

调用链只读、不计入“已证明正确”：`cli.cmd_fit` / `cmd_calibrate` / `cmd_intervene` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文：`Reasoning-Diff-修订方案-v3 (1).md` §2.5–2.6、§4.2、§5–7；PITFALLS 校准/P1/P2 条；REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01。

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

`score` / `predict_matrix` 与上式一致。`weighted_bce` **68–76** 与 `fit` **44–47** 现把 \(\mathcal K\) 限制为有限且 \(y\in\{0,1\}\)；空 \(\mathcal K\) 分别返回 NaN / `loss=None`。

### 3.2 Split conformal 与预测集

\[
a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij}),
\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow q=+\infty\)。\(\alpha\notin[0,1)\) 必须拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。等于 \(q\) 的边须保留。在同一浮点通道比较已算好的 \(1-p\) 与 \(q\)；十进制字面量 `0.7/0.3` 会破边。

`conformal_threshold` 的 \(k\) 与非法 \(\alpha\) 分支与上式一致。`predict_set` 现为 \((1-p)\le q+10^{-12}\)。`sequence_score` 默认仍是 `max(给定分数)`；`nonconformity="one_minus_p"` 才算 \(\max(1-p)\)。

### 3.3 迁移

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。无标签配对：中心化后正交 Procrustes（同维）或中心化 lstsq（异维）。监督适配必须是**不同估计程序**；若声称使用标签，必须有标签张量。双线性要成对映射 \(H\) 与 \(E\)。

### 3.4 P1–P3

- **P1：** 在 train 拟合控制模型 vs 控制+\(\rho\)（原文 / PITFALLS：logistic）；在**留出**基础题上比 Mann–Whitney AUC。平局贡献 \(1/2\)。默认路径不得写死 `len+0.01*op`。偏相关与题级 bootstrap 另报。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\) 必须共用分母 \(|P\setminus R_{\mathrm{task}}|\)；缺配对不得崩。新前提改分母，共同支持与注入列分开。
- **P3：** 相对 C-rand / C-layer；不得写“只是后果”。原文还要求非目标响应与相对基线 \(\Delta\mathrm{acc}\)。

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
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | 手算 0.9884682294074324 | **通过** |
| CHK-04 | 空 mask；`y=-1` / `y=2` / `y=0.5` | 直接调用 | **通过**：`-1`/`2`/`0.5` 均等于仅正类项 \(10(-\log 0.8)=2.231435513142097\)；若把 `-1` 当负类会得到旧泄漏值 `0.5341423516682081`，现不再如此。空 mask → NaN |
| CHK-05 | `y=nan` 是否排除 | `weighted_bce` | **通过** |
| CHK-06 | `fit` 梯度 | \(U_{00}\) 解析 vs 有限差，相对误差 \(3.0\times10^{-10}\) | **通过**（已知 \(\{0,1\}\)） |
| CHK-07 | `fit(-1)` 是否等于 `fit(nan)` | 同初值一步 | **通过**（\(\Delta U=\Delta V=0\)，loss 同）。空 \(\mathcal K\) → `no_known_labels` |
| CHK-08 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | \(N=4,\alpha=0.4\Rightarrow k=3,q=0.3\)；\(\alpha=0.1\Rightarrow+\infty\)；\(N=1,\alpha=0.05\Rightarrow+\infty\)；\(N=3,\alpha=0.5\Rightarrow k=2\)；\(N=10,\alpha=0.05\Rightarrow+\infty\)；\(\alpha=0\Rightarrow+\infty\) | **通过** |
| CHK-09 | \(\alpha\ge 1\)、\(\alpha<0\)、`None` 不回绕 | \(\alpha=1,1.5,-0.1,\mathrm{None}\) | **通过**（`invalid`，`q is None`） |
| CHK-10 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**：`1.0-0.7=0.30000000000000004`，`+1e-12` 后为 True。`0.5` 边通过；\(q=+\infty\) 全选。`q+5\times10^{-13}` 被纳入（保守）；`q+2\times10^{-12}` 排除 |
| CHK-11 | `sequence_score` | `[0.1,0.2]` | **部分通过**：默认 `0.2`（不是 \(a(X)\)）；`one_minus_p` → `0.9`。未知/空真集正确。CLI 仍用字面量（C3-M-04） |
| CHK-12 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`(2,5)@(6,4)` | **通过**（N/A；`ValueError`） |
| CHK-13 | \(X_B W=X_A\) 回收；H 与 E 成对映射 | 已知 \(W\)；`apply_bilinear_inputs` | **通过**（\(\sim10^{-15}\)；\(H\mapsto 2H,\,E\mapsto 3E\)） |
| CHK-14 | `labeled=True` 是否改估计 | 平移 \(X'=X+c\)；异维随机对 | **通过（估计程序已分列）**：平移例 \(\|W_{\mathrm{lab}}-W_{\mathrm{unl}}\|_\infty=7.57\)，无标签回收 \(I\)（\(\sim10^{-16}\)）；异维 \(\|W\|_\infty\) 差 1.67。签名仍无标签张量（C3-U-01） |
| CHK-15 | 常数分数 AUC 与排列 | `_auc(ones, y)` 三种排列 | **通过**（均为 0.5） |
| CHK-16 | Mann–Whitney 平局 | 手算 0.75 | **通过** |
| CHK-17 | 默认 P1 能否 silently 报数；留出能否检出 \(\rho=y\) | \(n=40\)：`len≡10`，`op~N(0,1000)`，`rho=y` | **默认通过**（`requires_held_out`）。**留出通过**：`auc_full=1`，`delta=0.43`。`precomputed=True` 仍是魔法系数，`delta=0.040`（C3-M-02） |
| CHK-18 | 留出拟合是否忽略 eval 行的 \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 分数差 0；eval 分数变） |
| CHK-19 | 空/满 `held_out` | 全 True / 全 False | **通过**（`held_out_empty`） |
| CHK-20 | P2 减法与 None | `p2_paired(0.2,0.5,0.8,0.6,4)`；`None` 各槽 | **部分通过**：差值正确；`None` → `missing_pair` 不再 TypeError。分母只回传/`len(shared_premises)`；不一致 \(\rho\) 仍标 `ok`（C3-M-03） |
| CHK-21 | P3 相对对照、禁句 | `p3_recovery(0.5,0.4,0.3,0.1)` | **通过** asked 项（`vs_crand/vs_clayer`；`causal_reverse_claim is False`）。无 vs-baseline / nontarget（C3-M-05） |
| CHK-22 | INLP 更新 \(H\) | 三维混合信号；`steps=1` vs `8` | **通过**（`max\|P1-P8\|=0.963`；`rank(I-P)`：1→3；一步后 \(Hu\sim10^{-16}\)） |
| CHK-23 | `test_c03` 是否真测迭代 | \(H=[[2,0],[2,0],[0,1],[0,1]]\) | **通过（测试有效）**：一步后 col0 为 `[1.6,1.6,0.4,0.4]`；两步后 \(\approx0\)。一步假实现过不了 |
| CHK-24 | C-rand / C-layer 匹配主范数 | 主基 seed=99 的 \(\|\Delta\|\) vs 对照 | **通过**（`actual_norm=2.7233772766385282` 完全相等；缺 `target_norm` 抛错；dummy rng(1) 范数 0.662，不相等；零 \(\Delta\) → `zero_norm`） |
| CHK-25 | 交换公式 | \(e_1+\Pi_{e_2}(e_2-e_1)=e_1+e_2\) | **通过** |
| CHK-26 | 集合路径负 excess、零分母、缺 sham | 手算 −0.5；全祖先袋；无 protocol | **通过** |
| CHK-27 | 矩阵 `noise=None` | `task=[[0,0,1]], behavior=[[1,0,1]]` | **通过**：S/M 的 noise/excess 均为 `None`；`null_reason=noise_missing`；raw 仍为 0.5 / 0.0 |
| CHK-28 | 并集 \(\rho\) vs \(\frac1n\sum\rho(s_i)\) | 步1 \(\rho=1/2\)、步2 \(T=B=\{1,2\}\) \(\rho=0\)，均值 0.25；并集 \(T=B=\{1,2\}\) | **失败**（C3-M-01）：`rho_S_raw=0` |
| CHK-29 | 空 `noise_set` | `[]` 且 protocol 无 hits；`[]` 且 `hits=['p3']` | **部分通过**：前者 `noise_set_empty`。后者伪造 `noise=0`、`excess=0.5`、`null_reason=None`（C3-M-07） |
| CHK-30 | Boundary Hidden=256；拒绝 128 | 形状 + `ValueError` | **通过** |
| CHK-31 | Repairability/RR 零分母；`run_repair` | 公式函数 vs 入口 | 公式 **通过**。入口默认 `generated_tokens=0`、`extra_prefill_tokens=len(original_tokens)`（C3-M-06） |
| CHK-32 | Procrustes \(R=UV^H\) | 已知正交 \(R\) 回收 \(\|AR-B\|_F\sim10^{-15}\) | **通过** |
| CHK-33 | `pytest` 数学相关 | `tests/test_science.py tests/test_measure.py tests/test_review_regressions.py -q` | **42 passed，exit 0**。不覆盖 CHK-28/29 后半、CHK-11 CLI、CHK-17 `precomputed` 反例、CHK-20 不一致 \(\rho\) |
| CHK-34 | 作者声称全仓库 70 | `python -m pytest tests -q`（本审查重跑，非采信） | **70 passed，9.94s**。不等于公式正确 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | CLI 校准仍用字面量/loss 拼分数（`cli.py` 366–375）；`cmd_analyze` 的 `p1/p2/p3` 为 `None` |
| 阅读其他 round-03 通道 | 任务禁止 |
| Abnar rollout 是否为论文承诺 | `attention_rollout` 是 \((A+I)\) 累乘，不是 \(\frac12 A+\frac12 I\)；未对原文验收 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数；高维功效属外部 |

---

## 6. 既有 ledger（独立确认，不采信 `fixed_pending_review`）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\)，常数分与排列均为 0.5 |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | `0<=α<1` 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | `work = work @ step`；反例可分 |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm`；匹配主范数 |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels` |
| C2-M-02 默认 P1 非留出 | **关闭（默认路径）** | 省略 `held_out` 且非 `precomputed` → `requires_held_out`。留出 OLS 能检出 \(\rho=y\)。**未关闭**：`precomputed` 仍是 `len+0.01*op`；不是 logistic（C3-M-02） |
| C2-M-03 `1-0.7≰0.3` | **关闭** | `q+1e-12` 保住该边；覆盖方向保守 |
| C2-M-04 并集 \(\rho\) | **未关闭** | 见 C3-M-01。ISSUES 也未把它标成本轮已修 |
| C2-M-05 监督/无标签同一 lstsq | **关闭（估计程序）** | 无标签：中心化 Procrustes / 中心化 lstsq；监督：未中心化 lstsq。平移反例 \(W\) 不同 |
| C2-M-06 P2 `None` TypeError | **关闭（崩溃）** | `missing_pair`。**未关闭**：不重算共享分母（C3-M-03） |
| C2-M-07 `a(X)` / CLI 校准 | **未关闭** | 见 C3-M-04 |
| C2-M-08 `run_repair` 预算 | **未关闭** | 见 C3-M-06 |
| 旧 C-M-05 矩阵缺噪声当 0 | **关闭** | CHK-27 |

---

## 7. 发现

状态：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

### C3-M-01 — 集合 API 不是 \(\rho_S(T)=\frac1n\sum\rho_S(s_i)\)

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `dependency_densities` 集合分支 `measure.py` **91–99**。CLI `cmd_label` **315–321** 对一个 ancestor 袋调用一次
- **原文：** §2.6（156）：\(\rho_S(T)=\frac1n\sum_i\rho_S(s_i)\)
- **反例（独立手算）：**
  - 步 1：\(P=\{1,2,3\},T=\{3\},B=\{1,3\}\) → \(\rho=1/2\)
  - 步 2：\(P=\{1,2,3\},T=\{1,2\},B=\{1,2\}\) → \(\rho=0\)
  - 均值 **0.25**
  - 并集一次调用 \(T=B=\{1,2\},P=\{1,2,3\}\) → `rho_S_raw=0`
- **影响：** 多步轨迹若把并集一次性传入，轨迹级依赖密度被压低/抬高。单图一次调用碰巧等于该图的 \(\rho_S(s)\)，不能冒充 \(\rho_S(T)\)
- **修复：** 逐步算再平均；N/A 步单独计数

### C3-M-02 — P1 留出分支是线性概率，不是 logistic；`precomputed` 仍是魔法系数

- **严重度：** Medium
- **状态：** confirmed defect（默认 silent 错估已关掉；指定估计量仍不符）
- **符号：** `p1_incremental` `analysis.py` **43–56**；`_fit_scores` **27–30**
- **原文：** §2.6 表 P1；§7（321）：控制链长与 op 后的 **logistic AUC** 与偏相关
- **证据：**
  - 默认（无 `held_out`、`precomputed=False`）→ `requires_held_out`。**不再**用 `10+0.01*op` 报数
  - 留出后半、\(n=40\)、`len≡10`、`op~N(0,1000)`、`rho=y`：OLS `auc_full=1`，`delta_auc=0.43`，`held_out=True`。污染 eval 行 \(X\) 后 train 分数差 0
  - 同数据 `precomputed=True`：`auc_full=0.6`，`delta=0.040`，`held_out=False`。旗标名像“已算好的分数”，实现仍是 `length+0.01*op[+rho]`
  - `_fit_scores` 是 `lstsq` 线性概率，不是 logistic；无偏相关；`bootstrap_cluster` 未挂上；不强制 \(\rho_S^{\mathrm{excess}}\)
- **影响：** 省略 `held_out` 时不能再 silently 写出假 ΔAUC。但 `precomputed=True`（`test_c01` 走这条）仍是旧估计量；即便走留出，报出的也不是论文的 logistic AUC
- **修复：** 去掉魔法系数路径，或让 `precomputed` 真正接收外部分数；train 上拟合两个 logistic，test 比 AUC；另报偏相关

### C3-M-03 — P2 None-safe，但不计算共享分母

- **严重度：** Medium
- **状态：** confirmed defect（崩溃已关；估计量未完成）
- **符号：** `p2_paired` `analysis.py` **67–96**
- **证据：** `p2_paired(None, 0.4, …)` → `missing_pair`，不再 TypeError。`shared_denominator` 在传入时原样返回，或 `len(shared_premises)`。`p2_paired(0.9, 0.1, 1.0, 0.0, 4)` 标 `ok`，不检验两 \(\rho\) 是否共用 \(|P\setminus T|\)
- **影响：** 新前提改分母时，无法区分“共享支撑上的 \(\Delta\rho\)”与“注入列”
- **修复：** 在共享前提上重算两个 \(\rho\)；不一致则 null

### C3-M-04 — `sequence_score` 默认不是 \(a(X)=\max(1-\hat p)\)；CLI 校准仍不是真分数

- **严重度：** Medium
- **状态：** confirmed defect（接口/流水线）
- **符号：** `sequence_score` `calibrate.py` **9–23**；`cli.cmd_calibrate` **366–375**
- **证据：** `[0.1,0.2]` 默认 → `0.2`；`one_minus_p` → `0.9`。CLI 默认 `[0.1,0.2,0.3,0.4]`，有探针时用 `abs(loss)` 拼四个标量，再逐个套 `one_minus_p`，与边、轨迹、`base_group_id` 无关
- **影响：** 命题 2 的覆盖声明不能从数据成立。阈值公式本身已对
- **修复：** 只在已知真边上算 `1-p`，轨迹取 max；N=独立基础题或已声明的块

### C3-M-05 — P3 仍无非目标、无相对基线 \(\Delta\mathrm{acc}\)

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `p3_recovery` `analysis.py` **99–106**。`intervention_report` 有四项相对对照，P3 入口不用它
- **原文：** §2.6 表 P3；§7（325）
- **证据：** 仅 `vs_crand/vs_clayer/invalid_rate`。禁句开关正确
- **影响：** 无法排除“靠损伤模型提分”
- **修复：** 与 `intervention_report` 合并；保留 REST-02

### C3-M-06 — `run_repair` 默认仍不供给真实解码长度

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `repair.py` **34–52**
- **证据：** `run_repair(..., [3,4], "abcd")` → `generated_tokens=0`，`extra_prefill_tokens=2`（`len(original_tokens)`），`original_token_budget=7`。传入 `generated_tokens=[1,2,3]` 后 generated=3。`repairability(1,0) is None` 公式函数本身正确。CLI `cmd_repair` 写死 `generated=[1,2]`
- **影响：** 走默认入口的 Repairability 恒为 1 或未定义。非本轮清单主项
- **修复：** 写入真实解码与 extra prefill token；按原始槽位 token 对齐预算

### C3-M-07 — 空 `noise_set` 在 protocol 带 `hits` 时伪造 0 参照

- **严重度：** Medium
- **状态：** confirmed defect（API；CLI 当前用 `noise_set=list(hits)`，两边同时空时走 `noise_set_empty`）
- **符号：** `measure.py` **106–117**
- **触发：** `noise_set=[]` 且 `sham_protocol.get("hits")` 为真
- **证据：** `P={p1,p2,p3},T={p1},B={p2},noise_set=[],hits=['p3']` → `rho_S_noise=0.0`，`rho_S_excess=0.5`，`null_reason=None`。空袋本应 null
- **影响：** 不一致输入被写成“已测噪声、扣除后仍有信号”
- **修复：** 空 `noise_set` 一律 null，不要用 `hits` 当逃生门

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C3-U-01 | Medium | `fit_linear_map` 无标签张量；`uses_labels` 只选 lstsq vs Procrustes | `transfer.py` 19–42 | 两条估计程序已不同，满足“分别拟合”。若“监督”必须吃任务/行为标签，则仍缺输入 |
| C3-U-02 | Medium | `apply_bilinear_inputs` 未被 CLI/analyze 调用；跨模型路径只跑 `direct_transfer(4096,3584)` | `transfer.py` 49–50；`cli.py` 447 | API 公式正确 |
| C3-U-03 | Medium | `cmd_fit` 对两个头用同一张 \(Y\)；无有限标签时填 `eye` | `cli.py` 339–348 | 估计程序在 \(\{0,1\}\) 上正确；伪造对角是流水线问题 |
| C3-U-04 | Low | `attention_rollout` 为 \((A+I)\) 累乘，不是 Abnar \(\frac12A+\frac12I\) | `baselines.py` 28–33 | 未核原文是否承诺官方 rollout |
| C3-U-05 | Low | INLP 默认 8 步在低维会把整空间投掉（本反例 `rank(I-P)=3`） | `interventions.py` 52–67 | 标准 INLP 会拟合残差噪声；高维 8 步可接受。实现是 lstsq 不是 SVM |
| C3-U-06 | Low | `predict_set(q=None)` 会 TypeError | `calibrate.py` 39–42 | 非法 q 应由校准入口挡住 |
| C3-U-07 | Low | 矩阵噪声数组含 NaN 且 `noise is not None` 时，`noise==1` 把 NaN 当未命中，S excess 变成 0.5 | `measure.py` 149–153 | 未见生产构造 |
| C3-U-08 | Low | P1 正类方向未固定；ρ 是否 excess 由调用方决定 | `analysis.py` 33–64 | 无断言 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C3-S-01 | 真实轨迹命题 2 覆盖 | 校准不计算边级 \(a(X)\) |
| C3-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明 N/A，未跑 `apply_bilinear_inputs` |
| C3-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册；analyze 不调用 P1–P3 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`（`bilinear.py` 21–29）；`fit` 在 \(y\in\{0,1\}\) 上的梯度（有限差）
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64
3. 未知哨兵 `-1` / 非 \(\{0,1\}\) / NaN 不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
4. Conformal \(k\) 公式、\(k>N\Rightarrow+\infty\)、\(\alpha\ge1\) 不再回绕；\(\alpha=0\Rightarrow+\infty\)
5. `predict_set([0.7], 0.3)` 现为 True（`1e-12` slack，覆盖保守）
6. `direct_transfer` 拒 4096≠3584；`apply_map` 维不匹配抛错；`apply_bilinear_inputs` 分别变换 H、E
7. 无标签适配 ≠ 监督 lstsq（平移与异维反例 \(W\) 不同）；同维正交可回收 \(R\)
8. `_auc` Mann–Whitney，平局 1/2，排列不变
9. 默认 P1 拒绝无留出调用；留出 `_fit_scores` 不用 eval 行的 \(X\)；留出 OLS 能检出被 op 淹没的 \(\rho=y\)
10. P2 缺测 → `missing_pair`，不再崩溃
11. 集合路径：零分母 None；缺 sham → excess None；负 excess −0.5 不截断；空 `noise_set` 且无 hits → `noise_set_empty`
12. 矩阵路径：`noise=None` → noise/excess None
13. INLP 在已投影 \(H\) 上迭代
14. C-rand / C-layer 匹配传入的主干预范数；缺范数即失败
15. 交换 \(H+\Pi_Z(H_d-H_b)\)
16. `p3_recovery["causal_reverse_claim"] is False`；相对 crand/clayer
17. `BoundaryMLP` Hidden=256，非 256 拒绝；2 层 ReLU
18. Week-8 无阈值 → `unregistered`，`scientific_conclusion is None`
19. Procrustes 形状不等 N/A；同形状可回收 \(R\)
20. `verbalizer(supervised, trained=False)` 拒绝

---

## 11. 测试质量（仅公式）

`42 passed`（数学三文件）与全仓库 `70 passed` **不能**证明本通道估计量正确。

- `test_c_unknown_label_is_masked` **有效**：`-1` 与仅正类项相等
- `test_p1_requires_held_out_by_default` **有效**
- `test_c01` 排列测的是 **`precomputed=True` 魔法系数路径**，不测 CHK-17 的留出增量
- `test_c01_held_out` 只断言 `held_out is True` 且 `auc_base is not None`，不断言未泄漏、不断言检出增量、不断言 logistic
- `test_c02` 覆盖 \(\alpha\ge1\)，不覆盖 `1-0.7` 浮点边、不覆盖按题去重的 \(N\)
- `test_c03` **有效**（第一步不是 \(e_1\)）
- `test_c04` / `test_b01` 有效关闭对应缺陷
- 无并集 vs 逐步、无 P2 `None`、无 `predict_set(0.7,0.3)`、无 labeled/unlabeled \(W\) 差、无 empty+hits、无 CLI \(a(X)\)

---

## 12. 结论

冻结哈希 `67bb9c90…` **已复现**。审查绑定该 55 文件快照。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | 通过 |
| 未知 mask / 空 \(\mathcal K\) | **通过**（C2-M-01 关闭） |
| conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\ge1\) 不回绕 | 通过 |
| `predict_set` \(1-p\le q\)（含 0.7/0.3） | **通过**（C2-M-03 关闭） |
| 迁移无 pad；4096→3584 N/A；labeled vs unlabeled | **通过（程序已分列）** |
| P1 留出 | **默认通过**；留出能检出增量；**不是 logistic**（C3-M-02） |
| P2 None-safe | **崩溃通过**；共享分母 **未计算**（C3-M-03） |
| P3 相对对照、无反向因果句 | 通过 asked 项；缺 nontarget/基线（C3-M-05） |
| INLP 在投影 H 上；C-rand/C-layer 匹配主范数 | 通过 |
| 有符号 excess；缺噪声为 null 不是 0 | 通过（空袋+hits 除外，C3-M-07） |
| Boundary hidden=256 | 通过 |

**可关闭（独立确认）：** C-01、C-02、C-03、C-04、C2-M-01、C2-M-02（仅默认路径）、C2-M-03、C2-M-05（仅“同一 lstsq”）、C2-M-06（仅 TypeError）、旧 C-M-05。

仍会污染论文数字的 confirmed defects：**C3-M-01（并集 \(\rho_S(T)\)）**。其次 C3-M-02（P1 非 logistic / `precomputed` 后门）、C3-M-03/04/05/06/07。

**验收意见：** `FAIL_MATH_STATS`。r2 指定的未知 BCE、默认 P1 非留出、`1-p<=q` 边、P2 崩溃、C-rand/INLP **本轮不再是拦路缺陷**。在 C3-M-01 关闭并经独立复审前，不得把集合路径一次并集调用写成 \(\rho_S(T)\)。在 C3-M-02 关闭前，不得把 P1 写成 logistic AUC。在 C3-M-04 关闭前，不得把 CLI 校准写成命题 2 覆盖。

---

## 附录：55 文件 SHA-256（POSIX relpath）

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  bf3440b0fd0fd01cfb08314690efade13c45ada89e3abfd98a77f4f5336e86cc
src/reasoning_diff/artifacts.py  61dc639ead0eff1fc1d0679f334c1853881cde6cadd80c56f7c091c252234293
src/reasoning_diff/baselines.py  2d28ef1cdff3bd571bd91fccf73e2f87d3dc4fc6b20d7816febfa0d48f05399c
src/reasoning_diff/cli.py  bcdf4f982b585f1da3751cd920bcd972ce433d93b256969af34a5ec7762dfd7b
src/reasoning_diff/edits.py  f201eb4931556ac03b1922ff132b3b7df5f49c9c7a5decf5308f45620276c3b2
src/reasoning_diff/events.py  73e9b2667e489b546ec4782c1019c99c2f07dc3530a0ae4824dc7cfd66f5c403
src/reasoning_diff/executor.py  d1760266a9a7606b3bd36eaf12d9fdde19a0533e3339842f32404773905b8d21
src/reasoning_diff/graphs.py  1e287cebf844cec0d055138224ae5a0b39c0358228c6587e8b4b6d4cfc604241
src/reasoning_diff/interventions.py  b971c432d1e2b2fd465fddbc673834e2a190a42b9ea44276631e7487c700a22e
src/reasoning_diff/io.py  c5c77a27d196e97da61947344a786137ee54cbaf4b2381208ce4d574da5b6897
src/reasoning_diff/measure.py  fde5ec49294e5b7409b673bd3d2d37c6af6bd838cc7bfb01ef2090ca5c448d70
src/reasoning_diff/models/__init__.py  0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8
src/reasoning_diff/models/adapters.py  a8680ef98b8075ce0f01cbcc43841a1974c1c93dfe7eb0ed248c50737c759ddc
src/reasoning_diff/models/collect.py  051e1b3005631c486b132b7889cfa7b91e85dc0dbcbd6d9d533907b8227815ad
src/reasoning_diff/models/features.py  ff5c6a79b9ecf0820be547e6dba39b6cfe9d705547d16587148e182e2d1e1e0e
src/reasoning_diff/models/generate.py  4fd7091842236d7a4249e41c7647ac13cece434f72f7f42c23a43b14cf02e012
src/reasoning_diff/models/tiny.py  bd916289e9aaa006e94f4a55e37cbc295982a5c057d7c5a7233a72e9c0860d69
src/reasoning_diff/probes/__init__.py  3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5
src/reasoning_diff/probes/bilinear.py  35e8d6ff7425f818e609cf527390c158c825ce019932b1664c3f9778ebd742e6
src/reasoning_diff/probes/boundary.py  a45ec29f20fc3b3c5f421c6b93bc66e909030e1d8854194137c3c0167a490347
src/reasoning_diff/probes/calibrate.py  16609e8f7007aab433b2ea12f13587582676d0ab103742a842ed82a801c8c864
src/reasoning_diff/repair.py  55cbcf07d0f42bbd3dfd36e194463c78e8b8b0eff0ee29623f6d4fcc22bb8d9e
src/reasoning_diff/rng.py  2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908
src/reasoning_diff/schema.py  5140f8b1687569b99cb3a3b728897ea8d9a825c9c2bc3371c42db43bf3f751fe
src/reasoning_diff/scoring.py  d05822c4fb784fe4a57d9f82f583eaa31c0f3b2e0e96c04b81f77db7413433f8
src/reasoning_diff/splits.py  fd871c0ae40ef72103d6ca6c61be809d559868e99f3fad949f95c7fcd78db436
src/reasoning_diff/tasks/__init__.py  4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754
src/reasoning_diff/tasks/catalog.py  5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0
src/reasoning_diff/tasks/t1_config.py  e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94
src/reasoning_diff/tasks/t1_fixture.py  01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41
src/reasoning_diff/tasks/t1_official.py  3267cf12bf9ef5e4578f98b7c01b20bdc5149385f603e3c2a8482b51daec1ab1
src/reasoning_diff/tasks/t2_gsm_plus.py  6d396506526c52814ef5562d7a95fd9d6739fdbe2ea182d8bbf56fe1d528eaed
src/reasoning_diff/tasks/t2_gsm_symbolic.py  f0492a797e6d89a021092272bfc0cd31b386d7c99752160bc6078722879d0628
src/reasoning_diff/tasks/t2_noop.py  26cf5c21b5838a6bf1a335bf8b0eb5bc767a77c2e4128fc8a36a8c482456c874
src/reasoning_diff/tasks/t3_hotpot.py  e5e7a9075ea64df98076d06b00ce88fce410c83cc52840ee8c7eba7949aa5bdd
src/reasoning_diff/tasks/t3_humaneval.py  3f74a52b59748db72da703d34229ad62d0bba833aed2bad21e2fc82e828e82de
src/reasoning_diff/tasks/t3_musique.py  761c8bc8b7c77bfe3b55a558916ce92b70d3ae6a5095308e437c216a0f811aaa
src/reasoning_diff/tasks/t4_boundary.py  a2ca9188353b213d2c7c617dd27c60415adb0c16c40326ae8a7ecce03f94a5f9
src/reasoning_diff/transfer.py  cffe4791564fbb9ca19561691faac2fee106dc48d1b05cfcdd0ef000892697b4
tests/conftest.py  1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1
tests/test_artifacts.py  830953f379954233c76c9aab9f5f4b3860ea598579015a58bddd9909c5bd3278
tests/test_cli_pipeline.py  63b4c09f51f6c7d807e8928f27fa62ec54e3f4656229b3615371ae930b5de0b9
tests/test_generate_loop.py  ffe10b0d6812908ca34f446103b22a23c2e857a85172cc78e72caf005a979a46
tests/test_measure.py  fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab
tests/test_review_regressions.py  1e91c98d55e645480f89599f7e12a1fb8bb02ca4929c463aa743de75e143c8c5
tests/test_science.py  3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  54e57fea7417d901c75b7d17cfe9b90ee442f2d634a08d22272a678959ce9650
tests/test_tiny_cache.py  097a48534da1e870244bae2da2a849a65fda2c00233c3fe1b8792897e0fc5024
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  64150ec08e6059e11a492e663d355a59d351c4bdbb28e6be603a6167598deb8e
```
