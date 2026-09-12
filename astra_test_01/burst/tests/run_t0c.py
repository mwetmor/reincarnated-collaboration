"""Run the full local unittest suite and write machine-readable evidence.
Execute from burst root: python3 -B tests/run_t0c.py. No temp outside tests/tmp.
Two F04 assertions remain active; they are not xfailed or threshold-tuned.
"""
import json
import sys
import time
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
(ROOT/'tests/tmp').mkdir(exist_ok=True)
started=time.monotonic()
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
with (ROOT/'tests/t0c_suite_output.txt').open('w') as stream:
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
summary={'tests_run':result.testsRun,'successful_tests':result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),'failures':[{'test':t.id(),'traceback':trace} for t,trace in result.failures],'errors':[{'test':t.id(),'traceback':trace} for t,trace in result.errors],'skipped':result.skipped,'elapsed_s':time.monotonic()-started,'regression':json.loads((ROOT/'tests/gates_regression_diff.json').read_text()),'acceptance':json.loads((ROOT/'tests/oracles_acceptance_measurements.json').read_text()),'palette':json.loads((ROOT/'tests/oracles_palette_measurements.json').read_text()),'silhouette':json.loads((ROOT/'tests/oracles_silhouette_measurements.json').read_text()),'parts':json.loads((ROOT/'tests/parts_measurements.json').read_text())}
(ROOT/'tests/t0c_summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:summary[k] for k in ['tests_run','successful_tests','elapsed_s']}))
raise SystemExit(0 if result.wasSuccessful() else 1)
