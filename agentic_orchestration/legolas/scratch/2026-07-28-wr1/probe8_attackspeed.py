#!/usr/bin/env python3
"""probe8 (WR1 E-3) — attack-speed model.
(a) weapon-class base-speed fields across item classes
(b) any record defining speed-tag -> seconds
(c) monster-side cadence for the KC1 opposition roster + controllers. Read-only."""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
db = ArzArchive(ROOT/"database/database.arz")

print("### (a) census of characterBaseAttackSpeed values by item Class (database.arz)")
cnt = collections.Counter()
examples = {}
speedfields = collections.Counter()
for rp in db.records:
    if not rp.startswith("records/items/"): continue
    rt = db.record_type(rp)
    if not rt.startswith("Weapon"): continue
    rec = db.read_record(rp)
    for k in rec:
        if re.search(r'attackspeed|speed', k, re.I):
            speedfields[k] += 1
    v = rec.get('characterBaseAttackSpeed')
    cnt[(rt, v)] += 1
    examples.setdefault((rt, v), rp)
for (rt, v), n in sorted(cnt.items(), key=lambda x: (x[0][0], str(x[0][1]))):
    print(f"  {rt:28s} characterBaseAttackSpeed={v!r:24s} n={n:5d}  e.g. {examples[(rt,v)]}")
print("\n  speed-ish field names seen on weapon records:")
for k, n in speedfields.most_common(20):
    print(f"    {k:44s} {n}")

print("\n### (b) records that might map speed tag -> seconds")
for rp in db.records:
    base = rp.rsplit('/',1)[-1]
    if re.search(r'attackspeed|weaponspeed|speedtag', base, re.I) or 'itemattributes' in rp or rp.endswith('gameiteminfo.dbr'):
        print(f"  {rp}   [{db.record_type(rp)}]")
