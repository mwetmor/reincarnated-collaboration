"""Camera translation trace, v2.

The camera is MEASURED rigidly player-locked (player nameplate bar left edge fixed at
screen x=924, y=429; 1,742/1,840 detections over the fight, p5-p75 = 921-924 px).
Therefore camera translation == player world displacement, in screen pixels, exactly.

Lap H's trace ran ~30% high on peaks (its own landmark self-correction). Two changes here:
  * register on the GRADIENT MAGNITUDE of the terrain band, not raw luminance -- terrain
    geometry is high-frequency, VFX glow is low-frequency, so the gradient image is
    terrain-dominated and the correlation peak stops being pulled by moving light
  * sub=2 (960x380) instead of sub=4, halving the quantisation floor
Validated against the Lap H landmark measurement at 732.50-732.75 (nameplate tracked
by hand: 236 px / 0.25 s).
"""
import numpy as np, subprocess, sys
V="/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"

def _ft(f,win):
    f=f.astype(np.float32)
    gy=np.zeros_like(f); gx=np.zeros_like(f)
    gy[1:-1,:]=f[2:,:]-f[:-2,:]
    gx[:,1:-1]=f[:,2:]-f[:,:-2]
    g=np.clip(np.hypot(gx,gy),0,60.0)
    return np.fft.rfft2((g-g.mean())*win)

def trace(s,e,fps,sub=2,band=(100,860)):
    W,H = 1920//sub, (band[1]-band[0])//sub
    vf=f"fps={fps},crop=1920:{band[1]-band[0]}:0:{band[0]},scale={W}:{H},format=gray"
    cmd=['ffmpeg','-v','error','-ss',str(s),'-t',str(e-s),'-i',V,'-vf',vf,'-f','rawvideo','-pix_fmt','gray','-']
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,bufsize=W*H*4)
    win=np.hanning(H)[:,None]*np.hanning(W)[None,:]
    out=[]; prev=None; i=0
    while True:
        raw=proc.stdout.read(W*H)
        if len(raw)<W*H: break
        cur=_ft(np.frombuffer(raw,dtype=np.uint8).reshape(H,W),win)
        if prev is not None:
            R=cur*np.conj(prev); m=np.abs(R); m[m<1e-9]=1e-9
            r=np.fft.irfft2(R/m,s=(H,W))
            k=np.argmax(r); dy,dx=np.unravel_index(k,r.shape); pk=float(r.flat[k])
            def sp(v0,v1,v2):
                d=(v0-2*v1+v2)
                return 0.0 if abs(d)<1e-12 else 0.5*(v0-v2)/d
            sx=sp(r[dy,(dx-1)%W],r[dy,dx],r[dy,(dx+1)%W]); sy=sp(r[(dy-1)%H,dx],r[dy,dx],r[(dy+1)%H,dx])
            if dy>H//2: dy-=H
            if dx>W//2: dx-=W
            out.append([s+(i-1)/fps,(dx+np.clip(sx,-1,1))*sub,(dy+np.clip(sy,-1,1))*sub,pk])
        prev=cur; i+=1
    proc.stdout.close(); proc.wait()
    return np.array(out)

if __name__=='__main__':
    a=trace(683.0,866.75,float(sys.argv[1]) if len(sys.argv)>1 else 20.0)
    np.save('/tmp/pm4h2/cam60g.npy',a)
    mag=np.hypot(a[:,1],a[:,2])
    print('n',len(a),'mag pct',np.percentile(mag,[10,25,50,75,90,95,99,100]).round(2))
    # landmark validation: cumulative displacement 732.50 -> 732.75
    for (t0,t1,ref) in [(732.50,732.75,236.0)]:
        m=(a[:,0]>=t0-1e-6)&(a[:,0]<t1-1e-6)
        d=np.hypot(a[m,1].sum(),a[m,2].sum())
        print(f'landmark {t0}-{t1}: trace={d:.1f} px  LapH hand-landmark={ref} px  ratio={d/ref:.3f}')
