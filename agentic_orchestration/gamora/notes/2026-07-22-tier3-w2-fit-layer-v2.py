#!/usr/bin/env python3
"""
Tier-3 PREREG-beat — PART 1: fit(kit, encounter | era) RE-JOIN on the membership sidecar.

Re-runs the W2 fit layer (2026-07-22-tier3-w2-fit-layer.py) but sources family
resolution from elrond's materialized membership sidecar (ALL tiers) instead of the
gateA-only table. Consumes ACTIVE rows only (falsy `shadowed_by`), `on_spine` for the
record-267 spine. Adds `membership_tier` per fit row (ruling L-13(c)). Emits v2 output
+ a census DELTA vs v1. Does NOT modify the v1 output file (audit trail).

RULINGS THAT BIND (do NOT change):
  - v0 scoring 0.50*verb + 0.30*topology + 0.20*shelf ADOPTED AS PREREG CANDIDATE (L-13(a)).
  - re-join adds membership_tier per fit row (L-13(c)).
  - resolution fallback stays family -> kit-level -> era (unchanged from v1).

Substrate: corpus.db md5 d091881d (READ-ONLY) + sidecar (READ-ONLY, commit 6dd43161).
Engine repo untouched.
Author: named-gamora sub-agent, 2026-07-22.

Run:  python3 2026-07-22-tier3-w2-fit-layer-v2.py
Emits: 2026-07-22-tier3-w2-fit-output-v2.json + prints a compute+delta census.
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
SIDECAR = os.path.join(HERE, "..", "..", "elrond", "notes",
                       "2026-07-22-tier3-family-membership-sidecar.json")
V1_OUT = os.path.join(HERE, "2026-07-22-tier3-w2-fit-output.json")
EXPECTED_MD5_PREFIX = "d091881d"
SIDECAR_COMMIT = "6dd43161"
OUT_PATH = os.path.join(HERE, "2026-07-22-tier3-w2-fit-output-v2.json")

# ----- v0 scoring weights (L-13(a) ADOPTED AS PREREG CANDIDATE — frozen, do NOT change) -----
W_VERB = 0.50
W_TOPO = 0.30
W_SHELF = 0.20

# ---------------------------------------------------------------------------
# W1 GRAMMAR-AS-DATA — transcribed verbatim from the frozen v1 fit script
# (2026-07-22-tier3-w2-fit-layer.py). Working labels throughout (charter §5 / T3-V2).
# ---------------------------------------------------------------------------
ERA_DECKS = {
    "I": {
        "era_year": 2000, "source_game": "d2", "signature_family": "MELEE-STRIKE",
        "present_families": ["WHIRLWIND", "AURA", "TOTEM-SENTRY", "TRAP-MINE",
                             "MELEE-STRIKE", "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY",
                             "CHAIN-BOUNCE", "SHAPESHIFT", "DASH-STRIKER"],
        "hole_families": ["CHANNELED-BEAM", "MINION-PET", "IDENTITY-GAUGE"],
    },
    "II": {
        "era_year": 2013, "source_game": "poe1", "signature_family": "DOT-AILMENT",
        "present_families": ["CHANNELED-BEAM", "AURA", "TOTEM-SENTRY", "TRAP-MINE",
                             "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY", "CHAIN-BOUNCE",
                             "WHIRLWIND"],
        "hole_families": ["MELEE-STRIKE", "SHAPESHIFT", "MINION-PET", "IDENTITY-GAUGE",
                          "DASH-STRIKER"],
    },
    "III": {
        "era_year": 2016, "source_game": "gd", "signature_family": "CHANNELED-BEAM",
        "present_families": ["WHIRLWIND", "CHANNELED-BEAM", "TOTEM-SENTRY", "TRAP-MINE",
                             "MELEE-STRIKE", "DOT-AILMENT", "CHAIN-BOUNCE", "DASH-STRIKER",
                             "SHAPESHIFT"],
        "hole_families": ["AURA", "MULTI-PROJECTILE-VOLLEY", "MINION-PET", "IDENTITY-GAUGE"],
    },
    "IV": {
        "era_year": 2024, "source_game": "poe2+le", "signature_family": None,
        "present_families": ["WHIRLWIND", "CHANNELED-BEAM", "AURA", "TOTEM-SENTRY",
                             "TRAP-MINE", "DOT-AILMENT", "MULTI-PROJECTILE-VOLLEY",
                             "MELEE-STRIKE", "SHAPESHIFT", "CHAIN-BOUNCE"],
        "hole_families": ["MINION-PET", "IDENTITY-GAUGE"],
    },
}

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
}

FORMATION_MEDIUM = {
    ("tm_preseed_corridor", "II"),
    ("da_field_retreat", "II"),
}
IV_LE_FORMATIONS = {"ww_converge_spin", "cb_crossfire", "aura_matron_center",
                    "ts_environmental_nest", "tm_ritual_minefield", "mpv_boss_sweep",
                    "ss_phase_transform", "da_field_retreat"}

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

DERIVED_CELLS = {
    ("SHAPESHIFT", "I"): "secondary",
    ("SHAPESHIFT", "III"): "secondary",
    ("DASH-STRIKER", "I"): "texture_docket_input",
    ("CHAIN-BOUNCE", "IV"): "texture_docket_input",
    ("WHIRLWIND", "II"): "headline_capable",
}

ERA_OF_YEAR = {2000: "I", 2013: "II", 2016: "III", 2024: "IV"}

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
    "form-transition": {"favor": [], "penalize": []},
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
    "converge": {"favor": [("amp_val", "var"), ("proxy_val", "heavy")],
                 "penalize": [("range_val", "ranged")]},
    "anchor": {"favor": [("range_val", "ranged"), ("amp_val", "spiky")],
               "penalize": [("range_val", "melee")]},
    "field": {"favor": [("tempo_val", "high"), ("range_val", "ranged")],
              "penalize": [("commit_val", "channel")]},
    "transform": {"favor": [], "penalize": []},
    "flank": {"favor": [("range_val", "melee"), ("tempo_val", "high")],
              "penalize": [("range_val", "ranged")]},
}


def _affinity(kit, table_entry):
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


def load_sidecar_membership():
    """ACTIVE rows only (falsy shadowed_by); return {kit_id: (family, tier)}.
    on_spine filtering applied by the caller against the record-267 spine (all
    active-spine rows here are on_spine=True; we key on kit_id and resolve for the
    267 records, so off-spine actives simply never match a record kit_id)."""
    with open(SIDECAR) as f:
        sc = json.load(f)
    # md5 tripwire: the sidecar declares the corpus md5 it was built against.
    declared = sc.get("corpus_md5_ro", "")
    active = {}
    tier_of = {}
    for row in sc["memberships"]:
        if row.get("shadowed_by"):          # non-active (shadowed) — skip
            continue
        active[row["kit_id"]] = row["family"]
        tier_of[row["kit_id"]] = row["tier"]
    return active, tier_of, declared, sc.get("counts", {})


def load_kits(sidecar_family, sidecar_tier):
    """Read-only load of the record-267 spine; family resolved from the sidecar
    (active rows), tier carried per L-13(c). Fallback: family -> (kit-level -> era)."""
    con = sqlite3.connect(f"file:{CORPUS_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # gateA (v1 source) — retained ONLY to compute the newly-resolved delta.
    gateA = {}
    for row in cur.execute('SELECT kit_id, "group" AS grp FROM atlas_gateA_labels_2026_07_14'):
        gateA[row["kit_id"]] = row["grp"]
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
        # RESOLUTION: sidecar active row for this kit_id (family->kit-level); else era-only.
        k["family_sidecar"] = sidecar_family.get(k["kit_id"])
        k["membership_tier"] = sidecar_tier.get(k["kit_id"])  # None if unresolved
        k["family_gateA_v1"] = gateA.get(k["kit_id"])         # for delta only
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
    """Determinate join + v0 scoring (weights FROZEN L-13(a)). Family from sidecar."""
    deck = ERA_DECKS[era]
    family = kit["family_sidecar"]
    tier = kit["membership_tier"]
    kit_era = ERA_OF_YEAR.get(kit["era_year"])

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
    row_conf = "MEDIUM" if any(f["confidence"] == "MEDIUM" for f in forms) else "HIGH"

    if shelf_match == "native":
        shelf_aff = 1.0
    elif family_present == "hole":
        shelf_aff = 0.0
    else:
        shelf_aff = 0.5

    if family is None:
        verb_aff, verb_reason = 0.5, "era_only_unresolved_family"
        topo_aff, topo_reason, topo_formation = 0.5, "era_only_unresolved_family", None
        scoring_basis = "era_only_unresolved_family"
    else:
        verb_aff, verb_reason = _affinity(kit, VERB_AFFINITY.get(verb_class, {}))
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
        "family": family if family else "UNRESOLVED",
        # L-13(c): membership_tier per fit row (None -> "UNRESOLVED" surface label)
        "membership_tier": tier if tier else "UNRESOLVED",
        "family_resolution": ("sidecar_" + tier) if family else "UNRESOLVED",
        "kit_era_shelf": kit_era,
        "shelf_match": shelf_match,
        "family_present": family_present,
        "micro_verb_class": verb_class,
        "meso_formations": forms,
        "derived_cell_role": derived_role,
        "confidence": row_conf,
        "scoring_basis": scoring_basis,
        "verb_affinity": round(verb_aff, 4), "verb_affinity_reason": verb_reason,
        "topology_affinity": round(topo_aff, 4), "topology_affinity_reason": topo_reason,
        "topology_best_formation": topo_formation,
        "shelf_affinity": round(shelf_aff, 4),
        "fit_score": fit_score,
    }


def load_v1_scores():
    """Load v1 fit_records keyed (kit_id, era) -> fit_score, for the delta spread."""
    with open(V1_OUT) as f:
        v1 = json.load(f)
    out = {}
    for r in v1["fit_records"]:
        out[(r["kit_id"], r["era"])] = r["fit_score"]
    return out, v1["census"]


def _spread(vals):
    if not vals:
        return {"n": 0}
    vals = sorted(vals)
    n = len(vals)
    mean = sum(vals) / n
    var = sum((x - mean) ** 2 for x in vals) / n
    return {"n": n, "min": round(vals[0], 4), "max": round(vals[-1], 4),
            "mean": round(mean, 4), "stdev": round(var ** 0.5, 4)}


def main():
    if not os.path.exists(CORPUS_DB):
        print(f"FATAL: corpus.db not found at {CORPUS_DB}", file=sys.stderr)
        sys.exit(2)
    md5 = md5_check(CORPUS_DB)
    if not md5.startswith(EXPECTED_MD5_PREFIX):
        print(f"FATAL: corpus.db md5 {md5} != expected {EXPECTED_MD5_PREFIX}...", file=sys.stderr)
        sys.exit(2)

    sidecar_family, sidecar_tier, sidecar_md5, sidecar_counts = load_sidecar_membership()
    if not md5.startswith(sidecar_md5[:8]):
        print(f"WARN: sidecar declares corpus md5 {sidecar_md5[:8]} != live {md5[:8]}", file=sys.stderr)

    kits = load_kits(sidecar_family, sidecar_tier)
    n_kits = len(kits)

    fit_records = []
    errors = []
    for kit in kits:
        for era in ("I", "II", "III", "IV"):
            try:
                rec = compute_fit(kit, era)
                fit_records.append(dict(kit_id=kit["kit_id"], **rec))
            except Exception as e:
                errors.append({"kit_id": kit["kit_id"], "era": era, "error": repr(e)})

    n_expected = n_kits * 4
    n_computed = len(fit_records)

    # ---- v2 census ----
    resolved_kits = [k for k in kits if k["family_sidecar"]]
    n_resolved = len(resolved_kits)
    n_unresolved = n_kits - n_resolved
    fam_counts = Counter(k["family_sidecar"] for k in resolved_kits)
    tier_counts = Counter(k["membership_tier"] for k in resolved_kits)
    present_dist = Counter(r["family_present"] for r in fit_records)
    conf_dist = Counter(r["confidence"] for r in fit_records)
    basis_dist = Counter(r["scoring_basis"] for r in fit_records)

    # ---- DELTA vs v1 ----
    v1_scores, v1_census = load_v1_scores()
    v1_basis = v1_census["scoring_basis_distribution"]

    # newly-resolved kits = sidecar-resolved AND NOT v1-gateA-resolved
    newly_resolved = [k for k in kits if k["family_sidecar"] and not k["family_gateA_v1"]]
    newly_ids = set(k["kit_id"] for k in newly_resolved)

    # fit_score spread for the 85 newly-resolved kits: v1 (era_only) vs v2 (full)
    v1_newly_scores = [v1_scores[(k["kit_id"], e)] for k in newly_resolved
                       for e in ("I", "II", "III", "IV") if (k["kit_id"], e) in v1_scores]
    v2_newly_scores = [r["fit_score"] for r in fit_records if r["kit_id"] in newly_ids]

    # per-era resolution mix (v2): how many kits resolve full vs era_only per era
    per_era_mix = {}
    for era in ("I", "II", "III", "IV"):
        era_rows = [r for r in fit_records if r["era"] == era]
        per_era_mix[era] = {
            "full": sum(1 for r in era_rows if r["scoring_basis"] == "full"),
            "era_only": sum(1 for r in era_rows if r["scoring_basis"] == "era_only_unresolved_family"),
            "present": sum(1 for r in era_rows if r["family_present"] == "present"),
            "hole": sum(1 for r in era_rows if r["family_present"] == "hole"),
            "unresolved": sum(1 for r in era_rows if r["family_present"] == "unresolved"),
        }

    # per-family spine counts (active resolution), + tier breakdown per family
    per_family_tier = defaultdict(Counter)
    for k in resolved_kits:
        per_family_tier[k["family_sidecar"]][k["membership_tier"]] += 1

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
            "resolvable_via": "membership sidecar (ACTIVE rows, all tiers; commit " + SIDECAR_COMMIT + ")",
            "resolution_fallback": "family -> kit-level -> era (L-13; unchanged from v1)",
            "records_resolved": n_resolved,
            "records_unresolved": n_unresolved,
            "families_covered": sorted(fam_counts.keys()),
            "families_covered_count": len(fam_counts),
            "per_family_record_counts": dict(fam_counts),
            "per_family_tier_breakdown": {f: dict(c) for f, c in per_family_tier.items()},
            "membership_tier_counts": dict(tier_counts),
            "all_tiers_materialized": True,
            "sidecar_declared_counts": sidecar_counts,
        },
        "family_present_distribution": dict(present_dist),
        "confidence_distribution": dict(conf_dist),
        "scoring_basis_distribution": dict(basis_dist),
        "fit_score_summary": {"min": score_min, "max": score_max, "mean": score_mean},
        "DELTA_vs_v1": {
            "v1_source": "atlas_gateA_labels_2026_07_14 (RATIFIED-only)",
            "v2_source": "membership sidecar (all tiers, active rows)",
            "resolved_kits_v1": sum(1 for k in kits if k["family_gateA_v1"]),
            "resolved_kits_v2": n_resolved,
            "newly_resolved_kits": len(newly_resolved),
            "scoring_basis_before": v1_basis,
            "scoring_basis_after": dict(basis_dist),
            "per_era_resolution_mix_v2": per_era_mix,
            "newly_resolved_fit_score_spread_v1_era_only": _spread(v1_newly_scores),
            "newly_resolved_fit_score_spread_v2_full": _spread(v2_newly_scores),
            "per_family_spine_counts_v2": dict(fam_counts),
        },
        "scoring_status": {
            "scoring_formula": "ADOPTED AS PREREG CANDIDATE (L-13(a)) — weights FROZEN",
            "weights": {"w_verb": W_VERB, "w_topology": W_TOPO, "w_shelf": W_SHELF},
        },
    }

    out = {
        "artifact": "tier3-w2-fit-output-v2",
        "run": "Tier-3 Encounter-Geometry Run · PREREG-beat · Part 1 RE-JOIN",
        "author": "named-gamora sub-agent",
        "date": "2026-07-22",
        "substrate_md5": md5,
        "sidecar_provenance": {
            "path": "agentic_orchestration/elrond/notes/2026-07-22-tier3-family-membership-sidecar.json",
            "commit": SIDECAR_COMMIT,
            "declared_corpus_md5": sidecar_md5,
            "ruling": "L-13(b) materialization; consumed per L-13(c) (membership_tier per fit row)",
            "consumption": "ACTIVE rows only (falsy shadowed_by); on_spine resolves the record-267 spine",
        },
        "engine_head_at_author": "b34a14b",
        "working_label_caveat": ("all family values are WORKING LABELS, not canon "
                                 "(charter §5 / T3-V2); rename is value-swap-safe"),
        "scoring_caveat": ("fit_score uses the L-13(a) ADOPTED prereg-candidate weights "
                           "(w_v=0.50/w_t=0.30/w_s=0.20); weights FROZEN, not re-derived here. "
                           "The v1 output file is preserved unmodified for the audit trail."),
        "census": census,
        "fit_records": fit_records,
    }

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    # ---- print census + delta ----
    print("=" * 74)
    print("TIER-3 PREREG-BEAT · PART 1 · FIT RE-JOIN (sidecar) — CENSUS + DELTA")
    print("=" * 74)
    print(f"substrate md5:            {md5[:8]}  (expected {EXPECTED_MD5_PREFIX})  "
          f"{'OK' if md5.startswith(EXPECTED_MD5_PREFIX) else 'MISMATCH'}")
    print(f"sidecar commit:           {SIDECAR_COMMIT}  (declared corpus md5 {sidecar_md5[:8]})")
    print(f"kits (record-267 spine):  {n_kits}")
    print(f"join rows computed:       {n_computed}/{n_expected}   errors: {len(errors)}")
    print(f"TOTALITY PREDICATE MET:   {census['totality_predicate_met']}")
    print("-" * 74)
    print(f"family resolved (sidecar):{n_resolved}/{n_kits}   unresolved: {n_unresolved}")
    print(f"  v1 (gateA) resolved:    {census['DELTA_vs_v1']['resolved_kits_v1']}")
    print(f"  NEWLY resolved:         {len(newly_resolved)}")
    print(f"families covered ({len(fam_counts)}):    {dict(fam_counts)}")
    print(f"membership_tier counts:   {dict(tier_counts)}")
    print("-" * 74)
    print("SCORING_BASIS DELTA:")
    print(f"  before (v1):            {v1_basis}")
    print(f"  after  (v2):            {dict(basis_dist)}")
    print("-" * 74)
    print("PER-ERA RESOLUTION MIX (v2):")
    for era in ("I", "II", "III", "IV"):
        m = per_era_mix[era]
        print(f"  {era:3s}  full={m['full']:3d}  era_only={m['era_only']:3d}  "
              f"present={m['present']:3d}  hole={m['hole']:3d}  unresolved={m['unresolved']:3d}")
    print("-" * 74)
    print("85 NEWLY-RESOLVED KITS — fit_score spread (v1 era_only -> v2 full):")
    print(f"  v1 (era_only): {census['DELTA_vs_v1']['newly_resolved_fit_score_spread_v1_era_only']}")
    print(f"  v2 (full):     {census['DELTA_vs_v1']['newly_resolved_fit_score_spread_v2_full']}")
    print("-" * 74)
    print(f"fit_score [min,mean,max]: [{score_min}, {score_mean}, {score_max}]")
    print("=" * 74)
    print(f"wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
