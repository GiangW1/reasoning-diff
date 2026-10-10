"""Frozen-cohort accounting must survive parser-only remeasurement."""
import copy
import importlib
from pathlib import Path

import pytest

from reasoning_diff import cli
from reasoning_diff.formal import build_design
from reasoning_diff.io import digest, file_digest, read_json, write_json
from reasoning_diff.schema import Task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.fixture
def cohort(tmp_path, t1_tiny_path, monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'scripts'))
    runner = importlib.import_module('audit_formal_matching')
    task = load_t1_fixture(t1_tiny_path)
    design = build_design([task], seeds=(0,), noise_seeds=(3,), edit_values=1)
    source = tmp_path / 'source'
    dataset = tmp_path / 'dataset.json'
    write_json(dataset, task.to_dict())
    protocol = {'design_digest': digest(design), 'dataset_hash': file_digest(dataset), 'revision': 'frozen',
                'config': {'dataset': str(dataset), 'reference_seeds': [0], 'noise_seeds': [3], 'edit_values': 1}}
    write_json(source / 'design.json', design)
    write_json(source / 'protocol.json', protocol)
    owners = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    for request in design['requests']:
        owner = owners[request['task_id']]
        row = cli._synthetic_trace(owner, 'q = 7\n</think>\n7', request['id'], request['seed']).to_dict()
        row['metadata'].update(revision='frozen', formal_role=request['role'],
                               formal_condition=owner.metadata['formal_condition'])
        write_json(source / 'responses' / (request['id'].replace(':', '_') + '.json'),
                   {'protocol_digest': digest(protocol), 'request_digest': digest(request),
                    'trace_digest': digest(row), 'trace': row})
    return runner, source, design


def test_audit_freezes_reference_events_and_never_rewrites_checkpoints(cohort, tmp_path, monkeypatch):
    runner, source, design = cohort
    reparser = importlib.import_module('reparse_pr8')
    seen = []

    def reparse(row, task, parser_hash):
        from reasoning_diff.schema import Trace
        seen.append(row['id'])
        changed = copy.deepcopy(row)
        changed['events'] = []  # A deliberately destructive comparison parser.
        return Trace.from_dict(changed)

    monkeypatch.setattr(reparser, 'reparse_trace', reparse)
    hashes = {p: file_digest(p) for p in source.rglob('*.json')}
    original_align = cli.align_events
    runner.audit(source, tmp_path / 'baseline')
    runner.audit(source, tmp_path / 'reparsed', reparse_comparisons=True)
    old, new = (read_json(tmp_path / name / 'summary.json') for name in ('baseline', 'reparsed'))
    assert set(seen) == {r['id'] for r in design['requests'] if r['role'] != 'reference'}
    assert new['n_traces'] == len(design['requests']) and new['new_generation_calls'] == 0
    assert new['reference_events_frozen']
    for condition in old['conditions']:
        assert old['conditions'][condition]['eligible_cells'] == new['conditions'][condition]['eligible_cells']
    assert hashes == {p: file_digest(p) for p in hashes}
    assert cli.align_events is original_align


def test_audit_rejects_tampered_checkpoint(cohort, tmp_path):
    runner, source, _ = cohort
    path = next((source / 'responses').iterdir())
    saved = read_json(path)
    saved['trace']['text'] += ' tampered'
    write_json(path, saved)
    with pytest.raises(ValueError, match='checkpoint provenance'):
        runner.audit(source, tmp_path / 'tampered-output')
    assert not (tmp_path / 'tampered-output').exists()


def test_audit_rejects_writing_inside_frozen_experiment(cohort):
    runner, source, _ = cohort
    with pytest.raises(ValueError, match='outside the frozen'):
        runner.audit(source, source / 'new-output')
