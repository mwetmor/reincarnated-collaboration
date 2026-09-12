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

# O3b calibration inputs are generated in tests/motif_calibration.py. Fixed from
# synthetic 8/14/22px rings, seeded texture and a rectangular no-ring sprite;
# real crops are held out. See CALIBRATION.md for measured confirmation.
FAMILY_PARAMETERS = dict(min_radius_px=8, max_radius_px=30, vote_thresh=.50)

def _allowed_map(allowed_masks, native_shape, shape):
    allowed = np.zeros(shape, bool)
    h, w = shape
    nh, nw = native_shape
    for mask in ([] if allowed_masks is None else allowed_masks):
        m = np.asarray(mask)
        if m.shape == (4,):
            x0, y0, x1, y1 = m.astype(float)
            if not (0 <= x0 < x1 <= nw and 0 <= y0 < y1 <= nh):
                raise ValueError('Allowed bbox outside image')
            allowed[round(y0*h/nh):round(y1*h/nh), round(x0*w/nw):round(x1*w/nw)] = True
        else:
            if m.shape != native_shape:
                raise ValueError('Allowed mask shape mismatch')
            allowed |= scaled_mask(m, shape)
    return allowed

def count_family(rgb, family='ring', min_radius_px=8, max_radius_px=30,
                 vote_thresh=.50, allowed_masks=None, display_scale=None, *,
                 gradient_floor=.02, smooth_fraction=.08, nms_radius_fraction=.8,
                 min_angular_support=.75, radial_tolerance_fraction=.15,
                 alignment_cosine=.9, angular_samples=48,
                 max_outside=None, subject=''):
    """O3b gradient-vote circular Hough, numpy/scipy only.

    Sobel gradients on sigma=1 luminance; each edge votes in BOTH directions
    for every integer display radius. Gaussian orientation-vote accumulation,
    sigma=max(1,r*smooth_fraction), normalised by circle circumference and the
    Gaussian peak. Score is effective radial votes / circumference, NOT an NCC
    or a probability. Signed radial gradients must support >=75% of angular samples within a
    radius +/-15% (minimum 2px) band, alignment cosine >=.9. Synthetic half-arcs
    and rectangles calibrate this shape check, not real-crop count targets.
    Max across radii and spatial/radius NMS count a concentric
    primitive once. Named vote_thresh calibrated ONLY on the synthetic set in
    tests/motif_calibration.py; real crops confirm, never fit that threshold.
    gradient_floor=.02 uses normalised Sobel (contrast / display pixel).
    Radius inputs and returned centers/radii are in native source pixels;
    display_scale is analytical downsampling, never artwork registration.
    Result envelope notes.metrics contains inside, outside and peaks.
    """
    if family != 'ring':
        raise ValueError('Only the registered ring primitive is implemented')
    parameters=[min_radius_px,max_radius_px,vote_thresh,gradient_floor,smooth_fraction,
                nms_radius_fraction,min_angular_support,radial_tolerance_fraction,alignment_cosine]
    if not all(np.isfinite(v) for v in parameters) or not (
            0 < min_radius_px <= max_radius_px and vote_thresh > 0 and gradient_floor > 0
            and smooth_fraction > 0 and nms_radius_fraction > 0 and 0<min_angular_support<=1
            and radial_tolerance_fraction>0 and 0<alignment_cosine<=1
            and type(angular_samples) is int and angular_samples>=8):
        raise ValueError('Invalid family parameters')
    native = image_array(rgb)
    a = image_array(rgb, display_scale)
    h, w = a.shape[:2]
    factor = 1 if display_scale is None else display_scale
    allowed = _allowed_map(allowed_masks, native.shape[:2], (h, w))
    lum = ndimage.gaussian_filter(a[..., :3] @ LUMA / 255, 1)
    gx = ndimage.sobel(lum, axis=1) / 8
    gy = ndimage.sobel(lum, axis=0) / 8
    magnitude = np.hypot(gx, gy)
    ys, xs = np.where(magnitude >= gradient_floor)
    ux, uy = gx[ys, xs]/magnitude[ys, xs], gy[ys, xs]/magnitude[ys, xs]
    candidates = []
    radii = range(max(1, int(np.ceil(min_radius_px*factor))),
                  int(np.floor(max_radius_px*factor))+1)
    for radius in radii:
        votes = np.zeros((h, w), float)
        for sign in (-1, 1):
            vx = np.rint(xs + sign*radius*ux).astype(int)
            vy = np.rint(ys + sign*radius*uy).astype(int)
            valid = (vx >= 0) & (vx < w) & (vy >= 0) & (vy < h)
            np.add.at(votes, (vy[valid], vx[valid]), 1)
        sigma = max(1., radius*smooth_fraction)
        score = ndimage.gaussian_filter(votes, sigma) * sigma*sigma/radius
        local = ndimage.maximum_filter(score, size=max(3, radius//2*2+1))
        cy, cx = np.where((score >= vote_thresh) & (score == local))
        for y, x in zip(cy, cx):
            # A whole primitive must fit; clipped arcs are not complete rings.
            if radius <= x < w-radius and radius <= y < h-radius:
                angles = np.arange(angular_samples)*2*np.pi/angular_samples
                tolerance = max(2., radius*radial_tolerance_fraction)
                offsets = np.linspace(-tolerance, tolerance, 2*int(np.ceil(tolerance))+1)
                rr = radius+offsets[:, None]
                px = x+rr*np.cos(angles)
                py = y+rr*np.sin(angles)
                sx = ndimage.map_coordinates(gx, [py, px], order=1)
                sy = ndimage.map_coordinates(gy, [py, px], order=1)
                mag = np.hypot(sx, sy)
                radial = sx*np.cos(angles)+sy*np.sin(angles)
                # A single coherent edge polarity must surround the center.
                support = max(float(np.mean(np.any((sign*radial >= alignment_cosine*mag) &
                              (mag >= gradient_floor), axis=0))) for sign in (-1, 1))
                if support >= min_angular_support:
                    candidates.append(dict(center=[float(x), float(y)], radius=float(radius),
                                           score=float(score[y, x]), angular_support=support))
    retained = []
    for p in sorted(candidates, key=lambda p: (-p['score'], p['center'], p['radius'])):
        if any(np.linalg.norm(np.subtract(p['center'], q['center'])) <
               nms_radius_fraction*max(p['radius'], q['radius']) for q in retained):
            continue
        retained.append(p)
    inside = 0
    for p in retained:
        x, y = p['center']
        p['inside'] = bool(allowed[int(y), int(x)])
        inside += int(p['inside'])
        p['center'] = [x*native.shape[1]/w, y*native.shape[0]/h]
        p['radius'] /= factor
    outside = len(retained)-inside
    return report('O3b', subject, outside, max_outside, unit='instances', metrics={
        'inside': inside, 'outside': outside, 'peaks': retained, 'family': family,
        'min_radius_px': min_radius_px, 'max_radius_px': max_radius_px,
        'vote_thresh': vote_thresh, 'gradient_floor': gradient_floor,
        'smooth_fraction': smooth_fraction, 'nms_radius_fraction': nms_radius_fraction,
        'min_angular_support': min_angular_support, 'radial_tolerance_fraction': radial_tolerance_fraction,
        'alignment_cosine': alignment_cosine, 'angular_samples': angular_samples})
