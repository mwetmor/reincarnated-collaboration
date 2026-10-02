import numpy as np, sys
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
c=np.load('cam60g.npy'); ct=c[:,0]
k=np.ones(15)/15
lfx=np.convolve(c[:,1],k,mode='same'); hfx=c[:,1]-lfx
lfy=np.convolve(c[:,2],k,mode='same'); hfy=c[:,2]-lfy
R2,ctt,cx,cy=load(); W,pw=world(R2,ctt,cx,cy)
rows=[]
for wave,t0,t1 in WAVES:
    for tr in track(W,t0,t1):
        if len(tr['p'])<60: continue
        p=np.array(tr['p']); t=p[:,0]
        for i in range(len(t)-1):
            if abs(t[i+1]-t[i]-1/60)>1e-3: continue
            kk=int(np.argmin(abs(ct-t[i])))
            rows.append((c[kk,1],hfx[kk],lfx[kk],c[kk,2],hfy[kk],p[i+1,3]-p[i,3],p[i+1,4]-p[i,4],p[i+1,1]-p[i,1],p[i+1,2]-p[i,2], abs(ct[kk]-t[i])))
Z=np.array(rows); print('max time mismatch',Z[:,9].max())
def sl(x,y): return round(np.cov(x,y)[0,1]/np.var(x),3)
print('screen dx on cam dx',sl(Z[:,0],Z[:,5]),' on cam hf',sl(Z[:,1],Z[:,5]),' on cam lf',sl(Z[:,2],Z[:,5]))
print('world dx on cam dx',sl(Z[:,0],Z[:,7]),' on hf',sl(Z[:,1],Z[:,7]),' on lf',sl(Z[:,2],Z[:,7]))
print('screen dy on cam dy',sl(Z[:,3],Z[:,6]),' on hf',sl(Z[:,4],Z[:,6]))
print('world dy on cam dy',sl(Z[:,3],Z[:,8]),' on hf',sl(Z[:,4],Z[:,8]))
print('check world-screen+cam', np.abs(Z[:,7]-(Z[:,5]-Z[:,0])).max())
np.save('camstep.npy',Z)
