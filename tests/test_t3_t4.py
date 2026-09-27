import pytest

from reasoning_diff.executor import SpyExecutor
from reasoning_diff.schema import T4_STATUSES
from reasoning_diff.scoring import score_code
from reasoning_diff.tasks.t3_hotpot import document_edit, load_hotpot
from reasoning_diff.tasks.t3_humaneval import load_humaneval, score_submission
from reasoning_diff.tasks.t3_musique import load_musique_records
from reasoning_diff.tasks.t4_boundary import load_t4


def test_hotpot_support_is_not_full_dag():
    task = load_hotpot("tests/fixtures/t3_hotpot_one.json")
    assert task.graph_status == "unknown"
    assert task.metadata["supporting_facts_are_not_complete_dag"] is True
    edited = document_edit(task, "DocA", "The film was produced in Spain.")
    assert len(edited["changed_premise_ids"]) == 2
    assert edited["single_premise_claim"] is False


def test_musique_keeps_unanswerable_pair():
    tasks = load_musique_records("tests/fixtures/t3_musique_pair.json")
    assert len(tasks) == 2
    assert {t.variant_id for t in tasks} == {"answerable", "unanswerable"}
    assert tasks[0].base_group_id == tasks[1].base_group_id
    assert tasks[0].graph_kind == "composition_reference"


def test_humaneval_never_host_exec():
    task = load_humaneval("tests/fixtures/t3_humaneval_one.json")
    spy = SpyExecutor()
    result = score_code("def add(a,b): return a+b", task.metadata["test"], executor=spy)
    assert result["status"] == "executor_unavailable"
    assert result["value"] is None
    assert len(spy.calls) == 1
    assert score_submission("print(1)", "assert False", executor=spy)["status"] == "executor_unavailable"
    assert len(spy.calls) == 2
    rejected = score_code("exec('x')", "assert True", executor=spy)
    assert rejected["status"] == "rejected"


def test_t4_statuses_distinct():
    tasks = load_t4("tests/fixtures/t4_boundary.json")
    assert {t.answer_spec.status for t in tasks} == set(T4_STATUSES)
