"""Independent deterministic saved-graph evaluation; no model counterfactuals."""
import ast
from collections import defaultdict
from functools import lru_cache
import json
from pathlib import Path

OUT = Path('/mnt/mydata/wja/reasoning-diff/reports/pr10-server-recurrence-review-20261010')


@lru_cache(None)
def tree(expression):
    return ast.parse(expression, mode='eval').body


def calculate(node, values):
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return node.value
    if isinstance(node, ast.Name):
        return values[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -calculate(node.operand, values)
    if isinstance(node, ast.BinOp):
        a, b = calculate(node.left, values), calculate(node.right, values)
        if isinstance(node.op, ast.Add): return a+b
        if isinstance(node.op, ast.Sub): return a-b
        if isinstance(node.op, ast.Mult): return a*b
    raise ValueError(ast.dump(node))


def evaluate(task, override=None):
    values = {p['premise_id']: int(p['value']) % 23 for p in task['premises'] if p['kind']=='definition'}
    pending = list(task['nodes'])
    while pending:
        count = len(pending)
        for node in pending[:]:
            try:
                value = override[1] if override and node['id']==override[0] else calculate(tree(node['expression']), values)
            except KeyError:
                continue
            values[node['id']] = value % 23
            pending.remove(node)
        if len(pending)==count: raise ValueError('Saved graph has unresolved dependencies')
    return values


def children(task):
    result = defaultdict(list)
    for node in task['nodes']:
        for parent in node['parents']: result[parent].append(node['id'])
    return result


def sensitivity(task, node_id, wrong_value=None):
    canonical = evaluate(task)
    child = children(task)
    reachable, pending = set(), list(child[node_id])
    while pending:
        next_id = pending.pop()
        if next_id not in reachable:
            reachable.add(next_id); pending.extend(child[next_id])
    alternatives = [{'override':x,'final':evaluate(task,(node_id,x))[task['target']]} for x in range(23)]
    node = next(n for n in task['nodes'] if n['id']==node_id)
    result = {'node_id':node_id,'aliases':node['aliases'],'canonical_value':canonical[node_id],
              'children':child[node_id],'descendants':sorted(reachable),
              'target':task['target'],'target_is_descendant':task['target'] in reachable,
              'canonical_final':canonical[task['target']], 'all_residues':alternatives,
              'distinct_final_values':len({r['final'] for r in alternatives}),
              'final_numerically_sensitive':len({r['final'] for r in alternatives})>1}
    if wrong_value is not None:
        altered=evaluate(task,(node_id,wrong_value))
        result.update(wrong_value=wrong_value,wrong_final=altered[task['target']],
                      comparison=[{'node_id':n['id'],'aliases':n['aliases'], 'canonical':canonical[n['id']], 'wrong_path':altered[n['id']]}
                                  for n in task['nodes'] if canonical[n['id']]!=altered[n['id']] or n['id']==task['target']],
                      changed_downstream_nodes=[key for key in sorted(reachable) if canonical[key]!=altered[key]])
    return result


def main():
    records=[json.loads(line) for line in (OUT/'records.jsonl').read_text().splitlines()]
    lookup={r['code']:r for r in records}
    base={r['meta']['base_group_id']:r['task'] for r in records if r['code'][0] in {'P','V'} and r['condition']=='base'}
    assert len(base)==24
    baseline_checks=[]; node_checks=[]
    for task in base.values():
        computed=evaluate(task)
        assert all(computed[n['id']]==int(n['value']) % 23 for n in task['nodes'])
        assert computed[task['target']]==int(task['answer_spec']['value']) % 23
        baseline_checks.append({'task_id':task['task_id'],'target':task['target'],
                                'target_children':children(task)[task['target']], 'canonical_matches_saved_nodes_and_answer':True})
        for node in task['nodes']:
            if node['id']!=task['target']:
                check=sensitivity(task,node['id'])
                node_checks.append({'task_id':task['task_id'],**check})
    assert all(not r['target_children'] for r in baseline_checks)
    specs=[('V17',"Aquarium's Frilled Lizard",19,'observed_arithmetic_error'),
           ('P22',"Rockpool Exhibit's Trout",12,'initial_error_and_later_rejected_hypothesis'),
           ('P47',"Kangaroo's Hypothalamus",22,'inverse_constraint_with_uncorrected_source_binding'),
           ('P66',"Kangaroo's Hypothalamus",22,'conditional_inverse_constraint_not_actual_use'),
           ('P69',"Tiger's Alula",13,'post_correction_hypothesis_not_actual_use'),
           ('V58',"Walrus's Liver",12,'value_implied_by_rejected_difference_constraint_not_observed_working_value')]
    cases={}
    for code,alias,wrong,interpretation in specs:
        task=lookup[code]['task']
        node=next(n for n in task['nodes'] if alias in n['aliases'])
        cases[code]={'trace_id':lookup[code]['meta']['id'],'task_id':task['task_id'],
                     'candidate_value_interpretation':interpretation,**sensitivity(task,node['id'],wrong)}
    for code in ['P05','P24','V13','V24','P48','V50','P32','V69','V70','V59','V43','P26','P27','P31']:
        task=lookup[code]['task']
        cases[code]={'trace_id':lookup[code]['meta']['id'],'task_id':task['task_id'],
                     'candidate_value_interpretation':'wrong_target_restatement_or_hypothesis; direct target override is not observed propagation',
                     **sensitivity(task,task['target'],17)}
    task=lookup['E24']['task']
    cases['E24']={'trace_id':lookup['E24']['meta']['id'],'task_id':task['task_id'],
                  'candidate_value_interpretation':'explicitly rejected reversed subtraction hypothetical',
                  **sensitivity(task,task['target'],16)}
    for code,alias,unreduced,reduced in [
            ('P40',"Walmart's Ingredient",54,31),
            ('P71',"Walmart's Ingredient",54,31),
            ('E18',"Canned Vegetables's Thyme",59,36)]:
        task=lookup[code]['task']
        node=next(n for n in task['nodes'] if alias in n['aliases'])
        assert unreduced % 23 == reduced % 23 == evaluate(task)[node['id']]
        cases[code]={'trace_id':lookup[code]['meta']['id'],'task_id':task['task_id'],
                     'candidate_value_interpretation':'modularly_equivalent_representatives; no observed numerical error',
                     'representative_a':unreduced,'representative_b':reduced,
                     'both_residues':unreduced % 23,
                     **sensitivity(task,node['id'])}
    v=cases['V17']
    assert v['canonical_value']==13 and v['wrong_final']==7 and v['distinct_final_values']==1
    assert len(v['changed_downstream_nodes'])==8
    report={'analysis_kind':'deterministic_task_graph_only; not language-model intervention',
            'modulus':23,'all_canonical_checks':baseline_checks,'all_non_target_node_sensitivity':node_checks,
            'cases':cases,'summary':{'n_base_tasks':24,'target_with_children':0,
                                     'non_target_nodes_checked':len(node_checks),
                                     'nodes_with_target_path':sum(r['target_is_descendant'] for r in node_checks),
                                     'tasks_with_constant_final_node':len({r['task_id'] for r in node_checks if r['target_is_descendant'] and not r['final_numerically_sensitive']}),
                                     'nodes_with_target_path_but_constant_final':sum(r['target_is_descendant'] and not r['final_numerically_sensitive'] for r in node_checks)}}
    (OUT/'task-sensitivity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report['summary'],ensure_ascii=False,indent=2))
    print('V17',json.dumps({k:v[k] for k in ['canonical_value','wrong_value','wrong_final','distinct_final_values','changed_downstream_nodes']},ensure_ascii=False))


if __name__=='__main__': main()
