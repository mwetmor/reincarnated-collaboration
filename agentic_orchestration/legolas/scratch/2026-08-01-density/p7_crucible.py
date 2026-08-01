#!/usr/bin/env python3
"""P7 - Crucible/SurvivalMode wave density census. READ-ONLY.
Wave = tierNN/proxy_wWW_p01..p06. Each spawn-point Proxy picks ONE of pool1..poolN by weight.
Wave count = sum over spawn points of chosen pool's spawn count (+ champions)."""
import sys, pathlib, collections, re, json
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
STACK=[("sm_mod",ROOT/"mods/survivalmode/database/SurvivalMode.arz"),
       ("sm1",ROOT/"survivalmode1/database/SurvivalMode1.arz"),
       ("sm2",ROOT/"survivalmode2/database/SurvivalMode2.arz"),
       ("sm3",ROOT/"survivalmode3/database/SurvivalMode3.arz")]
CAMP=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
M={}
for k,p in CAMP+STACK:      # survival overrides campaign; later survival wins
    a=ArzArchive(p)
    for r in a.records: M[r]=(k,a)
def get(p):
    e=M.get(p); return e[1].read_record(p) if e else None
def num(v,d=0.0):
    try: return float(v)
    except: return d

PAT=re.compile(r"^records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)([a-z]*)\.dbr$")
waves=collections.defaultdict(list)
unres=collections.Counter()
for path,(own,arc) in M.items():
    m=PAT.match(path)
    if not m: continue
    tier,w,pt=int(m.group(1)),int(m.group(2)),int(m.group(3))
    rec=arc.read_record(path)
    opts=[]
    for i in range(1,9):
        p=rec.get(f'pool{i}')
        if not p: continue
        pr=get(str(p))
        if pr is None: unres[str(p)]+=1; continue
        opts.append(dict(pool=str(p),w=num(rec.get(f'weight{i}'),0),
            smin=num(pr.get('spawnMin')),smax=num(pr.get('spawnMax')),
            cch=num(pr.get('championChance')),cmin=num(pr.get('championMin')),cmax=num(pr.get('championMax'))))
    if not opts: continue
    wt=sum(o['w'] for o in opts) or 1
    waves[(tier,w)].append(dict(pt=pt,path=path,own=own,opts=opts,
        pmin=min(o['smin'] for o in opts), pmax=max(o['smax']+o['cmax'] for o in opts),
        pexp=sum(o['w']*(((o['smin']+o['smax'])/2)+(o['cch']/100.0)*((o['cmin']+o['cmax'])/2)) for o in opts)/wt))
print(f"resolved wave spawn-point proxies: {sum(len(v) for v in waves.values())}  distinct (tier,wave)={len(waves)}")
print(f"unresolved pool refs: {sum(unres.values())} distinct={len(unres)}")
for p,c in unres.most_common(10): print("   UNRESOLVED",p,c)

rows=[]
for (tier,w),pts in waves.items():
    rows.append(dict(tier=tier,wave=w,npts=len(pts),
        wmin=sum(p['pmin'] for p in pts), wmax=sum(p['pmax'] for p in pts),
        wexp=sum(p['pexp'] for p in pts),
        owners=sorted(set(p['own'] for p in pts)),
        pts=sorted((p['pt'],p['path'],p['pmin'],p['pmax'],round(p['pexp'],2)) for p in pts)))
print("\n=== TOP 20 WAVES by ceiling (sum of per-point max incl. champions) ===")
print(f"{'tier':>4} {'wave':>4} {'pts':>3} {'min':>5} {'MAX':>6} {'E[n]':>7}  archives")
for r in sorted(rows,key=lambda x:(-x['wmax'],-x['wexp']))[:20]:
    print(f"{r['tier']:4d} {r['wave']:4d} {r['npts']:3d} {r['wmin']:5.0f} {r['wmax']:6.0f} {r['wexp']:7.2f}  {','.join(r['owners'])}")
print("\n=== TOP 20 WAVES by E[monster count] ===")
for r in sorted(rows,key=lambda x:-x['wexp'])[:20]:
    print(f"{r['tier']:4d} {r['wave']:4d} {r['npts']:3d} min{r['wmin']:5.0f} MAX{r['wmax']:6.0f} E={r['wexp']:7.2f}  {','.join(r['owners'])}")
print("\n=== PER-TIER aggregate (10 waves each) ===")
print(f"{'tier':>4} {'waves':>5} {'sum_min':>8} {'sum_MAX':>8} {'sum_E':>9} {'maxwave_MAX':>11}")
for t in sorted(set(r['tier'] for r in rows)):
    tr=[r for r in rows if r['tier']==t]
    print(f"{t:4d} {len(tr):5d} {sum(r['wmin'] for r in tr):8.0f} {sum(r['wmax'] for r in tr):8.0f} "
          f"{sum(r['wexp'] for r in tr):9.2f} {max(r['wmax'] for r in tr):11.0f}")
json.dump(rows,open("crucible_rows.json","w"),indent=1)
print("\n[wrote crucible_rows.json]")
print("\n=== DENSEST SINGLE WAVE - full breakdown ===")
top=max(rows,key=lambda x:(x['wmax'],x['wexp']))
print(f"tier{top['tier']:02d} wave{top['wave']:02d}  points={top['npts']} min={top['wmin']:.0f} MAX={top['wmax']:.0f} E={top['wexp']:.2f}")
for pt,path,pmin,pmax,pexp in top['pts']:
    print(f"   p{pt:02d} min={pmin:.0f} max={pmax:.0f} E={pexp}  {path}")
    rec=get(path)
    for i in range(1,9):
        p=rec.get(f'pool{i}')
        if not p: continue
        pr=get(str(p))
        print(f"        w={rec.get(f'weight{i}')} -> {p}  spawn {pr.get('spawnMin')}-{pr.get('spawnMax')} "
              f"champ {pr.get('championChance')}% {pr.get('championMin')}-{pr.get('championMax')}")
