"""Fast synthetic-only tests for the T3a loop contract (no real-clip IO)."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

from oracle import video_cut as vc

ROOT = Path(__file__).resolve().parents[1]


def figure(i=0, bob_period=None, breath_period=None, jump=0, size=160):
    """Connected head, chest and planted feet; optional 6px whole-body splice."""
    a = np.zeros((size,size,4),np.uint8)
    top = 20+(round(6*np.cos(2*np.pi*i/bob_period)) if bob_period else 0)
    width = 36+(round(8*np.sin(2*np.pi*i/breath_period)) if breath_period else 0)
    a[40:110,72:88] = (130,160,200,255)
    a[top:48,68:92] = (200,180,160,255)
    a[48:75,80-width//2:80+(width+1)//2] = (90,140,200,255)
    a[100:140,64:76] = (100,110,140,255)
    a[100:140,84:96] = (100,110,140,255)
    if jump:
        a = np.roll(a,jump,axis=1)
    return Image.fromarray(a)


class Tests(unittest.TestCase):
    def setUp(self):
        (ROOT/'tests/tmp').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT/'tests/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def test_bob_17_stride_34(self):
        series = vc.track([figure(i,bob_period=17) for i in range(145)])
        p = vc.detect_period('walk',series,24)
        self.assertAlmostEqual(p['bob_frames'],17,delta=1)
        self.assertAlmostEqual(p['frames'],34,delta=2)
        self.assertEqual(p['source'],'head_bob_autocorr')
        self.assertGreaterEqual(p['confidence'],.3)
        run = vc.detect_period('run',series,24)
        self.assertEqual(run,p)
        print('VIDEO_SYNTHETIC_BOB '+json.dumps(p))

    def test_idle_48_and_flat_fallback(self):
        series = vc.track([figure(i,breath_period=48) for i in range(145)])
        p = vc.detect_period('idle',series,24)
        self.assertAlmostEqual(p['frames'],48,delta=1)
        self.assertEqual(p['source'],'chest_width_autocorr')
        flat = vc.track([figure() for _ in range(145)])
        fallback = vc.detect_period('idle',flat,24)
        self.assertEqual((fallback['source'],fallback['frames']),('prompted_fallback',48))
        self.assertEqual(vc.detect_period('idle',flat,24,prompted_s=3)['frames'],72)
        self.assertIsNone(vc.detect_period('walk',flat,24)['frames'])
        sibling = vc.detect_period('run',flat,24,sibling_stride_frames=34)
        self.assertEqual((sibling['source'],sibling['frames']),('sibling',34))
        print('VIDEO_SYNTHETIC_IDLE '+json.dumps(p))

    def test_track_largest_component_median_and_coordinates(self):
        frames = [np.asarray(figure()).copy() for _ in range(7)]
        frames[3][2:5,75:85] = (255,255,255,255)  # detached speck is ignored
        s = vc.track(frames)
        self.assertEqual(s['head_top_y'],[20.]*7)
        self.assertEqual(s['sole_y'],[139.]*7)
        self.assertEqual(s['H'],[120.]*7)
        self.assertLessEqual(s['working_scale'],.5)
        self.assertEqual(len(s['bbox']),7)
        self.assertTrue(all(len(p)==2 for p in s['tip_xy']))
        self.assertGreater(s['chest_w'][0],0)
        self.assertEqual(s['invalid_indices'],[])
        json.dumps(s,allow_nan=False)
        invalid = vc.track([np.zeros((160,160),bool)]*7)
        self.assertEqual(invalid['invalid_indices'],list(range(7)))
        self.assertIsNone(vc.detect_period('walk',invalid,24)['frames'])
        with self.assertRaises(ValueError): vc.track([np.zeros((160,160,3),np.uint8)])
        with self.assertRaises(ValueError): vc.track([np.zeros((160,160),bool),np.zeros((80,80),bool)])

    def test_latest_down_and_bounds(self):
        s = vc.track([figure(i,bob_period=17) for i in range(145)])
        p = vc.detect_period('walk',s,24)
        cut = vc.select_cycle('walk',s,p,24,4.4)
        self.assertEqual(cut['start'],max(c['start'] for c in cut['candidates']))
        self.assertLessEqual(cut['end_exclusive']/24,4.4)
        self.assertTrue(all(c['end_exclusive']-c['start']==34 for c in cut['candidates']))
        self.assertTrue(all(c['seam_mad'] is not None for c in cut['candidates']))
        self.assertIsNone(vc.select_cycle('walk',s,p,24,1)['start'])
        self.assertIsNone(vc.select_cycle('walk',s,{'frames':None},24,4.4)['start'])
        later = vc.select_cycle('walk',s,p,24,4.4,min_start_s=2)
        self.assertTrue(all(c['start']>=48 for c in later['candidates']))

    def test_idle_rgb_closure_optimum_and_latest_tie(self):
        frames = [figure() for _ in range(12)]
        s = vc.track(frames)
        cut = vc.select_cycle('idle',s,{'frames':4},24,.5)
        self.assertEqual(cut['start'],7)
        self.assertEqual(cut['closure_mad'],0)
        changed = [np.asarray(f).copy() for f in frames]
        for i,a in enumerate(changed): a[60:65,75:85,:3] = i*17
        changed[5] = changed[1].copy()
        s = vc.track(changed)
        cut = vc.select_cycle('idle',s,{'frames':4},24,.5)
        self.assertEqual(cut['start'],1)
        self.assertEqual(cut['closure_mad'],0)
        self.assertLess(cut['closure_mad'],max(c['closure_mad'] for c in cut['candidates']))
        masks = vc.track([np.asarray(f)[...,3] for f in frames])
        with self.assertRaises(ValueError): vc.select_cycle('idle',masks,{'frames':4},24,.5)

    def test_latest_down_within_flat_maximum(self):
        # A 3-frame median can leave a two-frame DOWN plateau. Its later frame
        # is still a local maximum and is the contracted latest eligible start.
        s = {'head_top_y':[0.,1.,3.,3.,2.,0.,1.,3.,3.,2.,0.,1.]}
        cut = vc.select_cycle('walk',s,{'frames':4,'bob_frames':2},24,.5)
        self.assertEqual(cut['start'],8)
        self.assertEqual(cut['end_exclusive'],12)
        self.assertIsNone(cut['seam_mad'])

    def test_splice_108_and_selection_membership(self):
        frames = [figure(jump=6 if i>=108 else 0) for i in range(145)]
        splice = vc.splice_check(frames)
        self.assertEqual(splice['suspect_pairs'],[[107,108]])
        self.assertEqual(splice['median_pair_mad'],0)
        s = vc.track(frames); s['splice'] = splice
        # Force one DOWN candidate spanning the planted jump.
        s['head_top_y'] = [float(-abs(i-100)) for i in range(145)]
        cut = vc.select_cycle('walk',s,{'frames':34},24,6.1)
        self.assertTrue(cut['suspect_inside_selected'])
        self.assertEqual(cut['suspect_pairs_inside_selected'],[[107,108]])
        self.assertEqual(vc.splice_check([figure(),figure()])['suspect_pairs'],[])
        self.assertEqual(vc.splice_check([])['per_pair_mad'],[])
        print('VIDEO_SYNTHETIC_SPLICE '+json.dumps({'suspect_pairs':splice['suspect_pairs'],
              'mad':splice['per_pair_mad'][107],'median':splice['median_pair_mad']}))

    def test_resample_python_round_and_bad_arguments(self):
        self.assertEqual(vc.resample(71,105,12),[71,74,77,79,82,85,88,91,94,97,99,102])
        self.assertEqual(vc.resample(0,5,2),[0,2])
        self.assertEqual(vc.resample(0,2,3),[0,1,1])
        for args in [(0,0,1),(5,2,1),(0,4,0),(-1,3,2),(0.,4,2)]:
            with self.subTest(args=args), self.assertRaises(ValueError): vc.resample(*args)
        for fps in (0,-1,float('nan')):
            with self.assertRaises(ValueError): vc.detect_period('idle',{'chest_w':[1]*12},fps)
        with self.assertRaises(ValueError): vc.detect_period('jump',{},24)

    def test_register_shared_transform_including_rest(self):
        # Native frame 0 is rest; frame 1 is the selected-cycle anchor.
        base = figure().resize((640,640),Image.Resampling.NEAREST)
        shifted = Image.fromarray(np.roll(np.asarray(base),8,axis=1))
        frames, transform = vc.register([base,shifted,base],anchor_index=1)
        self.assertAlmostEqual(transform['anchor_H'],240,delta=1)
        self.assertEqual(transform['anchor_sole_row'],399)
        self.assertEqual(transform['anchor_cx'],255.5)
        self.assertLessEqual(transform['scale'],1)
        self.assertTrue(transform['one_transform_for_every_frame'])
        np.testing.assert_array_equal(frames[0],frames[2])
        for source,actual in zip([base,shifted,base],frames):
            scaled = source.resize(tuple(transform['scaled_size']),Image.Resampling.LANCZOS,
                                   box=tuple(transform['source_sampling_box_xyxy']))
            expected = Image.new('RGBA',(512,512)); expected.paste(scaled,tuple(transform['translation_xy']))
            np.testing.assert_array_equal(actual,expected)
        with self.assertRaises(ValueError): vc.register([figure()]) # would upscale
        with self.assertRaises(ValueError): vc.register([base],anchor_index=2)
        print('VIDEO_SYNTHETIC_REGISTER '+json.dumps(transform))

    def test_matte_floor_and_edge_note(self):
        a = np.asarray(figure()).copy(); a[a[...,3]==0] = (0,255,0,255)
        path = self.base/'plate.png'; Image.fromarray(a).convert('RGB').save(path)
        frames = vc.matte_frames([path],edge_mode='clamp')
        self.assertEqual(frames[0].mode,'RGBA')
        self.assertEqual(frames.notes[0]['alpha_floor'],40)
        self.assertEqual(frames.notes[0]['edge_mode_requested'],'clamp')
        self.assertEqual(np.asarray(frames[0])[0,0,3],0)
        with self.assertRaises(ValueError): vc.matte_frames([path],edge_mode='unknown')
        with self.assertRaises(ValueError): vc.matte_frames([path],alpha_floor=-1)
        with self.assertRaises(ValueError): vc.matte_frames([])
        bad = self.base/'bad.png'; Image.new('RGB',(64,64),'red').save(bad)
        with self.assertRaises(ValueError): vc.matte_frames([bad])

    def test_half_rate_native_units(self):
        full = vc.track([figure(i,bob_period=16) for i in range(145)])
        half = vc.track([figure(i,bob_period=16) for i in range(0,145,2)])
        half['indices_native'] = list(range(0,145,2))
        half['times'] = [i/24 for i in half['indices_native']]
        p = vc.detect_period('walk',half,24)
        self.assertEqual(p['frames'],vc.detect_period('walk',full,24)['frames'])
        self.assertEqual(p['bob_frames'],16)
        cut = vc.select_cycle('walk',half,p,24,4.4)
        self.assertEqual(cut['end_exclusive']-cut['start'],32)
        self.assertTrue(all(i%2==0 for i in cut['indices_native']))

    def test_split_real_synthetic_video_strict_time_and_half_rate(self):
        clip = self.base/'synthetic.mkv'
        subprocess.run([vc.FFMPEG,'-v','error','-f','lavfi','-i',
            'color=c=green:s=64x96:r=24:d=0.5','-c:v','ffv1',str(clip)],check=True,capture_output=True)
        for half in (False,True):
            meta = vc.split(clip,self.base/str(half),t_max_s=.25,half_rate=half)
            self.assertEqual(meta['fps'],24)
            self.assertEqual((meta['w'],meta['h']),(64,96))
            self.assertEqual(meta['n'],3 if half else 6)
            self.assertEqual(meta['indices_native'],[0,2,4] if half else list(range(6)))
            self.assertTrue(all(t<.25 for t in meta['times']))
            self.assertEqual(len(meta['paths']),meta['n'])
        with self.assertRaises(ValueError): vc.split(clip,self.base/'False')
        with self.assertRaises(ValueError): vc.split(clip,self.base/'bad',t_max_s=0)


if __name__ == '__main__':
    unittest.main()
