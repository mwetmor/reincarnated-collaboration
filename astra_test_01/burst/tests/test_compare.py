from compare.compare_to_bible import compare_answers,compare_to_bible
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_control_claim_and_invalid_answers(self):
        b=stub();a={p['name']:{'present':False,'count':0} for p in b['PARTS']}
        self.assertTrue(compare_answers(b,a)['passed'])
        a['boots']={'present':True,'count':1}
        self.assertFalse(compare_answers(b,a)['passed'])
        a['boots']={'present':False,'count':-1};self.assertIsNone(compare_answers(b,a)['passed'])
        a['boots']={'present':False,'count':0,'bbox':[0,0,1,1]};self.assertIsNone(compare_answers(b,a)['passed'])
    def test_template_count_crosscheck(self):
        from oracles.common import report
        b=stub();a={p['name']:{'present':False,'count':0} for p in b['PARTS']}
        measured=report('O3','',0,0,metrics={'inside':1,'outside':0})
        self.assertFalse(compare_answers(b,a,motif_measurement=measured)['passed'])
    def compare_fixture(self,name,allowed):
        _,kw=fixture_params()
        return compare_to_bible(FIXTURES/f'{name}.png',stub(),template_rgb=FIXTURES/'sigil_template.png',allowed_masks=allowed,**kw)
    def test_stub_rejects_f04_crop(self):
        """SPEC verbatim: compare_to_bible with the stub FAILS the F04 crop."""
        manifest,_=fixture_params();r=self.compare_fixture('f04_advanced_crop',[manifest['sigil_template']['bbox_in_advanced_crop']])
        self.assertIs(r['passed'],False,r)
    def test_stub_accepts_clean_crop(self):
        """SPEC verbatim: compare_to_bible with the stub PASSES the clean crop."""
        self.assertIs(self.compare_fixture('clean_crop',[])['passed'],True)
    def test_missing_reviewed_masks_is_null(self):
        self.assertIsNone(self.compare_fixture('clean_crop',None)['passed'])

    def test_anatomical_controls(self):
        b=stub();a={p['name']:{'present':True,'count':1} for p in b['PARTS']}
        a.update({p:{'present':False,'count':0} for p in b['controls']['declared_absent_parts']})
        self.assertTrue(compare_answers(b,a)['passed'])
        for present,count in [(True,1),(False,1),(True,0)]:
            a['helmet']={'present':present,'count':count}
            self.assertFalse(compare_answers(b,a,question_set='parts')['passed'])
        del a['helmet'];self.assertIsNone(compare_answers(b,a,question_set='parts')['passed'])

    def test_either_instrument_violates_both_mode(self):
        from unittest.mock import patch
        from oracles.common import report
        _,kw=fixture_params()
        for tv,fv in [(0,1),(1,0),(1,1)]:
            with patch('compare.compare_to_bible.count_instances',return_value=report('O3','',tv,0)), patch('compare.compare_to_bible.count_family',return_value=report('O3b','',fv,0)):
                r=compare_to_bible(sprite(),stub(),template_rgb=sprite(),allowed_masks=[],**kw)
                self.assertFalse(r['passed']);self.assertEqual(r['value'],1)
