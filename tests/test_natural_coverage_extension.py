import importlib
from pathlib import Path

import pytest

from reasoning_diff.next_round import sentence_graph_task, registered_pilot_edits
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.fixture
def coverage(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'scripts'))
    return importlib.import_module('extend_natural_coverage')


def test_expansion_registers_all_values_and_noise_before_outcomes(coverage, t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    old = coverage.expected_source_requests([task])
    requests = coverage.additional_requests([task], old)
    assert len(old) == 16
    assert len(requests) == 35
    assert len({r['id'] for r in requests}) == len(requests)
    assert {r['seed'] for r in requests if r['kind'] == 'noise'} == set(range(7, 24))
    assert {(r['task_id'], r['seed']) for r in requests}.isdisjoint(old)
    edits = coverage.expanded_edits(task)
    assert len(edits) == 9
    assert {e.changed_premise_ids[0] for e in edits} == {e.changed_premise_ids[0] for e in registered_pilot_edits(task)}
    for edit in edits:
        for seed in range(3):
            assert (edit.task.task_id, seed) in old or any(r['task_id'] == edit.task.task_id and r['seed'] == seed for r in requests)


def test_repeat_measurement_preserves_denominator_and_unique_observations(coverage, t1_tiny_path):
    from reasoning_diff import cli
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    rows = [cli._synthetic_trace(task, 'q = 7', f'trace-base:{s}', s).to_dict() for s in range(24)]
    rows += [cli._synthetic_trace(e.task, 'q = 8', f'edit:{e.id}:{s}', s).to_dict()
             for e in coverage.expanded_edits(task) for s in range(3)]
    report, observations, _ = coverage.engine.measure([task], rows, noise_seeds=range(24), edits_for=coverage.expanded_edits)
    original, _, _ = coverage.engine.measure([task], rows)
    assert report['overall']['eligible_cells'] == original['overall']['eligible_cells']
    assert len({o['observation_id'] for o in observations}) == len(observations)
    lookup = {r['id']: r for r in rows}
    for obs in observations:
        left, right = lookup[obs['reference_trace']], lookup[obs['comparison_trace']]
        assert left['seed'] != right['seed'] if obs['rng_pair'].startswith('sham:') else left['seed'] == right['seed']
    with pytest.raises(KeyError):
        coverage.engine.measure([task], rows[:-1], noise_seeds=range(24), edits_for=coverage.expanded_edits)
