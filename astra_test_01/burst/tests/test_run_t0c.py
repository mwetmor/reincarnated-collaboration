"""BL-2v-b: setup errors/skips must replace a stale suite summary."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from run_t0c import result_summary, write_summary


class SuiteSummaryTests(unittest.TestCase):
    def test_forced_setup_error_and_skip_holders_rewrite_summary(self):
        class Broken(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                raise RuntimeError('forced setup error')
            def test_unreachable(self):
                self.fail('setup should prevent this body')
        class Skipped(unittest.TestCase):
            @classmethod
            def setUpClass(cls):
                raise unittest.SkipTest('forced setup skip')
            def test_unreachable(self):
                self.fail('setup should prevent this body')
        suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
                                   for c in (Broken, Skipped))
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream).run(suite)
        self.assertFalse(result.wasSuccessful())
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(len(result.skipped), 1)
        self.assertIn('forced setup error', stream.getvalue())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'t0c_summary.json'
            path.write_text('{"stale":true}')
            write_summary(path, result_summary(result, 0))
            data = json.loads(path.read_text())
        self.assertNotIn('stale', data)
        self.assertIn('setUpClass', data['errors'][0]['test'])
        self.assertIn('forced setup error', data['errors'][0]['traceback'])
        self.assertIn('setUpClass', data['skipped'][0][0])
        self.assertEqual(data['skipped'][0][1], 'forced setup skip')

    def test_identifier_falls_back_to_string(self):
        result = unittest.TestResult()
        result.skipped.append(('holder without id method', 'reason'))
        self.assertEqual(result_summary(result, 0)['skipped'],
                         [('holder without id method', 'reason')])
