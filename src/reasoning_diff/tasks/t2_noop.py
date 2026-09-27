"""Project-derived no-op pairs. Not an official GSM-NoOp release."""
from __future__ import annotations

import re

from ..edits import recompute
from ..graphs import ancestors
from ..schema import Task


def _sentence_insert_at(question: str, position: str) -> int:
    if position == "front":
        return 0
    if position == "back":
        return len(question)
    bounds = [match.end() for match in re.finditer(r"[.!?]\s+", question)]
    mid = max(1, len(question) // 2)
    if bounds:
        return min(bounds, key=lambda idx: abs(idx - mid))
    left = question.rfind(" ", 0, mid)
    right = question.find(" ", mid)
    if left >= 0:
        return left + 1
    if right >= 0:
        return right + 1
    raise ValueError("no sentence or word boundary for mid no-op")


def _locate_original(question: str, premise_text: str, prefer_from: int) -> int:
    loc = question.find(premise_text, prefer_from)
    if loc >= 0:
        return loc
    raise ValueError("base premise text missing after no-op injection")


def make_noop_pair(base: Task, sentence: str, position: str, surface: str, independent_non_ancestor: bool) -> Task:
    if position not in {"front", "mid", "back"}:
        raise ValueError("noop position must be front/mid/back")
    if surface not in {"low", "medium", "high"}:
        raise ValueError("surface relatedness must be stratified")
    if not independent_non_ancestor:
        raise ValueError("no-op requires an independent non-ancestor judgment")
    anc = ancestors(base) if base.nodes else {}
    target_anc = anc.get(base.target or "", set())
    q = base.question
    at = _sentence_insert_at(q, position)
    left, right = q[:at], q[at:]
    if position == "front":
        question = sentence + " " + q
        shift = len(sentence) + 1
    elif position == "back":
        question = q + " " + sentence
        shift = 0
    else:
        question = (left.rstrip() + " " + sentence + " " + right.lstrip()).strip()
        if left.rstrip() not in question or right.lstrip() not in question:
            raise ValueError("noop insertion would corrupt original question")
        shift = 0
    mid = at
    data = base.to_dict()
    data.update(
        {
            "task_id": f"{base.task_id}::noop",
            "variant_id": f"{base.variant_id}:noop:{position}:{surface}",
            "source": "reasoning_diff_noop",
            "source_kind": "project_derived",
            "question": question,
            "graph_status": base.graph_status if base.graph_status != "complete" else "complete",
            "metadata": {
                **base.metadata,
                "noop_position": position,
                "surface_relatedness": surface,
                "official_noop_release": False,
                "injected_non_ancestor": True,
            },
        }
    )
    remapped = []
    for p in base.premises:
        if position == "front":
            prefer = p.start + shift
        elif position == "mid" and p.start >= mid:
            prefer = mid + len(sentence) + 2
        else:
            prefer = p.start
        loc = _locate_original(question, p.text, prefer)
        remapped.append(
            {
                "premise_id": p.premise_id,
                "text": p.text,
                "start": loc,
                "end": loc + len(p.text),
                "value": p.value,
                "kind": p.kind,
            }
        )
    if position == "front":
        start = 0
    elif position == "back":
        start = question.rfind(sentence)
    else:
        start = question.find(sentence, mid)
    remapped.append(
        {"premise_id": "noop", "text": sentence, "start": start, "end": start + len(sentence), "value": None, "kind": "fact"}
    )
    data["premises"] = remapped
    data["answer_spec"] = base.answer_spec.__dict__ if not isinstance(base.answer_spec, dict) else base.answer_spec
    pair = Task.from_dict(data)
    after_anc = ancestors(pair) if pair.nodes else {}
    target_after = after_anc.get(pair.target or "", set())
    if "noop" in target_after:
        raise ValueError("injected sentence is an ancestor of the target")
    if pair.nodes:
        proven = recompute(pair)
        if proven.answer_spec.value != base.answer_spec.value:
            raise ValueError("no-op changed the recomputed answer")
        pair.metadata["answer_unchanged_proven"] = True
        pair.metadata["injected_non_ancestor"] = True
        pair.metadata["noop_proof"] = "recompute_and_ancestors"
    else:
        pair.metadata["answer_unchanged_proven"] = False
        pair.metadata["injected_non_ancestor"] = None
        pair.metadata["noop_proof"] = "unknown_without_graph"
    return pair
