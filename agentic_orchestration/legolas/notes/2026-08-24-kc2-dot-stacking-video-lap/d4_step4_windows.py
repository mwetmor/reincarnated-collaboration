"""STEP 4 — enumerate DECAY-CANDIDATE windows: contiguous frame runs with NO discrete hit
(no delta <= -4, which is far below the smallest post-mitigation monster hit) and length >= 1.0 s.
For each, report net slope. Cluster structure reveals the pure-regen ceiling."""
import statistics, collections
from d4_lib import load_trace, FPS
HPMAX=20005
frames=load_trace(); ks=sorted(frames)
pairs=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        pairs.append((ks[i], frames[ks[i]][0], frames[ks[i-1]][1], frames[ks[i]][1]))
# window = maximal run with no delta <= -4 ; require prev-hp < HPMAX (regen unclipped) throughout
wins=[]; cur=[]
prev=None
for f,t,h0,h1 in pairs:
    d=h1-h0
    ok = (prev is None or f==prev+1) and d > -4 and h0 < HPMAX
    if ok: cur.append((f,t,h0,h1))
    else:
        if len(cur)>=60: wins.append(cur)
        cur=[(f,t,h0,h1)] if (d>-4 and h0<HPMAX) else []
    prev=f
if len(cur)>=60: wins.append(cur)
print(f'unclipped, hit-free windows >= 1.0 s : {len(wins)}')
print(f"{'t_start':>10} {'dur_s':>7} {'hp0':>6} {'hp1':>6} {'slope HP/s':>11} {'zero%':>7} {'>3%':>6}")
rows=[]
for w in wins:
    dur=(w[-1][0]-w[0][0]+1)/FPS
    h0=w[0][2]; h1=w[-1][3]
    slope=(h1-h0)/dur
    ds=[b-a for _,_,a,b in w]
    z=100*sum(1 for x in ds if x==0)/len(ds)
    big=100*sum(1 for x in ds if x>3)/len(ds)
    rows.append((w[0][1],dur,h0,h1,slope,z,big,w))
for r in sorted(rows,key=lambda z:-z[1]):
    print(f'{r[0]:10.4f} {r[1]:7.4f} {r[2]:6d} {r[3]:6d} {r[4]:11.2f} {r[5]:7.1f} {r[6]:6.1f}')
# leech-free subset: no delta > 3
clean=[r for r in rows if r[6]==0.0]
print(f'\nLEECH-FREE (no delta>+3) windows: {len(clean)}')
for r in sorted(clean,key=lambda z:-z[1]):
    print(f'  t={r[0]:10.4f} dur={r[1]:6.3f}s slope={r[4]:8.2f} HP/s  zero%={r[5]:5.1f}')
if clean:
    sl=[r[4] for r in clean]
    print(f'\nleech-free slope: n={len(sl)} min={min(sl):.2f} max={max(sl):.2f} median={statistics.median(sl):.2f}')
