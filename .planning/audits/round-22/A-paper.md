# Round-22 Channel A — Paper consistency

- **Agent:** Cursor Grok 4.6 (independent channel A subagent). No parent-assigned reviewer id.
- **Time:** 2026-09-21 (Asia/Shanghai).
- **Scope:** Paper + protocol + Goal §5 + REQUIREMENTS + all `src/reasoning_diff/**/*.py`. Production code, tests, and `pyproject.toml` were not modified. Other round-22 A–F reports were not read. Prior-round A–F files were not used as evidence of this tree. `.planning/audits/ISSUES.md` was treated as author claims only, not as closed.
- **Declared freeze:** `.planning/audits/round-22/VERSION.md`
- **Declared hash:** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` (61 files)
- **Recomputed hash (open):** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` (61 files)
- **Recomputed hash (submit):** `1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb` (61 files)
- **Hash verdict:** **HASH_MATCH**
- **Paper file:** `Reasoning-Diff-修订方案-v3 (1).md`
- **Paper SHA-256:** `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C` (match; 517 lines)

## 1. Hash reproduction

Ran VERSION.md script exactly (POSIX relpath + NUL + bytes over `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`):

```
n_files 61
hash 1f5f379835bba8431e1857c7d184ba4fc136bf1896a15b3193a5609819c7bcdb
```

git_head in VERSION.md (`46a6e26…`) was not used as the freeze identity. Working tree is dirty; the content hash is the freeze. Author notes that r21 A–E PASS on `5097c831…` do not transfer, and that r21 F FAIL concerned disjunctive sham/noise locks (`rho_M_excess != 1.0 or null_reason`). Those notes are versioning remarks only, not evidence about this tree. This channel re-checked the named behaviors on this hash.

## 2. File coverage

Read in full: paper (517 lines), `docs/EXPERIMENT_PROTOCOL.md`, `docs/CURSOR_GOAL_PROMPT.md` §5 (and surrounding sections as context), `.planning/REQUIREMENTS.md`, every production `.py` under `src/reasoning_diff/` (42 files). Sampled `.planning/PAPER_TRACEABILITY.md` executable rows against live symbols. Tests were executed, not accepted as paper-correct. Fixtures and `.planning/audits/round-22/_a_scratch/` were used only as repro inputs. Main scientific dirs were `stage_a` / `stage_b` (no sibling `prep` / `prepare` / `s-prep`).

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
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc` | full; four-tier verbalizer |
| `src/reasoning_diff/cli.py` | 1268 | `cc5eae53d7be27eb87a2813290a5bae0ebda5006ced5897906c3e829d5da2df3` | full; prepare/collect/fit/intervene, finders, pair copy, `prefix_n` |
| `src/reasoning_diff/edits.py` | 367 | `cc8e2d23592a3ab89bdd9c889ee3cb3d559b0f01047d3ad5679aa09669725b51` | full; `_rewrite_ids`, XOR vs rename |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | full |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5` | full |
| `src/reasoning_diff/measure.py` | 405 | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | full; labels, S/M, sham, TO/CSP |
| `src/reasoning_diff/models/__init__.py` | 1 | `0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8` | full |
| `src/reasoning_diff/models/adapters.py` | 42 | `c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a` | full; `card` |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38` | full; H/E, three positions, hook decode |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0` | full |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173` | full; teacher-force, `apply_model_template` |
| `src/reasoning_diff/models/tiny.py` | 120 | `c75d0f53257666128facbfd1f2ab292edc3a99f9840e617bcce35d59d74c537f` | full; Qwen2 `max_position_embeddings=128` |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332` | full; 1 id / char |
| `src/reasoning_diff/probes/__init__.py` | 3 | `3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5` | full |
| `src/reasoning_diff/probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | full |
| `src/reasoning_diff/probes/boundary.py` | 44 | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | full |
| `src/reasoning_diff/probes/calibrate.py` | 45 | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | full |
| `src/reasoning_diff/repair.py` | 232 | `f76ff9998b9a6b1716c0136239fb8ca6cd4e15c17b18a1debaeff6483cf6409b` | full |
| `src/reasoning_diff/rng.py` | 53 | `2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908` | full |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122c0b39a00b2cc6b019d4fe8af4905240881689332ae99ee99` | full |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e9a03ab30c00ccef361290c9e8b3fbc60e0deffdc3e3180c3` | full |
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
| `src/reasoning_diff/transfer.py` | 86 | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | full; Procrustes after common-dim |

Per-file SHA-256 values are from a direct `hashlib.sha256(path.read_bytes())` pass over this freeze tree.

Fixtures inspected (not in the freeze hash): `tests/fixtures/t1_tiny.json` (`source_kind=fixture`). A 70-char padded copy was written only under `_a_scratch/t1_70.json`.

**PAPER_TRACEABILITY sample (executable rows vs symbols).** Sampled rows were checked against this tree, not accepted as closed:

| row | claimed symbol | this tree |
|---|---|---|
| TR-0033 / TR-0121 | `probes/{bilinear,boundary,calibrate}` | `BilinearProbe`, `BoundaryMLP`, `conformal_threshold` present |
| TR-0056 | `interventions.py:intervention_report` | present; relative-to-controls only |
| TR-0073 | `events.py:surface_mentions` | present; stored separately from value labels |
| TR-0082 | `models/features.py:select_prefix_index` | present; three positions |
| TR-0089 | `measure.py:cone_bundle` | present |
| TR-0173 / TR-0341 | `baselines.py:verbalizer` + `cli:fit` | library function exists; **scientific** `fit` writes four `refused_not_section8` rows with **no** `score` (see hunt 7) |
| TR-0337 | `analysis.py:week8_decision` | present; gates stay `unregistered` |

REQUIREMENTS checkboxes marked `implemented_*` remain author claims.

## 3. Checks run

| check | command / method | result | paper-correct? |
|---|---|---|---|
| Freeze hash | VERSION.md Python (open + submit) | 61 files, `1f5f3798…`, HASH_MATCH | n/a |
| Paper SHA | SHA-256 of paper bytes | `F3C0EC08…` match | n/a |
| Unit/regression | `python -m pytest -q --tb=line` | **172 passed**, 26.97s, exit 0 | **No.** Green ≠ paper-correct. |
| Hunt 1 XOR vs rename | `make_source_value_pair` + `apply_alt_source_same_value` + `apply_rename_edit` on `t1_tiny` | keep `p2`, add `src_b=0`, parents `{p1,src_b}`; rename **drops** `p2` | **not the named rename-as-source defect** |
| Hunt 2 overlapping rename | `{p1:p2,p2:p1}` via `_rewrite_ids` / `apply_rename_edit` | question `p2 = 4. p1 = 0. What is q = p2 * p1?`; expr `p2 * p1`. Sequential oracle is `p1 * p1` | **not reproduced** |
| Hunt 3 unknown → M | `build_labels` + `event_density_sets`; live scientific labels | `behavior_unknown=True`, `M=[]`, `rho_M_raw=None` | **not reproduced** |
| Hunt 4 sham row | direct + live `sham:q` | `null_reason=noise_set_missing`; excess/noise all None on the event row | **not reproduced** |
| Hunt 5 noise_ref=0, no sham | constructed real-premise labels | `event_density_sets` → missing, not empty evaluated N | **not reproduced** on the live helper path |
| Hunt 6 ancestor / sibling `lab` | isolated feat/labs; WRONG-TASK in ancestor `col/`; fake labels in sibling `lab/` | `_find_tasks_jsonl` / `_find_labels_jsonl` None | **not reproduced** |
| Hunt 6b `cmd_calibrate` + sibling `lab` | live `calibrate --in-dir fit --features-dir stage_b` with sibling `lab/labels.jsonl` planted | finder args only `(None, fit, feat)`; scores identical after unlink | **not reproduced** |
| Hunt 7 scientific fit §8 | `fit --eval-mode scientific` on `stage_b` + `stage_a` labels | four rows present; `refused_not_section8`; no `score` | **not reproduced**; filter not vacuous |
| Hunt 8 70-char hook ids | scientific prepare/collect/intervene on 70-char fixture; spy `intervene_hidden_decode` **and** `decode_loop` `prompt_ids` | all hook/decode lengths **79 > 64**; `prefix_n=79`; `prefix_truncated=False` | **not reproduced** as silent 64-cap; flag-only would still be green |
| Hunt 9 sham densities conjunctive | live + rebuilt event rows: `rho_*_excess is None` **and** `rho_*_noise is None` **and** `null_reason == noise_set_missing` | True on the one scientific event row. Forged `{0.0, null_reason=None}` passes `rho_M_excess != 1.0 or null_reason` and **fails** the conjunction | **not reproduced**; disjunction rejected as a lock |
| Scientific prepare | `prepare --eval-mode scientific --fixture t1_tiny.json --sham-opportunities 1 --split-fractions 0.40 0.15 0.10 0.10 0.10 0.15 --weight-seed 0` → `stage_a` | exit 0; 7 traces; all `constrained_target` | honest teacher-force; not MODEL-01 |
| Scientific collect | `collect --eval-mode scientific --backend tiny` → `stage_b` | H `(7,32)`, E `(2,32)`, three position arrays, `edits.jsonl` copied | finite H; independently named dir still carries pair meta |
| Scientific fit | `fit --eval-mode scientific --split probe_train --labels-dir stage_a` → `fit` | task head loss finite; behavior `no_known_labels`; four §8 refused, no score | not paper CoT / not §8 scores |
| Scientific intervene | `intervene --eval-mode scientific` on `stage_b` → `intervene` | `donor_kind=same_value_diff_source`, rows `[0,3]`, `prefix_n=45` | preference holds without `prep`/`col` names |
| Analyze | `analyze --in-dir stage_a` → `analyze` | `p1=p2=p3=null`; gates `unregistered`; `scientific_conclusion=None` | honest |
| `p1_incremental` no held-out | two-class, `held_out=None` | `status=requires_held_out` | honest; not fake P1 |

Not run (out of this machine / not required for the named hunts): real HF weights, official iGSM 500, GPU intervene/repair, server collect, full Plus persist two-process lock.

## 4. Paper-paragraph coverage (omissions vs swaps)

Empty “looks implemented” is not a pass. Below is the paper map. Background, related-work, schedule, and untested numeric forecasts are not code requirements.

| paper locus | requirement | this tree | status |
|---|---|---|---|
| §2.2 / §4.1 | Natural generate + identity align; fixture ≠ official | Fixture loader refuses `official`. Scientific generate is tiny + teacher-force `\nq = `, labeled `constrained_target`, `parse_region=generated`. | **non-defect** if not claimed as MODEL-01 / §4.1. See ND-01. |
| §2.3 | $R^{val}$ vs $R^{surf}$; structure separate | `surface_mentions` stored; structure via align `removed/merged` | present as schema; T1 scientific only emits target `q` |
| §2.4 / §6 / Goal §5.10 | Source–value decoupling: keep $a$, add $b=a$, graph reads $b$ not $a$ (XOR) | `apply_alt_source_same_value` keeps `p2`, adds `src_b`, retargets $q$; rename drops `p2` | **named hunt 1 not reproduced** |
| §2.4 rename | overlapping `{p1:p2,p2:p1}` must be simultaneous | one-pass `_rewrite_ids`; live question/expr swap, not `p1 * p1` | **named hunt 2 not reproduced** |
| §2.4 IE / swap | $H'=H_b+\Pi_Z(H_d-H_b)$; C-rand / C-layer | `apply_swap`, `c_rand_delta`, `c_layer_delta` exist | tools present; tiny intervene without `--dev-layer-scores` leaves C-layer null (honest) |
| §2.5 Prop 1–2, cone | over-approx protocol; conformal ceil((N+1)(1-α)) | `dirty_cone`, `conformal_threshold`, `joint_edit_counterexample` | formulas present; not evaluated on real traces |
| §2.6 / §3 | $S=B\setminus T$, $M=T\setminus B$; unknown ≠ negative; noise matched or null | unknown/unscanned → `behavior_unknown`, `rho_M_raw=null`; sham rows → event-row `noise_set_missing` and all `rho_*_excess` / `rho_*_noise` None | **hunts 3–5 and 9 not reproduced** |
| §3 TO/CSP | LCS TO; matched CSP; empty denom N/A | `preservation_to_csp`, `lcs_overlap` | present |
| §4.2 bilinear / MLP-256 | $h^\top UV^\top e+b$, $r=64$; Hidden=256 | `BilinearProbe`, `BoundaryMLP` | form present; CLI boundary fit is all-ones / no negatives (stub; ND-07) |
| §5 Fig. 2 three positions | pre-step / pre-value / post-step | collect writes `H_pre_step`, `H_pre_value`, `H_post_step` | present on tiny |
| §7 T1–T4 | official iGSM + GSM-Symbolic/Plus + Hotpot/MuSiQue/HumanEval + T4 | adapters exist; graphs unknown/partial where required; no official Plus-id list | DATA-02 loaders present; **pending_server** for real dumps |
| §7 T2-noop | front/mid/back × surface; not official NoOp | `make_noop_pair`, `official_noop_release=False` | present |
| §8 / Goal §5.14 | Gate 0–2 unregistered ≠ pass | `week8_decision` → `unregistered`; `scientific_conclusion=None` | **non-defect** ND-02 |
| §8 eval-mode | no cone gate / verifier fallback | `RepairRecord` raises if gated | present |
| Goal §5.8 / §2.5 | P1 held-out length+op vs +ρ; no fake P1 | no `p1_table` → `p1 is None`; no held-out → `requires_held_out` | **non-defect** ND-03 |
| Goal §5.5 / DATA-03 | Plus test-only; family co-group | persist JSON + RAM still in `splits.py` | **not re-run** this freeze; see ND-04 |
| MODEL-01 | frozen Qwen3 / R1-Distill HF | cards + `load_frozen`; local path is random tiny | **pending_server**; tiny ≠ MODEL-01 (ND-01) |
| §8 verbalizer four tiers | real model self-report | scientific `fit` writes four refused rows with no score; fixture-mode still echoes prefix | **hunt 7 not reproduced** on scientific; see ND-07 |
| Leftover first-seen E | E = task.premises, not labels.jsonl order | `_e_premise_ids` starts from `task.premises`, then **appends** leftover non-sham label ids | live scientific E is 2 premise rows. **non-defect residue** ND-05 |
| Ancestor / sibling `lab` | must not bind E/labels from parent `col/` or sibling `lab/` | `_find_stage_file` only inspects given stage dirs; `cmd_calibrate` does not walk sibling `lab` | **hunt 6 not reproduced** |
| Pair metadata | collect must carry pair so independently named dirs still pair | collect copies `edits.jsonl`; `_load_source_value_pair` reads only `in-dir/edits.jsonl` | still holds on `stage_b` |
| Protocol §4 / Goal §5.10 prefix | 70-char intervene must keep hook `prompt_ids` length >64; `prefix_truncated` flag alone is not enough | independent spy: all hook/decode ids **79**; written `prefix_n=79` | **named hunt 8 not reproduced** as a 64-cap |
| §2.6 / §3 sham densities | event-row `rho_*_excess` and `rho_*_noise` are None **and** `null_reason == noise_set_missing`. `rho_M_excess != 1.0 or null_reason` is not a lock | live + rebuilt event row satisfies the conjunction; forged 0.0 fails it | **named hunt 9 not reproduced** |

## 5. Named hunts (independent)

### 5.1 Teacher-force `\nq=` vs §4.1 CoT

Scientific prepare on `t1_tiny.json` (`weight_seed=0`) produced 7 traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value-edit traces, `trace-sham`. Every one has `parse_status=constrained_target`, `parse_region=generated`, `weight_source=random_init`. Events are a single generated-region assignment (`q = 82` or `q = 53`) after teacher-forced `\nq = ` (`generate.append_target_assignment`, docstring: “Not gold values.”). `run_spec.source_kinds` is `{t1_tiny.json: fixture}`.

This is **honest `constrained_target`**. It is **not** MODEL-01 and **not** paper §4.1 natural CoT. Do not require inventing natural CoT. Do not allow anyone to file this path as §4.1 / C1 evidence.

### 5.2 Fixture as official

`load_t1_fixture` requires `source_kind=fixture`. `Task.validate` rejects `official` + `self_authored_arithmetic`. Scientific prepare recorded `source_kind=fixture`. **Not a swap.**

### 5.3 Gate unregistered as pass

`analyze` on `stage_a`: all three gates `decision=unregistered`, `scientific_conclusion=None`, `skip_p2_p3=true`, week8 `status=not_evaluated`. Direct `p1_incremental` with two classes and no held-out → `requires_held_out`. **Not a pass. No fake P1.** Gate unregistered is **not a defect**.

### 5.4 Hunt 1 — `same_value_diff_source` vs rename (XOR)

Direct `make_source_value_pair(task, "p2", "2")` and `apply_alt_source_same_value(task, "p2")` on `t1_tiny`:

| | base | `same_value_diff_source` | `apply_rename_edit({p2: src_b})` |
|---|---|---|---|
| premises | `p1=4`, `p2=0` | `p1=4`, `p2=0`, `src_b=0` | `p1=4`, `src_b=0` |
| q parents | `[p1, p2]` | `[p1, src_b]` | `[p1, src_b]` |
| expression | `p1 * p2` | `p1 * src_b` | `p1 * src_b` |
| answer | `0` | `0` | `0` |
| $R_{\mathrm{task}}(q)$ | `{p1,p2}` | `{p1,src_b}` | `{p1,src_b}` |

Guards in `apply_alt_source_same_value` (221–277): keep original leaf $a$, add equal-value $b$=`src_b`, require $b$ in parents and $a$ **not** in parents. Runtime: `keep_a=True`, `added_b=True`, `b_equals_a=True`, `reads_b_not_a=True`. Rename **drops** `p2` (`same_premise_set_as_rename=False`). Parents/expression of the target coincide with a rename of the same leaf, but the graphs are not the same object: $a$ and $b$ coexist only on the source pair.

`same_source_diff_value` is a real value edit (`p2: 0→2`, $q=8`). Scientific `edits.jsonl` writes that pair and `trace_ids.same_value_diff_source = trace-source`. Live `trace-source` prompt is `p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?` with event `task_parents=["p1","src_b"]`.

Paper §6 (ll. 304–307) / §2.4: target computation reads $a$ vs $b$, first $a=b$. This tree keeps $a$, adds $b$, and retargets. **Named hunt 1 is not a confirmed rename-as-source defect on this freeze.**

### 5.5 Hunt 2 — overlapping rename `{p1:p2,p2:p1}` must be simultaneous

`_rewrite_ids` (`edits.py` 151–157) compiles every mapping key into one regex and substitutes in a single pass. `apply_rename_edit` uses that for question, premise text, and expression; parent/id maps use `mapping.get` on the original names.

On `t1_tiny` (`p1 = 4. p2 = 0. What is q = p1 * p2?`):

| | simultaneous (this tree) | sequential oracle (`p1→p2` then `p2→p1`) |
|---|---|---|
| question | `p2 = 4. p1 = 0. What is q = p2 * p1?` | `p1 = 4. p1 = 0. What is q = p1 * p1?` |
| expression | `p2 * p1` | `p1 * p1` |
| premises | `p2=4`, `p1=0` | would collapse both names onto `p1` |

Live `apply_rename_edit` matches the simultaneous column. **Named hunt 2 is not a sequential overlapping-rename defect on this freeze.**

### 5.6 Hunt 3 — unknown / unscanned must not become $M$

`build_labels`: non-exhaustive `no_change` → `behavior=None`, `behavior_known=False`. `event_density_sets` sets `behavior_unknown` if no known behavior on the event or if $T\nsubseteq$ known. `dependency_densities` then forces $M=\emptyset$ and `rho_M_raw=None`.

Direct non-exhaustive `no_change` on `{p1,p2}`: event row `M=[]`, `rho_M_raw=null`, `behavior_unknown=true`. Scientific prepare: labels `p1`/`p2` have `behavior_label=None`, `behavior_known=False`; densities `rho_M_raw=null`, `M=[]`, `behavior_unknown=true`. Fit behavior head: `no_known_labels`. **Hunt 3 not reproduced.**

### 5.7 Hunt 4 — any `sham:` row → `noise_set` missing

`event_density_sets`: any `sham:` label row or sham hit → `noise_set=None`, `noise_evaluated=False` → `dependency_densities` reason `noise_set_missing`, all excess/noise null.

Direct sham **no-change** (`noise_ref=0.0` on `sham:q`): excess/noise all None, `noise_set_missing`. Live scientific sham **changed** `82` vs `53`; `sham:q` `noise_ref=1.0`; event-row excess/noise still None; `null_reason=noise_set_missing`. Real premises keep `noise_ref=None`. **Hunt 4 not reproduced.**

### 5.8 Hunt 5 — real premises `noise_ref=0`, no `sham:`, must not book empty evaluated $N$

Constructed labels: `p1`/`p2` `noise_ref=0.0`, no sham rows. `event_density_sets` → `noise_set` missing (not `[]` + `noise_evaluated=True`). Excess/noise None (`null_reason=noise_set_missing`).

The public helper `dependency_densities(..., noise_set=[], noise_evaluated=True)` still writes a numeric noise term (`rho_M_noise=1.0`, `rho_M_excess=-0.5` on this construction: $T=\{p1,p2\}$, $B=\{p1\}$). That path is not used by prepare/label/`event_density_sets` for this case. Named hunt is the live/event-set path. **Hunt 5 not reproduced.** Residue: do not call the helper with evaluated empty $N$ (ND-06).

### 5.9 Hunt 6 — `_find_tasks_jsonl` / `_find_labels_jsonl` must not walk ancestors or sibling `lab`

Source (`cli.py` 703–719): `_find_stage_file` only opens `name` inside the directories it was given. No `parent` / `rglob` / sibling-name walk (`lab` / `label` / `labels`).

Independent layout: WRONG-TASK planted in ancestor `col/tasks.jsonl`; fake labels in sibling `lab/labels.jsonl`; isolated `deep/feat` and `deep/labs` have **no** `tasks.jsonl` / `labels.jsonl`. `_find_tasks_jsonl(feat, labs)` is `None`. `_find_labels_jsonl(feat, labs)` is `None`. Passing the sibling `lab` directory itself finds that file only then.

`cmd_calibrate` was also run with a sibling `lab/labels.jsonl` present and **not** passed as `--labels-dir`. Spy on `_find_labels_jsonl`: the only call was `(None, fit, feat)`. Scores with the sibling file present equal scores after that file was removed.

`_e_premise_ids` on the real fixture is `['p1','p2']` then leftover ids if present (`['p1','p2','leftover']`). The ancestor / sibling files were not consulted. **Hunt 6 not reproduced.** Residue ND-05.

### 5.10 Hunt 7 — scientific fit must write four §8 refused rows with no score (filter not vacuous)

VERSION.md records a prior vacuous-filter failure: `all(... if baseline in S)` is vacuous if the four §8 rows are omitted or carry `score=1.0`. This freeze was checked on the live scientific `fit` blob (`_a_scratch/fit/probes.jsonl`):

| baseline | status | `score` key |
|---|---|---|
| `verbalizer` | `refused_not_section8` | **absent** |
| `attention_mean` | `refused_not_section8` | **absent** |
| `attention_rollout` | `refused_not_section8` | **absent** |
| `attention_threshold` | `refused_not_section8` | **absent** |

All four names are present (none missing). Keys on each row are only `{baseline, reason, status}`. A set-equality check `present == {verbalizer, attention_mean, attention_rollout, attention_threshold}` plus `all(status==refused_not_section8 and "score" not in row)` is **True**. That is not a vacuous `all` over an empty filtered list.

Task head: finite loss, rank 32. Behavior: `no_known_labels`. Do not write Fig. 5 / §8 from this run. **Hunt 7 not reproduced.** Boundary MLP still trains all-ones on event rows (ND-07); that is not a §8 verbalizer/attention score.

### 5.11 Hunt 8 — 70-char intervene hook `prompt_ids` length >64 (not just `prefix_truncated`)

A check that only locks `prefix_truncated is not True` stays green on `{prefix_truncated: False, n_ids: 64}` and on a missing field. This freeze was required to spy the hook `prompt_ids` length.

`cmd_intervene` still **hardcodes** `hook_meta["prefix_truncated"] = False` (`cli.py` 959). It also writes `hook_meta["prefix_n"] = len(ids)` (960). `_tiny_prefix_ids` encodes one id per character, returns 70 ids for a 70-char string, and **raises** on 97 (`>96`). It does not slice to 64.

Independent 70-char fixture (original `t1_tiny` question padded to length 70; spans unchanged). Scientific prepare/collect/intervene. Spies were installed on **both** `collect.intervene_hidden_decode` (the list CLI passes) **and** `collect.decode_loop` / `generate.decode_loop` (the tensor the hook actually sees):

| probe | lengths |
|---|---|
| prepare `prompt_text` | `[70, 70, 70, 83, 70, 70, 70]` (source pair is longer) |
| `intervene_hidden_decode(prompt_ids)` | `[79, 79, 79, 79]` |
| `decode_loop` tensor width | eight calls, all `79` |
| written `relative.prefix_n` | `79` |
| written `relative.prefix_truncated` | `False` |

79 = 70-char question + the generated prefix up to the teacher-forced assignment start. All hook/decode lengths are **>64**. `prefix_n` matches the spy. A flag-only assertion (`prefix_truncated is not True`) would still have passed if the hook had been 64; that is why the spy is the named check.

Qwen2 tiny `max_position_embeddings=128`, so 79 ids are inside the model context. `_tiny_prefix_ids("x"*97)` still raises. Unpadded `t1_tiny` scientific intervene writes `prefix_n=45` (36-char question + generated prefix); that short path is not the 70-char hunt.

**Named hunt 8 is not a silent 64-token cap on this freeze.** Residue: `prefix_truncated` remains a constant `False` (ND-08). Do not treat that flag as proof of prefix length.

### 5.12 Hunt 9 — scientific sham densities (conjunctive lock)

The named lock is **not** `rho_M_excess != 1.0 or null_reason`. That disjunction is true for a forged event row `{rho_*_excess: 0.0, rho_*_noise: 0.0, null_reason: None}` and for a booked empty $N$ whose noise term is `1.0` only if the other side of the `or` happens to be truthy. Neither case is an honest “noise protocol missing.”

Required on **event rows** (live scientific `labels.jsonl` densities, and the same labels rebuilt through `event_density_sets`):

- `rho_S_excess is None`
- `rho_M_excess is None`
- `rho_S_noise is None`
- `rho_M_noise is None`
- `null_reason == "noise_set_missing"`

Live scientific event row (one `q` event; sham observation `changed` `82` vs `53`; `sham:q` `noise_ref=1.0`): all four fields are JSON `null`, `null_reason` is `noise_set_missing`. Rebuilt from the written label rows: same. Direct `sham:q` with `noise_ref=0.0`: same conjunction. Real-premise `noise_ref=0.0` with no `sham:` row: same conjunction, `noise_set` missing, not evaluated empty $N$.

Aggregation on the blob averages only numeric event values, so top-level `null_reason` is absent. That is not the named lock. Top-level `rho_*_excess` / `rho_*_noise` are still `None`. Do not accept the top-level disjunction `rho_M_excess != 1.0 or null_reason` as proof: it is true whenever excess is `None` even if `null_reason` is missing.

A constructed helper call `dependency_densities(..., noise_set=[], noise_evaluated=True)` still books `rho_M_noise=1.0`. That path is not the scientific event-row path (ND-06).

**Named hunt 9 is not a booked sham/empty-$N$ density on this freeze.** The conjunctive event-row lock holds; the disjunction is insufficient and was not used as a pass.

## 6. Findings

### Named hunts

| ID | Severity | Status | Evidence |
|---|---|---|---|
| Hunt 1 / XOR rename-as-source | — | **not reproduced** | Keep `p2`, add `src_b=0`, $q$ reads `src_b` not `p2`. Rename drops `p2`. |
| Hunt 2 / sequential overlapping rename | — | **not reproduced** | `{p1:p2,p2:p1}` → `p2 = 4. p1 = 0. What is q = p2 * p1?`, expr `p2 * p1`. Sequential oracle is `p1 * p1`. |
| Hunt 3 / unknown as $M$ | — | **not reproduced** | Unknown → `behavior_unknown`, $M=\emptyset$, `rho_M_raw=None` (direct + live). |
| Hunt 4 / sham books $N$ | — | **not reproduced** | Any `sham:` row → `noise_set_missing`. Live sham hit still excess/noise-null on the event row. |
| Hunt 5 / noise_ref=0 empty $N$ | — | **not reproduced** on `event_density_sets` | Real-premise `noise_ref=0` with no sham → missing, not evaluated empty $N`. See ND-06. |
| Hunt 6 / ancestor + sibling `lab` | — | **not reproduced** | Finders do not walk parents or sibling `lab`. Isolated feat/labs find nothing. `cmd_calibrate` with sibling `lab` present uses only given dirs; scores unchanged. |
| Hunt 7 / invented or omitted §8 scores | — | **not reproduced** | Four §8 rows exist; `refused_not_section8`; no `score`. Filter is not vacuous. |
| Hunt 8 / 70-char hook ids capped at 64 | — | **not reproduced** | Spy: hook and `decode_loop` ids all **79 > 64**. `prefix_n=79`. Flag-only is still insufficient by itself. |
| Hunt 9 / sham densities disjunction | — | **not reproduced** | Event-row conjunction holds. Forged 0.0 / missing `null_reason` fails it and would have passed `rho_M_excess != 1.0 or null_reason`. |

No confirmed in-scope paper defect on this freeze.

### Non-defects and doubts

**ND-01 (non-defect).** Teacher-forced `\nq=` is labeled `constrained_target`. Not §4.1, not MODEL-01. Tiny random weights. REQUIREMENTS’ `MODEL-01 implemented_local_tiny` is an author claim, not a paper result.

**ND-02 (non-defect).** Gate 0–2 stay `unregistered`. No pass/fail. Unregistered is not a defect.

**ND-03 (non-defect).** P1 is not inferred from labels. Held-out is required.

**ND-04 (not re-verified this freeze).** `splits.py` still persists Plus family keys to `.planning/research/.cache/gsm_test_only_families.json`. No official Plus-id list is shipped under `src/`. Isolated Symbolic with no Plus remains `probe_train` by that design. This channel did not re-run the two-process lock sequence.

**ND-05 (non-defect residue).** `_e_premise_ids` still appends leftover label ids. Live scientific E follows `task.premises` (2 columns). Not a first-seen column swap on the path that has `tasks.jsonl`.

**ND-06 (non-defect residue).** `dependency_densities(..., noise_set=[], noise_evaluated=True)` still deducts empty $N$ (`rho_M_noise=1.0` on the constructed $T=\{p1,p2\}$). Prepare/label/`event_density_sets` do not take that branch for sham rows or for real-premise `noise_ref=0` without sham.

**ND-07 (non-defect residue).** Scientific `fit` still writes `boundary_mlp` with all-ones labels (`event-rows-only_no_negatives`). That is not a §8 verbalizer/attention score. Do not write Fig. 2 boundary F1 from that blob.

**ND-08 (non-defect residue).** `prefix_truncated` is still hardcoded `False`. The 70-char hunt is closed by the live hook/`decode_loop` lengths (79), not by that flag. A future change that silently sliced ids to 64 while leaving the flag False would still be a defect.

**ND-09 (non-defect residue).** Aggregated densities omit `null_reason` because the mean-over-events helper only averages numeric keys. The named lock is the **event row**. Do not treat a top-level `rho_M_excess is None` disjunction as the sham protocol.

**pending_server.** Official iGSM 500 / real GSM-Plus+Symbolic dumps / frozen Qwen3-8B and R1-Distill-Qwen-7B / GPU swap-ablate-rescue / real P1–P3. Missing **code** is not hiding in this list: adapters, tiny hooks, and CLI stages exist. Missing **weights/data** are external.

## 7. Scientific pipeline snapshot (`t1_tiny`, weight_seed=0, dirs `stage_a`/`stage_b`)

- Traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value edits, `trace-sham`.
- Split: `fix-t1-001` → `probe_train` (hash of this fixture family; not official).
- Events: one generated-region `q = ##` each; `parse_status=constrained_target`; assignment `\nq = 82` or `\nq = 53`.
- H: finite `(7,32)`; E finite `(2,32)`; `H_pre_step` / `H_pre_value` / `H_post_step` present.
- Sham: `sham:q`, changed `82` vs `53`; `noise_ref=1.0`; event-row excess/noise null, `null_reason=noise_set_missing`.
- Densities: `rho_S_raw=null` (empty $P\setminus T$), `rho_M_raw=null`, event-row `rho_*_excess`/`rho_*_noise` null, `behavior_unknown=true`.
- Fit: task head trained; behavior head `no_known_labels`; four §8 baselines refused with no score.
- Analyze: `p1=p2=p3=null`, gates unregistered.
- Intervene (`stage_b`, not named `prep`/`col`): `donor_kind=same_value_diff_source`, donor rows `[0,3]`, `prefix_truncated=false`, `prefix_n=45` on the short fixture.

## 8. Verdict

**PASS**

Hash matches on open and submit. Named hunts did **not** reproduce as paper defects on this freeze: the source pair keeps $a$ and adds equal-value $b$ (XOR, not a rename); overlapping `{p1:p2,p2:p1}` is simultaneous (`p2 * p1`, not sequential `p1 * p1`); unknown is not booked as $M$; sham and `noise_ref=0` do not evaluate empty $N$; ancestor `tasks.jsonl` and sibling `lab/` are not walked, including a live `cmd_calibrate` with sibling `lab` present; independently named collect dirs still carry pair metadata; scientific fit writes four §8 verbalizer/attention rows with `refused_not_section8` and no `score` (the existence check is not vacuous); a 70-char intervene was spied at the hook and `decode_loop` — all `prompt_ids` lengths are **79 > 64**, not merely `prefix_truncated=False`; scientific sham **event rows** have `rho_*_excess is None` **and** `rho_*_noise is None` **and** `null_reason == noise_set_missing`. `rho_M_excess != 1.0 or null_reason` was checked only as a negative control (a forged 0.0 row passes it) and was **not** accepted as sufficient. Teacher-force, fixture marking, unregistered gates, and refused fake P1 are not defects. Pytest 172 passed is not paper-correct.

This channel does **not** declare the Goal complete. A single-channel PASS does not start `consecutive_pass_count` by itself.
