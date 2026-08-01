#!/usr/bin/env python3
"""P5 - MASTER CENSUS. Campaign proxy->pool density + Crucible wave density. READ-ONLY.
Resolves each Class=Proxy record's pool1..poolN (weighted alternatives) to the pool records
carrying spawnMin/spawnMax/championChance/championMin/championMax."""
import sys, pathlib, collections, re, json, statistics as st
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
CAMP=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
SURV=[("sm_mod",ROOT/"mods/survivalmode/database/SurvivalMode.arz"),
      ("sm1",ROOT/"survivalmode1/database/SurvivalMode1.arz"),
      ("sm2",ROOT/"survivalmode2/database/SurvivalMode2.arz"),
      ("sm3",ROOT/"survivalmode3/database/SurvivalMode3.arz")]

def load(pairs):
    arcs={}; idx={}
    for k,p in pairs:
        a=ArzArchive(p); arcs[k]=a
        for r in a.records: idx.setdefault(r,[]).append(k)
    return arcs,idx

def num(v,d=0):
    try: return float(v)
    except: return d

class Res:
    """resolver across a stack of archives; later archive in list wins."""
    def __init__(self,pairs):
        self.arcs=[(k,ArzArchive(p)) for k,p in pairs]
        self.map={}
        for k,a in self.arcs:
            for r in a.records: self.map[r]=(k,a)   # later wins
    def get(self,path):
        e=self.map.get(path)
        return e[1].read_record(path) if e else None
    def owner(self,path):
        e=self.map.get(path); return e[0] if e else None

def pool_stats(rec):
    if rec is None: return None
    smin=num(rec.get('spawnMin')); smax=num(rec.get('spawnMax'))
    cch=num(rec.get('championChance')); cmin=num(rec.get('championMin')); cmax=num(rec.get('championMax'))
    ncommon=sum(1 for i in range(1,13) if rec.get(f'name{i}'))
    nchamp=sum(1 for i in range(1,13) if rec.get(f'nameChampion{i}'))
    nhero=sum(1 for i in range(1,13) if '/hero/' in str(rec.get(f'nameChampion{i}') or ''))
    # min player level gates
    mpl=[num(rec.get(f'minPlayerLevel{i}'),0) for i in range(1,13) if rec.get(f'name{i}')]
    mplc=[num(rec.get(f'minPlayerLevelChampion{i}'),0) for i in range(1,13) if rec.get(f'nameChampion{i}')]
    lv=[str(rec.get(f'levelVarianceEquation{i}') or '').split('/')[-1].replace('.dbr','')
        for i in range(1,13) if rec.get(f'name{i}')]
    return dict(spawnMin=smin,spawnMax=smax,championChance=cch,championMin=cmin,championMax=cmax,
                ncommon=ncommon,nchamp=nchamp,nhero=nhero,
                minPL=min(mpl) if mpl else 0, minPLchamp=min(mplc) if mplc else 0,
                lvbands=sorted(set(x for x in lv if x)))

def proxy_rows(res, path_filter):
    rows=[]
    for path,(ownk,arc) in sorted(res.map.items()):
        if not path_filter(path): continue
        rec=arc.read_record(path)
        cls=str(rec.get('Class'))
        if cls not in ('Proxy','ProxyAmbush'): continue
        pools=[]; wts=[]
        for i in range(1,9):
            p=rec.get(f'pool{i}')
            if p:
                pools.append(str(p)); wts.append(num(rec.get(f'weight{i}'),0))
        ps=[(p,pool_stats(res.get(p)),w) for p,w in zip(pools,wts)]
        ps=[(p,s,w) for p,s,w in ps if s]
        if not ps: continue
        wtot=sum(w for _,_,w in ps) or 1
        smax_max=max(s['spawnMax'] for _,s,_ in ps)
        smin_min=min(s['spawnMin'] for _,s,_ in ps)
        cmax_max=max(s['championMax'] for _,s,_ in ps)
        exp=sum(w*((s['spawnMin']+s['spawnMax'])/2) for _,s,w in ps)/wtot
        expch=sum(w*(s['championChance']/100.0)*((s['championMin']+s['championMax'])/2) for _,s,w in ps)/wtot
        ceiling=smax_max+cmax_max
        amb=dict(minGroupSize=num(rec.get('minGroupSize')),maxGroupSize=num(rec.get('maxGroupSize')),
                 spawnThreshold=num(rec.get('spawnThreshold')),
                 minSpawnTime=num(rec.get('minSpawnTime')),maxSpawnTime=num(rec.get('maxSpawnTime'))) if cls=='ProxyAmbush' else None
        rows.append(dict(path=path,owner=ownk,cls=cls,npools=len(ps),
                         spawnMin=smin_min,spawnMax=smax_max,champMax=cmax_max,ceiling=ceiling,
                         expected=exp,expChamp=expch, expTotal=exp+expch,
                         minPL=min(s['minPL'] for _,s,_ in ps),
                         lvbands=sorted(set(b for _,s,_ in ps for b in s['lvbands'])),
                         pools=[p for p,_,_ in ps], ambush=amb))
    return rows

# ---------- Q1: CAMPAIGN ----------
resC=Res(CAMP)
camp=proxy_rows(resC, lambda p: p.startswith("records/proxies/"))
print("="*130)
print(f"Q1 CAMPAIGN: resolvable Proxy/ProxyAmbush records with pools = {len(camp)}")
print("  by Class:", dict(collections.Counter(r['cls'] for r in camp)))
print("  by owning archive:", dict(collections.Counter(r['owner'] for r in camp)))
print("="*130)
print("\n--- TOP 25 by ceiling (spawnMax + championMax), Class=Proxy ---")
pr=[r for r in camp if r['cls']=='Proxy']
print(f"{'ceiling':>7} {'sMin':>4} {'sMax':>4} {'chMax':>5} {'E[tot]':>7} {'nP':>3} {'mPL':>4}  path")
for r in sorted(pr,key=lambda x:(-x['ceiling'],-x['expTotal']))[:25]:
    print(f"{r['ceiling']:7.0f} {r['spawnMin']:4.0f} {r['spawnMax']:4.0f} {r['champMax']:5.0f} {r['expTotal']:7.2f} {r['npools']:3d} {r['minPL']:4.0f}  {r['path'].replace('records/proxies/','')}")
print("\n--- TOP 25 by E[total spawn] (weighted expectation), Class=Proxy ---")
for r in sorted(pr,key=lambda x:-x['expTotal'])[:25]:
    print(f"{r['expTotal']:7.2f} (sMin{r['spawnMin']:.0f}/sMax{r['spawnMax']:.0f}/chMax{r['champMax']:.0f}) nP={r['npools']} mPL={r['minPL']:.0f}  {r['path'].replace('records/proxies/','')}")
print("\n--- ProxyAmbush TOP 20 by maxGroupSize then ceiling ---")
am=[r for r in camp if r['cls']=='ProxyAmbush']
print(f"{'maxGrp':>6} {'minGrp':>6} {'thresh':>6} {'sMax':>4} {'chMax':>5} {'spawnT':>12}  path")
for r in sorted(am,key=lambda x:(-x['ambush']['maxGroupSize'],-x['ceiling']))[:20]:
    a=r['ambush']
    print(f"{a['maxGroupSize']:6.0f} {a['minGroupSize']:6.0f} {a['spawnThreshold']:6.0f} {r['spawnMax']:4.0f} {r['champMax']:5.0f} {a['minSpawnTime']:5.1f}-{a['maxSpawnTime']:<6.1f}  {r['path'].replace('records/proxies/','')}")
json.dump(camp,open("campaign_rows.json","w"),indent=1)
print("\n[wrote campaign_rows.json]")
