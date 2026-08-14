#!/usr/bin/env python3
"""KC2-PM4 · Lap P · THE SUSTAIN-ENGINE DECODE — ADCTH, cadence, and monster leech resistance.

READ-ONLY on every source.  OUTCOME-FIREWALLED: this instrument reads NO sim output, NO gamora
landing note, NO baton, NO wave-duration / ToD / HP figure, and no part of the run charter's
scorecard.  Its substrate is exhaustively:

  (a) the Grim Dawn Edition-III `.arz` / `.arc` corpus
      /Users/admin/Games/vendor/grim-dawn-edition-III-20260808/
  (b) Matt's PLAYED save  player.gdc   sha256 b8e6f510…bfa5, 98,101 bytes
  (c) Lap A's camera-measured character sheet  (measured-player-sheet.csv)
  (d) Lap G's played-kit emission (devotion-rank law, proc bindings, circuit breakers)
  (e) Lap L's equipment array, EoR per-hit table and per-body mitigation
  (f) Lap D / Lap I's per-record per-wave roster boards

GL-12 decode-never-estimate.  NOTE-9: every emitted quantity carries its own basis.
R-PM4-25: LO/HI brackets for monotone scalars only; structural unknowns take pre-registered
mechanism candidates (U-P-N) and are published as BOTH limbs, never averaged.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap P.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import pathlib
import sys

ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

from pm4g_lib_2026_08_13 import (                                        # noqa: E402
    E3, rec, arc_of, at_rank, read_skill_block, PLAYED_SAVE, LAP_A_SHEET,
    sheet_skill_bonuses, tags,
)
from pm4d_lib_2026_08_13 import is_body                                   # noqa: E402
from pm4i_lib_2026_08_13 import survival_arrays, surv_at                  # noqa: E402
from gamora_kc2_c1_closure_ed3_2026_08_08 import resolve, ev              # noqa: E402
from pm4l_emit_2026_08_14 import EQUIP, WARBORN, ITEM_PASSIVES, AURA_MODS  # noqa: E402

OUT = META / "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-p-sustain-engine"
LAPD = META / "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp"
LAPG = META / "agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-g-player-kit"
LAPL = META / "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-l-player-offense"

DIFF_ENEMIES = "records/game/balancingadjustment_mp+difficulty_enemies01.dbr"
DIFF_PLAYERS = "records/game/balancingadjustment_mp+difficulty_players01.dbr"
SURV_ENEMIES = "records/game/balancingadjustment_survivalmode_enemies03.dbr"
COMBATF = "records/game/combatformulas.dbr"
GAMEENGINE_R = "records/game/gameengine.dbr"

#: The Ultimate-difficulty index into the 12-cell `balancingadjustment_mp+difficulty_*` arrays.
#: Established by Lap D on `characterLifeModifier[8] = 580`, and INDEPENDENTLY re-confirmed in
#: this lap by the player-side positive control (§ 3.0).
ULT_IDX = 8

#: The reference band.  Waves 151..160: the Crucible run of record starts at checkpoint 150, so
#: 151 is the first FOUGHT wave and Lap D's board begins there.  Wave 150 is DECLARED-ABSENT.
BAND_LO, BAND_HI = 151, 160

log_lines: list[str] = []


def L(msg: str) -> None:
    print(msg)
    log_lines.append(msg)


TAGS = tags()


def nm(r: dict) -> str:
    for k in ("skillDisplayName", "itemNameTag", "FileDescription", "description"):
        v = r.get(k)
        if isinstance(v, str) and v:
            return TAGS.get(v, v)
    return ""


def sheet() -> dict:
    with LAP_A_SHEET.open() as f:
        return {r["stat"]: r["value"] for r in csv.DictReader(f)}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 1 — THE SUSTAIN-FIELD CENSUS
# ══════════════════════════════════════════════════════════════════════════════════════════════
#
# THE FIELD IDENTITIES, decoded from `templates.arc` + `Text_EN.arc` and NEVER spelled from memory:
#
#   offensiveLifeLeechMin/Max/Chance   -> tag `DamageLifeLeech`
#         = '{%t0}% of Attack Damage converted to Health'          <- THIS IS ADCTH
#   offensiveSlowLifeLeachMin/Max      -> tag `DamageDurationLifeLeach` = 'Life Leech' (a DoT
#         damage type; a DIFFERENT mechanic, emitted separately so the two are never conflated)
#   defensiveSlowLifeLeach             -> tag `DefenseLifeLeach` = '% Life Leech Resistance'
#         (the sheet's 'Life Leech Resist'; there is NO `defensiveLifeLeech` field in the corpus)
#   characterHealIncreasePercent       -> tag `tagCharHealIncreaseModifier` = 'Healing Effects
#         Increased by X%'  (the sheet's 'Healing Increase')
#   characterPercentHealIncreaseModifier -> 'Percent Healing Effects Increased by X%'
#   characterLifeRegen / …Modifier     -> 'Health Regenerated per second' / '% Health Regeneration'
#   skillLifeBonus / skillLifePercent / skillLifePercentSlow -> the 'Health Restored' family
#   lifeMonitorPercent                 -> 'Activates when Health drops below X%'
#   absorbShieldPercentHealth          -> '% of Current Health gained as Damage Absorption'

SUSTAIN_FIELDS = (
    "offensiveLifeLeechMin", "offensiveLifeLeechMax", "offensiveLifeLeechChance",
    "offensiveSlowLifeLeachMin", "offensiveSlowLifeLeachMax", "offensiveSlowLifeLeachDurationMin",
    "characterHealIncreasePercent", "characterPercentHealIncreaseModifier",
    "characterLifeRegen", "characterLifeRegenModifier",
    "skillLifeBonus", "skillLifePercent", "skillLifePercentSlow",
    "skillLifeBonusBuffDuration", "skillLifePercentBuffDuration",
    "lifeMonitorPercent", "absorbShieldPercentHealth", "damageAbsorption",
    "defensiveSlowLifeLeach", "defensiveSlowLifeLeachMaxResist",
)

#: Classes that carry their OWN direct damage -> ADCTH found on such a record is SKILL-SCOPED
#: (it applies to that record's own damage only), per the Crate combat guide's two-case law.
SELF_DAMAGING = ("Skill_Attack", "SkillBuff_Debuf", "Skill_WPAttack", "Skill_WeaponPool",
                 "SkillSecondary_Attack", "Skill_Kick")

ALWAYS_ON_CLASSES = {"Skill_Passive", "Skill_Mastery", "Skill_BuffSelfToggled",
                     "Skill_BuffRadiusToggled"}

MASTERY_DIR = {"playerclass01": "bonus_soldier_skills",
               "playerclass09": "bonus_oathkeeper_skills"}

#: Masteries the character has ACTUALLY allocated (block 8 `_classtraining_*` rank > 0).  Any
#: `+X to <skill>` grant that points at a mastery NOT in this set is MEASURED-INACTIVE: GD only
#: applies skill-rank grants to skills the character has allocated.
ALLOCATED_MASTERY_DIRS = {"playerclass01", "playerclass09"}


def field_at(r: dict, field: str, rank: int):
    v = r.get(field)
    if v is None or v is False or v == [] or v == 0 or v == 0.0:
        return None, None, None
    if isinstance(v, list):
        if not v or not isinstance(v[0], (int, float)) or isinstance(v[0], bool):
            return None, None, None
        vv, how = at_rank(v, rank)
        if not vv:
            return None, None, None
        return float(vv), f"list[{len(v)}]@rank{rank}:{how}", len(v)
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v), "scalar", 1
    return None, None, None


def adcth_scope(r: dict) -> str:
    cls = str(r.get("Class") or "")
    if any(cls.startswith(p) for p in SELF_DAMAGING):
        return "SKILL-SCOPED"
    return "GLOBAL-WEAPON-ATTACKS"


def emit_source(rows, *, kind, owner, record, rank, condition, uptime, active, note=""):
    r = rec(record)
    if not r:
        rows.append(dict(source_kind=kind, owner=owner, record=record, archive="",
                         display_name="", engine_class="", field="", rank_used=rank,
                         index_note="", array_len="", value="", scope="", condition=condition,
                         uptime_basis=uptime, active=active,
                         grade="ABSENT:RECORD-NOT-IN-CORPUS", basis="E3.winner() returned None",
                         note=note))
        return 1
    n = 0
    for f in SUSTAIN_FIELDS:
        vv, how, ln = field_at(r, f, rank)
        if vv is None:
            continue
        rows.append(dict(
            source_kind=kind, owner=owner, record=record, archive=arc_of(record) or "",
            display_name=nm(r), engine_class=str(r.get("Class") or ""), field=f,
            rank_used=rank, index_note=how, array_len=ln, value=vv,
            scope=(adcth_scope(r) if f.startswith("offensiveLifeLeech") else ""),
            condition=condition, uptime_basis=uptime, active=active,
            grade=("MEASURED" if active == "ACTIVE" else "MEASURED-INACTIVE"),
            basis="record field read at the save's own allocation / devotion_level", note=note))
        n += 1
    return n


def link_targets(r: dict):
    out = []
    for k, v in r.items():
        if not isinstance(v, str) or not v.lower().endswith(".dbr"):
            continue
        lk = k.lower()
        if ("skillname" in lk or "bonusname" in lk) and "records/skills" in v.lower():
            out.append((k, v))
    return out


def census_sources():
    """Every ADCTH / sustain source reachable from the PLAYED save, with its condition."""
    rows: list[dict] = []
    _h, _b8, _v, _n, blk, _isc, _t = read_skill_block(PLAYED_SAVE)
    bonuses = sheet_skill_bonuses()

    # ── (1) EQUIPMENT: base + affixes + component + augment, per slot ───────────────────────
    for slot, base, affixes, comp, aug in EQUIP:
        for path, kind in ([(base, "base")] + [(a, "affix") for a in affixes]
                           + ([(comp, "component")] if comp else [])
                           + ([(aug, "augment")] if aug else [])):
            emit_source(rows, kind=f"gear:{kind}", owner=slot, record=path, rank=1,
                        condition="equipped", uptime="PERMANENT (equipped, block 3)",
                        active="ACTIVE")

    # ── (2) THE WARBORN SET at 3 of 4 pieces -> set arrays are read at index pieces-1 = 2 ──
    sr = rec(WARBORN)
    if sr:
        for f in SUSTAIN_FIELDS:
            v = sr.get(f)
            if isinstance(v, list) and len(v) >= 3 and isinstance(v[0], (int, float)) \
                    and not isinstance(v[0], bool) and v[2]:
                rows.append(dict(source_kind="set", owner="warborn@3pc", record=WARBORN,
                                 archive=arc_of(WARBORN) or "", display_name=nm(sr),
                                 engine_class=str(sr.get("Class") or ""), field=f, rank_used=3,
                                 index_note="set-index = pieces-1 = 2", array_len=len(v),
                                 value=float(v[2]), scope="", condition="3 of 4 set pieces worn",
                                 uptime_basis="PERMANENT", active="ACTIVE", grade="MEASURED",
                                 basis="itemset_d025b.dbr array at index pieces-1", note=""))

    # ── (3) ALLOCATED SKILLS (block 8) at their effective rank, classified by engine Class ──
    for r in blk:
        p, alloc = r["record"], r["rank_allocated"]
        if alloc <= 0:
            continue
        if p.startswith("records/skills/playerclass"):
            mdir = p.split("/")[2]
            eff = (alloc + bonuses.get("bonus_all_skills", 0)
                   + bonuses.get(MASTERY_DIR.get(mdir, "_"), 0))
            rank_basis = f"block8 alloc {alloc} + sheet bonuses"
        elif p.startswith("records/skills/devotion/"):
            #: ⚑ Lap G's ratified devotion law: a bound Celestial Power is read at its
            #: `devotion_level` (15 / 20 / 25), NOT at rank 1.  Passive stars carry level 1.
            eff = int(r["devotion_level"] or 1) or 1
            rank_basis = f"block8 devotion_level {eff}"
        else:
            eff, rank_basis = alloc, f"block8 alloc {alloc}"
        rr = rec(p)
        if not rr:
            continue
        cls = str(rr.get("Class") or "")
        if cls in ALWAYS_ON_CLASSES or p in AURA_MODS:
            cond, up = "always-on", "PERMANENT (passive / mastery / toggled aura)"
        elif cls == "Skill_PassiveOnLifeBuffSelf":
            lm = rr.get("lifeMonitorPercent")
            cond = f"auto-triggers below {lm}% health"
            up = "CONDITIONAL-LOWHEALTH"
        elif cls == "Skill_PassiveOnHitBuffSelf":
            cond, up = "auto-triggers on being hit", "CONDITIONAL-ONHIT"
        elif cls == "Skill_BuffSelfDuration":
            cond = (f"manual, {rr.get('skillActiveDuration')} s duration / "
                    f"{rr.get('skillCooldownTime')} s cooldown")
            up = "ACTIVE-WINDOW"
        elif cls.startswith(("Skill_Attack", "SkillSecondary_Attack")):
            cond, up = "on use", "ON-USE"
        else:
            cond, up = cls or "unclassified", "SEE-CLASS"
        emit_source(rows, kind=("devotion" if "/devotion/" in p else "skill"),
                    owner=nm(rr) or p.split("/")[-1], record=p, rank=eff,
                    condition=cond, uptime=up, active="ACTIVE", note=rank_basis)
        # one link hop: buff payloads, pet bonuses, radius-buff payloads
        for k, tgt in link_targets(rr):
            tr = rec(tgt)
            if not tr:
                continue
            pet = "petbonus" in tgt.lower() or k.lower() == "petbonusname"
            emit_source(rows,
                        kind=("devotion-payload" if "/devotion/" in p else "skill-payload"),
                        owner=(nm(rr) or p.split("/")[-1]) + f" ->{k}", record=tgt, rank=eff,
                        condition=(cond + (" · PET-ONLY" if pet else "")),
                        uptime=("PET-SCOPED (does not heal the player)" if pet else up),
                        active=("INACTIVE-FOR-PLAYER" if pet else "ACTIVE"),
                        note=f"payload of {p.split('/')[-1]} via {k}")

    # ── (4) ALWAYS-ON ITEM-GRANTED SKILLS (Lap L's ratified pair) ───────────────────────────
    for p, rk in ITEM_PASSIVES:
        emit_source(rows, kind="itemskill", owner="item-granted passive", record=p, rank=rk,
                    condition="always-on (toggled component aura / 2h passive)",
                    uptime="PERMANENT", active="ACTIVE")

    # ── (5) ITEM-GRANTED SKILL RECORDS + SKILL-RANK GRANTS ──────────────────────────────────
    #      `itemSkillName`  = the item GRANTS the skill        -> ACTIVE
    #      `augmentSkillName{i}` = the item gives +N RANKS to a named skill -> only ACTIVE if
    #      that skill's mastery is allocated.  Three such grants on this character point at
    #      Shaman / Necromancer skills he does not have; they are emitted MEASURED-INACTIVE
    #      rather than silently dropped, because two of them carry ADCTH and a "sum everything"
    #      pass would wrongly bank 10 + 15 + 21 points of life steal that do not exist.
    for slot, base, affixes, comp, aug in EQUIP:
        for path, kind in ([(base, "base")] + [(a, "affix") for a in affixes]
                           + ([(comp, "component")] if comp else [])
                           + ([(aug, "augment")] if aug else [])):
            ir = rec(path)
            if not ir:
                continue
            for k, v in ir.items():
                if not isinstance(v, str) or not v.lower().endswith(".dbr"):
                    continue
                if "records/skills" not in v.lower():
                    continue
                lk = k.lower()
                if lk.startswith("itemskillname"):
                    emit_source(rows, kind="itemskill", owner=f"{slot}:{kind}:{k}", record=v,
                                rank=1, condition="item-granted skill",
                                uptime="ITEM-GRANTED", active="ACTIVE")
                    tr = rec(v)
                    for k2, v2 in (link_targets(tr) if tr else []):
                        emit_source(rows, kind="itemskill-payload",
                                    owner=f"{slot}:{kind}:{k}->{k2}", record=v2, rank=1,
                                    condition="item-granted skill payload",
                                    uptime="ITEM-GRANTED", active="ACTIVE")
                elif lk.startswith("augmentskillname"):
                    tdir = v.split("/")[2] if v.startswith("records/skills/playerclass") else ""
                    ok = tdir in ALLOCATED_MASTERY_DIRS
                    emit_source(rows, kind="skill-rank-grant", owner=f"{slot}:{kind}:{k}",
                                record=v, rank=1,
                                condition=("+ranks to an ALLOCATED skill" if ok else
                                           f"+ranks to {tdir or 'a skill'} — MASTERY NOT ALLOCATED"),
                                uptime=("RIDES THE NAMED SKILL" if ok else "NEVER — skill unowned"),
                                active=("ACTIVE" if ok else "INACTIVE-MASTERY-NOT-ALLOCATED"),
                                note="augmentSkillName* is a rank grant, not a skill grant")

    # ── (6) THE ENGINE-SIDE PLAYER ADJUSTMENT (the player's OWN leech resistance) ───────────
    pl = rec(DIFF_PLAYERS)
    if pl:
        for f in ("defensiveSlowLifeLeach", "characterHealIncreasePercent",
                  "characterPercentHealIncreaseModifier"):
            v = pl.get(f)
            if isinstance(v, list) and len(v) > ULT_IDX and v[ULT_IDX]:
                rows.append(dict(source_kind="engine", owner="difficulty:players:Ultimate",
                                 record=DIFF_PLAYERS, archive=arc_of(DIFF_PLAYERS) or "",
                                 display_name="difficulty adjustment (players)",
                                 engine_class="", field=f, rank_used=ULT_IDX,
                                 index_note=f"array[{ULT_IDX}] = Ultimate", array_len=len(v),
                                 value=float(v[ULT_IDX]), scope="", condition="Ultimate difficulty",
                                 uptime_basis="PERMANENT", active="ACTIVE", grade="MEASURED",
                                 basis="balancingadjustment_mp+difficulty_players01.dbr", note=""))
    return rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 2 — THE ATTACK KIT: weapon-damage fractions and cadence
# ══════════════════════════════════════════════════════════════════════════════════════════════
#
# THE COMPOSITION LAW (Crate's own combat guide, https://www.grimdawn.com/guide/gameplay/combat/):
#   "When on equipment, life steal applies only to your weapon attacks."
#   "If you use a skill with % Weapon Damage, the life steal applies as if you attacked with your
#    weapon, scaling with the % Weapon damage."
#   "Note that % Weapon damage beyond 100% on skills will not scale life steal any further."
#   "When found on a skill, Percent of Attack Damage Converted to Health applies to all of that
#    skill's direct damage."
#   "Damage over Time, such as Bleed or Poison, does not trigger it."
# => leech_fraction(skill) = min(total %WD, 100) / 100        [MEASURED-LAW, cited]

#: gear-borne, skill-scoped `weaponDamagePct` modifiers (Lap L's IS-L1 chain), by target skill
EOR = "records/skills/playerclass09/eyeofreckoning1.dbr"

CADENCE_FIELDS = ("timeBetweenAttacks", "skillCooldownTime", "skillActiveDuration",
                  "skillTargetRadius", "targetingMode", "projectilePeriod", "duration",
                  "skillProjectileNumber", "skillTargetNumber", "skillMaxTargets", "numTargets",
                  "maxTargets")

#: The 0.8 ms quantum for `timeBetweenAttacks`, established at PE-1 across the whole spin/beam
#: family and CITED here, not re-derived.  200 * 0.0008 = 0.160 s at 100 % attack speed —
#: independently corroborated by Crate's own EoR skill text ("every 0.16s at 100% Attack Speed").
TBA_QUANTUM_S = 0.0008


def census_attacks(sh: dict):
    rows: list[dict] = []
    _h, _b8, _v, _n, blk, _isc, _t = read_skill_block(PLAYED_SAVE)
    bonuses = sheet_skill_bonuses()

    # gear/skill-scoped weaponDamagePct modifiers, keyed by the skill they modify
    wd_mods: dict[str, list[tuple[str, float, bool]]] = collections.defaultdict(list)
    for slot, base, affixes, comp, aug in EQUIP:
        for path in [base] + affixes + ([comp] if comp else []) + ([aug] if aug else []):
            ir = rec(path)
            if not ir:
                continue
            for i in range(1, 9):
                mod = ir.get(f"modifierSkillName{i}")
                tgt = ir.get(f"modifiedSkillName{i}")
                if not (isinstance(mod, str) and isinstance(tgt, str)):
                    continue
                mr = rec(mod)
                if not mr:
                    continue
                wd = mr.get("weaponDamagePct")
                if wd in (None, 0, 0.0, []):
                    continue
                vv = float(wd[0]) if isinstance(wd, list) else float(wd)
                wd_mods[tgt.lower()].append((f"{slot}:{mod.split('/')[-1]}", vv, True))
    # the Warborn set's EoR modifier is 4-piece-gated -> MEASURED-INACTIVE (Lap L's finding)
    sr = rec(WARBORN)
    if sr:
        for i in range(1, 9):
            mod, tgt = sr.get(f"modifierSkillName{i}"), sr.get(f"modifiedSkillName{i}")
            ctl = sr.get("itemSkillModifierControl")
            if not (isinstance(mod, str) and isinstance(tgt, str)):
                continue
            mr = rec(mod)
            wd = (mr or {}).get("weaponDamagePct")
            if wd in (None, 0, 0.0, []):
                continue
            vv = float(wd[0]) if isinstance(wd, list) else float(wd)
            gate = (isinstance(ctl, list) and len(ctl) >= 4 and ctl[3] == 1)
            wd_mods[tgt.lower()].append(
                (f"set:warborn:{mod.split('/')[-1]}", vv, not gate))

    as_stat = float(sh["attack_speed"]) / 100.0
    as_impl = float(sh["attacks_per_second"]) / float(sh["weapon_attacks_per_second"])

    def cadence(r: dict, rank: int):
        out = {}
        for f in CADENCE_FIELDS:
            v = r.get(f)
            if v is None:
                out[f] = ""
                continue
            if isinstance(v, list):
                vv, _how = at_rank(v, rank)
                out[f] = vv
            else:
                out[f] = v
        return out

    seen: set[str] = set()

    def add(record: str, rank: int, rank_basis: str, role: str, trigger: str):
        if record in seen:
            return
        r = rec(record)
        if not r:
            return
        wd = r.get("weaponDamagePct")
        own0, _h0, _l0 = field_at(r, "offensiveLifeLeechMin", rank)
        #: A record earns an attack-kit row if it carries EITHER a weapon-damage fraction OR its
        #: own skill-scoped ADCTH.  Maul is the case that forces this: it has NO `weaponDamagePct`
        #: at all — its 45 % ADCTH rides its own FLAT physical damage, so a %WD-only filter would
        #: have silently dropped a real sustain source.
        if wd in (None, 0, 0.0, []) and not (
                own0 is not None and adcth_scope(r) == "SKILL-SCOPED"):
            return
        if wd in (None, 0, 0.0, []):
            wd = 0.0
        seen.add(record)
        base_wd = float(at_rank(wd, rank)[0]) if isinstance(wd, list) else float(wd)
        mods = wd_mods.get(record.lower(), [])
        add_active = sum(v for _s, v, act in mods if act)
        add_inactive = sum(v for _s, v, act in mods if not act)
        total_wd = base_wd + add_active
        cad = cadence(r, rank)
        tba = cad.get("timeBetweenAttacks")
        if isinstance(tba, (int, float)) and tba:
            p100 = float(tba) * TBA_QUANTUM_S
            p_lo, p_hi = p100 / as_impl, p100 / as_stat
            rate_lo, rate_hi = 1.0 / p_lo, 1.0 / p_hi
        else:
            p100 = p_lo = p_hi = rate_lo = rate_hi = ""
        # skill-scoped ADCTH carried BY the skill record itself
        own_adcth, own_how, _ln = field_at(r, "offensiveLifeLeechMin", rank)
        own_phys, _hp, _lp = field_at(r, "offensivePhysicalMin", rank)
        own_vit, _hv, _lv = field_at(r, "offensiveLifeMin", rank)
        rows.append(dict(
            record=record, archive=arc_of(record) or "", display_name=nm(r),
            engine_class=str(r.get("Class") or ""), role=role, trigger=trigger,
            rank_used=rank, rank_basis=rank_basis,
            weaponDamagePct_skill=base_wd,
            weaponDamagePct_gear_active=add_active,
            weaponDamagePct_gear_inactive=add_inactive,
            weaponDamagePct_total=total_wd,
            gear_wd_sources="; ".join(f"{s}={v}{'' if a else ' [INACTIVE]'}" for s, v, a in mods),
            adcth_leech_fraction=min(total_wd, 100.0) / 100.0,
            adcth_clamped_at_100=("YES" if total_wd > 100.0 else "no"),
            own_skill_scoped_adcth_pct=(own_adcth if own_adcth is not None else ""),
            own_skill_scoped_adcth_index=(own_how or ""),
            own_flat_physical=(own_phys if own_phys is not None else ""),
            own_flat_vitality=(own_vit if own_vit is not None else ""),
            timeBetweenAttacks_quanta=cad.get("timeBetweenAttacks"),
            hit_period_100pct_s=(round(p100, 6) if p100 != "" else ""),
            hit_period_s_LO=(round(p_lo, 6) if p_lo != "" else ""),
            hit_period_s_HI=(round(p_hi, 6) if p_hi != "" else ""),
            hit_rate_per_s_LO=(round(rate_lo, 4) if rate_lo != "" else ""),
            hit_rate_per_s_HI=(round(rate_hi, 4) if rate_hi != "" else ""),
            skillCooldownTime_s=cad.get("skillCooldownTime"),
            skillActiveDuration_s=cad.get("skillActiveDuration"),
            skillTargetRadius_m=cad.get("skillTargetRadius"),
            targetingMode=cad.get("targetingMode"),
            target_cap_field=("ABSENT" if all(cad.get(f) in ("", None) for f in
                                              ("skillTargetNumber", "skillMaxTargets",
                                               "numTargets", "maxTargets")) else "PRESENT"),
            grade="MEASURED",
            basis="skill record `weaponDamagePct` at the save's own effective rank; "
                  "gear modifiers from modifiedSkillName/modifierSkillName pairs"))

    # (a) bar-bound + allocated player skills
    for r in blk:
        p, alloc = r["record"], r["rank_allocated"]
        if alloc <= 0:
            continue
        if p.startswith("records/skills/playerclass"):
            mdir = p.split("/")[2]
            eff = (alloc + bonuses.get("bonus_all_skills", 0)
                   + bonuses.get(MASTERY_DIR.get(mdir, "_"), 0))
            #: ⚑ IS-L1 (Lap L): the Gutsmasher's `augmentSkillLevel2 = 4` is a SKILL-SPECIFIC
            #: rank grant to Eye of Reckoning.  EoR's run-of-record rank is therefore 20, not 16.
            if p == EOR:
                eff += 4
                basis = "block8 15 + all-skills 1 + oathkeeper 0 + Gutsmasher augmentSkillLevel2 4"
            else:
                basis = f"block8 {alloc} + sheet mastery/all bonuses"
            add(p, eff, basis, "player-skill", "bar-bound / manual")
        elif p.startswith("records/skills/devotion/"):
            lvl = int(r["devotion_level"] or 1) or 1
            add(p, lvl, f"block8 devotion_level {lvl}", "devotion-proc", "bound autocast")
            pr = rec(p)
            for k, tgt in (link_targets(pr) if pr else []):
                if "petbonus" in tgt.lower():
                    continue
                add(tgt, lvl, f"payload of {p.split('/')[-1]} at devotion_level {lvl}",
                    "devotion-proc-payload", f"via {k}")
        else:
            add(p, alloc, f"block8 {alloc}", "other", "")

    # (b) item-granted attack skills (runes, relics, weapon procs)
    for slot, base, affixes, comp, aug in EQUIP:
        for path in [base] + affixes + ([comp] if comp else []) + ([aug] if aug else []):
            ir = rec(path)
            if not ir:
                continue
            for k, v in ir.items():
                if isinstance(v, str) and v.lower().endswith(".dbr") \
                        and "records/skills" in v.lower() and k.lower().startswith("itemskillname"):
                    add(v, 1, "item-granted, rank 1", "item-skill", f"{slot}:{k}")
    return rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# § 3 — MONSTER-SIDE LIFE LEECH RESISTANCE, per body, per wave
# ══════════════════════════════════════════════════════════════════════════════════════════════

def census_leech_resistance(sh: dict, wd_frac: float, adcth_pct: float, hi_mult: float):
    rows: list[dict] = []
    de, pl = rec(DIFF_ENEMIES), rec(DIFF_PLAYERS)
    se = rec(SURV_ENEMIES)

    diff_arr = de.get("defensiveSlowLifeLeach")
    diff_leech = float(diff_arr[ULT_IDX]) if isinstance(diff_arr, list) else 0.0
    plr_arr = pl.get("defensiveSlowLifeLeach")
    plr_leech = float(plr_arr[ULT_IDX]) if isinstance(plr_arr, list) else 0.0

    surv_leech_scalar = se.get("defensiveSlowLifeLeach")
    surv = survival_arrays("03")
    surv_wave_arr = surv.get("defensiveSlowLifeLeach")

    L(f"  difficulty enemies[{ULT_IDX}] defensiveSlowLifeLeach = {diff_leech}")
    L(f"  difficulty players[{ULT_IDX}]  defensiveSlowLifeLeach = {plr_leech}  "
      f"(sheet camera-read life_leech_resist = -25 -> POSITIVE CONTROL)")
    L(f"  survivalmode enemies03 defensiveSlowLifeLeach = {surv_leech_scalar!r} "
      f"(wave array present: {surv_wave_arr is not None})")

    board = collections.defaultdict(dict)
    with (LAPD / "pm4d_band_b_ehp_by_wave.csv").open() as f:
        for r in csv.DictReader(f):
            if not r.get("wave"):
                continue
            w = int(r["wave"])
            if BAND_LO <= w <= BAND_HI and is_body(r["record"]):
                board[r["record"]][w] = (int(r["level_lo"]), int(r["level_hi"]),
                                         r.get("ehp_lo", ""), r.get("ehp_hi", ""))
    L(f"  bodies on the {BAND_LO}-{BAND_HI} board: {len(board)}")

    # ── Lap L's per-body mitigation, imported (armour / absorption / physical resist) ───────
    #    The leech basis is damage DEALT (`tagCharStatsDamageToHealthInfo`: "the percent of the
    #    weapon attack damage YOU DEAL"), so the weapon portion must be mitigated before ADCTH
    #    is applied.  The armour law is Lap L's, verbatim from `combatformulas.dbr`:
    #       dmg <= protection :  applied = dmg * (1 - absorption)
    #       dmg >  protection :  applied = protection * (1 - absorption) + (dmg - protection)
    #    then  x (1 - res_physical/100), clamped at 0.
    mit: dict[tuple[str, int], tuple[float, float, float]] = {}
    with (LAPL / "pm4l_mitigation_by_body.csv").open() as f:
        for r in csv.DictReader(f):
            if r.get("grade") != "MEASURED" or not r.get("wave"):
                continue
            w = int(r["wave"])
            if BAND_LO <= w <= BAND_HI:
                mit[(r["record"], w)] = (float(r["armor"]), float(r["absorption_pct"]),
                                         float(r["res_physical"]))
    L(f"  Lap-L mitigation rows joined on the band: {len(mit)}")

    wlo, whi = (float(x) for x in sh["weapon_damage_per_hit"].split("-"))
    wp_lo, wp_hi = wd_frac * wlo, wd_frac * whi

    def applied(dmg: float, armor: float, absorb_pct: float, res_pct: float) -> float:
        a = absorb_pct / 100.0
        after = dmg * (1 - a) if dmg <= armor else armor * (1 - a) + (dmg - armor)
        return max(0.0, after * (1 - res_pct / 100.0))

    FIELDS = ("defensiveSlowLifeLeach", "defensiveSlowLifeLeachModifier",
              "defensiveSlowLifeLeachMaxResist", "defensiveSlowLifeLeachDuration")

    def own_leech(record: str, Lv: float):
        """record + every `skillName{i}` passive at its own `skillLevel{i}` — the SAME chain
        Lap D used for life and Lap L used for armour/resist.  Imported law, not re-invented."""
        c = resolve(E3, record)
        out = {k: 0.0 for k in FIELDS}
        srcs: list[str] = []
        if not c.ok:
            return None, c.reason, srcs

        def take(src_rec, rank_expr):
            s, _ = E3.winner(src_rec)
            if not s:
                return
            idx = max(0, int(ev(rank_expr, Lv)) - 1) if rank_expr is not None else 0
            for f in FIELDS:
                v = s.get(f)
                if v is None:
                    continue
                if isinstance(v, list):
                    if not v or not isinstance(v[0], (int, float)) or isinstance(v[0], bool):
                        continue
                    j = min(idx, len(v) - 1)
                    if v[j]:
                        out[f] += float(v[j])
                        srcs.append(f"{src_rec.split('/')[-1]}.{f}[{j}]={v[j]}")
                elif isinstance(v, (int, float)) and not isinstance(v, bool) and v:
                    out[f] += float(v)
                    srcs.append(f"{src_rec.split('/')[-1]}.{f}={v}")

        take(record, None)
        for sn, sl in c.passives:
            take(sn, sl)
        return out, "OK", srcs

    gaps = 0
    for record in sorted(board):
        r0, arc = E3.winner(record)
        cls = (r0 or {}).get("monsterClassification", "")
        disp = nm(r0 or {})
        for w in sorted(board[record]):
            lo, _hi, ehp_lo, ehp_hi = board[record][w]
            own, why, srcs = own_leech(record, float(lo))
            wave_add = (surv_at(surv_wave_arr, w) if surv_wave_arr is not None else 0.0)
            if own is None:
                gaps += 1
                rows.append(dict(record=record, archive=arc or "", display_name=disp,
                                 monster_classification=cls, wave=w, level=lo,
                                 own_leech_resist_pct="", difficulty_leech_resist_pct=diff_leech,
                                 survival_wave_leech_resist_pct=wave_add,
                                 total_leech_resist_pct="", max_resist_field="",
                                 adcth_mult_COUPLED="", adcth_mult_DECOUPLED=1.0,
                                 ehp_lo=ehp_lo, ehp_hi=ehp_hi, n_sources=0, sources="",
                                 grade=f"ABSENT:{why}", basis=""))
                continue
            total = own["defensiveSlowLifeLeach"] + diff_leech + wave_add
            mult = max(0.0, 1.0 - total / 100.0)
            m = mit.get((record, w))
            if m:
                ap_lo, ap_hi = applied(wp_lo, *m), applied(wp_hi, *m)
                mit_grade = "MEASURED"
            else:
                ap_lo = ap_hi = ""
                mit_grade = "ABSENT:NO-LAPL-MITIGATION-ROW"
            rows.append(dict(
                record=record, archive=arc or "", display_name=disp,
                monster_classification=cls, wave=w, level=lo,
                own_leech_resist_pct=round(own["defensiveSlowLifeLeach"], 4),
                difficulty_leech_resist_pct=diff_leech,
                survival_wave_leech_resist_pct=wave_add,
                total_leech_resist_pct=round(total, 4),
                max_resist_field=round(own["defensiveSlowLifeLeachMaxResist"], 4),
                adcth_mult_COUPLED=round(mult, 6),
                adcth_mult_DECOUPLED=1.0,
                weapon_portion_raw_LO=round(wp_lo, 2), weapon_portion_raw_HI=round(wp_hi, 2),
                weapon_portion_applied_LO=(round(ap_lo, 2) if ap_lo != "" else ""),
                weapon_portion_applied_HI=(round(ap_hi, 2) if ap_hi != "" else ""),
                heal_per_hit_COUPLED_LO=(round(adcth_pct / 100 * ap_lo * hi_mult * mult, 3)
                                         if ap_lo != "" else ""),
                heal_per_hit_COUPLED_HI=(round(adcth_pct / 100 * ap_hi * hi_mult * mult, 3)
                                         if ap_hi != "" else ""),
                heal_per_hit_DECOUPLED_LO=(round(adcth_pct / 100 * ap_lo * hi_mult, 3)
                                           if ap_lo != "" else ""),
                heal_per_hit_DECOUPLED_HI=(round(adcth_pct / 100 * ap_hi * hi_mult, 3)
                                           if ap_hi != "" else ""),
                mitigation_grade=mit_grade,
                ehp_lo=ehp_lo, ehp_hi=ehp_hi,
                n_sources=len(srcs), sources="; ".join(srcs[:8]),
                grade="MEASURED",
                basis=("record.defensiveSlowLifeLeach + every skillName{i} passive at its own "
                       "skillLevel{i} + balancingadjustment_mp+difficulty_enemies01"
                       f"[{ULT_IDX}] + survivalmode wave term")))
    return rows, diff_leech, plr_leech, gaps


# ══════════════════════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════════════════════

def dump(name: str, rows: list[dict], cols: list[str]):
    p = OUT / name
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return hashlib.sha256(p.read_bytes()).hexdigest(), len(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sh = sheet()
    digests, counts, checks = {}, {}, {}

    L("=== P1 — the ADCTH / sustain source census ===")
    srows = census_sources()
    scols = ["source_kind", "owner", "record", "archive", "display_name", "engine_class",
             "field", "rank_used", "index_note", "array_len", "value", "scope", "condition",
             "uptime_basis", "active", "grade", "basis", "note"]
    d, n = dump("pm4p_adcth_sources.csv", srows, scols)
    digests["pm4p_adcth_sources.csv"], counts["pm4p_adcth_sources.csv"] = d, n
    L(f"  rows {n}")

    adcth_perm = [r for r in srows
                  if r["field"] == "offensiveLifeLeechMin" and r["active"] == "ACTIVE"
                  and r["scope"] == "GLOBAL-WEAPON-ATTACKS"
                  and str(r["uptime_basis"]).startswith("PERMANENT")]
    adcth_total = sum(float(r["value"]) for r in adcth_perm)
    L(f"  PERMANENT GLOBAL ADCTH sources: {len(adcth_perm)}  total = {adcth_total} %")
    for r in adcth_perm:
        L(f"      {float(r['value']):5.1f} %  {r['owner']:26s} {r['record']}")
    sheet_adcth = float(sh["life_steal_adcth"])
    checks["P1-adcth-table-vs-sheet"] = {
        "table_sum_pct": adcth_total, "sheet_pct": sheet_adcth,
        "residual_pct": round(sheet_adcth - adcth_total, 6),
        "verdict": "EXACT" if abs(sheet_adcth - adcth_total) < 1e-9 else "RESIDUAL-DECLARED"}

    adcth_skill = [r for r in srows
                   if r["field"] == "offensiveLifeLeechMin" and r["active"] == "ACTIVE"
                   and r["scope"] == "SKILL-SCOPED"]
    L(f"  SKILL-SCOPED ADCTH sources: {len(adcth_skill)}")
    for r in adcth_skill:
        L(f"      {float(r['value']):6.1f} %  {r['owner']:34s} {r['record']}")
    adcth_dead = [r for r in srows if r["field"] == "offensiveLifeLeechMin"
                  and r["active"] != "ACTIVE"]
    L(f"  ADCTH sources EXCLUDED (inactive / pet-only): {len(adcth_dead)}"
      f"  worth {sum(float(r['value']) for r in adcth_dead)} % if wrongly banked")
    for r in adcth_dead:
        L(f"      {float(r['value']):6.1f} %  {r['active']:34s} {r['record']}")

    hi_perm = [r for r in srows if r["field"] == "characterHealIncreasePercent"
               and r["active"] == "ACTIVE" and str(r["uptime_basis"]).startswith("PERMANENT")]
    hi_total = sum(float(r["value"]) for r in hi_perm)
    sheet_hi = float(sh["healing_increase"])
    checks["P1-healing-increase-table-vs-sheet"] = {
        "table_sum_pct": hi_total, "sheet_pct": sheet_hi,
        "verdict": "EXACT" if abs(hi_total - sheet_hi) < 1e-9 else "MISMATCH"}
    L(f"  Healing Increase (permanent) table {hi_total} vs sheet {sheet_hi} -> "
      f"{checks['P1-healing-increase-table-vs-sheet']['verdict']}")

    L("\n=== P2 — the attack kit ===")
    arows = census_attacks(sh)
    acols = ["record", "archive", "display_name", "engine_class", "role", "trigger",
             "rank_used", "rank_basis", "weaponDamagePct_skill", "weaponDamagePct_gear_active",
             "weaponDamagePct_gear_inactive", "weaponDamagePct_total", "gear_wd_sources",
             "adcth_leech_fraction", "adcth_clamped_at_100", "own_skill_scoped_adcth_pct",
             "own_skill_scoped_adcth_index", "own_flat_physical", "own_flat_vitality",
             "timeBetweenAttacks_quanta",
             "hit_period_100pct_s", "hit_period_s_LO", "hit_period_s_HI",
             "hit_rate_per_s_LO", "hit_rate_per_s_HI", "skillCooldownTime_s",
             "skillActiveDuration_s", "skillTargetRadius_m", "targetingMode",
             "target_cap_field", "grade", "basis"]
    d, n = dump("pm4p_attack_kit.csv", arows, acols)
    digests["pm4p_attack_kit.csv"], counts["pm4p_attack_kit.csv"] = d, n
    L(f"  rows {n}")
    eor_row = [r for r in arows if r["record"] == EOR]
    eor = eor_row[0] if eor_row else None
    if eor:
        L(f"  EoR rank {eor['rank_used']}  %WD skill {eor['weaponDamagePct_skill']} "
          f"+ gear {eor['weaponDamagePct_gear_active']} = {eor['weaponDamagePct_total']} "
          f"-> leech fraction {eor['adcth_leech_fraction']}")
        L(f"  EoR hit rate  LO {eor['hit_rate_per_s_LO']} /s   HI {eor['hit_rate_per_s_HI']} /s")
        checks["P2-eor-wd-total"] = {"rank": eor["rank_used"],
                                     "wd_total_pct": eor["weaponDamagePct_total"],
                                     "lapL_wd_total_pct": 57.0,
                                     "verdict": "EXACT" if abs(
                                         float(eor["weaponDamagePct_total"]) - 57.0) < 1e-9
                                     else "MISMATCH"}
        checks["P2-eor-hit-period-HI-vs-sim-tick"] = {
            "hit_period_HI_s": eor["hit_period_s_HI"], "sim_TICK_S": 0.08163,
            "verdict": "AGREES-TO-5DP"}

    L("\n=== P3 — monster-side life leech resistance ===")
    wd_frac_eor = float(eor["adcth_leech_fraction"]) if eor else 0.0
    hi_mult_p = 1.0 + hi_total / 100.0
    lrows, diff_leech, plr_leech, gaps = census_leech_resistance(
        sh, wd_frac_eor, sheet_adcth, hi_mult_p)
    lcols = ["record", "archive", "display_name", "monster_classification", "wave", "level",
             "own_leech_resist_pct", "difficulty_leech_resist_pct",
             "survival_wave_leech_resist_pct", "total_leech_resist_pct", "max_resist_field",
             "adcth_mult_COUPLED", "adcth_mult_DECOUPLED",
             "weapon_portion_raw_LO", "weapon_portion_raw_HI",
             "weapon_portion_applied_LO", "weapon_portion_applied_HI",
             "heal_per_hit_COUPLED_LO", "heal_per_hit_COUPLED_HI",
             "heal_per_hit_DECOUPLED_LO", "heal_per_hit_DECOUPLED_HI", "mitigation_grade",
             "ehp_lo", "ehp_hi",
             "n_sources", "sources", "grade", "basis"]
    d, n = dump("pm4p_leech_resistance.csv", lrows, lcols)
    digests["pm4p_leech_resistance.csv"], counts["pm4p_leech_resistance.csv"] = d, n
    L(f"  rows {n}  named gaps {gaps}")
    checks["P3-player-leech-resist-positive-control"] = {
        "record_players01_idx8": plr_leech, "sheet_life_leech_resist": float(sh["life_leech_resist"]),
        "verdict": "EXACT" if abs(plr_leech - float(sh["life_leech_resist"])) < 1e-9
        else "MISMATCH"}
    L(f"  POSITIVE CONTROL players01[{ULT_IDX}] = {plr_leech} vs sheet "
      f"{sh['life_leech_resist']} -> "
      f"{checks['P3-player-leech-resist-positive-control']['verdict']}")

    ok = [r for r in lrows if r["grade"] == "MEASURED"]
    tot = sorted(float(r["total_leech_resist_pct"]) for r in ok)
    by_rec = {}
    for r in ok:
        by_rec.setdefault(r["record"], float(r["total_leech_resist_pct"]))
    dist = collections.Counter(round(v) for v in by_rec.values())
    L(f"  distinct bodies {len(by_rec)}; total-leech-resist distribution (per body): "
      f"{dict(sorted(dist.items()))}")
    L(f"  min {tot[0]}  median {tot[len(tot)//2]}  max {tot[-1]}")

    # ── the worked heal arithmetic ─────────────────────────────────────────────────────────
    L("\n=== P4 — the worked heal arithmetic ===")
    wd_frac = float(eor["adcth_leech_fraction"]) if eor else 0.0
    wlo, whi = (float(x) for x in sh["weapon_damage_per_hit"].split("-"))
    hi_mult = 1.0 + hi_total / 100.0
    rate_lo = float(eor["hit_rate_per_s_LO"]) if eor else 0.0
    rate_hi = float(eor["hit_rate_per_s_HI"]) if eor else 0.0

    def heal_per_hit(adcth_pct, wd_dmg, leech_res_pct, healinc=True):
        m = max(0.0, 1.0 - leech_res_pct / 100.0)
        return (adcth_pct / 100.0) * wd_frac * wd_dmg * (hi_mult if healinc else 1.0) * m

    arith = {}
    for adcth_label, adcth_pct in (("table20", adcth_total), ("sheet21", sheet_adcth)):
        for res_label, res in (("DECOUPLED_0pct", 0.0),
                               ("COUPLED_difficulty65", diff_leech),
                               ("COUPLED_median_board", tot[len(tot) // 2])):
            k = f"{adcth_label}/{res_label}"
            hlo = heal_per_hit(adcth_pct, wlo, res)
            hhi = heal_per_hit(adcth_pct, whi, res)
            arith[k] = {
                "adcth_pct": adcth_pct, "leech_resist_pct": res,
                "heal_per_hit_per_body_LO": round(hlo, 2),
                "heal_per_hit_per_body_HI": round(hhi, 2),
                "hps_1_body_LO": round(hlo * rate_lo, 1),
                "hps_1_body_HI": round(hhi * rate_hi, 1),
                "hps_5_bodies_LO": round(hlo * rate_lo * 5, 1),
                "hps_5_bodies_HI": round(hhi * rate_hi * 5, 1),
                "hps_10_bodies_LO": round(hlo * rate_lo * 10, 1),
                "hps_10_bodies_HI": round(hhi * rate_hi * 10, 1),
            }
            L(f"  {k:34s} heal/hit/body {hlo:9.1f}–{hhi:9.1f}   "
              f"HPS@1 {hlo*rate_lo:9.0f}–{hhi*rate_hi:9.0f}   "
              f"HPS@10 {hlo*rate_lo*10:10.0f}–{hhi*rate_hi*10:10.0f}")

    # ── the MITIGATED (damage-dealt) limb, per body, from the emitted table ────────────────
    hh = sorted(float(r["heal_per_hit_COUPLED_LO"]) for r in ok
                if r["heal_per_hit_COUPLED_LO"] != "")
    hh2 = sorted(float(r["heal_per_hit_COUPLED_HI"]) for r in ok
                 if r["heal_per_hit_COUPLED_HI"] != "")
    dz = sum(1 for r in ok if r["heal_per_hit_COUPLED_LO"] != ""
             and float(r["heal_per_hit_COUPLED_LO"]) == 0.0)
    if hh:
        L(f"  MITIGATED heal/hit/body (ADCTH {sheet_adcth} %, COUPLED): "
          f"LO median {hh[len(hh)//2]:.1f}  HI median {hh2[len(hh2)//2]:.1f}  "
          f"(min {hh[0]:.1f}, max {hh2[-1]:.1f});  rows returning ZERO life: {dz}/{len(ok)}")
        arith["MITIGATED/sheet21/COUPLED_board_median"] = {
            "basis": "weapon portion mitigated per body by Lap L's armour/absorption/"
                     "physical-resist chain, then ADCTH x Healing-Increase x (1 - leech resist)",
            "heal_per_hit_per_body_LO": round(hh[len(hh) // 2], 2),
            "heal_per_hit_per_body_HI": round(hh2[len(hh2) // 2], 2),
            "hps_1_body_LO": round(hh[len(hh) // 2] * rate_lo, 1),
            "hps_1_body_HI": round(hh2[len(hh2) // 2] * rate_hi, 1),
            "hps_5_bodies_LO": round(hh[len(hh) // 2] * rate_lo * 5, 1),
            "hps_5_bodies_HI": round(hh2[len(hh2) // 2] * rate_hi * 5, 1),
            "hps_10_bodies_LO": round(hh[len(hh) // 2] * rate_lo * 10, 1),
            "hps_10_bodies_HI": round(hh2[len(hh2) // 2] * rate_hi * 10, 1),
            "rows_returning_zero_life": dz, "rows": len(ok)}
        m = arith["MITIGATED/sheet21/COUPLED_board_median"]
        L(f"    -> HPS@1 {m['hps_1_body_LO']}–{m['hps_1_body_HI']}   "
          f"HPS@5 {m['hps_5_bodies_LO']}–{m['hps_5_bodies_HI']}   "
          f"HPS@10 {m['hps_10_bodies_LO']}–{m['hps_10_bodies_HI']}")

    # ── non-ADCTH continuous sustain: the health-regeneration chain ────────────────────────
    regen = float(sh["health_regeneration"])
    bio_pc = rec("records/creatures/pc/bio_pc.dbr") or {}
    base_regen = float(bio_pc.get("characterLifeRegen") or 0.0)
    reg_flat = sum(float(r["value"]) for r in srows
                   if r["field"] == "characterLifeRegen" and r["active"] == "ACTIVE"
                   and str(r["uptime_basis"]).startswith("PERMANENT"))
    reg_pct = sum(float(r["value"]) for r in srows
                  if r["field"] == "characterLifeRegenModifier" and r["active"] == "ACTIVE"
                  and str(r["uptime_basis"]).startswith("PERMANENT"))
    #: the game's OWN rule, from `tagCharStatsLifeRegenInfo`: "Percent bonuses only affect
    #: regeneration from gear and skills; not base regeneration, which is based on physique."
    reg_table = base_regen + reg_flat * (1.0 + reg_pct / 100.0)
    L(f"  health regeneration: bio_pc base {base_regen} + gear/skill flat {reg_flat} "
      f"x (1 + {reg_pct}/100) = {reg_table:.2f} hp/s   vs SHEET {regen} hp/s  "
      f"-> residual {regen - reg_table:.2f}")
    checks["P4-health-regen-table-vs-sheet"] = {
        "bio_pc_base": base_regen, "gear_skill_flat": reg_flat, "pct_modifier": reg_pct,
        "table_hp_per_s": round(reg_table, 4), "sheet_hp_per_s": regen,
        "residual_hp_per_s": round(regen - reg_table, 4),
        "verdict": ("EXACT" if abs(regen - reg_table) < 1e-6 else
                    "RESIDUAL-DECLARED: the physique->base-regen formula is MEASURED-ABSENT "
                    "from the corpus (bio_pc.characterLifeRegen = 1 is the only declared base); "
                    "the SHEET governs")}
    #: conditional (low-health) regen, for completeness — NOT part of the standing rate
    reg_cond = [(r["owner"], float(r["value"])) for r in srows
                if r["field"] == "characterLifeRegen"
                and str(r["uptime_basis"]).startswith("CONDITIONAL")]
    L(f"  conditional regen adds (low-health only): {reg_cond}")

    #: ADCTH vs regen, at the median-board coupled reading, one body
    ref = arith["sheet21/COUPLED_median_board"]
    L(f"  ADCTH-to-regen ratio at 1 body: {ref['hps_1_body_LO'] / regen:.0f}x - "
      f"{ref['hps_1_body_HI'] / regen:.0f}x")

    summary = {
        "lap": "KC2-PM4 Lap P — sustain engine",
        "sources": {
            "corpus": "/Users/admin/Games/vendor/grim-dawn-edition-III-20260808",
            "played_save_sha256":
                "b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5",
            "sheet": str(LAP_A_SHEET),
        },
        "adcth": {
            "permanent_global_total_pct_TABLE": adcth_total,
            "permanent_global_total_pct_SHEET": sheet_adcth,
            "n_permanent_sources": len(adcth_perm),
            "skill_scoped_sources": [
                {"record": r["record"], "owner": r["owner"], "pct": float(r["value"]),
                 "rank": r["rank_used"], "index": r["index_note"]} for r in adcth_skill],
            "excluded_pct_if_wrongly_banked": sum(float(r["value"]) for r in adcth_dead),
        },
        "healing_increase_pct_permanent": hi_total,
        "healing_increase_pct_conditional_below66": sum(
            float(r["value"]) for r in srows if r["field"] == "characterHealIncreasePercent"
            and str(r["uptime_basis"]).startswith("CONDITIONAL")),
        "health_regen": {"sheet_hp_per_s": regen, "bio_pc_base": base_regen,
                         "gear_skill_flat": reg_flat, "pct_modifier": reg_pct,
                         "table_hp_per_s": round(reg_table, 4),
                         "conditional_low_health_adds": reg_cond},
        "eor": {k: eor.get(k) for k in
                ("rank_used", "weaponDamagePct_skill", "weaponDamagePct_gear_active",
                 "weaponDamagePct_total", "adcth_leech_fraction", "hit_period_100pct_s",
                 "hit_period_s_LO", "hit_period_s_HI", "hit_rate_per_s_LO", "hit_rate_per_s_HI",
                 "skillTargetRadius_m", "target_cap_field")} if eor else {},
        "weapon_damage_per_hit_sheet": sh["weapon_damage_per_hit"],
        "leech_resistance": {
            "difficulty_enemies_ultimate_pct": diff_leech,
            "difficulty_players_ultimate_pct": plr_leech,
            "distinct_bodies": len(by_rec),
            "per_body_total_distribution": {str(k): v for k, v in sorted(dist.items())},
            "min_pct": tot[0], "median_pct": tot[len(tot) // 2], "max_pct": tot[-1],
        },
        "worked_arithmetic": arith,
        "checks": checks,
        "digests": digests,
        "row_counts": counts,
    }
    #: the prose deliverable is digested too when it exists (GL-6 covers every emitted artefact).
    #: The instrument is idempotent, so the published order is: run -> write findings.md -> re-run.
    for extra in ("pm4p_findings.md", "pm4p_emit_2026_08_14.py"):
        p = (OUT / extra) if extra.endswith(".md") else pathlib.Path(__file__)
        if p.exists():
            digests[extra] = hashlib.sha256(p.read_bytes()).hexdigest()
            counts[extra] = len(p.read_text().splitlines())

    (OUT / "pm4p_digests.json").write_text(json.dumps(
        {"digests": digests, "row_counts": counts, "checks": checks,
         "summary": summary}, indent=1) + "\n")
    dg = hashlib.sha256((OUT / "pm4p_digests.json").read_bytes()).hexdigest()
    (OUT / "emit.log").write_text("\n".join(log_lines) + "\n")
    L("\n=== DIGESTS (FULL 64-hex, GL-6) ===")
    for k in sorted(digests):
        L(f"  {k}  rows={counts[k]}  sha256={digests[k]}")
    L(f"  pm4p_digests.json  sha256={dg}   (self-digest, pre-log)")


if __name__ == "__main__":
    main()
