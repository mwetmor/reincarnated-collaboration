#!/usr/bin/env python3
"""H2/H3: dump every HP/level-relevant field on each wave-160 roster record + its bio chain. READ-ONLY."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners

OUT = pathlib.Path(__file__).parent
roster = json.load(open(OUT / "t1_roster.json"))

TOK = ("life", "level", "health", "hp", "modifier", "classification", "bio",
       "character", "monster", "scale", "difficulty", "tier", "rank", "champion", "hero")

print("=" * 110)
print("STEP 2 — full field dump for one representative (Zantarin) so we can see the shape")
print("=" * 110)
rec, prov, own = merged("records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr")
print(f"owners={own}  fields={len(rec)}")
for f in sorted(rec):
    print(f"  {f:48s} = {str(rec[f])[:90]:90s} [{prov[f]}]")

print("\n" + "=" * 110)
print("STEP 3 — per-roster-record HP chain")
print("=" * 110)

rows = []
bios = {}
for p in sorted(roster):
    rec, prov, own = merged(p)
    if not rec:
        print(f"!! MISSING {p}")
        continue
    row = {"record": p, "owners": own}
    for f in sorted(rec):
        lf = f.lower()
        if any(t in lf for t in TOK) or "equation" in lf:
            row[f] = rec[f]
    rows.append(row)
    # follow bio / parent chains
    for f, v in rec.items():
        if isinstance(v, str) and v.lower().endswith(".dbr") and (
                "bio" in v.lower() or "attribute" in f.lower() or "Attribute" in f):
            bios.setdefault(v.lower(), set()).add(p)

for r in rows:
    print(f"\n-- {r['record']}  owners={r['owners']}")
    for k, v in r.items():
        if k in ("record", "owners"):
            continue
        print(f"     {k:46s} = {str(v)[:88]}")

print("\n\n== BIO CHAIN TARGETS ==")
for b in sorted(bios):
    print(f"  {b}   <- {len(bios[b])} records")

json.dump({"rows": rows, "bios": {k: sorted(v) for k, v in bios.items()}},
          open(OUT / "t2_monster_fields.json", "w"), indent=1, default=str)
print("\nwrote t2_monster_fields.json")
