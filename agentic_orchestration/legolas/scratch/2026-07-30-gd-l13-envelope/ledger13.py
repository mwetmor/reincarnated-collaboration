#!/usr/bin/env python3
"""NON-PRODUCTION SCRATCH — L13 ledger with the CORRECTED (multiplicative) life rule.
The pak's characterLifeModifier is a SEPARATE multiplicative stage, not an additive
term in the skill-passive pool. Adjudicated against the MEASURED Primordian pool
(15,822 @ player L13, from the .gdc play_stats block).
"""
import importlib.util, pathlib, sys
_s = importlib.util.spec_from_file_location("g5a",
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
    "legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(_s); _s.loader.exec_module(R)

_orig = R.resolve
def resolve(mpath, spawn):
    r = _orig(mpath, spawn)
    t = r["hp_terms"]
    # CORRECTED: skill pool and pak are separate multiplicative stages
    r["hp_additive"] = r["hp"]
    r["hp"] = (t["bioBase"] + t["flat"]) * (1 + t["skillModPct"]/100.0) \
                                        * (1 + t["pakModPct"]/100.0) \
                                        * (1 + t["pakMultPct"]/100.0)
    return r

ROSTER = [
 # (label, record, spawn level at aPL13)
 ("Walking Dead",        "records/creatures/enemies/zombie_a01.dbr", 12),
 ("Walking Dead",        "records/creatures/enemies/zombie_a01.dbr", 13),
 ("Wretcher",            "records/creatures/enemies/zombie_b02h.dbr", 13),
 ("Plague Walker",       "records/creatures/enemies/zombie_g01.dbr", 13),
 ("Rotting Soldier",     "records/creatures/enemies/zombie_soldiera01.dbr", 13),
 ("Tainted Hound",       "records/creatures/enemies/zombiehound_a01.dbr", 13),
 ("Corruption",          "records/creatures/enemies/gazer_a01.dbr", 13),
 ("Ghoul",               "records/creatures/enemies/ghoul_a01.dbr", 13),
 ("Stonetusk",           "records/creatures/enemies/boar_a01.dbr", 13),
 ("Gargantuan Stonetusk","records/creatures/enemies/boar_a02.dbr", 13),
 ("Scavenger",           "records/creatures/enemies/scavenger_a01.dbr", 13),
 ("Rifthound",           "records/creatures/enemies/rifthound_swamp_a01.dbr", 13),
 ("Cronley's Lackey",    "records/creatures/enemies/humanoutlaw_melee_a01.dbr", 13),
 ("Bloodsworn Adulant",  "records/creatures/enemies/humanchthonic_cultist_a01.dbr", 13),
 ("Rift Scourge",        "records/creatures/enemies/prawn_a01.dbr", 13),
 ("Dreadweave Arachnid", "records/creatures/enemies/spidergianta_a01.dbr", 13),
 ("Boneback Gnasher",    "records/creatures/enemies/bonerat_meleea01.dbr", 13),
 ("Skeletal Warrior",    "records/creatures/enemies/skeleton_a01.dbr", 13),
 ("-- CHAMPION --", None, None),
 ("Fleshwarped Butcher", "records/creatures/enemies/zombiemutated_a01.dbr", 14),
 ("Fury",                "records/creatures/enemies/zombie_c01.dbr", 14),
 ("Ironhide Stonetusk",  "records/creatures/enemies/boar_b01.dbr", 14),
 ("-- HERO --", None, None),
 ("Dreadtusk",           "records/creatures/enemies/hero/boar_h01.dbr", 16),
 ("Abner",               "records/creatures/enemies/hero/zombie_h01.dbr", 16),
 ("Charrus",             "records/creatures/enemies/hero/rifthound_h01.dbr", 16),
 ("-- BOSS --", None, None),
 ("Primordian (MEASURED anchor 15,822)",
                         "records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr", 15),
 ("Warden Krieg ph.1",   "records/creatures/enemies/boss&quest/warden01.dbr", 16),
 ("Warden Krieg ph.2",   "records/creatures/enemies/boss&quest/warden02.dbr", 16),
]

PLAYER_HP_HUMAN, PLAYER_HP_WERE = 759.0, 1600.0
PLAYER_DPS_LO, PLAYER_DPS_HI = 370.0, 530.0   # 310/hit x 1.2-1.7 hits/s

print(f"{'name':38s} {'charL':>5s} {'HP(new)':>9s} {'HP(g5a)':>9s} {'dmg/hit':>12s} "
      f"{'%759':>6s} {'%1600':>6s} {'run':>5s} {'TTK_lo':>7s} {'TTK_hi':>7s}")
tot = {}
for label, path, spawn in ROSTER:
    if path is None:
        print(f"--- {label}")
        continue
    try: r = resolve(path, spawn)
    except KeyError:
        print(f"{label:38s}  MISSING"); continue
    dmid = (r["dmg_min"] + r["dmg_max"]) / 2
    ttk_lo = r["hp"] / PLAYER_DPS_HI
    ttk_hi = r["hp"] / PLAYER_DPS_LO
    print(f"{label:38s} {r['charLevel']:5d} {r['hp']:9.0f} {r['hp_additive']:9.0f} "
          f"{r['dmg_min']:5.0f}-{r['dmg_max']:<6.0f} "
          f"{100*dmid/PLAYER_HP_HUMAN:5.1f}% {100*dmid/PLAYER_HP_WERE:5.1f}% "
          f"{r['runSpeed_eff']:5.2f} {ttk_lo:6.1f}s {ttk_hi:6.1f}s")
    tot[label] = r["hp"]

w = tot.get("Warden Krieg ph.1", 0) + tot.get("Warden Krieg ph.2", 0)
print(f"\nWarden Krieg COMBINED (ph.1+ph.2) HP = {w:,.0f}")
print(f"  boss:player HP ratio  vs 759  = {w/PLAYER_HP_HUMAN:.1f}x")
print(f"  boss:player HP ratio  vs 1600 = {w/PLAYER_HP_WERE:.1f}x")
print(f"  fight duration @ {PLAYER_DPS_LO:.0f}-{PLAYER_DPS_HI:.0f} HP/s = "
      f"{w/PLAYER_DPS_HI:.0f}-{w/PLAYER_DPS_LO:.0f} s")
print(f"\nPlayer run speed (malepc01.characterRunSpeed) = 0.93 (no Normal pak modifier)")
