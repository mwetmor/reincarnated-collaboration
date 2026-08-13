#!/usr/bin/env python3
"""KC2-PM4 Lap I shared library -- the MONSTER-OFFENSE limb + the band-C (waves 171-180) extension.

READ-ONLY on the vendor corpus and on the engine tree.  OUTCOME-FIREWALLED: this module reads
NO sim output, NO baton produced after the frozen 20-wave roll, NO findings JSON.  The one baton
it reads is the FROZEN roster roll (`kc2-baton-v1-E-s09-cp150-20260809_052836.json`), which is a
ROSTER basis (which records were drawn at which wave), not a sim outcome, and is the same basis
Lap D used.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE FOUR DECODES (ruling R-PM4-14)
═══════════════════════════════════════════════════════════════════════════════════════════════

 1. WAVE-G DAMAGE MODIFIER.  Lap D decoded `survivalmode_enemies03.characterLifeModifier`.  The
    SAME record carries 26 other 200-cell wave-indexed arrays, among them
    `offensiveTotalDamageModifier` -- the damage-side pair of the life modifier.  Same array-
    lookup law (S 10.7 / L-33: fighting wave `w` reads the cell LABELED `w`, i.e. index `w-1`).

 2. ULTIMATE OFFENSE PAKS.  `balancingadjustment_mp+difficulty_enemies01.dbr` carries
    `Class = AttributePak` and 12-cell arrays = 3 difficulties x 4 player counts.  Cell [8] is
    Ultimate/solo -- the SAME cell Lap D read `characterLifeModifier[8] = 580.0` from.  Every
    offense-bearing field on that record is decoded at every cell, with [8] flagged.

 3. DOT RIDERS.  Per record on the waves-151-160 board (+ its summon closure), the full skill
    closure is walked and every `offensiveSlow*` damage-over-time family is read at the rank the
    record's own `skillLevel{i}` equation yields at the record's charLevel.

 4. BAND C.  `MAX_WAVE = 200` (wave_engine, R-KC2-4 / U-8) and the corpus carries
    `records/proxies/tier01waves` .. `tier20waves` -- 20 content tiers x 10 waves.  Waves 171-180
    are tier 18.  The Lap-D band stopped at 170 because the FROZEN BATON stops there
    (`arena_tier_exhausted`), NOT because the substrate does.  The life chain is unchanged; only
    the wave index moves, and `G(171)=420 .. G(180)=510` are real cells of the same 200-cell array.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE DAMAGE CHAIN, BY EXACT PARALLEL WITH THE LIFE CHAIN
═══════════════════════════════════════════════════════════════════════════════════════════════

    life:    SIGMA_life(w,L)  = ultimate.characterLifeModifier[8]
                              + surv.characterLifeModifier[w-1]
                              + SIGMA_i skill_i.characterLifeModifier[rank_i(L)-1]

    damage:  SIGMA_dmg(w,L)   = ultimate.offensiveTotalDamageModifier[8]
                              + surv.offensiveTotalDamageModifier[w-1]
                              + SIGMA_i skill_i.offensiveTotalDamageModifier[rank_i(L)-1]

  ⚑ GRADE ON THE COMPOSITION RULE.  The three TERMS are each MEASURED (named record, named field,
    named index).  That they COMBINE ADDITIVELY is asserted by parallel with the life chain
    (L-65: "the life stack is ADDITIVE-within-field"), NOT independently measured on the damage
    field.  Every emitted sum column is therefore graded `DERIVED-SUM-ADDITIVE-BY-PARALLEL`, and
    the three components ride beside it so a consumer can recombine under a different rule.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, Lap I (ruling R-PM4-14).
"""
from __future__ import annotations

import collections
import csv
import json
import math
import pathlib
import sys
from typing import Dict, List, Optional, Sequence, Set, Tuple

ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")

sys.path.insert(0, str(ENGINE / "src" / "reincarnated" / "simulation" / "scripts"))
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))
sys.path.insert(0, str(ENGINE / "src"))

from gamora_kc2_c1_closure_ed3_2026_08_08 import E3, Chain, resolve, ev      # noqa: E402
from gamora_kc2_stat_fold_ed3_2026_08_08 import (                            # noqa: E402
    lv_formula_table, floor_set, pool_slot_proxies, APL_B_PRIME,
)
# Lap D's own instrument -- the summon closure with IS-B2/IS-B3 restored, imported not re-written.
from pm4d_lib_2026_08_13 import (                                            # noqa: E402
    summon_closure_extended, is_body, BATON_20W, POOLS_CSV,
    DIFF_PATH, SURV_PATH, DIFFICULTY_INDEX,
    survival_life_modifier_array, G_at,
)

DATA = ENGINE / "data" / "kc2"

#: Band C, as this lap defines it: content tier 18 = waves 171..180 (`ceil(w/10)`), the first band
#: past the frozen baton's `arena_tier_exhausted` stop and past C-D2's G(171)=420 discontinuity.
BAND_C_FIRST, BAND_C_LAST = 171, 180
#: The DoT population's band -- PM-3 S 5 / Lap D's P-ROLLED-10.
DOT_FIRST, DOT_LAST = 151, 160
#: The terminal waves of the reference sitting (Matt's banked testimony names the LAST wave).
TERMINAL_WAVES = (159, 160)
#: Full emission band for the wave-modifier table.  151..200 = every cell past the reference band
#: that the 200-cell arrays and the 20 tier directories both cover.
WAVE_MOD_FIRST, WAVE_MOD_LAST = 151, 200

WAVES_PER_TIER = 10


def content_tier(wave: int) -> int:
    """`ceil(w/10)` -- selects the `tier<NN>waves` proxy directory (wave_engine S 0.1 glossary)."""
    return math.ceil(wave / WAVES_PER_TIER)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# TARGET 1 -- the wave-indexed OFFENSE arrays on the survival-mode adjustment record
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: The 200-cell wave-indexed arrays on `survivalmode_enemies03`, enumerated FROM THE RECORD
#: (`survival_array_fields()`), not spelled from memory.  This tuple is the OFFENSE-relevant
#: subset the emission carries as named columns; the enumeration is emitted in full beside it.
SURV_OFFENSE_FIELDS = (
    "offensiveTotalDamageModifier",
    "offensivePhysicalModifier",
    "offensiveCritDamageModifier",
    "offensiveSlowBleedingModifier",
    "offensiveSlowColdModifier",
    "offensiveSlowFireModifier",
    "offensiveSlowLifeModifier",
    "offensiveSlowLightningModifier",
    "offensiveSlowPhysicalModifier",
    "offensiveSlowPoisonModifier",
    "characterOffensiveAbility",
    "characterOffensiveAbilityModifier",
    "characterAttackSpeedModifier",
    "characterSpellCastSpeedModifier",
    "skillCooldownReduction",
    "retaliationTotalDamageModifier",
    "characterDefensiveAbility",
    "characterDefensiveAbilityModifier",
    "characterLifeModifier",
)

SURV_RECORDS = {
    "01": "records/game/balancingadjustment_survivalmode_enemies01.dbr",
    "02": "records/game/balancingadjustment_survivalmode_enemies02.dbr",
    "03": "records/game/balancingadjustment_survivalmode_enemies03.dbr",
}
#: The Crucible difficulty of record.  Lap D established `enemies03` by reproducing G(150..170) =
#: 304..344 and by 200/200 agreement with the gladiator scaling CSV.  Carried, and RE-CHECKED here.
SURV_OF_RECORD = "03"


def survival_arrays(which: str = SURV_OF_RECORD) -> Dict[str, List[float]]:
    """Every array field of length > 1 on the named survival adjustment record, decoded."""
    r, arc = E3.winner(SURV_RECORDS[which])
    if r is None:
        raise RuntimeError(f"{SURV_RECORDS[which]} absent from Edition-III")
    return {k: [float(x) for x in v] for k, v in r.items()
            if isinstance(v, list) and len(v) > 1}


def survival_archive(which: str = SURV_OF_RECORD) -> str:
    _r, arc = E3.winner(SURV_RECORDS[which])
    return arc


def surv_at(arr: Sequence[float], wave: int) -> float:
    """The array-lookup law, TOTAL on [1, len(arr)], NO CLAMP (Lap D's `G_at`, same rule)."""
    w = int(wave)
    if not (1 <= w <= len(arr)):
        raise ValueError(f"wave {w} outside array domain [1, {len(arr)}]")
    return float(arr[w - 1])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# TARGET 2 -- the Ultimate difficulty AttributePak
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: The 12 cells of `mp+difficulty_enemies01` = 3 difficulties x 4 player counts, in the order the
#: record stores them.  Cell [8] is the one Lap D's `580.0` came from, which FIXES the layout:
#: `characterLifeModifier = [50 x4, 320 x4, 580 x4]` -> block 0 = Normal, 1 = Elite, 2 = Ultimate,
#: and within a block the four cells are player counts 1..4 (`characterLifeMultModifier =
#: [0,90,180,270] x3` -- the multiplayer life scaling, which is what makes the inner index the
#: PLAYER COUNT).  Both statements are DECODED from the arrays, not assumed.
DIFFICULTY_NAMES = ("Normal", "Elite", "Ultimate")


def difficulty_cell_label(i: int) -> Tuple[str, int]:
    return DIFFICULTY_NAMES[i // 4], (i % 4) + 1


def difficulty_pak() -> Tuple[Dict[str, List[float]], Dict[str, float], str]:
    """`(arrays, scalars, archive)` for `balancingadjustment_mp+difficulty_enemies01.dbr`."""
    r, arc = E3.winner(DIFF_PATH)
    if r is None:
        raise RuntimeError(f"{DIFF_PATH} absent from Edition-III")
    arrays = {k: [float(x) for x in v] for k, v in r.items()
              if isinstance(v, list) and len(v) > 1}
    scalars = {k: v for k, v in r.items() if not isinstance(v, list)}
    return arrays, scalars, arc


# ══════════════════════════════════════════════════════════════════════════════════════════════
# TARGET 3 -- DoT riders
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: The DoT families, keyed by the `offensiveSlow<STEM>` stem, with the in-game damage name DECODED
#: from `resources/Text_EN.arc :: tags_ui.txt` (see `dot_display_names()`), never spelled from
#: memory.  `is_dot = False` rows are the INSTANT sibling carried for completeness because the
#: commission says "poison/acid" and in this corpus ACID is the instant `offensivePoison*` family
#: while POISON is the over-time `offensiveSlowPoison*` family -- the two are different fields.
DOT_FAMILIES = (
    # (stem,           display key in tags_ui,        is_dot)
    ("Poison",         "DamageDurationPoison",        True),
    ("Bleeding",       "DamageDurationBleeding",      True),
    ("Life",           "DamageDurationLife",          True),
    ("Fire",           "DamageDurationFire",          True),
    ("Cold",           "DamageDurationCold",          True),
    ("Lightning",      "DamageDurationLightning",     True),
    ("Physical",       "DamageDurationPhysical",      True),
    ("LifeLeach",      "DamageDurationLifeLeach",     True),
)
#: The instant families carried beside the DoT ones so "poison/acid" is answered literally.
INSTANT_FAMILIES = (("Poison", "DamagePoison"),)

#: Fields that carry NON-damage over-time effects on the same `offensiveSlow*` prefix -- speed and
#: ability debuffs.  ENUMERATED so they are visibly EXCLUDED rather than silently dropped.
NON_DAMAGE_SLOW_STEMS = (
    "TotalSpeed", "RunSpeed", "AttackSpeed", "CastSpeed",
    "OffensiveAbility", "DefensiveAbility", "OffensiveReduction", "DefensiveReduction",
    "DamageMult", "Manaburn", "ManaBurn", "Energy", "Bloodburst",
)

_SPAWN_PREFIXES = ("spawnObjects", "petBonusName", "summonRecord")
_NEST_FIELDS = ("buffSkillName", "autoCastSkill", "petSkillName")


def dot_display_names() -> Dict[str, str]:
    """`{tag key -> display string}` from `resources/Text_EN.arc :: tags_ui.txt`, DECODED."""
    from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file
    p = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/"
                     "resources/Text_EN.arc")
    a = ArcArchive(p)
    out: Dict[str, str] = {}
    for k, v in parse_tag_file(a.read_file("tags_ui.txt")):
        out[k] = v
    return out


def creature_skill_slots(record: str) -> List[Tuple[str, Optional[str]]]:
    """`[(skill record, skillLevel expression)]` off the creature's OWN tree.  Same read the life
    chain's `Chain.passives` uses (`resolve`), so the rank basis is identical."""
    r, _ = E3.winner(record)
    if not r:
        return []
    out: List[Tuple[str, Optional[str]]] = []
    for i in range(1, 40):
        sn = r.get(f"skillName{i}")
        if not sn:
            continue
        sn = (sn if isinstance(sn, str) else sn[0]).lower().replace("\\", "/")
        out.append((sn, r.get(f"skillLevel{i}")))
    return out


def _refs(rec: dict, prefixes) -> Set[str]:
    out: Set[str] = set()
    for k, val in (rec or {}).items():
        if not str(k).startswith(tuple(prefixes)):
            continue
        for x in (val if isinstance(val, list) else [val]):
            if isinstance(x, str) and x.lower().endswith(".dbr"):
                out.add(x.lower().replace("\\", "/"))
    return out


def skill_closure(record: str, L: float, max_depth: int = 8):
    """`{skill record -> (rank, depth, rank_grade, via)}` -- the full skill closure of one body.

    DEPTH 0 skills come off the creature's own `skillName{i}` / `skillLevel{i}` pairing; their rank
    is `int(ev(skillLevel_i, L))`, the SAME expression the life chain evaluates, so a DoT rank and
    a life-passive rank on the same slot are read at the same index.

    ⚑ DEPTH > 0 RANK IS INHERITED, AND GRADED AS SUCH.  A nested `buffSkillName` /
      `autoCastSkill` / `petSkillName` carries no `skillLevel` of its own on the referring record;
      the referring skill's rank is propagated and the row is graded
      `DERIVED-INHERITED-RANK`.  This is a MODEL CHOICE about rank propagation, not a decode, and
      every consumer can filter on the grade.  Depth-0 rows are `MEASURED-RANK`.

    `spawnObjects*` targets are NOT followed here -- a spawned body is a SEPARATE body with its own
    life and its own skills, and it enters this lap through the summon closure (`pet_bodies`), not
    through its summoner's skill closure.
    """
    out: Dict[str, Tuple[int, int, str, str]] = {}
    frontier: List[Tuple[str, int, int, str, str]] = []
    for sn, sl in creature_skill_slots(record):
        try:
            rank = int(ev(sl, L)) if sl is not None else 1
        except Exception:
            rank = 1
        frontier.append((sn, rank, 0, "MEASURED-RANK", "skillName-slot"))
    depth = 0
    while frontier and depth <= max_depth:
        nxt: List[Tuple[str, int, int, str, str]] = []
        for sn, rank, d, grade, via in frontier:
            prev = out.get(sn)
            if prev is not None and prev[0] >= rank:
                continue
            out[sn] = (rank, d, grade, via)
            s, _ = E3.winner(sn)
            if not s:
                continue
            for f in _NEST_FIELDS:
                for x in (s.get(f) if isinstance(s.get(f), list) else [s.get(f)]):
                    if isinstance(x, str) and x.lower().endswith(".dbr"):
                        t = x.lower().replace("\\", "/")
                        if is_body(t):
                            continue          # a body, not a skill: reached by summon closure
                        nxt.append((t, rank, d + 1, "DERIVED-INHERITED-RANK", f))
            for i in range(1, 41):
                x = s.get(f"skillName{i}")
                if isinstance(x, list):
                    x = x[0] if x else None
                if isinstance(x, str) and x.lower().endswith(".dbr"):
                    t = x.lower().replace("\\", "/")
                    if not is_body(t):
                        nxt.append((t, rank, d + 1, "DERIVED-INHERITED-RANK", f"skillName{i}"))
        frontier = nxt
        depth += 1
    return out


def _idx(arr, rank: int) -> Tuple[int, str]:
    """Rank -> array index, with the OUT-OF-RANGE case NAMED rather than silently clamped.

    GD arrays are frequently SHORTER than the skill's own `skillMaxLevel` (e.g.
    `damage_totaladjuster` carries a 25-cell array with `skillMaxLevel = 60`).  A read past the
    end is a real condition, not an error; it is CLAMPED and the row says so.
    """
    i = int(rank) - 1
    if i < 0:
        return 0, "CLAMPED-LOW"
    if i >= len(arr):
        return len(arr) - 1, "CLAMPED-HIGH"
    return i, "IN-RANGE"


def dot_rows_for_skill(skill: str, rank: int) -> List[dict]:
    """Every DoT family present on ONE skill record at ONE rank."""
    s, arc = E3.winner(skill)
    if not s:
        return []
    rows: List[dict] = []
    for stem, tagkey, is_dot in DOT_FAMILIES:
        mn = s.get(f"offensiveSlow{stem}Min")
        mx = s.get(f"offensiveSlow{stem}Max")
        if mn is None and mx is None:
            continue

        def read(v):
            if v is None:
                return None, "", ""
            if isinstance(v, list):
                if not any(v):
                    return None, "", ""
                i, st = _idx(v, rank)
                return float(v[i]), str(i), st
            return (float(v), "", "SCALAR") if v else (None, "", "")

        v_mn, i_mn, st_mn = read(mn)
        v_mx, i_mx, st_mx = read(mx)
        if v_mn is None and v_mx is None:
            continue
        d_mn = s.get(f"offensiveSlow{stem}DurationMin")
        d_mx = s.get(f"offensiveSlow{stem}DurationMax")

        def rdur(v):
            if v is None:
                return None
            if isinstance(v, list):
                if not any(v):
                    return None
                i, _st = _idx(v, rank)
                return float(v[i])
            return float(v) if v else None

        rows.append(dict(
            skill_record=skill, skill_archive=arc, dot_family=stem, is_dot=is_dot,
            rank=rank,
            array_index_min=i_mn, array_index_max=i_mx,
            index_state=st_mn or st_mx,
            magnitude_min=v_mn, magnitude_max=v_mx,
            duration_min=rdur(d_mn), duration_max=rdur(d_mx),
            chance_pct=(float(s[f"offensiveSlow{stem}Chance"])
                        if s.get(f"offensiveSlow{stem}Chance") else None),
            is_global=bool(s.get(f"offensiveSlow{stem}Global")) or None,
            is_xor=bool(s.get(f"offensiveSlow{stem}XOR")) or None,
            skill_modifier_pct=(float(s[f"offensiveSlow{stem}Modifier"])
                                if isinstance(s.get(f"offensiveSlow{stem}Modifier"), (int, float))
                                and s.get(f"offensiveSlow{stem}Modifier") else None),
            skill_duration_modifier_pct=(
                float(s[f"offensiveSlow{stem}DurationModifier"])
                if isinstance(s.get(f"offensiveSlow{stem}DurationModifier"), (int, float))
                and s.get(f"offensiveSlow{stem}DurationModifier") else None),
            skill_class=str(s.get("Class") or ""),
            skill_max_level=(int(s["skillMaxLevel"]) if s.get("skillMaxLevel") else None),
            array_len_min=(len(mn) if isinstance(mn, list) else None),
        ))
    return rows


def instant_rows_for_skill(skill: str, rank: int) -> List[dict]:
    """The INSTANT `offensivePoison*` (Acid) family -- carried so "poison/acid" is answered."""
    s, arc = E3.winner(skill)
    if not s:
        return []
    rows: List[dict] = []
    for stem, _tag in INSTANT_FAMILIES:
        mn, mx = s.get(f"offensive{stem}Min"), s.get(f"offensive{stem}Max")
        if mn is None and mx is None:
            continue

        def read(v):
            if v is None:
                return None, "", ""
            if isinstance(v, list):
                if not any(v):
                    return None, "", ""
                i, st = _idx(v, rank)
                return float(v[i]), str(i), st
            return (float(v), "", "SCALAR") if v else (None, "", "")
        v_mn, i_mn, st = read(mn)
        v_mx, i_mx, _ = read(mx)
        if v_mn is None and v_mx is None:
            continue
        rows.append(dict(skill_record=skill, skill_archive=arc, dot_family=f"{stem}-INSTANT",
                         is_dot=False, rank=rank, array_index_min=i_mn, array_index_max=i_mx,
                         index_state=st, magnitude_min=v_mn, magnitude_max=v_mx,
                         duration_min=None, duration_max=None,
                         chance_pct=(float(s[f"offensive{stem}Chance"])
                                     if s.get(f"offensive{stem}Chance") else None),
                         is_global=bool(s.get(f"offensive{stem}Global")) or None,
                         is_xor=bool(s.get(f"offensive{stem}XOR")) or None,
                         skill_modifier_pct=None, skill_duration_modifier_pct=None,
                         skill_class=str(s.get("Class") or ""),
                         skill_max_level=(int(s["skillMaxLevel"]) if s.get("skillMaxLevel") else None),
                         array_len_min=(len(mn) if isinstance(mn, list) else None)))
    return rows


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE TOTAL-DAMAGE-MODIFIER term the creature itself grants (the third additive term)
# ══════════════════════════════════════════════════════════════════════════════════════════════

def own_total_damage_modifier(record: str, L: float) -> Tuple[float, List[str]]:
    """`SIGMA_i skill_i.offensiveTotalDamageModifier[rank_i(L)-1]` over the creature's OWN slots.

    The exact structural parallel of `Chain.passive_pct` on the life side, on the damage field.
    Depth-0 slots ONLY, because that is what the life chain sums -- keeping the two chains on the
    same footing is worth more than reaching further on one of them.
    """
    total, src = 0.0, []
    for sn, sl in creature_skill_slots(record):
        s, _ = E3.winner(sn)
        if not s:
            continue
        v = s.get("offensiveTotalDamageModifier")
        if v is None:
            continue
        if isinstance(v, list):
            if not any(v):
                continue
            try:
                rank = int(ev(sl, L)) if sl is not None else 1
            except Exception:
                rank = 1
            i, st = _idx(v, rank)
            if v[i]:
                total += float(v[i])
                src.append(f"{sn.split('/')[-1]}[{i}]={v[i]}({st})")
        elif v:
            total += float(v)
            src.append(f"{sn.split('/')[-1]}={v}")
    return total, src


# ══════════════════════════════════════════════════════════════════════════════════════════════
# POPULATIONS
# ══════════════════════════════════════════════════════════════════════════════════════════════

def rolled_actors(first: int, last: int) -> List[dict]:
    b = json.loads(BATON_20W.read_text())
    return [a for a in b["actors"] if first <= int(a["wave"]) <= last]


def pool_rows(first: int, last: int) -> List[dict]:
    with POOLS_CSV.open() as fh:
        return [r for r in csv.DictReader(fh) if first <= int(r["global_wave"]) <= last]


def pool_population(first: int, last: int):
    """`(rec -> pools, rec -> waves, rec -> slots, rec -> kinds, pools)` -- Lap D's shape."""
    rec_pools: Dict[str, Set[str]] = collections.defaultdict(set)
    rec_waves: Dict[str, Set[int]] = collections.defaultdict(set)
    rec_slot: Dict[str, Set[str]] = collections.defaultdict(set)
    rec_kind: Dict[str, Set[str]] = collections.defaultdict(set)
    pools: Set[str] = set()
    for r in pool_rows(first, last):
        pr = r["pool_record"].lower()
        pools.add(pr)
        w = int(r["global_wave"])
        for col, slot in (("roster_records", "roster"), ("champ_records", "champ")):
            for x in (r.get(col) or "").split("|"):
                x = x.strip().lower()
                if not x:
                    continue
                rec_pools[x].add(pr)
                rec_waves[x].add(w)
                rec_slot[x].add(slot)
                rec_kind[x].add(r.get("pool_kind", ""))
    return rec_pools, rec_waves, rec_slot, rec_kind, pools


def level_sets(pools: Set[str], rec_pools: Dict[str, Set[str]]):
    """Lap D's `band_b_level_sets`, unchanged, over any pool set.  INDEX-PAIRED slot law."""
    lvt = lv_formula_table(E3)
    slot_map = {pr: pool_slot_proxies(E3, pr) for pr in sorted(pools)}
    lvsets: Dict[str, Set[int]] = collections.defaultdict(set)
    proxies: Dict[str, Set[str]] = collections.defaultdict(set)
    for rec, prs in rec_pools.items():
        for pr in prs:
            for lv in slot_map.get(pr, {}).get(rec, ()):
                if lv in lvt:
                    lvsets[rec] |= set(floor_set(lvt, lv, APL_B_PRIME))
                    proxies[rec].add(lv)
    return ({r: sorted(s) for r, s in lvsets.items()},
            {r: sorted(s) for r, s in proxies.items()}, lvt)


def sha256(path: pathlib.Path) -> str:
    import hashlib
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()
