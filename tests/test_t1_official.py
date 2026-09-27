from reasoning_diff.edits import apply_value_edit
from reasoning_diff.graphs import ancestors
from reasoning_diff.tasks.t1_config import validate_t1_prepare_config
from reasoning_diff.tasks.t1_official import SHARED_RNG, load_igsm_snapshot


def test_template_not_g_and_mod23(tmp_path):
    from pathlib import Path

    path = Path("tests/fixtures/t1_official_shape.json")
    task = load_igsm_snapshot(path, source_kind="official")
    assert task.source_kind == "official"
    assert task.answer_spec.mod == 23
    assert ancestors(task)["q"] == {"a", "b"}
    assert task.metadata["ignored_structure_graph"] is True
    assert task.metadata["shared_rng_excluded"] is True
    assert SHARED_RNG == (-1, 0, 0, 0)
    edited = apply_value_edit(task, "a", "4")
    assert edited.task.nodes[0].value != "99"
    assert edited.task.answer_spec.value == "12"


def test_config_ops():
    checked = validate_t1_prepare_config({"ops": [5, 10, 15, 21], "n_problems": 500, "mod": 23})
    assert checked["status"] == "checked"


def test_no_tools_import():
    import reasoning_diff.tasks.t1_official as mod
    text = open(mod.__file__, encoding="utf-8").read()
    assert "import tools" not in text and "from tools" not in text
