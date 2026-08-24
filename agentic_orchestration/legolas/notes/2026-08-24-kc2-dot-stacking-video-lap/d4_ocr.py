"""D-4 HP-orb OCR — bootstrapped from Lap K labels.
ROI + mask follow Lap K I-1 (x 578..696, y 1009..1021; white ink R>140 & G>140 & B>128),
widened to x566..706 / y1002..1028 to guarantee no glyph touches an edge.
Templates are LEARNED from eor-test-2 frames whose value Lap K already certified, so the
label source is a prior MEASURED instrument, never an assumption about the font.
"""
import numpy as np, subprocess, csv
CX,CY,CW,CH = 566,1002,140,26
FPS=60.0
def stream(path, t0=None, t1=None):
    cmd=['ffmpeg','-v','error']
    if t0 is not None: cmd += ['-ss',str(t0)]
    cmd += ['-i',path]
    if t1 is not None: cmd += ['-t',str(t1-(t0 or 0))]
    cmd += ['-vf',f'crop={CW}:{CH}:{CX}:{CY}','-pix_fmt','rgb24','-f','rawvideo','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,bufsize=10**8)
    n=CW*CH*3; i=0
    while True:
        b=p.stdout.read(n)
        if len(b)<n: break
        yield i, np.frombuffer(b,np.uint8).reshape(CH,CW,3)
        i+=1
    p.stdout.close(); p.wait()

def mask_of(img):
    r,g,b=img[:,:,0].astype(int),img[:,:,1].astype(int),img[:,:,2].astype(int)
    return (r>140)&(g>140)&(b>128)

def boxes(m, min_w=2, max_w=16):
    """Lap K gate G3: any box touching a ROI edge is REJECTED (clipping / HUD furniture)."""
    cols=m.sum(0); on=cols>0; out=[]; s=None
    W=len(on)
    for i,v in enumerate(on):
        if v and s is None: s=i
        elif not v and s is not None:
            out.append((s,i)); s=None
    if s is not None: out.append((s,W))
    return [(a,b) for a,b in out
            if min_w<=(b-a)<=max_w and a>0 and b<W]

def norm(bm, H=18, W=12):
    ys=np.where(bm.any(1))[0]
    if len(ys)==0: return None
    bm=bm[ys[0]:ys[-1]+1]
    from PIL import Image
    im=Image.fromarray((bm*255).astype(np.uint8)).resize((W,H), Image.BILINEAR)
    a=np.asarray(im,dtype=float)/255.0
    a=a-a.mean(); n=np.linalg.norm(a)
    return a/n if n>0 else None

def ncc(a,b): return float((a*b).sum())
