"""MuSiQue adapter. Composition references are not all legal reasoning routes."""
from __future__ import annotations

from pathlib import Path

from ..io import read_json
from ..schema import AnswerSpec, Edit, Node, Premise, Task


def load_musique_records(path: str | Path) -> list[Task]:
    payload = read_json(path)
    records = payload if isinstance(payload, list) else payload["records"]
    tasks = []
    for record in records:
        paras = record.get("paragraphs") or []
        premises = [
            Premise(
                f"p{p['idx']}",
                p["paragraph_text"],
                0,
                len(p["paragraph_text"]),
                kind="paragraph",
                document_id=p.get("title"),
            )
            for p in paras
        ] or [Premise("q", record["question"], 0, len(record["question"]))]
        nodes = []
        for item in record.get("question_decomposition") or []:
            parents = []
            for token in item["question"].split():
                token = token.strip(".,;:?!)")
                if token.startswith("#") and token[1:].rstrip(".").isdigit():
                    parents.append(f"s{token[1:]}")
            if item.get("paragraph_support_idx") is not None:
                parents.append(f"p{item['paragraph_support_idx']}")
            nodes.append(
                Node(
                    id=f"s{item['id']}",
                    parents=parents or [premises[0].premise_id],
                    value=str(item.get("answer") or ""),
                    expression="composition_reference",
                )
            )
        variant = "answerable" if record.get("answerable", True) else "unanswerable"
        tasks.append(
            Task(
                task_id=f"{record['id']}::{variant}",
                base_group_id=record["id"],
                variant_id=variant,
                tier="T3",
                source="musique",
                source_kind="official",
                premises=premises,
                question=record["question"],
                answer_spec=AnswerSpec(
                    value=record.get("answer"),
                    kind="span",
                    aliases=list(record.get("answer_aliases") or []),
                    status=None if record.get("answerable", True) else "no_solution",
                ),
                nodes=nodes,
                graph_status="partial",
                graph_kind="composition_reference",
                metadata={"native_id": record["id"], "answerable": record.get("answerable", True)},
            )
        )
    ids = [t.task_id for t in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("MuSiQue variants must keep distinct record ids")
    return tasks


def paragraph_edit(task: Task, premise_id: str, replacement: str, new_answer: str | None = None) -> Task:
    premises = []
    found = False
    for premise in task.premises:
        if premise.premise_id == premise_id:
            found = True
            premises.append(
                Premise(premise.premise_id, replacement, 0, len(replacement), kind=premise.kind, document_id=premise.document_id)
            )
        else:
            premises.append(premise)
    if not found:
        raise ValueError(f"unknown paragraph {premise_id}")
    data = task.to_dict()
    data.update(
        {
            "task_id": f"{task.task_id}::{premise_id}",
            "premises": [p.__dict__ for p in premises],
            "answer_spec": {**task.answer_spec.__dict__, "value": new_answer, "status": "requires_independent_truth"},
            "nodes": [
                {**n, "value": ""} if isinstance(n, dict) else n
                for n in data.get("nodes", [])
            ],
        }
    )
    for node in data["nodes"]:
        if isinstance(node, dict):
            node["value"] = ""
    edited = Task.from_dict(data)
    return Edit(
        id=f"edit:{task.task_id}:{premise_id}",
        base_task_id=task.task_id,
        changed_premise_ids=[premise_id],
        task=edited,
        kind="paragraph",
        before={premise_id: next(p.text for p in task.premises if p.premise_id == premise_id)},
        after={premise_id: replacement},
        validity="needs_truth",
    )
