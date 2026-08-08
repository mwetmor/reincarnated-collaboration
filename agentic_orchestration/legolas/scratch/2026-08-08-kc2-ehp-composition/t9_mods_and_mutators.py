#!/usr/bin/env python3
"""H4 + verification: every remaining life-touching term. READ-ONLY."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index

OUT = pathlib.Path(__file__).parent

print("=" * 108)
print("A — VERIFY the survival wave modifier at wave 160 Gladiator (index 159)")
print("=" * 108)
for d, p in (("Aspirant", "records/game/balancingadjustment_survivalmode_enemies01.dbr"),
             ("Challenger", "records/game/balancingadjustment_survivalmode_enemies02.dbr"),
             ("Gladiator", "records/game/balancingadjustment_survivalmode_enemies03.dbr")):
    rec, prov, own = merged(p)
    for f in ("characterLife", "characterLifeModifier", "characterLifeMultModifier",
              "characterLifeRegenModifier", "defensivePercentCurrentLife"):
        v = rec.get(f)
        if isinstance(v, list):
            print(f"   {d:11s} {f:30s} len={len(v)}  i=149:{v[149]}  i=155:{v[155]}  "
                  f"i=158:{v[158]}  **i=159:{v[159]}**  i=160:{v[160]}  i=169:{v[169]}  i=199:{v[199]}")
        else:
            print(f"   {d:11s} {f:30s} = {v!r}")

print("\n" + "=" * 108)
print("B — per-ROSTER-RECORD own life modifiers (H3 residual)")
print("=" * 108)
chain = json.load(open(OUT / "t3_chain.json"))["chain"]
for p, e in sorted(chain.items()):
    rec, prov, own = merged(p)
    hits = {f: v for f, v in rec.items()
            if ("life" in f.lower() or "health" in f.lower())
            and isinstance(v, (int, float)) and abs(v) > 1e-9}
    if hits:
        print(f"   {e['desc'] or p.split('/')[-1]:42s} {hits}")

print("\n" + "=" * 108)
print("C — MUTATORS: every mutator record carrying a life term (H4)")
print("=" * 108)
muts = sorted(p for p in index() if p.startswith("records/game/mutators/"))
print(f"   {len(muts)} mutator records in corpus")
life_muts = []
for m in muts:
    rec, prov, own = merged(m)
    hits = {f: v for f, v in rec.items()
            if "life" in f.lower() and isinstance(v, (int, float)) and abs(v) > 1e-9}
    if hits:
        life_muts.append((m, hits, own))
print(f"   {len(life_muts)} carry a non-zero *life* field:\n")
for m, hits, own in life_muts:
    print(f"     {m.split('/')[-1]:44s} {hits}   [{own}]")

print("\n" + "=" * 108)
print("D — which mutators does the CRUCIBLE actually reference?")
print("=" * 108)
# survival mutator pools
pools = sorted(p for p in index()
               if "mutator" in p and not p.startswith("records/game/mutators/"))
for p in pools[:60]:
    print(f"     {p}   owners={index()[p]}")
print(f"   ({len(pools)} total)")
