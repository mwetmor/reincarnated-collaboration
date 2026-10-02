import numpy as np, sys
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
rows=[]
for wave,t0,t1 in WAVES:
    for tr in track(W,t0,t1):
        if len(tr['p'])<60: continue
        p=np.array(tr['p']); t=p[:,0]; wx=p[:,1]; wy=p[:,2]/K; w=p[:,5]; sx=p[:,3]; sy=p[:,4]
        dt=np.diff(t); ok=np.abs(dt-1/60)<1e-3
        dx=np.diff(wx); dy=np.diff(wy)
        # range at frame (raw)
        px=np.array([pw[round(tt,4)][0] for tt in t]); py=np.array([pw[round(tt,4)][1]/K for tt in t])
        r=np.hypot(px-wx,py-wy)
        for i in np.where(ok)[0]:
            rows.append((wave,r[i],w[i],w[i+1],dx[i],dy[i], dx[i+1] if i+1<len(dx) and ok[min(i+1,len(ok)-1)] else np.nan, dy[i+1] if i+1<len(dy) and ok[min(i+1,len(ok)-1)] else np.nan, sx[i+1]-sx[i], wx[i+1]-wx[i]))
J=np.array(rows); np.save('jit.npy',J)
print(J.shape)
for lo,hi in [(0,150),(150,300),(300,600),(600,1400)]:
    b=(J[:,1]>=lo)&(J[:,1]<hi)
    for nm,s in [('narrow',b&(J[:,2]<21)),('wide',b&(J[:,2]>=40))]:
        d=np.hypot(J[s,4],J[s,5]); 
        ac=np.nanmean(J[s,4]*J[s,6])/np.nanmean(J[s,4]**2)
        acy=np.nanmean(J[s,5]*J[s,7])/np.nanmean(J[s,5]**2)
        dw=np.abs(J[s,3]-J[s,2])
        print(lo,hi,nm,len(d),'|step| p50/p90/p99',np.percentile(d,[50,90,99]).round(1),'lag1 ac x/y',round(ac,2),round(acy,2),'|dw|>3:',round((dw>3).mean(),3))
