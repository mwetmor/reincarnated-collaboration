"""T4e synthetic contracts; all temporary assets remain inside this burst."""
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image
from scipy import ndimage

from oracle.peak_pieces import (build, decompose, isolate, plane_quality, quantise,
                                _pivot, _connected_merge, CONNECTIVITY)


TEMP_ROOT = Path(__file__).resolve().parents[1]/'runs/C-5/t3/T4e-r1/tmp'


class PeakPiecesTests(unittest.TestCase):
    def setUp(self):
        TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def save(self, rgba, name='source.png'):
        path = self.root/name
        Image.fromarray(rgba).save(path)
        return path

    def check_partition(self, pieces, bands, alpha):
        union = np.zeros(alpha.shape, dtype=int)
        for piece in pieces:
            mask = piece['mask']
            union += mask
            x, y = np.floor(np.array(piece['pivot'])+.5).astype(int)
            self.assertTrue(mask[y, x])
            self.assertEqual(ndimage.label(mask, CONNECTIVITY)[1], 1)
            self.assertEqual(piece['connected_components'], 1)
            self.assertEqual(piece['area_px'], int(mask.sum()))
            self.assertEqual(piece['band_histogram'],
                             {str(i): int(((bands == i) & mask).sum()) for i in range(4)})
        np.testing.assert_array_equal(union, (alpha > 0).astype(int))

    def five_tongues(self):
        y, x = np.indices((256, 256))
        angle = np.arctan2(y-128, x-128)
        radius = np.hypot(x-128, y-128)
        bound = np.full(radius.shape, 45.)
        for i, amplitude in enumerate([40, 35, 45, 30, 38]):
            delta = np.angle(np.exp(1j*(angle-i*2*np.pi/5)))
            bound += amplitude*np.exp(-.5*(delta/.16)**2)
        mask = radius <= bound
        bands = np.where(ndimage.distance_transform_edt(mask) > 5, 2, 0).astype(np.uint8)
        return bands, (mask*255).astype(np.uint8)

    def test_five_unequal_two_band_tongues(self):
        bands, alpha = self.five_tongues()
        pieces = decompose(bands, alpha)
        self.assertGreaterEqual(len(pieces), 8)
        self.assertLessEqual(len(pieces), 15)
        self.assertLessEqual(max(p['area_px'] for p in pieces), .25*np.count_nonzero(alpha))
        self.assertEqual(len(pieces[0]['geometry']['tips']), 5)
        self.assertTrue(all(sum(n > 0 for n in p['band_histogram'].values()) >= 2 for p in pieces))
        self.check_partition(pieces, bands, alpha)
        # Colour permutations must not move the spatial cuts.
        recoloured = decompose((3-bands).astype(np.uint8), alpha)
        for a, b in zip(pieces, recoloured):
            np.testing.assert_array_equal(a['mask'], b['mask'])

    def test_crescent_pivot_snaps_to_nearest_covered_pixel(self):
        y, x = np.indices((80, 80))
        mask = ((x-40)**2+(y-40)**2 <= 28**2) & ((x-51)**2+(y-40)**2 > 27**2)
        alpha = (mask*255).astype(np.uint8)
        pivot, centroid, adjusted = _pivot(mask, alpha)
        self.assertTrue(adjusted)
        cx, cy = centroid
        self.assertFalse(mask[int(np.floor(cy+.5)), int(np.floor(cx+.5))])
        yy, xx = np.where(mask)
        nearest = np.argmin((xx-cx)**2+(yy-cy)**2)
        self.assertEqual(pivot, [int(xx[nearest]), int(yy[nearest])])
        self.check_partition(decompose(np.zeros(mask.shape, dtype=np.uint8), alpha),
                             np.zeros(mask.shape, dtype=np.uint8), alpha)

    def test_long_tongue_split_at_waist(self):
        # A broad distal head beyond a narrow shaft: interior waist, not tip taper.
        y, x = np.indices((180, 300))
        core = (x-65)**2+(y-90)**2 <= 42**2
        shaft = (x >= 65) & (x <= 230) & (abs(y-90) <= (8+np.minimum(18, ((x-170)/10)**2)))
        head = ((x-237)/34)**2+((y-90)/24)**2 <= 1
        mask = core | shaft | head
        alpha = (mask*255).astype(np.uint8)
        bands = np.where(ndimage.distance_transform_edt(mask) > 4, 2, 0).astype(np.uint8)
        pieces = decompose(bands, alpha)
        bases = [p for p in pieces if p['kind'] == 'tongue_base']
        self.assertTrue(bases)
        base = max(bases, key=lambda p: p['contour_tip'][0])
        tip = next(p for p in pieces if p['kind'] == 'tongue_tip' and p['tongue_id'] == base['tongue_id'])
        self.assertGreater(base['tongue_length_px'], 1.5*base['geometry']['core_radius_px'])
        # Known narrowest shaft section is x=170, allowing integer width plateau.
        self.assertAlmostEqual(base['waist']['projection_px'], 170, delta=12)
        self.assertGreater(tip['pivot'][0], base['pivot'][0])
        self.check_partition(pieces, bands, alpha)

    def test_green_key_one_pixel_fringe_and_opaque_black(self):
        rgba = np.full((32, 32, 4), [0, 255, 0, 255], dtype=np.uint8)
        rgba[8:24, 8:24] = [85, 85, 85, 255]
        rgba[12:20, 12:20] = [0, 0, 0, 255]
        rgba[7, 8:24] = [43, 170, 43, 255]
        rgba[6, 8:24] = [43, 170, 43, 255]
        image = isolate(self.save(rgba))
        a = np.asarray(image)
        self.assertEqual(image.info['isolation']['plate_path_used'], 'green')
        self.assertEqual(image.info['isolation']['fringe_width_px'], 1)
        self.assertEqual(image.info['isolation']['removed_fringe_pixels'], 16)
        self.assertTrue(np.all(a[7, 8:24, 3] == 128))
        self.assertTrue(np.all(a[7, 8:24, :3] == 85))
        self.assertTrue(np.all(a[6, :, 3] == 0))
        self.assertTrue(np.all(a[12:20, 12:20, 3] == 255))
        self.assertEqual(np.count_nonzero(a[..., 3]), 16*16+16)
        bands, alpha, _ = quantise(a)
        self.check_partition(decompose(bands, alpha), bands, alpha)

    def test_sliver_merges_across_longest_shared_border(self):
        labels = np.zeros((24, 32), dtype=np.int32)
        labels[3:21, 3:29] = 1
        labels[3:21, 20:29] = 2
        labels[10:12, 18:20] = 3
        descriptions = {i: {'kind': 'test'} for i in (1, 2, 3)}
        result, info = _connected_merge(labels, descriptions)
        # Sliver has six edge contacts with label 1, two with label 2.
        self.assertTrue(np.all(result[10:12, 18:20] == result[8, 8]))
        self.assertEqual(len(info), 2)
        self.assertTrue(any(p['merged_slivers'] for p in info.values()))
        np.testing.assert_array_equal(result > 0, labels > 0)

    def test_disconnected_source_island_is_reported_never_bridged(self):
        alpha = np.zeros((40, 50), dtype=np.uint8)
        alpha[10:20, 4:14] = 255
        alpha[8:22, 24:36] = 255
        alpha[14, 18:20] = 51
        bands = np.ones(alpha.shape, dtype=np.uint8)
        pieces = decompose(bands, alpha)
        detached = next(p for p in pieces if p['area_px'] == 2)
        self.assertIn('no shared border', detached['unmergeable_sliver'])
        self.check_partition(pieces, bands, alpha)

    def test_multicomponent_label_is_split_before_merging(self):
        labels = np.zeros((40, 60), dtype=np.int32)
        labels[2:12, 2:12] = labels[20:30, 20:30] = 1
        result, info = _connected_merge(labels, {1: {'kind': 'test'}})
        self.assertEqual(len(info), 2)
        for label in info:
            self.assertEqual(ndimage.label(result == label, CONNECTIVITY)[1], 1)

    def test_quantise_nearest_and_quality_without_alpha_changes(self):
        rgba = np.array([[[0, 0, 0, 255], [86, 86, 86, 1], [130, 130, 130, 254], [240, 240, 240, 255]]], dtype=np.uint8)
        bands, alpha, hist = quantise(rgba)
        np.testing.assert_array_equal(bands, [[0, 1, 2, 3]])
        np.testing.assert_array_equal(alpha, rgba[..., 3])
        self.assertEqual(list(hist.values()), [1, 1, 1, 1])
        self.assertEqual(plane_quality(rgba)['farther_than_20_fraction'], .25)

    def test_build_roundtrip_full_canvas_and_deterministic_files(self):
        rgba = np.zeros((32, 32, 4), dtype=np.uint8)
        rgba[4:28, 4:16] = [0, 0, 0, 255]
        rgba[4:28, 16:28] = [170, 170, 170, 93]
        source = self.save(rgba)
        one = build(source, self.root/'one', centre=[3, 5])
        two = build(source, self.root/'two', centre=[3, 5])
        self.assertEqual(one, two)
        union_alpha = np.zeros((32, 32), dtype=np.uint16)
        for p in one['pieces']:
            with Image.open(self.root/'one'/p['mask']) as im:
                self.assertEqual(im.size, (32, 32))
                a = np.array(im)
            union_alpha += a[..., 3]
            bands, _, _ = quantise(rgba)
            mask = a[..., 3] > 0
            np.testing.assert_array_equal(a[mask, :3], np.repeat((bands[mask]*85)[:, None], 3, axis=1))
            self.assertEqual(p['band_histogram'], {str(i): int(((bands == i) & mask).sum()) for i in range(4)})
        np.testing.assert_array_equal(union_alpha, rgba[..., 3])
        for file in (self.root/'one').iterdir():
            self.assertEqual(file.read_bytes(), (self.root/'two'/file.name).read_bytes())

    def test_invalid_inputs(self):
        opaque = np.full((16, 16, 4), 255, dtype=np.uint8)
        path = self.save(opaque)
        with self.assertRaisesRegex(ValueError, 'no flat pure green'):
            isolate(path)
        self.assertEqual(isolate(path, 'alpha').info['isolation']['plate_path_used'], 'alpha')
        with self.assertRaises(ValueError):
            decompose(np.full((4, 4), 4, dtype=np.uint8), np.full((4, 4), 255, dtype=np.uint8))
        with self.assertRaises(ValueError):
            decompose(np.zeros((4, 4), dtype=np.uint8), np.zeros((4, 4), dtype=np.uint8))
        with self.assertRaises(ValueError):
            build(path, self.root/'bad', centre=[float('nan'), 0], plate='alpha')
        self.assertFalse((self.root/'bad').exists())


if __name__ == '__main__':
    unittest.main()
