#!/usr/bin/env python3
"""C7 — how universal is armorbaseNN on monsters? Is offensiveTotalDamageModifier a system-wide scaler? READ-ONLY."""
import sys, pathlib, re
from collections import Counter
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
ab=[r for r in a.records if 'nonplayerskills/passive/armorbase' in r]
print("armorbase records:")
for r in sorted(ab):
    rec=a.read_record(r)
    v=rec.get('offensiveTotalDamageModifier')
    d=rec.get('FileDescription','')
    if isinstance(v,list): v=f"r1={v[0]} r16={v[15]} r50={v[49]} r91={v[90]}"
    print(f"  {r:70s} {d!r:52s} totalDmgMod {v}")
# how many monsters carry an armorbase skill at all
cnt=Counter(); tot=0; withab=0
for r in list(a.records):
    if a.record_type(r)!='Monster': continue
    rec=a.read_record(r)
    tot+=1
    skills=[rec.get(f'skillName{i}') for i in range(1,25)]
    hits=[s for s in skills if s and 'armorbase' in s]
    if hits: withab+=1; cnt[hits[0]]+=1
print(f"\nMonster records: {tot};  carrying an armorbase passive: {withab} ({100*withab/tot:.1f}%)")
for k,v in cnt.most_common(12): print(f"   {k:70s} {v}")
