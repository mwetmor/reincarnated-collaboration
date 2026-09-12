from oracles.motif import count_instances
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_exact_scaled_rotated_peaks_partition_nms(self):
        rng=np.random.default_rng(42);t=rng.integers(0,256,(20,16,3),dtype=np.uint8)
        a=np.full((160,160,3),40,np.uint8);a[20:40,20:36]=t
        rot=np.rot90(t);a[80:96,100:120]=rot
        scaled=np.array(Image.fromarray(t).resize((24,30),Image.Resampling.BICUBIC));a[95:125,30:54]=scaled
        row=count_instances(a,t,[1,1.5],[0,90],.95,[[20,20,36,40]])
        m=metrics(row);self.assertEqual(m['inside'],1);self.assertEqual(m['outside'],2);assert_envelope(self,row)
        repeated=count_instances(a,t,[1,1,1.5],[0,0,90],.95,[[20,20,36,40]])
        self.assertEqual(len(metrics(repeated)['peaks']),3)
        self.assertIsNone(count_instances(a,np.zeros((8,8,3),np.uint8),[1],[0],.65)['passed'])
        assert_envelope(self,count_instances(a,t,[1,1.5],[0,90],.65,display_scale=.5))
    def test_f04_outside_at_least_three(self):
        """SPEC verbatim: O3 on the F04 crop with allowed=[rod_head bbox] → outside ≥ 3."""
        manifest,kw=fixture_params()
        row=count_instances(FIXTURES/'f04_advanced_crop.png',FIXTURES/'sigil_template.png',allowed_masks=[manifest['sigil_template']['bbox_in_advanced_crop']],**kw)
        self.assertGreaterEqual(metrics(row)['outside'],3)
    def test_clean_outside_zero(self):
        """SPEC verbatim: on clean_crop → outside == 0."""
        _,kw=fixture_params();row=count_instances(FIXTURES/'clean_crop.png',FIXTURES/'sigil_template.png',allowed_masks=[],**kw)
        self.assertEqual(metrics(row)['outside'],0)
