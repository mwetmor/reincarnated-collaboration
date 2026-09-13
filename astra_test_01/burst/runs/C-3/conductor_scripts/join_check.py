"""Conductor acceptance probe: structural join at a painted strip's inner edge (line 256) inside a new chunk.
Continuity = correlation of the across-line edge profile in the 12 px just before vs just after the line;
compared with the same statistic at control lines. usage: join_check.py chunk.png TOP|LEFT ..."""
import sys, numpy as np
from PIL import Image
im=np.array(Image.open(sys.argv[1]).convert('L')).astype(np.float32)
rgb=np.array(Image.open(sys.argv[1]).convert('RGB')).astype(np.int16)
green=(rgb[...,1]>200)&(rgb[...,0]<80)&(rgb[...,2]<80)
def cont(line, axis, w=12):
    if axis=='TOP':
        g=np.abs(np.diff(im,axis=1)); a=g[line-w:line].mean(0); b=g[line+1:line+1+w].mean(0); ok=~green[line-w:line+w,1:].any(0)
    else:
        g=np.abs(np.diff(im,axis=0)); a=g[:,line-w:line].mean(1); b=g[:,line+1:line+1+w].mean(1); ok=~green[1:,line-w:line+w].any(1)
    if ok.sum()<100: return None
    a=a[ok]; b=b[ok]
    return float(np.corrcoef(a,b)[0,1])
for side in sys.argv[2:]:
    c=cont(256,side); ctrl=[cont(l,side) for l in (150,190,330,370,420)]
    ctrl=[x for x in ctrl if x is not None]
    if c is None or not ctrl: print(side,'n/a'); continue
    print(side,'continuity',round(c,2),'ctrl',round(float(np.median(ctrl)),2),'ratio',round(c/np.median(ctrl),2))
