"""STEP 10 — THE RE-APPLICATION TEST (the discriminating experiment this footage CAN run).

Most monster DoT riders in this corpus ride on ATTACKS (weapon/skill), so every direct hit that
lands is also a DoT APPLICATION EVENT. Therefore:
   during a flat DoT plateau, count the direct hits that land.
   (a) FULL STACKING  predicts the plateau RISES with each application.
   (b) REFRESH-ONLY   predicts the plateau stays FLAT however many land.
This needs no knowledge of N in advance -- the hits count themselves."""
import statistics, csv
from d4_lib import load_trace, FPS
frames=load_trace(); ks=sorted(frames)
seq=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        h0=frames[ks[i-1]][1]; h1=frames[ks[i]][1]
        seq.append((ks[i], frames[ks[i]][0], h1-h0))
byf={s[0]:s for s in seq}
plats=list(csv.DictReader(open('d4_plateaus.csv')))
print(f"{'plateau t0':>11} {'ticks':>5} {'median':>7} {'span_s':>6} {'DIRECT HITS in span':>20} {'hit magnitudes':>14}")
for p in plats:
    t0=float(p['t_start_s']); span=float(p['span_s']); n=int(p['n_ticks']); med=float(p['median_mag'])
    f0=round(t0*FPS); f1=f0+round(span*FPS)
    hits=[]
    for f in range(f0,f1+1):
        s=byf.get(f)
        if s and s[2] < -(med*3):     # >=3x the plateau tick = unambiguously a direct hit
            hits.append(-s[2])
    print(f'{t0:11.4f} {n:5d} {med:7.1f} {span:6.3f} {len(hits):20d}  {sorted(hits,reverse=True)[:6]}')
