from __future__ import annotations
import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path
B=Path('/mnt/mydata/wja/reasoning-diff'); REPO=Path('/home/wja/reasoning-diff-pr9-quantity-v3'); OPS=B/'operations/pr9-formal-gate-20261010'; STATE=OPS/'queue.json'
V={'natural':(B/'runs/pr9-validation-natural-20261010',B/'configs/pr9-validation-natural-20261010.json',6),'controlled':(B/'runs/pr9-validation-controlled-20261010',B/'configs/pr9-validation-controlled-20261010.json',7)}
F={'natural':(B/'runs/pr9-formal-natural-20261010',B/'configs/pr9-formal-natural-20261010.json',6),'controlled':(B/'runs/pr9-formal-controlled-20261010',B/'configs/pr9-formal-controlled-20261010.json',7)}
def now():return datetime.now().astimezone().isoformat()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def count(root):return len(list((root/'responses').glob('*.json')))
def status(root):
 p=root/'pipeline.json'
 if p.exists():
  try:return read(p).get('status')
  except:pass
 return 'running' if (root/'responses').exists() else 'planned'
def pid_alive(pid):
 try:return Path(f'/proc/{pid}').exists()
 except:return False
def refresh(state):
 for label,items in [('validation',V),('formal',F)]:
  for name,(root,config,gpu) in items.items():
   key=f'{label}_{name}'; entry=state.get('children',{}).get(key,{})
   pid=entry.get('pid'); rc=None if pid and pid_alive(pid) else entry.get('returncode',0)
   state.setdefault('progress',{})[key]={'pid':pid,'gpu':gpu,'responses':count(root),'pipeline':status(root),'process_alive':bool(pid and pid_alive(pid)),'returncode':rc,'updated_at':now()}
 state['updated_at']=now();write(STATE,state)
def validation_ready(name, root):
    planned=read(root/'plan_summary.json')['requests'] if (root/'plan_summary.json').exists() else 0
    complete=count(root)==planned and planned>0
    measured=(root/'measurement.json').exists()
    measurement=read(root/'measurement.json') if measured else {}
    reports=measurement.get('conditions',{})
    checks={}
    for condition in ('base','related_noop','neutral_noop'):
        report=reports.get(condition,{})
        groups=[report.get('overall',{}),*report.get('by_op',{}).values(),*report.get('by_problem',{}).values()]
        checks[condition]=bool(report.get('passed')) and bool(report.get('by_op')) and bool(report.get('by_problem')) and all(
            isinstance(group.get(key),(int,float)) and group[key]>=.95
            for group in groups for key in ('matched_cell_coverage','common_noise_coverage','rho_coverage'))
    return complete and measured and all(checks.values()), {
        'planned':planned,'responses':count(root),'pipeline':status(root),
        'measurement':measured,'coverage_checks':checks,'minimum_coverage':.95}

def gate(state):
    vals={};ready={}
    for n,(root,_,_) in V.items(): ready[n],vals[n]=validation_ready(n,root)
    cond={'validation_natural_matching':ready['natural'], 'validation_controlled_matching':ready['controlled']}
    formal_file=OPS/'formal_candidates.json'
    formal_info=read(formal_file) if formal_file.exists() else {}
    formal_ready=formal_info.get('fresh_generator_cohort') is True and formal_info.get('n_test_families',0)>=24 and formal_info.get('frozen_disjoint_design') is True
    semantic=OPS/'independent_semantic_audit.json'
    semantic_ok=semantic.exists() and read(semantic).get('passed') is True
    cond.update(fresh_formal_test_cohort=formal_ready, independent_semantic_audit=semantic_ok)
    d={'updated_at':now(),'conditions':cond,'launch_formal':all(cond.values()),
       'validation':vals,'minimum_coverage':.95,
       'decision_note':'Generation completion and constrained format alone do not establish natural matching or semantic validity. Original placeholder count is a quality screen, not an independent semantic audit.',
       'formal_candidate':formal_info}
    write(OPS/'validation_gate.json',d)
    return d
def launch_formal(state):
 for name,(root,config,gpu) in F.items():
  if state.get('children',{}).get('formal_'+name,{}).get('pid'):continue
  (root/'logs').mkdir(parents=True,exist_ok=True);(root/'tmp').mkdir(exist_ok=True)
  env=dict(os.environ,PYTHONPATH='src:scripts',PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',CUDA_VISIBLE_DEVICES='',TMPDIR=str(root/'tmp'))
  cmd=[str(Path('/mnt/mydata/zm/projects/RPent/.venv/bin/python')),str(OPS/'continue_unlimited.py'),'--mode','all','--config',str(config),'--out-root',str(root)]
  log=(root/'runner.log').open('a');p=subprocess.Popen(cmd,cwd=REPO,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
  state.setdefault('children',{})['formal_'+name]={'pid':p.pid,'gpu':gpu,'root':str(root),'started_at':now(),'command':cmd}
 state['status']='formal_running';write(STATE,state)
if __name__=='__main__':
 state=read(STATE);state['supervisor_pid']=os.getpid();state['supervisor_started_at']=now();state['status']='validation_running';write(STATE,state)
 while True:
  refresh(state)
  vp=gate(state);state['validation_gate']=vp
  val_alive=any(state['progress'].get('validation_'+n,{}).get('process_alive') for n in V)
  if not val_alive and vp['launch_formal'] and not any(state.get('children',{}).get('formal_'+n,{}).get('pid') for n in F):launch_formal(state)
  if state.get('status')=='formal_running':
   formal_alive=any(state['progress'].get('formal_'+n,{}).get('process_alive') for n in F)
   if not formal_alive and all(status(root) in {'complete','stopped_unestimable','stopped_unmeasurable','failed','budget_exhausted'} for root,_,_ in F.values()):state['status']='complete'
  if not val_alive and not vp['launch_formal']:
   state['status']='awaiting_acceptance_criteria'
  if state.get('status')=='complete':
   refresh(state);state['finished_at']=now();write(STATE,state);break
  time.sleep(30)
