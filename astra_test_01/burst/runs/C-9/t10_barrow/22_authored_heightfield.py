#!/usr/bin/env python3
"""C-9 T10: the AUTHORED barrow ground -- the plan from the painting, the relief by hand.

    python3 22_authored_heightfield.py --variant a

The derived heightfield (21_heightfield.py) carries a 1.71x calibration spread, because the
one thing a monocular model cannot measure from an orthographic painting is the absolute
depth scale. What the painting DOES give reliably is the PLAN: where the tarn is, where the
mound is, where the outcrops break through, and how big everything is across the screen --
all of that is ruler work through K, with no depth model in it.

So this builds the same grid from the half of the evidence that is solid, plus four
constraints read off the picture and stated as numbers rather than inferred:

    the tarn is FLAT and LOW        a frozen tarn has a level surface, by definition
    the mound is a RAISED DOME      a barrow is a heaped mound with a door cut into it
    the middle is GENTLY SLOPING    it is the walkable ground; the concept shows it open
    the edges RISE into the outcrops where bedrock breaks through the snow

Every one of those is a parameter at the top of this file, not a number buried in a
formula, because the point of the authored surface is that it can be argued with.

THE PLAN POSITIONS ARE UNPROJECTED AT h = 0, and that is a real approximation worth naming:
a ground point's plan position moves by 0.755 m for every metre of height, so a feature
2 m up sits 1.5 m from where a flat unprojection puts it. The script therefore runs TWICE
-- once flat to get the plan, once more with the authored heights in hand -- and reports
how far things moved between the passes, which is the size of the approximation rather
than a promise that it is small.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts" / "T10C-barrow"
WORK = HERE / "work"
OUT = HERE / "out"

RIGHT = np.array([0.681998491287231, 0.0, -0.731353580951691])
UP = np.array([-0.583728015422821, 0.60246217250824, -0.54433536529541])
FWD = np.array([-0.440612882375717, -0.798147439956665, -0.410878270864487])
SIN_P, COS_P = 0.798147439956665, 0.602462172508240

# ---- the four constraints, as numbers -------------------------------------------------
TARN_DROP_M = 1.15      # how far the ice sits below the surrounding snow field
MOUND_RISE_M = 1.70     # the barrow's crown above the walkable ground
OUTCROP_RISE_M = 0.55   # bedrock shouldering up through the snow
GROUND_SLOPE = 0.055    # m per m, rising AWAY from the camera across the play space
SMOOTH_M = 0.85         # the radius over which one region blends into the next


def unproject(px, py, K, W, H, h):
    u = (px - W / 2.0) / K
    v = -(py - H / 2.0) / K
    D = (COS_P * v - h) / SIN_P
    return (RIGHT[0] * u + UP[0] * v + FWD[0] * D,
            RIGHT[2] * u + UP[2] * v + FWD[2] * D)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="a")
    ap.add_argument("--grid", type=float, default=0.05)
    a = ap.parse_args()
    v = a.variant

    ref = json.loads((OUT / ("height_%s_marigold.json" % v)).read_text())
    K = ref["figure"]["px_per_metre"]
    GW, GH = ref["heightfield"]["size"]
    g = a.grid
    W, H = ref["image"]

    def mask(nm):
        p = WORK / ("evf_%s_%s.png" % (v, nm))
        return (np.asarray(Image.open(p).convert("L")) > 127) if p.exists() else None

    ice = mask("ice")
    door = mask("barrow_door")
    stones = mask("standing_stones")
    objs = json.loads((OUT / ("objects_%s.json" % v)).read_text())
    rocks = [o for o in objs["objects"] if o["class"] == "rock_outcrop"]

    yy, xx = np.mgrid[0:H, 0:W]
    rep = {"variant": v, "grid_m": g, "size": [GW, GH],
           "constraints": {"tarn_drop_m": TARN_DROP_M, "mound_rise_m": MOUND_RISE_M,
                           "outcrop_rise_m": OUTCROP_RISE_M,
                           "ground_slope_m_per_m": GROUND_SLOPE, "blend_m": SMOOTH_M}}

    hf = np.zeros((GH, GW), np.float32)
    shift_report = None
    for it, hguess in enumerate((None, "self")):
        # where every screen pixel lands in plan, given the current height estimate
        if hguess is None:
            hpx = np.zeros((H, W), np.float32)
        else:
            gx0 = np.clip(((wx_all - x0) / g).astype(np.int32), 0, GW - 1)
            gz0 = np.clip(((wz_all - z0) / g).astype(np.int32), 0, GH - 1)
            hpx = hf[gz0, gx0]
        wx_all, wz_all = unproject(xx, yy, K, W, H, hpx)
        if it == 0:
            x0, z0 = float(wx_all.min()), float(wz_all.min())
            first = (wx_all.copy(), wz_all.copy())
        else:
            d = np.hypot(wx_all - first[0], wz_all - first[1])
            shift_report = {"mean_m": round(float(d.mean()), 3),
                            "p95_m": round(float(np.percentile(d, 95)), 3),
                            "max_m": round(float(d.max()), 3)}

        gx = np.clip(((wx_all - x0) / g).astype(np.int32), 0, GW - 1)
        gz = np.clip(((wz_all - z0) / g).astype(np.int32), 0, GH - 1)

        def to_grid(m):
            out = np.zeros((GH, GW), bool)
            if m is None:
                return out
            out[gz[m], gx[m]] = True
            return ndimage.binary_closing(out, np.ones((5, 5)))

        g_ice, g_door, g_stone = to_grid(ice), to_grid(door), to_grid(stones)

        # the walkable ground: a plane tilted away from the camera
        azim = np.array([FWD[0], FWD[2]])
        azim = azim / np.linalg.norm(azim)
        gxs, gzs = np.meshgrid(np.arange(GW) * g, np.arange(GH) * g)
        along = gxs * azim[0] + gzs * azim[1]
        base = -GROUND_SLOPE * (along - along.mean())

        target = base.copy()
        # the mound: a dome centred on the doorway, sized by the door's own plan extent
        if g_door.any():
            zs, xs = np.nonzero(g_door)
            mcx, mcz = xs.mean() * g, zs.mean() * g
            # the mound is the hill BEHIND the door, so push its centre away from the camera
            mcx += azim[0] * 2.2
            mcz += azim[1] * 2.2
            rad = max(2.6, float(np.hypot(xs.std(), zs.std()) * g * 2.2))
            d2 = np.hypot(gxs - mcx, gzs - mcz)
            target += MOUND_RISE_M * np.exp(-(d2 / rad) ** 2.2)
            rep["mound"] = {"centre_xz": [round(mcx, 2), round(mcz, 2)],
                            "radius_m": round(rad, 2), "rise_m": MOUND_RISE_M}
        # the outcrops: a local rise at each one, scaled by its measured height
        for o in rocks:
            ox = (o["world_xz"][0] - x0)
            oz = (o["world_xz"][1] - z0)
            r = max(0.35, o["width_m"] * 0.7)
            d2 = np.hypot(gxs - ox, gzs - oz)
            target += OUTCROP_RISE_M * min(1.0, o["height_m"] / 1.2) * np.exp(-(d2 / r) ** 2)
        # blend everything that is not the tarn
        target = ndimage.gaussian_filter(target, SMOOTH_M / g)
        # the tarn LAST, and flat: a frozen surface is level, and smoothing it would tilt it
        if g_ice.any():
            lvl = float(np.percentile(target[g_ice], 20)) - TARN_DROP_M
            w = ndimage.gaussian_filter(g_ice.astype(np.float32), 0.45 / g)
            w = np.clip(w / max(w.max(), 1e-6), 0, 1)
            target = target * (1 - w) + lvl * w
            rep["tarn"] = {"level_m": round(lvl, 2), "cells": int(g_ice.sum()),
                           "drop_m": TARN_DROP_M}
        hf = target.astype(np.float32)

    rep["plan_shift_between_passes"] = shift_report
    gy, gxg = np.gradient(hf, g)
    slope = np.degrees(np.arctan(np.hypot(gy, gxg)))
    rep["heightfield"] = {
        "extent_m": [round(GW * g, 2), round(GH * g, 2)],
        "height_range_m": [round(float(hf.min()), 3), round(float(hf.max()), 3)],
        "relief_m": round(float(hf.max() - hf.min()), 3),
        "slope_deg": {"median": round(float(np.median(slope)), 1),
                      "p90": round(float(np.percentile(slope, 90)), 1),
                      "over_45_pct": round(float((slope > 45).mean() * 100), 2),
                      "over_70_pct": round(float((slope > 70).mean() * 100), 2)},
        "roughness_lap_rms_m": round(float(np.sqrt((ndimage.laplace(hf) ** 2).mean())), 4),
    }
    lo, hi = float(hf.min()), float(hf.max())
    span = max(hi - lo, 1e-6)
    Image.fromarray(((hf - lo) / span * 65535).astype(np.uint16), mode="I;16").save(
        OUT / ("height_%s_authored.png" % v))
    rep["png"] = {"file": str(OUT / ("height_%s_authored.png" % v)),
                  "encoding": "16-bit, 0 = min height, 65535 = max",
                  "metres_per_pixel": g, "height_min_m": round(lo, 4),
                  "height_max_m": round(hi, 4),
                  "world_origin_xz": [round(x0, 3), round(z0, 3)]}
    (OUT / ("height_%s_authored.json" % v)).write_text(json.dumps(rep, indent=1) + "\n")
    print(json.dumps({k: rep[k] for k in
                      ("heightfield", "mound", "tarn", "plan_shift_between_passes")
                      if k in rep}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
