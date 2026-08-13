"""60fps burst extractor + min-projection de-VFX.
Rationale (method note): Grim Dawn skill VFX and floating damage numbers are ADDITIVE-BRIGHT
and transient at 60fps. Body sprites and terrain persist. A per-pixel MINIMUM across a short
burst (K frames, <=0.2 s, during which bodies move <1 px) suppresses transient bright overdraw
and leaves the persistent underlying sprite. This is a de-occlusion instrument, not a
reconstruction: it can only REMOVE bright overlay, never invent a body.
"""
import numpy as np, subprocess, os, sys
from PIL import Image
V="/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4"

def grab(s, dur, crop=(1920,1080,0,0), fps=60):
    cw,ch,cx,cy=crop
    vf=f"fps={fps},crop={cw}:{ch}:{cx}:{cy}"
    cmd=['ffmpeg','-v','error','-ss',str(s),'-t',str(dur),'-i',V,'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.run(cmd,capture_output=True)
    b=np.frombuffer(p.stdout,dtype=np.uint8)
    n=len(b)//(cw*ch*3)
    return b[:n*cw*ch*3].reshape(n,ch,cw,3)

def minproj(F, K=7, stride=6):
    """sliding min-projection; returns (list of (idx_center, img))"""
    out=[]
    for i in range(0, len(F)-K+1, stride):
        out.append((i+K//2, F[i:i+K].min(axis=0)))
    return out

if __name__=='__main__':
    s=float(sys.argv[1]); dur=float(sys.argv[2]); tag=sys.argv[3]
    cw,ch,cx,cy=[int(x) for x in sys.argv[4].split(':')] if len(sys.argv)>4 else (1920,1080,0,0)
    K=int(sys.argv[5]) if len(sys.argv)>5 else 7
    stride=int(sys.argv[6]) if len(sys.argv)>6 else 6
    F=grab(s,dur,(cw,ch,cx,cy))
    print('frames',len(F),file=sys.stderr)
    od=f'/tmp/pm4h2/work/{tag}'; os.makedirs(od,exist_ok=True)
    for i,img in minproj(F,K,stride):
        t=s+i/60.0
        Image.fromarray(img).save(f'{od}/{tag}_{t:.3f}.jpg',quality=88)
    # also raw frames at same instants for comparison
    od2=f'/tmp/pm4h2/work/{tag}_raw'; os.makedirs(od2,exist_ok=True)
    for i,_ in minproj(F,K,stride):
        t=s+i/60.0
        Image.fromarray(F[i]).save(f'{od2}/{tag}r_{t:.3f}.jpg',quality=88)
    print('done',od,file=sys.stderr)
