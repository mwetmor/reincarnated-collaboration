"""Contracted idle geometry, lineage, calibration, contamination and drift cases.

Synthetic amplitude truth and tolerances are unchanged from T1a-idle.
"""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image

from oracle.idle_curves import amplitude, classify_regions, curves, period
from oracle.motion_map import camera_shift, load_frames, motion_energy

ROOT = Path(__file__).resolve().parents[1]
BOX = (206, 130, 306, 330)


def synthetic(static=False, pan=False):
    frames = []
    for i in range(96):
        phase = 0. if static else np.sin(2*np.pi*i/24)
        width = int(round(44+6*phase))
        bob = int(round(2*phase))
        a = np.zeros((512, 512, 3), np.uint8)
        # Static connected core, legs and soles; all stay out of the head band.
        a[170:250, 249:263] = (120, 100, 90)
        a[220:250, 240:272] = (120, 100, 90)
        a[250:310, 240:250] = (110, 95, 85)
        a[250:310, 262:272] = (110, 95, 85)
        a[310:330, 236:250] = (110, 95, 85)
        a[310:330, 262:276] = (110, 95, 85)
        left = 256-width//2
        a[180:212, left:left+width] = (180, 150, 120)
        a[138+bob:160+bob, 245:267] = (200, 180, 150)
        if pan:
            a = np.roll(a, 3*i, axis=1)
        frames.append(a)
    return frames


class Tests(unittest.TestCase):
    def setUp(self):
        (ROOT/'tests/tmp').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def save(self, name, frames, mode='RGB'):
        directory = self.base/name
        directory.mkdir()
        for i, frame in enumerate(frames):
            a = frame.copy()
            support = np.any(a != 0, axis=2)
            if mode == 'green':
                a[~support] = (0, 255, 0)
                a = np.dstack((a, np.full(a.shape[:2], 255, np.uint8)))
            elif mode == 'RGBA':
                a = np.dstack((a, support.astype(np.uint8)*255))
            Image.fromarray(a).save(directory/f'frame_{i:03}.png')
        return directory

    def test_synthetic_idle_contract(self):
        d = curves(self.save('idle', synthetic()), BOX, 12)
        s = d['summary']
        print('SYNTHETIC_IDLE_MEASURED '+json.dumps(s, sort_keys=True))
        with self.subTest(metric='period'):
            self.assertIsNotNone(s['breath_period_frames'])
            self.assertLessEqual(abs(s['breath_period_frames']-24), 1)
        with self.subTest(metric='breath_amplitude'):
            self.assertAlmostEqual(s['breath_amplitude_H'], .06, delta=.06*.15)
        with self.subTest(metric='head_sway'):
            self.assertAlmostEqual(s['head_sway_H'], .02, delta=.02*.15)
        with self.subTest(metric='classification'):
            self.assertEqual(set(s['LOCK']), {'hips', 'legs', 'feet', 'arms_left', 'arms_right'})
            self.assertEqual(set(s['MOTION']), {'head', 'shoulders_chest'})
            self.assertEqual(s['moving_count'], 2)
        self.assertEqual(d['void_frames'], [])
        self.assertEqual(period(np.sin(np.arange(96)*2*np.pi/24), 12)[:2], (24, 2.))
        json.dumps(d, allow_nan=False)

    def test_static_clip(self):
        d = curves(self.save('static', synthetic(static=True)), BOX, 12)
        self.assertEqual(d['summary']['moving_count'], 0)
        self.assertEqual(len(d['summary']['LOCK']), 7)
        self.assertIsNone(d['summary']['breath_period_s'])
        self.assertEqual(d['summary']['breath_amplitude_H'], 0.)
        self.assertIsNone(d['summary']['head_sway_H'])
        self.assertEqual(d['void_frames'], [])
        self.assertEqual(period([1]*96, 12), (None, None, 0.))
        self.assertIsNone(amplitude([None]*96))
        with self.assertRaises(ValueError):
            period([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            classify_regions({'head': [0, 1]}, eps=-1)
        with self.assertRaises(ValueError):
            motion_energy(synthetic(static=True)[:2], (0, 0, 0, 0), 12)

    def test_three_pixel_pan_is_void(self):
        directory = self.save('pan', synthetic(pan=True))
        d = curves(directory, BOX, 12)
        self.assertEqual(d['void_frames'], list(range(96)))
        self.assertEqual(d['frame_status'], ['VOID']*96)
        self.assertIsNone(d['summary']['passed'])
        self.assertIsNone(d['result']['passed'])
        self.assertIn('VOID', d['result']['notes'])
        self.assertTrue(all(np.linalg.norm(v)>1 for v in d['camera_shift_px']))
        ours = curves(directory, BOX, 12, ours=True)
        self.assertEqual(ours['void_frames'], [])
        self.assertEqual(ours['frame_status'], ['MEASURED']*96)
        self.assertNotIn('camera_shift_px', ours)
        self.assertEqual(ours['figure_drift_px'], d['camera_shift_px'])

    def test_animated_background_contamination(self):
        frames = synthetic(static=True)
        yy, xx = np.indices(frames[0].shape[:2])
        for i, frame in enumerate(frames):
            background = ~np.any(frame, axis=2)
            stripes = (((xx+3*i)//7) % 2)*100+20
            frame[background] = np.repeat(stripes[..., None], 3, axis=2)[background]
        d = curves(self.save('contaminated', frames), BOX, 12)
        self.assertGreater(d['contamination'], .5)
        self.assertIsNone(d['summary']['passed'])
        self.assertIsNone(d['result']['passed'])
        self.assertEqual(d['summary']['reason'], 'background_motion')
        self.assertIn('background_motion', d['result']['notes'])
        self.assertEqual(d['control_box'], [326, 130, 426, 330])
        self.assertEqual(set(d['control_energy']), set(d['energy_by_region']))

    def test_noisy_feet_calibrate_lock(self):
        frames = synthetic()
        for i, frame in enumerate(frames):
            frame[300:306, 208:218] = 255 if i % 2 else 0
        known_noise = 60 / (100*30)
        directory = self.save('noisy_feet', frames)
        d = curves(directory, BOX, 12)
        self.assertGreaterEqual(d['eps'], known_noise)
        self.assertEqual(d['eps'], np.percentile(d['energy_by_region']['feet'], 95))
        self.assertEqual(d['floor'], 3*d['eps'])
        self.assertIn('feet', d['summary']['LOCK'])
        overridden = curves(directory, BOX, 12, eps=.001, floor=.002,
                            control_box=[86, 130, 186, 330])
        self.assertEqual(overridden['eps'], .001)
        self.assertEqual(overridden['floor'], .002)
        self.assertEqual(overridden['control_box'], [86, 130, 186, 330])

    def test_green_and_native_alpha_identical_curves(self):
        frames = synthetic()
        rgb = curves(self.save('rgb', frames), BOX, 12)
        for mode in ('green', 'RGBA'):
            with self.subTest(mode=mode):
                directory = self.save(mode, frames, mode)
                loaded = load_frames(directory)
                for expected, actual in zip(frames, loaded):
                    np.testing.assert_array_equal(expected, actual)
                other = curves(directory, BOX, 12)
                for key in ('energy_by_region', 'head_dy_px', 'head_dy_H', 'chest_dw_H',
                            'weapon_tip_H', 'camera_shift_px', 'void_frames', 'summary'):
                    self.assertEqual(other[key], rgb[key])


if __name__ == '__main__':
    unittest.main()
