# Round-15 Channel A — Paper consistency

- **Agent:** Cursor Grok 4.6 (independent channel A subagent). No parent-assigned reviewer id.
- **Time:** 2026-09-21 (Asia/Shanghai).
- **Scope:** Paper + protocol + Goal §5 + REQUIREMENTS + all `src/reasoning_diff/**/*.py`. Production code, tests, and `pyproject.toml` were not modified. Other round-15 A–F reports were not read. Prior-round A–F files were not used as evidence of this tree. `.planning/audits/ISSUES.md` was treated as author claims only.
- **Declared freeze:** `.planning/audits/round-15/VERSION.md`
- **Declared hash:** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` (61 files)
- **Recomputed hash:** `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` (61 files)
- **Hash verdict:** **HASH_MATCH**
- **Paper file:** `Reasoning-Diff-修订方案-v3 (1).md`
- **Paper SHA-256:** `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C` (match; 517 lines)

## 1. Hash reproduction

Ran VERSION.md script exactly (POSIX relpath + NUL + bytes over `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`):

```
n_files 61
hash 401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716
```

git_head in VERSION.md (`46a6e26…`) was not used as the freeze identity. Working tree is dirty; the content hash is the freeze. Author note that r14 bound `1f61fd06…` is stale is accepted only as a versioning remark, not as evidence about this tree.

## 2. File coverage

Read in full: paper (517 lines), `docs/EXPERIMENT_PROTOCOL.md`, `docs/CURSOR_GOAL_PROMPT.md` §5 (and surrounding sections as context), `.planning/REQUIREMENTS.md`, every production `.py` under `src/reasoning_diff/`. Tests were executed, not accepted as paper-correct. Fixtures and a reviewer scratch dir were used only as repro inputs.

| path | lines | digest | what was read |
|---|---|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 517 | `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C` | full paper |
| `docs/EXPERIMENT_PROTOCOL.md` | 86 | `83a9142dba4f7fcd337a70ef8cd1a847ed7eb7ff110f2d77f466387ab491391d` | full protocol |
| `docs/CURSOR_GOAL_PROMPT.md` | 166 | `b9e0a8ea3fc87bf00f1949bd8201407e097ef3e25660173275ba11e42a39eb7e` | §5 required; rest for context |
| `.planning/REQUIREMENTS.md` | 76 | `39cf907c0b66b9b26ae7355e394848cfa1ff41ce5166310e1dc0a9307f9ac498` | full; author status only |
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb` | full |
| `src/reasoning_diff/__main__.py` | 4 | `307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7` | full |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | full; P1/P2/P3, week8, cone, retrieval |
| `src/reasoning_diff/artifacts.py` | 85 | `524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332` | full |
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc` | full |
| `src/reasoning_diff/cli.py` | 1252 | `c1a274e233988aad3c3390041cd40ad5e214ade82ba7579a3c7c8fc35156a71a` | full; prepare/collect/label/fit/analyze, E-order, donor pairing |
| `src/reasoning_diff/edits.py` | 362 | `250055ab8257ea2e24be885a389713e0c6d71c93936b44794a1ec821cf9e39db` | full; `apply_alt_source_same_value`, `make_source_value_pair` |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | full |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5` | full |
| `src/reasoning_diff/measure.py` | 408 | `8ec8cf09db1490978f5eacd7d90fd578cfe807bb2c6e09e2d002ae62ab83002c` | full; labels, S/M, sham, TO/CSP |
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

Fixtures inspected (not in the freeze hash): `tests/fixtures/t1_tiny.json` (`source_kind=fixture`).

## 3. Checks run

| check | command / method | result | paper-correct? |
|---|---|---|---|
| Freeze hash | VERSION.md Python | 61 files, `401e509b…`, HASH_MATCH | n/a |
| Paper SHA | SHA-256 of paper bytes | `F3C0EC08…` match | n/a |
| Unit/regression | `python -m pytest -q --tb=line` | **159 passed**, 24.43s, exit 0 | **No.** Green ≠ paper-correct. Suite encodes the rename graph as success. |
| Direct source pair | `make_source_value_pair` + `apply_rename_edit` on `t1_tiny` | parents/expr of “alt source” = rename of the same leaf | **defect** A13-01 |
| Unknown / unscanned M | `build_labels` + `event_density_sets` | `behavior_unknown=True`, `M=[]`, `rho_M_raw=None` | **not the named A13-02 on this tree** |
| Sham no-change N | direct labels + fixture prepare + scientific prepare | sham rows → `noise_set=None`; excess null | **not the named A13-03 on this tree** |
| Ancestor WRONG-TASK E | isolated feat/labs; WRONG-TASK planted in ancestor `col/` | `_find_tasks_jsonl` None; fit raises `tasks.jsonl` | **not the named A12-03 on this tree** |
| Scientific prepare | `prepare --eval-mode scientific --fixture t1_tiny.json --sham-opportunities 1 --split-fractions 0.40 0.15 0.10 0.10 0.10 0.15 --weight-seed 0` | exit 0; 7 traces; all `constrained_target` | honest teacher-force; pair object still rename |
| Scientific collect | `collect --eval-mode scientific --backend tiny` | H `(7,32)`, E `(2,32)`, three position arrays, all finite | finite H yes; events are constrained-target |
| Scientific label | `label` on prepare dir | exit 0; `rho_M_raw=null` | unknown not booked as M |
| Scientific fit | `fit --split probe_train` | task head loss finite; behavior `no_known_labels` | not paper CoT labels |
| Analyze | `analyze --in-dir <sci_prep>` | `p1=p2=p3=null`; gates `unregistered`; `scientific_conclusion=None` | honest |
| `p1_incremental` no held-out | direct call | `status=requires_held_out` | honest; not fake P1 |
| Intervene donor | collect sibling named `prep`/`col` | `donor_kind=same_value_diff_source`, rows `[0,3]` = `trace-source` | prefers source **object**, but that object is still a rename |
| Official Plus-id list | `src/**/*.json`, `gsm8k` under `src/` | none (only family-key parsing) | isolated Symbolic without Plus may be `probe_train` |

Not run (out of this machine / not required for the named hunts): real HF weights, official iGSM 500, GPU intervene/repair, server collect, full Plus persist two-process lock.

## 4. Paper-paragraph coverage (omissions vs swaps)

Empty “looks implemented” is not a pass. Below is the paper map. Background, related-work, schedule, and untested numeric forecasts are not code requirements.

| paper locus | requirement | this tree | status |
|---|---|---|---|
| §2.2 / §4.1 | Natural generate + identity align; fixture ≠ official | Fixture loader refuses `official`. Scientific generate is tiny + teacher-force `\nq = `, labeled `constrained_target`, `parse_region=generated`. | **non-defect** if not claimed as MODEL-01 / §4.1. See ND-01. |
| §2.3 | $R^{val}$ vs $R^{surf}$; structure separate | `surface_mentions` stored; structure via align `removed/merged` | present as schema; T1 scientific only emits target `q` |
| §2.4 / §6 / Goal §5.10 | Source–value decoupling: read $a$ vs $b$, first $a=b$ | `apply_alt_source_same_value` is an ID rewrite of the same product leaf | **A13-01 confirmed** |
| §2.4 IE / swap | $H'=H_b+\Pi_Z(H_d-H_b)$; C-rand / C-layer | `apply_swap`, `c_rand_delta`, `c_layer_delta` exist | tools present; donor identity is a rename graph (A13-01) |
| §2.5 Prop 1–2, cone | over-approx protocol; conformal ceil((N+1)(1-α)) | `dirty_cone`, `conformal_threshold`, `joint_edit_counterexample` | formulas present; not evaluated on real traces |
| §2.6 / §3 | $S=B\setminus T$, $M=T\setminus B$; unknown ≠ negative; noise matched or null | unknown/unscanned → `behavior_unknown`, `rho_M_raw=null`; sham rows → excess null | **A13-02, A13-03 not reproduced** |
| §3 TO/CSP | LCS TO; matched CSP; empty denom N/A | `preservation_to_csp`, `lcs_overlap` | present |
| §4.2 bilinear / MLP-256 | $h^\top UV^\top e+b$, $r=64$, $\lambda_{FN}=10$; Hidden=256 | `BilinearProbe`, `BoundaryMLP` | form present; CLI boundary fit is all-ones / no negatives (stub) |
| §5 Fig. 2 three positions | pre-step / pre-value / post-step | collect writes `H_pre_step`, `H_pre_value`, `H_post_step` | present on tiny |
| §7 T1–T4 | official iGSM + GSM-Symbolic/Plus + Hotpot/MuSiQue/HumanEval + T4 | adapters exist; graphs unknown/partial where required; no official Plus-id list | DATA-02 loaders present; **pending_server** for real dumps |
| §7 T2-noop | front/mid/back × surface; not official NoOp | `make_noop_pair`, `official_noop_release=False` | present |
| §8 / Goal §5.14 | Gate 0–2 unregistered ≠ pass | `week8_decision` → `unregistered`; `scientific_conclusion=None` | **non-defect** ND-02 |
| §8 eval-mode | no cone gate / verifier fallback | `RepairRecord` raises if gated | present |
| Goal §5.8 / §2.5 | P1 held-out length+op vs +ρ; no fake P1 | no `p1_table` → `p1 is None`; no held-out → `requires_held_out` | **non-defect** ND-03 |
| Goal §5.5 / DATA-03 | Plus test-only; family co-group | persist JSON + RAM still in `splits.py` | **not re-run** this freeze; see ND-04 |
| MODEL-01 | frozen Qwen3 / R1-Distill HF | cards + `load_frozen`; local path is random tiny | **pending_server**; tiny ≠ MODEL-01 (ND-01) |
| §8 verbalizer four tiers | real model self-report | CLI `fit` uses `generate_fn=lambda p: prefix[:80]` | stub; **non-defect suggestion** NS-01 |
| Leftover first-seen E | E = task.premises, not labels.jsonl order | `_e_premise_ids` starts from `task.premises`, then **appends** leftover non-sham label ids | live scientific E is 2 premise rows; extra would be `j >= e.shape[0]` skip. **non-defect residue** ND-05 |
| Ancestor tasks.jsonl | must not bind E from parent `col/` WRONG-TASK | `_find_tasks_jsonl` only inspects given stage dirs | **A12-03 not reproduced** |

REQUIREMENTS checkboxes marked `implemented_*` are author claims, not this review’s verdict. VERSION.md’s “alt-source same-value graph / unknown → rho_M null / sham rows never evaluate empty N” is likewise an author claim; only the last two matched this tree.

## 5. Named hunts (independent)

### 5.1 Teacher-force `\nq=` vs §4.1 CoT

Scientific prepare on `t1_tiny.json` (`weight_seed=0`) produced 7 traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value-edit traces, `trace-sham`. Every one has `parse_status=constrained_target`, `parse_region=generated`, `weight_source=random_init`. Events are a single generated-region assignment (`q = 82` or `q = 53`) after teacher-forced `\nq = ` (`generate.append_target_assignment`, docstring: “Not gold values.”). `run_spec.source_kinds` is `{t1_tiny.json: fixture}`.

This is **honest `constrained_target`**. It is **not** MODEL-01 and **not** paper §4.1 natural CoT. Do not require inventing natural CoT. Do not allow anyone to file this path as §4.1 / C1 evidence.

### 5.2 Fixture as official

`load_t1_fixture` requires `source_kind=fixture`. `Task.validate` rejects `official` + `self_authored_arithmetic`. Scientific prepare recorded `source_kind=fixture`. **Not a swap.**

### 5.3 Gate unregistered as pass

`analyze` on the scientific prepare dir: all three gates `decision=unregistered`, `scientific_conclusion=None`, `skip_p2_p3=true`, week8 `status=not_evaluated`. Direct `p1_incremental` without held-out → `requires_held_out`. **Not a pass. No fake P1.**

### 5.4 Leftover first-seen E columns / ancestor WRONG-TASK

`_find_tasks_jsonl` only opens `tasks.jsonl` inside the directories it was given. It does not walk parents.

Independent layout: collect `tasks.jsonl` overwritten to `task_id=WRONG-TASK` with reversed premises; features/labels copied into `deep/x/feat` and `deep/x/labs` with **no** `tasks.jsonl`. `_find_tasks_jsonl(feat, isolated)` is `None`. `fit --in-dir feat --labels-dir isolated` raises `fit requires tasks.jsonl so E columns follow task.premises, not label order`. `_e_premise_ids(real)` is `['p1','p2']`; `_e_premise_ids(WRONG-TASK)` is `['p2','p1']`. The ancestor file was not consulted.

Live scientific collect E is `(2, 32)` from `task.premises`. `_e_premise_ids` still **appends** leftover non-sham label ids (`['p1','p2','leftover']`); those extras are past `e.shape[0]` and skipped. Residue only (ND-05). **A12-03 not reproduced.**

### 5.5 A13-01 — same_value_diff_source is still a rename of the same leaf

Direct `make_source_value_pair(task, "p2", "2")` on `t1_tiny`:

| | base | `same_value_diff_source` | `apply_rename_edit({p2: p2_src})` |
|---|---|---|---|
| premises | `p1=4`, `p2=0` | `p1=4`, `p2_src=0` | `p1=4`, `p2_src=0` |
| q parents | `[p1, p2]` | `[p1, p2_src]` | `[p1, p2_src]` |
| expression | `p1 * p2` | `p1 * p2_src` | `p1 * p2_src` |
| answer / node | `0` | `0` | `0` |
| $R_{\mathrm{task}}(q)$ | `{p1,p2}` | `{p1,p2_src}` | `{p1,p2_src}` |

`p2` is deleted. `{p2, p2_src}` never coexist. There is no second source $b$ that $q$ could read instead of $a$. The implementation is `_rewrite_ids` of the same product leaf, plus the string `(alt source)` in the question. The guard `_target_parents(swapped) == _target_parents(task)` is satisfied by **any** parent-ID rewrite, including `apply_rename_edit`.

Paper §6 (ll. 304–307) and §2.4 require: target computation reads $a$ vs $b$, first $a=b$ so the value matches, then a same-source different-value pair. Goal §5.10 / CAUSAL-02: source and value must not be confused. A renamed leaf is not a second source.

`same_source_diff_value` is a real value edit (`p2: 0→2`, $q=8$). `apply_source_value_edit` still returns that value edit and stamps `source_value_decoupled=True`. CLI prepare uses `make_source_value_pair` and writes both sides; the metadata lie remains on the helper.

Scientific `edits.jsonl` `trace_ids.same_value_diff_source = trace-source`. On a `prep`/`col` sibling layout, `_load_source_value_pair(col)` finds `../prep/edits.jsonl` and `_pair_source_value` / `intervene` report `donor_kind=same_value_diff_source`, `donor_rows=[0,3]`. That is the requested **preference**. It does not make the donor a paper source pair. A collect dir whose sibling is not named `prep`/`prepare`/`s-prep` falls through to `same_identity_fallback` (observed when the scratch collect sat next to `sci_prep`).

### 5.6 A13-02 — unknown / unscanned must not become $M$

`build_labels`: non-exhaustive `no_change` → `behavior=None`, `behavior_known=False`. `event_density_sets` sets `behavior_unknown` if no known behavior on the event or if $T\nsubseteq$ known. `dependency_densities` then forces $M=\emptyset$ and `rho_M_raw=None`.

Direct non-exhaustive `no_change` on `{p1,p2}`: `rho_M_raw=None`, `M=[]`. Partial scan (only `p2` unknown): same. Exhaustive known negatives: `rho_M_raw=1.0`, $M=\{p1,p2\}$ — that is a **known** miss, not unknown-as-negative.

Scientific prepare (teacher-force same digits on edit traces): labels `p1`/`p2` have `behavior_label=None`, `behavior_known=False`; densities `rho_M_raw=null`, `M=[]`, `behavior_unknown=true`. Fit behavior head: `no_known_labels`. **A13-02 not reproduced.**

### 5.7 A13-03 — sham no-change must not book empty $N$

`event_density_sets`: any `sham:` label row or sham hit → `noise_set=None`, `noise_evaluated=False` → `dependency_densities` reason `noise_set_missing`, all excess null.

Direct sham **no-change** (`noise_ref=0.0` on `sham:q`): excess null. Direct sham **change**: same. Fixture prepare + `--sham-opportunities 1`: observation `sham:q` / `no_change` / `['0','0']`; written densities `rho_M_noise=null`, `rho_M_excess=null`. Scientific prepare sham **changed** `82` vs `53`; `sham:q` `noise_ref=1.0`; excess still null. Real premises keep `noise_ref=None`.

The public helper `dependency_densities(..., noise_set=[], noise_evaluated=True)` still writes `rho_M_noise=1.0`, `rho_M_excess=-0.5`. That path is not used by prepare/label when sham rows exist (`_has_sham_row` → `None`). Named hunt is the sham path. **A13-03 not reproduced.** Residue: do not call the helper with evaluated empty $N$ (ND-06).

## 6. Findings

### A13-01 — Rename-of-leaf pair still claimed as source–value decoupling

| field | value |
|---|---|
| **ID** | A13-01 |
| **Severity** | high |
| **Status** | confirmed defect |
| **File / symbol / line** | `src/reasoning_diff/edits.py` `apply_alt_source_same_value` 219–289 (ID rewrite + drop original leaf; parents/expr via `_rewrite_ids`); guard 269–272 only checks parent-**id** set inequality; `make_source_value_pair` 292–301; `apply_source_value_edit` 304–318 still stamps `source_value_decoupled=True` on the **value** edit; `cli.py` `_pair_source_value` 816–839 prefers `same_value_diff_source` when pair meta is found |
| **Trigger** | any T1-style task with a non-placeholder premise (`t1_tiny`; `make_source_value_pair(task, "p2", "2")`; scientific prepare `edits.jsonl`) |
| **Paper req** | Paper §2.4 (ll. 96–108), §6 (ll. 304–307): construct pairs whose **required sources** are $a$ vs $b$ with $a=b$ first, then same-source different-value. Goal §5.10, CAUSAL-02: source and value must not be confused. A rename of the same leaf is not a second source. |
| **Repro** | 1) `make_source_value_pair` on `t1_tiny`: `same_value_diff_source` premises `[p1=4, p2_src=0]`, parents `[p1, p2_src]`, expression `p1 * p2_src`, answer `0`. `p2` absent. `{p2, p2_src}` never coexist. 2) `apply_rename_edit({p2: p2_src})` yields the **same** parent set and expression. 3) Scientific prepare writes that graph as `kind=same_value_diff_source` and `trace-source`. 4) On `prep`/`col` siblings, intervene `donor_kind=same_value_diff_source` (preference holds). On a collect dir whose sibling is not `prep`/`prepare`/`s-prep`, pair meta is missed and donor falls back to `same_identity_fallback`. |
| **Impact** | C2 “source–value decoupled donors” remain a renamed product leaf plus a numeric edit. Event identity of `q` does not change. A paper source-follow matrix cannot be built: there is no $b$ that the target reads instead of $a$. Preferring `trace-source` as donor only swaps hidden states from that rename graph. Tests that assert `p1 * p2_src` encode the swap, so the green suite does not close this. |
| **Fix** | Build two graphs that actually require different existing parents for the target with $a=b$ (keep both $a$ and $b$ in $P$; change which one $q$ reads). A second pair with values unequal. Stop treating `_rewrite_ids` / `{leaf}_src` as `same_value_diff_source`. Keep the donor preference for a **true** source trace, or refuse the pair. |

### A13-02 — Unknown / unscanned as $M$

| field | value |
|---|---|
| **ID** | A13-02 |
| **Severity** | — |
| **Status** | **not reproduced** on this freeze |
| **Evidence** | `measure.py` 123–127 / 343–373: unknown → `behavior_unknown`, $M=\emptyset$, `rho_M_raw=None`. Scientific prepare and direct non-exhaustive `no_change` both write `rho_M_raw=null`. Exhaustive known negatives still report $M=T$ (correct). |

### A13-03 — Sham no-change books empty $N$

| field | value |
|---|---|
| **ID** | A13-03 |
| **Severity** | — |
| **Status** | **not reproduced** on this freeze (live sham path) |
| **Evidence** | Sham rows force `noise_set=None`. Fixture sham `no_change ['0','0']` and scientific sham `changed ['82','53']` both write excess null. Real premises are not given a mapped noise identity. See ND-06 for the unused helper footgun. |

### A12-03 — Ancestor WRONG-TASK binds E

| field | value |
|---|---|
| **ID** | A12-03 |
| **Severity** | — |
| **Status** | **not reproduced** on this freeze |
| **Evidence** | `_find_tasks_jsonl` does not walk parents. Isolated feat/labs refuse fit. WRONG-TASK in ancestor `col/tasks.jsonl` did not bind E. |

### Non-defects and doubts

**ND-01 (non-defect).** Teacher-forced `\nq=` is labeled `constrained_target`. Not §4.1, not MODEL-01. Tiny random weights. REQUIREMENTS’ `MODEL-01 implemented_local_tiny` is an author claim, not a paper result.

**ND-02 (non-defect).** Gate 0–2 stay `unregistered`. No pass/fail.

**ND-03 (non-defect).** P1 is not inferred from labels. Held-out is required.

**ND-04 (not re-verified this freeze).** `splits.py` still persists Plus family keys to `.planning/research/.cache/gsm_test_only_families.json`. No official Plus-id list is shipped under `src/`. Isolated Symbolic with no Plus remains `probe_train` by that design. This channel did not re-run the two-process lock sequence.

**ND-05 (non-defect residue).** `_e_premise_ids` still appends leftover label ids. Live scientific E follows `task.premises` (2 columns). Not a first-seen column swap on the path that has `tasks.jsonl`.

**ND-06 (non-defect residue).** `dependency_densities(..., noise_set=[], noise_evaluated=True)` still deducts empty $N$ (`rho_M_noise=1.0`). Prepare/label/`event_density_sets` do not take that branch when sham rows exist.

**NS-01 (non-defect suggestion).** CLI `fit` verbalizer `generate_fn` echoes the trace prefix. Do not write Fig. 5 / §8 from that blob. Boundary MLP note `event-rows-only_no_negatives` is equally a stub.

**pending_server.** Official iGSM 500 / real GSM-Plus+Symbolic dumps / frozen Qwen3-8B and R1-Distill-Qwen-7B / GPU swap-ablate-rescue / real P1–P3. Missing **code** is not hiding in this list: adapters, tiny hooks, and CLI stages exist. Missing **weights/data** are external.

## 7. Scientific pipeline snapshot (`t1_tiny`, weight_seed=0)

- Traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value edits, `trace-sham`.
- Split: `fix-t1-001` → `probe_train` (hash of this fixture family; not official).
- Events: one generated-region `q = ##` each; `parse_status=constrained_target`.
- H: finite `(7,32)`; E finite `(2,32)`; `H_pre_step` / `H_pre_value` / `H_post_step` present.
- Sham: `sham:q`, changed `82` vs `53` (scientific); fixture sham `no_change` `['0','0']`.
- Densities: `rho_S_raw=null` (empty $P\setminus T$), `rho_M_raw=null`, excess null, `behavior_unknown=true`.
- Fit: task head trained; behavior head `no_known_labels`.
- Analyze: `p1=p2=p3=null`, gates unregistered.
- Intervene (`prep`/`col` siblings): `donor_kind=same_value_diff_source` pointing at the rename graph.

## 8. Verdict

**FAIL**

Confirmed in-scope paper defect: **A13-01** (`same_value_diff_source` is still a rename of the same leaf; parent-id inequality and `trace-source` donor preference do not make it read-$a$ vs read-$b$). A13-02, A13-03, and A12-03 did **not** reproduce on this freeze. Hash matches. Pytest 159 passed is not paper-correct. Teacher-force, fixture marking, unregistered gates, and refused fake P1 are not defects.

This channel does **not** declare Goal complete. `consecutive_pass_count` cannot start from this report.
