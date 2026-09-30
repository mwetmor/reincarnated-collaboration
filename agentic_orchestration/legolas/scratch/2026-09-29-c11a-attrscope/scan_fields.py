#!/usr/bin/env python3
"""C-7: locate every record carrying a named field, across all 8 archives. READ-ONLY."""
import sys, json
sys.path.insert(0,'.')
from arz import arz, ARZS

TARGETS = set(sys.argv[1:]) or {"notEnoughManaSound"}
hits = {}
for n in ARZS:
    a = arz(n)
    # cheap prefilter: field name must be in this archive's string table
    st = set(a.strings)
    tgt = TARGETS & st
    if not tgt: continue
    for rec in a.records:
        try: d = a.get(rec)
        except Exception: continue
        f = tgt & set(d)
        if f:
            hits.setdefault(rec, []).append((n, d["__type__"], {k: d[k] for k in sorted(f)}))
print(json.dumps(hits, indent=1, default=str))
print(f"--- {len(hits)} records", file=sys.stderr)
