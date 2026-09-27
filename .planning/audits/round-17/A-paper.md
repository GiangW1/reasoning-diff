# Round-17 Channel A — Paper consistency

- **Agent:** Cursor Grok 4.6 (independent channel A subagent). No parent-assigned reviewer id.
- **Time:** 2026-09-21 03:02 (Asia/Shanghai).
- **Scope:** Paper + protocol + Goal §5 + REQUIREMENTS + all `src/reasoning_diff/**/*.py`. Production code, tests, and `pyproject.toml` were not modified. Other round-17 A–F reports were not read. `.planning/audits/ISSUES.md` was treated as author claims only, not closed. Prior-round A–F files were not used as evidence of this tree.
- **Declared freeze:** `.planning/audits/round-17/VERSION.md`
- **Declared hash:** `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` (61 files)
- **Recomputed hash:** `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` (61 files)
- **Hash verdict:** **HASH_MATCH**
- **Paper file:** `Reasoning-Diff-修订方案-v3 (1).md`
- **Paper SHA-256:** `f3c0ec087b5bf4e503db35f4d234c727df3ce66f933e80781c69a0cc312ea57c` (517 lines)

## 1. Hash reproduction

Ran VERSION.md script exactly (POSIX relpath + NUL + bytes over `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`):

```
n_files 61
hash 3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6
```

git_head in VERSION.md (`46a6e26…`) was not used as the freeze identity. Working tree is dirty; the content hash is the freeze. Author notes in VERSION.md / `PAPER_TRACEABILITY.md` about prior freezes or later hashes are versioning remarks, not evidence about this tree.

## 2. File coverage

Read in full: paper (517 lines; sections 0–12, formulas, tables, S1–S4), `docs/EXPERIMENT_PROTOCOL.md`, `docs/CURSOR_GOAL_PROMPT.md` §5 (rest for context), `.planning/REQUIREMENTS.md`, every production `.py` under `src/reasoning_diff/`. Sampled executable `PAPER_TRACEABILITY.md` rows against live symbols. Tests were executed as claimed-lock evidence, not as paper-correctness. Fixtures and `.planning/audits/round-17/_a_scratch/` were used only as reviewer inputs / runtime.

| path | lines | digest | what was read |
|---|---|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 517 | `f3c0ec087b5bf4e503db35f4d234c727df3ce66f933e80781c69a0cc312ea57c` | full paper |
| `docs/EXPERIMENT_PROTOCOL.md` | 86 | `83a9142dba4f7fcd337a70ef8cd1a847ed7eb7ff110f2d77f466387ab491391d` | full protocol |
| `docs/CURSOR_GOAL_PROMPT.md` | 166 | `b9e0a8ea3fc87bf00f1949bd8201407e097ef3e25660173275ba11e42a39eb7e` | §5 required; rest for context |
| `.planning/REQUIREMENTS.md` | 76 | `39cf907c0b66b9b26ae7355e394848cfa1ff41ce5166310e1dc0a9307f9ac498` | full; author status only |
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58db2279eb40d144c57bbd25f5bcddb74a8edcd0d995dcde9fb` | full |
| `src/reasoning_diff/__main__.py` | 4 | `307299fda7b77d22c64cb51430ec75e5f59d78e9c948786afb3b2544fe45e4b7` | full |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63bfca95a567c25b05fdddf9b08a6a3253bc84f4462ba86b7af` | full; P1/P2/P3, week8, cone, retrieval |
| `src/reasoning_diff/artifacts.py` | 85 | `524657027e9b402f61fe173b8de9b0cdb70dd348c525f7de6cf4bd37c05a2332` | full |
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4af55bb1b18afaf023d503279c778d21fd3344ebe41ffc5fc` | full; four-tier verbalizer + attention helpers |
| `src/reasoning_diff/cli.py` | 1260 | `9431b7768fda6a3c3c577f811b747f57f79f57b111dfe89c12281d1d23f95bb5` | full; prepare/collect/label/fit/calibrate/intervene/repair/analyze |
| `src/reasoning_diff/edits.py` | 365 | `1e5b97d63a62ab78a43ee9db33594a2cc1de3add5ad25aac81007b05af3efb91` | full; `apply_alt_source_same_value` XOR `src_b` |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814c3c99b3a55a1f3499055517d0be2751061c850caee39c8f3` | full |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78ebeecbc63977c6b5a866b41d5ae6048e0e6541604a4d84a4` | full |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277405b706e249302680e7a761caa949b1a8bc7200d673f4583` | full; `R_task` ancestors |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649fc68f56c58a4915ae4d67666e7a068a59b9cabce68d2f9f2` | full; swap / C-rand / C-layer / INLP / IE |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd37dffc0097e0433ddf87a51d4e3adb3164458a63f448bd7b5` | full |
| `src/reasoning_diff/measure.py` | 405 | `985b9d9328e4111f2b841f00e442fdf02623c1279dc16761edec5ce1305605a5` | full; labels, S/M, sham, empty-N, TO/CSP |
| `src/reasoning_diff/models/__init__.py` | 1 | `0b7dd6c4dd8520655339529f3599b04f17709bd921a6014de8668ff2d63ba3a8` | full |
| `src/reasoning_diff/models/adapters.py` | 42 | `c1992624026a1bf015dc6f308d60acb8e3d9a9264f7c951b005ab10e773a0a7a` | full; frozen cards, `load_frozen` |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20162137fd9bd6469034103df19f1aedbdb63bad7299248c38` | full; H/E, three positions |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185aef07a80e80025c4f6d100685f3cb866ed98b25a4c153863e0` | full |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7f19b37c77716b59f75f56fe1f5fb061a2cbdb877c20d9173` | full; teacher-force `\n{target} = ` |
| `src/reasoning_diff/models/tiny.py` | 120 | `c75d0f53257666128facbfd1f2ab292edc3a99f9840e617bcce35d59d74c537f` | full; random-init Qwen2/3 mini |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010facf05f2fe835e1e3a7b0119c5e655f81b02769fb0a678d332` | full; 60–75% band |
| `src/reasoning_diff/probes/__init__.py` | 3 | `3065196db28e929c617e0f13488fceeba839acabe10d4f8b6bde9edab7cf39f5` | full |
| `src/reasoning_diff/probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec88b2720f239e162baf6d66ab9116e437b990f8b31a08b3a9` | full; \(h^\top UV^\top e+b\), \(\lambda_{FN}=10\) |
| `src/reasoning_diff/probes/boundary.py` | 44 | `ce3b549be7d671ff3e0d2513b038e144492f5d43f2e6c1f840cd857297659034` | full; Hidden=256 |
| `src/reasoning_diff/probes/calibrate.py` | 45 | `e8b3ed3459bb22c51db94b57009399d3491626b161ce2f8a8a5e2fc2134fb334` | full; \(\lceil(N+1)(1-\alpha)\rceil\) |
| `src/reasoning_diff/repair.py` | 232 | `f76ff9998b9a6b1716c0136239fb8ca6cd4e15c17b18a1debaeff6483cf6409b` | full |
| `src/reasoning_diff/rng.py` | 53 | `2098c2c72a852eaa1e5d3a71b74edd68c180469e9c9e9366ec0737af3e736908` | full |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a4504a56cefc66c9ade4e6366fb310e6ddedf9418e087eb53a7` | full; official≠fixture |
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
| `src/reasoning_diff/transfer.py` | 86 | `5549f84bd1bd624037b0f365a00fbe963190c5f5b910c8a05f70349e256c95c2` | full |

Per-file SHA-256 values are from a direct `hashlib.sha256(path.read_bytes())` pass over this freeze tree.

Fixtures inspected (not in the freeze hash): `tests/fixtures/t1_tiny.json` (`source_kind=fixture`).

### 2.1 Traceability sample (executable rows vs live symbols)

| row | claimed symbol | live? | note |
|---|---|---|---|
| TR-0006 DATA-01 | `t1_official.py:load_igsm_snapshot` | yes L14 | official-only; refuses `G` without template |
| TR-0007 MEAS-02 | `measure.py:dependency_densities` | yes L84 | S/M + null excess |
| TR-0008 SURF-01 | `events.py:surface_mentions` | yes L13 | present |
| TR-0010 PROP1-01 | `measure.py:joint_edit_counterexample` | yes L388 | blocks joint soundness |
| TR-0011 C3-01 | `analysis.py:p1_incremental` | yes L41 | held-out required |
| TR-0033 PROBE-01 | `probes/bilinear.py:BilinearProbe` | yes L7 | form present |
| TR-0158 / TR-0332 CAUSAL-02 | `interventions.py:intervention_report` | yes L98 | **ledger mis-map:** a-vs-b *construction* is `edits.py:apply_alt_source_same_value` L219, not this reporter. `PAPER_TRACEABILITY.md` does not mention `apply_alt_source_same_value` / `make_source_value_pair`. Author ledger, not a code defect. |
| TR-0173 VERB-01 | `baselines.py:verbalizer` | yes L92 | library exists; scientific CLI refuses toys |

REQUIREMENTS `implemented_*` checkboxes and VERSION’s “XOR src_b / refused_not_section8 / empty-N not evaluated” are author claims. This review re-checked them from source + runtime.

## 3. Checks run

| check | command / method | result | paper-correct? |
|---|---|---|---|
| Freeze hash | VERSION.md Python | 61 files, `3d0a0764…`, **HASH_MATCH** | n/a |
| Paper / protocol SHA | SHA-256 of bytes | paper `f3c0ec08…`; protocol `83a9142d…` | n/a |
| Unit/regression | `python -m pytest -q --tb=line` | **160 passed**, 25.01s, exit 0 | **No.** Green ≠ paper-correct. Suite is a claimed lock only. |
| Hunt 1 XOR vs rename | `apply_alt_source_same_value` vs `apply_rename_edit` on `t1_tiny` p2 | keep `p2`, add `src_b=0`, parents `{p1,src_b}`, expr `p1 * src_b`; rename **drops** `p2` | **not the named rename-only defect** |
| Hunt 2 unknown ≠ M | `build_labels` + `event_density_sets` | non-exhaustive `no_change` → `behavior_unknown=True`, `M=[]`, `rho_M_raw=None`; exhaustive known negatives → `M={p1,p2}`, `rho_M_raw=1.0` | **not reproduced** |
| Hunt 3 sham row | labels with `sham:q` | `null_reason=noise_set_missing`; all excess null | **not reproduced** |
| Hunt 4 noise_ref=0, no sham | real premises `noise_ref=0.0`, no `sham:` row | excess null, `noise_set_missing` (not raw; not evaluated empty N) | **not reproduced** |
| Hunt 5 ancestor extras | isolated feat/labs; WRONG-TASK in ancestor `deep/col/` | `_find_tasks_jsonl(feat,labs)=None`; scientific fit raises `tasks.jsonl` | **not reproduced** |
| Hunt 6 scientific §8 | `fit --eval-mode scientific` probes.jsonl | verbalizer/attention_* all `refused_not_section8`; no zeros / echo / `[0.1,0.9]` | honest refuse (see ND-01 / NS-01) |
| Hunt 7 teacher-force | scientific prepare traces | all `parse_status=constrained_target`, assignment `\nq = ##` | honest; not §4.1 / MODEL-01 |
| Hunt 8 gates / tiny / offline H | `week8_decision`; collect backends | gates `unregistered`; tiny `random_init`; scientific+offline raises; fixture offline H `(1,8)` `offline_prefix_ids` | **non-defects** as specified |
| Scientific prepare | `prepare --eval-mode scientific --fixture t1_tiny.json --sham-opportunities 1 --split-fractions 0.40 0.15 0.10 0.10 0.10 0.15 --weight-seed 0` | exit 0; 7 traces; pair graph keeps `p2`+`src_b` | honest teacher-force; XOR pair written |
| Scientific collect | `collect --eval-mode scientific --backend tiny --weight-seed 0` | H `(7,32)` finite; E `(2,32)` finite; three position arrays; `weight_source=random_init` | finite H yes; not MODEL-01 |
| Scientific fit | `fit --eval-mode scientific --split probe_train` | task head loss finite; behavior `no_known_labels`; §8 refused | not paper CoT labels; no fake Fig. 5 |
| Intervene | `intervene --in-dir col` (edits copied into collect) | `donor_kind=same_value_diff_source`, `donor_rows=[0,3]` (`trace-base`,`trace-source`); C-layer `dev_scores_missing` | preference holds on a **true** XOR graph; scores are tiny decode, not §6 follow |
| Scientific collect + offline | `--backend offline --eval-mode scientific` | **ValueError** `scientific collect refuses offline_prefix_ids as H` | honest |
| Fixture collect + offline | `--backend offline --eval-mode fixture` | H `(1,8)`, `weight_source=offline_prefix_ids` | **not** scientific collect (ND-05) |
| Official+self_authored | `Task.from_dict` with `source_kind=official` on fixture body | `Self-authored fixtures cannot be marked official` | not a swap |
| `p1_incremental` no held-out | direct call | `status=requires_held_out` | honest |
| Helper empty-N evaluated | `dependency_densities(..., noise_set=[], noise_evaluated=True)` | `rho_M_noise=1.0`, `rho_M_excess=-0.5` | unused by prepare/label (ND-06) |

Not run (out of this machine / not required for the named hunts): real HF weights, official iGSM 500, GPU intervene/repair, server collect, full Plus persist two-process lock.

## 4. Paper-paragraph coverage (omissions vs swaps)

Empty “looks implemented” is not a pass. Below is the paper map. Background, related-work, schedule, and untested numeric forecasts are not code requirements.

| paper locus | requirement | this tree | status |
|---|---|---|---|
| §2.2 / §4.1 | Natural generate + identity align; fixture ≠ official | Fixture loader refuses `official`. Scientific generate is tiny + teacher-force `\nq = `, labeled `constrained_target`. | **non-defect** if not claimed as MODEL-01 / §4.1 (ND-01). |
| §2.3 | \(R^{val}\) vs \(R^{surf}\); structure separate | `surface_mentions` stored; structure via align `removed/merged` | present as schema |
| §2.4 / §6 / Goal §5.10 | Source–value decoupling: read \(a\) vs \(b\), first \(a=b\) | `apply_alt_source_same_value` keeps leaf \(a\), adds equal-value `src_b`, retargets so \(q\) reads \(b\) not \(a\) (XOR). Distinct from `apply_rename_edit` (drops \(a\)). | **named hunt 1 not reproduced** |
| §2.4 IE / swap | \(H'=H_b+\Pi_Z(H_d-H_b)\); C-rand / C-layer | `apply_swap`, `c_rand_delta`, `c_layer_delta` exist; live C-layer stays `dev_scores_missing` without a dev curve | tools present; no fake C-layer decode |
| §2.5 Prop 1–2, cone | over-approx protocol; conformal ceil((N+1)(1-α)) | `dirty_cone`, `conformal_threshold`, `joint_edit_counterexample` | formulas present; not evaluated on real traces |
| §2.6 / §3 | \(S=B\setminus T\), \(M=T\setminus B\); unknown ≠ negative; noise matched or null | unknown → `behavior_unknown`, `rho_M_raw=None`; sham / noise_ref=0 without mapped hits → excess null | **hunts 2–4 not reproduced** |
| §3 TO/CSP | LCS TO; matched CSP; empty denom N/A | `preservation_to_csp`, `lcs_overlap` | present |
| §4.2 bilinear / MLP-256 | \(h^\top UV^\top e+b\), \(r=64\); Hidden=256 | `BilinearProbe`, `BoundaryMLP` | form present; CLI boundary fit is all-ones / no negatives (NS-02) |
| §5 Fig. 2 three positions | pre-step / pre-value / post-step | collect writes `H_pre_step`, `H_pre_value`, `H_post_step` on tiny | present on tiny |
| §7 T1–T4 | official iGSM + GSM-Symbolic/Plus + Hotpot/MuSiQue/HumanEval + T4 | adapters exist; graphs unknown/partial where required | **pending_server** for real dumps |
| §7 T2-noop | front/mid/back × surface; not official NoOp | `make_noop_pair`, `official_noop_release=False` | present |
| §8 / Goal §5.7 / VERB-01 / ATTN-01 | four-tier verbalizer + attention/rollout | library in `baselines.py`; scientific fit **refuses** fake scores; fixture fit still writes toys | honest refuse on scientific path (ND-02); fixture toys must not become Fig. 5 (NS-01) |
| §8 / Goal §5.14 | Gate 0–2 unregistered ≠ pass | `week8_decision` → `unregistered`; `scientific_conclusion=None` | **non-defect** ND-03 |
| Goal §5.8 / §2.5 | P1 held-out length+op vs +ρ; no fake P1 | no held-out → `requires_held_out` | **non-defect** ND-04 |
| MODEL-01 | frozen Qwen3 / R1-Distill HF | cards + `load_frozen`; local path is random tiny | **pending_server**; tiny ≠ MODEL-01 (ND-01) |
| Goal §5.6 / collect | scientific H is model hidden states | scientific+non-tiny raises; fixture offline writes 8-id prefix | **non-defect** ND-05 |
| Ancestor tasks.jsonl | must not bind E from parent extras | `_find_tasks_jsonl` only inspects given stage dirs | **hunt 5 not reproduced** |

## 5. Named hunts (independent)

### 5.1 Hunt 1 — `same_value_diff_source` vs rename (XOR `src_b`)

Direct `apply_alt_source_same_value(task, "p2")` vs `apply_rename_edit(task, {"p2": "src_b"})` on `t1_tiny`:

| | base | `same_value_diff_source` | `apply_rename_edit({p2: src_b})` |
|---|---|---|---|
| premises | `p1=4`, `p2=0` | `p1=4`, `p2=0`, `src_b=0` | `p1=4`, `src_b=0` |
| \(q\) parents | `{p1,p2}` | `{p1,src_b}` | `{p1,src_b}` |
| expression | `p1 * p2` | `p1 * src_b` | `p1 * src_b` |
| answer | `0` | `0` | `0` |
| \(R_{\mathrm{task}}(q)\) | `{p1,p2}` | `{p1,src_b}` | `{p1,src_b}` |
| keeps leaf \(a\) (`p2`) | yes | **yes** | **no (dropped)** |

Guards in `apply_alt_source_same_value` (L268–275): parents must change; value unchanged; `p2` still in \(P\); `src_b` in parents; `p2` not in parents.

This is **not** rename-only. Same *target parents* as a rename of \(a\to b\) is what XOR retargeting *is*: the graph must read \(b\) not \(a\). The defect condition is drop-\(a\) / the whole object being a rename. Here \(P\) differs: `{p1,p2,src_b}` vs `{p1,src_b}`.

Scientific `edits.jsonl` `source_value_pair` writes the same XOR graph (`premises=['p1','p2','src_b']`, parents `['p1','src_b']`, `trace-source`). Collect copies `edits.jsonl`. Intervene `donor_kind=same_value_diff_source`, `donor_rows=[0,3]`.

**A13-01 / hunt 1 not reproduced on this freeze.**

### 5.2 Hunt 2 — unknown behavior must not become \(M\)

`build_labels`: non-exhaustive `no_change` → `behavior=None`, `behavior_known=False`. `event_density_sets` sets `behavior_unknown` if no known behavior or \(T\nsubseteq\) known. `dependency_densities` then forces \(M=\emptyset\), `rho_M_raw=None`.

Direct non-exhaustive `no_change` on `{p1,p2}`: `M=[]`, `rho_M_raw=None`, `behavior_unknown=True`. Exhaustive known negatives: `rho_M_raw=1.0`, \(M=\{p1,p2\}\) — a **known** miss, not unknown-as-negative.

Scientific prepare labels: `p1`/`p2` `behavior_label=None`, `behavior_known=False`; densities `rho_M_raw=null`, `M=[]`, `behavior_unknown=true`. Fit behavior head: `no_known_labels`. **Not reproduced.**

### 5.3 Hunt 3 — `sham:` row → noise_set missing, not evaluated empty \(N\)

`event_density_sets` L349–351: any `sham:` row or sham hit → `noise_set=None`, `evaluated=False` → `null_reason=noise_set_missing`, all excess null.

Direct sham `no_change` (`noise_ref=0` on `sham:q`): excess null. Direct sham `changed` (`noise_ref=1`): excess still null; real \(M\) may still be computed from *behavior* labels, but noise/excess stay null.

Live scientific prepare: `sham:q` changed `['82','53']`, `noise_ref=1.0`; densities `null_reason=noise_set_missing`, all excess null. **Not reproduced.**

### 5.4 Hunt 4 — real premises `noise_ref=0`, no `sham:` row

Constructed labels: `p1`/`p2` with `noise_ref=0.0`, no `sham:` row, sham protocol present. `event_density_sets`: observed (0 is not None), no `real_hits` (`noise_ref==1.0` required), else-branch `noise_set=None`, `evaluated=False` → excess **null**, `noise_set_missing`. Same on the no-`event_id` fallback.

This is **not** booked as evaluated \(N=\emptyset\). Excess is null, not raw.

The public helper `dependency_densities(..., noise_set=[], noise_evaluated=True)` still writes `rho_M_noise=1.0`, `rho_M_excess=-0.5`. Prepare/label/`event_density_sets` do not take that branch. Residue only (ND-06). **Hunt 4 not reproduced.**

### 5.5 Hunt 5 — `_find_tasks_jsonl` must not walk ancestor extras

Source L703–711: only `Path(folder) / "tasks.jsonl"` for directories it was given. No parent walk, no rglob.

Isolated `deep/x/feat` + `deep/x/labs` (features/labels copied, no `tasks.jsonl`); WRONG-TASK planted in `deep/col/tasks.jsonl`. `_find_tasks_jsonl(feat, labs)` is `None`. `fit --in-dir feat --labels-dir labs --eval-mode scientific` raises `fit requires tasks.jsonl so E columns follow task.premises, not label order`. Ancestor file was not consulted.

`_e_premise_ids` still **appends** leftover non-sham label ids (`['p1','p2','leftover']`). Live scientific E is `(2, 32)` from `task.premises`; extras past `e.shape[0]` are skipped. Residue (ND-07). **A12-03 not reproduced.**

### 5.6 Hunt 6 — scientific fit must not invent §8 scores

Scientific `probes.jsonl`:

- `verbalizer` / `attention_mean` / `attention_rollout` / `attention_threshold` → `status=refused_not_section8` (reasons: no dependency-label verbalizer on this prefix; no attention maps).
- No `score=0`, no prefix echo, no `fit_attention_threshold([0.1,0.9], …)`.

**Refuse is honest on this path:** tiny teacher-force `\nq=` is not a §8 verbalizer of dependencies, and tiny collect does not write attention maps. Inventing Fig. 5 numbers would be the defect.

The **library** (`baselines.verbalizer`, `attention_mean`, `attention_rollout`, `fit_attention_threshold`) exists (Goal §5.7 / VERB-01 / ATTN-01 / BASE-01). Scientific CLI refuses to emit toy numbers. That is not a missing function; it is a missing *real* §8 run (**pending_server**). Fixture-mode fit still writes echo verbalizer + `[0.1,0.9]` (NS-01). Do not copy either path into Fig. 5.

Boundary MLP on scientific fit still trains all-ones with note `event-rows-only_no_negatives`. That is a §4.2 stub, not a fake §8 verbalizer score (NS-02).

### 5.7 Hunt 7 — teacher-force `\nq=` is honest `constrained_target`

`append_target_assignment` docstring: “Teacher-force `\\n{target} = ` then sample digits from model logits. Not gold values.” Scientific prepare (`weight_seed=0`) produced 7 traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value-edit traces, `trace-sham`. Every one has `parse_status=constrained_target`, `parse_region=generated`, `weight_source=random_init`, `target_assignment` `\nq = 82` or `\nq = 53`. Events are a single generated-region `q = ##`. `run_spec.source_kinds` is `{t1_tiny.json: fixture}`.

This is **honest `constrained_target`**. It is **not** MODEL-01 and **not** paper §4.1 natural CoT. This review does not require inventing natural CoT. Do not file this path as §4.1 / C1 / MODEL-01 evidence.

### 5.8 Hunt 8 — unregistered gates / tiny / offline prefix

- `week8_decision({})`: all three gates `decision=unregistered`, `scientific_conclusion=None`, `skip_p2_p3=true`, `status=not_evaluated`. **Not a pass. Not a defect.**
- Scientific collect: `weight_source=random_init`, `hidden_layer=1`, tiny 32-d. **tiny ≠ MODEL-01.**
- Scientific + `--backend offline` raises `scientific collect refuses offline_prefix_ids as H`.
- Fixture + `--backend offline` writes H `(1,8)` from `token_ids[:8]`, `weight_source=offline_prefix_ids`. **That is not scientific collect.**

## 6. Findings

No **confirmed defect** on this freeze for the named paper hunts.

### A13-01 — Rename-of-leaf claimed as source–value decoupling

| field | value |
|---|---|
| **ID** | A13-01 |
| **Severity** | — |
| **Status** | **not reproduced** on this freeze |
| **Evidence** | `edits.py` `apply_alt_source_same_value` L219–292 keeps \(a\), adds `src_b` with equal value, retargets parents/expr so \(q\) reads \(b\) not \(a\). Rename of the same leaf **drops** \(a\). Scientific pair + intervene donor preference use that XOR graph. Same parent *set* as rename is the XOR edge rewrite, not drop-\(a\). |

### A13-02 — Unknown / unscanned as \(M\)

| field | value |
|---|---|
| **ID** | A13-02 |
| **Severity** | — |
| **Status** | **not reproduced** |
| **Evidence** | `measure.py` L48–53 / L123 / L369: unknown → `behavior_unknown`, \(M=\emptyset\), `rho_M_raw=None`. Direct and scientific prepare agree. |

### A13-03 — Sham books empty \(N\)

| field | value |
|---|---|
| **ID** | A13-03 |
| **Severity** | — |
| **Status** | **not reproduced** |
| **Evidence** | Sham rows force `noise_set=None`. Live scientific sham changed `82` vs `53`; excess null; `null_reason=noise_set_missing`. |

### A14-04 — Real `noise_ref=0` books evaluated empty \(N\)

| field | value |
|---|---|
| **ID** | A14-04 |
| **Severity** | — |
| **Status** | **not reproduced** |
| **Evidence** | Real premises with `noise_ref=0` and no `sham:` row → excess null, not raw. |

### A12-03 — Ancestor WRONG-TASK binds E

| field | value |
|---|---|
| **ID** | A12-03 |
| **Severity** | — |
| **Status** | **not reproduced** |
| **Evidence** | `_find_tasks_jsonl` does not walk parents. Isolated feat/labs refuse fit. |

### Non-defects, doubts, suggestions

**ND-01 (non-defect).** Teacher-forced `\nq=` is labeled `constrained_target`. Not §4.1, not MODEL-01. Tiny random weights. REQUIREMENTS `MODEL-01 implemented_local_tiny` is an author claim.

**ND-02 (non-defect).** Scientific fit refuses §8 toys (`refused_not_section8`). Honest: no attention maps, no dependency verbalizer on this prefix. Library functions exist. Real Fig. 5 is **pending_server**, not a silent missing baseline on this path.

**ND-03 (non-defect).** Gate 0–2 stay `unregistered`. No pass/fail.

**ND-04 (non-defect).** P1 is not inferred from labels. Held-out is required.

**ND-05 (non-defect).** Fixture 8-id offline prefix H is not scientific collect. Scientific collect refuses that backend.

**ND-06 (non-defect residue).** `dependency_densities(..., noise_set=[], noise_evaluated=True)` still deducts empty \(N\). Live prepare/label do not call that branch.

**ND-07 (non-defect residue).** `_e_premise_ids` still appends leftover label ids. Live scientific E follows `task.premises` (2 columns).

**NS-01 (non-defect suggestion).** Fixture-mode `fit` still echoes the prefix and fits `attention_threshold` on `[0.1,0.9]`. Do not write Fig. 5 / §8 from that blob.

**NS-02 (non-defect suggestion).** CLI `BoundaryMLP` on all-ones event rows (`event-rows-only_no_negatives`) is a stub. Do not write §4.2 F1 from it.

**NS-03 (non-defect suggestion / unconfirmed for C2 scoring).** Intervene prefers the equal-value XOR donor then scores by **answer equality**. Paper §6 uses \(a=b\) to *construct* the pair and \(a\neq b\) to *evaluate* source-follow. On this run both base and source traces have the same constrained-target digits (`82`); decoded tiny answer was `9`. `target=0.0` is not a paper source-follow matrix. `clayer_status=dev_scores_missing` is honest. Do not copy these numbers into Fig. 3.

**NS-04 (author-ledger mismatch, not a code defect).** Executable CAUSAL-02 construction rows (e.g. TR-0158) point at `intervention_report`. The constructor is `apply_alt_source_same_value`. Ledger status `implemented_local` is an author claim.

**pending_server.** Official iGSM 500 / real GSM-Plus+Symbolic dumps / frozen Qwen3-8B and R1-Distill-Qwen-7B / GPU swap-ablate-rescue / real P1–P3 / real §8 attention maps and supervised verbalizer. Missing **code** is not hiding in this list: adapters, tiny hooks, and CLI stages exist. Missing **weights/data** are external.

## 7. Scientific pipeline snapshot (`t1_tiny`, weight_seed=0)

Scratch: `.planning/audits/round-17/_a_scratch/{prep,col,fit,int}` (not production).

- Traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value edits, `trace-sham`.
- Split: `fix-t1-001` → `probe_train` (hash of this fixture family; not official).
- Events: one generated-region `q = ##` each; `parse_status=constrained_target`.
- Pair: `same_value_diff_source` premises `{p1,p2,src_b}`, parents `{p1,src_b}`, expression `p1 * src_b`.
- H: finite `(7,32)`; E finite `(2,32)` from **base** `task.premises` (not `src_b`); three position arrays present; `weight_source=random_init`.
- Sham: `sham:q`, changed `82` vs `53`; `noise_ref=1.0`; excess null.
- Densities: `rho_S_raw=null` (empty \(P\setminus T\)), `rho_M_raw=null`, excess null, `behavior_unknown=true`, `null_reason=noise_set_missing`.
- Fit: task head trained; behavior head `no_known_labels`; §8 rows `refused_not_section8`.
- Intervene: `donor_kind=same_value_diff_source` `[0,3]`; norms matched; C-layer not decoded without dev scores.

## 8. Verdict

**PASS**

Hash matches. Named hunts 1–5 did **not** reproduce on this freeze: XOR `src_b` keeps \(a\); unknown is not \(M\); `sham:` and `noise_ref=0` without a mapped hit do not book evaluated empty \(N\); `_find_tasks_jsonl` does not walk ancestors. Scientific fit refuses fake §8 scores (honest refuse, not invented zeros/echo/`[0.1,0.9]`). Teacher-force is honest `constrained_target` and is not §4.1 / MODEL-01. Unregistered gates, tiny ≠ MODEL-01, and fixture 8-id prefix H are not defects.

Pytest 160 passed is not paper correctness. This channel does **not** declare Goal complete. `consecutive_pass_count` cannot start from a single channel. Real MODEL-01 / official dumps / Fig. 3–5 remain **pending_server**.
