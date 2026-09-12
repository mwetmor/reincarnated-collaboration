"""Known-truth 12-phase walker and explicit bad/ambiguous input controls."""
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image,ImageDraw
from oracle.walk_landmarks import figure_mask,figure_mask_row,landmarks,track_landmarks,track_head,_translate
from oracle.walk_curves import measure_sequence,head_path,bob,phase_table,curves
from oracle.walk_bands import main,bands
ROOT=Path(__file__).resolve().parents[1]


def synthetic_otsu_lineage(grid=False,floating=False):
    frames=[]
    for i in range(12):
        a=Image.new('RGB',(300,360),(30,30,30));d=ImageDraw.Draw(a)
        if grid:
            for x in range(0,300,17): d.line((x,0,x,359),fill=(150,150,150))
            for y in range(0,360,17): d.line((0,y,299,y),fill=(150,150,150))
        # Six-phase bob: low Cartesian-up head at offsets 1/2 (DOWN).
        # Quantized 7px peak-to-peak / median H~241 = 2.90%H.
        shift=0 if floating else [0,4,4,0,-3,-3][i%6]
        hx=round(3*np.sin(2*np.pi*i/12))
        color=(220,220,220)
        d.rectangle((137+hx,60+shift,163+hx,87+shift),fill=color)
        d.rectangle((145,80,155,112),fill=color)
        d.rectangle((129,107,171,222),fill=color)
        # Legs remain distinct below .75H; track L and R do not cross.
        for side,base,off in [('L',103,i),('R',197,(i+6)%12)]:
            planted=off<6
            dx=round(12-4*off) if planted else round(-8+4*(off-6))
            x=base+dx;y=300 if planted else 290
            d.line((140 if side=='L' else 160,210,x,270),fill=color,width=12)
            d.rectangle((x-7,266,x+7,y),fill=color)
            # Screen signed wrist movement opposes leg dx; at the 0.45H row.
            armx=(106 if side=='L' else 194)-dx
            d.line((130 if side=='L' else 170,120,armx,168),fill=color,width=9)
            d.rectangle((armx-5,157,armx+5,180),fill=color)
        frames.append(np.array(a))
    return frames


def synthetic(grid=False,floating=False):
    """Fixed camera: torso advances 16px/frame, planted soles stay still.

    Swing reaches touchdown x one sample before the ground contact. Background
    occupancy is below half the row, as required by the median estimator.
    """
    frames=[]
    for i in range(12):
        a=Image.new('RGB',(560,360),(30,30,30));d=ImageDraw.Draw(a)
        if grid:
            for x in range(0,560,17):d.line((x,0,x,359),fill=(150,150,150))
            for y in range(0,360,17):d.line((0,y,559,y),fill=(150,150,150))
        shift=0 if floating else [0,4,4,0,-3,-3][i%6]
        ox=16*i;hx=round(3*np.sin(2*np.pi*i/12));color=(220,220,220)
        d.rectangle((137+ox+hx,60+shift,163+ox+hx,87+shift),fill=color)
        d.rectangle((145+ox,80,155+ox,112),fill=color)
        d.rectangle((129+ox,107,171+ox,222),fill=color)
        for side,base,off in [('L',90,i),('R',210,(i+6)%12)]:
            stance=off<6
            dx=40-16*off if stance else [-56,-32,-8,16,40,56][off-6]
            x=base+ox+dx;y=300 if stance else 290
            d.line((ox+(140 if side=='L' else 160),210,x,y-6),fill=color,width=12)
            d.rectangle((x-7,y-8,x+7,y),fill=color)
            armx=ox+(106 if side=='L' else 194)-round(.3*dx)
            d.line((ox+(130 if side=='L' else 170),120,armx,168),fill=color,width=9)
            d.rectangle((armx-5,157,armx+5,180),fill=color)
        frames.append(np.array(a))
    return frames


def tracked(frames):
    masks=figure_mask_row(frames);seq=track_landmarks(masks)
    for d,h in zip(seq,track_head(frames,masks)):d.update(h)
    return seq


class Tests(unittest.TestCase):
    def setUp(self):
        (ROOT/'tests/tmp').mkdir(exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp');self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)

    def test_synthetic_contract_and_grid(self):
        plain=synthetic();grid=synthetic(True)
        seq=tracked(plain);other=tracked(grid)
        for a,b in zip(seq,other):
            for key in ('head_top_y','head_ref_y','head_cx','sole_line_y','torso_cx','foot_L_x','foot_R_x','wrist_ext_L','wrist_ext_R'):
                self.assertIsNotNone(a[key],key);self.assertAlmostEqual(a[key],b[key],delta=2,msg=key)
        measured=measure_sequence(seq);s=measured['summary']
        print('SYNTHETIC_WALK '+json.dumps(s,sort_keys=True))
        self.assertAlmostEqual(s['W1'],.03,delta=.03*.15)
        self.assertTrue(all(p['phase']=='DOWN' for p in s['W2']['min']))
        self.assertEqual(s['W4'],2);self.assertEqual(s['W3c'],2)
        self.assertGreaterEqual(s['W6'],11/12)
        self.assertTrue(all(any(d['planted'].values()) for d in seq))
        self.assertEqual(sum(p['phase']=='CONTACT' for p in measured['phase_table']),2)
        json.dumps(measured,allow_nan=False)

    def test_floating_below_calibrated_floor(self):
        seq=tracked(synthetic(floating=True))
        d=measure_sequence(seq,w1_floor=.0255)
        self.assertEqual(d['summary']['W1'],0.)
        self.assertIs(d['results'][0]['passed'],False)

    def test_stationary_definition_and_swing(self):
        seq=tracked(synthetic())
        for d in seq:
            for side in ('L','R'):
                if d['planted_'+side]:self.assertLessEqual(abs(d['foot_'+side+'_velocity_x']),2)
        scroll=measure_sequence(seq)['summary']['sole_scroll']
        self.assertGreater(scroll['mean_scroll_px_per_frame'],20)
        self.assertTrue(all(abs(v)<1e-9 for side in ('L','R') for v in scroll['planted_scroll_lineage'][side]['delta_px_per_frame'] if v is not None))

    def test_grid_registration_known_translation(self):
        plain=synthetic(True);shifted=[_translate(f,(i%3)-1,(i%3)-1,fill=30) for i,f in enumerate(plain)]
        _,health=figure_mask_row(shifted,return_diagnostics=True)
        for i,h in enumerate(health):
            np.testing.assert_allclose(h['grid_shift_xy'],[-(i%3),-(i%3)],atol=1)

    def test_pigeon_and_line(self):
        t=np.arange(12)*2*np.pi/12
        p=head_path(np.cos(t),np.sin(t));self.assertGreater(p['W3a'],.35)
        self.assertEqual(p['W3c'],2)
        self.assertAlmostEqual(head_path(np.cos(t),4*np.cos(t))['W3a'],0.,delta=1e-7)
        self.assertIsNone(head_path([0]*12,[0]*12)['W3a'])

    def test_alpha_green_parity(self):
        f=synthetic()[0];mask=np.any(f!=30,axis=2)
        rgba=np.dstack((f,mask.astype(np.uint8)*255));green=f.copy();green[~mask]=(0,255,0)
        np.testing.assert_array_equal(figure_mask(rgba),figure_mask(green))
        self.assertEqual(landmarks(figure_mask(rgba))['head_top_y'],landmarks(figure_mask(green))['head_top_y'])

    def test_thin_head_and_missing_feet(self):
        m=np.zeros((300,200),bool);m[30:60,99:101]=True;m[60:260,70:130]=True
        d=landmarks(m);self.assertTrue(d['head_top_thin']);self.assertEqual(d['head_ref_y'],60)
        seq=track_landmarks([m]*12);data=measure_sequence(seq)
        self.assertIsNone(data['summary']['W6']);self.assertTrue(all(p['phase'] is None for p in data['phase_table']))
        self.assertFalse(landmarks(np.zeros((5,5),bool))['valid'])

    def test_front_rear_nulls_and_cli_merge(self):
        source=self.base/'frames';source.mkdir()
        for i,f in enumerate(synthetic()):Image.fromarray(f).save(source/f'front_{i+1:02}.png')
        out=self.base/'bands.json';plots=self.base/'plots'
        for label in ('plate13_front','plate13_rear'):
            main(['--ref',str(source),'--pattern','front_*.png','--fps','8.33','--label',label,'--out',str(out)])
        rows=json.loads(out.read_text());self.assertEqual(len(rows),2)
        for row in rows.values():
            for key in ('W5','W6','sole_scroll'):self.assertIsNone(row['summary'][key])
        with self.assertRaises(ValueError):curves(source,'none*.png')
        with self.assertRaises(ValueError):curves(source,'front_01.png')
        with self.assertRaises(ValueError):curves(source,'*.png',fps=0)
        with self.assertRaises(ValueError):curves(source,'*.png',ours=True)


if __name__=='__main__':unittest.main()
