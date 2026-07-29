#!/usr/bin/env python3
"""P8 — endgame stat picture. Raw inputs + bracketed composition (operator still HELD per
2026-07-28-kitcal1-primordian-proto.md §7)."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

R = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
base = ArzArchive(R / "database/database.arz")
sm   = ArzArchive(R / "mods/survivalmode/database/SurvivalMode.arz")

ab = base.read_record("records/skills/nonplayerskills/passive/armorbase05.dbr")
dp = base.read_record("records/skills/nonplayerskills/passive/damagebase_physical04.dbr")
dt = base.read_record("records/skills/nonplayerskills/passive/damage_totaladjuster.dbr")
print("armorbase05 array lengths:", {k: len(v) for k, v in ab.items() if isinstance(v, list)})
for f in ["characterLifeModifier", "offensiveTotalDamageModifier", "defensiveProtection"]:
    a = ab.get(f)
    if isinstance(a, list):
        print(f"  armorbase05.{f}: len={len(a)}  r13={a[12]} r17={a[16]} r100={a[99] if len(a)>99 else None} "
              f"r105={a[104] if len(a)>104 else None} r108={a[107] if len(a)>107 else None} last={a[-1]}")
for f in ["offensivePhysicalMin", "offensivePhysicalMax"]:
    a = dp[f]
    print(f"  damagebase_physical04.{f}: len={len(a)} r13={a[12]} r105={a[104]} r108={a[107]}")
a = dt["offensiveTotalDamageModifier"]
print(f"  damage_totaladjuster.oTDM: len={len(a)} r2={a[1]} r6={a[5]}")

mp = base.read_record("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
sm_u = sm.read_record("records/game/balancingadjustment_survivalmode_enemies03.dbr")
sm_n = sm.read_record("records/game/balancingadjustment_survivalmode_enemies01.dbr")

def life_base_campaign(cl): return ((cl * 51) ** 1.53) + 2400
def life_base_crucible(cl): return ((cl * 25) ** 1.5) + 100

def arr(a, i): return a[i - 1] if 0 < i <= len(a) else a[-1]

print("\n" + "="*92)
print("SCENARIO 1 — CAMPAIGN, Wightmire Cave, difficulty sweep, player level 100 (1P)")
print("="*92)
aPL = 100
spawn_lo, spawn_hi = (aPL + 2) + aPL // 50, (aPL + 3) + aPL // 50   # lv6_hero
print(f"  lv6_hero spawn = {spawn_lo}-{spawn_hi}; charLevel = spawn+3 = {spawn_lo+3}-{spawn_hi+3}")
for diff, idx in [("Normal", 0), ("Elite", 4), ("Ultimate", 8)]:
    for cl in (spawn_lo + 3, spawn_hi + 3):
        Lb = life_base_campaign(cl)
        ab_life = arr(ab["characterLifeModifier"], cl)
        pak_life = mp["characterLifeModifier"][idx]
        add = Lb * (1 + (ab_life + pak_life) / 100.0)
        mult = Lb * (1 + ab_life / 100.0) * (1 + pak_life / 100.0)
        otdm = arr(ab["offensiveTotalDamageModifier"], cl) + arr(dt["offensiveTotalDamageModifier"], (cl//25)+2) \
               + mp["offensiveTotalDamageModifier"][idx]
        pmin, pmax = arr(dp["offensivePhysicalMin"], cl), arr(dp["offensivePhysicalMax"], cl)
        print(f"  {diff:8s} cl={cl:3d}  base_life={Lb:12,.0f}  armorbase05={ab_life:+.0f}%  pak={pak_life:+.0f}%"
              f"  -> life[additive]={add:12,.0f}  life[mult]={mult:12,.0f}")
        print(f"           {'':11s} baseATK {pmin}-{pmax} phys   netTDM={otdm:+.0f}%"
              f"   retalTDM={mp['retaliationTotalDamageModifier'][idx]:+.0f}%")

print("\n" + "="*92)
print("SCENARIO 2 — CRUCIBLE (Gladiator = Ultimate table), player level 100")
print("="*92)
sp_lo, sp_hi = aPL + 3, (aPL + 3) + aPL // 50   # lv7_uber hero
print(f"  lv7_uber hero spawn = {sp_lo}-{sp_hi}; charLevel = spawn+3 = {sp_lo+3}-{sp_hi+3}")
print("  NOTE: Crucible overrides bio characterLife to ((charLevel*25)^1.5)+100")
for label, wave in [("tier09 w06 (~wave 86)", 86), ("tier14 w02 (~wave 132)", 132)]:
    for dname, rec in [("Aspirant/Normal", sm_n), ("Gladiator/Ultimate", sm_u)]:
        cl = sp_hi + 3
        Lb = life_base_crucible(cl)
        ab_life = arr(ab["characterLifeModifier"], cl)
        w_life = arr(rec["characterLifeModifier"], wave)
        add = Lb * (1 + (ab_life + w_life) / 100.0)
        mult = Lb * (1 + ab_life / 100.0) * (1 + w_life / 100.0)
        w_tdm = arr(rec["offensiveTotalDamageModifier"], wave)
        w_oa, w_da = arr(rec["characterOffensiveAbility"], wave), arr(rec["characterDefensiveAbility"], wave)
        w_ret = arr(rec["retaliationTotalDamageModifier"], wave)
        print(f"  {label:24s} {dname:19s} cl={cl}  base_life={Lb:10,.0f}"
              f"  armorbase05={ab_life:+.0f}%  wave={w_life:+.0f}%"
              f"  -> life[add]={add:11,.0f} life[mult]={mult:11,.0f}")
        print(f"    {'':44s} waveTDM={w_tdm:+.0f}%  +OA={w_oa:.0f} +DA={w_da:.0f}  retalTDM={w_ret:+.0f}%")

print("\n" + "="*92)
print("REFERENCE — Matt's measured campaign fight (Normal, cl 13 / 17 candidates)")
print("="*92)
for cl in (13, 17):
    Lb = life_base_campaign(cl)
    print(f"  cl={cl}: base_life={Lb:,.1f} armorbase05={arr(ab['characterLifeModifier'],cl):+.0f}% "
          f"pakNormal1P={mp['characterLifeModifier'][0]:+.0f}%")
