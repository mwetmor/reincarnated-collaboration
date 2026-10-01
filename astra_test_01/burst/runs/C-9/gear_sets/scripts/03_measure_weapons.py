# R-C9-98 proportion checks on the weapon sheets BEFORE any 3D (the W2 blade:grip lesson).
# The plates came back as dark gradients, not #00ff00, so the object mask is LOCAL CONTRAST (ink + texture), closed and
# hole-filled; views are split at empty column runs. Each view's bbox and its row-width PROFILE are written, and an overlay
# PNG is saved so the numbers can be checked by eye. Part boundaries (head / haft, crystal / shaft / grip) are found from the
# width profile, then converted to metres at a stated target length and set against the body measured on the base sheets:
#   barbarian NB-1_b front: 701 px crown-to-sole = 1.85 m (379 px/m); hand wrist-to-fingertip 85 px = 0.224 m, ~0.11 m wide
#   sorceress SO-1_b front: 736 px = 1.70 m (433 px/m); hand 76 px = 0.176 m; palm ~29 px = 0.067 m
import json, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
ART = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/artifacts/'
OUT = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/'


def mask_of(p):
    a = np.asarray(Image.open(p).convert('RGB')).astype(np.float32)
    L = a.mean(2)
    m1 = ndimage.uniform_filter(L, 5)
    ct = np.sqrt(np.maximum(ndimage.uniform_filter(L * L, 5) - m1 * m1, 0))
    m = ct > 9
    m = ndimage.binary_closing(m, iterations=6)
    m = ndimage.binary_fill_holes(m)
    m = ndimage.binary_opening(m, iterations=3)
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 3000])
    return keep, a


def views(m):
    cols = m.any(0)
    runs, x = [], 0
    W = len(cols)
    while x < W:
        if cols[x]:
            x0 = x
            while x < W and cols[x]:
                x += 1
            runs.append((x0, x))
        x += 1
    out = []
    for x0, x1 in runs:
        sub = m[:, x0:x1]
        ys = np.where(sub.any(1))[0]
        widths = sub.sum(1)
        out.append(dict(x0=int(x0), x1=int(x1), y0=int(ys.min()), y1=int(ys.max()), w=int(x1 - x0), h=int(ys.max() - ys.min()),
                        widths=widths))
    return out


def profile_runs(widths, y0, y1, thr):
    """rows (y0..y1) whose width is >= thr: returns the first/last contiguous wide band from the top"""
    rows = np.arange(y0, y1 + 1)
    wide = widths[y0:y1 + 1] >= thr
    return rows, wide


res = {}
for sheet in ('GS-BMAUL', 'GS-SWAND', 'GS-SBOOK'):
    for v in 'ab':
        p = ART + f'{sheet}/{sheet}_{v}.png'
        m, a = mask_of(p)
        V = views(m)
        rec = []
        for vw in V:
            w = vw['widths']; y0, y1 = vw['y0'], vw['y1']
            r = dict(x0=vw['x0'], x1=vw['x1'], y0=y0, y1=y1, w_px=vw['w'], h_px=vw['h'])
            if sheet == 'GS-BMAUL':
                # head = the top band wider than 2.5x the median haft width
                haft = float(np.median(w[y0 + vw['h'] // 2:y1 - vw['h'] // 8]))
                wide = np.where(w[y0:y1 + 1] > 2.5 * haft)[0]
                top = wide[wide < vw['h'] * 0.5]
                r.update(haft_w_px=haft, head_rows=[int(y0 + top.min()), int(y0 + top.max())] if len(top) else None,
                         head_h_px=int(top.max() - top.min()) if len(top) else None,
                         head_len_px=int(w[y0 + top].max()) if len(top) else None)
            if sheet == 'GS-SWAND':
                shaft = float(np.median(w[y0 + int(vw['h'] * 0.3):y0 + int(vw['h'] * 0.55)]))
                grip = float(np.median(w[y0 + int(vw['h'] * 0.72):y0 + int(vw['h'] * 0.85)]))
                r.update(shaft_w_px=shaft, grip_w_px=grip)
            rec.append(r)
        res[f'{sheet}_{v}'] = rec
        ov = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(ov)
        for r in rec:
            d.rectangle([r['x0'], r['y0'], r['x1'], r['y1']], outline=(0, 255, 0), width=3)
            if r.get('head_rows'):
                d.line([r['x0'], r['head_rows'][1], r['x1'], r['head_rows'][1]], fill=(255, 0, 255), width=3)
        folder = 'barbarian_gladiator' if 'MAUL' in sheet else 'sorceress_battlemage'
        ov.reduce(2).save(OUT + f'{folder}/measure_{sheet}_{v}.jpg', quality=88)
        print(sheet, v, [{k: (round(x, 1) if isinstance(x, float) else x) for k, x in r.items()} for r in rec])
json.dump(res, open(OUT + 'weapon_measure_raw.json', 'w'), indent=1, default=lambda o: o.tolist())
