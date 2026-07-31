#!/usr/bin/env python3
"""D1 - armorbase0N offensiveTotalDamageModifier across ALL tiers. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
ab=sorted(r for r in a.records if 'nonplayerskills/passive/armorbase' in r)
print("=== armorbase records: offensiveTotalDamageModifier by rank ===")
for r in ab:
    rec=a.read_record(r)
    v=rec.get('offensiveTotalDamageModifier')
    life=rec.get('characterLifeModifier')
    if isinstance(v,list):
        s=" ".join(f"r{k}={v[k-1]}" for k in (1,12,13,14,15,16,18,19,20) if k-1<len(v))
    else: s=str(v)
    lf = life[0] if isinstance(life,list) else life
    print(f"{r.split('/')[-1]:22s} lifeMod={lf}  totalDmgMod: {s}")
print()
print("=== damage_totaladjuster ===")
for r in sorted(x for x in a.records if 'totaladjuster' in x):
    rec=a.read_record(r)
    for k in ('offensiveTotalDamageModifier','offensivePhysicalModifier','skillLevelEquation','FileDescription'):
        if k in rec: print(f"  {r.split('/')[-1]} {k} = {rec[k] if not isinstance(rec[k],list) else rec[k][:6]}")
