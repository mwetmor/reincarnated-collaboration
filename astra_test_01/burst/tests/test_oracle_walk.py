"""Known-truth 12-phase walker and explicit bad/ambiguous input controls."""
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image,ImageDraw
from oracle.walk_landmarks import figure_mask,figure_mask_row,landmarks,track_landmarks,track_head,_translate,mask_stability
from oracle.walk_curves import measure_sequence,head_path,bob,phase_table,curves,annotation_curves,annotation_landmarks
from oracle.walk_bands import main,bands,agreement
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


def alpha_frames(frames):
    """Use the synthetic drawing's exact foreground, without segmentation."""
    return [np.dstack((f, (np.any(f != 30, axis=2)*255).astype(np.uint8))) for f in frames]


def synthetic_annotation():
    """True points from synthetic(): translating hip, drawn head/wrists/soles."""
    frames = []
    keys = ('head_top','chin','hip','near_sole','far_sole','near_wrist','far_wrist','ground_y')
    for i in range(12):
        ox = 16*i; shift = [0,4,4,0,-3,-3][i%6]
        hx = round(3*np.sin(2*np.pi*i/12))
        f = dict(frame=i, head_top=[150+ox+hx,60+shift], chin=[150+ox+hx,87+shift],
                 hip=[150+ox,210], ground_y=300, confidence={k:1. for k in keys})
        for name,base,off,arm in [('near',90,i,106),('far',210,(i+6)%12,194)]:
            stance = off < 6
            dx = 40-16*off if stance else [-56,-32,-8,16,40,56][off-6]
            f[name+'_sole'] = [base+ox+dx, 300 if stance else 290]
            f[name+'_wrist'] = [ox+arm-round(.3*dx),168]
            f['planted_'+name] = stance
        frames.append(f)
    return dict(plate='synthetic', row='lateral', frames=frames,
                subject_height_px=float(np.mean([300-f['head_top'][1] for f in frames])),
                stride_notes={'contact_frames':[0,6]})


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
    def test_alpha_synthetic_kinematics(self):
        # Kinematics are scoped to exact alpha truth; RGB parity stays separate.
        seq=tracked(alpha_frames(synthetic()))
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
        seq=tracked(alpha_frames(synthetic()))
        for d in seq:
            for side in ('L','R'):
                if d['planted_'+side]:self.assertLessEqual(abs(d['foot_'+side+'_velocity_x']),2)
        scroll=measure_sequence(seq)['summary']['sole_scroll']
        self.assertGreater(scroll['mean_scroll_px_per_frame'],20)
        self.assertTrue(all(abs(v)<1e-9 for side in ('L','R') for v in scroll['planted_scroll_lineage'][side]['delta_px_per_frame'] if v is not None))

    def test_grid_registration_known_translation(self):
        plain=synthetic(True);shifted=[_translate(f,(i%3)-1,(i%3)-1,fill=30) for i,f in enumerate(plain)]
        _,health=figure_mask_row(shifted,return_diagnostics=True,method="B")
        for i,h in enumerate(health):
            np.testing.assert_allclose(h['grid_shift_xy'],[-(i%3),-(i%3)],atol=1)

    def test_annotation_truth_and_per_frame_coordinate_invariance(self):
        ann = synthetic_annotation(); path = self.base/'annotation.json'
        path.write_text(json.dumps(ann)); data = annotation_curves(path)
        s = data['summary']; H = ann['subject_height_px']
        self.assertEqual(s['W1'], 7/H)
        self.assertEqual(s['W4'], 2); self.assertEqual(s['W3c'], 2)
        # These screen-separated synthetic arms/legs share hip-relative signs;
        # unlike the mask's centered proxy, literal annotation opposition is zero.
        self.assertEqual(s['W6'], 0.)
        self.assertEqual([p['phase'] for p in data['phase_table']],
                         ['CONTACT','PASSING','UP','UP','UP','UP',
                          'CONTACT','DOWN','DOWN','DOWN','DOWN','PASSING'])
        self.assertEqual(s['W2']['min'], [{'frame':i,'phase':data['phase_table'][i]['phase']} for i in (1,2,7,8)])
        for quantity in data['quantities'].values():
            self.assertEqual(quantity['source'], 'annotation'); self.assertEqual(quantity['mean_confidence'],1.)
        # Arbitrary cell cuts, including vertical offsets larger than the bob.
        for i, frame in enumerate(ann['frames']):
            dy = [0,31,-14,8][i%4]; dx = 27*i
            frame['ground_y'] += dy
            for key in ('head_top','chin','hip','near_sole','far_sole','near_wrist','far_wrist'):
                frame[key][0] += dx; frame[key][1] += dy
        path.write_text(json.dumps(ann)); moved = annotation_curves(path)
        self.assertEqual(s, moved['summary']); self.assertEqual(data['phase_table'],moved['phase_table'])
        # Literal opposition uses same-side signs, without mean-centering.
        for frame in ann['frames']:
            for side in ('near','far'):
                frame[side+'_wrist'][0] = 2*frame['hip'][0]-frame[side+'_sole'][0]
        path.write_text(json.dumps(ann))
        self.assertEqual(annotation_curves(path)['summary']['W6'],1.)

    def test_annotation_extra_contact_is_not_repaired(self):
        ann = synthetic_annotation();ann['frames'][2]['planted_near'] = False
        path = self.base/'annotation.json';path.write_text(json.dumps(ann))
        phases = annotation_curves(path)['phase_table']
        self.assertTrue(all(p['phase'] is None for p in phases))
        self.assertTrue(all(p['reason']=='expected two contact events; observed 3' for p in phases))
        self.assertEqual(sum(len(p['contact_sides']) for p in phases),3)

    def test_mask_stability_selector_and_method_default(self):
        masks=[figure_mask(f) for f in alpha_frames(synthetic())]
        self.assertTrue(mask_stability(masks)['stable'])
        bad=[np.zeros_like(masks[0])]*6+masks[6:]
        self.assertFalse(mask_stability(bad)['stable'])
        # Exactly .25 is excluded, not rounded into the stable interval.
        low=np.zeros((20,20),bool);low[1:16,1:6]=True
        high=np.zeros_like(low);high[1:16,1:6]=True;high[1:11,6:11]=True
        self.assertEqual(mask_stability([low,high]*6)['mask_stability'],.25)
        self.assertFalse(mask_stability([low,high]*6)['stable'])
        for direct,row in zip(masks,figure_mask_row(alpha_frames(synthetic()))):
            np.testing.assert_array_equal(direct,row)
        source=self.base/'unstable';source.mkdir()
        for i,m in enumerate(bad):
            Image.fromarray(np.dstack((np.zeros((*m.shape,3),np.uint8),m.astype(np.uint8)*255))).save(source/f'{i:02}.png')
        data=curves(source)
        self.assertIsNone(data['mask_estimate']);self.assertEqual(data['reason'],'unstable_segmentation')
        self.assertTrue(all(v is None for v in data['summary'].values()))

    def test_annotation_cli_agreement_and_ours_alpha(self):
        source=self.base/'alpha';source.mkdir()
        for i,f in enumerate(alpha_frames(synthetic())):
            Image.fromarray(f).save(source/f'frame_{i:02}.png')
        ann=synthetic_annotation();path=self.base/'annotation.json';path.write_text(json.dumps(ann))
        out=self.base/'bands.json'
        main(['--landmarks',str(path),'--ref',str(source),'--fps','8.33',
              '--label','plate13_lateral','--out',str(out)])
        row=json.loads(out.read_text())['plate13_lateral']
        self.assertIsNotNone(row['mask_estimate'])
        self.assertEqual(row['bands']['W1']['value'],row['summary']['W1'])
        self.assertEqual(row['bands']['W1']['source'],'annotation')
        self.assertTrue(row['agreement']['W1']['within_20_percent'])
        self.assertIsNone(agreement(row['summary'],None)['W1']['abs_delta'])
        self.assertEqual(agreement({'W1':0.},{'W1':0.})['W1']['within_20_percent'],True)
        ours=self.base/'ours';ours.mkdir()
        for i,f in enumerate(alpha_frames(synthetic_otsu_lineage())):
            canvas=np.zeros((512,512,4),np.uint8);canvas[:360,:300]=f
            Image.fromarray(canvas).save(ours/f'{i:02}.png')
        self.assertIsNotNone(curves(ours,ours=True)['summary']['W1'])

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
