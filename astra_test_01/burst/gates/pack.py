"""Character and VFX pixel packing, ported from run_03 package.py / vfx.py."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from .common import DIRS,COUNTS,rgba


def package(frames_dir,out_dir):
    root=Path(frames_dir);out=Path(out_dir)
    character={'status':'IN_PROGRESS','directions':DIRS,'canvas':[512,512],'pivot':[256,400],'cast_spawn_index':5,'animations':{}}
    total=0
    for anim,count in COUNTS.items():
        sheet=Image.new('RGBA',(count*512,8*512));entries=[];available={}
        for row,d in enumerate(DIRS):
            files=sorted((root/anim/d).glob('*.png'));available[d]=len(files)
            seen=set()
            for f in files:
                index=int(f.stem.split('_')[-1])
                if not 0<=index<count or index in seen:raise ValueError('Invalid or duplicate frame index')
                seen.add(index);im=rgba(f)
                if im.size!=(512,512):raise ValueError('Character frame canvas must be 512x512')
                rect=[index*512,row*512,512,512];sheet.paste(im,tuple(rect[:2]))
                entries.append(dict(direction=d,index=index,rect=rect,file='frames/'+f.relative_to(root).as_posix()))
        total+=len(entries)
        for folder,im in [('sheets',sheet),('contact',sheet.resize((sheet.width//4,sheet.height//4),Image.Resampling.LANCZOS))]:
            path=out/folder;path.mkdir(parents=True,exist_ok=True);im.save(path/f'{anim}.png')
        character['animations'][anim]={'sheet':f'sheets/{anim}.png','fps':{'idle':8,'walk':10,'cast':16}[anim],'loop':anim!='cast','count':count,'available':available,'frames':entries}
    character.update(available_frames=total,required_frames=224)
    if total==224:character['status']='FRAMES_COMPLETE_ACCEPTANCE_PENDING'
    out.mkdir(parents=True,exist_ok=True);(out/'atlas.json').write_text(json.dumps(character,indent=2)+'\n')
    return character


def composite_sockets(frames_dir):
    """Literal blue-frost selection and reviewed recovery sockets from package.py."""
    root=Path(frames_dir);sockets={}
    for d in ['S','E']:
        sockets[d]=[]
        for i in range(12):
            a=np.array(rgba(root/f'cast/{d}/cast_{d}_{i:02d}.png')).astype(float)
            mask=(a[...,2]>a[...,0]+25)&(a[...,2]>90)&(a[...,3]>64)
            mask[280:]=False;ys,xs=np.where(mask)
            sockets[d].append([float(np.median(xs)),float(np.median(ys))] if len(xs) else None)
        sockets[d][8]={'S':[201,166],'E':[277,155]}[d]
        if any(sockets[d][i] is None for i in range(2,9)):raise ValueError(f'Missing active spell socket {d}')
    return sockets


def vfx_atlas(sizes=None,counts=None,pack_module=None, *, frames_dir=None,out_dir=None):
    """Pack pixels internally when frames_dir/out_dir supplied; legacy callback optional."""
    sizes=VFX_SIZES if sizes is None else sizes
    counts=VFX_COUNTS if counts is None else counts
    if pack_module is None:
        if frames_dir is None or out_dir is None:
            raise ValueError('frames_dir and out_dir required without legacy callback')
        pack_module=lambda module: pack_vfx(module,frames_dir,out_dir,sizes=sizes)
    data={'status':'FRAMES_COMPLETE_PLAYBACK_UNVERIFIED','fps':20,'modules':{}}
    for module,count in counts.items():
        pack_module(module);w,h=sizes[module]
        data['modules'][module]={'sheet':f'sheets/{module}.png','emissive':f'sheets/{module}_emissive.png','canvas':[w,h],
          'pivot':[170,64] if module=='travel' else [w//2,h//2],'fps':20,'loop':module=='travel','count':count,
          'frames':[dict(index=i,rect=[i*w,0,w,h],file=f'frames/{module}/{module}_{i:02d}.png') for i in range(count)]}
    return data


VFX_SIZES={'cast':(256,256),'travel':(256,128),'impact':(384,384)}
VFX_COUNTS={'cast':8,'travel':6,'impact':10}

def pack_vfx(module,frames_dir,out_dir,*,sizes=None):
    """Literal run_03/vfx.py pack: straight RGB times alpha -> luminance energy.
    Fixed quarter-size contacts and three review backgrounds are layout constants.
    No emissive threshold or normalization is introduced.
    """
    sizes=VFX_SIZES if sizes is None else sizes
    size=sizes[module];root=Path(frames_dir);out=Path(out_dir)
    files=sorted((root/module).glob('*.png'))
    if not files: raise ValueError('No VFX frames')
    sheet=Image.new('RGBA',(size[0]*len(files),size[1]))
    for i,f in enumerate(files):
        im=rgba(f)
        if im.size!=size:raise ValueError('Unexpected VFX frame canvas')
        sheet.paste(im,(i*size[0],0))
    folder=out/'sheets';folder.mkdir(parents=True,exist_ok=True)
    sheet.save(folder/f'{module}.png')
    a=np.array(sheet).astype(float)
    emission=a[...,:3]*(a[...,3,None]/255)
    lum=emission@np.array([.2126,.7152,.0722])
    Image.fromarray(lum.clip(0,255).astype('uint8')).save(folder/f'{module}_emissive.png')
    contact=out/'contact';contact.mkdir(exist_ok=True)
    sheet.resize((max(1,sheet.width//4),max(1,sheet.height//4)),Image.Resampling.LANCZOS).save(contact/f'{module}.png')
    review=Image.new('RGB',(sheet.width,sheet.height*3+72));draw=ImageDraw.Draw(review)
    for j,(color,label) in enumerate([((20,25,34),'DARK'),((230,233,239),'LIGHT'),((70,80,130),'BLUE')]):
        bg=Image.new('RGBA',sheet.size,(*color,255));bg.alpha_composite(sheet)
        review.paste(bg,(0,j*(sheet.height+24)+24));draw.text((8,j*(sheet.height+24)+4),label,fill='white')
    (out/'evidence').mkdir(exist_ok=True)
    review.save(out/'evidence'/f'vfx_{module}_edges.png')
    return {'frames':len(files),'size':list(sheet.size)}
