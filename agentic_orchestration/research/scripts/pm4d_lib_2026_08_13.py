#!/usr/bin/env python3
"""KC2-PM4 Lap D shared library -- BAND-B (Crucible waves 151-170) monster LIFE chain.

READ-ONLY on the vendor corpus and on the engine tree.

═══════════════════════════════════════════════════════════════════════════════════════════════
WHAT THIS EXTENDS, AND WHY IT IMPORTS RATHER THAN RE-IMPLEMENTS
═══════════════════════════════════════════════════════════════════════════════════════════════

The band-A life table (`data/kc2/t22_band_a_monster_stats.csv`) is emitted by
`simulation/scripts/gamora_kc2_stat_fold_ed3_2026_08_08.py`, whose life chain is in turn imported
verbatim from `gamora_kc2_c1_closure_ed3_2026_08_08.py` (the C-1 closure).  THIS MODULE IMPORTS
THE SAME TWO MODULES.  A second implementation of the same chain is a second thing that can
drift -- gamora's own words at the band-A lap, and they bind here.

Consequence: `Ed.winner()` (WHOLE-RECORD REPLACEMENT, the L-33/C-9 overlay law) is the reader,
not `Ed.merged()`.

  ⚑ IS-B1 -- INSTRUMENT-SCHEMA CORRECTION AGAINST MY OWN LAP-B BASIS.  `s2_lib.E3.merged()`
    (Lap B, 2026-08-12) does a LAST-WINS FIELD MERGE across the eight archives.  L-33/C-9 ruled
    the overlay to be whole-record replacement: a field-merge RESURRECTS deliberately-deleted
    fields (that is precisely how Kubacabra's stripped death-spawn chain would have haunted the
    model).  This lap therefore does NOT use the Lap-B reader for the life chain.  The Lap-B
    roster BASIS (which records) is still used; only the record READER changed.  The two readers
    are diffed in `reader_delta()` so the correction is priced, not asserted.

═══════════════════════════════════════════════════════════════════════════════════════════════
THE CHAIN (band A's, verbatim; ONE index moves)
═══════════════════════════════════════════════════════════════════════════════════════════════

    base_life(L)   = bio.characterLife            evaluated at charLevel = L
    passive_pct(L) = SIGMA_i  skill_i.characterLifeModifier[ int(skillLevel_i(L)) - 1 ]
    SIGMA(w, L)    = 580.0  +  G[w-1]  +  passive_pct(L)
    eHP(w, L)      = floor( base_life(L) * (1 + SIGMA(w, L) / 100) )

  580.0 = `balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8]` (Ultimate/solo)
  G     = `balancingadjustment_survivalmode_enemies03.characterLifeModifier`, read at index w-1
          under the S 10.7 / L-33 ARRAY-LOOKUP LAW (fighting wave w reads the cell LABELED w).

  ⚑ The creature's OWN `characterLifeModifier` is NOT folded.  Band A does not fold it either
    (`Chain.ehp` sums bio + difficulty + survival + granted-passives only), and L-33(b) falsified
    it on camera -- `t21_wave160_board_ehp_r2.csv` carries `own_applied = NO` on every row.  It is
    EMITTED as a column so the exclusion stays inspectable; it is never summed.

Band A is the SAME expression at waves 1..93.  Nothing about band B changes the arithmetic; what
changes is that `G` runs 306..344 instead of 95..156, and that the roster is a different set.

Author: legolas (UNKNOWN-RESEARCHER), 2026-08-13.  Run KC2-PM4, iteration I-1, Lap D.
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

# THE BAND-A CHAIN, IMPORTED. Not re-implemented.
from gamora_kc2_c1_closure_ed3_2026_08_08 import (  # noqa: E402
    E3, Chain, resolve, constants, ev,
)
from gamora_kc2_stat_fold_ed3_2026_08_08 import (   # noqa: E402
    lv_formula_table, floor_set, pool_slot_proxies, summon_targets, APL_B_PRIME,
)

DATA = ENGINE / "data" / "kc2"
OUTPUT = ENGINE / "src" / "reincarnated" / "output"

# ══════════════════════════════════════════════════════════════════════════════════════════════
# POPULATION BASES -- every count in this lap asserts which of these it counts over (NOTE-9)
# ══════════════════════════════════════════════════════════════════════════════════════════════

#: The FROZEN 20-wave baton of record.  Its `actors[]` is the roll that PM-2/PM-3 inherit.
BATON_20W = OUTPUT / "kc2-baton-v1-E-s09-cp150-20260809_052836.json"

#: The PM-3 fight-cell batons.  They stop at the death wave (156), so they are a SUBSET of the
#: frozen roll and are used only as an agreement check, never as the roster basis.
PM3_BATONS = sorted(OUTPUT.glob("kc2-baton-v1-E-s09-cp150-pm3-*.json"))

POOLS_CSV = DATA / "pe6_crucible_wave_pools_v2.csv"
WAVES_CSV = DATA / "pe6_crucible_waves.csv"
BOARD160_CSV = DATA / "t21_wave160_board_ehp_r2.csv"
BAND_A_CSV = DATA / "t22_band_a_monster_stats.csv"
SCALING_CSV = DATA / "halt9_survival_wave_scaling_full.csv"

#: BAND B, as this lap defines it.  151 is the first wave of the E-s09-cp150 sitting; 170 is the
#: last wave the frozen baton rolls (`run_summary.final_wave = 170`, `arena_tier_exhausted`).
BAND_B_FIRST, BAND_B_LAST = 151, 170
#: The sub-band PM-3 S 5 measured its 188 bodies over.
PM3_BAND_FIRST, PM3_BAND_LAST = 151, 160

DIFF_PATH = "records/game/balancingadjustment_mp+difficulty_enemies01.dbr"
SURV_PATH = "records/game/balancingadjustment_survivalmode_enemies03.dbr"
#: Ultimate / solo cell.  Same index band A's life chain reads.
DIFFICULTY_INDEX = 8


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE WAVE-SCALING ARRAY -- DECODED HERE, from the record, not read from any CSV
# ══════════════════════════════════════════════════════════════════════════════════════════════

def survival_life_modifier_array() -> List[float]:
    """`survivalmode_enemies03.characterLifeModifier`, decoded first-hand (GL-12).

    200 cells.  The consumer indexes at `wave - 1` (S 10.7 / L-33: fighting wave `w` reads the
    cell LABELED `w`).  NOT read from `halt9_survival_wave_scaling_full.csv` -- that CSV is
    CHECKED against this decode in `pm4d_verify`, which is the opposite direction of trust.
    """
    s, _arc = E3.winner(SURV_PATH)
    if s is None:
        raise RuntimeError(f"{SURV_PATH} absent from Edition-III -- the band-B fold has no G")
    return [float(x) for x in s["characterLifeModifier"]]


def ultimate_life_modifier_pct() -> float:
    """`balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8]` -- decoded."""
    d, _arc = E3.winner(DIFF_PATH)
    return float(d["characterLifeModifier"][DIFFICULTY_INDEX])


def G_at(surv: Sequence[float], wave: int) -> float:
    """The array-lookup law, TOTAL on [1, len(surv)], NO CLAMP.

    A clamp here would answer an out-of-band question silently and wrongly -- the F-7 finding the
    band-A module carries, applied to band B.
    """
    w = int(wave)
    if not (1 <= w <= len(surv)):
        raise ValueError(f"wave {w} outside the survival array's domain [1, {len(surv)}]")
    return float(surv[w - 1])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# ROSTER BASES
# ══════════════════════════════════════════════════════════════════════════════════════════════

def rolled_actors(baton: pathlib.Path = BATON_20W,
                  first: int = BAND_B_FIRST, last: int = BAND_B_LAST) -> List[dict]:
    """Every `actors[]` row of `baton` whose wave is in [first, last].  The ROLLED population."""
    b = json.loads(baton.read_text())
    return [a for a in b["actors"] if first <= int(a["wave"]) <= last]


def rolled_records(baton: pathlib.Path = BATON_20W,
                   first: int = BAND_B_FIRST, last: int = BAND_B_LAST) -> Dict[str, dict]:
    """`{record -> facts}` over the rolled population.  Records, not actors -- the two counts
    differ and every assertion in this lap says which it is using."""
    agg: Dict[str, dict] = collections.OrderedDict()
    for a in rolled_actors(baton, first, last):
        rp = a["record_path"].lower()
        e = agg.setdefault(rp, dict(record=rp, display_name=a["display_name"],
                                    n_actors=0, n_champion=0, waves=set(),
                                    baton_levels=set(), baton_hp_max=set(),
                                    threat_tiers=set(), archetype_tags=set()))
        e["n_actors"] += 1
        e["n_champion"] += 1 if a.get("is_champion") else 0
        e["waves"].add(int(a["wave"]))
        if a.get("level") is not None:
            e["baton_levels"].add(int(a["level"]))
        if a.get("hp_max") is not None:
            e["baton_hp_max"].add(float(a["hp_max"]))
        if a.get("threat_tier"):
            e["threat_tiers"].add(a["threat_tier"])
        if a.get("archetype_tag"):
            e["archetype_tags"].add(a["archetype_tag"])
    return agg


def pool_rows(first: int = BAND_B_FIRST, last: int = BAND_B_LAST) -> List[dict]:
    with POOLS_CSV.open() as fh:
        return [r for r in csv.DictReader(fh) if first <= int(r["global_wave"]) <= last]


def pool_population(first: int = BAND_B_FIRST, last: int = BAND_B_LAST):
    """`(record -> {pool_record}, record -> {wave}, record -> {'roster'|'champ'}, pools)`.

    The POOL population: every record any band-B pool can put on the board, regardless of whether
    this run's seed drew it.  Future-proofs the band against a re-roll (charter L-0).
    """
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


def summon_closure(seed_records: Set[str]) -> Tuple[Set[str], List[int]]:
    """Band A's summon closure, run to FIXPOINT on the band-B seed set.

    `summon_targets` is imported from the band-A instrument unchanged, so the SAME edges are
    walked (spawnObjects* / petBonusName / summonRecord / buffSkillName+petSkillName one hop) and
    the SAME edge is excluded (`poolToSpawnOnDeath`, Crucible-stripped, L-33(h)).
    """
    seen = set(seed_records)
    frontier = set(seed_records)
    layers: List[int] = []
    while frontier:
        nxt: Set[str] = set()
        for r in sorted(frontier):
            nxt |= summon_targets(E3, r)
        nxt -= seen
        if not nxt:
            break
        layers.append(len(nxt))
        seen |= nxt
        frontier = nxt
    return seen, layers


# ══════════════════════════════════════════════════════════════════════════════════════════════
# IS-B2 -- THE EXTENDED CLOSURE. Band A's closure UNDER-REACHES, and the shortfall is MEASURED.
# ══════════════════════════════════════════════════════════════════════════════════════════════
#
# Band A's `summon_targets` walks `buffSkillName` / `petSkillName` exactly ONE hop, never follows
# `autoCastSkill` at all, and drops any target without `/creatures/` in its path.  Measured
# against Lap B's own pet chain (`pm2_tg2_pet_chain.csv`, 70 distinct pet bodies, life 149/149
# MEASURED), band A's closure MISSES 29 of them.  Two mechanisms, both read off the chain:
#
#   (i)  NESTED SKILL REFS (Lap B's IS-4).  `witchgod_finalboss` reaches
#        `bonerat_witchgod_a01_summon` through `tree+nested` -- a granted skill whose
#        `buffSkillName`/`autoCastSkill` points at a SECOND skill that carries the `spawnObjects`.
#        One hop is not enough; Lap B measured the chain running to depth 6.
#   (ii) SKILL-RECORD PET CARRIERS.  `records/skills/.../pets/pet_eldritchrift_02.dbr` is a pet
#        whose own skill tree spawns `korvaakservant_b01_korvaaksummon`.  Band A's `/creatures/`
#        filter drops the CARRIER, so the creature behind it is never reached.
#
# IS-B3 -- AND THE ADMISSION PREDICATE IS `Class`, NOT PATH.  Restoring the two edges above still
# left 18 of Lap B's 70 pet bodies unreached, and every one of them lives under
# `records/skills/.../pets/` while carrying `Class = Monster` -- which is Lap B's IS-3 finding
# verbatim ("15 of the 57 pet creature records live under `records/skills/.../pets/` yet carry
# `Class = Monster`; a path-prefix classifier drops them, and equally MISCOUNTS loot chests
# (`Class = Destructible` / `FixedItemContainer`) as summons").  Band A's `/creatures/` path filter
# is that error.  Admission here is by the TARGET RECORD'S OWN `Class`, so the loot-chest half of
# Lap B's finding is guarded too.

_SPAWN_PREFIXES = ("spawnObjects", "petBonusName", "summonRecord")
_NEST_FIELDS = ("buffSkillName", "autoCastSkill", "petSkillName")

#: `Class` values that ARE a body on the board.  Measured off the corpus, not spelled from memory:
#: see `class_census()` below, which is what chose this set.
BODY_CLASSES = frozenset({"Monster"})


def is_body(path: str) -> bool:
    """IS-B3 admission predicate: the record's own `Class`, never its path."""
    r, _ = E3.winner(path)
    return bool(r) and str(r.get("Class") or "") in BODY_CLASSES


def class_census(paths) -> Dict[str, int]:
    """`{Class -> n}` over spawn targets -- the measurement BODY_CLASSES is chosen from."""
    c: Dict[str, int] = collections.Counter()
    for p in paths:
        r, _ = E3.winner(p)
        c[str((r or {}).get("Class") or "<absent>")] += 1
    return dict(c)


def _refs(rec: dict, prefixes) -> Set[str]:
    out: Set[str] = set()
    for k, val in (rec or {}).items():
        if not str(k).startswith(tuple(prefixes)):
            continue
        for x in (val if isinstance(val, list) else [val]):
            if isinstance(x, str) and x.lower().endswith(".dbr"):
                out.add(x.lower().replace("\\", "/"))
    return out


def _skill_tree(rec: dict) -> Set[str]:
    out: Set[str] = set()
    for i in range(1, 41):
        sn = (rec or {}).get(f"skillName{i}")
        if isinstance(sn, list):
            sn = sn[0] if sn else None
        if isinstance(sn, str) and sn.lower().endswith(".dbr"):
            out.add(sn.lower().replace("\\", "/"))
    return out


def summon_closure_extended(seed_records: Set[str]) -> Tuple[Set[str], List[int], Dict[str, Set[str]]]:
    """`(bodies, layer_sizes, summoner_of)` -- the closure with IS-B2's two edges restored.

    `poolToSpawnOnDeath` remains EXCLUDED (L-33(h) -- the Crucible strips campaign death-spawn
    wiring; walking it would resurrect bodies the Crucible never spawns).  That exclusion is band
    A's and it is kept deliberately; it is the one edge this extension does NOT restore.
    """
    bodies = set(seed_records)
    summoner_of: Dict[str, Set[str]] = collections.defaultdict(set)
    frontier = set(seed_records)
    layers: List[int] = []
    while frontier:
        nxt_bodies: Set[str] = set()
        for owner in sorted(frontier):
            r, _ = E3.winner(owner)
            if not r:
                continue
            # skills reachable from this body: its tree, plus nested refs to fixpoint
            skills = _skill_tree(r) | _refs(r, _SPAWN_PREFIXES + _NEST_FIELDS)
            seen_sk: Set[str] = set()
            sk_frontier = set(skills)
            while sk_frontier:
                nxt_sk: Set[str] = set()
                for sp in sorted(sk_frontier):
                    if sp in seen_sk:
                        continue
                    seen_sk.add(sp)
                    s, _ = E3.winner(sp)
                    if not s:
                        continue
                    for t in _refs(s, _SPAWN_PREFIXES):
                        if is_body(t):
                            if t not in bodies:
                                nxt_bodies.add(t)
                            summoner_of[t].add(owner)
                        else:
                            # not a body: a skill-record CARRIER (traverse) or a loot chest
                            # (`Destructible` / `FixedItemContainer` -- traversal is harmless,
                            # admission is what IS-B3 guards).
                            nxt_sk.add(t)
                    nxt_sk |= _refs(s, _NEST_FIELDS) | _skill_tree(s)
                sk_frontier = nxt_sk - seen_sk
            # direct spawn refs on the body record itself
            for t in _refs(r, _SPAWN_PREFIXES):
                if is_body(t):
                    if t not in bodies:
                        nxt_bodies.add(t)
                    summoner_of[t].add(owner)
        nxt_bodies -= bodies
        if not nxt_bodies:
            break
        layers.append(len(nxt_bodies))
        bodies |= nxt_bodies
        frontier = nxt_bodies
    return bodies, layers, summoner_of


# ══════════════════════════════════════════════════════════════════════════════════════════════
# LEVEL FLOOR-SETS for band B -- the C-1 prescription: `L` is a SET, never a midpoint
# ══════════════════════════════════════════════════════════════════════════════════════════════

def band_b_level_sets(pools: Set[str], rec_pools: Dict[str, Set[str]]):
    """`(record -> sorted level list, slot_map, proxies_used)` over the band-B pools.

    INDEX-PAIRED SLOT LAW (band A S E, imported): a pool pairs `nameN` with
    `levelVarianceEquationN` and `nameChampionN` with `levelVarianceEquationChampionN`.  The proxy
    is a property of the SLOT, not of the pool.  Unioning every `levelVarianceEquation*` on the
    pool is the error band A's own positive control caught (894/895 rows wrong).
    """
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
    return ({r: sorted(s) for r, s in lvsets.items()}, slot_map,
            {r: sorted(s) for r, s in proxies.items()}, lvt)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE LIFE FOLD
# ══════════════════════════════════════════════════════════════════════════════════════════════

class LifeRow:
    """One record's resolved band-B life surface.  Every link's grade rides on the row."""

    __slots__ = ("record", "chain", "levels", "level_grade", "level_source",
                 "own_life_modifier_pct", "monster_class", "archive", "life_grade")

    def __init__(self, record: str) -> None:
        self.record = record
        self.chain: Optional[Chain] = None
        self.levels: List[int] = []
        self.level_grade = ""
        self.level_source = ""
        self.own_life_modifier_pct = 0.0
        self.monster_class = ""
        self.archive = ""
        self.life_grade = ""

    # ---- the four links -------------------------------------------------------------------
    def base_life(self, L: int) -> Optional[float]:
        if not (self.chain and self.chain.ok):
            return None
        try:
            return float(self.chain.base_life(float(L)))
        except Exception:
            return None

    def passive_pct(self, L: int) -> Optional[float]:
        if not (self.chain and self.chain.ok):
            return None
        try:
            pct, _src = self.chain.passive_pct(E3, float(L))
            return float(pct)
        except Exception:
            return None

    def passive_sources(self, L: int) -> List[str]:
        if not (self.chain and self.chain.ok):
            return []
        try:
            _pct, src = self.chain.passive_pct(E3, float(L))
            return list(src)
        except Exception:
            return []

    def ehp(self, wave: int, L: int, surv: Sequence[float], ult: float) -> Optional[int]:
        base = self.base_life(L)
        pas = self.passive_pct(L)
        if base is None or pas is None:
            return None
        sigma = ult + G_at(surv, wave) + pas
        return math.floor(base * (1.0 + sigma / 100.0))


def build_life_row(record: str, levels: Sequence[int]) -> LifeRow:
    """Resolve one record.  `resolve` is band A's, imported -- same reader, same failure taxonomy."""
    row = LifeRow(record)
    row.levels = sorted(set(int(x) for x in levels))
    c = resolve(E3, record)
    row.chain = c
    r, arc = E3.winner(record)
    row.archive = arc or ""
    if r is not None:
        row.monster_class = str(r.get("monsterClassification") or "")
        own = r.get("characterLifeModifier")
        if isinstance(own, list):
            own = own[0] if own else 0.0
        row.own_life_modifier_pct = float(own) if isinstance(own, (int, float)) else 0.0
    if not c.ok:
        # NAMED GAP.  GL-12: no estimate, no sibling fill, no modal fallback.
        row.life_grade = f"ABSENT:{c.reason}"
    elif not row.levels:
        row.life_grade = "ABSENT:NO-LEVEL-SOURCE (bio resolves; no band-B pool slot cites a proxy)"
    else:
        row.life_grade = "MEASURED"
    return row


# ══════════════════════════════════════════════════════════════════════════════════════════════
# THE READER DELTA -- IS-B1, priced rather than asserted
# ══════════════════════════════════════════════════════════════════════════════════════════════

def reader_delta(records: Sequence[str]) -> Dict[str, object]:
    """How many band-B records READ DIFFERENTLY under merge vs whole-record replacement.

    Imports the Lap-B merge reader on purpose, so the correction has a magnitude.
    """
    sys.path.insert(0, str(META / "agentic_orchestration" / "legolas" / "notes"
                          / "2026-08-12-kc2-roster-decode-completion"))
    from s2_lib import E3 as E3_MERGE  # noqa: E402  (the Lap-B field-merge reader)
    differ, same, absent = [], 0, 0
    for rec in records:
        w, _ = E3.winner(rec)
        m, _ = E3_MERGE.merged(rec)
        if w is None or not m:
            absent += 1
            continue
        if set(w.keys()) != set(m.keys()):
            extra = sorted(set(m.keys()) - set(w.keys()))
            differ.append({"record": rec, "n_winner_fields": len(w), "n_merged_fields": len(m),
                           "fields_merge_resurrects": extra[:12]})
        else:
            same += 1
    return {"population": "records passed in", "n": len(records), "identical": same,
            "differ": len(differ), "absent": absent, "examples": differ[:12]}


def dump_csv(path: pathlib.Path, rows: Sequence[dict], cols: Optional[Sequence[str]] = None):
    if cols is None:
        cols = []
        for r in rows:
            for k in r:
                if k not in cols:
                    cols.append(k)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cols))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})
    print(f"    wrote {path.name}: {len(rows)} rows x {len(cols)} cols")
    return path


def sha256_of(path: pathlib.Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()
