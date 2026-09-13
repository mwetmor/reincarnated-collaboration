import colorsys
import json
import unittest

import numpy as np

from gates.element_hue import evaluate


def color(hue, saturation=1., alpha=255):
    rgb = np.rint(np.array(colorsys.hsv_to_rgb(hue/360, saturation, 1.))*255).astype(np.uint8)
    a = np.zeros((16, 16, 4), np.uint8)
    a[..., :3] = rgb; a[..., 3] = alpha
    return a


class TestElementHue(unittest.TestCase):
    def test_frost_and_fire_rotated_known_bad(self):
        frost, fire = color(210), color(30)
        self.assertTrue(evaluate([frost])['passed'])
        self.assertFalse(evaluate([fire])['passed'])
        self.assertTrue(evaluate([fire], element='fire')['passed'])
        self.assertFalse(evaluate([frost], element='fire')['passed'])

    def test_band_edges_and_outside(self):
        for hue in (180, 200, 230):
            with self.subTest(hue=hue):
                self.assertTrue(evaluate([color(hue)])['passed'])
        for hue in (179, 231, 90, 300):
            with self.subTest(hue=hue):
                self.assertFalse(evaluate([color(hue)])['passed'])
        self.assertTrue(evaluate([color(0)], 'fire')['passed'])

    def test_invisible_rgb_and_white_do_not_vote_hue(self):
        self.assertTrue(evaluate([color(210), color(20, alpha=0)])['passed'])
        self.assertIsNone(evaluate([color(0, saturation=0)])['passed'])
        self.assertIsNone(evaluate([color(210, alpha=0)])['passed'])

    def test_alpha_value_weighted_dominance_not_target_filter(self):
        a = color(25)
        a[0, 0] = color(210)[0, 0]
        self.assertFalse(evaluate([a])['passed'])
        self.assertTrue(evaluate([color(25, alpha=10), color(210)])['passed'])
        dark_fire = color(25); dark_fire[..., :3] //= 10
        self.assertTrue(evaluate([dark_fire, color(210)])['passed'])

    def test_physical_low_saturation(self):
        self.assertTrue(evaluate([color(210, saturation=.1)], 'physical')['passed'])
        self.assertFalse(evaluate([color(210)], 'physical')['passed'])
        self.assertIsNone(evaluate([], 'physical')['passed'])

    def test_circular_mode_wraps_at_red(self):
        r = evaluate([color(359), color(1)], 'fire')
        self.assertTrue(r['passed'])
        self.assertLess(r['value'], 2)

    def test_schema_and_invalid_element(self):
        r = evaluate([color(210)])
        self.assertEqual(r['threshold'], [180., 230.])
        self.assertEqual(json.loads(r['notes'])['in_band_fraction'], 1)
        json.dumps(r, allow_nan=False)
        with self.assertRaises(ValueError): evaluate([color(210)], 'unknown')


if __name__ == '__main__':
    unittest.main()
