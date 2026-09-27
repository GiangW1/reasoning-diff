"""HotpotQA adapter. supporting_facts are answer evidence, not a full event DAG."""
from __future__ import annotations

from pathlib import Path
import re

from ..io import read_json
from ..schema import AnswerSpec, Edit, Premise, Task


def load_hotpot(path: str | Path, sidecar: dict | None = None) -> Task:
    record = read_json(path)
    premises = []
    cursor = 0
    question_parts = []
    for title, sentences in record["context"]:
        for i, sent in enumerate(sentences):
            pid = f"{title}:{i}"
            premises.append(Premise(pid, sent, cursor, cursor + len(sent), kind="sentence", document_id=title, sentence_id=i))
            cursor += len(sent) + 1
            question_parts.append(sent)
    support = {f"{title}:{sid}" for title, sid in record.get("supporting_facts", [])}
    question = record["question"]
    task = Task(
        task_id=record["_id"],
        base_group_id=record["_id"],
        variant_id=record.get("level", "base"),
        tier="T3",
        source="hotpotqa",
        source_kind="official",
        premises=premises or [Premise("q", question, 0, len(question))],
        question=question if premises else question,
        answer_spec=AnswerSpec(value=record.get("answer"), kind="span"),
        graph_status="partial" if sidecar else "unknown",
        graph_kind="supporting_facts_only",
        metadata={
            "supporting_facts": sorted(support),
            "supporting_facts_are_not_complete_dag": True,
            "unknown_non_support": True,
        },
    )
    if premises:
        # Question is independent of concatenated context; store context in metadata.
        task.question = question
        task.premises = [
            Premise(p.premise_id, p.text, 0, len(p.text), kind=p.kind, document_id=p.document_id, sentence_id=p.sentence_id)
            for p in premises
        ]
    return task


def document_edit(
    task: Task,
    document_id: str,
    replacement: str,
    new_answer: str | None = None,
    sentence_id: int | None = None,
) -> dict:
    if sentence_id is None:
        changed = [p.premise_id for p in task.premises if p.document_id == document_id]
        if len(changed) < 1:
            raise ValueError("document edit must list actual changed premise ids")
        parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", replacement) if part.strip()] or [replacement]
        replacement_rows = [
            Premise(f"{document_id}:{i}", part, 0, len(part), kind="sentence", document_id=document_id, sentence_id=i)
            for i, part in enumerate(parts)
        ]
        premises = []
        inserted = False
        for premise in task.premises:
            if premise.document_id == document_id:
                if not inserted:
                    premises.extend(replacement_rows)
                    inserted = True
            else:
                premises.append(premise)
    else:
        changed = [
            p.premise_id
            for p in task.premises
            if p.document_id == document_id and p.sentence_id == sentence_id
        ]
        if len(changed) < 1:
            raise ValueError("document edit must list actual changed premise ids")
        premises = []
        for premise in task.premises:
            if premise.premise_id in changed:
                premises.append(
                    Premise(premise.premise_id, replacement, 0, len(replacement), kind=premise.kind, document_id=document_id, sentence_id=premise.sentence_id)
                )
            else:
                premises.append(premise)
    data = task.to_dict()
    data.update(
        {
            "task_id": f"{task.task_id}::{document_id}",
            "variant_id": f"{task.variant_id}:{document_id}",
            "premises": [p.__dict__ if not isinstance(p, dict) else p for p in premises],
            "answer_spec": {
                **task.answer_spec.__dict__,
                "value": new_answer,
                "status": "requires_independent_truth",
            },
        }
    )
    edited = Task.from_dict(data)
    rec = Edit(
        id=f"edit:{task.task_id}:{document_id}",
        base_task_id=task.task_id,
        changed_premise_ids=changed,
        task=edited,
        kind="document",
        before={document_id: " ".join(p.text for p in task.premises if p.document_id == document_id)},
        after={document_id: replacement},
        validity="needs_truth",
    )
    return {
        "changed_premise_ids": changed,
        "single_premise_claim": False,
        "replacement": replacement,
        "task": edited,
        "edit": rec,
        "answer_updated": new_answer is not None,
    }
