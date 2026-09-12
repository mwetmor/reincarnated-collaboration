from oracles.sheet_consistency import measure,identity_vector
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_idle_and_mirrored_outlier(self):
        frames=[np.array(Image.open(p).convert('RGBA')) for p in sorted((FRAME/'idle/S').glob('*.png'))]
        self.assertGreaterEqual(len(frames),3)
        normal=measure(frames);bad=list(frames);bad[0]=bad[0][:,::-1].copy();changed=measure(bad)
        self.assertGreater(changed['value'],normal['value'])
        self.assertEqual(metrics(changed)['farthest_frame_index'],0)
        self.assertIsNone(normal['passed']);assert_envelope(self,normal)
        (ROOT/'tests/sheet_consistency_calibration.json').write_text(json.dumps(dict(idle=normal,mirrored=changed),indent=2)+'\n')
    def test_identical_empty_and_palette_shift(self):
        a=sprite();self.assertAlmostEqual(measure([a,a])['value'],0)
        b=sprite((210,30,40));self.assertGreater(np.linalg.norm(identity_vector(a)-identity_vector(b)),0)
        self.assertIsNone(measure([])['passed'])
        self.assertIsNone(measure([np.zeros((32,32,4),np.uint8)])['passed'])
