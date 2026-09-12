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
