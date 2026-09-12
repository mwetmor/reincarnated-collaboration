from oracles.plain_budget import plain_fraction
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_plain_vs_stripes_mask_empty(self):
        a=sprite();b=a.copy();b[:,::4,:3]=255;b[:,1::4,:3]=0
        mask=np.zeros((64,64),bool);mask[12:52,12:52]=True
        good=plain_fraction(a,a[...,3],mask,.02,min_plain=.9)
        bad=plain_fraction(b,b[...,3],mask,.02,min_plain=.9)
        self.assertTrue(good['passed']);self.assertFalse(bad['passed']);assert_envelope(self,bad)
        self.assertIsNone(plain_fraction(a,np.zeros((64,64)),edge_thresh=.02)['passed'])
        assert_envelope(self,plain_fraction(a,a[...,3],edge_thresh=.02,display_scale=.5))
