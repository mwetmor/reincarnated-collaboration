"""Per-frame controlled comparison: what does a monster DO when a body blocks its
line to the player, versus when nothing does?  This is the fork stated as a
measurable contrast rather than as a per-track label."""
import numpy as np, sys, json
sys.path.insert(0,'/tmp/pm4h2')
from d1b import *
from d1run import WAVES, V_STILL, R_CONTACT

def collect(corridor=70.0):
    R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
    rec=[]
    for wave,t0,t1 in WAVES:
        for tr in track(W,t0,t1):
            if len(tr['p'])<int(1.0*FPS): continue
            k=kinematics(tr,pw,W,corridor=corridor)
            if k is None: continue
            n=len(k['t'])
            rec.append(np.column_stack([np.full(n,wave),k['t'],k['r'],k['spd'],
                                        k['vr'],k['vt'],k['blocked'].astype(float),k['nblk']]))
    return np.vstack(rec)

if __name__=='__main__':
    for corridor in [50.0,70.0,100.0]:
        A=collect(corridor)
        out=A[(A[:,2]>R_CONTACT)&(A[:,2]<900)]   # outside contact, plate on screen & near
        blk=out[:,6]>0.5; unb=~blk
        def stats(S,name):
            still=(S[:,3]<V_STILL).mean()
            tang=(S[:,5]>np.abs(S[:,4])).mean()
            clos=(S[:,4]>60).mean()
            return f'  {name:<10} n={len(S):6d}  still={still:.3f}  tangential-dominant={tang:.3f}  closing={clos:.3f}  med_spd={np.median(S[:,3]):6.1f}  med_vt={np.median(S[:,5]):6.1f}  med_vr={np.median(S[:,4]):6.1f}'
        print(f'CORRIDOR={corridor:.0f} ground px   (frames outside contact r>{R_CONTACT:.0f})')
        print(stats(out[blk],'BLOCKED')); print(stats(out[unb],'UNBLOCKED'))
        # graded by number of blockers
        for nb in [1,2,3]:
            S=out[(out[:,7]>=nb)]
            if len(S)>500: print(stats(S,f'blk>={nb}'))
        print()
