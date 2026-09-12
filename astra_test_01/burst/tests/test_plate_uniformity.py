from gates.plate_uniformity import measure
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_per_channel_fraction_and_threshold(self):
        a=np.full((16,16,3),(0,255,0),np.uint8);alpha=np.zeros((16,16),np.uint8)
        a[4:12,4:12]=(100,80,50);alpha[4:12,4:12]=255
        r=measure(a,alpha);self.assertEqual(r['value'],1);self.assertIsNone(r['passed'])
        self.assertTrue(measure(a,alpha,min_fraction=.99)['passed'])
        a[0]=(9,255,0)
        self.assertFalse(measure(a,alpha,min_fraction=.99)['passed'])
        self.assertAlmostEqual(measure(a,alpha)['value'],176/192)
        self.assertEqual(len(metrics(r)['plate_sd_rgb']),3)
    def test_empty_background(self):
        self.assertIsNone(measure(sprite(),np.full((64,64),255))['passed'])
