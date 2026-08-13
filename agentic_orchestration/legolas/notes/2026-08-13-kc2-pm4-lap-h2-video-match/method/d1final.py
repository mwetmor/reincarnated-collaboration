import numpy as np, sys, csv, json
sys.path.insert(0,'/tmp/pm4h2')
from d1b import *
from d1run import WAVES, V_STILL, R_CONTACT, spans, classify
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
rows=[]; keep={}
for wave,t0,t1 in WAVES:
    idx=0
    for tr in sorted(track(W,t0,t1),key=lambda x:-len(x['p'])):
        if len(tr['p'])<int(1.0*FPS): continue
        k=kinematics(tr,pw,W)
        if k is None: continue
        idx+=1; tid='W%d-T%02d'%(wave,idx)
        lab,ev=classify(k)
        still=k['spd']<V_STILL; out=k['r']>R_CONTACT
        dwb=[(b-a)/FPS for a,b in spans(still&out&k['blocked'],6)]
        mv=k['spd']>100.0
        rows.append(dict(track_id=tid,wave=wave,t_start=round(float(k['t'][0]),3),
            t_end=round(float(k['t'][-1]),3),dur_s=round(float(k['t'][-1]-k['t'][0]),3),
            n_frames=int(k['n']),classification=lab,
            r_start_gpx=round(float(k['r'][0]),1),r_end_gpx=round(float(k['r'][-1]),1),
            r_min_gpx=round(float(k['r'].min()),1),
            blocked_frac=round(float(k['blocked'].mean()),3),
            still_frac=round(float(still.mean()),3),
            max_blocked_dwell_s=round(float(max(dwb,default=0.0)),3),
            med_speed_gpx_s=round(float(np.median(k['spd'])),1),
            med_v_radial_gpx_s=round(float(np.median(k['vr'])),1),
            med_v_tangential_gpx_s=round(float(np.median(k['vt'])),1),
            tang_ratio_moving=round(float(np.median(k['vt'][mv]/np.maximum(k['spd'][mv],1e-6))) if mv.sum()>10 else float('nan'),3),
            tang_path_gpx=round(float(np.trapezoid(k['vt'],k['t'])),0),
            radial_path_gpx=round(float(np.trapezoid(np.abs(k['vr']),k['t'])),0)))
        keep[tid]=k
rows.sort(key=lambda r:(r['wave'],-r['n_frames']))
with open('/tmp/pm4h2/tracks.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
import collections
print('tracks',len(rows),collections.Counter(r['classification'] for r in rows))
# exemplars: longest range-spanning tracks per wave
ex=[r for r in rows if r['r_start_gpx']>500 and r['r_min_gpx']<200 and r['dur_s']>2.5]
ex.sort(key=lambda r:-(r['r_start_gpx']-r['r_min_gpx']))
print('\nEXEMPLARS (far -> ring, dur>2.5 s):', len(ex))
for r in ex[:14]:
    print('  %-9s w%d %7.2f-%7.2f n=%3d %-20s r %5.0f->%5.0f  blk=%.2f  maxdwell=%.2f  vt=%5.0f vr=%5.0f  tangratio=%.2f'%(
      r['track_id'],r['wave'],r['t_start'],r['t_end'],r['n_frames'],r['classification'],
      r['r_start_gpx'],r['r_min_gpx'],r['blocked_frac'],r['max_blocked_dwell_s'],
      r['med_v_tangential_gpx_s'],r['med_v_radial_gpx_s'],r['tang_ratio_moving']))
np.save('/tmp/pm4h2/exemplar_ids.npy',np.array([r['track_id'] for r in ex[:14]]))
import pickle
pickle.dump({t:dict(t=k['t'],r=k['r'],vr=k['vr'],vt=k['vt'],spd=k['spd'],scr=k['scr'],blocked=k['blocked']) for t,k in keep.items()},open('/tmp/pm4h2/kin.pkl','wb'))
