"""Publish lightweight PR9 evidence while preserving the original server runs."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/mnt/mydata/wja/reasoning-diff')
REPO = Path('/home/wja/reasoning-diff-pr9-quantity-v3')
OPS = ROOT / 'operations/pr9-formal-gate-20261010'
PUBLICATION = Path(__file__).parent
BUNDLE = ROOT / 'exports/rd-pr9-single-pass-validation-20261010-light'
LIMIT = 5 * 1024**2
TEXT = {'.json', '.jsonl', '.md', '.log', '.txt', '.csv', '.tsv'}
EXPANDED = {'traces.jsonl', 'events.jsonl', 'observations.jsonl', 'labels.jsonl',
            'event_rows.jsonl', 'probe_predictions.jsonl'}
SKIP_DIRS = {'responses', 'checkpoints', 'cache', 'tmp', '__pycache__'}
CODE_NAMES = ['prepare.py', 'queue.py', 'supervise.py', 'continue_unlimited.py',
              'audit_current.py', 'test_acceptance.py', 'test_unlimited.py']


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def main():
    if BUNDLE.exists():
        raise FileExistsError('Preserve existing exports; choose a new name.')
    BUNDLE.mkdir(parents=True)
    included, excluded, runs = [], [], {}

    def copy(source, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        included.append({'source': str(source), 'path': target.relative_to(BUNDLE).as_posix(),
                         'bytes': target.stat().st_size, 'sha256': sha(target)})

    for run in sorted((ROOT / 'runs').glob('pr9-*')):
        if not run.is_dir():
            continue
        dest = BUNDLE / 'runs' / run.name
        for source in sorted(run.rglob('*')):
            if not source.is_file() or source.is_symlink():
                continue
            relative = source.relative_to(run)
            if any(part in SKIP_DIRS or part.startswith(('pytest', 'test-', 'acceptance-test-', 'timeout-test-', 'failure-test-'))
                   for part in relative.parts[:-1]):
                why = 'raw_checkpoint_cache_or_temporary_directory'
            elif source.name in EXPANDED:
                why = 'expanded_token_or_observation_data'
            elif source.suffix not in TEXT:
                why = 'binary_or_runtime_file'
            elif source.stat().st_size > LIMIT:
                why = 'larger_than_5_MiB'
            else:
                copy(source, dest / relative)
                continue
            excluded.append({'run': run.name, 'path': relative.as_posix(),
                             'bytes': source.stat().st_size, 'reason': why})

        checkpoint_rows, role_counts, correct_counts, statuses = [], Counter(), Counter(), Counter()
        for response in sorted((run / 'responses').glob('*.json')):
            saved = json.loads(response.read_text())
            trace = saved['trace']
            metadata = trace.get('metadata', {})
            role = metadata.get('formal_role', 'unknown')
            role_counts[role] += 1
            correct_counts[role] += trace.get('correct') is True
            statuses[trace.get('status', 'unknown')] += 1
            row = {key: trace.get(key) for key in ('id', 'task_id', 'base_group_id', 'seed', 'status', 'correct', 'answer')}
            row.update({key: saved.get(key) for key in ('protocol_digest', 'request_digest', 'trace_digest')})
            row.update({'request_id': response.stem, 'role': role,
                        'file_sha256': sha(response),
                        'text_sha256': hashlib.sha256(trace.get('text', '').encode()).hexdigest(),
                        'generated_tokens': metadata.get('generated_tokens'),
                        'quantity_step_format': metadata.get('quantity_step_format'),
                        'stop_reason': metadata.get('stop_reason')})
            checkpoint_rows.append(row)
        if checkpoint_rows:
            dest.mkdir(parents=True, exist_ok=True)
            (dest / 'checkpoint_summary.jsonl').write_text(''.join(
                json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n' for row in checkpoint_rows))
        overview = {'completed_response_count': len(checkpoint_rows),
                    'completed_by_role': dict(role_counts), 'correct_by_role': dict(correct_counts),
                    'status_counts': dict(statuses)}
        for filename, key in [('pipeline.json', 'pipeline'), ('plan_summary.json', 'plan'),
                              ('validation_analysis_status.json', 'validation_analysis_status')]:
            if (run / filename).exists():
                overview[key] = json.loads((run / filename).read_text())
        runs[run.name] = overview
        write(dest / 'CURRENT_SUMMARY.json', overview)

    for source in sorted((ROOT / 'configs').glob('pr9-*.json')):
        copy(source, BUNDLE / 'configs' / source.name)
    for folder in sorted((ROOT / 'inputs').glob('pr9-*')):
        if not folder.is_dir():
            continue
        for source in sorted(folder.rglob('*')):
            if source.is_file() and source.suffix in TEXT and source.stat().st_size <= LIMIT:
                copy(source, BUNDLE / 'inputs' / folder.name / source.relative_to(folder))
    for source in sorted(OPS.iterdir()):
        if source.is_file() and source.suffix in TEXT and source.stat().st_size <= LIMIT:
            copy(source, BUNDLE / 'operations' / source.name)
    for source in sorted((ROOT / 'operations/storage-audit-20261010').glob('*')):
        if source.is_file() and source.suffix in {'.json', '.csv'}:
            copy(source, BUNDLE / 'storage-audit' / source.name)
    for source in sorted((PUBLICATION / 'checks').glob('*.log')):
        copy(source, BUNDLE / 'checks' / source.name)

    validation = json.loads((OPS / 'VALIDATION_RESULTS.json').read_text())
    gate = json.loads((OPS / 'validation_gate.json').read_text())
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    write(BUNDLE / 'summary.json', {
        'exported_at': datetime.now().astimezone().isoformat(), 'experiment_code_commit': commit,
        'source_pr': 'https://github.com/GiangW1/reasoning-diff/pull/9',
        'runs': runs, 'validation': validation, 'formal_launch_gate': gate,
        'natural_matching_resolved': False, 'formal_experiments_started': False,
        'independent_semantic_audit_completed': False,
        'validation_has_test_families': False,
        'interpretation': 'Engineering/development evidence only. Forced schema coverage is not natural matching recovery; no confirmatory C3 success is established.'})
    copy(OPS / 'VALIDATION_RESULTS.zh-CN.md', BUNDLE / 'VALIDATION_RESULTS.zh-CN.md')
    (BUNDLE / 'README.md').write_text(
        '# PR9 single-pass experiments and validation (2026-10-10)\n\n'
        f'Experiment source commit: `{commit}`. Source PR: GiangW1/reasoning-diff#9.\n\n'
        'Natural and constrained validation each generated 525/525 registered responses. '
        'Reference accuracy was 36/36 and 31/36 respectively. Natural matching coverage was '
        '47.35% (base), 48.59% (related no-op), and 51.77% (neutral no-op). Common noise '
        'coverage was about 30%; rho coverage was 0%, 8.33%, and 0%. Constrained coverage '
        'was 100% by construction. The original natural matching problem remains unresolved.\n\n'
        'Each registered reference/edit/noise condition is generated once; no matching retries '
        'or post-hoc response completion were used in the single-pass batches. Earlier pilot '
        'attempts are separate historical development evidence and are not pooled with validation.\n\n'
        'The validation cohort has no test families, so P3 cannot be estimated. The controlled '
        'report was completed by representing its genuinely empty registered P3 shard; no new '
        'model generation occurred. Natural references are all correct, leaving no error class '
        'for error prediction evaluation in this cohort. The old 24-family formal candidates '
        'include only one test family and prior development exposure. The new formal directories '
        'contain plans only: no formal responses were generated.\n\n'
        'The file named `semantic_audit.json` in historical runs counts placeholder text only; '
        'it is a quality screen, not an independent entity/value/relation semantic audit. '
        'The corrected supervisor requires measured natural and controlled coverage, a fresh '
        'formal test cohort, and independent semantic audit before launch. Actual time deadlines '
        'were removed via the recorded operational adapter while frozen configurations remain '
        'unchanged as provenance.\n\n'
        'Original STATUS files and queue/launch logs are historical snapshots and may say '
        'running or contain old estimates. Use `summary.json`, `VALIDATION_RESULTS.zh-CN.md`, '
        'and each `CURRENT_SUMMARY.json` for this export’s status. Operational source snapshots '
        'are committed under `experiments/pr9-validation-20261010/operations/`; their absolute '
        'paths describe the actual server deployment and are not portable defaults.\n\n'
        'Includes metrics, plans, configs, selected inputs, logs, failure diagnostics, checkpoint '
        'metadata/digests, and storage inventory. Model assets, binary tensors, raw checkpoint '
        'copies, expanded token/observation files, caches, and individual files over 5 MiB are '
        'omitted. `export_manifest.json` records exclusions; original manifests describe full '
        'runs and can reference omitted artifacts. Authoritative originals remain under '
        '`/mnt/mydata/wja/reasoning-diff/`. Verify this export with `sha256sum -c SHA256SUMS`.\n')
    write(BUNDLE / 'export_manifest.json', {
        'size_limit_bytes': LIMIT, 'included_originals': included, 'excluded': excluded,
        'original_artifacts_preserved': True, 'source_manifests_reference_full_runs': True})
    files = sorted(p for p in BUNDLE.rglob('*') if p.is_file())
    assert all(p.stat().st_size <= LIMIT for p in files)
    (BUNDLE / 'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(BUNDLE).as_posix()}\n' for p in files))
    code = PUBLICATION / 'code/experiments/pr9-validation-20261010/operations'
    code.mkdir(parents=True, exist_ok=True)
    for name in CODE_NAMES:
        shutil.copy2(OPS / name, code / name)
    shutil.copy2(Path(__file__), code / 'package_results.py')
    (code / 'README.md').write_text(
        '# PR9 server operation snapshots\n\n'
        'These are the executed 2026-10-10 operational scripts, including coverage gating and '
        'the explicitly requested timeout override. They retain absolute server paths to preserve '
        'the actual deployment. `audit_current.py` is a placeholder-quality screen despite the '
        'historical output filename; it does not establish semantic validity. `prepare.py` '
        'records historical exposed-cohort selection and does not create a fresh confirmatory '
        'test cohort. Frozen experiment source remains unchanged. Read the results bundle '
        'for final outcomes and limitations before reusing the scripts.\n')
    print(json.dumps({'bundle': str(BUNDLE), 'files': len(files) + 1,
                      'bytes': sum(p.stat().st_size for p in BUNDLE.rglob('*') if p.is_file()),
                      'excluded_files': len(excluded), 'code_snapshot': str(code)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
