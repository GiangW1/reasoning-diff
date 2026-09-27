import pytest
import torch

from reasoning_diff.models.tiny import build_tiny, decode_step, resid_post_hook


@pytest.mark.integration
@pytest.mark.parametrize("kind", ["qwen2", "qwen3"])
def test_tiny_forward_and_hook_cleanup(kind):
    torch.manual_seed(0)
    model = build_tiny(kind)
    model.eval()
    ids = torch.randint(0, 64, (1, 4))
    out = decode_step(model, ids)
    assert out.logits.shape[-1] == 64
    def add_one(t):
        return t + 1.0

    with resid_post_hook(model, 1, add_one) as rec:
        patched = decode_step(model, ids)
        assert rec.touched
    after = decode_step(model, ids)
    assert torch.allclose(out.logits, after.logits)
    assert not torch.allclose(out.logits, patched.logits)
