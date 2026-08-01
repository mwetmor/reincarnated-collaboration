#!/usr/bin/env python3
"""P15 - Q3 level bands: Crucible pool level equations + minPlayerLevel gating on top campaign entries. READ-ONLY."""
import sys, pathlib, collections, json
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
sm=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")
print("### Crucible poolsbasic level equations (do Crucible monsters scale to player?)")
lv=collections.Counter(); mpl=collections.Counter(); n=0
for r in sorted(sm.records):
    if "records/proxies/poolsbasic" not in r: continue
    rec=sm.read_record(r)
    if rec.get('spawnMin') is None: continue
    n+=1
    for i in range(1,13):
        e=rec.get(f'levelVarianceEquation{i}')
        if e: lv[str(e).split('/')[-1].replace('.dbr','')]+=1
        v=rec.get(f'minPlayerLevel{i}')
        if v is not None: mpl[int(float(v))]+=1
print(f" pools={n}"); print(" lvEq:",dict(lv.most_common(10))); print(" minPlayerLevel:",dict(sorted(mpl.items())) or "NONE")

print("\n### tier14 wave06 pools: level equations + rosters (the densest wave)")
for p in ["records/proxies/poolsbasic/chthoniandevourer_t2.dbr","records/proxies/poolsbasic/cultistchaos_t3.dbr",
          "records/proxies/poolsbasic/skeletonranged_t2.dbr"]:
    if p in sm.records:
        rec=sm.read_record(p)
        print(f"  {p}  spawn {rec.get('spawnMin')}-{rec.get('spawnMax')}")
        for i in range(1,13):
            nm=rec.get(f'name{i}')
            if nm: print(f"     w={rec.get(f'weight{i}')} lv={str(rec.get(f'levelVarianceEquation{i}','')).split('/')[-1]} minPL={rec.get(f'minPlayerLevel{i}')} :: {str(nm).split('/')[-1]}")

print("\n### Q3 BAND TABLE - top campaign entries, minPlayerLevel gate on roster + area")
camp=json.load(open("campaign_rows.json"))
def band(r):
    p=r['path']
    if '_areab_' in p: return 'Act2 (~L24-32)'
    if '_areac_' in p: return 'Act3 (~L32-40)'
    if '_aread_' in p: return 'Act4 (~L40-50)'
    if '_areae_' in p or 'gdx1' in r['owner']: return 'AoM/Act5-6 (~L50-75)'
    if '_areag_' in p or r['owner']=='gdx2': return 'FG/Act7 (~L65-90)'
    if '_areah_' in p or r['owner']=='gdx3': return 'FoA/Act8 (~L90+)'
    if 'area001' in p: return 'Act1-shared (scales; L1+)'
    return 'unclassified'
sel=sorted([r for r in camp if r['cls']=='Proxy'],key=lambda x:-x['ceiling'])[:12]
sel+=sorted([r for r in camp if r['cls']=='ProxyAmbush'],key=lambda x:-(x['ambush']['maxGroupSize']))[:12]
print(f"{'ceil/grp':>8} {'minPL':>5}  {'band':26s} path")
for r in sel:
    v=r['ceiling'] if r['cls']=='Proxy' else r['ambush']['maxGroupSize']
    print(f"{v:8.0f} {r['minPL']:5.0f}  {band(r):26s} {r['path'].replace('records/proxies/','')}")
