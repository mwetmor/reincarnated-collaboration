# bm_mx: the 8-heading STILLS SHEET from the Godot stills (gear_stills.gd naming stack<k>_<clip>@<t>_h<h>_s<scale>_<mode>.png):
# one row per shot, one column per heading; each cell cropped round the figure AND the weapon (the ID pass, every non-black pixel),
# all cells the same size (the largest extent over the sheet, so the scale is shared and the maul is never cut off).
#   python3 bm06_sheet.py <dir> <stack> <scale> <out.jpg> <clip@t,clip@t,...> [--labels a,b,...]
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
a = sys.argv[1:]; D, ST, SC, OUT = a[0], a[1], a[2], a[3]; SHOTS = a[4].split(',')
LAB = a[a.index('--labels') + 1].split(',') if '--labels' in a else SHOTS
HS = list(range(0, 360, 45))
def nm(sh, h, mode):
    c, t = sh.split('@'); return '%s/stack%s_%s@%.2f_h%d_s%s_%s.png' % (D, ST, c, float(t), h, SC, mode)
boxes = {}
for sh in SHOTS:
    for h in HS:
        m = np.asarray(Image.open(nm(sh, h, 'id')).convert('RGB')).astype(int).sum(2) > 30; ys, xs = np.nonzero(m)
        boxes[(sh, h)] = (xs.min(), ys.min(), xs.max(), ys.max())
w = max(b[2] - b[0] for b in boxes.values()) + 24; hgt = max(b[3] - b[1] for b in boxes.values()) + 24
LW = 150; font = ImageFont.load_default()
S = Image.new('RGB', (LW + w * 8, 30 + hgt * len(SHOTS)), (245, 245, 245)); dr = ImageDraw.Draw(S)
for j, h in enumerate(HS): dr.text((LW + j * w + w // 2 - 20, 8), 'heading %d' % h, fill=(0, 0, 0), font=font)
for i, sh in enumerate(SHOTS):
    dr.text((8, 30 + i * hgt + hgt // 2), LAB[i], fill=(0, 0, 0), font=font)
    for j, h in enumerate(HS):
        b = boxes[(sh, h)]; cx, cy = (b[0] + b[2]) // 2, (b[1] + b[3]) // 2
        S.paste(Image.open(nm(sh, h, 'beauty')).convert('RGB').crop((cx - w // 2, cy - hgt // 2, cx - w // 2 + w, cy - hgt // 2 + hgt)), (LW + j * w, 30 + i * hgt))
S.save(OUT, quality=88); print(OUT, S.size)
