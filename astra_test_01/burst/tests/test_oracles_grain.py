from oracles.grain import band_energy
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_known_frequencies_source_units_and_anchor_distance(self):
        y,x=np.indices((128,128));alpha=np.ones((128,128),bool)
        def field(period):return np.repeat((128+80*np.sin(x*2*np.pi/period))[...,None],3,axis=2).astype('uint8')
        a=field(16);b=field(4)
        reference=band_energy(a,alpha,128);profile=metrics(reference)['profile']
        same=band_energy(a,alpha,128,anchor_profile=profile,threshold=.1)
        wrong=band_energy(b,alpha,128,anchor_profile=profile,threshold=.1)
        self.assertTrue(same['passed']);self.assertFalse(wrong['passed'])
        down=band_energy(a,alpha,128,display_scale=.5)
        edges=np.array(metrics(down)['frequency_edges_cycles_per_source_px'])
        center=(edges[:-1]+edges[1:])/2
        peak=center[np.argmax(metrics(down)['profile'])]
        self.assertLess(abs(peak-1/16),1/32)
        assert_envelope(self,down)
        self.assertIsNone(band_energy(np.full_like(a,80),alpha,128)['passed'])
