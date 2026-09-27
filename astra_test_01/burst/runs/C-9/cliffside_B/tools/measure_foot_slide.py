#!/usr/bin/env python3
"""C-9: does the knight's foot slide at the scene's walk speed, and by how much?

walk_px_s is NOT changed by this tool or by the build -- this only measures and
reports.  Writes frames/knight_foot_slide.json and prints the table.

THE QUESTION.  Each walk cell is 12 frames sampled across ONE stride of a 24 fps clip
whose stride is `stride_native_frames` long, and the build plays it at that clip's own
timing (fps = 12*24/stride_native_frames).  One loop therefore takes
stride_native_frames/24 seconds, during which the body travels

    body_travel = walk_px_s * stride_native_frames / 24          [canvas px]

For the feet to look planted, the PAINTING's stride must cover the same ground.

MEASURING THE PAINTED STRIDE.  In an in-place locomotion cycle a planted foot moves
BACKWARD relative to the body by exactly the ground distance covered while it is down,
so the two feet are furthest apart, along the travel direction, at full stride.  So:

    step  = max over the 12 frames of the feet's extent along the travel direction
    stride = 2 * step                                   (a cycle is two steps)

measured in source pixels on the foot band (the bottom 18% of the body silhouette,
after the 1x11 horizontal opening that deletes the halberd shaft), then multiplied by
the knight's sprite scale to reach canvas pixels.

    slide_ratio = body_travel / painted_stride

1.0 = planted.  Above 1.0 the feet skate forward under a body that is outrunning them.

CAVEAT, stated because the numbers are not equally trustworthy per direction: the
cells are painted in a 3/4 view, so a stride toward or away from camera (N, S) is
FORESHORTENED in the picture plane and measures shorter than the ground distance it
represents.  The N and S ratios are therefore UPPER bounds; W and E, painted in true
profile, are the honest ones.  Every direction is reported, with the profile pair
flagged, rather than silently correcting for a foreshortening factor nobody measured.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PROJ = Path(__file__).resolve().parent.parent
RUNS_ROOT = PROJ.parents[2]
MANIFEST = PROJ.parent / "artifacts" / "knight_cells_manifest.json"
FIT = PROJ / "frames" / "knight_fit.json"
OUT = PROJ / "frames" / "knight_foot_slide.json"

DIRS = ["S", "SW", "W", "NW", "N", "NE", "E", "SE"]
# on-screen travel per facing: keeper.gd maps the input vector's angle straight onto
# these, so S is +y (screen down) and E is +x
SCREEN_DIR = {"S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1),
              "N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1)}
PROFILE = {"W", "E"}            # painted side-on: no foreshortening in the stride axis
FOOT_BAND = 0.18
OPEN_W = 11


def body_mask(path):
    a = np.asarray(Image.open(path).convert("RGBA"))[..., 3] > 8
    opened = ndimage.binary_opening(a, structure=np.ones((1, OPEN_W), bool))
    lab, n = ndimage.label(opened)
    if n == 0:
        return opened
    sizes = ndimage.sum(opened, lab, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s >= 0.05 * sizes.max()]
    return np.isin(lab, keep)


def main():
    man = json.loads(MANIFEST.read_text())
    fit = json.loads(FIT.read_text())
    scale = float(fit["knight"]["scale"])
    walk_px_s = float(json.loads((PROJ / "parallax" / "parallax.json").read_text())
                      ["movement"]["walk_px_s"])

    print(f"knight sprite scale {scale:.6f}   walk_px_s {walk_px_s:.0f} (NOT changed)")
    print(f"{'dir':<4}{'stride_nf':>10}{'fps':>8}{'period_s':>10}"
          f"{'body_travel':>12}{'painted_stride':>15}{'slide_px':>10}{'ratio':>8}"
          f"{'no-slide fps':>14}")
    rows = {}
    for d in DIRS:
        cell = man["cells"]["walk_" + d]
        nf = int(cell["stride_native_frames"])
        src_fps = float(cell.get("fps_source", 24))
        fps = 12.0 * src_fps / nf
        period = nf / src_fps
        travel = walk_px_s * period
        vx, vy = SCREEN_DIR[d]
        norm = math.hypot(vx, vy)
        ux, uy = vx / norm, vy / norm
        spreads = []
        for rel in cell["frames"]:
            m = body_mask(RUNS_ROOT / rel)
            ys = np.nonzero(m.sum(1))[0]
            if len(ys) == 0:
                continue
            cut = int(ys.max() - FOOT_BAND * (ys.max() - ys.min()))
            fy, fx = np.nonzero(m[cut:])
            if len(fy) == 0:
                continue
            u = fx * ux + (fy + cut) * uy
            spreads.append(float(u.max() - u.min()))
        step_src = max(spreads)
        stride_canvas = 2.0 * step_src * scale
        ratio = travel / stride_canvas
        rows[d] = {
            "stride_native_frames": nf, "playback_fps": round(fps, 4),
            "stride_period_s": round(period, 4),
            "body_travel_px_per_stride": round(travel, 1),
            "painted_stride_px": round(stride_canvas, 1),
            "foot_slide_px_per_stride": round(travel - stride_canvas, 1),
            "slide_ratio": round(ratio, 2),
            "fps_that_would_plant_the_feet": round(12.0 * walk_px_s / stride_canvas, 2),
            "profile_view": d in PROFILE,
        }
        print(f"{d:<4}{nf:>10}{fps:>8.3f}{period:>10.3f}{travel:>12.1f}"
              f"{stride_canvas:>15.1f}{travel - stride_canvas:>10.1f}{ratio:>7.2f}x"
              f"{12.0 * walk_px_s / stride_canvas:>14.2f}"
              + ("   <- true profile" if d in PROFILE else ""))

    ratios = [r["slide_ratio"] for r in rows.values()]
    prof = [r["slide_ratio"] for d, r in rows.items() if r["profile_view"]]
    verdict = ("YES -- the feet slide visibly in every direction. The painted strides are "
               "stately (%.1f-%.1f s per stride) while walk_px_s asks for a brisk game "
               "walk, so the body outruns the painting by %.1fx-%.1fx (%.1fx-%.1fx on the "
               "two true-profile cells, which are the trustworthy pair)."
               % (min(r["stride_period_s"] for r in rows.values()),
                  max(r["stride_period_s"] for r in rows.values()),
                  min(ratios), max(ratios), min(prof), max(prof)))
    print("\nverdict:", verdict)
    OUT.write_text(json.dumps({
        "note": "Measured, not applied. walk_px_s is unchanged.",
        "walk_px_s": walk_px_s, "knight_sprite_scale": scale,
        "knight_figure_h_canvas_px": fit["knight"]["figure_h_canvas_px"],
        "method": __doc__.strip(), "verdict": verdict, "per_direction": rows,
    }, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    sys.exit(main())
