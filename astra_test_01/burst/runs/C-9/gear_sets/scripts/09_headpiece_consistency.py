# R-C9-98 stage 1b: is the sorceress's new headpiece the SAME object in all four views?
# Per cell (head region = top 0.19 of the cell: above the breastplate runes): the ember-red ENAMEL/CLOTH mask (hue <16 or >335 deg, sat > 0.45, value > 0.35)
# -> its top row (wing tips / hood crown), bottom row, height, x-span (width across the head); and the figure's topmost
# ink row (local contrast > 0.06) = the top of the headpiece. Side views see the wings edge-on-ish, so width is compared
# FRONT vs BACK and RIGHT vs LEFT; heights compare across all four. Spread = max - min over the four views.
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
ART = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/'
def run(p):
    a = np.asarray(Image.open(ART + p).convert('RGB')).astype(np.float32) / 255
    mx, mn = a.max(2), a.min(2); d = mx - mn + 1e-6; r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, (g - b) / d % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = d / (mx + 1e-6); L = a.mean(2)
    m1 = ndimage.uniform_filter(L, 5); ct = np.sqrt(np.maximum(ndimage.uniform_filter(L * L, 5) - m1 * m1, 0))
    red = ((h < 16) | (h > 335)) & (s > 0.45) & (mx > 0.35) & (ct > 0.02)
    out = {}
    for i, name in enumerate(('FRONT', 'RIGHT', 'BACK', 'LEFT')):
        cy, cx = divmod(i, 2); y0, x0 = cy * 768, cx * 512
        sl = (slice(y0, y0 + int(0.19 * 768)), slice(x0, x0 + 512))
        m = ndimage.binary_opening(red[sl], iterations=1)
        lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
        keep = np.isin(lab, [j + 1 for j, z in enumerate(sz) if z > 25])
        ys, xs = np.nonzero(keep)
        top = np.where((ct[sl] > 0.06).sum(1) > 3)[0]
        out[name] = dict(red_top=int(ys.min()) if len(ys) else None, red_bot=int(ys.max()) if len(ys) else None,
                         red_h=int(ys.max() - ys.min()) if len(ys) else None, red_w=int(xs.max() - xs.min()) if len(xs) else None,
                         red_px=int(keep.sum()), fig_top=int(top.min()) if len(top) else None)
    for k, v in out.items():
        v['tip_above_crown'] = (CROWN[k] - v['red_top']) if v['red_top'] is not None else None
    keys = ('tip_above_crown', 'red_h')
    spread = {k: (max(v[k] for v in out.values() if v[k] is not None) - min(v[k] for v in out.values() if v[k] is not None)) for k in keys}
    spread['w_front_vs_back'] = abs((out['FRONT']['red_w'] or 0) - (out['BACK']['red_w'] or 0))
    spread['w_right_vs_left'] = abs((out['RIGHT']['red_w'] or 0) - (out['LEFT']['red_w'] or 0))
    return out, spread
# the base crown per view (SO-1_b, green plate: exact), so wing tips are read as px ABOVE HER OWN CROWN in that view
_b = np.asarray(Image.open(ART + 'CS9-guides/SO-1_b_harvest.png').convert('RGB')).astype(int)
_fg = ~((_b[..., 1] > 180) & (_b[..., 0] < 120) & (_b[..., 2] < 120))
CROWN = {n: int(np.where(_fg[(i // 2) * 768:(i // 2) * 768 + 200, (i % 2) * 512:(i % 2) * 512 + 512].any(1))[0].min())
         for i, n in enumerate(('FRONT', 'RIGHT', 'BACK', 'LEFT'))}
print('base crown row per view', CROWN)
res = {'base_crown': CROWN}
for p in sys.argv[1:]:
    o, sp = run(p); res[p] = dict(views=o, spread=sp)
    print(p); [print('   %-5s %s' % (k, v)) for k, v in o.items()]; print('   SPREAD', sp)
json.dump(res, open('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_battlemage/headpiece_consistency.json', 'w'), indent=1)
