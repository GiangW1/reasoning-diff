"""Legal edits recompute answers from expressions; they never reuse stale lookup values."""
from __future__ import annotations

import ast
import operator
import re
from typing import Any

from .events import NUMBER
from .schema import Edit, Premise, Task, canonical_value
from .graphs import ancestors

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def _eval_expr(expr: str, env: dict[str, Any], mod: int | None) -> Any:
    tree = ast.parse(expr, mode="eval")

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -walk(node.operand)
        if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
            right = walk(node.right)
            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
                raise ValueError("operator reverse is not a consistent text transformation")
            value = _BINOPS[type(node.op)](walk(node.left), right)
            if mod is not None and isinstance(value, (int, float)):
                return int(value) % mod
            return value
        if isinstance(node, ast.Name):
            if node.id not in env:
                raise ValueError(f"Unknown name in expression: {node.id}")
            raw = env[node.id]
            try:
                return int(str(raw).replace(",", ""))
            except ValueError:
                return float(raw)
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    return walk(tree)


def recompute(task: Task) -> Task:
    env: dict[str, Any] = {}
    for premise in task.premises:
        env[premise.premise_id] = premise.value
    mod = task.answer_spec.mod
    new_nodes = []
    for node in task.nodes:
        if not node.expression:
            raise ValueError(f"Node {node.id} has no expression; cannot recompute from lookup")
        value = _eval_expr(node.expression, env, mod)
        env[node.id] = value
        text = canonical_value(value)
        new_nodes.append(
            type(node)(
                id=node.id,
                parents=list(node.parents),
                value=text,
                aliases=list(node.aliases),
                expression=node.expression,
                scope=node.scope,
            )
        )
    answer = task.answer_spec
    new_answer = type(answer)(
        value=canonical_value(env[task.target]) if task.target else answer.value,
        kind=answer.kind,
        mod=answer.mod,
        aliases=list(answer.aliases),
        status=answer.status,
    )
    updated = Task.from_dict(
        {
            **task.to_dict(),
            "nodes": [n.__dict__ for n in new_nodes],
            "answer_spec": new_answer.__dict__,
        }
    )
    ancestors(updated)
    return updated


def _replace_isolated_value(span: str, old: str, new: str) -> str:
    if not old:
        return f"{span}={new}"
    tokens = list(re.finditer(NUMBER, span))
    if "." not in old:
        for match in tokens:
            token = match.group()
            if "." in token and token.split(".", 1)[0].lstrip("+-") == old.lstrip("+-"):
                raise ValueError(f"value {old!r} is not a unique isolated token in {span!r}")
    matches = [m for m in tokens if m.group() == old]
    if len(matches) != 1:
        raise ValueError(f"value {old!r} is not a unique isolated token in {span!r}")
    start, end = matches[0].span()
    return span[:start] + new + span[end:]


def apply_value_edit(task: Task, premise_id: str, new_literal: str, edit_id: str | None = None) -> Edit:
    found = next((p for p in task.premises if p.premise_id == premise_id), None)
    if found is None:
        raise ValueError(f"Unknown premise {premise_id}")
    before = {premise_id: found.value or ""}
    new_text = _replace_isolated_value(found.text, found.value or "", new_literal) if found.value else f"{found.text}={new_literal}"
    question = task.question[: found.start] + new_text + task.question[found.end :]
    delta = len(new_text) - len(found.text)
    premises = []
    for premise in task.premises:
        start = premise.start + (delta if premise.start > found.start else 0)
        end = premise.end + (delta if premise.start > found.start else 0)
        if premise.premise_id == premise_id:
            premises.append(Premise(premise.premise_id, new_text, start, start + len(new_text), new_literal, premise.kind))
        else:
            premises.append(Premise(premise.premise_id, premise.text, start, end, premise.value, premise.kind))
    new_id = f"{task.task_id}::{premise_id}={new_literal}"
    draft = Task.from_dict(
        {
            **task.to_dict(),
            "task_id": new_id,
            "record_id": new_id,
            "variant_id": f"{task.variant_id}:{premise_id}",
            "question": question,
            "premises": [p.__dict__ for p in premises],
            "edit_ref": premise_id,
        }
    )
    recomputed = recompute(draft)
    return Edit(
        id=edit_id or f"edit:{task.task_id}:{premise_id}:{new_literal}",
        base_task_id=task.task_id,
        changed_premise_ids=[premise_id],
        task=recomputed,
        kind="value",
        before=before,
        after={premise_id: new_literal},
        validity="valid",
        metadata={"recomputed": True},
    )


def _rewrite_ids(text: str | None, mapping: dict[str, str]) -> str:
    out = text or ""
    if not mapping:
        return out
    keys = sorted(mapping, key=len, reverse=True)
    pattern = re.compile(r"(?<!\w)(" + "|".join(re.escape(key) for key in keys) + r")(?!\w)")
    return pattern.sub(lambda match: mapping[match.group(1)], out)


def apply_rename_edit(task: Task, mapping: dict[str, str], edit_id: str | None = None) -> Edit:
    question = _rewrite_ids(task.question, mapping)
    premises = []
    for premise in task.premises:
        text = _rewrite_ids(premise.text, mapping)
        start = question.find(text)
        if start < 0:
            raise ValueError(f"renamed premise {premise.premise_id} missing from question")
        premises.append(
            Premise(
                mapping.get(premise.premise_id, premise.premise_id),
                text,
                start,
                start + len(text),
                premise.value,
                premise.kind,
            )
        )
    nodes = []
    for node in task.nodes:
        aliases = [mapping.get(alias, alias) for alias in node.aliases]
        nodes.append(
            type(node)(
                id=mapping.get(node.id, node.id),
                parents=[mapping.get(parent, parent) for parent in node.parents],
                value=node.value,
                aliases=aliases,
                expression=_rewrite_ids(node.expression, mapping) if node.expression else node.expression,
                scope=node.scope,
            )
        )
    data = task.to_dict()
    new_id = f"{task.task_id}::rename"
    data.update(
        {
            "task_id": new_id,
            "record_id": new_id,
            "variant_id": f"{task.variant_id}:rename",
            "question": question,
            "premises": [p.__dict__ for p in premises],
            "nodes": [n.__dict__ for n in nodes],
            "target": mapping.get(task.target, task.target) if task.target else task.target,
        }
    )
    return Edit(
        id=edit_id or f"edit:{task.task_id}:rename",
        base_task_id=task.task_id,
        changed_premise_ids=[],
        task=Task.from_dict(data),
        kind="rename",
        before=dict(mapping),
        after={v: k for k, v in mapping.items()},
        validity="valid",
        metadata={"values_unchanged": True},
    )


def _target_parents(task: Task) -> set[str]:
    node = next((item for item in task.nodes if item.id == task.target), None)
    return set(node.parents) if node else set()


def apply_alt_source_same_value(task: Task, premise_id: str, edit_id: str | None = None) -> Edit:
    """Keep leaf *a*, add equal-value leaf *b*, retarget so the graph reads *b* not *a*."""
    found = next((p for p in task.premises if p.premise_id == premise_id), None)
    if found is None:
        raise ValueError(f"Unknown premise {premise_id}")
    new_id = "src_b"
    if any(p.premise_id == new_id for p in task.premises):
        raise ValueError("src_b already exists")
    value = found.value or ""
    new_text = f"{new_id} = {value}"
    mapping = {premise_id: new_id}
    question = task.question[: found.end] + f" {new_text}" + _rewrite_ids(task.question[found.end :], mapping)
    premises = []
    for premise in task.premises:
        start = question.find(premise.text)
        if start < 0:
            raise ValueError(f"premise {premise.premise_id} missing after source swap")
        premises.append(
            Premise(premise.premise_id, premise.text, start, start + len(premise.text), premise.value, premise.kind)
        )
    start = question.find(new_text)
    if start < 0:
        raise ValueError("alt source span missing from question")
    premises.append(Premise(new_id, new_text, start, start + len(new_text), value, found.kind))
    nodes = []
    for node in task.nodes:
        nodes.append(
            type(node)(
                id=node.id,
                parents=[mapping.get(parent, parent) for parent in node.parents],
                value=node.value,
                aliases=list(node.aliases),
                expression=_rewrite_ids(node.expression, mapping) if node.expression else node.expression,
                scope=node.scope,
            )
        )
    data = task.to_dict()
    new_task_id = f"{task.task_id}::src"
    data.update(
        {
            "task_id": new_task_id,
            "record_id": new_task_id,
            "variant_id": f"{task.variant_id}:src",
            "question": question,
            "premises": [p.__dict__ for p in premises],
            "nodes": [n.__dict__ for n in nodes],
        }
    )
    swapped = Task.from_dict(data)
    if _target_parents(swapped) == _target_parents(task):
        raise ValueError("same_value_diff_source must change required sources")
    if swapped.answer_spec.value != task.answer_spec.value:
        raise ValueError("same_value_diff_source must keep the target value")
    if premise_id not in {p.premise_id for p in swapped.premises} or new_id not in _target_parents(swapped):
        raise ValueError("same_value_diff_source must keep a and retarget to b")
    if premise_id in _target_parents(swapped):
        raise ValueError("same_value_diff_source must not still require a")
    return Edit(
        id=edit_id or f"edit:{task.task_id}:src:{premise_id}",
        base_task_id=task.task_id,
        changed_premise_ids=[new_id],
        task=swapped,
        kind="same_value_diff_source",
        before={premise_id: value},
        after={new_id: value},
        validity="valid",
        metadata={
            "values_unchanged": True,
            "same_value_diff_source": True,
            "same_source_diff_value": False,
            "required_sources_before": sorted(_target_parents(task)),
            "required_sources_after": sorted(_target_parents(swapped)),
        },
    )


def make_source_value_pair(task: Task, premise_id: str, new_literal: str) -> dict:
    value_edit = apply_value_edit(task, premise_id, new_literal)
    source_edit = apply_alt_source_same_value(task, premise_id)
    nontargets = [p.premise_id for p in task.premises if p.premise_id != premise_id]
    return {
        "same_source_diff_value": value_edit,
        "same_value_diff_source": source_edit,
        "targets": [task.target] if task.target else [],
        "nontargets": nontargets,
    }


def apply_source_value_edit(task: Task, premise_id: str, new_literal: str) -> Edit:
    pair = make_source_value_pair(task, premise_id, new_literal)
    edit = pair["same_source_diff_value"]
    edit.kind = "source_value"
    edit.metadata["source_value_decoupled"] = True
    edit.metadata["decoupled_pair"] = {
        "same_source_diff_value": True,
        "same_value_diff_source": True,
        "companion_edit": pair["same_value_diff_source"].id,
        "changed_premise": premise_id,
        "before": edit.before.get(premise_id),
        "after": new_literal,
        "targets": pair["targets"],
        "nontargets": pair["nontargets"],
    }
    return edit


def apply_operator_reverse(task: Task, node_id: str) -> Edit:
    flips = {"+": "-", "-": "+", "*": "/", "/": "*"}
    node = next((n for n in task.nodes if n.id == node_id), None)
    if node is None or not node.expression:
        raise ValueError(f"cannot reverse operator on {node_id}")
    expr = node.expression
    found = None
    for old, new in flips.items():
        if old in expr:
            found = (old, new)
            break
    if found is None:
        raise ValueError(f"no reversible operator in {expr!r}")
    new_expr = expr.replace(found[0], found[1], 1)
    nodes = []
    for item in task.nodes:
        nodes.append(
            type(item)(
                id=item.id,
                parents=list(item.parents),
                value=item.value,
                aliases=list(item.aliases),
                expression=new_expr if item.id == node_id else item.expression,
                scope=item.scope,
            )
        )
    if expr not in task.question and new_expr not in task.question:
        raise ValueError("no consistent text transformation for operator reverse")
    question = task.question.replace(expr, new_expr, 1) if expr in task.question else task.question
    data = task.to_dict()
    new_id = f"{task.task_id}::oprev:{node_id}"
    data.update({"task_id": new_id, "record_id": new_id, "nodes": [n.__dict__ for n in nodes], "question": question})
    recomputed = recompute(Task.from_dict(data))
    return Edit(
        id=f"edit:{task.task_id}:oprev:{node_id}",
        base_task_id=task.task_id,
        changed_premise_ids=list(node.parents),
        task=recomputed,
        kind="operator_reverse",
        before={node_id: expr},
        after={node_id: new_expr},
        validity="valid",
        metadata={"recomputed": True, "changed_input": True},
    )
