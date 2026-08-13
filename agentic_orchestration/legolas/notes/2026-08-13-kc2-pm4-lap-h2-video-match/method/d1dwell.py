import numpy as np, sys, json
sys.path.insert(0,'/tmp/pm4h2')
from d1b import *
from d1run import WAVES, V_STILL, R_CONTACT, spans
R,ctt,cx,cy=load(); W,pw=world(R,ctt,cx,cy)
dw_b=[]; dw_u=[]; prof=[]
tracks_out=[]
for wave,t0,t1 in WAVES:
    idx=0
    for tr in sorted(track(W,t0,t1),key=lambda x:-len(x['p'])):
        if len(tr['p'])<int(1.0*FPS): continue
        k=kinematics(tr,pw,W)
        if k is None: continue
        idx+=1
        still=k['spd']<V_STILL
        out=k['r']>R_CONTACT
        for a,b in spans(still&out&k['blocked'],6): dw_b.append((b-a)/FPS)
        for a,b in spans(still&out&(~k['blocked']),6): dw_u.append((b-a)/FPS)
        prof.append(np.column_stack([k['r'],still.astype(float),k['blocked'].astype(float),
                                     k['vt'],np.abs(k['vr']),k['spd']]))
        tracks_out.append(dict(wave=wave,idx=idx,t0=float(k['t'][0]),t1=float(k['t'][-1]),
            n=int(k['n']),r0=float(k['r'][0]),r1=float(k['r'][-1]),
            blkfrac=float(k['blocked'].mean()),stillfrac=float(still.mean()),
            tangfrac=float((k['vt']>np.abs(k['vr'])).mean()),
            maxdwell_blocked=float(max([(b-a)/FPS for a,b in spans(still&out&k['blocked'],6)],default=0.0)),
            tangpath=float(np.trapezoid(k['vt'],k['t'])),
            radpath=float(np.trapezoid(np.abs(k['vr']),k['t'])),
            medspd=float(np.median(k['spd']))))
json.dump(tracks_out,open('/tmp/pm4h2/d1tracks.json','w'))
db=np.array(dw_b); du=np.array(dw_u)
print('DWELL SPANS (continuous still & outside contact):')
print('  BLOCKED   n=%d  median %.2f s  p90 %.2f  max %.2f  ;  >=1.0s: %d  >=1.5s: %d  >=2.5s: %d'%(
  len(db),np.median(db),np.percentile(db,90),db.max(),(db>=1).sum(),(db>=1.5).sum(),(db>=2.5).sum()))
print('  UNBLOCKED n=%d  median %.2f s  p90 %.2f  max %.2f  ;  >=1.0s: %d  >=1.5s: %d  >=2.5s: %d'%(
  len(du),np.median(du),np.percentile(du,90),du.max(),(du>=1).sum(),(du>=1.5).sum(),(du>=2.5).sum()))
P=np.vstack(prof)
print()
print('PROFILE vs range r (ground px):')
print('   r-band      n   still  blocked  tang-dom  med_spd')
for lo,hi in [(0,100),(100,150),(150,220),(220,300),(300,400),(400,600),(600,900)]:
    S=P[(P[:,0]>=lo)&(P[:,0]<hi)]
    if len(S)<200: continue
    print('  %4d-%4d %7d  %.3f   %.3f    %.3f    %6.1f'%(lo,hi,len(S),S[:,1].mean(),S[:,2].mean(),
        (S[:,3]>S[:,4]).mean(),np.median(S[:,5])))
print()
print('tracks recorded:',len(tracks_out))
