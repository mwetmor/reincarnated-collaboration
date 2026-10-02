import numpy as np, sys
sys.path.insert(0,'.')
from d1b import *
from d1run import WAVES
def collect2(corridor=70.0, R=None, cam=None):
    if R is None:
        R,ctt,cx,cy=load()
    else:
        ctt,cx,cy=cam
    W,pw=world(R,ctt,cx,cy)
    rec=[]; tid=0
    for wave,t0,t1 in WAVES:
        for tr in track(W,t0,t1):
            if len(tr['p'])<int(1.0*FPS): continue
            k=kinematics(tr,pw,W,corridor=corridor)
            if k is None: continue
            n=len(k['t']); tid+=1
            rec.append(np.column_stack([np.full(n,wave),k['t'],k['r'],k['spd'],k['vr'],k['vt'],
               k['blocked'].astype(float),k['nblk'],np.full(n,tid),k['scr'][:,0],k['scr'][:,1],k['scr'][:,2],np.full(n,k['n'])]))
    return np.vstack(rec)
if __name__=='__main__':
    A=collect2(); np.save('ref_frames2.npy',A); print(A.shape)
