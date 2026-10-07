import importlib
from pathlib import Path

import pytest

from reasoning_diff import cli
from reasoning_diff.io import digest, write_json
from reasoning_diff.next_round import registered_pilot_edits, sentence_graph_task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.fixture
def extension(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'scripts'))
    return importlib.import_module('extend_natural_pilot')


def test_plan_is_balanced_and_independent_of_trace_outcomes(extension, t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    requests = extension.requests_for([task])
    assert len(requests) == len({r['id'] for r in requests}) == 10
    assert {r['seed'] for r in requests if r['kind'] == 'noise'} == {3, 4, 5, 6}
    assert {r['seed'] for r in requests if r['kind'] == 'edit'} == {1, 2}
    assert all(sum(r['task_id'] == e.task.task_id for r in requests) == 2 for e in registered_pilot_edits(task))


def synthetic_rows(task):
    rows = []
    for seed in range(7):
        rows.append(cli._synthetic_trace(task, 'q = 7', f'trace-base:seed{seed}', seed).to_dict())
    for e in registered_pilot_edits(task):
        for seed in range(3):
            rows.append(cli._synthetic_trace(e.task, 'q = 8', f'trace-edit:{e.id}:seed{seed}', seed).to_dict())
    return rows


def test_extension_pairs_same_seed_and_never_uses_edits_as_noise(extension, t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    rows = synthetic_rows(task)
    report, observations, _ = extension.measure([task], rows)
    assert report['overall']['n_traces'] == 3
    lookup = {r['id']: r for r in rows}
    for obs in observations:
        left, right = lookup[obs['reference_trace']], lookup[obs['comparison_trace']]
        if obs['rng_pair'].startswith('sham:'):
            assert right['task_id'] == left['task_id'] == task.task_id
            assert right['seed'] != left['seed']
        else:
            assert left['seed'] == right['seed']
    original = extension.measure([task], rows, (0,), (0, 1, 2))[0]
    assert original['overall']['n_traces'] == 1
    changed = [r for r in rows if r['seed'] < 3]
    assert extension.measure([task], changed, (0,), (0, 1, 2))[0]['overall'] == original['overall']


def test_missing_or_duplicate_requests_cannot_be_silently_dropped(extension, t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    rows = synthetic_rows(task)
    with pytest.raises(KeyError):
        extension.measure([task], rows[:-1])
    with pytest.raises(ValueError, match='duplicate'):
        extension.measure([task], rows + rows[:1])


def test_checkpoint_cannot_change_seed_or_trajectory_content(extension, tmp_path):
    request = {'id': 'request', 'task_id': 't', 'seed': 1}
    protocol = {'revision': 'pinned'}
    trace = {'task_id': 't', 'seed': 1, 'metadata': {'revision': 'pinned'}, 'text': 'q = 7'}
    payload = {'protocol_digest': digest(protocol), 'request_digest': digest(request), 'trace_digest': digest(trace), 'trace': trace}
    path = tmp_path / 'responses/request.json'
    write_json(path, payload)
    assert extension.checkpoint(tmp_path, protocol, request) == trace
    payload['trace']['seed'] = 2
    payload['trace_digest'] = digest(payload['trace'])
    write_json(path, payload)
    with pytest.raises(ValueError, match='provenance'):
        extension.checkpoint(tmp_path, protocol, request)
    payload['trace']['seed'] = 1
    payload['trace']['text'] = 'q = 9'
    write_json(path, payload)
    with pytest.raises(ValueError, match='provenance'):
        extension.checkpoint(tmp_path, protocol, request)
