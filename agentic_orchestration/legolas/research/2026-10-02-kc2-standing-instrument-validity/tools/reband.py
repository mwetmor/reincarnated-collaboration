"""Referent re-banded to the ORACLE's range definition: body ground point (plate + OFF screen px) to the player's
ground point.  Speeds are unchanged (a constant offset cancels in the derivative).  FOOTAGE; post-registration."""
import numpy as np, sys, json
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
edges=[0,100,150,220,300,400,600,900,1400]
out={}
recs=[]
for wave,t0,t1 in WAVES:
    for tr in track(W,t0,t1):
        if len(tr['p'])<60: continue
        k=kinematics(tr,pw,W)
        if k is None: continue
        for q in range(len(k['t'])):
            recs.append((k['sx'][q],k['sy'][q],k['px'][q],k['py'][q],k['spd'][q],k['scr'][q,2]))
Z=np.array(recs)   # sx, sy are ground-plane (y already /K); px,py ground-plane
for OFF in [0,80,115,160]:
    gy=Z[:,1]+OFF/K
    r=np.hypot(Z[:,0]-Z[:,2],gy-Z[:,3]); b=np.digitize(r,edges)-1
    sf=[round(float((Z[b==i,4]<50).mean()),3) if (b==i).any() else None for i in range(8)]
    n=[int((b==i).sum()) for i in range(8)]
    ins=b<4; mid=(b==4)|(b==5)
    out[OFF]=dict(still_by_band=sf,n=n,inside_300=round(float((Z[ins,4]<50).mean()),3),band_300_600=round(float((Z[mid,4]<50).mean()),3),
                  inside_300_wide=round(float((Z[ins&(Z[:,5]>=40),4]<50).mean()),3),band_300_600_wide=round(float((Z[mid&(Z[:,5]>=40),4]<50).mean()),3))
    print(OFF,out[OFF])
json.dump(out,open('reband.json','w'),indent=1)
