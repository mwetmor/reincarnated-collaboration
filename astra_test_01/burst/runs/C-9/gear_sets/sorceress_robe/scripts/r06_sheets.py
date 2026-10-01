# R-C9-119 / R-C9-120 before/after sheets: per shot, a row of the 4 headings BEFORE over the same 4 headings AFTER,
# each tile cropped to the union of the figure's box (pixels differing from the flat background) across the 8 tiles.
#   python3 r06_sheets.py <out.jpg> <scale> <title> <before_dir>:<clip>[:<label>] <after_dir>:<clip>[:<label>] [more pairs...]
import sys
import numpy as np
from PIL import Image, ImageDraw
a = sys.argv[1:]; OUT, SC, TITLE = a[0], int(a[1]), a[2]; pairs = a[3:]
HD = [25, 115, 205, 295]
rows = []
for k in range(0, len(pairs), 2):
    sets = []
    for spec in pairs[k:k + 2]:
        d, clip, *lab = spec.split(':')
        sets.append(([np.array(Image.open("%s/stack0_%s_h%d_s%d_beauty.png" % (d, clip, h, SC)).convert('RGB')) for h in HD], lab[0] if lab else clip))
    allim = [im for s_, _ in sets for im in s_]
    bg = allim[0][2, 2].astype(int)
    m = np.any([np.abs(im.astype(int) - bg).sum(2) > 30 for im in allim], axis=0)
    ys, xs = np.where(m); pad = 12 * SC
    y0, y1, x0, x1 = max(ys.min() - pad, 0), ys.max() + pad, max(xs.min() - pad, 0), xs.max() + pad
    for ims, lab in sets:
        rows.append((np.hstack([im[y0:y1, x0:x1] for im in ims]), lab))
Wd = max(r.shape[1] for r, _ in rows)
canvas = Image.new('RGB', (Wd + 220, sum(r.shape[0] for r, _ in rows) + 40), (255, 255, 255))
dr = ImageDraw.Draw(canvas); dr.text((10, 10), TITLE + "   headings 25 / 115 / 205 / 295, %dx" % SC, fill=(0, 0, 0))
y = 40
for r, lab in rows:
    canvas.paste(Image.fromarray(r), (220, y)); dr.text((10, y + r.shape[0] // 2), lab, fill=(0, 0, 0)); y += r.shape[0]
canvas.save(OUT, quality=88); print(OUT, canvas.size)
