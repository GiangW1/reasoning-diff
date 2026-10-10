import json
from collections import Counter
from pathlib import Path
from reasoning_diff.io import digest, file_digest
from reasoning_diff.schema import Task
from reasoning_diff.splits import split_for_task
B=Path('/mnt/mydata/wja/reasoning-diff'); d=json.loads((B/'runs/pr9-formal-20261008-r2/design.json').read_text())
current=set(json.loads((B/'inputs/pr9-pilot-20261009/selection.json').read_text())['selected_groups'])
pool={t['base_group_id']:t for t in d['tasks'] if t['task_id']==t['base_group_id'] and t['metadata']['formal_condition']=='base'}
remaining=set(pool)-current
byop={op:sorted((pool[g] for g in remaining if pool[g]['metadata']['op']==op),key=lambda t:digest([7319,'formal',t['base_group_id']])) for op in (5,10,15,21)}
# Formal set is fixed first and contains the only remaining test family.
test=[pool[t] for t in remaining if split_for_task(Task.from_dict(pool[t]),seed=7319)=='test']; assert len(test)==1,test
formal=[]
for op in (5,10,15,21):
 bucket=byop[op]; forced=[t for t in test if t['metadata']['op']==op]
 take=forced[:1]+[t for t in bucket if t not in forced][:6-len(forced)]
 assert len(take)==6
 formal.extend(take)
formal_ids={t['base_group_id'] for t in formal}
rest=[t for op in (5,10,15,21) for t in byop[op] if t['base_group_id'] not in formal_ids]
# Validation is a disjoint 12-family check, balanced by operation.
validation=[]
for op in (5,10,15,21): validation.extend([t for t in rest if t['metadata']['op']==op][:3])
assert len(validation)==12 and not formal_ids & {t['base_group_id'] for t in validation}
for label,tasks,exposure in [('validation',validation,'development_exposed_identity_holdout; validation_only; not_confirmatory'),('formal',sorted(formal,key=lambda t:t['base_group_id']),'official_snapshot_identity_holdout; design_frozen_before_validation_outcomes; model_exposure_unknown; formal_engineering_group')]:
 out=B/'inputs'/('pr9-validation-20261010' if label=='validation' else 'pr9-formal-holdout-20261010');out.mkdir(parents=True,exist_ok=True)
 (out/'tasks.jsonl').write_text(''.join(json.dumps(t,sort_keys=True)+'\n' for t in tasks))
 manifest={'selected_groups':[t['base_group_id'] for t in tasks],'excluded_current_groups':sorted(current),'outcomes_used_for_selection':False,'seed':7319,'difficulty_counts':dict(Counter(t['metadata']['op'] for t in tasks)),'family_roles':dict(Counter(split_for_task(Task.from_dict(t),seed=7319) for t in tasks)),'source_design_sha256':file_digest(B/'runs/pr9-formal-20261008-r2/design.json'),'dataset_sha256':file_digest(out/'tasks.jsonl'),'dataset_exposure':exposure,'selection':'formal first; forced remaining test family into formal; operation balanced; deterministic hash order; roles preserved'}
 (out/'selection.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(label,manifest['difficulty_counts'],manifest['family_roles'],manifest['selected_groups'])
base=json.loads((B/'configs/pr9-constrained-v3-20261009.json').read_text())
for label,n,sub,exposure in [('validation',12,'pr9-validation-20261010','development_exposed_identity_holdout; validation_only; not_confirmatory'),('formal',24,'pr9-formal-holdout-20261010','official_snapshot_identity_holdout; design_frozen_before_validation_outcomes; model_exposure_unknown; formal_engineering_group')]:
 for protocol,gpu in [('natural',6),('controlled',7)]:
  c=dict(base);c.update({'dataset':str(B/'inputs'/sub/'tasks.jsonl'),'dataset_exposure':exposure,'exclude_groups':sorted(current),'gpus':[gpu],'batch_size':1,'gpu_min_free_mib':21000,'time_budget_hours':12,'n_problems':n,'trajectory_protocol':'natural' if protocol=='natural' else 'quantity_steps'})
  c.pop('quantity_decoding_protocol',None)
  if protocol=='controlled':c['quantity_decoding_protocol']='registered_quantity_constrained_v3'
  (B/'configs'/f'pr9-{label}-{protocol}-20261010.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
