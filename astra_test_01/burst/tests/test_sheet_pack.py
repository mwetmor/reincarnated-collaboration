import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image

from oracle.sheet_pack import numbered_frames, sheet_pack


class SheetPackTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).parent / 'tmp'
        root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def frames(self, count=3, size=(16, 12)):
        paths = []
        for i in range(count):
            image = Image.new('RGBA', size, (0, 0, 0, 0))
            image.putpixel((2, 3), (20 + i, 80, 160, 127))
            path = self.root / f'fx{i:05}.png'
            image.save(path)
            paths.append(path)
        return paths

    def test_roundtrip_alpha_canvas_and_pivot(self):
        frames = self.frames()
        out = self.root / 'atlas.png'
        result = sheet_pack(frames, out, columns=2, pivot=(4, 9))
        with Image.open(out) as atlas:
            self.assertEqual(atlas.size, (32, 24))
            for entry, path in zip(result['frames'], frames):
                x, y, w, h = entry['rect']
                with Image.open(path) as source:
                    self.assertEqual(atlas.crop((x, y, x+w, y+h)).tobytes(), source.tobytes())
                self.assertEqual(entry['atlas_pivot'], [x+4, y+9])
            self.assertFalse(np.asarray(atlas)[12:, 16:, :].any())
        self.assertEqual(json.loads(out.with_suffix('.json').read_text()), result)

    def test_numbered_order_nonzero_start(self):
        for n in (10, 8, 9):
            Image.new('RGBA', (2, 2)).save(self.root / f'fx{n}.png')
        self.assertEqual([p.name for p in numbered_frames(self.root)], ['fx8.png', 'fx9.png', 'fx10.png'])

    def test_missing_duplicate_and_malformed(self):
        paths = self.frames()
        paths[1].unlink()
        with self.assertRaises(ValueError):
            numbered_frames(self.root)
        Image.new('RGBA', (16, 12)).save(paths[1])
        duplicate = self.root / 'fx0.png'
        duplicate.write_bytes(paths[0].read_bytes())
        with self.assertRaises(ValueError):
            numbered_frames(self.root)
        duplicate.unlink()
        (self.root / 'fxoops.png').write_bytes(paths[0].read_bytes())
        with self.assertRaises(ValueError):
            numbered_frames(self.root)

    def test_reject_wrong_canvas_mode_and_oversize(self):
        paths = self.frames(2)
        for mode, size in [('RGB', (16, 12)), ('RGBA', (17, 12)), ('RGBA', (513, 12))]:
            with self.subTest(mode=mode, size=size):
                Image.new(mode, size).save(paths[1])
                with self.assertRaises(ValueError):
                    sheet_pack(paths, self.root / 'atlas.png')

    def test_reject_empty_invalid_parameters_and_overwrite(self):
        paths = self.frames(1)
        for kwargs in [{'columns': 0}, {'columns': True}, {'fps': 0}, {'fps': float('nan')}, {'pivot': (1, float('inf'))}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                sheet_pack(paths, self.root / 'atlas.png', **kwargs)
        with self.assertRaises(ValueError):
            sheet_pack([], self.root / 'atlas.png')
        with self.assertRaises(ValueError):
            sheet_pack(paths, paths[0])


if __name__ == '__main__':
    unittest.main()
