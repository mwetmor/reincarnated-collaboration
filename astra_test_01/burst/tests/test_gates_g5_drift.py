from gates.g5_drift import evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_excessive_drift_and_missing_comparator(self):
        self.assertTrue(evaluate([sprite(),sprite(1)],sprite(20))['passed'])
        self.assertFalse(evaluate([sprite(),sprite(20)],sprite(1))['passed'])
        self.assertIsNone(evaluate([sprite(),sprite(1)])['passed'])
