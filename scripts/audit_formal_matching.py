#!/usr/bin/env python3
"""Remeasure a frozen formal cohort without generating or changing any trace."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from pathlib import Path

from reasoning_diff import cli
from reasoning_diff.events import align_events
from reasoning_diff.formal import observations_for
from reasoning_diff.io import digest, file_digest, read_json, write_json, write_jsonl
from reasoning_diff.next_round import measurement_report
from reasoning_diff.schema import Task


def audit(source, output, reparse_comparisons=False):
    source, output = source.resolve(), output.resolve()
    if output == source or output.is_relative_to(source) or (output.exists() and any(output.iterdir())):
        raise ValueError('use a new output directory outside the frozen experiment')
    protocol, design = read_json(source / 'protocol.json'), read_json(source / 'design.json')
    if digest(design) != protocol['design_digest'] or file_digest(protocol['config']['dataset']) != protocol['dataset_hash']:
        raise ValueError('frozen design or dataset hash mismatch')
    tasks = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    roles = {s['task_id']: s['role'] for s in design['splits']}
    traces, checkpoints, reparsed = [], {}, []
    for request in design['requests']:
        path = source / 'responses' / (request['id'].replace(':', '_') + '.json')
        saved = read_json(path)
        row = saved['trace']
        if (saved['protocol_digest'] != digest(protocol) or saved['request_digest'] != digest(request)
                or saved['trace_digest'] != digest(row) or row['id'] != request['id']
                or row['task_id'] != request['task_id'] or row['seed'] != request['seed']
                or row['metadata']['revision'] != protocol['revision']):
            raise ValueError(f'checkpoint provenance mismatch: {path.name}')
        if reparse_comparisons and request['role'] != 'reference':
            from reparse_pr8 import reparse_trace
            updated = reparse_trace(row, tasks[row['task_id']], file_digest(Path(cli.__file__).with_name('events.py'))).to_dict()
            reparsed.append({'trace_id': row['id'], 'old_events': len(row['events']), 'new_events': len(updated['events']),
                             'events_changed': digest(row['events']) != digest(updated['events'])})
            row = updated
        traces.append(row)
        checkpoints[path.name] = file_digest(path)
    event_digests = {row['id']: digest(row['events']) for row in traces}
    owners = {row['id']: row for row in traces}
    pair_order = deque((ref, edit['comparison_ids'][seed]) for edit in design['edits']
                       if edit['kind'] != 'source_value_pair' for seed, ref in edit['reference_ids'].items())
    groups = defaultdict(list)
    for request in design['requests']:
        if request['role'] in {'reference', 'noise'}:
            groups[request['task_id']].append(request)
    pair_order.extend((ref['id'], donor['id']) for group in groups.values()
                      for ref in group if ref['role'] == 'reference'
                      for donor in group if donor['role'] == 'noise')
    pair_reports = []

    def align(left, right):
        aligned = align_events(left, right)
        ref_id, other_id = pair_order.popleft()
        if any(event_digests[tid] != digest([e.to_dict() for e in events])
               for tid, events in ((ref_id, left), (other_id, right))):
            raise ValueError('formal comparison order or event identity changed')
        ref = owners[ref_id]
        matched = {a.identity.key() for a, b in aligned['pairs']}
        losses = {r['left']: r for r in aligned.get('unmatched_left', [])}
        eligible = [e for e in left if e.event_region == 'thinking' and e.event_kind != 'restatement' and e.status == 'ok']
        pair_reports.append({
            'reference': ref_id, 'comparison': other_id, 'family_role': roles[ref['task_id']],
            'condition': ref['metadata']['formal_condition'], 'comparison_role': owners[other_id]['metadata']['formal_role'],
            'counts': dict(Counter('matched' if e.identity.key() in matched else
                                  losses.get(e.identity.key(), {}).get('reason', 'unclassified') for e in eligible)),
            'certificates': aligned.get('pair_certificates', []),
            'unmatched': [{**losses.get(e.identity.key(), {}), 'event_id': e.identity.key(),
                           'text': e.text, 'node_id': e.node_id, 'phase': e.event_phase,
                           'expression': e.expression_signature, 'views': e.expression_views,
                           'context': e.alignment_context} for e in eligible if e.identity.key() not in matched],
        })
        return aligned

    original = cli.align_events
    cli.align_events = align
    try:
        observations = observations_for(design, traces)
    finally:
        cli.align_events = original
    if pair_order:
        raise ValueError('some registered comparisons were not measured')
    reports, table = {}, []
    for condition in ('base', 'related_noop', 'neutral_noop'):
        selected_tasks = [t for t in design['tasks'] if t['metadata']['formal_condition'] == condition]
        ids = {t['task_id'] for t in selected_tasks}
        selected_traces = [r for r in traces if r['task_id'] in ids]
        reports[condition] = measurement_report(selected_traces, selected_tasks, observations, design['splits'])
        table.extend({**r, 'condition': condition} for r in reports[condition]['trajectories'])
    summary = {'protocol_digest': digest(protocol), 'design_digest': digest(design),
               'parser_sha256': file_digest(Path(cli.__file__).with_name('events.py')),
               'n_traces': len(traces), 'new_generation_calls': 0,
               'reference_events_frozen': True, 'reparse_comparisons': reparse_comparisons,
               'sampling': {k: protocol['config'][k] for k in ('reference_seeds', 'noise_seeds', 'edit_values')},
               'conditions': {c: r['overall'] for c, r in reports.items()},
               'partial_common_support': sum(r['common_support_diagnostic']['excess'] is not None for r in table),
               'full_rho': sum(r['rho'] is not None for r in table),
               'scientific_conclusion': None}
    write_json(output / 'summary.json', summary)
    write_json(output / 'measurement.json', {'conditions': reports})
    write_json(output / 'source_checkpoints.json', checkpoints)
    write_jsonl(output / 'p1_table.jsonl', table)
    write_jsonl(output / 'pair_diagnostics.jsonl', pair_reports)
    write_jsonl(output / 'observations.jsonl', observations)
    write_jsonl(output / 'reparsed_comparisons.jsonl', reparsed)
    if checkpoints != {name: file_digest(source / 'responses' / name) for name in checkpoints}:
        raise ValueError('source checkpoints changed while auditing')
    print(summary, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--reparse-comparisons', action='store_true')
    args = parser.parse_args()
    audit(args.source, args.output, args.reparse_comparisons)
