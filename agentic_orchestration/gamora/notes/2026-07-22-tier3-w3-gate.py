#!/usr/bin/env python3
"""
Tier-3 W3 — T3-F4 GATE (MECHANICAL EXECUTION of the FROZEN prereg sheet).

WAVE W3 of the Tier-3 Encounter-Geometry Run (conductor: gandalf RUN-CONDUCTOR).
The gate instrument is PRE-REGISTERED + FROZEN (commit 5ea56bf3, doc
agentic_orchestration/gandalf/notes/2026-07-22-tier3-w3-prereg.md). This executable is
ZERO-DISCRETION mechanical execution: every §2/§5/§6 rule is law; a situation the sheet
does not decide is a RED-FLAG (stop that pair, record it, continue), never an improvised rule.

EXECUTION PLAN (the frozen sheet IS the math note — Discipline #1; no re-derivation here):
  STEP 1 SELECTION (deterministic): per era {I,II,III,IV}, candidate pool = v2 fit rows with
    scoring_basis=full ONLY. Draft 4 HIGH (argmax fit_score) + 4 LOW (argmin) under a kit-side
    family round-robin (§5.2-3: no family twice until every family with >=1 candidate in that era
    has appeared once; draft-family = the kit's single ACTIVE sidecar row). Courts check (§5.4:
    >=3 element-courts across the 8 kits; swap per §5.7 tiebreak = smallest
    |fit_score - era-deck-median|, ties by kit_id lexicographic asc).
  STEP 2 FORMATION ASSIGNMENT (§5.4): each pair's encounter = the kit's argmax [high] / argmin [low]
    COMMON-4 formation (swarm / volley-fan / lane / emplacement) from its era deck. Per-formation
    fit sub-scores are NOT materialized in v2, so COMPUTE them with the SAME frozen component logic
    (0.50*verb + 0.30*topo + 0.20*shelf): verb + shelf are CONSTANT per (kit,era); only the topo term
    varies per formation (frozen _affinity on TOPO_AFFINITY[TOPO_CLASS[fid]]). Strain-4 EXCLUDED
    (cbn_corridor_arc, cb_crossfire, ts_environmental_nest, ss_phase_transform per W2).
  STEP 3 FIGHTS: 32 pairs x 4 seeds = 128. Encounter built with the four COMMON-4 builders at HEAD
    (arena.py build_{swarm,volley_fan,lane,emplacement}_formation), MOB-COUNT PARITY 40 TOTAL hard
    (a builder that cannot hold 40 -> red-flag the pair, no silent normalize). Fighter = the kit's
    BC->nearest-endgame-cell->real fighting PlayerClass, BYTE-IDENTICAL to the baseline (reuse the
    baseline mapping + idx-assignment + neutral mob stat-block). dmod=1.0; same 4 seeds.
  STEP 4 GATE (§6): d_m = mean_over_4_seeds(m_enc - kit_baseline_mean_m) / sd_pool(m); composite =
    median of the 3 per-metric d's; LEG1 median composite over 16 high >= +0.5; LEG2 median composite
    over 16 low <= -0.5; LEG3 >=24/32 pairs sign-correct (>=2 of 3 metric d's have predicted sign).
    PASS iff all three, else FAIL (no partial pass).

Substrate: corpus.db md5 d091881d (READ-ONLY). Sidecar commit 6dd43161. Engine harness invoked BY
PATH; ZERO writes to the engine repo. Baselines JSON supplies m-bar + sd_pool. Author: gamora, 2026-07-22.

Run:  python3 2026-07-22-tier3-w3-gate.py
Emits: 2026-07-22-tier3-w3-gate-output.json + prints selection census + gate legs + verdict.
"""
import hashlib
import json
import math
import os
import statistics
import sqlite3
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DB = os.path.abspath(os.path.join(HERE, "..", "..", "research", "curated", "corpus.db"))
SIDECAR = os.path.join(HERE, "..", "..", "elrond", "notes",
                       "2026-07-22-tier3-family-membership-sidecar.json")
V2_FIT = os.path.join(HERE, "2026-07-22-tier3-w2-fit-output-v2.json")
BASELINES = os.path.join(HERE, "2026-07-22-tier3-prereg-baselines.json")
PREREG_DOC = os.path.abspath(os.path.join(HERE, "..", "..", "gandalf", "notes",
                                          "2026-07-22-tier3-w3-prereg.md"))
OUT_PATH = os.path.join(HERE, "2026-07-22-tier3-w3-gate-output.json")

EXPECTED_MD5_PREFIX = "d091881d"
SIDECAR_COMMIT = "6dd43161"
PREREG_FREEZE_COMMIT = "5ea56bf3"
ENGINE_HEAD_BASELINE = "a3671d4"

# ----- FROZEN sheet constants (do NOT re-derive; the prereg IS the math note) -----
SEEDS = [20260722, 20260723, 20260724, 20260725]      # §2 shared seed set (baseline-identical)
DAMAGE_MODIFIER = 1.0                                   # §2 dmod=1.0 uniform
MOB_PARITY_TOTAL = 40                                   # §2 mob-count parity 40 total (hard)
SD_POOL = {"mobs_killed": 12.82, "total_aoe_hits": 12.82, "player_damage_total": 6370.0}  # §2
GATE_X = 0.5                                            # §3 effect-size threshold (standardized)
GATE_Y_MIN_CORRECT = 24                                 # §4/§6 direction: >=24 of 32 (75%)
PRIMARY_METRICS = ["mobs_killed", "total_aoe_hits", "player_damage_total"]  # §5 metric subset
MIN_COURTS = 3                                          # §5.4 courts check
ERAS = ("I", "II", "III", "IV")

# ----- Strain-4 formations EXCLUDED (§5.4 encounter construction; W2 probe verdicts) -----
STRAIN4_EXCLUDED = frozenset({
    "cbn_corridor_arc", "cb_crossfire", "ts_environmental_nest", "ss_phase_transform",
})

# ----- formation_id -> COMMON-4 builder class (authoritative: W2 scenario-set FORMATION_SCENARIO_MAP
#       formation_class column, collapsed to the four builder classes). NOT re-derived — transcribed. -----
FORMATION_TO_COMMON4 = {
    # swarm builder: converging melee mass
    "ms_swarm_surround": "swarm",
    "ww_converge_spin": "swarm",
    "ww_arc_sweep": "swarm",
    "ww_derived_frenzy_line": "swarm",
    "da_field_retreat": "swarm",          # W2: da_field_retreat -> dense_cell (field/close), swarm-class builder
    "ss_derived_form_swap": "swarm",      # SHAPESHIFT derived (non-strain) -> transform texture, class-proxied by swarm converge
    # lane builder: corridor / wedge / directional single-file
    "ms_wedge_advance": "lane",
    "tm_preseed_corridor": "lane",
    "cb_lane_hold": "lane",
    "ds_flank_burst": "lane",             # W2: ds_flank_burst -> elite_pack flank; directional flank -> lane-class
    "ds_derived_gap_close": "lane",
    # volley-fan builder: arc of ranged casters
    "mpv_fan_from_position": "volley-fan",
    "mpv_boss_sweep": "volley-fan",
    "da_curse_at_distance": "volley-fan",  # ranged applied-at-distance -> ranged-hold arc class
    # emplacement builder: held-position emitters
    "ts_anchor_screen": "emplacement",
    "ts_resurrection_loop": "emplacement",
    "aura_carrier_pack": "emplacement",
    "aura_matron_center": "emplacement",
    "tm_ritual_minefield": "emplacement",
    "tm_spawner_nest": "emplacement",
    "cbn_derived_arc_pass": "emplacement",  # CHAIN-BOUNCE derived (non-strain, field) -> emplacement-class field
}

# ---------------------------------------------------------------------------
# Engine harness BY PATH (import/invoke only; ZERO writes to the engine repo).
# ---------------------------------------------------------------------------
ENGINE_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                          "reincarnated-engine", "src"))
if not os.path.isdir(ENGINE_SRC):
    print(f"FATAL: engine src not found at {ENGINE_SRC}", file=sys.stderr)
    sys.exit(2)
sys.path.insert(0, ENGINE_SRC)

from reincarnated.simulation.spatial_gauntlet.arena import (  # noqa: E402
    Arena, ArenaScenario, SpawnSpec,
    build_swarm_formation, build_volley_fan_formation,
    build_lane_formation, build_emplacement_formation,
)
from reincarnated.simulation.spatial_gauntlet.spatial_engine import (  # noqa: E402
    run_spatial_fight, SpatialFightConvergenceError,
)
from reincarnated.generation.typed_monster_skills import (  # noqa: E402
    emit_skills_for_threat_tier,
)
from reincarnated.generation.endgame_encounter_catalog import (  # noqa: E402
    ENDGAME_ENCOUNTER_CATALOG,
)
from reincarnated.simulation.martial_bar_rederivation_driver import (  # noqa: E402
    _build_martial_player_class,
)
from reincarnated.generation.resource_economy import DEFAULT_RESOURCE_ECONOMY  # noqa: E402

# ---------------------------------------------------------------------------
# Frozen fit-component logic — transcribed VERBATIM from
# 2026-07-22-tier3-w2-fit-layer-v2.py (weights + tables + _affinity + formations_for).
# The per-formation topology sub-score reuses these exactly (no re-derivation).
# ---------------------------------------------------------------------------
W_VERB, W_TOPO, W_SHELF = 0.50, 0.30, 0.20

ERA_DECKS = {
    "I": {"era_year": 2000, "signature_family": "MELEE-STRIKE",
          "present_families": ["WHIRLWIND", "AURA", "TOTEM-SENTRY", "TRAP-MINE", "MELEE-STRIKE",
                               "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY", "CHAIN-BOUNCE",
                               "SHAPESHIFT", "DASH-STRIKER"],
          "hole_families": ["CHANNELED-BEAM", "MINION-PET", "IDENTITY-GAUGE"]},
    "II": {"era_year": 2013, "signature_family": "DOT-AILMENT",
           "present_families": ["CHANNELED-BEAM", "AURA", "TOTEM-SENTRY", "TRAP-MINE", "DOT-AILMENT",
                                "MULTI-PROJECTILE-VOLLEY", "CHAIN-BOUNCE", "WHIRLWIND"],
           "hole_families": ["MELEE-STRIKE", "SHAPESHIFT", "MINION-PET", "IDENTITY-GAUGE", "DASH-STRIKER"]},
    "III": {"era_year": 2016, "signature_family": "CHANNELED-BEAM",
            "present_families": ["WHIRLWIND", "CHANNELED-BEAM", "TOTEM-SENTRY", "TRAP-MINE", "MELEE-STRIKE",
                                 "DOT-AILMENT", "CHAIN-BOUNCE", "DASH-STRIKER", "SHAPESHIFT"],
            "hole_families": ["AURA", "MULTI-PROJECTILE-VOLLEY", "MINION-PET", "IDENTITY-GAUGE"]},
    "IV": {"era_year": 2024, "signature_family": None,
           "present_families": ["WHIRLWIND", "CHANNELED-BEAM", "AURA", "TOTEM-SENTRY", "TRAP-MINE",
                                "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY", "MELEE-STRIKE",
                                "SHAPESHIFT", "CHAIN-BOUNCE"],
           "hole_families": ["MINION-PET", "IDENTITY-GAUGE"]},
}

FORMATIONS = {
    "WHIRLWIND": [("ww_converge_spin", ["IV"]), ("ww_arc_sweep", ["I", "III"]),
                  ("ww_derived_frenzy_line", ["II"])],
    "CHANNELED-BEAM": [("cb_lane_hold", ["II", "III", "IV"]), ("cb_crossfire", ["IV"])],
    "AURA": [("aura_carrier_pack", ["I", "II", "IV"]), ("aura_matron_center", ["IV"])],
    "TOTEM-SENTRY": [("ts_anchor_screen", ["I", "II", "III", "IV"]),
                     ("ts_resurrection_loop", ["II", "IV"]), ("ts_environmental_nest", ["II", "IV"])],
    "TRAP-MINE": [("tm_preseed_corridor", ["I", "II"]),
                  ("tm_ritual_minefield", ["II", "III", "IV"]), ("tm_spawner_nest", ["I", "III"])],
    "MELEE-STRIKE": [("ms_swarm_surround", ["I", "III", "IV"]), ("ms_wedge_advance", ["I", "III"])],
    "DOT-AILMENT": [("da_field_retreat", ["I", "II", "III", "IV"]), ("da_curse_at_distance", ["I", "III"])],
    "MULTI-PROJECTILE-VOLLEY": [("mpv_fan_from_position", ["I", "II", "IV"]), ("mpv_boss_sweep", ["IV"])],
    "CHAIN-BOUNCE": [("cbn_corridor_arc", ["I", "II", "III"]), ("cbn_derived_arc_pass", ["IV"])],
    "SHAPESHIFT": [("ss_phase_transform", ["IV"]), ("ss_derived_form_swap", ["I", "III"])],
    "DASH-STRIKER": [("ds_flank_burst", ["III"]), ("ds_derived_gap_close", ["I"])],
}

FAMILY_VERB = {
    "WHIRLWIND": "spin-and-close", "CHANNELED-BEAM": "channel-lanes", "AURA": "aura-enable",
    "TOTEM-SENTRY": "emplace-and-hold", "TRAP-MINE": "pre-seed", "MELEE-STRIKE": "swarm-the-brawl",
    "DOT-AILMENT": "stack-and-retreat", "MULTI-PROJECTILE-VOLLEY": "fan",
    "CHAIN-BOUNCE": "bounce-and-chain", "SHAPESHIFT": "form-transition",
    "DASH-STRIKER": "dash-and-strike", "MINION-PET": "minion-swarm", "IDENTITY-GAUGE": "gauge-threshold",
}

VERB_AFFINITY = {
    "stack-and-retreat": {"favor": [("range_val", "ranged"), ("range_val", "dual"), ("commit_val", "instant")],
                          "penalize": [("range_val", "melee"), ("commit_val", "channel")]},
    "swarm-the-brawl": {"favor": [("proxy_val", "heavy"), ("proxy_val", "light"), ("amp_val", "var")],
                        "penalize": [("proxy_val", "solo")]},
    "channel-lanes": {"favor": [("range_val", "melee"), ("range_val", "mid"), ("commit_val", "instant")],
                      "penalize": [("commit_val", "channel")]},
    "fan": {"favor": [("range_val", "ranged"), ("proxy_val", "heavy")], "penalize": [("range_val", "melee")]},
    "spin-and-close": {"favor": [("range_val", "ranged"), ("range_val", "dual"), ("tempo_val", "high")],
                       "penalize": [("range_val", "melee"), ("tempo_val", "low")]},
    "emplace-and-hold": {"favor": [("amp_val", "spiky"), ("range_val", "ranged")], "penalize": [("tempo_val", "low")]},
    "pre-seed": {"favor": [("tempo_val", "high"), ("proxy_val", "heavy")], "penalize": [("commit_val", "channel")]},
    "form-transition": {"favor": [], "penalize": []},
    "bounce-and-chain": {"favor": [("proxy_val", "solo"), ("range_val", "ranged")], "penalize": [("proxy_val", "heavy")]},
    "aura-enable": {"favor": [("amp_val", "spiky")], "penalize": [("amp_val", "flat")]},
    "dash-and-strike": {"favor": [("range_val", "melee"), ("tempo_val", "high")], "penalize": [("range_val", "ranged")]},
    "minion-swarm": {"favor": [], "penalize": []},
    "gauge-threshold": {"favor": [], "penalize": []},
}

TOPO_CLASS = {
    "cbn_corridor_arc": "corridor", "cb_lane_hold": "corridor", "cb_crossfire": "corridor",
    "tm_preseed_corridor": "corridor",
    "ww_converge_spin": "converge", "ww_arc_sweep": "converge", "ww_derived_frenzy_line": "converge",
    "ms_swarm_surround": "converge", "ms_wedge_advance": "converge",
    "ts_anchor_screen": "anchor", "ts_resurrection_loop": "anchor", "aura_matron_center": "anchor",
    "aura_carrier_pack": "anchor", "mpv_fan_from_position": "anchor", "mpv_boss_sweep": "anchor",
    "da_field_retreat": "field", "da_curse_at_distance": "field", "tm_ritual_minefield": "field",
    "tm_spawner_nest": "field", "ts_environmental_nest": "field", "cbn_derived_arc_pass": "field",
    "ss_phase_transform": "transform", "ss_derived_form_swap": "transform",
    "ds_flank_burst": "flank", "ds_derived_gap_close": "flank",
}
TOPO_AFFINITY = {
    "corridor": {"favor": [("range_val", "ranged")], "penalize": [("range_val", "melee")]},
    "converge": {"favor": [("amp_val", "var"), ("proxy_val", "heavy")], "penalize": [("range_val", "ranged")]},
    "anchor": {"favor": [("range_val", "ranged"), ("amp_val", "spiky")], "penalize": [("range_val", "melee")]},
    "field": {"favor": [("tempo_val", "high"), ("range_val", "ranged")], "penalize": [("commit_val", "channel")]},
    "transform": {"favor": [], "penalize": []},
    "flank": {"favor": [("range_val", "melee"), ("tempo_val", "high")], "penalize": [("range_val", "ranged")]},
}
ERA_OF_YEAR = {2000: "I", 2013: "II", 2016: "III", 2024: "IV"}


def _affinity(kit, table_entry):
    """VERBATIM from v2 fit script."""
    fav = table_entry.get("favor", [])
    pen = table_entry.get("penalize", [])
    if not fav and not pen:
        return 0.5, "neutral"
    hit_fav = any(kit.get(ax) == val for (ax, val) in fav)
    hit_pen = any(kit.get(ax) == val for (ax, val) in pen)
    if hit_fav and not hit_pen:
        return 1.0, "favor"
    if hit_pen and not hit_fav:
        return 0.0, "penalize"
    return 0.5, "neutral"


def formations_for(family, era):
    """Formation_ids a family deals in an era (VERBATIM logic from v2 fit script)."""
    return [fid for (fid, eras) in FORMATIONS.get(family, []) if era in eras]


# ---------------------------------------------------------------------------
# Baseline fighter-mapping code — reused BYTE-IDENTICAL from
# 2026-07-22-tier3-prereg-baselines.py so each kit's fighter is identical to its baseline.
# ---------------------------------------------------------------------------
def _nrange(x):
    return {"melee": "melee", "dual": "mid", "ranged": "ranged"}.get(x, "mid")
def _ntempo(x):
    return {"high": "high", "med": "medium", "low": "low"}.get(x, "medium")
def _namp(x):
    return {"flat": "flat", "spiky": "spiky", "var": "variable"}.get(x, "flat")
def _nattr(x):
    return (x or "STR").upper()


def _neutral_cells():
    out = []
    for e in ENDGAME_ENCOUNTER_CATALOG:
        if e.bc_proxy_density == "none" and not e.encounter_id.endswith(("_escape", "_dense")):
            out.append((e.encounter_id, e.bc_range, e.bc_tempo, e.bc_amplitude, e.bc_attribute))
    return out


def nearest_cell(k, cells):
    tr, tt, ta, tat = _nrange(k["range_val"]), _ntempo(k["tempo_val"]), _namp(k["amp_val"]), _nattr(k["attr_val"])
    best, bestd = None, 99
    for (cid, cr, ct, ca, cat_attr) in cells:
        d = (cr != tr) * 2 + (cat_attr != tat) * 2 + (ct != tt) + (ca != ta)
        if d < bestd:
            bestd, best = d, cid
    return best, bestd


def build_neutral_mob_dicts(spawn_tiers):
    """Neutral roster stat-block per baseline build_neutral_mobs, keyed on each spawn's tier. Held
    byte-identical across ALL encounters (neutrality). Formation shapes GEOMETRY; the per-tier HP
    block (swarm 150 / elite 2500) is the same stat-block the baseline used."""
    out = []
    for tier in spawn_tiers:
        if tier in ("boss", "mini-boss", "miniboss", "elite"):
            skills = emit_skills_for_threat_tier(tier, signature_element="fire")
            hp = 2500.0
        else:
            skills = emit_skills_for_threat_tier(tier)
            hp = 150.0
        out.append({"id": f"mob_{len(out)}", "max_hp": hp, "energy": 100.0, "max_energy": 100.0,
                    "armor": 20.0, "skills": skills, "movement_speed": 5.5,
                    "preferred_behavior": "melee_aggressive", "aggro_radius_m": 15.0,
                    "leash_distance_m": 18.0})
    return out


def md5_check(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Formation scenario builders — 44x44 neutral arena, player north-center facing south, 40 spawns.
# scenario_id is NEW (not open_arena/chokepoint_corridor) so the engine's MOB_HP_DIFFICULTY x1.5 gate
# (arena.py MOB_HP_DIFFICULTY_SCENARIOS) does NOT implicitly fire — mob HP stays the neutral stat-block
# (geometry is the manipulated variable, not HP tuning; §2 "formation shapes geometry, not budget").
# ---------------------------------------------------------------------------
_ARENA_W = _ARENA_H = 44.0
_PLAYER_SPAWN = SpawnSpec(x=22.0, y=38.0, heading_rad=-math.pi / 2, entity_radius=0.5,
                          threat_tier="player", archetype_tag="player")


def _formation_spawns(fclass):
    """Return the 40-spawn layout for a COMMON-4 class (params chosen to hit exactly 40, in-bounds)."""
    if fclass == "swarm":
        return build_swarm_formation(center=(22.0, 16.0), n_packs=10, pack_size=4, pack_spread_m=13.0)
    if fclass == "volley-fan":
        return build_volley_fan_formation(center=(22.0, 20.0), count=40, radius_m=15.0,
                                          arc_span_rad=math.pi, arc_center_rad=-math.pi / 2)
    if fclass == "lane":
        return build_lane_formation(x_center=22.0, y_start=6.0, length_m=26.0, count=40,
                                    rows_per_band=4, lane_width_m=8.0)
    if fclass == "emplacement":
        return build_emplacement_formation(origin=(8.0, 8.0), cols=8, rows=5, spacing_m=3.8)
    raise ValueError(f"unknown COMMON-4 class {fclass!r}")


def make_formation_scenario(fclass):
    """(scenario, red_flag_or_None). Enforces MOB-COUNT PARITY 40 (§2): a builder whose 40-spawn
    layout is not exactly 40 or lands out of bounds -> red-flag (do NOT normalize silently)."""
    spawns = _formation_spawns(fclass)
    if len(spawns) != MOB_PARITY_TOTAL:
        return None, f"builder {fclass} produced {len(spawns)} spawns != {MOB_PARITY_TOTAL} (parity)"
    oob = [(sp.x, sp.y) for sp in spawns
           if not (0.5 <= sp.x <= _ARENA_W - 0.5 and 0.5 <= sp.y <= _ARENA_H - 0.5)]
    if oob:
        return None, f"builder {fclass} has {len(oob)} out-of-bounds spawns (e.g. {oob[0]})"
    arena = Arena(width_m=_ARENA_W, height_m=_ARENA_H, choke_zones=[], name=f"t3w3_{fclass}_44x44")
    scen = ArenaScenario(
        scenario_id=f"t3w3_{fclass}", description=f"T3-W3 neutral-arena {fclass} formation (40-parity)",
        arena=arena, player_spawn=_PLAYER_SPAWN, mob_spawns=spawns,
        max_duration_s=120.0, win_condition="all_mobs_killed", boss_index=None)
    return scen, None


# ---------------------------------------------------------------------------
# STEP 1 — SELECTION (deterministic family round-robin + courts check).
# ---------------------------------------------------------------------------
def load_full_fit_rows():
    """v2 fit rows with scoring_basis=full, enriched with each kit's corpus BC + court + sidecar family."""
    v2 = json.load(open(V2_FIT))
    fit = [r for r in v2["fit_records"] if r["scoring_basis"] == "full"]
    # sidecar ACTIVE on_spine family (draft-family authority, §5.6)
    sc = json.load(open(SIDECAR))
    active = {r["kit_id"]: r["family"] for r in sc["memberships"]
              if not r.get("shadowed_by") and r.get("on_spine")}
    # corpus BC + court
    con = sqlite3.connect(f"file:{CORPUS_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    bc = {}
    for row in con.execute(
            "SELECT kit_id, court, original_element, attr_val, range_val, tempo_val, amp_val, "
            "proxy_val, commit_val FROM canon_corpus WHERE corpus_class='record'"):
        bc[row["kit_id"]] = dict(row)
    con.close()
    out = []
    for r in fit:
        kid = r["kit_id"]
        b = bc.get(kid, {})
        out.append({
            "kit_id": kid, "era": r["era"], "family": r["family"],
            "draft_family": active.get(kid),   # §5.6 single ACTIVE sidecar row
            "membership_tier": r["membership_tier"], "fit_score": r["fit_score"],
            "court": b.get("court"), "element": b.get("original_element"),
            "range_val": b.get("range_val"), "tempo_val": b.get("tempo_val"),
            "amp_val": b.get("amp_val"), "proxy_val": b.get("proxy_val"),
            "commit_val": b.get("commit_val"), "attr_val": b.get("attr_val"),
            "verb_affinity": r["verb_affinity"], "shelf_affinity": r["shelf_affinity"],
        })
    return out


def round_robin_draft(candidates, side):
    """§5.2-3 kit-side family round-robin. side='high' -> descending fit_score; 'low' -> ascending.
    No family (draft_family) contributes a 2nd kit until every family with >=1 candidate in the pool
    has contributed one. Deterministic tiebreak on equal fit_score: kit_id lexicographic ascending."""
    reverse = (side == "high")
    ordered = sorted(candidates, key=lambda c: (c["fit_score"], c["kit_id"]), reverse=reverse)
    # stable secondary: when reverse, kit_id should still be ascending on ties -> re-sort ties.
    ordered = sorted(candidates, key=lambda c: c["kit_id"])                       # kit_id asc primary tie
    ordered = sorted(ordered, key=lambda c: c["fit_score"], reverse=reverse)      # fit primary
    families_with_candidate = set(c["draft_family"] for c in candidates)
    picked = []
    used_families = set()
    # round-robin: iterate; skip a family already used until all families used once, then allow repeats
    remaining = list(ordered)
    while len(picked) < 4 and remaining:
        progressed = False
        for c in list(remaining):
            fam = c["draft_family"]
            all_used_once = used_families >= families_with_candidate
            if fam in used_families and not all_used_once:
                continue
            picked.append(c)
            remaining.remove(c)
            used_families.add(fam)
            progressed = True
            if len(picked) == 4:
                break
        if not progressed:
            # every remaining kit's family already used but not all families used once
            # (families_with_candidate includes families that ran out of kits) -> allow repeats now
            for c in list(remaining):
                picked.append(c)
                remaining.remove(c)
                if len(picked) == 4:
                    break
            break
    return picked[:4]


def courts_swap(picked_high, picked_low, candidates_high, candidates_low, deck_median):
    """§5.4 courts check across the 8 drafted kits (>=3 element-courts). If violated, swap the
    least-extreme pick (smallest |fit_score - deck_median|) for the next-best candidate from a
    MISSING court (§5.7 tiebreak; ties -> kit_id lexicographic asc). Returns (high, low, swap_log)."""
    swap_log = []
    all8 = picked_high + picked_low
    courts = set(c["court"] for c in all8)
    if len(courts) >= MIN_COURTS:
        return picked_high, picked_low, swap_log
    # need a swap: find the least-extreme pick across all 8
    while len(set(c["court"] for c in (picked_high + picked_low))) < MIN_COURTS:
        all8 = picked_high + picked_low
        present_courts = set(c["court"] for c in all8)
        # candidate replacement kits from missing courts, not already drafted
        drafted_ids = set(c["kit_id"] for c in all8)
        pool = [c for c in (candidates_high + candidates_low)
                if c["court"] not in present_courts and c["kit_id"] not in drafted_ids]
        if not pool:
            swap_log.append({"result": "NO_MISSING_COURT_CANDIDATE",
                             "present_courts": sorted(present_courts)})
            break
        # least-extreme pick to remove (smallest |fit - deck_median|, tie kit_id asc)
        least = min(all8, key=lambda c: (abs(c["fit_score"] - deck_median), c["kit_id"]))
        # best replacement from a missing court: prefer the pick's SIDE extremity, tie kit_id asc.
        # "next-best candidate from a missing court" -> for a high pick removed, pick max fit; for a
        # low pick removed, min fit; determine which side `least` is on.
        on_high = any(c["kit_id"] == least["kit_id"] for c in picked_high)
        repl = (max(pool, key=lambda c: (c["fit_score"], [-ord(ch) for ch in c["kit_id"]]))
                if on_high else
                min(pool, key=lambda c: (c["fit_score"], c["kit_id"])))
        # apply swap
        if on_high:
            picked_high = [repl if c["kit_id"] == least["kit_id"] else c for c in picked_high]
        else:
            picked_low = [repl if c["kit_id"] == least["kit_id"] else c for c in picked_low]
        swap_log.append({
            "removed": {"kit_id": least["kit_id"], "court": least["court"], "fit_score": least["fit_score"],
                        "abs_dist_to_deck_median": round(abs(least["fit_score"] - deck_median), 4),
                        "side": "high" if on_high else "low"},
            "added": {"kit_id": repl["kit_id"], "court": repl["court"], "fit_score": repl["fit_score"]},
            "deck_median": round(deck_median, 4),
            "tiebreak": "smallest |fit - deck_median|, ties kit_id asc (§5.7)",
        })
    return picked_high, picked_low, swap_log


# ---------------------------------------------------------------------------
# STEP 2 — FORMATION ASSIGNMENT (per-formation fit sub-score with frozen component logic).
# ---------------------------------------------------------------------------
def per_formation_subscores(kit_row):
    """For a drafted (kit, era) row, compute per-COMMON-4-formation fit sub-scores using the FROZEN
    component logic. verb + shelf are CONSTANT per (kit,era) (from the v2 row); only the topo term
    varies per formation. Strain-4 formations EXCLUDED. Returns [{formation_id, common4_class,
    topo_class, topo_affinity, fit_subscore}...] over the family's era formations."""
    family = kit_row["family"]
    era = kit_row["era"]
    verb_aff = kit_row["verb_affinity"]      # constant per (kit,era) — reuse the v2 value
    shelf_aff = kit_row["shelf_affinity"]    # constant per (kit,era)
    subs = []
    for fid in formations_for(family, era):
        if fid in STRAIN4_EXCLUDED:
            continue
        common4 = FORMATION_TO_COMMON4.get(fid)
        if common4 is None:
            # sheet does not decide how to map this formation to a COMMON-4 builder -> red-flag upstream
            subs.append({"formation_id": fid, "common4_class": None, "topo_class": TOPO_CLASS.get(fid),
                         "topo_affinity": None, "fit_subscore": None,
                         "red_flag": f"formation_id {fid} has no COMMON-4 mapping"})
            continue
        tclass = TOPO_CLASS.get(fid, "transform")
        topo_aff, _ = _affinity(kit_row, TOPO_AFFINITY.get(tclass, {}))
        sub = round(W_VERB * verb_aff + W_TOPO * topo_aff + W_SHELF * shelf_aff, 4)
        subs.append({"formation_id": fid, "common4_class": common4, "topo_class": tclass,
                     "topo_affinity": round(topo_aff, 4), "fit_subscore": sub})
    return subs


def assign_formation(kit_row, side):
    """§5.4: encounter = the kit's argmax [high] / argmin [low] COMMON-4 formation from its era deck.
    Returns (chosen_dict, subscores, red_flag_or_None)."""
    subs = [s for s in per_formation_subscores(kit_row) if s.get("fit_subscore") is not None]
    if not subs:
        return None, per_formation_subscores(kit_row), \
            f"no COMMON-4 formation available for {kit_row['family']}/{kit_row['era']} (all strain/unmapped)"
    if side == "high":
        chosen = max(subs, key=lambda s: (s["fit_subscore"], s["formation_id"]))
    else:
        chosen = min(subs, key=lambda s: (s["fit_subscore"], s["formation_id"]))
    return chosen, subs, None


# ---------------------------------------------------------------------------
# STEP 3 — FIGHTS + STEP 4 — GATE.
# ---------------------------------------------------------------------------
def median3(vals):
    return statistics.median(vals)


def main():
    t_open = time.perf_counter()
    md5 = md5_check(CORPUS_DB)
    if not md5.startswith(EXPECTED_MD5_PREFIX):
        print(f"FATAL: corpus md5 {md5} != {EXPECTED_MD5_PREFIX}", file=sys.stderr)
        sys.exit(2)

    baselines = json.load(open(BASELINES))
    kit_baseline_mean = {}  # kit_id -> {metric: mean}
    for pk in baselines["per_kit_baselines"]:
        kit_baseline_mean[pk["kit_id"]] = {
            m: pk["within_kit_variance"][m]["mean"] for m in PRIMARY_METRICS}

    full_rows = load_full_fit_rows()

    # ---- STEP 1: per-era selection ----
    selection = {}
    for era in ERAS:
        cands = [r for r in full_rows if r["era"] == era]
        deck_median = statistics.median([c["fit_score"] for c in cands])
        high = round_robin_draft(cands, "high")
        low = round_robin_draft(cands, "low")
        high, low, swap_log = courts_swap(high, low, cands, cands, deck_median)
        selection[era] = {"high": high, "low": low, "swap_log": swap_log,
                          "deck_median_fit": round(deck_median, 4),
                          "n_candidates": len(cands)}

    # ---- STEP 2: formation assignment per pair ----
    pairs = []  # each: era, side, kit_row, formation dict, subscores, red_flag
    for era in ERAS:
        for side in ("high", "low"):
            for kit_row in selection[era][side]:
                chosen, subs, rf = assign_formation(kit_row, side)
                pairs.append({"era": era, "side": side, "kit_row": kit_row,
                              "formation": chosen, "formation_subscores": subs, "red_flag": rf})

    # ---- Discipline #11 smoke: 2-pair non-passive check BEFORE the full 128 ----
    cells = _neutral_cells()
    # cache one PlayerClass per used cell, idx = position in sorted(all used cells over the WHOLE
    # resolved spine) to be byte-identical to the baseline's assignment.
    con = sqlite3.connect(f"file:{CORPUS_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    all_kits = []
    sc = json.load(open(SIDECAR))
    active_ids = {r["kit_id"] for r in sc["memberships"]
                  if not r.get("shadowed_by") and r.get("on_spine")}
    for row in con.execute("SELECT kit_id, attr_val, range_val, tempo_val, amp_val "
                           "FROM canon_corpus WHERE corpus_class='record' ORDER BY kit_id"):
        if row["kit_id"] in active_ids:
            all_kits.append(dict(row))
    con.close()
    cell_of = {k["kit_id"]: nearest_cell(k, cells)[0] for k in all_kits}
    dist_of = {k["kit_id"]: nearest_cell(k, cells)[1] for k in all_kits}
    all_used_cells = sorted(set(cell_of.values()))
    pc_cache = {}
    t_build = time.perf_counter()
    for idx, cid in enumerate(all_used_cells):
        pc, _ = _build_martial_player_class(cid, idx, "balanced")
        cd = pc.model_dump()
        cd["resource_economy"] = dict(DEFAULT_RESOURCE_ECONOMY)
        pc_cache[cid] = (pc, cd)
    build_s = time.perf_counter() - t_build

    # pre-build the 4 formation scenarios once (deterministic); record any parity red-flags
    formation_scenarios = {}
    formation_red_flags = {}
    for fclass in ("swarm", "volley-fan", "lane", "emplacement"):
        scen, rf = make_formation_scenario(fclass)
        formation_scenarios[fclass] = scen
        if rf:
            formation_red_flags[fclass] = rf

    # smoke: first 2 non-red-flagged pairs
    smoke_targets = [p for p in pairs if p["red_flag"] is None and p["formation"] is not None][:2]
    smoke_results = []
    for p in smoke_targets:
        kid = p["kit_row"]["kit_id"]
        cid = cell_of.get(kid)
        pc, cd = pc_cache[cid]
        fclass = p["formation"]["common4_class"]
        scen = formation_scenarios[fclass]
        tiers = [sp.threat_tier for sp in scen.mob_spawns]
        mobs = build_neutral_mob_dicts(tiers)
        raw = run_spatial_fight(scenario=scen, class_dict=cd, mob_dicts=mobs, n_fights=1,
                                session_id=f"w3_smoke_{kid}", base_seed=SEEDS[0],
                                season_id="tier3-w3-smoke", player_class=pc,
                                damage_modifier=DAMAGE_MODIFIER, track_proxy_population=False)
        fr = raw["fight_results"][0]
        mk = int(getattr(fr, "mobs_killed", 0) or 0)
        pd_ = float(getattr(fr, "player_damage_total", 0.0) or 0.0)
        smoke_results.append({"kit_id": kid, "cell": cid, "formation_class": fclass,
                              "mobs_killed": mk, "player_damage_total": pd_,
                              "passive": (mk == 0 and pd_ == 0.0)})
    if any(s["passive"] for s in smoke_results):
        print("SMOKE FAIL: passive player detected on a formation scenario — STOP (do not patch generation).",
              file=sys.stderr)
        print(json.dumps(smoke_results, indent=2), file=sys.stderr)
        # write a HALT stub and exit; conductor decides.
        json.dump({"verdict": "HALT", "reason": "passive_player_smoke_fail",
                   "smoke_results": smoke_results}, open(OUT_PATH, "w"), indent=2)
        sys.exit(3)

    # ---- STEP 3: the full 128 fights ----
    t0 = time.perf_counter()
    fight_records = []
    for p in pairs:
        era, side = p["era"], p["side"]
        kit_row = p["kit_row"]
        kid = kit_row["kit_id"]
        # red-flag pairs: record, do not fight (§ pin-not-decided handling)
        if p["red_flag"] is not None or p["formation"] is None:
            fight_records.append({"era": era, "side": side, "kit_id": kid,
                                  "red_flag": p["red_flag"], "fights": [], "skipped": True})
            continue
        fclass = p["formation"]["common4_class"]
        if fclass in formation_red_flags:
            fight_records.append({"era": era, "side": side, "kit_id": kid,
                                  "red_flag": formation_red_flags[fclass], "fights": [], "skipped": True})
            continue
        cid = cell_of.get(kid)
        pc, cd = pc_cache[cid]
        scen = formation_scenarios[fclass]
        tiers = [sp.threat_tier for sp in scen.mob_spawns]
        mobs = build_neutral_mob_dicts(tiers)
        per_seed = []
        for seed in SEEDS:
            try:
                raw = run_spatial_fight(scenario=scen, class_dict=cd, mob_dicts=mobs, n_fights=1,
                                        session_id=f"w3_{kid}_{side}", base_seed=seed,
                                        season_id="tier3-w3", player_class=pc,
                                        damage_modifier=DAMAGE_MODIFIER, track_proxy_population=False)
                fr = raw["fight_results"][0]
                row = {"seed": seed}
                for m in PRIMARY_METRICS + ["elapsed_s", "max_flanking_count", "total_flanking_ticks",
                                            "winner", "total_mob_count"]:
                    v = getattr(fr, m, None)
                    row[m] = v if isinstance(v, str) else (float(v) if v is not None else None)
                per_seed.append(row)
            except SpatialFightConvergenceError as e:
                per_seed.append({"seed": seed, "error": "convergence", "detail": str(e)[:120]})
            except Exception as e:  # noqa: BLE001
                per_seed.append({"seed": seed, "error": type(e).__name__, "detail": str(e)[:120]})
        fight_records.append({
            "era": era, "side": side, "kit_id": kid, "family": kit_row["family"],
            "draft_family": kit_row["draft_family"], "membership_tier": kit_row["membership_tier"],
            "court": kit_row["court"], "fit_score": kit_row["fit_score"],
            "formation_id": p["formation"]["formation_id"], "formation_class": fclass,
            "formation_fit_subscore": p["formation"]["fit_subscore"],
            "assigned_cell": cid, "cell_distance": dist_of.get(kid),
            "fights": per_seed, "skipped": False,
        })
    wall = time.perf_counter() - t0

    # ---- STEP 4: gate computation ----
    per_pair = []
    for fr in fight_records:
        if fr.get("skipped"):
            per_pair.append({"era": fr["era"], "side": fr["side"], "kit_id": fr["kit_id"],
                             "red_flag": fr.get("red_flag"), "skipped": True})
            continue
        kid = fr["kit_id"]
        base = kit_baseline_mean.get(kid, {})
        oks = [f for f in fr["fights"] if "error" not in f]
        d_m = {}
        sign_correct_metrics = 0
        predicted_sign = +1 if fr["side"] == "high" else -1
        for m in PRIMARY_METRICS:
            deltas = [f[m] - base[m] for f in oks if f.get(m) is not None and base.get(m) is not None]
            if not deltas:
                d_m[m] = None
                continue
            mean_delta = sum(deltas) / len(deltas)
            d = mean_delta / SD_POOL[m]
            d_m[m] = round(d, 4)
            if (predicted_sign > 0 and d > 0) or (predicted_sign < 0 and d < 0):
                sign_correct_metrics += 1
        dvals = [d_m[m] for m in PRIMARY_METRICS if d_m[m] is not None]
        composite = round(median3(dvals), 4) if dvals else None
        pair_sign_correct = (sign_correct_metrics >= 2)  # §4: >=2 of 3 metrics predicted sign
        per_pair.append({
            "era": fr["era"], "side": fr["side"], "kit_id": kid, "family": fr["family"],
            "membership_tier": fr["membership_tier"], "court": fr["court"], "fit_score": fr["fit_score"],
            "formation_id": fr["formation_id"], "formation_class": fr["formation_class"],
            "n_ok_seeds": len(oks), "d_per_metric": d_m, "composite_d": composite,
            "predicted_sign": "+" if predicted_sign > 0 else "-",
            "n_metrics_sign_correct": sign_correct_metrics, "pair_sign_correct": pair_sign_correct,
            "skipped": False,
        })

    scored = [p for p in per_pair if not p.get("skipped") and p.get("composite_d") is not None]
    high_pairs = [p for p in scored if p["side"] == "high"]
    low_pairs = [p for p in scored if p["side"] == "low"]
    leg1_median = round(median3([p["composite_d"] for p in high_pairs]), 4) if high_pairs else None
    leg2_median = round(median3([p["composite_d"] for p in low_pairs]), 4) if low_pairs else None
    n_sign_correct = sum(1 for p in scored if p["pair_sign_correct"])
    leg3_n = n_sign_correct
    leg3_total = len(scored)

    leg1_pass = (leg1_median is not None and leg1_median >= GATE_X)
    leg2_pass = (leg2_median is not None and leg2_median <= -GATE_X)
    leg3_pass = (leg3_n >= GATE_Y_MIN_CORRECT)
    verdict = "PASS" if (leg1_pass and leg2_pass and leg3_pass) else "FAIL"

    red_flag_pairs = [p for p in per_pair if p.get("red_flag")]
    if red_flag_pairs and verdict == "PASS":
        # a red-flagged pair means the sampled 32 is incomplete; report but do not silently pass.
        verdict = "FAIL"  # incomplete sample cannot certify a PASS (no partial pass, §6)

    # ---- WAVE-level red-flags: situations the FROZEN sheet did not decide (recorded, not improvised) ----
    # (A) hole-cell formation-assignment gap: §5 selection legitimately drafts hole-cell kits as argmin
    #     (they ARE the lowest fit, family_present=hole, fit=0.15), but §5.4 encounter-construction gives
    #     NO COMMON-4 formation for a hole cell (the family deals no formation in that era's deck). The
    #     sheet does not pin a formation for hole cells -> per-pair red-flag (STOP the pair, do not improvise).
    # (B) HP-budget composition confound: §2 pins mob-count parity "40 total" ("formation shapes geometry,
    #     NOT budget") but does NOT pin the encounter's per-mob HP / elite-swarm split. The baseline is
    #     open_arena = 40 mobs (3 elite + 37 swarm) WITH the engine's 1.5x MOB_HP_DIFFICULTY (elite eff
    #     3750, swarm eff 225 -> total destructible HP pool ~19,575). The COMMON-4 formations are
    #     HOMOGENEOUS (all swarm-tier, or all magic-tier) at the neutral per-tier stat-block; with a fresh
    #     scenario_id the 1.5x does not fire (geometry, not tuning). Net: encounter total destructible HP
    #     (e.g. swarm 40x150=6,000) != baseline pool (~19,575), so mobs_killed SATURATES at the 40 ceiling
    #     and player_damage_total PINS at the formation's total-HP for a full clear -> both are dominated by
    #     the HP-budget mismatch, not by formation geometry. The confound is INHERENT to the frozen
    #     instrument (elite-heavy open_arena baseline vs homogeneous-formation encounter, both "40 total") —
    #     matching per-mob HP would NOT dissolve it (the elite/swarm split is unpinned by "40 total"). This
    #     limits 2 of the 3 gate metrics; total_aoe_hits is likewise ceiling-coupled to mobs_killed here.
    #     Recorded for the conductor; NOT silently rescaled (rescaling is an un-pinned rule that would move
    #     the verdict — forbidden by zero-discretion mechanical execution).
    ceiling_saturated_pairs = sum(
        1 for f in fight_records if not f.get("skipped")
        for s in f["fights"] if "error" not in s and (s.get("mobs_killed") == 40.0))
    wave_red_flags = [
        {"id": "RF-A-hole-cell-formation-gap",
         "class": "per-pair (4 pairs); sheet-undecided",
         "finding": ("§5 round-robin drafts hole-cell families as low-side argmin (family_present=hole, "
                     "fit=0.15, meso=[]); §5.4 gives no COMMON-4 formation for a hole cell -> the encounter "
                     "is undefined. STOPPED those 4 pairs, recorded, did not improvise a formation."),
         "affected_pairs": [{"era": p["era"], "kit_id": p["kit_id"], "reason": p["red_flag"]}
                            for p in red_flag_pairs]},
        {"id": "RF-B-hp-budget-composition-confound",
         "class": "wave-level measurement artifact; sheet-undecided (§2 pins count=40, not HP/composition)",
         "finding": ("baseline open_arena = 40 mobs (3 elite + 37 swarm) at 1.5x MOB_HP_DIFFICULTY (total "
                     "destructible HP ~19,575) vs homogeneous COMMON-4 formations at the neutral per-tier "
                     "stat-block, fresh scenario_id (no 1.5x). Total-destructible-HP mismatch makes "
                     "mobs_killed saturate at the 40 ceiling and player_damage_total pin at the formation "
                     "total-HP for a full clear -> 2 of 3 gate metrics are HP-budget-dominated, not "
                     "geometry-dominated. Inherent to the frozen instrument; not rescaled (un-pinned rule)."),
         "evidence": {"baseline_open_arena_roster": "3 elite + 37 swarm, 1.5x HP (~19,575 total HP)",
                      "encounter_swarm_total_hp": "40 x 150 = 6,000",
                      "encounter_fights_at_mobs_killed_ceiling_40": ceiling_saturated_pairs,
                      "example_low_positive_d": "poe1-frost-blades low/volley-fan: baseline mk=22 -> "
                                                "encounter mk=40 (ceiling) -> d=+1.40 (HP-budget, not fit)"}},
    ]

    # ---- decompositions ----
    per_era_legs = {}
    for era in ERAS:
        eh = [p for p in high_pairs if p["era"] == era]
        el = [p for p in low_pairs if p["era"] == era]
        per_era_legs[era] = {
            "high_median_composite_d": round(median3([p["composite_d"] for p in eh]), 4) if eh else None,
            "low_median_composite_d": round(median3([p["composite_d"] for p in el]), 4) if el else None,
            "n_sign_correct": sum(1 for p in scored if p["era"] == era and p["pair_sign_correct"]),
            "n_pairs": sum(1 for p in scored if p["era"] == era),
        }
    per_family_mean_d = {}
    fam_bucket = defaultdict(list)
    for p in scored:
        fam_bucket[p["family"]].append(p["composite_d"])
    for fam, ds in fam_bucket.items():
        per_family_mean_d[fam] = round(sum(ds) / len(ds), 4)
    per_metric_medians = {}
    for m in PRIMARY_METRICS:
        hv = [p["d_per_metric"][m] for p in high_pairs if p["d_per_metric"].get(m) is not None]
        lv = [p["d_per_metric"][m] for p in low_pairs if p["d_per_metric"].get(m) is not None]
        per_metric_medians[m] = {
            "high_median_d": round(median3(hv), 4) if hv else None,
            "low_median_d": round(median3(lv), 4) if lv else None}
    tier_mix = Counter(p["membership_tier"] for p in scored)

    # ---- selection census (families + courts per era; swaps) ----
    selection_census = {}
    for era in ERAS:
        h = selection[era]["high"]
        lo = selection[era]["low"]
        all8 = h + lo
        selection_census[era] = {
            "deck_median_fit": selection[era]["deck_median_fit"],
            "n_candidates": selection[era]["n_candidates"],
            "high": [{"kit_id": c["kit_id"], "draft_family": c["draft_family"],
                      "membership_tier": c["membership_tier"], "fit_score": c["fit_score"],
                      "court": c["court"]} for c in h],
            "low": [{"kit_id": c["kit_id"], "draft_family": c["draft_family"],
                     "membership_tier": c["membership_tier"], "fit_score": c["fit_score"],
                     "court": c["court"]} for c in lo],
            "families_drafted": sorted(set(c["draft_family"] for c in all8)),
            "courts_drafted": sorted(set(c["court"] for c in all8)),
            "n_courts": len(set(c["court"] for c in all8)),
            "courts_check_ok": len(set(c["court"] for c in all8)) >= MIN_COURTS,
            "swap_log": selection[era]["swap_log"],
        }

    engine_head_close = os.popen(
        "git -C ~/Games/reincarnated-engine rev-parse HEAD 2>/dev/null").read().strip()
    subtree_delta = os.popen(
        "git -C ~/Games/reincarnated-engine diff a3671d4..HEAD --stat -- "
        "src/reincarnated/simulation/spatial_gauntlet src/reincarnated/generation 2>/dev/null").read().strip()
    head_invariant_ok = (subtree_delta == "")

    out = {
        "artifact": "tier3-w3-gate-output",
        "run": "Tier-3 Encounter-Geometry Run · Wave W3 · T3-F4 GATE (mechanical execution)",
        "author": "gamora", "date": "2026-07-22",
        "header": {
            "substrate_md5": md5,
            "sidecar_commit": SIDECAR_COMMIT,
            "prereg_freeze_commit": PREREG_FREEZE_COMMIT,
            "prereg_doc": PREREG_DOC,
            "engine_head_at_open": ENGINE_HEAD_BASELINE,
            "engine_head_at_close": engine_head_close,
            "head_state_invariant_ok": head_invariant_ok,
            "head_subtree_delta_a3671d4_to_close": subtree_delta or "(empty — byte-identical)",
            "seeds": SEEDS, "damage_modifier": DAMAGE_MODIFIER,
            "frozen_X_effect_size": GATE_X, "frozen_Y_min_correct": GATE_Y_MIN_CORRECT,
            "frozen_Y_pct": "75% (>=24/32)", "sd_pool": SD_POOL,
            "mob_parity_total": MOB_PARITY_TOTAL,
            "zero_writes_to_engine_repo": True,
        },
        "verdict": verdict,
        "gate_legs": {
            "leg1_showcase": {"metric": "median composite d over 16 high-fit pairs",
                              "value": leg1_median, "threshold": f">= +{GATE_X}", "pass": leg1_pass},
            "leg2_stress": {"metric": "median composite d over 16 low-fit pairs",
                            "value": leg2_median, "threshold": f"<= -{GATE_X}", "pass": leg2_pass},
            "leg3_direction": {"metric": "pairs sign-correct (>=2 of 3 metric d's predicted sign)",
                               "value": f"{leg3_n}/{leg3_total}", "threshold": f">= {GATE_Y_MIN_CORRECT}/32",
                               "pass": leg3_pass},
        },
        "decomposition": {
            "per_era_legs": per_era_legs,
            "per_family_mean_composite_d": per_family_mean_d,
            "per_metric_medians": per_metric_medians,
            "membership_tier_mix_of_scored_pairs": dict(tier_mix),
            "n_scored_pairs": len(scored), "n_red_flag_pairs": len(red_flag_pairs),
        },
        "selection_census": selection_census,
        "wave_red_flags": wave_red_flags,
        "formation_builder_red_flags": formation_red_flags,
        "smoke_nonpassive_check": {"targets": len(smoke_results), "results": smoke_results,
                                   "build_seconds": round(build_s, 1)},
        "per_pair_table": per_pair,
        "fight_records": fight_records,
        "wall_seconds": round(wall, 1),
        "prereg_caveat": ("MECHANICAL EXECUTION of the FROZEN sheet (5ea56bf3). Zero design "
                          "discretion; any pin the sheet does not decide is a red-flag, not an "
                          "improvised rule. The prereg IS the math note (Discipline #1)."),
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    # ---- print ----
    print("=" * 82)
    print("TIER-3 W3 · T3-F4 GATE · MECHANICAL EXECUTION OF THE FROZEN SHEET")
    print("=" * 82)
    print(f"substrate md5:        {md5[:8]} (expected {EXPECTED_MD5_PREFIX})  "
          f"{'OK' if md5.startswith(EXPECTED_MD5_PREFIX) else 'MISMATCH'}")
    print(f"engine HEAD open/close: {ENGINE_HEAD_BASELINE} / {engine_head_close[:7]}  "
          f"HEAD-invariant {'OK' if head_invariant_ok else 'VIOLATED'}")
    print(f"seeds {SEEDS} dmod={DAMAGE_MODIFIER}  X={GATE_X} Y>={GATE_Y_MIN_CORRECT}/32")
    print(f"PlayerClass builds: {len(pc_cache)} cells in {build_s:.1f}s   fights wall: {wall:.1f}s")
    print("-" * 82)
    print("SELECTION CENSUS (families + courts per era):")
    for era in ERAS:
        sc_e = selection_census[era]
        print(f"  Era {era}: fams={sc_e['families_drafted']}")
        print(f"           courts={sc_e['courts_drafted']} (n={sc_e['n_courts']}, "
              f"check {'OK' if sc_e['courts_check_ok'] else 'FAIL'})  swaps={len(sc_e['swap_log'])}")
    print("-" * 82)
    print("GATE LEGS:")
    print(f"  LEG1 showcase (median composite d, 16 high): {leg1_median}  "
          f">= +{GATE_X} ? {leg1_pass}")
    print(f"  LEG2 stress   (median composite d, 16 low):  {leg2_median}  "
          f"<= -{GATE_X} ? {leg2_pass}")
    print(f"  LEG3 direction: {leg3_n}/{leg3_total} sign-correct  >= {GATE_Y_MIN_CORRECT}/32 ? {leg3_pass}")
    print("-" * 82)
    print("PER-ERA (descriptive):")
    for era in ERAS:
        e = per_era_legs[era]
        print(f"  Era {era}: high_med={e['high_median_composite_d']}  low_med={e['low_median_composite_d']}  "
              f"sign_correct={e['n_sign_correct']}/{e['n_pairs']}")
    print("-" * 82)
    print(f"membership_tier mix (scored pairs): {dict(tier_mix)}")
    print(f"red-flag pairs (hole-cell, RF-A): {len(red_flag_pairs)}")
    if red_flag_pairs:
        for p in red_flag_pairs:
            print(f"    RED-FLAG {p['era']}/{p['side']} {p['kit_id']}: {p['red_flag']}")
    print("WAVE RED-FLAGS:")
    for wrf in wave_red_flags:
        print(f"    {wrf['id']} [{wrf['class']}]")
    print("=" * 82)
    print(f"VERDICT: {verdict}")
    print("=" * 82)
    print(f"wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
