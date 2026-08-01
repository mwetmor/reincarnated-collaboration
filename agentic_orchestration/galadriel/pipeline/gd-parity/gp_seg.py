#!/usr/bin/env python3
"""GD-PARITY — anchor-region character segmentation + bbox.

Instrument, not oracle. Segments the subject at a given screen anchor from its
local terrain by colour distance to a border-sampled background model, keeps the
connected component that contains the seed, and reports the bbox in SOURCE
pixels. Always writes a mask overlay so the read can be looked at before it is
believed (GAL-CAM `gc_look` precedent).

Green debug-text overlay (Matt's dev HUD) and red aggro lines are masked out by
hue before segmentation, so they cannot inflate the box.
"""
import argparse, json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--x0", type=int, required=True)
ap.add_argument("--y0", type=int, required=True)
ap.add_argument("--w", type=int, required=True)
ap.add_argument("--h", type=int, required=True)
ap.add_argument("--seedx", type=int, required=True)
ap.add_argument("--seedy", type=int, required=True)
ap.add_argument("--pct", type=float, default=72.0,
                help="percentile of colour distance kept as foreground")
ap.add_argument("--border", type=int, default=14)
ap.add_argument("--out", required=True)
ap.add_argument("--json", default=None)
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
A = np.asarray(im, dtype=np.float32)
roi = A[a.y0:a.y0 + a.h, a.x0:a.x0 + a.w]

# --- kill the dev-HUD overlay colours (bright green text, pure-red lines) ---
r, g, b = roi[..., 0], roi[..., 1], roi[..., 2]
hud = ((g > 110) & (g > r * 1.35) & (g > b * 1.35)) | ((r > 110) & (r > g * 1.9) & (r > b * 1.9))

# --- background model: the ROI border ring ---
bm = np.zeros(roi.shape[:2], bool)
bm[:a.border, :] = True; bm[-a.border:, :] = True
bm[:, :a.border] = True; bm[:, -a.border:] = True
bm &= ~hud
bg = np.median(roi[bm], axis=0)

d = np.linalg.norm(roi - bg[None, None, :], axis=2)
d[hud] = 0.0
thr = np.percentile(d, a.pct)
fg = d > thr

# --- 4-connected flood from the seed ---
sy, sx = a.seedy - a.y0, a.seedx - a.x0
if not fg[sy, sx]:
    # nudge to the nearest foreground pixel within 12 px
    best = None
    for dy in range(-12, 13):
        for dx in range(-12, 13):
            yy, xx = sy + dy, sx + dx
            if 0 <= yy < a.h and 0 <= xx < a.w and fg[yy, xx]:
                c = dy * dy + dx * dx
                if best is None or c < best[0]:
                    best = (c, yy, xx)
    if best:
        sy, sx = best[1], best[2]

lab = np.zeros(fg.shape, bool)
stack = [(sy, sx)]
lab[sy, sx] = True
H, W = fg.shape
while stack:
    y, x = stack.pop()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < H and 0 <= xx < W and fg[yy, xx] and not lab[yy, xx]:
            lab[yy, xx] = True
            stack.append((yy, xx))

ys, xs = np.nonzero(lab)
res = {
    "src": a.src, "roi": [a.x0, a.y0, a.w, a.h], "pct": a.pct,
    "n_px": int(lab.sum()),
    "top": int(a.y0 + ys.min()), "bottom": int(a.y0 + ys.max()),
    "left": int(a.x0 + xs.min()), "right": int(a.x0 + xs.max()),
}
res["h_px"] = res["bottom"] - res["top"] + 1
res["w_px"] = res["right"] - res["left"] + 1
res["h_frac"] = res["h_px"] / im.size[1]

vis = roi.copy()
vis[lab] = vis[lab] * 0.45 + np.array([255, 40, 200]) * 0.55
z = max(1, 900 // a.w)
Image.fromarray(vis.astype("uint8")).resize((a.w * z, a.h * z), Image.NEAREST).save(a.out)
print(json.dumps(res))
if a.json:
    json.dump(res, open(a.json, "w"), indent=1)
