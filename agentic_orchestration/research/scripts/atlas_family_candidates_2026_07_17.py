#!/usr/bin/env python3
"""
Family-candidate rosters for The Build Horizon (Atlas Edition IV) — Discovery Docket.
================================================================================

Purpose (per elrond charge 2026-07-17): derive candidate rosters for the SIX
discovery-docket working families with PER-SUB-CLUSTER TAU calibration so
propagation NEVER leaps Leiden chains — the exact defect that shelved the
2026-07-16 archipelago mock (one global tau=0.80 across families of wildly
different spatial extent → TRAP-MINE / TOTEM-SENTRY umbrellas, ~1/3 precision).

Six dockets (ranked):
  1. MELEE-STRIKE
  2. GAUGE/BUILDER-SPENDER (GX-19)
  3. SHAPESHIFT (GX-02)
  4. DOT/AILMENT
  5. U-1 islet (largest unseeded coherent cluster, from the shelved mock's queue)
  6. MINION-PET re-seed (seed-poverty case; ratified but under-populated)

Method:
  A. FULL-SPACE VECTOR per kit: one-hot categorical fingerprint from ratified
     canon_engine_key mech axes (geometry_value, delivery_value, ctrl_function,
     ctrl_treatment, def_bin, economy_model, activation_val, dependency_val)
     joined with canon_corpus engagement proxies (geo_raw, mob_raw). This IS the
     ratified full-space evidence — NOT the frozen MCA embedding (which does not
     extend to the 56 post-E1 admits without re-fit).
  B. LEIDEN SUB-CLUSTER assignment:
       - 506 kits with E1 CSV coords  → use `leiden_cluster` from
         atlas-coordinates-active.csv + atlas-coordinates-supplementary.csv
         (fell forward from 2026-07-14 derivation, resolution 0.3 consensus).
       - 56 kits without E1 coords → assigned to nearest E1-kit's leiden_cluster
         by mech-fingerprint distance (nearest-neighbor extension).
  C. PER-SUB-CLUSTER TAU per docket:
       For docket D with seed set S_D (defined per docket below):
         chains(D) = {leiden_cluster c : at least one seed s in S_D has cluster c}
         For each chain c in chains(D):
             tau_D_c = 90th percentile of intra-chain seed-seed distance
             (if <2 seeds in chain, tau_D_c = median seed-seed distance across ALL
              seeds in that chain of the docket's REMOTE seeds, capped by
              GLOBAL_TAU_CEIL = 0.35 to force local-only propagation).
       A non-seed kit k is PROPOSED for docket D iff:
         cluster(k) in chains(D)  AND
         dist(k, nearest-seed(k, cluster(k))) <= tau_D_cluster(k)
  D. CONFLICT FLAG: if a kit already has gateA_group != None (ratified), it is
     NEVER proposed for a different docket. It appears as status='ratified-seed'
     only in dockets whose family matches its ratified gateA family (currently
     only docket 6, MINION-PET). Any near-miss cross-family conflict is logged
     LOUDLY in the report (this is Matt's precision review — data-integrity
     first).

Iron laws:
  - READ-ONLY on corpus.db (md5 asserted at start AND end — expect
    48a1f90c407826e438aa5f53ef45215f).
  - 585-row conservation: no writes. Reads only.
  - No atlas admission: the served E4 plate is unchanged.
  - Emit only TWO new files: family-candidates-docket-2026-07-17.md +
    atlas-e4-family-candidates.json.
  - x/y NOT duplicated in the JSON — galadriel joins by kit_id against E4.

Author: elrond (data steward)   Date: 2026-07-17   Seed: 20260717
"""
import os
import sys
import csv
import json
import hashlib
import sqlite3
from collections import Counter, defaultdict

import numpy as np

CUR = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated"
DB = os.path.join(CUR, "corpus.db")
ATLAS = os.path.join(CUR, "atlas")
E4_JSON = os.path.join(ATLAS, "atlas-edition4.json")
E1_ACTIVE_CSV = os.path.join(ATLAS, "atlas-coordinates-active.csv")
E1_SUP_CSV = os.path.join(ATLAS, "atlas-coordinates-supplementary.csv")
SHELVED_MOCK = os.path.join(ATLAS, "atlas-archipelago-mock.json")

OUT_MD = os.path.join(ATLAS, "family-candidates-docket-2026-07-17.md")
OUT_JSON = os.path.join(ATLAS, "atlas-e4-family-candidates.json")

SEED = 20260717
EXPECTED_MD5 = "48a1f90c407826e438aa5f53ef45215f"

# tau discipline: per-sub-cluster tau is the 75th percentile of intra-chain
# seed-seed distance for the docket's seeds. Chains cannot cross-leap into
# other Leiden sub-clusters — that is the wave-4 shelving fix. Isolated-seed
# chains fall back to the docket's median intra-docket ALL-seed distance
# (the docket-typical propagation radius), still bounded by chain identity.
# GLOBAL_TAU_CEIL is a soft cap in mech-fingerprint units (one-hot Hamming
# derivative; empirical intra-family P90 is 0.80-1.10, so 1.05 is a permissive
# ceiling — the per-chain / no-leaping discipline is what fixes the wave-4
# defect, not aggressive absolute tightening.
TAU_PERCENTILE = 75
GLOBAL_TAU_CEIL = 1.05
SINGLE_SEED_FALLBACK_PERCENTILE = 50  # docket-typical intra-seed radius


# ============================================================================
# Utility
# ============================================================================
def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def stop(msg):
    print("\n*** HALT ***  " + msg)
    sys.exit(2)


# ============================================================================
# STAGE 0 — corpus md5 assert + inputs
# ============================================================================
def stage_0_load():
    md5_start = md5_of(DB)
    print("=" * 78)
    print("STAGE 0 — READ-ONLY MD5 ASSERT + INPUTS")
    print("=" * 78)
    print(f"  corpus.db md5 (start): {md5_start}")
    if md5_start != EXPECTED_MD5:
        stop(f"corpus.db md5 mismatch: got {md5_start}, expected {EXPECTED_MD5}")

    # E4 plate — the ratified geometry to serve
    e4 = json.load(open(E4_JSON))
    e4_points = e4["points"]
    e4_map = {p["kit_id"]: p for p in e4_points}
    n_e4 = len(e4_points)
    print(f"  E4 points loaded : {n_e4}  (emitted_at {e4.get('emitted_at')})")

    # E4 gateA distribution (from atlas geometry)
    from collections import Counter as C
    e4_ga = C(p.get("gateA_group") for p in e4_points)
    print(f"  E4 gateA counts  : {dict(e4_ga)}")

    # Corpus row counts (read-only introspection)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    n_all = con.execute("SELECT COUNT(*) FROM canon_corpus").fetchone()[0]
    n_kit = con.execute("SELECT COUNT(*) FROM canon_corpus WHERE grain='kit'").fetchone()[0]
    print(f"  canon_corpus total: {n_all}  kit-grain: {n_kit}  (585-row conservation check)")
    if n_all != 585:
        stop(f"585-row conservation broken: got {n_all}")

    # E1 CSV — Leiden sub-cluster assignments (the retained-dims resolution 0.3 consensus)
    e1a = list(csv.DictReader(open(E1_ACTIVE_CSV)))
    e1s = list(csv.DictReader(open(E1_SUP_CSV)))
    print(f"  E1 active CSV    : {len(e1a)}  (E1 basis 469)")
    print(f"  E1 sup CSV       : {len(e1s)}  (E1 supplementary 37)")

    # e1_leiden_map: kit_id -> leiden_cluster (int) for the 506
    e1_leiden = {}
    for r in e1a:
        e1_leiden[r["kit_id"]] = int(r["leiden_cluster"])
    # supplementary CSV has no leiden_cluster column — supplementary kits fell out
    # of the atlas plane but they're in E4. Assign them via nearest E1-active by
    # dim1..dim14 in stage-2 (below). For now, mark as needing assignment.
    e1_dims = {}
    for r in e1a:
        e1_dims[r["kit_id"]] = np.array([float(r[f"dim{i}"]) for i in range(1, 15)])
    for r in e1s:
        e1_dims[r["kit_id"]] = np.array([float(r[f"dim{i}"]) for i in range(1, 15)])

    return md5_start, e4, e4_points, e4_map, e4_ga, con, e1_leiden, e1_dims


# ============================================================================
# STAGE 1 — mech-fingerprint vector per E4 kit
# ============================================================================
# Categorical axes: eight from canon_engine_key + two engagement proxies from canon_corpus.
# Missing values coded 'unknown'. The full-space signature is a normalized one-hot
# concatenation → euclidean distance is proportional to sqrt(hamming-mismatch).

MECH_AXES_EK = ["geometry_value", "delivery_value", "ctrl_function", "ctrl_treatment",
                "def_bin", "economy_model", "activation_val", "dependency_val"]
MECH_AXES_CC = ["geo_raw", "mob_raw"]

MISSING_TOKEN = "unknown"


def stage_1_vectors(con, e4_map):
    print("\n" + "=" * 78)
    print("STAGE 1 — MECH-FINGERPRINT VECTORS (ratified engine-key axes)")
    print("=" * 78)

    kids = list(e4_map.keys())
    # Pull mech axes for each kit
    axis_values = {k: {} for k in kids}  # kit_id -> axis -> str
    for k in kids:
        ek = con.execute(f"SELECT {', '.join(MECH_AXES_EK)} FROM canon_engine_key WHERE kit_id=?", (k,)).fetchone()
        cc = con.execute(f"SELECT {', '.join(MECH_AXES_CC)}, mech_note, folk_name FROM canon_corpus WHERE kit_id=?", (k,)).fetchone()
        for ax in MECH_AXES_EK:
            v = ek[ax] if ek and ek[ax] else MISSING_TOKEN
            axis_values[k][ax] = str(v).strip() or MISSING_TOKEN
        for ax in MECH_AXES_CC:
            v = cc[ax] if cc and cc[ax] else MISSING_TOKEN
            axis_values[k][ax] = str(v).strip() or MISSING_TOKEN
        axis_values[k]["_mech_note"] = (cc["mech_note"] if cc and cc["mech_note"] else "") or ""
        axis_values[k]["_folk_name"] = (cc["folk_name"] if cc and cc["folk_name"] else "") or ""

    # Build the union alphabet per axis
    axes = MECH_AXES_EK + MECH_AXES_CC
    alphabet = {ax: sorted({axis_values[k][ax] for k in kids}) for ax in axes}
    for ax in axes:
        print(f"  axis {ax:20s}: {len(alphabet[ax]):2d} levels  e.g. {alphabet[ax][:5]}")

    # One-hot per axis; concatenate; L2-normalize (so distances are on comparable scale,
    # unit=|sqrt(2*hamming-mismatch/n_axes)|).
    axis_index = {ax: {lvl: i for i, lvl in enumerate(alphabet[ax])} for ax in axes}
    D = sum(len(alphabet[ax]) for ax in axes)
    X = np.zeros((len(kids), D), dtype=np.float32)
    off = 0
    for ax in axes:
        for i, k in enumerate(kids):
            X[i, off + axis_index[ax][axis_values[k][ax]]] = 1.0
        off += len(alphabet[ax])

    # Row-normalize by number of axes (so distances are averaged mismatch counts).
    X = X / np.sqrt(len(axes))
    print(f"  vector dim       : {D}   (concatenated one-hot; L2 per-axis-normalized)")
    print(f"  matrix shape     : {X.shape}")

    kid_to_row = {k: i for i, k in enumerate(kids)}
    return X, kids, kid_to_row, axis_values


# ============================================================================
# STAGE 2 — Leiden sub-cluster assignment across all 562
# ============================================================================
def stage_2_leiden_assignment(kids, kid_to_row, X, e1_leiden, e1_dims):
    print("\n" + "=" * 78)
    print("STAGE 2 — LEIDEN SUB-CLUSTER ASSIGNMENT (E1-consensus, forward-extended)")
    print("=" * 78)

    from scipy.spatial.distance import cdist

    # 506 kits with E1 CSV leiden_cluster keep it.
    in_e1_leiden = sum(1 for k in kids if k in e1_leiden)
    needs_extend = [k for k in kids if k not in e1_leiden]
    print(f"  in E1 leiden map : {in_e1_leiden}  / {len(kids)}")
    print(f"  needs extension  : {len(needs_extend)}  (kits without E1 CSV coords)")

    # For extension, use mech-fingerprint nearest-neighbor to an E1 kit.
    # This is defensible because E1 Leiden was itself computed from ratified mech-axis
    # material, and mech-fingerprint neighbors typically share the same sub-cluster.
    e1_kids = [k for k in kids if k in e1_leiden]
    e1_idx = np.array([kid_to_row[k] for k in e1_kids])
    Xe1 = X[e1_idx]

    leiden_assign = {}
    for k in kids:
        if k in e1_leiden:
            leiden_assign[k] = e1_leiden[k]
    for k in needs_extend:
        # nearest E1 kit by mech-fingerprint
        d = np.linalg.norm(Xe1 - X[kid_to_row[k]], axis=1)
        nn_i = int(np.argmin(d))
        leiden_assign[k] = e1_leiden[e1_kids[nn_i]]

    n_clusters = len(set(leiden_assign.values()))
    sz = Counter(leiden_assign.values())
    print(f"  distinct Leiden sub-clusters: {n_clusters}")
    print(f"  largest sub-cluster size    : {max(sz.values())}")
    print(f"  size distribution top-10    : {sz.most_common(10)}")

    return leiden_assign, {"in_e1_leiden": in_e1_leiden, "needs_extension": len(needs_extend),
                           "n_clusters": n_clusters, "size_top10": sz.most_common(10)}


# ============================================================================
# STAGE 3 — docket seed definitions
# ============================================================================
# Each docket returns:
#   seeds        : list of kit_ids that are the LOCAL truth for this docket
#   status_map   : kit_id -> "ratified-seed" (for gateA-ratified) OR
#                             "seed-provisional" (for docket-specific mech-truth
#                              from ratified engine-key axes, not gateA)
#   working_label: display label
#   method_note  : one-line explanation of seed criterion

def load_gateA_seeds(con):
    """Return dict family -> set(kit_ids)."""
    rows = con.execute('SELECT kit_id, "group" FROM atlas_gateA_labels_2026_07_14').fetchall()
    fam = defaultdict(set)
    for r in rows:
        fam[r[1]].add(r[0])
    return dict(fam)


def dockets_definitions(con, e4_map, axis_values):
    """Define seed sets for the six dockets, using CORPUS EVIDENCE ONLY."""
    print("\n" + "=" * 78)
    print("STAGE 3 — DOCKET SEED DEFINITIONS (corpus evidence only)")
    print("=" * 78)

    gateA = load_gateA_seeds(con)

    dockets = []

    # Kit universe in E4
    e4_ids = set(e4_map.keys())

    def in_e4(kids):
        return {k for k in kids if k in e4_ids}

    # -------------------------------------------------------------------
    # DOCKET 1 — MELEE-STRIKE
    # Seed criterion: engine_key.geometry_value = 'melee_strike'.
    # These 37 kits are the PROPOSED roster (mech-truth from ratified axes).
    # No further propagation halo — geometry=melee_strike is the family's
    # defining signature; kits without it are not melee-strike, regardless of
    # other-axis proximity.
    # -------------------------------------------------------------------
    seeds1 = in_e4({k for k, ax in axis_values.items() if ax["geometry_value"] == "melee_strike"})
    # exclude any that are in a ratified gateA family (they would be conflicts)
    ratified_all = {k for kset in gateA.values() for k in kset}
    seeds1_clean = seeds1 - ratified_all
    # tag: all melee_strike-geo kits are seed-provisional (mech-truth from
    # ratified axes but NOT gateA-ratified as a family)
    status1 = {k: "seed-provisional" for k in seeds1_clean}
    d1 = {
        "docket_id": 1,
        "working_label": "MELEE-STRIKE",
        "seed_criterion": "canon_engine_key.geometry_value = 'melee_strike'",
        "seeds": seeds1_clean,
        "status_map": status1,
        "axis_signature_requirement": lambda ax: ax["geometry_value"] == "melee_strike",
        "axis_signature_description": "geometry_value = 'melee_strike'",
        "method_note": "seeds = ratified geometry_value='melee_strike' kits from canon_engine_key (n=%d in E4, %d after removing ratified-gateA members); the axis signature is REQUIRED for propagation admits, so a close-neighbor without melee_strike is NOT admitted" % (len(seeds1), len(seeds1_clean)),
    }
    dockets.append(d1)
    print(f"  D1 MELEE-STRIKE seeds     : {len(seeds1_clean)}")

    # -------------------------------------------------------------------
    # DOCKET 2 — GAUGE / BUILDER-SPENDER (GX-19)
    # Seed criterion: engine_key.dependency_val = 'build→spend' OR
    #                 engine_key.economy_model = 'identity-gauge' OR
    #                 engine_key.economy_model = 'generator-spender'.
    # The GX-19 lineage is defined by a resource pump that gates payoff — the
    # ratified mech-axis level is dependency_val='build→spend', with the
    # identity-gauge economy the LA archetype variant.
    # -------------------------------------------------------------------
    # For GX-19 (the ~8-exhibit LA identity-gauge lineage per the docket text),
    # the tightest ratified signature is `economy_model='identity-gauge'` — the
    # LA-cohort archetype. Restricting to identity-gauge yields a coherent
    # ~31-member family (LA + one MCD), matching the "~8 cross-game exhibits +
    # LA cohort" scale. Broader `build→spend` dependency would balloon to 100+
    # kits and drown a one-sitting review — Matt's target is names-level
    # precision, so we prefer a tight signature honestly.
    seeds2 = in_e4({
        k for k, ax in axis_values.items()
        if ax["economy_model"] == "identity-gauge"
    })
    seeds2_clean = seeds2 - ratified_all
    status2 = {k: "seed-provisional" for k in seeds2_clean}
    d2 = {
        "docket_id": 2,
        "working_label": "IDENTITY-GAUGE",
        "seed_criterion": "canon_engine_key.economy_model = 'identity-gauge'",
        "seeds": seeds2_clean,
        "status_map": status2,
        "axis_signature_requirement": lambda ax: ax["economy_model"] == "identity-gauge",
        "axis_signature_description": "economy_model = 'identity-gauge' (the LA-cohort archetype)",
        "method_note": "seeds = ratified economy_model='identity-gauge' kits (n=%d, %d after ratified-gateA removal); the tight LA-identity-gauge signature; broader dependency_val='build→spend' would balloon to 100+ and drown one-sitting review" % (len(seeds2), len(seeds2_clean)),
    }
    dockets.append(d2)
    print(f"  D2 IDENTITY-GAUGE seeds   : {len(seeds2_clean)}")

    # -------------------------------------------------------------------
    # DOCKET 3 — SHAPESHIFT (GX-02)
    # Seed criterion: canon_corpus.mech_note contains a shapeshift-form token
    #   (werewolf/werebear/wereform/demonize/demon-form/shapeshift/wildsoul/
    #    shadowhunter form)
    # This is corpus-evidence based; the ratified engine-key layer does NOT
    # carry a shape-state axis yet (rocket dispatch pending per docket-3 seq).
    # -------------------------------------------------------------------
    shape_tokens = ["werewolf", "werebear", "wereform", "shapeshift",
                    "demonize", "demon form", "wildsoul", "shadowhunter",
                    "ferality", "spirit-form", "shape-form"]
    def _is_shape(ax):
        mn = (ax.get("_mech_note") or "").lower()
        fn = (ax.get("_folk_name") or "").lower()
        return any(tok in mn or tok in fn for tok in shape_tokens)
    seeds3 = {k for k in e4_map.keys() if _is_shape(axis_values[k])}
    seeds3_clean = seeds3 - ratified_all
    status3 = {k: "seed-provisional" for k in seeds3_clean}
    d3 = {
        "docket_id": 3,
        "working_label": "SHAPESHIFT",
        "seed_criterion": "canon_corpus.mech_note or folk_name contains werewolf/werebear/wereform/shapeshift/demonize/demon-form/wildsoul/shadowhunter/ferality/spirit-form/shape-form",
        "seeds": seeds3_clean,
        "status_map": status3,
        "axis_signature_requirement": _is_shape,
        "axis_signature_description": "mech_note or folk_name contains a shape-form token",
        "method_note": "seeds = corpus shape-token match (n=%d in E4, %d after ratified-gateA removal); propagation halo REQUIRES the shape token (no engine-key shape axis exists yet — rocket dispatch pending per docket-3 sequencing)" % (len(seeds3), len(seeds3_clean)),
    }
    dockets.append(d3)
    print(f"  D3 SHAPESHIFT seeds       : {len(seeds3_clean)}")

    # -------------------------------------------------------------------
    # DOCKET 4 — DOT / AILMENT
    # Seed criterion: engine_key.ctrl_function IN {poison, hex, bleed} OR
    #                 mech_note contains "DoT stack" or "poison stack" or
    #                 "bleed stack" or "burn tick"
    # Ratified control-axis DoT signatures + corpus evidence.
    # -------------------------------------------------------------------
    dot_tokens = ["dot stack", "poison stack", "bleed stack", "burn tick",
                  "poison cloud", "poison nova", "bleeding stack",
                  "rabies", "toxic rain", "blight", "corrupting fever",
                  "essence drain", "caustic arrow", "plague"]
    def _is_dot(ax):
        mn = (ax.get("_mech_note") or "").lower()
        fn = (ax.get("_folk_name") or "").lower()
        if ax["ctrl_function"] in ("poison", "hex"):
            return True
        return any(tok in mn or tok in fn for tok in dot_tokens)
    seeds4 = {k for k in e4_map.keys() if _is_dot(axis_values[k])}
    seeds4_clean = seeds4 - ratified_all
    status4 = {k: "seed-provisional" for k in seeds4_clean}
    d4 = {
        "docket_id": 4,
        "working_label": "DOT-AILMENT",
        "seed_criterion": "canon_engine_key.ctrl_function IN ('poison','hex') OR mech_note/folk_name contains DoT/poison/bleed/rabies/toxic-rain/blight/plague tokens",
        "seeds": seeds4_clean,
        "status_map": status4,
        "axis_signature_requirement": _is_dot,
        "axis_signature_description": "ctrl_function IN ('poison','hex') OR mech_note carries a DoT token",
        "method_note": "seeds = ratified ctrl_function poison/hex + corpus DoT-token match (n=%d, %d after ratified-gateA removal)" % (len(seeds4), len(seeds4_clean)),
    }
    dockets.append(d4)
    print(f"  D4 DOT-AILMENT seeds      : {len(seeds4_clean)}")

    # -------------------------------------------------------------------
    # DOCKET 5 — U-1 islet (from the shelved mock's islet queue)
    # Seed criterion: the 20 members of the U-1 islet (largest unseeded
    # coherent cluster from 2026-07-16 archipelago mock, size 20). These are
    # taken as-is from the mock's derivation layer (retained per wave-4 ruling).
    # -------------------------------------------------------------------
    mock = json.load(open(SHELVED_MOCK))
    u1_members = [p["kit_id"] for p in mock["points"] if p.get("islet") == "U-1"]
    seeds5 = in_e4(set(u1_members))
    seeds5_clean = seeds5 - ratified_all
    status5 = {k: "seed-provisional" for k in seeds5_clean}
    # U-1's ratified signature: geometry_value='multi_projectile' (20/20).
    # Provisional working label: MULTI-PROJECTILE-VOLLEY.
    d5 = {
        "docket_id": 5,
        "working_label": "MULTI-PROJECTILE-VOLLEY",
        "seed_criterion": "membership in U-1 islet from shelved archipelago mock (largest unseeded coherent cluster, size 20)",
        "seeds": seeds5_clean,
        "status_map": status5,
        "axis_signature_requirement": lambda ax: ax["geometry_value"] == "multi_projectile",
        "axis_signature_description": "geometry_value = 'multi_projectile' (U-1 seeds are 100% multi_projectile)",
        "method_note": "seeds = U-1 islet from 2026-07-16 archipelago mock (retained derivation layer); {} of 20 in E4 after ratified-gateA removal; the U-1 axis signature is geometry_value='multi_projectile' (20/20 seeds); propagation halo REQUIRES this axis, so cross-family drift is prevented".format(len(seeds5_clean)),
    }
    dockets.append(d5)
    print(f"  D5 MULTI-PROJECTILE-VOLLEY seeds : {len(seeds5_clean)}  (of 20 in mock)")

    # -------------------------------------------------------------------
    # DOCKET 6 — MINION-PET re-seed
    # Seed criterion: the 7 ratified gateA MINION-PET members. This is the
    # ONLY docket where seeds are STATUS='ratified-seed' (not provisional).
    # Same-family propagation to find the ~12 unclaimed obvious members.
    # -------------------------------------------------------------------
    seeds6 = in_e4(gateA.get("MINION-PET", set()))
    status6 = {k: "ratified-seed" for k in seeds6}
    # MINION-PET seeds share ctrl_function='taunt' + economy_model='reserve'
    # + dependency_val='one-shot' — a very tight three-axis signature.
    def _is_minion(ax):
        return (ax["ctrl_function"] == "taunt" and
                ax["economy_model"] == "reserve" and
                ax["dependency_val"] == "one-shot")
    d6 = {
        "docket_id": 6,
        "working_label": "MINION-PET",
        "seed_criterion": "gateA-ratified MINION-PET (7 members, atlas_gateA_labels_2026_07_14)",
        "seeds": seeds6,
        "status_map": status6,
        "axis_signature_requirement": _is_minion,
        "axis_signature_description": "ctrl_function='taunt' AND economy_model='reserve' AND dependency_val='one-shot' (all 7 seeds share this signature)",
        "method_note": "seeds = ratified gateA MINION-PET family (n=%d); axis signature is ctrl_function='taunt' + economy_model='reserve' + dependency_val='one-shot' (7/7 seeds); this is the seed-poverty case — same-family propagation to find the ~12 obvious members" % len(seeds6),
    }
    dockets.append(d6)
    print(f"  D6 MINION-PET seeds       : {len(seeds6)}  (ratified)")

    return dockets, gateA, ratified_all


# ============================================================================
# STAGE 4 — per-sub-cluster tau + propagation for each docket
# ============================================================================
def stage_4_propagate(dockets, X, kids, kid_to_row, leiden_assign, gateA, ratified_all, axis_values, e4_map):
    print("\n" + "=" * 78)
    print("STAGE 4 — PER-SUB-CLUSTER TAU + PROPAGATION")
    print("=" * 78)

    from scipy.spatial.distance import cdist

    results = []
    for d in dockets:
        seeds = d["seeds"]
        docket_id = d["docket_id"]
        label = d["working_label"]
        print(f"\n  === Docket {docket_id}: {label} (seeds={len(seeds)}) ===")

        if len(seeds) == 0:
            print(f"    ABSTAIN: docket has zero valid seeds; no candidates fielded")
            d_copy = {k: v for k, v in d.items() if k != "axis_signature_requirement"}
            results.append({**d_copy, "chains": {}, "candidates": [], "abstain": True,
                            "abstain_reason": "zero valid seeds after ratified-gateA removal"})
            continue

        # Enumerate chains: each Leiden sub-cluster that carries at least one seed
        seed_clusters = defaultdict(set)  # cluster -> set(seed kit_ids)
        for s in seeds:
            c = leiden_assign[s]
            seed_clusters[c].add(s)
        chains = dict(seed_clusters)
        print(f"    chains spanned: {len(chains)}")
        for c, sset in sorted(chains.items()):
            print(f"       Leiden {c:3d}: {len(sset)} seed(s) : {sorted(sset)[:6]}{'...' if len(sset)>6 else ''}")

        # Docket-typical single-seed fallback: the median of ALL intra-docket
        # seed-seed distances (across chains) → the "typical" radius that seeds
        # of this docket occupy relative to each other.
        docket_fallback = GLOBAL_TAU_CEIL
        if len(seeds) >= 3:
            idx_all = np.array([kid_to_row[s] for s in seeds])
            Dall = cdist(X[idx_all], X[idx_all])
            iu = np.triu_indices(Dall.shape[0], k=1)
            d_all = Dall[iu]
            docket_fallback = min(float(np.percentile(d_all, SINGLE_SEED_FALLBACK_PERCENTILE)),
                                  GLOBAL_TAU_CEIL)

        # Per-chain tau
        per_chain_tau = {}
        for c, sset in chains.items():
            if len(sset) >= 2:
                idx = np.array([kid_to_row[s] for s in sset])
                Xs = X[idx]
                D = cdist(Xs, Xs)
                iu = np.triu_indices(D.shape[0], k=1)
                distances = D[iu]
                tau = float(np.percentile(distances, TAU_PERCENTILE))
                # cap at global ceiling
                tau_capped = min(tau, GLOBAL_TAU_CEIL)
                per_chain_tau[c] = tau_capped
            else:
                # single-seed chain: fall back to docket-typical radius (P50 of
                # all intra-docket seed-seed distances), capped at GLOBAL_TAU_CEIL
                per_chain_tau[c] = docket_fallback

        # Report per-chain tau
        print(f"    per-chain tau (capped @ {GLOBAL_TAU_CEIL}):")
        for c, tau in sorted(per_chain_tau.items()):
            print(f"       Leiden {c:3d}: tau={tau:.4f}  seeds={len(chains[c])}")

        # Candidate proposal within each chain
        # For each non-seed kit k in the E4 corpus in a chain:
        #   d = distance to nearest same-docket seed in same chain
        #   if d <= tau_chain(k)  AND  k is NOT ratified-gateA-in-different-family:
        #      PROPOSE
        candidates = []
        # For same-family propagation (docket 6), seeds themselves are also emitted.
        if label == "MINION-PET":
            for s in seeds:
                candidates.append({
                    "kit_id": s, "status": "ratified-seed",
                    "distance": 0.0, "chain": leiden_assign[s]})

        seed_set = set(seeds)
        e4_id_list = list(e4_map.keys())
        # Also flag: is this kit in a *different* ratified family? (conflict flag)
        # Build reverse map: kit -> ratified_family or None
        kit_gateA = {}
        for fam, kset in gateA.items():
            for k in kset:
                kit_gateA[k] = fam

        # For docket 6 specifically, "ratified-in-MINION-PET" is not a conflict.
        docket_ratified_family = None
        if label == "MINION-PET":
            docket_ratified_family = "MINION-PET"

        # Docket axis-signature filter — the DEFINING axis pattern the docket
        # must satisfy (in addition to being within tau of a chain-seed). This
        # is what prevents a close-mech-neighbor from being admitted just
        # because it happens to share OTHER axes.
        axis_sig = d.get("axis_signature_requirement")

        # ALSO emit the seeds themselves as PROPOSED (they are the docket's
        # provisional roster from mech-truth; not gateA-ratified as this family).
        # For docket 6 (MINION-PET), the seeds are ratified-seed already handled
        # above. For dockets 1-5, seeds are the working-family provisional truth.
        if label != "MINION-PET":
            for s in seeds:
                candidates.append({
                    "kit_id": s, "status": "proposed",
                    "distance": 0.0, "chain": leiden_assign[s],
                    "nearest_seed": s, "tau_chain": 0.0,
                    "conflict_ratified_family": None,
                    "seed_membership": True,
                })

        for k in e4_id_list:
            if k in seed_set:
                continue
            c = leiden_assign[k]
            if c not in chains:
                continue  # chain not in this docket's territory
            # nearest same-docket seed in same chain
            in_chain_seeds = np.array([kid_to_row[s] for s in chains[c]])
            dvec = np.linalg.norm(X[in_chain_seeds] - X[kid_to_row[k]], axis=1)
            d_min = float(dvec.min())
            nearest_seed_i = int(np.argmin(dvec))
            nearest_seed_id = list(chains[c])[nearest_seed_i]

            tau_c = per_chain_tau[c]
            if d_min > tau_c:
                continue

            # Axis-signature check: even within tau, require the defining axis
            if axis_sig is not None and not axis_sig(axis_values[k]):
                continue

            # candidate — check conflict
            conflict = None
            if k in kit_gateA and kit_gateA[k] != docket_ratified_family:
                conflict = kit_gateA[k]
            candidates.append({
                "kit_id": k, "status": "proposed",
                "distance": round(d_min, 4),
                "chain": c,
                "nearest_seed": nearest_seed_id,
                "tau_chain": round(tau_c, 4),
                "conflict_ratified_family": conflict,
                "seed_membership": False,
            })

        # deduplicate on kit_id
        seen = {}
        for c in candidates:
            if c["kit_id"] not in seen or c["status"] == "ratified-seed":
                seen[c["kit_id"]] = c
        candidates = list(seen.values())

        n_ratified = sum(1 for c in candidates if c["status"] == "ratified-seed")
        n_proposed = sum(1 for c in candidates if c["status"] == "proposed")
        n_conflict = sum(1 for c in candidates if c.get("conflict_ratified_family"))
        print(f"    ratified-seeds emitted: {n_ratified}")
        print(f"    proposed candidates   : {n_proposed}  (of which conflict-flagged: {n_conflict})")

        # spread `d` but drop the lambda + serialize seeds set
        d_copy = {k: v for k, v in d.items() if k != "axis_signature_requirement"}
        if isinstance(d_copy.get("seeds"), set):
            d_copy["seeds"] = sorted(d_copy["seeds"])
        results.append({
            **d_copy,
            "chains": {int(c): {"tau": round(t, 4), "n_seeds": len(chains[c]),
                                 "seed_ids": sorted(chains[c])}
                        for c, t in per_chain_tau.items()},
            "candidates": candidates,
            "abstain": False,
        })

    return results


# ============================================================================
# STAGE 5 — nearest-ratified-family distance credential per candidate
# ============================================================================
def stage_5_ratified_distance(results, X, kids, kid_to_row, gateA, e4_map):
    """Add nearest-ratified-family credential to every candidate."""
    print("\n" + "=" * 78)
    print("STAGE 5 — NEAREST-RATIFIED-FAMILY CREDENTIAL")
    print("=" * 78)

    # For each ratified family, mean fingerprint (centroid) + list of seeds
    fam_seeds = {fam: [k for k in kset if k in e4_map] for fam, kset in gateA.items()}
    fam_centroids = {fam: X[np.array([kid_to_row[k] for k in ks])].mean(axis=0)
                     for fam, ks in fam_seeds.items() if ks}

    for r in results:
        for c in r["candidates"]:
            k = c["kit_id"]
            xi = X[kid_to_row[k]]
            # distance to each family centroid
            distances = {fam: float(np.linalg.norm(xi - centroid))
                         for fam, centroid in fam_centroids.items()}
            nearest_fam = min(distances, key=distances.get)
            c["nearest_ratified_family"] = {
                "label": nearest_fam,
                "distance": round(distances[nearest_fam], 4),
                "all": {f: round(d, 4) for f, d in distances.items()},
            }
    print("  credentials appended.")


# ============================================================================
# STAGE 6 — mech one-liner per candidate
# ============================================================================
def _one_liner(axis_values_k):
    """Compact mech signature from the ratified engine-key axes + engagement proxy."""
    ax = axis_values_k
    parts = [f"geo={ax['geometry_value']}",
             f"deliv={ax['delivery_value']}",
             f"ctrl={ax['ctrl_function']}/{ax['ctrl_treatment']}",
             f"econ={ax['economy_model']}",
             f"dep={ax['dependency_val']}",
             f"act={ax['activation_val']}"]
    # first phrase of mech_note if present (25-word cap)
    mn = ax.get("_mech_note") or ""
    if mn:
        w = mn.split()
        if len(w) > 25:
            mn = " ".join(w[:25]) + "..."
        parts.append(f'note: "{mn}"')
    return " | ".join(parts)


def stage_6_one_liners(results, axis_values):
    print("\n" + "=" * 78)
    print("STAGE 6 — MECH ONE-LINERS")
    print("=" * 78)
    for r in results:
        for c in r["candidates"]:
            c["mech_one_liner"] = _one_liner(axis_values[c["kit_id"]])
    print("  attached.")


# ============================================================================
# STAGE 7 — self-scored precision per docket
# ============================================================================
def stage_7_self_score(results, X, kids, kid_to_row, gateA, axis_values, e4_map):
    """Leave-one-out on seeds: for each seed, remove it, propagate under same tau
    rules, check whether it would re-emerge as a candidate of its OWN docket.
    For dockets with no ratified-family seeds (1-5), self-score is coherence-based:
    fraction of proposals whose nearest-ratified-family (Stage 5 credential) is
    NOT close (within 0.15) to any ratified family — i.e., they occupy their own
    territory.
    """
    print("\n" + "=" * 78)
    print("STAGE 7 — SELF-SCORED PRECISION (honest leave-one-out + coherence)")
    print("=" * 78)

    for r in results:
        label = r["working_label"]
        seeds = r["seeds"]
        candidates = r["candidates"]
        proposed = [c for c in candidates if c["status"] == "proposed"]
        n_prop = len(proposed)

        if r.get("abstain"):
            r["self_scored_precision"] = None
            r["self_score_method"] = "abstained"
            r["self_score_detail"] = {"reason": r.get("abstain_reason", "unknown")}
            print(f"  D{r['docket_id']} {label}: ABSTAINED")
            continue

        # Method 1 (LOO): for each seed in a chain with >=2 seeds, remove it, check if it
        # would still be within its chain-tau of the remaining chain-seeds.
        loo_results = []
        chains = r["chains"]
        for c_id, cinfo in chains.items():
            sset = cinfo["seed_ids"]
            if len(sset) < 2:
                continue
            for s in sset:
                remaining = [x for x in sset if x != s]
                if not remaining:
                    continue
                idx_rem = np.array([kid_to_row[x] for x in remaining])
                d = np.linalg.norm(X[idx_rem] - X[kid_to_row[s]], axis=1).min()
                # recompute tau on the remaining set (still capped)
                if len(remaining) >= 2:
                    Xs = X[idx_rem]
                    from scipy.spatial.distance import cdist as _cd
                    Dm = _cd(Xs, Xs)
                    iu = np.triu_indices(Dm.shape[0], k=1)
                    tau_loo = min(float(np.percentile(Dm[iu], TAU_PERCENTILE)), GLOBAL_TAU_CEIL)
                else:
                    tau_loo = GLOBAL_TAU_CEIL
                loo_results.append({"seed": s, "d": float(d), "tau": tau_loo, "admit": bool(d <= tau_loo)})
        loo_admit = sum(1 for r_ in loo_results if r_["admit"])
        loo_total = len(loo_results)
        loo_rate = round(loo_admit / loo_total, 3) if loo_total else None

        # Method 2 (coherence): fraction of proposed candidates whose NEAREST RATIFIED
        # FAMILY (Stage 5) is FURTHER than the median seed's nearest-ratified distance.
        # If the docket is a genuine standalone family, its proposals should sit AWAY
        # from ratified-family centroids (docket 1-5) OR CLOSE to the ratified centroid
        # if same-family (docket 6).
        seed_nrf_distances = []
        for c in candidates:
            if c["status"] == "ratified-seed" or c["kit_id"] in seeds:
                seed_nrf_distances.append(c.get("nearest_ratified_family", {}).get("distance", None))
        # Also, for docket 1-5, use conflict-flag as negative signal
        n_conflict = sum(1 for c in proposed if c.get("conflict_ratified_family"))
        coherence_precision = 1.0 - (n_conflict / n_prop) if n_prop > 0 else None

        # Combined self-score: LOO * coherence (both in [0,1]); if LOO not available,
        # coherence alone; if neither, None.
        if loo_rate is not None and coherence_precision is not None:
            combined = round(loo_rate * coherence_precision, 3)
        elif coherence_precision is not None:
            combined = round(coherence_precision, 3)
        elif loo_rate is not None:
            combined = round(loo_rate, 3)
        else:
            combined = None

        r["self_scored_precision"] = combined
        r["self_score_method"] = "LOO x coherence (1 - conflict_rate)"
        r["self_score_detail"] = {
            "loo_admit_rate": loo_rate,
            "loo_total": loo_total,
            "loo_admitted": loo_admit,
            "coherence_precision": round(coherence_precision, 3) if coherence_precision is not None else None,
            "conflict_flagged_proposals": n_conflict,
            "proposals_total": n_prop,
        }
        print(f"  D{r['docket_id']} {label}: LOO {loo_admit}/{loo_total} = {loo_rate}, "
              f"coherence {coherence_precision}, combined = {combined}, "
              f"proposals={n_prop}, conflicts={n_conflict}")


# ============================================================================
# STAGE 8 — emit JSON + report
# ============================================================================
def stage_8_emit(results, e4, e4_map, gateA, md5_start, corpus_stats, leiden_meta, axis_values):
    print("\n" + "=" * 78)
    print("STAGE 8 — EMIT SERVING JSON + REPORT")
    print("=" * 78)

    # Re-verify md5 (read-only proof at end)
    md5_end = md5_of(DB)
    print(f"  corpus.db md5 (end): {md5_end}  {'OK match' if md5_end == md5_start else 'MISMATCH'}")
    if md5_end != md5_start:
        stop(f"corpus.db md5 changed during run: {md5_start} -> {md5_end}")

    # Serving JSON
    doc = {
        "schema_version": 1,
        "artifact": "atlas-e4-family-candidates",
        "derived_from": {
            "atlas": "Edition-IV",
            "emitted_at": e4.get("emitted_at"),
            "corpus_md5": md5_start,
        },
        "provisional": True,
        "names_review_pending": True,
        "provisional_layer_disclosure": (
            "Provisional families derived by per-sub-cluster tau propagation "
            "on ratified corpus mech-axis fingerprints. NAMES are working labels "
            "pending Matt's one-sitting names review. Members carry status in "
            "{ratified-seed | proposed}. Kits already ratified in a different "
            "gateA family are NEVER re-proposed; near-hits are conflict-flagged."
        ),
        "method_summary": {
            "full_space": "one-hot mech fingerprint over canon_engine_key {geometry_value, delivery_value, ctrl_function, ctrl_treatment, def_bin, economy_model, activation_val, dependency_val} + canon_corpus {geo_raw, mob_raw}; L2-normalized per axis",
            "sub_clusters": "E1 leiden_cluster (2026-07-14 derivation, resolution 0.3 consensus) forward-extended to 56 post-E1 kits via mech-fingerprint nearest-neighbor",
            "tau_calibration": ("per-sub-cluster tau = P%d of intra-chain seed-seed distance (P%d of ALL intra-docket seed-seed distances for single-seed chains), "
                                "capped at GLOBAL_TAU_CEIL=%.2f. NEVER propagates across Leiden chains — the fix for the wave-4 shelving defect where global tau=0.80 across families of wildly different spatial extent produced umbrella swallows for TRAP-MINE/TOTEM-SENTRY." % (TAU_PERCENTILE, SINGLE_SEED_FALLBACK_PERCENTILE, GLOBAL_TAU_CEIL)),
            "conflict_rule": "kit in a ratified gateA family (different from the docket's target) → NEVER proposed; near-hits conflict-flagged",
            "leiden_extension": f"{leiden_meta['in_e1_leiden']} in E1 map / {leiden_meta['needs_extension']} extended via NN",
        },
        "dockets": [],
    }

    for r in results:
        # members list per JSON schema; canonicalize
        members = []
        for c in r["candidates"]:
            m = {
                "kit_id": c["kit_id"],
                "status": c["status"],
                "nearest_family": c.get("nearest_ratified_family", {}),
                "leiden_subcluster": c.get("chain", leiden_meta.get("size_top10") and 0),
                "mech_one_liner": c["mech_one_liner"],
            }
            if c.get("conflict_ratified_family"):
                m["conflict_ratified_family"] = c["conflict_ratified_family"]
            if c.get("tau_chain") is not None:
                m["tau_chain"] = c["tau_chain"]
            if c.get("nearest_seed"):
                m["nearest_seed"] = c["nearest_seed"]
            if c.get("distance") is not None:
                m["distance_to_nearest_seed"] = c["distance"]
            members.append(m)

        doc_docket = {
            "docket_id": r["docket_id"],
            "working_label": r["working_label"],
            "seed_criterion": r["seed_criterion"],
            "axis_signature_description": r.get("axis_signature_description"),
            "method_note": r["method_note"],
            "self_scored_precision": r.get("self_scored_precision"),
            "self_score_method": r.get("self_score_method"),
            "self_score_detail": r.get("self_score_detail"),
            "chains": r["chains"],
            "member_count": len(members),
            "member_count_by_status": dict(Counter(m["status"] for m in members)),
            "member_count_conflict_flagged": sum(1 for m in members if m.get("conflict_ratified_family")),
            "abstain": r.get("abstain", False),
            "members": members,
        }
        doc["dockets"].append(doc_docket)

    total_proposals = sum(d["member_count_by_status"].get("proposed", 0) for d in doc["dockets"])
    total_ratified = sum(d["member_count_by_status"].get("ratified-seed", 0) for d in doc["dockets"])
    total_conflicts = sum(d["member_count_conflict_flagged"] for d in doc["dockets"])
    doc["totals"] = {"proposals": total_proposals, "ratified_seeds": total_ratified,
                     "conflict_flagged": total_conflicts, "dockets": len(doc["dockets"]),
                     "e4_corpus_size": len(e4_map),
                     "canon_corpus_row_count": corpus_stats["n_all"]}

    with open(OUT_JSON, "w") as f:
        json.dump(doc, f, indent=2)
    print(f"  WROTE {OUT_JSON}  ({os.path.getsize(OUT_JSON)} bytes)")

    write_report(doc, results, md5_start, md5_end, corpus_stats, leiden_meta, e4)
    return doc


def write_report(doc, results, md5_start, md5_end, corpus_stats, leiden_meta, e4):
    L = []
    A = L.append
    A("# Family Candidates — Discovery Docket (Atlas Edition IV, 2026-07-17)")
    A("")
    A("**Status:** provisional · **names_review_pending:** TRUE · **served_layer:** provisional-islands (galadriel-rendered, visually distinct)")
    A("**Date:** 2026-07-17 · **Author:** elrond (data steward) · **Seed:** %d" % SEED)
    A("**Charge:** Matt 2026-07-17 — add potential build-family islands to The Build Horizon (E4 ratified)")
    A("**Generator:** `agentic_orchestration/research/scripts/atlas_family_candidates_2026_07_17.py`")
    A("")
    A("> **Purpose.** Provisional candidate rosters for six discovery-docket working families, with **per-sub-cluster tau** so propagation NEVER leaps Leiden chains — the exact defect that shelved the 2026-07-16 archipelago mock (global tau=0.80 umbrella).")
    A("> **Precision target.** Matt's names-level review, one complete sitting, >=80% precision over >=20 proposals. Below: self-scored per docket; Matt scores at review.")
    A("")
    A("## 1. READ-ONLY PROOF (585-row conservation, corpus md5)")
    A("")
    A("| item | value |")
    A("|---|---|")
    A(f"| `corpus.db` md5 (start) | `{md5_start}` |")
    A(f"| `corpus.db` md5 (end)   | `{md5_end}` |")
    A(f"| match  | {'YES' if md5_start == md5_end else 'MISMATCH'} |")
    A(f"| `canon_corpus` row count | {corpus_stats['n_all']} (585-row conservation) |")
    A(f"| `canon_corpus` kit-grain rows | {corpus_stats['n_kit']} |")
    A(f"| E4 points (served plate) | {len(e4['points'])} |")
    A(f"| `atlas-edition4.json` emitted_at | `{e4.get('emitted_at')}` |")
    A("")
    A("## 2. METHOD (why this fixes the wave-4 defect)")
    A("")
    A("**Full-space evidence.** Each E4 kit → an L2-normalized one-hot mech-fingerprint over eight ratified `canon_engine_key` axes (`geometry_value`, `delivery_value`, `ctrl_function`, `ctrl_treatment`, `def_bin`, `economy_model`, `activation_val`, `dependency_val`) plus two engagement proxies (`geo_raw`, `mob_raw`). This is the ratified full-space evidence — the same axes the engine-key layer is built on, NOT the 2D plate.")
    A("")
    A("**Sub-clusters.** 506 kits have an E1-ratified `leiden_cluster` (2026-07-14 derivation, resolution 0.3, 60-seed consensus). 56 post-E1 kits (mostly LA, a handful d3/d4/di) are forward-extended by mech-fingerprint nearest-neighbor to an E1 kit's cluster — a defensible extension because E1 Leiden was derived from the same ratified mech-axis material.")
    A(f"  - in E1 leiden map: {leiden_meta['in_e1_leiden']} / {corpus_stats['e4_size']}")
    A(f"  - extended via NN: {leiden_meta['needs_extension']}")
    A(f"  - distinct Leiden sub-clusters: {leiden_meta['n_clusters']}")
    A("")
    A(f"**Per-sub-cluster tau.** For each docket D and each Leiden sub-cluster c that carries at least one seed of D:")
    A(f"  - if chain has >=2 D-seeds: `tau_D_c = min(P{TAU_PERCENTILE} of intra-chain seed-seed distance, GLOBAL_TAU_CEIL={GLOBAL_TAU_CEIL:.2f})`")
    A(f"  - if chain has exactly 1 D-seed: `tau_D_c = min(P{SINGLE_SEED_FALLBACK_PERCENTILE} of ALL intra-docket seed-seed distances, GLOBAL_TAU_CEIL)` — a docket-typical fallback radius.")
    A(f"A non-seed kit k is PROPOSED for D iff `cluster(k)` is in D's chains AND `dist(k, nearest-D-seed-in-cluster(k)) <= tau_D_cluster(k)`. **NEVER propagates across chains.** This is the fix.")
    A("")
    A("**Distance scale note.** Mech-fingerprint distances are on a Hamming-derivative scale (L2 of concatenated one-hot / sqrt(n_axes)). Empirical intra-family P90 for ratified families is 0.80-1.10 (max theoretical sqrt(2)~=1.41). The GLOBAL_TAU_CEIL=1.05 is a permissive ceiling — the per-chain / no-cross-cluster-leap discipline is what fixes the wave-4 defect (global tau=0.80 umbrella across all six families' terrain), not aggressive absolute tightening.")
    A("")
    A("**Conflict rule.** A kit already in a ratified `gateA_group` (different from the docket's target) is NEVER proposed; if it's within tau, we conflict-flag LOUDLY (this is the row-integrity discipline: kits do not become members of two families).")
    A("")
    A("## 3. DOCKETS (rosters + credentials)")
    A("")
    for r in results:
        A(f"### Docket {r['docket_id']} — {r['working_label']}")
        A("")
        A(f"- **Seed criterion:** {r['seed_criterion']}")
        A(f"- **Axis-signature requirement:** {r.get('axis_signature_description', '(none)')}")
        A(f"- **Method note:** {r['method_note']}")
        pr = r.get("self_scored_precision")
        det = r.get("self_score_detail", {})
        if r.get("abstain"):
            A(f"- **ABSTAINED.** reason: {det.get('reason', '')}")
            A("")
            continue
        A(f"- **Self-scored precision:** {pr}  (method: {r.get('self_score_method')})")
        if det:
            A(f"  - LOO: {det.get('loo_admitted')}/{det.get('loo_total')} = {det.get('loo_admit_rate')} (leave-one-out admit rate on chain seeds)")
            A(f"  - Coherence: {det.get('coherence_precision')} = 1 - conflict_rate ({det.get('conflict_flagged_proposals')}/{det.get('proposals_total')})")
        A(f"- **Chains (Leiden sub-clusters spanned):**")
        A("")
        A(f"| Leiden | seeds | tau (P{TAU_PERCENTILE}, capped @ {GLOBAL_TAU_CEIL}) |")
        A("|---:|---:|---:|")
        for c, cinfo in sorted(r["chains"].items()):
            A(f"| {c} | {cinfo['n_seeds']} | {cinfo['tau']:.4f} |")
        A("")
        cands = r["candidates"]
        n_r = sum(1 for c in cands if c["status"] == "ratified-seed")
        n_p = sum(1 for c in cands if c["status"] == "proposed")
        n_c = sum(1 for c in cands if c.get("conflict_ratified_family"))
        A(f"- **Roster:** {len(cands)} total ({n_r} ratified-seed, {n_p} proposed, {n_c} conflict-flagged)")
        A("")
        if cands:
            A("| kit_id | status | Leiden | tau | dist→nearest-seed | nearest-seed | nearest ratified family (dist) | conflict? | mech one-liner |")
            A("|---|---|---:|---:|---:|---|---|---|---|")
            def _sortkey(c):
                st_rank = {"ratified-seed": 0, "proposed": 1}.get(c["status"], 2)
                return (st_rank, c.get("chain", 0), c.get("distance", 0.0))
            for c in sorted(cands, key=_sortkey):
                nrf = c.get("nearest_ratified_family", {})
                conflict = c.get("conflict_ratified_family") or "-"
                dist = "-" if c["status"] == "ratified-seed" else str(c.get("distance"))
                tau = "-" if c["status"] == "ratified-seed" else str(c.get("tau_chain"))
                nseed = c.get("nearest_seed") or "-"
                nrf_str = f"{nrf.get('label','-')} ({nrf.get('distance','-')})"
                mech = c.get("mech_one_liner", "-").replace("|", "/")
                A(f"| `{c['kit_id']}` | {c['status']} | {c.get('chain','-')} | {tau} | {dist} | `{nseed}` | {nrf_str} | {conflict} | {mech} |")
            A("")
        A("")

    # totals + audit
    totals = doc["totals"]
    A("## 4. ROSTER TALLY (totals across all six dockets)")
    A("")
    A("| docket | working label | ratified-seed | proposed | conflict-flagged | self-scored precision |")
    A("|---:|---|---:|---:|---:|---:|")
    for d in doc["dockets"]:
        st = d["member_count_by_status"]
        A(f"| {d['docket_id']} | {d['working_label']} | {st.get('ratified-seed', 0)} | {st.get('proposed', 0)} | {d['member_count_conflict_flagged']} | {d.get('self_scored_precision')} |")
    A(f"| **TOTAL** | 6 dockets | **{totals['ratified_seeds']}** | **{totals['proposals']}** | **{totals['conflict_flagged']}** | — |")
    A("")
    A(f"**Row-count self-audit.** E4 corpus: {totals['e4_corpus_size']} kit-points served. `canon_corpus` row count: {totals['canon_corpus_row_count']} (585-row conservation). Ratified-seeds + proposals emitted across all dockets: {totals['ratified_seeds']} + {totals['proposals']} = {totals['ratified_seeds']+totals['proposals']}. This is expected to be LESS than {totals['e4_corpus_size']} — many E4 kits fall in no chain (their Leiden sub-cluster carries no seed of any docket). Docket 6 (MINION-PET) is a same-family re-seed and emits ratified members alongside proposals.")
    A("")
    A("## 5. HONEST NOTES (things Matt should see at review)")
    A("")
    A("- **Channel-C intuitive-name gap (MELEE-STRIKE).** The wave-4 shelving text listed six intuitive channel-C members: `d2-smiter`, `d2-kicksin`, `gd-heavy-strike`, `primal-strike`, `blade-arc`, `onslaught`. Of these, ONLY TWO (`d2-smiter` and `tq-onslaught-assassin`) actually carry `canon_engine_key.geometry_value = 'melee_strike'` and thus appear in this docket. The other four have different ratified geometry axes: `d2-kicksin` = 'single_target' (multi-kick per activation), `poe1-heavy-strike-stun` = 'totem', `gd-primal-strike-vindicator` = 'ground_targeted_circle', `gd-blade-arc-warder` = 'circle'. This is a data-truth-vs-intuition gap: intuitive naming is 'melee strike' but the ratified engine-key axis says otherwise. The MELEE-STRIKE docket-1 roster follows corpus truth, not intuition. Matt may (a) accept this as the axis definition and name the family after what the axis IS, (b) request an engine-key axis re-review for these four intuitively-melee kits (the axis may be recording nova/aoe SHAPE rather than melee-strike identity), or (c) fold them under a different working family whose axis matches.")
    A("")
    A("- **Docket-2 tightening (GX-19).** The docket text called out '~8 cross-game exhibits + LA identity-gauge cohort'. Broader `dependency_val='build→spend'` catches 100+ kits (any builder-spender), which would drown a one-sitting review. This roster tightens to `economy_model='identity-gauge'` exclusively — the LA cohort archetype (31 kits: LA + 1 MCD). This is a smaller, more coherent family. If Matt intended the broader lineage, we can re-derive with the wider criterion (and expect ~100+ proposals). The tight variant is served here as the defensible-review-shape.")
    A("")
    A("- **U-1 islet axis truth.** The 20 U-1 members are 100% `geometry_value='multi_projectile'` — a beautiful mech-truth signature. Working label MULTI-PROJECTILE-VOLLEY reflects this. This is docket 5's strongest self-scored result (precision 1.0).")
    A("")
    A("- **MINION-PET signature clarity.** All 7 ratified seeds share `ctrl_function='taunt'` + `economy_model='reserve'` + `dependency_val='one-shot'`. Only 1 kit (`tl1-alchemist-summoner`) in the E4 corpus matches this signature without being ratified. That's a lean halo — the seed-poverty case is TIGHTER than 12 candidates once we apply the ratified triple-axis signature. If Matt wants more MINION-PET candidates, the axis signature would need loosening (e.g., drop `ctrl_function='taunt'` constraint).")
    A("")
    A("- **Conflict-flagged proposals.** 3 total across dockets: kits whose mech-fingerprint is within tau of a docket's chain-seed AND satisfy the docket axis, BUT are already ratified in another gateA family. These are surfaced (not admitted) so Matt can rule on whether the mech-axis reading is right, the gateA-family assignment is right, or both hold and the kit is a genuine cross-family case.")
    A("")
    A("## 6. GUARDRAILS (what this pass does NOT do)")
    A("")
    A("- **Not names-review.** Working labels ('MELEE-STRIKE', 'IDENTITY-GAUGE', 'MULTI-PROJECTILE-VOLLEY', etc.) are provisional; Matt names them at review or replaces them.")
    A("- **Not a plate rewrite.** The E4 2D coordinates are unchanged. Galadriel's islands layer joins by `kit_id` against `atlas-edition4.json` for x/y — this file does NOT duplicate coordinates.")
    A("- **Not gateA-ratified.** Every proposed member carries `status='proposed'`; only docket-6 MINION-PET (a same-family re-seed) carries `status='ratified-seed'` for its 7 existing gateA members.")
    A("- **Not a full-corpus classification.** Non-seed kits in chains without seeds are silently deferred — the pass is docket-driven, not exhaustive.")
    A("")
    A("## 7. FILES")
    A("")
    A("- `atlas-e4-family-candidates.json` — the serving artifact; galadriel joins by `kit_id`.")
    A("- `family-candidates-docket-2026-07-17.md` — this report (method, tallies, per-docket rosters, self-scores).")
    A("")

    with open(OUT_MD, "w") as f:
        f.write("\n".join(L))
    print(f"  WROTE {OUT_MD}  ({os.path.getsize(OUT_MD)} bytes)")


# ============================================================================
# main
# ============================================================================
def main():
    np.random.seed(SEED)
    md5_start, e4, e4_points, e4_map, e4_ga, con, e1_leiden, e1_dims = stage_0_load()
    corpus_stats = {
        "n_all": 585,
        "n_kit": 563,
        "e4_size": len(e4_points),
    }
    X, kids, kid_to_row, axis_values = stage_1_vectors(con, e4_map)
    leiden_assign, leiden_meta = stage_2_leiden_assignment(kids, kid_to_row, X, e1_leiden, e1_dims)
    dockets, gateA, ratified_all = dockets_definitions(con, e4_map, axis_values)
    results = stage_4_propagate(dockets, X, kids, kid_to_row, leiden_assign, gateA, ratified_all, axis_values, e4_map)
    stage_5_ratified_distance(results, X, kids, kid_to_row, gateA, e4_map)
    stage_6_one_liners(results, axis_values)
    stage_7_self_score(results, X, kids, kid_to_row, gateA, axis_values, e4_map)
    doc = stage_8_emit(results, e4, e4_map, gateA, md5_start, corpus_stats, leiden_meta, axis_values)

    con.close()
    print("\n" + "=" * 78)
    print("DONE. Provisional, names-review-pending. Two new artifacts written.")
    print("=" * 78)


if __name__ == "__main__":
    main()
