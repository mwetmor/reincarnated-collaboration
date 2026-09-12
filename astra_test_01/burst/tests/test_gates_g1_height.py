from gates.g1_height import evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_height_mutation(self):
        self.assertTrue(evaluate(sprite(),sprite())['passed'])
        bad=sprite();ImageDraw.Draw(bad).rectangle((50,1,60,30),fill='white')
        self.assertFalse(evaluate(bad,sprite())['passed'])
