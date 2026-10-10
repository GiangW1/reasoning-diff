"""P3: fit an extra-dependency direction on direction_fit; patch held-out prefixes."""
from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np

from .events import align_events, extract_answer
from .measure import compare_pair
from .formal import cluster_interval
from .graphs import ancestors
from .io import digest
from .schema import Task
from .protocol import answer_score

CONDITIONS = ('baseline', 'main', 'crand', 'clayer', 'wrong_direction', 'rescue_matched', 'rescue_random')


def direction_labels(event_rows, labels, tasks):
    """Positive: any observed non-ancestor response. Negative: full negative scan.

    Missing cells never become negative. This is an empirical scan label, not
    a claim that a direction represents a uniquely identified causal read set.
    """
    owners = {t['task_id']: Task.from_dict(t) for t in tasks}
    index = defaultdict(dict)
    for label in labels:
        if label.get('task_label') == 0 and label.get('behavior_label') in {0, 1}:
            index[label.get('trace_id'), label.get('event_id')][label['premise_id']] = label['behavior_label']
    result = []
    for event in event_rows:
        task = owners[event['task_id']]
        graph = ancestors(task)
        if event.get('node_id') not in graph:
            result.append(None)
            continue
        candidates = {p.premise_id for p in task.premises} - graph[event['node_id']]
        known = index[event['trace_id'], event['identity_key']]
        if any(known.get(p) == 1 for p in candidates):
            result.append(1)
        elif candidates and candidates <= known.keys():
            result.append(0)
        else:
            result.append(None)
    return result


def fit_direction(hidden, event_rows, labels, tasks, splits, ridge=1.0):
    if ridge <= 0 or len(hidden) != len(event_rows):
        raise ValueError('positive ridge and one hidden row per event required')
    roles = {s['base_group_id']: s['role'] for s in splits}
    y = direction_labels(event_rows, labels, tasks)
    use = np.array([roles[e['base_group_id']] == 'direction_fit' and v is not None
                    for e, v in zip(event_rows, y)], dtype=bool)
    observed = np.asarray([v for v, keep in zip(y, use) if keep], dtype=float)
    provenance = {'fit_role': 'direction_fit', 'n_events': int(use.sum()),
                  'fit_groups': sorted({e['base_group_id'] for e, keep in zip(event_rows, use) if keep}),
                  'label': 'observed_extra_dependency_presence', 'negative_requires_full_nonancestor_scan': True,
                  'rank': 1, 'ridge': ridge, 'decision_threshold': 0.5}
    if len(set(observed)) < 2:
        return {**provenance, 'status': 'insufficient_direction_classes', 'direction': None}
    x = np.asarray(hidden, dtype=float)[use]
    if not np.isfinite(x).all():
        raise ValueError('nonfinite direction-fit hidden states')
    mean, scale = x.mean(axis=0), x.std(axis=0)
    scale = np.where(scale > 1e-8, scale, 1.0)
    centered = (x - mean) / scale
    # Thin SVD avoids allocating a 4096×4096 covariance or dense projector.
    u, s, vt = np.linalg.svd(centered, full_matrices=False)
    weight = vt.T @ ((s / (s * s + ridge)) * (u.T @ (observed - observed.mean())))
    raw_weight = weight / scale
    norm = float(np.linalg.norm(raw_weight))
    if norm < 1e-12:
        return {**provenance, 'status': 'zero_direction', 'direction': None}
    # A linear probability score; the fixed threshold is not selected on test.
    intercept = float(observed.mean() - mean @ raw_weight)
    return {**provenance, 'status': 'fitted', 'direction': (raw_weight / norm).tolist(),
            'score_weight': raw_weight.tolist(), 'score_intercept': intercept,
            'direction_hash': digest((raw_weight / norm).tolist()),
            'n_positive': int(observed.sum()), 'n_negative': int(len(observed) - observed.sum())}


def choose_prefix(trace, event_rows, hidden, direction):
    if direction.get('status') != 'fitted':
        return None
    if trace['metadata'].get('boundary_status') != 'ok':
        return None
    candidates = [(i, e) for i, e in enumerate(event_rows) if e['trace_id'] == trace['id']]
    for i, event in sorted(candidates, key=lambda pair: pair[1]['boundary_start']):
        score = float(hidden[i] @ direction['score_weight'] + direction['score_intercept'])
        if score < direction['decision_threshold']:
            continue
        ids = event.get('prefix_token_ids') or []
        if not ids or event.get('timing') != 'pre_step':
            continue
        offsets = trace['offsets'][:len(ids)]
        if any(b > event['boundary_start'] for _, b in offsets):
            raise ValueError('P3 prefix contains target-step tokens')
        if trace['token_ids'][:len(ids)] != ids:
            raise ValueError('P3 prefix does not match the saved generation')
        return {'event': event, 'index': i, 'score': score, 'ids': ids}
    return None


def matched_deltas(main_hidden, weak_hidden, direction, weak_direction, seed):
    from .interventions import orthonormal_basis, scale_to_norm
    main_hidden, weak_hidden = np.asarray(main_hidden), np.asarray(weak_hidden)
    removed = -np.asarray(direction) * float(main_hidden @ direction)
    norm = float(np.linalg.norm(removed))
    rng = np.random.default_rng(seed)
    random = orthonormal_basis(len(main_hidden), 1, rng)[:, 0]
    crand, cr_status = scale_to_norm(-random * float(main_hidden @ random), norm)
    weak = np.asarray(weak_direction)
    clayer, cl_status = scale_to_norm(-weak * float(weak_hidden @ weak), norm)
    if norm > 1e-12 and (cr_status != 'ok' or cl_status != 'ok'):
        raise ValueError('cannot construct norm-matched P3 controls from zero components')
    rescue = orthonormal_basis(len(main_hidden), 1, rng)[:, 0] * norm
    return {'main': removed, 'crand': crand, 'clayer': clayer, 'wrong_direction': -removed,
            'rescue_matched': np.zeros_like(removed), 'rescue_random': removed + rescue,
            'norms': {'main': norm, 'crand': float(np.linalg.norm(crand)), 'clayer': float(np.linalg.norm(clayer))},
            'rescue_caveat': 'matched restoration is identity reconstruction, not independent causal evidence'}


def run_p3(traces, tasks, event_rows, hidden, direction, weak_layer, weak_direction, runtime,
           main_layer, *, max_new, sampling, seed=0, model_kind='qwen3'):
    from .models.collect import _hidden_at_layer, intervene_hidden_decode
    from . import cli
    owners = {t['task_id']: Task.from_dict(t) for t in tasks}
    rows = []
    for trace in traces:
        if trace.get('metadata', {}).get('formal_role') != 'reference' or trace['metadata']['formal_split'] != 'test':
            continue
        task = owners[trace['task_id']]
        base_record = {'trace_id': trace['id'], 'problem_id': task.base_group_id, 'split': 'test',
                       'condition_variant': task.metadata['formal_condition'],
                       'direction_fit_groups': direction['fit_groups'],
                       'boundary_selection': 'first_scored_positive_offline_annotated_event',
                       'feature_visibility': 'saved_prefix_only', 'online_boundary_detection_claim': False}
        if task.base_group_id in direction['fit_groups']:
            raise ValueError('P3 test/direction-fit family leakage')
        selected = choose_prefix(trace, event_rows, hidden, direction)
        unavailable = direction['status'] != 'fitted' or weak_direction['status'] != 'fitted'
        if selected is None or unavailable:
            original_correct = int(trace['status'] == 'natural_complete' and trace.get('correct') is True)
            rows.append({**base_record, 'status': 'direction_unavailable' if unavailable else 'no_selected_prefix',
                         'conditions': None if unavailable else {c: {'correct': original_correct,
                             'invalid': int(trace.get('answer') is None), 'actual_norm': 0.0} for c in CONDITIONS},
                         'policy': 'no_detected_prefix_no_intervention'})
            continue
        ids, event = selected['ids'], selected['event']
        weak_hidden = _hidden_at_layer(runtime['model'], ids, weak_layer)[-1]
        stable_seed = int(digest([seed, trace['id']])[:8], 16)
        deltas = matched_deltas(hidden[selected['index']], weak_hidden, direction['direction'], weak_direction['direction'], stable_seed)
        outputs = {}
        baseline_events = None
        for condition in CONDITIONS:
            delta = np.zeros_like(deltas['main']) if condition == 'baseline' else deltas[condition]
            layer = weak_layer if condition == 'clayer' else main_layer
            from .models.quantity_constraint import for_task
            constraint = for_task(task, runtime['tokenizer'], ids[trace['metadata'].get('prompt_len', len(ids)):])
            decoded = intervene_hidden_decode(model_kind, ids, layer, mode='add_delta', delta=delta,
                seed=stable_seed, model=runtime['model'], max_new=max_new, event_aligned=True,
                target_prefix_len=len(ids), eos_id=runtime['tokenizer'].eos_token_id,
                target_delta_norm=deltas['norms']['main'] if condition in {'main', 'crand', 'clayer', 'wrong_direction'} else None,
                **({'constraint': constraint} if constraint is not None else {}),
                **sampling)
            if not decoded['hook_fired'] or not decoded['prefix_boundary_verified']:
                raise RuntimeError('P3 hook did not fire at the requested boundary')
            actual = float(decoded['hook_delta_norm'])
            if condition in {'main', 'crand', 'clayer'} and not np.isclose(actual, deltas['norms'][condition], rtol=.02, atol=1e-4):
                raise RuntimeError('P3 actual hook norms do not match the control protocol')
            tokenizer = runtime['tokenizer']
            prefix = tokenizer.decode(ids, skip_special_tokens=False)
            full = tokenizer.decode(ids + decoded['generated_ids'], skip_special_tokens=False)
            if not full.startswith(prefix):
                raise ValueError('P3 continuation does not preserve the saved prefix')
            text = full[len(prefix):]
            complete = decoded['stop_reason'] != 'max_new' and '</think>' in full
            answer = extract_answer(full[full.rfind('</think>') + len('</think>'):], task.answer_spec.kind) if complete else None
            score = answer_score(answer, task.answer_spec.value, task.answer_spec.kind, task.answer_spec.aliases)
            from .quantity_steps import is_controlled, trace_format
            step_format = (trace_format({'text': full, 'metadata': trace['metadata']}, task)
                           if is_controlled(task) else None)
            format_valid = step_format is None or step_format['passed']
            _, future = cli._parse_intervention_events(task, full, len(prefix), trace['metadata']['rendered_prompt_text'])
            if condition == 'baseline':
                baseline_events = future
            excluded = {event['node_id']}
            for node in task.nodes:
                if excluded.intersection(node.parents):
                    excluded.add(node.id)
            pairs = align_events(baseline_events or [], future)['pairs']
            others = [(a, b) for a, b in pairs if a.node_id not in excluded and a.event_kind != 'restatement']
            nontarget = sum(compare_pair(a, b) == 'changed' for a, b in others) / len(others) if others else None
            outputs[condition] = {'correct': int(complete and format_valid and score['correct'] is True),
                'invalid': int(answer is None or not format_valid), 'complete': complete, 'stop_reason': decoded['stop_reason'],
                'quantity_step_format': step_format,
                'quantity_constraint': decoded.get('quantity_constraint'),
                'actual_norm': actual, 'planned_norm': float(np.linalg.norm(delta)), 'layer': layer,
                'norm_calibration': decoded.get('norm_calibration'),
                'nontarget_change_rate': nontarget, 'nontarget_matched_events': len(others),
                'generated_ids': decoded['generated_ids'], 'continuation_text': text,
                'hook_token_position': decoded['hook_token_position'], 'hook_sequence_length': decoded['hook_sequence_length']}
        rows.append({**base_record, 'status': 'prospective_decode', 'selected_event': event['identity_key'],
                     'score': selected['score'], 'prefix_tokens': len(ids), 'conditions': outputs,
                     'random_seed': stable_seed, 'estimand': 'paired_conditional_continuations',
                     'original_correct': trace.get('correct'), 'rescue_caveat': deltas['rescue_caveat']})
    return rows


def p3_report(rows):
    result = {'n_registered': len(rows), 'statuses': dict(Counter(r['status'] for r in rows)),
              'n_executed': sum(r['status'] == 'prospective_decode' for r in rows),
              'n_unavailable': sum(r['conditions'] is None for r in rows), 'contrasts': {},
              'selection': 'no_selection_on_test_correctness_or_observed_dependency_labels',
              'causal_reverse_claim': False}
    usable = [r for r in rows if r['conditions'] is not None]
    for variant in ('all', 'base', 'related_noop', 'neutral_noop'):
        subset = [r for r in usable if variant == 'all' or r['condition_variant'] == variant]
        result['contrasts'][variant] = {}
        for control in ('baseline', 'crand', 'clayer', 'wrong_direction'):
            values = [r['conditions']['main']['correct'] - r['conditions'][control]['correct'] for r in subset]
            result['contrasts'][variant][f'main_minus_{control}'] = cluster_interval(values, [r['problem_id'] for r in subset])
        result['contrasts'][variant]['conditions'] = {c: {
            'accuracy': cluster_interval([r['conditions'][c]['correct'] for r in subset], [r['problem_id'] for r in subset]),
            'invalid_rate': cluster_interval([r['conditions'][c]['invalid'] for r in subset], [r['problem_id'] for r in subset]),
            'nontarget_change': cluster_interval([r['conditions'][c].get('nontarget_change_rate') for r in subset], [r['problem_id'] for r in subset])}
            for c in CONDITIONS}
    result['status'] = 'estimate' if usable else 'not_estimable'
    return result
