import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

from review.composite_socket import composite, estimate_sockets, premultiplied_over

TMP = Path(__file__).resolve().parent/'tmp'


def character():
    a = np.zeros((32, 32, 4), np.uint8)
    a[8:28, 10:22] = (40, 60, 100, 255)
    return a


def effect():
    a = np.zeros((8, 8, 4), np.uint8)
    a[3:6, 3:6] = (100, 190, 255, 128)
    return a


def fake_encode(frames, fps, out_mp4, **kwargs):
    Path(out_mp4).write_bytes(b'unit-test encoder stand-in')
    return Path(out_mp4)


class TestCompositeSocket(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=TMP, prefix='t3e_')
        self.addCleanup(self.tmp.cleanup)

    def test_porter_duff_over_and_no_double_alpha(self):
        base = np.array([[[0, 0, 255, 128]]], np.uint8)
        top = np.array([[[255, 0, 0, 128]]], np.uint8)
        before = base.copy(), top.copy()
        np.testing.assert_array_equal(premultiplied_over(base, top), [[[170, 0, 85, 192]]])
        np.testing.assert_array_equal(base, before[0]); np.testing.assert_array_equal(top, before[1])
        blank = np.array([[[255, 255, 255, 0]]], np.uint8)
        np.testing.assert_array_equal(premultiplied_over(blank, top), top)
        np.testing.assert_array_equal(premultiplied_over(blank, blank), np.zeros((1, 1, 4), np.uint8))

    def test_fixed_socket_tail_and_encoder_contract(self):
        with patch('review.composite_socket.encode_loop', side_effect=fake_encode) as enc:
            r = composite([character()]*3, [effect()]*2, [16, 12], self.tmp.name, 20)
        self.assertEqual(r['count'], 3)
        self.assertEqual(r['placements'][0]['offset_xy'], [12, 8])
        self.assertIsNone(r['placements'][2]['vfx_index'])
        self.assertTrue(r['attachment']['passed'])
        self.assertEqual(enc.call_args.kwargs, dict(scale=1, loops=1))
        self.assertEqual(set(r['pse']), {'character', 'vfx', 'composite'})
        np.testing.assert_array_equal(np.array(Image.open(r['frames'][2])), character())
        persisted = json.loads(Path(r['sockets_json']).read_text())
        self.assertEqual(persisted['xy_per_frame'], [[16., 12.]]*3)

    def test_moving_socket_and_longer_effect_not_truncated(self):
        with patch('review.composite_socket.encode_loop', side_effect=fake_encode):
            r = composite([character()], [effect()]*3, [[12, 12], [16, 12], [20, 12]], self.tmp.name, 20)
        self.assertEqual([p['character_index'] for p in r['placements']], [0]*3)
        for i, x in enumerate((12, 16, 20)):
            with Image.open(r['frames'][i]) as im:
                self.assertGreater(im.getpixel((x, 12))[0], 40)

    def test_clipping_is_recorded(self):
        with patch('review.composite_socket.encode_loop', side_effect=fake_encode):
            r = composite([character()], [effect()], [-2, -2], self.tmp.name, 20)
        self.assertGreater(r['placements'][0]['clipped_alpha_fraction'], 0)

    def test_tip_mapping_pixel_centres_and_identity(self):
        native = [character()]*2
        identity = estimate_sockets(native)
        mapped = estimate_sockets(native, dict(scale=.5, translation_xy=[3, 7], source_size=[32, 32]))
        expected = (np.asarray(identity['xy_per_frame'])+.5)*.5-.5+[3, 7]
        np.testing.assert_allclose(mapped['xy_per_frame'], expected)
        self.assertEqual(identity['input_space'], 'registered')
        self.assertEqual(mapped['input_space'], 'native')
        blank = np.zeros((32, 32, 4), np.uint8)
        self.assertEqual(estimate_sockets([blank])['xy_per_frame'], [None])

    def test_estimate_report_can_drive_composite(self):
        report = estimate_sockets([character()]*2)
        with patch('review.composite_socket.encode_loop', side_effect=fake_encode):
            r = composite([character()]*2, [effect()]*2, report, self.tmp.name, 20)
        self.assertEqual(r['socket_source']['source'], 'oracle.video_cut.track.tip_xy')

    def test_validation(self):
        for sockets in ([[0, 0]], [float('nan'), 0], [None, None]):
            with self.subTest(sockets=sockets), self.assertRaises(ValueError):
                composite([character()]*2, [effect()], sockets, self.tmp.name, 20)
        with self.assertRaises(ValueError): composite([], [effect()], [0, 0], self.tmp.name, 20)
        with self.assertRaises(ValueError): composite([character()], [effect()], [0, 0], self.tmp.name, 0)
        for transform in (dict(scale=2, translation_xy=[0, 0]),
                          dict(scale=.5, translation_xy=[.5, 0]),
                          dict(scale=.5, translation_xy=[0, 0], source_size=[64, 64])):
            with self.subTest(transform=transform), self.assertRaises(ValueError):
                estimate_sockets([character()], transform)


if __name__ == '__main__':
    unittest.main()
