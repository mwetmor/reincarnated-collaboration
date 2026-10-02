"""Referent instrument noise floor: what still fraction does the Lap H-2 velocity pipeline report for a body that
does not move, given the referent's OWN per-frame anchor noise in each range band?  (FOOTAGE-derived instrument
property; no oracle input.)"""
import numpy as np, sys, json
from scipy.ndimage import median_filter
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
edges=[0,100,150,220,300,400,600,900,1400]
res={i:{'n':0,'fm':0} for i in range(8)}; resw={}
swaps={i:[0,0] for i in range(8)}
med_sd=[]
ker=np.ones(15)/15
recs=[]
for wave,t0,t1 in WAVES:
    for tr in track(W,t0,t1):
        if len(tr['p'])<60: continue
        p=np.array(tr['p']); t=p[:,0]; wx=p[:,1]; wy=p[:,2]/K; w=p[:,5]
        mx=median_filter(wx,9,mode='nearest'); my=median_filter(wy,9,mode='nearest')
        ex=wx-mx; ey=wy-my
        # pure-noise track through the identical smoother + gradient, on the identical sample times
        sx=np.convolve(ex,ker,mode='valid'); sy=np.convolve(ey,ker,mode='valid'); st=t[7:len(t)-7]
        v=np.hypot(np.gradient(sx,st),np.gradient(sy,st))
        # true kinematics of the same track for band assignment
        k=kinematics(tr,pw,W)
        if k is None: continue
        r=k['r']; b=np.digitize(r,edges)-1
        # per-frame step of the median-filtered path (persistent jumps)
        dm=np.hypot(np.diff(mx),np.diff(my))
        wc=w[7:len(t)-7]
        for i in range(len(v)):
            if 0<=b[i]<8:
                recs.append((b[i],v[i],wc[i],k['spd'][i],dm[min(i+7,len(dm)-1)]))
Z=np.array(recs); np.save('noisefloor_frames.npy',Z)
out={}
for i in range(8):
    m=Z[:,0]==i
    out[f'{edges[i]}-{edges[i+1]}']=dict(n=int(m.sum()),
        noise_only_still=round(float((Z[m,1]<50).mean()),3),
        noise_only_still_wide=round(float((Z[m&(Z[:,2]>=40),1]<50).mean()),3),
        noise_only_still_narrow=round(float((Z[m&(Z[:,2]<21),1]<50).mean()),3),
        noise_speed_p50=round(float(np.median(Z[m,1])),1), noise_speed_p90=round(float(np.percentile(Z[m,1],90)),1),
        measured_still=round(float((Z[m,3]<50).mean()),3),
        medpath_step_gt12_frac=round(float((Z[m,4]>12).mean()),4))
print(json.dumps(out,indent=1)); json.dump(out,open('noisefloor.json','w'),indent=1)
