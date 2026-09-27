---
reviewed: 2026-09-21T03:24:36Z
depth: deep
status: issues_found
scope: data adapters, edits, event identity, labels, measurement, splits, prepare/label call chains
---

# Data and measurement review

Independent read-only review against AGENTS.md, original paper section 4.1 and 7, and docs/EXPERIMENT_PROTOCOL.md sections 2–3. No old Cursor review used as evidence. CPU snippets ran against current source with PYTHONPATH=src. Mocking read_json supplied official-shaped records without creating data files or touching the persistent split cache. No model downloads or source edits. Paths below are relative to C:/Users/22688/Desktop/diff.

## Narrative Findings (AI reviewer)

### DM-01 — BLOCKER / P1: repeated event versions collapse into one behavior label

**Files:** src/reasoning_diff/cli.py:229–253; src/reasoning_diff/measure.py:25–49; src/reasoning_diff/cli.py:609–645.

`_observations` replaces each full identity with `node_id` in both observation_id and event_pair. `build_labels` groups by `(node_id, premise_id)`, ignoring occurrence, scope, reference trace, model, and base problem. Any changed occurrence turns all occurrences positive. `cmd_fit` subsequently broadcasts this node label to every matching row, including other traces. This occurs in scientific prepare at lines 303–307, then scientific collect/fit consume these same records.

**CPU evidence:** Parse base `q = 8\nq = 8` and edit `q = 9\nq = 8` for the supplied T1 task with p2 changed to 2. `_observations(..., run_id='r')` produces two rows both named `obs:r:q:p1`, with outcomes changed/no_change. `build_labels` returns only `[('q', 1)]` although the second occurrence did not change.

**Fix:** Keep reference trajectory and complete EventIdentity as label/observation keys; keep node_id separately for task ancestor lookup. Match features to exact event/trace identity. Include edit and pairing identity in observation IDs.

### DM-02 — BLOCKER / P1: structural and failed scan opportunities vanish

**Files:** src/reasoning_diff/cli.py:229–255, 293–307, 382–399, 435.

`_observations` only iterates aligned pairs. Removed, added, merged, unaligned, parse-failed and generation-failed observations are never emitted despite schema support. In scientific mode an initial empty trace aborts preparation before recording its evidence; extra scans with empty events silently contribute no observations. Scan edit/task definitions are also omitted from edits.jsonl/tasks.jsonl: only the initial edit and optional source/value pair are written. The manifest hardcodes success=1/failure=0. Thus behavioral frequency, coverage and structural failure denominators cannot be audited or reconstructed from the claimed complete artifacts.

**CPU evidence:** A base trace with two q events and an edit trace with zero events returns `[]` from `_observations`. The removed count is available in `align_events` but discarded by the caller.

**Fix:** Persist one explicit outcome per expected base event/opportunity plus structural additions; persist every scan edit and edited task, including failures. Derive counts from these records. Preserve a stage failure record before refusing a scientifically unusable batch.

### DM-03 — BLOCKER / P1: no finite-scan negatives reach the behavior head

**Files:** src/reasoning_diff/measure.py:43–65; src/reasoning_diff/cli.py:216–226, 246–247, 303–307, 641–652; src/reasoning_diff/schema.py:358 (Edit.exhaustive default).

All generated value edits have exhaustive=False. build_labels recognizes no_change only if exhaustive=True, so unchanged but actually scanned cells become unknown, with opportunities=0. Scientific prepare therefore supplies only positive known behavioral labels; empirical M and a supervised response/nonresponse classifier cannot be estimated. This is not merely conservative language about universal independence: the finite-scan empirical target and its opportunity count have been erased.

**CPU evidence:** Replace a valid observation outcome with no_change while leaving exhaustive=False. `build_labels` yields `(behavior_label=None, opportunities=0)` after a real matched comparison. A changed observation yields `(1,1)`.

**Fix:** Represent empirical observed response/nonresponse under the frozen finite scan separately from exhaustive/universal claims. Count every matched scan opportunity, retain scan_state, response frequency and coverage; do not relabel unscanned/failure cases as zero.

### DM-04 — BLOCKER / P1: unknown truth/support becomes measured zero or spurious dependence

**Files:** src/reasoning_diff/measure.py:119–127, 330–369, 372–384.

event_density_sets substitutes an empty ancestor set when a graph/event is unknown, then passes every premise into the denominator. Known behavioral support is used only to suppress M. S is calculated even when no behavioral cells are known, and task_known is ignored. Both scientific prepare (line 376) and label (line 575) use this path.

**CPU evidence:** A task with graph_kind='none', graph_status='unknown', no nodes, two premises, and one changed p1 label with task_known=False reports `S=['p1'], rho_S_raw=0.5`. A complete q=p1*p2 task with an extra p3 and only an unknown p3 behavior label reports `rho_S_raw=0.0, behavior_unknown=True, denominator_S=1`. Neither is a measured spurious-dependence density.

**Fix:** Require known task membership and observed behavioral support per event-premise cell. Calculate on explicit eligible common support, expose coverage counts, and return null where task truth or all responses are unknown. Label finite-scan lower bounds explicitly if retained separately.

### DM-05 — BLOCKER / P1: missing matrix noise is treated as observed zero noise

**File:** src/reasoning_diff/measure.py:167–185.

The matrix path only regards the whole noise argument being None as missing. NaN/-1 cells remain in the denominator and compare unequal to 0/1, silently yielding zero reference rates. Behavioral NaNs similarly pass `(behavior != -1)`. This produces corrected scientific metrics without common support. This public helper is not the active prepare set-based path, but is directly used by callers/tests of matrix densities.

**CPU repro:** `dependency_densities(task=np.array([[0,1]]), behavior=np.array([[1,0]]), noise=np.array([[np.nan,np.nan]]))` returns rho_S_noise=0.0, rho_M_noise=0.0, both excess=1.0 and null_reason=None.

**Fix:** Validate shape and labels, construct finite binary support for all compared matrices, and emit null corrected quantities where noise has no support. Preserve raw metrics on their own declared support separately.

### DM-06 — BLOCKER / P1: official GSM-Symbolic gold is an entire rationale, not a number

**File:** src/reasoning_diff/tasks/t2_gsm_symbolic.py:54; downstream numeric equality at :83–85 and models/generate.py:175–190.

Official records store a GSM8K-style rationale ending in `#### <final_answer>`. canonical_value normalizes the entire string rather than extracting that terminal answer, so correct numeric predictions compare unequal. The fixture's already-numeric answer hides the bug. This affects scientific runs supplied official-shaped snapshots.

**CPU evidence:** Mock record answer `Calculate 4+3=7.\n#### 7` produces answer_spec.value `calculate 4+3=7. #### 7`; prediction `7` fails equality.

**Official format verification:** [Apple GSM-Symbolic dataset card](https://huggingface.co/datasets/apple/GSM-Symbolic) specifies the answer terminal marker. Consulted 2026-09-21; no dataset downloaded.

**Fix:** Extract and validate the terminal gold answer before canonicalization; preserve the rationale in a separate field, never as numeric truth.

### DM-07 — BLOCKER / P1: official GSM-Symbolic instances share task/record IDs

**File:** src/reasoning_diff/tasks/t2_gsm_symbolic.py:45–48.

Official id identifies a template; instance distinguishes its generated realizations. task_id uses only id, so all numeric/name variants share task_id and default record_id. Edit IDs built from task_id also collide. variant_id being separate does not fix code/artifact consumers that key on task_id.

**CPU evidence:** Mock official records `(id=0,instance=0)` and `(id=0,instance=1)` with distinct question text. Both load with task_id='0' and record_id='0'.

**Official evidence:** [Apple dataset card](https://huggingface.co/datasets/apple/GSM-Symbolic) explicitly defines id/instance. Its field descriptions establish this independently of project fixtures.

**Fix:** Namespace task_id by dataset configuration, template and instance; keep shared original-question identity only as base_group_id/family grouping.

### DM-08 — BLOCKER / P1: prepare silently drops all but the first input problem

**File:** src/reasoning_diff/cli.py:168–184, 382, 400, 435.

For an iGSM directory `_load_task` loads all tasks then returns loaded[0]. MuSiQue and T4 list loaders likewise return only index zero. prepare always emits one base problem plus its edit and one split row. Supplying a 500-question directory or a multirecord file does not execute or emit a dataset. There is no loop elsewhere in prepare. The same `_load_task` runs before the scientific/fixture branch.

**Concrete call chain:** `prepare --kind igsm --snapshot <directory>` → load_igsm_directory(all JSONs) → `loaded[0]` → exactly two tasks.jsonl records. `--t1-ops` validates declared configuration but never creates the missing task loop.

**Fix:** Return/iterate all tasks with per-task unique trace/run IDs and durable scan records, or explicitly reject multi-task inputs until batch handling exists. Validate actual problem counts and op coverage against protocol instead of silently accepting partial data.

### DM-09 — BLOCKER / P1: operator reversal changes gold but leaves model input unchanged

**File:** src/reasoning_diff/edits.py:340–366; T2 wrapper src/reasoning_diff/tasks/t2_gsm_symbolic.py:75–80.

apply_operator_reverse changes a graph expression and recomputes gold, but never rewrites task.question or premise text. It calls the result validity='valid' with no changed_premise_ids. This gives the same model input different expected answers and classifies every premise as unedited. Although not selected by the current CLI's default edit, this is the exposed T2 operator-edit implementation.

**CPU repro:** Load tests/fixtures/t1_tiny.json; apply_value_edit(p2,'2'); apply_operator_reverse(q). Before and after question both equal `p1 = 4. p2 = 2. What is q = p1 * p2?`; answer changes 8→2.

**Fix:** Use a verified editable operator/constraint span or task renderer to update question and independent graph together; declare the actual changed input dependency. Reject reversal when no consistent text transformation exists.

### DM-10 — BLOCKER / P1: T3 documents are never presented to the scientific generator

**Files:** src/reasoning_diff/tasks/t3_hotpot.py:14–47; src/reasoning_diff/tasks/t3_musique.py:16–26, 52–54; src/reasoning_diff/models/generate.py:101–102, 121–128; src/reasoning_diff/cli.py:294–295.

Both adapters keep context documents in task.premises while task.question holds just the question. task_prompt returns only task.question, and scientific prepare passes that to generation. Thus Hotpot/MuSiQue context replacements do not change any input tokens. The resulting comparison cannot test document dependence; many T3 inputs additionally encounter the tiny 96-token restriction or no-event failure, rather than a full T3 pipeline.

**Concrete evidence:** Inspecting document_edit shows it only changes premises and answer_spec. `task_prompt(base) == task_prompt(edited)` for a document replacement by construction. No generator code consumes task.premises.

**Fix:** Render dataset-appropriate context with stable title/sentence identities into the model prompt, track correct spans, and verify every declared document edit changes the actual prompt. Add nonnumeric answer extraction/scoring for T3 (extract_answer('The answer is Paris.','span') currently returns None at events.py:260–274).

### DM-11 — BLOCKER / P2: a premise's own event is classified as independent of itself

**Files:** src/reasoning_diff/events.py:78–87; src/reasoning_diff/measure.py:217–222, 239–250.

parse_events assigns every premise event task_parents=[] even for complete graphs. preservation_to_csp treats that as known-independent, so directly changing p1 puts the p1 event in the clean region. graphs.ancestors also omits premise entries from its returned mapping, so these same scientific events have unknown task labels downstream.

**CPU evidence:** For base `p1 = 4\nq = 8` and edited `p1 = 5\nq = 10`, with p1 edited and q=p1*p2, CSP reports clean_total=1, clean_matched=1, csp=0.0. All emitted events actually depend on p1; clean_total should be zero and CSP null.

**Fix:** Map a premise-value event to its own singleton input ancestor and include that identity in task-label lookup, or exclude premise restatements consistently from the event universe.

### DM-12 — BLOCKER / P2: occurrence-count ambiguity is converted back into an assumed match

**File:** src/reasoning_diff/events.py:196–215; scientific caller src/reasoning_diff/cli.py:230.

parse_events numbers occurrences independently within each trace. When one repeat is deleted, surviving repetitions shift numbers. align_events correctly marks unequal counts ambiguous; align_events_monotonic then pairs equal local occurrence numbers anyway. It also leaves matched identities in added/removed structural lists while shrinking unaligned to skipped left events only. This is the default for every nonfixture trace, including scientific tiny and future real traces.

**CPU evidence:** Two q events in base versus one in edit produces one pair `(version 1, version 1)` even though the survivor could be old version 2. The code has no source-location or expression evidence resolving which occurrence survived. Scientific observations treat this as an ordinary numerical comparison.

**Fix:** Preserve ambiguity unless an independent semantic/context mapping resolves versions; retain consistent disjoint matched/removed/added sets. Do not use renumbered occurrence counters as proof of identity after deletion.

### DM-13 — BLOCKER / P2: middle no-op insertion corrupts the original question

**File:** src/reasoning_diff/tasks/t2_noop.py:25–35.

The middle position is an arbitrary character midpoint. It can split a word or a premise, introducing a wording/meaning change in addition to the supposedly irrelevant sentence. If it cuts a premise, span remapping raises; if it cuts unannotated question wording, the corrupted pair can be accepted with answer_unchanged_proven=True because only the unchanged graph is recomputed.

**CPU evidence:** make_noop_pair(T1 task with p2=2, 'A shop has 9 chairs.', 'mid', 'low', True) returns `p1 = 4. p2 = 2. Wh A shop has 9 chairs. at is q = p1 * p2?`.

**Fix:** Insert at a verified sentence/clause boundary outside premise spans, record that boundary, and verify the original text is preserved as intact segments. Include position/surface/variant identity in unique task IDs.

### DM-14 — BLOCKER / P2: renaming the target node makes a valid task fail validation

**File:** src/reasoning_diff/edits.py:178–207.

apply_rename_edit updates node IDs, parents, aliases and expressions, but leaves task.target pointing to the old ID.

**CPU repro:** `apply_rename_edit(load_t1_fixture('tests/fixtures/t1_tiny.json'), {'q':'z'})` raises `ValueError: Target must be a task node`.

**Fix:** Map target through the same rename mapping and validate injectivity and reference consistency.

### DM-15 — BLOCKER / P2: full Hotpot document replacement repeats the new document per old sentence

**File:** src/reasoning_diff/tasks/t3_hotpot.py:58–70.

With sentence_id=None, every sentence in the document is replaced with the whole replacement string. A document with N sentences becomes N identical copies of a replacement document, rather than one replacement. Once context rendering is repaired this changes length, repetition and attention independently of the intended document substitution.

**CPU evidence:** tests/fixtures/t3_hotpot_one.json has two DocA sentences. `document_edit(task,'DocA','New document')` returns two DocA premises both text='New document'.

**Fix:** Accept/resegment a replacement document and rebuild its sentence identities, or expose an explicitly sentence-scoped edit and reject document-wide use without a sentence mapping.

### DM-16 — BLOCKER / P1: split assignments depend on preparation order and an unhashed local cache

**Files:** src/reasoning_diff/splits.py:15–34, 127–152; src/reasoning_diff/tasks/t2_gsm_plus.py:20–22; src/reasoning_diff/cli.py:260–263, 400, 409–414.

Loading a Plus record globally registers test-only family locks. split_for_task rereads those locks, but previously written split artifacts/fitted models are never invalidated or regrouped. Preparing Symbolic first can place a shared GSM family in probe_train; loading its Plus relative later forces test, creating the forbidden family train/test overlap. The cache is also absent from run_spec input hashes. This is not resolved by correct within-record base_group_id grouping.

**CPU evidence (read function mocked, no cache writes):** for the supplied fixture family, `_load_persisted_locks` returning empty gives split_for_task='probe_train'; returning `{task.base_group_id}` gives 'test' with the same seed/input. `siblings` also falsely locks unrelated families when both lack optional shared keys, because None is included on both sides of the set intersection (lines 130–141); an unrelated fit-ineligible Plus task changed this fixture from probe_train to test.

**Fix:** Freeze a complete family-level split manifest before any fitting, including test-only relatives, and hash/version it. Reject conflicting prior artifacts. Remove None from sibling key sets. Do not use mutable process/disk history as an unrecorded input to splitting.

## Additional verified scope limitations for the parent summary

- prepare's allowed-edit scans have one chosen alternative per numeric premise, one random stream, and exhaustive=False. This is a finite pilot, not the full perturbation grid; do not infer universal soundness. Task DAGs are independently loaded, but fixture traces themselves are rendered directly from node gold values; fixture behavioral labels are therefore oracle-derived by design. Scientific traces must remain separately labeled.
- T2/T3 adapters mostly expose contracts/placeholders, rather than the complete protocol. CLI `_domain_edit` hardcodes GSM-Plus 4→5, HumanEval append-comment with no independently validated new solution, Hotpot/MuSiQue literal 'replacement', and T4 append-question-mark (cli.py:187–212). These cannot establish meaningful full T1–T4 implementation. Scientific prepare's generic assignment parser cannot parse span answers/status labels; most no-node domains immediately fail no-events at cli.py:296–297. T4 loader always source_kind='fixture' (tasks/t4_boundary.py:25).
- Finite no-edit shams deliberately retain synthetic sham premise IDs and do not identify real-premise noise. Accordingly prepare's corrected density fields remain null. This is appropriate missingness, but the noise-corrected C3 measurement protocol is not implemented by those artifacts. Do not patch it by copying global noise changes onto arbitrary real premise IDs.
- preservation_to_csp computes csp_noise with edited_premises=set() (measure.py:285), so its reference includes the entire known event set rather than the perturbation's clean event region. Same-region/noise comparisons required by the protocol are not met.
- MuSiQue decomposition reference parsing uses token[1:] without stripping punctuation (tasks/t3_musique.py:30–32). With `Where was #1?`, it constructs parent `s1?`; task.validate later raises `Node s2 must reference earlier nodes/premises`. Confirmed using an in-memory record. This is an additional adapter robustness defect, not evidence that every official record contains that particular form.

No changes were made to source, tests, split caches, experiment artifacts, or scientific results. This report is the only authored file in this lane.
