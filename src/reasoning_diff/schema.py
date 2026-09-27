"""Versioned, JSON-serializable contracts shared by all experiment stages."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from fractions import Fraction
from typing import Any
import math

SCHEMA_VERSION = 1

SOURCE_KINDS = ("official", "project_derived", "fixture")
GRAPH_STATUSES = ("complete", "partial", "unknown")
SPLIT_ROLES = (
    "probe_train",
    "dev",
    "direction_fit",
    "calibration",
    "transfer_pairs",
    "test",
)
OUTCOMES = (
    "changed",
    "no_change",
    "structural",
    "unaligned",
    "parse_failed",
    "generation_failed",
)
SCAN_STATES = ("observed_response", "no_response_observed_in_scan", "unscanned", "unknown")
ALIGNMENT_STATUSES = (
    "matched",
    "missing",
    "merged",
    "split",
    "version_changed",
    "ambiguous",
    "unmatched",
)
POSITION_KINDS = ("pre_step", "pre_value", "post_step")
T4_STATUSES = (
    "insufficient_information",
    "inconsistent_constraints",
    "no_solution",
    "strategy_change",
)


def canonical_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    text = str(value).strip()
    try:
        return str(Fraction(text.replace(",", "")))
    except (ValueError, ZeroDivisionError):
        return " ".join(text.casefold().split())


def _require_enum(name: str, value: str, allowed: tuple[str, ...]) -> None:
    if value not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {value!r}")


@dataclass
class Premise:
    premise_id: str
    text: str
    start: int
    end: int
    value: str | None = None
    kind: str = "fact"
    document_id: str | None = None
    sentence_id: int | None = None


@dataclass
class Node:
    id: str
    parents: list[str]
    value: str
    aliases: list[str] = field(default_factory=list)
    expression: str = ""
    scope: str = "global"


@dataclass
class AnswerSpec:
    value: str | None
    kind: str = "numeric"
    mod: int | None = None
    aliases: list[str] = field(default_factory=list)
    status: str | None = None


@dataclass
class Task:
    task_id: str
    base_group_id: str
    variant_id: str
    tier: str
    source: str
    source_kind: str
    premises: list[Premise]
    question: str
    answer_spec: AnswerSpec
    nodes: list[Node] = field(default_factory=list)
    graph_status: str = "unknown"
    graph_kind: str = "none"
    upstream_id: str | None = None
    upstream_split: str | None = None
    target: str | None = None
    graph_ref: str | None = None
    edit_ref: str | None = None
    schema_version: int = SCHEMA_VERSION
    record_id: str = ""
    run_id: str = ""
    status: str = "ok"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.record_id:
            self.record_id = self.task_id
        _require_enum("source_kind", self.source_kind, SOURCE_KINDS)
        _require_enum("graph_status", self.graph_status, GRAPH_STATUSES)
        if isinstance(self.answer_spec, dict):
            self.answer_spec = AnswerSpec(**self.answer_spec)

    @property
    def id(self) -> str:
        return self.task_id

    @property
    def base_id(self) -> str:
        return self.base_group_id

    def validate(self) -> None:
        if not self.task_id or not self.base_group_id or not self.question:
            raise ValueError("Task id, base_group_id and question must be nonempty")
        if self.source_kind == "official" and self.source in {"self_authored_arithmetic", "fixture"}:
            raise ValueError("Self-authored fixtures cannot be marked official")
        ids = [p.premise_id for p in self.premises] + [n.id for n in self.nodes]
        if len(set(ids)) != len(ids):
            raise ValueError("Premise/node IDs must be unique")
        if not self.premises:
            raise ValueError("Task requires at least one premise")
        for p in self.premises:
            if p.kind in {"sentence", "paragraph", "spec"}:
                if not 0 <= p.start < p.end <= len(p.text):
                    raise ValueError(f"Premise self-span mismatch: {p.premise_id}")
                continue
            if not 0 <= p.start < p.end <= len(self.question) or self.question[p.start:p.end] != p.text:
                raise ValueError(f"Premise span mismatch: {p.premise_id}")
        known = {p.premise_id for p in self.premises}
        for n in self.nodes:
            if not n.parents:
                raise ValueError(f"Node {n.id} requires parents")
            if not set(n.parents) <= known:
                raise ValueError(f"Node {n.id} must reference earlier nodes/premises")
            if len(n.parents) != len(set(n.parents)):
                raise ValueError(f"Repeated dependency in {n.id}")
            known.add(n.id)
        if self.target is not None and self.target not in {n.id for n in self.nodes}:
            raise ValueError("Target must be a task node")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        payload = dict(data)
        payload["premises"] = [Premise(**p) if not isinstance(p, Premise) else p for p in payload["premises"]]
        payload["nodes"] = [Node(**n) if not isinstance(n, Node) else n for n in payload.get("nodes", [])]
        if "answer_spec" in payload and not isinstance(payload["answer_spec"], AnswerSpec):
            payload["answer_spec"] = AnswerSpec(**payload["answer_spec"])
        obj = cls(**{k: v for k, v in payload.items() if k in cls.__dataclass_fields__})
        obj.validate()
        return obj


@dataclass(frozen=True)
class EventIdentity:
    """Identity uses entity/expression, occurrence version, and scope — never the value."""

    entity_or_expression: str
    occurrence_version: int
    scope: str = "global"

    def key(self) -> str:
        import json
        return json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)


@dataclass
class Event:
    identity: EventIdentity
    value: str
    start: int
    end: int
    value_start: int
    text: str
    task_parents: list[str] | None = None
    correct: bool | None = None
    source: str = "parser"
    surface_mentions: list[str] = field(default_factory=list)
    node_id: str = ""
    graph_status: str = "unknown"
    schema_version: int = SCHEMA_VERSION
    record_id: str = ""
    run_id: str = ""
    base_group_id: str = ""
    status: str = "ok"

    def __post_init__(self) -> None:
        if not self.record_id:
            ident = self.identity.key() if isinstance(self.identity, EventIdentity) else ""
            self.record_id = f"{self.run_id}:{ident}" if self.run_id else ident

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Event:
        return cls(**{**data, "identity": EventIdentity(**data["identity"])})


@dataclass
class Alignment:
    status: str
    left_key: str | None = None
    right_key: str | None = None
    note: str | None = None

    def __post_init__(self) -> None:
        _require_enum("alignment status", self.status, ALIGNMENT_STATUSES)


@dataclass
class Observation:
    observation_id: str
    reference_trace: str
    comparison_trace: str
    edit_id: str
    premise_id: str
    event_pair: list[str]
    outcome: str
    raw_values: list[str]
    alignment_ref: str
    rng_pair: str | None = None
    scan_state: str = "unknown"
    exhaustive: bool = False
    node_id: str = ""
    schema_version: int = SCHEMA_VERSION
    record_id: str = ""
    run_id: str = ""
    base_group_id: str = ""
    status: str = "ok"
    task_id: str = ""

    def __post_init__(self) -> None:
        if not self.record_id:
            self.record_id = self.observation_id
        _require_enum("outcome", self.outcome, OUTCOMES)
        _require_enum("scan_state", self.scan_state, SCAN_STATES)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Label:
    event_id: str
    premise_id: str
    task_label: int | None
    task_known: bool
    behavior_label: int | None
    behavior_known: bool
    noise_ref: float | None
    protocol_ref: str | None
    evidence_ids: list[str] = field(default_factory=list)
    opportunities: int = 0
    schema_version: int = SCHEMA_VERSION
    record_id: str = ""
    run_id: str = ""
    base_group_id: str = ""
    status: str = "ok"
    task_id: str = ""

    def __post_init__(self) -> None:
        if not self.record_id:
            self.record_id = f"{self.event_id}:{self.premise_id}"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Cost:
    prefill_tokens: int = 0
    decode_tokens: int = 0
    extra_prefill_tokens: int = 0
    elapsed_seconds: float = 0.0
    probe_seconds: float = 0.0
    scheduling_seconds: float = 0.0
    index_seconds: float = 0.0

    def __add__(self, other: Cost) -> Cost:
        return Cost(**{key: getattr(self, key) + getattr(other, key) for key in asdict(self)})


@dataclass
class Trace:
    id: str
    task_id: str
    base_group_id: str
    model: str
    seed: int
    text: str
    token_ids: list[int]
    offsets: list[list[int]]
    events: list[Event]
    answer: str | None
    correct: bool | None
    status: str = "ok"
    cost: Cost = field(default_factory=Cost)
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION
    record_id: str = ""
    run_id: str = ""

    def __post_init__(self) -> None:
        if not self.record_id:
            self.record_id = self.id

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Trace:
        allowed = set(cls.__dataclass_fields__)
        extra = {key: value for key, value in data.items() if key not in allowed}
        payload = {key: value for key, value in data.items() if key in allowed}
        meta = dict(payload.get("metadata") or {})
        meta.update(extra)
        payload["metadata"] = meta
        payload["events"] = [Event.from_dict(e) if not isinstance(e, Event) else e for e in payload.get("events", [])]
        if isinstance(payload.get("cost"), dict):
            payload["cost"] = Cost(**payload["cost"])
        return cls(**payload)


@dataclass
class Edit:
    id: str
    base_task_id: str
    changed_premise_ids: list[str]
    task: Task
    kind: str = "value"
    before: dict[str, str] = field(default_factory=dict)
    after: dict[str, str] = field(default_factory=dict)
    validity: str = "valid"
    exhaustive: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION
    record_id: str = ""
    run_id: str = ""
    base_group_id: str = ""
    status: str = "ok"

    def __post_init__(self) -> None:
        if not self.record_id:
            self.record_id = self.id
        if not self.base_group_id:
            self.base_group_id = self.task.base_group_id

    @property
    def premise_id(self) -> str:
        return self.changed_premise_ids[0] if self.changed_premise_ids else ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Edit:
        return cls(**{**data, "task": Task.from_dict(data["task"])})


def finite_or_none(value: float | None) -> float | None:
    return value if value is not None and math.isfinite(value) else None
