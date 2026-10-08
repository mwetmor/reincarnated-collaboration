import sys, numpy as np, json
from PIL import Image, ImageFilter
from scipy.ndimage import binary_fill_holes
D=sys.argv[1]; FIX=sys.argv[2]
L=lambda f: np.asarray(Image.open(D+'/'+f).convert('RGB')).astype(int)
def cls(a,rgb):
    on=a>200; off=a<55; m=np.ones(a.shape[:2],bool)
    for c,w in enumerate(rgb): m&= on[...,c] if w else off[...,c]
    return m
IDS=[(1,0,0),(0,1,0),(0,1,1),(1,1,0),(0,0,1),(1,0,1)]
rep={}
for clip in ['idle','walk','cast_fireball_m']:
  for h in ['S','SE','SW','E','W','N','NE','NW']:
    row={}
    foot=L(f'live_{clip}_{h}_z3_foot.png'); F=cls(foot,(1,0,0))
    # the HEAD window: the face footprint grown 18 px (z3), or the hood's top third when the face is turned away
    if F.sum() < 40:
        ida0=L(f'live_{clip}_{h}_z3_ida.png'); hd=cls(ida0,(0,0,1)); ys,xs=np.nonzero(hd); F=np.zeros_like(F); F[ys.min():ys.min()+(ys.max()-ys.min())//2, xs.min():xs.max()]=True
    Wn=np.asarray(Image.fromarray((F*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(37)))>127
    for v,nm in (('live','live'),(FIX,'final')):
      b=L(f'{v}_{clip}_{h}_z3_beauty.png'); ida=L(f'{v}_{clip}_{h}_z3_ida.png')
      her=np.zeros(b.shape[:2],bool)
      for c in IDS: her|=cls(ida,c)
      holes=binary_fill_holes(her)&~her&Wn
      lum=0.2126*b[...,0]+0.7152*b[...,1]+0.0722*b[...,2]
      m=her&Wn
      row[nm]=dict(see_through_px=int(holes.sum()), clipped_px=int(((b.max(2)>=250)&(m|holes)).sum()), white_px=int(((lum>=235)&(m|holes)).sum()), p99=round(float(np.percentile(lum[m],99)),1) if m.any() else None, max=int(b[m].max()) if m.any() else None)
    rep[f'{clip}_{h}']=row
    print('%-6s %-2s'%(clip[:6],h), ' | '.join('%s holes=%d clip=%d white=%d p99=%s max=%s'%(k,r['see_through_px'],r['clipped_px'],r['white_px'],r['p99'],r['max']) for k,r in row.items()))
json.dump(rep,open(D+'/head_clip_check.json','w'),indent=1)
