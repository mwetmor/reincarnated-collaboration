#!/usr/bin/env python3
"""P6 — difficulty/scaling picture for an endgame Primordian re-fight.
(a) base-game difficulty balancing tables (campaign Normal/Elite/Ultimate)
(b) Crucible wave-indexed tables at Primordian's two waves
(c) tier->wave mapping evidence
"""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
base = ArzArchive(ROOT / "database/database.arz")
sm   = ArzArchive(ROOT / "mods/survivalmode/database/SurvivalMode.arz")

print("#"*84); print("# A — base-game balancingadjustment records present"); print("#"*84)
for rp in sorted(base.records):
    if "balancingadjustment" in rp:
        print("  ", rp)

FIELDS = ["characterLifeModifier", "offensiveTotalDamageModifier", "characterOffensiveAbility",
          "characterDefensiveAbility", "characterAttackSpeedModifier", "retaliationTotalDamageModifier",
          "characterOffensiveAbilityModifier", "characterDefensiveAbilityModifier",
          "characterLifeRegenModifier", "characterPercentHealIncreaseModifier"]

print("\n### base: records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
r = base.read_record("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
for f in FIELDS:
    if f in r:
        print(f"  {f:38s} = {r[f]}")
print("  -- non-zero scalar/array fields (all) --")
for k in sorted(r):
    v = r[k]
    if isinstance(v, list):
        if any(x not in (0, 0.0) for x in v):
            print(f"    {k:40s} = {v}")
    elif v not in (0, 0.0, False, ""):
        print(f"    {k:40s} = {v}")

print("\n" + "#"*84); print("# B — Crucible wave-indexed tables at Primordian's waves"); print("#"*84)
TIER_WAVE = {"tier09/w06": (9, 6), "tier14/w02": (14, 2)}
maps = {"Normal": "records/game/balancingadjustment_survivalmode_enemies01.dbr",
        "Elite":  "records/game/balancingadjustment_survivalmode_enemies02.dbr",
        "Ultimate":"records/game/balancingadjustment_survivalmode_enemies03.dbr"}
recs = {d: sm.read_record(p) for d, p in maps.items()}

# candidate absolute wave numbers under the 10-waves-per-tier hypothesis
waves = {"tier09 w06": (9-1)*10 + 6, "tier14 w02": (14-1)*10 + 2}
print(f"hypothesised absolute waves: {waves}")
for f in FIELDS:
    if f not in recs["Normal"] or not isinstance(recs["Normal"][f], list):
        continue
    print(f"\n  --- {f} (array len {len(recs['Normal'][f])}) ---")
    print(f"    {'difficulty':10s} {'w1':>8s} {'w50':>8s} {'w86':>8s} {'w132':>8s} {'w150':>8s} {'last':>8s}")
    for d in ["Normal", "Elite", "Ultimate"]:
        a = recs[d][f]
        def g(i): return a[i-1] if 0 < i <= len(a) else None
        print(f"    {d:10s} {g(1):>8} {g(50):>8} {g(86):>8} {g(132):>8} {g(150):>8} {a[-1]:>8}")

print("\n" + "#"*84); print("# C — tier->wave mapping evidence"); print("#"*84)
# do wave proxies exist beyond w10 in any tier? and are there tier-level container records?
for rp in sorted(sm.records):
    if re.search(r"tier\d+waves?/", rp) and re.search(r"proxy_w(\d+)_p01a\.dbr$", rp):
        pass
tierdirs = sorted({rp.split("/")[2] for rp in sm.records if re.match(r"records/proxies/tier\d+waves/", rp)})
print("tier wave dirs:", tierdirs)
# any record naming waves absolutely?
print("\nrecords mentioning 'wave' outside tierNNwaves:")
for rp in sorted(sm.records):
    if "wave" in rp.lower() and not re.match(r"records/proxies/tier\d+waves/", rp):
        print("   ", rp)
