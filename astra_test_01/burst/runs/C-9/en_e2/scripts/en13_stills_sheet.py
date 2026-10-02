# EN-E2: the 8-heading stills sheet (rows idle / walk / cast_bolt at release / death at its end; columns headings 0..315) from the
# Godot stills (beauty pass, play camera, 100.6 px/m at scale 1), each cell cropped to a fixed window around the figure's origin.
#   python3 scripts/en13_stills_sheet.py <stills_dir> <out.png> <title>
import sys, glob, os, re
from PIL import Image, ImageDraw
D, OUT, TITLE = sys.argv[1:4]
rows = ['idle', 'walk', 'cast_bolt', 'death']; heads = [0, 45, 90, 135, 180, 225, 270, 315]
files = glob.glob(os.path.join(D, '*_beauty.png'))
def find(clip, h):
    for f in files:
        b = os.path.basename(f)
        if re.match(r'stack0_%s@[0-9.]+_h%d_s1_beauty\.png' % (clip, h), b): return f
CW, CH = 320, 420
sheet = Image.new('RGB', (CW * 8 + 90, CH * 4 + 40), (236, 230, 216)); dr = ImageDraw.Draw(sheet)
dr.text((10, 10), TITLE, fill=(0, 0, 0))
for j, h in enumerate(heads): dr.text((90 + j * CW + CW // 2 - 20, 26), 'h%d' % h, fill=(0, 0, 0))
for i, c in enumerate(rows):
    dr.text((8, 40 + i * CH + CH // 2), c, fill=(0, 0, 0))
    for j, h in enumerate(heads):
        f = find(c, h)
        if not f: continue
        im = Image.open(f).convert('RGB'); W, H = im.size
        cx, cy = W // 2, H // 2 + 10
        sheet.paste(im.crop((cx - CW // 2, cy - CH // 2 - 30, cx + CW // 2, cy + CH // 2 - 30)), (90 + j * CW, 40 + i * CH))
sheet.save(OUT); print('wrote', OUT, sheet.size)
