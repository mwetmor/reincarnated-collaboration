import numpy as np, sys
sys.path.insert(0,'.')
from d1frames import collect
A=collect(70.0)
print(A.shape)
B=np.load('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-h2-video-match/method/d1_profile_frames.npy')
print(B.shape)
edges=[0,100,150,220,300,400,600,900,1400]
for i in range(8):
    m=(A[:,2]>=edges[i])&(A[:,2]<edges[i+1])
    print(edges[i],edges[i+1],m.sum(), round((A[m,3]<50).mean(),3))
np.save('ref_frames.npy',A)
