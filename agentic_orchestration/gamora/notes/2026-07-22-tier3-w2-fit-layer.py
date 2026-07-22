#!/usr/bin/env python3
"""
Tier-3 W2 — fit(kit, encounter | era) layer + compute census.

WAVE W2 of the Tier-3 Encounter-Geometry Run (conductor: gandalf RUN-CONDUCTOR).
Reads the W1 grammar spec AS MATH (§7 four reads) and computes the fit join over
the record-267 kit spine × the 4 per-era decks. Totality is the done-predicate.

Determinate join = §1 of the math note (no ruling). v0 SCORING = §2 of the math note,
flagged PROPOSAL — conductor ruling required (weights w_v=0.50, w_t=0.30, w_s=0.20).

Substrate: corpus.db md5 d091881d (READ-ONLY). Engine repo untouched.
Math note: 2026-07-22-tier3-w2-fit-layer-math.md (this dir).
Author: named-gamora sub-agent, 2026-07-22.

Run:  python3 2026-07-22-tier3-w2-fit-layer.py
Emits: 2026-07-22-tier3-w2-fit-output.json  +  prints a compute census.
"""
import hashlib
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_DB = os.path.abspath(os.path.join(
    HERE, "..", "..", "research", "curated", "corpus.db"))
EXPECTED_MD5_PREFIX = "d091881d"
OUT_PATH = os.path.join(HERE, "2026-07-22-tier3-w2-fit-output.json")

# ----- v0 scoring weights (PROPOSAL — conductor ruling required; math note §2) -----
W_VERB = 0.50
W_TOPO = 0.30
W_SHELF = 0.20

# ---------------------------------------------------------------------------
# W1 GRAMMAR-AS-DATA. Transcribed from the frozen W1 spec (grammar-spec.md §2.4
# decks, §3.3 formation catalogue + verb column) + derived-templates instance
# (L-10). Working labels throughout (charter §5 / T3-V2) — NOT canon.
# ---------------------------------------------------------------------------

# §2.4 — the 4 per-era MACRO decks: present_families + hole_families (hostile side).
# (source_game / signature per deck header; kin slot is era-exempt, handled separately.)
ERA_DECKS = {
    "I": {
        "era_year": 2000, "source_game": "d2", "signature_family": "MELEE-STRIKE",
        "present_families": ["WHIRLWIND", "AURA", "TOTEM-SENTRY", "TRAP-MINE",
                             "MELEE-STRIKE", "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY",
                             "CHAIN-BOUNCE", "SHAPESHIFT", "DASH-STRIKER"],
        "hole_families": ["CHANNELED-BEAM", "MINION-PET", "IDENTITY-GAUGE"],
        # archetype_id -> hostile_family_roster (§2.4 Deck I table)
        "archetypes": {
            "I-A": ["MELEE-STRIKE", "DOT-AILMENT"],
            "I-B": ["MELEE-STRIKE", "TRAP-MINE", "MULTI-PROJECTILE-VOLLEY"],
            "I-C": ["TOTEM-SENTRY", "MULTI-PROJECTILE-VOLLEY", "AURA"],
            "I-D": ["WHIRLWIND", "AURA", "TOTEM-SENTRY", "DOT-AILMENT"],
            "I-E": ["CHAIN-BOUNCE", "MELEE-STRIKE", "DOT-AILMENT", "TOTEM-SENTRY"],
        },
        "archetype_forms": {"I-A": "PATROL", "I-B": "NEST", "I-C": "CHANNEL-ARENA",
                            "I-D": "BRAWL", "I-E": "WAVE-ARENA"},
    },
    "II": {
        "era_year": 2013, "source_game": "poe1", "signature_family": "DOT-AILMENT",
        "present_families": ["CHANNELED-BEAM", "AURA", "TOTEM-SENTRY", "TRAP-MINE",
                             "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY", "CHAIN-BOUNCE",
                             "WHIRLWIND"],  # WHIRLWIND-II is RDR-derived, headline-capable
        "hole_families": ["MELEE-STRIKE", "SHAPESHIFT", "MINION-PET", "IDENTITY-GAUGE",
                          "DASH-STRIKER"],
        "archetypes": {
            "II-A": ["TOTEM-SENTRY", "MULTI-PROJECTILE-VOLLEY"],
            "II-B": ["TOTEM-SENTRY", "CHANNELED-BEAM"],
            "II-C": ["TRAP-MINE", "DOT-AILMENT"],
            "II-D": ["AURA", "MULTI-PROJECTILE-VOLLEY", "CHANNELED-BEAM"],
            "II-E": ["DOT-AILMENT", "CHAIN-BOUNCE"],
        },
        "archetype_forms": {"II-A": "OUTPOST", "II-B": "CHANNEL-ARENA", "II-C": "NEST",
                            "II-D": "OUTPOST", "II-E": "BRAWL"},
    },
    "III": {
        "era_year": 2016, "source_game": "gd", "signature_family": "CHANNELED-BEAM",
        "present_families": ["WHIRLWIND", "CHANNELED-BEAM", "TOTEM-SENTRY", "TRAP-MINE",
                             "MELEE-STRIKE", "DOT-AILMENT", "CHAIN-BOUNCE", "DASH-STRIKER",
                             "SHAPESHIFT"],  # SHAPESHIFT-III RDR-derived secondary
        "hole_families": ["AURA", "MULTI-PROJECTILE-VOLLEY", "MINION-PET", "IDENTITY-GAUGE"],
        "archetypes": {
            "III-A": ["MELEE-STRIKE", "CHANNELED-BEAM"],
            "III-B": ["CHANNELED-BEAM", "DOT-AILMENT"],
            "III-C": ["MELEE-STRIKE", "DASH-STRIKER"],
            "III-D": ["MELEE-STRIKE", "TRAP-MINE"],
            "III-E": ["DOT-AILMENT", "TOTEM-SENTRY", "TRAP-MINE", "CHAIN-BOUNCE"],
        },
        "archetype_forms": {"III-A": "PATROL", "III-B": "CHANNEL-ARENA", "III-C": "BRAWL",
                            "III-D": "PATROL", "III-E": "BRAWL"},
    },
    "IV": {
        "era_year": 2024, "source_game": "poe2+le", "signature_family": None,
        "present_families": ["WHIRLWIND", "CHANNELED-BEAM", "AURA", "TOTEM-SENTRY",
                             "TRAP-MINE", "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY",
                             "MELEE-STRIKE", "SHAPESHIFT", "CHAIN-BOUNCE"],
        "hole_families": ["MINION-PET", "IDENTITY-GAUGE"],
        "archetypes": {
            "IV-A": ["WHIRLWIND", "MELEE-STRIKE"],
            "IV-B": ["TRAP-MINE", "TOTEM-SENTRY"],
            "IV-C": ["TOTEM-SENTRY", "MULTI-PROJECTILE-VOLLEY"],
            "IV-D": ["CHANNELED-BEAM", "AURA", "DOT-AILMENT"],
            "IV-E": ["SHAPESHIFT", "MULTI-PROJECTILE-VOLLEY", "WHIRLWIND"],
            "IV-F": ["DOT-AILMENT"],  # + UNMAPPED U-7 (reserved, not a family)
        },
        "archetype_forms": {"IV-A": "PATROL", "IV-B": "NEST", "IV-C": "OUTPOST",
                            "IV-D": "CHANNEL-ARENA", "IV-E": "BRAWL", "IV-F": "PATROL"},
    },
}

# §3.3 — formation catalogue: family -> list of (formation_id, eras_present[], provenance).
# MEDIUM-confidence per §8 tracked in FORMATION_MEDIUM.
FORMATIONS = {
    "WHIRLWIND": [("ww_converge_spin", ["IV"], "GENRE-ATTESTED"),
                  ("ww_arc_sweep", ["I", "III"], "GENRE-ATTESTED"),
                  ("ww_derived_frenzy_line", ["II"], "RDR-NATIVE-DERIVED")],
    "CHANNELED-BEAM": [("cb_lane_hold", ["II", "III", "IV"], "GENRE-ATTESTED"),
                       ("cb_crossfire", ["IV"], "GENRE-ATTESTED")],
    "AURA": [("aura_carrier_pack", ["I", "II", "IV"], "GENRE-ATTESTED"),
             ("aura_matron_center", ["IV"], "GENRE-ATTESTED")],
    "TOTEM-SENTRY": [("ts_anchor_screen", ["I", "II", "III", "IV"], "GENRE-ATTESTED"),
                     ("ts_resurrection_loop", ["II", "IV"], "GENRE-ATTESTED"),
                     ("ts_environmental_nest", ["II", "IV"], "GENRE-ATTESTED")],
    "TRAP-MINE": [("tm_preseed_corridor", ["I", "II"], "GENRE-ATTESTED"),
                  ("tm_ritual_minefield", ["II", "III", "IV"], "GENRE-ATTESTED"),
                  ("tm_spawner_nest", ["I", "III"], "GENRE-ATTESTED")],
    "MELEE-STRIKE": [("ms_swarm_surround", ["I", "III", "IV"], "GENRE-ATTESTED"),
                     ("ms_wedge_advance", ["I", "III"], "GENRE-ATTESTED")],
    "DOT-AILMENT": [("da_field_retreat", ["I", "II", "III", "IV"], "GENRE-ATTESTED"),
                    ("da_curse_at_distance", ["I", "III"], "GENRE-ATTESTED")],
    "MULTI-PROJECTILE-VOLLEY": [("mpv_fan_from_position", ["I", "II", "IV"], "GENRE-ATTESTED"),
                                ("mpv_boss_sweep", ["IV"], "GENRE-ATTESTED")],
    "CHAIN-BOUNCE": [("cbn_corridor_arc", ["I", "II", "III"], "GENRE-ATTESTED"),
                     ("cbn_derived_arc_pass", ["IV"], "RDR-NATIVE-DERIVED")],
    "SHAPESHIFT": [("ss_phase_transform", ["IV"], "GENRE-ATTESTED"),
                   ("ss_derived_form_swap", ["I", "III"], "RDR-NATIVE-DERIVED")],
    "DASH-STRIKER": [("ds_flank_burst", ["III"], "GENRE-ATTESTED"),
                     ("ds_derived_gap_close", ["I"], "RDR-NATIVE-DERIVED")],
    # MINION-PET / IDENTITY-GAUGE: guest-family, catalogue-only this run (charter §1) — no formations dealt.
}

# §8 MEDIUM-confidence formation cells: (formation_id, era) tuples sourced from
# Age-II rows 17-18 or Age-IV LE rows.
FORMATION_MEDIUM = {
    ("tm_preseed_corridor", "II"),   # Hellion #17 Maxroll-only
    ("da_field_retreat", "II"),      # Chaos Zealot #18 Maxroll-only
    # All Age-IV LE-sourced formations → MEDIUM (1.0-era staleness). Applied at era==IV
    # for formations whose IV presence rests on LE rows (marked in IV_LE_FORMATIONS).
}
IV_LE_FORMATIONS = {"ww_converge_spin", "cb_crossfire", "aura_matron_center",
                    "ts_environmental_nest", "tm_ritual_minefield", "mpv_boss_sweep",
                    "ss_phase_transform", "da_field_retreat"}

# §3.3 verb column (R-b2): family -> canonical MICRO verb-class.
FAMILY_VERB = {
    "WHIRLWIND": "spin-and-close",
    "CHANNELED-BEAM": "channel-lanes",
    "AURA": "aura-enable",
    "TOTEM-SENTRY": "emplace-and-hold",
    "TRAP-MINE": "pre-seed",
    "MELEE-STRIKE": "swarm-the-brawl",
    "DOT-AILMENT": "stack-and-retreat",
    "MULTI-PROJECTILE-VOLLEY": "fan",
    "CHAIN-BOUNCE": "bounce-and-chain",
    "SHAPESHIFT": "form-transition",
    "DASH-STRIKER": "dash-and-strike",
    "MINION-PET": "minion-swarm",
    "IDENTITY-GAUGE": "gauge-threshold",
}

# The 5 RDR-NATIVE-DERIVED cells (L-10): (family, era) -> serving_role.
DERIVED_CELLS = {
    ("SHAPESHIFT", "I"): "secondary",
    ("SHAPESHIFT", "III"): "secondary",
    ("DASH-STRIKER", "I"): "texture_docket_input",
    ("CHAIN-BOUNCE", "IV"): "texture_docket_input",
    ("WHIRLWIND", "II"): "headline_capable",
}

ERA_OF_YEAR = {2000: "I", 2013: "II", 2016: "III", 2024: "IV"}

# ---------------------------------------------------------------------------
# v0 SCORING TABLES (PROPOSAL — conductor ruling required; math note §2.2)
# favor = 1.0, neutral = 0.5, penalize = 0.0; multiple axis-hits averaged.
# Each verb-class maps to (favor_predicates, penalize_predicates) over BC axes.
# A predicate is (axis, value). A kit scores favor if it hits any favor predicate,
# penalize if it hits any penalize predicate; both/neither -> neutral 0.5.
# ---------------------------------------------------------------------------
VERB_AFFINITY = {
    "stack-and-retreat": {
        "favor": [("range_val", "ranged"), ("range_val", "dual"), ("commit_val", "instant")],
        "penalize": [("range_val", "melee"), ("commit_val", "channel")]},
    "swarm-the-brawl": {
        "favor": [("proxy_val", "heavy"), ("proxy_val", "light"), ("amp_val", "var")],
        "penalize": [("proxy_val", "solo")]},
    "channel-lanes": {
        "favor": [("range_val", "melee"), ("range_val", "mid"), ("commit_val", "instant")],
        "penalize": [("commit_val", "channel")]},
    "fan": {
        "favor": [("range_val", "ranged"), ("proxy_val", "heavy")],
        "penalize": [("range_val", "melee")]},
    "spin-and-close": {
        "favor": [("range_val", "ranged"), ("range_val", "dual"), ("tempo_val", "high")],
        "penalize": [("range_val", "melee"), ("tempo_val", "low")]},
    "emplace-and-hold": {
        "favor": [("amp_val", "spiky"), ("range_val", "ranged")],
        "penalize": [("tempo_val", "low")]},
    "pre-seed": {
        "favor": [("tempo_val", "high"), ("proxy_val", "heavy")],
        "penalize": [("commit_val", "channel")]},
    "form-transition": {"favor": [], "penalize": []},  # neutral baseline 0.5
    "bounce-and-chain": {
        "favor": [("proxy_val", "solo"), ("range_val", "ranged")],
        "penalize": [("proxy_val", "heavy")]},
    "aura-enable": {
        "favor": [("amp_val", "spiky")],
        "penalize": [("amp_val", "flat")]},
    "dash-and-strike": {
        "favor": [("range_val", "melee"), ("tempo_val", "high")],
        "penalize": [("range_val", "ranged")]},
    "minion-swarm": {"favor": [], "penalize": []},
    "gauge-threshold": {"favor": [], "penalize": []},
}

# topology_affinity: formation_id -> (favor, penalize) over BC axes (math note §2.2 term 2).
TOPO_CLASS = {
    # corridor / lane
    "cbn_corridor_arc": "corridor", "cb_lane_hold": "corridor", "cb_crossfire": "corridor",
    "tm_preseed_corridor": "corridor",
    # converge / swarm
    "ww_converge_spin": "converge", "ww_arc_sweep": "converge", "ww_derived_frenzy_line": "converge",
    "ms_swarm_surround": "converge", "ms_wedge_advance": "converge",
    # emplaced / anchor
    "ts_anchor_screen": "anchor", "ts_resurrection_loop": "anchor", "aura_matron_center": "anchor",
    "aura_carrier_pack": "anchor", "mpv_fan_from_position": "anchor", "mpv_boss_sweep": "anchor",
    # field / nest
    "da_field_retreat": "field", "da_curse_at_distance": "field", "tm_ritual_minefield": "field",
    "tm_spawner_nest": "field", "ts_environmental_nest": "field", "cbn_derived_arc_pass": "field",
    # transform (neutral)
    "ss_phase_transform": "transform", "ss_derived_form_swap": "transform",
    "ds_flank_burst": "flank", "ds_derived_gap_close": "flank",
}
TOPO_AFFINITY = {
    "corridor": {"favor": [("range_val", "ranged")], "penalize": [("range_val", "melee")]},
    "converge": {"favor": [("amp_val", "var"), ("proxy_val", "heavy")],
                 "penalize": [("range_val", "ranged")]},  # ranged single-target funneled into the spin
    "anchor": {"favor": [("range_val", "ranged"), ("amp_val", "spiky")],
               "penalize": [("range_val", "melee")]},
    "field": {"favor": [("tempo_val", "high"), ("range_val", "ranged")],
              "penalize": [("commit_val", "channel")]},
    "transform": {"favor": [], "penalize": []},
    "flank": {"favor": [("range_val", "melee"), ("tempo_val", "high")],
              "penalize": [("range_val", "ranged")]},
}


def _affinity(kit, table_entry):
    """favor/neutral/penalize -> [0,1]. Averages over hits; 0.5 if neither/both fire."""
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


def md5_check(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_kits():
    """Read-only load of the record-267 spine + family membership (gateA RATIFIED)."""
    con = sqlite3.connect(f"file:{CORPUS_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # gateA family membership (RATIFIED tier) — the ONLY resolvable membership in this db.
    fam = {}
    for row in cur.execute('SELECT kit_id, "group" AS grp FROM atlas_gateA_labels_2026_07_14'):
        fam[row["kit_id"]] = row["grp"]
    # gx secondary signal (documented, NOT used as membership) — for the coverage report.
    gxmap = {}
    for row in cur.execute(
            "SELECT kit_id, gx FROM canon_corpus WHERE corpus_class='record' AND gx IS NOT NULL AND gx<>''"):
        gxmap[row["kit_id"]] = row["gx"]
    kits = []
    for row in cur.execute(
            "SELECT kit_id, folk_name, game, era_year, range_val, court, original_element, "
            "proxy_val, commit_val, tempo_val, amp_val "
            "FROM canon_corpus WHERE corpus_class='record' ORDER BY kit_id"):
        k = dict(row)
        k["family_gateA"] = fam.get(k["kit_id"])
        k["gx"] = gxmap.get(k["kit_id"])
        kits.append(k)
    con.close()
    return kits


def formations_for(family, era):
    out = []
    for (fid, eras, prov) in FORMATIONS.get(family, []):
        if era in eras:
            medium = ((fid, era) in FORMATION_MEDIUM) or (era == "IV" and fid in IV_LE_FORMATIONS)
            out.append({"formation_id": fid, "provenance": prov,
                        "confidence": "MEDIUM" if medium else "HIGH"})
    return out


def compute_fit(kit, era):
    """The determinate join (math note §1.4) + v0 scoring (§2, PROPOSAL)."""
    deck = ERA_DECKS[era]
    family = kit["family_gateA"]
    kit_era = ERA_OF_YEAR.get(kit["era_year"])

    # --- determinate join ---
    shelf_match = "native" if kit_era == era else "off-shelf"
    if family is None:
        family_present = "unresolved"
    elif family in deck["present_families"]:
        family_present = "present"
    else:
        family_present = "hole"

    forms = formations_for(family, era) if family else []
    verb_class = FAMILY_VERB.get(family) if family else None
    derived_role = DERIVED_CELLS.get((family, era)) if family else None

    # confidence carry: MEDIUM if any sourced formation is MEDIUM
    row_conf = "MEDIUM" if any(f["confidence"] == "MEDIUM" for f in forms) else "HIGH"

    # --- v0 scoring (PROPOSAL) ---
    # shelf_affinity (determinate term)
    if shelf_match == "native":
        shelf_aff = 1.0
    elif family_present == "hole":
        shelf_aff = 0.0
    else:  # off-shelf but present, or unresolved
        shelf_aff = 0.5

    if family is None:
        # UNRESOLVED family -> era-only neutral verb/topology (determinate degradation)
        verb_aff, verb_reason = 0.5, "era_only_unresolved_family"
        topo_aff, topo_reason, topo_formation = 0.5, "era_only_unresolved_family", None
        scoring_basis = "era_only_unresolved_family"
    else:
        verb_aff, verb_reason = _affinity(kit, VERB_AFFINITY.get(verb_class, {}))
        # topology: score against the BEST-fitting dealable formation for this family/era
        # (argmax over the family's era formations — the kit's most-favorable topology).
        if forms:
            best = None
            for f in forms:
                tclass = TOPO_CLASS.get(f["formation_id"], "transform")
                aff, reason = _affinity(kit, TOPO_AFFINITY.get(tclass, {}))
                if best is None or aff > best[0]:
                    best = (aff, reason, f["formation_id"])
            topo_aff, topo_reason, topo_formation = best
        else:
            topo_aff, topo_reason, topo_formation = 0.5, "no_formation_dealt", None
        scoring_basis = "full"

    fit_score = round(W_VERB * verb_aff + W_TOPO * topo_aff + W_SHELF * shelf_aff, 4)

    return {
        "era": era,
        "deck_source_game": deck["source_game"],
        # determinate join
        "family": family if family else "UNRESOLVED",
        "family_resolution": "gateA_RATIFIED" if family else "UNRESOLVED",
        "kit_era_shelf": kit_era,
        "shelf_match": shelf_match,
        "family_present": family_present,
        "micro_verb_class": verb_class,
        "meso_formations": forms,
        "derived_cell_role": derived_role,
        "confidence": row_conf,
        # v0 scoring (PROPOSAL)
        "scoring_basis": scoring_basis,
        "verb_affinity": round(verb_aff, 4), "verb_affinity_reason": verb_reason,
        "topology_affinity": round(topo_aff, 4), "topology_affinity_reason": topo_reason,
        "topology_best_formation": topo_formation,
        "shelf_affinity": round(shelf_aff, 4),
        "fit_score": fit_score,
    }


def main():
    if not os.path.exists(CORPUS_DB):
        print(f"FATAL: corpus.db not found at {CORPUS_DB}", file=sys.stderr)
        sys.exit(2)
    md5 = md5_check(CORPUS_DB)
    if not md5.startswith(EXPECTED_MD5_PREFIX):
        print(f"FATAL: corpus.db md5 {md5} != expected {EXPECTED_MD5_PREFIX}...",
              file=sys.stderr)
        sys.exit(2)

    kits = load_kits()
    n_kits = len(kits)

    # ---- compute the full join: 267 kits x 4 decks ----
    fit_records = []
    errors = []
    per_kit = {}
    for kit in kits:
        kit_fits = {}
        for era in ("I", "II", "III", "IV"):
            try:
                kit_fits[era] = compute_fit(kit, era)
            except Exception as e:  # totality guard: no fit may throw
                errors.append({"kit_id": kit["kit_id"], "era": era, "error": repr(e)})
        per_kit[kit["kit_id"]] = kit_fits
        for era, rec in kit_fits.items():
            fit_records.append(dict(kit_id=kit["kit_id"], **rec))

    n_expected = n_kits * 4
    n_computed = len(fit_records)

    # ---- census ----
    resolved = sum(1 for k in kits if k["family_gateA"])
    unresolved = n_kits - resolved
    fam_counts = Counter(k["family_gateA"] for k in kits if k["family_gateA"])
    shelf_counts = Counter(ERA_OF_YEAR.get(k["era_year"]) for k in kits)
    present_dist = Counter(r["family_present"] for r in fit_records)
    conf_dist = Counter(r["confidence"] for r in fit_records)
    basis_dist = Counter(r["scoring_basis"] for r in fit_records)
    score_min = min(r["fit_score"] for r in fit_records)
    score_max = max(r["fit_score"] for r in fit_records)
    score_mean = round(sum(r["fit_score"] for r in fit_records) / n_computed, 4)

    census = {
        "n_kits": n_kits,
        "n_era_decks": 4,
        "n_join_rows_expected": n_expected,
        "n_join_rows_computed": n_computed,
        "error_count": len(errors),
        "errors": errors,
        "totality_predicate_met": (n_computed == n_expected and len(errors) == 0),
        "family_resolution": {
            "resolvable_via": "atlas_gateA_labels_2026_07_14 (RATIFIED tier)",
            "records_resolved": resolved,
            "records_unresolved": unresolved,
            "families_covered": sorted(fam_counts.keys()),
            "families_covered_count": len(fam_counts),
            "families_uncovered": sorted(set(FAMILY_VERB) - set(fam_counts) - {"MINION-PET"}
                                         | ({"MINION-PET"} if "MINION-PET" not in fam_counts else set())),
            "per_family_record_counts": dict(fam_counts),
            "tau_propagated_docket_tiers_present": False,
            "gap_note": ("charter cites gateA RATIFIED 86 + tau-PROPAGATED 44 + DOCKET-5 + "
                         "fresh-draft; ONLY the RATIFIED gateA table is materialized in md5 "
                         "d091881d. 7 of 13 families have no membership; 221/267 records "
                         "UNRESOLVED. Fit degrades UNRESOLVED kits to era-level cleanly (no "
                         "fabrication) and computes over all 267."),
        },
        "era_shelf_counts": dict(shelf_counts),
        "era_anomaly": {"kit_id": "poe1-kinetic-fusillade",
                        "note": "game=poe1 but era_year=2024 -> shelves to IV (shelf key is era_year)"},
        "family_present_distribution": dict(present_dist),
        "confidence_distribution": dict(conf_dist),
        "scoring_basis_distribution": dict(basis_dist),
        "fit_score_summary": {"min": score_min, "max": score_max, "mean": score_mean},
        "scoring_status": {
            "determinate_join": "TOTAL (math note §1) — no ruling needed",
            "scoring_formula": "PROPOSAL — conductor ruling required (math note §2)",
            "proposed_weights": {"w_verb": W_VERB, "w_topology": W_TOPO, "w_shelf": W_SHELF},
        },
    }

    out = {
        "artifact": "tier3-w2-fit-output",
        "run": "Tier-3 Encounter-Geometry Run · Wave W2",
        "author": "named-gamora sub-agent",
        "date": "2026-07-22",
        "substrate_md5": md5,
        "engine_head_at_author": "a57ee1f",
        "working_label_caveat": ("all family values are WORKING LABELS, not canon "
                                 "(charter §5 / T3-V2); rename is value-swap-safe"),
        "scoring_caveat": ("fit_score uses v0 PROPOSAL weights (w_v=0.50/w_t=0.30/w_s=0.20); "
                           "the determinate JOIN (family/shelf/formations/verbs) needs no "
                           "ruling — ONLY the scalar scoring does. conductor ruling required "
                           "before W3 consumes the ordering."),
        "census": census,
        "fit_records": fit_records,
    }

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    # ---- print census ----
    print("=" * 72)
    print("TIER-3 W2 FIT-LAYER COMPUTE CENSUS")
    print("=" * 72)
    print(f"substrate md5:            {md5} (expected {EXPECTED_MD5_PREFIX}...)  "
          f"{'OK' if md5.startswith(EXPECTED_MD5_PREFIX) else 'MISMATCH'}")
    print(f"kits (record-267 spine):  {n_kits}")
    print(f"era decks:                4 (I/II/III/IV)")
    print(f"join rows expected:       {n_expected}")
    print(f"join rows computed:       {n_computed}")
    print(f"errors:                   {len(errors)}")
    print(f"TOTALITY PREDICATE MET:   {census['totality_predicate_met']}")
    print("-" * 72)
    print(f"family resolved (gateA):  {resolved}/{n_kits}   unresolved: {unresolved}")
    print(f"families covered ({len(fam_counts)}/13): {dict(fam_counts)}")
    print(f"tau-PROPAGATED/DOCKET tiers present in db: "
          f"{census['family_resolution']['tau_propagated_docket_tiers_present']}")
    print(f"era shelf counts:         {dict(shelf_counts)}")
    print(f"family_present dist:      {dict(present_dist)}")
    print(f"confidence dist:          {dict(conf_dist)}")
    print(f"scoring_basis dist:       {dict(basis_dist)}")
    print(f"fit_score [min,mean,max]: [{score_min}, {score_mean}, {score_max}]")
    print("-" * 72)
    print("SCORING STATUS: determinate join = TOTAL (no ruling); "
          "scalar scoring = PROPOSAL (ruling required)")
    print(f"proposed weights: w_verb={W_VERB} w_topology={W_TOPO} w_shelf={W_SHELF}")
    print("=" * 72)
    print(f"wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
