"""XAG-118 temporal flash screen; spatial patterns explicitly report-only.

Citation: Microsoft Xbox Accessibility Guideline 118, Photosensitivity:
https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/118
Registered thresholds: relative luminance change >=.10, affected area >=.20
of a 1280x720-equivalent canvas, >3 flashes in any sliding one-second window;
saturated red R/(R+G+B)>=.8, change in max(0,R-G-B)*320 >20.
A flash is a PAIR of opposing transitions on the same pixels, not each edge.
All thresholds below are named parameters. No assertion of overall XAG
compliance: the spatial-pattern instrument remains unevaluable until a robust
>=5 light/dark-pair, >=20%-area detector is calibrated. No network required.
"""
import numpy as np
from oracles.common import report,LUMA

LUMINANCE_CHANGE=.10
AREA_FRACTION=.20
MAX_FLASHES_PER_SECOND=3
RED_SATURATION=.8
RED_TRANSITION=20.
RED_SCALE=320.
REFERENCE_CANVAS=(1280,720)
PATTERN_PAIRS=5


def _max_window(times,window_s=1.):
    start=0;maximum=0
    for end,t in enumerate(times):
        while start<=end and times[start]<=t-window_s+1e-12:start+=1
        maximum=max(maximum,end-start+1)
    return maximum


def _paired_events(fields,fps,required_area):
    pending=np.zeros(fields[0].shape,np.int8);events=[];transitions=[]
    for i,direction in enumerate(fields,1):
        paired=(direction!=0)&(pending==-direction)
        if np.count_nonzero(direction)>=required_area:transitions.append(i/fps)
        if np.count_nonzero(paired)>=required_area:events.append(i/fps)
        pending[paired]=0
        fresh=(direction!=0)&~paired
        pending[fresh]=direction[fresh]
    return events,transitions


def check(frames,fps,canvas_size=None,*,luminance_change=LUMINANCE_CHANGE,
          area_fraction=AREA_FRACTION,max_flashes_per_second=MAX_FLASHES_PER_SECOND,
          red_saturation=RED_SATURATION,red_transition=RED_TRANSITION,
          red_scale=RED_SCALE,pattern_pairs=PATTERN_PAIRS,subject=''):
    """RGB uint8 frame arrays; canvas_size=(width,height) of displayed viewport.

    A viewport larger than the frame represents an unchanging surrounding area;
    a smaller viewport is rejected. Area is converted to the reference canvas,
    preserving the viewport fraction. Alpha composites must be supplied as RGB.
    Result value/threshold assess temporal rules only; notes.results contains
    the separate unevaluable spatial-pattern envelope.
    """
    frames=[np.asarray(a) for a in frames]
    if not np.isfinite(fps) or fps<=0:raise ValueError('fps must be positive')
    if len(frames)<2:return report('pse_check',subject,None,reason='At least two frames required')
    shape=frames[0].shape
    if len(shape)!=3 or shape[2]!=3 or any(a.shape!=shape for a in frames):
        raise ValueError('Equal RGB frame shapes required; composite alpha first')
    if any(not np.isfinite(a).all() or np.any(a<0) or np.any(a>255) for a in frames):
        raise ValueError('RGB values must be in 0..255')
    height,width=shape[:2];canvas=tuple(canvas_size or (width,height))
    if len(canvas)!=2 or canvas[0]<width or canvas[1]<height:
        raise ValueError('Viewport cannot be smaller than its frame')
    if not (0<luminance_change<=1 and 0<area_fraction<=1 and 0<red_saturation<=1
            and max_flashes_per_second>=0 and red_transition>=0 and red_scale>0 and pattern_pairs>=1):
        raise ValueError('Invalid PSE thresholds')
    rgb=[a.astype(float)/255 for a in frames]
    luma=[np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)@LUMA for a in rgb]
    general=[];red=[]
    for i in range(1,len(rgb)):
        delta=luma[i]-luma[i-1]
        general.append(np.where(np.abs(delta)>=luminance_change,np.sign(delta),0).astype(np.int8))
        a,b=rgb[i-1],rgb[i]
        def saturated(v):
            total=v.sum(axis=2)
            return np.divide(v[...,0],total,out=np.zeros_like(total),where=total>0)>=red_saturation
        red_a=np.maximum(0,a[...,0]-a[...,1]-a[...,2])*red_scale
        red_b=np.maximum(0,b[...,0]-b[...,1]-b[...,2])*red_scale
        difference=red_b-red_a
        red.append(np.where((saturated(a)|saturated(b)) & (np.abs(difference)>red_transition),
                            np.sign(difference),0).astype(np.int8))
    needed=area_fraction*canvas[0]*canvas[1]
    rows=[]
    for name,fields in [('general_flash',general),('red_flash',red)]:
        events,transitions=_paired_events(fields,fps,needed)
        value=_max_window(events)
        rows.append(report('pse.'+name,subject,value,max_flashes_per_second,unit='flashes/second',
            metrics=dict(flash_times_s=events,qualifying_transition_times_s=transitions,
                         area_fraction=area_fraction,required_pixels=needed,
                         equivalent_area_threshold=area_fraction*np.prod(REFERENCE_CANVAS).item())))
    rows.append(report('pse.spatial_pattern',subject,None,pattern_pairs,unit='light-dark pairs',
        reason='Report only: regular stripes/checks >=5 pairs over >=20% area are not robustly computed; spatial rule requires review'))
    return report('pse_check',subject,max(r['value'] for r in rows[:2]),max_flashes_per_second,
        unit='temporal_flashes/second',metrics=dict(results=rows,fps=fps,canvas_size=list(canvas),
            thresholds=dict(luminance_change=luminance_change,area_fraction=area_fraction,
                red_saturation=red_saturation,red_transition=red_transition,red_scale=red_scale),
            coverage='general and red temporal flash rules only; spatial rule UNEVALUABLE'))


evaluate=check
