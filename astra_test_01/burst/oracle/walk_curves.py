"""Descriptive W-1..W-6 and stance-scroll instruments, no shipping verdict.

Head y is Cartesian-up (-image y) for bob extrema/phases. Raw image y is
retained. W-4 counts cyclic local minima including plateaux once. W-3 uses
centered head coordinates: PCA std minor/major, signed shoelace area over
peak-to-peak amplitudes, and zero crossings about mean x (zeros omitted).
W-6 is explicitly a projected tracked-side proxy; silhouettes cannot establish
anatomical same-side hands, hidden wrists, or legs. Missing data remain null.
"""
import re
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.signal import find_peaks
from gates.common import result
from .walk_landmarks import (MASK_PARAMS, ROW_MASK_PARAMS, mask_with_diagnostics,
    figure_mask_row, track_landmarks, track_head, _translate)


def _finite(a):
    return len(a)>0 and all(v is not None and np.isfinite(v) for v in a)


def phase_table(landmarks_seq):
    n=len(landmarks_seq)
    if not n: return []
    events=[]
    for i,d in enumerate(landmarks_seq):
        for side in ('L','R'):
            if d.get('planted_'+side) is True and landmarks_seq[(i-1)%n].get('planted_'+side) is False:
                events.append((i,side))
    contacts=sorted(set(i for i,s in events))
    valid=len(events)==2 and len(contacts)==2 and len({s for i,s in events})==2
    table=[]
    for i,d in enumerate(landmarks_seq):
        phase=None; lead=None
        if valid:
            contact=min(contacts,key=lambda c:(i-c)%n)
            next_c=next(c for c in contacts if c!=contact)
            length=(next_c-contact)%n; offset=(i-contact)%n
            phase=('CONTACT' if offset==0 else 'DOWN' if offset/length<.5 else 'PASSING' if offset/length<.75 else 'UP')
            lead=next(s for c,s in events if c==contact)
        table.append(dict(frame=i,printed_phase=i+1,phase=phase,contact= i in contacts,
                          lead_track=lead,planted=d.get('planted',{}),
                          contact_sides=[s for c,s in events if c==i],
                          boundary_contact=i==0 and i in contacts,
                          reason=None if valid else f'expected two contact events; observed {len(contacts)}'))
    return table


def bob(series, H=1., phases=None):
    if not _finite(series) or not np.isfinite(H) or H<=0:
        return dict(W1=None,W2=None,W4=None)
    y=-np.asarray(series,dtype=float);n=len(y)
    peaks=find_peaks(np.tile(-y,3))[0]
    minima=[int(i-n) for i in peaks if n<=i<2*n] if np.ptp(y)>0 else []
    mins=np.flatnonzero(np.isclose(y,y.min())).tolist();maxs=np.flatnonzero(np.isclose(y,y.max())).tolist()
    mapped=lambda ids:[dict(frame=i,phase=phases[i]['phase'] if phases else None) for i in ids]
    return dict(W1=float(np.ptp(y)/H), W2=dict(min=mapped(mins),max=mapped(maxs),coordinate='Cartesian up; negative image y'),W4=len(minima),minima_frames=minima)


def head_path(cx,cy):
    if len(cx)!=len(cy) or len(cx)<3 or not _finite(cx) or not _finite(cy):
        return dict(W3a=None,W3b=None,W3c=None)
    p=np.column_stack((cx,-np.array(cy,dtype=float)));p-=p.mean(axis=0)
    eigen=np.linalg.eigvalsh(p.T@p/len(p)); ratio=float(np.sqrt(max(0,eigen[0])/eigen[1])) if eigen[1]>1e-12 else None
    spans=np.ptp(p,axis=0);denom=float(np.prod(spans))
    area=float(np.sum(p[:,0]*np.roll(p[:,1],-1)-np.roll(p[:,0],-1)*p[:,1])/2)
    signs=np.sign(p[:,0][np.abs(p[:,0])>1e-9])
    crossings=int(np.count_nonzero(signs!=np.roll(signs,1))) if len(signs) else 0
    return dict(W3a=ratio,W3b=area/denom if denom>1e-12 else None,W3c=crossings,signed_area_px2=area)


def arm_swing(seq,H=1.):
    n=len(seq); amplitude={};opposition={};valid_counts={}
    for side in ('L','R'):
        a=[d.get('wrist_ext_'+side) for d in seq];l=[d.get('foot_'+side+'_x') for d in seq]
        amplitude[side]=float(np.ptp(a)/H) if _finite(a) else None
        valid=[i for i in range(n) if a[i] is not None and l[i] is not None]
        valid_counts[side]=len(valid)
        if len(valid)!=n or n<3:
            opposition[side]=None;continue
        # Left extent grows toward negative x; right toward positive x.
        arm=np.array(a)*(-1 if side=='L' else 1);leg=np.array(l)-np.array([d['torso_cx'] for d in seq])
        arm-=arm.mean();leg-=leg.mean()
        if np.ptp(arm)<1e-9 or np.ptp(leg)<1e-9:
            opposition[side]=None
        else:
            opposition[side]=float(np.mean((arm*leg<=1e-9)))
    values=list(opposition.values())
    return dict(W5=amplitude,W6=float(np.mean(values)) if all(v is not None for v in values) else None,
                W6_per_arm=opposition,valid_frames_per_arm=valid_counts,
                identity_note='projected track opposition, not independently established anatomical same-side identity')


def sole_scroll_planted_lineage(seq):
    out={};all_delta=[]
    for side in ('L','R'):
        x=[d.get('foot_'+side+'_x') if d.get('planted_'+side) else None for d in seq]
        delta=[(x[(i+1)%len(x)]-v) if v is not None and x[(i+1)%len(x)] is not None else None for i,v in enumerate(x)]
        finite=[v for v in delta if v is not None];all_delta.extend(finite)
        mean=float(np.mean(finite)) if finite else None
        out[side]=dict(planted_x_px=x,delta_px_per_frame=delta,mean_scroll_px_per_frame=mean,
                       slip_px_per_frame=[v-mean if v is not None else None for v in delta],
                       slip_rms_px_per_frame=float(np.std(finite)) if finite else None)
    out['mean_scroll_px_per_frame']=float(np.mean(all_delta)) if all_delta else None
    out['slip_rms_px_per_frame']=float(np.std(all_delta)) if all_delta else None
    return out


def sole_scroll(seq):
    """Observed swing-foot velocity; no seam difference on a translating plate."""
    out={};pooled=[]
    for side in ('L','R'):
        xs=[d.get('foot_'+side+'_x') for d in seq]
        velocity=[]
        for i,d in enumerate(seq):
            prev=xs[i-1] if i else None
            value=xs[i]-prev if i and xs[i] is not None and prev is not None and d.get('planted_'+side) is False else None
            velocity.append(value)
        finite=[v for v in velocity if v is not None];pooled.extend(finite)
        out[side]=dict(swing_x_px=[x if d.get('planted_'+side) is False else None for x,d in zip(xs,seq)],
                       delta_px_per_frame=velocity,mean_scroll_px_per_frame=float(np.mean(finite)) if finite else None,
                       observed_velocity_frames=len(finite))
    out['mean_scroll_px_per_frame']=float(np.mean(pooled)) if pooled else None
    out['mean_absolute_speed_px_per_frame']=float(np.mean(np.abs(pooled))) if pooled else None
    out['estimator']='backward velocity on observed non-planted frames; missing tracks and seam excluded'
    out['planted_scroll_lineage']=sole_scroll_planted_lineage(seq)
    return out


def measure_sequence(seq,lateral=True,w1_floor=None,subject='walk'):
    valid=all(d.get('valid',True) for d in seq) and bool(seq)
    if not valid:
        return dict(summary={'W1':None,'W2':None,'W3a':None,'W3b':None,'W3c':None,'W4':None,'W5':None,'W6':None,'sole_scroll':None},landmarks=seq,phase_table=[],results=[result('oracle_walk',subject,notes='empty mask')])
    H=float(np.median([d['H'] for d in seq]));phase=phase_table(seq)
    s={**bob([d['head_top_y'] for d in seq],H,phase),**head_path([d['head_cx'] for d in seq],[d['head_top_y'] for d in seq])}
    s['head_mask_bob_lineage']=bob([d.get('head_top_mask_y',d['head_top_y']) for d in seq],H,phase)
    s['head_ref_bob']=bob([d['head_ref_y'] for d in seq],H,phase)
    s.update(arm_swing(seq,H) if lateral else dict(W5=None,W6=None,W6_per_arm=None))
    s['sole_scroll']=sole_scroll(seq) if lateral else None
    s['H_median']=H
    s['W1_sanity_1_5_pct_H']=bool(.01<=s['W1']<=.05) if s['W1'] is not None else None
    s['contact_frames']=[p['frame'] for p in phase if p['contact']]
    s['head_track_flagged_frames']=[i for i,d in enumerate(seq) if d.get('head_track_valid') is False]
    s['projection_diagnostics']=dict(**arm_swing(seq,H),sole_scroll=sole_scroll(seq))
    notes=['H normalization uses clip median inclusive silhouette height; no per-frame rescaling',
           'Tracked head NCC drives W1/W2/W4; raw mask top retained under lineage names',
           'W1 outside 1-5%H flags an unreliable head track, not a veridical bob measurement',
           'W5 is a silhouette extent at 0.45H, not an identified wrist']
    if not lateral: notes.append('front/rear: W5, W6 and sole scroll are not meaningful and are null')
    if any(d.get('identity_ambiguous') for d in seq): notes.append('merged/hidden feet; identity and contact phase may be unreliable')
    results=[result('W1_floor',subject,s['W1'],w1_floor,op='>=',unit='fraction_H',notes='caller-supplied calibration floor' if w1_floor is not None else 'no committed floor')]
    for key,threshold,op in [('W1',.07,'<='),('W3a',.35,'<='),('W4',2,'=='),('W6',.75,'>=')]:
        results.append(result(key,subject,s.get(key),threshold,op=op,notes='SPEC descriptive screen; not a shipping verdict'))
    return dict(summary=s,landmarks=seq,phase_table=phase,results=results,notes=notes)


def frame_paths(directory,pattern):
    paths=list(Path(directory).glob(pattern))
    paths.sort(key=lambda p:([int(x) if x.isdigit() else x for x in re.split(r'(\d+)',p.name)]))
    if not paths: raise ValueError('no matching PNG frames')
    return paths


def curves(directory,pattern='*.png',fps=8.33,lateral=True,ours=False,w1_floor=None):
    if not np.isfinite(fps) or fps<=0: raise ValueError('fps must be positive finite')
    paths=frame_paths(directory,pattern)
    if len(paths)!=12: raise ValueError(f'expected 12 printed stride phases; got {len(paths)}')
    arrays=[];shape=None
    for path in paths:
        with Image.open(path) as im:
            a=np.array(im.convert('RGBA') if 'A' in im.getbands() else im.convert('RGB'))
        if shape is not None and a.shape[:2]!=shape:raise ValueError('frame dimensions differ')
        shape=a.shape[:2];arrays.append(a)
    masks,health=figure_mask_row(arrays,return_diagnostics=True)
    if ours and (shape!=(512,512) or any(h['method']!='frozen matte alpha >=128' for h in health)):
        raise ValueError('--ours requires registered 512x512 alpha/keyed frames')
    registered_frames=[];registered_masks=[]
    for a,m,h in zip(arrays,masks,health):
        dx,dy=h['grid_shift_xy'];registered_frames.append(_translate(a,dy,dx));registered_masks.append(_translate(m,dy,dx))
    seq=track_landmarks(registered_masks);heads=track_head(registered_frames,registered_masks)
    for lm,head,h in zip(seq,heads,health):
        lm.update(head);lm['grid_shift_xy']=h['grid_shift_xy']
        if lm.get('valid'):
            for key in ('head_top_y','head_cx','head_cy','head_top_mask_y'):
                lm[key+'_H']=lm[key]/lm['H'] if lm.get(key) is not None else None
    d=measure_sequence(seq,lateral,w1_floor,str(directory))
    d.update(frames=len(paths),fps=float(fps),mode='ours' if ours else 'ref',
             frame_names=[p.name for p in paths],mask_health=health,mask_params=ROW_MASK_PARAMS,
             coordinate_system='grid registered source pixels; native plot coordinates subtract grid_shift_xy')
    return d
