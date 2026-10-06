"""Event identity alignment; values never decide correspondence."""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
from fractions import Fraction
import re

from .graphs import ancestors
from .schema import Event, EventIdentity, Task, canonical_value

NUMBER = r"[+-]?(?:\d[\d,]*(?:\.\d+)?(?:\s*/\s*[+-]?\d+)?|\.\d+)"


def _entity_name(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"'s\b", "", name.casefold())).strip()


def premise_aliases(premise) -> list[str]:
    aliases = [str(premise.premise_id)] if getattr(premise, "premise_id", None) else []
    match = re.search(r"The number of (?:each )?(.+?) (?:equals?|is|are)\b", str(getattr(premise, "text", "")), re.IGNORECASE)
    if match:
        aliases.append(match.group(1))
    return aliases


def surface_mentions(text: str, task: Task) -> list[str]:
    found = []
    for premise in task.premises:
        names = premise_aliases(premise)
        for node in task.nodes:
            if node.id == premise.premise_id:
                names.extend(node.aliases)
        for name in names:
            if name and re.search(rf"(?<!\w){re.escape(str(name))}(?!\w)", text):
                found.append(premise.premise_id)
                break
    return sorted(set(found))


def _declared_aliases(text: str, entities: list[tuple]) -> dict[str, tuple]:
    """Resolve explicit variable declarations under an unambiguous entity heading."""
    names = defaultdict(dict)
    for entity in entities:
        alias, node_id, *_ = entity
        names[_entity_name(alias)][node_id] = entity
    scopes = {entity[0].rsplit("'s ", 1)[0].casefold() for entity in entities if "'s " in entity[0]}
    symbol = r"(?:[A-Za-z]_\{[A-Za-z0-9]+\}|[A-Za-z][A-Za-z0-9_]*)"
    declaration = re.compile(
        r"^\s*[-*]\s+(?P<name>.+?)\s*(?:"
        r"\((?:(?:let's\s+)?denote this as\s+)?(?P<paren>" + symbol + r")\)"
        r"|:\s*(?:(?:let's\s+)?denote this as\s+)?(?P<colon>" + symbol + r"))\s*(?:=.+)?\s*$",
        re.IGNORECASE,
    )
    reverse = re.compile(r"^\s*[-*]\s*(?:Let\s+)?(?P<symbol>" + symbol
                         + r")\s*=\s*(?:the\s+)?number of\s+(?P<name>.+?)\.?\s*$", re.IGNORECASE)
    full_names = sorted({re.escape(entity[0]).replace("'s", "(?:'s)?") for entity in entities}, key=len, reverse=True)
    inline = re.compile(r"(?<!\w)(?P<name>" + "|".join(full_names) + r")\s*\((?P<paren>" + symbol
                        + r")\)\s*(?==|[.,;]|$)", re.IGNORECASE) if full_names else None
    name_pattern = "|".join(full_names)
    reverse_entity = re.compile(r"^\s*[-*]\s*(?:Let\s+)?(?P<symbol>" + symbol
                                + r")\s*=\s*(?P<name>" + name_pattern + r")\s*\.?\s*$", re.IGNORECASE) if full_names else None
    prose = [re.compile(pattern, re.IGNORECASE) for pattern in (
        r"\blet\s+(?:me\s+)?denote\s+(?:the number of\s+)?(?P<name>" + name_pattern + r")\s+as\s+(?P<symbol>" + symbol + r")(?!\w)",
        r"\blet\s+(?P<symbol>" + symbol + r")\s+be\s+(?:the number of\s+)?(?P<name>" + name_pattern + r")(?!\w)",
        r"\blet\s+(?:me\s+)?denote\s+(?P<symbol>" + symbol + r")\s+as\s+(?:the number of\s+)?(?P<name>" + name_pattern + r")(?!\w)",
    )] if full_names else []
    subject = re.compile(r"\b(?:the\s+)?number of\s+(?P<name>" + name_pattern + r")\s*(?:equals?\b|=|is\b)", re.IGNORECASE) if full_names else None
    adjacent = re.compile(r"\b(?:so|then|therefore),?\s+(?:let(?:'s| us| me)?\s+denote this as\s+)?(?P<symbol>" + symbol + r")\s*=", re.IGNORECASE)
    pronoun = re.compile(r"\blet(?:'s| me| us)?\s+denote this as\s+(?P<symbol>" + symbol + r")(?!\w)", re.IGNORECASE)
    scope, offset, declared = None, 0, {}
    for line in text.splitlines(keepends=True):
        heading = re.fullmatch(r"(?:For\s+)?(.+?):", line.strip().strip("*"), re.IGNORECASE)
        if heading:
            candidate = heading.group(1).strip().casefold()
            scope = candidate if candidate in scopes else None
        match = (declaration.fullmatch(line.rstrip("\r\n")) or reverse.fullmatch(line.rstrip("\r\n"))
                 or (reverse_entity.fullmatch(line.rstrip("\r\n")) if reverse_entity else None))
        matches = ([match] if match else []) + (list(inline.finditer(line)) if inline else [])
        matches.extend(match for pattern in prose for match in pattern.finditer(line))
        # A same-line, explicit sentence subject may introduce a notation in
        # the following clause. Never infer an entity from its numeric value.
        subjects = list(subject.finditer(line)) if subject else []
        for notation in [*adjacent.finditer(line), *pronoun.finditer(line)]:
            prior_subjects = [m for m in subjects if m.end() <= notation.start()]
            if prior_subjects:
                owner = prior_subjects[-1]
                name = _entity_name(owner.group("name"))
                candidates = names.get(name, {})
                if len(candidates) == 1:
                    alias = notation.group("symbol")
                    entity = next(iter(candidates.values()))
                    key = alias.casefold()
                    position = offset + notation.start("symbol")
                    if key not in declared:
                        declared[key] = ((alias, *entity[1:]), position)
                    elif declared[key] is not None and declared[key][0][1] != entity[1]:
                        declared[key] = None
        for match in matches:
            name = _entity_name(match.group("name").strip().strip("*`$"))
            candidates = names.get(name)
            if not candidates and scope:
                candidates = names.get(_entity_name(f"{scope}'s {name}"))
            if candidates and len(candidates) == 1:
                entity = next(iter(candidates.values()))
                group, alias = next((key, value) for key, value in match.groupdict().items() if key != "name" and value)
                key = alias.casefold()
                prior = declared.get(key)
                if key not in declared:
                    declared[key] = ((alias, *entity[1:]), offset + match.start(group))
                elif prior is not None and prior[0][1] != entity[1]:
                    declared[key] = None
        offset += len(line)
    return {key: value for key, value in declared.items() if value is not None}


def _expression_tree(expression: str, entities: list[tuple]):
    """Validate printed arithmetic and derive a value-blind structural key."""
    expression = expression.strip().strip("$")
    expression = re.sub(r"([A-Za-z])_\{([A-Za-z0-9]+)\}", r"\1_\2", expression)
    expression = expression.replace(r"\times", "*").replace(r"\cdot", "*").replace(r"\div", "/")
    expression = expression.translate(str.maketrans({"×": "*", "÷": "/", "−": "-", "^": "**"}))
    expression = re.sub(r"\s*(?:\\?mod\b|modulo\b)\s*", " % ", expression, flags=re.IGNORECASE)
    names = defaultdict(set)
    for alias, node_id, *_ in entities:
        names[alias.casefold()].add(node_id)
    symbols = {}
    for index, alias in enumerate(sorted(names, key=len, reverse=True)):
        if len(names[alias]) != 1:
            continue
        symbol = f"entity_{index}"
        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
        expression = re.sub(pattern, symbol, expression, flags=re.IGNORECASE)
        symbols[symbol] = next(iter(names[alias]))
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError):
        return None
    allowed = (ast.Expression, ast.Name, ast.Load, ast.Constant, ast.BinOp, ast.UnaryOp,
               ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.UAdd, ast.USub)
    if any(not isinstance(node, allowed) or (isinstance(node, ast.Constant) and type(node.value) not in (int, float))
           for node in ast.walk(tree)):
        return None
    phase = "reduction" if any(isinstance(node, ast.Mod) for node in ast.walk(tree)) else (
        "calculation" if isinstance(tree.body, ast.BinOp) else "copy" if isinstance(tree.body, ast.Name) else "commit")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            node.value = "number"
        elif isinstance(node, ast.Name):
            node.id = symbols.get(node.id, "unresolved:" + node.id.casefold())
    return phase, ast.dump(tree, include_attributes=False)


def _numeric_commit(text: str, start: int, entities: list[tuple]):
    """Accept a terminal printed scalar, never evaluate an unfinished RHS."""
    line_end = text.find("\n", start)
    line_end = len(text) if line_end < 0 else line_end
    rhs = text[start:line_end]
    number = re.compile(NUMBER)
    for result in number.finditer(rhs):
        prefix = rhs[:result.start()].strip().strip("$").strip()
        scalar = prefix == "" or re.fullmatch(r"\(*\s*", prefix)
        if not scalar and not prefix.endswith("="):
            continue
        suffix = rhs[result.end():]
        # A close parenthesis or a LaTeX marker cannot hide pending math.
        rest = re.sub(r"^(?:\s*[)$])*\s*", "", suffix)
        mod = re.match(r"(?P<open>\()?\s*(?:\\?mod\b|modulo\b)\s*(?P<modulus>" + NUMBER + r")\s*(?(open)\))", rest, re.IGNORECASE)
        if mod:
            # "x = 3 mod 23" can annotate an explicitly printed residue.
            # "x = 25 mod 23" has not printed its reduced result: do not
            # evaluate it or record the pending reduction as a scalar commit.
            try:
                value = Fraction(result.group().replace(",", "").replace(" ", ""))
                modulus = Fraction(mod.group("modulus").replace(",", "").replace(" ", ""))
            except (ValueError, ZeroDivisionError):
                continue
            if not 0 <= value < modulus:
                continue
            rest = rest[mod.end():].lstrip()
        annotation = re.match(r"\((?:given|as given|from (?:the )?problem)\)", rest, re.IGNORECASE)
        if annotation:
            rest = rest[annotation.end():].lstrip()
        if rest and not re.match(r"[.,;?!]|</", rest):
            continue
        expressions = [] if scalar else prefix[:-1].split("=")
        trees = [_expression_tree(expr, entities) for expr in expressions]
        if any(tree is None for tree in trees):
            continue
        phase, signature = trees[0] if trees else ("commit", "scalar")
        if any(tree[0] == "reduction" for tree in trees):
            phase = "reduction"
        kind = "calculation" if any(tree[0] in {"calculation", "reduction"} for tree in trees) else "commit"
        return start + result.start(), start + result.end(), result.group(), kind, phase, signature
    return None


def _parse_assignments(text: str, task: Task, entities: list[tuple]) -> list[Event]:
    declarations = _declared_aliases(text, entities)
    registered = {(e[0].casefold(), e[1]) for e in entities}
    entities = [*entities, *[entity for entity, _ in declarations.values() if (entity[0].casefold(), entity[1]) not in registered]]
    counts = Counter(alias.casefold() for alias, *_ in entities)
    found = []
    for alias, node_id, gold, scope, parents, graph_status in entities:
        if counts[alias.casefold()] != 1:
            continue
        closing = r"\s*\)?" if alias.casefold() in declarations else ""
        pattern = re.compile(
            rf"(?<!\w){re.escape(alias)}{closing}\s*(?:=|:|equals?\b|is\b|are\b)\s*",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            declared = declarations.get(alias.casefold())
            if declared is not None and (alias.casefold(), node_id) not in registered and match.start() < declared[1]:
                continue
            start = match.start()
            # An entity mentioned inside another assignment's RHS is not a
            # new assignment head (e.g. q = p1 and p2 = 3).
            preceding = text[max(text.rfind("\n", 0, start), text.rfind(";", 0, start)) + 1:start]
            preceding = re.split(r"\.(?!\d)|,\s+(?=[A-Za-z])", preceding)[-1]
            if "=" in preceding:
                continue
            if re.search(r"(?:\b(?:and|plus|minus|times|add|subtract|multiply|divide)|[+*/−-])\s*$", preceding, re.IGNORECASE):
                continue
            kind = "restatement" if any(p.premise_id == node_id for p in task.premises) else "commit"
            if task.answer_spec.kind == "numeric":
                visible_entities = [entity for entity in entities if entity[0].casefold() not in declarations
                                    or declarations[entity[0].casefold()][1] <= start
                                    or (entity[0].casefold(), entity[1]) in registered]
                result = _numeric_commit(text, match.end(), visible_entities)
                if result is None:
                    continue
                value_start, end, value, parsed_kind, phase, signature = result
                if kind != "restatement":
                    kind = parsed_kind
            else:
                result = re.match(r"[^\n.;]+", text[match.end():])
                if result is None:
                    continue
                value_start, end, value = match.end(), match.end() + result.end(), result.group()
                phase, signature = "commit", "text"
            found.append((start, end, value_start, node_id, gold, scope, parents, graph_status, value, kind, phase, signature))
    found.sort(key=lambda item: (item[0], item[1]))
    line_counts = Counter(item[0] for item in found)
    occurrences: Counter = Counter()
    events = []
    for start, end, value_start, node_id, gold, scope, parents, graph_status, value, kind, phase, signature in found:
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
                event_kind=kind,
                event_phase=phase,
                expression_signature=signature,
            )
        )
    return events


def parse_events(text: str, task: Task) -> list[Event]:
    """Premises and nodes. Used by scientific generate; values never decide identity."""
    entities = []
    seen_alias = Counter()
    for premise in task.premises:
        if premise.kind in {"placeholder", "relation"} or not premise.premise_id:
            continue
        for alias in premise_aliases(premise):
            seen_alias[alias.casefold()] += 1
            entities.append((alias, premise.premise_id, premise.value, "global", [premise.premise_id], task.graph_status))
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

    def group(events: list[Event]) -> dict[tuple, list[Event]]:
        grouped = defaultdict(list)
        for event in events:
            key = (event.identity.entity_or_expression, event.identity.scope, event.event_region,
                   event.event_kind if event.expression_signature else "legacy",
                   event.event_phase, event.expression_signature)
            grouped[key].append(event)
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
        # Parsed scientific events need a unique value-blind phase/structure
        # anchor. Repeated indistinguishable confirmations are unresolved,
        # even when counts happen to agree. Legacy fixture identities retain
        # their explicitly enumerated occurrence correspondence.
        unique = not key[-1] or len(left_items) == len(right_items) == 1
        if unique and len(left_items) == len(right_items) and all(
            a.node_id == b.node_id for a, b in zip(left_items, right_items, strict=True)
        ) and all(e.status == "ok" for e in left_items + right_items):
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
            ambiguous.append({"entity": key[0], "scope": key[1], "region": key[2], "phase": key[4],
                              "left": len(left_items), "right": len(right_items),
                              "reason": "repeated_anchor" if not unique else "missing_or_incompatible_anchor"})
            structural_merged.extend(merged)
    # A reordered sequence of anchors inside one entity does not establish
    # corresponding computation stages. Keep those pairs unknown as well.
    anchored = defaultdict(list)
    for a, b in pairs:
        anchored[(a.identity.entity_or_expression, a.identity.scope, a.event_region)].append((a, b))
    pairs = []
    for key, items in anchored.items():
        items.sort(key=lambda pair: pair[0].identity.occurrence_version)
        versions = [b.identity.occurrence_version for _, b in items]
        if versions != sorted(versions):
            disappeared.extend(a.identity.key() for a, _ in items)
            added.extend(b.identity.key() for _, b in items)
            ambiguous.append({"entity": key[0], "scope": key[1], "region": key[2], "reason": "reordered_anchors"})
        else:
            pairs.extend(items)
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
            "detector": "region_phase_unique_structure_v2",
            "strategy_detector": "status_field_only",
            "scanned": False,
        },
    }


def align_events_monotonic(base: list[Event], changed: list[Event]) -> dict:
    """Keep repeated or reordered phase/structure anchors unresolved."""
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
                "event_region": event.event_region,
                "event_status": event.status,
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


def assign_event_regions(
    events: list[Event],
    text: str,
    *,
    finalizer_start: int | None = None,
    initial_thinking: bool = False,
) -> list[Event]:
    """Annotate events by the generation region that produced them.

    The parser intentionally remains region agnostic.  Generation owns the
    boundary because it knows whether the text contains a natural ``</think>``
    transition or a legacy finalizer.  Returning the same objects keeps this
    helper usable by both frozen and tiny backends.
    """
    close = text.find("</think>")
    answer_start = close + len("</think>") if close >= 0 else None
    for event in events:
        if finalizer_start is not None and event.start >= finalizer_start:
            event.event_region = "post_finalizer"
        elif answer_start is not None and event.start >= answer_start:
            event.event_region = "answer"
        else:
            # Tiny fixtures have no chat-template thinking marker.  Their
            # generated assignments are answer-region text; callers that need
            # a C1 feature can explicitly treat ``unknown`` as legacy data.
            event.event_region = "thinking" if answer_start is not None or initial_thinking else "answer"
    return events


def extract_answer_with_status(text: str, answer_kind: str) -> tuple[str | None, str]:
    """Extract an answer and preserve how it was obtained.

    Numeric fallback is retained for legacy data but is explicitly marked so
    it cannot be silently treated as a boxed or structured answer.
    """
    if "<think>" in text and "</think>" not in text:
        return None, "missing_think_close"
    text = re.sub(r"<think>.*?</think>", " ", text, flags=re.S)
    if answer_kind == "code":
        matches = re.findall(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
        return (matches[-1].strip(), "code_block") if matches else ((text.strip() or None), "code_text")
    matches = re.findall(r"\\boxed\{([^{}]+)\}", text)
    if matches:
        return canonical_value(matches[-1]), "boxed"
    matches = re.findall(r"####\s*([^\n]+)", text)
    if matches:
        return canonical_value(matches[-1]), "hash_delimited"
    if answer_kind in {"span", "text", "short"}:
        labeled = re.search(r"(?:the answer is|answer:)\s*(.+?)(?:[.!?]|$)", text, flags=re.I)
        if labeled:
            return canonical_value(labeled.group(1)), "labeled"
        stripped = text.strip()
        return (canonical_value(stripped), "text_fallback") if stripped else (None, "missing")
    numbers = re.findall(NUMBER, text)
    return (canonical_value(numbers[-1]), "numeric_fallback") if numbers else (None, "missing")


def extract_answer(text: str, answer_kind: str) -> str | None:
    return extract_answer_with_status(text, answer_kind)[0]


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
