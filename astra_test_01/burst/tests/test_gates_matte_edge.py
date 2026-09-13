"""T3b synthetic edge-mode and fixed-denominator regression instruments."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from PIL import Image
from scipy import ndimage

from gates.matte import extract, remove_chroma_key
from gates.matte_quality import alpha_area, direct_luminance_fringe, rim_luma_excess
from oracle.video_cut import matte_frames


def soft_disc():
    y, x = np.indices((128, 128))
    alpha = np.clip((38-np.hypot(x-63.5, y-63.5))/3, 0, 1)
    rgb = alpha[..., None]*np.array([50, 50, 90]) + (1-alpha[..., None])*np.array([0, 255, 0])
    return Image.fromarray(rgb.round().astype(np.uint8))


class MatteEdgeTests(unittest.TestCase):
    def test_soft_disc_known_bad(self):
        old = extract(soft_disc())[0]
        new = extract(soft_disc(), edge_mode='clamp')[0]
        self.assertGreater(rim_luma_excess(old)['value'], rim_luma_excess(new)['value'])

    def test_default_equals_explicit_legacy(self):
        default, note = extract(soft_disc())
        explicit, other = extract(soft_disc(), edge_mode='unpremultiply')
        np.testing.assert_array_equal(default, explicit)
        self.assertEqual(note, other)

    def test_alpha_byte_identical_all_options(self):
        for floor in (None, 40, 128):
            for particles in (False, True):
                with self.subTest(floor=floor, particles=particles):
                    a = np.array(extract(soft_disc(), particles, floor)[0])
                    b = np.array(extract(soft_disc(), particles, floor, 'clamp')[0])
                    np.testing.assert_array_equal(a[..., 3], b[..., 3])
                    np.testing.assert_array_equal(a[a[..., 3] == 255], b[b[..., 3] == 255])
                    self.assertTrue(np.all(b[b[..., 3] == 0] == 0))
                    self.assertEqual(alpha_area(a)['value'], alpha_area(b)['value'])

    def test_nearest_opaque_rgb_native_input(self):
        a = np.zeros((64, 64, 4), np.uint8)
        a[20:44, 20:32] = [30, 40, 50, 255]
        a[20:44, 32:44] = [90, 100, 110, 255]
        a[19, 20:44] = [255, 240, 230, 140]
        b = np.array(extract(Image.fromarray(a), edge_mode='clamp')[0])
        partial = (a[..., 3] > 0) & (a[..., 3] < 255)
        indices = ndimage.distance_transform_edt(a[..., 3] != 255, return_distances=False, return_indices=True)
        np.testing.assert_array_equal(b[partial, :3], a[indices[0][partial], indices[1][partial], :3])
        np.testing.assert_array_equal(b[..., 3], a[..., 3])

    def test_no_opaque_donor_is_undefined(self):
        a = np.zeros((64, 64, 4), np.uint8)
        a[20:44, 20:44] = [20, 40, 60, 200]
        with self.assertRaisesRegex(ValueError, 'fully opaque'):
            extract(Image.fromarray(a), edge_mode='clamp')
        self.assertIsNotNone(extract(Image.fromarray(a))[0])

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            extract(soft_disc(), edge_mode='erode')

    def test_alias_forwards(self):
        np.testing.assert_array_equal(remove_chroma_key(soft_disc(), edge_mode='clamp'),
                                      extract(soft_disc(), edge_mode='clamp')[0])

    def test_video_cut_forwards_mode_and_floor(self):
        root = Path(__file__).resolve().parent/'tmp'
        root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as tmp:
            path = Path(tmp)/'disc.png'
            soft_disc().save(path)
            with patch('oracle.video_cut.extract', wraps=extract) as wrapped:
                frames = matte_frames([path], alpha_floor=70, edge_mode='clamp')
                self.assertEqual(wrapped.call_args.kwargs, dict(alpha_floor=70, edge_mode='clamp'))
            self.assertEqual(frames.notes[0]['edge_mode_applied'], 'clamp')
            self.assertNotIn('edge_mode_note', frames.notes[0])


class MatteQualityEdgeTests(unittest.TestCase):
    def fixture(self):
        a = np.zeros((32, 32, 4), np.uint8)
        a[7:25, 7:25] = [200, 200, 200, 128]
        a[8:24, 8:24] = [100, 100, 100, 255]
        return a

    def test_rim_exact_ring_and_background(self):
        a = self.fixture()
        r = rim_luma_excess(a, bg=(60, 60, 60))
        self.assertAlmostEqual(r['value'], 200*128/255+60*127/255-100)
        self.assertEqual(r['metrics']['partial_band_pixels'], 18**2-16**2)
        self.assertEqual(r['metrics']['opaque_ring_pixels'], 16**2-10**2)
        self.assertIsNone(r['passed'])

    def test_known_bad_bright_rim(self):
        self.assertGreater(rim_luma_excess(self.fixture())['value'], 5)

    def test_alpha_area_is_integrated_mass(self):
        a = self.fixture()
        self.assertAlmostEqual(alpha_area(a)['value'], 256+68*128/255)
        self.assertEqual(alpha_area(np.zeros_like(a))['value'], 0)

    def test_pretrim_denominator_survives_partial_and_total_erosion(self):
        a = self.fixture()
        trimmed = a.copy()
        trimmed[7] = 0
        before = direct_luminance_fringe(a, a, bg=(0, 0, 0))
        after = direct_luminance_fringe(trimmed, a, bg=(0, 0, 0))
        self.assertEqual(before['metrics']['pre_trim_band_pixels'], 68)
        self.assertEqual(after['metrics']['pre_trim_band_pixels'], 68)
        self.assertAlmostEqual(after['value'], before['value']*50/68)
        trimmed[a[..., 3] < 255] = 0
        all_removed = direct_luminance_fringe(trimmed, a, bg=(0, 0, 0))
        self.assertEqual(all_removed['value'], 0)
        self.assertEqual(all_removed['metrics']['pre_trim_band_pixels'], 68)
        self.assertIn('R-52', all_removed['notes'])

    def test_reference_donors_stay_frozen(self):
        a = self.fixture()
        changed = a.copy()
        changed[a[..., 3] == 255, :3] = 255
        self.assertEqual(direct_luminance_fringe(a, a)['value'],
                         direct_luminance_fringe(changed, a)['value'])

    def test_empty_band_and_missing_opaque_are_unevaluable(self):
        for a in (np.zeros((32, 32, 4), np.uint8), np.full((32, 32, 4), 255, np.uint8),
                  np.full((32, 32, 4), 128, np.uint8)):
            with self.subTest(alpha=int(a[0, 0, 3])):
                for metric in (rim_luma_excess, direct_luminance_fringe):
                    r = metric(a)
                    self.assertIsNone(r['value'])
                    self.assertIsNone(r['passed'])
                    self.assertIn('UNEVALUABLE', r['notes'])

    def test_transparent_rgb_never_affects_metrics(self):
        a = self.fixture()
        b = a.copy()
        b[b[..., 3] == 0, :3] = 255
        self.assertEqual(rim_luma_excess(a)['value'], rim_luma_excess(b)['value'])
        self.assertEqual(direct_luminance_fringe(a, a)['value'], direct_luminance_fringe(b, a)['value'])

    def test_invalid_reference_and_background(self):
        with self.assertRaises(ValueError):
            direct_luminance_fringe(self.fixture(), np.zeros((4, 4, 4), np.uint8))
        for bg in ((1, 2), (1, 2, float('nan')), (1, 2, 256)):
            with self.assertRaises(ValueError):
                rim_luma_excess(self.fixture(), bg=bg)


if __name__ == '__main__':
    unittest.main()
