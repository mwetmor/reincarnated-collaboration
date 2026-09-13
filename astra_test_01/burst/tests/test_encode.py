"""T3d synthetic instruments, including known-bad input and seam cases."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

from review import encode

FFPROBE = '/opt/homebrew/bin/ffprobe'
TMP = Path(__file__).resolve().parent/'tmp'


def probe(path):
    return json.loads(subprocess.check_output([FFPROBE, '-v', 'error', '-select_streams', 'v:0',
        '-show_streams', '-of', 'json', str(path)]))['streams'][0]


def decode(path, count=None):
    info = probe(path)
    command = [encode.FFMPEG, '-v', 'error', '-i', str(path)]
    if count is not None:
        command += ['-frames:v', str(count)]
    raw = subprocess.check_output(command+['-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'])
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, info['height'], info['width'], 3)


class EncodeTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='t3d_encode_', dir=TMP)
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)
        self.frames = [Image.new('RGBA', (32, 32), (v, v, v, 255)) for v in (40, 100, 180)]

    def test_h264_scale_loops_fps_decode_and_faststart(self):
        target = encode.encode_loop(self.frames, 12, self.out/'loop.mp4')
        info = probe(target)
        self.assertEqual((info['codec_name'], info['codec_tag_string'], info['pix_fmt']), ('h264', 'avc1', 'yuv420p'))
        self.assertEqual((info['width'], info['height'], int(info['nb_frames'])), (64, 64, 15))
        self.assertEqual(info['r_frame_rate'], '12/1')
        pixels = decode(target)
        self.assertLessEqual(float(np.abs(pixels[0].astype(float)-40).mean()), 3)
        self.assertLessEqual(float(np.abs(pixels[0].astype(float)-pixels[3]).mean()), 3)
        data = target.read_bytes()
        self.assertLess(data.index(b'moov'), data.index(b'mdat'))

    def test_one_to_one_alpha_canvas_and_odd_padding(self):
        frame = Image.new('RGBA', (31, 29), (255, 0, 255, 0))
        frame.putpixel((15, 14), (200, 200, 200, 128))
        before = frame.tobytes()
        target = encode.encode_loop([frame], 8, self.out/'odd.mp4', scale=1, loops=1)
        image = decode(target)[0]
        self.assertEqual(image.shape, (30, 32, 3))
        self.assertLessEqual(float(np.abs(image[0, 0].astype(float)-[58, 63, 74]).mean()), 3)
        self.assertEqual(frame.tobytes(), before)
        target = encode.encode_loop([frame], 8, self.out/'canvas.mp4', scale=1, loops=1, canvas=(40, 40))
        self.assertEqual(decode(target).shape, (1, 40, 40, 3))

    def test_side_by_side_common_clock(self):
        left = [Image.new('RGB', (32, 32), (v,)*3) for v in (40, 180)]
        right = [Image.new('RGB', (32, 32), (v,)*3) for v in (30, 70, 110, 150)]
        target = encode.encode_side_by_side(left, right, 2, 4, self.out/'sbs.mp4', 32)
        pixels = decode(target)
        self.assertEqual(pixels.shape, (4, 32, 64, 3))
        for i, (lv, rv) in enumerate(zip((40, 40, 180, 180), (30, 70, 110, 150))):
            self.assertLessEqual(abs(float(pixels[i, 8:24, 8:24].mean())-lv), 3)
            self.assertLessEqual(abs(float(pixels[i, 8:24, 40:56].mean())-rv), 3)

    def test_side_by_side_shorter_sequence_repeats(self):
        target = encode.encode_side_by_side(self.frames[:1], self.frames, 4, 2, self.out/'unequal.mp4', 32)
        pixels = decode(target)
        self.assertEqual(len(pixels), 6)
        self.assertLessEqual(float(np.abs(pixels[:, 8:24, 8:24].astype(float)-40).mean()), 3)

    def test_seam_order_amplification_and_known_bad(self):
        target = encode.seam_pairs_png(self.frames, self.out/'seam.png')
        with Image.open(target) as im:
            self.assertEqual(im.size, (96, 32))
            self.assertEqual(im.getpixel((0, 0)), (180,)*3)
            self.assertEqual(im.getpixel((32, 0)), (40,)*3)
            self.assertEqual(im.getpixel((64, 0)), (255,)*3)
        target = encode.seam_pairs_png([self.frames[0], self.frames[0]], self.out/'closed.png')
        with Image.open(target) as im:
            self.assertEqual(im.getpixel((64, 0)), (0,)*3)
        target = encode.seam_pairs_png([Image.new('RGBA', (32, 32), (c, 0, 0, 0)) for c in (0, 255)], self.out/'hidden.png')
        with Image.open(target) as im:
            self.assertEqual(im.getpixel((64, 0)), (0,)*3)

    def test_strip_numbered_and_plain(self):
        for numbered in (False, True):
            path = encode.strip_png(self.frames, self.out/f'{numbered}.png', numbered)
            with Image.open(path) as im:
                self.assertEqual(im.size, (96, 52 if numbered else 32))
                self.assertEqual(im.getpixel((40, 30)), (100,)*3)
                if numbered:
                    self.assertGreater(int(np.array(im)[:20].max()), 100)

    def test_known_bad_parameters(self):
        for kwargs in ({'fps': 0}, {'fps': float('nan')}, {'scale': -1}, {'loops': 0},
                       {'loops': 1.5}, {'resample': 'bogus'}, {'canvas': (16, 16)}):
            args = {'fps': 12, 'out_mp4': self.out/'invalid.mp4', **kwargs}
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                encode.encode_loop(self.frames, **args)
        for frames in ([], [self.frames[0], Image.new('RGB', (12, 12))], [np.zeros((2, 2, 4))]):
            with self.subTest(frames=str(type(frames))), self.assertRaises(ValueError):
                encode.encode_loop(frames, 12, self.out/'invalid.mp4')
        with self.assertRaises(ValueError):
            encode.encode_side_by_side(self.frames, self.frames, 0, 12, self.out/'bad.mp4', 32)
        with self.assertRaises(ValueError):
            encode.encode_side_by_side(self.frames, self.frames, 12, 12, self.out/'bad.mp4', 31)

    def test_encoder_error_is_not_silent(self):
        with patch.object(encode, 'FFMPEG', '/usr/bin/false'):
            with self.assertRaises((RuntimeError, BrokenPipeError)):
                encode.encode_loop(self.frames, 12, self.out/'error.mp4')
        self.assertFalse((self.out/'error.mp4').exists())


if __name__ == '__main__':
    unittest.main()
