#!/usr/bin/env python3
"""Phase / variant records for the wave-160 roster — do any supply the F3 value? READ-ONLY."""
import sys, pathlib, math, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index, find

OUT = pathlib.Path(__file__).parent
F3 = 2295755.0
ULT, GLAD = 580.0, 324.0

print("=" * 112)
print("A — every nemesis record in the corpus (phase variants included)")
print("=" * 112)
nem = sorted(p for p in index() if "/nemesis/" in p and p.endswith(".dbr"))
for p in nem:
    rec, prov, own = merged(p)
    if rec.get("Class") != "Monster":
        continue
    bio = rec.get("characterAttributeEquations", "")
    print(f"   {p.split('/')[-1]:44s} cl={str(rec.get('charLevel')):22s} "
          f"bio={bio.split('/')[-1]:36s} mod={rec.get('characterLifeModifier')} "
          f"desc={rec.get('FileDescription')}")

print("\n" + "=" * 112)
print("B — Galakros / tomb-guardian / colossus family")
print("=" * 112)
for tok in ("galakros", "tombguardian", "korvaak"):
    for p in find(tok):
        if not p.endswith(".dbr"):
            continue
        rec, prov, own = merged(p)
        if rec.get("Class") != "Monster":
            continue
        print(f"   {p:70s} cl={str(rec.get('charLevel')):18s} "
              f"bio={str(rec.get('characterAttributeEquations','')).split('/')[-1]:38s} "
              f"cls={rec.get('monsterClassification')} desc={rec.get('FileDescription')}")

print("\n" + "=" * 112)
print("C — ALL bio records whose characterLife equation could yield F3 at M=10.04 and a plausible level")
print("=" * 112)
need = F3 / (1 + ULT / 100 + GLAD / 100)
print(f"   required base_life = {need:,.1f}")
bios = sorted(p for p in index() if "/bios/" in p and p.endswith(".dbr"))
print(f"   {len(bios)} bio records in corpus")
hits = []
for b in bios:
    rec, prov, own = merged(b)
    eq = rec.get("characterLife")
    if not isinstance(eq, str) or "charLevel" not in eq:
        continue
    e = eq.replace("^", "**")
    try:
        f = lambda c: eval(e, {}, {"charLevel": float(c)}) - need
        lo, hi = 1.0, 400.0
        if f(lo) * f(hi) > 0:
            continue
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(lo) * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
        cl = (lo + hi) / 2
    except Exception:
        continue
    if 95 <= cl <= 135:
        hits.append((cl, b, eq, own))
hits.sort()
print(f"\n   {len(hits)} bios reach the required base at charLevel in [95,135]:")
for cl, b, eq, own in hits:
    print(f"     cl={cl:7.2f}  {b.split('/')[-1]:46s} {eq:34s} [{own}]")
