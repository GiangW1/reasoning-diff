# C：数学与统计独立审查（round-09）

- 通道：C（math and statistics）
- 任务标识：Independent reviewer C；独立重推导 conformal \(k\)、P1 问题级 bootstrap \(\Delta\mathrm{AUC}\)（禁止 \([\delta]*n\)）、有符号 excess、C6-M-01 \(E\) 列身份。必须在**当前字节**上独立攻击：labels 首次出现序 \([p3,p2,p1]\) vs \(E=[p1,p2,p3]\)，\(\hat p=(0.9,0.1,0.8)\)，\(R=\{p1\}\) 必须得 \(a=0.1\) 不得 \(0.2\)；仅含 p2 的 labels 仍须索引 \(E\) 第 1 列。手算微例。Gate 未注册不是缺陷。不发明 Gate 阈值。
- 审查时间：2026-09-21
- 审查者上下文：独立 subagent。只读生产代码。未读 round-09 的 A/B/D/E/F。`round-08/C-math.md` 与 `round-06/C-math.md` 仅作猎单与体例，**结论全部由本轮对磁盘字节的公式推导与数值反例重做**，不沿用上一轮状态，不采信 ISSUES 的作者 `local close` / `fixed_pending_review`
- 声明冻结哈希：`9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`（`.planning/audits/round-09/VERSION.md`，60 文件、POSIX relpath + `0x00` + bytes）
- 本审查是否复现该汇总哈希：**开审是 / HASH_MATCH；交卷前否 / HASH_MISMATCH**（见 §1）
- git HEAD：`46a6e26da8637fe29d9f8f0667cb4e513538a59d`（工作区脏；`src/`、`tests/`、`pyproject.toml` 仍为未跟踪）
- 生产代码：本审查只读，未修改（只写本文件）
- numpy：1.26.4；CPython 3.11.7（Anaconda）

---

## 1. 冻结哈希

范围内文件数（开审）：**60**（`src/reasoning_diff/**/*.py` 42 + `tests/**/*.py` 17 + `pyproject.toml` 1；排除 `__pycache__`）。与 VERSION「60 files」一致。抽查核心公式文件均为 LF、`crlf=0`。

按 VERSION 给出的脚本逐字复算（开审第一动作）：

```text
path.as_posix().encode("utf-8") || b"\x00" || file_bytes
src 下 rglob *.py 排序 + tests 下 rglob *.py 排序 + pyproject.toml
```

| 时刻 | 文件数 | SHA-256 | 与声明值 |
|---|---|---|---|
| 开审（独立执行 VERSION 脚本） | 60 | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20` | **HASH_MATCH** |
| 第一轮公式攻击结束（同一脚本，连续两次） | 60 | `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20` | **当时仍 MATCH** |
| 手检中途（measure/cli/transfer 已被外部改写） | 60 | `57b43360c354ede2caf4a99adae7a0b33c082ec534f675b295709890931427bd` | **HASH_MISMATCH** |
| 二次攻击（出现 `tests/test_round07_regressions.py`） | 61 | `fea2565f59e248e5aaa8787bd6776fe603238fb9e5fc65327bc8ce99bf2d7a5f` | **HASH_MISMATCH** |
| 交卷前最后一读 | 61 | `c29ad0dd4a1f5fd161fb3459433d7af4f5f9dd987d0120f800f0c545c106d124` | **HASH_MISMATCH** |
| 本报告落盘后再算 | 61 | `813081243b89687be06260e1516c34f9d54b0217ca3f771fab9240b18f5a4b6d` | **HASH_MISMATCH**（仅 `tests/test_round07_regressions.py` 又被外部改写；`cli.py`/`measure.py`/`analysis.py`/`calibrate.py` 未再变） |

本通道未改 `src/`、`tests/`、`pyproject.toml`。工作区在审查进行中被其他进程改写：`measure.py`、`cli.py`、`transfer.py` 与多份测试在开审 MATCH 之后被替换，随后又新增第 18 个测试文件。**不得把声明冻结 `9ffc4cd9…` 标为已复核通过。**

公式库中**全程未漂**的 digest（开审至交卷前最后一读一致）：

| 文件 | SHA-256（全程绑定） |
|---|---|
| `analysis.py` | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` |
| `probes/calibrate.py` | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` |
| `probes/bilinear.py` | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` |
| `probes/boundary.py` | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` |
| `interventions.py` | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` |

中途被外部改写、交卷前最后一读：

| 文件 | 开审（声明冻结） | 交卷前最后一读 |
|---|---|---|
| `cli.py` | `a33cf79079089e1dc7d1af4d74ec1734e61ff6b30a23339673429ad5d39fda77` | `ba474e1fea1f7c5ab3488c90b32c776862d3651f281be38a543522e9ebeb5e98` |
| `measure.py` | `1fa2360e680d37ad086c9a81b3ec684c9d9d1e73affb0d906ff5a97231986df2` | `c81e2402671228b6ac8b42437b9d48b2ef1834f41b82275c2975114dab1063d6` |
| `transfer.py` | `d31bcd499a51ca94c28dca6c97cdbd5c5e3f05db996d15934e5b7d0b5bb22407` | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` |

C6-M-01 / conformal / P1 的**指定反例**在开审 MATCH 窗口与最后一读 `cli.py` 上各跑一遍，数值相同。`event_density_sets` 的 hit 记账只在后写的 `measure.py` 上变成扣除，**不是**声明冻结字节。

---

## 2. 范围与覆盖

| 文件 | 行（开审 / 最后） | SHA256 | 覆盖的符号 | 深度 |
|---|---|---|---|---|
| `src/reasoning_diff/probes/calibrate.py` | 1–45 / 同 | `e8b3ed34…` | `sequence_score`/`truth_indices`/`conformal_threshold`/`predict_set` | 全文；手算 \(k\) 9 组 |
| `src/reasoning_diff/analysis.py` | 1–337 / 同 | `e4368b0a…` | `_auc`/`_fit_scores`/`p1_incremental`/`_bootstrap_p1` | 全文；独立 IRLS 簇重算 \(\Delta\mathrm{AUC}\) |
| `src/reasoning_diff/measure.py` | 1–345 / 1–388 | 开审 `1fa2360e…`；最后 `c81e2402…` | `dependency_densities`/`event_density_sets` | 全文；signed excess + hit 记账两快照 |
| `src/reasoning_diff/cli.py` | 1–1241 / 1–1251 | 开审 `a33cf790…`；最后 `ba474e1f…` | `_e_premise_ids`/`cmd_fit`/`cmd_calibrate`/`cmd_analyze` | 实际 CLI 反例（两快照） |
| `src/reasoning_diff/probes/bilinear.py` | 1–101 / 同 | `b34ea3e5…` | `predict_matrix`（只为重建 \(\hat p\)） | 重建误差 |
| `src/reasoning_diff/transfer.py` | 1–75 / 1–86 | 开审 `d31bcd49…`；最后 `5549f84b…` | `direct_transfer(4096,3584)` | 直接调用 |
| `tests/test_round06_regressions.py` | — | 开审 `6c274aa6…` | C6-M-01 辅助函数 | 查测试能否锁 CLI |
| `tests/test_science.py` | — | `cdb5f146…` | conformal 规定例 | 查是否独立 |

调用链只读：`cli.cmd_fit` / `cmd_calibrate` / `cmd_analyze`。未覆盖：模型 hook/KV、数据适配器、executor。

---

## 3. 独立推导（先公式，后对代码）

原文 / 协议：REQUIREMENTS PROBE-01 / PROP2-01 / C3-01；PITFALLS 校准 / P1 / 有符号 excess 条。不发明 Gate 阈值。

### 3.1 Split conformal 与 \(a(X)\)

\[
a(X)=\max_{i,\ j\in R(s_i)}(1-\hat p_{ij}),\quad
k=\lceil(N+1)(1-\alpha)\rceil.
\]

空真集 \(a=0\)。\(1\le k\le N\Rightarrow q=s_{(k)}\)；\(k>N\Rightarrow +\infty\)。\(\alpha\notin[0,1)\) 拒绝。预测集 \(\hat R=\{j:1-\hat p_j\le q\}\)。\(j\) 是前提身份在 \(\hat p\) 列上的位置，必须与 \(E\) 行（`task.premises` 顺序）对齐，**不能**是 `labels.jsonl` 首次出现序。

规定反例：\(\hat p=(0.9,0.1,0.8)\)，\(E=(p1,p2,p3)\)，\(R=\{p1\}\) ⇒ \(a=1-0.9=0.1\)。若误用首次出现序 \([p3,p2,p1]\)，p1 下标 2，吃到 \(0.8\)，得 \(0.2\)。仅观察到 p2 时，p2 仍须是 \(E\) 列 1，\(a=1-0.1=0.9\)（旧 `unique=[p2]` 会吃列 0 得 \(0.1\)）。

### 3.2 P1 问题级 bootstrap

train 上 IRLS logistic（链长+op vs 链长+op+\(\rho\)），留出题上 Mann–Whitney AUC；平局 \(1/2\)。问题级簇 bootstrap：重采样基础题，**每次重算** \(\Delta\mathrm{AUC}\)。禁止把点估计复制 \(n\) 次得到 \([\delta,\delta]\)。假说不要求 \(\Delta\mathrm{AUC}>0\)。

### 3.3 有符号 excess

\[
S=B\setminus T,\quad
\rho_S=\frac{|S|}{|P\setminus T|},\quad
\mathrm{excess}=\mathrm{raw}-\mathrm{noise\_reference}.
\]

分母空 → N/A。缺 sham 协议 → excess null。已评估且 0-hit：\(N=\emptyset\)、noise \(=0\)、excess \(=\) raw。有 sham hit 时 \(N=\) 命中的真实前提，excess 做减法，**不是**改成 null。负差不截断。\(\rho_S(T)\) 是事件均值。

PITFALLS：raw \(=0.2\)、noise \(=0.3\) ⇒ excess \(=-0.1\)。

### 3.4 C6-M-01 列身份

`predict_matrix` 的列 \(j\) = `E` 行 \(j\) = `task.premises` 顺序。`truth_indices` 与 fit 的 \(Y\) 列必须是该序下的下标。labels 行序 \([p3,p2,p1]\) 不得改变列身份。

---

## 4. 已执行检查

| ID | 检查 | 方法 | 结果 |
|---|---|---|---|
| CHK-01 | \(k=\lceil(N+1)(1-\alpha)\rceil\) | 手算 9 组 vs `conformal_threshold` | **通过**。\(N=4,\alpha=0.4\) 且分数 \([0.1,0.2,0.3,0.4]\) ⇒ \(k=3,q=0.3\)；本审查默认袋 \([0,0.1,\ldots]\) 得 \(q=0.2\)（同一 \(k\)）。\(\alpha=0.1/0/0.05\) 且 \(k>N\) ⇒ \(+\infty\) |
| CHK-02 | \(\alpha\ge1\)、\(\alpha<0\)、空袋 | 直接调用 | **通过**（`invalid`） |
| CHK-03 | \(1-0.7\le 0.3\) | `predict_set([0.7], 0.3)` | **通过**：无 slack 为 False；`+1e-12` 后 True |
| CHK-04 | 库函数 \(a(X)\) | `[0.9,0.1,0.8]` | **通过**：`truth_indices=[0]` → \(0.1\)；无 indices + `one_minus_p` → \(0.9\)；空真集 → \(0\) |
| CHK-05 | **C6-M-01 规定反例 A（实际 `cmd_calibrate`）** | \(E=I_3\)；\(\hat p=\sigma(\mathrm{logit}(0.9,0.1,0.8))\)，最大重建误差 \(1.11\times10^{-16}\)；labels 行序 \([p3,p2,p1]\)；`Task.premises` \([p1,p2,p3]\)；`graph_kind=arithmetic_dag`；`ancestors(s1)=\{p1\}\) | **通过（两快照）**。`_e_premise_ids` → `[p1,p2,p3]`。开审 `cli.py a33cf790…` 与最后 `ba474e1f…` 的 CLI `scores=[0.1]`。旧首次出现序仍为 \(0.2\) |
| CHK-06 | **C6-M-01 仅 p2 labels（实际 CLI）** | 同上 pred；labels 只有 `{p2}`；事件 `s2`，祖先 \(\{p2\}\) | **通过（两快照）**：`index("p2")==1`；CLI `scores=[0.9]`。旧 `unique=[p2]` 吃列 0 得 \(0.1\) |
| CHK-07 | 两事件逐步 \(R(s_i)\) + 打乱 labels | \(\hat p_0=(0.9,0.1,0.8)\)、\(\hat p_1=(0.1,0.9,0.8)\)，\(R=\{p1\},\{p2\}\) | **通过**：CLI `scores=[0.1]`。旧并集仍为 \(0.9\) |
| CHK-08 | `cmd_fit` 的 \(Y\) 列身份 | 包装 `BilinearProbe.fit`；labels 行序 \([p3,p2,p1]\) | **通过（两快照）**：\(Y[0]=(1,0,0)\)，p1 在列 0 |
| CHK-09 | **P1 bootstrap 是否重算 \(\Delta\mathrm{AUC}\)** | \(n=40\)，`len≡10`，`op~N(0,1000)`（`rng(0)`），`rho=y`，`y` 交替，后 20 留出，`groups=i//2`，独立 IRLS 簇重算，同一 `rng(0)` | **通过**：代码区间 \([0.07372222222222223, 0.7262731481481484]\)，宽度 \(0.6525509259259261\)，`status=resampled_delta_auc`，\(n=200\)。独立同算法区间、均值 **逐位相同**。不是 \([\delta,\delta]\)（点估计 \(\delta=0.29\)） |
| CHK-10 | 仅传 `rng`、不传 `groups` | 同上 | **残留**：bootstrap 的是 \(\rho\) 均值 \(0.5\)，区间 \([0.35,0.625]\)，不是 \(\Delta\mathrm{AUC}\) |
| CHK-11 | 默认拒绝无留出；假说不要求正 AUC | 省略 `held_out`；\(\rho\sim N(0,1)\) | **通过**：`requires_held_out`；噪声 \(\delta=-0.13\) 仍 `estimate` |
| CHK-12 | 留出拟合不吃 eval \(X\)；常数 AUC；平局 | 只改 held-out 行的 `length` | **通过**：train 差 0；eval 变 \(0.106\)。常数 AUC \(0.5\)。分数 \([1,2,2,3]\) vs 标签 \([0,0,1,1]\) 手算 \(0.875\) |
| CHK-13 | signed excess 不截断；0-hit；空分母；事件均值 | `dependency_densities` | **通过**：\(P\) 15 / \(T\) 5 / \(S=\{p6,p7\}\) / \(N=\{p6,p7,p8\}\) ⇒ raw \(0.2\)、noise \(0.3\)、excess \(-0.1\)（浮点 \(-0.09999999999999998\)），不截断。0-hit ⇒ `noise=0`、`excess=raw`。空分母 ⇒ `rho_S` null。两事件 \(1/2\) 与 \(0\) ⇒ 均值 **0.25** |
| CHK-14 | **C7-M-01 hit 记账（声明冻结 `measure.py 1fa2360e…`）** | \(T=\{p1\}\)，\(B=\{p3\}\)，`noise_ref(p3)=1` | **失败（冻结快照）**：`event_density_sets` 得 `null_reason=noise_set_missing`，excess **null**。直接集合 API 得 excess \(0\) |
| CHK-15 | 同一反例（后写 `measure.py c81e2402…`） | 同上 | **后写树通过**：`real_hits` 写入 \(N\)，excess \(=0\)。这不是声明冻结字节 |
| CHK-16 | **C7-M-02 analyze 标签回退（声明冻结 `cli.py a33cf790…`）** | 6 行 task/behavior，全 `event_id=q` | **失败（冻结快照）**：\(\delta=0.25\)，bootstrap 区间 **\([0.25,0.25]\)**，`status=resampled_delta_auc`，`week8=evaluated_descriptive` |
| CHK-17 | 同一 CLI（后写 `cli.py ba474e1f…`） | 同上 | **后写树通过**：`p1 is None`，`week8=not_evaluated`。标签回退已删。不是声明冻结字节 |
| CHK-18 | 无 `tasks.jsonl` 回退首次出现序 | labels \([p3,p2,p1]\)，`node_id=p1` | **残留（两快照）**：CLI `scores=[0.2]` |
| CHK-19 | `direct_transfer(4096,3584)` | 直接调用 | **通过**（`not_applicable_dimension_mismatch`） |
| CHK-20 | Week-8 无发明门 | 默认 / 有阈无测 / 有阈有测 | **通过**：默认三门 `unregistered`。有阈无测 → `threshold_present_measurement_missing`。`rho_S_excess=0.1` vs \(0.9\) → `compared/below`。`scientific_conclusion is None` |
| CHK-21 | `pytest` | 开审冻结树；漂后树 | 开审全仓库 **144 passed**（作者声称成立）。漂后曾见 **153 passed, 1 failed**（`test_round07_regressions.py::test_event_density_maps_real_noise_hits`，`Premise span mismatch: p3`）；该测试名随后被外部改写。绿测**不能**单独证明公式 |

---

## 5. 未执行检查及原因

| 未做 | 原因 |
|---|---|
| 真实轨迹上的 \(a(X)\)、logistic P1 | 真实 HF 权重属 pending_server |
| 阅读其他 round-09 通道 | 任务禁止 |
| sklearn 对照 IRLS 系数 | 本机未依赖 sklearn；用独立同算法区间、污染 eval \(X\)、检出 \(\rho=y\) 代替 |
| 在声明冻结上重跑漂后新增的 r07 回归 | 该文件不在 60 文件冻结内，且审查中途仍被改写 |

---

## 6. 既有 ledger（独立确认，不采信作者 close）

| Ledger | 声明冻结 `9ffc4cd9…` | 交卷前最后一读 | 说明 |
|---|---|---|---|
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | **关闭** | 同（`calibrate.py` 未漂） | CHK-01/02 |
| C5-M-01 P1 bootstrap \([\delta]*n\) | **库函数关闭** | 同（`analysis.py` 未漂） | CHK-09。独立区间逐位相同 |
| C6-M-01 列身份 | **关闭（指定反例）** | **仍关**（后写 CLI 再跑得 \(0.1\)） | CHK-05/06/08 |
| signed excess 不截断；0-hit noise=0 | **集合 API 关闭** | 同 | CHK-13 |
| **C7-M-01** hit ⇒ excess null | **仍开** | 后写 `measure.py` 关上（非本冻结） | CHK-14/15 |
| **C7-M-02** analyze 标签冒充 P1，可 \([\delta,\delta]\) | **仍开**（本审查复现 \([0.25,0.25]\)） | 后写 `cli.py` 删回退（非本冻结） | CHK-16/17 |

---

## 7. 发现

### C9-H-01 — 声明冻结在审查中被外部改写，不得签通过

- **严重度：** High（过程 / 冻结完整性）
- **状态：** confirmed defect（本通道未改生产字节）
- **符号：** VERSION 脚本汇总哈希
- **事实：** 开审 `9ffc4cd9…`（60 文件）MATCH。第一轮攻击结束仍 MATCH。其后同一脚本依次得到 `57b43360…`（60）、`fea2565f…`（61）、`c29ad0dd…`（61）。漂移包含 `measure.py`（hit 记账）、`cli.py`（analyze 回退）、`transfer.py` 与新增 `tests/test_round07_regressions.py`
- **影响：** 不能把声明冻结当作已独立复核的论文数字基线。后写树上 C7-M-01/02 的“已关”**不能**记成对 `9ffc4cd9…` 的关闭
- **修复：** 停写生产树，重新冻结并开一轮新的独立 C

### C7-M-01 — 声明冻结上，有 sham hit 时 `event_density_sets` 丢掉 \(N\)

- **严重度：** High
- **状态：** confirmed defect **仅对声明冻结** `measure.py 1fa2360e…`（345 行，`elif hits: noise_set=None`）
- **反例（开审 MATCH 窗口，本审查执行）：**
  - \(P=\{p1,p2,p3\}\)，事件 `s1`，\(T=\{p1\}\)，\(B=\{p3\}\)，`noise_ref(p3)=1`
  - 论文 / 直接 `dependency_densities(..., noise_set=['p3'])`：raw \(0.5\)，noise \(0.5\)，excess \(0\)
  - 冻结 `event_density_sets`：`null_reason=noise_set_missing`，excess **null**
- 后写 `c81e2402…` 把 `real_hits` 写入 \(N\) 后同一反例 excess \(=0\)。那是另一份字节

### C7-M-02 — 声明冻结上，`cmd_analyze` 用前提级标签冒充 P1，区间可再变 \([\delta,\delta]\)

- **严重度：** High
- **状态：** confirmed defect **仅对声明冻结** `cli.py a33cf790…`（1052–1074 行标签回退）
- **反例（开审 MATCH 窗口，本审查执行）：**
  - 6 行 `task_label`/`behavior_label`，全 `event_id="q"`
  - `length≡1`，`op≡0`，`rho=behavior_label`，`y=task_label`，单一簇 `"q"`
  - \(\delta=0.25\)，bootstrap **\([0.25,0.25]\)**，`status=resampled_delta_auc`，`week8.status=evaluated_descriptive`
- 这直接违反本轮清单「禁止 \([\delta]*n\)」的**生产 analyze 路径**。库函数 `_bootstrap_p1` 本身在正确 `groups` 下是重算 \(\Delta\mathrm{AUC}\) 的
- 后写 `ba474e1f…` 删掉该回退，`p1 is None`。那是另一份字节

本轮**指定 C6-M-01 反例不是新的 confirmed defect**。

---

## 8. 未证实疑点

| ID | 严重度 | 内容 | 行 | 为何未升格 |
|---|---|---|---|---|
| C9-U-01 | Medium | 无 `tasks.jsonl` 时 `_e_premise_ids(None, labels)` 退回首次出现序。`node_id=p1` 时本审查两快照 CLI 均为 `scores=[0.2]` | 开审 `cli.py` 671–680；最后 707–716 | 指定 C6-M-01 以 \(E=[p1,p2,p3]\) 为前提。缺任务文件时应拒绝校准 |
| C9-U-02 | Low | 只传 `rng`、不传 `groups` 时仍 bootstrap \(\rho\) 均值 | `analysis.py` 87–88 | 正确 `p1_table` 路径传 `groups` |
| C9-U-03 | Low | `sequence_score` 默认 `nonconformity="prob"` 是 \(\max p\) | `calibrate.py` 24–26 | CLI 始终传 `one_minus_p` |
| C9-U-04 | Low | calibrate 仍 `task_label==1 or behavior_label==1`，且 `rsi` 含 `{nid}` | `cmd_calibrate` | 本轮主问列身份。任务/行为应分头校准 |

---

## 9. 外部待验证

| ID | 项目 | 原因 |
|---|---|---|
| C9-S-01 | 真实轨迹命题 2 覆盖 | 真实 HF 权重 pending_server；tiny 不是 MODEL-01 |
| C9-S-02 | 预注册后的 P1–P3 区间 | Gate 未注册（非缺陷）。声明冻结上 analyze 回退仍可写出伪 P1 |
| C9-S-03 | 4096↔3584 适配后的双线性 | 直接迁移 N/A 已对；共同维路径在审查中途被改写，未对声明冻结重做 PCA 对齐 |

---

## 10. 非缺陷 / 本轮独立核对通过

1. Conformal \(k\)；\(k>N\Rightarrow+\infty\)；\(\alpha\notin[0,1)\) 拒绝（`calibrate.py` 全程未漂）
2. `predict_set([0.7], 0.3)` 为 True；空真集 \(a=0\)
3. **C6-M-01 指定反例关闭（声明冻结 + 后写 CLI）：** labels \([p3,p2,p1]\) vs \(E=[p1,p2,p3]\) 得 CLI \(a=0.1\) 不是 \(0.2\)；仅 p2 索引列 1 得 \(0.9\)；fit \(Y[0]=(1,0,0)\)
4. 两事件逐步 \(R(s_i)\)，CLI \(a=0.1\)（并集仍关）
5. **库层 P1：** 簇重采样后重算 \(\Delta\mathrm{AUC}\)；独立 IRLS 区间逐位相同；宽度 \(0.65255\neq0\)
6. 默认 P1 拒绝无留出；假说不要求正 AUC（\(\delta=-0.13\)）
7. **集合 API signed excess** \(-0.1\) 不截断；0-hit ⇒ `noise=0`、`excess=raw`；事件均值 \(0.25\)
8. `direct_transfer(4096,3584)` N/A
9. Week-8 默认 `unregistered`（**不是缺陷**）；有阈无测 → `threshold_present_measurement_missing`。不发明阈值

---

## 11. 测试质量（仅公式）

作者声称 144 passed。本审查在**开审冻结树**上重跑全仓库：**144 passed**。其后树被改写，绿测数不再对应声明冻结。

- `test_truth_indices_follow_e_columns_not_label_order`：**半有效**。用 `SimpleNamespace` 锁 `_e_premise_ids` 与 `0.1` vs `0.2` 对照，以及 `only_last.index("p2")==1`。**不跑 `cmd_calibrate`**。本轮用真实 `Task` + 实际 CLI 关掉指定反例
- `test_p1_bootstrap_resamples_delta_auc` / `test_p1_bootstrap_interval_is_not_degenerate`：锁 `lo<hi`，**不对照独立 \(\Delta\mathrm{AUC}\) oracle**。本轮生产库路径已用独立 IRLS 对上逐位区间
- `test_sham_hits_do_not_book_evaluated_zero_noise`（r06）：**锁错公式**（hit ⇒ null）。与声明冻结上的 C7-M-01 同向，不能关闭本条
- 开审冻结**没有** CLI 列身份 oracle，也没有 analyze 回退 \([δ,δ]\) oracle
- 后写入的 `test_analyze_refuses_fake_p1_from_labels` / `test_c7_m01_mapped_noise_premise_is_deducted` 只约束后写树，**不能**回溯证明 `9ffc4cd9…`

---

## 12. 结论

开审冻结哈希 `9ffc4cd9…` **当时 HASH_MATCH**（60 文件）。交卷前同一脚本为 `c29ad0dd…`（61 文件）。**HASH_MISMATCH。** 本通道未改生产字节。作者 pytest 声称 144 passed：开审冻结树上 **144 passed** 成立；其后树不再是该声称。

对照本轮清单：

| 项 | 声明冻结 `9ffc4cd9…` | 交卷前最后一读 |
|---|---|---|
| conformal \(k\)；\(k>N\Rightarrow+\infty\) | **通过**（9 组手算） | 同（文件未漂） |
| P1 问题级 bootstrap 重算 \(\Delta\mathrm{AUC}\) | **库通过**（宽度 \(0.65255\)，独立区间逐位相同） | 同 |
| 生产 analyze 禁止 \([\delta]*n\) | **失败**（C7-M-02，\([0.25,0.25]\)） | 后写 CLI 不再回退 |
| signed excess 不截断 | **集合 API 通过**（\(-0.1\)） | 同 |
| 有 hit 时扣除 \(N\) | **失败**（C7-M-01，excess null） | 后写 `measure.py` 得 \(0\) |
| C6-M-01：\([p3,p2,p1]\) vs \(E=[p1,p2,p3]\) | **通过**。CLI \(a=0.1\) 不是 \(0.2\)；仅 p2 列 1；fit \(Y=(1,0,0)\) | **再跑仍通过** |
| Gate 未注册 | **不是缺陷** | 同 |

指定攻击（手算，不采信 ISSUES）：

- \(\hat p=\sigma(\mathrm{logit}(0.9,0.1,0.8))\)，\(E=I_3\) 对应 \((p1,p2,p3)\)
- labels 磁盘行序 \([p3,p2,p1]\)
- `Task.premises` 序 \([p1,p2,p3]\)，`ancestors(s1)=\{p1\}\)
- 论文：\(a=1-0.9=0.1\)
- 旧缺陷：首次出现序下 p1 下标 2，\(a=1-0.8=0.2\)
- **当前（及开审）`cmd_calibrate`：`scores=[0.1]`**
- 仅 `{p2}`：`index("p2")==1`；CLI \(a=0.9\)，不是列 0 的 \(0.1\)
- `cmd_fit` 截获 \(Y[0]=(1,0,0)\)

仍会污染**声明冻结**论文数字的 confirmed defects：**C9-H-01**（哈希已漂）；**C7-M-01**（冻结 `event_density_sets`）；**C7-M-02**（冻结 analyze 回退 \([0.25,0.25]\)）。C6-M-01 指定反例在冻结字节上关闭，但不能单独拯救冻结完整性。

**验收意见：** `FAIL_MATH_STATS`。不得为声明冻结 `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20` 签通过。C6-M-01 / conformal \(k\) / 库层 P1 bootstrap / 集合 API signed excess 已在开审 MATCH 窗口独立核对通过；生产 analyze 与 hit 记账在该窗口仍错。后写树上的“已修”必须重新冻结后再审。Gate 保持 `unregistered` 不是缺陷。

---

## 附录 A：开审 60 文件 SHA-256（声明冻结 MATCH 快照，仅 file bytes）

开审汇总哈希为声明值 `9ffc4cd93e2b14a2b2a18ce2608767a5e5f619e10a4e582740fd6eb8d1b3bf20`。

```
src/reasoning_diff/__init__.py  26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb
src/reasoning_diff/__main__.py  307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7
src/reasoning_diff/analysis.py  e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af
src/reasoning_diff/artifacts.py  524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332
src/reasoning_diff/baselines.py  3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc
src/reasoning_diff/cli.py  a33cf79079089e1dc7d1af4d74ec1734e61ff6b30a23339673429ad5d39fda77
src/reasoning_diff/edits.py  bfd1632b50504c042640bcda85368b0c695fd3f843ea885200d080055aa107b6
src/reasoning_diff/events.py  fc5031a51e99a4b511450d03ded6dd5f205175eb263bf4cbaf8695ee47746e17
src/reasoning_diff/executor.py  481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4
src/reasoning_diff/graphs.py  1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583
src/reasoning_diff/interventions.py  0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2
src/reasoning_diff/io.py  1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5
src/reasoning_diff/measure.py  1fa2360e680d37ad086c9a81b3ec684c9d9d1e73affb0d906ff5a97231986df2
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
tests/test_round06_regressions.py  6c274aa6d25a36f4509e659e3777b1f20d661237c9e32f5dc7cedda179585e74
tests/test_science.py  cdb5f1460502ba3cd5135f507762bb19c777e7462fe072d6979595cea3b33e36
tests/test_t1_official.py  f4b3cbc1fcd5371ec26def7ebe014f22b2c0e118371eece56275e329bfa1cb40
tests/test_t2_gsm.py  f66a95bb737dc973c6c653998640f30682338728f32be8e489feff4375ac2177
tests/test_t3_t4.py  d0381c097d04bc9d4567429e10f4ce4b2c965e79c41b23936a13c0516bef005c
tests/test_tiny_cache.py  83ae0441140f7e1791087bb87511d5c4ec75fdc19cb3ffa8696210ceb78ce47e
tests/test_tiny_hooks.py  e28e58b638568d8929398beffeab5eab5a728de8c43262ca074268d24a871d66
tests/test_tracer_t1_prepare.py  62a5e2f168a20e8f6b23c27003e12863fafc9df76d94a3e5fbf181bbd66d43ca
pyproject.toml  cb44851f7fbf7bf74613400f3e2d8ab1bab6523c78cb69c339f3103a6b2d3ae3
```

## 附录 B：交卷前最后一读 61 文件 SHA-256（HASH_MISMATCH，不得替代声明冻结）

落盘前汇总 `c29ad0dd…`；落盘后再算 `81308124…`（只变 `tests/test_round07_regressions.py` → `cad435ad…`）。公式结论对 `cli.py`/`measure.py` 绑定 `ba474e1f…` / `c81e2402…`；`analysis.py`/`calibrate.py` 仍为开审值。

```
src/reasoning_diff/cli.py  ba474e1fea1f7c5ab3488c90b32c776862d3651f281be38a543522e9ebeb5e98
src/reasoning_diff/measure.py  c81e2402671228b6ac8b42437b9d48b2ef1834f41b82275c2975114dab1063d6
src/reasoning_diff/transfer.py  5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2
src/reasoning_diff/edits.py  cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf
src/reasoning_diff/events.py  290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3
src/reasoning_diff/repair.py  f76ff9998b9a6b1716c0136239fb8ca6cd4e15c17b18a1debaeff6483cf6409b
src/reasoning_diff/splits.py  08f77e972927a9961885c09e0538f0c43d47ca6638944e1c80465cf6cc4af066
src/reasoning_diff/tasks/t2_gsm_plus.py  493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153
src/reasoning_diff/tasks/t2_gsm_symbolic.py  c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276
tests/test_round03_regressions.py  61247e8a074944a33933f5d6cba276745e191cbb22b13d13a8faf19af8d86b01
tests/test_round06_regressions.py  ac7e4e88248ff49edcd6f992cf48ff88409172c34ce7fa934ca288816fdf946c
tests/test_round07_regressions.py  e6f029be13a29de1719c16e4b217ecc87c69dddda77c8d241b0e13059ea5bedf
```

其余与附录 A 相同的文件 digest 见上表「全程未漂」行；此处只列相对开审冻结已变的路径。
