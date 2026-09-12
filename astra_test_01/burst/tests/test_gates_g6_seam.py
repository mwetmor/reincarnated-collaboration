from gates.g6_seam import evaluate
from gates_helpers import *
class Tests(unittest.TestCase):
    def test_bad_closure_and_distinct_comparators(self):
        frames=[Image.new('RGBA',(8,8),(v,v,v,255)) for v in (0,1,10,2)]
        a,b=evaluate(frames)
        self.assertFalse(a['passed']);self.assertTrue(b['passed'])
        self.assertEqual(a['threshold'],1);self.assertEqual(b['threshold'],8)
        self.assertTrue(all(r['passed'] is None for r in evaluate([])))

    def test_half_cycle_homologue_and_broken_seam(self):
        from gates.g6_seam import g6c
        frames=[Image.new('RGBA',(8,8),(v,v,v,255)) for v in (10,20,30,10,20,30)]
        legacy=evaluate(frames)
        r=g6c(frames);self.assertAlmostEqual(r['value'],1.)
        self.assertTrue(r['passed']);self.assertEqual(evaluate(frames),legacy)
        frames[-1]=Image.new('RGBA',(8,8),(100,100,100,255))
        bad=g6c(frames);self.assertGreater(bad['value'],1.25);self.assertFalse(bad['passed'])

    def test_g6c_idle_zero_and_invalid(self):
        from gates.g6_seam import g6c
        frames=[Image.new('RGBA',(8,8),(v,v,v,255)) for v in (0,1,10,2)]
        idle=g6c(frames,animation='idle');b=evaluate(frames)[1]
        self.assertEqual((idle['value'],idle['threshold'],idle['passed']),(b['value'],b['threshold'],b['passed']))
        self.assertIsNone(g6c(frames[:3])['passed'])
        equal=[frames[0]]*4;self.assertEqual(g6c(equal)['value'],1.)
        equal[-1]=frames[-1];r=g6c(equal)
        self.assertIsNone(r['value']);self.assertFalse(r['passed'])
