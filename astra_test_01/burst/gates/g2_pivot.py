"""Separate root registration, visible sole midpoint, and planted trajectories.
A visible two-sole midpoint is NOT an independently annotated ground/root.
Trajectory inputs require persistent reviewed foot IDs; automatic x-sorting
cannot determine anatomical identity or planted intervals.
"""
import json
import numpy as np
from .common import rgba, result
from .register import frame_contacts

def root_anchor(anchor=None, subject='', pivot=(256,400), tolerance=4):
    if anchor is None:
        return result('g2_pivot',subject,threshold=tolerance,unit='px',notes='UNEVALUABLE: independent reviewed root anchor required; sole midpoint is separate')
    a=np.asarray(anchor,float)
    if a.shape!=(2,) or not np.isfinite(a).all(): raise ValueError('Expected finite root XY')
    error=np.abs(a-pivot)
    return result('g2_pivot',subject,float(error.max()),tolerance,unit='px',notes=json.dumps({'root':a.tolist(),'error_xy':error.tolist()}))

def visible_midpoint(image, subject='', regions=None, pivot=(256,400), tolerance=4):
    try:
        points=frame_contacts(rgba(image),regions)
    except ValueError as e:
        return result('g2_sole_midpoint',subject,threshold=tolerance,unit='px',notes=str(e))
    error=np.abs(np.mean(points,axis=0)-pivot)
    return result('g2_sole_midpoint',subject,float(error.max()),tolerance,unit='px',
                  notes=json.dumps({'points':points,'error_xy':error.tolist(),'method':'reviewed regions' if regions is not None else 'automatic run_03 fallback'}))

def planted_trajectory(points=None, planted=None, subject='', tolerance=None, expected_leads=None):
    """Report planted XY trajectories and max adjacent displacement in pixels.
    points: T x F x 2, persistent reviewed IDs; planted: T x F bool.
    tolerance is optional because in-place gait legitimately moves a planted sole.
    expected_leads optionally specifies the reviewed planted foot index per frame.
    """
    if points is None or planted is None:
        return result('g2_planted_sole',subject,threshold=tolerance,unit='px/frame',notes='UNEVALUABLE: persistent foot IDs and reviewed planted intervals required')
    p=np.asarray(points,float); m=np.asarray(planted,bool)
    if p.ndim!=3 or p.shape[2]!=2 or m.shape!=p.shape[:2] or not np.isfinite(p).all():
        raise ValueError('Expected finite T x F x 2 points and T x F planted flags')
    segments=[]
    for t in range(1,len(p)):
        for f in range(p.shape[1]):
            if m[t-1,f] and m[t,f]:
                delta=p[t,f]-p[t-1,f]
                segments.append(dict(frame=t,foot=f,delta_xy=delta.tolist(),distance=float(np.linalg.norm(delta))))
    notes={'points':p.tolist(),'planted':m.tolist(),'segments':segments}
    rows=[result('g2_planted_sole',subject,max((s['distance'] for s in segments),default=None),tolerance,
                 unit='px/frame',notes=(('UNEVALUABLE verdict: trajectory reported without calibrated tolerance; ' if tolerance is None else '')+json.dumps(notes)) if segments else 'UNEVALUABLE: no consecutive planted samples; '+json.dumps(notes))]
    if expected_leads is not None:
        if len(expected_leads)!=len(p): raise ValueError('Lead schedule length mismatch')
        mismatch=sum(not m[t,f] or m[t].sum()!=1 for t,f in enumerate(expected_leads))
        rows.append(result('g2_planted_leads',subject,int(mismatch),0,unit='frames',notes='Compared to supplied reviewed lead schedule'))
    return rows

def evaluate(image, subject='', anchor=None, regions=None, points=None, planted=None, **kwargs):
    trajectory=planted_trajectory(points,planted,subject,**kwargs)
    return [root_anchor(anchor,subject),visible_midpoint(image,subject,regions)]+(trajectory if isinstance(trajectory,list) else [trajectory])
