import json, glob, collections
R=json.load(open('/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-10-02-crucible-enemy-roster-packet/roster.json'))
NAME={}
for t in R['types']:
    for m in t['members_detail']: NAME[m['record']]=m['display_name']
SUMMON={}
for s in R['summoned_bodies']:
    NAME.setdefault(s['pet_record'],s['display_name']); SUMMON[s['pet_record']]=[o['owner'] for o in s.get('owners',[])]
P=json.load(open('pools.json'))
for w in P:
    for sp in P[w]:
        for a in P[w][sp]:
            for r,n in zip(a['recs']+a['crecs'],a['names']+a['cnames']): NAME.setdefault(r,n)
fp=json.load(open('fp.json'))
FP=collections.defaultdict(list)
for rec,L,w,e in fp: FP[(w,e)].append((rec,L))
WB=[(151,682.6),(152,698.6),(153,714.9),(154,729.8),(155,744.0),(156,760.2),(157,780.4),(158,799.7),(159,812.7),(160,839.0),(161,864.8)]
def wave_of(t):
    for (w,a),(w2,b) in zip(WB,WB[1:]):
        if a<=t<b: return w
frames=[]
for f in sorted(glob.glob('cen/c*.json')):
    frames+=json.load(open(f))['frames']
frames.sort(key=lambda f:f['t'])
json.dump(frames,open('cen_all.json','w'))
def legal(w,rec):
    pts=[]
    for sp,alts in P[str(w)].items():
        for a in alts:
            if rec in a['recs'] or rec in a['crecs']: pts.append(sp)
    return sorted(set(pts))
out={}
for w in range(151,161):
    F=[f for f in frames if wave_of(f['t'])==w]
    cnt=collections.Counter(); simul=collections.Counter(); first={}; last={}
    for f in F:
        per=collections.Counter()
        for q in f['txt']:
            if not q['max'] or q['max']==20005: continue
            if q['green']>q['red']: continue
            per[q['max']]+=1; cnt[q['max']]+=1
            first.setdefault(q['max'],f['t']); last[q['max']]=f['t']
        for k,v in per.items(): simul[k]=max(simul[k],v)
    rows=[]
    for mx,n in cnt.most_common():
        cands=FP.get((w,mx),[]) or FP.get((w,mx+1),[]) or FP.get((w,mx-1),[])
        rows.append(dict(max=mx,n=n,simul=simul[mx],first=first[mx],last=last[mx],
            cands=[(r.split('/')[-1],L,NAME.get(r,'?'),legal(w,r),'S' if r in SUMMON else '') for r,L in cands]))
    out[w]=rows
json.dump(out,open('lineup_raw.json','w'),indent=1)
for w,rows in out.items():
    print('== wave',w,'frames',len([f for f in frames if wave_of(f['t'])==w]))
    for r in rows:
        if r['n']<2 and not r['cands']: continue
        print(f"  {r['max']:>9,} n={r['n']:4d} sim={r['simul']} {r['first']:.1f}-{r['last']:.1f}", r['cands'][:6])
