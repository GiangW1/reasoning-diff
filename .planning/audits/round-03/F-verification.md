# F: verification quality and adversarial doubt (round-03)

Independent review channel F. Production tree was not modified. Pytest green is not treated as paper-correctness. Other round-03 channel reports were not read (only `VERSION.md` existed at start). `ISSUES.md` was read only as author claims; every claimed closure was re-checked from tests vs production.

**Lead conclusion:** `python -m pytest -q` is **70 passed / exit 0**. Freeze hash **recomputes**. That is not Goal acceptance and is not independent proof of paper behavior. Round-03 added five regressions and some real unit oracles (B-06 text mention, B-23, B-24, default P1 `requires_held_out`, `-1` BCE mask). The CLI science path, logistic P1, conformal composition (`predict_set`), HumanEval isolation, C4 execution, bilinear/score/λ_FN/BoundaryMLP, C-layer **dev** selection, T3 truth updates, and most appendix symbols are still untested or tested by mirrors/stubs. This channel **does not pass** and **does not declare Goal complete**.

## 1. Metadata

| Field | Value |
|---|---|
| agent / task | Independent Reviewer F / verification quality and adversarial doubt |
| review time | 2026-09-21 (Asia/Shanghai) |
| declared freeze | `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e` |
| recomputed aggregate | `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e` |
| hash verdict | **HASH_MATCH** |
| hash method used | 55 files: `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml` (no `__pycache__`). Sort by POSIX `relpath`. Update SHA-256 with `relpath.encode() + b"\0" + file_bytes`. No CRLF in any scoped file. |
| file-count match | 55 files, matches `round-03/VERSION.md` |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d` (2026-09-20 23:54:47 +0800; working tree dirty; do not trust HEAD as the freeze) |
| pytest | **70 passed in 10.49s, exit 0.** Collect: 70 nodes. No skip/xfail/deselected/`unittest.mock`/`assert True`. One `@pytest.mark.integration` (tiny hooks) still **ran**. |
| scope | all `tests/**` (13 `.py` + 10 fixture JSON) and every production function those tests import or CLI-smoke; remaining production modules scanned for untested entry points |
| explicitly unread | `.planning/audits/round-03/{A,B,C,D,E}-*.md` (absent at start) |

Review object is the **current working-tree bytes** below. Author `pytest_author_claim: 70 passed` is independently confirmed as a command result only.

## 2. Per-file coverage

### 2.1 Tests (all read)

| File | Lines | File SHA-256 | What it actually binds |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | `t1_tiny_path` only |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest/NaN; digest self-check; **no** `--resume` hash fail |
| `tests/test_cli_pipeline.py` | 29 | `63b4c09f51f6c7d8…` | eight-stage exit 0 + `report.status==not_evaluated` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator replay + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | set densities, joint `f=xy`, cone source strings |
| `tests/test_review_regressions.py` | 371 | `1e91c98d55e64548…` | round-01/02 oracles + five new cases; mixed independence (see §6) |
| `tests/test_science.py` | 97 | `3180ca3217882de5…` | conformal happy path, transfer **shape**, one position, streams, Week8 unregistered, P1 single-class, verbalizer, repair flags, swap, noop metadata |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | official shape/mod23/answer 12; config happy path; no `tools` import |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8; unknown without sidecar; GSM-Plus test-only |
| `tests/test_t3_t4.py` | 40 | `54e57fea7417d901…` | Hotpot flags, MuSiQue pair, HumanEval status string, T4 set equality |
| `tests/test_tiny_cache.py` | 25 | `097a48534da1e870…` | cache mutation as **expected**; collect/intervene flags |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook effect + cleanup; L17 tautology |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare, identity, densities, TO, prepare CLI |
| `tests/fixtures/*.json` | 10 files | **outside freeze** | hand oracles |

Collect-only: **70 nodes**. Zero `skip` / `xfail` / `skipif` / `unittest.mock`. Zero `assert True`. One equivalent tautology: `assert layer.__class__.forward` (`tests/test_tiny_hooks.py` L17).

New vs prior 65-node suite (author-added, independently classified): `test_b23_*`, `test_b24_*`, `test_b06_surface_mentions_include_text_after_value`, `test_c_unknown_label_is_masked`, `test_p1_requires_held_out_by_default`.

### 2.2 Production vs tests

| File | Lines | File SHA-256 | Test reach | Untested or only stub-touched |
|---|---:|---|---|---|
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` only | argv/`SystemExit` |
| `analysis.py` | 157 | `bf3440b0fd0fd01c…` | P1 single-class + default `requires_held_out` + rank-AUC on **linear** `precomputed`; Week8 unregistered; P3 flag | logistic P1; holdout **leak oracle**; `p2_paired`; Week8 vs measurements; `cone_fit` (`r2` always None); `procrustes`; `retrieval_scatter`; `bootstrap_cluster` |
| `artifacts.py` | 83 | `61dc639ead0eff1f…` | run_spec/manifest | `completed_shard_ok` only inside CLI `assert`; **resume mismatch untested** |
| `baselines.py` | 44 | `2d28ef1cdff3bd57…` | verbalizer two visibilities | `text_predictor`; `attention_mean`; `attention_rollout`; fiveshot fairness |
| `cli.py` | 511 | `bcdf4f982b585f1d…` | exit codes; label/fit file keys; `--in-dir` parsed | collect writes **prefix ids** as `H`; calibrate 4 synthetic `1-loss` scores; intervene `geometry_only` / zero norms / `clayer_status=placeholder_subspace_not_dev_layer`; analyze ignores `labels.jsonl`; repair `generated_tokens` hardcoded `[1,2]` |
| `edits.py` | 184 | `f201eb4931556ac0…` | 7→0; isolated numeral; decimal; official 4*3%23=12 | `apply_rename_edit`; `apply_source_value_edit`; non-arithmetic expr |
| `events.py` | 142 | `73e9b2667e489b54…` | identity align; surface≠parents + text mention; deletion counts | `extract_answer`; `strategy_changed` empty unless status set; `boundary_index` `position` does not change `limit` |
| `executor.py` | 59 | `d1760266a9a7606b…` | Spy constructed | **`spy.calls` never asserted**; `forbid_host_exec`; `exec(` reject |
| `graphs.py` | 44 | `1e287cebf844cec0…` | ancestors via fixture | `graph_status` empty-complete reject |
| `interventions.py` | 91 | `b971c432d1e2b2fd…` | swap [1,1]; C-rand/C-layer **norm**; INLP dim-0 | rescue; `intervention_report`; C-layer **dev-split layer pick**; same-cohort identity |
| `io.py` | 127 | `c5c77a27d196e97d…` | encode/jsonl/npz | `runtime_info`; corrupt JSONL line |
| `measure.py` | 248 | `fde5ec49294e5b74…` | set ρ; matrix missing-noise; build_labels B-02/03/23; CSP empty parents | set-path empty `noise_set` (B-26 impl, **no test**); `compare_pair` structural |
| `models/__init__.py` | 1 | `0b7dd6c4dd852065…` | — | — |
| `models/adapters.py` | 29 | `a8680ef98b8075ce…` | **zero tests** | `card`; `latest` dead branch |
| `models/collect.py` | 47 | `051e1b3005631c48…` | flags | `cache_isolated` is `is not`; CLI collect does **not** call this |
| `models/features.py` | 43 | `ff5c6a79b9ecf082…` | D-01 indices 1/2/3 | `leaks_target` cannot become True (selected tokens have `b<=limit`) |
| `models/generate.py` | 56 | `4fd7091842236d7a…` | replay/greedy | `apply_model_template`; top-p/k; thinking |
| `models/tiny.py` | 104 | `bd916289e9aaa006…` | hook cleanup + logits change | last-token-only **not asserted** (impl does it); L17 tautology |
| `probes/__init__.py` | 3 | `3065196db28e929c…` | — | — |
| `probes/bilinear.py` | 76 | `35e8d6ff7425f818…` | `weighted_bce` `-1` vs slice | no σ(hᵀUVᵀe+b) oracle; λ_FN=10 not independently locked; CLI both heads share Y |
| `probes/boundary.py` | 23 | `a45ec29f20fc3b3c…` | **zero tests** | Hidden=256 ReLU (impl rejects 128; untested) |
| `probes/calibrate.py` | 42 | `16609e8f7007aab4…` | α=0.4/0.1; α≥1 invalid; `sequence_score` default `max(p)` | **`predict_set` unused**; `one_minus_p` unused in tests; slack +1e-12 |
| `repair.py` | 64 | `55cbcf07d0f42bbd…` | mask + refilled | default `generated_tokens=0`; CLI injects `[1,2]`; `repairability`/`recompute_ratio` **zero tests** |
| `rng.py` | 53 | `2098c2c72a852eaa…` | two scalars unequal | snapshot/restore; torch.Generator isolation |
| `schema.py` | 373 | `5140f8b1687569b9…` | enums, identity | `canonical_value` aliases; most negative paths |
| `scoring.py` | 30 | `d05822c4fb784fe4…` | code status string | `score_qa`; isolated true exec |
| `splits.py` | 78 | `fd871c0ae40ef721…` | gsm_plus→test; family_id **required** | same-members different `family_id` not asserted; `assert_disjoint`; illegal fractions |
| `tasks/catalog.py` | 39 | `5d3918394b1603bb…` | **zero tests** | `iter_snapshot_files` / `load_snapshot` |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | legal config only | reject ops/mod/n≠500 (impl raises; untested) |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 86 | `3267cf12bf9ef5e4…` | ancestors/mod/12 | dump-mismatch raise **untested**; `shared_rng_excluded` hardcoded True (L72) |
| `tasks/t2_gsm_plus.py` | 51 | `6d396506526c5281…` | test-only | `query_reversed` **∉** `T4_STATUSES` (L20–21) |
| `tasks/t2_gsm_symbolic.py` | 70 | `f0492a797e6d89a0…` | sidecar edit | no-sidecar placeholder premises |
| `tasks/t2_noop.py` | 80 | `26cf5c21b5838a6b…` | front span + metadata | mid/back |
| `tasks/t3_hotpot.py` | 94 | `e5e7a9075ea64df9…` | support≠DAG; changed ids | `document_edit` without `new_answer` leaves `requires_independent_truth` (unasserted) |
| `tasks/t3_humaneval.py` | 61 | `3f74a52b59748db7…` | family id; status | `apply_spec_edit` **zero tests**; `score_submission` never takes executor |
| `tasks/t3_musique.py` | 93 | `761c8bc8b7c77bfe…` | pair ids | `paragraph_edit` **zero tests** |
| `tasks/t4_boundary.py` | 33 | `a2ca9188353b213d…` | set equality | illegal status; family grouping |
| `transfer.py` | 50 | `cffe4791564fbb9c…` | 4096/3584 N/A; unlabeled **shape** | labeled numerical map; `apply_bilinear_inputs`; ones-shape still vacuous |

Fixture JSON is **not** in the freeze. Changing official answers / sidecar / T4 statuses does not change the published aggregate, but changes “ground truth.”

## 3. Checks run and results

| Check | Command / method | Result |
|---|---|---|
| Freeze hash | `VERSION.md` script verbatim | **HASH_MATCH** `67bb9c90…` (55 files, POSIX relpath + NUL + bytes). |
| Full pytest | `python -m pytest -q` at repo root (`pythonpath=src`) | **70 passed in 10.49s, exit code 0**. No skip/xfail/deselected. |
| Collect | `python -m pytest tests --collect-only -q` | 70 nodes, collect exit 0 |
| skip/xfail/`assert True` | ripgrep on `tests/**` | no skip/xfail/mock; tautology at `test_tiny_hooks.py` L17 |
| Hand oracles | iGSM `4*3 % 23 = 12`; dump `3*3%23=9`; fixture `7*0=0`; sidecar `5+3=8`; TO `2·LCS([1,2],[1,3])/4=0.5`; D-01 indices 1/2/3; C-02 α=1 invalid; BCE `10·(-log 0.8)` | those **unit** assertions that exist match independent arithmetic |
| Adversarial: CLI chain | prepare→…→analyze on `t1_tiny` | collect `H=[[1,0,…]]`, `weight_source=offline_prefix_ids`; both probe heads `loss=0.000559…` (same Y); calibrate scores `[1-loss, 1-(loss+0.1), 0.7, 0.6]`; intervene all norms `0.0`, accuracies `None`, `clayer_status=placeholder_subspace_not_dev_layer`; repair `generated_tokens=2` from hardcoded `[1,2]`; analyze `p1/p2/p3=None`, `status=not_evaluated` while `labels.jsonl` exists |
| Adversarial: resume | corrupt `traces.jsonl` then `--resume` | **raises** `ValueError: resume hash mismatch` — **no test** |
| Adversarial: P1 | default / precomputed / holdout / leaky lstsq-on-all | default `requires_held_out`; precomputed `delta_auc=0` via `length+0.01*op`; holdout is **lstsq not logistic**; leaky fit-on-all still `held_out=True` and `auc_base is not None` → `test_c01_held_out_*` would stay green |
| Adversarial: conformal | `[0.7,0.4]` | default `sequence_score=0.7` (`max(p)`); `one_minus_p=0.6`. Tests use `[0.1,0.9]` (palindrome) and never call `predict_set` |
| Adversarial: `predict_set` | `[0.9,0.1], q=0.2` | `[True, False]` uses `1-p`. Unused in suite |
| Adversarial: joint `f≡0` | `joint_edit_counterexample` | `joint_changed=False` but `soundness_claim_allowed=False` still (constant) |
| Adversarial: Week8 | `{gate0/1/2:0.9}` | all `evaluated`, **no measurement comparison**. `"already decided"` is blocked in code; **not fed by tests** |
| Adversarial: family_id | same members, ids A vs B | roles differ (`direction_fit` vs `probe_train`). **Test does not assert this case** |
| Adversarial: leak flag | several offset/kind pairs | `leaks_target` never True; D-01 “leak” case is `idx=None` + `False` |
| Adversarial: transfer | ones(5,4)/ones(5,6) unlabeled | `allclose(ones)` is **False** (impl changed); test still only checks `shape==(5,4)`. Labeled affine `tgt=diag(2,3)→I` recovers; **no test** |
| Adversarial: Spy / `exec(` | `score_code(..., executor=spy)` | `len(spy.calls)==1`; `exec(` → `rejected`. Tests assert neither |
| Adversarial: T3 edits | document/paragraph/spec without new truth | `answer_updated=False` / `requires_independent_truth` / `needs_truth` |
| Adversarial: iGSM mismatch | dump answer `99` vs template 9 | **raises** `official dump answer does not match template recompute`. **No test** |
| Adversarial: rename / source_value | fixture | rename keeps values; source_value is value-edit+kind. **Zero tests** |
| Adversarial: empty noise | `noise_set=[]` + sham protocol | `null_reason=noise_set_empty`. **No test** (B-26 claim) |
| Adversarial: last-token hook | tiny layer-1 | prefix hidden unchanged, last position transformed. **Not asserted** |
| Adversarial: `query_reversed` | `T4_STATUSES` | not a member; GSM-Plus sets it for `"reversing operation"` |
| Adversarial: BoundaryMLP / repairability | direct call | hidden `(3,256)`; `hidden=128` raises; `repairability(4,10)==0.6`. **Zero tests** |

## 4. Checks not run, and why

| Not run | Reason |
|---|---|
| Real HF weights, official full dumps, GPU/CUDA KV | out of scope / `pending_server` |
| Linux isolated executor actually running HumanEval | only `UnavailableExecutor` / `SpyExecutor` |
| Other channel reports | forbidden / files absent |
| Editing production or adding regressions | forbidden; counterexamples are protocol-only in §8 |
| Line-by-line audit of `transformers`/`torch` | project usage only |

## 5. Delivery claims vs what tests prove

| Claim | Location | Do tests support it? |
|---|---|---|
| `python -m pytest -q` → 70 passed | `VERSION.md` L9 | **Command yes.** Using it as phase/Goal evidence: **no.** |
| `python -m pytest -q` → 65 passed | `06-VERIFICATION.md` L8; `STATE.md` L15; `PAPER_TRACEABILITY.md` TR-0002+ | **Stale.** This freeze is 70. Still not Goal evidence. |
| “round-02 closures pending independent close” | `ISSUES.md` | **Partial.** See §9 F3-15. Several unit closures hold. Several author closures have **no** independent test (B-26, resume, predict_set, rename/source_value, spec/paragraph, iGSM mismatch). |
| CLI pipeline / stages consume upstream | `docs/SERVER_RUNBOOK.md` L22–31; `test_pipeline_consumes_upstream` | Files are read. Science is **not**: collect is prefix-id `H`; analyze ignores labels; calibrate is four `1-loss` numbers; intervene invents no accuracy (good) and also computes no paper effect (norms 0 on a 1-row feature). |
| Traceability `verification_method=python -m pytest -q` on hundreds of rows | `.planning/PAPER_TRACEABILITY.md` TR-0002+ | **Cannot.** Suite does not contain oracles for those rows. Ledger still says `passed_local_tests` / `65 passed`. |
| Goal §九 items 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **Not evidenced by this suite.** See §10. This channel **does not** declare Goal complete. |
| Author pytest claim 70 | `VERSION.md` | Independently confirmed: 70 / exit 0. |

## 6. Are tests independently valid?

### 6.1 Independent oracles (would fail a wrong impl)

- `test_value_edit_recomputes_expression`: `p1=7,p2=0 → q=0`.
- `test_symbolic_sidecar_edit` / `test_b08_*`: `a:4→5`, `a+b=8`, question/nodes updated.
- `test_template_not_g_and_mod23` **answer** `"12"` (`4*3 % 23`).
- `test_to_empty_is_null`: `[]` null; `[1,2]` vs `[1,3]` → 0.5.
- `test_signed_excess_not_clipped` / pitfalls: signed −0.5 under **this** set formula (locks the formula; see F3-11).
- `test_zero_denominator_null`; `test_b01_*` missing noise is None not 0.
- `test_b02_*` finite-scan `no_change` → unknown.
- `test_b03_*` sham `changed` does not set `behavior_label=1`.
- `test_b23_*` observed `no_change` without `exhaustive` → unknown.
- `test_b04_*` unequal occurrence counts → no rematch.
- `test_b06_*` `surface_mentions==[]` while parents `{p1,p2}`; text `"mentions p1"` includes `p1`.
- `test_b07_*` `HumanEval/0` not truncated.
- `test_b09_*` / `test_b24_*` `14`/`3.5` with value `"4"`/`"5"` must raise.
- `test_b10_*` front no-op does not steal `p1` span.
- `test_b11_*` empty parents + graph unknown → CSP null.
- `test_b14_*` `source="gsm_plus"` → `test`.
- `test_b13_*` **first line only**: missing `family_id` raises.
- `test_c02_*` α≥1 → `invalid`.
- `test_c03_*` INLP after 2 steps zeros the discriminative axis on the constructed `H`.
- `test_c04_*` C-rand without `target_norm` raises; norms match provided main.
- `test_c_unknown_label_is_masked`: `-1` excluded (equality to known-only slice). Catches treat-`-1`-as-`0`. Does **not** lock λ_FN independently (same function both sides).
- `test_p1_requires_held_out_by_default`: default two-class path is `requires_held_out`.
- `test_d01_*` token indices **1, 2, 3** on a constructed offset list — real POS-01 unit oracle (leak flag half is not; see F3-10).
- `test_swap_formula`: `[1,0]+Π([0,1]-[1,0])=[1,1]`.
- `test_encode_rejects_nan`; `test_npz_no_pickle`; fixture≠official; no `import tools`.
- `test_direct_transfer_rejects_4096_3584` **status string** (shape half is weak).
- Tiny hook: logits change under hook and restore after remove (L22–26). L17 excluded.
- `test_explicit_generator_replay`.

### 6.2 Invalid, self-referential, or too weak

| Test | Why it does not prove paper behavior |
|---|---|
| `test_full_cli_smoke` L24–29 | Exit 0 + `not_evaluated` + files exist. A CLI that writes constants still passes. This channel’s analyze-after-prepare run is exactly that. |
| `test_pipeline_consumes_upstream` L358–371 | Stops at fit. Asserts `"task_label" in row` and `"loss" in probes[0]`. Any finite loss on prefix-id `H` passes. Does not check label values equal prepare, or that `H` are hidden states. |
| `test_e04_analyze_manifest_includes_report` L281–288 | **Encodes the stub as the expected outcome** (`status==not_evaluated`, `scientific_conclusion is None`). Does not prove analyze refused to invent P1 from labels. |
| `test_e02_*` | Only `edited answer != base answer`. Any non-identity edit passes. |
| `test_e08_*` | `hasattr(entry, "main")`. |
| `test_e06_*` | No leftover tmp after **success**. Crash-mid-write atomicity untested. |
| `test_c01_auc_is_rank_and_permutation_invariant` | Uses **`precomputed=True`**: `length+0.01*op+rho` (`analysis.py` L46–48). Tests rank-AUC of the **linear substitute**, not paper logistic P1. |
| `test_c01_held_out_fit_does_not_use_eval_rows` | Asserts `held_out is True` and `auc_base is not None`. A leaky fit-on-all-rows lstsq still returns those. **Does not compare to an oracle that excludes eval rows.** Estimator is linear, not logistic. |
| `test_p1_null_on_single_class` | Any `if unique(y)<2: return None` stub passes. |
| `test_conformal_examples` L25 | `sequence_score([0.1,0.9])==0.9` is true for both `max(p)` and `max(1-p)`. `predict_set` never called. `one_minus_p` unused. |
| `test_joint_edit_blocks_soundness` | Uses `f=x*y` (good for `joint_changed`). `soundness_claim_allowed` is **hardcoded False** (`measure.py` L238). `f≡0` still yields False. Flag is not derived from the fixture. |
| `test_week8_never_passes_unregistered` | Only `not_evaluated`. Threshold path untested; REST string `"already decided"` is implemented (`analysis.py` L117–123) but **not fed**. |
| `test_direct_transfer` map | unlabeled ones → shape (5,4). `return np.ones((5,4))` still passes. Labeled path unused. |
| `test_cone_fields_separated` | Source strings only. Empty `predicted` still labeled `behavior_head`. |
| `test_template_not_g_and_mod23` flags | `shared_rng_excluded` is written `True` (`t1_official.py` L72), not computed from dropped nodes. Dump-vs-recompute mismatch untested. |
| `test_config_ops` | Legal `{5,10,15,21},500,23` only. |
| `test_collect_and_intervene_tiny` | `cache_isolated` is object identity (`collect.py` L44). `leaks_target is False` on that prompt. |
| `test_tiny_hooks` L17 | `assert layer.__class__.forward` is true for any class with a `forward`. Last-token-only untested. |
| `test_humaneval_never_host_exec` | Does not read `spy.calls`. `score_submission` has no executor arg. Hardcoded `executor_unavailable` passes. |
| `test_repair_reprefills_and_refuses_gate` | Accepts default `generated_tokens=0` (`repair.py` L43–48). CLI path injects `[1,2]` and is unasserted. |
| `test_streams_are_independent` | Two floats unequal. No replay/snapshot. |
| `test_verbalizer_supervision_contract` | No fiveshot, no shared split with probe. |
| `test_t4_statuses_distinct` | Set equality with `T4_STATUSES`. |
| `test_hotpot_support_is_not_full_dag` | Edit does not require new truth; `answer_updated` unasserted. |
| `test_b13_assign_family_*` after the raise | Different member lists. Hashing the whole set still passes. Same-members different ids **not** asserted (this channel: they differ in impl). |
| `test_c_unknown_label_is_masked` | Proves `-1` drop vs slice; λ_FN=10 and bilinear score formula not locked. |
| `test_d01_*` leak half | `token_index is None` and `leaks_target is False`. Names the flag “real” while the True branch is unreachable. |
| `test_use_cache_false_*` | Documents transformers pollution as **desired**. No failing test that a second condition must not consume the dirty cache. |

## 7. Mocks / stubs that hide unconnected paths

Almost no `unittest.mock`. Internal stubs do the same job.

1. **CLI science path still disconnected (F3-01).** `--in-dir` is parsed; label requires observations; resume hash-checks exist. Then:
   - `cmd_collect` L269–277 writes `H` from synthetic `token_prefix` (`offline_prefix_ids`), not `collect_tiny` / residual hooks. This channel: `H=[[1,0,0,0,0,0,0,0]]`.
   - `cmd_fit` trains `BilinearProbe.fit` on that row and a Y built by walking the first `h.shape[0]` label rows (L340–355). Task and behavior heads get the **same Y** and the **same loss**.
   - `cmd_calibrate` L366–375 uses four hand scores shifted by **training loss**, then `sequence_score(..., one_minus_p)` — not held-out nonconformity on calibration traces.
   - `cmd_intervene` L400–415 writes `target/nontarget/task_correct/invalid = None`, `status=geometry_only`, `clayer_status=placeholder_subspace_not_dev_layer`. With 1-row `H`, `base==donor` → all norms 0.
   - `cmd_analyze` L445–460 looks only for `p1_table.jsonl`. Prepare/label never write that file. P1–P3 stay `None`. `test_full_cli_smoke` **expects** `not_evaluated`.
2. **Repair is still a ledger (F3-06).** `run_repair` counts a caller-supplied id list. CLI always passes `generated_tokens=[1,2]`. No model decode, no slot graft.
3. **HumanEval isolation is a status string (F3-04).** Spy can record; tests do not look. `score_submission` → default `UnavailableExecutor`.
4. **Tiny intervene isolation is `is not` (F3-10).** `past_key_values=None` guarantees a new object.
5. **BoundaryMLP, attention/rollout, model cards, `apply_model_template`, INLP four-outcome semantics, rescue, P2, cone_fit, Procrustes, retrieval, `predict_set`, `repairability`, `catalog.load_snapshot`, `assert_disjoint`, `apply_rename_edit`, `apply_source_value_edit`, `apply_spec_edit`, `paragraph_edit`** have **zero test references** (ripgrep on `tests/`).

## 8. Counterexamples that should fail a wrong impl (current tests will not)

These are independent and writable as regressions. This channel did not add tests.

### CE-1 CLI analyze must consume labels or refuse

- Construct: `prepare` writes `labels.jsonl`; delete it or pass a dir without `p1_table.jsonl` / labels; run `analyze --in-dir`.
- Expect: refuse, or P1 computed from those labels with a frozen oracle.
- Current: exit 0, `p1 is None`, `status=not_evaluated`.
- `test_e04` **requires** that stub.

### CE-2 Held-out P1 leakage + logistic

```text
n=40, y = 1[length+op>0], rho = noise
held_out = last half
Oracle: fit logistic (or even lstsq) on ~held_out only.
Wrong: fit on all rows, then score held_out  → test_c01_held_out still passes
(auc_base is not None). This channel: leaky auc_base=0.979 vs honest 1.0.
Also: precomputed path must not be length+0.01*op.
Swap: rho perfect, length noise → ΔAUC>0 under logistic; current holdout lstsq can move;
      tests never require the sign/oracle.
```

### CE-3 Conformal units

```text
p_hat = [0.7, 0.4]
max(p)=0.7, max(1-p)=0.6  → distinguishes (this channel confirmed)
predict_set must use the same s.
α=1 already invalid (C-02 good). Keep it.
Call predict_set; do not leave +1e-12 slack untested if it is load-bearing.
```

### CE-4 Joint flag from evidence

```text
f(x,y)=x*y: singles 0, joint 1 → fixture valid
f≡0: joint_changed must be False; soundness_claim_allowed must not be a constant
      (either False-with-invalid_fixture, or derived from (single_ok ∧ joint_changed))
```

Current `f≡0` still `soundness_claim_allowed=False`.

### CE-5 Transfer numerical + both inputs

```text
src=I_2, tgt=[[2,0,0],[0,3,0]]
apply_map(tgt,W) ≈ src  (this channel: labeled lstsq already does; test does not check)
apply_bilinear_inputs must map H and E
silent pad/[:d] after a successful fit must fail
ones-shape must not be the only map assertion
```

### CE-6 HumanEval isolation

```text
score_code(..., executor=spy): len(spy.calls)==1 and source/tests match
score_submission must accept executor or be shown to call score_code
source containing exec(: Spy.status==rejected  (implemented, untested)
static: no host exec/eval in scoring path
```

### CE-7 Probe math

```text
Hand h,e,U,V,b → σ(sum((hU)*(eV))+b)  (this channel: 0.731…; no test)
Y with nan / mask=0: weighted_bce equals known-only terms, λ_FN=10 on positives
Treating unknown as 0 must fail ( -1 case is partly covered )
Task head and behavior head must not share Y unless protocol says so
BoundaryMLP: hidden==256, ReLU, and a numeric logit oracle
```

### CE-8 Repair budget

```text
repairability(4,10)=0.6; full=0 → None  (impl yes; no test)
After run_repair, generated_tokens is not identically 0 or identically 2
unless the stage is declared non-executing and removed from “C4 implemented”
```

### CE-9 Week8 / REST

```text
gate_thresholds={"gate0":0.9} + measurements below / unregistered method
  → not decision="evaluated" without a comparison
measurements text "already decided" → forbidden_claims_blocked (implemented, untested)
```

### CE-10 Family id / official metadata / GSM-Plus status / T3 truth / iGSM mismatch

```text
assign_family(same members, family_id A vs B) must differ (impl does; test does not)
Loader: SHARED_RNG node present in JSON but excluded from premises — assert premises, not metadata True
Official dump answer ≠ template recompute must raise (impl does; test does not)
GSM-Plus "reversing operation": status must be a declared enum or explicit non-T4 field; query_reversed ∉ T4_STATUSES
document/paragraph/spec edit without new_answer must be needs_truth; with new_answer must write it
rename keeps values; source_value recomputes
```

### CE-11 Empty noise / sham-only

```text
noise_set=[] + sham_protocol → excess null, reason noise_set_empty (impl; no test)
Only sham:changed, no real obs → behavior must not become 1
```

### CE-12 Hook last-token and cache content / resume

```text
resid_post_hook: prefix tokens unchanged, last position transformed (impl; no test)
cache_isolated: compare cloned tensor contents, not `is not`
second condition must not see first-condition KV
--resume after mutating a hashed file must raise (impl; no test)
```

## 9. Findings

### F3-00 Declared freeze hash recomputes

- **Severity:** —
- **Status:** 非缺陷建议 (process OK this round)
- **Files:** `.planning/audits/round-03/VERSION.md` L5–21; working tree 55 files
- **Repro:** §1. Local `67bb9c90…` == declared.
- **Note:** Fixtures remain outside the digest (F3-14). Consecutive-pass counting can start only if A–F all pass on this hash; this channel files confirmed defects.

### F3-01 CLI / Goal e2e tests accept an unconnected science path

- **Severity:** Critical
- **Status:** confirmed defect (verification; implementation still stubbed after label/fit)
- **Files/lines:** `tests/test_cli_pipeline.py` L4–29; `tests/test_review_regressions.py` `test_pipeline_consumes_upstream` L358–371, `test_e04_*` L281–288; `cli.py` `cmd_collect` L269–277, `cmd_calibrate` L366–375, `cmd_intervene` L400–415, `cmd_analyze` L445–460
- **Trigger:** documented eight-command chain
- **Requirement:** Goal §六 “从生产入口验证跨模块数据流”; OPS-01 / QA-01
- **Repro:** §3. Prefix-id `H`; calibrate `[1-loss,…]`; intervene norms 0 / `geometry_only`; analyze ignores labels
- **Impact:** 70 passed + runbook commands can be cited as “pipeline works” while P1–P3 never see labels
- **Fix:** CE-1; one run dir; analyze must hash-check upstream labels or refuse; stop asserting `not_evaluated` as the only success

### F3-02 P1 tests lock a linear substitute and do not prove holdout

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `analysis.py` `p1_incremental` L43–64, `_fit_scores` L27–30; `tests/test_review_regressions.py` L201–225, L353–355; `tests/test_science.py` L64–66
- **Trigger:** two-class data; optional `held_out` / `precomputed`
- **Requirement:** Goal §五.12 / C3-01 logistic length+op, incremental AUC
- **Repro:** default `requires_held_out` is real (new test). `precomputed` still `length+0.01*op`. Holdout test stays green if all rows are used in lstsq (this channel: leaky `auc_base=0.979` still `is not None`)
- **Impact:** Main-text P1 numbers can come from the wrong estimator with a green suite
- **Fix:** CE-2
- **Author claim C2-M-02:** default gate **closed**; logistic + leak-proof **not closed**

### F3-03 Conformal `predict_set` and sequence units are not synthesized

- **Severity:** High
- **Status:** confirmed defect (coverage); α≥1 wrap is **closed** by C-02
- **Files/lines:** `probes/calibrate.py` L9–23, L39–42; `tests/test_science.py` L20–27
- **Trigger:** non-palindromic `p_hat`; call `predict_set`
- **Requirement:** Goal §五.8 / PROP2-01
- **Repro:** `[0.7,0.4]` distinguishes `max(p)` vs `max(1-p)`; tests use palindrome; `predict_set` unused; CLI `one_minus_p` untested
- **Fix:** CE-3
- **Author claim C2-M-03:** **not closed** (slack/`predict_set` never observed)

### F3-04 HumanEval tests still do not observe the executor

- **Severity:** High
- **Status:** confirmed defect (verification)
- **Files/lines:** `tests/test_t3_t4.py` L29–35; `executor.py` L42–46; `t3_humaneval.py` L60–61
- **Trigger:** `score_code(..., executor=spy)` without `spy.calls`; `score_submission` default backend
- **Requirement:** Goal §五.15 / EXEC-01
- **Repro:** hardcoded `executor_unavailable` passes; this channel: `ncalls==1`, `exec(` → `rejected`, both untested
- **Fix:** CE-6

### F3-05 Probe/Boundary/BCE math has no independent score/λ_FN/MLP oracle

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `probes/bilinear.py` `fit`/`score`/`weighted_bce` L21–76; `probes/boundary.py` entire file; CLI `cmd_fit` L351–355; `tests/test_review_regressions.py` L343–350
- **Trigger:** `reasoning-diff fit`; any prefix-id `H` + loss
- **Requirement:** Goal §五.7 / PROBE-01 / BOUND-01
- **Repro:** `-1` mask test is real; both CLI heads share Y and loss; zero `BoundaryMLP` / bilinear score oracles; λ_FN not independently locked
- **Fix:** CE-7
- **Author claim C2-M-01:** **partial** (`-1` only)

### F3-06 Repair/C4 tests accept a non-executing ledger

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `repair.py` L34–52; `tests/test_science.py` L76–80; `cli.py` `cmd_repair` L427–435
- **Trigger:** any legal mask
- **Requirement:** Goal §五.13 / REPAIR-01
- **Repro:** unit default `generated_tokens==0`; CLI `==2` from `[1,2]`; `repairability(4,10)==0.6` untested
- **Fix:** CE-8 or formally drop C4 from “implemented”

### F3-07 Week8 + REST: thresholds imply `evaluated`; ban-string untested

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `analysis.py` `week8_decision` L109–125; `tests/test_science.py` L56–61
- **Trigger:** nonempty `gate_thresholds`
- **Requirement:** Goal §五.14 / DECIDE-01 / REST-01..03
- **Repro:** §3; `"already decided"` is blocked in code and not in tests
- **Fix:** CE-9

### F3-08 Joint soundness flag is a constant; test cannot see `f≡0`

- **Severity:** Medium
- **Status:** confirmed defect (verification). Constant False is REST-03-conservative, not a fixture proof.
- **Files/lines:** `measure.py` L231–240; `tests/test_measure.py` L25–32
- **Repro:** `f≡0` → `soundness_claim_allowed is False` anyway
- **Fix:** CE-4

### F3-09 Transfer / verbalizer / Hotpot / T4 / official flags / T3 edits remain surface contracts

- **Severity:** Medium
- **Status:** confirmed defect (verification gap)
- **Files/lines:** `tests/test_science.py` L30–37, L69–73; `tests/test_t3_t4.py` L12–18, L38–40; `t1_official.py` L71–80; `t3_hotpot.py` L51–94; `t3_musique.py` L72–93; `t3_humaneval.py` L34–57; `t2_gsm_plus.py` L20–21; `edits.py` L144–184
- **Repro:** ones map is shape-only; Hotpot/MuSiQue/HumanEval edits without new truth; `query_reversed ∉ T4_STATUSES`; metadata hardcoded; rename/source_value/spec/paragraph **zero tests**; iGSM mismatch raise untested
- **Fix:** CE-5, CE-10
- **Author claims** (T3 edits, iGSM recompute, rename/source_value): **implementation present, verification not closed**

### F3-10 Family-id / leak-flag / tiny tautology / identity cache / last-token

- **Severity:** Medium
- **Status:** confirmed defect (verification)
- **Files/lines:** `tests/test_review_regressions.py` L184–193, L257–268; `tests/test_tiny_hooks.py` L17; `models/collect.py` L44; `models/tiny.py` L59–69; `models/features.py` L25–29
- **Requirement:** Goal §五.10–11; POS-01; DATA-03
- **Repro:** family_id required (good) but same-members different ids untested; `leaks_target` unreachable True; L17 tautology; cache `is not`; last-token prefix invariance implemented and untested
- **Fix:** CE-10, CE-12
- **Author claim B-13:** **partial** (required, not keyed)

### F3-11 Density/noise tests lock a set formula; B-26 empty-noise untested

- **Severity:** Medium
- **Status:** confirmed defect (coverage). Formula-vs-paper remains 未证实疑点; empty-noise is a **confirmed** verification gap.
- **Files/lines:** `measure.py` L100–111; `tests/test_measure.py`; `tests/test_tracer_t1_prepare.py` L58–77
- **Repro:** `noise_set=[]` → `noise_set_empty` (this channel). No `test_b26_*`.
- **Author claim B-26:** **not closed**

### F3-12 Large symbol set still has zero tests

- **Severity:** Medium (set). Several items already raised in F3-05/06/09.
- **Status:** confirmed defect (coverage)
- **Symbols with no test mention:** `BoundaryMLP`, `predict_set`, `p2_paired`, `apply_bilinear_inputs`, `apply_model_template`, `apply_rename_edit`, `apply_source_value_edit`, `apply_spec_edit`, `paragraph_edit`, `attention_rollout`, `text_predictor`, `forbid_host_exec`, `extract_answer`, `score_qa`, `rescue`, `intervention_report`, `cone_fit`, `procrustes`, `retrieval_scatter`, `bootstrap_cluster`, `assert_disjoint`, `card`, `catalog.load_snapshot`, `repairability`, `recompute_ratio`
- **Requirement:** Goal §六 “独立 oracle…不能让期望值调用同一待测函数”; §四 reverse coverage
- **Fix:** property/counterexample tests, not more status-string mirrors

### F3-13 Traceability ledger treats `pytest -q` as row-level evidence

- **Severity:** Medium
- **Status:** confirmed defect (verification ledger)
- **Files:** `.planning/PAPER_TRACEABILITY.md` TR-0002 and following (`verification_method=python -m pytest -q`, `local_verify_status=passed_local_tests`, text still `65 passed`)
- **Impact:** Goal §九.1 can be paper-checked as “filled” while no test exists for the row
- **Fix:** per-row command/oracle or `untested`

### F3-14 Fixtures excluded from freeze

- **Severity:** Medium
- **Status:** confirmed defect (freeze protocol)
- **Files:** `tests/fixtures/*.json`; `VERSION.md` scope
- **Impact:** oracle bytes can move without changing even a *correct* aggregate of `.py`+toml

### F3-15 ISSUES `fixed_pending_review` overstates verification closure

- **Severity:** Medium
- **Status:** confirmed defect (process)
- **Independently closed as verification (unit):** B-06 (parents≠text + mention), B-14 (gsm_plus→test), B-23 (non-exhaustive unknown), B-24 (decimal isolation), C-02 (α≥1), C-04 (norm), D-01 **indices**, B-01/02/04/07–11, default P1 `requires_held_out` (C2-M-02 **gate only**), BCE `-1` mask (C2-M-01 **partial**).
- **Not closed as verification:** C2-M-02 logistic/leak; C2-M-03 `predict_set`; B-13 keying; B-26 empty noise; CLI resume hashes; collect residual features; T3 spec/paragraph + truth writeback; iGSM mismatch; rename/source_value; C-01 leak/logistic; D-02 last-token; D-03/E-01 science path; E-04 stub encoded; E-08 hasattr.
- **Do not mark closed from this channel** except the unit list above, and only as *verification of those units*, not Goal/requirement Complete.

### F3-16 Real models / official dumps / isolated Linux runner

- **Severity:** —
- **Status:** 外部待验证
- **Note:** tiny random weights, `offline_prefix_ids`, and `executor_unavailable` must not be rewritten as server acceptance.

### F3-17 Non-defect notes

- **Status:** 非缺陷建议
- Hash algorithm in `VERSION.md` now reproduces (unlike this channel’s round-02 object). Keep the script frozen.
- `test_use_cache_false_*` is a useful transformers 5.5.3 regression if renamed to “known pollution,” with a separate fail-if-reused-cache test.
- Constant-False soundness flag matches REST-03 spirit; still needs CE-4.
- C-02 α≥1, D-01 unit indices, B-23/B-24, B-06 mention, and default P1 holdout gate are real improvements over earlier F reports.
- `STATE.md` “scientific metrics not_evaluated” is more honest than treating 70 passed as Goal §九.3. `06-VERIFICATION.md` still cites 65 passed.
- Last-token hook and iGSM recompute and `--resume` hash check look implemented; absence of tests is the defect, not a claim that those functions are wrong.

## 10. Goal §九 items 1–7 — verification quality only

This is **not** a Goal-complete declaration. It is whether the **current tests and recorded commands** could support each stop condition.

| Item | Stop condition (abbrev.) | Verification quality |
|---|---|---|
| 1 | Paper/protocol atoms have impl, entry, **verification evidence**; traceability has no unexplained gaps | **Unsupported.** Ledger cites `pytest -q` / `passed_local_tests` for rows the suite does not test (F3-13). Reverse coverage of production symbols fails (F3-12). |
| 2 | No confirmed unresolved in-scope defects; no unadjudicated correctness doubts | **Unsupported by this channel.** F3-01..F3-12 are confirmed verification/implementation defects. ISSUES remain `fixed_pending_review`. |
| 3 | All applicable local checks actually run and pass; meaningful e2e / boundary / failure paths covered; unrun items not disguised as pass | **Partial command, fail substance.** `pytest -q` did run, 70/0, no skip disguise. E2e is exit-code smoke. Failure paths (α=1, family_id missing, resume impl) mostly untested or unasserted. Analyze `not_evaluated` is asserted as success. |
| 4 | GSD phases match reality; software pass ≠ science/server pass | **Docs mixed.** `STATE.md` / runbook keep science pending (good). `06-VERIFICATION.md` still leads with 65 passed; traceability marks `passed_local_tests` on science-adjacent rows (bad). |
| 5 | Two consecutive independent full A–F, no new confirmed defects, **same hash** | **Cannot start a pass.** Hash matches (good). `VERSION.md` `consecutive_pass_count: 0`. This channel **files confirmed defects**. |
| 6 | Server-pending items listed with real paths / reasons / future commands | **Not a test-suite question.** Runbook lists commands. Missing code must not hide here: prefix-id collect, placeholder C-layer, and unavailable executor are code gaps with names, not only server waits. |
| 7 | Delivery pack: runbook, config, traceability, issue closure, reviews, local record, server entry | **Issue closure is not ready** (F3-15). Local pytest record exists (70/0). |

## 11. Channel verdict

| Judgment | Content |
|---|---|
| pytest | **70 passed, exit 0, 10.49s.** No skip/xfail. **Not** QA-01 / Goal §九.3 evidence. |
| Freeze | **HASH_MATCH.** Declared and recomputed `67bb9c90c639ceb0c8926e02476aa1fcde3a0fc9a6bce3b39f897fdf80d5756e` (55 files). Per-file SHA-256 in §2. |
| Independence | Real oracles exist for several B-fixes, C-02, C-04 norms, D-01 units, arithmetic edits/TO, default P1 holdout *gate*, `-1` BCE mask. CLI science, logistic P1, conformal composition, isolation, repair, probe score/λ_FN/MLP **do not**. |
| Mocks/stubs | CLI prefix-id `H` + four calibration numbers + analyze-ignores-labels + repair ledger + identity cache + placeholder C-layer. Worse than unittest.mock. |
| Paper behavior still unproven | Logistic P1, P2, C-layer **dev** selection, bilinear score/λ_FN/BoundaryMLP, `predict_set` units, donor/swap-on-residual, C4 recompute, isolated exec, T2/T3 truth updates, R^surf beyond two fixture lines |
| Delivery vs tests | “70 passed / defects closed / pipeline consumes upstream” **exceeds** test force |
| Confirmed problems? | **Yes.** Critical: F3-01. High: F3-02..F3-07. |
| Goal complete? | **No.** |
| Channel pass? | **Fail.** Empty “looks fine” is inapplicable. |

Until CE-class tests exist, any closing sentence of the form “code acceptance passed; independent review found no confirmed leftover defects” contradicts this channel’s evidence.
