import importlib.util,json,tempfile,unittest
from pathlib import Path
OPS=Path(__file__).parent
spec=importlib.util.spec_from_file_location('supervisor',OPS/'supervise.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class AcceptanceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=OPS,prefix='acceptance-test-');self.root=Path(self.tmp.name);(self.root/'responses').mkdir();(self.root/'responses/a.json').write_text('{}');(self.root/'plan_summary.json').write_text('{"requests":1}');(self.root/'pipeline.json').write_text('{"status":"complete"}')
 def tearDown(self):self.tmp.cleanup()
 def measurement(self,overall=1.,problem=1.):
  def group(value):return {k:value for k in ('matched_cell_coverage','common_noise_coverage','rho_coverage')}
  report={'passed':True,'overall':group(overall),'by_op':{'5':group(1.)},'by_problem':{'problem':group(problem)}}
  (self.root/'measurement.json').write_text(json.dumps({'conditions':{k:report for k in ('base','related_noop','neutral_noop')}}))
 def test_completion_does_not_bypass_low_coverage(self):
  self.measurement(overall=.4);self.assertFalse(mod.validation_ready('natural',self.root)[0])
 def test_poor_single_problem_blocks_high_overall(self):
  self.measurement(problem=.7);self.assertFalse(mod.validation_ready('natural',self.root)[0])
 def test_all_registered_traces_required(self):
  self.measurement();(self.root/'plan_summary.json').write_text('{"requests":2}');self.assertFalse(mod.validation_ready('natural',self.root)[0])
 def test_missing_measurement_blocks(self):self.assertFalse(mod.validation_ready('natural',self.root)[0])
 def test_report_only_failure_does_not_hide_good_measurement(self):
  self.measurement();(self.root/'pipeline.json').write_text('{"status":"failed","error":"missing p3-gpu0.jsonl"}');self.assertTrue(mod.validation_ready('controlled',self.root)[0])
if __name__=='__main__':unittest.main()
