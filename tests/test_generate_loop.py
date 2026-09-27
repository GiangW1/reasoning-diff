import torch

from reasoning_diff.models.generate import decode_loop, sample_next
from reasoning_diff.models.tiny import build_tiny


def test_explicit_generator_replay():
    torch.manual_seed(0)
    model = build_tiny("qwen2")
    prompt = torch.randint(0, 64, (1, 3))
    g1 = torch.Generator().manual_seed(11)
    g2 = torch.Generator().manual_seed(11)
    a = decode_loop(model, prompt, g1, max_new=3)
    b = decode_loop(model, prompt, g2, max_new=3)
    assert a["generated_ids"] == b["generated_ids"]
    greedy = sample_next(torch.tensor([[0.1, 5.0, 0.2]]), torch.Generator().manual_seed(0), temperature=0)
    assert int(greedy.item()) == 1
