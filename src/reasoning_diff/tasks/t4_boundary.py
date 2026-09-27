"""T4 boundary labels stay distinct; names are not inferred from dataset titles."""
from __future__ import annotations

from pathlib import Path

from ..io import read_json
from ..schema import AnswerSpec, Edit, Premise, T4_STATUSES, Task


def load_t4(path: str | Path) -> list[Task]:
    rows = read_json(path)
    tasks = []
    for row in rows:
        status = row["status"]
        if status not in T4_STATUSES:
            raise ValueError(f"T4 status must be one of {T4_STATUSES}")
        question = row["question"]
        tasks.append(
            Task(
                task_id=row["id"],
                base_group_id=row.get("family_id", row["id"]),
                variant_id=status,
                tier="T4",
                source="t4_boundary",
                source_kind="fixture",
                premises=[Premise("p0", question, 0, len(question), kind="placeholder")],
                question=question,
                answer_spec=AnswerSpec(value=row.get("answer"), kind="status", status=status),
                graph_status=row.get("graph_status", "unknown"),
                metadata={"boundary": status},
            )
        )
    return tasks


def apply_t4_question_edit(task: Task, new_question: str) -> Edit:
    premise = Premise("p0", new_question, 0, len(new_question), kind="placeholder")
    data = task.to_dict()
    data.update({"task_id": f"{task.task_id}::edit", "question": new_question, "premises": [premise.__dict__]})
    edited = Task.from_dict(data)
    return Edit(
        id=f"edit:{task.task_id}:q",
        base_task_id=task.task_id,
        changed_premise_ids=["p0"],
        task=edited,
        kind="t4_question",
        before={"p0": task.question},
        after={"p0": new_question},
        validity="needs_truth",
        metadata={"status_preserved": task.answer_spec.status},
    )
