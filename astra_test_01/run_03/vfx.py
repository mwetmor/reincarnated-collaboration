"""Particle-preserving emission matting and VFX sheet packing."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
SIZES={'cast':(256,256),'travel':(256,128),'impact':(384,384)}
COUNTS={'cast':8,'travel':6,'impact':10}

def emission_matte(image):
    a=np.array(image.convert('RGBA'));rgb=a[...,:3].astype(float)
    if 'A' in image.getbands() and (a[...,3]==0).mean()>.01:
        return image.convert('RGBA'),{'method':'native alpha','discarded_components':0}
    border=np.concatenate([rgb[0],rgb[-1],rgb[:,0],rgb[:,-1]])
    if np.mean(border.max(axis=1)<=3)<.98:raise ValueError('Emission plate border is not uniformly black')
    value=rgb.max(axis=2);alpha=value/255
    color=np.divide(rgb,alpha[...,None],out=np.zeros_like(rgb),where=alpha[...,None]>0)
    out=np.dstack([color,alpha*255]).round().clip(0,255).astype('uint8');out[value<=2]=0
    return Image.fromarray(out),{'method':'black emission plate; alpha=max(RGB), straight RGB=emission/alpha','noise_floor':2,'discarded_components':0}

def edge_metrics(im):
    a=np.array(im.convert('RGBA'));edge=(a[...,3]>0)&(a[...,3]<255)
    border=np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])
    values=a[...,:3][edge].astype(float);lum=values@np.array([.2126,.7152,.0722]) if len(values) else np.array([])
    return {'partial_alpha_pixels':int(edge.sum()),'edge_mean_rgb':float(values.mean()) if len(values) else None,
            'edge_mean_luminance':float(lum.mean()) if len(lum) else None,'edge_luminance_p10':float(np.percentile(lum,10)) if len(lum) else None,
            'border_alpha_max':int(border.max()),'nonzero_alpha_pixels':int((a[...,3]>0).sum())}

def prepare(name,module,start,number=4):
    source=Image.open(ROOT/'source'/f'{name}.png');side=source.width//2;target=SIZES[module]
    if side<max(target):raise ValueError('Insufficient native cell resolution; would upscale')
    out=ROOT/'vfx/frames'/module;out.mkdir(parents=True,exist_ok=True);rows=[]
    for i in range(number):
        x=i%2*side;y=i//2*side;cell=source.crop((x,y,x+side,y+side))
        matte,info=emission_matte(cell)
        if module=='travel':
            # Uniform reduction followed by fixed central crop; no stretching.
            reduced=matte.resize((256,256),Image.Resampling.LANCZOS)
            pixels=np.array(reduced).astype(float)
            energy=(pixels[...,:3].mean(axis=2)*pixels[...,3]/255)**2
            center_y=float((energy*np.arange(256)[:,None]).sum()/energy.sum())
            shift=round(127.5-center_y)
            registered=Image.new('RGBA',(256,256));registered.paste(reduced,(0,shift));reduced=registered
            info.update(centerline_source_y=center_y,vertical_translation_px=shift)
            frame=reduced.crop((0,64,256,192))
        else:frame=matte.resize(target,Image.Resampling.LANCZOS)
        index=start+i;frame.save(out/f'{module}_{index:02d}.png');metrics=edge_metrics(frame);rows.append(dict(index=index,extraction=info,**metrics))
    (ROOT/'evidence'/f'{name}_metrics.json').write_text(json.dumps(rows,indent=2)+'\n');pack(module)
    print(json.dumps(rows,indent=2))

def pack(module):
    size=SIZES[module];files=sorted((ROOT/'vfx/frames'/module).glob('*.png'));sheet=Image.new('RGBA',(size[0]*len(files),size[1]))
    for i,f in enumerate(files):sheet.paste(Image.open(f),(i*size[0],0))
    folder=ROOT/'vfx/sheets';folder.mkdir(parents=True,exist_ok=True);sheet.save(folder/f'{module}.png')
    a=np.array(sheet).astype(float);emission=a[...,:3]*(a[...,3,None]/255);lum=emission@np.array([.2126,.7152,.0722]);Image.fromarray(lum.clip(0,255).astype('uint8')).save(folder/f'{module}_emissive.png')
    contact=ROOT/'vfx/contact';contact.mkdir(exist_ok=True);sheet.resize((max(1,sheet.width//4),max(1,sheet.height//4)),Image.Resampling.LANCZOS).save(contact/f'{module}.png')
    review=Image.new('RGB',(sheet.width,sheet.height*3+72));draw=ImageDraw.Draw(review)
    for j,(color,label) in enumerate([((20,25,34),'DARK'),((230,233,239),'LIGHT'),((70,80,130),'BLUE')]):
        bg=Image.new('RGBA',sheet.size,(*color,255));bg.alpha_composite(sheet);review.paste(bg,(0,j*(sheet.height+24)+24));draw.text((8,j*(sheet.height+24)+4),label,fill='white')
    review.save(ROOT/'evidence'/f'vfx_{module}_edges.png')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('module',choices=SIZES);p.add_argument('start',type=int);p.add_argument('--number',type=int,default=4);a=p.parse_args();prepare(a.name,a.module,a.start,a.number)
