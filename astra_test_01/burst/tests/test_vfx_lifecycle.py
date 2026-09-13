"""Synthetic lifecycle and known-bad cases; no external fixtures."""
import json
import unittest

import numpy as np

from gates.vfx_lifecycle import evaluate, sequence_pse


def effect(alpha, size=16):
    a = np.zeros((size, size, 4), np.uint8)
    a[4:12, 4:12] = (40, 160, 255, alpha)
    return a


def rows(module, alphas, fps=20):
    return {r['id']: r for r in evaluate(module, [effect(a) for a in alphas], fps)}


class TestVfxLifecycle(unittest.TestCase):
    def test_cast_count_clock_and_energy(self):
        r = rows('cast', [10, 30, 90, 255, 180, 100, 30, 0])
        for name in ['vfx.frame_count', 'vfx.fps', 'vfx.energy_curve', 'pse_check']:
            self.assertTrue(r[name]['passed'], name)
        self.assertEqual(json.loads(r['vfx.energy_curve']['notes'])['peak_index'], 3)

    def test_wrong_count_and_fps(self):
        r = rows('cast', [1, 30, 255, 90, 0], 16)
        self.assertFalse(r['vfx.frame_count']['passed'])
        self.assertFalse(r['vfx.fps']['passed'])

    def test_flat_second_peak_and_no_release(self):
        for alphas in ([50]*8, [1, 20, 255, 60, 150, 50, 10, 0],
                       [1, 20, 30, 40, 50, 60, 90, 255],
                       [1, 20, 255, 255, 50, 20, 10, 0]):
            with self.subTest(alphas=alphas):
                self.assertFalse(rows('cast', alphas)['vfx.energy_curve']['passed'])

    def test_impact_transparent_ending(self):
        r = rows('impact', [1, 80, 255, 200, 160, 100, 60, 30, 1, 0])
        self.assertTrue(r['vfx.energy_curve']['passed'])
        self.assertTrue(r['vfx.final_alpha_fraction']['passed'])
        self.assertEqual(r['vfx.final_alpha_fraction']['value'], 0)

    def test_known_bad_opaque_tail_and_secondary_peak(self):
        r = rows('impact', [1, 80, 255, 200, 160, 100, 60, 30, 1, 255])
        self.assertFalse(r['vfx.final_alpha_fraction']['passed'])
        self.assertFalse(r['vfx.energy_curve']['passed'])

    def test_final_alpha_literal_boundary(self):
        good = rows('impact', [1, 60, 200, 150, 100, 70, 40, 10, 2, 1])
        bad = rows('impact', [1, 60, 200, 150, 100, 70, 40, 10, 3, 2])
        self.assertEqual(good['vfx.final_alpha_fraction']['value'], .005)
        self.assertTrue(good['vfx.final_alpha_fraction']['passed'])
        self.assertFalse(bad['vfx.final_alpha_fraction']['passed'])

    def test_empty_energy_is_unevaluable(self):
        r = rows('impact', [0]*10)
        self.assertIsNone(r['vfx.energy_curve']['passed'])
        self.assertIsNone(r['vfx.final_alpha_fraction']['passed'])
        r = {r['id']: r for r in evaluate('cast', [], 20)}
        self.assertFalse(r['vfx.frame_count']['passed'])
        self.assertIsNone(r['pse_check']['passed'])

    def test_travel_symmetry_and_seam(self):
        frames = [effect(150)]*6
        r = {r['id']: r for r in evaluate('travel', frames, 20)}
        self.assertTrue(r['g6_seam']['passed'])
        self.assertEqual(r['vfx.top_bottom_mirror_diff']['value'], 0)
        self.assertIsNone(r['vfx.top_bottom_mirror_diff']['passed'])
        asymmetric = effect(150); asymmetric[8:] = 0
        r = {r['id']: r for r in evaluate('travel', [asymmetric]*6, 20)}
        self.assertEqual(r['vfx.top_bottom_mirror_diff']['value'], 1)
        self.assertIsNone(r['vfx.top_bottom_mirror_diff']['passed'])

    def test_bad_travel_seam_retains_literal_and_median(self):
        r = rows('travel', [20, 20, 20, 40, 70, 255])
        self.assertFalse(r['g6_seam']['passed'])
        self.assertIn('g6b', r)

    def test_invisible_rgb_cannot_change_energy_or_symmetry(self):
        blank = effect(0); blank[..., :3] = (255, 20, 30)
        r = {r['id']: r for r in evaluate('travel', [blank]*6, 20)}
        self.assertIsNone(r['vfx.top_bottom_mirror_diff']['value'])
        self.assertTrue(r['g6_seam']['passed'])

    def test_flash_known_bad_and_loop_closure(self):
        dark = np.zeros((16, 16, 4), np.uint8); dark[..., 3] = 255
        bright = np.full((16, 16, 4), 255, np.uint8)
        r = sequence_pse([dark, bright]*5, 20)
        self.assertFalse(r['passed'])
        loop = sequence_pse([dark, bright], 20, loop=True)
        self.assertFalse(loop['passed'])
        self.assertGreater(loop['value'], 3)

    def test_schema_and_input_errors(self):
        for r in evaluate('cast', [effect(a) for a in [1, 20, 100, 255, 100, 50, 10, 0]], 20):
            self.assertTrue({'id', 'subject', 'passed', 'value', 'threshold', 'op', 'unit', 'evidence', 'notes'} <= r.keys())
            json.dumps(r, allow_nan=False)
        for fps in (0, -1, float('nan'), float('inf'), True):
            with self.subTest(fps=fps), self.assertRaises(ValueError):
                evaluate('cast', [effect(10)], fps)
        with self.assertRaises(ValueError): evaluate('unknown', [effect(10)], 20)
        with self.assertRaises(ValueError): evaluate('cast', [np.zeros((4, 4, 3), np.uint8)], 20)
        with self.assertRaises(ValueError): evaluate('cast', [effect(10), effect(10, 32)], 20)


if __name__ == '__main__':
    unittest.main()
