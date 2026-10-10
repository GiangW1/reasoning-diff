"""Operational timeout override; leave frozen source and sampling untouched."""
from __future__ import annotations
import argparse, inspect, json, os, sys, time
from datetime import datetime
from pathlib import Path
REPO=Path('/home/wja/reasoning-diff-pr9-quantity-v3')
sys.path[:0]=[str(REPO/'src'),str(REPO/'scripts')]
import run_formal as formal
BASE_EXECUTE=formal.execute

def now():return datetime.now().astimezone().isoformat()
def write(path, data):
 tmp=path.with_suffix(path.suffix+'.tmp')
 tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)

def install_unlimited_executor():
 # Use the exact frozen executor, removing only the persisted-budget block.
 source=inspect.getsource(BASE_EXECUTE)
 start=source.index("    if config.get('time_budget_hours') is not None:\n")
 end=source.index("    logs = root / 'logs'\n",start)
 source=source[:start]+source[end:]
 exec(compile(source,str(Path(__file__))+'::unlimited_execute','exec'),formal.__dict__)
 return formal.execute

def worker_alive(pid, root):
 proc=Path('/proc')/str(pid)
 try:
  if proc.joinpath('stat').read_text().split(') ',1)[1].split()[0]=='Z':return False
  command=proc.joinpath('cmdline').read_bytes()
 except FileNotFoundError:return False
 if str(root).encode() not in command or b'worker' not in command:
  raise RuntimeError('attached PID no longer belongs to the registered worker')
 return True

def comparison_report(root):
 other=root.parent/'pr9-validation-controlled-20261010'
 ops=Path(__file__).parent
 result={'updated_at':now(),'batches':{},'single_generation_per_condition':True}
 lines=['# 自然与受控协议验证结果',f'更新：{result["updated_at"]}','','每个注册条件只生成一次，失败保留；受控格式覆盖率由约束保证。','']
 for label,r in [('自然',root),('受控',other)]:
  data={'root':str(r)}; counts={}; correct={}
  for p in (r/'responses').glob('*.json'):
   trace=json.loads(p.read_text())['trace'];role=trace['metadata']['formal_role']
   counts[role]=counts.get(role,0)+1;correct[role]=correct.get(role,0)+(trace.get('correct') is True)
  data['completed_by_role']=counts;data['correct_by_role']=correct
  data['measurement']=json.loads((r/'measurement.json').read_text()) if (r/'measurement.json').exists() else None
  result['batches'][label]=data
  lines += [f'## {label}',f'已生成 {sum(counts.values())} 条；参考答对 {correct.get("reference",0)}/{counts.get("reference",0)}。','']
  if data['measurement']:
   lines += ['| 条件 | 匹配覆盖率 | 噪声共同覆盖率 | rho覆盖率 |','|---|---:|---:|---:|']
   for condition,report in data['measurement']['conditions'].items():
    group=report['overall'];lines.append(f'| {condition} | {group["matched_cell_coverage"]:.2%} | {group["common_noise_coverage"]:.2%} | {group["rho_coverage"]:.2%} |')
   lines += ['']
 lines += ['该验证集没有test题族，P3不可估计。自然参考若全答对，则无法在此批估计错误预测效果。正式组启动由实际覆盖率、语义审查及独立正式题库决定。']
 write(ops/'VALIDATION_RESULTS.json',result)
 (ops/'VALIDATION_RESULTS.zh-CN.md').write_text('\n'.join(lines)+'\n')

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--attach-worker',type=int)
 parser.add_argument('--out-root',type=Path,required=True)
 opts,remaining=parser.parse_known_args()
 root=opts.out_root.resolve()
 protocol,design=formal.verified_plan(root)
 install_unlimited_executor()
 write(root/'budget_override.json',{'enabled':True,'time_budget_hours':None,'deadline':None,'requested_at':now(),'requested_by_user':'去掉预算截至','original_budget':json.loads((root/'budget.json').read_text()) if (root/'budget.json').exists() else None,'frozen_protocol_unchanged':True})
 if opts.attach_worker:
  write(root/'continuation.json',{'pid':os.getpid(),'attached_worker_pid':opts.attach_worker,'status':'waiting_for_existing_generation','deadline':None,'started_at':now()})
  while worker_alive(opts.attach_worker,root):time.sleep(5)
  # Verify every registered checkpoint; never regenerate an unfinished attempt.
  if any(formal.saved_response(root,protocol,r) is None for r in design['requests']):
   write(root/'continuation.json',{'pid':os.getpid(),'status':'incomplete_generation','deadline':None,'finished_at':now()})
   raise RuntimeError('worker exited with missing registered responses; no retry was performed')
  try:
   formal.main(['--mode','measure','--out-root',str(root)])
   # This continuation produces validation statistics, not a fictitious P3 result.
   write(root/'validation_analysis_status.json',{'status':'measurement_complete','completed_at':now(),'p3':'not_estimable_no_test_families','p1':json.loads((root/'answer_screen.json').read_text())['status'],'budget_deadline':None})
  finally:comparison_report(root)
  write(root/'continuation.json',{'pid':os.getpid(),'status':'measurement_complete','deadline':None,'finished_at':now()})
 else:
  return formal.main([*remaining,'--out-root',str(root)])
 return 0
if __name__=='__main__':raise SystemExit(main())
