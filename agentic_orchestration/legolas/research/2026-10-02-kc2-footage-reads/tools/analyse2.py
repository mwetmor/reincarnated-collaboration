import json, collections
exec(open('analyse.py').read().split("out={}")[0])
raw=json.load(open('lineup_raw.json'))
def wave_recs(w):
    s=set()
    for sp,alts in P[str(w)].items():
        for a in alts: s|=set(a['recs']+a['crecs'])
    return s
FPALL=collections.defaultdict(list)
for rec,L,w,e in fp: FPALL[w].append((e,rec,L))
res={}
for w in range(151,161):
    WR=wave_recs(w)
    rows=[]
    for r in raw[str(w)]:
        mx=r['max']
        cands=[]
        for d in (0,1,-1):
            cands+= [(rec,L) for rec,L in FP.get((w,mx+d),[])]
        leg=[(rec,L) for rec,L in cands if rec in WR]
        summ=[(rec,L) for rec,L in cands if rec in SUMMON and any(o in WR for o in SUMMON[rec])]
        near=[]
        if not cands:
            near=sorted([(abs(e-mx)/mx,e,rec,L) for e,rec,L in FPALL[w] if abs(e-mx)/mx<0.004 and (rec in WR or rec in SUMMON)])[:3]
        rows.append(dict(max=mx,n=r['n'],simul=r['simul'],first=r['first'],last=r['last'],ncand=len(cands),
             legal=[(rec.split('/')[-1],L,NAME.get(rec,'?'),legal(w,rec)) for rec,L in leg],
             summon=[(rec.split('/')[-1],L,NAME.get(rec,'?'),[o.split('/')[-1] for o in SUMMON[rec] if o in WR]) for rec,L in summ],
             near=[(round(x*100,3),e,rec.split('/')[-1],L) for x,e,rec,L in near]))
    res[w]=rows
json.dump(res,open('lineup_matched.json','w'),indent=1)
for w,rows in res.items():
    print('== wave',w)
    for r in rows:
        if r['n']<3: continue
        print(f"  {r['max']:>9,} n={r['n']:3d} sim={r['simul']} {r['first']:.1f}-{r['last']:.1f} ncand={r['ncand']}",
              'LEGAL',r['legal'][:5], 'SUMM',r['summon'][:3], 'NEAR' if r['near'] else '', r['near'])
