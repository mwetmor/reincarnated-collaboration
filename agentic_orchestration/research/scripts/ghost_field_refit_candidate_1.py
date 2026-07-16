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
# BUILD the refit ghost_field block.
# ===========================================================================
def build_ghost_field(db_conn, atlas_points=None):
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
                      "are L1' + L2 only. (drill_in omitted from this comparison artifact — the "
                      "decision surface is structural basis comparison, not the promoted-grain glyph "
                      "field; the v1.3 drill-in is unchanged and reproducible from ghost_field_edition2.)"),
        "feasible_cells": feasible_cells,
        "sealed_cells": sealed_cells,
    }
    return ghost


if __name__ == "__main__":
    import sqlite3, json
    DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
    con = sqlite3.connect(DB)
    g = build_ghost_field(con)
    con.close()
    d = g["denominators"]
    print("REFIT ghost field:")
    print("  MESO feasible:", d["meso_feasible"], "sealed:", d["meso_sealed"],
          "(L1", d["meso_sealed_L1"], "+ L2", d["meso_sealed_L2"], ")")
    print("  EXACT post-red-law:", d["exact_post_red_law"],
          "MATCH" if g["depth_sum_check"] == EXACT_POST_RED_LAW else "MISMATCH")
    print("  depth_sum_check:", g["depth_sum_check"])
    print("  lit cells:", g["lit_cells"], "| pull-lit:", g["pull_slice"]["lit_cells"],
          "| melee-lit:", g["melee_slice"]["lit_cells"])
    print("  unmapped:", g["unmapped_pending_curation"],
          "would-seal:", g["unmapped_would_seal_excluded"])
    print("  off-plane N:", g["off_plane_corpus"]["n"])
    print("  pull honest coords (n=%d):" % len(g["pull_honest_coords"]))
    for pc in g["pull_honest_coords"][:12]:
        print("     ", pc["core"], "(%.4f, %.4f)" % (pc["x"], pc["y"]), "LIT" if pc["lit"] else "")
