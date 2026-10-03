# E1b R-C9-141 stills, all from the JOIN-1 cells themselves (the play camera, pitch 52.95 deg, ppm 151.34 -- play distance):
#  (1) R-C9-141_notch_located.png: eor2 idle S frame 0 at 1x and zoomed, the notch CIRCLED (the pixels that change eor2->eor3,
#      which are exactly the body crown showing through the helm) next to the real visor slit (the eye glow, boxed);
#  (2) R-C9-141_before_after_<state>.png: 8 headings, before (eor2 pack) over after (eor3 pack), head crops x3 plus 1x thumbs;
#  (3) R-C9-141_ice.png: the ice variant after (probe cells), 8 headings.
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
C9 = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9'
P2, P3 = C9 + '/join1_pack/gd-eor-warlord/cells', C9 + '/join1_pack/gd-eor-warlord-eor3/cells'
ICE = C9 + '/wl_e1/work/n/ice_probe/cells'; OUT = C9 + '/wl_e1/look'
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]; BG = (88, 88, 92, 255)
def cell(root, st, d, i=0):
    im = Image.open('%s/%s/%s/%s_%s_%02d.png' % (root, st, d, st, d, i)).convert('RGBA'); bg = Image.new('RGBA', im.size, BG); bg.alpha_composite(im); return bg
def diffmask(st, d, i=0):
    a = np.asarray(cell(P2, st, d, i), np.int16); b = np.asarray(cell(P3, st, d, i), np.int16); return np.abs(a - b).max(-1) > 12
def headbox(st, d, i=0):
    m = diffmask(st, d, i); ys, xs = np.nonzero(m)
    if len(xs) > 10:                                   # centre on the changed pixels = the helm crown (the mace can top the alpha)
        cx, cy = int(np.median(xs)), int(np.median(ys)); return (cx - 60, cy - 50, cx + 60, cy + 60)
    im = np.asarray(Image.open('%s/%s/%s/%s_%s_%02d.png' % (P3, st, d, st, d, i)))[..., 3] > 0
    ys, xs = np.nonzero(im); top = ys.min(); cx = int(np.median(xs[ys < top + 40])) if (ys < top + 40).any() else int(xs.mean())
    return (cx - 60, top - 10, cx + 60, top + 100)
def glow(img):
    a = np.asarray(img, np.int16); return (a[..., 2] > 200) & (a[..., 0] > 150) & (a[..., 1] < 170)
rep = {}
# (1) located
st, d = 'idle', 'S'; before = cell(P2, st, d).convert('RGB'); m = diffmask(st, d)
ys, xs = np.nonzero(m); rep['notch_px_idle_S'] = int(m.sum())
bx = headbox(st, d); Z = 6
crop = before.crop(bx).resize(((bx[2] - bx[0]) * Z, (bx[3] - bx[1]) * Z), Image.NEAREST); dr = ImageDraw.Draw(crop)
if len(xs):
    cx, cy, r = (xs.mean() - bx[0]) * Z, (ys.mean() - bx[1]) * Z, max(np.ptp(xs), np.ptp(ys)) * Z / 2 + 14
    dr.ellipse([cx - r, cy - r * 0.75, cx + r, cy + r * 0.75], outline=(255, 60, 60), width=5); dr.text((cx + r + 6, cy - 10), 'NOTCH (body crown through the helm)', fill=(255, 90, 90))
g = glow(before); gy, gx = np.nonzero(g)
sel = (gx >= bx[0]) & (gx < bx[2]) & (gy >= bx[1]) & (gy < bx[3]) & (gy > (ys.max() if len(ys) else bx[1]))   # the visor glow: below the notch (the horn-tip speck excluded)
if sel.any():
    x0, x1, y0, y1 = (gx[sel].min() - bx[0]) * Z, (gx[sel].max() - bx[0] + 1) * Z, (gy[sel].min() - bx[1]) * Z, (gy[sel].max() - bx[1] + 1) * Z
    dr.rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], outline=(120, 220, 255), width=4); dr.text((x1 + 14, y0), 'real visor slit (eye glow)', fill=(140, 230, 255))
after = cell(P3, st, d).convert('RGB').crop(bx).resize(crop.size, Image.NEAREST)
one = before.crop((bx[0] - 60, bx[1] - 20, bx[2] + 60, bx[3] + 160))
W = Image.new('RGB', (crop.width * 2 + one.width + 40, crop.height + 40), (40, 40, 44)); W.paste(one, (10, 30)); W.paste(crop, (one.width + 20, 30)); W.paste(after, (one.width + crop.width + 30, 30))
D = ImageDraw.Draw(W); D.text((10, 8), 'eor2 idle S f0, 1x (play distance)', fill='white'); D.text((one.width + 20, 8), 'eor2 x6: BEFORE', fill='white'); D.text((one.width + crop.width + 30, 8), 'eor3 x6: AFTER', fill='white')
W.save(OUT + '/R-C9-141_notch_located.png')
# (2) before/after 8 headings
for st, fr in (('idle', 0), ('eor_spin_loop', 0), ('eor_spin_start', 3)):
    Z = 3; tiles = []
    for d in DIRS:
        bx = headbox(st, d, fr); b = cell(P2, st, d, fr).convert('RGB').crop(bx); a = cell(P3, st, d, fr).convert('RGB').crop(bx)
        rep['%s_%s_changed_px' % (st, d)] = int(diffmask(st, d, fr).sum())
        t = Image.new('RGB', (b.width * Z, b.height * Z * 2 + 24), (40, 40, 44)); t.paste(b.resize((b.width * Z, b.height * Z), Image.NEAREST), (0, 24)); t.paste(a.resize((a.width * Z, a.height * Z), Image.NEAREST), (0, 24 + b.height * Z))
        ImageDraw.Draw(t).text((4, 4), '%s  top eor2 / bottom eor3' % d, fill='white'); tiles.append(t)
    W = Image.new('RGB', (sum(t.width for t in tiles) + 8 * 4, tiles[0].height), (25, 25, 28)); x = 0
    for t in tiles: W.paste(t, (x, 0)); x += t.width + 4
    W.save(OUT + '/R-C9-141_before_after_%s.png' % st)
    # 1x full-cell strip (what the player sees)
    S = Image.new('RGB', (768 // 2 * 8, 768 // 2 * 2), (25, 25, 28))
    for i, d in enumerate(DIRS):
        for r, root in enumerate((P2, P3)): S.paste(cell(root, st, d, fr).convert('RGB').crop((192, 128, 576, 512)), (i * 384, r * 384))
    S.save(OUT + '/R-C9-141_before_after_%s_1x.png' % st)
# (3) ice
if os.path.isdir(ICE):
    for st in ('idle', 'eor_spin_loop'):
        tiles = []
        for d in DIRS:
            bx = headbox(st, d); c = cell(ICE, st, d).convert('RGB').crop(bx); tiles.append(c.resize((c.width * 3, c.height * 3), Image.NEAREST))
        W = Image.new('RGB', (sum(t.width for t in tiles) + 32, tiles[0].height), (25, 25, 28)); x = 0
        for t in tiles: W.paste(t, (x, 0)); x += t.width + 4
        W.save(OUT + '/R-C9-141_ice_%s.png' % st)
print(json.dumps(rep))
json.dump(rep, open(C9 + '/wl_e1/work/n/stills_report.json', 'w'), indent=1)
