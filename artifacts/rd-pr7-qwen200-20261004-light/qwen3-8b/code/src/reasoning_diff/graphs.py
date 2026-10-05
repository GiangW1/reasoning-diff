"""Independent task graphs: ancestors, status, dirty cones."""
from __future__ import annotations

from .schema import GRAPH_STATUSES, Task


def ancestors(task: Task) -> dict[str, set[str]]:
    """Return premise-only ancestor sets for each node (R_task columns)."""
    task.validate()
    if task.graph_kind in {"composition_reference", "supporting_facts_only", "none"}:
        return {}
    result: dict[str, set[str]] = {p.premise_id: {p.premise_id} for p in task.premises}
    known = set(result)
    for node in task.nodes:
        if not set(node.parents) <= known:
            raise ValueError(f"Node {node.id} parents are not yet defined")
        acc: set[str] = set()
        for parent in node.parents:
            acc |= result[parent]
        result[node.id] = acc
        known.add(node.id)
    return {node.id: result[node.id] for node in task.nodes}


def graph_status(task: Task) -> str:
    if task.graph_status not in GRAPH_STATUSES:
        raise ValueError(f"Invalid graph_status {task.graph_status}")
    if not task.nodes and task.graph_status == "complete":
        raise ValueError("Empty node list is not a complete graph; use unknown")
    return task.graph_status


def dirty_cone(task: Task, changed_premises: set[str], predicted: dict[str, set[str]] | None = None) -> set[str]:
    """cone(ΔP) = {s : R(s) ∩ ΔP ≠ ∅}. Default R is task ancestors."""
    refs = predicted if predicted is not None else ancestors(task)
    return {node_id for node_id, deps in refs.items() if set(deps) & set(changed_premises)}


def oracle_mask(task: Task, changed_premises: set[str]) -> dict:
    cone = dirty_cone(task, changed_premises, ancestors(task))
    return {"source": "task_oracle", "changed_premises": sorted(changed_premises), "slots": sorted(cone)}


def behavior_mask(predicted: dict[str, set[str]], changed_premises: set[str]) -> dict:
    cone = {node_id for node_id, deps in predicted.items() if set(deps) & set(changed_premises)}
    return {"source": "behavior_head", "changed_premises": sorted(changed_premises), "slots": sorted(cone)}
