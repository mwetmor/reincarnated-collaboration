#!/usr/bin/env python3
"""
Tier-3 W3' — T3-F4' GATE (MECHANICAL EXECUTION of the FROZEN amendment sheet).

WAVE W3' of the Tier-3 Encounter-Geometry Run (conductor: gandalf RUN-CONDUCTOR). The gate
instrument is PRE-REGISTERED + FROZEN: amendment sheet
agentic_orchestration/gandalf/notes/2026-07-22-tier3-w3prime-prereg.md (frozen 904f317c, clean PASS
c47f6cc8) + base sheet 2026-07-22-tier3-w3-prereg.md (5ea56bf3, incorporated by reference). This
executable is ZERO-DISCRETION mechanical execution: every clause is law; a situation the sheets do
not decide is a RED-FLAG (stop, record, continue/HALT), never an improvised rule.

WHAT W3' CHANGES vs W3 (the ONLY change): the baseline is COMPOSITION-MATCHED (amendment §2). For each
pair, the baseline = the open arena's DEFAULT PLACEMENT holding that pair's EXACT encounter mob
multiset (count + tier + per-mob HP + scalars). The fighter AND the HP budget both cancel in Delta;
the manipulated variable is placement geometry ALONE. Mechanical resolutions M1-M3, S1, D1, G1, E1
are recorded in 2026-07-22-tier3-w3prime-gate-math.md (the prereg sheets ARE the math note).

EXECUTION ORDER (amendment §7 + §8):
  1. Eligibility redraw: exclude family_present=hole BOTH sides (§5). Redraw argmin/argmax to next-best
     under UNCHANGED base §5.2-5.7. Full 32 pairs. Emit selection census (as W3).
  2. Build 32 encounters (COMMON-4 builders, argmax/argmin per base §5.4, strain-4 excluded, dmod=1.0).
  3. Build 32 matched baselines: encounter's EXACT mob multiset placed at open_arena default (x,y).
     COMPOSITION-PARITY HARD INVARIANT verified per pair (count+tier+HP+scalars); mismatch -> red-flag.
  4. Run 128 baseline fights (32 x 4 seeds). NO MEMOIZATION (§8.4 C6): every pair's baseline runs.
  5. Compute + SEAL: per-cell 4-seed means -> sd_pool'(m) = between-cell stdev over 32 cell means ->
     degeneracy flags (§4 + §8.3: DEGENERATE iff sd_pool'=0 OR >=29/32 cell MEANS at bound;
     mobs_killed bound=40, others none) -> informative count + renormalized sign rule. WRITE the seal
     JSON NOW (before ANY encounter fight); md5 it; IMMUTABLE hereafter.
  6. Run 128 encounter fights (same seeds, same fighter).
  7. Gate legs: per-pair d_m = mean_over_4_seeds(m_enc - m_matched_baseline)/sd_pool'(m); composite =
     median of INFORMATIVE d's; verdict = showcase median>=+0.5 AND stress median<=-0.5 AND
     direction>=24/32 sign-correct under SEALED renormalized rule. NO partial pass. If §4 fired:
     REPORT recomputed alpha (§8.4 C5); gate parameter stays >=24/32.
  8. Emit runner + seal + gate-output + report.

Substrate: corpus.db md5 d091881d (READ-ONLY, md5-checked open+close). Sidecar 6dd43161. Engine harness
imported BY PATH, READ-ONLY; ZERO writes to the engine repo. Author: gamora, 2026-07-22.

Run:  python3 2026-07-22-tier3-w3prime-gate.py
"""
import hashlib
import json
import math
import os
import statistics
import subprocess
import sqlite3
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DB = os.path.abspath(os.path.join(HERE, "..", "..", "research", "curated", "corpus.db"))
SIDECAR = os.path.join(HERE, "..", "..", "elrond", "notes",
                       "2026-07-22-tier3-family-membership-sidecar.json")
V2_FIT = os.path.join(HERE, "2026-07-22-tier3-w2-fit-output-v2.json")
PREREG_DOC = os.path.abspath(os.path.join(HERE, "..", "..", "gandalf", "notes",
                                          "2026-07-22-tier3-w3prime-prereg.md"))
BASE_PREREG_DOC = os.path.abspath(os.path.join(HERE, "..", "..", "gandalf", "notes",
                                               "2026-07-22-tier3-w3-prereg.md"))
SEAL_PATH = os.path.join(HERE, "2026-07-22-tier3-w3prime-pregate-seal.json")
OUT_PATH = os.path.join(HERE, "2026-07-22-tier3-w3prime-gate-output.json")

EXPECTED_MD5_PREFIX = "d091881d"
SIDECAR_COMMIT = "6dd43161"
PREREG_FREEZE_COMMIT = "904f317c"      # amendment sheet frozen commit
PREREG_CLEAN_PASS = "c47f6cc8"         # freeze-beat clean PASS
BASE_PREREG_FREEZE = "5ea56bf3"        # base sheet frozen commit
ENGINE_HEAD_STAMP = "a3671d4215489c4ddb58d69ebe1311784a946df4"   # fire stamp (== W3 baseline HEAD)

# ----- FROZEN sheet constants (do NOT re-derive; the preregs ARE the math note) -----
SEEDS = [20260722, 20260723, 20260724, 20260725]      # §6 shared seed set (baseline-identical)
DAMAGE_MODIFIER = 1.0                                   # §6 dmod=1.0 uniform
MOB_PARITY_TOTAL = 40                                   # §2 composition parity: count=40
GATE_X = 0.5                                            # §3/§6 effect-size threshold (standardized)
GATE_Y_MIN_CORRECT = 24                                 # §4/§6 direction: >=24 of 32 (75%)
PRIMARY_METRICS = ["mobs_killed", "total_aoe_hits", "player_damage_total"]  # §6 metric subset
METRIC_BOUND = {"mobs_killed": 40.0, "total_aoe_hits": None, "player_damage_total": None}  # §4/§8.3
DEGEN_AT_BOUND_MIN = 29                                 # §8.3 C3(ii): >=29 of 32 cell MEANS at bound
MIN_COURTS = 3                                          # §5.4 courts check
ERAS = ("I", "II", "III", "IV")

# ----- Strain-4 formations EXCLUDED (§5.4 encounter construction; W2 probe verdicts) -----
STRAIN4_EXCLUDED = frozenset({
    "cbn_corridor_arc", "cb_crossfire", "ts_environmental_nest", "ss_phase_transform",
})

# ----- formation_id -> COMMON-4 builder class (transcribed VERBATIM from the W3 runner) -----
FORMATION_TO_COMMON4 = {
    "ms_swarm_surround": "swarm", "ww_converge_spin": "swarm", "ww_arc_sweep": "swarm",
    "ww_derived_frenzy_line": "swarm", "da_field_retreat": "swarm", "ss_derived_form_swap": "swarm",
    "ms_wedge_advance": "lane", "tm_preseed_corridor": "lane", "cb_lane_hold": "lane",
    "ds_flank_burst": "lane", "ds_derived_gap_close": "lane",
    "mpv_fan_from_position": "volley-fan", "mpv_boss_sweep": "volley-fan",
    "da_curse_at_distance": "volley-fan",
    "ts_anchor_screen": "emplacement", "ts_resurrection_loop": "emplacement",
    "aura_carrier_pack": "emplacement", "aura_matron_center": "emplacement",
    "tm_ritual_minefield": "emplacement", "tm_spawner_nest": "emplacement",
    "cbn_derived_arc_pass": "emplacement",
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
    Arena, ArenaScenario, SpawnSpec, SCENARIO_OPEN_ARENA,
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
# Frozen fit-component logic — transcribed VERBATIM from the W3 runner.
# ---------------------------------------------------------------------------
W_VERB, W_TOPO, W_SHELF = 0.50, 0.30, 0.20

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
# Baseline fighter-mapping code — reused BYTE-IDENTICAL from the W3 runner.
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
    byte-identical across ALL fights (neutrality). BOTH arms (encounter + matched baseline) call this
    with the encounter's tier list -> IDENTICAL mob_dicts (composition parity)."""
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


def md5_str(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# ENCOUNTER formation scenario builders — 44x44 neutral arena (byte-identical to W3), 40 spawns.
# scenario_id is NEW (t3w3p_*) so the engine MOB_HP_DIFFICULTY x1.5 gate does NOT fire (geometry, not
# HP tuning). apply_mob_hp_difficulty_multiplier=False is ALSO passed (doubly-inert, resolution M2).
# ---------------------------------------------------------------------------
_ARENA_W = _ARENA_H = 44.0
_PLAYER_SPAWN = SpawnSpec(x=22.0, y=38.0, heading_rad=-math.pi / 2, entity_radius=0.5,
                          threat_tier="player", archetype_tag="player")


def _formation_spawns(fclass):
    """Return the 40-spawn ENCOUNTER layout for a COMMON-4 class (byte-identical to W3 runner)."""
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


def make_encounter_scenario(fclass):
    """(scenario, red_flag_or_None). Enforces count=40 (§2 parity): a builder whose layout is not
    exactly 40 or lands out of bounds -> red-flag (no silent normalize)."""
    spawns = _formation_spawns(fclass)
    if len(spawns) != MOB_PARITY_TOTAL:
        return None, f"encounter builder {fclass} produced {len(spawns)} spawns != {MOB_PARITY_TOTAL}"
    oob = [(sp.x, sp.y) for sp in spawns
           if not (0.5 <= sp.x <= _ARENA_W - 0.5 and 0.5 <= sp.y <= _ARENA_H - 0.5)]
    if oob:
        return None, f"encounter builder {fclass} has {len(oob)} out-of-bounds spawns (e.g. {oob[0]})"
    arena = Arena(width_m=_ARENA_W, height_m=_ARENA_H, choke_zones=[], name=f"t3w3p_{fclass}_44x44")
    scen = ArenaScenario(
        scenario_id=f"t3w3p_{fclass}", description=f"T3-W3' neutral-arena {fclass} formation (40-parity)",
        arena=arena, player_spawn=_PLAYER_SPAWN, mob_spawns=spawns,
        max_duration_s=120.0, win_condition="all_mobs_killed", boss_index=None)
    return scen, None


# ---------------------------------------------------------------------------
# MATCHED-BASELINE scenario builder (amendment §2; resolutions M1-M3).
# The encounter's EXACT mob multiset placed at the open_arena DEFAULT (x,y) positions. The MULTISET
# (count+tier) comes from the ENCOUNTER; the PLACEMENT (x,y) comes from the open_arena default layout.
# Fresh scenario_id t3w3p_base_* (NOT open_arena) so the 1.5x MOB_HP_DIFFICULTY gate does NOT fire
# (M2). Per-mob HP stays 150 (via build_neutral_mob_dicts on the encounter tiers) == encounter (parity).
# ---------------------------------------------------------------------------
_OA = SCENARIO_OPEN_ARENA
_OA_POS = [(sp.x, sp.y) for sp in _OA.mob_spawns]           # open_arena default 40 positions (M1/M3)
_OA_PLAYER = _OA.player_spawn                               # open_arena default player spawn
_OA_W = _OA.arena.width_m
_OA_H = _OA.arena.height_m
_OA_SERIAL = getattr(_OA, "serial_activation_radius_m", None)
_LEASH_SWARM = 35.0    # open_arena swarm-convention leash (all encounter mobs are non-elite; M3)


def make_matched_baseline_scenario(fclass, encounter_tiers):
    """(scenario, red_flag_or_None). Place the encounter's homogeneous multiset at the open_arena
    default (x,y) positions. Re-tier each default position to the encounter tier (parity). Fresh
    scenario_id -> no 1.5x. Verifies count=40 and in-bounds on the 36x36 open arena."""
    if len(encounter_tiers) != MOB_PARITY_TOTAL or len(_OA_POS) != MOB_PARITY_TOTAL:
        return None, (f"matched-baseline {fclass}: encounter tiers={len(encounter_tiers)} / "
                      f"open_arena positions={len(_OA_POS)} (need {MOB_PARITY_TOTAL} both)")
    spawns = []
    for (x, y), tier in zip(_OA_POS, encounter_tiers):
        # all encounter mobs are non-elite swarm/magic -> swarm-convention 35m leash, swarmer tag.
        spawns.append(SpawnSpec(x=x, y=y, heading_rad=-math.pi / 2, entity_radius=0.5,
                                threat_tier=tier, archetype_tag="swarmer",
                                leash_distance_override_m=_LEASH_SWARM))
    oob = [(sp.x, sp.y) for sp in spawns
           if not (0.5 <= sp.x <= _OA_W - 0.5 and 0.5 <= sp.y <= _OA_H - 0.5)]
    if oob:
        return None, f"matched-baseline {fclass} has {len(oob)} out-of-bounds spawns (e.g. {oob[0]})"
    arena = Arena(width_m=_OA_W, height_m=_OA_H, choke_zones=[], name=f"t3w3p_base_{fclass}_36x36")
    kw = dict(scenario_id=f"t3w3p_base_{fclass}",
              description=f"T3-W3' matched baseline: {fclass} multiset at open-arena default placement",
              arena=arena, player_spawn=_OA_PLAYER, mob_spawns=spawns,
              max_duration_s=120.0, win_condition="all_mobs_killed", boss_index=None)
    if _OA_SERIAL is not None:
        kw["serial_activation_radius_m"] = _OA_SERIAL
    return ArenaScenario(**kw), None


def multiset_signature(mob_dicts, spawns):
    """Composition signature for the PARITY invariant: sorted (tier, hp, armor, energy) tuples +
    count. Compared encounter-vs-baseline; equality is the §2 HARD INVARIANT."""
    tiers = [sp.threat_tier for sp in spawns]
    sig = sorted((t, round(md["max_hp"], 3), round(md["armor"], 3), round(md["energy"], 3))
                 for t, md in zip(tiers, mob_dicts))
    return {"count": len(mob_dicts), "sig": sig}


# ---------------------------------------------------------------------------
# STEP 1 — SELECTION (deterministic family round-robin + courts check).
# ---------------------------------------------------------------------------
def load_full_fit_rows():
    """v2 fit rows scoring_basis=full AND family_present != hole (§5 RF-A fix), enriched with each
    kit's corpus BC + court + sidecar family."""
    v2 = json.load(open(V2_FIT))
    fit = [r for r in v2["fit_records"]
           if r["scoring_basis"] == "full" and r.get("family_present") != "hole"]   # §5: exclude hole
    sc = json.load(open(SIDECAR))
    active = {r["kit_id"]: r["family"] for r in sc["memberships"]
              if not r.get("shadowed_by") and r.get("on_spine")}
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
            "family_present": r.get("family_present"),
            "draft_family": active.get(kid),
            "membership_tier": r["membership_tier"], "fit_score": r["fit_score"],
            "court": b.get("court"), "element": b.get("original_element"),
            "range_val": b.get("range_val"), "tempo_val": b.get("tempo_val"),
            "amp_val": b.get("amp_val"), "proxy_val": b.get("proxy_val"),
            "commit_val": b.get("commit_val"), "attr_val": b.get("attr_val"),
            "verb_affinity": r["verb_affinity"], "shelf_affinity": r["shelf_affinity"],
        })
    return out


def round_robin_draft(candidates, side):
    """§5.2-3 kit-side family round-robin (VERBATIM logic from the W3 runner). side='high' ->
    descending fit_score; 'low' -> ascending. No family (draft_family) contributes a 2nd kit until
    every family with >=1 candidate has contributed one. Tiebreak: kit_id lexicographic ascending."""
    reverse = (side == "high")
    ordered = sorted(candidates, key=lambda c: c["kit_id"])                       # kit_id asc tie
    ordered = sorted(ordered, key=lambda c: c["fit_score"], reverse=reverse)      # fit primary
    families_with_candidate = set(c["draft_family"] for c in candidates)
    picked = []
    used_families = set()
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
            for c in list(remaining):
                picked.append(c)
                remaining.remove(c)
                if len(picked) == 4:
                    break
            break
    return picked[:4]


def courts_swap(picked_high, picked_low, candidates_high, candidates_low, deck_median):
    """§5.4 courts check (>=3 element-courts across the 8 drafted kits). Swap the least-extreme pick
    (smallest |fit - deck_median|, ties kit_id asc) for the next-best candidate from a MISSING court
    (§5.7). VERBATIM logic from the W3 runner."""
    swap_log = []
    all8 = picked_high + picked_low
    if len(set(c["court"] for c in all8)) >= MIN_COURTS:
        return picked_high, picked_low, swap_log
    while len(set(c["court"] for c in (picked_high + picked_low))) < MIN_COURTS:
        all8 = picked_high + picked_low
        present_courts = set(c["court"] for c in all8)
        drafted_ids = set(c["kit_id"] for c in all8)
        pool = [c for c in (candidates_high + candidates_low)
                if c["court"] not in present_courts and c["kit_id"] not in drafted_ids]
        if not pool:
            swap_log.append({"result": "NO_MISSING_COURT_CANDIDATE",
                             "present_courts": sorted(present_courts)})
            break
        least = min(all8, key=lambda c: (abs(c["fit_score"] - deck_median), c["kit_id"]))
        on_high = any(c["kit_id"] == least["kit_id"] for c in picked_high)
        repl = (max(pool, key=lambda c: (c["fit_score"], [-ord(ch) for ch in c["kit_id"]]))
                if on_high else
                min(pool, key=lambda c: (c["fit_score"], c["kit_id"])))
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
# STEP 2 — FORMATION ASSIGNMENT (per-formation fit sub-score, VERBATIM from W3 runner).
# ---------------------------------------------------------------------------
def per_formation_subscores(kit_row):
    family = kit_row["family"]
    era = kit_row["era"]
    verb_aff = kit_row["verb_affinity"]
    shelf_aff = kit_row["shelf_affinity"]
    subs = []
    for fid in formations_for(family, era):
        if fid in STRAIN4_EXCLUDED:
            continue
        common4 = FORMATION_TO_COMMON4.get(fid)
        if common4 is None:
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
# helpers
# ---------------------------------------------------------------------------
def median3(vals):
    return statistics.median(vals)


def run_one_fight(scen, cd, pc, seed, session_id, season_id):
    """One spatial fight; apply_mob_hp_difficulty_multiplier=False (resolution M2). Returns metric row."""
    tiers = [sp.threat_tier for sp in scen.mob_spawns]
    mobs = build_neutral_mob_dicts(tiers)
    raw = run_spatial_fight(scenario=scen, class_dict=cd, mob_dicts=mobs, n_fights=1,
                            session_id=session_id, base_seed=seed, season_id=season_id,
                            player_class=pc, damage_modifier=DAMAGE_MODIFIER,
                            track_proxy_population=False, apply_mob_hp_difficulty_multiplier=False)
    fr = raw["fight_results"][0]
    row = {"seed": seed}
    for m in PRIMARY_METRICS + ["elapsed_s", "max_flanking_count", "total_flanking_ticks",
                                "winner", "total_mob_count"]:
        v = getattr(fr, m, None)
        row[m] = v if isinstance(v, str) else (float(v) if v is not None else None)
    return row


def cell_means(fight_rows):
    """4-seed mean per primary metric over the ok fights of one cell."""
    out = {}
    for m in PRIMARY_METRICS:
        vals = [f[m] for f in fight_rows if "error" not in f and f.get(m) is not None]
        out[m] = (sum(vals) / len(vals)) if vals else None
    return out


def main():
    t_open = time.perf_counter()
    md5_open = md5_check(CORPUS_DB)
    if not md5_open.startswith(EXPECTED_MD5_PREFIX):
        print(f"FATAL: corpus md5 {md5_open} != {EXPECTED_MD5_PREFIX}", file=sys.stderr)
        sys.exit(2)

    # ---- HEAD-state invariant: stamp at fire; subtrees byte-identical to stamp else HALT (§6/§7) ----
    def _git(args):
        return subprocess.run(["git", "-C", os.path.abspath(os.path.join(ENGINE_SRC, "..")), *args],
                              capture_output=True, text=True).stdout.strip()
    engine_head_fire = _git(["rev-parse", "HEAD"])
    subtree_delta_fire = _git(["diff", ENGINE_HEAD_STAMP + "..HEAD", "--stat", "--",
                               "src/reincarnated/simulation/spatial_gauntlet",
                               "src/reincarnated/generation"])
    if subtree_delta_fire != "":
        print("HALT: engine subtree drifted from fire stamp BEFORE run:\n" + subtree_delta_fire,
              file=sys.stderr)
        json.dump({"verdict": "HALT", "reason": "engine_subtree_drift_at_fire",
                   "engine_head_stamp": ENGINE_HEAD_STAMP, "engine_head_fire": engine_head_fire,
                   "subtree_delta": subtree_delta_fire}, open(OUT_PATH, "w"), indent=2)
        sys.exit(4)

    full_rows = load_full_fit_rows()

    # ---- STEP 1: per-era selection (eligibility redraw already applied in load_full_fit_rows) ----
    selection = {}
    for era in ERAS:
        cands = [r for r in full_rows if r["era"] == era]
        deck_median = statistics.median([c["fit_score"] for c in cands])
        high = round_robin_draft(cands, "high")
        low = round_robin_draft(cands, "low")
        high, low, swap_log = courts_swap(high, low, cands, cands, deck_median)
        selection[era] = {"high": high, "low": low, "swap_log": swap_log,
                          "deck_median_fit": round(deck_median, 4), "n_candidates": len(cands)}

    # ---- STEP 2: formation assignment per pair ----
    pairs = []
    for era in ERAS:
        for side in ("high", "low"):
            for kit_row in selection[era][side]:
                chosen, subs, rf = assign_formation(kit_row, side)
                pairs.append({"era": era, "side": side, "kit_row": kit_row,
                              "formation": chosen, "formation_subscores": subs, "red_flag": rf})

    # ---- fighter build (byte-identical mapping to baseline) ----
    cells = _neutral_cells()
    con = sqlite3.connect(f"file:{CORPUS_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    sc = json.load(open(SIDECAR))
    active_ids = {r["kit_id"] for r in sc["memberships"]
                  if not r.get("shadowed_by") and r.get("on_spine")}
    all_kits = []
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

    # ---- pre-build the 4 encounter scenarios + record their homogeneous tier-lists ----
    encounter_scenarios, encounter_red_flags, encounter_tiers = {}, {}, {}
    for fclass in ("swarm", "volley-fan", "lane", "emplacement"):
        scen, rf = make_encounter_scenario(fclass)
        encounter_scenarios[fclass] = scen
        if rf:
            encounter_red_flags[fclass] = rf
        else:
            encounter_tiers[fclass] = [sp.threat_tier for sp in scen.mob_spawns]

    # ---- pre-build the 4 matched-baseline scenarios (open-arena placement, encounter multiset) ----
    baseline_scenarios, baseline_red_flags, parity_checks = {}, {}, {}
    for fclass in ("swarm", "volley-fan", "lane", "emplacement"):
        if fclass in encounter_red_flags:
            continue
        etiers = encounter_tiers[fclass]
        bscen, rf = make_matched_baseline_scenario(fclass, etiers)
        baseline_scenarios[fclass] = bscen
        if rf:
            baseline_red_flags[fclass] = rf
            continue
        # COMPOSITION-PARITY HARD INVARIANT (§2 bullet 3): encounter vs baseline multiset equality.
        e_mobs = build_neutral_mob_dicts(etiers)
        b_mobs = build_neutral_mob_dicts([sp.threat_tier for sp in bscen.mob_spawns])
        e_sig = multiset_signature(e_mobs, encounter_scenarios[fclass].mob_spawns)
        b_sig = multiset_signature(b_mobs, bscen.mob_spawns)
        parity_ok = (e_sig == b_sig)
        parity_checks[fclass] = {
            "parity_ok": parity_ok,
            "encounter_count": e_sig["count"], "baseline_count": b_sig["count"],
            "encounter_tier_mix": dict(Counter(sp.threat_tier for sp in encounter_scenarios[fclass].mob_spawns)),
            "baseline_tier_mix": dict(Counter(sp.threat_tier for sp in bscen.mob_spawns)),
            "encounter_hp_multiset": dict(Counter(round(md["max_hp"], 1) for md in e_mobs)),
            "baseline_hp_multiset": dict(Counter(round(md["max_hp"], 1) for md in b_mobs)),
        }
        if not parity_ok:
            baseline_red_flags[fclass] = f"COMPOSITION-PARITY VIOLATION on {fclass}: multisets differ"

    # ---- Discipline #11 smoke: 2 non-red-flagged pairs, non-passive check (as W3) ----
    smoke_targets = [p for p in pairs if p["red_flag"] is None and p["formation"] is not None
                     and p["formation"]["common4_class"] not in encounter_red_flags][:2]
    smoke_results = []
    for p in smoke_targets:
        kid = p["kit_row"]["kit_id"]
        cid = cell_of.get(kid)
        pc, cd = pc_cache[cid]
        fclass = p["formation"]["common4_class"]
        row = run_one_fight(encounter_scenarios[fclass], cd, pc, SEEDS[0],
                            f"w3p_smoke_{kid}", "tier3-w3prime-smoke")
        mk = int(row.get("mobs_killed") or 0)
        pd_ = float(row.get("player_damage_total") or 0.0)
        smoke_results.append({"kit_id": kid, "cell": cid, "formation_class": fclass,
                              "mobs_killed": mk, "player_damage_total": pd_,
                              "passive": (mk == 0 and pd_ == 0.0)})
    if any(s["passive"] for s in smoke_results):
        print("SMOKE FAIL: passive player on a formation scenario — STOP (do not patch generation).",
              file=sys.stderr)
        json.dump({"verdict": "HALT", "reason": "passive_player_smoke_fail",
                   "smoke_results": smoke_results}, open(OUT_PATH, "w"), indent=2)
        sys.exit(3)

    # ---- STEP 4: run the 128 BASELINE fights (NO MEMOIZATION, §8.4 C6) ----
    t_base = time.perf_counter()
    baseline_records = []
    for p in pairs:
        era, side = p["era"], p["side"]
        kid = p["kit_row"]["kit_id"]
        if p["red_flag"] is not None or p["formation"] is None:
            baseline_records.append({"era": era, "side": side, "kit_id": kid,
                                     "red_flag": p["red_flag"], "fights": [], "skipped": True})
            continue
        fclass = p["formation"]["common4_class"]
        if fclass in encounter_red_flags or fclass in baseline_red_flags:
            baseline_records.append({"era": era, "side": side, "kit_id": kid,
                                     "red_flag": encounter_red_flags.get(fclass)
                                     or baseline_red_flags.get(fclass), "fights": [], "skipped": True})
            continue
        cid = cell_of.get(kid)
        pc, cd = pc_cache[cid]
        bscen = baseline_scenarios[fclass]
        per_seed = []
        for seed in SEEDS:
            try:
                per_seed.append(run_one_fight(bscen, cd, pc, seed, f"w3p_base_{kid}_{side}",
                                              "tier3-w3prime-baseline"))
            except SpatialFightConvergenceError as e:
                per_seed.append({"seed": seed, "error": "convergence", "detail": str(e)[:120]})
            except Exception as e:  # noqa: BLE001
                per_seed.append({"seed": seed, "error": type(e).__name__, "detail": str(e)[:120]})
        baseline_records.append({"era": era, "side": side, "kit_id": kid,
                                 "family": p["kit_row"]["family"], "formation_class": fclass,
                                 "formation_id": p["formation"]["formation_id"],
                                 "assigned_cell": cid, "fights": per_seed, "skipped": False})
    base_wall = time.perf_counter() - t_base

    # ---- STEP 5: sd_pool' + degeneracy + SEAL (BEFORE any encounter fight) ----
    scored_base = [b for b in baseline_records if not b.get("skipped")
                   and any("error" not in f for f in b["fights"])]
    per_cell_baseline_means = []
    for b in scored_base:
        cm = cell_means(b["fights"])
        per_cell_baseline_means.append({"era": b["era"], "side": b["side"], "kit_id": b["kit_id"],
                                        "formation_class": b["formation_class"], "means": cm})
    sd_pool_prime = {}
    for m in PRIMARY_METRICS:
        means = [c["means"][m] for c in per_cell_baseline_means if c["means"].get(m) is not None]
        sd_pool_prime[m] = (statistics.pstdev(means) if len(means) >= 1 else 0.0)  # between-cell stdev

    # degeneracy (§4 + §8.3 C3): sd_pool'=0 OR >=29/32 cell MEANS exactly at the hard structural bound.
    degeneracy = {}
    n_cells = len(per_cell_baseline_means)
    for m in PRIMARY_METRICS:
        bound = METRIC_BOUND[m]
        at_bound = 0
        if bound is not None:
            at_bound = sum(1 for c in per_cell_baseline_means
                           if c["means"].get(m) is not None and c["means"][m] == bound)
        sd_zero = (sd_pool_prime[m] == 0.0)
        is_degen = sd_zero or (bound is not None and at_bound >= DEGEN_AT_BOUND_MIN)
        degeneracy[m] = {"sd_pool_prime": round(sd_pool_prime[m], 6), "bound": bound,
                         "cells_at_bound": at_bound, "n_cells": n_cells,
                         "sd_pool_prime_is_zero": sd_zero,
                         "at_bound_threshold": DEGEN_AT_BOUND_MIN, "degenerate": is_degen}
    informative = [m for m in PRIMARY_METRICS if not degeneracy[m]["degenerate"]]
    n_inf = len(informative)
    if n_inf == 3:
        sign_rule = ">=2-of-3 informative metrics agree with predicted sign"
    elif n_inf == 2:
        sign_rule = "2-of-2 informative metrics must agree with predicted sign"
    elif n_inf == 1:
        sign_rule = "sign of the single informative metric alone (record LOW-POWER)"
    else:
        sign_rule = "0 informative -> RED-FLAG HALT"

    seal = {
        "artifact": "tier3-w3prime-pregate-seal",
        "sealed_before": "ANY encounter fight (amendment §8.2 C2)",
        "author": "gamora", "date": "2026-07-22",
        "substrate_md5_open": md5_open, "engine_head_fire": engine_head_fire,
        "sd_pool_prime": {m: round(sd_pool_prime[m], 6) for m in PRIMARY_METRICS},
        "degeneracy": degeneracy,
        "informative_metrics": informative, "n_informative": n_inf,
        "renormalized_sign_rule": sign_rule,
        "n_baseline_cells_scored": n_cells,
        "per_cell_baseline_means": per_cell_baseline_means,
        "composition_parity_checks": parity_checks,
        "compositions_by_class": {
            fclass: {"tier_multiset": dict(Counter(encounter_tiers.get(fclass, []))),
                     "count": len(encounter_tiers.get(fclass, []))}
            for fclass in encounter_tiers},
        "baseline_red_flags": baseline_red_flags,
        "encounter_red_flags": encounter_red_flags,
        "seeds": SEEDS, "note": "sd_pool' + degeneracy + sign-rule are IMMUTABLE after this point.",
    }
    seal_json = json.dumps(seal, indent=2, sort_keys=True)
    with open(SEAL_PATH, "w") as f:
        f.write(seal_json)
    seal_md5 = md5_str(seal_json)

    # ---- §4/§8.3: 0 informative -> RED-FLAG HALT (no improvised metric swap) ----
    if n_inf == 0:
        print("RED-FLAG HALT: 0 informative metrics after degeneracy determination (§4).", file=sys.stderr)
        json.dump({"verdict": "HALT", "reason": "zero_informative_metrics_degeneracy",
                   "seal_md5": seal_md5, "degeneracy": degeneracy}, open(OUT_PATH, "w"), indent=2)
        sys.exit(5)

    # ---- STEP 6: run the 128 ENCOUNTER fights (same seeds, same fighter) ----
    t_enc = time.perf_counter()
    encounter_recs = []
    for p in pairs:
        era, side = p["era"], p["side"]
        kit_row = p["kit_row"]
        kid = kit_row["kit_id"]
        if p["red_flag"] is not None or p["formation"] is None:
            encounter_recs.append({"era": era, "side": side, "kit_id": kid,
                                   "red_flag": p["red_flag"], "fights": [], "skipped": True})
            continue
        fclass = p["formation"]["common4_class"]
        if fclass in encounter_red_flags or fclass in baseline_red_flags:
            encounter_recs.append({"era": era, "side": side, "kit_id": kid,
                                   "red_flag": encounter_red_flags.get(fclass)
                                   or baseline_red_flags.get(fclass), "fights": [], "skipped": True})
            continue
        cid = cell_of.get(kid)
        pc, cd = pc_cache[cid]
        scen = encounter_scenarios[fclass]
        per_seed = []
        for seed in SEEDS:
            try:
                per_seed.append(run_one_fight(scen, cd, pc, seed, f"w3p_enc_{kid}_{side}",
                                              "tier3-w3prime-encounter"))
            except SpatialFightConvergenceError as e:
                per_seed.append({"seed": seed, "error": "convergence", "detail": str(e)[:120]})
            except Exception as e:  # noqa: BLE001
                per_seed.append({"seed": seed, "error": type(e).__name__, "detail": str(e)[:120]})
        encounter_recs.append({
            "era": era, "side": side, "kit_id": kid, "family": kit_row["family"],
            "draft_family": kit_row["draft_family"], "membership_tier": kit_row["membership_tier"],
            "court": kit_row["court"], "fit_score": kit_row["fit_score"],
            "formation_id": p["formation"]["formation_id"], "formation_class": fclass,
            "formation_fit_subscore": p["formation"]["fit_subscore"],
            "assigned_cell": cid, "cell_distance": dist_of.get(kid),
            "fights": per_seed, "skipped": False})
    enc_wall = time.perf_counter() - t_enc

    # ---- STEP 7: gate computation (composition-matched deltas; informative-metric composite) ----
    base_by_key = {(b["era"], b["side"], b["kit_id"]): b for b in baseline_records}
    per_pair = []
    for er in encounter_recs:
        key = (er["era"], er["side"], er["kit_id"])
        if er.get("skipped"):
            per_pair.append({"era": er["era"], "side": er["side"], "kit_id": er["kit_id"],
                             "red_flag": er.get("red_flag"), "skipped": True})
            continue
        b = base_by_key.get(key)
        b_means = cell_means(b["fights"]) if b and not b.get("skipped") else {}
        enc_ok = [f for f in er["fights"] if "error" not in f]
        base_ok = [f for f in b["fights"] if "error" not in f] if b else []
        # per-seed matched deltas: pair encounter seed with matched-baseline seed (same seed set)
        d_m = {}
        sign_correct_metrics = 0
        predicted_sign = +1 if er["side"] == "high" else -1
        for m in PRIMARY_METRICS:
            enc_by_seed = {f["seed"]: f[m] for f in enc_ok if f.get(m) is not None}
            base_by_seed = {f["seed"]: f[m] for f in base_ok if f.get(m) is not None}
            common = [s for s in SEEDS if s in enc_by_seed and s in base_by_seed]
            if not common or sd_pool_prime[m] == 0.0:
                d_m[m] = None
                continue
            deltas = [enc_by_seed[s] - base_by_seed[s] for s in common]
            mean_delta = sum(deltas) / len(deltas)
            d = mean_delta / sd_pool_prime[m]
            d_m[m] = round(d, 4)
        # sign-correctness counted over INFORMATIVE metrics only (SEALED renormalized rule)
        for m in informative:
            if d_m.get(m) is None:
                continue
            d = d_m[m]
            if (predicted_sign > 0 and d > 0) or (predicted_sign < 0 and d < 0):
                sign_correct_metrics += 1
        inf_dvals = [d_m[m] for m in informative if d_m.get(m) is not None]
        composite = round(median3(inf_dvals), 4) if inf_dvals else None
        # renormalized per-pair sign-correct
        if n_inf == 3:
            pair_sign_correct = (sign_correct_metrics >= 2)
        elif n_inf == 2:
            pair_sign_correct = (sign_correct_metrics == 2)
        else:  # n_inf == 1
            pair_sign_correct = (sign_correct_metrics == 1)
        per_pair.append({
            "era": er["era"], "side": er["side"], "kit_id": er["kit_id"], "family": er["family"],
            "membership_tier": er["membership_tier"], "court": er["court"], "fit_score": er["fit_score"],
            "formation_id": er["formation_id"], "formation_class": er["formation_class"],
            "n_ok_enc_seeds": len(enc_ok), "n_ok_base_seeds": len(base_ok),
            "baseline_means": {m: (round(b_means[m], 3) if b_means.get(m) is not None else None)
                               for m in PRIMARY_METRICS},
            "d_per_metric": d_m, "composite_d_informative": composite,
            "predicted_sign": "+" if predicted_sign > 0 else "-",
            "n_informative_sign_correct": sign_correct_metrics, "pair_sign_correct": pair_sign_correct,
            "skipped": False})

    scored = [p for p in per_pair if not p.get("skipped") and p.get("composite_d_informative") is not None]
    high_pairs = [p for p in scored if p["side"] == "high"]
    low_pairs = [p for p in scored if p["side"] == "low"]
    leg1_median = round(median3([p["composite_d_informative"] for p in high_pairs]), 4) if high_pairs else None
    leg2_median = round(median3([p["composite_d_informative"] for p in low_pairs]), 4) if low_pairs else None
    n_sign_correct = sum(1 for p in scored if p["pair_sign_correct"])
    leg3_total = len(scored)

    leg1_pass = (leg1_median is not None and leg1_median >= GATE_X)
    leg2_pass = (leg2_median is not None and leg2_median <= -GATE_X)
    leg3_pass = (n_sign_correct >= GATE_Y_MIN_CORRECT)
    verdict = "PASS" if (leg1_pass and leg2_pass and leg3_pass) else "FAIL"

    red_flag_pairs = [p for p in per_pair if p.get("red_flag")]
    if red_flag_pairs and verdict == "PASS":
        verdict = "FAIL"  # incomplete sample cannot certify a PASS (no partial pass)

    # ---- §8.4 C5: recomputed alpha for the realized informative configuration (REPORTING only) ----
    def binom_tail_ge(k, n, p=0.5):
        return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))
    alpha_realized = binom_tail_ge(GATE_Y_MIN_CORRECT, leg3_total, 0.5) if leg3_total else None
    degeneracy_fired = any(degeneracy[m]["degenerate"] for m in PRIMARY_METRICS)

    # ---- decompositions ----
    per_era_legs = {}
    for era in ERAS:
        eh = [p for p in high_pairs if p["era"] == era]
        el = [p for p in low_pairs if p["era"] == era]
        per_era_legs[era] = {
            "high_median_composite_d": round(median3([p["composite_d_informative"] for p in eh]), 4) if eh else None,
            "low_median_composite_d": round(median3([p["composite_d_informative"] for p in el]), 4) if el else None,
            "n_sign_correct": sum(1 for p in scored if p["era"] == era and p["pair_sign_correct"]),
            "n_pairs": sum(1 for p in scored if p["era"] == era)}
    per_family_mean_d = {}
    fam_bucket = defaultdict(list)
    for p in scored:
        fam_bucket[p["family"]].append(p["composite_d_informative"])
    for fam, ds in fam_bucket.items():
        per_family_mean_d[fam] = round(sum(ds) / len(ds), 4)
    per_metric_medians = {}
    for m in PRIMARY_METRICS:
        hv = [p["d_per_metric"][m] for p in high_pairs if p["d_per_metric"].get(m) is not None]
        lv = [p["d_per_metric"][m] for p in low_pairs if p["d_per_metric"].get(m) is not None]
        per_metric_medians[m] = {"informative": (m in informative),
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
                      "court": c["court"], "family_present": c["family_present"]} for c in h],
            "low": [{"kit_id": c["kit_id"], "draft_family": c["draft_family"],
                     "membership_tier": c["membership_tier"], "fit_score": c["fit_score"],
                     "court": c["court"], "family_present": c["family_present"]} for c in lo],
            "families_drafted": sorted(set(c["draft_family"] for c in all8)),
            "courts_drafted": sorted(set(c["court"] for c in all8)),
            "n_courts": len(set(c["court"] for c in all8)),
            "courts_check_ok": len(set(c["court"] for c in all8)) >= MIN_COURTS,
            "swap_log": selection[era]["swap_log"]}

    # ---- HEAD invariant re-check at close (byte-identical to stamp through the run) ----
    engine_head_close = _git(["rev-parse", "HEAD"])
    subtree_delta_close = _git(["diff", ENGINE_HEAD_STAMP + "..HEAD", "--stat", "--",
                                "src/reincarnated/simulation/spatial_gauntlet",
                                "src/reincarnated/generation"])
    head_invariant_ok = (subtree_delta_close == "")
    md5_close = md5_check(CORPUS_DB)
    corpus_stable = (md5_open == md5_close)

    out = {
        "artifact": "tier3-w3prime-gate-output",
        "run": "Tier-3 Encounter-Geometry Run · Wave W3' · T3-F4' GATE (mechanical execution)",
        "author": "gamora", "date": "2026-07-22",
        "header": {
            "substrate_md5_open": md5_open, "substrate_md5_close": md5_close,
            "corpus_stable_open_close": corpus_stable,
            "sidecar_commit": SIDECAR_COMMIT,
            "amendment_freeze_commit": PREREG_FREEZE_COMMIT,
            "amendment_clean_pass": PREREG_CLEAN_PASS,
            "base_prereg_freeze_commit": BASE_PREREG_FREEZE,
            "prereg_doc": PREREG_DOC, "base_prereg_doc": BASE_PREREG_DOC,
            "engine_head_stamp": ENGINE_HEAD_STAMP,
            "engine_head_at_fire": engine_head_fire, "engine_head_at_close": engine_head_close,
            "head_state_invariant_ok": head_invariant_ok,
            "head_subtree_delta_stamp_to_close": subtree_delta_close or "(empty — byte-identical)",
            "seeds": SEEDS, "damage_modifier": DAMAGE_MODIFIER,
            "frozen_X_effect_size": GATE_X, "frozen_Y_min_correct": GATE_Y_MIN_CORRECT,
            "frozen_Y_pct": "75% (>=24/32)",
            "sd_pool_prime": {m: round(sd_pool_prime[m], 6) for m in PRIMARY_METRICS},
            "mob_parity_total": MOB_PARITY_TOTAL,
            "seal_md5": seal_md5, "seal_path": os.path.basename(SEAL_PATH),
            "zero_writes_to_engine_repo": True,
        },
        "verdict": verdict,
        "gate_legs": {
            "leg1_showcase": {"metric": "median composite d (informative) over high-fit pairs",
                              "value": leg1_median, "threshold": f">= +{GATE_X}", "pass": leg1_pass,
                              "n_pairs": len(high_pairs)},
            "leg2_stress": {"metric": "median composite d (informative) over low-fit pairs",
                            "value": leg2_median, "threshold": f"<= -{GATE_X}", "pass": leg2_pass,
                            "n_pairs": len(low_pairs)},
            "leg3_direction": {"metric": "pairs sign-correct under SEALED renormalized rule",
                               "value": f"{n_sign_correct}/{leg3_total}",
                               "threshold": f">= {GATE_Y_MIN_CORRECT}/32", "pass": leg3_pass,
                               "sealed_sign_rule": sign_rule},
        },
        "degeneracy_determination": {
            "informative_metrics": informative, "n_informative": n_inf,
            "renormalized_sign_rule": sign_rule, "degeneracy": degeneracy,
            "degeneracy_fired": degeneracy_fired,
            "alpha_realized_for_direction_leg": alpha_realized,
            "alpha_note": ("§8.4 C5: alpha recomputed for the realized informative configuration; "
                           "the gate PARAMETER stays the >=24/32 count. The base-sheet 0.0035 is exact "
                           "only under all-pairs-3-informative."),
        },
        "decomposition": {
            "per_era_legs": per_era_legs,
            "per_family_mean_composite_d": per_family_mean_d,
            "per_metric_medians": per_metric_medians,
            "membership_tier_mix_of_scored_pairs": dict(tier_mix),
            "n_scored_pairs": len(scored), "n_red_flag_pairs": len(red_flag_pairs)},
        "composition_parity_checks": parity_checks,
        "selection_census": selection_census,
        "red_flags": {
            "red_flag_pairs": [{"era": p["era"], "side": p.get("side"), "kit_id": p["kit_id"],
                                "reason": p.get("red_flag")} for p in red_flag_pairs],
            "encounter_builder_red_flags": encounter_red_flags,
            "baseline_builder_red_flags": baseline_red_flags,
        },
        "smoke_nonpassive_check": {"targets": len(smoke_results), "results": smoke_results,
                                   "build_seconds": round(build_s, 1)},
        "per_pair_table": per_pair,
        "baseline_fight_records": baseline_records,
        "encounter_fight_records": encounter_recs,
        "n_baseline_fights": sum(len(b["fights"]) for b in baseline_records if not b.get("skipped")),
        "n_encounter_fights": sum(len(e["fights"]) for e in encounter_recs if not e.get("skipped")),
        "baseline_wall_seconds": round(base_wall, 1), "encounter_wall_seconds": round(enc_wall, 1),
        "prereg_caveat": ("MECHANICAL EXECUTION of the FROZEN amendment sheet (904f317c) + base sheet "
                          "(5ea56bf3). Zero design discretion; any pin the sheets do not decide is a "
                          "red-flag, not an improvised rule. The preregs ARE the math note (Discipline #1). "
                          "Mechanical resolutions M1-M3/S1/D1/G1/E1 in 2026-07-22-tier3-w3prime-gate-math.md."),
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    # ---- print ----
    print("=" * 84)
    print("TIER-3 W3' · T3-F4' GATE · MECHANICAL EXECUTION OF THE FROZEN AMENDMENT SHEET")
    print("=" * 84)
    print(f"substrate md5 open/close: {md5_open[:8]}/{md5_close[:8]}  stable={corpus_stable}")
    print(f"engine HEAD fire/close:   {engine_head_fire[:7]}/{engine_head_close[:7]}  "
          f"HEAD-invariant {'OK' if head_invariant_ok else 'VIOLATED'}")
    print(f"seeds {SEEDS} dmod={DAMAGE_MODIFIER}  X={GATE_X} Y>={GATE_Y_MIN_CORRECT}/32")
    print(f"PlayerClass builds: {len(pc_cache)} cells in {build_s:.1f}s  "
          f"baseline {base_wall:.1f}s / encounter {enc_wall:.1f}s")
    print(f"seal md5: {seal_md5}")
    print("-" * 84)
    print("COMPOSITION-PARITY (encounter multiset == matched-baseline multiset):")
    for fclass, pc_ in parity_checks.items():
        print(f"  {fclass:12s} parity={pc_['parity_ok']}  enc_tiers={pc_['encounter_tier_mix']}  "
              f"base_tiers={pc_['baseline_tier_mix']}  enc_hp={pc_['encounter_hp_multiset']}")
    print("-" * 84)
    print("DEGENERACY DETERMINATION (baseline cells only; SEALED):")
    for m in PRIMARY_METRICS:
        dg = degeneracy[m]
        print(f"  {m:20s} sd_pool'={dg['sd_pool_prime']:.4f}  at_bound={dg['cells_at_bound']}/{dg['n_cells']} "
              f"(bound={dg['bound']}, thr>={dg['at_bound_threshold']})  DEGEN={dg['degenerate']}")
    print(f"  informative={informative} (n={n_inf})  sign-rule: {sign_rule}")
    if degeneracy_fired:
        print(f"  §4 FIRED -> alpha_realized(direction leg) = {alpha_realized}")
    print("-" * 84)
    print("SELECTION CENSUS (families + courts per era):")
    for era in ERAS:
        sc_e = selection_census[era]
        print(f"  Era {era}: fams={sc_e['families_drafted']}")
        print(f"           courts={sc_e['courts_drafted']} (n={sc_e['n_courts']}, "
              f"check {'OK' if sc_e['courts_check_ok'] else 'FAIL'})  swaps={len(sc_e['swap_log'])}")
    print("-" * 84)
    print("GATE LEGS:")
    print(f"  LEG1 showcase (median composite d, {len(high_pairs)} high): {leg1_median}  >= +{GATE_X} ? {leg1_pass}")
    print(f"  LEG2 stress   (median composite d, {len(low_pairs)} low):  {leg2_median}  <= -{GATE_X} ? {leg2_pass}")
    print(f"  LEG3 direction: {n_sign_correct}/{leg3_total} sign-correct  >= {GATE_Y_MIN_CORRECT}/32 ? {leg3_pass}")
    print("-" * 84)
    print("PER-ERA (descriptive):")
    for era in ERAS:
        e = per_era_legs[era]
        print(f"  Era {era}: high_med={e['high_median_composite_d']}  low_med={e['low_median_composite_d']}  "
              f"sign_correct={e['n_sign_correct']}/{e['n_pairs']}")
    print("-" * 84)
    print(f"membership_tier mix (scored pairs): {dict(tier_mix)}")
    print(f"red-flag pairs: {len(red_flag_pairs)}  encounter_rf={list(encounter_red_flags)}  "
          f"baseline_rf={list(baseline_red_flags)}")
    for p in red_flag_pairs:
        print(f"    RED-FLAG {p['era']}/{p.get('side')} {p['kit_id']}: {p.get('red_flag')}")
    print(f"baseline fights: {out['n_baseline_fights']}  encounter fights: {out['n_encounter_fights']} "
          f"(expect 128 + 128 = 256)")
    print("=" * 84)
    print(f"VERDICT: {verdict}")
    print("=" * 84)
    print(f"wrote seal:   {SEAL_PATH}")
    print(f"wrote output: {OUT_PATH}")


if __name__ == "__main__":
    main()
