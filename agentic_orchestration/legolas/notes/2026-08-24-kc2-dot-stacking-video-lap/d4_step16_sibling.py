"""STEP 16 — run the whole instrument stack on the SIBLING (eor-test-1, 2498.37 s)."""
import csv, collections, statistics
FPS=60.0
rows=list(csv.DictReader(open('d4_sibling_hp_trace.csv')))
val=[(int(r['frame']), float(r['t_s']), int(r['hp_cur']), int(r['hp_max'])) for r in rows if r['hp_cur']]
print(f'frames total {len(rows)}  read {len(val)} ({100*len(val)/len(rows):.2f}%)')
hm=collections.Counter(v[3] for v in val)
print('hp_max values:', hm.most_common(6))
HPMAX=hm.most_common(1)[0][0]
v=[x for x in val if x[3]==HPMAX]
print(f'frames at modal hp_max={HPMAX}: {len(v)}   t {v[0][1]:.1f} -> {v[-1][1]:.1f}')
fr={x[0]:(x[1],x[2]) for x in v}
ks=sorted(fr)
seq=[]
for i in range(1,len(ks)):
    if ks[i]==ks[i-1]+1:
        seq.append((ks[i], fr[ks[i]][0], fr[ks[i-1]][1], fr[ks[i]][1], fr[ks[i]][1]-fr[ks[i-1]][1]))
print(f'adjacent pairs: {len(seq)}')

# (A) quiet-window census
def census(leech_free):
    wins=[];cur=[];prev=None
    for f,t,h0,h1,d in seq:
        ok = d>-4 and h0<HPMAX and (not leech_free or d<=3) and (prev is None or f==prev+1)
        if ok: cur.append((f,t))
        else:
            if cur: wins.append(cur); 
            cur=[(f,t)] if (d>-4 and h0<HPMAX and (not leech_free or d<=3)) else []
        prev=f
    if cur: wins.append(cur)
    return [(w[0][1],(w[-1][0]-w[0][0]+1)/FPS) for w in wins]
for lf in (False,True):
    w=census(lf); lg=max((x[1] for x in w), default=0)
    print(f'\nhit-free, unclipped, leech_free={lf}: longest window = {lg:.3f} s')
    for T in (1.0,2.0,3.0,5.0,8.0):
        print(f'    >= {T:4.1f}s : {sum(1 for x in w if x[1]>=T)}')

# (B) tick chains + staircases
ev=[(f,t,-d) for f,t,h0,h1,d in seq if d<0]
chains=[];cur=[ev[0]]
for a,b in zip(ev,ev[1:]):
    if 5<=(b[0]-a[0])<=7: cur.append(b)
    else:
        if len(cur)>=6: chains.append(cur)
        cur=[b]
if len(cur)>=6: chains.append(cur)
print(f'\n100ms-cadence chains (>=6 ticks): {len(chains)}   longest {max((len(c) for c in chains),default=0)} ticks')
g=collections.Counter()
for a,b in zip(ev,ev[1:]):
    if 1<=b[0]-a[0]<=14 and a[2]<=40 and b[2]<=40: g[b[0]-a[0]]+=1
tot=sum(g.values())
print('inter-DoT-scale-event gap (sibling):', {k:g[k] for k in sorted(g)})
if tot: print(f'   modal gap {max(g,key=g.get)} frames = {max(g,key=g.get)/FPS*1000:.1f} ms  ({100*g[max(g,key=g.get)]/tot:.1f}% of {tot})')
def levels(ch,MIN=3,TOL=0.12):
    out=[];i=0;n=len(ch)
    while i<n:
        j=i+1
        while j<n:
            s=[e[2] for e in ch[i:j+1]]; m=statistics.median(s)
            if max(abs(x-m) for x in s)<=TOL*m: j+=1
            else: break
        if j-i>=MIN:
            s=[e[2] for e in ch[i:j]]; out.append((ch[i][1],j-i,statistics.median(s))); i=j
        else: i+=1
    return out
nst=0
for ch in chains:
    lv=levels(ch)
    if len(lv)<2: continue
    vals=[l[2] for l in lv]; steps=[round(b-a,1) for a,b in zip(vals,vals[1:])]
    desc=[s for s in steps if s<0]
    print(f'  t0={ch[0][1]:9.3f} ticks={len(ch):2d} levels={[f"{l[2]:.0f}x{l[1]}" for l in lv]} steps={steps}')
    if len(desc)>=2: nst+=1; print(f'     >>> MULTI-STEP DESCENT {desc}')
print(f'\nsibling chains with multi-step descent: {nst}')
