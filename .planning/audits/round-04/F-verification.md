# F: verification quality and adversarial doubt (round-04)

Independent review channel F. Production tree, tests, and `pyproject.toml` were not modified. Pytest green is not treated as paper-correctness or Goal acceptance. Other round-04 channel reports were not read. `ISSUES.md` was read only as author claims; every claimed r03 closure was re-checked from tests vs production, then attacked with in-process counterexamples (no test files added).

**Lead conclusion:** `python -m pytest -q` is **97 passed / exit 0**. Freeze hash **recomputes**. That is not Goal acceptance. Several r03 unit holes now have real oracles (B-14 production key, B-24 `5.5`/`5.0`, C3-M-01 event mean, C3-M-03 denom, C3-M-07 empty-list null, conformal `[0.7,0.4]` + `predict_set`, bilinear σ/λ_FN, HumanEval `spy.calls`, D-08 `leaks_target`, E-17 labels hash). The CLI science path, holdout-leak P1, Week-8 flag tree, BoundaryMLP loss, C4 ledger, transfer numerical map, sham noise, last-token/once hooks, and `--eval-mode scientific` are still untested or tested by mirrors/stubs — and several of those still **misbehave** under an independent oracle. This channel **does not pass** and **does not declare Goal complete**.

## 1. Metadata

| Field | Value |
|---|---|
| agent / task | Independent Reviewer F / verification quality and adversarial doubt |
| review time | 2026-09-21 (Asia/Shanghai) |
| declared freeze | `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17` |
| recomputed aggregate | `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17` |
| hash verdict | **HASH_MATCH** |
| hash method used | 56 files: `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml` (no `__pycache__`). Sort by POSIX `relpath`. Update SHA-256 with `relpath.encode() + b"\0" + file_bytes`. Zero CRLF in scoped files. |
| file-count match | 56 files, matches `round-04/VERSION.md` (was 55 in r03; added `tests/test_round03_regressions.py`) |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d` (2026-09-20 23:54:47 +0800; working tree dirty; do not trust HEAD as the freeze) |
| pytest | **97 passed in 10.93s, exit 0.** Collect: **97 nodes**. No skip/xfail/deselected/`unittest.mock`/`assert True` tautology. One unused `monkeypatch` fixture. One `@pytest.mark.integration` (tiny hooks, 2 params) still **ran**. |
| scope | all `tests/**` (14 `.py` + 10 fixture JSON) and every production function those tests import or CLI-smoke; remaining production modules scanned for untested entry points |
| explicitly unread | `.planning/audits/round-04/{A,B,C,D,E}-*.md` |

Review object is the **current working-tree bytes** below. Author `pytest_author_claim: 97 passed` is independently confirmed as a command result only.

## 2. Per-file coverage

### 2.1 Tests (all read)

| File | Lines | File SHA-256 | What it actually binds |
|---:|---:|---|---|
| `tests/conftest.py` | 11 | `1b4eac7fa8e43fdb…` | `t1_tiny_path` only |
| `tests/test_artifacts.py` | 73 | `830953f379954233…` | JSONL/NPZ/run_spec/manifest digest; **no** `success_count` assert; **no** `--resume` |
| `tests/test_cli_pipeline.py` | 29 | `0cedc6188e5f64b1…` | eight-stage exit 0 + `report.status==not_evaluated` |
| `tests/test_generate_loop.py` | 17 | `ffe10b0d6812908c…` | Generator replay + greedy argmax |
| `tests/test_measure.py` | 40 | `fbc68abd89ed109e…` | set densities, joint `f=xy`, cone source strings |
| `tests/test_review_regressions.py` | 394 | `37414926677d0596…` | r01/r02 oracles + event-mean + default P1 gate + pipeline-to-fit |
| `tests/test_round03_regressions.py` | 288 | `70475c77edce6844…` | 27 new nodes; mixed independence (see §6) |
| `tests/test_science.py` | 97 | `3180ca3217882de5…` | conformal happy path, transfer **shape**, streams, Week8 unregistered, verbalizer, repair flags, swap |
| `tests/test_t1_official.py` | 31 | `f4b3cbc1fcd5371e…` | official shape/mod23/answer 12; config happy path |
| `tests/test_t2_gsm.py` | 33 | `f66a95bb737dc973…` | sidecar 5+3=8; Plus `fit_eligible`/`role` |
| `tests/test_t3_t4.py` | 44 | `d0381c097d04bc9d…` | Hotpot flags; HumanEval **`spy.calls` + `score_submission` + `exec(` reject** |
| `tests/test_tiny_cache.py` | 26 | `83ae0441140f7e17…` | cache mutation as expected; `cache_isolated is True` |
| `tests/test_tiny_hooks.py` | 27 | `e28e58b638568d89…` | hook effect + cleanup; L17 tautology |
| `tests/test_tracer_t1_prepare.py` | 100 | `62a5e2f168a20e8f…` | fixture prepare, identity, densities, TO, prepare CLI |
| `tests/fixtures/*.json` | 10 files | **outside freeze** | hand oracles |

Collect-only: **97 nodes**. Zero `skip` / `xfail` / `skipif` / `unittest.mock`. Zero `assert True` as an assertion (the string appears only inside HumanEval/`SubprocessExecutor` payloads). One tautology: `assert layer.__class__.forward` (`tests/test_tiny_hooks.py` L17). Unused `monkeypatch` on `test_p1_held_out_logistic_detects_rho`.

New vs r03 70-node suite: the 27 functions in `tests/test_round03_regressions.py`.

### 2.2 Production vs tests

| File | Lines | File SHA-256 | Test reach | Untested or only stub-touched |
|---|---:|---|---|---|
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` only | argv/`SystemExit` |
| `analysis.py` | 253 | `18adcce069d4b50e…` | P1 default gate, ρ-detect, precomputed *author case*, P2 denom, P3 echo, Week8 substring, cone `r2>0.9` | holdout **leak oracle**; Week8 **flag tree**; gate **threshold compare**; `procrustes`; `retrieval_scatter`; `bootstrap_cluster` |
| `artifacts.py` | 85 | `524657027e9b402f…` | digest self-check | `success_count` unasserted; resume only via CLI exception (no test) |
| `baselines.py` | 80 | `7c0f14a9dd90a877…` | verbalizer + `text_predictor` requires fit | `attention_mean`; `attention_rollout`; fiveshot fairness |
| `cli.py` | 658 | `c7b8061e036c9f83…` | exit codes; labels-dir hash; analyze-if-`p1_table` | default smoke: prefix-id `H`, calibrate `scores=None`, analyze ignores labels; `--eval-mode scientific` **zero tests**; E-16 leftover |
| `edits.py` | 258 | `0e8365ca08ea3db3…` | value/rename/op-reverse/5.5 | `apply_source_value_edit` **zero tests** |
| `events.py` | 154 | `c7f9c33ecb97d1d85…` | identity; equal-count `node_id`; extract_answer think | `scanned` is a constant; strategy detector is `status_field_only` |
| `executor.py` | 99 | `86b434ed3c8bbead…` | spy.calls + subprocess timeout/ok | `forbid_host_exec` unused; subprocess is host CPython, not a sandbox |
| `graphs.py` | 46 | `1c755e6f8d22e277…` | ancestors via fixture | empty-complete reject |
| `interventions.py` | 115 | `0ffdbb8805be7649…` | swap, INLP, C-rand norm, `ie_z`, rescue norms, weak layer | CLI C-layer uses **hardcoded** `{0:0.2,1:0.1,2:0.4}` not a dev split |
| `io.py` | 133 | `1a03b2f8d865bdd3…` | encode/jsonl/npz | corrupt JSONL line |
| `measure.py` | 320 | `b287249e03b49354…` | event-mean; empty `noise_set`→null | sham prepare still `noise_set_empty`; `soundness_claim_allowed` constant False |
| `models/__init__.py` | 1 | `0b7dd6c4dd852065…` | — | — |
| `models/adapters.py` | 42 | `c1992624026a1bf0…` | **zero tests** | `card` |
| `models/collect.py` | 60 | `fcfb9be8a3e7a3e9…` | flags; `cache_isolated is True` | isolation is object identity; CLI offline path does not call this |
| `models/features.py` | 39 | `0a9f0b8beb0185ae…` | D-01 indices + D-08 True | — |
| `models/generate.py` | 57 | `0ea73ab1e0da2dbe…` | replay/greedy | `apply_model_template` absent; top-p/k |
| `models/tiny.py` | 120 | `21725a183452bd06…` | hook cleanup + logits change | last-token-only and `once=True` **implemented, unasserted**; L17 tautology |
| `probes/__init__.py` | 3 | `3065196db28e929c…` | — | — |
| `probes/bilinear.py` | 95 | `52de70553b37dec6…` | σ oracle + λ_FN=10 on +class; `-1` mask | CLI dual-head **same Y/loss** on fixture |
| `probes/boundary.py` | 44 | `7f9d62ab84f9452c…` | `status==ok` + `predict.shape==(4,)` | Hidden=256 / ReLU / **loss sign** untested |
| `probes/calibrate.py` | 42 | `16609e8f7007aab4…` | `[0.7,0.4]` units + `predict_set` | `+1e-12` slack load-bearing; CLI default still `scores=None` |
| `repair.py` | 73 | `9fa3ddbe26334273…` | `repairability(4,10)==0.6`; `len([9,8])==2` | no model decode; CLI `generated_ids` missing → 0 |
| `rng.py` | 53 | `2098c2c72a852eaa…` | two scalars unequal | snapshot/restore |
| `schema.py` | 384 | `b61ee242b0a5bcbc…` | enums, identity exclude values | `Event.from_dict` rejects extras; `Label` has no `from_dict` |
| `scoring.py` | 30 | `d05822c4fb784fe4…` | code via spy | `score_qa` **zero tests** |
| `splits.py` | 97 | `2bc45ed0bbce3a5c…` | Plus→test even on `gsm8k-1`; `fit_eligible` | `assert_disjoint` **zero tests** |
| `tasks/catalog.py` | 39 | `5d3918394b1603bb…` | **zero tests** | `iter_snapshot_files` / `load_snapshot` |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | legal config only | reject ops/mod/n≠500 |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 92 | `5c1432f736969031…` | ancestors/mod/12; mismatch raise | `shared_rng_excluded` still hardcoded True |
| `tasks/t2_gsm_plus.py` | 52 | `606e4a09cfcbd8d9…` | test-only + placeholder kind | `"reversing operation"` not a T4 status; **no test** |
| `tasks/t2_gsm_symbolic.py` | 84 | `067af473ddb143b7…` | sidecar edit | no-sidecar placeholder premises |
| `tasks/t2_noop.py` | 93 | `9329d9b1e2e91dad…` | front span + metadata | `answer_unchanged_proven` **implemented, unasserted** |
| `tasks/t3_hotpot.py` | 104 | `b86ca7dffd774606…` | support≠DAG | `new_answer` writeback unasserted |
| `tasks/t3_humaneval.py` | 62 | `398a8ab68104fb98…` | family id; spy; spec `needs_truth` | isolated true exec still unavailable by default |
| `tasks/t3_musique.py` | 103 | `9587aa9662b1c1d7…` | pair ids; paragraph `needs_truth` | `new_answer` writeback unasserted |
| `tasks/t4_boundary.py` | 33 | `aab4821f407c0f06…` | set equality | illegal status |
| `transfer.py` | 52 | `c58e673a5bc96841…` | 4096/3584; labeled **requires labels**; **shape only** | `apply_map(tgt)≈src` recovers in impl; **not asserted** |

Fixture JSON is **not** in the freeze.

## 3. Checks run and results

| Check | Command / method | Result |
|---|---|---|
| Freeze hash | `VERSION.md` script verbatim | **HASH_MATCH** `fb1e3dfa…` (56 files, POSIX relpath + NUL + bytes). |
| Full pytest | `python -m pytest -q` at repo root (`pythonpath=src`) | **97 passed in 10.93s, exit code 0**. No skip/xfail/deselected. |
| Collect | `python -m pytest tests --collect-only -q` | 97 nodes, collect exit 0 |
| skip/xfail/`assert True` | ripgrep on `tests/**` | no skip/xfail/mock; tautology at `test_tiny_hooks.py` L17; unused `monkeypatch` |
| Hand oracles | iGSM `4*3 % 23 = 12`; sidecar `5+3=8`; TO `2·LCS([1,2],[1,3])/4=0.5`; σ(1)=0.731…; 10·(-log 0.8); `repairability(4,10)=0.6`; `[0.7,0.4]` units | those **unit** assertions that exist match independent arithmetic |
| Adversarial: CLI offline chain | prepare→…→analyze on `t1_tiny` `--backend offline` | `H=[[1..8]]`, `weight_source=offline_prefix_ids`; both heads **same loss** `0.05036…`; calibrate `scores=None` / `probe_weights_or_features_missing`; intervene `donor_missing` / all norms None; repair `generated_tokens=0`, budget=20; analyze `p1/p2/p3=None`, `status=not_evaluated` while `labels.jsonl` has 1 row |
| Adversarial: CLI tiny + `--features-dir` | collect tiny; calibrate with features | `H` shape `(2,32)`, `weight_source=random_init`; calibrate finite `one_minus_p` scores; **analyze still `p1 is None` / `not_evaluated`** |
| Adversarial: `--eval-mode scientific` | prepare / collect-offline / calibrate / analyze | all **raise** as coded; **zero tests** |
| Adversarial: E-16 | `analyze --in-dir` a file | `NotADirectoryError`; leftover `report.json` + `failure.json` + `manifest.json` |
| Adversarial: E-09 | prepare missing fixture | `failure.json` + `success_count=0` / `failure_count=1` — **no test** |
| Adversarial: B-12 sham | `--sham-opportunities 1` | sham `premise_id=""`; extra label `('q','',0.0,None)`; event `null_reason=noise_set_empty`; all ρ None |
| Adversarial: P1 leak | eval-only `rho=y`, length/op noise, n=80 | honest ΔAUC=`0.0` (`auc=0.42`); leaky-all-rows ΔAUC=`0.45` (`auc_full=0.885`). Existing `test_p1_held_out_logistic_detects_rho` **still passes** a leaky impl (`auc_full=1`, `delta>0`). `test_c01_held_out_*` only checks `auc_base is not None` |
| Adversarial: precomputed | length=`[1,0,1,0]`, rho=`y` | current Δ=`0.5`; old magic `len+0.01*op+rho` Δ=`0.375`. Author test (`length==rho`, `op=0`) Δ=`0` under **both** — **does not fail the old magic** |
| Adversarial: conformal | `[0.7,0.4]` | `max(p)=0.7`, `max(1-p)=0.6`; `predict_set(...,0.3)=[T,F]`; `1-0.7<=0.3` is False without `+1e-12` |
| Adversarial: spy | `score_code` / `score_submission` / `exec(` | `ncalls` increments; default backend `UnavailableExecutor`. Suite now asserts this |
| Adversarial: bilinear | hand U,V,b | `score=0.7310585786300049` matches σ(1). Suite now asserts this |
| Adversarial: BoundaryMLP | 2-point BCE | impl loss formula → `0.0`; correct BCE → `0.223…`. Fit path reports **negative** loss. Suite only checks `status==ok` and shape |
| Adversarial: repair | `[9,8]` vs default | `generated_tokens=2` vs `0`. Ledger. Suite asserts the ledger |
| Adversarial: Week8 | flags vs thresholds | `"already decided"` substring works (tested). `{gate0:0.9}` → gate **`evaluated` with no measurement compare**. `{measurement_unresolved:True}` / `{c3_negative:True}` / `{p1_failed:True}` / `{evaluated:True}` all stay **`not_evaluated`** unless `rho_S_excess` is set |
| Adversarial: transfer | `src=I`, `tgt=diag(2,3)` | `apply_map` recovers `I` (impl). Suite asserts **shape only** |
| Adversarial: empty noise | `noise_set=[]` + hits | `null_reason=noise_set_empty` (tested). Observed empty set is indistinguishable from missing N |
| Adversarial: hook | tiny layer-1 | transform input shape `(1,1,32)` last-token only; `once=True` fires **1** of 2 forwards. **Not asserted** |
| Adversarial: clone_cache | after decode | new object, new storage, `is_initialized` copied; a follow-up step ran. **No test** |
| Adversarial: D-08 | `[[0,10]]` @ 3 | `leaks_target is True` (tested) |
| Adversarial: B-14 | `assign_split("gsm8k-1")==probe_train`; Plus `original_id=gsm8k-1` | `split_for_task` / token `gsm_plus:` → `test`. Test covers this |
| Adversarial: B-24 | `5.5`/`5.0` value `"5"` | both raise. Test covers this |
| Adversarial: B-21 | Plus `"reversing operation"` | `answer_spec.status is None` (∉ T4); metadata `query_target_change`. **No test** |
| Adversarial: B-10 | noop front | `answer_unchanged_proven is True`. **Unasserted** |
| Adversarial: B-05 | align | `scanned is False` always; `strategy_detector=status_field_only` |
| Adversarial: resume | mutate `traces.jsonl` then `--resume` | raises `resume hash mismatch` — **no test** |
| Adversarial: joint `f≡0` | `joint_edit_counterexample` | `joint_changed=False` but `soundness_claim_allowed=False` still (constant) |

## 4. Checks not run, and why

| Not run | Reason |
|---|---|
| Real HF weights, official full dumps, GPU/CUDA KV | out of scope / `pending_server` |
| Linux cgroup / true isolated sandbox for HumanEval | only `UnavailableExecutor` / `SpyExecutor` / host `subprocess` |
| Other round-04 channel reports | forbidden |
| Editing production or adding regressions | forbidden; counterexamples are protocol-only in §8 |
| Line-by-line audit of `transformers`/`torch` | project usage only |

## 5. Delivery claims vs what tests prove

| Claim | Location | Do tests support it? |
|---|---|---|
| `python -m pytest -q` → 97 passed | `VERSION.md` L9 | **Command yes.** Using it as phase/Goal evidence: **no.** |
| r03 items closed locally, pending independent close | `ISSUES.md` | **Partial.** See §9 F4-15. Several unit closures hold. Several author closures have **no** independent test, or the impl is still wrong (A3-20, B-12, E-16, BoundaryMLP loss, P1 leak, CLI science). |
| CLI pipeline / stages consume upstream | `test_full_cli_smoke`; `test_pipeline_consumes_upstream`; `test_analyze_uses_p1_table` | Files are read. Science is **not**: default collect is prefix-id `H`; default calibrate writes `scores=None`; analyze on labels stays `not_evaluated`; `test_analyze_uses_p1_table` only asserts `p1 is not None` on a hand table. |
| Traceability `verification_method=python -m pytest -q` | `.planning/PAPER_TRACEABILITY.md` TR-0002+ | **Cannot.** Ledger still says `passed_local_tests` / **`65 passed`**. |
| Goal §九 items 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **Not evidenced by this suite.** See §10. This channel **does not** declare Goal complete. |
| Author pytest claim 97 | `VERSION.md` | Independently confirmed: 97 / exit 0. |

## 6. Are tests independently valid?

### 6.1 Independent oracles (would fail a wrong impl)

**Still closed from earlier rounds (re-checked):** B-01 missing noise null; B-02/B-23 unknown; B-03 sham∉R_behavior; B-04 deletion rematch; B-06 surface≠parents + mention; B-07 HumanEval/0; B-08 sidecar 8; B-09 numeral isolation; B-10 **span** (not answer proof); B-11 empty parents; B-13 `family_id` required; B-14 **source=/test_only**; C-02 α≥1; C-03 INLP; C-04 norms; D-01 indices; default P1 `requires_held_out`; `-1` BCE mask; fixture arithmetic/TO; swap formula; encode NaN.

**Newly independent this freeze:**

- `test_b14_plus_family_key_stays_test_even_when_hash_would_train`: `assign_split("gsm8k-1")==probe_train` but `source="gsm_plus"` / loaded Plus → `test`. This channel confirmed the `gsm8k-1` hash is `probe_train`.
- `test_b24_integer_does_not_edit_trailing_decimal` / extended `test_b24_*`: `5.5`/`5.0` with value `"5"` raise.
- `test_c3_m01_event_mean_not_union` / `test_rho_event_mean_is_not_union`: mean 0.25 / 0.5, not union.
- `test_c3_m07_empty_noise_ignores_hits`: `noise_set=[]` + protocol hits → null (fails an impl that substitutes hits as N).
- `test_p2_inconsistent_denom_is_null`: `99` vs `["p1"]`.
- `test_sequence_score_units_and_predict_set`: `[0.7,0.4]` distinguishes `max(p)` vs `max(1-p)`; `predict_set` membership.
- `test_bilinear_score_and_fn_weight`: σ(1) and `10·(-log 0.8)`.
- `test_humaneval_never_host_exec`: `len(spy.calls)` 1 then 2; `score_submission` takes executor; `exec(` → `rejected`.
- `test_d01_*` leak half: `leaks_target is True` on a straddling token (D-08).
- `test_align_equal_count_requires_same_node`: `q` vs `r` → no pair (B-04 residual).
- `test_extract_answer_ignores_open_think`: open `<think>` → None; boxed 7.
- `test_igsm_mismatch_raises`.
- `test_fit_hashes_labels_dir`: `labels.jsonl` appears in `input_hashes` (E-17).
- `test_repairability_and_budget` **formula half**: `repairability(4,10)==0.6`.
- `test_subprocess_executor_timeout_and_ok`: child timeout vs `x=1` (proves **host CPython child**, not a sandbox).
- `test_p3_reports_nontarget` **vs_baseline half**: `0.5-0.45=0.05`.
- `test_text_predictor_requires_fit`: unfitted raises.
- `test_labeled_transfer_needs_labels`: labeled without tensor raises.
- `test_spec_and_paragraph_need_truth`: `needs_truth` without new answer.
- `test_rename_keeps_expression`: `p1 * p2` unchanged.

### 6.2 Invalid, self-referential, or too weak

| Test | Why it does not prove paper behavior |
|---|---|
| `test_full_cli_smoke` | Exit 0 + `not_evaluated`. This channel’s offline run is exactly prefix-id `H`, `scores=None`, P1 None. |
| `test_e04_analyze_manifest_includes_report` | **Encodes the stub** (`status==not_evaluated`). |
| `test_pipeline_consumes_upstream` | Stops at fit; any finite `loss` on prefix-id `H` passes. |
| `test_analyze_uses_p1_table` | Only `p1 is not None`. A stub `if table: p1={}` passes. Does not consume `labels.jsonl`. |
| `test_p1_held_out_logistic_detects_rho` | `rho=y` on **all** rows. Leaky fit-on-all still `auc_full=1` and `delta>0`. Unused `monkeypatch`. |
| `test_c01_held_out_fit_does_not_use_eval_rows` | `held_out is True` and `auc_base is not None`. Leaky stays green. |
| `test_p1_precomputed_is_scores_not_magic` / `test_c01_auc_*` | `length==rho`, `op=0`. Old magic `len+0.01*op+rho` also yields Δ=`0`. |
| `test_p1_null_on_single_class` | Any `unique(y)<2 → None` stub passes. |
| `test_conformal_examples` | Palindrome `[0.1,0.9]` still does not distinguish units (new test does). |
| `test_boundary_mlp_trains` | `status==ok` + shape. Hides wrong BCE sign (this channel: impl 0 vs correct 0.223). |
| `test_cone_fit_returns_r2` | `r2>0.9` on data from the same family. Stub `r2=0.95` passes. Recovered λ/γ were 0.68/1.2 vs 0.8/1.5. |
| `test_repairability_and_budget` **ledger half** | `generated_tokens==len([9,8])`. Any counter of the caller list passes. |
| `test_week8_blocks_already_decided` | Substring in `str(measurements)`. Does not compare a gate threshold to a measurement. |
| `test_week8_never_passes_unregistered` | Empty thresholds only. |
| `test_p3_reports_nontarget` **nontarget half** | Echoes the argument. |
| `test_direct_transfer` / `test_labeled_transfer_needs_labels` map | unlabeled/labeled **shape**. This channel: `apply_map` already recovers `I`; test would not notice `return ones_like`. |
| `test_align_equal_count_requires_same_node` `scanned is False` | Mirrors a **hardcoded** `scanned=False`. |
| `test_b14_*` `kind==placeholder` | Documents B-17 stub as the expected outcome. |
| `test_tiny_hooks` L17 | `assert layer.__class__.forward` is true for any class with `forward`. Last-token / `once` untested. |
| `test_collect_and_intervene_tiny` `cache_isolated` | `is not` on cache objects. `past_key_values=None` guarantees a new object. |
| `test_joint_edit_blocks_soundness` | `soundness_claim_allowed` is constant False. `f≡0` still False. |
| `test_operator_reverse` | Only `"/"` in expression. Any flip-to-slash stub passes. |
| `test_ie_z_and_rescue_controls` | Arithmetic of means/norms; not a causal effect. |
| `test_e02_*` / `test_e08_*` / `test_e06_*` | Non-identity edit; `hasattr`; leftover tmp after success. |

## 7. Mocks / stubs that hide unconnected paths

Almost no `unittest.mock`. Internal stubs still do that job.

1. **CLI science path still disconnected (F4-01).** `--in-dir` is parsed; labels-dir is hashed (E-17 real). Then:
   - Default **tested** collect is `--backend offline` → `H` from `token_ids[:8]`, `offline_prefix_ids`.
   - `cmd_fit` trains two heads; on the fixture both get the **same Y** and the **same loss**.
   - `cmd_calibrate` without `--features-dir` (the smoke) writes `scores=None`. Scientific mode would refuse — **untested**.
   - `cmd_intervene` on 1-row offline `H` → `donor_missing`, accuracies None. Tiny path uses **hardcoded** layer scores, not a dev split.
   - `cmd_analyze` on `labels.jsonl` never builds P1. `test_full_cli_smoke` / `test_e04` **expect** `not_evaluated`.
   - `cmd_repair` counts `generated_ids` or `[]` → 0. No decode.
2. **`--eval-mode scientific` is a side door (F4-18).** Refusals exist in code and have **zero tests**. Fixture mode remains the documented green path.
3. **Week-8 tree is a string/status switch (F4-07).** Flags are swallowed when `rho_S_excess is None` and `status` defaults to `not_evaluated`. Thresholds mark `evaluated` without a comparison.
4. **Repair is still a ledger (F4-06).**
5. **BoundaryMLP.fit is a shape stub over a wrong loss (F4-05).**
6. **HumanEval isolation is now observed (spy) but not a sandbox (F4-04).** `SubprocessExecutor` runs `sys.executable` on a temp file. Goal §五.15 forbids calling that an isolated sandbox.
7. **Symbols with no test mention:** `attention_rollout`, `apply_source_value_edit`, `forbid_host_exec`, `assert_disjoint`, `procrustes`, `retrieval_scatter`, `bootstrap_cluster`, `score_qa`, `catalog.load_snapshot`, `apply_model_template` (absent).

## 8. Counterexamples that should fail a wrong impl (current tests will not)

These were executed in-process. This channel did not add tests.

### CE-1 CLI analyze must consume labels or refuse

- Construct: prepare writes `labels.jsonl`; run analyze `--in-dir` that dir (the smoke).
- Expect: refuse, or P1 from those labels with a frozen oracle.
- Current: exit 0, `p1 is None`, `status=not_evaluated`.
- `test_e04` / `test_full_cli_smoke` **require** that stub.
- Tiny collect + `--features-dir` still leaves analyze `not_evaluated`.

### CE-2 Held-out P1 leakage + precomputed

```text
n=80, length/op ~ N(0,1), y alternating, held_out = last half
rho = noise on train, rho = y on eval only
Oracle (this channel): honest ΔAUC = 0.0 (auc 0.42 / 0.42)
Wrong fit-on-all logistic: ΔAUC = 0.45 (auc_full 0.885)
test_p1_held_out_logistic_detects_rho / test_c01_held_out stay green

precomputed: length=[1,0,1,0], y=rho=[0,0,1,1]
current Δ=0.5; old magic Δ=0.375
author test length==rho, op=0 → Δ=0 under both
```

### CE-3 Conformal units (partially now locked)

```text
[0.7,0.4]: max(p)=0.7 vs max(1-p)=0.6   ← test now locks
predict_set([0.7,0.4], 0.3) = [T,F]     ← test now locks
1-0.7 <= 0.3 is False; +1e-12 makes True  ← slack still untested as load-bearing
CLI smoke still scores=None; scientific refuse untested
```

### CE-4 HumanEval isolation (spy locked; sandbox not)

```text
score_code(..., executor=spy): len(spy.calls) increments   ← test now locks
score_submission accepts executor                         ← test now locks
exec( → rejected                                          ← test now locks
SubprocessExecutor(sys.executable) is host CPython        ← Goal §五.15 residual
```

### CE-5 Probe math

```text
sigma(h^T U V^T e + b) and lambda_FN=10 on +class          ← test now locks
BoundaryMLP: impl loss = -(y log p - (1-y) log(1-p))
  2-point (p=[0.8,0.2], y=[1,0]): impl 0.0 vs BCE 0.223
test_boundary_mlp_trains stays green
CLI task/behavior heads share Y on t1_tiny (same loss)
```

### CE-6 Repair budget

```text
repairability(4,10)=0.6                                    ← test now locks
run_repair(..., generated_tokens=[9,8]).generated_tokens==2
  is len(list), not decode
CLI traces without generated_ids → 0 (this channel)
```

### CE-7 Week8 / REST

```text
measurements note "already decided" → blocked              ← test now locks
gate_thresholds={"gate0":0.9} → gates.gate0.decision=="evaluated"
  with no comparison to any measurement
{"measurement_unresolved": True} → status stays not_evaluated
  unless rho_S_excess is also set
```

### CE-8 Transfer numerical

```text
src=I_2, tgt=diag(2,3), labeled lstsq
apply_map(tgt,W) == I     (this channel: True; test checks shape only)
apply_bilinear_inputs maps H and E to I  (True; unasserted)
```

### CE-9 Empty noise / sham

```text
noise_set=[] + hits → null                                 ← test now locks
prepare --sham-opportunities 1:
  sham premise_id=""; extra label ('q','',None);
  event null_reason=noise_set_empty; all ρ None
Observed N=∅ cannot be told from missing N
```

### CE-10 Hook last-token / once / resume / E-16

```text
resid_post_hook: transform sees (1,1,32); prefix not passed  (impl; no test)
once=True: 2 forwards → 1 transform call                   (impl; no test)
--resume after mutating hashed traces raises               (impl; no test)
analyze --in-dir <file> leaves report.json                 (impl defect; no test)
```

## 9. Findings

### F4-00 Declared freeze hash recomputes

- **Severity:** —
- **Status:** 非缺陷建议 (process OK this round)
- **Files:** `.planning/audits/round-04/VERSION.md` L5–23; working tree 56 files
- **Repro:** §1. Local `fb1e3dfa…` == declared. 0 CRLF.
- **Note:** Fixtures remain outside the digest (F4-14). Consecutive-pass counting cannot start while this channel files confirmed defects.

### F4-01 CLI / Goal e2e tests still accept an unconnected science path

- **Severity:** Critical
- **Status:** confirmed defect (verification; implementation still stubbed after label/fit)
- **Files/lines:** `tests/test_cli_pipeline.py` L4–29; `tests/test_review_regressions.py` `test_pipeline_consumes_upstream` L381–394, `test_e04_*` L287–294; `tests/test_round03_regressions.py` `test_analyze_uses_p1_table` L253–271; `cli.py` `cmd_collect` L324–330, `cmd_calibrate` L417–442, `cmd_intervene` L445–503, `cmd_analyze` L525–584, `cmd_repair` L507–522
- **Trigger:** documented eight-command chain (offline, the tested path)
- **Requirement:** Goal §六 “从生产入口验证跨模块数据流”; OPS-01 / QA-01
- **Repro:** §3. Prefix-id `H=[[1..8]]`; calibrate `scores=None`; intervene `donor_missing`; repair `generated_tokens=0`; analyze ignores labels
- **Impact:** 97 passed + runbook commands can be cited as “pipeline works” while P1–P3 never see labels
- **Fix:** CE-1; one run dir; analyze must hash-check upstream labels or refuse; stop asserting `not_evaluated` as the only success; if fixture mode is non-science, do not use it as Goal e2e evidence

### F4-02 P1 tests lock estimator *names*, not holdout or non-magic scores

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `analysis.py` `p1_incremental` L41–81, `_fit_scores` L27–38; `tests/test_round03_regressions.py` L72–91; `tests/test_review_regressions.py` L206–230
- **Trigger:** two-class data; optional `held_out` / `precomputed`
- **Requirement:** Goal §五.12 / C3-01 logistic length+op, incremental AUC on **held-out** rows
- **Repro:** IRLS logistic is real (improvement). Default `requires_held_out` is real. Leak: eval-only `rho=y` → honest Δ=`0`, leaky Δ=`0.45`; existing tests stay green. Precomputed author case does not fail `length+0.01*op+rho`
- **Impact:** Main-text P1 numbers can come from a leaky fit with a green suite
- **Fix:** CE-2
- **Author claim C3-M-02:** logistic **partial**; leak-proof / non-magic **not closed**

### F4-03 Conformal composition is unit-tested; CLI still does not use it

- **Severity:** Medium (was High in r03; units closed)
- **Status:** confirmed defect (CLI/coverage). α≥1 and `[0.7,0.4]` / `predict_set` **closed**
- **Files/lines:** `probes/calibrate.py` L9–42; `cli.py` L426–442; `tests/test_round03_regressions.py` L106–111; `tests/test_science.py` L20–27
- **Repro:** units match independent arithmetic. Smoke calibrate writes `scores=None`. `1-0.7<=0.3` needs `+1e-12`. Scientific refuse untested
- **Fix:** CE-3 on the CLI path; keep the new unit test
- **Author claim C3-M-04:** **partial** (units yes; CLI science no)

### F4-04 HumanEval spy is now observed; subprocess is not a sandbox

- **Severity:** Medium (spy verification **closed**; EXEC-01 residual)
- **Status:** confirmed defect (Goal §五.15 overclaim if subprocess is treated as isolation)
- **Files/lines:** `tests/test_t3_t4.py` L29–39; `tests/test_round03_regressions.py` L172–179; `executor.py` L55–84, L87–92
- **Repro:** spy.calls/rejected locked. `SubprocessExecutor` runs `sys.executable` on `source+tests`. Default `get_executor()` is still `UnavailableExecutor`
- **Fix:** keep spy oracles; do not name host subprocess as EXEC-01 isolation; pending_server for cgroup

### F4-05 BoundaryMLP loss is wrong; fit test is a shape stub

- **Severity:** High
- **Status:** confirmed defect (implementation + verification)
- **Files/lines:** `probes/boundary.py` L43; `tests/test_round03_regressions.py` L127–133; CLI `cmd_fit` L407–412
- **Trigger:** `BoundaryMLP.fit`; any `status==ok` + `predict.shape`
- **Requirement:** Goal §五.7 / BOUND-01; Goal §六 independent oracle
- **Repro:** loss = `-(y log p - (1-y) log(1-p))` = `-y log p + (1-y) log(1-p)`. 2-point oracle: impl `0.0`, correct BCE `0.223…`. Fitted path reported negative loss. Dual-head CLI losses identical on t1_tiny
- **Fix:** CE-5; assert Hidden=256, ReLU, numeric BCE, and distinct task/behavior Y
- **Author claims** BoundaryMLP.fit / dual-head Y / bilinear persist: bilinear σ/λ_FN **closed**; MLP/Y **not**

### F4-06 Repair/C4 tests accept a non-executing ledger

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `repair.py` L41–61, L64–67; `tests/test_round03_regressions.py` L144–150; `tests/test_science.py` L76–80; `cli.py` L511–521
- **Requirement:** Goal §五.13 / REPAIR-01
- **Repro:** `repairability(4,10)==0.6` is real. `generated_tokens` is `len(caller list)`. CLI missing `generated_ids` → 0 (no longer hardcoded `[1,2]`, still a ledger)
- **Fix:** CE-6 or formally drop C4 from “implemented”
- **Author claim C3-M-06:** **partial** (formula only)

### F4-07 Week8 flag tree is dead; thresholds imply `evaluated` without a compare

- **Severity:** High
- **Status:** confirmed defect (implementation + verification)
- **Files/lines:** `analysis.py` `week8_decision` L159–188; `tests/test_round03_regressions.py` L153–156; `tests/test_science.py` L56–61
- **Trigger:** default `status=not_evaluated` and `rho_S_excess is None` (the analyze path)
- **Requirement:** Goal §五.14 / DECIDE-01 / REST-01..03; author A3-20
- **Repro:** `"already decided"` substring works (tested). `{gate0:0.9}` → `decision=="evaluated"` with no measurement. `{measurement_unresolved:True}` / `{c3_negative:True}` / `{p1_failed:True}` / `{evaluated:True}` all remain `not_evaluated` until excess is set. Only an explicit `status=` string survives
- **Fix:** CE-7
- **Author claim A3-20:** **not closed** — this is a new confirmed leftover of the claimed fix

### F4-08 Joint soundness flag is still a constant

- **Severity:** Medium
- **Status:** confirmed defect (verification)
- **Files/lines:** `measure.py` L303–312; `tests/test_measure.py` L25–32
- **Repro:** `f≡0` → `soundness_claim_allowed is False` anyway
- **Fix:** derive the flag from `(single_ok ∧ joint_changed)` or mark the fixture invalid

### F4-09 Transfer / Plus perturbation / T3 truth remain surface contracts

- **Severity:** Medium
- **Status:** confirmed defect (verification gap)
- **Files/lines:** `tests/test_science.py` L30–37; `tests/test_round03_regressions.py` L198–214, L281–288; `transfer.py` L19–52; `t2_gsm_plus.py` L16–44
- **Repro:** labeled map recovers `I` (impl) but tests check shape; Plus `"reversing operation"` is not a T4 status and is untested; Hotpot/MuSiQue `new_answer` writeback unasserted; `apply_source_value_edit` zero tests
- **Fix:** CE-8 + a reversing-operation record
- **Author claim B-21:** **not closed** as verification

### F4-10 Last-token / once / tautology / identity cache / B-05 mirror

- **Severity:** Medium
- **Status:** confirmed defect (verification). Last-token and `once=True` **look implemented**
- **Files/lines:** `tests/test_tiny_hooks.py` L17; `models/tiny.py` L55–73; `models/collect.py` L46–57; `events.py` L119–127; `tests/test_round03_regressions.py` L159–164
- **Requirement:** Goal §五.10–11; D-07; B-05
- **Repro:** transform input `(1,1,32)`; `once=True` fires once; L17 tautology; `cache_isolated` is `is not`; `scanned=False` is a constant that the new test asserts
- **Fix:** CE-10; assert prefix invariance and second-forward no-op; detect strategy from status **or** stop claiming a scan
- **Author claims D-07 / B-05:** impl present / constant; **verification not closed** (B-05 test is a mirror)

### F4-11 Sham/empty-noise over-nulls; B-12 not closed

- **Severity:** Medium
- **Status:** confirmed defect (implementation + verification gap)
- **Files/lines:** `measure.py` L128–133, L265–300; `cli.py` L214–242; `tests/test_round03_regressions.py` L60–69
- **Repro:** `test_c3_m07` correctly forbids treating protocol hits as N. Prepare+sham still writes `premise_id=""`, a junk label, and `noise_set_empty`, so excess stays null. Observed `N=∅` cannot be represented
- **Author claims C3-M-07 / B-12:** C3-M-07 **closed for the stated empty-list spec**; B-12 **not closed**

### F4-12 Large symbol set still has zero tests

- **Severity:** Medium (set)
- **Status:** confirmed defect (coverage)
- **Symbols with no test mention:** `attention_rollout`, `attention_mean`, `apply_source_value_edit`, `forbid_host_exec`, `score_qa`, `procrustes`, `retrieval_scatter`, `bootstrap_cluster`, `assert_disjoint`, `card`, `catalog.load_snapshot`
- **Requirement:** Goal §六 independent oracle; §四 reverse coverage

### F4-13 Traceability ledger still treats `pytest -q` as row-level evidence

- **Severity:** Medium
- **Status:** confirmed defect (verification ledger)
- **Files:** `.planning/PAPER_TRACEABILITY.md` TR-0002+ (`verification_method=python -m pytest -q`, `local_verify_status=passed_local_tests`, text still **`65 passed`**). `06-VERIFICATION.md` L8 still `65 passed`
- **Impact:** Goal §九.1 can be paper-checked as “filled” while no test exists for the row

### F4-14 Fixtures excluded from freeze

- **Severity:** Medium
- **Status:** confirmed defect (freeze protocol)
- **Files:** `tests/fixtures/*.json`; `VERSION.md` scope
- **Impact:** oracle bytes can move without changing a correct aggregate of `.py`+toml

### F4-15 ISSUES `fixed_pending_review` overstates verification closure

- **Severity:** Medium
- **Status:** confirmed defect (process)
- **Independently closed as verification (unit) this freeze:** B-14 production family key + `fit_eligible`; B-24 `5.5`/`5.0`; B-04 equal-count `node_id`; B-22 / C3-M-03 inconsistent denom; C3-M-01 event mean; C3-M-07 empty-list ignores hits; D-08 `leaks_target`; E-17 labels-dir hash; conformal units + `predict_set`; bilinear σ + λ_FN; HumanEval `spy.calls` / `score_submission` / `exec(` reject; extract_answer open-think; iGSM mismatch raise; rename keeps expression; spec/paragraph `needs_truth`; labeled-transfer requires labels; `repairability` formula; default P1 holdout **gate**; `-1` BCE mask; prior B-01/02/03/06–11/13/23.
- **Implementation present, verification not closed:** B-10 answer proof; D-07 `once`; D-10 clone metadata; E-09 failure manifest; `--eval-mode scientific`; resume hash check; last-token prefix invariance.
- **Not closed (wrong or mirror):** A3-20 Week-8 flags (F4-07); B-12 sham densities (F4-11); B-05 `scanned` (mirror); B-17 placeholder (mirror); B-21 reversing map (no test); C3-M-02 leak/magic (F4-02); C3-M-04 CLI scores (F4-03); C3-M-05 nontarget echo; C3-M-06 C4 ledger; BoundaryMLP loss (F4-05); dual-head Y; E-16 leftover (F4-17); CLI science (F4-01).
- **Do not mark closed from this channel** except the unit list above, and only as *verification of those units*, not Goal/requirement Complete.

### F4-16 Real models / official dumps / isolated Linux runner

- **Severity:** —
- **Status:** 外部待验证
- **Note:** tiny random weights, `offline_prefix_ids`, host `subprocess`, and `executor_unavailable` must not be rewritten as server acceptance.

### F4-17 Analyze `--in-dir` file still leaves a half-written report

- **Severity:** High
- **Status:** confirmed defect (implementation; untested)
- **Files/lines:** `cli.py` `cmd_analyze` L582–583 then L639–654; `_upstream` L68–69
- **Trigger:** `--in-dir` pointing at a file
- **Requirement:** author E-16; Goal e2e failure paths
- **Repro:** `NotADirectoryError`; leftover `report.json` **and** `failure.json`/`manifest.json`
- **Author claim E-16:** **not closed**. `_upstream` is first inside `_write_stage`, but analyze writes `report.json` before `_write_stage`

### F4-18 `--eval-mode scientific` has zero tests

- **Severity:** Medium
- **Status:** confirmed defect (verification). Refusals **exist** (prepare fractions; collect offline; calibrate loss; analyze no `--in-dir`)
- **Files/lines:** `cli.py` L181–182, L311–312, L435–436, L530–531
- **Impact:** the only green e2e path is the fixture/offline stub (F4-01)

### F4-19 Non-defect notes

- **Status:** 非缺陷建议
- Hash algorithm in `VERSION.md` reproduces. Keep the script frozen.
- Real improvements vs this channel’s r03 report: B-14 production key, B-24 `5.5`/`5.0`, C3-M-01, C3-M-03, C3-M-07 (stated spec), conformal units/`predict_set`, bilinear σ/λ_FN, HumanEval spy, D-08 True, E-17, extract_answer, iGSM mismatch, IRLS logistic (not leak-proof).
- `STATE.md` “scientific metrics not_evaluated” and “consecutive two-round review not yet passed” are more honest than treating 97 passed as Goal §九.3.
- Last-token hook, `once=True`, clone metadata, `--resume` hash check, E-09 failure counts, and scientific refusals look implemented; absence of tests (or leftover E-16 / dead Week-8 flags / wrong MLP loss) is why they are not closed.

## 10. Goal §九 items 1–7 — verification quality only

This is **not** a Goal-complete declaration. It is whether the **current tests and recorded commands** could support each stop condition.

| Item | Stop condition (abbrev.) | Verification quality |
|---|---|---|
| 1 | Paper/protocol atoms have impl, entry, **verification evidence**; traceability has no unexplained gaps | **Unsupported.** Ledger cites `pytest -q` / `passed_local_tests` / **65 passed** for rows the suite does not test (F4-13). Reverse coverage of production symbols fails (F4-12). |
| 2 | No confirmed unresolved in-scope defects; no unadjudicated correctness doubts | **Unsupported by this channel.** F4-01, F4-02, F4-05, F4-06, F4-07, F4-17 are confirmed leftover defects. ISSUES remain `fixed_pending_review`. |
| 3 | All applicable local checks actually run and pass; meaningful e2e / boundary / failure paths covered; unrun items not disguised as pass | **Partial command, fail substance.** `pytest -q` did run, 97/0, no skip disguise. E2e is exit-code smoke that **asserts** `not_evaluated`. Scientific refusals, resume, E-16, Week-8 flags, P1 leak are untested or unasserted. |
| 4 | GSD phases match reality; software pass ≠ science/server pass | **Docs mixed.** `STATE.md` keeps science pending (good). `06-VERIFICATION.md` and traceability still lead with **65 passed** (bad). |
| 5 | Two consecutive independent full A–F, no new confirmed defects, **same hash** | **Cannot start a pass.** Hash matches (good). `VERSION.md` `consecutive_pass_count: 0`. This channel **files confirmed defects**. |
| 6 | Server-pending items listed with real paths / reasons / future commands | **Not a test-suite question.** Missing code must not hide here: prefix-id collect, placeholder C-layer, host subprocess, and unavailable executor are **code** gaps with names. |
| 7 | Delivery pack: runbook, config, traceability, issue closure, reviews, local record, server entry | **Issue closure is not ready** (F4-15). Local pytest record exists (97/0). |

## 11. Channel verdict

| Judgment | Content |
|---|---|
| pytest | **97 passed, exit 0, 10.93s, 97 collected.** No skip/xfail. **Not** QA-01 / Goal §九.3 evidence. |
| Freeze | **HASH_MATCH.** Declared and recomputed `fb1e3dfad996c9221e508c9ec153b146e76946b81dc6f3d61b28425090c66d17` (56 files). Per-file SHA-256 in §2. |
| Independence | New real oracles: B-14 key, B-24 decimals, C3-M-01/03/07, conformal units, bilinear σ/λ_FN, spy.calls, D-08, E-17. **Not** independent: CLI science, P1 leak, Week-8 flags, BoundaryMLP loss, C4 ledger, transfer numbers, sham noise, last-token/once. |
| Mocks/stubs | Offline prefix-id `H` + calibrate `scores=None` + analyze-ignores-labels + repair ledger + identity cache + hardcoded C-layer scores + `not_evaluated` encoded as success. Worse than unittest.mock. |
| Paper behavior still unproven | Leak-proof logistic P1, P2 from labels, C-layer **dev** selection, BoundaryMLP BCE, C4 recompute, isolated exec, T2 reversing map, R^surf beyond fixture lines |
| Delivery vs tests | “97 passed / r03 defects closed / pipeline consumes upstream” **exceeds** test force |
| Confirmed problems? | **Yes.** Critical: F4-01. High: F4-02, F4-05, F4-06, F4-07, F4-17. |
| Goal complete? | **No.** |
| Channel pass? | **Fail.** Empty “looks fine” is inapplicable. Green pytest is not acceptance. |

Until CE-class tests exist for the High/Critical items — and A3-20 / E-16 / BoundaryMLP loss are actually fixed — any closing sentence of the form “code acceptance passed; independent review found no confirmed leftover defects” contradicts this channel’s evidence.
