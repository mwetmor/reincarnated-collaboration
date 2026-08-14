#!/usr/bin/env python3
"""KC2-PM4 Lap O shared library -- THE TRASH-BOARD DECODE + OA/DA BOTH SIDES OF THE SCREEN.

READ-ONLY on the vendor corpus.  OUTCOME-FIREWALLED: the ONLY key read out of the i14 findings
JSON is the data-gate HALT LIST (`⚑ data_gate.⚑ halted_records` + `attr_measured_records` +
the four record/actor counts).  No scorecard, no verdict, no l4l, no death field is opened.

═══════════════════════════════════════════════════════════════════════════════════════════════
PART A -- THE TRASH BOARD
═══════════════════════════════════════════════════════════════════════════════════════════════
Prior laps decoded bosses / heroes / nemeses.  The TRASH board -- the `records/creatures/enemies/
*_a01 / _b01 / _c01` commons, the `devotion/` and `hero/` champions, the `bounties/` bodies --
was never in scope, and the simulation's own data gate says so: 154 of 169 records carry NO
measured attribute term, 104 of 169 carry no measured own-total-damage term.

Two terms per body, both from the body's OWN records:

  1. ATTRIBUTES.  `<creature>.characterAttributeEquations` -> a `bio_*.dbr` carrying
     `characterDexterity` / `characterIntelligence` / `characterStrength` as charLevel
     EQUATIONS.  Evaluated at the body's spawn level.  Plus `Σ_i skill_i.characterDexterity`
     over the body's own depth-0 skill slots at each slot's own rank.
     ⚑ THE PRIOR GAP EXPLAINED: the attribute terms are NOT on the creature record.  They are
       one hop away, on the bio the creature POINTS AT.  An extractor that reads the creature
       record and stops finds nothing -- which is exactly the 15-of-169 pattern the gate reports.

  2. OWN TOTAL-DAMAGE PASSIVES.  `Σ_i skill_i.offensiveTotalDamageModifier[rank_i(L)-1]` over
     the body's own depth-0 `skillName{i}` slots (Lap I's `own_total_damage_modifier`, imported).
     A body with no such slot is an honest ABSENT -- reported as 0.0 with EVERY skill record
     checked named, never imputed.

═══════════════════════════════════════════════════════════════════════════════════════════════
PART B -- OA / DA, BOTH DIRECTIONS
═══════════════════════════════════════════════════════════════════════════════════════════════
The game's own equations, verbatim from `records/game/combatformulas.dbr`:

  offensiveAbilityEquation =
     (offensiveAbilityDV + (characterLevelDV*12) + ((dexterityDV + bonusDV)*0.5))
       * (1 + (offensiveAbilityModifierDV/100)) + 53
  defensiveAbilityEquation =
     (defensiveAbilityDV + (characterLevelDV*12) + ((strengthDV + bonusDV)*0.5))
       * (1 + (defensiveAbilityModifierDV/100)) + 53
  probabilityToHitEquation =
     ((((OA/((DA/3.5)+OA))*300)*0.3) + (((((OA*3.25)+10000)-(DA*3.25))/100)*0.7)) - 50
  pthMinimum = 55
  pthThreshold1..6  = 70 / 90 / 105 / 120 / 130 / 135
  pthDamageModifier1..6 = 1.0 / 1.1 / 1.2 / 1.3 / 1.4 / 1.5
  normalPTHEquation = probabilityToHitDV / 70

THE ROLL MODEL, and exactly how much of it is documented
--------------------------------------------------------
grimdawn.com/guide/gameplay/combat (accessed 2026-08-14) states, verbatim:
  * the PTH equation above, character-for-character identical to the record;
  * "PTH cannot go below 55 for you or your enemies, meaning that no matter how much Defensive
     Ability you or your foe may have, you will never have a lower than 55% chance to hit them";
  * "At PTH 100 and above, you cannot miss your target";
  * "If your PTH is lower than 70, any attacks that land will do reduced damage.  The damage
     reduction multiplier is equal to your PTH / 70 (ex. if your PTH is 65, you will do 92.86%
     of normal damage on a hit, or 65/70)";
  * "When your PTH reaches 90 and beyond, you will begin to see critical hits."
The community mechanics writeups (Grim Dawn Wiki `Game_Mechanics`; Steam `Grim Dawn - Game
Mechanics Guide` id 596728673) add the roll itself: a uniform 1..100 roll decides hit/crit, and
"the chance to critically strike is PTH - 90" (PTH 95 -> 5 % crit; PTH 110 -> 20 % crit).

  ⚑ GRADE.  The following are MEASURED-OR-DOCUMENTED:
       PTH equation (record AND official guide, identical)
       pthMinimum 55 (record AND guide)
       hit chance = min(1, PTH/100), floor 55 % (guide, stated twice)
       sub-70 damage scalar = PTH/70 (guide, with a worked example)
       tier-1 crit mass = PTH - 90 (wiki/Steam, with two worked examples;
                                    the record's pthThreshold2 = 90 agrees)
       the six thresholds and the six multipliers (record)
  ⚑ The following is DERIVED-BY-PARALLEL, NOT measured:
       that the SAME "mass = PTH - T_k" rule extends to T_3..T_6 (105/120/130/135).  The record
       stores the six thresholds in ONE uniform array with ONE uniform multiplier array, and the
       k=2 case is documented; extending the identical rule to k=3..6 is the minimal reading.
       Every tier-distribution column carries this grade.  A consumer that rejects it can
       recombine from `pth_effective` alone, which is carried beside every distribution.

  So, per direction, with P = clamp(PTH, 55, +inf):
       P(miss)            = max(0, 100 - P) / 100
       P(tier >= T_k)     = clamp((P - T_k) / 100, 0, 1)      k = 2..6
       P(exact tier k)    = P(>=T_k) - P(>=T_{k+1})
       P(normal x1.0)     = P(hit) - P(>=T_2)                 [only when P >= 70]
       if P < 70:  no crit mass; every landed hit carries the flat scalar P/70.
       E[multiplier | hit] = Σ_k P(exact k)*mult_k / P(hit)

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap O.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import sys
from typing import Dict, List, Optional, Sequence, Tuple

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4i_lib_2026_08_13 import (                                            # noqa: E402
    E3, ev, creature_skill_slots, own_total_damage_modifier,
    surv_at, survival_arrays, difficulty_pak, _idx, BATON_20W,
)
from pm4m_lib_2026_08_14 import (                                            # noqa: E402
    combatformulas, pth, bio_of, bio_path, _ev, skill_stat_sum, sha256_of, dump_csv,
)

#: The findings JSON whose HALT LIST is the commission.  ONLY the data-gate keys are opened.
I14 = (ENGINE / "src" / "reincarnated" / "simulation" / "output"
       / "kc2-pm4-i14-findings-20260814_094018.json")

#: Ultimate / solo cell of the difficulty AttributePak -- the SAME cell Lap D read 580.0 from.
ULT_SOLO = 8

#: THE PLAYER DEFENCE + OFFENCE SHEET, camera-MEASURED off the referent's own character sheet
#: (Lap A `measured-player-sheet.csv`, screenshots 495 / 508; the played save is
#: `gdc/_EoRWarlGuts/player.gdc`, parsed at Lap A / Lap G).
PLAYER_SHEET = dict(
    level=100,
    physique=914,          # sheet total (base + gear + skills)
    cunning=1219,          # sheet total -- the dexterityDV of the OA equation
    spirit=398,
    OA=3259.0,             # sheet TOTAL: already includes gear flat/%, skills, attributes
    DA=2591.0,             # sheet TOTAL
    crit_damage_pct=57.0,  # sheet "+57% Critical Damage"
)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# The halt list -- the ONLY thing read out of the findings JSON
# ══════════════════════════════════════════════════════════════════════════════════════════════
def halt_list() -> dict:
    d = json.loads(I14.read_text())
    g = d["⚑ data_gate"]
    return dict(
        own_halted=dict(g["⚑ halted_records"]),
        attr_measured=set(g["attr_measured_records"]),
        n_actors=int(g["n_actors"]), n_records=int(g["n_records"]),
        n_attr_halted_records=int(g["⚑ n_attr_halted_records"]),
        n_attr_halted_actors=int(g["⚑ n_attr_halted_actors"]),
        n_own_halted_records=int(g["⚑ n_own_halted_records"]),
        n_own_halted_actors=int(g["⚑ n_own_halted_actors"]),
        basis=g["basis"],
    )


def roster_actors() -> List[dict]:
    """The FROZEN roster roll -- `record_path` / `wave` / `level` only.  A roster basis, not an
    outcome: which record was drawn at which wave at which spawn level."""
    b = json.loads(BATON_20W.read_text())
    return b["actors"]


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PART A -- the two halted terms, decoded
# ══════════════════════════════════════════════════════════════════════════════════════════════
def skill_stat_sources(record: str, L: float, field: str) -> Tuple[float, List[str], List[str]]:
    """`(Σ, [source strings], [every skill record CHECKED])` for one field over depth-0 slots."""
    total, src, checked = 0.0, [], []
    for sn, sl in creature_skill_slots(record):
        s, _ = E3.winner(sn)
        checked.append(sn)
        if not s:
            continue
        v = s.get(field)
        if v is None:
            continue
        if isinstance(v, list):
            if not any(v):
                continue
            try:
                rank = int(_ev(sl, L)) if sl is not None else 1
            except Exception:
                rank = 1
            i, st = _idx(v, rank)
            if v[i]:
                total += float(v[i])
                src.append(f"{sn}::{field}[{i}]={v[i]}({st},rank={rank})")
        elif v:
            total += float(v)
            src.append(f"{sn}::{field}={v}(SCALAR)")
    return total, src, checked


def attr_terms(record: str, L: float) -> dict:
    """Every attribute term of one body at one level, with the record path of every term."""
    bp = bio_path(record)
    bio = bio_of(record) or {}
    _b, bio_arc = (E3.winner(bp) if bp else (None, ""))
    out = dict(bio_record=bp or "ABSENT", bio_archive=bio_arc or "")
    for name, field in (("dex", "characterDexterity"),
                        ("int", "characterIntelligence"),
                        ("str", "characterStrength"),
                        ("oa", "characterOffensiveAbility"),
                        ("da", "characterDefensiveAbility")):
        eq = bio.get(field)
        if isinstance(eq, list):
            eq = eq[0] if eq else None
        if eq is None:
            out[f"{name}_equation"] = "ABSENT"
            out[f"{name}_bio_value"] = ""
            out[f"{name}_source"] = f"{bp or record}::{field} ABSENT (record checked)"
        else:
            out[f"{name}_equation"] = str(eq)
            out[f"{name}_bio_value"] = round(_ev(eq, L), 4)
            out[f"{name}_source"] = f"{bp}::{field}"
        add, src, checked = skill_stat_sources(record, L, field)
        out[f"{name}_skill_add"] = round(add, 4)
        out[f"{name}_skill_sources"] = " | ".join(src) if src else (
            f"ABSENT on all {len(checked)} own skill slots")
        base = out[f"{name}_bio_value"]
        out[f"{name}_total"] = round((base if base != "" else 0.0) + add, 4)
    return out


def own_tdm_terms(record: str, L: float) -> dict:
    """The body's OWN `offensiveTotalDamageModifier` grant, with the ABSENT case named.

    Sources carry the FULL record path (the commission's requirement).  The total is cross-checked
    against Lap I's `own_total_damage_modifier` -- an independently-written walk of the same slots
    -- and any disagreement is surfaced in the row rather than swallowed.
    """
    total, src, checked = skill_stat_sources(record, L, "offensiveTotalDamageModifier")
    lapi_total, _lapi_src = own_total_damage_modifier(record, L)
    return dict(
        own_total_damage_modifier_pct=round(total, 4),
        own_tdm_n_sources=len(src),
        own_tdm_sources=(" | ".join(src) if src else
                         "ABSENT -- offensiveTotalDamageModifier absent or all-zero on every "
                         f"own depth-0 skill slot ({len(checked)} records checked)"),
        own_tdm_slots_checked=(" | ".join(checked) if checked else
                               "NO own skillName{i} slots on the creature record"),
        own_tdm_state=("MEASURED" if src else "ABSENT-MEASURED-ZERO"),
        own_tdm_lapI_crosscheck=("AGREE" if abs(lapi_total - total) < 1e-9
                                 else f"DISAGREE lapI={lapi_total} here={total}"),
    )


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PART B -- OA and DA per the game's own equations
# ══════════════════════════════════════════════════════════════════════════════════════════════
def ability(record: str, L: float, wave: int, surv, pak, which: str) -> dict:
    """`offensiveAbilityEquation` (which='oa') or `defensiveAbilityEquation` (which='da'),
    with every additive term named and carried."""
    assert which in ("oa", "da")
    base_f = "characterOffensiveAbility" if which == "oa" else "characterDefensiveAbility"
    mod_f = base_f + "Modifier"
    attr_f = "characterDexterity" if which == "oa" else "characterStrength"

    bio = bio_of(record) or {}
    attr = _ev(bio.get(attr_f), L) + skill_stat_sum(record, L, attr_f)
    base = _ev(bio.get(base_f), L)
    skill = skill_stat_sum(record, L, base_f)
    wave_add = surv_at(surv[base_f], wave) if base_f in surv else 0.0
    ult_add = pak[base_f][ULT_SOLO] if base_f in pak else 0.0
    mod_skill = skill_stat_sum(record, L, mod_f)
    mod_wave = surv_at(surv[mod_f], wave) if mod_f in surv else 0.0
    mod_ult = pak[mod_f][ULT_SOLO] if mod_f in pak else 0.0
    mod = mod_skill + mod_wave + mod_ult
    flat = base + skill + wave_add + ult_add
    val = (flat + (L * 12) + (attr * 0.5)) * (1 + mod / 100.0) + 53
    return {
        f"{which}_attr_{attr_f}": round(attr, 4),
        f"{which}_flat_bio": round(base, 4),
        f"{which}_flat_own_skills": round(skill, 4),
        f"{which}_flat_wave_surv": wave_add,
        f"{which}_flat_ultimate_pak": ult_add,
        f"{which}_mod_pct_own_skills": round(mod_skill, 4),
        f"{which}_mod_pct_wave_surv": mod_wave,
        f"{which}_mod_pct_ultimate_pak": mod_ult,
        f"{which}_mod_pct_total": round(mod, 4),
        f"{which}_level_term": L * 12,
        f"{which}_attr_term": round(attr * 0.5, 4),
        which.upper(): round(val, 4),
    }


# ══════════════════════════════════════════════════════════════════════════════════════════════
# The PTH / crit-tier prediction
# ══════════════════════════════════════════════════════════════════════════════════════════════
def thresholds() -> List[Tuple[int, float, float]]:
    cf = combatformulas()
    return [(i, float(cf[f"pthThreshold{i}"]), float(cf[f"pthDamageModifier{i}"]))
            for i in range(1, 7)]


def pth_prediction(oa: float, da: float) -> dict:
    """PREDICTED-FROM-RECORDS hit / miss / crit-tier distribution for one direction."""
    cf = combatformulas()
    raw = pth(oa, da)
    P = max(float(cf["pthMinimum"]), raw)
    ths = thresholds()
    T = {i: t for i, t, _m in ths}
    M = {i: m for i, _t, m in ths}

    p_hit = min(1.0, P / 100.0)
    p_miss = 1.0 - p_hit

    ge = {i: max(0.0, min(1.0, (P - T[i]) / 100.0)) for i in range(2, 7)}
    exact = {}
    for i in range(2, 7):
        nxt = ge[i + 1] if i + 1 <= 6 else 0.0
        exact[i] = max(0.0, ge[i] - nxt)
    crit_mass = sum(exact.values())

    if P < T[1]:                      # sub-70: no crit mass, flat PTH/70 scalar on every hit
        sub70 = P / T[1]
        p_normal = p_hit
        exact = {i: 0.0 for i in range(2, 7)}
        crit_mass = 0.0
        e_mult = sub70
        normal_mult = sub70
    else:
        sub70 = 1.0
        normal_mult = float(M[1])
        p_normal = max(0.0, p_hit - crit_mass)
        e_mult = ((p_normal * normal_mult + sum(exact[i] * M[i] for i in range(2, 7)))
                  / p_hit) if p_hit > 0 else 0.0

    out = dict(
        pth_raw=round(raw, 4),
        pth_effective=round(P, 4),
        pth_floored_at_55=(raw < float(cf["pthMinimum"])),
        p_hit_pct=round(100.0 * p_hit, 4),
        p_miss_pct=round(100.0 * p_miss, 4),
        sub70_damage_scalar=round(sub70, 6),
        p_normal_x1_0_pct=round(100.0 * p_normal, 4),
        p_crit_any_pct=round(100.0 * crit_mass, 4),
        expected_mult_given_hit=round(e_mult, 6),
        expected_mult_per_swing=round(e_mult * p_hit, 6),
    )
    for i in range(2, 7):
        out[f"p_tier{i}_x{M[i]:.1f}_pct"] = round(100.0 * exact[i], 4)
    out["tier_mass_sum_check_pct"] = round(
        100.0 * (p_miss + p_normal + crit_mass), 6)
    return out


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()
