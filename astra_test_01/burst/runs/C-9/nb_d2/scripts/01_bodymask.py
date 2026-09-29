# D2: a body mask for NB-1_b, so the gear sheets can be compared to it on the
# BODY rather than on their backgrounds.
#
#   python3 scripts/01_bodymask.py
#
# The sheets do not share a background: NB-1_b and G1/G2 lost their plate to
# the usual dark gradient with a warm halo, G3 kept its green. A raw pixel
# difference between two sheets is therefore mostly a difference of plates, and
# any "the body is unchanged" measure taken over the whole canvas would be
# measuring the halo.
#
# The figure is separated by LOCAL CONTRAST, not by colour: a painted body is
# full of high-frequency detail -- hair, mail, folds, laces -- and a lost plate
# is a smooth gradient whatever its hue. That holds for green and for brown.
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(os.path.dirname(ROOT), "artifacts")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ART, "NB-1", "NB-1_b.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "work", "bodymask.png")
a = np.array(Image.open(SRC).convert("L"), np.float32)
# local standard deviation over a small window
k = 5
m1 = ndimage.uniform_filter(a, k)
m2 = ndimage.uniform_filter(a * a, k)
sd = np.sqrt(np.maximum(m2 - m1 * m1, 0))
thr = np.percentile(sd, 62)
m = sd > thr
m = ndimage.binary_closing(m, np.ones((9, 9)))
m = ndimage.binary_fill_holes(m)
m = ndimage.binary_opening(m, np.ones((5, 5)))
# the sheet is a 2x2 of four views: keep the largest blob PER CELL, so one
# view's figure cannot be discarded for being smaller than another's
H, W = m.shape
out = np.zeros_like(m)
for cy in range(2):
    for cx in range(2):
        sub = m[cy * H // 2:(cy + 1) * H // 2, cx * W // 2:(cx + 1) * W // 2]
        lab, n = ndimage.label(sub)
        if n:
            sz = ndimage.sum(sub, lab, range(1, n + 1))
            sub = lab == (int(np.argmax(sz)) + 1)
        out[cy * H // 2:(cy + 1) * H // 2, cx * W // 2:(cx + 1) * W // 2] = sub
out = ndimage.binary_fill_holes(out)
print("%s: body mask covers %.2f%% of the sheet (sd threshold %.2f)"
      % (os.path.basename(SRC), 100 * out.mean(), thr))
for cy in range(2):
    for cx in range(2):
        sub = out[cy * H // 2:(cy + 1) * H // 2, cx * W // 2:(cx + 1) * W // 2]
        ys, xs = np.where(sub)
        print("   cell (%d,%d): %6d px, box x %3d..%3d y %3d..%3d"
              % (cy, cx, sub.sum(), xs.min(), xs.max(), ys.min(), ys.max()))
Image.fromarray((out * 255).astype(np.uint8)).save(OUT)
