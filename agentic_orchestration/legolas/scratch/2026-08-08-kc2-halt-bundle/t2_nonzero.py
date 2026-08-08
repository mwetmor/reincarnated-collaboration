#!/usr/bin/env python3
"""HALT-9 step 2: non-zero field inventory + RAMP/FLAT classification. READ-ONLY."""
import sys, pathlib, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
A = ArzArchive(ROOT / "mods/survivalmode/database/SurvivalMode.arz")
RECS = {"aspirant": "records/game/balancingadjustment_survivalmode_enemies01.dbr",
        "challenger": "records/game/balancingadjustment_survivalmode_enemies02.dbr",
        "gladiator": "records/game/balancingadjustment_survivalmode_enemies03.dbr"}
R = {d: A.read_record(p) for d, p in RECS.items()}

SKIP_STR = {"Class", "FileDescription", "templateName", "characterBaseAttackSpeedTag"}


def nz(v):
    if isinstance(v, list):
        return any(isinstance(x, (int, float)) and abs(x) > 1e-9 for x in v)
    if isinstance(v, (int, float)):
        return abs(v) > 1e-9
    return False


fields = sorted(set().union(*[set(r) for r in R.values()]))
nzf = [f for f in fields if any(nz(R[d].get(f)) for d in R)]

print(f"TOTAL fields per record: {len(fields)}")
print(f"NON-ZERO numeric fields (union over 3 difficulties): {len(nzf)}\n")

hdr = f"{'#':>3} {'field':46s} {'kind':7s} {'len':>4s} | {'ASPIRANT':>26s} | {'CHALLENGER':>26s} | {'GLADIATOR':>26s} | shape"
print(hdr)
print("-" * len(hdr))
rows = []
for i, f in enumerate(nzf, 1):
    cells, shapes, kinds, lns = [], [], [], []
    for d in ("aspirant", "challenger", "gladiator"):
        v = R[d].get(f)
        if isinstance(v, list):
            kinds.append("array"); lns.append(len(v))
            if len(v) >= 200:
                cells.append(f"{v[0]:g}/{v[99]:g}/{v[199]:g}")
            else:
                cells.append(f"len{len(v)}:{v[0]:g}..{v[-1]:g}")
            uniq = len(set(v))
            if uniq == 1:
                shapes.append("FLAT")
            else:
                mono = all(v[j + 1] >= v[j] for j in range(len(v) - 1)) or \
                       all(v[j + 1] <= v[j] for j in range(len(v) - 1))
                shapes.append("RAMP" if mono else "VARY")
        elif isinstance(v, (int, float)):
            kinds.append("scalar"); lns.append(0)
            cells.append(f"{v:g}")
            shapes.append("SCALAR")
        else:
            kinds.append("absent"); lns.append(0); cells.append("--"); shapes.append("--")
    kind = kinds[0] if len(set(kinds)) == 1 else "/".join(kinds)
    ln = lns[0] if len(set(lns)) == 1 else "*"
    shape = shapes[0] if len(set(shapes)) == 1 else "/".join(shapes)
    print(f"{i:>3} {f:46s} {kind:7s} {str(ln):>4s} | {cells[0]:>26s} | {cells[1]:>26s} | {cells[2]:>26s} | {shape}")
    rows.append({"field": f, "kind": kind, "len": ln, "shape": shape})

json.dump(rows, open(pathlib.Path(__file__).parent / "t2_nonzero_fields.json", "w"), indent=1)
print(f"\nARRAY fields: {sum(1 for r in rows if r['kind']=='array')}   SCALAR fields: {sum(1 for r in rows if r['kind']=='scalar')}")
