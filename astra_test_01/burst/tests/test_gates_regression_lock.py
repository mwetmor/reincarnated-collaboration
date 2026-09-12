import json
from gates.run_gates import measurements,regression_diff
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_regression_lock(self):
        expected=json.loads((ROOT.parent/'run_03/evidence/current_checks.json').read_text())
        actual=measurements(FIXTURE_ROOT)
        report=regression_diff(actual,expected)
        # Persistent evidence is intentional, not a temporary fixture.
        (ROOT/'tests/gates_regression_diff.json').write_text(json.dumps(report,indent=2)+'\n')
        self.assertGreater(report['compared'],1500)
        self.assertTrue(report['within_tolerance'],json.dumps(report['differences'][:8]))
