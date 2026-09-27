# Round-13 Channel A — Paper consistency

- **Agent:** Cursor Grok 4.6 (independent channel A subagent). No parent-assigned reviewer id.
- **Time:** 2026-09-21 (Asia/Shanghai).
- **Scope:** Paper + protocol + Goal §5 + REQUIREMENTS + all `src/reasoning_diff/**/*.py`. Production code, tests, and `pyproject.toml` were not modified. Other round-13 A–F reports were not read. Prior-round A–F files were not used as evidence. `.planning/audits/ISSUES.md` was not treated as closed.
- **Declared freeze:** `.planning/audits/round-13/VERSION.md`
- **Declared hash:** `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b` (61 files)
- **Recomputed hash:** `0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b` (61 files)
- **Hash verdict:** **HASH_MATCH**
- **Paper file:** `Reasoning-Diff-修订方案-v3 (1).md`
- **Paper SHA-256:** `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C` (match; 517 lines)

## 1. Hash reproduction

Ran VERSION.md script exactly (POSIX relpath + NUL + bytes over `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`):

```
n_files 61
hash 0816fa5ba35cc8cef9537c69908f3b2f3483545b5ea3697fdbf72785f293de3b
```

git_head in VERSION.md (`46a6e26…`) was not used as the freeze identity. Working tree is dirty; the content hash is the freeze.

## 2. File coverage

Read in full: paper (517 lines), `docs/EXPERIMENT_PROTOCOL.md`, `docs/CURSOR_GOAL_PROMPT.md` §5 (and surrounding sections as context), `.planning/REQUIREMENTS.md`, every production `.py` under `src/reasoning_diff/`. Tests were executed, not accepted as paper-correct. Fixtures used only as repro inputs.

| path | lines | digest | what was read |
|---|---|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 517 | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C` | full paper |
| `docs/EXPERIMENT_PROTOCOL.md` | 86 | (not in freeze hash) | full protocol |
| `docs/CURSOR_GOAL_PROMPT.md` | 166 | (not in freeze hash) | §5 required; rest for context |
| `.planning/REQUIREMENTS.md` | 76 | (not in freeze hash) | full; author status only |
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb` | full |
| `src/reasoning_diff/__main__.py` | 4 | `307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7` | full |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | full; P1/P2/P3, week8, cone, retrieval |
| `src/reasoning_diff/artifacts.py` | 85 | `524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332` | full |
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc` | full |
| `src/reasoning_diff/cli.py` | 1254 | `175abf12f4c207c551c6f5c5910b002d62f7f9125f41226389d0acbde4083c17` | full; prepare/collect/label/fit/analyze, E-order, donor pairing |
| `src/reasoning_diff/edits.py` | 287 | `cacb63ac27cbcccfa502335c5ffbd826d48b63158f688658d1c07464afe54fcf` | full; `make_source_value_pair` |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | full |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5` | full |
| `src/reasoning_diff/measure.py` | 392 | `b15fb8a5bb92220f5693b01acf6b60bd6640b57449e6419cb0e7b2bc6e4b6ba6` | full; labels, S/M, sham, TO/CSP |
| `src/reasoning_diff/models/__init__.py` | 1 | `0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8` | full |
| `src/reasoning_diff/models/adapters.py` | 42 | `c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a` | full |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38` | full; H/E, three positions |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0` | full |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6bf0ac1c3dab599db32d9d38c8583ebbd3009df52840e49844` | full; teacher-force |
| `src/reasoning_diff/models/tiny.py` | 120 | `21725a183452bd06593789217745202863269cd7e9dea1ec144e4bbdb0a1ddb0` | full |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332` | full |
| `src/reasoning_diff/probes/__init__.py` | 3 | `3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5` | full |
| `src/reasoning_diff/probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | full |
| `src/reasoning_diff/probes/boundary.py` | 44 | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | full |
| `src/reasoning_diff/probes/calibrate.py` | 45 | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | full |
| `src/reasoning_diff/repair.py` | 232 | `f76ff9998b9a6b1716c0136239fb8ca6cd4e15c17b18a1debaeff6483cf6409b` | full |
| `src/reasoning_diff/rng.py` | 53 | `2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908` | full |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full; persist locks |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3b40143968112166fd82913675037093c6b95e0676268b754` | full |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b32f80be9096f26ee6fbfd9173246706c11bacb49d5c295d5` | full |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d9e904a65a2bd23f04df20570f190feb1c26d47fb6fa5cf94` | full |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3cee0e92aafa9c5979a14c0c5d6752f165c95e9c847f08b41` | full |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f7369690318eef0f7530151b162b061949486311eb86c27ec5b17a0e1b` | full |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6ff5980677ebfb6c66a315ebd4a35693eaf474d529e57a0153` | full |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb303542786f4125c5892d9a9c16efdf50d0c7ac8cc12d04ec35276` | full |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d561494d95368fcfbb313bb0fad9e1832ea36ef69c14f9ae8f3eed` | full |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb2837a1cc080bcea90cedfde274246117d16976f49afdf7fe` | full |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc712f5bafeb68ed1a6ff9c7960aa59c103ec7fa4001a8561b1` | full |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0523b36e2771750696f3362d191cdb797a9b49ba805a51895` | full |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f886da1fd049c324cdd9b3ac60033357eed1622fd373f893de2` | full |
| `src/reasoning_diff/transfer.py` | 86 | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | full |

Per-file SHA-256 values are from a direct `hashlib.sha256(path.read_bytes())` pass over this freeze tree.

Fixtures inspected (not in the freeze hash): `tests/fixtures/t1_tiny.json` (`source_kind=fixture`), `t2_gsmplus_one.json` (`original_id=gsm8k-12`), `t2_symbolic_one.json` (`original_id=gsm8k-12`), `t2_formula_sidecar.json`.

## 3. Checks run

| check | command / method | result | paper-correct? |
|---|---|---|---|
| Freeze hash | VERSION.md Python | 61 files, `0816fa5b…`, HASH_MATCH | n/a |
| Paper SHA | SHA-256 of paper bytes | `F3C0EC08…` match | n/a |
| Unit/regression | `python -m pytest -q --tb=line` | **156 passed**, 20.20s, exit 0 | **No.** Green ≠ paper-correct. |
| Scientific prepare | `reasoning_diff prepare --eval-mode scientific --fixture tests/fixtures/t1_tiny.json --sham-opportunities 1 --split-fractions 0.40 0.15 0.10 0.10 0.10 0.15 --weight-seed 0` | exit 0 | Inspected; see findings |
| Scientific collect | `collect --eval-mode scientific --backend tiny` | exit 0; finite H `(7,32)`, E `(2,32)`, three position arrays | finite H yes; events are constrained-target |
| Scientific label | `label` on prepare dir | exit 0 | densities as below |
| Scientific fit | `fit --split probe_train` (prepare role was `probe_train`) | exit 0; task head loss finite; behavior `no_known_labels` | not paper CoT labels |
| Analyze without `p1_table` | `analyze --in-dir <prep>` | `p1 is null`; gates `unregistered`; `scientific_conclusion: null` | honest |
| `p1_incremental` no held-out | direct call | `status=requires_held_out` | honest; not fake P1 |
| A10-04 persist | Plus `gsm8k-1` then RAM-only clear; full clear; two-process | see §5 | persist works; isolated Symbolic `probe_train` expected |
| Official Plus-id list hunt | `src/**/*.json`, `*gsm8k*` under `src/` | **none** | isolated Symbolic without Plus may be `probe_train` |
| Booked-zero / sham: | direct `build_labels`+`event_density_sets`; fixture prepare + sham | no-change sham writes non-null excess from `N=[]` | defect |
| Source-value pair | `make_source_value_pair` + scientific `edits.jsonl` | rename `p2→p2_src`, values unchanged | defect |
| Teacher-force | scientific traces | `parse_status=constrained_target`, generated-region `q = ##` | honest; not §4.1 / MODEL-01 |

Not run (out of this machine / not required for the named hunts): real HF weights, official iGSM 500, GPU intervene/repair, server collect.

## 4. Paper-paragraph coverage (omissions vs swaps)

Empty “looks implemented” is not a pass. Below is the paper map. Background, related-work, schedule, and untested numeric forecasts are not code requirements.

| paper locus | requirement | this tree | status |
|---|---|---|---|
| §2.2 / §4.1 | Natural generate + identity align; fixture ≠ official | Fixture loader refuses `official`. Scientific generate is tiny + teacher-force `\nq = `, labeled `constrained_target`, `parse_region=generated`. | **non-defect** if not claimed as MODEL-01 / §4.1. See ND-01. |
| §2.3 | $R^{val}$ vs $R^{surf}$; structure separate | `surface_mentions` stored; structure via align `removed/merged` | present as schema; T1 scientific only emits target `q` |
| §2.4 / §6 / Goal §5.10 | Source–value decoupling: read $a$ vs $b$, first $a=b$ | `make_source_value_pair` is **rename-only** | **A13-01 confirmed** |
| §2.4 IE / swap | $H'=H_b+\Pi_Z(H_d-H_b)$; C-rand / C-layer | `apply_swap`, `c_rand_delta`, `c_layer_delta` exist | tools present; donor identity is wrong (A13-01) |
| §2.5 Prop 1–2, cone | over-approx protocol; conformal $\lceil(N+1)(1-\alpha)\rceil$ | `dirty_cone`, `conformal_threshold`, `joint_edit_counterexample` | formulas present; not evaluated on real traces |
| §2.6 / §3 | $S=B\setminus T$, $M=T\setminus B$; unknown ≠ negative; noise matched or null | unknown/unscanned enter $M$; sham: no-change books $N=\emptyset$ as evaluated | **A13-02, A13-03** |
| §3 TO/CSP | LCS TO; matched CSP; empty denom N/A | `preservation_to_csp`, `lcs_overlap` | present |
| §4.2 bilinear / MLP-256 | $h^\top UV^\top e+b$, $r=64$, $\lambda_{FN}=10$; Hidden=256 | `BilinearProbe`, `BoundaryMLP` | form present; CLI boundary fit is all-ones / no negatives (stub) |
| §5 Fig. 2 three positions | pre-step / pre-value / post-step | collect writes `H_pre_step`, `H_pre_value`, `H_post_step` | present on tiny |
| §7 T1–T4 | official iGSM + GSM-Symbolic/Plus + Hotpot/MuSiQue/HumanEval + T4 | adapters exist; graphs unknown/partial where required; no official Plus-id list | DATA-02 loaders present; **pending_server** for real dumps |
| §7 T2-noop | front/mid/back × surface; not official NoOp | `make_noop_pair`, `official_noop_release=False` | present |
| §8 / Goal §5.14 | Gate 0–2 unregistered ≠ pass | `week8_decision` → `unregistered`; `scientific_conclusion=None` | **non-defect** ND-02 |
| §8 eval-mode | no cone gate / verifier fallback | `RepairRecord` raises if gated | present |
| Goal §5.8 / §2.5 | P1 held-out length+op vs +ρ; no fake P1 | no `p1_table` → `p1 is None`; no held-out → `requires_held_out` | **non-defect** ND-03 |
| Goal §5.5 / DATA-03 | Plus test-only; family co-group | persist JSON + RAM; A10-04 new-process lock **holds** after Plus | **non-defect** ND-04; isolated Symbolic `probe_train` expected |
| MODEL-01 | frozen Qwen3 / R1-Distill HF | cards + `load_frozen`; local path is random tiny | **pending_server**; tiny ≠ MODEL-01 (ND-01) |
| §8 verbalizer four tiers | real model self-report | CLI `fit` uses `generate_fn=lambda p: prefix[:80]` | stub; not scored as a confirmed paper result path unless claimed as Fig. 5. **non-defect suggestion** NS-01 |
| Leftover first-seen E | E = task.premises, not labels.jsonl order | `_e_premise_ids` starts from `task.premises`, then **appends** leftover non-sham label ids | live scientific E is 2 premise rows; extra would be `j >= e.shape[0]` skip. **non-defect residue** ND-05 |

REQUIREMENTS checkboxes marked `implemented_*` are author claims, not this review’s verdict.

## 5. Named hunts (independent)

### 5.1 Teacher-force `\nq=` vs §4.1 CoT

Scientific prepare on `t1_tiny.json` produced 7 traces. Every one has `parse_status=constrained_target`, `parse_region=generated`, `weight_source=random_init`. Events are a single generated-region assignment such as `q = 82` / `q = 53` after teacher-forced `\nq = ` (`generate.append_target_assignment`, docstring: “Not gold values.”). `run_spec.source_kinds` is `{t1_tiny.json: fixture}`.

This is **honest `constrained_target`**. It is **not** MODEL-01 and **not** paper §4.1 natural CoT. Do not require inventing natural CoT. Do not allow anyone to file this path as §4.1 / C1 evidence.

### 5.2 Fixture as official

`load_t1_fixture` requires `source_kind=fixture`. `Task.validate` rejects `official` + `self_authored_arithmetic`. Scientific prepare recorded `source_kind=fixture`. **Not a swap.**

### 5.3 Gate unregistered as pass

`analyze` on the scientific prepare dir: all three gates `decision=unregistered`, `scientific_conclusion=None`, `skip_p2_p3=true`, week8 `status=not_evaluated`. Direct `week8_decision({...})` same. **Not a pass.**

### 5.4 Leftover first-seen E columns

`cli._e_premise_ids` (708–712) still appends first-seen leftover label premise ids after `task.premises`. Scientific collect E is `(2, 32)` = `{p1,p2}`. Fit with `tasks.jsonl` present maps by that order. Extra ids are appended, not used to reorder existing columns; `j >= e.shape[0]` skips them. Missing `tasks.jsonl` with labels raises. **No live first-seen remapping on the scientific path.** Residue only (ND-05).

### 5.5 Fake P1

`cmd_analyze` computes P1 only if `p1_table.jsonl` exists. Labels-only analyze → `p1: null`. `p1_incremental` without `held_out` and without `precomputed` → `requires_held_out`. **No fake P1.**

### 5.6 Booked-zero noise vs deducted N

See **A13-03**. Sham premise ids are `sham:<node>`. Sham **change** (scientific: `82` vs `53`) → `noise_set is None` → excess null (`noise_set_missing`). Sham **no-change** (fixture prepare, and direct labels) → `noise_set=[]`, `noise_evaluated=True` → `dependency_densities` treats empty $N$ as evaluated and writes `rho_M_noise=1.0`, `rho_M_excess=-0.5`. That is booked empty-$N$ deduction, not a matched premise support set. Protocol forbids assigning a no-edit stream change (or non-change) a real premise identity.

### 5.7 Rename-only source-value pair

See **A13-01**. Confirmed on both the function and scientific `edits.jsonl`.

### 5.8 Plus / Symbolic family persist (A10-04)

No official Plus-id list is shipped under `src/` (zero JSON, zero `gsm8k*` files).

Independent sequence (`gsm8k-1` hashes to `probe_train`; `gsm8k-12` hashes to `test` and **cannot** prove a lock):

1. `clear_test_only_families()`. Isolated Symbolic `original_id=gsm8k-1` → **`probe_train`**, `family_locked_test=False`. **Expected** (no Plus ever registered; no shipped list).
2. `load_gsm_plus` with `original_id=gsm8k-1` → writes RAM **and** `.planning/research/.cache/gsm_test_only_families.json`. Symbolic same family → **`test`**.
3. Clear **only** `_TEST_ONLY_FAMILY_KEYS`. Disk still `["gsm8k-1", "q:ada has 4 apples…"]`. Symbolic still **`test`**.
4. `clear_test_only_families()` (RAM + file). Isolated Symbolic again **`probe_train`**.
5. **New process A** only loads Plus. **New process B** only loads Symbolic (RAM empty). Disk has the keys. Process B: `split_for_task=test`, `assign_split("gsm8k-1")=probe_train`, `family_locked_test=True`.

A10-04 as “Plus lock is process-local RAM only” is **not** a defect on this freeze. Persist holds across processes. Isolated Symbolic with no Plus remains `probe_train` by design.

Note (operational, not a paper defect): pytest loads `t2_gsmplus_one.json` (`gsm8k-12`) after the lock-clearing test, so the cache file often still contains `gsm8k-12` after a green suite. That family already hashes to `test`.

## 6. Findings

### A13-01 — Rename-only pair claimed as source–value decoupling

| field | value |
|---|---|
| **ID** | A13-01 |
| **Severity** | high |
| **Status** | confirmed defect |
| **File / symbol / line** | `src/reasoning_diff/edits.py` `make_source_value_pair` 214–226; `apply_source_value_edit` 229–233 (`source_value_decoupled=True`); `src/reasoning_diff/cli.py` `_try_source_value_pair` 676–688; prepare write `kind=source_value_pair` 384–397; `_pair_source_value` 816–819 uses donor `same_source_diff_value` (the **value** edit), not the rename |
| **Trigger** | any T1-style task with a non-placeholder premise (`t1_tiny` scientific prepare; direct `make_source_value_pair(task, "p2", "2")`) |
| **Paper req** | Paper §2.4 (ll. 96–108), §6 (ll. 304–307), Goal §5.10, CAUSAL-02: construct pairs whose **required sources** differ while the target **value** is first equal ($a=b$, read $a$ vs read $b$), then same-source different-value. Rename of one premise is not a second source. |
| **Repro** | Scientific prepare wrote `same_value_diff_source.task` premises `[p1=4, p2_src=0]`, node `q` parents `[p1, p2_src]`, expression `p1 * p2_src`, value `0` (same as base). `same_source_diff_value` is the real value edit `p2:0→2`, `q=8`. Trace `trace-source` text is `p2_src = 0` / `q = p1 * p2_src` with the same teacher-forced `q = 82` as base. Direct call: `kind_src=same_value_diff_source`, values still `['4','0']`, answer still `0`. |
| **Impact** | C2 “source–value decoupled donors” are a rename of the same leaf plus a numeric edit. Event identity of `q` does not change. Intervene pairing prefers the **value-edit** hidden row as donor (`donor_tid=same_source_diff_value`). A paper source-follow matrix cannot be built from this object. Metadata `source_value_decoupled=True` is a concept swap. |
| **Fix** | Build two graphs that actually require different parents for the target with $a=b$ (and a second pair with values unequal). Stop labeling `apply_rename_edit` as `same_value_diff_source`. Point `_pair_source_value` at a true source donor, or refuse the pair. |

### A13-02 — Unknown / unscanned premises counted as $M$ (漏读)

| field | value |
|---|---|
| **ID** | A13-02 |
| **Severity** | high |
| **Status** | confirmed defect |
| **File / symbol / line** | `src/reasoning_diff/measure.py` `event_density_sets` 354–356 (`behavior_set` = `{premise: behavior_label==1}` only); `build_labels` 48–53 (non-exhaustive `no_change` → `behavior=None`); scientific prepare `_observations` / `_allowed_edits` never set `exhaustive=True` (`cli.py` 229–254, 216–226) |
| **Trigger** | scientific prepare on `t1_tiny` (teacher-force same seed ⇒ edit traces also `q=82` ⇒ `no_change` + not exhaustive); or any label set with `behavior_label is None` |
| **Paper req** | Goal §5.3: 未知不作负标签. Paper §2.2 / §4.1: “未观察到变化” ≠ “已覆盖全部允许扰动且没有变化”. Paper §2.6 $M=R_{\mathrm{task}}\setminus R_{\mathrm{behavior}}$ is empirical **known** miss, and finite-scan $M$ is not “never read” (protocol §2.4). Unscanned columns are not $M$. |
| **Repro** | Scientific labels: `q/p1` and `q/p2` have `behavior_label=None`, `behavior_known=False`. Densities: `M=["p1","p2"]`, `rho_M_raw=1.0`. Direct `build_labels` with a single non-exhaustive `no_change` on `p2` → `rho_M_raw=1.0`, $M=\{p1,p2\}$. Fit behavior head: `no_known_labels` (consistent with unknown) while prepare still **writes** $\rho_M=1$. |
| **Impact** | C3 “漏读密度” is 1.0 whenever behavior is unknown. That is a negative-like claim from missing labels. Week-8 must not treat `rho_M_raw` as a measured miss rate. |
| **Fix** | Build $B$ and $M$ only from `behavior_known` rows. If no known behavior on the event, `rho_M_* = null` with `null_reason=behavior_unknown`. Unscanned premises stay out of $M$. |

### A13-03 — `sham:` prefix never maps to premises; no-change books empty $N$ as deducted noise

| field | value |
|---|---|
| **ID** | A13-03 |
| **Severity** | high |
| **Status** | confirmed defect |
| **File / symbol / line** | `cli.py` prepare sham `premise_id=f"sham:{node}"` 312–329 / 343–360; `measure.build_labels` 68–80 (`noise_ref` only on `sham:` ids); `event_density_sets` 328–349 (sham hits → `noise_set=None`; **else** `noise_set=[]`, `evaluated=True`); `dependency_densities` 138–144 (empty evaluated $N$ ⇒ $\rho_M^{\mathrm{noise}}=\|T\|/\|T\|=1$, excess = raw−1) |
| **Trigger** | `--sham-opportunities > 0`. Scientific tiny (this seed): sham **changed** `82→53` → excess **null** (`noise_set_missing`). Fixture prepare (identical text): sham **no_change** → `noise_ref=0.0` on `sham:q` → booked $N=\emptyset$. |
| **Paper req** | Paper §2.6 / §3 / §12: all $\rho$ after a **matched** same-problem different-stream noise referent; empty denom or missing protocol → N/A. Protocol §2.6: 不能给一个无编辑随机变化强加具体前提身份; unregistered pairing ⇒ corrected **null**. Goal §5.4: noise referent must be a matched opportunity and common support. |
| **Repro** | 1) Scientific prepare: sham obs `premise=sham:q`, `outcome=changed`, `raw=['82','53']`; label `sham:q` `noise_ref=1.0`; densities `null_reason=noise_set_missing`, all excess null. Honest for the change fork. 2) Fixture prepare + sham: label `q/p2` beh=1, `q/sham:q` `noise_ref=0.0`; densities `null_reason=None`, `rho_M_noise=1.0`, `rho_M_excess=-0.5`. 3) Direct labels with sham `no_change` reproduce the same booked excess. Prepare even notes “sham hits are not mapped onto real premises” while still writing deducted $M$ on the no-change fork. |
| **Impact** | There is no premise-level noise support. The change fork nulls (correct). The no-change fork **deducts** as if $N=\emptyset$ were an evaluated common support: $\rho_M$ is shifted by a full 1.0. That is booked-zero/$N=\emptyset$ noise, not paper $\rho^{\mathrm{noise}}$. If a later seed’s teacher-force digits match, scientific mode takes this fork too. |
| **Fix** | Keep excess **null** whenever the only noise rows are `sham:`-prefixed (change or not). Do not set `noise_evaluated=True` on empty $N$ unless each real premise has a mapped no-edit opportunity. Do not attach a real `premise_id` to a no-edit stream. |

### Non-defects and doubts

**ND-01 (non-defect).** Teacher-forced `\nq=` is labeled `constrained_target`. Not §4.1, not MODEL-01. Tiny random weights. REQUIREMENTS’ `MODEL-01 implemented_local_tiny` is an author claim, not a paper result.

**ND-02 (non-defect).** Gate 0–2 stay `unregistered`. No pass/fail.

**ND-03 (non-defect).** P1 is not inferred from labels. Held-out is required.

**ND-04 (non-defect).** Plus family lock persists to `.planning/research/.cache/gsm_test_only_families.json`. RAM-only clear still locks Symbolic via disk. A later process that only loads Symbolic stays `test` after a prior process registered Plus. Isolated Symbolic with no Plus ever registered stays `probe_train`. No shipped official Plus-id list. Fixture `gsm8k-12` hashing to `test` is not evidence of the lock.

**ND-05 (non-defect residue).** `_e_premise_ids` still appends leftover label ids. Live scientific E follows `task.premises`. Not a first-seen column swap on the path that has `tasks.jsonl`.

**NS-01 (non-defect suggestion).** CLI `fit` verbalizer `generate_fn` echoes the trace prefix. Do not write Fig. 5 / §8 from that blob. Boundary MLP note `event-rows-only_no_negatives` is equally a stub.

**pending_server.** Official iGSM 500 / real GSM-Plus+Symbolic dumps / frozen Qwen3-8B and R1-Distill-Qwen-7B / GPU swap-ablate-rescue / real P1–P3. Missing **code** is not hiding in this list: adapters, tiny hooks, and CLI stages exist. Missing **weights/data** are external.

## 7. Scientific pipeline snapshot (`t1_tiny`, weight_seed=0)

- Traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value edits, `trace-sham`.
- Split: `fix-t1-001` → `probe_train` (hash of this fixture family; not official).
- Events: one generated-region `q = ##` each; `in_generated=True`.
- H: finite `(7,32)`; E finite `(2,32)`; `H_pre_step` / `H_pre_value` / `H_post_step` present; layer 1 (3-layer tiny 60–75% band).
- Sham: `sham:q`, changed `82` vs `53`.
- Densities: `rho_S_raw=null` (empty $P\setminus T$), `rho_M_raw=1.0`, excess null.
- Fit: task head trained; behavior head `no_known_labels`.
- Analyze: `p1=p2=p3=null`, gates unregistered.

## 8. Verdict

**FAIL**

Confirmed in-scope paper defects: **A13-01** (rename-only “source–value” pair), **A13-02** (unknown counted as $M$), **A13-03** (sham: no-change books empty $N$ as deducted noise). Hash matches. Pytest 156 passed is not paper-correct. Teacher-force, fixture marking, unregistered gates, refused fake P1, leftover-E residue, and Plus persist (including new-process) are not defects on this freeze.

This channel does **not** declare Goal complete. `consecutive_pass_count` cannot start from this report.
