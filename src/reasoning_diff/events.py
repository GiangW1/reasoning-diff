"""Event identity alignment; values never decide correspondence."""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
import hashlib
import re

from .graphs import ancestors
from .schema import Event, EventIdentity, Task, canonical_value

NUMBER = r"[+-]?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s*/\s*[+-]?\d+)?|\.\d+)"
ALIGNMENT_POLICY = "printed_expression_views_forced_sequence_v9"


def context_entity_token(node_id):
    """A stable alphabetic identity, unaffected by masking numeric literals."""
    return 'entity' + hashlib.sha256(node_id.encode()).hexdigest().translate(str.maketrans('0123456789', 'ghijklmnop'))


@lru_cache(maxsize=8192)
def expression_key(signature):
    """Read ast.dump as data, including after a registered C2 source rename."""
    def read(node):
        if isinstance(node, ast.Constant):
            return node.value
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.args:
            raise ValueError("unsupported expression signature")
        name = node.func.id
        fields = {kw.arg: read(kw.value) for kw in node.keywords}
        if name == "Expression":
            return fields["body"]
        if name == "BinOp" and fields["op"] in (("Add", ()), ("Mult", ())):
            op = fields["op"][0]
            def terms(child):
                return list(child[1]) if isinstance(child, tuple) and child[0] == op else [child]
            return op, tuple(sorted(terms(fields["left"]) + terms(fields["right"]), key=repr))
        return name, tuple(sorted(fields.items()))
    try:
        return read(ast.parse(signature, mode="eval").body)
    except (SyntaxError, ValueError, KeyError):
        return "literal", signature


def _entity_name(name: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"'s\b", "", name.casefold())).strip()


def _abbreviates(symbol: str, name: str) -> bool:
    """Lexical initials/full words only; no values or task-DAG expressions."""
    parts = re.findall(r"[A-Z]+(?=[A-Z][a-z]|_|$)|[A-Z]?[a-z]+|[0-9]+", symbol)
    expanded_name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    words = re.findall(r"[a-z]+|[0-9]+", _entity_name(expanded_name))
    if not parts or len("".join(parts)) < 2 or not words:
        return False
    positions = {0}
    for part_index, part in enumerate(map(str.casefold, parts)):
        following = set()
        starts = positions if part_index == 0 else {start for position in positions for start in range(position, len(words))}
        for start in starts:
            if start < len(words) and (part == words[start] or len(part) >= 2 and words[start].startswith(part)):
                following.add(start + 1)
            for end in range(start + 1, len(words) + 1):
                if part == "".join(w[0] for w in words[start:end]):
                    following.add(end)
        positions = following
    # A unique named prefix such as Starfish_Nasal may omit "Cavity".
    return len(words) in positions or any(i >= 2 for i in positions)


def _topic_alias_matches(symbol, name):
    if _abbreviates(symbol, name):
        return True
    local_name = name.rsplit("'s ", 1)[-1]
    if _abbreviates(symbol, local_name):
        return True
    # An explicit named topic can introduce quantity-first initials (Cvas
    # for Asia Supermarket's Canned Vegetables), including omitted words.
    # This is context-scoped, never a global alias guess.
    letters = symbol.replace('_', '').casefold()
    initials = Counter(word[0] for word in re.findall(r'[a-z]+', _entity_name(name)))
    if len(letters) >= 2 and letters.isalpha() and not (Counter(letters) - initials):
        return True
    return len(symbol) == 1 and bool(local_name) and symbol.casefold() == local_name[0].casefold()


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
    symbol = r"(?:[A-Za-z]_\{[A-Za-z0-9]+\}|[A-Za-z][A-Za-z0-9_]*['′]?)"
    # Only an explicit parenthesis can introduce a multiword shorthand.
    # Do not extend free prose/heading guesses to arbitrary word sequences.
    paren_symbol = symbol + r"(?:[ \t]+" + symbol + r"){0,2}"
    declaration = re.compile(
        r"^\s*(?:[-*]\s+)?(?P<name>.+?)\s*(?:"
        r"\((?:(?:let's\s+)?denote this as\s+)?(?P<paren>" + paren_symbol + r")\)"
        r"|:\s*(?:(?:let's\s+)?(?:denote this as|call this)\s+)?(?P<colon>" + symbol + r"))\s*(?:=.+)?\s*$",
        re.IGNORECASE,
    )
    reverse = re.compile(r"^\s*[-*]\s*(?:Let\s+)?(?P<symbol>" + symbol
                         + r")\s*=\s*(?:the\s+)?number of\s+(?P<name>.+?)\.?\s*$", re.IGNORECASE)
    full_names = sorted({re.escape(entity[0]).replace("'s", "(?:'s)?") for entity in entities}, key=len, reverse=True)
    inline = re.compile(r"(?<!\w)(?P<name>" + "|".join(full_names) + r")\s*\("
                        r"(?:(?:[^()\n]*?\b)?let(?:'s| me| us)?\s+(?:denote|call)\s+(?:this|it)\s+(?:as\s+)?)?"
                        r"(?P<paren>" + paren_symbol + r")\)\s*(?==|equals?\b|is\b|[.,;]|$)",
                        re.IGNORECASE) if full_names else None
    name_pattern = "|".join(full_names)
    human_names = "|".join(re.escape(alias).replace("'s", "(?:'s)?") for alias, node_id, *_ in entities if alias != node_id)
    reverse_entity = re.compile(r"^\s*(?:[-*]\s+)?(?:Let\s+)?(?P<symbol>" + symbol
                                + r")\s*=\s*(?:(?:the\s+)?number of\s+)?(?P<name>" + human_names
                                + r")(?:\.?\s*$|\s*(?==))", re.IGNORECASE) if human_names else None
    prose = [re.compile(pattern, re.IGNORECASE) for pattern in (
        r"\blet\s+(?:me\s+)?denote\s+(?:the number of\s+)?(?P<name>" + name_pattern + r")\s+as\s+(?P<symbol>" + symbol + r")(?!\w)",
        r"\blet\s+(?P<symbol>" + symbol + r")\s+be\s+(?:the number of\s+)?(?P<name>" + name_pattern + r")(?!\w)",
        r"\blet\s+(?:me\s+)?denote\s+(?P<symbol>" + symbol + r")\s+as\s+(?:the number of\s+)?(?P<name>" + name_pattern + r")(?!\w)",
    )] if full_names else []
    subject = re.compile(r"\b(?:the\s+)?number of\s+(?P<name>" + name_pattern + r")\s*(?:equals?\b|=|is\b)", re.IGNORECASE) if full_names else None
    adjacent = re.compile(r"\b(?:so|then|therefore),?\s+(?:let(?:'s| us| me)?\s+denote this as\s+)?(?P<symbol>" + symbol + r")\s*=", re.IGNORECASE)
    pronoun = re.compile(r"\blet(?:'s| me| us)?\s+denote this as\s+(?P<symbol>" + symbol + r")(?!\w)", re.IGNORECASE)
    scope, offset, declared, priorities = None, 0, {}, {}
    def register(alias, entity, position, priority=2):
        key = alias.casefold()
        prior = declared.get(key)
        if key not in declared or priority > priorities[key]:
            if prior is not None and prior[0][1] == entity[1]:
                position = min(position, prior[1])
            declared[key] = ((alias, *entity[1:]), position)
            priorities[key] = priority
        elif prior is not None:
            # Detectors visit lines and cross-line declarations separately;
            # discovery order must not replace the earliest printed binding.
            if prior[0][1] == entity[1]:
                declared[key] = ((alias, *entity[1:]), min(position, prior[1]))
            elif priority == priorities[key]:
                declared[key] = None

    for line in text.splitlines(keepends=True):
        heading = re.fullmatch(r"(?:For\s+)?(.+?):", line.strip().strip("*"), re.IGNORECASE)
        if heading:
            candidate = heading.group(1).strip().casefold()
            scope = candidate if candidate in scopes else None
        match = (declaration.fullmatch(line.rstrip("\r\n"))
                 or (reverse_entity.match(line.rstrip("\r\n")) if reverse_entity else None)
                 or reverse.fullmatch(line.rstrip("\r\n")))
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
                    explicit = bool(re.search(r"\bdenote\b", notation.group(), re.I))
                    if not explicit and not _topic_alias_matches(alias, entity[0]):
                        continue
                    position = offset + notation.start("symbol")
                    register(alias, entity, position, priority=2 if explicit else 0)
        for match in matches:
            name = _entity_name(match.group("name").strip().strip("*`$"))
            candidates = names.get(name)
            if not candidates and scope:
                candidates = names.get(_entity_name(f"{scope}'s {name}"))
            if candidates and len(candidates) == 1:
                entity = next(iter(candidates.values()))
                group, alias = next((key, value) for key, value in match.groupdict().items() if key != "name" and value)
                register(alias, entity, offset + match.start(group))
        offset += len(line)
    # An explicit "write/denote that as:" or "So:" may introduce a
    # notation on the next line. Its named subject must be in the same
    # paragraph as the introducer; do not inherit topics across narration.
    topics = re.compile(r"(?P<name>" + human_names + r")\s*(?:equals?\b|=|is\b)", re.IGNORECASE) if human_names else None
    introduction = re.compile(r"\b(?:let(?:'s| me| us)?\s+(?:denote|write|note)\s+(?:that|this)\s+as"
                              r"|so|then|therefore)\s*[:,]?\s*(?:[-*+•][ \t]+)?(?P<symbol>" + symbol + r")\s*=", re.IGNORECASE)
    topic_matches = list(topics.finditer(text)) if topics else []
    for notation in introduction.finditer(text):
        owners = [match for match in topic_matches if match.end() <= notation.start()]
        if not owners:
            continue
        owner = owners[-1]
        if "\n\n" in text[owner.end():notation.start()]:
            continue
        # A named entity on another assignment's RHS is not a new topic.
        before = text[text.rfind("\n", 0, owner.start()) + 1:owner.start()]
        if "=" in re.split(r"\.(?!\d)|;", before)[-1]:
            continue
        candidates = names.get(_entity_name(owner.group("name")), {})
        if len(candidates) != 1:
            continue
        alias = notation.group("symbol")
        explicit = bool(re.match(r"let\b|let's\b", notation.group(), re.I))
        if not explicit and not _topic_alias_matches(alias, owner.group("name")):
            continue
        register(alias, next(iter(candidates.values())), notation.start("symbol"), priority=2 if explicit else 0)
    # Recognize unambiguous conventional abbreviations independently of any
    # later declaration. Generic X/Sum1 cannot inherit a nearby topic.
    lexical = {}
    for match in re.finditer(r"(?<!\w)([A-Za-z][A-Za-z0-9_]*)\s*\)?\s*(?:=|is\b|equals?\b)", text):
        alias = match.group(1)
        if not ("_" in alias or any(c.isupper() for c in alias)):
            continue
        if alias not in lexical:
            lexical[alias] = {e[1]: e for e in entities if e[0] != e[1] and _abbreviates(alias, e[0])}
        if len(lexical[alias]) == 1:
            entity = next(iter(lexical[alias].values()))
            register(alias, entity, match.start(1), priority=1)
    return {key: value for key, value in declared.items() if value is not None}


def _prose_arithmetic(expression):
    """Translate explicitly grouped binary arithmetic prose, without evaluation."""
    pieces, index = [], 0
    while index < len(expression):
        if expression[index] != '(':
            pieces.append(expression[index])
            index += 1
            continue
        end, depth = index + 1, 1
        while end < len(expression) and depth:
            depth += (expression[end] == '(') - (expression[end] == ')')
            end += 1
        if depth:
            raise ValueError('unclosed prose expression')
        pieces.append('(' + _prose_arithmetic(expression[index + 1:end - 1]) + ')')
        index = end
    rendered = ''.join(pieces).strip()
    operation = re.match(r'(?:the\s+)?(sum of|product of|difference between)\s+', rendered, re.I)
    if not operation:
        return rendered
    body = rendered[operation.end():]
    depth, separators = 0, []
    for match in re.finditer(r'[()]|\band\b', body, re.I):
        if match.group() == '(':
            depth += 1
        elif match.group() == ')':
            depth -= 1
        elif depth == 0:
            separators.append(match)
    if len(separators) != 1:
        raise ValueError('ambiguous prose operands')
    sep = separators[0]
    operator = {'sum of': '+', 'product of': '*', 'difference between': '-'}[operation.group(1).lower()]
    return '(' + _prose_arithmetic(body[:sep.start()]) + operator + _prose_arithmetic(body[sep.end():]) + ')'


def _expression_tree(expression: str, entities: list[tuple]):
    """Validate printed arithmetic and derive a value-blind structural key."""
    expression = expression.strip().strip("$")
    expression = re.sub(r"([A-Za-z])_\{([A-Za-z0-9]+)\}", r"\1_\2", expression)
    expression = expression.replace(r"\times", "*").replace(r"\cdot", "*").replace(r"\div", "/")
    expression = expression.translate(str.maketrans({"×": "*", "÷": "/", "−": "-", "^": "**"}))
    expression = re.sub(r"\s*(?:\\?mod(?=\b|\d)|modulo\b)\s*", " % ", expression, flags=re.IGNORECASE)
    names = defaultdict(set)
    for alias, node_id, *_ in entities:
        names[alias.casefold()].add(node_id)
    symbols = {}
    for index, alias in enumerate(sorted(names, key=len, reverse=True)):
        if len(names[alias]) != 1:
            continue
        symbol = f"entity_{index}"
        pattern = rf"(?<!\w)(?:(?:the\s+)?number of\s+)?{re.escape(alias)}(?!\w)"
        # Printed scalar annotations on names are not function calls or
        # multiplication. Bare numeric annotations require a human name;
        # p1(22) remains unsupported rather than silently changing its meaning.
        annotation = r'which\s+is\s+' if not re.search(r"\s|'s", alias) else r'(?:which\s+is\s+)?'
        pattern += r'(?:[ \t]*\(' + annotation + NUMBER + r'\))?'
        expression = re.sub(pattern, symbol, expression, flags=re.IGNORECASE)
        symbols[symbol] = next(iter(names[alias]))
    # Replace operators after entity names, so names containing e.g. "Plus"
    # retain their identity. This translates printed syntax, never computes it.
    for words, operator in ((r'plus', '+'), (r'minus', '-'),
                            (r'multiplied by|times', '*'), (r'divided by', '/')):
        expression = re.sub(r'\b(?:' + words + r')\b', operator, expression, flags=re.I)
    try:
        if re.search(r'\b(?:sum of|product of|difference between)\b', expression, re.I):
            expression = _prose_arithmetic(expression)
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
    def canonical(node):
        if isinstance(node, ast.BinOp):
            node.left, node.right = canonical(node.left), canonical(node.right)
            if isinstance(node.op, (ast.Add, ast.Mult)):
                def terms(child):
                    return terms(child.left) + terms(child.right) if isinstance(child, ast.BinOp) and type(child.op) is type(node.op) else [child]
                parts = sorted(terms(node), key=lambda n: ast.dump(n, include_attributes=False))
                result = parts[0]
                for part in parts[1:]:
                    result = ast.BinOp(result, type(node.op)(), part)
                return result
        elif isinstance(node, ast.UnaryOp):
            node.operand = canonical(node.operand)
        return node
    tree.body = canonical(tree.body)
    return phase, ast.dump(tree, include_attributes=False)


def _numeric_commit(text: str, start: int, entities: list[tuple], *, target_node=None):
    """Accept a terminal printed scalar, never evaluate an unfinished RHS."""
    line_end = text.find("\n", start)
    line_end = len(text) if line_end < 0 else line_end
    rhs = text[start:line_end]
    # Keep source offsets while preventing an operand annotation's "is"
    # from being mistaken for another relation in the equation chain.
    rhs = re.sub(r'\(which\s+is\s+' + NUMBER + r'\)', lambda m: ' ' * len(m.group()), rhs, flags=re.I)
    number = re.compile(NUMBER)
    for result in number.finditer(rhs):
        prefix = rhs[:result.start()].strip().strip("$").strip()
        scalar = prefix == "" or re.fullmatch(r"(?:(?:also|still|equal to)\b\s*)?\(*\s*", prefix, re.I)
        prose_copy = re.fullmatch(r"(?:the )?same as\s+(.+?),\s*(?:so\s*)?", prefix, re.I)
        if prose_copy is None:
            prose_copy = re.fullmatch(
                r"(?:equal to\s+)?(.+?),\s*(?:which (?:is|we just found to be)|so (?:that's|that is)(?: also)?)\s*",
                prefix, re.I)
        relation = r"=|≡|\\equiv\b|\bis\b|\bequals?\b"
        if not scalar and not prose_copy and not re.search(r"(?:" + relation + r")$", prefix, re.I):
            continue
        suffix = rhs[result.end():]
        # A close parenthesis or a LaTeX marker cannot hide pending math.
        rest = re.sub(r"^(?:\s*[)$])*\s*", "", suffix)
        mod = re.match(r"(?P<open>\()?\s*(?:\\?mod(?=\b|\d)|modulo\b)\s*(?P<modulus>" + NUMBER + r")\s*(?(open)\))", rest, re.IGNORECASE)
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
        if rest and not re.match(r"[.,;?!→]|</", rest):
            continue
        expressions = [prose_copy.group(1)] if prose_copy else [] if scalar else re.split(relation, prefix, flags=re.I)[:-1]
        trees = [_expression_tree(expr, entities) for expr in expressions]
        if any(tree is None for tree in trees):
            continue
        if prose_copy and (trees[0][0] != "copy" or "unresolved:" in trees[0][1]):
            continue
        # X = Full name = expression = value repeats the destination label.
        # Preserve other-entity copies and arithmetic involving X itself.
        self_name = ('copy', ast.dump(ast.Expression(body=ast.Name(id=target_node, ctx=ast.Load())),
                                     include_attributes=False)) if target_node is not None else None
        while not prose_copy and trees and trees[0] == self_name:
            trees.pop(0)
        phase, signature = trees[0] if trees else ("commit", "scalar")
        if any(tree[0] == "reduction" for tree in trees) or re.search(r"≡|\\equiv\b", prefix):
            phase = "reduction"
        kind = "calculation" if phase == "reduction" or any(tree[0] == "calculation" for tree in trees) else "commit"
        # A printed residue is a different stage from an unannotated raw
        # scalar, even when their numbers happen to coincide.
        if mod and phase in {"commit", "copy"}:
            phase = "residue_" + phase
        # Keep only printed operation views, not an inferred DAG expression.
        views = list(dict.fromkeys(sig for ph, sig in trees if ph != "commit")) or [signature]
        return start + result.start(), start + result.end(), result.group(), kind, phase, signature, views
    return None


def _substitution_shape(signature, *, before_reduction=False):
    """Check complete printed substitution, never a partial term's value."""
    key = expression_key(signature)
    if before_reduction and key[0] == 'BinOp':
        fields = dict(key[1])
        if fields.get('op') == ('Mod', ()):
            key = fields['left']
    def mask(node):
        if not isinstance(node, tuple):
            return node
        if node and node[0] == 'Name':
            return 'Constant', (('value', 'number'),)
        if node and node[0] in ('Add', 'Mult'):
            return node[0], tuple(sorted((mask(child) for child in node[1]), key=repr))
        return tuple(mask(child) for child in node)
    return mask(key)


def _adjacent_substitution(text, start, entities):
    """A printed formula followed by its explicit local operand substitution."""
    # Stay within a single line; a new paragraph/region cannot supply the work.
    line = text[start:].split('\n', 1)[0]
    follow = re.match(r'(?P<formula>.+?)\.[ \t]+', line)
    formulas = [_expression_tree(part, entities) for part in follow.group('formula').split('=')] if follow else []
    if not formulas or any(f is None or f[0] not in {'calculation', 'reduction', 'copy'} for f in formulas):
        return None
    formula = formulas[0]
    offset = follow.end()
    direct = re.match(r'(?:(?:So|That\x27s|That is)[ \t]+|Let me compute that[.:][ \t]+)?(?P<work>[+\-(\d])', line[offset:], re.I)
    operand = None if direct else re.match(r'(?:Since[ \t]+)?(?P<name>[^.,;!?=]+?)[ \t]+(?:is|equals?)[ \t]+'
                       + NUMBER + r'(?P<connector>,[ \t]*(?:so[ \t]+)?|\.[ \t]+So[ \t]+)',
                       line[offset:], re.I)
    if operand:
        named = _expression_tree(operand.group('name'), entities)
        if not named or named[0] != 'copy' or 'unresolved:' in named[1]:
            return None
        # Require an explicitly printed operand of THIS formula. A new
        # destination/topic may not lend its following arithmetic backwards.
        name_key = expression_key(named[1])
        def contains(key):
            return key == name_key or isinstance(key, tuple) and any(contains(k) for k in key)
        if not contains(expression_key(formula[1])):
            return None
        offset += operand.end()
        expanded = re.match(r'that would be[ \t]+(?P<expr>.+?)\.[ \t]+Let me compute that[:.][ \t]+',
                            line[offset:], re.I)
        if expanded:
            view = _expression_tree(expanded.group('expr'), [])
            if not view or 'Name(' in view[1] or _substitution_shape(formula[1], before_reduction=True) != _substitution_shape(view[1]):
                return None
            offset += expanded.end()
    elif direct:
        offset += direct.start('work')
    if not re.match(r'[+\-(\d]', line[offset:]):
        return None
    printed = _numeric_commit(text, start + offset, [])
    if (not printed or printed[3] != 'calculation' or any('Name(' in v for v in printed[6])
            or not any(_substitution_shape(f[1], before_reduction=printed[4] != 'reduction')
                       == _substitution_shape(printed[5]) for f in formulas)):
        return None
    value_start, end, value, kind, phase, signature, views = printed
    if formula[0] == phase:
        signature, views = formula[1], list(dict.fromkeys([f[1] for f in formulas if f[0] == phase] + views))
    return value_start, end, value, kind, phase, signature, views


def _split_printed_reduction(text, start, result, entities, node_id):
    """Retain an explicit raw result before its reduction in an equation chain."""
    if result[4] != 'reduction':
        return None
    pattern = re.compile(r'(?P<raw>' + NUMBER + r')[ \t]*(?P<op>(?:\\?mod(?=\b|\d)|modulo\b)|≡|\\equiv\b)', re.I)
    for match in pattern.finditer(text, start, result[0]):
        raw = _numeric_commit(text[:match.end('raw')], start, entities, target_node=node_id)
        # The prefix must print the result of a complete raw calculation.
        # An operand inside (a+b) mod m or q=25 mod m is not another result.
        if not raw or raw[4] != 'calculation' or raw[0] != match.start('raw'):
            continue
        reduced = _numeric_commit(text, match.start('raw'), entities)
        if not reduced or reduced[1] != result[1]:
            continue
        if match.group('op') in {'≡', r'\equiv'}:
            modulus = re.match(r'[ \t]*\(?[ \t]*(?:\\?mod(?=\b|\d)|modulo\b)[ \t]*(' + NUMBER + r')',
                               text[result[1]:], re.I)
            if modulus is None:
                continue
            # "25 ≡ 2 mod 23" explicitly states the same reduction as
            # "25 mod 23 = 2". No arithmetic or value-based binding is used.
            _, signature = _expression_tree(match.group('raw') + ' mod ' + modulus.group(1), [])
            reduced = (*reduced[:5], signature, [signature])
        return raw, match.start('raw'), reduced
    return None


def _adjacent_reduction(text, end, entities):
    """Read an explicitly printed local reduction; never compute a residue."""
    separator = re.match(r'[ \t]*(?:\.[ \t]*(?:(?:Then|Since|So(?: that\x27s)?)[ \t]+)?'
                         r'|,[ \t]*(?:then[ \t]+)?|→[ \t]*)', text[end:], re.I)
    if separator is None:
        return None
    start = end + separator.end()
    direct = re.match(NUMBER + r'[ \t]*(?:mod(?=\b|\d)|modulo)[ \t]*' + NUMBER
                      + r'[ \t]*(?:=|is\b|equals?\b)', text[start:], re.I)
    if direct:
        result = _numeric_commit(text, start, entities)
        return (start, result) if result and result[4] == 'reduction' else None
    division = re.match(r'(?P<raw>' + NUMBER + r')[ \t]+divided by[ \t]+(?P<mod>' + NUMBER
                        + r')[ \t]+is[ \t]+' + NUMBER + r'[ \t]+with[ \t]+(?:a[ \t]+)?remainder[ \t]+(?:of[ \t]+)?',
                        text[start:], re.I)
    heading = re.match(r'(?:modulo|mod)[ \t]*(?P<mod>' + NUMBER + r'),[ \t]*(?P<raw>' + NUMBER + r')(?=[ \t]*-)',
                       text[start:], re.I)
    if division:
        result = _numeric_commit(text, start + division.end(), [])
        match = division
        if not result or result[4] != 'commit':
            return None
    elif heading:
        result = _numeric_commit(text, start + heading.start('raw'), [])
        match = heading
        shapes = {_expression_tree(expr, [])[1] for expr in ('1 - 1', '1 - 1 * 1')}
        if not result or result[5] not in shapes:
            return None
    else:
        return None
    _, signature = _expression_tree(match.group('raw') + ' mod ' + match.group('mod'), [])
    return start, (*result[:3], 'calculation', 'reduction', signature, [signature])


def _concludes_local_reduction(text, previous, start, node_id, scope):
    """A 'therefore' commit inherits an explicitly stated local modulo stage.

    Require the immediately preceding event to calculate the same quantity.
    Only anonymous arithmetic and narrow connective prose may intervene; a
    different entity, conditional, region marker or new topic breaks the link.
    Printed numbers are never checked for equality or arithmetic correctness.
    """
    if (previous.node_id != node_id or previous.identity.scope != scope
            or previous.event_kind != 'calculation' or previous.event_phase not in {'calculation', 'reduction'}):
        return False
    between = text[previous.end:start]
    if not re.search(r'\b(?:so|therefore|thus|hence|then)\s*[:,]?\s*(?:the\s+number\s+of\s*)?$', between, re.I):
        return False
    if previous.event_phase != 'reduction' and not re.search(r'\b(?:mod|modulo)\s*' + NUMBER, between, re.I):
        return False
    masked = re.sub(NUMBER, ' ', between).casefold()
    allowed = set(('now applying working modulo mod let s me compute divide divided by is equals equal to '
                   'so therefore thus hence then the result remainder of with a since but we re number').split())
    if not set(re.findall(r'[a-z]+', masked)) <= allowed:
        return False
    return re.fullmatch(r"[\s.,:;'’()+*/=×÷−\-]*", re.sub(r'[a-z]+', '', masked)) is not None


def _parse_assignments(text: str, task: Task, entities: list[tuple]) -> list[Event]:
    source_text = text
    # Mask paired inline formatting with spaces of exactly the same length.
    # Match on rendered words while reporting offsets in the saved raw text.
    text = re.sub(r"(?<!\w)(\*\*|__|`)(?=\S)([^\n]*?\S)\1(?!\w)",
                  lambda match: " " * len(match.group(1)) + match.group(2) + " " * len(match.group(1)), text)
    declarations = _declared_aliases(text, entities)
    registered = {(e[0].casefold(), e[1]) for e in entities}
    entities = [*entities, *[entity for entity, _ in declarations.values() if (entity[0].casefold(), entity[1]) not in registered]]
    counts = Counter(alias.casefold() for alias, *_ in entities)
    found = []
    for alias, node_id, gold, scope, parents, graph_status in entities:
        if counts[alias.casefold()] != 1:
            continue
        closing = r"[ \t]*\)?" if alias.casefold() in declarations else ""
        pattern = re.compile(
            rf"(?<!\w){re.escape(alias)}{closing}[ \t]*(?:=|:|equals?\b|is\b|are\b)[ \t]*",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            declared = declarations.get(alias.casefold())
            if declared is not None and (alias.casefold(), node_id) not in registered and match.start() < declared[1]:
                continue
            start = match.start()
            # An entity mentioned inside another assignment's RHS is not a
            # new assignment head (e.g. q = p1 and p2 = 3).
            line_start = text.rfind("\n", 0, start) + 1
            clause_start = max(line_start, text.rfind(";", 0, start) + 1)
            preceding = text[clause_start:start]
            sentence_prefix = re.split(r"[.!?](?!\d)", preceding)[-1]
            if (re.search(r"\bif\s+(?:(?:the\s+)?number of\s*)?$", sentence_prefix, re.I)
                    or re.search(r"\bif\b.*(?:=|\bis\b|\bequals?\b)", sentence_prefix, re.I)):
                # An if-clause and its same-sentence consequent describe a
                # conditional, not a committed value in the current derivation.
                continue
            # A line-leading Markdown marker is layout, not a preceding
            # operand. Keep offsets in the original text unchanged.
            if clause_start == line_start:
                preceding = re.sub(r"^\s*(?:>\s*)?[-*+•]\s+", "", preceding)
            preceding = re.split(r"\.(?!\d)|,\s+(?=[A-Za-z])", preceding)[-1]
            if "=" in preceding:
                continue
            if re.search(r"(?:\b(?:and|plus|minus|times|add|subtract|multiply|divide|with)|[+*/×÷−-])\s*(?:(?:the\s+)?number of\s*)?$", preceding, re.IGNORECASE):
                continue
            kind = "restatement" if any(p.premise_id == node_id for p in task.premises) else "commit"
            if task.answer_spec.kind == "numeric":
                visible_entities = [entity for entity in entities if entity[0].casefold() not in declarations
                                    or declarations[entity[0].casefold()][1] <= start
                                    or (entity[0].casefold(), entity[1]) in registered]
                # A named destination supplies the lexical namespace for a
                # shortened RHS (Studio's Pack: same as Rucksack, 3).
                owners = {a.rsplit("'s ", 1)[0] for a, nid, *_ in visible_entities if nid == node_id and "'s " in a}
                if len(owners) == 1:
                    owner = next(iter(owners)) + "'s "
                    visible_entities += [(a[len(owner):], *entity[1:]) for entity in visible_entities
                                         if (a := entity[0]).startswith(owner)]
                result = _numeric_commit(text, match.end(), visible_entities, target_node=node_id)
                if result is None:
                    result = _adjacent_substitution(text, match.end(), visible_entities)
                if result is None:
                    continue
                split = _split_printed_reduction(text, match.end(), result, visible_entities, node_id)
                if split:
                    raw, reduced_start, result = split
                    raw_value_start, raw_end, raw_value, raw_kind, raw_phase, raw_sig, raw_views = raw
                    found.append((start, raw_end, raw_value_start, node_id, gold, scope, parents, graph_status,
                                  raw_value, 'restatement' if kind == 'restatement' else raw_kind,
                                  raw_phase, raw_sig, raw_views))
                    start = reduced_start
                value_start, end, value, parsed_kind, phase, signature, views = result
                if kind != "restatement":
                    kind = parsed_kind
            else:
                result = re.match(r"[^\n.;]+", text[match.end():])
                if result is None:
                    continue
                value_start, end, value = match.end(), match.end() + result.end(), result.group()
                phase, signature, views = "commit", "text", []
            found.append((start, end, value_start, node_id, gold, scope, parents, graph_status, value, kind, phase, signature, views))
            if task.answer_spec.kind == "numeric" and kind == "calculation" and phase == "calculation":
                # A directly adjacent anonymous reduction continues this
                # named calculation. Keep BOTH printed stages: the raw result
                # must not silently become the residue or leave the denominator.
                continuation = _adjacent_reduction(text, end, visible_entities)
                if continuation:
                    reduction_start, reduced = continuation
                    rvalue_start, rend, rvalue, rkind, rphase, rsig, rviews = reduced
                    found.append((reduction_start, rend, rvalue_start, node_id, gold, scope,
                                  parents, graph_status, rvalue, rkind, rphase, rsig, rviews))
    found.sort(key=lambda item: (item[0], item[1]))
    # "Entity: X = value" names one printed result twice. Use the innermost
    # assignment's arithmetic, keeping the complete statement's start.
    distinct = {}
    for item in found:
        key = (item[3], item[5], item[2], item[1])
        previous = distinct.get(key, item)
        distinct[key] = (min(previous[0], item[0]), *item[1:])
    found = sorted(distinct.values(), key=lambda item: (item[0], item[1]))
    line_counts = Counter(item[0] for item in found)
    occurrences: Counter = Counter()
    events = []
    context_cache = {}
    stopwords = set(('a an the of to and or is as be so let me we it this that then therefore number mod modulo '
                     'equals equal all are was with for at in on i my our zero one two three four five six seven '
                     'eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen '
                     'twenty thirty forty fifty sixty seventy eighty ninety hundred thousand').split())
    node_tokens = {e[1]: context_entity_token(e[1]) for e in entities}
    alias_patterns = [(re.compile(rf'(?<!\w){re.escape(alias)}(?!\w)', re.I), node_tokens[nid])
                      for alias, nid, *_ in sorted(entities, key=lambda e: -len(e[0])) if counts[alias.casefold()] == 1]
    region_markers = list(re.finditer(r'</?think>', source_text))
    def context(start, end, node_id):
        previous = source_text.rfind('\n\n', 0, start)
        lo = previous + 2 if previous >= 0 else 0
        hi = source_text.find('\n\n', end)
        hi = len(source_text) if hi < 0 else hi
        # Paragraph layout is independent of the thinking/answer boundary.
        # Answer prose must never resolve a repeated thinking assignment.
        for marker in region_markers:
            if marker.end() <= start:
                lo = max(lo, marker.end())
            elif marker.start() >= end:
                hi = min(hi, marker.start())
        key = (lo, hi)
        if key not in context_cache:
            block = source_text[lo:hi]
            for pattern, token in alias_patterns:
                block = pattern.sub(' ' + token + ' ', block)
            block = re.sub(r'\b\d+(?:st|nd|rd|th)\b', ' ', block, flags=re.I)
            block = re.sub(NUMBER, ' ', block)
            context_cache[key] = sorted(set(re.findall(r'[a-z]+', block.casefold())) - stopwords)
        return [word for word in context_cache[key] if word != node_tokens[node_id]]
    for start, end, value_start, node_id, gold, scope, parents, graph_status, value, kind, phase, signature, views in found:
        if (kind == 'commit' and phase == 'commit' and events
                and _concludes_local_reduction(source_text, events[-1], start, node_id, scope)):
            phase = 'residue_commit'
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
                source_text[start:end],
                parents_out,
                canonical_value(value) == canonical_value(gold) if gold is not None else None,
                surface_mentions=surface_mentions(text[start:end], task),
                node_id=node_id,
                graph_status=graph_status,
                status=status,
                event_kind=kind,
                event_phase=phase,
                expression_signature=signature,
                expression_views=views,
                alignment_context=context(start, end, node_id),
            )
        )
    return events


def parse_events(text: str, task: Task) -> list[Event]:
    """Premises and nodes. Used by scientific generate; values never decide identity."""
    from .quantity_steps import is_controlled, parse_steps
    if is_controlled(task):
        return parse_steps(text, task)
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


def _align_unique_events(base: list[Event], changed: list[Event]) -> dict:
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


def _alignment_key(event):
    return (event.identity.entity_or_expression, event.node_id, event.identity.scope,
            event.event_kind, event.event_phase, expression_key(event.expression_signature))


def _compatible_events(a, b):
    if _alignment_key(a)[:-1] != _alignment_key(b)[:-1]:
        return False
    if expression_key(a.expression_signature) == expression_key(b.expression_signature):
        return True
    av, bv = set(map(expression_key, a.expression_views)), set(map(expression_key, b.expression_views))
    named_a = {expression_key(v) for v in a.expression_views if "Name(" in v}
    named_b = {expression_key(v) for v in b.expression_views if "Name(" in v}
    # Common numeric arithmetic must not hide different named inputs.
    if named_a and named_b and not named_a & named_b:
        return False
    return bool(av & bv)


def align_events(base: list[Event], changed: list[Event]) -> dict:
    """Retain only correspondences forced by all optimal ordered alignments.

    A correspondence assumes stage order is preserved in this region. The
    score counts compatible steps, never values, gold answers, or proximity.
    Multiple optimal partners stay unknown rather than taking a tie-break.
    """
    from .quantity_steps import PHASE, align_steps
    if any(e.event_phase == PHASE for e in base + changed):
        # align_steps accepts only registered steps, including when the
        # counterpart is empty; natural and controlled units never match.
        return align_steps(base, changed)
    if not any(e.expression_signature for e in base + changed) or all(
        e.event_phase == "final_assignment" for e in base + changed
    ):
        # Legacy fixtures have explicitly enumerated identities. The separate
        # final-state diagnostic matches entities rather than all-step order.
        return _align_unique_events(base, changed)
    for events in (base, changed):
        if len({e.identity.key() for e in events}) != len(events):
            raise ValueError("Duplicate event identities cannot be aligned")
    pairs, certificates, unmatched = [], [], []
    for region in sorted({e.event_region for e in base + changed}):
        left = sorted([e for e in base if e.event_region == region and e.status == "ok"], key=lambda e: e.start)
        right = sorted([e for e in changed if e.event_region == region and e.status == "ok"], key=lambda e: e.start)
        aa, bb = [_alignment_key(e) for e in left], [_alignment_key(e) for e in right]
        n, m = len(aa), len(bb)
        edges = [[_compatible_events(a, b) for b in right] for a in left]
        def context_score(a, b):
            x, y = set(a.alignment_context), set(b.alignment_context)
            common = x & y
            return 1000 * len(common) // len(x | y) if len(common) >= 2 else 0
        context_scores = [[context_score(a,b) if edges[i][j] else 0 for j,b in enumerate(right)] for i,a in enumerate(left)]
        # Lexicographic objective: maximize compatible steps, then lexical
        # discourse agreement. Neither target values nor position distance
        # enters the objective; ties across optimal paths remain unresolved.
        unit = (min(n,m) + 1) * 1001
        prefix = [[0] * (m + 1) for _ in range(n + 1)]
        suffix = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(m):
                prefix[i + 1][j + 1] = max(prefix[i][j + 1], prefix[i + 1][j],
                    prefix[i][j] + unit + context_scores[i][j] if edges[i][j] else 0)
        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                suffix[i][j] = max(suffix[i + 1][j], suffix[i][j + 1],
                    suffix[i + 1][j + 1] + unit + context_scores[i][j] if edges[i][j] else 0)
        # Every optimal path has exactly one pair at each matched rank. A
        # rank with one feasible edge is common to every such path.
        ranks = defaultdict(list)
        optimum = prefix[n][m]
        for i in range(n):
            for j in range(m):
                if edges[i][j] and prefix[i][j] + unit + context_scores[i][j] + suffix[i + 1][j + 1] == optimum:
                    ranks[prefix[i][j] // unit + 1].append((i, j))
        forced = [(rank, edges[0]) for rank, edges in ranks.items() if len(edges) == 1]
        context_entities = {aa[i][:3] for _, (i, j) in forced}
        for rank, (i, j) in forced:
            unique = sum(edges[i]) == sum(row[j] for row in edges) == 1
            distinguishing_context = (context_scores[i][j] > 0
                and context_scores[i].count(context_scores[i][j]) == 1
                and sum(row[j] == context_scores[i][j] for row in context_scores) == 1
                and context_scores[i][j] == max(context_scores[i]) == max(row[j] for row in context_scores))
            # Counts alone do not resolve an isolated run of identical
            # confirmations; require an independent entity in the context.
            if not unique and len(context_entities) < 2 and not distinguishing_context:
                continue
            pairs.append((left[i], right[j]))
            certificates.append({"left": left[i].identity.key(), "right": right[j].identity.key(),
                                 "region": region, "matched_rank": rank, "optimal_length": optimum // unit,
                                 "context_agreement": context_scores[i][j], "context_distinguishes_repeat": distinguishing_context,
                                 "objective": "max_compatible_steps_then_value_masked_discourse",
                                 "expression_evidence": "primary_canonical" if expression_key(left[i].expression_signature) == expression_key(right[j].expression_signature) else "printed_view_intersection",
                                 "feasible_edges_at_rank": 1, "independent_context_entities": len(context_entities)})
        matched = {e.identity.key() for e, _ in pairs}
        optimal_edges = {edge for group in ranks.values() for edge in group}
        for i, event in enumerate(left):
            if event.identity.key() in matched:
                continue
            entity = [j for j in range(m) if aa[i][:3] == bb[j][:3]]
            phase = [j for j in entity if aa[i][3:5] == bb[j][3:5]]
            compatible = [j for j in phase if edges[i][j]]
            feasible = [j for j in compatible if (i, j) in optimal_edges]
            reason = ("no_same_entity" if not entity else "phase_incompatible" if not phase else
                      "expression_incompatible" if not compatible else "order_or_context_conflict" if not feasible
                      else "ambiguous_repeated_step")
            unmatched.append({"left": event.identity.key(), "region": region, "reason": reason,
                              "same_entity_candidates": len(entity), "same_phase_candidates": len(phase),
                              "compatible_candidates": [right[j].identity.key() for j in compatible],
                              "optimal_candidates": [right[j].identity.key() for j in feasible],
                              "interpretation": "parsed_event_sets_only_not_proof_of_model_omission"})
    paired_left = {e.identity.key() for e, _ in pairs}
    paired_right = {e.identity.key() for _, e in pairs}
    removed = [e.identity.key() for e in base if e.identity.key() not in paired_left]
    added = [e.identity.key() for e in changed if e.identity.key() not in paired_right]
    return {"pairs": pairs, "pair_certificates": certificates, "unmatched_left": unmatched, "removed": removed, "added": added,
            "unaligned": removed + added,
            "structural": {"disappeared": removed, "merged": [],
                           "strategy_changed": [e.identity.key() for e in base + changed if e.status == "strategy_change"],
                           "ambiguous": [{"left": removed, "right": added, "reason": "non_forced_or_incompatible_step"}] if removed or added else [],
                           "detector": ALIGNMENT_POLICY,
                           "strategy_detector": "status_field_only", "scanned": False}}


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
