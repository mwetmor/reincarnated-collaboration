#!/usr/bin/env python3
"""H1/H2/H4: corpus-wide hunt for every remaining HP-multiplier layer. READ-ONLY."""
import sys, pathlib, json, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index, find, read

OUT = pathlib.Path(__file__).parent

print("=" * 110)
print("A — records/game/* inventory (where global scalars live)")
print("=" * 110)
game = [p for p in index() if p.startswith("records/game/")]
for p in sorted(game):
    print(f"   {p}   owners={index()[p]}")

print("\n" + "=" * 110)
print("B — gameengine.dbr : every field whose NAME touches life/health/hero/champion/boss/difficulty")
print("=" * 110)
rec, prov, own = merged("records/game/gameengine.dbr")
print(f"owners={own} fields={len(rec)}")
TOK = ("life", "health", "hero", "champion", "boss", "difficulty", "monster", "level", "scal")
for f in sorted(rec):
    if any(t in f.lower() for t in TOK):
        print(f"   {f:46s} = {str(rec[f])[:80]:80s} [{prov[f]}]")

print("\n" + "=" * 110)
print("C — gameengine.dbr FULL field list (so nothing is missed)")
print("=" * 110)
for f in sorted(rec):
    print(f"   {f:46s} = {str(rec[f])[:74]}")
