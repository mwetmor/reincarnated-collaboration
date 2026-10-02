"""Referent transient anchor residuals (raw - 9-frame median), in SCREEN px, pooled by the referent frame's range band."""
import numpy as np, sys
from scipy.ndimage import median_filter
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
edges=[0,100,150,220,300,400,600,900,1400]
pools={i:[] for i in range(8)}
for wave,t0,t1 in WAVES:
    for tr in track(W,t0,t1):
        if len(tr['p'])<60: continue
        p=np.array(tr['p']); t=p[:,0]; wx=p[:,1]; wys=p[:,2]
        ex=wx-median_filter(wx,9,mode='nearest'); ey=wys-median_filter(wys,9,mode='nearest')
        px=np.array([pw[round(tt,4)][0] for tt in t]); py=np.array([pw[round(tt,4)][1] for tt in t])
        r=np.hypot(px-wx,(py-wys)/K); b=np.digitize(r,edges)-1
        for i in range(len(t)):
            if 0<=b[i]<8: pools[b[i]].append((ex[i],ey[i]))
np.savez('resid_pools.npz',**{f'b{i}':np.array(pools[i]) for i in range(8)})
print({i:len(pools[i]) for i in range(8)})
