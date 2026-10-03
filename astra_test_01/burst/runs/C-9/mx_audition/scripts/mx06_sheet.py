# MX audition (R-C9-149): the 8-heading stills sheet, CURRENT vs MIXAMO side by side -- per state, the clip of record's row
# first, then each candidate's row directly under it (same headings, same crop, same scale). Godot beauty stills at the play
# camera (ortho, pitch 52.95 deg, yaw 47, 100.6 px/m), each cell cropped to one fixed window about the record's origin (screen
# centre + the 0.85 m target offset), so heights compare directly across rows. Row labels carry the clip, read time and source.
#   python3 scripts/mx06_sheet.py <tag> <out.png> "<title>"
import sys, os, json, re
from PIL import Image, ImageDraw, ImageFont
tag, OUT, TITLE = sys.argv[1:4]
S = json.load(open('specs/%s.json' % tag)); cfg = json.load(open('work/stills_%s.json' % tag)); src = S.get('sources', {})
D = 'stills/%s' % tag; heads = [0, 45, 90, 135, 180, 225, 270, 315]
CW, CH, OY = int(S.get('crop_w', 400)), int(S.get('crop_h', 440)), 52          # OY: the 0.85 m target, projected (0.85 cos 52.95 x 100.6)
LW = 300
F = ImageFont.load_default(size=18); Fs = ImageFont.load_default(size=14); Ft = ImageFont.load_default(size=24)
order = []
for st in S['pairs']:
    for i, c in enumerate(st[1:]):
        if not c: continue
        for (cc, t) in cfg['shots']:
            if cc == c: order.append((st[0], i, c, t))
sheet = Image.new('RGB', (LW + CW * 8, 70 + CH * len(order)), (236, 230, 216)); dr = ImageDraw.Draw(sheet)
dr.text((10, 10), TITLE, fill=(0, 0, 0), font=Ft)
for j, h in enumerate(heads): dr.text((LW + j * CW + CW // 2 - 20, 44), 'h%d' % h, fill=(0, 0, 0), font=F)
prev = None
for r, (state, i, c, t) in enumerate(order):
    y0 = 70 + r * CH
    if state != prev and r: dr.line([(0, y0), (sheet.width, y0)], fill=(60, 60, 60), width=4)
    prev = state
    tagc = (40, 40, 160) if i == 0 else (150, 40, 20)
    dr.text((10, y0 + 20), state.upper(), fill=(0, 0, 0), font=Ft)
    dr.text((10, y0 + 56), ('RECORD: ' if i == 0 else 'MIXAMO: ') + c, fill=tagc, font=F)
    dr.text((10, y0 + 82), '@ %.2f s' % t, fill=(0, 0, 0), font=F)
    s = src.get(c, '')
    for k in range(0, len(s), 34): dr.text((10, y0 + 110 + 18 * (k // 34)), s[k:k + 34], fill=(70, 70, 70), font=Fs)
    for j, h in enumerate(heads):
        f = '%s/stack0_%s@%.2f_h%d_s1_beauty.png' % (D, c, t, h)
        if not os.path.exists(f): continue
        im = Image.open(f).convert('RGB'); W, H = im.size; cx, cy = W // 2, H // 2 + OY
        top = cy - int(CH * 0.72)
        sheet.paste(im.crop((cx - CW // 2, top, cx + CW // 2, top + CH)), (LW + j * CW, y0))
sheet.save(OUT, optimize=True); print('wrote', OUT, sheet.size, len(order), 'rows')
