"""Frozen C3 design and problem-level analysis. No automatic scientific gates."""
from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np

from .analysis import _auc, _fit_scores, classification_metrics
from .edits import C2_PAIR_KINDS, _rewrite_ids, apply_value_edit, recompute
from .events import align_events, premise_aliases
from .graphs import ancestors, dirty_cone
from .io import digest
from .next_round import base_trajectories, scan_edits, sentence_graph_task
from .schema import Edit, Premise, Task, Trace
from .splits import DEFAULT_FRACTIONS, split_for_task
from .tasks.t2_noop import make_noop_pair

CONDITIONS = ('base', 'related_noop', 'neutral_noop')


def condition_tasks(task):
    """New, independent quantities; both injections have the same word count.

    Graph invariance is an algebraic check. Human semantic validation remains
    necessary; these are project-derived examples, not official GSM-NoOp.
    """
    base = sentence_graph_task(task)
    name = base.metadata['names'][base.target]
    neutral = ' '.join(['silver'] * len(name.split()))
    result = [base]
    for condition, topic, surface in [('related_noop', name, 'high'), ('neutral_noop', neutral, 'low')]:
        sentence = f'The number of souvenir labels at the {topic} display equals 17.'
        pair = make_noop_pair(base, sentence, 'front', surface, True)
        pair.premises[-1].value = '17'
        pair.premises[-1].kind = 'definition'
        pair.validate()
        result.append(pair)
    for condition, item in zip(CONDITIONS, result, strict=True):
        item.metadata.update(formal_condition=condition, noop_semantic_audit='pending',
                             length_control='equal_injected_word_count_not_token_count')
    return result


def source_factorial(task, premise_id, alternate):
    """Both equal-valued source facts appear in both route conditions.

    Downstream rule text and the independent graph change together. Physical
    ordering is counterbalanced by family. These equal-value strata control
    route changes; build_design adds unequal fixed-fact route contrasts.
    """
    found = next(p for p in task.premises if p.premise_id == premise_id)
    alias = premise_aliases(found)[-1]
    reserve = 'alternate reserve quantity'
    new_id = 'src_b'
    if any(p.premise_id == new_id for p in task.premises):
        raise ValueError('source ID collision')
    extra = Premise(new_id, f'The number of {reserve} equals {found.value}.', 0, 1, found.value, 'definition')
    physical = list(task.premises)
    offset = physical.index(found) + int(int(digest(task.base_group_id)[:2], 16) % 2)
    physical.insert(offset, extra)
    tail = task.question[max(p.end for p in task.premises):]
    routes = []
    for route in ('a', 'b'):
        sentences, premises = [], []
        mapping = {premise_id: new_id, alias: reserve} if route == 'b' else {}
        for p in physical:
            body = p.text if p.premise_id in {premise_id, new_id} else _rewrite_ids(p.text, mapping)
            start = len(' '.join(sentences)) + bool(sentences)
            value = _rewrite_ids(p.value, {premise_id: new_id}) if route == 'b' and p.kind == 'relation' else p.value
            premises.append({**p.__dict__, 'text': body, 'start': start, 'end': start + len(body), 'value': value})
            sentences.append(body)
        tid = f'{task.task_id}::route_{route}'
        nodes = [{**n.__dict__, 'parents': [new_id if route == 'b' and p == premise_id else p for p in n.parents],
                  'expression': _rewrite_ids(n.expression, {premise_id: new_id}) if route == 'b' else n.expression}
                 for n in task.nodes]
        item = recompute(Task.from_dict({**task.to_dict(), 'task_id': tid, 'record_id': tid, 'nodes': nodes,
            'question': ' '.join(sentences) + tail, 'premises': premises,
            'metadata': {**task.metadata, 'source_route': route, 'source_order': offset}}))
        item.validate()
        routes.append(item)
    a, b = routes
    if a.answer_spec.value != b.answer_spec.value or premise_id in ancestors(b)[b.target]:
        raise ValueError('source factorial failed independent route/value check')
    # In the high-value stratum both available facts have the same new value.
    # Thus route-a/route-b prompts have identical numbers and physical order.
    def value_companion(owner):
        first = apply_value_edit(owner, premise_id, alternate)
        second = apply_value_edit(first.task, new_id, alternate)
        return Edit('route-values:' + owner.task_id, owner.task_id, [premise_id, new_id], second.task,
                    kind='same_source_diff_value', before={premise_id: found.value, new_id: found.value},
                    after={premise_id: alternate, new_id: alternate}, validity='valid',
                    metadata={'source_route_unchanged': True, 'joint_equal_value_control': True})
    av, bv = value_companion(a), value_companion(b)
    if av.task.answer_spec.value != bv.task.answer_spec.value:
        raise ValueError('unequal-value routes must have the same gold answer')
    return a, b, av, bv


def build_design(tasks, *, seeds=(0, 1, 2), noise_seeds=(3, 4, 5), edit_values=2, split_seed=0,
                 trajectory_protocol='natural', quantity_decoding_protocol=None):
    if trajectory_protocol not in {'natural', 'quantity_steps'}:
        raise ValueError('unknown trajectory protocol')
    if quantity_decoding_protocol is not None:
        from .models.quantity_constraint import PROTOCOL as CONSTRAINED
        if quantity_decoding_protocol != CONSTRAINED or trajectory_protocol != 'quantity_steps':
            raise ValueError('quantity decoding requires its registered controlled trajectory protocol')
    if len(set(seeds)) != len(seeds) or not seeds or len(set(noise_seeds)) != len(noise_seeds):
        raise ValueError('generation seeds must be nonempty and unique')
    if not noise_seeds or set(seeds) & set(noise_seeds) or edit_values < 1 or edit_values > 22:
        raise ValueError('noise seeds must be disjoint; edit_values must be 1..22')
    owners, requests, edits, splits = {}, [], [], []

    def request(owner, seed, role):
        owners[owner.task_id] = owner.to_dict()
        rid = f'trace-{role}:' + digest([owner.task_id, seed])[:24]
        requests.append({'task_id': owner.task_id, 'seed': seed, 'role': role, 'id': rid})
        return rid

    for task in tasks:
        for owner in condition_tasks(task):
            role = split_for_task(task, seed=split_seed, fractions=DEFAULT_FRACTIONS)
            owners[owner.task_id] = owner.to_dict()
            refs = {seed: request(owner, seed, 'reference') for seed in seeds}
            for seed in noise_seeds:
                request(owner, seed, 'noise')
            for edit in scan_edits(owner, edit_values):
                comparisons = {seed: request(edit.task, seed, 'edit') for seed in seeds}
                edits.append({**edit.to_dict(), 'reference_ids': refs, 'comparison_ids': comparisons})
            if owner.metadata['formal_condition'] == 'base' and role in {'dev', 'test'}:
                needed = ancestors(owner)[owner.target]
                candidates = ((p, str((int(p.value) + shift) % 23)) for p in owner.premises
                              if p.kind == 'definition' and p.premise_id in needed for shift in range(1, 23))
                identifiable = next(((p, value) for p, value in candidates
                    if apply_value_edit(owner, p.premise_id, value).task.answer_spec.value != owner.answer_spec.value), None)
                if identifiable is None:
                    continue
                source, alt = identifiable
                a, b, av, bv = source_factorial(owner, source.premise_id, alt)
                ids = {x.task_id: request(x, seeds[0], 'source') for x in (a, b, av.task, bv.task)}
                nontargets = [n.id for n in owner.nodes if n.id not in dirty_cone(owner, {source.premise_id})]
                back = Edit('route-value-back:' + av.task.task_id, av.task.task_id, [source.premise_id, 'src_b'], a,
                            kind='same_source_diff_value', before={source.premise_id: alt, 'src_b': alt},
                            after={source.premise_id: source.value, 'src_b': source.value}, validity='valid',
                            metadata={'source_route_unchanged': True, 'joint_equal_value_control': True})
                for left, right, changed in ((a, b, av), (av.task, bv.task, back)):
                    value = next(p.value for p in left.premises if p.premise_id == source.premise_id)
                    source_edit = Edit('route:' + left.task_id, left.task_id, ['src_b'], right,
                        kind='same_value_diff_source', before={source.premise_id: value},
                        after={'src_b': value}, validity='valid')
                    edits.append({'kind': 'source_value_pair', 'base_task_id': left.task_id,
                        'same_value_diff_source': source_edit.to_dict(), 'same_source_diff_value': changed.to_dict(),
                        'targets': [owner.target], 'nontargets': nontargets,
                        'trace_ids': {'base': ids[left.task_id], 'same_value_diff_source': ids[right.task_id],
                                      'same_source_diff_value': ids[changed.task.task_id]}, 'unequal_source_companion': ids[bv.task.task_id],
                        'source_value_stratum': value})
                # Hold both physical facts fixed, with distinct values. Switch
                # only the downstream route, in both directions and assignments.
                for changed_id in ('src_b', source.premise_id):
                    left = apply_value_edit(a, changed_id, alt).task
                    right = apply_value_edit(b, changed_id, alt).task
                    facts = lambda t: [(p.premise_id, p.text, p.value) for p in t.premises if p.kind == 'definition']
                    if facts(left) != facts(right) or left.answer_spec.value == right.answer_spec.value:
                        raise ValueError('fixed-fact routes must have identical facts and different gold answers')
                    for item in (left, right):
                        ids[item.task_id] = request(item, seeds[0], 'source')
                    for recipient, donor, old, new, direction in (
                        (left, right, source.premise_id, 'src_b', 'a_to_b'),
                        (right, left, 'src_b', source.premise_id, 'b_to_a'),
                    ):
                        values = {p.premise_id: p.value for p in recipient.premises}
                        changed = [p.premise_id for p, q in zip(recipient.premises, donor.premises, strict=True)
                                   if p.text != q.text]
                        source_edit = Edit('fixed-route:' + recipient.task_id, recipient.task_id, changed, donor,
                            kind='fixed_values_diff_source', before={old: values[old]}, after={new: values[new]},
                            validity='valid', metadata={'source_value_mode': 'unequal_fixed_facts'})
                        edits.append({'kind': 'source_value_pair', 'base_task_id': recipient.task_id,
                            'fixed_values_diff_source': source_edit.to_dict(), 'routing_direction': direction,
                            'targets': [owner.target], 'nontargets': nontargets,
                            'trace_ids': {'base': ids[recipient.task_id], 'fixed_values_diff_source': ids[donor.task_id]}})
    if trajectory_protocol == 'quantity_steps':
        from .quantity_steps import controlled_task
        owners = {tid: controlled_task(Task.from_dict(row)).to_dict() for tid, row in owners.items()}
        if quantity_decoding_protocol is not None:
            for row in owners.values():
                row['metadata']['quantity_decoding_protocol'] = quantity_decoding_protocol
        for edit in edits:
            nested = ([edit] if edit['kind'] != 'source_value_pair' else
                      [v for v in edit.values() if isinstance(v, dict) and 'task' in v])
            for item in nested:
                item['task'] = owners[item['task']['task_id']]
    for owner in owners.values():
        splits.append({'task_id': owner['task_id'], 'base_group_id': owner['base_group_id'],
                       'role': split_for_task(Task.from_dict(owner), seed=split_seed, fractions=DEFAULT_FRACTIONS)})
    if len({r['id'] for r in requests}) != len(requests):
        raise ValueError('duplicate registered generation request')
    return {'tasks': list(owners.values()), 'requests': requests, 'edits': edits, 'splits': splits,
            'summary': {'n_problems': len({t.base_group_id for t in tasks}), 'requests': len(requests),
                        'by_role': dict(Counter(r['role'] for r in requests)),
                        'family_roles': dict(Counter({s['base_group_id']: s['role'] for s in splits}.values()))}}


def observations_for(design, rows):
    from . import cli
    traces = {r['id']: Trace.from_dict(r) for r in rows}
    if set(traces) != {r['id'] for r in design['requests']} or len(traces) != len(rows):
        raise ValueError('generation cohort differs from the frozen request set')
    tasks = {r['task_id']: Task.from_dict(r) for r in design['tasks']}
    observations = []
    for row in design['edits']:
        if row['kind'] == 'source_value_pair':
            continue
        fields = {k: v for k, v in row.items() if k in Edit.__dataclass_fields__}
        edit = Edit(**{**fields, 'task': Task.from_dict(fields['task'])})
        for seed, ref in row['reference_ids'].items():
            obs = cli._observations(tasks[edit.base_task_id], traces[ref], traces[row['comparison_ids'][seed]],
                                    edit, f'stream:{seed}', 'formal:' + row['id'] + ':' + str(seed))
            observations.extend(o.to_dict() for o in obs)
    grouped = defaultdict(list)
    for r in design['requests']:
        if r['role'] in {'reference', 'noise'}:
            grouped[r['task_id']].append(r)
    for tid, requests in grouped.items():
        for ref in [r for r in requests if r['role'] == 'reference']:
            for donor in [r for r in requests if r['role'] == 'noise']:
                observations.extend(o.to_dict() for o in cli._sham_observations(tasks[tid], traces[ref['id']],
                    traces[donor['id']], donor['seed'], f"formal-noise:{ref['id']}:{donor['id']}"))
    return observations


def cluster_interval(values, groups, *, seed=0, n_boot=500):
    buckets = defaultdict(list)
    for value, group in zip(values, groups, strict=True):
        if value is not None:
            buckets[str(group)].append(float(value))
    means = np.array([np.mean(v) for v in buckets.values()])
    if not len(means):
        return {'mean': None, 'interval': None, 'n_problems': 0, 'status': 'missing'}
    interval = None
    if len(means) >= 2:
        rng = np.random.default_rng(seed)
        draws = means[rng.integers(0, len(means), (n_boot, len(means)))].mean(axis=1)
        interval = np.quantile(draws, [.025, .975]).tolist()
    return {'mean': float(means.mean()), 'interval': interval, 'n_problems': len(means),
            'status': 'estimate' if interval else 'insufficient_problems', 'unit': 'equal_weight_problem'}


def p1_report(table, n_boot=500, conditions=('base',), answered_only=False):
    """Fit on probe_train only; evaluate test. Missing rho has its own audit."""
    table = [r for r in table if r.get('condition') in conditions]
    estimands = {r.get('density_protocol', 'matched_cell_response_rate_excess_v1') for r in table}
    if len(estimands) > 1:
        raise ValueError('different measurement estimands require separate P1 reports')
    if answered_only:
        table = [{**r, 'y': int(r['answer_correct'])} for r in table if r.get('answer_completed')]
    counts = dict(Counter(str(r['y']) for r in table))
    result = {'n_trajectories': len(table), 'class_counts': counts, 'conditions': list(conditions),
              'outcome': 'answered_task_correctness' if answered_only else 'ITT_failures_as_incorrect',
              'missing_by_outcome': dict(Counter(str(r['y']) for r in table if r['rho'] is None)),
              'missing_by_split': dict(Counter(r['split'] for r in table if r['rho'] is None)),
              'estimand': next(iter(estimands), 'matched_cell_response_rate_excess_v1'), 'future_information': 'full_trajectory_diagnostic',
              'missing_policy': 'no_imputation_complete_case_attribution_with_ITT_accounting'}
    rows = [r for r in table if r['split'] in {'probe_train', 'test'} and r['rho'] is not None]
    train = np.array([r['split'] == 'probe_train' for r in rows], dtype=bool)
    labels = np.array([1 - r['y'] for r in rows], dtype=int)
    for mask, name in ((train, 'train'), (~train, 'test')):
        if not mask.any() or len(set(labels[mask])) < 2:
            return {**result, 'status': f'insufficient_classes_{name}', 'delta_auc': None}
    groups = [r['problem_id'] for r in rows]
    if {g for g, flag in zip(groups, train) if flag} & {g for g, flag in zip(groups, train) if not flag}:
        raise ValueError('P1 family leakage')
    x = np.array([[r['length'], r['op'], r.get('restatement_fraction', 0),
                   r.get('calculation_fraction', 0), r.get('coverage') or 0,
                   int(r['condition'] == 'related_noop'), int(r['condition'] == 'neutral_noop')] for r in rows], dtype=float)
    rho = np.array([r['rho'] for r in rows])
    predictions = {name: _fit_scores(features, labels, train)[~train]
                   for name, features in [('length_op', x[:, :2]), ('strong_base', x),
                                          ('with_rho', np.c_[x, rho])]}
    truth = labels[~train]
    held_groups = [g for g, flag in zip(groups, train) if not flag]
    weights = np.array([1 / Counter(held_groups)[g] for g in held_groups])
    metrics = {name: {**classification_metrics(score, truth, split='test', groups=held_groups),
                     'brier_problem_weighted': float(np.average((score - truth) ** 2, weights=weights))}
               for name, score in predictions.items()}
    delta = metrics['with_rho']['auc'] - metrics['strong_base']['auc']
    unique = list(dict.fromkeys(held_groups))
    rng, draws = np.random.default_rng(0), []
    for _ in range(n_boot):
        selected = rng.choice(unique, len(unique), replace=True)
        idx = np.array([i for g in selected for i, actual in enumerate(held_groups) if actual == g])
        a, b = _auc(predictions['with_rho'][idx], truth[idx]), _auc(predictions['strong_base'][idx], truth[idx])
        if a is not None and b is not None:
            draws.append(a - b)
    return {**result, 'status': 'estimate', 'metrics': metrics, 'delta_auc': delta,
            'delta_auc_interval': np.quantile(draws, [.025, .975]).tolist() if len(unique) >= 2 and draws else None,
            'bootstrap': {'unit': 'problem', 'n_valid': len(draws), 'n_requested': n_boot, 'refit': False},
            'test_predictions': [{'trace_id': r['trace_id'], 'problem_id': r['problem_id'], 'incorrect': int(y),
                                  **{k: float(v[i]) for k, v in predictions.items()}}
                                 for i, (r, y) in enumerate(zip([r for r in rows if r['split'] == 'test'], truth))]}


def event_response_cells(trace, owner, observations):
    graph = ancestors(owner)
    result = {}
    real, noise = defaultdict(list), defaultdict(list)
    for row in observations:
        if row['reference_trace'] != trace.id or row['outcome'] not in {'changed', 'no_change'}:
            continue
        if (row.get('rng_pair') or '').startswith('sham:'):
            noise[row['alignment_ref']].append(row['outcome'] == 'changed')
        else:
            real[row['alignment_ref'], row['premise_id']].append(row['outcome'] == 'changed')
    for event in trace.events:
        if event.event_region != 'thinking' or event.event_kind == 'restatement' or event.node_id not in graph:
            continue
        key = event.identity.key()
        for premise in owner.premises:
            if premise.premise_id in graph[event.node_id]:
                continue
            values, reference = real[key, premise.premise_id], noise[key]
            if values and reference:
                result[key, premise.premise_id] = np.mean(values) - np.mean(reference)
    return result


def p2_report(traces, tasks, observations):
    """Compare identical aligned event×original-premise cells across conditions."""
    owners = {r['task_id']: Task.from_dict(r) for r in tasks}
    by = {(r['base_group_id'], r['seed'], owners[r['task_id']].metadata['formal_condition']): Trace.from_dict(r)
          for r in base_trajectories(traces, tasks)}
    rows, contrasts = [], []
    for (group, seed, condition), base in by.items():
        if condition != 'base':
            continue
        left_task = owners[base.task_id]
        left_cells = event_response_cells(base, left_task, observations)
        paired_cells, paired_rows = {}, {}
        for condition in CONDITIONS[1:]:
            right = by[group, seed, condition]
            right_task = owners[right.task_id]
            right_cells = event_response_cells(right, right_task, observations)
            pairs = align_events(base.events, right.events)['pairs']
            shared, delta, cell_deltas = [], [], {}
            for a, b in pairs:
                for pid in [p.premise_id for p in left_task.premises]:
                    ka, kb = (a.identity.key(), pid), (b.identity.key(), pid)
                    if ka in left_cells and kb in right_cells:
                        shared.append([a.identity.key(), b.identity.key(), pid])
                        delta.append(float(right_cells[kb] - left_cells[ka]))
                        cell_deltas[ka] = delta[-1]
            injected = [float(value) for (_, pid), value in right_cells.items() if pid == 'noop']
            rows.append({'problem_id': group, 'seed': seed, 'condition': condition,
                         'split': next(r.get('metadata', {}).get('formal_split') for r in traces if r['id'] == base.id),
                         'delta_acc': int(right.status == 'natural_complete' and right.correct is True)
                                      - int(base.status == 'natural_complete' and base.correct is True),
                         'delta_rho_common_cells': float(np.mean(delta)) if delta else None,
                         'shared_cells': shared, 'injected_excess': float(np.mean(injected)) if injected else None,
                         'base_rho_cells': len(left_cells), 'noop_rho_cells': len(right_cells)})
            paired_cells[condition], paired_rows[condition] = cell_deltas, rows[-1]
        related, neutral = (paired_cells[c] for c in CONDITIONS[1:])
        common = related.keys() & neutral.keys()
        contrasts.append({'problem_id': group, 'seed': seed, 'split': rows[-1]['split'],
            'delta_acc': paired_rows['related_noop']['delta_acc'] - paired_rows['neutral_noop']['delta_acc'],
            'delta_rho_common_cells': float(np.mean([related[k] - neutral[k] for k in common])) if common else None,
            'three_arm_common_cells': len(common)})
    test = [r for r in rows if r['split'] == 'test']
    summaries = {}
    for condition in CONDITIONS[1:]:
        subset = [r for r in test if r['condition'] == condition]
        summaries[condition] = {key: cluster_interval([r[key] for r in subset], [r['problem_id'] for r in subset])
                               for key in ('delta_acc', 'delta_rho_common_cells', 'injected_excess')}
    test_contrasts = [r for r in contrasts if r['split'] == 'test']
    summaries['related_minus_neutral'] = {key: cluster_interval([r[key] for r in test_contrasts], [r['problem_id'] for r in test_contrasts])
                                         for key in ('delta_acc', 'delta_rho_common_cells')}
    return {'status': 'estimate' if test else 'no_test_pairs', 'rows': rows, 'contrasts': contrasts, 'test': summaries,
            'accuracy_denominator': 'all_registered_pairs_including_generation_failures',
            'rho_denominator': 'identical_aligned_event_and_original_premise_cells', 'unknown_is_negative': False}


def c2_report(rows, tasks):
    """Report failed generations as incorrect within executed paired hooks.

    Missing donors/boundaries remain unavailable; complete-answer filtering
    cannot remove a condition selectively from the primary effect.
    """
    from .next_round import c2_summary
    empty_shards = [r for r in rows if r.get('status') == 'no_source_pairs_in_split']
    rows = [r for r in rows if r.get('status') != 'no_source_pairs_in_split']
    families = {t['task_id']: t['base_group_id'] for t in tasks}
    buckets = defaultdict(dict)
    for row in rows:
        key = row.get('base_task_id'), row.get('pair_index'), row.get('pair_kind')
        if row.get('condition') in buckets[key]:
            raise ValueError('duplicate C2 condition in a registered contrast')
        buckets[key][row.get('condition')] = row
    effects, unavailable, verified = [], [], set()
    required = {'baseline', 'main', 'crand', 'clayer'}
    for (task_id, index, kind), conditions in buckets.items():
        if not required <= conditions.keys() or any(conditions[c].get('status') != 'prospective_decode' for c in required):
            unavailable.append({'base_task_id': task_id, 'pair_index': index, 'pair_kind': kind})
            continue
        main_norm = conditions['main'].get('actual_norm')
        norms = [conditions[c].get('actual_norm') for c in ('main', 'crand', 'clayer')]
        matched = (isinstance(main_norm, (int, float)) and main_norm > 0
                   and all(isinstance(v, (int, float)) and np.isfinite(v) and v > 0
                           and np.isclose(v, main_norm, rtol=.02, atol=0) for v in norms)
                   and all(conditions[c].get('norm_source') == 'resid_post_hook'
                           and conditions[c].get('hook_fired') is True
                           and conditions[c].get('prefix_boundary_verified') is True for c in ('main', 'crand', 'clayer'))
                   and conditions['baseline'].get('norm_source') == 'unmodified_baseline'
                   and conditions['baseline'].get('actual_norm') == 0
                   and conditions['clayer'].get('clayer_status') == 'dev_weak_layer_decode')
        if not matched:
            unavailable.append({'base_task_id': task_id, 'pair_index': index, 'pair_kind': kind, 'reason': 'control_norm_or_layer_invalid'})
            continue
        verified.add((task_id, index, kind))
        correct = {c: float(conditions[c].get('decode_complete') is True and conditions[c].get('invalid') == 0
                            and conditions[c].get('task_correct') == 1) for c in required}
        follow = {c: (None if conditions[c].get('target') is None else
                      float(conditions[c].get('decode_complete') is True and conditions[c].get('invalid') == 0
                            and conditions[c]['target'] == 1)) for c in required}
        effects.append({'problem_id': families[task_id], 'pair_kind': kind, 'base_task_id': task_id, 'pair_index': index,
            **{f'main_minus_{c}': correct['main'] - correct[c] for c in ('baseline', 'crand', 'clayer')},
            **{f'target_follow_main_minus_{c}': None if follow['main'] is None or follow[c] is None
               else follow['main'] - follow[c] for c in ('baseline', 'crand', 'clayer')},
            'conditions': {c: {'correct': correct[c], 'invalid': conditions[c].get('invalid'),
                               'target_follow': follow[c],
                               'nontarget': conditions[c].get('nontarget')} for c in required}})
    # Secondary complete-answer effects must obey the same measured-hook
    # requirements. Keep unavailable contrasts in coverage with failed status.
    result = c2_summary([r if (r.get('base_task_id'), r.get('pair_index'), r.get('pair_kind')) in verified
                         else {**r, 'status': 'unverified_control_cohort'} for r in rows])
    metrics = ('main_minus_baseline', 'main_minus_crand', 'main_minus_clayer',
               'target_follow_main_minus_baseline', 'target_follow_main_minus_crand', 'target_follow_main_minus_clayer')
    result['paired_ITT'] = {kind: {metric: cluster_interval([r[metric] for r in effects if r['pair_kind'] == kind],
        [r['problem_id'] for r in effects if r['pair_kind'] == kind]) for metric in metrics}
        for kind in C2_PAIR_KINDS}
    result.update(executed_ITT_effects=effects, unavailable=unavailable, empty_shards=empty_shards,
                  generation_failures='incorrect_within_complete_executed_hook_cohorts',
                  donor_failures='unknown_retained_in_coverage', complete_answer_effects='secondary_descriptive_only')
    return result
