#!/usr/bin/env python3
"""barrow_v2 paint lane (BVP, drax): THE ZONE MAP -- the paint guide under R-C9-151 (Matt): a FLAT, colour-coded
2D map at the game camera, rendered from layout_v2.json (v4) -- no shaded 3D shapes. The painter invents every
shape; the map only says WHERE (and how tall, by a thin outline).

    python3 tools/bvp_zonemap.py      -> paint/barrow_v2_zonemap.png (plate grid, paint/frame_bvp.json) + _preview.jpg
                                         + paint/zonemap_legend.json

Camera: oblique orthographic, pitch a = 52.9535411256029 deg, zero yaw, P = 100.617553710938 px/m (the plate):
plate_X = P*x + X0, plate_Y = P*sin(a)*y - P*cos(a)*z + Y0.

Ground: the heightfield (layout sculpt.heightfield, 0.5 m) is ray-cast per plate column -- the camera looks north
and down, so the visible ground point of a screen row is the SOUTHERNMOST y with sin(a)*y - cos(a)*h(x, y) <= row
(the suffix minimum of that function is monotone, so one searchsorted per column). Each visible point is coloured
FLAT by its zone (the floor's biome classes from greybox/ground_class_map.png; outside: the barrow mound, steep rock
faces, beach shingle, shore ice, sea, snow-covered land with a soft height tint).
Marks on top (thin, flat, no shading): the walkable floor's edge (a faint dotted line, NOT to be painted), the six
8 m spawn discs (faint dotted ellipses), and each deliverer / structure as a flat-coloured footprint at its base
plus a thin outline of how high it rises on screen.
"""
import hashlib, json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
BV2 = os.path.dirname(HERE)
PAINT = os.path.join(BV2, "paint")
L = json.load(open(os.path.join(BV2, "layout_v2.json")))
FR = json.load(open(os.path.join(PAINT, "frame_bvp.json")))
GCM = json.load(open(os.path.join(BV2, "greybox", "ground_class_map.json")))
P = FR["px_per_m"]; X0, Y0 = FR["origin_px"]; W, H = FR["size_px"]
A = math.radians(FR["pitch_deg"]); S, C = math.sin(A), math.cos(A)
Image.MAX_IMAGE_PIXELS = None
K = 2                       # ray-cast at half plate resolution, then upscaled
DY = 0.08                   # ground sampling step along y (m)
CARRY_M = 6.0

ZONES = {   # name -> flat RGB (the legend the brief repeats in words)
    "floor_snow":      (247, 246, 242),
    "grave_ground":    (232, 205, 200),
    "shore_shingle":   (214, 204, 190),
    "cliff_top_rock":  (222, 219, 212),
    "hall_yard_ash":   (196, 186, 178),
    "snow_field":      (247, 246, 242),
    "circle":          (238, 233, 222),
    "path":            (233, 226, 214),
    "mere_ice":        (168, 204, 232),
    "stream_ice":      (168, 204, 232),
    "land_snow":       (226, 232, 240),
    "barrow_mound":    (204, 196, 160),
    "rock_face":       (158, 150, 142),
    "beach_shingle":   (188, 180, 168),
    "shore_ice":       (200, 224, 240),
    "sea":             (58, 84, 110),
}
MARKS = {   # structure kind -> (fill, outline) flat colours
    "door":           ((40, 30, 28), (40, 30, 28)),
    "wreck":          ((150, 98, 58), (120, 74, 40)),
    "mast":           ((120, 74, 40), (120, 74, 40)),
    "hall":           ((126, 84, 52), (100, 62, 36)),
    "porch":          ((214, 120, 40), (190, 96, 20)),
    "gable":          ((176, 110, 70), (150, 86, 48)),
    "palisade":       ((112, 82, 58), (112, 82, 58)),
    "standing_stone": ((128, 128, 136), (100, 100, 110)),
    "stone":          ((128, 128, 136), (100, 100, 110)),
    "cave":           ((18, 18, 22), (18, 18, 22)),
    "stair":          ((186, 172, 150), (140, 126, 104)),
    "fallen_stone":   ((150, 150, 156), (150, 150, 156)),
}


def px(x, y, z=0.0):
    return X0 + P * x, Y0 + P * S * y - P * C * z


def heightfield():
    hf = L["sculpt"]["heightfield"]
    Hh = np.fromfile(os.path.join(BV2, hf["file"]), dtype="<f4").reshape(hf["shape"])
    return Hh, hf["extent_sim_m"], float(hf["px_per_m"])


def sample(grid, ex, ppm, x, y, order=1, cval=0.0):
    return ndimage.map_coordinates(grid, [(y - ex["y0"]) * ppm, (x - ex["x0"]) * ppm], order=order, mode="nearest" if cval is None else "constant", cval=cval if cval is not None else 0.0)


def ground_zones():
    Hh, ex, hp = heightfield()
    cm = np.asarray(Image.open(os.path.join(BV2, GCM["png"]))).copy()
    cex, cpp = GCM["extent_sim_m"], float(GCM["px_per_m"])
    names = GCM["classes"]
    # the mini-biomes do not stop at the walkable edge: plain land within CARRY_M (+- noise) of the floor takes its
    # nearest biome (heather on the barrow toe, shingle to the shore, rock to the cliff, ash round the hall)
    inv = {v: int(k) for k, v in names.items()}
    biome = np.isin(cm, [inv[n] for n in ("grave_ground", "shore_shingle", "cliff_top_rock", "hall_yard_ash", "snow_field")])
    d, (iy, ix) = ndimage.distance_transform_edt(~biome, return_indices=True)
    rng = np.random.default_rng(3)
    nz = ndimage.zoom(rng.standard_normal((cm.shape[0] // 24 + 3, cm.shape[1] // 24 + 3)), 24, order=3)[:cm.shape[0], :cm.shape[1]]
    reach = (CARRY_M + 2.2 * nz / (nz.std() + 1e-9)) * cpp
    take = (cm == inv["outside_land"]) & (d < reach)
    cm[take] = cm[iy[take], ix[take]]
    zid = {n: i for i, n in enumerate(ZONES)}
    lut_cls = np.array([zid.get(names[str(k)], zid["land_snow"]) if names[str(k)] not in ("outside_land", "outside_shore_ice", "outside_sea")
                        else -1 for k in range(len(names))])
    mound = next(f for f in L["features"] if f["kind"] == "mound")["footprint"]
    mimg = Image.new("L", (int((cex["x1"] - cex["x0"]) * cpp), int((cex["y1"] - cex["y0"]) * cpp)), 0)
    ImageDraw.Draw(mimg).polygon([((q[0] - cex["x0"]) * cpp, (q[1] - cex["y0"]) * cpp) for q in mound], fill=1)
    mgrid = np.asarray(mimg)
    gy, gx = np.gradient(Hh, 1.0 / hp)
    slope = np.hypot(gx, gy)
    Wk, Hk = W // K, H // K
    xs = (np.arange(Wk) * K + K / 2 - X0) / P
    ys = np.arange(ex["y1"], ex["y0"], -DY)                         # south -> north
    XX, YY = np.meshgrid(xs, ys)                                   # (ny, nx)
    h = sample(Hh, ex, hp, XX, YY, order=1, cval=None)
    f = S * YY - C * h                                             # screen-metres of each ground sample
    F = np.minimum.accumulate(f, axis=0)                           # running min from the SOUTH (rows are south->north)
    # largest-y (first from the south) sample with f <= row: in south->north order that is the FIRST index where F <= row
    rows = (np.arange(Hk) * K + K / 2 - Y0) / P                    # screen-metres of each output row
    hit = np.full((Hk, Wk), -1, np.int32)
    negF = -F                                                      # non-decreasing down the column
    for c in range(Wk):
        idx = np.searchsorted(negF[:, c], -rows, side="left")      # first i with -F_i >= -row  <=>  F_i <= row
        idx[idx >= len(ys)] = -1
        hit[:, c] = idx
    ok = hit >= 0
    hy = np.where(ok, ys[np.clip(hit, 0, None)], np.nan)
    hx = np.broadcast_to(xs[None, :], hy.shape)
    hz = np.where(ok, sample(Hh, ex, hp, hx, np.nan_to_num(hy), order=1, cval=None), 0)
    cls = sample(cm.astype(np.float32), cex, cpp, hx, np.nan_to_num(hy), order=0, cval=None).astype(int)
    z = lut_cls[cls]
    outside = z < 0
    nm = lambda n: zid[n]
    out = np.full(z.shape, nm("land_snow"))
    sl = sample(slope.astype(np.float32), ex, hp, hx, np.nan_to_num(hy), order=1, cval=None)
    inm = sample(mgrid.astype(np.float32), cex, cpp, hx, np.nan_to_num(hy), order=0, cval=None) > 0.5
    out[(hz <= -4.35)] = nm("sea")
    out[(hz > -0.62) & (hz <= -0.38)] = nm("shore_ice")
    out[(hz > -0.42) & (hz < -0.05) & (sl < 0.6)] = nm("beach_shingle")
    out[inm & (hz > 0.25)] = nm("barrow_mound")
    out[(sl > 1.05) & (hz > -4.35)] = nm("rock_face")
    cls_name = np.array([names[str(k)] for k in range(len(names))])[cls]
    out[(cls_name == "outside_shore_ice") & (hz > -0.62) & (hz < -0.05)] = nm("shore_ice")
    z = np.where(outside, out, z)
    z[~ok] = nm("land_snow")
    return z, hz, ok


def main():
    zk, hz, ok = ground_zones()
    # the 0.5 m heightfield's sawtooth (cliff faces, bank teeth) is not a shape to hand a painter: a median
    # (majority-like) filter on the zone index, outside the floor only
    Wk, Hk = W // K, H // K
    fm = Image.new("L", (Wk, Hk), 0)
    ImageDraw.Draw(fm).polygon([((X0 + P * q[0]) / K, (Y0 + P * S * q[1]) / K) for q in L["floor"]["polygon"]], fill=255)
    floor = np.asarray(fm) > 0
    zmed = ndimage.median_filter(zk.astype(np.uint8), size=19)
    zk = np.where(floor, zk, zmed)
    lut = np.array(list(ZONES.values()), np.float32)
    rgb = lut[zk]
    # the floor's mini-biomes MELD at their seams (R-C9-144): a 1.5 m soft blend inside the floor only
    # (the frozen water keeps a crisper edge: the mere is p05's deliverer, its ice edge is a real shoreline)
    def soft(mask, sig):
        fw = mask.astype(np.float32)
        return np.stack([ndimage.gaussian_filter(rgb[..., c] * fw, sig) for c in range(3)], -1) / np.maximum(ndimage.gaussian_filter(fw, sig), 1e-4)[..., None]
    water = np.isin(zk, [list(ZONES).index("mere_ice"), list(ZONES).index("stream_ice")])
    zl = list(ZONES)
    land_f = np.isin(zk, [zl.index(n) for n in ("floor_snow", "grave_ground", "shore_shingle", "cliff_top_rock", "hall_yard_ash",
                                                 "snow_field", "circle", "path", "land_snow")])
    bl = soft(land_f, 0.8 * P / K)
    wsoft = ndimage.gaussian_filter(water.astype(np.float32), 0.25 * P / K)[..., None]
    rgb = np.where(land_f[..., None], bl, rgb)
    rgb = np.where(floor[..., None], rgb * (1 - wsoft) + np.array(ZONES["mere_ice"], np.float32) * wsoft, rgb)
    # a soft height tint on the land outside the floor: higher = a touch bluer-grey (relief, no shading)
    tint = np.clip(hz / 7.0, 0, 1)[..., None] * (zk[..., None] == list(ZONES).index("land_snow"))
    rgb = rgb * (1 - 0.22 * tint) + np.array([190, 200, 216], np.float32) * 0.22 * tint
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((W, H), Image.NEAREST).filter(ImageFilter.GaussianBlur(1.2))
    dr = ImageDraw.Draw(im)
    # ---- structures: flat footprint at its base + a thin outline of how high it rises on screen
    order = []
    for f in L["features"]:
        k = f["kind"]
        if k not in MARKS or k == "cliff":
            continue
        fp = f["footprint"]; z0 = float(f["z_bottom_m"]); z1 = float(f["z_top_m"])
        order.append((max(q[1] for q in fp), k, fp, z0, z1))
    st = L["stair"]
    fl = st["flight"]["polygon"]       # top wall-side, top sea-side, foot sea-side, foot wall-side
    zf = [0.0, 0.0, float(st["flight"]["z_bottom_m"]), float(st["flight"]["z_bottom_m"])]
    order.sort(key=lambda t: t[0])
    for _, k, fp, z0, z1 in order:
        fill, line = MARKS[k]
        if k == "cave":
            # the mouth is a dark opening IN the cliff face: its face quad (outer edge, from its floor to its roof)
            q = sorted(fp, key=lambda p: -p[1])[:2]
            dr.polygon([px(q[0][0], q[0][1], z0), px(q[1][0], q[1][1], z0), px(q[1][0], q[1][1], z1), px(q[0][0], q[0][1], z1)], fill=fill)
            continue
        hull = hull2([px(q[0], q[1], z) for q in fp for z in (z0, z1)])
        if z1 - z0 > 0.6 and k not in ("palisade",):
            dr.line(hull + [hull[0]], fill=line, width=3)
        dr.polygon([px(q[0], q[1], z0) for q in fp], fill=fill)
        if k == "palisade":
            # a stake line: the run's base, plus its top as a thin line
            dr.line([px(q[0], q[1], z1) for q in fp] + [px(fp[0][0], fp[0][1], z1)], fill=line, width=2)
    for poly, zs in ((st["top_landing"]["polygon"], None), (st["bottom_landing"]["polygon"], float(st["bottom_landing"]["z_m"]))):
        dr.polygon([px(q[0], q[1], zs if zs is not None else 0.0) for q in poly], fill=MARKS["stair"][0])
    dr.polygon([px(q[0], q[1], z) for q, z in zip(fl, zf)], fill=MARKS["stair"][0], outline=MARKS["stair"][1])
    # step lines across the flight (the stair's own direction, nothing more)
    n = int(st["flight"]["n_steps"])
    for i in range(1, n):
        t = i / n
        a = [fl[0][j] + (fl[3][j] - fl[0][j]) * t for j in (0, 1)]
        b = [fl[1][j] + (fl[2][j] - fl[1][j]) * t for j in (0, 1)]
        zz = zf[0] + (zf[3] - zf[0]) * t
        dr.line([px(a[0], a[1], zz), px(b[0], b[1], zz)], fill=MARKS["stair"][1], width=1)
    # ---- the floor's edge (faint dotted) and the six spawn discs (faint dotted ellipses): NOT to be painted
    flp = [px(q[0], q[1]) for q in L["floor"]["polygon"]]
    dotted(dr, flp + [flp[0]], (150, 150, 160), 6, 14, 3)
    for a in L["anchors"]["points"]:
        cx, cy = px(a["x"], a["y"])
        ell = [(cx + 8 * P * math.cos(t), cy + 8 * P * S * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 240)]
        dotted(dr, ell, (205, 170, 110), 5, 16, 2)
    out = os.path.join(PAINT, "barrow_v2_zonemap.png")
    im.save(out, optimize=True)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    pv = im.copy(); pv.thumbnail((2400, 2400)); pv.save(os.path.join(PAINT, "barrow_v2_zonemap_preview.jpg"), quality=86)
    json.dump({"zones_rgb": ZONES, "marks_rgb": {k: {"fill": v[0], "outline": v[1]} for k, v in MARKS.items()},
               "dotted_grey": "the walkable floor's edge (not to be painted)", "dotted_gold": "the six 8 m spawn discs (not to be painted)",
               "zonemap": os.path.relpath(out, BV2), "sha256": sha}, open(os.path.join(PAINT, "zonemap_legend.json"), "w"), indent=1)
    print(out, im.size, "sha256", sha)


def hull2(pts):
    pts = sorted(set((round(p[0], 2), round(p[1], 2)) for p in pts))
    if len(pts) < 3:
        return pts
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def dotted(dr, pts, col, on, off, w):
    acc, draw = 0.0, True
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L_ = math.hypot(x1 - x0, y1 - y0); t = 0.0
        while t < L_:
            seg = min((on if draw else off) - acc, L_ - t)
            if draw:
                a = (x0 + (x1 - x0) * t / L_, y0 + (y1 - y0) * t / L_); b = (x0 + (x1 - x0) * (t + seg) / L_, y0 + (y1 - y0) * (t + seg) / L_)
                dr.line([a, b], fill=col, width=w)
            t += seg; acc += seg
            if acc >= (on if draw else off) - 1e-9:
                acc, draw = 0.0, not draw


if __name__ == "__main__":
    main()
