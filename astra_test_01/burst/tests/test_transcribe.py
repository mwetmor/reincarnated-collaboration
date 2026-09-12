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
