#!/usr/bin/env python3
"""Plan, checkpoint, and analyze the formal C3 experiment on server GPUs."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import math
import os
from pathlib import Path
import subprocess
import sys
from threading import local
import time

from reasoning_diff import cli
from reasoning_diff.formal import build_design, c2_report, p1_report, p2_report
from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, read_npz, write_json, write_jsonl
from reasoning_diff.next_round import base_trajectories, measurement_report, select_dev_layer
from reasoning_diff.schema import Task
from reasoning_diff.spurious_intervention import fit_direction, p3_report, run_p3
from reasoning_diff.splits import DEFAULT_FRACTIONS

REPO = Path(__file__).resolve().parents[1]


def source_hash():
    files = [*sorted((REPO / 'src').rglob('*.py')), Path(__file__), Path(__file__).with_name('trace_batching.py')]
    return digest({p.relative_to(REPO).as_posix(): file_digest(p) for p in files})


def select_tasks(tasks, count, excluded, seed):
    families = {}
    for task in tasks:
        if task.base_group_id in excluded:
            continue
        if task.base_group_id in families:
            raise ValueError('supply one base task per family; generate variants from the frozen design')
        if task.graph_status != 'complete' or not task.nodes:
            raise ValueError('formal T1 requires an independent complete task graph')
        families[task.base_group_id] = task
    strata = {}
    for task in families.values():
        strata.setdefault(task.metadata.get('op', len(task.nodes)), []).append(task)
    if not strata or count <= 0 or count % len(strata):
        raise ValueError('n_problems must be positive and divisible by the number of difficulty strata')
    selected = []
    for op, bucket in sorted(strata.items()):
        ordered = sorted(bucket, key=lambda t: digest([seed, t.base_group_id]))
        if len(ordered) < count // len(strata):
            raise ValueError(f'insufficient unseen op{op} families')
        selected.extend(ordered[:count // len(strata)])
    return selected


def plan(args):
    config = read_json(args.config)
    if args.dataset is not None:
        config['dataset'] = str(args.dataset.resolve())
    if args.model:
        config['model'] = args.model
        config['layers'] = [0, 12, 24, 35] if args.model == 'qwen3-8b' else [0, 9, 18, 27]
    from reasoning_diff.models.adapters import card
    model_card = card(config['model'])
    if (not config['gpus'] or len(set(config['gpus'])) != len(config['gpus']) or min(config['gpus']) < 0
            or config['batch_size'] < 1 or config['max_new'] < 1
            or len(config['layers']) < 2 or len(set(config['layers'])) != len(config['layers'])
            or min(config['layers']) < 0 or max(config['layers']) >= model_card['layers']
            or (config.get('time_budget_hours') is not None and config['time_budget_hours'] <= 0)):
        raise ValueError('invalid GPU, batch, generation, layer, or time budget configuration')
    root = args.out_root.resolve()
    if (root / 'protocol.json').exists():
        protocol, _ = verified_plan(root)
        if protocol['config'] != config:
            raise ValueError('existing plan has a different configuration; use a new output root')
        return
    if root.exists() and any(root.iterdir()):
        raise ValueError('plan output already contains files without a frozen protocol')
    dataset = Path(config['dataset'])
    opts = cli.build_parser().parse_args(['prepare', '--fixture', str(dataset), '--kind', config.get('kind', 'igsm'), '--out-dir', str(root)])
    selected = select_tasks(cli._load_tasks(opts), config['n_problems'], set(config.get('exclude_groups', [])), config['split_seed'])
    design = build_design(selected, seeds=config['reference_seeds'], noise_seeds=config['noise_seeds'],
                          edit_values=config['edit_values'], split_seed=config['split_seed'])
    protocol = {'version': 'formal_c3_v1', 'config': config, 'revision': model_card['revision'],
                'source_hash': source_hash(), 'dataset_hash': file_digest(dataset), 'design_digest': digest(design),
                'frozen_at': time.time(), 'scientific_gates': 'not_preregistered',
                'registration': 'local_prospectively_frozen_design_not_external_registration',
                'measurement_estimand': 'matched_cell_response_rate_excess_v1',
                'family_split_fractions': DEFAULT_FRACTIONS, 'conditions': ['base', 'related_noop', 'neutral_noop'],
                'known_development_exclusions': config.get('exclude_groups', []),
                'dataset_exposure': config.get('dataset_exposure', 'unknown'),
                'confirmatory_claim_ready': False}
    write_json(root / 'protocol.json', protocol)
    write_json(root / 'design.json', design)
    write_jsonl(root / 'tasks.jsonl', design['tasks'])
    write_jsonl(root / 'splits.jsonl', design['splits'])
    write_json(root / 'plan_summary.json', {**design['summary'],
        'decode_token_ceiling': len(design['requests']) * config['max_new'],
        'expected_opportunities': {'edit_values': config['edit_values'], 'reference_seeds': config['reference_seeds'],
                                   'noise_donors_per_reference': len(config['noise_seeds'])},
        'p3_decode_calls_per_selected_prefix': 14, 'semantic_audit': 'pending', 'scientific_conclusion': None})
    print(read_json(root / 'plan_summary.json'), flush=True)


def verified_plan(root):
    protocol, design = read_json(root / 'protocol.json'), read_json(root / 'design.json')
    if protocol['source_hash'] != source_hash() or protocol['design_digest'] != digest(design):
        raise ValueError('code or frozen design changed; use a new output root')
    if protocol['dataset_hash'] != file_digest(protocol['config']['dataset']):
        raise ValueError('dataset changed after design freeze')
    return protocol, design


def saved_response(root, protocol, request):
    path = root / 'responses' / (request['id'].replace(':', '_') + '.json')
    if not path.exists():
        return None
    payload = read_json(path)
    row = payload['trace']
    if (payload['protocol_digest'] != digest(protocol) or payload['request_digest'] != digest(request)
            or payload['trace_digest'] != digest(row) or row['task_id'] != request['task_id']
            or row['seed'] != request['seed'] or row['metadata']['revision'] != protocol['revision']):
        raise ValueError('checkpoint provenance mismatch')
    return row


def worker(root, index, reference_only=False):
    from reasoning_diff.models import generate
    from trace_batching import BatchDecoder
    protocol, design = verified_plan(root)
    config = protocol['config']
    owners = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    roles = {s['task_id']: s['role'] for s in design['splits']}
    requests = design['requests'][index::len(config['gpus'])]
    if reference_only:
        requests = [r for r in requests if r['role'] == 'reference']
    missing = [r for r in requests if saved_response(root, protocol, r) is None]
    if not missing:
        return
    opts = cli.build_parser().parse_args(['prepare', '--fixture', str(root / 'tasks.jsonl'), '--kind', 'task_jsonl',
        '--out-dir', str(root), '--eval-mode', 'scientific', '--backend', 'frozen', '--model-name', config['model'], '--device', 'cuda'])
    runtime = cli._load_frozen_runtime(opts)
    decoder, state = BatchDecoder(config['batch_size']), local()
    original_decode = generate.decode_loop

    def decode(*a, **kw):
        output = decoder(*a, **kw)
        state.execution = output['batch_execution']
        return output

    def save(request):
        owner = owners[request['task_id']]
        trace = generate.generate_task_trace(owner, seed=request['seed'], run_id=request['id'], backend='frozen',
            model_name=config['model'], packed=runtime, device='cuda', max_new=config['max_new'],
            allow_forced_target=False, enable_thinking=True, **config['sampling'])
        trace.metadata.update(formal_role=request['role'], formal_split=roles[owner.task_id],
                              formal_condition=owner.metadata['formal_condition'], execution=state.execution)
        row = trace.to_dict()
        if row['metadata']['revision'] != protocol['revision']:
            raise ValueError('model revision differs from frozen protocol')
        write_json(root / 'responses' / (request['id'].replace(':', '_') + '.json'),
            {'protocol_digest': digest(protocol), 'request_digest': digest(request), 'trace_digest': digest(row), 'trace': row})
        print(request['id'], request['role'], trace.status, flush=True)

    generate.decode_loop = decode
    try:
        with ThreadPoolExecutor(max_workers=config['batch_size']) as pool:
            # References are first, so the answer-only screen can be inspected
            # before the much larger fixed scan finishes.
            missing.sort(key=lambda r: (r['role'] != 'reference', r['task_id'], r['seed']))
            for start in range(0, len(missing), config['batch_size']):
                list(pool.map(save, missing[start:start + config['batch_size']]))
    finally:
        generate.decode_loop = original_decode
        decoder.close()


def audit_sample(traces, observations, limit=240):
    owners = {r['id']: r for r in traces}
    buckets = {}
    for row in observations:
        ref = owners[row['reference_trace']]
        stratum = (ref['metadata']['formal_condition'], row['outcome'], (row.get('rng_pair') or '').startswith('sham:'))
        buckets.setdefault(stratum, []).append(row)
    result = []
    per_bucket = max(1, limit // max(len(buckets), 1))
    for stratum, bucket in sorted(buckets.items()):
        for row in sorted(bucket, key=lambda r: digest(r['observation_id']))[:per_bucket]:
            ref, comparison = owners[row['reference_trace']], owners[row['comparison_trace']]
            def excerpt(trace, identity):
                event = next((e for e in trace['events'] if event_identity_key(e) == identity), None)
                return trace['text'][max(0, event['start'] - 100):event['end'] + 100] if event else None
            result.append({'audit_id': row['observation_id'], 'stratum': stratum,
                'reference_trace': ref['id'], 'comparison_trace': comparison['id'],
                'reference_excerpt': excerpt(ref, row['event_pair'][0]),
                'comparison_excerpt': excerpt(comparison, row['event_pair'][1]) if len(row['event_pair']) > 1 else None,
                'reported_outcome': row['outcome'], 'event_valid': None, 'alignment_valid': None,
                'annotator': None, 'note': None})
    return result


def event_identity_key(event):
    from reasoning_diff.schema import EventIdentity
    return EventIdentity(**event['identity']).key()


def measure(root):
    protocol, design = verified_plan(root)
    traces = [saved_response(root, protocol, r) for r in design['requests']]
    if any(t is None for t in traces):
        raise ValueError('registered requests missing; resume generation before measurement')
    from reasoning_diff.formal import observations_for
    observations = observations_for(design, traces)
    prepare = root / 'prepare'
    for name, rows in [('tasks', design['tasks']), ('traces', traces), ('splits', design['splits']), ('edits', design['edits'])]:
        write_jsonl(prepare / f'{name}.jsonl', rows)
    cli._write_stage(prepare, 'observations', observations,
        extra_files=[prepare / f'{n}.jsonl' for n in ('tasks', 'traces', 'splits', 'edits')],
        config={'command': 'formal_prepare', 'protocol_digest': digest(protocol), 'eval_mode': 'scientific',
                'source_kinds': {t['task_id']: t['source_kind'] for t in design['tasks']}})
    reports, table = {}, []
    for condition in ('base', 'related_noop', 'neutral_noop'):
        tasks = [t for t in design['tasks'] if t['metadata']['formal_condition'] == condition]
        task_ids = {t['task_id'] for t in tasks}
        rows = [t for t in traces if t['task_id'] in task_ids]
        reports[condition] = measurement_report(rows, tasks, observations, design['splits'])
        for row in reports[condition]['trajectories']:
            ref = next(t for t in rows if t['id'] == row['trace_id'])
            events = ref['events']
            row.update(condition=condition, restatement_fraction=sum(e['event_kind'] == 'restatement' for e in events) / max(len(events), 1),
                       calculation_fraction=sum(e['event_kind'] == 'calculation' for e in events) / max(len(events), 1),
                       answer_completed=ref.get('answer') is not None and ref['metadata'].get('stop_reason') != 'max_new',
                       answer_correct=ref.get('correct'))
            table.append(row)
    write_json(root / 'measurement.json', {'conditions': reports, 'interpretation_status': 'requires_independent_audit',
        'engineering_thresholds_are_scientific_gates': False, 'unknown_is_negative': False})
    write_jsonl(root / 'p1_table.jsonl', table)
    write_json(root / 'p1.json', {'primary_base': p1_report(table),
        'secondary_all_conditions': p1_report(table, conditions=('base', 'related_noop', 'neutral_noop')),
        'secondary_answered_only': p1_report(table, conditions=('base', 'related_noop', 'neutral_noop'), answered_only=True)})
    p2 = p2_report(traces, design['tasks'], observations)
    write_json(root / 'p2.json', p2)
    write_jsonl(root / 'audit_sample.jsonl', audit_sample(traces, observations))
    refs = base_trajectories(traces, design['tasks'])
    audit_refs = sorted(refs, key=lambda r: digest(r['id']))[:24]
    write_jsonl(root / 'parser_recall_audit.jsonl', [{'trace_id': r['id'], 'problem_id': r['base_group_id'],
        'text': r['text'], 'parsed_events': r['events'], 'missed_gold_events': None, 'false_events': None, 'annotator': None} for r in audit_refs])
    reference_tasks = {r['task_id'] for r in design['requests'] if r['role'] == 'reference'}
    write_jsonl(root / 'semantic_audit.jsonl', [{'task_id': t['task_id'], 'question': t['question'],
        'base_group_id': t['base_group_id'], 'condition': t['metadata']['formal_condition'],
        'independent_semantic_noop': None, 'annotator': None} for t in design['tasks']
        if t['metadata']['formal_condition'] != 'base' and t['task_id'] in reference_tasks])
    print({c: r['overall'] for c, r in reports.items()}, flush=True)


def execute(root, name, command, gpu=None):
    protocol, _ = verified_plan(root)
    config = protocol['config']
    env = dict(os.environ, PYTHONUNBUFFERED='1', RD_MODEL_ROOT=config['model_root'], RD_LOCAL_FILES_ONLY='1')
    if gpu is not None:
        env['CUDA_VISIBLE_DEVICES'] = str(gpu)
    timeout = None
    if config.get('time_budget_hours') is not None:
        budget = root / 'budget.json'
        if not budget.exists():
            write_json(budget, {'started': time.time(), 'seconds': config['time_budget_hours'] * 3600})
        saved = read_json(budget)
        timeout = saved['seconds'] - (time.time() - saved['started'])
        if timeout <= 0:
            raise TimeoutError('persisted wall-clock budget exhausted')
    logs = root / 'logs'
    logs.mkdir(exist_ok=True)
    print(name, flush=True)
    with (logs / f'{name}.log').open('a', encoding='utf-8') as log:
        subprocess.run([str(x) for x in command], env=env, stdout=log, stderr=subprocess.STDOUT,
                       cwd=REPO, check=True, timeout=timeout)


def generate(root, reference_only=False):
    protocol, _ = verified_plan(root)
    with ThreadPoolExecutor(max_workers=len(protocol['config']['gpus'])) as pool:
        for job in [pool.submit(execute, root, f"{'answers' if reference_only else 'generate'}-{i}",
                    [sys.executable, Path(__file__), '--mode', 'worker', '--out-root', root, '--worker-index', i,
                     *(['--reference-only'] if reference_only else [])], gpu)
                    for i, gpu in enumerate(protocol['config']['gpus'])]:
            job.result()


def answer_screen(root):
    protocol, design = verified_plan(root)
    from collections import Counter
    rows = [saved_response(root, protocol, r) for r in design['requests'] if r['role'] == 'reference']
    if any(r is None for r in rows):
        raise ValueError('answer screen missing registered references')
    counts = {}
    for condition in ('base', 'related_noop', 'neutral_noop'):
        for role in ('probe_train', 'dev', 'direction_fit', 'test'):
            subset = [r for r in rows if r['metadata']['formal_condition'] == condition and r['metadata']['formal_split'] == role]
            counts[f'{condition}/{role}'] = dict(Counter(str(int(r['status'] == 'natural_complete' and r.get('correct') is True)) for r in subset))
    answered = [r for r in rows if r.get('answer') is not None and r['metadata'].get('stop_reason') != 'max_new']
    outcomes = {int(r.get('correct') is True) for r in answered}
    result = {'n_references': len(rows), 'n_problems': len({r['base_group_id'] for r in rows}),
              'class_counts_by_condition_and_split': counts,
              'answered_class_counts': dict(Counter(str(int(r.get('correct') is True)) for r in answered)),
              'failure_counts': dict(Counter(r['status'] for r in rows if r['status'] != 'natural_complete')),
              'status': 'two_outcomes_observed' if len(outcomes) == 2 else 'single_class',
              'parser_and_budget_failures_are_not_genuine_reasoning_errors': True,
              'failure_as_incorrect': True, 'correctness_does_not_change_cohort': True,
              'scientific_conclusion': None}
    write_json(root / 'answer_screen.json', result)
    print(result, flush=True)
    return result


def fit(root):
    protocol, _ = verified_plan(root)
    config, prepare, labels = protocol['config'], root / 'prepare', root / 'labels'

    def stage(name, *args, gpu=None):
        execute(root, name, [sys.executable, '-m', 'reasoning_diff', *args, '--eval-mode', 'scientific', '--resume'], gpu)

    stage('label', 'label', '--in-dir', prepare, '--out-dir', labels)

    def lane(index, gpu):
        for layer in config['layers'][index::len(config['gpus'])]:
            features, probes = root / f'collect-layer{layer}', root / f'fit-layer{layer}'
            stage(f'collect-{layer}', 'collect', '--fixture', root / 'tasks.jsonl', '--kind', 'task_jsonl',
                '--in-dir', prepare, '--out-dir', features, '--backend', 'frozen', '--model-name', config['model'],
                '--device', 'cuda', '--hidden-layer', layer, gpu=gpu)
            stage(f'fit-{layer}', 'fit', '--in-dir', features, '--labels-dir', labels, '--out-dir', probes)

    with ThreadPoolExecutor(max_workers=len(config['gpus'])) as pool:
        for job in [pool.submit(lane, i, g) for i, g in enumerate(config['gpus'])]:
            job.result()
    scores = []
    for layer in config['layers']:
        row = next((r for r in read_jsonl(root / f'fit-layer{layer}/probes.jsonl') if r.get('head') == 'behavior' and 'U' in r), {})
        scores.append((row.get('metrics', {}).get('dev') or {}).get('auc'))
    usable = [(l, s) for l, s in zip(config['layers'], scores) if s is not None and math.isfinite(s)]
    if len(usable) < 2:
        write_json(root / 'layer_selection.json', {'status': 'insufficient_dev_layers', 'main': None, 'weak': None,
            'layers': config['layers'], 'dev_behavior_auc': scores, 'scientific_conclusion': None})
        return False
    selected = select_dev_layer([l for l, _ in usable], [s for _, s in usable])
    weak = min((l for l, _ in usable if l != selected),
               key=lambda l: (scores[config['layers'].index(l)], l))
    write_json(root / 'layer_selection.json', {'status': 'ready', 'main': selected, 'weak': weak,
        'layers': config['layers'], 'dev_behavior_auc': scores})
    stage('fit-all', 'fit', '--in-dir', root / f'collect-layer{selected}', '--labels-dir', labels, '--out-dir', root / 'fit',
          '--position', 'all', '--dev-layer-ids', *[l for l, _ in usable], '--dev-layer-scores', *[s for _, s in usable])
    stage('calibrate', 'calibrate', '--in-dir', root / 'fit', '--features-dir', root / f'collect-layer{selected}',
          '--labels-dir', labels, '--out-dir', root / 'calibration', '--alpha', '0.1', '--head', 'behavior')
    for layer in (selected, weak):
        source = root / f'collect-layer{layer}'
        direction = fit_direction(read_npz(source / 'features.npz')['H'], read_jsonl(source / 'event_rows.jsonl'),
                                  read_jsonl(labels / 'labels.jsonl'), read_jsonl(prepare / 'tasks.jsonl'), read_jsonl(prepare / 'splits.jsonl'))
        write_json(root / f's_direction-layer{layer}.json', direction)
    return True


def p3_signature(root):
    protocol, _ = verified_plan(root)
    selection = read_json(root / 'layer_selection.json')
    files = [root / f"s_direction-layer{l}.json" for l in (selection['main'], selection['weak'])]
    files.extend(root / f"collect-layer{selection['main']}" / n for n in ('features.npz', 'event_rows.jsonl'))
    files.extend(root / 'prepare' / n for n in ('traces.jsonl', 'tasks.jsonl'))
    return digest({'protocol': protocol, 'selection': selection,
                   'files': {p.relative_to(root).as_posix(): file_digest(p) for p in files}})


def p3_worker(root, index):
    protocol, _ = verified_plan(root)
    config, selection = protocol['config'], read_json(root / 'layer_selection.json')
    source = root / f"collect-layer{selection['main']}"
    tasks = read_jsonl(root / 'prepare/tasks.jsonl')
    event_rows = read_jsonl(source / 'event_rows.jsonl')
    hidden = read_npz(source / 'features.npz')['H']
    direction = read_json(root / f"s_direction-layer{selection['main']}.json")
    weak_direction = read_json(root / f"s_direction-layer{selection['weak']}.json")
    signature = p3_signature(root)
    from reasoning_diff.models.adapters import load_frozen
    runtime = load_frozen(config['model'], device='cuda')
    traces = read_jsonl(root / 'prepare/traces.jsonl')
    refs = [r for r in traces if r['metadata']['formal_role'] == 'reference' and r['metadata']['formal_split'] == 'test']
    assigned = refs[index::len(config['gpus'])]
    saved = root / f'p3-gpu{index}.jsonl'
    prior = read_jsonl(saved) if saved.exists() else []
    if (len({r['trace_id'] for r in prior}) != len(prior)
            or not {r['trace_id'] for r in prior} <= {r['id'] for r in assigned}
            or any(r.get('input_signature') != signature for r in prior)):
        raise ValueError('P3 checkpoint cohort mismatch')
    done = {r['trace_id'] for r in prior}
    for trace in assigned:
        if trace['id'] in done:
            continue
        result = run_p3([trace], tasks, event_rows, hidden, direction,
            selection['weak'], weak_direction, runtime, selection['main'],
            max_new=config['max_new'], sampling=config['sampling'], seed=config['split_seed'])
        for row in result:
            row['input_signature'] = signature
        prior.extend(result)
        write_jsonl(saved, prior)
        print(trace['id'], result[0]['status'], flush=True)


def intervene(root):
    protocol, _ = verified_plan(root)
    config, selection = protocol['config'], read_json(root / 'layer_selection.json')
    if selection.get('main') is None or selection.get('weak') is None:
        raise ValueError('formal fit could not identify main and weak dev layers; intervention is not estimable')

    def lane(index, gpu):
        execute(root, f'p3-{index}', [sys.executable, Path(__file__), '--mode', 'p3-worker', '--out-root', root, '--worker-index', index], gpu)
        execute(root, f'c2-{index}', [sys.executable, '-m', 'reasoning_diff', 'intervene', '--in-dir', root / 'prepare',
            '--features-dir', root / f"collect-layer{selection['main']}", '--probes-dir', root / 'fit/pre_step',
            '--labels-dir', root / 'labels', '--out-dir', root / f'c2-gpu{index}', '--backend', 'frozen',
            '--model-name', config['model'], '--device', 'cuda', '--max-new', config['max_new'],
            '--temperature', config['sampling']['temperature'], '--top-k', config['sampling']['top_k'],
            '--top-p', config['sampling']['top_p'],
            '--all-source-pairs', '--pair-split', 'test', '--pair-shard', index, len(config['gpus']),
            '--eval-mode', 'scientific', '--resume'], gpu)

    with ThreadPoolExecutor(max_workers=len(config['gpus'])) as pool:
        for job in [pool.submit(lane, i, g) for i, g in enumerate(config['gpus'])]:
            job.result()
    report(root)


def report(root):
    protocol, design = verified_plan(root)
    p3 = [r for i in range(len(protocol['config']['gpus'])) for r in read_jsonl(root / f'p3-gpu{i}.jsonl')]
    expected = {r['id'] for r in design['requests'] if r['role'] == 'reference'
                and next(s['role'] for s in design['splits'] if s['task_id'] == r['task_id']) == 'test'}
    if len(p3) != len(expected) or {r['trace_id'] for r in p3} != expected:
        raise ValueError('P3 missing or duplicate registered test reference')
    signature = p3_signature(root)
    if any(r.get('input_signature') != signature for r in p3):
        raise ValueError('P3 checkpoint inputs changed')
    write_json(root / 'p3.json', p3_report(p3))
    c2 = [r for i in range(len(protocol['config']['gpus'])) for r in read_jsonl(root / f'c2-gpu{i}/interventions.jsonl')]
    write_json(root / 'c2.json', c2_report(c2, read_jsonl(root / 'prepare/tasks.jsonl')))
    write_json(root / 'experiment_report.json', {'protocol_digest': digest(protocol), 'P1': read_json(root / 'p1.json'),
        'P2': read_json(root / 'p2.json'), 'P3': read_json(root / 'p3.json'), 'C2': read_json(root / 'c2.json'),
        'measurement': read_json(root / 'measurement.json'), 'scientific_conclusion': None,
        'claim_status': 'requires_independent_measurement_audit_and_frozen_decision_rule',
        'dataset_exposure': protocol['dataset_exposure'], 'cross_model_transfer': 'separate_from_within_model_replication'})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('plan', 'answers', 'generate', 'measure', 'fit', 'intervene', 'report', 'all', 'worker', 'p3-worker'), default='plan')
    parser.add_argument('--config', type=Path, default=REPO / 'experiments/formal_c3.json')
    parser.add_argument('--dataset', type=Path)
    parser.add_argument('--model', choices=('qwen3-8b', 'r1-distill-qwen-7b'))
    parser.add_argument('--out-root', type=Path, required=True)
    parser.add_argument('--worker-index', type=int, default=0)
    parser.add_argument('--reference-only', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = args.out_root.resolve()
    if args.mode in {'plan', 'all'}:
        plan(args)
    if args.mode == 'plan':
        return 0
    protocol, _ = verified_plan(root)
    if args.mode in {'worker', 'p3-worker'}:
        if not 0 <= args.worker_index < len(protocol['config']['gpus']):
            raise ValueError('invalid worker index')
        if args.mode == 'worker':
            worker(root, args.worker_index, args.reference_only)
        else:
            p3_worker(root, args.worker_index)
        return 0
    try:
        if args.mode in {'answers', 'all'}:
            generate(root, reference_only=True)
            screen = answer_screen(root)
            if args.mode == 'all' and screen['status'] == 'single_class':
                write_json(root / 'pipeline.json', {'status': 'stopped_unestimable', 'stage': 'answer_screen',
                    'reason': 'answered_references_have_fewer_than_two_correctness_classes', 'scientific_conclusion': None})
                return 0
        if args.mode in {'generate', 'all'}:
            generate(root)
        for mode, function in [('measure', measure), ('fit', fit), ('intervene', intervene), ('report', report)]:
            if args.mode == mode or (args.mode == 'all' and mode != 'report'):
                if function(root) is False:
                    write_json(root / 'pipeline.json', {'status': 'stopped_unestimable', 'stage': mode,
                        'reason': 'cannot_identify_main_and_weak_dev_layers', 'scientific_conclusion': None})
                    return 0
        write_json(root / 'pipeline.json', {'status': 'complete', 'mode': args.mode, 'scientific_conclusion': None})
    except Exception as exc:
        write_json(root / 'pipeline.json', {'status': 'budget_exhausted' if isinstance(exc, (TimeoutError, subprocess.TimeoutExpired)) else 'failed',
                                           'mode': args.mode, 'error': str(exc), 'scientific_conclusion': None})
        raise
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
