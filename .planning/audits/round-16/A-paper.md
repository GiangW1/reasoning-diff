# Round-16 Reviewer A — Paper consistency

- **Agent:** Cursor Grok 4.6 (independent channel A subagent). No parent-assigned reviewer id.
- **Time:** 2026-09-21 (Asia/Shanghai).
- **Repo:** `C:\Users\22688\Desktop\diff`
- **Declared freeze:** `.planning/audits/round-16/VERSION.md`
- **Declared hash:** `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` (61 files)
- **ISSUES.md:** author claims only; not treated as closed
- **Other round-16 A–F reports:** not read, not used as evidence
- **Prior-round A–F files:** format only; not used as evidence
- **Production tree:** report-only; `src/`, `tests/`, `pyproject.toml` not edited

## 0. Freeze hash

Method: exact `VERSION.md` script (POSIX relpath + NUL + bytes over `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`).

| | SHA-256 | files |
|---|---|---|
| **Declared** | `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` | 61 |
| **This reviewer, first recompute (open)** | `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` | 61 |
| **This reviewer, mid-session recompute** | `3d0a076481863eefea311428271cfba76c3d4bd9c6ceee682dd97211f6fdfbc6` | 61 |
| **This reviewer, closing recompute** | `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f` | 61 |

**HASH_MISMATCH.** Automatic **FAIL**.

This channel did not write `src/`, `tests/`, or `pyproject.toml`. Observed motion after the opening match:

| path | first read (while open hash still matched) | later / close |
|---|---|---|
| `src/reasoning_diff/edits.py` | 362 lines; `apply_alt_source_same_value` drops `p2`, adds `p2_src`, rewrites `q = p1 * p2_src` | 365 / `1e5b97d63a62ab78…`; keeps `p2`, adds `src_b`, retargets `q = p1 * src_b` |
| `src/reasoning_diff/measure.py` | 408 lines; sham row → `noise_set=None`; leftover `else` booked `N=[]` / `evaluated=True` | 405 / `985b9d9328e4111f…`; leftover `else` now `noise_set=None` |
| `src/reasoning_diff/models/generate.py` | 201 lines; no `cap=48`; refuse if `len(prompt_ids)>96` | 200 / `6e6040394ac641c7…`; same refuse, full `prompt_text` |
| `src/reasoning_diff/cli.py` | scientific fit already `refused_not_section8`; `_find_tasks_jsonl` only given dirs | 1259 then 1260 / `9431b7768fda6a3c…` |

git_head in VERSION (`46a6e26da8637fe29d9f8f0667cb4e513538a59d`) was not used as the freeze object. Working tree dirty; production files are untracked.

Paper SHA-256 (required): `f3c0ec087b5bf4e503db35f4d234c727df3ce66f933e80781c69a0cc312ea57c` — **MATCH** declared `F3C0EC08…`. Size 51935 bytes. Title `Reasoning-Diff-修订方案-v3 (1).md`.

Pytest author claim in VERSION: 159 passed. This reviewer: `python -m pytest -q --tb=line` → **160 passed / 23.16s / exit 0**. Green is not paper-correct. The extra test vs the author claim is further evidence the freeze object is not a stable byte set.

## 1. File coverage

Digests below are **closing-tree** SHA-256 unless noted. “Read” is what this channel actually opened.

### Required documents

| path | lines / bytes | digest | what was read |
|---|---|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 517 / 51935 B | `f3c0ec08…` MATCH | full: C1–C4, §2.1–2.6, §3, §4.1 pipeline, §5–§8 (source–value, verbalizer), Week-8 / Gates / §12 |
| `docs/EXPERIMENT_PROTOCOL.md` | 86 | — | full: scope, labels, splits, intervention conditions, P1–P3, Gate 0–2 unregistered |
| `docs/CURSOR_GOAL_PROMPT.md` | §5 (file 166) | — | §5 items 1–15 (truth, events, noise, splits, baselines, causal, C3, gates) |
| `.planning/REQUIREMENTS.md` | 76 | — | full v1 + paper atomics + author status column (claims, not closures) |
| `.planning/audits/round-16/VERSION.md` | 28 | — | declared hash, method, pytest claim, D14-05 prior note |

### `src/reasoning_diff/**/*.py` (closing tree unless noted)

| path | lines | digest16 | what was read |
|---|---|---|---|
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58d` | full |
| `src/reasoning_diff/__main__.py` | 4 | `307299fda7b77d22` | full |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63b` | full: `p1_incremental`, `week8_decision`, forbidden claims |
| `src/reasoning_diff/artifacts.py` | 85 | `524657027e9b402f` | full |
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4` | full: `verbalizer`, `attention_*` |
| `src/reasoning_diff/cli.py` | 1260 | `9431b7768fda6a3c` | full in chunks: prepare/collect/label/fit/analyze; `_find_tasks_jsonl`; `_pair_source_value`; scientific verbalizer refuse |
| `src/reasoning_diff/edits.py` | 365 | `1e5b97d63a62ab78` | full, twice. Open read was 362-line drop-`a` / `p2_src` rename |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814` | full |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78` | full |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277` | full |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649` | full |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd3` | full |
| `src/reasoning_diff/measure.py` | 405 | `985b9d9328e4111f` | full, twice. Open read booked empty `N` in the leftover `else` |
| `src/reasoning_diff/models/__init__.py` | 1 | `0b7dd6c4dd852065` | full |
| `src/reasoning_diff/models/adapters.py` | 42 | `c1992624026a1bf0` | full |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20` | full; hidden `[:max_position_embeddings]`, not the 48-char prompt cap |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185ae` | full |
| `src/reasoning_diff/models/generate.py` | 200 | `6e6040394ac641c7` | full: `append_target_assignment`, `generate_task_trace` |
| `src/reasoning_diff/models/tiny.py` | 120 | `c75d0f5325766612` | full |
| `src/reasoning_diff/models/tokenize.py` | 31 | `b0cc8974af1010fa` | full |
| `src/reasoning_diff/probes/__init__.py` | 3 | `3065196db28e929c` | full |
| `src/reasoning_diff/probes/bilinear.py` | 101 | `b34ea3e5a1e2e1ec` | full |
| `src/reasoning_diff/probes/boundary.py` | 44 | `ce3b549be7d671ff` | full |
| `src/reasoning_diff/probes/calibrate.py` | 45 | `e8b3ed3459bb22c5` | full |
| `src/reasoning_diff/repair.py` | 232 | `f76ff9998b9a6b17` | full |
| `src/reasoning_diff/rng.py` | 53 | `2098c2c72a852eaa` | full |
| `src/reasoning_diff/schema.py` | 385 | `57c69c6f58cc9a45` | full |
| `src/reasoning_diff/scoring.py` | 30 | `8a7a3c0777240122` | full |
| `src/reasoning_diff/splits.py` | 184 | `40ab4021d4dccc6e` | full: persist lock, `TEST_ONLY_SOURCES` |
| `src/reasoning_diff/tasks/__init__.py` | 1 | `4df493e2a536a4c3` | full |
| `src/reasoning_diff/tasks/catalog.py` | 45 | `bcc83ec636ad207b` | full |
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d` | full: 500 / op∈{5,10,15,21} / mod 23 |
| `src/reasoning_diff/tasks/t1_fixture.py` | 20 | `01b6748804316fb3` | full: refuses non-fixture |
| `src/reasoning_diff/tasks/t1_official.py` | 92 | `5c1432f736969031` | full: official snapshot, template not `G` |
| `src/reasoning_diff/tasks/t2_gsm_plus.py` | 84 | `493108ae857b7b6f` | full |
| `src/reasoning_diff/tasks/t2_gsm_symbolic.py` | 85 | `c588d60fafb30354` | full |
| `src/reasoning_diff/tasks/t2_noop.py` | 100 | `850f779c81d56149` | full |
| `src/reasoning_diff/tasks/t3_hotpot.py` | 104 | `f6769cd49dd623fb` | full |
| `src/reasoning_diff/tasks/t3_humaneval.py` | 78 | `f39cff590b21adc7` | full |
| `src/reasoning_diff/tasks/t3_musique.py` | 110 | `b3f79e2c466a28c0` | full |
| `src/reasoning_diff/tasks/t4_boundary.py` | 51 | `e4b34f3697825f88` | full |
| `src/reasoning_diff/transfer.py` | 86 | `5549f84bd1bd6240` | full |

`tests/**/*.py` were executed via pytest, not line-audited as paper text. Fixture `tests/fixtures/t1_tiny.json` was loaded (`source_kind=fixture`, `p1=4`, `p2=0`, `q=p1*p2`).

## 2. Checks run

| check | command / object | result |
|---|---|---|
| Freeze hash (VERSION script) | open + mid + close | open MATCH `5413a4bc…`; mid `3d0a0764…`; close **MISMATCH** `3d0f1c10…` |
| Paper SHA-256 | `Reasoning-Diff-修订方案-v3 (1).md` | `f3c0ec08…` MATCH |
| pytest | `python -m pytest -q --tb=line` | 160 passed / 23.16s / exit 0. Not paper-correct |
| A13-01 library | `make_source_value_pair` vs `apply_rename_edit` on `t1_tiny` | **live (unbound):** keep `p2`, add `src_b`, parents `{p1,src_b}`, not rename-isomorphic. **open read (freeze window):** drop `p2`, add `p2_src` — rename |
| A13-02 library | `build_labels` non-exhaustive `no_change`; `event_density_sets`; `behavior_unknown=True` | `M=[]`, `rho_M_raw=null`. Known exhaustive miss still `M={p1,p2}`, `rho_M_raw=1.0` |
| A13-03 library | sham `no_change` / `changed`; leftover observed-without-sham-row | sham excess **null** (`noise_set_missing`). Leftover live also null |
| A12-03 | deep `feat/` without `tasks.jsonl`; ancestor `col/tasks.jsonl` swapped `[p2,p1]` | `_find_tasks_jsonl(feat) is None`; `cmd_fit` **raises** `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order` |
| D14-05 | `generate_task_trace` on live source pair + reconstructed `p2_src` rename | no `cap=48`; live `prompt_text` is full 49-char `… * src_b?`; rename reconstruction contains full `* p2_src` (44 chars) |
| Scientific prepare | `reasoning_diff prepare --fixture tests/fixtures/t1_tiny.json --eval-mode scientific --split-fractions 0.40 0.15 0.10 0.10 0.10 0.15 --sham-opportunities 1 --weight-seed 0` | rc 0. Artifacts under `.planning/audits/round-16/_a_sci_run/prep` |
| Scientific collect | collect `--backend tiny --weight-seed 0` | rc 0. `H` (7,32) all finite; `E` (2,32) all finite; three position arrays present |
| Scientific label | label on prepare dir | rc 0. `behavior_unknown`, `M=[]`, `rho_M_raw=null`, excess null |
| Scientific fit | fit `--split probe_train --eval-mode scientific` | rc 0. Task head loss 0.050; behavior `no_known_labels`; verbalizer/attention `refused_not_section8` |
| Analyze (no `p1_table`) | analyze on prep | `p1=null`, `scientific_conclusion=null`, Gate 0–2 `unregistered` |
| Fixture ≠ official | `load_t1_fixture`; `load_igsm_snapshot(..., official)` on `t1_tiny` | fixture loads; official path `KeyError: 'template'` |

Scientific-run inspection (live tree; not the declared freeze):

- Seven traces: `trace-base`, `trace-t0p`, `trace-edit`, `trace-source`, two extra value edits, `trace-sham`.
- Every collected trace: `parse_status=constrained_target`, `parse_region=generated`, `weight_source=random_init`. `target_assignment` is teacher-forced `\nq = ` then two sampled digits (base `82`, t0p `53`, source `82`, sham `53`).
- `source_kind=fixture`. Source pair: premises `[p1,p2,src_b]`, parents `[p1,src_b]`, expression `p1 * src_b`, answer `0`. `prompt_text` = `p1 = 4. p2 = 0 src_b = 0. What is q = p1 * src_b?` (49 chars; not 48-truncated).
- Sham: `premise_id=sham:q`, `noise_ref=1.0`. Real premises `behavior_label=None`, `behavior_known=False`. Densities: `behavior_unknown=true`, `M=[]`, `rho_M_raw=null`, `null_reason=noise_set_missing`.
- Fit verbalizer/attention rows are refused as not §8. Do not treat the refused keys as Fig. 5.

## 3. Findings

### A16-01 — Freeze hash mismatch

- **Severity:** blocker
- **File / symbol / line:** `.planning/audits/round-16/VERSION.md` vs live `src/reasoning_diff/{edits,measure,cli,models/generate}.py` (and tests: author 159 → this run 160)
- **Trigger:** VERSION freeze object is not the tree under review at close
- **Paper / protocol req:** audit contract — reviewers bind a frozen byte set. Mismatch means paper claims cannot be attributed to the declared hash
- **Repro:** run the VERSION.md Python block. Declared `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc`; live `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`
- **Impact:** any “closed on 5413a4bc…” statement is unbound. Mid-review patches (including the A13-01 rewrite from `p2_src` to `src_b`) cannot be written back onto this freeze
- **Fix:** stop edits; re-freeze; restart the round
- **Status:** confirmed defect

### A13-01 — Opening freeze `same_value_diff_source` is a rename, not paper *a* vs *b*

- **Severity:** high
- **Status:** confirmed defect **on the declared-freeze window** (first read of `edits.py` while the opening hash still matched). Live tree after mid-review rewrite is **unbound** and is not this freeze.
- **File / symbol / line:** `edits.py` `apply_alt_source_same_value`. Open freeze: drop original leaf, `new_id=f"{premise_id}_src"`, rewrite expression/parents via the same ID map as `apply_rename_edit`. Close (unbound): `new_id="src_b"`, keep `a`, add `b`, retarget.
- **Trigger:** paper §6 / results §5 (ll. 304–307), §2.4, Goal §5.10, CAUSAL-02: “目标计算分别要求读取 *a* 或 *b*，先令 *a=b*”. Rename of one leaf is not a second source.
- **Repro (open read):** `apply_alt_source_same_value` removed `p2` from premises, appended `p2_src`, mapped parents `{p1,p2}→{p1,p2_src}` and expression `p1 * p2` → `p1 * p2_src`. The `_target_parents(swapped)==_target_parents(task)` check only tests that ID **strings** changed — tautological for a rename. That object is isomorphic to `apply_rename_edit(..., {"p2":"p2_src"})`.
- **Repro (live, unbound, not credited):** `make_source_value_pair(t1_tiny,"p2","2")` now keeps `p2`, adds `src_b=0`, parents `{p1,src_b}`, expression `p1 * src_b`, answer still `0`. `set(alt.parents)!=set(rename.parents)`. `isomorphic_to_rename=False`. Scientific `trace-source` uses that graph. This is closer to “keep *a*, read *b*” but **cannot close A13-01 on 5413a4bc**.
- **Impact:** C2 source–value donors on the declared freeze are a relabel of the same leaf. Source-follow on that pair does not test “which premise was read”.
- **Fix:** stop edits; re-freeze the keep-*a*/add-*b* construction (or a two-existing-premise *a=b* pair) and re-review that hash.

---

### Hunt closures that are **not** defects

These were independently reproduced. They do **not** start a consecutive-pass count, because the freeze identity is gone.

#### ND-01 — Teacher-forced `\nq=` is honest `constrained_target`

- **Status:** non-defect
- `generate.py` `append_target_assignment` docstring: “Not gold values.” `generate_task_trace` sets `parse_status=constrained_target` when the assignment falls after free decode. All seven scientific traces carry that flag + `weight_source=random_init` + `tiny-qwen2`. This is **not** MODEL-01 and **not** paper §4.1 natural CoT. Do not require inventing CoT. Do not allow anyone to file this path as §4.1 / C1 evidence.

#### ND-02 — A13-02 unknown is not written into *M* (live + scientific)

- **Status:** non-defect on the paths run (cannot bind to 5413a4bc)
- `dependency_densities`: `M=[]` and `rho_M_raw=null` when `behavior_unknown`. `event_density_sets` sets that flag when no known behavior on the task set. Scientific labels: `q/p1` and `q/p2` have `behavior_label=None`; densities `M=[]`, `rho_M_raw=null`. Direct known exhaustive miss still records `M={p1,p2}`. Fit behavior head: `no_known_labels`.

#### ND-03 — A13-03 sham empty *N* is not deducted

- **Status:** non-defect on the paths run (cannot bind to 5413a4bc)
- Sham row present → `noise_set=None`, `evaluated=False` → excess null (`noise_set_missing`), change or no-change. Scientific sham `82` vs `53` → `noise_ref=1.0` on `sham:q` only; real premises `noise_ref=None`; excess null. Live leftover (protocol set, no sham row, observed `noise_ref` on reals) also nulls. Open-freeze leftover `else` that booked `N=[]`/`evaluated=True` is **not** the sham hunt and is in any case unbound.

#### ND-04 — A12-03 ancestor `col/tasks.jsonl` is not bound

- **Status:** non-defect (independently confirmed on live helper/CLI)
- `_find_tasks_jsonl` searches only the given stage directories. Deep `feat/` without its own `tasks.jsonl`, ancestor `col/tasks.jsonl` with premises swapped `[p2,p1]`: helper returns `None`; `cmd_fit` **raises**; *E* is not `[p2,p1]`.

#### ND-05 — D14-05 no 48-char prompt cap; full expression kept

- **Status:** non-defect on generate (cannot bind to 5413a4bc)
- `generate_task_trace` has no `cap=48`. It stores the full `task.question` as `prompt_text` and raises if `len(prompt_ids)>96`. Live source `prompt_text` contains the full current expression `* src_b` (49 chars). A rename reconstruction `p2→p2_src` still contains full `* p2_src` (44 chars) and is not clipped to 48. The hunt literal `* p2_src` is absent from the **live** source pair because the (unbound) A13-01 rewrite renamed the new leaf to `src_b`, not because of truncation.

#### ND-06 — Fixture is not official

- **Status:** non-defect
- `t1_tiny.json` `source_kind=fixture`. `load_t1_fixture` refuses non-fixture. `load_igsm_snapshot(t1_tiny, official)` raises `KeyError: 'template'`. Official 500-grid remains `pending_server`.

#### ND-07 — Gate 0–2 unregistered is not a pass

- **Status:** non-defect
- Analyze report: `gates.gate0/1/2.decision=unregistered`, `scientific_conclusion=None`, week8 `status=not_evaluated`. Protocol §6 and GOAL §5.14 require this.

#### ND-08 — Analyze does not invent P1

- **Status:** non-defect
- `cmd_analyze` sets `p1` only from `p1_table.jsonl`. Without it, report `p1=null`.

#### ND-09 — Leftover first-seen append is residual, not the A12-03 bind

- **Status:** non-defect suggestion
- `_e_premise_ids` still appends leftover non-sham label IDs after `task.premises`. Without a task, order is first-seen (`['p2','p1','extra']`). Fit will not use that path when labels exist and `tasks.jsonl` is missing (raises).

#### ND-10 — Scientific fit does not write fake §8 verbalizer/attention scores

- **Status:** non-defect on the live CLI path (not a named hunt; not a freeze closure)
- Scientific `cmd_fit` appends `refused_not_section8` rows instead of prefix-echo scores. Do not write Fig. 5 / §8 from that blob. Boundary MLP note `event-rows-only_no_negatives` remains a stub.

#### pending_server

Official iGSM 500 / op grid, Qwen3-8B / R1-Distill weights (MODEL-01), natural long CoT, Gate thresholds, held-out P1 table, C-rand/C-layer on real donors: not present as executed science. Tiny `random_init` and `constrained_target` are labeled as such. Do not write them into a scientific conclusion (analyze already writes `scientific_conclusion=None`).

## 4. Verdict

**FAIL.**

Reasons (the first is enough):

1. **HASH_MISMATCH** — declared `5413a4bc65f4b0a6bda1b98eeb25a1c64643d89ef415b8e4ce32e07e97e661fc` vs closing `3d0f1c1025d501509a88023df5f14fe32392c38f28657fed2cb906bdb7c0952f`
2. **A13-01** confirmed on the opening-freeze read: source–value “pair” dropped `a` and renamed it to `p2_src`. The later keep-*a*/add-`src_b` rewrite is mid-review and unbound.

Empty “looks fine” is not available. Consecutive-pass count cannot start on this freeze.

Teacher-force `\nq=` remains an honest local interface (`constrained_target`). It is not a defect and it is not §4.1 / MODEL-01.
