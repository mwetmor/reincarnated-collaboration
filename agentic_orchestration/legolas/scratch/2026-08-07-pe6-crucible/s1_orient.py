#!/usr/bin/env python3
"""S1 — PE6 orient. READ-ONLY.
Enumerate every record under records/proxies/tier*waves/ across the 4-archive survival overlay stack,
plus every survival-mode record that is NOT a wave spawn-point proxy. Establish schema + coverage.
"""
import sys, pathlib, collections, re, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
STACK = [("sm_mod", ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1",    ROOT / "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2",    ROOT / "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3",    ROOT / "survivalmode3/database/SurvivalMode3.arz")]
CAMP = [("base", ROOT / "database/database.arz"), ("gdx1", ROOT / "gdx1/database/GDX1.arz"),
        ("gdx2", ROOT / "gdx2/database/GDX2.arz"), ("gdx3", ROOT / "gdx3/database/GDX3.arz")]

ARCS = {}
OWNER = {}          # path -> owner key (LAST writer wins = survival overrides campaign)
OWNERS_ALL = collections.defaultdict(list)
for k, p in CAMP + STACK:
    a = ArzArchive(p)
    ARCS[k] = a
    for r in a.records:
        OWNER[r] = k
        OWNERS_ALL[r].append(k)

print(f"total distinct records across 8 archives: {len(OWNER)}")
for k, a in ARCS.items():
    print(f"  {k:8s} rt_count={a.rt_count:7d} records={len(a.records):7d} strings={len(a.strings):7d}")

# ---- every record under a tierNNwaves folder
TIERDIR = re.compile(r"^records/proxies/tier(\d+)waves/(.+)$")
byTier = collections.defaultdict(list)
nonwave = []
WAVEPAT = re.compile(r"^proxy_w(\d+)_p(\d+)([a-z]*)\.dbr$")
for path in OWNER:
    m = TIERDIR.match(path)
    if not m:
        continue
    t = int(m.group(1)); leaf = m.group(2)
    byTier[t].append(leaf)
    if not WAVEPAT.match(leaf):
        nonwave.append(path)

print(f"\ntier dirs present: {sorted(byTier)}")
print(f"records under tier*waves: {sum(len(v) for v in byTier.values())}")
print(f"NON-conforming (not proxy_wWW_pPP*.dbr): {len(nonwave)}")
for p in sorted(nonwave)[:40]:
    print("   ", p, "|owner", OWNER[p])

print("\nper-tier leaf counts + wave indices + suffix variants:")
for t in sorted(byTier):
    waves = collections.defaultdict(set)
    sfx = collections.Counter()
    for leaf in byTier[t]:
        m = WAVEPAT.match(leaf)
        if not m: continue
        waves[int(m.group(1))].add(int(m.group(2)))
        sfx[m.group(3)] += 1
    print(f"  tier{t:02d}: leaves={len(byTier[t]):3d} waves={sorted(waves)} "
          f"pts/wave={{{', '.join(f'w{w}:{len(waves[w])}' for w in sorted(waves))}}} sfx={dict(sfx)}")

# ---- all survival-only records NOT under proxies (script entities, game, ui, etc.)
survonly = collections.defaultdict(list)
for path, owner in OWNER.items():
    if owner not in ("sm_mod", "sm1", "sm2", "sm3"):
        continue
    if path.startswith("records/proxies/tier"):
        continue
    top = "/".join(path.split("/")[:3])
    survonly[top].append(path)
print("\n=== survival-archive-owned records OUTSIDE tier*waves, by folder ===")
for top, ps in sorted(survonly.items(), key=lambda kv: -len(kv[1])):
    print(f"  {len(ps):5d}  {top}")

json.dump({"tiers": {str(k): sorted(v) for k, v in byTier.items()},
           "nonwave": sorted(nonwave)},
          open("s1_tiers.json", "w"), indent=1)
print("\n[wrote s1_tiers.json]")
