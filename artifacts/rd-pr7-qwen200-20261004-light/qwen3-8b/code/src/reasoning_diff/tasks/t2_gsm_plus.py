"""GSM-Plus official records are test-only. Solution text is not a DAG."""
from __future__ import annotations

from pathlib import Path

from ..io import read_json
from ..schema import AnswerSpec, Edit, Premise, Task, T4_STATUSES, canonical_value
from ..splits import gsm_family_id, gsm_text_key, lock_test_only, register_test_only_family


def load_gsm_plus(path: str | Path) -> Task:
    record = read_json(path)
    question = record["question"]
    perturbation = record.get("perturbation_type", "")
    status = None
    if perturbation in {"missing information", "critical thinking"}:
        status = "insufficient_information"
    elif perturbation == "reversing operation":
        status = None
    family = gsm_family_id(record)
    text_key = gsm_text_key(record)
    register_test_only_family(family, text_key)
    premises = [Premise("seed", question, 0, len(question), kind="placeholder")]
    task = Task(
        task_id=str(record.get("id") or canonical_value(question)[:24]),
        base_group_id="gsm_plus:" + family,
        variant_id=perturbation or "base",
        tier="T2",
        source="gsm_plus",
        source_kind="official",
        premises=premises,
        question=question,
        answer_spec=AnswerSpec(
            value=canonical_value(record.get("answer", "")),
            kind="numeric",
            status=status,
        ),
        graph_status="unknown",
        graph_kind="none",
        metadata={
            "fit_eligible": False,
            "perturbation_type": perturbation,
            "solution_is_not_dag": True,
            "shared_gsm_family": family,
            "shared_gsm_text": text_key,
            "perturbation_status": "query_target_change" if perturbation == "reversing operation" else None,
        },
    )
    task.metadata["role"] = lock_test_only("gsm_plus")
    return task


def apply_plus_numeric_edit(task: Task, old: str, new: str, new_answer: str | None = None) -> Edit:
    from ..edits import _replace_isolated_value

    if old not in task.question:
        raise ValueError("no editable numeral in GSM-Plus question")
    question = _replace_isolated_value(task.question, old, new)
    premise = Premise("seed", question, 0, len(question), kind="placeholder")
    data = task.to_dict()
    data.update(
        {
            "task_id": f"{task.task_id}::num",
            "question": question,
            "premises": [premise.__dict__],
            "answer_spec": {**task.answer_spec.__dict__, "value": new_answer, "status": "requires_independent_truth"},
        }
    )
    edited = Task.from_dict(data)
    return Edit(
        id=f"edit:{task.task_id}:num",
        base_task_id=task.task_id,
        changed_premise_ids=["seed"],
        task=edited,
        kind="plus_numeric",
        before={"seed": old},
        after={"seed": new},
        validity="needs_truth",
    )


def refuse_fit_split(task: Task, requested: str) -> None:
    if task.metadata.get("fit_eligible") is False and requested != "test":
        raise ValueError("GSM-Plus cannot be assigned a fitting role")
