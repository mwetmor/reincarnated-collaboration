from gates.g3_light import evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_wrong_side_light(self):
        self.assertTrue(evaluate(sprite())['passed'])
        self.assertFalse(evaluate(sprite(wrong_light=True))['passed'])
    def test_wrong_side_and_clipping_detection(self):
        from gates.g9_alpha import evaluate as alpha
        bad=sprite(wrong_light=True);ImageDraw.Draw(bad).rectangle((45,0,55,20),fill='white')
        self.assertFalse(alpha(bad)[0]['passed'])
        self.assertFalse(evaluate(sprite(wrong_light=True))['passed'])
