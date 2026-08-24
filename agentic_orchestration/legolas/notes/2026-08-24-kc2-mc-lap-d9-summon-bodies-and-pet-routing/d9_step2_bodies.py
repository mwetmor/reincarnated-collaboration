#!/usr/bin/env python3
"""D-9 step 2 -- dump the summon BODY records in full. READ-ONLY."""
import sys
NOTES = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
         "2026-08-12-kc2-roster-decode-completion")
sys.path.insert(0, NOTES)
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from s2_lib import E3

TARGETS = ["records/skills/itemskillsgdx1/pets/itempet_deathstalker_a01.dbr"]
TARGETS += ["records/skills/playerclass09/pets/celestialguardian_%02d.dbr" % i for i in (1, 2, 26)]

for t in TARGETS:
    rec, owners = E3.merged(t)
    print("=" * 100)
    print(t, "  owners=", owners, "  found=", rec is not None)
    if not rec:
        continue
    for k in sorted(rec):
        print("   %-44s %r" % (k, rec[k]))

# --- variation census over all 26 guardian bodies -------------------------------------------
print("=" * 100)
print("GUARDIAN 26-BODY VARIATION CENSUS")
recs = []
for i in range(1, 27):
    p = "records/skills/playerclass09/pets/celestialguardian_%02d.dbr" % i
    r, o = E3.merged(p)
    recs.append((i, p, r, o))
    if r is None:
        print("  MISSING", p)
keys = set()
for _, _, r, _ in recs:
    if r:
        keys |= set(r)
for k in sorted(keys):
    vals = [repr(r.get(k)) if r else "<missing>" for _, _, r, _ in recs]
    if len(set(vals)) == 1:
        print("  CONST  %-40s %s" % (k, vals[0][:150]))
    else:
        print("  VARIES %-40s" % k)
        for (i, _, _, _), v in zip(recs, vals):
            print("           rank %2d  %s" % (i, v[:150]))
