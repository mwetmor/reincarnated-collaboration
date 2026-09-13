import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image
from gates.coherence import evaluate


class Tests(unittest.TestCase):
    def setUp(self):
        base=Path(__file__).resolve().parent/'tmp';base.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base,prefix='t3c_coherence_')
        self.path=Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def save(self,frames):
        for i,f in enumerate(frames): Image.fromarray(f).save(self.path/f'frame_{i:02}.png')
        return self.path
    def block(self):
        a=np.zeros((96,96,4),np.uint8)
        a[25:65,25:65,:3]=np.random.default_rng(1).integers(30,230,(40,40,3),dtype=np.uint8)
        a[25:65,25:65,3]=255
        return a
    def test_translated_block_carried(self):
        a=self.block();b=np.roll(a,(3,4),(0,1))
        r=evaluate(self.save([a,b]),{'head':[15,15,78,78]})
        v=r['value']['head'];self.assertEqual(v['classification'],'carried')
        self.assertEqual(v['max_residual_mad'],0)
        self.assertEqual(v['pairs'][0]['translation_xy'],[4,3]);self.assertIsNone(r['passed'])
    def test_retextured_block_redrawn_and_worst_pair(self):
        a=self.block();b=a.copy();b[25:65,25:65,:3]=np.random.default_rng(7).integers(30,230,(40,40,3),dtype=np.uint8)
        r=evaluate(self.save([a,a,b]),{'head':[20,20,70,70]})
        v=r['value']['head'];self.assertEqual(v['classification'],'redrawn')
        self.assertEqual(v['worst_pair'],[1,2]);self.assertGreater(v['max_residual_mad'],.5*v['raw_mad_at_max_residual'])
        json.dumps(r,allow_nan=False)
    def test_noise_static_and_bad_input(self):
        a=self.block();r=evaluate(self.save([a,a]),{'feet':[20,20,70,70]})
        self.assertEqual(r['value']['feet']['classification'],'carried')
        with self.assertRaises(ValueError): evaluate(self.path,{'bad':[-1,0,5,5]})
        with self.assertRaises(ValueError): evaluate(self.path,{})
