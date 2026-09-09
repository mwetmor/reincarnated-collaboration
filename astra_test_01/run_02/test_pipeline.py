"""Synthetic instrument tests; shapes here are test fixtures, never asset art."""
import unittest
import numpy as np
from PIL import Image, ImageDraw
from pipeline import extract, registration, measure
from registration_preflight import measured_anchor, preflight


class PipelineTests(unittest.TestCase):
    def test_green_matte_recovers_known_neutral_edge(self):
        a = np.zeros((80, 80, 4), dtype=np.uint8)
        a[20:60, 20:60] = [100, 100, 100, 255]
        a[19, 20:60] = [100, 100, 100, 128]
        fg = Image.fromarray(a)
        bg = Image.new('RGBA', fg.size, (0, 255, 0, 255))
        bg.alpha_composite(fg)
        matte, _ = extract(bg.convert('RGB'))
        result = np.array(matte)
        np.testing.assert_allclose(result[19, 30], a[19, 30], atol=2)
        self.assertTrue(np.all(result[0] == 0))

    def test_native_alpha_preserves_dark_interior(self):
        a = np.zeros((80, 80, 4), dtype=np.uint8)
        a[20:60, 20:60] = [2, 3, 5, 255]
        result, info = extract(Image.fromarray(a))
        self.assertTrue(info['native_input_alpha'])
        np.testing.assert_array_equal(np.array(result), a)

    def test_checkerboard_is_rejected(self):
        a = np.indices((80, 80)).sum(axis=0) % 2 * 60 + 150
        with self.assertRaisesRegex(ValueError, 'No native alpha'):
            extract(Image.fromarray(np.repeat(a[..., None], 3, axis=2).astype('uint8')))

    def test_upscale_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'upscale'):
            registration(Image.new('RGBA', (100, 100)), {'body_height': 80, 'anchor': [50, 90]})

    def test_measured_contact_registration_and_independent_output_check(self):
        im = Image.new('RGBA', (1024, 1024))
        d = ImageDraw.Draw(im)
        d.rectangle((300, 200, 650, 780), fill=(80, 80, 90, 255))
        d.rectangle((320, 780, 400, 840), fill=(50, 50, 70, 255))
        d.rectangle((570, 780, 630, 900), fill=(50, 50, 70, 255))
        source_rois = [[300, 790, 420, 860], [550, 790, 650, 920]]
        anchor = measured_anchor(im, source_rois)
        frame, _ = registration(im, {'body_height': 701, 'anchor': anchor})
        # Output-space review regions, separately specified; not transformed landmarks.
        result = preflight(frame, [[195, 375, 240, 400], [283, 393, 315, 426]])
        self.assertTrue(result['pass'], result)

    def test_clipped_sole_does_not_false_pass(self):
        im = Image.new('RGBA', (100, 100))
        ImageDraw.Draw(im).rectangle((20, 20, 40, 90), fill='white')
        with self.assertRaisesRegex(ValueError, 'clips'):
            measured_anchor(im, [[10, 30, 50, 80], [10, 30, 50, 95]])

    def test_right_light_and_clipping_are_detected(self):
        im = Image.new('RGBA', (100, 100))
        d = ImageDraw.Draw(im)
        d.rectangle((20, 0, 80, 90), fill=(30, 40, 60, 255))
        d.rectangle((70, 10, 80, 50), fill='white')
        result = measure(im)
        self.assertFalse(result['light_pass'])
        self.assertEqual(result['border_alpha_max'], 255)


if __name__ == '__main__':
    unittest.main()
