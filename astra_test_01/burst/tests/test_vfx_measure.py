"""Independent synthetic contracts and known-bad inputs for T3s."""
import colorsys
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

from oracle.vfx_measure import compare, measure

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'runs/C-3/t3/T3s'
REFERENCE = ROOT/'oracle/vfx_reference_hades.json'


def synthetic_frames():
    """30 exact supports; peak at 1, half at frame 4, tail 20%, 3 planes.

    Equal populations at hue 152/168 degrees give circular SD 8.013 degrees
    before 8-bit quantization. Full support determines geometry independently
    of value/saturation. Rotating the colour layout makes 30 unique drawings.
    """
    envelope = [.2, 1., .85, .7, .5] + [.2]*25
    frames = []
    for i, fraction in enumerate(envelope):
        n = round(10000*fraction)
        height = n//100
        core = round(n*(.30 if i == 1 else .15))
        colors = [np.round(np.array(colorsys.hsv_to_rgb(h/360, .8, v))*255).astype(np.uint8)
                  for v in (.35, .7) for h in (152, 168)]
        colored = np.array([colors[j % 4] for j in range(n-core)], dtype=np.uint8)
        pixels = np.concatenate((np.full((core, 3), 255, np.uint8), colored))
        pixels = np.roll(pixels, i*7, axis=0)
        rgba = np.zeros((128, 128, 4), dtype=np.uint8)
        rgba[10:10+height, 14:114, :3] = pixels.reshape(height, 100, 3)
        rgba[10:10+height, 14:114, 3] = 255
        frames.append(rgba)
    return frames, dict(envelope=envelope, rise_frames=1, rise_ms=1000/60,
                        peak_frame=1, half_frame=4, frames_to_half=3,
                        ms_to_half=3000/60, residue_fraction=.2,
                        white_core_fraction=.30, hue_sd_deg=8., value_bands=3,
                        peak_area_px=10000, width_px=100, height_px=100,
                        width_bh=100/130, height_bh=100/130,
                        bright_s=0., dim_s=.8, unique_frames=30,
                        unique_frames_per_s=60., observed_life_frames=30,
                        observed_life_ms=500., straight_alpha_edges=0)


def write_frames(directory, frames, names=None):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for i, array in enumerate(frames):
        Image.fromarray(array).save(directory/(names[i] if names else f'frame_{i:03d}.png'))
    return directory


class VFXMeasureTests(unittest.TestCase):
    def setUp(self):
        temporary = OUT/'tmp'
        temporary.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=temporary, prefix='unit_')
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def sample(self, frames, timing=60, plate='alpha', body_h_px=130):
        return measure(write_frames(self.path/'frames', frames), timing, body_h_px, plate)

    def test_known_30_frame_envelope_and_all_instruments(self):
        frames, expected = synthetic_frames()
        result = self.sample(frames)
        checks = {
            'rise_frames': result['O1']['rise_frames'], 'rise_ms': result['O1']['rise_ms'],
            'peak_frame': result['O1']['peak_frame'], 'half_frame': result['O1']['half_frame'],
            'frames_to_half': result['O1']['frames_to_half'], 'ms_to_half': result['O1']['ms_to_half'],
            'residue_fraction': result['residue_fraction'],
            'white_core_fraction': result['O3']['core_frac_at_peak'],
            'hue_sd_deg': result['O4']['hue_sd_deg_at_peak'], 'value_bands': result['O10']['count_at_peak'],
            'peak_area_px': result['O1']['peak_area_px'],
            'bright_s': result['O5']['bright_15_median_at_peak'],
            'dim_s': result['O5']['dim_25_median_at_peak'],
            'straight_alpha_edges': result['straight_alpha_edges']['count']}
        checks.update({k: result['O6'][k] for k in ('width_px', 'height_px', 'width_bh', 'height_bh')})
        checks.update({k: result['O8'][k] for k in ('unique_frames', 'unique_frames_per_s')})
        checks.update({k: result['O2'][k] for k in ('observed_life_frames', 'observed_life_ms')})
        for name, measured in checks.items():
            with self.subTest(quantity=name):
                self.assertAlmostEqual(measured, expected[name], delta=abs(expected[name])*.05)
        np.testing.assert_allclose(result['O1']['envelope_area_over_peak'], expected['envelope'], rtol=.05)
        self.assertEqual(result['O3']['classification'], 'flash-first')
        self.assertIsNone(result['O2']['visible_life_frames'])
        self.assertTrue(result['O2']['censored'])
        self.assertTrue(result['O10']['inspect_only'])
        self.assertTrue(all(row['passed'] is None for row in result['results']))
        rate = next(row for row in compare(result, REFERENCE) if row['id'] == 'O8_rate')
        self.assertIs(rate['in_band'], True)
        json.dumps(result, allow_nan=False)

    def test_flat_value_is_one_mode_and_achromatic_hue_is_missing(self):
        a = np.full((10, 10, 4), [128, 128, 128, 255], np.uint8)
        r = self.sample([a])
        self.assertEqual(r['O10']['count_at_peak'], 1)
        self.assertIsNone(r['O4']['hue_sd_deg_at_peak'])
        self.assertEqual(r['O4']['series'][0]['n'], 0)
        self.assertIsNone(next(row for row in compare(r, REFERENCE) if row['id'] == 'O10_modes')['passed'])

    def test_finite_life_and_irregular_durations(self):
        frames = []
        for n in (0, 2, 10, 5, 1, 0):
            a = np.zeros((4, 4, 4), np.uint8)
            a.reshape(-1, 4)[:n] = [30, 90, 180, 255]
            frames.append(a)
        r = self.sample(frames, [10, 20, 30, 40, 50, 60])
        self.assertEqual(r['O1']['onset_frame'], 1)
        self.assertEqual(r['O1']['rise_ms'], 20)
        self.assertEqual(r['O1']['frames_to_half'], 1)
        self.assertEqual(r['O1']['ms_to_half'], 30)
        self.assertEqual(r['O2']['end_frame'], 5)  # exactly .10 at 4 is still visible
        self.assertEqual(r['O2']['visible_life_frames'], 4)
        self.assertEqual(r['O2']['visible_life_ms'], 140)
        self.assertFalse(r['O2']['censored'])
        self.assertIsNone(r['O3']['white_core_fraction'][0])
        self.assertEqual(r['residue_fraction'], 0)

    def test_core_last_and_no_core(self):
        a = np.full((4, 4, 4), [30, 180, 90, 255], np.uint8)
        b = a.copy(); b[:2, :, :3] = 255
        r = self.sample([a, b])
        self.assertEqual(r['O3']['classification'], 'core-last')
        self.assertEqual(r['O1']['peak_frame'], 0)
        r = self.sample([a, a])
        self.assertEqual(r['O3']['classification'], 'no-core')

    def test_white_core_thresholds_and_hue_wrap(self):
        rgb = [np.round(np.array(colorsys.hsv_to_rgb(h/360, 1., .8))*255).astype(np.uint8)
               for h in (359, 1)]
        a = np.array([[[*rgb[0], 255], [*rgb[1], 255], [255, 255, 255, 255],
                       [242, 242, 242, 255], [255, 190, 190, 255]]], np.uint8)
        r = self.sample([a])
        self.assertAlmostEqual(r['O3']['core_frac_at_peak'], .2)
        self.assertLess(r['O4']['hue_sd_deg_at_peak'], 1.1)

    def test_alpha_edges_and_hidden_rgb(self):
        a = np.zeros((5, 5, 4), np.uint8)
        a[1:4, 1:4] = [60, 50, 40, 255]
        a[1, 1] = [255, 255, 255, 128]
        a[0, 0] = [255, 255, 255, 0]
        r = self.sample([a])
        self.assertEqual(r['O1']['peak_area_px'], 9)
        self.assertEqual(r['straight_alpha_edges']['count'], 1)
        self.assertEqual(r['O6']['bbox_at_peak'], [1, 1, 4, 4])

    def test_exact_unique_vs_consecutive_drawings(self):
        a = np.full((2, 2, 4), [1, 2, 3, 255], np.uint8)
        b = a.copy(); b[0, 0, 0] = 2
        r = self.sample([a, b, a], 30)
        self.assertEqual(r['O8']['unique_frames'], 2)
        self.assertAlmostEqual(r['O8']['unique_frames_per_s'], 20)
        self.assertEqual(r['O8']['drawing_changes'], 2)
        self.assertAlmostEqual(r['O8']['drawing_runs_per_s'], 30)

    def test_black_exact_support_and_no_alpha_claim(self):
        a = np.zeros((5, 5, 3), np.uint8)
        a[2, 2] = [1, 0, 0]
        r = self.sample([a], plate='black')
        self.assertEqual(r['O1']['peak_area_px'], 1)
        self.assertIsNone(r['straight_alpha_edges']['count'])
        self.assertFalse(r['straight_alpha_edges']['available'])

    def test_empty_support_is_unevaluable_not_zero_life(self):
        r = self.sample([np.zeros((3, 3, 4), np.uint8)]*2)
        self.assertIsNone(r['O1']['peak_frame'])
        self.assertIsNone(r['O2']['visible_life_frames'])
        self.assertIsNone(r['O4']['hue_sd_deg_at_peak'])
        self.assertIsNone(r['residue_fraction'])
        self.assertEqual(r['O1']['envelope_area_over_peak'], [None, None])
        json.dumps(r, allow_nan=False)

    def test_natural_frame_order(self):
        a = np.full((2, 2, 4), 255, np.uint8)
        b = a.copy(); b[0] = 0
        p = write_frames(self.path/'frames', [a, b], ['frame10.png', 'frame2.png'])
        r = measure(p, 60)
        self.assertEqual(r['frame_files'], ['frame2.png', 'frame10.png'])
        self.assertEqual(r['O1']['rise_frames'], 1)

    def test_malformed_no_frames_and_mixed_sizes(self):
        with self.assertRaises(ValueError):
            measure(self.path, 60)
        with self.assertRaises(ValueError):
            measure(self.path/'absent', 60)
        with self.assertRaises(ValueError):
            self.sample([np.zeros((3, 3, 4), np.uint8), np.zeros((2, 3, 4), np.uint8)])

    def test_malformed_fps_durations_and_body(self):
        p = write_frames(self.path/'frames', [np.full((2, 2, 4), 255, np.uint8)]*2)
        for value in (0, -1, float('nan'), float('inf'), True, '60', [], [10],
                      [10, 0], [10, -1], [10, float('nan')], [10, True], {'fps': 60}):
            with self.subTest(timing=repr(value)), self.assertRaises(ValueError):
                measure(p, value)
        for body in (0, -1, float('nan'), True):
            with self.subTest(body=body), self.assertRaises(ValueError):
                measure(p, 60, body_h_px=body)

    def test_malformed_plate_and_mode(self):
        p = write_frames(self.path/'frames', [np.zeros((2, 2, 3), np.uint8)])
        with self.assertRaises(ValueError):
            measure(p, 60, plate='green')
        with self.assertRaises(ValueError):
            measure(p, 60, plate='alpha')

    def test_compare_rise_1_and_6_with_source_conflict_exposed(self):
        for rise, expected in ((1, True), (6, False)):
            rows = compare({'O1': {'rise_frames': rise}}, REFERENCE)
            strike = next(r for r in rows if r['id'] == 'O1_rise_strike')
            aggregate = next(r for r in rows if r['id'] == 'O1_rise_all_exemplars')
            self.assertIs(strike['in_band'], expected)
            self.assertEqual(strike['threshold'], {'min': 0, 'max': 1})
            self.assertIs(aggregate['in_band'], True)
            self.assertTrue(all(r['passed'] is None for r in rows))

    def test_compare_commitment_proposal_inspection_and_missing(self):
        ref = {'committed': True, 'bands': [dict(path='x', min=1, max=2)]}
        self.assertIs(compare({'x': 1}, ref)[0]['passed'], True)
        self.assertIs(compare({'x': 3}, ref)[0]['passed'], False)
        for value in (None, float('nan'), float('inf'), True, '1'):
            row = compare({'x': value}, ref)[0]
            self.assertIsNone(row['in_band']); self.assertIsNone(row['passed'])
            json.dumps(row, allow_nan=False)
        for flag, val in (('proposed', True), ('committed', False), ('inspect_only', True)):
            changed = copy.deepcopy(ref); changed['bands'][0][flag] = val
            self.assertIsNone(compare({'x': 1}, changed)[0]['passed'])
        ref['bands'][0]['path'] = 'O10.count_at_peak'
        self.assertIsNone(compare({'O10': {'count_at_peak': 2}}, ref)[0]['passed'])

    def test_compare_invalid_and_open_bounds(self):
        ref = {'bands': [dict(path='x', min=1, max=None)]}
        self.assertIs(compare({'x': 9}, ref)[0]['in_band'], True)
        ref['bands'][0]['min'] = None
        self.assertIsNone(compare({'x': 9}, ref)[0]['in_band'])
        for low, high in ((3, 1), (float('nan'), 3), (1, True)):
            ref['bands'][0].update(min=low, max=high)
            with self.assertRaises(ValueError):
                compare({'x': 2}, ref)

    def test_cli_fps_durations_reference_and_bad_fps(self):
        p = write_frames(self.path/'frames', [np.full((2, 2, 4), 255, np.uint8)]*2)
        durations = self.path/'durations.json'; durations.write_text('[20, 30]')
        command = [sys.executable, '-B', '-m', 'oracle.vfx_measure', str(p), '--fps', '60',
                   '--durations', str(durations), '--ref', str(REFERENCE)]
        run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result['duration_ms'], 50)
        self.assertTrue(result['comparison'])
        bad = subprocess.run(command+['--fps', '0'], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)


if __name__ == '__main__':
    unittest.main()
