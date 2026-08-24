"""STEP 2 — establish the pure-regen baseline empirically, on frames where regen is UNCLIPPED
(both endpoints strictly below hp_max) and no discrete hit landed."""
import collections, statistics
from d4_lib import load_trace, deltas, FPS
HPMAX=20005
frames = load_trace()
ks=sorted(frames)
d=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        h0=frames[ks[i-1]][1]; h1=frames[ks[i]][1]
        d.append((ks[i], frames[ks[i]][0], h0, h1, h1-h0))
# UNCLIPPED: previous frame strictly below max (so regen had headroom for a full frame)
unc=[x for x in d if x[2] < HPMAX]
print(f'adjacent pairs total {len(d)}; unclipped (prev hp<max) {len(unc)}')
c=collections.Counter(x[4] for x in unc)
print('\ndelta histogram on UNCLIPPED frames (top 24):')
for k,v in sorted(c.items(), key=lambda kv:-kv[1])[:24]:
    print(f'  {k:+7d}  x{v:5d}  {100*v/len(unc):5.2f}%')
band=[x for x in unc if 0<=x[4]<=6]
print(f'\nfraction of unclipped frames with delta in [0,6]: {len(band)/len(unc):.3f}')
# The pure-regen quantum: mean of the {2,3} population
r23=[x[4] for x in unc if x[4] in (2,3)]
print(f'\n+2/+3 population n={len(r23)} mean={statistics.mean(r23):.4f} HP/frame -> {statistics.mean(r23)*FPS:.2f} HP/s')
n2=sum(1 for v in r23 if v==2); n3=len(r23)-n2
print(f'   +2 x{n2}  +3 x{n3}   ratio {n3/len(r23):.4f}')
