from oracles.pse_check import check
from oracles_helpers import *
class Tests(unittest.TestCase):
    def sequence(self,hz,color=(255,255,255),seconds=2,fps=32):
        return [np.full((48,64,3),color if int(i*2*hz/fps)%2 else (0,0,0),np.uint8)
                for i in range(seconds*fps+1)]
    def test_four_hz_white_and_one_hz(self):
        high=check(self.sequence(4),32);low=check(self.sequence(1),32)
        self.assertFalse(high['passed']);self.assertEqual(high['value'],4)
        self.assertTrue(low['passed']);self.assertEqual(low['value'],1)
        self.assertIsNone(metrics(low)['results'][2]['passed'])
    def test_red_and_area_rules(self):
        r=check(self.sequence(4,(255,0,0)),32)
        self.assertFalse(metrics(r)['results'][1]['passed'])
        a=self.sequence(4);a=[np.pad(x[:5,:5],((0,43),(0,59),(0,0))) for x in a]
        self.assertTrue(check(a,32)['passed'])
        self.assertTrue(check(self.sequence(4),32,canvas_size=(1280,720))['passed'])
    def test_threshold_boundary_and_invalid(self):
        self.assertTrue(check(self.sequence(3,fps=48),48)['passed'])
        with self.assertRaises(ValueError):check(self.sequence(1),0)
        self.assertIsNone(check([],24)['passed'])
