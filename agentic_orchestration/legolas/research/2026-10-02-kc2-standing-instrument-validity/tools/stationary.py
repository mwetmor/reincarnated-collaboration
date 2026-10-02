"""Known-stationary proxy: segments where a referent track's ROBUST world position (rolling median, 0.5 s) stays
inside a 20-gpx disc for >= 2.5 s.  Such a body did not walk (any walk at >= 0.4 m/s would leave the disc in < 0.4 s).
Report what the Lap H-2 instrument (0.25 s boxcar, gradient, < 50 gpx/s) said about those same frames."""
import numpy as np, sys, json
from scipy.ndimage import median_filter
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
edges=[0,100,150,220,300,400,600,900,1400]
segs=[]; fr=[]
for wave,t0,t1 in WAVES:
    for tr in track(W,t0,t1):
        if len(tr['p'])<60: continue
        k=kinematics(tr,pw,W)
        if k is None: continue
        p=np.array(tr['p']); wx=p[:,1]; wy=p[:,2]/K
        mx=median_filter(wx,31,mode='nearest')[7:len(wx)-7]; my=median_filter(wy,31,mode='nearest')[7:len(wy)-7]
        t=k['t']; n=len(t)
        i=0
        while i<n:
            j=i; cxm,cym=mx[i],my[i]
            # grow while every robust position stays within 20 gpx of the running segment centre
            while j+1<n and np.hypot(mx[j+1]-cxm,my[j+1]-cym)<20:
                j+=1; cxm=np.mean(mx[i:j+1]); cym=np.mean(my[i:j+1])
            if t[j]-t[i]>=2.5:
                # shrink check: all inside 20 of final centre
                ok=np.hypot(mx[i:j+1]-cxm,my[i:j+1]-cym)<20
                sl=np.arange(i,j+1)[ok]
                segs.append(dict(wave=wave,t0=float(t[i]),t1=float(t[j]),dur=float(t[j]-t[i]),r_med=float(np.median(k['r'][sl])),
                                 still=float((k['spd'][sl]<50).mean()),w_med=float(np.median(k['scr'][sl,2])),n=len(sl)))
                for q in sl: fr.append((k['r'][q],k['spd'][q],k['scr'][q,2],wave))
                i=j+1
            else:
                i+=1
F=np.array(fr)
print('segments',len(segs),'frames',len(F))
out={}
for a,b in [(0,150),(150,300),(300,600),(600,1400)]:
    m=(F[:,0]>=a)&(F[:,0]<b)
    if m.sum(): out[f'{a}-{b}']=dict(n=int(m.sum()),instrument_still=round(float((F[m,1]<50).mean()),3),
        wide_still=round(float((F[m&(F[:,2]>=40),1]<50).mean()),3) if (m&(F[:,2]>=40)).sum() else None,
        narrow_still=round(float((F[m&(F[:,2]<21),1]<50).mean()),3) if (m&(F[:,2]<21)).sum() else None)
print(json.dumps(out,indent=1))
for s in sorted(segs,key=lambda s:-s['dur'])[:15]: print({k:(round(v,2) if isinstance(v,float) else v) for k,v in s.items()})
json.dump(dict(bands=out,segments=segs),open('stationary.json','w'),indent=1)
