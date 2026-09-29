#!/usr/bin/env python3
"""C-9 T9-1b: cut the albedo-repaint canvases out of plate_v4.png.

The repaint has to come back and sit on the plate PIXEL FOR PIXEL, so every choice here
is made to keep registration recoverable:

  * NATIVE RESOLUTION, NO RESAMPLING. Each canvas is an exact 1536x1024 crop of the plate.
    1536x1024 is not a ceiling I happened to hit -- it is the size the image model returns.
    A canvas of any other size comes back rescaled to one of the model's own sizes, and
    then "restore the alpha to the pixel" is already impossible before reassembly starts.
  * CLEAR GOES GREEN. Under alpha==0 the plate's RGB is undefined -- near-black garbage
    the painter never saw (mean RGB 5.9,5.7,1.6 over the bridge view). Handing that to a
    painter asks them to repaint noise; flat #00ff00 says "nothing here" in the same
    language the rest of this run uses.
  * ALPHA TRAVELS SEPARATELY and is restored from the original plate, never from the
    return. 39.75% of this plate is transparent and the backdrop occludes the sky the
    moment that channel drifts.
  * THREE TILES, NOT FOUR. A 2x2 grid over the bridge view + margin puts 92% green in the
    top-left canvas -- an Astra call spent on the void. The top tile is slid left to
    x3120 instead, which both swallows the plateau lip the 2x2 grid split and leaves the
    void uncovered, because the void has nothing to repaint. Verified: 0 painted pixels
    of the measured frame, and 0 of frame+200, fall outside these three rects.

Writes canvases, per-tile alpha masks, per-tile layout JSON and one grid JSON.
"""
import json
import pathlib
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

HERE = pathlib.Path(__file__).resolve().parent.parent
PLATE = HERE / "godot" / "plate" / "plate_v4.png"
OUT = HERE / "t9_1b"

TW, TH = 1536, 1024
GREEN = (0, 255, 0)

# The measured frame (tools/shot_t9.gd aim (3459.88,1027.18) zoom 1.0) and its margin.
BRIDGE_VIEW = (2500, 487, 4420, 1567)
MARGIN = 200

TILES = {
    "top":       (3120, 103),
    "bot_left":  (2024, 927),
    "bot_right": (3360, 927),
}


def main() -> int:
    plate = np.asarray(Image.open(PLATE))
    H, W = plate.shape[:2]
    alpha = plate[..., 3]

    for d in ("canvas", "mask", "layout"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    # --- the coverage proof, run every time, because the layout is hand-placed ---------
    bx0, by0, bx1, by1 = BRIDGE_VIEW
    for label, rect in (("frame", BRIDGE_VIEW),
                        ("frame+%d" % MARGIN, (bx0 - MARGIN, by0 - MARGIN,
                                               bx1 + MARGIN, by1 + MARGIN))):
        x0, y0, x1, y1 = rect
        cov = np.zeros((y1 - y0, x1 - x0), bool)
        for tx, ty in TILES.values():
            ax0, ay0 = max(tx, x0), max(ty, y0)
            ax1, ay1 = min(tx + TW, x1), min(ty + TH, y1)
            if ax1 > ax0 and ay1 > ay0:
                cov[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0] = True
        missed = int(((alpha[y0:y1, x0:x1] > 0) & ~cov).sum())
        print("coverage %-12s painted px outside the canvases: %d" % (label, missed))
        if missed:
            print("HALT: the canvases do not cover the region", file=sys.stderr)
            return 2

    grid = {
        "plate": {"file": "godot/plate/plate_v4.png", "size": [W, H]},
        "bridge_view_px": {"x0": bx0, "y0": by0, "x1": bx1, "y1": by1,
                           "aim": [3459.88, 1027.18], "zoom": 1.0},
        "margin_px": MARGIN,
        "tile_size": [TW, TH],
        "clear_fill_rgb": list(GREEN),
        "mask_rule": "canvas RGB = plate RGB where alpha > 0, #00ff00 where alpha == 0",
        "tiles": {},
    }

    for tid, (x0, y0) in TILES.items():
        assert 0 <= x0 and x0 + TW <= W and 0 <= y0 and y0 + TH <= H, tid
        tile = plate[y0:y0 + TH, x0:x0 + TW]
        ta = tile[..., 3]
        rgb = tile[..., :3].copy()
        rgb[ta == 0] = GREEN

        cpath = OUT / "canvas" / ("t9_albedo_%s.png" % tid)
        mpath = OUT / "mask" / ("t9_albedo_%s_alpha.png" % tid)
        Image.fromarray(rgb, "RGB").save(cpath)
        Image.fromarray(ta, "L").save(mpath)

        overlaps = {}
        for oid, (ox, oy) in TILES.items():
            if oid == tid:
                continue
            ix0, iy0 = max(x0, ox), max(y0, oy)
            ix1, iy1 = min(x0 + TW, ox + TW), min(y0 + TH, oy + TH)
            if ix1 > ix0 and iy1 > iy0:
                overlaps[oid] = {"plate_rect": [ix0, iy0, ix1, iy1],
                                 "w": ix1 - ix0, "h": iy1 - iy0}

        lum = 0.2126 * tile[..., 0] + 0.7152 * tile[..., 1] + 0.0722 * tile[..., 2]
        painted = ta > 0
        rec = {
            "canvas": str(cpath.relative_to(HERE)),
            "alpha_mask": str(mpath.relative_to(HERE)),
            "plate_rect": [x0, y0, x0 + TW, y0 + TH],
            "size": [TW, TH],
            "overlaps": overlaps,
            "alpha": {"clear_pct": round(float((ta == 0).mean() * 100), 2),
                      "partial_pct": round(float(((ta > 0) & (ta < 255)).mean() * 100), 2),
                      "opaque_pct": round(float((ta == 255).mean() * 100), 2)},
            "painted_luma": {"mean": round(float(lum[painted].mean()), 2),
                             "near_black_pct": round(float((lum[painted] <= 32).mean() * 100), 2)},
        }
        grid["tiles"][tid] = rec
        (OUT / "layout" / ("t9_albedo_%s.json" % tid)).write_text(
            json.dumps(rec, indent=1) + "\n")
        print("%-9s -> %s  clear %5.2f%%  overlaps %s"
              % (tid, cpath.name, rec["alpha"]["clear_pct"],
                 {k: "%dx%d" % (v["w"], v["h"]) for k, v in overlaps.items()}))

    (OUT / "t9_albedo_grid.json").write_text(json.dumps(grid, indent=1) + "\n")
    print("grid -> %s" % (OUT / "t9_albedo_grid.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
