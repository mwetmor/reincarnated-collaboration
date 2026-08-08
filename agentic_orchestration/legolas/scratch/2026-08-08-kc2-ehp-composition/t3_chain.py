#!/usr/bin/env python3
"""H1/H2/H3: full HP composition chain per wave-160 roster record. READ-ONLY."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged

OUT = pathlib.Path(__file__).parent
roster = json.load(open(OUT / "t1_roster.json"))

# --- level variance proxies ---
print("=" * 110)
print("A — levelVarianceEquation proxy records (the SPAWN-LEVEL layer)")
print("=" * 110)
for lv in ("records/proxies/lv8_boss+.dbr", "records/proxies/lv7_uber hero.dbr",
           "records/proxies/lv6_hero.dbr", "records/proxies/lv2_normal.dbr",
           "records/proxies/lv3_strong.dbr"):
    rec, prov, own = merged(lv)
    if not rec:
        print(f"  !! ABSENT {lv}")
        continue
    print(f"\n-- {lv}  owners={own}  fields={len(rec)}")
    for f in sorted(rec):
        print(f"     {f:40s} = {str(rec[f])[:80]:80s} [{prov[f]}]")

# --- per-record chain ---
print("\n\n" + "=" * 110)
print("B — per-roster-record: charLevel eq, bio, classification, own life fields")
print("=" * 110)
chain = {}
for p in sorted(roster):
    rec, prov, own = merged(p)
    e = {"owners": own,
         "charLevel": rec.get("charLevel"),
         "bio": rec.get("characterAttributeEquations"),
         "cls": rec.get("monsterClassification"),
         "characterLife": rec.get("characterLife"),
         "characterLifeModifier": rec.get("characterLifeModifier"),
         "minLevel": rec.get("minLevel"), "maxLevel": rec.get("maxLevel"),
         "desc": rec.get("FileDescription"),
         "pools": roster[p]["pools"]}
    # any other *Life* fields with non-zero value
    for f, v in rec.items():
        if "life" in f.lower() and f not in e and isinstance(v, (int, float)) and abs(v) > 1e-9:
            e.setdefault("otherLife", {})[f] = v
    chain[p] = e
    print(f"\n{p}")
    print(f"    desc={e['desc']}  cls={e['cls']}  owners={own}")
    print(f"    charLevel = {e['charLevel']!r}")
    print(f"    bio       = {e['bio']!r}")
    print(f"    ownLife   = characterLife={e['characterLife']!r} mod={e['characterLifeModifier']!r} "
          f"other={e.get('otherLife')}")

# --- bios ---
print("\n\n" + "=" * 110)
print("C — bio records (the characterLife EQUATION layer)")
print("=" * 110)
biopaths = sorted({v["bio"].lower() for v in chain.values() if v["bio"]})
bios = {}
for b in biopaths:
    rec, prov, own = merged(b)
    bios[b] = {"owners": own, "fields": rec}
    print(f"\n-- {b}  owners={own}  fields={len(rec)}")
    for f in sorted(rec):
        print(f"     {f:40s} = {str(rec[f])[:82]:82s} [{prov[f]}]")

json.dump({"chain": chain, "bios": {k: {"owners": v["owners"], "fields": v["fields"]} for k, v in bios.items()}},
          open(OUT / "t3_chain.json", "w"), indent=1, default=str)
print("\nwrote t3_chain.json")
