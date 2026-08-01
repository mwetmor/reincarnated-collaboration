#!/usr/bin/env python3
"""E. Crucible t13/t14 wave06 pools + survival balancing adjustments. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCS=[("sm_mod","mods/survivalmode/database/SurvivalMode.arz"),("sm1","survivalmode1/database/SurvivalMode1.arz"),
      ("sm2","survivalmode2/database/SurvivalMode2.arz"),("sm3","survivalmode3/database/SurvivalMode3.arz")]
A={k:ArzArchive(ROOT/p) for k,p in ARCS}
def res(path):
    out=None
    for k,_ in ARCS:
        if path in A[k].records: out=(k,A[k].read_record(path))
    return out

for tier in (13,14):
    print("="*70); print(f"Crucible tier{tier:02d} wave06 spawn points")
    tot=[0,0]
    for pp in range(1,7):
        p=f"records/proxies/tier{tier:02d}waves/proxy_w06_p{pp:02d}a.dbr"
        r=res(p)
        if not r: continue
        k,rec=r
        pools=[(rec[f"pool{i}"],rec.get(f"weight{i}",0)) for i in range(1,7) if rec.get(f"pool{i}")]
        print(f"  p{pp:02d} [{k}] pools={len(pools)}")
        for pl,w in pools:
            pr=res(pl)
            if not pr: print("     MISSING",pl); continue
            _,po=pr
            print(f"     w={w:4} {pl.split('/')[-1]:44} sMin={po.get('spawnMin')} sMax={po.get('spawnMax')} chC={po.get('championChance')} chMin={po.get('championMin')} chMax={po.get('championMax')}")

print("\n"+"="*70); print("Survival balancing adjustments (Normal/Elite/Ultimate = Aspirant/Challenger/Gladiator)")
base=ArzArchive(ROOT/"database/database.arz")
for n,tag in [("01","Normal/Aspirant"),("02","Elite/Challenger"),("03","Ultimate/Gladiator")]:
    p=f"records/game/balancingadjustment_survivalmode_enemies{n}.dbr"
    got=None
    for k,_ in ARCS:
        if p in A[k].records: got=(k,A[k].read_record(p))
    if got is None and p in base.records: got=("BASE",base.read_record(p))
    print(f"\n-- {tag}  {p}  [{got[0] if got else 'NOT FOUND'}]")
    if got:
        for kk,vv in sorted(got[1].items()): print(f"   {kk} = {vv}")
