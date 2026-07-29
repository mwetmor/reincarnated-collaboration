#!/usr/bin/env python3
"""P4 — resolve the Crucible wave context + SR boss-proxy context around Primordian."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
sm   = ArzArchive(ROOT / "mods/survivalmode/database/SurvivalMode.arz")
gdx2 = ArzArchive(ROOT / "gdx2/database/GDX2.arz")
base = ArzArchive(ROOT / "database/database.arz")

def dump(a, rp, title, maxlist=10):
    print(f"\n{'-'*84}\n### {title}\n### {rp}\n{'-'*84}")
    try:
        r = a.read_record(rp)
    except KeyError:
        print("  -- NOT PRESENT --"); return None
    for k in sorted(r):
        v = r[k]
        if isinstance(v, list) and len(v) > maxlist:
            v = f"[len={len(v)}] {v[:6]} ... {v[-2:]}"
        print(f"  {k:38s} = {v}")
    return r

print("#"*84); print("# PART A — CRUCIBLE (mods/survivalmode) wave structure"); print("#"*84)

# what tier wave dirs exist, and how many waves per tier
tiers = {}
for rp in sm.records:
    m = re.match(r"records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)([a-z]*)\.dbr", rp)
    if m:
        tiers.setdefault(int(m.group(1)), set()).add(int(m.group(2)))
print("\nCrucible tier -> wave numbers present:")
for t in sorted(tiers):
    ws = sorted(tiers[t])
    print(f"  tier{t:02d}: waves {min(ws)}-{max(ws)}  (count {len(ws)})")

dump(sm, "records/proxies/tier09waves/proxy_w06_p02a.dbr", "CRUCIBLE tier09 wave06 proxy (Primordian, pool1)")
dump(sm, "records/proxies/tier14waves/proxy_w02_p03a.dbr", "CRUCIBLE tier14 wave02 proxy (Primordian, pool2)")

# the level variance equation
dump(base, "records/proxies/lv7_uber hero.dbr", "lv7_uber hero level-variance equation (base)")
dump(sm,   "records/proxies/lv7_uber hero.dbr", "lv7_uber hero — survivalmode override?")

# Crucible level/difficulty controller records
print("\n\nCrucible records matching level/difficulty/wave-control patterns:")
for rp in sorted(sm.records):
    if re.search(r"(survival|crucible|difficult|tierlevel|gamelevel|wavecontrol|levelequation)", rp, re.I):
        print("   ", rp)

print("\n" + "#"*84); print("# PART B — SHATTERED REALM (gdx2 endlessdungeon) boss proxies"); print("#"*84)

for rp in ["records/endlessdungeon/proxies/proxy_boss/proxy_bossbaseeasy01_01.dbr",
           "records/endlessdungeon/proxies/proxy_boss/proxy_bossbasefull02_01.dbr"]:
    r = dump(gdx2, rp, f"SR boss proxy — {rp.split('/')[-1]}", maxlist=4)

print("\nAll SR boss proxy records (the family Primordian sits in):")
for rp in sorted(gdx2.records):
    if "endlessdungeon/proxies/proxy_boss/" in rp:
        print("   ", rp)
