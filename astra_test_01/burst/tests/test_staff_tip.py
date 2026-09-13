"""T3i alpha staff instrument: analytic silhouettes and registered clips."""
import math
from pathlib import Path
import unittest
import numpy as np
from PIL import Image, ImageDraw
from oracle.staff_tip import tip

ROOT = Path(__file__).resolve().parents[1]


def figure(staff=((170, 90), (170, 380)), hair=False):
    im = Image.new('RGBA', (512, 512))
    draw = ImageDraw.Draw(im)
    draw.rectangle((225, 155, 265, 195), fill='white')
    draw.rectangle((215, 196, 280, 340), fill='white')
    draw.rectangle((220, 341, 245, 399), fill='white')
    draw.rectangle((252, 341, 277, 399), fill='white')
    if hair:
        for x in (228, 235, 243, 251, 260):
            draw.line((x, 156, x-2, 198), fill='white', width=3)
    if staff:
        draw.line((*staff[0], *staff[1]), fill='white', width=3)
    return im


class StaffTipTests(unittest.TestCase):
    def check_tip(self, im, expected, tolerance=2):
        result = tip(im)
        self.assertEqual(result['reason'], 'ok', result)
        self.assertGreaterEqual(result['line_inliers'], 40)
        self.assertLessEqual(math.dist(result['tip'], expected), tolerance, result)
        return result

    def test_vertical_three_pixel_staff(self):
        self.check_tip(figure(), (170, 90))

    def test_diagonal_staff(self):
        self.check_tip(figure(((160, 100), (205, 385))), (160, 100))

    def test_raised_above_head_does_not_define_head_top(self):
        self.check_tip(figure(((249, 65), (185, 300))), (249, 65))

    def test_hair_strands_excluded(self):
        self.check_tip(figure(hair=True), (170, 90))

    def test_near_horizontal_chooses_end_farther_from_head(self):
        self.check_tip(figure(((40, 220), (214, 220))), (40, 220))

    def test_empty_no_head_short_staff_and_wrong_input(self):
        self.assertEqual(tip(Image.new('RGBA', (512, 512)))['reason'], 'empty_alpha')
        im = Image.new('RGBA', (512, 512)); ImageDraw.Draw(im).line((30, 10, 30, 300), fill='white', width=3)
        self.assertEqual(tip(im)['reason'], 'no_head_run_ge_14')
        self.assertIsNone(tip(figure(((170, 90), (170, 99))))['tip'])
        self.assertIsNone(tip(figure(None, hair=True))['tip'])
        for bad in (Image.new('RGB', (32, 32)), np.zeros((32, 32, 4), dtype=float)):
            with self.assertRaises(ValueError): tip(bad)

    def test_real_cast_anchors(self):
        for index, expected in ((0, (216, 165)), (2, (249, 82))):
            with self.subTest(frame=index):
                with Image.open(ROOT/f'runs/C-3/cells/cast_S/frames/cast/S/cast_S_{index:02d}.png') as im:
                    self.check_tip(im, expected, 5)

    def test_real_walk_e_staff_line(self):
        with Image.open(ROOT/'runs/C-3/cells/walk_E/frames/walk/E/walk_E_05.png') as im:
            result = self.check_tip(im, (285, 160), 5)
        x, y = result['tip']
        # Independently visible staff segment (285,160) -> (323,383).
        distance = abs(223*(x-285)-38*(y-160))/math.hypot(223,38)
        self.assertLessEqual(distance, 2.5)


if __name__ == '__main__': unittest.main()
