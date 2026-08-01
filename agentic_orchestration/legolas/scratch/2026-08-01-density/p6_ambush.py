#!/usr/bin/env python3
"""P6 - full dumps of the top-density ProxyAmbush records + their pools. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
arcs=[("base",ArzArchive(ROOT/"database/database.arz")),("gdx1",ArzArchive(ROOT/"gdx1/database/GDX1.arz")),
      ("gdx2",ArzArchive(ROOT/"gdx2/database/GDX2.arz")),("gdx3",ArzArchive(ROOT/"gdx3/database/GDX3.arz"))]
M={}
for k,a in arcs:
    for r in a.records: M[r]=(k,a)
def get(p):
    e=M.get(p); return e[1].read_record(p) if e else None

TOP=["records/proxies/boss&quest/proxy_aread_bastionofchaos_gauntletendless.dbr",
     "records/proxies/boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr",
     "records/proxies/boss&quest/proxy_aread_bastionofchaos_traproomwave3.dbr",
     "records/proxies/boss&quest/questproxy_areac_dermapteraninfestation.dbr",
     "records/proxies/boss&quest/proxy_areab_stepsoftorment_floor5eventfiller.dbr"]
for t in TOP:
    rec=get(t)
    print("="*120); print(f"{t}   owner={M[t][0]}   Class={rec.get('Class')}")
    for k,v in sorted(rec.items()):
        if k in ('mesh','baseTexture','templateName','shadowBias','outlineThickness','physicsFriction',
                 'physicsMass','physicsRestitution','maxTransparency','allowTransparency','castsShadows',
                 'actorHeight','actorRadius','unloadedBoundingBoxExtents'): continue
        print(f"   {k} = {v}")
    for i in range(1,9):
        p=rec.get(f'pool{i}')
        if not p: continue
        pr=get(str(p))
        print(f"   --- POOL{i}: {p}")
        if pr is None: print("        (UNRESOLVED)"); continue
        print(f"        spawnMin={pr.get('spawnMin')} spawnMax={pr.get('spawnMax')} "
              f"championChance={pr.get('championChance')} championMin={pr.get('championMin')} championMax={pr.get('championMax')}")
        for j in range(1,13):
            n=pr.get(f'name{j}')
            if n: print(f"          common w={pr.get(f'weight{j}')} limit={pr.get(f'limit{j}')} "
                        f"minPL={pr.get(f'minPlayerLevel{j}')} lv={str(pr.get(f'levelVarianceEquation{j}','')).split('/')[-1]} :: {str(n).split('/')[-1]}")
        for j in range(1,13):
            n=pr.get(f'nameChampion{j}')
            if n: print(f"          CHAMP  w={pr.get(f'weightChampion{j}')} minPL={pr.get(f'minPlayerLevelChampion{j}')} :: {str(n).split('/')[-1]}")
    print()
