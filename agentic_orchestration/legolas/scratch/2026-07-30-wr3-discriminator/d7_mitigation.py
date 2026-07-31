#!/usr/bin/env python3
"""D7 - player mitigation from the equipped set: armor + resistances. READ-ONLY."""
import sys, pathlib, json
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[(p.name,ArzArchive(p)) for p in ARZS]
def get(n):
    for nm,a in ars:
        if n in a.records: return a.read_record(n)
    return None
G="/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/gear_named.json"
gear=json.load(open(G))
tot={}
print("per-item defensive contributions (base + prefix + suffix records):")
for it in gear:
    if it.get("group")!="equipment": continue
    print(f"  [{it['slot']}] {it['name']}")
    for role,part in it.get("parts",{}).items():
        if not part or not part.get("record"): continue
        rec=get(part["record"])
        if rec is None: continue
        for k,v in rec.items():
            if not k.startswith("defensive"): continue
            if isinstance(v,list): v=v[0]
            if not v: continue
            if k.endswith(("Chance","DurationMin","DurationMax","Modifier")) and "Resistance" not in k: pass
            tot[k]=tot.get(k,0.0)+float(v)
            print(f"        {role:11s} {k:44s} {v}")
print()
print("=== TOTALS across the equipped set ===")
for k in sorted(tot):
    print(f"  {k:48s} {tot[k]:.1f}")
print()
print("=== player base armor from malepc01 / class training ===")
for rn in ["records/creatures/pc/malepc01.dbr","records/skills/playerclass10/_classtraining_class10.dbr"]:
    rec=get(rn)
    if rec is None: continue
    for k,v in sorted(rec.items()):
        if not k.startswith("defensive"): continue
        vv=v[15] if isinstance(v,list) and len(v)>15 else (v[0] if isinstance(v,list) else v)
        if vv: print(f"  {rn.split('/')[-1]:32s} {k:44s} {vv}")
