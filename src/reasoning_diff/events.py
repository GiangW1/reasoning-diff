"""Event identity alignment; values never decide correspondence."""
from __future__ import annotations

from collections import Counter, defaultdict
import re

from .graphs import ancestors
from .schema import Event, EventIdentity, Task, canonical_value

NUMBER = r"[+-]?(?:\d[\d,]*(?:\.\d+)?(?:\s*/\s*[+-]?\d+)?|\.\d+)"


def surface_mentions(text: str, task: Task) -> list[str]:
    found = []
    for premise in task.premises:
        names = [premise.premise_id]
        for node in task.nodes:
            if node.id == premise.premise_id:
                names.extend(node.aliases)
        for name in names:
            if name and re.search(rf"(?<!\w){re.escape(str(name))}(?!\w)", text):
                found.append(premise.premise_id)
                break
    return sorted(set(found))


def _parse_assignments(text: str, task: Task, entities: list[tuple]) -> list[Event]:
    counts = Counter(alias.casefold() for alias, *_ in entities)
    found = []
    for alias, node_id, gold, scope, parents, graph_status in entities:
        if counts[alias.casefold()] != 1:
            continue
        value_pattern = NUMBER if task.answer_spec.kind == "numeric" else r"[^\n.;]+"
        pattern = re.compile(
            rf"(?<!\w){re.escape(alias)}\s*(?:=|:|equals?|is|are)\s*\$?(?P<value>{value_pattern})",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            start = match.start()
            end = match.end()
            found.append((start, end, match.start("value"), node_id, gold, scope, parents, graph_status, match.group("value")))
    found.sort(key=lambda item: (item[0], item[1]))
    line_counts = Counter(item[0] for item in found)
    occurrences: Counter = Counter()
    events = []
    for start, end, value_start, node_id, gold, scope, parents, graph_status, value in found:
        key = (node_id, scope)
        occurrences[key] += 1
        identity = EventIdentity(node_id, occurrences[key], scope)
        if parents is None and graph_status != "complete":
            parents_out = None
        else:
            parents_out = list(parents or [])
        status = "ok" if line_counts[start] == 1 else "ambiguous"
        events.append(
            Event(
                identity,
                canonical_value(value),
                start,
                end,
                value_start,
                text[start:end],
                parents_out,
                canonical_value(value) == canonical_value(gold) if gold is not None else None,
                surface_mentions=surface_mentions(text[start:end], task),
                node_id=node_id,
                graph_status=graph_status,
                status=status,
            )
        )
    return events


def parse_events(text: str, task: Task) -> list[Event]:
    """Premises and nodes. Used by scientific generate; values never decide identity."""
    entities = []
    seen_alias = Counter()
    for premise in task.premises:
        if premise.kind == "placeholder" or not premise.premise_id:
            continue
        seen_alias[premise.premise_id.casefold()] += 1
        entities.append((premise.premise_id, premise.premise_id, premise.value, "global", [premise.premise_id], task.graph_status))
    for node in task.nodes:
        for alias in node.aliases or [node.id]:
            seen_alias[alias.casefold()] += 1
            anc = ancestors(task).get(node.id, set())
            entities.append((alias, node.id, node.value, node.scope, sorted(anc), task.graph_status))
    return _parse_assignments(text, task, entities)


def parse_fixture_events(text: str, task: Task) -> list[Event]:
    aliases = [(alias, node) for node in task.nodes for alias in (node.aliases or [node.id])]
    counts = Counter(alias.casefold() for alias, _ in aliases)
    found = []
    for alias, node in aliases:
        if counts[alias.casefold()] != 1:
            continue
        value_pattern = NUMBER if task.answer_spec.kind == "numeric" else r"[^\n.;]+"
        pattern = re.compile(
            rf"(?<!\w){re.escape(alias)}\s*(?:=|:|equals?|is|are)\s*\$?(?P<value>{value_pattern})",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", start)
            end = len(text) if line_end < 0 else line_end
            found.append((start, end, match.start("value"), node, match.group("value")))
    found.sort(key=lambda item: (item[0], item[1]))
    line_counts = Counter(item[0] for item in found)
    occurrences: Counter = Counter()
    anc = ancestors(task) if task.nodes else {}
    events = []
    for start, end, value_start, node, value in found:
        key = (node.id, node.scope)
        occurrences[key] += 1
        identity = EventIdentity(node.id, occurrences[key], node.scope)
        parents = sorted(anc.get(node.id, set()))
        if not parents and task.graph_status != "complete":
            parents_out = None
        else:
            parents_out = parents
        status = "ok" if line_counts[start] == 1 else "ambiguous"
        events.append(
            Event(
                identity,
                canonical_value(value),
                start,
                end,
                value_start,
                text[start:end],
                parents_out,
                canonical_value(value) == canonical_value(node.value),
                surface_mentions=surface_mentions(text[start:end], task),
                node_id=node.id,
                graph_status=task.graph_status,
                status=status,
            )
        )
    return events


def align_events(base: list[Event], changed: list[Event]) -> dict:
    left_keys = [e.identity.key() for e in base]
    right_keys = [e.identity.key() for e in changed]
    if len(set(left_keys)) != len(base) or len(set(right_keys)) != len(changed):
        raise ValueError("Duplicate event identities cannot be aligned")

    def group(events: list[Event]) -> dict[tuple[str, str], list[Event]]:
        grouped: dict[tuple[str, str], list[Event]] = defaultdict(list)
        for event in events:
            grouped[(event.identity.entity_or_expression, event.identity.scope)].append(event)
        return grouped

    left = group(base)
    right = group(changed)
    pairs = []
    disappeared = []
    added = []
    ambiguous = []
    structural_merged = []
    for key in sorted(set(left) | set(right)):
        left_items = sorted(left.get(key, []), key=lambda e: e.identity.occurrence_version)
        right_items = sorted(right.get(key, []), key=lambda e: e.identity.occurrence_version)
        if len(left_items) == len(right_items) and all(
            a.node_id == b.node_id for a, b in zip(left_items, right_items, strict=True)
        ):
            pairs.extend(zip(left_items, right_items, strict=True))
        else:
            disappeared.extend(e.identity.key() for e in left_items)
            added.extend(e.identity.key() for e in right_items)
            if len(left_items) > 1 and len(right_items) == 1:
                merged = [e.identity.key() for e in left_items]
            elif len(left_items) == 1 and len(right_items) > 1:
                merged = [e.identity.key() for e in right_items]
            else:
                merged = []
            ambiguous.append({"entity": key[0], "scope": key[1], "left": len(left_items), "right": len(right_items)})
            structural_merged.extend(merged)
    return {
        "pairs": pairs,
        "removed": disappeared,
        "added": added,
        "unaligned": disappeared + added,
        "structural": {
            "disappeared": disappeared,
            "merged": structural_merged,
            "strategy_changed": [e.identity.key() for e in base + changed if e.status == "strategy_change"],
            "ambiguous": ambiguous,
            "detector": "occurrence_count",
            "strategy_detector": "status_field_only",
            "scanned": False,
        },
    }


def align_events_monotonic(base: list[Event], changed: list[Event]) -> dict:
    """Keep occurrence-count mismatches ambiguous. Do not rematch by renumbered versions."""
    grouped = align_events(base, changed)
    if grouped["structural"]["ambiguous"]:
        grouped["structural"] = {**grouped["structural"], "detector": "ambiguous_unresolved"}
    return grouped


def review_export(events: list[Event], task: Task | None = None) -> list[dict]:
    rows = []
    for event in events:
        rows.append(
            {
                "record_id": event.record_id,
                "run_id": event.run_id,
                "identity": event.identity.key() if isinstance(event.identity, EventIdentity) else None,
                "text": event.text,
                "value": event.value,
                "node_id": event.node_id,
                "task_id": None if task is None else task.task_id,
                "review": None,
                "review_status": "awaiting_human",
            }
        )
    return rows


def merge_review(rows: list[dict], reviews: list[dict]) -> list[dict]:
    by_id = {row["record_id"]: row for row in reviews if row.get("record_id")}
    merged = []
    for row in rows:
        rec = dict(row)
        extra = by_id.get(rec.get("record_id"))
        if extra is not None and extra.get("review") is not None:
            rec["review"] = extra["review"]
            rec["review_status"] = "filled"
        merged.append(rec)
    return merged


def boundary_index(offsets: list[list[int]], character: int, position: str = "before") -> int | None:
    """Last token fully before a boundary. Never include a straddling token."""
    if position not in ("before", "value", "end", "pre_step", "pre_value", "post_step"):
        raise ValueError("Unknown boundary position")
    limit = character
    candidates = [i for i, (a, b) in enumerate(offsets) if a < b and b <= limit]
    return candidates[-1] if candidates else None


def extract_answer(text: str, answer_kind: str) -> str | None:
    if "<think>" in text and "</think>" not in text:
        return None
    text = re.sub(r"<think>.*?</think>", " ", text, flags=re.S)
    if answer_kind == "code":
        matches = re.findall(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
        return matches[-1].strip() if matches else text.strip() or None
    matches = re.findall(r"\\boxed\{([^{}]+)\}", text)
    if matches:
        return canonical_value(matches[-1])
    matches = re.findall(r"####\s*([^\n]+)", text)
    if matches:
        return canonical_value(matches[-1])
    if answer_kind in {"span", "text", "short"}:
        labeled = re.search(r"(?:the answer is|answer:)\s*(.+?)(?:[.!?]|$)", text, flags=re.I)
        if labeled:
            return canonical_value(labeled.group(1))
        stripped = text.strip()
        return canonical_value(stripped) if stripped else None
    numbers = re.findall(NUMBER, text)
    return canonical_value(numbers[-1]) if numbers else None


def normalize_answer(value: str | None, answer_kind: str) -> str | None:
    """Normalize a predicted or gold answer with the same task-kind rules."""
    if value is None:
        return None
    normalized = canonical_value(value)
    if answer_kind == "code":
        return normalized.strip()
    if answer_kind in {"span", "text", "short"}:
        normalized = re.sub(r"[^\w\s]", " ", normalized, flags=re.UNICODE)
        normalized = " ".join(normalized.casefold().split())
    return normalized


def answers_equal(predicted: str | None, gold: str | None, answer_kind: str) -> bool | None:
    pred = normalize_answer(predicted, answer_kind)
    target = normalize_answer(gold, answer_kind)
    return None if pred is None or target is None else pred == target
