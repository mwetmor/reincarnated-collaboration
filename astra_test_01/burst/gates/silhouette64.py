"""64px binary alpha, centroid/area alignment, aligned IoU and seven Hu moments.
Hu moments are a screen, not the primary shape distance. Threshold is caller-set.
"""
import numpy as np
from scipy import ndimage
from PIL import Image
from .common import rgba, result

def descriptor(alpha):
    if isinstance(alpha,dict): return alpha
    if isinstance(alpha,np.ndarray) and alpha.ndim==2:
        a=alpha.astype(float);a=a*255 if a.max(initial=0)<=1 else a
        im=Image.fromarray(a.astype(np.uint8),'L')
    elif isinstance(alpha,Image.Image) and alpha.mode=='L': im=alpha
    else: im=rgba(alpha).getchannel('A')
    m=np.array(im.resize((64,64),Image.Resampling.LANCZOS))>=128
    y,x=np.where(m)
    if not len(x): raise ValueError('Empty silhouette')
    cx,cy=x.mean(),y.mean();x=x-cx;y=y-cy;area=len(x)
    n=lambda p,q:float(np.sum(x**p*y**q)/area**(1+(p+q)/2))
    a,b,c,d,e,f,g=n(2,0),n(0,2),n(1,1),n(3,0),n(1,2),n(2,1),n(0,3)
    hu=[a+b,(a-b)**2+4*c*c,(d-3*e)**2+(3*f-g)**2,(d+e)**2+(f+g)**2,
        (d-3*e)*(d+e)*((d+e)**2-3*(f+g)**2)+(3*f-g)*(f+g)*(3*(d+e)**2-(f+g)**2),
        (a-b)*((d+e)**2-(f+g)**2)+4*c*(d+e)*(f+g),
        (3*f-g)*(d+e)*((d+e)**2-3*(f+g)**2)-(d-3*e)*(f+g)*(3*(d+e)**2-(f+g)**2)]
    return dict(mask=m,area=area,centroid=[float(cx),float(cy)],hu=hu)

def aligned_metrics(a,b):
    a,b=descriptor(a),descriptor(b)
    # Shared padded canvas avoids clipping during area normalization.
    target_area=512.;center=np.array([63.5,63.5])
    def align(d):
        scale=(target_area/d['area'])**.5
        matrix=np.eye(2)/scale
        offset=np.array(d['centroid'][::-1])-center/scale
        return ndimage.affine_transform(d['mask'].astype(float),matrix,offset,output_shape=(128,128),order=0)>0
    x,y=align(a),align(b); union=(x|y).sum()
    iou=float((x&y).sum()/union) if union else 0.
    ex=x&~ndimage.binary_erosion(x);ey=y&~ndimage.binary_erosion(y)
    contour=float((ndimage.distance_transform_edt(~ex)[ey].mean()+ndimage.distance_transform_edt(~ey)[ex].mean())/2)
    return dict(aligned_iou=iou,contour_distance=contour,hu_a=a['hu'],hu_b=b['hu'])

def distance(a,b):
    return 1-aligned_metrics(a,b)['aligned_iou']

def evaluate(image,master,subject='',threshold=None):
    import json
    try: m=aligned_metrics(image,master)
    except ValueError as e: return result('silhouette64',subject,notes=str(e))
    return result('silhouette64',subject,1-m['aligned_iou'],threshold,unit='1-iou',notes=('UNEVALUABLE verdict: no calibrated threshold supplied; ' if threshold is None else '')+json.dumps(m))
