import tempfile
from pathlib import Path
import unittest


class ModuleTests(unittest.TestCase):
    def test_missing_event_log(self):
        from lane.audit import audit
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent / "tmp") as td:
            root = Path(td).resolve()
            result = audit(root / 'missing', root, {'roots': [str(root)], 'files': {}}, {'image_cap': 0, 'tool_call_cap': 0}, 'CHECK')
            self.assertTrue(result['violations'])
