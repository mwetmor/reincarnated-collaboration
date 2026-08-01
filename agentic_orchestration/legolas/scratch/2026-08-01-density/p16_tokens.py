#!/usr/bin/env python3
"""P16 - widen folklore-token search to ALL record paths (not just proxies). READ-ONLY."""
import sys, pathlib, collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ALL={}
for k,p in [("base","database/database.arz"),("gdx1","gdx1/database/GDX1.arz"),
            ("gdx2","gdx2/database/GDX2.arz"),("gdx3","gdx3/database/GDX3.arz")]:
    a=ArzArchive(ROOT/p)
    for r in a.records: ALL.setdefault(r,k)
print(f"total campaign records indexed: {len(ALL)}")
for t in ["cronley","krieg","cellar","fleshwork","heretic","ancientgrove","warden","valbury","bastionofchaos",
          "stepsoftorment","direni","burrwitch","shatteredrealm","tomb"]:
    hits=[r for r in ALL if t in r.lower()]
    print(f"\n## '{t}': {len(hits)} records")
    for r in sorted(hits)[:8]: print(f"     [{ALL[r]}] {r}")
    if len(hits)>8: print(f"     ... +{len(hits)-8} more")
