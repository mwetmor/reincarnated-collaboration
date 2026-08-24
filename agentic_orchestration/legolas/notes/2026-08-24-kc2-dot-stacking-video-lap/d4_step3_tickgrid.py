"""STEP 3 — INSTRUMENT CALIBRATION. Is delta==0 on unclipped frames (a) DoT cancelling regen,
or (b) the capture sampling a game that updates HP slower than 60 fps (duplicate frames)?
Discriminator: under (b), a 0 must be FOLLOWED by an accumulated larger jump."""
import collections, statistics
from d4_lib import load_trace, FPS
HPMAX=20005
frames=load_trace(); ks=sorted(frames)
seq=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        seq.append((ks[i], frames[ks[i-1]][1], frames[ks[i]][1]-frames[ks[i-1]][1]))
unc=[x for x in seq if x[1]<HPMAX]
c=collections.Counter(x[2] for x in unc)
print('exact counts, small deltas:')
for v in range(-3,9): print(f'  {v:+3d}: {c.get(v,0)}')

# conditional: delta AFTER a zero, restricted to quiet (no big hits) neighbourhoods
byframe={x[0]:x for x in unc}
after_zero=[]; after_pos=[]
for f,h0,x in unc:
    nxt=byframe.get(f+1)
    if nxt is None or not (-1<=nxt[2]<=9): continue
    if x==0: after_zero.append(nxt[2])
    elif x in (2,3): after_pos.append(nxt[2])
def summarise(name,arr):
    cc=collections.Counter(arr)
    print(f'\n{name}  n={len(arr)}  mean={statistics.mean(arr):.3f}')
    for v in sorted(cc): print(f'    {v:+3d}: {cc[v]:5d}  {100*cc[v]/len(arr):5.1f}%')
summarise('delta immediately AFTER a 0-delta frame', after_zero)
summarise('delta immediately AFTER a +2/+3 frame', after_pos)

# run-length of consecutive zeros
runs=collections.Counter(); cur=0; prev=None
for f,h0,x in unc:
    if prev is not None and f==prev+1 and x==0: cur+=1
    else:
        if cur: runs[cur]+=1
        cur = 1 if x==0 else 0
    prev=f
if cur: runs[cur]+=1
print('\nconsecutive-zero run lengths:', dict(sorted(runs.items())[:8]))
