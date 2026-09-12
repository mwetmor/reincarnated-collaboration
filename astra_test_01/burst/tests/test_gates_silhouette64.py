from gates.silhouette64 import descriptor,distance,evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_swollen_bag_and_shift_alignment(self):
        self.assertLess(distance(sprite(),sprite(8)),.1)
        self.assertGreater(distance(sprite(),sprite(bag=20)),.1)
        self.assertEqual(len(descriptor(sprite())['hu']),7)
        self.assertFalse(evaluate(sprite(bag=20),sprite(),threshold=.1)['passed'])
        with self.assertRaises(ValueError):descriptor(np.zeros((64,64)))
    def test_real_mirror_vs_idle(self):
        from PIL import ImageOps
        a=Image.open(FIXTURE_ROOT/'idle/S/idle_S_00.png').convert('RGBA')
        b=Image.open(FIXTURE_ROOT/'idle/S/idle_S_01.png').convert('RGBA')
        self.assertGreater(distance(a,ImageOps.mirror(a)),distance(a,b))
