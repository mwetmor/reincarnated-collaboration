import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
from oracle import idle_bands
from gates import gait_intent
from oracles.keylight import azimuth


class Tests(unittest.TestCase):
    def setUp(self):
        base=Path(__file__).resolve().parent/'tmp';base.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base,prefix='t3c_fixes_');self.path=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_ours_explicit_out_and_unchanged_default(self):
        source=self.path/'frames';source.mkdir()
        a=np.zeros((512,512,4),np.uint8);a[160:400,220:290]=(150,100,80,255)
        for i in range(3):Image.fromarray(a).save(source/f'frame_{i:02}.png')
        args=['--ours',str(source),'--label','sample','--fps','8']
        out=self.path/'explicit.json'
        with contextlib.redirect_stdout(io.StringIO()): idle_bands.main(args+['--out',str(out)])
        self.assertEqual(json.loads(out.read_text())['mode'],'ours')
        with patch.object(idle_bands,'_write') as write,contextlib.redirect_stdout(io.StringIO()):idle_bands.main(args)
        self.assertEqual(write.call_args.args[0],idle_bands.OURS_ROOT/'sample_ours.json')
    def test_weak_resultant_null_and_directional_gradient(self):
        y,x=np.mgrid[:81,:81];r=((x-40)**2+(y-40)**2)
        lum=80+100*np.exp(-r/300)+.001*x
        rgb=np.repeat(lum[...,None],3,axis=2)
        alpha=np.ones((81,81),bool)
        weak=azimuth(rgb,alpha)
        note=json.loads(weak['notes']);self.assertLess(note['metrics']['resultant'],.05)
        self.assertIsNone(note['metrics']['azimuth']);self.assertIsNone(weak['value'])
        self.assertIn('below_min_resultant',note['reason'])
        strong=azimuth(np.repeat((200-x-y)[...,None],3,axis=2),alpha,tolerance=5)
        self.assertAlmostEqual(json.loads(strong['notes'])['metrics']['azimuth_deg'],135)
        self.assertIsNotNone(azimuth(rgb,alpha,min_resultant=0)['value'])
    def test_near_far_roles_and_proposed_null(self):
        f=self.path/'frame_00.png';Image.new('RGBA',(512,512),(50,80,100,255)).save(f)
        summary=dict(W1=.03,W3a=.2,W3c=2,W4=2,W5={'near':.04,'far':.12},W6=.8,H_median=240,
                     W6_per_arm={'near':.8,'far':.8},sole_scroll={})
        seq=[dict(head_top_y=100+i%3) for i in range(12)]
        row=dict(committed=True,arm_roles={'weapon_arm':'near','free_arm':'far'})
        with patch.object(gait_intent,'alpha_box'),patch.object(gait_intent,'frame_paths',return_value=[f]*12),patch.object(gait_intent,'track_landmarks_otsu_stance_lineage',return_value=seq),patch.object(gait_intent,'measure_sequence',return_value=dict(summary=summary,phase_table=[])):
            by={r['id']:r for r in gait_intent.evaluate(self.path,row,[None]*12)}
            self.assertEqual(by['W5_near_floor']['value'],.04)
            self.assertEqual(by['W5_far_ceiling']['value'],.12)
            self.assertNotIn('W5_L',by)
            row['proposed']=True
            self.assertTrue(all(r['passed'] is None for r in gait_intent.evaluate(self.path,row,[None]*12)))
