# so_mx: a stills sheet -- rows = shots, columns = headings, each tile cropped to the union of the figure across the sheet.
#   python3 so20_sheet.py <stills_dir> <out.jpg> <scale> <title> <clip>[:label] ...   (headings from the files)
import sys, glob, re, os
import numpy as np
from PIL import Image, ImageDraw
D, OUT, SC, TITLE = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]; shots = sys.argv[5:]
rows = []
for s in shots:
    clip, lab = (s.split(':') + [s])[:2]
    fs = sorted(glob.glob('%s/stack0_%s_h*_s%d_beauty.png' % (D, clip, SC)), key=lambda f: int(re.search(r'_h(\d+)_', f).group(1)))
    rows.append((lab, [np.array(Image.open(f).convert('RGB')) for f in fs]))
allim = [im for _, ims in rows for im in ims]; bg = allim[0][2, 2].astype(int)
m = np.any([np.abs(im.astype(int) - bg).sum(2) > 30 for im in allim], axis=0); ys, xs = np.where(m); p = 10 * SC
y0, y1, x0, x1 = max(ys.min() - p, 0), ys.max() + p, max(xs.min() - p, 0), xs.max() + p
tiles = [(lab, np.hstack([im[y0:y1, x0:x1] for im in ims])) for lab, ims in rows]
Wd = max(t.shape[1] for _, t in tiles); H = sum(t.shape[0] for _, t in tiles)
c = Image.new('RGB', (Wd + 170, H + 34), 'white'); dr = ImageDraw.Draw(c); dr.text((8, 8), TITLE, fill=(0, 0, 0)); y = 34
for lab, t in tiles:
    c.paste(Image.fromarray(t), (170, y)); dr.text((8, y + t.shape[0] // 2), lab, fill=(0, 0, 0)); y += t.shape[0]
c.save(OUT, quality=88); print(OUT, c.size)
