"""Domain scorers. Code scoring never execs on the host."""
from __future__ import annotations

from .executor import get_executor
from .schema import canonical_value


def score_numeric(prediction: str, gold: str) -> dict:
    ok = canonical_value(prediction) == canonical_value(gold)
    return {"metric": "exact_match", "value": 1.0 if ok else 0.0, "denominator": 1, "eligibility": True}


def score_qa(prediction: str, gold: str, aliases: list[str] | None = None) -> dict:
    cand = {canonical_value(gold), *(canonical_value(a) for a in aliases or [])}
    ok = canonical_value(prediction) in cand
    return {"metric": "em", "value": 1.0 if ok else 0.0, "denominator": 1, "eligibility": True}


def score_code(source: str, tests: str, executor=None) -> dict:
    backend = executor or get_executor()
    result = backend.submit(source, tests)
    value = None if result.tests_passed is None else (1.0 if result.tests_passed else 0.0)
    return {
        "metric": "isolated_unit",
        "value": value,
        "denominator": None if result.status == "executor_unavailable" else 1,
        "eligibility": result.status not in {"executor_unavailable", "rejected"},
        "failure_reason": result.reason,
        "status": result.status,
    }
