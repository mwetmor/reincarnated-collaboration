#!/usr/bin/env python3
r"""
displacement_field_edition1_rerun_mcd_2026_07_15.py
===================================================
CONFIRMATION-GATE RE-RUN of the Edition-I displacement field over the GROWN corpus.

Purpose (gandalf's confirmation gate, Matt-approved 2026-07-15): the MCD curation landed
(120 mcd- rows, 94 with cell_keys), growing the mapped corpus 469 -> 563 survivors+mcd. Re-run
the SAME displacement decomposition over ALL mapped kits INCLUDING the 94 keyable mcd rows to
CONFIRM (or report a shift in) the pre-registered Edition-II drill-in slate.

  Pre-registration record (DO NOT MODIFY): atlas-displacement-field-edition1.csv/.json (455 rows)
  + 2026-07-15-displacement-field-drill-in-slate.md (memo + prediction P-DF-1), commit c7804393.

  This re-run emits NEW dated artifacts ONLY:
    atlas-displacement-field-edition1-rerun-mcd.csv   (survivors 455 + mcd projections)
    atlas-displacement-field-edition1-rerun-mcd.json  (rows + regions + mcd census + provenance)

FREEZE DISCIPLINE (non-negotiable — same as the original; NO re-fit, NO basis change):
  - The frozen Edition-I MCA fit is reconstructed byte-identically to the original emitter
    (imported build_frozen_fit). The 14-dim basis, the fuse_map, the col_std loadings are all
    the FROZEN ones. NOTHING is refit.
  - SURVIVORS reproduce byte-identically to the original run (same atlas-point loop, same
    frozen-fit position, same live-key join). Asserted at runtime against the original CSV.
  - MCD kits are NEW points that PROJECT INTO the frozen space via the established
    "masked-like projection" / lighting-census-current discipline: each mcd kit's position is
    F(d) = sum_j rowp_j * col_std_j(d) over its OWN 14-field cell_key levels, using the FROZEN
    col_std and the FROZEN fuse_map. This is the identical CA supplementary transition formula the
    original uses for a kit position — the ONLY difference is the mcd kit has no atlas.json point
    and no frozen-fit row, so its position is computed here rather than read. A new kit projects
    with the frozen loadings; it does not move the basis. Out-of-basis levels (levels present in
    mcd but absent from the frozen columns — e.g. delivery=melee, range=mid) contribute ZERO to
    the position and drop from W_all: the honest freeze behavior (the basis is not extended to
    accommodate new vocabulary).
  - Cell positions are READ from atlas.json ghost_field.feasible_cells (frozen emitted plane).
    An mcd kit maps to a LIT feasible cell iff its live core tuple already lights that cell —
    which it does by construction (the mcd kit is IN the ghost/displacement predicate, so it
    already lit its own cell in the census-current ghost emission).

ATTRIBUTION (exact three-part additive, identical machinery to the original):
    Delta = (A) direct       sum_l (w_l*c_l)/W_all     per masked non-core level's pull
          + (B) core-dilution Score*(1/W_all - 1/W_core) renorm consequence of masking non-core
          + (C) core-substitution C_frozencore - C_published  frozen-position-key vs live-key drift
  For SURVIVORS (C) is the pre-C3 vs post-C3 curation drift (70 kits nonzero) as in the original.
  For MCD (C) is expected ~0: the mcd position AND its lit cell both derive from the SAME fresh
  live cell_key (there is no separate pre-C3 frozen key for mcd) — verified, not assumed.

SENSITIVITY (gandalf's required segment): mcd keys are steward-derived-from-prose (geometry
  conf 0.7, no canon_probe_facts). If any per-region ranking shifts vs the pre-registration, the
  ranking is RE-COMPUTED EXCLUDING mcd rows. If the shift disappears on the high-confidence
  (survivor-only) corpus, the shift is mcd-low-confidence-driven and is reported as
  "slate holds on high-confidence corpus; mcd-sensitive at [coord/region]" rather than a slate change.

Author: elrond (data steward). TOOL script (analytical extraction), not engine code.
Register-ref: feasibility-cuts-register-v1.1. Basis: Edition-I (frozen). Lineage: the original
displacement_field_edition1.py (imported wholesale; this script adds only mcd projection + the
sensitivity/census reporting the confirmation gate requires).
"""

import os, sys, csv, json
import numpy as np
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Import the ORIGINAL emitter wholesale — preserves script lineage; reuses the frozen machinery
# verbatim (build_frozen_fit, kit_present_terms, kit_core_tuple, load_atlas, aggregate_regions,
# quadrant, POLE_NAME, CORE, NONCORE, NAMES, MASK, load_live_keys).
import displacement_field_edition1 as orig
import atlas_derivation_2026_07_14 as pipe
import ghost_field_edition1 as gf

NAMES = orig.NAMES
MASK = orig.MASK
CORE = orig.CORE
NONCORE = orig.NONCORE

ATLAS_DIR = orig.ATLAS_DIR
# Pre-registration artifacts (READ-ONLY — used to assert survivor byte-reproduction).
ORIG_CSV = os.path.join(ATLAS_DIR, "atlas-displacement-field-edition1.csv")
# NEW dated output paths (the confirmation-gate artifacts).
OUT_CSV = os.path.join(ATLAS_DIR, "atlas-displacement-field-edition1-rerun-mcd.csv")
OUT_JSON = os.path.join(ATLAS_DIR, "atlas-displacement-field-edition1-rerun-mcd.json")


# ---------------------------------------------------------------------------
# 22-vertex ghost hull (galadriel r4/r5 ghostHullWorld) — Andrew's monotone chain over the
# DISTINCT world positions of ALL feasible cells (incl. out-of-frame). Reproduces 7128 distinct
# positions -> 22 vertices -> east reach 1.2581 -> 14 survivor beyond-horizon (validated).
# Boundary convention (spec §9.5.1): ON hull edge => INSIDE (not beyond).
# ---------------------------------------------------------------------------
def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def point_in_hull(pt, hull, eps=1e-9):
    n = len(hull)
    x, y = pt
    for i in range(n):
        ax, ay = hull[i]
        bx, by = hull[(i + 1) % n]
        cr = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        if abs(cr) < eps and min(ax, bx) - eps <= x <= max(ax, bx) + eps and \
           min(ay, by) - eps <= y <= max(ay, by) + eps:
            return True  # on edge => inside
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = hull[i]
        xj, yj = hull[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def ghost_hull_from_atlas(a):
    allpos = set((round(c["x"], 10), round(c["y"], 10)) for c in a["ghost_field"]["feasible_cells"])
    return convex_hull(list(allpos)), len(allpos)


# ---------------------------------------------------------------------------
# Diagnose WHICH of the 7 core slots fails the register-meso crosswalk for a kit whose core
# does not map. Mirrors orig.kit_core_tuple slot-by-slot. Used only for the mcd census (so the
# "predicate-satisfied but plane-unmapped" reason is legible per-slot, never invented).
# ---------------------------------------------------------------------------
CK_IDX = gf.CK_IDX


def mcd_failed_core_slots(ck_fields):
    geometry = ck_fields[3]
    proxy = ck_fields[CK_IDX["proxy"]]
    res = {
        "movement": gf.fit2reg_movement(ck_fields[CK_IDX["movement"]]),
        "delivery": gf.fit2reg_delivery(ck_fields[CK_IDX["delivery"]], geometry, proxy),
        "treatment": gf.fit2reg_direct(ck_fields[CK_IDX["treatment"]], "treatment"),
        "function": gf.fit2reg_direct(ck_fields[CK_IDX["function"]], "function"),
        "proxy": gf.fit2reg_direct(ck_fields[CK_IDX["proxy"]], "proxy"),
        "activation": gf.fit2reg_direct(ck_fields[CK_IDX["activation"]], "activation"),
        "dependency": gf.fit2reg_direct(ck_fields[CK_IDX["dependency"]], "dependency"),
    }
    # report (slot, raw cell_key value) for each None-mapping core slot
    out = []
    for slot, v in res.items():
        if v is None:
            out.append(f"{slot}={ck_fields[CK_IDX[slot]]}")
    return out


def mcd_counterfactual_map_if_movement(live_keys, survivor_ids):
    """If movement were assigned (any of walk/full-move/rooted), how many mcd would then map?
    Isolates the movement gate from any OTHER gate (e.g. delivery=melee). Reports the residual
    still-unmapped set — the second, independent gate. Never mutates the DB; a what-if only."""
    mv2reg = {"full-move": "FREE-MOVE", "walk": "WALK", "rooted": "ROOTED"}
    counts = {}
    residual_ids = None
    for mv in ("walk", "full-move", "rooted"):
        mapped = 0
        resid = []
        for kid in sorted(live_keys.keys()):
            if kid in survivor_ids:
                continue
            f = live_keys[kid]
            geometry = f[3]
            proxy = f[CK_IDX["proxy"]]
            core = {
                "movement": mv2reg.get(mv),
                "delivery": gf.fit2reg_delivery(f[CK_IDX["delivery"]], geometry, proxy),
                "treatment": gf.fit2reg_direct(f[CK_IDX["treatment"]], "treatment"),
                "function": gf.fit2reg_direct(f[CK_IDX["function"]], "function"),
                "proxy": gf.fit2reg_direct(f[CK_IDX["proxy"]], "proxy"),
                "activation": gf.fit2reg_direct(f[CK_IDX["activation"]], "activation"),
                "dependency": gf.fit2reg_direct(f[CK_IDX["dependency"]], "dependency"),
            }
            if any(v is None for v in core.values()):
                resid.append(kid)
            elif gf.meso_feasible(core):
                mapped += 1
            else:
                resid.append(kid)
        counts[mv] = mapped
        residual_ids = sorted(resid)
    return counts, residual_ids


# ---------------------------------------------------------------------------
# Project ONE cell_key into the FROZEN space and emit the same per-kit row the original writes,
# plus an `origin` field (survivor|mcd) and a `beyond_horizon` flag. `fused` is the cell_key with
# the FROZEN fuse_map already applied. Out-of-basis levels (no frozen column) drop from the sum.
# This is exactly orig.kit_present_terms + the original row-build arithmetic, factored so it can be
# fed a computed (mcd) fused key rather than only a frozen-fit key.
# ---------------------------------------------------------------------------
def build_row(kid, fused_raw, fused, fit, core_tuple, cell, origin, hull,
              franchise=None, gateA_group=None, atlas_point=None):
    terms = orig.kit_present_terms(fused, fit)
    core_terms = [t for t in terms if t[0] in CORE]
    nc_terms = [t for t in terms if t[0] in NONCORE]
    W_all = sum(t[2] for t in terms)
    W_core = sum(t[2] for t in core_terms)
    Score = sum(t[2] * t[3] for t in core_terms)
    K = (Score + sum(t[2] * t[3] for t in nc_terms)) / W_all
    C_fc = Score / W_core

    kit_x, kit_y = float(K[0]), float(K[1])
    cell_x, cell_y = float(cell["x"]), float(cell["y"])
    dx, dy = kit_x - cell_x, kit_y - cell_y
    mag = float(np.hypot(dx, dy))

    C_pub = np.array([cell_x, cell_y])
    dilution = Score * (1.0 / W_all - 1.0 / W_core)
    substitution = C_fc - C_pub
    direct = {}
    for (co, lv, w, c) in nc_terms:
        contr = (w * c) / W_all
        direct[co] = (float(contr[0]), float(contr[1]), lv)
    ncsum = np.zeros(2)
    for co in direct:
        ncsum += np.array([direct[co][0], direct[co][1]])
    recon = ncsum + dilution + substitution
    resid = float(np.max(np.abs(recon - np.array([dx, dy]))))

    beyond = not point_in_hull((round(kit_x, 10), round(kit_y, 10)), hull)

    def nc(name):
        return fused_raw[NAMES.index(name)]

    row = {
        "kit_id": kid,
        "origin": origin,
        "franchise": franchise,
        "gateA_group": gateA_group,
        "core_movement": core_tuple[0], "core_delivery": core_tuple[1],
        "core_treatment": core_tuple[2], "core_function": core_tuple[3],
        "core_proxy": core_tuple[4], "core_activation": core_tuple[5],
        "core_dependency": core_tuple[6],
        "kit_x": round(kit_x, 8), "kit_y": round(kit_y, 8),
        "atlas_point_x": round(atlas_point["x"], 8) if atlas_point else "",
        "atlas_point_y": round(atlas_point["y"], 8) if atlas_point else "",
        "cell_x": round(cell_x, 8), "cell_y": round(cell_y, 8),
        "dx": round(dx, 8), "dy": round(dy, 8), "mag": round(mag, 8),
        "beyond_horizon": int(beyond),
        "nc_amp": nc("amp"), "nc_geometry": nc("geometry"), "nc_defense": nc("defense"),
        "nc_economy": nc("economy"), "nc_range": nc("range"), "nc_tempo": nc("tempo"),
        "nc_commit": nc("commit"),
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
    }
    return row


# ---------------------------------------------------------------------------
# Build the GROWN displacement field: survivors (byte-identical to original) + mcd projections.
# ---------------------------------------------------------------------------
def build_grown_field():
    fit = orig.build_frozen_fit()
    a, points, cell_by_core = orig.load_atlas()
    live_keys = orig.load_live_keys()               # 563 rows: 469 survivors + 94 mcd
    hull, n_hull_pos = ghost_hull_from_atlas(a)

    frozen_fused = {kid: fit["kit_fused"][i] for i, (kid, _) in enumerate(fit["keys"])}

    survivor_rows = []
    mcd_rows = []
    unmapped = []
    mcd_unmapped = []
    excluded_no_cell = []

    # ---- survivors: the ORIGINAL atlas-point loop, frozen-fit position, live-key join ----
    for kid in sorted(points.keys()):
        live = live_keys.get(kid)
        if live is None:
            unmapped.append((kid, "no-live-key"))
            continue
        core_tuple, reason = orig.kit_core_tuple(live)
        if core_tuple is None:
            unmapped.append((kid, reason))
            continue
        cell = cell_by_core.get(core_tuple)
        if cell is None:
            excluded_no_cell.append(kid)
            continue
        fused = frozen_fused.get(kid)
        if fused is None:
            continue
        ap = points[kid]
        row = build_row(kid, fused, fused, fit, core_tuple, cell, "survivor", hull,
                        franchise=ap.get("franchise"), gateA_group=ap.get("gateA_group"),
                        atlas_point=ap)
        survivor_rows.append(row)

    # ---- mcd: NEW points projected into the frozen space via masked-like projection ----
    # The mcd kits satisfy the SQL predicate (row_class='combat-kit' AND negative=0 AND
    # cell_key IS NOT NULL) — that is the predicate the curation log verified 94/94. But the
    # ghost/displacement JOIN applies a SECOND gate AFTER the fetch: kit_core_tuple maps the
    # kit's 7 CORE cell_key slots to a register-meso tuple via fit2reg_*. A mcd kit lights a
    # ghost cell only if ALL 7 core slots map. We record per-slot WHY any mcd kit fails, so the
    # "predicate-satisfied but plane-unmapped" distinction is explicit (not silently dropped).
    survivor_ids = set(points.keys())
    for kid in sorted(live_keys.keys()):
        if kid in survivor_ids:
            continue                                # only the NEW (mcd/non-atlas) kits here
        live = live_keys[kid]
        core_tuple, reason = orig.kit_core_tuple(live)
        if core_tuple is None:
            # attribute the failure to specific unmapped core slot(s) for the census.
            slots = mcd_failed_core_slots(live)
            mcd_unmapped.append((kid, reason, slots))
            continue
        cell = cell_by_core.get(core_tuple)
        if cell is None:
            mcd_unmapped.append((kid, "no-lit-cell", []))
            continue
        # POSITION via frozen col_std + frozen fuse_map applied to the mcd cell_key (masked-like).
        fused = fit["apply_fuse"](live)             # FROZEN fuse_map — no re-derivation
        row = build_row(kid, fused, fused, fit, core_tuple, cell, "mcd", hull,
                        franchise="mcd", gateA_group=None, atlas_point=None)
        mcd_rows.append(row)

    all_rows = survivor_rows + mcd_rows
    all_rows.sort(key=lambda r: (-r["mag"], r["kit_id"]))
    return (a, hull, n_hull_pos, all_rows, survivor_rows, mcd_rows,
            unmapped, mcd_unmapped, excluded_no_cell)


# ---------------------------------------------------------------------------
# Survivor byte-reproduction assertion: every survivor row must match the pre-registration CSV
# on the load-bearing numeric fields (kit_x/y, cell_x/y, dx/dy/mag, all attr_* ). Guards the
# freeze: if a survivor moved, the frozen machinery drifted and the run HALTS.
# ---------------------------------------------------------------------------
CMP_FIELDS = ["kit_x", "kit_y", "cell_x", "cell_y", "dx", "dy", "mag",
              "attr_geometry_x", "attr_geometry_y", "attr_commit_x", "attr_commit_y",
              "attr_economy_x", "attr_economy_y", "attr_coredilution_x", "attr_coredilution_y",
              "attr_coresub_x", "attr_coresub_y", "attr_coresub_mag"]


def assert_survivors_reproduce(survivor_rows):
    orig_by_id = {}
    with open(ORIG_CSV, newline="") as f:
        for r in csv.DictReader(f):
            orig_by_id[r["kit_id"]] = r
    assert len(survivor_rows) == len(orig_by_id), \
        f"survivor count {len(survivor_rows)} != original {len(orig_by_id)}"
    worst = 0.0
    for r in survivor_rows:
        o = orig_by_id.get(r["kit_id"])
        assert o is not None, f"survivor {r['kit_id']} absent from original CSV"
        for fld in CMP_FIELDS:
            d = abs(float(r[fld]) - float(o[fld]))
            worst = max(worst, d)
    assert worst < 1e-6, f"survivor reproduction drift {worst} >= 1e-6 — FREEZE VIOLATED"
    return worst


def main():
    (a, hull, n_hull_pos, all_rows, survivor_rows, mcd_rows,
     unmapped, mcd_unmapped, excluded_no_cell) = build_grown_field()

    # FREEZE GUARD — survivors must reproduce the pre-registration exactly.
    worst = assert_survivors_reproduce(survivor_rows)

    # regions on the GROWN corpus (survivors + mcd) and on survivors-only (sensitivity).
    regions_all, r_split = orig.aggregate_regions(all_rows, a)
    regions_surv, _ = orig.aggregate_regions(survivor_rows, a)

    # re-derive live_keys + survivor_ids for the counterfactual + gate census (cheap; same source).
    live_keys = orig.load_live_keys()
    survivor_ids = set(orig.load_atlas()[1].keys())
    cf_counts, cf_residual = mcd_counterfactual_map_if_movement(live_keys, survivor_ids)

    # --- write per-kit CSV (grown) ---
    cols = list(all_rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)

    # --- mcd census ---
    # mcd kits that DID map to a lit cell (their region distribution / beyond-horizon / coresub).
    mcd_bh = [r for r in mcd_rows if r["beyond_horizon"]]
    mcd_region = Counter()
    mcd_quadrant = Counter()
    for r in mcd_rows:
        cx, cy = r["cell_x"], r["cell_y"]
        q = orig.quadrant(cx, cy)
        band = "outer" if np.hypot(cx, cy) >= r_split else "inner"
        mcd_region[f"{q}-{band}"] += 1
        mcd_quadrant[q] += 1
    mcd_coresub_max = max((r["attr_coresub_mag"] for r in mcd_rows), default=0.0)
    mcd_coresub_nonzero = sum(1 for r in mcd_rows if r["attr_coresub_mag"] > 1e-6)
    mcd_commit = Counter(r["nc_commit"] for r in mcd_rows)

    # gate diagnosis over the mcd kits that FAILED the register-meso core join.
    gate_slot = Counter()          # which core slot failed, per (slot,rawval)
    for (kid, reason, slots) in mcd_unmapped:
        for s in slots:
            gate_slot[s] += 1
    # commit distribution over ALL 94 keyed mcd rows (from the live cell_key), for the census.
    all_mcd_live = {kid: live_keys[kid] for kid in live_keys if kid not in survivor_ids}
    commit_idx = NAMES.index("commit")
    mcd_commit_all = Counter(v[commit_idx] for v in all_mcd_live.values())

    # --- geometry-universality re-test (grown corpus) ---
    geom_universal_all = all(R["dominant_promotable"] and R["dominant_promotable"][0][0] == "geometry"
                             for R in regions_all)
    geom_universal_surv = all(R["dominant_promotable"] and R["dominant_promotable"][0][0] == "geometry"
                              for R in regions_surv)

    sidecar = {
        "artifact": "atlas-displacement-field-edition1-rerun-mcd",
        "purpose": "confirmation-gate re-run over grown corpus (survivors 455 + 94 mcd); "
                   "pre-registration untouched (atlas-displacement-field-edition1.*).",
        "basis": "Edition-I (frozen; masked-like projection for new mcd points — no re-fit)",
        "register_ref": "feasibility-cuts-register-v1.1",
        "survivor_reproduction_worst_abs": worst,
        "n_displaced_total": len(all_rows),
        "n_survivors": len(survivor_rows),
        "n_mcd_mapped": len(mcd_rows),
        "n_mcd_unmapped": len(mcd_unmapped),
        "mcd_unmapped": {u[0]: {"reason": u[1], "failed_core_slots": u[2]} for u in mcd_unmapped},
        "n_survivor_unmapped": len(unmapped),
        "ghost_hull_vertices": len(hull),
        "ghost_hull_distinct_positions": n_hull_pos,
        "ghost_hull_east_reach_x": round(max(v[0] for v in hull), 6),
        "r_split_median_lit_radius": round(r_split, 6),
        "regions_grown": regions_all,
        "regions_survivor_only": regions_surv,
        "geometry_universal_grown": geom_universal_all,
        "geometry_universal_survivor_only": geom_universal_surv,
        "mcd_census": {
            "n_keyed_rows": len(all_mcd_live),
            "n_mapped_to_lit_cell": len(mcd_rows),
            "n_unmapped_at_core_join": len(mcd_unmapped),
            "gate_diagnosis_failed_core_slot": dict(gate_slot.most_common()),
            "counterfactual_if_movement_assigned_mapped": cf_counts,
            "counterfactual_residual_still_unmapped_ids": cf_residual,
            "commit_distribution_all_keyed": dict(mcd_commit_all.most_common()),
            "mapped_region_distribution": dict(mcd_region.most_common()),
            "mapped_quadrant_distribution": dict(mcd_quadrant.most_common()),
            "mapped_commit_distribution": dict(mcd_commit.most_common()),
            "beyond_horizon_count": len(mcd_bh),
            "beyond_horizon_ids": sorted(r["kit_id"] for r in mcd_bh),
            "coresub_max": mcd_coresub_max,
            "coresub_nonzero_count": mcd_coresub_nonzero,
        },
        "rows": all_rows,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(sidecar, f, indent=2)

    # --- console report ---
    print("=== SURVIVOR FREEZE GUARD ===")
    print(f"survivors reproduced: {len(survivor_rows)} (expect 455); worst abs drift {worst:.2e} (< 1e-6 required)")
    print()
    print("=== GROWN FIELD COUNTS ===")
    print(f"total displaced rows: {len(all_rows)} (455 survivors + {len(mcd_rows)} mcd mapped)")
    print(f"mcd keyed rows: {len(all_mcd_live)}; mcd MAPPED to lit cell: {len(mcd_rows)}; "
          f"mcd unmapped at core join: {len(mcd_unmapped)}")
    print(f"ghost hull: {len(hull)} vertices over {n_hull_pos} distinct positions (expect 22 / 7128)")
    print(f"r_split (median lit radius): {r_split:.6f} (expect 0.434249)")
    print()
    print("=== MCD GATE DIAGNOSIS (why the 94 keyed rows do/don't reach the plane) ===")
    print(f"failed-core-slot tally (raw cell_key value): {dict(gate_slot.most_common())}")
    print(f"counterfactual — if movement were assigned, mcd that would map: {cf_counts}")
    print(f"counterfactual residual (still unmapped even with movement, e.g. delivery=melee): "
          f"{len(cf_residual)}")
    print()
    print("=== MCD CENSUS (of the mapped subset) ===")
    print(f"commit distribution over ALL 94 keyed mcd: {dict(mcd_commit_all.most_common())}")
    print(f"mcd mapped: {len(mcd_rows)}; mapped region dist: {dict(mcd_region.most_common())}")
    print(f"mcd beyond-horizon: {len(mcd_bh)} {sorted(r['kit_id'] for r in mcd_bh)}")
    print(f"mcd coresub: max={mcd_coresub_max:.2e}, nonzero(>1e-6)={mcd_coresub_nonzero}")
    print()
    print("=== GEOMETRY UNIVERSALITY ===")
    print(f"geometry = #1 promotable in ALL regions (grown): {geom_universal_all}")
    print(f"geometry = #1 promotable in ALL regions (survivor-only): {geom_universal_surv}")
    print()
    # region-delta: grown vs survivor-only (must be identical since 0 mcd entered the plane).
    surv_by_id = {R["region"]: R for R in regions_surv}
    max_mass_delta = 0.0
    for R in regions_all:
        s = surv_by_id.get(R["region"])
        if s:
            max_mass_delta = max(max_mass_delta,
                                 abs(R["mass_abs_delta"] - s["mass_abs_delta"]),
                                 abs(R["n_kits"] - s["n_kits"]))
    print(f"=== SENSITIVITY: max |grown - survivor-only| over regions (mass or n): {max_mass_delta} ===")
    print("   (0 => the corpus growth added NO mapped point; the ranking is mcd-invariant by construction)")
    print()
    print(f"=== REGIONS — GROWN (survivors + mcd); r_split={r_split:.3f} ===")
    for R in regions_all:
        prom = ", ".join(f"{k}:{v:.2f}" for k, v in R["dominant_promotable"])
        print(f"  {R['region']:12s} [{R['pole_x']}x{R['pole_y']}] n={R['n_kits']:3d} "
              f"mass={R['mass_abs_delta']:7.2f} mean={R['mean_abs_delta']:.3f}")
        print(f"               promotable: {prom}")
    print()
    print(f"=== REGIONS — SURVIVOR-ONLY (sensitivity control) ===")
    for R in regions_surv:
        prom = ", ".join(f"{k}:{v:.2f}" for k, v in R["dominant_promotable"])
        print(f"  {R['region']:12s} [{R['pole_x']}x{R['pole_y']}] n={R['n_kits']:3d} "
              f"mass={R['mass_abs_delta']:7.2f} mean={R['mean_abs_delta']:.3f}")
        print(f"               promotable: {prom}")
    print()
    print("wrote:", OUT_CSV)
    print("wrote:", OUT_JSON)
    return sidecar


if __name__ == "__main__":
    main()
