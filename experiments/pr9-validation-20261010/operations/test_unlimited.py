import importlib.util,json,tempfile,sys,unittest
from pathlib import Path
from unittest.mock import patch
OPS=Path(__file__).parent
spec=importlib.util.spec_from_file_location('unlimited',OPS/'continue_unlimited.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class UnlimitedTests(unittest.TestCase):
 def test_expired_budget_does_not_stop_new_stage(self):
  with tempfile.TemporaryDirectory(dir=OPS,prefix='timeout-test-') as x:
   root=Path(x);(root/'budget.json').write_text('{"started":0,"seconds":1}')
   executor=mod.install_unlimited_executor()
   with patch.object(mod.formal,'verified_plan',return_value=({'config':{'model_root':'unused','time_budget_hours':12}},{})):
    executor(root,'after-old-deadline',[sys.executable,'-c','print("finished")'])
   self.assertIn('finished',(root/'logs/after-old-deadline.log').read_text())
 def test_command_failure_remains_failure(self):
  import subprocess
  with tempfile.TemporaryDirectory(dir=OPS,prefix='failure-test-') as x:
   with patch.object(mod.formal,'verified_plan',return_value=({'config':{'model_root':'unused','time_budget_hours':12}},{})):
    with self.assertRaises(subprocess.CalledProcessError):
     mod.install_unlimited_executor()(Path(x),'command-error',[sys.executable,'-c','raise SystemExit(7)'])
if __name__=='__main__':unittest.main()
