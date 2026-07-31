#!/usr/bin/env python3
"""E1 - quantify the damper chain as a function of (difficulty, monster charLevel).
READ-ONLY. Primordian chain: armorbase05 (rank=charLevel) + damage_totaladjuster
(rank=(charLevel/25)+2) pooled, then the difficulty pak as a separate multiplicative stage.
"""
import sys
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7")
from lib_corpus import get

_, _, AB5 = get("records/skills/nonplayerskills/passive/armorbase05.dbr")
_, _, AB1 = get("records/skills/nonplayerskills/passive/armorbase01.dbr")
_, _, ADJ = get("records/skills/nonplayerskills/passive/damage_totaladjuster.dbr")
_, _, PAK = get("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
_, _, DBP = get("records/skills/nonplayerskills/passive/damagebase_physical04.dbr")

pak_dmg = PAK["offensiveTotalDamageModifier"]
DIFF = [("Normal", 0), ("Elite", 1), ("Ultimate", 2)]


def rank_val(arr, rank):
    return arr[min(max(rank, 1), len(arr)) - 1]


def pool(armor, cl):
    a = rank_val(armor["offensiveTotalDamageModifier"], cl)
    j = rank_val(ADJ["offensiveTotalDamageModifier"], (cl // 25) + 2)
    return a, j, 1 + (a + j) / 100.0


print("PAK offensiveTotalDamageModifier, 12 slots = 3 difficulties x 4 player counts")
for name, d in DIFF:
    print(f"   {name:9s} slots[{d*4}:{d*4+4}] = {pak_dmg[d*4:d*4+4]}  -> 1p factor x{1+pak_dmg[d*4]/100:.4f}")
print()

print("=== BOSS CHAIN (armorbase05) composite outgoing factor by monster charLevel x difficulty ===")
print(f"{'charLvl':>7s} {'armorbase05':>12s} {'adjuster':>9s} {'pool':>7s} |"
      f"{'Normal':>9s} {'Elite':>9s} {'Ultimate':>9s} | {'phys max':>9s}")
for cl in (13, 16, 18, 19, 25, 30, 40, 45, 50, 55, 65, 75, 85, 88, 94, 100):
    a, j, pl = pool(AB5, cl)
    row = f"{cl:7d} {a:12.1f} {j:9.1f} {pl:7.4f} |"
    for name, d in DIFF:
        row += f"{pl*(1+pak_dmg[d*4]/100):9.4f}"
    row += f" | {rank_val(DBP['offensivePhysicalMax'], cl):9.0f}"
    print(row)
print()
print("=== TRASH CHAIN (armorbase01/02) ===")
print(f"{'charLvl':>7s} {'armorbase01':>12s} {'pool':>7s} |{'Normal':>9s} {'Elite':>9s} {'Ultimate':>9s}")
for cl in (13, 18, 30, 45, 56, 65, 85, 100):
    a, j, pl = pool(AB1, cl)
    row = f"{cl:7d} {a:12.1f} {pl:7.4f} |"
    for name, d in DIFF:
        row += f"{pl*(1+pak_dmg[d*4]/100):9.4f}"
    print(row)
print()
ref = pool(AB5, 18)[2] * (1 + pak_dmg[0] / 100)
print(f"REFERENT (boss, cl 18, Normal, 1p) composite = x{ref:.4f}   [= S2_FULL]")
print(f"S1_PAK (pak only, no pool)                   = x{1+pak_dmg[0]/100:.4f}")
print(f"ratio S1/S2 = {(1+pak_dmg[0]/100)/ref:.3f}x")
print()
print("Monster charLevel at which the boss chain's Normal composite reaches S1_PAK's x0.75:")
for cl in range(1, 201):
    if pool(AB5, cl)[2] * 0.75 >= 0.75:
        print(f"   charLevel {cl}  (pool crosses 1.0)"); break
