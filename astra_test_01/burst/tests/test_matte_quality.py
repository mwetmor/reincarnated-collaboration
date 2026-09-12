from gates.matte_quality import measure
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_spill_halo_and_loss_known_bad(self):
        a=sprite();source=np.zeros_like(a);source[:]=(0,255,0,255)
        source[a[...,3]>0]=a[a[...,3]>0]
        rows=measure(a,source);self.assertEqual(rows[0]['value'],0)
        b=a.copy();b[8:56,8:56,:3]=(20,190,20);b[7,8:56]=(0,200,0,100)
        bad=measure(b,source);self.assertGreater(bad[0]['value'],.9);self.assertGreater(bad[1]['value'],0)
        source[1,1]=(50,202,50,255) # source proxy alpha 103
        rows=measure(a,source);self.assertEqual(rows[2]['value'],1)
        a[1,1]=(50,80,50,103)
        self.assertEqual(measure(a,source)[2]['value'],0)
        for row in rows:assert_envelope(self,row)
    def test_undefined_transparent_rgb_has_no_halo(self):
        a=sprite();a[a[...,3]==0,:3]=(0,255,0)
        self.assertEqual(measure(a,a)[1]['value'],0)
