"""STEP 11 — (i) pin the tick period from plateau spans; (ii) BEFORE/AFTER-HIT test."""
import statistics, csv
from d4_lib import load_trace, FPS
frames=load_trace(); ks=sorted(frames)
seq=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        seq.append((ks[i], frames[ks[i]][0], frames[ks[i]][1]-frames[ks[i-1]][1]))
byf={s[0]:s for s in seq}

print('=== (i) TICK PERIOD from plateau spans (span / (n_ticks-1)) ===')
per=[]
for p in csv.DictReader(open('d4_plateaus.csv')):
    n=int(p['n_ticks']); span=float(p['span_s'])
    if n>=6:
        v=span/(n-1); per.append((v,n,float(p['t_start_s'])))
for v,n,t in sorted(per): print(f'   t={t:9.4f} n={n:2d}  period={v*1000:7.2f} ms')
w=sum(v*(n-1) for v,n,_ in per)/sum(n-1 for _,n,_ in per)
print(f'   tick-weighted mean period = {w*1000:.2f} ms   ({1/w:.3f} Hz)')

print('\n=== (ii) BEFORE/AFTER-HIT test ===')
ev=[(f,t,-d) for f,t,d in seq if d<0]
chains=[];cur=[ev[0]]
for a,b in zip(ev,ev[1:]):
    if 5<=(b[0]-a[0])<=7: cur.append(b)
    else:
        if len(cur)>=4: chains.append(cur)
        cur=[b]
if len(cur)>=4: chains.append(cur)
med=lambda c: statistics.median([e[2] for e in c])
pairs=0
print(f'   cadence chains (>=4): {len(chains)}')
for a,b in zip(chains,chains[1:]):
    gap_f = b[0][0]-a[-1][0]
    if gap_f > 90: continue                      # <=1.5 s apart
    hits=[-byf[f][2] for f in range(a[-1][0]+1,b[0][0]) if f in byf and byf[f][2] < -max(3*med(a),60)]
    if not hits: continue
    pairs+=1
    print(f'   t={a[-1][1]:9.4f}->{b[0][1]:9.4f} gap={gap_f/FPS:5.3f}s  DoT rate {med(a)*10:7.1f} -> {med(b)*10:7.1f} HP/s'
          f'  ({len(hits)} hit(s), max {max(hits)})')
print(f'   usable before/after pairs: {pairs}')
