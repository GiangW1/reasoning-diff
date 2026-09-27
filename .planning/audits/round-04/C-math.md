# C：数学与统计独立审查（round-04）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导双线性/加权 BCE 未知掩码、split conformal、`predict_set` 的 \(1-p\le q\)、P1 留出 logistic、`precomputed` 调用方分数、P2 共享分母一致性与 None-safe、P3 对照+非目标、\(\rho_S(T)\) 逐步均值、空 `noise_set`、INLP、C-rand 范数、4096≠3584、labeled vs unlabeled、`cone_fit`、Week-8 门。仍错则给反例。重跑数学测试。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读 round-04 的 A/B/D/E/F。体例对照过 `round-03/C-math.md`，**结论全部由本轮对当前磁盘字节的公式推导与数值反例重做**，不沿用上一轮状态，不采信 ISSUES 的 `fixed_pending_review`
- 声明冻结哈希：`fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17`（`.planning/audits/round-04/VERSION.md`，56 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**是**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改（只写本文件）
- numpy：1.26.4；CPython 3.11.7

---

## 1. 冻结哈希

范围内文件数：**56**（`src/reasoning_diff/**/*.py` 41 + `tests/**/*.py` 14 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「56 files」一致。相对 r03 的 55 文件，多出 `tests/test_round03_regressions.py`。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 方法 | SHA-256 | 与声明值 |
|---|---|---|
| VERSION 脚本（本审查独立执行） | `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17` | **是** |

审查对象绑定该冻结快照。逐文件 SHA-256 见附录。下列公式结论绑定这些 digest。

---

## 2. 范围与覆盖

| 文件 | 行 | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/bilinear.py` | 1–95 | `52de70553b37dec69822b790b006b7282e58ee926bb77006b3da40b419726e15` | `score`/`predict_matrix`/`fit`/`weighted_bce` | 全文；独立数值 + 有限差 + 未知哨兵 |
| `src/reasoning_diff/probes/calibrate.py` | 1–42 | `16609e8f7007aab433b2ea12f13587582676d0ab103742a842ed82a801c8c864` | `sequence_score`/`conformal_threshold`/`predict_set` | 全文；手算 \(k\)；`1-0.7` 边 |
| `src/reasoning_diff/probes/boundary.py` | 1–44 | `7f9d62ab84f9452cd7c5a863b5d719aa162c4988b6e5d519efc4daca944d00cc` | `BoundaryMLP` Hidden=256；报告损失 | 全文；括号反例 |
| `src/reasoning_diff/analysis.py` | 1–253 | `18adcce069d4b50e4e77d92525335951f2feb57282bdaa194bda3b07f7103875` | `_auc`/`_fit_scores`/`p1_incremental`/`p2_paired`/`p3_recovery`/`cone_fit`/`week8_decision` | 全文；IRLS logistic；grid 锥拟合 |
| `src/reasoning_diff/transfer.py` | 1–52 | `c58e673a5bc9684169ad7275da295099386962ddc348f579838ac9bb86366af0` | `direct_transfer`/`fit_linear_map`/`apply_map`/`apply_bilinear_inputs` | 全文；labeled 张量；平移/异维 \(W\) |
| `src/reasoning_diff/measure.py` | 1–320 | `b287249e03b493546e378175d4945e2d99bf129b1cc2ed0227db1f26dc7f13f9` | `dependency_densities`/`event_density_sets`/`_matrix_densities` | 全文；均值；空袋；0-hit 构造 |
| `src/reasoning_diff/interventions.py` | 1–115 | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | `inlp_remove`/`c_rand_delta`/`c_layer_delta`/`project_delta` | 全文；多步秩；范数匹配 |
| `src/reasoning_diff/repair.py` | 1–73 | `9fa3ddbe26334273d4a0dfb92f3faf8fee788ed34a07f9523117c1b87e0b7290` | `repairability`/`run_repair` | 对照 |
| `src/reasoning_diff/baselines.py` | 1–80 | `7c0f14a9dd90a87750872f90d5634736538c370d715252c48875b25e59079ee1` | rollout / verbalizer | 全文（非本通道主公式） |
| `src/reasoning_diff/cli.py` | 352–584 | `c7b8061e036c9f83a84b13df01e96e73fc89e9f66b47bd3010349441f0f11c45` | `cmd_label`/`cmd_fit`/`cmd_calibrate`/`cmd_analyze` | 只读调用链 |
| `tests/test_science.py` | 1–97 | `3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c` | 校准规定例 / 4096≠3584 | 查是否独立 |
| `tests/test_measure.py` | 1–40 | `fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab` | 负 excess / 零分母 | 集合路径 |
| `tests/test_review_regressions.py` | 1–394 | `37414926677d059610794b4f64ec3bcbf7c242ecce9c563bc8e549abc5d3a60c` | C-01..C-04 / 未知 BCE / 事件均值 | 查测试能否关闭缺陷 |
| `tests/test_round03_regressions.py` | 1–288 | `70475c77edce6844cad811c010f4ecb29aa764dc11b24ccb5d3de1dd14b09e51` | C3-M-01/02/03/05/07 / cone / labeled | 查是否独立 oracle |

调用链只读、不计入“已证明正确”：`cli.cmd_fit` / `cmd_calibrate` / `cmd_intervene` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文：`Reasoning-Diff-修订方案-v3 (1).md` §2.5–2.6、§4.2、§5–7、附录 S2–S3；PITFALLS 校准/P1/P2 条；REQUIREMENTS PROBE-01 / PROP2-01 / C3-01 / XFER-01 / GEOM-01 / CAUSAL-01。

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

`score` / `predict_matrix` 与上式一致。`weighted_bce` **87–95** 与 `fit` **44–47** 把 \(\mathcal K\) 限制为有限且 \(y\in\{0,1\}\)；空 \(\mathcal K\) 分别返回 NaN / `loss=None`。

### 3.2 Split conformal 与预测集

\[
a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij}),
\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow q=+\infty\)。\(\alpha\notin[0,1)\) 必须拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。等于 \(q\) 的边须保留。在同一浮点通道比较已算好的 \(1-p\) 与 \(q\)；十进制字面量 `0.7/0.3` 会破边。

`conformal_threshold` 的 \(k\) 与非法 \(\alpha\) 分支与上式一致。`predict_set` 为 \((1-p)\le q+10^{-12}\)。`sequence_score` 默认仍是 `max(给定分数)`；`nonconformity="one_minus_p"` 才算 \(\max(1-p)\)，且对传入的**全部**列取 max，不是 \(j\in R(s_i)\)。

### 3.3 迁移

维不等 ⇒ 直接迁移 N/A，禁止 pad/truncate。无标签配对：中心化后正交 Procrustes（同维）或中心化 lstsq（异维）。监督适配必须是**不同估计程序**；若声称使用标签，必须有标签张量。双线性要成对映射 \(H\) 与 \(E\)。

### 3.4 P1–P3

- **P1：** 在 train 拟合控制模型 vs 控制+\(\rho\)（原文 / PITFALLS：logistic）；在**留出**基础题上比 Mann–Whitney AUC。平局贡献 \(1/2\)。默认路径不得写死 `len+0.01*op`。`precomputed` 必须是调用方已算好的分数，不是魔法系数。偏相关与题级 bootstrap 另报。
- **P2：** \(\Delta\rho=\rho_{\mathrm{noop}}-\rho_{\mathrm{base}}\) 必须共用分母 \(|P\setminus R_{\mathrm{task}}|\)；缺配对不得崩。传入的 `shared_denom` 须与 `|shared_premises|` 一致。
- **P3：** 相对 C-rand / C-layer；报告非目标响应与相对基线 \(\Delta\mathrm{acc}\)。不得写“只是后果”。

### 3.5 Excess / INLP / 对照范数 / 锥

缺失噪声协议 ⇒ excess = null，不得把参照当 0。空 `noise_set` 一律 null（与“已评估且 0 hit ⇒ \(N=\emptyset\)、noise=0”不是同一状态）。excess 可负。\(\rho_S(T)=\frac1n\sum_i\rho_S(s_i)\)，不是并集一次调用。

INLP：每步在**已投影** \(H\) 上重拟合，再累乘 \(I-uu^\top\)。C-rand / C-layer 必须缩放到**该样本主干预实际** \(\|\Delta\|\)。

附录 S2：

\[
\frac{|\mathrm{cone}|}{n}\approx 1-\exp\{-\lambda(1-x)^\gamma\}.
\]

必须对 \((\lambda,\gamma)\) 做拟合；\(R^2\) 只作描述，不得当贡献。Week-8 Gate 0–2 无预注册阈值时必须保持 `unregistered`，不得发明通过线。

Boundary MLP：2 层 ReLU，Hidden=256；报告损失须是 BCE。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(\langle hU,eV\rangle\) 与 \((HU)(EV)^\top\) | 独立 `h@U@V.T@e` vs `score`/`predict_matrix` | **通过**（误差 0） |
| CHK-02 | 默认 `rank=64`、`fn_weight=10` | 构造 | **通过** |
| CHK-03 | \(y\in\{0,1\}\) 加权 BCE | 手算 \(0.5(10(-\log 0.8)+(-\log 0.8))=1.2272895322281534\) | **通过** |
| CHK-04 | 空 mask；`y=-1` / `y=2` / `y=0.5` | 直接调用 | **通过**：`-1`/`2`/`0.5`/`nan` 均等于仅正类项 \(10(-\log 0.8)=2.231435513142097\)。若把 `-1` 当负类会得到旧泄漏值 `1.2272895322281534`，现不再如此。空 mask → NaN |
| CHK-05 | `y=nan` 是否排除 | `weighted_bce` | **通过** |
| CHK-06 | `fit` 梯度 | \(U_{00}\) 解析 vs 有限差，相对误差 \(1.25\times10^{-10}\) | **通过**（已知 \(\{0,1\}\)） |
| CHK-07 | `fit(-1)` 是否等于 `fit(nan)` | 同初值一步 | **通过**（\(\Delta U=0\)，loss 同 \(4.721939809098778\)）。空 \(\mathcal K\) → `no_known_labels` |
| CHK-08 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | \(N=4,\alpha=0.4\Rightarrow k=3,q=0.3\)；\(\alpha=0.1\Rightarrow+\infty\)；\(N=1,\alpha=0.05\Rightarrow+\infty\)；\(N=3,\alpha=0.5\Rightarrow k=2,q=0.2\)；\(N=10,\alpha=0.05\Rightarrow+\infty\)；\(\alpha=0\Rightarrow+\infty\) | **通过** |
| CHK-09 | \(\alpha\ge 1\)、\(\alpha<0\)、`None` 不回绕 | \(\alpha=1,1.5,-0.1,\mathrm{None}\) | **通过**（`invalid`，`q is None`） |
| CHK-10 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**：`1.0-0.7=0.30000000000000004`，无 slack 为 False，`+1e-12` 后为 True。`0.4` 边排除；\(q=+\infty\) 全选；`0.5` 边通过 |
| CHK-11 | `sequence_score` / \(a(X)\) | `[0.1,0.2]`；真边 \(p=0.9\)、假边 \(p=0.1\) | **部分通过**：默认 `0.2`；`one_minus_p` → `0.9`。真集限制失败（C4-M-02）：论文 \(a=0.1\)，代码 \(0.9\) |
| CHK-12 | 4096≠3584；维不匹配无 pad | `direct_transfer`；`(2,3)@(4,2)` | **通过**（N/A；`matmul` 形状错） |
| CHK-13 | labeled 缺张量 | `labeled=True, labels=None` | **通过**（`ValueError: supervised adapt requires a label tensor`） |
| CHK-14 | labeled vs unlabeled 是否改估计 | 平移 \(X'=X+c\)；异维随机对；对角缩放 | **通过（程序已分列）**：平移 unlabeled 回收 \(I\)（\(\|W-I\|_\infty\sim10^{-15}\)），labeled 差 \(10.0\)；对角例 \(\|W_{\mathrm{lab}}-W_{\mathrm{unl}}\|_\infty=0.5\)。标签张量不进估计（C4-U-01）：`[0,1]` 与 `[1,0]` 的 \(\|W\|_\infty\) 差为 **0** |
| CHK-15 | 常数分数 AUC 与排列 | `_auc(ones, y)` | **通过**（0.5） |
| CHK-16 | Mann–Whitney 平局 | 分数 `[1,2,2,3]`，标签 `[0,0,1,1]` | **通过**（手算 \(0.875\)） |
| CHK-17 | 默认 P1；留出 logistic；`precomputed` | \(n=40\)，`len≡10`，`op~N(0,1000)`，`rho=y` | **默认通过**（`requires_held_out`）。**留出通过**：`estimator=held_out_logistic`，`auc_full=1`，`delta=0.29`，分数落在 \((0,1)\)。**`precomputed` 通过**：`estimator=precomputed_scores`，`auc_base=0.5`（常数 length），`auc_full=1`，`delta=0.5`。旧魔法 `10+0.01*op` 在 held 上 AUC=0.71，现不再被这条路径使用 |
| CHK-18 | 留出拟合是否忽略 eval 行的 \(X\) | 只改 held-out 行再 `_fit_scores` | **通过**（train 分数差 0；eval 分数变 \(0.598\)） |
| CHK-19 | 空/满 `held_out` | 全 True / 全 False | **通过**（`held_out_empty`） |
| CHK-20 | P2 减法、None、分母一致性 | `p2_paired(0.2,0.5,0.8,0.6,4)`；`None`；`99` vs `['p1']` | **通过 asked 项**：差值 \(0.3/-0.2\)；`None` → `missing_pair`；`99` vs 1 元列表 → `denominator_inconsistent`。**残留**（C4-U-03）：`p2_paired(0.9,0.1,1,0,4, shared_premises=list('abcd'))` 仍 `ok`，\(0.9\) 不可能是分母 4 上的 \(\|S\|/4\) |
| CHK-21 | P3 相对对照、非目标、禁句 | `p3_recovery(0.5,0.4,0.3,0.1,nontarget=0.2,baseline_acc=0.45)` | **通过**：`vs_crand=0.1`，`vs_clayer=0.2`，`vs_baseline=0.05`，`nontarget=0.2`，`causal_reverse_claim is False`。缺测时 nontarget/vs_baseline 为 None |
| CHK-22 | INLP 更新 \(H\) | 手算第一步 \(w=(0.5,-1)\)；`steps=1` vs `8` | **通过**：一步后 \(H P=\[[1.6,0.8],[1.6,0.8],[0.4,0.2],[0.4,0.2]]\)；两步后 \(\approx 0\)；`max\|P1-P8\|>0` |
| CHK-23 | `test_c03` 是否真测迭代 | 同上 | **通过（测试有效）**：一步不是 \(e_1\) 消掉 |
| CHK-24 | C-rand / C-layer 匹配主范数 | 主基 seed=99 的 \(\|\Delta\|\) vs 对照 | **通过**（`actual_norm=2.7233772766385282` 完全相等；缺 `target_norm` 抛错；dummy rng(1) 范数 0.662，不相等；零 \(\Delta\) → `zero_norm`） |
| CHK-25 | 交换公式 | \(e_1+\Pi_{e_2}(e_2-e_1)=e_1+e_2\) | **通过** |
| CHK-26 | 集合路径负 excess、零分母、缺 sham | 手算 −0.5；全祖先袋；无 protocol | **通过** |
| CHK-27 | 矩阵 `noise=None` | `task=[[0,1]], behavior=[[1,0]]`（回归） | **通过**（测试锁住 null） |
| CHK-28 | 并集 \(\rho\) vs \(\frac1n\sum\rho(s_i)\) | 步1 \(\rho=1/2\)、步2 \(\rho=0\)，均值 **0.25**；`event_sets` | **通过**（`aggregation=mean_over_events`，`rho_S_raw=0.25`）。无 `event_sets` 的单袋调用仍是单事件 \(\rho_S(s)\)，不是轨迹均值 |
| CHK-29 | 空 `noise_set` 一律 null | `[]` + protocol `hits=['p3']` | **API 通过**：`rho_S_noise is None`，`null_reason=noise_set_empty`，不再用 hits 逃生。**生产构造失败**（C4-M-01） |
| CHK-30 | 已评估 0-hit sham | 任务 \(T=\{p1,p2\},B=\{p3\}\)，labels `noise_ref=0` | **失败**（C4-M-01）：手算 \(\rho=1\)、noise=0、excess=1；`event_density_sets` 得 `raw=1`、`noise=None`、`excess=None` |
| CHK-31 | Boundary Hidden=256；拒绝 128 | 形状 + `ValueError` | **通过** |
| CHK-32 | Boundary 报告损失 | \(y=0,p=\sigma(10)\approx 0.9999546\) | **失败**（C4-M-03）：报告 `-10.000045398900186`；真 BCE \(\approx 10.000045\) |
| CHK-33 | `cone_fit` 是否拟合 | \(y=1-e^{-0.8(1-x)^{1.5}}\)，\(n=12\) | **通过**：`r2=0.9776421802579095`，\((\hat\lambda,\hat\gamma)=(0.6812920690579611,1.2)\)（grid 最近元，不是 stub）。\(n<2\) → `r2=None`。`wording=descriptive_only` |
| CHK-34 | Week-8 无发明门 | 默认；传入阈值 | **默认通过**：三门 `threshold=None`/`unregistered`，`scientific_conclusion is None`，`skip_p2_p3=True`。传入阈值会标 `evaluated` 但不比较测量（C4-U-04） |
| CHK-35 | Repairability/RR 零分母 | 公式函数 vs 入口 | 公式 **通过**（`repairability(1,0) is None`，`4/10=0.6`）。入口默认 `generated_tokens=0`，`extra_prefill_tokens=len(new_prefix.split())` |
| CHK-36 | `pytest` 数学相关 | `tests/test_science.py tests/test_measure.py tests/test_review_regressions.py tests/test_round03_regressions.py -q` | **69 passed，exit 0**。不覆盖 CHK-11 真边、CHK-30、CHK-32、CHK-14 标签无用 |
| CHK-37 | 作者声称全仓库 97 | `python -m pytest tests -q`（本审查重跑，非采信） | **97 passed，11.22s**。不等于公式正确 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1、配对迁移 | CLI 校准不限制 \(j\in R(s_i)\)（C4-M-02）；真实权重属 pending_server |
| 阅读其他 round-04 通道 | 任务禁止 |
| 在真实权重上核对 INLP 8 步有效秩 | 本通道只验证迭代代数；高维功效属外部 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用分数值域、污染 eval \(X\)、检出 \(\rho=y\) 代替 |

---

## 6. 既有 ledger（独立确认，不采信 `fixed_pending_review`）

| Ledger | 本轮 | 说明 |
|---|---|---|
| C-01 顺序敏感 trapz AUC | **关闭** | `_auc` 是 \(P(s_+>s_-)+0.5P(=)\) |
| C-02 conformal \(\alpha\ge1\) 回绕 | **关闭** | `0<=α<1` 否则 `invalid` |
| C-03 INLP 不投影 H | **关闭** | `work = work @ step` |
| C-04 C-rand 用 rng(1) 哑范数 | **关闭** | 强制 `target_norm`；匹配主范数 |
| C2-M-01 未知 BCE / 空批为 0 | **关闭** | \(\mathcal K=\{0,1\}\)；空 → NaN / `no_known_labels` |
| C2-M-02 默认 P1 非留出 | **关闭** | 省略 `held_out` 且非 `precomputed` → `requires_held_out` |
| C3-M-02 P1 非 logistic / `precomputed` 魔法系数 | **关闭** | `_fit_scores` 为 30 步 IRLS logistic；`precomputed` 把 `length`/`rho` 当调用方分数 |
| C2-M-03 `1-0.7≰0.3` | **关闭** | `q+1e-12` 保住该边 |
| C3-M-01 并集 \(\rho_S(T)\) | **关闭** | `event_sets` → `mean_over_events`；r03 反例现得 0.25。CLI `cmd_label` 走 `event_density_sets` |
| C2-M-05 监督/无标签同一 lstsq | **关闭（估计程序）** | 无标签：中心化 Procrustes / 中心化 lstsq；监督：未中心化 lstsq |
| C2-M-06 P2 `None` TypeError | **关闭** | `missing_pair` |
| C3-M-03 共享分母 | **关闭 asked 项** | `shared_denom != \|shared_premises\|` → `denominator_inconsistent`。不重算 \(\rho\) 见 C4-U-03 |
| C3-M-04 `a(X)` / CLI 校准 | **部分关闭** | scientific 拒绝字面量/loss；有探针时用 `one_minus_p`。真边限制未关（C4-M-02） |
| C3-M-05 P3 非目标 | **关闭（接口）** | `nontarget` / `vs_baseline` 字段存在；CLI 仍只回传调用方表 |
| C3-M-06 `run_repair` 预算 | **部分关闭** | `extra_prefill_tokens=len(new_prefix.split())`；传入 `generated_tokens` 后计数正确。默认仍 0 |
| C3-M-07 空袋+hits 伪造 0 | **API 关闭** | 空 `noise_set` 一律 `noise_set_empty`。生产 0-hit 见 C4-M-01 |
| 旧 C-M-05 矩阵缺噪声当 0 | **关闭** | 回归仍在 |
| `cone_fit` 空壳 | **关闭** | grid 最小化 \(SS_{\mathrm{res}}\) |

---

## 7. 发现

状态：`confirmed defect` | `未证实疑点` | `外部待验证` | `非缺陷建议`。

### C4-M-01 — 已评估且 0-hit 的 sham 被写成 empty `noise_set`，有效 excess 变成 null

- **严重度：** High
- **状态：** confirmed defect
- **符号：** `event_density_sets` `measure.py` **273–280**；空袋分支 **128–133**。CLI `cmd_label` **368–369** 走这条
- **原文：** §2.6 / §7：先报 \(\rho_S^{\mathrm{noise}}\) 再扣。已评估且无 sham 变化 ⇒ \(N=\emptyset\)，noise \(=0\)，excess \(=\) raw，**不是**缺失
- **本轮 API 契约（独立确认）：** 调用方传入 `noise_set=[]` 一律 `noise_set_empty`。这关闭了 C3-M-07 的 hits 逃生门，本身不是本条的问题
- **反例（独立手算）：**
  - 任务：\(P=\{p1,p2,p3\}\)，\(q\) 祖先 \(T=\{p1,p2\}\)，行为 \(B=\{p3\}\)
  - \(S=\{p3\}\)，\(|P\setminus T|=1\)，\(\rho_S=1\)
  - 三条 label 的 `noise_ref=0.0`（sham 已做、全 miss）⇒ hits `[]`
  - 公式：noise \(=|N\setminus T|/|P\setminus T|=0\)，excess \(=1-0=1\)
  - `event_density_sets(...)`：`rho_S_raw=1.0`，`rho_S_noise=None`，`rho_S_excess=None`，事件 `null_reason=noise_set_empty`
- **影响：** 生产标注路径无法表示“观测到的零噪声”。0-hit 是 sham 的合法结果，会被写成 C3 未测。Week-8 / analyze 读到的 `rho_S_excess` 为 null，后续 P2/P3 分流被空参照扭曲
- **修复：** 区分 missing（`noise_set is None` / 无 `noise_ref`）与 evaluated-zero（有 `noise_ref` 且 hits 空 ⇒ \(N=\emptyset\)、noise=0）。空列表 API 可继续 null，但构造器不得把已评估 0-hit 填成 `[]`

### C4-M-02 — \(a(X)\) 仍是全列 \(\max(1-p)\)，不是 \(\max_{j\in R(s_i)}(1-p)\)

- **严重度：** Medium
- **状态：** confirmed defect（接口/流水线；阈值公式本身已对）
- **符号：** `sequence_score` `calibrate.py` **21–23**；`cli.cmd_calibrate` **432**
- **原文：** §2.5（134）：\(a(X)=\max_{i,\,j\in R(s_i)}(1-\hat p_{ij})\)
- **反例：** 一行 \(\hat p=(0.9,0.1,0.8)\)，真依赖只有第 0 列
  - 论文：\(a=1-0.9=0.1\)
  - `sequence_score(..., nonconformity="one_minus_p")`：`0.9`
- **证据：** CLI 在有 `U` 与 `features.npz` 时对 `predict_matrix` 的**每一列**取 `one_minus_p`，不读标签、不限制 \(R(s_i)\)。默认 `sequence_score` 仍是 `max(p)`（`[0.1,0.2]→0.2`）
- **影响：** 命题 2 的 \(q_\alpha\) 被假阴边抬高；覆盖事件与 \(N\) 的可交换单位都不是原文定义。scientific 模式已拒绝字面量，不再是 C3-M-04 的 loss 拼数
- **修复：** 只在已知真边上算 \(1-p\)，轨迹取 max；空真集才为 0；\(N=\) 独立基础题或已声明的块

### C4-M-03 — `BoundaryMLP.fit` 报告的 BCE 括号写反，损失可为负

- **严重度：** Medium
- **状态：** confirmed defect
- **符号：** `boundary.py` **43**
- **公式：** 标准 BCE 为 \(-\bigl[y\log p+(1-y)\log(1-p)\bigr]\)
- **代码：** `-(y*log(p) - (1-y)*log(1-p))` \(= -y\log p+(1-y)\log(1-p)\)
- **反例：** \(y=(0,0)\)，\(p=\sigma(10)\approx(0.9999546,0.9999546)\)
  - 真 BCE \(\approx 10.000045398900186\)
  - 报告 `loss=-10.000045398900186`
- **影响：** 梯度仍用 `pred-y`，拟合方向大体对；任何写入报告/早停的 loss 在负类上会减而不是加。`test_boundary_mlp_trains` 只断言 `status==ok` 与形状
- **修复：** 改成 `-(y*log(p)+(1-y)*log(1-p))`，并锁 \(y=0,p\to1\) 不得为负

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C4-U-01 | Medium | `fit_linear_map` 要求 `labels` 但不使用；`[0,1]` 与 `[1,0]` 的 \(W\) 相同 | `transfer.py` 23–27 | asked 项“必须有张量 / 两套程序不同”已满足。若“监督”必须吃任务/行为标签，则估计量仍是未中心化 lstsq |
| C4-U-02 | Low | P1 不返回 `bootstrap_cluster` 区间；偏相关用全样本不是留出 | `analysis.py` 72、84–94、242–253 | 原文要区间。本轮清单只验 logistic / `precomputed`。\(\rho=y\) 时全样本与留出偏相关都是 1，无数值分裂 |
| C4-U-03 | Low | P2 不在共享前提上重算 \(\rho\)；`0.9` 对分母 4 仍 `ok` | `analysis.py` 129–137 | 整数一致性与 None-safe 已关 C3-M-03 asked 项。\(0.9\notin\{0,1/4,1/2,3/4,1\}\) |
| C4-U-04 | Low | 传入 `gate_thresholds` 后三门标 `evaluated`，不比较任何测量 | `analysis.py` 161–166 | 默认 analyze 不传阈值，三门保持 `unregistered`。本轮“无发明门”默认路径成立 |
| C4-U-05 | Low | `event_sets` 对 None 密度跳过再平均：`[None, 1]` → `1.0` 不是 `1/2` | `measure.py` 107–109 | 分母为空记 N/A 后，\(n\) 是否含 N/A 步原文未写死 |
| C4-U-06 | Low | INLP 用 lstsq(\(\pm1\)) 不是 SVM；低维 8 步可投掉整空间 | `interventions.py` 52–67 | 迭代投影本身已对 |
| C4-U-07 | Low | `cmd_analyze` 在 `rho_S_excess is None` 且已有 P1 表时仍写 p2/p3；`skip_p2_p3` 只是旗标 | `cli.py` 551–578；`analysis.py` 171–187 | 流水线问题；公式函数未发明结论句 |
| C4-U-08 | Low | `predict_set(q=None)` TypeError | `calibrate.py` 39–42 | 非法 q 应由校准入口挡住 |
| C4-U-09 | Low | `run_repair` 默认 `generated_tokens=0`；prefill 按空白分词不是 tokenizer | `repair.py` 50–57 | 非本轮清单主项；传入列表后计数正确 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C4-S-01 | 真实轨迹命题 2 覆盖 | 校准不按真边算 \(a(X)\) |
| C4-S-02 | 4096↔3584 适配后的双线性 | 映射器存在；analyze 只声明 N/A |
| C4-S-03 | 预注册后的 P1–P3 区间 | Gate 未注册；真实轨迹未跑 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. 双线性评分与 `predict_matrix`（`bilinear.py` 21–29）；`fit` 在 \(y\in\{0,1\}\) 上的梯度（有限差 \(1.25\times10^{-10}\)）
2. \(\lambda_{\mathrm{FN}}=10\)，默认 rank 64
3. 未知哨兵 `-1` / 非 \(\{0,1\}\) / NaN 不进 BCE；空 \(\mathcal K\) 为 NaN / `no_known_labels`
4. Conformal \(k\) 公式、\(k>N\Rightarrow+\infty\)、\(\alpha\notin[0,1)\) 拒绝；\(\alpha=0\Rightarrow+\infty\)
5. `predict_set([0.7], 0.3)` 为 True（`1e-12` slack）
6. `direct_transfer` 拒 4096≠3584；`apply_map` 维不匹配无法乘；`apply_bilinear_inputs` 分别变换 H、E
7. `labeled=True` 无张量即失败；无标签适配 ≠ 监督 lstsq（平移回收 \(I\)，监督不回收）
8. `_auc` Mann–Whitney，平局 1/2
9. 默认 P1 拒绝无留出；留出 IRLS logistic 不吃 eval 行的 \(X\)；能检出被 op 淹没的 \(\rho=y\)；`precomputed` 是调用方分数，不是 `length+0.01*op`
10. P2 缺测 → `missing_pair`；`shared_denom` 与 `|shared_premises|` 不一致 → `denominator_inconsistent`
11. P3：`vs_crand`/`vs_clayer`/`vs_baseline`/`nontarget`；`causal_reverse_claim is False`
12. `event_sets` 均值 0.25，不是并集 0；CLI label 走 `event_density_sets`
13. 空 `noise_set` API 一律 null，忽略 protocol `hits`
14. 集合/矩阵：零分母 None；缺 sham → excess None；负 excess −0.5 不截断
15. INLP 在已投影 \(H\) 上迭代
16. C-rand / C-layer 匹配传入的主干预范数；缺范数即失败
17. 交换 \(H+\Pi_Z(H_d-H_b)\)
18. `BoundaryMLP` Hidden=256，非 256 拒绝；2 层 ReLU
19. `cone_fit` 对 \((\lambda,\gamma)\) 做 \(25\times20\) grid，返回 r2/参数；措辞 `descriptive_only`
20. Week-8 默认三门 `unregistered`，`scientific_conclusion is None`，不发明通过线
21. `verbalizer(supervised, trained=False)` 拒绝

---

## 11. 测试质量（仅公式）

`69 passed`（数学四文件）与全仓库 `97 passed` **不能**证明本通道估计量正确。

- `test_c_unknown_label_is_masked` **有效**
- `test_p1_requires_held_out_by_default` / `test_p1_held_out_logistic_detects_rho` **有效**（后者断言 `auc_full==1` 且 `delta>0`）
- `test_p1_precomputed_is_scores_not_magic` **有效**（同分数 delta=0，estimator 名）
- `test_c01` 仍走 `precomputed=True`，现与“调用方分数”一致
- `test_c3_m01_event_mean_not_union` **有效**（0.25）
- `test_c3_m07_empty_noise_ignores_hits` **有效（API）**；不测 `event_density_sets` 的 0-hit 构造
- `test_p2_inconsistent_denom_is_null` **有效**（整数）；不测不可能的 \(\rho=0.9\)
- `test_p3_reports_nontarget` **有效（字段）**
- `test_sequence_score_units_and_predict_set` 锁住 `0.7/0.3` 边；**同时锁住默认 `max(p)`**
- `test_cone_fit_returns_r2` 只断言 `r2>0.9`，不回收真 \((\lambda,\gamma)\)
- `test_boundary_mlp_trains` 不验损失符号
- `test_labeled_transfer_needs_labels` 不验标签是否进入 \(W\)
- 无 0-hit sham、无真边 \(a(X)\)、无负 BCE

---

## 12. 结论

冻结哈希 `fb1e3df…` **已复现**。审查绑定该 56 文件快照。全仓库 pytest **97 passed**（本审查重跑）。

对照本轮清单：

| 项 | 本轮 |
|---|---|
| 双线性 \(\sigma(h^\top UV^\top e+b)\)，\(\lambda_{\mathrm{FN}}=10\) | 通过 |
| 未知 mask / 空 \(\mathcal K\) 为 NaN 不是 0 | **通过** |
| conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) | 通过 |
| `predict_set` \(1-p\le q\)（含 0.7/0.3） | **通过** |
| P1 留出 logistic，不是 `length+0.01*op` | **通过** |
| `precomputed` 是调用方分数 | **通过** |
| P2 共享分母一致性；None-safe | **asked 项通过**（整数 vs 列表；None → `missing_pair`） |
| P3 vs 对照 + nontarget | **通过（接口）** |
| \(\rho_S(T)=\) 事件均值不是并集 | **通过** |
| 空 `noise_set` 一律 null | **API 通过**；生产 0-hit 构造 **失败**（C4-M-01） |
| INLP 在投影 H 上；C-rand 匹配主范数 | 通过 |
| 4096≠3584 直接迁移 N/A | 通过 |
| labeled vs unlabeled 不同；labeled 要标签张量 | **通过 asked 项**（张量不进 \(W\)，C4-U-01） |
| `cone_fit` 真正拟合 | **通过** |
| Week-8 无发明门 | **默认通过** |

**可关闭（独立确认）：** C-01、C-02、C-03、C-04、C2-M-01、C2-M-02、C3-M-02、C2-M-03、C3-M-01、C2-M-05、C2-M-06、C3-M-03（asked）、C3-M-05（接口）、C3-M-07（API）、`cone_fit` 空壳。

仍会污染论文数字的 confirmed defects：**C4-M-01**（已评估 0-hit → excess null，手算应为 1）；**C4-M-02**（\(a(X)\) 0.9 vs 0.1）；**C4-M-03**（Boundary 报告损失 −10 vs 真 BCE 10）。

**验收意见：** `FAIL_MATH_STATS`。r03 指定的未知 BCE、默认/留出 P1、`1-p<=q` 边、并集 \(\rho_S(T)\)、空袋 hits 逃生、P2 崩溃/整数分母、C-rand/INLP、cone stub、4096 N/A **本轮不再是拦路缺陷**。在 C4-M-01 关闭并经独立复审前，不得把 `event_density_sets` / `cmd_label` 的 null excess 写成“噪声已扣”。在 C4-M-02 关闭前，不得把 CLI 校准写成命题 2 覆盖。在 C4-M-03 关闭前，不得把 Boundary `loss` 写成 BCE。

---

## 附录：56 文件 SHA-256（POSIX relpath，仅 file bytes）

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  18adcce069d4b50e4e77d92525335951f2feb57282bdaa194bda3b07f7103875
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  7c0f14a9dd90a87750872f90d5634736538c370d715252c48875b25e59079ee1
src/reasoning_diff/cli.py  c7b8061e036c9f83a84b13df01e96e73fc89e9f66b47bd3010349441f0f11c45
src/reasoning_diff/edits.py  0e8365ca08ea3db3fa9cb190ae14cf15975973a9345281a6a7002a6a91e04b77
src/reasoning_diff/events.py  c7f9c33ecb97d1d85b2e5d0c388fc62456c4a0b4d4ec711ddbd2759a1b23486e
src/reasoning_diff/executor.py  86b434ed3c8bbeadb95275b993004c4942d19278fda269473309821b73f2f128
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  b287249e03b493546e378175d4945e2d99bf129b1cc2ed0227db1f26dc7f13f9
src/reasoning_diff/models/__init__.py  0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8
src/reasoning_diff/models/adapters.py  c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a
src/reasoning_diff/models/collect.py  fcfb9be8a3e7a3e9650c72c5b0a8e1244491dc12e58b13f3bad080254c58dffe
src/reasoning_diff/models/features.py  0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0
src/reasoning_diff/models/generate.py  0ea73ab1e0da2dbe7f2d6270b939625e8eccc2619857ca1200209b53158c9812
src/reasoning_diff/models/tiny.py  21725a183452bd06593789217745202863269cd7e9dea1ec144e4bbdb0a1ddb0
src/reasoning_diff/probes/__init__.py  3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5
src/reasoning_diff/probes/bilinear.py  52de70553b37dec69822b790b006b7282e58ee926bb77006b3da40b419726e15
src/reasoning_diff/probes/boundary.py  7f9d62ab84f9452cd7c5a863b5d719aa162c4988b6e5d519efc4daca944d00cc
src/reasoning_diff/probes/calibrate.py  16609e8f7007aab433b2ea12f13587582676d0ab103742a842ed82a801c8c864
src/reasoning_diff/repair.py  9fa3ddbe26334273d4a0dfb92f3faf8fee788ed34a07f9523117c1b87e0b7290
src/reasoning_diff/rng.py  2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908
src/reasoning_diff/schema.py  b61ee242b0a5bcbc520c75ace00a9f23dd5b3012c0a4d4c55b68bd44c8291091
src/reasoning_diff/scoring.py  d05822c4fb784fe4a57d9f82f583eaa31c0f3b2e0e96c04b81f77db7413433f8
src/reasoning_diff/splits.py  2bc45ed0bbce3a5c8bcaa97aedf506ae5469e5db0d0fcba2ce0c23ac71ed2f1b
src/reasoning_diff/tasks/__init__.py  4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754
src/reasoning_diff/tasks/catalog.py  5d3918394b1603bb829ba0f23bbaae648a13d1a0cb98d66fd0221e3ad0201ae0
src/reasoning_diff/tasks/t1_config.py  e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94
src/reasoning_diff/tasks/t1_fixture.py  01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41
src/reasoning_diff/tasks/t1_official.py  5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b
src/reasoning_diff/tasks/t2_gsm_plus.py  606e4a09cfcbd8d9b3ab771d8648a10d0798f2ee937fb0818ae8d7a5ca1bfc78
src/reasoning_diff/tasks/t2_gsm_symbolic.py  067af473ddb143b7dc017cd3ab0ab92276edd8cfbd15ae5b33eff64ba7787751
src/reasoning_diff/tasks/t2_noop.py  9329d9b1e2e91dadfedde51687ccc1325f5560881cfc3c9c720424c71719110f
src/reasoning_diff/tasks/t3_hotpot.py  b86ca7dffd774606d4f0b9ad1f831d949b1a8434eb95bbbc5d14969e12e62f2b
src/reasoning_diff/tasks/t3_humaneval.py  398a8ab68104fb98170e75487d9b62625c9e26b194a9d6d0ba5e736deecc3468
src/reasoning_diff/tasks/t3_musique.py  9587aa9662b1c1d7f67b8adb8d82838e636ba51f2df8ed27f0e7bcc8d635e7a4
src/reasoning_diff/tasks/t4_boundary.py  aab4821f407c0f06d52d69abca581c1b067a1748327c67b2391a6978c0dbd2ba
src/reasoning_diff/transfer.py  c58e673a5bc9684169ad7275da295099386962ddc348f579838ac9bb86366af0
tests/conftest.py  1b4eac7fa8e43fdb2f7d486ec1ed7750ed665612eb15b156c90c0e23c7e447b1
tests/test_artifacts.py  830953f379954233c76c9aab9f5f4b3860ea598579015a58bddd9909c5bd3278
tests/test_cli_pipeline.py  0cedc6188e5f64b1ad6c97620c8c31ad18a6d8b48e6f511a930e0700f31c31a1
tests/test_generate_loop.py  ffe10b0d6812908ca34f446103b22a23c2e857a85172cc78e72caf005a979a46
tests/test_measure.py  fbc68abd89ed109edd84c352a3643cb454ff5e38262fe4f27becd7e786a452ab
tests/test_review_regressions.py  37414926677d059610794b4f64ec3bcbf7c242ecce9c563bc8e549abc5d3a60c
tests/test_round03_regressions.py  70475c77edce6844cad811c010f4ecb29aa764dc11b24ccb5d3de1dd14b09e51
tests/test_science.py  3180ca3217882de5324c9a5bcd2304a26cb8c03be10f990ed51c0b41dc5d250c
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```
