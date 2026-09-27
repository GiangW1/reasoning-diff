# F: verification quality and adversarial doubt (round-02)

Independent review channel F. Production tree was not modified. Pytest green is not treated as paper-correctness. Other round-02 channel reports were not read. `ISSUES.md` was read only as author claims; every claimed closure was re-checked from tests vs production.

**Lead conclusion:** `python -m pytest -q` is **65 passed / exit 0**. That is not Goal acceptance and is not independent proof of paper behavior. Round-01 added a useful regression file with some real oracles (B-01/02/08/09, C-02, C-04, D-01). The CLI science path, P1 estimator, conformal units, HumanEval isolation, repair execution, bilinear/BCE math, BoundaryMLP, and most appendix symbols are still either untested or tested by mirrors/stubs. Declared freeze hash **does not recompute**. This channel **does not pass**.

## 1. Metadata

| Field | Value |
|---|---|
| agent / task | Independent Reviewer F / verification quality and adversarial doubt |
| review time | 2026-09-21 (Asia/Shanghai) |
| declared freeze | `2676a0983f6b42148202eedfbfaea44ce207d1fd386b8d47cbc909e983c5cc38` |
| recomputed aggregate | `7b6680d6d937097fd02841d5950df1a7b3498ebcd1965381220b5e429ec5c617` |
| hash verdict | **HASH_MISMATCH** |
| hash method used | 55 files: `src/reasoning_diff/**/*.py` + `tests/**/*.py` + `pyproject.toml` (no `__pycache__`). Sort by POSIX `relpath`. Update SHA-256 with `relpath.encode() + b"\0" + file_bytes`. No CRLF in any scoped file. |
| variants also tried | path+bytes without NUL; path+NL+bytes; bytes-only; sha256sum listing; merkle of file digests; `io.digest` of path→hex; LF-normalize (no-op); exclude `__init__.py`; include fixture JSON (65 files). **None** equal `2676a098…`. |
| file-count match | 55 files, matches `round-02/VERSION.md` |
| git_head | `46a6e26da8637fe29d9f8f0667cb4e513538a59d` (2026-09-20 23:54:47 +0800; working tree dirty; do not trust HEAD as the freeze) |
| scope | all `tests/**` (13 `.py` + 10 fixture JSON) and every production function those tests import or CLI-smoke; remaining production modules scanned for untested entry points |
| explicitly unread | `.planning/audits/round-02/{A,B,C,D,E}-*.md` |

Review object is the **current working-tree bytes** below (per-file SHA-256). The declared aggregate cannot be used as an independent identity of this tree.

## 2. Per-file coverage

### 2.1 Tests (all read)

| File | Lines | What it actually binds |
|---:|---:|---|
| `tests/conftest.py` | 11 | `t1_tiny_path` only |
| `tests/test_artifacts.py` | 73 | JSONL/NPZ/run_spec/manifest/NaN; digest self-check |
| `tests/test_cli_pipeline.py` | 29 | eight-stage exit 0 + `report.status==not_evaluated` |
| `tests/test_generate_loop.py` | 17 | Generator replay + greedy argmax |
| `tests/test_measure.py` | 40 | set densities, joint `f=xy`, cone source strings |
| `tests/test_review_regressions.py` | 315 | round-01 defect oracles; mixed independence (see §6) |
| `tests/test_science.py` | 97 | conformal happy path, transfer shape, one position, streams, Week8 unregistered, P1 single-class, verbalizer, repair flags, swap, noop metadata |
| `tests/test_t1_official.py` | 31 | official shape/mod23/answer 12; config happy path; no `tools` import |
| `tests/test_t2_gsm.py` | 33 | sidecar 5+3=8; unknown without sidecar; GSM-Plus test-only |
| `tests/test_t3_t4.py` | 40 | Hotpot flags, MuSiQue pair, HumanEval status string, T4 set equality |
| `tests/test_tiny_cache.py` | 25 | cache mutation as **expected**; collect/intervene flags |
| `tests/test_tiny_hooks.py` | 27 | hook effect + cleanup; L17 tautology |
| `tests/test_tracer_t1_prepare.py` | 100 | fixture prepare, identity, densities, TO, prepare CLI |
| `tests/fixtures/*.json` | 10 files | hand oracles; **outside freeze hash** |

Collect-only: **65 nodes**. No `skip` / `xfail` / `skipif` / `unittest.mock`. One `@pytest.mark.integration` (tiny hooks) still **ran**. Zero `assert True`. One equivalent tautology: `assert layer.__class__.forward` (`tests/test_tiny_hooks.py` L17).

### 2.2 Production vs tests

| File | Lines | File SHA-256 | Test reach | Untested or only stub-touched |
|---|---:|---|---|---|
| `src/reasoning_diff/__init__.py` | 5 | `26d1e3039417f58d…` | import | — |
| `__main__.py` | 4 | `307299fda7b77d22…` | `hasattr(main)` only | argv/`SystemExit` |
| `analysis.py` | 131 | `146ca012939ed23c…` | P1 single-class + rank-AUC on **linear** scores; Week8 unregistered; P3 flag | logistic P1; `p2_paired`; Week8 vs measurements; `cone_fit` (`r2` always None); `procrustes`; `retrieval_scatter`; `bootstrap_cluster` |
| `artifacts.py` | 83 | `61dc639ead0eff1f…` | run_spec/manifest | `completed_shard_ok` only inside CLI `assert`; resume semantics |
| `baselines.py` | 44 | `2d28ef1cdff3bd57…` | verbalizer two visibilities | `text_predictor`; `attention_mean`; `attention_rollout`; fiveshot fairness |
| `cli.py` | 419 | `9ae87fe24abfeb63…` | exit codes; label/fit file keys | analyze ignores `labels.jsonl`; collect writes `np.eye(4)`; calibrate 4 synthetic scores; intervene `geometry_only` null accuracies; repair `generated_tokens=0` |
| `edits.py` | 141 | `6226f3adc81dda92…` | 7→0; isolated numeral; official 4*3%23=12 | non-arithmetic expr; multi-premise span shift beyond B-09 |
| `events.py` | 125 | `1d1d3413601c4834…` | identity align; surface≠parents; deletion counts | `merged`/`strategy_changed` always `[]`; `extract_answer` |
| `executor.py` | 59 | `d1760266a9a7606b…` | Spy constructed | **`spy.calls` never asserted**; `forbid_host_exec`; `exec(` reject |
| `graphs.py` | 44 | `1e287cebf844cec0…` | ancestors via fixture | `graph_status` empty-complete reject |
| `interventions.py` | 91 | `b971c432d1e2b2fd…` | swap [1,1]; C-rand/C-layer **norm**; INLP dim-0 | rescue; `intervention_report`; C-layer **dev-split layer pick**; same-cohort identity |
| `io.py` | 127 | `c5c77a27d196e97d…` | encode/jsonl/npz | `runtime_info`; corrupt JSONL line |
| `measure.py` | 242 | `2d9272406879cbf9…` | set ρ; matrix missing-noise; build_labels B-02/03; CSP empty parents | set-path `noise_set` ≠ sham observations; `compare_pair` structural |
| `models/__init__.py` | 1 | `0b7dd6c4dd852065…` | — | — |
| `models/adapters.py` | 29 | `a8680ef98b8075ce…` | **zero tests** | `card`; `latest` dead branch |
| `models/collect.py` | 47 | `051e1b3005631c48…` | flags | `cache_isolated` is `is not`; CLI collect does **not** call this |
| `models/features.py` | 43 | `ff5c6a79b9ecf082…` | D-01 indices 1/2/3 | leak=True when a selected token still straddles (D-01 leak case is idx=None) |
| `models/generate.py` | 56 | `4fd7091842236d7a…` | replay/greedy | `apply_model_template`; top-p/k; thinking |
| `models/tiny.py` | 92 | `3bf2200b9b71d191…` | hook cleanup | last-token-only not asserted; tuple vs tensor L17 fake |
| `probes/__init__.py` | 3 | `3065196db28e929c…` | — | — |
| `probes/bilinear.py` | 74 | `81451eb4c0d6945e…` | CLI writes `loss` | no σ(h^T U V^T e + b) oracle; no `weighted_bce`; unknown mask; λ_FN=10; two heads share Y |
| `probes/boundary.py` | 23 | `a45ec29f20fc3b3c…` | **zero tests** | Hidden=256 ReLU |
| `probes/calibrate.py` | 35 | `d753c94bc0467dd7…` | α=0.4/0.1; α≥1 invalid | **`predict_set` unused**; sequence vs 1−p not composed; palindrome [0.1,0.9] |
| `repair.py` | 57 | `54559ea4f50eda9a…` | mask + refilled | `generated_tokens` locked 0; `repairability`/`recompute_ratio` **zero tests** |
| `rng.py` | 53 | `2098c2c72a852eaa…` | two scalars unequal | snapshot/restore; torch.Generator isolation |
| `schema.py` | 371 | `c07301be5fabd647…` | enums, identity | `canonical_value` aliases; most negative paths |
| `scoring.py` | 30 | `d05822c4fb784fe4…` | code status string | `score_qa`; isolated true exec |
| `splits.py` | 75 | `a62d819bf99ceb13…` | gsm_plus→test; family weak | `assert_disjoint`; illegal fractions |
| `tasks/catalog.py` | 39 | `5d3918394b1603bb…` | **zero tests** | `iter_snapshot_files` / `load_snapshot` |
| `tasks/t1_config.py` | 21 | `e1e7f8232dfa603d…` | legal config only | reject ops/mod/n≠500 |
| `tasks/t1_fixture.py` | 20 | `01b6748804316fb3…` | load | — |
| `tasks/t1_official.py` | 83 | `2e83cc052a518d43…` | ancestors/mod/12 | `shared_rng_excluded` hardcoded True (L72) |
| `tasks/t2_gsm_plus.py` | 51 | `0da626321ee5d786…` | test-only | `query_reversed` **∉** `T4_STATUSES` (L18–21) |
| `tasks/t2_gsm_symbolic.py` | 70 | `e8fc9d046ba13006…` | sidecar edit | no-sidecar placeholder premises |
| `tasks/t2_noop.py` | 80 | `26cf5c21b5838a6b…` | front span + metadata | mid/back |
| `tasks/t3_hotpot.py` | 59 | `a79ab16c0ebdae7f…` | support≠DAG | `document_edit` does **not** return a new Task/answer |
| `tasks/t3_humaneval.py` | 35 | `c77e136ceb6e6f71…` | family id; status | `score_submission` never takes executor |
| `tasks/t3_musique.py` | 69 | `095f10acc7c4600f…` | pair ids | composition_reference recompute |
| `tasks/t4_boundary.py` | 33 | `a2ca9188353b213d…` | set equality | illegal status; family grouping |
| `transfer.py` | 40 | `0020150ebf53663b…` | 4096/3584 N/A; ones→shape | numerical map (ones still `allclose`); `apply_bilinear_inputs` |

Fixture JSON is **not** in the freeze. Changing official answers / sidecar / T4 statuses does not change any published aggregate, but changes “ground truth.”

## 3. Checks run and results

| Check | Command / method | Result |
|---|---|---|
| Freeze hash | algorithm in §1 | **HASH_MISMATCH** vs `2676a098…`. Local aggregate `7b6680d6…`. |
| Full pytest | `python -m pytest -q` at repo root (`pythonpath=src`) | **65 passed in 11.13s, exit code 0**. No skip/xfail/deselected. |
| Collect | `python -m pytest tests --collect-only -q` | 65 nodes, collect exit 0 |
| skip/xfail/`assert True` | ripgrep on `tests/**` | no skip/xfail/mock; tautology at `test_tiny_hooks.py` L17 |
| Hand oracles | iGSM `4*3 % 23 = 12`; fixture `7*0=0`; sidecar `5+3=8`; TO `2·LCS([1,2],[1,3])/4=0.5`; D-01 indices 1/2/3; C-02 α=1 invalid | those **unit** assertions match independent arithmetic |
| Adversarial: analyze vs labels | `prepare` then `analyze --in-dir <prep>` | `report.status==not_evaluated`, `p1 is None`; **no** `p1_table.jsonl`; labels exist and are ignored (`cli.py` L351–368) |
| Adversarial: collect/fit/cal | real CLI | `features.npz` keys `dummy,H,E` all `eye(4)`; both probe heads same `loss=0.1417…`; calibrate scores `[loss, loss+0.1, 0.3, 0.4]` not trace nonconformity |
| Adversarial: intervene/repair | real CLI | intervene `geometry_only`, all accuracies `None`, norms matched; repair `generated_tokens=0` |
| Adversarial: sequence vs `predict_set` | `[0.9,0.1]` and `[0.1,0.9]` | `sequence_score` both `0.9` (palindrome); `predict_set([0.9,0.1], 0.2)=[True, False]` uses `1-p`. **No test composes them.** |
| Adversarial: P1 no holdout | `rho=length` | `delta_auc=0` via `length+0.01*op+rho` (**not logistic**) |
| Adversarial: Week8 thresholds | `{gate0/1/2:0.9}` | all `evaluated`, **no measurement comparison** |
| Adversarial: joint `f≡0` | `joint_edit_counterexample` | `joint_changed=False` but `soundness_claim_allowed=False` still (constant) |
| Adversarial: transfer ones | `ones(5,4)` / `ones(5,6)` | `allclose(ones)` True — shape test is vacuous |
| Adversarial: known affine | `tgt=[[2,0,0],[0,3,0]]→src=I` | lstsq recovers; **no test uses this** |
| Adversarial: Spy | `score_code(..., executor=spy)` | `spy.calls` length 1 in production; **test does not assert it** |
| Adversarial: `query_reversed` | `T4_STATUSES` | not a member; GSM-Plus sets it anyway |

## 4. Checks not run, and why

| Not run | Reason |
|---|---|
| Real HF weights, official full dumps, GPU/CUDA KV | out of scope / `pending_server` |
| Linux isolated executor actually running HumanEval | only `UnavailableExecutor` / `SpyExecutor` |
| Other channel reports | forbidden |
| Editing production or adding regressions | forbidden; counterexamples are protocol-only in §8 |
| Line-by-line audit of `transformers`/`torch` | project usage only |

## 5. Delivery claims vs what tests prove

| Claim | Location | Do tests support it? |
|---|---|---|
| `python -m pytest -q` → 65 passed | `06-VERIFICATION.md` L8; `STATE.md` L15; `VERSION.md` L9 | **Command yes.** Using it as phase/Goal evidence: **no.** |
| “round-01 defects closed in code” | `06-VERIFICATION.md` L9; `ISSUES.md` `fixed_pending_review` | **Partial.** Several closures have independent unit tests. Several do not (C-01 leak, B-13, D-02 last-token, E-01/E-03, D-03 encoded stub). |
| CLI pipeline / stages consume upstream | `docs/SERVER_RUNBOOK.md` L22–31; `test_pipeline_consumes_upstream` | Files are read. Science is **not**: collect is I₄; analyze ignores labels; calibrate is four numbers; intervene invents no accuracy (good) and also computes no paper effect. |
| Traceability `verification_method=python -m pytest -q` on hundreds of rows | `.planning/PAPER_TRACEABILITY.md` TR-0002+ | **Cannot.** Suite does not contain oracles for those rows. This is a verification-ledger defect, not a green-bar success. |
| Goal §九 items 1–7 | `docs/CURSOR_GOAL_PROMPT.md` L146–157 | **Not evidenced by this suite.** See §10. This channel does **not** declare Goal complete. |
| Author pytest claim 65 | `VERSION.md` | Independently confirmed: 65 / exit 0. |

## 6. Are tests independently valid?

### 6.1 Independent oracles (would fail a wrong impl)

- `test_value_edit_recomputes_expression`: `p1=7,p2=0 → q=0`.
- `test_symbolic_sidecar_edit` / `test_b08_*`: `a:4→5`, `a+b=8`, question/nodes updated.
- `test_template_not_g_and_mod23` **answer** `"12"` (`4*3 % 23`).
- `test_to_empty_is_null`: `[]` null; `[1,2]` vs `[1,3]` → 0.5.
- `test_signed_excess_not_clipped` / pitfalls: signed −0.5 under **this** set formula (locks the formula; see F2-11).
- `test_zero_denominator_null`; `test_b01_*` missing noise is None not 0.
- `test_b02_*` finite-scan `no_change` → unknown.
- `test_b03_*` sham `changed` does not set `behavior_label=1`.
- `test_b04_*` unequal occurrence counts → no rematch.
- `test_b06_*` `surface_mentions==[]` while parents `{p1,p2}`.
- `test_b07_*` `HumanEval/0` not truncated.
- `test_b09_*` `14` with value `"4"` must raise.
- `test_b10_*` front no-op does not steal `p1` span.
- `test_b11_*` empty parents + graph unknown → CSP null.
- `test_b14_*` `source="gsm_plus"` → `test`.
- `test_c02_*` α≥1 → `invalid` (this channel: `conformal_threshold(...,1.0)["status"]=="invalid"`).
- `test_c04_*` C-rand without `target_norm` raises; norms match provided main.
- `test_d01_*` token indices **1, 2, 3** on a constructed offset list — real POS-01 unit oracle.
- `test_swap_formula`: `[1,0]+Π([0,1]-[1,0])=[1,1]`.
- `test_encode_rejects_nan`; `test_npz_no_pickle`; fixture≠official; no `import tools`.
- `test_direct_transfer_rejects_4096_3584` **status string** (shape half is weak).
- Tiny hook: logits change under hook and restore after remove (L22–26). L17 excluded.
- `test_explicit_generator_replay`.

### 6.2 Invalid, self-referential, or too weak

| Test | Why it does not prove paper behavior |
|---|---|
| `test_full_cli_smoke` L24–29 | Exit 0 + `not_evaluated` + files exist. A CLI that writes constants still passes. This channel’s analyze-after-prepare run is exactly that. |
| `test_pipeline_consumes_upstream` L302–315 | Stops at fit. Asserts `"task_label" in row` and `"loss" in probes[0]`. Any finite loss on I₄ features passes. Does not check label values equal prepare, or that H/E are hidden states. |
| `test_e04_analyze_manifest_includes_report` L278–285 | **Encodes the stub as the expected outcome** (`status==not_evaluated`, `scientific_conclusion is None`). Does not prove analyze refused to invent P1 from labels. |
| `test_e02_*` | Only `edited answer != base answer`. Any non-identity edit passes. |
| `test_e08_*` | `hasattr(entry, "main")`. |
| `test_e06_*` | No leftover tmp after **success**. Crash-mid-write atomicity untested. |
| `test_c01_auc_is_rank_and_permutation_invariant` | Uses **no-holdout** path: `length+0.01*op+rho` (`analysis.py` L42–44). Tests rank-AUC of the **linear substitute**, not paper logistic P1. |
| `test_c01_held_out_fit_does_not_use_eval_rows` | Asserts `held_out is True` and `auc_base is not None`. A leaky fit-on-all-rows implementation still returns those. **Does not compare to an oracle that excludes eval rows.** |
| `test_p1_null_on_single_class` | Any `if unique(y)<2: return None` stub passes. |
| `test_conformal_examples` L25 | `sequence_score([0.1,0.9])==0.9` is true for both `max(p)` and `max(1-p)`. `predict_set` never called. |
| `test_joint_edit_blocks_soundness` | Now uses `f=x*y` (better than round-01). `soundness_claim_allowed` is **hardcoded False** (`measure.py` L232). `f≡0` still yields False. Flag is not derived from the fixture. |
| `test_week8_never_passes_unregistered` | Only `not_evaluated`. Threshold path untested; REST string `"already decided"` is implemented (`analysis.py` L91–97) but **not fed**. |
| `test_direct_transfer` map | `np.ones` → shape (5,4). `return np.ones((5,4))` passes. This channel: `allclose(ones)` is True. |
| `test_cone_fields_separated` | Source strings only. Empty `predicted` still labeled `behavior_head`. |
| `test_template_not_g_and_mod23` flags | `shared_rng_excluded` is written `True` (`t1_official.py` L72), not computed from dropped nodes. |
| `test_config_ops` | Legal `{5,10,15,21},500,23` only. |
| `test_collect_and_intervene_tiny` | `cache_isolated` is object identity (`collect.py` L44). `leaks_target is False` on that prompt. |
| `test_tiny_hooks` L17 | `assert layer.__class__.forward` is true for any class with a `forward`. |
| `test_humaneval_never_host_exec` | Does not read `spy.calls`. `score_submission` has no executor arg. Hardcoded `executor_unavailable` passes. |
| `test_repair_reprefills_and_refuses_gate` | Accepts `generated_tokens=0` (`repair.py` L41). |
| `test_streams_are_independent` | Two floats unequal. No replay/snapshot. |
| `test_verbalizer_supervision_contract` | No fiveshot, no shared split with probe. |
| `test_t4_statuses_distinct` | Set equality with `T4_STATUSES`. |
| `test_hotpot_support_is_not_full_dag` | Edit does not update `answer_spec` (`t3_hotpot.py` L51–59). |
| `test_b13_assign_family_*` | Different member lists. Ignoring `family_id` and hashing the whole set still passes. Collision check is `len>=2` after a third family — not a forced use of `family_id`. |
| `test_use_cache_false_*` | Documents transformers pollution as **desired**. No failing test that a second condition must not consume the dirty cache. |

## 7. Mocks / stubs that hide unconnected paths

Almost no `unittest.mock`. Internal stubs do the same job.

1. **CLI science path still disconnected (F2-01).** `--in-dir` is parsed. `label` requires observations (good). Then:
   - `cmd_collect` L220–221 writes `dummy/H/E = np.eye(4)`, not `collect_tiny` / residual hooks.
   - `cmd_fit` trains `BilinearProbe` on that I₄ and a Y built by walking the first `h.shape[0]` label rows (L263–269). Task and behavior heads get the **same Y**.
   - `cmd_calibrate` L287–292 uses four hand scores, optionally shifted by **training loss**, not held-out nonconformity on calibration traces.
   - `cmd_intervene` L328–331 writes `target/nontarget/task_correct/invalid = None`, `status=geometry_only`.
   - `cmd_analyze` L351–368 looks only for `p1_table.jsonl`. Prepare/label never write that file. P1–P3 stay `None`. `test_full_cli_smoke` **expects** `not_evaluated`.
2. **Repair is a ledger (F2-10).** `run_repair` always `generated_tokens=0`. CLI repair ignores `--in-dir` tasks.
3. **HumanEval isolation is a status string (F2-08).** Spy can record; tests do not look. `score_submission` → default `UnavailableExecutor`.
4. **Tiny intervene isolation is `is not` (F2-13).** `past_key_values=None` guarantees a new object.
5. **BoundaryMLP, attention/rollout, model cards, `apply_model_template`, INLP four-outcome semantics, rescue, P2, cone_fit, Procrustes, retrieval, `weighted_bce`, `predict_set`, `repairability`, `catalog.load_snapshot`, `assert_disjoint`** have **zero test references** (ripgrep on `tests/`).

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
(auc_base is not None).
Also: no-holdout path must not be length+0.01*op.
Swap: rho perfect, length noise → ΔAUC>0 under logistic; current linear add may tautologize.
```

### CE-3 Conformal units

```text
p_hat = [0.9, 0.1]
s = 1-p = [0.1, 0.9]
sequence unit = max(s) = 0.9   # same as max(p) on this pair — use [0.8, 0.2]
max(p)=0.8, max(1-p)=0.8 still palindromic; use [0.7, 0.4]:
max(p)=0.7, max(1-p)=0.6  → distinguishes
predict_set must use the same s.
α=1 already invalid (C-02 good). Keep it.
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
src=[[1,0],[0,1]], tgt=[[2,0,0],[0,3,0]]
apply_map(tgt,W) ≈ src  (this channel: lstsq already does; test does not check)
apply_bilinear_inputs must map H and E
silent pad/[:d] after a successful fit must fail
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
Hand h,e,U,V,b → σ(sum((hU)*(eV))+b)
Y with nan / mask=0: weighted_bce equals known-only terms, λ_FN=10 on positives
Treating unknown as 0 must fail
Task head and behavior head must not share Y unless protocol says so
BoundaryMLP: hidden==256, ReLU, and a numeric logit oracle
```

### CE-8 Repair budget

```text
repairability(4,10)=0.6; full=0 → None
After run_repair, generated_tokens is not identically 0 unless the stage is declared non-executing and removed from “C4 implemented”
```

### CE-9 Week8 / REST

```text
gate_thresholds={"gate0":0.9} + measurements below / unregistered method
  → not decision="evaluated" without a comparison
measurements text "already decided" → forbidden_claims_blocked (implemented, untested)
```

### CE-10 Family id / official metadata / GSM-Plus status

```text
assign_family(same members, family_id A vs B) must differ (or document hash(family_id))
Loader: SHARED_RNG node present in JSON but excluded from premises — assert premises, not metadata True
GSM-Plus perturbation "reversing operation": status must be a declared enum or explicit non-T4 field; query_reversed ∉ T4_STATUSES
```

### CE-11 Sham-only and set-vs-observation noise

```text
Only sham:changed, no real obs → behavior must not become 1
dependency_densities(noise_set=...) must not be the only noise test; build_labels sham path already partially covered
```

### CE-12 Hook last-token and cache content

```text
resid_post_hook: prefix tokens unchanged, last position transformed
cache_isolated: compare cloned tensor contents, not `is not`
second condition must not see first-condition KV
```

## 9. Findings

### F2-00 Declared freeze hash does not recompute

- **Severity:** High (process / identity of the review object)
- **Status:** confirmed defect
- **Files:** `.planning/audits/round-02/VERSION.md` L5–6; working tree 55 files
- **Trigger:** recompute POSIX relpath + bytes
- **Requirement:** Goal §七 “same frozen code version”; §九.5 same hash
- **Repro:** §1. Local `7b6680d6…` ≠ `2676a098…`
- **Impact:** Round-02 reviewers cannot prove they audited the author’s freeze. Consecutive-pass counting on this hash is undefined.
- **Fix:** Publish the exact bytes script; re-freeze from the script; include fixtures or a second digest.

### F2-01 CLI / Goal e2e tests accept an unconnected science path

- **Severity:** Critical
- **Status:** confirmed defect (verification; implementation still stubbed after fit)
- **Files/lines:** `tests/test_cli_pipeline.py` L4–29; `tests/test_review_regressions.py` `test_pipeline_consumes_upstream` L302–315, `test_e04_*` L278–285; `cli.py` `cmd_collect` L220–221, `cmd_calibrate` L287–292, `cmd_analyze` L351–368
- **Trigger:** documented eight-command chain
- **Requirement:** Goal §六 “从生产入口验证跨模块数据流”; OPS-01 / QA-01
- **Repro:** §3 analyze-after-prepare; collect I₄; calibrate `[loss, loss+0.1, 0.3, 0.4]`
- **Impact:** 65 passed + runbook commands can be cited as “pipeline works” while P1–P3 never see labels
- **Fix:** CE-1; one run dir; analyze must hash-check upstream labels or refuse; stop asserting `not_evaluated` as the only success

### F2-02 P1 tests lock a linear substitute and do not prove holdout

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `analysis.py` `p1_incremental` L42–55; `tests/test_review_regressions.py` L198–222; `tests/test_science.py` L64–66
- **Trigger:** two-class data; optional `held_out`
- **Requirement:** Goal §五.12 / C3-01 logistic length+op, incremental AUC
- **Repro:** no-holdout `delta_auc=0` with `rho=length`; holdout test stays green if all rows are used in lstsq
- **Impact:** Main-text P1 numbers can come from the wrong estimator with a green suite
- **Fix:** CE-2

### F2-03 Conformal `predict_set` and sequence units are not synthesized

- **Severity:** High
- **Status:** confirmed defect (coverage); α≥1 wrap is **closed** by C-02
- **Files/lines:** `probes/calibrate.py` L9–16, L32–35; `tests/test_science.py` L20–27
- **Trigger:** non-palindromic `p_hat`; call `predict_set`
- **Requirement:** Goal §五.8 / PROP2-01
- **Repro:** `[0.1,0.9]` cannot distinguish `max(p)` vs `max(1-p)`; `predict_set` unused in tests
- **Fix:** CE-3

### F2-04 HumanEval tests still do not observe the executor

- **Severity:** High
- **Status:** confirmed defect (verification)
- **Files/lines:** `tests/test_t3_t4.py` L29–35; `executor.py` L42–46; `t3_humaneval.py` L34–35
- **Trigger:** `score_code(..., executor=spy)` without `spy.calls`; `score_submission` default backend
- **Requirement:** Goal §五.15 / EXEC-01
- **Repro:** hardcoded `executor_unavailable` passes; `exec(` reject untested
- **Fix:** CE-6

### F2-05 Probe/Boundary/BCE math has no independent oracle

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `probes/bilinear.py` `fit`/`score`/`weighted_bce` L21–74; `probes/boundary.py` entire file; CLI `cmd_fit` L270–276
- **Trigger:** `reasoning-diff fit`; any I₄ + loss
- **Requirement:** Goal §五.7 / PROBE-01 / BOUND-01
- **Repro:** ripgrep: zero `weighted_bce` / `BoundaryMLP` / bilinear score oracles in tests; both heads share Y
- **Fix:** CE-7

### F2-06 Repair/C4 tests accept a zero-generation ledger

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `repair.py` L34–45; `tests/test_science.py` L76–80; `cli.py` `cmd_repair` L338–343
- **Trigger:** any legal mask
- **Requirement:** Goal §五.13 / REPAIR-01
- **Repro:** CLI repair `generated_tokens==0`; `repairability` untested (this channel: `repairability(4,10)==0.6`)
- **Fix:** CE-8 or formally drop C4 from “implemented”

### F2-07 Week8 + REST: thresholds imply `evaluated`; ban-string untested

- **Severity:** High
- **Status:** confirmed defect
- **Files/lines:** `analysis.py` `week8_decision` L83–99; `tests/test_science.py` L56–61
- **Trigger:** nonempty `gate_thresholds`
- **Requirement:** Goal §五.14 / DECIDE-01 / REST-01..03
- **Repro:** §3; `"already decided"` is blocked in code and not in tests
- **Fix:** CE-9

### F2-08 Joint soundness flag is a constant; test cannot see `f≡0`

- **Severity:** Medium
- **Status:** confirmed defect (verification). Constant False is REST-03-conservative, not a fixture proof.
- **Files/lines:** `measure.py` L225–234; `tests/test_measure.py` L25–32
- **Repro:** `f≡0` → `soundness_claim_allowed is False` anyway
- **Fix:** CE-4

### F2-09 Transfer / verbalizer / Hotpot / T4 / official flags remain surface contracts

- **Severity:** Medium
- **Status:** confirmed defect (verification gap)
- **Files/lines:** `tests/test_science.py` L30–37, L69–73; `tests/test_t3_t4.py` L12–18, L38–40; `t1_official.py` L71–73; `t3_hotpot.py` L51–59; `t2_gsm_plus.py` L18–21
- **Repro:** ones map; Hotpot edit has no new truth; `query_reversed ∉ T4_STATUSES`; metadata hardcoded
- **Fix:** CE-5, CE-10

### F2-10 Family-id test does not force `family_id`

- **Severity:** Medium
- **Status:** confirmed defect (verification)
- **Files/lines:** `tests/test_review_regressions.py` L183–190; `splits.py` `assign_family` L32–44
- **Repro:** different member sets; this channel `a["a-member"] != b["a-member"]` without proving the key is `family_id`
- **Fix:** CE-10 same-members different ids

### F2-11 Tiny tautology, identity cache, last-token untested

- **Severity:** Medium
- **Status:** confirmed defect (verification)
- **Files/lines:** `tests/test_tiny_hooks.py` L17; `models/collect.py` L44; `models/tiny.py` L59–69
- **Requirement:** Goal §五.10–11
- **Fix:** CE-12

### F2-12 Large symbol set still has zero tests

- **Severity:** Medium (set). Several items already raised in F2-05/06.
- **Status:** confirmed defect (coverage)
- **Symbols with no test mention:** `BoundaryMLP`, `predict_set`, `weighted_bce`, `p2_paired`, `apply_bilinear_inputs`, `apply_model_template`, `attention_rollout`, `text_predictor`, `forbid_host_exec`, `extract_answer`, `score_qa`, `rescue`, `intervention_report`, `cone_fit`, `procrustes`, `retrieval_scatter`, `bootstrap_cluster`, `assert_disjoint`, `card`, `catalog.load_snapshot`, `repairability`, `recompute_ratio`
- **Requirement:** Goal §六 “独立 oracle…不能让期望值调用同一待测函数”; §四 reverse coverage
- **Fix:** property/counterexample tests, not more status-string mirrors

### F2-13 Traceability ledger treats `pytest -q` as row-level evidence

- **Severity:** Medium
- **Status:** confirmed defect (verification ledger)
- **Files:** `.planning/PAPER_TRACEABILITY.md` TR-0002 and following (`verification_method=python -m pytest -q`, `local_verify_status=passed_local_tests`)
- **Impact:** Goal §九.1 can be paper-checked as “filled” while no test exists for the row
- **Fix:** per-row command/oracle or `untested`

### F2-14 Fixtures excluded from freeze

- **Severity:** Medium
- **Status:** confirmed defect (freeze protocol)
- **Files:** `tests/fixtures/*.json`; `VERSION.md` scope
- **Impact:** oracle bytes can move without changing even a *correct* aggregate of `.py`+toml

### F2-15 ISSUES `fixed_pending_review` overstates verification closure

- **Severity:** Medium
- **Status:** confirmed defect (process). Independent unit closures: B-01, B-02, B-04 (unequal counts), B-06–B-11, B-14, C-02, C-04 (norm), D-01 (unit). **Not closed as verification:** C-01 (leak/logistic), B-13, D-02 (last-token), D-03 (stub encoded), E-01 (science path), E-03 (no resume test), E-08 (hasattr).
- **Do not mark closed from this channel.**

### F2-16 Real models / official dumps / isolated Linux runner

- **Severity:** —
- **Status:** 外部待验证
- **Note:** tiny random weights and `executor_unavailable` must not be rewritten as server acceptance.

### F2-17 Non-defect notes

- **Status:** 非缺陷建议
- `test_use_cache_false_*` is a useful transformers 5.5.3 regression if renamed to “known pollution,” with a separate fail-if-reused-cache test.
- Constant-False soundness flag matches REST-03 spirit; still needs CE-4.
- C-02 α≥1 and D-01 unit indices are real improvements over round-01 F.
- `STATE.md` “scientific metrics not_evaluated” is more honest than treating 65 passed as Goal §九.3.

## 10. Goal §九 items 1–7 — verification quality only

This is **not** a Goal-complete declaration. It is whether the **current tests and recorded commands** could support each stop condition.

| Item | Stop condition (abbrev.) | Verification quality |
|---|---|---|
| 1 | Paper/protocol atoms have impl, entry, **verification evidence**; traceability has no unexplained gaps | **Unsupported.** Ledger cites `pytest -q` / `passed_local_tests` for rows the suite does not test (F2-13). Reverse coverage of production symbols fails (F2-12). |
| 2 | No confirmed unresolved in-scope defects; no unadjudicated correctness doubts | **Unsupported by this channel.** F2-01..F2-12 are confirmed verification/implementation defects. ISSUES remain `fixed_pending_review`. |
| 3 | All applicable local checks actually run and pass; meaningful e2e / boundary / failure paths covered; unrun items not disguised as pass | **Partial command, fail substance.** `pytest -q` did run, 65/0, no skip disguise. E2e is exit-code smoke. Failure paths (α=1 aside) mostly untested. Analyze `not_evaluated` is asserted as success. |
| 4 | GSD phases match reality; software pass ≠ science/server pass | **Docs mixed.** `STATE.md` / runbook keep science pending (good). `06-VERIFICATION.md` leads with 65 passed; traceability marks `passed_local_tests` on science-adjacent rows (bad). |
| 5 | Two consecutive independent full A–F, no new confirmed defects, **same hash** | **Cannot start.** HASH_MISMATCH (F2-00). `VERSION.md` `consecutive_pass_count: 0`. This channel **files new confirmed defects**. |
| 6 | Server-pending items listed with real paths / reasons / future commands | **Not a test-suite question.** Runbook lists commands. Missing code must not hide here: collect I₄ and unavailable executor are code gaps with names, not only server waits. |
| 7 | Delivery pack: runbook, config, traceability, issue closure, reviews, local record, server entry | **Issue closure and review identity are not ready** (F2-00, F2-15). Local pytest record exists. |

## 11. Channel verdict

| Judgment | Content |
|---|---|
| pytest | **65 passed, exit 0, 11.13s.** No skip/xfail. **Not** QA-01 / Goal §九.3 evidence. |
| Freeze | **HASH_MISMATCH.** Declared `2676a098…`. Recomputed `7b6680d6…` (55 files, POSIX relpath + NUL + bytes). Per-file SHA-256 in §2.2. |
| Independence | Real oracles exist for several B-fixes, C-02, C-04 norms, D-01 units, arithmetic edits/TO. CLI science, P1, conformal composition, isolation, repair, probe math **do not**. |
| Mocks/stubs | CLI I₄ + four calibration numbers + analyze-ignores-labels + repair ledger + identity cache. Worse than unittest.mock. |
| Paper behavior still unproven | Logistic P1, P2, C-layer **dev** selection, bilinear/BCE/BoundaryMLP, `predict_set` units, donor/swap-on-residual, C4 recompute, isolated exec, T2/T3 truth updates, R^surf beyond one fixture line |
| Delivery vs tests | “65 passed / defects closed / pipeline consumes upstream” **exceeds** test force |
| Confirmed problems? | **Yes.** Critical: F2-01. High: F2-00, F2-02..F2-07. |
| Channel pass? | **Fail.** Empty “looks fine” is inapplicable. |

Until CE-class tests exist and the freeze hash recomputes, any closing sentence of the form “code acceptance passed; independent review found no confirmed leftover defects” contradicts this channel’s evidence.
