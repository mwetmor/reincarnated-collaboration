"""O6 CIELAB a*b* bins; luminance deliberately ignored.
Bins: {part: {'a':[low,high], 'b':[low,high]}} inclusive intervals.
Overlapping memberships are unclassified (no order-dependent assignment).
Health measured BEFORE erosion over alpha>0: soft border pixels excluded from
opaque-core classification count as unclassified. Erosion is 1 or 2 display px.
max_unclassified requires reviewed label-sheet calibration; absent => null gate.
"""
from scipy import ndimage
from oracles.common import *

def classify_by_bins(rgba,bins,*,erosion_px=1,max_unclassified=None,alpha_min=ALPHA_MIN,display_scale=None,subject=''):
    if erosion_px not in (1,2):raise ValueError('erosion_px must be 1 or 2')
    a=image_array(rgba,display_scale);colors=lab(a[...,:3]);visible=a[...,3]>0;core=a[...,3]>=alpha_min
    memberships={}
    for name,bin in bins.items():
        if set(bin)!= {'a','b'}:raise ValueError('Each bin requires a and b intervals')
        m=core.copy()
        for channel,index in [('a',1),('b',2)]:
            lo,hi=bin[channel]
            if not np.isfinite([lo,hi]).all() or lo>hi:raise ValueError('Invalid bin interval')
            m &= (colors[...,index]>=lo)&(colors[...,index]<=hi)
        memberships[name]=m
    hits=np.sum(list(memberships.values()),axis=0) if memberships else np.zeros_like(core,int)
    unique=hits==1
    masks={name:ndimage.binary_erosion(m&unique,iterations=erosion_px) for name,m in memberships.items()}
    fraction=float((visible&~unique).sum()/visible.sum()) if visible.any() else None
    reason='Empty foreground' if fraction is None else ('Unclassified fraction exceeds calibrated health limit; VOID' if max_unclassified is not None and fraction>max_unclassified else '')
    row=report('O6',subject,fraction,max_unclassified,unit='fraction',reason=reason,metrics={'erosion_px':erosion_px,'unclassified_pixels':int((visible&~unique).sum()),'ambiguous_pixels':int((hits>1).sum())})
    return {'masks':masks,'unclassified_frac':fraction,'result':row}

def evaluate(*args,**kwargs):return classify_by_bins(*args,**kwargs)['result']
