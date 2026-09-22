#!/usr/bin/env python3
"""Full-database field scan. READ-ONLY.
  scan.py FIELDPAT [VALUEFILTER]   -- list records carrying a field matching regex"""
import sys, re, pathlib, struct, lz4.block
sys.path.insert(0,'.')
import arz

pat = re.compile(sys.argv[1])
lim = int(sys.argv[2]) if len(sys.argv)>2 else 60
tot = 0
for n in arz.ARZS:
    a = arz.arz(n)
    for rec in a.records:
        d = a.get(rec)
        hits = {k:v for k,v in d.items() if pat.search(k)}
        if hits:
            tot += 1
            if tot <= lim:
                print(f"{n}\t{rec}\t{hits}")
print(f"--- total records with a matching field: {tot}")
