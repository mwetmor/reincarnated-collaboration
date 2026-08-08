#!/usr/bin/env python3
"""D5 — who can spawn swampcrab_a00_summon, and which pools carry basilisk_h02. Edition-II. READ-ONLY."""
import sys, collections
sys.path.insert(0,".")
import lib2
E2 = lib2.E2

TARGET_BODY = "records/creatures/enemies/swampcrab_a00_summon.dbr"
print("=== 1. skills whose spawnObjects include the crabling body ===")
skills = []
for p in E2.idx:
    if not p.startswith("records/skills"): continue
    r,_ = E2.merged(p)
    if not r: continue
    for k,v in r.items():
        if "spawnObject" in k or "petObject" in k or k in ("spawnObjects",):
            vs = v if isinstance(v,list) else [v]
            if any(isinstance(x,str) and x.lower()==TARGET_BODY for x in vs):
                skills.append(p); print(f"   {p}  Class={r.get('Class')} petLimit={r.get('petLimit')} burst={r.get('petBurstSpawn')}")
                break

print("\n=== 2. creature records that reference any of those skills ===")
sk = set(s.lower() for s in skills)
owners = collections.defaultdict(list)
for p in E2.idx:
    if not p.startswith("records/creatures"): continue
    r,_ = E2.merged(p)
    if not r: continue
    for k,v in r.items():
        if not isinstance(v,str): continue
        if v.lower() in sk:
            owners[p].append((k, v))
for p, hits in sorted(owners.items()):
    r,_ = E2.merged(p)
    print(f"   {p}  cls={r.get('monsterClassification')} charLevel={r.get('charLevel')}  via {hits}")

print("\n=== 3. every proxy pool containing basilisk_h02 / basilisk_h03 / aetherialcorruption_h02 ===")
WANT = ["records/creatures/enemies/hero/basilisk_h02.dbr",
        "records/creatures/enemies/hero/basilisk_h03.dbr",
        "records/creatures/enemies/hero/aetherialcorruption_h02.dbr"]
for w in WANT:
    print(f"  -- {w}")
    for p in E2.idx:
        if "/proxies/" not in p: continue
        r,_ = E2.merged(p)
        if not r: continue
        for k,v in r.items():
            if isinstance(v,str) and v.lower()==w:
                # find the matching variance equation
                idx = k.replace("name","").replace("Champion","")
                lv = r.get(f"levelVarianceEquationChampion{idx}") or r.get(f"levelVarianceEquation{idx}") or r.get("levelVarianceEquation1")
                print(f"       {p}   [{k}]  lv={lv}")
