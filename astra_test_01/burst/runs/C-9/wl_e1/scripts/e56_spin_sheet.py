# R-C9-132/133 SPIN SHEET: rows of 8 headings (Godot stills, 2x, cropped round the figure) with a label strip, and the wwcr
# reference crops (look_k/ref_wwcr_crops.png) as the top row.  e56_spin_sheet.py <out.png> <ref.png> <label>=<dir>:<stack>:<shot> ...
import sys, numpy as np
from PIL import Image, ImageDraw
out, ref = sys.argv[1:3]; rows = []
CW, CH = 520, 600
for spec in sys.argv[3:]:
    lab, rest = spec.split('=', 1); d, st, shot = rest.split(':', 2); ims = []
    for h in range(0, 360, 45):
        im = Image.open('%s/stack%s_%s_h%d_s2_beauty.png' % (d, st, shot, h)).convert('RGB')
        idm = np.asarray(Image.open('%s/stack%s_%s_h%d_s2_id.png' % (d, st, shot, h)).convert('RGB')).astype(int).sum(2) > 30
        ys, xs = np.nonzero(idm); cx, cy = int((xs.min() + xs.max()) / 2), int((ys.min() + ys.max()) / 2)
        c = im.crop((cx - 380, cy - 440, cx + 380, cy + 440)).resize((CW, CH)); ImageDraw.Draw(c).text((8, 8), 'h%d' % h, fill=(0, 0, 0)); ims.append(c)
    row = Image.new('RGB', (CW * 8, CH + 28), (255, 255, 255)); ImageDraw.Draw(row).text((8, 6), lab, fill=(0, 0, 0))
    for i, x in enumerate(ims): row.paste(x, (i * CW, 28))
    rows.append(row)
R = Image.open(ref).convert('RGB'); R = R.resize((CW * 8, int(R.height * CW * 8 / R.width)))
hdr = Image.new('RGB', (CW * 8, R.height + 28), (255, 255, 255)); ImageDraw.Draw(hdr).text((8, 6), 'REFERENCE (wwcr harness, 2026-08-24): extended-arm spin frames', fill=(0, 0, 0)); hdr.paste(R, (0, 28))
S = Image.new('RGB', (CW * 8, hdr.height + sum(r.height for r in rows)), (255, 255, 255)); y = 0
for r in [hdr] + rows: S.paste(r, (0, y)); y += r.height
S.save(out); print(out, S.size)
