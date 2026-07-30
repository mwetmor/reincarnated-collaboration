#!/usr/bin/env python3
"""A9 — cross-creature run-speed census: anim root-motion base x characterRunSpeed.
Discriminates model (A) anim-driven base vs model (B) global-constant base. READ-ONLY."""
import sys, pathlib, re, math
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive
sys.path.insert(0,'.')
from a4_parse import parse
import tempfile, os

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
archives = [(p.name, ArzArchive(p)) for p in ARZS]
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")
arcs = []
for p in sorted(GD.rglob("Creatures.arc")):
    try: arcs.append((p, ArcArchive(p)))
    except Exception: pass

def rec(t):
    out = None
    for nm, a in archives:
        if t in a.records: out = a.read_record(t)   # last archive wins (expansion override)
    if out is None: raise KeyError(t)
    return out

def anm_bytes(assetpath):
    key = assetpath.replace("\\","/")
    if key.lower().startswith("creatures/"): key = key[len("creatures/"):]
    for p, a in arcs:
        if key in a.entries: return a.read_file(key)
    for p, a in arcs:
        for n in a.names():
            if n.lower().endswith(key.lower().split("/")[-1]): return a.read_file(n)
    return None

def base_speed(assetpath):
    b = anm_bytes(assetpath)
    if b is None: return None, None, None
    with tempfile.NamedTemporaryFile(suffix=".anm", delete=False) as f:
        f.write(b); tmp = f.name
    a = parse(tmp); os.unlink(tmp)
    root = a['bones'][0][1]
    d = math.dist(root[-1][:3], root[0][:3])
    dur = (a['nkeys']-1)/a['fps']
    return d, dur, (d/dur if dur else None)

for t in sys.argv[1:]:
    try: r = rec(t)
    except KeyError: print(f"{t}\tNOT FOUND"); continue
    crs = r.get("characterRunSpeed") or 0.0
    tbl = r.get("charAnimationTableName")
    ranim = rspd = None
    if tbl:
        try:
            at = rec(tbl)
            for pre in ("unarmed","sHanded","dHanded","ranged2h","ranged1h"):
                if at.get(pre+"RunAnim"):
                    ranim = at[pre+"RunAnim"]; rspd = at.get(pre+"RunAnimSpeed") or 1.0
                    break
        except KeyError: pass
    d = dur = base = None
    if ranim: d, dur, base = base_speed(ranim)
    eff = (base*rspd*crs) if base else None
    print(f"{t.split('/')[-1]:34s} crs={crs:5.2f} animSpd={rspd if rspd else 0:4.2f} "
          f"root={d if d else float('nan'):7.3f}u dur={dur if dur else float('nan'):6.3f}s "
          f"base={base if base else float('nan'):6.3f}u/s  eff={eff if eff else float('nan'):6.3f}u/s  {ranim}")
