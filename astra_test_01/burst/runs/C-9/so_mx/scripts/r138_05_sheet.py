# R-C9-138/140 sheets from the gear_stills renders (look/r138_before, look/r138_after):
#   R-C9-138_before_after.png   8 headings x (idle, walk, Fire Ball at its release) -- BEFORE | AFTER side by side
#   R-C9-138_idle_candidates.png  the idle: before (ss134f), A (the pitch-fixed idle, the pick), B (sword-and-shield idle 4), 8 headings
#   R-C9-140_hood_hair.png      hood ON (hair off) and hood OFF (hair back), front and 3/4, idle and walk, 3x crop of the head
#   R-C9-138_more_states.png    run, Meteor at its release, block: before | after, 8 headings
# Crops are placed on the character's ID-pass bounding box (the black-ground ID image), so nothing is guessed.
import os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
B, A = os.path.join(R, 'look/r138_before'), os.path.join(R, 'look/r138_after')
HD = [0, 45, 90, 135, 180, 225, 270, 315]
try:
    FONT = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18); FS = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 14)
except Exception:
    FONT = FS = ImageFont.load_default()


def shot(d, stack, clip, h, cell=300, head=False, zoom=1.0):
    p = os.path.join(d, 'stack%d_%s_h%d_s1_beauty.png' % (stack, clip, h)); q = p.replace('_beauty', '_id')
    im = Image.open(p).convert('RGB'); idm = np.asarray(Image.open(q).convert('RGB')).sum(2) > 30
    ys, xs = np.nonzero(idm)
    if head:
        top = ys.min(); cx = int(np.median(xs[ys < top + 40])); cy = top + 22; half = int(cell / 2 / zoom)
    else:
        cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2; half = int(max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 + 12)
        half = max(half, int(cell / 2 / zoom))
    box = (cx - half, cy - half, cx + half, cy + half)
    return im.crop(box).resize((cell, cell), Image.LANCZOS)


def grid(rows, cols, cells, title, colnames, rownames, cell=300, out=None):
    W, H = 110 + cols * cell, 60 + rows * cell
    sh = Image.new('RGB', (W, H), (245, 245, 245)); dr = ImageDraw.Draw(sh)
    dr.text((10, 8), title, fill=(0, 0, 0), font=FONT)
    for j, n in enumerate(colnames): dr.text((110 + j * cell + 6, 36), n, fill=(0, 0, 0), font=FS)
    for i, n in enumerate(rownames): dr.text((8, 60 + i * cell + cell // 2 - 8), n, fill=(0, 0, 0), font=FS)
    for (i, j), im in cells.items(): sh.paste(im, (110 + j * cell, 60 + i * cell))
    sh.save(out); print('wrote', out, sh.size)


L = os.path.join(R, 'look')
# 1. before | after, idle / walk / Fire Ball
cols = [('idle', 'idle'), ('walk', 'walk'), ('cast_fireball_m', 'Fire Ball @ release 0.2667 s')]
cells = {}
for i, h in enumerate(HD):
    for j, (c, _) in enumerate(cols):
        cells[(i, 2 * j)] = shot(B, 0, c, h); cells[(i, 2 * j + 1)] = shot(A, 0, c, h)
grid(8, 6, cells, 'R-C9-138: the arena kit (orb staff + shield) -- BEFORE ss134f | AFTER ss138a, play camera, 8 headings (heading 45 faces the camera)',
     sum([['%s BEFORE' % n, '%s AFTER' % n] for _, n in cols], []), ['h%d' % h for h in HD], out=os.path.join(L, 'R-C9-138_before_after.png'))
# 2. the idle candidates
cells = {}
for i, h in enumerate(HD):
    cells[(i, 0)] = shot(B, 0, 'idle', h); cells[(i, 1)] = shot(A, 0, 'idle', h); cells[(i, 2)] = shot(A, 0, 'idle_ss4', h)
grid(8, 3, cells, 'R-C9-138 idle: BEFORE (torso -5.9 deg, leaning back) | A: pitch-fixed (+2.8, the pick) | B: sword-and-shield idle 4 (+6.9, knees 46)',
     ['BEFORE (ss134f idle)', 'A (ss138a idle)', 'B (idle_ss4, ?soidle=ss4)'], ['h%d' % h for h in HD], out=os.path.join(L, 'R-C9-138_idle_candidates.png'))
# 3. hood on / off (R-C9-140): front = h45, 3/4 = h0 and h90; 3x head crops and full figure
cells = {}; rn = []
for i, (c, h) in enumerate([('idle', 45), ('idle', 0), ('idle', 90), ('walk', 45), ('walk', 90), ('idle', 225)]):
    cells[(i, 0)] = shot(A, 0, c, h); cells[(i, 1)] = shot(A, 0, c, h, head=True, zoom=3.0)
    cells[(i, 2)] = shot(A, 1, c, h); cells[(i, 3)] = shot(A, 1, c, h, head=True, zoom=3.0); rn.append('%s h%d' % (c, h))
grid(6, 4, cells, 'R-C9-140: hood ON = hair off (hood_hair morph 1) | hood OFF = hair back (G gear), ss138a, front (h45), 3/4 (h0/h90), back (h225)',
     ['hood ON', 'hood ON, head 3x', 'hood OFF', 'hood OFF, head 3x'], rn, out=os.path.join(L, 'R-C9-140_hood_hair.png'))
# 4. more states
cols = [('run', 'run'), ('cast_meteor', 'Meteor @ release 1.80 s'), ('block', 'block')]
cells = {}
for i, h in enumerate(HD):
    for j, (c, _) in enumerate(cols):
        cells[(i, 2 * j)] = shot(B, 0, c, h); cells[(i, 2 * j + 1)] = shot(A, 0, c, h)
grid(8, 6, cells, 'R-C9-138: run, Meteor, block -- BEFORE ss134f | AFTER ss138a, 8 headings',
     sum([['%s BEFORE' % n, '%s AFTER' % n] for _, n in cols], []), ['h%d' % h for h in HD], out=os.path.join(L, 'R-C9-138_more_states.png'))
