"""T3d packet contract, proposal propagation, isolation, and one-shot timing."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

from review.cell_packet import build_packet, flatten_checks, validate_packet_html
from test_encode import decode, probe

ROOT = Path(__file__).resolve().parents[1]


class CellPacketTests(unittest.TestCase):
    def setUp(self):
        (ROOT/'tests/tmp').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='t3d_packet_', dir=ROOT/'tests/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def cell(self, kind='walk', metadata=None):
        cell = self.root/kind
        frames = cell/'frames'/kind/'E'; frames.mkdir(parents=True)
        for i, value in enumerate((40, 110, 180)):
            Image.new('RGBA', (32, 32), (value,)*3+(255,)).save(frames/f'{kind}_E_{i:02d}.png')
        rest = cell/'frames/rest/E'; rest.mkdir(parents=True)
        Image.new('RGBA', (32, 32)).save(rest/'rest_E.png')
        (cell/'registration.json').write_text(json.dumps(metadata or {'fps': 24}))
        return cell

    def test_proposed_and_uncommitted_never_gain_verdicts(self):
        checks = {'proposed': True, 'quantities': {'bob': {'value': 2, 'floor': 1, 'target': 2, 'ceiling': 3, 'passed': True}}}
        row = flatten_checks(checks)[0]
        self.assertIsNone(row['passed']); self.assertEqual(row['band'], {'floor': 1, 'target': 2, 'ceiling': 3})
        for modifier in ({'committed': False}, {'band': {'proposed': True}}, {'threshold': {'committed': False}}):
            with self.subTest(modifier=modifier):
                self.assertIsNone(flatten_checks({'id': 'q', 'value': 2, 'passed': False, **modifier})[0]['passed'])

    def test_flatten_gate_envelopes_and_unknown(self):
        rows = flatten_checks({'checks': [{'id': 'g6', 'value': 5, 'threshold': 3, 'op': '<=', 'passed': False},
                                          {'name': 'unknown', 'value': None, 'passed': None}]})
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['band']['ceiling'], 3)
        self.assertIs(rows[0]['passed'], False)
        self.assertIsNone(rows[1]['passed'])
        self.assertEqual(flatten_checks([]), [])

    def test_packet_products_local_links_and_default_output_rate(self):
        out = self.root/'packet'
        result = build_packet(self.cell(), [], out)
        self.assertEqual(result['fps'], 12)  # legacy native fps=24 is not playback fps
        self.assertLessEqual(result['wall_s'], 120)
        for filename in ('walk_E_2x.mp4', 'walk_E_1to1.mp4', 'seam_pairs.png', 'strip.png',
                         'numbers.json', 'summary.txt', 'review.html', 'img/seam_pairs.png', 'img/strip.png'):
            self.assertTrue((out/filename).is_file(), filename)
        self.assertEqual(len((out/'summary.txt').read_text().splitlines()), 10)
        self.assertTrue(validate_packet_html(out/'review.html'))
        self.assertEqual(probe(out/'walk_E_1to1.mp4')['width'], 32)
        self.assertEqual(probe(out/'walk_E_2x.mp4')['width'], 64)
        self.assertNotIn('http', (out/'review.html').read_text())
        self.assertNotIn(str(self.root), (out/'review.html').read_text())

    def test_one_shots_full_sequence_then_half_second_hold(self):
        for kind, fps in (('jump', 12), ('cast', 20)):
            with self.subTest(kind=kind):
                out = self.root/f'{kind}_packet'
                result = build_packet(self.cell(kind), [], out)
                self.assertEqual(result['hold_frames'], fps//2)
                pixels = decode(out/f'{kind}_E_1to1.mp4')
                length = 3+fps//2
                self.assertEqual(len(pixels), length*5)
                values = pixels[:, 8:24, 8:24].mean(axis=(1, 2, 3))
                expected = np.array(([40, 110, 180]+[180]*(fps//2))*5)
                self.assertLessEqual(float(np.abs(values-expected).max()), 3)

    def test_oracle_and_cli(self):
        cell = self.cell(metadata={'fps_out': 10})
        oracle = self.root/'oracle'; oracle.mkdir()
        Image.new('RGB', (32, 32), 'white').save(oracle/'00.png')
        checks = self.root/'checks.json'; checks.write_text('[]')
        out = self.root/'cli'
        completed = subprocess.run([sys.executable, '-B', '-m', 'review.cell_packet', '--cell', str(cell),
            '--checks', str(checks), '--oracle', str(oracle), '--oracle-fps', '4', '--out', str(out)],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)['fps'], 10)
        self.assertEqual(probe(out/'oracle.mp4')['r_frame_rate'], '4/1')
        self.assertIn('oracle.mp4', validate_packet_html(out/'review.html'))

    def test_known_bad_cell_and_missing_oracle_rate(self):
        cell = self.cell()
        with self.assertRaises(ValueError):
            build_packet(cell, [], self.root/'bad', oracle=self.root)
        (cell/'frames/walk/E/walk_E_01.png').unlink()
        with self.assertRaises(ValueError):
            build_packet(cell, [], self.root/'bad')
        empty = self.root/'empty'; empty.mkdir()
        with self.assertRaises(ValueError):
            build_packet(empty, [], self.root/'bad')

    def test_known_bad_html_paths_and_symlink(self):
        out = self.root/'html'; out.mkdir()
        page = out/'review.html'
        for ref in ('/absolute.png', 'https://example.org/a.png', '//example.org/a', '../escape.png',
                    '%2e%2e/escape.png', 'file:foo.png', 'missing.png', r'..\escape.png'):
            with self.subTest(ref=ref):
                page.write_text('<img src="'+ref+'">')
                with self.assertRaises(ValueError):
                    validate_packet_html(page)
        external = self.root/'escape.png'; external.write_bytes(b'x')
        (out/'linked.png').symlink_to(external)
        page.write_text('<img src="linked.png">')
        with self.assertRaises(ValueError):
            validate_packet_html(page)

    def test_measurement_html_is_escaped(self):
        out = self.root/'escaped'
        build_packet(self.cell(), [{'id': '<script src="https://bad/">', 'value': 1, 'passed': None}], out)
        self.assertNotIn('<script', (out/'review.html').read_text())
        validate_packet_html(out/'review.html')


if __name__ == '__main__':
    unittest.main()
