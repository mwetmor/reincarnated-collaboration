#!/usr/bin/env python3
"""D1 — crabling identity + level chain. Edition-II pin (fixture substrate). READ-ONLY."""
import sys, math
sys.path.insert(0, ".")
import lib2
E2, E3 = lib2.E2, lib2.E3

def ev(expr, L):
    s = str(expr).replace("^","**").replace("charLevel", f"({L})")
    return eval(s, {"__builtins__": {}}, {})

def show(p, ed=E2, fields=None):
    r, ow = ed.merged(p)
    if r is None:
        print(f"  [ABSENT] {p}"); return None
    print(f"  {p}   owners={ow}")
    keys = fields or ["description","monsterClassification","charLevel","characterAttributeEquations",
                      "levelVarianceEquation1","levelVarianceEquation","Class","petLimit"]
    for k in keys:
        if k in r: print(f"      {k:32s} = {r[k]}")
    return r

# --- 1. every record that looks like a crab summon body ---
print("=== crab-ish summon bodies in Edition-II ===")
cands = [p for p in E2.idx if "crab" in p and p.endswith(".dbr")]
print(f"  total 'crab' records: {len(cands)}")
summons = [p for p in cands if "summon" in p]
for p in sorted(summons):
    r,_ = E2.merged(p)
    print(f"   {p}\n       desc={r.get('description')} cls={r.get('monsterClassification')} charLevel={r.get('charLevel')} bio={r.get('characterAttributeEquations')}")
