"""PR8 sentence-fact protocol and measurement checks (no model truth hints)."""
from __future__ import annotations

import ast
from collections import defaultdict
import math

from .edits import apply_value_edit, recompute
from .events import premise_aliases
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


def trace_labels(observations, tasks):
    """Behavior labels belong to the reference seed, not a pooled event ID."""
    owners = {t.task_id: t for t in tasks}
    grouped = defaultdict(list)
    for obs in observations:
        if not (obs.rng_pair or "").startswith("sham:"):
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


def trajectory_table(traces, tasks, observations, splits):
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
        if o.get("outcome") not in {"changed", "no_change"}:
            continue
        bucket = noise if (o.get("rng_pair") or "").startswith("sham:") else real
        bucket[key].append(o)
    result = []
    for trace in traces:
        owner = owners.get(trace["task_id"])
        if owner is None or owner.edit_ref or "::" in trace["task_id"]:
            continue
        if "sham" in trace["id"] or "source" in trace["id"]:
            continue
        graph = ancestors(owner)
        supported, raw, excess = 0, [], []
        graph.update({p.premise_id: {p.premise_id} for p in owner.premises})
        eligible = 0
        for event in trace.get("events", []):
            if event.get("event_region") != "thinking" or event.get("event_kind") == "restatement" or event.get("status", "ok") != "ok":
                continue
            key = (trace["id"], EventIdentity(**event["identity"]).key())
            non_task = {p.premise_id for p in owner.premises} - graph.get(event["node_id"], set())
            eligible += len(non_task)
            cells = defaultdict(list)
            for obs in real[key]:
                if obs["premise_id"] in non_task:
                    cells[obs["premise_id"]].append(obs["outcome"] == "changed")
            n = noise[key]
            rate = sum(o["outcome"] == "changed" for o in n) / len(n) if n else None
            event_raw, event_excess = [], []
            for values in cells.values():
                value = sum(values) / len(values)
                event_raw.append(value)
                supported += 1
                if rate is not None:
                    event_excess.append(value - rate)
            if event_raw:
                raw.append(sum(event_raw) / len(event_raw))
                if len(event_excess) == len(event_raw):
                    excess.append(sum(event_excess) / len(event_excess))
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
                       "observed_events": len(raw), "aggregation": "mean_over_observed_events",
                       "coverage": supported / eligible if eligible else None,
                       "y": int(complete and trace.get("correct") is True), "split": role,
                       "held_out": role == "test", "trace_status": trace.get("status"),
                       "failure_as_incorrect": not complete})
    return result


def smoke_report(traces, tasks, observations, event_rows, probes):
    base = [t for t in traces if "trace-base" in t["id"] or "trace-t0p" in t["id"]]
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
