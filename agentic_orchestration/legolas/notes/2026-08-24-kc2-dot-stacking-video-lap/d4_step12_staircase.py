"""STEP 12 — THE DECAY STAIRCASE, read directly off tick magnitude (no quiet window needed).
Segment each 100ms-cadence chain into level plateaus (>=3 ticks within +/-12% of level median),
then read the level SEQUENCE. Under full stacking of same-magnitude instances a descent falls in
EQUAL steps, one per expiring instance. Under refresh-only a type contributes exactly one step."""
import statistics, csv
from d4_lib import load_trace, FPS
frames=load_trace(); ks=sorted(frames)
ev=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        d=frames[ks[i]][1]-frames[ks[i-1]][1]
        if d<0: ev.append((ks[i], frames[ks[i]][0], -d))
chains=[];cur=[ev[0]]
for a,b in zip(ev,ev[1:]):
    if 5<=(b[0]-a[0])<=7: cur.append(b)
    else:
        if len(cur)>=6: chains.append(cur)
        cur=[b]
if len(cur)>=6: chains.append(cur)

def levels(ch, MIN=3, TOL=0.12):
    out=[];i=0;n=len(ch)
    while i<n:
        j=i+1
        while j<n:
            seg=[e[2] for e in ch[i:j+1]]; m=statistics.median(seg)
            if max(abs(x-m) for x in seg)<=TOL*m: j+=1
            else: break
        if j-i>=MIN:
            seg=[e[2] for e in ch[i:j]]
            out.append((ch[i][1], j-i, statistics.median(seg))); i=j
        else: i+=1
    return out

print(f'cadence chains (>=6 ticks): {len(chains)}')
nstair=0
for ch in chains:
    lv=levels(ch)
    if len(lv)<2: continue
    seq=[f'{l[2]:.0f}x{l[1]}' for l in lv]
    vals=[l[2] for l in lv]
    steps=[round(b-a,1) for a,b in zip(vals,vals[1:])]
    print(f'\n t0={ch[0][1]:9.4f} span={(ch[-1][0]-ch[0][0])/FPS:5.3f}s ticks={len(ch):2d}')
    print(f'   levels(HP/tick x n): {seq}')
    print(f'   level steps: {steps}')
    desc=[s for s in steps if s<0]
    if len(desc)>=2:
        nstair+=1
        print(f'   >>> MULTI-STEP DESCENT: {desc}  ratios to smallest: '
              f'{[round(abs(s)/min(abs(x) for x in desc),2) for s in desc]}')
print(f'\nchains with a multi-step descent: {nstair}')
