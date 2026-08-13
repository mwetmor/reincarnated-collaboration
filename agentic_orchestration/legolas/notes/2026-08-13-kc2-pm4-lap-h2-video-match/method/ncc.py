"""Independent camera-displacement check by normalised cross-correlation of a TERRAIN
patch between two frames. Terrain patch chosen automatically as the 160x160 window in
the frame with the highest gradient energy and lowest brightness (i.e. structured stone,
not VFX). Search over +-400 px."""
import numpy as np, subprocess, sys
V="/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"
def frm(t):
    p=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True)
    return np.frombuffer(p.stdout,dtype=np.uint8)[:1920*1080].reshape(1080,1920).astype(np.float32)
def ncc_shift(A,B,patch=(160,160),search=400):
    H,W=A.shape; ph,pw=patch
    best=None
    # candidate patch centres on a grid in the terrain band
    cands=[]
    for cy in range(260,760,60):
        for cx in range(300,1620,80):
            p=A[cy-ph//2:cy+ph//2, cx-pw//2:cx+pw//2]
            if p.shape!=(ph,pw): continue
            gy=np.diff(p,axis=0); gx=np.diff(p,axis=1)
            score=(np.abs(gy).mean()+np.abs(gx).mean())/(1+p.mean()/40.0)
            cands.append((score,cy,cx))
    cands.sort(reverse=True)
    results=[]
    for score,cy,cx in cands[:6]:
        T=A[cy-ph//2:cy+ph//2, cx-pw//2:cx+pw//2]
        T=T-T.mean(); tn=np.sqrt((T*T).sum())
        bb=(-1e9,0,0)
        for dy in range(-search,search+1,2):
            y0=cy-ph//2+dy
            if y0<0 or y0+ph>H: continue
            for dx in range(-search,search+1,2):
                x0=cx-pw//2+dx
                if x0<0 or x0+pw>W: continue
                S=B[y0:y0+ph, x0:x0+pw]; S=S-S.mean()
                d=np.sqrt((S*S).sum())
                if d<1e-6: continue
                v=float((T*S).sum()/(tn*d))
                if v>bb[0]: bb=(v,dx,dy)
        results.append((bb[0],bb[1],bb[2],cy,cx))
    return results
if __name__=='__main__':
    t0,t1=float(sys.argv[1]),float(sys.argv[2])
    A,B=frm(t0),frm(t1)
    for v,dx,dy,cy,cx in ncc_shift(A,B):
        print(f'  patch@({cx},{cy})  ncc={v:.3f}  dx={dx:+5d} dy={dy:+5d}  |d|={np.hypot(dx,dy):6.1f}')
