#!/usr/bin/env python3
"""BV2F LV M1 cover sheet (R-C9-180 W4): one phone screen, three asks with one recommendation each, a slot for P6'.
    python3 fid/lv/tools/lv_m1_cover.py [P6' result text]   -> fid/lv/M1/M1_cover.jpg"""
import os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); M1 = os.path.join(os.path.dirname(HERE), "M1")
P6 = sys.argv[1] if len(sys.argv) > 1 else "P6' (geometry agreement, as-built extents): PENDING -- PH re-measure"
W, H = 1080, 1920
im = Image.new("RGB", (W, H), (22, 22, 26)); d = ImageDraw.Draw(im)
f = lambda n: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", n)
fr = lambda n: ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", n)
y = 40
d.text((40, y), "barrow_v2 - M1", fill=(255, 255, 255), font=f(64)); y += 90
mp = Image.open(os.path.join(M1, "M1_map_v7c.jpg")).convert("RGB"); mp.thumbnail((1000, 500))
im.paste(mp, ((W - mp.width) // 2, y)); y += mp.height + 30
asks = [
    ("1. Which layout?", "RECOMMENDED: v7c.", "v7c passes every check: all six spawn openings are visible from the game camera. It also separates the fallen gable again as its own ruin, reversing the merged hall you saw after R-C9-148. v7b is shown for comparison only: it fails the visibility check (the hall door faces away, the sea cave is hidden)."),
    ("2. The burnt hall: open sides?", "RECOMMENDED: keep it closed-sided except the one great door.", "The burnt walls stay walls, so the painter cannot read gaps as extra entrances (no false doorways). The tall part of the entrance is a raised roof bay set back about 5-8 m behind the great door; at the door itself the porch stands about 5 m."),
    ("3. How do you walk it?", "RECOMMENDED: the .command on the Mac now.", "Double-click 'Walk barrow_v2 v7c.command'. A packaged .app can follow later, once there is disk space."),
]
for t, rec, why in asks:
    d.text((40, y), t, fill=(255, 225, 120), font=f(46)); y += 62
    for line in textwrap.wrap(rec, 40):
        d.text((60, y), line, fill=(140, 230, 140), font=f(38)); y += 48
    for line in textwrap.wrap(why, 52):
        d.text((60, y), line, fill=(225, 225, 225), font=fr(32)); y += 40
    y += 26
d.rectangle([30, y, W - 30, y + 150], outline=(120, 180, 255), width=4)
for i, line in enumerate(textwrap.wrap(P6, 56)[:3]):
    d.text((50, y + 18 + 42 * i), line, fill=(170, 210, 255), font=fr(32))
im.save(os.path.join(M1, "M1_cover.jpg"), quality=90)
print("cover", y + 150, "px used of", H)
