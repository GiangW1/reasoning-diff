"""A separate conditional-response experiment on fixed natural assignment prefixes."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction

from .events import assign_event_regions, parse_events
from .graphs import ancestors
from .io import digest
from .models.generate import task_prompt
from .next_round import base_trajectories, registered_pilot_edits, scan_edits
from .schema import Task

PROTOCOL = "shared_prefix_assignment_v1"
ESTIMAND = "numeric_assignment_response_conditional_on_fixed_pre_value_history"
SEEDS = (0, 1, 2)
SAMPLING = {"temperature": 0.6, "top_k": 20, "top_p": 0.95}


def make_plan(trace_rows, task_rows):
    """Select anchors before any continuation outcomes; retain unusable anchors."""
    if len({t["id"] for t in trace_rows}) != len(trace_rows):
        raise ValueError("duplicate source trace IDs")
    unique = {}
    for task in task_rows:
        if task["task_id"] in unique and unique[task["task_id"]] != task:
            raise ValueError("conflicting source task records")
        unique[task["task_id"]] = task
    tasks = {t["task_id"]: Task.from_dict(t) for t in task_rows}
    bases = base_trajectories(trace_rows, task_rows)
    if not bases:
        raise ValueError("no saved natural base trajectories")
    anchors, sources, variants = [], [], {}
    for row in bases:
        task, meta = tasks[row["task_id"]], row.get("metadata") or {}
        if (task.answer_spec.kind != "numeric" or task.metadata.get("premise_protocol") != "sentence_graph_v1"
                or task.metadata.get("trajectory_protocol", "natural") != "natural"
                or meta.get("trajectory_protocol", "natural") != "natural"):
            raise ValueError("shared prefixes require natural numeric sentence-graph source traces")
        prompt = meta.get("rendered_prompt_text")
        if not isinstance(prompt, str) or not row["text"].startswith(prompt) or meta.get("rendered_prompt_char_len") != len(prompt):
            raise ValueError("source rendered prompt boundary is not authenticated")
        if prompt.count(task_prompt(task)) != 1 or meta.get("enable_thinking") is not True:
            raise ValueError("source question/template or thinking mode is incompatible")
        body = row["text"][len(prompt):]
        events = assign_event_regions(parse_events(body, task), body, initial_thinking=True)
        eligible = [e for e in events if e.event_region == "thinking" and e.event_kind != "restatement"]
        sources.append({"trace_id": row["id"], "task_id": task.task_id, "problem_id": task.base_group_id,
                        "op": task.metadata.get("op", len(task.nodes)), "eligible_anchors": len(eligible)})
        graph = ancestors(task)
        for index, event in enumerate(eligible):
            reasons = []
            if event.status != "ok":
                reasons.append("ambiguous_source_event")
            if meta.get("boundary_status") != "ok":
                reasons.append("source_boundary_failed")
            if meta.get("finalizer_used") or meta.get("thinking_forced_close"):
                reasons.append("forced_source_trajectory")
            anchors.append({"id": digest([PROTOCOL, row["id"], event.identity.key(), event.start, event.value_start]),
                            "source_trace_id": row["id"], "source_seed": row.get("seed"), "task_id": task.task_id,
                            "problem_id": task.base_group_id, "op": task.metadata.get("op", len(task.nodes)),
                            "event_key": event.identity.key(), "node_id": event.node_id, "event_start": event.start,
                            "history": body[:event.value_start], "history_hash": digest(body[:event.value_start]),
                            "rendered_prompt": prompt, "source_model": row.get("model"), "source_revision": meta.get("revision"),
                            "source_usable": not reasons, "source_failures": reasons, "pilot": index == 0,
                            "task_ancestors": sorted(graph.get(event.node_id, set()))})
        base_id = "base:" + task.task_id
        if base_id not in variants:
            variants[base_id] = {"id": base_id, "task_id": task.task_id, "kind": "base", "task": task.to_dict()}
            for edit in scan_edits(task, len(SEEDS)):
                variants[edit.id] = {"id": edit.id, "task_id": task.task_id, "kind": "edit", "task": edit.task.to_dict(),
                                     "premise_id": edit.changed_premise_ids[0], "seed": edit.metadata["rng_seed"]}
    return {"protocol": PROTOCOL, "estimand": ESTIMAND, "anchors": anchors, "sources": sources,
            "variants": list(variants.values()), "tasks": [tasks[tid].to_dict() for tid in sorted({r['task_id'] for r in bases})]}


def requests_for(plan, phase):
    if phase not in {"pilot", "scan"}:
        raise ValueError("unknown shared-prefix phase")
    tasks = {t["task_id"]: Task.from_dict(t) for t in plan["tasks"]}
    pilot_edits = {tid: {e.id for e in registered_pilot_edits(task)} for tid, task in tasks.items()}
    by_task = defaultdict(list)
    for variant in plan["variants"]:
        by_task[variant["task_id"]].append(variant)
    requests = []
    for anchor in plan["anchors"]:
        if phase == "pilot" and not anchor["pilot"]:
            continue
        for variant in by_task[anchor["task_id"]]:
            if phase == "pilot" and variant["kind"] == "edit" and variant["id"] not in pilot_edits[anchor["task_id"]]:
                continue
            for seed in SEEDS if variant["kind"] == "base" else (variant["seed"],):
                requests.append({"id": digest([PROTOCOL, anchor["id"], variant["id"], seed]), "anchor_id": anchor["id"],
                                 "variant_id": variant["id"], "kind": variant["kind"], "seed": seed,
                                 "premise_id": variant.get("premise_id")})
    return requests


def prefix_text(anchor, task, variant):
    original, edited = task_prompt(task), task_prompt(variant)
    if anchor["rendered_prompt"].count(original) != 1 or digest(anchor["history"]) != anchor["history_hash"]:
        raise ValueError("anchor prompt/history mismatch")
    return anchor["rendered_prompt"].replace(original, edited, 1) + anchor["history"]


def first_boundary(text):
    """A complete first line or thinking close, never an unfinished digit token."""
    ends = [text.find(marker) for marker in ("\n", "</think>") if marker in text]
    return min(ends) if ends else None


def read_response(anchor, task, continuation, stop_reason):
    end = first_boundary(continuation)
    if end is None and stop_reason != "eos":
        return {"status": "budget_exhausted", "value": None}
    line = continuation if end is None else continuation[:end]
    body = anchor["history"] + line
    events = assign_event_regions(parse_events(body, task), body, initial_thinking=True)
    # The fixed assignment head, not a later occurrence or an agreeing value,
    # identifies the response. Values already in the history cannot count.
    candidates = [e for e in events if e.start == anchor["event_start"] and e.node_id == anchor["node_id"]
                  and e.value_start >= len(anchor["history"]) and e.status == "ok" and e.event_region == "thinking"]
    if len(candidates) != 1:
        return {"status": "unparseable_assignment", "value": None}
    event = candidates[0]
    try:
        Fraction(event.value)
    except (ValueError, ZeroDivisionError):
        return {"status": "unparseable_assignment", "value": None}
    return {"status": "observed", "value": event.value, "response_span": [event.value_start, event.end],
            "response_text": event.text}


def run_request(request, anchor, task, variant, packed, max_new, decode):
    """Retokenize the exact character cut; never include a straddling value token."""
    import time
    import torch
    from .models.adapters import model_device

    result = {"request": request, "protocol": PROTOCOL, "estimand": ESTIMAND, "history_hash": anchor["history_hash"],
              "status": "source_unusable", "value": None, "generated_ids": [], "prefix_ids": [], "sampling": SAMPLING}
    if not anchor["source_usable"]:
        result["source_failures"] = anchor["source_failures"]
        return result
    info = packed["card"]
    if (anchor["source_model"] != info["id"] or anchor["source_revision"] != info["revision"]):
        raise ValueError("continuation model/revision differs from the source trace")
    tokenizer, model = packed["tokenizer"], packed["model"]
    prefix = prefix_text(anchor, task, variant)
    ids = tokenizer.encode(prefix, add_special_tokens=False)
    result.update(prefix_ids=ids, prefix_hash=digest(prefix), prefix_token_hash=digest(ids))
    if tokenizer.decode(ids, skip_special_tokens=False) != prefix:
        result["status"] = "prefix_roundtrip_failed"
        return result
    budget = min(max_new, int(info["context_limit"]) - len(ids))
    result["requested_max_new"], result["effective_max_new"] = max_new, max(0, budget)
    if budget < 1:
        result["status"] = "context_exhausted"
        return result
    generator = torch.Generator(device=model_device(model)).manual_seed(request["seed"])
    def stopped(produced):
        # Only look for a terminator here; verify the exact full prefix once
        # after decoding instead of repeatedly decoding a long fixed history.
        return first_boundary(tokenizer.decode(produced, skip_special_tokens=False)) is not None
    started = time.perf_counter()
    decoded = decode(model, ids, generator, max_new=budget, eos_id=tokenizer.eos_token_id,
                     stop_condition=stopped, **SAMPLING)
    produced = decoded["generated_ids"]
    # Keep EOS in the replay record, remove only the actual final EOS ID for
    # parsing. An arbitrary textual special token is not silently removed.
    content = produced[:-1] if produced and produced[-1] == tokenizer.eos_token_id else produced
    full_text = tokenizer.decode(ids + content, skip_special_tokens=False)
    result.update(generated_ids=produced, stop_reason=decoded["stop_reason"],
                  elapsed_seconds=time.perf_counter() - started, batch_execution=decoded.get("batch_execution"),
                  prefill_tokens=len(ids), decode_tokens=len(produced))
    if not full_text.startswith(prefix):
        result["status"] = "continuation_boundary_failed"
        return result
    continuation = full_text[len(prefix):]
    result.update(continuation=continuation, **read_response(anchor, task, continuation, decoded["stop_reason"]))
    return result


def summarize(plan, requests, results, phase):
    """Paired local responses; invalid/missing draws remain in every denominator."""
    expected = {r["id"]: r for r in requests}
    if len(expected) != len(requests):
        raise ValueError("duplicate request IDs")
    actual = {}
    anchors = {a["id"]: a for a in plan["anchors"]}
    for result in results:
        request = result["request"]
        if request["id"] in actual or expected.get(request["id"]) != request or result.get("protocol") != PROTOCOL:
            raise ValueError("duplicate, unexpected or mixed-condition response")
        if result.get("history_hash") != anchors[request["anchor_id"]]["history_hash"]:
            raise ValueError("responses do not share the registered history")
        if (result["status"] == "observed") != (result.get("value") is not None):
            raise ValueError("response status/value disagree")
        actual[request["id"]] = result
    bases = {(r["anchor_id"], r["seed"]): actual.get(r["id"]) for r in requests if r["kind"] == "base"}
    contrasts = []
    def observed(row):
        return row is not None and row["status"] == "observed"
    for request in requests:
        if request["kind"] != "edit":
            continue
        anchor = anchors[request["anchor_id"]]
        edited, base = actual.get(request["id"]), bases.get((anchor["id"], request["seed"]))
        controls = [bases.get((anchor["id"], seed)) for seed in SEEDS if seed != request["seed"]]
        paired = observed(base) and observed(edited)
        common = paired and all(observed(control) for control in controls)
        raw = int(base["value"] != edited["value"]) if paired else None
        noise = sum(base["value"] != control["value"] for control in controls) / len(controls) if common else None
        contrasts.append({"request_id": request["id"], "anchor_id": anchor["id"], "source_trace_id": anchor["source_trace_id"],
                          "problem_id": anchor["problem_id"], "op": anchor["op"], "node_id": anchor["node_id"],
                          "premise_id": request["premise_id"], "seed": request["seed"],
                          "task_dependency": request["premise_id"] in anchor["task_ancestors"],
                          "paired": paired, "common_support": common, "response": raw, "noise": noise,
                          "excess": raw - noise if common else None,
                          "base_status": base["status"] if base else "missing",
                          "edit_status": edited["status"] if edited else "missing",
                          "noise_statuses": [c["status"] if c else "missing" for c in controls]})

    def stats(rows):
        n, paired, common = len(rows), sum(r["paired"] for r in rows), [r for r in rows if r["common_support"]]
        non_task = [r for r in common if not r["task_dependency"]]
        non_task_all = [r for r in rows if not r["task_dependency"]]
        non_task_paired = sum(r["paired"] for r in non_task_all)
        return {"planned_comparisons": n, "paired_comparisons": paired, "common_comparisons": len(common),
                "paired_coverage": paired / n if n else 0, "common_noise_coverage": len(common) / n if n else 0,
                "mean_excess_on_common_support": sum(r["excess"] for r in common) / len(common) if common else None,
                "non_task_planned_comparisons": len(non_task_all), "non_task_paired_comparisons": non_task_paired,
                "non_task_common_comparisons": len(non_task),
                "non_task_paired_coverage": non_task_paired / len(non_task_all) if non_task_all else 0,
                "non_task_common_noise_coverage": len(non_task) / len(non_task_all) if non_task_all else 0,
                "non_task_mean_excess_on_common_support": sum(r["excess"] for r in non_task) / len(non_task) if non_task else None}
    groups = {}
    for field in ("problem_id", "op", "source_trace_id"):
        grouped = defaultdict(list)
        for row in contrasts:
            grouped[str(row[field])].append(row)
        groups[field] = {key: stats(rows) for key, rows in sorted(grouped.items())}
    overall = stats(contrasts)
    strata = [overall, *[row for group in groups.values() for row in group.values()]]
    checks = {"every_source_has_anchor": bool(plan["sources"]) and all(s["eligible_anchors"] > 0 for s in plan["sources"]),
              "all_requests_recorded": len(actual) == len(expected),
              **{key: bool(contrasts) and all(r[key] >= 0.5 for r in strata) for key in
                 ("paired_coverage", "common_noise_coverage", "non_task_paired_coverage", "non_task_common_noise_coverage")}}
    return {"protocol": PROTOCOL, "estimand": ESTIMAND, "phase": phase, "passed": all(checks.values()), "checks": checks,
            "overall": overall, "by_problem": groups["problem_id"], "by_op": groups["op"], "by_source_trace": groups["source_trace_id"],
            "response_statuses": dict(Counter(row["status"] for row in actual.values())), "missing_requests": len(expected) - len(actual),
            "contrasts": contrasts, "scientific_conclusion": None, "original_natural_matching_resolved": False,
            "aggregation": "equal_registered_edit_opportunities_on_common_support; descriptive_only",
            "inference_unit": "source_problem; shared_baselines_and_histories_are_not_independent",
            "not_evaluated": ["unconditional_trajectory_effect", "original_P1", "C1_probe", "C2_hidden_intervention", "P3", "C4"]}
