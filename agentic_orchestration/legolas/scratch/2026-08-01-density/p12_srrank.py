#!/usr/bin/env python3
"""P12 - rank every EndlessDungeonGenerator ruleset by floor monster total. READ-ONLY."""
import sys, pathlib, collections, re, json
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
arcs=[("gdx2",ArzArchive(ROOT/"gdx2/database/GDX2.arz")),("gdx3",ArzArchive(ROOT/"gdx3/database/GDX3.arz"))]
rows=[]
for k,a in arcs:
    for r in sorted(a.records):
        rec=a.read_record(r)
        if str(rec.get('Class'))!='EndlessDungeonGenerator': continue
        def n(f,d=0):
            try: return float(rec.get(f,d))
            except: return d
        rows.append(dict(arc=k,path=r,desc=str(rec.get('FileDescription') or ''),
            proxies=n('proxies'),heroProxies=n('heroProxies'),bossProxies=n('bossProxies'),
            trapProxies=n('trapProxies'),floors=n('floors'),
            championChance=n('championChance'),heroChance=n('heroChance'),commonChance=n('commonChance'),
            maxShrines=n('maxShrines'),
            fN=str(rec.get('floorTotalNormal') or ''),fE=str(rec.get('floorTotalElite') or ''),
            fU=str(rec.get('floorTotalUltimate') or ''),
            nfloorList=len(rec.get('floorList') or []),nspecial=len(rec.get('specialFloors') or []),
            nboss=len(rec.get('bossFloorList') or []),
            shrineW=str(rec.get('shrineProxyWeights') or ''),nemW=str(rec.get('nemesisProxyWeights') or '')))
print(f"EndlessDungeonGenerator rulesets: {len(rows)}")
# evaluate floorTotal equations: commonProxies = proxies (the 'proxies' field IS commonProxies count?)
def ev(eq,common,hero):
    try: return eval(eq,{"__builtins__":{}},{"commonProxies":common,"heroProxies":hero})
    except Exception as e: return None
print(f"\n{'arc':5s} {'prox':>5} {'hero':>5} {'boss':>5} {'flr':>4} {'chChn':>6} {'N':>7} {'E':>7} {'U':>7}  path :: desc")
out=[]
for r in sorted(rows,key=lambda x:-(ev(x['fU'],x['proxies'],x['heroProxies']) or 0)):
    N=ev(r['fN'],r['proxies'],r['heroProxies']); E=ev(r['fE'],r['proxies'],r['heroProxies']); U=ev(r['fU'],r['proxies'],r['heroProxies'])
    r['evalN'],r['evalE'],r['evalU']=N,E,U
    out.append(r)
    print(f"{r['arc']:5s} {r['proxies']:5.0f} {r['heroProxies']:5.0f} {r['bossProxies']:5.0f} {r['floors']:4.0f} "
          f"{r['championChance']:6.0f} {N if N is None else round(N,1):>7} {E if E is None else round(E,1):>7} {U if U is None else round(U,1):>7}  "
          f"{r['path'].split('/')[-1]} :: {r['desc'][:38]}")
print("\n### distinct floorTotal equation forms")
for f in ('fN','fE','fU'):
    print(f"  {f}:", dict(collections.Counter(r[f] for r in rows)))
json.dump(out,open("sr_rulesets.json","w"),indent=1)
print("\n[wrote sr_rulesets.json]")
