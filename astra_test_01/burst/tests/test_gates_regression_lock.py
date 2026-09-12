import json
from gates.run_gates import measurements,regression_diff
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_regression_lock(self):
        expected=json.loads((ROOT.parent/'run_03/evidence/current_checks.json').read_text())
        output=json.loads((ROOT.parent/'run_03/output_contact_regions.json').read_text())
        source=json.loads((ROOT.parent/'run_03/source_contact_regions.json').read_text())
        self.assertTrue(source)  # Source-cell coordinates must NOT be used on registered frames.
        regions={k.removeprefix('character/frames/'):v['regions'] for k,v in output.items()}
        actual=measurements(FIXTURE_ROOT,regions=regions)
        report=regression_diff(actual,expected)
        # Persistent evidence is intentional, not a temporary fixture.
        (ROOT/'tests/gates_regression_diff.json').write_text(json.dumps(report,indent=2)+'\n')
        self.assertGreater(report['compared'],1500)
        self.assertTrue(report['within_tolerance'],json.dumps(report['differences'][:8]))
