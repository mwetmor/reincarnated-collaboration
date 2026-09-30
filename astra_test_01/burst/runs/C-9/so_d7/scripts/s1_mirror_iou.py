# Pick the base-body sheet by MIRROR IoU (G1-S rule; on a tie take b).
#
#   python3 scripts/s1_mirror_iou.py <a.png> <b.png>
#
# A turnaround's front and back are left-right mirrors in silhouette, and so are
# its two sides. The better the agreement, the less the 3D generator has to
# reconcile -- and disagreement is the usual source of a lumpy back or an arm
# that is two different lengths depending on the view.
#
# Each pair is aligned before scoring: both masks are cropped to their own bbox
# and scaled to a common height, feet on the same line. Raw IoU on the cells
# would score where the artist happened to put the figure, not the figure.
import json, sys
import numpy as np
from PIL import Image


def mask(im):
    a = np.asarray(im.convert('RGB')).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # chroma green: strong G, weak R and B. Everything else is figure.
    return ~((g > 150) & (r < 120) & (b < 120))


def cells(path):
    im = Image.open(path)
    W, H = im.size
    cw, ch = W // 2, H // 2
    c = {}
    for nm, (i, j) in dict(front=(0, 0), right=(1, 0), back=(0, 1), left=(1, 1)).items():
        c[nm] = mask(im.crop((i * cw, j * ch, (i + 1) * cw, (j + 1) * ch)))
    return c


def norm(m, H=600, W=400):
    ys, xs = np.nonzero(m)
    crop = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = crop.shape
    s = H / h
    nw = max(1, int(round(w * s)))
    im = Image.fromarray((crop * 255).astype(np.uint8)).resize((nw, H), Image.NEAREST)
    out = np.zeros((H, W), bool)
    x0 = (W - nw) // 2
    a = np.asarray(im) > 127
    xs0, xs1 = max(0, x0), min(W, x0 + nw)
    out[:, xs0:xs1] = a[:, xs0 - x0:xs1 - x0]
    return out


def iou(a, b):
    return float((a & b).sum()) / float((a | b).sum())


res = {}
for tag, p in zip(("a", "b"), sys.argv[1:3]):
    c = cells(p)
    fb = iou(norm(c["front"]), norm(c["back"])[:, ::-1])
    rl = iou(norm(c["right"]), norm(c["left"])[:, ::-1])
    res[tag] = dict(front_back=round(fb, 4), right_left=round(rl, 4),
                    mean=round((fb + rl) / 2, 4))
    print("  %s  front/back %.4f   right/left %.4f   mean %.4f" % (tag, fb, rl, (fb + rl) / 2))
d = res["a"]["mean"] - res["b"]["mean"]
TIE = 0.01
pick = "b" if abs(d) <= TIE else ("a" if d > 0 else "b")
why = ("tie within %.2f -> b by the G1-S rule (athletic build)" % TIE if abs(d) <= TIE
       else "higher mean mirror IoU")
print("  PICK: %s  (%s; a-b = %+.4f)" % (pick, why, d))
json.dump(dict(scores=res, pick=pick, why=why, tie_tolerance=TIE),
          open("work/s1_pick.json", "w"), indent=1)
