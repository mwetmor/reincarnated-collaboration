from oracles.silhouette64 import descriptor,distance,evaluate
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_mirror_distance_exceeds_adjacent_idle(self):
        a=Image.open(FRAME/'idle/S/idle_S_00.png').convert('RGBA')
        b=Image.open(FRAME/'idle/S/idle_S_01.png').convert('RGBA')
        cast=Image.open(FRAME/'cast/S/cast_S_05.png').convert('RGBA')
        mirror=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        neighbor=distance(a,b);mirrored=distance(a,mirror)
        self.assertGreater(mirrored,neighbor)
        self.assertGreater(mirrored-neighbor,.05) # Synthetic/neighbor separation screen, not shipping gate.
        (ROOT/'tests/oracles_silhouette_measurements.json').write_text(json.dumps({'neighbor':neighbor,'mirrored':mirrored,'cast05':distance(a,cast)},indent=2)+'\n')
        self.assertEqual(descriptor(a)['mask'].shape,(64,64));assert_envelope(self,evaluate(a,b,display_scale=.5))
        self.assertIsNone(evaluate(np.zeros((64,64)),np.zeros((64,64)))['passed'])
