# R-C9-98: sole-line registration by the SHOES themselves (kept unchanged by every brief). The feet contrast band of
# 02/07 is polluted once greaves and wraps change, and the base's gradient plate defeats the ink-row instrument.
# Shoe mask = brown-leather colour (hue 5-35 deg, sat 0.25-0.75, value 0.25-0.75) in the bottom 0.78-1.0 of each cell,
# largest components only. Reports per cell: sole row (99th percentile of mask rows), centroid (x, y) vs the base.
# Also the CROWN row: the topmost non-plate row in the top 0.25 of the cell (plate = smooth: low local contrast).
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
ART = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/'
def hsv(p):
    a = np.asarray(Image.open(p).convert('RGB').resize((1024, 1536))).astype(np.float32) / 255
    mx, mn = a.max(2), a.min(2); d = mx - mn + 1e-6
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, (g - b) / d % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, d / (mx + 1e-6), mx, a.mean(2)
def cell_stats(p):
    h, s, v, L = hsv(p); out = {}
    m1 = ndimage.uniform_filter(L, 5); ct = np.sqrt(np.maximum(ndimage.uniform_filter(L * L, 5) - m1 * m1, 0))
    for i, name in enumerate(('FRONT', 'RIGHT', 'BACK', 'LEFT')):
        cy, cx = divmod(i, 2); y0, x0 = cy * 768, cx * 512
        sl = (slice(y0 + int(0.78 * 768), y0 + 768), slice(x0, x0 + 512))
        m = (h[sl] > 5) & (h[sl] < 35) & (s[sl] > 0.25) & (s[sl] < 0.75) & (v[sl] > 0.25) & (v[sl] < 0.75) & (ct[sl] > 0.02)
        m = ndimage.binary_opening(m, iterations=1)
        lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
        keep = np.isin(lab, [j + 1 for j, z in enumerate(sz) if z > 400])
        ys, xs = np.nonzero(keep)
        tsl = (slice(y0, y0 + int(0.25 * 768)), slice(x0, x0 + 512))
        crown = np.where((ct[tsl] > 0.06).sum(1) > 4)[0]
        out[name] = dict(sole=float(np.percentile(ys, 99.5)) + int(0.78 * 768) if len(ys) else None,
                         cx=float(xs.mean()) if len(xs) else None, cy=float(ys.mean()) + int(0.78 * 768) if len(ys) else None,
                         n=int(keep.sum()), crown=int(crown.min()) if len(crown) else None)
    return out
base = sys.argv[1]; B = cell_stats(ART + base); res = {'base': B}
print('base', {k: (round(v['sole'], 1), round(v['cx'], 1), v['crown']) for k, v in B.items()})
for p in sys.argv[2:]:
    S = cell_stats(ART + p); res[p] = S
    print(p)
    for k in S:
        b, s = B[k], S[k]
        print('   %-5s sole_dy %+6.1f  shoe centroid dx %+6.1f dy %+6.1f  (px %d vs %d)  crown_dy %+d' % (
            k, s['sole'] - b['sole'], s['cx'] - b['cx'], s['cy'] - b['cy'], s['n'], b['n'], (s['crown'] or 0) - (b['crown'] or 0)))
json.dump(res, open('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/shoe_register_' + base.split('/')[0] + '.json', 'w'), indent=1)
