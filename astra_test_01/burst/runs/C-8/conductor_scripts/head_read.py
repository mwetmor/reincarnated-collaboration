# Conductor head-read for a Grok clip (R-C6-11 mandate): every 6th frame → figure strip + head-crop grid for the eye. usage: head_read.py <cell_name> [<mp4 relpath>]
import sys, glob, subprocess, pathlib
from PIL import Image, ImageDraw
import numpy as np
B=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); S=pathlib.Path('/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c798c4cb-f5ae-4f80-8419-ca68760f2e6f/scratchpad')
cell=sys.argv[1]; mp4=B/(sys.argv[2] if len(sys.argv)>2 else f'runs/C-8/xvideo/in/{cell}.mp4')
fd=S/f'frames_{cell}'; fd.mkdir(exist_ok=True)
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(mp4),'-vf','select=not(mod(n\\,6))','-vsync','vfr',str(fd/'f_%03d.png')],check=True)
fs=sorted(glob.glob(str(fd/'f_*.png'))); ims=[Image.open(f).convert('RGB') for f in fs]; w,h=ims[0].size
def bbox(im):
    a=np.asarray(im).astype(int); fg=~((a[...,1]>150)&(a[...,0]<120)&(a[...,2]<120)); ys,xs=np.nonzero(fg); return xs.min(),ys.min(),xs.max(),ys.max()
# union bbox over frames 12.. (after any stance-transition opening)
bbs=[bbox(im) for im in ims[2:]] or [bbox(ims[0])]; x0=min(b[0] for b in bbs); y0=min(b[1] for b in bbs); x1=max(b[2] for b in bbs); y1=max(b[3] for b in bbs)
H=420; strip=[]
for im in ims[::2]:
    c=im.crop((max(0,x0-30),max(0,y0-20),min(w,x1+30),min(h,y1+20))); s=H/c.size[1]; strip.append(c.resize((round(c.size[0]*s),H),Image.LANCZOS))
W=sum(i.size[0] for i in strip)+6*(len(strip)+1); sheet=Image.new('RGB',(W,H+24),(58,63,74)); d=ImageDraw.Draw(sheet); x=6
for i,im in enumerate(strip): sheet.paste(im,(x,20)); d.text((x+4,3),f'f{i*12}',fill='white'); x+=im.size[0]+6
sheet.save(S/f'{cell}_strip.png')
# head band: the CROWN is the topmost figure pixel inside the body's centre column (the blade sits off to one side); band = crown .. crown + 22 % of figure height
def head_box(im):
    a=np.asarray(im).astype(int); fg=~((a[...,1]>150)&(a[...,0]<120)&(a[...,2]<120)); ys,xs=np.nonzero(fg)
    feet=ys.max(); fx=xs[ys>feet-40]; cx=int(np.median(fx)); fw=x1-x0; band=fg[:, max(0,cx-int(fw*0.12)):cx+int(fw*0.12)]
    rows=np.nonzero(band.any(1))[0]; crown=int(rows.min()); hh=int((feet-crown)*0.22)
    return (max(0,cx-int(fw*0.28)), max(0,crown-10), min(w,cx+int(fw*0.28)), crown+hh)
hb=head_box(ims[len(ims)//2]); heads=[im.crop(hb) for im in ims]; cw,ch=heads[0].size; cols=7; rows=(len(heads)+cols-1)//cols
grid=Image.new('RGB',(cols*(cw+4)+4, rows*(ch+18)+4),(58,63,74)); d=ImageDraw.Draw(grid)
for i,hm in enumerate(heads):
    gx=4+(i%cols)*(cw+4); gy=4+(i//cols)*(ch+18); grid.paste(hm,(gx,gy+14)); d.text((gx+2,gy),f'f{i*6}',fill='white')
grid.save(S/f'{cell}_heads.png')
# figure-height trace (stance transition / zoom detector): bbox height per sampled frame
hs=[bbox(im)[3]-bbox(im)[1] for im in ims]
print(cell, 'frames', len(ims), 'size', (w,h), 'bbox h per sampled frame:', hs[:6], '...', hs[-3:], '| strip', sheet.size, '| heads', grid.size)
