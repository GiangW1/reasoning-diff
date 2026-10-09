import pytest
import torch

from reasoning_diff.models.quantity_constraint import QuantityConstraint


class CharacterTokenizer:
    eos_token_id = 127
    all_special_ids = [127]
    def __len__(self):
        return 128
    def encode(self, text, **kw):
        return list(map(ord, text))
    def decode(self, ids, **kw):
        return ''.join(chr(i) for i in ids if i != 127)


def advance(constraint, limit=1000):
    tokens = []
    for _ in range(limit):
        logits = torch.zeros(1, 128)
        # Try ending early, using arbitrary tags, then produce a model value 7.
        logits[0, 127] = 100
        logits[0, ord('<')] = 90
        logits[0, ord('7')] = 80
        token = int(constraint.mask(logits).argmax())
        constraint.accept(token)
        tokens.append(token)
        if token == 127:
            break
    return tokens


def test_adversarial_model_cannot_move_steps_to_answer_or_supply_extra_nodes():
    tokenizer = CharacterTokenizer()
    constraint = QuantityConstraint(tokenizer, ['a', 'b'], reasoning_limit=4)
    text = tokenizer.decode(advance(constraint))
    assert text == ('<think>\n<step node="a"><commit>7</commit></step>\n'
                    '<step node="b"><commit>7</commit></step>\n</think>\n\\boxed{777777777777}')
    assert constraint.report()['complete']
    assert constraint.report()['sampled_numeric_tokens'] == 14


def test_prefix_replay_continues_the_same_constraint_including_mid_tag():
    tokenizer = CharacterTokenizer()
    original = advance(QuantityConstraint(tokenizer, ['a', 'b']))
    for boundary in [1, 15, 35, 60, len(original) - 2]:
        recovered = QuantityConstraint(tokenizer, ['a', 'b'])
        for token in original[:boundary]:
            recovered.accept(token)
        assert original[:boundary] + advance(recovered) == original


def test_budget_does_not_append_missing_commits_or_final_answer():
    constraint = QuantityConstraint(CharacterTokenizer(), ['a'])
    produced = advance(constraint, limit=5)
    assert len(produced) == 5 and not constraint.report()['complete']


def test_reasoning_cap_and_invalid_prefix_are_explicit():
    constraint = QuantityConstraint(CharacterTokenizer(), ['a'], reasoning_limit=3)
    while constraint.phase != 'reasoning':
        token = int(constraint.mask(torch.zeros(1, 128)).argmax())
        constraint.accept(token)
    for _ in range(3):
        constraint.accept(ord('x'))
    assert int(constraint.mask(torch.zeros(1, 128)).argmax()) == ord('<')
    assert constraint.report()['reasoning_budget_forced_commits'] == 1
    with pytest.raises(ValueError, match='prefix'):
        QuantityConstraint(CharacterTokenizer(), ['a']).accept(ord('x'))


def test_batched_and_single_decoding_keep_independent_constraint_state(monkeypatch):
    import importlib
    from pathlib import Path
    from reasoning_diff.models.generate import decode_loop
    from reasoning_diff.models.tiny import build_tiny
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'scripts'))
    batching = importlib.import_module('trace_batching')
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(12)
        model = build_tiny('qwen2').eval()
        model.resize_token_embeddings(128)
    prompts = [torch.tensor([[1, 2]]), torch.tensor([[1, 2, 3]])]
    tokenizer = CharacterTokenizer()
    expected = [decode_loop(model, prompt, torch.Generator().manual_seed(i), 300, eos_id=127,
                    constraint=QuantityConstraint(tokenizer, nodes, reasoning_limit=2))
                for i, (prompt, nodes) in enumerate(zip(prompts, [['a'], ['a', 'b']]))]
    requests = [batching.DecodeRequest(model, prompt, torch.Generator().manual_seed(i), 300, eos_id=127,
                    constraint=QuantityConstraint(tokenizer, nodes, reasoning_limit=2))
                for i, (prompt, nodes) in enumerate(zip(prompts, [['a'], ['a', 'b']]))]
    actual = batching.decode_batch(requests)
    assert [r['generated_ids'] for r in actual] == [r['generated_ids'] for r in expected]
    assert all(r['quantity_constraint']['complete'] for r in actual)
    clone = requests[0].constraint.fork()
    clone.forced.append(-1)
    assert -1 not in requests[0].constraint.forced
