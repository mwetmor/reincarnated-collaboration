import tempfile
from pathlib import Path
import unittest


class ModuleTests(unittest.TestCase):
    def test_empty_budget(self):
        from lane.ledger import empty
        a, b = empty(), empty()
        a['bursts'].append({})
        self.assertEqual(b['bursts'], [])
        self.assertEqual(b['images_cap'], 250)

    def test_provenance_and_authoritative_image_budget(self):
        from unittest.mock import patch
        from lane import ledger
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent / 'tmp') as td, patch.object(ledger, 'ROOT', Path(td)):
            entry = dict(id='one', image_calls=1, image_calls_events=7,
                         generated_images_new=[dict(path='/generated/one.png', sha256='a'*64)],
                         model='gpt-6-astra', model_source='profile', effort='high',
                         codex_version='codex test', profile_sha256='b'*64,
                         artifacts_in_place=[dict(root='/declared', name='tool.py', sha256='c'*64)])
            data = ledger.append('test', entry)
            self.assertEqual(data['bursts'], [entry])
            self.assertEqual(data['images_used'], 1)
            for value in [-1, True, 1.5, '1']:
                with self.subTest(value=value), self.assertRaises(ValueError):
                    ledger.append('test', dict(id='bad', image_calls=value))
            with self.assertRaises(ValueError):
                ledger.append('test', entry)
            import json
            stored = json.loads((Path(td)/'runs/test/ledger.json').read_text())
            self.assertEqual(stored, data)
