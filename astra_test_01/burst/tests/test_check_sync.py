import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from lane import check_sync


class ModuleTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent / 'tmp')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.source = self.root / 'source.txt'
        self.source.write_text('source')
        self.stamp = hashlib.sha256(self.source.read_bytes()).hexdigest()[:12]
        self.doc = self.root / 'doc.md'
        self.text = ('## 6. Other\n| `ignored` | ignored | 000000000000 | 2026-09-11 |\n'
                     '## 7. SYNC\n| Source | Role | sha256[:12] | Reconciled |\n|---|---|---|---|\n'
                     f'| `{self.source}` (source note) | fixture | {self.stamp} | 2026-09-11 |\n'
                     '## 8. Other\n| `ignored` | ignored | 000000000000 | 2026-09-11 |\n')
        self.doc.write_text(self.text)

    def cli(self, *args):
        return subprocess.run([sys.executable, '-B', str(Path(check_sync.__file__)), '--doc', str(self.doc), *args], capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))

    def test_all_ok_and_parenthetical(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f'OK {self.stamp} {self.stamp} {self.source}\n')
        self.assertEqual(self.doc.read_text(), self.text)
        result = self.cli('--json')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), [dict(status='OK', stamped=self.stamp, actual=self.stamp, path=str(self.source))])

    def test_stale_row(self):
        self.source.write_text('changed')
        result = self.cli('--json')
        self.assertEqual(result.returncode, 1)
        row = json.loads(result.stdout)[0]
        self.assertEqual(row['status'], 'DRIFT')
        self.assertNotEqual(row['actual'], row['stamped'])

    def test_unreadable_source(self):
        self.source.unlink()
        result = self.cli('--json')
        self.assertEqual(result.returncode, 1)
        row = json.loads(result.stdout)[0]
        self.assertEqual(row['status'], 'DRIFT')
        self.assertEqual(row['actual'], 'UNREADABLE')
        self.assertIn('error', row)

    def test_parse_failures(self):
        for bad in ['', self.text.replace('## 7.', '## 9.'), self.text.replace(self.stamp, 'bad-hash'), self.text.replace(' (source note)', ' bad suffix')]:
            with self.subTest(bad=bad):
                self.doc.write_text(bad)
                result = self.cli('--json')
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout), [])
                self.assertIn('parse error', result.stderr)

    def test_relative_and_tilde_resolution(self):
        for name in ['source.txt', '~/source.txt']:
            with self.subTest(name=name), patch.object(check_sync, 'REPO', self.root), patch.dict(os.environ, {'HOME': str(self.root)}):
                self.doc.write_text(self.text.replace(str(self.source), name))
                self.assertEqual(check_sync.check(self.doc)[0]['status'], 'OK')
        self.assertEqual(check_sync.REPO, Path(check_sync.__file__).resolve().parents[3])
