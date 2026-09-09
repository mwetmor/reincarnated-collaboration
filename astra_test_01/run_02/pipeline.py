"""Prepare generated painted sprites. No character drawing or pose synthesis.

Input art remains immutable. Native alpha is retained; green plates use recorded
chroma matting. Registration uses only uniform downscale and translation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / 'config.json').read_text())


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def extract(image):
    a = np.array(image.convert('RGBA')).astype(float)
    native = bool('A' in image.getbands() and np.mean(a[..., 3] == 0) > .01)
    if native:
        method = 'native alpha'
        out = a.astype(np.uint8)
    else:
        rgb = a[..., :3]
        border = np.concatenate([rgb[:10].reshape(-1,3),rgb[-10:].reshape(-1,3),
                                 rgb[:,:10].reshape(-1,3),rgb[:,-10:].reshape(-1,3)])
        green_fraction = float(np.mean((border[:,1] > 210) &
                                       (border[:,0] < 45) & (border[:,2] < 45)))
        if green_fraction < .95:
            raise ValueError(f'No native alpha or uniform green plate: border green fraction {green_fraction:.4f}')
        excess = rgb[...,1] - np.maximum(rgb[...,0],rgb[...,2])
        alpha = np.clip(1 - excess / 255, 0, 1)
        alpha[excess <= 12] = 1
        alpha[excess >= 250] = 0
        clean = (rgb - (1-alpha[...,None])*np.array([0,255,0])) / np.maximum(alpha[...,None],1e-6)
        out = np.dstack([np.clip(clean,0,255),alpha*255]).round().astype(np.uint8)
        method = 'green excess matte + inverse straight-alpha compositing'
    # Remove only detached alpha dust, never dark character pixels.
    labels, n = ndimage.label(out[...,3] >= 128)
    counts = np.bincount(labels.ravel())
    counts[0] = 0
    main_component = int(counts.argmax())
    support = ndimage.binary_dilation(labels == main_component, iterations=3)
    dust = int(np.count_nonzero((out[...,3]>0) & ~support))
    out[~support] = 0
    out[out[...,3] == 0, :3] = 0
    mask = out[...,3] >= 128
    if mask.sum() < 100:
        raise ValueError('Empty extracted subject')
    return Image.fromarray(out), {'method':method, 'removed_background_or_detached_alpha_dust_pixels':dust,
                                'native_input_alpha':native}


def registration(image, annotations, size=512, locked_scale=None):
    scale = locked_scale if locked_scale is not None else 240 / annotations['body_height']
    scale *= size / 512
    if scale > 1:
        raise ValueError('Would upscale source artwork')
    if image.width != image.height:
        raise ValueError('Character source must be square')
    scaled_side = round(image.width * scale)
    scale = scaled_side / image.width
    anchor = np.array(annotations['anchor'],float)
    target = np.array([256,400],float) * size / 512
    translation = target-scale*anchor
    reduced=image.resize((scaled_side,scaled_side),Image.Resampling.LANCZOS)
    inverse = (1,0,-translation[0],0,1,-translation[1])
    # Prefilter the reduction; Pillow uses associated-alpha for RGBA sampling.
    result=reduced.transform((size,size),Image.Transform.AFFINE,inverse,
                           resample=Image.Resampling.BICUBIC)
    pixels=np.array(result)
    excess=pixels[...,1].astype(float)-np.maximum(pixels[...,0],pixels[...,2])
    spill=(pixels[...,3]>0)&(pixels[...,3]<246)&(excess>12)
    pixels[spill,1]=np.maximum(pixels[spill,0],pixels[spill,2])
    pixels[pixels[...,3]==0,:3]=0
    result=Image.fromarray(pixels)
    points={name:(np.array(point)*scale+translation).tolist()
            for name,point in annotations.get('landmarks',{}).items()}
    points['registered_anchor']=(anchor*scale+translation).tolist()
    return result, {'scale':scale, 'translation':translation.tolist(),
                    'resampled_green_edge_pixels_despilled':int(spill.sum()),
                    'source_anchor':anchor.tolist(),'transformed_landmarks':points,
                    'body_height_after_transform':annotations['body_height']*scale,
                    'transform_generated_anchor_is_not_independent_validation':True}


def measure(image):
    a=np.array(image.convert('RGBA')); mask=a[...,3]>=128
    ys,xs=np.where(mask)
    if not len(xs): return {'valid':False}
    box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
    lum=a[...,:3].astype(float)@np.array([.2126,.7152,.0722])
    n=math.ceil(len(xs)*.05)
    ix=np.argsort(lum[mask],kind='stable')[-n:]
    c=[float(xs[ix].mean()),float(ys[ix].mean())]
    center=[(box[0]+box[2]-1)/2,(box[1]+box[3]-1)/2]
    edge=(a[...,3]>0)&(a[...,3]<255)
    green_excess=a[...,1].astype(float)-np.maximum(a[...,0],a[...,2])
    border=np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])
    return {'valid':True,'bbox':box,'height':box[3]-box[1],
            'transparent_fraction':float(np.mean(a[...,3]==0)),
            'border_alpha_max':int(border.max()),'light_centroid':c,'silhouette_center':center,
            'light_pass':bool(c[0]<center[0] and c[1]<center[1]),
            'brightest_5pct_pixels':n,'partial_alpha_pixels':int(edge.sum()),
            'edge_mean_rgb_value':float(a[...,:3][edge].mean()) if edge.any() else None,
            'green_contaminated_pixels':int(np.count_nonzero(edge & (green_excess>20)))}


def review(image, target):
    # Comparison evidence is explicitly separate from the production frame.
    plate=Image.new('RGB',(image.width*3,image.height+32))
    d=ImageDraw.Draw(plate)
    for j,(color,label) in enumerate([((20,25,34),'DARK'),((225,229,235),'LIGHT'),((75,85,130),'BLUE')]):
        bg=Image.new('RGBA',image.size,(*color,255));bg.alpha_composite(image)
        plate.paste(bg.convert('RGB'),(j*image.width,32))
        d.text((j*image.width+10,10),label,fill='white')
    plate.save(target)


def prepare(name):
    ann=json.loads((ROOT/'annotations.json').read_text())[name]
    src=ROOT/ann['source']; original=Image.open(src)
    matte,details=extract(original)
    outdir=ROOT/'prepared'/name;outdir.mkdir(parents=True,exist_ok=True)
    matte.save(outdir/'matte.png')
    frame,transform=registration(matte,ann,locked_scale=ann.get('locked_scale'))
    frame.save(outdir/'frame.png')
    reference,_=registration(matte,ann,size=1024,locked_scale=ann.get('locked_scale'))
    reference.save(outdir/'reference_alpha.png')
    green=Image.new('RGBA',reference.size,(0,255,0,255));green.alpha_composite(reference)
    green.convert('RGB').save(outdir/'reference_green.png')
    review(frame,outdir/'edge_review.png')
    result={'name':name,'source':ann['source'],'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'source_mode':original.mode,'source_size':list(original.size),
            'extraction':details,'registration':transform,
            'raw_metrics':measure(matte),'registered_metrics':measure(frame)}
    save_json(outdir/'metrics.json',result)
    print(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('name');args=p.parse_args();prepare(args.name)
