# EYE SPRITES AS SEEN: the sprite render (stack 3 = plain helm + sprites) against the plain render without sprites (look_j/eyes_halo
# stack 3): changed pixels -> blobs; per heading and scale: each of the two largest blobs' px, and dL* against the 9x9 ring.
#   python3 e45_sprite_measure.py <sprite dir> <plain dir> [--json f]
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
def Lst(rgb):
    c = rgb / 255.0; c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4); Y = c @ np.array([0.2126, 0.7152, 0.0722])
    return np.where(Y > 0.008856, 116 * np.cbrt(Y) - 16, 903.3 * Y)
A, B = sys.argv[1], sys.argv[2]; out = {}
for sc in (1, 2):
    for h in range(0, 360, 45):
        a = np.asarray(Image.open('%s/stack3_idle_h%d_s%d_beauty.png' % (A, h, sc)).convert('RGB')).astype(float)
        b = np.asarray(Image.open('%s/stack3_idle_h%d_s%d_beauty.png' % (B, h, sc)).convert('RGB')).astype(float)
        m = np.abs(a - b).sum(2) > 40; k = 'h%d_s%d' % (h, sc)
        if not m.any(): out[k] = dict(eyes_px=[0, 0]); continue
        lab, n = ndimage.label(m, np.ones((3, 3))); sz = sorted([int(x) for x in ndimage.sum(m, lab, range(1, n + 1))])
        ring = ndimage.binary_dilation(m, np.ones((9, 9))) & ~m
        out[k] = dict(eyes_px=(sz[-2:] if len(sz) > 1 else [0] + sz), blobs=n, dL=round(float(np.median(Lst(a[m])) - np.median(Lst(a[ring]))), 1), L_glow=round(float(np.median(Lst(a[m]))), 1))
for k, v in out.items(): print(k, v)
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
