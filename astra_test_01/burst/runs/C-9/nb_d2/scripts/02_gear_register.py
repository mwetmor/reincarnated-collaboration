# D2 step 1: choose each gear variant by whether the UNCOVERED BODY MOVED.
#
#   python3 scripts/02_gear_register.py NB-G1 NB-G2 NB-G3
#
# Not by masking the body. A local-contrast mask of NB-1_b comes back as the
# figure PLUS a ring of the lost plate's warm halo, and the halo is different
# on every sheet -- so a "body unchanged" score taken over that mask would be
# scoring haloes. Eroding the ring away eats the arms.
#
# The defect these variants were retried for is a SHIFT of body landmarks, so
# shift is what gets measured, on a region no gear in any of these three sheets
# touches: the legs and boots, the bottom third of each view. The helmet and
# bracers are above it, the byrnie's hem stops at mid-thigh, the mantle is on
# the shoulders. Scored on high-contrast pixels only, so a plate gradient
# cannot vote.
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(os.path.dirname(ROOT), "artifacts")
BASE = np.array(Image.open(os.path.join(ART, "NB-1", "NB-1_b.png")
                           ).convert("L"), np.float32)
H, W = BASE.shape
R = 6
LO, HI = 0.62, 0.97            # legs and boots, of each cell's height


def cells(img):
    h, w = H // 2, W // 2
    for cy in range(2):
        for cx in range(2):
            c = img[cy * h:(cy + 1) * h, cx * w:(cx + 1) * w]
            yield (cy, cx), c[int(LO * h):int(HI * h)]


def contrast(a, k=5):
    m1 = ndimage.uniform_filter(a, k)
    sd = np.sqrt(np.maximum(ndimage.uniform_filter(a * a, k) - m1 * m1, 0))
    return sd


out = {}
for sheet in sys.argv[1:]:
    print("=== %s" % sheet)
    for v in ("a", "b"):
        p = os.path.join(ART, sheet, "%s_%s.png" % (sheet, v))
        if not os.path.exists(p):
            continue
        G = np.array(Image.open(p).convert("L"), np.float32)
        offs, res, nrm = [], [], []
        for (cy, cx), b in cells(BASE):
            g = list(cells(G))[cy * 2 + cx][1]
            sel = contrast(b) > np.percentile(contrast(b), 80)
            if sel.sum() < 500:
                continue
            best = None
            for dy in range(-R, R + 1):
                for dx in range(-R, R + 1):
                    gs = np.roll(np.roll(g, dy, 0), dx, 1)
                    d = float(np.abs(b[sel] - gs[sel]).mean())
                    if best is None or d < best[0]:
                        best = (d, dx, dy)
            z = float(np.abs(b[sel] - g[sel]).mean())
            offs.append((best[1], best[2])); res.append(z); nrm.append(best[0])
        mo = float(np.mean([abs(x) + abs(y) for x, y in offs]))
        print("   %s_%s  offsets %s  |offset| mean %.2f px   residual at zero "
              "%.2f (best %.2f)" % (sheet, v, offs, mo, float(np.mean(res)),
                                    float(np.mean(nrm))))
        out["%s_%s" % (sheet, v)] = dict(offsets=offs, mean_abs_offset=round(mo, 3),
                                         residual_at_zero=round(float(np.mean(res)), 3),
                                         residual_best=round(float(np.mean(nrm)), 3))
import json
json.dump(out, open(os.path.join(ROOT, "work", "gear_register.json"), "w"), indent=1)
