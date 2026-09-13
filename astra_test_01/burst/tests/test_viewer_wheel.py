"""T3f portable wheel and known-bad paths/metadata."""
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from review.encode import encode_loop
from review.viewer_wheel import build_viewer, validate_viewer

TMP = Path(__file__).resolve().parent/'tmp'


class ViewerWheelTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='t3f-wheel-', dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cells = self.root/'cells';self.cells.mkdir()

    def cell(self, anim='walk', count=2):
        folder = self.cells/(anim+'_E');folder.mkdir()
        for i in range(count):
            Image.new('RGBA', (512, 512), (50+i, 70, 90, 255)).save(folder/f'{anim}_E_{i:02d}.png')
        return folder

    def data(self, out):
        text = (out/'index.html').read_text()
        marker = '<script id="cell-data" type="application/json">'
        return json.loads(text.split(marker)[1].split('</script>')[0])

    def test_two_cells_numbers_missing_reason_local_assets_and_buttons(self):
        walk = self.cell();self.cell('idle', 1)
        numbers = [{'id':'metric', 'value':2, 'passed':None, 'proposed':True}]
        (walk/'numbers.json').write_text(json.dumps(numbers))
        (walk/'registration.json').write_text('{"fps":24,"fps_out":10}')
        (self.cells/'missing.json').write_text('{"cast_N":{"reason":"Awaiting approved cut"}}')
        out = self.root/'viewer';report = build_viewer(self.cells, out)
        data = self.data(out)
        self.assertEqual(report['cells'], ['idle_E', 'walk_E'])
        self.assertEqual(report['missing_cells'], 38)
        self.assertEqual(data['walk_E']['numbers'], numbers)
        self.assertEqual(data['walk_E']['fps'], 10)
        self.assertEqual(data['idle_E']['fps'], 8)
        self.assertEqual(data['cast_N']['reason'], 'Awaiting approved cut')
        self.assertEqual(len(validate_viewer(out/'index.html')), 5)
        text = (out/'index.html').read_text()
        self.assertEqual(text.count('<button data-dir='), 8)
        self.assertEqual(text.count('<button data-anim='), 5)
        self.assertIn('<li>idle_E', text);self.assertIn('<li>walk_E', text)
        self.assertNotIn('fetch(', text)
        self.assertNotIn('https://', text)
        for path in data['walk_E']['frames']:
            self.assertEqual((out/path).read_bytes(), (walk/Path(path).name).read_bytes())

    def test_packet_only_mp4_prefers_1to1_and_retains_numbers(self):
        packet = self.cells/'packet';packet.mkdir()
        encode_loop([Image.new('RGBA', (16, 16))], 12, packet/'walk_E_1to1.mp4', scale=1, loops=1)
        (packet/'walk_E_2x.mp4').write_bytes((packet/'walk_E_1to1.mp4').read_bytes())
        (packet/'numbers.json').write_text('[{"value":3,"passed":null}]')
        out = self.root/'viewer';build_viewer(self.cells, out)
        data = self.data(out)['walk_E']
        self.assertTrue(data['video'].endswith('walk_E_1to1.mp4'))
        self.assertEqual(data['fps'], 12)
        self.assertEqual(data['frames'], [])
        self.assertEqual(data['numbers'], [{'value':3,'passed':None}])
        self.assertEqual(len(validate_viewer(out/'index.html')), 2)

    def test_script_injection_escaped_and_values_preserved(self):
        folder = self.cell()
        payload = '</script><script>alert(1)</script>'
        (folder/'numbers.json').write_text(json.dumps({'notes':payload}))
        (self.cells/'missing.json').write_text(json.dumps({'idle_N':payload}))
        out = self.root/'viewer';build_viewer(self.cells, out)
        self.assertNotIn(payload, (out/'index.html').read_text())
        self.assertEqual(self.data(out)['walk_E']['numbers']['notes'], payload)

    def test_external_escaping_and_missing_embedded_references_rejected(self):
        self.cell()
        out = self.root/'viewer';build_viewer(self.cells, out)
        path = out/'index.html';original = path.read_text()
        good = self.data(out)['walk_E']['frames'][0]
        for bad in ('https://example.invalid/a.png', '../escape.png', '/absolute.png',
                    'cells/missing.png', '%2e%2e/escape.png'):
            with self.subTest(reference=bad):
                path.write_text(original.replace(good, bad))
                with self.assertRaises(ValueError):
                    validate_viewer(path)

    def test_invalid_missing_conflicting_present_and_nan_numbers_rejected(self):
        folder = self.cell()
        for missing in ({'unknown_N':'missing'}, {'idle_N':''}, {'walk_E':'missing'}, []):
            with self.subTest(missing=missing):
                (self.cells/'missing.json').write_text(json.dumps(missing))
                with self.assertRaises(ValueError):
                    build_viewer(self.cells, self.root/'viewer')
        (self.cells/'missing.json').unlink()
        (folder/'numbers.json').write_text('{"value":NaN}')
        with self.assertRaises(ValueError):
            build_viewer(self.cells, self.root/'viewer')

    def test_empty_matrix_has_explicit_reasons(self):
        out = self.root/'viewer';report = build_viewer(self.cells, out)
        self.assertEqual(report['missing_cells'], 40)
        self.assertTrue(all(entry['reason'] for entry in self.data(out).values()))


if __name__ == '__main__':
    unittest.main()
