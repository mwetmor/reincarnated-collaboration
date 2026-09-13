import json
import unittest

import numpy as np

from gates.attachment import evaluate, flare_centroid


def flare(x=12, y=10):
    a = np.zeros((32, 32, 4), np.uint8)
    a[y-1:y+2, x-1:x+2] = (255, 255, 255, 255)
    return a


class TestAttachment(unittest.TestCase):
    def test_exact_and_literal_six_pixel_boundary(self):
        self.assertEqual(flare_centroid(flare()), [12., 10.])
        self.assertTrue(evaluate([flare()], [[12, 10]])['passed'])
        self.assertTrue(evaluate([flare()], [[18, 10]])['passed'])
        self.assertFalse(evaluate([flare()], [[18.01, 10]])['passed'])

    def test_distance_is_max_not_mean(self):
        r = evaluate([flare()]*5, [[12, 10]]*4+[[19, 10]])
        self.assertEqual(r['value'], 7)
        self.assertFalse(r['passed'])

    def test_alpha_weight_and_disconnected_cores(self):
        a = flare()
        a[20:30, 20:30] = (255, 255, 255, 25)
        a[0, 0] = (255, 255, 255, 255)
        self.assertEqual(flare_centroid(a), [12., 10.])

    def test_transparent_frame_excluded(self):
        blank = np.full((32, 32, 4), 255, np.uint8); blank[..., 3] = 0
        self.assertIsNone(flare_centroid(blank))
        r = evaluate([flare(), blank], [[12, 10], None])
        self.assertTrue(r['passed'])
        self.assertEqual(json.loads(r['notes'])['per_frame'][1]['reason'], 'no_emissive_flare')
        self.assertIsNone(evaluate([blank], [[12, 10]])['passed'])

    def test_missing_active_socket_is_not_success(self):
        self.assertIsNone(evaluate([flare(), flare()], [[12, 10], None])['passed'])
        self.assertFalse(evaluate([flare(), flare()], [[30, 10], None])['passed'])

    def test_validation(self):
        with self.assertRaises(ValueError): evaluate([flare()], [])
        with self.assertRaises(ValueError): evaluate([flare()], [[0, float('nan')]])
        with self.assertRaises(ValueError): evaluate([flare()], [[0, 0, 1]])
        for tol in (-1, float('inf'), True):
            with self.subTest(tol=tol), self.assertRaises(ValueError):
                evaluate([flare()], [[0, 0]], tol)
        self.assertIsNone(evaluate([], [])['passed'])


if __name__ == '__main__':
    unittest.main()
