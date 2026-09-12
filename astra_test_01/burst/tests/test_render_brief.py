import tempfile
from pathlib import Path
import unittest


class ModuleTests(unittest.TestCase):
    def test_missing_type_rules(self):
        from lane.render_brief import render
        with self.assertRaises(ValueError):
            render({}, 'bogus')
