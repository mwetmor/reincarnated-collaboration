#!/usr/bin/env python3
"""P7 (CLEAN FLOOR, measured ON THE PAINTING) and P8 (HEATHER FROM THE PAINTED TUFTS) -- constraint rows (charter
§ 9 C-1 as amended by Gate-1 W-1: a v1 positive control, RED shown once on a constructed input; not discarded for
failing to separate R-C9-159).

P7. On the walkable FLOOR and in every LANE, painted on the painting itself:
    tuft share    = painted tuft pixels (v1's step-3 classifier, paint_world_prep.tuft_classes, verbatim) / area
    clutter share = pixels whose L* (0.05 m Gaussian) < 55, not tufts / area (rock, wood, dark debris; snow's blue
                    shadow dabs sit at L* 70-85 and are flat marks)
    v1: floor = the arena disc (barrow_full_layout.json regions: disc uv (0,1) r 7 m, "nothing placed"); lanes = the
        4 m path polyline ("path ground; nothing placed on it") and the door corridor (half_w 1.3 m, v 8.6-10.5).
    BARS from v1's own spread: floor -- the max over the disc's four quadrants; lanes -- the max over 2 m lane segments.
    A level: its floor polygon and lanes (sim xz), projected by its paint frame.
    CONSTRUCTED RED: a 3 x 3 m patch of v1's own heather ground (uv (-11, 4), dense painted tufts) pasted onto the
    arena centre (uv (0, 1)).
P8. HEATHER SHARE ON PAINTED TUFTS: each 3D heather instance (godot/data/.../heather.json rows x, z) projected to the
    painting at a tuft's half-height (0.15 m, v1's rule) -- ON a tuft if any painted tuft pixel lies within its screen
    footprint radius (24 px, v1's heather footprint_px 47.1 / 2). Share = instances on tufts / instances.
    TINT agreement -- Pearson r between each instance's mul_r/mul_b and the painting's R/B under its footprint ("tinted
    from the paint"); PASS needs share >= bar AND both r >= 0.90 x v1's lower r (also provisional).
    BAR: PROVISIONAL = 0.90 x v1's value measured here, until lane PT's reproduced v1 value lands (Gate-1 W-2: the
    plan's 50% withdrawn; the recorded 0.44-0.47 is a different quantity -- painted tuft cells COVERED, take/build/
    painted_prep.json heather.placement.heather.tuft_cells_covered_share 0.4379).
    CONSTRUCTED RED: v1's instances displaced by a seeded random 3-8 m each (placed by noise, not from the tufts).
"""
import argparse
import importlib.util
import math
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

C47, S47 = math.cos(math.radians(47)), math.sin(math.radians(47))
SINP = math.sin(math.radians(PITCH))


def _pw():
    spec = importlib.util.spec_from_file_location("pw_v1_readonly", BF / "tools/paint_world_prep.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


PW = _pw()


def poly_mask(shape, pts):
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=1)
    return np.asarray(im, bool)


def tuft_clutter(P8):
    heather, shrub = PW.tuft_classes(P8, np.ones(P8.shape[:2], bool))
    tufts = heather | shrub
    L = ndimage.gaussian_filter(rgb_to_lab(P8.astype(np.float32))[..., 0], 0.05 * PPM_V1)
    return tufts, (L < 55) & ~tufts


def shares(tufts, clutter, m):
    n = max(int(m.sum()), 1)
    return {"tuft": round(float((tufts & m).sum() / n), 4), "clutter": round(float((clutter & m).sum() / n), 4), "px": n}


# ---------------------------------------------------------------- v1 geometry
def v1_px(u, v, h=0.0):
    return PW.px_of_uv(u, v, h)


def v1_disc(shape, cu, cv, r, quadrant=None):
    pts = []
    a0, a1 = (0, 360) if quadrant is None else (90 * quadrant, 90 * quadrant + 90)
    if quadrant is not None:
        pts.append(v1_px(cu, cv))
    for a in np.linspace(a0, a1, 64):
        pts.append(v1_px(cu + r * math.cos(math.radians(a)), cv + r * math.sin(math.radians(a))))
    return poly_mask(shape, pts)


def v1_lane_segments(shape):
    L = jload(BF / "barrow_full_layout.json")["regions"]
    path = [r for r in L.values() if r.get("type") == "polyline"][0]
    corr = [r for r in L.values() if r.get("type") == "corridor"][0]
    segs = []
    pts = np.array(path["points_uv"], float)
    hw = path["width_m"] / 2
    for (u0, v0), (u1, v1) in zip(pts[:-1], pts[1:]):
        d = math.hypot(u1 - u0, v1 - v0)
        n = max(1, int(d // 2))
        for i in range(n):
            a = np.array([u0, v0]) + (np.array([u1, v1]) - [u0, v0]) * i / n
            b = np.array([u0, v0]) + (np.array([u1, v1]) - [u0, v0]) * (i + 1) / n
            t = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            nrm = np.array([-t[1], t[0]]) * hw
            q = [a + nrm, b + nrm, b - nrm, a - nrm]
            segs.append(("path seg %d" % len(segs), poly_mask(shape, [v1_px(*p) for p in q])))
    h = corr["half_w_m"]
    va, vb = corr["v"]
    segs.append(("door corridor", poly_mask(shape, [v1_px(-h, va), v1_px(h, va), v1_px(h, vb), v1_px(-h, vb)])))
    return segs


def p7_v1(P8):
    tufts, clutter = tuft_clutter(P8)
    floor = v1_disc(P8.shape, 0.0, 1.0, 7.0)
    quads = [shares(tufts, clutter, v1_disc(P8.shape, 0.0, 1.0, 7.0, q)) for q in range(4)]
    lanes = [(nm, shares(tufts, clutter, m)) for nm, m in v1_lane_segments(P8.shape)]
    return {"floor": shares(tufts, clutter, floor), "floor_quadrants": quads, "lanes": dict(lanes)}


def p7_bars(v1):
    return {"floor_tuft": max(q["tuft"] for q in v1["floor_quadrants"]), "floor_clutter": max(q["clutter"] for q in v1["floor_quadrants"]),
            "lane_tuft": max(l["tuft"] for l in v1["lanes"].values()), "lane_clutter": max(l["clutter"] for l in v1["lanes"].values())}


def p7_verdict(r, b):
    f = r["floor"]
    ok_f = f["tuft"] <= b["floor_tuft"] and f["clutter"] <= b["floor_clutter"]
    bad_l = [k for k, l in r["lanes"].items() if l["tuft"] > b["lane_tuft"] or l["clutter"] > b["lane_clutter"]]
    return {"floor": f, "lanes_over": bad_l, "pass": ok_f and not bad_l}


# ---------------------------------------------------------------- a v2-frame level (R-C9-159)
def v2_px(F, x, z, h=0.0):
    u = x * C47 - z * S47
    v = -x * S47 - z * C47
    return (u - F["u0"]) * F["ppm"], (F["v1"] - v) * F["ppm"] * SINP - h * F["ppm"] * math.cos(math.radians(PITCH))


def p7_159():
    lvl = jload(BF / "godot/data/barrow_v2_sw/level.json")
    F = lvl["frame"]["paint"]
    P8 = np.asarray(Image.open(BF / "godot/data/barrow_v2_sw/painted/ground.png").convert("RGB"))
    tufts, clutter = tuft_clutter(P8)
    floor = poly_mask(P8.shape, [v2_px(F, x, z) for x, z in lvl["floor_polygon_xz"]])
    floor &= np.ones_like(floor)
    lanes = {k: shares(tufts, clutter, poly_mask(P8.shape, [v2_px(F, x, z) for x, z in pts])) for k, pts in lvl["lanes"].items()}
    lanes = {k: v for k, v in lanes.items() if v["px"] > 2000}       # lanes inside this section's paint frame only
    return {"floor": shares(tufts, clutter, floor), "lanes": lanes, "floor_in_frame_px": int(floor.sum())}


# ---------------------------------------------------------------- P8
def p8_v1(rows=None, seed=None):
    H = jload(BF / "godot/data/painted/heather.json")
    rows = np.array(H["rows"], float) if rows is None else rows
    P8 = np.asarray(Image.open(PW.PAINTING).convert("RGB"))
    idx, _ = PW.id_index()
    heather, shrub = PW.tuft_classes(P8, idx == 0)
    tuft = heather | shrub
    if seed is not None:
        rng = np.random.default_rng(seed)
        ang = rng.uniform(0, 2 * math.pi, len(rows))
        d = rng.uniform(3, 8, len(rows))
        rows = rows.copy()
        rows[:, 0] += d * np.cos(ang)
        rows[:, 1] += d * np.sin(ang)
    return _p8(rows, tuft, P8, lambda x, z: PW.px_of_uv(x * C47 - z * S47, -x * S47 - z * C47, 0.15))


def _p8(rows, tuft, P8, to_px):
    near = ndimage.binary_dilation(tuft, structure=_disk(24))
    on, tint = 0, []
    H, W = tuft.shape
    for r in rows:
        x, y = to_px(r[0], r[1])
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < W and 0 <= yi < H:
            if near[yi, xi]:
                on += 1
            y0, y1, x0, x1 = max(yi - 24, 0), min(yi + 25, H), max(xi - 24, 0), min(xi + 25, W)
            m = tuft[y0:y1, x0:x1]
            if m.sum() > 20:
                c = P8[y0:y1, x0:x1][m].mean(0)
                tint.append((r[4], r[6], c[0], c[2]))
    t = np.array(tint) if tint else np.zeros((0, 4))
    rr = float(np.corrcoef(t[:, 0], t[:, 2])[0, 1]) if len(t) > 3 else None
    rb = float(np.corrcoef(t[:, 1], t[:, 3])[0, 1]) if len(t) > 3 else None
    return {"instances": int(len(rows)), "on_painted_tufts": on, "share": round(on / max(len(rows), 1), 4),
            "tint_r_vs_paint_r": None if rr is None else round(rr, 3), "tint_b_vs_paint_b": None if rb is None else round(rb, 3)}


def _disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def p8_159():
    lvl = jload(BF / "godot/data/barrow_v2_sw/level.json")
    F = lvl["frame"]["paint"]
    rows = np.array(jload(BF / "godot/data/barrow_v2_sw/heather.json")["rows"], float)
    P8 = np.asarray(Image.open(BF / "godot/data/barrow_v2_sw/painted/ground.png").convert("RGB"))
    heather, shrub = PW.tuft_classes(P8, np.ones(P8.shape[:2], bool))
    return _p8(rows, heather | shrub, P8, lambda x, z: v2_px(F, x, z, 0.15))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.parse_args()
    P8 = np.asarray(Image.open(PW.PAINTING).convert("RGB"))
    v1 = p7_v1(P8)
    bars = p7_bars(v1)
    C = P8.copy()
    sx, sy = v1_px(-11.0, 4.0)
    dx, dy = v1_px(0.0, 1.0)
    w, h = int(3 * PPM_V1), int(3 * PPM_V1 * SINP)
    C[int(dy - h / 2):int(dy + h / 2), int(dx - w / 2):int(dx + w / 2)] = P8[int(sy - h / 2):int(sy + h / 2), int(sx - w / 2):int(sx + w / 2)]
    p7 = {"bars_from_v1": bars, "v1": dict(v1, **p7_verdict(v1, bars)), "constructed": p7_verdict(p7_v1(C), bars)}
    r159 = p7_159()
    p7["159"] = dict(r159, **p7_verdict(r159, bars))
    for k in ("v1", "constructed", "159"):
        print("P7 %-12s floor tuft %.4f clutter %.4f  lanes over %s -> %s" % (k, p7[k]["floor"]["tuft"], p7[k]["floor"]["clutter"],
                                                                         p7[k]["lanes_over"], "PASS" if p7[k]["pass"] else "FAIL"))
    print("   bars", bars)
    a = p8_v1()
    bar = round(0.9 * a["share"], 4)
    tbar = round(0.9 * min(a["tint_r_vs_paint_r"], a["tint_b_vs_paint_b"]), 3)

    def ok(r):
        t = [x for x in (r["tint_r_vs_paint_r"], r["tint_b_vs_paint_b"]) if x is not None]
        return r["share"] >= bar and bool(t) and min(t) >= tbar
    p8 = {"bar_provisional": bar, "bar_rule": "0.90 x v1 measured here, PROVISIONAL until PT's reproduced v1 value (W-2)",
          "tint_bar_provisional": None, "v1": dict(a, **{"pass": None}), "constructed": None, "159": None}
    p8["tint_bar_provisional"] = tbar
    p8["v1"]["pass"] = ok(a)
    c = p8_v1(seed=8)
    p8["constructed"] = dict(c, **{"pass": ok(c)})
    b = p8_159()
    p8["159"] = dict(b, **{"pass": ok(b)})
    for k in ("v1", "constructed", "159"):
        print("P8 %-12s share %.4f of %d (bar %.4f)  tint r %s b %s -> %s" % (k, p8[k]["share"], p8[k]["instances"], bar,
              p8[k]["tint_r_vs_paint_r"], p8[k]["tint_b_vs_paint_b"], "PASS" if p8[k]["pass"] else "FAIL"))
    dump({"p7": p7, "p8": p8}, str(PH / "results/p7_p8.json"))
