import numpy as np, subprocess, sys
sys.path.insert(0,'/tmp/pm4h2')
from bars import green_mask2, _runs
V="/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"
CX,CY,CW,CH=790,370,340,150
def pbar(a):
    m=green_mask2(a); W=(a[...,0]>150)&(a[...,1]>150)&(a[...,2]>145)
    best=None
    for y in range(0,a.shape[0]-1):
        for (s,e) in _runs(m[y],14,90):
            ok=False
            for (s2,e2) in _runs(m[y+1],10,92):
                if min(e,e2)-max(s,s2)>0.6*min(e-s,e2-s2): ok=True;break
            if not ok: continue
            xc=(s+e)//2
            txt=int(W[max(0,y-34):max(0,y-18), max(0,xc-95):xc+96].sum())
            if txt<60: continue
            c=(s,e,y+1.0,e-s+1)
            if best is None or c[3]>best[3]: best=c
    return best
def run(fps, out):
    cmd=['ffmpeg','-v','error','-ss','683','-t','184','-i',V,'-vf',f'fps={fps},crop={CW}:{CH}:{CX}:{CY}','-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.run(cmd,capture_output=True)
    b=np.frombuffer(p.stdout,dtype=np.uint8); n=len(b)//(CW*CH*3)
    F=b[:n*CW*CH*3].reshape(n,CH,CW,3)
    res=[]
    for i in range(n):
        bb=pbar(F[i])
        res.append((683+i/fps, np.nan,np.nan,np.nan,0) if bb is None else (683+i/fps, bb[0]+CX, bb[1]+CX, bb[2]+CY, bb[3]))
    R=np.array(res); np.save(out,R); return R
if __name__=='__main__':
    R=run(float(sys.argv[1]), sys.argv[2])
    ok=~np.isnan(R[:,1])
    print('n',len(R),'det %.1f%%'%(100*ok.mean()))
    print('x_left  pct', np.percentile(R[ok,1],[0,1,5,25,50,75,95,99,100]).round(1))
    print('y       pct', np.percentile(R[ok,3],[0,1,5,50,95,99,100]).round(1))
    print('w       pct', np.percentile(R[ok,4],[0,5,25,50,75,95,100]).round(1))
