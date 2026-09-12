"""Numeric animation instructions from frozen bands; no source pixels.

All positions are fractions of subject H, horizontal relative to the torso,
vertical above ground. Idle delta-y is image-down. Targets are not clamped to
ceilings and conflicting band intent is reported. Walk source trajectories,
when available, preserve phase and foot identity. Otherwise an explicit
procedural design supplies missing positions; it is not measured evidence.
"""
import math
import numpy as np


def _positive(value, name):
    if not isinstance(value, (int,float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(name+' must be positive finite')


def idle_sheet(bands_idle_row, n_frames, fps):
    row = bands_idle_row
    if type(n_frames) is not int or n_frames < 2: raise ValueError('n_frames must be integer >=2')
    _positive(fps, 'fps')
    period = row.get('breath_period_s')
    if period is None: period = n_frames/fps
    _positive(period, 'breath_period_s')
    breath = row['breath_amplitude_H']['target']; head = row['head_sway_H']['target']
    if any(v is None or not math.isfinite(v) or v < 0 for v in (breath,head)):
        raise ValueError('finite nonnegative head and breath targets required')
    locks = list(row.get('lock_regions',[])); motion = list(row.get('motion_regions',[]))
    amplitudes = dict(head=head, shoulders_chest=breath)
    assertions = ['LOCK '+name+': displacement <= '+str(row.get('lock_eps_H',.004))+' H.' for name in locks]
    motion_targets = {name:amplitudes.get(name,row.get('region_amplitudes_H',{}).get(name)) for name in motion}
    assertions += [f'MOTION {name}: peak-to-peak displacement target {value} H.' for name,value in motion_targets.items()]
    conflicts = [f'{name} is LOCK but has nonzero amplitude target {amplitudes[name]} H'
                 for name in locks if amplitudes.get(name,0)>0]
    for name,key in [('head','head_sway_H'),('shoulders_chest','breath_amplitude_H')]:
        b=row[key]
        if b.get('ceiling') is not None and b['target']>b['ceiling']:
            conflicts.append(name+' target exceeds ceiling')
    table=[]; sentences=[]
    for i in range(n_frames):
        phase = 2*math.pi*i/fps/period
        dy = head/2*math.sin(phase); dw = breath/2*math.sin(phase)
        table.append(dict(frame=i,time_s=i/fps,phase_radians=phase,head_dy_H=dy,chest_dw_H=dw))
        sentences.append(f'frame {i+1} — head delta y {dy:+.6f} H (image-down), chest delta width {dw:+.6f} H.')
    cycles = n_frames/fps/period
    if not math.isclose(cycles,round(cycles),abs_tol=1e-9):
        conflicts.append('clip duration is not an integer multiple of band period; temporal seam is not periodic')
    return dict(kind='idle',n_frames=n_frames,fps=float(fps),period_s=float(period),
        period_source='band' if row.get('breath_period_s') is not None else 'clip_duration',
        committed=row.get('committed') is True,amplitudes_H=amplitudes,lock_regions=locks,
        motion_regions=motion,motion_amplitudes_H=motion_targets,assertions=assertions,
        conflicts=conflicts,frames=table,
        prompt_text='\n'.join(assertions+['INTENT CONFLICT: '+c+'.' for c in conflicts]+sentences))


def _rescale(values, amplitude, baseline):
    a=np.asarray(values,dtype=float)
    if not np.isfinite(a).all(): raise ValueError('nonfinite trajectory')
    span=float(np.ptp(a))
    if span == 0:
        if amplitude: raise ValueError('cannot phase a nonzero amplitude from a flat source trajectory')
        return np.full(len(a), baseline)
    return baseline+(a-a.mean())*amplitude/span


def walk_sheet(bands_walk_row, n_frames=12):
    if n_frames != 12: raise ValueError('walk requires the registered 12-frame phase table')
    row=bands_walk_row; bands=row.get('bands',row); phases=row.get('phase_table',[])
    if len(phases)!=12 or any(p.get('phase') not in ('CONTACT','DOWN','PASSING','UP') for p in phases):
        raise ValueError('valid 12-frame phase table required; phases are never fabricated')
    k=bands.get('parameters',{}).get('k_vert',2.)
    amplitude=bands['W1']['floor']*k
    _positive(amplitude, 'W1 floor times k_vert')
    source=row.get('curves',{}); seq=source.get('landmarks',[])
    summary=row.get('summary',source.get('summary',{}))
    H=summary.get('H_mean',summary.get('H_median'))
    conflicts=[]; assumptions=[]
    if bands['W1'].get('ceiling') is not None and amplitude>bands['W1']['ceiling']:
        conflicts.append('W1 target exceeds ceiling; target retained without clamping')
    if len(seq)==12 and H and all(d.get('head_top_y') is not None for d in seq):
        heights=_rescale([-d['head_top_y']/H for d in seq],amplitude,1.)
        trajectory_source='source numeric landmarks, normalized; head amplitude scaled'
    else:
        w2=bands.get('W2',{}); w2=w2.get('bands',w2.get('value',w2))
        knots={}
        for name,value in [('min',-1.),('max',1.)]:
            for entry in w2.get(name,[]): knots[entry['frame']]=value
        if len(knots)<2 or len(set(knots.values()))!=2:
            raise ValueError('walk needs numeric head trajectory or W2 extrema to phase bob')
        keys=sorted(knots)
        heights=1.+np.interp(np.arange(12),keys,[knots[i] for i in keys],period=12)*amplitude/2
        trajectory_source='periodic linear interpolation through W2 extrema'
        assumptions.append('missing measured sole trajectories: procedural stance/swing design, stride 0.30 H, clearance 0.06 H')
    table=[]; sentences=[]
    # Preserve source side names rather than claiming anatomical L/R assignment.
    names=('near','far') if any('near' in p.get('planted',{}) for p in phases) else ('L','R')
    arm_bands=bands.get('W5') or {};arm_bands=arm_bands.get('bands',arm_bands)
    soles_by_side={s:[] for s in names}
    for i,p in enumerate(phases):
        for j,side in enumerate(names):
            raw_side=('L','R')[j]
            planted=p.get('planted',{}).get(side)
            if type(planted) is not bool: raise ValueError('explicit boolean planted flags required per sole')
            d=seq[i] if len(seq)==12 else {}
            x=d.get('foot_'+raw_side+'_x');y=d.get('foot_'+raw_side+'_y')
            if H and x is not None and y is not None:
                x=(x-d.get('torso_cx',0))/H
                ground=d.get('ground_line_y',0)
                height=(ground-y)/H
            else:
                contacts=[q['frame'] for q in phases if q.get('planted',{}).get(side) is True and phases[(q['frame']-1)%12].get('planted',{}).get(side) is False]
                if len(contacts)!=1: raise ValueError('procedural sole design requires one stance onset per foot')
                offset=(i-contacts[0])%12
                stance_count=sum(q['planted'][side] for q in phases)
                if planted:
                    x=.15-.30*offset/max(1,stance_count-1); height=0.
                else:
                    progress=(offset-stance_count+1)/(12-stance_count+1)
                    x=-.15+.30*progress; height=.06*math.sin(math.pi*progress)
            soles_by_side[side].append(dict(x_H=float(x),height_H=float(height),planted=planted))
    # Opposing arm targets are hip-relative and have row target p2p amplitude.
    arms={}
    for side in names:
        x=np.array([p['x_H'] for p in soles_by_side[side]])
        arm=arm_bands.get(side,{})
        target=arm.get('target') if isinstance(arm,dict) else None
        if target is None:
            target=.08;assumptions.append(side+' arm amplitude missing; procedural 0.08 H target')
        span=float(np.ptp(x))
        arms[side]=-x*target/span if span else np.zeros(12)
    for i,p in enumerate(phases):
        soles={s:soles_by_side[s][i] for s in names}
        arm={s:float(arms[s][i]) for s in names}
        plants=[s for s in names if soles[s]['planted']]
        swing={s:soles[s]['x_H'] for s in names if not soles[s]['planted']}
        entry=dict(frame=i,phase=p['phase'],head_height_H=float(heights[i]),soles=soles,
                   planted_feet=plants,swing_foot_x_H=swing,arm_x_H=arm,
                   arm_opposition={s:bool(arm[s]*soles[s]['x_H']<0) for s in names})
        table.append(entry)
        description='; '.join(f'{s} sole x {v["x_H"]:+.6f} H, height {v["height_H"]:.6f} H, '+('planted' if v['planted'] else 'swing') for s,v in soles.items())
        sentences.append(f'frame {i+1} — {p["phase"]}: head height {heights[i]:.6f} H; {description}; '+
                         '; '.join(f'{s} arm x {v:+.6f} H, opposing same-side sole' for s,v in arm.items())+'.')
    return dict(kind='walk',n_frames=12,committed=row.get('committed') is True,
        head_amplitude_H=float(amplitude),k_vert=k,coordinate_system='x relative to torso; height above ground; units H',
        trajectory_source=trajectory_source,conflicts=conflicts,assumptions=assumptions,frames=table,
        prompt_text='\n'.join(['INTENT CONFLICT: '+s+'.' for s in conflicts]+['DESIGN ASSUMPTION: '+s+'.' for s in assumptions]+sentences))
