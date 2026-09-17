# Conductor data prep (C-6 P1): the N3 animation master re-plated at the Keeper's still canvas — 512x512, FIGURE 240 px
# sole-to-crown (the blade rises above), feet on the ground line y~480, flat #00ff00 plate. Same shape as C-3's K1p master.
import sys, numpy as np, pathlib
from PIL import Image
B=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
src=B/'runs/C-6/artifacts/N3-final-cam-01/necro_final_cam.png'; dst=B/'runs/C-6/artifacts/N3-final-cam-01/necro_master_S_512.png'
a=np.asarray(Image.open(src).convert('RGB')).astype(int)
key=(a[...,1]>150)&(a[...,0]<120)&(a[...,2]<120)
rgba=np.dstack([a.astype(np.uint8), np.where(key,0,255).astype(np.uint8)])
ys,xs=np.nonzero(~key); crop=Image.fromarray(rgba,'RGBA').crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
FIG_SRC=567.0  # torso-column rows 401..967 measured on the N3 master (ledger M-C6-N3-CAM: 566)
s=240.0/FIG_SRC; w,h=crop.size; asset=crop.resize((round(w*s),round(h*s)),Image.LANCZOS)
plate=Image.new('RGBA',(512,512),(0,255,0,255))
feet_y=480; x=(512-asset.size[0])//2; y=feet_y-asset.size[1]
plate.alpha_composite(asset,(x,y)); plate.convert('RGB').save(dst)
print('wrote',dst.name,'asset',asset.size,'scale',round(s,4),'placed',(x,y),'top y',y,'feet y',feet_y)
