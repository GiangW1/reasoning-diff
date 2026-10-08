#!/usr/bin/env python3
"""Fixed natural coverage acquisition: three edit values, 24 base seeds.

Keep the 24 existing reference trajectories, extend only their pre-registered
three premises, and report edit/noise sampling ablations. This exploratory
acquisition does not repair the original cohort or authorize formal analysis.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import extend_natural_pilot as engine
from reasoning_diff import events
from reasoning_diff.artifacts import write_manifest
from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, write_json, write_jsonl
from reasoning_diff.next_round import registered_pilot_edits, scan_edits
from reasoning_diff.schema import Task

NOISE_SEEDS = tuple(range(24))


def expanded_edits(task):
    chosen = {e.changed_premise_ids[0] for e in registered_pilot_edits(task)}
    return [e for e in scan_edits(task, 3) if e.changed_premise_ids[0] in chosen]


def expected_source_requests(tasks):
    return ({(t.task_id, s) for t in tasks for s in engine.NOISE_SEEDS}
            | {(e.task.task_id, s) for t in tasks for e in registered_pilot_edits(t) for s in engine.PAIRED_SEEDS})


def additional_requests(tasks, reused):
    requests = []
    for task in tasks:
        for owner, seeds, kind in [(task, NOISE_SEEDS, 'noise'),
                                  *[(e.task, engine.PAIRED_SEEDS, 'edit') for e in expanded_edits(task)]]:
            for seed in seeds:
                if (owner.task_id, seed) in reused:
                    continue
                identity = {'task_id': owner.task_id, 'seed': seed, 'kind': kind}
                requests.append({**identity, 'id': 'coverage-' + digest(identity)[:20], 'task': owner.to_dict()})
    return requests


def load_source(source):
    manifest = read_json(source / 'manifest.json')
    for name, checksum in manifest['file_hashes'].items():
        if file_digest(source / name) != checksum:
            raise ValueError('source manifest mismatch')
    report = read_json(source / 'measurement_report.json')
    if (not report.get('posthoc_reparse') or report['n_new'] != 80
            or not report['checks']['extension_generation_complete']
            or report['parser_hash'] != file_digest(Path(events.__file__))):
        raise ValueError('require completed 80-request extension measured with this parser')
    rows = read_jsonl(source / 'traces.jsonl')
    owners = {r['task_id']: Task.from_dict(r) for r in read_jsonl(source / 'tasks.jsonl')}
    tasks = [owners[key] for key in sorted(report['by_problem'])]
    expected = expected_source_requests(tasks)
    if len(rows) != len(expected) or {(r['task_id'], r['seed']) for r in rows} != expected:
        raise ValueError('missing or duplicate reused source request')
    generation = report['generation_protocol']
    for row in rows:
        meta = row['metadata']
        if (meta['revision'] != generation['revision'] or meta['sampling'] != generation['sampling']
                or meta['natural_prompt_policy'] != generation['natural_prompt_policy']
                or meta.get('boundary_status') != 'ok' or not meta.get('enable_thinking')
                or meta.get('finalizer_used') or meta.get('thinking_forced_close')):
            raise ValueError('reused generation conditions differ')
    return tasks, rows, report


def plan(args):
    root, source = args.out_root.resolve(), args.source.resolve()
    if not root.is_relative_to(engine.SERVER) or root == source or root.is_relative_to(source):
        raise ValueError('use separate server output storage')
    if root.exists() and any(root.iterdir()):
        raise ValueError('plan requires an empty directory')
    if not args.gpus or len(set(args.gpus)) != len(args.gpus) or min(args.gpus) < 0 or args.batch_size < 1:
        raise ValueError('invalid GPU list or batch size')
    tasks, rows, source_report = load_source(source)
    previous = source_report['generation_protocol']
    budget_path = Path(source_report['source_extension']) / 'budget.json'
    budget = read_json(budget_path)
    protocol = {key: previous[key] for key in ('model', 'revision', 'model_root', 'max_new', 'sampling', 'natural_prompt_policy')}
    protocol.update(protocol='natural_fixed_reference_three_value_extension_v1', source=str(source),
        source_files=read_json(source / 'manifest.json')['file_hashes'], source_hashes=engine.source_hashes(),
        matching_policy=events.ALIGNMENT_POLICY, gpus=args.gpus, batch_size=args.batch_size,
        paired_seeds=list(engine.PAIRED_SEEDS), noise_seeds=list(NOISE_SEEDS), edit_values_per_premise=3,
        seconds=budget['seconds'], budget_origin={'file': str(budget_path), 'sha256': file_digest(budget_path), **budget},
        formal_evidence=False, original_natural_matching_resolved=False,
        acquisition_reason='After the 80-request pilot failed per-problem support gates; all 280 requests fixed before acquisition, no outcome-based resampling.')
    requests = additional_requests(tasks, expected_source_requests(tasks))
    write_json(root / 'protocol.json', protocol)
    write_json(root / 'plan.json', {'protocol_digest': digest(protocol), 'requests': requests})
    write_json(root / 'budget.json', budget)
    summary = {'problems': len(tasks), 'reference_traces': len(tasks) * 3, 'reused_traces': len(rows),
        'new_requests': len(requests), 'new_edits': sum(r['kind'] == 'edit' for r in requests),
        'new_noise': sum(r['kind'] == 'noise' for r in requests), 'new_token_ceiling': len(requests) * protocol['max_new'],
        'measurement_denominator': source_report['overall']['eligible_cells'], 'scientific_conclusion': None}
    write_json(root / 'plan_summary.json', summary)
    print(summary, flush=True)


def summarize(root):
    protocol, registered = engine.verified_plan(root)
    tasks, original, old_report = load_source(Path(protocol['source']))
    added = [engine.checkpoint(root, protocol, r) for r in registered['requests']]
    if any(row is None for row in added):
        raise ValueError('registered requests missing; cannot summarize')
    rows = original + added
    report, observations, owners = engine.measure(tasks, rows, noise_seeds=NOISE_SEEDS, edits_for=expanded_edits)
    ablations = {}
    for name, noise, edits in [('previous_acquisition', engine.NOISE_SEEDS, registered_pilot_edits),
                               ('extra_noise_only', NOISE_SEEDS, registered_pilot_edits),
                               ('extra_values_only', engine.NOISE_SEEDS, expanded_edits)]:
        ablations[name] = engine.measure(tasks, rows, noise_seeds=noise, edits_for=edits)[0]
    if ablations['previous_acquisition']['overall'] != old_report['overall']:
        raise ValueError('previous acquisition measurement changed')
    if report['overall']['eligible_cells'] != old_report['overall']['eligible_cells']:
        raise ValueError('fixed reference denominator changed')
    report.update(protocol=protocol, ablations=ablations, n_reused=len(original), n_new=len(added),
        formal_launch_ready=False, original_natural_matching_resolved=False, scientific_conclusion=None,
        new_completion_count=sum(t['status'] == 'natural_complete' for t in added))
    report['checks']['extension_generation_complete'] = all(
        t['status'] == 'natural_complete' and t['metadata'].get('boundary_status') == 'ok' for t in added)
    report['failures'] = [key for key, passed in report['checks'].items() if not passed]
    report['passed'] = not report['failures']
    for name, data in [('tasks.jsonl', owners), ('traces.jsonl', rows), ('observations.jsonl', observations)]:
        write_jsonl(root / name, data)
    write_json(root / 'measurement_report.json', report)
    files = ['tasks.jsonl', 'traces.jsonl', 'observations.jsonl', 'measurement_report.json', 'protocol.json', 'plan.json']
    write_manifest(root, [root / name for name in files], {'traces': len(rows), 'new_requests': len(added)})
    write_json(root / 'pipeline.json', {'status': 'complete', 'measurement_passed': report['passed'],
        'formal_launch_ready': False, 'scientific_conclusion': None})
    print(report['overall'], flush=True)
    print(report['checks'], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('plan', 'run', 'report'), required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--out-root', type=Path, required=True)
    parser.add_argument('--gpus', nargs='+', type=int, default=[2, 3, 6])
    parser.add_argument('--batch-size', type=int, default=4)
    args = parser.parse_args()
    if args.mode == 'plan':
        if args.source is None:
            parser.error('--source is required for plan')
        plan(args)
    elif args.mode == 'run':
        engine.run(args.out_root, reporter=summarize)
    else:
        summarize(args.out_root)


if __name__ == '__main__':
    main()
