#!/usr/bin/env python3
"""HALT-5: corpus-wide sweep for characterManaLimitReserve* on everything the fixture has active.
READ-ONLY."""
import sys, pathlib, re, json, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
STACK = [("base", ROOT / "database/database.arz"), ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
         ("gdx2", ROOT / "gdx2/database/GDX2.arz"), ("gdx3", ROOT / "gdx3/database/GDX3.arz")]

M = {}
ARCH = {}
for k, p in STACK:
    a = ArzArchive(p)
    ARCH[k] = a
    for r in a.records:
        M[r] = k          # later archives win


def rec(path):
    p = str(path).lower().replace("\\", "/")
    k = M.get(p)
    return ARCH[k].read_record(p) if k else None


FIELDS = ["characterManaLimitReserve", "characterManaLimitReserveModifier",
          "characterManaLimitReserveReduction", "characterManaLimitReserveReductionModifier"]

# ---------- pass 1: corpus-wide census of ANY record carrying a non-zero reserve field ----------
hits = {}
for p, k in M.items():
    try:
        r = ARCH[k].read_record(p)
    except Exception:
        continue
    d = {}
    for f in FIELDS:
        v = r.get(f)
        if isinstance(v, list) and any(abs(x) > 1e-9 for x in v if isinstance(x, (int, float))):
            d[f] = v
        elif isinstance(v, (int, float)) and abs(v) > 1e-9:
            d[f] = v
    if d:
        d["_arch"] = k
        d["_cls"] = r.get("Class")
        d["_fd"] = r.get("FileDescription")
        d["_dn"] = r.get("skillDisplayName") or r.get("itemNameTag")
        hits[p] = d

print(f"== CORPUS CENSUS: {len(hits)} records in the whole DB carry a non-zero reserve field ==")
byfam = collections.Counter(re.sub(r"/[^/]+$", "", p) for p in hits)
for fam, n in byfam.most_common(30):
    print(f"   {n:4d}  {fam}")
json.dump(hits, open(HERE / "t6_reserve_census.json", "w"), indent=0, default=str)
