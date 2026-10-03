# R-C9-152 sheets: LIVE (ss138a, hair morph) vs A (ss152a, hood cap incl. braid) vs B (ss152b, cap above 1.30 m + braid
# tucked), hood on, and hood off -- 8 headings; per clip a 3x head-and-back crop and a 1x play-distance figure.
import os, numpy as np
from PIL import Image, ImageDraw
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'look')
H = [0, 45, 90, 135, 180, 225, 270, 315]
ROWS = [('r152_live_cb', 0, 'LIVE ss138a (hair pulled in), hood on'), ('r152_fix_cb', 0, 'A ss152a: hood cap incl. braid, hood on'),
        ('r152_fixb_cb', 0, 'B ss152b: cap + braid tucked, hood on'), ('r152_fix_cb', 1, 'hood off (A and B: hair unchanged)')]
def crop(d, st, c, h, s, half):
    im = Image.open(f'{L}/{d}/stack{st}_{c}_h{h}_s{s}_beauty.png').convert('RGB')
    idm = np.asarray(Image.open(f'{L}/{d}/stack{st}_{c}_h{h}_s{s}_id.png').convert('RGB')).sum(2) > 30
    ys, xs = np.nonzero(idm)
    if s == 3:
        top = ys.min(); cx = int(np.median(xs[ys < top + 60])); cy = top + 130
    else:
        cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
    return im.crop((cx - half, cy - half, cx + half, cy + half)).resize((220, 220), Image.LANCZOS)
for clip, lab in (('idle', 'idle'), ('walk', 'walk'), ('cast_fireball_m', 'Fire Ball @ release')):
    for s, half, tag in ((3, 170, '3x head and back'), (1, 130, 'play distance 1x')):
        S = Image.new('RGB', (230 + 8 * 220, 40 + 4 * 220), (245, 245, 245)); d = ImageDraw.Draw(S)
        d.text((8, 8), 'R-C9-152 %s, %s, 8 headings (h45 faces the camera)' % (lab, tag), fill=(0, 0, 0))
        for j, h in enumerate(H): d.text((230 + j * 220 + 5, 24), 'h%d' % h, fill=(0, 0, 0))
        for i, (dd, st, rl) in enumerate(ROWS):
            d.text((5, 40 + i * 220 + 100), rl, fill=(0, 0, 0))
            for j, h in enumerate(H): S.paste(crop(dd, st, clip, h, s, half), (230 + j * 220, 40 + i * 220))
        out = f'{L}/R-C9-152_{clip}_{"3x" if s == 3 else "1x"}.jpg'; S.save(out, quality=88); print(out)
