"""Official iGSM snapshot loader. Uses template, never G; never imports tools.tools."""
from __future__ import annotations

from pathlib import Path

from ..edits import apply_value_edit, recompute
from ..io import read_json
from ..schema import AnswerSpec, Node, Premise, Task


SHARED_RNG = (-1, 0, 0, 0)


def load_igsm_snapshot(path: str | Path, source_kind: str = "official") -> Task:
    if source_kind != "official":
        raise ValueError("load_igsm_snapshot is only for official snapshots")
    data = read_json(path)
    if "G" in data and "template" not in data:
        raise ValueError("Official iGSM R_task must come from template, not G")
    template = data["template"]
    question = data["question"]
    premises = []
    for item in template["nodes"]:
        if tuple(item.get("id", ())) == SHARED_RNG or item.get("kind") == "shared_rng":
            continue
        if item.get("kind") != "premise":
            continue
        span = item["span"]
        premises.append(
            Premise(
                premise_id=item["param"],
                text=question[span[0]:span[1]],
                start=span[0],
                end=span[1],
                value=str(item["literal"]),
                kind="definition",
            )
        )
    nodes = []
    for item in template["nodes"]:
        if item.get("kind") != "compute":
            continue
        nodes.append(
            Node(
                id=item["param"],
                parents=list(item["parents"]),
                value=str(item.get("value", "")),
                aliases=[item["param"]],
                expression=item["expression"],
                scope="global",
            )
        )
    task = Task(
        task_id=data["native_id"],
        base_group_id=data.get("family_id", data["native_id"]),
        variant_id=data.get("variant_id", "base"),
        tier="T1",
        source="facebookresearch/iGSM",
        source_kind="official",
        premises=premises,
        question=question,
        answer_spec=AnswerSpec(value=str(data["answer"]), kind="numeric", mod=int(data.get("mod", 23))),
        nodes=nodes,
        graph_status="complete",
        graph_kind="igsm_template",
        target=data.get("target"),
        metadata={
            "revision": data.get("revision"),
            "op": data.get("op"),
            "n_op": data.get("n_op"),
            "ignored_structure_graph": "G" in data,
            "shared_rng_excluded": True,
            "lookup_ignored": "lookup" in data,
        },
    )
    task.validate()
    recomputed = recompute(task)
    if recomputed.answer_spec.value != task.answer_spec.value:
        raise ValueError("official dump answer does not match template recompute")
    return recomputed


def official_value_edit(task: Task, premise_id: str, new_literal: str) -> Task:
    if task.source_kind != "official":
        raise ValueError("official_value_edit requires an official task")
    return apply_value_edit(task, premise_id, new_literal).task


def load_igsm_directory(root: str | Path) -> list[Task]:
    root = Path(root)
    files = [root] if root.is_file() else sorted(root.glob("**/*.json"))
    return [load_igsm_snapshot(path) for path in files]
