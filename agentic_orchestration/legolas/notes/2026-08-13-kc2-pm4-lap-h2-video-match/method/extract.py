"""Per-frame nameplate extraction over an arbitrary window.

Outputs one row per detected plate:
  t, kind(M|P), x_anchor, y_bar, w, txt
where x_anchor = x_left + 36.  MEASURED: the bar depletes RIGHTWARD from a fixed left
edge (player bar x_left held 921-924 px across 1,742 detections while its width ranged
14-74 px), so the left edge -- not the bar centre -- is the anchor; +36 = half the
full-width bar (72 px) recovers the character's screen x.
"""
import numpy as np, subprocess, sys
sys.path.insert(0,'/tmp/pm4h2')
from bars import find_bars, green_mask2, _runs
V="/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"
HUD=[(1330,0,1920,262),(0,0,1920,58),(0,980,1920,1080),(0,0,300,120)]
def in_hud(x,y): return any(x0<=x<=x1 and y0<=y<=y1 for (x0,y0,x1,y1) in HUD)

def pbar(a):
    m=green_mask2(a); W=(a[...,0]>150)&(a[...,1]>150)&(a[...,2]>145)
    best=None
    for y in range(300,700):
        for (s,e) in _runs(m[y],14,90):
            if not (890<=s<=960): continue
            ok=False
            for (s2,e2) in _runs(m[y+1],10,92):
                if min(e,e2)-max(s,s2)>0.6*min(e-s,e2-s2): ok=True;break
            if not ok: continue
            xc=(s+e)//2
            txt=int(W[max(0,y-34):max(0,y-18), max(0,xc-95):xc+96].sum())
            if txt<60: continue
            c=(s,y+1.0,e-s+1,txt)
            if best is None or c[2]>best[2]: best=c
    return best

def run(s,dur,fps,out):
    cmd=['ffmpeg','-v','error','-ss',str(s),'-t',str(dur),'-i',V,'-vf',f'fps={fps}','-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,bufsize=1920*1080*3)
    rows=[]; i=0
    N=1920*1080*3
    while True:
        raw=p.stdout.read(N)
        if len(raw)<N: break
        a=np.frombuffer(raw,dtype=np.uint8).reshape(1080,1920,3)
        t=s+i/fps
        for b in find_bars(a,minw=14,y0=60,y1=975):
            if in_hud(b['x_c'],b['y']): continue
            rows.append((t,0,b['x_left']+36,b['y'],b['w'],b['txt']))
        pb=pbar(a)
        if pb is not None: rows.append((t,1,pb[0]+36,pb[1],pb[2],pb[3]))
        i+=1
    p.stdout.close(); p.wait()
    R=np.array(rows); np.save(out,R)
    return R,i

if __name__=='__main__':
    s,dur,fps,out=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
    R,n=run(s,dur,fps,out)
    print('frames',n,'plates',len(R),'player rows',int((R[:,1]==1).sum()))
