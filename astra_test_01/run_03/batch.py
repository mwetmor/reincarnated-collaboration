"""Prepare 2x2 layout-conditioned cells with one fixed canvas scale."""
import argparse,json
import numpy as np
from PIL import Image,ImageDraw
from animation import ROOT,extract,registration,measure,front_contacts
from character_matte import refine_blue_edges

def prepare(name,anim,direction,start,specs=None):
    original=Image.open(ROOT/'source'/f'{name}.png');side=original.width//2
    if original.width!=original.height or side<512:raise ValueError('Invalid native cell dimensions')
    dest=ROOT/'character/frames'/anim/direction;dest.mkdir(parents=True,exist_ok=True)
    rows=[];review=Image.new('RGBA',(2048,544),(20,25,34,255));draw=ImageDraw.Draw(review)
    for i in range(4):
        if specs:
            anim,direction,index=specs[i];dest=ROOT/'character/frames'/anim/direction;dest.mkdir(parents=True,exist_ok=True)
        cell=original.crop((i%2*side,i//2*side,(i%2+1)*side,(i//2+1)*side));matte,info=extract(cell)
        if anim=='cast':matte,extra=refine_blue_edges(cell,matte);info.update(extra)
        points=front_contacts(matte,exclude_thin_staff=True);anchor=np.mean(points,axis=0).tolist()
        # Layout cell is an unscaled 640px crop of the 1024px native reference.
        # Output image may change canvas dimensions, but every cell uses this
        # identical conversion. No per-pose silhouette fitting.
        scale=320/side
        frame,transform=registration(matte,{'body_height':480,'anchor':anchor},locked_scale=scale)
        if not specs:index=start+i
        if anim=='idle' and index==0:frame=Image.open(dest/f'idle_{direction}_00.png').convert('RGBA')
        else:frame.save(dest/f'{anim}_{direction}_{index:02d}.png')
        actual=front_contacts(frame,exclude_thin_staff=True);error=np.abs(np.mean(actual,axis=0)-[256,400]);row=measure(frame)
        row.update(index=index,source_contacts=points,output_contacts=actual,contact_error_xy=error.tolist(),pivot_pass=bool((error<=4).all()),registration=transform,extraction=info)
        rows.append(row);review.alpha_composite(frame,(i*512,32));draw.text((i*512+8,8),f'{anim} {direction} {index:02d}',fill='white')
        for x,y in actual:draw.ellipse((i*512+x-2,y+30,i*512+x+2,y+34),outline='#55ffee')
    (ROOT/'evidence'/f'{name}_metrics.json').write_text(json.dumps(rows,indent=2)+'\n');review.save(ROOT/'evidence'/f'{name}_review.png')
    print(json.dumps([dict(index=r['index'],height=r['height'],light=r['light_pass'],pivot=r['pivot_pass'],error=r['contact_error_xy']) for r in rows]))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('anim');p.add_argument('direction');p.add_argument('start',type=int);a=p.parse_args();prepare(a.name,a.anim,a.direction,a.start)
