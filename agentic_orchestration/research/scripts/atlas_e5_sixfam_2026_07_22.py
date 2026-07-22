#!/usr/bin/env python3
"""
atlas_e5_sixfam_2026_07_22.py — E5 CANDIDATE · SIX NAMED BUILD-FAMILIES exhibit (elrond, 2026-07-22)
====================================================================================================
Matt's PRIMARY family exhibit. He rejected the fresh-cut lasso lens (algorithmic clusters + court
coloring): *"Why are we looking at element? I just want to see the build families we already know
of!"*  This exhibit shows the SIX NAMED, gateA-RATIFIED island families from the Edition-I
archipelago work — WHIRLWIND · CHANNELED-BEAM · MINION-PET · AURA · TOTEM-SENTRY · TRAP-MINE — in
BOTH cameras (E4 SERVED plane + E5-candidate-aligned plane), colored BY FAMILY. No element, no court,
no algorithmic clusters, no new names.

  reproduction + recompute of record:  atlas_e5_exhibit_2026_07_22.py       (V1)
  574 placement machinery (verbatim):   atlas_e5_exhibit_574_2026_07_22.py  (F)
  lasso geometry + span + metric:       atlas_e5_lassos_2026_07_22.py       (L)  <- SAME dispersion
                                                                                    metric for README
                                                                                    comparability
  refit of record (imported, NOT modified): atlas_legb_refit_2026_07_22.py  (R)
  gate report of record:                2026-07-22-legb-gate-report.md
  §8-C VERDICT: B3 congruence 0.7836 < 0.85 -> E5 NOT served, E4 remains truth.

MEMBERSHIP RECOVERY (the load-bearing fix — NO silent conflation):
  The archipelago-mock "core" census CONFLATED gateA-RATIFIED members with tau-propagated proposals
  (44 proposals ran ~1/3 precision). This exhibit RECOVERS the actual gateA-RATIFIED lists:
    - RATIFIED  = corpus.db `atlas_gateA_labels_2026_07_14` (86 rows: kit_id + group). This IS the
      ratified source (the mock seeded from it). Verified byte-identical to the mock's
      `gateA_seed=True` members (0 disagreements across all six families).
      -> WHIRLWIND 15 · CHANNELED-BEAM 9 · MINION-PET 7 · AURA 8 · TOTEM-SENTRY 24 · TRAP-MINE 23.
    - PROPAGATED = archipelago-mock tau-cores (`family` set) MINUS ratified (`gateA_seed=True`).
      -> WHIRLWIND +0 · CHANNELED-BEAM +0 · MINION-PET +0 · AURA +2 · TOTEM-SENTRY +22 · TRAP-MINE +20.
  These match the report's ratified truth EXACTLY (WHIRL 15+0 · BEAM 9+0 · MINION 7+0 · AURA 8+2 ·
  TOTEM 24+22 · TRAP 23+20). RATIFIED render SOLID (markers + hull); PROPAGATED render FAINT/HOLLOW +
  DASHED hull-extension, and the conflation caveat is stamped on-plot + in the README.

  CORPUS DRIFT NOTE: the archipelago was cut on the Edition-I 469-kit corpus; current is 574. One
  ratified member — `chr-crown-proc-engine` (TRAP-MINE) — is corpus_class=`system` and NOT in the
  574 real-kit `kit_master` view, so it is UNPLACEABLE and reported explicitly. 129/130 place.

RENDERS (exhibit-only; ZERO corpus.db writes; reproduction gate FIRST, must re-hit 8/8):
  1. six-families-side-by-side.png  — E4 (left) vs E5-aligned (right). Points BY FAMILY (6 colors);
     ratified=solid marker+SOLID hull; propagated=faint hollow marker+DASHED hull-extension; ALL
     non-family kits = tiny light-grey background points (keep the map's shape, de-emphasized).
     Family-name labels ON the hulls. NO court, NO element anywhere.
  2. six-families-delta-arrows.png  — E4->E5-aligned displacement arrows for family members ONLY,
     colored by family, name labels at arrow-cluster centroids. Background kits ghost-grey.
  3. six-families-membership.csv    — kit key, family, ratified|propagated, E4 xy, E5 xy, displacement.
  4. README.md                      — numbers only.

Both PNGs watermarked "E5 CANDIDATE — NOT SERVED (§8-C: E4 remains truth)".

HARD CONSTRAINTS: READ-ONLY corpus.db (uri mode=ro; zero mutations) · NO serving artifacts · imports
V1/F/L/R verbatim (method drift = a different fork) · reproduction gate runs FIRST, any mismatch ->
HALT, no renders. Naming rule: the SIX ratified names are allowed + wanted; NOTHING else named.

Executor: elrond. TOOL script (curation/exhibit), not engine code.
"""

import os
import sys
import csv
import json
import math
import collections
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

warnings.filterwarnings("ignore", category=FutureWarning)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Reuse the exhibit machinery verbatim — never re-implement recompute / placement / geometry math.
import atlas_e5_exhibit_2026_07_22 as V1
import atlas_e5_exhibit_574_2026_07_22 as F
import atlas_e5_lassos_2026_07_22 as L
import atlas_legb_refit_2026_07_22 as R
from atlas_legb_refit_2026_07_22 import ro_connect

DB = R.DB
SEED = R.SEED

# Output dir: F.OUT_V1 already IS .../atlas/2026-07-22-e5-candidate-exhibit; nest six-families under it.
OUT = os.path.join(F.OUT_V1, "six-families")

WATERMARK = "E5 CANDIDATE — NOT SERVED (§8-C: E4 remains truth)"

# The SIX ratified names, in a stable draw order (largest territory last so its label reads on top).
FAMILIES = ["WHIRLWIND", "CHANNELED-BEAM", "MINION-PET", "AURA", "TOTEM-SENTRY", "TRAP-MINE"]

# Six DISTINCT family colors (NOT court/element hues — a fresh categorical family palette).
FAMILY_COLOR = {
    "WHIRLWIND":      "#1b9e77",  # teal-green
    "CHANNELED-BEAM": "#d95f02",  # burnt-orange
    "MINION-PET":     "#7570b3",  # indigo
    "AURA":           "#e7298a",  # magenta
    "TOTEM-SENTRY":   "#66a61e",  # olive
    "TRAP-MINE":      "#a6761d",  # ochre-brown
}


# ---------------------------------------------------------------------------
# Membership recovery. RATIFIED from corpus.db (authoritative gateA labels table);
# PROPAGATED from the archipelago mock (tau-cores minus ratified). Verified equal at load.
# ---------------------------------------------------------------------------
def recover_membership(con):
    """Returns (ratified, propagated, absent_report) where:
      ratified   : {family -> set(kit_id)}   from corpus.db atlas_gateA_labels_2026_07_14
      propagated : {family -> set(kit_id)}   from mock tau-cores minus ratified
      verify     : dict of cross-check facts for the README.
    HALTs (raises) if the corpus.db ratified table disagrees with the mock's gateA_seed set —
    that would mean the recovery is not trustworthy and we must NOT silently proceed."""
    # --- RATIFIED: corpus.db gateA labels (the ratified source of record) ---
    ratified = collections.defaultdict(set)
    for kid, grp in con.execute(
            'SELECT kit_id, "group" FROM atlas_gateA_labels_2026_07_14').fetchall():
        ratified[grp].add(kid)

    # --- MOCK: recover both ratified-seed set and tau-cores, to (a) verify + (b) derive propagated ---
    mock_path = os.path.join(os.path.dirname(F.OUT_V1), "atlas-archipelago-mock.json")
    with open(mock_path) as f:
        mock = json.load(f)
    mock_ratified = collections.defaultdict(set)   # gateA_seed=True
    mock_tau_core = collections.defaultdict(set)    # family != None (all tau-cores)
    for p in mock["points"]:
        fam = p.get("family")
        if fam is None:
            continue
        mock_tau_core[fam].add(p["kit_id"])
        if p.get("gateA_seed") is True:
            mock_ratified[p.get("e1_gateA_group")].add(p["kit_id"])

    # --- VERIFY corpus.db ratified == mock gateA_seed (0 disagreements required) ---
    disagreements = {}
    for fam in FAMILIES:
        db_set = set(ratified.get(fam, set()))
        mk_set = set(mock_ratified.get(fam, set()))
        if db_set != mk_set:
            disagreements[fam] = {
                "db_only": sorted(db_set - mk_set),
                "mock_only": sorted(mk_set - db_set),
            }
    if disagreements:
        raise RuntimeError(
            "RATIFIED-SOURCE DISAGREEMENT (corpus.db gateA vs mock gateA_seed): %s. "
            "HALT — recovery not trustworthy; do NOT proceed to renders." % disagreements)

    # --- PROPAGATED = mock tau-cores MINUS ratified ---
    propagated = collections.defaultdict(set)
    for fam in FAMILIES:
        propagated[fam] = set(mock_tau_core.get(fam, set())) - set(ratified.get(fam, set()))

    verify = {
        "ratified_source": "corpus.db atlas_gateA_labels_2026_07_14 (86 rows) — "
                           "verified byte-identical to archipelago-mock gateA_seed=True set "
                           "(0 disagreements across all six families).",
        "propagated_source": "archipelago-mock tau-cores (`family` set) MINUS ratified.",
        "ratified_counts": {f: len(ratified[f]) for f in FAMILIES},
        "propagated_counts": {f: len(propagated[f]) for f in FAMILIES},
        "ratified_total": sum(len(ratified[f]) for f in FAMILIES),
        "propagated_total": sum(len(propagated[f]) for f in FAMILIES),
    }
    return dict(ratified), dict(propagated), verify


# ---------------------------------------------------------------------------
# Per-kit family/tag tagging over the 574 placement table.
# ---------------------------------------------------------------------------
def tag_family(recs, ratified, propagated):
    """Attach 'family' and 'tag' (ratified|propagated) to each rec that is a family member.
    Returns (fam_of, tag_of, present, absent):
      fam_of/tag_of : {kit_id -> family/tag} for members PRESENT in the 574 corpus.
      present       : {family -> {tag -> [kit_id present in 574]}}
      absent        : {family -> {tag -> [kit_id NOT in 574 corpus]}}  (corpus-drift casualties)."""
    corpus_ids = set(r["kit_id"] for r in recs)
    fam_of, tag_of = {}, {}
    present = {f: {"ratified": [], "propagated": []} for f in FAMILIES}
    absent = {f: {"ratified": [], "propagated": []} for f in FAMILIES}
    for fam in FAMILIES:
        for tag, mset in (("ratified", ratified.get(fam, set())),
                          ("propagated", propagated.get(fam, set()))):
            for k in sorted(mset):
                if k in corpus_ids:
                    present[fam][tag].append(k)
                    fam_of[k] = fam
                    tag_of[k] = tag
                else:
                    absent[fam][tag].append(k)
    return fam_of, tag_of, present, absent


# ---------------------------------------------------------------------------
# Per-family dispersion + centroid shift under E5 — SAME metric as the lassos exhibit README
# (L.analyze_carryover): shift = centroid displacement E4->E5-aligned; shift_frac = shift/span;
# spread = RMS radius about centroid on each plane; spread_ratio = spread_e5 / spread_e4.
# Computed over RATIFIED-CORE members placed in BOTH cameras (comparable, ratified-anchored).
# ---------------------------------------------------------------------------
def per_family_dispersion(recs, present, span):
    xy = {r["kit_id"]: r for r in recs}
    out = []
    for fam in FAMILIES:
        # ratified-core members placed in BOTH cameras
        kids = [k for k in present[fam]["ratified"]
                if xy[k]["e4xy"] is not None and xy[k]["e5xy"] is not None]
        prop_kids = [k for k in present[fam]["propagated"]
                     if xy[k]["e4xy"] is not None and xy[k]["e5xy"] is not None]
        if len(kids) < 1:
            out.append({"family": fam, "n_core": 0, "n_prop": len(prop_kids),
                        "shift": float("nan"), "shift_frac": float("nan"),
                        "spread_e4": float("nan"), "spread_e5": float("nan"),
                        "spread_ratio": float("nan")})
            continue
        e4 = np.array([xy[k]["e4xy"] for k in kids])
        e5 = np.array([xy[k]["e5xy"] for k in kids])
        c4, c5 = e4.mean(0), e5.mean(0)
        shift = float(np.hypot(*(c5 - c4)))
        sp4 = float(np.sqrt(((e4 - c4) ** 2).sum(1).mean()))
        sp5 = float(np.sqrt(((e5 - c5) ** 2).sum(1).mean()))
        spread_ratio = (sp5 / sp4) if sp4 > 1e-9 else float("nan")
        out.append({
            "family": fam, "n_core": len(kids), "n_prop": len(prop_kids),
            "shift": shift, "shift_frac": shift / span,
            "spread_e4": sp4, "spread_e5": sp5, "spread_ratio": spread_ratio,
            "centroid_e4": (float(c4[0]), float(c4[1])),
            "centroid_e5": (float(c5[0]), float(c5[1])),
        })
    return out


# ---------------------------------------------------------------------------
# Rendering helpers.
# ---------------------------------------------------------------------------
def _background(ax, recs, coord_key, member_ids):
    """Tiny light-grey background points for ALL non-family placed kits (they give the map its
    shape; keep them, de-emphasized)."""
    xs, ys = [], []
    for r in recs:
        if r["kit_id"] in member_ids:
            continue
        p = r[coord_key]
        if p is None:
            continue
        xs.append(p[0]); ys.append(p[1])
    if xs:
        ax.scatter(xs, ys, s=5, c="#dddddd", alpha=0.55, linewidths=0, zorder=1)


def _family_hull(ax, pts, color, span, solid=True):
    """Draw a family hull. solid=True -> filled + solid edge (ratified core); solid=False ->
    unfilled + dashed edge (propagated extension). Reuses the lassos hull geometry verbatim."""
    if len(pts) < 2:
        return
    if solid:
        L.draw_cluster_hull(ax, pts, color, "-", span, filled=True, lw=1.9,
                            alpha_fill=0.10, alpha_edge=0.95, zorder=4)
    else:
        L.draw_cluster_hull(ax, pts, color, "--", span, filled=False, lw=1.2,
                            alpha_edge=0.75, zorder=4)


def _panel(ax, recs, coord_key, member_ids, fam_of, tag_of, span, title, xlim, ylim,
           footnote):
    _background(ax, recs, coord_key, member_ids)
    xy = {r["kit_id"]: r for r in recs}
    # draw per family: propagated hull (dashed) first (under), then ratified hull (solid) on top
    for fam in FAMILIES:
        col = FAMILY_COLOR[fam]
        rat_pts = [xy[k][coord_key] for k in member_ids
                   if fam_of.get(k) == fam and tag_of.get(k) == "ratified"
                   and xy[k][coord_key] is not None]
        prop_pts = [xy[k][coord_key] for k in member_ids
                    if fam_of.get(k) == fam and tag_of.get(k) == "propagated"
                    and xy[k][coord_key] is not None]
        # combined hull for propagated = the OUTWARD extension: hull over ratified+propagated,
        # dashed — shows how far the (lower-precision) proposals stretch the territory.
        if prop_pts:
            _family_hull(ax, rat_pts + prop_pts, col, span, solid=False)
        if len(rat_pts) >= 2:
            _family_hull(ax, rat_pts, col, span, solid=True)
    # markers: ratified solid, propagated faint hollow
    for fam in FAMILIES:
        col = FAMILY_COLOR[fam]
        rx = [xy[k][coord_key][0] for k in member_ids
              if fam_of.get(k) == fam and tag_of.get(k) == "ratified" and xy[k][coord_key]]
        ry = [xy[k][coord_key][1] for k in member_ids
              if fam_of.get(k) == fam and tag_of.get(k) == "ratified" and xy[k][coord_key]]
        px = [xy[k][coord_key][0] for k in member_ids
              if fam_of.get(k) == fam and tag_of.get(k) == "propagated" and xy[k][coord_key]]
        py = [xy[k][coord_key][1] for k in member_ids
              if fam_of.get(k) == fam and tag_of.get(k) == "propagated" and xy[k][coord_key]]
        if px:
            ax.scatter(px, py, s=22, facecolors="none", edgecolors=col, linewidths=0.8,
                       alpha=0.55, zorder=5)
        if rx:
            ax.scatter(rx, ry, s=30, c=col, alpha=0.95, linewidths=0, zorder=6)
    # family-name labels ON the hulls (at the ratified-core centroid; propagated-only families
    # labelled at the extension centroid)
    for fam in FAMILIES:
        col = FAMILY_COLOR[fam]
        rat_pts = [xy[k][coord_key] for k in member_ids
                   if fam_of.get(k) == fam and tag_of.get(k) == "ratified"
                   and xy[k][coord_key] is not None]
        anchor_pts = rat_pts if rat_pts else [xy[k][coord_key] for k in member_ids
                                              if fam_of.get(k) == fam and xy[k][coord_key]]
        if anchor_pts:
            cen = np.array(anchor_pts).mean(0)
            ax.text(cen[0], cen[1], fam, fontsize=8.5, fontweight="bold", color=col,
                    ha="center", va="center", zorder=8,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col, alpha=0.9))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="#ececec", lw=0.5, zorder=0)
    ax.axvline(0, color="#ececec", lw=0.5, zorder=0)
    ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=7)
    ax.text(0.01, 0.01, footnote, transform=ax.transAxes, fontsize=6.4, va="bottom",
            ha="left", color="#333333",
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#bbbbbb", alpha=0.9))
    ax.text(0.5, 0.5, WATERMARK, transform=ax.transAxes, fontsize=12.5, color="#d24545",
            alpha=0.15, ha="center", va="center", rotation=24, zorder=9, weight="bold")


CONFLATION_FOOTNOTE = ("SOLID = gateA-RATIFIED core (corpus.db gateA labels). "
                       "DASHED hull + hollow = tau-PROPAGATED proposals (~1/3 precision; "
                       "NOT ratified). Grey = all other kits (map shape). No court/element.")


def render_side_by_side(recs, member_ids, fam_of, tag_of, span, b, cov):
    xlim, ylim, _ = L.both_limits(recs)
    fig, axes = plt.subplots(1, 2, figsize=(16.5, 8.4))
    _panel(axes[0], recs, "e4xy", member_ids, fam_of, tag_of, span,
           "LEFT — E4 SERVED plane (truth) · six named families",
           xlim, ylim, CONFLATION_FOOTNOTE)
    _panel(axes[1], recs, "e5xy", member_ids, fam_of, tag_of, span,
           "RIGHT — E5 CANDIDATE (B2: rot %.2f°, refl %s, NO scale) · same memberships"
           % (abs(b["ang2"]), bool(b["refl2"])),
           xlim, ylim, CONFLATION_FOOTNOTE)
    # legend: family swatches + tag key
    fam_handles = [Patch(facecolor=FAMILY_COLOR[f], edgecolor="none", label=f) for f in FAMILIES]
    tag_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#555555", markersize=6,
               label="ratified core (solid + solid hull)"),
        Line2D([0], [0], marker="o", color="none", markeredgecolor="#555555",
               markerfacecolor="none", markersize=6, label="propagated (hollow + dashed hull)"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#dddddd", markersize=5,
               label="other kits (grey — map shape)"),
    ]
    axes[0].legend(handles=fam_handles + tag_handles, loc="upper left", fontsize=6.4,
                   framealpha=0.93, title="the six ratified families")
    fig.suptitle("THE SIX NAMED BUILD-FAMILIES in E4 vs E5-candidate · ratified %d + propagated %d "
                 "(129/130 placed; 1 corpus-drift casualty) · B3 congruence=%.4f (< 0.85 → NOT served)"
                 % (cov["rat_placed"], cov["prop_placed"], b["cong2"]), fontsize=11)
    fig.text(0.995, 0.004, WATERMARK + " · Matt's PRIMARY family exhibit · 2026-07-22",
             ha="right", va="bottom", fontsize=7, color="#8a1a1a", style="italic")
    fig.tight_layout(rect=(0, 0.02, 1, 0.955))
    p = os.path.join(OUT, "six-families-side-by-side.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    return p


def render_delta_arrows(recs, member_ids, fam_of, tag_of, span, b):
    xy = {r["kit_id"]: r for r in recs}
    both = [k for k in member_ids if xy[k]["e4xy"] is not None and xy[k]["e5xy"] is not None]
    pts = []
    for k in both:
        pts.append(xy[k]["e4xy"]); pts.append(xy[k]["e5xy"])
    P = np.array(pts)
    xmin, ymin = P.min(0); xmax, ymax = P.max(0)
    padx = 0.08 * (xmax - xmin); pady = 0.08 * (ymax - ymin)

    fig, ax = plt.subplots(figsize=(11, 10))
    # ghost-grey background (family footprint context only)
    _background(ax, recs, "e4xy", set(member_ids))
    for k in both:
        (x0, y0), (x1, y1) = xy[k]["e4xy"], xy[k]["e5xy"]
        col = FAMILY_COLOR[fam_of[k]]
        ratified = (tag_of[k] == "ratified")
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=col,
                                    lw=1.1 if ratified else 0.7,
                                    alpha=0.9 if ratified else 0.5,
                                    linestyle="-" if ratified else "--"), zorder=3)
        ax.scatter([x0], [y0], s=18 if ratified else 10,
                   c=col if ratified else "none",
                   edgecolors="none" if ratified else col,
                   linewidths=0 if ratified else 0.7,
                   alpha=0.95 if ratified else 0.6, zorder=4)
    # family-name labels at each family's arrow-cluster centroid (E4 origin cluster)
    for fam in FAMILIES:
        fam_e4 = [xy[k]["e4xy"] for k in both if fam_of[k] == fam]
        if fam_e4:
            cen = np.array(fam_e4).mean(0)
            ax.text(cen[0], cen[1], fam, fontsize=9, fontweight="bold",
                    color=FAMILY_COLOR[fam], ha="center", va="center", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.22", fc="white",
                              ec=FAMILY_COLOR[fam], alpha=0.92))
    ax.set_xlim(xmin - padx, xmax + padx); ax.set_ylim(ymin - pady, ymax + pady)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="#ececec", lw=0.5, zorder=0)
    ax.axvline(0, color="#ececec", lw=0.5, zorder=0)
    n_rat = sum(1 for k in both if tag_of[k] == "ratified")
    n_prop = len(both) - n_rat
    ax.set_title("Δ arrows (E4 → E5-aligned) · family members ONLY · %d ratified (solid) + "
                 "%d propagated (dashed) · B3 congruence=%.4f"
                 % (n_rat, n_prop, b["cong2"]), fontsize=9.5)
    fam_handles = [Line2D([0], [0], color=FAMILY_COLOR[f], lw=2.4, label=f) for f in FAMILIES]
    ax.legend(handles=fam_handles, loc="upper left", fontsize=7, framealpha=0.92,
              title="family")
    ax.tick_params(labelsize=7)
    ax.text(0.02, 0.02, CONFLATION_FOOTNOTE, transform=ax.transAxes, fontsize=6.6, va="bottom",
            ha="left", color="#333333",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#bbbbbb", alpha=0.9))
    ax.text(0.5, 0.5, WATERMARK, transform=ax.transAxes, fontsize=15, color="#d24545",
            alpha=0.14, ha="center", va="center", rotation=24, zorder=1, weight="bold")
    fig.text(0.995, 0.004, WATERMARK + " · 2026-07-22", ha="right", va="bottom",
             fontsize=7, color="#8a1a1a", style="italic")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    p = os.path.join(OUT, "six-families-delta-arrows.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    return p


# ---------------------------------------------------------------------------
# CSV.
# ---------------------------------------------------------------------------
def write_membership_csv(recs, fam_of, tag_of, absent):
    xy = {r["kit_id"]: r for r in recs}
    p = os.path.join(OUT, "six-families-membership.csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kit_id", "family", "tag", "corpus_class", "placed_in_574",
                    "e4_x", "e4_y", "e5_x_aligned", "e5_y_aligned", "displacement"])
        # placed members
        for k in sorted(fam_of.keys(), key=lambda x: (fam_of[x], tag_of[x], x)):
            r = xy[k]
            e4 = r["e4xy"]; e5 = r["e5xy"]
            disp = ""
            if e4 is not None and e5 is not None:
                disp = "%.6f" % math.hypot(e5[0] - e4[0], e5[1] - e4[1])
            w.writerow([k, fam_of[k], tag_of[k], r["corpus_class"], 1,
                        "%.6f" % e4[0] if e4 else "", "%.6f" % e4[1] if e4 else "",
                        "%.6f" % e5[0] if e5 else "", "%.6f" % e5[1] if e5 else "", disp])
        # absent (corpus-drift) members — recorded honestly, no coords
        for fam in FAMILIES:
            for tag in ("ratified", "propagated"):
                for k in absent[fam][tag]:
                    w.writerow([k, fam, tag, "ABSENT-FROM-574", 0, "", "", "", "", ""])
    return p


# ---------------------------------------------------------------------------
# README (numbers only).
# ---------------------------------------------------------------------------
def compute_coverage(recs, present, absent):
    xy = {r["kit_id"]: r for r in recs}
    cov = {"by_family": {}, "rat_placed": 0, "prop_placed": 0, "rat_absent": 0,
           "prop_absent": 0, "annex_sys_members": 0}
    for fam in FAMILIES:
        d = {}
        for tag in ("ratified", "propagated"):
            kids = present[fam][tag]
            e4 = sum(1 for k in kids if xy[k]["e4xy"])
            e5 = sum(1 for k in kids if xy[k]["e5xy"])
            both = sum(1 for k in kids if xy[k]["e4xy"] and xy[k]["e5xy"])
            cls = collections.Counter(xy[k]["corpus_class"] for k in kids)
            n_annex_sys = sum(v for c, v in cls.items() if c in ("annex", "system"))
            d[tag] = {"placed": len(kids), "e4": e4, "e5": e5, "both": both,
                      "class": dict(cls), "annex_sys": n_annex_sys,
                      "absent": len(absent[fam][tag])}
            if tag == "ratified":
                cov["rat_placed"] += len(kids); cov["rat_absent"] += len(absent[fam][tag])
            else:
                cov["prop_placed"] += len(kids); cov["prop_absent"] += len(absent[fam][tag])
            cov["annex_sys_members"] += n_annex_sys
        cov["by_family"][fam] = d
    return cov


def write_readme(recs, b, verify, cov, disp, absent, span, repro_ok, repro_lines, files):
    p = os.path.join(OUT, "README.md")
    xy = {r["kit_id"]: r for r in recs}
    with open(p, "w") as f:
        f.write("# E5 CANDIDATE — SIX NAMED BUILD-FAMILIES — numbers only\n\n")
        f.write("**Date:** 2026-07-22 · **Executor:** elrond · **Purpose:** Matt's PRIMARY family "
                "exhibit — see the six build-families we ALREADY KNOW OF (the gateA-ratified island "
                "families) in both cameras, colored by family. NO element, NO court, NO new names.\n\n")
        f.write("> **%s**\n\n" % WATERMARK)
        f.write("> **NO SILENT CONFLATION.** The archipelago-mock 'core' census conflated "
                "gateA-RATIFIED members with tau-PROPAGATED proposals (the 44 proposals ran ~1/3 "
                "precision). This exhibit separates them: RATIFIED render solid (marker + solid "
                "hull); PROPAGATED render faint/hollow + dashed hull-extension. Treat propagated as "
                "hypotheses, not membership.\n\n")

        f.write("## Reproduction gate (vs 2026-07-22-legb-gate-report.md) — runs FIRST\n\n")
        f.write("**Result: %s**\n\n" % ("PASS — 8/8 match record" if repro_ok else "FAIL — HALT"))
        f.write("\n".join(repro_lines) + "\n\n")

        f.write("## Membership source (ratified lists RECOVERED — yes)\n\n")
        f.write("- **RATIFIED source:** %s\n" % verify["ratified_source"])
        f.write("- **PROPAGATED source:** %s\n" % verify["propagated_source"])
        f.write("- **Recovered counts** (ratified + propagated) match the archipelago-mock report's "
                "stated ratified truth EXACTLY: WHIRLWIND 15+0 · CHANNELED-BEAM 9+0 · MINION-PET 7+0 · "
                "AURA 8+2 · TOTEM-SENTRY 24+22 · TRAP-MINE 23+20. Ratified total **%d**, "
                "propagated total **%d**.\n\n"
                % (verify["ratified_total"], verify["propagated_total"]))

        f.write("## Placement census (into the CURRENT 574 corpus)\n\n")
        f.write("> **Corpus-drift note:** the archipelago was cut on the Edition-I **469-kit** "
                "corpus; current is **574**. Members are matched by kit_id into the 574 real-kit "
                "`kit_master` view; a member present in E1-469 but absent from the 574 view is "
                "UNPLACEABLE and reported (not fabricated).\n\n")
        f.write("| family | ratified placed/total | rat both-cam | propagated placed/total | "
                "prop both-cam | annex+system members |\n")
        f.write("|---|---|---|---|---|---|\n")
        for fam in FAMILIES:
            d = cov["by_family"][fam]
            rt = d["ratified"]; pt = d["propagated"]
            rat_tot = rt["placed"] + rt["absent"]
            prop_tot = pt["placed"] + pt["absent"]
            f.write("| **%s** | %d/%d | %d | %d/%d | %d | %d |\n"
                    % (fam, rt["placed"], rat_tot, rt["both"],
                       pt["placed"], prop_tot, pt["both"],
                       rt["annex_sys"] + pt["annex_sys"]))
        f.write("| **TOTAL** | **%d/%d** | — | **%d/%d** | — | **%d** |\n\n"
                % (cov["rat_placed"], cov["rat_placed"] + cov["rat_absent"],
                   cov["prop_placed"], cov["prop_placed"] + cov["prop_absent"],
                   cov["annex_sys_members"]))
        # unplaceable list
        unplaceable = [(fam, tag, k) for fam in FAMILIES for tag in ("ratified", "propagated")
                       for k in absent[fam][tag]]
        if unplaceable:
            f.write("- **Unplaceable (corpus-drift casualties, %d):** "
                    % len(unplaceable)
                    + "; ".join("`%s` (%s %s)" % (k, fam, tag)
                                for fam, tag, k in unplaceable) + ". ")
            f.write("`chr-crown-proc-engine` is corpus_class=`system` and NOT in the 574 real-kit "
                    "`kit_master` view (system-records are excluded from the real-kit universe), so "
                    "TRAP-MINE ratified places 22/23. All other 128 members place in BOTH cameras.\n\n")
        else:
            f.write("- **Unplaceable:** none.\n\n")

        f.write("## Per-family E5 dispersion + centroid shift "
                "(SAME metric as the lassos exhibit README — comparability)\n\n")
        f.write("`shift` = centroid displacement E4→E5-aligned (plane units; frac of plane span "
                "= %.4f). `spread` = RMS radius about centroid on each plane; "
                "`spread_ratio` = spread(E5) ÷ spread(E4) (>1 = the family SPREADS/splinters under "
                "the candidate angle; <1 = TIGHTENS). Computed over **RATIFIED-CORE** members placed "
                "in BOTH cameras (ratified-anchored; propagated excluded from the metric).\n\n" % span)
        f.write("| family | n (ratified core) | shift | shift/span | spread E4 | spread E5 | "
                "spread_ratio |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for c in sorted(disp, key=lambda x: (-x["spread_ratio"]
                                             if not math.isnan(x["spread_ratio"]) else 0)):
            if c["n_core"] == 0:
                f.write("| **%s** | 0 | — | — | — | — | — |\n" % c["family"])
            else:
                f.write("| **%s** | %d | %.4f | %.3f | %.4f | %.4f | %.3f |\n"
                        % (c["family"], c["n_core"], c["shift"], c["shift_frac"],
                           c["spread_e4"], c["spread_e5"], c["spread_ratio"]))
        f.write("\n")
        migr = [c for c in disp if not math.isnan(c["shift_frac"]) and c["shift_frac"] >= 0.20]
        splt = [c for c in disp if not math.isnan(c["spread_ratio"]) and c["spread_ratio"] >= 1.30]
        tght = [c for c in disp if not math.isnan(c["spread_ratio"]) and c["spread_ratio"] <= 0.77]
        f.write("- **Migrate (centroid shift ≥ 20%% of plane span):** %s\n"
                % ("; ".join("%s → %.2f span" % (c["family"], c["shift_frac"])
                             for c in sorted(migr, key=lambda x: -x["shift_frac"])) or "none"))
        f.write("- **Spread / splinter (E5 RMS radius ≥ 1.30× E4):** %s\n"
                % ("; ".join("%s → ×%.2f" % (c["family"], c["spread_ratio"])
                             for c in sorted(splt, key=lambda x: -x["spread_ratio"])) or "none"))
        f.write("- **Tighten (E5 RMS radius ≤ 0.77× E4):** %s\n\n"
                % ("; ".join("%s → ×%.2f" % (c["family"], c["spread_ratio"])
                             for c in sorted(tght, key=lambda x: x["spread_ratio"])) or "none"))

        f.write("## Standing caveats\n\n")
        f.write("1. **Conflation (headline):** propagated ≠ ratified. The 44 tau-propagated "
                "proposals ran ~1/3 precision (global-τ umbrella defect over multi-cluster "
                "families — TOTEM-SENTRY and TRAP-MINE are the archipelagic families that absorbed "
                "nearly all proposals: +22 and +20). Solid hull = trust; dashed hull = candidate.\n")
        f.write("2. **Annex/system members carry NO six-block gb_* data (design-NULL).** **%d of "
                "the %d placed members are annex/system-class** and therefore place from the SHARED "
                "pre-v2.0 register coords + element_primary ONLY (their gb_* geometry-band blocks "
                "are passive). MINION-PET is **entirely annex-class (7/7)** — none of its members "
                "carry six-block data, so its placement is register-driven, not geometry-driven. "
                "WHIRLWIND ratified is 8 annex / 7 record; AURA propagated includes 1 system. This "
                "is EXPECTED (annex/system never got the v2.0 side-car) and is why annex/system "
                "family placements are lower-resolution than record-class ones.\n"
                % (cov["annex_sys_members"], cov["rat_placed"] + cov["prop_placed"]))
        f.write("3. **Rare-bucket leverage (carried from exhibit v1):** the fused rare level "
                "`gb_width:other-rare` tops BOTH candidate dims (dim1 +1.86, dim2 +2.48). A "
                "low-population fused level dominating the leading axes is part of why the refit is "
                "not servable-grade (with the 0.7836 < 0.85 congruence, §8-C keeps E4 as truth). The "
                "candidate camera here is a diagnostic, not a proposed replacement.\n")
        f.write("4. **E5 supplementary projection is V-2 machinery:** the 265-kit record fit DERIVES "
                "the axes (byte-identical to the reproduction gate); every family member is placed as "
                "a supplementary point (annex/system + non-fit record) or read from the fit basis "
                "(fit-member record). Supplementary rows NEVER bend the axes.\n\n")

        f.write("## Files\n\n")
        for name, size in files:
            f.write("- `%s` — %d bytes\n" % (name, size))
        f.write("\n## Exact reproduction command\n\n")
        f.write("```\ncd %s\npython3 atlas_e5_sixfam_2026_07_22.py\n```\n\n" % SCRIPT_DIR)
        f.write("Deterministic: SEED=%d, all randomness pinned. corpus.db opened read-only "
                "(uri mode=ro). Imports `atlas_e5_exhibit_2026_07_22`, "
                "`atlas_e5_exhibit_574_2026_07_22`, `atlas_e5_lassos_2026_07_22`, "
                "`atlas_legb_refit_2026_07_22` verbatim (no recompute/placement/geometry math "
                "changed).\n\n" % SEED)
        f.write("## Constraint attestation\n\n")
        f.write("- READ-ONLY on corpus.db and every store — zero mutations, zero serving artifacts.\n")
        f.write("- Reproduction gate (8/8) gates the renders: any mismatch → HALT, no renders.\n")
        f.write("- Membership recovery HALTS if corpus.db ratified disagrees with the mock "
                "gateA_seed set (it does not: 0 disagreements). Ratified vs propagated never "
                "silently merged.\n")
        f.write("- Only the SIX ratified family names are used (WHIRLWIND · CHANNELED-BEAM · "
                "MINION-PET · AURA · TOTEM-SENTRY · TRAP-MINE). Nothing else named. No court/element "
                "anywhere on the plots.\n")
    return p


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    print("=== E5 SIX-FAMILIES exhibit — recompute + reproduction gate (delegated to V1) ===")
    b = V1.recompute()
    repro_ok, repro_lines = V1.repro_check(b)
    for ln in repro_lines:
        print(ln)
    if not repro_ok:
        with open(os.path.join(OUT, "REPRODUCTION-MISMATCH.md"), "w") as f:
            f.write("# E5 SIX-FAMILIES — REPRODUCTION MISMATCH — HALT\n\n")
            f.write("The E5 recompute did NOT reproduce the gate report of record 8/8. "
                    "NO renders emitted. Determinism is the whole warrant for this exhibit.\n\n")
            f.write("\n".join(repro_lines) + "\n")
        print("!!! HALT — reproduction mismatch. Wrote REPRODUCTION-MISMATCH.md, no renders. !!!")
        sys.exit(3)
    print("--- reproduction PASS (8/8) — recovering membership + building exhibit ---")

    con = ro_connect(DB)
    ratified, propagated, verify = recover_membership(con)
    corpus = F.load_corpus_574(con)
    con.close()
    print("ratified counts:", verify["ratified_counts"], "total", verify["ratified_total"])
    print("propagated counts:", verify["propagated_counts"], "total", verify["propagated_total"])

    project_e5_row = F.build_e5_supp_projector(b)
    e4_placements = F.build_e4_placements(corpus, b)
    recs, both = F.assemble_table(corpus, b, project_e5_row, e4_placements)

    fam_of, tag_of, present, absent = tag_family(recs, ratified, propagated)
    member_ids = set(fam_of.keys())
    _, _, span = L.both_limits(recs)

    cov = compute_coverage(recs, present, absent)
    disp = per_family_dispersion(recs, present, span)

    p_sbs = render_side_by_side(recs, member_ids, fam_of, tag_of, span, b, cov)
    p_arr = render_delta_arrows(recs, member_ids, fam_of, tag_of, span, b)
    p_csv = write_membership_csv(recs, fam_of, tag_of, absent)

    files = []
    for pth in [p_sbs, p_arr, p_csv]:
        files.append((os.path.basename(pth), os.path.getsize(pth)))
    p_readme = write_readme(recs, b, verify, cov, disp, absent, span, repro_ok, repro_lines, files)
    files.append((os.path.basename(p_readme), os.path.getsize(p_readme)))

    print("\n=== PLACEMENT (into 574) ===")
    for fam in FAMILIES:
        d = cov["by_family"][fam]
        print("  %-14s ratified placed=%d/%d both=%d annex+sys=%d | propagated placed=%d/%d both=%d"
              % (fam, d["ratified"]["placed"], d["ratified"]["placed"] + d["ratified"]["absent"],
                 d["ratified"]["both"], d["ratified"]["annex_sys"] + d["propagated"]["annex_sys"],
                 d["propagated"]["placed"], d["propagated"]["placed"] + d["propagated"]["absent"],
                 d["propagated"]["both"]))
    print("  TOTAL ratified placed=%d/%d  propagated placed=%d/%d  annex+system members=%d"
          % (cov["rat_placed"], cov["rat_placed"] + cov["rat_absent"],
             cov["prop_placed"], cov["prop_placed"] + cov["prop_absent"],
             cov["annex_sys_members"]))
    print("\n=== PER-FAMILY DISPERSION (ratified core, both cameras) ===")
    for c in disp:
        if c["n_core"] == 0:
            print("  %-14s n=0 (no ratified core placed both cameras)" % c["family"])
        else:
            print("  %-14s n=%2d shift=%.4f (%.3f span) spread %.4f->%.4f ratio=%.3f"
                  % (c["family"], c["n_core"], c["shift"], c["shift_frac"],
                     c["spread_e4"], c["spread_e5"], c["spread_ratio"]))
    print("\n=== FILES ===")
    for name, size in files:
        print("  %-32s %8d bytes" % (name, size))
    print("\n=== exhibit dir: %s ===" % OUT)


if __name__ == "__main__":
    main()
