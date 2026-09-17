# Conductor seed geometry for C-6 P3 (C-3 pad_seed.py lineage): each judged rest still cropped to its alpha bbox, UNIFORMLY scaled to
# 70 % of a 1024x1536 #00ff00 canvas height, feet at row 1428, centred. usage: pad_seed.py [D=relpath ...] (defaults: S master + N5 mints)
import sys, json, hashlib, pathlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
from PIL import Image
import numpy as np
from gates import matte
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); out = B/'runs/C-6/artifacts/N5-pad'; out.mkdir(parents=True, exist_ok=True)
over = dict(a.split('=') for a in sys.argv[1:])
src = {'S': B/'runs/C-6/artifacts/N3-final-cam-01/necro_final_cam.png', **{d: B/f'runs/C-6/artifacts/N5-turn-{d}/n5_{d}.png' for d in ['SW','W','NW','N','NE','E','SE']}}
for d, rel in over.items(): src[d] = B/rel
meta = {}
for d, p in src.items():
    im = Image.open(p).convert('RGB'); rgba, info = matte.extract(im, alpha_floor=40); a = np.array(rgba)[..., 3]
    ys, xs = np.where(a >= 128); x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1
    H = 1075; s = H/(y1-y0); W = round((x1-x0)*s)
    fig = im.crop((x0, y0, x1, y1)).resize((W, H), Image.LANCZOS)
    c = Image.new('RGB', (1024, 1536), (0, 255, 0)); px, py = round(512 - W/2), 1428 - H; c.paste(fig, (px, py))
    f = out/f'pad_{d}.png'; c.save(f)
    meta[d] = dict(source=str(p), source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bbox=[x0, y0, x1, y1], scale=round(s, 4), paste=[px, py], headroom_px=py, sha256=hashlib.sha256(f.read_bytes()).hexdigest())
json.dump(meta, open(out/'pad_seeds.json', 'w'), indent=1); print({d: (m['scale'], m['headroom_px']) for d, m in meta.items()})
