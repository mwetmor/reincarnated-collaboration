"""Silhouette walk landmarks; screen tracks are not anatomical labels.

Collotype defaults: 7px median (suppresses <=2px printed lines), Otsu,
bright/dark polarity from an inset border, reject near-full-width background rows,
largest 8-connected component and 3px closing. Broad-row rejection protects
against printed floor strips; a mask touching that rejection is flagged.
Coordinates are source pixels; H is inclusive silhouette height. Every scalar
coordinate also has an _H counterpart. No registration or image resampling.
"""
import numpy as np
from PIL import Image
from scipy import ndimage
from gates.matte import remove_chroma_key

MASK_PARAMS = dict(median_size=7, close_size=3, preclose_size=7, grid_open_size=5, broad_row_fraction=.78,
                   alpha_threshold=128, ground_tolerance_px=2,
                   polarity='opposite inset-border majority', component='largest 8-connected')


def _runs(row):
    edges = np.diff(np.r_[False, row, False].astype(int))
    return list(zip(np.where(edges == 1)[0], np.where(edges == -1)[0]))


def _otsu(gray):
    hist = np.bincount(np.clip(np.rint(gray), 0, 255).astype(np.uint8).ravel(), minlength=256)
    p = hist / hist.sum()
    w = np.cumsum(p); m = np.cumsum(p*np.arange(256))
    variance = np.divide((m[-1]*w-m)**2, w*(1-w), out=np.zeros(256), where=(w*(1-w))>0)
    return int(np.argmax(variance))


def mask_with_diagnostics_otsu_lineage(frame_rgb):
    a = np.asarray(frame_rgb)
    if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] not in (3, 4):
        raise ValueError('expected uint8 RGB or RGBA')
    border = np.concatenate((a[0,:,:3], a[-1,:,:3], a[:,0,:3], a[:,-1,:3]))
    green = np.mean((border[:,1]>210)&(border[:,0]<45)&(border[:,2]<45)) >= .95
    native = a.shape[2] == 4 and np.any(a[...,3]<255)
    if native and not np.any(a[...,3] >= MASK_PARAMS['alpha_threshold']):
        return np.zeros(a.shape[:2], dtype=bool), dict(
            method='frozen matte alpha >=128', grid_or_floor_contact=False, empty=True)
    if native or green:
        m = np.array(remove_chroma_key(Image.fromarray(a), preserve_particles=True))[...,3]>=128
        return m, dict(method='frozen matte alpha >=128', grid_or_floor_contact=False)
    gray = a[...,:3].astype(float) @ np.array([.2126,.7152,.0722])
    smooth = ndimage.median_filter(gray, size=MASK_PARAMS['median_size'], mode='nearest')
    threshold = _otsu(smooth)
    bright = np.rint(smooth) > threshold
    inset = min(7, max(1, min(bright.shape)//10))
    b = np.concatenate((bright[inset,inset:-inset], bright[-inset-1,inset:-inset],
                        bright[inset:-inset,inset], bright[inset:-inset,-inset-1]))
    raw = ~bright if b.mean() > .5 else bright
    broad = raw.mean(axis=1) > MASK_PARAMS['broad_row_fraction']
    raw[broad] = False
    # Remove remaining narrow grid branches, then join short shadow gaps.
    raw = ndimage.binary_opening(raw, structure=np.ones((5,5)))
    raw = ndimage.binary_closing(raw, structure=np.ones((7,7)))
    raw[broad] = False
    lab, n = ndimage.label(raw, np.ones((3,3)))
    if not n:
        return raw, dict(method='median Otsu', threshold=threshold, empty=True)
    sizes = np.bincount(lab.ravel()); sizes[0]=0
    m = lab == sizes.argmax()
    # Closing can join narrow contour holes, but cannot put rejected floor back.
    m = ndimage.binary_closing(m, structure=np.ones((3,3)), border_value=0)
    m = ndimage.binary_fill_holes(m)
    m[broad] = False
    contact = bool(np.any(m & ndimage.binary_dilation(np.broadcast_to(broad[:,None], m.shape))))
    return m, dict(method='median Otsu largest component close', threshold=threshold,
                   rejected_broad_rows=np.flatnonzero(broad).tolist(),
                   grid_or_floor_contact=contact, area_fraction=float(m.mean()),
                   head_top_unreliable=True,
                   head_top_note='collotype hair contrast is unverified; geometric thin flag alone cannot detect omitted dark hair')


def figure_mask(frame_rgb):
    return mask_with_diagnostics_otsu_lineage(frame_rgb)[0]


def landmarks(mask, ground_line=None):
    m = np.asarray(mask, dtype=bool)
    if m.ndim != 2:
        raise ValueError('mask must be 2D')
    yy, xx = np.where(m)
    if not len(xx):
        return {'valid':False, 'reason':'empty_mask', 'mask_area':0}
    top, bottom = int(yy.min()), int(yy.max()); h = bottom-top+1
    widths = [max((b-a for a,b in _runs(row)), default=0) for row in m[top:bottom+1]]
    upper = widths[:max(1, int(np.ceil(.2*h)))]
    # The fallback is the first row attaining the widest horizontal run.
    ref = top+int(np.argmax(upper))
    head = m.copy(); head[:top]=False; head[top+max(1,int(np.ceil(.12*h))):]=False
    hy,hx=np.where(head)
    torso_rows = m[top+int(.25*h):top+int(.6*h)]
    centers=[]; torso_widths=[]
    for row in torso_rows:
        runs=_runs(row)
        if runs:
            a,b=max(runs,key=lambda v:v[1]-v[0]); centers.append((a+b-1)/2);torso_widths.append(b-a)
    torso=float(np.median(centers)) if centers else float(xx.mean())
    tw=float(np.median(torso_widths)) if torso_widths else 0.
    row=m[min(bottom,top+int(.45*h))]; rx=np.flatnonzero(row)
    wl=max(0.,torso-tw/2-float(rx.min())) if len(rx) else None
    wr=max(0.,float(rx.max())-torso-tw/2) if len(rx) else None
    low=m.copy(); low[:top+int(.75*h)]=False
    lab,n=ndimage.label(low,np.ones((3,3)))
    feet=[]
    for k in range(1,n+1):
        y,x=np.where(lab==k)
        if len(x)<3: continue
        sole=int(y.max()); sole_x=float(np.median(x[y>=sole-2]))
        feet.append(dict(x=sole_x,y=sole,area=int(len(x))))
    feet=sorted(sorted(feet,key=lambda f:f['area'],reverse=True)[:2],key=lambda f:f['x'])
    ground=float(bottom if ground_line is None else ground_line)
    d=dict(valid=True, mask_area=int(m.sum()), mask_area_per_H=float(m.sum()/h),
           head_top_y=top, head_top_thin=bool(np.mean(widths[:max(1,int(np.ceil(.05*h)))])<3),
           head_ref_y=ref, sole_line_y=bottom,H=h, head_cx=float(hx.mean()),
           torso_cx=torso, torso_width=tw,wrist_ext_L=wl,wrist_ext_R=wr,
           foot_components=len(feet), feet_merged=len(feet)<2,
           ground_line_y=ground, foot_identity='initial image x order; tracked over time, not anatomical')
    for i,side in enumerate(('L','R')):
        foot=feet[i] if i<len(feet) else None
        d['foot_'+side+'_x']=foot['x'] if foot else None
        d['foot_'+side+'_y']=foot['y'] if foot else None
        d['planted_'+side]=abs(foot['y']-ground)<=2 if foot else None
    d['planted']={s:d['planted_'+s] for s in ('L','R')}
    for key,v in list(d.items()):
        if key in ('head_top_y','head_ref_y','sole_line_y','head_cx','torso_cx','torso_width','wrist_ext_L','wrist_ext_R','ground_line_y','foot_L_x','foot_R_x','foot_L_y','foot_R_y'):
            d[key+'_H']=v/h if v is not None else None
    return d


def track_landmarks_otsu_stance_lineage(masks):
    """Predictive nearest assignment, preserving missing feet as null.

Ground is clip-wide maximum sole y. Ambiguous merges do not get an invented
second foot. Identity continuity is a screen-space estimate and is flagged.
"""
    seq=[landmarks(m) for m in masks]
    if not all(d['valid'] for d in seq):
        return seq
    ground=max(d['sole_line_y'] for d in seq)
    previous={}; velocity={s:0. for s in ('L','R')}
    for d in seq:
        feet=[(d['foot_'+s+'_x'],d['foot_'+s+'_y']) for s in ('L','R') if d['foot_'+s+'_x'] is not None]
        assignments={}
        if len(feet)==2:
            orders=[feet, feet[::-1]]
            chosen=min(orders,key=lambda f:sum((f[j][0]-previous.get(s,f[j][0])-velocity[s])**2 for j,s in enumerate(('L','R'))))
            assignments=dict(zip(('L','R'),chosen))
        elif feet:
            side=min(('L','R'),key=lambda s:abs(feet[0][0]-previous.get(s,feet[0][0])-velocity[s]))
            assignments[side]=feet[0]
        d['identity_ambiguous']=len(feet)!=2
        d['ground_line_y']=ground;d['ground_line_y_H']=ground/d['H']
        for s in ('L','R'):
            x,y=assignments.get(s,(None,None))
            if x is not None:
                velocity[s]=x-previous[s] if s in previous else 0.; previous[s]=x
            for axis,v in (('x',x),('y',y)):
                d[f'foot_{s}_{axis}']=v;d[f'foot_{s}_{axis}_H']=v/d['H'] if v is not None else None
            d['planted_'+s]=abs(y-ground)<=2 if y is not None else None
        d['planted']={s:d['planted_'+s] for s in ('L','R')}
    return seq


# Method A is the default; method B remains an explicit experimental option.
mask_with_diagnostics = mask_with_diagnostics_otsu_lineage
ROW_MASK_PARAMS = dict(method='grid phase correlation / registered temporal median',
                       tau=12., line_width_px=5, close_size=3,
                       grid_highpass='signed 5px median residual, long-line opening',
                       registration='integer translation; phase correlation; no scale',
                       ground_tolerance_px=3., stationary_tolerance_px=2.,
                       head_search_fraction_H=.25, head_patch_fraction_H=.12)


def _translate(a, dy, dx, fill=0):
    """Integer, non-wrapping translation used only by the measuring instrument."""
    out=np.full(a.shape,fill,dtype=a.dtype)
    h,w=a.shape[:2];dy,dx=int(dy),int(dx)
    y0,y1=max(0,dy),min(h,h+dy);x0,x1=max(0,dx),min(w,w+dx)
    if y1>y0 and x1>x0:out[y0:y1,x0:x1]=a[y0-dy:y1-dy,x0-dx:x1-dx]
    return out


def _grid_image(frame):
    gray=np.asarray(frame)[...,:3].astype(np.float32).mean(axis=2)
    high=gray-ndimage.median_filter(gray,size=5,mode='nearest')
    length=max(15,int(min(gray.shape)*.15))
    bright=np.maximum(high,0);dark=np.maximum(-high,0)
    def lines(a):
        return np.maximum(ndimage.grey_opening(a,size=(1,length)),
                          ndimage.grey_opening(a,size=(length,1)))
    return lines(bright)-lines(dark)


def _grid_shift(reference, current):
    if min(np.std(reference),np.std(current))<1e-6:
        return (0,0),dict(grid_detected=False,phase_peak=None,phase_peak_ratio=None)
    # Collapse to grid-line profiles before phase correlation. This removes
    # the occlusion pattern of the travelling body from the registration cue.
    # Repeated grid lines admit period aliases; choose the nearest phase peak.
    shifts=[];peaks=[];ratios=[];periods=[]
    for axis in (0,1):
        ra=np.mean(reference,axis=1-axis);ca=np.mean(current,axis=1-axis)
        ra-=ra.mean();ca-=ca.mean();n=len(ra)
        if min(np.std(ra),np.std(ca))<1e-6:
            shifts.append(0);peaks.append(None);ratios.append(None);periods.append(None);continue
        spectrum=np.fft.rfft(ra);power=np.abs(spectrum)**2
        frequencies=np.arange(len(power));valid=(frequencies>=3)&(frequencies<=n//5)
        dominant=int(np.argmax(np.where(valid,power,0)))
        period=n/dominant if dominant else n
        cross=np.fft.fft(ra)*np.conj(np.fft.fft(ca))
        cross=np.divide(cross,np.abs(cross),out=np.zeros_like(cross),where=np.abs(cross)>1e-9)
        corr=np.fft.ifft(cross).real;index=np.arange(n);signed=np.where(index<=n//2,index,index-n)
        # Fix the lattice branch at the nearest origin; never infer whole
        # grid periods from figure motion. The unresolved alias is reported.
        limit=max(2,int(np.floor(period/2)));allowed=np.abs(signed)<=limit
        score=np.where(allowed,corr,-np.inf);k=int(np.argmax(score))
        second=score.copy();second[np.abs(signed-signed[k])<=1]=-np.inf
        runner=float(np.max(second));value=float(score[k])
        shifts.append(int(signed[k]));peaks.append(value);ratios.append(value/runner if runner>0 else None);periods.append(period)
    return tuple(shifts),dict(grid_detected=True,phase_peak=peaks,phase_peak_ratio=ratios,
        grid_period_yx=periods,periodic_grid_ambiguity='nearest lattice phase; whole-period displacement unresolved')


def figure_mask_row(frames, return_diagnostics=False, method="A"):
    """Method A: independent median/Otsu/morphology masks (the default).

    Set method="B" for the grid-registered temporal-median experiment.
    The white top-hat residual (features narrower than 5px) is subtracted from
    absolute RGB difference before thresholding. No Otsu fallback is used.
    Diagnostics retain grid translation, support and median-contamination risks.
    """
    arrays=[np.asarray(f) for f in frames]
    if not arrays or any(a.dtype!=np.uint8 or a.ndim!=3 or a.shape[2] not in (3,4) for a in arrays):
        raise ValueError('expected nonempty uint8 RGB/RGBA row')
    if len({a.shape[:2] for a in arrays})!=1:raise ValueError('frame dimensions differ')
    if method not in ('A', 'B'):
        raise ValueError('mask method must be A or B')
    if method == 'A':
        pairs = [mask_with_diagnostics_otsu_lineage(a) for a in arrays]
        masks = [m for m, _ in pairs]
        health = []
        for m, diag in pairs:
            lm = landmarks(m)
            health.append(dict(diag, mask_method='A', grid_shift_xy=[0, 0],
                               mask_area=int(m.sum()), H=lm.get('H'),
                               mask_area_per_H=lm.get('mask_area_per_H')))
        return (masks, health) if return_diagnostics else masks
    native=[]
    for a in arrays:
        b=np.concatenate((a[0,:,:3],a[-1,:,:3],a[:,0,:3],a[:,-1,:3]))
        native.append((a.shape[2]==4 and np.any(a[...,3]<255)) or np.mean((b[:,1]>210)&(b[:,0]<45)&(b[:,2]<45))>=.95)
    if any(native):
        if not all(native):raise ValueError('mixed opaque and alpha/keyed row')
        pairs=[mask_with_diagnostics(a) for a in arrays]
        masks=[m for m,h in pairs];health=[dict(h,grid_shift_xy=[0,0],grid_leak=0.,mask_area=int(m.sum()),H=landmarks(m).get('H'),mask_area_per_H=landmarks(m).get('mask_area_per_H')) for m,h in pairs]
        return (masks,health) if return_diagnostics else masks
    grids=[_grid_image(a) for a in arrays]
    registrations=[_grid_shift(grids[0],g) for g in grids]
    registered=[_translate(a[...,:3].astype(np.float32),*shift,fill=np.nan) for a,(shift,_) in zip(arrays,registrations)]
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        backdrop=np.nanmedian(np.stack(registered),axis=0)
    masks=[];health=[]
    for a,g,(shift,diag) in zip(registered,grids,registrations):
        delta=np.nan_to_num(np.max(np.abs(a-backdrop),axis=2),nan=0.)
        # Explicit top-hat subtraction = a 5x5 opening of positive difference.
        broad=delta-ndimage.white_tophat(delta,size=(5,5))
        raw=broad>ROW_MASK_PARAMS['tau']
        labels,n=ndimage.label(raw,np.ones((3,3)));sizes=np.bincount(labels.ravel());sizes[0]=0
        m=labels==sizes.argmax() if n else np.zeros(raw.shape,bool)
        m=ndimage.binary_closing(m,structure=np.ones((3,3)))
        m=ndimage.binary_fill_holes(m)
        m=_translate(m,-shift[0],-shift[1])
        grid_lines=np.abs(g)>max(3.,float(np.percentile(np.abs(g),85)))
        lm=landmarks(m);area=int(m.sum())
        masks.append(m);health.append(dict(diag,method=ROW_MASK_PARAMS['method'],
            grid_shift_xy=[shift[1],shift[0]],grid_leak=float((m&grid_lines).sum()/area) if area else None,
            detected_grid_fraction=float(grid_lines.mean()),mask_area=area,H=lm.get('H'),
            mask_area_per_H=lm.get('mask_area_per_H'),area_fraction=float(m.mean()),
            median_foreground_caveat='body occupancy >= half the row persists in the median; no semantic repair',
            registration_valid_fraction=float(np.isfinite(a[...,0]).mean())))
    return (masks,health) if return_diagnostics else masks


def track_head(frames,masks):
    """Fixed-template NCC, visited forward/backward from the widest-head frame.

    Input arrays and masks must share a coordinate system (registered grid for
    plates). The mask-top and mask centroid series survive as lineage fields.
    A search-limit or low-correlation result is exposed, never amplitude-clamped.
    """
    from scipy.signal import fftconvolve
    seq=[landmarks(m) for m in masks]
    if not seq or not all(d['valid'] for d in seq):
        return [dict(head_track_valid=False,head_top_y=None,head_cx=None,head_cy=None,
                     head_top_mask_y=d.get('head_top_y')) for d in seq]
    widths=[]
    for m,d in zip(masks,seq):
        top=d['head_top_y'];widths.append(max((max((b-a for a,b in _runs(r)),default=0) for r in m[top:top+max(1,int(.2*d['H']))]),default=0))
    template_index=int(np.argmax(widths));lm=seq[template_index];m=masks[template_index]
    y0=lm['head_top_y'];ph=max(3,int(np.ceil(.12*lm['H'])));y1=min(m.shape[0],y0+ph)
    _,xs=np.where(m[y0:y1]);x0=max(0,int(xs.min())-2);x1=min(m.shape[1],int(xs.max())+3)
    gray=[np.asarray(f)[...,:3].astype(float).mean(axis=2) for f in frames]
    template=gray[template_index][y0:y1,x0:x1];ph,pw=template.shape
    centered=template-template.mean();energy=float(np.sum(centered**2));area=ph*pw
    out=[None]*len(seq)
    def record(i,x,y,score,clipped):
        d=seq[i]
        return dict(head_cx=float(x+(pw-1)/2),head_cy=float(y+(ph-1)/2),head_top_y=float(y),
            head_top_mask_y=d['head_top_y'],head_cx_mask_lineage=d['head_cx'],
            head_box_xyxy=[int(x),int(y),int(x+pw),int(y+ph)],head_template_frame=template_index,
            head_ncc=score,head_search_limit=bool(clipped),head_track_valid=bool(score is not None and score>=.5 and not clipped),
            head_track_method='fixed head patch NCC; +/-25%H previous position')
    out[template_index]=record(template_index,x0,y0,1. if energy>1e-9 else None,False)
    for direction in (1,-1):
        px,py=x0,y0
        for i in range(template_index+direction,len(seq) if direction==1 else -1,direction):
            radius=int(np.ceil(.25*lm['H']));h,w=gray[i].shape
            left,right=max(0,px-radius),min(w-pw,px+radius)
            top,bottom=max(0,py-radius),min(h-ph,py+radius)
            search=gray[i][top:bottom+ph,left:right+pw]
            ones=np.ones(template.shape);sums=fftconvolve(search,ones,mode='valid');squares=fftconvolve(search**2,ones,mode='valid')
            numerator=fftconvolve(search,centered[::-1,::-1],mode='valid')
            denom=np.sqrt(np.maximum(0,squares-sums*sums/area)*energy)
            corr=np.divide(numerator,denom,out=np.full(numerator.shape,-1.),where=denom>1e-9)
            iy,ix=np.unravel_index(np.argmax(corr),corr.shape);px,py=int(left+ix),int(top+iy)
            clipped=ix in (0,corr.shape[1]-1) or iy in (0,corr.shape[0]-1)
            out[i]=record(i,px,py,float(corr[iy,ix]) if energy>1e-9 else None,clipped)
    return out


def track_landmarks(masks):
    """Track feet, then use stationary sole x AND ground proximity for stance.

    First sample uses the next sample because there is no previous observation;
    raw fixed-camera x is never wrapped from frame 12 to frame 1. Missing feet
    stay null. A first-frame stance is a boundary contact, explicitly marked.
    """
    seq=track_landmarks_otsu_stance_lineage(masks)
    if not seq or not all(d['valid'] for d in seq):return seq
    for i,d in enumerate(seq):
        d['head_top_mask_y']=d['head_top_y']
        d['planted_ground_only_lineage']=dict(d['planted'])
        for side in ('L','R'):
            other=seq[i-1] if i else (seq[1] if len(seq)>1 else {})
            x=d.get('foot_'+side+'_x');previous=other.get('foot_'+side+'_x');y=d.get('foot_'+side+'_y')
            speed=(x-previous)*(1 if i else -1) if x is not None and previous is not None else None
            d['foot_'+side+'_velocity_x']=speed
            d['planted_'+side]=bool(abs(speed)<=2 and abs(y-d['ground_line_y'])<=3) if speed is not None and y is not None else None
        d['planted']={s:d['planted_'+s] for s in ('L','R')}
        d['velocity_boundary']='forward difference (no prior frame)' if i==0 else 'backward difference'
    return seq


def mask_stability(masks):
    """Population area and inclusive-height CV; both must be strictly < .25.

    Empty masks invalidate the row, even if the remaining masks are consistent.
    Stability is a selector, not evidence that a segmentation is anatomically right.
    """
    areas = [int(np.asarray(m, dtype=bool).sum()) for m in masks]
    heights = [landmarks(m).get('H', 0) for m in masks]
    def cv(values):
        return float(np.std(values) / np.mean(values)) if values and np.mean(values) > 0 else None
    area_cv, height_cv = cv(areas), cv(heights)
    stable = bool(areas and all(areas) and all(heights) and
                  area_cv < .25 and height_cv < .25)
    return dict(mask_stability=area_cv, mask_H_cv=height_cv,
                mask_area_px=areas, mask_H_px=heights, threshold=.25,
                stable=stable, reason=None if stable else 'unstable_segmentation')
