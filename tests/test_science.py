import math

import numpy as np
import pytest

from reasoning_diff.analysis import p1_incremental, p3_recovery, week8_decision
from reasoning_diff.baselines import verbalizer
from reasoning_diff.events import boundary_index
from reasoning_diff.interventions import apply_swap, orthonormal_basis
from reasoning_diff.models.features import select_prefix_index
from reasoning_diff.probes.calibrate import conformal_threshold, sequence_score
from reasoning_diff.repair import run_repair
from reasoning_diff.rng import StreamBank
from reasoning_diff.splits import require_split
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.tasks.t2_noop import make_noop_pair
from reasoning_diff.transfer import apply_map, direct_transfer, fit_linear_map


def test_conformal_examples():
    finite = conformal_threshold([0.1, 0.2, 0.3, 0.4], 0.4)
    assert finite["q"] == 0.3
    inf = conformal_threshold([0.1, 0.2, 0.3, 0.4], 0.1)
    assert math.isinf(inf["q"])
    assert sequence_score([0.1, 0.9], True, False) == 0.9
    assert sequence_score([], True, True) == 0.0
    assert sequence_score([0.2], False, False) is None


def test_direct_transfer_rejects_4096_3584():
    assert direct_transfer(4096, 3584)["status"] == "not_applicable_dimension_mismatch"
    src = np.ones((5, 4))
    tgt = np.ones((5, 6))
    fitted = fit_linear_map(src, tgt, "transfer_pairs", labeled=False)
    assert fitted["status"] == "unlabeled_pair_adapt"
    mapped = apply_map(tgt, fitted)
    assert mapped.shape == (5, 4)
    with pytest.raises(ValueError):
        require_split("test", ("transfer_pairs",), "transfer mapping")


def test_boundary_excludes_straddle():
    assert boundary_index([[0, 2], [2, 8], [8, 9]], 6) == 0
    feat = select_prefix_index([[0, 2], [2, 8], [8, 9]], 6, "pre_step")
    assert feat["token_index"] == 0
    assert feat["straddling_excluded"] == [1]


def test_streams_are_independent():
    bank = StreamBank(0)
    a = bank.get("sample").random()
    b = StreamBank(0).get("direction").random()
    assert a != b


def test_week8_never_passes_unregistered():
    decision = week8_decision({"status": "not_evaluated"})
    assert decision["gates"]["gate0"]["decision"] == "unregistered"
    assert decision["scientific_conclusion"] is None
    p3 = p3_recovery(0.4, 0.4, 0.4, 0.2)
    assert p3["causal_reverse_claim"] is False


def test_p1_null_on_single_class():
    out = p1_incremental(np.ones(3), np.ones(3), np.ones(3), np.zeros(3))
    assert out["auc_full"] is None


def test_verbalizer_supervision_contract():
    with pytest.raises(ValueError):
        verbalizer("supervised", "p", "gold", trained=False)
    assert verbalizer("zeroshot", "pre", None, False)["visibility"] == "prospective"
    assert verbalizer("reflection", "pre", None, False)["visibility"] == "retrospective"


def test_repair_reprefills_and_refuses_gate():
    rec = run_repair("task_oracle", ["q"], [3], "new prefix")
    assert rec.refilled_prefix is False
    assert rec.status == "prefill_unavailable"
    assert rec.extra_prefill_tokens is None
    ran = run_repair("task_oracle", ["q"], [3], "new prefix", prefix_token_ids=[1, 2, 3], generated_tokens=[9])
    assert ran.refilled_prefix is False
    assert ran.status == "prefill_unavailable"
    assert not ran.gated
    with pytest.raises(ValueError):
        run_repair("not-a-mask", ["q"], [3], "x")


def test_swap_formula():
    base = np.array([1.0, 0.0])
    donor = np.array([0.0, 1.0])
    basis = np.array([[0.0], [1.0]])
    out = apply_swap(base, donor, basis)
    assert np.allclose(out, np.array([1.0, 1.0]))


def test_noop_pair_is_project_derived(t1_tiny_path):
    base = load_t1_fixture(t1_tiny_path)
    pair = make_noop_pair(base, "A red herring is mentioned.", "front", "high", True)
    assert pair.source == "reasoning_diff_noop"
    assert pair.source_kind == "project_derived"
    assert pair.metadata["official_noop_release"] is False
    assert any(p.premise_id == "noop" for p in pair.premises)
