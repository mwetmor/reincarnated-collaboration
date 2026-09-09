"""Pack real frames with explicit availability; never advertise missing cells."""
import json
from PIL import Image
from check import DIRS,COUNTS
from animation import ROOT
from vfx import SIZES,COUNTS as VFX_COUNTS,pack

def save(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')

def package():
    character={'status':'IN_PROGRESS','directions':DIRS,'canvas':[512,512],'pivot':[256,400],'cast_spawn_index':5,'animations':{}}
    total=0
    for anim,count in COUNTS.items():
        sheet=Image.new('RGBA',(count*512,8*512));entries=[];available={}
        for row,d in enumerate(DIRS):
            files=sorted((ROOT/'character/frames'/anim/d).glob('*.png'));available[d]=len(files)
            for f in files:
                index=int(f.stem.split('_')[-1]);rect=[index*512,row*512,512,512];sheet.paste(Image.open(f),tuple(rect[:2]));entries.append(dict(direction=d,index=index,rect=rect,file=str(f.relative_to(ROOT/'character'))))
        total+=len(entries)
        for folder,im in [('sheets',sheet),('contact',sheet.resize((sheet.width//4,sheet.height//4),Image.Resampling.LANCZOS))]:
            path=ROOT/'character'/folder;path.mkdir(exist_ok=True);im.save(path/f'{anim}.png')
        character['animations'][anim]={'sheet':f'sheets/{anim}.png','fps':{'idle':8,'walk':10,'cast':16}[anim],'loop':anim!='cast','count':count,'available':available,'frames':entries}
    character.update(available_frames=total,required_frames=224)
    save(ROOT/'character/atlas.json',character)
    vfx={'status':'FRAMES_COMPLETE_PLAYBACK_UNVERIFIED','fps':20,'modules':{}}
    for module,count in VFX_COUNTS.items():
        pack(module);w,h=SIZES[module]
        # Travel core is 2/3 across the cell; centerline is registered to y64.
        pivot=[170,64] if module=='travel' else [w//2,h//2]
        vfx['modules'][module]={'sheet':f'sheets/{module}.png','emissive':f'sheets/{module}_emissive.png','canvas':[w,h],'pivot':pivot,'fps':20,'loop':module=='travel','count':count,'frames':[dict(index=i,rect=[i*w,0,w,h],file=f'frames/{module}/{module}_{i:02d}.png') for i in range(count)]}
    save(ROOT/'vfx/atlas.json',vfx)
    # Blue frost centroid supplies an explicit socket per actual S/E frame.
    import numpy as np
    sockets={}
    for d in ['S','E']:
        sockets[d]=[]
        for i in range(12):
            a=np.array(Image.open(ROOT/f'character/frames/cast/{d}/cast_{d}_{i:02d}.png')).astype(float)
            mask=(a[...,2]>a[...,0]+25)&(a[...,2]>90)&(a[...,3]>64)
            mask[280:]=False;ys,xs=np.where(mask)
            sockets[d].append([float(np.median(xs)),float(np.median(ys))] if len(xs) else None)
        # Unglowed frames need no VFX socket. Active cast frames must have one.
        # Reviewed unglowed fork centers from actual recovery frame 08.
        sockets[d][8]={'S':[201,166],'E':[277,155]}[d]
        if any(sockets[d][i] is None for i in range(2,9)):raise ValueError(f'Missing active spell socket {d}')
    save(ROOT/'evidence/composite_sockets.json',sockets)
    html=(ROOT/'preview_template.html').read_text().replace('__ASSET_DATA__',json.dumps(dict(character=character,vfx=vfx,sockets=sockets)))
    (ROOT/'preview').mkdir(exist_ok=True);(ROOT/'preview/index.html').write_text(html)
    print(json.dumps(dict(character_frames=total,vfx_frames=24,browser='UNVERIFIED')))

if __name__=='__main__':package()
