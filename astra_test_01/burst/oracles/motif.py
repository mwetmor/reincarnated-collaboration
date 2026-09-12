"""O3 masked zero-mean NCC via scipy.signal.fftconvolve, scale/rotation bank.
Correlation threshold MUST be supplied. Calibration set: exact transformed
synthetic templates + independent clean sprite negative; F04 held-out tell.
NMS overlap .25 and center fraction .5 are provisional duplicate suppression,
not acceptance calibration; override explicitly and record alongside results.
Allowed masks: native image Boolean arrays or XYXY exclusive bounding boxes.
Partition uses detected center; returned boxes/centers remain native coordinates.
"""
from scipy import ndimage,signal
from .common import *

NMS_IOU=.25
NMS_CENTER_FRACTION=.5
VARIANCE_EPS=1e-10  # Numerical division guard, not a content threshold.

def _correlate(image,template,weight):
    kernel=weight[::-1,::-1];count=weight.sum()
    mean=float((template*weight).sum()/count);t=(template-mean)*weight
    norm=float((t*t).sum())
    if norm<=VARIANCE_EPS:return None
    sums=signal.fftconvolve(image,kernel,mode='valid')
    squares=signal.fftconvolve(image*image,kernel,mode='valid')
    variance=np.maximum(squares-sums*sums/count,0)
    numerator=signal.fftconvolve(image,t[::-1,::-1],mode='valid')
    denominator=np.sqrt(variance*norm)
    return np.divide(numerator,denominator,out=np.zeros_like(numerator),where=denominator>VARIANCE_EPS).clip(-1,1)

def _duplicate(a,b,nms_iou,nms_center_fraction):
    x,y=a['bbox'],b['bbox']
    intersection=max(0,min(x[2],y[2])-max(x[0],y[0]))*max(0,min(x[3],y[3])-max(x[1],y[1]))
    area=lambda r:(r[2]-r[0])*(r[3]-r[1])
    iou=intersection/(area(x)+area(y)-intersection)
    center_distance=np.linalg.norm(np.array(a['center'])-b['center'])
    return iou>nms_iou or center_distance<nms_center_fraction*min(x[2]-x[0],x[3]-x[1],y[2]-y[0],y[3]-y[1])

def count_instances(rgb,template_rgb,scales,rotations_deg,thresh,allowed_masks=None,*,nms_iou=NMS_IOU,nms_center_fraction=NMS_CENTER_FRACTION,max_outside=None,display_scale=None,subject=''):
    if not -1<=thresh<=1 or not scales or not rotations_deg:raise ValueError('Invalid NCC search parameters')
    native=image_array(rgb);a=image_array(rgb,display_scale);h,w=a.shape[:2]
    factor=1 if display_scale is None else display_scale
    lum=a[...,:3]@LUMA/255;template=image_array(template_rgb)[...,:3]@LUMA/255
    allowed=np.zeros((h,w),bool)
    for mask in ([] if allowed_masks is None else allowed_masks):
        m=np.asarray(mask)
        if m.shape==(4,):
            x0,y0,x1,y1=m.astype(float)
            if not(0<=x0<x1<=native.shape[1] and 0<=y0<y1<=native.shape[0]):raise ValueError('Allowed bbox outside image')
            sx=w/native.shape[1];sy=h/native.shape[0]
            allowed[round(y0*sy):round(y1*sy),round(x0*sx):round(x1*sx)]=True
        else:
            if m.shape!=native.shape[:2]:raise ValueError('Allowed mask shape mismatch')
            allowed |= scaled_mask(m,(h,w))
    peaks=[];evaluated=0
    for scale in scales:
        if scale<=0:raise ValueError('Scale must be positive')
        # Template pyramid interpolation is analytical, never delivered artwork.
        size=tuple(max(2,round(v*scale*factor)) for v in template.shape[::-1])
        base=np.array(Image.fromarray(template.astype('float32')).resize(size,Image.Resampling.BICUBIC))
        for angle in rotations_deg:
            t=ndimage.rotate(base,angle,reshape=True,order=1,mode='constant',cval=0,prefilter=False)
            weight=ndimage.rotate(np.ones_like(base),angle,reshape=True,order=0,mode='constant',cval=0,prefilter=False)
            th,tw=t.shape
            if th>h or tw>w:continue
            ncc=_correlate(lum,t,weight)
            if ncc is None:continue
            evaluated+=1
            local=ndimage.maximum_filter(ncc,size=(max(3,th//2),max(3,tw//2)))
            ys,xs=np.where((ncc>=thresh)&(ncc==local))
            for y,x in zip(ys,xs):
                peaks.append({'score':float(ncc[y,x]),'bbox':[int(x),int(y),int(x+tw),int(y+th)],'center':[float(x+tw/2),float(y+th/2)],'scale':float(scale),'rotation_deg':float(angle)})
    if not evaluated:return report('O3',subject,None,max_outside,reason='No nonconstant template fits image')
    retained=[]
    for p in sorted(peaks,key=lambda p:(-p['score'],p['bbox'],p['scale'],p['rotation_deg'])):
        if not any(_duplicate(p,q,nms_iou,nms_center_fraction) for q in retained):retained.append(p)
    inside=0
    for p in retained:
        cx,cy=p['center'];p['inside']=bool(allowed[min(h-1,int(cy)),min(w-1,int(cx))]);inside+=int(p['inside'])
        p['bbox']=[v*(native.shape[1]/w if i%2==0 else native.shape[0]/h) for i,v in enumerate(p['bbox'])]
        p['center']=[cx*native.shape[1]/w,cy*native.shape[0]/h]
    outside=len(retained)-inside
    return report('O3',subject,outside,max_outside,unit='instances',metrics={'inside':inside,'outside':outside,'peaks':retained,'evaluated_templates':evaluated,'thresh':thresh,'nms_iou':nms_iou,'nms_center_fraction':nms_center_fraction})
