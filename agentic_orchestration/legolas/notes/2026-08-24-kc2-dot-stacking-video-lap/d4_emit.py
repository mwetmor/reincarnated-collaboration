"""Emit the lap's measured artifacts as CSV (primary video, eor-test-2)."""
import statistics, csv
from d4_lib import load_trace, FPS
frames=load_trace(); ks=sorted(frames)
seq=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        seq.append((ks[i], frames[ks[i]][0], frames[ks[i-1]][1], frames[ks[i]][1],
                    frames[ks[i]][1]-frames[ks[i-1]][1]))
byf={s[0]:s for s in seq}
ev=[(f,t,-d) for f,t,h0,h1,d in seq if d<0]
chains=[];cur=[ev[0]]
for a,b in zip(ev,ev[1:]):
    if 5<=(b[0]-a[0])<=7: cur.append(b)
    else:
        if len(cur)>=4: chains.append(cur)
        cur=[b]
if len(cur)>=4: chains.append(cur)
with open('d4_tick_chains.csv','w',newline='') as fh:
    w=csv.writer(fh)
    w.writerow(['chain_id','tick_idx','t_s','frame','gap_frames','magnitude_hp','implied_rate_hp_per_s','basis'])
    for ci,ch in enumerate(chains):
        for i,(f,t,m) in enumerate(ch):
            gap = '' if i==0 else f-ch[i-1][0]
            w.writerow([ci,i,f'{t:.4f}',f,gap,m,f'{m*10:.1f}',
                        'MEASURED - Lap K I-1 exact printed integer HP, 60fps, adjacent-frame delta'])
print(f'wrote d4_tick_chains.csv : {len(chains)} chains, {sum(len(c) for c in chains)} ticks')
# inter-tick gap histogram
import collections
g=collections.Counter()
for ch in chains:
    for a,b in zip(ch,ch[1:]): g[b[0]-a[0]]+=1
with open('d4_tick_period.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['gap_frames','gap_ms','count'])
    for k in sorted(g): w.writerow([k,f'{k/FPS*1000:.2f}',g[k]])
tot=sum(g.values()); wm=sum(k*v for k,v in g.items())/tot
print(f'wrote d4_tick_period.csv : n={tot}  mean gap {wm:.3f} fr = {wm/FPS*1000:.2f} ms  modal {max(g,key=g.get)} fr')
