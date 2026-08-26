import sys, os, math, json, time
import numpy as np
sys.path.insert(0,'/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/pipeline')
from frame_forensics_depth import _write_synth, analyse_depth

W,H,N,FPS = 1280,720,90,30
rng = np.random.default_rng(11)
yy,xx = np.mgrid[0:H,0:W]
bg = rng.normal(40,9,(H,W,3)).clip(0,90)
for _ in range(500):
    cy,cx = rng.integers(0,H), rng.integers(0,W); r=int(rng.integers(5,34))
    bg[(yy-cy)**2+(xx-cx)**2 <= r*r] += rng.normal(0,26,3)
bg = bg.clip(0,130)

def trail(f, cx, cy, taper, sparks, smoke):
    # ⚑ 26 px/frame, 130 px trail: the FIRST control set moved 7 px/frame with a
    # 220 px trail, so the +/-4-frame motion-compensated plate covered the
    # object's own path and CANCELLED IT. The bar/smoke arms produced no core at
    # all and F1-F5 had no valid null. Overlap must be small for the plate to
    # treat the object as transient.
    L = 130.0
    for k in range(22):
        t = k/21.0
        px = cx - t*L
        rad = (3.5+13.0*t) if taper else 8.0
        g = np.exp(-((xx-px)**2+(yy-cy)**2)/(2*rad*rad))
        if taper:
            inten = 255.0*(1.0-t)**1.5; col = np.array([1.0,1.0-0.8*t,1.0-0.97*t])
        else:
            inten = 200.0; col = np.array([1.0,0.55,0.15])
        for c in range(3): f[...,c] += inten*col[c]*g
    if sparks:
        for _ in range(22):
            a=rng.uniform(0,2*np.pi); r=rng.uniform(38,120)
            sx,sy = cx-rng.uniform(0,110)+r*np.cos(a)*0.35, cy+r*np.sin(a)
            f += (240.0*np.exp(-((xx-sx)**2+(yy-sy)**2)/6.0))[...,None]
    if smoke:
        f += (30.0*np.exp(-(((xx-(cx-70))**2)+((yy-cy)*1.8)**2)/(2*95.0**2)))[...,None]
    return f

def make(name, taper, sparks, smoke):
    fr=[]
    for i in range(N):
        f = bg.copy()
        cx = 120 + 26.0*i
        if cx < W+140: trail(f, cx, H//2, taper, sparks, smoke)
        fr.append(f.clip(0,255))
    _write_synth(f'synth/synth2_{name}.mp4', fr, FPS)

t=time.time()
os.makedirs('synth',exist_ok=True)
make('comet', True, True, False)
make('bar',   False, False, False)
make('smoke', False, False, True)

# F6a scar positive + null: static camera, a bright flash at frame 45; the
# positive leaves a permanent dark scorch disc, the null leaves nothing.
def scarclip(name, permanent):
    fr=[]
    disc = ((xx-640)**2+(yy-430)**2) <= 62**2
    for i in range(N):
        f = bg.copy()
        k = i-45
        if 0 <= k < 7:
            f += (255.0*math.exp(-k/2.0)*np.exp(-(((xx-640)**2+(yy-430)**2)/(2*55.0**2))))[...,None]
        if permanent and i >= 45:
            f[disc] *= 0.38
        fr.append(f.clip(0,255))
    _write_synth(f'synth/synth2_{name}.mp4', fr, FPS)
scarclip('scar', True); scarclip('scarnull', False)
print('written %.0fs'%(time.time()-t))

res={}
for n in ('comet','bar','smoke','scar','scarnull'):
    t0=time.time(); r=analyse_depth(f'synth/synth2_{n}.mp4', n)
    print(n,'%.0fs'%(time.time()-t0)); res[n]=r['summary']
json.dump(res, open('out/synth_controls2.json','w'), indent=2, default=str)
