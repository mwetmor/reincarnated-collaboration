# EYE SLIT AS SEEN (Godot beauty stills, game camera): glow pixels = where the glow stack differs from the plain-helm stack
# (|dRGB| sum > 40), per heading at 1x and 2x; their count, bounding box (px), and contrast against the VISOR ring around them
# (pixels within 4 px of the glow, not glow): L* difference and Weber luminance contrast (Lglow - Lvisor) / Lvisor.
#   python3 e39_eye_measure.py <stills dir> <glow stack> <plain stack> <clip> [--json f]
import sys, glob, json, numpy as np
from PIL import Image
from scipy import ndimage
d, sg, sp, clip = sys.argv[1:5]
def L(rgb):
    c = rgb / 255.0; c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4); Y = c @ np.array([0.2126, 0.7152, 0.0722])
    return Y, np.where(Y > 0.008856, 116 * np.cbrt(Y) - 16, 903.3 * Y)
out = {}
for f in sorted((glob.glob('%s/stack%s_%s@*_beauty.png' % (d, sg, clip)) or glob.glob('%s/stack%s_%s_h*_beauty.png' % (d, sg, clip)))):
    p = f.replace('stack%s_' % sg, 'stack%s_' % sp); a = np.asarray(Image.open(f).convert('RGB')).astype(float); b = np.asarray(Image.open(p).convert('RGB')).astype(float)
    m = np.abs(a - b).sum(2) > 40; m = ndimage.binary_opening(m, np.ones((1, 1)))
    key = f.split('_h')[-1].split('_beauty')[0]
    if m.sum() == 0: out[key] = dict(px=0); continue
    ys, xs = np.nonzero(m); ring = ndimage.binary_dilation(m, np.ones((9, 9))) & ~m
    Yg, Lg = L(a[m]); Yv, Lv = L(a[ring])
    out[key] = dict(px=int(m.sum()), bbox_wh=[int(np.ptp(xs) + 1), int(np.ptp(ys) + 1)], L_glow=round(float(np.median(Lg)), 1), L_visor=round(float(np.median(Lv)), 1),
                    dL=round(float(np.median(Lg) - np.median(Lv)), 1), weber=round(float((np.median(Yg) - np.median(Yv)) / max(np.median(Yv), 1e-4)), 2))
for k, v in out.items(): print(k, v)
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
