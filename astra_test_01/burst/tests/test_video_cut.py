"""Fast synthetic-only tests for the T3a loop contract (no real-clip IO)."""
import json
from pathlib import Path
import subprocess
import sys
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


def jump_series():
    # Independent 30 baseline / 6 crouch / 10 rise / 10 fall / 6 land / 20 rest.
    head = np.r_[np.full(30,100.), [102,104,106,108,110,112],
                 np.linspace(95,50,10), np.linspace(55,100,10),
                 [104,108,112,110,106,102], np.full(20,100.)]
    sole = np.r_[np.full(36,340.), np.linspace(335,290,10),
                 np.linspace(295,340,10), np.full(26,340.)]
    return dict(head_top_y=head.tolist(),sole_y=sole.tolist())


def cast_series():
    tip = np.tile([100.,100.],(82,1))
    tip[30:40,1] = np.linspace(96,60,10)  # gather 39
    tip[40] = [102,62]
    tip[41] = [106,64]
    tip[42] = [156,70]                 # largest arrival speed, release 42
    tip[43:46] = [[166,75],[172,80],[176,85]]
    tip[46:56] = np.linspace([169,87],[100,100],10)  # return 55
    return dict(tip_xy=tip.tolist())


class OneShotTests(unittest.TestCase):
    def test_jump_all_key_poses_within_one_frame(self):
        result = vc.detect_oneshot('jump',jump_series(),60)
        expected = dict(onset=30,crouch=35,take_off=36,apex=45,touchdown=55,
                        landing_crouch=58,settle=62)
        self.assertIsNotNone(result['detection'])
        errors = {k:abs(result['detection'][k]-v) for k,v in expected.items()}
        self.assertLessEqual(max(errors.values()),1)
        self.assertEqual(result['baseline']['samples'],30)
        self.assertEqual(vc.resample_oneshot('jump',result),[30,35,36,40,45,50,58,62])
        print('VIDEO_SYNTHETIC_JUMP '+json.dumps(dict(expected=expected,
              measured=result['detection'],errors=errors,confidence=result['confidence'])))

    def test_cast_gather_release_and_order(self):
        result = vc.detect_oneshot('cast',cast_series(),60)
        self.assertIsNotNone(result['detection'])
        expected = dict(onset=30,raise_mid=34,gather=39,release=42,
                        follow_through=45,return_mid=50,return_index=55,settle=55)
        self.assertAlmostEqual(result['detection']['gather'],39,delta=1)
        self.assertAlmostEqual(result['detection']['release'],42,delta=1)
        self.assertEqual(vc.resample_oneshot('cast',result),[30,34,39,42,45,50,55,55])
        print('VIDEO_SYNTHETIC_CAST '+json.dumps(dict(expected=expected,
              measured=result['detection'],gather_error=abs(result['detection']['gather']-39),
              release_error=abs(result['detection']['release']-42))))

    def test_no_event_flat_and_baseline_noise(self):
        for noisy in (False,True):
            noise = np.tile([-.2,.2],41) if noisy else np.zeros(82)
            samples = [('jump',dict(head_top_y=(100+noise).tolist(),sole_y=[340.]*82)),
                       ('cast',dict(tip_xy=np.column_stack([100+noise,100+noise]).tolist()))]
            for kind,series in samples:
                with self.subTest(kind=kind,noisy=noisy):
                    result = vc.detect_oneshot(kind,series,60)
                    self.assertIsNone(result['detection'])
                    self.assertLess(result['confidence'],.3)
                    self.assertIsNone(result['onset'])
                    with self.assertRaises(ValueError): vc.resample_oneshot(kind,result)
                    json.dumps(result,allow_nan=False)

    def test_single_frame_spike_and_crouch_without_flight(self):
        series = dict(head_top_y=[100.]*82,sole_y=[340.]*82)
        series['head_top_y'][35] = 120
        self.assertIsNone(vc.detect_oneshot('jump',series,60)['onset'])
        series['head_top_y'][36] = 120
        result = vc.detect_oneshot('jump',series,60)
        self.assertEqual(result['onset'],35)
        self.assertIsNone(result['detection']); self.assertLess(result['confidence'],.3)
        tip = dict(tip_xy=[[100.,100.] for _ in range(82)])
        tip['tip_xy'][35] = [200.,50.]
        self.assertIsNone(vc.detect_oneshot('cast',tip,60)['onset'])

    def test_incomplete_events_never_fabricate_settle(self):
        for kind,series in [('jump',jump_series()),('cast',cast_series())]:
            for length in (20,48,60 if kind=='cast' else 67):
                with self.subTest(kind=kind,length=length):
                    short = {k:v[:length] for k,v in series.items()}
                    result = vc.detect_oneshot(kind,short,60)
                    self.assertIsNone(result['detection'])
                    self.assertLess(result['confidence'],.3)
                    self.assertIsNone(result['settle'])

    def test_settle_requires_six_consecutive_samples(self):
        series = jump_series()
        series['head_top_y'][67] = 100.1  # breaks first five rest samples
        result = vc.detect_oneshot('jump',series,60)
        self.assertEqual(result['settle'],68)
        cast = cast_series()
        cast['tip_xy'][60] = [100.1,100.]
        self.assertEqual(vc.detect_oneshot('cast',cast,60)['settle'],61)

    def test_invalid_tracking_and_arguments(self):
        for kind,series in [('jump',jump_series()),('cast',cast_series())]:
            for bad in (None,float('nan'),float('inf')):
                broken = {k:list(v) for k,v in series.items()}
                key = next(iter(broken))
                broken[key][40] = [bad,bad] if kind=='cast' else bad
                result = vc.detect_oneshot(kind,broken,60)
                self.assertIsNone(result['detection'])
                self.assertLess(result['confidence'],.3)
                json.dumps(result,allow_nan=False)
        for fps in (0,-1,float('nan')):
            with self.assertRaises(ValueError): vc.detect_oneshot('jump',jump_series(),fps)
        with self.assertRaises(ValueError): vc.detect_oneshot('walk',{},60)
        with self.assertRaises(ValueError): vc.detect_oneshot('cast',{'tip_xy':[1.]*82},60)
        with self.assertRaises(ValueError): vc.detect_oneshot('jump',dict(head_top_y=[1.]*82,sole_y=[1.]*80),60)

    def test_native_offset_and_half_rate(self):
        series = jump_series(); series['indices_native'] = list(range(100,182))
        result = vc.detect_oneshot('jump',series,60)
        self.assertEqual(result['onset'],130)
        self.assertEqual(result['settle'],162)
        cast = cast_series(); cast['indices_native'] = list(range(101,183))
        measured = vc.detect_oneshot('cast',cast,60)
        self.assertEqual(measured['detection']['raise_mid'],136)
        half = {k:v[::2] for k,v in series.items()}
        result = vc.detect_oneshot('jump',half,60)
        self.assertEqual(result['baseline']['samples'],15)
        self.assertAlmostEqual(result['detection']['apex'],145,delta=1)
        self.assertEqual(result['settle'],162)

    def test_resampling_counts_midpoints_and_bad_poses(self):
        detection = vc.detect_oneshot('jump',jump_series(),60)
        for count in (1,2,5,8,16):
            sampled = vc.resample_oneshot('jump',detection,count)
            self.assertEqual(len(sampled),count)
            self.assertEqual(sampled,sorted(sampled))
            self.assertEqual(sampled[0],30)
            if count>1: self.assertEqual(sampled[-1],62)
        for n in (0,-1,2.,True):
            with self.assertRaises(ValueError): vc.resample_oneshot('jump',detection,n)
        with self.assertRaises(ValueError): vc.resample_oneshot('cast',detection)
        with self.assertRaises(ValueError): vc.resample_oneshot('jump',{})
        with self.assertRaises(ValueError): vc.resample_oneshot('jump',None)
        detection['detection']['apex'] = 20
        with self.assertRaises(ValueError): vc.resample_oneshot('jump',detection)


class CLITests(unittest.TestCase):
    setUp = Tests.setUp

    def test_missing_matte_is_reported_without_fabricated_measurements(self):
        good = self.base/'good.png'; bad = self.base/'bad.png'
        figure().save(good); Image.new('RGB',(160,160),'red').save(bad)
        frames = vc._matte_oneshot_report([good,bad,good,good],'clamp')
        series = vc.track(frames)
        self.assertEqual(series['invalid_indices'],[1])
        self.assertIsNone(series['head_top_y'][1])
        self.assertFalse(frames.notes[1]['valid'])
        self.assertIn('uniform green plate',frames.notes[1]['error'])
        scan = vc._splice_missing(frames,series['invalid_indices'])
        self.assertEqual(scan['per_pair_mad'],[None,None,0.])
        self.assertEqual(scan['invalid_pairs'],[[0,1],[1,2]])
        self.assertEqual(scan['suspect_pairs'],[])
        self.assertEqual(scan['median_pair_mad'],0.)
        with self.assertRaises(ValueError): vc.matte_frames([good,bad])

    def test_cli_synthetic_idle_half_rate_and_audit(self):
        clip = self.base/'idle.mkv'
        subprocess.run([vc.FFMPEG,'-v','error','-f','lavfi','-i',
            'color=c=0x00ff00:s=640x640:r=24:d=3,drawbox=x=200:y=80:w=240:h=480:color=0x708090:t=fill',
            '-c:v','ffv1',str(clip)],check=True,capture_output=True)
        out = self.base/'cli'
        command = [sys.executable,'-B','-m','oracle.video_cut','--clip',str(clip),
            '--kind','idle','--direction','NE','--n','4','--fps-out','8','--out',str(out),
            '--half-rate','--edge-mode','clamp']
        completed = subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(completed.returncode,0,completed.stderr)
        record = json.loads((out/'registration.json').read_text())
        series = json.loads((out/'series.json').read_text())
        self.assertEqual(record['n_native'],72)
        self.assertEqual(record['source']['n'],36)
        self.assertEqual(record['fps_out'],8)
        self.assertTrue(all(i%2==0 for i in record['indices_native']))
        self.assertEqual(len(record['output_frames']),4)
        self.assertEqual(len(record['selection']['candidates']),12)
        self.assertEqual(series['indices_native'],list(range(0,72,2)))
        self.assertFalse((out/'tmp').exists())
        self.assertIsNone(record['results'][0]['passed'])
        self.assertEqual(record['transform']['anchor_H'],240)
        self.assertEqual(record['transform']['anchor_sole_row'],399)
        self.assertEqual(record['transform']['anchor_cx'],255.5)
        for f in record['output_frames']:
            with Image.open(f['path']) as image:
                self.assertEqual(image.mode,'RGBA'); self.assertEqual(image.size,(512,512))
        with Image.open(out/'sheets/idle_NE_strip.png') as image:
            self.assertEqual(image.getpixel((0,0)),(58,63,74))
        repeated = subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        self.assertNotEqual(repeated.returncode,0)
        self.assertIn('out must be empty',repeated.stderr)


if __name__ == '__main__':
    unittest.main()
