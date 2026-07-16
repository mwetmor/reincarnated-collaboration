#!/usr/bin/env python3
"""
ghost_field_refit_candidate_1.py — the ghost_field block for REFIT CANDIDATE 1.
==============================================================================
Fork of the ghost-field machinery (ghost_field_edition1/2/3) at the MACHINERY LEVEL. Edition-III
wraps Edition-II wraps Edition-I and reads the FROZEN Edition-I fit (atlas-frozen-fit-cellkeys-
edition1.csv, 469 rows). This module instead builds the fit from the REFIT's 628 active cell_keys
(refit-candidate-1-fit-cellkeys.csv, emitted by atlas_refit_candidate_2026_07_16.py) and projects
the SAME register v1.3 lattice through the NEW basis column-standard coordinates.

WHAT CHANGES vs the Edition-III ghost field (R3 of the elrond charge):
  1. FIT BASIS is the refit 628-active fit (NOT the frozen 469). New column-standard coordinates.
  2. PULL is UN-MASKED: REG2FIT["function"]["pull"] = "pull" (the refit fit HAS a `pull` function
     column — function=pull active n=10 >= FUSE_MIN, so it did not fuse). Its fit2reg image becomes
     REAL: pull meso cells now land at HONEST coordinates instead of projecting on their other 6
     core coords (masked-like). Reported: masked -> honest coordinate shift.
  3. MELEE is UN-MASKED likewise: REG2FIT["delivery"]["MELEE"] = "melee" (delivery=melee active
     n=31 >= FUSE_MIN earns a `melee` fit column). MELEE meso cells now land honestly; the MELEE
     ghost-image collapse (delivery=melee had NO meso ghost image in Edition-I/II/III) partially
     closes. Reported: unmapped/off-plane count change.
  4. The register v1.3 lattice DOES NOT MOVE. Denominators (exact 767,411,820 / meso 11,160 /
     sealed 1,314 / pull slice 1,080 feasible + 54 sealed) are asserted BYTE-IDENTICAL to v1.3.
     Un-masking changes WHERE cells land, not HOW MANY exist (the SPACE is unchanged; only the FIT
     projection of the SPACE changes).
  5. Lit census read LIVE from the (unchanged, post-normalize) corpus.db.

Author: elrond (data steward). TOOL script (curation/enumeration), not engine code. Imported by
build_atlas_refit_candidate_1_json.py. Logged in research/curated/MIGRATION.md.
"""

import os
import sys
import csv
import itertools
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_refit_candidate_2026_07_16 as pipe   # the refit pipeline (build_indicator, mca_greenacre)
import ghost_field_edition2 as gf2                 # reuse v1.2/v1.3 lattice predicates + drill-in + pull slice
import ghost_field_edition1 as gf1                 # reuse fit2reg crosswalks + depth-by-delivery

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
REFIT_FIT_CSV = os.path.join(ATLAS_DIR, "refit-candidate-1-fit-cellkeys.csv")

NAMES = pipe.NAMES
MASK = pipe.MASK
FUSE_MIN = pipe.FUSE_MIN
OTHER_RARE = pipe.OTHER_RARE

GHOST_FIELD_VERSION = "refit-candidate-1"
REGISTER_REF = "feasibility-cuts-register-v1.3"   # lattice UNCHANGED — v1.3, byte-identical denominators

CORE = gf1.CORE
CK_IDX = gf1.CK_IDX

# ---- register-meso ABSTRACT vocabulary (same as Edition-II/III: function includes `pull`) ----
REG = dict(gf2.REG)   # includes the +pull function level; delivery includes MELEE

# ---- register -> FIT column crosswalk — REFIT: pull + MELEE UN-MASKED (they earn fit columns) ----
REG2FIT = {k: dict(v) for k, v in gf1.REG2FIT.items()}
REG2FIT["function"]["pull"] = "pull"     # UN-MASK: the refit fit has a `pull` function column
REG2FIT["delivery"]["MELEE"] = "melee"   # UN-MASK: the refit fit has a `melee` delivery column

# v1.3 denominators the refit lattice must reproduce byte-identically (the SPACE did not move).
EXACT_POST_RED_LAW = gf2.EXACT_POST_RED_LAW      # 767,411,820
EXACT_POST_LOGICAL = gf2.EXACT_POST_LOGICAL      # 819,439,740
EXACT_RAW_NAIVE = gf2.EXACT_RAW_NAIVE            # 990,186,120
MESO_FEASIBLE = gf2.MESO_FEASIBLE                # 11,160
MESO_SEALED = gf2.MESO_SEALED                    # 1,314
PULL_MESO_FEASIBLE = 1080
PULL_MESO_SEALED = 54


# ===========================================================================
# REFIT FIT reconstruction — build the 628-active basis (NOT the frozen 469).
# ===========================================================================
def build_refit_fit():
    """Build the refit fit column-standard coordinates from the 628 active cell_keys, using the SAME
    MCA machinery (build_indicator + mca_greenacre + Greenacre fusing at FUSE_MIN) the derivation used.
    Returns the same dict shape gf1.build_frozen_fit() returns so the projection helpers work verbatim."""
    if not os.path.exists(REFIT_FIT_CSV):
        raise FileNotFoundError(
            "refit fit-cellkeys snapshot missing: %s — run atlas_refit_candidate_2026_07_16.py first."
            % REFIT_FIT_CSV)
    keys = []
    with open(REFIT_FIT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            keys.append((row["kit_id"], row["cell_key"].split("|")))
    kit_vals = [k[1] for k in keys]
    n = len(kit_vals)

    # Greenacre fusing map — IDENTICAL rule to the derivation (n<FUSE_MIN fuses per coord).
    fuse_map = {}
    for i in range(14):
        c = Counter(v[i] for v in kit_vals if v[i] not in MASK)
        for lv, cnt in c.items():
            if cnt < FUSE_MIN:
                fuse_map[(i, lv)] = OTHER_RARE

    def apply_fuse(vals):
        return [vals[i] if vals[i] in MASK else fuse_map.get((i, vals[i]), vals[i]) for i in range(14)]

    kit_fused = [apply_fuse(v) for v in kit_vals]
    Z, cm, block_of_col, first_sv = pipe.build_indicator(kit_fused, block_weight=True)
    mca = pipe.mca_greenacre(Z, cm)
    sv = mca["sv"]

    # retained dims — READ from the refit basis draft (parallel-analysis outcome), so the ghost field
    # uses the SAME retained-dim count the derivation retained (NOT a hard-coded 14).
    nret = _read_refit_nret()
    col_std = mca["col_pc"][:, :nret] / sv[:nret][None, :]
    colidx = {lvl: i for i, lvl in enumerate(cm)}
    return dict(col_std=col_std, colidx=colidx, block_of_col=block_of_col,
                first_sv=first_sv, apply_fuse=apply_fuse, fuse_map=fuse_map, nret=nret,
                ncols=Z.shape[1], n_active=n)


def _read_refit_nret():
    import json
    p = os.path.join(ATLAS_DIR, "refit-candidate-1-basis-draft.json")
    with open(p) as f:
        return int(json.load(f)["retained_dims"])


# ===========================================================================
# Meso projection through the REFIT basis (pull + MELEE now project HONESTLY).
# ===========================================================================
def project_meso_cell(cell, fit):
    """Project a register-meso cell into the REFIT basis via the CA supplementary transition formula.
    Uses the REFIT REG2FIT (pull -> 'pull', MELEE -> 'melee' — honest columns now). Absent core levels
    (SUMMON/hybrid/silence -> None) still contribute nothing (masked-like)."""
    col_std, colidx, block_of_col, first_sv = (fit["col_std"], fit["colidx"],
                                               fit["block_of_col"], fit["first_sv"])
    row = np.zeros(fit["ncols"])
    present = 0
    for coord in CORE:
        fitlvl = REG2FIT[coord][cell[coord]]
        if fitlvl is None:
            continue
        # apply fuse if the fit fused this level (e.g. a level that dropped below FUSE_MIN in the 628 fit)
        fj = fit["fuse_map"].get((NAMES.index(coord), fitlvl))
        lookup = fj if fj is not None else fitlvl
        j = colidx.get((coord, lookup))
        if j is None:
            continue
        row[j] = 1.0 / first_sv[block_of_col[j]]
        present += 1
    rt = row.sum()
    if rt <= 0:
        return None, None, 0
    rowp = row / rt
    coord = np.zeros(fit["nret"])
    for j in range(len(row)):
        if rowp[j] != 0:
            coord += rowp[j] * col_std[j]
    return float(coord[0]), float(coord[1]), present


# ===========================================================================
# LIT-MAPPING — map LIVE corpus kits to register-meso cells (refit REG; pull in-vocab, MELEE honest).
# ===========================================================================
def fit2reg_direct2(v, coord):
    return v if v in REG[coord] else None


def lit_map(db_conn):
    rows = db_conn.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL ORDER BY k.kit_id"
    ).fetchall()
    counts = {}
    unmapped = []
    unmapped_would_seal = []
    lit_pull_cells = set()
    lit_melee_cells = set()
    for kid, ck in rows:
        f = ck.split("|")
        geometry = f[3]
        core = {
            "movement": gf1.fit2reg_movement(f[CK_IDX["movement"]]),
            "delivery": gf1.fit2reg_delivery(f[CK_IDX["delivery"]], geometry, f[CK_IDX["proxy"]]),
            "treatment": fit2reg_direct2(f[CK_IDX["treatment"]], "treatment"),
            "function": fit2reg_direct2(f[CK_IDX["function"]], "function"),
            "proxy": fit2reg_direct2(f[CK_IDX["proxy"]], "proxy"),
            "activation": fit2reg_direct2(f[CK_IDX["activation"]], "activation"),
            "dependency": fit2reg_direct2(f[CK_IDX["dependency"]], "dependency"),
        }
        if any(v is None for v in core.values()):
            unmapped.append(kid)
            continue
        if not gf2.meso_feasible(core):
            unmapped_would_seal.append(kid)
            continue
        key = tuple(core[c] for c in CORE)
        counts[key] = counts.get(key, 0) + 1
        if core["function"] == "pull":
            lit_pull_cells.add(key)
        if core["delivery"] == "MELEE":
            lit_melee_cells.add(key)
    return counts, unmapped, unmapped_would_seal, lit_pull_cells, lit_melee_cells


# ===========================================================================
# PLANE-ALIGNMENT (item A' — gandalf verify-gate ruling). Q = optimal orthogonal 2x2 map
# (rotation+reflection, NO scaling, NO translation) refit-plane -> Edition-I-plane, computed on the
# 469 shared actives. Applied ATOMICALLY to EVERY emitted plane coordinate so points/loadings-plane-
# coords/ghost-cells/drill-in/hull/p_df_1 all carry the SAME Q (the ruling's internal-consistency
# law). A direction vector d transforms as d @ Q as well (projections s = p·d are invariant since
# (pQ)·(dQ) = p·d for orthogonal Q), so S_max / K_max / verdict are Q-INVARIANT; only the emitted
# coordinate presentation rotates. Source of Q = axis_sign_alignment_refit_candidate_1_2026_07_16.py
# (single source; the emitter + comparison script import the identical Q).
# ===========================================================================
def _apply_Q(x, y, Q):
    if Q is None:
        return x, y
    v = np.array([x, y]) @ Q
    return float(v[0]), float(v[1])


# ===========================================================================
# EAST-HALF geometry×commit DRILL-IN (R3-ADDENDUM item B). Ported from ghost_field_edition2 VERBATIM
# in mechanics; the ONLY differences are (a) it consults the REFIT REG2FIT (pull/MELEE un-masked) and
# REFIT fit, so the promoted geometry vocabulary AUTO-FOLLOWS the refit fit (gains `aura`: 13 vs 12
# levels), and (b) coordinates are aligned by Q. The region pin, RED-3 seal law, local-first law,
# glyph-field binning, and hull machinery are IDENTICAL. Region pin "EAST-half (projected x>=0;
# PERFORM side)" is applied to the ALIGNED x (meaningful only post-alignment, per the ruling).
# ===========================================================================
DRILLIN_RENDER_BIN_DP = gf2.DRILLIN_RENDER_BIN_DP          # 2 — identical render-grid resolution
MOVE_VERB_GEOMS_FITVOCAB = gf2.MOVE_VERB_GEOMS_FITVOCAB    # {dash_attack} — identical RED-3 geometry class


def promoted_levels(fit):
    """The promoted-level vocabularies = the REFIT fit's geometry + commit column levels (auto-follows
    the refit fit -> gains `aura`). instant is the CA baseline; append only if fused-out (it is NOT in
    the refit -> already present, guard won't fire). Identical logic to gf2.promoted_levels."""
    geos = sorted({lvl for (coord, lvl) in fit["colidx"] if coord == "geometry"})
    commits = sorted({lvl for (coord, lvl) in fit["colidx"] if coord == "commit"})
    if "instant" not in commits:
        commits = commits + ["instant"]
    return geos, commits


def drillin_cut_id(geometry, commit):
    """Sub-cell seal cause at the PROMOTED (geometry×commit) grain — IDENTICAL law + convention to
    gf2: RED-3- surfaces iff geometry in move-verb set {dash_attack} AND commit != instant."""
    if geometry in MOVE_VERB_GEOMS_FITVOCAB and commit != "instant":
        return "RED-3-movement-damage-carveout"
    return None


def project_subcell(cell, geometry, commit, fit):
    """Project a drill-in sub-cell (7 core levels + promoted geometry + commit) via the SAME CA
    supplementary transition formula, through the REFIT basis. RAW (pre-Q) plane coord; Q applied by
    the caller. Mirrors gf2.project_subcell but reads the refit REG2FIT + refit fuse_map."""
    col_std, colidx, block_of_col, first_sv = (fit["col_std"], fit["colidx"],
                                               fit["block_of_col"], fit["first_sv"])
    row = np.zeros(fit["ncols"])
    for coord in CORE:
        fitlvl = REG2FIT[coord][cell[coord]]
        if fitlvl is None:
            continue
        fj = fit["fuse_map"].get((NAMES.index(coord), fitlvl))
        lookup = fj if fj is not None else fitlvl
        j = colidx.get((coord, lookup))
        if j is None:
            continue
        row[j] = 1.0 / first_sv[block_of_col[j]]
    jg = colidx.get(("geometry", geometry))
    if jg is not None:
        row[jg] = 1.0 / first_sv[block_of_col[jg]]
    jc = colidx.get(("commit", commit))
    if jc is not None:
        row[jc] = 1.0 / first_sv[block_of_col[jc]]
    rt = row.sum()
    if rt <= 0:
        return None, None
    rowp = row / rt
    coord = np.zeros(fit["nret"])
    for j in range(len(row)):
        if rowp[j] != 0:
            coord += rowp[j] * col_std[j]
    return float(coord[0]), float(coord[1])


def build_drill_in(fit, feasible_cells, Q=None):
    """EAST-half (ALIGNED x>=0) geometry×commit drill-in. Emission form IDENTICAL to gf2.build_drill_in
    (exact counts + seal breakdown + reach hull + render-grid glyph field + pattern seal ledger +
    _full_sub_feasible for P-DF-1). Differences: refit fit/vocab (aura promotes), aligned coords, and
    the EAST region is pinned on the ALIGNED x. Every emitted coordinate is Q-applied.

    IMPORTANT: feasible_cells carry ALIGNED x/y (Q already applied in build_ghost_field). The EAST pin
    reads that aligned x. Sub-cell projections are computed RAW then Q-applied here, so ALL drill-in
    coords share the one Q with the parent field + points."""
    from scipy.spatial import ConvexHull as _CH
    geos, commits = promoted_levels(fit)
    east_cells = [c for c in feasible_cells if c["x"] >= 0.0]   # ALIGNED x (post-Q) — PERFORM side
    full_sub_feasible = []      # ALIGNED (x,y) for P-DF-1 + hull (not serialized)
    n_sub_sealed = 0
    sealed_pattern = {}
    for c in east_cells:
        cell = dict(zip(CORE, c["core"]))
        for g in geos:
            for cm in commits:
                cut = drillin_cut_id(g, cm)
                if cut is not None:
                    n_sub_sealed += 1
                    sealed_pattern[(g, cm, cut)] = sealed_pattern.get((g, cm, cut), 0) + 1
                    continue
                x, y = project_subcell(cell, g, cm, fit)
                if x is None:
                    continue
                xa, ya = _apply_Q(x, y, Q)
                full_sub_feasible.append((round(xa, 8), round(ya, 8)))

    xy = np.array(full_sub_feasible)
    hull = _CH(xy)
    hull_vertices = [[float(xy[v][0]), float(xy[v][1])] for v in hull.vertices]

    binned = {}
    for x, y in full_sub_feasible:
        k = (round(x, DRILLIN_RENDER_BIN_DP), round(y, DRILLIN_RENDER_BIN_DP))
        binned[k] = binned.get(k, 0) + 1
    glyph_field = [{"x": k[0], "y": k[1], "multiplicity": v} for k, v in sorted(binned.items())]

    seal_ledger = [{"geometry": g, "commit": cm, "cut_id": cut, "count": n}
                   for (g, cm, cut), n in sorted(sealed_pattern.items())]

    block = {
        "region": "EAST-half (projected x>=0; PERFORM side) — slate #1 ES + #2 EN (one drill-in serves both)",
        "promoted_pair": ["geometry", "commit"],
        "promoted_geometry_levels": geos,
        "promoted_commit_levels": commits,
        "local_first_law": ("EAST-half only; Edition-wide promotion is ~21x the glyph field and "
                            "unvettable in one pass (interaction law). Expansion only on a scored "
                            "P-DF-1 + a NEW pre-registered slate. Alternate WN-inner logged, unfired."),
        "seal_enum": ["L1-treatment-function-coherence", "L2-summon-implies-proxy",
                      "RED-3-movement-damage-carveout"],
        "red3_surfaces_here": ("RED-3' (geometry∈move-verb {dash_attack} × commit≠instant) is netted-out "
                               "of meso depth; at the PROMOTED geometry×commit grain it SURFACES as visible "
                               "RED-3- sub-cell seals — and ONLY here."),
        "n_east_parent_cells": len(east_cells),
        "n_sub_feasible": len(full_sub_feasible),
        "n_sub_sealed": n_sub_sealed,
        "sub_feasible_hull_reach": hull_vertices,
        "sub_feasible_hull_n_vertices": len(hull_vertices),
        "sub_feasible_glyph_field": glyph_field,
        "sub_feasible_glyph_field_bin_dp": DRILLIN_RENDER_BIN_DP,
        "sub_feasible_glyph_field_n_distinct": len(glyph_field),
        "sub_sealed_ledger": seal_ledger,
        "emission_note": ("The full n_sub_feasible enumeration is dense + coincident-heavy; it renders "
                          "as dark GROUND (a field), coincident glyphs aggregated per §9.1. The JSON "
                          "carries the render-grid glyph field (distinct @2dp + multiplicity) + reach "
                          "hull; the FULL enumeration is reproducible from ghost_field_refit_candidate_1. "
                          "Sealed sub-cells render as a chrome ledger (pattern), never on-plane (§9.2.4). "
                          "All coordinates are plane_alignment Q-applied (aligned frame)."),
        "_full_sub_feasible": full_sub_feasible,   # ALIGNED; for P-DF-1 (stripped before serialization)
    }
    return block


# ===========================================================================
# P-DF-1 scoring (R3-ADDENDUM item C). û construction VERBATIM against the REFIT loadings:
# û = normalize(mean(c_whirlwind, c_channel)) on (x,y) from the refit column-standard coords. Both
# referenced columns are present in the refit fit (verified) -> the construction runs; NO vocabulary
# HALT. Q-consistency: û is a DIRECTION, so it is aligned as û @ Q; the feasible-cell + point coords
# fed here are ALREADY aligned -> all projections live in the one aligned frame. S_max/K_max/verdict
# are Q-invariant; only the emitted u_direction + S_argmax coords rotate.
# ===========================================================================
_feasible_cache = None   # module-level cache of the ALIGNED feasible ghost positions (P-DF-1 hull)


def score_pdf1(fit, drill_in, atlas_points, Q=None):
    colidx, col_std = fit["colidx"], fit["col_std"]
    j_whirl = colidx.get(("geometry", "whirlwind"))
    j_chan = colidx.get(("commit", "channel"))
    if j_whirl is None or j_chan is None:
        # verbatim-construction guard: referenced column absent/fused -> HALT + surface (never substitute)
        raise RuntimeError(
            "P-DF-1 û construction cannot run VERBATIM on the refit vocabulary: "
            "geometry/whirlwind present=%s, commit/channel present=%s. HALT (do not improvise a column)."
            % (j_whirl is not None, j_chan is not None))
    c_whirl = np.array(col_std[j_whirl][:2])
    c_chan = np.array(col_std[j_chan][:2])
    u_raw = (c_whirl + c_chan) / 2.0
    u_raw = u_raw / np.hypot(*u_raw)
    # align the DIRECTION into the same frame as the (already-aligned) points/cells: û_aligned = û @ Q
    u = np.array(_apply_Q(u_raw[0], u_raw[1], Q)) if Q is not None else u_raw

    # S_max over ALL drill-in sub-feasible cells (aligned coords; the full enumeration)
    full = drill_in["_full_sub_feasible"]        # ALIGNED (x,y)
    s_vals = [x * u[0] + y * u[1] for (x, y) in full]
    s_max = float(max(s_vals)) if s_vals else float("-inf")
    s_argmax = None
    if s_vals:
        i = int(np.argmax(s_vals))
        s_argmax = {"x": full[i][0], "y": full[i][1]}

    # beyond-horizon kits: active points OUTSIDE the ALIGNED ghost hull (_feasible_cache is aligned).
    from scipy.spatial import ConvexHull
    ghost_xy = np.array([[c["x"], c["y"]] for c in _feasible_cache])
    hull = ConvexHull(ghost_xy)

    def inside_hull(p):
        return np.all(hull.equations[:, :2] @ p + hull.equations[:, 2] <= 1e-9)

    bh_projs = []
    for p in atlas_points:
        if p.get("supplementary"):
            continue
        pt = np.array([p["x"], p["y"]])   # atlas_points are ALIGNED (emitter applied Q before calling)
        if not inside_hull(pt):
            bh_projs.append(float(np.dot(pt, u)))
    k_max = float(max(bh_projs)) if bh_projs else float("-inf")
    verdict = "PASS" if s_max > k_max else "FAIL"
    return {
        "prediction": "P-DF-1",
        "statement": ("EAST drill-in (geometry×commit) extends the dark BEYOND the whirlwind/beam "
                      "kits along û=normalize(mean(c_whirlwind, c_channel))."),
        "u_direction": [float(u[0]), float(u[1])],
        "S_max": round(s_max, 8),
        "S_argmax": s_argmax,
        "K_max_beyond_horizon": round(k_max, 8),
        "n_beyond_horizon_kits": len(bh_projs),
        "verdict": verdict,
        "falsified": verdict == "FAIL",
        "consequence_if_falsified": ("INTERIOR-1 re-opens with new fuel (§9.4.4 trigger) — SURFACE to "
                                     "Matt, never auto-fire."),
    }


# ===========================================================================
# BUILD the refit ghost_field block.
# ===========================================================================
def build_ghost_field(db_conn, atlas_points=None, Q=None):
    global _feasible_cache
    fit = build_refit_fit()
    depth_by_delivery = gf1.build_depth_by_delivery()
    lit_counts, unmapped, unmapped_would_seal, lit_pull_cells, lit_melee_cells = lit_map(db_conn)

    feasible_cells = []
    sealed_cells = []
    depth_sum = 0
    lit_total = 0
    lit_pull_total = 0
    lit_melee_total = 0
    # honest-vs-masked coordinate audit for pull + MELEE cells (the un-mask shift)
    pull_cell_coords = {}    # core-tuple -> (x,y)  honest refit coord
    melee_cell_coords = {}
    for combo in itertools.product(*[REG[c] for c in CORE]):
        cell = dict(zip(CORE, combo))
        core_tuple = list(combo)
        if gf2.meso_feasible(cell):
            x, y, present = project_meso_cell(cell, fit)
            x, y = _apply_Q(x, y, Q)   # plane_alignment: aligned frame (atomic Q, everywhere)
            key = tuple(combo)
            kc = lit_counts.get(key, 0)
            depth = depth_by_delivery[cell["delivery"]]
            depth_sum += depth
            lit = kc >= 1
            if lit:
                lit_total += 1
                if cell["function"] == "pull":
                    lit_pull_total += 1
                if cell["delivery"] == "MELEE":
                    lit_melee_total += 1
            if cell["function"] == "pull":
                pull_cell_coords[key] = (round(x, 8), round(y, 8))
            if cell["delivery"] == "MELEE":
                melee_cell_coords[key] = (round(x, 8), round(y, 8))
            feasible_cells.append({
                "core": core_tuple, "x": round(x, 8), "y": round(y, 8),
                "lit": lit, "kit_count": kc, "depth": depth,
            })
        else:
            sealed_cells.append({"core": core_tuple, "cut_id": gf2.meso_cut_id(cell)})

    feasible_cells.sort(key=lambda c: c["core"])
    sealed_cells.sort(key=lambda c: c["core"])

    # ---- BYTE-IDENTICAL lattice assertions (the SPACE did not move) ----
    assert len(feasible_cells) == MESO_FEASIBLE, \
        "meso_feasible %d != v1.3 %d — lattice moved (BUG)" % (len(feasible_cells), MESO_FEASIBLE)
    assert len(sealed_cells) == MESO_SEALED, \
        "meso_sealed %d != v1.3 %d — lattice moved (BUG)" % (len(sealed_cells), MESO_SEALED)
    assert depth_sum == EXACT_POST_RED_LAW, \
        "depth_sum %d != v1.3 exact %d — lattice moved (BUG)" % (depth_sum, EXACT_POST_RED_LAW)

    sealed_L1 = sum(1 for c in sealed_cells if c["cut_id"] == "L1-treatment-function-coherence")
    sealed_L2 = sum(1 for c in sealed_cells if c["cut_id"] == "L2-summon-implies-proxy")

    off_plane = gf2.off_plane_corpus(db_conn)

    # ---- R3-ADDENDUM item B: EAST-half drill-in (refit fit/vocab; ALIGNED coords) ----
    # feasible_cells already carry ALIGNED x/y; drill-in reads that aligned x for the EAST pin and
    # aligns its own sub-cell projections with the SAME Q. _feasible_cache (aligned) drives P-DF-1 hull.
    _feasible_cache = feasible_cells
    drill_in = build_drill_in(fit, feasible_cells, Q=Q)

    # ---- R3-ADDENDUM item C: P-DF-1 re-score (verbatim û from refit loadings; aligned frame) ----
    pdf1 = None
    if atlas_points is not None:
        pdf1 = score_pdf1(fit, drill_in, atlas_points, Q=Q)
    # strip the P-DF-1-only full enumeration from the serialized block (the emitter is the
    # reproducible source of the full sub-cell set; the JSON carries glyph-field + hull).
    drill_in.pop("_full_sub_feasible", None)

    ghost = {
        "version": GHOST_FIELD_VERSION,
        "register_ref": REGISTER_REF,
        "edition": "Refit-Candidate-1",
        "unratified_comparison_artifact": True,
        "grain": "meso (never-demote core: movement, delivery, treatment, function, proxy, activation, dependency)",
        "core_order": CORE,
        "basis_ref": ("Refit-Candidate-1 (628-active fit; NOT frozen Edition-I). Ghosts are zero-mass "
                      "supplementary in the NEW basis — the refit axes were fit on the 628 actives, "
                      "then the lattice projects into them."),
        "refit_fit_input": "refit-candidate-1-fit-cellkeys.csv (628 active cell_keys)",
        "projection": ("CA supplementary transition formula F_sup(d)=sum_j rowp_j*col_std_j(d) through "
                       "the REFIT basis. pull + MELEE now have REAL fit columns (UN-MASKED); "
                       "SUMMON/hybrid/silence still masked-like (no fit column)."),
        "refit_change": ("pull UN-MASKED (function=pull earns a fit column, n=10>=FUSE_MIN) and MELEE "
                         "UN-MASKED (delivery=melee earns a fit column, n=31>=FUSE_MIN). The v1.3 "
                         "lattice is byte-identical (SPACE unchanged); only the FIT projection moved. "
                         "pull/MELEE meso cells now land at honest coordinates."),
        "denominators": {
            "exact_raw_naive": EXACT_RAW_NAIVE,
            "exact_post_logical": EXACT_POST_LOGICAL,
            "exact_post_red_law": EXACT_POST_RED_LAW,
            "meso_raw": len(feasible_cells) + len(sealed_cells),
            "meso_feasible": len(feasible_cells),
            "meso_sealed": len(sealed_cells),
            "meso_sealed_L1": sealed_L1,
            "meso_sealed_L2": sealed_L2,
            "register_v1_3_byte_identical": True,
            "note": ("v1.3 denominators asserted byte-identical: the refit changes the FIT layer only. "
                     "Un-masking pull/MELEE relocates their projected coordinates; it does not change "
                     "the lattice cardinality."),
        },
        "pull_slice": {
            "meso_total": PULL_MESO_FEASIBLE + PULL_MESO_SEALED, "meso_feasible": PULL_MESO_FEASIBLE,
            "meso_sealed": PULL_MESO_SEALED, "sealed_by_cut": {"L2-summon-implies-proxy": PULL_MESO_SEALED},
            "new_law_needed": 0, "halt": False,
            "lit_cells": lit_pull_total,
            "lit_pull_core_tuples": sorted([list(k) for k in lit_pull_cells]),
            "un_masked": True,
            "pull_now_honest": ("pull meso cells project on a REAL `pull` function column now (was "
                                "masked-like in Edition-I/II/III). See ghost_field.pull_honest_coords."),
        },
        "pull_honest_coords": [
            {"core": list(k), "x": v[0], "y": v[1], "lit": k in lit_pull_cells}
            for k, v in sorted(pull_cell_coords.items())],
        "melee_slice": {
            "un_masked": True,
            "lit_cells": lit_melee_total,
            "lit_melee_core_tuples": sorted([list(k) for k in lit_melee_cells]),
            "n_melee_feasible_cells": len(melee_cell_coords),
            "melee_now_honest": ("MELEE meso cells project on a REAL `melee` delivery column now (was "
                                 "masked-like -> NO meso ghost image in Edition-I/II/III). The MELEE "
                                 "ghost-image collapse partially closes. See melee_honest_coords."),
        },
        "melee_honest_coords_sample": [
            {"core": list(k), "x": v[0], "y": v[1], "lit": k in lit_melee_cells}
            for k, v in sorted(melee_cell_coords.items())][:40],
        "depth_by_delivery": depth_by_delivery,
        "depth_sum_check": depth_sum,
        "lit_cells": lit_total,
        "unmapped_pending_curation": len(unmapped),
        "unmapped_pending_curation_kits": sorted(unmapped),
        "unmapped_would_seal_excluded": len(unmapped_would_seal),
        "unmapped_would_seal_kits": sorted(unmapped_would_seal),
        "off_plane_corpus": off_plane,
        "red3_note": ("RED-3' seals live at GEOMETRY drill-in, not the meso plane. Meso SEALED cells "
                      "are L1' + L2 only. Depth badges already net out RED-3' within-cell. RED-3- "
                      "surfaces as VISIBLE sub-cell seals in the drill_in block (and only there) — "
                      "run VERBATIM against the refit fit (promoted geometry gains `aura`: 13 levels)."),
        "drill_in": drill_in,
        "feasible_cells": feasible_cells,
        "sealed_cells": sealed_cells,
    }
    if pdf1 is not None:
        ghost["p_df_1"] = pdf1
    ghost["plane_alignment"] = _plane_alignment_stamp(Q)
    return ghost


def _plane_alignment_stamp(Q):
    """The ruling's `plane_alignment` stamp (replaces the reflection-only `axis_sign_alignment`)."""
    import axis_sign_alignment_refit_candidate_1_2026_07_16 as align
    _, d = align.compute_Q()
    return {
        "method": "in-plane orthogonal Procrustes (rotation+reflection), no scaling, no translation",
        "Q": d["Q"],
        "rotation_deg": d["rotation_deg"],
        "det": d["det"],
        "raw_corr_before": d["raw_corr"],
        "corr_after": d["post_corr"],
        "raw_corr_before_diagonal_dominant": d["raw_diagonal_dominant"],
        "corr_after_diagonal_dominant": d["post_diagonal_dominant"],
        "raw_same_index_dim1": d["raw_same_index_dim1"],
        "raw_same_index_dim2": d["raw_same_index_dim2"],
        "raw_cross_E1d1_refit_d2": d["raw_cross_E1d1_refit_d2"],
        "shared_actives": d["shared_n"],
        "rationale": ("refit plane rotated ~117deg + reflected vs Edition-I; reflection-only "
                      "insufficient (raw dim1 same-index corr 0.045; raw matrix ANTI-diagonal "
                      "dominant). Aligned for plate comparability; disclosed on-plate + reported as "
                      "headline structure evidence. Distances/spreads/congruence/gates/plane-inertia "
                      "are Q-invariant; only the arbitrary MCA/SVD orientation convention changes. "
                      "Applied ATOMICALLY to every plane coordinate (points, ghost cells, drill-in, "
                      "hull, p_df_1, CSVs). The aligned dim2 tracks E1_dim2 only weakly (0.27, below "
                      "its off-diagonal 0.40) — the refit's 2nd axis does not survive the rotation "
                      "cleanly; disclosed, not smoothed."),
        "invariance_note": ("plane corrected-inertia 8.903% is a subspace property — invariant under "
                            "Q; the per-dim split (5.15/3.75) does NOT apply to the aligned x/y and is "
                            "NOT rendered per-axis. P-DF-1 is internally consistent because points, "
                            "loadings-plane-coords, cells, and hull all carry the SAME Q."),
        "source": "axis_sign_alignment_refit_candidate_1_2026_07_16.py (single source of Q)",
    }


if __name__ == "__main__":
    import sqlite3, csv as _csv
    import axis_sign_alignment_refit_candidate_1_2026_07_16 as align
    DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
    Q, _qd = align.compute_Q()   # single source of Q
    # load refit active points, ALIGN them (the emitter does the same before calling)
    pts = []
    with open(os.path.join(ATLAS_DIR, "refit-candidate-1-coordinates-active.csv"), newline="") as f:
        for row in _csv.DictReader(f):
            xa, ya = _apply_Q(float(row["dim1"]), float(row["dim2"]), Q)
            pts.append({"kit_id": row["kit_id"], "x": xa, "y": ya, "supplementary": False})
    con = sqlite3.connect(DB)
    g = build_ghost_field(con, atlas_points=pts, Q=Q)
    con.close()
    d = g["denominators"]
    print("REFIT ghost field (aligned frame; Q applied):")
    print("  MESO feasible:", d["meso_feasible"], "sealed:", d["meso_sealed"],
          "(L1", d["meso_sealed_L1"], "+ L2", d["meso_sealed_L2"], ")")
    print("  EXACT post-red-law:", d["exact_post_red_law"],
          "MATCH" if g["depth_sum_check"] == EXACT_POST_RED_LAW else "MISMATCH")
    print("  lit cells:", g["lit_cells"], "| pull-lit:", g["pull_slice"]["lit_cells"],
          "| melee-lit:", g["melee_slice"]["lit_cells"])
    print("  off-plane N:", g["off_plane_corpus"]["n"])
    pa = g["plane_alignment"]
    print("  plane_alignment: det=%s rot=%s post-diag-dominant=%s"
          % (pa["det"], pa["rotation_deg"], pa["corr_after_diagonal_dominant"]))
    di = g["drill_in"]
    print("  drill_in: EAST parents=%d sub-feasible=%d sub-sealed=%d | promoted_geometry=%d levels %s"
          % (di["n_east_parent_cells"], di["n_sub_feasible"], di["n_sub_sealed"],
             len(di["promoted_geometry_levels"]), di["promoted_geometry_levels"]))
    p = g["p_df_1"]
    print("  P-DF-1: %s  S_max=%.4f  K_max=%.4f  bh_kits=%d  u=%s"
          % (p["verdict"], p["S_max"], p["K_max_beyond_horizon"], p["n_beyond_horizon_kits"],
             [round(x, 4) for x in p["u_direction"]]))
