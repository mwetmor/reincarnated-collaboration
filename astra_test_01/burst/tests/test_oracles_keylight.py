from oracles.keylight import azimuth
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_shaded_planes_and_flat(self):
        y,x=np.indices((64,64));lum=250-x-y
        a=np.repeat(lum[...,None],3,axis=2).astype('uint8');alpha=np.ones((64,64),bool)
        good=azimuth(a,alpha,tolerance=3);bad=azimuth(255-a,alpha,tolerance=3,display_scale=.5)
        self.assertAlmostEqual(metrics(good)['azimuth_deg'],135,places=4)
        self.assertTrue(good['passed']);self.assertFalse(bad['passed']);assert_envelope(self,bad)
        self.assertIsNone(azimuth(np.full_like(a,50),alpha,tolerance=3)['passed'])
