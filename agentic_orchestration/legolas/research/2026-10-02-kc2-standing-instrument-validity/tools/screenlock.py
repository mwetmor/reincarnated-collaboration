import numpy as np
K=0.537
A=np.load('ref_frames2.npy')   # wave,t,r,spd,vr,vt,blk,nblk,tid,sx,sy,w,n
c=np.load('cam60g.npy'); ct=c[:,0]
# camera content velocity smoothed like kinematics (boxcar 15 on cumulative, gradient)
cx=np.concatenate([[0],np.cumsum(c[:,1])]); cy=np.concatenate([[0],np.cumsum(c[:,2])]); ctt=np.concatenate([ct,[ct[-1]+1/60]])
ker=np.ones(15)/15
scx=np.convolve(cx,ker,mode='same'); scy=np.convolve(cy,ker,mode='same')
vcx=np.gradient(scx,ctt); vcy=np.gradient(scy,ctt)/K
camspd=np.hypot(vcx,vcy)
out=[]
tids=np.unique(A[:,8])
lock=np.zeros(len(A),bool); scrspd=np.zeros(len(A)); cs=np.zeros(len(A))
for tid in tids:
    m=np.where(A[:,8]==tid)[0]
    t=A[m,1]; sx=A[m,9]; sy=A[m,10]/K
    # screen positions are raw (unsmoothed) at kinematics frames; smooth again lightly
    if len(m)<5: continue
    k5=np.ones(9)/9
    ssx=np.convolve(sx,k5,mode='same'); ssy=np.convolve(sy,k5,mode='same')
    v=np.hypot(np.gradient(ssx,t),np.gradient(ssy,t))
    j=np.clip(np.searchsorted(ctt,t),0,len(ctt)-1)
    scrspd[m]=v; cs[m]=camspd[j]
np.save('scr_cam.npy',np.column_stack([scrspd,cs]))
mov=cs>300
print('frames with camera >300 gpx/s:',mov.sum())
for lo,hi in [(0,150),(150,300),(300,600),(600,1400)]:
    b=(A[:,2]>=lo)&(A[:,2]<hi)
    for nm,ws in [('narrow',A[:,11]<21),('wide',A[:,11]>=40),('all',A[:,11]>0)]:
        s=b&ws&mov
        print(lo,hi,nm,'n',s.sum(),'screen-fixed (<50 px/s) while cam>300:',round((scrspd[s]<50).mean(),3))
