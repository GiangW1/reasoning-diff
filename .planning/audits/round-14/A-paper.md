# Round-14 Reviewer A — Paper consistency

- **Agent:** unknown (independent subagent; channel A)
- **Time:** 2026-09-21
- **Repo:** `C:\Users\22688\Desktop\diff`
- **Declared freeze:** `.planning/audits/round-14/VERSION.md`
- **git_head (VERSION claim):** `46a6e26da8637fe29d9f8f0667cb4e513538a59d` (working tree dirty; not used as the freeze object)
- **ISSUES.md:** author claims only; not treated as closed
- **Other A–F reports:** not used as evidence
- **Production tree:** report-only; `src/`, `tests/`, `pyproject.toml` not edited

## 0. Freeze hash

Method: exact `VERSION.md` script (POSIX relpath + NUL + bytes over `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml`, exclude `__pycache__`).

| | SHA-256 | files |
|---|---|---|
| **Declared** | `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637` | 61 |
| **This reviewer, first recompute (open)** | `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637` | 61 |
| **This reviewer, closing recompute** | `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716` | 61 |

**HASH_MISMATCH.** Automatic **FAIL**.

Observed drift vs the opening freeze read (this channel did not write these files):

| path | open (lines / digest16) | close (lines / digest16) |
|---|---|---|
| `src/reasoning_diff/edits.py` | 287 / `cacb63ac27cbcccf` | 362 / `250055ab8257ea2e` (`apply_alt_source_same_value` added) |
| `src/reasoning_diff/measure.py` | 392 / `b15fb8a5bb92220f` | 408 / `8ec8cf09db149097` (`behavior_unknown`, `_has_sham_row`) |
| `src/reasoning_diff/cli.py` | 1249 / `779cedd373a8a509` | 1252 / `c1a274e233988aad` |

Paper file SHA-256 (required): `F3C0EC087B5BF4E503DB35F4D234C727DF3CE66F933E80781C69A0CC312EA57C` — **MATCH** declared `F3C0EC08…`. Size 51935 bytes. Title `Reasoning-Diff-修订方案-v3 (1).md`.

Pytest author claim in VERSION: 157 passed. This reviewer: `python -m pytest -q --tb=line` → **159 passed / 20.45s / exit 0**. Green is not paper-correct. The extra two tests are further evidence the freeze object moved.

## 1. File coverage

Digests are **closing-tree** SHA-256 unless noted. “Read” is what this channel actually opened.

### Required documents

| path | lines / bytes | digest | what was read |
|---|---|---|---|
| `Reasoning-Diff-修订方案-v3 (1).md` | 51935 B | `F3C0EC08…` MATCH | full: C1–C4, §2.1–2.4, §2.3 decoupling, §3 noise, §4.1 pipeline, §5 source–value, §8 verbalizer/attention, Week-8 / Gates |
| `docs/EXPERIMENT_PROTOCOL.md` | 86 | — | full: scope, labels, splits, intervention conditions, P1–P3, Gate 0–2 unregistered |
| `docs/CURSOR_GOAL_PROMPT.md` | §5 | — | §5 items 1–15 (truth, events, noise, splits, baselines, causal, C3, gates) |
| `.planning/REQUIREMENTS.md` | 76 | — | full v1 + paper atomics + author status column (claims, not closures) |
| `.planning/audits/round-14/VERSION.md` | 28 | — | declared hash, method, pytest claim |

### `src/reasoning_diff/**/*.py` (closing tree)

| path | lines | digest16 | what was read |
|---|---|---|---|
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58d` | full |
| `src/reasoning_diff/__main__.py` | 4 | `307299fda7b77d22` | full |
| `src/reasoning_diff/analysis.py` | 337 | `e4368b0a386da63b` | full: `p1_incremental`, `week8_decision`, forbidden claims |
| `src/reasoning_diff/artifacts.py` | 85 | `524657027e9b402f` | full |
| `src/reasoning_diff/baselines.py` | 125 | `3d7ec3ba60f894b4` | full: `verbalizer`, `attention_*` |
| `src/reasoning_diff/cli.py` | 1252 | `c1a274e233988aad` | full: prepare/collect/label/fit/analyze; `_find_tasks_jsonl`; `_e_premise_ids`; verbalizer wiring |
| `src/reasoning_diff/edits.py` | 362 | `250055ab8257ea2e` | full. Open freeze was 287 / `cacb63ac27cbcccf` (`make_source_value_pair` → `apply_rename_edit`) |
| `src/reasoning_diff/events.py` | 274 | `290a4fd676ac0814` | full |
| `src/reasoning_diff/executor.py` | 109 | `481d6ed597c93e78` | full |
| `src/reasoning_diff/graphs.py` | 46 | `1c755e6f8d22e277` | full |
| `src/reasoning_diff/interventions.py` | 115 | `0ffdbb8805be7649` | full |
| `src/reasoning_diff/io.py` | 133 | `1a03b2f8d865bdd3` | full |
| `src/reasoning_diff/measure.py` | 408 | `8ec8cf09db149097` | full. Open freeze was 392 / `b15fb8a5bb92220f` |
| `src/reasoning_diff/models/__init__.py` | 1 | `0b7dd6c4dd852065` | full |
| `src/reasoning_diff/models/adapters.py` | 42 | `c1992624026a1bf0` | full |
| `src/reasoning_diff/models/collect.py` | 261 | `83658cd8ba879f20` | full |
| `src/reasoning_diff/models/features.py` | 39 | `0a9f0b8beb0185ae` | full |
| `src/reasoning_diff/models/generate.py` | 201 | `07493570c6410e6b` | full: `append_target_assignment`, `generate_task_trace` |
| `src/reasoning_diff/models/tiny.py` | 120 | `21725a183452bd06` | full |
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
| `src/reasoning_diff/tasks/t1_config.py` | 21 | `e1e7f8232dfa603d` | full: 500 / op∈{5,10,15,21} / mod 23 checks only |
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

`tests/**/*.py` were executed via pytest, not line-audited as paper text. Fixture `tests/fixtures/t1_tiny.json` was loaded for the scientific run (`source_kind=fixture`, `p1=4`, `p2=0`, `q=p1*p2`).

## 2. Checks run

| check | command / object | result |
|---|---|---|
| Freeze hash (VERSION script) | open + close | open MATCH `1f61fd06…`; close **MISMATCH** `401e509b…` |
| Paper SHA-256 | `Reasoning-Diff-修订方案-v3 (1).md` | `F3C0EC08…` MATCH |
| pytest | `python -m pytest -q --tb=line` (`PYTHONPATH=src`) | 159 passed / 20.45s. Not paper-correct |
| Scientific prepare | `reasoning_diff` prepare `--fixture tests/fixtures/t1_tiny.json --eval-mode scientific --split-fractions 0.40 0.15 0.10 0.10 0.10 0.15 --sham-opportunities 1 --weight-seed 0` | rc 0. Artifacts under `.planning/audits/round-14/_a_sci_run/prep` |
| Scientific collect | collect `--backend tiny --weight-seed 0` | rc 0. `H` (7,32) all finite; `E` (2,32) all finite; 7 event rows, node `q` only |
| Scientific label | label on collect/prepare | rc 0 |
| Scientific fit | fit `--split probe_train --eval-mode scientific` | rc 0. Task head loss 0.050; behavior `no_known_labels` |
| Analyze (no `p1_table`) | analyze on hunt dir | `p1=null`, `scientific_conclusion=null`, Gate 0–2 `unregistered` |
| Source–value vs rename | `make_source_value_pair` vs `apply_rename_edit` on `t1_tiny` | parents/expr identical: `['p1','p2_src']` / `p1 * p2_src`. `reads_a_xor_b=False` |
| A12-03 | deep `feat/` without `tasks.jsonl`; ancestor `col/tasks.jsonl` swapped `[p2,p1]` | `_find_tasks_jsonl(feat) is None`; fit **raises** `ValueError: fit requires tasks.jsonl so E columns follow task.premises, not label order` |
| Leftover first-seen | `_e_premise_ids` | with task: `['p1','p2','extra']`; without: `['p2','p1','extra']` |
| Plus persist | isolated unique Symbolic; Plus register; RAM `_TEST_ONLY_FAMILY_KEYS.clear()` | isolated → `transfer_pairs` (not test); after Plus+clear → Symbolic still `test` |
| Booked-zero library | `event_density_sets` constructed labels | see A14-04 / ND-04 |
| Fixture ≠ official | `load_t1_fixture`; `load_igsm_snapshot(..., official)` on `t1_tiny` | fixture loads; official path `KeyError: 'template'` (not silent official) |

Scientific-run inspection (generated region, sham, densities):

- Every collected trace: `parse_status=constrained_target`, `parse_region=generated`, `weight_source=random_init`, `target_assignment` starts with `\nq = ` (base `82`, t0p `53`, sham `53`).
- Events: only generated-region `q` (`start=45` ≥ `prompt_len=36` on base; source `start=57`, `prompt_len=48`). Prompt `p1`/`p2` are not events.
- Sham: `premise_id=sham:q`, `rng_pair=sham:0`, outcome `changed` (82 vs 53). Real premises `noise_ref=None`.
- Densities: `null_reason=noise_set_missing`, `rho_S_excess=null`, `rho_M_excess=null`. Note in labels: “sham hits are not mapped onto real premises”.
- `source_kind=fixture` throughout. `source_value_pair.same_value_diff_source`: parents `['p1','p2_src']`, expression `p1 * p2_src`, text `p2_src = 0 (alt source)`.
- Fit verbalizer zeroshot/fiveshot/reflection: `score=1.0`, `extracted=82`, `text` is the teacher-forced prefix echo. `attention_mean` score `0.0`. `attention_threshold` on toy `[0.1, 0.9]`.

## 3. Findings

### A14-01 — Freeze hash mismatch

- **Severity:** blocker
- **File / symbol / line:** `.planning/audits/round-14/VERSION.md` vs live `src/reasoning_diff/{edits,measure,cli}.py` (and tests that moved pytest 157→159)
- **Trigger:** VERSION freeze object is not the tree under review at close
- **Paper / protocol req:** audit contract — reviewers bind a frozen byte set. Mismatch means paper claims cannot be attributed to the declared hash
- **Repro:** run the VERSION.md Python block. Declared `1f61fd06…`; live `401e509b…`
- **Impact:** any “closed on 1f61fd06…” statement is unbound. Mid-review patches cannot be written back onto this freeze
- **Fix:** stop edits; re-freeze; restart the round
- **Status:** confirmed defect

### A14-02 — `same_value_diff_source` is rename-isomorphic, not paper *a* vs *b*

- **Severity:** high
- **File / symbol / line:** `edits.py` `apply_alt_source_same_value` 219–289, `make_source_value_pair` 292–301, `_target_parents` 214–216. Open freeze: `make_source_value_pair` called `apply_rename_edit` (287-line file). Closing tree added cosmetic `(alt source)` text; the DAG is the same
- **Trigger:** paper §5 / C2: “目标计算分别要求读取 *a* 或 *b*，先令 *a=b*，使目标输出值相同而来源不同”. Protocol §4: equal-value different-source pairs for decoupling. GOAL §5.10
- **Repro:** `make_source_value_pair(load_t1_fixture(t1_tiny), "p2", "2")` vs `apply_rename_edit(..., {"p2":"p2_src"})`. Both: parents `['p1','p2_src']`, expression `p1 * p2_src`, premises `{p1, p2_src}`, answer still `0`. `set(alt.parents)==set(rename.parents)`. Target still reads *both* remaining leaves; it does not read *a* XOR *b*. `_target_parents(swapped)==_target_parents(task)` only checks that the mapped ID strings changed — tautological for a rename
- **Impact:** scientific `trace-source` and any C2 donor pair built from this API are a relabel of the same leaf, not a source–value decoupled pair. Source-follow scoring on this pair does not test “which premise was read”
- **Fix:** construct two existing premises *a*, *b* with *a=b* and two targets (or two graphs) that each require only one of them. Reject pairs whose parent *multiset of values* / required-source set is a rename of the base
- **Status:** confirmed defect

### A14-03 — Scientific `cmd_fit` writes §8 verbalizer / attention rows that are not §8

- **Severity:** high
- **File / symbol / line:** `cli.py` `cmd_fit` 650–671; `baselines.py` `verbalizer` 92–125, `attention_mean` 49–52
- **Trigger:** paper §8 “模型自述四档” predicts **依赖标签**, same samples / split / visible prefix as the probe. GOAL §5.7: “不能只用简陋替身对比”. REQUIREMENTS BASE-01 / VERB-01 / ATTN-01 (author `implemented_local` is not a closure)
- **Repro:** scientific fit on `_a_sci_run`. Rows: verbalizer zeroshot/fiveshot/reflection `score=1.0` because `generate_fn=lambda p, t=prefix: t` echoes `…\nq = 82` and gold is `trace.answer` `82`. Supervised raises (honest). `attention_mean(np.zeros((0,)), [])` → `0.0`. `fit_attention_threshold(np.array([0.1,0.9]), np.array([0.0,1.0]))` → `f1=1.0`
- **Impact:** artifacts named `baseline:verbalizer` / `attention_*` are answer-extraction from teacher-forced text and dummy arrays, not dependency self-report or premise-token attention. Claiming BASE-01 / §8 / Fig. 5 from this CLI path is a concept swap
- **Fix:** wire verbalizer gold to dependency labels on the same prefix as the probe; pass real attention maps; or refuse to write these keys in scientific mode
- **Status:** confirmed defect

### A14-04 — `event_density_sets` else branch still books evaluated-empty *N*

- **Severity:** medium
- **File / symbol / line:** `measure.py` `event_density_sets` 346–363 (`else: noise_set=[]; evaluated=True`)
- **Trigger:** paper §3 / protocol §2.6: noise referent needs a matching comparison opportunity; missing protocol or unmatched opportunity → null excess, not raw−0. Hunt: booked-zero vs deducted *N*
- **Repro:** constructed labels on `t1_tiny` with `sham_protocol` set, `noise_ref=0.0` on `p1`/`p2`, **no** `sham:` row, no mapped hit. Result: `null_reason=None`, `rho_M_noise=1.0`, `rho_M_excess=-1.0` (*N*=∅ ⇒ *T*∖*N*=*T*). Same function with a `sham:` row (hit or miss) → `noise_set_missing`, excess null
- **Impact:** library callers that mark real premises `observed` without a sham row book *N*=∅ as evaluated. Scientific CLI prepare with `--sham-opportunities 1` does **not** hit this (sham rows present → null). `sham_opportunities=0` sets `sham_protocol=None` → also null
- **Fix:** book evaluated-empty *N* only when a matching sham opportunity was actually recorded and produced 0 mapped hits; otherwise null
- **Status:** confirmed defect (library path). Scientific sham CLI path independently did **not** book zero

---

### Hunt closures that are **not** defects

#### ND-01 — Teacher-forced `\nq=` is honest `constrained_target`

- **Status:** non-defect
- `generate.py` `append_target_assignment` 72–98 docstring: “Not gold values.” `generate_task_trace` 157–158 sets `parse_status=constrained_target` when the assignment falls after free decode. Scientific traces all carry that flag + `weight_source=random_init` + `tiny-qwen2`. This is **not** MODEL-01 and **not** paper §4.1 natural CoT. Do not require inventing CoT. Do not allow anyone to file this path as §4.1 / C1 evidence.

#### ND-02 — Fixture is not official

- **Status:** non-defect
- `t1_tiny.json` `source_kind=fixture`. `load_t1_fixture` refuses non-fixture. `load_igsm_snapshot(t1_tiny, official)` raises `KeyError: 'template'`. `t1_config.validate_t1_prepare_config` only checks 500 / ops / mod 23 — no official dump is shipped. Official 500-grid remains `pending_server` (REQUIREMENTS DATA-01), not a silent fixture promotion.

#### ND-03 — Gate 0–2 unregistered is not a pass

- **Status:** non-defect
- `week8_decision` / analyze report: `gates.gate0/1/2.decision=unregistered`, `scientific_conclusion=None`, `status=not_evaluated`. Protocol §6 and GOAL §5.14 require this. Unregistered ≠ pass.

#### ND-04 — Scientific sham path does not book *N*=∅

- **Status:** non-defect (CLI path). See A14-04 for the leftover else
- Live scientific labels: `sham:q` `noise_ref=1.0`; `p1`/`p2` `None`; event densities `noise_set_missing`; excess null.

#### ND-05 — A12-03 ancestor `col/tasks.jsonl` is not bound

- **Status:** non-defect (independently confirmed)
- `_find_tasks_jsonl` 692–700 searches only the given stage directories. Deep `feat/` without its own `tasks.jsonl`, ancestor `col/tasks.jsonl` with premises swapped `[p2,p1]`: helper returns `None`; `cmd_fit` 618–619 **raises**; *E* is not `[p2,p1]`.

#### ND-06 — Leftover first-seen append is residual, not the A12-03 bind

- **Status:** non-defect suggestion
- `_e_premise_ids` 703–712 still appends leftover non-sham label IDs after `task.premises`. Without a task, order is first-seen (`['p2','p1','extra']`). Fit will not use that path when labels exist and `tasks.jsonl` is missing (raises). Extra IDs after official premises could still widen *E* if a task is present. Tightening: do not append leftovers.

#### ND-07 — Isolated Symbolic without Plus is not a family leak

- **Status:** non-defect
- Unique Symbolic, never registered Plus, persist cleared: `split_for_task` → `transfer_pairs` (hash split; not forced `test`). After Plus on a shared family + RAM clear, persist still locks that family to `test`. That is the intended disk lock, not an isolated-Symbolic leak. No shipped official Plus-id list was found. Isolated Symbolic staying out of `test` is expected.

#### ND-08 — Analyze does not invent P1

- **Status:** non-defect
- `cmd_analyze` 1068–1087: `p1` is set only from `p1_table.jsonl`. Without it, report `p1=null`, `status=not_evaluated`. Labels/covariates are not used as a fake P1 table.

#### ND-09 — Omitted official / server paragraphs

- **Status:** pending_server (not a local code defect if not claimed as run)
- Official iGSM 500 / op grid, Qwen3-8B / R1-Distill weights (MODEL-01), natural long CoT, Gate thresholds, held-out P1 table, C-rand/C-layer on real donors: not present as executed science. Tiny `random_init` and `constrained_target` are labeled as such. Do not write them into a scientific conclusion (analyze already writes `scientific_conclusion=None`).

## 4. Verdict

**FAIL.**

Reasons (any one is enough):

1. **HASH_MISMATCH** — declared `1f61fd067efe316bd749bb4f8ac8fb6eaf49d4c148830c14082dc0d4ddb91637` vs closing `401e509bc7a9b054c00e28e8bf56e0828ab84f7f67cd167b3d170817de88f716`
2. **A14-02** confirmed: source–value “pair” is a rename of the same leaf, not paper §5 *a* vs *b*
3. **A14-03** confirmed: scientific fit artifacts named verbalizer/attention are not paper §8
4. **A14-04** confirmed: `event_density_sets` else still books evaluated-empty *N* on the library path

Empty “looks fine” is not available. Consecutive-pass count cannot start on this freeze.

Teacher-force `\nq=` remains an honest local interface (`constrained_target`). It is not a defect and it is not §4.1 / MODEL-01.
