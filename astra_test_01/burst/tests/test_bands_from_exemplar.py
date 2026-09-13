from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
from oracle.bands_from_exemplar import propose, score, frame_digest, facing_rows, main


class Tests(unittest.TestCase):
    def setUp(self):
        base=Path(__file__).resolve().parent/'tmp';base.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base,prefix='t3c_bands_');self.path=Path(self.temp.name)
        a=np.zeros((512,512,4),np.uint8);a[160:400,220:290]=(150,100,80,255)
        for i in range(3):Image.fromarray(a).save(self.path/f'frame_{i:02}.png')
    def tearDown(self):self.temp.cleanup()
    def test_actual_static_exemplar_and_bad_value(self):
        row=propose('idle',self.path,'test',8,'S')
        self.assertTrue(row['proposed']);self.assertFalse(row['committed'])
        self.assertEqual(len(row['quantities']),9)
        for b in row['quantities'].values():
            self.assertEqual(b,dict(value=0.,target=0.,floor=0.,ceiling=0.))
        actual={k:b['value'] for k,b in row['quantities'].items()}
        checks=score(actual,row)
        self.assertTrue(all(json.loads(c['notes'])['inside'] for c in checks))
        self.assertTrue(all(c['passed'] is None for c in checks))
        actual['breath_amplitude_H']=1.
        self.assertFalse(json.loads(score(actual,row)[0]['notes'])['inside'])
    def test_hash_order_and_missing_never_zero(self):
        paths=sorted(self.path.glob('*.png'))
        expected=hashlib.sha256(''.join(hashlib.sha256(p.read_bytes()).hexdigest() for p in paths).encode()).hexdigest()
        self.assertEqual(frame_digest(self.path),expected)
        with patch('oracle.bands_from_exemplar.measure',return_value=({'W6':None,'W1':.02},{})):
            row=propose('walk',self.path,'test',12,'E')
        self.assertIn('W6',row['unmeasured']);self.assertNotIn('W6',row['quantities'])
        self.assertEqual(row['quantities']['W1']['floor'],.012)
    def test_facing_copies_keep_old_rows(self):
        old={s:dict(committed=True,bands={'W3a':{'value':.2}}) for s in ('plate13_rear','plate13_front')}
        before=deepcopy(old);east=dict(proposed=True,committed=False,quantities={'W1':{'value':.02}})
        rows=facing_rows(east,old)
        self.assertEqual(old,before)
        self.assertEqual(rows['walk_N_proposal']['bands'],old['plate13_rear']['bands'])
        self.assertEqual(rows['walk_S_proposal']['proposed_from'],'muybridge')
        self.assertTrue(all(r['proposed'] and not r['committed'] for r in rows.values()))
        rows['walk_W_video']['quantities']['W1']['value']=8
        self.assertEqual(east['quantities']['W1']['value'],.02)
    def test_cli_and_invalid(self):
        out=self.path/'proposal.json'
        main(['--kind','idle','--frames',str(self.path),'--label','static','--fps','8','--out',str(out)])
        self.assertIn('static',json.loads(out.read_text()))
        with self.assertRaises(ValueError):propose('idle',self.path,'bad',0)
        with self.assertRaises(ValueError):propose('idle',self.path,'bad',8,'Q')
