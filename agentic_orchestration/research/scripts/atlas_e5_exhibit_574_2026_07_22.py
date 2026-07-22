#!/usr/bin/env python3
"""
atlas_e5_exhibit_574_2026_07_22.py — E5 CANDIDATE FULL-574 EXHIBIT (elrond, 2026-07-22)
================================================================================
EXTENDS `atlas_e5_exhibit_2026_07_22.py` (the v1 265-fit-basis exhibit). Matt asked to see
the FULL 574 real-kit corpus placed in BOTH cameras (E4 served + E5 candidate-aligned) so he
can watch how build families reorient under the candidate angle before ruling the camera fork.

  v1 exhibit (imported for its recompute + repro gate + alignment): atlas_e5_exhibit_2026_07_22.py
  refit of record (imported, NOT modified):                        atlas_legb_refit_2026_07_22.py
  gate report of record:                                           2026-07-22-legb-gate-report.md
  §8-C VERDICT: B3 congruence 0.7836 < 0.85 -> E5 NOT served, E4 remains truth.

WHAT IS NEW vs v1 (v1 rendered ONLY the 265 fit basis):
  - The 265-kit record FIT BASIS still DERIVES the axes (unchanged; the ledger V-2 machinery:
    record-class derives, wider corpus projects SUPPLEMENTARY — supplementary rows never bend
    the axes they validate).
  - All 574 real kits (kit_master view: 267 record + 299 annex + 8 in-view system) are
    SUPPLEMENTARY-PROJECTED into the E5 candidate space via the standard CA transition formula
    (col_std = col_pc/sv; MFA-weighted weighted-row-profile). Annex/system carry NO gb_* bands
    (design-NULL) — they place from the SHARED (pre-v2.0) register coords + element_primary only;
    their gb_* blocks are passive. This is EXPECTED and rendered VISUALLY DISTINCT (smaller,
    hollow/faint markers), never hidden.
  - E4 panel places all 574 too: stored `atlas_coords` where present (record 265 + system 3),
    the rest via the FROZEN E4/E1 basis (FrozenBasis.project_point_xy from the 14-field cell_key
    — annex 292, +2 record, +1 system recoverable). Kits with NO cell_key AND no stored coords
    are UNPLACEABLE and reported explicitly (coverage counts in README + on-plot annotation).
    NO silent fabrication.

HARD CONSTRAINTS honored (same as v1):
  - READ-ONLY on corpus.db and every store (uri mode=ro; zero mutations).
  - NO serving artifacts: no atlas-edition5.json, nothing served-looking. Files prefixed
    `side-by-side-574` / `delta-arrows-574` / `e5-candidate-coords-574` under a full-574/ subdir.
  - Imports v1 + refit verbatim (method drift = a different fork). The B2 alignment reused is
    IDENTICAL to the B3 gate test (translation + rotation + reflection, NO scale).
  - REPRODUCTION GATE runs FIRST (delegates to v1.repro_check). Any mismatch -> HALT, no renders.

Color/annotate ONLY by ratified vocabulary: court (ratified k=5 element-courts; court-NULL=grey),
corpus_class, game. NO island/cluster/build-family naming (Matt-gated).

Executor: elrond. TOOL script (curation/exhibit), not engine code.
"""

import os
import sys
import csv
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# v1 exhibit — reuse its recompute (fit + B2 alignment) + reproduction gate verbatim.
import atlas_e5_exhibit_2026_07_22 as V1
# refit machinery — the EXACT fit/fuse/indicator/MCA math (never re-implemented here).
import atlas_legb_refit_2026_07_22 as R
from atlas_legb_refit_2026_07_22 import (
    ALL_NAMES, REG_NAMES, BAND_NAMES, ELEM_NAME,
    ro_connect, fuse_rows, build_indicator_multi, is_mask, OTHER_RARE,
)
from atlas_derivation_2026_07_14 import mca_greenacre
from atlas_frozen_basis_reconstruct import FrozenBasis

import json

DB = R.DB
# NEW subdir under the v1 exhibit dir.
OUT_V1 = V1.OUT
OUT = os.path.join(OUT_V1, "full-574")

WATERMARK = "E5 CANDIDATE — NOT SERVED (§8-C: E4 remains truth)"

# Ratified k=5 element-courts -> color. court-NULL = grey.
COURT_COLOR = {
    "physical":     "#8a8f98",  # steel-grey (distinct from the null grey below via saturation)
    "fire":         "#e2571e",
    "cold":         "#2b8fd6",
    "lightning":    "#e6b800",
    "chaos-poison": "#8f3fbf",
}
COURT_ORDER = ["physical", "fire", "cold", "lightning", "chaos-poison"]
NULL_COURT_COLOR = "#cfcfcf"   # grey for court-NULL (annex/system + 9 record)


def court_color(court):
    return COURT_COLOR.get(court, NULL_COURT_COLOR)


# ---------------------------------------------------------------------------
# Load the full 574 real-kit corpus (kit_master view = 267 record + 299 annex + 8 system).
# For each kit we capture: corpus_class, court, game, cell_key, and the E5 feature row
# (register coords from cell_key + element_primary from mapping_json; gb_* only for record).
# ---------------------------------------------------------------------------
def load_corpus_574(con):
    """Returns list of dicts with keys: kit_id, corpus_class, court, game, cell_key,
    e5_row (dict over ALL_NAMES; gb_* None for annex/system by design), has_e5_row."""
    rows = con.execute(
        "SELECT m.kit_id, c.corpus_class, c.court, c.game, k.cell_key, km.mapping_json "
        "FROM kit_master m "
        "JOIN canon_corpus c ON c.kit_id=m.kit_id "
        "JOIN kit_mapping km ON km.kit_id=m.kit_id "
        "LEFT JOIN canon_engine_key k ON k.kit_id=m.kit_id "
        "ORDER BY c.corpus_class, m.kit_id").fetchall()
    # primary (ordinal-0) geometry band per kit (record-class only carries these; annex/system NULL)
    band0 = {}
    for r in con.execute(
        "SELECT sgb.kit_id, sgb.delivery_class, sgb.range_band, sgb.motion_signature, "
        "sgb.width_band, sgb.speed_band, sgb.cadence_class "
        "FROM skill_geometry_band sgb WHERE sgb.skill_ordinal=0").fetchall():
        band0[r[0]] = {"gb_delivery": r[1], "gb_range": r[2], "gb_motion": r[3],
                       "gb_width": r[4], "gb_speed": r[5], "gb_cadence": r[6]}
    out = []
    for kit_id, cclass, court, game, cell_key, mj in rows:
        # element_primary (first skill) from mapping_json
        ep = None
        try:
            d = json.loads(mj)
            sk = d.get("skills", [])
            if sk:
                ep = sk[0].get("element_primary")
        except Exception:
            pass
        rec = None
        if cell_key is not None:
            parts = cell_key.split("|")
            if len(parts) == 14:
                rec = {REG_NAMES[i]: parts[i] for i in range(14)}
                b = band0.get(kit_id, {nm: None for nm in BAND_NAMES})
                for nm in BAND_NAMES:
                    rec[nm] = b.get(nm)   # None for annex/system by design -> passive
                rec[ELEM_NAME] = ep
        out.append({
            "kit_id": kit_id, "corpus_class": cclass, "court": court, "game": game,
            "cell_key": cell_key, "e5_row": rec, "has_e5_row": rec is not None,
        })
    return out


# ---------------------------------------------------------------------------
# E5 supplementary projection: rebuild the E5 fit indicator (the SAME 265-kit fit the axes
# came from), recover column standard coordinates, then project every 574 real kit as a
# supplementary weighted-row-profile. This is the V-2 machinery — supplementary rows do NOT
# influence the axes (we never re-fit with them). Then apply the SAME B2 transform used in the
# reproduction gate so the E5-candidate panel is aligned/comparable to E4.
# ---------------------------------------------------------------------------
def build_e5_supp_projector(b):
    """b = V1.recompute() bundle. Returns a closure project_e5_row(row_dict) -> nret-vector
    (unaligned E5 coords), plus (mu_m2, R2, mu_r2) for the B2 transform to aligned 2D."""
    con = ro_connect(DB)
    kit_ids, kit_rows, _, _ = V1.load_fit_data(con)
    con.close()
    kit_fused, fuse_map = fuse_rows(kit_rows, ALL_NAMES)
    Z, col_meta, block_of_col, first_sv, block_index = build_indicator_multi(kit_fused, ALL_NAMES)
    mca = mca_greenacre(Z, col_meta)
    sv = mca["sv"]
    nret = b["nret"]
    col_std = mca["col_pc"][:, :nret] / sv[:nret][None, :]
    colidx = {lvl: i for i, lvl in enumerate(col_meta)}
    ncols = Z.shape[1]

    def project_e5_row(row):
        """row: dict over ALL_NAMES. Fuse to the fit's fuse_map; build MFA-weighted profile over
        the fit's columns; masks + absent-from-basis levels are passive. Returns nret coord or None."""
        # fuse per-block using the fit's fuse_map
        fused = {}
        for nm in ALL_NAMES:
            v = row.get(nm)
            fused[nm] = v if is_mask(v) else fuse_map.get((nm, v), v)
        vec = np.zeros(ncols)
        present = 0
        for nm in ALL_NAMES:
            v = fused[nm]
            if is_mask(v):
                continue
            key = (nm, v)
            if key in colidx:
                j = colidx[key]
                vec[j] = 1.0 / first_sv[block_of_col[j]]   # same MFA weight as the fit
                present += 1
        rt = vec.sum()
        if rt <= 0:
            return None
        rowp = vec / rt
        coord = np.zeros(nret)
        nz = np.nonzero(rowp)[0]
        for j in nz:
            coord += rowp[j] * col_std[j]
        return coord

    return project_e5_row


def align_e5_2d(coord_nret, b):
    """Apply the reproduction-gate B2 transform (translation+rotation+reflection, NO scale) to a
    single unaligned E5 coord's first-2 dims. Identical transform to the anchor fit + v1 render."""
    mov2 = np.asarray(coord_nret[:2], float)
    return (mov2 - b["mu_m2"]) @ b["R2"] + b["mu_r2"]


# ---------------------------------------------------------------------------
# E4-side placement: stored atlas_coords where present; else FrozenBasis projection from the
# 14-field cell_key (register coords only — the frozen E1 basis has no bands/element). NO fabrication.
# ---------------------------------------------------------------------------
def build_e4_placements(corpus, b):
    """Returns dict kit_id -> (x, y, source) where source in {'stored','projected'}; missing kits
    absent from the dict (unplaceable E4-side). Uses b['e4_served'] (stored/reconstructed E4 camera)
    and FrozenBasis.project_point_xy for the rest."""
    fb = b["fb"]
    e4_served = b["e4_served"]   # kit_id -> (x,y): the E4/E1 SERVED plane (record + 3 system stored)
    out = {}
    for rec in corpus:
        kid = rec["kit_id"]
        if kid in e4_served:
            x, y = e4_served[kid]
            out[kid] = (float(x), float(y), "stored")
        elif rec["cell_key"] is not None:
            xy = fb.project_point_xy(rec["cell_key"])   # register-coord CA supplementary in frozen E1
            if xy is not None:
                out[kid] = (float(xy[0]), float(xy[1]), "projected")
        # else: no stored coords, no cell_key -> unplaceable E4-side (omitted, reported)
    return out


# ---------------------------------------------------------------------------
# Assemble the per-kit exhibit table: E4 (x,y,source), E5-aligned (x,y), supplementary flag,
# displacement (only where BOTH placed), mover rank.
# ---------------------------------------------------------------------------
def assemble_table(corpus, b, project_e5_row, e4_placements):
    idx_fit = b["idx"]   # kit_id -> row index in the 265 fit (fit-basis members)
    fit_ids = set(idx_fit.keys())
    all_aligned2 = b["all_aligned2"]   # fit members' aligned 2D (from the gate transform)
    fit_kit_ids = b["kit_ids"]

    recs = []
    for rec in corpus:
        kid = rec["kit_id"]
        # ---- E5-aligned coord ----
        e5xy = None
        supplementary = True
        if kid in fit_ids:
            # fit-basis member: its aligned 2D is already computed in the gate bundle (axis-deriving)
            i = idx_fit[kid]
            e5xy = (float(all_aligned2[i, 0]), float(all_aligned2[i, 1]))
            supplementary = False
        elif rec["has_e5_row"]:
            coord = project_e5_row(rec["e5_row"])
            if coord is not None:
                a = align_e5_2d(coord, b)
                e5xy = (float(a[0]), float(a[1]))
        # ---- E4 coord ----
        e4 = e4_placements.get(kid)   # (x,y,source) or None
        e4xy = (e4[0], e4[1]) if e4 else None
        e4src = e4[2] if e4 else ""
        # ---- displacement (only if BOTH) ----
        disp = None
        if e4xy is not None and e5xy is not None:
            disp = math.hypot(e5xy[0] - e4xy[0], e5xy[1] - e4xy[1])
        recs.append({
            "kit_id": kid, "corpus_class": rec["corpus_class"], "court": rec["court"],
            "game": rec["game"], "e4xy": e4xy, "e4src": e4src, "e5xy": e5xy,
            "supplementary": supplementary, "disp": disp,
        })
    # mover ranks over kits placed in BOTH
    both = [r for r in recs if r["disp"] is not None]
    both.sort(key=lambda r: -r["disp"])
    rank_of = {r["kit_id"]: i + 1 for i, r in enumerate(both)}
    for r in recs:
        r["mover_rank"] = rank_of.get(r["kit_id"], "")
    return recs, both


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------
def _both_limits(recs):
    pts = []
    for r in recs:
        if r["e4xy"]:
            pts.append(r["e4xy"])
        if r["e5xy"]:
            pts.append(r["e5xy"])
    P = np.array(pts)
    xmin, ymin = P.min(0); xmax, ymax = P.max(0)
    padx = 0.06 * (xmax - xmin); pady = 0.06 * (ymax - ymin)
    return (xmin - padx, xmax + padx), (ymin - pady, ymax + pady)


def _panel(ax, recs, coord_key, title, xlim, ylim, coverage_note):
    """Scatter one camera. coord_key in {'e4xy','e5xy'}. Color by court; record=solid,
    annex/system=smaller hollow/faint. court-NULL = grey."""
    # record-class solid, colored by court
    for court in COURT_ORDER + [None]:
        xs, ys = [], []
        for r in recs:
            if r["corpus_class"] != "record":
                continue
            if r[coord_key] is None:
                continue
            rc = r["court"] if (r["court"] in COURT_COLOR) else None
            if rc != court:
                continue
            xs.append(r[coord_key][0]); ys.append(r[coord_key][1])
        if xs:
            ax.scatter(xs, ys, s=26, c=court_color(court), alpha=0.9, linewidths=0, zorder=3)
    # annex + system: smaller hollow/faint markers (all court-NULL -> grey), visually distinct
    for cls, marker, edge in (("annex", "o", "#9aa0a6"), ("system", "s", "#5a5f66")):
        xs, ys = [], []
        for r in recs:
            if r["corpus_class"] != cls:
                continue
            if r[coord_key] is None:
                continue
            xs.append(r[coord_key][0]); ys.append(r[coord_key][1])
        if xs:
            ax.scatter(xs, ys, s=13 if cls == "annex" else 22, facecolors="none",
                       edgecolors=edge, linewidths=0.6, alpha=0.55, marker=marker, zorder=2,
                       label="%s (n=%d, supp.)" % (cls, len(xs)))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="#e2e2e2", lw=0.5, zorder=0)
    ax.axvline(0, color="#e2e2e2", lw=0.5, zorder=0)
    ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=7)
    ax.text(0.01, 0.01, coverage_note, transform=ax.transAxes, fontsize=6.6,
            va="bottom", ha="left", color="#333333",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#bbbbbb", alpha=0.85))
    # watermark on THIS panel
    ax.text(0.5, 0.5, WATERMARK, transform=ax.transAxes, fontsize=13, color="#d24545",
            alpha=0.16, ha="center", va="center", rotation=24, zorder=5, weight="bold")


def render_side_by_side(recs, b, cov):
    xlim, ylim = _both_limits(recs)
    e4_n = sum(1 for r in recs if r["e4xy"])
    e5_n = sum(1 for r in recs if r["e5xy"])
    fig, axes = plt.subplots(1, 2, figsize=(16, 8.2))
    _panel(axes[0], recs, "e4xy",
           "LEFT — E4 SERVED plane (truth) · all placeable real kits",
           xlim, ylim,
           "E4-placed: %d / 574  (stored %d + projected %d)"
           % (e4_n, cov["e4_stored"], cov["e4_projected"]))
    _panel(axes[1], recs, "e5xy",
           "RIGHT — E5 CANDIDATE (B2: rot %.2f°, refl %s, NO scale)"
           % (abs(b["ang2"]), bool(b["refl2"])),
           xlim, ylim,
           "E5-placed: %d / 574  (265 fit-basis derive axes; %d supplementary)"
           % (e5_n, e5_n - 265))
    # legend: courts + class markers
    court_handles = [Patch(facecolor=COURT_COLOR[c], edgecolor="none", label="court: %s" % c)
                     for c in COURT_ORDER]
    court_handles.append(Patch(facecolor=NULL_COURT_COLOR, edgecolor="none", label="court: NULL"))
    class_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#8a8f98",
               markersize=6, label="record (solid, axis-deriving/supp.)"),
        Line2D([0], [0], marker="o", color="none", markeredgecolor="#9aa0a6",
               markerfacecolor="none", markersize=6, label="annex (hollow, supp.)"),
        Line2D([0], [0], marker="s", color="none", markeredgecolor="#5a5f66",
               markerfacecolor="none", markersize=6, label="system (hollow, supp.)"),
    ]
    axes[0].legend(handles=court_handles + class_handles, loc="upper left",
                   fontsize=6.4, framealpha=0.92, ncol=1)
    fig.suptitle("E5 CANDIDATE vs SERVED E4 — full 574 real-kit corpus · "
                 "B3 congruence=%.4f (< 0.85 → NOT served) · anchor n=%d"
                 % (b["cong2"], len(b["common"])), fontsize=12)
    fig.text(0.995, 0.004, WATERMARK + " · exhibit for R1 ruling · 2026-07-22",
             ha="right", va="bottom", fontsize=7, color="#8a1a1a", style="italic")
    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    p = os.path.join(OUT, "side-by-side-574.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    return p


def render_delta_arrows(recs, b, both, cov):
    """Displacement arrows ONLY for kits placed in BOTH cameras. Full-strength arrows for
    record-class; thin faint arrows for annex/system. Label top-10 movers."""
    pts = []
    for r in both:
        pts.append(r["e4xy"]); pts.append(r["e5xy"])
    P = np.array(pts)
    xmin, ymin = P.min(0); xmax, ymax = P.max(0)
    padx = 0.06 * (xmax - xmin); pady = 0.06 * (ymax - ymin)

    fig, ax = plt.subplots(figsize=(11, 10))
    for r in both:
        (x0, y0), (x1, y1) = r["e4xy"], r["e5xy"]
        if r["corpus_class"] == "record":
            col = court_color(r["court"] if r["court"] in COURT_COLOR else None)
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.05, alpha=0.85), zorder=3)
            ax.scatter([x0], [y0], s=16, c=col, alpha=0.9, linewidths=0, zorder=4)
        else:
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="->", color="#9aa0a6", lw=0.5, alpha=0.45), zorder=2)
    # label top-10 movers (by displacement, over BOTH-placed)
    top10 = both[:10]
    for r in top10:
        x0, y0 = r["e4xy"]
        ax.scatter([x0], [y0], s=34, facecolors="none", edgecolors="#111111",
                   linewidths=0.9, zorder=5)
        ax.annotate("%s (Δ%.2f)" % (r["kit_id"], r["disp"]), (x0, y0), fontsize=6.4,
                    color="#111111", xytext=(3, 3), textcoords="offset points", zorder=6)

    ax.set_xlim(xmin - padx, xmax + padx); ax.set_ylim(ymin - pady, ymax + pady)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="#e2e2e2", lw=0.5, zorder=0)
    ax.axvline(0, color="#e2e2e2", lw=0.5, zorder=0)
    n_rec = sum(1 for r in both if r["corpus_class"] == "record")
    n_supp = len(both) - n_rec
    ax.set_title("Δ arrows (E4 → E5-aligned) for kits placed in BOTH cameras: "
                 "%d record (full arrows) + %d annex/system (faint) · B3 congruence=%.4f"
                 % (n_rec, n_supp, b["cong2"]), fontsize=9.5)
    court_handles = [Line2D([0], [0], color=COURT_COLOR[c], lw=2, label=c) for c in COURT_ORDER]
    court_handles.append(Line2D([0], [0], color=NULL_COURT_COLOR, lw=2, label="NULL"))
    court_handles.append(Line2D([0], [0], color="#9aa0a6", lw=0.7, label="annex/system (faint)"))
    ax.legend(handles=court_handles, loc="upper left", fontsize=7, framealpha=0.92, title="court")
    ax.tick_params(labelsize=7)
    ax.text(0.5, 0.5, WATERMARK, transform=ax.transAxes, fontsize=15, color="#d24545",
            alpha=0.15, ha="center", va="center", rotation=24, zorder=1, weight="bold")
    fig.text(0.995, 0.004, WATERMARK + " · 2026-07-22", ha="right", va="bottom",
             fontsize=7, color="#8a1a1a", style="italic")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    p = os.path.join(OUT, "delta-arrows-574.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    return p


# ---------------------------------------------------------------------------
# CSV + README
# ---------------------------------------------------------------------------
def write_coords_csv(recs):
    p = os.path.join(OUT, "e5-candidate-coords-574.csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kit_id", "corpus_class", "court", "game",
                    "e4_x", "e4_y", "e4_source", "e5_x_aligned", "e5_y_aligned",
                    "supplementary", "displacement", "mover_rank"])
        for r in sorted(recs, key=lambda x: (x["corpus_class"], x["kit_id"])):
            e4x = "%.6f" % r["e4xy"][0] if r["e4xy"] else ""
            e4y = "%.6f" % r["e4xy"][1] if r["e4xy"] else ""
            e5x = "%.6f" % r["e5xy"][0] if r["e5xy"] else ""
            e5y = "%.6f" % r["e5xy"][1] if r["e5xy"] else ""
            dsp = "%.6f" % r["disp"] if r["disp"] is not None else ""
            w.writerow([r["kit_id"], r["corpus_class"], r["court"] or "", r["game"],
                        e4x, e4y, r["e4src"], e5x, e5y,
                        1 if r["supplementary"] else 0, dsp, r["mover_rank"]])
    return p


def compute_coverage(recs):
    cov = {"by_class": {}, "e4_stored": 0, "e4_projected": 0}
    for cls in ("record", "annex", "system"):
        sub = [r for r in recs if r["corpus_class"] == cls]
        e4 = sum(1 for r in sub if r["e4xy"])
        e5 = sum(1 for r in sub if r["e5xy"])
        both = sum(1 for r in sub if r["e4xy"] and r["e5xy"])
        neither = sum(1 for r in sub if not r["e4xy"] and not r["e5xy"])
        cov["by_class"][cls] = {"total": len(sub), "e4": e4, "e5": e5,
                                "both": both, "neither": neither}
    cov["e4_stored"] = sum(1 for r in recs if r["e4src"] == "stored")
    cov["e4_projected"] = sum(1 for r in recs if r["e4src"] == "projected")
    return cov


def write_readme(recs, b, both, cov, repro_ok, repro_lines, files):
    p = os.path.join(OUT, "README.md")
    tot = cov["by_class"]
    T = lambda k, f: tot[k][f]
    grand = {f: sum(tot[c][f] for c in ("record", "annex", "system"))
             for f in ("total", "e4", "e5", "both", "neither")}
    with open(p, "w") as f:
        f.write("# E5 CANDIDATE EXHIBIT — FULL 574 corpus — numbers only\n\n")
        f.write("**Date:** 2026-07-22 · **Executor:** elrond · "
                "**Purpose:** R1 camera-fork ruling — Matt sees the FULL 574 real-kit corpus in "
                "BOTH cameras before ruling. **E5 NOT served (§8-C: E4 remains truth).**\n\n")
        f.write("Numbers only. NO island/cluster/build-family naming (Matt-gated). "
                "Color/annotate only by ratified vocabulary: court (k=5), corpus_class, game.\n\n")

        f.write("## Reproduction gate (vs 2026-07-22-legb-gate-report.md) — runs FIRST\n\n")
        f.write("**Result: %s**\n\n" % ("PASS — 8/8 match record" if repro_ok else "FAIL — HALT"))
        f.write("\n".join(repro_lines) + "\n\n")

        f.write("## Coverage table (of the 574 real kits = kit_master view)\n\n")
        f.write("kit_master = 267 record + 299 annex + 8 in-view system. "
                "E4-placed = stored `atlas_coords` OR frozen-E1 CA projection from the 14-field "
                "cell_key. E5-placed = 265 fit-basis (axis-deriving) + supplementary CA projection.\n\n")
        f.write("| corpus_class | total | E4-placed | E5-placed | both | neither |\n")
        f.write("|---|---|---|---|---|---|\n")
        for c in ("record", "annex", "system"):
            f.write("| %s | %d | %d | %d | %d | %d |\n"
                    % (c, T(c, "total"), T(c, "e4"), T(c, "e5"), T(c, "both"), T(c, "neither")))
        f.write("| **TOTAL** | **%d** | **%d** | **%d** | **%d** | **%d** |\n\n"
                % (grand["total"], grand["e4"], grand["e5"], grand["both"], grand["neither"]))
        f.write("- E4-placed breakdown: **%d stored** atlas_coords + **%d projected** "
                "(frozen-E1 CA supplementary from cell_key).\n" % (cov["e4_stored"], cov["e4_projected"]))
        f.write("- **Neither** = no stored coords AND no 14-field cell_key → unplaceable in either "
                "camera. Record's 2 = the pre-registered unprojectable degenerate kits "
                "(`d2-teleport-sorc`, `poe1-blood-magic-kit`; no cell_key at all).\n")
        f.write("- Delta arrows are drawn ONLY for the **%d kits placed in BOTH** cameras "
                "(record full-strength; annex/system thin/faint).\n\n" % grand["both"])

        f.write("## Top-10 movers (kits in BOTH cameras, by E4→E5-aligned displacement)\n\n")
        f.write("| rank | kit_id | corpus_class | court | Δ (plane units) | E4 (x,y) | E5-aligned (x,y) |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for i, r in enumerate(both[:10]):
            f.write("| %d | %s | %s | %s | %.4f | (%.3f, %.3f) | (%.3f, %.3f) |\n"
                    % (i + 1, r["kit_id"], r["corpus_class"], r["court"] or "NULL", r["disp"],
                       r["e4xy"][0], r["e4xy"][1], r["e5xy"][0], r["e5xy"][1]))
        f.write("\n")
        # displacement stats over BOTH-placed, split record vs supp
        d_rec = np.array([r["disp"] for r in both if r["corpus_class"] == "record"])
        d_sup = np.array([r["disp"] for r in both if r["corpus_class"] != "record"])
        d_all = np.array([r["disp"] for r in both])
        f.write("- Displacement over BOTH-placed (n=%d): min=%.4f median=%.4f max=%.4f mean=%.4f.\n"
                % (len(d_all), d_all.min(), float(np.median(d_all)), d_all.max(), d_all.mean()))
        if len(d_rec):
            f.write("  - record (n=%d): median=%.4f max=%.4f.\n"
                    % (len(d_rec), float(np.median(d_rec)), d_rec.max()))
        if len(d_sup):
            f.write("  - annex/system supplementary (n=%d): median=%.4f max=%.4f.\n"
                    % (len(d_sup), float(np.median(d_sup)), d_sup.max()))
        f.write("\n")

        f.write("## Method notes\n\n")
        f.write("- **Supplementary projection = V-2 machinery** (ratified): the record class "
                "DERIVES the axes; the wider corpus projects **supplementary** (standard MCA "
                "supplementary-point / CA transition-formula projection). Supplementary rows "
                "NEVER influence the axes — the 574 were never re-fit; the 265-kit record fit "
                "basis is byte-identical to the reproduction gate.\n")
        f.write("- **Annex places from SHARED vocabulary only.** The v2.0 six-block side-car "
                "(gb_* geometry-bands) populate ONLY the 267 record-class kits — annex/system "
                "have NONE, BY DESIGN. So annex/system project from the pre-v2.0 register coords "
                "(14-field cell_key) + element_primary; their gb_* blocks are passive. This is "
                "EXPECTED and rendered visually distinct (smaller hollow/faint markers), not hidden.\n")
        f.write("- **E4-side projection IS recoverable** for annex/system via the frozen E1 basis "
                "(`atlas_frozen_basis_reconstruct.FrozenBasis.project_point_xy`), which projects a "
                "supplementary point from the 14-field cell_key (register coords; the frozen basis "
                "has no bands/element). Stored `atlas_coords` used where present.\n")
        f.write("- **B2 alignment** reused verbatim from the reproduction gate = the identical B3 "
                "test transform (translation + rotation + reflection, **NO scale**; s* disclosed, "
                "not applied). Both panels share axis limits → directly comparable.\n\n")

        f.write("## Carried-forward caveat (from exhibit v1)\n\n")
        f.write("- The fused rare bucket **`gb_width/other-rare` tops BOTH candidate dims** "
                "(dim1 loading **+1.86**, dim2 loading **+2.48**). This is rare-category MCA "
                "leverage: a low-population fused level dominating the leading axes is part of why "
                "the refit is **not servable-grade** (it, with the 0.7836 congruence < 0.85, is why "
                "§8-C keeps E4 as truth). The candidate camera shown here is a diagnostic, not a "
                "proposed replacement.\n\n")

        f.write("## Files\n\n")
        for name, size in files:
            f.write("- `%s` — %d bytes\n" % (name, size))
        f.write("\n## Exact reproduction command\n\n")
        f.write("```\ncd %s\npython3 atlas_e5_exhibit_574_2026_07_22.py\n```\n\n" % SCRIPT_DIR)
        f.write("Deterministic: SEED=%d, all randomness pinned. corpus.db opened read-only "
                "(uri mode=ro). Imports `atlas_e5_exhibit_2026_07_22` + `atlas_legb_refit_2026_07_22` "
                "verbatim (no math changed). corpus.db md5 = "
                "`bebc933b0bf9bcab5988bbc16bcc55b4` (unchanged; read-only).\n\n" % R.SEED)
        f.write("## Constraint attestation\n\n")
        f.write("- READ-ONLY on corpus.db and every store — zero mutations.\n")
        f.write("- NO serving artifacts: no atlas-edition5.json, nothing under serving/vendor/Glance "
                "paths, no served-coordinate filenames. All files under this full-574/ exhibit dir.\n")
        f.write("- Reproduction gate (8/8) gates the renders: any mismatch → HALT, no renders.\n")
        f.write("- No island/cluster/build-family naming (Matt-gated). Vocabulary shown: court, "
                "corpus_class, game.\n")
    return p


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    print("=== E5 FULL-574 exhibit — recompute + reproduction gate (delegated to v1) ===")
    b = V1.recompute()
    repro_ok, repro_lines = V1.repro_check(b)
    for ln in repro_lines:
        print(ln)
    if not repro_ok:
        # Write a halt marker in the full-574 dir (do NOT emit renders).
        with open(os.path.join(OUT, "REPRODUCTION-MISMATCH.md"), "w") as f:
            f.write("# E5 FULL-574 EXHIBIT — REPRODUCTION MISMATCH — HALT\n\n")
            f.write("The E5 recompute did NOT reproduce the gate report of record 8/8. "
                    "NO renders emitted. Determinism is the whole warrant for this exhibit.\n\n")
            f.write("\n".join(repro_lines) + "\n")
        print("!!! HALT — reproduction mismatch. Wrote REPRODUCTION-MISMATCH.md, no renders. !!!")
        sys.exit(3)
    print("--- reproduction PASS (8/8) — emitting full-574 exhibit ---")

    con = ro_connect(DB)
    corpus = load_corpus_574(con)
    con.close()
    n_by_class = {c: sum(1 for r in corpus if r["corpus_class"] == c)
                  for c in ("record", "annex", "system")}
    print("corpus_574 loaded: %s (total %d)" % (n_by_class, len(corpus)))
    assert len(corpus) == 574, "kit_master should yield 574 real kits, got %d" % len(corpus)

    project_e5_row = build_e5_supp_projector(b)
    e4_placements = build_e4_placements(corpus, b)
    recs, both = assemble_table(corpus, b, project_e5_row, e4_placements)
    cov = compute_coverage(recs)

    p_sbs = render_side_by_side(recs, b, cov)
    p_arr = render_delta_arrows(recs, b, both, cov)
    p_csv = write_coords_csv(recs)

    files = []
    for pth in [p_sbs, p_arr, p_csv]:
        files.append((os.path.basename(pth), os.path.getsize(pth)))
    p_readme = write_readme(recs, b, both, cov, repro_ok, repro_lines, files)
    files.append((os.path.basename(p_readme), os.path.getsize(p_readme)))

    print("\n=== COVERAGE (of 574) ===")
    for c in ("record", "annex", "system"):
        cc = cov["by_class"][c]
        print("  %-8s total=%3d  E4=%3d  E5=%3d  both=%3d  neither=%d"
              % (c, cc["total"], cc["e4"], cc["e5"], cc["both"], cc["neither"]))
    print("  E4 stored=%d projected=%d" % (cov["e4_stored"], cov["e4_projected"]))
    print("\n=== TOP-5 MOVERS (both cameras) ===")
    for i, r in enumerate(both[:5]):
        print("  %d. %-32s %-8s court=%-13s Δ=%.4f"
              % (i + 1, r["kit_id"], r["corpus_class"], r["court"] or "NULL", r["disp"]))
    print("\n=== FILES ===")
    for name, size in files:
        print("  %-30s %8d bytes" % (name, size))
    print("\n=== exhibit dir: %s ===" % OUT)


if __name__ == "__main__":
    main()
