#!/usr/bin/env python3
"""Balanced natural pilot extension: paired seeds 0..2, noise seeds 0..6.

Reuses a verified reparse_pr8 --pilot export, registers every additional
request before generation, and reports the original seed-0 condition too.
This is exploratory acquisition, not a repair of the original saved cohort.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
from threading import local
import time

from reasoning_diff import cli
from reasoning_diff.alignment_audit import alignment_audit
from reasoning_diff.artifacts import write_manifest
from reasoning_diff.events import ALIGNMENT_POLICY
from reasoning_diff.io import digest, file_digest, read_json, read_jsonl, write_json, write_jsonl
from reasoning_diff.next_round import measurement_report, registered_pilot_edits
from reasoning_diff.schema import Task, Trace

REPO = Path(__file__).resolve().parents[1]
SERVER = Path('/mnt/mydata/wja/reasoning-diff')
PAIRED_SEEDS = (0, 1, 2)
NOISE_SEEDS = tuple(range(7))


def source_hashes():
    return {p.relative_to(REPO).as_posix(): file_digest(p)
            for folder in ('src', 'scripts') for p in sorted((REPO / folder).rglob('*.py'))}


def requests_for(tasks):
    requests = []
    for task in tasks:
        for owner, seeds, kind in [(task, range(3, 7), 'noise'),
                                   *[(e.task, (1, 2), 'edit') for e in registered_pilot_edits(task)]]:
            for seed in seeds:
                identity = {'task_id': owner.task_id, 'seed': seed, 'kind': kind}
                requests.append({**identity, 'id': 'extension-' + digest(identity)[:20], 'task': owner.to_dict()})
    return requests


def load_source(source):
    manifest = read_json(source / 'manifest.json')
    for name, checksum in manifest['file_hashes'].items():
        if file_digest(source / name) != checksum:
            raise ValueError('source manifest mismatch')
    report = read_json(source / 'measurement_report.json')
    if not report.get('posthoc_reparse') or report['trajectory_protocol'] != 'natural':
        raise ValueError('source must be a verified natural pilot reparse')
    rows = read_jsonl(source / 'traces.jsonl')
    all_tasks = {r['task_id']: Task.from_dict(r) for r in read_jsonl(source / 'tasks.jsonl')}
    base_ids = {r['task_id'] for r in rows if ':trace-base:' in r['id']}
    tasks = [all_tasks[key] for key in sorted(base_ids)]
    expected = {(task.task_id, seed) for task in tasks for seed in PAIRED_SEEDS}
    expected |= {(e.task.task_id, 0) for task in tasks for e in registered_pilot_edits(task)}
    if len(rows) != len(expected) or {(r['task_id'], r['seed']) for r in rows} != expected:
        raise ValueError('missing or duplicate source pilot request')
    generation = report['generation_protocol']
    for row in rows:
        meta = row['metadata']
        if (meta.get('sampling') != {k: generation[k] for k in ('temperature', 'top_k', 'top_p')}
                or not meta.get('enable_thinking') or meta.get('finalizer_used')
                or meta.get('thinking_forced_close') or meta.get('boundary_status') != 'ok'):
            raise ValueError('source generation conditions differ')
    revisions = {row['metadata']['revision'] for row in rows}
    if len(revisions) != 1:
        raise ValueError('mixed model revisions')
    return tasks, rows, report, next(iter(revisions))


def plan(args):
    root, source = args.out_root.resolve(), args.source.resolve()
    if not root.is_relative_to(SERVER) or root == source or root.is_relative_to(source):
        raise ValueError('use a separate output directory under server storage')
    if not args.gpus or len(set(args.gpus)) != len(args.gpus) or args.batch_size < 1 or args.time_budget_hours <= 0:
        raise ValueError('invalid GPU list, batch size or time budget')
    if root.exists() and any(root.iterdir()):
        raise ValueError('plan requires an empty output directory; run resumes an existing plan')
    tasks, rows, report, revision = load_source(source)
    generation = report['generation_protocol']
    protocol = {'protocol': 'natural_balanced_seed_extension_v1', 'source': str(source),
                'source_files': read_json(source / 'manifest.json')['file_hashes'],
                'source_hashes': source_hashes(), 'matching_policy': ALIGNMENT_POLICY,
                'model': generation['model'], 'revision': revision, 'model_root': generation['model_root'],
                'max_new': generation['max_new'], 'sampling': {k: generation[k] for k in ('temperature', 'top_k', 'top_p')},
                'natural_prompt_policy': generation['natural_prompt_policy'], 'paired_seeds': list(PAIRED_SEEDS),
                'noise_seeds': list(NOISE_SEEDS), 'batch_size': args.batch_size, 'gpus': args.gpus,
                'seconds': args.time_budget_hours * 3600, 'formal_evidence': False, 'original_natural_matching_resolved': False}
    requests = requests_for(tasks)
    if args.resume_from is not None:
        import_completed(args.resume_from.resolve(), root, protocol, requests)
    write_json(root / 'protocol.json', protocol)
    write_json(root / 'plan.json', {'protocol_digest': digest(protocol), 'requests': requests})
    write_json(root / 'plan_summary.json', {'problems': len(tasks), 'reused_traces': len(rows),
        'additional_edit_traces': sum(r['kind'] == 'edit' for r in requests),
        'additional_noise_traces': sum(r['kind'] == 'noise' for r in requests),
        'reference_traces': len(tasks) * len(PAIRED_SEEDS), 'new_token_ceiling': len(requests) * protocol['max_new'],
        'scientific_conclusion': None})
    print(read_json(root / 'plan_summary.json'), flush=True)


def import_completed(parent, root, protocol, requests):
    """Copy verified checkpoints unchanged, permitting only scheduler changes.

    Freeze the previous protocol and each imported payload digest inside the
    new protocol. The generation/parser source files and registered requests
    must be identical; only this orchestration script may have changed.
    """
    with (parent / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        old, registered = read_json(parent / 'protocol.json'), read_json(parent / 'plan.json')
        execution = {'gpus', 'batch_size', 'seconds', 'source_hashes', 'resume_provenance'}
        scientific = lambda p: {k: v for k, v in p.items() if k not in execution}
        code = lambda p: {k: v for k, v in p['source_hashes'].items() if k != 'scripts/extend_natural_pilot.py'}
        if (registered['protocol_digest'] != digest(old) or registered['requests'] != requests
                or scientific(old) != scientific(protocol) or code(old) != code(protocol)):
            raise ValueError('migration changes scientific protocol, requests or generation/parser code')
        completed = [r for r in requests if checkpoint(parent, old, r) is not None]
        payloads = {r['id']: read_json(parent / 'responses' / (r['id'] + '.json')) for r in completed}
        budget_path = parent / 'budget.json'
        budget = read_json(budget_path) if budget_path.exists() else {'started': time.time()}
        protocol['resume_provenance'] = {'parent_root': str(parent), 'protocol': old,
            'plan_digest': digest(registered), 'checkpoint_digests': {key: digest(value) for key, value in payloads.items()}}
        (root / 'responses').mkdir(parents=True, exist_ok=True)
        for request in completed:
            name = request['id'] + '.json'
            shutil.copyfile(parent / 'responses' / name, root / 'responses' / name)
        write_json(root / 'imported_plan.json', registered)
        write_json(root / 'budget.json', {'started': budget['started'], 'seconds': protocol['seconds']})


def checkpoint_protocol_valid(saved, protocol, request):
    if saved['protocol_digest'] == digest(protocol):
        return True
    lineage = protocol.get('resume_provenance')
    return bool(lineage and lineage['checkpoint_digests'].get(request['id']) == digest(saved)
                and checkpoint_protocol_valid(saved, lineage['protocol'], request))


def verified_plan(root):
    protocol, registered = read_json(root / 'protocol.json'), read_json(root / 'plan.json')
    if registered['protocol_digest'] != digest(protocol) or protocol['source_hashes'] != source_hashes():
        raise ValueError('registered protocol/source changed')
    for name, checksum in protocol['source_files'].items():
        if file_digest(Path(protocol['source']) / name) != checksum:
            raise ValueError('upstream source changed')
    return protocol, registered


def checkpoint(root, protocol, request):
    path = root / 'responses' / (request['id'] + '.json')
    if not path.exists():
        return None
    saved = read_json(path)
    row = saved['trace']
    if (not checkpoint_protocol_valid(saved, protocol, request) or saved['request_digest'] != digest(request)
            or saved['trace_digest'] != digest(row) or row['task_id'] != request['task_id']
            or row['seed'] != request['seed'] or row['metadata']['revision'] != protocol['revision']):
        raise ValueError('checkpoint provenance mismatch')
    return row


def worker(root, index):
    from reasoning_diff.models import generate
    from trace_batching import BatchDecoder
    protocol, registered = verified_plan(root)
    requests = registered['requests'][index::len(protocol['gpus'])]
    missing = [r for r in requests if checkpoint(root, protocol, r) is None]
    if not missing:
        return
    opts = cli.build_parser().parse_args(['prepare', '--fixture', protocol['source'], '--kind', 'igsm',
        '--out-dir', str(root), '--eval-mode', 'scientific', '--backend', 'frozen', '--model-name', protocol['model'], '--device', 'cuda'])
    packed = cli._load_frozen_runtime(opts)
    decoder = BatchDecoder(protocol['batch_size'])
    original_decode, state = generate.decode_loop, local()
    def decode(*args, **kwargs):
        result = decoder(*args, **kwargs)
        state.execution = result['batch_execution']
        return result
    def save(request):
        task = Task.from_dict(request['task'])
        row = generate.generate_task_trace(task, seed=request['seed'], run_id=request['id'], backend='frozen',
            model_name=protocol['model'], packed=packed, device='cuda', max_new=protocol['max_new'],
            enable_thinking=True, allow_forced_target=False, **protocol['sampling']).to_dict()
        if row['metadata']['revision'] != protocol['revision']:
            raise ValueError('model revision differs from source')
        row['metadata'].update(execution=state.execution, op=task.metadata.get('op'), extension_protocol=protocol['protocol'])
        payload = {'protocol_digest': digest(protocol), 'request_digest': digest(request), 'trace_digest': digest(row), 'trace': row}
        path = root / 'responses' / (request['id'] + '.json')
        temporary = path.with_suffix('.tmp')
        write_json(temporary, payload)
        temporary.replace(path)
        print(request['id'], request['kind'], request['seed'], row['status'], row['metadata']['generated_tokens'], flush=True)
    generate.decode_loop = decode
    try:
        with ThreadPoolExecutor(max_workers=protocol['batch_size']) as pool:
            for offset in range(0, len(missing), protocol['batch_size']):
                list(pool.map(save, missing[offset:offset + protocol['batch_size']]))
    finally:
        generate.decode_loop = original_decode
        decoder.close()


def measure(tasks, rows, reference_seeds=PAIRED_SEEDS, noise_seeds=NOISE_SEEDS, *, edits_for=registered_pilot_edits):
    traces = {(row['task_id'], row['seed']): Trace.from_dict(row) for row in rows}
    if len(traces) != len(rows):
        raise ValueError('duplicate task/seed request')
    selected, references, owners, observations, scanned = {}, [], [], [], {}
    for task in tasks:
        bases = {seed: traces[task.task_id, seed] for seed in noise_seeds}
        selected.update({t.id: t.to_dict() for t in bases.values()})
        owners.append(task.to_dict())
        edits = edits_for(task)
        scanned[task.task_id] = list(dict.fromkeys(e.changed_premise_ids[0] for e in edits))
        owners.extend(e.task.to_dict() for e in edits)
        for seed in reference_seeds:
            base = bases[seed]
            references.append(base.to_dict())
            for edit in edits:
                donor = traces[edit.task.task_id, seed]
                selected[donor.id] = donor.to_dict()
                observations.extend(cli._observations(task, base, donor, edit, f'stream:{seed}',
                    f'extension:{task.task_id}:{edit.changed_premise_ids[0]}:seed{seed}'))
            for other_seed, other in bases.items():
                if other_seed != seed:
                    observations.extend(cli._sham_observations(task, base, other, other_seed,
                        f'extension-noise:{task.task_id}:seed{seed}:{other_seed}'))
    obs = [o.to_dict() for o in observations]
    report = measurement_report(references, owners, obs, [], scanned)
    report['alignment_audit'] = alignment_audit(list(selected.values()), owners, obs, report)
    report['pilot_protocol'] = {'reference_seeds': list(reference_seeds), 'noise_seeds': list(noise_seeds),
        'edit_seed_rule': 'same_seed_as_reference', 'scanned_premises': scanned, 'formal_evidence': False}
    return report, obs, owners


def summarize(root):
    protocol, registered = verified_plan(root)
    tasks, original, old_report, _ = load_source(Path(protocol['source']))
    added = [checkpoint(root, protocol, request) for request in registered['requests']]
    if any(row is None for row in added):
        raise ValueError('registered requests missing; cannot summarize an incomplete extension')
    rows = original + added
    report, observations, owners = measure(tasks, rows)
    ablations = {}
    for name, refs, noise in [('original_seed0', (0,), PAIRED_SEEDS),
                              ('seed0_extended_noise', (0,), NOISE_SEEDS),
                              ('all_paired_original_noise', PAIRED_SEEDS, PAIRED_SEEDS)]:
        ablations[name] = measure(tasks, rows, refs, noise)[0]
    if ablations['original_seed0']['overall'] != old_report['overall']:
        raise ValueError('original seed-0 measurement changed')
    report.update(protocol=protocol, ablations=ablations, n_reused=len(original), n_new=len(added),
                  formal_launch_ready=False, original_natural_matching_resolved=False,
                  new_completion_count=sum(t['status'] == 'natural_complete' for t in added), scientific_conclusion=None)
    complete = all(t['status'] == 'natural_complete' and t['metadata'].get('boundary_status') == 'ok' for t in added)
    report['checks']['extension_generation_complete'] = complete
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


def run(root, reporter=summarize):
    protocol, registered = verified_plan(root)
    with (root / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if all(checkpoint(root, protocol, r) is not None for r in registered['requests']):
            reporter(root)
            return
        for directory in ('logs', 'tmp', 'cache', 'responses'):
            (root / directory).mkdir(exist_ok=True)
        budget_path = root / 'budget.json'
        budget = read_json(budget_path) if budget_path.exists() else {'started': time.time(), 'seconds': protocol['seconds']}
        write_json(budget_path, budget)
        deadline = budget['started'] + budget['seconds']
        processes, handles = [], []
        try:
            if time.time() >= deadline:
                raise TimeoutError('persisted generation deadline exhausted')
            for index, gpu in enumerate(protocol['gpus']):
                handle = (root / 'logs' / f'gpu{gpu}.log').open('a')
                handles.append(handle)
                env = {**os.environ, 'PYTHONPATH': str(REPO / 'src'), 'PYTHONDONTWRITEBYTECODE': '1',
                    'CUDA_DEVICE_ORDER': 'PCI_BUS_ID', 'CUDA_VISIBLE_DEVICES': str(gpu), 'PYTHONUNBUFFERED': '1',
                    'RD_MODEL_ROOT': protocol['model_root'], 'RD_LOCAL_FILES_ONLY': '1', 'HF_HUB_OFFLINE': '1',
                    'HF_HOME': str(root / 'cache'), 'TMPDIR': str(root / 'tmp'),
                    'OMP_NUM_THREADS': '4', 'OPENBLAS_NUM_THREADS': '4', 'MKL_NUM_THREADS': '4'}
                processes.append(subprocess.Popen([sys.executable, __file__, '--mode', 'worker', '--out-root', str(root),
                    '--worker-index', str(index)], cwd=REPO, env=env, stdout=handle, stderr=subprocess.STDOUT, start_new_session=True))
            while any(p.poll() is None for p in processes):
                if any(p.poll() not in (None, 0) for p in processes):
                    raise RuntimeError('generation worker failed; see GPU logs')
                if time.time() >= deadline:
                    raise TimeoutError('persisted generation deadline exhausted')
                count = len(list((root / 'responses').glob('*.json')))
                write_json(root / 'pipeline.json', {'status': 'running', 'completed': count, 'planned': len(registered['requests']),
                                                  'elapsed_seconds': time.time() - budget['started']})
                time.sleep(2)
            if any(p.returncode != 0 for p in processes):
                raise RuntimeError('generation worker failed; see GPU logs')
        except BaseException as exc:
            write_json(root / 'pipeline.json', {'status': 'failed', 'error': str(exc), 'scientific_conclusion': None})
            raise
        finally:
            for process in processes:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
            for handle in handles:
                handle.close()
        reporter(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('plan', 'run', 'worker', 'report'), required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--out-root', type=Path, required=True)
    parser.add_argument('--gpus', nargs='+', type=int, default=[2, 3])
    parser.add_argument('--batch-size', type=int, default=2)
    parser.add_argument('--time-budget-hours', type=float, default=1)
    parser.add_argument('--resume-from', type=Path, help='import completed requests into a new plan; preserve budget start')
    parser.add_argument('--worker-index', type=int, default=0)
    args = parser.parse_args()
    if args.mode == 'plan':
        if args.source is None:
            parser.error('--source is required to plan')
        plan(args)
    elif args.mode == 'worker':
        worker(args.out_root, args.worker_index)
    elif args.mode == 'run':
        run(args.out_root)
    else:
        summarize(args.out_root)


if __name__ == '__main__':
    main()
