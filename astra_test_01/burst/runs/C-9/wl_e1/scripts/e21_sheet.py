# 8-heading contact sheet from the Godot stills: crop each 2x beauty still round the figure. e21_sheet.py <dir> <stack> <out.png>
import sys, glob, numpy as np
from PIL import Image
d, st, out = sys.argv[1:4]; ims = []
for h in range(0, 360, 45):
    im = Image.open('%s/stack%s_idle_h%d_s2_beauty.png' % (d, st, h)).convert('RGB'); a = np.asarray(im).astype(int)
    idm = np.asarray(Image.open('%s/stack%s_idle_h%d_s2_id.png' % (d, st, h)).convert('RGB')).astype(int).sum(2) > 30
    ys, xs = np.nonzero(idm); cx, cy = int(xs.mean()), int((ys.min() + ys.max()) / 2)
    ims.append(im.crop((cx - 230, cy - 330, cx + 230, cy + 330)))
W = Image.new('RGB', (460 * 8, 660)); [W.paste(x, (i * 460, 0)) for i, x in enumerate(ims)]; W.save(out); print(out, W.size)
