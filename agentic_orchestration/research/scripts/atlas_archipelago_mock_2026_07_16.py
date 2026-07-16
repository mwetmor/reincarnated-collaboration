#!/usr/bin/env python3
"""
Archipelago MOCK on Edition-I's 469 active kits — Part B of the elrond charge 2026-07-16.

THROWAWAY-CLASS EXHIBIT. Matt approved the archipelago strategy sight-unseen; this
mock shows what the territory surface looks like and answers his membership-census
question with real numbers. One JSON + one report. NOTHING SERVED, NOTHING VENDORED.
G1/G2/G3 ratification gates are NOT run (charter-run, pre-registered, later).
Emissions carry mock:true, ratified:false. Seating is designed-for-legibility;
memberships are computed. Both facts are disclosed IN the JSON and report.

Pipeline:
  0  CORPUS ASSERT (fail-loud, uses Part A's grain column): mock corpus = E1's 469
     active kits EXACTLY (the atlas-coordinates-active.csv membership). Assert all
     469 grain='kit'; assert zero mcd rows; report LA composition (expect 0). HALT
     if any gear/class-grain row is inside the 469.
  1  CLUSTER in FULL mechanical space (dim1..dim14 MCA coords from the E1 CSV — the
     retained-dims space, NOT the 2D plane). Method: Leiden-CPM consensus on kNN
     graph (k=10), the EXISTING atlas_derivation leiden_consensus machinery, at a
     disclosed resolution chosen for archipelago legibility. HDBSCAN was tried and
     REJECTED (degenerate: one giant cluster 65-72% of kits — the dense MCA core
     lumps; disclosed in report). Full resolution profile disclosed.
  2  FAMILY LABELS: seed from the 86 gateA ratified family labels (6 families).
     Label propagation (kNN vote in MCA space) to unlabeled kits with confidence
     threshold tau CALIBRATED on a ~20% gateA holdout (tau maximizes holdout
     assignment accuracy with abstention allowed). tau curve + holdout accuracy
     disclosed.
  3  FIVE-STRATA assignment for all 469 (+ ghost cells):
       CORE     tau-confident family member
       ISLET    cluster carrying NO gateA seed AND no member reaches tau -> U-1,U-2,..
       STRAIT   split affinity between two families within margin m (disclosed)
       DRIFTER  below-tau, no strong family match (the dense mainland + scatter)
       GHOST    feasible cells shaded by family affinity; shallows=family-adjacent
                frontier, deep=no family within affinity radius (the true frontier)
  4  SEATING (territory surface — memberships computed, seating designed-for-legibility):
       MDS on cluster centroids (full-space euclidean distances) -> island seats;
       within-island local layout (member offset from centroid, MDS-2D of members);
       water by fiat spacing; tombstones (negative kits) on their HOME island per
       Finding F-1 (kit death is not geography) — E1-469 has ZERO negative kits, so
       F-1 is honored vacuously (mechanism disclosed).
  5  EMIT atlas-archipelago-mock.json + archipelago-mock-report.md (FIRST table =
     the ashore/at-sea census).

Iron laws: no served artifact touched; no existing atlas artifact re-fit/re-emitted;
reads corpus.db (grain column, Part A) + the E1 coordinates CSV; writes only the two
new mock files. All randomness pinned to SEED.

Run:  python3 atlas_archipelago_mock_2026_07_16.py
"""
import os
import sys
import csv
import json
import sqlite3
import warnings
from collections import Counter, defaultdict

import numpy as np

warnings.filterwarnings("ignore")

CUR = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated"
SCRIPTS = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts"
DB = os.path.join(CUR, "corpus.db")
E1_CSV = os.path.join(CUR, "atlas", "atlas-coordinates-active.csv")
OUT_JSON = os.path.join(CUR, "atlas", "atlas-archipelago-mock.json")
OUT_MD = os.path.join(CUR, "atlas", "archipelago-mock-report.md")

sys.path.insert(0, SCRIPTS)

SEED = 20260716
np.random.seed(SEED)

# clustering + propagation hyperparameters (all disclosed in the report)
LEIDEN_K = 10                 # kNN graph degree (matches E1 pipeline)
LEIDEN_RES = 0.3              # CPM resolution — chosen for archipelago legibility (disclosed)
LEIDEN_SEEDS = 60             # consensus seeds
RES_PROFILE = [0.2, 0.3, 0.5, 0.8, 1.0]  # full resolution profile for disclosure
PROP_K = 5                    # kNN vote degree for family determination (which family, given admitted)
HOLDOUT_FRAC = 0.20           # gateA holdout fraction for tau calibration
# tau is an ABSOLUTE AFFINITY threshold: a kit is a core of family F iff its distance to the
# nearest same-family seed <= tau. This gates on genuine mechanical proximity (not mere vote
# plurality), so the mainland (far from every family) becomes drifters, not forced cores. The
# grid spans the empirical intra-family / non-seed distance regime (intra-family p90 ~1.0).
TAU_GRID = [round(0.10 * i, 2) for i in range(3, 21)]  # 0.30..2.00 (MCA-space euclidean)
STRAIT_MARGIN = 0.15          # m: nearest two families' affinity distances within this ratio -> strait
ISLET_MIN_SIZE = 3            # unseeded cluster must have >= this many members to be an islet;
                              # singletons + pairs adrift in unseeded space are drifters (a lone
                              # kit at sea is a drifter, not an island). Disclosed.
GHOST_RADIUS_QUANTILE = 0.90  # ghost affinity radius = this quantile of intra-family member distances

NAMED_FAMILIES = ["TOTEM-SENTRY", "TRAP-MINE", "WHIRLWIND", "CHANNELED-BEAM", "AURA", "MINION-PET"]


def stop(msg):
    print("\n*** HALT ***  " + msg)
    sys.exit(2)


# ============================================================================
# Stage 0 — corpus assert (fail-loud, uses Part A grain column)
# ============================================================================
def load_and_assert():
    rows = list(csv.DictReader(open(E1_CSV)))
    kids = [r["kit_id"] for r in rows]
    assert len(kids) == len(set(kids)) == 469, "E1 CSV not 469 unique kit_ids (got %d)" % len(kids)

    con = sqlite3.connect(DB)
    # grain column must exist (Part A)
    cols = {c[1] for c in con.execute("PRAGMA table_info(canon_corpus)").fetchall()}
    if "grain" not in cols:
        stop("grain column absent from canon_corpus — Part A must run first.")

    qs = ",".join("?" * len(kids))
    grain_dist = dict(con.execute(
        f"SELECT COALESCE(grain,'(NULL)'), COUNT(*) FROM canon_corpus WHERE kit_id IN ({qs}) GROUP BY 1", kids
    ).fetchall())
    mcd = con.execute(f"SELECT COUNT(*) FROM canon_corpus WHERE kit_id IN ({qs}) AND game='mcd'", kids).fetchone()[0]
    la = con.execute(f"SELECT COUNT(*) FROM canon_corpus WHERE kit_id IN ({qs}) AND game='la'", kids).fetchone()[0]
    non_kit = con.execute(
        f"SELECT kit_id, COALESCE(grain,'(NULL)') FROM canon_corpus WHERE kit_id IN ({qs}) "
        f"AND (grain IS NULL OR grain!='kit')", kids
    ).fetchall()

    print("=" * 70)
    print("STAGE 0 — CORPUS ASSERT (E1-469, grain column from Part A)")
    print("=" * 70)
    print(f"  E1 active kit_ids            : {len(kids)}")
    print(f"  grain distribution           : {grain_dist}")
    print(f"  mcd-source rows in the 469    : {mcd}  (expect 0)")
    print(f"  LA composition in the 469     : {la}  (expect 0 — post-E1 growth)")
    print(f"  non-kit-grain rows in the 469 : {len(non_kit)}  (expect 0)")

    # HALT if any gear/class-grain row inside the 469
    if non_kit:
        stop("gear/class-grain rows inside the E1-469: %s" % non_kit[:10])
    if mcd != 0:
        stop("mcd-source rows inside the E1-469 (%d)" % mcd)
    assert grain_dist.get("kit") == 469, "not all 469 are grain='kit': %s" % grain_dist
    con.close()

    dims = ["dim%d" % i for i in range(1, 15)]
    X = np.array([[float(r[d]) for d in dims] for r in rows], dtype=float)
    ga = [r["gateA_group"] if r["gateA_group"] else None for r in rows]
    e1_leiden = [r["leiden_cluster"] for r in rows]
    assert not np.isnan(X).any(), "NaN in MCA coordinates"
    return rows, kids, X, ga, e1_leiden, {"grain_dist": grain_dist, "mcd": mcd, "la": la}


# ============================================================================
# Stage 1 — cluster in full 14-dim MCA space (Leiden-CPM consensus, existing machinery)
# ============================================================================
def cluster(X):
    from scipy.spatial.distance import pdist, squareform
    import atlas_derivation_2026_07_14 as ad

    D = squareform(pdist(X, "euclidean"))
    D = D / D.max()
    N = X.shape[0]

    # full resolution profile (disclosure) — light seed count for the sweep
    profile = []
    for res in RES_PROFILE:
        prof = ad.leiden_consensus(D, LEIDEN_K, [res], 20, SEED)
        _, med_ncl, cons_ncl, cons = prof[0]
        sizes = sorted(Counter(cons).values(), reverse=True)
        biggest = sizes[0]
        profile.append({"resolution": res, "consensus_clusters": int(cons_ncl),
                        "biggest": int(biggest), "biggest_pct": round(100 * biggest / N, 1),
                        "top6": [int(s) for s in sizes[:6]]})

    # primary partition at LEIDEN_RES with full consensus seeds
    prof = ad.leiden_consensus(D, LEIDEN_K, [LEIDEN_RES], LEIDEN_SEEDS, SEED)
    labels = np.array(prof[0][3])
    n_clusters = len(set(labels))
    sizes = sorted(Counter(labels).values(), reverse=True)
    biggest_pct = 100 * sizes[0] / N

    print("\n" + "=" * 70)
    print("STAGE 1 — CLUSTER (Leiden-CPM consensus, full 14-dim MCA space)")
    print("=" * 70)
    print(f"  method            : Leiden-CPM consensus on kNN(k={LEIDEN_K}) graph, "
          f"{LEIDEN_SEEDS} seeds @ res={LEIDEN_RES}")
    print(f"  clusters          : {n_clusters}")
    print(f"  biggest cluster   : {sizes[0]} ({biggest_pct:.1f}%)")
    print(f"  resolution profile:")
    for p in profile:
        print(f"    res={p['resolution']}: clusters={p['consensus_clusters']:3d} "
              f"biggest={p['biggest']} ({p['biggest_pct']}%)")

    # HALT on degenerate clustering (one cluster > 60%)
    if biggest_pct > 60.0:
        stop(f"degenerate clustering — biggest cluster {biggest_pct:.1f}% > 60%")

    return labels, D, profile, {"n_clusters": n_clusters, "biggest": int(sizes[0]),
                                "biggest_pct": round(biggest_pct, 1)}


# ============================================================================
# Stage 2 — label propagation with tau calibrated on a gateA holdout
# ============================================================================
def _family_affinity(X, seed_idx, seed_lab, target_idx):
    """For each target kit, the distance to the nearest seed OF EACH FAMILY.
    Returns dict target_i -> {family: min_dist}. Affinity = mechanical proximity to a
    family's known members (NOT vote plurality) — the mainland is genuinely far from
    every family, so an absolute tau on this distance abstains it correctly."""
    from scipy.spatial.distance import cdist
    fams = sorted(set(seed_lab))
    fam_seed = {f: [seed_idx[j] for j in range(len(seed_idx)) if seed_lab[j] == f] for f in fams}
    out = {}
    for gi in target_idx:
        dmin = {}
        for f in fams:
            S = X[fam_seed[f]]
            dmin[f] = float(cdist(X[gi:gi + 1], S).min())
        out[gi] = dmin
    return out


def propagate(X, ga):
    seed_idx = np.array([i for i, g in enumerate(ga) if g is not None])
    seed_lab_full = np.array([ga[i] for i in seed_idx])
    n_seed = len(seed_idx)
    print("\n" + "=" * 70)
    print("STAGE 2 — AFFINITY LABELS + tau CALIBRATION (gateA holdout, absolute-distance tau)")
    print("=" * 70)
    print(f"  gateA seeds       : {n_seed}  {dict(Counter(seed_lab_full))}")

    # --- stratified ~20% holdout ---
    rng = np.random.RandomState(SEED)
    holdout_mask = np.zeros(n_seed, dtype=bool)
    for fam in sorted(set(seed_lab_full)):   # sorted: set-iteration order is hash-randomized
        fam_pos = np.where(seed_lab_full == fam)[0]
        n_hold = max(1, int(round(HOLDOUT_FRAC * len(fam_pos))))
        chosen = rng.choice(fam_pos, size=n_hold, replace=False)
        holdout_mask[chosen] = True
    train_pos = ~holdout_mask
    train_idx = seed_idx[train_pos]
    train_lab = seed_lab_full[train_pos]
    hold_idx = seed_idx[holdout_mask]
    hold_true = seed_lab_full[holdout_mask]
    print(f"  holdout           : {len(hold_idx)} / {n_seed} "
          f"({100*len(hold_idx)/n_seed:.0f}%), stratified by family")

    # affinity of the holdout to TRAIN-only family seeds
    hold_aff = _family_affinity(X, train_idx, train_lab, list(hold_idx))
    # NEGATIVE control: non-seed mainland kits (far cloud) — a good tau must REJECT most of these.
    non_seed_idx = np.array([i for i in range(X.shape[0]) if ga[i] is None])
    neg_aff = _family_affinity(X, train_idx, train_lab, list(non_seed_idx))

    # tau curve: at each tau, a holdout kit is ADMITTED iff its nearest-family affinity <= tau.
    #   TP  = admitted AND nearest family == true family (recall of true members)
    #   FN  = abstained true member (coverage loss)
    #   accuracy = of admitted holdout, fraction whose nearest family is the TRUE family
    #   coverage = admitted / holdout
    #   mainland_admit = fraction of non-seed mainland admitted (the false-core cost — want LOW)
    # chosen tau maximizes  accuracy * coverage * (1 - mainland_admit_rate)  (all in [0,1]).
    tau_curve = []
    best_tau, best_score = TAU_GRID[0], -1.0
    n_neg = len(non_seed_idx)
    for tau in TAU_GRID:
        admitted = correct = 0
        for hi, htrue in zip(hold_idx, hold_true):
            near_fam = min(hold_aff[hi], key=hold_aff[hi].get)
            if hold_aff[hi][near_fam] <= tau:
                admitted += 1
                if near_fam == htrue:
                    correct += 1
        acc = (correct / admitted) if admitted else 0.0
        cov = admitted / len(hold_idx)
        mainland_admit = sum(1 for i in non_seed_idx
                             if min(neg_aff[i].values()) <= tau) / n_neg
        score = acc * cov * (1.0 - mainland_admit)
        tau_curve.append({"tau": tau, "admitted": admitted, "accuracy": round(acc, 3),
                          "coverage": round(cov, 3), "mainland_admit_rate": round(mainland_admit, 3),
                          "score": round(score, 3)})
        if score > best_score:
            best_score, best_tau = score, tau
    chosen_tau = best_tau
    chosen_row = next(r for r in tau_curve if r["tau"] == chosen_tau)
    print(f"  tau curve (admit iff nearest-family affinity <= tau):")
    for r in tau_curve:
        mark = "  <== chosen" if r["tau"] == chosen_tau else ""
        print(f"    tau={r['tau']:.2f}: admit={r['admitted']:2d}/{len(hold_idx)} "
              f"acc={r['accuracy']:.3f} cov={r['coverage']:.3f} "
              f"mainland_admit={r['mainland_admit_rate']:.3f} score={r['score']:.3f}{mark}")
    print(f"  CHOSEN tau        : {chosen_tau}  (holdout accuracy {chosen_row['accuracy']:.3f}, "
          f"coverage {chosen_row['coverage']:.3f}, mainland_admit {chosen_row['mainland_admit_rate']:.3f})")

    # --- final affinity: ALL seeds define families; every non-seed kit gets per-family affinity ---
    final_aff = _family_affinity(X, seed_idx, seed_lab_full, list(non_seed_idx))
    prop = {}
    for i in range(X.shape[0]):
        if ga[i] is not None:
            prop[i] = {"family": ga[i], "affinity": 0.0, "second_affinity": None,
                       "source": "gateA-seed", "per_family": {ga[i]: 0.0}}
        else:
            aff = final_aff[i]
            ranked = sorted(aff.items(), key=lambda kv: kv[1])
            best_fam, best_d = ranked[0]
            second_d = ranked[1][1] if len(ranked) > 1 else None
            prop[i] = {"family": best_fam, "affinity": round(best_d, 4),
                       "second_family": ranked[1][0] if len(ranked) > 1 else None,
                       "second_affinity": round(second_d, 4) if second_d is not None else None,
                       "source": "affinity", "per_family": {k: round(v, 4) for k, v in aff.items()}}
    return prop, {
        "n_seed": int(n_seed), "holdout_n": int(len(hold_idx)),
        "holdout_accuracy": chosen_row["accuracy"], "holdout_coverage": chosen_row["coverage"],
        "holdout_mainland_admit": chosen_row["mainland_admit_rate"],
        "chosen_tau": chosen_tau, "tau_curve": tau_curve,
        "tau_semantics": "absolute distance in MCA space to nearest same-family gateA seed",
        "seed_family_counts": {k: int(v) for k, v in Counter(seed_lab_full).items()},
    }


# ============================================================================
# Stage 3 — five-strata assignment
# ============================================================================
def assign_strata(rows, X, labels, ga, prop, tau):
    N = X.shape[0]
    # cluster -> set of gateA seed families it carries
    clust_seed_fams = defaultdict(Counter)
    for i in range(N):
        if ga[i] is not None:
            clust_seed_fams[labels[i]][ga[i]] += 1
    seeded_clusters = set(clust_seed_fams.keys())

    strata = {}   # kit_id -> dict(stratum, family, ...)
    islet_map = {}  # cluster -> U-n label
    islet_counter = 0

    for i in range(N):
        kid = rows[i]["kit_id"]
        c = int(labels[i])
        p = prop[i]

        if p["source"] == "gateA-seed":
            strata[kid] = {"stratum": "core", "family": p["family"], "affinity": 0.0,
                           "cluster": c, "seed": True}
            continue

        aff = p["affinity"]                     # distance to nearest family
        fam = p["family"]
        second_fam = p.get("second_family")
        second_aff = p.get("second_affinity")
        # STRAIT: within tau of the nearest family AND the two nearest families are within
        # margin m of each other (relative): (second - nearest) / nearest <= m. Contested boundary.
        contested = (second_aff is not None and aff > 0
                     and (second_aff - aff) / aff <= STRAIT_MARGIN)

        if aff <= tau and contested and second_aff <= tau:
            strata[kid] = {"stratum": "strait", "family": None, "between": [fam, second_fam],
                           "affinity": round(aff, 3), "second": round(second_aff, 3), "cluster": c}
        elif aff <= tau:
            strata[kid] = {"stratum": "core", "family": fam, "affinity": round(aff, 3),
                           "cluster": c, "seed": False}
        else:
            # beyond tau of EVERY family: ISLET if in an unseeded cluster; else DRIFTER (mainland)
            if c not in seeded_clusters:
                if c not in islet_map:
                    islet_counter += 1
                    islet_map[c] = "U-%d" % islet_counter
                strata[kid] = {"stratum": "islet", "family": None, "islet": islet_map[c],
                               "nearest_family": fam, "affinity": round(aff, 3), "cluster": c}
            else:
                strata[kid] = {"stratum": "drifter", "family": None, "nearest_family": fam,
                               "affinity": round(aff, 3), "cluster": c}

    # An islet is a COHERENT unseeded cluster. Demote to drifter when:
    #   (a) the cluster has >=1 tau-core member (it is a seeded-family FRINGE, not a pure islet), OR
    #   (b) the cluster is below ISLET_MIN_SIZE (a lone/tiny fragment adrift is a drifter, not land).
    cluster_size = Counter(int(labels[i]) for i in range(N))
    cluster_has_core = defaultdict(bool)
    for kid, s in strata.items():
        if s["stratum"] == "core":
            cluster_has_core[s["cluster"]] = True
    reassigned_fringe = reassigned_tiny = 0
    for kid, s in strata.items():
        if s["stratum"] == "islet":
            if cluster_has_core[s["cluster"]]:
                s["stratum"] = "drifter"
                s.pop("islet", None)
                reassigned_fringe += 1
            elif cluster_size[s["cluster"]] < ISLET_MIN_SIZE:
                s["stratum"] = "drifter"
                s.pop("islet", None)
                reassigned_tiny += 1
    reassigned = reassigned_fringe + reassigned_tiny
    # recompute islet labels contiguously after reassignment (largest islet = U-1, deterministic)
    live_islet_clusters = sorted({s["cluster"] for s in strata.values() if s["stratum"] == "islet"},
                                 key=lambda c: (-cluster_size[c], c))
    relabel = {c: "U-%d" % (n + 1) for n, c in enumerate(live_islet_clusters)}
    for s in strata.values():
        if s["stratum"] == "islet":
            s["islet"] = relabel[s["cluster"]]

    census = Counter(s["stratum"] for s in strata.values())
    print("\n" + "=" * 70)
    print("STAGE 3 — FIVE-STRATA ASSIGNMENT")
    print("=" * 70)
    print(f"  cores    : {census['core']}")
    print(f"  islets   : {census['islet']}  (in {len(live_islet_clusters)} unseeded clusters: "
          f"{sorted(set(relabel.values()))})")
    print(f"  straits  : {census['strait']}")
    print(f"  drifters : {census['drifter']}")
    # per-family core sizes
    fam_core = Counter(s["family"] for s in strata.values() if s["stratum"] == "core")
    print(f"  per-family CORE sizes:")
    for f in NAMED_FAMILIES:
        print(f"    {f:16s} {fam_core.get(f,0)}")
    return strata, {"census": dict(census), "family_core_sizes": dict(fam_core),
                    "islet_clusters": {relabel[c]: int(c) for c in live_islet_clusters},
                    "islet_sizes": {relabel[c]: int(cluster_size[c]) for c in live_islet_clusters},
                    "islet_reassigned_to_drifter": reassigned,
                    "reassigned_fringe": reassigned_fringe, "reassigned_tiny": reassigned_tiny,
                    "islet_min_size": ISLET_MIN_SIZE,
                    "seeded_clusters": sorted(int(c) for c in seeded_clusters)}


# ============================================================================
# Stage 3b — ghost cells (shallows vs deep by family affinity) — MOCK approximation
# ============================================================================
def ghost_cells(rows, X, strata):
    """Mock family-affinity ghost census. The full charter ghost-field projects the
    11,160-cell meso-lattice (Edition-scoped, read-only). For the E1-469 MOCK we
    compute a lightweight affinity census over the 469 kits' OWN occupied cell
    footprint: a feasible-adjacent region is 'shallow' if within an affinity radius
    of a family centroid, 'deep' if beyond all family radii. Disclosed as a mock
    approximation, NOT the charter ghost field."""
    from scipy.spatial.distance import cdist
    # family centroids in MCA space (from cores)
    fam_members = defaultdict(list)
    for i, r in enumerate(rows):
        s = strata[r["kit_id"]]
        if s["stratum"] == "core":
            fam_members[s["family"]].append(i)
    centroids = {f: X[idx].mean(axis=0) for f, idx in fam_members.items() if idx}
    # affinity radius per family = quantile of member-to-centroid distances
    radii = {}
    for f, idx in fam_members.items():
        if len(idx) >= 2:
            dists = np.linalg.norm(X[idx] - centroids[f], axis=1)
            radii[f] = float(np.quantile(dists, GHOST_RADIUS_QUANTILE))
        elif idx:
            radii[f] = float(np.linalg.norm(X[idx] - centroids[f], axis=1).max()) or 0.1

    # ghost "cells": we shade the occupied meso footprint of the 469 as the frontier grid.
    # Approximate the frontier by the DRIFTER + ISLET kits (the unclaimed territory) and ask,
    # for each, whether it falls within any family radius (shallow) or beyond all (deep).
    frontier_idx = [i for i, r in enumerate(rows)
                    if strata[r["kit_id"]]["stratum"] in ("drifter", "islet")]
    fam_names = sorted(centroids.keys())   # sorted for deterministic tie-breaking in argmin
    C = np.array([centroids[f] for f in fam_names])
    R = np.array([radii[f] for f in fam_names])
    shallow = deep = 0
    ghost_by_family = Counter()
    Dfront = cdist(X[frontier_idx], C) if frontier_idx else np.zeros((0, len(fam_names)))
    for ti in range(len(frontier_idx)):
        within = Dfront[ti] <= R
        if within.any():
            shallow += 1
            nearest = fam_names[int(np.argmin(Dfront[ti] / np.where(R > 0, R, 1e-9)))]
            ghost_by_family[nearest] += 1
        else:
            deep += 1
    print("\n" + "=" * 70)
    print("STAGE 3b — GHOST CELLS (family-affinity shading, MOCK approximation)")
    print("=" * 70)
    print(f"  frontier cells (drifter+islet): {len(frontier_idx)}")
    print(f"  shallows (within a family radius): {shallow}")
    print(f"  deep (beyond ALL family radii — the frontier): {deep}")
    print(f"  shallow-by-nearest-family: {dict(ghost_by_family)}")
    return {"frontier_cells": len(frontier_idx), "shallows": shallow, "deep": deep,
            "shallow_by_family": {k: int(v) for k, v in ghost_by_family.items()},
            "affinity_radii": {k: round(v, 4) for k, v in radii.items()},
            "radius_quantile": GHOST_RADIUS_QUANTILE,
            "method_note": ("MOCK approximation over the 469 kits' own unclaimed (drifter+islet) "
                            "footprint; NOT the charter 11,160-cell meso ghost-field projection "
                            "(that is Edition-scoped + read-only).")}


# ============================================================================
# Stage 4 — seating (MDS on cluster centroids; within-island local layout; water by fiat)
# ============================================================================
def seat(rows, X, labels, strata, prop):
    from sklearn.manifold import MDS
    from scipy.spatial.distance import pdist, squareform

    N = X.shape[0]
    # island identity for seating: named-family islands (6) + islets (U-n). Cores/straits/drifters
    # seat relative to their family/islet; drifters with a nearest family float near that island's
    # shallows. We seat by CLUSTER CENTROID MDS then group clusters into islands by family.
    clusters = sorted(set(int(c) for c in labels))
    cluster_centroid = {c: X[labels == c].mean(axis=0) for c in clusters}
    Cmat = np.array([cluster_centroid[c] for c in clusters])
    Dc = squareform(pdist(Cmat, "euclidean"))
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=SEED, n_init=4,
              normalized_stress="auto")
    cluster_xy = mds.fit_transform(Dc)
    # scale to a legible canvas with water-by-fiat margin
    cluster_xy = cluster_xy - cluster_xy.mean(axis=0)
    span = np.abs(cluster_xy).max() or 1.0
    cluster_xy = cluster_xy / span * 100.0  # canvas ~[-100,100]
    cluster_seat = {c: cluster_xy[i] for i, c in enumerate(clusters)}

    # within-island local layout: member offset via 2D MDS of the members inside each cluster
    seats = {}
    for c in clusters:
        members = [i for i in range(N) if labels[i] == c]
        base = cluster_seat[c]
        if len(members) >= 3:
            Xm = X[members]
            Dm = squareform(pdist(Xm, "euclidean"))
            if Dm.max() > 0:
                m2 = MDS(n_components=2, dissimilarity="precomputed", random_state=SEED,
                         n_init=2, normalized_stress="auto").fit_transform(Dm)
                m2 = m2 - m2.mean(axis=0)
                loc_span = np.abs(m2).max() or 1.0
                m2 = m2 / loc_span * 6.0  # local island radius ~6 units (water by fiat between islands)
            else:
                m2 = np.zeros((len(members), 2))
        else:
            # tiny cluster: jitter deterministically
            rng = np.random.RandomState(SEED + c)
            m2 = rng.uniform(-2, 2, size=(len(members), 2))
        for j, i in enumerate(members):
            seats[i] = (float(base[0] + m2[j][0]), float(base[1] + m2[j][1]))

    print("\n" + "=" * 70)
    print("STAGE 4 — SEATING (MDS on cluster centroids; local layout; water by fiat)")
    print("=" * 70)
    print(f"  clusters seated   : {len(clusters)}")
    print(f"  MDS stress        : {mds.stress_:.4f}")
    print(f"  canvas            : ~[-100,100] x [-100,100], local island radius ~6")

    # island seats = named-family + islet anchor positions (mean of member seats per island)
    island_seats = {}
    # named-family island position = mean seat of its cores
    fam_seat_pts = defaultdict(list)
    islet_seat_pts = defaultdict(list)
    for i in range(N):
        s = strata[rows[i]["kit_id"]]
        if s["stratum"] == "core":
            fam_seat_pts[s["family"]].append(seats[i])
        elif s["stratum"] == "islet":
            islet_seat_pts[s["islet"]].append(seats[i])
    for f, pts in fam_seat_pts.items():
        arr = np.array(pts)
        island_seats[f] = {"type": "named-island", "x": float(arr[:, 0].mean()),
                           "y": float(arr[:, 1].mean()), "n_cores": len(pts)}
    for u, pts in islet_seat_pts.items():
        arr = np.array(pts)
        island_seats[u] = {"type": "islet", "x": float(arr[:, 0].mean()),
                           "y": float(arr[:, 1].mean()), "n": len(pts)}

    return seats, island_seats, {"n_clusters_seated": len(clusters),
                                 "mds_stress": round(float(mds.stress_), 4)}


# ============================================================================
# Stage 5 — emit JSON + report
# ============================================================================
def emit(rows, kids, X, labels, strata, prop, seats, island_seats,
         assert_info, cluster_meta, cluster_profile, prop_meta, strata_meta, ghost, seat_meta):
    # tombstones (negative kits) — E1-469 has zero; F-1 honored vacuously
    con = sqlite3.connect(DB)
    qs = ",".join("?" * len(kids))
    neg = [r[0] for r in con.execute(
        f"SELECT kit_id FROM canon_corpus WHERE kit_id IN ({qs}) AND negative=1", kids).fetchall()]
    con.close()

    points = []
    for i, r in enumerate(rows):
        kid = r["kit_id"]
        s = strata[kid]
        pt = {
            "kit_id": kid,
            "cluster": int(labels[i]),
            "seat": {"x": round(seats[i][0], 3), "y": round(seats[i][1], 3)},
            "stratum": s["stratum"],
            "family": s.get("family"),
            "affinity": s.get("affinity"),
            "e1_gateA_group": r["gateA_group"] or None,
            "e1_leiden_cluster": r["leiden_cluster"],
            "franchise_rollup": r.get("franchise_rollup") or None,
        }
        if s["stratum"] == "islet":
            pt["islet"] = s["islet"]
            pt["nearest_family"] = s.get("nearest_family")
        if s["stratum"] == "strait":
            pt["between"] = s.get("between")
            pt["second_affinity"] = s.get("second")
        if s["stratum"] == "drifter":
            pt["nearest_family"] = s.get("nearest_family")
        if s.get("seed"):
            pt["gateA_seed"] = True
        if kid in neg:
            pt["tombstone"] = True
        points.append(pt)

    census = strata_meta["census"]
    ashore = census.get("core", 0)
    at_sea = census.get("drifter", 0)
    islet_n = census.get("islet", 0)
    strait_n = census.get("strait", 0)

    doc = {
        "artifact": "atlas-archipelago-mock",
        "mock": True,
        "ratified": False,
        "disclosure": ("THROWAWAY MOCK. Memberships are COMPUTED (clustering + label propagation "
                       "in full 14-dim MCA space); island SEATING is DESIGNED-FOR-LEGIBILITY (MDS "
                       "on cluster centroids + within-island local layout + water by fiat), NOT a "
                       "measured coordinate. G1/G2/G3 ratification gates NOT run (charter-run, "
                       "pre-registered, later). Nothing served, nothing vendored."),
        "generated": "2026-07-16",
        "generator": "agentic_orchestration/research/scripts/atlas_archipelago_mock_2026_07_16.py",
        "corpus": {
            "set": "Edition-I 469 active kits (atlas-coordinates-active.csv membership)",
            "grain_assert": {"all_kit_grain": assert_info["grain_dist"].get("kit") == 469,
                             "grain_distribution": assert_info["grain_dist"],
                             "mcd_rows": assert_info["mcd"], "la_rows": assert_info["la"],
                             "note": "kit-grain-clean by construction; mcd + LA are post-E1 growth"},
            "seed": SEED,
        },
        "clustering": {
            "space": "full 14-dim MCA coordinates (dim1..dim14 from E1 CSV) — retained-dims space, NOT the 2D plane",
            "method": f"Leiden-CPM consensus on kNN(k={LEIDEN_K}) graph, {LEIDEN_SEEDS} seeds @ resolution {LEIDEN_RES}",
            "n_clusters": cluster_meta["n_clusters"],
            "biggest_cluster_pct": cluster_meta["biggest_pct"],
            "resolution_profile": cluster_profile,
            "hdbscan_rejected": ("HDBSCAN tried on the same space; produced a degenerate giant "
                                 "cluster (65-72% of kits at min_cluster_size 5-10) because the "
                                 "dense MCA core lumps. Rejected. Leiden-CPM partitions the core."),
        },
        "family_labels": {
            "seed_source": "86 gateA ratified family labels (atlas_gateA_labels_2026_07_14)",
            "families": NAMED_FAMILIES,
            "method": ("family = nearest gateA seed by family; core iff ABSOLUTE affinity (MCA-space "
                       "distance to nearest same-family seed) <= tau; mainland (far from all families) "
                       "abstains as drifters. Absolute-distance tau (not vote-share) is what makes the "
                       "mainland/family separation real."),
            "tau_calibration": prop_meta,
            "strait_margin_m": STRAIT_MARGIN,
        },
        "strata": {
            "definitions": {
                "core": "tau-confident family member (gateA seed OR propagated share>=tau)",
                "islet": "member of an unseeded cluster (no gateA seed, no core) — labeled U-n",
                "strait": f"split affinity between two families within margin m={STRAIT_MARGIN}",
                "drifter": "below-tau with no strong family match (dense mainland + scatter)",
                "ghost": "feasible cells shaded by family affinity; shallow=family-adjacent, deep=frontier",
            },
            "census": census,
            "family_core_sizes": strata_meta["family_core_sizes"],
            "islet_clusters": strata_meta["islet_clusters"],
            "islet_sizes": strata_meta["islet_sizes"],
            "islet_min_size": strata_meta["islet_min_size"],
            "reassigned_fringe_to_drifter": strata_meta["reassigned_fringe"],
            "reassigned_tiny_to_drifter": strata_meta["reassigned_tiny"],
            "seeded_clusters": strata_meta["seeded_clusters"],
        },
        "ghost_field": ghost,
        "seating": {
            "disclosure": "designed-for-legibility, NOT measured",
            "method": "MDS(2D) on cluster centroids (full-space euclidean) + within-island local MDS layout + water by fiat",
            "mds_stress": seat_meta["mds_stress"],
            "n_clusters_seated": seat_meta["n_clusters_seated"],
            "islands": island_seats,
            "tombstones": {"count": len(neg), "kit_ids": neg,
                           "finding_F1": ("tombstones seat on their HOME island (kit death is not "
                                          "geography); E1-469 has ZERO negative kits, so F-1 is "
                                          "honored vacuously — mechanism disclosed, no placement needed.")},
        },
        "census_headline": {
            "ashore_cores": ashore, "at_sea_drifters": at_sea,
            "islands_named": len([k for k in island_seats if island_seats[k]["type"] == "named-island"]),
            "islets": islet_n, "straits": strait_n,
            "ghost_shallows": ghost["shallows"], "ghost_deep": ghost["deep"],
            "total": len(points),
        },
        "points": points,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(doc, f, indent=2)
    print(f"\nWROTE {OUT_JSON}  ({os.path.getsize(OUT_JSON)} bytes, {len(points)} points)")
    write_report(doc, neg)
    return doc


def write_report(doc, neg):
    c = doc["census_headline"]
    fcs = doc["strata"]["family_core_sizes"]
    ghost = doc["ghost_field"]
    prop = doc["family_labels"]["tau_calibration"]
    # data-driven: how many distinct Leiden clusters each family's gateA SEEDS span
    fam_seed_clusters = defaultdict(set)
    for p in doc["points"]:
        if p.get("e1_gateA_group"):
            fam_seed_clusters[p["e1_gateA_group"]].add(p["cluster"])
    fam_spread = {f: len(fam_seed_clusters[f]) for f in NAMED_FAMILIES}
    archipelagic = sorted([f for f, n in fam_spread.items() if n >= 3], key=lambda f: -fam_spread[f])
    single_island = sorted([f for f, n in fam_spread.items() if n < 3], key=lambda f: -fam_spread[f])
    n_straits = c["straits"]
    largest_islet = None
    if doc["strata"]["islet_sizes"]:
        largest_islet = max(doc["strata"]["islet_sizes"].items(), key=lambda kv: kv[1])
    L = []
    A = L.append
    A("# Archipelago MOCK — Edition-I 469 kits — ashore/at-sea census + territory surface")
    A("")
    A("**Status:** MOCK · **ratified:** FALSE · **Date:** 2026-07-16 · **Author:** elrond (data steward)")
    A("**Charge:** `agentic_orchestration/gandalf/briefs/2026-07-16-elrond-grain-law-and-archipelago-mock-brief.md` (Part B)")
    A("**Authority:** Matt 2026-07-16 — *\"I do approve of the archipelago strategy.\"* (strategy approved sight-unseen; this mock buys the census with real numbers.)")
    A("**Generator:** `agentic_orchestration/research/scripts/atlas_archipelago_mock_2026_07_16.py` · **Seed:** %d" % SEED)
    A("")
    A("> **THROWAWAY-CLASS EXHIBIT — NOTHING SERVED, NOTHING VENDORED.** Memberships are **computed** "
      "(clustering + label propagation in full 14-dim MCA space). Island **seating is designed-for-legibility** "
      "(MDS on cluster centroids), **not a measured coordinate** — disclosed as such in the JSON. "
      "**G1/G2/G3 ratification gates are NOT run** in this mock (they are charter-run + pre-registered, later). "
      "Do not read this mock as ratified.")
    A("")
    A("## 1. ASHORE / AT-SEA CENSUS (the answer to Matt's membership question)")
    A("")
    A("| stratum | count | of 469 |")
    A("|---|---:|---:|")
    A("| **Islands (named six) — cores ashore** | %d | %.1f%% |" % (c["ashore_cores"], 100*c["ashore_cores"]/c["total"]))
    A("| **Islets (U-n, unnamed)** | %d | %.1f%% |" % (c["islets"], 100*c["islets"]/c["total"]))
    A("| **Straits (split family affinity)** | %d | %.1f%% |" % (c["straits"], 100*c["straits"]/c["total"]))
    A("| **Drifters (at sea — below-tau, no family)** | %d | %.1f%% |" % (c["at_sea_drifters"], 100*c["at_sea_drifters"]/c["total"]))
    A("| **TOTAL** | %d | 100%% |" % c["total"])
    A("")
    A("**Per-family CORE sizes (the six named islands):**")
    A("")
    A("| island (family) | core size |")
    A("|---|---:|")
    for f in NAMED_FAMILIES:
        A("| %s | %d |" % (f, fcs.get(f, 0)))
    A("| **named-island cores total** | %d |" % sum(fcs.values()))
    A("")
    A("**Ghost cells (frontier, family-affinity shaded — MOCK approximation):**")
    A("")
    A("| ghost stratum | cells |")
    A("|---|---:|")
    A("| shallows (within a family affinity radius) | %d |" % ghost["shallows"])
    A("| deep (beyond ALL family radii — the true frontier) | %d |" % ghost["deep"])
    A("| frontier cells total (drifter+islet footprint) | %d |" % ghost["frontier_cells"])
    A("")
    A("## 2. What the numbers say (survey-mode: what IS)")
    A("")
    A("- **The named six are minority coasts, not the mainland.** %d of 469 kits (%.0f%%) sit on a named "
      "family island as tau-confident cores; the bulk (%d drifters, %.0f%%) is the mechanically-generic "
      "mainland at sea — kits that resemble no gateA family strongly. This is the honest shape of the corpus: "
      "the distinctive families are peripheral minorities around a dense generic core."
      % (c["ashore_cores"], 100*c["ashore_cores"]/c["total"], c["at_sea_drifters"],
         100*c["at_sea_drifters"]/c["total"]))
    A("- **Some families are archipelagos, some are single islands.** Measured by how many distinct Leiden "
      "clusters each family's gateA seeds span: %s. The archipelagic families (%s) scatter their seeds across "
      "multiple sub-islands under one named territory; the single-island families (%s) concentrate in one (or "
      "nearly one) cluster."
      % (", ".join("%s=%d" % (f, fam_spread[f]) for f in NAMED_FAMILIES),
         ", ".join("%s(%d)" % (f, fam_spread[f]) for f in archipelagic) or "none",
         ", ".join("%s(%d)" % (f, fam_spread[f]) for f in single_island) or "none"))
    if n_straits == 0:
        A("- **No straits (0).** At margin m=%.2f, no kit sits between two families (2nd-nearest family within "
          "%.0f%% of the nearest, both within tau). The six gateA families are **mechanically well-separated** "
          "in MCA space — kits commit cleanly to one family. (Note: the gateA seeds of TOTEM-SENTRY and "
          "MINION-PET do share one Leiden cluster, so a *cluster-level* strait notion would fire there; but at "
          "*kit-level affinity* each kit is clearly closer to one family. The mock reports the kit-level result "
          "honestly rather than manufacture a strait.)" % (STRAIT_MARGIN, STRAIT_MARGIN*100))
    else:
        A("- **%d straits** — kits between two families within margin m=%.2f (the genuine boundary the strait "
          "stratum is for)." % (n_straits, STRAIT_MARGIN))
    A("- **%d islets (U-n)** in %d coherent unseeded clusters (size>=%d) carry no gateA seed and no tau-core — "
      "unnamed territory the gateA labeling never reached%s. They are the concrete candidates for the next round "
      "of family naming."
      % (c["islets"], len(doc["strata"]["islet_clusters"]), doc["strata"]["islet_min_size"],
         (" (largest: %s, %d kits)" % (largest_islet[0], largest_islet[1])) if largest_islet else ""))
    A("")
    A("## 3. Method (disclosed)")
    A("")
    A("**Corpus (Stage 0, fail-loud):** the mock corpus is Edition-I's 469 active kits, exactly the "
      "`atlas-coordinates-active.csv` membership. Asserted (via Part A's ratified `grain` column): "
      "all 469 `grain='kit'`; **zero mcd rows**; **LA composition = %d** (expected 0 — the 62 LA rows are "
      "post-E1 growth). Kit-grain-clean by construction; no HALT." % doc["corpus"]["grain_assert"]["la_rows"])
    A("")
    A("**Clustering (Stage 1):** full **14-dim MCA space** (`dim1..dim14` — the retained-dims space, NOT the "
      "2D plane). Method: **Leiden-CPM consensus** on a kNN(k=%d) graph, %d seeds @ resolution %.1f "
      "(the existing `atlas_derivation_2026_07_14.leiden_consensus` machinery). **%d clusters**, biggest "
      "%.1f%% (no degeneracy). Resolution profile:"
      % (LEIDEN_K, LEIDEN_SEEDS, LEIDEN_RES, doc["clustering"]["n_clusters"], doc["clustering"]["biggest_cluster_pct"]))
    A("")
    A("| resolution | clusters | biggest | biggest %% |")
    A("|---:|---:|---:|---:|")
    for p in doc["clustering"]["resolution_profile"]:
        mark = " **(chosen)**" if p["resolution"] == LEIDEN_RES else ""
        A("| %.1f%s | %d | %d | %.1f%% |" % (p["resolution"], mark, p["consensus_clusters"], p["biggest"], p["biggest_pct"]))
    A("")
    A("> **HDBSCAN was tried and REJECTED.** On the same 14-dim space it produced a **degenerate giant "
      "cluster (65-72%% of kits** at min_cluster_size 5-10), because the dense MCA core lumps into one blob "
      "and everything else becomes noise. That would trip the mock's own >60%% HALT. Leiden-CPM partitions "
      "the dense core into resolvable communities, which is what an archipelago needs. Disclosed per the brief.")
    A("")
    A("**Family labels + tau (Stage 2):** seeded from the **86 gateA ratified labels** (6 families). "
      "A kit's family = its nearest gateA seed by family; **tau is an ABSOLUTE affinity threshold** — "
      "distance in MCA space to the nearest same-family seed — so the mechanically-generic mainland (far "
      "from every family) is **abstained as drifters, not force-assigned** (this was the key fix: a "
      "vote-share tau admitted everything and flooded two families to 130-160 members; an absolute-distance "
      "tau produces a real archipelago). **tau calibrated on a stratified %.0f%% gateA holdout** (%d of %d "
      "seeds): tau maximizes accuracy x coverage x (1 - mainland-admit-rate) — the third factor is the "
      "false-core penalty that makes tau discriminating. **Chosen tau = %.2f**, holdout accuracy **%.3f**, "
      "coverage **%.3f**, mainland-admit-rate **%.3f**."
      % (HOLDOUT_FRAC*100, prop["holdout_n"], prop["n_seed"], prop["chosen_tau"],
         prop["holdout_accuracy"], prop["holdout_coverage"], prop["holdout_mainland_admit"]))
    A("")
    A("| tau | admit/holdout | accuracy | coverage | mainland-admit | score |")
    A("|---:|---:|---:|---:|---:|---:|")
    for r in prop["tau_curve"]:
        mark = " **<-- chosen**" if r["tau"] == prop["chosen_tau"] else ""
        A("| %.2f | %d/%d | %.3f | %.3f | %.3f | %.3f%s |" % (r["tau"], r["admitted"], prop["holdout_n"],
          r["accuracy"], r["coverage"], r["mainland_admit_rate"], r["score"], mark))
    A("")
    A("**Five strata (Stage 3):** core (affinity<=tau) / islet (coherent unseeded cluster, size>=%d, U-n) / "
      "strait (two families within m=%.2f AND both within tau) / drifter (below-tau, no family — the mainland) "
      "/ ghost (frontier). Islet discipline: an unseeded cluster is demoted to drifter if it gained tau-cores "
      "(a family **fringe**, not a pure islet — %d members) or is below size %d (a lone/tiny fragment adrift is "
      "a **drifter**, not land — %d members). U-n therefore means genuinely-unclaimed coherent territory; "
      "U-1 is the largest islet."
      % (doc["strata"]["islet_min_size"], STRAIT_MARGIN, doc["strata"]["reassigned_fringe_to_drifter"],
         doc["strata"]["islet_min_size"], doc["strata"]["reassigned_tiny_to_drifter"]))
    A("")
    A("**Ghost cells (Stage 3b, MOCK):** %s Shallows=%d (within a family affinity radius, %.0fth-percentile "
      "intra-family), deep=%d (beyond all — the true frontier)."
      % (ghost["method_note"], ghost["shallows"], ghost["radius_quantile"]*100, ghost["deep"]))
    A("")
    A("**Seating (Stage 4):** %s. MDS stress %.4f over %d cluster centroids. Islands seat at the mean of their "
      "cores; islets at the mean of their members; water by fiat between islands; local island radius ~6 units. "
      "**Tombstones:** E1-469 has **%d negative kits** — Finding F-1 (tombstones on their HOME island; kit death "
      "is not geography) is honored **vacuously**; the placement mechanism is disclosed but no tombstone needs seating."
      % (doc["seating"]["method"], doc["seating"]["mds_stress"], doc["seating"]["n_clusters_seated"], len(neg)))
    A("")
    A("## 4. Gates NOT run (say so plainly)")
    A("")
    A("**G1/G2/G3 ratification gates are NOT run in this mock.** They are charter-run and pre-registered, to "
      "fire later against a real (non-mock) archipelago derivation. This exhibit answers the *census* question "
      "with real numbers and shows the *shape* of the territory surface; it does **not** ratify anything. "
      "The seating is designed-for-legibility, not measured. Nothing here is served or vendored.")
    A("")
    A("## 5. Residual framings embedded for Matt to rule on concretely")
    A("")
    A("- **Two-surfaces identity:** memberships (computed, defensible) vs seating (designed, legibility-only). "
      "The mock keeps them separate and stamped; a ratified atlas would need to decide whether the archipelago "
      "*replaces* or *overlays* the plane surface.")
    A("- **Five-strata membership:** the census above is the concrete instance. Matt can now see whether "
      "core/islet/strait/drifter/ghost is the right vocabulary against real counts, or whether (e.g.) drifters "
      "at %.0f%% argue for a coarser family net or more seed labels." % (100*c["at_sea_drifters"]/c["total"]))
    A("")
    A("**Artifacts:** `atlas-archipelago-mock.json` (this dir) · this report. Both stamped `mock:true, ratified:false`.")
    A("")
    with open(OUT_MD, "w") as f:
        f.write("\n".join(L))
    print(f"WROTE {OUT_MD}")


def main():
    rows, kids, X, ga, e1_leiden, assert_info = load_and_assert()
    labels, D, cluster_profile, cluster_meta = cluster(X)
    prop, prop_meta = propagate(X, ga)
    tau = prop_meta["chosen_tau"]
    strata, strata_meta = assign_strata(rows, X, labels, ga, prop, tau)
    ghost = ghost_cells(rows, X, strata)
    seats, island_seats, seat_meta = seat(rows, X, labels, strata, prop)
    emit(rows, kids, X, labels, strata, prop, seats, island_seats,
         assert_info, cluster_meta, cluster_profile, prop_meta, strata_meta, ghost, seat_meta)
    print("\nDONE (MOCK — nothing served, nothing vendored).")


if __name__ == "__main__":
    main()
