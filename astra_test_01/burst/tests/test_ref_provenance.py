import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from lane import ref_provenance,run_burst

class Tests(unittest.TestCase):
    def test_first_party_and_symlink_escape(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'tmp') as td:
            root=Path(td).resolve();astra=root/'astra';astra.mkdir();outside=root/'outside.png';outside.write_bytes(b'fixture')
            with patch.object(ref_provenance,'ASTRA_ROOT',astra):
                for name in ['burst/runs/C-1/artifacts/b/image.png','run_03/frames/image.png',
                             'design/experiments/E01/image.png','burst/fixtures/image.png']:
                    p=astra/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
                    self.assertTrue(ref_provenance.check(p)[0])
                link=astra/'burst/fixtures/escape.png';link.symlink_to(outside)
                self.assertFalse(ref_provenance.check(link)[0]);self.assertFalse(ref_provenance.check(outside)[0])
                self.assertFalse(ref_provenance.check('/tmp/not-a-reference.png')[0])
                task=dict(text='test',references=[dict(path=str(link),role='style')],image_cap=0,
                          minutes_cap=1,tool_call_cap=1,outputs=[],effort='high',add_dirs=[])
                with self.assertRaisesRegex(ValueError,'reference provenance'):run_burst.validate_task(task,'CHECK')
