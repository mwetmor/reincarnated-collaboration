#!/usr/bin/env python3
"""P13 - area-prefix census, level-band gating, SR pool sanity-check, folklore-location measured numbers. READ-ONLY."""
import sys, pathlib, collections, re, json, statistics as st
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
CAMP=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
M={}
for k,p in CAMP:
    a=ArzArchive(p)
    for r in a.records: M[r]=(k,a)
def get(p):
    e=M.get(p); return e[1].read_record(p) if e else None
camp=json.load(open("campaign_rows.json"))

print("### area-prefix tokens inside boss&quest* record NAMES (base+gdx)")
tok=collections.Counter()
for r in M:
    if "/boss&quest" not in r: continue
    m=re.search(r"(?:proxy|questproxy)_(area[a-z])_", r)
    if m: tok[m.group(1)]+=1
    else: tok["<no area prefix>"]+=1
print(dict(tok.most_common()))

print("\n### FOLKLORE LOCATION LEDGER - measured ceilings from campaign_rows.json")
LOC={"Steps of Torment (Act2)":"stepsoftorment","Bastion of Chaos (Act4)":"bastionofchaos",
     "Port Valbury (Act4)":"portvalbury","Warden's/Burrwitch (Act1)":"warden",
     "Burrwitch token":"burrwitch","Wightmire (Act1)":"wightmire","Ancient Grove (GDX1)":"ancientgrove",
     "Malmouth (GDX1)":"malmouth","Cronley":"cronley","Fleshworks":"fleshwork",
     "Tomb of the Heretic":"heretic","Twin Falls (Act1)":"twinfalls","Dermapteran infest (Act3)":"dermapteran"}
for label,t in LOC.items():
    hits=[r for r in camp if t in r['path'].lower()]
    if not hits:
        print(f"  {label:30s} UNPROBED - 0 records match token '{t}' in the proxy tree"); continue
    best=max(hits,key=lambda x:(x['ceiling'] if x['cls']=='Proxy' else (x['ambush']['maxGroupSize'] if x['ambush'] else 0)))
    amb=[r for r in hits if r['cls']=='ProxyAmbush']
    bamb=max(amb,key=lambda x:x['ambush']['maxGroupSize']) if amb else None
    print(f"  {label:30s} n={len(hits):3d}  best Proxy ceiling={max((r['ceiling'] for r in hits if r['cls']=='Proxy'),default=0):.0f}"
          f"  best Ambush maxGroup={bamb['ambush']['maxGroupSize'] if bamb else 0:.0f}"
          f"  ({(bamb or best)['path'].split('/')[-1]})")

print("\n### LEVEL-BAND GATING: do campaign pools carry absolute level fields, or only averagePlayerLevel-relative?")
lv=collections.Counter(); mplvals=collections.Counter()
npool=0
for r in M:
    if not r.startswith("records/proxies/"): continue
    rec=get(r)
    if 'spawnMin' not in rec: continue
    npool+=1
    for i in range(1,13):
        e=rec.get(f'levelVarianceEquation{i}')
        if e: lv[str(e).split('/')[-1].replace('.dbr','')]+=1
        v=rec.get(f'minPlayerLevel{i}')
        if v is not None: mplvals[int(float(v))]+=1
print(f" pools scanned={npool}")
print(" levelVarianceEquation targets:",dict(lv.most_common(12)))
print(" minPlayerLevel<i> value histogram:",dict(sorted(mplvals.items())))
print(" -> ALL variance equations resolve against averagePlayerLevel (see p3 dump): monsters scale to the player.")

print("\n### SR common-pool spawn sanity check (does commonProxy avg ~3.5 monsters?)")
g2=ArzArchive(ROOT/"gdx2/database/GDX2.arz")
sm=[];hm=[]
for r in sorted(g2.records):
    if "endlessdungeon/proxies/poolsbasic" in r:
        rec=g2.read_record(r)
        if rec.get('spawnMin') is not None:
            sm.append((float(rec['spawnMin'])+float(rec['spawnMax']))/2)
    if "endlessdungeon/proxies/poolshero" in r:
        rec=g2.read_record(r)
        if rec.get('spawnMin') is not None:
            hm.append((float(rec['spawnMin'])+float(rec['spawnMax']))/2)
print(f"  SR common pools n={len(sm)} mean_avg_spawn={sum(sm)/len(sm):.2f} median={st.median(sm):.2f} min={min(sm)} max={max(sm)}")
if hm: print(f"  SR hero   pools n={len(hm)} mean_avg_spawn={sum(hm)/len(hm):.2f} median={st.median(hm):.2f} min={min(hm)} max={max(hm)}")
print("\n### SR difficultyscaling records")
for r in sorted(g2.records):
    if "endlessdungeon/difficultyscaling" in r:
        rec=g2.read_record(r)
        keys=[k for k in rec if 'spawn' in k.lower() or 'proxy' in k.lower() or 'champion' in k.lower()]
        print(f"   {r}  ({len(rec)} fields)  density-relevant keys: {keys}")
