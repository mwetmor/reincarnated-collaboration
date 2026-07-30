#!/usr/bin/env python3
"""A10 — is the last key a duplicate of the first (looping clip)? Decides (N-1)/fps vs N/fps."""
import sys, pathlib, math
sys.path.insert(0,'.')
from a4_parse import parse
for f in sys.argv[1:]:
    a = parse(f)
    # compare non-root bones frame0 vs frameN-1 and frame0 vs frame1
    d_end = d_1 = 0.0
    for name, keys in a['bones'][1:]:
        d_end += sum(abs(keys[-1][c]-keys[0][c]) for c in range(14))
        d_1   += sum(abs(keys[1][c]-keys[0][c]) for c in range(14))
    print(f"{pathlib.Path(f).name:52s} keys={a['nkeys']:3d}  |f0-fN-1|={d_end:9.5f}  |f0-f1|={d_1:9.5f}  "
          f"{'LOOP-DUP' if d_end < d_1*0.25 else 'distinct'}")
