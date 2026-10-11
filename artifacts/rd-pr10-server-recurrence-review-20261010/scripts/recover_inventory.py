"""Recover and verify already-generated PR10 handoff texts. No model execution."""
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path('/mnt/mydata/wja/reasoning-diff')
REPO = Path('/home/wja/reasoning-diff-pr10')
AUDIT = REPO / 'experiments/natural-recurrence-audit-20261010'
OUT = ROOT / 'reports/pr10-server-recurrence-review-20261010'
EXPORT = ROOT / 'exports/rd-pr9-single-pass-validation-20261010-light'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def condition(task_id):
    return 'related_noop' if task_id.endswith(':high') else 'neutral_noop' if task_id.endswith(':low') else 'base'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = OUT / 'source_data'
    artifact = source / 'artifacts'
    artifact.mkdir(parents=True, exist_ok=True)
    link = artifact / EXPORT.name
    if not link.exists():
        link.symlink_to(EXPORT, target_is_directory=True)
    archive = artifact / 'rd-pr8-natural-pilot-20261007-light/raw-and-reparsed-pilot.tar.gz'
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(subprocess.check_output(['git', 'show', 'HEAD:artifacts/rd-pr8-natural-pilot-20261007-light/raw-and-reparsed-pilot.tar.gz'], cwd=REPO))
    module_path = AUDIT / 'scripts/audit_natural_recurrence.py'
    spec = importlib.util.spec_from_file_location('pr10_original_reader', module_path)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    reader.ROOT, reader.ART, reader.PR9 = source, artifact, link
    original = reader.load()
    assert len(original) == 72
    snapshot = json.loads((AUDIT / 'natural-recurrence-evidence.json').read_text())
    snapshot_rows = {r['code']: r for r in snapshot['inventory']}
    assert all(sha(r['text'].encode()) == snapshot_rows[r['code']]['text_sha256'] for r in original)
    original_ids = {(r['code'][0], r['meta']['id']): r for r in original if r['code'][0] in {'P', 'V'}}
    missing = json.loads((AUDIT / 'missing-pr9-fulltexts.json').read_text())['records']
    missing_keys = {(r['run'], r['id']) for r in missing}
    expected, trace_rows, failures = [], [], []
    for prefix, run in [('P', 'pr9-pilot-20261009'), ('V', 'pr9-validation-natural-20261010')]:
        checkpoint_rows = [r for r in rows(EXPORT / 'runs' / run / 'checkpoint_summary.jsonl') if r['role'] in {'reference', 'noise'}]
        assert len(checkpoint_rows) == 72
        tasks = {t['task_id']: t for t in json.loads((ROOT / 'runs' / run / 'design.json').read_text())['tasks']}
        next_code = 25
        for expected_row in checkpoint_rows:
            path = ROOT / 'runs' / run / 'responses' / (expected_row['request_id'] + '.json')
            previously = original_ids.get((prefix, expected_row['id']))
            code = previously['code'] if previously else f'{prefix}{next_code:02}'
            if not previously:
                next_code += 1
            entry = dict(code=code, run=run, id=expected_row['id'], request_id=expected_row['request_id'],
                         task_id=expected_row['task_id'], base_group_id=expected_row['base_group_id'],
                         seed=expected_row['seed'], role=expected_row['role'], condition=condition(expected_row['task_id']),
                         previously_missing=(run, expected_row['id']) in missing_keys, path=str(path), found=path.is_file())
            if not path.is_file():
                failures.append(entry)
                expected.append(entry)
                continue
            raw = path.read_bytes()
            payload = json.loads(raw)
            trace = payload['trace']
            metadata = trace.get('metadata', {})
            text = trace['text']
            identity = all(trace.get(k) == expected_row[k] for k in ('id', 'task_id', 'base_group_id', 'seed'))
            identity = identity and metadata.get('formal_role') == expected_row['role']
            digests = all(payload.get(k) == expected_row[k] for k in ('protocol_digest', 'request_digest', 'trace_digest'))
            entry.update(file_sha256=sha(raw), text_sha256=sha(text.encode()),
                         expected_file_sha256=expected_row['file_sha256'], expected_text_sha256=expected_row['text_sha256'],
                         file_hash_match=sha(raw) == expected_row['file_sha256'],
                         text_hash_match=sha(text.encode()) == expected_row['text_sha256'],
                         metadata_match=bool(identity), protocol_and_request_digest_match=digests,
                         original_audit_text_match=previously is None or previously['text'] == text,
                         text_chars=len(text), generated_tokens=expected_row.get('generated_tokens'))
            entry['verified'] = all(entry[k] for k in ('file_hash_match', 'text_hash_match', 'metadata_match', 'protocol_and_request_digest_match', 'original_audit_text_match'))
            if not entry['verified']:
                failures.append(entry)
            expected.append(entry)
            trace_rows.append({'code': code, 'run': run, 'task': tasks[trace['task_id']], 'meta': expected_row,
                               'source_path': str(path), 'text': text, 'events': trace.get('events', []),
                               'body_start': metadata.get('rendered_prompt_char_len', 0)})
    for r in original:
        if r['code'].startswith('E'):
            trace_rows.append({'code': r['code'], 'run': 'pr8-natural-pilot-20261007-d02a40c',
                               'task': r['task'], 'meta': dict(r['meta'], role='unedited_original'),
                               'source_path': str(archive)+'::'+r['archive_member']+'::line='+str(r['source_line']),
                               'text': r['text'], 'events': r['events'], 'body_start': r['text'].find('<think>')})
    trace_rows.sort(key=lambda r: (r['code'][0], int(r['code'][1:])))
    records = []
    screens = []
    cue = re.compile(r'misread|mistak|\bwrong\b|\berror\b|correct(?:ed|ion)|recalculat|recomput|\bwait\b|conflict|contradict|should be|actually|rather than|instead of|souvenir|\blabel\b|first sentence|interpret', re.I)
    (OUT / 'fulltexts').mkdir(exist_ok=True)
    (OUT / 'screening').mkdir(exist_ok=True)
    for r in trace_rows:
        text = r['text']
        (OUT / 'fulltexts' / (r['code']+'.txt')).write_bytes(text.encode())
        paragraphs = reader.paragraphs(r)
        hits = [i for i, (start, end, para) in enumerate(paragraphs) if end > r['body_start'] and cue.search(para)]
        contexts = sorted({j for i in hits for j in range(max(0, i-1), min(len(paragraphs), i+2))})
        rendered = '\n\n'.join(f'[P{i+1:03} chars {paragraphs[i][0]}:{paragraphs[i][1]}]\n{paragraphs[i][2]}' for i in contexts)
        (OUT / 'screening' / (r['code']+'.txt')).write_text(rendered+'\n')
        locator_flags = reader.flags(r)
        metadata = r['meta']
        item = {k: v for k, v in r.items() if k not in {'text', 'events'}}
        item.update(text_sha256=sha(text.encode()), fulltext_path='fulltexts/'+r['code']+'.txt',
                    condition=condition(metadata['task_id']), text_chars=len(text),
                    cue_paragraphs=[i+1 for i in hits], parser_flags_are_locators_only=locator_flags)
        records.append(item)
        screens.append({'code':r['code'], 'run':r['run'], 'id':metadata['id'], 'task_id':metadata['task_id'],
                        'role':metadata['role'], 'seed':metadata['seed'], 'condition':condition(metadata['task_id']),
                        'chars':len(text), 'cue_paragraphs':len(hits),
                        'parser_sequences_not_labels': [(f['node'], f['sequence']) for f in locator_flags]})
    (OUT / 'records.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    write(OUT / 'coverage-records.json', expected)
    groups = defaultdict(Counter)
    for r in expected:
        c = groups[(r['run'],r['role'],r['seed'],r['condition'])]
        c['expected'] += 1
        c['found'] += r['found']
        c['file_hash_match'] += bool(r.get('file_hash_match'))
        c['text_hash_match'] += bool(r.get('text_hash_match'))
        c['verified'] += bool(r.get('verified'))
        c['missing'] += not r['found']
        c['content_mismatch'] += bool(r['found'] and not r.get('text_hash_match'))
    grouped=[dict(run=k[0],role=k[1],seed=k[2],condition=k[3],**v) for k,v in sorted(groups.items())]
    with (OUT / 'coverage.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(grouped[0]));writer.writeheader();writer.writerows(grouped)
    summary={'pr10_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
             'expected_pr9':len(expected),'found_pr9':sum(r['found'] for r in expected),
             'verified_pr9':sum(bool(r.get('verified')) for r in expected),
             'previously_missing_expected':len(missing),'previously_missing_verified':sum(r['previously_missing'] and bool(r.get('verified')) for r in expected),
             'pr8_original_fulltexts':24,
             'unique_run_task_seed_role_keys':len({(r['run'],r['meta']['task_id'],r['meta']['seed'],r['meta']['role']) for r in records}),
             'unique_fulltext_hashes':len({r['text_sha256'] for r in records}),
             'original_72_text_hashes_verified':72,
             'pr8_archive_sha256':sha(archive.read_bytes()),
             'identity_note':'PR8 trace IDs collide across original GPU shards. Use run/task/seed/role and archive member/line, not trace ID alone.',
             'failures':failures,'groups':grouped,'screening_is_not_semantic_annotation':True,
             'original_snapshot_hashes':{str(p.relative_to(AUDIT)):sha(p.read_bytes()) for p in sorted(AUDIT.rglob('*')) if p.is_file()}}
    write(OUT/'coverage-summary.json',summary)
    write(OUT/'screening-index.json',screens)
    print(json.dumps({k:v for k,v in summary.items() if k not in {'groups','original_snapshot_hashes','failures'}},ensure_ascii=False,indent=2))
    print('Failures:',len(failures))


if __name__ == '__main__':
    main()
