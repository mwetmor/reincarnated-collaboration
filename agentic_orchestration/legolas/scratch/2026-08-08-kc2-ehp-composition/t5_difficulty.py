#!/usr/bin/env python3
"""H1: the ORDINARY difficulty-scaling layer. READ-ONLY."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged

RECS = ["records/game/balancingadjustment_mp+difficulty_enemies01.dbr",
        "records/game/balancingadjustment_mp+difficulty_players01.dbr",
        "records/game/balancingadjustment_mp+difficulty_pets01.dbr",
        "records/game/balancingadjustment_challengemode_enemies01.dbr",
        "records/game/balancingadjustment_ultramode_enemies01.dbr",
        "records/game/gameproxies.dbr"]


def nz(v):
    if isinstance(v, list):
        return any(isinstance(x, (int, float)) and abs(x) > 1e-9 for x in v)
    if isinstance(v, (int, float)):
        return abs(v) > 1e-9
    if isinstance(v, str):
        return v.strip() not in ("", "0")
    return bool(v)


for p in RECS:
    rec, prov, own = merged(p)
    if not rec:
        print(f"\n!! ABSENT {p}")
        continue
    hits = {f: v for f, v in rec.items() if nz(v)}
    print("\n" + "=" * 108)
    print(f"{p}   owners={own}   fields={len(rec)}   non-zero={len(hits)}")
    print("=" * 108)
    for f in sorted(hits):
        v = hits[f]
        if isinstance(v, list) and len(v) > 12:
            s = f"len{len(v)} [{v[0]}, {v[1]}, ... {v[98] if len(v) > 98 else '?'}(i98), {v[99] if len(v) > 99 else '?'}(i99), ... {v[-1]}]"
        else:
            s = str(v)
        print(f"   {f:48s} = {s[:100]}   [{prov[f]}]")
