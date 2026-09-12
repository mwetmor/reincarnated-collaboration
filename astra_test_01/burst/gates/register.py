"""Uniform reduction/translation and independently remeasured reviewed soles.
No source configuration or annotation files are loaded implicitly.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

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

def sole_contacts(image, regions):
    mask = np.array(image.convert('RGBA'))[..., 3] >= 128
    points = []
    if len(regions) != 2:
        raise ValueError('Exactly two reviewed sole regions are required')
    for x0, y0, x1, y1 in regions:
        if not (0 <= x0 < x1 <= image.width and 0 <= y0 < y1 <= image.height):
            raise ValueError('Sole region outside image')
        roi = mask[y0:y1, x0:x1]
        yy, xx = np.where(roi)
        if not len(yy):
            raise ValueError('Empty sole region')
        bottom = int(yy.max())
        if bottom >= roi.shape[0] - 1:
            raise ValueError('Sole region clips the contact; review the region')
        low_x = xx[yy >= bottom - 1]
        if low_x.min() == 0 or low_x.max() == roi.shape[1] - 1:
            raise ValueError('Sole region clips the contact horizontally')
        points.append([float(np.median(low_x) + x0), float(bottom + y0)])
    return points

def measured_anchor(image, regions):
    return np.mean(sole_contacts(image, regions), axis=0).tolist()

def preflight(image, regions, pivot=(256, 400), tolerance=4):
    points = sole_contacts(image, regions)
    midpoint = np.mean(points, axis=0)
    error = np.abs(midpoint - pivot)
    return {'points': points, 'midpoint': midpoint.tolist(),
            'error_xy': error.tolist(), 'pass': bool((error <= tolerance).all())}

def contacts(im, regions):
    mask = np.array(im.convert('RGBA'))[...,3] >= 128
    below = np.zeros_like(mask); below[:-1] = mask[1:]
    contour = mask & ~below
    points = []
    if len(regions) != 2: raise ValueError('Exactly two reviewed sole regions required')
    for x0,y0,x1,y1 in regions:
        if not (0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height):
            raise ValueError('Sole region outside image')
        yy,xx = np.where(contour[y0:y1,x0:x1])
        if not len(yy): raise ValueError('No visible lower contour')
        bottom = yy.max(); xs = xx[yy >= bottom-1]
        if bottom == y1-y0-1 or xs.min() == 0 or xs.max() == x1-x0-1:
            raise ValueError('Review region truncates lowest sole contour')
        points.append([float(np.median(xs)+x0),float(bottom+y0)])
    return {'points':points,'midpoint':np.mean(points,axis=0).tolist()}

def front_contacts(im,exclude_thin_staff=False):
    a=np.array(im)[...,3]>=128;ys,xs=np.where(a)
    if not len(xs): raise ValueError('Empty alpha subject')
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
            if len(xx) and xx.max()-xx.min()>=(ys.max()-ys.min())*.035:
                bottom=yy.max();feet.append([float(np.median(xx[yy>=bottom-1])),float(bottom)])
        feet.sort(key=lambda p:p[1],reverse=True)
        if len(feet)>=2:return sorted(feet[:2],key=lambda p:p[0])
        edge[:int(ys.min()+.78*(ys.max()-ys.min()))]=False
        labels,n=ndimage.label(ndimage.binary_dilation(edge,iterations=max(1,round(im.width/1254*2))))
        candidates=[]
        for k in range(1,n+1):
            yy,xx=np.where(edge&(labels==k))
            if len(xx) and xx.max()-xx.min()>=(ys.max()-ys.min())*.035:
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


def frame_contacts(im, regions=None):
    return contacts(im, regions)['points'] if regions is not None else front_contacts(im, exclude_thin_staff=True)

def register_reviewed(image, regions, body_height, **kwargs):
    return registration(image, {'anchor':measured_anchor(image,regions), 'body_height':body_height}, **kwargs)
