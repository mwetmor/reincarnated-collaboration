#!/usr/bin/env python3
"""KC2-PM4 Lap M shared library -- THE DEATH-MECHANISM DECODE (ruling R-PM4-32).

READ-ONLY on the vendor corpus.  OUTCOME-FIREWALLED: reads NO sim output, NO findings JSON, NO
gamora landing note, NO baton produced after the frozen roster roll.  The single baton read is the
FROZEN roster roll `kc2-baton-v1-E-s09-cp150-20260809_052836.json` (a ROSTER basis: which record
was drawn at which wave), the same basis Laps D and I used.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE QUESTION
═══════════════════════════════════════════════════════════════════════════════════════════════
Lap K measured the referent's death: 20,005 HP (the FULL buffed pool) removed inside 0.0834 s,
from full health, on wave 160.  17,887 of it landed in a SINGLE 60 fps frame (16.7 ms).

This lap asks the tables: WHICH BODY, WITH WHICH SKILL, CAN DELIVER >= 20,005 POST-MITIGATION
DAMAGE TO THE DECODED PLAYER DEFENCE SHEET IN <= 1 SIM TICK, as a single hit or as a
geometrically-co-landing volley?  If none can, that null is the finding, and the maximum any
candidate CAN deliver is reported instead.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE ATTACK CHAIN, DECODED (every term names its record + field + index)
═══════════════════════════════════════════════════════════════════════════════════════════════

  flat(type, rank)   skill record's `offensive<TYPE>Min|Max`, read at the rank the body's own
                     `skillLevel{i}` equation yields at its pool charLevel  [MEASURED]

  attribute scaling  records/game/combatformulas.dbr
                       physicalDamageEquation = physicalDamageDV*((dexterityDV/245)+1)
                       pierceDamageEquation   = pierceDamageDV  *((dexterityDV/245)+1)
                       magicalDamageEquation  = magicalDamageDV *((intelligenceDV/215)+1)
                     dexterity / intelligence from the body's `characterAttributeEquations` bio
                     evaluated at charLevel                                  [MEASURED]

  total-damage mod   ultimate pak [8] (+40) + survival_enemies03[w-1] (+43 @ w160) + the body's
                     OWN `offensiveTotalDamageModifier` passives             [Lap I, MEASURED]
                     composition ADDITIVE-BY-PARALLEL (Lap I S 1.4 grade, carried)

  per-type mod       survival_enemies03.offensive<T>Modifier[w-1] + ultimate pak + the body's own
                     `offensive<T>Modifier` passives                          [MEASURED]

  crit               probabilityToHitEquation(body OA, player DA 2591) -> pthThreshold1..6 ->
                     pthDamageModifier1..6, floored at pthMinimum = 55        [MEASURED law]
                     body OA via combatformulas.offensiveAbilityEquation

  range scale        `projectileDamageRange1..3Scale` -- the projectile's own distance falloff;
                     band 1 is melee-adjacent, which is where an Eye-of-Reckoning player stands.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE PLAYER DEFENCE SHEET (Lap A, camera-MEASURED off the referent's own character sheet)
═══════════════════════════════════════════════════════════════════════════════════════════════
  HP 20,005 (buffed; post-death max 18,065 -> the killing blow had to overcome 20,005)
  Armour 3,557 @ 70.0 % absorption (`gameengine.armorDefensiveAbsorption`, closed at Lap L)
  DA 2,591
  Resists  physical 16 · pierce 80 · fire 80 · cold 80 · lightning 80 · acid/poison 80 ·
           vitality 80 · aether 80 · chaos 80 · bleeding 85
  Life-leech resist -25 (NEGATIVE: enemy life leech is AMPLIFIED 25 % against this player)
  Block 0 · Dodge 0 · Deflect 0 -- no avoidance layer exists on this build

  armour law, verbatim from `records/game/combatformulas.dbr`:
     dmg <= armour :  dmg * (1 - absorption)
     dmg >  armour :  armour * (1 - absorption) + (dmg - armour)

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap M (ruling R-PM4-32).
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import math
import pathlib
import sys
from typing import Dict, List, Optional, Sequence, Set, Tuple

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4i_lib_2026_08_13 import (                                            # noqa: E402
    E3, ev, skill_closure, creature_skill_slots, own_total_damage_modifier,
    pool_population, level_sets, rolled_actors, surv_at, survival_arrays,
    difficulty_pak, _idx, summon_closure_extended, is_body,
)

WAVE_OF_DEATH = 160
WAVES = (159, 160)

# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE PLAYER DEFENCE SHEET -- MEASURED (Lap A `measured-player-sheet.csv`) + Lap L absorption
# ══════════════════════════════════════════════════════════════════════════════════════════════
PLAYER = dict(
    hp_buffed=20005,          # the pool the killing blow had to overcome (Lap K)
    hp_unbuffed=18065,
    armor=3557.0,
    armor_absorption=0.70,    # gameengine.armorDefensiveAbsorption = 70.0  (Lap L, MEASURED)
    DA=2591.0,
)
#: player resistance %, by the damage stem used in the `offensive<STEM>Min` field names
PLAYER_RES = {
    "Physical": 16.0,
    "Pierce": 80.0,
    "Fire": 80.0,
    "Cold": 80.0,
    "Lightning": 80.0,
    "Poison": 80.0,       # `DefensePoison` = "Poison & Acid Resistance"; the INSTANT family is Acid
    "Life": 80.0,         # vitality
    "Aether": 80.0,
    "Chaos": 80.0,
    "Elemental": 80.0,    # splits fire/cold/lightning in thirds -- all three are 80 here
}
#: which attribute equation scales which family (combatformulas.dbr, MEASURED)
ATTR_SCALE = {
    "Physical": "dex", "Pierce": "dex",
    "Fire": "int", "Cold": "int", "Lightning": "int", "Poison": "int",
    "Life": "int", "Aether": "int", "Chaos": "int", "Elemental": "int",
}
INSTANT_STEMS = ("Physical", "Pierce", "Fire", "Cold", "Lightning", "Poison",
                 "Life", "Aether", "Chaos", "Elemental")

#: ⚑ DEFECT D-M-1, CAUGHT AND BANKED.  The first emission of this lap treated
#: `offensiveLifeLeechMin` as a DAMAGE family (it sits beside the others in the same field
#: namespace, it has a player-side "Life Leech Resistance" of -25 %, and at rank 28 the Kymon
#: nemesis carries 3,000 of it).  Composed, it produced a 60,876 post-mitigation basic attack --
#: an instant kill from a white hit, every 1.4 s.  The game's OWN text settles it:
#:     Text_EN.arc :: tags_ui.txt
#:       DamageLifeLeech          = "{%t0}% of Attack Damage converted to Health"   <- ATTACKER heal
#:       DamageDurationLifeLeach  = " Life Leech"                                   <- the DoT
#: The INSTANT `offensiveLifeLeech*` family is the attacker's LEECH PERCENTAGE, not damage dealt
#: to the target.  It is excluded here and named, and the player's -25 % Life Leech Resistance
#: applies to the `offensiveSlowLifeLeach*` DoT family instead (Lap I's limb, not this one).
EXCLUDED_NOT_DAMAGE = {
    "LifeLeech": "tags_ui DamageLifeLeech = '% of Attack Damage converted to Health' -- "
                 "attacker-side leech, NOT damage to the target",
    "ManaBurnDrain": "energy, not health",
    "Stun": "control, not damage",
    "Confusion": "control, not damage",
    "Disruption": "skill disruption, not damage",
    "Fumble": "to-hit debuff, not damage",
    "Convert": "charm, not damage",
    "Freeze": "control, not damage",
    "Petrify": "control, not damage",
}

# ══════════════════════════════════════════════════════════════════════════════════════════════
# combatformulas.dbr -- read, never spelled
# ══════════════════════════════════════════════════════════════════════════════════════════════
_CF: Optional[dict] = None


def combatformulas() -> dict:
    global _CF
    if _CF is None:
        r, _ = E3.winner("records/game/combatformulas.dbr")
        if r is None:
            raise RuntimeError("combatformulas.dbr absent")
        _CF = r
    return _CF


def pth(oa: float, da: float) -> float:
    """probabilityToHitEquation, verbatim from combatformulas.dbr."""
    return ((((oa / ((da / 3.5) + oa)) * 300) * 0.3)
            + (((((oa * 3.25) + 10000) - (da * 3.25)) / 100) * 0.7)) - 50


def pth_effective(oa: float, da: float) -> float:
    cf = combatformulas()
    return max(float(cf["pthMinimum"]), pth(oa, da))


def crit_tier(p: float) -> Tuple[int, float]:
    """`(tier, multiplier)` from the six pthThreshold / pthDamageModifier slots."""
    cf = combatformulas()
    tier, mult = 0, 1.0
    for i in range(1, 7):
        if p >= float(cf[f"pthThreshold{i}"]):
            tier, mult = i, float(cf[f"pthDamageModifier{i}"])
    return tier, mult


def hit_chance(p: float) -> float:
    return min(1.0, p / 70.0)          # normalPTHEquation = probabilityToHitDV/70


def armor_law(raw_physical: float, armor: float, absorption: float) -> float:
    """physcialDamageDefenseEquationDLEP / physicalDamageDefenseEquationDGP, verbatim."""
    if raw_physical <= armor:
        return raw_physical * (1.0 - absorption)
    return armor * (1.0 - absorption) + (raw_physical - armor)


def applied_to_player(stem: str, raw: float) -> float:
    """Post-mitigation damage of one family against the MEASURED player defence sheet."""
    if raw <= 0:
        return 0.0
    if stem == "Physical":
        after = armor_law(raw, PLAYER["armor"], PLAYER["armor_absorption"])
        return after * max(0.0, 1.0 - PLAYER_RES["Physical"] / 100.0)
    res = PLAYER_RES[stem]
    return raw * max(0.0, 1.0 - res / 100.0)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# Per-body attribute + ability decode
# ══════════════════════════════════════════════════════════════════════════════════════════════
def bio_of(record: str) -> Optional[dict]:
    r, _ = E3.winner(record)
    if not r:
        return None
    b = r.get("characterAttributeEquations")
    if isinstance(b, list):
        b = b[0] if b else None
    if not isinstance(b, str):
        return None
    br, _ = E3.winner(b.lower().replace("\\", "/"))
    return br


def bio_path(record: str) -> str:
    r, _ = E3.winner(record)
    b = (r or {}).get("characterAttributeEquations")
    if isinstance(b, list):
        b = b[0] if b else None
    return (b or "").lower().replace("\\", "/")


def _ev(expr, L: float) -> float:
    try:
        return float(ev(expr, L))
    except Exception:
        return 0.0


def skill_stat_sum(record: str, L: float, field: str) -> float:
    """SIGMA over the body's OWN depth-0 skill slots of `field` read at that slot's rank."""
    total = 0.0
    for sn, sl in creature_skill_slots(record):
        s, _ = E3.winner(sn)
        if not s:
            continue
        v = s.get(field)
        if v is None:
            continue
        if isinstance(v, list):
            if not any(v):
                continue
            rank = int(_ev(sl, L)) if sl is not None else 1
            i, _st = _idx(v, rank)
            total += float(v[i])
        elif v:
            total += float(v)
    return total


def body_stats(record: str, L: float, wave: int, surv: Dict[str, List[float]],
               pak: Dict[str, List[float]]) -> dict:
    """Attributes + Offensive Ability of one body at one level and one wave, per the game's own
    `offensiveAbilityEquation`."""
    bio = bio_of(record) or {}
    dex = _ev(bio.get("characterDexterity"), L) + skill_stat_sum(record, L, "characterDexterity")
    inte = _ev(bio.get("characterIntelligence"), L) + skill_stat_sum(record, L, "characterIntelligence")
    oa_base = _ev(bio.get("characterOffensiveAbility"), L)
    oa_skill = skill_stat_sum(record, L, "characterOffensiveAbility")
    oa_wave = surv_at(surv["characterOffensiveAbility"], wave) if "characterOffensiveAbility" in surv else 0.0
    oa_ult = pak["characterOffensiveAbility"][8] if "characterOffensiveAbility" in pak else 0.0
    mod_skill = skill_stat_sum(record, L, "characterOffensiveAbilityModifier")
    mod_wave = surv_at(surv["characterOffensiveAbilityModifier"], wave) if "characterOffensiveAbilityModifier" in surv else 0.0
    mod_ult = pak["characterOffensiveAbilityModifier"][8] if "characterOffensiveAbilityModifier" in pak else 0.0
    oa_sum = oa_base + oa_skill + oa_wave + oa_ult + (L * 12) + (dex * 0.5)
    oa = oa_sum * (1 + (mod_skill + mod_wave + mod_ult) / 100.0) + 53
    return dict(dex=dex, intel=inte, oa=oa, oa_base=oa_base, oa_skill=oa_skill,
                oa_wave=oa_wave, oa_ult=oa_ult,
                oa_mod_pct=mod_skill + mod_wave + mod_ult, bio=bio_path(record))


def attr_mult(stem: str, dex: float, intel: float) -> float:
    return (1 + dex / 245.0) if ATTR_SCALE[stem] == "dex" else (1 + intel / 215.0)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# Skill damage read
# ══════════════════════════════════════════════════════════════════════════════════════════════
def read_at_rank(v, rank: int) -> Tuple[Optional[float], str, str]:
    if v is None:
        return None, "", ""
    if isinstance(v, list):
        if not any(v):
            return None, "", ""
        i, st = _idx(v, rank)
        return float(v[i]), str(i), st
    return (float(v), "", "SCALAR") if v else (None, "", "")


def skill_instant_damage(skill: str, rank: int) -> Dict[str, Tuple[float, float, str, str]]:
    """`{stem -> (min, max, array_index, index_state)}` for every INSTANT damage family present."""
    s, _arc = E3.winner(skill)
    if not s:
        return {}
    out: Dict[str, Tuple[float, float, str, str]] = {}
    for stem in INSTANT_STEMS:
        mn, imn, stmn = read_at_rank(s.get(f"offensive{stem}Min"), rank)
        mx, imx, stmx = read_at_rank(s.get(f"offensive{stem}Max"), rank)
        if mn is None and mx is None:
            continue
        lo = mn if mn is not None else mx
        hi = mx if mx is not None else mn
        out[stem] = (float(lo), float(hi), imn or imx, stmn or stmx)
    return out


def sha256_of(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def dump_csv(path: pathlib.Path, rows: Sequence[dict], cols: Sequence[str]) -> str:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cols))
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    return sha256_of(path)
