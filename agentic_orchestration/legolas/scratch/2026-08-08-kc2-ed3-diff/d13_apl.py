#!/usr/bin/env python3
"""D13 — solve averagePlayerLevel from the resolved w152 level structure. READ-ONLY."""
import sys; sys.path.insert(0,".")
import lib2
E2=lib2.E2
print("=== basilisk_t3 basic pool (w152 sp=3) ===")
r,ow=E2.merged("records/proxies/poolsbasicgdx1/basilisk_t3.dbr")
for k in sorted(r):
    if "name" in k.lower() or "level" in k.lower() or "spawn" in k.lower() or "champion" in k.lower():
        print(f"    {k:34s} = {r[k]}")
print("\n=== lv proxy intervals as functions of A; solve A from the resolved level sets ===")
LV={}
for p in sorted(E2.find("records/proxies/lv")):
    rr,_=E2.merged(p)
    LV[p.split('/')[-1][:-4]]=(rr["minVarianceEquationNormal"], rr["maxVarianceEquationNormal"])
def iv(name,A):
    mn,mx=LV[name]
    f=lambda e: eval(e.replace("averagePlayerLevel",f"({A})"),{"__builtins__":{}},{})
    return f(mn), f(mx)
import math
OBS=[("lv2_normal",{102,103}),("lv3_strong",{103,104}),("lv5_elitechampion",{106}),
     ("lv6_hero",{107,108}),("lv7_uber hero",{108})]
ok=[]
A=100.0
while A<108.0:
    good=True
    for nm,want in OBS:
        mn,mx=iv(nm,A)
        floors=set(range(math.floor(mn), math.floor(mx)+1))
        if not want <= floors: good=False; break
    if good: ok.append(A)
    A=round(A+0.02,4)
if ok: print(f"   admissible averagePlayerLevel: [{min(ok):.2f}, {max(ok):.2f}]")
else: print("   NO admissible A")
for A in (100.0, 103.0, 103.4, 103.5):
    print(f"\n   A={A}:")
    for nm in ("lv1_weak","lv2_normal","lv3_strong","lv4_champion","lv5_elitechampion","lv6_hero","lv7_uber hero","lv8_boss","lv8_boss+"):
        mn,mx=iv(nm,A)
        print(f"      {nm:20s} [{mn:7.3f},{mx:7.3f}] -> floors {sorted(set(range(math.floor(mn),math.floor(mx)+1)))}")
