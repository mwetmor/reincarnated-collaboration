# Cape poke-through AS SEEN, at the play camera (Godot ID pass, 2x): BODY pixels (red) in the lower 55% of the figure that have
# GARMENT pixels (blue) within 8 px on BOTH sides in the row -- body showing through / between cape panels -- as a share of
# the garment pixels in that band. Per stack, per clip (walk, run), the mean and max over keys x back-ish headings.
#   python3 e28_poke_pixels.py <dir> [--json f]
import sys, glob, json, re, numpy as np
from PIL import Image
from scipy import ndimage
d = sys.argv[1]; res = {}
for f in sorted(glob.glob(d + '/stack*_id.png')):
    mm = re.search(r'stack(\d+)_(\w+)@([\d.]+)_h(\d+)_s2_id', f)
    if not mm: continue
    a = np.asarray(Image.open(f).convert('RGB')).astype(int)
    red = (a[..., 0] > 128) & (a[..., 1] < 80) & (a[..., 2] < 80); blue = (a[..., 2] > 128) & (a[..., 0] < 80)
    fig = red | blue | ((a[..., 1] > 128) & (a[..., 0] < 80))
    ys = np.where(fig.any(1))[0]; y0 = int(ys.min() + 0.45 * (ys.max() - ys.min()))
    band = np.zeros_like(red); band[y0:ys.max() + 1] = True
    k = np.ones((1, 17), bool); kl = k.copy(); kl[:, 9:] = False; kr = k.copy(); kr[:, :8] = False
    left = ndimage.binary_dilation(blue, kr); right = ndimage.binary_dilation(blue, kl)
    enc = red & left & right & band
    share = float(enc.sum()) / max(int((blue & band).sum()), 1)
    res.setdefault(mm.group(1), {}).setdefault(mm.group(2), []).append(share)
out = {s: {c: dict(mean=round(float(np.mean(v)), 4), max=round(float(np.max(v)), 4), n=len(v)) for c, v in cl.items()} for s, cl in res.items()}
print(json.dumps(out, indent=1))
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
