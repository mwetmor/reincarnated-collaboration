#!/usr/bin/env python3
"""P0 - orient: archive sizes, Class histogram under records/proxies/, path token census. READ-ONLY."""
import sys, pathlib, collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCS={
 "base":ROOT/"database/database.arz",
 "gdx1":ROOT/"gdx1/database/GDX1.arz",
 "gdx2":ROOT/"gdx2/database/GDX2.arz",
 "gdx3":ROOT/"gdx3/database/GDX3.arz",
 "sm_mod":ROOT/"mods/survivalmode/database/SurvivalMode.arz",
 "sm1":ROOT/"survivalmode1/database/SurvivalMode1.arz",
 "sm2":ROOT/"survivalmode2/database/SurvivalMode2.arz",
 "sm3":ROOT/"survivalmode3/database/SurvivalMode3.arz",
}
for k,p in ARCS.items():
    a=ArzArchive(p)
    recs=a.records
    prox=[r for r in recs if r.startswith("records/proxies/")]
    print(f"\n=== {k}  {p.name}  total_records={len(recs)}  under records/proxies/={len(prox)}")
    # top-level dirs
    tl=collections.Counter(r.split("/")[1] if r.count("/")>1 else r for r in recs)
    print("  top-level dirs:", dict(tl.most_common(14)))
    if prox:
        seg=collections.Counter(r.split("/")[2] for r in prox)
        print("  proxies/<seg2> :", dict(seg.most_common(30)))
