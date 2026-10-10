import json,re,time
from collections import Counter
from pathlib import Path
B=Path('/mnt/mydata/wja/reasoning-diff');r=B/'runs/pr9-quantity-constrained-v3-20261009';ts=[]
for p in sorted((r/'responses').glob('*.json')):
 try:ts.append(json.loads(p.read_text())['trace'])
 except Exception:pass
rows=[]
for t in ts:
 m=t.get('metadata',{});body=t.get('text','')[m.get('rendered_prompt_char_len',0):]
 steps=re.findall(r'<step\s+node="[^"]+">(.*?)<commit>',body,re.S)
 ph=[s for s in steps if re.fullmatch(r'\s*your reasoning[.\s]*',s,re.I)]
 rows.append({'id':t.get('id'),'role':m.get('formal_role'),'task_id':t.get('task_id'),'correct':t.get('correct'),'format_pass':m.get('quantity_step_format',{}).get('passed'),'steps':len(steps),'placeholder_steps':len(ph),'forced_commit_nodes':m.get('quantity_constraint',{}).get('reasoning_budget_forced_commits',0),'text_chars':len(body)})
by={}
for role in ['reference','noise','edit','source']:
 x=[z for z in rows if z['role']==role];by[role]={'traces':len(x),'correct':sum(z['correct'] is True for z in x),'format_pass':sum(z['format_pass'] is True for z in x),'steps':sum(z['steps'] for z in x),'placeholder_steps':sum(z['placeholder_steps'] for z in x),'placeholder_rate':(sum(z['placeholder_steps'] for z in x)/sum(z['steps'] for z in x) if sum(z['steps'] for z in x) else None),'forced_commit_traces':sum(z['forced_commit_nodes']>0 for z in x)}
out={'created_at':time.time(),'run':str(r),'n_traces':len(rows),'by_role':by,'all_format_pass':all(z['format_pass'] for z in rows),'reference_placeholder_rate':by.get('reference',{}).get('placeholder_rate'),'reference_accuracy':by.get('reference',{}).get('correct',0)/by.get('reference',{}).get('traces',1),'gate_thresholds':{'reference_placeholder_rate_max':0.10,'all_format_pass_required':True},'gate_passed':bool(rows) and all(z['format_pass'] for z in rows) and by['reference']['placeholder_rate']<=.10,'interpretation':'Engineering semantic screen; no trace was regenerated or excluded.'}
(B/'runs/pr9-quantity-constrained-v3-20261009/semantic_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(B/'runs/pr9-quantity-constrained-v3-20261009/semantic_audit_rows.jsonl').write_text(''.join(json.dumps(z,ensure_ascii=False)+'\n' for z in rows))
print(json.dumps(out,ensure_ascii=False,indent=2))
