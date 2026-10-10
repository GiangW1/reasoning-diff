"""Package existing trace evidence and deterministic arithmetic checks only.

This does not invoke a language model. Judgments are an assistant's manual
audit, not independent gold labels. Excerpts retain exact source text.
"""
import ast
import hashlib
import json
from collections import Counter
from pathlib import Path

from audit_natural_recurrence import PR9, jsonl, load, paragraphs

DEST = Path(__file__).resolve().parents[1]
EVIDENCE = DEST / 'recurrence-evidence'

JUDGMENTS = {
    'P05': '数值结果正确，但错误题面绑定持续到最终解释；未确认来源已纠正，更未确认纠正后的错误计算复发。',
    'P14': '区分标签与目标，后续疑问属于语义复核；算式中的系数17有合法来源。',
    'P15': '初期目标/标签混淆，随后区分标签变量与目标；未确认再次实际错误计算。',
    'P17': '开始对17的绑定提出疑问，计算前将标签另命名；未确认计算复发。',
    'P18': '标签与目标分开；中间算式中的17是10+7的合法结果，不能归因于干扰源。',
    'P19': '初期错误重述，正确结果出现后存在条件式语义复核；未确认错误值再次进入实际下游计算。',
    'P21': '初期错误重述，随后区分；后续合法中间量也等于17，不能凭数值认定来源。',
    'P22': '初期从错误绑定推导R_T=12；后期重现12明确置于If分支并用矛盾否定，不认定为复发。',
    'P24': '初期混淆，随后区分；正确21之后的17分支为假设和矛盾检验。',
    'V03': '初期命名含混，计算前区分标签与目标；未确认复发。',
    'V04': '计算前将标签与Gaming Backpack区分；未确认复发。',
    'V08': '标签单列；未确认实际错误来源计算。',
    'V13': '错误目标重述反复出现；一处公式缩写混淆立即修正，未见17进入该计算；后期错误分支被否定。',
    'V18': '先讨论标签歧义，随后正确计算7；未确认复发。',
    'V20': '计算前重新命名标签以避免混淆；随后为假设性复核。',
    'V21': '正确0之后反复讨论17的解释，但未确认采用17执行错误后续计算。',
    'V24': '错误重述在正确4之后再次出现，但后续计算仍使用正确链；17的反推属假设性复核。',
    'V17': '真实算术错误及八个下游非目标量的错误传播，随后修正且未见复发；最终答案对该中间量完全不敏感。',
    'E24': '13-20得到16的错误候选是明确反事实分支，随后拒绝；实际答案维持7。',
}

SELECTED = {
    'P05': [4, 5, 8, 9, 12, 166, 178, 204, 205],
    'P22': [4, 9, 17, 22, 74, 75],
    'P24': [26, 36, 44, 45, 47],
    'V13': [4, 5, 59, 60, 61],
    'V24': [4, 11, 12, 13, 20, 23, 24, 32, 37],
    'V17': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 33, 71, 73, 75,
            78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 100, 109, 110],
    'E24': [96],
}


def condition(row):
    taskid = row['meta']['task_id']
    return 'related_noop' if taskid.endswith(':high') else 'neutral_noop' if taskid.endswith(':low') else 'base'


def eval_expr(expr, values):
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.Name):
            return values[node.id]
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
        raise ValueError(ast.dump(node))
    return visit(ast.parse(expr, mode='eval').body)


def recompute(task, override=None):
    values = {p['premise_id']: int(p['value']) for p in task['premises'] if p['kind'] == 'definition'}
    pending = list(task['nodes'])
    while pending:
        before = len(pending)
        for node in list(pending):
            try:
                value = override[1] if override and node['id'] == override[0] else eval_expr(node['expression'], values) % 23
            except KeyError:
                continue
            values[node['id']] = value
            pending.remove(node)
        assert len(pending) < before, 'Non-topological or incomplete graph'
    return values


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    rows = load()
    lookup = {r['code']: r for r in rows}
    inventory = []
    for r in rows:
        digest = hashlib.sha256(r['text'].encode()).hexdigest()
        if 'text_sha256' in r['meta']:
            assert digest == r['meta']['text_sha256']
        item = {k: r[k] for k in ('code', 'source', 'source_line')}
        item.update(task_id=r['meta']['task_id'], seed=r['meta']['seed'], condition=condition(r),
                    correct=r['meta']['correct'], text_sha256=digest,
                    review_depth='focused_source_passages' if condition(r) == 'related_noop' else 'retrieval_screen',
                    judgment=JUDGMENTS.get(r['code']), archive_member=r.get('archive_member'))
        if r['code'] in SELECTED:
            ps = paragraphs(r)
            item['review_depth'] = 'selected_candidate_context_review'
            item['excerpts'] = [dict(paragraph=i, start=ps[i-1][0], end=ps[i-1][1], text=ps[i-1][2])
                                for i in SELECTED[r['code']]]
            header = f"TRACE {r['code']} | {r['meta']['task_id']} | seed={r['meta']['seed']}\nSource: {r['source']}\nJSONL line: {r['source_line']}\nArchive member: {r.get('archive_member')}\nText SHA256: {digest}\n\nParagraph labels and offsets are audit annotations; paragraph contents below are copied verbatim.\n"
            full = header + '\n\n'.join(f'[P{i:03} chars {s}:{e}]\n{p}' for i,(s,e,p) in enumerate(ps,1)) + '\n'
            (EVIDENCE / f"{r['code']}.txt").write_text(full)
        inventory.append(item)

    # Deterministic verification against saved graph; no additional generation.
    task = lookup['V17']['task']
    canonical = recompute(task)
    assert all(canonical[n['id']] == int(n['value']) for n in task['nodes'])
    chosen = 'p_0_1_0_0'
    assert next(n for n in task['nodes'] if n['id'] == chosen)['aliases'][1] == "Aquarium's Frilled Lizard"
    sensitivity = [{'override': x, 'final': recompute(task, (chosen, x))[task['target']]} for x in range(23)]
    assert {v['final'] for v in sensitivity} == {7}
    wrong = recompute(task, (chosen, 19))
    comparison = [dict(node=n['id'], name=n['aliases'][1], erroneous_path=wrong[n['id']], corrected_path=canonical[n['id']])
                  for n in task['nodes'] if n['id'] == chosen or wrong[n['id']] != canonical[n['id']] or n['id'] == task['target']]
    assert sum(v['erroneous_path'] != v['corrected_path'] for v in comparison) == 9

    tasks = [t for folder in ('pr9-pilot-20261009', 'pr9-validation-20261010')
             for t in jsonl(PR9 / 'inputs' / folder / 'tasks.jsonl')]
    target_children = [dict(task_id=t['task_id'], target=t['target'],
                            children=[n['id'] for n in t['nodes'] if t['target'] in n['parents']]) for t in tasks]
    assert len(tasks) == 24 and all(not t['children'] for t in target_children)
    summary = dict(repository_commit='2d5a76e0065d33c15d72712901a44813216d6290',
                   no_new_model_runs=True, labels_are_independently_validated=False,
                   selection='PR9 exports: sorted reference trace IDs by digest, first 24 per run; PR8 original unedited traces only.',
                   trace_counts={prefix: dict(Counter(condition(r) for r in rows if r['code'].startswith(prefix))) for prefix in ('P','V','E')},
                   inspected_fulltext_records=72, source_focused_records=17,
                   warning='72 is retrieval coverage, not 72 independently or exhaustively annotated chains. No prevalence estimate.',
                   confirmed_strict_post_correction_same_source_computational_recurrence=0,
                   v17_math_check=dict(override_node=chosen, all_residues=sensitivity, comparison=comparison,
                                      formula='225*(12*x-6)+2*x+12*x = 2714*x-1350 = 7 (mod 23)',
                                      interpretation='Exact task-graph cancellation; not a measured LLM counterfactual.'),
                   target_children=target_children, inventory=inventory)
    (DEST / 'natural-recurrence-evidence.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')

    missing = []
    for prefix, run in [('P', 'pr9-pilot-20261009'), ('V', 'pr9-validation-natural-20261010')]:
        present = {r['meta']['id'] for r in rows if r['code'].startswith(prefix)}
        saved = jsonl(PR9 / 'runs' / run / 'checkpoint_summary.jsonl')
        eligible = [r for r in saved if r['role'] in ('reference', 'noise')]
        assert len(eligible) == 72 and len(present) == 24
        for record in eligible:
            if record['id'] in present:
                continue
            missing.append(dict(run=run, expected_server_relative_path=f"runs/{run}/responses/{record['request_id']}.json",
                                checkpoint_summary=f"artifacts/{PR9.name}/runs/{run}/checkpoint_summary.jsonl",
                                **record))
    assert len(missing) == 96
    assert Counter(r['role'] for r in missing) == {'reference': 24, 'noise': 72}
    manifest = dict(scope='Existing PR9 reference/noise full texts absent from the local audit export; do not regenerate.',
                    server_repository_hint='/mnt/mydata/wja/reasoning-diff',
                    counts=dict(Counter(r['role'] for r in missing)), records=missing)
    (DEST / 'missing-pr9-fulltexts.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: summary[k] for k in ('trace_counts','inspected_fulltext_records','source_focused_records')}, ensure_ascii=False))
    print('V17 graph check:', comparison)
    print('Existing PR9 full texts to locate:', len(missing), manifest['counts'])


if __name__ == '__main__':
    main()
