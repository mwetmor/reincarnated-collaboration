#!/usr/bin/env python3
"""A7 — per-bone motion range; find which bone carries root translation."""
import sys, pathlib
sys.path.insert(0,'.')
from a4_parse import parse
a = parse(sys.argv[1])
print(f"{pathlib.Path(sys.argv[1]).name} keys={a['nkeys']} fps={a['fps']}")
for name, keys in a['bones']:
    rngs = []
    for c in range(14):
        vs = [k[c] for k in keys]
        rngs.append(max(vs)-min(vs))
    if max(rngs[:3]) > 0.01 or (len(sys.argv)>2 and sys.argv[2].lower() in name.lower()):
        print(f"  {name:24s} transRange={rngs[0]:9.3f} {rngs[1]:9.3f} {rngs[2]:9.3f}  "
              f"first={keys[0][:3]} last={keys[-1][:3]}")
