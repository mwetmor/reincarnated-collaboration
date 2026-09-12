"""Shared result envelope and literal run_02/run_03 pixel measurements."""
import math
from pathlib import Path
import numpy as np
from PIL import Image

DIRS = ['S','SW','W','NW','N','NE','E','SE']
COUNTS = {'idle':8, 'walk':8, 'cast':12}

def result(id, subject, value=None, threshold=None, op='<=', unit='', notes='', passed=None, evidence=()):
    if passed is None and value is not None and threshold is not None:
        passed = bool({'<=':lambda:value<=threshold, '<':lambda:value<threshold,
                       '>=':lambda:value>=threshold, '==':lambda:value==threshold}[op]())
    return dict(id=id, subject=str(subject), passed=passed, value=value, threshold=threshold,
                op=op, unit=unit, evidence=list(evidence), notes=notes)

def rgba(image):
    if isinstance(image, (str, Path)):
        with Image.open(image) as im: return im.convert('RGBA')
    if isinstance(image, np.ndarray): return Image.fromarray(image.astype(np.uint8)).convert('RGBA')
    return image.convert('RGBA')

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

def pixels(path):
    im=rgba(path);bg=Image.new('RGBA',im.size,(20,25,34,255));bg.alpha_composite(im)
    return np.array(bg)[...,:3].astype(float),np.array(im)[...,3]>0

def difference(a,b):
    x,m=pixels(a);y,n=pixels(b);v=np.abs(x-y);u=m|n
    return {'canvas':float(v.mean()),'foreground_union':float(v[u].mean()) if u.any() else None}


def pair_differences(frames):
    if len(frames)<2: raise ValueError('At least two frames required')
    return [difference(frames[i],frames[(i+1)%len(frames)]) for i in range(len(frames))]
