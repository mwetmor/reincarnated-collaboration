from oracles.motif import count_instances,count_family,FAMILY_PARAMETERS
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
        row=count_family(FIXTURES/'f04_advanced_crop.png',allowed_masks=[manifest['sigil_template']['bbox_in_advanced_crop']],**FAMILY_PARAMETERS)
        self.assertGreaterEqual(metrics(row)['outside'],3)
    def test_clean_outside_zero(self):
        """SPEC verbatim: on clean_crop → outside == 0."""
        _,kw=fixture_params();row=count_instances(FIXTURES/'clean_crop.png',FIXTURES/'sigil_template.png',allowed_masks=[],**kw)
        self.assertEqual(metrics(row)['outside'],0)

    def test_family_clean_outside_zero(self):
        """SPEC verbatim: on clean_crop → outside == 0."""
        self.assertEqual(metrics(count_family(FIXTURES/'clean_crop.png',**FAMILY_PARAMETERS))['outside'],0)

    def test_synthetic_family_rings_and_negatives(self):
        from motif_calibration import rings,no_rings,half_arcs,RINGS
        for textured in (False,True):
            row=count_family(rings(textured),allowed_masks=[[20,20,60,70]],**FAMILY_PARAMETERS)
            m=metrics(row);self.assertEqual((m['inside'],m['outside']),(1,2));assert_envelope(self,row)
            for x,y,r in RINGS:
                peak=min(m['peaks'],key=lambda p:np.linalg.norm(np.subtract(p['center'],[x,y])))
                self.assertLessEqual(np.linalg.norm(np.subtract(peak['center'],[x,y])),2)
                self.assertLessEqual(abs(peak['radius']-r),2)
        for a in (no_rings(),half_arcs()):
            self.assertEqual(metrics(count_family(a,**FAMILY_PARAMETERS))['outside'],0)

    def test_family_masks_and_invalid_parameters(self):
        from motif_calibration import rings
        a=rings();mask=np.zeros(a.shape[:2],bool);mask[20:70,20:60]=True
        self.assertEqual(metrics(count_family(a,allowed_masks=[mask]))['inside'],1)
        for kw in ({'family':'unknown'},{'min_radius_px':0},{'vote_thresh':0},{'display_scale':2},
                   {'hollow_min':-.1},{'hollow_min':1.1},{'hollow_min':float('nan')}):
            with self.assertRaises(ValueError):count_family(a,**kw)

    def test_filled_discs_rejected_and_auditable(self):
        from motif_calibration import filled_discs,RINGS
        for textured in (False,True):
            with self.subTest(textured=textured):
                row=count_family(filled_discs(textured),allowed_masks=[[20,20,60,70]],**FAMILY_PARAMETERS)
                m=metrics(row);assert_envelope(self,row)
                self.assertEqual((m['inside'],m['outside']),(0,0))
                self.assertEqual(m['annulus_rejected'],3)
                self.assertEqual(len(m['peaks']),3)
                self.assertEqual(sum(p['inside'] for p in m['peaks']),1)
                for x,y,r in RINGS:
                    peak=min(m['peaks'],key=lambda p:np.linalg.norm(np.subtract(p['center'],[x,y])))
                    self.assertLessEqual(np.linalg.norm(np.subtract(peak['center'],[x,y])),2)
                    self.assertLessEqual(abs(peak['radius']-r),2)
                    self.assertEqual(peak['rejected'],'not_annulus')
                    self.assertLess(peak['hollow_score'],m['hollow_min'])
                    for k in ('inner_opposed_support','lab_color_return'):
                        self.assertGreaterEqual(peak[k],0);self.assertLessEqual(peak[k],1)

    def test_annulus_threshold_from_synthetic_observations(self):
        from motif_calibration import rings,filled_discs
        positive=[];negative=[]
        for textured in (False,True):
            positive.extend(p['hollow_score'] for p in metrics(count_family(rings(textured)))['peaks'])
            negative.extend(p['hollow_score'] for p in metrics(count_family(filled_discs(textured)))['peaks'])
        self.assertLess(max(negative),min(positive))
        self.assertEqual(FAMILY_PARAMETERS['hollow_min'],(max(negative)+min(positive))/2)

    def test_named_genuine_annuli_retained(self):
        manifest,_=fixture_params()
        m=metrics(count_family(FIXTURES/'f04_advanced_crop.png',
            allowed_masks=[manifest['sigil_template']['bbox_in_advanced_crop']],**FAMILY_PARAMETERS))
        for center in ([152,173],[113,201],[111,311],[170,253],[212,393]):
            with self.subTest(center=center):
                peak=next(p for p in m['peaks'] if p['center']==center)
                self.assertNotIn('rejected',peak)
