"""Exact T4d classifier, denominator, spatial attribution and case contracts."""
import unittest
import numpy as np
from oracle.white_gate import baseline, crop_bounds, measure, measure_cases, white_mask


class WhiteGateTests(unittest.TestCase):
    def setUp(self):
        self.plate = np.zeros((540, 960, 3), np.uint8)
        self.centre = (480, 270)

    def test_known_four_percent_peak_and_clip_mean(self):
        peak = self.plate.copy()
        peak.reshape(-1, 3)[:20736] = 255
        result = measure(self.plate, [self.plate, peak, self.plate], self.centre)
        self.assertEqual(result['peak']['frame'], 1)
        self.assertAlmostEqual(result['peak']['attributable']['percent'], 4.0, delta=.2)
        self.assertAlmostEqual(result['mean']['attributable']['percent'], 4/3)
        self.assertEqual(result['crop_origin_xy'], [0,0])
        self.assertEqual(result['denominator_px'], 518400)
        self.assertTrue(all(r['passed'] is None for r in result['results']))

    def test_spatial_difference_does_not_cancel_displaced_white(self):
        self.plate[:10] = 255
        effect = np.zeros_like(self.plate); effect[10:20] = 255
        r = measure(self.plate, [effect], self.centre)['peak']
        self.assertEqual(r['total']['pixels'], 9600)
        self.assertEqual(r['baseline']['pixels'], 9600)
        self.assertEqual(r['attributable']['pixels'], 9600)
        self.assertEqual(r['removed_baseline']['pixels'], 9600)

    def test_total_at_attributable_peak_and_first_tie(self):
        self.plate[:100] = 255
        a = self.plate.copy(); a[101] = 255
        b = np.zeros_like(a); b[102:105] = 255
        r = measure(self.plate, [a,b,b], self.centre)
        self.assertEqual(r['peak']['frame'], 1)
        self.assertEqual(r['peak']['total']['pixels'], 2880)
        self.assertEqual(r['peak']['baseline']['pixels'], 96000)

    def test_strict_white_thresholds(self):
        pixels = np.array([[[242,242,242], [243,243,243], [255,204,204],
                            [255,205,205], [255,203,203], [255,0,0], [0,0,0]]],np.uint8)
        self.assertEqual(white_mask(pixels).tolist(), [[False,True,False,True,False,False,False]])

    def test_baseline_empty_crop(self):
        self.plate[:10] = 255
        r = baseline(self.plate, self.centre)
        self.assertEqual(r['peak']['attributable']['percent'], 0)
        self.assertEqual(r['peak']['baseline']['pixels'], 9600)

    def test_crop_native_centre_no_padding(self):
        self.assertEqual(crop_bounds((1000.2,800.8), (2000,1500)),[520,531,1480,1071])
        for point in [(0,0), (479,270), (480,269), (float('nan'),270)]:
            with self.subTest(point=point), self.assertRaises(ValueError):
                crop_bounds(point, (960,540))

    def test_flash_on_off_and_four_cast_cases_are_separate(self):
        cases = {name: dict(plate=self.plate,frames=[self.plate],impact_xy=self.centre,
                           flash=flash,cast_pattern=pattern,cast_count=count)
                 for name,flash,pattern,count in [('on',True,'single',1),('off',False,'single',1),
                                                  ('four_sync',True,'synchronised',4),('four_stagger',False,'staggered',4)]}
        r = measure_cases(cases)
        self.assertEqual(set(r),set(cases))
        self.assertEqual(r['four_sync']['cast_count'],4)
        self.assertFalse(r['four_stagger']['flash'])

    def test_known_bad_empty_misaligned_transparent_and_nonbyte(self):
        for frames in [[],[np.zeros((539,960,3),np.uint8)],
                       [np.zeros((540,960,4),np.uint8)], [np.zeros((540,960,3),float)]]:
            with self.assertRaises(ValueError): measure(self.plate,frames,self.centre)
        with self.assertRaises(ValueError): measure_cases({})


if __name__ == '__main__': unittest.main()
