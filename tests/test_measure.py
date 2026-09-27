from reasoning_diff.graphs import ancestors
from reasoning_diff.measure import cone_bundle, dependency_densities, joint_edit_counterexample
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def test_signed_excess_not_clipped():
    result = dependency_densities(
        premises=["p1", "p2", "p3", "p4"],
        task_set=["p1", "p2"],
        behavior_set=["p2"],
        noise_set=["p2", "p3"],
        sham_protocol={"name": "matched", "opportunities": 1},
    )
    assert result["rho_S_raw"] == 0.0
    assert result["rho_S_noise"] == 0.5
    assert result["rho_S_excess"] == -0.5


def test_zero_denominator_null():
    result = dependency_densities(premises=["p1"], task_set=["p1"], behavior_set=["p1"])
    assert result["rho_S_raw"] is None
    assert result["denominator_S"] is None


def test_joint_edit_blocks_soundness():
    def f(x, y):
        return x * y

    report = joint_edit_counterexample(f, [((0, 0), (1, 0)), ((0, 0), (0, 1))], ((0, 0), (1, 1)))
    assert report["single_point_unchanged"]
    assert report["joint_changed"]
    assert report["soundness_claim_allowed"] is False


def test_cone_fields_separated(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    bundle = cone_bundle(task, {"p1"}, ancestors(task))
    assert bundle["oracle_mask"]["source"] == "task_oracle"
    assert bundle["behavior_mask"]["source"] == "behavior_head"
    assert "q" in bundle["cone"]
