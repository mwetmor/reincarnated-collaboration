# Conductor sheet composition for the gear paint-over (seed.py precedent: uniform scale + translation only, recorded for inversion).
# usage: paint_sheet.py <frames_dir> <label> <cols> <rows>
import sys, json, glob, hashlib, pathlib
from PIL import Image
import numpy as np
fd, label, cols, rows = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
out = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-3/artifacts/P5-sheets'); out.mkdir(parents=True, exist_ok=True)
files = sorted(glob.glob(fd + '/*_[0-9][0-9].png')); assert len(files) == cols * rows, (len(files), cols * rows)
ims = [Image.open(f).convert('RGBA') for f in files]
al = np.maximum.reduce([np.array(i)[..., 3] for i in ims]); ys, xs = np.where(al >= 16)
x0, y0, x1, y1 = max(0, xs.min() - 8), max(0, ys.min() - 8), min(512, xs.max() + 9), min(512, ys.max() + 9)
W, H = 1024, 1536; cw, ch = W // cols, H // rows
s = min(0.92 * ch / (y1 - y0), 0.92 * cw / (x1 - x0))
sheet = Image.new('RGB', (W, H), (0, 255, 0)); cells = []
for k, im in enumerate(ims):
    crop = im.crop((x0, y0, x1, y1)); tw, th = round((x1 - x0) * s), round((y1 - y0) * s)
    crop = crop.resize((tw, th), Image.LANCZOS); c, r = k % cols, k // cols
    px, py = c * cw + (cw - tw) // 2, r * ch + (ch - th) // 2
    sheet.paste(crop, (px, py), crop); cells.append(dict(frame=pathlib.Path(files[k]).name, cell=[c, r], paste=[px, py], size=[tw, th]))
p = out / f'sheet_{label}.png'; sheet.save(p)
meta = dict(source_dir=fd, label=label, cols=cols, rows=rows, sheet=[W, H], cell=[cw, ch], union_crop_512=[int(x0), int(y0), int(x1), int(y1)], scale=s, cells=cells,
            inverse='frame_512 = paste back: cell region [paste, paste+size] resized to (x1-x0, y1-y0) with LANCZOS, placed at (x0,y0) on a 512 transparent canvas', sha256=hashlib.sha256(p.read_bytes()).hexdigest())
json.dump(meta, open(out / f'sheet_{label}.json', 'w'), indent=1); print(label, 'scale', round(s, 3), 'crop', meta['union_crop_512'])
