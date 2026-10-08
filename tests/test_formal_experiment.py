import copy
import importlib.util
from pathlib import Path

import numpy as np
import pytest

from reasoning_diff.events import parse_events
from reasoning_diff.formal import (build_design, c2_report, cluster_interval, condition_tasks, observations_for,
                                   p1_report, p2_report, source_factorial)
from reasoning_diff.next_round import base_trajectories, trajectory_table
from reasoning_diff.schema import Task, Trace, Cost
from reasoning_diff.spurious_intervention import (choose_prefix, direction_labels, fit_direction,
                                                matched_deltas, p3_report)
from reasoning_diff.tasks.t1_fixture import load_t1_fixture
from reasoning_diff.io import digest, read_json, read_jsonl, write_json, write_jsonl


def test_substitution_operand_is_not_an_assignment_destination(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    text = 'q = 21 + p2. Substituting the value we just found for p2: 21 + 2 = 23.'
    events = parse_events(text, task)
    assert not any(e.node_id == 'p2' and e.value == '23' for e in events)


def formal_trace(task, rid, seed, role, split='test'):
    # An explicit CPU fixture for pipeline accounting, not generated-model evidence.
    text = '\n'.join(f'{n.id} = {n.value}.' for n in task.nodes)
    events = parse_events(text, task)
    for e in events:
        e.event_region = 'thinking'
    return Trace(id=rid, task_id=task.task_id, base_group_id=task.base_group_id, model='fixture', seed=seed,
                 text=text, token_ids=list(range(len(text))), offsets=[[i, i+1] for i in range(len(text))],
                 events=events, answer=task.answer_spec.value, correct=True, status='natural_complete', cost=Cost(),
                 metadata={'formal_role': role, 'formal_split': split, 'generated_tokens': len(text),
                           'boundary_status': 'ok', 'formal_condition': task.metadata['formal_condition']}).to_dict()


def test_design_crosses_edit_values_with_all_reference_seeds(t1_tiny_path):
    task = load_t1_fixture(t1_tiny_path)
    design = build_design([task], edit_values=2)
    edits = [e for e in design['edits'] if e['kind'] != 'source_value_pair']
    assert all(set(e['reference_ids']) == {0, 1, 2} for e in edits)
    assert all(set(e['comparison_ids']) == {0, 1, 2} for e in edits)
    for owner in condition_tasks(task):
        rows = [e for e in edits if e['base_task_id'] == owner.task_id]
        assert {e['changed_premise_ids'][0] for e in rows} == {p.premise_id for p in owner.premises}
        assert len(rows) == len(owner.premises) * 2
    assert len({s['role'] for s in design['splits']}) == 1
    assert len({r['id'] for r in design['requests']}) == len(design['requests'])


def test_noop_injection_is_not_parsed_as_target_assignment(t1_tiny_path):
    base, related, neutral = condition_tasks(load_t1_fixture(t1_tiny_path))
    assert related.answer_spec.value == neutral.answer_spec.value == base.answer_spec.value
    assert len(related.premises[-1].text.split()) == len(neutral.premises[-1].text.split())
    for task in (related, neutral):
        events = parse_events(task.premises[-1].text, task)
        assert not any(e.node_id == task.target for e in events)
        assert any(e.node_id == 'noop' and e.value == '17' for e in events)


def test_source_pair_has_identical_available_sources(t1_tiny_path):
    task = condition_tasks(load_t1_fixture(t1_tiny_path))[0]
    a, b, av, bv = source_factorial(task, 'p1', '4')
    assert [p.premise_id for p in a.premises] == [p.premise_id for p in b.premises]
    assert [(p.premise_id, p.text) for p in a.premises if p.kind != 'relation'] == [
        (p.premise_id, p.text) for p in b.premises if p.kind != 'relation']
    assert a.answer_spec.value == b.answer_spec.value
    assert av.task.answer_spec.value == bv.task.answer_spec.value
    assert 'p1' in a.nodes[0].parents and 'src_b' in b.nodes[0].parents
    for variant in (a, b, av.task, bv.task):
        variant.validate()


def test_formal_variant_references_and_noise_are_accounted_separately(t1_tiny_path):
    design = build_design([load_t1_fixture(t1_tiny_path)], edit_values=1)
    owners = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    traces = [formal_trace(owners[r['task_id']], r['id'], r['seed'], r['role']) for r in design['requests']]
    observations = observations_for(design, traces)
    references = base_trajectories(traces, design['tasks'])
    assert len(references) == 9
    assert sum('::noop:' in r['task_id'] for r in references) == 6
    table = trajectory_table(traces, design['tasks'], observations, design['splits'])
    assert len(table) == 9
    assert all(r['rho'] == 0 for r in table)
    p2 = p2_report(traces, design['tasks'], observations)
    assert len(p2['rows']) == 6
    assert all(r['delta_rho_common_cells'] == 0 for r in p2['rows'])
    assert all(r['three_arm_common_cells'] > 0 for r in p2['contrasts'])


def test_p2_three_arm_contrast_does_not_compare_different_support(t1_tiny_path):
    design = build_design([load_t1_fixture(t1_tiny_path)], edit_values=1)
    owners = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    traces = [formal_trace(owners[r['task_id']], r['id'], r['seed'], r['role']) for r in design['requests']]
    observations = observations_for(design, traces)
    for row in observations:
        condition = owners[row['task_id']].metadata['formal_condition']
        if row['premise_id'] == 'unused_a':
            if condition == 'related_noop':
                row['outcome'] = 'changed'
            elif condition == 'neutral_noop':
                row['outcome'] = 'unaligned'
    report = p2_report(traces, design['tasks'], observations)
    assert all(r['delta_rho_common_cells'] == 0 for r in report['contrasts'])
    assert report['test']['related_minus_neutral']['delta_rho_common_cells']['mean'] == 0


def test_missing_generation_request_cannot_be_summarized(t1_tiny_path):
    design = build_design([load_t1_fixture(t1_tiny_path)], edit_values=1)
    with pytest.raises(ValueError, match='cohort'):
        observations_for(design, [])


def test_cluster_means_weight_problems_not_number_of_seeds():
    result = cluster_interval([1, 1, 1, 0], ['a', 'a', 'a', 'b'])
    assert result['mean'] == .5
    assert result['n_problems'] == 2
    assert cluster_interval([1], ['a'])['interval'] is None
    assert cluster_interval([None], ['a'])['mean'] is None


def test_p1_requires_both_classes_in_each_role():
    table = [{'condition': 'base', 'rho': 0, 'y': 1, 'split': 'probe_train', 'problem_id': 'p',
              'length': 10, 'op': 5}]
    result = p1_report(table)
    assert result['status'] == 'insufficient_classes_train'
    assert result['delta_auc'] is None


def test_p1_precision_recall_metric_does_not_rank_ties_by_input_order():
    from reasoning_diff.analysis import classification_metrics
    left = classification_metrics(np.zeros(4), np.array([1, 1, 0, 0]), split='test')
    right = classification_metrics(np.zeros(4), np.array([0, 0, 1, 1]), split='test')
    assert left['pr_auc'] == right['pr_auc'] == .5


def test_p1_uses_test_predictions_and_reports_missingness():
    table = []
    for role in ('probe_train', 'dev', 'direction_fit', 'test'):
        for i in range(12):
            table.append({'condition': 'base', 'rho': float(i % 2), 'y': 1 - i % 2, 'split': role,
                          'problem_id': f'{role}:{i}', 'trace_id': f'{role}:{i}', 'length': 10, 'op': 5, 'coverage': .8})
    table.append({**table[-1], 'rho': None, 'trace_id': 'missing'})
    result = p1_report(table, n_boot=30)
    assert result['status'] == 'estimate'
    assert result['delta_auc'] > .4
    assert len(result['test_predictions']) == 12
    assert result['missing_by_outcome'] == {'0': 1}
    altered = copy.deepcopy(table)
    for row in altered:
        if row['split'] in {'dev', 'direction_fit'}:
            row['rho'] = -100
    assert p1_report(altered, n_boot=30)['test_predictions'] == result['test_predictions']


def test_p1_rejects_family_leakage():
    rows = [{'condition': 'base', 'rho': i % 2, 'y': i % 2, 'split': role, 'problem_id': 'shared',
             'length': 10, 'op': 5, 'trace_id': f'{role}{i}'} for role in ('probe_train', 'test') for i in range(2)]
    with pytest.raises(ValueError, match='leakage'):
        p1_report(rows)


def test_direction_fit_does_not_read_test_labels(t1_tiny_path):
    task = condition_tasks(load_t1_fixture(t1_tiny_path))[0]
    tasks, events, labels, splits = [], [], [], []
    for i in range(6):
        own = Task.from_dict(task.to_dict())
        own.task_id, own.base_group_id = f't{i}', f'g{i}'
        tasks.append(own.to_dict())
        splits.append({'base_group_id': own.base_group_id, 'role': 'direction_fit' if i < 4 else 'test'})
        events.append({'task_id': own.task_id, 'base_group_id': own.base_group_id, 'trace_id': f'r{i}', 'identity_key': 'q0', 'node_id': 'q'})
        for pid in ('unused_a', 'unused_b'):
            labels.append({'task_id': own.task_id, 'trace_id': f'r{i}', 'event_id': 'q0', 'premise_id': pid,
                           'task_label': 0, 'behavior_label': i % 2})
    hidden = np.array([[i % 2, 1, 0] for i in range(6)], dtype=float)
    first = fit_direction(hidden, events, labels, tasks, splits)
    assert first['status'] == 'fitted'
    for row in labels:
        if row['trace_id'] in {'r4', 'r5'}:
            row['behavior_label'] = 1 - row['behavior_label']
    assert fit_direction(hidden, events, labels, tasks, splits) == first
    assert first['fit_groups'] == ['g0', 'g1', 'g2', 'g3']
    incomplete = [r for r in labels if r['premise_id'] != 'unused_b']
    assert direction_labels(events, incomplete, tasks)[0] is None


def test_p3_deltas_match_norms_and_rescue_is_marked_identity():
    deltas = matched_deltas(np.array([2., 3., 4.]), np.array([1., 2., 3.]), [1., 0., 0.], [0., 1., 0.], 19)
    assert deltas['norms'] == {'main': 2., 'crand': 2., 'clayer': 2.}
    assert np.allclose(deltas['rescue_matched'], 0)
    assert np.allclose(deltas['wrong_direction'], -deltas['main'])


def test_p3_selection_uses_first_positive_saved_prefix():
    trace = {'id': 'r', 'token_ids': [1, 2, 3], 'offsets': [[0, 1], [1, 2], [2, 3]], 'metadata': {'boundary_status': 'ok'}}
    events = [{'trace_id': 'r', 'boundary_start': 2, 'timing': 'pre_step', 'prefix_token_ids': [1, 2]},
              {'trace_id': 'r', 'boundary_start': 1, 'timing': 'pre_step', 'prefix_token_ids': [1]}]
    direction = {'status': 'fitted', 'score_weight': [1.], 'score_intercept': 0., 'decision_threshold': .5}
    assert choose_prefix(trace, events, np.array([[.8], [.6]]), direction)['index'] == 1
    events[1]['prefix_token_ids'] = [1, 2]
    with pytest.raises(ValueError, match='target-step'):
        choose_prefix(trace, events, np.array([[.8], [.6]]), direction)


def test_p3_unavailable_directions_are_not_zero_effects():
    result = p3_report([{'status': 'direction_unavailable', 'conditions': None}])
    assert result['status'] == 'not_estimable' and result['n_unavailable'] == 1
    assert result['contrasts']['all']['main_minus_crand']['mean'] is None


@pytest.fixture
def formal_runner():
    path = Path(__file__).resolve().parents[1] / 'scripts/run_formal.py'
    spec = importlib.util.spec_from_file_location('formal_runner_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def planned_formal(tmp_path, t1_tiny_path, formal_runner):
    tasks = []
    for i in range(2):
        task = load_t1_fixture(t1_tiny_path)
        task.task_id, task.base_group_id = f'formal-{i}', f'formal-{i}'
        tasks.append(task.to_dict())
    dataset = tmp_path / 'input.jsonl'
    write_jsonl(dataset, tasks)
    config = read_json(Path(__file__).resolve().parents[1] / 'experiments/formal_c3.json')
    config.update(dataset=str(dataset), kind='task_jsonl', n_problems=2, edit_values=1, exclude_groups=[], gpus=[0])
    config_path = tmp_path / 'config.json'
    write_json(config_path, config)
    root = tmp_path / 'run'
    assert formal_runner.main(['--config', str(config_path), '--out-root', str(root)]) == 0
    return root, config_path


def save_fixture_responses(root, runner, roles=None):
    protocol, design = runner.verified_plan(root)
    owners = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    splits = {r['task_id']: r['role'] for r in design['splits']}
    for request in design['requests']:
        if roles is not None and request['role'] not in roles:
            continue
        row = formal_trace(owners[request['task_id']], request['id'], request['seed'], request['role'], splits[request['task_id']])
        row['metadata']['revision'] = protocol['revision']
        write_json(root / 'responses' / (request['id'].replace(':', '_') + '.json'),
            {'protocol_digest': digest(protocol), 'request_digest': digest(request), 'trace_digest': digest(row), 'trace': row})


def test_saved_plan_rejects_modified_request(formal_runner, planned_formal):
    root, _ = planned_formal
    protocol, design = formal_runner.verified_plan(root)
    design['requests'][0]['seed'] += 100
    write_json(root / 'design.json', design)
    with pytest.raises(ValueError, match='frozen design'):
        formal_runner.verified_plan(root)


def test_response_hash_is_verified_before_resume(formal_runner, planned_formal):
    root, _ = planned_formal
    save_fixture_responses(root, formal_runner, {'reference'})
    protocol, design = formal_runner.verified_plan(root)
    request = next(r for r in design['requests'] if r['role'] == 'reference')
    path = root / 'responses' / (request['id'].replace(':', '_') + '.json')
    payload = read_json(path)
    payload['trace']['correct'] = False
    write_json(path, payload)
    with pytest.raises(ValueError, match='provenance'):
        formal_runner.saved_response(root, protocol, request)


def test_measurement_cli_writes_real_trajectory_and_paired_tables(formal_runner, planned_formal):
    root, _ = planned_formal
    save_fixture_responses(root, formal_runner)
    assert formal_runner.main(['--mode', 'measure', '--out-root', str(root)]) == 0
    assert len(read_jsonl(root / 'p1_table.jsonl')) == 18
    assert read_json(root / 'p1.json')['primary_base']['status'].startswith('insufficient_classes')
    assert len(read_json(root / 'p2.json')['rows']) == 12
    assert len(read_jsonl(root / 'semantic_audit.jsonl')) == 4
    assert all(r['event_valid'] is None for r in read_jsonl(root / 'audit_sample.jsonl'))
    from reasoning_diff import cli
    assert cli.main(['label', '--in-dir', str(root / 'prepare'), '--out-dir', str(root / 'label'), '--eval-mode', 'scientific']) == 0
    assert read_jsonl(root / 'label/labels.jsonl')


def test_all_stops_single_class_before_expensive_scan(monkeypatch, formal_runner, planned_formal):
    root, config = planned_formal
    calls = []
    def generate(output, reference_only=False):
        calls.append(reference_only)
        save_fixture_responses(output, formal_runner, {'reference'})
    monkeypatch.setattr(formal_runner, 'generate', generate)
    assert formal_runner.main(['--mode', 'all', '--config', str(config), '--out-root', str(root)]) == 0
    assert calls == [True]
    assert read_json(root / 'pipeline.json')['status'] == 'stopped_unestimable'
    assert not (root / 'prepare').exists()


def test_parser_failures_do_not_create_reasoning_error_signal(formal_runner, planned_formal):
    root, _ = planned_formal
    save_fixture_responses(root, formal_runner, {'reference'})
    path = next((root / 'responses').glob('*.json'))
    payload = read_json(path)
    payload['trace']['status'] = 'parse_failed'
    payload['trace_digest'] = digest(payload['trace'])
    write_json(path, payload)
    screen = formal_runner.answer_screen(root)
    assert screen['status'] == 'single_class'
    assert screen['answered_class_counts'] == {'1': 18}
    assert screen['failure_counts'] == {'parse_failed': 1}


def test_c2_primary_includes_invalid_generation_as_incorrect():
    rows = []
    for condition in ('baseline', 'main', 'crand', 'clayer'):
        rows.append({'base_task_id': 'a', 'pair_index': 0, 'pair_kind': 'same_source_diff_value',
            'condition': condition, 'status': 'prospective_decode', 'invalid': int(condition == 'main'),
            'decode_complete': condition != 'main', 'task_correct': None if condition == 'main' else 1,
            'actual_norm': 0 if condition == 'baseline' else 1, 'clayer_status': 'dev_weak_layer_decode',
            'norm_source': 'unmodified_baseline' if condition == 'baseline' else 'resid_post_hook',
            'hook_fired': condition != 'baseline', 'prefix_boundary_verified': True,
            'target': None, 'nontarget': None})
    report = c2_report(rows, [{'task_id': 'a', 'base_group_id': 'problem'}])
    assert report['usable_main_contrasts'] == 0  # complete-answer diagnostic
    assert report['paired_ITT']['same_source_diff_value']['main_minus_crand']['mean'] == -1
    assert not report['unavailable']


def test_second_model_uses_its_own_valid_layer_indices(formal_runner, planned_formal):
    root, config = planned_formal
    other = root.parent / 'r1'
    formal_runner.main(['--config', str(config), '--model', 'r1-distill-qwen-7b', '--out-root', str(other)])
    protocol, design = formal_runner.verified_plan(other)
    assert protocol['config']['layers'] == [0, 9, 18, 27]
    original = read_json(root / 'design.json')
    assert original['splits'] == design['splits']


def test_formal_c2_passes_the_frozen_sampling_parameters(monkeypatch, formal_runner, planned_formal):
    from reasoning_diff import cli
    root, _ = planned_formal
    write_json(root / 'layer_selection.json', {'main': 12, 'weak': 0})
    protocol = read_json(root / 'protocol.json')
    protocol['config']['sampling'] = {'temperature': .7, 'top_k': 10, 'top_p': .9}
    write_json(root / 'protocol.json', protocol)
    commands = []
    monkeypatch.setattr(formal_runner, 'execute', lambda output, name, command, gpu=None: commands.append((name, command)))
    monkeypatch.setattr(formal_runner, 'report', lambda output: None)
    formal_runner.intervene(root)
    args = cli.build_parser().parse_args([str(v) for v in commands[-1][1][3:]])
    assert (args.temperature, args.top_k, args.top_p) == (.7, 10, .9)


def test_unestimable_dev_curve_is_saved_before_interventions(monkeypatch, formal_runner, planned_formal):
    root, _ = planned_formal
    def execute(output, name, command, gpu=None):
        if name.startswith('fit-'):
            layer = int(name.split('-')[1])
            write_jsonl(output / f'fit-layer{layer}/probes.jsonl',
                [{'head': 'behavior', 'U': [[1]], 'metrics': {'dev': {'auc': .8 if layer == 12 else None}}}])
    monkeypatch.setattr(formal_runner, 'execute', execute)
    assert formal_runner.fit(root) is False
    selection = read_json(root / 'layer_selection.json')
    assert selection['status'] == 'insufficient_dev_layers'
    assert selection['main'] is None and selection['weak'] is None
    assert not (root / 's_direction-layer12.json').exists()


def test_formal_source_freeze_includes_cached_fit_helper(monkeypatch, formal_runner):
    original = formal_runner.file_digest
    before = formal_runner.source_hash()
    monkeypatch.setattr(formal_runner, 'file_digest',
                        lambda path: 'modified-fit-helper' if Path(path).name == 'fit_cached_inputs.py' else original(path))
    assert formal_runner.source_hash() != before


def test_formal_subprocess_threads_follow_cpu_or_gpu_work(monkeypatch, formal_runner, planned_formal):
    root, _ = planned_formal
    calls = []
    monkeypatch.setattr(formal_runner.subprocess, 'run', lambda command, **kw: calls.append(kw['env']))
    formal_runner.execute(root, 'cpu', ['unused'])
    formal_runner.execute(root, 'gpu', ['unused'], gpu=2)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        assert calls[0][key] == '8'
        assert calls[1][key] == '1'
    assert calls[1]['CUDA_VISIBLE_DEVICES'] == '2'


def test_formal_fit_uses_cached_parallel_positions_before_aggregation(monkeypatch, formal_runner, planned_formal):
    root, _ = planned_formal
    calls = []
    def execute(output, name, command, gpu=None):
        calls.append((name, command))
        if name.startswith('fit-') and name[4:].isdigit():
            layer = int(name[4:])
            write_jsonl(output / f'fit-layer{layer}/probes.jsonl',
                        [{'head': 'behavior', 'U': [[1]], 'metrics': {'dev': {'auc': .8 if layer == 12 else .6}}}])
    monkeypatch.setattr(formal_runner, 'execute', execute)
    monkeypatch.setattr(formal_runner, 'read_npz', lambda path: {'H': np.zeros((0, 2))})
    monkeypatch.setattr(formal_runner, 'read_jsonl', lambda path: read_jsonl(path) if Path(path).name == 'probes.jsonl' else [])
    monkeypatch.setattr(formal_runner, 'fit_direction', lambda *args: {'status': 'insufficient_direction_classes'})
    assert formal_runner.fit(root) is True
    names = [name for name, command in calls]
    for position in ('pre_step', 'pre_value', 'post_step'):
        assert names.index(f'fit-{position}') < names.index('fit-all')
    fits = [(name, command) for name, command in calls if name.startswith('fit-')]
    assert all(Path(command[1]).name == 'fit_cached_inputs.py' for name, command in fits)
    assert all('--resume' in command for name, command in fits)


@pytest.mark.integration
def test_p3_real_tiny_hook_and_control_decode_path(t1_tiny_path, request):
    import torch
    previous_threads = torch.get_num_threads()
    request.addfinalizer(lambda: torch.set_num_threads(previous_threads))
    torch.set_num_threads(1)
    from reasoning_diff.models.tiny import build_tiny
    from reasoning_diff.models.collect import _hidden_at_layer
    from reasoning_diff.spurious_intervention import run_p3, CONDITIONS
    model = build_tiny('qwen3')
    model.eval()
    hidden = _hidden_at_layer(model, [1, 2], 1)[-1:]
    dim = hidden.shape[1]
    class Tokenizer:
        eos_token_id = 63
        def decode(self, ids, **kwargs):
            return ''.join(chr(96 + int(i)) for i in ids)
    task = condition_tasks(load_t1_fixture(t1_tiny_path))[0]
    trace = {'id': 'r', 'task_id': task.task_id, 'correct': False, 'status': 'natural_complete',
             'token_ids': [1, 2, 3], 'offsets': [[0, 1], [1, 2], [2, 3]],
             'metadata': {'formal_role': 'reference', 'formal_split': 'test', 'boundary_status': 'ok', 'rendered_prompt_text': 'a'}}
    event = {'trace_id': 'r', 'task_id': task.task_id, 'boundary_start': 2, 'timing': 'pre_step',
             'prefix_token_ids': [1, 2], 'node_id': 'q', 'identity_key': 'q:0'}
    direction = {'status': 'fitted', 'fit_groups': [], 'direction': [1.] + [0.] * (dim - 1),
                 'score_weight': [0.] * dim, 'score_intercept': 1., 'decision_threshold': .5}
    outputs = run_p3([trace], [task.to_dict()], [event], hidden, direction, 0, direction,
                     {'model': model, 'tokenizer': Tokenizer()}, 1, max_new=3,
                     sampling={'temperature': .6, 'top_k': 20, 'top_p': .95})
    assert outputs[0]['status'] == 'prospective_decode'
    records = outputs[0]['conditions']
    assert set(records) == set(CONDITIONS)
    assert all(r['hook_sequence_length'] == 2 for r in records.values())
    norms = [records[c]['actual_norm'] for c in ('main', 'crand', 'clayer')]
    assert np.allclose(norms, norms[0], rtol=.02, atol=1e-4)
