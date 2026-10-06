"""PR8 sentence-fact protocol and measurement checks (no model truth hints)."""
from __future__ import annotations

import ast
from collections import defaultdict
import math

from .edits import apply_value_edit, recompute
from .events import ALIGNMENT_POLICY, premise_aliases
from .graphs import ancestors
from .schema import Edit, EventIdentity, Label, Premise, Task


def select_dev_layer(layers, scores):
    if len(layers) != len(scores) or len(set(layers)) != len(layers):
        raise ValueError("dev layer IDs and scores must correspond uniquely")
    usable = [(float(score), -int(layer), int(layer)) for layer, score in zip(layers, scores)
              if score is not None and math.isfinite(float(score))]
    if not usable:
        raise ValueError("no finite dev behavior AUC; cannot select a layer")
    return max(usable)[2]


def _expression_text(expression, names):
    def render(node):
        if isinstance(node, ast.Expression):
            return render(node.body)
        if isinstance(node, ast.Name):
            return f"the number of {names[node.id]}"
        if isinstance(node, ast.Constant):
            return str(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return f"negative {render(node.operand)}"
        if isinstance(node, ast.BinOp):
            phrases = {ast.Add: "the sum of", ast.Sub: "the difference between", ast.Mult: "the product of"}
            phrase = phrases.get(type(node.op))
            if phrase:
                return f"({phrase} {render(node.left)} and {render(node.right)})"
        raise ValueError(f"unsupported sentence-fact expression: {expression}")
    return render(ast.parse(expression, mode="eval"))


def sentence_graph_task(task):
    """Explicit sentence premises, including rules and two irrelevant facts.

    This is a new project-derived condition; the original official question
    and template are retained in metadata. Implicit aggregate rules become
    explicit facts, so these results must not be pooled with PR7.
    """
    if task.metadata.get("premise_protocol") == "sentence_graph_v1":
        return task
    names = {p.premise_id: premise_aliases(p)[-1] for p in task.premises}
    names.update({n.id: next((a for a in n.aliases if a != n.id), n.id) for n in task.nodes})
    premises, sentences = [], []

    def add(pid, text, value, kind):
        start = len(" ".join(sentences)) + bool(sentences)
        premises.append(Premise(pid, text, start, start + len(text), value, kind))
        sentences.append(text)

    for p in task.premises:
        add(p.premise_id, f"The number of {names[p.premise_id]} equals {p.value}.", p.value, "definition")
    nodes = []
    for n in task.nodes:
        pid = f"relation_{n.id}"
        add(pid, f"The number of {names[n.id]} equals {_expression_text(n.expression, names)}.", n.expression, "relation")
        nodes.append({**n.__dict__, "parents": [*n.parents, pid], "aliases": list(dict.fromkeys([n.id, names[n.id]]))})
    for pid, name, value in (("unused_a", "unrelated blue lanterns", "17"), ("unused_b", "unrelated green ribbons", "9")):
        if pid in names:
            raise ValueError("sentence-fact distractor ID collision")
        add(pid, f"The number of {name} equals {value}.", value, "definition")
    question = " ".join(sentences) + f" What is the number of {names[task.target]}?"
    if task.answer_spec.mod is not None:
        question += f" All arithmetic is modulo {task.answer_spec.mod}."
    derived = Task.from_dict({**task.to_dict(), "question": question, "premises": [p.__dict__ for p in premises],
                              "nodes": nodes, "source_kind": "project_derived", "graph_kind": "sentence_fact_dag",
                              "metadata": {**task.metadata, "premise_protocol": "sentence_graph_v1", "names": names,
                                           "official_question": task.question, "official_task": task.to_dict()}})
    derived.validate()
    return recompute(derived)


def relation_edit(task, premise_id, repeat):
    premise = next(p for p in task.premises if p.premise_id == premise_id)
    if premise.kind != "relation":
        raise ValueError("relation edit requires a rule premise")
    owner = next(n for n in task.nodes if f"relation_{n.id}" == premise_id)
    # Nonzero shifts modulo 23; the sentence and expression change together.
    shift = repeat + 1
    expression = f"({owner.expression}) + {shift}"
    text = f"The number of {task.metadata['names'][owner.id]} equals {_expression_text(expression, task.metadata['names'])}."
    delta = len(text) - len(premise.text)
    premises = []
    for p in task.premises:
        body = dict(p.__dict__)
        if p.premise_id == premise_id:
            body.update(text=text, end=p.start + len(text), value=expression)
        elif p.start > premise.start:
            body.update(start=p.start + delta, end=p.end + delta)
        premises.append(body)
    tid = f"{task.task_id}::{premise_id}:shift{shift}"
    updated = Task.from_dict({**task.to_dict(), "task_id": tid, "record_id": tid, "variant_id": f"{premise_id}:shift{shift}",
                             "question": task.question[:premise.start] + text + task.question[premise.end:], "premises": premises,
                             "nodes": [{**n.__dict__, "expression": expression if n.id == owner.id else n.expression} for n in task.nodes]})
    updated = recompute(updated)
    updated.validate()
    return Edit(f"edit:{tid}", task.task_id, [premise_id], updated, kind="relation", before={premise_id: owner.expression},
                after={premise_id: expression}, validity="valid", metadata={"recomputed": True})


def scan_edits(task, repeats):
    edits = []
    for p in task.premises:
        if not p.value or p.kind == "placeholder":
            continue
        for repeat in range(repeats):
            if p.kind == "relation":
                edit = relation_edit(task, p.premise_id, repeat)
            else:
                candidates = [str(x) for x in range(23) if str(x) != p.value]
                edit = apply_value_edit(task, p.premise_id, candidates[repeat % len(candidates)])
            # Several values do not constitute an exhaustive legal-value scan.
            edit.exhaustive = False
            edit.metadata.update(rng_seed=repeat, perturbation_id=f"{p.premise_id}:{repeat}", scan_protocol="all_sentence_facts_v1")
            edits.append(edit)
    return edits


def registered_pilot_edits(task):
    sources = ancestors(task).get(task.target, set())
    relevant = next(p.premise_id for p in task.premises if p.kind != "relation" and p.premise_id in sources)
    chosen = {relevant, "unused_a", "unused_b"}
    return [edit for edit in scan_edits(task, 1) if edit.changed_premise_ids[0] in chosen]


def trace_labels(observations, tasks):
    """Behavior labels belong to the reference seed, not a pooled event ID."""
    owners = {t.task_id: t for t in tasks}
    grouped = defaultdict(list)
    for obs in observations:
        if not (obs.rng_pair or "").startswith("sham:") and obs.event_pair[0]:
            grouped[(obs.task_id, obs.reference_trace, obs.alignment_ref, obs.premise_id)].append(obs)
    rows = []
    for (tid, trace, event, premise), items in grouped.items():
        task = owners[tid]
        node = items[0].node_id
        graph = ancestors(task)
        graph.update({p.premise_id: {p.premise_id} for p in task.premises})
        known = [o for o in items if o.outcome in {"changed", "no_change"}]
        rows.append(Label(event, premise, int(premise in graph.get(node, set())) if node in graph else None,
                          node in graph, int(any(o.outcome == "changed" for o in known)) if known else None,
                          bool(known), None, "all_sentence_facts_v1", evidence_ids=[o.observation_id for o in known],
                          opportunities=len(known), task_id=tid, base_group_id=task.base_group_id, trace_id=trace,
                          record_id=f"label:{tid}:{trace}:{event}:{premise}"))
    return rows


def base_trajectories(traces, tasks):
    owners = {t["task_id"]: t for t in tasks}
    return [trace for trace in traces if trace.get("task_id") in owners
            and not owners[trace["task_id"]].get("edit_ref") and "::" not in trace["task_id"]
            and not any(kind in trace["id"] for kind in ("sham", "source"))]


def parser_coverage(traces, tasks):
    """DAG-variable coverage is a diagnostic, not annotated step recall."""
    owners = {t["task_id"]: Task.from_dict(t) for t in tasks}
    rows = []
    for trace in base_trajectories(traces, tasks):
        task = owners[trace["task_id"]]
        nodes = {node.id: node for node in task.nodes}
        required, pending = set(), [task.target]
        while pending:
            node_id = pending.pop()
            if node_id in nodes and node_id not in required:
                required.add(node_id)
                pending.extend(nodes[node_id].parents)
        parsed = {e["node_id"] for e in trace.get("events", []) if e.get("event_region") == "thinking"
                  and e.get("event_kind") != "restatement" and e.get("status", "ok") == "ok"}
        if (trace.get("metadata") or {}).get("boundary_status", "ok") != "ok":
            parsed = set()
        rows.append({"trace_id": trace["id"], "problem_id": task.base_group_id,
                     "op": task.metadata.get("op", len(task.nodes)), "required_nodes": len(required),
                     "parsed_required_nodes": len(required & parsed), "missing_nodes": sorted(required - parsed),
                     "variable_coverage": len(required & parsed) / len(required) if required else None,
                     "target_present": task.target in parsed})
    return rows


def trajectory_table(traces, tasks, observations, splits, scanned_premises=None):
    """One row per base trajectory. Missing attribution stays missing in ITT.

    Raw density is the mean changed fraction on observed non-task cells.
    Excess subtracts the matched event's base-seed variation on exactly those
    cells. This is a descriptive response-rate excess, not proof of a causal
    spurious dependency. Unaligned cells never become negative labels.
    """
    owners = {t["task_id"]: Task.from_dict(t) for t in tasks}
    roles = {r.get("base_group_id"): r["role"] for r in splits}
    real, noise = defaultdict(list), defaultdict(list)
    for o in observations:
        key = (o["reference_trace"], o.get("alignment_ref", ""))
        if o.get("outcome") not in {"changed", "no_change"} or o.get("boundary_status", "ok") == "failed":
            continue
        bucket = noise if (o.get("rng_pair") or "").startswith("sham:") else real
        bucket[key].append(o)
    result = []
    for trace in base_trajectories(traces, tasks):
        owner = owners[trace["task_id"]]
        graph = ancestors(owner)
        supported, noise_supported, noise_events, raw, excess = 0, 0, 0, [], []
        common_raw, common_noise = [], []
        graph.update({p.premise_id: {p.premise_id} for p in owner.premises})
        eligible = 0
        for event in trace.get("events", []):
            if (trace.get("metadata") or {}).get("boundary_status", "ok") != "ok":
                continue
            if event.get("event_region") != "thinking" or event.get("event_kind") == "restatement" or event.get("status", "ok") != "ok":
                continue
            key = (trace["id"], EventIdentity(**event["identity"]).key())
            non_task = {p.premise_id for p in owner.premises} - graph.get(event["node_id"], set())
            if scanned_premises is not None:
                non_task &= set(scanned_premises.get(owner.task_id, []))
            eligible += len(non_task)
            cells = defaultdict(list)
            for obs in real[key]:
                if obs["premise_id"] in non_task:
                    cells[obs["premise_id"]].append(obs["outcome"] == "changed")
            n = noise[key]
            if n:
                noise_events += 1
            rate = sum(o["outcome"] == "changed" for o in n) / len(n) if n else None
            event_raw, event_excess = [], []
            for values in cells.values():
                value = sum(values) / len(values)
                event_raw.append(value)
                supported += 1
                if rate is not None:
                    event_excess.append(value - rate)
                    noise_supported += 1
            if event_raw:
                raw.append(sum(event_raw) / len(event_raw))
                if len(event_excess) == len(event_raw):
                    excess.append(sum(event_excess) / len(event_excess))
                    common_raw.append(sum(event_raw) / len(event_raw))
                    common_noise.append(rate)
        meta = trace.get("metadata") or {}
        role = roles.get(owner.base_group_id)
        complete = trace.get("status") == "natural_complete"
        result.append({"analysis_unit": "trajectory", "density_protocol": "matched_cell_response_rate_excess_v1",
                       "head": "behavior", "position": "pre_step", "problem_id": owner.base_group_id,
                       "task_id": owner.task_id, "trace_id": trace["id"], "seed": trace.get("seed"),
                       "length": int(meta.get("generated_tokens", (trace.get("cost") or {}).get("decode_tokens", 0))),
                       "op": owner.metadata.get("op", len(owner.nodes)), "rho_raw": sum(raw) / len(raw) if raw else None,
                       "rho": sum(excess) / len(excess) if excess and len(excess) == len(raw) else None,
                       "rho_missing_reason": None if raw and len(excess) == len(raw) else "missing_matched_support_or_noise",
                       "support_cells": supported, "eligible_cells": eligible,
                       "noise_supported_cells": noise_supported, "noise_support_events": noise_events,
                       "observed_events": len(raw), "aggregation": "mean_over_observed_events",
                       # Expose partial common support without changing the
                       # registered rho, its missingness, or analysis gates.
                       "common_support_diagnostic": {
                           "status": "descriptive_only" if excess else "no_common_support",
                           "raw": sum(common_raw) / len(common_raw) if common_raw else None,
                           "noise": sum(common_noise) / len(common_noise) if common_noise else None,
                           "excess": sum(excess) / len(excess) if excess else None,
                           "events": len(excess), "observed_events": len(raw), "cells": noise_supported,
                           "event_coverage": len(excess) / len(raw) if raw else None,
                           "aggregation": "equal_event_weights_on_identical_edit_and_noise_support"},
                       "support_scope": "all_sentence_facts" if scanned_premises is None else "registered_pilot_facts",
                       "coverage": supported / eligible if eligible else None,
                       "y": int(complete and trace.get("correct") is True), "split": role,
                       "held_out": role == "test", "trace_status": trace.get("status"),
                       "failure_as_incorrect": not complete})
    return result


def measurement_report(traces, tasks, observations, splits, scanned_premises=None):
    """CPU-only prerequisites evaluated before feature collection or fitting."""
    table = trajectory_table(traces, tasks, observations, splits, scanned_premises)
    parsed = {row["trace_id"]: row for row in parser_coverage(traces, tasks)}
    strata = defaultdict(list)
    problems = defaultdict(list)
    for row in table:
        row.update(parsed[row["trace_id"]])
        strata[str(row["op"])].append(row)
        problems[row["problem_id"]].append(row)

    def summarize(rows):
        possible = sum(r["eligible_cells"] for r in rows)
        support = sum(r["support_cells"] for r in rows)
        noise = sum(r["noise_supported_cells"] for r in rows)
        coverage = [r["variable_coverage"] for r in rows if r["variable_coverage"] is not None]
        return {"n_traces": len(rows), "n_problems": len({r["problem_id"] for r in rows}),
                "eligible_cells": possible, "support_cells": support, "noise_supported_cells": noise,
                "matched_cell_coverage": support / possible if possible else 0,
                "common_noise_coverage": noise / possible if possible else 0,
                "rho_coverage": sum(r["rho"] is not None for r in rows) / len(rows) if rows else 0,
                "variable_coverage": sum(coverage) / len(coverage) if coverage else 0,
                "target_coverage": sum(r["target_present"] for r in rows) / len(rows) if rows else 0}

    overall = summarize(table)
    by_op = {op: summarize(rows) for op, rows in strata.items()}
    by_problem = {problem: summarize(rows) for problem, rows in problems.items()}
    groups = [overall, *by_op.values(), *by_problem.values()]
    checks = {"trajectory_rows_unique": bool(table) and len({r["trace_id"] for r in table}) == len(table)}
    for key in ("matched_cell_coverage", "common_noise_coverage", "rho_coverage", "variable_coverage", "target_coverage"):
        checks[key] = bool(table) and all(group[key] >= 0.5 for group in groups)
    checks["exact_boundaries"] = bool(table) and all(
        (trace.get("metadata") or {}).get("boundary_status") == "ok" for trace in base_trajectories(traces, tasks))
    failures = [key for key, value in checks.items() if not value]
    classes = {str(value): sum(r["y"] == value for r in table) for value in (0, 1)}
    return {"passed": not failures, "checks": checks, "failures": failures,
            "overall": overall, "by_op": by_op, "by_problem": by_problem, "trajectories": table,
            "matching_policy": ALIGNMENT_POLICY, "coverage_threshold": 0.5,
            "coverage_unit": "overall_and_each_problem_and_op",
            "parser_recall": "not_estimated_without_annotated_steps",
            "p1_estimability": {"status": "single_class" if not all(classes.values()) else "requires_held_out_classes",
                                 "class_counts": classes, "blocks_engineering_smoke": False},
            "scientific_conclusion": None}


def cached_paired_screen(traces, tasks, observations, splits):
    """Run the registered small screen on existing exact edit comparisons."""
    originals = [row for row in tasks if "::" not in row["task_id"] and not row.get("edit_ref")]
    base = base_trajectories(traces, tasks)
    by_task = defaultdict(list)
    for row in base:
        if row.get("seed") == 0:
            by_task[row["task_id"]].append(row)
    references, planned, scanned = [], [], {}
    for owner in originals:
        candidates = by_task[owner["task_id"]]
        if len(candidates) != 1:
            continue
        trace = candidates[0]
        references.append(trace)
        for edit in registered_pilot_edits(Task.from_dict(owner)):
            pid = edit.changed_premise_ids[0]
            planned.append((trace["id"], edit.id))
            scanned.setdefault(owner["task_id"], []).append(pid)
    selected, comparisons = [], defaultdict(set)
    reference_ids = {row["id"] for row in references}
    trace_ids = {row["id"]: row for row in base}
    for obs in observations:
        reference = obs["reference_trace"]
        if reference not in reference_ids:
            continue
        if (obs.get("rng_pair") or "").startswith("sham:"):
            donor = trace_ids.get(obs["comparison_trace"], {})
            if donor.get("seed") in (1, 2) and donor.get("task_id") == trace_ids[reference]["task_id"]:
                selected.append(obs)
        elif (reference, obs["edit_id"]) in planned:
            comparisons[reference, obs["edit_id"]].add(obs["comparison_trace"])
            selected.append(obs)
    report = measurement_report(references, originals, selected, splits, scanned)
    report["checks"]["unique_seed0_references"] = len(references) == len(originals) and bool(originals)
    report["checks"]["registered_edit_comparisons"] = bool(planned) and all(len(comparisons[key]) == 1 for key in planned)
    report["failures"] = [key for key, value in report["checks"].items() if not value]
    report["passed"] = not report["failures"]
    report["cache_coverage"] = {"planned_edits": len(planned), "cached_edits": sum(len(comparisons[key]) == 1 for key in planned),
                                "missing_edits": [list(key) for key in planned if not comparisons[key]],
                                "ambiguous_edits": [list(key) for key in planned if len(comparisons[key]) > 1]}
    report["pilot_protocol"] = {"edit_seed": 0, "noise_seeds": [1, 2], "scanned_premises": scanned,
                                "scope": "relevant_fact_and_two_distractors", "formal_evidence": False,
                                "generation_reused": True}
    return report


def smoke_report(traces, tasks, observations, event_rows, probes):
    base = base_trajectories(traces, tasks)
    complete = sum(t.get("status") == "natural_complete" for t in base) / max(len(base), 1)
    events = [e for t in base for e in t.get("events", []) if e.get("event_region") == "thinking"
              and e.get("event_kind") != "restatement" and e.get("status", "ok") == "ok"]
    originals = [t for t in tasks if "::" not in t["task_id"]]
    planned = {(t["task_id"], p["premise_id"]) for t in originals for p in t["premises"]}
    scanned = {(o["task_id"], o["premise_id"]) for o in observations if not (o.get("rng_pair") or "").startswith("sham:")}
    metrics = {r.get("head"): (r.get("metrics") or {}) for r in probes
               if r.get("position") == "pre_step" and "U" in r and not r.get("baseline")}
    checks = {"completion_rate": bool(base) and complete >= 0.5, "thinking_calculation_events": bool(events),
              "all_premises_scanned": bool(planned) and planned <= scanned, "collected_events": bool(event_rows),
              "exact_boundaries": all((t.get("metadata") or {}).get("boundary_status") == "ok" for t in base),
              "behavior_train_and_dev": all((metrics.get("behavior", {}).get(role) or {}).get("status") == "ok"
                                             for role in ("probe_train", "dev"))}
    return {"passed": all(checks.values()), "checks": checks, "failures": [k for k, v in checks.items() if not v],
            "base_traces": len(base), "completion_rate": complete, "thinking_calculation_events": len(events),
            "planned_facts": len(planned), "scanned_facts": len(planned & scanned),
            "threshold_note": "Engineering smoke: >=50% complete base traces; no AUC/accuracy acceptance threshold.",
            "scientific_conclusion": None}


def intervention_coverage(rows):
    """Count complete source contrasts with valid answers in every control."""
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row.get("base_task_id"), row.get("pair_index"), row.get("pair_kind"))].append(row)
    usable, contrasts = 0, []
    required = {"baseline", "main", "crand", "clayer"}
    for (task, index, kind), records in grouped.items():
        conditions = {r.get("condition"): r for r in records}
        failures = []
        for condition in sorted(required):
            r = conditions.get(condition, {})
            norm = r.get("actual_norm")
            valid = (r.get("status") == "prospective_decode" and r.get("invalid") == 0
                     and r.get("decode_complete") is True
                     and isinstance(norm, (int, float)) and math.isfinite(norm)
                     and (norm == 0 if condition == "baseline" else norm > 0))
            if (sum(row.get("condition") == condition for row in records) != 1 or not valid
                    or (condition == "clayer" and r.get("clayer_status") != "dev_weak_layer_decode")):
                failures.append(condition)
        usable += not failures
        contrasts.append({"base_task_id": task, "pair_index": index, "pair_kind": kind,
                          "usable": not failures, "failed_conditions": failures})
    by_kind = defaultdict(int)
    for contrast in contrasts:
        if contrast["usable"]:
            by_kind[str(contrast["pair_kind"])] += 1
    return {"usable_main_contrasts": usable, "usable_by_kind": dict(by_kind), "contrasts": contrasts, "P3": "not_evaluated"}


def c2_summary(rows):
    coverage = intervention_coverage(rows)
    effects = []
    for contrast in coverage["contrasts"]:
        if not contrast["usable"]:
            continue
        records = {r["condition"]: r for r in rows if r.get("base_task_id") == contrast["base_task_id"]
                   and r.get("pair_index") == contrast["pair_index"] and r.get("pair_kind") == contrast["pair_kind"]}
        main = records["main"]
        def delta(condition, key):
            left, right = main.get(key), records[condition].get(key)
            return left - right if isinstance(left, (int, float)) and isinstance(right, (int, float)) else None
        effects.append({**contrast, "task_correct_vs_baseline": delta("baseline", "task_correct"),
                        "task_correct_vs_crand": delta("crand", "task_correct"),
                        "task_correct_vs_clayer": delta("clayer", "task_correct"),
                        "target_follow_vs_baseline": delta("baseline", "target"),
                        "interpretation": "same_value_cannot_identify_source_follow" if contrast["pair_kind"] == "same_value_diff_source"
                                          else "paired_descriptive_decode_contrast"})
    return {**coverage, "status": "evaluated_descriptive" if effects else "no_usable_contrast",
            "effects": effects, "scientific_conclusion": None}


def matched_baselines(h, y_task, y_beh, event_keys, feature_rows, tasks, traces, premise_keys, train, roles, position):
    """Train and evaluate text and trivial baselines on the probe's exact cells."""
    import numpy as np
    from .analysis import _fit_scores, classification_metrics
    from .baselines import fit_text_predictor, text_predictor
    trace_text = {t["id"]: t.get("text", "") for t in traces}
    boundaries = {}
    for i, (tid, identity, _node, _record, _owner) in enumerate(event_keys):
        row = feature_rows[i]
        if position == "pre_step":
            boundaries[i] = row["boundary_start"]
        elif position == "pre_value":
            boundaries[i] = row["boundary_end"]
        else:
            event = next((e for t in traces if t["id"] == tid for e in t.get("events", [])
                          if EventIdentity(**e["identity"]).key() == identity), None)
            boundaries[i] = event["end"] if event else row["boundary_end"]
    # Predict the next variable using only visible text, then consult its DAG.
    # Unlike the legacy oracle baseline, this never inserts the true node ID.
    candidate_rows = []
    for i, (tid, _identity, node, _record, owner) in enumerate(event_keys):
        if not np.isfinite(y_task[i]).any():
            continue
        task = tasks[owner]
        for candidate in task.nodes:
            name = next((a for a in candidate.aliases if a != candidate.id), candidate.id)
            candidate_rows.append((i, candidate.id, trace_text[tid][:boundaries[i]], name, int(node == candidate.id)))
    fitted_rows = [row for row in candidate_rows if train[row[0]]]
    variable_model = None
    if fitted_rows:
        variable_model = fit_text_predictor([r[2] for r in fitted_rows], np.array([r[4] for r in fitted_rows]), premises=[r[3] for r in fitted_rows])
    winners = {}
    if variable_model is not None:
        for i, node, prefix, name, _truth in candidate_rows:
            score = text_predictor(prefix, name, variable_model)
            if i not in winners or score > winners[i][0]:
                winners[i] = (score, node)
    output = []
    for head, labels in (("task", y_task), ("behavior", y_beh)):
        ii, jj = np.where(np.isfinite(labels))
        if not len(ii) or not train[ii].any():
            continue
        prefixes, premises, features, groups = [], [], [], []
        for i, j in zip(ii, jj):
            tid, identity, node, _record, owner = event_keys[i]
            task = tasks[owner]
            pid = str(premise_keys[j]).split("::", 1)[-1]
            premise = next(p for p in task.premises if p.premise_id == pid)
            row = feature_rows[i]
            boundary = boundaries[i]
            prefixes.append(trace_text[tid][:boundary])
            premises.append(premise.text)
            features.append([int(row.get("event_kind") == "restatement"), float(y_task[i, j]) if np.isfinite(y_task[i, j]) else 0])
            groups.append(task.base_group_id)
        truth = labels[ii, jj]
        mask = train[ii]
        model = fit_text_predictor([p for p, keep in zip(prefixes, mask) if keep], truth[mask],
                                   premises=[p for p, keep in zip(premises, mask) if keep])
        predictions = {
            "text_predictor": np.array([text_predictor(p, e, model) for p, e in zip(prefixes, premises)]),
            "restatement_and_R_task": _fit_scores(np.asarray(features), truth, mask),
        }
        if variable_model is not None:
            predictions["next_variable_to_dag"] = np.array([
                float(str(premise_keys[j]).split("::", 1)[-1] in ancestors(tasks[event_keys[i][-1]]).get(winners.get(i, (0, ""))[1], set()))
                for i, j in zip(ii, jj)])
        for name, scores in predictions.items():
            metrics = {}
            for role in ("probe_train", "dev", "calibration", "test"):
                keep = np.array([roles.get(str(event_keys[i][-1])) == role for i in ii])
                if keep.any():
                    metrics[role] = classification_metrics(scores[keep], truth[keep], split=role,
                                                           groups=[g for g, flag in zip(groups, keep) if flag])
            output.append({"baseline": name, "head": head, "position": position, "metrics": metrics,
                           "train_split": "probe_train", "comparison_cells": "identical_to_probe",
                           "oracle_diagnostic": name == "restatement_and_R_task"})
    return output
