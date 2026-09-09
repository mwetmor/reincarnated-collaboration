"""Extract generated sheet cells and register without pose warping."""
from pathlib import Path
import sys,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'run_02'))
from pipeline import extract,registration,measure


def front_contacts(im,exclude_thin_staff=False):
    a=np.array(im)[...,3]>=128;ys,xs=np.where(a)
    cx=(xs.min()+xs.max())/2;floor=ys.min()+.72*(ys.max()-ys.min())
    below=np.zeros_like(a);below[:-1]=a[1:];edge=a&~below
    if exclude_thin_staff:
        # A complete lower-foot component joins heel and toe naturally. Prefer
        # these when both feet separate; overlapping side-view boots still need
        # the global lower-contour fallback below.
        lower=a.copy();lower[:int(ys.min()+.78*(ys.max()-ys.min()))]=False
        components,n=ndimage.label(lower);feet=[]
        for k in range(1,n+1):
            yy,xx=np.where(edge&(components==k))
            if len(xx) and xx.max()-xx.min()>=(ys.max()-ys.min())*.025:
                bottom=yy.max();feet.append([float(np.median(xx[yy>=bottom-1])),float(bottom)])
        feet.sort(key=lambda p:p[1],reverse=True)
        if len(feet)>=2:return sorted(feet[:2],key=lambda p:p[0])
        edge[:int(ys.min()+.78*(ys.max()-ys.min()))]=False
        labels,n=ndimage.label(ndimage.binary_dilation(edge,iterations=max(1,round(im.width/1254*2))))
        candidates=[]
        for k in range(1,n+1):
            yy,xx=np.where(edge&(labels==k))
            if len(xx) and xx.max()-xx.min()>=(ys.max()-ys.min())*.025:
                bottom=yy.max();candidates.append([float(np.median(xx[yy>=bottom-1])),float(bottom)])
        candidates.sort(key=lambda p:p[1],reverse=True)
        selected=[]
        for candidate in candidates:
            if all(np.linalg.norm(np.array(candidate)-point)>(ys.max()-ys.min())*.085 for point in selected):
                selected.append(candidate)
            if len(selected)==2:break
        if len(selected)<2:raise ValueError('Cannot separate two visible sole contours')
        return sorted(selected,key=lambda p:p[0])
    y,x=np.where(edge);points=[]
    for side in [x<cx,x>=cx]:
        choose=side&(y>floor);xx=x[choose];yy=y[choose]
        if not len(yy):raise ValueError('Cannot identify both front-view feet')
        low=yy.max();points.append([float(np.median(xx[yy>=low-1])),float(low)])
    return points


def prepare_sheet(name,anim,direction,start,scale=240/475):
    im=Image.open(ROOT/'source'/f'{name}.png');side=im.width//2
    if im.width!=im.height or im.width%2:raise ValueError('Expected even square 2x2 sheet')
    dest=ROOT/'character/frames'/anim/direction;dest.mkdir(parents=True,exist_ok=True)
    rows=[];review=Image.new('RGBA',(2048,544),(20,25,34,255))
    for i in range(4):
        x=i%2*side;y=i//2*side;cell=im.crop((x,y,x+side,y+side));matte,info=extract(cell)
        points=front_contacts(matte);anchor=np.mean(points,axis=0).tolist()
        frame,transform=registration(matte,{'body_height':475,'anchor':anchor},locked_scale=scale)
        index=start+i
        if not(anim=='idle' and index==0):frame.save(dest/f'{anim}_{direction}_{index:02d}.png')
        outpoints=front_contacts(frame);error=np.abs(np.mean(outpoints,axis=0)-[256,400])
        row=measure(frame);row.update(index=index,source_contacts=points,output_contacts=outpoints,contact_error_xy=error.tolist(),pivot_pass=bool((error<=4).all()),registration=transform,extraction=info)
        rows.append(row);review.alpha_composite(frame,(512*i,32));draw=ImageDraw.Draw(review);draw.text((512*i+10,8),f'{anim} {direction} {index:02d}',fill='white')
        for px,py in outpoints:draw.ellipse((512*i+px-2,py+30,512*i+px+2,py+34),outline='#55ffee')
    (ROOT/'evidence'/f'{name}_metrics.json').write_text(json.dumps(rows,indent=2)+'\n');review.save(ROOT/'evidence'/f'{name}_review.png')
    print(json.dumps([{'index':r['index'],'height':r['height'],'light':r['light_pass'],'pivot_error':r['contact_error_xy']} for r in rows],indent=2))


def loop_metrics(anim,direction):
    files=sorted((ROOT/'character/frames'/anim/direction).glob('*.png'));images=[]
    for f in files:
        bg=Image.new('RGBA',(512,512),(20,25,34,255));bg.alpha_composite(Image.open(f));images.append(np.array(bg)[...,:3].astype(float))
    differences=[float(np.abs(images[i]-images[(i+1)%len(images)]).mean()) for i in range(len(images))]
    return {'frames':[f.name for f in files],'adjacent_plus_seam':differences,'seam_pass':differences[-1]<=min(differences[:-1])}


def prepare_single(name,anim,direction,index,registration_reference=None):
    original=Image.open(ROOT/'source'/f'{name}.png');matte,info=extract(original)
    if anim=='cast':
        from character_matte import refine_blue_edges
        matte,refinement=refine_blue_edges(original,matte);info.update(refinement)
    points=front_contacts(matte,exclude_thin_staff=True);anchor=np.mean(points,axis=0).tolist()
    # Canvas normalization is fixed, independent of each pose's bbox.
    scale=512/original.width;scale_fit=None
    if anim=='walk':
        from head_registration import fit_scale
        scale,scale_fit=fit_scale(matte,Image.open(ROOT/'character/frames/idle'/direction/f'idle_{direction}_00.png'))
    if registration_reference:
        previous=json.loads((ROOT/'evidence'/f'{registration_reference}_metrics.json').read_text())
        scale=previous['registration']['scale'];anchor=previous['registration']['source_anchor']
        scale_fit={'method':'Inherited complete transform from a localized edit target with unchanged framing','reference':registration_reference}
    frame,transform=registration(matte,{'body_height':original.height*240/512,'anchor':anchor},locked_scale=scale)
    dest=ROOT/'character/frames'/anim/direction;dest.mkdir(parents=True,exist_ok=True)
    frame.save(dest/f'{anim}_{direction}_{index:02d}.png')
    outpoints=front_contacts(frame,exclude_thin_staff=True);error=np.abs(np.mean(outpoints,axis=0)-[256,400])
    row=measure(frame);row.update(index=index,source_contacts=points,output_contacts=outpoints,contact_error_xy=error.tolist(),pivot_pass=bool((error<=4).all()),registration=transform,scale_fit=scale_fit,extraction=info)
    (ROOT/'evidence'/f'{name}_metrics.json').write_text(json.dumps(row,indent=2)+'\n')
    return row


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('anim');p.add_argument('direction');p.add_argument('start',type=int);a=p.parse_args();prepare_sheet(a.name,a.anim,a.direction,a.start)
