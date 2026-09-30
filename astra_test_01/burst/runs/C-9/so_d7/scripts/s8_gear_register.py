# Choose each D7 gear variant by whether the UNCOVERED BODY MOVED -- D2's rule,
# with the band chosen PER LAYER.
#
#   python3 scripts/s8_gear_register.py
#
# D2 scored every layer on the legs and boots (0.62-0.97 of each cell), because
# nothing the barbarian wore reached below the knee. This costume's robe falls
# to her ankles: scored on that band, the robe variant would be judged on the
# robe itself and "the body moved" would mean "the robe differs from bare legs".
# So each layer is scored only where THAT layer cannot be:
#   robe          the head (0.02-0.13) and the boot feet (0.88-0.97)
#   mantle, cb,   the legs and boots (0.62-0.97): the mantle is at the
#   belt          shoulders, the circlet at the brow, the bracers on the forearms
#                 (0.40-0.55 in this A-pose), the belt and pouches at the hips
# Lower mean |offset| wins; ties go to the lower residual.
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ART = os.path.join(os.path.dirname(ROOT), "artifacts")
BASE = np.array(Image.open(os.path.join(ART, "CS9-guides", "SO-1_b_harvest.png")).convert("L"), np.float32)
H, W = BASE.shape
R = 6
BANDS = {"SOG-robe": [(0.02, 0.13), (0.88, 0.97)], "SOG-mantle": [(0.62, 0.97)],
         "SOG-cb": [(0.62, 0.97)], "SOG-belt": [(0.62, 0.97)]}


def contrast(a, k=5):
    m1 = ndimage.uniform_filter(a, k)
    return np.sqrt(np.maximum(ndimage.uniform_filter(a * a, k) - m1 * m1, 0))


def bands(img, spans):
    h, w = H // 2, W // 2
    for cy in range(2):
        for cx in range(2):
            c = img[cy * h:(cy + 1) * h, cx * w:(cx + 1) * w]
            for lo, hi in spans:
                yield (cy, cx, lo), c[int(lo * h):int(hi * h)]


out, pick = {}, {}
for sheet, spans in BANDS.items():
    scores = {}
    for v in ("a", "b"):
        p = os.path.join(ART, sheet, "%s_%s.png" % (sheet, v))
        if not os.path.exists(p):
            continue
        G = np.array(Image.open(p).convert("L").resize((W, H)), np.float32)
        offs, res = [], []
        gb = dict(bands(G, spans))
        for key, b in bands(BASE, spans):
            g = gb[key]
            cb = contrast(b)
            sel = cb > np.percentile(cb, 80)
            if sel.sum() < 300:
                continue
            best = min(((float(np.abs(b[sel] - np.roll(np.roll(g, dy, 0), dx, 1)[sel]).mean()), dx, dy)
                        for dy in range(-R, R + 1) for dx in range(-R, R + 1)))
            offs.append((best[1], best[2])); res.append(best[0])
        mo = float(np.mean([abs(x) + abs(y) for x, y in offs])) if offs else 99.0
        scores[v] = dict(mean_abs_offset=round(mo, 3), residual=round(float(np.mean(res)), 3) if res else None,
                         bands=len(offs))
        print("  %-10s %s  |offset| %.2f px  residual %.2f  (%d band cells)"
              % (sheet, v, mo, scores[v]["residual"] or -1, len(offs)))
    if scores:
        pick[sheet] = min(scores, key=lambda k: (scores[k]["mean_abs_offset"], scores[k]["residual"] or 0))
        out[sheet] = dict(scored_on=spans, variants=scores, pick=pick[sheet])
print("PICK:", pick)
json.dump(out, open(os.path.join(ROOT, "work", "gear_register.json"), "w"), indent=1)
