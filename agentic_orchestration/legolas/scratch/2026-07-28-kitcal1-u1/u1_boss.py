#!/usr/bin/env python3
"""SCRATCH (U-1) — resolve a GD monster's stat block at a given charLevel.

Implements the G-5a five-record chain:
  monster.characterAttributeEquations -> bio_*.dbr  (attribute equations in charLevel)
  monster.skillNameN @ skillLevelN(charLevel) -> nonplayerskills passives (rank arrays)
  gameengine.monsterAttributePak -> balancingadjustment_mp+difficulty_enemies01 [Normal/1P = idx 0]
Read-only.
"""
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import u1_lib as U  # noqa: E402

PAK = "records/game/balancingadjustment_mp+difficulty_enemies01.dbr"
IDX = 0  # Normal, 1 player


def ev(eq, charLevel):
    """Evaluate a GD equation string in charLevel."""
    if isinstance(eq, (int, float)):
        return float(eq)
    s = eq.replace("^", "**").replace("charLevel", str(charLevel))
    s = s.replace("averagePlayerLevel", str(charLevel))
    return float(eval(s, {"__builtins__": {}}, {"math": math}))


def pak():
    _, _, _, f = U.rec(PAK)
    return {k: (v[IDX] if isinstance(v, list) else v) for k, v in f.items()}


def resolve(path, charLevel, verbose=True):
    _, rel, rtype, m = U.rec(path)
    assert m, path
    bio_path = m["characterAttributeEquations"]
    _, biorel, _, bio = U.rec(bio_path)
    P = pak()

    out = {"record": path, "src": rel, "charLevel": charLevel, "bio": bio_path}
    base = {}
    for k in ("characterLife", "characterMana", "characterStrength", "characterDexterity",
              "characterIntelligence", "characterOffensiveAbility", "characterDefensiveAbility"):
        if k in bio:
            base[k] = ev(bio[k], charLevel)
    out["bio_values"] = base

    # ranked passives
    skills = []
    for i in range(1, 25):
        n = m.get(f"skillName{i}")
        if not n:
            continue
        lvl_eq = m.get(f"skillLevel{i}", 1)
        rank = int(ev(lvl_eq, charLevel))
        _, srel, srt, sf = U.rec(n)
        skills.append({"i": i, "record": n, "rank": rank, "class": (sf or {}).get("Class"),
                       "levelEq": lvl_eq, "fields": sf})
    out["skills"] = [{k: v for k, v in s.items() if k != "fields"} for s in skills]

    # additive pools from Skill_Passive only
    lifeMod = 0.0
    tdm = 0.0
    armor = 0.0
    dmg = {}
    for s in skills:
        if s["class"] != "Skill_Passive":
            continue
        sf = s["fields"]
        r = s["rank"]
        lifeMod += U.at(sf, "characterLifeModifier", r) or 0 if not isinstance(
            U.at(sf, "characterLifeModifier", r), tuple) else 0
        v = U.at(sf, "offensiveTotalDamageModifier", r)
        tdm += v if isinstance(v, (int, float)) else 0
        v = U.at(sf, "defensiveProtection", r)
        armor += v if isinstance(v, (int, float)) else 0
        for k in sf:
            if k.startswith("offensive") and (k.endswith("Min") or k.endswith("Max")):
                v = U.at(sf, k, r)
                if isinstance(v, (int, float)) and v:
                    dmg[k] = dmg.get(k, 0) + v

    pakLife = P.get("characterLifeModifier", 0)
    pakLifeMult = P.get("characterLifeMultModifier", 0)
    pakTdm = P.get("offensiveTotalDamageModifier", 0)

    life = base["characterLife"] * (1 + (lifeMod + pakLife) / 100) * (1 + pakLifeMult / 100)
    mana = base["characterMana"]
    out["skill_lifeMod_pct"] = lifeMod
    out["pak_lifeMod_pct"] = pakLife
    out["life"] = life
    out["mana"] = mana
    out["life_plus_mana"] = life + mana
    out["armor"] = armor + (m.get("defensiveProtection", 0) or 0)
    out["tdmMult"] = (1 + tdm / 100) * (1 + pakTdm / 100)
    out["damage_pools"] = dmg

    dex = base.get("characterDexterity", 0) * (1 + P.get("characterDexterityModifier", 0) / 100)
    strn = base.get("characterStrength", 0) * (1 + P.get("characterStrengthModifier", 0) / 100)
    out["OA"] = (base.get("characterOffensiveAbility", 0) + charLevel * 12 + dex * 0.5) * \
        (1 + P.get("characterOffensiveAbilityModifier", 0) / 100) + \
        P.get("characterOffensiveAbility", 0) + 53
    out["DA"] = (base.get("characterDefensiveAbility", 0) + charLevel * 12 + strn * 0.5) * \
        (1 + P.get("characterDefensiveAbilityModifier", 0) / 100) + \
        P.get("characterDefensiveAbility", 0) + 53

    res = {k: v for k, v in m.items()
           if k.startswith("defensive") and isinstance(v, (int, float)) and v}
    out["record_resistances"] = res
    out["attackSpeed"] = (m.get("characterAttackSpeed", 1.0) or 1.0) * \
        (1 + P.get("characterAttackSpeedModifier", 0) / 100)
    out["runSpeed"] = (m.get("characterRunSpeed", 1.0) or 1.0) * \
        (1 + P.get("characterRunSpeedModifier", 0) / 100)

    if verbose:
        print(f"\n===== {path}  @ charLevel {charLevel}   ({rel})")
        print(f"  bio: {bio_path}")
        for k, v in base.items():
            print(f"    {k:<28} = {v:.2f}")
        print(f"  skill passives:")
        for s in out["skills"]:
            print(f"    [{s['i']:>2}] rank {s['rank']:<4} {s['class']:<28} {s['record']}")
        print(f"  lifeMod skills {lifeMod:+.0f}%  pak {pakLife:+.0f}%  pakMult {pakLifeMult:+.0f}%")
        print(f"  LIFE {life:,.0f}   MANA {mana:,.0f}   LIFE+MANA {life+mana:,.0f}")
        print(f"  armor {out['armor']:.0f}  tdmMult {out['tdmMult']:.3f}  "
              f"OA {out['OA']:.0f}  DA {out['DA']:.0f}")
        print(f"  dmg pools {dmg}")
        print(f"  resistances {res}")
    return out


if __name__ == "__main__":
    p = sys.argv[1]
    for L in [int(x) for x in sys.argv[2:]] or [13]:
        resolve(p, L)
