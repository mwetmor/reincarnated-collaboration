"""Synthetic calibration and defect controls for the 512-canvas G12 tool."""
import json
import unittest

import numpy as np
from PIL import Image

from gates.mask_composite import composite, compose_loop, evaluate


def idle_sprite():
    base = np.zeros((512, 512, 4), dtype=np.uint8)
    # Hidden RGB tests byte preservation as well as visible appearance.
    base[..., :3] = (11, 17, 23)
    base[160:200, 236:276] = (200, 210, 220, 255)
    base[200:340, 226:286] = (40, 70, 110, 255)
    base[340:400, 226:246] = (30, 40, 50, 255)
    base[340:400, 266:286] = (30, 40, 50, 255)
    base[220:250, 286:306] = (120, 140, 160, 255)
    return base


class Tests(unittest.TestCase):
    def test_everywhere_variant_is_unevaluable(self):
        base = idle_sprite()
        variant = np.full_like(base, 255)
        out, mask, metrics = composite(base, variant, (0, 0, 512, 512))
        self.assertTrue(mask.all())
        self.assertEqual(metrics['mask_area_fraction'], 1.0)
        self.assertEqual(metrics['mask_figure_fraction'], 1.0)
        self.assertIsNone(evaluate(base, out, mask)['passed'])
        self.assertIsNone(metrics['base_preserved_fraction'])

    def test_shifted_variant_is_caught_by_region(self):
        base = idle_sprite()
        variant = np.roll(base, 12, axis=1)
        box = (280, 210, 325, 260)
        out, mask, metrics = composite(base, variant, box)
        actual = np.array(out)
        allowed = np.zeros((512, 512), bool)
        allowed[210:260, 280:325] = True
        self.assertGreater(metrics['dropped_out_of_box_pixels'], 0)
        self.assertTrue(mask.any())
        self.assertFalse(mask[~allowed].any())
        np.testing.assert_array_equal(actual[~allowed], base[~allowed])
        np.testing.assert_array_equal(actual[mask], variant[mask])
        self.assertGreater(metrics['changed_inside_pixels'], 0)

    def test_identical_variant_has_empty_mask(self):
        base = idle_sprite()
        out, mask, metrics = composite(base, base.copy(), (0, 0, 512, 512))
        self.assertFalse(mask.any())
        self.assertEqual(metrics['base_preserved_fraction'], 1.0)
        self.assertEqual(metrics['changed_inside_fraction'], 0.0)
        self.assertEqual(metrics['dropped_out_of_box_pixels'], 0)
        np.testing.assert_array_equal(out, base)
        self.assertTrue(evaluate(base, out, mask)['passed'])

    def test_planted_out_of_box_change_dropped_and_reported(self):
        base = idle_sprite()
        variant = base.copy()
        variant[230:235, 290:295, :3] = 250
        variant[170:180, 240:250, :3] = 0
        out, mask, metrics = composite(base, variant, (280, 210, 330, 270), dilate_px=2)
        self.assertEqual(metrics['dropped_out_of_box_pixels'], 100)
        self.assertEqual(metrics['out_of_box_changed_pixels'], 100)
        np.testing.assert_array_equal(np.array(out)[170:180, 240:250], base[170:180, 240:250])
        self.assertEqual(metrics['outside_mask_changed_pixels'], 0)
        self.assertTrue(metrics['outside_mask_byte_identical'])

    def test_synthetic_idle_arm_moves_with_base_preserved(self):
        base = idle_sprite()
        original = base.copy()
        variant = base.copy()
        variant[220:250, 286:306] = (11, 17, 23, 0)
        variant[230:260, 296:316] = (120, 140, 160, 255)
        saved_variant = variant.copy()
        out, mask, metrics = composite(Image.fromarray(base), variant, (280, 210, 330, 270))
        actual = np.array(out)
        np.testing.assert_array_equal(actual[~mask], base[~mask])
        np.testing.assert_array_equal(actual[mask], variant[mask])
        self.assertEqual(int(actual[225, 290, 3]), 0)
        self.assertEqual(int(actual[255, 310, 3]), 255)
        self.assertEqual(metrics['base_preserved_fraction'], 1.0)
        self.assertGreater(metrics['changed_inside_fraction'], 0)
        gate = evaluate(base, out, mask, 'idle/S/01')
        self.assertGreaterEqual(gate['value'], 0.99)
        self.assertTrue(gate['passed'])
        self.assertEqual(gate['subject'], 'idle/S/01')
        self.assertEqual(gate['threshold'], 0.99)
        self.assertEqual(gate['op'], '>=')
        self.assertEqual(set(gate), {'id', 'subject', 'passed', 'value', 'threshold',
                                    'op', 'unit', 'evidence', 'notes'})
        json.dumps(gate, allow_nan=False)
        json.dumps(metrics, allow_nan=False)
        np.testing.assert_array_equal(base, original)
        np.testing.assert_array_equal(variant, saved_variant)

    def test_alpha_aware_hidden_rgb_and_black_alpha_changes(self):
        base = idle_sprite()
        variant = base.copy()
        variant[10:20, 10:20, :3] = 255
        out, mask, _ = composite(base, variant, (0, 0, 512, 512), thresh=0, dilate_px=0)
        self.assertFalse(mask.any())
        np.testing.assert_array_equal(out, base)
        base[20, 20] = (0, 0, 0, 255)
        variant = base.copy()
        variant[20, 20, 3] = 0
        variant[21, 21] = (0, 0, 0, 128)
        out, mask, _ = composite(base, variant, (0, 0, 512, 512), dilate_px=0)
        self.assertTrue(mask[20, 20])
        self.assertTrue(mask[21, 21])
        self.assertEqual(int(np.array(out)[20, 20, 3]), 0)

    def test_premultiplied_threshold_and_strict_boundary(self):
        base = idle_sprite()
        base[20, 20] = (0, 0, 0, 128)
        base[20, 21] = (0, 0, 0, 255)
        variant = base.copy()
        variant[20, 20, 0] = 15  # 7.53 premultiplied units, below 8.
        variant[20, 21, 0] = 8  # Exactly 8 is not selected.
        _, mask, _ = composite(base, variant, (0, 0, 512, 512), thresh=8, dilate_px=0)
        self.assertFalse(mask.any())
        variant[20, 20, 0] = 16
        variant[20, 21, 0] = 9
        _, mask, _ = composite(base, variant, (0, 0, 512, 512), thresh=8, dilate_px=0)
        self.assertEqual(int(mask.sum()), 2)

    def test_dilation_and_xyxy_exclusive_clipping(self):
        base = idle_sprite()
        variant = base.copy()
        variant[10, 10] = (255, 255, 255, 255)
        for radius, expected in ((0, 1), (1, 4), (2, 9)):
            with self.subTest(radius=radius):
                _, mask, _ = composite(base, variant, (10, 10, 13, 13), dilate_px=radius)
                self.assertEqual(int(mask.sum()), expected)
                self.assertFalse(mask[9].any())
                self.assertFalse(mask[13].any())
                self.assertFalse(mask[:, 13].any())
        # An outside seed is dilated first, but the seed itself is never pasted.
        variant = base.copy()
        variant[11, 9] = (255, 255, 255, 255)
        out, mask, metrics = composite(base, variant, (10, 10, 13, 13), dilate_px=1)
        self.assertEqual(int(mask.sum()), 3)
        self.assertEqual(metrics['dropped_out_of_box_pixels'], 1)
        np.testing.assert_array_equal(out, base)

    def test_g12_detects_outside_corruption_including_hidden_bytes(self):
        base = idle_sprite()
        mask = np.zeros((512, 512), bool)
        out = base.copy()
        out.reshape(-1, 4)[:2621, 0] ^= 1
        self.assertTrue(evaluate(base, out, mask)['passed'])
        out.reshape(-1, 4)[2621, 0] ^= 1
        gate = evaluate(base, out, mask)
        self.assertFalse(gate['passed'])
        self.assertAlmostEqual(gate['value'], 1 - 2622 / (512 * 512))
        self.assertFalse(json.loads(gate['notes'])['outside_mask_byte_identical'])

    def test_preservation_uses_outside_denominator(self):
        base = idle_sprite()
        mask = base[..., 3] < 128
        out = base.copy()
        coords = np.argwhere(~mask)[:131]
        out[coords[:, 0], coords[:, 1], 0] ^= 1
        gate = evaluate(base, out, mask)
        self.assertAlmostEqual(gate['value'], 1 - 131 / 13000)
        self.assertFalse(gate['passed'])

    def test_coverage_guard_uses_figure_not_canvas_and_strict_limit(self):
        base = np.zeros((512, 512, 4), np.uint8)
        base[100:110, 100:110] = (30, 40, 50, 128)
        base[10:20, 10:20] = (30, 40, 50, 127)  # Not figure support.
        mask = np.zeros((512, 512), bool)
        mask[100:106, 100:110] = True
        self.assertTrue(evaluate(base, base, mask)['passed'])
        mask[106, 100] = True
        gate = evaluate(base, base, mask)
        self.assertIsNone(gate['passed'])
        self.assertEqual(gate['value'], 1.0)
        self.assertEqual(json.loads(gate['notes'])['mask_figure_fraction'], 0.61)
        self.assertTrue(evaluate(base, base, mask, max_mask_figure_fraction=0.61)['passed'])

    def test_empty_figure_and_full_mask_are_unevaluable(self):
        base = np.zeros((512, 512, 4), np.uint8)
        for mask in (np.zeros((512, 512), bool), np.ones((512, 512), bool)):
            gate = evaluate(base, base, mask)
            self.assertIsNone(gate['passed'])
            self.assertIn('UNEVALUABLE', gate['notes'])
            json.dumps(gate, allow_nan=False)
        base = idle_sprite()
        gate = evaluate(base, base, np.ones((512, 512), bool), max_mask_figure_fraction=1)
        self.assertIsNone(gate['passed'])
        self.assertIn('no outside-mask pixels', gate['notes'])

    def test_loop_uses_same_base_and_one_box_per_variant(self):
        base = idle_sprite()
        variant = base.copy()
        variant[220:225, 290:295, :3] = 255
        boxes = [(280, 210, 330, 270)] * 2
        frames = compose_loop(base, [variant, base.copy()], boxes, thresh=0, dilate_px=0)
        self.assertEqual(len(frames), 2)
        self.assertFalse(np.array_equal(frames[0][0], base))
        np.testing.assert_array_equal(frames[1][0], base)
        self.assertFalse(frames[1][1].any())
        self.assertEqual(compose_loop(base, [], []), [])
        with self.assertRaises(ValueError):
            compose_loop(base, [variant], [])

    def test_invalid_inputs_are_rejected(self):
        base = idle_sprite()
        for box in ((0, 0, 513, 512), (-1, 0, 5, 5), (2, 0, 1, 5),
                    (0, 0, 0, 5), (0.5, 0, 5, 5), (True, 0, 5, 5), (0, 0, 5), None):
            with self.subTest(box=box), self.assertRaises(ValueError):
                composite(base, base, box)
        for thresh in (-1, 256, float('nan'), float('inf'), True, '8'):
            with self.subTest(thresh=thresh), self.assertRaises(ValueError):
                composite(base, base, (0, 0, 512, 512), thresh=thresh)
        for radius in (-1, 0.5, True):
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                composite(base, base, (0, 0, 512, 512), dilate_px=radius)
        for bad in (base[:128, :128], base.astype(float), base[..., :3],
                    Image.new('RGBA', (627, 627))):
            with self.assertRaises(ValueError):
                composite(base, bad, (0, 0, 512, 512))
        for bad in (np.zeros((512, 512), np.uint8), np.zeros((128, 128), bool)):
            with self.assertRaises(ValueError):
                evaluate(base, base, bad)
        for kwargs in ({'min_preserved_fraction': -0.1}, {'max_mask_figure_fraction': 1.1}):
            with self.assertRaises(ValueError):
                evaluate(base, base, np.zeros((512, 512), bool), **kwargs)


if __name__ == '__main__':
    unittest.main()
