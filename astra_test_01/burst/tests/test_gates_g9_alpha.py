from gates.g9_alpha import evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_dark_fringe_and_green(self):
        im=sprite();a=np.array(im);a[30:40,43:45]=[0,0,0,100]
        rows=evaluate(Image.fromarray(a),dark_threshold=20)
        self.assertFalse(rows[-1]['passed'])
        a[30:40,43:45]=[0,255,0,100]
        self.assertFalse(evaluate(Image.fromarray(a))[1]['passed'])
        self.assertIsNone(evaluate(sprite())[-1]['passed'])
