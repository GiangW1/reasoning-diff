"""All variants, models and editing rounds share their base problem's split role."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .schema import SPLIT_ROLES

DEFAULT_FRACTIONS = (0.40, 0.15, 0.10, 0.10, 0.10, 0.15)
TEST_ONLY_SOURCES = frozenset({"gsm_plus", "GSM-Plus", "gsm-plus"})
_TEST_ONLY_FAMILY_KEYS: set[str] = set()


def _lock_file() -> Path:
    return Path(__file__).resolve().parents[2] / ".planning" / "research" / ".cache" / "gsm_test_only_families.json"


def _load_persisted_locks() -> set[str]:
    path = _lock_file()
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {str(item) for item in data} if isinstance(data, list) else set()


def _save_persisted_locks() -> None:
    path = _lock_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    merged = sorted(_TEST_ONLY_FAMILY_KEYS | _load_persisted_locks())
    path.write_text(json.dumps(merged), encoding="utf-8")


def gsm_text_key(record: dict) -> str | None:
    from .schema import canonical_value

    text = record.get("seed_question") or record.get("original_question") or record.get("question")
    if not text:
        return None
    return "q:" + canonical_value(str(text))


def gsm_family_id(record: dict) -> str:
    from .schema import canonical_value

    for key in ("original_id", "id_orig", "seed_id", "gsm8k_id"):
        val = record.get(key)
        if val and "gsm8k" in str(val).lower():
            return canonical_value(str(val))
    text = gsm_text_key(record)
    if text:
        return text
    return canonical_value(str(record.get("id") or record.get("task_id") or ""))


def register_test_only_family(*keys: str | None) -> None:
    added = False
    for key in keys:
        if key:
            _TEST_ONLY_FAMILY_KEYS.add(key)
            added = True
    if added:
        _save_persisted_locks()


def clear_test_only_families() -> None:
    _TEST_ONLY_FAMILY_KEYS.clear()
    path = _lock_file()
    if path.exists():
        path.unlink()


def family_locked_test(*keys: str | None) -> bool:
    locked = _TEST_ONLY_FAMILY_KEYS | _load_persisted_locks()
    return any(key in locked for key in keys if key)


def assign_split(
    base_group_id: str,
    seed: int = 0,
    fractions=DEFAULT_FRACTIONS,
    test_only: bool = False,
    source: str | None = None,
    fit_eligible: bool | None = None,
) -> str:
    token = f"{source or ''}:{base_group_id}".lower()
    if (
        test_only
        or fit_eligible is False
        or (source is not None and source in TEST_ONLY_SOURCES)
        or "gsmplus" in token
        or "gsm-plus" in token
        or "gsm_plus" in token
    ):
        return "test"
    if len(fractions) != len(SPLIT_ROLES) or any(v <= 0 for v in fractions) or abs(sum(fractions) - 1) > 1e-9:
        raise ValueError("Require six positive split fractions summing to 1")
    value = int.from_bytes(hashlib.sha256(f"{seed}:{base_group_id}".encode()).digest()[:8], "big") / 2**64
    cumulative = 0.0
    for split, fraction in zip(SPLIT_ROLES, fractions, strict=True):
        cumulative += fraction
        if value < cumulative:
            return split
    return SPLIT_ROLES[-1]


def assign_family(
    members: list[str],
    seed: int = 0,
    fractions=DEFAULT_FRACTIONS,
    test_only: bool = False,
    family_id: str | None = None,
    source: str | None = None,
) -> dict[str, str]:
    if not members:
        raise ValueError("Empty family")
    if family_id is None:
        raise ValueError("assign_family requires a stable family_id; member lists are not a family key")
    key = family_id
    role = assign_split(key, seed=seed, fractions=fractions, test_only=test_only, source=source, fit_eligible=None)
    return {member: role for member in members}


def split_for_task(task, seed: int = 0, fractions=DEFAULT_FRACTIONS, siblings: list | None = None) -> str:
    eligible = task.metadata.get("fit_eligible")
    family = task.metadata.get("shared_gsm_family") or task.base_group_id
    keys = {item for item in (family, task.metadata.get("shared_gsm_text"), task.base_group_id) if item}
    pool = [task, *(siblings or [])]
    sibling_lock = any(
        (
            getattr(other, "source", None) in TEST_ONLY_SOURCES
            or (getattr(other, "metadata", {}) or {}).get("fit_eligible") is False
        )
        and keys
        & {
            item
            for item in (
                (getattr(other, "metadata", {}) or {}).get("shared_gsm_family"),
                (getattr(other, "metadata", {}) or {}).get("shared_gsm_text"),
                getattr(other, "base_group_id", None),
            )
            if item
        }
        for other in pool
    )
    locked = family_locked_test(family, task.metadata.get("shared_gsm_text"), task.base_group_id) or sibling_lock
    return assign_split(
        family,
        seed=seed,
        fractions=fractions,
        test_only=locked,
        source=task.source,
        fit_eligible=None if eligible is None else bool(eligible),
    )


def assert_same_role(members: dict[str, str]) -> str:
    roles = set(members.values())
    if len(roles) != 1:
        raise ValueError(f"Family members split across roles: {members}")
    return next(iter(roles))


def assert_disjoint(groups: dict[str, set[str]]) -> None:
    seen: set[str] = set()
    for name, ids in groups.items():
        overlap = seen & ids
        if overlap:
            raise ValueError(f"Base-problem leakage into {name}: {sorted(overlap)[:5]}")
        seen |= ids


def require_split(split: str, allowed: tuple[str, ...], operation: str) -> None:
    if split not in allowed:
        raise ValueError(f"{operation} cannot fit on {split}; expected {allowed}")


def require_persisted_roles(
    rows: list[dict],
    expected: str,
    operation: str,
    scientific: bool = False,
    allow_mixed: bool = False,
) -> None:
    if not rows:
        raise ValueError(f"{operation} requires persisted splits.jsonl roles")
    roles = {row.get("role") for row in rows}
    if "test" in roles and expected != "test":
        raise ValueError(f"{operation} refuses test-family artifacts {sorted(roles)}")
    if scientific and expected not in roles:
        raise ValueError(f"{operation} requires persisted {expected} rows; found {sorted(roles)}")
    if scientific and not allow_mixed and roles != {expected}:
        raise ValueError(f"{operation} persisted roles {sorted(roles)} do not match {expected}")


def lock_test_only(source: str, requested: str | None = None) -> str:
    if source in TEST_ONLY_SOURCES:
        if requested not in {None, "test"}:
            raise ValueError(f"{source} is test-only and cannot be assigned {requested}")
        return "test"
    if requested:
        return requested
    raise ValueError("split role required")
