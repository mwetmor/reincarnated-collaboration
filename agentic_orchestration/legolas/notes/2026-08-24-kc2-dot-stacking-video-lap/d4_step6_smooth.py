"""STEP 6 — hunt SUSTAINED SMOOTH DRAIN: runs of consecutive frames whose per-frame delta stays
inside a narrow negative band (no discrete spike). A monster's smallest post-mitigation direct hit
on this player is in the hundreds (Lap M chain), so a multi-frame run capped at |delta|<=THRESH
contains NO direct hit and its slope is continuous damage (DoT) net of regen."""
import collections, statistics
from d4_lib import load_trace, FPS
HPMAX=20005
frames=load_trace(); ks=sorted(frames)
pairs=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        pairs.append((ks[i], frames[ks[i]][0], frames[ks[i-1]][1], frames[ks[i]][1]))
for THRESH in (20, 30):
    runs=[];cur=[];prev=None
    for f,t,h0,h1 in pairs:
        d=h1-h0
        ok=(abs(d)<=THRESH) and (prev is None or f==prev+1) and h0<HPMAX
        if ok: cur.append((f,t,h0,h1,d))
        else:
            if len(cur)>=15: runs.append(cur)
            cur=[(f,t,h0,h1,d)] if (abs(d)<=THRESH and h0<HPMAX) else []
        prev=f
    if len(cur)>=15: runs.append(cur)
    dec=[]
    for r in runs:
        dur=(r[-1][0]-r[0][0]+1)/FPS
        slope=(r[-1][3]-r[0][2])/dur
        if slope < -100: dec.append((r[0][1],dur,r[0][2],r[-1][3],slope,r))
    dec.sort(key=lambda z:z[4])
    print(f'\n=== |delta|<={THRESH}, >=0.25s, net slope < -100 HP/s : {len(dec)} runs ===')
    print(f"{'t_start':>10} {'dur_s':>7} {'hp0':>6} {'hp1':>6} {'net HP/s':>10} {'drain(+regen~129)':>18}")
    for t0,dur,h0,h1,sl,r in dec[:14]:
        print(f'{t0:10.4f} {dur:7.4f} {h0:6d} {h1:6d} {sl:10.1f} {129.38-sl:18.1f}')
    if dec:
        best=dec[0]
        print(f'\nfine structure of steepest run @ t={best[0]:.4f} (dur {best[1]:.3f}s):')
        print('   deltas:', [x[4] for x in best[5]])
