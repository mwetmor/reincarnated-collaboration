"""STEP 5 — WINDOW CENSUS. How much quiet does this footage contain, at every threshold that
matters? DoT durations in the wave-150..160 population are 1.0-8.0 s (Lap I pm4i_dot_riders.csv),
so a decay-tail instrument needs a hit-free, leech-free, regen-unclipped window >= the duration."""
import csv, collections
from d4_lib import load_trace, LAPI, FPS
HPMAX=20005
frames=load_trace(); ks=sorted(frames)
pairs=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        pairs.append((ks[i], frames[ks[i]][0], frames[ks[i-1]][1], frames[ks[i]][1]))

def census(hit_thresh=-4, need_unclipped=True, leech_free=False):
    wins=[];cur=[];prev=None
    for f,t,h0,h1 in pairs:
        d=h1-h0
        ok=(d>hit_thresh)
        if need_unclipped: ok = ok and h0<HPMAX
        if leech_free: ok = ok and d<=3
        ok = ok and (prev is None or f==prev+1)
        if ok: cur.append((f,t,h0,h1))
        else:
            if cur: wins.append(cur)
            cur=[]
            # restart check
            ok2=(d>hit_thresh) and (not need_unclipped or h0<HPMAX) and (not leech_free or d<=3)
            if ok2: cur=[(f,t,h0,h1)]
        prev=f
    if cur: wins.append(cur)
    return [ (w[0][1],(w[-1][0]-w[0][0]+1)/FPS) for w in wins ]

# DoT durations present
durs=[]
for r in csv.DictReader(open(LAPI)):
    if r['is_dot']=='True' and r['duration_min_s']:
        durs.append(float(r['duration_min_s']))
print(f'DoT rider durations (n={len(durs)}): min={min(durs)} max={max(durs)} distinct={sorted(set(durs))}')

for label,kw in [('hit-free, unclipped', dict()),
                 ('hit-free, unclipped, LEECH-FREE', dict(leech_free=True)),
                 ('hit-free (full-HP allowed)', dict(need_unclipped=False)),
                 ('hit-free, unclipped, LEECH-FREE (strict hit thresh -1)', dict(leech_free=True,hit_thresh=-1))]:
    w=census(**kw)
    print(f'\n--- {label} ---')
    for T in (0.5,1.0,2.0,3.0,5.0,8.0):
        sel=[x for x in w if x[1]>=T]
        longest=max((x[1] for x in w), default=0)
        print(f'   >= {T:4.1f}s : {len(sel):3d} windows   (longest anywhere = {longest:.3f}s)')
