import json
import numpy as np
from PIL import Image
from gates.gait_intent import evaluate
from gates_helpers import TemporaryTest
from test_oracle_walk import synthetic_otsu_lineage


def walk_row(committed=True):
    phase=[dict(frame=i,phase=['CONTACT','DOWN','DOWN','PASSING','PASSING','UP'][i%6],
                planted={'L':i<6,'R':i>=6}) for i in range(12)]
    return dict(committed=committed,phase_table=phase,bands={
        'W1':dict(floor=.02,target=.03,ceiling=.07),
        'W2':dict(min=[dict(frame=i,phase='DOWN') for i in (1,2,7,8)],
                  max=[dict(frame=i,phase='PASSING' if i%6==4 else 'UP') for i in (4,5,10,11)]),
        'W5_role_limits':dict(assignment={'L':'free_arm','R':'weapon_arm'}),
        'planted_sole_slip':dict(ceiling=1.)})


class Tests(TemporaryTest):
    def save(self,floating=False):
        path=self.base/('floating' if floating else 'walk');path.mkdir(exist_ok=True)
        for i,f in enumerate(synthetic_otsu_lineage(floating=floating)):
            a=np.zeros((512,512,4),np.uint8)
            a[:360,:300,:3]=f;a[:360,:300,3]=np.any(f!=30,axis=2)*255
            Image.fromarray(a).save(path/f'frame_{i:02}.png')
        return path

    def test_all_w_quantities_evaluated(self):
        row=walk_row();r=evaluate(self.save(),row,row['phase_table']);by={v['id']:v for v in r}
        self.assertEqual(by['W4']['value'],2)
        self.assertGreaterEqual(by['W6']['value'],.75)
        for key in ('W1_floor','W1_ceiling','W2','W3a','W3c_floor','W3c_ceiling','W4','W5_L_floor','W5_R_floor','W6','planted_sole_slip_L','planted_sole_slip_R'):
            self.assertIsNotNone(by[key]['value'],key)
        self.assertTrue(by['W2']['passed'],by['W2'])
        json.dumps(r,allow_nan=False)

    def test_bad_bob_phase_and_provisional(self):
        row=walk_row();path=self.save(True);r=evaluate(path,row,row['phase_table'])
        self.assertFalse(next(v for v in r if v['id']=='W1_floor')['passed'])
        row['committed']=False
        self.assertTrue(all(v['passed'] is None for v in evaluate(path,row,row['phase_table'])))
        row=walk_row();phases=[dict(p) for p in row['phase_table']];phases[1]['phase']='UP'
        r=evaluate(self.save(),row,phases)
        self.assertFalse(next(v for v in r if v['id']=='W2')['passed'])

    def test_unassigned_role_and_slip_threshold_are_null(self):
        row=walk_row();row['bands'].pop('W5_role_limits');row['bands'].pop('planted_sole_slip')
        r=evaluate(self.save(),row,row['phase_table']);by={v['id']:v for v in r}
        self.assertIsNone(by['W5_L']['passed']);self.assertIsNotNone(by['W5_L']['value'])
        self.assertIsNone(by['planted_sole_slip_R']['passed'])
