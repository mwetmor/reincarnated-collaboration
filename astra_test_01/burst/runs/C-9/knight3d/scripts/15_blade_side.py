#!/usr/bin/env python3
"""C-9 knight3d: WHICH SIDE of the haft is the pollaxe's blade on?

Matt, R-C9-57: "the poleaxe blade is pointing backwards." Before rotating
anything, measure it, in the figure's own frame, from the eight mattes.

Method. In each view the head occupies the rows where the axe matte is wide.
Fit the haft's centre line (01_matte_seeds already isolates the haft as a
constant-width bar, so the axe mask minus a dilated haft leaves head only).
For the head rows, split the head's pixels either side of the haft centre and
take the signed screen offset of the head's area centroid.

That screen offset is  du = h . r(alpha),  with r = (-cos a, sin a, 0), for a
head whose offset from the haft in the FIGURE's frame is h = (hx, hy). Two
unknowns, eight equations -> least squares. The sign of hy is the answer:
hy > 0 means the blade sits FORWARD of the haft (the way the knight faces).
"""
import json, os, sys
import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(HERE)))
K3 = os.path.dirname(HERE)
MASKS = os.path.join(K3, "work", "masks")
OUT = os.path.join(K3, "out")
FIT = json.load(open(os.path.join(K3, "work", "fit_result.json")))
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]


def main():
    rows = []
    for d in DIRS:
        axe = np.load(os.path.join(MASKS, "%s_axe.npy" % d))
        ys = np.where(axe.any(axis=1))[0]
        wid = np.array([int(axe[y].sum()) for y in ys])
        haft_w = float(np.median(wid[wid < 60]))
        head_rows = ys[wid > haft_w * 2.2]
        if not len(head_rows):
            continue
        y0, y1 = int(head_rows.min()), int(head_rows.max())
        band = axe[y0:y1 + 1]
        # the haft's centre through the head rows: interpolate from the rows
        # above and below the head, where the matte is haft-only
        near = ys[(wid <= haft_w * 1.6)]
        cs = [(int(y), float(np.where(axe[y])[0].mean())) for y in near]
        ya = np.array([c[0] for c in cs], float); xa = np.array([c[1] for c in cs])
        m, c = np.polyfit(ya, xa, 1)
        yy, xx = np.where(band)
        cx = m * (yy + y0) + c
        off = xx - cx
        # head pixels only: drop anything within the haft's own width
        keep = np.abs(off) > haft_w * 0.6
        du = float(off[keep].mean())
        # The centroid is a weak witness: the fan and the fluke sit on
        # opposite sides and partly cancel, so it reports a few px on a head
        # 213 px across. What distinguishes a FAN from a FLUKE is REACH, so
        # measure how far the head extends each way, and which way holds the
        # bulk of the area.
        o = off[keep]
        reach_p = float(o.max()) if (o > 0).any() else 0.0
        reach_n = float(o.min()) if (o < 0).any() else 0.0
        area_p = int((o > 0).sum()); area_n = int((o < 0).sum())
        fan_du = reach_p if abs(reach_p) >= abs(reach_n) else reach_n
        H = int(np.ptp(np.where(np.load(os.path.join(MASKS, "%s_body.npy" % d))
                                .any(axis=1))[0]) + 1)
        rows.append(dict(view=d, head_rows=[y0, y1], haft_w_px=haft_w,
                         head_px=int(keep.sum()), du_px=du, du_over_H=du / H,
                         reach_fwdside_px=reach_p, reach_backside_px=reach_n,
                         area_fwdside_px=area_p, area_backside_px=area_n,
                         fan_du_over_H=fan_du / H,
                         alpha=FIT["canonical"]["views"][d]["alpha"],
                         nominal=FIT["canonical"]["views"][d]["nominal_alpha"]))

    for key, tag in (("alpha", "fitted azimuths"), ("nominal", "nominal azimuths")):
        A = np.array([[-np.cos(np.radians(r[key])), np.sin(np.radians(r[key]))]
                      for r in rows])
        b = np.array([r["fan_du_over_H"] for r in rows])
        h, *_ = np.linalg.lstsq(A, b, rcond=None)
        pred = A @ h
        res = pred - b
        print("\n%s:  head offset from the haft  hx = %+.4f H,  hy = %+.4f H"
              % (tag, h[0], h[1]))
        print("  (fitted on the FAN's reach, not the head's centroid)")
        print("  hy %s 0  ->  the blade sits %s of the haft"
              % (">" if h[1] > 0 else "<", "FORWARD" if h[1] > 0 else "BEHIND"))
        print("  %-4s %-8s %-11s %-11s %s" % ("view", "alpha", "measured", "predicted", "resid"))
        for r, p_, e in zip(rows, pred, res):
            print("  %-4s %-8.1f %+-11.4f %+-11.4f %+.4f   reach %+5.0f / %+5.0f px"
                  " area %5d / %5d" % (r["view"], r[key], r["fan_du_over_H"], p_, e,
                                       r["reach_fwdside_px"], r["reach_backside_px"],
                                       r["area_fwdside_px"], r["area_backside_px"]))
        print("  rms residual %.4f H" % np.sqrt((res ** 2).mean()))
        if key == "alpha":
            out = dict(note=__doc__.strip().splitlines()[0],
                       fan_direction_over_H=dict(fx=float(h[0]), fy=float(h[1])),
                       fan_bearing_deg_from_forward=float(
                           np.degrees(np.arctan2(h[0], h[1]))),
                       blade_side="FORWARD (+Y)" if h[1] > 0 else "BEHIND (-Y)",
                       rms_residual_over_H=float(np.sqrt((res ** 2).mean())),
                       per_view=rows)
    with open(os.path.join(OUT, "blade_side.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwrote", os.path.join(OUT, "blade_side.json"))


main()
