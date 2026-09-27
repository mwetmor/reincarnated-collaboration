#!/usr/bin/env python3
"""C-9 scene v3: the ANGEL and the DEMON as static south-facing stills for style B.

Matt's call: STILLS, no animation.  They stand at the bridge's west landing on either
side of the path, y-sorted with the knight so he passes in front of or behind them, and
each carries a small ellipse of collision at its feet so he walks AROUND them rather
than through them.  Hidden -- and un-collided -- in style A.

Reads (READ-ONLY, conductor-owned):
    runs/C-9/artifacts/AL-2-south/AL-2-south_a.png    flat #00ff00 plate
    runs/C-9/artifacts/DM-2-south/DM-2-south_a.png    flat #00ff00 plate

Writes, inside this project:
    sprites_figures/angel.png, demon.png       keyed + unmixed, cropped
    frames/figures_b.json                      every measurement behind the placement

KEY -> UNMIX.  Same operation as the parallax layers, and for the same reason: these
plates are not pure #00ff00 either, and a threshold leaves the painted antialiased edge
carrying the backing's green.  tools/build_b_assets.py owns the implementation; this
imports it rather than keeping a second copy that can drift from the first.

SIZE.  The brief sets the angel at the knight's figure height x1.0 and the demon at
x1.15.  "Figure height" for these two cannot be the silhouette's bounding box: the
angel's WINGS are the tallest thing in his picture and the brief says in so many words
that they extend ABOVE his height.  So it is measured crown-to-sole over the CENTRAL
40% of the silhouette's width -- which is the head, the halo and the body, and not the
wings, which are lateral.  The measured crown row and the bbox top are both recorded so
the difference is visible rather than asserted.

PLACEMENT.  World positions are the node's own origin = the figure's FEET, so the
sprite offset is -(pivot) exactly as the Keeper's and the knight's are, and y-sorting
under Actors/ (y_sort_enabled) sorts on the feet.  Both spots are checked against
parallax/walkable.json before they are written: a figure standing in blocked ground
would look placed and be unreachable.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_b_assets import green_unmix, to_img          # noqa: E402  (same unmix, one copy)

PROJ = Path(__file__).resolve().parent.parent
ART = PROJ.parent / "artifacts"
OUT_SPR = PROJ / "sprites_figures"
OUT_JSON = PROJ / "frames" / "figures_b.json"
FIT_JSON = PROJ / "frames" / "knight_fit.json"
WALKABLE = PROJ / "parallax" / "walkable.json"

CENTRAL_FRACTION = 0.40      # width band the crown is measured in (excludes wings)
SOLE_MIN_RUN_FRAC = 0.04     # a foot is wide relative to the figure; a wingtip is not

FIGURES = [
    # name,   source,                               height x knight,  world feet pos
    ("angel", "AL-2-south/AL-2-south_a.png", 1.00, (2585.0, 1440.0)),
    ("demon", "DM-2-south/DM-2-south_a.png", 1.15, (2880.0, 1420.0)),
]


def widest_run(row):
    xs = np.nonzero(row)[0]
    if len(xs) == 0:
        return 0
    best = s = p = xs[0]
    best = 1
    for x in xs[1:]:
        if x > p + 2:
            best = max(best, p - s + 1)
            s = x
        p = x
    return max(best, p - s + 1)


def measure(alpha):
    """-> dict with crown/sole/figure height, measured the way the docstring says."""
    m = alpha > 0.5
    ys, xs = np.nonzero(m)
    x0, x1 = int(xs.min()), int(xs.max())
    bbox_top = int(ys.min())
    w = x1 - x0 + 1
    half = CENTRAL_FRACTION * 0.5
    cx0, cx1 = int(x0 + w * (0.5 - half)), int(x0 + w * (0.5 + half))
    band = m[:, cx0:cx1 + 1]
    crown = int(np.nonzero(band.any(1))[0].min())
    min_run = max(6, int(SOLE_MIN_RUN_FRAC * w))
    runs = np.array([widest_run(m[y]) for y in range(m.shape[0])])
    sole = int(np.nonzero(runs >= min_run)[0].max())
    foot = m[max(sole - 6, 0):sole + 1]
    foot_cx = float(np.nonzero(foot)[1].mean()) if foot.any() else (x0 + x1) / 2.0
    return {"bbox": [x0, bbox_top, x1, int(ys.max())], "crown_row": crown,
            "sole_row": sole, "figure_h_px": sole - crown + 1,
            "bbox_top_row": bbox_top, "above_crown_px": crown - bbox_top,
            "feet_centre_x": foot_cx, "central_band_x": [cx0, cx1],
            "sole_min_run_px": min_run}


def walkable_ok(pt):
    w = json.loads(WALKABLE.read_text())
    def contains(poly, p):
        n, inside = len(poly), False
        for i in range(n):
            (xi, yi), (xj, yj) = poly[i], poly[(i + 1) % n]
            if (yi > p[1]) != (yj > p[1]):
                if p[0] < (xj - xi) * (p[1] - yi) / (yj - yi + 1e-12) + xi:
                    inside = not inside
        return inside
    ok = any(contains(p, pt) for p in w["walkable"])
    bad = any(contains(b, pt) for b in w["blocked"])
    return ok and not bad


def ellipse_points(rx, ry, n=32):
    return [(rx * np.cos(t), ry * np.sin(t)) for t in np.linspace(0, 2 * np.pi, n, endpoint=False)]


def main():
    fit = json.loads(FIT_JSON.read_text())
    knight_canvas_h = fit["knight"]["figure_h_canvas_px"]
    OUT_SPR.mkdir(exist_ok=True)
    out = {"note": "C-9 v3 static B-only figures. Written by tools/build_figures_b.py.",
           "knight_figure_h_canvas_px": knight_canvas_h, "figures": {}}

    for name, rel, mult, pos in FIGURES:
        rgb = np.asarray(Image.open(ART / rel).convert("RGB")).astype(np.float32) / 255.0
        rgba, st = green_unmix(rgb)
        m = measure(rgba[..., 3])
        target = knight_canvas_h * mult
        scale = target / m["figure_h_px"]

        img = to_img(rgba)
        x0, y0, x1, y1 = m["bbox"]
        # Crop to the painted bbox, NOT to the sole: the angel's cross-staff is planted
        # and its point reaches below his feet, and cutting at the sole row amputates it.
        # The pivot is the sole either way, so the extra rows simply hang below the
        # ground line where they were painted.
        img = img.crop((x0, m["bbox_top_row"], x1 + 1, y1 + 1))
        img.save(OUT_SPR / f"{name}.png")

        # sprite offset: the node origin sits on the FEET, like the Keeper's and the
        # knight's, so y-sorting under Actors/ sorts on the ground contact point
        pivot = [m["feet_centre_x"] - x0, m["sole_row"] + 1 - m["bbox_top_row"]]
        below_sole = y1 - m["sole_row"]
        rx = max(8.0, 0.11 * m["figure_h_px"] * scale)
        ry = max(3.0, rx * 6.04 / 16.61)          # the Keeper's own feet-ellipse ratio

        ok = walkable_ok(pos)
        out["figures"][name] = {
            "source": rel, "unmix": st, "measure": m,
            "png": f"sprites_figures/{name}.png", "png_size": list(img.size),
            "height_multiplier": mult, "target_canvas_h": round(target, 2),
            "scale": round(scale, 9), "offset": [round(-pivot[0], 4), round(-pivot[1], 4)],
            "world_pos": list(pos), "walkable": ok,
            "collision_ellipse_rx_ry": [round(rx, 3), round(ry, 3)],
            "drawn_h_canvas_px": round(img.size[1] * scale, 2),
            "wings_above_head_canvas_px": round(m["above_crown_px"] * scale, 2),
            "painted_below_sole_px": int(below_sole),
            "painted_below_sole_canvas_px": round(below_sole * scale, 2),
        }
        print("%-6s %s -> %s  figure %d px (bbox top %d, crown %d: %d px of wing/halo above)"
              % (name, rgb.shape[1::-1], img.size, m["figure_h_px"],
                 m["bbox_top_row"], m["crown_row"], m["above_crown_px"]))
        print("       scale %.5f -> figure %.1f canvas px (knight %.1f x %.2f = %.1f)"
              % (scale, m["figure_h_px"] * scale, knight_canvas_h, mult, target))
        print("       drawn %.1f canvas px tall: %.1f above the head, %.1f below the feet"
              % (img.size[1] * scale, m["above_crown_px"] * scale, below_sole * scale))
        print("       feet at %s  walkable=%s   collision ellipse %.1f x %.1f"
              % (pos, ok, rx, ry))
        if not ok:
            print("       *** NOT ON WALKABLE GROUND -- fix FIGURES[] before shipping")

    OUT_JSON.write_text(json.dumps(out, indent=1))
    print("wrote", OUT_JSON)
    return 0


if __name__ == "__main__":
    sys.exit(main())
