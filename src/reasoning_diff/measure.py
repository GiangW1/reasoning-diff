"""Task/behavior labels, S/M densities, noise, TO/CSP, and cone checks."""
from __future__ import annotations

from typing import Iterable

import numpy as np

from .events import align_events
from .graphs import behavior_mask, dirty_cone, oracle_mask
from .schema import Event, Label, Observation, Trace, finite_or_none


def compare_pair(base: Event, changed: Event, structural: bool = False, aligned: bool = True) -> str:
    if not aligned:
        return "unaligned"
    if structural:
        return "structural"
    return "changed" if base.value != changed.value else "no_change"


def _is_sham(obs: Observation) -> bool:
    return (obs.rng_pair or "").startswith("sham:")


def _event_key(obs: Observation) -> str:
    return obs.alignment_ref or obs.node_id or (obs.event_pair[0] if obs.event_pair else "")


def _label_node_id(event_id: str, node_id: str | None, ancestors: dict[str, set[str]]) -> str:
    if event_id in ancestors:
        return event_id
    if node_id and node_id in ancestors:
        return node_id
    try:
        import json

        body = json.loads(event_id)
        ent = body.get("entity_or_expression")
        if ent and ent in ancestors:
            return ent
    except (TypeError, ValueError, json.JSONDecodeError):
        pass
    return node_id or event_id


def build_labels(
    observations: Iterable[Observation],
    task_ancestors: dict[str, set[str]],
    sham_protocol: dict | None = None,
) -> list[Label]:
    # Materialize once: callers may pass a generator.  Re-iterating a
    # generator silently drops sham observations and changes noise labels.
    observations = list(observations)
    rows = []
    grouped: dict[tuple[str, str, str], list[Observation]] = {}
    for obs in observations:
        # New traces carry an explicit task/base key.  Legacy fixtures often
        # do not; keep their historical event/premise grouping for backwards
        # compatibility instead of using reference_trace as an implicit task
        # identity (which splits real/sham rows that belong together).
        task_key = obs.task_id or obs.base_group_id or ""
        grouped.setdefault((task_key, _event_key(obs), obs.premise_id), []).append(obs)
    for (task_key, event_id, premise_id), items in grouped.items():
        node_id = next((item.node_id for item in items if item.node_id), None)
        graph_id = _label_node_id(event_id, node_id, task_ancestors)
        known_task = graph_id in task_ancestors
        task_pos = known_task and premise_id in task_ancestors.get(graph_id, set())
        real = [i for i in items if not _is_sham(i)]
        positives = [i for i in real if i.outcome == "changed"]
        known_negatives = [
            i
            for i in real
            if i.outcome == "no_change"
            and i.scan_state in {"observed_response", "no_response_observed_in_scan"}
        ]
        if positives:
            behavior, known_b = 1, True
        elif known_negatives:
            behavior, known_b = 0, True
        else:
            behavior, known_b = None, False
        rows.append(
            Label(
                event_id=event_id,
                premise_id=premise_id,
                task_label=1 if known_task and task_pos else (0 if known_task else None),
                task_known=known_task,
                behavior_label=behavior,
                behavior_known=known_b,
                noise_ref=None,
                protocol_ref=None if sham_protocol is None else sham_protocol.get("name"),
                evidence_ids=[i.observation_id for i in real],
                opportunities=len(positives) + len(known_negatives),
                task_id=items[0].task_id,
                base_group_id=items[0].base_group_id,
            )
        )
    sham_by_event: dict[tuple[str, str], list[Observation]] = {}
    for obs in observations:
        if _is_sham(obs):
            task_key = obs.task_id or obs.base_group_id or ""
            sham_by_event.setdefault((task_key, _event_key(obs)), []).append(obs)
    for row in rows:
        task_key = row.task_id or row.base_group_id
        shams = sham_by_event.get((task_key, row.event_id), [])
        if not shams and not task_key:
            # Legacy observations have no task key.  Match their sham by
            # event, while keyed observations remain isolated per task.
            shams = [
                item
                for (sham_task, sham_event), items in sham_by_event.items()
                if sham_event == row.event_id
                for item in items
            ]
        if sham_protocol is None or not shams:
            row.noise_ref = None
        elif str(row.premise_id).startswith("sham:"):
            row.noise_ref = 1.0 if any(item.outcome == "changed" for item in shams) else 0.0
            row.evidence_ids = list(row.evidence_ids) + [item.observation_id for item in shams]
        else:
            row.noise_ref = None
    return rows


def dependency_densities(
    premises: Iterable[str] | None = None,
    task_set: Iterable[str] | None = None,
    behavior_set: Iterable[str] | None = None,
    noise_set: Iterable[str] | None = None,
    sham_protocol: dict | None = None,
    noise_evaluated: bool | None = None,
    behavior_unknown: bool = False,
    task: np.ndarray | None = None,
    behavior: np.ndarray | None = None,
    noise: np.ndarray | None = None,
    support: np.ndarray | None = None,
    event_sets: list[dict] | None = None,
) -> dict:
    """S = B\\T, M = T\\B. Empty denominator or missing sham protocol → null excess."""
    if event_sets is not None:
        rows = [
            dependency_densities(
                premises=item.get("premises", premises),
                task_set=item.get("task_set", task_set),
                behavior_set=item.get("behavior_set", behavior_set),
                noise_set=item.get("noise_set", noise_set),
                sham_protocol=item.get("sham_protocol", sham_protocol),
                noise_evaluated=item.get("noise_evaluated"),
                behavior_unknown=bool(item.get("behavior_unknown")),
            )
            for item in event_sets
        ]
        out = {"events": rows, "aggregation": "mean_over_events"}
        for key in ("rho_S_raw", "rho_M_raw", "rho_S_noise", "rho_M_noise", "rho_S_excess", "rho_M_excess"):
            values = [row[key] for row in rows if row.get(key) is not None]
            out[key] = float(np.mean(values)) if values else None
        return out
    if task is not None:
        return _matrix_densities(task, behavior, noise, support)
    P = set(premises or [])
    T = set(task_set or [])
    B = set(behavior_set or [])
    S = B - T
    M = set() if behavior_unknown else (T - B)
    denom_s = P - T
    denom_m = T
    rho_s = (len(S) / len(denom_s)) if denom_s else None
    rho_m = None if behavior_unknown else ((len(M) / len(denom_m)) if denom_m else None)
    if sham_protocol is None or noise_set is None:
        noise_s = None
        noise_m = None
        excess_s = None
        excess_m = None
        reason = "sham_protocol_missing" if sham_protocol is None else "noise_set_missing"
    elif isinstance(noise_set, (list, set, tuple)) and len(list(noise_set)) == 0 and not noise_evaluated:
        noise_s = None
        noise_m = None
        excess_s = None
        excess_m = None
        reason = "noise_set_empty"
    else:
        N = set(noise_set)
        noise_s = (len(N - T) / len(denom_s)) if denom_s else None
        noise_m = (len(T - N) / len(denom_m)) if denom_m else None
        excess_s = None if rho_s is None or noise_s is None else rho_s - noise_s
        excess_m = None if rho_m is None or noise_m is None else rho_m - noise_m
        reason = None
    if behavior_unknown:
        noise_m = None
        excess_m = None
    return {
        "S": sorted(S),
        "M": sorted(M),
        "rho_S_raw": finite_or_none(rho_s),
        "rho_M_raw": finite_or_none(rho_m),
        "rho_S_noise": finite_or_none(noise_s),
        "rho_M_noise": finite_or_none(noise_m),
        "rho_S_excess": finite_or_none(excess_s),
        "rho_M_excess": finite_or_none(excess_m),
        "behavior_unknown": behavior_unknown,
        "denominator_S": len(denom_s) or None,
        "denominator_M": len(denom_m) or None,
        "null_reason": reason,
        "interpretation": "signed descriptive excess on evaluated common support; M is empirical",
    }


def _matrix_densities(task, behavior, noise, support) -> dict:
    task = np.asarray(task, dtype=float)
    behavior = np.asarray(behavior, dtype=float)
    noise_missing = noise is None
    noise = np.full(task.shape, np.nan) if noise is None else np.asarray(noise, dtype=float)
    binary = lambda arr: np.isfinite(arr) & ((arr == 0) | (arr == 1))
    known = binary(task) & binary(behavior)
    support = known if support is None else np.asarray(support, dtype=bool) & known
    noise_ok = binary(noise)
    result = {"events": [], "support_cells": int(support.sum()), "null_reason": "noise_missing" if noise_missing else None}
    for i in range(task.shape[0]):
        row = {}
        for name, eligible in (("S", task[i] == 0), ("M", task[i] == 1)):
            mask = support[i] & eligible
            total_eligible = int(eligible.sum())
            denominator = int(mask.sum())
            raw = float(((behavior[i] == (1 if name == "S" else 0)) & mask).sum() / denominator) if denominator else None
            noise_mask = mask & noise_ok[i]
            if noise_missing or int(noise_mask.sum()) == 0:
                ref = None
            else:
                ref = float(((noise[i] == (1 if name == "S" else 0)) & noise_mask).sum() / int(noise_mask.sum()))
            excess = None if raw is None or ref is None else raw - ref
            row[name] = {
                "raw": raw,
                "noise": ref,
                "excess": excess,
                "denominator": denominator,
                "eligible": total_eligible,
                "coverage": denominator / total_eligible if total_eligible else None,
            }
        result["events"].append(row)
    for name in ("S", "M"):
        for kind in ("raw", "noise", "excess"):
            values = [row[name][kind] for row in result["events"] if row[name][kind] is not None]
            result[f"rho_{name}_{kind}"] = float(np.mean(values)) if values else None
    result["interpretation"] = "signed descriptive excess on evaluated common support; M is empirical"
    if not noise_missing and result["rho_S_noise"] is None and result["rho_M_noise"] is None:
        result["null_reason"] = "noise_set_missing"
    return result


def lcs_overlap(left: list, right: list) -> float | None:
    if not left and not right:
        return None
    if len(left) < len(right):
        left, right = right, left
    previous = [0] * (len(right) + 1)
    for item in left:
        current = [0]
        for j, other in enumerate(right, 1):
            current.append(previous[j - 1] + 1 if item == other else max(previous[j], current[-1]))
        previous = current
    return 2 * previous[-1] / (len(left) + len(right))


def _known_parents(event: Event) -> bool:
    if event.task_parents is None:
        return False
    if event.task_parents == [] and event.graph_status != "complete":
        return False
    return True


def probe_prf1(pred: Iterable[int], gold: Iterable[int]) -> dict:
    pred_set = {i for i, v in enumerate(pred) if v == 1}
    gold_set = {i for i, v in enumerate(gold) if v == 1}
    tp = len(pred_set & gold_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    f1 = None if precision is None or recall is None or (precision + recall) == 0 else 2 * precision * recall / (precision + recall)
    return {"precision": precision, "recall": recall, "f1": f1, "tp": tp, "fp": fp, "fn": fn}


def preservation_to_csp(base: Trace, changed: Trace, edited_premises: set[str], noise_pair: tuple[Trace, Trace] | None = None) -> dict:
    aligned = align_events(base.events, changed.events)
    clean_base = [
        e for e in base.events if _known_parents(e) and not edited_premises.intersection(e.task_parents or [])
    ]
    clean = [
        (a, b)
        for a, b in aligned["pairs"]
        if _known_parents(a) and not edited_premises.intersection(a.task_parents or [])
    ]
    dirty = [
        (a, b)
        for a, b in aligned["pairs"]
        if _known_parents(a) and edited_premises.intersection(a.task_parents or [])
    ]

    def token_region(trace, events):
        if not trace.token_ids or not trace.offsets:
            return []
        return [
            token
            for token, (a, b) in zip(trace.token_ids, trace.offsets, strict=True)
            if any(e.start <= a < b <= e.end for e in events)
        ]

    def facet(predicate):
        left = [e for e in base.events if predicate(e)]
        right = [e for e in changed.events if predicate(e)]
        if not left and not right:
            return None
        return lcs_overlap(
            token_region(base, left) or [e.value for e in left],
            token_region(changed, right) or [e.value for e in right],
        )

    return {
        "csp": sum(a.value == b.value for a, b in clean) / len(clean) if clean else None,
        "clean_alignment_coverage": len(clean) / len(clean_base) if clean_base else None,
        "clean_matched": len(clean),
        "clean_total": len(clean_base),
        "dirty_change_rate": sum(a.value != b.value for a, b in dirty) / len(dirty) if dirty else None,
        "added": len(aligned["added"]),
        "removed": len(aligned["removed"]),
        "to_all": lcs_overlap(base.token_ids, changed.token_ids),
        "to_clean": lcs_overlap(token_region(base, [a for a, _ in clean]), token_region(changed, [b for _, b in clean])),
        "to_correct": facet(lambda e: e.correct is True),
        "to_incorrect": facet(lambda e: e.correct is False),
        "to_noise": None if noise_pair is None else lcs_overlap(noise_pair[0].token_ids, noise_pair[1].token_ids),
        "csp_noise": None if noise_pair is None else preservation_to_csp(noise_pair[0], noise_pair[1], edited_premises).get("csp"),
    }


def _mapped_noise_hits(premises: list[str], labels) -> list[str]:
    return [
        lab.premise_id
        for lab in labels
        if lab.noise_ref == 1.0 and lab.premise_id in premises and not str(lab.premise_id).startswith("sham:")
    ]


def _unmapped_noise_hits(premises: list[str], labels) -> bool:
    return any(
        lab.noise_ref == 1.0
        and (
            not lab.premise_id
            or str(lab.premise_id).startswith("sham:")
            or lab.premise_id not in premises
        )
        for lab in labels
    )


def _has_sham_row(labels) -> bool:
    return any(str(lab.premise_id).startswith("sham:") for lab in labels)


def _fallback_noise_set(premises: list[str], labels, sham_protocol: dict | None):
    if sham_protocol is None:
        return None
    if _has_sham_row(labels) or _unmapped_noise_hits(premises, labels):
        return None
    mapped = _mapped_noise_hits(premises, labels)
    if mapped:
        return mapped
    return None


def _fallback_noise_evaluated(premises: list[str], labels, sham_protocol: dict | None, observed: bool) -> bool:
    if not observed or sham_protocol is None or _has_sham_row(labels):
        return False
    return not _unmapped_noise_hits(premises, labels)


def _density_null(reason: str) -> dict:
    return {
        "S": [],
        "M": [],
        "rho_S_raw": None,
        "rho_M_raw": None,
        "rho_S_noise": None,
        "rho_M_noise": None,
        "rho_S_excess": None,
        "rho_M_excess": None,
        "behavior_unknown": True,
        "denominator_S": None,
        "denominator_M": None,
        "null_reason": reason,
        "interpretation": "signed descriptive excess on evaluated common support; M is empirical",
    }


def event_density_sets(task, labels, sham_protocol: dict | None = None) -> dict:
    from .graphs import ancestors

    if getattr(task, "graph_status", None) == "unknown" or getattr(task, "graph_kind", None) in {"none"}:
        return _density_null("task_graph_unknown")
    if not any(getattr(lab, "task_known", False) for lab in labels):
        return _density_null("task_truth_unknown")
    anc = ancestors(task) if task.nodes else {}
    for premise in task.premises:
        if premise.kind not in {"placeholder", "spec"} and premise.premise_id:
            anc.setdefault(premise.premise_id, {premise.premise_id})
    premises = [p.premise_id for p in task.premises if p.kind not in {"placeholder", "spec"}]
    event_ids = sorted({lab.event_id for lab in labels if lab.event_id})
    event_sets = []
    for event_id in event_ids:
        ev_labs = [lab for lab in labels if lab.event_id == event_id]
        hits = [lab.premise_id for lab in ev_labs if lab.noise_ref == 1.0 and lab.premise_id]
        sham_hits = [h for h in hits if str(h).startswith("sham:")]
        real_hits = [h for h in hits if h in premises and not str(h).startswith("sham:")]
        observed = any(lab.noise_ref is not None for lab in ev_labs)
        known = {lab.premise_id for lab in ev_labs if lab.behavior_known and lab.premise_id in premises}
        positives = {lab.premise_id for lab in ev_labs if lab.behavior_label == 1 and lab.premise_id in premises}
        node_guess = next((lab.event_id for lab in ev_labs if lab.event_id in anc), event_id)
        task_set = set(anc.get(_label_node_id(event_id, node_guess, anc), set()))
        if sham_protocol is None:
            noise_set = None
            evaluated = False
        elif _has_sham_row(ev_labs) or sham_hits:
            noise_set = None
            evaluated = False
        elif not observed:
            noise_set = []
            evaluated = False
        elif real_hits:
            noise_set = real_hits
            evaluated = True
        else:
            noise_set = None
            evaluated = False
        event_sets.append(
            {
                "premises": premises,
                "task_set": sorted(task_set),
                "behavior_set": sorted(positives),
                "noise_set": noise_set,
                "noise_evaluated": evaluated,
                "sham_protocol": sham_protocol,
                "behavior_unknown": not known or (bool(task_set) and not task_set <= known),
            }
        )
    if not event_sets:
        observed = any(lab.noise_ref is not None for lab in labels)
        known = {lab.premise_id for lab in labels if lab.behavior_known and lab.premise_id in premises}
        task_set = anc.get(task.target) if task.target in anc else set()
        return dependency_densities(
            premises=premises,
            task_set=task_set,
            behavior_set={lab.premise_id for lab in labels if lab.behavior_label == 1 and lab.premise_id in premises},
            sham_protocol=sham_protocol,
            noise_set=_fallback_noise_set(premises, labels, sham_protocol),
            noise_evaluated=_fallback_noise_evaluated(premises, labels, sham_protocol, observed),
            behavior_unknown=not known or (bool(task_set) and not set(task_set) <= known),
        )
    return dependency_densities(event_sets=event_sets)


def joint_edit_counterexample(f, singles, joint) -> dict:
    """f(x,y)=xy at (0,0): single edits stay 0, joint (1,1) changes. Blocks soundness claims."""
    single_changed = [f(*args) != f(*origin) for origin, args in singles]
    joint_changed = f(*joint[1]) != f(*joint[0])
    return {
        "single_point_unchanged": not any(single_changed),
        "joint_changed": joint_changed,
        "soundness_claim_allowed": False,
        "reason": "single-point scan does not prove arbitrary joint-edit soundness",
    }


def cone_bundle(task, changed_premises: set[str], predicted: dict[str, set[str]] | None = None) -> dict:
    return {
        "cone": sorted(dirty_cone(task, changed_premises, predicted or None)),
        "oracle_mask": oracle_mask(task, changed_premises),
        "behavior_mask": behavior_mask(predicted or {}, changed_premises),
    }
