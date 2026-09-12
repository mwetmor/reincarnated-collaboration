import unittest
from lane.run_burst import validate_task


class ModuleTests(unittest.TestCase):
    def test_incomplete_task_rejected(self):
        with self.assertRaises(ValueError):
            validate_task({'text': 'incomplete'}, 'CHECK')
