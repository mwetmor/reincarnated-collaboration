import tempfile
from pathlib import Path
import unittest


class ModuleTests(unittest.TestCase):
    def test_missing_receipt(self):
        from lane.schema_check import check
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as td:
            self.assertTrue(check(Path(td) / 'missing.json'))
