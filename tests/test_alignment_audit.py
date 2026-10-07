from copy import deepcopy

import pytest

from reasoning_diff import cli
from reasoning_diff.alignment_audit import alignment_audit
from reasoning_diff.events import assign_event_regions, parse_events
from reasoning_diff.next_round import measurement_report, registered_pilot_edits, sentence_graph_task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


def test_loss_audit_reconciles_missing_phase_and_missing_noise(t1_tiny_path):
    task = sentence_graph_task(load_t1_fixture(t1_tiny_path))
    def trace(owner, text, name, seed):
        result = cli._synthetic_trace(owner, text, name, seed)
        result.events = assign_event_regions(parse_events(text, owner), text, initial_thinking=True)
        result.metadata['boundary_status'] = 'ok'
        return result
    base = trace(task, 'q = 7.', 'trace-base', 0)
    noise = trace(task, 'q = p1 = 7.', 'trace-base-noise', 1)
    traces, observations, scanned = [base, noise], [], []
    for edit in registered_pilot_edits(task):
        pid = edit.changed_premise_ids[0]
        donor = trace(edit.task, 'q = p1 = 7.' if pid == 'unused_b' else 'q = 7.', pid, 0)
        traces.append(donor)
        scanned.append(pid)
        observations.extend(cli._observations(task, base, donor, edit, 'stream:0', pid))
    obs = [o.to_dict() for o in observations]
    report = measurement_report([base.to_dict()], [task.to_dict()], obs, [], {task.task_id: scanned})
    audit = alignment_audit([t.to_dict() for t in traces], [task.to_dict()], obs, report)
    assert audit['eligible_cells'] == 2
    assert audit['cells_by_outcome'] == {'matched': 1, 'phase_incompatible': 1}
    assert audit['trajectories'][0]['noise_support'] == {'matched_without_noise': 1}
    broken = deepcopy(report)
    broken['trajectories'][0]['support_cells'] += 1
    with pytest.raises(ValueError, match='does not reconcile'):
        alignment_audit([t.to_dict() for t in traces], [task.to_dict()], obs, broken)
