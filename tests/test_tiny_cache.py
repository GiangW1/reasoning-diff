import torch

from reasoning_diff.models.collect import collect_tiny, intervene_tiny
from reasoning_diff.models.tiny import build_tiny, decode_step


def test_use_cache_false_still_mutates_passed_cache():
    model = build_tiny("qwen2")
    ids = torch.randint(0, 64, (1, 3))
    first = decode_step(model, ids, past=None, use_cache=True)
    cache = first.past_key_values
    before = cache.layers[0].keys.clone()
    decode_step(model, ids[:, -1:], past=cache, use_cache=False)
    # Transformers 5.5.3: a passed cache can update even when use_cache=False.
    assert not torch.equal(before, cache.layers[0].keys)


def test_collect_and_intervene_tiny():
    out = collect_tiny("qwen3", [1, 2, 3], max_new=2)
    assert out["weight_source"] == "random_init"
    assert out["hidden_prefix"].shape[-1] == 32
    assert out["features"]["pre_step"]["leaks_target"] is False
    inter = intervene_tiny("qwen2", [1, 2, 3, 4])
    assert inter["hook"] == "resid_post"
    assert inter["cache_isolated"] is True
    assert not torch.equal(inter["base_logits"], inter["patched_logits"])
