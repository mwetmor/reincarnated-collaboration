# R-C9-120: where body pixels APPEAR (cyan) or DISAPPEAR (magenta) between two id-pass still sets, painted on the AFTER beauty.
#   python3 r10_diffsheet.py <before_dir> <after_dir> <out.png> <shot> [<shot> ...]      (shot like run_h25)
import sys
import numpy as np
from PIL import Image
A_, B_, OUT = sys.argv[1:4]; tiles = []
red = lambda a: (a[..., 0] > 200) & (a[..., 1] < 50) & (a[..., 2] < 50)
for s in sys.argv[4:]:
    A = np.array(Image.open(f'{A_}/stack0_{s}_s1_id.png').convert('RGB')); B = np.array(Image.open(f'{B_}/stack0_{s}_s1_id.png').convert('RGB'))
    ra, rb = red(A), red(B); o = np.array(Image.open(f'{B_}/stack0_{s}_s1_beauty.png').convert('RGB'))
    o[rb & ~ra] = [0, 255, 255]; o[ra & ~rb] = [255, 0, 255]
    m = (B.sum(2) > 0) | (A.sum(2) > 0); ys, xs = np.where(m); t = o[ys.min() - 4:ys.max() + 4, xs.min() - 4:xs.max() + 4]
    tiles.append(np.array(Image.fromarray(t).resize((t.shape[1] * 3, t.shape[0] * 3), Image.NEAREST)))
    print(s, 'appear', int((rb & ~ra).sum()), 'disappear', int((ra & ~rb).sum()))
H = max(t.shape[0] for t in tiles); out = np.full((H, sum(t.shape[1] for t in tiles), 3), 255, np.uint8); x = 0
for t in tiles: out[:t.shape[0], x:x + t.shape[1]] = t; x += t.shape[1]
Image.fromarray(out).save(OUT)
