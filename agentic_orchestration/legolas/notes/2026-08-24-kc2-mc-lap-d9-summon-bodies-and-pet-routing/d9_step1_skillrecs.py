#!/usr/bin/env python3
"""D-9 step 1 -- dump the two player-summon SKILL records in full, from the Edition-III
overlay stack (the same basis `pm2_tg2_pet_chain.csv` was emitted on). READ-ONLY."""
import sys, json
NOTES = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
         "2026-08-12-kc2-roster-decode-completion")
sys.path.insert(0, NOTES)
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from s2_lib import E3

TARGETS = [
    "records/skills/playerclass09/summon_celestialguardian1.dbr",
    "records/skills/itemskillsgdx1/relics/summondeathstalker.dbr",
    "records/skills/playerclass09/summon_celestialguardian2_petmodifier.dbr",
    "records/items/gearrelic/d114_relic.dbr",
]

for t in TARGETS:
    rec, owners = E3.merged(t)
    print("=" * 100)
    print(t, "  owners=", owners, "  found=", rec is not None)
    if not rec:
        continue
    for k in sorted(rec):
        print("   %-44s %r" % (k, rec[k]))
