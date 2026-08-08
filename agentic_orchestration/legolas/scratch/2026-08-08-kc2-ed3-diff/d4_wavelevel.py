#!/usr/bin/env python3
"""D4 — hunt the Crucible level term. Edition-II pin. READ-ONLY."""
import sys
sys.path.insert(0, ".")
import lib2
E2 = lib2.E2

print("=== survivalinfo.dbr ===")
for p in E2.find("survivalinfo"):
    r,_ = E2.merged(p)
    print(f"  {p}")
    for k in sorted(r): print(f"      {k:38s} = {str(r[k])[:160]}")

print("\n=== balancingadjustment_survivalmode_enemies03 : ALL scalar/array field NAMES ===")
p = "records/game/balancingadjustment_survivalmode_enemies03.dbr"
r,ow = E2.merged(p)
print(f"  owners={ow}   fields={len(r)}")
for k in sorted(r):
    v = r[k]
    if isinstance(v, list):
        print(f"      {k:38s} [array {len(v)}]  idx149..160 = {v[149:161]}")
    else:
        print(f"      {k:38s} = {v}")
