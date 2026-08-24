"""STEP 7 — TICK STRUCTURE. Treat every negative delta as a damage EVENT. Ask:
 (1) is there a periodic component (a global DoT tick clock)?
 (2) what is the magnitude spectrum of SMALL events (DoT-scale, not direct-hit scale)?"""
import collections, statistics
from d4_lib import load_trace, FPS
HPMAX=20005
frames=load_trace(); ks=sorted(frames)
ev=[]   # (frame, t, delta) for negative deltas on adjacent unclipped pairs
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        h0=frames[ks[i-1]][1]; h1=frames[ks[i]][1]; d=h1-h0
        if d<0: ev.append((ks[i], frames[ks[i]][0], d, h0<HPMAX))
print(f'negative-delta events (whole trace): {len(ev)}')
small=[e for e in ev if -40<=e[2]<=-1]
print(f'  SMALL events (-1..-40, DoT-scale): {len(small)}')
big=[e for e in ev if e[2]<-200]
print(f'  LARGE events (< -200, direct-hit scale): {len(big)}')
print(f'  mid (-41..-200): {len(ev)-len(small)-len(big)}')

# inter-event interval for SMALL events, within contiguous stretches
iv=collections.Counter()
for a,b in zip(small, small[1:]):
    gap=b[0]-a[0]
    if 1<=gap<=40: iv[gap]+=1
tot=sum(iv.values())
print(f'\ninter-SMALL-event gaps (frames @60fps), n={tot}:')
for g in sorted(iv):
    if iv[g]>=8:
        print(f'   {g:3d} fr = {g/FPS*1000:6.1f} ms : {iv[g]:4d}  {100*iv[g]/tot:5.1f}%')
# magnitude spectrum of small events
mg=collections.Counter(e[2] for e in small)
print('\nSMALL event magnitude spectrum (count>=10):')
for m in sorted(mg, reverse=True):
    if mg[m]>=10: print(f'   {m:+4d} : {mg[m]:4d}')
