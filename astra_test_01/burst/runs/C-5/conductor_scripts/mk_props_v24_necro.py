# Conductor glue (C-6 → C-5 PACK v23): key the N3 camera master on green, scale by FIGURE height (240-px figure in the 512 cell → 146 px = 13.5 % of 1080), place on the path.
# usage: mk_props_v23_necro.py <master_png> <figure_px_in_source> <level_x> <level_y>
import sys, json, shutil, pathlib
import numpy as np; from PIL import Image
B=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
src=pathlib.Path(sys.argv[1]); fig_src=float(sys.argv[2]); x,y=float(sys.argv[3]),float(sys.argv[4])
H_TARGET=float(sys.argv[5]) if len(sys.argv)>5 else 151.0
im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(int)
key=(a[...,1]>180)&(a[...,0]<110)&(a[...,2]<110)
rgba=np.dstack([a[...,:3].astype(np.uint8), np.where(key,0,255).astype(np.uint8)])
ys,xs=np.where(~key); crop=Image.fromarray(rgba,'RGBA').crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
s=H_TARGET/fig_src; asset=crop.resize((max(1,round(crop.size[0]*s)),max(1,round(crop.size[1]*s))),Image.LANCZOS)
src_props=B/'runs/C-5/artifacts/CS-props-v19'; dst=B/'runs/C-5/artifacts/CS-props-v24'
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src_props,dst); (dst/'assets').mkdir(exist_ok=True); asset.save(dst/'assets'/'necro_master_still.png')
pj=json.load(open(dst/'props.json')); w,h=asset.size
pj['assets'].append({'name':'necro_master_still','file':'assets/necro_master_still.png','anchor':[w/2.0,float(h)],'footprint':{'w':round(min(w,110)*0.8,1),'h':round(min(w,110)*0.35,1),'offset':[0,0],'shape':'ellipse'},'collide':True,'fade_when_behind':False})
pj['instances'].append({'asset':'necro_master_still','position':[x,y]})
json.dump(pj,open(dst/'props.json','w'),indent=1)
print('asset',asset.size,'scale',round(s,4),'placed at',(x,y),'assets',len(pj['assets']),'instances',len(pj['instances']))
# F-C5-9 (Matt 2026-09-16): the cow_flies swarm never moved with the carcass (v19 moved the cow to 4600,830; the swarm stayed at 4233,554). Re-seat the swarm over the carcass.
pj=json.load(open(dst/'props.json')); cow=[i for i in pj['instances'] if i['asset']=='cow_carcass'][0]['position']
for s in pj.get('swarms',[]):
    if s['name']=='cow_flies': s['position']=[round(cow[0]-20.0,1), round(cow[1]-70.0,1)]; s['sort_y']=float(cow[1]); print('cow_flies re-seated at',s['position'],'sort_y',s['sort_y'])
json.dump(pj,open(dst/'props.json','w'),indent=1)
