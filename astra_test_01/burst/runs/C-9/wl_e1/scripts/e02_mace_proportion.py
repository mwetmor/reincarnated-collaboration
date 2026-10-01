# Weapon proportion check ON THE SHEET (the D5 sword lesson): head length vs whole, haft below the head in head-lengths,
# haft thickness vs head width. Mask = matte alpha if given, else a luminance threshold over the dark plate.
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
src = sys.argv[1]; alpha = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else None
im = np.asarray(Image.open(src).convert('RGB')).astype(int)
m = (np.asarray(Image.open(alpha).convert('RGBA'))[..., 3] > 128) if alpha else (im.mean(2) > 95)
m = ndimage.binary_closing(ndimage.binary_opening(m, np.ones((3, 3))), np.ones((5, 5)))
W = im.shape[1]; out = []
for k, (x0, x1) in enumerate([(0, W // 3), (W // 3, 2 * W // 3), (2 * W // 3, W)]):
    s = m[:, x0:x1]; lab, n = ndimage.label(s); sz = ndimage.sum(s, lab, range(1, n + 1)); s = lab == 1 + int(np.argmax(sz))
    rows = np.where(s.any(1))[0]; top, bot = int(rows.min()), int(rows.max())
    width = np.array([np.ptp(np.where(s[r])[0]) + 1 if s[r].any() else 0 for r in range(s.shape[0])])
    L = bot - top + 1
    hw = float(np.median(width[top + int(0.55 * L):top + int(0.70 * L)]))
    # the head ends at the last row in the top half wider than 1.6x the haft (collar included)
    wide = [r for r in range(top, top + L // 2) if width[r] > 1.6 * hw]
    hb = max(wide); H = hb - top + 1; headw = int(width[top:hb + 1].max())
    rec = dict(view=k, length_px=L, head_px=H, head_frac=round(H / L, 3), haft_below_head_in_heads=round((bot - hb) / H, 2),
               haft_px=hw, head_w_px=headw, haft_over_headw=round(hw / headw, 3))
    out.append(rec); print(rec)
v = out[1]
verdict = dict(head_le_third=all(o['head_frac'] <= 0.34 for o in out), haft_ge_2p5=all(o['haft_below_head_in_heads'] >= 2.5 for o in out),
               haft_thin=all(o['haft_over_headw'] <= 0.2 for o in out))
print(verdict)
json.dump(dict(src=src, views=out, verdict=verdict), open(sys.argv[3] if len(sys.argv) > 3 else '/dev/stdout', 'w'), indent=1)
