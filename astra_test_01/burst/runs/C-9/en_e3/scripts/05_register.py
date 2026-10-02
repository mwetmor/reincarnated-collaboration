# Does the paint land where the render put it?
#
#   python3 scripts/05_register.py <painted.png> <layout name>
#
# NOT by segmenting the paint and comparing masks. The first version did that
# and reported IoU 0.44-0.54, which looks exactly like a registration failure
# and was not one: this creature is dark blue-grey, the lost plate is dark, and
# a luminance threshold keeps the pale belly and mane and drops the body. The
# instrument was measuring my own thresholding.
#
# Registration is an ALIGNMENT question, so it is measured as alignment: the
# painted ink outline is a strong image edge, and the render mask's boundary is
# where that edge belongs. Score an offset by the mean painted gradient along
# the shifted boundary and find the peak. Offset (0,0) winning IS registration,
# and it needs no threshold at all.
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAINT, NAME = sys.argv[1], sys.argv[2]
R = int(sys.argv[3]) if len(sys.argv) > 3 else 8
L = json.load(open(os.path.join(ROOT, "work", "layout_%s.json" % NAME)))
P = np.array(Image.open(PAINT).convert("RGB")).astype(np.float32)
lum = P @ np.array([0.2126, 0.7152, 0.0722], np.float32)
gy, gx = np.gradient(lum)
G = np.hypot(gx, gy)
print("registration of %s against layout %s (search +-%d px)"
      % (os.path.basename(PAINT), NAME, R))
out = {}
for d, c in L["cells"].items():
    x0, y0, w, h = c["rect"]
    A = np.array(Image.open(os.path.join(
        ROOT, "work", "_cells_%s" % NAME, "cell_%s.png" % d)).convert("RGBA"))[:, :, 3] > 8
    # boundary of the render mask
    b = np.zeros_like(A)
    b[1:-1, 1:-1] = A[1:-1, 1:-1] & ~(A[:-2, 1:-1] & A[2:, 1:-1] &
                                      A[1:-1, :-2] & A[1:-1, 2:])
    ys, xs = np.where(b)
    best = None
    grid = np.full((2 * R + 1, 2 * R + 1), np.nan)
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            Y, X = ys + y0 + dy, xs + x0 + dx
            ok = (Y >= 0) & (Y < G.shape[0]) & (X >= 0) & (X < G.shape[1])
            s = float(G[Y[ok], X[ok]].mean()) if ok.any() else 0.0
            grid[dy + R, dx + R] = s
            if best is None or s > best[0]:
                best = (s, dx, dy)
    s0 = grid[R, R]
    out[d] = dict(best_offset=[best[1], best[2]], peak=round(best[0], 2),
                  at_zero=round(float(s0), 2),
                  ratio=round(float(s0) / max(best[0], 1e-6), 4))
    print("   %-9s peak offset (%+d,%+d)  score %6.2f   at (0,0) %6.2f  "
          "ratio %.3f %s" % (d, best[1], best[2], best[0], s0, s0 / max(best[0], 1e-6),
                             "" if (best[1], best[2]) == (0, 0) else "<-- SHIFTED"))
mr = float(np.mean([v["ratio"] for v in out.values()]))
md = float(np.mean([abs(v["best_offset"][0]) + abs(v["best_offset"][1])
                    for v in out.values()]))
print("   MEAN at-zero/peak ratio %.3f over %d cells; mean |offset| %.2f px"
      % (mr, len(out), md))
out["_summary"] = dict(mean_ratio=round(mr, 4), mean_abs_offset_px=round(md, 3),
                       painted=os.path.basename(PAINT))
json.dump(out, open(os.path.join(ROOT, "work", "register_%s_%s.json"
                                 % (NAME, os.path.basename(PAINT).split(".")[0])),
                    "w"), indent=1)
