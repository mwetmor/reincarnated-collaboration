#!/usr/bin/env python3
"""KC2-PM2 Lap B / task 2 -- the OA-vs-DA to-hit + crit (PTH) constants, read from the corpus.

The community documents this formula. This script does NOT trust that: it reads the constants
out of Grim Dawn's own `records/game/combatformulas.dbr` and `records/game/gameengine.dbr`,
so every constant in `hit-math.md` can be graded MEASURED rather than remembered. Where a
constant is NOT in the corpus, the script says so and the grade drops -- it never fills a hole.

Also re-emits per-identity DA/OA for the roster so any gap against tg2_monster_stats.csv is
closed on the same pass.

READ-ONLY.
"""
import sys
import json
import argparse

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm2b_lib_2026_08_12 import E3, roster, num, evaleq, bio_stats, dump_csv

COMBAT = "records/game/combatformulas.dbr"
ENGINE = "records/game/gameengine.dbr"

# Fields this lap asserts are load-bearing for incoming-damage resolution. Anything absent
# from the record is reported ABSENT, never defaulted.
COMBAT_KEYS = [
    "probabilityToHitEquation", "normalPTHEquation",
    "pthMinimum",
    "pthThreshold1", "pthThreshold2", "pthThreshold3",
    "pthThreshold4", "pthThreshold5", "pthThreshold6",
    "pthDamageModifier1", "pthDamageModifier2", "pthDamageModifier3",
    "pthDamageModifier4", "pthDamageModifier5", "pthDamageModifier6",
    "offensiveAbilityEquation", "defensiveAbilityEquation",
    "physicalDamageEquation", "physicalDurationDamageEquation",
    "magicalDamageEquation", "magicalDurationDamageEquation",
    "pierceDamageEquation",
    "physicalDamageDefenseEquationDGP", "physcialDamageDefenseEquationDLEP",
    "meleeBlockEquation", "projectileBlockEquation",
    "shieldDamageReductionEquationDGB", "shieldDamageReductionEquationDLEB",
    "combatRegionHeadChance", "combatRegionTorsoChance", "combatRegionArmsChance",
    "combatRegionLegsChance", "combatRegionShouldersChance", "combatRegionFeetChance",
    "combatRegionUnprotectedChance", "combatRegionFullyProtectedChance",
]
ENGINE_KEYS = [
    "armorDefensiveAbsorption", "absMaxDamageScaling", "damageMagnitude",
    "playerAttackSpeedCapMin", "playerAttackSpeedCapMax",
    "monsterAttackSpeedCapMax", "bossAttackSpeedCapMin", "bossAttackSpeedCapMax",
    "playerRunSpeedCapMin", "playerRunSpeedCapMax",
    "monsterRunSpeedCapMax", "bossRunSpeedCapMin", "bossRunSpeedCapMax",
    "absoluteRunSpeedCapMax", "playerReflectCap", "pvpDamageMultiplier",
    "miniPetLimit", "2hWeaponDamageFactor", "dwWeaponDamageFactor",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outjson", default="/tmp/leg_pm2b/hit_math_constants.json")
    ap.add_argument("--outcsv", default="/tmp/leg_pm2b/tg2_monster_oa_da.csv")
    a = ap.parse_args()

    out = {}
    for path, keys in ((COMBAT, COMBAT_KEYS), (ENGINE, ENGINE_KEYS)):
        rec, own = E3.merged(path)
        blk = {"__record__": path, "__arz_owners__": own, "__n_fields__": len(rec or {})}
        for k in keys:
            blk[k] = rec.get(k, "__ABSENT-FROM-RECORD__") if rec else "__RECORD-UNRESOLVED__"
        out[path] = blk

    with open(a.outjson, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(a.outjson, "written")
    for p, blk in out.items():
        miss = [k for k, v in blk.items() if v == "__ABSENT-FROM-RECORD__"]
        print("  %s  owners=%s fields=%d  ABSENT=%d %s"
              % (p, blk["__arz_owners__"], blk["__n_fields__"], len(miss), miss))

    # ---- per-identity DA/OA, closing any gap against tg2_monster_stats.csv
    rows = []
    for r in roster():
        rec, _ = E3.merged(r["record"])
        lvl = r["level_min"] if r["level_min"] != "" else None
        bp, life, da, oa = bio_stats(rec, lvl)
        # granted-tree passives that move OA/DA (declared, not folded -- gamora rules the fold)
        tree_oa = tree_da = 0.0
        oa_srcs, da_srcs = [], []
        for k, v in rec.items():
            if not (k.startswith("skillName") and isinstance(v, str) and v.lower().endswith(".dbr")):
                continue
            s, _ = E3.merged(v)
            if not s:
                continue
            for fld, acc, src in (("characterOffensiveAbility", "oa", oa_srcs),
                                  ("characterDefensiveAbility", "da", da_srcs)):
                val = s.get(fld)
                if isinstance(val, list):
                    cand = [x for x in val if isinstance(x, (int, float))]
                    val = max(cand) if cand else 0
                if isinstance(val, (int, float)) and val:
                    src.append("%s=%g" % (v.rsplit("/", 1)[-1].replace(".dbr", ""), val))
                    if acc == "oa":
                        tree_oa += float(val)
                    else:
                        tree_da += float(val)
        rows.append(dict(
            record=r["record"], display_name=r["display_name"], stratum=r["stratum"],
            level_used=lvl, bio_record=bp,
            offensive_ability_base=round(oa, 2) if oa is not None else "",
            defensive_ability_base=round(da, 2) if da is not None else "",
            base_life=round(life) if life is not None else "",
            creature_own_oa_flat=num(rec.get("characterOffensiveAbility"), 0.0),
            creature_own_da_flat=num(rec.get("characterDefensiveAbility"), 0.0),
            creature_oa_modifier_pct=num(rec.get("characterOffensiveAbilityModifier"), 0.0),
            creature_da_modifier_pct=num(rec.get("characterDefensiveAbilityModifier"), 0.0),
            tree_oa_flat_sum=round(tree_oa, 2), tree_da_flat_sum=round(tree_da, 2),
            tree_oa_sources="|".join(oa_srcs), tree_da_sources="|".join(da_srcs),
            grade=("MEASURED" if oa is not None and da is not None else "BIO-EQ-UNEVALUABLE"),
        ))
    dump_csv(a.outcsv, rows)
    n_ok = sum(1 for r in rows if r["grade"] == "MEASURED")
    print("OA/DA MEASURED on %d/%d identities" % (n_ok, len(rows)))


if __name__ == "__main__":
    main()
