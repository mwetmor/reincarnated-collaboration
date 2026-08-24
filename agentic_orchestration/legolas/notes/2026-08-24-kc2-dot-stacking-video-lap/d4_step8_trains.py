"""STEP 8 — TICK TRAINS. A 'train' is a maximal chain of SMALL damage events (-1..-60) whose
consecutive gaps are 5-7 frames (the measured 100 ms +/- 1-frame sampling jitter).
Within a train, the per-tick magnitude sequence is the observable that discriminates stacking."""
import collections, statistics
from d4_lib import load_trace, FPS
HPMAX=20005
frames=load_trace(); ks=sorted(frames)
ev=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        h0=frames[ks[i-1]][1]; h1=frames[ks[i]][1]; d=h1-h0
        if -60<=d<=-1: ev.append((ks[i], frames[ks[i]][0], -d, h0))
trains=[]; cur=[ev[0]]
for a,b in zip(ev,ev[1:]):
    if 5<=(b[0]-a[0])<=7: cur.append(b)
    else:
        if len(cur)>=4: trains.append(cur)
        cur=[b]
if len(cur)>=4: trains.append(cur)
print(f'small events {len(ev)}; TICK TRAINS (>=4 ticks at 100ms cadence): {len(trains)}')
trains.sort(key=len, reverse=True)
for tr in trains[:14]:
    mags=[e[2] for e in tr]
    dur=(tr[-1][0]-tr[0][0])/FPS
    gaps=[b[0]-a[0] for a,b in zip(tr,tr[1:])]
    print(f'\n t0={tr[0][1]:9.4f}  n={len(tr):2d}  span={dur:5.3f}s  gaps={gaps}')
    print(f'   magnitudes: {mags}')
    print(f'   distinct={sorted(set(mags))}  min={min(mags)} max={max(mags)} ratio={max(mags)/min(mags):.2f}')
