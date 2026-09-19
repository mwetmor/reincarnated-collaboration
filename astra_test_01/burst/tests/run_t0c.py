"""Run the full local unittest suite and write machine-readable evidence.
Execute from burst root: python3 -B tests/run_t0c.py. No temp outside tests/tmp.
All literal crop assertions remain active; none are xfailed or threshold-tuned.
"""
import json
import sys
import time
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
def result_summary(result, elapsed_s):
    """unittest setup holders and subtests are identifiers, never JSON objects."""
    def identifier(test):
        return test.id() if callable(getattr(test, 'id', None)) else str(test)
    return {
        'tests_run': result.testsRun,
        'successful_tests': result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
        'failures': [{'test': identifier(t), 'traceback': trace} for t, trace in result.failures],
        'errors': [{'test': identifier(t), 'traceback': trace} for t, trace in result.errors],
        'skipped': [(identifier(t), reason) for t, reason in result.skipped],
        'elapsed_s': elapsed_s,
    }


def write_summary(path, summary):
    path.write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')


def main():
    (ROOT/'tests/tmp').mkdir(exist_ok=True)
    started=time.monotonic()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    with (ROOT/'tests/t0c_suite_output.txt').open('w') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    summary={**result_summary(result,time.monotonic()-started),'regression':json.loads((ROOT/'tests/gates_regression_diff.json').read_text()),'acceptance':json.loads((ROOT/'tests/oracles_acceptance_measurements.json').read_text()),'palette':json.loads((ROOT/'tests/oracles_palette_measurements.json').read_text()),'silhouette':json.loads((ROOT/'tests/oracles_silhouette_measurements.json').read_text()),'parts':json.loads((ROOT/'tests/parts_measurements.json').read_text())}
    for name in ('o3b_calibration','f5_calibration','matte_quality_calibration','sheet_consistency_calibration'):
        path=ROOT/'tests'/(name+'.json')
        if path.is_file():summary[name]=json.loads(path.read_text())
    write_summary(ROOT/'tests/t0c_summary.json',summary)
    print(json.dumps({k:summary[k] for k in ['tests_run','successful_tests','elapsed_s']}))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
