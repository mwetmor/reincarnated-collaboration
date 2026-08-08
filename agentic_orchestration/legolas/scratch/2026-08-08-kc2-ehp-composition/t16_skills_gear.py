#!/usr/bin/env python3
"""Do any wave-160 roster SKILLS or EQUIPPED ITEMS carry a life term? READ-ONLY."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged

OUT = pathlib.Path(__file__).parent
chain = json.load(open(OUT / "t3_chain.json"))["chain"]

LIFEK = ("characterlife", "characterlifemodifier", "characterlifemultmodifier")


def life_fields(rec):
    out = {}
    for f, v in rec.items():
        lf = f.lower()
        if lf.startswith("characterlife") and "regen" not in lf:
            if isinstance(v, list):
                if any(isinstance(x, (int, float)) and abs(x) > 1e-9 for x in v):
                    out[f] = v
            elif isinstance(v, (int, float)) and abs(v) > 1e-9:
                out[f] = v
            elif isinstance(v, str) and v.strip() not in ("", "0"):
                out[f] = v
    return out


print("=" * 108)
print("Per-roster-record: SKILL and ITEM chains scanned for characterLife* terms")
print("=" * 108)
for p, e in sorted(chain.items(), key=lambda kv: kv[1]["desc"] or kv[0]):
    rec, prov, own = merged(p)
    who = e["desc"] or p.split("/")[-1]
    refs = set()
    for f, v in rec.items():
        if isinstance(v, str) and v.lower().endswith(".dbr"):
            lf = f.lower()
            if "skill" in lf or "item" in lf or "loot" in lf or "buff" in lf or "pet" in lf:
                refs.add(v.lower())
    hits = []
    seen = set()
    stack = list(refs)
    depth = 0
    while stack and depth < 4000:
        depth += 1
        r = stack.pop()
        if r in seen:
            continue
        seen.add(r)
        rr, _, ro = merged(r)
        if not rr:
            continue
        lf = life_fields(rr)
        if lf:
            hits.append((r, lf, ro))
        # follow buff/pet skill chains one more hop
        for f, v in rr.items():
            if isinstance(v, str) and v.lower().endswith(".dbr") and \
               any(t in f.lower() for t in ("buffskillname", "petskillname", "skillname", "modifierskill")):
                stack.append(v.lower())
    tag = "  <-- LIFE TERM" if hits else ""
    print(f"\n   {who[:44]:46s} refs={len(seen):4d}{tag}")
    for r, lf, ro in hits:
        print(f"        {r.split('/')[-1]:52s} {lf}   [{ro}]")
