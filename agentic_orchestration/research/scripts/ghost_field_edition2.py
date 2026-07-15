#!/usr/bin/env python3
"""
ghost_field_edition2.py — the atlas.json ghost_field block v2 (EDITION II).
==========================================================================
Edition II grows the LATTICE by one function level (`pull`), opens the first
promoted-grain ground (EAST-half geometry×commit drill-in), and re-emits the ghost
field + every denominator against register v1.2. The Edition-I FIT layer stays FROZEN
(14-dim basis, 506 point coords, tombstones, axis names, RIDER-1, F-1): this module
touches ONLY the lattice.

Author: elrond (data steward). TOOL script (curation/enumeration), not engine code.
Imported by build_atlas_json_edition2.py. Logged in research/curated/MIGRATION.md.

WHAT CHANGES vs ghost_field_edition1 (all lattice-side; basis untouched — decoupling law):
  1. REG["function"] gains `pull` (10 -> 11 levels). register v1.2.
  2. REG2FIT["function"]["pull"] = None — the FROZEN fit never saw `pull`, so it has NO
     column-standard coordinate. A pull cell projects on its OTHER 6 core coords
     (function masked-like, EXACTLY as silence/hybrid/MELEE/SUMMON are already handled).
     This is what keeps the basis byte-frozen: pull cannot bend an axis it was never fit on.
  3. Denominators re-derive to v1.2 (exact 767,411,820 / meso 11,160 / sealed 1,314;
     pull slice 1,080 feasible + 54 sealed, all L2). depth_by_delivery unchanged (non-core);
     depth_sum = Σ over 11,160 feasible = 767,411,820 exactly.
  4. NEW off-plane corpus disclosure: `off_plane_corpus` — the MCD gear-grain kits held
     out by the emitter gate (movement=blank / no engine-key row). N from gate rejections,
     never hard-coded (spec §10.4.4).
  5. NEW `drill_in` block: EAST-half geometry×commit sub-cells (slate #1+#2), RED-3'-vetted
     at the promoted grain -> grain-scoped seal enum {L1-, L2-, RED-3-}. Zero-mass
     supplementary ground; any frame-exit clip-discloses via the renderer's §9.2.3 machinery.

FROZEN-BASIS DISCIPLINE (unchanged from Edition-I): the fit reconstructs from the durable
  pre-C3 snapshot atlas-frozen-fit-cellkeys-edition1.csv; lighting uses the LIVE (post-C3 +
  post-Stage-3 pull re-key) corpus.db keys AT EMISSION TIME. Frozen frame, census-current lit.
"""

import os, sys, csv, itertools
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_derivation_2026_07_14 as pipe
import ghost_field_edition1 as gf1

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))

NAMES = pipe.NAMES
GHOST_FIELD_VERSION = "2.0"
REGISTER_REF = "feasibility-cuts-register-v1.2"

CORE = gf1.CORE
CK_IDX = gf1.CK_IDX

# Edition-II exact denominators (register v1.2 — independently re-derived, acceptance 22).
EXACT_RAW_NAIVE = 990186120
EXACT_POST_LOGICAL = 819439740
EXACT_POST_RED_LAW = 767411820
MESO_RAW = 12474
MESO_FEASIBLE = 11160
MESO_SEALED = 1314

# ---- register-meso ABSTRACT vocabulary (Edition-II: function +pull) ----
REG = dict(gf1.REG)
REG["function"] = list(gf1.REG["function"]) + ["pull"]   # 10 -> 11

# ---- register -> FIT column crosswalk (Edition-II: pull -> None, masked-like) ----
# pull is NOT in the frozen fit's function block -> None (absent core block; identical
# handling to silence/hybrid/MELEE/SUMMON). This preserves the frozen basis exactly.
REG2FIT = {k: dict(v) for k, v in gf1.REG2FIT.items()}
REG2FIT["function"]["pull"] = None


# ===========================================================================
# Feasibility predicates at MESO grain (v1.2: L1' + L2 bind here; pull inherits the
# ratified ledger with ZERO new laws — L1' cannot seal pull (pull != none); L2 seals
# SUMMON x solo x pull). Must match the register generator.
# ===========================================================================
def meso_feasible(cell):
    t, f = cell["treatment"], cell["function"]
    if t in ("control", "hybrid") and f == "none":      # L1'
        return False
    if cell["delivery"] == "SUMMON" and cell["proxy"] == "solo":  # L2
        return False
    return True


def meso_cut_id(cell):
    t, f = cell["treatment"], cell["function"]
    if t in ("control", "hybrid") and f == "none":
        return "L1-treatment-function-coherence"
    if cell["delivery"] == "SUMMON" and cell["proxy"] == "solo":
        return "L2-summon-implies-proxy"
    return None


# ===========================================================================
# LIT-MAPPING — reuse the Edition-I crosswalk verbatim, BUT with the Edition-II REG
# (so `pull` is now an in-vocab function value that lights via fit2reg_direct).
# gf1.fit2reg_direct reads gf1.REG; we must make it see the Edition-II function vocab.
# Cleanest: local direct-mapper that consults the Edition-II REG.
# ===========================================================================
def fit2reg_direct2(v, coord):
    if v in REG[coord]:
        return v
    return None


def lit_map(db_conn):
    rows = db_conn.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL ORDER BY k.kit_id"
    ).fetchall()
    counts = {}
    unmapped = []
    unmapped_would_seal = []
    lit_pull_cells = set()
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
        if not meso_feasible(core):
            unmapped_would_seal.append(kid)
            continue
        key = tuple(core[c] for c in CORE)
        counts[key] = counts.get(key, 0) + 1
        if core["function"] == "pull":
            lit_pull_cells.add(key)
    return counts, unmapped, unmapped_would_seal, lit_pull_cells


# ===========================================================================
# OFF-PLANE corpus disclosure (spec §10.4.4): kits the emitter GATE holds off the plane.
# The MCD gear-grain kits (mcd- prefix) carry movement=blank / have no engine-key row ->
# they cannot light a meso cell. N is COMPUTED from the gate, never hard-coded.
#   Gate-rejected off-plane set = combat-kit corpus rows whose engine-key row exists but
#   whose fit2reg_movement is None (movement=blank), PLUS mcd rows with no engine-key row.
#   Per the deferred docket the ledger line is about the mcd gear-grain kits specifically.
# ===========================================================================
def off_plane_corpus(db_conn):
    # (a) mcd rows with NO engine-key row (the 26 unresolved incl. 6 pull) — off-plane by
    #     construction (no cell_key). (b) mcd rows WITH an engine-key row but movement=blank
    #     (the 94 keyed gear kits) — off-plane by the movement gate.
    n_mcd_total = db_conn.execute(
        "SELECT COUNT(*) FROM canon_corpus WHERE game='mcd' AND negative=0").fetchone()[0]
    # keyed mcd combat-kit rows whose movement gate rejects (fit2reg_movement is None)
    keyed = db_conn.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE c.game='mcd' AND c.negative=0 AND k.row_class='combat-kit' AND k.cell_key IS NOT NULL"
    ).fetchall()
    gate_rejected = []
    for kid, ck in keyed:
        mv = gf1.fit2reg_movement(ck.split("|")[CK_IDX["movement"]])
        if mv is None:
            gate_rejected.append(kid)
    # unresolved mcd rows (no engine-key row)
    unresolved = [r[0] for r in db_conn.execute(
        "SELECT c.kit_id FROM canon_corpus c WHERE c.game='mcd' AND c.negative=0 "
        "AND c.kit_id NOT IN (SELECT kit_id FROM canon_engine_key)"
    ).fetchall()]
    # The DISCLOSURE N is the KEYED gear kits held off by the MOVEMENT GATE (spec §10.0/§10.4.4:
    # "the 94 MCD rows stay atlas-invisible" — "classless gear carries no movement identity at kit
    # grain" is EXACTLY the movement-blank reason, which applies to the keyed set). The unresolved
    # 26 are off-plane for a DIFFERENT reason (no key at all — thin-artifact / pending curation) and
    # are reported separately, not folded into the movement-identity disclosure N.
    disclosure_kits = sorted(gate_rejected)
    return {
        "n": len(disclosure_kits),                    # 94 — the movement-gate-held keyed gear kits
        "n_mcd_total": n_mcd_total,
        "gate_rejected_keyed": len(gate_rejected),
        "unresolved_no_key": len(unresolved),
        "unresolved_no_key_kits": sorted(unresolved),
        "kits": disclosure_kits,
        "disclosure": (f"{len(disclosure_kits)} gear-grain kits (mcd-) sit in the corpus off-plane — "
                       "classless gear carries no movement identity at kit grain; admission is a "
                       "deferred grain ruling."),
    }


# ===========================================================================
# EAST-HALF geometry×commit DRILL-IN (slate #1+#2; spec §10.3).
# ===========================================================================
# The promoted pair = geometry × commit. Sub-cells = feasible EAST-half meso cell × the
# fit-present geometry levels × the fit-present commit levels. A sub-cell projects with the
# 7 core levels PLUS the 2 promoted levels (so W includes 2 extra blocks -> renormalization
# over ~9 blocks, the memo's mechanism). Only geometry/commit levels PRESENT in the frozen
# fit column vocabulary can contribute (others masked-like). RED-3' vets at THIS grain:
#   geometry in move-verb-geoms {dash_attack, teleport} AND commit != instant -> SEAL (RED-3-).
#
# EAST-half = meso cells whose projected x >= 0 (PERFORM side). "local-first" law: EAST-half
# only; Edition-wide promotion is out of scope (~21x glyph field). Alternate WN-inner logged
# unfired in the slate.

# The promoted-level vocabularies = the frozen fit's geometry + commit column levels.
def promoted_levels(fit):
    geos = sorted({lvl for (coord, lvl) in fit["colidx"] if coord == "geometry"})
    commits = sorted({lvl for (coord, lvl) in fit["colidx"] if coord == "commit"})
    # commit reference level 'instant' is the CA baseline (fused-out of the column set); it is
    # a legitimate promoted value (masked-like -> contributes nothing, but names a real sub-cell).
    if "instant" not in commits:
        commits = commits + ["instant"]
    return geos, commits


# RED-3' movement-verb geometry class (curation-bound: {dash_attack, teleport}); the frozen
# fit fuses teleport into other-rare/absent, so at fit-vocab grain the observable member is
# dash_attack. RED-3' predicate at drill-in grain: geometry in this set AND commit != instant.
MOVE_VERB_GEOMS_FITVOCAB = {"dash_attack"}   # teleport not a distinct fit column (fused); dash_attack is


def drillin_cut_id(geometry, commit):
    """Sub-cell seal cause at the PROMOTED (geometry×commit) grain. RED-3- surfaces ONLY here."""
    if geometry in MOVE_VERB_GEOMS_FITVOCAB and commit != "instant":
        return "RED-3-movement-damage-carveout"
    return None  # feasible at this grain (L1/L2 already applied at the parent meso cell)


def project_subcell(cell, geometry, commit, fit):
    """Project a drill-in sub-cell: the 7 core levels + promoted geometry + commit, via the
    SAME CA supplementary transition formula. geometry/commit contribute ONLY if present in
    the frozen fit column vocabulary (else masked-like)."""
    col_std, colidx, block_of_col, first_sv = (fit["col_std"], fit["colidx"],
                                               fit["block_of_col"], fit["first_sv"])
    row = np.zeros(fit["ncols"])
    # 7 core levels (fit vocabulary; pull->None masked-like just like the meso cell)
    for coord in CORE:
        fitlvl = REG2FIT[coord][cell[coord]]
        if fitlvl is None:
            continue
        j = colidx.get((coord, fitlvl))
        if j is None:
            continue
        fj = fit["fuse_map"].get((NAMES.index(coord), fitlvl))
        if fj is not None:
            j = colidx.get((coord, fj))
            if j is None:
                continue
        row[j] = 1.0 / first_sv[block_of_col[j]]
    # promoted geometry
    jg = colidx.get(("geometry", geometry))
    if jg is not None:
        row[jg] = 1.0 / first_sv[block_of_col[jg]]
    # promoted commit
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


# Render-grid resolution for the drill-in glyph field. The full sub-cell enumeration
# (172,312 feasible) is dense and coincident-heavy; the renderer draws the drill-in as dark
# GROUND (a field), aggregating coincident glyphs per §9.1. We emit the field at a render-grid
# bin resolution (2dp on the frozen-basis coordinates) — the honest renderable glyph set — while
# the FULL set drives P-DF-1 (S_max over all sub-cells) and the reach hull. The full 172,312-cell
# enumeration is reproducible from this emitter (build_drill_in returns it internally).
DRILLIN_RENDER_BIN_DP = 2


def build_drill_in(fit, feasible_cells):
    """EAST-half (projected x>=0) geometry×commit drill-in. Returns the drill_in block.

    Emission form (steward decision, spec §10.4.1 intent + §9.1 coincident-aggregation +
    §10.3.3 ~21× glyph-field law + atlas.json practicality):
      - EXACT counts + seal breakdown (the ledger truth).
      - reach ENVELOPE (convex hull of ALL sub-feasible positions) — the renderable extended-dark
        boundary the P-DF-1 overshoot is about; hull recomputed, never constant.
      - render-grid glyph field: DISTINCT sub-feasible positions binned at 2dp with multiplicity
        (the field the renderer draws as ground).
      - seal LEDGER described by pattern (10,136 = EAST parents × dash_attack × {channel,wind-up},
        all RED-3-) — rendered as a chrome register, never on-plane (§9.2.4); NOT 10k raw rows.
      - the FULL sub-feasible list is returned under `_full_sub_feasible` for P-DF-1 scoring, and
        is NOT serialized into atlas.json (the emitter is the reproducible source of record).
    """
    import numpy as _np
    from scipy.spatial import ConvexHull as _CH
    geos, commits = promoted_levels(fit)
    east_cells = [c for c in feasible_cells if c["x"] >= 0.0]
    full_sub_feasible = []      # for P-DF-1 + hull (not serialized)
    n_sub_sealed = 0
    sealed_pattern = {}         # (geometry,commit,cut_id) -> count
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
                full_sub_feasible.append((round(x, 8), round(y, 8)))

    # reach hull (envelope) over ALL sub-feasible positions
    xy = _np.array(full_sub_feasible)
    hull = _CH(xy)
    hull_vertices = [[float(xy[v][0]), float(xy[v][1])] for v in hull.vertices]

    # render-grid glyph field: distinct positions @ bin resolution, with multiplicity
    binned = {}
    for x, y in full_sub_feasible:
        k = (round(x, DRILLIN_RENDER_BIN_DP), round(y, DRILLIN_RENDER_BIN_DP))
        binned[k] = binned.get(k, 0) + 1
    glyph_field = [{"x": k[0], "y": k[1], "multiplicity": v}
                   for k, v in sorted(binned.items())]

    # seal ledger (pattern, not raw rows)
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
                          "as dark GROUND (a field), coincident glyphs aggregated per §9.1. atlas.json "
                          "carries the render-grid glyph field (distinct @2dp + multiplicity) + reach "
                          "hull; the FULL enumeration is reproducible from ghost_field_edition2. Sealed "
                          "sub-cells render as a chrome ledger (pattern), never on-plane (§9.2.4)."),
        "_full_sub_feasible": full_sub_feasible,   # for P-DF-1 (stripped before serialization)
    }
    return block


# ===========================================================================
# P-DF-1 scoring (spec §10.5; displacement memo §5). Mechanical PASS/FAIL at render.
# ===========================================================================
def score_pdf1(fit, drill_in, atlas_points):
    """PASS iff max drill-in sub-cell projection along û (whirlwind+channel unit dir) exceeds
    the max beyond-horizon-kit projection along û. û = normalize(mean(c_whirlwind, c_channel))
    on (x,y) from the frozen loadings — content-locked (frozen loading ranks)."""
    colidx, col_std = fit["colidx"], fit["col_std"]
    j_whirl = colidx.get(("geometry", "whirlwind"))
    j_chan = colidx.get(("commit", "channel"))
    c_whirl = col_std[j_whirl][:2]
    c_chan = col_std[j_chan][:2]
    u = (c_whirl + c_chan) / 2.0
    u = u / np.hypot(*u)
    # S_max over ALL drill-in sub-feasible cells (the full enumeration, not the binned field)
    full = drill_in["_full_sub_feasible"]        # list of (x,y)
    s_vals = [x * u[0] + y * u[1] for (x, y) in full]
    s_max = float(max(s_vals)) if s_vals else float("-inf")
    s_argmax = None
    if s_vals:
        i = int(np.argmax(s_vals))
        s_argmax = {"x": full[i][0], "y": full[i][1]}
    # beyond-horizon kits: active points OUTSIDE the ghost hull. Recompute the hull + membership
    # here (single source; the renderer recomputes independently). We approximate the "beyond-
    # horizon set" projection ceiling by the max over ALL active points of the û-projection that
    # exceed the ghost feasible x-reach — but the memo's precise K_max is over the 14 beyond-
    # horizon kits. We compute K_max as max û-projection over active points strictly outside the
    # convex hull of the feasible ghost positions.
    from scipy.spatial import ConvexHull  # available in the pipe env
    ghost_xy = np.array([[c["x"], c["y"]] for c in _feasible_cache])
    hull = ConvexHull(ghost_xy)
    hull_pts = ghost_xy[hull.vertices]
    def inside_hull(p):
        # point-in-polygon via all half-plane tests using hull equations
        return np.all(hull.equations[:, :2] @ p + hull.equations[:, 2] <= 1e-9)
    bh_projs = []
    for p in atlas_points:
        if p.get("supplementary"):
            continue
        pt = np.array([p["x"], p["y"]])
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


# module-level cache for the feasible ghost positions (used by P-DF-1 hull)
_feasible_cache = None


# ===========================================================================
# BUILD the Edition-II ghost_field block.
# ===========================================================================
def build_ghost_field(db_conn, atlas_points=None):
    global _feasible_cache
    fit = gf1.build_frozen_fit()
    depth_by_delivery = gf1.build_depth_by_delivery()
    lit_counts, unmapped, unmapped_would_seal, lit_pull_cells = lit_map(db_conn)

    feasible_cells = []
    sealed_cells = []
    depth_sum = 0
    lit_total = 0
    lit_pull_total = 0
    for combo in itertools.product(*[REG[c] for c in CORE]):
        cell = dict(zip(CORE, combo))
        core_tuple = list(combo)
        if meso_feasible(cell):
            # project with the Edition-II REG2FIT (pull->None masked-like)
            x, y = _project_meso(cell, fit)
            key = tuple(combo)
            kc = lit_counts.get(key, 0)
            depth = depth_by_delivery[cell["delivery"]]
            depth_sum += depth
            lit = kc >= 1
            if lit:
                lit_total += 1
                if cell["function"] == "pull":
                    lit_pull_total += 1
            feasible_cells.append({
                "core": core_tuple, "x": round(x, 8), "y": round(y, 8),
                "lit": lit, "kit_count": kc, "depth": depth,
            })
        else:
            sealed_cells.append({"core": core_tuple, "cut_id": meso_cut_id(cell)})

    feasible_cells.sort(key=lambda c: c["core"])
    sealed_cells.sort(key=lambda c: c["core"])
    _feasible_cache = feasible_cells

    off_plane = off_plane_corpus(db_conn)
    drill_in = build_drill_in(fit, feasible_cells)

    pdf1 = None
    if atlas_points is not None:
        pdf1 = score_pdf1(fit, drill_in, atlas_points)
    # strip the P-DF-1-only full enumeration from the serialized block (emitter is the
    # reproducible source of the full 172,312-cell set; atlas.json carries glyph-field + hull).
    drill_in.pop("_full_sub_feasible", None)

    # sealed decomposition
    sealed_L1 = sum(1 for c in sealed_cells if c["cut_id"] == "L1-treatment-function-coherence")
    sealed_L2 = sum(1 for c in sealed_cells if c["cut_id"] == "L2-summon-implies-proxy")

    ghost = {
        "version": GHOST_FIELD_VERSION,
        "register_ref": REGISTER_REF,
        "edition": "II",
        "grain": "meso (never-demote core: movement, delivery, treatment, function, proxy, activation, dependency)",
        "core_order": CORE,
        "basis_ref": "Edition-I (frozen; ghosts are zero-mass supplementary — axes cannot move, decoupling law)",
        "frozen_fit_input": "atlas-frozen-fit-cellkeys-edition1.csv (pre-C3 snapshot; reproduces frozen active dim1/dim2 to 0.00)",
        "projection": ("CA supplementary transition formula F_sup(d)=sum_j rowp_j*col_std_j(d); "
                       "6+ core blocks in fit vocab; pull/silence/hybrid/MELEE/SUMMON have no fit "
                       "column -> masked-like (frozen basis preserved)."),
        "edition2_change": ("function coordinate 10 -> 11 levels (+`pull`). Law ledger unchanged; "
                            "pull vets under the ratified ledger with ZERO new laws (L1' cannot seal "
                            "pull; L2 seals SUMMON×solo×pull = 54)."),
        "denominators": {
            "exact_raw_naive": EXACT_RAW_NAIVE,
            "exact_post_logical": EXACT_POST_LOGICAL,
            "exact_post_red_law": EXACT_POST_RED_LAW,
            "meso_raw": len(feasible_cells) + len(sealed_cells),
            "meso_feasible": len(feasible_cells),
            "meso_sealed": len(sealed_cells),
            "meso_sealed_L1": sealed_L1,
            "meso_sealed_L2": sealed_L2,
            "superseded_edition1": {"exact_post_red_law": 693146160, "meso_feasible": 10080,
                                    "meso_sealed": 1260,
                                    "note": "Edition-I lineage strings — permitted only in labeled lineage copy."},
        },
        "pull_slice": {
            "meso_total": 1134, "meso_feasible": 1080, "meso_sealed": 54,
            "sealed_by_cut": {"L2-summon-implies-proxy": 54},
            "new_law_needed": 0, "halt": False,
            "lit_cells": lit_pull_total,
            "lit_pull_core_tuples": sorted([list(k) for k in lit_pull_cells]),
        },
        "depth_by_delivery": depth_by_delivery,
        "depth_sum_check": depth_sum,
        "lit_cells": lit_total,
        "unmapped_pending_curation": len(unmapped),
        "unmapped_pending_curation_kits": sorted(unmapped),
        "unmapped_would_seal_excluded": len(unmapped_would_seal),
        "unmapped_would_seal_kits": sorted(unmapped_would_seal),
        "off_plane_corpus": off_plane,
        "red3_note": ("RED-3' seals live at GEOMETRY drill-in, not the meso plane (geometry is a "
                      "demotable non-core coord). Meso SEALED cells are L1' + L2 only. Depth badges "
                      "already net out RED-3' within-cell. RED-3- surfaces as VISIBLE sub-cell seals "
                      "in the drill_in block (and only there)."),
        "drill_in": drill_in,
        "feasible_cells": feasible_cells,
        "sealed_cells": sealed_cells,
    }
    if pdf1 is not None:
        ghost["p_df_1"] = pdf1
    return ghost


def _project_meso(cell, fit):
    """Edition-II meso projection (pull->None masked-like). Mirrors gf1.project_meso_cell but
    reads the Edition-II REG2FIT."""
    col_std, colidx, block_of_col, first_sv = (fit["col_std"], fit["colidx"],
                                               fit["block_of_col"], fit["first_sv"])
    row = np.zeros(fit["ncols"])
    for coord in CORE:
        fitlvl = REG2FIT[coord][cell[coord]]
        if fitlvl is None:
            continue
        j = colidx.get((coord, fitlvl))
        if j is None:
            continue
        fj = fit["fuse_map"].get((NAMES.index(coord), fitlvl))
        if fj is not None:
            j = colidx.get((coord, fj))
            if j is None:
                continue
        row[j] = 1.0 / first_sv[block_of_col[j]]
    rt = row.sum()
    if rt <= 0:
        return None, None
    rowp = row / rt
    coord = np.zeros(fit["nret"])
    for j in range(len(row)):
        if rowp[j] != 0:
            coord += rowp[j] * col_std[j]
    return float(coord[0]), float(coord[1])


if __name__ == "__main__":
    import sqlite3, json
    DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
    ATLAS_JSON = os.path.join(ATLAS_DIR, "atlas.json")
    # load the FROZEN Edition-I points (for P-DF-1)
    with open(ATLAS_JSON) as f:
        pts = json.load(f)["points"]
    con = sqlite3.connect(DB)
    g = build_ghost_field(con, atlas_points=pts)
    con.close()
    d = g["denominators"]
    print("MESO feasible:", d["meso_feasible"], "sealed:", d["meso_sealed"], "raw:", d["meso_raw"],
          "(L1", d["meso_sealed_L1"], "+ L2", d["meso_sealed_L2"], ")")
    print("EXACT post-red-law:", d["exact_post_red_law"])
    print("depth_sum_check:", g["depth_sum_check"],
          "MATCH" if g["depth_sum_check"] == EXACT_POST_RED_LAW else "MISMATCH")
    print("lit cells:", g["lit_cells"], "| pull lit cells:", g["pull_slice"]["lit_cells"],
          "| pull lit tuples:", g["pull_slice"]["lit_pull_core_tuples"])
    print("off-plane N:", g["off_plane_corpus"]["n"], g["off_plane_corpus"]["disclosure"])
    print("drill-in EAST parents:", g["drill_in"]["n_east_parent_cells"],
          "sub-feasible:", g["drill_in"]["n_sub_feasible"],
          "sub-sealed(RED-3-):", g["drill_in"]["n_sub_sealed"])
    print("P-DF-1:", g["p_df_1"]["verdict"], "S_max", g["p_df_1"]["S_max"],
          "K_max", g["p_df_1"]["K_max_beyond_horizon"], "bh_kits", g["p_df_1"]["n_beyond_horizon_kits"])
