"""Synthetic step-count and invalid-input checks; no real cell mutation."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

from oracle.steps_per_loop import measure

ROOT = Path(__file__).resolve().parents[1]


class StepsPerLoopTests(unittest.TestCase):
    def setUp(self):
        root = ROOT/'runs/C-3/t3/T3n/tmp'
        root.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def frames(self, tops, directory=None, alpha=255):
        directory = directory or self.base/'frames'
        directory.mkdir(parents=True, exist_ok=True)
        for i, y in enumerate(tops):
            a = np.zeros((64,64,4), dtype=np.uint8)
            a[int(y):60,24:40] = (100,150,200,alpha)
            # Below-threshold noise must not become the head-top measurement.
            a[0,0] = (255,255,255,127)
            Image.fromarray(a).save(directory/f'frame_{i:02d}.png')
        return directory

    def test_two_and_four_bobs_in_twelve_registered_frames(self):
        for bobs in (2,4):
            with self.subTest(bobs=bobs):
                tops = 20+np.rint(8*np.cos(2*np.pi*bobs*np.arange(12)/12))
                result = measure(self.frames(tops))
                self.assertEqual(result['steps'],bobs)
                self.assertAlmostEqual(result['confidence'],1.,places=12)
                self.assertEqual(result['method'],'head_top_y_fft_power')
                json.dumps(result,allow_nan=False)

    def test_confidence_is_dominant_share_of_non_dc_power(self):
        tops = [20,26,28,25,20,18,18,18,20,22,22,22]
        series = np.asarray(tops,float); series -= series.mean()
        power = abs(np.fft.rfft(series))[1:]**2
        result = measure(self.frames(tops))
        self.assertEqual(result['steps'],int(np.argmax(power))+1)
        self.assertAlmostEqual(result['confidence'],float(max(power)/sum(power)),places=12)
        self.assertLess(result['confidence'],.99)

    def test_mean_offset_and_alpha_threshold(self):
        tops = 20+np.rint(8*np.cos(2*np.pi*2*np.arange(12)/12))
        first = measure(self.frames(tops,alpha=128))
        second = measure(self.frames(tops+10,alpha=255))
        self.assertEqual(first,second)

    def test_nyquist_bin_is_included(self):
        result = measure(self.frames([20,28]*6))
        self.assertEqual(result['steps'],6)
        self.assertAlmostEqual(result['confidence'],1.)

    def test_flat_loop_has_no_fabricated_steps(self):
        result = measure(self.frames([20]*12))
        self.assertIsNone(result['steps'])
        self.assertEqual(result['confidence'],0.)
        self.assertIn('no non-DC energy',result['method'])

    def test_cell_root_excludes_rest_and_sheets_and_cli_prints_json(self):
        tops = 20+np.rint(8*np.cos(2*np.pi*4*np.arange(12)/12))
        cell = self.base/'walk_E'
        leaf = self.frames(tops,cell/'frames/walk/E')
        self.frames([20]*12,cell/'frames/rest/E')
        self.frames([20]*12,cell/'sheets')
        self.assertEqual(measure(cell),measure(leaf))
        self.assertEqual(measure(cell/'frames'),measure(leaf))
        result = subprocess.run([sys.executable,'-B','-m','oracle.steps_per_loop',str(cell)],
                                cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout),measure(leaf))

    def test_missing_empty_short_and_mixed_loops_rejected(self):
        for path in (self.base/'missing',self.base):
            with self.subTest(path=path), self.assertRaises(ValueError): measure(path)
        one = self.frames([20])
        with self.assertRaises(ValueError): measure(one)
        cell = self.base/'cell'
        self.frames([20,21],cell/'frames/walk/E')
        self.frames([20,21],cell/'frames/run/E')
        with self.assertRaisesRegex(ValueError,'exactly one'): measure(cell)

    def test_empty_alpha_rgb_and_mismatched_canvas_rejected(self):
        for mode,size,color in [('RGBA',(64,64),(0,0,0,0)),
                                ('RGBA',(64,64),(255,255,255,127)),
                                ('RGB',(64,64),(100,150,200)),
                                ('RGBA',(32,32),(100,150,200,255))]:
            directory = self.frames([20,21])
            Image.new(mode,size,color).save(directory/'frame_01.png')
            with self.subTest(mode=mode,size=size,color=color), self.assertRaises(ValueError):
                measure(directory)


if __name__ == '__main__':
    unittest.main()
