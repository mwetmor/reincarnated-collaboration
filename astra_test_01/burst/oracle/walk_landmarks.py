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


def mask_with_diagnostics(frame_rgb):
    a = np.asarray(frame_rgb)
    if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] not in (3, 4):
        raise ValueError('expected uint8 RGB or RGBA')
    border = np.concatenate((a[0,:,:3], a[-1,:,:3], a[:,0,:3], a[:,-1,:3]))
    green = np.mean((border[:,1]>210)&(border[:,0]<45)&(border[:,2]<45)) >= .95
    native = a.shape[2] == 4 and np.any(a[...,3]<255)
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
    return mask_with_diagnostics(frame_rgb)[0]


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


def track_landmarks(masks):
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
