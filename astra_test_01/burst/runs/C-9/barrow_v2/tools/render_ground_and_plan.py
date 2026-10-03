#!/usr/bin/env python3
"""barrow_v2 (lane BX): rasterize the ground zones and draw the labelled top-down plan.

Light work (numpy + PIL + matplotlib, no Godot/Blender). Outputs:
  greybox/ground_class_map.png      4 px/m, palette PNG: one index per ground class (the paint + crater-v5 surface driver)
  greybox/ground_class_map.json     index -> class, the raster's sim-frame extent, its sha256
  godot/data/ground_colour.png      8 px/m soft colour zones + faint spawn discs/boxes + the floor edge (the greybox ground texture)
  greybox/plan_topdown.png          the labelled plan, north up
"""
import hashlib
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bv2_geom as G  # noqa: E402

ROOT = os.path.dirname(HERE)
L = json.load(open(os.path.join(ROOT, "layout_v2.json")))
EXT = {"x0": -62.0, "x1": 66.0, "y0": -74.0, "y1": 62.0}      # sim frame, the land/sea texture extent

CLASSES = ["outside_sea", "outside_shore_ice", "outside_land", "grave_ground", "shore_shingle", "cliff_top_rock",
           "hall_yard_ash", "snow_field", "mere_ice", "stream_ice", "circle", "path"]
OUT_RGB = {"outside_sea": (0.20, 0.27, 0.34), "outside_shore_ice": (0.62, 0.70, 0.77), "outside_land": (0.62, 0.61, 0.58)}


def grid(ppm):
    w = int(round((EXT["x1"] - EXT["x0"]) * ppm))
    h = int(round((EXT["y1"] - EXT["y0"]) * ppm))
    xs = EXT["x0"] + (np.arange(w) + 0.5) / ppm
    ys = EXT["y0"] + (np.arange(h) + 0.5) / ppm
    return np.meshgrid(xs, ys)


def poly_mask(poly, X, Y):
    """Vectorized even-odd point-in-polygon."""
    inside = np.zeros(X.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if y0 == y1:
            continue
        cond = (y0 > Y) != (y1 > Y)
        xi = x0 + (Y - y0) * (x1 - x0) / (y1 - y0)
        inside ^= cond & (xi > X)
    return inside


def polyline_dist(pl, X, Y):
    d = np.full(X.shape, np.inf)
    for (ax, ay), (bx, by) in zip(pl[:-1], pl[1:]):
        dx, dy = bx - ax, by - ay
        t = np.clip(((X - ax) * dx + (Y - ay) * dy) / (dx * dx + dy * dy), 0, 1)
        d = np.minimum(d, np.hypot(X - (ax + t * dx), Y - (ay + t * dy)))
    return d


def classify(ppm):
    X, Y = grid(ppm)
    Z = L["zones"]["classes"]
    floor = poly_mask(L["floor"]["polygon"], X, Y)
    land = poly_mask(L["land"]["polygon"], X, Y)
    ice = poly_mask(L["shore_ice"]["polygon"], X, Y)
    cls = np.full(X.shape, CLASSES.index("outside_sea"), dtype=np.uint8)
    cls[ice] = CLASSES.index("outside_shore_ice")
    cls[land] = CLASSES.index("outside_land")
    # seeded biomes on the floor: nearest seed
    names = ["grave_ground", "shore_shingle", "cliff_top_rock", "hall_yard_ash", "snow_field"]
    best = np.full(X.shape, np.inf)
    lab = np.zeros(X.shape, dtype=np.uint8)
    for nm in names:
        for sx, sy in Z[nm]["seeds"]:
            d = np.hypot(X - sx, Y - sy) * (1.25 if nm == "snow_field" else 1.0)
            m = d < best
            best[m] = d[m]
            lab[m] = CLASSES.index(nm)
    cls[floor] = lab[floor]
    c = Z["circle"]["disc"]
    circ = np.hypot(X - c["centre"][0], Y - c["centre"][1]) <= c["r_m"]
    path = polyline_dist(L["path"]["polyline"], X, Y) <= L["path"]["width_m"] / 2
    stream = polyline_dist(L["stream"]["polyline"], X, Y) <= L["stream"]["width_m"] / 2
    mere = poly_mask(L["mere"]["polygon"], X, Y)
    cls[floor & path] = CLASSES.index("path")
    cls[floor & circ] = CLASSES.index("circle")
    cls[stream & (floor | land)] = CLASSES.index("stream_ice")
    cls[mere] = CLASSES.index("mere_ice")
    return cls, X, Y, floor


def rgb_of(name):
    if name in OUT_RGB:
        return OUT_RGB[name]
    return tuple(L["zones"]["classes"][name]["rgb"])


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    os.makedirs(os.path.join(ROOT, "greybox"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "godot", "data"), exist_ok=True)
    # ---- the class map (4 px/m) ----
    cls4, *_ = classify(4.0)
    im = Image.fromarray(cls4, mode="P")
    pal = []
    for nm in CLASSES:
        pal += [int(255 * v) for v in rgb_of(nm)]
    im.putpalette(pal + [0] * (768 - len(pal)))
    p_cls = os.path.join(ROOT, "greybox", "ground_class_map.png")
    im.save(p_cls, optimize=True)
    counts = {nm: round(float((cls4 == i).sum()) / 16.0, 1) for i, nm in enumerate(CLASSES)}
    meta = {"_what": "barrow_v2 ground class map: one palette index per ground class (paint + crater-v5 surface driver)",
            "png": "greybox/ground_class_map.png", "png_sha256": sha256(p_cls), "px_per_m": 4.0,
            "extent_sim_m": EXT, "row0": "y = y0 (north edge); col0 = x0 (west edge)",
            "classes": {i: nm for i, nm in enumerate(CLASSES)},
            "surface": {nm: L["zones"]["classes"][nm]["surface"] for nm in CLASSES if nm in L["zones"]["classes"]},
            "area_m2_by_class": counts}
    json.dump(meta, open(os.path.join(ROOT, "greybox", "ground_class_map.json"), "w"), indent=2, ensure_ascii=False)
    open(os.path.join(ROOT, "greybox", "ground_class_map.json"), "a").write("\n")

    # ---- the soft colour ground (8 px/m) ----
    ppm = 8.0
    cls8, X, Y, floor = classify(ppm)
    lut = np.array([rgb_of(nm) for nm in CLASSES], dtype=np.float32)
    rgb = lut[cls8]
    blur_px = L["zones"]["blend_m"] / 2.0 * ppm
    soft = np.asarray(Image.fromarray((rgb * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur_px)),
                      dtype=np.float32) / 255.0
    # soften only on the floor (the seams blend); the outside keeps its hard edges
    rgb = np.where(floor[..., None], soft, rgb)
    shade = np.ones(X.shape)
    sc = L.get("sculpt")
    if sc:
        # R-C9-149a: the ground outside the floor is coloured from the sculpted terrain (snow, rock on steep
        # faces, grass/heather on the mound, shingle beach, shore ice, ledges, water); the floor is mottled
        hf = sc["heightfield"]
        H = np.fromfile(os.path.join(ROOT, hf["file"]), dtype="<f4").reshape(hf["shape"])
        hp = hf["px_per_m"]
        fx = np.clip((X - EXT["x0"]) * hp, 0, H.shape[1] - 1.001)
        fy = np.clip((Y - EXT["y0"]) * hp, 0, H.shape[0] - 1.001)
        i0, j0 = fx.astype(int), fy.astype(int)
        tx, ty = fx - i0, fy - j0
        Hs = (H[j0, i0] * (1 - tx) + H[j0, i0 + 1] * tx) * (1 - ty) + (H[j0 + 1, i0] * (1 - tx) + H[j0 + 1, i0 + 1] * tx) * ty
        gyy, gxx = np.gradient(Hs, 1.0 / ppm)
        slope = np.hypot(gxx, gyy)
        rng = np.random.default_rng(7)
        nz = np.asarray(Image.fromarray((rng.random((X.shape[0] // 8 + 1, X.shape[1] // 8 + 1)) * 255).astype(np.uint8)).resize(
            (X.shape[1], X.shape[0]), Image.BICUBIC), dtype=np.float32) / 255.0 - 0.5
        nz2 = np.asarray(Image.fromarray((rng.random((X.shape[0] // 2 + 1, X.shape[1] // 2 + 1)) * 255).astype(np.uint8)).resize(
            (X.shape[1], X.shape[0]), Image.BILINEAR), dtype=np.float32) / 255.0 - 0.5
        out = np.zeros(X.shape + (3,), dtype=np.float32)
        out[:] = np.stack([0.91 + 0.05 * nz, 0.91 + 0.05 * nz, 0.89 + 0.05 * nz], -1)          # snow
        rock = np.stack([0.47 + 0.10 * nz2, 0.45 + 0.09 * nz2, 0.41 + 0.08 * nz2], -1)
        rw = np.clip((slope - 0.7) / 1.0, 0, 1)[..., None]
        out = out * (1 - rw) + rock * rw
        mo = next(f for f in L["features"] if f["kind"] == "mound")["footprint"]
        in_mound = poly_mask(mo, X, Y)
        mound_m = in_mound & (Hs > 0.3) & ((nz > -0.25) | (Hs < 4.5)) & (slope < 1.6)
        tus = (~in_mound) & (Hs > 0.4) & (nz2 > 0.28) & (slope < 1.2)
        out[tus] = (0.6 * out + 0.4 * np.stack([0.66, 0.60, 0.50]))[tus]
        grass = np.stack([0.60 + 0.08 * nz2, 0.53 + 0.07 * nz2, 0.38 + 0.06 * nz2], -1)
        out[mound_m] = (0.35 * out + 0.65 * grass)[mound_m]
        beach = (Hs < -0.05) & (Hs > -0.42) & (slope < 0.5)
        out[beach] = np.stack([0.60 + 0.08 * nz2, 0.61 + 0.08 * nz2, 0.62 + 0.08 * nz2], -1)[beach]
        icem = (Hs <= -0.40) & (Hs > -0.6)
        out[icem] = np.stack([0.76 + 0.06 * nz2, 0.84 + 0.04 * nz2, 0.91 + 0.03 * nz2], -1)[icem]
        ledge = (Hs < -1.0) & (Hs > -4.4)
        out[ledge] = rock[ledge] * 0.95
        sea = Hs <= -4.4
        out[sea] = np.array([0.19, 0.26, 0.33])
        land_out = ~floor
        rgb = np.where(land_out[..., None], out, rgb * (1 + 0.06 * nz[..., None]))
        lx, ly, lz = -0.45, -0.55, 0.70                        # light from the north-west, high
        nrm = np.stack([-gxx, -gyy, np.ones_like(gxx)], -1)
        nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
        shade = np.clip(0.55 + 0.6 * (nrm[..., 0] * lx + nrm[..., 1] * ly + nrm[..., 2] * lz), 0.35, 1.15)
    img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    dr = ImageDraw.Draw(img, "RGBA")

    def px(p):
        return ((p[0] - EXT["x0"]) * ppm, (p[1] - EXT["y0"]) * ppm)
    h = L["anchors"]["scatter"]["half_width_m"]
    for a in L["anchors"]["points"]:
        c = (a["x"], a["y"])
        r = L["anchors"]["scatter"]["disc_radius_m_brief"] * ppm
        cp = px(c)
        dr.ellipse([cp[0] - r, cp[1] - r, cp[0] + r, cp[1] + r], fill=(235, 180, 60, 34), outline=(205, 140, 30, 120), width=3)
        dr.ellipse([cp[0] - 5, cp[1] - 5, cp[0] + 5, cp[1] + 5], fill=(170, 100, 20, 200))
    fl = [px(p) for p in L["floor"]["polygon"]]
    dr.line(fl + [fl[0]], fill=(40, 40, 40, 200), width=3)
    p_col = os.path.join(ROOT, "godot", "data", "ground_colour.png")
    img.save(p_col, optimize=True)

    # ---- the plan ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MPoly, Rectangle, Circle
    fig, ax = plt.subplots(figsize=(14, 14.6), dpi=150)
    ax.imshow(np.clip(np.asarray(img, dtype=np.float32) / 255.0 * shade[..., None], 0, 1),
              extent=[EXT["x0"], EXT["x1"], EXT["y1"], EXT["y0"]], interpolation="bilinear")
    kind_col = {"mound": "#8c8a6a", "door": "#3a2a1a", "standing_stone": "#6d6d6d", "wreck": "#6b4a2b", "mast": "#4a3220",
                "rock": "#777", "hall": "#4b3b2e", "gable": "#5a4030", "palisade": "#5b4632", "cliff": "#8a8378", "cave": "#111",
                "fallen_stone": "#9a968c", "grave_marker": "#6a6058", "driftwood": "#8a7050", "beam": "#2e2622",
                "tree": "#c8c0b0", "juniper": "#334433", "floe": "#dde8f0", "porch": "#6a4a2a", "stone": "#6d6d6d",
                "drift_berm": "#ffffff", "ash_heap": "#333", "pressure_ridge": "#e8f4ff", "heather": "#7a4a5a",
                "rock_slab": "#888", "scree": "#777", "shingle_tongue": "#99a", "pebble": "#888", "trodden_snow": "#ccc", "stream_bank": "#eee"}
    for f in L["features"]:
        poly = f["footprint"]
        if f["kind"] == "mound":
            ax.add_patch(MPoly(poly, closed=True, fill=False, ec="#4a4a30", lw=0.8, ls=(0, (3, 2))))
            continue
        if not f["blocks_movement"]:          # walk-over detail: drawn faintly
            ax.add_patch(MPoly(poly, closed=True, fc=kind_col.get(f["kind"], "#bbb"), ec="none", lw=0, alpha=0.35))
            continue
        ax.add_patch(MPoly(poly, closed=True, fc=kind_col.get(f["kind"], "#999"), ec="black", lw=0.5, alpha=0.85))
    S = L["stair"]
    for part, colr in (("top_landing", "#c9b48a"), ("flight", "#d9c79a"), ("bottom_landing", "#b29f78")):
        ax.add_patch(MPoly(S[part]["polygon"], closed=True, fc=colr, ec="#5a4020", lw=1.0))
    fl3 = S["flight"]["polygon"]
    n = S["flight"]["n_steps"]
    for k in range(1, n, 5):
        t = k / n
        a = [fl3[0][0] + t * (fl3[3][0] - fl3[0][0]), fl3[0][1] + t * (fl3[3][1] - fl3[0][1])]
        b = [fl3[1][0] + t * (fl3[2][0] - fl3[1][0]), fl3[1][1] + t * (fl3[2][1] - fl3[1][1])]
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#5a4020", lw=0.4)
    ax.add_patch(MPoly(L["floor"]["polygon"], closed=True, fill=False, ec="black", lw=2.0))
    ax.add_patch(MPoly(L["floor"]["min_disc_hull"]["polygon"], closed=True, fill=False, ec="#666", lw=0.7, ls=(0, (1, 2))))
    ax.plot(*zip(*L["land"]["cliff_lip"]), color="#3a2c20", lw=1.0, ls="-")
    for a in L["anchors"]["points"]:
        ax.plot([0, a["x"]], [0, a["y"]], color="#a06010", lw=0.9, ls=(0, (4, 3)))
        ax.add_patch(Circle((a["x"], a["y"]), 8.0, fill=False, ec="#b07010", lw=1.2))
        ax.plot(a["x"], a["y"], "o", color="#8a4a00", ms=5)
        ax.annotate(f"{a['id']}  {a['compass_deg']:.0f}°  {a['dist_from_start_m']:.1f} m\n{a['delivered_by'].split(' (')[0]}",
                    (a["x"], a["y"]), xytext=(6, -14), textcoords="offset points", fontsize=8.5, color="#3a2000",
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.8))
    ax.plot(0, 0, marker="+", color="black", ms=14, mew=2)
    ax.annotate("start (0,0)", (0, 0), xytext=(6, 6), textcoords="offset points", fontsize=8.5)
    for v in L["views"]:
        w, hh = v["window_m"]
        tx, ty = v["target"]
        ax.add_patch(Rectangle((tx - w / 2, ty - hh / 2), w, hh, fill=False, ec="#2050a0", lw=0.9, ls=(0, (6, 3))))
        ax.annotate(v["id"], (tx - w / 2, ty - hh / 2), xytext=(2, 9), textcoords="offset points", fontsize=7, color="#2050a0")
    labels = {"barrow_mound": "the King's barrow (outside)", "wreck_hull": "the wreck (outside)", "longhall": "burnt longhall",
              "fallen_gable": "fallen gable (hall SW end)", "sea_cave_mouth": "sea cave"}
    for f in L["features"]:
        if f["id"] in labels:
            xs = [p[0] for p in f["footprint"]]
            ys = [p[1] for p in f["footprint"]]
            ax.annotate(labels[f["id"]], (sum(xs) / len(xs), sum(ys) / len(ys)), fontsize=8, ha="center", color="white",
                        bbox=dict(boxstyle="round,pad=0.2", fc="#000", ec="none", alpha=0.55))
    ax.annotate("stair: 3.0 m wide, 28 x (0.15 rise / 0.30 tread)\n26.6° ramp, 4.2 m climb from the ledge, open sea side",
                (S["flight"]["polygon"][2][0] - 14, S["flight"]["polygon"][2][1] + 9), fontsize=7.5,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85))
    ax.annotate("frozen mere", (-14, -16), fontsize=8.5, color="#183050", ha="center")
    ax.annotate("stream from the barrow", tuple(L["stream"]["polyline"][2]), fontsize=7.5, color="#183050")
    ax.annotate("stone circle", (2.5, -7.8), fontsize=8, ha="center")
    # scale bar + north arrow
    ax.plot([-55, -35], [55, 55], color="black", lw=3)
    ax.text(-45, 53.2, "20 m", ha="center", fontsize=9)
    ax.annotate("N", xy=(58, -66), xytext=(58, -58), ha="center", fontsize=12, arrowprops=dict(arrowstyle="-|>", lw=1.5))
    ax.set_xlim(EXT["x0"], EXT["x1"])
    ax.set_ylim(EXT["y1"], EXT["y0"])       # north (-y) up
    ax.set_aspect("equal")
    ax.set_xlabel("x (m, east)")
    ax.set_ylabel("y (m, SOUTH)  -- north is up")
    fa = L["floor"]
    ax.set_title(f"barrow_v2 'Fjord Headland' greybox plan -- walkable floor {fa['extents']['width_x']:.1f} x {fa['extents']['depth_y']:.1f} m, "
                 f"{fa['area_m2']:.0f} m2 (black, ORGANIC edge, R-C9-149a) around the disc-hull minimum {fa['min_disc_hull']['area_m2']:.0f} m2 (grey dotted)\n"
                 "gold: the 8 m scatter discs (the oracle's polar law), dashed lines: open lines to the start; blue dashed: the 25 x 18 m camera windows",
                 fontsize=9.5)
    fig.tight_layout()
    p_plan = os.path.join(ROOT, "greybox", "plan_topdown.png")
    fig.savefig(p_plan)
    print("wrote", p_cls, p_col, p_plan)
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
