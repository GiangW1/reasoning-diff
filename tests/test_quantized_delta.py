import numpy as np
import pytest
import torch

from reasoning_diff.models import collect


@pytest.mark.parametrize('target', [.025, .123])
def test_bfloat16_delta_matches_measured_norm_without_changing_direction(target):
    original = torch.linspace(-2, 2, 256).to(torch.bfloat16).reshape(1, 1, -1)
    delta = np.random.default_rng(17).normal(size=256)
    delta *= target / np.linalg.norm(delta)
    changed, calibration = collect.quantized_norm_matched_add(original, delta, target)
    measured = float((changed.float() - original.float()).norm())
    assert np.isclose(measured, target, rtol=.02, atol=1e-4)
    expected = torch.as_tensor(original.float().numpy().reshape(-1).astype(float)
                               + calibration['scale'] * delta, dtype=original.dtype).view_as(original)
    assert torch.equal(changed, expected)
    assert calibration['actual_norm'] == measured


def test_unrepresentable_delta_is_rejected_not_reported_as_matched():
    original = torch.ones(1, 1, 32, dtype=torch.bfloat16)
    with pytest.raises(ValueError, match='representable'):
        collect.quantized_norm_matched_add(original, np.ones(32) * 1e-4, 1e-3)


def test_zero_target_is_exact_identity():
    original = torch.ones(1, 1, 32, dtype=torch.bfloat16)
    changed, calibration = collect.quantized_norm_matched_add(original, np.ones(32), 0)
    assert torch.equal(original, changed)
    assert calibration['actual_norm'] == 0


def test_calibration_reaches_real_bfloat16_residual_hook():
    from reasoning_diff.models.tiny import build_tiny
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(12)
        model = build_tiny('qwen3').to(dtype=torch.bfloat16).eval()
    delta = np.random.default_rng(9).normal(size=model.config.hidden_size)
    delta *= .05 / np.linalg.norm(delta)
    decoded = collect.intervene_hidden_decode('qwen3', [1, 2], 1, model=model,
        mode='add_delta', delta=delta, target_delta_norm=.05, event_aligned=True,
        target_prefix_len=2, max_new=1)
    assert decoded['hook_fired'] and decoded['prefix_boundary_verified']
    assert np.isclose(decoded['hook_delta_norm'], .05, rtol=.02, atol=1e-4)
    assert np.isclose(decoded['hook_delta_norm'], decoded['norm_calibration']['actual_norm'], rtol=1e-6)
