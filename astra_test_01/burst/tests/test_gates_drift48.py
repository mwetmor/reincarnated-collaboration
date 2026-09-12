from gates.drift48 import evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_comparator_at_48(self):
        self.assertTrue(evaluate([sprite(),sprite(1)],sprite(20))['passed'])
        self.assertFalse(evaluate([sprite(),sprite(20)],sprite(1))['passed'])
