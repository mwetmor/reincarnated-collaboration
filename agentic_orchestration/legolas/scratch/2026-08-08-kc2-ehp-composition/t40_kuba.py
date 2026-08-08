#!/usr/bin/env python3
"""Q4: is the Kubacabra phase chain wired, and to what?"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find
TAGS=json.load(open("t23_tags.json"))
print("== all nemesis_beast_01* records ==")
for p in sorted(find("nemesis_beast_01")):
    rec,prov,own = merged(p)
    print(f"  {p}  owners={own}  desc={rec.get('description')!r}->{TAGS.get(rec.get('description',''),'?')!r} "
          f"bio={(rec.get('characterAttributeEquations') or '').split('/')[-1]}  charLevel={rec.get('charLevel')!r}")
print("\n== who REFERENCES the p2/p3 records anywhere in the corpus? ==")
from t0_lib import archives
targets=[p for p in find("nemesis_beast_01") if "_p2" in p or "_p3" in p]
print("  targets:", targets)
refs={t:[] for t in targets}
for k,a in archives():
    for r in a.records:
        rec=a.read_record(r)
        for f,v in rec.items():
            vals = v if isinstance(v,list) else [v]
            for x in vals:
                if isinstance(x,str):
                    xl=x.lower()
                    for t in targets:
                        if xl==t: refs[t].append((k,r,f))
for t,l in refs.items():
    print(f"\n  {t}  -> {len(l)} references")
    for k,r,f in l[:20]: print(f"       [{k}] {r}  field={f}")
print("\n== Kubacabra P1 phase-transition wiring: skills of transition classes ==")
rec,prov,own = merged("records/creatures/enemies/nemesis/nemesis_beast_01_p1.dbr")
for i in range(1,40):
    s=rec.get(f"skillName{i}")
    if not s: continue
    sr,sp,so=merged(s); cl=sr.get("Class")
    if cl and ("Spawn" in cl or "Death" in cl or "Life" in cl or "Transform" in cl):
        print(f"   skill{i} {cl}  {s}")
        for kk in ("spawnObjects","spawnObjects2","petLimit","petBurstSpawn","spawnObjectsTimeToLive"):
            if kk in sr: print(f"        {kk} = {sr[kk]!r}")
for kk in ("lowHealthTriggerLevel","lowHealthResetLevel","deathObject","transformObject"):
    if kk in rec: print(f"   [P1 field] {kk} = {rec[kk]!r} [{prov[kk]}]")
