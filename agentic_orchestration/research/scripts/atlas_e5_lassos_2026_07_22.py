#!/usr/bin/env python3
"""
atlas_e5_lassos_2026_07_22.py — E5 CANDIDATE BUILD-FAMILY LASSOS (elrond, 2026-07-22)
================================================================================
EXHIBIT-ONLY visual scaffolding for Matt's camera-fork ruling. Draws build-family
clusters as enclosing HULLS ("lassos") on the two cameras (E4 SERVED plane + E5
CANDIDATE-aligned plane), so Matt can SEE how build families reorient/tighten/splinter
under the candidate angle before ruling.

  reproduction + placement of record: atlas_e5_exhibit_2026_07_22.py  (V1: recompute + gate)
                                       atlas_e5_exhibit_574_2026_07_22.py (F: 574 placement)
  refit of record (imported, NOT modified): atlas_legb_refit_2026_07_22.py (R)
  gate report of record:               2026-07-22-legb-gate-report.md
  §8-C VERDICT: B3 congruence 0.7836 < 0.85 -> E5 NOT served, E4 remains truth.

CRITICAL GOVERNANCE (Matt hold): canonical island-cutting and family NAMING are GATED.
These lassos are EXHIBIT-ONLY. Clusters carry NEUTRAL LETTER labels (A, B, C…) and
numbers-only legends. NO thematic names, NO archetype names, NO island names. Every
render carries BOTH watermarks.

WHAT IS NEW vs the 574 exhibit:
  - CUT A — E4-carryover families. Cluster on the E4 SERVED plane using ALL 561 kits placed
    in BOTH cameras (stored + supplementary projections). Draw each cluster's hull on the E4
    panel, then draw the SAME MEMBERSHIP's hull on the E5-aligned panel -> shows how E4's
    families reorient under the candidate angle. -> lassos-e4-carryover.png
  - CUT B — E5-native families. Cluster FRESH on the E5-candidate-aligned plane using
    RECORD-CLASS ONLY (265 axis-deriving fit members). Rationale HONORED: annex/system E5
    placements derive from SHARED older vocabulary only (no six-block gb_* data) — cutting
    families from those draped placements would MANUFACTURE structure. Draw hulls on the E5
    panel; outline the same memberships back on the E4 panel (dashed). -> lassos-e5-native.png

CLUSTERING METHOD (decision tree, documented in README):
  - HDBSCAN (sklearn.cluster.HDBSCAN) is attempted FIRST for each cut (noise stays UNLASSOED
    — honest). If HDBSCAN under-resolves for legibility — a single hull covering the bulk of
    points ("giant blob"), OR fewer than 5 clusters — we FALL BACK to k-means with
    silhouette-selected k in [5, 10] for that cut (the task-sanctioned fallback). The chosen
    method + params + the rejected HDBSCAN result are BOTH recorded in the README.
  - Target 5–10 hulls per cut. Hulls are PADDED convex hulls (outward-offset), rendered with
    translucent fills + distinct edge styles so overlaps stay legible. Degenerate clusters
    (<3 points) drawn as a small ring / segment.

LEGEND per cluster (numbers only): letter label · n members · corpus_class split ·
court composition % (ratified k=5: physical/fire/cold/lightning/chaos-poison/NULL) ·
top-3 gb_* register tokens among RECORD-class members (ratified mechanical vocabulary from
the six-block side-car, e.g. gb_delivery:melee_arc, gb_motion:point_strike). Register tokens
are RATIFIED and allowed; interpretive family names are NOT.

HARD CONSTRAINTS honored:
  - READ-ONLY on corpus.db and every store (uri mode=ro; zero mutations).
  - NO serving artifacts. All outputs under a lassos/ subdir of the E5 exhibit dir.
  - Imports V1 + F + R verbatim (method drift = a different fork). REPRODUCTION GATE runs
    FIRST (delegates to V1.recompute + V1.repro_check); any mismatch -> HALT, no renders.

Executor: elrond. TOOL script (curation/exhibit), not engine code.
"""

import os
import sys
import csv
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon as MplPolygon, Circle

from scipy.spatial import ConvexHull
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.metrics import silhouette_score

# sklearn HDBSCAN copy-default FutureWarning is noise for this deterministic tool.
warnings.filterwarnings("ignore", category=FutureWarning)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Reuse the exhibit machinery verbatim — never re-implement the recompute / placement math.
import atlas_e5_exhibit_2026_07_22 as V1
import atlas_e5_exhibit_574_2026_07_22 as F
import atlas_legb_refit_2026_07_22 as R
from atlas_legb_refit_2026_07_22 import ro_connect, BAND_NAMES

DB = R.DB
SEED = R.SEED
OUT = os.path.join(F.OUT_V1, "lassos")   # new subdir under the E5 exhibit dir

# BOTH watermarks — every render carries them.
WM_NOTSERVED = "E5 CANDIDATE — NOT SERVED (§8-C: E4 remains truth)"
WM_UNNAMED = ("EXHIBIT-ONLY — families UNNAMED; island cut + naming remain gated "
              "(Matt hold)")

# Ratified k=5 element-courts -> composition color for legend swatches (court-NULL = grey).
COURT_ORDER = ["physical", "fire", "cold", "lightning", "chaos-poison"]
COURT_COLOR = {
    "physical":     "#8a8f98",
    "fire":         "#e2571e",
    "cold":         "#2b8fd6",
    "lightning":    "#e6b800",
    "chaos-poison": "#8f3fbf",
}
NULL_COURT_COLOR = "#cfcfcf"

# Neutral cluster palette (letters A..). Distinct hues; hull edge styles cycle for overlap legibility.
CLUSTER_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#17becf", "#bcbd22", "#7f7f7f",
]
EDGE_STYLES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1)),
               "-", "--", "-.", ":", (0, (5, 2))]
LETTERS = "ABCDEFGHIJ"

# gb_* block -> the skill_geometry_band column carrying its ratified token vocabulary.
GB_COL = {
    "gb_delivery": "delivery_class",
    "gb_range":    "range_band",
    "gb_motion":   "motion_signature",
    "gb_width":    "width_band",
    "gb_speed":    "speed_band",
    "gb_cadence":  "cadence_class",
}


# ---------------------------------------------------------------------------
# Register-token side-car: ordinal-0 gb_* tokens per RECORD-class kit (ratified vocabulary).
# ---------------------------------------------------------------------------
def load_gb_tokens(con):
    """kit_id -> {gb_block: token} for skill_ordinal=0. Only record-class kits carry these
    (annex/system have NONE by design). NULL tokens are omitted (not counted as a token)."""
    out = {}
    rows = con.execute(
        "SELECT kit_id, delivery_class, range_band, motion_signature, "
        "width_band, speed_band, cadence_class "
        "FROM skill_geometry_band WHERE skill_ordinal=0").fetchall()
    cols = ["gb_delivery", "gb_range", "gb_motion", "gb_width", "gb_speed", "gb_cadence"]
    for r in rows:
        kid = r[0]
        d = {}
        for i, nm in enumerate(cols):
            v = r[i + 1]
            if v is not None and str(v).strip() != "":
                d[nm] = str(v)
        out[kid] = d
    return out


# ---------------------------------------------------------------------------
# Clustering with the documented HDBSCAN-first / silhouette-k-means fallback decision.
# ---------------------------------------------------------------------------
def _sizes(labels):
    import collections
    c = collections.Counter(labels)
    nz = sorted(k for k in c if k >= 0)
    return len(nz), c.get(-1, 0), [c[k] for k in nz]


def cluster_plane(X, cut_name, min_cluster_size=10, min_samples=5, blob_frac=0.55):
    """Return (labels, method_dict). HDBSCAN first; fall back to silhouette k-means if it
    under-resolves for legibility (a hull over > blob_frac of points, or < 5 clusters).
    labels: -1 = noise (k-means never emits -1). Deterministic (SEED-pinned)."""
    method = {"cut": cut_name}
    # --- attempt HDBSCAN ---
    h = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples).fit(X)
    hk, hnoise, hsizes = _sizes(h.labels_)
    biggest = max(hsizes) if hsizes else 0
    method["hdbscan"] = {
        "min_cluster_size": min_cluster_size, "min_samples": min_samples,
        "k": hk, "noise": hnoise, "sizes": hsizes,
        "biggest_frac": (biggest / len(X)) if len(X) else 0.0,
    }
    giant_blob = (biggest / len(X) > blob_frac) if len(X) else True
    under = (hk < 5)
    if not giant_blob and not under and hk <= 10:
        method["chosen"] = "hdbscan"
        method["reason"] = ("HDBSCAN gave k=%d (noise=%d) with no giant blob "
                            "(largest hull = %.0f%% of points) -> legible; used as-is."
                            % (hk, hnoise, 100.0 * biggest / len(X)))
        return h.labels_, method
    # --- fall back to silhouette k-means (task-sanctioned) ---
    reject = []
    if giant_blob:
        reject.append("largest HDBSCAN hull = %.0f%% of points (> %.0f%% giant-blob gate)"
                      % (100.0 * biggest / len(X), 100.0 * blob_frac))
    if under:
        reject.append("HDBSCAN k=%d < 5 (below legibility floor)" % hk)
    if hk > 10:
        reject.append("HDBSCAN k=%d > 10 (above legibility ceiling)" % hk)
    best_k, best_s, best_labels = None, -2.0, None
    sweep = []
    for k in range(5, 11):
        km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(X)
        s = float(silhouette_score(X, km.labels_))
        sweep.append((k, s))
        if s > best_s:
            best_k, best_s, best_labels = k, s, km.labels_
    method["chosen"] = "kmeans"
    method["kmeans"] = {"k": best_k, "silhouette": best_s, "sweep": sweep,
                        "sizes": _sizes(best_labels)[2]}
    method["reason"] = ("HDBSCAN rejected (%s). Fell back to silhouette k-means: "
                        "best k=%d (silhouette=%.4f over k in [5,10])."
                        % ("; ".join(reject), best_k, best_s))
    return best_labels, method


# ---------------------------------------------------------------------------
# Per-cluster summary (numbers only): n, class split, court %, top-3 gb_* tokens (record only).
# ---------------------------------------------------------------------------
def summarize_clusters(members_by_label, rec_by_kit, gb_tokens):
    """members_by_label: {label(int) -> [kit_id]} (label -1 excluded by caller).
    Returns ordered list of dicts keyed by letter, sorted by descending n."""
    import collections
    summaries = []
    for lab, kids in members_by_label.items():
        n = len(kids)
        cls = collections.Counter(rec_by_kit[k]["corpus_class"] for k in kids)
        court = collections.Counter(
            (rec_by_kit[k]["court"] if rec_by_kit[k]["court"] in COURT_COLOR else "NULL")
            for k in kids)
        court_pct = []
        for c in COURT_ORDER + ["NULL"]:
            if court.get(c, 0):
                court_pct.append((c, court[c], 100.0 * court[c] / n))
        # top gb_* tokens among RECORD-class members only (block:value)
        tok = collections.Counter()
        n_rec_with_tok = 0
        for k in kids:
            if rec_by_kit[k]["corpus_class"] != "record":
                continue
            d = gb_tokens.get(k, {})
            if d:
                n_rec_with_tok += 1
            for block, val in d.items():
                tok["%s:%s" % (block, val)] += 1
        top_tok = tok.most_common(3)
        summaries.append({
            "label": lab, "n": n, "kids": kids,
            "class": dict(cls), "court_pct": court_pct,
            "top_tokens": top_tok, "n_rec": cls.get("record", 0),
            "n_rec_with_tok": n_rec_with_tok,
        })
    summaries.sort(key=lambda s: -s["n"])
    for i, s in enumerate(summaries):
        s["letter"] = LETTERS[i]
    return summaries


# ---------------------------------------------------------------------------
# Hull geometry: padded convex hull (outward offset from centroid). Degenerate -> ring/segment.
# ---------------------------------------------------------------------------
def hull_polygon(points, pad_frac=0.06, global_span=1.0):
    """points: (m,2). Returns an ordered (h,2) padded hull vertex array, OR None if <3 unique
    points (caller draws a ring/segment instead). Padding is an outward offset from the hull
    centroid plus a small absolute pad scaled by the global plane span."""
    P = np.asarray(points, float)
    uniq = np.unique(P, axis=0)
    if len(uniq) < 3:
        return None
    try:
        hull = ConvexHull(uniq)
    except Exception:
        return None
    verts = uniq[hull.vertices]
    cen = verts.mean(0)
    pad_abs = pad_frac * global_span
    out = []
    for v in verts:
        d = v - cen
        nrm = np.hypot(d[0], d[1])
        if nrm < 1e-9:
            out.append(v)
        else:
            out.append(v + d / nrm * pad_abs + d * pad_frac)
    return np.array(out)


def draw_cluster_hull(ax, points, color, edge_style, global_span, filled=True, lw=1.6,
                      alpha_fill=0.11, alpha_edge=0.9, zorder=3):
    """Draw one cluster's lasso. Padded convex hull where possible; ring for <3 points,
    segment for exactly 2."""
    P = np.asarray(points, float)
    poly = hull_polygon(P, global_span=global_span)
    if poly is not None:
        if filled:
            ax.add_patch(MplPolygon(poly, closed=True, facecolor=color, edgecolor="none",
                                    alpha=alpha_fill, zorder=zorder - 1))
        ax.add_patch(MplPolygon(poly, closed=True, facecolor="none", edgecolor=color,
                                linewidth=lw, linestyle=edge_style, alpha=alpha_edge,
                                zorder=zorder))
    else:
        uniq = np.unique(P, axis=0)
        cen = uniq.mean(0)
        if len(uniq) == 2:
            ax.plot(uniq[:, 0], uniq[:, 1], color=color, lw=lw, linestyle=edge_style,
                    alpha=alpha_edge, zorder=zorder)
        r = max(0.04 * global_span, 1e-3)
        ax.add_patch(Circle(cen, r, facecolor=color if filled else "none", edgecolor=color,
                            alpha=alpha_fill if filled else alpha_edge, lw=lw,
                            linestyle=edge_style, zorder=zorder))


# ---------------------------------------------------------------------------
# Shared plane limits across both panels (E4 + E5), computed over placed kits used in cuts.
# ---------------------------------------------------------------------------
def both_limits(recs):
    pts = []
    for r in recs:
        if r["e4xy"]:
            pts.append(r["e4xy"])
        if r["e5xy"]:
            pts.append(r["e5xy"])
    P = np.array(pts)
    xmin, ymin = P.min(0)
    xmax, ymax = P.max(0)
    padx = 0.07 * (xmax - xmin)
    pady = 0.07 * (ymax - ymin)
    span = max(xmax - xmin, ymax - ymin)
    return (xmin - padx, xmax + padx), (ymin - pady, ymax + pady), span


def _scatter_base(ax, recs, coord_key, faint_noise_kids=None):
    """Light grey background scatter of all placed kits (record solid-ish, annex/system hollow),
    so the hulls read on top. Points are neutral grey — color meaning lives in the hulls +
    legend, honoring the numbers-only / unnamed constraint."""
    rec_x, rec_y, sup_x, sup_y = [], [], [], []
    for r in recs:
        p = r[coord_key]
        if p is None:
            continue
        if r["corpus_class"] == "record":
            rec_x.append(p[0]); rec_y.append(p[1])
        else:
            sup_x.append(p[0]); sup_y.append(p[1])
    if sup_x:
        ax.scatter(sup_x, sup_y, s=9, facecolors="none", edgecolors="#c2c6cc",
                   linewidths=0.5, alpha=0.6, zorder=1)
    if rec_x:
        ax.scatter(rec_x, rec_y, s=13, c="#9aa0a6", alpha=0.65, linewidths=0, zorder=2)


def _watermarks(ax):
    ax.text(0.5, 0.54, WM_NOTSERVED, transform=ax.transAxes, fontsize=12.5,
            color="#d24545", alpha=0.15, ha="center", va="center", rotation=24,
            zorder=6, weight="bold")
    ax.text(0.5, 0.46, WM_UNNAMED, transform=ax.transAxes, fontsize=9.5,
            color="#3a5fcd", alpha=0.15, ha="center", va="center", rotation=24,
            zorder=6, weight="bold")


def _panel_frame(ax, xlim, ylim, title, note):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="#e6e6e6", lw=0.5, zorder=0)
    ax.axvline(0, color="#e6e6e6", lw=0.5, zorder=0)
    ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=7)
    if note:
        ax.text(0.01, 0.01, note, transform=ax.transAxes, fontsize=6.6, va="bottom",
                ha="left", color="#333333",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#bbbbbb", alpha=0.85))


def _cluster_legend_text(summaries):
    """Build the numbers-only legend block text lines for a cut."""
    lines = []
    for s in summaries:
        cls = " ".join("%s=%d" % (k, v) for k, v in sorted(s["class"].items()))
        court = " ".join("%s %.0f%%" % (c, pct) for c, _, pct in s["court_pct"])
        toks = ", ".join("%s(%d)" % (t, c) for t, c in s["top_tokens"]) or "(no record gb_* tokens)"
        lines.append("%s  n=%d [%s]  court: %s  |  top gb_*: %s"
                     % (s["letter"], s["n"], cls, court, toks))
    return lines


# ---------------------------------------------------------------------------
# CUT A render: cluster on E4, draw membership hulls on BOTH panels.
# ---------------------------------------------------------------------------
def render_cut_a(recs, rec_by_kit, summaries, xlim, ylim, span, method, b):
    letter_of = {}
    for s in summaries:
        for k in s["kids"]:
            letter_of[k] = s["letter"]

    fig, axes = plt.subplots(1, 2, figsize=(17, 8.6))
    for ci, (coord_key, side_title) in enumerate([
        ("e4xy", "LEFT — E4 SERVED plane (truth) · CUT-A families cut HERE"),
        ("e5xy", "RIGHT — E5 CANDIDATE (B2: rot %.2f°, refl %s, NO scale) · SAME memberships"
                 % (abs(b["ang2"]), bool(b["refl2"])))]):
        ax = axes[ci]
        _scatter_base(ax, recs, coord_key)
        for i, s in enumerate(summaries):
            col = CLUSTER_COLORS[i]
            style = EDGE_STYLES[i]
            pts = [r[coord_key] for r in recs
                   if r["kit_id"] in set(s["kids"]) and r[coord_key] is not None]
            if len(pts) >= 2:
                draw_cluster_hull(ax, pts, col, style, span, filled=True)
                cen = np.array(pts).mean(0)
                ax.text(cen[0], cen[1], s["letter"], fontsize=12, fontweight="bold",
                        color=col, ha="center", va="center", zorder=7,
                        bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=col, alpha=0.9))
        note = ("E4-cut clusters: %d · method=%s · drawn over %d kits (both-placed)"
                % (len(summaries), method["chosen"], sum(1 for r in recs if r["e4xy"] and r["e5xy"])))
        _panel_frame(ax, xlim, ylim, side_title, note)
        _watermarks(ax)

    # legend: cluster letters + court swatches
    handles = [Line2D([0], [0], color=CLUSTER_COLORS[i], lw=2.4, linestyle=EDGE_STYLES[i],
                      label="%s (n=%d)" % (s["letter"], s["n"]))
               for i, s in enumerate(summaries)]
    court_h = [Patch(facecolor=COURT_COLOR[c], edgecolor="none", label="court %s" % c)
               for c in COURT_ORDER] + \
              [Patch(facecolor=NULL_COURT_COLOR, edgecolor="none", label="court NULL")]
    axes[0].legend(handles=handles, loc="upper left", fontsize=6.6, framealpha=0.92,
                   title="CUT-A clusters (letters only)")
    axes[1].legend(handles=court_h, loc="upper left", fontsize=6.4, framealpha=0.92,
                   title="court composition key")

    fig.suptitle("CUT A — E4-CARRYOVER families (cut on E4 SERVED plane; same memberships "
                 "shown on E5) · B3 congruence=%.4f (< 0.85 → E5 NOT served)" % b["cong2"],
                 fontsize=11.5)
    # legend text block under the plots (numbers only)
    txt = "CUT-A cluster legend (numbers only; families UNNAMED):\n" + \
          "\n".join(_cluster_legend_text(summaries))
    fig.text(0.012, 0.008, txt, fontsize=6.2, va="bottom", ha="left", family="monospace",
             color="#222222")
    fig.text(0.995, 0.004, WM_NOTSERVED + " · " + WM_UNNAMED + " · 2026-07-22",
             ha="right", va="bottom", fontsize=6.6, color="#8a1a1a", style="italic")
    fig.tight_layout(rect=(0, 0.11, 1, 0.955))
    p = os.path.join(OUT, "lassos-e4-carryover.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    return p


# ---------------------------------------------------------------------------
# CUT B render: cluster fresh on E5 (record-only); hulls on E5 solid, dashed echo on E4.
# ---------------------------------------------------------------------------
def render_cut_b(recs, rec_by_kit, summaries, noise_kids, xlim, ylim, span, method, b):
    fig, axes = plt.subplots(1, 2, figsize=(17, 8.6))
    # LEFT panel = E4 (dashed echo of E5-native memberships); RIGHT = E5 (native cut, solid)
    for ci, (coord_key, side_title, solid) in enumerate([
        ("e4xy", "LEFT — E4 SERVED plane (truth) · E5-native memberships echoed (dashed)", False),
        ("e5xy", "RIGHT — E5 CANDIDATE plane · CUT-B families cut HERE (record-class only)", True)]):
        ax = axes[ci]
        _scatter_base(ax, recs, coord_key)
        # noise (record-class, E5-native) drawn as small hollow crosses — honestly UNLASSOED
        if noise_kids:
            nx = [r[coord_key][0] for r in recs
                  if r["kit_id"] in noise_kids and r[coord_key] is not None]
            ny = [r[coord_key][1] for r in recs
                  if r["kit_id"] in noise_kids and r[coord_key] is not None]
            if nx:
                ax.scatter(nx, ny, s=20, c="#444444", marker="x", linewidths=0.8,
                           alpha=0.7, zorder=4,
                           label="unlassoed (n=%d)" % len(noise_kids) if ci == 1 else None)
        for i, s in enumerate(summaries):
            col = CLUSTER_COLORS[i]
            style = EDGE_STYLES[i]
            pts = [r[coord_key] for r in recs
                   if r["kit_id"] in set(s["kids"]) and r[coord_key] is not None]
            if len(pts) >= 2:
                if solid:
                    draw_cluster_hull(ax, pts, col, style, span, filled=True, lw=1.7,
                                      alpha_fill=0.12, alpha_edge=0.92)
                    cen = np.array(pts).mean(0)
                    ax.text(cen[0], cen[1], s["letter"], fontsize=12, fontweight="bold",
                            color=col, ha="center", va="center", zorder=7,
                            bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=col, alpha=0.9))
                else:
                    # dashed, hollow echo on E4
                    draw_cluster_hull(ax, pts, col, "--", span, filled=False, lw=1.1,
                                      alpha_edge=0.75)
        note = ("E5-native clusters: %d · method=%s · record-class only (n=%d) · unlassoed=%d"
                % (len(summaries), method["chosen"],
                   sum(1 for r in recs if r["corpus_class"] == "record"
                       and not r["supplementary"] and r["e5xy"]),
                   len(noise_kids)))
        _panel_frame(ax, xlim, ylim, side_title, note)
        _watermarks(ax)

    handles = [Line2D([0], [0], color=CLUSTER_COLORS[i], lw=2.4, linestyle=EDGE_STYLES[i],
                      label="%s (n=%d)" % (s["letter"], s["n"]))
               for i, s in enumerate(summaries)]
    if noise_kids:
        handles.append(Line2D([0], [0], color="#444444", marker="x", lw=0, markersize=6,
                              label="unlassoed (n=%d)" % len(noise_kids)))
    axes[1].legend(handles=handles, loc="upper left", fontsize=6.6, framealpha=0.92,
                   title="CUT-B clusters (letters only)")
    court_h = [Patch(facecolor=COURT_COLOR[c], edgecolor="none", label="court %s" % c)
               for c in COURT_ORDER] + \
              [Patch(facecolor=NULL_COURT_COLOR, edgecolor="none", label="court NULL")]
    axes[0].legend(handles=court_h, loc="upper left", fontsize=6.4, framealpha=0.92,
                   title="court composition key")

    fig.suptitle("CUT B — E5-NATIVE families (cut FRESH on E5 CANDIDATE plane; RECORD-class "
                 "only — annex/system draped placements excluded by design) · "
                 "B3 congruence=%.4f" % b["cong2"], fontsize=11.5)
    txt = "CUT-B cluster legend (numbers only; families UNNAMED):\n" + \
          "\n".join(_cluster_legend_text(summaries))
    fig.text(0.012, 0.008, txt, fontsize=6.2, va="bottom", ha="left", family="monospace",
             color="#222222")
    fig.text(0.995, 0.004, WM_NOTSERVED + " · " + WM_UNNAMED + " · 2026-07-22",
             ha="right", va="bottom", fontsize=6.6, color="#8a1a1a", style="italic")
    fig.tight_layout(rect=(0, 0.11, 1, 0.955))
    p = os.path.join(OUT, "lassos-e5-native.png")
    fig.savefig(p, dpi=150); plt.close(fig)
    return p


# ---------------------------------------------------------------------------
# Migration/split analysis: for each CUT-A cluster, measure how it reorients under E5.
# Numbers only + register-token descriptors. "split" = members fan across multiple regions;
# "migrate" = centroid moves far relative to the plane span. Neutral letters only.
# ---------------------------------------------------------------------------
def analyze_carryover(recs, summaries_a, span):
    """Returns list of dicts per CUT-A cluster: centroid shift E4->E5, spread ratio E5/E4,
    and a numbers+tokens descriptor of split/migrate behavior."""
    xy = {r["kit_id"]: r for r in recs}
    out = []
    for s in summaries_a:
        e4 = np.array([xy[k]["e4xy"] for k in s["kids"] if xy[k]["e4xy"] is not None])
        e5 = np.array([xy[k]["e5xy"] for k in s["kids"] if xy[k]["e5xy"] is not None])
        c4, c5 = e4.mean(0), e5.mean(0)
        shift = float(np.hypot(*(c5 - c4)))
        # RMS spread about centroid, each plane
        sp4 = float(np.sqrt(((e4 - c4) ** 2).sum(1).mean()))
        sp5 = float(np.sqrt(((e5 - c5) ** 2).sum(1).mean()))
        spread_ratio = (sp5 / sp4) if sp4 > 1e-9 else float("nan")
        out.append({
            "letter": s["letter"], "n": s["n"], "top_tokens": s["top_tokens"],
            "shift": shift, "shift_frac": shift / span,
            "spread_e4": sp4, "spread_e5": sp5, "spread_ratio": spread_ratio,
            "centroid_e4": (float(c4[0]), float(c4[1])),
            "centroid_e5": (float(c5[0]), float(c5[1])),
        })
    return out


# ---------------------------------------------------------------------------
# CSV: per-kit lasso membership.
# ---------------------------------------------------------------------------
def write_membership_csv(recs, cutA_letter, cutB_letter, cutB_noise):
    p = os.path.join(OUT, "lasso-membership.csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kit_id", "corpus_class", "court", "supplementary",
                    "cutA_cluster", "cutB_cluster", "e4_x", "e4_y",
                    "e5_x_aligned", "e5_y_aligned"])
        for r in sorted(recs, key=lambda x: (x["corpus_class"], x["kit_id"])):
            a = cutA_letter.get(r["kit_id"], "")   # blank = not in a both-placed CUT-A cluster
            if r["kit_id"] in cutB_letter:
                bcl = cutB_letter[r["kit_id"]]
            elif r["kit_id"] in cutB_noise:
                bcl = "noise"
            else:
                bcl = ""   # not eligible for CUT B (annex/system, or not E5-placed)
            e4x = "%.6f" % r["e4xy"][0] if r["e4xy"] else ""
            e4y = "%.6f" % r["e4xy"][1] if r["e4xy"] else ""
            e5x = "%.6f" % r["e5xy"][0] if r["e5xy"] else ""
            e5y = "%.6f" % r["e5xy"][1] if r["e5xy"] else ""
            w.writerow([r["kit_id"], r["corpus_class"], r["court"] or "",
                        1 if r["supplementary"] else 0, a, bcl, e4x, e4y, e5x, e5y])
    return p


# ---------------------------------------------------------------------------
# README (numbers only).
# ---------------------------------------------------------------------------
def _cluster_table(f, summaries, cut_label):
    f.write("| cluster | n | class split | court composition % | top-3 gb_* register tokens (record) |\n")
    f.write("|---|---|---|---|---|\n")
    for s in summaries:
        cls = " ".join("%s=%d" % (k, v) for k, v in sorted(s["class"].items()))
        court = " ".join("%s %.0f%%" % (c, pct) for c, _, pct in s["court_pct"])
        toks = ", ".join("`%s`(%d)" % (t, c) for t, c in s["top_tokens"]) or "—"
        f.write("| **%s** | %d | %s | %s | %s |\n" % (s["letter"], s["n"], cls, court, toks))
    f.write("\n")


def write_readme(recs, b, repro_ok, repro_lines, method_a, method_b,
                 summaries_a, summaries_b, cutB_noise, carryover, files):
    p = os.path.join(OUT, "README.md")
    with open(p, "w") as f:
        f.write("# E5 CANDIDATE — BUILD-FAMILY LASSOS — numbers only\n\n")
        f.write("**Date:** 2026-07-22 · **Executor:** elrond · **Purpose:** camera-fork ruling "
                "input — Matt SEES build-families as enclosing hulls on both cameras.\n\n")
        f.write("> **%s**\n>\n> **%s**\n\n" % (WM_NOTSERVED, WM_UNNAMED))
        f.write("Clusters carry NEUTRAL LETTER labels (A, B, C…). Legends are numbers-only + "
                "RATIFIED mechanical vocabulary (court k=5; `gb_*` register tokens from the "
                "six-block side-car). NO thematic / archetype / island names. Canonical "
                "island-cut + naming remain GATED (Matt hold).\n\n")

        f.write("## Reproduction gate (vs 2026-07-22-legb-gate-report.md) — runs FIRST\n\n")
        f.write("**Result: %s**\n\n" % ("PASS — 8/8 match record" if repro_ok else "FAIL — HALT"))
        f.write("\n".join(repro_lines) + "\n\n")

        f.write("## Method — clustering (HDBSCAN-first, silhouette-k-means fallback)\n\n")
        f.write("HDBSCAN (`sklearn.cluster.HDBSCAN`) is attempted first per cut (noise stays "
                "UNLASSOED — honest). If it under-resolves for legibility — a single hull over "
                "> 55%% of points (giant blob) OR fewer than 5 clusters — we fall back to "
                "k-means with silhouette-selected k in [5, 10] for that cut (task-sanctioned "
                "fallback). Both the chosen method and the rejected HDBSCAN result are recorded. "
                "All deterministic (SEED=%d).\n\n" % SEED)
        for tag, m in (("CUT A (E4-carryover)", method_a), ("CUT B (E5-native)", method_b)):
            f.write("**%s**\n\n" % tag)
            hd = m["hdbscan"]
            f.write("- HDBSCAN(min_cluster_size=%d, min_samples=%d) → k=%d, noise=%d, "
                    "largest hull=%.0f%% of points, sizes=%s.\n"
                    % (hd["min_cluster_size"], hd["min_samples"], hd["k"], hd["noise"],
                       100.0 * hd["biggest_frac"], hd["sizes"]))
            if m["chosen"] == "kmeans":
                km = m["kmeans"]
                sweep = " ".join("k%d:%.3f" % (k, s) for k, s in km["sweep"])
                f.write("- **Chosen: k-means k=%d** (silhouette=%.4f). Silhouette sweep: %s. "
                        "sizes=%s.\n" % (km["k"], km["silhouette"], sweep, km["sizes"]))
            else:
                f.write("- **Chosen: HDBSCAN** (k in legible range, no giant blob).\n")
            f.write("- Rationale: %s\n\n" % m["reason"])

        f.write("## CUT A — E4-carryover families (cut on the E4 SERVED plane)\n\n")
        f.write("Clustered on the E4 served plane using ALL **%d** kits placed in BOTH cameras "
                "(record + annex/system supplementary). Each cluster's hull is drawn on the E4 "
                "panel and the SAME MEMBERSHIP's hull on the E5-aligned panel → shows how E4's "
                "families reorient under the candidate angle.\n\n"
                % sum(1 for r in recs if r["e4xy"] and r["e5xy"]))
        _cluster_table(f, summaries_a, "A")

        f.write("### How CUT-A families reorient under E5 (numbers + register tokens only)\n\n")
        f.write("`shift` = centroid displacement E4→E5-aligned (plane units; frac of plane span). "
                "`spread_ratio` = RMS radius on E5 ÷ RMS radius on E4 (>1 = the family SPREADS / "
                "splinters; <1 = TIGHTENS). Families named by letter + top register tokens ONLY.\n\n")
        f.write("| cluster | n | shift | shift/span | spread E4 | spread E5 | spread_ratio | "
                "top gb_* tokens (record) |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for c in sorted(carryover, key=lambda x: -x["shift"]):
            toks = ", ".join("`%s`" % t for t, _ in c["top_tokens"]) or "—"
            f.write("| **%s** | %d | %.3f | %.2f | %.3f | %.3f | %.2f | %s |\n"
                    % (c["letter"], c["n"], c["shift"], c["shift_frac"], c["spread_e4"],
                       c["spread_e5"], c["spread_ratio"], toks))
        f.write("\n")
        # narrative: which split / migrate — letters + tokens ONLY
        migr = [c for c in carryover if c["shift_frac"] >= 0.20]
        splt = [c for c in carryover if c["spread_ratio"] >= 1.30]
        tght = [c for c in carryover if c["spread_ratio"] <= 0.77]
        def _desc(c):
            toks = "/".join(t.split(":", 1)[1] for t, _ in c["top_tokens"][:2]) or "no-token"
            return "Cluster %s (%s-heavy)" % (c["letter"], toks)
        f.write("- **Migrate (centroid shift ≥ 20%% of plane span):** %s\n"
                % ("; ".join("%s → shift %.2f span" % (_desc(c), c["shift_frac"]) for c in
                             sorted(migr, key=lambda x: -x["shift_frac"])) or "none"))
        f.write("- **Split / spread (E5 RMS radius ≥ 1.30× E4):** %s\n"
                % ("; ".join("%s → spread ×%.2f" % (_desc(c), c["spread_ratio"]) for c in
                             sorted(splt, key=lambda x: -x["spread_ratio"])) or "none"))
        f.write("- **Tighten (E5 RMS radius ≤ 0.77× E4):** %s\n\n"
                % ("; ".join("%s → spread ×%.2f" % (_desc(c), c["spread_ratio"]) for c in
                             sorted(tght, key=lambda x: x["spread_ratio"])) or "none"))

        f.write("## CUT B — E5-native families (cut FRESH on the E5 CANDIDATE plane)\n\n")
        f.write("Clustered on the E5-candidate-aligned plane using **RECORD-CLASS ONLY (%d "
                "axis-deriving fit members)**. Rationale HONORED: annex/system E5 placements "
                "derive from SHARED older vocabulary only (no six-block `gb_*` data) — cutting "
                "families from those draped placements would MANUFACTURE structure, so they are "
                "excluded from this cut. Hulls drawn on the E5 panel; the same memberships are "
                "echoed (dashed, hollow) on the E4 panel. Unlassoed (noise) record kits: **%d** "
                "(drawn as small × marks — honestly outside every hull).\n\n"
                % (sum(1 for r in recs if r["corpus_class"] == "record"
                       and not r["supplementary"] and r["e5xy"]), len(cutB_noise)))
        _cluster_table(f, summaries_b, "B")

        f.write("## Files\n\n")
        for name, size in files:
            f.write("- `%s` — %d bytes\n" % (name, size))
        f.write("\n## Exact reproduction command\n\n")
        f.write("```\ncd %s\npython3 atlas_e5_lassos_2026_07_22.py\n```\n\n" % SCRIPT_DIR)
        f.write("Deterministic: SEED=%d, all randomness pinned (HDBSCAN + KMeans). corpus.db "
                "opened read-only (uri mode=ro). Imports `atlas_e5_exhibit_2026_07_22`, "
                "`atlas_e5_exhibit_574_2026_07_22`, `atlas_legb_refit_2026_07_22` verbatim "
                "(no recompute/placement math changed). corpus.db md5 = "
                "`bebc933b0bf9bcab5988bbc16bcc55b4` (unchanged; read-only).\n\n" % SEED)

        f.write("## Constraint attestation\n\n")
        f.write("- READ-ONLY on corpus.db and every store — zero mutations, zero serving artifacts.\n")
        f.write("- Reproduction gate (8/8) gates the renders: any mismatch → HALT, no renders.\n")
        f.write("- EXHIBIT-ONLY lassos: NEUTRAL letter labels, numbers-only legends, RATIFIED "
                "vocabulary only (court k=5; `gb_*` register tokens). NO thematic / archetype / "
                "island names. Canonical island-cut + family naming remain GATED (Matt hold).\n")
        f.write("- CUT B excludes annex/system (no six-block data) — draped placements are NOT "
                "cut into families, avoiding manufactured structure.\n")
    return p


# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    print("=== E5 LASSOS — recompute + reproduction gate (delegated to V1) ===")
    b = V1.recompute()
    repro_ok, repro_lines = V1.repro_check(b)
    for ln in repro_lines:
        print(ln)
    if not repro_ok:
        with open(os.path.join(OUT, "REPRODUCTION-MISMATCH.md"), "w") as f:
            f.write("# E5 LASSOS — REPRODUCTION MISMATCH — HALT\n\n")
            f.write("The E5 recompute did NOT reproduce the gate report of record 8/8. "
                    "NO renders emitted. Determinism is the whole warrant for this exhibit.\n\n")
            f.write("\n".join(repro_lines) + "\n")
        print("!!! HALT — reproduction mismatch. Wrote REPRODUCTION-MISMATCH.md, no renders. !!!")
        sys.exit(3)
    print("--- reproduction PASS (8/8) — building lassos ---")

    # Reuse the 574 placement machinery verbatim.
    con = ro_connect(DB)
    corpus = F.load_corpus_574(con)
    gb_tokens = load_gb_tokens(con)
    con.close()
    project_e5_row = F.build_e5_supp_projector(b)
    e4_placements = F.build_e4_placements(corpus, b)
    recs, both = F.assemble_table(corpus, b, project_e5_row, e4_placements)
    rec_by_kit = {r["kit_id"]: r for r in recs}

    xlim, ylim, span = both_limits(recs)

    # ---- CUT A: cluster on E4 plane, all kits placed in BOTH cameras (561) ----
    a_recs = [r for r in recs if r["e4xy"] and r["e5xy"]]
    Xa = np.array([r["e4xy"] for r in a_recs])
    labels_a, method_a = cluster_plane(Xa, "CUT A (E4-carryover)")
    members_a = {}
    for r, lab in zip(a_recs, labels_a):
        if lab < 0:
            continue
        members_a.setdefault(int(lab), []).append(r["kit_id"])
    summaries_a = summarize_clusters(members_a, rec_by_kit, gb_tokens)
    cutA_letter = {}
    for s in summaries_a:
        for k in s["kids"]:
            cutA_letter[k] = s["letter"]
    carryover = analyze_carryover(recs, summaries_a, span)

    # ---- CUT B: cluster fresh on E5 plane, RECORD-class fit-basis only (265) ----
    b_recs = [r for r in recs if r["corpus_class"] == "record"
              and not r["supplementary"] and r["e5xy"]]
    Xb = np.array([r["e5xy"] for r in b_recs])
    labels_b, method_b = cluster_plane(Xb, "CUT B (E5-native)")
    members_b = {}
    cutB_noise = set()
    for r, lab in zip(b_recs, labels_b):
        if lab < 0:
            cutB_noise.add(r["kit_id"])
        else:
            members_b.setdefault(int(lab), []).append(r["kit_id"])
    summaries_b = summarize_clusters(members_b, rec_by_kit, gb_tokens)
    cutB_letter = {}
    for s in summaries_b:
        for k in s["kids"]:
            cutB_letter[k] = s["letter"]

    # ---- renders ----
    p_a = render_cut_a(recs, rec_by_kit, summaries_a, xlim, ylim, span, method_a, b)
    p_b = render_cut_b(recs, rec_by_kit, summaries_b, cutB_noise, xlim, ylim, span, method_b, b)
    p_csv = write_membership_csv(recs, cutA_letter, cutB_letter, cutB_noise)

    files = []
    for pth in [p_a, p_b, p_csv]:
        files.append((os.path.basename(pth), os.path.getsize(pth)))
    p_readme = write_readme(recs, b, repro_ok, repro_lines, method_a, method_b,
                            summaries_a, summaries_b, cutB_noise, carryover, files)
    files.append((os.path.basename(p_readme), os.path.getsize(p_readme)))

    print("\n=== CUT A (E4-carryover) — method=%s ===" % method_a["chosen"])
    for s in summaries_a:
        print("  %s n=%3d class=%s court=%s top=%s"
              % (s["letter"], s["n"], s["class"],
                 " ".join("%s%.0f%%" % (c, p) for c, _, p in s["court_pct"]),
                 [t for t, _ in s["top_tokens"]]))
    print("  carryover shifts (frac span):")
    for c in sorted(carryover, key=lambda x: -x["shift_frac"]):
        print("    %s shift=%.2f span  spread_ratio=%.2f  top=%s"
              % (c["letter"], c["shift_frac"], c["spread_ratio"], [t for t, _ in c["top_tokens"]]))

    print("\n=== CUT B (E5-native) — method=%s ===" % method_b["chosen"])
    for s in summaries_b:
        print("  %s n=%3d class=%s court=%s top=%s"
              % (s["letter"], s["n"], s["class"],
                 " ".join("%s%.0f%%" % (c, p) for c, _, p in s["court_pct"]),
                 [t for t, _ in s["top_tokens"]]))
    print("  unlassoed (noise): %d" % len(cutB_noise))

    print("\n=== FILES ===")
    for name, size in files:
        print("  %-28s %8d bytes" % (name, size))
    print("\n=== lassos dir: %s ===" % OUT)


if __name__ == "__main__":
    main()
