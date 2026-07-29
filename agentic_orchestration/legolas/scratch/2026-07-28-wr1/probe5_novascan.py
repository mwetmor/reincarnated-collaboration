#!/usr/bin/env python3
"""probe5 (WR1 E-1) — corpus-wide census of ring/nova/frigid monster skills:
(a) every record whose path matches frigid|ring|nova|blizzard|frost|chill|cold under nonplayerskills
(b) every Skill_AttackProjectileRing record in the corpus, with its freeze payload.
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
PAT = re.compile(r'frigid|nova|ring|blizzard', re.I)

print("### (a) RING-CLASS records across corpus (Class == Skill_AttackProjectileRing)")
rows = []
for p in ARZS:
    a = ArzArchive(p)
    for rp in a.records:
        if a.record_type(rp) == "Skill_AttackProjectileRing":
            rec = a.read_record(rp)
            def g(k, i=None):
                v = rec.get(k)
                if isinstance(v, list):
                    return v[i] if (i is not None and i < len(v)) else (v[0] if v else None)
                return v
            rows.append((p.name, rp, rec.get('FileDescription'),
                         g('projectileLaunchNumber'), g('projectileLaunchRotation'),
                         g('projectileExplosionRadius'),
                         g('offensiveFreezeMin', 3), g('offensiveFreezeMax', 3),
                         g('offensiveColdMin', 3), g('offensivePhysicalMin', 3),
                         rec.get('skillProjectileName')))
for r in sorted(rows, key=lambda x: x[1]):
    print(f"  [{r[0]:12s}] {r[1]}")
    print(f"      desc={r[2]!r} n={r[3]} rot={r[4]} expRad={r[5]} freeze@r4={r[6]}-{r[7]} cold@r4={r[8]} phys@r4={r[9]}")
print(f"  TOTAL ring-class records: {len(rows)}")

print("\n### (b) nonplayerskills paths matching frigid|nova|ring|blizzard")
for p in ARZS:
    a = ArzArchive(p)
    for rp in a.records:
        if 'nonplayerskills' in rp and PAT.search(rp.rsplit('/',1)[-1]):
            print(f"  [{p.name:12s}] {rp:80s} {a.record_type(rp)}")
