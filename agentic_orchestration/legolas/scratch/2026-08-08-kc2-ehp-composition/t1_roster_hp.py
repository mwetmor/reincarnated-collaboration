#!/usr/bin/env python3
"""H3 step 1: read the ACTUAL wave-160 roster records + their bio HP fields. READ-ONLY."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners, find, read

OUT = pathlib.Path(__file__).parent

POOLS = {
    "p01": "records/proxies/poolsboss/nemesis_all.dbr",
    "p02": "records/proxies/poolsbossgdx1/nemesis_all_noaetherialvanguard.dbr",
    "p03": "records/proxies/poolsbossgdx1/nemesis_wendigooraetherialvanguard.dbr",
    "p04a": "records/proxies/poolsbossgdx1/aetherialcolossus_galakros.dbr",
    "p04b": "records/proxies/poolsbossgdx2/korvaaktombguardian.dbr",
    "p06": "records/proxies/poolsherogdx1/wendigocannibal_hero.dbr",
}

print("=" * 100)
print("STEP 1 — resolve wave-160 pool records and their monster entries")
print("=" * 100)

roster = {}     # monster record path -> {pools:[], levelEq:..}
for tag, pth in POOLS.items():
    rec, prov, own = merged(pth)
    if not rec:
        print(f"  !! {tag}: NOT FOUND {pth}")
        continue
    print(f"\n-- {tag}  {pth}   owners={own}  fields={len(rec)}")
    for f in sorted(rec):
        if any(t in f.lower() for t in ("spawn", "champion", "ignoregamebalance", "level")):
            print(f"     {f:44s} = {rec[f]!r}   [{prov[f]}]")
    # entries — non-champion slots are name{i}, champion slots nameChampion{i}
    for pref, lvpref in (("name", "levelVarianceEquation"),
                         ("nameChampion", "levelVarianceEquationChampion")):
        for i in range(1, 40):
            v = rec.get(f"{pref}{i}")
            if not v:
                continue
            paths = v if isinstance(v, list) else [v]
            for pp in paths:
                if not pp:
                    continue
                k = pp.lower()
                roster.setdefault(k, {"pools": [], "lvkeys": {}, "slot": pref})
                roster[k]["pools"].append(f"{tag}:{pref}{i}")
                for lk in (f"{lvpref}{i}", f"minPlayerLevel{i}", f"weight{i}", f"limit{i}"):
                    if lk in rec:
                        roster[k]["lvkeys"][lk] = rec[lk]

print(f"\n\n== ROSTER: {len(roster)} distinct monster records ==")
for p in sorted(roster):
    print(f"  {p}  pools={roster[p]['pools']}  {roster[p]['lvkeys']}")

json.dump({k: v for k, v in roster.items()}, open(OUT / "t1_roster.json", "w"), indent=1, default=str)
print("\nwrote t1_roster.json")
