# Conductor seed geometry (seed.py precedent, C-1 conductor_scripts): the judged rest still, cropped to its alpha bbox, UNIFORMLY downscaled to 70 % of a 1024x1536 #00ff00 canvas height, feet at row 1428 (93 %), centred — headroom for jump apex and staff raise. Uniform scale + translation only.
import sys, json, hashlib, pathlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from PIL import Image
import numpy as np
from gates import matte
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); out = B/'runs/C-3/artifacts/K2c-pad'; out.mkdir(parents=True, exist_ok=True)
src = {'S': B/'runs/C-1/artifacts/K1p-gen-01/k1p_master_C.png', **{d: B/f'runs/C-3/artifacts/K2c-gen-{d}/k2c_{d}.png' for d in ['SW','W','NW','N','NE','E','SE']}}
meta = {}
for d, p in src.items():
    im = Image.open(p).convert('RGB'); rgba, info = matte.extract(im, alpha_floor=40); a = np.array(rgba)[..., 3]
    ys, xs = np.where(a >= 128); x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1
    H = 1075; s = H/(y1-y0); W = round((x1-x0)*s)
    fig = im.crop((x0, y0, x1, y1)).resize((W, H), Image.LANCZOS)
    c = Image.new('RGB', (1024, 1536), (0, 255, 0)); px, py = round(512 - W/2), 1428 - H; c.paste(fig, (px, py))
    f = out/f'pad_{d}.png'; c.save(f)
    meta[d] = dict(source=str(p), bbox=[x0, y0, x1, y1], scale=round(s, 4), paste=[px, py], headroom_px=py, sha256=hashlib.sha256(f.read_bytes()).hexdigest())
json.dump(meta, open(out/'pad_seeds.json', 'w'), indent=1); print({d: (m['scale'], m['headroom_px']) for d, m in meta.items()})
