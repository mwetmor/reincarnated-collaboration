# C-5 conductor glue (data, not lane code): migrate the six v19 kits to the T4a material (drop tint/pixel_scale, add pierce, recover the four baked colours as material.palette, index-quantise frames) — T4f build_export.py recipe.
import json, sys, shutil, pathlib
import numpy as np
from PIL import Image
ROOT=pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); sys.path.insert(0,str(ROOT))
from export.effect_kit import build
SRC=ROOT/'runs/C-5/cliffside_v19/vfx'; OUT=ROOT/'runs/C-5/vfx_kits/v9'; 
if OUT.exists(): shutil.rmtree(OUT)
entries=[]; report=[]
for name in ['frozen_orb','blackwater_cocktail','poisonous_concoction','lightning_blast','zeus_chain','healing_hands']:
    source=SRC/name; data=json.loads((source/'kit.json').read_text())
    data.pop('tint',None); data.pop('pixel_scale',None); data['pierce']=-1 if name=='frozen_orb' else 0
    paths={ph['sheet'] for ph in data['phases'].values()}; paths.update(f['file'] for ph in data['phases'].values() for f in ph['frames']); phase_paths=set(paths)
    paths.update(layer[k] for layer in data['layers'].values() if isinstance(layer,dict) for k in ('file','texture') if k in layer)
    colours=set()
    for rel in phase_paths:
        rgba=np.array(Image.open(source/rel).convert('RGBA')); colours.update(map(tuple,np.unique(rgba[rgba[...,3]>0,:3],axis=0)))
    colours=sorted(colours,key=lambda c:sum(map(int,c)))
    if len(colours)!=4: raise SystemExit((name,'expected four authored colours',len(colours)))
    data['material']={'palette':[[float(v)/255 for v in c]+[1.0] for c in colours]}
    inputs=OUT/'definitions'/name
    for rel in paths:
        rgba=np.array(Image.open(source/rel).convert('RGBA')); rgb=rgba[...,:3].copy()
        if rel not in phase_paths: rgba[...,:3]=(np.rint(rgb.max(axis=2)/85.0)*85).astype(np.uint8)[...,None]
        for i,c in enumerate(colours): rgba[...,:3][np.all(rgb==c,axis=2)]=i*85
        rgba[...,:3][rgba[...,3]==0]=0
        t=inputs/rel; t.parent.mkdir(parents=True,exist_ok=True); Image.fromarray(rgba).save(t)
    d=inputs/'effect.json'; d.write_text(json.dumps(data,indent=2)+'\n')
    kit=OUT/name; build(d,kit); entries.append({'name':name,'dir':str(kit)}); report.append({'name':name,'pierce':data['pierce'],'palette':[[round(x,3) for x in p] for p in data['material']['palette']]})
(ROOT/'runs/C-5/vfx_kits').mkdir(exist_ok=True); (ROOT/'runs/C-5/vfx_kits/kits_v9.json').write_text(json.dumps({'kits':entries},indent=2)+'\n')
(OUT/'migration_report.json').write_text(json.dumps(report,indent=1))
print('kits_v9:',[(r['name'],r['pierce']) for r in report])
