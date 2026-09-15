"""Signed-haze cut (conductor glue): sheet on a hazy background -> 64 px painted-pixel frames. Brighter-than-haze pixels map to
light bands by excess; darker-than-haze pixels (objects like the flask body) become the dark band. usage: cut_signed.py SHEET OUT [N]"""
import sys, json, pathlib, numpy as np
from PIL import Image
from scipy import ndimage
sheet=np.array(Image.open(sys.argv[1]).convert('L')).astype(np.float32)/255; OUT=pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True,exist_ok=True); N=int(sys.argv[3]) if len(sys.argv)>3 else 64
H,W=sheet.shape; cw,ch=W//6,H//4; ROWS=['cast','travel','impact','residual']; rec={}
for r,ph in enumerate(ROWS):
    for c in range(6):
        cell=sheet[r*ch:(r+1)*ch, c*cw:(c+1)*cw]
        haze=ndimage.gaussian_filter(ndimage.median_filter(cell, size=61), 8)
        light=np.clip(cell-haze,0,1); dark=np.clip(haze-cell,0,1)
        for a_ in (light,dark): a_[:14]=a_[-14:]=0; a_[:,:14]=a_[:,-14:]=0
        top=max(np.percentile(light,99.5),0.05); light=np.clip(light/top,0,1)
        Ls=np.array(Image.fromarray((light*255).astype(np.uint8)).resize((N,N),Image.BOX)).astype(np.float32)/255
        Ds=np.array(Image.fromarray((np.clip(dark/float(sys.argv[4] if len(sys.argv)>4 else 0.18),0,1)*255).astype(np.uint8)).resize((N,N),Image.BOX)).astype(np.float32)/255
        lvl=np.zeros((N,N),np.float32); a=np.zeros((N,N),np.float32)
        for lo,v in ((0.9,1.0),(0.6,0.68),(0.35,0.42)):
            sel=(Ls>=lo)&(a==0); lvl[sel]=v; a[sel]=1
        sel=(Ds>=float(sys.argv[5] if len(sys.argv)>5 else 0.5))&(a==0); lvl[sel]=0.18; a[sel]=1
        lab,n=ndimage.label(a>0); sizes=ndimage.sum(a>0,lab,range(1,n+1)); keep=np.isin(lab,[i+1 for i,s in enumerate(sizes) if s>=3]); a*=keep; lvl*=keep
        g=(lvl*255).astype(np.uint8); Image.fromarray(np.dstack([g,g,g,(a*255).astype(np.uint8)]),'RGBA').save(OUT/f'{ph}_{c:02d}.png')
        rec[f'{ph}_{c:02d}.png']={'opaque_px':int((a>0).sum()),'white_frac':round(float(((lvl>=.99)&(a>0)).sum()/max(1,(a>0).sum())),3),'dark_frac':round(float(((lvl<.2)&(a>0)).sum()/max(1,(a>0).sum())),3)}
json.dump(rec,open(OUT/'frames.json','w'),indent=1)
prev=Image.new('RGB',(6*N*4,4*N*4),(40,42,50))
for r,ph in enumerate(ROWS):
    for c in range(6):
        im=Image.open(OUT/f'{ph}_{c:02d}.png').resize((N*4,N*4),Image.NEAREST); prev.paste(im,(c*N*4,r*N*4),im)
prev.save(OUT/'preview_x4.png'); print({k:v for k,v in rec.items() if k in ('travel_02.png','impact_03.png','residual_01.png')})
