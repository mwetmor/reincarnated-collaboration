#!/usr/bin/env python3
"""Load all Text_EN.arc tag tables from the depot. READ-ONLY."""
import sys, pathlib; sys.path.insert(0,'.')
from arcread import ArcArchive, parse_tag_file
DEPOT = pathlib.Path("/Users/admin/depots")
ARCS = sorted(DEPOT.glob("*/24346246/**/Text_EN.arc"))
TAGS, SRC = {}, {}
for p in ARCS:
    a = ArcArchive(p)
    for name in a.names():
        if not name.lower().endswith(".txt"): continue
        try: pairs = parse_tag_file(a.read_file(name))
        except Exception as e: print("SKIP", p.parent.parent.name, name, e, file=sys.stderr); continue
        for k,v in pairs:
            TAGS[k]=v; SRC[k]=(p.parent.parent.name, name)
if __name__ == "__main__":
    import re
    pat = re.compile(sys.argv[1], re.I)
    val = len(sys.argv)>2
    n=0
    for k in sorted(TAGS):
        if pat.search(k) or (val and pat.search(TAGS[k])):
            print(f"{k}\t{TAGS[k]}\t<- {SRC[k][1]}"); n+=1
    print(f"--- {n} tags matched (corpus {len(TAGS)})", file=sys.stderr)
