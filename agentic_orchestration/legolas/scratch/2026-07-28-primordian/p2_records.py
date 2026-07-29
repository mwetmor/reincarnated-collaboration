#!/usr/bin/env python3
"""P2 — dump + diff the Primordian-relevant records across base / gdx2 / survivalmode."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
A = {
    "base": ArzArchive(ROOT / "database/database.arz"),
    "gdx2": ArzArchive(ROOT / "gdx2/database/GDX2.arz"),
    "sm":   ArzArchive(ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
    "sm1":  ArzArchive(ROOT / "survivalmode1/database/SurvivalMode1.arz"),
    "sm2":  ArzArchive(ROOT / "survivalmode2/database/SurvivalMode2.arz"),
    "sm3":  ArzArchive(ROOT / "survivalmode3/database/SurvivalMode3.arz"),
}

def dump(tag, rp, title):
    print(f"\n{'='*90}\n### {title}\n### [{tag}] {rp}\n{'='*90}")
    try:
        r = A[tag].read_record(rp)
    except KeyError:
        print("  -- NOT IN ARCHIVE --")
        return None
    for k in sorted(r):
        v = r[k]
        if isinstance(v, list) and len(v) > 8:
            v = f"[len={len(v)}] {v[:6]} ... {v[-2:]}"
        print(f"  {k:42s} = {v}")
    return r

MON = "records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr"
base_mon = dump("base", MON, "PRIMORDIAN monster record — BASE")
sm_mon   = dump("sm",   MON, "PRIMORDIAN monster record — SURVIVALMODE (Crucible override)")

print(f"\n{'='*90}\n### DIFF base vs survivalmode monster record\n{'='*90}")
if base_mon and sm_mon:
    keys = sorted(set(base_mon) | set(sm_mon))
    ndiff = 0
    for k in keys:
        b, s = base_mon.get(k, "<absent>"), sm_mon.get(k, "<absent>")
        if b != s:
            ndiff += 1
            print(f"  {k}\n      base = {b}\n      surv = {s}")
    print(f"  -> {ndiff} differing fields out of {len(keys)}")

dump("sm",   "records/proxies/poolsboss/slith_primordian.dbr", "CRUCIBLE boss pool — Primordian")
dump("gdx2", "records/endlessdungeon/proxies/poolsboss/slith_primordian.dbr", "SHATTERED REALM boss pool — Primordian")
