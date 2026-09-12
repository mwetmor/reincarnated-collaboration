import json
from gates.run_gates import run,regression_diff,measurements
from gates_helpers import *
class Tests(TemporaryTest):
    def test_empty_sequence_not_silent_success(self):
        rows=run(self.base,sprite())
        self.assertTrue(any(r['passed'] is False for r in rows))
        self.assertTrue(any(r['passed'] is None for r in rows))
        self.assertEqual(set(rows[0]),{'id','subject','passed','value','threshold','op','unit','evidence','notes'})
    def test_regression_comparator_detects_mutation(self):
        a={'directions':{'S':{'animations':{'idle':{'available':0,'frames':[]}}}}}
        b={'directions':{'S':{'animations':{'idle':{'available':1,'frames':[]}}}}}
        self.assertTrue(regression_diff(a,b)['differences'])
