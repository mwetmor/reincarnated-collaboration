from gates.g6_seam import evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_bad_closure_and_distinct_comparators(self):
        frames=[Image.new('RGBA',(8,8),(v,v,v,255)) for v in (0,1,10,2)]
        a,b=evaluate(frames)
        self.assertFalse(a['passed']);self.assertTrue(b['passed'])
        self.assertEqual(a['threshold'],1);self.assertEqual(b['threshold'],8)
        self.assertTrue(all(r['passed'] is None for r in evaluate([])))
