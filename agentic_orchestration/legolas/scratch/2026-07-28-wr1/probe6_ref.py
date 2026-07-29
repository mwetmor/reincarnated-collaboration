#!/usr/bin/env python3
"""probe6 (WR1 E-1) — reverse-reference: which creatures wire the cold-ring/nova candidates,
and are any of them Act-1 / Wightmire spawns? Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
CAND = [
 "records/skills/nonplayerskills/heroskills/igrixx_frigidring.dbr",
 "records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr",
 "records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr",
 "records/skills/nonplayerskills/bossskills/special/cloneice_icenova.dbr",
 "records/skills/nonplayerskills/bossskills/primordian_arcticblast.dbr",
]
archives = [(p.name, ArzArchive(p)) for p in ARZS]

# 1. creature -> which candidates it wires
for name, a in archives:
    for rp in a.records:
        if not rp.startswith("records/creatures/"):
            continue
        rec = a.read_record(rp)
        hits = []
        for k, v in rec.items():
            if isinstance(v, str) and v in CAND:
                hits.append((k, v.rsplit('/',1)[-1]))
        if hits:
            print(f"[{name}] {rp}")
            print(f"        desc={rec.get('description')} class={rec.get('monsterClassification')} charLevel={rec.get('charLevel')}")
            for k, v in sorted(hits):
                print(f"        {k:26s} -> {v}")

# 2. igrixx_frigidring full scalar + ranks
print("\n### igrixx_frigidring detail")
T = "records/skills/nonplayerskills/heroskills/igrixx_frigidring.dbr"
for name, a in archives:
    if T in a.records:
        rec = a.read_record(T)
        print(f"  [{name}] type={a.record_type(T)}")
        for k in sorted(rec):
            v = rec[k]
            if isinstance(v, list):
                if any((isinstance(x,(int,float)) and x != 0) for x in v):
                    print(f"    {k:40s} [n={len(v)}] r1={v[0]} r4={v[3] if len(v)>3 else None} r5={v[4] if len(v)>4 else None}")
            elif isinstance(v, (int,float)) and v == 0:
                continue
            elif v is False:
                continue
            else:
                print(f"    {k:40s} {v!r}")
        break

# 3. which proxies/pools reference the creatures found above (area001 = Act1)
