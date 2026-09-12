from oracles.palette import adherence
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_known_swatch_shift_and_empty(self):
        a=adherence(sprite(),['#32465a'],5,max_off_pct=2)
        b=adherence(sprite((180,20,40)),['#32465a'],5,max_off_pct=2)
        self.assertEqual(a['value'],0);self.assertEqual(b['value'],100)
        self.assertTrue(a['passed']);self.assertFalse(b['passed']);assert_envelope(self,b)
        self.assertEqual(len(metrics(b)['off_palette_lab_centroids']),1)
        self.assertIsNone(adherence(np.zeros((8,8,4),np.uint8),['#32465a'],5)['passed'])
    def test_frame_shift_margin(self):
        a=np.array(Image.open(FRAME/'idle/S/idle_S_00.png').convert('RGBA'))
        colors=a[...,:3][a[...,3]>=128]
        # Representative palette derived only from original foreground.
        q=Image.fromarray(colors[None]).quantize(colors=32).convert('RGB')
        palette=['#%02x%02x%02x'%tuple(v) for v in np.unique(np.array(q).reshape(-1,3),axis=0)]
        b=a.copy();b[...,:3]=np.clip(b[...,:3].astype(int)+[90,10,-20],0,255)
        original=adherence(a,palette,10,cluster_count=1);shifted=adherence(b,palette,10,cluster_count=1)
        margin=shifted['value']-original['value'];self.assertGreater(margin,20)
        (ROOT/'tests/oracles_palette_measurements.json').write_text(json.dumps({'original_off_pct':original['value'],'shifted_off_pct':shifted['value'],'margin':margin},indent=2)+'\n')
        assert_envelope(self,adherence(a,palette,10,display_scale=.5))
