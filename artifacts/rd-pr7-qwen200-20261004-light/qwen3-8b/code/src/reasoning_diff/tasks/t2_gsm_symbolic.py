"""GSM-Symbolic official records + project formula sidecar. No untrusted eval."""
from __future__ import annotations

from pathlib import Path

from ..edits import apply_value_edit
from ..io import read_json
from ..events import extract_answer
from ..schema import AnswerSpec, Node, Premise, Task, canonical_value
from ..splits import gsm_family_id, gsm_text_key


def family_id(record: dict) -> str:
    return gsm_family_id(record) or canonical_value(str(record.get("id")))


def load_gsm_symbolic(path: str | Path, sidecar: dict | None = None) -> Task:
    record = read_json(path)
    question = record["question"]
    graph_status = "partial" if sidecar else "unknown"
    premises = []
    nodes = []
    if sidecar:
        for item in sidecar["premises"]:
            premises.append(
                Premise(
                    premise_id=item["id"],
                    text=question[item["start"]:item["end"]],
                    start=item["start"],
                    end=item["end"],
                    value=str(item["value"]),
                )
            )
        for item in sidecar.get("nodes", []):
            nodes.append(
                Node(
                    id=item["id"],
                    parents=list(item["parents"]),
                    value=str(item.get("value", "")),
                    aliases=[item["id"]],
                    expression=item["expression"],
                )
            )
    else:
        premises.append(Premise("q0", question, 0, len(question), kind="placeholder"))
    instance = record.get("instance", 0)
    gold = extract_answer(str(record["answer"]), "numeric") or canonical_value(record["answer"])
    task_id = f"{record['id']}:{instance}"
    return Task(
        task_id=task_id,
        record_id=task_id,
        base_group_id=family_id(record),
        variant_id=str(instance),
        tier="T2",
        source="gsm_symbolic",
        source_kind="official",
        premises=premises,
        question=question,
        answer_spec=AnswerSpec(value=gold, kind="numeric"),
        nodes=nodes,
        graph_status=graph_status,
        graph_kind="formula_sidecar" if sidecar else "none",
        target=sidecar.get("target") if sidecar else None,
        metadata={
            "canary": record.get("canary"),
            "original_id": record.get("original_id"),
            "text_family": family_id(record),
            "shared_gsm_family": family_id(record),
            "shared_gsm_text": gsm_text_key(record),
        },
    )


def apply_formula_edit(task: Task, sidecar: dict, premise_id: str, new_value: str) -> Task:
    if task.graph_status == "unknown":
        raise ValueError("Cannot legally edit without a formula sidecar")
    return apply_value_edit(task, premise_id, str(new_value)).task


def apply_operator_reverse_edit(task: Task, node_id: str):
    from ..edits import apply_operator_reverse

    if task.graph_status == "unknown":
        raise ValueError("Cannot legally edit without a formula sidecar")
    return apply_operator_reverse(task, node_id)


def score_numeric(prediction: str, gold: str) -> dict:
    ok = canonical_value(prediction) == canonical_value(gold)
    return {"metric": "exact_match", "value": 1.0 if ok else 0.0, "denominator": 1}
