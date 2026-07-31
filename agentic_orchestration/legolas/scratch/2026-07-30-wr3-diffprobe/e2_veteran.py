#!/usr/bin/env python3
"""E2 - what the Veteran mutator does to the S-arm ceilings. READ-ONLY.
Veteran = records/game/balancingadjustment_challengemode_enemies01.dbr, applied as a Mutator
(Game.dll: Mutator::GetAttributePak, GameEngine::ContributeMutatorOffensiveDamageAttributes --
a contribution path SEPARATE from the monster AttributePak).
"""
import sys
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7")
from lib_corpus import get

_, _, VET = get("records/game/balancingadjustment_challengemode_enemies01.dbr")
_, _, PAK = get("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
_, _, AB5 = get("records/skills/nonplayerskills/passive/armorbase05.dbr")
_, _, AB1 = get("records/skills/nonplayerskills/passive/armorbase01.dbr")
_, _, ADJ = get("records/skills/nonplayerskills/passive/damage_totaladjuster.dbr")

vd = VET["offensiveTotalDamageModifier"]
vl = VET["characterLifeModifier"]
pk = PAK["offensiveTotalDamageModifier"][0]
print(f"Veteran mutator: offensiveTotalDamageModifier +{vd}  characterLifeModifier +{vl}")
print(f"Normal pak     : offensiveTotalDamageModifier {pk}")
print()


def rv(arr, r):
    return arr[min(max(r, 1), len(arr)) - 1]


def pool(ab, cl):
    return rv(ab["offensiveTotalDamageModifier"], cl), rv(ADJ["offensiveTotalDamageModifier"], (cl // 25) + 2)


print("=== outgoing-damage factor, Normal difficulty, boss chain (armorbase05) ===")
print(f"{'charLvl':>7s} {'S2 no-Vet':>10s} {'S2 +Vet sep':>12s} {'S2 +Vet pooled':>15s} {'S1 no-Vet':>10s} {'S1 +Vet':>9s}")
for cl in (13, 18, 19):
    a, j = pool(AB5, cl)
    s2 = (1 + (a + j) / 100) * (1 + pk / 100)
    s2vs = s2 * (1 + vd / 100)
    s2vp = (1 + (a + j + vd) / 100) * (1 + pk / 100)
    print(f"{cl:7d} {s2:10.4f} {s2vs:12.4f} {s2vp:15.4f} {0.75:10.4f} {0.75*(1+vd/100):9.4f}")
print()

# Prior published ceilings (post-mitigation, whole L13-reachable corpus) from d3/d5/d8.
CEIL = {"S1_PAK": 670.9, "S2_FULL": 252.9}
TGT = [("greatestDamageReceived", 260.498), ("lastHitBy", 273.704)]
a, j = pool(AB5, 18)
s2_18 = (1 + (a + j) / 100) * (1 + pk / 100)
mult_sep = 1 + vd / 100
mult_pool = ((1 + (a + j + vd) / 100) * (1 + pk / 100)) / s2_18

print("=== prior ceilings re-based under Veteran ===")
print(f"{'regime':22s} {'ceiling':>9s} {'260.498':>10s} {'273.704':>10s}")
for reg, c in CEIL.items():
    for lbl, m in (("no Veteran", 1.0), ("+Vet (separate stage)", mult_sep), ("+Vet (pooled)", mult_pool)):
        if reg == "S1_PAK" and lbl == "+Vet (pooled)":
            m = (1 + (-25 + vd) / 100) / 0.75      # S1 has no skill pool; pool the mutator into the pak
        cc = c * m
        f = lambda t: "REACHABLE" if cc >= t else f"short {100*(t-cc)/t:.1f}%"
        print(f"{reg+' '+lbl:44s} {cc:9.1f} {f(260.498):>14s} {f(273.704):>14s}")
print()
print("=== HP anchor under Veteran (measured Primordian lifeAndMana = 15,822) ===")
base18 = 15891 / ((1 - 0.71) * 1.50)
for lbl, pred in (("cl18, no Veteran (prior)", 15891),
                  ("cl18, +Vet separate stage", 15891 * (1 + vl / 100)),
                  ("cl18, +Vet pooled into pak", base18 * (1 - 0.71) * (1 + 0.50 + vl / 100))):
    print(f"   {lbl:32s} predicted {pred:10.0f}   ratio to measured {pred/15822:.3f}x")
print()
print(f"   base HP required at the save's OWN recorded monster level 13, WITH Veteran:")
need = 15822 / ((1 - 0.71) * 1.50 * (1 + vl / 100))
print(f"      base(cl13) = {need:,.0f}   vs back-solved base(cl18) = {base18:,.0f}"
      f"   -> implies {base18/need:.2f}x HP growth over levels 13->18")
print(f"      (Veteran life multiplier is {1+vl/100:.2f}x -- note how close these two are:"
      f" the HP anchor CANNOT separate 'cl18 no-Veteran' from 'cl13 Veteran'.)")
