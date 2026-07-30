#!/usr/bin/env python3
"""N1 — dump only structurally-interesting (non-zero/non-False) fields. READ-ONLY."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
archives = [(p.name, ArzArchive(p)) for p in ARZS]
def interesting(v):
    if v is False or v == 0 or v == 0.0 or v == '' : return False
    if isinstance(v, list):
        return any(x not in (0, 0.0, False, '') for x in v)
    return True
for t in sys.argv[1:]:
    found=False
    for name, a in archives:
        if t in a.records:
            rec = a.read_record(t)
            print(f"=== {t}  [{name}] type={a.record_type(t)} fields={len(rec)}")
            for k in sorted(rec):
                v = rec[k]
                if not interesting(v): continue
                if isinstance(v, list) and len(v) > 6:
                    v = f"[{v[0]!r} .. {v[-1]!r}]  (len={len(v)})"
                print(f"  {k:46s} {v!r}")
            found=True
    if not found: print(f"=== {t}  NOT FOUND")
