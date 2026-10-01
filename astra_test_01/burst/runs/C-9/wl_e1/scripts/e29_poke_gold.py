# (a)'s own measure, in the BEAUTY pass (the ID pass cannot judge it: the under-layer is itself a garment): GILT/BRIGHT PLATE
# pixels (LCh hue 35-95, C* > 22, or L* > 45 and not cloth) in the lower 55% of the figure that have CAPE-cloth pixels (hue
# 250-340, C* > 7) within 8 px on BOTH sides -- leg plate seen between / through the cape -- as a share of the cloth pixels in
# that band. Per stack and clip: mean, max over keys x headings.   python3 e29_poke_gold.py <dir> [--json f]
import sys, glob, json, re, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
def lab(rgb):
    c = rgb / 255.0; c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]); X = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(X > 0.008856, np.cbrt(X), 7.787 * X + 16 / 116); return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
d = sys.argv[1]; res = {}
for f in sorted(glob.glob(d + '/stack*_beauty.png')):
    mm = re.search(r'stack(\d+)_(\w+)@([\d.]+)_h(\d+)_s2_beauty', f)
    if not mm or mm.group(1) == '0': continue
    a = np.asarray(Image.open(f).convert('RGB')).astype(float); idm = np.asarray(Image.open(f.replace('beauty', 'id')).convert('RGB')).astype(int)
    fig = idm.sum(2) > 30; Lb = lab(a); C = np.hypot(Lb[..., 1], Lb[..., 2]); h = np.degrees(np.arctan2(Lb[..., 2], Lb[..., 1])) % 360
    cloth = fig & (h > 250) & (h < 340) & (C > 7); gold = fig & ~cloth & (((h > 35) & (h < 95) & (C > 22)) | (Lb[..., 0] > 45))
    ys = np.where(fig.any(1))[0]; y0 = int(ys.min() + 0.45 * (ys.max() - ys.min())); band = np.zeros_like(fig); band[y0:] = True
    k = np.ones((1, 17), bool); kl = k.copy(); kl[:, 9:] = False; kr = k.copy(); kr[:, :8] = False
    enc = gold & band & ndimage.binary_dilation(cloth, kr) & ndimage.binary_dilation(cloth, kl)
    res.setdefault(mm.group(1), {}).setdefault(mm.group(2), []).append(float(enc.sum()) / max(int((cloth & band).sum()), 1))
out = {s: {c: dict(mean=round(float(np.mean(v)), 4), max=round(float(np.max(v)), 4), n=len(v)) for c, v in cl.items()} for s, cl in res.items()}
print(json.dumps(out))
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
