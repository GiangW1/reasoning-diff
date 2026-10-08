"""Registered quantity steps: a separate controlled generation condition."""
from __future__ import annotations

from collections import Counter
import re

from .graphs import ancestors
from .schema import Event, EventIdentity, Task, canonical_value

PROTOCOL = "quantity_steps_v1"
MATCHING_POLICY = "registered_quantity_steps_v1"
PHASE = "registered_quantity_step"
ESTIMAND = "one_committed_result_per_registered_quantity_step"
STEP = re.compile(r'<step\s+node=(?P<quote>["\'])(?P<node>[^"\'<>]+)(?P=quote)\s*>'
                  r'(?P<body>(?:(?!<step\b|</step>).)*?)</step>', re.S)
COMMIT = re.compile(r'(?P<reasoning>.*?)<commit>\s*(?P<value>[+-]?\d+)\s*</commit>\s*', re.S)


def is_controlled(task):
    return (getattr(task, "metadata", None) or {}).get("trajectory_protocol") == PROTOCOL


def controlled_task(task):
    if task.metadata.get("premise_protocol") != "sentence_graph_v1" or task.answer_spec.kind != "numeric" or not task.nodes:
        raise ValueError("quantity steps require numeric sentence-graph tasks with registered nodes")
    ancestors(task)  # The registered schedule must be topologically valid.
    plan = [{"node_id": n.id, "name": next((a for a in n.aliases if a != n.id), n.id)} for n in task.nodes]
    if is_controlled(task):
        if task.metadata.get("quantity_step_plan") != plan:
            raise ValueError("quantity step plan differs from the task nodes")
        return task
    return Task.from_dict({**task.to_dict(), "source_kind": "project_derived", "metadata": {
        **task.metadata, "trajectory_protocol": PROTOCOL, "quantity_step_plan": plan,
        "measurement_estimand": ESTIMAND, "parent_trajectory_condition": "natural"}})


def prompt_instructions(task):
    if not is_controlled(task):
        return ""
    plan = task.metadata["quantity_step_plan"]
    lines = "\n".join(f'{slot["node_id"]}: {slot["name"]}' for slot in plan)
    mod = task.answer_spec.mod
    arithmetic = f"Apply modulo {mod} after each arithmetic operation. " if mod else ""
    return ("\n\nThis run uses registered quantity steps. " + arithmetic
            + "During thinking, work through the quantities below in the listed order. "
            "For each quantity emit exactly one block <step node=\"NODE_ID\">your reasoning "
            "<commit>INTEGER</commit></step>. Use its exact listed NODE_ID. "
            "You may check or revise arithmetic inside the block before committing; "
            "commit exactly once, at the end of that block. The integer is your computed result, "
            "not an expression. Do not repeat a block or emit unlisted nodes. "
            "No answers or dependencies are supplied by this list.\n" + lines
            + "\nAfter finishing all blocks, close thinking naturally and give the requested "
            "answer with one \\boxed{number}. Do not emit step blocks in the answer section.")


def _blocks(text):
    result = []
    for step in STEP.finditer(text):
        commit = COMMIT.fullmatch(step.group("body"))
        if commit is not None and step.group("body").count("<commit>") == 1:
            result.append((step, commit))
    return result


def parse_steps(text, task):
    nodes = {n.id: n for n in task.nodes}
    planned = {slot["node_id"] for slot in task.metadata["quantity_step_plan"]}
    blocks = _blocks(text)
    counts = Counter(step.group("node") for step, _ in blocks)
    occurrences, events = Counter(), []
    graph = ancestors(task)
    for step, commit in blocks:
        nid = step.group("node")
        if nid not in planned or nid not in nodes:
            continue
        occurrences[nid] += 1
        value = canonical_value(commit.group("value"))
        node = nodes[nid]
        events.append(Event(EventIdentity(nid, occurrences[nid], node.scope), value, step.start(), step.end(),
                            step.start("body") + commit.start("value"), step.group(), sorted(graph[nid]),
                            canonical_value(node.value) == value if node.value is not None else None,
                            node_id=nid, graph_status=task.graph_status, status="ok" if counts[nid] == 1 else "ambiguous",
                            event_kind="commit", event_phase=PHASE, expression_signature=PROTOCOL,
                            source="registered_quantity_step"))
    return events


def format_report(text, task):
    """Full generated text only; partial continuation parsing is separate."""
    close = text.find("</think>")
    thinking, answer = (text[:close], text[close + len("</think>"):]) if close >= 0 else (text, "")
    plan = [slot["node_id"] for slot in task.metadata["quantity_step_plan"]]
    blocks = _blocks(thinking)
    ids = [step.group("node") for step, _ in blocks]
    counts = Counter(ids)
    issues = {
        "missing_nodes": [nid for nid in plan if counts[nid] == 0],
        "duplicate_nodes": sorted(nid for nid, count in counts.items() if count > 1),
        "unknown_nodes": sorted(set(ids) - set(plan)),
        "malformed_steps": max(len(re.findall(r"<step\b", thinking)), thinking.count("</step>")) - len(blocks),
        "uncontained_commits": max(len(re.findall(r"<commit\b", thinking)), thinking.count("</commit>")) - len(blocks),
        "answer_steps": len(re.findall(r"<step\b", answer)),
        "order_mismatch": [nid for nid in ids if nid in plan] != [nid for nid in plan if nid in ids],
    }
    return {"protocol": PROTOCOL, "passed": not any(issues.values()), "planned_steps": len(plan),
            "parsed_steps": len(blocks), **issues}


def align_steps(base, changed):
    for events in (base, changed):
        if len({e.identity.key() for e in events}) != len(events):
            raise ValueError("Duplicate event identities cannot be aligned")
    def unique(events):
        groups = {}
        for event in events:
            key = (event.node_id, event.identity.scope, event.event_region)
            groups.setdefault(key, []).append(event)
        return {key: values[0] for key, values in groups.items() if len(values) == 1 and values[0].status == "ok"
                and values[0].event_phase == PHASE and values[0].expression_signature == PROTOCOL}
    same_condition = all(e.event_phase == PHASE and e.expression_signature == PROTOCOL for e in base + changed)
    left, right = (unique(base), unique(changed)) if same_condition else ({}, {})
    pairs = [(left[key], right[key]) for key in left.keys() & right.keys()]
    pairs.sort(key=lambda pair: pair[0].start)
    matched_left, matched_right = {a.identity.key() for a, _ in pairs}, {b.identity.key() for _, b in pairs}
    removed = [e.identity.key() for e in base if e.identity.key() not in matched_left]
    added = [e.identity.key() for e in changed if e.identity.key() not in matched_right]
    return {"pairs": pairs, "removed": removed, "added": added, "unaligned": removed + added,
            "pair_certificates": [{"left": a.identity.key(), "right": b.identity.key(),
                                    "registered_node": a.node_id, "scope": a.identity.scope, "region": a.event_region,
                                    "semantic_unit": ESTIMAND} for a, b in pairs],
            "structural": {"disappeared": removed, "merged": [], "strategy_changed": [],
                           "ambiguous": [{"reason": "missing_or_duplicate_registered_step" if same_condition else "trajectory_condition_mismatch"}] if removed or added else [],
                           "detector": MATCHING_POLICY, "scanned": False}}


def trace_format(trace, task):
    """Recompute from generated text; never count the prompt's example tags."""
    prompt = (trace.get("metadata") or {}).get("rendered_prompt_text", "")
    text = trace.get("text", "")
    if prompt and not text.startswith(prompt):
        return {"protocol": PROTOCOL, "passed": False, "error": "rendered_prompt_mismatch"}
    return format_report(text[len(prompt):], task)
