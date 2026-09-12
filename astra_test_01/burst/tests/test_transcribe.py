from transcribe.questions import from_bible,schema_from_bible
from lane.schema_check import validate
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_atomic_unique_dependency_ordered_absent_controls(self):
        b=stub();q=from_bible(b);seen=set()
        self.assertTrue(any(x['declared_absent_control'] for x in q))
        for x in q:
            self.assertNotIn(x['id'],seen);self.assertTrue(set(x['depends_on'])<=seen);seen.add(x['id'])
        self.assertEqual(len(q),2*len(b['PARTS']))
        b['RULE'][0]['exclusions']=[]
        with self.assertRaises(ValueError):from_bible(b)
    def test_strict_schema_no_coordinates_or_open_vocabulary(self):
        schema=json.loads((ROOT/'transcribe.schema.json').read_text())
        self.assertEqual(schema,json.loads((ROOT/'transcribe/transcribe.schema.json').read_text()))
        def check(s):
            if s['type']=='object':
                self.assertFalse(s['additionalProperties']);self.assertEqual(set(s['required']),set(s['properties']))
                for child in s['properties'].values():check(child)
        check(schema)
        answers={p['name']:{'present':False,'count':0} for p in stub()['PARTS']}
        self.assertFalse(validate(answers,schema));answers['hair']['x']=4;self.assertTrue(validate(answers,schema))
        del answers['hair']['x'];answers['unknown']={'present':True,'count':1};self.assertTrue(validate(answers,schema))

    def test_separate_part_inventory(self):
        from transcribe.questions import parts_from_bible,parts_questions,parts_schema
        b=stub();q=parts_from_bible(b);closed=[p['name'] for p in b['PARTS']]+b['controls']['declared_absent_parts']
        self.assertEqual(len(q),2*len(closed));seen=set()
        for item in q:
            self.assertNotIn(item['id'],seen);self.assertTrue(set(item['depends_on'])<=seen);seen.add(item['id'])
            if item['declared_absent_control']:
                self.assertIn(item['part'],b['controls']['declared_absent_parts'])
                self.assertEqual(item['expected'],False if item['predicate']=='present' else 0)
        other=parts_questions(['coat','rifle'],['helmet','staff'])
        self.assertEqual([x['part'] for x in other[::2]],['coat','rifle','helmet','staff'])
        schema=parts_schema(['coat','rifle'],['helmet','staff'])
        a={p:{'present':False,'count':0} for p in schema['required']}
        self.assertEqual(validate(a,schema),[]);del a['staff'];self.assertTrue(validate(a,schema))
        with self.assertRaises(ValueError):parts_questions(['coat','coat'],['helmet'])
