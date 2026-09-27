"""HumanEval-derived spec edits. Scoring uses an isolated executor only."""
from __future__ import annotations

from pathlib import Path

from ..io import read_json
from ..schema import AnswerSpec, Edit, Premise, Task
from ..scoring import score_code


def load_humaneval(path: str | Path) -> Task:
    record = read_json(path)
    prompt = record["prompt"]
    return Task(
        task_id=record["task_id"],
        base_group_id=record["task_id"],
        variant_id=record.get("variant_id", "base"),
        tier="T3",
        source="humaneval_derived",
        source_kind=record.get("source_kind", "project_derived"),
        premises=[Premise("spec", prompt, 0, len(prompt), kind="placeholder")],
        question=prompt,
        answer_spec=AnswerSpec(value=record.get("canonical_solution"), kind="code"),
        graph_status="unknown",
        graph_kind="none",
        metadata={
            "entry_point": record.get("entry_point"),
            "test": record.get("test"),
            "reference_dfg_is_not_task_dag": True,
        },
    )


def apply_spec_edit(
    task: Task,
    new_prompt: str,
    new_tests: str,
    new_solution: str | None = None,
    edit_kind: str = "spec",
    executor=None,
) -> Edit:
    premise = Premise("spec", new_prompt, 0, len(new_prompt), kind="placeholder")
    data = task.to_dict()
    scored = None
    if new_solution is not None and new_tests:
        scored = score_code(new_solution, new_tests, executor=executor)
    valid = bool(scored and scored.get("value") == 1.0)
    data.update(
        {
            "task_id": f"{task.task_id}::spec",
            "variant_id": f"{task.variant_id}:spec",
            "question": new_prompt,
            "premises": [premise.__dict__],
            "answer_spec": {**task.answer_spec.__dict__, "value": new_solution, "status": None if valid else "requires_independent_truth"},
            "metadata": {**task.metadata, "test": new_tests, "spec_edited": True, "edit_kind": edit_kind, "score": scored},
        }
    )
    edited = Task.from_dict(data)
    return Edit(
        id=f"edit:{task.task_id}:spec",
        base_task_id=task.task_id,
        changed_premise_ids=["spec"],
        task=edited,
        kind=edit_kind,
        before={"spec": task.question},
        after={"spec": new_prompt},
        validity="valid" if valid else "needs_truth",
        metadata={
            "distinguishing_tests": bool(new_tests),
            "invariant_behavior_unspecified": edit_kind != "invariant_behavior",
            "input_list_edit": edit_kind == "input_list",
            "executor_status": None if scored is None else scored.get("status"),
        },
    )


def score_submission(source: str, tests: str, executor=None) -> dict:
    return score_code(source, tests, executor=executor)
