#!/usr/bin/env python3
"""
galadriel :: atlas-archipelago-mock static exhibit render
=========================================================
ONE static PNG for Matt decision-exhibit. Throwaway-class.
NOT production art, nothing served, nothing vendored, no glance touch.

Input : agentic_orchestration/research/curated/atlas/atlas-archipelago-mock.json
        (elrond MOCK derivation, NOT ratified; gandalf-verified structure)
Output: agentic_orchestration/galadriel/captures/2026-07-16-archipelago-mock/

Renders the "archipelago" surface:
  - 6 named islands: family CORES colored per-family + island-name labels
  - 27 U-n ISLETS: muted grays, clustered by U-n (label largest few only)
  - 126 DRIFTERS: small at-sea scatter marks
  - water background
Burns TWO stamps: "MOCK - NOT RATIFIED" (prominent),
  "seating designed-for-legibility, not measured" (smaller).
Legend carries census: cores 130 / islets 213 / straits 0 / drifters 126.

Seating is MDS-DESIGNED-FOR-LEGIBILITY, not a measured coordinate --
that caveat is burned into the image per brief.
"""
import json
import os
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

# ---- paths -----------------------------------------------------------------
ROOT = "/Users/admin/Games/reincarnated-collaboration"
SRC = os.path.join(
    ROOT, "agentic_orchestration/research/curated/atlas/atlas-archipelago-mock.json"
)
OUT_DIR = os.path.join(
    ROOT, "agentic_orchestration/galadriel/captures/2026-07-16-archipelago-mock"
)
OUT_PNG = os.path.join(OUT_DIR, "atlas-archipelago-mock.png")
os.makedirs(OUT_DIR, exist_ok=True)

# ---- load ------------------------------------------------------------------
with open(SRC) as fh:
    d = json.load(fh)
pts = d["points"]
islands = d["seating"]["islands"]
census = d["census_headline"]

# ---- palette (per-family, distinct + saturated for legibility) -------------
# ordered by core-count so legend reads big->small
FAMILY_ORDER = [
    "TOTEM-SENTRY",  # 46
    "TRAP-MINE",     # 43
    "WHIRLWIND",     # 15
    "AURA",          # 10
    "CHANNELED-BEAM",  # 9
    "MINION-PET",    # 7
]
FAMILY_COLOR = {
    "TOTEM-SENTRY": "#e6194b",     # red
    "TRAP-MINE": "#f58231",        # orange
    "WHIRLWIND": "#3cb44b",        # green
    "AURA": "#ffe119",             # yellow
    "CHANNELED-BEAM": "#911eb4",   # purple
    "MINION-PET": "#42d4f4",       # cyan
}
ISLET_GRAY = "#9aa4ad"
ISLET_EDGE = "#6b747c"
DRIFTER_GRAY = "#5f6b73"
WATER = "#0f2a3f"        # deep water fill
WATER_HAZE = "#14344c"   # slightly lighter panel to imply light on water
LAND_HALO = "#1b3d57"    # faint island halo

# ---- split points by stratum ----------------------------------------------
cores = {f: {"x": [], "y": []} for f in FAMILY_ORDER}
islet_pts = {"x": [], "y": []}
drifter_pts = {"x": [], "y": []}
core_counts = Counter()
islet_counts = Counter()
for p in pts:
    x, y = p["seat"]["x"], p["seat"]["y"]
    st = p["stratum"]
    if st == "core":
        fam = p["family"]
        cores.setdefault(fam, {"x": [], "y": []})
        cores[fam]["x"].append(x)
        cores[fam]["y"].append(y)
        core_counts[fam] += 1
    elif st == "islet":
        islet_pts["x"].append(x)
        islet_pts["y"].append(y)
        islet_counts[p.get("islet")] += 1
    elif st == "drifter":
        drifter_pts["x"].append(x)
        drifter_pts["y"].append(y)

# label only the largest few U-n islets
LABEL_ISLETS = [u for u, _ in islet_counts.most_common(6)]

# ---- figure ----------------------------------------------------------------
FIG_W, FIG_H, DPI = 15.0, 10.5, 130
fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor(WATER)
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set_facecolor(WATER)

# data extent -> generous water margin so nothing kisses the frame
xs = [p["seat"]["x"] for p in pts]
ys = [p["seat"]["y"] for p in pts]
pad = 22
ax.set_xlim(min(xs) - pad, max(xs) + pad)
ax.set_ylim(min(ys) - pad, max(ys) + pad)
ax.set_aspect("equal")
ax.axis("off")

# faint water gradient band (subtle "light on the sea", drawn as wide bands)
xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()
nbands = 40
for i in range(nbands):
    frac = i / (nbands - 1)
    yy0 = ymin + (ymax - ymin) * frac
    yy1 = ymin + (ymax - ymin) * (frac + 1.0 / nbands)
    # very subtle lighten toward centre
    t = 1.0 - abs(frac - 0.5) * 2.0
    shade = tuple(
        c0 + (c1 - c0) * (0.35 * t)
        for c0, c1 in zip(
            (0.059, 0.165, 0.247), (0.078, 0.204, 0.298)
        )
    )
    ax.axhspan(yy0, yy1, color=shade, lw=0, zorder=0)

# ---- per-family convex-hull "coastline" tint -------------------------------
# The two largest families (TRAP-MINE n=43, TOTEM-SENTRY n=46) sit DIFFUSE in
# the MDS layout (mean core-radius 41 / 19 from their seat; max ~70 / ~47),
# so their colored cores sprawl + interleave across the map centre. A faint
# family-tinted hull lets the eye group them WITHOUT moving any point -- the
# seating stays exactly as the mock computed it (disclosure preserved).
def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


try:
    from scipy.spatial import ConvexHull  # noqa: E402

    _HAVE_HULL = True
except Exception:
    _HAVE_HULL = False

for fam in FAMILY_ORDER:
    xy = cores.get(fam, {"x": [], "y": []})
    cx, cy = xy["x"], xy["y"]
    if len(cx) < 3:
        continue
    rgb = _hex_to_rgb(FAMILY_COLOR[fam])
    if _HAVE_HULL:
        import numpy as np  # noqa: E402

        P = np.column_stack([cx, cy])
        try:
            hull = ConvexHull(P)
            hx = P[hull.vertices, 0]
            hy = P[hull.vertices, 1]
            ax.fill(hx, hy, color=rgb, alpha=0.09, zorder=1, lw=0)
            ax.fill(hx, hy, facecolor="none", edgecolor=rgb, alpha=0.30,
                    lw=1.2, zorder=1)
        except Exception:
            pass

# ---- island land halos (soft "landmass" under each named island) -----------
for fam, info in islands.items():
    if info.get("type") != "named-island":
        continue
    ix, iy, n = info["x"], info["y"], info["n_cores"]
    # radius scales with sqrt(core count); big enough to read as land
    r = 6.5 + (n ** 0.5) * 3.6
    for k, (rr, aa) in enumerate([(r * 1.5, 0.10), (r * 1.18, 0.16), (r, 0.24)]):
        ax.scatter(
            [ix], [iy], s=(rr ** 2) * 3.14, c=LAND_HALO, alpha=aa,
            edgecolors="none", zorder=1,
        )

# faint islet halos so U-n clusters read as tiny land, not open water
for u, info in islands.items():
    if info.get("type") != "islet":
        continue
    ix, iy, n = info["x"], info["y"], info["n"]
    r = 3.0 + (n ** 0.5) * 1.6
    ax.scatter(
        [ix], [iy], s=(r ** 2) * 3.14, c=LAND_HALO, alpha=0.14,
        edgecolors="none", zorder=1,
    )

# ---- drifters (draw first, lowest, small + quiet at-sea marks) -------------
ax.scatter(
    drifter_pts["x"], drifter_pts["y"], s=14, c=DRIFTER_GRAY, marker="x",
    linewidths=0.8, alpha=0.6, zorder=2, label="_drifter",
)

# ---- islets (muted gray, clustered by U-n) ---------------------------------
ax.scatter(
    islet_pts["x"], islet_pts["y"], s=26, c=ISLET_GRAY, marker="o",
    edgecolors=ISLET_EDGE, linewidths=0.5, alpha=0.9, zorder=3,
)

# ---- cores (per-family color) ----------------------------------------------
for fam in FAMILY_ORDER:
    xy = cores.get(fam, {"x": [], "y": []})
    ax.scatter(
        xy["x"], xy["y"], s=52, c=FAMILY_COLOR[fam], marker="o",
        edgecolors="#0b1e2d", linewidths=0.6, alpha=0.95, zorder=5,
    )

# ---- island name labels ----------------------------------------------------
def _label(ix, iy, text, fs, weight, color, halo, dy=0.0):
    t = ax.text(
        ix, iy + dy, text, fontsize=fs, fontweight=weight, color=color,
        ha="center", va="center", zorder=8, fontfamily="DejaVu Sans",
    )
    t.set_path_effects(
        [
            matplotlib.patheffects.withStroke(linewidth=halo, foreground="#071521"),
        ]
    )
    return t


import matplotlib.patheffects  # noqa: E402

for fam, info in islands.items():
    if info.get("type") != "named-island":
        continue
    ix, iy, n = info["x"], info["y"], info["n_cores"]
    r = 6.5 + (n ** 0.5) * 3.6
    _label(
        ix, iy, f"{fam}", fs=15, weight="bold",
        color=FAMILY_COLOR[fam], halo=3.2, dy=r + 5.5,
    )
    _label(
        ix, iy, f"{n} cores", fs=10, weight="normal",
        color="#dbe4ea", halo=2.4, dy=r + 1.5,
    )

# label largest U-n islets (muted)
for u in LABEL_ISLETS:
    info = islands.get(u)
    if not info:
        continue
    ix, iy, n = info["x"], info["y"], info["n"]
    _label(ix, iy, f"{u}", fs=9, weight="bold", color="#c3ccd3", halo=2.2,
           dy=(3.0 + (n ** 0.5) * 1.6) + 3.0)

# ---- title block (top-left) ------------------------------------------------
fig.text(
    0.018, 0.965, "ATLAS TERRITORY - ARCHIPELAGO", fontsize=22,
    fontweight="bold", color="#f2f7fa", ha="left", va="top",
    fontfamily="DejaVu Sans",
)
fig.text(
    0.018, 0.925,
    "Edition-I 469 active kits  |  five strata  |  elrond MOCK derivation, 2026-07-16",
    fontsize=11, color="#aebcc6", ha="left", va="top", fontfamily="DejaVu Sans",
)

# ---- MOCK stamps (burned in, prominent) ------------------------------------
# big diagonal watermark across the field
fig.text(
    0.5, 0.55, "MOCK - NOT RATIFIED", fontsize=58, fontweight="bold",
    color="#ff3b3b", alpha=0.11, ha="center", va="center", rotation=24,
    fontfamily="DejaVu Sans", zorder=1,
)
# solid stamp badge top-right
badge = FancyBboxPatch(
    (0.735, 0.905), 0.247, 0.072, transform=fig.transFigure,
    boxstyle="round,pad=0.004,rounding_size=0.010",
    facecolor="#7a0f14", edgecolor="#ff5a5a", linewidth=2.0, zorder=20,
)
fig.patches.append(badge)
fig.text(
    0.858, 0.955, "MOCK - NOT RATIFIED", fontsize=15, fontweight="bold",
    color="#ffd9d9", ha="center", va="center", zorder=21,
    fontfamily="DejaVu Sans",
)
fig.text(
    0.858, 0.923,
    "seating designed-for-legibility, not measured",
    fontsize=8.5, color="#ffbcbc", ha="center", va="center", zorder=21,
    fontfamily="DejaVu Sans",
)

# ---- legend (bottom-left): census + family colors -------------------------
LX, LY = 0.018, 0.315
# panel
panel = FancyBboxPatch(
    (LX - 0.006, 0.020), 0.300, 0.300, transform=fig.transFigure,
    boxstyle="round,pad=0.004,rounding_size=0.010",
    facecolor="#0a1e2e", edgecolor="#2f5772", linewidth=1.4, alpha=0.94,
    zorder=15,
)
fig.patches.append(panel)

fig.text(
    LX, LY, "CENSUS", fontsize=12, fontweight="bold", color="#f2f7fa",
    ha="left", va="top", zorder=16, fontfamily="DejaVu Sans",
)
census_lines = [
    ("cores", census["ashore_cores"], "ashore, 6 named islands"),
    ("islets", census["islets"], "27 U-n clusters"),
    ("straits", census["straits"], "-"),
    ("drifters", census["at_sea_drifters"], "at sea"),
]
yy = LY - 0.030
for name, num, note in census_lines:
    fig.text(
        LX + 0.006, yy, f"{name}", fontsize=10.5, color="#cdd8df",
        ha="left", va="top", zorder=16, fontfamily="DejaVu Sans",
    )
    fig.text(
        LX + 0.088, yy, f"{num}", fontsize=10.5, fontweight="bold",
        color="#ffffff", ha="right", va="top", zorder=16,
        fontfamily="DejaVu Sans",
    )
    fig.text(
        LX + 0.100, yy, f"{note}", fontsize=8.5, color="#8fa1ac",
        ha="left", va="top", zorder=16, fontfamily="DejaVu Sans",
    )
    yy -= 0.026

# families sub-header + swatches
yy -= 0.008
fig.text(
    LX, yy, "FAMILY CORES", fontsize=10, fontweight="bold", color="#dbe4ea",
    ha="left", va="top", zorder=16, fontfamily="DejaVu Sans",
)
yy -= 0.024
for fam in FAMILY_ORDER:
    # swatch dot via a small figure-space marker
    fig.text(
        LX + 0.010, yy, "●", fontsize=12, color=FAMILY_COLOR[fam],
        ha="center", va="center", zorder=16, fontfamily="DejaVu Sans",
    )
    fig.text(
        LX + 0.026, yy, f"{fam}", fontsize=9.5, color="#e3ebf0",
        ha="left", va="center", zorder=16, fontfamily="DejaVu Sans",
    )
    fig.text(
        LX + 0.282, yy, f"{core_counts[fam]}", fontsize=9.5, fontweight="bold",
        color="#ffffff", ha="right", va="center", zorder=16,
        fontfamily="DejaVu Sans",
    )
    yy -= 0.0205

# islet + drifter marks in legend
yy -= 0.004
fig.text(
    LX + 0.010, yy, "●", fontsize=11, color=ISLET_GRAY,
    ha="center", va="center", zorder=16, fontfamily="DejaVu Sans",
)
fig.text(
    LX + 0.026, yy, "islet member (U-n, unnamed)", fontsize=9,
    color="#b9c4cb", ha="left", va="center", zorder=16,
    fontfamily="DejaVu Sans",
)
yy -= 0.020
fig.text(
    LX + 0.010, yy, "✕", fontsize=10, color=DRIFTER_GRAY,
    ha="center", va="center", zorder=16, fontfamily="DejaVu Sans",
)
fig.text(
    LX + 0.026, yy, "drifter (at sea, no family)", fontsize=9,
    color="#b9c4cb", ha="left", va="center", zorder=16,
    fontfamily="DejaVu Sans",
)

# ---- provenance footer (bottom-right) --------------------------------------
fig.text(
    0.982, 0.028,
    "elrond derivation  ·  gandalf-verified structure  ·  galadriel render "
    "·  clustering in full 14-dim MCA space  ·  MDS stress "
    f"{d['seating']['mds_stress']:.0f}  ·  nothing served / nothing vendored",
    fontsize=7.5, color="#7d8f9a", ha="right", va="bottom",
    fontfamily="DejaVu Sans",
)

# ---- save ------------------------------------------------------------------
fig.savefig(OUT_PNG, dpi=DPI, facecolor=WATER)
plt.close(fig)

# report actual pixel dims
from PIL import Image  # noqa: E402

with Image.open(OUT_PNG) as im:
    w, h = im.size
print(f"WROTE {OUT_PNG}")
print(f"DIMS {w}x{h}")
print(
    f"CORES {sum(core_counts.values())}  ISLETS {sum(islet_counts.values())}  "
    f"DRIFTERS {len(drifter_pts['x'])}  LABELLED_ISLETS {LABEL_ISLETS}"
)
