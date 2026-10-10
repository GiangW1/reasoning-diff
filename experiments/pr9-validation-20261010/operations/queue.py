from __future__ import annotations
import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path
B=Path('/mnt/mydata/wja/reasoning-diff'); REPO=Path('/home/wja/reasoning-diff-pr9-quantity-v3'); OPS=B/'operations/pr9-formal-gate-20261010';
V={
 'natural':(B/'runs/pr9-validation-natural-20261010',B/'configs/pr9-validation-natural-20261010.json',6),
 'controlled':(B/'runs/pr9-validation-controlled-20261010',B/'configs/pr9-validation-controlled-20261010.json',7)}
F={
 'natural':(B/'runs/pr9-formal-natural-20261010',B/'configs/pr9-formal-natural-20261010.json',6),
 'controlled':(B/'runs/pr9-formal-controlled-20261010',B/'configs/pr9-formal-controlled-20261010.json',7)}
STATE=OPS/'queue.json'; LOG=OPS/'queue.log'
def now():return datetime.now().astimezone().isoformat()
def write(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def read(path): return json.loads(path.read_text())
def status(root):
 p=root/'pipeline.json'
 if p.exists():
  try:return read(p).get('status')
  except:pass
 return 'running' if (root/'responses').exists() else 'planned'
def count(root):return len(list((root/'responses').glob('*.json')))
def launch(label,items,state):
 procs={}
 for name,(root,config,gpu) in items.items():
  (root/'logs').mkdir(parents=True,exist_ok=True)
  env=dict(os.environ,PYTHONPATH='src:scripts',PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',CUDA_VISIBLE_DEVICES='',TMPDIR=str(root/'tmp'))
  (root/'tmp').mkdir(exist_ok=True)
  cmd=[str(Path('/mnt/mydata/zm/projects/RPent/.venv/bin/python')),str(REPO/'scripts/run_formal.py'),'--mode','all','--config',str(config),'--out-root',str(root)]
  log=(root/'runner.log').open('a')
  p=subprocess.Popen(cmd,cwd=REPO,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
  procs[name]=(p,log); state.setdefault('children',{})[f'{label}_{name}']={'pid':p.pid,'gpu':gpu,'root':str(root),'started_at':now(),'command':cmd}
 write(STATE,state)
 return procs
def wait(label,items,procs,state):
 while True:
  done=True
  for name,(root,config,gpu) in items.items():
   p,log=procs[name]; rc=p.poll()
   state.setdefault('progress',{})[f'{label}_{name}']={'pid':p.pid,'gpu':gpu,'responses':count(root),'pipeline':status(root),'returncode':rc,'updated_at':now()}
   if rc is None:done=False
   else:log.close()
  write(STATE,state)
  if done:return
  time.sleep(30)
def validation_gate(state):
 audit=read(B/'runs/pr9-quantity-constrained-v3-20261009/semantic_audit.json')
 vals={name:{'pipeline':status(root),'responses':count(root)} for name,(root,_,_) in V.items()}
 conditions={'current_semantic_audit':audit.get('gate_passed') is True,'validation_natural_finished':vals['natural']['pipeline']=='complete','validation_controlled_finished':vals['controlled']['pipeline']=='complete','frozen_disjoint_design':True}
 # Formal holdout was frozen before this decision; this gate never edits or selects families based on outcomes.
 decision={'updated_at':now(),'conditions':conditions,'passed_count':sum(conditions.values()),'threshold':3,'launch_formal':sum(conditions.values())>=3,'validation':vals,'audit':audit}
 write(OPS/'validation_gate.json',decision)
 return decision
if __name__=='__main__':
 state={'status':'starting','started_at':now(),'validation_roots':{k:str(v[0]) for k,v in V.items()},'formal_roots':{k:str(v[0]) for k,v in F.items()},'design_frozen':True,'outcomes_used_for_selection':False}
 write(STATE,state)
 vp=launch('validation',V,state);state['status']='validation_running';write(STATE,state);wait('validation',V,vp,state)
 decision=validation_gate(state);state['validation_gate']=decision
 if decision['launch_formal']:
  fp=launch('formal',F,state);state['status']='formal_running';write(STATE,state);wait('formal',F,fp,state)
  state['status']='complete'
 else: state['status']='stopped_validation_gate'
 state['finished_at']=now();write(STATE,state)
