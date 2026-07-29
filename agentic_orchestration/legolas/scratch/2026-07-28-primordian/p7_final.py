#!/usr/bin/env python3
"""P7 — close the remaining gaps:
 (a) full head of the base-vs-survivalmode monster diff (charLevel? skills? classification?)
 (b) characterLifeMultModifier + other MULTIPLICATIVE terms in the Crucible wave tables
 (c) campaign Ultimate composed stat picture for Primordian
 (d) does survivalmode override lv6/lv7 variance eq, bio, or armorbase05?
"""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
base = ArzArchive(ROOT / "database/database.arz")
sm   = ArzArchive(ROOT / "mods/survivalmode/database/SurvivalMode.arz")
MON = "records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr"

print("#"*80); print("# A — key identity/scaling fields, base vs Crucible override"); print("#"*80)
b, s = base.read_record(MON), sm.read_record(MON)
KEYS = ["Class", "monsterClassification", "charLevel", "minLevel", "maxLevel", "experiencePoints",
        "characterAttributeEquations", "controller", "description", "FileDescription",
        "numAttackSlots", "numDefenseSlots", "healthGainOnKillPct", "Difficulty",
        "defensiveCold", "defensivePoison", "defensiveFreeze", "defensiveKnockdown",
        "onDie", "factions", "dropItems", "giveXP"]
print(f"{'field':36s} {'BASE':>34s} | CRUCIBLE")
for k in KEYS:
    print(f"  {k:34s} {str(b.get(k,'<absent>')):>34s} | {s.get(k,'<absent>')}")
print("\nskillName* wiring:")
for i in range(1, 14):
    kn, kl = f"skillName{i}", f"skillLevel{i}"
    if kn in b or kn in s:
        print(f"  {kn:14s} base={str(b.get(kn,'-')).split('/')[-1]:44s} [{b.get(kl,'-')}]")
        print(f"  {'':14s} cruc={str(s.get(kn,'-')).split('/')[-1]:44s} [{s.get(kl,'-')}]")

print("\n" + "#"*80); print("# B — multiplicative + remaining terms, Crucible wave tables"); print("#"*80)
maps = {"Normal": "records/game/balancingadjustment_survivalmode_enemies01.dbr",
        "Elite":  "records/game/balancingadjustment_survivalmode_enemies02.dbr",
        "Ultimate":"records/game/balancingadjustment_survivalmode_enemies03.dbr"}
recs = {d: sm.read_record(p) for d, p in maps.items()}
for f in ["characterLifeMultModifier", "characterLife", "characterRunSpeedModifier",
          "defensiveAbsorptionModifier", "characterDefensiveBlockRecoveryReduction",
          "defensivePhysical", "defensiveCold", "defensiveAether", "defensiveChaos"]:
    n = recs["Normal"].get(f, "<absent>")
    if isinstance(n, list):
        print(f"\n  --- {f} ---")
        for d in ["Normal", "Elite", "Ultimate"]:
            a = recs[d][f]
            def g(i): return a[i-1] if 0 < i <= len(a) else None
            print(f"    {d:9s} w1={g(1):>7} w86={g(86):>7} w132={g(132):>7} w150={g(150):>7}")
    else:
        print(f"  {f:42s} scalar/absent -> {n}")

print("\n" + "#"*80); print("# C — campaign difficulty index map + composed campaign picture"); print("#"*80)
mp = base.read_record("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
print("  12-entry arrays = 3 difficulties x 4 player-counts. 1P indices: Normal=0, Elite=4, Ultimate=8")
for f in ["characterLifeModifier", "characterLifeMultModifier", "offensiveTotalDamageModifier",
          "retaliationTotalDamageModifier", "characterOffensiveAbility", "characterDefensiveAbility",
          "characterAttackSpeedModifier", "characterRunSpeedModifier", "defensiveCold", "defensiveFreeze"]:
    a = mp[f]
    print(f"  {f:34s} Normal1P={a[0]:>8} Elite1P={a[4]:>8} Ultimate1P={a[8]:>8}")

print("\n" + "#"*80); print("# D — survivalmode overrides of the scaling substrate?"); print("#"*80)
for rp in ["records/proxies/lv6_hero.dbr", "records/proxies/lv7_uber hero.dbr",
           "records/creatures/enemies/bios/bio_boss_standard_01.dbr",
           "records/skills/nonplayerskills/passive/armorbase05.dbr",
           "records/skills/nonplayerskills/passive/damagebase_physical04.dbr",
           "records/skills/nonplayerskills/bossskills/primordian_icearmor.dbr"]:
    print(f"  {'PRESENT (override)' if rp in sm.records else 'absent (inherits base)':24s} {rp}")

print("\nbio_boss_standard_01 (base) equations:")
bio = base.read_record("records/creatures/enemies/bios/bio_boss_standard_01.dbr")
for k in sorted(bio):
    if k.startswith("character"):
        print(f"    {k:34s} = {bio[k]}")
