#!/usr/bin/env python3
r"""
displacement_field_edition1.py — the DISPLACEMENT FIELD over the frozen Atlas Edition-I.
========================================================================================
For every active non-supplementary kit that maps to a LIT feasible ghost cell:

    Delta(kit) = kit_position - own_cell_position

This is the reconstruction error of the 7-core meso instrument (the ghost field)
evaluated at every lit point on the frozen Edition-I plane. A KIT projects with all
14 coordinates; a GHOST CELL projects with only the 7 core coordinates (non-core
blocks masked, CA renormalized over core-present levels). The displacement is exactly
the contribution of the 7 MASKED non-core coordinates, mediated through renormalization.

Author: elrond (data steward). TOOL script (analytical extraction), not engine code.
Commissioned by gandalf, Matt-approved 2026-07-15 (displacement-field emission +
Edition-II drill-in slate pre-registration). Reproducible emission of the
atlas-displacement-field-edition1.csv artifact.

FREEZE DISCIPLINE (non-negotiable — no re-fit, no basis change, new files only):
  - The frozen Edition-I MCA fit is reconstructed from the DURABLE pre-C3 snapshot
    atlas-frozen-fit-cellkeys-edition1.csv (verified to reproduce all 469 active kit
    positions to ~5e-8 — atlas.json stores 8 decimals). Same reconstruction the ghost
    emitter uses (ghost_field_edition1.build_frozen_fit). No fit is recomputed here that
    is not byte-equivalent to the frozen one.
  - Kit positions and cell positions are computed by the IDENTICAL CA supplementary
    transition formula F(d) = sum_j rowp_j * col_std_j(d); they differ ONLY in which
    levels are present (kit: up to 14; cell: 7 core). This is what makes Delta a clean
    additive object. (In classical CA on an indicator matrix, the row principal
    coordinate and the own-profile transition formula coincide — verified.)
  - Cell positions are READ from atlas.json ghost_field.feasible_cells (the frozen
    emitted artifact), not recomputed, so the displacement is measured against the
    exact published ghost plane.

JOIN (reuses ghost_field_edition1.lit_map logic exactly):
  Each active kit's LIVE cell_key -> 7-core register-meso tuple via the REG2FIT
  crosswalk (fit2reg_movement / fit2reg_delivery / fit2reg_direct). Kits whose core
  doesn't map to a feasible cell = the unmapped-pending-curation set (14, matching the
  ghost emitter) -> EXCLUDED from displacement, LISTED in the memo. Kits mapping to a
  feasible cell that is NOT lit cannot occur (the kit itself lights it).

ATTRIBUTION (exact, verified to machine precision):
  With w_j = 1/first_sv[block_j] the MFA weight of level j, and c_j = col_std_j the
  frozen column standard coordinate (== the loadings), let:
      Score = sum_{j in core}    w_j * c_j        (core numerator vector)
      NC_l  = w_l * c_l                            (per non-core level l numerator)
      W_all = sum_{j present} w_j                  W_core = sum_{j in core} w_j
  Then:
      K = (Score + sum_l NC_l) / W_all             (kit position)
      C =  Score / W_core                          (cell position)
      Delta = K - C
            = Score*(1/W_all - 1/W_core)   +   (1/W_all) * sum_l NC_l
              \___ core-dilution vector ___/       \__ per-non-core direct pulls __/
  The DIRECT per-non-core contribution of level l is  (w_l * c_l) / W_all  — a signed
  vector on each display axis, attributed to that named level. The CORE-DILUTION term
  belongs to no single non-core level (it is the renormalization consequence of masking
  ALL of them collectively) and is carried as its own labeled term. Their sum
  reconstructs Delta exactly (residual < 1e-15).

Register-ref: feasibility-cuts-register-v1.1. Basis: Edition-I (frozen).
"""

import os, sys, csv, json
import numpy as np
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import atlas_derivation_2026_07_14 as pipe
import ghost_field_edition1 as gf

ATLAS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "atlas"))
FROZEN_FIT_CSV = os.path.join(ATLAS_DIR, "atlas-frozen-fit-cellkeys-edition1.csv")
ATLAS_JSON = os.path.join(ATLAS_DIR, "atlas.json")
OUT_CSV = os.path.join(ATLAS_DIR, "atlas-displacement-field-edition1.csv")
OUT_JSON = os.path.join(ATLAS_DIR, "atlas-displacement-field-edition1.json")

NAMES = pipe.NAMES
MASK = pipe.MASK
FUSE_MIN = pipe.FUSE_MIN
OTHER_RARE = pipe.OTHER_RARE
CORE = gf.CORE                                   # 7 core coords (never-demote)
NONCORE = [n for n in NAMES if n not in CORE]    # 7 non-core (masked at meso)
CK_IDX = gf.CK_IDX                               # core-slot indices in the 14-field cell_key


# ---------------------------------------------------------------------------
# FROZEN FIT reconstruction (byte-equivalent to ghost_field_edition1.build_frozen_fit,
# but we also retain col_std for BOTH display axes for attribution).
# ---------------------------------------------------------------------------
def build_frozen_fit():
    keys = []
    with open(FROZEN_FIT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            keys.append((row["kit_id"], row["cell_key"].split("|")))
    kit_vals = [k[1] for k in keys]
    fuse_map = {}
    for i in range(14):
        c = Counter(v[i] for v in kit_vals if v[i] not in MASK)
        for lv, n in c.items():
            if n < FUSE_MIN:
                fuse_map[(i, lv)] = OTHER_RARE

    def apply_fuse(vals):
        return [vals[i] if vals[i] in MASK else fuse_map.get((i, vals[i]), vals[i]) for i in range(14)]

    kit_fused = [apply_fuse(v) for v in kit_vals]
    Z, cm, block_of_col, first_sv = pipe.build_indicator(kit_fused, block_weight=True)
    mca = pipe.mca_greenacre(Z, cm)
    sv = mca["sv"]
    nret = 14
    col_std = mca["col_pc"][:, :nret] / sv[:nret][None, :]   # frozen column standard coords
    colidx = {lvl: i for i, lvl in enumerate(cm)}
    return dict(keys=keys, kit_fused=kit_fused, apply_fuse=apply_fuse, fuse_map=fuse_map,
                Z=Z, colidx=colidx, block_of_col=block_of_col, first_sv=first_sv,
                col_std=col_std, ncols=Z.shape[1])


def kit_present_terms(fused, fit):
    """Present (non-mask, in-vocab) levels of a kit -> (coord, level, w_j, c_xy)."""
    colidx, block_of_col, first_sv, col_std = (fit["colidx"], fit["block_of_col"],
                                               fit["first_sv"], fit["col_std"])
    terms = []
    for i in range(14):
        v = fused[i]
        if v in MASK:
            continue
        j = colidx.get((NAMES[i], v))
        if j is None:
            continue
        w = 1.0 / first_sv[block_of_col[j]]
        terms.append((NAMES[i], v, w, col_std[j][:2].copy()))
    return terms


# ---------------------------------------------------------------------------
# JOIN: kit LIVE cell_key -> 7-core register-meso tuple (reuse ghost lit_map crosswalk).
# ---------------------------------------------------------------------------
def kit_core_tuple(ck_fields):
    geometry = ck_fields[3]
    proxy = ck_fields[CK_IDX["proxy"]]
    core = {
        "movement": gf.fit2reg_movement(ck_fields[CK_IDX["movement"]]),
        "delivery": gf.fit2reg_delivery(ck_fields[CK_IDX["delivery"]], geometry, proxy),
        "treatment": gf.fit2reg_direct(ck_fields[CK_IDX["treatment"]], "treatment"),
        "function": gf.fit2reg_direct(ck_fields[CK_IDX["function"]], "function"),
        "proxy": gf.fit2reg_direct(ck_fields[CK_IDX["proxy"]], "proxy"),
        "activation": gf.fit2reg_direct(ck_fields[CK_IDX["activation"]], "activation"),
        "dependency": gf.fit2reg_direct(ck_fields[CK_IDX["dependency"]], "dependency"),
    }
    if any(v is None for v in core.values()):
        return None, "unmapped-core-slot"
    if not gf.meso_feasible(core):
        return None, "would-seal"
    return tuple(core[c] for c in CORE), None


# ---------------------------------------------------------------------------
# Load atlas.json: active kit positions + lit-cell positions keyed by core tuple.
# ---------------------------------------------------------------------------
def load_atlas():
    with open(ATLAS_JSON) as f:
        a = json.load(f)
    points = {p["kit_id"]: p for p in a["points"] if not p.get("supplementary")}
    cell_by_core = {}
    for c in a["ghost_field"]["feasible_cells"]:
        cell_by_core[tuple(c["core"])] = c
    return a, points, cell_by_core


# ---------------------------------------------------------------------------
# Live cell_keys for active kits — read from the same corpus.db the ghost emitter uses,
# so the join is byte-identical to the emitted lighting. (Falls back cleanly if DB absent
# by reconstructing from frozen fit keys — but the frozen keys are PRE-C3 and the lit
# mapping is POST-C3, so DB is authoritative for the join. We require the DB.)
# ---------------------------------------------------------------------------
def load_live_keys():
    import sqlite3
    # corpus.db lives at research/curated/corpus.db (the SAME DB the ghost emitter reads;
    # ghost_field_edition1.__main__ hard-codes this absolute path). It is one level UP from
    # the atlas/ artifact dir. Authoritative for the POST-C3 lit-mapping join.
    DB = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "curated", "corpus.db"))
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT k.kit_id, k.cell_key FROM canon_engine_key k JOIN canon_corpus c ON c.kit_id=k.kit_id "
        "WHERE k.row_class='combat-kit' AND c.negative=0 AND k.cell_key IS NOT NULL ORDER BY k.kit_id"
    ).fetchall()
    con.close()
    return {kid: ck.split("|") for kid, ck in rows}


# ---------------------------------------------------------------------------
# BUILD the displacement field.
# ---------------------------------------------------------------------------
def build_displacement_field():
    fit = build_frozen_fit()
    a, points, cell_by_core = load_atlas()
    live_keys = load_live_keys()

    # frozen-fit fused keys, indexed by kit for the transition-formula terms
    frozen_fused = {kid: fit["kit_fused"][i] for i, (kid, _) in enumerate(fit["keys"])}
    frozen_raw = {kid: vals for kid, vals in fit["keys"]}

    rows = []
    unmapped = []          # kits whose core doesn't map to a feasible cell
    excluded_no_point = [] # kits with no active point in atlas (should not happen for active)
    excluded_no_cell = []  # kits mapping to a feasible core tuple that isn't in the plane (should not happen)

    for kid in sorted(points.keys()):
        # LIVE key drives the JOIN (post-C3 lighting); FROZEN fused drives the POSITION.
        live = live_keys.get(kid)
        if live is None:
            # no live combat-kit row (e.g. a point present in atlas but filtered live) -> skip join
            unmapped.append((kid, "no-live-key"))
            continue
        core_tuple, reason = kit_core_tuple(live)
        if core_tuple is None:
            unmapped.append((kid, reason))
            continue
        cell = cell_by_core.get(core_tuple)
        if cell is None:
            excluded_no_cell.append(kid)
            continue

        # kit position via frozen transition formula (== atlas point to ~5e-8)
        fused = frozen_fused.get(kid)
        if fused is None:
            excluded_no_point.append(kid)
            continue
        terms = kit_present_terms(fused, fit)
        core_terms = [t for t in terms if t[0] in CORE]
        nc_terms = [t for t in terms if t[0] in NONCORE]
        W_all = sum(t[2] for t in terms)
        W_core = sum(t[2] for t in core_terms)
        Score = sum(t[2] * t[3] for t in core_terms)
        K = (Score + sum(t[2] * t[3] for t in nc_terms)) / W_all
        C = Score / W_core

        kit_x, kit_y = float(K[0]), float(K[1])
        cell_x, cell_y = float(cell["x"]), float(cell["y"])   # PUBLISHED cell (live-keyed)
        dx, dy = kit_x - cell_x, kit_y - cell_y
        mag = float(np.hypot(dx, dy))

        # EXACT THREE-PART additive attribution of Delta = K - C_published.
        #   K       = Score/W_all + NCsum/W_all
        #   C_fc    = Score/W_core            (cell reconstructed from the KIT's FROZEN core levels)
        #   C_pub   = published ghost cell    (reconstructed from the LIVE core tuple via project_meso_cell)
        # Then Delta = K - C_pub decomposes exactly as:
        #   (A) direct      = NCsum/W_all                         per-non-core masked-level pull
        #   (B) dilution    = Score*(1/W_all - 1/W_core)          core renorm (masking ALL non-core)
        #   (C) substitution= C_fc - C_pub                        FROZEN-position-key vs LIVE-lighting-key
        #                                                         core-level drift (C3 re-keys, other-rare
        #                                                         fusions) — ZERO for the 385 kits whose
        #                                                         frozen core == live core; nonzero for 70.
        C_fc = Score / W_core
        C_pub = np.array([cell_x, cell_y])
        dilution = Score * (1.0 / W_all - 1.0 / W_core)
        substitution = C_fc - C_pub
        direct = {}                                              # per non-core level -> (x,y,level)
        for (co, lv, w, c) in nc_terms:
            contr = (w * c) / W_all
            direct[co] = (float(contr[0]), float(contr[1]), lv)
        # reconstruction check: (A) + (B) + (C) must equal (dx,dy)
        ncsum = np.zeros(2)
        for co in direct:
            ncsum += np.array([direct[co][0], direct[co][1]])
        recon = ncsum + dilution + substitution
        resid = float(np.max(np.abs(recon - np.array([dx, dy]))))

        # kit position from the published atlas point (for cross-check / provenance)
        ap = points[kid]

        rows.append({
            "kit_id": kid,
            "franchise": ap.get("franchise"),
            "gateA_group": ap.get("gateA_group"),
            "core_movement": core_tuple[0], "core_delivery": core_tuple[1],
            "core_treatment": core_tuple[2], "core_function": core_tuple[3],
            "core_proxy": core_tuple[4], "core_activation": core_tuple[5],
            "core_dependency": core_tuple[6],
            "kit_x": round(kit_x, 8), "kit_y": round(kit_y, 8),
            "atlas_point_x": round(ap["x"], 8), "atlas_point_y": round(ap["y"], 8),
            "cell_x": round(cell_x, 8), "cell_y": round(cell_y, 8),
            "dx": round(dx, 8), "dy": round(dy, 8), "mag": round(mag, 8),
            # non-core levels carried (raw frozen values)
            "nc_amp": frozen_fused[kid][NAMES.index("amp")],
            "nc_geometry": frozen_fused[kid][NAMES.index("geometry")],
            "nc_defense": frozen_fused[kid][NAMES.index("defense")],
            "nc_economy": frozen_fused[kid][NAMES.index("economy")],
            "nc_range": frozen_fused[kid][NAMES.index("range")],
            "nc_tempo": frozen_fused[kid][NAMES.index("tempo")],
            "nc_commit": frozen_fused[kid][NAMES.index("commit")],
            # attribution: per non-core direct pull on x and y
            "attr_amp_x": round(direct.get("amp", (0, 0, ""))[0], 8),
            "attr_amp_y": round(direct.get("amp", (0, 0, ""))[1], 8),
            "attr_geometry_x": round(direct.get("geometry", (0, 0, ""))[0], 8),
            "attr_geometry_y": round(direct.get("geometry", (0, 0, ""))[1], 8),
            "attr_defense_x": round(direct.get("defense", (0, 0, ""))[0], 8),
            "attr_defense_y": round(direct.get("defense", (0, 0, ""))[1], 8),
            "attr_economy_x": round(direct.get("economy", (0, 0, ""))[0], 8),
            "attr_economy_y": round(direct.get("economy", (0, 0, ""))[1], 8),
            "attr_range_x": round(direct.get("range", (0, 0, ""))[0], 8),
            "attr_range_y": round(direct.get("range", (0, 0, ""))[1], 8),
            "attr_tempo_x": round(direct.get("tempo", (0, 0, ""))[0], 8),
            "attr_tempo_y": round(direct.get("tempo", (0, 0, ""))[1], 8),
            "attr_commit_x": round(direct.get("commit", (0, 0, ""))[0], 8),
            "attr_commit_y": round(direct.get("commit", (0, 0, ""))[1], 8),
            "attr_coredilution_x": round(float(dilution[0]), 8),
            "attr_coredilution_y": round(float(dilution[1]), 8),
            "attr_coresub_x": round(float(substitution[0]), 8),
            "attr_coresub_y": round(float(substitution[1]), 8),
            "attr_coresub_mag": round(float(np.hypot(*substitution)), 8),
            "attr_residual": round(resid, 12),
        })

    rows.sort(key=lambda r: (-r["mag"], r["kit_id"]))
    return a, rows, unmapped, excluded_no_point, excluded_no_cell


# ---------------------------------------------------------------------------
# Region aggregation. Bin lit cells (equivalently, the kits' OWN cells) spatially.
# CHOICE (documented in memo): compass quadrant (poles are meaningful: x+=PERFORM /
# x-=DEPLOY / y+=LAUNCH / y-=EMBODY) x radius band (inner/outer at the median cell
# radius) = up to 8 semantically-named regions. Each kit is binned by its OWN CELL's
# position (the anchor the displacement is measured FROM). Aggregate |Delta| mass
# (sum) and mean |Delta|; dominant masked-coordinate attribution per region.
# ---------------------------------------------------------------------------
def quadrant(x, y):
    ew = "E" if x >= 0 else "W"          # E = PERFORM (+x), W = DEPLOY (-x)
    ns = "N" if y >= 0 else "S"          # N = LAUNCH (+y), S = EMBODY (-y)
    return ew + ns

POLE_NAME = {"E": "PERFORM", "W": "DEPLOY", "N": "LAUNCH", "S": "EMBODY"}


def aggregate_regions(rows, a):
    # median radius over LIT cells (the anchor set)
    lit = [c for c in a["ghost_field"]["feasible_cells"] if c["lit"]]
    lit_r = np.array([np.hypot(c["x"], c["y"]) for c in lit])
    r_split = float(np.median(lit_r))

    regions = {}
    for r in rows:
        cx, cy = r["cell_x"], r["cell_y"]
        q = quadrant(cx, cy)
        band = "outer" if np.hypot(cx, cy) >= r_split else "inner"
        rid = f"{q}-{band}"
        regions.setdefault(rid, {"kits": [], "mass": 0.0, "dxsum": 0.0, "dysum": 0.0,
                                 "attr": Counter(), "attr_x": Counter(), "attr_y": Counter()})
        R = regions[rid]
        R["kits"].append(r["kit_id"])
        R["mass"] += r["mag"]
        R["dxsum"] += r["dx"]
        R["dysum"] += r["dy"]
        # dominant masked-coordinate attribution: sum |contribution| per non-core coord.
        # NOTE the two non-promotable terms carried alongside the 7 promotable non-core coords:
        #   _coredilution  = the renorm consequence of masking non-core (a drill-in reduces it
        #                    indirectly by un-masking); _coresub = frozen-vs-live core-key drift
        #                    (a drill-in on a NON-core coord does NOT reduce it — it is a curation
        #                    signal, not a promotion signal).
        for co in NONCORE:
            cxv = r[f"attr_{co}_x"]; cyv = r[f"attr_{co}_y"]
            R["attr"][co] += float(np.hypot(cxv, cyv))
            R["attr_x"][co] += cxv
            R["attr_y"][co] += cyv
        R["attr"]["_coredilution"] += float(np.hypot(r["attr_coredilution_x"], r["attr_coredilution_y"]))
        R["attr_x"]["_coredilution"] += r["attr_coredilution_x"]
        R["attr_y"]["_coredilution"] += r["attr_coredilution_y"]
        R["attr"]["_coresub"] += float(np.hypot(r["attr_coresub_x"], r["attr_coresub_y"]))
        R["attr_x"]["_coresub"] += r["attr_coresub_x"]
        R["attr_y"]["_coresub"] += r["attr_coresub_y"]

    out = []
    for rid, R in regions.items():
        n = len(R["kits"])
        ew, band = rid.split("-")[0][0], rid.split("-")[1]
        ns = rid.split("-")[0][1]
        # PROMOTABLE ranking = the 7 non-core coords only (a drill-in can promote these).
        promotable = Counter({k: v for k, v in R["attr"].items() if k in NONCORE})
        out.append({
            "region": rid,
            "pole_x": POLE_NAME[ew], "pole_y": POLE_NAME[ns], "band": band,
            "n_kits": n,
            "mass_abs_delta": round(R["mass"], 6),
            "mean_abs_delta": round(R["mass"] / n, 6),
            "net_dx": round(R["dxsum"], 6), "net_dy": round(R["dysum"], 6),
            "dominant_attr": R["attr"].most_common(5),
            "dominant_promotable": promotable.most_common(4),
            "net_attr_x": {k: round(v, 6) for k, v in R["attr_x"].most_common()},
            "net_attr_y": {k: round(v, 6) for k, v in R["attr_y"].most_common()},
        })
    out.sort(key=lambda d: -d["mass_abs_delta"])
    return out, r_split


if __name__ == "__main__":
    a, rows, unmapped, exc_np, exc_nc = build_displacement_field()

    # --- write per-kit CSV ---
    cols = list(rows[0].keys()) if rows else []
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    regions, r_split = aggregate_regions(rows, a)

    # --- write JSON sidecar (rows + regions + provenance) ---
    sidecar = {
        "artifact": "atlas-displacement-field-edition1",
        "basis": "Edition-I (frozen)",
        "register_ref": "feasibility-cuts-register-v1.1",
        "method": "Delta(kit)=kit_position-own_cell_position; kit=14-coord CA transition, "
                  "cell=7-core CA transition (non-core masked, renormalized); exact additive "
                  "attribution Delta = core-dilution + sum(per-non-core direct pulls).",
        "n_displaced": len(rows),
        "n_unmapped_pending_curation": len(unmapped),
        "unmapped_pending_curation": sorted([u[0] for u in unmapped]),
        "unmapped_reasons": {u[0]: u[1] for u in unmapped},
        "excluded_no_point": exc_np,
        "excluded_no_cell": exc_nc,
        "region_binning": "compass quadrant (x+=PERFORM/x-=DEPLOY, y+=LAUNCH/y-=EMBODY) "
                          "x radius band (inner/outer at median lit-cell radius r_split); "
                          "kit binned by its OWN CELL position.",
        "r_split_median_lit_radius": round(r_split, 6),
        "regions": regions,
        "rows": rows,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(sidecar, f, indent=2)

    # --- console report ---
    print("displacement rows:", len(rows), "(expect 469 - 14 unmapped = 455)")
    print("unmapped-pending-curation:", len(unmapped))
    for u in sorted(unmapped):
        print("   ", u[0], "->", u[1])
    print("excluded_no_point:", exc_np, "| excluded_no_cell:", exc_nc)
    print()
    resid_max = max(r["attr_residual"] for r in rows)
    print("max attribution residual:", resid_max, "(expect < 1e-8)")
    n_sub = sum(1 for r in rows if r["attr_coresub_mag"] > 1e-6)
    print(f"kits with nonzero core-substitution (>1e-6): {n_sub} "
          f"(frozen-position-key vs live-lighting-key core drift)")
    print()
    print("=== TOP 8 kits by |Delta| ===")
    for r in rows[:8]:
        print(f"  {r['kit_id']:32s} |D|={r['mag']:.3f} dx={r['dx']:+.3f} dy={r['dy']:+.3f} "
              f"grp={r['gateA_group']} commit={r['nc_commit']} geom={r['nc_geometry']} "
              f"sub={r['attr_coresub_mag']:.2f}")
    print()
    print(f"=== REGIONS (binned by own-cell; r_split={r_split:.3f}) ===")
    for R in regions:
        prom = ", ".join(f"{k}:{v:.2f}" for k, v in R["dominant_promotable"])
        allt = ", ".join(f"{k}:{v:.2f}" for k, v in R["dominant_attr"])
        print(f"  {R['region']:12s} [{R['pole_x']}x{R['pole_y']}] n={R['n_kits']:3d} "
              f"mass={R['mass_abs_delta']:7.2f} mean={R['mean_abs_delta']:.3f}")
        print(f"               promotable: {prom}")
        print(f"               all-terms:  {allt}")
    print()
    print("wrote:", OUT_CSV)
    print("wrote:", OUT_JSON)
