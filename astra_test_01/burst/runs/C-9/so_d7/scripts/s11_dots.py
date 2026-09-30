# Name every remaining pale DOT (s11_count's isolated-speckle rule) and say what is BEHIND it.
#   python3 scripts/s11_dots.py <dir> <tag> [--sheet out.png]
# Needs the stills harness's extra passes (stills.json "id_nobody" and "depth_passes"):
#   idnb  the ID pass with the body HIDDEN -- is there garment behind the dot at all?
#   zb/zg view DEPTH of the body alone and of the garments alone, as colour (57..63 m, R coarse,
#         G fine, sRGB pre-compensated in the shader)
# "Garment behind" is NOT enough to call a poke: through a real opening the ray meets the body and
# then the robe's far side, and the first version of this tool called all 8 dots pokes that way.
# So: POKE when the nearest garment behind the body pixel is within 3 cm of it (the body is just in
# front of the cloth that should cover it); GAP when it is farther (no near cloth on that line of
# sight -- a hole or slit in the near layer, and the body behind it is simply exposed).
import glob, json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
D, TAG = sys.argv[1], sys.argv[2]
SHEET = sys.argv[sys.argv.index('--sheet') + 1] if '--sheet' in sys.argv else None
from collections import Counter
res = Counter(); rows = []; tiles = []


def zdec(p):
    A = np.asarray(Image.open(p).convert('RGB')).astype(float)
    return np.where(A[..., 2] > 250, 57.0 + (A[..., 0] + A[..., 1] / 255.0) / 255.0 * 6.0, np.nan)


for idp in sorted(glob.glob(os.path.join(D, '%s_*_id.png' % TAG))):
    bp = idp[:-len('_id.png')] + '_beauty.png'; nbp = idp[:-len('_id.png')] + '_idnb.png'
    if not os.path.exists(nbp):
        continue
    I = np.asarray(Image.open(idp).convert('RGB')).astype(int)
    B = np.asarray(Image.open(bp).convert('RGB')).astype(int)
    N = np.asarray(Image.open(nbp).convert('RGB')).astype(int)
    body = (I[..., 0] > 200) & (I[..., 1] < 60) & (I[..., 2] < 60)
    garm = (I[..., 2] > 200) & (I[..., 0] < 60) & (I[..., 1] < 60)
    pale = B.min(-1) > 170
    m = re.search(r'%s_(.+?)_h(\d+)_s(\d+)_id\.png$' % re.escape(TAG), idp)
    sc = int(m.group(3)); MAXC = 6 * sc * sc
    lab, n = ndimage.label(body, np.ones((3, 3)))
    if not n:
        continue
    sizes = ndimage.sum(body, lab, range(1, n + 1))
    big = np.isin(lab, (np.nonzero(sizes > MAXC)[0] + 1))
    near = ndimage.binary_dilation(big, np.ones((3, 3)), iterations=2 * sc)
    sil = I.sum(-1) > 90; sy, sx = np.nonzero(sil)
    for ci in np.nonzero(sizes <= MAXC)[0] + 1:
        cm = lab == ci
        ring = ndimage.binary_dilation(cm, np.ones((3, 3))) & ~cm
        if not (ring.sum() and (garm & ring).sum() / ring.sum() >= 0.75) or (cm & near).any() or not (cm & pale).any():
            continue
        ys, xs = np.nonzero(cm & pale)
        zbp = idp[:-len('_id.png')] + '_zb.png'; zgp = idp[:-len('_id.png')] + '_zg.png'
        if os.path.exists(zbp) and os.path.exists(zgp):
            ZB, ZG = zdec(zbp), zdec(zgp)
            gaps = [float(ZG[y, x] - ZB[y, x]) for y, x in zip(ys, xs)]
            kinds = ['poke' if (g == g and g < 0.03) else ('gap' if g == g else 'gap(no cloth behind)') for g in gaps]
        else:
            gaps = []
            kinds = ['cloth-behind' if (N[y, x][2] > 200 and N[y, x][0] < 60) else 'nothing-behind' for y, x in zip(ys, xs)]
        for k in kinds:
            res[k] += 1
        y, x = int(ys.mean()), int(xs.mean())
        rows.append(dict(still='%s h%s s%s' % m.groups(), px=[x, y], pale_px=int(len(ys)), behind=kinds,
                         cloth_behind_by_m=[round(g, 4) if g == g else None for g in gaps],
                         height_from_top=round((y - sy.min()) / max(1, sy.max() - sy.min()), 2)))
        if SHEET:
            h = 24 * sc; y0, x0 = max(0, y - h), max(0, x - h)
            t = Image.new('RGB', (720, 262), 'white')
            for k_, A in enumerate((B, I, N)):
                t.paste(Image.fromarray(A[y0:y + h, x0:x + h].astype(np.uint8)).resize((240, 240), Image.NEAREST), (240 * k_, 22))
            ImageDraw.Draw(t).text((4, 4), '%s  (%d,%d)  %s   [beauty | id | id, body hidden]' % (rows[-1]['still'], x, y, ','.join(sorted(set(kinds)))), fill='black')
            tiles.append(t)
for r in rows:
    print('  %-24s px %-12s pale %d  %s  cloth behind by %s m' % (r['still'], r['px'], r['pale_px'], r['behind'], r['cloth_behind_by_m']))
print('  pale dot pixels: %s' % dict(res))
if SHEET and tiles:
    W = Image.new('RGB', (720, 262 * len(tiles)), 'white')
    for i, t in enumerate(tiles):
        W.paste(t, (0, 262 * i))
    W.save(SHEET)
json.dump(dict(dots=rows, behind=dict(res)), open(os.path.join(D, '%s_dots.json' % TAG), 'w'), indent=1)
