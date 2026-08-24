"""STEP 9 — PLATEAU CENSUS at all magnitudes. A PLATEAU is >=6 consecutive 100ms-cadence damage
events whose magnitudes stay within +/-12% of their median. Direct-hit chains cannot hold a
plateau (variable damage, variable cadence); a DoT stack can. The plateau VALUE x 10 Hz is the
instantaneous total DoT rate, which is then tested against the refresh-only ceiling."""
import statistics, csv
from d4_lib import load_trace, FPS
frames=load_trace(); ks=sorted(frames)
ev=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        h0=frames[ks[i-1]][1]; h1=frames[ks[i]][1]; d=h1-h0
        if d<0: ev.append((ks[i], frames[ks[i]][0], -d))
print(f'all negative events: {len(ev)}  max magnitude: {max(e[2] for e in ev)}')
# cadence chains at any magnitude
chains=[];cur=[ev[0]]
for a,b in zip(ev,ev[1:]):
    if 5<=(b[0]-a[0])<=7: cur.append(b)
    else:
        if len(cur)>=6: chains.append(cur)
        cur=[b]
if len(cur)>=6: chains.append(cur)
print(f'100ms-cadence chains >=6 events: {len(chains)}')
plats=[]
for ch in chains:
    # sliding maximal plateau inside the chain
    n=len(ch); i=0
    while i<n:
        j=i+1
        while j<n:
            seg=[e[2] for e in ch[i:j+1]]
            med=statistics.median(seg)
            if max(abs(x-med) for x in seg) <= 0.12*med: j+=1
            else: break
        seg=ch[i:j]
        if len(seg)>=6:
            m=[e[2] for e in seg]
            plats.append((seg[0][1], len(seg), statistics.median(m), min(m), max(m),
                          (seg[-1][0]-seg[0][0])/FPS))
            i=j
        else: i+=1
plats.sort(key=lambda p:-p[2])
print(f'\nPLATEAUS (>=6 ticks, within +/-12% of median): {len(plats)}')
print(f"{'t_start':>10} {'ticks':>6} {'median':>7} {'min':>5} {'max':>5} {'span_s':>7} {'implied HP/s':>13}")
for p in plats[:25]:
    print(f'{p[0]:10.4f} {p[1]:6d} {p[2]:7.1f} {p[3]:5d} {p[4]:5d} {p[5]:7.3f} {p[2]*10:13.1f}')
with open('d4_plateaus.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['t_start_s','n_ticks','median_mag','min_mag','max_mag','span_s','implied_dot_hp_per_s'])
    for p in plats: w.writerow([f'{p[0]:.4f}',p[1],p[2],p[3],p[4],f'{p[5]:.4f}',f'{p[2]*10:.1f}'])
print(f'\nMAX plateau rate: {plats[0][2]*10:.1f} HP/s   (refresh-only ceiling 679.13 conservative / 1605.09 permissive)')
