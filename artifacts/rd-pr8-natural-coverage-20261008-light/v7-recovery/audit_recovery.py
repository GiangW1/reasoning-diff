"""Audit parser recovery on fixed saved trajectories and original result spans."""
import argparse
import json
from pathlib import Path

from reasoning_diff.graphs import ancestors
from reasoning_diff.schema import EventIdentity, Task


def rows(path):
    return [json.loads(line) for line in path.open()]


def span(event):
    return (event['node_id'], event['value_start'], event['end'], event['event_region'])


def eligible(event):
    return event['event_region'] == 'thinking' and event['event_kind'] != 'restatement' and event['status'] == 'ok'


def load(directory):
    traces = {t['id']: t for t in rows(directory / 'traces.jsonl')}
    tasks = {t['task_id']: Task.from_dict(t) for t in rows(directory / 'tasks.jsonl')}
    report = json.loads((directory / 'measurement_report.json').read_text())
    report = report.get('measurement_quality', report)
    real, noise = set(), set()
    pairs = {}
    ids = {tid: {EventIdentity(**e['identity']).key(): span(e) for e in t['events']} for tid, t in traces.items()}
    for o in rows(directory / 'observations.jsonl'):
        if o['outcome'] not in {'changed', 'no_change'} or o.get('boundary_status') == 'failed':
            continue
        key = o['reference_trace'], ids[o['reference_trace']][o['alignment_ref']]
        if (o.get('rng_pair') or '').startswith('sham:'):
            noise.add(key)
        else:
            cell = (*key, o['premise_id'])
            real.add(cell)
            donor = ids[o['comparison_trace']][o['event_pair'][1]]
            pairs[(o['reference_trace'], o['comparison_trace'], o['premise_id'], key[1], donor)] = o['alignment_certificate']
    cells = set()
    for ref in report['trajectories']:
        tid = ref['trace_id']
        task = tasks[traces[tid]['task_id']]
        graph = ancestors(task)
        premises = {p.premise_id for p in task.premises}
        if ref['support_scope'] == 'registered_pilot_facts':
            premises &= set(report['pilot_protocol']['scanned_premises'][task.task_id])
        for e in traces[tid]['events']:
            if eligible(e):
                cells.update((tid, span(e), p) for p in premises - graph.get(e['node_id'], set()))
    # Pilot protocol lives at the top level in pilot reports. Old reports
    # use every premise, matching the production registered denominator.
    supported = cells & real
    common = {c for c in supported if c[:2] in noise}
    assert (len(cells), len(supported), len(common)) == tuple(report['overall'][k] for k in ('eligible_cells', 'support_cells', 'noise_supported_cells'))
    return traces, report, cells, supported, common, pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--after', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    bt, br, bc, bs, bn, bp = load(args.before)
    at, ar, ac, ass, an, ap = load(args.after)
    assert bt.keys() == at.keys()
    fields = ('text', 'token_ids', 'offsets', 'answer', 'correct', 'status')
    assert all(bt[tid].get(f) == at[tid].get(f) for tid in bt for f in fields)
    removed = []
    additions = []
    for tid, trace in bt.items():
        previous = {span(e): e for e in trace['events'] if eligible(e)}
        current = {span(e): e for e in at[tid]['events'] if eligible(e)}
        removed.extend({'trace': tid, 'event': previous[s]} for s in previous.keys() - current.keys())
        additions.extend({'trace': tid, 'event': current[s]} for s in current.keys() - previous.keys())
    assert not removed, 'Previously eligible result spans disappeared'
    assert bc <= ac, 'Previously eligible cells disappeared'
    added_pairs = []
    for pair in ap.keys() - bp.keys():
        tid, donor, premise, left, right = pair
        if (tid, left, premise) not in ac:
            continue
        aa = next(e for e in at[tid]['events'] if span(e) == left)
        bb = next(e for e in at[donor]['events'] if span(e) == right)
        added_pairs.append({'reference': tid, 'comparison': donor, 'premise': premise,
                            'left': aa, 'right': bb, 'certificate': ap[pair]})
    result = {
        'before': str(args.before), 'after': str(args.after),
        'all_saved_generation_fields_unchanged': True,
        'prior_eligible_result_spans_removed': len(removed),
        'prior_eligible_cells_removed': len(bc - ac),
        'before_overall': br['overall'], 'after_overall': ar['overall'],
        'original_denominator_diagnostic': {
            'eligible_cells': len(bc), 'before_support': len(bs), 'after_support': len(ass & bc),
            'before_common_noise': len(bn), 'after_common_noise': len(an & bc),
            'gained_support': len((ass - bs) & bc), 'lost_support': len(bs - ass),
            'note': 'Diagnostic only; full production denominator includes all recovered steps.'},
        'new_cells': {'eligible': len(ac - bc), 'supported': len(ass - bc), 'common_noise': len(an - bc)},
        'new_events': additions, 'new_or_reassigned_pairs': sorted(added_pairs, key=lambda p: (p['reference'], p['comparison'], p['left']['start'])),
        'pair_audit_note': 'Algorithmic certificates and raw evidence; not a human precision estimate.',
    }
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in {'new_events', 'new_or_reassigned_pairs'}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
