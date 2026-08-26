"""Positive + matched-null control for the RADIAL variant (G-7).

hotcore : white centre -> saturated orange rim, intensity falling with radius
flatdisc: the SAME footprint, one flat colour, one flat intensity
Ground truth: hotcore has a hot desaturated core; flatdisc does not.
Both PULSE on and off so the +/-4-frame plate treats them as transient
(the lesson from the first control set, which cancelled its own null).
"""
import sys, os, math, json, time
import numpy as np
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline')
from frame_forensics_depth import _write_synth, analyse_depth

W,H,N,FPS = 1280,720,90,30
rng = np.random.default_rng(7)
yy,xx = np.mgrid[0:H,0:W]
bg = rng.normal(40,9,(H,W,3)).clip(0,90)
for _ in range(500):
    cy,cx = rng.integers(0,H), rng.integers(0,W); r=int(rng.integers(5,34))
    bg[(yy-cy)**2+(xx-cx)**2 <= r*r] += rng.normal(0,26,3)
bg = bg.clip(0,130)

def make(name, hot):
    fr=[]
    R=90.0
    for i in range(N):
        f = bg.copy()
        ph = (i % 15) / 14.0            # pulse: on for 15 frames, then repeat
        amp = math.sin(math.pi*ph)**2
        d = np.sqrt((xx-640.0)**2 + (yy-380.0)**2)
        m = d <= R
        t = np.clip(d/R, 0, 1)
        if hot:
            inten = 255.0*amp*(1.0-t)**1.4
            # white at centre -> orange at rim
            f[...,0] += np.where(m, inten, 0)
            f[...,1] += np.where(m, inten*(1.0-0.55*t), 0)
            f[...,2] += np.where(m, inten*(1.0-0.95*t), 0)
        else:
            inten = 200.0*amp
            f[...,0] += np.where(m, inten, 0)
            f[...,1] += np.where(m, inten*0.55, 0)
            f[...,2] += np.where(m, inten*0.15, 0)
        fr.append(f.clip(0,255))
    _write_synth(f'synth/synth_r_{name}.mp4', fr, FPS)

t=time.time(); os.makedirs('synth',exist_ok=True)
make('hotcore', True); make('flatdisc', False)
print('written %.0fs'%(time.time()-t), flush=True)
o={}
for n in ('hotcore','flatdisc'):
    r=analyse_depth(f'synth/synth_r_{n}.mp4', n); o[n]=r['summary']['F1r_radial_core']
    o[n]['_elongation']=r['summary']['F3_width']['elongation_med']
    print(n, {k:(round(v,4) if isinstance(v,float) else v) for k,v in o[n].items()}, flush=True)
json.dump(o, open('out/synth_radial_control.json','w'), indent=2, default=str)
