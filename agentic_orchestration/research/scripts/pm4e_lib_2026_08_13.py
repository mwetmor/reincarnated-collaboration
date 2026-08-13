#!/usr/bin/env python3
"""KC2-PM4 Lap E shared library -- DOES THE ROSTER LIFE FOLD REACH A MONSTER-SUMMONED PET?

READ-ONLY on the vendor corpus, the engine tree, and every emission of every prior lap.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE QUESTION (charter L-2, CLIFF C-D1)
═══════════════════════════════════════════════════════════════════════════════════════════════

Lap B priced a monster-summoned pet at `floor(base_life(L) * (1 + tree_pct/100))` -- the GRANTED-
PASSIVE term ONLY.  The roster chain (Lap D, band A) folds two more terms:

    Ultimate/solo difficulty cell   +580.0 %      `mp+difficulty_enemies01.characterLifeModifier[8]`
    Crucible wave term  G(w)        +304..+344 %  `survivalmode_enemies03.characterLifeModifier[w-1]`

Lap D filed C-D1 and declared *"I have no measured evidence either way."*  THIS LAP FOUND THE
EVIDENCE.  It was already inside the positive control Lap D itself used.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE DECODE, IN FOUR LINKS -- each one checked first-hand (GL-12), none adopted from a citation
═══════════════════════════════════════════════════════════════════════════════════════════════

L1. THE DIFFICULTY PAK IS DISPATCHED BY THE BODY'S `Class`, AND THE DISPATCH TABLE IS IN THE DB.
    `records/game/gameengine.dbr` carries THREE class-scoped pak bindings:

        monsterAttributePak -> balancingadjustment_mp+difficulty_enemies01.dbr   (tpl desc:
                               "AttributePak for monster bonuses")      [8] = 580.0
        petAttributePak     -> balancingadjustment_mp+difficulty_pets01.dbr      [8] =  15.0
        playerAttributePak  -> balancingadjustment_mp+difficulty_players01.dbr   (scalar 0.0)

    The three target categories correspond to four body `Class` values, each declared as the
    `defaultValue` of the `Class` field in its own template (decoded from `templates.arc`):

        monster.tpl          Class = "Monster"
        pet.tpl              Class = "Pet"                (includes Monster.tpl)
        petnonscaling.tpl    Class = "PetNonScaling"      (includes Pet.tpl)
        petplayerscaling.tpl Class = "PetPlayerScaling"   (includes Pet.tpl)

L2. EVERY MONSTER-SUMMONED PET BODY ON THIS BOARD IS `Class = Monster`, NOT `Class = Pet*`.
    Measured over all 70 distinct pet bodies of `pm2_tg2_pet_chain.csv`: `{Monster: 70}`,
    `templateName = monster.tpl` on 70/70.  The 53 roster owners are `{Monster: 53}`.  Corpus-wide
    the `Pet` (765) and `PetPlayerScaling` (1244) records live under `records/skills/playerclass*`
    / `devotion` / `itemskills` -- the PLAYER's summons.  So a monster's summon takes the SAME pak
    binding as the roster body that summoned it.

L3. THE SURVIVAL (Crucible) TERM HAS NO CLASS DISPATCH AT ALL.
    `records/game/survivalinfo.dbr` binds exactly THREE adjustments -- `survivalAdjustment`
    {Normal,Elite,Ultimate} -> `balancingadjustment_survivalmode_enemies0{1,2,3}.dbr`, tpl
    description "GameAdjustment".  There is NO pet variant and NO player variant; `survivalinfo.tpl`
    carries no other adjustment field.  `gameadjustment.tpl` is `attributepak.tpl` + four spawn-COUNT
    fields (`spawnMinAdj`, `spawnMaxAdj`, `spawnChampionMinAdj`, `spawnChampionMaxAdj`).

L4. ⚑ THE POSITIVE CONTROL -- FOUR CAMERA-MEASURED SKILL-SPAWNED PETS, AND THEY DECIDE IT.
    `data/kc2/t21_wave160_board_ehp_r2.csv` carries 8 rows with an INDEPENDENT `measured` eHP
    (`verdict = EXACT`; the other 31 rows are `PREDICTION-uncorroborated`).  FOUR of those eight
    are `proxy = "(none - skill-spawned pet)"`.  Recomputed here from the corpus at their
    camera-measured levels, all four reproduce their measured eHP EXACTLY under the FULL fold, and
    every discriminating alternative fails:

        body                 L    measured   FULL(580+G+p)   no-ULT   no-G    Lap-B (passives only)
        Death Revenant     109     468,504       468,504 ✓  227,820  334,053         93,368
        Skeletal Archer    109      41,237        41,237 ✓   19,767   29,244          7,773
        Aleksander's Shard 109     103,912       103,912 ✓   50,529   74,091         20,708
        Aetherial Bileeater112     484,095       484,095 ✓  236,279  345,660         97,844

    This is not an argument from naming.  It is four bodies whose life was read off the real game
    and which are reproducible ONLY with both folds applied.

⇒ THE RULE THIS LAP EMITS IS THE ROSTER CHAIN, UNCHANGED, WITH ONE INDEX MOVED (the level source):

       base_life(L)   = bio.characterLife  at charLevel = L, L = THE OWNER'S level (see L5)
       passive_pct(L) = SIGMA_i skill_i.characterLifeModifier[ int(skillLevel_i(L)) - 1 ]
       eHP(w, L)      = floor( base_life(L) * (1 + (580.0 + G[w-1] + passive_pct(L)) / 100) )

L5. THE LEVEL SOURCE.  `character.tpl`'s `charLevel` field is described *"Equation used to
    determine level if this character is placed in the world MANUALLY."*  A summoned body is not
    placed manually, and NO spawn-pet skill template carries a level field at all (checked on all
    seven spawn-skill classes present on this board).  Measured against the camera: the pet enters
    at its OWNER'S level, and its own `charLevel` equation is NOT applied --
    Death Revenant (`charLevel*1+2`) and Aleksander's Shard (`charLevel*1+3`) both enter at 109,
    their owners' level, not at 111 / 112.  ONE body dissents and is NOT explained away: see
    CLIFF C-E1 in the README.

⚑ THIS MODULE RE-IMPLEMENTS NOTHING.  It imports Lap D's `pm4d_lib`, which itself imports band A's
  `Chain`/`resolve`/`ev` and the stat-fold level machinery.  A second implementation of the same
  chain is a second thing that can drift (gamora's rule at the band-A lap; it binds here too).

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, iteration I-2, Lap E.
"""
from __future__ import annotations

import collections
import csv
import math
import pathlib
import sys
from typing import Dict, List, Sequence, Set, Tuple

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
ENGINE = pathlib.Path("/Users/admin/Games/reincarnated-engine")
sys.path.insert(0, str(META / "agentic_orchestration" / "research" / "scripts"))

# Lap D's library, imported. Same reader (`Ed.winner`, whole-record replacement), same chain,
# same failure taxonomy, same array-lookup law.
from pm4d_lib_2026_08_13 import (  # noqa: E402
    E3, BAND_B_FIRST, BAND_B_LAST, LifeRow, build_life_row, dump_csv,
    G_at, pool_population, band_b_level_sets, sha256_of,
    summon_closure_extended, survival_life_modifier_array, ultimate_life_modifier_pct,
)

DATA = ENGINE / "data" / "kc2"
LAPD = META / "agentic_orchestration" / "legolas" / "notes" / "2026-08-13-kc2-pm4-lap-d-roster-ehp"

PET_CHAIN_CSV = DATA / "pm2_tg2_pet_chain.csv"          # Lap B's emission (the 70-body basis)
BOARD_R2_CSV = DATA / "t21_wave160_board_ehp_r2.csv"    # the camera-measured positive control
LAPD_LIFE_CSV = LAPD / "pm4d_band_b_monster_life.csv"
LAPD_EHP_CSV = LAPD / "pm4d_band_b_ehp_by_wave.csv"

#: The `gameengine.dbr` class-scoped pak dispatch table (L1). Decoded, not spelled from memory.
GAMEENGINE = "records/game/gameengine.dbr"
SURVIVALINFO = "records/game/survivalinfo.dbr"
PAK_FIELDS = ("monsterAttributePak", "petAttributePak", "playerAttributePak")

#: `Class` values that take `monsterAttributePak`. Measured: all 70 pet bodies are in this set.
MONSTER_PAK_CLASSES = frozenset({"Monster"})
#: `Class` values that take `petAttributePak`.
PET_PAK_CLASSES = frozenset({"Pet", "PetNonScaling", "PetPlayerScaling"})


# ══════════════════════════════════════════════════════════════════════════════════════════════
# L1 / L3 -- THE DISPATCH SURFACE, DECODED FROM THE RECORDS
# ══════════════════════════════════════════════════════════════════════════════════════════════

def pak_dispatch() -> Dict[str, str]:
    """`{gameengine field -> pak record}` for the three class-scoped difficulty paks."""
    r, _arc = E3.winner(GAMEENGINE)
    if r is None:
        raise RuntimeError(f"{GAMEENGINE} absent -- the pak dispatch cannot be decoded")
    return {f: str(r.get(f) or "") for f in PAK_FIELDS}


def survival_dispatch() -> Dict[str, str]:
    """`{survivalinfo field -> GameAdjustment record}`. THREE fields, all `_enemies`; no pet
    variant exists -- that absence is a measurement and it is reported, not assumed away."""
    r, _arc = E3.winner(SURVIVALINFO)
    if r is None:
        raise RuntimeError(f"{SURVIVALINFO} absent -- the survival term has no binding")
    return {k: str(v) for k, v in r.items() if k.startswith("survivalAdjustment")}


def pak_life_pct(pak_record: str, index: int) -> float:
    """One cell of an AttributePak's `characterLifeModifier`. Scalars are returned as-is."""
    r, _arc = E3.winner(pak_record)
    v = (r or {}).get("characterLifeModifier")
    if isinstance(v, list):
        return float(v[index])
    return float(v if isinstance(v, (int, float)) else 0.0)


def body_class(record: str) -> str:
    r, _arc = E3.winner(record)
    return str((r or {}).get("Class") or "<absent>")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE PET POPULATION -- NOTE-9: two bases, and they are NOT the same size
# ══════════════════════════════════════════════════════════════════════════════════════════════

def lapb_pet_rows() -> List[dict]:
    """`pm2_tg2_pet_chain.csv`, status=OK. The (owner, skill, pet) EDGE grain -- 149 rows."""
    with PET_CHAIN_CSV.open() as fh:
        return [r for r in csv.DictReader(fh) if (r.get("status") or "") == "OK"]


def lapb_pet_bodies() -> List[str]:
    """P-PET-70: the 70 distinct pet RECORDS of Lap B's chain. The commission's declared basis."""
    return sorted({r["pet_record"] for r in lapb_pet_rows() if r.get("pet_record")})


def owners_of_lapb() -> Dict[str, Set[str]]:
    """`{pet record -> {owner record}}` from Lap B's EDGE rows."""
    out: Dict[str, Set[str]] = collections.defaultdict(set)
    for r in lapb_pet_rows():
        if r.get("pet_record") and r.get("owner_record"):
            out[r["pet_record"]].add(r["owner_record"])
    return out


def summon_only_bodies() -> Tuple[List[str], List[str]]:
    """`(P-SUMMON-128, the 58 Lap B misses)`.

    ⚑ IS-E1, MEASURED.  P-PET-70 is Lap B's chain output and it is NOT the summon population.
    Running Lap D's EXTENDED closure to fixpoint over the 663 band-B pool records reaches 791
    bodies, of which **128 are summon-only** (reachable only as a spawn target, never as a pool
    roster/champ record).  Lap B's chain reaches **70** of those 128.  All 128 carry
    `Class = Monster`, so the Lap E verdict generalises over the whole set, not just the 70.

    The 58 it misses include `aetherialbloater_b01_summon` -- which is one of the FOUR
    camera-measured positive controls this lap's verdict rests on.  A population that omits a body
    whose life was read off the real game is a population worth correcting.
    """
    rec_pools, _rw, _rs, _rk, _pools = pool_population()
    pool_set = set(rec_pools)
    bodies, _layers, _summ = summon_closure_extended(pool_set)
    summon_only = sorted(b for b in bodies if b not in pool_set)
    lapb = set(lapb_pet_bodies())
    return summon_only, sorted(b for b in summon_only if b not in lapb)


def closure_summoners() -> Dict[str, Set[str]]:
    """`{summon body -> {summoner}}` from Lap D's EXTENDED closure over the band-B pool population.

    ⚑ IS-E1.  This reaches edges Lap B's chain does not.  `aetherialbloater_b01_summon` -- one of
    the four camera-measured positive controls -- has ZERO owner edges in `pm2_tg2_pet_chain.csv`,
    yet `aetherialcolossus_galakros.skillName12` -> `galakros_summonbloater_secondary.dbr`
    -> `spawnObjects` reaches it.  Reported, not silently patched over Lap B's basis.
    """
    rec_pools, _rw, _rs, _rk, _pools = pool_population()
    _bodies, _layers, summoner_of = summon_closure_extended(set(rec_pools))
    return {k: set(v) for k, v in summoner_of.items()}


def owner_level_sets() -> Tuple[Dict[str, List[int]], Dict[str, Set[str]]]:
    """`(pet -> sorted owner-derived level list, pet -> summoners)`.

    L5: the pet enters at its OWNER'S level.  The owner's level set is Lap D's band-B pool
    floor-set (`MEASURED-SET`, index-paired slot law).  A pet with several possible owners
    inherits the UNION -- a set, never a midpoint (the C-1 prescription).  Depth-2 pets (a pet
    that summons a pet) inherit transitively, run to fixpoint.
    """
    rec_pools, _rw, _rs, _rk, pools = pool_population()
    lvsets, _slot, _prox, _lvt = band_b_level_sets(pools, rec_pools)
    summoner_of = closure_summoners()
    for pet, owners in owners_of_lapb().items():          # union Lap B's edges in
        summoner_of.setdefault(pet, set()).update(owners)

    resolved: Dict[str, Set[int]] = {r: set(v) for r, v in lvsets.items()}
    for _ in range(12):                                    # fixpoint; depth is bounded and small
        moved = False
        for body, owners in summoner_of.items():
            inherit: Set[int] = set()
            for o in owners:
                inherit |= set(resolved.get(o, ()))
            if inherit and not inherit <= set(resolved.get(body, ())):
                resolved.setdefault(body, set()).update(inherit)
                moved = True
        if not moved:
            break
    return ({r: sorted(v) for r, v in resolved.items()}, summoner_of)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE FOLD -- the roster chain, applied to a pet body
# ══════════════════════════════════════════════════════════════════════════════════════════════

def pet_ehp(row: LifeRow, wave: int, L: int, surv: Sequence[float], ult: float):
    """`floor(base_life(L) * (1 + (ult + G[w-1] + passive_pct(L)) / 100))`.

    Identical expression to Lap D's `LifeRow.ehp`; called through the same object so there is one
    implementation.  Kept as a named function only so the verifier can re-derive independently.
    """
    return row.ehp(wave, L, surv, ult)


def lapb_life(row_edges: Sequence[dict]) -> Dict[str, float]:
    """`{pet record -> Lap-B `pet_life_at_owner_level`}`. The value the sim carries TODAY.

    Lap B emits one value per EDGE; a record on several edges can carry several values (different
    owners => different levels).  This takes the MINIMUM per record, which is the softest body the
    sim could be fielding, so the hardening ratio reported against it is a LOWER bound on the
    correction.  The full per-edge spread rides `pm4e_pet_life_decode.csv`.
    """
    agg: Dict[str, List[float]] = collections.defaultdict(list)
    for r in row_edges:
        v = (r.get("pet_life_at_owner_level") or "").strip()
        if r.get("pet_record") and v:
            try:
                agg[r["pet_record"]].append(float(v))
            except ValueError:
                pass
    return {k: min(v) for k, v in agg.items() if v}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE POSITIVE CONTROL -- L4
# ══════════════════════════════════════════════════════════════════════════════════════════════

def camera_measured_pets() -> List[dict]:
    """The rows of `t21_wave160_board_ehp_r2.csv` that are BOTH skill-spawned pets AND carry an
    independent `measured` eHP. Four of them. This is the evidence Lap D said it did not have."""
    with BOARD_R2_CSV.open() as fh:
        rows = list(csv.DictReader(fh))
    return [r for r in rows
            if (r.get("measured") or "").strip() and "skill-spawned" in (r.get("proxy") or "")]


def control_table(wave: int = 160) -> List[dict]:
    """Recompute each camera-measured pet FOUR ways and report which one reproduces the measurement.

    The three counterfactuals are the point: a fold that matches under all of them proves nothing.
    """
    surv = survival_life_modifier_array()
    ult = ultimate_life_modifier_pct()
    g = G_at(surv, wave)
    out = []
    for r in camera_measured_pets():
        rec = r["record"].lower()
        L = int(float(r["charLevel"]))
        meas = int(float(r["measured"]))
        lr = build_life_row(rec, [L])
        base, pas = lr.base_life(L), lr.passive_pct(L)
        if base is None or pas is None:
            out.append(dict(body=r["body"], record=rec, level=L, measured=meas,
                            verdict="CHAIN-UNRESOLVED"))
            continue
        f = lambda pct: math.floor(base * (1.0 + pct / 100.0))   # noqa: E731
        out.append(dict(
            body=r["body"], record=rec, level=L, level_grade=r.get("charLevel_grade", ""),
            base_life=round(base, 4), passive_pct=pas, ult_pct=ult, g_pct=g, measured=meas,
            ehp_full=f(ult + g + pas), ehp_without_ultimate=f(g + pas),
            ehp_without_g=f(ult + pas), ehp_lapb_passives_only=f(pas),
            verdict="EXACT" if f(ult + g + pas) == meas else "MISMATCH",
        ))
    return out


def read_lapd_ehp() -> Dict[Tuple[str, int], Tuple[int, int]]:
    """Lap D's `(record, wave) -> (lo, hi)`. Used ONLY as a cross-check target, never as a source."""
    out: Dict[Tuple[str, int], Tuple[int, int]] = {}
    with LAPD_EHP_CSV.open() as fh:
        for r in csv.DictReader(fh):
            lo, hi = (r.get("ehp_lo") or "").strip(), (r.get("ehp_hi") or "").strip()
            if lo and hi:
                out[(r["record"], int(r["wave"]))] = (int(float(lo)), int(float(hi)))
    return out
