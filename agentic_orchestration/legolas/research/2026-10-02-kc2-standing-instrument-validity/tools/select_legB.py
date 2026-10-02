import numpy as np
def legB(A):
    """per salt, keep the LAST invocation of each wave (the PW-folded per-wave series the instruments count)."""
    keep=np.zeros(len(A),bool)
    for s in [x for x in np.unique(A[:,0]) if x>=0]:
        ms=A[:,0]==s
        for w in range(151,161):
            m=ms&(A[:,1]==w)
            if not m.any(): continue
            last=A[m,18].max(); keep|=m&(A[:,18]==last)
    return keep
if __name__=='__main__':
    A=np.load('v310full_s0-19.npz')['rows']; k=legB(A); B=A[k]
    HB=np.array([0,100,150,220,300,400,600,900,1400])/122.0
    r=np.hypot(B[:,14]-B[:,16],B[:,15]-B[:,17]); b=np.digitize(r,HB)-1
    sf=[round((B[b==i,12]==0).mean(),3) for i in range(8)]; n=[int((b==i).sum()) for i in range(8)]
    print('sf',sf); print('n',n)
    print('inside 2.46', round(sum(sf[i]*n[i] for i in range(4))/sum(n[:4]),4), ' 2.46-4.92', round(((B[(b==4)|(b==5),12]==0).mean()),3))
    np.save('legB_rows.npy',B)
