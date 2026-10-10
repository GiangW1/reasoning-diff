"""Explain missing natural-step support without changing labels or denominators."""
from collections import Counter, defaultdict

from .events import align_events
from .graphs import ancestors
from .schema import Task, Trace


def alignment_audit(trace_rows, task_rows, observations, measurement):
    traces = {row['id']: Trace.from_dict(row) for row in trace_rows}
    tasks = {row['task_id']: Task.from_dict(row) for row in task_rows}
    references = {row['trace_id']: row for row in measurement['trajectories']}
    real_pairs = defaultdict(set)
    for obs in observations:
        if not (obs.get('rng_pair') or '').startswith('sham:'):
            real_pairs[obs['reference_trace'], obs['premise_id']].add(obs['comparison_trace'])
    pair_cache, pair_rows = {}, []

    def eligible(trace):
        if trace.metadata.get('boundary_status', 'ok') != 'ok':
            return []
        return [e for e in trace.events if e.event_region == 'thinking'
                and e.event_kind != 'restatement' and e.status == 'ok']

    def compare(a, b, premise, noise=False):
        cache_key = (a.id, b.id, premise, noise)
        if cache_key in pair_cache:
            return pair_cache[cache_key]
        # Match the full production sequence, including restatement anchors.
        aligned = align_events(a.events, b.events)
        matched = {e.identity.key() for e, _ in aligned['pairs']}
        if any(t.metadata.get('boundary_status', 'ok') != 'ok' for t in (a, b)):
            matched = set()
        losses = {r['left']: r['reason'] for r in aligned.get('unmatched_left', [])}
        graph = ancestors(tasks[a.task_id])
        left = [e for e in eligible(a) if noise or premise not in graph.get(e.node_id, set())]
        right = eligible(b)
        entity = lambda e: (e.node_id, e.identity.scope)
        phase = lambda e: (*entity(e), e.event_kind, e.event_phase)
        counts = Counter('matched' if e.identity.key() in matched else
                         losses.get(e.identity.key(), 'boundary_or_unclassified') for e in left)
        pair_rows.append({'reference': a.id, 'comparison': b.id, 'premise': premise,
                          'kind': 'noise' if noise else 'edit', 'eligible_pair_events': len(left),
                          'reference_events': len(eligible(a)), 'comparison_events': len(right),
                          'counts': dict(counts),
                          'entity_count_ceiling': sum((Counter(map(entity, left)) & Counter(map(entity, right))).values()),
                          'phase_count_ceiling': sum((Counter(map(phase, left)) & Counter(map(phase, right))).values())})
        pair_cache[cache_key] = matched, losses
        return matched, losses

    rows = []
    for trace_id, measured in references.items():
        a = traces[trace_id]
        owner = tasks[a.task_id]
        graph = ancestors(owner)
        premises = {p.premise_id for p in owner.premises}
        if measured['support_scope'] == 'registered_pilot_facts':
            premises &= {pid for tid, pid in real_pairs if tid == trace_id}
        noise = [t for t in traces.values() if t.task_id == a.task_id and t.id != a.id and t.seed != a.seed]
        noise_matches = set().union(*(compare(a, b, None, True)[0] for b in noise))
        cells, common, examples = Counter(), Counter(), []
        # Rank identifies the furthest stage reached by ANY saved comparison;
        # it is a loss diagnosis, never a new alignment or a negative label.
        stages = ['no_comparison', 'boundary_or_unclassified', 'no_same_entity', 'phase_incompatible',
                  'expression_incompatible', 'order_or_context_conflict', 'ambiguous_repeated_step', 'matched']
        for event in eligible(a):
            key = event.identity.key()
            for premise in sorted(premises - graph.get(event.node_id, set())):
                reasons = []
                for donor_id in sorted(real_pairs[trace_id, premise]):
                    matched, losses = compare(a, traces[donor_id], premise)
                    reasons.append('matched' if key in matched else losses.get(key, 'boundary_or_unclassified'))
                reason = max(reasons or ['no_comparison'], key=stages.index)
                cells[reason] += 1
                if reason == 'matched':
                    common['matched_with_noise' if key in noise_matches else 'matched_without_noise'] += 1
                elif len(examples) < 8:
                    examples.append({'event': key, 'premise': premise, 'reason': reason,
                                     'start': event.start, 'end': event.end, 'text': event.text})
        if (sum(cells.values()), cells['matched'], common['matched_with_noise']) != (
                measured['eligible_cells'], measured['support_cells'], measured['noise_supported_cells']):
            raise ValueError(f'alignment audit does not reconcile with measurement: {trace_id}')
        rows.append({'trace_id': trace_id, 'problem_id': owner.base_group_id,
                     'eligible_cells': sum(cells.values()), 'cells_by_outcome': dict(cells),
                     'noise_support': dict(common), 'examples': examples})
    totals = Counter()
    for row in rows:
        totals.update(row['cells_by_outcome'])
    return {'protocol': 'natural_alignment_loss_audit_v1', 'changes_measurement': False,
            'interpretation': 'Counts describe saved parsed events, not annotated parser recall. '
                              'Count ceilings ignore expression, order and ambiguity; they are not achieved coverage. '
                              'An incompatible parsed event is not proof that the model omitted the step.',
            'eligible_cells': sum(totals.values()), 'cells_by_outcome': dict(totals),
            'trajectories': rows, 'pair_diagnostics': pair_rows}
