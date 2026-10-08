"""Regressions through the formal pipeline's real fit/calibrate/dispatch paths."""
import numpy as np
import pytest

from reasoning_diff import cli
from reasoning_diff.formal import build_design, c2_report, condition_tasks
from reasoning_diff.io import read_jsonl, write_jsonl, write_npz
from reasoning_diff.probes.bilinear import BilinearProbe
from reasoning_diff.schema import Task
from reasoning_diff.tasks.t1_fixture import load_t1_fixture


@pytest.fixture
def variant_features(tmp_path, t1_tiny_path):
    tasks, splits, events, traces, labels, premises = [], [], [], [], [], []
    for group, role in [('train', 'probe_train'), ('cal', 'calibration')]:
        raw = load_t1_fixture(t1_tiny_path)
        raw.task_id = raw.base_group_id = group
        owners = condition_tasks(raw)
        route = Task.from_dict(owners[0].to_dict())
        route.task_id += '::route_a::value:p1:5'
        owners.append(route)
        for i, task in enumerate(owners):
            tid = 'trace:' + task.task_id
            tasks.append(task.to_dict())
            splits.append({'task_id': task.task_id, 'base_group_id': group, 'role': role})
            events.append({'trace_id': tid, 'task_id': task.task_id, 'base_group_id': group,
                'identity_key': 'q0', 'node_id': 'q', 'boundary_start': 0, 'boundary_end': 1,
                'event_kind': 'calculation'})
            traces.append({'id': tid, 'task_id': task.task_id, 'base_group_id': group,
                'text': 'q = 0.', 'events': [], 'status': 'natural_complete', 'correct': True})
            premises.append({'premise_key': task.task_id + '::p1', 'task_id': task.task_id, 'premise_id': 'p1'})
            labels.append({'trace_id': tid, 'task_id': task.task_id, 'base_group_id': group,
                'event_id': 'q0', 'premise_id': 'p1', 'task_label': 1, 'behavior_label': i % 2})
    for name, rows in [('tasks', tasks), ('splits', splits), ('event_rows', events), ('traces', traces),
                       ('premise_rows', premises), ('labels', labels)]:
        write_jsonl(tmp_path / f'{name}.jsonl', rows)
    h = np.array([[1 + i % 2, -1.] for i in range(len(events))])
    write_npz(tmp_path / 'features.npz', {'H': h, 'H_pre_value': h, 'H_post_step': h, 'E': h})
    return tmp_path


def test_fit_joins_exact_task_and_premise_identity(variant_features, monkeypatch):
    captured = []
    def capture(self, h, e, y, **kw):
        captured.append(y.copy())
        raise RuntimeError('captured_training_labels')
    monkeypatch.setattr(BilinearProbe, 'fit', capture)
    with pytest.raises(RuntimeError, match='captured_training_labels'):
        cli.main(['fit', '--in-dir', str(variant_features), '--out-dir', str(variant_features / 'fit'),
                  '--eval-mode', 'scientific'])
    assert np.array_equal(np.isfinite(captured[0]), np.eye(4, 8, dtype=bool))


def test_formal_fit_all_positions_and_calibration_keep_every_variant(variant_features):
    root = variant_features
    assert cli.main(['fit', '--in-dir', str(root), '--out-dir', str(root / 'fit'),
                     '--position', 'all', '--eval-mode', 'scientific']) == 0
    assert cli.main(['calibrate', '--in-dir', str(root / 'fit'), '--features-dir', str(root),
                     '--labels-dir', str(root), '--out-dir', str(root / 'cal'),
                     '--head', 'behavior', '--eval-mode', 'scientific']) == 0
    rows = read_jsonl(root / 'cal/calibration.jsonl')
    assert {r['position'] for r in rows} == {'pre_step', 'pre_value', 'post_step'}
    assert all(r['events_per_unit'] == {'cal': 4} for r in rows)


def test_calibration_keeps_composite_ids_without_running_fit(variant_features):
    root = variant_features
    probe = BilinearProbe(2, 2, rank=1)
    row = {'head': 'behavior', 'position': 'pre_step', 'dim_h': 2, 'dim_e': 2, 'rank': 1,
           'U': probe.U.tolist(), 'V': probe.V.tolist(), 'b': probe.b}
    write_jsonl(root / 'probe/probes.jsonl', [row])
    cli.main(['calibrate', '--in-dir', str(root / 'probe'), '--features-dir', str(root),
              '--labels-dir', str(root), '--out-dir', str(root / 'cal'), '--eval-mode', 'scientific'])
    assert read_jsonl(root / 'cal/calibration.jsonl')[0]['events_per_unit'] == {'cal': 4}


def test_design_registers_fixed_unequal_sources_in_both_directions(t1_tiny_path):
    from reasoning_diff.splits import split_for_task
    task = load_t1_fixture(t1_tiny_path)
    seed = next(s for s in range(100) if split_for_task(task, seed=s) == 'test')
    design = build_design([task], edit_values=1, split_seed=seed)
    pairs = [p for p in design['edits'] if 'fixed_values_diff_source' in p]
    assert len(pairs) == 4
    tasks = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    for pair in pairs:
        edit = pair['fixed_values_diff_source']
        left, right = tasks[pair['base_task_id']], Task.from_dict(edit['task'])
        facts = lambda t: [(p.premise_id, p.text, p.value) for p in t.premises if p.kind == 'definition']
        assert facts(left) == facts(right)
        assert left.answer_spec.value != right.answer_spec.value
        assert edit['metadata']['source_value_mode'] == 'unequal_fixed_facts'
        assert set(pair['trace_ids']) == {'base', 'fixed_values_diff_source'}
    assert {p['routing_direction'] for p in pairs} == {'a_to_b', 'b_to_a'}


def c2_rows():
    return [{'base_task_id': 'a', 'pair_index': 0, 'pair_kind': 'fixed_values_diff_source',
             'condition': c, 'status': 'prospective_decode', 'invalid': 0, 'decode_complete': True,
             'task_correct': 1, 'target': int(c == 'main'), 'nontarget': 1,
             'actual_norm': 0 if c == 'baseline' else 1, 'planned_norm': 1,
             'norm_source': 'unmodified_baseline' if c == 'baseline' else 'resid_post_hook',
             'hook_fired': c != 'baseline', 'prefix_boundary_verified': True,
             'clayer_status': 'dev_weak_layer_decode'} for c in ('baseline', 'main', 'crand', 'clayer')]


def test_c2_rejects_legacy_planned_norms_and_retains_empty_shards():
    rows = c2_rows()
    for r in rows:
        r.pop('norm_source')
    result = c2_report(rows, [{'task_id': 'a', 'base_group_id': 'g'}])
    assert not result['executed_ITT_effects']
    assert result['unavailable']
    empty = [{'status': 'no_source_pairs_in_split', 'split': 'test', 'pair_shard': [i, 3]} for i in range(3)]
    result = c2_report(empty, [])
    assert len(result['empty_shards']) == 3
    assert not result['executed_ITT_effects']


def test_c2_reports_ITT_source_follow_against_every_control():
    result = c2_report(c2_rows(), [{'task_id': 'a', 'base_group_id': 'g'}])
    effect = result['paired_ITT']['fixed_values_diff_source']
    assert all(effect['target_follow_main_minus_' + c]['mean'] == 1 for c in ('baseline', 'crand', 'clayer'))


@pytest.mark.parametrize('measured_norms', [(1., 1., 1.), (0., .5, .7)])
def test_c2_real_dispatch_alignment_scoring_and_measured_norm_persistence(tmp_path, t1_tiny_path, monkeypatch, measured_norms):
    from reasoning_diff.events import assign_event_regions, parse_events
    from reasoning_diff.io import write_json
    from reasoning_diff.models import collect
    from reasoning_diff.schema import Cost, Trace
    from reasoning_diff.splits import split_for_task
    task = load_t1_fixture(t1_tiny_path)
    seed = next(s for s in range(100) if split_for_task(task, seed=s) == 'test')
    design = build_design([task], edit_values=1, split_seed=seed)
    pair = next(p for p in design['edits'] if 'fixed_values_diff_source' in p)
    tasks = {t['task_id']: Task.from_dict(t) for t in design['tasks']}
    owners = [tasks[pair['base_task_id']], Task.from_dict(pair['fixed_values_diff_source']['task'])]
    class Tokenizer:
        eos_token_id = 0
        def decode(self, ids, **kw):
            return ''.join(chr(i) for i in ids)
    traces, events = [], []
    for owner, tid in zip(owners, pair['trace_ids'].values(), strict=True):
        prompt = owner.question + '<think>'
        # Both observed donor/base values are wrong and equal. Source-follow
        # must use the independent graph, not these observed values.
        body = f'q = {owner.nodes[0].expression} = 99.\n</think>\n99'
        parsed = assign_event_regions(parse_events(body, owner), body, initial_thinking=True)
        for e in parsed:
            e.start += len(prompt)
            e.end += len(prompt)
            e.value_start += len(prompt)
        text = prompt + body
        trace = Trace(id=tid, task_id=owner.task_id, base_group_id=owner.base_group_id,
            text=text, events=parsed, token_ids=list(map(ord, text)), offsets=[[i, i + 1] for i in range(len(text))],
            model='fixture', seed=0, answer='99', correct=False, cost=Cost(),
            metadata={'boundary_status': 'ok', 'rendered_prompt_text': prompt})
        traces.append(trace.to_dict())
        e = next(e for e in parsed if e.node_id == 'q' and e.event_region == 'thinking')
        events.append({'trace_id': tid, 'task_id': owner.task_id, 'node_id': 'q',
                       'identity_key': e.identity.key(), 'prefix_token_ids': list(map(ord, text[:e.start]))})
    for name, rows in [('tasks', [t.to_dict() for t in owners]), ('traces', traces), ('event_rows', events),
                       ('edits', [pair]), ('splits', [{'task_id': t.task_id, 'role': 'test'} for t in owners]),
                       ('probes', [{'head': 'behavior', 'U': [[1.], [0.]]}])]:
        write_jsonl(tmp_path / f'{name}.jsonl', rows)
    write_json(tmp_path / 'run_spec.json', {'config': {'hidden_layer': 0, 'model_kind': 'qwen2'}})
    write_npz(tmp_path / 'features.npz', {'H': np.array([[0., 0.], [1., 1.]])})
    runtime = {'model': object(), 'tokenizer': Tokenizer(), 'card': {'layers': 2, 'context_limit': 10000}}
    monkeypatch.setattr(cli, '_load_frozen_runtime', lambda _: runtime)
    monkeypatch.setattr(collect, '_hidden_at_layer', lambda _, ids, layer: np.array([[sum(ids) / 1000., 1.]]))
    calls = []
    def decode(_kind, ids, layer, **kw):
        i = len(calls)
        calls.append(i)
        answer = owners[1 if i == 0 else 0].answer_spec.value
        return {'generated_ids': list(map(ord, '</think>\n' + answer)),
                'baseline_generated_ids': list(map(ord, '</think>\n' + owners[0].answer_spec.value)),
                'stop_reason': 'eos', 'baseline_stop_reason': 'eos', 'hook': 'once', 'hook_fired': True,
                'transform': 'add_delta', 'followed_donor': True, 'timing': 'pre_step',
                'prefix_boundary_verified': True, 'hook_delta_norm': measured_norms[min(i, 2)],
                'hook_token_position': len(ids) - 1, 'hook_sequence_length': len(ids)}
    monkeypatch.setattr(collect, 'intervene_hidden_decode', decode)
    combined = []
    for shard in range(3):
        out = tmp_path / f'out{shard}'
        cli.main(['intervene', '--in-dir', str(tmp_path), '--out-dir', str(out), '--backend', 'frozen',
            '--eval-mode', 'scientific', '--all-source-pairs', '--pair-split', 'test', '--pair-shard', str(shard), '3',
            '--dev-layer-scores', '.8', '.5', '--dev-layer-ids', '0', '1'])
        combined.extend(read_jsonl(out / 'interventions.jsonl'))
    records = {r['condition']: r for r in combined if 'condition' in r}
    assert set(records) == {'baseline', 'main', 'crand', 'clayer'}
    assert [records[c]['actual_norm'] for c in ('main', 'crand', 'clayer')] == list(measured_norms)
    assert all(records[c]['planned_norm'] == pytest.approx(1.) for c in ('main', 'crand', 'clayer'))
    assert records['main']['target_value_source'] == 'independent_graph_gold'
    assert records['main']['target'] == 1 and records['baseline']['target'] == 0
    report = c2_report(combined, [t.to_dict() for t in owners])
    assert len(report['empty_shards']) == 2
    assert len(report['executed_ITT_effects']) == int(measured_norms[0] > 0)


@pytest.mark.integration
def test_bfloat16_rounded_away_patch_is_not_an_executed_c2_effect(request):
    import torch
    from reasoning_diff.models.collect import intervene_hidden_decode
    from reasoning_diff.models.tiny import build_tiny
    threads = torch.get_num_threads()
    request.addfinalizer(lambda: torch.set_num_threads(threads))
    torch.set_num_threads(1)
    model = build_tiny('qwen3').to(dtype=torch.bfloat16).eval()
    delta = np.full(model.config.hidden_size, 1e-10)
    decoded = intervene_hidden_decode('qwen3', [1, 2], 1, model=model, mode='add_delta', delta=delta,
                                     event_aligned=True, target_prefix_len=2, max_new=1)
    assert np.linalg.norm(delta) > 0 and decoded['hook_delta_norm'] == 0
    rows = c2_rows()
    rows[1]['actual_norm'] = decoded['hook_delta_norm']
    result = c2_report(rows, [{'task_id': 'a', 'base_group_id': 'g'}])
    assert not result['executed_ITT_effects'] and not result['effects']


def test_p3_excludes_selected_node_and_descendants(monkeypatch, t1_tiny_path):
    from reasoning_diff.spurious_intervention import run_p3
    from reasoning_diff.models import collect
    task = load_t1_fixture(t1_tiny_path).to_dict()
    task['nodes'].extend([
        {'id': 'r', 'parents': ['q'], 'value': '1', 'expression': 'q + 1', 'aliases': ['r']},
        {'id': 'u', 'parents': ['p1'], 'value': '7', 'expression': 'p1 + 3', 'aliases': ['u']}])
    task['target'], task['answer_spec']['value'] = 'r', '1'
    task = condition_tasks(Task.from_dict(task))[0]
    text = {0: 'q = 0.\nr = 1.\nu = 7.\n</think>\n1', 1: 'q = 1.\nr = 2.\nu = 7.\n</think>\n2'}
    class Tokenizer:
        eos_token_id = 99
        def decode(self, ids, **kw):
            return 'Prompt<think>' + (text[ids[-1]] if len(ids) > 2 else '')
    def decode(*args, **kw):
        changed = int(np.linalg.norm(kw['delta']) > 0)
        return {'generated_ids': [changed], 'stop_reason': 'eos', 'hook_fired': True,
                'prefix_boundary_verified': True, 'hook_delta_norm': float(np.linalg.norm(kw['delta'])),
                'hook_token_position': 1, 'hook_sequence_length': 2}
    monkeypatch.setattr(collect, 'intervene_hidden_decode', decode)
    monkeypatch.setattr(collect, '_hidden_at_layer', lambda *a: np.array([[2., 3.]]))
    trace = {'id': 't', 'task_id': task.task_id, 'token_ids': [1, 2], 'offsets': [[0, 6], [6, 13]],
             'metadata': {'formal_role': 'reference', 'formal_split': 'test', 'boundary_status': 'ok',
                          'rendered_prompt_text': 'Prompt'}}
    event = {'trace_id': 't', 'node_id': 'q', 'boundary_start': 13, 'timing': 'pre_step',
             'prefix_token_ids': [1, 2], 'identity_key': 'q0'}
    direction = {'status': 'fitted', 'fit_groups': [], 'direction': [1., 0.], 'score_weight': [0., 0.],
                 'score_intercept': 1., 'decision_threshold': .5}
    result = run_p3([trace], [task.to_dict()], [event], np.array([[2., 3.]]), direction, 0, direction,
                    {'model': None, 'tokenizer': Tokenizer()}, 1, max_new=10, sampling={})[0]
    assert result['conditions']['main']['nontarget_matched_events'] == 1
    assert result['conditions']['main']['nontarget_change_rate'] == 0
