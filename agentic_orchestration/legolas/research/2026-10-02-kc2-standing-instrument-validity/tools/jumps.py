import numpy as np, sys, json
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
rows=[]
for wave,t0,t1 in WAVES:
    for tr in track(W,t0,t1):
        if len(tr['p'])<60: continue
        p=np.array(tr['p']); t=p[:,0]; wx=p[:,1]; wy=p[:,2]/K; sx=p[:,3]; w=p[:,5]
        px=np.array([pw[round(tt,4)][0] for tt in t]); py=np.array([pw[round(tt,4)][1]/K for tt in t])
        r=np.hypot(px-wx,py-wy)
        for i in range(1,len(t)):
            gap=round((t[i]-t[i-1])*60)
            rows.append((r[i],gap,wx[i]-wx[i-1],wy[i]-wy[i-1],w[i]-w[i-1],w[i-1],w[i]))
J=np.array(rows)
step=np.hypot(J[:,2],J[:,3])
for a,b in [(0,150),(150,300),(300,600),(600,1400)]:
    m=(J[:,0]>=a)&(J[:,0]<b); big=m&(step>12)
    dxonly=big&(np.abs(J[:,3])<=4)
    trunc=big&(np.abs(np.abs(J[:,2])-np.abs(J[:,4]))<=3)&(np.abs(J[:,3])<=4)   # x moves by ~ the width change: left-edge truncation/restoration
    print(f'{a}-{b}: n={m.sum()} gaps>1 frame {round((m&(J[:,1]>1)).mean()/m.mean(),3)}  big-step(>12gpx) {round(big.sum()/m.sum(),3)}'
          f'  of which x-only {round(dxonly.sum()/max(1,big.sum()),2)}  x-shift==width-change (left-edge truncation) {round(trunc.sum()/max(1,big.sum()),2)}  y-shift>=10gpx {round((big&(np.abs(J[:,3])>=10)).sum()/max(1,big.sum()),2)}')
