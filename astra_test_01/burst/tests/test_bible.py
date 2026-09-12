import copy
from bible.validate import validate
from oracles_helpers import *
class Tests(unittest.TestCase):
    def test_stub_and_v01_fields(self):
        b=stub();self.assertEqual(validate(b),[])
        self.assertEqual(set(b),{'RULE','PILLARS','PALETTE','PARTS','CONSTRUCTION','LIGHT','SCALE'})
        self.assertEqual(len([r for r in b['RULE'] if r['class']=='motif']),1)
        self.assertEqual(b['LIGHT']['key_azimuth_deg'],135)
        self.assertEqual(b['SCALE']['canvas_px'],512)
        self.assertEqual([p['name'] for p in b['PARTS']],['hair','face','shirt','tabard','belt','satchel','pauldron_L','pauldron_R','bracers','trousers','boots','rod','rod_head'])
    def test_known_bad_schema_constraints(self):
        original=stub()
        for mutate in [lambda b:b['PILLARS'].pop(),lambda b:b['PARTS'][0].update(rigidity='stone'),lambda b:b.update(extra=1),lambda b:b['PALETTE']['swatches'].append('blue'),lambda b:b['LIGHT'].update(fill_ratio='unknown'),lambda b:b['RULE'][0]['placements'][0].update(count=-1),lambda b:b['SCALE']['feature_size_px'].update(sigil='tiny')]:
            b=copy.deepcopy(original);mutate(b);self.assertTrue(validate(b))
        b=copy.deepcopy(original);b['CONSTRUCTION']=[{'part':'belt','terminates_at':'tabard','closes':'shirt','statement':'invalid both'}]
        self.assertTrue(validate(b))
