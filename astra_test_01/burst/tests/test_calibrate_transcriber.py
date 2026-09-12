import copy
from compare.calibrate_transcriber import score
from oracles_helpers import *
class Tests(unittest.TestCase):
    def setUp(self):
        self.hand={'coat':{'present':True,'count':1},'belt':{'present':True,'count':1},
                   'helmet':{'present':False,'count':0}}
    def test_perfect(self):
        row=score(self.hand,[self.hand]);m=metrics(row)
        self.assertTrue(row['passed']);assert_envelope(self,row)
        self.assertEqual(m['aggregate']['presence_precision'],1)
        self.assertEqual(m['aggregate']['presence_recall'],1)
        self.assertEqual(m['aggregate']['control_catch_rate'],1)
        self.assertIsNone(score(self.hand,[])['passed'])
    def test_control_present_and_false_zero(self):
        for present,count in [(True,1),(False,1),(True,0)]:
            a=copy.deepcopy(self.hand);a['helmet']={'present':present,'count':count}
            r=score(self.hand,[a]);self.assertFalse(r['passed'])
            self.assertEqual(metrics(r)['aggregate']['control_catch_rate'],0)
    def test_count_off_by_two_and_disagreement(self):
        a=copy.deepcopy(self.hand);a['coat']['count']=3
        r=score(self.hand,[a]);self.assertFalse(r['passed'])
        self.assertAlmostEqual(metrics(r)['aggregate']['count_within_one_fraction'],2/3)
        self.assertEqual(metrics(r)['per_part_disagreement']['coat']['counts_outside_tolerance'],1)
    def test_missing_or_open_inventory(self):
        with self.assertRaises(ValueError):score(self.hand,[{'coat':self.hand['coat']}])
        a=copy.deepcopy(self.hand);a['coat']['x']=4
        with self.assertRaises(ValueError):score(self.hand,[a])

    def test_cli_roundtrip_and_named_thresholds(self):
        import tempfile,subprocess,sys
        with tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp') as td:
            root=Path(td);hand=root/'hand.json';answer=root/'answer.json';out=root/'score.json'
            hand.write_text(json.dumps(self.hand));answer.write_text(json.dumps(self.hand))
            subprocess.run([sys.executable,'-B',str(ROOT/'compare/calibrate_transcriber.py'),
                '--hand',str(hand),'--answers',str(answer),'--out',str(out)],check=True)
            row=json.loads(out.read_text());self.assertTrue(row['passed'])
            self.assertTrue(metrics(row)['per_burst'][0]['passed'])
            self.assertTrue(metrics(row)['aggregate']['passed'])
        a=copy.deepcopy(self.hand);a['coat']['count']=3
        self.assertTrue(score(self.hand,[a],count_tolerance=2)['passed'])
