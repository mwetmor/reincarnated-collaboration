# R-C9-98: did the uncovered body MOVE? (D2/D7 rule, s8_gear_register.py method: contrast-selected pixels, best integer shift)
# A full armour set covers nearly everything, so each set is scored only where no piece reaches:
#   feet  (0.90-0.985 of each cell: shoes / boot feet below the greaves)
#   face  (per-character band of each cell: the face under an open helm; side/back cells included as hair/ear)
# Search radius 32 px (the GS-BGL figures visibly sit lower). Also reports each cell's sole line and top line vs the base,
# so a SCALE change shows as a different top-to-sole height, not just an offset.
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
ART = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/'
OUT = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/'
SETS = {'GS-SBM': (ART + 'CS9-guides/SO-1_b_harvest.png', {'feet': (0.90, 0.985), 'face': (0.06, 0.13)}, 'sorceress_battlemage'),
        'GS-BGL': (ART + 'NB-1/NB-1_b.png', {'feet': (0.88, 0.95), 'face': (0.06, 0.14)}, 'barbarian_gladiator')}
R = 32


def contrast(a, k=5):
    m1 = ndimage.uniform_filter(a, k)
    return np.sqrt(np.maximum(ndimage.uniform_filter(a * a, k) - m1 * m1, 0))


def cells(img):
    H, W = img.shape; h, w = H // 2, W // 2
    for cy in range(2):
        for cx in range(2):
            yield ('FRONT', 'RIGHT', 'BACK', 'LEFT')[cy * 2 + cx], img[cy * h:(cy + 1) * h, cx * w:(cx + 1) * w]


def ink_rows(c):
    # rows holding the figure's dark outline ink (works on green, gradient or dark plates: local contrast, not colour)
    ct = contrast(c, 3)
    rows = np.where((ct > 18).sum(1) > 3)[0]
    return int(rows.min()), int(rows.max())


res = {}
for sheet, (basep, bands, folder) in SETS.items():
    B = np.array(Image.open(basep).convert('L'), np.float32)
    bc = dict(cells(B))
    res[sheet] = {}
    for v in 'ab':
        G = np.array(Image.open(ART + f'{sheet}/{sheet}_{v}.png').convert('L').resize(B.shape[::-1]), np.float32)
        gc = dict(cells(G)); rv = {}
        for name in bc:
            b, g = bc[name], gc[name]; h = b.shape[0]; rv[name] = {}
            for bn, (lo, hi) in bands.items():
                y0, y1 = int(lo * h), int(hi * h)
                bb = b[y0:y1]; cb = contrast(bb); sel = cb > np.percentile(cb, 85)
                def score(dx, dy):
                    if y0 + dy < 0 or y1 + dy > h:
                        return None
                    return float(np.abs(bb[sel] - np.roll(g[y0 + dy:y1 + dy], -dx, 1)[sel]).mean())
                cand = [(score(dx, dy), dx, dy) for dy in range(-R, R + 1, 2) for dx in range(-R, R + 1, 2)]
                s, dx, dy = min(c for c in cand if c[0] is not None)
                fine = [(score(dx + i, dy + j), dx + i, dy + j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
                s, dx, dy = min(c for c in fine if c[0] is not None)
                rv[name][bn] = dict(dx=dx, dy=dy, residual=round(s, 2))
            bt, bs = ink_rows(b); gt, gs = ink_rows(g)
            rv[name]['sole_dy'] = gs - bs
            rv[name]['top_dy'] = gt - bt
        offs = [abs(rv[c][bn]['dx']) + abs(rv[c][bn]['dy']) for c in rv for bn in bands]
        rv['mean_abs_offset_px'] = round(float(np.mean(offs)), 2)
        res[sheet][v] = rv
        print(sheet, v, 'mean |offset|', rv['mean_abs_offset_px'])
        for c in ('FRONT', 'RIGHT', 'BACK', 'LEFT'):
            print('   %-5s feet(dx,dy)=(%3d,%3d) r%.1f  face(dx,dy)=(%3d,%3d) r%.1f  sole_dy %+d  top_dy %+d' % (
                c, rv[c]['feet']['dx'], rv[c]['feet']['dy'], rv[c]['feet']['residual'], rv[c]['face']['dx'],
                rv[c]['face']['dy'], rv[c]['face']['residual'], rv[c]['sole_dy'], rv[c]['top_dy']))
    json.dump(res[sheet], open(OUT + f'{folder}/register_{sheet}.json', 'w'), indent=1)
