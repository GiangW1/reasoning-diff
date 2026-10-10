import torch
from types import SimpleNamespace

from reasoning_diff.models.generate import decode_loop, sample_next, task_prompt
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


def test_decode_loop_stops_on_completed_output_condition():
    torch.manual_seed(0)
    model = build_tiny("qwen2")
    prompt = torch.randint(0, 64, (1, 3))
    out = decode_loop(
        model,
        prompt,
        torch.Generator().manual_seed(11),
        max_new=8,
        stop_condition=lambda produced: len(produced) == 2,
    )
    assert len(out["generated_ids"]) == 2
    assert out["stop_reason"] == "stop_condition"


def test_official_prompt_does_not_leak_target_membership_or_assignment_name():
    task = SimpleNamespace(
        question="How many Ingredient does Canned Beef have?",
        source_kind="official",
        answer_spec=SimpleNamespace(mod=23),
        target="total",
        nodes=[
            SimpleNamespace(id="paprika", aliases=["paprika", "Canned Beef's Paprika"], parents=[], expression="parsley"),
            SimpleNamespace(
                id="total",
                aliases=["total", "Canned Beef's Ingredient"],
                parents=["dill", "parsley", "paprika"],
                expression="dill + parsley + paprika",
            ),
        ],
        premises=[
            SimpleNamespace(premise_id="dill", kind="definition", text="The number of each Canned Beef's Dill equals 7"),
            SimpleNamespace(premise_id="parsley", kind="definition", text="The number of each Canned Beef's Parsley equals 22"),
        ],
    )
    prompt = task_prompt(task)
    assert "Canned Beef's Ingredient" not in prompt
    assert "Canned Beef's Dill" not in prompt
    assert "Canned Beef's Parsley" not in prompt
    assert "Canned Beef's Paprika" not in prompt
    assert "Full Name = final integer" not in prompt
    assert "Canned Beef's Ingredient = integer" not in prompt
    assert "compute every arithmetic operation modulo 23" in prompt
