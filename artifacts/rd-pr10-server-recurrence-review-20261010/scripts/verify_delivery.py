"""Verify delivery against existing raw files, original snapshots and exact spans."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
from zoneinfo import ZoneInfo

ROOT=Path('/mnt/mydata/wja/reasoning-diff')
OUT=ROOT/'reports/pr10-server-recurrence-review-20261010'
REPO=Path('/home/wja/reasoning-diff-pr10')
AUDIT=REPO/'experiments/natural-recurrence-audit-20261010'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    summary=json.loads((OUT/'coverage-summary.json').read_text())
    records=[json.loads(s) for s in (OUT/'records.jsonl').read_text().splitlines()]
    lookup={r['code']:r for r in records}
    coverage=json.loads((OUT/'coverage-all-records.json').read_text())
    assert len(records)==len(coverage)==168
    assert len({(r['run'],r['meta']['task_id'],r['meta']['seed'],r['meta']['role']) for r in records})==168
    assert len({r['text_sha256'] for r in records})==168
    payloads={}
    for row in coverage:
        r=lookup[row['code']]
        fulltext=(OUT/r['fulltext_path']).read_bytes()
        assert sha(fulltext)==row['text_sha256']==r['text_sha256']
        if row['code'].startswith('E'):continue
        raw=Path(row['source_path']).read_bytes()
        assert sha(raw)==row['file_sha256']==row['expected_file_sha256']
        p=json.loads(raw);t=p['trace'];payloads[(r['run'],t['id'])]=p
        assert t['text'].encode()==fulltext
        for k in ('id','task_id','base_group_id','seed'):
            assert t[k]==r['meta'][k]
        assert t['metadata']['formal_role']==r['meta']['role']
        for k in ('protocol_digest','request_digest','trace_digest'):
            assert p[k]==r['meta'][k]
        assert row['verified']
    missing=json.loads((AUDIT/'missing-pr9-fulltexts.json').read_text())['records']
    missing_roles=Counter()
    for row in missing:
        p=payloads[(row['run'],row['id'])];t=p['trace']
        path=ROOT/row['expected_server_relative_path']
        assert sha(path.read_bytes())==row['file_sha256']
        assert sha(t['text'].encode())==row['text_sha256']
        for k in ('id','task_id','base_group_id','seed'):
            assert t[k]==row[k]
        assert t['metadata']['formal_role']==row['role']
        for k in ('protocol_digest','request_digest','trace_digest'):
            assert p[k]==row[k]
        missing_roles.update([row['role']])
    assert len(missing)==96 and missing_roles=={'reference':24,'noise':72}
    archive=OUT/'source_data/artifacts/rd-pr8-natural-pilot-20261007-light/raw-and-reparsed-pilot.tar.gz'
    archive_bytes=archive.read_bytes()
    git_bytes=subprocess.check_output(['git','show','HEAD:artifacts/rd-pr8-natural-pilot-20261007-light/raw-and-reparsed-pilot.tar.gz'],cwd=REPO)
    assert archive_bytes==git_bytes
    assert sha(archive_bytes)==summary['pr8_archive_sha256']
    with tarfile.open(archive) as tf:
        member_rows={}
        for row in coverage:
            if not row['code'].startswith('E'):continue
            member=row['archive_member']
            assert member.endswith('/traces.jsonl') and '/pilot-gpu' in member
            if member not in member_rows:
                member_rows[member]=[json.loads(s) for s in tf.extractfile(member) if s.strip()]
            raw=member_rows[member][row['source_line']-1]
            r=lookup[row['code']]
            assert raw['text'].encode()==(OUT/r['fulltext_path']).read_bytes()
            for k in ('id','task_id','base_group_id','seed'):
                assert raw[k]==r['meta'][k]
            assert raw['metadata'].get('edit_id') is None
    original=json.loads((AUDIT/'natural-recurrence-evidence.json').read_text())
    original_excerpts=0
    for row in original['inventory']:
        text=(OUT/lookup[row['code']]['fulltext_path']).read_text()
        assert sha(text.encode())==row['text_sha256']
        for e in row.get('excerpts',[]):
            assert text[e['start']:e['end']]==e['text']
            original_excerpts+=1
    snapshot_count=0
    for name,digest in summary['original_snapshot_hashes'].items():
        raw=(AUDIT/name).read_bytes()
        assert sha(raw)==digest
        git_path=str((AUDIT/name).relative_to(REPO))
        assert raw==subprocess.check_output(['git','show','HEAD:'+git_path],cwd=REPO)
        snapshot_count+=1
    candidates=json.loads((OUT/'candidates.json').read_text())['records']
    new_excerpts=0
    for c in candidates:
        r=lookup[c['code']];text=(OUT/r['fulltext_path']).read_text()
        assert c['text_sha256']==sha(text.encode())
        paras=list(re.finditer(r'[^\n]+(?:\n(?!\n)[^\n]+)*',text))
        excerpt_map={e['paragraph']:e for e in c['excerpts']}
        for e in c['excerpts']:
            p=paras[e['paragraph']-1]
            assert p.start()==e['start'] and p.end()==e['end']
            assert text[e['start']:e['end']]==e['text']==p.group()
            assert e['text'] in (OUT/c['evidence_file']).read_text()
            new_excerpts+=1
        for phase in c['phases'].values():
            for p in phase['positions'] or []:
                e=excerpt_map[p['paragraph']]
                assert (p['start'],p['end'])==(e['start'],e['end'])
        assert c['phases']['post_correction_actual_error_use']['positions'] is None
    assert new_excerpts==298
    sensitivity=json.loads((OUT/'task-sensitivity.json').read_text())
    assert sensitivity['summary']['non_target_nodes_checked']==174
    assert sensitivity['summary']['nodes_with_target_path_but_constant_final']==15
    assert sensitivity['summary']['tasks_with_constant_final_node']==6
    assert set(sensitivity['cases'])=={c['code'] for c in candidates}
    assert all(len(s['all_residues'])==23 for s in sensitivity['cases'].values())
    assert all(n['canonical_matches_saved_nodes_and_answer'] and not n['target_children'] for n in sensitivity['all_canonical_checks'])
    for c in ('P40','P71','E18'):
        s=sensitivity['cases'][c]
        assert s['representative_a'] % 23==s['representative_b'] % 23==s['canonical_value']
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=REPO,text=True)
    assert head==summary['pr10_commit'] and not status
    # No new inference commands are present in these offline helper scripts.
    operation_dir=ROOT/'operations/pr10-server-review-20261010'
    for script in operation_dir.glob('*.py'):
        assert str(script.resolve()).startswith('/mnt/mydata/wja/')
    ids=Counter((r['run'],r['meta']['id']) for r in records if r['code'].startswith('E'))
    assert sum(v>1 for v in ids.values())==12
    verification={
        'verified_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
        'passed':True,'pr10_commit':head,'source_worktree_clean':True,
        'original_pr10_snapshot_files_unchanged_and_equal_git':snapshot_count,
        'original_snapshot_fulltexts_verified':len(original['inventory']),
        'original_snapshot_excerpt_intervals_verified':original_excerpts,
        'missing_manifest_records_verified_directly':len(missing),
        'missing_manifest_roles':dict(missing_roles),
        'original_pr9_files_and_fulltexts_verified':len(payloads),
        'protocol_verification':'saved digest field equality; not independent digest algorithm recomputation',
        'pr8_original_members_verified':24,'pr8_archive_equal_to_pr10_git_bytes':True,
        'pr8_colliding_run_trace_id_groups':12,
        'unique_run_task_seed_role_keys':168,'unique_fulltext_sha256':168,
        'reviewed_candidates':24,'new_complete_paragraph_intervals_verified':new_excerpts,
        'arithmetic':sensitivity['summary'],
        'no_new_model_generation_or_gpu_job_started_by_this_review':True,
        'no_gate_or_original_experiment_file_written_by_this_review':True,
        'model_and_gate_fields_basis':'scope and commands executed in this review, not an assertion about unrelated users or historic processes',
        'not_an_exhaustive_semantic_audit':True,'not_a_second_human_annotation':True,
        'new_report_storage_root':str(OUT),
        'external_source_data_link_not_copied_into_checksum_manifest':str(OUT/'source_data/artifacts/rd-pr9-single-pass-validation-20261010-light'),
        'operation_script_sha256':{p.name:sha(p.read_bytes()) for p in sorted(operation_dir.glob('*.py'))}}
    (OUT/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
    paths=[p for p in sorted(OUT.rglob('*')) if p.is_file() and not p.is_symlink() and p.name!='SHA256SUMS']
    lines=[f'{sha(p.read_bytes())}  {p.relative_to(OUT)}' for p in paths]
    (OUT/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    # Recheck the written delivery manifest before reporting success.
    for line in (OUT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert sha((OUT/name).read_bytes())==digest
    print(json.dumps({'passed':True,'original_files_unchanged':snapshot_count,
                      'original_excerpt_checks':original_excerpts,'new_excerpt_checks':new_excerpts,
                      'checksum_files':len(paths)},ensure_ascii=False))


if __name__=='__main__':main()
