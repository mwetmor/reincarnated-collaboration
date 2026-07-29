#!/usr/bin/env python3
"""probe18 — (a) per-cast cost band for non-channelled Oathkeeper skills (magnitude cross-check),
(b) the level/skill-point/tier arithmetic.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
archives = {p.name: ArzArchive(p) for p in [
    ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
    ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]}

print("=== (a) Oathkeeper skill energy costs (per-cast vs per-tick magnitude band) ===")
for rp in ["records/skills/playerclass09/righteousfervor1.dbr",
           "records/skills/playerclass09/judgment1.dbr",
           "records/skills/playerclass09/aegis1.dbr",
           "records/skills/playerclass09/viremight1.dbr",
           "records/skills/playerclass09/ascension1.dbr",
           "records/skills/playerclass09/eyeofreckoning1.dbr"]:
    for name, a in archives.items():
        if rp in a.records:
            rec = a.read_record(rp)
            mc = rec.get("skillManaCost")
            cd = rec.get("skillCooldownTime")
            print(f"  {rp.split('/')[-1]:24s} [{rec.get('Class'):42s}] tba={rec.get('timeBetweenAttacks')} "
                  f"cd={cd} cost={mc if not isinstance(mc, list) else [mc[0], mc[15] if len(mc) > 15 else None, mc[-1]]}")

print("\n=== (b) arithmetic ===")
pl = archives["GDX2.arz"].read_record("records/creatures/pc/playerlevels.dbr")
smp = pl["skillModifierPoints"]
tier = archives["database.arz"].read_record("records/game/gameengine.dbr")["skillMasteryTierLevel"]
mil = archives["database.arz"].read_record("records/creatures/pc/malepc01.dbr")["masteryIncrementLevel"]
print(f"  skillMasteryTierLevel = {tier}   -> EoR is skillTier 6 -> requires mastery bar {tier[5]}")
print(f"  masteryIncrementLevel = {mil}  (char level at which 1st / 2nd mastery may be taken)")

def points_at(L):
    # index i grants points on reaching level i+2  (verified: 49x3 -> lvl 2..50, 40x2 -> 51..90, 1 -> 91..100)
    return sum(smp[0:L - 1])

for L in range(2, 21):
    print(f"    level {L:3d}: {points_at(L):3d} skill points"
          + ("   <-- 26 needed for bar25 + EoR r1" if points_at(L) >= 26 and points_at(L - 1) < 26 else ""))
for L in (12, 25, 30, 40, 50, 100):
    print(f"    level {L:3d}: {points_at(L):3d} skill points")
